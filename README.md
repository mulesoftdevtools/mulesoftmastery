# MuleSoft Mastery — Complete MuleSoft Learning Website

A premium, fully responsive, multi-page static website for learning MuleSoft —
built with plain HTML, CSS and JavaScript only. No frameworks, no build step
required to run it, no AI integrations, and no API keys anywhere in the code.

## What's in this zip

```
website/         <- THE ACTUAL SITE. Push the contents of this folder to your
                     GitHub repository root — this is what GitHub Pages serves.
source-files/    <- Optional. The Python generator + JSON content used to build
                     the site, in case you want to edit lesson text later and
                     regenerate all 142 pages automatically instead of hand-editing HTML.
README.md        <- This file.
```

## What's included

- 14 categories, 121 lessons (142 HTML pages total) covering the complete
  MuleSoft curriculum: Introduction to MuleSoft, Anypoint Platform & Studio,
  Anypoint Platform Components (Runtime Manager, environments, VPC, access
  management, Exchange, Design Center, monitoring, CLI, Secrets Manager),
  Mule 4 Flow Fundamentals, DataWeave 2.0 (including a full function
  reference), 21 MuleSoft Connectors with config examples (HTTP, Database,
  MySQL, File, FTP, SFTP, Amazon S3, Azure Service Bus, Salesforce, Workday,
  SAP, ServiceNow, NetSuite, Email, JMS, ActiveMQ, Anypoint MQ, VM, Object
  Store, Web Service Consumer, Kafka), Error Handling, APIkit/RAML/OAS
  (a deep RAML reference — data types, traits, resource types, security
  schemes, libraries, examples), MUnit Testing, Deployment & CloudHub
  (CloudHub 1.0 and 2.0, Runtime Fabric, standalone/hybrid, CLI, Maven
  plugin), API Manager & Security (every major policy type plus a
  step-by-step "how to apply a policy" walkthrough), Batch Processing &
  Scheduling, AI in MuleSoft (MuleSoft AI Chain, Einstein, Intelligent
  Document Processing, generative AI patterns, Composer), and Best
  Practices & Interview Prep.
- Hand-built inline SVG flow diagrams on the pages where a visual helps most
  (Mule event structure, API-led connectivity layers, error handling
  branches, OAuth 2.0 token flow, batch job phases, CloudHub architecture,
  deployment models, MUnit test anatomy, the Anypoint Platform component
  map, DataWeave transformation flow, and the API policy chain) — pure SVG,
  no images or external diagram services.
- Top navigation bar with logo, primary links, and a live client-side search box.
- Left sidebar with all categories as collapsible dropdowns (`<details>`
  accordions) and every subtopic nested underneath — works even with
  JavaScript disabled, and is enhanced with smooth accordion behavior and a
  mobile slide-out drawer when JavaScript is on.
- Client-side search (no backend, no API key) powered by a static
  `assets/js/search-index.json` file generated from your content.
- Fully responsive design: desktop, tablet, and mobile layouts, tested down
  to 390px wide.
- Home, About, Contact (pre-filled with **beautifulcreator9@gmail.com**),
  Privacy Policy, Disclaimer/Terms, a full "All Topics" index page, and a
  custom 404 page.
- `sitemap.xml` and `robots.txt` for SEO.
- Ad placeholder slots (`<div class="ad-slot">`) already positioned in the
  layout (in-article and sidebar) — clearly marked, empty, and ready for you
  to paste your AdSense `<ins>` unit code into once your site is approved.
  Nothing ad-related is hard-coded, so the site works perfectly with zero ads
  as-is.

## 1. Site URL — already set for your repo

Every HTML page's canonical/Open Graph URL is already pre-configured for:

```
https://mulesoftdevtools.github.io/mulesoftmastery
```

That matches `https://github.com/mulesoftdevtools/mulesoftmastery`, so as
long as you publish this exact `website/` folder to that exact repository
(steps below), there's nothing to change here — skip straight to step 2.

If you ever fork this to a different repo or username, open
`source-files/generator.py`, change the `SITE_URL` constant near the top,
run `python3 generator.py` from inside `source-files/`, and copy the
regenerated `build/` folder contents over `website/`.

> Note on regenerating: `generator.py` expects a `content/` folder next to it
> (already provided under `source-files/content/`) and writes its output to a
> `build/` folder it creates alongside itself. No third-party Python packages
> are required — only the standard library.

