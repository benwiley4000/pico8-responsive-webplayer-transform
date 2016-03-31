#!/usr/bin/python

# PICO-8 Responsive Web Player Transform


import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--now',
    action='store_true',
    help='If provided, tries to use PyQuery to ' +
        'restructure document now. If PyQuery is not ' +
        'available, falls back to JavaScript.',
    default=False
)
parser.add_argument(
    'filename',
    help='The name of the HTML file to be transformed.'
)
args = vars(parser.parse_args())


def include_in_head (tag, html):
    html_parts = html.split('</head>')
    return '</head>'.join([html_parts[0] + tag] + html_parts[1:])

def override_styles (html):
    styles = """[CSS]"""
    style_tag = '<style class="responsive_override">\n' + styles + '</style>\n'
    return include_in_head(style_tag, html)

def javascript_restructure (html):
    script = """[JS]"""
    onload_script = 'window.onload = function () {\n\n' + script + '\n};\n'
    script_tag = '<script async class="restructure_script">\n' + onload_script + '</script>\n'
    return include_in_head(script_tag, html)

def pyquery_restructure (html):
    pass


restructure = javascript_restructure
if args['now']:
    try:
        from pyquery import PyQuery as pq
        restructure = pyquery_restructure
    except NameError:
        print(
            'WARNING: "pyquery" module unavailable; ' +
            'using JavaScript (to be run in browser) as ' +
            'restructuring fallback.'
        )


filename = args['filename']
f = open(filename)

html = f.read().replace('</HEAD>', '</head>')

transformed_html = restructure(override_styles(html))

new_filename = filename.replace('.html', '-responsive.html')
t = open(new_filename, 'w')
t.write(transformed_html)

f.close()
t.close()
