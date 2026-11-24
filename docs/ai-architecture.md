# StyleIQ AI Architecture

**Status:** Proposed architecture. No AI services are implemented yet.

## Service boundaries

- **Avatar service:** manages measurement profiles and photo-derived visual inputs.
- **Catalog service:** exposes supported garment images, category metadata, measurements, and stock.
- **Try-on orchestrator:** validates compatibility and calls a replaceable model adapter.
- **Fit intelligence:** compares confirmed body measurements with garment measurements using explainable rules initially.
- **Analytics service:** collects privacy-safe product events.

## Proposed request flow

```text
Next.js client
   |
   v
FastAPI API gateway
   |
   +--> Authentication & consent
   |
   +--> Avatar service
   |      +--> Measurement avatar
   |      +--> Photo validation / pose / segmentation
   |
   +--> Catalog service
   |      +--> Garment image
   |      +--> Size-specific measurements
   |
   +--> Try-on orchestrator
   |      +--> Licensed VTON model/API
   |      +--> Quality validation
   |      +--> Private asset storage
   |
   +--> Fit intelligence
   |      +--> Measurement comparison
   |      +--> Explanation and uncertainty
   |
   +--> Privacy-safe analytics
```

## Try-on pipeline

1. Validate input file type, size, and image quality.
2. Check supported pose and garment category.
3. Segment or preprocess the person and garment image as required by the selected model.
4. Invoke the VTON model through an adapter interface.
5. Validate output dimensions and basic visual quality.
6. Store output privately with an expiry policy.
7. Return an access-controlled preview URL.

## Fit pipeline

Inputs:
- Confirmed body measurements relevant to the garment.
- Garment measurements for each size.
- Fit intent (slim, regular, relaxed).
- Fabric stretch and category metadata when available.

Example: `ease = garment_measurement - body_measurement`

The acceptable ease range must be category-, construction-, fabric-, and fit-specific. Do not use a universal threshold. Missing data should produce an unavailable/low-confidence result, not a fabricated recommendation.

## Model adapter

Keep the model provider replaceable. Evaluate:
- Code licence
- Checkpoint/weights licence
- Dataset restrictions
- Hosted API terms and retention
- Commercial usage rights
- Data transfer and processing locations
- Latency and GPU cost
- Output quality and failure rate

Research availability is not commercial permission. Legal and security review must happen before real customer photos are sent to a provider.

## Video phase

Video is a later milestone:
- Start from a validated static preview or 3D avatar.
- Use controlled motion and camera angles.
- Evaluate identity, garment consistency, flicker, and latency.
- Label generated output.
- Do not imply physical fabric or fit simulation unless measured and validated.
