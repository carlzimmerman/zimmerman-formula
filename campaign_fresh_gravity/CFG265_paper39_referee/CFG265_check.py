#!/usr/bin/env python3
"""CFG265_check.py: the frozen claim-checker pipeline (frozen criteria sections 3b, 3c, 7). Flags are HINTS; the verdict is the
hand table CFG265_classification.csv. Families: NUM VERB CAVEAT CITE WITHDRAWN SCOPE ARITH LANE CLASS NOSRC.
The NUM / VERB / CAVEAT / SCOPE / NOSRC machinery is adapted from CFG241_check.py (rule v4: integers match as integers, ranges
as pairs, a number counts as supported only from the top-ranked paragraph or from a lane the claim names; verbs negation-aware).
  python3 CFG265_check.py                               main run on the draft at 53f374ae2; exit 0 coverage met, 2 otherwise
  python3 CFG265_check.py --plant                       14 plants + 3 paraphrases in scratch copies; exit 0 all caught and no
                                                        paraphrase newly flagged, 1 otherwise, 3 if an old string is missing
  python3 CFG265_check.py --plant --disable NUM --only M1   self-disable run (must exit 1)
Sources are read at 53f374ae2 (git show), never the working tree, except untracked files (none expected)."""
import re, os, sys, csv, json, argparse, hashlib, collections
from CFG265_common import *
import CFG265_extract as EX

LANES = [4, 28, 29, 43, 44, 48, 49, 50, 63, 70, 72] + list(range(117, 125)) + [130, 131] + list(range(151, 160)) + [171, 172, 173, 188, 191, 200, 230, 231, 232, 240, 242, 243, 244, 245, 251, 252, 253, 254, 259]
EXT = ('.md', '.out', '.txt', '.csv', '.json', '.lean')


def corpus_files():
    sizes = ls_pin_sizes("campaign_fresh_gravity/")
    pat = re.compile(r'^campaign_fresh_gravity/CFG(%s)[A-Z]?(_[^/]*)(/.*)?$' % '|'.join(map(str, LANES)))
    files = [f for f, s in sizes.items() if pat.match(f) and f.endswith(EXT) and not (f.endswith('.json') and s > 2_000_000)]
    files += [f for f in sizes if re.match(r'^campaign_fresh_gravity/(STANDING_[^/]*\.md|LEDGER\.md|closure_map/[^/]*\.(md|out))$', f)]
    cc = "fable_independent_2026/lean_2026/ChainCert/"
    files += [f for f in ls_pin(cc) if f.endswith(('.lean', 'README.md', 'verify_chain.out', 'Axioms.out', 'Mutate.out'))]
    files += [f for f in ls_pin("gemini_pi_puzzle/") if f.endswith('.md')]
    files += ["real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out", "citations/CORRECTIONS.md", "citations/UNVERIFIED.md",
              "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md", "prep_2026/gaia_dr4_prep/dr4_ready_1/edge_table_dr4.json"]
    files += [f for f in ls_pin("prep_2026/gaia_dr4_prep/") if re.search(r'AMENDMENT\d+_DRAFT.*\.md$|dr4_ready_1/[^/]*\.md$', f)]
    return sorted(set(f for f in files if 'CFG265' not in f))


STOP = set("that this with from have which their there these those about would could between against across into over under than then also only when where while whose such each both more most some many much very been being were what they them said same other another still even just upon within without after before above below here none every".split())
NUMRE = re.compile(r'(?<![\w.])[-+\u2212]?\d[\d,]*\.?\d*')


def norm_nums(text):
    t = text.replace('\u2212', '-').replace('\u2013', '-')
    out = []
    for m in NUMRE.finditer(t):
        s = m.group(0).replace(',', '').lstrip('+').rstrip('.')
        try:
            out.append((s, float(s)))
        except ValueError:
            pass
    return out


def words(text):
    return set(w for w in re.findall(r'[a-z]{4,}', text.lower()) if w not in STOP)


class Corpus:
    def __init__(self):
        self.paras = []
        self.files = corpus_files()
        for f in self.files:
            t, how = pin_text(f)
            if t is None:
                continue
            lines = t.split('\n')
            blk, start = [], 1
            for i, ln in enumerate(lines + ['']):
                if ln.strip() == '':
                    if blk:
                        txt = '\n'.join(blk)
                        if len(txt) > 1500 and len(blk) > 1:
                            for k, l2 in enumerate(blk):
                                if l2.strip():
                                    self._add(f, start + k, l2)
                        else:
                            self._add(f, start, txt)
                    blk = []
                else:
                    if not blk:
                        start = i + 1
                    blk.append(ln)
        self.num_index = collections.defaultdict(set)
        self.by_file = collections.defaultdict(list)
        for k, p in enumerate(self.paras):
            self.by_file[p['file']].append(k)
            for s, v in p['nums']:
                self.num_index[round(abs(v), 6)].add(k)

    def _add(self, f, line, txt):
        txt = txt[:4000]
        self.paras.append(dict(file=f, line=line, text=txt, nums=norm_nums(txt), words=words(txt)))


def num_match(tok, pnums):
    s, v = tok
    if '.' not in s:
        a = s.lstrip('-+')
        return any(ps.lstrip('-+') == a for ps, _ in pnums)
    d = len(s.split('.')[1])
    tol = 0.5 * 10 ** (-d) + 1e-9
    return any(abs(abs(x) - abs(v)) <= tol for _, x in pnums)


