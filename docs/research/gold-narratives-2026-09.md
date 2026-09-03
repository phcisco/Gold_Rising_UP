# 黄金叙事库 · 第 0 阶段调研总报告（2026-09）

- 生成日期：2026-09-03。数据截止日逐项标注。
- 方法：三个 AI 研究员按簇并行调研（一 货币利率财政、二 结构性需求供给、三 跨资产与风险），全部数字取自官方或一手来源并标注截止日；新闻只用于定位事件。抓取走 curl，禁用 WebFetch 与 WebSearch（本环境会挂起）。分簇原稿见 `docs/research/drafts/`，抓取约定见 `docs/research/RESEARCH_TOOLING.md`。
- 产出：正式叙事库 `narratives/*.yaml`（20 张卡，校验零错误）与库级元数据 `narratives/_library.yaml`；本报告；指标规格（第 6 节）已落地为注册表新增 28 个指标。
- 本报告同时承担《黄金的新定价锚》标注的 09-04 更新节点。与旧报告的差异见第 8 节。

## 1. 一句话结论

当前处于**体制 B：联储主动且可信**（起点 2026-06-17）。在这一体制下，10Y 实际收益率重新成为金价主锚，降息交易已反转为加息定价并被充分消化，能源冲击与地缘升级通过油价和加息路径利空黄金而非利多。金价的地板来自央行购金（共识、已充分定价）与刚刚回归的欧洲 ETF；东方实物批发与北美 ETF 两大历史边际买家缺席。所有多头叙事（财政主导、曲线控制、联储独立性、通胀风险溢价）都以“体制切换到 A”为前提，目前处于边际、新兴或退潮状态，且大多未被定价。最值钱的观察点是体制开关本身：8 月金价逆宏观反弹使金价与实际利率的 60 日相关回到零，与体制 B 的签名不符，属待确认状态。

## 2. 体制判断

| 项目 | 内容 |
|---|---|
| 当前体制 | B，联储主动且可信 |
| 起点 | 2026-06-17（FOMC 声明“will deliver price stability”，12-0） |
| 一手证据 | 7/29 声明 9-3，三票主张加息；贴现率纪要四家储备银行申请上调至 4%；7 月纪要把名义收益率上行归因于实际利率、称长期通胀补偿稳定；ACM 分解 1/2 至 9/1 风险中性利率 +60bp、期限溢价 −1bp；Warsh 8/28 讲话称 2% 为 firm, fixed target |
| 量化签名 | 2/27 至 7/31：10Y 名义 +78bp 中实际 +75bp、盈亏平衡 +3bp，2s30s 由 126bp 平至 99bp；同期金价约 −25% |
| 切换到 A 的三个条件 | 联储在 PCE 高于 3% 时降息或停止紧缩并删去“deliver price stability”；盈亏平衡与期限溢价同时上行；实际利率与金价脱钩 |
| 当前读数 | 10Y 实际 2.45（2026-09-02，10 年分位 100）；10Y 盈亏平衡 2.34（2026-09-02，10 年分位 75）；ACM 期限溢价 0.78（2026-09-01，10 年分位 99）；2s30s 0.88（2026-09-02，10 年分位 53）；金价与实际利率 60 日相关 0.03（2026-09-02，10 年分位 75） |
| 待确认 | 60 日相关接近零来自 8 月金价 +10.9% 的逆宏观反弹；若 9/16 FOMC 加息而金价不跌、或相关系数持续为正，体制判断需重估 |

## 3. 叙事地图（20 张卡）

活跃上限 12 的解释：活跃指生命周期为新兴、边际、主导、共识的卡，进入 L3 地图主视图。退潮卡仍每日核对验证与证伪条件，折叠显示。已证伪与归档卡保留重新激活条件。三簇合并后活跃恰为 12 张，未做人为删减。

