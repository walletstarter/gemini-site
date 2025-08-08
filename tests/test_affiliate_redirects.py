import re


def test_gemini_redirect_url():
    with open('go/gemini.html', 'r', encoding='utf-8') as f:
        content = f.read()
    expected = 'https://gemini.sjv.io/'
    assert expected in content, 'Gemini affiliate link missing'



def test_ledger_redirect_url():
    with open('go/ledger.html', 'r', encoding='utf-8') as f:
        content = f.read()
    expected = 'https://shop.ledger.com/'
    assert expected in content, 'Ledger affiliate link missing'


def test_nordvpn_redirect_url():
    with open('go/nord.html', 'r', encoding='utf-8') as f:
        content = f.read()
    expected = 'https://affiliates.nordvpn.com/'
    assert expected in content, 'NordVPN affiliate link missing'
