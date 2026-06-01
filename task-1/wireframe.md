# Task 1 Wireframe (Low Fidelity)

## Main Screen (Analyst View)

```text
+--------------------------------------------------------------------------------+
| Channel Performance Assistant                                                   |
| Date Range: [Last 7 Days v]   Brand: [All v]   Region: [All v]  [Refresh]     |
+--------------------------------------------------------------------------------+
| Last Sync: 2026-06-01 09:15 UTC     Data Health: Good                          |
+--------------------------------------------------------------------------------+
| KPI Summary                                                                     |
| Spend: $120,000 | Revenue: $310,000 | ROAS: 2.58 | CTR: 1.9% | CVR: 3.2%      |
+--------------------------------------------------------------------------------+
| Channel Table                                                                    |
| Channel   Spend    Clicks   Conv   CTR    CVR    CPA     ROAS    Focus         |
| Search    45,000   52,000   1,900  2.4%   3.6%   23.68   3.20    Increase      |
| Social    40,000   41,000   1,000  1.8%   2.4%   40.00   1.75    Review        |
| Display   35,000   29,000     580  1.1%   2.0%   60.34   1.05    Reduce        |
+--------------------------------------------------------------------------------+
| Recommendation Notes                                                             |
| - Increase Search: strongest ROAS with scalable conversion volume.             |
| - Review Social targeting: mid-volume, sub-target CVR.                         |
| - Reduce Display spend: low ROAS and high CPA relative to benchmark.           |
+--------------------------------------------------------------------------------+
| [Export CSV] [Copy Summary]                                                     |
+--------------------------------------------------------------------------------+
```

## Interaction Flow
1. Analyst selects filters and refreshes data.
2. Tool normalizes and computes KPIs.
3. Tool displays ranked channel performance plus focus guidance.
4. Analyst exports summary for stakeholders.
