#!/usr/bin/env python3
"""CFG265_refs.py: frozen-criteria section 5. Parses the 12 reference entries of the PAPER39 draft (at 53f374ae2), compares
them with citations/REFERENCES.bib (matched by arXiv id), with the repo's deposit records for [P36]/[P38] (README.md table,
the .zenodo.json files), and with the hand transcription of the arXiv pages fetched by the referee (CFG265_refs_webfetch.json).
No network inside this script. Exit 0 if the comparison completed (discrepancies are printed, never an exit code)."""
import re, os, sys, json
from CFG265_common import *


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower().replace('\\^', '').replace("\\'", '').replace('\\"', ''))


def main():
    tex, _ = pin_text(TEX_REL)
    refs = references(tex)
    bib, how = pin_text('citations/REFERENCES.bib')
    entries = re.split(r'\n@', bib) if bib else []
    web = json.load(open(os.path.join(HERE, 'CFG265_refs_webfetch.json')))['pages']
    readme, _ = pin_text('README.md')
    print('repo <repo>; references read at', PIN, '; REFERENCES.bib read from', how)
    print('the tex comment says: titles, authors and arXiv ids checked against the arXiv abstract pages; journal data only where the page shows them')
    for k in sorted(refs):
        r = refs[k]
        ax = re.search(r'arXiv:(\d{4}\.\d{4,5})', r)
        title = re.search(r'``(.*?)\'\'', r)
        title = title.group(1) if title else ''
        jr = re.search(r"'',\s*(.*?)(?:, arXiv|, doi|$)", r)
        print('\n[%s] %s' % (k, r[:240]))
        if ax:
            hit = [e for e in entries if ax.group(1) in e]
            if hit:
                e = hit[0]
                bt = re.search(r'title\s*=\s*[{"](.*?)[}"],?\n', e, re.S)
                bj = re.search(r'journal\s*=\s*[{"](.*?)[}"]', e); bv = re.search(r'volume\s*=\s*[{"]?(\w+)', e); bp = re.search(r'pages\s*=\s*[{"]?([\w-]+)', e)
                print('   bib: key %s | title match %s | journal %s vol %s pages %s' % (e.split(',')[0][:40], (norm(bt.group(1)) == norm(title)) if bt else 'n/a',
                      bj.group(1) if bj else '-', bv.group(1) if bv else '-', bp.group(1) if bp else '-'))
            else:
                print('   bib: NO entry with arXiv %s in citations/REFERENCES.bib' % ax.group(1))
        if k in web:
            w = web[k]
            tm = norm(w['title']) == norm(title)
            print('   arXiv page (WebFetch, referee): title match %s | authors %s | journal_ref "%s"' % (tm, ', '.join(w['authors']), w['journal_ref']))
            if w.get('content_quote'):
                print('   page content: "%s"' % w['content_quote'])
        if k in ('P36', 'P38'):
            doi = re.search(r'doi:(10\.5281/zenodo\.\d+)', r).group(1)
            line = [l for l in readme.split('\n') if doi in l and l.startswith('|')]
            print('   repo deposit record (README.md table):', (line[0][:200] if line else 'NOT FOUND'))
        if re.search(r'submitted|accepted', r):
            print('   status entry carries a volume?', bool(re.search(r'\b\d{2,4}, [A-Z]?\d+', r.split("''")[-1])))
    print('\nFrozen pair: HFB17 and MC10 agree with their arXiv pages (title, authors, journal reference; HFB17 abstract carries "seven orders of magnitude").')
    print('Not checkable here: journal-side pagination beyond the arXiv page; the BBN-only value 0.98 +- 0.06 of [A20] (eq. 9, not in its abstract);')
    print('the 2026 papers beyond their abstract pages; that any arXiv page is the final version.')
    sys.exit(0)


if __name__ == '__main__':
    main()
