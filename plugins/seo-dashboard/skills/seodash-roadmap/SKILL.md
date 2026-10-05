---
name: seodash-roadmap
description: Turn SEO findings for a site into a prioritised implementation plan — an ICE-scored backlog, a 30/60/90-day roadmap and ready-to-file tickets with acceptance criteria and a measurement plan — from GSC Dashboard data or from a diagnosis/opportunity analysis already in the conversation. Use for "SEO plan", "roadmap", "what should we do first", "prioritise", "kế hoạch SEO", "lộ trình", "ưu tiên việc gì".
---

# Build an SEO roadmap

Follow `seodash-core` rules. A roadmap is only as good as its inputs. Reuse findings already in the
conversation (from `seodash-diagnose` or `seodash-opportunities`); otherwise collect them.

## 1. Collect findings (skip what is already known)

- `get_seo_findings(days=28)`: rule-based issues ranked by clicks at stake.
- The opportunity sources from `seodash-opportunities`: low CTR, striking distance, new queries,
  cannibalization.
- `get_content_decay(days=90)`, `get_dataset('pruning')`: content to refresh, merge or prune.
- `get_onpage_seo(only_issues=true)`: on-page gaps on the top pages.
- If a recent drop is unexplained, run the `seodash-diagnose` steps first. A roadmap that ignores an
  active loss is wrong.

## 2. Turn findings into backlog items

- **One item = one change a person can do and finish.** "Improve content" is not an item; "Rewrite the
  title and H1 of /reading/five-cards-tarot for 'tarot online 5 lá'" is.
- **Merge** items that touch the same page.
- **Split** items longer than a few days.
- Each item needs: what · where (pages/queries) · why (the evidence, with numbers) · the type of work.

## 3. Score with ICE (`references/scoring.md`)

- **Impact**: estimated monthly clicks gained or protected, using `seodash-opportunities` estimates.
  For conversion-heavy pages, weigh conversions (GA4) over clicks.
- **Confidence**: evidence strength, 1–3.
- **Effort**: 1–5, per the scale.

Score = Impact × Confidence ÷ Effort. Protecting existing traffic (fixing a loss) beats chasing new
traffic when the scores are close.

## 4. Schedule 30 / 60 / 90 days

- **30 days**: effort 1–2 with high or medium confidence, fixes for active losses, and anything blocking
  other work (indexing, redirects).
- **60 days**: content work (refreshes, merges, new sections), effort 3.
- **90 days**: new pages or clusters, and structural or technical projects, effort 4–5.
- Respect dependencies: merge before you redirect, decide the primary page before you de-optimise the
  others.
- Assume roughly 1 day of SEO work per week unless the user states their capacity. Ask once if it
  changes the plan a lot.

## 5. Write tickets (`references/ticket.md`)

Each ticket gets acceptance criteria and a **measurement plan**:
- the metric;
- the page/query filter to use in `query_search_analytics`;
- the baseline value now;
- the check date: about 4 weeks after deploy for on-page changes, 8–12 weeks for content.

Remind the user to log an annotation in the dashboard when it ships, so `seodash-measure` and
`get_annotation_impact` can evaluate it.

## Output

1. **Plan summary**: expected impact of the 30-day block, and the three things to start this week.
2. **Backlog table**: # · item · pages/queries · evidence · impact (clicks/month) · C · E · score ·
   window.
3. **Roadmap**: 30 / 60 / 90 lists in order.
4. **Tickets**: for the 30-day items, in the template. Offer the rest on request.
5. **Risks and open questions**: missing data, assumptions made, decisions the user must take.

When the user wants the tickets elsewhere, format them as GitHub Issues, Jira or Notion markdown. If the
user has the site's code open, offer `seodash-implement` for the 30-day items.
