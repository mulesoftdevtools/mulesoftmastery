#!/usr/bin/env python3
"""
Static site generator for the MuleSoft Mastery learning website.
Reads structured JSON content from ./content and renders a complete,
multi-page, responsive static HTML site into ./build.

No external Python packages required (standard library only).
No AI / API key integrations anywhere in the generated output.
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
OUT_DIR = ROOT / "build"

SITE_NAME = "MuleSoft Mastery"
SITE_TAGLINE = "The Complete MuleSoft Learning Platform"
SITE_DESCRIPTION = (
    "Learn MuleSoft from scratch: Anypoint Platform, Mule 4, DataWeave 2.0, 21 connectors, "
    "RAML/OAS API design, every API Manager policy, MUnit testing, CloudHub 1.0/2.0 deployment, "
    "Runtime Manager and AI in MuleSoft — a free, structured course from beginner to advanced."
)
# Replace with your real published domain once you publish to GitHub Pages
# (e.g. https://yourusername.github.io/mulesoft-mastery). Used only for
# canonical tags, sitemap.xml and Open Graph URLs.
SITE_URL = "https://mulesoftdevtools.github.io/mulesoftmastery"
CONTACT_EMAIL = "beautifulcreator9@gmail.com"

# External resource links (shown in the top nav, sidebar, footer, and a
# homepage promo section). Both open in a new tab.
DEV_TOOL_URL = "https://mulesoftdevtools.github.io/mulesoft-project-tools/index.html"
EBOOK_STORE_URL = "https://payhip.com/mulesoftebooks/collection/mulesoft"

# ---------------------------------------------------------------- Icons ----
ICON_SEARCH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/>'
               '<line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>')
ICON_CLOCK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/>'
              '<polyline points="12 7 12 12 15.5 14"/></svg>')
ICON_LAYERS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/>'
               '<polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>')
ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/>'
             '<polyline points="2 6 12 13 22 6"/></svg>')
ICON_BOOK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
             '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>')
ICON_CODE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/>'
             '<polyline points="8 6 2 12 8 18"/></svg>')
ICON_SHIELD = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>')
ICON_CLOUD = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round">'
              '<path d="M17.5 19H9a5 5 0 1 1 1.3-9.8A6 6 0 0 1 22 12.5a4.5 4.5 0 0 1-4.5 6.5z"/></svg>')
ICON_ARROW_RIGHT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
                     'stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
                     '<polyline points="12 5 19 12 12 19"/></svg>')
ICON_EXTERNAL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
                  'stroke-linecap="round" stroke-linejoin="round" class="icon-external">'
                  '<path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>')
ICON_TOOL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.8 2.8-2-2z"/></svg>')
ICON_SUN = ('<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.5"/>'
            '<path d="M12 2.5v2.4M12 19.1v2.4M4.6 4.6l1.7 1.7M17.7 17.7l1.7 1.7M2.5 12h2.4M19.1 12h2.4'
            'M4.6 19.4l1.7-1.7M17.7 6.3l1.7-1.7"/></svg>')
ICON_MOON = ('<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.8 6.8 0 0 0 10.5 10.5z"/></svg>')

# --------------------------------------------------------------- Helpers ---
def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------- SVG diagrams ---
def svg_text(x, y, lines, fill="#ffffff", size=13, weight=600):
    if isinstance(lines, str):
        lines = [lines]
    line_h = size + 5
    start_y = y - (len(lines) - 1) * line_h / 2 + size / 3
    tspans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_h
        tspans.append('<tspan x="{}" dy="{}">{}</tspan>'.format(x, dy, esc(line)))
    return ('<text x="{x}" y="{y}" text-anchor="middle" font-family="Inter, Arial, sans-serif" '
            'font-size="{size}" font-weight="{weight}" style="fill:{fill}">{tspans}</text>').format(
        x=x, y=start_y, size=size, weight=weight, fill=fill, tspans="".join(tspans)
    )


def svg_box(cx, cy, w, h, lines, fill="#2f5fed", text_fill="#ffffff", rx=12, font_size=13,
            stroke=None, dashed=False):
    x, y = cx - w / 2, cy - h / 2
    stroke_attr = ' stroke="{}" stroke-width="1.5"'.format(stroke) if stroke else ""
    dash_attr = ' stroke-dasharray="6,4"' if dashed else ""
    rect = '<rect x="{}" y="{}" width="{}" height="{}" rx="{}" fill="{}"{}{}/>'.format(
        x, y, w, h, rx, fill, stroke_attr, dash_attr
    )
    return rect + svg_text(cx, cy, lines, fill=text_fill, size=font_size)


def svg_arrow(x1, y1, x2, y2, color="var(--diagram-lifeline)", dashed=False, label=None, label_bg=True):
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    line = ('<line x1="{}" y1="{}" x2="{}" y2="{}" style="stroke:{}" stroke-width="2.2" '
            'marker-end="url(#arrowhead)"{}/>').format(x1, y1, x2, y2, color, dash)
    lbl = ""
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 9
        bg = ""
        if label_bg:
            bg = '<rect x="{}" y="{}" width="{}" height="16" style="fill:var(--diagram-label-bg)"/>'.format(
                mx - len(label) * 3.3, my - 12, len(label) * 6.6
            )
        lbl = bg + ('<text x="{}" y="{}" text-anchor="middle" font-family="Inter, Arial, sans-serif" '
                     'font-size="11" font-weight="600" style="fill:var(--diagram-label-text)">{}</text>').format(mx, my, esc(label))
    return line + lbl


def svg_wrap(w, h, body):
    return ('<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Diagram" preserveAspectRatio="xMidYMid meet">'
            '<defs><marker id="arrowhead" markerWidth="9" markerHeight="9" refX="7" refY="3" '
            'orient="auto"><path d="M0,0 L0,6 L8,3 z" style="fill:var(--diagram-lifeline)"/></marker></defs>{body}</svg>'
            ).format(w=w, h=h, body=body)


def diagram_card(caption, svg):
    return ('<div class="diagram-card"><div class="diagram-title">Visual Overview</div>{svg}'
            '<p class="diagram-caption">{caption}</p></div>').format(svg=svg, caption=esc(caption))


def hchain(steps, width=780, height=180, box_w=150, box_h=70, colors=None, y=None, arrow_labels=None,
           font_size=12.5):
    n = len(steps)
    y = y if y is not None else height / 2
    margin = 50
    usable = width - 2 * margin
    gap = (usable - n * box_w) / (n - 1) if n > 1 else 0
    xs = [margin + box_w / 2 + i * (box_w + gap) for i in range(n)]
    default_colors = ["#2f5fed", "#3f6ff0", "#1548c9", "#00a99b", "#00c2a8"]
    parts = []
    for i, (cx, label) in enumerate(zip(xs, steps)):
        fill = colors[i] if colors else default_colors[i % len(default_colors)]
        lines = label if isinstance(label, list) else label.split("\n")
        parts.append(svg_box(cx, y, box_w, box_h, lines, fill=fill, font_size=font_size))
    for i in range(n - 1):
        x1, x2 = xs[i] + box_w / 2, xs[i + 1] - box_w / 2
        albl = arrow_labels[i] if arrow_labels and i < len(arrow_labels) else None
        parts.append(svg_arrow(x1, y, x2, y, label=albl))
    return svg_wrap(width, height, "".join(parts))


def _diagram_mule_event():
    steps = ["HTTP Listener\n(Source)", "Mule Event Created\nPayload + Attributes\n+ Variables",
              "Set Variable", "Transform Message\n(DataWeave)", "HTTP Response"]
    svg = hchain(steps, width=800, height=190, box_w=145, box_h=82, font_size=12)
    return diagram_card("Every Mule flow builds a Mule event as it moves through a source and a chain of processors — the event carries the payload, attributes, and variables together.", svg)


def _diagram_api_led():
    W, H = 760, 380
    parts = [
        svg_box(380, 30, 220, 44, ["Client Apps / Devices"], fill="#0b1220", font_size=12.5),
        svg_box(380, 120, 640, 60, ["Experience APIs", "channel-specific data shaping"], fill="#00c2a8",
                text_fill="#06251f", font_size=13),
        svg_box(380, 200, 640, 60, ["Process APIs", "orchestration & business logic"], fill="#2f5fed",
                font_size=13),
        svg_box(380, 280, 640, 60, ["System APIs", "unlock backend systems of record"], fill="#0b1220",
                font_size=13),
        svg_box(140, 355, 170, 42, ["SAP"], fill="#eaf0ff", text_fill="#1e46c4", font_size=12.5),
        svg_box(380, 355, 170, 42, ["Salesforce"], fill="#eaf0ff", text_fill="#1e46c4", font_size=12.5),
        svg_box(620, 355, 170, 42, ["Database"], fill="#eaf0ff", text_fill="#1e46c4", font_size=12.5),
        svg_arrow(380, 52, 380, 90, color="var(--diagram-lifeline)"),
        svg_arrow(380, 150, 380, 170, color="var(--diagram-lifeline)"),
        svg_arrow(380, 230, 380, 250, color="var(--diagram-lifeline)"),
        svg_arrow(380, 310, 140, 334, color="var(--diagram-lifeline)"),
        svg_arrow(380, 310, 380, 334, color="var(--diagram-lifeline)"),
        svg_arrow(380, 310, 620, 334, color="var(--diagram-lifeline)"),
    ]
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("API-led connectivity organizes APIs into three layers so each system, process and channel can evolve independently.", svg)


def _diagram_error_handling():
    W, H = 720, 300
    parts = [
        svg_box(130, 55, 190, 60, ["Flow Processor"], fill="#2f5fed"),
        svg_box(440, 55, 190, 60, ["Error Thrown"], fill="#dc2626"),
        svg_arrow(225, 55, 345, 55, label="raises"),
        svg_box(230, 175, 210, 62, ["On Error Continue"], fill="#16a34a"),
        svg_box(590, 175, 210, 62, ["On Error Propagate"], fill="#d97706"),
        svg_arrow(410, 75, 300, 150, color="var(--diagram-lifeline)"),
        svg_arrow(470, 75, 560, 150, color="var(--diagram-lifeline)"),
        svg_box(230, 262, 260, 50, ["Flow resumes normally"], fill="#eaf7ee", text_fill="#166534",
                font_size=12),
        svg_box(590, 262, 260, 50, ["Error re-thrown to caller"], fill="#fdf1e2", text_fill="#92400e",
                font_size=12),
        svg_arrow(230, 206, 230, 237, color="var(--diagram-lifeline)"),
        svg_arrow(590, 206, 590, 237, color="var(--diagram-lifeline)"),
    ]
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("On Error Continue swallows the error and lets the flow finish normally; On Error Propagate handles it but still re-throws it to the caller.", svg)


def _diagram_oauth2():
    W, H = 800, 300
    lifeline_top, lifeline_bot = 70, 280
    parts = [
        svg_box(100, 40, 160, 44, ["Client App"], fill="#2f5fed", font_size=12.5),
        svg_box(400, 40, 190, 44, ["Authorization Server"], fill="#0b1220", font_size=12.5),
        svg_box(700, 40, 160, 44, ["Mule API"], fill="#00a99b", font_size=12.5),
        svg_arrow(100, lifeline_top, 100, lifeline_bot, color="var(--diagram-lifeline)", dashed=True),
        svg_arrow(400, lifeline_top, 400, lifeline_bot, color="var(--diagram-lifeline)", dashed=True),
        svg_arrow(700, lifeline_top, 700, lifeline_bot, color="var(--diagram-lifeline)", dashed=True),
        svg_arrow(100, 100, 400, 100, label="1. Request authorization"),
        svg_arrow(400, 140, 100, 140, label="2. Issue access token"),
        svg_arrow(100, 180, 700, 180, label="3. Call API + Bearer token"),
        svg_arrow(700, 215, 400, 215, label="4. Validate / introspect token"),
        svg_arrow(700, 255, 100, 255, label="5. Protected response"),
    ]
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("A typical OAuth 2.0 authorization code exchange in front of a Mule-implemented API.", svg)


def _diagram_batch_job():
    steps = ["Input Records\n(Load & Dispatch)", "Batch Step 1\n(Validate)", "Batch Step 2\n(Enrich / Send)",
              "On Complete\n(Aggregate Results)"]
    svg = hchain(steps, width=800, height=180, box_w=170, box_h=76, font_size=12.5)
    return diagram_card("A batch job loads records, streams them through one or more batch steps record-by-record, then runs an on-complete phase once every record finishes.", svg)


def _diagram_cloudhub_arch():
    W, H = 760, 290
    parts = [
        svg_box(380, 25, 220, 40, ["Client Requests"], fill="#0b1220", font_size=12),
        '<rect x="60" y="60" width="640" height="200" rx="14" fill="none" style="stroke:var(--diagram-lifeline)" stroke-width="1.5" stroke-dasharray="6,4"/>',
        svg_text(90, 82, ["CloudHub Virtual Private Cloud"], fill="var(--diagram-label-text)", size=12, weight=700),
        svg_box(380, 130, 240, 46, ["Shared / Dedicated Load Balancer"], fill="#2f5fed", font_size=12),
        svg_box(240, 220, 190, 66, ["Worker (vCore)", "Your App Replica"], fill="#00a99b", font_size=12),
        svg_box(520, 220, 190, 66, ["Worker (vCore)", "Your App Replica"], fill="#00a99b", font_size=12),
        svg_arrow(380, 45, 380, 107, color="var(--diagram-lifeline)"),
        svg_arrow(340, 153, 260, 187, color="var(--diagram-lifeline)"),
        svg_arrow(420, 153, 500, 187, color="var(--diagram-lifeline)"),
    ]
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("Each CloudHub worker runs an isolated replica of your application behind a load balancer inside a dedicated Virtual Private Cloud.", svg)


def _diagram_deployment_models():
    W, H = 800, 210
    parts = [
        svg_box(400, 30, 340, 44, ["Anypoint Platform Control Plane"], fill="#0b1220", font_size=12.5),
        svg_box(140, 145, 220, 74, ["CloudHub", "Fully managed by MuleSoft"], fill="#2f5fed", font_size=12.5),
        svg_box(400, 145, 220, 74, ["Runtime Fabric", "Self-managed containers"], fill="#00a99b",
                font_size=12.5),
        svg_box(660, 145, 220, 74, ["Standalone / Hybrid", "Self-hosted on VMs / on-prem"], fill="#3f6ff0",
                font_size=12.5),
        svg_arrow(320, 45, 170, 108, color="var(--diagram-lifeline)"),
        svg_arrow(400, 52, 400, 108, color="var(--diagram-lifeline)"),
        svg_arrow(480, 45, 630, 108, color="var(--diagram-lifeline)"),
    ]
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("All three deployment models are managed from the same Anypoint Platform control plane but differ in who runs the underlying infrastructure.", svg)


def _diagram_munit():
    steps = ["Setup\nMock & set the\nMule event", "Execution\nRun the flow\nunder test", "Validation\nAssert on the\nresult"]
    svg = hchain(steps, width=760, height=180, box_w=190, box_h=82, font_size=12.5)
    return diagram_card("Every MUnit test follows the same three phases: set up mocks and input, execute the flow, then assert the outcome.", svg)


def _diagram_platform_components():
    W, H = 740, 340
    labels = ["Design Center", "Anypoint Exchange", "API Manager", "Runtime Manager",
              "Access Management", "Anypoint Monitoring"]
    parts = [svg_box(150, H / 2, 220, 70, ["Anypoint Platform", "Control Plane"], fill="#0b1220", font_size=13)]
    top = 25
    step = (H - 2 * top) / (len(labels) - 1)
    for i, lbl in enumerate(labels):
        cy = top + i * step
        parts.append(svg_box(580, cy, 260, 46, [lbl], fill="#2f5fed" if i % 2 == 0 else "#00a99b", font_size=12.5))
        parts.append(svg_arrow(260, H / 2, 450, cy, color="var(--diagram-lifeline)"))
    svg = svg_wrap(W, H, "".join(parts))
    return diagram_card("Anypoint Platform is a single control plane spanning design, cataloging, governance, deployment, access control and observability.", svg)


def _diagram_dataweave_transform():
    steps = ["Input\nJSON / XML / CSV\n/ Java", "DataWeave 2.0\nTransform Script", "Output\nJSON / XML / CSV\n/ Java"]
    svg = hchain(steps, width=760, height=190, box_w=210, box_h=90, font_size=12.5)
    return diagram_card("DataWeave sits between any input and output format, so the same script logic works regardless of the wire format on either side.", svg)


def _diagram_policy_chain():
    steps = ["API Request", "Rate Limiting\nPolicy", "Client ID\nEnforcement", "OAuth 2.0 Token\nValidation",
              "Your API\nImplementation"]
    svg = hchain(steps, width=820, height=180, box_w=150, box_h=78, font_size=11.8)
    return diagram_card("Policies execute as a chain in front of your API implementation — each request must pass every applied policy, in order, before it reaches your flow.", svg)


DIAGRAM_MAP = {
    "mule-event-message-structure": _diagram_mule_event,
    "api-led-connectivity": _diagram_api_led,
    "on-error-continue-vs-propagate": _diagram_error_handling,
    "oauth2-in-mulesoft": _diagram_oauth2,
    "batch-job-overview": _diagram_batch_job,
    "cloudhub-overview": _diagram_cloudhub_arch,
    "standalone-and-hybrid-deployment": _diagram_deployment_models,
    "munit-overview": _diagram_munit,
    "runtime-manager-overview": _diagram_platform_components,
    "dataweave-introduction": _diagram_dataweave_transform,
    "how-to-apply-a-policy": _diagram_policy_chain,
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_file(rel_path, content):
    out_path = OUT_DIR / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")


def cat_path(cat):
    return "categories/{}.html".format(cat["slug"])


def sub_path(cat, sub):
    return "topics/{}/{}.html".format(cat["slug"], sub["slug"])


def breadcrumbs(trail):
    """trail: list of (label, href_or_None)"""
    parts = []
    n = len(trail)
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append('<a href="{}">{}</a>'.format(href, esc(label)))
        else:
            parts.append('<span aria-current="page">{}</span>'.format(esc(label)))
        if i < n - 1:
            parts.append('<span class="sep">/</span>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">{}</nav>'.format("".join(parts))


# ------------------------------------------------------- Load content data -
index_data = load_json(CONTENT_DIR / "_index.json")
categories_meta = sorted(index_data["categories"], key=lambda c: c["order"])

content_by_cat = {}
for cm in categories_meta:
    content_by_cat[cm["slug"]] = load_json(CONTENT_DIR / (cm["slug"] + ".json"))

CATEGORIES = []
for cm in categories_meta:
    cslug = cm["slug"]
    content_cat = content_by_cat[cslug]
    sub_content_by_slug = {s["slug"]: s for s in content_cat["subtopics"]}
    subtopics = []
    for sm in sorted(cm["subtopics"], key=lambda s: s["order"]):
        sslug = sm["slug"]
        sc = sub_content_by_slug[sslug]
        subtopics.append({
            "slug": sslug,
            "title": sm["title"],
            "order": sm["order"],
            "meta_description": sc["meta_description"],
            "reading_time": sc["reading_time"],
            "summary": sc["summary"],
            "content_html": sc["content_html"],
        })
    CATEGORIES.append({
        "slug": cslug,
        "title": cm["title"],
        "order": cm["order"],
        "description": cm["description"],
        "subtopics": subtopics,
    })

FLAT = []
for cat in CATEGORIES:
    for sub in cat["subtopics"]:
        FLAT.append((cat, sub))

TOTAL_CATEGORIES = len(CATEGORIES)
TOTAL_LESSONS = len(FLAT)

# ------------------------------------------------------------- Templates ---
def core_nav_items(prefix):
    return [
        {"key": "home", "label": "Home", "href": prefix + "index.html"},
        {"key": "categories", "label": "All Topics", "href": prefix + "categories/index.html"},
        {"key": "about", "label": "About", "href": prefix + "about.html"},
        {"key": "contact", "label": "Contact", "href": prefix + "contact.html"},
        {"key": "devtools", "label": "Dev Tool", "href": DEV_TOOL_URL, "external": True, "highlight": True},
        {"key": "ebooks", "label": "Ebook Store", "href": EBOOK_STORE_URL, "external": True, "highlight": True},
    ]


def nav_link_html(it, active=None):
    classes = []
    if active and it.get("key") == active:
        classes.append("active")
    if it.get("highlight"):
        classes.append("nav-highlight")
    cls = ' class="{}"'.format(" ".join(classes)) if classes else ""
    if it.get("external"):
        return '<a href="{}" target="_blank" rel="noopener noreferrer"{}>{}{}</a>'.format(
            it["href"], cls, it["label"], ICON_EXTERNAL
        )
    return '<a href="{}"{}>{}</a>'.format(it["href"], cls, it["label"])


def render_head(title, description, prefix, canonical_path):
    if title == SITE_NAME:
        full_title = "{} — {}".format(SITE_NAME, SITE_TAGLINE)
    else:
        full_title = "{} | {}".format(title, SITE_NAME)
    canonical = "{}/{}".format(SITE_URL, canonical_path) if canonical_path else SITE_URL + "/"
    return """<head>