## 2. Publish to GitHub Pages

1. Copy **everything inside `website/`** (including the hidden `.nojekyll`
   file) into the root of `mulesoftdevtools/mulesoftmastery` — `index.html`
   should sit directly at the repo root, not inside a subfolder.
2. Commit and push.
3. In the repo, go to **Settings → Pages**, set **Source** to your default
   branch (e.g. `main`) and folder `/ (root)`, then save.
4. GitHub will serve it at `https://mulesoftdevtools.github.io/mulesoftmastery/`.
   Wait a minute or two for the first deploy, then visit it.

The included `.nojekyll` file tells GitHub Pages to serve the files exactly
as-is, skipping Jekyll processing — this avoids GitHub trying to interpret
folders like `assets` in unexpected ways.

### Using a custom domain instead
If you'd rather use your own domain, add a `CNAME` file to the repo root
containing just your domain name, point your DNS at GitHub Pages per
[GitHub's custom domain docs](https://docs.github.com/en/pages), and update
`SITE_URL` as described in step 1.

## 3. Preparing for Google AdSense

This site was built with AdSense review in mind:

- Substantial, original, well-organized content on every page (no thin or
  placeholder pages).
- Clear site navigation, search, and a full sitemap.
- About, Contact, Privacy Policy and Disclaimer pages are all included and
  linked from the footer of every page.
- No pop-ups, no deceptive placements, no auto-playing media.
- No ad code is included by default — nothing to remove or misconfigure
  before you apply.

**To add ads after you're approved:**
1. Get your AdSense publisher code snippet from your AdSense account.
2. Add the main AdSense `<script>` tag (the one with your `ca-pub-XXXXXXXXXXXXXXXX`
   ID) once, right before the closing `</head>` tag in each page — or, since
   this is a generated site, add it inside the `render_head()` function in
   `source-files/generator.py` and regenerate, so it's added to all 142 pages
   at once.
3. Replace the placeholder text inside any `<div class="ad-slot">...</div>`
   block with your actual `<ins class="adsbygoogle">` ad unit code. These
   slots already exist in the sidebar and inside each lesson article.
4. Once your AdSense account is approved, Google will also ask you to place
   an `ads.txt` file at your site root with a line like:
   `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`
   Create this file yourself with your real publisher ID — don't guess it,
   AdSense shows you the exact line to use in your account dashboard.

## 4. Editing content later

Every lesson lives in `source-files/content/<category-slug>.json` as plain
JSON (title, meta description, reading time, summary, and an HTML content
fragment per lesson). To edit a lesson: open the relevant JSON file, edit the
`content_html` field for that subtopic (keep it as an HTML fragment — no
`<html>`, `<head>`, or `<h1>` tags, since the page template adds those), save,
and re-run `python3 generator.py`. It will regenerate all 142 pages with fully
consistent navigation, so you never have to hand-edit the header, sidebar or
footer across 142 files. `content/_index.json` controls category/lesson order,
titles and slugs — edit this if you want to add a brand-new category or
lesson (remember to also add matching content to the relevant category's
JSON file).

## 5. Tech notes

- Fonts: Google Fonts (Inter/Poppins) are loaded via a `<link>` tag — free,
  no API key. If you want a fully offline/self-hosted site, remove the two
  `fonts.googleapis.com` / `fonts.gstatic.com` lines from the `<head>` of
  each page (or from `render_head()` in the generator) and the site will
  fall back to system fonts automatically.
- No cookies, no analytics, and no tracking scripts are included. If you
  later add Google Analytics or AdSense, update `privacy-policy.html` (or the
  `build_privacy()` function in `generator.py`) accordingly — it already
  contains standard AdSense cookie-disclosure language to save you a step.
- All internal links are relative (not absolute paths), so the site works
  correctly whether it's hosted at a domain root or in a GitHub Pages
  project subpath like `/your-repo/`.

## 6. Local preview

Because the search box uses `fetch()` to load `search-index.json`, opening
`index.html` directly from your filesystem (`file://`) will show the search
box but return no results (browsers block `fetch` on local files). To
preview the full site locally, including search, run a simple local server
from inside `website/`:

```bash
cd website
python3 -m http.server 8000
```
Then open `http://localhost:8000` in your browser. This local-preview
limitation does not apply once the site is hosted on GitHub Pages — search
works there immediately.

---

Questions about this build? Contact: **beautifulcreator9@gmail.com**
