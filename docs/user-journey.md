# StyleIQ Customer Journey

## Primary journey

1. Customer browses personalized fashion discovery.
2. Customer opens a supported product detail page.
3. Customer selects **Try it on me**.
4. Customer selects or creates an avatar:
   - Measurement-based, no photo required.
   - Optional photo-based with explicit consent.
5. StyleIQ validates the input and product compatibility.
6. Try-on service generates a static preview.
7. Customer reviews the AI-generated appearance preview.
8. Fit service separately evaluates confirmed body and garment measurements.
9. Customer sees size guidance, reasons, missing data, and uncertainty.
10. Customer checks size availability and adds the selected item to cart.
11. Customer may later provide fit feedback.

## Failure and recovery journeys

| Failure | Response |
|---|---|
| Photo too dark or obstructed | Explain issue; provide retake guidance |
| Unsupported pose | Offer measurement avatar or normal product images |
| Missing body measurements | Do not produce a confident fit recommendation |
| Missing garment measurements | Show retailer size chart; suppress fit prediction |
| Try-on service timeout | Retry once; offer standard product images |
| Product out of stock | Show available sizes or alternatives |
| Customer declines photo consent | Continue through measurement path |
| Deletion requested | Revoke access and remove stored/derived assets per retention policy |

## Journey design principles

- Explain why information is requested.
- Do not make photo upload mandatory.
- Preserve user-selected size; never silently change it.
- Clearly label generated images.
- Separate visual preview from physical fit guidance.
- Make privacy and deletion controls discoverable.
