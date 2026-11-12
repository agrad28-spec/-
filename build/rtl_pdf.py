#!/usr/bin/env python3
"""Mark PDFs as right-to-left books: two-page spreads read right->left, cover alone on the right."""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, TextStringObject

def fix(path):
    r = PdfReader(path)
    w = PdfWriter(clone_from=r)
    root = w._root_object
    root[NameObject('/ViewerPreferences')] = DictionaryObject({NameObject('/Direction'): NameObject('/R2L')})
    root[NameObject('/PageLayout')] = NameObject('/TwoPageRight')   # page 1 (cover) alone, then 2|3, 4|5 ...
    root[NameObject('/Lang')] = TextStringObject('ar')
    with open(path, 'wb') as f:
        w.write(f)
    r2 = PdfReader(path)
    rc = r2.trailer['/Root']
    print(path.split('/')[-1], len(r2.pages), rc['/ViewerPreferences'], rc['/PageLayout'])

for p in sys.argv[1:]:
    fix(p)
