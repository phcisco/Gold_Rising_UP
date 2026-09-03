"""工作区路径约定。仓库根目录可用环境变量 GOLD_ROOT 覆盖。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _default_root() -> Path:
    env = os.environ.get("GOLD_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Workspace:
    root: Path

    @classmethod
    def default(cls) -> Workspace:
        return cls(root=_default_root())

    @property
    def registry_path(self) -> Path:
        return self.root / "indicators" / "registry.yaml"

    @property
    def data_raw(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def data_curated(self) -> Path:
        return self.root / "data" / "curated"

    @property
    def data_manual(self) -> Path:
        return self.root / "data" / "manual"

    @property
    def narratives_dir(self) -> Path:
        return self.root / "narratives"

    @property
    def site_dir(self) -> Path:
        return self.root / "site"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    @property
    def snapshots_dir(self) -> Path:
        return self.root / "data" / "snapshots"

    def ensure(self) -> None:
        for p in (
            self.data_raw,
            self.data_curated,
            self.data_manual,
            self.narratives_dir,
            self.site_dir,
            self.logs_dir,
            self.snapshots_dir,
        ):
            p.mkdir(parents=True, exist_ok=True)