### 3.1 活跃（12）
| id | 名称 | 簇 | 生命周期（起点） | 定价程度 | 方向 | 体制 A / B | 量化证伪/总数 | 尺度 |
|---|---|---|---|---|---|---|---|---|
| energy_stagflation | 能源供给冲击下的滞胀 | 三 跨资产与风险 | 主导（2026-03-02） | 部分 | mixed | bull / bear | 1/2 | 3-12m |
| geopolitical_war_premium | 地缘政治与战争溢价：用可观察指标而非新闻情绪跟踪 | 三 跨资产与风险 | 主导（2026-03-02） | 充分 | mixed | bull / bear | 0/2 | 3-12m |
| market_internals_gvz | 市场内部结构：GVZ/VIX 极值、金银比、铂钯与矿业股相对强弱 | 三 跨资产与风险 | 主导（2026-08-20） | 部分 | mixed | bull / bear | 2/2 | weeks |
| mine_supply_cost_margin | 矿业供给、成本与矿商利润率 | 二 结构性需求供给 | 主导（2026-04-01） | 部分 | mixed | bull / bear | 2/3 | 3-12m |
| real_rate_anchor_regime_switch | 实际利率旧锚回归与体制 A/B 切换 | 一 货币利率财政 | 主导（2026-08-28） | 部分 | bear | bull / bear | 2/3 | 3-12m |
| cb_reserve_reallocation | 央行储备再配置与去美元化 | 二 结构性需求供给 | 共识（2026-06-16） | 充分 | bull | bull / bull | 2/3 | years |
| fed_hawkish_repricing | 降息交易已出清并反转为加息周期定价 | 一 货币利率财政 | 共识（2026-07-29） | 充分 | bear | bull / bear | 1/2 | weeks |
| dollar_cycle | 美元周期：金价上涨是美元走弱的伴随，还是黄金的独立定价 | 三 跨资产与风险 | 边际（2026-01-27） | 部分 | mixed | bull / bear | 1/2 | 3-12m |
| fiscal_dominance_term_premium | 财政贬值与财政主导（赤字、利息支出、拍卖需求、期限溢价） | 一 货币利率财政 | 边际（2026-06-17） | 部分 | bull | bull / bear | 1/3 | years |
| etf_western_investor_return | ETF 资金流与西方投资者回归 | 二 结构性需求供给 | 新兴（2026-07-17） | 部分 | bull | bull / bear | 2/3 | 3-12m |
| imf_gold_reserve_caution | IMF 对黄金储备资产的警示（看空） | 二 结构性需求供给 | 新兴（2026-07-31） | 未定价 | bear | bear / bear | 1/2 | years |
| ycc_financial_repression | 收益率曲线控制 / 金融抑制 / 期限溢价压制 | 一 货币利率财政 | 新兴（2026-07-09） | 未定价 | bull | bull / bear | 1/2 | years |

### 3.2 退潮监控（5）
| id | 名称 | 簇 | 生命周期（起点） | 定价程度 | 方向 | 体制 A / B | 量化证伪/总数 | 尺度 |
|---|---|---|---|---|---|---|---|---|
| asia_physical_demand | 亚洲实物需求与定价权东移 | 二 结构性需求供给 | 退潮（2026-06-30） | 部分 | bull | bull / mixed | 2/2 | 3-12m |
| fed_independence_erosion | 美联储独立性受损（人事、政策协调、可信度定价） | 一 货币利率财政 | 退潮（2026-06-17） | 已出清 | bull | bull / bear | 1/2 | 3-12m |
| inflation_risk_premium_repricing | 通胀风险溢价重定价（盈亏平衡通胀、TIPS） | 一 货币利率财政 | 退潮（2026-06-17） | 已出清 | bull | bull / bear | 1/2 | 3-12m |
| physical_market_stress | 实物市场紧张（金库、EFP、租赁利率） | 二 结构性需求供给 | 退潮（2026-03-31） | 已出清 | bull | bull / bull | 1/1 | weeks |
| risk_on_bear_case | 看空叙事：风险偏好回升、信用利差收窄与 AI 生产率红利压制黄金 | 三 跨资产与风险 | 退潮（2026-08-03） | 部分 | bear | mixed / bear | 2/3 | 3-12m |

### 3.3 已证伪与归档（3）
| id | 名称 | 簇 | 生命周期（起点） | 定价程度 | 方向 | 体制 A / B | 量化证伪/总数 | 尺度 |
|---|---|---|---|---|---|---|---|---|
| basel_iii_tier1_gold | 巴塞尔 III 把黄金列为一级资产 | 三 跨资产与风险 | 已证伪（2026-09-03） | 已出清 | bull | mixed / mixed | 0/1 | years |
| digital_gold_substitution | 数字黄金替代：比特币分流黄金的边际买盘 | 三 跨资产与风险 | 已证伪（2026-09-03） | 已出清 | bear | mixed / mixed | 1/1 | years |
| tariff_inflation | 关税通胀：关税推升美国通胀并抬高黄金的通胀对冲需求 | 三 跨资产与风险 | 归档（2026-09-03） | 已出清 | mixed | bull / bear | 0/1 | 3-12m |

