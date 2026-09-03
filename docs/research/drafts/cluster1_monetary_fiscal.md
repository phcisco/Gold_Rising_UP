# 簇一：货币、利率与财政体制 — 一手来源调研稿

- 研究日：2026-09-03（数据截止日逐项标注）
- 研究员：簇一（货币/利率/财政）
- 方法：全部数字来自官方一手来源（美联储、财政部 Fiscal Data 与收益率曲线、纽约联储、BLS、CFTC、SPDR），新闻仅用于定位事件；预测市场与期货用于定价程度判断。禁用 FRED。
- 卡片：`narratives/drafts/cluster1/*.yaml`（6 张，均通过 YAML 解析）

---

## 1. 簇总览

### 1.1 体制判断：当前处于体制 B（联储主动且可信），起点 2026-06-17

| 证据 | 一手来源 | 数值/措辞 | 截止日 |
|---|---|---|---|
| 声明措辞 | FOMC 声明 6/17（12-0）、7/29（9-3） | "The Committee will deliver price stability" | 2026-07-29 |
| 异议方向 | FOMC 声明 7/29 | Hammack、Kashkari、Logan 三票主张加息 25bp | 2026-07-29 |
| 储备银行意向 | 贴现率会议纪要（8/25 发布） | 克利夫兰、明尼阿波利斯、堪萨斯城、达拉斯申请一级信贷利率升至 4% | 2026-07-29 |
| 主席立场 | Warsh Jackson Hole 讲话 | "65 个月持续高通胀的责任完全在央行"；2% 是 "firm, fixed target" | 2026-08-28 |
| 收益率归因 | 7 月 FOMC 纪要 | "名义收益率上行 25–30bp，由实际利率的相应上升驱动"；"长期通胀补偿稳定" | 2026-07-29 |
| ACM 分解 | 纽约联储 ACM | 10Y 风险中性利率 3.48% → 4.08%（1/2 → 9/1）；10Y 期限溢价 0.80% → 0.78% | 2026-09-01 |
| 实际利率 | 财政部实际收益率曲线 | 10Y TIPS 1.72%（2/27 低点）→ 2.45%（9/2）；年内高点 2.47%（7/31） | 2026-09-02 |
| 盈亏平衡 | 财政部名义-实际 | 10Y 2.34%、5Y 2.35%、30Y 2.29%；年内区间 2.18–2.50% | 2026-09-02 |
| 金价 | CME GC=F（经 Yahoo） | 1/29 峰值 5318 → 9/3 4476（约 -16%）；8/28 单日 -2.9% | 2026-09-03 |
| 政策利率 | 纽约联储 EFFR | 3.63%，目标区间 3.50–3.75%，IORB 3.65% | 2026-09-01 |

**结论**：实际利率重新成为主锚；名义收益率的上行是"预期政策路径"而不是"财政溢价"。体制切换到 A 需要看到：联储在通胀 3%+ 时停止紧缩或转向宽松、盈亏平衡与期限溢价同时上行、实际利率与金价脱钩。这三个条件目前一个都不满足。

### 1.2 张力表

| 叙事 A | 叙事 B | 冲突点 | 当前谁占上风 |
|---|---|---|---|
| real_rate_anchor_regime_switch（主导，bear） | fiscal_dominance_term_premium（边际，bull） | 同一组赤字数据在 B 体制下抬高实际利率压金价，在 A 体制下抬高期限溢价推金价 | 实际利率锚（ACM 期限溢价持平） |
| fed_hawkish_repricing（共识，bear） | fed_independence_erosion（退潮，bull） | 加息定价能否兑现取决于白宫是否施压 | 加息定价（Polymarket 9 月加息 51.5%、年内 70.5%） |
| fed_hawkish_repricing（共识，bear） | inflation_risk_premium_repricing（退潮，bull） | 加息兑现压低通胀补偿；不兑现则 100bp 缺口释放 | 加息定价 |
| real_rate_anchor_regime_switch | ycc_financial_repression（新兴，bull） | 曲线控制使实际利率失去市场定价意义 | 实际利率锚（Warsh 原则五反对非常规政策） |
| fed_hawkish_repricing（市场比 SEP 更鹰） | 自身 | 期货定价 2027 年 3 月 4.1% vs SEP 2027 年末中位 3.6%；Desk 调查中位数为零加息 | 风险不对称偏向"联储不如市场鹰" |

