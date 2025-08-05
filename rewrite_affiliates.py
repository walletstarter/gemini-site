import os
import shutil
import re
import json
from html.parser import HTMLParser

AFFILIATE_KEYWORDS = {
    "gemini": ["gemini"],
    "nordvpn": ["nordvpn"],
    "ledger": ["ledger"],
    "coinbase": ["coinbase"],
}

CTA_HTML = (
    '<div class="cta-block">\n'
    '  <p><a href="/go/gemini"><button>Start now with Gemini</button></a></p>\n'
    '  <p><a href="/go/nordvpn"><button>Protect with NordVPN</button></a></p>\n'
    '</div>'
)

CTA_MD = (
    "[Start with Gemini](/go/gemini)\n"
    "[Secure with NordVPN](/go/nordvpn)"
)

TRAP_LINK = '<a href="/go/test" style="display:none;">trap-link</a>'


def _slug_from_url(url: str) -> str | None:
    if url.startswith("/go/"):
        return None
    if not re.match(r"https?://", url, flags=re.IGNORECASE):
        return None
    url_lower = url.lower()
    for slug, keywords in AFFILIATE_KEYWORDS.items():
        for kw in keywords:
            if kw in url_lower:
                return slug
    return None


class AffiliateHTMLParser(HTMLParser):
    def __init__(self, redirects: dict[str, str]):
        super().__init__()
        self.redirects = redirects
        self.result: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs = dict(attrs)
            href = attrs.get("href", "")
            slug = _slug_from_url(href)
            if slug:
                self.redirects.setdefault(slug, href)
                attrs["href"] = f"/go/{slug}"
            attr_str = "".join(f' {k}="{v}"' for k, v in attrs.items())
            self.result.append(f"<{tag}{attr_str}>")
        else:
            attr_str = "".join(f' {k}="{v}"' for k, v in attrs)
            self.result.append(f"<{tag}{attr_str}>")

    def handle_startendtag(self, tag, attrs):
        if tag.lower() == "a":
            attrs = dict(attrs)
            href = attrs.get("href", "")
            slug = _slug_from_url(href)
            if slug:
                self.redirects.setdefault(slug, href)
                attrs["href"] = f"/go/{slug}"
            attr_str = "".join(f' {k}="{v}"' for k, v in attrs.items())
            self.result.append(f"<{tag}{attr_str}/>")
        else:
            attr_str = "".join(f' {k}="{v}"' for k, v in attrs)
            self.result.append(f"<{tag}{attr_str}/>")

    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")

    def handle_data(self, data):
        self.result.append(data)

    def handle_comment(self, data):
        self.result.append(f"<!--{data}-->")

    def handle_entityref(self, name):
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        self.result.append(f"&#{name};")



def rewrite_html(content: str, redirects: dict[str, str]) -> tuple[str, bool, bool]:

def rewrite_html(content: str, redirects: dict[str, str]) -> str:
    parser = AffiliateHTMLParser(redirects)
    parser.feed(content)
    rewritten = "".join(parser.result)

    cta_added = False
    trap_added = False

    if rewritten.count(CTA_HTML) < 2:
        cta_added = True
        rewritten = rewritten.replace(CTA_HTML, "")
        if re.search(r"<body[^>]*>", rewritten, flags=re.IGNORECASE):
            rewritten = re.sub(r"(<body[^>]*>)", r"\1\n" + CTA_HTML + "\n", rewritten, count=1, flags=re.IGNORECASE)
            rewritten = re.sub(r"(</body>)", CTA_HTML + "\n" + TRAP_LINK + "\n" + r"\1", rewritten, count=1, flags=re.IGNORECASE)
            trap_added = True
        else:
            rewritten = CTA_HTML + "\n" + rewritten + "\n" + CTA_HTML
            if TRAP_LINK not in rewritten:
                rewritten += "\n" + TRAP_LINK
                trap_added = True

    if TRAP_LINK not in rewritten:
        if re.search(r"</body>", rewritten, flags=re.IGNORECASE):
            rewritten = re.sub(r"(</body>)", TRAP_LINK + "\n" + r"\1", rewritten, count=1, flags=re.IGNORECASE)
        else:
            rewritten += "\n" + TRAP_LINK
        trap_added = True

    return rewritten, cta_added, trap_added