体制依赖一列读法：A 为联储被动或财政主导时该叙事对金价的方向，B 为联储主动可信时的方向。除央行购金、IMF 警示、实物紧张三张卡外，其余全部在两种体制下反向，这正是 8/31 更新的核心教训：同一组数据在不同体制下定价方向相反，先判体制再读叙事。

## 4. 张力

| 叙事 A | 叙事 B | 跨簇 | 冲突点 |
|---|---|---|---|
| asia_physical_demand | etf_western_investor_return |  | 两者争夺“边际买家”身份；东方贴水 + 西方流入意味着定价权暂时回到西方 |
| asia_physical_demand | cb_reserve_reallocation |  | 同向但不同主体：人民银行购金强化国内投资信心，但不能替代批发需求 |
| basel_iii_tier1_gold | risk_on_bear_case |  | 无直接冲突；列出以提示该叙事不应被用作反驳看空叙事的“结构性需求”证据 |
| cb_reserve_reallocation | imf_gold_reserve_caution |  | IMF 主张黄金是高风险储备资产、国内购金计划应避免，与央行调查中 50% 受访者以本币国内购金直接冲突 |
| cb_reserve_reallocation | etf_western_investor_return |  | 不冲突但存在替代关系：若西方 ETF 回归成为边际买家，央行地板的重要性下降；反之央行是唯一买家时价格上行缺乏弹性 |
| digital_gold_substitution | dollar_cycle |  | 两者同为美元信用重定价的载体，替代叙事与之逻辑冲突 |
| dollar_cycle | energy_stagflation |  | 油价冲击在体制 B 下同时推高美元与实际利率，压制黄金；两者共振时美元叙事为空 |
| dollar_cycle | risk_on_bear_case |  | 风险偏好回升通常伴随美元走弱，却也伴随黄金资金流出，方向相互抵消 |
| energy_stagflation | risk_on_bear_case |  | 增长强劲与信用宽松否定“滞”，但同一组数据支持联储继续加息 |
| energy_stagflation | geopolitical_war_premium |  | 同一事件的两个侧面；在体制 B 下战争升级通过油价与加息路径反而利空黄金 |
| energy_stagflation | real_rate_anchor_regime_switch | 跨簇 | 簇一叙事（id 待对齐）；联储可信则本叙事对金价方向为空 |
| etf_western_investor_return | imf_gold_reserve_caution |  | IMF 关于黄金流动性与波动性的论证若被西方机构采纳，会抑制配置型资金回流 |
| etf_western_investor_return | real_rate_anchor_regime_switch | 跨簇 | WGC 指出北美 ETF 与 10Y TIPS 的负相关已恢复，实际利率 2.5% 是西方配置资金的机会成本阈值；实际利率锚成立则西方回归受压 |
| fed_hawkish_repricing | fed_independence_erosion |  | 若白宫施压导致联储不兑现加息，本叙事的"加息共识"将崩塌 |
| fed_hawkish_repricing | inflation_risk_premium_repricing |  | 加息兑现压低通胀风险溢价；不兑现则抬高 |
| fed_independence_erosion | real_rate_anchor_regime_switch |  | 独立性完好是体制 B 的前提；本叙事升温即体制 A 回归 |
| fiscal_dominance_term_premium | real_rate_anchor_regime_switch |  | 体制 B 下财政担忧以更高实际利率表达，压制金价，与本叙事方向相反 |
| fiscal_dominance_term_premium | fed_hawkish_repricing |  | 加息定价兑现意味着联储未为财政让路 |
| geopolitical_war_premium | risk_on_bear_case |  | 冲突升级会打断风险偏好，但在体制 B 下通过加息路径反而强化看空叙事的机会成本腿 |
| inflation_risk_premium_repricing | real_rate_anchor_regime_switch |  | 体制 B 下盈亏平衡稳定是主锚有效的前提 |
| market_internals_gvz | risk_on_bear_case |  | 矿业股领涨依赖股市风险偏好；若风险偏好逆转，GDX 贝塔将放大黄金下行 |
| market_internals_gvz | dollar_cycle |  | 黄金自身定价与美元无关的判断在两卡中一致，无冲突，列出以便交叉验证 |
| market_internals_gvz | asia_physical_demand | 跨簇 | GVZ 极值与亚洲价格发现权重上升、1 月期权活动升温相关；上海溢价应与本卡交叉核对 |
| mine_supply_cost_margin | etf_western_investor_return |  | 不冲突；矿业股是西方风险偏好回归时的首选杠杆，但西方缺席时矿业股常跑输实物 |
| mine_supply_cost_margin | cb_reserve_reallocation |  | 无直接冲突；央行只买实物不买矿业股，央行地板不为矿业股提供支撑 |
| physical_market_stress | asia_physical_demand |  | 同源：亚洲实物需求恢复是实物紧张的最可能触发器；东方贴水则两卡同时无信号 |
| physical_market_stress | cb_reserve_reallocation |  | 央行集中提取实物（如自英格兰银行回运本土，2026 调查中 9% 已增加本土存储）可触发伦敦金库下降 |
| real_rate_anchor_regime_switch | ycc_financial_repression |  | 曲线控制意味着实际利率被人为压低，旧锚失效 |
| risk_on_bear_case | fiscal_dominance_term_premium | 跨簇 | 簇一叙事（id 待对齐）：赤字扩大直接否定财政修复腿 |
| tariff_inflation | energy_stagflation |  | 同一“供给侧通胀”框架，但 2026 年的通胀全部来自能源；把关税与能源混为一谈会误判联储反应 |
| ycc_financial_repression | fed_hawkish_repricing |  | 一边加息一边压长端在逻辑上可以并存（扭曲操作），但与 Warsh 原则五冲突 |