<meta charset="UTF-8">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(!t){{t=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}}if(t==='dark'){{document.documentElement.setAttribute('data-theme','dark');}}}}catch(e){{}}}})();</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>""".format(
        title=esc(full_title), desc=esc(description), canonical=canonical,
        site=esc(SITE_NAME), prefix=prefix,
    )


def render_header(prefix, active):
    items = core_nav_items(prefix)
    nav_html = "".join(nav_link_html(it, active) for it in items)
    return """<header class="site-header">
  <div class="header-inner">
    <button class="sidebar-toggle" data-sidebar-toggle aria-label="Toggle navigation menu" aria-controls="sidebar">
      <span class="icon-bars"><span></span><span></span><span></span></span>
    </button>
    <a class="brand" href="{prefix}index.html">
      <span class="brand-mark">M</span>
      <span class="brand-text"><span class="brand-name">{site}</span><span class="brand-tag">{tagline}</span></span>
    </a>
    <nav class="main-nav" aria-label="Primary">{nav}</nav>
    <div class="header-search">
      <input type="search" data-search-input placeholder="Search MuleSoft topics..." aria-label="Search MuleSoft topics" autocomplete="off">
      <span class="search-icon-btn">{icon_search}</span>
      <div class="search-results" data-search-results role="listbox"></div>
    </div>
    <button class="theme-toggle" data-theme-toggle type="button" aria-label="Toggle dark mode" title="Toggle dark mode">
      {icon_sun}{icon_moon}
    </button>
  </div>
