# Task 1 Product Brief

## 1) Problem Statement
The team currently answers cross-channel performance questions through manual effort across multiple tools. The process is slow, inconsistent across team members, and not resilient when key analysts are unavailable.

## 2) Core Question
How is marketing performing across channels right now, and where should the team focus next?

## 3) Product Objective
Design an internal tool that produces a consistent, fast, and explainable cross-channel performance view for decision-making.

## 4) Primary User (v1)
Internal marketing analyst.

## 5) Secondary Users (v1)
- Marketing manager (consumes summary output)
- Client success lead (uses exported summary for client communication)

## 6) Success Criteria (v1)
- User gets an answer in under 5 minutes.
- Output is consistent across users for the same inputs.
- Recommendations are explainable and tied to transparent KPI logic.

## 7) V1 Scope
- Pull standardized channel metrics from existing tools/workflows.
- Normalize data into a single cross-channel table.
- Compute core KPIs: CTR, CVR, CPA, ROAS.
- Surface channel ranking and simple focus guidance (increase/maintain/review).
- Provide a shareable summary view and CSV export.

## 8) Explicitly Out Of Scope (v1)
- Forecasting and predictive modeling.
- Campaign auto-optimization.
- Full client-facing portal.
- Replacing source tools or forcing workflow change.

## 9) Input Data Requirements
- Date range
- Channel/source
- Spend
- Impressions
- Clicks
- Conversions
- Revenue

## 10) Decision Logic (Simple and Explainable)
- High ROAS + scalable volume: increase focus.
- High spend + weak CVR/ROAS: investigate and reduce focus.
- Low data volume: mark as insufficient signal instead of forcing a recommendation.

## 11) Risks and Mitigations
- Inconsistent source definitions
  - Mitigation: shared metric dictionary and mapping layer.
- Trust concerns
  - Mitigation: show formula definitions and source timestamps.
- Data freshness gaps
  - Mitigation: visible last-sync indicator and stale-data warning.

## 12) What To Revisit Later
- Role-based client views
- Budget reallocation simulation
- Alerting and anomaly detection
