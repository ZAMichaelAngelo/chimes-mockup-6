# Chimes Mockup v6 — Concord-Format Homepage Relayout

## Purpose

Relayout `index.html` only. Keep the existing "liquid glass" dark theme (colors, glass panels, blob animations, Archivo/Barlow type) and all current content/images, but reshape the page's structure to follow the format of competitor reference site concordcranes.com: image-card grids with a consistent label + title + short description + arrow pattern, a leaner stats band with a values tagline, an image-paired "Story" section, and a simplified footer. Other pages (fleet, tailored-solutions, galleries, contact) are out of scope for this pass.

## Reference (verified live, 2026-06-25)

concordcranes.com homepage structure: header (dual CTA buttons + dropdown nav) → hero (heading + body + single CTA) → stats band (3-4 metrics + "CRANES 4 LIFE" values tagline: Loyalty, Integrity, Foresight, Excellence) → "Story" section (featured image + headline + "Our Story" link) → 8-card services grid (each card: image, capacity/category label, title, ~13-15 word description, arrow link) → footer (logo, social icons, copyright, certification badges).

## Section-by-section changes

1. **Header** — no change. Existing phone + "Get a Quote" buttons already match Concord's dual-CTA header pattern.

2. **Hero** — no structural change. Heading + body + CTA(s) already matches; both existing hero buttons are kept (we are keeping everything, not trimming to Concord's single-CTA hero).

3. **Marquee ticker** — unchanged. No Concord equivalent; stays as-is between hero and stats band.

4. **Stats band** — add a values tagline under the 4 existing numeric stats: "Loyalty · Integrity · Foresight · Excellence" (Chimes' own stated values, currently only in the footer tag). Numeric stats themselves are unchanged.

5. **"Who We Are" → Story section** — add a featured image alongside the existing text (currently text-only two-column `about-split`). Keep existing copy, the "The Chimes Story" link, and BEE badge. Image: `Cinematic Images/BARLOW pic #1.jpg` — the only Cinematic Images asset not already used elsewhere on this page (hero-still.jpg is the hero, crane LBBD #1.jpg is capability card 01, Chimes Team #1.jpg is the team band).

6. **Capabilities grid** — every card becomes an image card (currently only card 01 "Mobile Crane Hire" has a photo; cards 02-04 are plain text). Reformat all 4 to: image + title + short (~13-15 word) description + arrow link, matching card 01's existing pattern:
   - 02 Rigging → use an existing real rigging photo (`images/gallery/onsite-rigging1.jpg`, `onsite-rigging2.jpg`, or `onsite-rigging-harness.jpg`)
   - 03 Transport → use `images/gallery/onsite-rigging2.jpg` ("crew loading a cabin onto a trailer" — closest real fit for transport) or another real load/trailer shot from the pool
   - 04 Lift Planning & Studies → **known gap**: no real photo of CAD/lift-planning work exists in the asset pool. This card keeps a text-forward treatment with a sourced line icon (see Icons below) instead of forcing an unrelated photo — flagged here the same way prior known photo gaps (telecom/renewable on tailored-solutions.html) were flagged.

7. **Industries section** — converted from the interactive hover/tab panel to a static image-card grid, same format as Capabilities (image + title + short description + arrow). Reuse the real industry photos already shot for `tailored-solutions.html` (`images/tailored/construction.jpg`, `mining.jpg`, `petrochemical.webp`, `telecoms.jpg`, `renewables.jpg`) — same known caveat already on record: telecoms/renewables use the closest-fit real photo, not a dedicated shot. Keep the "See Tailored Solutions By Industry" link below the grid. The interactive tab/hover JS behavior (`setIndustry()`) becomes dead code on this page once removed — drop the now-unused markup/JS for this section specifically, not the shared script.

8. **Fleet showcase** — already closest to Concord's card pattern (image + class label + title). Trim each card's description to a short arrow-link-style line for consistency with the other grids; no other structural change.

9. **Testimonials, 10. Team band, 11. Gallery preview** — unchanged. No Concord equivalent; kept per the decision to retain all existing content.

12. **CTA band** — unchanged.

13. **Footer** — restructure toward Concord's leaner shape: logo, a social/contact icon row (Facebook — the only confirmed real Chimes social profile — plus a mail icon for the existing email link and a phone icon for the existing number, replacing plain text-link styling), copyright line, and the existing BEE Level 4 tag presented as a small badge-style chip. Existing nav columns (Company/Services/Contact) are kept since we're keeping all content — Concord's footer is simpler, but trimming those columns isn't part of this pass.

   **Note on certification badges**: Concord's footer shows real BEE and ISO certification badge graphics. We do not have a verified ISO certification or an official BEE certificate graphic on file, so we will not fabricate certification badge artwork — keep the existing text+icon BEE Level 4 chip rather than inventing a badge image. Flagging this so it isn't mistaken for an oversight.

## Icons

Photos remain the default for every card (per existing project convention: real photos only, no generic/stock imagery). Icons are only used as a fallback where no suitable real photo exists (Lift Planning & Studies card) or for small UI glyphs (footer contact icons). Any icon used is sourced from a real, professional icon set — **Tabler Icons** (`cdn.jsdelivr.net/npm/@tabler/icons@latest/icons/outline/<name>.svg`), the same library already used elsewhere in this project after custom hand-drawn SVGs were flagged as "too AI." No new hand-drawn/generic icon shapes.

## Out of scope

- Fleet, Tailored Solutions, Galleries, and Contact pages — not touched in this pass (their own footers/headers stay as they are today; a follow-up pass would be needed to bring them in line with whatever footer changes land here).
- Fabricating certification badge artwork (ISO, BEE certificate graphics).
- Inventing unconfirmed social profiles (LinkedIn, Instagram) beyond the one confirmed real Facebook page.
- Any JS/CSS cleanup beyond what's needed to remove the now-unused industries tab/hover behavior on this page.