def claim_numbers(text):
    t = re.sub(r'\\(ref|label|fpath|cite)\{[^}]*\}', ' ', text)
    t = re.sub(r'CFG\d+[A-Z]?', ' ', t)
    t = re.sub(r'\b[0-9a-f]{9}\b', ' ', t)
    t = re.sub(r'\[[A-Z]+\d*(, ?[A-Z]+\d*)*\]', ' ', t)
    t = re.sub(r'\\[A-Za-z]+', ' ', t)
    t = re.sub(r'\^\{?-?\d+\}?', ' ', t)
    out = []
    for s, v in norm_nums(t):
        if s.lstrip('-').isdigit() and abs(v) < 10:
            continue
        if s.lstrip('-').isdigit() and 1900 <= abs(v) <= 2100:
            continue
        out.append((s, v))
    return out


def lane_dirs(names):
    return ['CFG%s_' % re.sub(r'[A-Z]$', '', x[3:]) for x in names] + ['CFG%s/' % x[3:] for x in names]


VERB = [(4, r'prov\w*|establish\w*|exclud\w*|rule[sd]? out|reject\w*|detect\w*|confirm\w*|decisive|refut\w*'),
        (3, r'show\w*|demonstrat\w*|certif\w*|reveal\w*'),
        (2, r'find\w*|found|indicat\w*|impl(y|ies|ied)|conclude\w*'),
        (1, r'suggest\w*|lean\w*|hint\w*|gives?|favour\w*|adds?'),
        (0, r'lies inside|consistent with|sits?|reads?|descriptive')]


def verb_all(text):
    out = []
    for L, rx in VERB:
        for m in re.finditer(r'\b(' + rx + r')\b', text, re.I):
            pre = text[max(0, m.start() - 18):m.start()].lower()
            if re.search(r'\b(not|no|never|without|nor)\b', pre):
                continue
            out.append((L, m.group(0).lower()))
    return out


def verb_level(text):
    lv = -1
    for L, v in verb_all(text):
        lv = max(lv, L)
    return lv


CAVEATS = ['post hoc', 'not blind', 'withdrawn', 'not to be quoted', 'not possible', 'non-diagnostic', 'non-discriminating', 'a reading', 'not a theorem',
           'not a detection', 'conditional', 'hand-check', 'toy', 'not independent', 'unverified', 'hypothesis', 'assumes', 'premise', 'restatement',
           'extrapolation', 'not a derivation', 'interpretation']
HYP = r'\b(if|provided|assum\w*|hypothes\w*|requires?|conditional|premises?|for the p2 kernel|frozen class|spherical|monomials?|pointwise|0 ?<= ?b)\b'
QUANT = re.compile(r'\b(any|every|all|whatever|always|never|however many|exactly|in every|at every|for any)\s+(\w+)', re.I)
ROW_VERDICT_BAD = r'UNDEFINED|NOT ADDRESSED|RESTATEMENT|restatement|p\\\*|p\*|stop rule|hand-check|phase 1|realis'
ROW_VERDICT_FAIL = r'\bFAIL|\bF\b|no-go|NO-GO|KILL|DEAD|fails'


def references_meta(tex):
    refs = references(tex)
    meta = {}
    for k, r in refs.items():
        auth = r.split(' 20')[0] if not k.startswith('P3') else ''
        sur = [re.sub(r'[\\{}`\'^~]', '', a.split('~')[-1]).strip() for a in re.split(r',| \\& ', auth) if a.strip() and 'et al' not in a]
        sur = [s.replace('Cot', 'Cot') for s in sur if s]
        if 'et al' in auth:
            sur.append(re.sub(r'[\\{}`\'^~.]', '', auth.split('~')[-1].replace(' et al', '')).strip())
        title = re.search(r"``(.*?)''", r)
        tw = [w[:5] for w in re.findall(r'[a-z]{4,}', (title.group(1) if title else '').lower()) if w not in STOP]
        meta[k] = dict(surnames=[s for s in sur if s], title5=set(tw))
    return meta


def load_withdrawn():
    p = os.path.join(HERE, 'CFG265_withdrawn_lexicon.json')
    return json.load(open(p))['patterns']


# ------------------------------------------------------------------ ARITH relations (>= 20, frozen section 4 P9)
def _f(tex, rx, g=1):
    m = re.search(rx, tex)
    return None if not m else m.group(g)


