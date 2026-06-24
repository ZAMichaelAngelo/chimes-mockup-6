# Chimes Mockup v6 "Liquid Glass" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5-page static HTML mockup (`chimes-mockup-v6`) for Chimes Crane Hire — a dark, "liquid glass" (Apple-style frosted, pill-shaped, rounded chrome) redesign with flowing gradient-blob animation, sourcing copy/structure from v4 and adding a new Tailored Solutions page.

**Architecture:** Plain static HTML/CSS/JS, no build step or framework — same pattern as v3/v4/v5. One shared `style.css` + `script.js` included on every page; each page repeats its own nav/footer markup (no templating engine in this codebase).

**Tech Stack:** HTML5, CSS3 (`backdrop-filter`, CSS animations), vanilla JS (`IntersectionObserver`), Python 3 + `opencv-python-headless` (one-off, for hero frame extraction only — not a runtime dependency of the site).

## Global Constraints

- Brand colors (verified from the live site, not guessed): green `#70BF44`, navy `#1A427F`, background `#0A0A0C`, white `#FFFFFF`.
- Glass effect must be pure CSS (`backdrop-filter`) — no JS distortion/refraction libraries.
- No `<video>` element anywhere on the homepage — hero must use a static image.
- All photography must be real existing Chimes photos from `chimes-mockup-v4`'s asset pool — no external/generic stock photography.
- Fonts: Archivo (headings) + Barlow (body) via Google Fonts, same as v3–v5.
- Every page ships the same nav (5 links + Tailored Solutions tab) and footer.
- Do not create a GitHub repo or push anywhere — local git commits only.

---

## File Structure

```
chimes-mockup-v6/
  index.html
  fleet.html
  galleries.html
  tailored-solutions.html
  contact.html
  style.css
  script.js
  favicon-16.png / favicon-32.png / favicon-180.png / favicon.ico
  Logos/Chimes_Dynamic_Logo_White_PNG.png
  Cinematic Images/BARLOW pic #1.jpg, crane LBBD #1.jpg, Chimes Team #1.jpg, hero-still.jpg
  images/fleet/*.jpg (8 files)
  images/gallery/*.jpg (40 files)
  images/tailored/ (6 files, copied+renamed from existing pool)
  images/*.webp (silo-tanks-1.webp, construction-14-e1486547976132.webp, the_team.webp, the_team3.webp, the_braai.webp)
  scripts/sample_hero_frames.py
  scripts/extract_hero_frame.py
```

---

### Task 1: Project scaffold — copy assets + design tokens

**Files:**
- Create: `chimes-mockup-v6/style.css`
- Create: `chimes-mockup-v6/style-guide.html` (smoke-test page, kept as living reference)
- Copy: see asset list below

**Interfaces:**
- Produces CSS variables every later task consumes: `--bg`, `--bg2`, `--green`, `--green-soft`, `--green-glow`, `--navy`, `--navy-soft`, `--navy-glow`, `--amber`, `--white`, `--text`, `--muted`, `--glass`, `--glass-hi`, `--glass-border`, `--radius-pill`, `--radius-card`, `--ff-head`, `--ff-body`.
- Produces base classes: `.glass`, `.glass-pill`, `.fu` (fade-up reveal, same contract as v4: starts hidden, `.vis` added by JS on scroll).

- [ ] **Step 1: Copy shared assets from v4**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups"
mkdir -p chimes-mockup-v6/Logos chimes-mockup-v6/"Cinematic Images" chimes-mockup-v6/images/fleet chimes-mockup-v6/images/gallery chimes-mockup-v6/images/tailored chimes-mockup-v6/scripts

cp chimes-mockup-v4/favicon-16.png chimes-mockup-v4/favicon-32.png chimes-mockup-v4/favicon-180.png chimes-mockup-v4/favicon.ico chimes-mockup-v6/
cp chimes-mockup-v4/Logos/Chimes_Dynamic_Logo_White_PNG.png chimes-mockup-v6/Logos/
cp "chimes-mockup-v4/Cinematic Images/BARLOW pic #1.jpg" "chimes-mockup-v4/Cinematic Images/crane LBBD #1.jpg" "chimes-mockup-v4/Cinematic Images/Chimes Team #1.jpg" "chimes-mockup-v6/Cinematic Images/"
cp chimes-mockup-v4/images/fleet/*.jpg chimes-mockup-v6/images/fleet/
cp chimes-mockup-v4/images/gallery/*.jpg chimes-mockup-v6/images/gallery/
cp chimes-mockup-v4/images/silo-tanks-1.webp chimes-mockup-v4/images/construction-14-e1486547976132.webp chimes-mockup-v4/images/the_team.webp chimes-mockup-v4/images/the_team3.webp chimes-mockup-v4/images/the_braai.webp chimes-mockup-v6/images/

cp "chimes-mockup-v6/images/gallery/onsite-lbbd7.jpg" "chimes-mockup-v6/images/tailored/construction.jpg"
cp "chimes-mockup-v6/Cinematic Images/BARLOW pic #1.jpg" "chimes-mockup-v6/images/tailored/mining.jpg"
cp "chimes-mockup-v6/images/silo-tanks-1.webp" "chimes-mockup-v6/images/tailored/petrochemical.webp"
cp "chimes-mockup-v6/images/gallery/onsite-lbbd3.jpg" "chimes-mockup-v6/images/tailored/telecoms.jpg"
cp "chimes-mockup-v6/images/gallery/onsite-c8.jpg" "chimes-mockup-v6/images/tailored/renewables.jpg"
cp "chimes-mockup-v6/images/construction-14-e1486547976132.webp" "chimes-mockup-v6/images/tailored/industrial.webp"

ls chimes-mockup-v6/images/tailored
```

Expected: 6 files listed (construction.jpg, mining.jpg, petrochemical.webp, telecoms.jpg, renewables.jpg, industrial.webp).

- [ ] **Step 2: Write `style.css` — tokens, reset, typography, glass base**

```css
/* Chimes Crane Hire — Mockup v6 "Liquid Glass" */

@font-face { /* fonts loaded via <link> in <head>, no @font-face needed */ }

* { margin:0; padding:0; box-sizing:border-box; }

:root{
  --bg:#0A0A0C;
  --bg2:#111418;
  --green:#70BF44;
  --green-soft:#9AD673;
  --green-glow:rgba(112,191,68,.45);
  --navy:#1A427F;
  --navy-soft:#3868B0;
  --navy-glow:rgba(26,66,127,.5);
  --amber:#E8A93C;
  --white:#FFFFFF;
  --text:rgba(255,255,255,.86);
  --muted:rgba(255,255,255,.56);
  --glass:rgba(255,255,255,.06);
  --glass-hi:rgba(255,255,255,.16);
  --glass-border:rgba(255,255,255,.16);
  --radius-pill:999px;
  --radius-card:28px;
  --ff-head:'Archivo', sans-serif;
  --ff-body:'Barlow', sans-serif;
}

html{scroll-behavior:smooth;}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--ff-body);
  font-size:16px;
  line-height:1.55;
  overflow-x:hidden;
}
h1,h2,h3,h4,h5{font-family:var(--ff-head); font-weight:800; color:var(--white); line-height:1.1;}
a{color:inherit; text-decoration:none;}
img{max-width:100%; display:block;}
.hl{color:var(--green); text-shadow:0 0 24px var(--green-glow);}
.eyebrow{
  display:inline-flex; align-items:center; gap:7px;
  font-family:var(--ff-head); font-size:12px; font-weight:800;
  letter-spacing:.18em; text-transform:uppercase; color:var(--green); margin-bottom:14px;
}
.eyebrow::before{content:''; width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 10px var(--green-glow);}

.sec{padding:120px 0;}
.sec.alt{background:var(--bg2);}
.sec-inner{max-width:1180px; margin:0 auto; padding:0 24px;}

.fu{opacity:0; transform:translateY(28px); transition:opacity .7s ease, transform .7s ease;}
.fu.vis{opacity:1; transform:translateY(0);}

/* ===== GLASS ===== */
.glass{
  position:relative;
  background:linear-gradient(160deg, var(--glass-hi), var(--glass));
  backdrop-filter:blur(22px) saturate(160%);
  -webkit-backdrop-filter:blur(22px) saturate(160%);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-card);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22), 0 20px 60px rgba(0,0,0,.45);
}
.glass::before{
  content:''; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background:linear-gradient(180deg, rgba(255,255,255,.16), transparent 42%);
}
.glass-pill{border-radius:var(--radius-pill);}

/* ===== AURORA (flowing background blobs) ===== */
.aurora{position:fixed; inset:0; z-index:-1; overflow:hidden; filter:blur(70px); pointer-events:none;}
.aurora span{position:absolute; border-radius:50%; mix-blend-mode:screen; opacity:.5;}
.aurora .a1{width:52vw; height:52vw; top:-16vw; left:-12vw; background:var(--green); animation:drift1 34s ease-in-out infinite alternate, morph 18s ease-in-out infinite;}
.aurora .a2{width:42vw; height:42vw; bottom:-12vw; right:-10vw; background:var(--navy); animation:drift2 28s ease-in-out infinite alternate, morph 22s ease-in-out infinite;}
.aurora .a3{width:30vw; height:30vw; top:34%; left:58%; background:var(--green-soft); animation:drift3 40s ease-in-out infinite alternate, morph 26s ease-in-out infinite;}
@keyframes drift1{0%{transform:translate(0,0) scale(1);} 100%{transform:translate(7vw,9vw) scale(1.15);}}
@keyframes drift2{0%{transform:translate(0,0) scale(1);} 100%{transform:translate(-8vw,-6vw) scale(1.12);}}
@keyframes drift3{0%{transform:translate(0,0) scale(1);} 100%{transform:translate(-5vw,8vw) scale(1.2);}}
@keyframes morph{0%{border-radius:50% 50% 50% 50%;} 50%{border-radius:42% 58% 54% 46%;} 100%{border-radius:50% 50% 50% 50%;}}

/* ===== HEADER / NAV (floating glass pill) ===== */
#hdr{position:fixed; top:18px; left:50%; transform:translateX(-50%); z-index:100; width:min(94vw, 1180px);}
#hdr .nav-wrap{
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 10px 10px 24px; transition:box-shadow .3s;
}
#hdr.scrolled .nav-wrap{box-shadow:inset 0 1px 0 rgba(255,255,255,.22), 0 24px 70px rgba(0,0,0,.6);}
.logo-link img{height:30px;}
.nav-links{display:flex; align-items:center; gap:6px;}
.nav-links a{
  font-family:var(--ff-head); font-size:13px; font-weight:700; letter-spacing:.02em;
  color:var(--text); padding:10px 16px; border-radius:var(--radius-pill); transition:background .2s, color .2s;
}
.nav-links a:hover{background:rgba(255,255,255,.08); color:var(--white);}
.nav-links a.active{background:var(--green); color:var(--bg); box-shadow:0 0 18px var(--green-glow);}
.nav-ctas{display:flex; align-items:center; gap:10px;}
.hbg{display:none; background:none; border:none; color:var(--white); cursor:pointer; padding:8px;}

.btn-out,.btn-fill,.btn-grn,.btn-hero,.btn-wht,.btn-sub{
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  font-family:var(--ff-head); font-size:13px; font-weight:800; letter-spacing:.03em;
  border-radius:var(--radius-pill); padding:13px 26px; border:1.5px solid transparent;
  cursor:pointer; position:relative; overflow:hidden; transition:transform .25s, box-shadow .25s;
}
.btn-out{border-color:rgba(255,255,255,.25); color:var(--text);}
.btn-out:hover{border-color:var(--green); color:var(--green);}
.btn-fill,.btn-grn,.btn-hero,.btn-sub{background:var(--green); color:var(--bg); box-shadow:0 0 24px var(--green-glow);}
.btn-wht{background:var(--white); color:var(--bg);}
.btn-fill:hover,.btn-grn:hover,.btn-hero:hover,.btn-sub:hover,.btn-wht:hover{transform:translateY(-2px); box-shadow:0 8px 30px var(--green-glow);}
.btn-hero-out{display:inline-flex; align-items:center; gap:8px; font-family:var(--ff-head); font-weight:800; font-size:13px; letter-spacing:.03em; color:var(--white); border:1.5px solid rgba(255,255,255,.35); border-radius:var(--radius-pill); padding:13px 26px;}
.btn-hero-out:hover{border-color:var(--white); background:rgba(255,255,255,.08);}

