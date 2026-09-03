from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date
from pathlib import Path

from goldrising.workspace import Workspace


def _setup_logging(ws: Workspace) -> None:
    ws.logs_dir.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    handlers.append(logging.FileHandler(ws.logs_dir / "daily.log", encoding="utf-8"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", handlers=handlers)


def _load_env_file(root: Path) -> None:
    """读取 .env（若存在）注入进程环境；只处理 KEY=VALUE 行，不打印任何值。"""
    import os

    p = root / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k and k not in os.environ:
            os.environ[k] = v.strip().strip('"').strip("'")


def cmd_registry(args: argparse.Namespace, ws: Workspace) -> int:
    from goldrising.contracts import load_registry

    reg = load_registry(ws.registry_path)
    if args.verb == "validate":
        n_col, n_der = len(reg.collectable()), len(reg.derived_in_order())
        print(f"注册表有效：{len(reg.indicators)} 个指标，{n_col} 个可采集，{n_der} 个派生")
        return 0
    for ind in reg.indicators:
        flag = "" if ind.collect else f"  [未接入，第 {ind.stage} 阶段]"
        print(f"{ind.id:22s} T{ind.tier:6s} {ind.group:18s} {ind.source.provider:18s} {ind.name}{flag}")
    return 0


def cmd_data(args: argparse.Namespace, ws: Workspace) -> int:
    from goldrising.contracts import load_registry
    from goldrising.data.fetch import fetch_all

    reg = load_registry(ws.registry_path)
    only = set(args.only.split(",")) if args.only else None
    rep = fetch_all(ws, reg, only=only, today=_today(args))
    for r in rep.results:
        print(f"{r.status:8s} {r.indicator_id:22s} {r.as_of:10s} {r.message[:100]}")
    print(f"成功 {len(rep.ok)}，失败 {len(rep.failed)}，跳过 {len([r for r in rep.results if r.status == 'skipped'])}")
    return 1 if rep.failed and not rep.ok else 0


def cmd_compute(args: argparse.Namespace, ws: Workspace) -> int:
    from goldrising.compute.snapshot import build_snapshot
    from goldrising.contracts import load_registry

    reg = load_registry(ws.registry_path)
    snap = build_snapshot(ws, reg, today=_today(args), fetch_report=_latest_fetch_report(ws))
    n_missing, n_fail = len(snap["missing"]), len(snap["derived_failures"])
    print(f"快照已生成：{len(snap['indicators'])} 个指标，缺失 {n_missing}，派生失败 {n_fail}")
    for f in snap["derived_failures"]:
        print("  派生失败:", f)
    return 0


def cmd_render(args: argparse.Namespace, ws: Workspace) -> int:
    from goldrising.publish.site import write_site

    latest = ws.snapshots_dir / "latest.json"
    if not latest.exists():
        print("缺少快照，请先运行 gold compute run", file=sys.stderr)
        return 1
    snap = json.loads(latest.read_text(encoding="utf-8"))
    out = write_site(ws.site_dir, snap)
    print(f"页面已生成：{out}")
    return 0


def cmd_run(args: argparse.Namespace, ws: Workspace) -> int:
    from goldrising.compute.snapshot import build_snapshot
    from goldrising.contracts import load_registry
    from goldrising.data.fetch import fetch_all
    from goldrising.publish.site import git_publish, write_site

    reg = load_registry(ws.registry_path)
    today = _today(args)
    report = None
    if not args.no_fetch:
        rep = fetch_all(ws, reg, today=today)
        report = rep.to_dict()
        logging.getLogger("gold").info("抓取完成：成功 %d 失败 %d", len(rep.ok), len(rep.failed))
    snap = build_snapshot(ws, reg, today=today, fetch_report=report or _latest_fetch_report(ws))
    out = write_site(ws.site_dir, snap)
    msg = git_publish(ws.root, str(snap["run_date"]))
    print(f"完成：{out}；发布：{msg}")
    return 0


def _today(args: argparse.Namespace) -> date | None:
    d = getattr(args, "date", None)
    return date.fromisoformat(d) if d else None


def _latest_fetch_report(ws: Workspace) -> dict[str, object] | None:
    reports = sorted(ws.logs_dir.glob("fetch_*.json"))
    if not reports:
        return None
    return dict(json.loads(reports[-1].read_text(encoding="utf-8")))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gold", description="黄金大作手仪表盘")
    p.add_argument("--root", help="仓库根目录（默认自动探测）")
    sub = p.add_subparsers(dest="domain", required=True)

    reg = sub.add_parser("registry", help="指标注册表")
    reg.add_argument("verb", choices=["validate", "list"])
    reg.set_defaults(func=cmd_registry)

    data = sub.add_parser("data", help="数据抓取")
    data.add_argument("verb", choices=["fetch"])
    data.add_argument("--only", help="只抓取这些指标 id，逗号分隔")
    data.add_argument("--date", help="运行日期 YYYY-MM-DD（默认今天 UTC）")
    data.set_defaults(func=cmd_data)

    comp = sub.add_parser("compute", help="计算快照")
    comp.add_argument("verb", choices=["run"])
    comp.add_argument("--date")
    comp.set_defaults(func=cmd_compute)

    rend = sub.add_parser("render", help="渲染页面")
    rend.add_argument("verb", choices=["page"])
    rend.set_defaults(func=cmd_render)

    run = sub.add_parser("run", help="每日全流程")
    run.add_argument("verb", choices=["daily"])
    run.add_argument("--no-fetch", action="store_true")
    run.add_argument("--date")
    run.set_defaults(func=cmd_run)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ws = Workspace(Path(args.root).resolve()) if args.root else Workspace.default()
    ws.ensure()
    _load_env_file(ws.root)
    _setup_logging(ws)
    return int(args.func(args, ws))


if __name__ == "__main__":
    raise SystemExit(main())
