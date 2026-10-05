# Kế hoạch bộ skill — SEO Dashboard AI Kit

## Mục tiêu

Biến dữ liệu thật của các dự án (Search Console, GA4, Google Ads, content changes, backlinks… trong
dashboard `tool.nguyenvietloc.com`) thành **quyết định SEO có thể triển khai**. Mọi câu trả lời phải
đi qua chuỗi: **phân tích kết quả → tìm nguyên nhân / cơ hội → ưu tiên → kế hoạch triển khai → đo lại**.

Bộ skill **không** thay thế công cụ crawl hay audit kỹ thuật (đã có plugin `claude-seo`). Nó làm phần
mà crawler không làm được: đọc hiệu quả thật của site, tức là số liệu click, thứ hạng và chuyển đổi
của chính bạn.

## Nguyên tắc chung (áp dụng cho mọi skill)

1. **Số liệu trước, ý kiến sau.** Mỗi nhận định phải có số liệu kèm mốc so sánh. Thiếu dữ liệu thì nói
   rõ là thiếu, không đoán.
2. **Không tự cộng tay.** Dùng `meta.totals`, `group_by` và các trường đã tính sẵn ở server.
3. **Ưu tiên theo click có thể giành lại.** Mọi đề xuất đều kèm ước lượng tác động (click/tháng), độ tự
   tin và công sức.
4. **Kết thúc bằng hành động.** Mỗi việc nêu rõ: sửa gì, ở đâu, vì sao, ai làm, đo lại bằng gì và khi nào.
5. **Đúng ngôn ngữ người dùng.** Skill viết bằng tiếng Anh (cho model), trả lời theo ngôn ngữ người hỏi.
6. **Chỉ đọc.** MCP hiện chỉ có quyền đọc. Thay đổi trên site chỉ xảy ra khi bạn yêu cầu skill
   `seodash-implement` sửa code trong repo đang mở.

## Kiến trúc

```
plugins/seo-dashboard/
├─ .mcp.json                 kết nối MCP (OAuth, không token)
├─ skills/
│  ├─ seodash-core/          nền tảng: quy ước dữ liệu, bản đồ tool, chuẩn trình bày
│  ├─ seodash-portfolio/     tổng quan mọi dự án, chọn dự án cần xử lý trước
│  ├─ seodash-diagnose/      truy nguyên nhân tăng/giảm traffic
│  ├─ seodash-opportunities/ cơ hội từ khoá, CTR, striking distance, cannibalization, paid↔organic
│  ├─ seodash-content/       audit & chiến lược nội dung, brief trang mới
│  ├─ seodash-roadmap/       gom phát hiện → backlog ưu tiên → lộ trình 30/60/90 ngày
│  ├─ seodash-implement/     biến đề xuất thành thay đổi code trong repo đang mở
│  ├─ seodash-measure/       đo tác động sau triển khai, nhật ký bài học
│  ├─ seodash-report/        báo cáo tuần/tháng/quý, bản cho khách hàng và bản kỹ thuật
│  └─ seodash-ai-search/     traffic & mức hiện diện trên ChatGPT/Perplexity/Gemini (GEO)
└─ commands/                 lệnh tắt cho Claude Code: /seo-check, /seo-why, /seo-wins, /seo-content,
                             /seo-plan, /seo-implement, /seo-report
```

Mỗi skill gồm `SKILL.md` ngắn: khi nào dùng, các bước làm, khuôn đầu ra. Phần dài (ngưỡng, ma trận
quyết định, template) để ở `references/` và chỉ nạp khi cần, nhằm giữ ngữ cảnh gọn.

## Chi tiết từng skill

### 1. `seodash-core` — nền tảng (đã có, chuyển từ `seo-dashboard-analyst`)
- **Kích hoạt:** mọi câu hỏi về traffic, thứ hạng, từ khoá hay trang của các site trong dashboard.
- **Nội dung:**
  - Chọn property.
  - Quy ước ngày (GSC trễ 2–4 ngày), đơn vị (CTR %, position thấp là tốt), so sánh kỳ.
  - Bẫy dữ liệu: query ẩn danh, mẫu nhỏ, brand filter.
  - Bảng câu hỏi → tool.
  - Chuẩn trình bày.