</header>""".format(prefix=prefix, site=esc(SITE_NAME), tagline=esc(SITE_TAGLINE),
                     nav=nav_html, icon_search=ICON_SEARCH, icon_sun=ICON_SUN, icon_moon=ICON_MOON)


def render_sidebar(prefix, active_cat=None, active_sub=None):
    items = core_nav_items(prefix)
    mobile_links = "".join(nav_link_html(it) for it in items)

    cat_blocks = []
    for cat in CATEGORIES:
        open_attr = " open" if cat["slug"] == active_cat else ""
        sub_items = []
        for sub in cat["subtopics"]:
            cls = ' class="active"' if (cat["slug"] == active_cat and sub["slug"] == active_sub) else ""
            sub_items.append('<li><a href="{}{}"{}>{}</a></li>'.format(
                prefix, sub_path(cat, sub), cls, esc(sub["title"])
            ))
        sub_html = "".join(sub_items)
        cat_blocks.append(
            '<details class="side-cat"{open_attr}>'
            '<summary><span class="side-cat-num">{num}</span>'
            '<span class="side-cat-title">{title}</span>'
            '<svg class="side-cat-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="9 18 15 12 9 6"/></svg></summary>'
            '<ul class="side-sublist">{subs}</ul>'
            '<a class="sidebar-cat-link" href="{prefix}{cpath}">View category overview →</a>'
            '</details>'.format(
                open_attr=open_attr, num=cat["order"], title=esc(cat["title"]),
                subs=sub_html, prefix=prefix, cpath=cat_path(cat)
            )
        )
    cats_html = "".join(cat_blocks)
    return (
        '<aside class="sidebar" id="sidebar">'
        '<div class="mobile-nav-links">{mobile}</div>'
        '<div class="sidebar-heading">Course Curriculum</div>'
        '{cats}'
        '</aside>'
        '<div class="sidebar-backdrop" id="sidebarBackdrop"></div>'
    ).format(mobile=mobile_links, cats=cats_html)


def render_footer(prefix):
    quick = [("Home", "index.html"), ("All Topics", "categories/index.html"),
             ("About Us", "about.html"), ("Contact", "contact.html")]
    legal = [("Privacy Policy", "privacy-policy.html"), ("Disclaimer", "disclaimer.html"),
             ("Sitemap", "sitemap.xml")]
    quick_html = "".join('<li><a href="{}{}">{}</a></li>'.format(prefix, href, label) for label, href in quick)
    legal_html = "".join('<li><a href="{}{}">{}</a></li>'.format(prefix, href, label) for label, href in legal)
    cat_html = "".join(
        '<li><a href="{}{}">{}</a></li>'.format(prefix, cat_path(cat), esc(cat["title"])) for cat in CATEGORIES
    )
    resources_html = (
        '<li><a href="{}" target="_blank" rel="noopener noreferrer">MuleSoft Dev Tool{ext}</a></li>'
        '<li><a href="{}" target="_blank" rel="noopener noreferrer">Ebook Store{ext}</a></li>'
    ).format(DEV_TOOL_URL, EBOOK_STORE_URL, ext=ICON_EXTERNAL)
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{prefix}index.html">
          <span class="brand-mark">M</span>
          <span class="brand-text"><span class="brand-name" style="color:#fff">{site}</span></span>
        </a>
        <p>{desc}</p>
        <p style="color:#7d88ab;font-size:13px;">New lessons are added regularly &mdash; check back often
          for fresh content.</p>
        <p style="color:#7d88ab;font-size:13px;">Questions, feedback or corrections?
          <a href="mailto:{email}" style="color:#5be6cf;font-weight:600;">{email}</a></p>
      </div>
      <div class="footer-col"><h5>Explore</h5><ul>{quick}</ul></div>
      <div class="footer-col"><h5>Categories</h5><ul>{cats}</ul></div>
      <div class="footer-col"><h5>Resources</h5><ul>{resources}</ul></div>
      <div class="footer-col"><h5>Legal</h5><ul>{legal}</ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="footerYear">2026</span> {site}. All rights reserved.</span>
      <div class="fb-links">
        <a href="{prefix}privacy-policy.html">Privacy</a>
        <a href="{prefix}disclaimer.html">Disclaimer</a>
        <a href="{prefix}contact.html">Contact</a>
      </div>
    </div>
    <p class="trademark-note">{site} is an independent, community-built educational resource created to
      help developers learn integration concepts. It is not affiliated with, endorsed by, or sponsored by
      Salesforce, Inc. MuleSoft&reg;, Anypoint Platform&reg;, Anypoint Studio&reg;, DataWeave&reg; and related
      marks are registered trademarks of Salesforce, Inc. and/or MuleSoft, LLC. All product names, logos and
      brands referenced on this site are used for identification and educational purposes only.</p>
  </div>
</footer>
<script>window.__MM_SEARCH_INDEX__ = {search_json};</script>
<script src="{prefix}assets/js/main.js" defer></script>""".format(
        prefix=prefix, site=esc(SITE_NAME), desc=esc(SITE_DESCRIPTION), email=CONTACT_EMAIL,
        quick=quick_html, cats=cat_html, legal=legal_html, resources=resources_html,
        search_json=SEARCH_ITEMS_JS,
    )


