import re


def test_gemini_redirect_url():
    with open('go/gemini.html', 'r', encoding='utf-8') as f:
        content = f.read()
    expected = 'https://gemini.sjv.io/'
    assert expected in content, 'Gemini affiliate link missing'


def test_coinbase_redirect_url():
    with open('go/coinbase', 'r', encoding='utf-8') as f:
        content = f.read()
    expected = 'https://www.coinbase.com/join/YOURCODE'
    assert expected in content, 'Coinbase affiliate link missing'

