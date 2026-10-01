#!/usr/bin/env python3
"""CFG265_extract.py: frozen section-3 claim enumeration of the PAPER39 draft (read at the pinned commit 53f374ae2).
Writes CFG265_claims.csv; prints counts. Exit 0 if the frozen throwaway count (115 prose sentences, 115 claim sentences,
25 table rows, 140 claim units) is reproduced and the tex sha256 matches; 1 if not (the difference is printed and kept)."""
import csv, re, sys, hashlib, os, collections
from CFG265_common import *


def main(tex_override=None, outdir=HERE, quiet=False):
    tex, how = pin_text(TEX_REL) if tex_override is None else (tex_override, 'OVERRIDE')
    E = extract(tex)
    sents, rows, src = E['sents'], E['rows'], E['src']
    claims_s = [s for s in sents if is_claim(s)]
    non = [s for s in sents if not is_claim(s)]
    tags = [(i + 1, re.search(r'AUDIT: (B\d+)', l).group(1)) for i, l in enumerate(src) if re.match(r'% AUDIT: B\d+', l)]

    def tag_for(line):
        for ln, t in tags:
            if ln > line:
                return t
        return ''
    allc = [dict(kind='S', **s) for s in claims_s] + [dict(kind='T', **r) for r in rows]
    for k, c in enumerate(allc):
        c['id'] = 'C%03d' % (k + 1)
        c['tag'] = tag_for(c['line'])
        c['hash'] = hashlib.sha1(c['text'].encode()).hexdigest()[:10]
        t = strip_tex(c['text'])
        c['numbers'] = re.findall(r'[-+]?\d[\d,]*\.?\d*', re.sub(r'\\[A-Za-z]+', ' ', t))
        c['lanes'] = sorted(set(re.findall(r'CFG\d+[A-Z]?', c['text'])))
        c['keys'] = sorted(set(k2.strip() for grp in re.findall(r'\[([A-Z]+\d*(?:, ?[A-Z]+\d*)*)\]', c['text']) for k2 in grp.split(',')))
        c['quant'] = sorted(set(m.group(0).lower() for m in re.finditer(r'\b(any|every|all|whatever|always|never|however many|exactly|in every|at every|for any)\b', t, re.I)))
    if not quiet:
        cols = ['id', 'kind', 'line', 'sec', 'tag', 'hash', 'lanes', 'keys', 'quant', 'numbers', 'text']
        with open(os.path.join(outdir, 'CFG265_claims.csv'), 'w', newline='') as f:
            w = csv.writer(f); w.writerow(cols)
            for c in allc:
                w.writerow([c['id'], c['kind'], c['line'], c['sec'], c['tag'], c['hash'], ';'.join(c['lanes']), ';'.join(c['keys']), ';'.join(c['quant']), ';'.join(c['numbers']), c['text']])
    return dict(how=how, sha=sha(tex), units=len(E['units']), sents=len(sents), claims_s=len(claims_s), non=non, rows=len(rows),
                header=len(E['header']), claims=allc, src=src, refs=references(tex), tex=tex)


if __name__ == '__main__':
    r = main()
    print('repo: <repo>   tex read from:', r['how'], '  current head', head_commit())
    print('tex sha256 %s  matches frozen: %s' % (r['sha'][:16], r['sha'] == TEX_SHA))
    print('units (incl. 25 row units + 1 header):', r['units'])
    print('prose sentence units:', r['sents'], '  prose claim sentences:', r['claims_s'], '  non-claims:', len(r['non']))
    for s in r['non']:
        print('   NON-CLAIM line %d: %s' % (s['line'], s['text'][:100]))
    print('table rows (header excluded):', r['rows'], '  header rows:', r['header'])
    print('TOTAL claim units:', len(r['claims']))
    print('by section:', dict(collections.Counter(c['sec'] for c in r['claims'])))
    print('reference entries:', len(r['refs']), sorted(r['refs']))
    fp = sorted(set(re.findall(r'\\fpath\{([^}]*)\}', r['tex'])))
    print('fpath mentions:', fp)
    for p in fp:
        cand = [p, 'campaign_fresh_gravity/' + p, 'qwen_claude_field_theory/papers_2026/' + p]
        ok = [c for c in cand if pin_text(c.rstrip('/'))[1] != 'MISSING' or ls_pin(c)]
        print('   %-60s exists at pin: %s' % (p, ok[0] if ok else 'NOT FOUND'))
    ok = (r['sents'] == 115 and r['claims_s'] == 115 and r['rows'] == 25 and len(r['claims']) == 140 and r['sha'] == TEX_SHA)
    print('FROZEN COUNT REPRODUCED (115 / 115 / 25 / 140) and sha matches:', ok)
    sys.exit(0 if ok else 1)