def render_page(title, description, prefix, canonical_path, active_nav, body_html,
                 active_cat=None, active_sub=None, pre_layout_html="", main_wrapper_class=""):
    head = render_head(title, description, prefix, canonical_path)
    header = render_header(prefix, active_nav)
    sidebar = render_sidebar(prefix, active_cat, active_sub)
    footer = render_footer(prefix)
    return """<!DOCTYPE html>
<html lang="en">
{head}
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
{header}
{pre_layout}
<div class="layout">
{sidebar}
<main class="main-wrapper {mwc}" id="main-content">
{body}
</main>
</div>
{footer}
</body>
</html>""".format(head=head, header=header, pre_layout=pre_layout_html, sidebar=sidebar,
                   mwc=main_wrapper_class, body=body_html, footer=footer)


def render_bare_page(title, description, prefix, canonical_path, active_nav, body_html):
    """Page without sidebar layout (used for the 404 page)."""
    head = render_head(title, description, prefix, canonical_path)
    header = render_header(prefix, active_nav)
    footer = render_footer(prefix)
    return """<!DOCTYPE html>
<html lang="en">
{head}
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
{header}
<main id="main-content" style="padding-top:var(--header-height);">
{body}
</main>
{footer}
</body>
</html>""".format(head=head, header=header, body=body_html, footer=footer)


