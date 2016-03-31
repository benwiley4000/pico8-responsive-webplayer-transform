#!/usr/bin/python

# PICO-8 Responsive Web Player Transform


import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-l',
    '--lazy',
    action='store_true',
    help='If this flag is provided, we won\'t try using Python to ' +
        'restructure HTML document and will always insert JavaScript ' +
        'to be run on page load instead.',
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

def soup_restructure (html):
    soup = BeautifulSoup(html, 'lxml')

    # purge all br elements
    [br.extract() for br in soup('br')]

    # get rid of center elements and keep contents
    [center.unwrap() for center in soup('center')]

    # add pico8_container class to container element
    container = soup.find(id='canvas').parent
    container_class = 'pico8_container'
    existing_class = str(container.get('class') or '')
    container['class'] = (
        existing_class.replace(container_class, '') +
        ' ' + container_class
    ).strip()

    # remove element-specific width from container element
    container_style = cssutils.parseStyle(container.get('style'))
    if container_style:
        container_style.setProperty('width', None)
        new_style = container_style.cssText.replace('\n', '')
        if len(new_style):
            container['style'] = new_style
        else:
            del container['style']

    # move pico 8 options to new options container element
    options = soup(class_='pico8_el')
    if len(options):
        options_container = soup.new_tag('div')
        options_container['class'] = 'pico8_options'
        options[0].insert_before(options_container)
        for option in options:
            options_container.append(option)

    return soup.prettify()


restructure = javascript_restructure
if not args['lazy']:
    soup_available = True
    lxml_available = True
    cssutils_available = True
    try:
        from bs4 import BeautifulSoup
    except:
        soup_available = False
    try:
        import lxml
    except:
        lxml_available = False
    try:
        import cssutils
    except:
        cssutils_available = False

    if not (soup_available and lxml_available and cssutils_available):
        if not soup_available:
            print('[WARNING]: "beautifulsoup4" package unavailable.')
        if not lxml_available:
            print('[WARNING]: "lxml" package unavailable.')
        if not cssutils_available:
            print('[WARNING]: "cssutils" package unavailable.')
        print('Using JavaScript (to be run in browser) as restructuring fallback.')
    else:
        restructure = soup_restructure


filename = args['filename']
f = open(filename)

html = f.read().replace('</HEAD>', '</head>')

transformed_html = restructure(override_styles(html))

new_filename = filename.replace('.html', '-responsive.html')
t = open(new_filename, 'w')
t.write(transformed_html)

f.close()
t.close()