### 1.3 六张卡片一览

| id | 名称 | 状态（起点） | 定价程度 | 方向 | 体制依赖（A/B） |
|---|---|---|---|---|---|
| real_rate_anchor_regime_switch | 实际利率旧锚回归与体制切换 | 主导（2026-08-28） | 部分 | bear | bull / bear |
| fed_hawkish_repricing | 降息交易出清并反转为加息定价 | 共识（2026-07-29） | 充分 | bear | bull / bear |
| fed_independence_erosion | 美联储独立性受损 | 退潮（2026-06-17） | 已出清 | bull | bull / bear |
| fiscal_dominance_term_premium | 财政贬值与财政主导 | 边际（2026-06-17） | 部分 | bull | bull / bear |
| ycc_financial_repression | 曲线控制 / 金融抑制 | 新兴（2026-07-09） | 未定价 | bull | bull / bear |
| inflation_risk_premium_repricing | 通胀风险溢价重定价 | 退潮（2026-06-17） | 已出清 | bull | bull / bear |

---

## 2. 逐条叙事

### 2.1 real_rate_anchor_regime_switch — 实际利率旧锚回归与体制 A/B 切换

**命题**：只要联储主动且可信（体制 B），10Y 实际收益率就是金价主锚；切换开关是联储对通胀的反应函数。

**逻辑链**：通胀高于目标 → 联储承诺"deliver price stability"并出现加息异议 → 市场把收益率上行全部归因于实际利率与政策路径（盈亏平衡不动） → 实际收益率作为持金机会成本上升 → 金价按旧范式反向运动；若联储在通胀 3%+ 时转向宽松，市场切回体制 A。

**当前证据（官方数值）**：
- 10Y TIPS 实际收益率 2.45%（财政部，2026-09-02），年内低点 1.72%（2/27）、高点 2.47%（7/31）。
- 10Y 盈亏平衡 2.34%（2026-09-02），年内 2.18–2.50%。
- 2s30s 由 1.32（1/29）熊平至 0.88（9/2）；2s10s 0.71 → 0.40。
- ACM：10Y 风险中性利率 +60bp、期限溢价 -1bp（1/2 → 9/1）。
- 金价 5318（1/29）→ 4476（9/3），8/28 当日 GC=F 4609.7 → 4478.1（-2.9%），同日 10Y 实际 +8bp、盈亏平衡 -2bp、2s30s 由 0.99 平至 0.88。
- 7 月纪要原文归因："driven by corresponding increases in real interest rates"。

**体制依赖**：B 下 bear（当前）；A 下 bull（脱钩）。判据为 ACM 分解与盈亏平衡。

**状态与定价**：主导（2026-08-28 起）。定价"部分"：金价已跌 16%，但 CFTC 管理基金净多 144,747 张（2026-08-25，五年 78.5 百分位，2026 年高点，且早于 Warsh 讲话），GLD 1056.62 吨（9/2）较 20 日前 +42 吨、仍低于 2/27 的 1101 吨高点——下跌中仍有流入，多头未出清。

**验证信号**：v1 9/16 FOMC 措辞与金价当日反向（qual）；v2 dfii10 > 2.55（20 日）；v3 cot_mm_net < 100,000（60 日）；v4 t10yie 保持 2.2–2.5；v5 ff_cum_change_bp > 40（加息定价不退）。

**证伪条件**：f1 到 2026-12-31 dfii10 > 2.3 且 gc_front > 5318（脱钩）；f2 联储在 PCE > 3% 时降息/停止紧缩且删去"deliver price stability"（qual，2027-03-31）；f3 到 2026-12-31 t10yie > 2.6 且 2s30s > 1.2。

**张力**：fiscal_dominance_term_premium、fed_independence_erosion、ycc_financial_repression。

**最强反方**：实际收益率 2.45% 已在年内高位，加息若拖累增长，降息预期会迅速回归；16% 回撤或主要是拥挤度释放；央行购金对实际利率不敏感；以 CPI 3.4% 计算的事后实际政策利率仅约 0.3%。

