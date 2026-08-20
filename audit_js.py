from pathlib import Path
from html.parser import HTMLParser

class ScriptParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.parts = []
        self.current = []
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'script':
            return
        attrs = dict(attrs)
        if attrs.get('src'):
            self.srcs.append(attrs['src'])
        else:
            self.in_script = True
            self.current = []

    def handle_data(self, data):
        if self.in_script:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == 'script' and self.in_script:
            self.parts.append(''.join(self.current))
            self.in_script = False

html_path = Path('/home/ubuntu/upload/index.html')
parser = ScriptParser()
parser.feed(html_path.read_text(encoding='utf-8'))
js_path = Path('/home/ubuntu/inline-app.js')
js_path.write_text('\n\n'.join(parser.parts), encoding='utf-8')
print(f'inline_scripts={len(parser.parts)}')
print('external_scripts=' + ','.join(parser.srcs))
print(f'inline_bytes={js_path.stat().st_size}')
