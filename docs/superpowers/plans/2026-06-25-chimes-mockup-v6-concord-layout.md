# Chimes Mockup v6 — Concord-Format Homepage Relayout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Relayout `index.html` of chimes-mockup-v6 to follow concordcranes.com's structural patterns (image-card grids, label+title+description+arrow format, leaner stats/story/footer formatting) while keeping the existing liquid-glass dark theme, all current content, and all current images.

**Architecture:** Pure HTML/CSS/vanilla JS static site, no build step. Each task edits `index.html`, `style.css`, and/or `script.js` directly. No test framework exists in this repo — verification per task is a deterministic `grep` structural check (fast, scriptable) plus a final cross-section Playwright visual QA pass at the end of the plan (this environment has the Playwright MCP tool available and can navigate directly to a local `file://` path, no dev server needed).

**Tech Stack:** HTML5, CSS3 (custom properties, backdrop-filter glass system already defined in `style.css`), vanilla JS (`script.js`), Archivo/Barlow via Google Fonts.

## Global Constraints

- Scope is `index.html` only for this pass — do not touch `fleet.html`, `tailored-solutions.html`, `galleries.html`, `contact.html`, or their shared footer/header markup beyond what's already identical via copy-paste (this plan does not propagate footer changes to other pages).
- Keep the existing liquid-glass dark theme: colors (`--green:#70BF44`, `--navy:#1A427F`, `--bg:#0A0A0C`), glass panel system (`.glass`), pill radii, Archivo/Barlow fonts. Do not introduce new colors or fonts.
- Real photos remain the default for every card. The only new icon needed (Lift Planning & Studies, footer mail/phone) must come from Tabler Icons outline set — exact SVG source is provided in this plan, already fetched from `cdn.jsdelivr.net/npm/@tabler/icons@latest/icons/outline/`. Never hand-draw a new icon shape.
- Do not fabricate ISO/BEE certification badge artwork — keep the existing text+icon BEE Level 4 treatment, only restyle it as a pill/chip.
- Do not invent unconfirmed social profiles (LinkedIn, Instagram) — Facebook is the only confirmed real Chimes social profile.
- No `<video>` re-introduction, no JS glass-distortion libraries (out of scope from the original v6 spec, still holds).
- Every task ends with the page still opening cleanly with no new console errors.

---

## Task 1: Stats band values tagline

**Files:**
- Modify: `index.html:62-69` (`.stat-band` block)
- Modify: `style.css:144-149` (`STAT BAND` rules)

**Interfaces:**
- Produces: `.stat-values` CSS class, reusable if other pages later add a values line.

- [ ] **Step 1: Add the values tagline markup**

In `index.html`, the current stat band is:

```html
<div class="stat-band">
  <div class="stat-grid">
    <div class="stat fu"><div class="stat-n" data-to="2003" data-suffix="">0</div><div class="stat-l">Established</div></div>
    <div class="stat fu"><div class="stat-n" data-to="20" data-suffix="+">0</div><div class="stat-l">Cranes In Fleet</div></div>
    <div class="stat fu"><div class="stat-n" data-to="400" data-suffix="T">0</div><div class="stat-l">Max Capacity</div></div>
    <div class="stat fu"><div class="stat-n" data-to="24" data-suffix="/7">0</div><div class="stat-l">Always On Call</div></div>
  </div>
</div>
```

Replace it with:

```html
<div class="stat-band">
  <div class="stat-grid">
    <div class="stat fu"><div class="stat-n" data-to="2003" data-suffix="">0</div><div class="stat-l">Established</div></div>
    <div class="stat fu"><div class="stat-n" data-to="20" data-suffix="+">0</div><div class="stat-l">Cranes In Fleet</div></div>
    <div class="stat fu"><div class="stat-n" data-to="400" data-suffix="T">0</div><div class="stat-l">Max Capacity</div></div>
    <div class="stat fu"><div class="stat-n" data-to="24" data-suffix="/7">0</div><div class="stat-l">Always On Call</div></div>
  </div>
  <div class="stat-values fu">
    <span>Loyalty</span><span class="dot">&middot;</span><span>Integrity</span><span class="dot">&middot;</span><span>Foresight</span><span class="dot">&middot;</span><span>Excellence</span>
  </div>
</div>
```

- [ ] **Step 2: Add the CSS**

In `style.css`, the current stat band block is:

```css
/* ===== STAT BAND ===== */
.stat-band{padding:70px 0; background:var(--bg);}
.stat-grid{max-width:1180px; margin:0 auto; padding:0 24px; display:grid; grid-template-columns:repeat(4,1fr); gap:24px;}
.stat{text-align:center;}
.stat-n{font-family:var(--ff-head); font-weight:900; font-size:clamp(32px,4vw,48px); color:var(--white);}
.stat-l{font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:6px;}
```

Replace it with:

```css
/* ===== STAT BAND ===== */
.stat-band{padding:70px 0; background:var(--bg);}
.stat-grid{max-width:1180px; margin:0 auto; padding:0 24px; display:grid; grid-template-columns:repeat(4,1fr); gap:24px;}
.stat{text-align:center;}
.stat-n{font-family:var(--ff-head); font-weight:900; font-size:clamp(32px,4vw,48px); color:var(--white);}
.stat-l{font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:6px;}
.stat-values{max-width:1180px; margin:36px auto 0; padding:24px 24px 0; border-top:1px solid var(--glass-border); display:flex; justify-content:center; flex-wrap:wrap; gap:10px; font-family:var(--ff-head); font-weight:800; font-size:13px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted);}
.stat-values .dot{color:var(--green); text-shadow:0 0 8px var(--green-glow);}
```

