---
description: Design complete email sequences with subject lines, body copy, timing, segmentation, and deliverability guidance
argument-hint: "<sequence type: welcome|nurture|onboarding|re-engagement|cart-abandonment>"
---

# Email Sequence

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Design a complete email sequence ready for implementation in any ESP. Includes subject lines with A/B variants, preview text, full body copy, send timing with cadence logic, segmentation rules, branching conditions, personalization tokens, and deliverability best practices.

## Trigger

User runs `/email-sequence` or asks to create an email drip, email flow, nurture sequence, welcome series, re-engagement campaign, or cart abandonment flow.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Sequence type** — one of:
   - Welcome series (new subscriber/user)
   - Nurture sequence (move leads down funnel)
   - Onboarding (activate new users/customers)
   - Re-engagement (win back inactive subscribers)
   - Cart abandonment (recover lost purchases)
   - Post-purchase (retention, upsell, review request)
   - Event-based (webinar, product launch, seasonal)
   - Promotional (sale, offer, limited-time)

2. **Goal** — what the sequence should achieve (activate, convert, retain, upsell, educate, re-engage)

3. **Audience segment** — who receives this sequence and what triggers entry (signup, purchase, inactivity period, cart event, etc.)

4. **Number of emails** — desired count, or let the system recommend based on sequence type

5. **Key messages or offers** — core value propositions, promotions, or content to include

6. **ESP** (optional) — platform in use (Klaviyo, Mailchimp, HubSpot, SendGrid, Customer.io) for format and feature guidance

## Brand Voice

- If a brand profile exists, apply voice settings automatically
- Load email-specific tone overrides from guidelines if available
- Apply compliance rules (CAN-SPAM, GDPR, CASL) based on brand's target markets

## Sequence Design

### Sequence Architecture
- Map the sequence to the customer journey stage
- Define the narrative arc (introduction → value → proof → conversion)
- Determine optimal email count based on sequence type:
  - Welcome: 3-5 emails over 7-14 days
  - Nurture: 5-8 emails over 3-6 weeks
  - Onboarding: 4-7 emails over 14-30 days
  - Re-engagement: 3-4 emails over 7-14 days
  - Cart abandonment: 3 emails over 3 days
  - Post-purchase: 3-5 emails over 30-60 days
- Define send cadence and timing logic

### Per-Email Blueprint

For each email in the sequence:

**Subject Lines:**
- 2-3 subject line options per email
- Character counts (aim for 30-50 characters for mobile)
- Preview text that complements (not repeats) the subject
- A/B testing recommendations

**Body Copy:**
- Opening hook tied to the sequence narrative
- Body content with clear hierarchy and scannable formatting
- Single primary CTA (button text + destination)
- Secondary CTA (optional, text link)
- Personalization tokens (first name, company, product, behavior-based)
- Dynamic content blocks (based on segment attributes)

**Timing:**
- Send delay from trigger or previous email
- Best send time recommendation (day of week, time of day)
- Timezone handling notes

### Segmentation and Branching Logic
- Entry trigger conditions
- Branching rules based on engagement (opened, clicked, converted)
- Exit conditions (converted, unsubscribed, completed sequence)
- Suppression rules (already purchased, already in another sequence)

### Deliverability Checklist

For each email, verify:
- No spam trigger words in subject or body
- Link density appropriate (not too many links)
- Image-to-text ratio balanced
- Unsubscribe link present and functional
- Physical address included (CAN-SPAM)
- Authentication reminders (SPF, DKIM, DMARC)
- List hygiene recommendations

## Output Format

### Sequence Overview
- Sequence name, type, and goal
- Target audience and entry trigger
- Email count and total duration
- Expected performance benchmarks for the sequence type

### Email-by-Email Breakdown

| Email # | Subject Line | Send Timing | Goal | Primary CTA |
|---------|-------------|-------------|------|-------------|

Followed by full copy for each email.

### Flow Diagram
- Visual representation of the sequence flow with branching logic
- Entry → Email 1 → Wait → Email 2 → Branch (opened/not opened) → etc.

### Performance Benchmarks

| Metric | Industry Average | Target |
|--------|-----------------|--------|

Include: open rate, click rate, conversion rate, unsubscribe rate per email.

## After the Sequence

Ask: "Would you like me to:
- Set up this sequence in your ESP? (`/send-email-campaign`)
- Create A/B test variants for the subject lines? (`/prompt-test`)
- Design a complementary re-engagement flow for non-openers?
- Build landing pages for the CTA destinations? (`/content-engine`)
- Add SMS touchpoints alongside the emails? (`/send-sms`)
- Review deliverability setup for your domain? (`/email-sequence` with deliverability focus)"
