import requests

redirect_urls = [
  'https://walletstarter.com/go/gemini',
  'https://walletstarter.com/go/ledger.html',
]

def validate_redirects(urls):
    status = {}
    for url in urls:
        try:
            r = requests.head(url, allow_redirects=True, timeout=10)
            status[url] = {'status_code': r.status_code, 'final_url': r.url}
        except Exception as e:
            status[url] = {'error': str(e)}
    return status

if __name__ == '__main__':
    print(validate_redirects(redirect_urls))