def arith_checks(tex, rows):
    R = []

    def add(i, anchor, ok, det):
        R.append(dict(id=i, anchor=anchor, ok=bool(ok), detail=det))
    n_tot, n_ng = _f(tex, r'gives (\d+) routes: (\d+) scoped no-gos', 1), _f(tex, r'gives (\d+) routes: (\d+) scoped no-gos', 2)
    ok1 = n_tot is not None and int(n_tot) == int(n_ng) + 2 + 1
    add('R01', 'Counting the rows honestly gives', ok1, 'total %s = no-gos %s + 2 + 1' % (n_tot, n_ng))
    tc = collections.Counter('no-go' if r['text'].split('&')[-1].strip().startswith('no-go') else ('nomech' if 'no mechanism' in r['text'].split('&')[-1] else ('real' if 'realisable' in r['text'].split('&')[-1] else 'other')) for r in rows)
    okc = n_tot is not None and len(rows) == int(n_tot) and tc['no-go'] == int(n_ng) and tc['nomech'] == 2 and tc['real'] == 1
    add('R02', 'ARITH-COUNT', okc, 'table rows %d, no-go %d, no mechanism %d, realisable %d vs prose %s/%s/2/1' % (len(rows), tc['no-go'], tc['nomech'], tc['real'], n_tot, n_ng))
    m = re.search(r'D = (\d+), P = (\d+), I = (\d+), X = (\d+), U = (\d+)', tex)
    n54 = _f(tex, r'documentary count of (\d+) committed')
    add('R03', 'documentary count', m and n54 and sum(map(int, m.groups())) == int(n54), 'sum %s vs %s' % (sum(map(int, m.groups())) if m else None, n54))
    s1 = re.search(r'\((\d+) theorems, (\d+) in the library\)', tex); s2 = re.search(r'\((\d+) theorems, (\d+)\)', tex); s3 = re.search(r'\((\d+) theorems, (\d+)\)\.', tex)
    steps = re.findall(r'\((\d+) theorems, (\d+)(?: in the library)?\)', tex)
    ok4 = len(steps) == 3 and all(int(steps[i][1]) + int(steps[i + 1][0]) == int(steps[i + 1][1]) for i in range(2))
    add('R04', 'theorems,', ok4, 'cumulative steps %s' % steps)
    vc = _f(tex, r'reporting (\d+) theorems checked'); ab = _f(tex, r'library of (\d+) theorems')
    add('R05', 'theorems', steps and vc and ab and int(vc) == int(steps[-1][1]) == int(ab), 'verifier %s, abstract %s, last step %s' % (vc, ab, steps[-1][1] if steps else None))
    kb = re.search(r'\$\\hat\\gamma\\ge(1\.\d+)\$ kills B', tex)
    add('R06', 'kills B', kb and abs(float(kb.group(1)) - (1 + 3 * 0.028)) < 0.002, 'B kill line >= 1 + 3 x 0.028: %s' % (kb.group(1) if kb else 'no ">=" form'))
    fl = _f(tex, r"floor is (1\.\d+) \(alt")
    kl = re.search(r'\$\\hat\\gamma\\le(1\.\d+)\$ kills the bare law', tex)
    add('R07', 'kills the bare law', kl and fl and 1.0 < float(kl.group(1)) < float(fl), 'bare-law kill line "<=" and below the floor: %s' % (kl.group(1) if kl else 'no "<=" form'))
    ss = _f(tex, r'sigma_\{\\rm sys\}=(0\.\d+)'); cap = _f(tex, r'the cap is ([\d.]+)\$\\sigma')
    add('R08', 'the cap is', fl and ss and cap and abs((float(fl) - 1) / float(ss) - float(cap)) < 0.06, 'cap (floor-1)/sigma_sys = %s' % ((float(fl) - 1) / float(ss) if fl and ss else None))
    np_ = _f(tex, r'needs about ([\d,]+) pairs')
    if np_ and fl and ss:
        cpp = 3.291
        n3 = cpp ** 2 / (((float(fl) - 1) / 3) ** 2 - float(ss) ** 2)
        add('R09', 'pairs', abs(int(np_.replace(',', '')) - n3) / n3 < 0.05, 'N3sigma %.0f vs %s' % (n3, np_))
    else:
        add('R09', 'pairs', False, 'pairs not found')
    zk = re.search(r'\+0\.3245\\pm0\.038\$ \(([\d.]+)\$\\sigma', tex); flo = _f(tex, r'a ([\d.]+)-dex systematic floor')
    add('R10', 'Kaplan', zk and flo and abs(0.3245 / (0.038 ** 2 + float(flo) ** 2) ** 0.5 - float(zk.group(1))) < 0.02, 'KM z %s' % (zk.group(1) if zk else None))
    a1, a2 = _f(tex, r'median of \$-(0\.\d+)\$ dex'), _f(tex, r'or \$-(0\.\d+)\$ dex')
    add('R11', 'a fifth to a third', a1 and a2 and 0.17 < float(a1) / 0.3245 < 0.23 and 0.30 < float(a2) / 0.3245 < 0.36, 'fractions %s %s' % (a1, a2))
    # v1.1 (harness fix after the first main run, before any plant run): the tex closes $ after \sigma
    ku, ks = _f(tex, r'gives \$\\kappa=([\d.]+)\$, ([\d.]+)\$\\sigma\$ off', 1), _f(tex, r'gives \$\\kappa=([\d.]+)\$, ([\d.]+)\$\\sigma\$ off', 2)
    add('R12', 'Unruh', ku and ks and abs((float(ku) - 0.465) / 0.076 - float(ks)) < 0.06, 'Unruh sigma')
    add('R13', 'lies inside both', abs(0.5 - 0.465) < 0.076 and abs(0.5 - 0.547) < 0.175 and '0.465\\pm0.076' in tex and '0.547\\pm0.175' in tex, '1/2 inside both')
    gt = _f(tex, r'\\Gamma\\tau=([\d.]+)\$ \(\$H_\\Lambda'); g1, g2 = _f(tex, r'needs \$\\Gamma\\ge\$ ([\d.]+) / ([\d.]+)', 1), _f(tex, r'needs \$\\Gamma\\ge\$ ([\d.]+) / ([\d.]+)', 2)
    add('R14', 'Gamma', gt and g1 and g2 and 4.0 <= float(gt) * float(g2) and float(gt) * float(g1) <= 4.3, 'Gamma tau x needed rates')
    add('R15', 'R^*', 'R^{*2}\\Lambda=8\\pi' in tex and 'a_0=c^2/(2R^*)' in tex, 'R*^2 Lambda = 8 pi and a0 = c^2/(2R*) give kappa = 1/2')
    add('R16', '32\\pi', 'G\\rho_\\Lambda=4a_0^2' in tex and '=32\\pi' in tex, '32 pi = 2^2 x 8 pi; rational 4')
    rb, bb = _f(tex, r'G_N<(0\.\d+)\$'), re.search(r'=(0\.\d+)\\pm(0\.\d+)\$ \[A20\]', tex)
    add('R17', 'excluded', rb and bb and (float(bb.group(1)) - float(rb)) / float(bb.group(2)) >= 3, 'BBN gap / quoted error = %.2f (>= 3 needed for "excluded" if the error is 1 sigma)' % ((float(bb.group(1)) - float(rb)) / float(bb.group(2)) if rb and bb else -1))
    mb = re.search(r'gives (1\.\d+)--(1\.\d+), which separates from ownership by ([\d.]+)--([\d.]+)', tex)
    if mb:
        st = 0.02759
        lo, hi = (float(mb.group(1)) - 1) / st, (float(mb.group(2)) - 1) / st
        add('R18', 'separates from ownership', abs(lo - float(mb.group(3))) < 0.1 and abs(hi - float(mb.group(4))) < 0.1, 'band %.2f-%.2f sigma vs stated %s-%s' % (lo, hi, mb.group(3), mb.group(4)))
    else:
        add('R18', 'separates from ownership', False, 'band sentence not found')
    s_abs, s_sat = _f(tex, r'failure \(([\d.]+--[\d.]+)\$\\sigma\$\)'), _f(tex, r'stays ([\d.]+ to [\d.]+)\$\\sigma')
    add('R19', '3.5', s_abs and s_sat and s_abs.replace('--', ' to ') == s_sat, 'abstract %s vs section 5 %s' % (s_abs, s_sat))
    pa = _f(tex, r'scales as \$M\^\{([\d.\-]+)\}\$')
    pr = re.search(r'\$p=([\d.]+)\$--([\d.]+)', tex)      # v1.1 harness fix: the tex closes $ after the first value
    add('R20', 'M^{0.33', pa and pr and pa == '%s-%s' % pr.groups(), 'abstract %s vs row %s' % (pa, pr.groups() if pr else None))
    r1, r2 = _f(tex, r'at 0\.065--([\d.]+) \$g'), _f(tex, r'exchange forms give ([\d.]+) \$g')
    add('R21', 'g_{\\rm law}', r1 and r2 and r1 == r2, 'Gap 2 upper %s vs S6 %s' % (r1, r2))
    add('R22', 'of 40', '8 of 40' in tex and '33 of the 40' in tex, 'both of 40')
    n0 = _f(tex, r'\$n\(t_\{\\rm ff\}\)=([\d.]+)\$, minimum'); n1 = _f(tex, r'keeps \$n=([\d.]+)\$'); n2 = _f(tex, r'\(\$n\(t_\{\\rm ff\}\)=([\d.]+)\$ against')
    add('R23', 'n(t_{\\rm ff})', n0 and n1 and n2 and n0 == n1 == n2, 'latch n %s %s %s' % (n0, n1, n2))
    o1, o2 = _f(tex, r'\\Omega h\^2=0\.1200\\times10\^\{(-?[\d.]+)\}\$ at \$z=1100\$\)'), _f(tex, r'supplies \$\\Omega h\^2=0\.1200\\times10\^\{(-?[\d.]+)\}\$ at \$z=1100\$, and')
    add('R24', '1376', o1 and o2 and o1 == o2, 'abstract %s vs S1 %s' % (o1, o2))
    return R


