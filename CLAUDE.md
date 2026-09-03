# 黄金大作手仪表盘 · 项目约定

设计文档是唯一的需求与架构来源：`docs/design/dashboard-design.md`（决策记录 D01–D24）。动手前先读它的第 0、3、4、5 节。

## 分工原则（不可违背）
- 规则程序只处理封闭式问题：抓数据、算指标、监控信号、核对可量化条件、写日志、做审计。
- AI 分析师处理开放式判断：叙事状态、定价程度、张力、情景概率、方向与信心、新闻解读、调研。每条判断必须引用数据或链接。
- 用户只读、可选覆盖。任何流程都不得把"人工确认"或"人工定级"放在关键路径上。

## 数据质量硬规则
- 指标值只取官方或一手来源的最新正式发布值；新闻里的行情数字禁止作为指标值。
- 每个数据点带出处（provider、publisher、series、as_of、fetched_at、lag_days），见 `contracts/datapoint.py`。
- 指标由 `indicators/registry.yaml` 驱动，增删指标只改配置。级别：1 常驻 / 2 叙事证据 / 3 背景与观察池 / target 标的监控。一级指标的增删需版本化留痕，AI 不能改。
- 抓取失败必须记录并在页面上标注，绝不静默；缺失时发布"仅数据"版本并显著提示。
- 已知网络事实：本机直连 `fred.stlouisfed.org` 被拦截，FRED 只能走 API（需 `FRED_API_KEY`）；Yahoo `CNH=X` 无历史数据，用 `CNY=X`；Stooq 有 JS 人机验证不可无人值守；财政部站点对 `python-requests` UA 限速，必须带浏览器样式 UA。

## 代码结构与规范
- Python 3.11，`src/goldrising/{cli,contracts,data,compute,rules,render,publish}`；`contracts` 不依赖下游；`compute`、`rules` 不依赖 `data.providers` 与 `render`。
- 文档、注释、commit message 中文；标识符英文。CLI 形如 `gold <domain> <verb>`。
- `make check`（ruff、mypy、pytest，覆盖率门槛 40%，只覆盖 compute/contracts/rules）为唯一门禁。
- 第三方库必须在 `pyproject.toml` 声明；`openpyxl` 等重依赖在函数内导入。
- 禁止版本号后缀文件名；业务逻辑不放 `scripts/`。
- 密钥只经环境变量或 `.env`（不入库）。不要读取 `.env`。
- `data/curated/`、`data/snapshots/` 不入库：第三方数据（SPDR、Yahoo、Cboe）有再分发限制，官方源可随时重抓；公开仓库只发布 `site/` 渲染页面与代码、叙事库、文档。

## 常用命令
- `make install`：创建 `.venv` 并安装。
- `.venv/bin/gold registry validate|list`
- `.venv/bin/gold data fetch [--only id1,id2]`
- `.venv/bin/gold compute run` → `data/snapshots/latest.json`
- `.venv/bin/gold render page` → `site/index.html` 与 `site/YYYY-MM-DD.html`
- `.venv/bin/gold narratives validate [--include-drafts]`：叙事卡结构校验
- `.venv/bin/gold run daily`：全流程；存在 origin 时自动提交 `site/` 并推送，`GOLD_PUBLISH_PUSH=0` 关闭。
- `bash scripts/install-launchd.sh install|status|run-now`：工作日 07:30 定时任务（周二至周六）。

## 阶段状态
- 第 0 阶段（已完成 2026-09-03）：叙事库 `narratives/*.yaml` 20 张卡（12 活跃、5 退潮、3 归档），体制判断在 `narratives/_library.yaml`，总报告 `docs/research/gold-narratives-2026-09.md`。分簇原稿在 `docs/research/drafts/` 与 `narratives/drafts/`。
- 子代理调研只能用 curl 抓取（WebFetch/WebSearch 在后台代理中会挂起），约定见 `docs/research/RESEARCH_TOOLING.md`。
- 第 1 阶段：数据层与 L1 行情台（本仓库当前）。
- 第 2 阶段：规则层扩展、AI 分析师、L2 到 L4；第 3 阶段：L5、校准审计、飞书推送。
