"""L1 行情台页面渲染。输入是快照 JSON，输出是单文件 HTML。"""

from __future__ import annotations

import html
from typing import Any

from goldrising.render.svg import percentile_bar, sparkline
from goldrising.render.theme import CSS, FONT_LINK

TIER_LABEL = {"1": ("一级", "t1"), "2": ("二级", "t2"), "3": ("三级", "t3"), "target": ("标的", "tt")}


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def fmt_value(v: float | None, unit: str, decimals: int) -> str:
    if v is None:
        return "—"
    if unit == "pct":
        return f"{v:.{decimals}f}%"
    if unit == "pctl":
        return f"{v:.0f} 分位"
    if unit == "pct_change":
        return f"{v:+.{decimals}f}%"
    if unit == "bp":
        return f"{v:+.0f}bp"
    if unit in {"usd"}:
        return f"{v:,.{decimals}f}"
    if unit in {"contracts", "tonnes", "count"}:
        return f"{v:,.{decimals}f}"
    return f"{v:,.{decimals}f}"


def fmt_change(entry: dict[str, Any], horizon: str) -> tuple[str, str]:
    ch = (entry.get("changes") or {}).get(horizon) or {}
    unit = entry.get("unit")
    decimals = int(entry.get("decimals", 2))
    abs_v = ch.get("abs")
    pct_v = ch.get("pct")
    if abs_v is None:
        return "—", "flat"
    cls = "up" if abs_v > 0 else "down" if abs_v < 0 else "flat"
    if unit in {"pct", "pct_change"}:
        return f"{abs_v * 100:+.0f}bp", cls
    if unit == "pctl":
        return f"{abs_v:+.1f} pt", cls
    if unit == "bp":
        return f"{abs_v:+.0f}bp", cls
    if pct_v is not None and unit in {"usd", "index", "ratio", "tonnes"}:
        return f"{pct_v:+.2f}%", cls
    return f"{abs_v:+.{decimals}f}", cls


def gold_sign_hint(entry: dict[str, Any]) -> str:
    sign = int(entry.get("gold_sign", 0))
    ch = (entry.get("changes") or {}).get("5d") or {}
    abs_v = ch.get("abs")
    if sign == 0 or abs_v is None or abs_v == 0:
        return ""
    bullish = (abs_v > 0) == (sign > 0)
    return "近 5 日变动对金价：偏多" if bullish else "近 5 日变动对金价：偏空"


def render_flags(entry: dict[str, Any]) -> str:
    return "".join(
        f'<span class="flag {esc(f.get("code", ""))}" title="{esc(f.get("detail", ""))}">{esc(f.get("label", ""))}</span>'
        for f in entry.get("flags", [])
    )


def tier_badge(tier: str) -> str:
    label, cls = TIER_LABEL.get(tier, (tier, ""))
    return f'<span class="tier {cls}">{label}</span>'


def render_card(entry: dict[str, Any]) -> str:
    unit = str(entry.get("unit"))
    dec = int(entry.get("decimals", 2))
    chg_txt, chg_cls = fmt_change(entry, "1d" if entry.get("frequency") == "daily" else "5d")
    chg20_txt, chg20_cls = fmt_change(entry, "20d")
    pct = entry.get("pct_10y")
    pct_label = "10 年"
    if pct is None:
        pct, pct_label = entry.get("pct_5y"), "5 年"
    if pct is None:
        first = str(entry.get("first_date") or "")[:7]
        pct, pct_label = entry.get("pct_all"), (f"自 {first} " if first else "全史")
    hint = gold_sign_hint(entry)
    prov = entry.get("provenance") or {}
    stale_note = ""
    sd = entry.get("staleness_days")
    if isinstance(sd, int) and sd > 0:
        stale_note = f"滞后 {sd} 天"
    note = entry.get("note") or ""
    hint_html = f'<div class="sub">{esc(hint)}</div>' if hint else ""
    short_note = esc(note[:60]) + ("…" if len(note) > 60 else "")
    note_html = f'<div class="sub" title="{esc(note)}">{short_note}</div>' if note else ""
    return (
        '<div class="card">'
        f'<div class="top"><span class="name">{esc(entry["name"])}{tier_badge(str(entry.get("tier")))}</span>'
        f'<span class="val n">{esc(fmt_value(entry.get("last"), unit, dec))}</span></div>'
        f'<div class="meta"><span>日变动 <b class="chg {chg_cls} n">{esc(chg_txt)}</b></span>'
        f'<span>20 日 <b class="chg {chg20_cls} n">{esc(chg20_txt)}</b></span></div>'
        f"{sparkline(entry.get('sparkline') or [])}"
        f"{percentile_bar(pct, pct_label)}"
        f'<div class="meta" style="margin-top:14px"><span>数据截止 <span class="n">{esc(entry.get("last_date") or "—")}</span>'
        f"{(' · ' + stale_note) if stale_note else ''}</span><span>{esc(prov.get('publisher', ''))}</span></div>"
        f"<div>{render_flags(entry)}</div>"
        f"{hint_html}"
        f"{note_html}"
        "</div>"
    )