def run_pipeline(corp, tex, disable=()):
    r = EX.main(tex_override=tex, quiet=True)
    claims = r['claims']
    E = extract(tex)
    meta = references_meta(tex)
    allsur = {s.lower(): k for k, m in meta.items() for s in m['surnames']}
    wd = load_withdrawn()
    at, _ = pin_text(AUDIT_REL)
    srcmap = {}
    for m in re.finditer(r'^\s+"(\w+)":\s*(CFG \+ |CM \+ )?"([^"]+)",', at, re.M):
        pre = {'CFG + ': 'campaign_fresh_gravity/', 'CM + ': 'campaign_fresh_gravity/closure_map/'}.get(m.group(2) or '', '')
        srcmap[m.group(1)] = pre + m.group(3)
    audit_ptr = collections.defaultdict(set)
    for m in re.finditer(r'^R\("(B\d+)", "[^"]*", "(\w+)"', at, re.M):
        audit_ptr[m.group(1)].add(srcmap.get(m.group(2), ''))
    arith = arith_checks(tex, E['rows'])
    tc_bad = [a for a in arith if a['id'] == 'R02' and not a['ok']]
    over = None
    if tc_bad:
        n_ng = _f(tex, r'gives (\d+) routes: (\d+) scoped no-gos', 2)
        cnt = sum(1 for rw in E['rows'] if rw['text'].split('&')[-1].strip().startswith('no-go'))
        over = 'no-go' if (n_ng and cnt > int(n_ng)) else 'other'
    ten, _ = pin_text("campaign_fresh_gravity/closure_map/TEN_DOORS_RESULT_2026-09-29.md")
    d11, _ = pin_text("campaign_fresh_gravity/closure_map/DOOR11_RESULT_2026-09-29.md")
    for c in claims:
        text = c['text']
        toks = claim_numbers(text)
        cw = words(strip_tex(text))
        lanes_here = sorted(set(re.findall(r'CFG\d+[A-Z]?', text)))
        lanes_para = sorted(set(re.findall(r'CFG\d+[A-Z]?', c.get('para') or text)))
        ld = lane_dirs(lanes_para)
        pf = audit_ptr.get(c['tag'], set())
        cand = set()
        for s, v in toks:
            cand |= corp.num_index.get(round(abs(v), 6), set())
        if len(cand) < 40:
            for k, p in enumerate(corp.paras):
                if len(cw & p['words']) >= 4:
                    cand.add(k)
        for f in pf:
            cand |= set(corp.by_file.get(f, []))
        scored = []
        for k in cand:
            p = corp.paras[k]
            n = sum(1 for tk in toks if num_match(tk, p['nums']))
            w = len(cw & p['words'])
            bonus = 2.0 if (any(d in p['file'] for d in ld) or p['file'] in pf) else 0.0
            scored.append((3 * n + 0.5 * min(w, 8) + bonus, n, w, k))
        scored.sort(reverse=True)
        top = scored[:3]
        c['top'] = [(corp.paras[k]['file'], corp.paras[k]['line'], round(sc, 1), n, w) for sc, n, w, k in top]
        c['top_text'] = [corp.paras[k]['text'] for _, _, _, k in top]
        fl = []
        # NUM (v4)
        for tk in toks:
            ok = False
            for rank, (sc, n, w, k) in enumerate(top):
                if not num_match(tk, corp.paras[k]['nums']):
                    continue
                if rank == 0 and (n >= 2 or w >= 2 or len(toks) == 1):
                    ok = True
                if rank > 0 and (n >= 2 or w >= 2) and any(d in corp.paras[k]['file'] for d in ld):
                    ok = True
            if not ok:
                fl.append(('NUM', tk[0]))
        tt = re.sub(r'\\[A-Za-z]+', ' ', strip_tex(text)).replace('--', ' to ').replace('\u2212', '-').replace('$', ' ')
        for m in re.finditer(r'(?<![\w.])(-?\d[\d,]*\.?\d*)\s*(?:to|-)\s*(-?\d[\d,]*\.?\d*)', tt):
            A_, B_ = m.group(1).replace(',', ''), m.group(2).replace(',', '')
            if A_.lstrip('-').isdigit() and B_.lstrip('-').isdigit() and abs(float(A_)) < 10 and abs(float(B_)) < 10:
                continue
            rx = r'(?<![\d.])' + re.escape(A_.lstrip('-')) + r'(?![\d])[^0-9]{1,14}(?<![\d.])' + re.escape(B_.lstrip('-')) + r'(?![\d])'
            if not any(re.search(rx, sp_.replace('\u2212', '-').replace('\u2013', '-')) for sp_ in c['top_text']):
                fl.append(('NUM', 'range:%s-%s' % (A_, B_)))
        # VERB
        cvs = [(L, v) for L, v in verb_all(strip_tex(text)) if L >= 2]
        if cvs and top:
            best = (-1, '')
            for sc, n, w, k in top:
                for sen in re.split(r'(?<=[.;])\s+', corp.paras[k]['text']):
                    s2 = sum(1 for tk in toks if num_match(tk, norm_nums(sen))) * 2 + len(cw & words(sen))
                    if s2 > best[0]:
                        best = (s2, sen)
            sl = max(verb_level(best[1]), 0)
            for L, v in cvs:
                if L > sl:
                    fl.append(('VERB', v))
        # CAVEAT
        ptxt = (c.get('para') or text).lower()
        srcall = ' '.join(c['top_text']).lower()
        for cv_ in CAVEATS:
            if cv_ in srcall and cv_ not in ptxt:
                fl.append(('CAVEAT', cv_))
        # CITE (a) surname before a key, (b) phantom, (c) KEYTOPIC
        for m in re.finditer(r'\[([A-Z]+\d*(?:, ?[A-Z]+\d*)*)\]', text):
            pre = strip_tex(text[max(0, m.start() - 40):m.start()])
            keys = [k.strip() for k in m.group(1).split(',')]
            for sur, sk in allsur.items():
                if re.search(r'\b' + re.escape(sur) + r'\b', pre.lower()) and sk not in keys:
                    fl.append(('CITE', '%s->%s' % (sur, ','.join(keys))))
            w5 = set(x[:5] for x in re.findall(r'[a-z]{4,}', strip_tex(text).lower()))
            for k in keys:
                if k in meta and meta[k]['title5'] and not (meta[k]['title5'] & w5):
                    fl.append(('CITE', 'keytopic:%s' % k))
                if k not in meta:
                    fl.append(('CITE', 'phantom-key:%s' % k))
        for m in re.finditer(r'([A-Z][a-z]+) et al\.\\ (\d{4})|\(([A-Z][a-z]+) (\d{4})\)', text):
            nm = (m.group(1) or m.group(3)).lower()
            if nm not in allsur:
                fl.append(('CITE', 'phantom:%s %s' % (m.group(1) or m.group(3), m.group(2) or m.group(4))))
        # WITHDRAWN
        for p_ in wd:
            if re.search(p_['rx'], text) and (not p_.get('rx2') or re.search(p_['rx2'], text)) and not (p_.get('except') and re.search(p_['except'], text, re.I)):
                fl.append(('WITHDRAWN', p_['id']))
        # SCOPE
        hyp = re.search(HYP, srcall)
        for m in QUANT.finditer(strip_tex(text)):
            if hyp or m.group(1).lower() not in srcall:
                fl.append(('SCOPE', m.group(0).lower()))
        # ARITH
        for a_ in arith:
            if a_['ok']:
                continue
            if a_['id'] == 'R02':
                if c['kind'] == 'T' and over == 'no-go' and text.split('&')[-1].strip().startswith('no-go'):
                    fl.append(('ARITH', 'R02'))
                if 'Counting the rows honestly gives' in text:
                    fl.append(('ARITH', 'R02'))
            elif a_['anchor'] in text:
                fl.append(('ARITH', a_['id']))
        # LANE
        if lanes_here and toks:
            lf = [f for f in corp.files if any(('/' + d) in ('/' + f.split('/', 1)[-1]) or f.startswith('campaign_fresh_gravity/' + d) for d in lane_dirs(lanes_here))]
            lidx = set(k for f in lf for k in corp.by_file.get(f, []))
            for tk in toks:
                hits = corp.num_index.get(round(abs(tk[1]), 6), set())
                if hits and not (hits & lidx):
                    fl.append(('LANE', tk[0]))
        # CLASS
        if c['kind'] == 'T':
            cls = text.split('&')[-1].strip()
            lm = re.search(r'(CFG\d+[A-Z]?), [0-9a-f]{9}', text)
            if lm and cls.startswith('no-go'):
                ln_ = lm.group(1)
                vt = []
                for f in corp.files:
                    if re.match(r'campaign_fresh_gravity/%s_[^/]+/(README|%s_README)\.md$' % (ln_, ln_), f):
                        t, _ = pin_text(f)
                        vt += [l for l in t.split('\n')[:80] if re.search(r'verdict|Verdict|VERDICT|Bottom line|bottom line|FAIL|no-go|binding|BINDING|realis|UNDEFINED|NOT ADDRESSED|restatement', l)]
                vt += [l for l in (ten + '\n' + d11).split('\n') if l.startswith('|') and ('(%s,' % ln_ in l or '(%s ' % ln_ in l)]
                vtxt = '\n'.join(vt)
                if re.search(ROW_VERDICT_BAD, vtxt) or not re.search(ROW_VERDICT_FAIL, vtxt):
                    fl.append(('CLASS', ln_))
        # NOSRC
        sup = any(n >= 2 or (n >= 1 and w >= 2) or (not toks and w >= 4) for sc, n, w, k in top)
        if not sup and (toks or re.search(r'shows?|finds?|confirm', text, re.I)):
            fl.append(('NOSRC', ''))
        c['flags'] = [x for x in fl if x[0] not in disable]
    return claims, arith


