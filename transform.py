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
    styles = """.pico8_container {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -webkit-flex-direction: column;
      -ms-flex-direction: column;
          flex-direction: column;
  -webkit-box-align: center;
  -webkit-align-items: center;
      -ms-flex-align: center;
          align-items: center;
}

canvas#canvas {
  margin-top: 10px;
  width: 290px;
  height: 270px;
}

@media screen and (min-width: 580px) and (min-height: 600px) {
  canvas#canvas {
    margin-top: 20px;
    width: 580px;
    height: 540px;
  }
}

@media screen and (min-width: 1160px) and (min-height: 1150px) {
  canvas#canvas {
    margin-top: 30px;
    width: 1160px;
    height: 1080px;
  }
}

.pico8_options {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -webkit-justify-content: center;
      -ms-flex-pack: center;
          justify-content: center;
  -webkit-flex-wrap:wrap;
      -ms-flex-wrap:wrap;
          flex-wrap:wrap
}

.pico8_el {
  float: initial;
  display: initial;
}
"""
    style_tag = '<style class="responsive_override">\n' + styles + '</style>\n'
    return include_in_head(style_tag, html)

def javascript_restructure (html):
    script = """// purge all br elements
var brs = document.querySelectorAll('br');
Array.prototype.forEach.call(brs, function (br) {
  br.parentNode.removeChild(br);
});

// get rid of center elements (assume multiple elements to be safe)
var centerElems = document.querySelectorAll('center');
Array.prototype.forEach.call(centerElems, function (elem) {
  var parent = elem.parentNode;
  var children = elem.childNodes;
  for (var i = children.length - 1; i >= 0; i--) {
    parent.insertBefore(children[i], elem);
  }
  parent.removeChild(elem);
});

// add pico8_container class to container element
var container = document.getElementById('canvas').parentNode;
var containerClassName = 'pico8_container';
if (container.classList) {
  container.classList.add(containerClassName);
} else {
  container.className = container.className + ' ' + containerClassName;
}

// remove element-specific width from container element
container.style.width = '';

// move pico 8 options to new options container element
var options = document.getElementsByClassName('pico8_el');
if (options.length) {
  var optionsContainer = document.createElement('div');
  optionsContainer.className = 'pico8_options';
  container.insertBefore(optionsContainer, options[0]);
  Array.prototype.forEach.call(options, function (option) {
    optionsContainer.appendChild(option);
  });
}
"""
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