- [ ] **Step 3: Verify structurally**

Run: `grep -c "stat-values" "index.html" "style.css"`
Expected: `index.html:1` (the markup block, `grep -c` counts matching lines so the single multi-span line counts once), `style.css:2` (the two new rule lines).

If using PowerShell instead: `Select-String -Path index.html,style.css -Pattern "stat-values" | Measure-Object | Select-Object Count`

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "Add values tagline to homepage stats band"
```

---

## Task 2: "Who We Are" → Story section with featured image

**Files:**
- Modify: `index.html:71-86` (`#about` section)
- Modify: `style.css:151-158` (`ABOUT` rules)
- Modify: `style.css:342` (responsive rule referencing `.about-split`)

**Interfaces:**
- Produces: `.about-img` CSS class.
- Consumes: `Cinematic Images/BARLOW pic #1.jpg` (existing asset, not yet used elsewhere on this page).

- [ ] **Step 1: Restructure the markup to an image + content layout**

Current block in `index.html`:

```html
<section class="sec" id="about">
  <div class="sec-inner about-split">
    <div class="fu">
      <span class="eyebrow">Who We Are</span>
      <h2>Lifting Power,<br>Built On <span class="hl">Trust.</span></h2>
    </div>
    <div class="about-rt fu">
      <p>For two decades Chimes Crane Hire has put steel in the sky across South Africa — safely, precisely and on schedule. Navy for authority, green for go: it's how we move.</p>
      <a href="contact.html#team" class="about-link">The Chimes Story <span class="arrow">&rarr;</span></a>
      <div class="bee">
        <svg width="18" height="18" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg>
        <span>BEE Level 4 Contributor</span>
      </div>
    </div>
  </div>
</section>
```

Replace it with:

```html
<section class="sec" id="about">
  <div class="sec-inner about-split">
    <div class="about-img fu"><img src="Cinematic%20Images/BARLOW%20pic%20%231.jpg" alt="Chimes crane on site" loading="lazy"></div>
    <div class="about-rt fu">
      <span class="eyebrow">Who We Are</span>
      <h2>Lifting Power,<br>Built On <span class="hl">Trust.</span></h2>
      <p>For two decades Chimes Crane Hire has put steel in the sky across South Africa — safely, precisely and on schedule. Navy for authority, green for go: it's how we move.</p>
      <a href="contact.html#team" class="about-link">The Chimes Story <span class="arrow">&rarr;</span></a>
      <div class="bee">
        <svg width="18" height="18" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg>
        <span>BEE Level 4 Contributor</span>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add the CSS for the image column**

Current block in `style.css`:

```css
/* ===== ABOUT ===== */
.about-split{display:grid; grid-template-columns:1fr 1fr; gap:60px; align-items:center;}
.about-split h2{font-size:clamp(28px,3.6vw,44px);}
.about-rt p{font-size:16px; color:var(--text); margin-bottom:20px;}
.about-link{display:inline-flex; align-items:center; gap:8px; font-family:var(--ff-head); font-size:12.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:var(--green);}
.about-link .arrow{transition:transform .2s;}
.about-link:hover .arrow{transform:translateX(4px);}
.bee{display:inline-flex; align-items:center; gap:8px; margin-top:22px; font-size:13px; color:var(--text);}
```

Replace it with:

```css
/* ===== ABOUT ===== */
.about-split{display:grid; grid-template-columns:1fr 1fr; gap:60px; align-items:center;}
.about-split h2{font-size:clamp(28px,3.6vw,44px);}
.about-img{border-radius:var(--radius-card); overflow:hidden; border:1px solid var(--glass-border); min-height:380px;}
.about-img img{width:100%; height:100%; min-height:380px; object-fit:cover;}
.about-rt p{font-size:16px; color:var(--text); margin:18px 0 20px;}
.about-link{display:inline-flex; align-items:center; gap:8px; font-family:var(--ff-head); font-size:12.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:var(--green);}
.about-link .arrow{transition:transform .2s;}
.about-link:hover .arrow{transform:translateX(4px);}
.bee{display:inline-flex; align-items:center; gap:8px; margin-top:22px; font-size:13px; color:var(--text);}
```

- [ ] **Step 3: Verify structurally**

Run: `grep -n "about-img\|about-split" "index.html" "style.css"`
Expected: shows the new `about-img` markup in `index.html` and both `about-img` rules in `style.css`, plus the still-present `about-split` grid rule.

- [ ] **Step 4: Visual check**

Open `index.html` directly in a browser (double-click or `file://` path) and confirm: the "Who We Are" section now shows a photo on one side and the heading/text/link/BEE badge on the other, at both desktop and narrow widths (image stacks above text below 900px per the existing `.about-split{grid-template-columns:1fr}` responsive rule — no change needed there since it already targets `.about-split`).

- [ ] **Step 5: Commit**

