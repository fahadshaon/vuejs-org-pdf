import logging
import os
import re

import pdfkit
from bs4 import BeautifulSoup

import core

header_regex = re.compile('^-+$')


def read_header(m):
    header = {}
    start = False

    with open(os.path.join(core.md_path, m)) as f:

        for l in f:
            l = l.strip()

            if header_regex.match(l) and not start:
                start = True
                continue

            if header_regex.match(l) and start:
                start = False
                continue

            if start:
                parts = l.split(':', 2)
                header[parts[0].strip()] = parts[1].strip()

    header['order'] = int(header['order'])
    header['md_file'] = m
    header['html_file'] = m.replace('.md', '.html')

    return header


def get_content_html(h):
    p = os.path.join(core.html_path, h['html_file'])
    with open(p) as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    node = soup.select_one(".content")

    remove_by_id(node, 'div', 'ad')
    remove_by_id(node, 'div', 'video-modal')

    remove_by_selector(node, '.footer')
    remove_by_selector(node, '.guide-links')

    for img in node.find_all('img'):
        src = img['src']
        if src.startswith('/images'):
            img['src'] = src[1:]

    return node.prettify()


def remove_by_selector(node, selector):
    for n in node.select(selector):
        n.decompose()


def remove_by_id(node, tag, id):
    n = node.find(tag, id=id)
    if n:
        n.decompose()


@core.cli.command(
    name='build',
    help='Generate guide pdf'
)
def build():
    headers = [read_header(l) for l in os.listdir(core.md_path)]
    headers.sort(key=lambda h: h['order'])

    output_html_file = os.path.join(core.dist_path, 'vuejs_org_guide_single_page.html')

    html_header = """
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="css/page.css"> 
    <link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600|Roboto Mono' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Dosis:500&text=Vue.js' rel='stylesheet' type='text/css'>

    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <style>
    .content {
        max-width: 950px !important
    }
    </style>
    <script src="js/vue.js"></script>
    <script>
      Vue.config.productionTip = false
      window.PAGE_TYPE = "guide"
    </script>
</head>
<body>"""

    logging.info("Building combined file")

    with open(output_html_file, 'wb') as f:
        f.write(html_header)

        for h in headers:
            logging.info("Adding: {}".format(h['html_file']))

            content = get_content_html(h)
            f.write(content.encode('utf-8'))
            f.write('<div style="page-break-after: always;"></div>')

        f.write('</body></html>')

    logging.info("Generating pdf")

    output_pdf_file = os.path.join(core.dist_path, 'vuejs_org_guide_single_page.pdf')
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'footer-font-size': '8',
        'footer-right': '[page]',
    }

    pdfkit.from_file(output_html_file, output_pdf_file, options=options)