**来源**：FOMC 声明 6/17、7/29；7 月纪要；Warsh 8/28 讲话；财政部名义与实际曲线 CSV；纽约联储 ACM xls；CFTC 72hh-3qpy；SPDR GLD 档案。

### 2.2 fed_hawkish_repricing — 降息交易已出清并反转为加息周期定价

**命题**：市场已把 2026 年降息预期全部出清并定价约 2.4 次加息；黄金失去"降息交易"支撑，但加息已充分定价，进一步利空需要联储比市场更鹰。

**对任务中疑问的核实与解释**（"联邦基金期货正在为 9 月加息定价，2Y 4.39% 高于 EFFR 3.63%"）：
- 纽约联储 EFFR 3.63%（2026-09-01），目标区间 3.50–3.75%。
- CME 联邦基金期货（经 Yahoo，2026-09-03 收盘）：ZQU26 96.30 → 3.70%；ZQV26 3.785%；ZQX26 3.85%；ZQZ26 3.955%；ZQF27 4.005%；ZQH27 4.105%；ZQM27 4.215%；ZQU27 4.24%。
- 9 月合约按当月 EFFR 均值结算，会议 9/16、新利率自 9/17 起覆盖 14/30 天：加息概率 ≈ (3.70−3.63)/(0.25×14/30) ≈ 60%。10 月合约 3.785% ≈ 62% 的一次加息；12 月 3.955% ≈ 1.3 次；2027 年 3 月 4.105% ≈ 1.9 次；2027 年 9 月 4.24% ≈ 2.4 次。
- 与 2Y 4.39% 一致：2Y ≈ 未来两年政策路径均值 + 少量期限溢价（ACM 2Y 期限溢价 0.15%）。
- 官方口径佐证：7 月纪要"市场已完全定价 9 月加息 25bp，并在明年一季度末前再加一次"；6 月 SEP 联邦基金利率中位数 2026 年末 3.8%（3 月为 3.4%）、2027 年 3.6%、2028 年 3.4%、长期 3.1%。
- Polymarket（2026-09-03）：9 月加息 25bp 51.5%、不变 47.5%；10 月前加息 65.5%；"2026 年内加息" 70.5%；"2026 年零降息" 89%；2026 年末上限 4.0% 概率 41%、3.75% 24.5%。
- 通胀背景（BLS）：CPI 同比 4 月 3.81%、5 月 4.25%、6 月 3.53%、7 月 3.36%；核心 7 月 2.48%；6–7 月 NSA 环比 -0.35%、-0.01%。Warsh 引用 PCE 12 个月 3.7%、6 个月年化 4.1%。
- 原因：中东冲突能源冲击 + 关税 + AI 投资需求（纪要 staff 归因）。

**体制依赖**：B 下 bear；A 下（联储拒绝兑现市场定价）bull。

**状态与定价**：共识（2026-07-29）；充分。关键不对称：市场路径（2027 年 3 月 4.1%）比 SEP 中位数（2027 年末 3.6%）更鹰，Desk 调查中位受访者预期零加息、2028 年初降息。鹰派冲击对金价的边际利空基本释放；风险偏向"联储不如市场鹰"。

**验证信号**：v1 9/16 加息且异议为鸽派；v2 dgs2 > 4.5；v3 ff_cum_change_bp > 75 且 Polymarket 年内加息 > 85%；v4 effr > 3.85（加息落地）；v5 8 月 CPI 核心环比 ≥ 0.3%（9/11 前后）。

**证伪条件**：f1 到 2026-12-31 dgs2 < 3.6 且 ff_cum_change_bp < 0；f2 9 月与 10 月均不加息且表态转向宽松（qual，2026-10-28）。

**张力**：fed_independence_erosion；inflation_risk_premium_repricing。

**最强反方**：期货定价 2.4 次加息 vs SEP 隐含 1 次、Desk 调查零次；九位多数在 7 月选择等待；Warsh"承诺一种纪律而非一项决定"；CPI 环比已接近零。若 9 月不加息，短端将大幅重定价，金价反弹。

**来源**：7 月纪要；6 月 SEP 表 1；纽约联储 EFFR API；财政部曲线；CME ZQ（Yahoo，二手渠道的交易所数据）；BLS API；Polymarket Gamma API。