```bash
git add index.html style.css
git commit -m "Add featured image to homepage Story section"
```

---

## Task 3: Capabilities grid — every card becomes an image card

**Files:**
- Modify: `index.html:88-101` (`#services` section)
- Modify: `style.css:160-178` (`CAPABILITIES` rules)

**Interfaces:**
- Produces: `.cap-img-card` CSS class (image-backed capability/industry card, reused again in Task 4).
- Produces: `.cap-card-ico` CSS class (Tabler-icon styling for non-photo cards).

- [ ] **Step 1: Replace the two plain-text cards with image cards, add an icon to the remaining text card**

Current block in `index.html`:

```html
<section class="sec alt" id="services">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Capabilities</span><h2>What We Do</h2></div>
    <div class="cap-grid">
      <a class="cap-feature fu" href="fleet.html" style="background-image:url('Cinematic%20Images/crane%20LBBD%20%231.jpg');">
        <span class="cap-no">01</span>
        <div class="cap-txt"><h3>Mobile Crane Hire</h3><p>Compact city cranes to high-capacity all-terrain machines, with certified operators included.</p></div>
      </a>
      <div class="cap-card fu"><span class="cap-no">02</span><h3>Rigging</h3><p>Red Seal riggers for precise, safe load handling on every site.</p><span class="cap-arrow">&rarr;</span></div>
      <div class="cap-card fu"><span class="cap-no">03</span><h3>Transport</h3><p>Abnormal &amp; specialised load transport, fully permitted.</p><span class="cap-arrow">&rarr;</span></div>
      <div class="cap-card fu"><span class="cap-no">04</span><h3>Lift Planning &amp; Studies</h3><p>CAD-planned rigging studies and load charts before the crane ever arrives on site.</p><span class="cap-arrow">&rarr;</span></div>
    </div>
  </div>
</section>
```

Replace it with:

```html
<section class="sec alt" id="services">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Capabilities</span><h2>What We Do</h2></div>
    <div class="cap-grid">
      <a class="cap-feature fu" href="fleet.html" style="background-image:url('Cinematic%20Images/crane%20LBBD%20%231.jpg');">
        <span class="cap-no">01</span>
        <div class="cap-txt"><h3>Mobile Crane Hire</h3><p>Compact city cranes to high-capacity all-terrain machines, with certified operators included.</p></div>
      </a>
      <a class="cap-img-card fu" href="contact.html#quote" style="background-image:url('images/gallery/onsite-rigging1.jpg');">
        <span class="cap-no">02</span>
        <div class="cap-txt"><h3>Rigging</h3><p>Red Seal riggers for precise, safe load handling on every site.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <a class="cap-img-card fu" href="contact.html#quote" style="background-image:url('images/gallery/onsite-rigging2.jpg');">
        <span class="cap-no">03</span>
        <div class="cap-txt"><h3>Transport</h3><p>Abnormal &amp; specialised load transport, fully permitted.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <div class="cap-card fu">
        <svg class="cap-card-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2"/><path d="M9 5a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2"/><path d="M9 12l.01 0"/><path d="M13 12l2 0"/><path d="M9 16l.01 0"/><path d="M13 16l2 0"/></svg>
        <span class="cap-no">04</span><h3>Lift Planning &amp; Studies</h3><p>CAD-planned rigging studies and load charts before the crane ever arrives on site.</p><span class="cap-arrow">&rarr;</span>
      </div>
    </div>
  </div>
</section>
```

(`images/gallery/onsite-rigging1.jpg` = real Chimes rigging-crew photo; `images/gallery/onsite-rigging2.jpg` = real photo of a crew loading a cabin onto a trailer, the closest real match for "Transport" in the existing asset pool.)

- [ ] **Step 2: Add the CSS — merge `.cap-feature` with the new `.cap-img-card`, add the icon class**

Current block in `style.css`:

```css
/* ===== CAPABILITIES ===== */
.cap-hd{margin-bottom:44px;}
.cap-hd h2{font-size:clamp(28px,3.6vw,44px);}
.cap-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:20px;}
.cap-feature{
  grid-row:span 2; min-height:360px; background-size:cover; background-position:center;
  border-radius:var(--radius-card); position:relative; display:flex; flex-direction:column; justify-content:flex-end; padding:28px;
  border:1px solid var(--glass-border); overflow:hidden;
}
.cap-feature::before{content:''; position:absolute; inset:0; background:linear-gradient(180deg, transparent 30%, rgba(10,10,12,.92) 100%);}
.cap-feature .cap-no,.cap-feature .cap-txt{position:relative; z-index:1;}
.cap-card{
  background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%);
  border:1px solid var(--glass-border); border-radius:var(--radius-card); padding:28px; display:flex; flex-direction:column; gap:10px;
  transition:transform .3s, border-color .3s;
}
.cap-card:hover{transform:translateY(-4px); border-color:var(--green);}
.cap-no{font-family:var(--ff-head); font-weight:800; color:var(--green); font-size:13px;}
.cap-arrow{color:var(--green); font-size:18px;}
```

Replace it with:

