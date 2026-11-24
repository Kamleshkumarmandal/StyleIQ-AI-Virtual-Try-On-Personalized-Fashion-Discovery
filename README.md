# StyleIQ — AI Virtual Try-On & Personalized Fashion Discovery

**See it. Try it. Trust the fit.**

StyleIQ is a product concept and in-progress portfolio project exploring how fashion e-commerce can reduce purchase uncertainty through personalized product discovery, AI-powered virtual try-on, and measurement-based fit guidance.

<img width="1273" height="717" alt="image" src="https://github.com/user-attachments/assets/32ab8289-ca49-4de4-b7a6-ca4cfcb11ba6" />



> **Project status:** Product definition and technical planning. The repository currently documents the intended product and MVP. Virtual try-on, avatar generation, fit prediction, video generation, and commerce integrations are planned—not yet implemented.

## The problem

When shopping for clothing online, customers cannot physically try a garment before purchase. Product images and generic size charts may not answer three different questions:

1. **Appearance:** How might this garment look on a representation of me?
2. **Fit:** Do the garment's actual measurements make this size a plausible fit?
3. **Availability:** Can I purchase the recommended size for my location?

StyleIQ treats these as related but separate product problems.

## Product vision

Build a customer-centered fashion shopping experience that lets shoppers:
- Discover fashion based on style preferences, category, occasion, and budget.
- Create a personal avatar using either manually entered measurements or an optional photo.
- Preview selected garments on the avatar through a virtual try-on experience.
- Receive transparent, measurement-based size guidance when reliable garment data is available.
- Check size availability and add the selected item to a cart.
- Control, review, and delete personal avatar data.

## Two avatar creation paths

### 1. Measurement-based avatar
A privacy-first path that does not require a photo.
- Enter height and relevant body measurements.
- Select body-proportion and appearance preferences for the visual avatar.
- Review and adjust the avatar.
- Use confirmed measurements as inputs to fit guidance.

### 2. Photo-based avatar
An optional path for a more personalized visual preview.
- Review a plain-language explanation and give explicit consent.
- Upload a suitable full-body photo.
- Validate image quality and supported pose.
- Generate a visual representation for try-on.
- Review, retry, or delete the source photo and generated assets.

A single photo cannot reliably reveal hidden body dimensions. Photo-derived visual estimates must not be presented as precise measurements. Customers should confirm measurements before receiving fit guidance.

## Core product principle: visual try-on is not fit prediction

StyleIQ separates two engines:

| Capability | Purpose | Evidence required |
|---|---|---|
| Virtual try-on | Visualize how a garment may appear on an avatar | Person/avatar image, garment image, compatible category |
| Fit intelligence | Estimate whether a size is likely to fit | Confirmed body measurements, garment measurements, fit metadata |

A convincing generated image is not proof of physical fit. If body or garment measurements are missing, StyleIQ should show the standard size chart or explain that it cannot make a reliable recommendation.

## Initial MVP scope

1. Product detail page with a **Try it on me** entry point.
2. Measurement-based avatar creation.
3. Optional photo-based avatar creation with explicit consent.
4. Static virtual try-on image for a limited set of supported tops and dresses.
5. Basic, explainable fit guidance using confirmed body and garment measurements.
6. Product size availability and add-to-cart flow.
7. User controls for viewing and deleting avatar data.
8. Instrumented events for product and usability evaluation.

Short animated previews, 360-degree movement, advanced outfit recommendations, learned fit models, and broad catalog coverage are later milestones.

## Product success measures

**Proposed North Star Metric:** kept purchases per 100 eligible shoppers.

Supporting measures:
- Avatar creation completion rate
- Try-on generation success and completion rates
- Time to usable preview
- Try-on adoption among eligible product-page visitors
- Add-to-cart and purchase conversion
- Fit-related exchange and return rate
- Customer-reported confidence and trust
- Cost per completed try-on
- Photo deletion completion and privacy-request handling

