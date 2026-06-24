# Chimes Mockup v6 — "Liquid Glass" Dark Redesign

## Purpose

A new pitch mockup for Chimes Crane Hire, styled completely differently from v3/v4/v5: a dark theme built around an Apple-style "liquid glass" UI — translucent, pill-shaped, rounded chrome (header/footer/buttons/cards) with flowing animated backgrounds. Content/copy is sourced from v4's pages; visual language is new.

## Brand colors (verified, not guessed)

Pulled by screenshotting the live site (chimescranes.co.za) and sampling actual pixel values:

- Signature green: `#70BF44` (top bar, crane livery, primary brand color)
- Navy blue: `#1A427F` (nav bar / logo wordmark — the brand's actual secondary color)
- Near-black background: `#0A0A0C`
- White text: `#FFFFFF`
- Amber/hazard-yellow micro-accent (industry-standard safety color, used sparingly for hairline details, not blocks)

This differs from v4 (dark navy + lime industrial) and v5 (dark + green-only glow) by introducing navy as a real secondary panel/accent color alongside green, rather than staying green-monochrome.

## Visual system

**Glass technique** — pure CSS, no JS distortion libraries:
- `backdrop-filter: blur() saturate()` on translucent panels
- Fully rounded / pill-shaped header, footer, nav links, buttons, and cards
- Soft inset highlight along the top edge of glass panels to fake specular light (the core visual trick behind "liquid glass" look)
- Subtle gradient borders (1px, low-opacity, light-to-transparent) on glass edges

Rationale for pure CSS over SVG displacement/refraction filters or JS glass libraries: comparable visual payoff, far better cross-browser reliability and performance — relevant since the project also explicitly trades a hero video for a static image for performance.

**Flowing animation**:
- Multiple large, slow, blurred gradient blobs drifting continuously behind glass panels (bigger/slower/more multi-color than v5's aurora — mixing green and navy)
- A liquid morphing blob shape idling in the hero (animated `border-radius`/`clip-path`)
- Scroll-reveal fade/slide-ins on section entry
- Glass ripple effect on button hover
- Animated marquee ticker (pattern carried over from v4/v5)

**Typography**: keep Archivo (headings) + Barlow (body), consistent with v3–v5.

## Pages

Mirrors v4's page set, plus one new page:

- `index.html` — home
- `fleet.html` — fleet & specs
- `galleries.html` — galleries
- `contact.html` — contact
- `tailored-solutions.html` — **new**, added as its own header nav tab

All restyled in the new glass system; content/copy/section structure sourced from v4's existing pages. Proven interactive *behaviors* from v5 (industries tab panel, gallery lightbox) may be reused, rebuilt visually in the new style.

## Hero media: video → static image

The homepage hero currently autoplays `Cinematic Images/top-body-video.mp4`. For performance, this is replaced with a static image:

- Source: `Chimes Work/Source Assets/Must Use Content/Top body video.mp4` (the real master file, not the existing dramatic sunset poster photo)
- Extract an actual frame from this video where the truck is clearly in frame (via local frame extraction, e.g. OpenCV — no system-wide ffmpeg install)
- Export as an optimized static image, used as the hero background; no `<video>` element, no autoplay weight

## Tailored Solutions page (new)

A dedicated page — not just a homepage panel like v5's industries widget — with a hero and a grid of service categories, each with a real Chimes photo + short description:

- Steel / Construction
- Mining
- Petrochemical
- Telecoms
- Renewables
- General Industrial

Images are pulled from the existing real photo pool (`Cinematic Images`, `Crane Sizes`) rather than generic stock photography — authentic, no licensing risk, consistent with the rest of the site.

**Known gap**: the current photo pool has no dedicated telecom- or renewable-specific shot. Those two categories will use the closest-fit real fleet/action photo as a placeholder. Flagged for the user to swap in better photos later if/when industry-specific site photos are taken.

## Repo / hosting

New folder `chimes-mockup-v6`, sibling to `chimes-mockup-v3/v4/v5`, following the same self-contained pattern (own copy of image assets). Git init and any GitHub repo creation / push / Pages setup requires explicit user confirmation before being done — not assumed as part of this spec.

## Out of scope

- Generic/external stock photography (explicitly rejected in favor of real photos)
- JS-based glass distortion/refraction effects
- Pushing to GitHub or creating the GitHub repo (separate confirmation step)
