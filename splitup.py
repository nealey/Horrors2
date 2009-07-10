#! /usr/bin/env python3

import optparse
import re

badchars = re.compile(r'[^A-Za-z0-9]')

p = optparse.OptionParser()
opts, args = p.parse_args()

chapter = None
for fn in args:
    for line in open(fn):
        if line.startswith('%%%%%%%%%'):
            continue
        if line.startswith('\\chapter'):
            chapter = line[9:-2]
            chapter_line = line
            continue
        if line.startswith('\\by{'):
            by = line[4:-2]
            by = badchars.sub('_', by)

            chapter_ = badchars.sub('_', chapter)
            chapter_ = chapter_[:10]

            ofn = 'stories/%s.%s' % (by, chapter_)
            print('\\include{%s}' % ofn)
            of = open(ofn + '.tex', 'w')
            of.write(chapter_line)
        of.write(line)
