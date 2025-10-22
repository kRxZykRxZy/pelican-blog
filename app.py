import os
import subprocess
from pathlib import Path

# --- Basic site info ---
SITE_TITLE = "SnapLabs - Blog"
SITE_DESCRIPTION = "A light and modern blog from SnapLabs."
THEME_NAME = "purelight"

# --- Directory setup ---
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "output"
THEME_DIR = BASE_DIR / "theme" / THEME_NAME

# --- Create folders if missing ---
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
THEME_DIR.mkdir(parents=True, exist_ok=True)

# --- Generate a sample Markdown post if none exist ---
sample_post = CONTENT_DIR / "hello-world.md"
if not sample_post.exists():
    sample_post.write_text(f"""Title: Hello World
Date: 2025-10-22
Category: General
Author: SnapLabs

Welcome to **{SITE_TITLE}** — your home for light blue ideas 💡!
""")

# --- Create a simple light blue and white theme ---
(THEME_DIR / "static" / "css").mkdir(parents=True, exist_ok=True)
css = """
body {
  background-color: #f0f8ff;
  color: #002b5c;
  font-family: "Segoe UI", sans-serif;
  margin: 2rem auto;
  max-width: 800px;
  line-height: 1.6;
}
a { color: #007fff; }
header, footer {
  text-align: center;
  background: #e6f2ff;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}
"""
(THEME_DIR / "static" / "css" / "style.css").write_text(css)

# --- Minimal base template ---
templates_dir = THEME_DIR / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)
(templates_dir / "base.html").write_text(f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{{{ SITENAME }}}}</title>
    <meta name="description" content="{{{{ SITEDESCRIPTION }}}}">
    <link rel="stylesheet" href="{{{{ THEME_STATIC_DIR }}}}/css/style.css">
  </head>
  <body>
    <header>
      <h1>{{{{ SITENAME }}}}</h1>
      <p>{{{{ SITEDESCRIPTION }}}}</p>
    </header>
    <main>
      {{{{ content }}}}
    </main>
    <footer>
      <p>© 2025 SnapLabs</p>
    </footer>
  </body>
</html>
""")

# --- Pelican config file ---
pelicanconf = f"""
SITENAME = '{SITE_TITLE}'
SITEDESCRIPTION = '{SITE_DESCRIPTION}'
PATH = 'content'
TIMEZONE = 'UTC'
DEFAULT_LANG = 'en'
THEME = '{THEME_DIR.as_posix()}'
THEME_STATIC_DIR = 'theme/static'
MARKUP = ['md']
"""
(BASE_DIR / "pelicanconf.py").write_text(pelicanconf)

# --- Run pelican and local server ---
print("🔧 Building Pelican site...")
subprocess.run(["pelican", "content", "-s", "pelicanconf.py"], check=True)

print("🚀 Starting local server at http://localhost:8000 ...")
subprocess.run(["python", "-m", "http.server", "8000", "--directory", str(OUTPUT_DIR)])
