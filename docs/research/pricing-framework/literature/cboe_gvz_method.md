# Cboe《Selected Broad-Based Index, Equity and ETF Volatility Indices Methodology》（含 GVZ）

- 机构：Cboe Global Indices
- 年份：现行版本（含 2025 年 6 月与 11 月重启的 VXSLV、VXGDX 说明）
- URL：https://cdn.cboe.com/api/global/us_indices/governance/Volatility_Index_Methodology_Selected_Broad_Based_Index_Equity_and_ETF_Volatility_Indices.pdf （从 https://www.cboe.com/us/indices/dashboard/gvz/ 进入）
- 访问日期：2026-09-03
- 是否全文：全文（24 页 PDF）

## 内容要点

1. GVZ（Cboe Gold ETF Volatility Index）用 VIX 相同方法，目标 30 天常数期限；成分是 **PM 结算、每月第三个周五到期的 GLD 期权**（不用周度期权）；剩余不足 7 天的系列剔除；报价源为 NBBO。
2. 同一文档定义 **VXGDX（Cboe Gold Miners ETF Volatility Index，GDX 期权）**，2025 年 11 月 3 日重启，历史按现行方法回算至 2022 年 2 月 14 日停编日；VXSLV（SLV）2025 年 6 月 16 日重启。VXTLT（20 年以上国债 ETF 波动率）、BITVX（IBIT 比特币 ETF 波动率）也在同一族。
3. 计算四步：选近月与次月；计算利率；计算两期方差（方差互换复制式，对全部虚值看涨看跌加权）；插值到 30 天并开方乘 100。系列级过滤算法与系数（alpha、gamma、lambda）在配套文档 Cboe Volatility Index Mathematics Methodology 中。
4. 用 ETF 期权而非期货期权：GVZ 度量的是 GLD 的隐含波动，含 ETF 折溢价与美股交易时段限制，不等于 COMEX 期货期权隐含波动。

## 对框架的含义

- **C3 与 C5 的度量**：GVZ 是免费日频的黄金隐含波动，但它只反映美股时段 GLD 期权，看不到亚洲时段。H9（GVZ/VIX 极值的信息含量）在设计时要注意 GVZ 每月第三个周五换月带来的期限结构跳变。
- **矿业股波动率（VXGDX）重启**是新的可观测量：GDX 隐含波动相对 GVZ 的比值可直接度量"矿业股对金价的贝塔放大"（H8），也是 GDXU 这类杠杆产品损耗的前瞻指标。骨架第 6 节未列入。
- 同族的 VXTLT 可作为 MOVE 的免费替代（MOVE 数据源为 ICE，非免费）。

## 对指标体系的含义

- `gvz`（已接入）；新增 `vxgdx`（Cboe CSV 端点应有 VXGDX_History.csv，待核）、`vxtlt`（替代 MOVE）、`gvz_vix_ratio`、`vxgdx_gvz_ratio`。日频、无滞后、免费。
- 期权持仓（骨架"待接入"）：CFTC 合并报告的 delta 折算未平仓可作弱代理；GLD 期权持仓量需 OCC 数据（免费但需接入）。

## 我的评价

方法文档本身没有惊喜，价值在两条：GVZ 的成分是月度 GLD 期权（不是期货期权），以及 VXGDX 已于 2025 年 11 月重启。后者对交易 GDX/GDXU 的用户是直接可用的新指标。