/* glass ripple on click */
.btn-out,.btn-fill,.btn-grn,.btn-hero,.btn-wht,.btn-sub,.btn-hero-out{ -webkit-tap-highlight-color:transparent; }
.ripple{position:absolute; border-radius:50%; background:rgba(255,255,255,.5); transform:scale(0); animation:ripple-anim .6s ease-out; pointer-events:none;}
@keyframes ripple-anim{to{transform:scale(3); opacity:0;}}

/* ===== HERO (home) ===== */
.hero{position:relative; min-height:96vh; display:flex; align-items:center; overflow:hidden;}
.hero-media{position:absolute; inset:0; z-index:0;}
.hero-media img{width:100%; height:100%; object-fit:cover;}
.hero::before{content:''; position:absolute; inset:0; z-index:1; background:linear-gradient(115deg, var(--bg) 18%, rgba(10,10,12,.55) 55%, rgba(10,10,12,.15) 100%);}
.hero-cnt{position:relative; z-index:2; max-width:1180px; margin:0 auto; padding:160px 24px 0;}
.hero-cnt h1{font-size:clamp(36px,6vw,72px); margin:18px 0 22px;}
.hero-cnt p{max-width:520px; font-size:17px; color:var(--text); margin-bottom:34px;}
.hero-btns{display:flex; gap:14px; flex-wrap:wrap;}

/* page hero (sub-pages) */
.page-hero-v6{position:relative; min-height:56vh; display:flex; align-items:center; background-size:cover; background-position:center; overflow:hidden;}
.page-hero-v6::before{content:''; position:absolute; inset:0; background:linear-gradient(115deg, var(--bg) 15%, rgba(10,10,12,.6) 60%, rgba(10,10,12,.2) 100%);}
.page-hero-v6-cnt{position:relative; z-index:1; max-width:1180px; margin:0 auto; padding:170px 24px 60px;}
.page-hero-v6-cnt h1{font-size:clamp(32px,5vw,56px); margin:14px 0 16px;}
.page-hero-v6-cnt p{max-width:560px; color:var(--text);}

/* ===== MARQUEE ===== */
.marquee{background:var(--bg2); border-top:1px solid var(--glass-border); border-bottom:1px solid var(--glass-border); overflow:hidden; white-space:nowrap; padding:18px 0;}
.marquee-track{display:inline-flex; animation:marquee 26s linear infinite;}
.marquee-track span{font-family:var(--ff-head); font-weight:700; font-size:14px; letter-spacing:.04em; padding:0 14px; color:var(--text);}
.marquee-track .dot{color:var(--green); text-shadow:0 0 8px var(--green-glow);}
@keyframes marquee{from{transform:translateX(0);} to{transform:translateX(-50%);}}

/* ===== STAT BAND ===== */
.stat-band{padding:70px 0; background:var(--bg);}
.stat-grid{max-width:1180px; margin:0 auto; padding:0 24px; display:grid; grid-template-columns:repeat(4,1fr); gap:24px;}
.stat{text-align:center;}
.stat-n{font-family:var(--ff-head); font-weight:900; font-size:clamp(32px,4vw,48px); color:var(--white);}
.stat-l{font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:6px;}

/* ===== ABOUT ===== */
.about-split{display:grid; grid-template-columns:1fr 1fr; gap:60px; align-items:center;}
.about-split h2{font-size:clamp(28px,3.6vw,44px);}
.about-rt p{font-size:16px; color:var(--text); margin-bottom:20px;}
.about-link{display:inline-flex; align-items:center; gap:8px; font-family:var(--ff-head); font-size:12.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:var(--green);}
.bee{display:inline-flex; align-items:center; gap:8px; margin-top:22px; font-size:13px; color:var(--text);}

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

/* ===== TESTIMONIALS ===== */
.testi-card{display:none; padding:36px; max-width:760px;}
.testi-card.active{display:block;}
.testi-card p{font-size:20px; color:var(--white); margin-bottom:18px;}
.testi-name{font-family:var(--ff-head); font-weight:800; color:var(--green); margin-right:10px;}
.testi-role{font-size:13px; color:var(--muted);}
.testi-ctrls{display:flex; align-items:center; justify-content:space-between; max-width:760px; margin-top:10px;}
.testi-count{font-family:var(--ff-head); font-size:12px; color:var(--muted); letter-spacing:.08em;}
.testi-arrow{width:38px; height:38px; border-radius:50%; border:1px solid var(--glass-border); background:var(--glass); color:var(--white); cursor:pointer;}
.testi-arrow:hover{border-color:var(--green); color:var(--green);}

/* ===== TEAM BAND ===== */
.team-band{position:relative; background-size:cover; background-position:center; padding:140px 0; background-color:var(--bg2);}
.team-band::before{content:''; position:absolute; inset:0; background:linear-gradient(115deg, rgba(10,10,12,.92) 30%, rgba(10,10,12,.45) 100%);}
.team-band-cnt{position:relative; z-index:1; max-width:1180px; margin:0 auto; padding:0 24px;}
.team-band-cnt h2{font-size:clamp(28px,3.6vw,44px); margin:14px 0 18px;}
.team-band-cnt p{max-width:520px; color:var(--text); margin-bottom:28px;}

/* ===== GALLERY (home marquee teaser + full galleries page) ===== */
.gal-marquee{overflow:hidden;}
.gal-track{display:flex; gap:16px; animation:gal-scroll 50s linear infinite;}
.gal-track figure{margin:0; position:relative; overflow:hidden; flex:0 0 auto; width:300px; height:210px; border-radius:var(--radius-card); border:1px solid var(--glass-border);}
.gal-track figure img{width:100%; height:100%; object-fit:cover;}
.gal-track figure.wide{width:420px;}
@keyframes gal-scroll{from{transform:translateX(0);} to{transform:translateX(-50%);}}

.gal-tabs{display:flex; gap:10px; margin-bottom:36px;}
.gal-tab-btn{font-family:var(--ff-head); font-size:12.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; background:var(--glass); backdrop-filter:blur(14px); color:var(--text); border:1px solid var(--glass-border); padding:13px 24px; border-radius:var(--radius-pill); cursor:pointer;}
.gal-tab-btn:hover{border-color:var(--green); color:var(--white);}
.gal-tab-btn.active{background:var(--green); color:var(--bg); border-color:var(--green); box-shadow:0 0 20px var(--green-glow);}
.gal-panel{display:none;}
.gal-panel.active{display:block;}
.gallery-grid{display:grid; grid-template-columns:repeat(4,1fr); grid-auto-rows:200px; gap:16px;}
.gallery-grid figure{margin:0; position:relative; overflow:hidden; border-radius:var(--radius-card); border:1px solid var(--glass-border); cursor:pointer; background:var(--bg2);}
.gallery-grid figure img{width:100%; height:100%; object-fit:cover; transition:transform .4s;}
.gallery-grid figure:hover img{transform:scale(1.06);}
.gallery-grid figure.wide{grid-column:span 2;}
.gallery-grid figure.tall{grid-row:span 2;}

.lightbox{position:fixed; inset:0; z-index:200; background:rgba(5,5,7,.92); display:none; align-items:center; justify-content:center;}
.lightbox.open{display:flex;}
.lightbox img{max-width:88vw; max-height:84vh; border-radius:var(--radius-card);}
.lb-close,.lb-prev,.lb-next{position:absolute; background:var(--glass); backdrop-filter:blur(14px); border:1px solid var(--glass-border); color:var(--white); border-radius:50%; width:46px; height:46px; cursor:pointer; font-size:20px;}
.lb-close{top:24px; right:24px;}
.lb-prev{left:24px; top:50%; transform:translateY(-50%);}
.lb-next{right:24px; top:50%; transform:translateY(-50%);}
.lb-count{position:absolute; bottom:24px; left:50%; transform:translateX(-50%); color:var(--muted); font-family:var(--ff-head); font-size:13px;}

/* ===== TAILORED SOLUTIONS GRID ===== */
.tlr-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:24px;}
.tlr-card{border-radius:var(--radius-card); overflow:hidden; border:1px solid var(--glass-border); background:var(--bg2); transition:transform .3s, border-color .3s;}
.tlr-card:hover{transform:translateY(-4px); border-color:var(--green);}
.tlr-card .tlr-img{height:220px; background-size:cover; background-position:center;}
.tlr-card .tlr-body{padding:26px;}
.tlr-card h3{font-size:20px; margin-bottom:10px;}
.tlr-card p{font-size:14.5px; color:var(--text);}

/* ===== CTA ===== */
.cta-v6{position:relative; padding:140px 0; text-align:center; overflow:hidden;}
.cta-v6-inner h2{font-size:clamp(30px,4vw,52px); margin:14px 0 30px;}

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

/* ===== COOKIE BANNER / WHATSAPP FAB ===== */
.cookie-banner{position:fixed; bottom:24px; left:24px; right:24px; max-width:600px; margin:0 auto; z-index:150; background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%); border:1px solid var(--glass-border); border-radius:var(--radius-card); padding:22px 26px; transform:translateY(140%); transition:transform .4s ease; box-shadow:0 20px 60px rgba(0,0,0,.5);}
.cookie-banner.show{transform:translateY(0);}
.cookie-banner p{font-size:13px; color:var(--text); margin-bottom:14px;}
.cookie-banner-btns{display:flex; gap:10px; justify-content:flex-end;}
.cb-decline,.cb-accept{font-family:var(--ff-head); font-size:12px; font-weight:800; padding:9px 18px; border-radius:var(--radius-pill); cursor:pointer; border:1px solid var(--glass-border); background:transparent; color:var(--text);}
.cb-accept{background:var(--green); color:var(--bg); border-color:var(--green);}

