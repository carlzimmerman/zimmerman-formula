#!/usr/bin/env python3
"""CFG241_extract.py: frozen section-3 claim enumeration of PAPER38 (read at git HEAD).
Writes CFG241_claims.csv + CFG241_sections.json; prints counts. Exit 0 if the legacy count (120 units / 117 claims)
is reproduced, 1 if not (the difference is printed and kept)."""
import csv, json, re, sys, hashlib, os
from CFG241_common import *

def main(tex_override=None, outdir=HERE, quiet=False):
    tex, how = head_text(TEX_REL) if tex_override is None else (tex_override, 'OVERRIDE')
    units, sents, rows, src, start, refs = extract(tex)
    legacy_claims = [s for s in sents if is_claim(s)]
    # non-table prose
    prose = [s for s in sents if not s['tab']]
    prose_claims = [s for s in prose if is_claim(s)]
    secs = []
    for i, l in enumerate(src):
        m = re.match(r'\\section\*?\{(.*?)\}', l)
        if m: secs.append((i + 1, m.group(1)))
    # audit-tag assignment: next '% AUDIT' tag at or after the unit's last line
    tags = [(i + 1, re.search(r'AUDIT: (B\d+)', l).group(1)) for i, l in enumerate(src) if re.match(r'% AUDIT: B\d+', l)]
    def tag_for(line):
        for ln, t in tags:
            if ln > line: return t
        return ''
    allc = []
    for s in prose_claims:
        allc.append(dict(kind='S', **s))
    for r in rows:
        allc.append(dict(kind='T', **r))
    for k, c in enumerate(allc):
        c['id'] = 'C%03d' % (k + 1)
        c['tag'] = tag_for(c['line'])
        c['hash'] = hashlib.sha1(c['text'].encode()).hexdigest()[:10]
        t = strip_tex(c['text'])
        c['numbers'] = re.findall(r'[-+]?\d[\d,]*\.?\d*', re.sub(r'\\[A-Za-z]+', ' ', t))
        c['lanes'] = sorted(set(re.findall(r'CFG\d+[a-z]?', c['text'])))
        c['keys'] = sorted(set(re.findall(r'\[([A-Z]+\d*)\]', c['text'])) - {'T'})
    cols = ['id', 'kind', 'line', 'sec', 'tag', 'hash', 'lanes', 'keys', 'numbers', 'text']
    if not quiet:
        with open(os.path.join(outdir, 'CFG241_claims.csv'), 'w', newline='') as f:
            w = csv.writer(f); w.writerow(cols)
            for c in allc:
                w.writerow([c['id'], c['kind'], c['line'], c['sec'], c['tag'], c['hash'], ';'.join(c['lanes']), ';'.join(c['keys']), ';'.join(c['numbers']), c['text']])
        json.dump(dict(sections=secs, n_sections_numbered=sum(1 for _, t in secs if not t.startswith('References'))), open(os.path.join(outdir, 'CFG241_sections.json'), 'w'))
    return dict(how=how, units=len(units), legacy_sents=len(sents), legacy_claims=len(legacy_claims),
                prose_sents=len(prose), prose_claims=len(prose_claims), rows=len(rows), claims=allc, secs=secs, src=src, refs=refs)

if __name__ == '__main__':
    r = main()
    print('repo: <repo>   tex read from:', r['how'], '  head', head_commit())
    print('units (collapsed tables):', r['units'])
    print('LEGACY enumeration (frozen throwaway rule; tables collapsed): sentence units', r['legacy_sents'], ' claim sentences', r['legacy_claims'])
    print('prose sentence units excluding table cells:', r['prose_sents'], ' prose claim sentences:', r['prose_claims'])
    print('table rows added as row-claims:', r['rows'])
    print('TOTAL claim units to classify (prose claims + table rows):', len(r['claims']))
    print('sections (numbered, excluding References):', sum(1 for _, t in r['secs'] if not t.startswith('References')), '| section commands incl. References:', len(r['secs']))
    ok = (r['legacy_sents'] == 120 and r['legacy_claims'] == 117)
    print('FROZEN COUNT REPRODUCED (120 / 117):', ok)
    sys.exit(0 if ok else 1)
