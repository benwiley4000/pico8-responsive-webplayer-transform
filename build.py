#!/usr/bin/python

p = open('src/transform.py')
c = open('src/override.css')
j = open('src/restructure.js')

overrideStyles = c.read()
restructureScript = j.read()

contents = p.read() \
    .replace('"""[CSS]"""', '"""' + overrideStyles + '"""') \
    .replace('"""[JS]"""', '"""' + restructureScript + '"""')

f = open('transform.py', 'w')
f.write(contents)

p.close()
c.close()
j.close()
f.close()