```css
/* ===== CAPABILITIES ===== */
.cap-hd{margin-bottom:44px;}
.cap-hd h2{font-size:clamp(28px,3.6vw,44px);}
.cap-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:20px;}
.cap-feature,.cap-img-card{
  background-size:cover; background-position:center; position:relative;
  border-radius:var(--radius-card); display:flex; flex-direction:column; justify-content:flex-end; padding:28px;
  border:1px solid var(--glass-border); overflow:hidden; transition:transform .3s;
}
.cap-feature{grid-row:span 2; min-height:360px;}
.cap-img-card{min-height:280px;}
.cap-img-card:hover{transform:translateY(-4px);}
.cap-feature::before,.cap-img-card::before{content:''; position:absolute; inset:0; background:linear-gradient(180deg, transparent 30%, rgba(10,10,12,.92) 100%);}
.cap-feature .cap-no,.cap-feature .cap-txt,.cap-img-card .cap-no,.cap-img-card .cap-txt{position:relative; z-index:1;}
.cap-card{
  background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%);
  border:1px solid var(--glass-border); border-radius:var(--radius-card); padding:28px; display:flex; flex-direction:column; gap:10px;
  transition:transform .3s, border-color .3s;
}
.cap-card:hover{transform:translateY(-4px); border-color:var(--green);}
.cap-card-ico{width:40px; height:40px; color:var(--green); filter:drop-shadow(0 0 10px var(--green-glow));}
.cap-no{font-family:var(--ff-head); font-weight:800; color:var(--green); font-size:13px;}
.cap-arrow{display:inline-block; margin-top:4px; color:var(--green); font-size:18px; transition:transform .2s;}
.cap-img-card:hover .cap-arrow,.cap-card:hover .cap-arrow{transform:translateX(4px);}
```

- [ ] **Step 3: Verify structurally**

Run: `grep -c "cap-img-card" "index.html" "style.css"` — expected `index.html:2` (two new cards), `style.css:6` (class appears across the merged rules).
Run: `grep -c "cap-card-ico" "index.html" "style.css"` — expected `index.html:1`, `style.css:1`.
Run: `grep -c "icon-tabler-clipboard-list\|M9 5h-2" "index.html"` — expected at least `1` (confirms the Tabler path data landed, not a placeholder).

- [ ] **Step 4: Visual check**

Open `index.html` in a browser. Confirm the Capabilities grid now shows: card 01 (existing large photo card), cards 02 and 03 with real rigging/transport photos and visible arrows, and card 04 still a glass card but now with a small green clipboard-list icon above its title. Check the 2-column tablet breakpoint and 1-column mobile breakpoint (resize browser or use devtools) — cards should stack without overlapping text.

- [ ] **Step 5: Commit**

```bash
git add index.html style.css
git commit -m "Convert capability cards to consistent image-card format"
```

---

## Task 4: Industries section — convert from hover panel to static image-card grid

**Files:**
- Modify: `index.html:103-129` (`#industries` section)
- Modify: `style.css:180-191` (`INDUSTRIES` rules)
- Modify: `style.css:342` (drop `.ind-split` from the 900px responsive rule)
- Modify: `script.js:42-51` (remove `setIndustry` and its listeners — dead code once the markup is gone, confirmed unused on every other page in this repo)

**Interfaces:**
- Consumes: `.cap-img-card` class from Task 3.
- Produces: `.ind-grid` CSS class.

- [ ] **Step 1: Replace the interactive panel with a static card grid**

Current block in `index.html`:

```html
<section class="sec" id="industries">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Industries We Serve</span><h2>Built For The Work.</h2></div>
    <div class="ind-split glass fu">
      <ul class="ind-list">
        <li class="ind-li active" data-ind="construction">Construction<span class="ind-arrow">&rarr;</span></li>
        <li class="ind-li" data-ind="mining">Mining<span class="ind-arrow">&rarr;</span></li>
        <li class="ind-li" data-ind="petro">Petrochemical<span class="ind-arrow">&rarr;</span></li>
        <li class="ind-li" data-ind="telecoms">Telecoms<span class="ind-arrow">&rarr;</span></li>
        <li class="ind-li" data-ind="renewable">Renewable Energy<span class="ind-arrow">&rarr;</span></li>
      </ul>
      <div class="ind-panel">
        <svg class="ind-panel-ico active" data-ind="construction" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="35" x2="36" y2="35"/><rect x="8" y="21" width="9" height="14"/><rect x="23" y="14" width="11" height="21"/><line x1="28.5" y1="14" x2="28.5" y2="6"/><line x1="28.5" y1="6" x2="35" y2="6"/><line x1="35" y1="6" x2="35" y2="11"/></svg>
        <svg class="ind-panel-ico" data-ind="mining" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 33 L14 15 L19 23 L24 11 L36 33 Z"/><line x1="4" y1="33" x2="36" y2="33"/></svg>
        <svg class="ind-panel-ico" data-ind="petro" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21a6 6 0 0 1 12 0" /><rect x="6" y="21" width="12" height="13" rx="1"/><line x1="27" y1="34" x2="27" y2="16"/><path d="M27 16c-2.2 1.8-2.2 3.8 0 5.6c2.2-1.8 2.2-3.8 0-5.6z" fill="currentColor" stroke="none"/><line x1="3" y1="34" x2="36" y2="34"/></svg>
        <svg class="ind-panel-ico" data-ind="telecoms" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="13" y1="35" x2="13" y2="9"/><circle cx="13" cy="7" r="1.8" fill="currentColor" stroke="none"/><line x1="8" y1="35" x2="18" y2="35"/><path d="M19 16a9 9 0 0 1 0 13"/><path d="M24 11a16 16 0 0 1 0 23"/></svg>
        <svg class="ind-panel-ico" data-ind="renewable" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="20" y1="35" x2="20" y2="11"/><circle cx="20" cy="9" r="1.8" fill="currentColor" stroke="none"/><path d="M20 9 L10 6"/><path d="M20 9 L30 12"/><path d="M20 9 L23 19"/><line x1="14" y1="35" x2="26" y2="35"/></svg>
        <p class="ind-panel-txt active" data-ind="construction">From foundations to steel erection, our cranes handle material handling and structural lifts on construction sites of every size across Gauteng.</p>
        <p class="ind-panel-txt" data-ind="mining">Rough-terrain and all-terrain units built for shaft equipment, bulk material handling and heavy components on demanding mine sites.</p>
        <p class="ind-panel-txt" data-ind="petro">Tandem-lift capable cranes for refinery turnarounds, tank erection and flare stack work, handled to petrochemical safety standards.</p>
        <p class="ind-panel-txt" data-ind="telecoms">Mast and tower lifts for telecoms rollouts, carried out by certified riggers who understand confined access and live-site safety.</p>
        <p class="ind-panel-txt" data-ind="renewable">Wind turbine component handling and solar infrastructure lifts, supporting South Africa's renewable energy build-out.</p>
      </div>
    </div>
    <div style="text-align:center; margin-top:30px;"><a href="tailored-solutions.html" class="about-link">See Tailored Solutions By Industry <span class="arrow">&rarr;</span></a></div>
  </div>
</section>
```

