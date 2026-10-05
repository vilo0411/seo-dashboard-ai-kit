# Symptoms, causes, responses

## Shapes (daily clicks)

| Shape | Usually means |
|---|---|
| Cliff: one day, −30% or more, stays down | Deploy or migration (noindex, robots, redirects, canonical), manual action, property or tracking change |
| Steps over 1–2 weeks | Core or spam update rollout (check `get_google_updates`), large content change |
| Slow slide over months | Content decay, competitors, shrinking demand, SERP features taking clicks |
| Spike then back to normal | News, a viral mention, a one-off campaign: not an SEO change |
| Weekly sawtooth | Normal weekday pattern: compare full weeks, never partial ones |

## Matrix (per losing group)

| Impressions | Position | CTR | Likely cause | Next check |
|---|---|---|---|---|
| ↓ big | worse (+3 or more) | ~ | Ranking loss: update, competitor, content or technical regression | Updates, content changes, indexing |
| ↓ | ~ flat | ~ | Demand fell (seasonal or trend) or a SERP layout change | Same period last year; ask about Google Trends |
| ~ | ~ | ↓ | CTR loss: SERP features (AI Overview, ads, snippets), weaker title vs competitors | Title/meta changes, `get_onpage_seo` |
| ↓ to 0 for some pages | — | — | De-indexed, 404/5xx, noindex, canonical to another URL | `get_indexing_status`, content changes (status) |
| query ↓ on page A, ↑ on page B | ~ | ~ | Cannibalization or intended consolidation | `get_cannibalization` |
| all ↓ evenly, all sections | ~ | ~ | Site-wide: update, manual action, tracking or property change | Updates, annotations, data freshness |
| ↓ on one device or country | | | Mobile usability or rendering, hreflang/geo targeting | `dimensions=['device'/'country']` |

## Responses

- **Ranking loss after a core update.** Content quality and intent review of the losing pages against
  the pages now ranking; no quick technical fix. Measure after the next core update.
- **Ranking loss after a deploy.** Diff the changes (`get_content_change_diff`); restore titles,
  content, internal links and canonical; request recrawl.
- **De-indexing.** Fix status, noindex, canonical and robots; check the sitemap; inspect URLs in GSC.
- **CTR loss.** Rewrite titles and meta for the intent; add structured data where eligible.
- **Cannibalization.** Choose one primary page; merge and 301 the rest, or differentiate their intent.
- **Demand loss.** No SEO fix. Shift effort to growing topics (`seodash-opportunities`).