### 2.3 fed_independence_erosion — 美联储独立性受损

**命题**：若白宫对加息公开施压、人事干预或迫使联储与财政部协调，市场将重新定价通胀风险溢价与期限溢价，黄金获得主权信用溢价；当前机制休眠。

**逻辑链**：加息触发白宫反应 → 市场怀疑"deliver price stability"能否兑现 → 盈亏平衡与期限溢价上行、美元走弱 → 实际利率与金价脱钩（体制 A）。

**当前证据**：
- 人事：主席 Kevin Warsh（8/28 自述"第 100 天"，即约 5 月 20 日就任）；Powell 以理事身份留任并投票支持多数；副主席 Jefferson；监管副主席 Bowman（联储理事会页面，更新 2026-05-28）。
- 投票：6/17 12-0；7/29 9-3，异议全部主张加息。贴现率纪要：四家储备银行申请上调至 4%。
- Warsh 7/14 国会证词："这些义务与联储在货币政策执行上的正当独立性是一体的"；8/28 讲话把通胀责任归于央行。
- 制度变动（潜在重燃点）：纪要记载主席提议每年六次会议、"任何变动不影响 2026 年余下日程"；Warsh 表示要改变前瞻指引的形式与功能、"更安静的联储"；五个任务组由外部人士共同领导（含 Andreessen、McMillon、Sharma）。
- 市场：Polymarket "Trump 在 12/31 前试图解除 Powell 理事职务" 8.0%、"Cook 12/31 前离任" 5.75%；9 月会议异议 3 票 36.5%、4 票以上 22.5%（分裂被定价，但方向鹰派）。
- 利率：盈亏平衡 2.34% 处于年内区间下半部，ACM 期限溢价持平，DXY 99.4。

**体制依赖**：本叙事就是 B→A 的切换机制；B 下每次顶住压力都利空黄金。

**状态与定价**：退潮（2026-06-17）；已出清（人事赔率 < 10%，利率无可信度溢价）。

**验证信号**：v1 9/16 加息后 72 小时内白宫公开批评；v2 Polymarket 人事赔率 > 20%；v3 t10yie 20 日 +15bp 且 dxy 同期下跌；v4 正式减少会议/取消 SEP 或新闻发布会（12/9 检查）；v5 出现鸽派异议或删去"deliver price stability"。

**证伪条件**：f1 到 2027-03-31 effr > 3.8 且 t10yie < 2.5（联储顶住压力加息、无可信度折价）；f2 到 2027-06-30 无解职、无公开利率要求、无正式协调声明（qual）。

**最强反方**：总统提名的主席比多数委员更鹰；分裂方向是鹰派；预测市场把人事风险定在 10% 以下；少开会、少指引可解读为"减少对市场的依赖"（Warsh 的 hall-of-mirrors 论）。

**来源**：7 月纪要；贴现率会议纪要 PDF（monetary20260825a1.pdf）；Warsh 8/28 讲话；Warsh 7/14 证词；任务组新闻稿 7/9；理事会成员页；Polymarket。

### 2.4 fiscal_dominance_term_premium — 财政贬值与财政主导

**命题**：赤字与利息支出的复利结构使财政对利率高度敏感；一旦联储转向被动，期限溢价与通胀补偿上行、美元贬值，黄金作为财政贬值对冲重获溢价。

