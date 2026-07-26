#!/usr/bin/env python3
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

for f in ['index.html','about.html','programs.html','contact.html']:
    html = open(f'01-alriyadh-academy/{f}', encoding='utf-8').read()
    has_dev = 'footer-dev' in html
    has_logo = 'arabix-logo.png' in html
    has_reveal = 'reveal' in html
    has_zoom = 'img-zoom' in html
    print(f'{f}: dev={has_dev} logo={has_logo} reveal={has_reveal} zoom={has_zoom}')

css = open('01-alriyadh-academy/style.css', encoding='utf-8').read()
has_anim = 'ANIMATIONS' in css
has_reveal_css = '.reveal' in css
has_bounce = 'scrollBounce' in css
has_dev_css = 'footer-dev' in css
print(f'CSS: anim={has_anim} reveal={has_reveal_css} bounce={has_bounce} footer-dev={has_dev_css}')

js = open('01-alriyadh-academy/script.js', encoding='utf-8').read()
has_reveal_js = 'revealObserver' in js
has_scroll = 'scrolled' in js
has_parallax = 'parallax' in js
print(f'JS: reveal={has_reveal_js} scroll={has_scroll} parallax={has_parallax}')
