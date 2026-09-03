"""视觉体系：沿用《黄金的新定价锚》的金、青、砖红三主色与双主题；中文字体 Noto。"""

CSS = r"""
:root{
  --metal:#8F6216; --metal-soft:#C9A227; --paper:#155A6B; --warn:#9E3B26; --ok:#2E7D5B;
  --bg:#F7F5F0; --card:#FFFFFF; --ink:#1E1E1C; --muted:#6B675F; --line:#E4DFD3; --chip:#EFE9DB;
  --up:#B23B2E; --down:#2E7D5B;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#15140F; --card:#1E1C16; --ink:#EDE8DC; --muted:#A39D90; --line:#33302A; --chip:#2A271F;
    --metal:#D4A63A; --paper:#4FA3B8; --warn:#E06E55; --ok:#5DBB8E; --up:#E06E55; --down:#5DBB8E;
  }
}
:root[data-theme="dark"]{
  --bg:#15140F; --card:#1E1C16; --ink:#EDE8DC; --muted:#A39D90; --line:#33302A; --chip:#2A271F;
  --metal:#D4A63A; --paper:#4FA3B8; --warn:#E06E55; --ok:#5DBB8E; --up:#E06E55; --down:#5DBB8E;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;font-size:15px;line-height:1.55}
.wrap{max-width:1180px;margin:0 auto;padding:20px 16px 60px}
h1,h2,h3{font-family:"Noto Serif SC","Songti SC",Georgia,serif;font-weight:600;letter-spacing:.01em;margin:0}
h1{font-size:28px;color:var(--metal)}
h2{font-size:20px;margin:36px 0 12px;padding-left:10px;border-left:4px solid var(--metal)}
h3{font-size:16px;margin:0 0 6px}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper);font-weight:600}
.sub{color:var(--muted);font-size:13px}
.n{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;font-variant-numeric:tabular-nums}
.header{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:flex-end;padding-bottom:14px;border-bottom:1px solid var(--line)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.kpi .v{font-size:22px;font-weight:600}
.kpi .l{font-size:12px;color:var(--muted)}
.chg.up{color:var(--up)} .chg.down{color:var(--down)} .chg.flat{color:var(--muted)}
.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap;vertical-align:middle}
th{font-weight:600;color:var(--muted);font-size:12px;background:var(--chip);position:sticky;top:0}
td:first-child,th:first-child{text-align:left;white-space:normal;min-width:150px}
tr:last-child td{border-bottom:none}
.tier{display:inline-block;font-size:10.5px;padding:1px 6px;border-radius:999px;background:var(--chip);color:var(--muted);margin-left:6px;vertical-align:middle}
.tier.t1{background:var(--metal);color:#fff}
.tier.tt{background:var(--paper);color:#fff}
.flag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:999px;margin:0 2px 2px 0;border:1px solid var(--line);color:var(--muted)}
.flag.jump{border-color:var(--warn);color:var(--warn)}
.flag.extreme_high,.flag.extreme_low{border-color:var(--metal);color:var(--metal)}
.flag.stale{border-color:var(--muted);background:var(--chip)}
.group{margin-top:22px}
.group .q{color:var(--muted);font-size:13px;margin:0 0 10px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.card .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.card .name{font-size:13.5px;font-weight:600}
.card .val{font-size:22px;font-weight:600}
.card .meta{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);gap:8px;flex-wrap:wrap}
.card svg{width:100%;height:46px;display:block}
.pbar{position:relative;height:6px;background:var(--chip);border-radius:3px;margin-top:4px}
.pbar i{position:absolute;top:-3px;width:3px;height:12px;background:var(--metal);border-radius:2px}
.pbar .lbl{position:absolute;right:0;top:8px;font-size:11px;color:var(--muted)}
.callout{border-left:4px solid var(--paper);background:var(--card);padding:10px 14px;border-radius:0 10px 10px 0;margin:12px 0;font-size:14px}
.callout.warn{border-color:var(--warn)}
.foot{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:12.5px}
.foot p{margin:6px 0}
.roadmap{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:10px}
.roadmap div{background:var(--card);border:1px dashed var(--line);border-radius:10px;padding:10px 12px;font-size:13px;color:var(--muted)}
.roadmap b{color:var(--ink)}
.nav{font-size:13px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;margin-top:8px}
.nav a{color:var(--paper);text-decoration:none}
a{color:var(--paper)}
@media (max-width:640px){body{font-size:14px}.wrap{padding:14px 10px 40px}h1{font-size:23px}.kpi .v{font-size:19px}.card .val{font-size:20px}}
"""

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600&family=Noto+Serif+SC:wght@600'
    '&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
)
