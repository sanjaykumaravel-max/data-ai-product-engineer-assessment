# V1 Scope Definition - Internal Marketing Analytics Dashboard

## Scope Goal
Deliver a simple internal dashboard that helps analysts answer: "How are channels performing right now, and where should we focus next?" without manual multi-tool reporting.

## In-Scope Features (v1)
- Cross-channel performance table for a selected date range.
- Standard KPI calculations: Spend, Impressions, Clicks, Conversions, Revenue, CTR, CVR, CPA, ROAS.
- Basic channel prioritization labels: Increase, Maintain, Review/Reduce.
- Data freshness visibility (last successful sync timestamp).
- Exportable output (CSV or copy-ready summary).
- Consistent metric definitions documented in-product.

## Out-of-Scope Features (v1)
- Predictive forecasting or budget optimization recommendations.
- Automated campaign changes (bids, budgets, targeting).
- Advanced attribution modeling (multi-touch custom models).
- Client-facing self-serve portal and permissions model.
- Real-time streaming updates.
- Full anomaly detection and alerting system.

## Technical Limitations (v1)
- Dependent on source system data quality and refresh cadence.
- Batch-oriented refresh (for example hourly/daily), not real-time.
- Rule-based recommendation logic, not ML-driven scoring.
- Limited historical backfill at launch to reduce implementation risk.
- Minimal role handling (internal analyst usage only).

## Trade-Offs
- Explainability over sophistication: deterministic rules are easier to trust and audit.
- Speed of delivery over feature breadth: smaller feature set ensures stable adoption.
- Consistency over customization: fixed KPI schema avoids analyst-to-analyst variance.
- Integration over replacement: preserve existing tools to reduce workflow disruption.

## Why Features Were Excluded
- Forecasting and optimization were excluded to avoid low-trust outputs without deeper data governance.
- Automation actions were excluded to prevent operational risk in v1.
- Client portal was excluded because primary value is internal analyst efficiency first.
- Real-time and anomaly systems were excluded due to complexity and higher infrastructure/monitoring overhead.
- Advanced attribution was excluded because it requires broader instrumentation alignment before reliable use.

## Practical v1 Outcome
A reliable internal dashboard that cuts manual reporting effort, standardizes cross-channel analysis, and enables faster, repeatable decision support.