# ------------------------------------------------------------ Page builds --
def build_home():
    prefix = ""
    intro = """<div class="home-intro">
  <span class="eyebrow-light">100%% Free &middot; No Sign-up Required &middot; Updated Regularly</span>
  <h1>Learn <span class="grad-text">MuleSoft</span> the Right Way &mdash; From Fundamentals to Production</h1>
  <p class="lead">%s</p>
  <div class="hero-actions">
    <a class="btn btn-primary btn-lg" href="categories/introduction-to-mulesoft.html">Start Learning %s</a>
    <a class="btn btn-outline btn-lg" href="categories/index.html">Browse All Topics</a>
  </div>
  <div class="home-stats">
    <div><span class="num">%d</span><span class="lbl">Categories</span></div>
    <div><span class="num">%d+</span><span class="lbl">Lessons</span></div>
    <div><span class="num">100%%</span><span class="lbl">Free Forever</span></div>
    <div><span class="num">Mule 4</span><span class="lbl">Up To Date</span></div>
  </div>
</div>""" % (esc(SITE_DESCRIPTION), ICON_ARROW_RIGHT, TOTAL_CATEGORIES, TOTAL_LESSONS)

    cards = []
    for cat in CATEGORIES:
        cards.append(
            '<a class="cat-card" href="{cpath}">'
            '<div class="card-num">{num:02d}</div>'
            '<h3>{title}</h3><p>{desc}</p>'
            '<div class="card-meta"><span>{count} lessons</span><span class="go">Explore &rarr;</span></div>'
            '</a>'.format(cpath=cat_path(cat), num=cat["order"], title=esc(cat["title"]),
                          desc=esc(cat["description"]), count=len(cat["subtopics"]))
        )
    cards_html = "".join(cards)

    roadmap_items = []
    for cat in CATEGORIES:
        roadmap_items.append(
            '<li><a class="rm-title" href="{cpath}">{num}. {title}</a>'
            '<div class="rm-desc">{desc}</div></li>'.format(
                cpath=cat_path(cat), num=cat["order"], title=esc(cat["title"]), desc=esc(cat["description"])
            )
        )
    roadmap_html = "".join(roadmap_items)

    body = intro + """
<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <div class="kicker">Course Catalog</div>
      <h2>Everything You Need to Master MuleSoft</h2>
      <p>Follow a structured, category-by-category curriculum covering the entire MuleSoft ecosystem
      &mdash; from your first flow in Anypoint Studio to securing and deploying production-grade APIs.</p>
    </div>
    <div class="cards-grid">{cards}</div>
  </div>
</section>

<section class="section on-bg">
  <div class="container">
    <div class="section-head">
      <div class="kicker">Why This Course</div>
      <h2>Built for Developers Who Want to Actually Learn</h2>
    </div>
    <div class="feature-grid">
      <div class="feature-item"><div class="fi-icon">{book}</div><h4>Structured Curriculum</h4>
        <p>Topics are ordered exactly how you should learn them &mdash; no guesswork, no missing pieces.</p></div>
      <div class="feature-item"><div class="fi-icon">{code}</div><h4>Real Code Examples</h4>
        <p>Every lesson includes practical Mule 4 XML, DataWeave 2.0 or configuration snippets you can reuse.</p></div>
      <div class="feature-item"><div class="fi-icon">{shield}</div><h4>No Sign-up, No Cost</h4>
        <p>Every lesson is free and open. No accounts, no paywalls, no API keys required.</p></div>
      <div class="feature-item"><div class="fi-icon">{cloud}</div><h4>Production-Focused</h4>
        <p>Learn deployment, security and testing &mdash; not just the basics &mdash; so you're job-ready.</p></div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <div class="kicker">Suggested Path</div>
      <h2>Your MuleSoft Learning Roadmap</h2>
      <p>New to MuleSoft? Follow these categories in order for the smoothest learning curve.</p>
    </div>
    <ol class="roadmap">{roadmap}</ol>
  </div>
</section>

<section class="section on-bg">
  <div class="container">
    <div class="section-head">
      <div class="kicker">Free Resources</div>
      <h2>More Ways to Work With MuleSoft</h2>
      <p>Two free companions to this course &mdash; a developer productivity tool and a library of
      MuleSoft ebooks.</p>
    </div>
    <div class="cards-grid-2">
      <div class="cat-card resource-card">
        <div class="resource-icon">{tool_icon}</div>
        <h3>MuleSoft Dev Tool</h3>
        <p>A free companion utility for MuleSoft developers &mdash; handy helpers and productivity
        shortcuts for everyday Anypoint Studio work.</p>
        <a class="btn btn-primary" href="{dev_tool_url}" target="_blank" rel="noopener noreferrer">
          Open Dev Tool {ext_icon}</a>
      </div>
      <div class="cat-card resource-card">
        <div class="resource-icon">{book_icon}</div>
        <h3>MuleSoft Ebook Store</h3>
        <p>Go deeper with downloadable MuleSoft ebooks covering DataWeave, connectors, integration
        patterns and certification preparation.</p>
        <a class="btn btn-primary" href="{ebook_url}" target="_blank" rel="noopener noreferrer">
          Browse Ebooks {ext_icon}</a>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Ready to become a MuleSoft developer?</h2>
        <p>Jump into Lesson 1 and start building real integrations today.</p>
      </div>
      <a class="btn btn-outline btn-lg" href="categories/introduction-to-mulesoft.html">Begin the Course</a>
    </div>
  </div>
</section>
""".format(cards=cards_html, book=ICON_BOOK, code=ICON_CODE, shield=ICON_SHIELD, cloud=ICON_CLOUD,
           roadmap=roadmap_html, tool_icon=ICON_TOOL, book_icon=ICON_BOOK, ext_icon=ICON_EXTERNAL,
           dev_tool_url=DEV_TOOL_URL, ebook_url=EBOOK_STORE_URL)

    doc = render_page(SITE_NAME, SITE_DESCRIPTION, prefix, "", "home", body)
    write_file("index.html", doc)


