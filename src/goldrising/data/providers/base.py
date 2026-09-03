from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Protocol

import requests

from goldrising.contracts import Indicator, IndicatorSeries
from goldrising.workspace import Workspace

USER_AGENT = "Mozilla/5.0 (compatible; GoldRisingDashboard/0.1)"
log = logging.getLogger(__name__)


class ProviderError(RuntimeError):
    """抓取或解析失败。调用方记录并继续，不得静默。"""


@dataclass
class FetchContext:
    workspace: Workspace
    session: requests.Session
    today: date
    env: dict[str, str]
    cache: dict[str, Any] = field(default_factory=dict)
    raw_dir: Path | None = None

    @classmethod
    def create(cls, workspace: Workspace, today: date | None = None) -> FetchContext:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})
        env = {k: v for k, v in os.environ.items() if k in {"FRED_API_KEY", "TUSHARE_TOKEN"}}
        return cls(
            workspace=workspace,
            session=session,
            today=today or datetime.now(UTC).date(),
            env=env,
            raw_dir=workspace.data_raw,
        )

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        timeout: int = 45,
        retries: int = 3,
        raw_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        last_err: Exception | None = None
        for attempt in range(retries):
            t0 = time.monotonic()
            try:
                resp = self.session.get(url, params=params, timeout=timeout, headers=headers)
                log.info("GET %s -> %s %.1fs %dB", url[:90], resp.status_code, time.monotonic() - t0, len(resp.content))
                if resp.status_code == 200:
                    if raw_name and self.raw_dir is not None:
                        self._save_raw(raw_name, resp.content)
                    return resp
                last_err = ProviderError(f"HTTP {resp.status_code} {url}")
                if resp.status_code in (400, 401, 403, 404):
                    break
            except requests.RequestException as e:  # 网络层错误重试
                log.warning("GET %s 失败 %.1fs: %s", url[:90], time.monotonic() - t0, e)
                last_err = e
            time.sleep(1.5 * (attempt + 1))
        raise ProviderError(f"抓取失败 {url}: {last_err}")

    def _save_raw(self, raw_name: str, content: bytes) -> None:
        assert self.raw_dir is not None
        sub = self.raw_dir / raw_name.split("/")[0]
        sub.mkdir(parents=True, exist_ok=True)
        stamp = self.today.isoformat()
        fname = raw_name.split("/", 1)[1] if "/" in raw_name else raw_name
        (sub / f"{stamp}_{fname}").write_bytes(content)


class Provider(Protocol):
    name: str

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries: ...