Replace it with:

```html
<section class="sec" id="industries">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Industries We Serve</span><h2>Built For The Work.</h2></div>
    <div class="ind-grid">
      <a class="cap-img-card fu" href="tailored-solutions.html" style="background-image:url('images/tailored/construction.jpg');">
        <div class="cap-txt"><h3>Construction</h3><p>Material handling and structural lifts on construction sites of every size across Gauteng.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <a class="cap-img-card fu" href="tailored-solutions.html" style="background-image:url('images/tailored/mining.jpg');">
        <div class="cap-txt"><h3>Mining</h3><p>Rough-terrain and all-terrain units built for shaft equipment and heavy components on mine sites.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <a class="cap-img-card fu" href="tailored-solutions.html" style="background-image:url('images/tailored/petrochemical.webp');">
        <div class="cap-txt"><h3>Petrochemical</h3><p>Tandem-lift capable cranes for refinery turnarounds and tank erection, to petrochemical safety standards.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <a class="cap-img-card fu" href="tailored-solutions.html" style="background-image:url('images/tailored/telecoms.jpg');">
        <div class="cap-txt"><h3>Telecoms</h3><p>Mast and tower lifts for telecoms rollouts, carried out by certified riggers on live sites.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
      <a class="cap-img-card fu" href="tailored-solutions.html" style="background-image:url('images/tailored/renewables.jpg');">
        <div class="cap-txt"><h3>Renewable Energy</h3><p>Wind turbine component handling and solar infrastructure lifts across South Africa.</p><span class="cap-arrow">&rarr;</span></div>
      </a>
    </div>
    <div style="text-align:center; margin-top:30px;"><a href="tailored-solutions.html" class="about-link">See Tailored Solutions By Industry <span class="arrow">&rarr;</span></a></div>
  </div>
</section>
```

(Image filenames match the real photos already used for the same five industries on `tailored-solutions.html`.)

- [ ] **Step 2: Replace the CSS — drop the panel rules, add the grid**

Current block in `style.css`:

```css
/* ===== INDUSTRIES ===== */
.ind-split{display:grid; grid-template-columns:.85fr 1.15fr; gap:0; border-radius:var(--radius-card); overflow:hidden;}
.ind-list{border-right:1px solid var(--glass-border);}
.ind-li{font-family:var(--ff-head); font-weight:800; font-size:17px; text-transform:uppercase; padding:22px 26px; border-bottom:1px solid var(--glass-border); cursor:pointer; display:flex; justify-content:space-between; align-items:center; transition:background .15s, color .15s;}
.ind-li.active,.ind-li:hover{background:rgba(255,255,255,.06); color:var(--green);}
.ind-li .ind-arrow{opacity:0; color:var(--green); transition:opacity .15s, transform .15s; transform:translateX(-6px);}
.ind-li.active .ind-arrow{opacity:1; transform:translateX(0);}
.ind-panel{padding:40px; position:relative;}
.ind-panel-ico{display:none; color:var(--green); width:56px; height:56px; margin-bottom:24px; filter:drop-shadow(0 0 12px var(--green-glow));}
.ind-panel-ico.active{display:block;}
.ind-panel-txt{display:none; font-size:16px; color:var(--text);}
.ind-panel-txt.active{display:block;}
```

Replace it with:

```css
/* ===== INDUSTRIES ===== */
.ind-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:20px;}
```

- [ ] **Step 3: Update the 900px responsive rule**

Current line in `style.css` (inside the `@media (max-width:900px)` block, line 342):

