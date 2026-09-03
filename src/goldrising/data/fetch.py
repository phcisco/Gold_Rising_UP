"""抓取编排：遍历注册表中可采集的指标，逐个调用提供方，成功入库，失败记录。绝不静默。"""

from __future__ import annotations

import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta

from goldrising.contracts import Indicator, Registry
from goldrising.data.providers import FetchContext, ProviderError, get_provider
from goldrising.data.store import CuratedStore
from goldrising.workspace import Workspace

log = logging.getLogger(__name__)


@dataclass
class FetchResult:
    indicator_id: str
    status: str  # ok | failed | skipped
    message: str = ""
    as_of: str = ""
    rows: int = 0
    seconds: float = 0.0


@dataclass
class FetchReport:
    run_date: str
    results: list[FetchResult] = field(default_factory=list)

    @property
    def failed(self) -> list[FetchResult]:
        return [r for r in self.results if r.status == "failed"]

    @property
    def ok(self) -> list[FetchResult]:
        return [r for r in self.results if r.status == "ok"]

    def to_dict(self) -> dict[str, object]:
        return {"run_date": self.run_date, "results": [asdict(r) for r in self.results]}


def fetch_all(
    workspace: Workspace,
    registry: Registry,
    only: set[str] | None = None,
    today: date | None = None,
    workers: int = 6,
) -> FetchReport:
    workspace.ensure()
    ctx = FetchContext.create(workspace, today)
    store = CuratedStore(workspace.data_curated)
    report = FetchReport(run_date=ctx.today.isoformat())
    store_lock = threading.Lock()
    targets = [ind for ind in registry.collectable() if not only or ind.id in only]

    def _one(ind: Indicator) -> FetchResult:
        t0 = time.monotonic()
        existing = store.load(ind.id)
        since = None
        if existing is not None and existing.last_date is not None:
            since = existing.last_date - timedelta(days=45)
        try:
            provider = get_provider(ind.source.provider)
            series = provider.fetch(ind, ctx, since=since)
            with store_lock:
                final = store.save(series)
            log.info(
                "抓取成功 %s as_of=%s rows=%d %.1fs",
                ind.id,
                final.provenance.as_of,
                final.values.shape[0],
                time.monotonic() - t0,
            )
            return FetchResult(
                ind.id,
                "ok",
                as_of=final.provenance.as_of,
                rows=int(final.values.shape[0]),
                seconds=round(time.monotonic() - t0, 1),
            )
        except ProviderError as e:
            status = "skipped" if "跳过" in str(e) or "缺少" in str(e) else "failed"
            log.warning("抓取%s %s: %s", "跳过" if status == "skipped" else "失败", ind.id, e)
            return FetchResult(ind.id, status, message=str(e), seconds=round(time.monotonic() - t0, 1))
        except Exception as e:
            log.exception("抓取异常 %s", ind.id)
            return FetchResult(
                ind.id, "failed", message=f"{type(e).__name__}: {e}", seconds=round(time.monotonic() - t0, 1)
            )

    # 共享缓存的提供方（treasury、cftc、spdr、fedfunds）先串行预热一次，避免并行重复下载
    warm = {"treasury", "cftc", "spdr", "nyfed", "fedfunds"}
    first_of: dict[str, Indicator] = {}
    for ind in targets:
        first_of.setdefault(ind.source.provider, ind)
    serial = [ind for prov, ind in first_of.items() if prov in warm]
    order_ids = {ind.id for ind in serial}
    for ind in serial:
        report.results.append(_one(ind))
    rest = [ind for ind in targets if ind.id not in order_ids]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for res in pool.map(_one, rest):
            report.results.append(res)
    out = workspace.logs_dir / f"fetch_{report.run_date}.json"
    out.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return report