def build_categories_index():
    prefix = "../"
    rows = []
    for cat in CATEGORIES:
        pills = "".join(
            '<a href="{}{}">{}</a>'.format(prefix, sub_path(cat, sub), esc(sub["title"]))
            for sub in cat["subtopics"]
        )
        rows.append(
            '<div class="cat-row"><div class="num">{num:02d}</div><div>'
            '<h3><a href="{prefix}{cpath}">{title}</a></h3>'
            '<p>{desc} &middot; {count} lessons</p>'
            '<div class="subtopic-pills">{pills}</div>'
            '</div></div>'.format(num=cat["order"], prefix=prefix, cpath=cat_path(cat),
                                   title=esc(cat["title"]), desc=esc(cat["description"]),
                                   count=len(cat["subtopics"]), pills=pills)
        )
    rows_html = "".join(rows)
    bc = breadcrumbs([("Home", prefix + "index.html"), ("All Topics", None)])
    body = """{bc}
<div class="page-hero" style="padding-top:0;">
  <h1>All MuleSoft Topics</h1>
  <p>Browse the complete curriculum &mdash; {ncat} categories and {nles} lessons covering every part of the
  MuleSoft ecosystem, organized in the order you should learn them.</p>
</div>
<div class="cat-list-page" style="margin-top:20px;">{rows}</div>""".format(
        bc=bc, ncat=TOTAL_CATEGORIES, nles=TOTAL_LESSONS, rows=rows_html
    )
    desc = "Browse all {} categories and {} MuleSoft lessons in this free, structured learning path covering Anypoint Platform, DataWeave, connectors, APIs, testing and deployment.".format(TOTAL_CATEGORIES, TOTAL_LESSONS)
    doc = render_page("All MuleSoft Topics — Full Course Index", desc, prefix, "categories/index.html",
                       "categories", body)
    write_file("categories/index.html", doc)


def build_category_page(cat):
    prefix = "../"
    sub_cards = []
    for sub in cat["subtopics"]:
        sub_cards.append(
            '<a class="cat-card" href="{prefix}{spath}">'
            '<div class="card-num">{num:02d}</div><h3>{title}</h3><p>{summary}</p>'
            '<div class="card-meta"><span>{rt}</span><span class="go">Read lesson &rarr;</span></div>'
            '</a>'.format(prefix=prefix, spath=sub_path(cat, sub), num=sub["order"],
                          title=esc(sub["title"]), summary=esc(sub["summary"]), rt=esc(sub["reading_time"]))
        )
    sub_html = "".join(sub_cards)
    bc = breadcrumbs([("Home", prefix + "index.html"), ("All Topics", prefix + "categories/index.html"),
                       (cat["title"], None)])
    body = """{bc}
<div class="page-hero" style="padding-top:0;">
  <span class="badge-soft">Category {num:02d} of {total}</span>
  <h1 style="margin-top:14px;">{title}</h1>
  <p>{desc}</p>
</div>
<div class="cards-grid" style="margin-top:28px;">{cards}</div>""".format(
        bc=bc, num=cat["order"], total=TOTAL_CATEGORIES, title=esc(cat["title"]),
        desc=esc(cat["description"]), cards=sub_html
    )
    desc_meta = "{} {} free lessons in the {} category of the MuleSoft Mastery course.".format(
        cat["description"], len(cat["subtopics"]), cat["title"]
    )[:160]
    doc = render_page(cat["title"], desc_meta, prefix, cat_path(cat), "categories", body,
                       active_cat=cat["slug"])
    write_file(cat_path(cat), doc)


def build_article_page(cat, sub, idx):
    prefix = "../../"
    prev_item = FLAT[idx - 1] if idx > 0 else None
    next_item = FLAT[idx + 1] if idx < len(FLAT) - 1 else None

    pn_parts = []
    if prev_item:
        pcat, psub = prev_item
        pn_parts.append(
            '<a class="pn-card prev" href="{prefix}{spath}"><div class="pn-label">&larr; Previous</div>'
            '<div class="pn-title">{title}</div></a>'.format(
                prefix=prefix, spath=sub_path(pcat, psub), title=esc(psub["title"])
            )
        )
    if next_item:
        ncat, nsub = next_item
        pn_parts.append(
            '<a class="pn-card next" href="{prefix}{spath}"><div class="pn-label">Next &rarr;</div>'
            '<div class="pn-title">{title}</div></a>'.format(
                prefix=prefix, spath=sub_path(ncat, nsub), title=esc(nsub["title"])
            )
        )
    prevnext_html = '<div class="prevnext">{}</div>'.format("".join(pn_parts))

    sib_items = []
    for s in cat["subtopics"]:
        cls = ' class="active"' if s["slug"] == sub["slug"] else ""
        sib_items.append('<li><a href="{prefix}{spath}"{cls}>{num}. {title}</a></li>'.format(
            prefix=prefix, spath=sub_path(cat, s), cls=cls, num=s["order"], title=esc(s["title"])
        ))
    sib_html = "".join(sib_items)

    aside_html = """<div class="aside-col">
  <div style="background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:18px 16px;">
    <div class="sidebar-heading" style="padding:0 0 10px;">In This Category</div>
    <ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:2px;">{sibs}</ul>
  </div>
  <div class="ad-slot ad-sidebar">Ad space<br><small>(Insert your AdSense unit here)</small></div>
</div>""".format(sibs=sib_html)

    bc = breadcrumbs([
        ("Home", prefix + "index.html"),
        ("All Topics", prefix + "categories/index.html"),
        (cat["title"], prefix + cat_path(cat)),
        (sub["title"], None),
    ])

    diagram_html = ""
    if sub["slug"] in DIAGRAM_MAP:
        diagram_html = DIAGRAM_MAP[sub["slug"]]()

    body = """{bc}
<div class="content-shell">
  <article class="article-col">
    <div class="article-header">
      <a class="category-pill" href="{prefix}{cpath}">{cat_title}</a>
      <h1>{title}</h1>
      <div class="article-meta">
        <span>{clock}{rt}</span>
        <span>{layers}Lesson {num} of {total} in {cat_title}</span>
      </div>
    </div>
    {diagram}
    <div class="ad-slot">Advertisement space &mdash; insert your AdSense ad unit code here after approval</div>
    <div class="prose">
{content}
    </div>
    <div class="article-footer">
      <div class="share-row">
        <span class="label">Topic tags:</span>
        <span class="tag-chip">{cat_title}</span>
        <span class="tag-chip">MuleSoft</span>
        <span class="tag-chip">Mule 4</span>
      </div>
      {prevnext}
    </div>
  </article>
  {aside}
</div>""".format(bc=bc, prefix=prefix, cpath=cat_path(cat), cat_title=esc(cat["title"]),
                  title=esc(sub["title"]), clock=ICON_CLOCK, rt=esc(sub["reading_time"]),
                  layers=ICON_LAYERS, num=sub["order"], total=len(cat["subtopics"]),
                  diagram=diagram_html, content=sub["content_html"], prevnext=prevnext_html,
                  aside=aside_html)

    doc = render_page(sub["title"], sub["meta_description"], prefix, sub_path(cat, sub), "categories",
                       body, active_cat=cat["slug"], active_sub=sub["slug"])
    write_file(sub_path(cat, sub), doc)