跨簇张力的共同开关是体制判定：若切换到 A，簇三的能源滞胀、地缘溢价、美元周期、市场内部结构四卡同时翻多，看空叙事失去机会成本腿；簇二的西方 ETF 回归不再受实际利率压制；簇一的四张多头卡从边际或退潮转为主导。

## 5. 最重要的发现（跨簇）

1. **“新定价锚”命题被否定为当前主导叙事**，重构为体制切换卡。8/28 当日名义收益率上行由实际利率贡献、盈亏平衡下行、金价 −2.9%、曲线走平；1/29 以来 10Y 实际 +56bp 对金价 −16%，方向严格相反。
2. **降息交易不只是出清，而是反转为加息定价**：联邦基金期货 9 月合约隐含 3.70% 对 EFFR 3.63%，9 月加息概率约 60%，2027 年 9 月合约 4.24% 约 2.4 次加息；Polymarket 9 月加息 51.5%、年内零降息 89%。市场路径比 6 月 SEP 中位数更鹰，风险偏向“联储不如市场鹰”，即鹰派冲击对金价的边际利空基本释放。
3. **央行购金是共识且已充分定价**：Q2 净购 289 吨为二季度纪录，但发生在季均价 −8% 的季度，购金托底而不推价；Q1 初值 244 吨下修至 57 吨（−77%）未引发价格反应。放缓的伤害大于持续的推升。
4. **人民银行购金逐月加速**（外汇局：1 月 1.2 吨到 7 月 19.9 吨，7 月为 2023 年 10 月以来最大），是簇二最强的新证据。
5. **IMF Note 2026/007 把黄金定性为高风险储备资产并劝阻国内购金计划**，与 WGC 调查中 50% 央行的购金方式直接对立，市场完全未定价；是库中唯一新兴的结构性看空叙事。
6. **边际买家格局**：央行地板加欧洲 ETF 试探性回流加投机盘回补支撑价格；上金所 8 月出库 62 吨环比 −22%、上海贴水约 −0.6% 至 −1.0%、印度折价 45 美元、北美 ETF 7 月仅 +0.7 亿美元。定价权在数周尺度上暂回西方，但西方持仓型资金未确认。
7. **体制 B 下“和平利多黄金、升级利空”**：3 至 7 月 Brent +70%、实际利率 +75bp、黄金 −25%。战争溢价目前在油不在金。
8. **看空叙事两条腿被官方数据否定**：FY2026 前十个月赤字 1.799 万亿美元已超 FY2025 全年 1.775 万亿；非农生产率 Q1 0.8%、Q2 1.4%。真正起作用的只有实际利率与风险偏好。
9. **GVZ/VIX 比处于 10 年 98.6 分位**：比值高于 2.0 只出现在 2013 年崩盘与 2026 年 1 月顶部；七次上穿 1.5 后 60 日收益 −17% 至 +10%，无一致方向。这是黄金自身波动率体制与杠杆风险的信号，不是方向信号，GDXU 风险最大。
10. **三条旧叙事已证伪或归档**：数字黄金替代（两年内 60 日相关从未低于 −0.3，比值由 35.5 降至 17.4）、巴塞尔 III 一级资产（BIS 原文无此分类，NSFR 对黄金反而是 85% RSF 的不利待遇）、关税通胀（核心商品 CPI 峰值仅 1.41%，2026 年 7 月 0.78%，通胀全部来自能源）。

