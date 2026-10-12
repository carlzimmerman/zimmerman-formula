#!/usr/bin/env python3
"""Builds the public web copy of the chart (ai_slop/website/public/kepler-grade/index.html) from
explainers/kepler_grade_prediction_chart.html: adds a full HTML document wrapper and a Home link, and rewords the three
do-not-cite cards that refer to 'the public site' so they read as public disclosures. Run, then `npm run build` and
`firebase deploy --only hosting` in ai_slop/website."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "kepler_grade_prediction_chart.html")
OUT = os.path.join(HERE, "..", "ai_slop", "website", "public", "kepler-grade", "index.html")
src = open(SRC, encoding="utf-8").read()

def rep(a, b):
    global src
    assert a in src, a[:70]
    src = src.replace(a, b, 1)

rep(''' ["'Z² confirmed' claims on the public site","The route notice and several cards still say DESI 4PCF 'confirms' the T³/Z₂ topology (r = 0.9986) and list the Z² constants as live. The η-invariant is exactly 0, matched circles exclude the topology, and the record retracts the constants as numerology. See the K4 rows."],''',
    ''' ["Older pages on this site: 'Z² confirmed' claims","Some older pages and cards say DESI 4PCF 'confirms' the T³/Z₂ topology (r = 0.9986) and list the Z² constants as live. The η-invariant is exactly 0, matched circles exclude the topology, and the record retracts the constants as numerology. See the K4 rows."],''')
rep(''' ["Public site /predictions page","The quarantined ai_slop page still lists Z² = 32π/3 numerology as live cards (δ<sub>CP</sub> = 195°, Σm<sub>ν</sub> ≈ 59–60 meV, λ<sub>Higgs</sub> = 13/100, H₀ = 71.5). The site's own route notice contradicts it."],''',
    ''' ["Older /predictions page on this site","It still lists Z² = 32π/3 numerology as live cards (δ<sub>CP</sub> = 195°, Σm<sub>ν</sub> ≈ 59–60 meV, λ<sub>Higgs</sub> = 13/100, H₀ = 71.5). It predates the retractions; this chart replaces it as the current record."],''')
rep(''' ["Public site wording on a₀(z)","The layout says a₀ is flat below z ≈ 20 and any robust evolution at z ≲ 5 falsifies it. The 10-10 kill sheet (G5) is the dark-energy-tracking version (+6% near z 0.4, about 0.74 by z = 3, flat only if w = −1). Reconcile before sharing."],''',
    ''' ["Older site wording on a₀(z)","Some site text says a₀ is flat below z ≈ 20 and any robust evolution at z ≲ 5 falsifies it. The 2026-10-10 kill sheet (G5) is the dark-energy-tracking version (+6% near z 0.4, about 0.74 by z = 3, flat only if w = −1). Both readings are listed in the a₀(z) rows above."],''')
head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Every testable prediction on the record, dated, with the framework's number, the rivals' numbers, what would count against it, the confronted results and the withdrawn claims. kappa = 1/2 is fitted; this is not a closed theory.">
<style>html{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}@media (prefers-color-scheme: dark){html:not([data-theme="light"]){color-scheme:dark}}</style>
'''
i = src.index("</style>") + len("</style>")
body = head + src[:i] + "\n</head>\n<body>" + src[i:] + "\n</body>\n</html>\n"
a = '<div class="wrap">\n  <h1>Kepler Grade Prediction Chart</h1>'
assert a in body
body = body.replace(a, '<div class="wrap">\n  <p style="margin:0 0 10px;font-size:13px"><a href="/" style="color:var(--accent)">← Home</a></p>\n  <h1>Kepler Grade Prediction Chart</h1>', 1)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(body)
print("wrote", os.path.relpath(OUT, HERE), len(body) // 1024, "KB")