```css
  .about-split,.ind-split,.quote-grid{grid-template-columns:1fr;}
```

Replace it with:

```css
  .about-split,.quote-grid{grid-template-columns:1fr;}
  .ind-grid{grid-template-columns:repeat(2,1fr);}
```

Also add `.ind-grid` to the 640px mobile single-column rule. Current line (inside `@media (max-width:640px)`):

```css
  .stat-grid,.cap-grid,.fleet-card-grid,.fleet-card-grid.sm,.quick-grid,.team-grid,.tlr-grid,.gallery-grid{grid-template-columns:1fr;}
```

Replace it with:

```css
  .stat-grid,.cap-grid,.ind-grid,.fleet-card-grid,.fleet-card-grid.sm,.quick-grid,.team-grid,.tlr-grid,.gallery-grid{grid-template-columns:1fr;}
```

- [ ] **Step 4: Remove the now-dead `setIndustry` JS**

Confirmed via repo-wide search that `.ind-li`/`.ind-panel` only ever existed on `index.html` — safe to delete outright, not just unused on this page.

Current block in `script.js`:

```javascript
// Industries clickable list + preview panel
function setIndustry(key) {
  document.querySelectorAll('.ind-li').forEach(el => el.classList.toggle('active', el.dataset.ind === key));
  document.querySelectorAll('.ind-panel-ico').forEach(el => el.classList.toggle('active', el.dataset.ind === key));
  document.querySelectorAll('.ind-panel-txt').forEach(el => el.classList.toggle('active', el.dataset.ind === key));
}
document.querySelectorAll('.ind-li').forEach(li => {
  li.addEventListener('click', () => setIndustry(li.dataset.ind));
  li.addEventListener('mouseenter', () => setIndustry(li.dataset.ind));
});

```

Delete this block entirely (replace with nothing — the surrounding blank lines collapse to a single blank line between the stats count-up block and the testimonial carousel block).

- [ ] **Step 5: Verify structurally**

Run: `grep -c "ind-split\|ind-li\|ind-panel\|setIndustry" "index.html" "style.css" "script.js"`
Expected: `0` for all three files (fully removed).

Run: `grep -c "ind-grid" "index.html" "style.css"`
Expected: `index.html:1` (the grid container), `style.css:3` (base rule + two responsive overrides).

Run: `grep -c "cap-img-card" "index.html"`
Expected: `7` (2 from Task 3 + 5 new industry cards).

- [ ] **Step 6: Visual check**

Open `index.html` in a browser. Confirm Industries now renders as a 3-column grid of real photo cards (Construction, Mining, Petrochemical, Telecoms, Renewable Energy) with no leftover hover/click interactivity, and that the "See Tailored Solutions By Industry" link below it still works. Check that clicking anywhere in the page no longer throws a console error about `setIndustry` being undefined (open devtools console while clicking around).

- [ ] **Step 7: Commit**

```bash
git add index.html style.css script.js
git commit -m "Convert Industries section from hover panel to static image-card grid"
```

---

## Task 5: Fleet showcase — arrow affordance for consistency

**Files:**
- Modify: `index.html:131-142` (`#fleet-showcase` section)
- Modify: `style.css:193-205` (`FLEET TEASER` rules)

**Interfaces:**
- Consumes: nothing new.
- Produces: `.fc-arrow` CSS class.

- [ ] **Step 1: Add an arrow to each fleet card**

Current block in `index.html`:

```html
<div class="fleet-card-grid fu">
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-400t.jpg');"><span class="fc-sub">Tadano ATF 400G-6</span><div class="fc-tag"><div class="fc-class">Heavy &middot; 400T</div><div class="fc-name">Our flagship — major lifts, max reach</div></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-220t.jpg');"><span class="fc-sub">126m With Jib</span><div class="fc-tag"><div class="fc-class">Premium &middot; 220T</div><div class="fc-name">Refinery &amp; power plant operations</div></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-90t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Mid &middot; 90T</div><div class="fc-name">The versatile workhorse</div></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-8-15t-truck.jpg');"><span class="fc-sub">Truck Mount</span><div class="fc-tag"><div class="fc-class">Compact &middot; 8&ndash;15T</div><div class="fc-name">Agile, tight-access lifting</div></div></a>
</div>
```

Replace it with:

```html
<div class="fleet-card-grid fu">
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-400t.jpg');"><span class="fc-sub">Tadano ATF 400G-6</span><div class="fc-tag"><div class="fc-class">Heavy &middot; 400T</div><div class="fc-name">Our flagship — major lifts, max reach</div><span class="fc-arrow">&rarr;</span></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-220t.jpg');"><span class="fc-sub">126m With Jib</span><div class="fc-tag"><div class="fc-class">Premium &middot; 220T</div><div class="fc-name">Refinery &amp; power plant operations</div><span class="fc-arrow">&rarr;</span></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-90t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Mid &middot; 90T</div><div class="fc-name">The versatile workhorse</div><span class="fc-arrow">&rarr;</span></div></a>
  <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-8-15t-truck.jpg');"><span class="fc-sub">Truck Mount</span><div class="fc-tag"><div class="fc-class">Compact &middot; 8&ndash;15T</div><div class="fc-name">Agile, tight-access lifting</div><span class="fc-arrow">&rarr;</span></div></a>
</div>
```

