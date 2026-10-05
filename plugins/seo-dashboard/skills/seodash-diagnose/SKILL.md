---
name: seodash-diagnose
description: Root-cause analysis of an organic search traffic change using the GSC Dashboard MCP tools — why clicks, impressions or rankings dropped or rose, when it started, which queries/pages/sections lost it, and what caused it (Google update, site change, indexing, cannibalization, demand, CTR). Use for "traffic dropped", "lost rankings", "what happened to my site", "vì sao traffic giảm", "tụt hạng", "mất traffic".
---

# Diagnose a traffic change

Follow `seodash-core` rules (property, dates, units, no manual sums). Work through the steps in order and
stop going deeper once a cause explains the change with high confidence.

## 1. Confirm the change and date it

- `get_overview(days=56, trend='week')` and `get_seo_findings(days=28)`: size, direction, which KPIs moved.
- `query_search_analytics(dimensions=['date'], days=90)`: find the break day. Classify the shape using
  `references/symptoms.md` → "Shapes".
- Seasonal site? Repeat with `compare_mode='same_period_ly'`. If last year shows the same dip, say so and stop.
- Too small to matter? Under ~10% change or under ~50 clicks/week counts as noise. Say that rather than
  inventing a cause.

## 2. Locate it

Use the same window before vs after the break (`start_date`/`end_date`, equal lengths), with
`compare_mode='prev_period'` and `sort_by='click_change', sort_dir='asc'`:

| Cut | Call |
|---|---|
| Themes | `query_search_analytics(dimensions=['query'], group_by='terms', group_terms=[…])`, terms taken from the top losers |
| Sections | `query_search_analytics(dimensions=['page'], group_by='url_folder')` |
| Clusters | `group_by='topic_cluster'` (if the site has clusters) or `get_topic_clusters` |
| Device | `dimensions=['device']` |
| Country | `dimensions=['country']` |
| Brand | `get_brand_split` (if brand keywords are set) |

State what share of the total loss the top 1–3 groups explain, for example "/reading/ explains 82% of
the loss".

## 3. Classify the loss

For the groups that explain the loss, read impressions, position and CTR together. Use the matrix in
`references/symptoms.md`:

- Ranking loss: position worsened.
- Visibility or demand loss: impressions fell, position held.
- CTR loss: position and impressions held, clicks fell.
- Index loss: pages disappeared entirely.
- Cannibalization: the query moved to another page of the site.
- Measurement: brand or data filters, or a property change.

## 4. Find the cause in the same window

- `get_google_updates`: does a rollout overlap the break day? Overlap is necessary, not sufficient.
- `get_content_changes(since_days=…)` on the losing pages, then `get_content_change_diff` for the
  suspicious ones (titles, removed sections, noindex, status changes).
- `list_annotations`: deploys, migrations, campaigns the team logged.
- `get_indexing_status`: the losing pages' verdict and coverage state.
- `get_cannibalization(days=90)`: for losing queries that now show several pages.
- `get_backlinks`: only if a ranking loss is site-wide and nothing else fits.

## 5. Conclude

Rank hypotheses by evidence. Each gets:
- a confidence level (high / medium / low);
- the evidence for it;
- the evidence against it;
- one check that would confirm or refute it.

Never blame an update whose dates do not line up with the break.

## Output

1. **Verdict** (2–3 lines): what changed, by how much, since when, most likely cause.
2. **Timeline**: weekly clicks/impressions around the break, plus updates, changes and annotations on
   the same axis.
3. **Where**: table of the groups explaining the loss, with clicks before → after, change, and share
   of the total.
4. **Why**: ranked hypotheses as above.
5. **What to do**: actions per cause (see `references/symptoms.md` → "Responses"), each with how to
   verify it worked.
   - If several actions are needed, hand off to `seodash-roadmap`.
   - If the fix is in a code repo the user has open, hand off to `seodash-implement`.