def build_about():
    prefix = ""
    bc = breadcrumbs([("Home", prefix + "index.html"), ("About", None)])
    body = """{bc}
<div class="page-hero"><h1>About MuleSoft Mastery</h1>
<p>A free, structured, independent learning resource built for developers who want to actually understand
MuleSoft &mdash; not just copy-paste from scattered blog posts.</p></div>
<div class="simple-page">
<div class="prose">
<h2>Why We Built This</h2>
<p>MuleSoft is one of the most widely used integration platforms in the enterprise world, powering
API-led connectivity for thousands of organizations. But learning it well can be hard: official
documentation is scattered across many separate guides, and most tutorials online only cover a single
narrow topic. MuleSoft Mastery was created to solve that problem by organizing every core concept &mdash;
from your very first Mule flow to production deployment and API security &mdash; into one clear,
ordered curriculum.</p>

<h2>Who This Course Is For</h2>
<ul>
<li><strong>Absolute beginners</strong> who are new to integration and want a guided, category-by-category path.</li>
<li><strong>Java or backend developers</strong> transitioning into MuleSoft/Anypoint Platform development.</li>
<li><strong>Certification candidates</strong> preparing for MuleSoft developer or architect certification exams.</li>
<li><strong>Working MuleSoft developers</strong> who want a quick, well-organized reference for DataWeave syntax,
connector configuration, error handling patterns or deployment steps.</li>
</ul>

<h2>How the Course Is Organized</h2>
<p>Content is grouped into {ncat} categories, each containing several focused lessons, for a total of
{nles} lessons. Categories are ordered the way we recommend learning them: start with the fundamentals
of Anypoint Platform and Mule 4 flows, move through DataWeave and connectors, then cover error handling,
API design, testing, deployment and security. Each lesson includes plain-language explanations alongside
realistic code and configuration examples you can adapt in your own projects.</p>

<h2>Always Growing</h2>
<p>This is a living course, not a one-time snapshot &mdash; we're adding new lessons, connectors and
deep-dive topics regularly. If there's a MuleSoft topic you'd like to see covered, let us know on the
<a href="{prefix}contact.html">Contact page</a> and we'll consider it for a future update.</p>

<h2>Independent &amp; Unaffiliated</h2>
<p>MuleSoft Mastery is an independently produced educational resource. It is not affiliated with,
endorsed by, or sponsored by Salesforce, Inc. or MuleSoft, LLC. MuleSoft&reg;, Anypoint Platform&reg; and
related names are registered trademarks of their respective owners and are referenced here purely for
educational and identification purposes. For official product documentation, licensing or support, please
refer to Salesforce's own MuleSoft resources.</p>

<h2>Get In Touch</h2>
<p>Spotted an error, have a suggestion, or want to contribute a correction? We'd love to hear from you &mdash;
visit our <a href="{prefix}contact.html">Contact page</a> to reach us.</p>
</div>
</div>""".format(bc=bc, ncat=TOTAL_CATEGORIES, nles=TOTAL_LESSONS, prefix=prefix)
    desc = "Learn about MuleSoft Mastery, a free and independent MuleSoft learning platform covering Anypoint Platform, Mule 4, DataWeave, connectors, testing, deployment and API security."
    doc = render_page("About Us", desc, prefix, "about.html", "about", body)
    write_file("about.html", doc)


def build_contact():
    prefix = ""
    bc = breadcrumbs([("Home", prefix + "index.html"), ("Contact", None)])
    body = """{bc}
<div class="page-hero"><h1>Contact Us</h1>
<p>Questions about a lesson, suggestions for new topics, corrections, or collaboration ideas &mdash;
we read every message.</p></div>
<div class="simple-page">
<div class="contact-card">
  <div class="ci">{mail_icon}</div>
  <div>
    <div class="cl">Email Us</div>
    <a class="ce" href="mailto:{email}">{email}</a>
  </div>
</div>
<div class="prose">
<h2>What to Email Us About</h2>
<ul>
<li><strong>Content corrections:</strong> found something inaccurate or outdated in a lesson? Let us know
the page and we'll review it.</li>
<li><strong>Topic requests:</strong> want us to cover a MuleSoft concept that isn't in the course yet?</li>
<li><strong>General feedback:</strong> tell us what's working and what could be clearer.</li>
</ul>
<h2>Please Note</h2>
<p>MuleSoft Mastery is an independent educational site and is not an official MuleSoft or Salesforce
support channel. For account, licensing, product bugs or production support issues, please contact
Salesforce/MuleSoft support directly through your Anypoint Platform account. We typically reply to
emails within a few business days.</p>
</div>
</div>""".format(bc=bc, mail_icon=ICON_MAIL, email=CONTACT_EMAIL)
    desc = "Get in touch with the MuleSoft Mastery team for corrections, feedback or topic suggestions. Email us at {}.".format(CONTACT_EMAIL)
    doc = render_page("Contact Us", desc, prefix, "contact.html", "contact", body)
    write_file("contact.html", doc)


def build_privacy():
    prefix = ""
    bc = breadcrumbs([("Home", prefix + "index.html"), ("Privacy Policy", None)])
    body = """{bc}
<div class="page-hero"><h1>Privacy Policy</h1><p>Last updated: August 2026</p></div>
<div class="simple-page">
<div class="prose">
<p>This Privacy Policy explains how {site} ("we", "us", "our", "this site") handles information when you
visit this website. We built this site to be as simple and privacy-respecting as possible: it is a static
website with no user accounts, no logins, and no AI or third-party API integrations of any kind.</p>

<h2>Information We Collect</h2>
<p>We do not directly collect, store, or process any personally identifiable information through this
website. There are no sign-up forms, comment systems, or account features on this site. The client-side
search feature runs entirely in your browser and does not transmit your search queries anywhere.</p>

<h2>Log Data</h2>
<p>Like most websites, the hosting provider (GitHub Pages) may automatically collect standard server log
information such as your browser type, approximate location, referring page, and pages visited. We do not
have access to personally identifying details from these logs beyond what GitHub Pages provides in
aggregate, anonymized form.</p>

<h2>Cookies and Advertising</h2>
<p>This site may display advertisements served by third-party advertising companies, including Google
AdSense. These companies may use cookies, web beacons, or similar technologies to serve ads based on your
prior visits to this or other websites. Google's use of advertising cookies enables it and its partners to
serve ads based on your visits to this site and/or other sites on the Internet. You may opt out of
personalized advertising by visiting Google's Ads Settings. Third-party vendors, including Google, use
cookies to serve ads based on a user's prior visits to this website or other websites.</p>

<h2>Third-Party Links</h2>
<p>This site may contain links to external websites, including official MuleSoft/Salesforce documentation.
We are not responsible for the privacy practices or content of external sites. We encourage you to review
the privacy policy of any third-party site you visit.</p>

<h2>Children's Privacy</h2>
<p>This website is not directed at children under the age of 13, and we do not knowingly collect personal
information from children.</p>

<h2>Changes to This Policy</h2>
<p>We may update this Privacy Policy from time to time. Any changes will be posted on this page with an
updated revision date.</p>

<h2>Contact Us</h2>
<p>If you have questions about this Privacy Policy, please email us at
<a href="mailto:{email}">{email}</a>.</p>
</div>
</div>""".format(bc=bc, site=esc(SITE_NAME), email=CONTACT_EMAIL)
    desc = "Read the Privacy Policy for {}, covering data collection, cookies, third-party advertising and how to contact us with privacy questions.".format(SITE_NAME)
    doc = render_page("Privacy Policy", desc, prefix, "privacy-policy.html", None, body)
    write_file("privacy-policy.html", doc)


