#!/usr/bin/env python3
"""CFG265_audit_anchor.py: frozen-criteria P10 (audit anchoring) and P11 (PDF / zenodo drift).
P10: parses the R(...) rows of PAPER39_audit.py AS TEXT (the script is never executed or imported), counts rows per source,
BARE regexes (fewer than 12 literal characters of context around the capture group) and whether their captured digits occur
more than once in the source, and the share of the tex's numeric tokens that sit in no audit literal of their own tag block.
Also checks the Reproducibility sentence's list of sources against the audit's SRC dictionary.
P11: pdftotext (if present) on the committed PDF; decimal tokens of the PDF vs the tex; the .zenodo.json description vs the
abstract (disclosure, not-deposited wording). Exit 0 if it completed."""
import re, os, sys, json, subprocess, shutil, tempfile, collections
from CFG265_common import *


def main():
    at, _ = pin_text(AUDIT_REL)
    tex, _ = pin_text(TEX_REL)
    src = dict(re.findall(r'^\s+"(\w+)":\s*(?:CFG|CM)?\s*\+?\s*"([^"]+)"', at, re.M))
    # resolve prefixes
    srcmap = {}
    for m in re.finditer(r'^\s+"(\w+)":\s*(CFG \+ |CM \+ )?"([^"]+)",', at, re.M):
        pre = {'CFG + ': 'campaign_fresh_gravity/', 'CM + ': 'campaign_fresh_gravity/closure_map/'}.get(m.group(2) or '', '')
        srcmap[m.group(1)] = pre + m.group(3)
    rows = re.findall(r'^R\("(B\d+)", "([^"]*)", "(\w+)", r"((?:[^"\\]|\\.)*)"(?:,\s*r?"((?:[^"\\]|\\.)*)")?\)', at, re.M)
    print('repo <repo>; audit read as text at', PIN)
    print('audit rows parsed:', len(rows), '(the draft and the commit message say 141)')
    per = collections.Counter(r[2] for r in rows)
    print('rows per source key:', dict(per))
    print('  share of rows checked against the status page (STAND):', '%d of %d (%.0f%%)' % (per['STAND'], len(rows), 100.0 * per['STAND'] / len(rows)))
    print('SRC dictionary (%d files):' % len(srcmap))
    for k, v in srcmap.items():
        print('   %-6s %s' % (k, v))
    # Reproducibility sentence
    m = re.search(r'The sources it reads are (.*?)\. No new analysis', tex, re.S)
    sent = m.group(1) if m else ''
    named = sorted(set(re.findall(r'CFG\d+', sent.replace('CFG242--CFG245', 'CFG242 CFG243 CFG244 CFG245'))))
    insrc = sorted(set(re.findall(r'CFG(\d+)', ' '.join(srcmap.values()))))
    insrc = ['CFG' + x for x in insrc]
    print('\nReproducibility sentence names lane READMEs:', named)
    print('lane files actually in SRC:', insrc)
    print('  named but NOT read by the audit:', [x for x in named if x not in insrc])
    print('  read by the audit but NOT named:', [x for x in insrc if x not in named])
    print('  "the two notes cited for kappa": SRC holds CFG0_README.md (kappa values) and VERIFICATION_REPORTED_ONLY (the footing reading);'
          ' the footing note itself (real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.*) is not in SRC')
    # BARE regex rows
    bare = []
    for b, val, key, rx, texlit in rows:
        lit = re.sub(r'\\.', 'x', rx)
        ctx = re.sub(r'\([^)]*\)', '', lit, count=1)
        if len(ctx) < 12:
            t, _ = pin_text(srcmap[key])
            occ = len(re.findall(re.escape(val.replace('−', '−')), t)) if t else -1
            bare.append((b, val, key, rx, occ))
    print('\nBARE rows (fewer than 12 literal context characters):', len(bare))
    for r in bare:
        print('   %s %-12s %-6s %-28s occurrences of the value in the source: %d' % r)
    # numeric tokens outside any audit literal of their block
    lines = tex.split('\n')
    blocks, cur = {}, []
    for ln in lines:
        mm = re.match(r'% AUDIT: (B\d+)', ln)
        if mm:
            blocks[mm.group(1)] = '\n'.join(cur); cur = []
        elif not ln.startswith('%'):
            cur.append(ln)
    lits = collections.defaultdict(list)
    for b, val, key, rx, texlit in rows:
        lits[b].append(texlit or val)
    tot = outside = 0
    examples = []
    for b, txt in blocks.items():
        t2 = re.sub(r'\\(ref|label|fpath)\{[^}]*\}', ' ', txt)
        t2 = re.sub(r'CFG\d+[A-Z]?', ' ', t2)
        t2 = re.sub(r'\b(19|20)\d\d\b', ' ', t2)
        t2 = re.sub(r'L\{[0-9.]+\\linewidth\}|\\setlength\{[^}]*\}\{[^}]*\}', ' ', t2)   # column widths
        t2 = re.sub(r'\b[0-9a-f]{9}\b', ' ', t2)                                    # commit hashes
        t2 = re.sub(r'\b(1[0-3]|[1-9])(A|B|C-[a-d]|D)\b', ' ', t2)                      # door labels 11A, 11C-a, ...
        t2 = re.sub(r'\b(Gap~|G|S|R)\d+\b', ' ', t2)                                   # gate / item labels
        for mm in re.finditer(r'(?<![\w.])\d+(?:\.\d+)?(?:e[-+]?\d+)?', t2):
            tok = mm.group(0)
            if len(tok) == 1:
                continue
            tot += 1
            if not any(tok in l for l in lits.get(b, [])):
                outside += 1
                if len(examples) < 40:
                    examples.append('%s:%s' % (b, tok))
    print('\nnumeric tokens (2+ characters, lane ids and years removed) in tagged blocks: %d; in no audit literal of their own block: %d (%.0f%%)' % (tot, outside, 100.0 * outside / max(tot, 1)))
    print('  examples:', ' '.join(examples))
    print('  the docstring itself says the route counts 25 / 22 / 2 / 1 are not audited:', 'route counts 25 / 22 / 2 / 1' in at)
    # P11
    print('\nP11 PDF / zenodo')
    pdf_rel = TEX_REL.replace('.tex', '.pdf')
    pdftotext = shutil.which('pdftotext')
    if pdftotext:
        with tempfile.TemporaryDirectory() as td:
            pdfp = os.path.join(td, 'p.pdf')
            r = subprocess.run(['git', '-C', REPO, 'show', '%s:%s' % (PIN, pdf_rel)], capture_output=True)
            open(pdfp, 'wb').write(r.stdout)
            subprocess.run([pdftotext, '-layout', pdfp, os.path.join(td, 'p.txt')], capture_output=True)
            ptxt = open(os.path.join(td, 'p.txt'), encoding='utf-8', errors='replace').read()
        dec = lambda s: set(re.findall(r'\d+\.\d+', s.replace('−', '-')))
        tbody = re.sub(r'(?m)^%.*$', '', tex)
        tonly, ponly = sorted(dec(tbody) - dec(ptxt)), sorted(dec(ptxt) - dec(tbody))
        print('  PDF bytes %d; decimal tokens in tex not in PDF text: %s' % (len(r.stdout), tonly))
        print('  decimal tokens in PDF text not in tex: %s' % ponly)
    else:
        print('  pdftotext not found: PDF drift NOT CHECKED')
    zj, how = pin_text(TEX_REL.replace('.tex', '.zenodo.json'))
    if zj:
        z = json.loads(zj)
        meta = z.get('metadata', z)
        desc = re.sub('<[^>]+>', ' ', meta.get('description', ''))
        print('  zenodo.json title:', meta.get('title', '')[:200])
        print('  zenodo.json version:', meta.get('version'), '| upload_type:', meta.get('upload_type'))
        for key in ('AI-assisted', 'not peer reviewed', 'not peer-reviewed', 'fitted', 'closed', '331', '25 ', '22 ', 'survival test', 'lean, not a detection'):
            print('   description contains %-22r %s' % (key, key.lower() in desc.lower()))
        dn = set(re.findall(r'\d+\.\d+', desc)); an = set(re.findall(r'\d+\.\d+', re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)))
        print('  decimal tokens in the description not in the abstract:', sorted(dn - an))
    sys.exit(0)


if __name__ == '__main__':
    main()