- [ ] **Step 2: Add the CSS**

Current block in `style.css`:

```css
/* ===== FLEET TEASER + FLEET PAGE CARDS ===== */
.fleet-card-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:20px;}
.fleet-card-grid.sm{grid-template-columns:repeat(4,1fr);}
.fc{
  position:relative; display:block; min-height:280px; background-size:cover; background-position:center;
  border-radius:var(--radius-card); border:1px solid var(--glass-border); overflow:hidden; text-align:left; padding:0; cursor:pointer;
  background-color:var(--bg2); font:inherit; transition:transform .3s;
}
.fc:hover{transform:translateY(-4px);}
.fc-sub{position:absolute; top:14px; left:14px; z-index:1; font-family:var(--ff-head); font-size:11px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; color:var(--white); background:rgba(10,10,12,.6); backdrop-filter:blur(8px); padding:5px 10px; border-radius:var(--radius-pill);}
.fc-tag{position:absolute; left:0; right:0; bottom:0; z-index:1; background:rgba(112,191,68,.92); backdrop-filter:blur(8px); color:var(--bg); padding:14px 18px;}
.fc-class{font-family:var(--ff-head); font-weight:800; font-size:13px;}
.fc-name{font-size:13px; margin-top:2px;}
```

Replace it with:

```css
/* ===== FLEET TEASER + FLEET PAGE CARDS ===== */
.fleet-card-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:20px;}
.fleet-card-grid.sm{grid-template-columns:repeat(4,1fr);}
.fc{
  position:relative; display:block; min-height:280px; background-size:cover; background-position:center;
  border-radius:var(--radius-card); border:1px solid var(--glass-border); overflow:hidden; text-align:left; padding:0; cursor:pointer;
  background-color:var(--bg2); font:inherit; transition:transform .3s;
}
.fc:hover{transform:translateY(-4px);}
.fc-sub{position:absolute; top:14px; left:14px; z-index:1; font-family:var(--ff-head); font-size:11px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; color:var(--white); background:rgba(10,10,12,.6); backdrop-filter:blur(8px); padding:5px 10px; border-radius:var(--radius-pill);}
.fc-tag{position:absolute; left:0; right:0; bottom:0; z-index:1; background:rgba(112,191,68,.92); backdrop-filter:blur(8px); color:var(--bg); padding:14px 18px;}
.fc-class{font-family:var(--ff-head); font-weight:800; font-size:13px;}
.fc-name{font-size:13px; margin-top:2px;}
.fc-arrow{display:inline-block; margin-top:6px; font-size:16px; font-weight:800; color:var(--bg); transition:transform .2s;}
.fc:hover .fc-arrow{transform:translateX(4px);}
```

- [ ] **Step 3: Verify structurally**

Run: `grep -c "fc-arrow" "index.html" "style.css"`
Expected: `index.html:4`, `style.css:2`.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "Add arrow affordance to fleet showcase cards for grid consistency"
```

---

## Task 6: Footer — contact icon row + badge-style BEE chip

**Files:**
- Modify: `index.html:201-221` (`<footer>`)
- Modify: `style.css:268-282` (`FOOTER` rules)

**Interfaces:**
- Consumes: nothing new.
- Produces: `.badge-chip` CSS class.

- [ ] **Step 1: Add mail/phone icons next to the existing Facebook icon**

Current block in `index.html`:

```html
<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
```

Replace it with:

```html
<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft badge-chip"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <div class="ft-social-row">
          <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
          <a href="mailto:office@chimes.co.za" aria-label="Email" class="ft-social"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10"/><path d="M3 7l9 6l9 -6"/></svg></a>
          <a href="tel:+27116261110" aria-label="Phone" class="ft-social"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2"/></svg></a>
        </div>
      </div>