def render_overview(snapshot: dict[str, Any]) -> str:
    inds: dict[str, Any] = snapshot["indicators"]
    rows = []
    order = [g["id"] for g in snapshot["groups"]]
    tier1 = [e for e in inds.values() if e.get("tier") == "1"]
    tier1.sort(key=lambda e: (order.index(e["group"]) if e["group"] in order else 99, e["name"]))
    for e in tier1:
        chg_txt, chg_cls = fmt_change(e, "1d" if e.get("frequency") == "daily" else "5d")
        chg20, cls20 = fmt_change(e, "20d")
        pct = e.get("pct_10y")
        pct_txt = f"{pct:.0f}" if pct is not None else "—"
        if pct is None and e.get("pct_5y") is not None:
            pct_txt = f"{e['pct_5y']:.0f}（5 年）"
        elif pct is None and e.get("pct_all") is not None:
            pct_txt = f"{e['pct_all']:.0f}（自 {str(e.get('first_date') or '')[:4]}）"
        z = e.get("z_250")
        z_txt = f"{z:+.1f}" if isinstance(z, int | float) else "—"
        rows.append(
            "<tr>"
            f'<td>{esc(e["name"])}<br><span class="sub">{esc(e.get("last_date") or "")}</span></td>'
            f'<td class="n">{esc(fmt_value(e.get("last"), str(e.get("unit")), int(e.get("decimals", 2))))}</td>'
            f'<td class="n chg {chg_cls}">{esc(chg_txt)}</td>'
            f'<td class="n chg {cls20}">{esc(chg20)}</td>'
            f'<td class="n">{pct_txt}</td><td class="n">{z_txt}</td>'
            f"<td style='text-align:left'>{render_flags(e)}</td>"
            "</tr>"
        )
    return (
        '<div class="tblwrap"><table><thead><tr><th>一级指标</th><th>最新</th><th>日变动</th><th>20 日</th>'
        "<th>10 年分位</th><th>z 分</th><th style='text-align:left'>标记</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def render_kpis(snapshot: dict[str, Any]) -> str:
    inds = snapshot["indicators"]
    picks = [
        "gold_nav_implied",
        "gc_c1",
        "dfii10",
        "t10yie",
        "dxy",
        "gvz",
        "cot_mm_net_pctl",
        "gld_tonnes",
        "ff_next_change_bp",
    ]
    cells = []
    for pid in picks:
        e = inds.get(pid)
        if not e:
            continue
        chg_txt, chg_cls = fmt_change(e, "1d" if e.get("frequency") == "daily" else "5d")
        cells.append(
            f'<div class="kpi"><div class="l">{esc(e["name"])}</div>'
            f'<div class="v n">{esc(fmt_value(e.get("last"), str(e.get("unit")), int(e.get("decimals", 2))))}</div>'
            f'<div class="sub"><span class="chg {chg_cls} n">{esc(chg_txt)}</span> · {esc(e.get("last_date") or "")}</div></div>'
        )
    return f'<div class="kpis">{"".join(cells)}</div>'


def render_anomalies(snapshot: dict[str, Any]) -> str:
    items = []
    for e in snapshot["indicators"].values():
        for f in e.get("flags", []):
            if f.get("code") in {"jump", "extreme_high", "extreme_low"}:
                items.append(f"<li><b>{esc(e['name'])}</b>：{esc(f['label'])}，{esc(f['detail'])}</li>")
    if not items:
        return '<div class="callout">今日无指标级异动与历史极值。</div>'
    return f'<div class="callout warn"><b>规则层异动清单</b>（阈值：日变动 z 分 ≥ 2.5，或 10 年分位 ≤ 5 / ≥ 95）<ul>{"".join(items)}</ul></div>'


def render_fedwatch(snapshot: dict[str, Any]) -> str:
    fw = snapshot.get("fedwatch")
    if not fw:
        return '<div class="callout">联邦基金期货隐含路径今日未生成。</div>'
    rows = []
    for m in fw.get("meetings", []):
        probs = m.get("probabilities", {})
        prob_txt = "，".join(
            f"{k}bp {v * 100:.0f}%" for k, v in sorted(probs.items(), key=lambda kv: int(kv[0].replace("+", "")))
        )
        rows.append(
            f'<tr><td class="n">{esc(m["date"])}</td><td class="n">{m["pre_rate"]:.2f}%</td><td class="n">{m["post_rate"]:.2f}%</td>'
            f'<td class="n chg {"down" if m["change_bp"] < 0 else "up" if m["change_bp"] > 0 else "flat"}">{m["change_bp"]:+.0f}</td>'
            f'<td class="n">{m["cum_change_bp"]:+.0f}</td><td style="text-align:left">{esc(prob_txt)}</td>'
            f'<td class="sub">{"次月合约" if m["method"] == "next_month" else "月内拆分"}</td></tr>'
        )
    return (
        f'<p class="sub">数据截止 <span class="n">{esc(fw.get("as_of"))}</span>，有效联邦基金利率 <span class="n">{fw.get("effr"):.2f}%</span>。'
        f"{esc(fw.get('method', ''))}</p>"
        '<div class="tblwrap"><table><thead><tr><th>FOMC 决议日</th><th>会前</th><th>会后隐含</th><th>变动 bp</th><th>累计 bp</th>'
        "<th style='text-align:left'>两档概率</th><th>方法</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def render_groups(snapshot: dict[str, Any]) -> str:
    inds = snapshot["indicators"]
    tier_order = {"1": 0, "target": 1, "2": 2, "3": 3}
    parts = []
    for g in snapshot["groups"]:
        members = [e for e in inds.values() if e["group"] == g["id"]]
        if not members:
            continue
        members.sort(key=lambda e: (tier_order.get(str(e.get("tier")), 9), e["name"]))
        parts.append(
            f'<section class="group" id="g-{esc(g["id"])}"><h3>{esc(g["name"])}</h3><p class="q">{esc(g.get("question", ""))}</p>'
            f'<div class="cards">{"".join(render_card(e) for e in members)}</div></section>'
        )
    return "".join(parts)


def render_sources(snapshot: dict[str, Any]) -> str:
    rows = []
    seen: set[tuple[str, str]] = set()
    for e in snapshot["indicators"].values():
        p = e.get("provenance") or {}
        key = (p.get("publisher", ""), p.get("provider", ""))
        if key in seen or p.get("provider") == "derived":
            continue
        seen.add(key)
        url = p.get("url") or ""
        link = f'<a href="{esc(url)}" rel="noopener">{esc(url[:70])}</a>' if url else ""
        rows.append(
            f'<tr><td>{esc(p.get("publisher", ""))}</td><td style="text-align:left">{esc(p.get("provider", ""))}</td>'
            f'<td style="text-align:left">{link}</td><td class="n">{esc(str(p.get("fetched_at", ""))[:19])}</td></tr>'
        )
    missing = snapshot.get("missing") or []
    fr = snapshot.get("fetch_report") or {}
    failed = [r for r in fr.get("results", []) if r.get("status") in {"failed", "skipped"}]
    fail_html = ""
    if failed:
        fail_html = (
            "<p><b>今日未更新的指标</b>："
            + "；".join(f"{esc(r['indicator_id'])}（{esc(r.get('message', '')[:80])}）" for r in failed)
            + "</p>"
        )
    miss_html = f"<p><b>尚未接入的注册表条目</b>：{esc('、'.join(missing))}</p>" if missing else ""
    return (
        '<div class="tblwrap"><table><thead><tr><th>发布机构</th><th style="text-align:left">适配器</th>'
        '<th style="text-align:left">来源页面</th><th>抓取时间 UTC</th></tr></thead><tbody>'
        + "".join(rows)
        + "</tbody></table></div>"
        + fail_html
        + miss_html
    )


def render_page(snapshot: dict[str, Any], archive_dates: list[str] | None = None) -> str:
    run_date = snapshot.get("run_date", "")
    gen = snapshot.get("generated_at", "")
    gold = snapshot["indicators"].get("gold_nav_implied") or {}
    gold_txt = fmt_value(gold.get("last"), "usd", 1) if gold else "—"
    fut = snapshot["indicators"].get("gc_c1") or {}
    fut_txt = fmt_value(fut.get("last"), "usd", 1) if fut else "—"
    nav = archive_dates or []
    nav_html = " ".join(f'<a href="{esc(d)}.html">{esc(d)}</a>' for d in nav[-7:])
    n_ind = len(snapshot["indicators"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>黄金大作手 · 行情台 {esc(run_date)}</title>
{FONT_LINK}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="header">
  <div>
    <div class="eyebrow">黄金大作手 · 跨资产行情台 · 第 1 阶段</div>
    <h1>黄金行情台 <span class="n" style="font-size:20px;color:var(--ink)">{esc(run_date)}</span></h1>
    <div class="sub">基准金价（GLD 官方 NAV 隐含，≈LBMA 定盘）<b class="n">{esc(gold_txt)}</b> · COMEX 活跃合约 <b class="n">{esc(fut_txt)}</b> · 指标 {n_ind} 个 · 生成于 <span class="n">{esc(gen)}</span> UTC · 所有数值来自官方或一手来源的最新正式发布，每个指标卡标注数据截止日与发布机构</div>
    <div class="nav">归档：{nav_html} <a href="archive.html">全部</a></div>
  </div>
</header>

<h2>今日速览</h2>
{render_kpis(snapshot)}
{render_anomalies(snapshot)}
<div style="margin-top:14px">{render_overview(snapshot)}</div>

<h2>联邦基金期货隐含路径</h2>
{render_fedwatch(snapshot)}

<h2>L1 行情台 · 分因子组</h2>
<p class="sub">级别：一级为常驻体制仪表；二级为叙事证据；三级为背景与观察池；标的为交易标的监控。分位条为该指标最新值在历史窗口中的位置。</p>
{render_groups(snapshot)}

<h2>数据来源与口径</h2>
{render_sources(snapshot)}

<footer class="foot">
  <p><b>口径说明</b>：日变动为最新两个观测日之差；利率类以基点显示；分位数按频率换算窗口（日频 10 年约 2520 个观测）。派生指标由官方序列计算，计算式见指标注册表。联邦基金隐含路径按 CME FedWatch 公开方法由 30 天联邦基金期货复算，不抓取 CME 页面。</p>
  <p><b>已知限制</b>：期货价格为 Yahoo 分发的收盘报价而非 CME 官方结算价；LBMA 定盘价需 ICE 授权，以 GLD 官方 NAV 隐含金价替代（10:30 纽约时间口径）；CFTC 持仓滞后三天；高收益利差需 FRED 密钥。</p>
  <div class="roadmap">
    <div><b>第 2 阶段</b> 叙事引擎、叙事地图、验证跟踪台，AI 分析师日评</div>
    <div><b>第 3 阶段</b> 情景展望与方向卡、校准审计、飞书推送</div>
  </div>
  <p style="margin-top:14px">本页为个人研究工具的自动生成结果，仅供参考，不构成投资建议。作者不是持牌投资顾问。</p>
</footer>
</div>
</body>
</html>
"""


def render_archive(dates: list[str]) -> str:
    items = "".join(f'<li><a href="{esc(d)}.html" class="n">{esc(d)}</a></li>' for d in sorted(dates, reverse=True))
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>黄金大作手 · 归档</title>{FONT_LINK}<style>{CSS}</style></head>
<body><div class="wrap"><header class="header"><div><div class="eyebrow">黄金大作手</div><h1>逐日归档</h1>
<div class="nav"><a href="index.html">返回最新</a></div></div></header><ul>{items}</ul></div></body></html>
"""