- **Các skill khác:** đều giả định core đã được nạp.

### 2. `seodash-portfolio` — "dự án nào cần tôi nhất tuần này?"
- **Kích hoạt:** "tổng quan các dự án", "site nào đang có vấn đề", "tuần này nên tập trung vào đâu".
- **Các bước:**
  1. `list_properties`.
  2. Với từng site: `get_seo_findings(days=28)` và `get_overview(compare_mode)` (tuần và tháng).
  3. Chấm điểm sức khoẻ, gồm:
     - xu hướng click;
     - mức độ nghiêm trọng của các finding;
     - số click bị đe doạ;
     - tình trạng dữ liệu (thiếu GA4, property bị `forbidden`).
- **Đầu ra:**
  - Bảng xếp hạng các dự án: trạng thái, 1 dòng lý do, việc tiếp theo.
  - 3 dự án cần xử lý trước.
- **Cần thêm ở MCP (nên làm):** tool `get_portfolio_summary` trả KPI của mọi property trong một lần
  gọi, thay vì N×2 lần gọi.

### 3. `seodash-diagnose` — "vì sao traffic giảm/tăng?"
- **Kích hoạt:** traffic giảm hoặc tăng đột ngột, mất thứ hạng, "chuyện gì xảy ra với site X".
- **Cây quyết định:**
  1. **Xác nhận và định thời điểm.** Dùng trend theo ngày hoặc tuần, tách khỏi mùa vụ (so với cùng kỳ
     năm trước).
  2. **Định vị.** Xem mất ở đâu: `group_by` theo `terms`, `url_folder`, `topic_cluster`; theo thiết bị
     và quốc gia.
  3. **Phân loại.** Mất thứ hạng · mất nhu cầu hoặc hiển thị · mất CTR (SERP feature, title) · mất
     index · cannibalization · đo lường (tracking hoặc filter).
  4. **Tìm nguyên nhân trong cùng khung thời gian.** Google update · content change · annotation ·
     indexing · backlink mất.
  5. **Kết luận** với độ tự tin (cao/vừa/thấp) và cách kiểm chứng.
- **Đầu ra:**
  - Tóm tắt 3 dòng.
  - Dòng thời gian.
  - Bảng "mất ở đâu".
  - Các giả thuyết, xếp theo bằng chứng.
  - Việc cần làm, kèm cách xác nhận giả thuyết.
- **`references/`:** ma trận triệu chứng → nguyên nhân; ngưỡng "đủ lớn để quan tâm"; cách đọc hình dạng
  đường cong (sập một ngày, trượt dần, theo bậc).

### 4. `seodash-opportunities` — "làm gì để có thêm traffic nhanh nhất?"
- **Kích hoạt:** cơ hội, quick wins, tăng traffic, từ khoá nên đẩy.
- **Các nhóm cơ hội, mỗi nhóm có công thức ước lượng click tăng thêm:**
  - **CTR thấp so với vị trí.** So với đường CTR chuẩn theo vị trí, viết lại title và meta (gợi ý cụ
    thể 2–3 phương án).
  - **Striking distance (vị trí 4–15).** Trang nào cần củng cố, bằng nội dung, internal link hoặc
    on-page.
  - **Query mới và đang lên.** Thêm section hay tạo trang mới.
  - **Cannibalization.** Gộp hoặc chia lại; chọn trang chính.
  - **Paid ↔ organic.** Từ khoá đang trả tiền Ads nhưng organic đã top 3 thì có thể giảm bid; từ khoá
    Ads chuyển đổi tốt mà organic yếu là ứng viên SEO.
- **Đầu ra:** backlog cơ hội gồm query, trang, hiện trạng, click dự kiến, công sức, độ tự tin và thay đổi
  cụ thể.
- **`references/`:** bảng CTR chuẩn theo vị trí (có ghi nguồn và giới hạn); công thức ước lượng; mẫu
  viết lại title.