```

- [ ] **Step 2: Add the CSS for the icon row and badge chip**

Current block in `style.css`:

```css
/* ===== FOOTER ===== */
footer{background:var(--bg2); border-top:1px solid var(--glass-border); padding:80px 0 30px;}
.ft-top{display:grid; grid-template-columns:1.4fr 1fr 1fr 1fr; gap:40px; margin-bottom:50px;}
.ft-brand img{height:30px; margin-bottom:16px;}
.ft-brand p{font-size:13.5px; color:var(--muted); max-width:320px;}
.ft-social{display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:50%; background:var(--glass); border:1px solid var(--glass-border); color:var(--white); margin-top:16px;}
.ft-col h5{font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--white); margin-bottom:16px;}
.ft-col ul{list-style:none;}
.ft-col li{margin-bottom:10px;}
.ft-col a{font-size:14px; color:var(--muted);}
.ft-col a:hover{color:var(--green);}
.bee-ft{margin-top:14px;}
.ft-bot{display:flex; justify-content:space-between; align-items:center; padding-top:26px; border-top:1px solid var(--glass-border); font-size:13px; color:var(--muted); flex-wrap:wrap; gap:10px;}
.ft-bot-link{color:var(--muted);}
.ft-tag{font-family:var(--ff-head); font-weight:700; letter-spacing:.04em;}
```

Replace it with:

```css
/* ===== FOOTER ===== */
footer{background:var(--bg2); border-top:1px solid var(--glass-border); padding:80px 0 30px;}
.ft-top{display:grid; grid-template-columns:1.4fr 1fr 1fr 1fr; gap:40px; margin-bottom:50px;}
.ft-brand img{height:30px; margin-bottom:16px;}
.ft-brand p{font-size:13.5px; color:var(--muted); max-width:320px;}
.ft-social{display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:50%; background:var(--glass); border:1px solid var(--glass-border); color:var(--white); transition:border-color .2s, color .2s;}
.ft-social:hover{border-color:var(--green); color:var(--green);}
.ft-social-row{display:flex; gap:10px; margin-top:16px;}
.ft-col h5{font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--white); margin-bottom:16px;}
.ft-col ul{list-style:none;}
.ft-col li{margin-bottom:10px;}
.ft-col a{font-size:14px; color:var(--muted);}
.ft-col a:hover{color:var(--green);}
.bee-ft{margin-top:14px;}
.badge-chip{padding:8px 14px; border:1px solid var(--glass-border); border-radius:var(--radius-pill); background:var(--glass);}
.ft-bot{display:flex; justify-content:space-between; align-items:center; padding-top:26px; border-top:1px solid var(--glass-border); font-size:13px; color:var(--muted); flex-wrap:wrap; gap:10px;}
.ft-bot-link{color:var(--muted);}
.ft-tag{font-family:var(--ff-head); font-weight:700; letter-spacing:.04em;}
```

- [ ] **Step 3: Verify structurally**

Run: `grep -c "badge-chip\|ft-social-row" "index.html" "style.css"`
Expected: `index.html:2` (one each), `style.css:2` (one each).
Run: `grep -c "class=\"ft-social\"" "index.html"`
Expected: `3` (Facebook, mail, phone — `ft-social-row` is a distinct string so it won't inflate this count).

- [ ] **Step 4: Visual check**

Open `index.html`, scroll to the footer. Confirm three circular icon buttons (Facebook, mail, phone) sit together under the brand paragraph, and the BEE Level 4 line now reads as a rounded pill/chip rather than plain inline text+icon.

- [ ] **Step 5: Commit**

```bash
git add index.html style.css
git commit -m "Restructure footer with contact icon row and badge-style BEE chip"
```

---

## Task 7: Final cross-section QA pass

**Files:**
- None (verification only). May produce a fix-up commit if QA finds a regression.

- [ ] **Step 1: Full-page structural sanity check**

Run from the repo root:

```bash
grep -c "ind-split\|ind-li\|ind-panel\|setIndustry" index.html style.css script.js
```

Expected: `0` everywhere — confirms Task 4's removal is complete and didn't leave orphaned references.

- [ ] **Step 2: Open the homepage with Playwright and screenshot each changed section**

Use the Playwright MCP browser tool to navigate to the local file (e.g. `file:///C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6/index.html`), then take a full-page screenshot. Visually confirm, top to bottom:

1. Stats band shows the 4 numbers plus the new "Loyalty · Integrity · Foresight · Excellence" line underneath.
2. "Who We Are" section shows an image beside the text (not two empty-feeling text columns).
3. Capabilities grid: all 4 cards have visual weight — 2 are large photos (01, plus the original feature), 2 are smaller photos (02 Rigging, 03 Transport), 1 is a glass card with a small green icon (04 Lift Planning & Studies).
4. Industries section is a grid of 5 real photo cards, no leftover sidebar list.
5. Fleet showcase cards each show a small arrow in the green tag area.
6. Footer shows 3 round icon buttons and a pill-shaped BEE badge.

- [ ] **Step 3: Check the browser console for errors**

Use the Playwright MCP console-messages tool against the same loaded page. Expected: no errors referencing `setIndustry`, `ind-li`, or any other removed identifier.

- [ ] **Step 4: Fix any regression found, otherwise finish**

If Step 2 or 3 surfaces a problem, fix it directly in `index.html`/`style.css`/`script.js`, re-run Steps 1-3, then commit the fix with message `Fix QA finding in homepage relayout` before continuing. If everything checks out, no commit is needed for this task — Task 6's commit is the last code change.

---

## Self-Review Notes

- **Spec coverage:** all 13 spec sections map to a task: 1 (header) and 2 (hero) and 3 (marquee) → no-change, confirmed by Global Constraints scope; 4 (stats) → Task 1; 5 (Story) → Task 2; 6 (Capabilities) → Task 3; 7 (Industries) → Task 4; 8 (Fleet) → Task 5; 9-11 (testimonials/team/gallery) → no-change per spec; 12 (CTA) → no-change; 13 (Footer) → Task 6; Icons section → Tasks 3 and 6 (Tabler SVGs, real source verified by curl during plan-writing, not invented); Out of scope items are respected (no other pages touched, no fabricated badges, no invented social profiles).
- **Type/class consistency:** `.cap-img-card` is defined once in Task 3 and reused unmodified in Task 4 — same class name, same properties, no duplicate definitions. `.fc-arrow`, `.stat-values`, `.about-img`, `.cap-card-ico`, `.badge-chip`, `.ft-social-row` are each defined exactly once and referenced consistently.
- **No placeholders:** every step shows the literal before/after code; no "TBD" or "similar to Task N" shortcuts.