**当前证据（财政部 Fiscal Data，除注明外）**：
- 公共债务总额 40.112 万亿美元，公众持有 32.421 万亿（Debt to the Penny，2026-09-01）。
- FY2026 前 10 个月（2025-10 至 2026-07）：收入 4.485 万亿、支出 6.284 万亿、赤字 1.799 万亿；FY2025 全年赤字 1.775 万亿（MTS 表 1，2026-07-31）。
- 利息支出 FYTD（10 个月）：公众持有债务 0.900 万亿 + 政府账户系列 0.270 万亿 = 1.170 万亿（Interest Expense，2026-07-31）。
- 可流通债务平均利率 3.443%（7 月），5 月 3.386%、6 月 3.411%，逐月上升；短债 3.758%、中期票据 3.309%、长债 3.442%。
- 可流通债务 31.43 万亿，其中短债 6.99 万亿（22.2%）、票据 16.17 万亿、长债 5.48 万亿、TIPS 2.15 万亿（MSPD 表 1，2026-07-31）。
- 拍卖（8 月）：10Y 8/12 投标倍数 2.53、间接 61.0%、得标 4.683%；30Y 8/13 投标倍数 2.39、间接 53.1%、得标 5.216%；20Y 8/19 投标倍数 2.53、间接 55.1%、得标 5.204%。需求正常。
- 30Y 收益率 5.27%（9/2），年内高点 5.31%（8/17）。
- ACM 10Y 期限溢价 0.78%（9/1），2010 年以来第 80 百分位，2026 年区间 0.46–0.89%，年初至今持平；2025 年高点 0.895%（5/21）。

**体制依赖**：8/31 教训的核心案例——同一组赤字数字在 B 下通过实际利率压金价，在 A 下通过期限溢价推金价。实时判据：ACM 分解（期限溢价 + 盈亏平衡同升 = A；风险中性利率升 = B）。

**状态与定价**：边际（2026-06-17）；部分（期限溢价处于高分位说明结构性财政溢价已嵌入，但 2026 年内未随赤字上升；金价在赤字创纪录时下跌 16%）。

**验证信号**：v1 ACM TP10 > 1.00% 且盈亏平衡同升；v2 2s30s > 1.2 且 dfii10 20 日下行（牛陡）；v3 30Y/20Y 拍卖间接 < 50% 且尾部 > 2bp；v4 10 月 MTS 显示 FY2026 利息 > 1.4 万亿、赤字 > 2.0 万亿；v5 11/4 再融资声明上调附息规模或以短债为主。

**证伪条件**：f1 到 2027-03-31 2s30s < 0.6 且 t10yie < 2.4；f2 到 2027-03-31 ACM TP10 < 0.5%（qual，待指标上线）；f3 FY2027 赤字 < 1.5 万亿且利息同比下降（qual，2027-10-31）。

**最强反方**：2026 年收益率上行几乎全是风险中性利率；拍卖倍数与间接份额稳定；短债占比 22% 未失控；市场在说"只要联储可信，财政问题由更高实际利率而非黄金定价"。

**来源**：Debt to the Penny；MTS 表 1；Interest Expense；Average Interest Rates；Auctions Query；MSPD 表 1；ACM xls；财政部曲线。

### 2.5 ycc_financial_repression — 收益率曲线控制 / 金融抑制

**命题**：若任务组结论或财政压力促使联储延长持仓久期、用资产负债表压低长端，实际利率被人为压低而通胀补偿上行，黄金作为金融抑制对冲被重新定价。期权型叙事。

**当前证据**：
- 7/9 新闻稿：主席任务组之"资产负债表政策"（Dynan、Rajan、Stein）审查"充足准备金体制与资产持有构成"的成本、收益与制度含义。
- 7 月纪要："多数参与者"评论资产负债表政策，议题含"联储持有国债的适当期限构成"。
- H.4.1（2026-08-27，截至 8/26 当周）：国库券 5,414 亿（同比 +3,459 亿）；名义中长期国债 3.62 万亿（+353 亿）；通胀指数国债 2,761 亿（-334 亿）；MBS 1.91 万亿（-1,876 亿）；国债合计 4.55 万亿（+3,434 亿）；总资产 6.73 万亿（+1,275 亿）；准备金余额 2.92 万亿（-3,000 亿）。资产负债表重新扩张但集中在短端。
- 反证：Warsh 8/28 原则五"非常规政策……应当节制使用，甚至不用"；原则六"货币很重要"；"任务组建议对当前政策没有影响"。
- 财政部短债占比 22.2%（MSPD 7 月）。

**体制依赖**：仅在 A 下成立；B 下任务组更可能建议中性或缩短构成。

**状态与定价**：新兴（2026-07-09）；未定价（TP10 0.78% 未被压制，30Y 接近年内高点，无官方目标，无预测市场）。

