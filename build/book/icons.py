# -*- coding: utf-8 -*-
"""Lucide icons (ISC, github.com/lucide-icons/lucide) as inline SVG, for HTML and for nesting inside SVG figures."""
import os, re
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'lucide')
_cache = {}

def _inner(name):
    if name not in _cache:
        p = os.path.join(_D, name + '.svg')
        if not os.path.exists(p):
            raise FileNotFoundError(name)
        s = open(p, encoding='utf-8').read()
        m = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S)
        _cache[name] = re.sub(r'\s+', ' ', m.group(1)).strip()
    return _cache[name]

def html(name, cls='ic', sw=1.75):
    """Inline icon for HTML text (sized by CSS, follows currentColor)."""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{_inner(name)}</svg>')

def nested(name, cx, cy, size, color, sw=1.75):
    """Icon centred at (cx, cy) inside another <svg>."""
    return (f'<svg x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{_inner(name)}</svg>')
