# SEO Dashboard AI Kit

Kết nối Claude (và các AI khác) với dữ liệu SEO thật của bạn trong
[GSC Dashboard](https://tool.nguyenvietloc.com): Search Console, GA4, Google Ads, content changes,
backlinks. Kèm một bộ skill để **phân tích kết quả → tìm nguyên nhân và cơ hội → lên kế hoạch → triển
khai → đo lại**.

Repo này chỉ chứa phần dùng chung (cấu hình MCP + skill). Dashboard và dữ liệu vẫn nằm ở
tool.nguyenvietloc.com. Không có token hay dữ liệu nào trong repo.

## Cài nhanh

**Claude Code** (mọi project, một lần):
```
/plugin marketplace add vilo0411/seo-dashboard-ai-kit
/plugin install seo-dashboard@seo-dashboard-ai-kit
```
Sau đó chạy `/mcp` → `gsc-dashboard` → **Authenticate** → đăng nhập dashboard → **Allow**.

**Claude.ai** (cá nhân hoặc công ty): Settings → Connectors → Add custom connector →
`https://tool.nguyenvietloc.com/api/mcp`. Skill: tải các file `.zip` ở
[Releases](https://github.com/vilo0411/seo-dashboard-ai-kit/releases/latest) rồi upload ở
Settings → Capabilities → Skills.

**Hoặc bảo AI:** *"Cài SEO kit từ github.com/vilo0411/seo-dashboard-ai-kit theo INSTALL.md"*.
Chi tiết cho từng client có trong [INSTALL.md](INSTALL.md).

## Có gì bên trong

| | |
|---|---|
| `plugins/seo-dashboard/.mcp.json` | Kết nối MCP tới dashboard (OAuth, không cần token) |
| `plugins/seo-dashboard/skills/` | Các skill `seodash-*`: `core`, `diagnose`, `opportunities`, `roadmap` (đang mở rộng, xem kế hoạch) |
| `plugins/seo-dashboard/commands/` | Lệnh tắt Claude Code: `/seo-why`, `/seo-wins`, `/seo-plan` |
| `tools.txt`, `scripts/check-tool-names.py` | Danh sách tool của MCP; CI báo lỗi nếu skill nhắc tool không tồn tại |
| `docs/SKILLS_PLAN.md` | Kế hoạch và mô tả chi tiết bộ skill |

## Cập nhật

Claude Code: `/plugin marketplace update seo-dashboard-ai-kit`. Claude.ai: tải lại zip ở bản Release mới.

## Phát hành

Sửa skill → commit → `git tag v0.x.y && git push --tags`. GitHub Action sẽ đóng gói zip và tạo Release.
