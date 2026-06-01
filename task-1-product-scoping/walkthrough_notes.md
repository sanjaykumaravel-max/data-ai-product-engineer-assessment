# Walkthrough Notes - Task 1 Product Scoping

## Problem
The current process for answering cross-channel performance is manual, inconsistent, and too dependent on individual analysts.

## Why This v1
I prioritized a fast, consistent internal analyst experience over broad feature depth. The goal is repeatable decision support, not a full reporting platform.

## Key Decisions
- Primary user: internal marketing analyst.
- Output: cross-channel KPI summary + clear focus guidance.
- Recommendation logic: deterministic and explainable in v1.
- Constraint respected: wrap around existing tools and current workflow.

## In Scope
- Standardized input metrics from existing channels.
- Unified performance table.
- KPI calculations (CTR, CVR, CPA, ROAS).
- Focus recommendations (increase, maintain, review/reduce).
- Exportable summary for sharing.

## Out Of Scope
- Predictive models and forecasting.
- Campaign auto-optimization.
- Client self-serve portal.
- Tool migration/replacement.

## Tradeoffs
I intentionally chose interpretability over sophistication. This keeps trust high and implementation risk low while solving the immediate business pain.

## What I Would Improve Next
- Role-based views for analysts, managers, and client-facing teams.
- Anomaly alerts and threshold-based notifications.
- Scenario simulation for budget reallocation.