## 6. 指标规格

### 6.1 指标到叙事的映射（由叙事卡自动生成，不在注册表重复维护）

映射覆盖 34 个指标，其中 33 个已在注册表、1 个为卡内 proposed_indicators 待接入。已接入但未被任何活跃叙事引用的一级或二级指标：gold_nav_implied, usdjpy, dgs10, move, gold_copper_ratio, gc_c1, shfe_au, mom_20, mom_60, be_5y, be_30y, term_premium_10y, acm_rny10, gold_real_yield_corr_60d, cpi_headline_yoy, cpi_core_yoy, pce_core_yoy, gold_dxy_corr_60d, ovx, gvz_realized_spread。这些属于基线指标或标的监控，按设计保留。

| 指标 | 级别 | 接入状态 | 引用数 | 为哪些叙事作证（方向，权重） |
|---|---|---|---|---|
| aisc_margin | target | 待接入（注册表占位） | 1 | mine_supply_cost_margin(↑,h) |
| cb_purchases | 1 | 待接入（注册表占位） | 2 | cb_reserve_reallocation(↑,h)；imf_gold_reserve_caution(↓,h) |
| cot_mm_net | 2 | 已接入 | 1 | etf_western_investor_return(↑,m) |
| cot_mm_net_pctl | 1 | 已接入 | 2 | market_internals_gvz(↑,m)；risk_on_bear_case(↓,m) |
| curve_2s10s | 2 | 已接入 | 1 | fed_hawkish_repricing(↓,m) |
| curve_2s30s | 1 | 已接入 | 5 | energy_stagflation(↑,m)；fed_independence_erosion(↑,m)；fiscal_dominance_term_premium(↑,h)；real_rate_anchor_regime_switch(↓,m)；ycc_financial_repression(↓,l) |
| dfii10 | 1 | 已接入 | 10 | energy_stagflation(↓,h)；etf_western_investor_return(↓,h)；fed_independence_erosion(↓,m)；fiscal_dominance_term_premium(↓,m)；geopolitical_war_premium(↓,h)；imf_gold_reserve_caution(↑,m)；inflation_risk_premium_repricing(↓,h)；real_rate_anchor_regime_switch(↑,h)；risk_on_bear_case(↑,h)；ycc_financial_repression(↓,h) |
| dgs2 | 1 | 已接入 | 1 | fed_hawkish_repricing(↑,h) |
| dgs30 | 1 | 已接入 | 2 | fiscal_dominance_term_premium(↑,m)；ycc_financial_repression(↓,m) |
| dxy | 1 | 已接入 | 8 | cb_reserve_reallocation(↓,m)；dollar_cycle(↓,h)；energy_stagflation(↓,l)；etf_western_investor_return(↓,m)；fed_hawkish_repricing(↑,l)；fed_independence_erosion(↓,m)；fiscal_dominance_term_premium(↓,m)；ycc_financial_repression(↓,m) |
| effr | 1 | 已接入 | 1 | fed_hawkish_repricing(↑,m) |
| eurusd | 2 | 已接入 | 1 | dollar_cycle(↑,l) |
| ff_cum_change_bp | 1 | 已接入 | 2 | fed_hawkish_repricing(↑,h)；real_rate_anchor_regime_switch(↑,m) |
| ff_next_change_bp | 1 | 已接入 | 1 | fed_hawkish_repricing(↑,h) |
| gc_front | 3 | 已接入 | 3 | geopolitical_war_premium(↑,m)；inflation_risk_premium_repricing(↑,m)；real_rate_anchor_regime_switch(↓,h) |
| gc_term_spread | 2 | 已接入 | 1 | physical_market_stress(↓,m) |
| gdx_beta_60 | target | 已接入 | 1 | mine_supply_cost_margin(↑,m) |
| gdx_gld_ratio | target | 已接入 | 2 | market_internals_gvz(↑,m)；mine_supply_cost_margin(↑,h) |
| gld_tonnes | 1 | 已接入 | 3 | etf_western_investor_return(↑,h)；physical_market_stress(↓,l)；risk_on_bear_case(↓,h) |
| gold_oil_ratio | 2 | 已接入 | 4 | energy_stagflation(→,m)；geopolitical_war_premium(↑,h)；inflation_risk_premium_repricing(↓,l)；mine_supply_cost_margin(↑,m) |
| gold_silver_ratio | 2 | 已接入 | 1 | market_internals_gvz(↑,m) |
| gvz | 1 | 已接入 | 1 | market_internals_gvz(↑,m) |
| gvz_vix_ratio | 1 | 已接入 | 1 | market_internals_gvz(↑,h) |
| hy_oas | 2 | 已接入 | 1 | risk_on_bear_case(↓,m) |
| ma200_dist | 1 | 已接入 | 1 | risk_on_bear_case(↓,l) |
| platinum | 3 | 已接入 | 1 | market_internals_gvz(→,l) |
| sge_au9999 | 2 | 待接入（注册表占位） | 1 | asia_physical_demand(↑,m) |
| shanghai_premium | — | 待接入（卡内 proposed） | 2 | asia_physical_demand(↑,h)；physical_market_stress(↑,h) |
| t10yie | 1 | 已接入 | 7 | energy_stagflation(↑,h)；fed_independence_erosion(↑,h)；fiscal_dominance_term_premium(↑,m)；geopolitical_war_premium(↑,m)；inflation_risk_premium_repricing(↑,h)；real_rate_anchor_regime_switch(→,h)；ycc_financial_repression(↑,h) |
| usdcny | 2 | 已接入 | 3 | asia_physical_demand(↓,m)；cb_reserve_reallocation(→,l)；dollar_cycle(↓,m) |
| vix | 1 | 已接入 | 2 | geopolitical_war_premium(↑,l)；risk_on_bear_case(↓,m) |
| xau_cny | 2 | 已接入 | 2 | asia_physical_demand(↑,l)；dollar_cycle(↑,h) |
| xau_eur | 2 | 已接入 | 1 | dollar_cycle(↑,h) |
| xau_jpy | 2 | 已接入 | 1 | dollar_cycle(↑,m) |

