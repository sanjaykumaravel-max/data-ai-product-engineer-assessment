# Task 1 Architecture Diagram

## System Flow (v1)

```mermaid
flowchart LR
    A[Analyst selects date range and filters] --> B[Tool UI]
    B --> C[Connector Layer]
    C --> D1[Ad Platform Data]
    C --> D2[Web Analytics Data]
    C --> D3[CRM/Conversion Data]

    D1 --> E[Normalization + Metric Mapping]
    D2 --> E
    D3 --> E

    E --> F[Unified Performance Table]
    F --> G[KPI Engine: CTR CVR CPA ROAS]
    G --> H[Recommendation Rules]
    H --> I[Summary View + Focus Guidance]
    I --> J[CSV/Shareable Export]

    F --> K[Audit Metadata: source and sync time]
    K --> I
```

## Architecture Notes
- The design wraps existing tools instead of replacing them.
- A lightweight normalization layer standardizes metric names and types.
- Recommendation logic is deterministic in v1 for explainability.
- Audit metadata improves trust and debugging.