### 5. `seodash-content` — audit & chiến lược nội dung
- **Kích hoạt:** audit nội dung, trang nào nên cập nhật, gộp, xoá; kế hoạch nội dung; brief bài mới.
- **Các bước:**
  - Decay (90 ngày+) · content matrix (star / gem / trap / weak) · pruning · on-page coverage ·
    cannibalization · topic clusters.
  - Mỗi trang nhận **đúng một** hành động: refresh, merge (ghi rõ trang đích), promote, fix on-page,
    prune (301 hoặc noindex), giữ nguyên.
  - Khoảng trống nội dung: query có impression mà chưa có trang phù hợp, gom thành cluster.
  - Brief trang mới: intent, từ khoá chính và phụ (lấy từ GSC), outline, internal link vào và ra, KPI.
- **Đầu ra:**
  - Bảng audit.
  - Top 5 việc cho tuần này.
  - Lịch nội dung 4–8 tuần.
- **Chuyển việc:** schema hay kỹ thuật sang `claude-seo` (`seo-schema`, `seo-technical`) nếu đã cài.

### 6. `seodash-roadmap` — từ phát hiện đến kế hoạch triển khai
- **Kích hoạt:** "lên kế hoạch SEO", "roadmap", "ưu tiên việc gì", hoặc sau diagnose, opportunities,
  content.
- **Các bước:**
  - Gom phát hiện từ các skill khác (hoặc tự chạy `get_seo_findings` cùng opportunities).
  - Chấm **ICE**:
    - Impact = click có thể giành lại;
    - Confidence = độ mạnh bằng chứng;
    - Effort = giờ công / độ khó, phân theo loại việc.
  - Chia thành 3 nhóm: 30 ngày (quick wins), 60 ngày (nội dung), 90 ngày (cấu trúc).
  - Mỗi việc thành một ticket: mô tả · trang hoặc query · tiêu chí xong · cách đo · ngày kiểm tra lại.
- **Đầu ra:** roadmap dạng bảng và danh sách ticket. Có thể xuất markdown để dán vào Notion, Jira hoặc
  GitHub Issues.
- **`references/`:** thang chấm Effort theo loại việc; template ticket.

### 7. `seodash-implement` — triển khai trong repo tự code
- **Kích hoạt:** đang mở repo của chính dự án và yêu cầu "sửa title", "thêm schema", "fix
  canonical/sitemap", "làm theo roadmap".
- **Các bước:**
  1. Nhận diện framework: Next.js (metadata API), Nuxt, Astro, Remix, SvelteKit, Laravel/Blade,
     WordPress theme, static HTML.
  2. Tìm nơi định nghĩa title, meta, canonical, robots, sitemap, hreflang, structured data, internal link
     và redirect.
  3. Đối chiếu đề xuất (từ roadmap hoặc tool) với code. Sửa có kiểm soát: thay đổi nhỏ, theo từng trang,
     giữ nguyên giọng văn.
  4. Kiểm tra bằng build/typecheck và render HTML để xác nhận thẻ đúng.
  5. Ghi danh sách trang đã đổi và ngày deploy để `seodash-measure` đo lại; nhắc tạo annotation trong
     dashboard.
- **`references/`:** bản đồ "đặt SEO ở đâu" cho từng framework; checklist trước khi merge.
- **An toàn:** không đổi URL hay slug khi chưa có kế hoạch redirect; không sửa hàng loạt khi chưa có
  bản xem trước (diff).

### 8. `seodash-measure` — đo tác động và học
- **Kích hoạt:** "thay đổi tuần trước có hiệu quả không", "đo lại", "sau khi cập nhật bài X".
- **Các bước:**
  - `get_annotation_impact` nếu đã có annotation.
  - Nếu không có: so hai khung bằng nhau trước và sau bằng `query_search_analytics`, lọc đúng trang hoặc
    query, có nhóm đối chứng (phần còn lại của site) để loại xu hướng chung.
  - Kết luận: có hiệu quả · chưa đủ dữ liệu (chờ thêm N ngày) · không hiệu quả. Kèm bài học rút ra.
