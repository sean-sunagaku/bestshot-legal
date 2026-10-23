"""Build a dependency-free, fully static multilingual GitHub Pages site."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
BASE = 'https://sean-sunagaku.github.io/bestshot-legal'
DATE = '2026-10-23'
LANGS = [('ja', '日本語'), ('en', 'English'), ('zh-Hans', '简体中文'), ('zh-Hant', '繁體中文'), ('ko', '한국어')]
PAGES = ['privacy', 'terms', 'support', 'delete-data']

def rich(text):
    parts = re.split(r'(\[[^\]]+\]\(https://[^)]+\))', text)
    result = []
    for part in parts:
        match = re.fullmatch(r'\[([^\]]+)\]\((https://[^)]+)\)', part)
        result.append(f'<a href="{escape(match[2], quote=True)}">{escape(match[1])}</a>' if match else escape(part))
    return ''.join(result)

def url(lang, page=''):
    return f'{BASE}/{lang}/' + (f'{page}/' if page else '')

def render(lang, data, page=''):
    doc = data['pages'][page] if page else data['home']
    languages = ''.join(f'<a lang="{code}" hreflang="{code}" href="{url(code, page)}"' + (' aria-current="true"' if code == lang else '') + f'>{name}</a>' for code, name in LANGS)
    nav = ''.join(f'<a href="{url(lang, name)}"' + (' aria-current="page"' if name == page else '') + f'>{escape(data["pages"][name]["title"])}</a>' for name in PAGES)
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{url(code, page)}">' for code, _ in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{BASE}/' + (f'{page}/' if page else '') + '">'
    sections = ''
    for index, section in enumerate(doc.get('sections', [])):
        sections += f'<section id="section-{index + 1}"><h2>{escape(section["title"])}</h2>'
        for paragraph in section.get('paragraphs', []):
            sections += f'<p>{rich(paragraph)}</p>'
        if section.get('items'):
            sections += '<ul>' + ''.join(f'<li>{rich(item)}</li>' for item in section['items']) + '</ul>'
        if section.get('contact'):
            subject = 'BestShot%20data%20request' if page == 'delete-data' else 'BestShot%20support'
            sections += f'<p class="contact"><a href="mailto:sunagaku.dx@gmail.com?subject={subject}">sunagaku.dx@gmail.com</a></p>'
        sections += '</section>'
    if page:
        toc = '<aside class="toc"><p>' + escape(data['contents']) + '</p><ol>' + ''.join(f'<li><a href="#section-{i+1}">{escape(s["title"])}</a></li>' for i, s in enumerate(doc['sections'])) + '</ol></aside>'
        body = f'<div class="document-layout">{toc}<article>{sections}</article></div>'
    else:
        cards = ''.join(f'<a class="document-link" href="{url(lang, name)}"><span><strong>{escape(data["pages"][name]["title"])}</strong><span>{escape(data["pages"][name]["summary"])}</span></span><span aria-hidden="true">↗</span></a>' for name in PAGES)
        body = f'<div class="home-layout"><div class="document-links">{cards}</div><article>{sections}</article></div>'
    updated = f'<p class="updated">{escape(data["updated"])} <time datetime="{DATE}">{DATE}</time></p>' if page in ['privacy', 'terms'] else ''
    description = doc['intro']
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(doc['title'])} | BestShot</title>
<meta name="description" content="{escape(description, quote=True)}">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#ffcc00">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'">
<link rel="canonical" href="{url(lang, page)}">{alternates}
<link rel="icon" type="image/png" href="{BASE}/assets/icon.png"><link rel="stylesheet" href="{BASE}/assets/style.css">
<meta property="og:title" content="{escape(doc['title'], quote=True)} | BestShot"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{url(lang, page)}">
</head>
<body>
<a class="skip" href="#main">{escape(data['skip'])}</a>
<header><div class="header-inner"><a class="brand" href="{url(lang)}"><img src="{BASE}/assets/icon.png" width="42" height="42" alt=""><span>BestShot</span></a><span class="site-label">{escape(data['siteLabel'])}</span></div></header>
<div class="shell"><nav class="languages" aria-label="{escape(data['language'], quote=True)}">{languages}</nav>
<main id="main"><div class="page-heading"><h1>{escape(doc['title'])}</h1><p class="intro">{escape(doc['intro'])}</p>{updated}</div>
<nav class="documents" aria-label="{escape(data['documents'], quote=True)}">{nav}</nav>{body}</main>
<footer><p>{escape(data['operator'])} <a href="mailto:sunagaku.dx@gmail.com">sunagaku.dx@gmail.com</a></p><p>{escape(data['languageNote'])}</p><p>© 2026 sunagaku</p></footer></div>
</body></html>'''

def main():
    for lang, _ in LANGS:
        data = json.loads((ROOT / 'content' / f'{lang}.json').read_text())
        assert set(data['pages']) == set(PAGES), f'Missing pages for {lang}'
        for page in ['', *PAGES]:
            dest = OUT / lang / page
            dest.mkdir(parents=True, exist_ok=True)
            (dest / 'index.html').write_text(render(lang, data, page))
        if lang == 'ja':
            # Stable, script-free default URLs for App Store metadata.
            for page in ['', *PAGES]:
                dest = OUT / page
                dest.mkdir(parents=True, exist_ok=True)
                (dest / 'index.html').write_text(render(lang, data, page))
    (OUT / '.nojekyll').touch()
    sitemap = [f'{BASE}/', *[f'{BASE}/{p}/' for p in PAGES]]
    sitemap += [url(lang, page) for lang, _ in LANGS for page in ['', *PAGES]]
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>' for u in sitemap) + '</urlset>')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    (OUT / '404.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | BestShot</title><link rel="stylesheet" href="{BASE}/assets/style.css"><main class="shell"><h1>Page not found</h1><p><a href="{BASE}/">BestShot · 日本語 / English / 中文 / 한국어</a></p></main></html>')
    print('Built 30 document pages, sitemap, and 404 page.')

if __name__ == '__main__':
    main()
