#! /usr/bin/env python3

import optparse
import xml.etree.ElementTree
import re

quotes_re = re.compile(r'"([^"]+)"')
dots_re = re.compile(r'\.\.\.+')
crap_re = re.compile(r'<p class="editedby">.*</p>', re.DOTALL)
tag_re = re.compile(r'<[^>]+>')

def by_class(e, classname):
    todo = [e]
    while todo:
        i = todo.pop(0)
        if i.get('class') == classname:
            yield i
        todo = i.getchildren() + todo

def first_by_class(e, classname):
    for i in by_class(e, classname):
        return i

def table_to_ltx(t):
    dt = first_by_class(t, 'author')

    username = dt.text
    if not username:
        # Moderators
        username = dt.getchildren()[-1].tail
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('\\by{%s}' % username)

    body = first_by_class(t, 'postbody')

    s = xml.etree.ElementTree.tostring(body)
    s = s.replace('<br />', '\n')
    s = s.replace('<i>', '{\\em ')
    s = s.replace('</i>', '}')
    s = s.replace('<b>', '{\\bf ')
    s = s.replace('</b>', '}')
    s = crap_re.sub('', s)
    s = tag_re.sub('', s)
    s = dots_re.sub('{\ldots}', s)
    s = quotes_re.sub(r"``\1''", s)
    print(s)

def doc_to_ltx(doc):
    for e in doc.getiterator('table'):
        if e.get('class') == 'post':
            table_to_ltx(e)

def main():
    p = optparse.OptionParser()
    (opts, args) = p.parse_args()

    for a in args:
        f = open(a, encoding='iso-8859-1')
        parser = xml.etree.ElementTree.XMLTreeBuilder()
        parser.entity.update(nbsp=" ",
                             lsaquo="<", rsaquo=">",
                             lsquo="`",  rsquo="'",
                             ldquo="``", rdquo="''",
                             hellip="{\\ldots}",
                             ndash="---",
                             mdash="---",
                             iexcl="{\\!`}",
                             copy="{\\copyright}",
                             eacute="\\'e",
                             ccedil="\\,c",
                             )
        doc = xml.etree.ElementTree.parse(f, parser)
        doc_to_ltx(doc)

main()
