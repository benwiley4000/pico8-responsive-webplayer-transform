# pico8 responsive webplayer transform

This is a python script you can run on an HTML file exported from the [PICO-8 Fantasy Console](http://www.lexaloffle.com/pico-8.php). It will create a new HTML file that is better suited for viewing at various window sizes, by injecting new CSS and JavaScript into your existing file.

Usage:

```
python transform.py cartridge.html
```

The command above will output a new file called `cartridge-responsive.html`. Use it with the same `cartridge.js` file generated by PICO-8.

## what it does

The JavaScript restructures some of the HTML elements. The CSS provides [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes) styling and tells the game canvas to take up to 2X the standard PICO-8 pixel dimensions (the canvas will be 290px, 580px, or 1160px wide dependending on available horizontal and vertical real estate).

It's best to stick to these three resolutions (multiples of the base resolution) in order for rendering to look nice.

## prerequisites

[Python](https://www.python.org/) (if you're on OSX or Linux, you likely already have Python installed.)

## build

To build `transform.py` from source, run:

```
# works in a UNIX shell environment
chmod +x build
./build
```

or:

```
python build.py
```