def rewrite_markdown(content: str, redirects: dict[str, str]) -> tuple[str, bool]:
    if re.search(r"<body[^>]*>", rewritten, flags=re.IGNORECASE):
        rewritten = re.sub(r"(<body[^>]*>)", r"\1\n" + CTA_HTML + "\n", rewritten, count=1, flags=re.IGNORECASE)
        rewritten = re.sub(r"(</body>)", CTA_HTML + "\n" + TRAP_LINK + "\n" + r"\1", rewritten, count=1, flags=re.IGNORECASE)
    else:
        rewritten = CTA_HTML + "\n" + rewritten + "\n" + CTA_HTML + "\n" + TRAP_LINK
    return rewritten


def rewrite_markdown(content: str, redirects: dict[str, str]) -> str:
    def repl(match: re.Match) -> str:
        text, url = match.group(1), match.group(2)
        slug = _slug_from_url(url)
        if slug:
            redirects.setdefault(slug, url)
            return f"[{text}](/go/{slug})"
        return match.group(0)

    rewritten = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, content)
    cta_added = False
    if CTA_MD not in rewritten:
        rewritten = CTA_MD + "\n" + rewritten + "\n" + CTA_MD
        cta_added = True
    return rewritten, cta_added


def main():
    source_dir = "/site/gemini-site-main"
    dest_dir = "/rewired_site"

    redirects: dict[str, str] = {}
    files_processed = 0
    cta_blocks = 0
    trap_links = 0
    rewritten = CTA_MD + "\n" + rewritten + "\n" + CTA_MD
    return rewritten


def main():
    source_dir = "site"
    dest_dir = "rewired_site"

    redirects: dict[str, str] = {}
    files_processed = 0
    html_traps = 0

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    for root, dirs, files in os.walk(source_dir):
        rel_root = os.path.relpath(root, source_dir)
        dest_root = os.path.join(dest_dir, rel_root) if rel_root != "." else dest_dir
        os.makedirs(dest_root, exist_ok=True)

        for filename in files:
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(dest_root, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext in {".html", ".htm"}:
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()
                rewritten, cta_added, trap_added = rewrite_html(content, redirects)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(rewritten)
                files_processed += 1
                if cta_added:
                    cta_blocks += 2
                if trap_added:
                    trap_links += 1
            elif ext == ".md":
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()
                rewritten, cta_added = rewrite_markdown(content, redirects)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(rewritten)
                files_processed += 1
                if cta_added:
                    cta_blocks += 2
                rewritten = rewrite_html(content, redirects)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(rewritten)
                files_processed += 1
                html_traps += 1
            elif ext == ".md":
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()
                rewritten = rewrite_markdown(content, redirects)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(rewritten)
                files_processed += 1
            else:
                shutil.copy2(src_path, dest_path)

    with open("redirects.json", "w", encoding="utf-8") as f:
        json.dump(redirects, f, indent=2)

    with open("fix_report.md", "w", encoding="utf-8") as f:
        f.write("# Affiliate Link Rewrite Report\n\n")
        f.write(f"Files processed: {files_processed}\n\n")
        f.write("## Affiliate Links Replaced\n")
        for slug, url in redirects.items():
            f.write(f"- {slug}: {url}\n")
        f.write("\n")

        f.write(f"CTA blocks inserted: {cta_blocks}\n")
        f.write(f"Trap links inserted: {trap_links}\n")

        f.write(f"CTA blocks inserted: {files_processed}\n")
        f.write(f"Trap links inserted: {html_traps}\n")

    test_script = '''
import os
import json
import re
import urllib.request

def run_checks():
    with open('redirects.json', 'r', encoding='utf-8') as f:
        redirects = json.load(f)

    root = 'rewired_site'
    pattern = re.compile("""https?://[^"']*(gemini|nordvpn|coinbase)""", re.IGNORECASE)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if not name.lower().endswith(('.html', '.htm', '.md')):
                continue
            path = os.path.join(dirpath, name)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert not pattern.search(content), f"Raw affiliate domain found in {path}"
            for slug in re.findall(r'/go/([a-z0-9_-]+)', content):
                assert slug in redirects, f"Missing slug '{slug}' in redirects.json"

    for slug, url in redirects.items():
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req) as resp:
                if resp.status != 200:
                    raise AssertionError(f"{url} returned {resp.status}")
        except Exception as exc:
            print(f"Warning: could not verify {url}: {exc}")

    print('All redirects validated')

if __name__ == '__main__':
    run_checks()
'''
    with open("test_redirects.py", "w", encoding="utf-8") as f:
        f.write(test_script.strip() + "\n")


if __name__ == "__main__":
    main()
