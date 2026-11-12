# -*- coding: utf-8 -*-
"""Colour illustrations (Microsoft Fluent Emoji, 'Color' style, MIT licence) used as pictures in HTML and inside SVG figures.
Accepts the old line-icon names too (COMPAT) so existing figures switch to pictures automatically."""
import os, base64
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'pics')
COMPAT = {'waves': 'wave', 'droplets': 'droplet', 'trees': 'tree', 'tree-deciduous': 'tree', 'tree-palm': 'palm', 'building-2': 'office', 'bug': 'bee',
          'bone': 'lion', 'map-pin': 'compass', 'sprout': 'seedling', 'flower': 'tulip', 'flower-2': 'bee', 'paw-print': 'fox', 'flame': 'fire',
          'layers': 'brick', 'triangle-alert': 'desert', 'trash-2': 'bin', 'worm': 'caterpillar', 'shirt': 'tshirt', 'footprints': 'camel',
          'shovel': 'potted', 'house': 'housegarden', 'volume-2': 'speaker', 'earth': 'globe'}
_cache = {}

def slug(name): return COMPAT.get(name, name)

def _b64(name):
    s = slug(name)
    if s not in _cache:
        _cache[s] = base64.b64encode(open(os.path.join(_D, s + '.svg'), 'rb').read()).decode()
    return _cache[s]

def html(name, cls='pic', sw=None):
    """<img> for HTML (relative path; the PDF is rendered from file://)."""
    return f'<img class="{cls}" src="assets/pics/{slug(name)}.svg" alt="">'

def nested(name, cx, cy, size, color=None, sw=None):
    """Picture centred at (cx, cy) inside an <svg> figure."""
    return (f'<image x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size}" height="{size}" '
            f'href="data:image/svg+xml;base64,{_b64(name)}"/>')