PLANTS = [
 ('M1', 'numeric swap', r'$n(t_{\rm ff})=0.791$, minimum 0.143', r'$n(t_{\rm ff})=0.917$, minimum 0.143', ('NUM',), '0.917$, minimum', '0.791$, minimum'),
 ('M2', 'stronger verb', r"The day's four swings (CFG242--245) add that ownership must remember boundness", r"The day's four swings (CFG242--245) prove that ownership must remember boundness", ('VERB',), 'prove that ownership', 'add that ownership'),
 ('M3', 'dropped caveat', r'\textbf{A cross-door pattern, a reading and not a theorem.}', r'\textbf{A cross-door pattern.}', ('CAVEAT',), 'Where cold matter is dynamical', 'Where cold matter is dynamical'),
 ('M4', 'wrong citation (surname)', r'2 Verlinde [V17]', r'2 Verlinde [M09]', ('CITE',), 'Verlinde [M09]', 'Verlinde [V17]'),
 ('M5', 'withdrawn claim', r'with $\kappa=\tfrac12$ fitted, never derived', r'with $\kappa=\tfrac12$ derived from the de Sitter Unruh temperature', ('WITHDRAWN',), 'derived from the de Sitter Unruh', 'fitted, never derived'),
 ('M6', 'scope inflation', r'with $f$ free, $\sigma(\log a_0)\ge3\sigma/\sqrt N$ (conditional on local slopes in $[0,\tfrac12]$)', r'with $f$ free, every sample and every kernel obeys $\sigma(\log a_0)\ge3\sigma/\sqrt N$', ('SCOPE', 'CAVEAT'), 'every sample and every kernel', 'conditional on local slopes'),
 ('M7', 'order-of-magnitude range', r'against $\approx4.1$--4.2 needed & no-go (Gate T)', r'against $\approx41$--42 needed & no-go (Gate T)', ('NUM',), '41$--42 needed', '4.1$--4.2 needed & no-go'),
 ('M8', 'invented support + phantom citation', r'and that the fluid must exist before structure.', r'and that the fluid must exist before structure. A Bullet Cluster lensing reanalysis independently confirms the early-fluid requirement at 4$\sigma$ (Clowe et al.\ 2027).', ('NOSRC', 'CITE'), 'Bullet Cluster', None),
 ('M9', 'count arithmetic', r'gives 25 routes: 22 scoped no-gos', r'gives 25 routes: 23 scoped no-gos', ('ARITH',), '23 scoped no-gos', '22 scoped no-gos'),
 ('M10', 'cumulative arithmetic', r'(62 theorems, 281)', r'(62 theorems, 291)', ('ARITH', 'NUM'), '(62 theorems, 291)', '(62 theorems, 281)'),
 ('M11', 'inequality direction swap', r'$\hat\gamma\ge1.084$ kills B; $\hat\gamma\le1.077$ kills the bare law', r'$\hat\gamma\le1.084$ kills B; $\hat\gamma\ge1.077$ kills the bare law', ('ARITH',), 'kills B;', 'kills B;'),
 ('M12', 'wrong lane attribution', r'(CFG243; the baryon-only $\sigma_b$ is 0.076 against the threshold 1.276)', r'(CFG253; the baryon-only $\sigma_b$ is 0.076 against the threshold 1.276)', ('LANE',), '(CFG253; the baryon-only', '(CFG243; the baryon-only'),
 ('M13', 'key-only citation swap', r'[O26, MC10]', r'[O26, M09]', ('CITE',), '[O26, M09]', '[O26, MC10]'),
 ('M14', 'route class upgrade', r'encodes $C(r)$, not derives it & realisable only', r'encodes $C(r)$, not derives it & no-go', ('CLASS', 'ARITH'), 'not derives it & no-go', 'not derives it & realisable only'),
]
# Fresh plants X1-X8 (written AFTER the flag code and after the frozen-set run; never used to tune a rule): the frozen set was
# frozen before the code, but the code was written knowing it, so its 14/14 is partly by construction.
PLANTS_X = [
 ('X1', 'numeric range swap', r'0.14--0.16 ($a_0/c$)', r'0.41--0.46 ($a_0/c$)', ('NUM',), '0.41--0.46', '0.14--0.16 ($a_0/c$)'),
 ('X2', 'dropped caveat', r'that branch is excluded, conditionally on its transfer assumptions, and', r'that branch is excluded, and', ('CAVEAT',), 'that branch is excluded, and', 'that branch is excluded, conditionally'),
 ('X3', 'stronger verb', r'CFG188 re-derived the field-equation core', r'CFG188 proved the field-equation core', ('VERB',), 'CFG188 proved', 'CFG188 re-derived'),
 ('X4', 'withdrawn number', r'A merged P2 law gives 1.063--1.127', r'A merged P2 law gives 1.16--1.18', ('WITHDRAWN', 'NUM', 'ARITH'), 'gives 1.16--1.18', 'gives 1.063--1.127'),
 ('X5', 'single-digit change', r'($n=2$ gives $\kappa=1.447$', r'($n=3$ gives $\kappa=1.447$', ('NUM', 'ARITH'), '$n=3$ gives', '$n=2$ gives'),
 ('X6', 'scope inflation', r'Every failure is a scoped no-go on its frozen class.', r'Every failure is a no-go for every model of its kind.', ('SCOPE', 'CAVEAT'), 'every model of its kind', 'scoped no-go on its frozen class'),
 ('X8', 'wrong lane attribution', r'\textbf{The 2026 dispersions (CFG259).}', r'\textbf{The 2026 dispersions (CFG229).}', ('LANE',), '(CFG229).}', '(CFG259).}'),
]
PARAS_X = [('X7', r'that is a prediction of a failed class, not a data statement.', r'that is what a failed class predicts, not a statement about data.', 'what a failed class predicts', 'a prediction of a failed class')]
PARAS = [
 ('P-a', r'Each item is a necessary condition read off the failures of scored classes; none is shown sufficient, and the set is not shown jointly satisfiable.',
  r'Each item is a necessary condition inferred from the failures of the scored classes; none has been shown sufficient, and the set has not been shown to be jointly satisfiable.', 'inferred from the failures', 'read off the failures'),
 ('P-b', r'A lean is not a detection.', r'A lean should not be read as a detection.', 'should not be read as a detection', 'A lean is not a detection.'),
 ('P-c', r'no stationary state; a ghost for $0<g t<2/3$', r'there is no stationary state, and a ghost appears for $0<g t<2/3$', 'there is no stationary state', 'no stationary state; a ghost'),
]


