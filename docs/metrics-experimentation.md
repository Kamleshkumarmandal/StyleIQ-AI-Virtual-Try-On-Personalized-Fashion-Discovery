# StyleIQ Metrics & Experimentation

**Status:** Proposed measurement plan. No product outcomes are claimed.

## North Star

**Kept purchases per 100 eligible shoppers.**

A kept purchase is an order that has not been returned within the defined observation window. The exact window and order attribution must be defined before analysis.

## Funnel

1. Eligible product-detail-page visitor
2. Avatar flow started
3. Avatar flow completed
4. Try-on started
5. Try-on completed
6. Fit guidance viewed (if available)
7. Size selected
8. Add to cart
9. Purchase completed
10. Purchase kept / returned

## Supporting metrics

| Metric | Definition concept |
|---|---|
| Avatar completion rate | Completed avatar profiles / avatar starts |
| Try-on success rate | Usable previews / generation attempts |
| Try-on completion rate | Completed previews viewed / try-on starts |
| Time to preview | Time from generation request to usable preview |
| Add-to-cart rate | Add-to-cart events / eligible product viewers |
| Purchase conversion | Orders / eligible shoppers |
| Fit-related return rate | Fit-related returned items / purchased items |
| Try-on cost | Inference and storage cost / completed previews |
| Trust score | Post-preview user-reported usefulness/confidence |

## Guardrails

- Page load and interaction latency
- Preview failure rate
- Customer complaints about inaccurate images
- Misleading fit recommendation rate
- Product availability accuracy
- Refund and exchange satisfaction
- Privacy complaints and deletion completion
- GPU cost per completed preview

## Experiment A — Visual try-on

Control: standard product imagery.  
Variant: standard imagery plus virtual try-on.

Primary measures: preview usefulness, add-to-cart, purchase conversion.  
Guardrails: latency, failure rate, trust, and cost.

## Experiment B — Avatar onboarding

Compare measurement-based and photo-based paths. Measure:
- Completion
- Time to complete
- Drop-off step
- Perceived privacy comfort
- Preview usefulness
- Support requests

Do not force photo upload to improve completion metrics.

## Experiment C — Fit guidance

Control: standard size chart.  
Variant: measurement comparison with explanation.

Primary measures: fit confidence and kept purchases.  
Guardrails: conversion, exchange/return complaints, recommendation uncertainty, and missing-data rate.

## Experiment integrity

- Randomize at the appropriate user/session level.
- Define eligible population and exclusion criteria.
- Determine sample size and duration before launch.
- Account for return observation delay.
- Avoid interpreting click-through uplift as proof of business impact.
- Separate real customer outcomes from synthetic test data.
- Report confidence intervals and limitations.
