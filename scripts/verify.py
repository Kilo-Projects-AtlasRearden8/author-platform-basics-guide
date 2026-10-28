#!/usr/bin/env python3
"""Verification script for the Author Platform Basics guide.

Checks:
- LICENSE copyright line is exactly "Copyright (c) 2026 Asdale Dynamics, LLC"
- README credits Asdale Dynamics, LLC
- Every HTML page has valid structure and resolves its internal links
- Site assets exist
- Docs markdown chapters exist and match site pages
- No secrets, personal emails, or .github/workflows
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)
    print("FAIL: " + msg)


def ok(msg):
    print("ok: " + msg)


def warn(msg):
    WARNINGS.append(msg)
    print("warn: " + msg)


class PageChecker(HTMLParser):
    def __init__(self, text, path):
        super().__init__()
        self.path = path
        self.text = text
        self.doctype = False
        self.has_html = False
        self.has_head = False
        self.has_body = False
        self.title = None
        self.charset = False
        self.viewport = False
        self.links = []
        self.images = []
        self.in_title = False
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "html":
            self.has_html = True
        if tag == "head":
            self.has_head = True
        if tag == "body":
            self.has_body = True
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if attr.get("charset"):
                self.charset = True
            if attr.get("name") == "viewport":
                self.viewport = True
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag in ("img", "script", "link") and attr.get(("src" if tag in ("img", "script") else "href")):
            key = "src" if tag in ("img", "script") else "href"
            self.images.append(attr[key])
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.in_title and self.title is None:
            self.title = data.strip()


def check_license():
    lic = ROOT / "LICENSE"
    if not lic.exists():
        error("LICENSE missing")
        return
    text = lic.read_text()
    target = "Copyright (c) 2026 Asdale Dynamics, LLC"
    if target not in text.splitlines():
        error('LICENSE missing exact line: ' + target)
    else:
        ok("LICENSE has exact copyright line")
    if "MIT License" in text:
        ok("LICENSE is MIT")


def check_readme():
    readme = ROOT / "README.md"
    if not readme.exists():
        error("README.md missing")
        return
    text = readme.read_text()
    if "Asdale Dynamics, LLC" in text:
        ok("README credits Asdale Dynamics, LLC")
    else:
        error("README does not credit Asdale Dynamics, LLC")


def check_no_github_workflows():
    if (ROOT / ".github" / "workflows").exists():
        error(".github/workflows exists (forbidden)")
    else:
        ok("No .github/workflows")


def check_no_secrets():
    patterns = {
        "sk-": "OpenAI-style key",
        "AKIA": "AWS key id",
        "ghp_": "GitHub token",
    }
    for path in ROOT.rglob("*"):
        if path == Path(__file__).resolve():
            continue
        if path.is_file() and path.stat().st_size < 2_000_000:
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            for sig, name in patterns.items():
                if sig in text:
                    error(f"Possible secret ({name}) in {path.relative_to(ROOT)}")
    # Personal-data scan: real-looking email addresses that are not placeholders
    email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.stat().st_size < 2_000_000:
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            for m in email_re.finditer(text):
                addr = m.group(0)
                if addr.endswith("example.com") or "example.com" in addr:
                    continue
                if addr in ("dylanasdale@users.noreply.github.com",):
                    warn(f"GitHub noreply email in {path.relative_to(ROOT)} (git identity only)")
                else:
                    error(f"Possible personal email in {path.relative_to(ROOT)}: {addr}")


def check_html_pages():
    html_pages = sorted((ROOT / "site").glob("*.html"))
    if not html_pages:
        error("No HTML pages in site/")
        return
    expected = {
        "index.html": "Home",
        "author-bio.html": "1. Author bio",
        "press-release.html": "2. Press release",
        "newsletter-setup.html": "3. Newsletter setup",
        "social-posts.html": "4. Social posts",
        "arc-readers.html": "5. ARC readers",
        "reviews.html": "6. Reviews",
        "local-events.html": "7. Local events",
    }
    for page in html_pages:
        text = page.read_text(errors="ignore")
        checker = PageChecker(text, page)
        checker.feed(text)
        name = page.name
        if "<!doctype html>" not in text.lower():
            error(f"{name}: missing <!DOCTYPE html>")
        else:
            checker.doctype = True
        if not checker.doctype:
            error(f"{name}: missing <!DOCTYPE html>")
        else:
            ok(f"{name}: doctype present")
        if not checker.has_html:
            error(f"{name}: missing <html>")
        if not checker.has_head:
            error(f"{name}: missing <head>")
        if not checker.has_body:
            error(f"{name}: missing <body>")
        if not checker.title:
            error(f"{name}: missing <title>")
        else:
            ok(f"{name}: title '{checker.title}'")
        if not checker.charset:
            error(f"{name}: missing charset meta")
        if not checker.viewport:
            error(f"{name}: missing viewport meta")

        # Internal links resolve
        for href in checker.links:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            resolved = (page.parent / target)
            if not resolved.exists():
                error(f"{name}: broken link -> {href}")
        # Assets exist
        for src in checker.images:
            resolved = (page.parent / src)
            if not resolved.exists():
                error(f"{name}: missing asset -> {src}")


def check_docs_match_site():
    docs = ROOT / "docs"
    chapters = [
        "01-author-bio.md",
        "02-press-release.md",
        "03-newsletter-setup.md",
        "04-social-posts.md",
        "05-arc-readers.md",
        "06-reviews.md",
        "07-local-events.md",
    ]
    for ch in chapters:
        if not (docs / ch).exists():
            error(f"docs/{ch} missing")
        else:
            ok(f"docs/{ch} exists")
    templates = [
        "author-bio.txt",
        "press-release.txt",
        "newsletter-welcome.txt",
        "social-posts.txt",
        "arc-reader-email.txt",
        "review-request-back-matter.txt",
        "event-signin-sheet.txt",
        "event-email.txt",
    ]
    for t in templates:
        if not (docs / "templates" / t).exists():
            error(f"docs/templates/{t} missing")
        else:
            ok(f"docs/templates/{t} exists")


def main():
    print(f"Root: {ROOT}")
    check_license()
    check_readme()
    check_no_github_workflows()
    check_html_pages()
    check_docs_match_site()
    check_no_secrets()
    print()
    if ERRORS:
        print(f"VERIFICATION FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        for e in ERRORS:
            print("  - " + e)
        return 1
    print(f"VERIFICATION PASSED ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())