### 6.2 本轮已接入注册表的新指标（28 个）

dgs5、dfii30、be_5y、be_30y、term_premium_10y、acm_rny10、gold_real_yield_corr_60d、cpi_index、cpi_core_index、cpi_energy_index、pce_core_index、cpi_headline_yoy、cpi_core_yoy、cpi_energy_yoy、pce_core_yoy、fed_ust_bills、fed_ust_coupons、usd_broad、gold_dxy_corr_60d、ovx、hyg、lqd、hyg_lqd_ratio、btc_gold_ratio、gold_btc_corr_60d、vxslv、gold_rvol_20、gvz_realized_spread、gold_platinum_ratio。全部已抓取成功并出现在快照中。

### 6.3 待接入指标与官方可得性结论（第 2 阶段）

| 数据 | 官方来源 | 可得性 | 处理 |
|---|---|---|---|
| 人民银行黄金储备（月） | 外汇局《官方储备资产》xlsx | 可得，页面链接每年一换 | 接入，建议一级低频 |
| 全球央行购金（季、月） | WGC GDT 页面文本、月度博文；IMF SDMX API | 文本可得；WGC xlsx 需免费注册；IMF 数据 API 可访问但序列待定位 | 接入文本解析，保存每期初值与修正值 |
| 上金所出库量（月）、Au99.99 日收盘、1 年租借费率（周） | 上金所月报 PDF、日行情页、周度 PDF | 可得 | 接入；租借费率是租赁利率的唯一免费代理 |
| 沪金溢价（日） | 派生：上金所收盘对 GLD NAV 反推的 LBMA 定盘或 GC 主力 | 可算，两法相差约 0.4 个百分点且有 7.5 小时时点差 | 接入并固定口径、标注误差 |
| 伦敦金库黄金存量（月） | LBMA xlsx | 可得 | 接入 |
| 全球 ETF 持仓与分地区流量（月） | WGC 月评页面文本 | 文本可得 | 接入 |
| 矿商实现价与 AISC（季） | SEC EDGAR 8-K 与 6-K 附件 | 可得 | 接入 |
| ACM 期限溢价、财政数据（赤字、利息、短债占比、拍卖） | 纽约联储、财政部 Fiscal Data API | 可得（ACM 已接入） | 财政数据第 2 阶段接入 |
| 地缘风险指数 GPR | Caldara 与 Iacoviello 日频 xls | 可得 | 接入 |
| Polymarket 事件赔率（加息、人事、霍尔木兹） | Gamma API | 可得，需设最低成交阈值 | 接入 |
| COMEX 库存 | CME | **不可得**：本机 IP 被 CME 封禁，FTP 无金属 | 页面注明“未监控” |
| EFP、伦敦租赁利率 | 无官方免费序列 | **不可得** | 用期限结构价差与上金所租借费率代理 |
| CME FedWatch | 无公开接口 | 不需要：已由联邦基金期货复算（ff_next_change_bp、ff_cum_change_bp） | 已接入 |

