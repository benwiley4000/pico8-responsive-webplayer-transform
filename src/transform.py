#!/usr/bin/python

# PICO-8 Responsive Web Player Transform

import sys

f = open(sys.argv[1])

html = f.read().replace('</HEAD>', '</head>')
override_styles = """[CSS]"""
restructure_script = """[JS]"""

onload_script = 'window.onload = function () {\n' + restructure_script + '};\n'

style_tag = '<style class="responsive_override">\n' + override_styles + '</style>'
script_tag = '<script async class="restructure_script">\n' + onload_script + '</script>'

html_parts = html.split('</head>')

transformed_html = '\n'.join([html_parts[0], style_tag, script_tag, html_parts[1]])

new_filename = sys.argv[1].replace('.html', '-responsive.html')
t = open(new_filename, 'w')
t.write(transformed_html)

f.close()
t.close()
