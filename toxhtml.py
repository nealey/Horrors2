#! /usr/bin/env python3

import re

block1_re = re.compile(r'{\\(?P<cmd>[\w*]+) (?P<txt>[^{}]+)}')
block2_re = re.compile(r'\\(?P<cmd>[\w*]+)(\[[^]]+\])?{(?P<txt>[^{}]*)}')


chapauth = None
chapimg = None
display = True
pfx = ''

def texsub(m):
    global pfx, display

    cmd = m.group('cmd')
    txt = m.group('txt')
    if cmd == 'em':
        return '<em>%s</em>' % txt
    elif cmd == 'bf':
        return '<strong>%s</strong>' % txt
    elif cmd == 'sf':
        return '<samp>%s</samp>' % txt
    elif cmd == 'sc':
        return '<span class="sc">%s</span>' % txt
    elif cmd == 'rm':
        return '<span class="rm">%s</span>' % txt
    elif cmd == 'url':
        return '<a href="%s">%s</a>' % (txt, txt)
    elif cmd == 'begin':
        if txt in ('center',):
            return
        elif txt in ('quotation', 'quote'):
            pfx = '> '
        elif txt == 'textblock':
            display = False
        else:
            print(cmd, txt)
            raise TypeError(cmd)
    elif cmd == 'end':
        if txt == 'textblock':
            display = True
        else:
            pfx = ''
        return ''
    elif cmd in ('include',
                 'chapter',
                 'chapimg',
                 'chapauth',
                 'illustration',
                 'scriptsize',
                 'section*',
                 'part'):
        return '#%s %s' % (cmd, txt)
    elif cmd in ('pagenumbering',
                 'includegraphics',
                 'newcommand',
                 'hbox'):
        return ''
    elif cmd in ('TeX',
                 'LaTeX'):
        return cmd
    else:
        print(cmd, txt)
        raise TypeError(cmd)

decor_stack = []
decor_re = re.compile(r'({\\(?P<cmd>\w\w) ?|})')

def decorsub(m):
    cmd = m.group('cmd')
    if not cmd:
        if not decor_stack:
            return m.group(0)
        cmd = decor_stack.pop()
        return '</%s>' % cmd
    else:
        if cmd == 'bf':
            cmd = 'strong'
        elif cmd == 'em':
            pass
        elif cmd == 'sc':
            decor_stack.append('span')
            return '<span class="sc">'
        else:
            raise TypeError(cmd)
        decor_stack.append(cmd)
        return '<%s>' % cmd

def art(artist, url, title=None):
    alt = title or ("Artwork by %s" % artist)
    print('<div class="art">')
    print('<img src="%s" alt="%s" />' % (url, alt))
    if title:
        atxt = '<em>%s</em> by %s' % (title, artist)
    else:
        atxt = alt
    print('<p class="artist">%s</p>' % (atxt))
    print('</div>')

outbuf = ''

def outline(l):
    global chapimg, chapauth, outbuf

    l = l.strip()
    if not l:
        print(outbuf)
    elif l[0] == '%':
        return
    l = l.replace(r'\'e', 'é')
    l = l.replace(r'\,c', 'ç')
    l = l.replace(r'\'n', 'ń')
    l = l.replace("''", '&rdquo;')
    l = l.replace("``", '&ldquo;')
    l = l.replace("'", '&rsquo;')
    l = l.replace("`", '&lsquo;')
    l = l.replace('---', '&mdash;')
    l = l.replace('--', '&ndash;')
    l = l.replace('\\\\', '<br />')
    l = l.replace('\_', '_')
    l = l.replace('\#', '#')
    l = l.replace('\$', '$')
    l = l.replace('\ ', ' ')
    l = l.replace(r'\-', '')
    l = l.replace(r'\~n', 'ñ')
    l = l.replace(r'{\ldots}', '&hellip;')
    l = l.replace(r'\ldots', '&hellip;')
    l = l.replace(r'\copyright', '&copy;')
    l = block1_re.sub(texsub, l)
    l = block2_re.sub(texsub, l)
    l = l.replace('{}', '')
    l = decor_re.sub(decorsub, l)

    if not l:
        return
    if l[0] == '#':
        if l.startswith('#include'):
            include(l[9:] + '.tex')
        elif l.startswith('#chapimg'):
            chapimg = l[9:-1].split('{')
        elif l.startswith('#chapauth'):
            chapauth = l[10:]
        elif l.startswith('#chapter'):
            print('<h1 class="chapter">%s</h1>' % l[9:])
            if chapauth:
                print('<h2 class="author">by %s</h2>' % chapauth)
                chapauth = None
            if chapimg:
                art(chapimg[0], chapimg[1])
                chapimg = None
        elif l.startswith('#part'):
            print('<h1 class="part">%s</h1>' % l[6:])
        elif l.startswith('#illustration'):
            artist, title, url = l[14:].split('{')
            title = title[:-1]
            url = url[:-1]
            art(artist, url, title)
        elif l.startswith('#section*'):
            print('<h2 class="section">%s</h2>' % l[10:])
        else:
            print('<--! %s -->' % l)
    elif l[0] == '\\':
        what = l[1:5].lower()
        if what in ('bigs', 'vfil'):
            print('<br class="bigskip"/>')
        elif what == 'newp':
            print('<br class="pagebreak"/>')
        elif what == 'noin':
            print(l[10:])
        elif what in ('hbox',
                      'inde',
                      'tabl',
                      'appe',
                      'page',
                      'list'):
            pass
        elif l[1:9] == 'maketitl':
            print('<h1>Horrors 2</h1>')
            print('<h2>The Something Awful Forums</h2>')
        else:
            print('================= %r' % what)
    elif display:
        print('%s%s' % (pfx, l))

def include(fn):
    if fn == 'praise.tex':
        return
    f = open(fn)

    for l in f:
        outline(l)

f = open('horrors2.ltx')

# skip LaTeX crap
for l in f:
    if l.startswith('\\begin{document'):
        break

print('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC
  "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Horrors 2</title>
    <link rel="stylesheet" href="style.css" type="text/css" />
  </head>

  <body>
''')

for l in f:
    outline(l)

print('''</body>
</html>
''')
