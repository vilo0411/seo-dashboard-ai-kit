---
name: seodash-opportunities
description: Find the fastest ways to grow organic traffic for a site from its real GSC Dashboard data — low-CTR queries to rewrite, striking-distance keywords (positions 4-15), new and rising queries, cannibalization to fix, and paid-vs-organic overlaps — each with an estimated click gain, effort and the concrete change. Use for "quick wins", "opportunities", "how to get more traffic", "which keywords to push", "cơ hội SEO", "từ khoá nên đẩy", "tăng traffic".
---

# Find opportunities

Follow `seodash-core` rules. Use `days=28` unless the user says otherwise (90 for small sites, where
28 days holds fewer than ~1,000 clicks). Every opportunity gets an **estimated monthly click gain**,
computed as in `references/estimates.md`. Gains are estimates; say so once, not on every line.

## Sources

1. **Low CTR for the position.** Rewrite title and meta.
   - `get_opportunities(limit=50)`, then `query_search_analytics(dimensions=['query','page'],
     query_match='equals', query_value=<query>)` for the page behind each query.
   - Keep queries whose CTR is well under the benchmark for their position (`references/estimates.md`)
     and that have at least ~100 impressions per month.
   - For each, write two or three concrete title/meta proposals matched to the query intent. Check the
     current title with `get_onpage_seo` when the page is among the top pages.
2. **Striking distance (positions 4–15).** Strengthen an existing page.
   - `query_search_analytics(dimensions=['query','page'], sort_by='impressions', limit=200)`, keeping
     position 4–15.
   - Group by page: one page often owns several such queries, so improving it lifts them all. Use
     `group_by='url_folder'` only for an overview.
   - Fixes, in order of effort:
     1. Put the query in the title or H1 (`get_onpage_seo`).
     2. Add a section answering it.
     3. Add internal links from strong pages with relevant anchors.
     4. Refresh the content.
3. **New and rising queries.** Expand, or create a page.
   - `get_new_lost_rankings` (bucket `new_query`).
   - `query_search_analytics(dimensions=['query'], compare_mode='prev_period', sort_by='click_change')`.
   - If the query has impressions but no page targets it (it lands on a generic page), propose a section
     or a new page. A full brief is `seodash-content`'s job.
4. **Cannibalization.** Unblock a ranking.
   - `get_cannibalization(days=90)`, starting with high severity and many clicks.
   - Choose the primary page (most clicks, best intent fit). Merge and 301, re-target, or de-optimise the
     others.
5. **Paid ↔ organic** (only if Google Ads is linked).
   - `get_ads_search_terms(sort_by='cost')` crossed with organic positions from
     `query_search_analytics(dimensions=['query'], query_match='regex', query_value='term1|term2…')`.
   - Paying for terms already ranking 1–3 organically: test lowering the bid.
   - Terms that convert in Ads but rank poorly organically: SEO targets with proven value.
   - `get_ads_search_terms(only_wasted=true)`: negative-keyword candidates, which also tells you the
     intent to avoid in content.
6. **AI search** (only if GA4 is linked): `get_ai_traffic`. Pages that AI assistants send visitors to
   are worth strengthening; for a deeper look use `seodash-ai-search`.

## Prioritise

Score each opportunity as gain × confidence ÷ effort (scales in `references/estimates.md`). Merge
duplicates: when the same page appears in several sources, list it once with all its queries.

## Output

1. **Summary**: total estimated gain across the top 10, and which source dominates.
2. **Top opportunities**: table with columns # · type · query/queries · page · now (position, CTR,
   impressions) · change to make · estimated clicks per month · effort · confidence.
3. **Details** for the top 5: the exact proposed title/meta, or section outline, or merge target and
   redirect.
4. **Next step**: hand off to `seodash-roadmap` to schedule it, or to `seodash-implement` if the site's
   code is open.