- **Đầu ra:** bảng trước/sau, kết luận, ghi chú để đưa vào lần lập roadmap sau.

### 9. `seodash-report` — báo cáo
- **Kích hoạt:** báo cáo tuần, tháng, quý; báo cáo cho khách hàng hoặc sếp.
- **Hai phiên bản:**
  - **Khách hàng:** ngôn ngữ kinh doanh, ít thuật ngữ, tập trung kết quả và kế hoạch.
  - **Kỹ thuật:** đủ chi tiết để làm việc.
- **Các phần:** tóm tắt · KPI (so kỳ trước và cùng kỳ năm trước) · thắng và thua · nguyên nhân · việc
  đã làm (từ annotation) · kế hoạch tiếp theo.
- **`references/`:** template từng loại báo cáo.

### 10. `seodash-ai-search` — hiện diện trên AI search (GEO)
- **Kích hoạt:** traffic từ ChatGPT/Perplexity, "AI có nhắc đến brand không", tối ưu cho AI Overviews.
- **Các bước:**
  - `get_ai_traffic` (lượt truy cập) và `get_ai_visibility` (mức nhắc đến, trích dẫn, đối thủ, khoảng
    trống).
  - Trang nào được AI dẫn tới và chuyển đổi ra sao.
  - Đề xuất nội dung để được trích dẫn: câu trả lời trực diện, dữ liệu gốc, cấu trúc rõ, entity.
- **Chuyển việc:** `claude-seo` → `seo-geo` cho phần audit kỹ thuật GEO.

## Lệnh tắt (Claude Code)

| Lệnh | Skill | Ví dụ |
|---|---|---|
| `/seo-check` | portfolio | tổng quan mọi dự án |
| `/seo-why [site]` | diagnose | vì sao traffic thay đổi |
| `/seo-wins [site]` | opportunities | quick wins |
| `/seo-content [site]` | content | audit nội dung |
| `/seo-plan [site]` | roadmap | kế hoạch 30/60/90 |
| `/seo-implement` | implement | sửa code theo roadmap trong repo đang mở |
| `/seo-report [site] [week\|month]` | report | báo cáo |

Trên Claude.ai, 6 prompt của MCP đóng vai trò tương đương các lệnh này.

## Phân phối

- **Claude Code:** `/plugin marketplace add vilo0411/seo-dashboard-ai-kit` rồi
  `/plugin install seo-dashboard@seo-dashboard-ai-kit`. Cài một lần là có ở mọi project.
- **Claude.ai (cá nhân hoặc công ty):**
  - GitHub Action đóng gói mỗi skill thành một file `.zip` đính vào Release để upload.
  - Connector thêm bằng URL `…/api/mcp`. Ở gói công ty, admin thêm connector.
- **Cursor và các client khác:** README có cấu hình MCP. Skill dùng như project rule.
- **"Bảo AI cài":** `INSTALL.md` viết sẵn các bước cho agent làm theo.

## Lộ trình xây dựng

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| A | Repo, plugin, MCP OAuth, `seodash-core`, README/INSTALL, Action đóng gói zip | đang làm |
| B | `seodash-diagnose`, `seodash-opportunities`, `seodash-roadmap` + lệnh tắt | tiếp theo |
| C | `seodash-content`, `seodash-report`, `seodash-measure` | |
| D | `seodash-implement`, `seodash-portfolio`, `seodash-ai-search` | |
| E | Bổ sung MCP: `get_portfolio_summary`, quyền ghi annotation (scope `write`) để ghi lại việc đã triển khai | |

## Đánh giá chất lượng

Mỗi skill có một bộ câu hỏi mẫu (tiếng Việt và tiếng Anh) trong `evals/<skill>.md`, kèm tiêu chí:
- gọi đúng tool;
- không tự cộng tay;
- mọi con số đều có mốc so sánh;
- có hành động cụ thể;
- nói rõ giới hạn của phân tích.

Chạy lại bộ câu hỏi này sau mỗi lần sửa skill.
