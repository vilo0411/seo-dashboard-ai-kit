# Estimating gains

## Benchmark CTR by position (desktop+mobile blend, non-brand)

Approximate industry averages; real CTR varies with SERP features, brand, intent and device. Treat them
as a yardstick, not a promise. When the site has enough data, prefer its own CTR at each position
(compare its queries at similar positions) and say which you used.

| Position | CTR % |
|---|---|
| 1 | 28 |
| 2 | 15 |
| 3 | 10 |
| 4 | 7 |
| 5 | 5 |
| 6 | 4 |
| 7 | 3 |
| 8 | 2.5 |
| 9 | 2 |
| 10 | 1.8 |
| 11–15 | 1 |
| 16–20 | 0.7 |

Branded queries routinely exceed these; exclude them from CTR-gap opportunities.

## Formulas (monthly = 28-day window)

- **CTR gap.** `impressions × (benchmark CTR at current position − current CTR)`, counting only when
  current CTR is below 60% of the benchmark. Assume you close half the gap, so multiply by 0.5.
- **Striking distance.** `impressions × (CTR at target position − current CTR)`. Target position 3 when
  current is 4–6; 5 when current is 7–10; 8 when 11–15. Multiply by 0.5 for uncertainty.
- **New query / new page.** Rarely estimable. Use `current impressions × 0.05` as a floor, mark it
  "low confidence", and rank by impressions trend instead.
- **Cannibalization.** `clicks lost by the secondary pages + 30% of the primary page's clicks`, as a
  rough upside of consolidation. Medium confidence at best.

## Scales

| Effort | Meaning |
|---|---|
| 1 | Edit a title/meta or add internal links (minutes) |
| 2 | Add a section, or an on-page fix across a few pages (hours) |
| 3 | Rewrite or merge a page, with redirects (a day) |
| 4 | New page or content cluster (days) |
| 5 | Structural or technical project (weeks) |

| Confidence | Meaning |
|---|---|
| High | Strong data (≥ ~500 impressions per month) and a known mechanism (CTR, title) |
| Medium | Enough data, outcome depends on competition |
| Low | Little data or speculative (new pages, demand) |
