import tempfile
import httpx
import tinycss2
from urllib.parse import urlparse
import os
import glob

proxy_domain[str] = 'www.example.com'

client = httpx.Client(
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0'},
    http2=True
    )

css_response = client.get(
    'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&display=swap'
    )
rules=tinycss2.parse_stylesheet(
    css_response.text,
    skip_whitespace=True,
    skip_comments=True
    )

# woff2形式のフォントURLリストを格納するリスト
woff2_list = []

for rule in rules:
    if rule.type == 'at-rule' and rule.at_keyword == 'font-face':
        declarations = tinycss2.parse_declaration_list(rule.content,skip_whitespace=True,skip_comments=True)
        for declaration in declarations:
            if declaration.name == 'src':
                print(declaration.value[1].value)
                woff2_list.append(declaration.value[1].value)

with tempfile.TemporaryDirectory() as tmpdirname:

    client = httpx.Client(
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0'},
        http2=True
        )

    for url in woff2_list:
        print(url)
        woff2_response = client.get(url)
        os.makedirs(f'{tmpdirname}{urlparse(url).path.rpartition('/')[0]}', exist_ok=True)
        with open(f'{tmpdirname}{urlparse(url).path}', 'wb') as f:
            f.write(woff2_response.content)
        print(glob.glob(f'{tmpdirname}/**', recursive=True))