**验证信号**：v1 任务组或纪要建议延长久期/市场功能购买（12/9）；v2 H.4.1 名义中长期持有 6 个月 +1,000 亿；v3 ACM TP10 < 0.30% 而赤字通胀未降；v4 dfii10 60 日 -50bp 且 t10yie 不降（quant）；v5 短债占比 > 25% 且联储扩大国库券购买。

**证伪条件**：f1 到 2027-06-30 任务组与 FOMC 维持/缩短久期、无收益率目标（qual）；f2 到 2027-06-30 dfii10 > 2.0 且 dgs30 > 4.8。

**最强反方**：Warsh 原则明确反非常规政策；Rajan、Stein 以批评 QE 外溢著称；国库券增持是准备金管理技术操作；讨论加息的委员会不会同时压长端。

**来源**：任务组新闻稿 7/9；7 月纪要；H.4.1 8/27；Warsh 8/28 讲话；MSPD 表 1；ACM xls。

### 2.6 inflation_risk_premium_repricing — 通胀风险溢价重定价

**命题**：若通胀在 3%+ 徘徊而联储不再加息，市场将把约 100bp 的"通胀—盈亏平衡"缺口重新定价为通胀风险溢价，盈亏平衡与黄金同升；当前缺口被联储可信度压住。

**当前证据**：
- BLS CPI（NSA）同比：4 月 3.81%、5 月 4.25%、6 月 3.53%、7 月 3.36%；核心 7 月 2.48%；SA 环比 7 月 0.07%、核心 0.22%。
- 财政部曲线（9/2）：10Y 盈亏平衡 2.34%（年内 2.18%[6/24]–2.50%[5/4]）、5Y 2.35%、30Y 2.29%；5y5y 远期约 2.33%（由 5Y/10Y 推算）。
- 7 月纪要：近端通胀补偿在 6 月会议后"显著下降"，长期"稳定并与 2% 一致"，归因于"投资者对委员会兑现物价稳定决心的认知"；5 月 PCE 4.1%、核心 3.4%（staff）。
- Warsh 8/28：PCE 12 个月 3.7%、6 个月年化 4.1%；PCE 篮子 54% 项目涨幅 > 3%（疫前二十年 32%）；"预期锚定良好，但必须密切看守"。
- 6 月 SEP：PCE 2026 年 3.6%（3 月 2.7%）、2027 年 2.3%、2028 年 2.0%；核心 3.3%/2.5%/2.1%。
- 10Y TIPS 拍卖 7/23：投标倍数 2.30、间接 58.3%（正常，无抢购）。

**体制依赖**：B 下 bear（加息压回补偿）；A 下 bull。100bp 缺口是"弹簧"。

**状态与定价**：退潮（2026-06-17）；已出清。

**验证信号**：v1 t10yie 20 日 +15bp；v2 30Y 盈亏平衡 > 2.50%；v3 8 月 CPI 核心环比 ≥ 0.3% 且 9/16 不加息；v4 t10yie 20 日 +10bp 且 dfii10 同期 -10bp；v5 9 月 SEP 上修 2027 年 PCE ≥ 2.5%。

**证伪条件**：f1 到 2026-12-31 t10yie < 2.2；f2 到 2027-03-31 核心 PCE < 2.5% 且 t10yie < 2.4（qual）。

**最强反方**：纪要与主席均称长期预期锚定、市场用回落的盈亏平衡与平淡的 TIPS 需求投票；CPI 环比接近零；三票加息异议与四家储备银行申请上调贴现率使"落后曲线"概率低。

**来源**：BLS API；财政部实际与名义曲线；7 月纪要；6 月 SEP；Warsh 8/28；Auctions Query（TIPS）。

---

## 3. 被否定或重构的候选及证据