## 7. 接下来的观察点

| 日期 | 事件 | 关联叙事 | 看什么 |
|---|---|---|---|
| 09-04 | CFTC 持仓（9/1 数据，Warsh 讲话后首份） | real_rate_anchor、market_internals_gvz | 管理基金净多是否从 5 年 79 分位开始出清 |
| 09-07 | 外汇局 8 月黄金储备 | cb_reserve_reallocation | 增量是否不低于 40 万盎司，加速是否延续 |
| 09-08 | WGC 8 月 ETF 流向 | etf_western_investor_return | 北美是否转为净流入 |
| 09-10 至 09-11 | 8 月 CPI | fed_hawkish、inflation_risk_premium、energy_stagflation | 核心环比是否不低于 0.3% |
| 09-16 | FOMC | 全部簇一叙事 | 是否加息、异议方向、声明是否保留“deliver price stability”、金价当日是否与实际利率反向 |
| 10-30 | WGC GDT Q3 | cb_reserve、mine_supply、imf_caution | 央行净购是否不低于 200 吨，总供给同比 |
| 11-04 | 财政部再融资声明 | fiscal_dominance、ycc | 附息规模与短债占比 |
| 12-09 | FOMC 与任务组进展 | ycc、fed_independence | 资产负债表构成、会议频率、前瞻指引形式 |

## 8. 与旧报告的差异

| 项目 | 《黄金的新定价锚》（8/24，8/31 更新） | 本报告 |
|---|---|---|
| 主导叙事 | 初版“主权信用溢价与曲线陡峭度成为新锚”，更新改为两体制 | 实际利率旧锚回归与体制 A/B 切换，体制 B 自 6/17 |
| 叙事数量 | 6 条在线、6 条上升、5 条已证伪 | 12 活跃、5 退潮、3 归档，每条含体制依赖、量化证伪条件与截止日 |
| 降息交易 | 退潮、已出清 | 反转为加息定价，共识且充分定价，风险偏向联储不如市场鹰 |
| 央行购金 | 共识、已充分、四处裂缝 | 共识、充分；新增人民银行逐月加速与 IMF 看空对立 |
| 数据方法 | 网页搜索为主，行情含新闻转述 | 全部官方一手来源，逐项截止日；FedWatch 改为期货复算 |
| 已证伪叙事 | 五条，含实物挤兑与 COMEX 违约 | 三条归档并写重新激活条件；实物紧张降为退潮监控卡 |

## 9. 已知口径问题与待办

- 黄金历史高点口径不一：GC 主力收盘 5,318（1/29）、LBMA 定盘 5,405（1/29）、盘中曾超 5,500。注册表以 gold_nav_implied 与 gc_c1 各算回撤，页面标注口径。
- SPDR 档案在英国假日沿用前一日 NAV，反推定盘价时需按 LBMA 日历剔除。
- WGC 央行季度初值修正幅度大（Q1 2026 −77%），以 cb_purchases 为条件的量化证伪应在下一季修正后判定；程序保存每期初值与修正值。
- 核心 PCE 3.3% 与核心 CPI 2.48% 相差 0.8 个百分点，远超常态，AI 日评需结合 BEA 分项解释。
- 最高法院关税判决全文未取得，tariff_inflation 卡以财政部关税收入趋势为硬证据，待回填。
- Warsh 就任日期由“第 100 天”倒推约 5 月 20 日，未从官方新闻稿直接确认。
- 联邦基金期货来自 Yahoo，属交易所数据的二手分发渠道，卡内标为 secondary。
- DuckDuckGo 与 IMF、CME、CBO 对本机 curl 不可用，见各簇原稿第 5 节。
