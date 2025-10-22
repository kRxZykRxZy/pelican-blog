#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Single-file Pelican blog with Markdown support,
build, serve, and automatic reload (like Codeberg style).
"""

import os
import sys
import shutil
import webbrowser
from pathlib import Path
import shlex
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG

try:
    from livereload import Server
except ImportError:
    Server = None  # optional for live reload

# --- Site configuration ---
SITE_TITLE = "SnapLabs - Blog"
SITE_AUTHOR = "SnapLabs Team"
SITE_DESCRIPTION = "Exploring code, design, and innovation from SnapLabs."
OUTPUT_PATH = Path("output").resolve()
CONTENT_PATH = Path("content").resolve()
THEME = "notmyidea"  # Pelican built-in clean theme
DEFAULT_LANG = "en"

# --- Pelican settings dict ---
SETTINGS = DEFAULT_CONFIG.copy()
SETTINGS.update({
    "SITENAME": SITE_TITLE,
    "AUTHOR": SITE_AUTHOR,
    "SITEDESCRIPTION": SITE_DESCRIPTION,
    "PATH": str(CONTENT_PATH),
    "OUTPUT_PATH": str(OUTPUT_PATH),
    "THEME": THEME,
    "TIMEZONE": "UTC",
    "DEFAULT_LANG": DEFAULT_LANG,
    "DELETE_OUTPUT_DIRECTORY": True,
    "MARKUP": ["md"],
    "RELATIVE_URLS": True,
    "FEED_ALL_ATOM": None,
    "CATEGORY_FEED_ATOM": None,
    "TRANSLATION_FEED_ATOM": None,
    "DEFAULT_PAGINATION": 10,
})

# --- Ensure content/output folders exist ---
CONTENT_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# --- Sample post if none exist ---
sample_post = CONTENT_PATH / "hello-world.md"
if not sample_post.exists():
    sample_post.write_text(f"""Title: Hello World
Date: 2025-10-22
Category: General
Author: {SITE_AUTHOR}

Welcome to **{SITE_TITLE}** — your home for ideas!
""")

# --- Helper functions ---
def pelican_build():
    """Build the site using Pelican"""
    print("🔧 Building Pelican site...")
    pelican_main(shlex.split("-s none"))  # config passed programmatically

def serve_site(host="localhost", port=8000):
    """Serve the static site with Pelican server"""
    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        str(OUTPUT_PATH),
        (host, port),
        ComplexHTTPRequestHandler
    )

    print(f"🚀 Serving at http://{host}:{port}")
    webbrowser.open(f"http://{host}:{port}")
    server.serve_forever()

def livereload_site(host="localhost", port=8000):
    """Serve with live reload (requires livereload package)"""
    if Server is None:
        print("⚠️ livereload package not installed. Install with `pip install livereload`")
        serve_site(host, port)
        return

    def build_wrapper():
        pelican_main([])

    server = Server()
    server.watch(str(CONTENT_PATH / "*.md"), build_wrapper)
    server.watch(str(CONTENT_PATH / "**/*.md"), build_wrapper)
    server.serve(root=str(OUTPUT_PATH), host=host, port=port, open_url_delay=1)

# --- CLI interface ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SnapLabs Single-File Pelican Blog")
    parser.add_argument("command", choices=["build", "serve", "livereload"], help="Action to perform")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # Inject settings programmatically into Pelican
    pelican_main_settings = SETTINGS.copy()
    pelican_main_settings["_original_config"] = pelican_main_settings

    if args.command == "build":
        pelican_build()
    elif args.command == "serve":
        pelican_build()
        serve_site(args.host, args.port)
    elif args.command == "livereload":
        pelican_build()
        livereload_site(args.host, args.port)