def plant_main(corp, tex0, disable, only, fresh=False):
    base, _ = run_pipeline(corp, tex0, disable)
    out, bad = [], 0
    if fresh:
        allp = list(PLANTS_X) + [(a, 'PARAPHRASE', b, c, (), d, e) for a, b, c, d, e in PARAS_X]
    else:
        allp = [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in PLANTS] + [(a, 'PARAPHRASE', b, c, (), d, e) for a, b, c, d, e in PARAS]
    for pid, kind, old, new, fam, frag, ofrag in allp:
        if only and pid != only:
            continue
        if tex0.count(old) != 1:
            out.append('%s: OLD STRING NOT FOUND exactly once (%d)' % (pid, tex0.count(old)))
            return out, 3
        cl1, _ = run_pipeline(corp, tex0.replace(old, new), disable)
        c1 = next((c for c in cl1 if frag in c['text']), None)
        c0 = next((c for c in base if ofrag and ofrag in c['text']), None)
        f1, f0 = set(c1['flags']) if c1 else set(), set(c0['flags']) if c0 else set()
        newf = f1 - f0
        if kind == 'PARAPHRASE':
            ok = (c1 is not None) and not newf
            out.append('%-4s PARAPHRASE  claim extracted: %s  new flags vs original: %s  -> %s' % (pid, c1 is not None, sorted(newf) or 'none', 'OK (not flagged)' if ok else 'FALSE POSITIVE'))
        else:
            hit = [x for x in newf if x[0] in fam]
            ok = c1 is not None and bool(hit)
            out.append('%-4s %-36s expected %-12s caught by %-46s other new flags %s -> %s' % (pid, kind, '/'.join(fam), str(sorted(hit)) if hit else 'NONE', sorted(x for x in newf if x not in hit) or '-', 'CAUGHT' if ok else 'MISSED'))
        if not ok:
            bad += 1
    return out, (1 if bad else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plant', action='store_true'); ap.add_argument('--disable', default=''); ap.add_argument('--only', default=''); ap.add_argument('--fresh', action='store_true')
    ap.add_argument('--classification', default=os.path.join(HERE, 'CFG265_classification.csv'))
    a = ap.parse_args()
    disable = tuple(x for x in a.disable.split(',') if x)
    corp = Corpus()
    print('repo <repo>; sources read at', PIN, '; current head', head_commit(), '; corpus files', len(set(p['file'] for p in corp.paras)), '; paragraphs', len(corp.paras))
    tex0, how = pin_text(TEX_REL)
    print('tex read from', how, 'sha256', sha(tex0)[:16])
    if a.plant:
        out, code = plant_main(corp, tex0, disable, a.only, a.fresh)
        print('\n'.join(out)); print('disabled families:', disable or 'none'); print('PLANT CONTROL EXIT', code)
        sys.exit(code)
    claims, arith = run_pipeline(corp, tex0, disable)
    with open(os.path.join(HERE, 'CFG265_worksheet.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'kind', 'line', 'sec', 'tag', 'flags', 'top_sources', 'text'])
        for c in claims:
            w.writerow([c['id'], c['kind'], c['line'], c['sec'], c['tag'], ' '.join('%s:%s' % x for x in c['flags']),
                        ' | '.join('%s:%d(s%.1f,n%d,w%d)' % t for t in c['top']), c['text']])
    json.dump([dict(id=c['id'], line=c['line'], flags=c['flags'], top=c['top'], top_text=[t[:600] for t in c['top_text']]) for c in claims],
              open(os.path.join(HERE, 'CFG265_worksheet.json'), 'w'))
    cnt = collections.Counter(x[0] for c in claims for x in c['flags'])
    print('claims:', len(claims), ' flag counts:', dict(cnt), ' claims with any flag:', sum(1 for c in claims if c['flags']))
    print('ARITH relations:', len(arith), ' failing:', [(x['id'], x['detail']) for x in arith if not x['ok']])
    for x in arith:
        print('   %s %s %s' % (x['id'], 'OK  ' if x['ok'] else 'FAIL', x['detail']))
    if os.path.exists(a.classification):
        rows = list(csv.DictReader(open(a.classification)))
        have = {r['id'] for r in rows}
        miss = [c['id'] for c in claims if c['id'] not in have]
        print('classification rows:', len(rows), ' claims without a row:', len(miss), miss[:10])
        hashes = {c['id']: c['hash'] for c in claims}
        stale = [r['id'] for r in rows if r.get('hash') and hashes.get(r['id']) != r['hash']]
        print('classification rows whose text hash does not match the extractor:', stale)
        if miss or stale:
            sys.exit(2)
        cls = collections.Counter(r['class'] for r in rows)
        print('class counts:', dict(cls))
        unv = cls.get('UNVERIFIABLE-OFFLINE', 0)
        print('UNVERIFIABLE-OFFLINE fraction: %.3f (target <= 0.10)' % (unv / len(claims)))
        fv = collections.defaultdict(lambda: [0, 0])
        for c in claims:
            r_ = next(r for r in rows if r['id'] == c['id'])
            nonf = r_['class'] != 'FAITHFUL'
            for fam in set(x[0] for x in c['flags']):
                fv[fam][0] += 1; fv[fam][1] += nonf
        print('flag precision against the hand verdict (claims flagged / of them hand non-FAITHFUL):', {k: tuple(v) for k, v in sorted(fv.items())})
        nonf_ids = [r['id'] for r in rows if r['class'] != 'FAITHFUL']
        unflagged = [i for i in nonf_ids if not next(c for c in claims if c['id'] == i)['flags']]
        print('hand non-FAITHFUL claims with no flag at all (flagger misses):', unflagged)
        sys.exit(0 if unv / len(claims) <= 0.10 else 2)
    print('no classification table yet'); sys.exit(2)


if __name__ == '__main__':
    main()
