"""数据提供方适配器。每个适配器只负责把一个官方来源变成带出处的 IndicatorSeries。"""

from __future__ import annotations

from goldrising.data.providers.base import FetchContext, Provider, ProviderError


def get_provider(name: str) -> Provider:
    # 函数级导入，避免注册表校验时加载全部网络依赖
    if name == "treasury":
        from goldrising.data.providers.treasury import TreasuryProvider

        return TreasuryProvider()
    if name == "nyfed":
        from goldrising.data.providers.nyfed import NYFedProvider

        return NYFedProvider()
    if name == "cboe":
        from goldrising.data.providers.cboe import CboeProvider

        return CboeProvider()
    if name == "fred":
        from goldrising.data.providers.fred import FredProvider

        return FredProvider()
    if name == "yahoo":
        from goldrising.data.providers.yahoo import YahooProvider

        return YahooProvider()
    if name == "yahoo_gc_contract":
        from goldrising.data.providers.yahoo import YahooGoldContractProvider

        return YahooGoldContractProvider()
    if name == "cftc":
        from goldrising.data.providers.cftc import CftcProvider

        return CftcProvider()
    if name == "spdr":
        from goldrising.data.providers.spdr import SpdrProvider

        return SpdrProvider()
    if name == "fedfunds":
        from goldrising.data.providers.fedfunds import FedFundsProvider

        return FedFundsProvider()
    if name == "manual":
        from goldrising.data.providers.manual import ManualProvider

        return ManualProvider()
    raise ProviderError(f"未实现的数据提供方: {name}")


__all__ = ["FetchContext", "Provider", "ProviderError", "get_provider"]
