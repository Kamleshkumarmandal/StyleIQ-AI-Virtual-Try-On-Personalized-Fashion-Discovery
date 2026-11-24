# StyleIQ Product Requirements Document

**Status:** Draft — discovery and MVP definition  
**Product:** StyleIQ — AI Virtual Try-On & Personalized Fashion Discovery

## 1. Vision

Help online fashion shoppers make more confident purchase decisions by combining personalized discovery, visual garment previews, and transparent measurement-based fit guidance.

## 2. Problem statement

Customers shopping online cannot physically try on clothing. Product images and generic size charts may leave uncertainty about appearance, size, fit, and availability. StyleIQ will investigate whether an avatar-based preview and clear fit guidance improve the shopping experience.

This is a product hypothesis. It must be validated through customer research and controlled testing.

## 3. Target users

- First-time online fashion shoppers who need confidence before ordering.
- Frequent shoppers who want faster discovery.
- Shoppers whose measurements fall between standard sizes.
- Style-focused shoppers who want outfit visualization.
- Privacy-conscious shoppers who prefer not to upload photos.

## 4. Goals

- Offer measurement-based and optional photo-based avatar creation.
- Provide a useful virtual try-on preview for supported items.
- Keep visual preview and fit guidance as separate experiences.
- Show explainable size guidance only when required measurement data exists.
- Allow customers to control and delete their avatar data.
- Instrument the journey to evaluate customer and business outcomes.

## 5. Non-goals for MVP

- Guaranteeing physical fit.
- Perfect fabric physics or exact fabric drape.
- Photorealistic video for every catalog item.
- Inferring exact hidden measurements from one photo.
- Replacing retailer size charts.
- Broad support for every garment category.

## 6. Personas and needs

### Privacy-first shopper
Wants to see how an item may look without sharing a photo. Needs measurement-based avatar creation and easy deletion.

### Visual-confidence shopper
Wants a more personal visual preview. Needs clear consent, understandable photo requirements, and control over generated results.

### Fit-uncertain shopper
Wants help choosing a size. Needs accurate garment measurements, transparent explanation, and uncertainty when data is missing.

## 7. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| AV-01 | Create measurement-based avatar | P0 |
| AV-02 | Create photo-based avatar with explicit consent | P0 |
| AV-03 | Edit and delete avatar | P0 |
| AV-04 | Switch avatar method | P1 |
| CAT-01 | Display supported products and garment images | P0 |
| CAT-02 | Store garment measurements per size | P0 for fit guidance |
| VTO-01 | Generate static preview for supported garments | P0 |
| VTO-02 | Label preview as AI-generated | P0 |
| VTO-03 | Provide retry and unsupported-item fallback | P0 |
| FIT-01 | Compare confirmed body and garment measurements | P0 |
| FIT-02 | Explain recommendation and missing data | P0 |
| CART-01 | Add selected product and size to cart | P0 |
| PRIV-01 | Record consent and retention choice | P0 |
| PRIV-02 | Delete source photo and derived assets | P0 |
| ANALYTICS-01 | Capture privacy-safe journey events | P0 |
| VTO-04 | Short controlled video preview | P2 |
| VTO-05 | Side/back/360 preview | P2 |

## 8. User experience rules

- Do not force photo upload.
- Age is not required for avatar generation or fit prediction.
- Skin tone is optional appearance personalization only.
- A single photo must not be presented as a reliable source of complete body measurements.
- A size recommendation requires sufficient confirmed body and garment measurements.
- If data is missing, show the standard size chart and explain the limitation.
- Generated images must be labeled as visual estimates, not photographs of the delivered garment.

## 9. Acceptance criteria for MVP

1. A user can create a measurement avatar without uploading a photo.
2. A user can opt into photo processing and complete the photo flow.
3. Users can review and delete avatar data.
4. A supported product can produce a static try-on preview.
5. Unsupported products receive a clear fallback.
6. Fit guidance explains the measurements used and missing inputs.
7. A user can choose a size and add the item to cart.
8. Analytics capture journey events without raw photos or measurements.
9. Failure states are tested: poor photo, missing measurements, AI failure, no stock, and deletion.

## 10. Open questions

- Which clothing categories have suitable garment images and measurement data?
- What level of avatar personalization do shoppers consider useful?
- Is a photo-based flow worth the additional privacy and processing cost?
- Does the preview improve confidence enough to justify generation latency?
- Which return reasons can be reliably linked to product fit?
- What minimum evidence is needed before a fit recommendation is shown?