.wa-fab{position:fixed; bottom:24px; right:24px; z-index:140; display:flex; align-items:center; gap:10px; background:#1faa55; color:var(--white); padding:14px 18px; border-radius:var(--radius-pill); box-shadow:0 10px 30px rgba(31,170,85,.5);}
.wa-pulse{position:absolute; inset:0; border-radius:var(--radius-pill); background:#1faa55; animation:wa-pulse 2.4s ease-out infinite; z-index:-1;}
@keyframes wa-pulse{0%{transform:scale(1); opacity:.6;} 100%{transform:scale(1.6); opacity:0;}}
.wa-label{font-family:var(--ff-head); font-size:13px; font-weight:700;}

/* ===== MODAL (fleet specs) ===== */
.modal-backdrop{position:fixed; inset:0; z-index:200; background:rgba(5,5,7,.8); display:none; align-items:center; justify-content:center; padding:24px;}
.modal-backdrop.open{display:flex;}
.modal-card{max-width:760px; max-height:88vh; overflow-y:auto; background:var(--bg2); border:1px solid var(--glass-border); border-radius:var(--radius-card); display:grid; grid-template-columns:1fr 1fr;}
.modal-img{position:relative; background-size:cover; background-position:center; min-height:280px;}
.modal-tag{position:absolute; top:16px; left:16px; background:var(--green); color:var(--bg); font-family:var(--ff-head); font-weight:800; font-size:11px; padding:6px 12px; border-radius:var(--radius-pill);}
.modal-close{position:absolute; top:14px; right:14px; width:34px; height:34px; border-radius:50%; background:rgba(10,10,12,.6); color:var(--white); border:none; font-size:18px; cursor:pointer;}
.modal-body{padding:32px;}
.modal-cap{font-size:12.5px; color:var(--green); font-weight:700; margin:6px 0 16px;}
.modal-desc{font-size:14.5px; color:var(--text); margin-bottom:20px;}
.spec-table{width:100%; font-size:13.5px; margin-bottom:20px;}
.spec-table td{padding:7px 0; border-bottom:1px solid var(--glass-border);}
.spec-table td:first-child{color:var(--muted);}
.spec-table td:last-child{text-align:right; color:var(--white); font-weight:600;}
.use-cases{display:flex; gap:8px; flex-wrap:wrap; margin-bottom:22px;}
.use-cases span{font-size:11.5px; background:rgba(255,255,255,.08); padding:5px 12px; border-radius:var(--radius-pill); color:var(--text);}

/* ===== FORMS (contact page) ===== */
.quick-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:20px;}
.qc-card{background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%); border:1px solid var(--glass-border); border-radius:var(--radius-card); padding:30px; transition:border-color .3s, transform .3s;}
.qc-card:hover{border-color:var(--green); transform:translateY(-4px);}
.wa-cta{display:inline-flex; align-items:center; gap:8px; background:var(--green); color:var(--bg); padding:12px 20px; font-family:var(--ff-head); font-size:12.5px; font-weight:800; letter-spacing:.04em; border-radius:var(--radius-pill);}
.signup-band{background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%); border:1px solid var(--glass-border); border-radius:var(--radius-card); display:flex; align-items:center; justify-content:space-between; gap:30px; padding:34px 38px; flex-wrap:wrap;}
.signup-form{display:flex; gap:10px;}
.signup-form input{background:rgba(0,0,0,.3); border:1px solid var(--glass-border); color:var(--white); padding:13px 16px; border-radius:var(--radius-pill); font-family:var(--ff-body); min-width:240px;}
.signup-form button{font-family:var(--ff-head); font-weight:800; font-size:12.5px; background:var(--green); color:var(--bg); border:none; padding:13px 22px; border-radius:var(--radius-pill); cursor:pointer;}
.quote-grid{display:grid; grid-template-columns:1fr 1fr; gap:50px; align-items:start;}
.form{padding:34px;}
.f-row{display:grid; grid-template-columns:1fr 1fr; gap:16px;}
.f-field{margin-bottom:16px;}
.f-field label{display:block; font-size:12px; color:var(--muted); margin-bottom:6px;}
.f-field input,.f-field select,.f-field textarea{width:100%; background:rgba(0,0,0,.3); border:1px solid var(--glass-border); color:var(--white); padding:13px 16px; border-radius:16px; font-family:var(--ff-body); font-size:14.5px;}
.f-field textarea{min-height:100px; resize:vertical;}
.f-field input:focus,.f-field select:focus,.f-field textarea:focus{outline:none; border-color:var(--green);}
.map-wrap{border-radius:var(--radius-card); overflow:hidden; border:1px solid var(--glass-border); height:360px;}
.map-wrap iframe{width:100%; height:100%; border:0;}
.team-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:20px;}
.team-card{background:var(--glass); backdrop-filter:blur(18px); border:1px solid var(--glass-border); border-radius:var(--radius-card); padding:24px;}
.team-card h4{font-size:17px; margin-bottom:4px;}
.team-role{font-size:12px; color:var(--green); text-transform:uppercase; letter-spacing:.06em; margin-bottom:10px;}
.team-card p{font-size:13.5px; color:var(--muted);}
.sub-hd{font-family:var(--ff-head); font-weight:800; font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--green); margin-bottom:18px;}

/* ===== RESPONSIVE ===== */
@media (max-width:900px){
  .about-split,.ind-split,.quote-grid{grid-template-columns:1fr;}
  .cap-grid{grid-template-columns:repeat(2,1fr);}
  .cap-feature{grid-row:span 1;}
  .fleet-card-grid,.fleet-card-grid.sm,.quick-grid,.team-grid,.tlr-grid{grid-template-columns:repeat(2,1fr);}
  .gallery-grid{grid-template-columns:repeat(2,1fr);}
  .gallery-grid figure.wide{grid-column:span 2;}
  .ft-top{grid-template-columns:1fr 1fr;}
  .modal-card{grid-template-columns:1fr;}
  .f-row{grid-template-columns:1fr;}
}
@media (max-width:640px){
  .hbg{display:block;}
  .nav-links{position:fixed; top:80px; left:16px; right:16px; flex-direction:column; align-items:stretch; padding:16px; display:none;
    background:linear-gradient(160deg, var(--glass-hi), var(--glass)); backdrop-filter:blur(22px) saturate(160%); border:1px solid var(--glass-border); border-radius:var(--radius-card);}
  .nav-links.open{display:flex;}
  .nav-ctas{display:none;}
  .stat-grid,.cap-grid,.fleet-card-grid,.fleet-card-grid.sm,.quick-grid,.team-grid,.tlr-grid,.gallery-grid{grid-template-columns:1fr;}
  .gallery-grid figure.wide{grid-column:span 1;}
  .ft-top{grid-template-columns:1fr;}
}
```

- [ ] **Step 3: Write `style-guide.html` smoke test**

```html
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Style Guide</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head><body>
<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>
<header id="hdr"><div class="nav-wrap glass glass-pill">
  <a href="#" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes"></a>
  <nav class="nav-links"><a href="#" class="active">Home</a><a href="#">Fleet</a></nav>
  <div class="nav-ctas"><a href="#" class="btn-out">Call</a><a href="#" class="btn-fill">Get a Quote</a></div>
</div></header>
<section class="sec" style="padding-top:200px;">
  <div class="sec-inner">
    <span class="eyebrow">Style Guide</span>
    <h2 class="hl">Glass Card Example</h2>
    <div class="glass" style="padding:30px; max-width:420px; margin-top:20px;">
      <p>This is a frosted glass panel over the aurora background.</p>
      <a href="#" class="btn-grn" style="margin-top:16px;">Button</a>
    </div>
  </div>
</section>
</body></html>
```

- [ ] **Step 4: Verify with Playwright**

Use `mcp__plugin_playwright_playwright__browser_navigate` to open the local `style-guide.html` file (`file:///C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6/style-guide.html`), then `mcp__plugin_playwright_playwright__browser_take_screenshot`.

