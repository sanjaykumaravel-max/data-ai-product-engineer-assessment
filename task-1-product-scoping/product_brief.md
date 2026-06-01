# Task 1 Product Brief

## Problem Statement
The marketing team currently answers cross-channel performance questions by manually pulling data from multiple tools. This makes reporting slow, inconsistent across team members, and overly dependent on individual analysts.

## Primary User
Internal marketing analyst (v1).

## User Pain Points
- Data is spread across tools and must be manually stitched.
- Output format changes depending on who prepares it.
- Turnaround time is too slow for regular decision-making.
- If a key analyst is unavailable, requests are delayed.

## Proposed Solution
A lightweight internal decision-support tool that consolidates channel metrics, computes standard KPIs, and returns clear focus guidance in a consistent format. The tool wraps around current tools and workflows rather than replacing them.

## v1 Features
- Date-range based cross-channel performance summary.
- Normalized metrics table across channels.
- KPI calculations: CTR, CVR, CPA, ROAS.
- Simple and explainable focus guidance (increase, maintain, review/reduce).
- Shareable summary and CSV export.
- Visible data freshness indicator (last sync timestamp).

## Out-of-Scope Features
- Forecasting and predictive modeling.
- Campaign auto-optimization.
- Full client self-serve portal.
- Replacing source tools or changing team workflows.
- Advanced anomaly detection in v1.

## Data Sources
- Ad platform exports/APIs (spend, impressions, clicks).
- Web analytics data (sessions, engagement/conversion context).
- CRM or conversion system data (conversions, revenue).
- User-selected filters (date range, brand, region/channel).

## Success Metrics
- Analyst can answer the core question in under 5 minutes.
- Same inputs produce consistent outputs across users.
- Recommendation statements are traceable to KPI definitions.
- Reduced manual reporting effort for recurring performance requests.

## Risks & Constraints
- Constraint: team will not change existing tools/workflows.
- Risk: inconsistent metric definitions across sources.
  - Mitigation: shared metric mapping and definitions.
- Risk: low trust in automated recommendations.
  - Mitigation: deterministic rules and formula transparency.
- Risk: stale or delayed source data.
  - Mitigation: sync timestamp and stale-data warning.
