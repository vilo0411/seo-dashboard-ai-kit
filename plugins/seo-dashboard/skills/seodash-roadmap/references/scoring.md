# ICE scoring

| Impact (clicks/month gained or protected) | Points |
|---|---|
| < 20 | 1 |
| 20–100 | 2 |
| 100–300 | 3 |
| 300–1,000 | 4 |
| > 1,000 | 5 |

Scale the bands to the site: for a site with fewer than 2,000 clicks/month, divide the thresholds by 5.
For lead-gen or e-commerce pages, raise Impact by 1 when GA4 shows the page converting above the site
average.

| Confidence | Points | Typical evidence |
|---|---|---|
| High | 3 | Large sample, known mechanism (CTR gap, de-indexed page, broken redirect) |
| Medium | 2 | Clear data, outcome depends on competitors (striking distance, refresh) |
| Low | 1 | Small sample or speculative (new page, demand bet) |

Effort: use the 1–5 scale from `seodash-opportunities` (title edit = 1 … structural project = 5).

Score = Impact × Confidence ÷ Effort. Ties: prefer protecting traffic, then the shorter task.
