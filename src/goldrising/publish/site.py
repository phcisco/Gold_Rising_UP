from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any

from goldrising.render.page import render_archive, render_page

log = logging.getLogger(__name__)


def archive_dates(site_dir: Path) -> list[str]:
    return sorted(p.stem for p in site_dir.glob("20??-??-??.html"))


def write_site(site_dir: Path, snapshot: dict[str, Any]) -> Path:
    site_dir.mkdir(parents=True, exist_ok=True)
    run_date = str(snapshot["run_date"])
    dates = archive_dates(site_dir)
    if run_date not in dates:
        dates.append(run_date)
    page = render_page(snapshot, archive_dates=sorted(dates))
    dated = site_dir / f"{run_date}.html"
    dated.write_text(page, encoding="utf-8")
    (site_dir / "index.html").write_text(page, encoding="utf-8")
    (site_dir / "archive.html").write_text(render_archive(sorted(dates)), encoding="utf-8")
    (site_dir / "archive.json").write_text(json.dumps(sorted(dates), ensure_ascii=False), encoding="utf-8")
    (site_dir / ".nojekyll").write_text("", encoding="utf-8")
    return dated


def git_publish(root: Path, run_date: str, push: bool | None = None) -> str:
    """提交生成的站点。默认在配置了远端时推送；GOLD_PUBLISH_PUSH=0 可关闭推送。无 git 仓库时跳过。"""
    if not (root / ".git").exists():
        return "skipped: 非 git 仓库"
    remote = os.environ.get("GOLD_GIT_REMOTE", "origin")
    branch = os.environ.get("GOLD_GIT_BRANCH", "main")

    def run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)

    has_remote = run("remote", "get-url", remote).returncode == 0
    env_push = os.environ.get("GOLD_PUBLISH_PUSH", "1") != "0"
    do_push = (env_push and has_remote) if push is None else push

    run("add", "site")
    status = run("status", "--porcelain")
    if not status.stdout.strip():
        return "nothing to commit"
    commit = run("commit", "-m", f"chore: 每日行情台 {run_date}")
    if commit.returncode != 0:
        return f"commit failed: {commit.stderr.strip()[:200]}"
    if not do_push:
        return "committed (push disabled)"
    pushed = run("push", remote, branch)
    if pushed.returncode != 0:
        return f"push failed: {pushed.stderr.strip()[:200]}"
    return "committed and pushed"