| 候选 | 处理 | 证据 |
|---|---|---|
| "实际利率锚已失效、黄金转而定价主权信用溢价"（8/24 报告初版命题） | **否定为当前主导叙事**，重构为体制 A/B 切换卡（real_rate_anchor_regime_switch） | 8/28 当日名义上行由实际利率贡献、盈亏平衡下行、金价 -2.9%、曲线走平；ACM 2026 年期限溢价持平；金价与 10Y 实际收益率自 1/29 以来方向严格相反（+56bp / -16%） |
| "降息交易是否已出清" | **重构**为 fed_hawkish_repricing：不只是出清，而是反转为加息周期定价 | ZQ 条 3.70% → 4.24%；2Y 4.39% vs EFFR 3.63%；纪要"完全定价 9 月加息"；Polymarket 零降息 89% |
| "美联储独立性受损"作为活跃叙事 | **降级为退潮**，保留卡片因其是体制切换机制 | 总统提名主席领导下 12-0 与 9-3（鹰派异议）；人事赔率 < 10%；无可信度溢价 |
| "财政部主动缩短久期 / 财政部—联储事实协调（ATI）" | **未单列**，并入 ycc_financial_repression 的 v5 与 fiscal_dominance 的 v5 | 短债占比 22.2% 未异常；再融资声明未能抓取（见第 5 节），一手证据不足 |
| "通胀预期脱锚" | **否定**当前成立，保留为 inflation_risk_premium_repricing（退潮） | 盈亏平衡 2.34% 处于年内下半部，30Y 2.29% 低于 10Y，纪要与主席均称锚定 |

---

## 4. proposed_indicators（注册表中不存在、卡片需要）

```yaml
proposed_indicators:
  - id: term_premium_10y
    name: 10 年期期限溢价（ACM 模型）
    source: Federal Reserve Bank of New York
    url: https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls
    frequency: daily
    lag: 1 个交易日
    tier: 2
    rationale: 区分体制 A/B 的核心读数；fiscal_dominance、ycc 卡的验证与证伪条件依赖它（列 ACMTP10，Excel 需 xlrd 解析）
  - id: acm_rny10
    name: 10 年期风险中性收益率（ACM）
    source: Federal Reserve Bank of New York
    url: https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls
    frequency: daily
    lag: 1 个交易日
    tier: 2
    rationale: 与 term_premium_10y 一起把名义收益率变动分解为"预期路径"与"溢价"（列 ACMRNY10）
  - id: be_30y
    name: 30 年期盈亏平衡通胀（财政部名义 30Y − 实际 30Y）
    source: U.S. Department of the Treasury
    url: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_real_yield_curve&field_tdr_date_value=2026&page&_format=csv
    frequency: daily
    lag: 当日
    tier: 2
    rationale: 远期通胀溢价读数；inflation_risk_premium 卡 v2；同一 CSV 可派生 be_5y 与 5y5y 远期
  - id: fed_dissent_count
    name: FOMC 异议票数（区分鹰派/鸽派）
    source: Federal Reserve
    url: https://www.federalreserve.gov/newsevents/pressreleases/2026-press-fomc.htm
    frequency: 每次 FOMC
    lag: 当日
    tier: 3
    rationale: 委员会分裂方向是体制判断的直接文本证据；Polymarket 有对应赔率市场
  - id: polymarket_fed_next_hike_prob
    name: Polymarket 下次 FOMC 加息 25bp 概率
    source: Polymarket Gamma API
    url: https://gamma-api.polymarket.com/events?closed=false&tag_slug=fed
    frequency: daily
    lag: 实时
    tier: 3
    rationale: 与 ff_next_change_bp 交叉验证；亦可抓取"年内加息""零降息""人事"市场
  - id: tsy_bill_share
    name: 短债占可流通债务比例
    source: U.S. Treasury Fiscal Data (MSPD Table 1)
    url: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_1?sort=-record_date
    frequency: monthly
    lag: 约 5 个工作日
    tier: 3
    rationale: 财政部缩短久期 = 隐性金融抑制的一半；ycc 卡 v5
  - id: interest_expense_fytd
    name: 公共债务利息支出（财年累计）
    source: U.S. Treasury Fiscal Data
    url: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/interest_expense?sort=-record_date
    frequency: monthly
    lag: 约 1 个月
    tier: 3
    rationale: 财政主导叙事的核心量；fiscal_dominance 卡 v4
  - id: deficit_fytd
    name: 联邦赤字（财年累计，MTS 表 1）
    source: U.S. Treasury Fiscal Data
    url: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_1
    frequency: monthly
    lag: 约 2 周
    tier: 3
    rationale: 替代被 403 拦截的 CBO；取 record_type_cd=SL、sequence 2.x 的 Year-to-Date 行
  - id: avg_interest_rate_marketable
    name: 可流通债务平均利率
    source: U.S. Treasury Fiscal Data
    url: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?sort=-record_date
    frequency: monthly
    lag: 约 1 周
    tier: 3
    rationale: 再融资成本上行速度；与 2Y–30Y 市场收益率的差距是未来利息压力
  - id: auction_indirect_share
    name: 附息债拍卖间接投标份额与投标倍数（10Y/20Y/30Y）
    source: U.S. Treasury Fiscal Data (Auctions Query)
    url: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query?sort=-auction_date
    frequency: 每次拍卖
    lag: 当日
    tier: 3
    rationale: 海外/官方需求的代理；fiscal_dominance 卡 v3（尾部需另配 WI 收益率，暂用定性）
  - id: fed_ust_coupon_holdings
    name: 联储持有名义中长期国债（H.4.1）
    source: Federal Reserve
    url: https://www.federalreserve.gov/releases/h41/current/h41.htm
    frequency: weekly
    lag: 1 天
    tier: 3
    rationale: 久期购买是 YCC 的物证；同页可取 fed_ust_bills_holdings
  - id: cpi_headline_yoy
    name: CPI-U 全项同比（NSA）
    source: U.S. Bureau of Labor Statistics
    url: https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0
    frequency: monthly
    lag: 约 2 周
    tier: 2
    rationale: 通胀—盈亏平衡缺口的分子；同 API 取 CUUR0000SA0L1E 得 cpi_core_yoy（无密钥日限 25 次）
  - id: gold_real_yield_corr_60d
    name: 金价与 10Y 实际收益率 60 日滚动相关系数（派生）
    source: 派生（gc_front、dfii10）
    url: n/a
    frequency: daily
    lag: 当日
    tier: 2
    rationale: 体制 A/B 的量化开关：显著为负 = B，接近零或为正 = A
```

