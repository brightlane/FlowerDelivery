import os
import json
import gzip
from datetime import datetime

# =====================================================
# 🥇 CORE CONFIG
# =====================================================

AFFILIATE_ID = "2013017799"
BASE_URL = "https://www.floristone.com/main.cfm"
SITE_URL = "https://brightlane.github.io/FlowerDelivery/"
OUTPUT = "output"

OCCASIONS = [
    "flower-delivery",
    "birthday-flowers",
    "sympathy-flowers",
    "anniversary-flowers",
    "romance-flowers",
    "mothers-day-flowers"
]

LANGS = ["en", "es", "fr"]

# =====================================================
# 🔗 AFFILIATE ENGINE
# =====================================================

def aff_link(topic):
    return f"{BASE_URL}?occ={topic}&source_id=aff&affiliate_id={AFFILIATE_ID}"

# =====================================================
# 🧠 SEO HELPERS
# =====================================================

def keywords(topic):
    return [
        f"{topic} flowers",
        f"send {topic} flowers online",
        f"best {topic} flower delivery",
        f"cheap {topic} bouquets",
        f"same day {topic} delivery",
        f"luxury {topic} arrangements",
    ]

def internal_links():
    return {o: [x for x in OCCASIONS if x != o] for o in OCCASIONS}

def crosslinks(topic):
    return "\n".join(
        f'<a href="{l}.html">{l.replace("-", " ").title()}</a>'
        for l in internal_links().get(topic, OCCASIONS)
    )

# =====================================================
# 🧠 SCHEMA
# =====================================================

def schema(topic):
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{topic}",
  "offers": {{
    "@type": "Offer",
    "url": "{aff_link(topic)}",
    "availability": "https://schema.org/InStock"
  }}
}}
</script>
"""

def schema_org():
    return """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Flower Delivery Affiliate Site",
  "url": "https://brightlane.github.io/FlowerDelivery/"
}
</script>
"""

def schema_website():
    return """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Flower Delivery Hub",
  "url": "https://brightlane.github.io/FlowerDelivery/"
}
</script>
"""

# =====================================================
# 🌍 SEO META (FULL UPGRADE)
# =====================================================

def canonical(topic):
    return f'<link rel="canonical" href="{SITE_URL}{topic}.html"/>'

def hreflang(topic):
    return "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{l}/{topic}.html"/>'
        for l in LANGS
    )

def og_tags(topic):
    return f"""
<meta property="og:title" content="{topic.title()} Flowers">
<meta property="og:url" content="{SITE_URL}{topic}.html">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
"""

# =====================================================
# 🌐 PAGE
# =====================================================

def page(topic):
    return f"""
<html>
<head>
<title>{topic.title()}</title>
<meta name="robots" content="index, follow">

{canonical(topic)}
{hreflang(topic)}
{og_tags(topic)}
{schema(topic)}
{schema_org()}
{schema_website()}
</head>

<body>
<h1>{topic.title()}</h1>
<p>Premium flower delivery for {topic}.</p>
<a href="{aff_link(topic)}">Order Now</a>
{crosslinks(topic)}
</body>
</html>
"""

# =====================================================
# ✍️ BLOG
# =====================================================

def blog(topic):
    filler = ("flower " + topic + " ") * 1200

    return f"""
<html>
<head>
<title>{topic.title()} Guide</title>
<meta name="robots" content="index, follow">

{canonical(topic)}
{hreflang(topic)}
{og_tags(topic)}
{schema(topic)}
{schema_org()}
{schema_website()}
</head>

<body>
<h1>{topic.title()} Guide</h1>
<p>{topic} flowers for every occasion.</p>
<p>{", ".join(keywords(topic))}</p>
<a href="{aff_link(topic)}">Send Flowers</a>
{crosslinks(topic)}
<p>{filler}</p>
</body>
</html>
"""

# =====================================================
# 🧭 INDEX
# =====================================================

def index():
    links = "\n".join(
        f'<li><a href="{o}.html">{o}</a></li>' for o in OCCASIONS
    )

    return f"""
<html>
<head>
<title>Flower Hub</title>
{schema_org()}
{schema_website()}
</head>
<body>
<h1>Flower Delivery Hub</h1>
<ul>{links}</ul>
<a href="blog.html">Blog Hub</a>
</body>
</html>
"""

def blog_index():
    links = "\n".join(
        f'<li><a href="blog-{o}.html">{o}</a></li>' for o in OCCASIONS
    )

    return f"""
<html>
<head><title>Blog Hub</title></head>
<body>
<h1>Blog Hub</h1>
<ul>{links}</ul>
</body>
</html>
"""

# =====================================================
# 🧭 SEO FILES (FULL ADDITION)
# =====================================================

def robots():
    return f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}sitemap.xml
"""

def llms():
    return "Flower SEO affiliate system for AI indexing"

def humans():
    return "Built by automated SEO generator"

def ads():
    return "google.com, pub-0000000000000000, DIRECT"

def manifest():
    return json.dumps({
        "name": "Flower Hub",
        "start_url": "/",
        "display": "standalone"
    }, indent=2)

def favicon():
    return "FAKE FAVICON PLACEHOLDER"

def sitemap():
    urls = ""
    for o in OCCASIONS:
        urls += f"<url><loc>{SITE_URL}{o}.html</loc></url>\n"
        urls += f"<url><loc>{SITE_URL}blog-{o}.html</loc></url>\n"
        for l in LANGS:
            urls += f"<url><loc>{SITE_URL}{l}/{o}.html</loc></url>\n"
    return f"<urlset>{urls}</urlset>"

def sitemap_gz():
    raw = sitemap().encode("utf-8")
    return gzip.compress(raw)

# =====================================================
# 📦 BUILD SYSTEM
# =====================================================

def build():
    os.makedirs(OUTPUT, exist_ok=True)

    for o in OCCASIONS:
        with open(f"{OUTPUT}/{o}.html", "w") as f:
            f.write(page(o))

        with open(f"{OUTPUT}/blog-{o}.html", "w") as f:
            f.write(blog(o))

        for l in LANGS:
            os.makedirs(f"{OUTPUT}/{l}", exist_ok=True)
            with open(f"{OUTPUT}/{l}/{o}.html", "w") as f:
                f.write(page(o))

    # CORE FILES
    with open(f"{OUTPUT}/index.html", "w") as f:
        f.write(index())

    with open(f"{OUTPUT}/blog.html", "w") as f:
        f.write(blog_index())

    # SEO FILES
    with open(f"{OUTPUT}/robots.txt", "w") as f:
        f.write(robots())

    with open(f"{OUTPUT}/llms.txt", "w") as f:
        f.write(llms())

    with open(f"{OUTPUT}/humans.txt", "w") as f:
        f.write(humans())

    with open(f"{OUTPUT}/ads.txt", "w") as f:
        f.write(ads())

    with open(f"{OUTPUT}/manifest.json", "w") as f:
        f.write(manifest())

    with open(f"{OUTPUT}/sitemap.xml", "w") as f:
        f.write(sitemap())

    with open(f"{OUTPUT}/sitemap.xml.gz", "wb") as f:
        f.write(sitemap_gz())

    with open(f"{OUTPUT}/.nojekyll", "w") as f:
        f.write("")

    with open(f"{OUTPUT}/favicon.ico", "w") as f:
        f.write(favicon())

    print("FULL PRODUCTION SEO SYSTEM BUILT")

# RUN
build()
