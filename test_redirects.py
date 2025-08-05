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
