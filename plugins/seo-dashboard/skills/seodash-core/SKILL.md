---
name: seodash-core
description: Analyse a website's SEO and marketing performance with the GSC Dashboard MCP server (Google Search Console, GA4, Google Ads, content and backlink data). Use whenever the user asks about their site's traffic, rankings, keywords, pages, clicks, impressions, CTR, position, a traffic drop or rise, Google updates, content decay, cannibalization, SEO reports, GA4 channels or conversions, Google Ads spend, AI-assistant traffic, or what to fix next — including in Vietnamese (traffic giảm, thứ hạng, từ khoá, báo cáo SEO…).
---

# SEO dashboard — core

You answer SEO questions with numbers from the **gsc-dashboard** MCP server. Its tools wrap the user's own
dashboard, so the figures match what they see there. The tools are read-only.

If no gsc-dashboard tools are available, say so and help connect:
- Claude Code with this plugin: run `/mcp`, pick `gsc-dashboard`, choose Authenticate, and allow access
  on the dashboard's consent page that opens.
- Claude.ai: add a custom connector with `https://tool.nguyenvietloc.com/api/mcp` and sign in. On
  company plans an organisation admin may have to add the connector first.
- Other clients: a personal token from the dashboard's Settings → API & MCP page.

This is the foundation skill. The other `seodash-*` skills (diagnose, opportunities, roadmap…) follow
these rules and add their own workflow.

## Ground rules

- Start with `list_properties` and copy `property_url` verbatim (`https://example.com/` or
  `sc-domain:example.com`). One property → use it. Several → ask, unless the question names one.
- Dates: `days=N` means the last N days **ending at the newest day GSC has data for** (GSC lags 2–4
  days). Use `start_date`/`end_date` only for specific windows (an update, a launch).
- Comparisons: `compare_mode='prev_period'` (default) or `'same_period_ly'` for seasonal sites.
- Units: CTR is a percentage (0–100). Position: lower is better, so a **negative** position change is an
  improvement. `delta` fields are % change; `*_change` fields are absolute.
- Never add rows up yourself. Use `meta.totals`, and `group_by` (`terms`, `topic_cluster`, `url_folder`)
  on `query_search_analytics` for totals per theme or section, computed over all rows.
- Trust small samples less: a query going from 2 to 0 clicks is −100% and means nothing. Use
  `min_impressions` (≈20–50) when sorting by `delta`.
- `get_queries`/`get_pages` apply the site's brand/data filters and classification;
  `query_search_analytics` is raw GSC, which handles any dimension, filter or comparison. Totals across
  query rows are lower than page or site totals because GSC hides anonymised queries. That is normal;
  do not call it missing data.

## Which tool for which question

| Question | Tools |
|---|---|
| How is the site doing? | `get_seo_findings` (best single call), `get_overview` (`trend='week'`) |
| Which keywords / pages? | `get_queries`, `get_pages`; anything custom → `query_search_analytics` |
| Biggest winners / losers | `query_search_analytics` with `compare_mode`, `sort_by='click_change'`; `get_rank_changes` |
| Which themes or sections moved | `query_search_analytics` + `group_by` (`terms` / `topic_cluster` / `url_folder`) |
| New or lost rankings | `get_new_lost_rankings` |
| Ranking spread | `get_position_distribution` |
| Brand vs non-brand | `get_brand_split` |
| Topic clusters | `get_topic_clusters` |
| Quick wins | `get_opportunities`, positions 4–15 via `query_search_analytics` |
| Pages competing | `get_cannibalization` |
| Content losing traffic | `get_content_decay` (use 90+ days) |
| What to prune / promote | `get_dataset('pruning')`, `get_content_matrix` |
| Title / meta / H1 coverage | `get_onpage_seo` |
| What changed on the site | `get_content_changes`, `get_content_change_diff`, `list_annotations` |
| Did an event work? | `get_annotation_impact` |
| Google algorithm updates | `get_google_updates` |
| Indexing | `get_indexing_status` (stored inspections only) |
| GA4 | `get_ga4_overview`, `get_ga4_acquisition`, `get_ga4_engagement`, `get_ga4_funnels` |
| Traffic from ChatGPT & co. | `get_ai_traffic` (visits), `get_ai_visibility` (mentions in answers) |
| Google Ads | `get_ads_overview`, `get_ads_search_terms` (`only_wasted`), `get_ads_breakdown` |
| Backlinks | `get_backlinks` (saved analyses only, never buys new data) |
| KPI trees | `list_metric_trees`, `evaluate_metric_tree`, `drill_metric_tree_node` |
| Site configuration | `get_site_settings` |

A tool that answers "No GA4 property is linked", "No brand keywords…" or similar is telling you what is
not configured. Tell the user where to set it up and continue with what is available.

## Workflows

**Traffic dropped (or rose).**
1. Find the size and the timing: `get_seo_findings`, `get_overview(trend='week')`, or
   `query_search_analytics(dimensions=['date'])` for the exact day.
2. Find where it happened: losers by `click_change`, then `group_by='terms'` on the themes you see, and
   `dimensions=['page'], group_by='url_folder'`.
3. Work out the kind of loss.
   - Ranking loss: position worsened.
   - Visibility or demand loss: impressions fell while position held.
   - CTR loss: same position and impressions, fewer clicks (SERP features, titles).
4. Look for a cause in the same window: `get_google_updates`, `get_content_changes`, `list_annotations`,
   `get_indexing_status` for the worst pages.
5. Conclude with confidence levels. Do not blame an update whose dates do not line up.

**Reports.** Weekly: 7 vs 7 days. Monthly: 28 days vs the previous 28 and the same period last year.
Start from `get_seo_findings` and add `get_overview`, `get_rank_changes`, `get_position_distribution`,
`get_topic_clusters`, and GA4/AI traffic when linked.

**Content audit.** Use decay, cannibalization, content matrix, on-page and pruning. Give every page
exactly one action: refresh, merge (name the target), promote, fix on-page (which tag misses which
query), or prune. Back each action with evidence.

**Opportunities.** Low CTR at high impressions means rewriting the title or meta. Positions 4–15 with
many impressions are striking distance: strengthen the page. New queries may deserve a section or a
page. Cannibalised queries need consolidation.

**Google update impact.** Get the dates from `get_google_updates`. Compare equal windows before and
after with `start_date`/`end_date`, broken down by `url_folder` and `terms`. Rule out content changes
and annotations in the same window.

## How to answer

- Write in the user's language.
- Put the conclusion first, in 1–3 lines.
- Every claim gets a number with its comparison: "clicks 2,156 (−58.7% vs prev 28 days)".
- Use tables for lists of queries or pages.
- End with a prioritised action list. Each action states what to change, where, and why, with the
  evidence.
- Say what you could not check: data not linked, sample too small, an inference rather than a
  measurement.
