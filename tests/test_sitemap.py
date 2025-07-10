import os
import urllib.parse


def test_sitemap_paths_exist():
    with open('sitemap.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        path = urllib.parse.urlparse(url).path.lstrip('/')
        assert os.path.exists(path), f"Missing file for {url}"