def build_disclaimer():
    prefix = ""
    bc = breadcrumbs([("Home", prefix + "index.html"), ("Disclaimer", None)])
    body = """{bc}
<div class="page-hero"><h1>Disclaimer &amp; Terms of Use</h1><p>Last updated: August 2026</p></div>
<div class="simple-page">
<div class="prose">
<h2>Educational Purpose Only</h2>
<p>All content on {site} is provided for general educational and informational purposes only. While we
strive to keep lessons accurate and up to date with real MuleSoft and Anypoint Platform concepts, we make
no warranties or guarantees, express or implied, about the completeness, accuracy, reliability, or
suitability of the information for any particular purpose. Any reliance you place on this information is
strictly at your own risk.</p>

<h2>Not Official MuleSoft Documentation</h2>
<p>This website is an independently produced learning resource and is not affiliated with, endorsed by,
sponsored by, or officially connected to Salesforce, Inc. or MuleSoft, LLC in any way. For authoritative,
up-to-date product documentation, licensing terms, or official support, please refer directly to
Salesforce's official MuleSoft resources.</p>

<h2>Trademark Notice</h2>
<p>MuleSoft&reg;, Anypoint Platform&reg;, Anypoint Studio&reg;, DataWeave&reg;, CloudHub&reg;, Runtime
Fabric&reg;, and other related names, logos, and marks are registered trademarks of Salesforce, Inc.
and/or MuleSoft, LLC. All other product and company names mentioned on this site may be trademarks of
their respective owners. Use of these names, logos, and brands on {site} is for identification and
educational reference purposes only and does not imply endorsement.</p>

<h2>No Professional Advice</h2>
<p>Nothing on this site constitutes professional, legal, or architectural consulting advice. Before making
production decisions based on any concept described here, validate the approach against official
documentation and your organization's specific requirements.</p>

<h2>External Links</h2>
<p>This site may link to third-party websites that are not owned or controlled by {site}. We have no
control over, and assume no responsibility for, the content, privacy policies, or practices of any
third-party websites.</p>

<h2>Limitation of Liability</h2>
<p>In no event shall {site} or its contributors be liable for any direct, indirect, incidental,
consequential, or special damages arising out of or in any way connected with the use of this website or
the information contained within it.</p>

<h2>Acceptable Use</h2>
<p>You may read, share, and link to content on this site for personal and educational use. Wholesale
reproduction or republishing of lesson content on other websites without prior written permission is not
permitted.</p>

<h2>Changes</h2>
<p>We may revise this Disclaimer and these Terms of Use at any time without prior notice. Continued use of
the site after changes are posted constitutes acceptance of the revised terms.</p>

<h2>Contact</h2>
<p>Questions about this disclaimer can be sent to <a href="mailto:{email}">{email}</a>.</p>
</div>
</div>""".format(bc=bc, site=esc(SITE_NAME), email=CONTACT_EMAIL)
    desc = "Disclaimer and Terms of Use for {} — an independent MuleSoft educational resource not affiliated with Salesforce or MuleSoft, LLC.".format(SITE_NAME)
    doc = render_page("Disclaimer & Terms of Use", desc, prefix, "disclaimer.html", None, body)
    write_file("disclaimer.html", doc)


def build_404():
    prefix = ""
    body = """<div class="error-page">
  <div>
    <div class="code">404</div>
    <h1>Lesson Not Found</h1>
    <p>The page you're looking for doesn't exist or may have moved. Let's get you back on track.</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-primary" href="{prefix}index.html">Go to Homepage</a>
      <a class="btn btn-outline" href="{prefix}categories/index.html">Browse All Topics</a>
    </div>
  </div>
</div>""".format(prefix=prefix)
    doc = render_bare_page("Page Not Found", "The page you requested could not be found on MuleSoft Mastery.",
                            prefix, "404.html", None, body)
    write_file("404.html", doc)


def build_sitemap():
    urls = ["index.html", "about.html", "contact.html", "privacy-policy.html", "disclaimer.html",
            "categories/index.html"]
    for cat in CATEGORIES:
        urls.append(cat_path(cat))
    for cat, sub in FLAT:
        urls.append(sub_path(cat, sub))
    entries = "\n".join(
        "  <url><loc>{}/{}</loc><changefreq>monthly</changefreq></url>".format(SITE_URL, u) for u in urls
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           '{}\n</urlset>\n').format(entries)
    write_file("sitemap.xml", xml)


def build_robots():
    txt = "User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n".format(SITE_URL)
    write_file("robots.txt", txt)


def strip_tags(text):
    import re
    return re.sub("<[^>]+>", " ", text)


def build_search_items():
    items = []
    for cat in CATEGORIES:
        items.append({
            "title": cat["title"],
            "url": cat_path(cat),
            "category": "Category",
            "summary": cat["description"],
            "keywords": cat["slug"].replace("-", " "),
        })
    for cat, sub in FLAT:
        items.append({
            "title": sub["title"],
            "url": sub_path(cat, sub),
            "category": cat["title"],
            "summary": sub["summary"],
            "keywords": "{} {}".format(cat["slug"], sub["slug"]).replace("-", " "),
        })
    return items


SEARCH_ITEMS = build_search_items()
# Safe to embed inline in every page's <script> tag (escape "</" so a literal
# "</script>" can never appear inside the JSON string and close the tag early).
SEARCH_ITEMS_JS = json.dumps(SEARCH_ITEMS, ensure_ascii=False, indent=None).replace("</", "<\\/")


def build_search_index():
    write_file("assets/js/search-index.json", json.dumps(SEARCH_ITEMS, ensure_ascii=False, indent=None))


# --------------------------------------------------------------- Main ------
def main():
    build_home()
    build_categories_index()
    for cat in CATEGORIES:
        build_category_page(cat)
    for idx, (cat, sub) in enumerate(FLAT):
        build_article_page(cat, sub, idx)
    build_about()
    build_contact()
    build_privacy()
    build_disclaimer()
    build_404()
    build_sitemap()
    build_robots()
    build_search_index()

    html_count = sum(1 for _ in OUT_DIR.rglob("*.html"))
    print("Generated {} HTML files, {} categories, {} lessons.".format(html_count, TOTAL_CATEGORIES, TOTAL_LESSONS))


if __name__ == "__main__":
    main()
