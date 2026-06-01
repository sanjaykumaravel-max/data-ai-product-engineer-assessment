# Task 1 - Product Scoping

## Objective
Design (not overbuild) an internal tool that answers:
"How is marketing performing across channels right now, and where should we be focusing?"

## Deliverables
- [Product Brief](./product-brief.md)
- [Architecture Diagram](./architecture-diagram.md)
- [Wireframe](./wireframe.md)

## Key Decisions
- Primary v1 user is the internal marketing analyst.
- v1 output must be consistent, fast, and explainable.
- Tool wraps existing workflows and tools rather than replacing them.
- Recommendation logic is deterministic in v1 to build trust.

## V1 Scope
- Unified cross-channel summary for selected date range
- Core KPI calculations: CTR, CVR, CPA, ROAS
- Channel focus guidance: increase, maintain, review
- Exportable summary for internal and client communication

## Out Of Scope (v1)
- Forecasting and predictive models
- Auto-optimization of campaigns
- Full client self-serve portal
- Workflow/tool migration for the team

## Validation Criteria
- New analyst can answer the core question in under 5 minutes.
- Same input produces same output across team members.
- Recommendations can be traced to visible KPI definitions.

## If More Time Was Available
- Role-based views for clients and managers
- Scenario simulation for budget reallocation
- Alerting and anomaly detection
