#!/usr/bin/env python3
"""
Export all pages and posts (all WPML languages) from the nc-wiki.ch WordPress
REST API into Hugo-flavored Markdown files under import/.

Usage:
    pip install requests markdownify pyyaml
    python scripts/import_wp.py

Output layout:
    import/<lang>/pages/<slug>.md
    import/<lang>/posts/<slug>.md

Each file gets a YAML frontmatter block (title, dates, original slug/id/link,
parent, author, categories/tags, featured image) followed by the page body
converted from HTML to Markdown.

This is a one-off migration dump for manual review, not wired into the live
Hugo content/ tree.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
import unicodedata
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Missing dependency 'requests'. Install with: pip install requests")

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency 'pyyaml'. Install with: pip install pyyaml")

try:
    from markdownify import markdownify as html_to_markdown
except ImportError:
    sys.exit("Missing dependency 'markdownify'. Install with: pip install markdownify")


BASE_URL = "https://www.nc-wiki.ch/wp-json/wp/v2"
LANGUAGES = ["de", "fr", "it"]
POST_TYPES = ["pages", "posts"]
PER_PAGE = 100
REQUEST_DELAY_SECONDS = 1.5  # pause between requests so we don't hammer the server
USER_AGENT = "nc-wiki-hugo-migration/1.0 (+https://github.com/Kroeppster/nc-wiki)"

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})


def fetch_all(post_type: str, lang: str) -> list[dict]:
    """Fetch every item of a post type in a given language, following pagination."""
    items: list[dict] = []
    page = 1
    while True:
        params = {
            "per_page": PER_PAGE,
            "page": page,
            "wpml_language": lang,
            "_embed": 1,
            "status": "publish",
        }
        url = f"{BASE_URL}/{post_type}"
        resp = session.get(url, params=params, timeout=30)
        time.sleep(REQUEST_DELAY_SECONDS)

        if resp.status_code == 400:
            # WP returns 400 once you page past the last available page
            break
        resp.raise_for_status()

        batch = resp.json()
        if not batch:
            break
        items.extend(batch)

        total_pages = int(resp.headers.get("X-WP-TotalPages", "1"))
        if page >= total_pages:
            break
        page += 1

    return items


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()


def clean_text(value: str) -> str:
    return html.unescape(strip_html(value)).strip()


def html_body_to_markdown(rendered_html: str) -> str:
    md = html_to_markdown(
        rendered_html or "",
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )
    md = html.unescape(md)
    # collapse runs of blank lines left behind by Elementor's wrapper divs
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def slugify_fallback(title: str, item_id: int) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug or f"item-{item_id}"


def extract_embedded_terms(item: dict) -> tuple[list[str], list[str]]:
    """Return (category_names, tag_names) from the _embedded payload, if present."""
    categories: list[str] = []
    tags: list[str] = []
    term_groups = item.get("_embedded", {}).get("wp:term", [])
    for group in term_groups:
        for term in group:
            name = term.get("name")
            taxonomy = term.get("taxonomy")
            if not name:
                continue
            if taxonomy == "category":
                categories.append(name)
            elif taxonomy == "post_tag":
                tags.append(name)
    return categories, tags


def extract_author(item: dict) -> str | None:
    authors = item.get("_embedded", {}).get("author", [])
    if authors and isinstance(authors, list):
        return authors[0].get("name")
    return None


def extract_featured_image(item: dict) -> str | None:
    media = item.get("_embedded", {}).get("wp:featuredmedia", [])
    if media and isinstance(media, list):
        return media[0].get("source_url")
    return None


def build_frontmatter(item: dict, post_type: str, lang: str, parent_slug: str | None) -> dict:
    title = clean_text(item.get("title", {}).get("rendered", ""))
    excerpt = clean_text(item.get("excerpt", {}).get("rendered", ""))

    frontmatter = {
        "title": title,
        "date": item.get("date"),
        "lastmod": item.get("modified"),
        "draft": False,
        "slug": item.get("slug"),
        "original_id": item.get("id"),
        "original_link": item.get("link"),
        "original_lang": lang,
        "original_type": post_type,
    }

    if excerpt:
        frontmatter["description"] = excerpt

    author = extract_author(item)
    if author:
        frontmatter["author"] = author

    featured_image = extract_featured_image(item)
    if featured_image:
        frontmatter["featured_image"] = featured_image

    if post_type == "posts":
        categories, tags = extract_embedded_terms(item)
        if categories:
            frontmatter["categories"] = categories
        if tags:
            frontmatter["tags"] = tags

    if post_type == "pages":
        frontmatter["menu_order"] = item.get("menu_order", 0)
        if parent_slug:
            frontmatter["parent_slug"] = parent_slug

    return frontmatter


def write_markdown_file(out_dir: Path, item: dict, post_type: str, lang: str, parent_slug: str | None) -> Path:
    slug = item.get("slug") or slugify_fallback(
        clean_text(item.get("title", {}).get("rendered", "")), item.get("id", 0)
    )
    frontmatter = build_frontmatter(item, post_type, lang, parent_slug)
    body = html_body_to_markdown(item.get("content", {}).get("rendered", ""))

    target_dir = out_dir / lang / post_type
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    fm_yaml = yaml.safe_dump(
        frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
    )
    target_path.write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")
    return target_path


def main() -> None:
    global REQUEST_DELAY_SECONDS

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="import", help="Output directory (default: import/)")
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY_SECONDS,
        help=f"Seconds to wait between HTTP requests (default: {REQUEST_DELAY_SECONDS})",
    )
    args = parser.parse_args()

    REQUEST_DELAY_SECONDS = args.delay

    out_dir = Path(args.out_dir)
    total_written = 0

    for lang in LANGUAGES:
        for post_type in POST_TYPES:
            print(f"Fetching {post_type} [{lang}] ...")
            items = fetch_all(post_type, lang)
            print(f"  -> {len(items)} item(s)")

            id_to_slug = {item["id"]: item.get("slug") for item in items}

            for item in items:
                parent_id = item.get("parent")
                parent_slug = id_to_slug.get(parent_id) if parent_id else None
                path = write_markdown_file(out_dir, item, post_type, lang, parent_slug)
                total_written += 1
                print(f"  wrote {path}")

    print(f"\nDone. {total_written} Markdown file(s) written to {out_dir}/")


if __name__ == "__main__":
    main()
