"""Check generated documents, translated structure, assets and internal links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import xml.etree.ElementTree as ET
from build import BASE, LANGS, OUT, PAGES

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.langs = set(), [], []
        self.h1 = self.scripts = self.title = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'html': self.langs.append(attrs.get('lang'))
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.title += 1
        if tag == 'script': self.scripts += 1
        for key in ['href', 'src']:
            if key in attrs: self.links.append(attrs[key])

def main():
    source = [json.loads((Path('content') / f'{lang}.json').read_text()) for lang, _ in LANGS]
    for data in source:
        assert set(data['pages']) == set(PAGES)
        for page in PAGES:
            sections = data['pages'][page]['sections']
            reference = source[0]['pages'][page]['sections']
            assert len(sections) == len(reference), f'Section coverage: {page}'
            for section, ref in zip(sections, reference):
                assert len(section.get('items', [])) == len(ref.get('items', [])), f'List coverage: {page}'
                assert len(section.get('paragraphs', [])) == len(ref.get('paragraphs', [])), f'Paragraph coverage: {page}'
    documents = {}
    for file in OUT.rglob('*.html'):
        parser = Document()
        parser.feed(file.read_text())
        assert parser.h1 == 1 and parser.title == 1, f'Heading or title missing: {file}'
        assert parser.scripts == 0, f'Unexpected script: {file}'
        assert len(parser.langs) == 1 and parser.langs[0] in dict(LANGS), f'Language missing: {file}'
        documents[file.resolve()] = parser
    assert len(documents) == 31, 'Expected 30 document pages and a 404 page'
    count = 0
    prefix = urlsplit(BASE)
    for file, parser in documents.items():
        for link in parser.links:
            part = urlsplit(link)
            if part.scheme == 'mailto':
                assert part.path == 'sunagaku.dx@gmail.com'
                continue
            if part.netloc and part.netloc != prefix.netloc: continue
            if part.netloc:
                assert part.path.startswith(prefix.path + '/'), f'Unexpected project link: {link}'
                target = OUT / unquote(part.path[len(prefix.path) + 1:])
            elif not part.path: target = file
            else: target = file.parent / unquote(part.path)
            if target.is_dir(): target = target / 'index.html'
            assert target.exists(), f'Broken link in {file}: {link}'
            if part.fragment:
                assert part.fragment in documents[target.resolve()].ids, f'Broken anchor: {link}'
            count += 1
    ET.parse(OUT / 'sitemap.xml')
    published = list(OUT.rglob('*'))
    assert not any(p.suffix in ['.swift', '.ts', '.env', '.ipa', '.mobileprovision'] for p in published)
    assert not any(p.name in ['content', '.git', '.github'] for p in published)
    for lang, _ in LANGS:
        for page in ['', *PAGES]:
            assert (OUT / lang / page / 'index.html').exists()
    print(f'PASS: 5 complete locales, {len(documents)} HTML pages, {count} local links/assets/anchors, sitemap and publish boundary.')

if __name__ == '__main__':
    main()