---

## 5. 抓取失败、替代方案与疑问

**失败**
- CBO（cbo.gov）：两种 UA 均 HTTP 403（767 字节拦截页）。替代：财政部 MTS 表 1 的财年累计赤字、Interest Expense 数据集。
- DuckDuckGo HTML 端点：返回 "anomaly" 反爬页（HTTP 202），无结果。全部来源改为直接访问已知官方入口 + 美联储 JSON 索引（`/json/ne-speeches.json`、`ne-press.json`、`ne-testimony.json`，非常好用）。
- 财政部新闻稿列表与"最近再融资文件"页：JS 渲染，HTML 内无 `sb` 链接；8 月再融资声明未取到。影响：fiscal_dominance v5、ycc v5 只能等 11/4 声明时再核。
- 美联储讲话 HTML 列表页正则失败（结构变化），改用 JSON 索引成功。
- Fiscal Data API 的 `page[size]` 需 URL 编码为 `page%5Bsize%5D`，未编码时返回空体导致 JSON 解析失败。
- 贴现率纪要 PDF 路径不是 `/monetarypolicy/files/discountrate_20260729.pdf`，正确路径为 `/newsevents/pressreleases/files/monetary20260825a1.pdf`。
- SPDR GLD xlsx 第一页为免责声明，数据在第二页 "US GLD Historical Archive"，日期列为字符串（如 `02-Sep-2026`）。

**未核实/需主会话注意**
- ZQ 期货来自 Yahoo（交易所数据的二手渠道），YAML 中标为 secondary；隐含概率是本研究员的推算（按 EFFR 月均结算、会议日 9/16），程序化后请由 ff_next_change_bp / ff_cum_change_bp 统一口径。
- CFTC 最新报告日 2026-08-25，早于 8/28 Warsh 讲话；9/4（周五）发布的 9/1 数据是检验多头是否开始出清的第一个观察点。
- 8 月 CPI 发布日按惯例约 9/10–9/11，需程序确认 BLS 日历。
- 老报告称 8/28 金价 -3.2%（可能为现货/盘中），本稿按 GC=F 收盘 -2.9%；两者口径不同，未采用老报告数字。
- Warsh 就任日期由"第 100 天"倒推约 2026-05-20，未从官方新闻稿直接确认（理事会页更新日 2026-05-28 与之一致）。
