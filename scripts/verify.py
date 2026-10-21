"""Check the generated static site using only Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = ('index.html', 'privacy.html', 'ar/index.html', 'ar/privacy.html')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.references = []
        self.alternates = {}
        self.language_links = []
        self.document = {}
        self.landmarks = []
        self.title_count = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'html':
            self.document = attrs
        if tag == 'title':
            self.title_count += 1
        if tag in ('main', 'header', 'footer', 'nav'):
            self.landmarks.append(tag)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID in {self.path}'
            self.ids.add(attrs['id'])
        for attribute in ('href', 'src'):
            if attribute in attrs:
                self.references.append(attrs[attribute])
        if 'srcset' in attrs:
            self.references.extend(candidate.strip().split()[0] for candidate in attrs['srcset'].split(','))
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs['hreflang']] = attrs['href']
        if tag == 'a' and 'language-switch' in attrs.get('class', '').split():
            self.language_links.append(attrs)


parsed = {}
for name in PAGES:
    path = ROOT / name
    content = path.read_text()
    assert '{{' not in content, f'Unresolved template in {name}'
    page = Page(path)
    page.feed(content)
    parsed[path] = page

for path, page in parsed.items():
    arabic = path.parent.name == 'ar'
    locale, direction = ('ar', 'rtl') if arabic else ('en', 'ltr')
    assert page.document.get('lang') == locale
    assert page.document.get('dir') == direction
    assert page.title_count == 1
    for landmark in ('main', 'header', 'footer', 'nav'):
        assert page.landmarks.count(landmark) == 1, (path, landmark)
    assert len(page.language_links) == 1
    alternate = page.language_links[0]
    assert alternate['hreflang'] == ('en' if arabic else 'ar')
    destination = (path.parent / alternate['href']).resolve()
    assert destination.name == path.name, 'Language switch must retain the page'
    assert parsed[destination].document['lang'] != locale
    assert set(page.alternates) == {'en', 'ar'}
    for language, href in page.alternates.items():
        assert parsed[(path.parent / href).resolve()].document['lang'] == language
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        destination = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert ROOT == destination or ROOT in destination.parents, f'Link escapes site: {reference}'
        assert destination.is_file(), f'Missing local resource: {reference} in {path}'
        if url.fragment:
            assert url.fragment in parsed[destination].ids, f'Missing fragment: {reference}'
    print(f'PASS {path.relative_to(ROOT)}: language, structure, links and fragments')
