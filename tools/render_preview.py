#!/usr/bin/env python3
"""
A deliberately small Jekyll stand-in, used only to preview this site locally.

rubygems.org is unreachable from this sandbox, so `jekyll build` cannot run here.
This script reproduces just enough of Jekyll to render the handful of templates
in this repo: front matter, collections, layout chaining, textual {% include %}
inlining, and the Liquid filters these templates actually use.

It is a verification aid, not a build tool. GitHub Pages still does the real build.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

import frontmatter
import markdown as md
import yaml
from liquid import Environment

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_preview"

MD = md.Markdown(extensions=["extra", "tables", "attr_list", "sane_lists", "smarty"])


def render_md(text: str) -> str:
    MD.reset()
    return MD.convert(text)


# --------------------------------------------------------------------------- #
# site object
# --------------------------------------------------------------------------- #

def load_config() -> dict:
    raw = (ROOT / "_config.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load(raw)
    data = {}
    for f in (ROOT / "_data").glob("*.yml"):
        data[f.stem] = yaml.safe_load(f.read_text(encoding="utf-8"))
    cfg["data"] = data
    cfg["time"] = dt.datetime.now(dt.timezone.utc)
    # preview is served from a local root: make base_path relative
    cfg["url"] = ""
    cfg["baseurl"] = ""
    return cfg


def as_date(v):
    if isinstance(v, dt.datetime):
        return v
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day)
    if isinstance(v, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(v.strip()[:19], fmt)
            except ValueError:
                continue
    return None


def load_docs(folder: str, permalink_tpl: str) -> list[dict]:
    d = ROOT / folder
    if not d.is_dir():
        return []
    docs = []
    for f in sorted(d.glob("*.md")):
        post = frontmatter.load(f)
        doc = dict(post.metadata)
        doc["raw"] = post.content
        doc["path"] = str(f.relative_to(ROOT))
        doc["id"] = f"/{folder.strip('_')}/{f.stem}"
        doc["date"] = as_date(doc.get("date"))

        if folder == "_posts":
            m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)", f.stem)
            slug = m.group(4) if m else f.stem
            if doc["date"] is None and m:
                doc["date"] = dt.datetime(*map(int, m.group(1, 2, 3)))
            doc["url"] = doc.get("permalink") or f"/{slug}/"
        else:
            doc["url"] = doc.get("permalink") or permalink_tpl.replace(":path", f.stem)
        docs.append(doc)
    return docs


# --------------------------------------------------------------------------- #
# include inlining
# --------------------------------------------------------------------------- #

INCLUDE_RE = re.compile(r"\{%-?\s*include\s+([^\s%}]+)((?:\s+[^%}]*)?)-?%\}")


def inline_includes(text: str, depth: int = 0) -> str:
    if depth > 8:
        return text

    def sub(m: re.Match) -> str:
        name = m.group(1).strip().strip("'\"").lstrip("/")
        params = m.group(2).strip()
        path = ROOT / "_includes" / name
        if not path.is_file():
            return f"<!-- missing include: {name} -->"
        body = path.read_text(encoding="utf-8")
        if params:  # {% include x.html type="grid" %}
            assigns = []
            for k, v in re.findall(r"(\w+)\s*=\s*(\"[^\"]*\"|'[^']*'|\S+)", params):
                assigns.append(f"{{% assign include_{k} = {v} %}}")
            body = re.sub(r"include\.(\w+)", r"include_\1", body)
            body = "".join(assigns) + body
        else:
            body = re.sub(r"include\.(\w+)", r"include_\1", body)
        return inline_includes(body, depth + 1)

    return INCLUDE_RE.sub(sub, text)


# --------------------------------------------------------------------------- #
# filters
# --------------------------------------------------------------------------- #

STRFTIME = {
    "%Y": "%Y", "%m": "%m", "%d": "%d", "%B": "%B", "%b": "%b",
    "%H": "%H", "%M": "%M", "%S": "%S", "%e": "%d", "%-d": "%d",
}


def f_date(value, fmt="%Y-%m-%d"):
    if value in (None, ""):
        return ""
    if isinstance(value, str) and value.lower() == "now":
        value = dt.datetime.now(dt.timezone.utc)
    d = as_date(value) if not isinstance(value, dt.datetime) else value
    if d is None:
        return str(value)
    fmt = fmt.replace("%-d", "%d").replace("%e", "%d")
    return d.strftime(fmt)


def f_date_to_xmlschema(value):
    d = as_date(value) if not isinstance(value, dt.datetime) else value
    return d.isoformat() if d else ""


def f_slugify(value, *_a):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def f_markdownify(value):
    return render_md(str(value or ""))


def f_strip_html(value):
    return re.sub(r"<[^>]+>", "", str(value or ""))


def f_strip_newlines(value):
    return str(value or "").replace("\n", "").replace("\r", "")


def f_escape_once(value):
    return html.escape(str(value or ""), quote=True)


def f_jsonify(value):
    return json.dumps(value, default=str)


def f_number_of_words(value):
    return len(str(value or "").split())


def f_relative_url(value):
    v = str(value or "")
    return v if v.startswith(("http", "/")) else "/" + v


def f_absolute_url(value, site_url=""):
    return f_relative_url(value)


def f_truncate(value, n=50, ell="..."):
    s = str(value or "")
    return s if len(s) <= n else s[: max(0, n - len(ell))] + ell


def f_divided_by(value, n):
    try:
        return int(value) // int(n)
    except Exception:
        return 0


def build_env() -> Environment:
    env = Environment()
    for name, fn in {
        "date": f_date,
        "date_to_xmlschema": f_date_to_xmlschema,
        "date_to_string": f_date,
        "slugify": f_slugify,
        "markdownify": f_markdownify,
        "strip_html": f_strip_html,
        "strip_newlines": f_strip_newlines,
        "escape_once": f_escape_once,
        "jsonify": f_jsonify,
        "number_of_words": f_number_of_words,
        "relative_url": f_relative_url,
        "absolute_url": f_absolute_url,
        "truncate": f_truncate,
        "divided_by": f_divided_by,
        "xml_escape": f_escape_once,
    }.items():
        env.add_filter(name, fn)
    return env


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #

def render_with_layouts(env, body_html, page, site, layout_name):
    seen = 0
    content = body_html
    while layout_name and seen < 6:
        seen += 1
        lp = ROOT / "_layouts" / f"{layout_name}.html"
        if not lp.is_file():
            break
        post = frontmatter.load(lp)
        tpl_src = inline_includes(post.content)
        tpl = env.from_string(tpl_src)
        content = tpl.render(site=site, page=page, content=content, paginator=None)
        layout_name = post.metadata.get("layout")
    return content


def main():
    site = load_config()
    site["publications"] = load_docs("_publications", "/publication/:path")
    site["posts"] = sorted(
        load_docs("_posts", "/:path/"),
        key=lambda d: d["date"] or dt.datetime.min,
        reverse=True,
    )
    site["talks"] = load_docs("_talks", "/talks/:path/")
    site["teaching"] = load_docs("_teaching", "/teaching/:path/")
    site["portfolio"] = load_docs("_portfolio", "/portfolio/:path/")
    site["related_posts"] = []
    site["categories"] = {}
    site["tags"] = {}

    env = build_env()

    # give every collection doc a rendered `content`, needed by read-time
    for coll in ("publications", "posts", "talks", "teaching", "portfolio"):
        for d in site[coll]:
            d["content"] = render_md(d.get("raw", ""))

    targets = []

    for f in sorted((ROOT / "_pages").glob("*")):
        if f.suffix not in (".md", ".html"):
            continue
        if f.stem in ("404", "markdown", "sitemap", "terms", "talkmap",
                      "cv-json", "non-menu-page", "archive-layout-with-content",
                      "page-archive", "category-archive", "tag-archive",
                      "collection-archive", "talks", "portfolio"):
            continue
        targets.append(("page", f))

    for d in site["posts"]:
        targets.append(("post", d))
    for d in site["publications"][:1]:
        targets.append(("publication", d))

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # static assets the preview needs
    for rel in ("assets", "images", "files"):
        src = ROOT / rel
        if src.is_dir():
            shutil.copytree(src, OUT / rel, dirs_exist_ok=True)

    written = []
    for kind, item in targets:
        if kind == "page":
            post = frontmatter.load(item)
            page = dict(post.metadata)
            page["raw"] = post.content
            page["url"] = page.get("permalink", "/" + item.stem + "/")
            is_md = item.suffix == ".md"
        else:
            page = dict(item)
            page["raw"] = item.get("raw", "")
            is_md = True

        layout = page.get("layout") or "single"

        body_src = inline_includes(page["raw"])
        try:
            body = env.from_string(body_src).render(site=site, page=page, post=page,
                                                    content="", paginator=None)
        except Exception as e:  # noqa: BLE001
            print(f"  !! liquid error in {page.get('url')}: {e}", file=sys.stderr)
            body = f"<pre>LIQUID ERROR: {html.escape(str(e))}</pre>"

        if is_md:
            body = render_md(body)
        page["content"] = body

        try:
            out_html = render_with_layouts(env, body, page, site, layout)
        except Exception as e:  # noqa: BLE001
            print(f"  !! layout error in {page.get('url')}: {e}", file=sys.stderr)
            continue

        url = page["url"].strip("/")
        dest = OUT / (url + "/index.html" if url else "index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out_html, encoding="utf-8")
        written.append(str(dest.relative_to(OUT)))

    # main.css: the SCSS is font-awesome only; the preview does not need icons
    (OUT / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "css" / "main.css").write_text(
        "/* preview stub: font-awesome only in the real build */\n", encoding="utf-8"
    )

    print(f"rendered {len(written)} pages into {OUT}")
    for w in written:
        print("  ", w)


if __name__ == "__main__":
    main()
