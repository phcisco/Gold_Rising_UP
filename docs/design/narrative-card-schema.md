# 叙事卡 YAML 规范（v1）

每条叙事一个文件：`narratives/<id>.yaml`。键名英文，值可用中文。程序按本规范校验。

```yaml
id: fed_independence                 # snake_case 英文，文件名同名
name: 美联储独立性受损                 # 中文名
status: active                       # active | archived
lifecycle_state: 边际                 # 新兴 | 边际 | 主导 | 共识 | 退潮 | 已证伪 | 归档
lifecycle_since: 2026-09-03          # 该状态起始日
lifecycle_rationale: 一段话，引用具体证据说明为何处于该状态
pricing_degree: 未定价                # 未定价 | 部分 | 充分 | 已出清
pricing_rationale: 一段话，引用持仓、资金流、赔率、卖方观点等说明市场已为此叙事下了多少注
direction: bull                      # bull | bear | mixed  （对金价方向）
horizon: 3-12m                       # weeks | 3-12m | years
thesis: 一句话命题
logic_chain:                         # 因果链，每步一行
  - 白宫施压联储人事与利率决策
  - 市场怀疑联储抗通胀可信度
  - 通胀风险溢价与期限溢价上升
  - 黄金作为无主权信用风险资产获得溢价
regime_dependency:                   # 8/31 报告的核心教训：同一叙事在不同体制下方向可能反转
  passive_fed: bull                  # 体制 A（联储被动、财政主导）下对金价方向
  credible_fed: bear                 # 体制 B（联储主动且可信）下对金价方向
  note: 说明为何反转或不反转
evidence_indicators:                 # 证据指标，引用 indicators/registry.yaml 的 id；不存在的放 proposed_indicators
  - indicator_id: t10yie
    expected_sign: up                # up | down | flat
    weight: high                     # high | medium | low
    rationale: 为什么该指标为此叙事作证
pricing_proxies:                     # 定价程度的观察代理
  - indicator_id: cot_mm_net_pctl
    note: 拥挤度
  - name: polymarket_fed_chair_odds  # 无 registry id 的用 name
    url: https://...
    note: 事件赔率
verification_signals:                # 3 到 5 条，能量化就量化
  - id: v1
    description: 新主席首次 FOMC 声明偏鸽，而 10Y 盈亏平衡同步上行
    type: qual                       # quant | qual
    next_check: 2026-09-16           # 下一个观察时点
  - id: v2
    description: 10Y 盈亏平衡通胀 20 日内上行超过 15bp
    type: quant
    rule: {indicator_id: t10yie, op: change_gt, value: 0.15, window_days: 20}
    next_check: 2026-09-30
falsification_conditions:            # 至少一条；量化的写 rule；只追加不覆盖，改动需新版本
  - id: f1
    version: 1
    created: 2026-09-03
    description: 到 2026-11-30，10Y 盈亏平衡仍低于 2.3% 且 2s30s 低于 80bp
    type: quant
    rule:
      all_of:
        - {indicator_id: t10yie, op: lt, value: 2.3}
        - {indicator_id: curve_2s30s, op: lt, value: 0.80}
    deadline: 2026-11-30
  - id: f2
    version: 1
    created: 2026-09-03
    description: 联储在压力下仍按数据路径行事且市场通胀预期锚定（定性，AI 判定）
    type: qual
    deadline: 2026-12-31
tensions:                            # 与之逻辑冲突的叙事
  - narrative_id: credible_fed_regime
    note: 两者不能同时成立
news_queries:                        # 3 到 5 个，AI 每日据此检索
  - Fed independence Warsh
  - Treasury Fed coordination rates
counterargument: 当前对该叙事最强的反方论证，一段话
sources:                             # 建卡依据，一手来源优先
  - title: FOMC Statement, July 2026
    url: https://www.federalreserve.gov/...
    publisher: Federal Reserve
    accessed: 2026-09-03
    type: primary                    # primary | secondary
history: []                          # 程序维护，只追加
```

## 可引用的指标 id（种子集）

| id | 含义 | 官方来源 |
|---|---|---|
| gold_nav_implied | GLD 官方 NAV 隐含金价（≈ LBMA 下午定盘，美元/盎司） | SPDR 官方档案 |
| gc_c1, gc_c2 | COMEX 黄金活跃合约与次活跃合约 | CME 经 Yahoo |
| gc_front | COMEX 黄金近月连续（长历史参考） | CME，经 Yahoo |
| xau_eur, xau_jpy, xau_cny | 多币种计价金价 | 派生 |
| dfii10 | 10Y TIPS 实际收益率 | FRED DFII10 |
| t10yie | 10Y 盈亏平衡通胀 | FRED T10YIE |
| dgs2, dgs10, dgs30 | 名义国债收益率 | FRED |
| curve_2s10s, curve_2s30s | 曲线斜率（百分点） | 派生 |
| effr | 有效联邦基金利率 | FRED EFFR |
| ff_next_change_bp, ff_cum_change_bp | 联邦基金期货复算的下次 FOMC 隐含变动（bp）与未来 12 个月累计隐含变动（bp） | CME ZQ 合约经 Yahoo |
| dxy | 美元指数 | ICE 经 Yahoo |
| usdcny, usdjpy, eurusd | 汇率（人民币为在岸 CNY=X） | Yahoo |
| vix | VIX | FRED VIXCLS |
| move | MOVE 指数 | Yahoo ^MOVE |
| hy_oas | 高收益债利差 | FRED BAMLH0A0HYM2 |
| gold_copper_ratio, gold_oil_ratio | 比价 | 派生 |
| btc, spx, brent, wti, copper, silver | 比特币、标普 500、布伦特、WTI、铜、白银 | Yahoo |
| cot_mm_net, cot_mm_net_pctl, cot_oi | CFTC 管理基金黄金净多头、其 5 年分位、总持仓 | CFTC 公开报告 API |
| gld_tonnes | GLD 信托持仓吨数 | SPDR |
| gc_term_spread | COMEX 活跃与次活跃合约价差 | Yahoo 合约 |
| sge_au9999, shfe_au, shanghai_premium | 上金所现货、上期所期货、沪金溢价 | 上金所/上期所经 Tushare 或 AKShare |
| cb_purchases | 央行净购金（月） | WGC/IMF |
| gold_silver_ratio | 金银比 | 派生 |
| gvz, gvz_vix_ratio | 黄金隐含波动率及其对 VIX 之比 | FRED GVZCLS |
| ma200_dist, mom_20, mom_60 | 技术状态 | 派生 |
| platinum, palladium | 铂、钯 | Yahoo |
| gdx, gdxj, gdxu, gdx_gld_ratio, gdx_beta_60, gdxu_decay | 矿业股组 | Yahoo，派生 |
| aisc_margin | 矿商 AISC 利润率（季） | WGC / 矿商季报 |

不在表中的指标写入卡片的 `proposed_indicators`：

```yaml
proposed_indicators:
  - id: term_premium_10y
    name: 10 年期期限溢价（ACM 模型）
    source: Federal Reserve Bank of New York
    url: https://www.newyorkfed.org/research/data_indicators/term-premia-tabs
    frequency: daily
    lag: 1 个交易日
    tier: 2
    rationale: 为财政贬值叙事作证
```