These are proposed product metrics, not measured outcomes. The project will not claim conversion or return improvements without a properly designed experiment and sufficient follow-up data.

## Product principles

- **Customer agency:** photo upload is optional; measurement-only use remains available.
- **Honest AI:** generated previews are labeled as AI visualizations.
- **Separate appearance from fit:** visual similarity does not establish garment fit.
- **Explainability:** size recommendations show the measurements and limitations behind them.
- **Privacy by design:** collect only what is needed, use data only for disclosed purposes, and provide deletion controls.
- **Progressive delivery:** validate a static image experience before investing in video generation.
- **Evidence-led roadmap:** prioritize from customer research, usability testing, and measurable outcomes.

## Proposed architecture

| Layer | Proposed technology | Responsibility |
|---|---|---|
| Web application | Next.js, React, TypeScript | Discovery, product detail, avatar setup, cart |
| API | Python, FastAPI, Pydantic | Authentication, orchestration, catalog, fit guidance |
| Database | PostgreSQL | Profiles, consent records, catalog metadata, events |
| Avatar service | Parametric 3D representation | Measurement-based avatar |
| Photo processing | OpenCV and validated pose/segmentation components | Input validation and visual preprocessing |
| Try-on adapter | Licensed model or commercial API | Garment visualization |
| Fit service | Python measurement rules initially | Explainable size guidance |
| Background jobs | Redis + Celery (proposed) | GPU tasks and asynchronous generation |
| Object storage | Private S3-compatible storage | Temporary source and generated assets |
| Deployment | Docker and cloud GPU worker | Reproducible development and inference |

The virtual try-on implementation must use models, weights, dependencies, and APIs with terms that permit the intended use. Research-code availability does not imply commercial-use permission. Model selection and licence review are required before integration.

## Privacy and safety

StyleIQ may process personal photos and body measurements. The implementation must include:
- Separate, explicit consent for photo processing.
- A measurement-only alternative.
- Clear purpose and retention disclosures.
- Encryption in transit and at rest.
- Private object storage and short-lived access links.
- No raw photos or body measurements in analytics events.
- No use of customer photos for model training without separate opt-in.
- User-accessible deletion controls for source photos and generated assets.
- Retention and deletion checks for external AI providers.
- Access controls, audit logs, upload validation, and incident procedures.
- Legal review of applicable privacy and consumer-protection requirements before public launch.

## Repository documentation

- [Product Requirements Document](docs/product-requirements.md)
- [User Research Plan](docs/user-research.md)
- [Competitor Analysis Framework](docs/competitor-analysis.md)
- [Customer Journey](docs/user-journey.md)
- [AI Architecture](docs/ai-architecture.md)
- [Privacy & Security](docs/privacy-and-security.md)
- [Product Roadmap](docs/product-roadmap.md)
- [Metrics & Experimentation](docs/metrics-experimentation.md)

## Proposed repository structure

```text
StyleIQ/
├── README.md
├── docs/
│   ├── product-requirements.md
│   ├── user-research.md
│   ├── competitor-analysis.md
│   ├── user-journey.md
│   ├── ai-architecture.md
│   ├── privacy-and-security.md
│   ├── product-roadmap.md
│   └── metrics-experimentation.md
├── frontend/              # Planned: Next.js application
├── backend/               # Planned: FastAPI application
├── ai/
│   ├── avatar-generation/ # Planned
│   ├── virtual-try-on/    # Planned
│   └── fit-intelligence/  # Planned
├── analytics/             # Planned: event definitions and analysis
├── tests/                 # Planned
└── assets/                # Product diagrams and approved demo assets
```

## Development status

This repository begins with product discovery and requirements. Implementation will be added incrementally. Until a feature is implemented and tested, it should be considered planned.

## License

No software licence has been selected yet. Until a licence is added, the repository contents are not granted for reuse by others by default. Review model and dataset licences independently before use.