Expected: dark background with two soft colored (green/navy) blurred blobs drifting, a pill-shaped translucent nav bar with logo + active green pill link, and a frosted glass card with visible top-edge highlight and a green pill button. Also run `mcp__plugin_playwright_playwright__browser_console_messages` — expected: no errors (404s for the logo are acceptable at this step since `script.js` doesn't exist yet, but there must be no CSS parse errors).

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6"
git add style.css style-guide.html Logos favicon-16.png favicon-32.png favicon-180.png favicon.ico "Cinematic Images" images
git commit -m "Add design tokens, glass/aurora CSS system, and copied asset pool"
```

---

### Task 2: Shared `script.js`

**Files:**
- Create: `chimes-mockup-v6/script.js`

**Interfaces:**
- Consumes: DOM ids/classes defined in Task 1 CSS (`#hdr`, `.nav-links`, `.hbg`, `.fu`, `.stat-n[data-to]`, `.ind-li`, `.testi-slide`, `.gal-tab-btn`, `.gal-panel`, `.modal-backdrop`, `.cookie-banner`).
- Produces global functions later page tasks call inline via `onclick`/`onsubmit`: `openModal(id)`, `closeModal(id)`, `setIndustry(key)`, `switchGalTab(key)`, `handleForm(event)`, `handleSignup(event)`.

- [ ] **Step 1: Write `script.js`** (adapted from v4's behavior — same function names/contracts, dark-glass site has no splash/page-transition curtain per the new design, so that part of v4's script is dropped)

```js
// Chimes Crane Hire — Mockup v6 shared behaviour

// Header scroll state
const hdr = document.getElementById('hdr');
if (hdr) window.addEventListener('scroll', () => hdr.classList.toggle('scrolled', scrollY > 20));

// Mobile nav toggle
const hbg = document.getElementById('hbg');
if (hbg) hbg.addEventListener('click', () => document.getElementById('nav').classList.toggle('open'));

// Fade-up on scroll
const fus = document.querySelectorAll('.fu');
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); }
  });
}, { threshold: 0.12 });
fus.forEach(el => io.observe(el));

// Count-up for stats
function countUp(el, target, suffix) {
  let v = 0;
  const step = target / 60;
  const t = setInterval(() => {
    v = Math.min(v + step, target);
    el.textContent = Math.floor(v) + suffix;
    if (v >= target) clearInterval(t);
  }, 22);
}
const sio = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const t = parseInt(e.target.dataset.to);
      const suffix = e.target.dataset.suffix !== undefined ? e.target.dataset.suffix : '+';
      if (t) countUp(e.target, t, suffix);
      sio.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-n[data-to]').forEach(el => sio.observe(el));

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

// Testimonial carousel
const testiSlides = document.querySelectorAll('.testi-slide');
const testiCount = document.getElementById('testiCount');
let testiIdx = 0;
function showTesti(i) {
  testiIdx = (i + testiSlides.length) % testiSlides.length;
  testiSlides.forEach((s, idx) => s.classList.toggle('active', idx === testiIdx));
  if (testiCount) testiCount.textContent = String(testiIdx + 1).padStart(2, '0') + ' / ' + String(testiSlides.length).padStart(2, '0');
}
document.getElementById('testiNext')?.addEventListener('click', () => showTesti(testiIdx + 1));
document.getElementById('testiPrev')?.addEventListener('click', () => showTesti(testiIdx - 1));

// Fleet spec modal
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) { modal.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) { modal.classList.remove('open'); document.body.style.overflow = ''; }
}
document.querySelectorAll('.modal-backdrop').forEach(m => {
  m.addEventListener('click', (e) => { if (e.target === m) closeModal(m.id); });
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') document.querySelectorAll('.modal-backdrop.open').forEach(m => closeModal(m.id));
});

// Quote form demo submit
function handleForm(e) {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-sub');
  if (!btn) return;
  const original = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;
  setTimeout(() => {
    btn.textContent = 'Request Sent!';
    e.target.reset();
    setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 3000);
  }, 1200);
}

// Newsletter signup demo
function handleSignup(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const original = btn.textContent;
  btn.textContent = 'Subscribed!';
  e.target.reset();
  setTimeout(() => { btn.textContent = original; }, 2500);
}

// Galleries page: tabs
function switchGalTab(key) {
  document.querySelectorAll('.gal-tab-btn').forEach(el => el.classList.toggle('active', el.dataset.tab === key));
  document.querySelectorAll('.gal-panel').forEach(el => el.classList.toggle('active', el.id === 'panel-' + key));
}
document.querySelectorAll('.gal-tab-btn').forEach(btn => {
  btn.addEventListener('click', () => switchGalTab(btn.dataset.tab));
});

// Galleries page: lightbox
const lightbox = document.getElementById('lightbox');
if (lightbox) {
  const lbImg = document.getElementById('lbImg');
  const lbCount = document.getElementById('lbCount');
  let lbList = [];
  let lbIdx = 0;
  function showLb(i) {
    lbIdx = (i + lbList.length) % lbList.length;
    lbImg.src = lbList[lbIdx].src;
    lbImg.alt = lbList[lbIdx].alt;
    lbCount.textContent = String(lbIdx + 1).padStart(2, '0') + ' / ' + String(lbList.length).padStart(2, '0');
  }
  function openLb(panel, index) {
    lbList = [...panel.querySelectorAll('img')];
    showLb(index);
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeLb() { lightbox.classList.remove('open'); document.body.style.overflow = ''; }
  document.querySelectorAll('.gal-panel').forEach(panel => {
    panel.querySelectorAll('figure').forEach((fig, i) => fig.addEventListener('click', () => openLb(panel, i)));
  });
  document.getElementById('lbClose')?.addEventListener('click', closeLb);
  document.getElementById('lbPrev')?.addEventListener('click', () => showLb(lbIdx - 1));
  document.getElementById('lbNext')?.addEventListener('click', () => showLb(lbIdx + 1));
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLb(); });
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowLeft') showLb(lbIdx - 1);
    if (e.key === 'ArrowRight') showLb(lbIdx + 1);
  });
}

// Cookie banner
const COOKIE_KEY = 'chimes_cookie_consent';
const cookieBanner = document.getElementById('cookieBanner');
if (cookieBanner && !localStorage.getItem(COOKIE_KEY)) {
  requestAnimationFrame(() => requestAnimationFrame(() => cookieBanner.classList.add('show')));
}
document.getElementById('cbAccept')?.addEventListener('click', () => { localStorage.setItem(COOKIE_KEY, 'accepted'); cookieBanner.classList.remove('show'); });
document.getElementById('cbDecline')?.addEventListener('click', () => { localStorage.setItem(COOKIE_KEY, 'declined'); cookieBanner.classList.remove('show'); });

// Glass ripple on buttons
document.querySelectorAll('.btn-out,.btn-fill,.btn-grn,.btn-hero,.btn-wht,.btn-sub').forEach(btn => {
  btn.addEventListener('click', function (e) {
    const r = document.createElement('span');
    r.className = 'ripple';
    const rect = this.getBoundingClientRect();
    r.style.left = (e.clientX - rect.left) + 'px';
    r.style.top = (e.clientY - rect.top) + 'px';
    this.appendChild(r);
    setTimeout(() => r.remove(), 650);
  });
});
```

- [ ] **Step 2: Add `script.js` to `style-guide.html` and re-verify**

Add `<script src="script.js"></script>` before `</body>` in `style-guide.html`. Click the `.btn-grn` button via `mcp__plugin_playwright_playwright__browser_click`, then `mcp__plugin_playwright_playwright__browser_take_screenshot` immediately after.

Expected: a brief white ripple circle expanding from the click point inside the button (the `.ripple` animation). Run `mcp__plugin_playwright_playwright__browser_console_messages` — expected: no JS errors.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6"
git add script.js style-guide.html
git commit -m "Add shared script.js (nav, reveal, modal, gallery, ripple behavior)"
```

---

### Task 3: Hero static image — extract a real frame from the source video

**Files:**
- Create: `chimes-mockup-v6/scripts/sample_hero_frames.py`
- Create: `chimes-mockup-v6/scripts/extract_hero_frame.py`
- Create: `chimes-mockup-v6/Cinematic Images/hero-still.jpg`

**Interfaces:**
- Produces: `Cinematic Images/hero-still.jpg`, consumed by `index.html`'s `.hero-media img` in Task 4.

- [ ] **Step 1: Install the one-off extraction dependency**

```bash
python3 -m pip install --quiet opencv-python-headless
python3 -c "import cv2; print(cv2.__version__)"
```

Expected: prints a version number (e.g. `4.x.x`), no `ModuleNotFoundError`.

- [ ] **Step 2: Write the candidate sampler**

```python
# scripts/sample_hero_frames.py
import cv2
import os

SRC = r"C:\Users\micha\OneDrive\Desktop\Chimes Work\Source Assets\Must Use Content\Top body video.mp4"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "_frame_candidates")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cap = cv2.VideoCapture(SRC)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    print(f"Total frames: {total}, fps: {fps:.2f}, duration: {total/fps:.1f}s")
    for pct in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]:
        frame_no = int(total * pct)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ok, frame = cap.read()
        if not ok:
            print(f"FAILED at {pct}")
            continue
        out_path = os.path.join(OUT_DIR, f"candidate_{int(pct*100)}pct.jpg")
        cv2.imwrite(out_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"Saved {out_path} (frame {frame_no}, {frame_no/fps:.1f}s)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the sampler and view each candidate**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6"
python3 scripts/sample_hero_frames.py
```

Expected: 10 JPEGs in `_frame_candidates/`, plus a printed total-frames/fps/duration line. Then view each of the 10 files (the Read tool renders images) and pick the one where the crane truck is most clearly and fully in frame, well-lit, and visually striking — this is the verification step for this task; there is no automated pass/fail, the implementer must look and choose.

- [ ] **Step 4: Write the final single-frame extractor using the chosen percentage**

```python
# scripts/extract_hero_frame.py
import cv2
import os
import sys

SRC = r"C:\Users\micha\OneDrive\Desktop\Chimes Work\Source Assets\Must Use Content\Top body video.mp4"
OUT = os.path.join(os.path.dirname(__file__), "..", "Cinematic Images", "hero-still.jpg")

# Set to the percentage chosen in Step 3 after viewing the 10 candidates.
CHOSEN_PCT = 0.45  # placeholder until Step 3's visual review picks the real value

def main():
    cap = cv2.VideoCapture(SRC)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_no = int(total * CHOSEN_PCT)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ok, frame = cap.read()
    if not ok:
        sys.exit(f"Failed to read frame {frame_no}")
    cv2.imwrite(OUT, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"Saved {OUT} from frame {frame_no} ({CHOSEN_PCT*100:.0f}%)")

if __name__ == "__main__":
    main()
```

Before running: edit `CHOSEN_PCT` to match the candidate selected by visual review in Step 3 (e.g. if `candidate_65pct.jpg` was the best, set `CHOSEN_PCT = 0.65`).

- [ ] **Step 5: Run it, verify, and clean up candidates**

```bash
python3 scripts/extract_hero_frame.py
```

Expected: `Cinematic Images/hero-still.jpg` exists. View it with Read to confirm it matches the chosen candidate. Then remove the scratch candidates (not part of the deliverable):

```bash
rm -rf _frame_candidates
```

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6"
git add scripts "Cinematic Images/hero-still.jpg"
git commit -m "Extract static hero frame from source video (replaces autoplay video for performance)"
```

---

### Task 4: `index.html` (home page)

**Files:**
- Create: `chimes-mockup-v6/index.html`

**Interfaces:**
- Consumes: `style.css` classes from Task 1, `script.js` functions from Task 2, `Cinematic Images/hero-still.jpg` from Task 3.
- Shares the nav/footer block verbatim (same markup, different `class="active"` placement) with Tasks 6–8. Nav order, fixed across every page: Home, Fleet & Specs, Tailored Solutions, Galleries, Who We Are, Contact.

Content is restructured from `chimes-mockup-v4/index.html` (sections: hero, marquee, stats, about, capabilities, industries, fleet teaser, testimonials, team band, gallery teaser, CTA, footer) into the new glass classes. Copy text is carried over verbatim from v4; the autoplay `<video>` is replaced with the static `hero-still.jpg`.

- [ ] **Step 1: Write `index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chimes Crane Hire — Gauteng's Trusted Crane Hire Experts</title>
<meta name="description" content="Chimes Crane Hire — owner-managed Tadano crane hire in Germiston, Johannesburg since 2003. 8 to 400 ton fleet, certified operators, BEE Level 4.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="favicon-180.png">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>

<header id="hdr">
  <div class="nav-wrap glass glass-pill">
    <a href="index.html" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire"></a>
    <button class="hbg" id="hbg" aria-label="Menu">
      <svg width="22" height="15" viewBox="0 0 22 15" fill="none"><rect y="0" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="6" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="12" width="22" height="2.5" rx="1" fill="currentColor"/></svg>
    </button>
    <nav class="nav-links" id="nav">
      <a href="index.html" class="active">Home</a>
      <a href="fleet.html">Fleet &amp; Specs</a>
      <a href="tailored-solutions.html">Tailored Solutions</a>
      <a href="galleries.html">Galleries</a>
      <a href="index.html#about">Who We Are</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-ctas">
      <a href="tel:+27116261110" class="btn-out">+27 11 626 1110</a>
      <a href="contact.html#quote" class="btn-fill">Get a Quote</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="hero-media"><img src="Cinematic%20Images/hero-still.jpg" alt="Chimes crane truck on site" loading="eager"></div>
  <div class="hero-cnt">
    <span class="eyebrow">Mobile Crane Hire &middot; Est. 2003 &middot; Gauteng</span>
    <h1>We Lift.<br>South Africa <span class="hl">Builds.</span></h1>
    <p>A new standard in mobile crane hire — engineered fleet, expert crews, and a Tadano fleet built to move the country forward.</p>
    <div class="hero-btns">
      <a href="contact.html#quote" class="btn-hero">Start A Project</a>
      <a href="fleet.html" class="btn-hero-out">Our Fleet</a>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>Steel</span><span class="dot">&middot;</span><span>Construction</span><span class="dot">&middot;</span><span>Mining</span><span class="dot">&middot;</span><span>Petrochemical</span><span class="dot">&middot;</span><span>Telecoms</span><span class="dot">&middot;</span><span>Renewables</span><span class="dot">&middot;</span><span>Industrial</span><span class="dot">&middot;</span>
    <span>Steel</span><span class="dot">&middot;</span><span>Construction</span><span class="dot">&middot;</span><span>Mining</span><span class="dot">&middot;</span><span>Petrochemical</span><span class="dot">&middot;</span><span>Telecoms</span><span class="dot">&middot;</span><span>Renewables</span><span class="dot">&middot;</span><span>Industrial</span><span class="dot">&middot;</span>
  </div>
</div>

<div class="stat-band">
  <div class="stat-grid">
    <div class="stat fu"><div class="stat-n" data-to="2003" data-suffix="">0</div><div class="stat-l">Established</div></div>
    <div class="stat fu"><div class="stat-n" data-to="20" data-suffix="+">0</div><div class="stat-l">Cranes In Fleet</div></div>
    <div class="stat fu"><div class="stat-n" data-to="400" data-suffix="T">0</div><div class="stat-l">Max Capacity</div></div>
    <div class="stat fu"><div class="stat-n" data-to="24" data-suffix="/7">0</div><div class="stat-l">Always On Call</div></div>
  </div>
</div>

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

<section class="sec alt" id="fleet-showcase">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Built To Lift Anything</span><h2>Our Fleet</h2></div>
    <div class="fleet-card-grid fu">
      <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-400t.jpg');"><span class="fc-sub">Tadano ATF 400G-6</span><div class="fc-tag"><div class="fc-class">Heavy &middot; 400T</div><div class="fc-name">Our flagship — major lifts, max reach</div></div></a>
      <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-220t.jpg');"><span class="fc-sub">126m With Jib</span><div class="fc-tag"><div class="fc-class">Premium &middot; 220T</div><div class="fc-name">Refinery &amp; power plant operations</div></div></a>
      <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-90t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Mid &middot; 90T</div><div class="fc-name">The versatile workhorse</div></div></a>
      <a class="fc" href="fleet.html" style="background-image:url('images/fleet/chimes-8-15t-truck.jpg');"><span class="fc-sub">Truck Mount</span><div class="fc-tag"><div class="fc-class">Compact &middot; 8&ndash;15T</div><div class="fc-name">Agile, tight-access lifting</div></div></a>
    </div>
    <div style="text-align:center; margin-top:44px;"><a href="fleet.html" class="btn-grn">View Full Fleet &amp; Specifications</a></div>
  </div>
</section>

<section class="sec" id="testimonials">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">What Clients Say</span><h2>Trusted On Site.</h2></div>
    <div class="glass fu">
      <div class="testi-card testi-slide active"><p>&ldquo;Chimes' crews showed up on time, on spec, and ran the lift exactly as planned. No surprises, no delays — that's rare in this industry.&rdquo;</p><span class="testi-name">Site Manager</span><span class="testi-role">Construction Client, Gauteng</span></div>
      <div class="testi-card testi-slide"><p>&ldquo;We needed a 220-ton lift on a tight refinery shutdown window. Chimes planned the rigging, hit the schedule, and kept the site safe throughout.&rdquo;</p><span class="testi-name">Projects Lead</span><span class="testi-role">Petrochemical Client</span></div>
      <div class="testi-card testi-slide"><p>&ldquo;Owner-managed really does make a difference — when we call, we're talking to someone who can actually make decisions on the spot.&rdquo;</p><span class="testi-name">Operations Manager</span><span class="testi-role">Mining Client</span></div>
      <div class="testi-ctrls" style="padding:0 36px 30px;">
        <span class="testi-count" id="testiCount">01 / 03</span>
        <div style="display:flex; gap:8px;"><button class="testi-arrow" id="testiPrev" aria-label="Previous testimonial">&larr;</button><button class="testi-arrow" id="testiNext" aria-label="Next testimonial">&rarr;</button></div>
      </div>
    </div>
  </div>
</section>

<div class="team-band" style="background-image:url('Cinematic%20Images/Chimes%20Team%20%231.jpg');">
  <div class="team-band-cnt fu">
    <span class="eyebrow">Our People</span>
    <h2>Trained Operators.<br>Every Time, Every <span class="hl">Lift.</span></h2>
    <p>Every Chimes crane comes with a certified operator, rigger, and safety officer. We don't just hire equipment — we deliver complete lifting solutions, safely and on time.</p>
    <a href="contact.html#team" class="btn-wht">Meet The Team</a>
  </div>
</div>

<section class="sec alt" id="gallery" style="padding-bottom:80px;">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">On Site</span><h2>From Our Yard To The Lift.</h2></div>
    <div class="gal-marquee fu"><div class="gal-track">
      <figure><img src="images/gallery/onsite-lbbd3.jpg" alt="Crane installing a billboard" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/onsite-barlow-sunset.jpg" alt="Crane silhouette at sunset" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-workers1.jpg" alt="Crew working with crane hook" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-rigging2.jpg" alt="Crew loading a cabin onto a trailer" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/cine-newcrane.jpg" alt="Cinematic render, dusk industrial site" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-c8.jpg" alt="Crane at golden hour" loading="lazy"></figure>
      <figure><img src="images/gallery/cine-lakeside7.jpg" alt="Cinematic render, lakeside dusk" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/team-group1.jpg" alt="The Chimes Crane Hire team" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-lbbd3.jpg" alt="Crane installing a billboard" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/onsite-barlow-sunset.jpg" alt="Crane silhouette at sunset" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-workers1.jpg" alt="Crew working with crane hook" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-rigging2.jpg" alt="Crew loading a cabin onto a trailer" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/cine-newcrane.jpg" alt="Cinematic render, dusk industrial site" loading="lazy"></figure>
      <figure><img src="images/gallery/onsite-c8.jpg" alt="Crane at golden hour" loading="lazy"></figure>
      <figure><img src="images/gallery/cine-lakeside7.jpg" alt="Cinematic render, lakeside dusk" loading="lazy"></figure>
      <figure class="wide"><img src="images/gallery/team-group1.jpg" alt="The Chimes Crane Hire team" loading="lazy"></figure>
    </div></div>
    <div style="text-align:center; margin-top:36px;"><a href="galleries.html" class="btn-grn">View Full Galleries</a></div>
  </div>
</section>

<section class="cta-v6">
  <div class="sec-inner cta-v6-inner fu">
    <span class="eyebrow">Let's Build Something</span>
    <h2>Ready When <span class="hl">You Are.</span></h2>
    <a href="contact.html#quote" class="btn-grn">Request A Quote</a>
  </div>
</section>

<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
      <div class="ft-col"><h5>Company</h5><ul><li><a href="index.html#about">About</a></li><li><a href="fleet.html">Fleet</a></li><li><a href="tailored-solutions.html">Tailored Solutions</a></li><li><a href="galleries.html">Galleries</a></li><li><a href="contact.html#team">Team</a></li></ul></div>
      <div class="ft-col"><h5>Services</h5><ul><li><a href="index.html#services">Crane Hire</a></li><li><a href="index.html#services">Rigging</a></li><li><a href="index.html#services">Transport</a></li><li><a href="index.html#services">Lift Planning</a></li></ul></div>
      <div class="ft-col"><h5>Contact</h5>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">+27 11 626 1110</p>
        <p style="font-size:14px; margin-bottom:8px;"><a href="mailto:office@chimes.co.za">office@chimes.co.za</a></p>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">Nasmith Ave, Jupiter Industrial,<br>Germiston, Johannesburg</p>
        <p style="font-size:14px; color:var(--muted);">+27 11 626 2267 (Fax)</p>
      </div>
    </div>
    <div class="ft-bot"><p>&copy; 2026 Chimes Crane Hire (Pty) Ltd.</p><span class="ft-tag">Navy For Authority &middot; Green For Go</span></div>
  </div>
</footer>

<div class="cookie-banner" id="cookieBanner">
  <p>We use cookies to understand how visitors use this site and measure ad performance.</p>
  <div class="cookie-banner-btns"><button class="cb-decline" id="cbDecline" type="button">Decline</button><button class="cb-accept" id="cbAccept" type="button">Accept</button></div>
</div>

<a href="https://wa.me/27823891573" class="wa-fab" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <span class="wa-pulse"></span>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
  <span class="wa-label">Chat On WhatsApp</span>
</a>

<script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify with Playwright**

Navigate to `file:///C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6/index.html`, take a screenshot, then check console messages.

Expected: dark glass homepage renders with the static hero image (not a video) behind the headline; aurora blobs visible; pill nav with "Tailored Solutions" link present; stat numbers animate on scroll (scroll down and re-screenshot to confirm); no console errors. Then run:

```bash
grep -i "<video" index.html
```

Expected: no output (confirms no video element on the homepage, satisfying the performance requirement).

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add index.html: home page in new glass system with static hero image"
```

---

### Task 5: `tailored-solutions.html` (new page)

**Files:**
- Create: `chimes-mockup-v6/tailored-solutions.html`

**Interfaces:**
- Consumes: `.tlr-grid`/`.tlr-card` classes (Task 1), `images/tailored/*` files (Task 1 Step 1), shared nav/footer block (active link = "Tailored Solutions").

Six categories, each with a real photo already copied into `images/tailored/` in Task 1: Steel/Construction (`construction.jpg`), Mining (`mining.jpg`), Petrochemical (`petrochemical.webp`), Telecoms (`telecoms.jpg` — closest-fit placeholder, no dedicated telecom photo exists yet), Renewables (`renewables.jpg` — closest-fit placeholder, no dedicated renewable photo exists yet), General Industrial (`industrial.webp`).

- [ ] **Step 1: Write `tailored-solutions.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tailored Solutions — Chimes Crane Hire</title>
<meta name="description" content="Chimes Crane Hire tailored lifting solutions by industry — Construction, Mining, Petrochemical, Telecoms, Renewables and General Industrial.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="favicon-180.png">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>

<header id="hdr">
  <div class="nav-wrap glass glass-pill">
    <a href="index.html" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire"></a>
    <button class="hbg" id="hbg" aria-label="Menu">
      <svg width="22" height="15" viewBox="0 0 22 15" fill="none"><rect y="0" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="6" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="12" width="22" height="2.5" rx="1" fill="currentColor"/></svg>
    </button>
    <nav class="nav-links" id="nav">
      <a href="index.html">Home</a>
      <a href="fleet.html">Fleet &amp; Specs</a>
      <a href="tailored-solutions.html" class="active">Tailored Solutions</a>
      <a href="galleries.html">Galleries</a>
      <a href="index.html#about">Who We Are</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-ctas">
      <a href="tel:+27116261110" class="btn-out">+27 11 626 1110</a>
      <a href="contact.html#quote" class="btn-fill">Get a Quote</a>
    </div>
  </div>
</header>

<section class="page-hero-v6" style="background-image:url('images/tailored/petrochemical.webp');">
  <div class="page-hero-v6-cnt">
    <span class="eyebrow">Tailored Solutions</span>
    <h1>The Right Crane.<br>For Your <span class="hl">Industry.</span></h1>
    <p>Every sector lifts differently. Here's how Chimes' fleet, riggers and lift planning adapt to the work you actually do.</p>
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <div class="tlr-grid fu">
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/construction.jpg');"></div>
        <div class="tlr-body"><h3>Steel &amp; Construction</h3><p>From foundations to steel erection, our cranes handle material handling and structural lifts on construction sites of every size across Gauteng.</p></div>
      </div>
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/mining.jpg');"></div>
        <div class="tlr-body"><h3>Mining</h3><p>Rough-terrain and all-terrain units built for shaft equipment, bulk material handling and heavy components on demanding mine sites.</p></div>
      </div>
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/petrochemical.webp');"></div>
        <div class="tlr-body"><h3>Petrochemical</h3><p>Tandem-lift capable cranes for refinery turnarounds, tank erection and flare stack work, handled to petrochemical safety standards.</p></div>
      </div>
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/telecoms.jpg');"></div>
        <div class="tlr-body"><h3>Telecoms</h3><p>Mast and tower lifts for telecoms rollouts, carried out by certified riggers who understand confined access and live-site safety.</p></div>
      </div>
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/renewables.jpg');"></div>
        <div class="tlr-body"><h3>Renewable Energy</h3><p>Wind turbine component handling and solar infrastructure lifts, supporting South Africa's renewable energy build-out.</p></div>
      </div>
      <div class="tlr-card">
        <div class="tlr-img" style="background-image:url('images/tailored/industrial.webp');"></div>
        <div class="tlr-body"><h3>General Industrial</h3><p>Plant equipment installs, machinery relocations and heavy component lifts for factories and processing plants across the region.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="cta-v6">
  <div class="sec-inner cta-v6-inner fu">
    <span class="eyebrow">Not Sure Which Fits?</span>
    <h2>Tell Us The Job.<br>We'll <span class="hl">Tailor The Lift.</span></h2>
    <a href="contact.html#quote" class="btn-grn">Get A Quote</a>
  </div>
</section>

<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
      <div class="ft-col"><h5>Company</h5><ul><li><a href="index.html#about">About</a></li><li><a href="fleet.html">Fleet</a></li><li><a href="tailored-solutions.html">Tailored Solutions</a></li><li><a href="galleries.html">Galleries</a></li><li><a href="contact.html#team">Team</a></li></ul></div>
      <div class="ft-col"><h5>Services</h5><ul><li><a href="index.html#services">Crane Hire</a></li><li><a href="index.html#services">Rigging</a></li><li><a href="index.html#services">Transport</a></li><li><a href="index.html#services">Lift Planning</a></li></ul></div>
      <div class="ft-col"><h5>Contact</h5>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">+27 11 626 1110</p>
        <p style="font-size:14px; margin-bottom:8px;"><a href="mailto:office@chimes.co.za">office@chimes.co.za</a></p>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">Nasmith Ave, Jupiter Industrial,<br>Germiston, Johannesburg</p>
        <p style="font-size:14px; color:var(--muted);">+27 11 626 2267 (Fax)</p>
      </div>
    </div>
    <div class="ft-bot"><p>&copy; 2026 Chimes Crane Hire (Pty) Ltd.</p><span class="ft-tag">Navy For Authority &middot; Green For Go</span></div>
  </div>
</footer>

<div class="cookie-banner" id="cookieBanner">
  <p>We use cookies to understand how visitors use this site and measure ad performance.</p>
  <div class="cookie-banner-btns"><button class="cb-decline" id="cbDecline" type="button">Decline</button><button class="cb-accept" id="cbAccept" type="button">Accept</button></div>
</div>

<a href="https://wa.me/27823891573" class="wa-fab" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <span class="wa-pulse"></span>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
  <span class="wa-label">Chat On WhatsApp</span>
</a>

<script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify with Playwright**

Navigate to `tailored-solutions.html`, screenshot, check console messages.

Expected: 6 glass cards in a 3-column grid, each with a distinct real photo and description; "Tailored Solutions" nav pill highlighted green/active; no console errors.

- [ ] **Step 3: Commit**

```bash
git add tailored-solutions.html
git commit -m "Add tailored-solutions.html: new industry-by-industry page with real fleet photos"
```

---

### Task 6: `fleet.html`

**Files:**
- Create: `chimes-mockup-v6/fleet.html`

**Interfaces:**
- Consumes: `.fc`/`.modal-backdrop`/`.spec-table`/`.use-cases` classes (Task 1), `openModal`/`closeModal` (Task 2), `images/fleet/*.jpg` (Task 1 Step 1).

Content (8 crane specs, identical data) sourced verbatim from `chimes-mockup-v4/fleet.html`. One full modal is written below as the exact template (`m-truck-815`); the remaining 7 follow the identical structure with the data substituted from the table beneath it.

- [ ] **Step 1: Write `fleet.html` head, nav, page hero, and crane grids**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Our Fleet &amp; Specifications — Chimes Crane Hire</title>
<meta name="description" content="Chimes Crane Hire's Tadano fleet, 8 to 400 tons. Click any crane for full specifications and typical use cases.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="favicon-180.png">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>

<header id="hdr">
  <div class="nav-wrap glass glass-pill">
    <a href="index.html" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire"></a>
    <button class="hbg" id="hbg" aria-label="Menu">
      <svg width="22" height="15" viewBox="0 0 22 15" fill="none"><rect y="0" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="6" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="12" width="22" height="2.5" rx="1" fill="currentColor"/></svg>
    </button>
    <nav class="nav-links" id="nav">
      <a href="index.html">Home</a>
      <a href="fleet.html" class="active">Fleet &amp; Specs</a>
      <a href="tailored-solutions.html">Tailored Solutions</a>
      <a href="galleries.html">Galleries</a>
      <a href="index.html#about">Who We Are</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-ctas">
      <a href="tel:+27116261110" class="btn-out">+27 11 626 1110</a>
      <a href="contact.html#quote" class="btn-fill">Get a Quote</a>
    </div>
  </div>
</header>

<section class="page-hero-v6" style="background-image:url('Cinematic%20Images/crane%20LBBD%20%231.jpg');">
  <div class="page-hero-v6-cnt">
    <span class="eyebrow">Our Fleet</span>
    <h1>Built To Lift <span class="hl">Anything.</span></h1>
    <p>Tadano cranes, 8 to 400 tons — every unit maintained to OEM specification with full inspection records. Click a crane for full specs and typical use cases.</p>
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <p style="font-size:13px; color:var(--muted); max-width:640px; margin-bottom:32px;">Specifications below reflect Chimes' Tadano fleet by capacity class. Exact load charts for your specific lift are available on request — <a href="contact.html#quote" class="hl">get in touch</a>.</p>

    <div class="cap-hd fu" style="margin-bottom:24px;"><span class="eyebrow">01</span><h2 style="font-size:28px;">Small Cranes</h2></div>
    <div class="fleet-card-grid sm fu">
      <button class="fc" onclick="openModal('m-truck-815')" style="background-image:url('images/fleet/chimes-8-15t-truck.jpg');"><span class="fc-sub">Truck Mount</span><div class="fc-tag"><div class="fc-class">8&ndash;15 Ton Capacity</div><div class="fc-name">8&ndash;15 Ton Truck Mount</div></div></button>
      <button class="fc" onclick="openModal('m-at-40')" style="background-image:url('images/fleet/chimes-40t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Tadano ATF 40G-2</div><div class="fc-name">40 Ton All Terrain</div></div></button>
      <button class="fc" onclick="openModal('m-truck-30')" style="background-image:url('images/fleet/chimes-30t.jpg');"><span class="fc-sub">Truck Mount</span><div class="fc-tag"><div class="fc-class">30 Ton Capacity</div><div class="fc-name">30 Ton Truck Mount</div></div></button>
      <button class="fc" onclick="openModal('m-at-50')" style="background-image:url('images/fleet/chimes-55t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">55 Ton Capacity</div><div class="fc-name">55 Ton All Terrain</div></div></button>
    </div>

    <div class="cap-hd fu" style="margin:64px 0 24px;"><span class="eyebrow">02</span><h2 style="font-size:28px;">Big Cranes</h2></div>
    <div class="fleet-card-grid fu">
      <button class="fc" onclick="openModal('m-at-90')" style="background-image:url('images/fleet/chimes-90t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Tadano ATF 90G-4</div><div class="fc-name">90 Ton All Terrain</div></div></button>
      <button class="fc" onclick="openModal('m-at-110')" style="background-image:url('images/fleet/chimes-110t.jpg');"><span class="fc-sub">All Terrain</span><div class="fc-tag"><div class="fc-class">Tadano Faun ATF 110G-5</div><div class="fc-name">110 Ton All Terrain</div></div></button>
      <button class="fc" onclick="openModal('m-at-220')" style="background-image:url('images/fleet/chimes-220t.jpg');"><span class="fc-sub">Premium</span><div class="fc-tag"><div class="fc-class">126m With Jib</div><div class="fc-name">220 Ton All Terrain</div></div></button>
      <button class="fc" onclick="openModal('m-at-400')" style="background-image:url('images/fleet/chimes-400t.jpg');"><span class="fc-sub">Flagship</span><div class="fc-tag"><div class="fc-class">Our Most Powerful Unit</div><div class="fc-name">400 Ton All Terrain</div></div></button>
    </div>
  </div>
</section>

<section class="cta-v6">
  <div class="sec-inner cta-v6-inner fu">
    <span class="eyebrow">Not Sure What You Need?</span>
    <h2>Tell Us The Lift.<br>We'll <span class="hl">Spec The Crane.</span></h2>
    <p style="color:var(--text); margin-bottom:30px;">Send us the load weight, height, radius and site access, and our team will recommend the right unit from the fleet above.</p>
    <a href="contact.html#quote" class="btn-grn">Get A Quote</a>
  </div>
</section>

<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
      <div class="ft-col"><h5>Company</h5><ul><li><a href="index.html#about">About</a></li><li><a href="fleet.html">Fleet</a></li><li><a href="tailored-solutions.html">Tailored Solutions</a></li><li><a href="galleries.html">Galleries</a></li><li><a href="contact.html#team">Team</a></li></ul></div>
      <div class="ft-col"><h5>Services</h5><ul><li><a href="index.html#services">Crane Hire</a></li><li><a href="index.html#services">Rigging</a></li><li><a href="index.html#services">Transport</a></li><li><a href="index.html#services">Lift Planning</a></li></ul></div>
      <div class="ft-col"><h5>Contact</h5>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">+27 11 626 1110</p>
        <p style="font-size:14px; margin-bottom:8px;"><a href="mailto:office@chimes.co.za">office@chimes.co.za</a></p>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">Nasmith Ave, Jupiter Industrial,<br>Germiston, Johannesburg</p>
        <p style="font-size:14px; color:var(--muted);">+27 11 626 2267 (Fax)</p>
      </div>
    </div>
    <div class="ft-bot"><p>&copy; 2026 Chimes Crane Hire (Pty) Ltd.</p><span class="ft-tag">Navy For Authority &middot; Green For Go</span></div>
  </div>
</footer>

<div class="cookie-banner" id="cookieBanner">
  <p>We use cookies to understand how visitors use this site and measure ad performance.</p>
  <div class="cookie-banner-btns"><button class="cb-decline" id="cbDecline" type="button">Decline</button><button class="cb-accept" id="cbAccept" type="button">Accept</button></div>
</div>

<a href="https://wa.me/27823891573" class="wa-fab" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <span class="wa-pulse"></span>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
  <span class="wa-label">Chat On WhatsApp</span>
</a>

<!-- ===== MODALS ===== -->
<div class="modal-backdrop" id="m-truck-815">
  <div class="modal-card">
    <div class="modal-img" style="background-image:url('images/fleet/chimes-8-15t-truck.jpg');"><span class="modal-tag">Truck Mount</span><button class="modal-close" onclick="closeModal('m-truck-815')" aria-label="Close">&times;</button></div>
    <div class="modal-body">
      <h3>8&ndash;15 Ton Truck Mount</h3>
      <div class="modal-cap">Tadano TM Series</div>
      <p class="modal-desc">Our smallest and most agile units, mounted on a standard truck chassis for fast road travel between sites. Ideal where access is tight and setup time matters.</p>
      <table class="spec-table">
        <tr><td>Capacity</td><td>8&ndash;15 Tons</td></tr>
        <tr><td>Max Boom Length</td><td>~21m</td></tr>
        <tr><td>Max Working Radius</td><td>10&ndash;15m</td></tr>
        <tr><td>Boom Elevation</td><td>0&deg; &ndash; 78&deg;</td></tr>
        <tr><td>Max Hook Block</td><td>15 Tons</td></tr>
        <tr><td>Slewing</td><td>360&deg; Continuous</td></tr>
        <tr><td>Type</td><td>Truck-Mounted</td></tr>
        <tr><td>Travel Speed</td><td>Highway-capable</td></tr>
      </table>
      <div class="use-cases"><span>Urban Sites</span><span>HVAC Installs</span><span>Quick Setup</span><span>Tight Access</span></div>
      <a href="contact.html#quote" class="btn-grn">Check Availability</a>
    </div>
  </div>
</div>
```

- [ ] **Step 2: Add the remaining 7 modals**

Repeat the exact `.modal-backdrop` > `.modal-card` > `.modal-img` + `.modal-body` structure from Step 1's `m-truck-815` example, substituting these values (insert each `<div class="modal-backdrop" id="...">...</div>` block directly before `<script src="script.js"></script>`, in this order):

| id | image | modal-tag | h3 | modal-cap | modal-desc | spec rows | use-cases |
|---|---|---|---|---|---|---|---|
| `m-at-40` | `images/fleet/chimes-40t.jpg` | All Terrain | 40 Ton All Terrain | Tadano ATF 40G-2 &middot; Verified Spec | A compact 2-axle all-terrain crane with independent suspension for excellent maneuverability, equally at home on construction sites and rough terrain. | Capacity: 40 Tons / Max Boom Length: 35.2m / Boom Elevation: -0.5&deg; &ndash; +79&deg; / Axles: 2 / Max Hook Block: 32 Tons / Slewing: 360&deg; Continuous / Type: All Terrain | Construction, Telecoms, Rough Terrain |
| `m-truck-30` | `images/fleet/chimes-30t.jpg` | Truck Mount | 30 Ton Truck Mount | Tadano TL300E | A standard truck-chassis crane offering a cost-effective, quickly deployed solution for medium lifts around building sites and container yards. | Capacity: 30 Tons / Max Boom Length: 38m / Max Working Radius: ~32m / Boom Elevation: 0&deg; &ndash; 80&deg; / Max Hook Block: 20 Tons / Slewing: 360&deg; Continuous / Type: Truck-Mounted | Building Construction, Container Handling, Fast Deployment |
| `m-at-50` | `images/fleet/chimes-55t.jpg` | All Terrain | 55 Ton All Terrain | 55 Ton Capacity | A heavy construction workhorse with an optional jib extension, suited to steel erection, industrial plant work and precast concrete placement. | Capacity: 55 Tons / Max Boom Length: 40m / Boom Elevation: -2&deg; &ndash; +83&deg; / Max Hook Block: 50 Tons / Slewing: 360&deg; Continuous / Type: All Terrain | Steel Erection, Industrial Plant, Precast Concrete, Jib Extension Available |
| `m-at-90` | `images/fleet/chimes-90t.jpg` | All Terrain | 90 Ton All Terrain | Tadano ATF 90G-4 &middot; Verified Spec | An industrial and petrochemical specialist, capable of handling heavy modules over long reach — a regular on mining and bridge-construction sites. | Capacity: 90 Tons / Max Boom Length: 51.2m / Boom Elevation: -1&deg; &ndash; +82.4&deg; / Axles: 4 / Max Hook Block: 100 Tons / Slewing: 360&deg; Continuous / Type: All Terrain | Heavy Modules, Mining Equipment, Bridge Construction, Wind Energy |
| `m-at-110` | `images/fleet/chimes-110t.jpg` | All Terrain | 110 Ton All Terrain | Tadano Faun ATF 110G-5 &middot; Verified Spec | A proven mid-range performer across petrochemical, mining and heavy construction projects, bridging the gap between our mid-tier and flagship units. | Capacity: 110 Tons / Max Boom Length: 52.0m / Boom Elevation: -2&deg; &ndash; +82&deg; / Axles: 5 / Max Hook Block: 125 Tons / Slewing: 360&deg; Continuous / Type: All Terrain | Industrial Lifts, Petrochemical, Mid-Size Tandem Lifts |
| `m-at-220` | `images/fleet/chimes-220t.jpg` | Premium | 220 Ton All Terrain | Tadano ATF 220G-5 &middot; Verified Spec | Tadano's all-terrain cranes feature purpose-built frames with full-width two-man cabs, electronic load moment devices, and automatic overload shut-off — engineered for reliable performance in any climate or terrain. | Capacity: 220 Tons / Boom Length: 68m / Reach With Jib: 126m / Boom Elevation: -1.5&deg; &ndash; +84&deg; / Axles: 5 / Max Hook Block: 151 Tons / Slewing: 360&deg; Continuous / Type: All Terrain | Refinery Operations, Power Plant Construction, Tandem Lifts, Extreme Reach |
| `m-at-400` | `images/fleet/chimes-400t.jpg` | Flagship | 400 Ton All Terrain | Tadano ATF 400G-6 &middot; Verified Spec | Our most powerful unit, reserved for the heaviest and most demanding lifts across South Africa's biggest industrial projects. | Capacity: 400 Tons / Max Boom Length: 80.0m / Boom Elevation: -0.8&deg; &ndash; +83.5&deg; / Axles: 6 / Max Hook Block: 250 Tons / Slewing: 360&deg; Continuous / Type: All Terrain &middot; Heavy Lift | Power Plants, Extreme Heavy Lifts, Industrial Mega Projects |

Each "spec rows" cell lists `label: value` pairs separated by ` / ` — render each as its own `<tr><td>label</td><td>value</td></tr>`. Each "use-cases" cell lists comma-separated tags — render each as its own `<span>tag</span>` inside `.use-cases`. Close with `<script src="script.js"></script></body></html>`.

- [ ] **Step 3: Verify with Playwright**

Navigate to `fleet.html`, screenshot. Click one small-crane `.fc` button (e.g. the 8–15 Ton one) via `mcp__plugin_playwright_playwright__browser_click`, screenshot again, then click its modal's close button and confirm it closes. Check console messages throughout.

Expected: 8 fleet cards across two grids; clicking a card opens its glass modal with the correct spec table and use-case tags; Escape key or close button dismisses it; no console errors.

- [ ] **Step 4: Commit**

```bash
git add fleet.html
git commit -m "Add fleet.html: 8-crane spec grid with glass modal detail view"
```

---

### Task 7: `galleries.html`

**Files:**
- Create: `chimes-mockup-v6/galleries.html`

**Interfaces:**
- Consumes: `.gal-tabs`/`.gal-tab-btn`/`.gal-panel`/`.gallery-grid`/`.lightbox` classes (Task 1), `switchGalTab`/lightbox JS (Task 2), `images/gallery/*` + `images/the_team*.webp`/`the_braai.webp` (Task 1 Step 1).

All 43 photos and their alt text are carried over verbatim from `chimes-mockup-v4/galleries.html`.

- [ ] **Step 1: Write `galleries.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Galleries — Chimes Crane Hire</title>
<meta name="description" content="Chimes Crane Hire photo galleries — on-site action, cinematic renders and the team behind the lifts.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="favicon-180.png">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>

<header id="hdr">
  <div class="nav-wrap glass glass-pill">
    <a href="index.html" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire"></a>
    <button class="hbg" id="hbg" aria-label="Menu">
      <svg width="22" height="15" viewBox="0 0 22 15" fill="none"><rect y="0" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="6" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="12" width="22" height="2.5" rx="1" fill="currentColor"/></svg>
    </button>
    <nav class="nav-links" id="nav">
      <a href="index.html">Home</a>
      <a href="fleet.html">Fleet &amp; Specs</a>
      <a href="tailored-solutions.html">Tailored Solutions</a>
      <a href="galleries.html" class="active">Galleries</a>
      <a href="index.html#about">Who We Are</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-ctas">
      <a href="tel:+27116261110" class="btn-out">+27 11 626 1110</a>
      <a href="contact.html#quote" class="btn-fill">Get a Quote</a>
    </div>
  </div>
</header>

<section class="page-hero-v6" style="background-image:url('images/gallery/onsite-lbbd3.jpg');">
  <div class="page-hero-v6-cnt">
    <span class="eyebrow">Galleries</span>
    <h1>The Fleet, <span class="hl">In Frame.</span></h1>
    <p>Live lifts, job sites and the crews behind every job — a closer look at Chimes in action.</p>
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <div class="gal-tabs fu">
      <button class="gal-tab-btn active" data-tab="onsite">On Site</button>
      <button class="gal-tab-btn" data-tab="cinematic">Cinematic</button>
      <button class="gal-tab-btn" data-tab="team">Team</button>
    </div>

    <div class="gal-panel active" id="panel-onsite">
      <div class="gallery-grid fu">
        <figure class="wide tall"><img src="images/gallery/onsite-lbbd3.jpg" alt="Crane installing a billboard" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-barlow1.jpg" alt="Crane on a job site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-barlow2.jpg" alt="Abnormal load at sunset" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-barlow4.jpg" alt="Crane on a job site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-workers1.jpg" alt="Crew working with crane hook" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-workers2.jpg" alt="Crew securing a load" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-rigging1.jpg" alt="Crew rigging a cabin for transport" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-rigging2.jpg" alt="Crew loading a cabin onto a trailer" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-rigging3.jpg" alt="Crew slinging a load on site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-rigging-harness.jpg" alt="Rigger in fall-arrest harness" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-lbbd2.jpg" alt="Crane on site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-lbbd4.jpg" alt="Crane on site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-lbbd6.jpg" alt="Crane on site" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-lbbd7.jpg" alt="Crane on site" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-c8.jpg" alt="Crane at golden hour" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-cch2.jpg" alt="Chimes crane on site" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-industrial4.jpg" alt="Industrial site lift" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-barlow-sunset.jpg" alt="Crane silhouette at sunset" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-reflection.jpg" alt="Crane reflected in wet ground" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-editorial1.jpg" alt="Crew loading a container" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-insta3.jpg" alt="Crane headlight close-up" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-insta5.jpg" alt="Crane fleet at dusk" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/onsite-insta-draft2.jpg" alt="Crane on site at sunset" loading="lazy"></figure>
        <figure><img src="images/gallery/onsite-randompost.jpg" alt="Chimes trucks at the yard" loading="lazy"></figure>
      </div>
    </div>

    <div class="gal-panel" id="panel-cinematic">
      <div class="gallery-grid fu">
        <figure class="wide tall"><img src="images/gallery/cine-newcrane.jpg" alt="Cinematic render, dusk industrial site" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-c3.jpg" alt="Cinematic render, hook against stormy sky" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-canyon5.jpg" alt="Cinematic render, canyon sunset" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/cine-lakeside1.jpg" alt="Cinematic render, lakeside building" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-lakeside3.jpg" alt="Cinematic render, lakeside dusk" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-lakeside4.jpg" alt="Cinematic render, lakeside building" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/cine-lakeside5.jpg" alt="Cinematic render, lakeside scene" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-lakeside6.jpg" alt="Cinematic render, lakeside scene" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-lakeside7.jpg" alt="Cinematic render, lakeside dusk" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/cine-lakeside8.jpg" alt="Cinematic render, lakeside scene" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-lakeside10.jpg" alt="Cinematic render, lakeside scene" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-ultra1.jpg" alt="Cinematic render, crew with hook" loading="lazy"></figure>
        <figure class="wide"><img src="images/gallery/cine-ultra2.jpg" alt="Cinematic render, crew with hook" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-ultra3.jpg" alt="Cinematic render, crew with hook" loading="lazy"></figure>
        <figure><img src="images/gallery/cine-editorial4.jpg" alt="Crane boom against golden sky" loading="lazy"></figure>
      </div>
    </div>

    <div class="gal-panel" id="panel-team">
      <div class="gallery-grid fu">
        <figure class="wide tall"><img src="images/gallery/team-group1.jpg" alt="The Chimes Crane Hire team" loading="lazy"></figure>
        <figure class="wide"><img src="images/the_team.webp" alt="The Chimes Crane Hire team" loading="lazy"></figure>
        <figure><img src="images/the_team3.webp" alt="Chimes crew on site" loading="lazy"></figure>
        <figure><img src="images/the_braai.webp" alt="Chimes team event" loading="lazy"></figure>
      </div>
    </div>
  </div>
</section>

<section class="cta-v6">
  <div class="sec-inner cta-v6-inner fu">
    <span class="eyebrow">Like What You See?</span>
    <h2>Let's Get You<br>On <span class="hl">Site.</span></h2>
    <a href="contact.html#quote" class="btn-grn">Request A Quote</a>
  </div>
</section>

<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
      <div class="ft-col"><h5>Company</h5><ul><li><a href="index.html#about">About</a></li><li><a href="fleet.html">Fleet</a></li><li><a href="tailored-solutions.html">Tailored Solutions</a></li><li><a href="galleries.html">Galleries</a></li><li><a href="contact.html#team">Team</a></li></ul></div>
      <div class="ft-col"><h5>Services</h5><ul><li><a href="index.html#services">Crane Hire</a></li><li><a href="index.html#services">Rigging</a></li><li><a href="index.html#services">Transport</a></li><li><a href="index.html#services">Lift Planning</a></li></ul></div>
      <div class="ft-col"><h5>Contact</h5>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">+27 11 626 1110</p>
        <p style="font-size:14px; margin-bottom:8px;"><a href="mailto:office@chimes.co.za">office@chimes.co.za</a></p>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">Nasmith Ave, Jupiter Industrial,<br>Germiston, Johannesburg</p>
        <p style="font-size:14px; color:var(--muted);">+27 11 626 2267 (Fax)</p>
      </div>
    </div>
    <div class="ft-bot"><p>&copy; 2026 Chimes Crane Hire (Pty) Ltd.</p><span class="ft-tag">Navy For Authority &middot; Green For Go</span></div>
  </div>
</footer>

<div class="cookie-banner" id="cookieBanner">
  <p>We use cookies to understand how visitors use this site and measure ad performance.</p>
  <div class="cookie-banner-btns"><button class="cb-decline" id="cbDecline" type="button">Decline</button><button class="cb-accept" id="cbAccept" type="button">Accept</button></div>
</div>

<a href="https://wa.me/27823891573" class="wa-fab" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <span class="wa-pulse"></span>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
  <span class="wa-label">Chat On WhatsApp</span>
</a>

<div class="lightbox" id="lightbox">
  <button class="lb-close" id="lbClose" aria-label="Close">&times;</button>
  <button class="lb-prev" id="lbPrev" aria-label="Previous">&larr;</button>
  <img id="lbImg" src="" alt="">
  <button class="lb-next" id="lbNext" aria-label="Next">&rarr;</button>
  <span class="lb-count" id="lbCount"></span>
</div>

<script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify with Playwright**

Navigate to `galleries.html`, screenshot the "On Site" tab. Click the "Cinematic" tab via `mcp__plugin_playwright_playwright__browser_click`, screenshot. Click a figure to open the lightbox, screenshot, then click `#lbNext` and screenshot again. Check console messages throughout.

Expected: tab switching swaps the visible grid; clicking any figure opens a full-screen glass lightbox with that image; next/prev cycle through the active panel's images only; no console errors.

- [ ] **Step 3: Commit**

```bash
git add galleries.html
git commit -m "Add galleries.html: tabbed photo grids with lightbox"
```

---

### Task 8: `contact.html`

**Files:**
- Create: `chimes-mockup-v6/contact.html`

**Interfaces:**
- Consumes: `.quick-grid`/`.qc-card`/`.signup-band`/`.quote-grid`/`.form`/`.f-row`/`.f-field`/`.team-grid`/`.team-card` classes (Task 1), `handleForm`/`handleSignup` (Task 2).

Content (quick-contact cards, signup band, quote form, map, leadership/team cards) sourced verbatim from `chimes-mockup-v4/contact.html`.

- [ ] **Step 1: Write `contact.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact Us — Chimes Crane Hire</title>
<meta name="description" content="Contact Chimes Crane Hire in Germiston, Johannesburg. Call, WhatsApp, or request a quote — meet the team behind the lifts.">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Barlow:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="favicon-180.png">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>

<header id="hdr">
  <div class="nav-wrap glass glass-pill">
    <a href="index.html" class="logo-link"><img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire"></a>
    <button class="hbg" id="hbg" aria-label="Menu">
      <svg width="22" height="15" viewBox="0 0 22 15" fill="none"><rect y="0" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="6" width="22" height="2.5" rx="1" fill="currentColor"/><rect y="12" width="22" height="2.5" rx="1" fill="currentColor"/></svg>
    </button>
    <nav class="nav-links" id="nav">
      <a href="index.html">Home</a>
      <a href="fleet.html">Fleet &amp; Specs</a>
      <a href="tailored-solutions.html">Tailored Solutions</a>
      <a href="galleries.html">Galleries</a>
      <a href="index.html#about">Who We Are</a>
      <a href="contact.html" class="active">Contact</a>
    </nav>
    <div class="nav-ctas">
      <a href="tel:+27116261110" class="btn-out">+27 11 626 1110</a>
      <a href="contact.html#quote" class="btn-fill">Get a Quote</a>
    </div>
  </div>
</header>

<section class="page-hero-v6" style="background-image:url('images/silo-tanks-1.webp');">
  <div class="page-hero-v6-cnt">
    <span class="eyebrow">Get In Touch</span>
    <h1>Let's Talk About <span class="hl">Your Lift.</span></h1>
    <p>Call, WhatsApp, or send us your project details below. For urgent site requirements, phone us directly — we're owner-managed, so you're talking to people who can make the call.</p>
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <div class="quick-grid fu">
      <div class="qc-card">
        <h3>Call Us</h3>
        <p style="margin-bottom:14px;">Available during business hours for quotes and urgent enquiries.</p>
        <a href="tel:+27116261110" class="btn-fill" style="display:inline-block;">+27 11 626 1110</a>
      </div>
      <div class="qc-card">
        <h3>WhatsApp</h3>
        <p style="margin-bottom:14px;">Fastest way to reach us for instant service or a quick quote.</p>
        <a href="https://wa.me/27823891573" target="_blank" rel="noopener noreferrer" class="wa-cta">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="#0a1420"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
          Chat Now
        </a>
      </div>
      <div class="qc-card">
        <h3>Visit / Write</h3>
        <p>Nasmith Avenue, Jupiter Industrial, Germiston, Johannesburg</p>
        <p>Fax: +27 11 626 2267</p>
        <p><a href="mailto:office@chimes.co.za" class="hl">office@chimes.co.za</a></p>
      </div>
    </div>
  </div>
</section>

<section class="sec alt" style="padding-top:0;">
  <div class="sec-inner">
    <div class="signup-band glass fu">
      <div>
        <h3>Stay In The Loop</h3>
        <p>Fleet updates, safety notices and project news — no spam, unsubscribe any time.</p>
      </div>
      <form class="signup-form" onsubmit="handleSignup(event)">
        <input type="email" placeholder="you@company.co.za" required aria-label="Email address">
        <button type="submit">Subscribe</button>
      </form>
    </div>
  </div>
</section>

<section class="cta-v6" id="quote" style="text-align:left; padding:96px 0;">
  <div class="sec-inner quote-grid">
    <div class="fu">
      <span class="eyebrow">Request A Quote</span>
      <h2 style="font-size:clamp(28px,3.6vw,44px); margin:16px 0 18px;">Tell Us About<br>The <span class="hl">Lift.</span></h2>
      <p style="color:var(--text); margin-bottom:26px;">Load weight, height, radius, site access, dates — the more detail, the faster we can quote. We respond promptly during business hours.</p>
      <div style="display:flex; flex-direction:column; gap:12px;">
        <a href="tel:+27116261110" style="display:flex; align-items:center; gap:10px; color:var(--white); font-family:var(--ff-head); font-weight:800;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="var(--green)"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
          +27 11 626 1110
        </a>
        <a href="mailto:office@chimes.co.za" style="display:flex; align-items:center; gap:10px; color:var(--text);">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 7l10 7 10-7"/></svg>
          office@chimes.co.za
        </a>
      </div>
    </div>
    <form class="form glass fu" onsubmit="handleForm(event)">
      <div class="f-row">
        <div class="f-field"><label for="qnm">Full Name</label><input type="text" id="qnm" name="name" placeholder="Your name" required></div>
        <div class="f-field"><label for="qco">Company</label><input type="text" id="qco" name="company" placeholder="Company name"></div>
      </div>
      <div class="f-row">
        <div class="f-field"><label for="qph">Phone</label><input type="tel" id="qph" name="phone" placeholder="+27 xx xxx xxxx" required></div>
        <div class="f-field"><label for="qem">Email</label><input type="email" id="qem" name="email" placeholder="you@company.co.za" required></div>
      </div>
      <div class="f-field">
        <label for="qcr">Crane Required</label>
        <select id="qcr" name="crane">
          <option value="">Select capacity...</option>
          <option>8&ndash;15 Ton Truck Mount</option>
          <option>40 Ton All Terrain</option>
          <option>30 Ton Truck Mount</option>
          <option>55 Ton All Terrain</option>
          <option>90 Ton All Terrain</option>
          <option>110 Ton All Terrain</option>
          <option>220 Ton All Terrain</option>
          <option>400 Ton All Terrain</option>
          <option>Not sure &ndash; please advise</option>
        </select>
      </div>
      <div class="f-field"><label for="qmsg">Project Details</label><textarea id="qmsg" name="message" placeholder="What are we lifting, how heavy, how high, and when?"></textarea></div>
      <button type="submit" class="btn-sub" id="sub-btn">Submit Request</button>
      <p style="font-size:11px; color:var(--muted); margin-top:14px;">POPIA: we only use these details to respond to your enquiry.</p>
    </form>
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Find Us</span><h2>Our Germiston Yard.</h2></div>
    <p style="font-size:15px; color:var(--text); margin-bottom:26px;">Nasmith Avenue, Jupiter Industrial, Germiston, Johannesburg, Gauteng.</p>
    <div class="map-wrap fu">
      <iframe src="https://maps.google.com/maps?q=Nasmith+Avenue,+Jupiter,+Germiston,+South+Africa&z=14&output=embed" allowfullscreen loading="lazy" title="Chimes Crane Hire location map"></iframe>
    </div>
  </div>
</section>

<section class="sec alt" id="team">
  <div class="sec-inner">
    <div class="cap-hd fu"><span class="eyebrow">Who You'll Be Talking To</span><h2>Owner-Managed.<br>Hands-On <span class="hl">Leadership.</span></h2></div>
    <p style="font-size:15px; color:var(--text); margin-bottom:40px; max-width:560px;">Chimes is owner-managed, not run by a faceless head office. Here's who's behind the company, and who picks up the phone.</p>

    <div class="sub-hd fu">Leadership</div>
    <div class="team-grid fu" style="margin-bottom:56px;">
      <div class="team-card">
        <h4>Bradley de Klerk</h4>
        <div class="team-role">Managing Director</div>
        <p>Leads Chimes' day-to-day operations and client relationships, ensuring every lift is delivered on time and on budget.</p>
        <p>Cell: <a href="tel:+27823860056">+27 82 386 0056</a></p>
        <p>Email: <a href="mailto:brad@chimes.co.za">brad@chimes.co.za</a></p>
      </div>
    </div>

    <div class="sub-hd fu">Your Chimes Team</div>
    <div class="team-grid fu">
      <div class="team-card">
        <h4>Marco Dos Santos</h4>
        <div class="team-role">Sales</div>
        <p>Cell: <a href="tel:+27823891573">+27 82 389 1573</a></p>
        <p>Email: <a href="mailto:marco@chimes.co.za">marco@chimes.co.za</a></p>
      </div>
      <div class="team-card">
        <h4>Broderick Marias</h4>
        <div class="team-role">Sales</div>
        <p>Cell: <a href="tel:+27716889160">+27 71 688 9160</a></p>
        <p>Email: <a href="mailto:broderick@chimes.co.za">broderick@chimes.co.za</a></p>
      </div>
      <div class="team-card">
        <h4>Hilton Levy</h4>
        <div class="team-role">Sales</div>
        <p>Cell: <a href="tel:+27828245469">+27 82 824 5469</a></p>
        <p>Email: <a href="mailto:hilton@chimes.co.za">hilton@chimes.co.za</a></p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="sec-inner">
    <div class="ft-top">
      <div class="ft-brand">
        <img src="Logos/Chimes_Dynamic_Logo_White_PNG.png" alt="Chimes Crane Hire">
        <p>Chimes Crane Hire (Pty) Ltd — raising the standard in mobile crane hire, rigging and specialised transport across South Africa since 2003.</p>
        <div class="bee bee-ft"><svg width="16" height="16" viewBox="0 0 20 20" fill="var(--green)"><path d="M10 2L12.4 7.2L18 8L14 11.8L15.1 17.4L10 14.7L4.9 17.4L6 11.8L2 8L7.6 7.2Z"/></svg><span>BEE Level 4 Contributor</span></div>
        <a href="https://www.facebook.com/ChimesCraneHire/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="ft-social"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
      </div>
      <div class="ft-col"><h5>Company</h5><ul><li><a href="index.html#about">About</a></li><li><a href="fleet.html">Fleet</a></li><li><a href="tailored-solutions.html">Tailored Solutions</a></li><li><a href="galleries.html">Galleries</a></li><li><a href="contact.html#team">Team</a></li></ul></div>
      <div class="ft-col"><h5>Services</h5><ul><li><a href="index.html#services">Crane Hire</a></li><li><a href="index.html#services">Rigging</a></li><li><a href="index.html#services">Transport</a></li><li><a href="index.html#services">Lift Planning</a></li></ul></div>
      <div class="ft-col"><h5>Contact</h5>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">+27 11 626 1110</p>
        <p style="font-size:14px; margin-bottom:8px;"><a href="mailto:office@chimes.co.za">office@chimes.co.za</a></p>
        <p style="font-size:14px; color:var(--muted); margin-bottom:8px;">Nasmith Ave, Jupiter Industrial,<br>Germiston, Johannesburg</p>
        <p style="font-size:14px; color:var(--muted);">+27 11 626 2267 (Fax)</p>
      </div>
    </div>
    <div class="ft-bot"><p>&copy; 2026 Chimes Crane Hire (Pty) Ltd.</p><span class="ft-tag">Navy For Authority &middot; Green For Go</span></div>
  </div>
</footer>

<div class="cookie-banner" id="cookieBanner">
  <p>We use cookies to understand how visitors use this site and measure ad performance.</p>
  <div class="cookie-banner-btns"><button class="cb-decline" id="cbDecline" type="button">Decline</button><button class="cb-accept" id="cbAccept" type="button">Accept</button></div>
</div>

<a href="https://wa.me/27823891573" class="wa-fab" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <span class="wa-pulse"></span>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.7.8-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-1.7-.7-2.8-2.4-2.9-2.5-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.6-1.4c-.1-.3-.3-.3-.5-.3h-.4c-.2 0-.4.1-.5.3-.2.2-.7.7-.7 1.7s.7 2 .8 2.1c.1.2 1.6 2.4 3.9 3.3 1.9.7 2.3.6 2.6.5.4-.1 1.2-.5 1.4-1 .2-.5.2-.9.1-1z"/></svg>
  <span class="wa-label">Chat On WhatsApp</span>
</a>

<script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify with Playwright**

Navigate to `contact.html`, screenshot. Fill the quote form via `mcp__plugin_playwright_playwright__browser_fill_form` (name, phone, email at minimum) and submit via click, then screenshot to confirm the button shows "Sending..." then "Request Sent!". Check console messages.

Expected: quick-contact glass cards, signup band, two-column quote form with the Google Maps iframe rendering below, leadership/team glass cards; form submit shows the demo success state; no console errors.

- [ ] **Step 3: Commit**

```bash
git add contact.html
git commit -m "Add contact.html: quick contact, quote form, map, leadership/team"
```

---

### Task 9: Cross-page QA pass

**Files:** none created — verification only.

- [ ] **Step 1: Walk every page with Playwright**

For each of `index.html`, `fleet.html`, `tailored-solutions.html`, `galleries.html`, `contact.html`:
1. `mcp__plugin_playwright_playwright__browser_navigate` to the file.
2. `mcp__plugin_playwright_playwright__browser_console_messages` — expected: empty/no errors.
3. `mcp__plugin_playwright_playwright__browser_take_screenshot` at default desktop size.
4. `mcp__plugin_playwright_playwright__browser_resize` to 390x844 (mobile) and screenshot again — expected: hamburger menu visible, grids collapse to 1–2 columns per the `@media (max-width:640px)` rules from Task 1, no horizontal scrollbar.

- [ ] **Step 2: Confirm the performance requirement holds site-wide**

```bash
cd "C:/Users/micha/OneDrive/Desktop/Chimes Work/Mockups/chimes-mockup-v6"
grep -rl "<video" *.html
```

Expected: no output (no page anywhere embeds a `<video>` element).

- [ ] **Step 3: Confirm nav consistency across all 5 pages**

```bash
grep -c "tailored-solutions.html" index.html fleet.html tailored-solutions.html galleries.html contact.html
```

Expected: every file reports a count of 2 or more (once in the nav, at least once more in the footer "Company" column).

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "Final cross-page QA pass for chimes-mockup-v6" --allow-empty
git log --oneline
```

Expected: a clean commit log showing all 9 tasks' commits. Remind the user at this point that no GitHub repo has been created and nothing has been pushed — that remains a separate, explicit decision per the spec's Global Constraints.
