# 黄金大作手仪表盘

站点：https://phcisco.github.io/Gold_Rising_UP/ （公开链接，已设 noindex，仅供小范围参考）

每日更新的黄金跨资产行情与叙事仪表盘。规则程序负责事实，AI 分析师负责判断，读者只读参考。

- 设计文档：[docs/design/dashboard-design.md](docs/design/dashboard-design.md)
- 指标注册表：[indicators/registry.yaml](indicators/registry.yaml)
- 叙事卡规范：[docs/design/narrative-card-schema.md](docs/design/narrative-card-schema.md)

## 快速开始

```bash
make install
cp .env.example .env   # 按需填写 FRED_API_KEY 等
.venv/bin/gold run daily
open site/index.html
```

站点由 GitHub Pages 通过 `.github/workflows/pages.yml` 发布 `site/` 目录（Pages 来源选 GitHub Actions）。
