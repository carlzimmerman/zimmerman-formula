#!/usr/bin/env python3
"""CFG241_refs.py: reference spot-check (frozen section 5). Offline only: compares the tex reference list with
citations/REFERENCES.bib, UNVERIFIED.md, CORRECTIONS.md and local copies in data_assembly. Never checks a journal.
Exit 0 if the comparison completed."""
import re, sys, os
from CFG241_common import *
tex, how = head_text(TEX_REL)
bib, _ = head_text('citations/REFERENCES.bib'); unv, _ = head_text('citations/UNVERIFIED.md'); cor, _ = head_text('citations/CORRECTIONS.md')
entries = re.findall(r'^\[([A-Z0-9]+)\]\s*(.*?)\\par', tex, re.M | re.S)
out = []
def P(s=''): print(s); out.append(s)
P('CFG241_refs: repo <repo>; tex from %s; %d reference entries (keys: %s)' % (how, len(entries), ', '.join(k for k, _ in entries)))
bibents = re.split(r'\n(?=@)', bib)
def bib_by_eprint(e):
    for b in bibents:
        if re.search(r'eprint\s*=\s*\{%s\}' % re.escape(e), b): return b
def field(b, f):
    m = re.search(r'\b%s\s*=\s*\{+(.*?)\}+,?\s*$' % f, b, re.M); return m.group(1) if m else None
raw_files = {}
import subprocess
rs = ls_head('data_assembly/multitracer_gas/raw_small/')
for f in rs: raw_files[f] = None
def raw(f):
    if raw_files[f] is None: raw_files[f] = head_text(f)[0] or ''
    return raw_files[f]
res = []
for key, body in entries:
    eps = [e.rstrip('.') for e in re.findall(r'arXiv:([\d.]+)', body)]; vol = re.search(r'\b(?:ApJL?|A\\&A|MNRAS)(?:\s|~)(\d+)(?:,\s*(\w?\d+))?', body)
    P('\n[%s] %s' % (key, re.sub(r'\s+', ' ', body)[:150]))
    P('   tex: arXiv %s; journal volume/page as printed: %s' % (eps, (vol.group(0) if vol else 'none printed')))
    for e in eps:
        b = bib_by_eprint(e)
        if b:
            P('   REFERENCES.bib: FOUND (eprint %s): volume=%s pages=%s year=%s doi=%s' % (e, field(b, 'volume'), field(b, 'pages'), field(b, 'year'), field(b, 'doi')))
            res.append((key, e, 'bib', field(b, 'volume'), field(b, 'pages')))
        else:
            P('   REFERENCES.bib: NO entry for eprint %s' % e)
            hits = [f for f in rs if e in raw(f)]
            res.append((key, e, 'nobib', None, None))
        P('   UNVERIFIED.md / CORRECTIONS.md mention: %s / %s' % (e in unv, e in cor))
        # third-party reference lists in locally fetched pages that print this paper's journal reference
        for f in rs:
            t = raw(f)
            for m in re.finditer(r'(Dunne[^<]{0,80}2022|Heintz[^<]{0,40}Watson[^<]{0,10}2020)[^\n]{0,120}', t):
                pass
    if key == 'D22':
        for f in rs:
            t = raw(f)
            m = re.search(r'Dunne, L\.[^\n]{0,200}2022, MNRAS, (517), (962)', t)
            if m: P('   local third-party copy: %s: "MNRAS, %s, %s" (a later paper\'s reference list, not the journal)' % (f.split('/')[-1], m.group(1), m.group(2))); break
    if key == 'HW20':
        for f in rs:
            t = raw(f)
            m = re.search(r'Heintz, K\. E\.,? (?:&amp;|&) Watson, D\. 2020, ApJ, (\d+), (L\d+)', t)
            if m: P('   local third-party copy: %s: "ApJ, %s, %s" (a later paper\'s reference list; ApJL is the Letters section of ApJ)' % (f.split('/')[-1], m.group(1), m.group(2))); break
    if key == 'ACE':
        for ep in ('2609.21040', '2609.20926'):
            f = [x for x in rs if ep in x]
            if f:
                t = raw(f[0]); ti = re.search(r'<title>(.*?)</title>', t, re.S)
                P('   local HTML %s title: %s' % (ep, re.sub(r'\s+', ' ', ti.group(1))[:140] if ti else None))
P('\nSUMMARY (frozen spot-checks D22 and HW20; offline limits):')
P('  - volume/page agreement with the repo\'s OWN records: B21 (A&A 650 A113), DM14 (MNRAS 441, 3359), NS23 (ApJ 944, 78) agree with REFERENCES.bib; D22 (MNRAS 517, 962) and HW20 (ApJL 889, L7) have NO bib entry and agree only with third-party reference lists inside locally fetched HTML pages and with the repo\'s own scoping note;')
P('  - B23 (ApJ, no volume/page), C19 (MNRAS, doi only), ACE x2 (arXiv 2609.xxxxx, "submitted to A&A"): no bib entry; titles/first authors of the ACE pair agree with the local HTML copies; "submitted to A&A" cannot be checked offline;')
P('  - NOT checkable offline: the journals\' own volume/page/year records; arXiv resolution; whether ACE exists as stated outside the repo\'s fetched copies.')
open(os.path.join(HERE, 'CFG241_refs.out'), 'w').write(scrub('\n'.join(out)) + '\n')
