# StyleIQ Privacy & Security Requirements

**Status:** Requirements proposal; implementation and legal review pending.

StyleIQ may process personal photos and body measurements. These data require careful purpose limitation, transparent consent, access controls, retention rules, and deletion workflows.

## Data classification

| Data | Classification | Proposed handling |
|---|---|---|
| Uploaded full-body photo | Sensitive personal content | Optional, private, short retention |
| Body measurements | Personal body-related data | Collect only necessary values |
| Avatar representation | Derived personal data | User-controlled and deletable |
| Generated try-on image/video | Derived personal content | Private, expiring access |
| Product events | Usage data | Avoid raw photos and measurements |
| Consent record | Compliance evidence | Restricted access and audit |

## Consent and purpose

- Explain the processing purpose before photo upload.
- Obtain explicit consent before sending the photo to processing services.
- Keep model-training consent separate and off by default.
- Provide a measurement-only alternative.
- Explain any third-party processor and relevant data handling.
- Do not collect age unless a validated product requirement needs it.

## Storage and retention

- Use private object storage.
- Encrypt data in transit and at rest.
- Use short-lived signed URLs.
- Define a retention window for original photos and generated previews.
- Delete temporary files after processing or expiry.
- Provide user-requested deletion and verify deletion across primary storage and derived assets.
- Record deletion completion without retaining the deleted content.

## Security controls

- TLS everywhere.
- Server-side authorization checks.
- Role-based access to customer assets.
- File type, MIME, size, and malware validation.
- Rate limits and abuse prevention on generation endpoints.
- Audit logs for photo access, processing, and deletion.
- Secrets stored outside the repository.
- No public buckets or permanent public image links.
- No photos or body measurements in logs or analytics payloads.

## Third-party AI providers

Before integration, review:
- Input retention period
- Training/reuse policy
- Processing region and subprocessors
- Deletion support
- Security controls
- Contractual terms
- Commercial-use permission

A product privacy promise must match the actual behaviour of the provider.

## Governance

Review the applicable Indian privacy and consumer-protection requirements before launch. Laws and commencement dates can change; obtain qualified legal advice. This document is a product/security checklist, not legal advice.
