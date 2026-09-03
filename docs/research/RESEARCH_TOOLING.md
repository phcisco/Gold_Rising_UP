# 调研代理的抓取工具约定（本机环境）

WebFetch 与 WebSearch 在本环境会因权限判定超时而挂起，**禁止使用**。全部网络访问走 Bash 的 curl，并遵守：

- 每次请求必带 `-sL -m 30 -A "Mozilla/5.0"`；同一地址最多重试 2 次；失败即记录并换来源，不要卡住。
- 搜索用 DuckDuckGo HTML 端点，再解析结果链接：
  `curl -sL -m 30 -A "Mozilla/5.0" "https://html.duckduckgo.com/html/?q=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' 'site:federalreserve.gov Jackson Hole 2026 speech')" | grep -o 'uddg=[^&"]*' | head -10 | python3 -c 'import sys,urllib.parse; [print(urllib.parse.unquote(l.strip()[5:])) for l in sys.stdin]'`
- 网页转文本：`curl ... | python3 -c 'import sys,re,html; s=sys.stdin.read(); s=re.sub(r"<(script|style)[^>]*>.*?</\1>","",s,flags=re.S); print(html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",s))))' | cut -c1-20000`
- PDF 转文本：先建一次临时环境 `uv venv /tmp/gold_research_venv -q && uv pip install --python /tmp/gold_research_venv/bin/python -q pypdf`，然后 `curl -sL -m 60 -A "Mozilla/5.0" -o /tmp/x.pdf URL && /tmp/gold_research_venv/bin/python -c 'import pypdf,sys; r=pypdf.PdfReader("/tmp/x.pdf"); print("\n".join((p.extract_text() or "") for p in r.pages[:40]))' | cut -c1-30000`
- 已知网络事实：`fred.stlouisfed.org` 被拦截且无密钥，**不要用 FRED**；财政部收益率 CSV、纽约联储 API、Cboe CSV、CFTC Socrata、SPDR xlsx、Yahoo 图表接口、Polymarket Gamma API 均可用。

可直接使用的一手数据入口：
- 美国财政部收益率：`https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv`（实际利率把 type 换成 `daily_treasury_real_yield_curve`）
- 财政部财政数据 API：`https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&page[size]=5`；月度财政报表 `.../v1/accounting/mts/mts_table_1?sort=-record_date&page[size]=12`
- 纽约联储 EFFR：`https://markets.newyorkfed.org/api/rates/unsecured/effr/last/10.json`；ACM 期限溢价页面 `https://www.newyorkfed.org/research/data_indicators/term-premia-tabs`
- 美联储：FOMC 日历 `https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm`；新闻稿列表 `https://www.federalreserve.gov/newsevents/pressreleases.htm`；讲话列表 `https://www.federalreserve.gov/newsevents/speeches.htm`
- BLS 公共 API（无需密钥，日限 25 次）：`https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?latest=true`（CPI 全项）、`CUUR0000SA0E`（能源）、`CUUR0000SA0L1E`（核心）
- BEA：`https://apps.bea.gov/` 页面；EIA 现货油价 CSV：`https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls`（Brent 日度）
- CFTC 黄金分类持仓：`https://publicreporting.cftc.gov/resource/72hh-3qpy.json?$where=cftc_contract_market_code='088691'&$order=report_date_as_yyyy_mm_dd%20DESC&$limit=10`
- SPDR GLD 档案（xlsx）：`https://api.spdrgoldshares.com/api/v1/historical-archive?product=gld&exchange=NYSE&lang=en`
- Cboe：`https://cdn.cboe.com/api/global/us_indices/daily_prices/GVZ_History.csv`、`VIX_History.csv`
- Yahoo 图表：`https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF?range=1y&interval=1d`
- Polymarket：`https://gamma-api.polymarket.com/markets?closed=false&limit=100&order=volume24hr&ascending=false`
- 世界黄金协会：`https://www.gold.org/goldhub/research`、`https://www.gold.org/goldhub/data/gold-reserves-by-country`；IMF 笔记与数据：`https://www.imf.org/en/Publications/`、`https://data.imf.org/`
- BIS 巴塞尔框架：`https://www.bis.org/basel_framework/`；中国央行储备（外汇局）：`https://www.safe.gov.cn/`；上金所：`https://www.sge.com.cn/`

进度汇报：每完成一条叙事或每 10 分钟，向 `docs/research/drafts/<cluster>_progress.md` 追加一行 `HH:MM 状态`，让主会话能监控。

## 2026-09-04 补充：实测可用的搜索与绕行方式
- DuckDuckGo 与 Bing 对本机 curl 均不可用（人机验证或结果不可解析）；**Brave 搜索可用**：`curl -sL -m 30 -A "Mozilla/5.0" "https://search.brave.com/search?q=<urlencoded>"` 再用正则抽链接。学术文献用 Semantic Scholar 与 OpenAlex 的公开 API 搜索更稳。
- Wayback 的 availability API 易 429，直连 `https://web.archive.org/web/2026id_/<原url>` 更稳（`id_` 取原始内容）。imf.org、tcd.ie、cmegroup.com 等对 curl 拒绝的站点多可经 Wayback 取得。
- 美联储的讲话与新闻稿有 JSON 索引：`https://www.federalreserve.gov/json/ne-speeches.json`、`ne-press.json`、`ne-testimony.json`。
- 财政部 Fiscal Data API 的方括号参数必须 URL 编码（`page%5Bsize%5D`）。
- 世界黄金协会的方法 PDF 与数据下载在免费注册门后，页面文本可读。
