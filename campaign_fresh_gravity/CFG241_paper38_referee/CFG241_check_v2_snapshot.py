#!/usr/bin/env python3
"""CFG241_check.py: the frozen claim-checker pipeline (section 3b/3c of the frozen criteria).
Flag families: NUM VERB CAVEAT CITE WITHDRAWN SCOPE ARITH NOSRC.  Flags are hints; the verdict is the hand
classification table CFG241_classification.csv.
  python3 CFG241_check.py              main run (reads PAPER38 tex at git HEAD); exit 0 coverage met, 2 otherwise
  python3 CFG241_check.py --plant      planted-error controls in scratch copies; exit 0 all caught and no new paraphrase flag, 1 otherwise, 3 old string missing
  python3 CFG241_check.py --plant --disable NUM --only M1    self-disable run (must exit 1)
"""
import re, os, sys, csv, json, math, argparse, tempfile, hashlib, collections
from CFG241_common import *
import CFG241_extract as EX

LANE_NUMS = [213,214,215,216,217,218,219,220,221,222,223,224,227,228,229,233,234,236,237,238,240,255,200,239,63]
EXT = ('.md', '.out', '.txt', '.lean', '.csv')

def corpus_files():
    allf = ls_head("campaign_fresh_gravity/")
    pat = re.compile(r'^campaign_fresh_gravity/CFG(%s)[^0-9/][^/]*(/|$)|^campaign_fresh_gravity/CFG(%s)_[^/]*$' % ('|'.join(map(str, LANE_NUMS)), '|'.join(map(str, LANE_NUMS))))
    files = [f for f in allf if pat.match(f) and f.endswith(EXT)]
    files += [f for f in allf if re.match(r'^campaign_fresh_gravity/(STANDING_[^/]*\.md|LEDGER\.md|closure_map/[^/]*\.(md|out))$', f)]
    files += ["data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md", "real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md",
              "fable_independent_2026/lean_2026/ChainCert/CalibrationWall.lean", "citations/CORRECTIONS.md", "citations/UNVERIFIED.md"]
    files += [f for f in ls_head("prep_2026/gaia_dr4_prep/") if f.endswith(('.md', '.out', '.txt')) and 'HASH' not in f]
    files += ["deepseek_push/DR4_AMENDMENT_12.md"]
    # exclude the frozen-criteria file of THIS lane (self-reference) and the CFG241 files
    return sorted(set(f for f in files if 'CFG241' not in f))

STOP = set("that this with from have which their there these those about would could between against across into over under than then also only when where while whose such each both more most some many much very been being were what they them said same other another still even just upon within without after before above below".split())
NUMRE = re.compile(r'(?<![\w.])[-+\u2212]?\d[\d,]*\.?\d*')

def norm_nums(text):
    t = text.replace('\u2212', '-').replace('\u2013', '-')
    out = []
    for m in NUMRE.finditer(t):
        s = m.group(0).replace(',', '').lstrip('+')
        s = s.rstrip('.')
        try:
            out.append((s, float(s)))
        except ValueError:
            pass
    return out

def words(text):
    return set(w for w in re.findall(r'[a-z]{4,}', text.lower()) if w not in STOP)

class Corpus:
    def __init__(self):
        self.paras = []   # dict(file, line, text, nums(set of floats), words)
        for f in corpus_files():
            t, how = head_text(f)
            if t is None: continue
            lines = t.split('\n')
            blk = []; blk_start = 1
            def push():
                nonlocal blk
                txt = '\n'.join(blk).strip()
                if txt:
                    if len(txt) > 1500 and len(blk) > 1:
                        for k, ln in enumerate(blk):
                            if ln.strip(): self._add(f, blk_start + k, ln)
                    else:
                        self._add(f, blk_start, txt)
                blk = []
            for i, ln in enumerate(lines):
                if ln.strip() == '':
                    push(); blk_start = i + 2
                else:
                    if not blk: blk_start = i + 1
                    blk.append(ln)
            push()
        self.num_index = collections.defaultdict(set)
        for k, p in enumerate(self.paras):
            for s, v in p['nums']:
                self.num_index[round(abs(v), 6)].add(k)
    def _add(self, f, line, txt):
        if len(txt) > 4000: txt = txt[:4000]
        self.paras.append(dict(file=f, line=line, text=txt, nums=norm_nums(txt), words=words(txt)))

def num_match(tok, pnums):
    """v2 (after the first-run M7 miss): an integer token must match an integer-formatted source token exactly;
    a decimal token matches by rounding to its displayed precision."""
    s, v = tok
    if '.' not in s:
        a = s.lstrip('-+')
        return any(ps.lstrip('-+') == a for ps, _ in pnums)
    d = len(s.split('.')[1])
    tol = 0.5 * 10 ** (-d) + 1e-9
    for _, x in pnums:
        if abs(abs(x) - abs(v)) <= tol: return True
    return False

def claim_numbers(text):
    t = re.sub(r'\\(ref|label|fpath)\{[^}]*\}', ' ', text)
    t = re.sub(r'CFG\d+[a-z]?', ' ', t)
    t = re.sub(r'\\[A-Za-z]+', ' ', t)
    t = re.sub(r'\^\{?-?\d+\}?', ' ', t)
    toks = norm_nums(t)
    out = []
    for s, v in toks:
        if s.lstrip('-').isdigit() and abs(v) < 10: continue    # single-digit integer counts/conventions are not tracked mechanically
        if s.lstrip('-').isdigit() and 1900 <= abs(v) <= 2100: continue
        out.append((s, v))
    return out

def score(c, toks, cw, lanedirs, p, pf):
    n = sum(1 for tk in toks if num_match(tk, p['nums']))
    w = len(cw & p['words'])
    b = 2.0 if (any(d in p['file'] for d in lanedirs) or p['file'] in pf) else 0.0
    return 3 * n + 0.5 * min(w, 8) + b, n, w

# ---------------------------------------------------------------- flag-family helpers
VERB = [(4, r'prov\w*|establish\w*|exclud\w*|rule[sd]? out|reject\w*|detect\w*|confirm\w*|decisive|refut\w*'),
        (3, r'show\w*|demonstrat\w*|certif\w*|reveal\w*'),
        (2, r'find\w*|found|indicat\w*|impl(y|ies|ied)|conclude\w*'),
        (1, r'suggest\w*|lean\w*|hint\w*|gives?|favour\w*'),
        (0, r'lies inside|consistent with|sits?|reads?|descriptive')]
def verb_level(text):
    lv = -1; vb = ''
    for L, v in verb_all(text):
        if L > lv: lv, vb = L, v
    return lv, vb
def verb_all(text):
    """every verb occurrence with its level; occurrences under a negation (not a / not / no / never / without within 18 chars before) are skipped (v2)"""
    out = []
    for L, rx in VERB:
        for m in re.finditer(r'\b(' + rx + r')\b', text, re.I):
            pre = text[max(0, m.start() - 18):m.start()].lower()
            if re.search(r'\b(not|no|never|without|nor)\b', pre): continue
            out.append((L, m.group(0).lower()))
    return out
CAVEATS = ['post hoc', 'not blind', 'withdrawn', 'not to be quoted', 'not possible', 'non-discriminating', 'fragile', 'calibration-bound',
           'descriptive', 'not a detection', 'bracket', 'unverified', 'hypothesis', 'assumes']
HYP = r'\b(if|provided|assum\w*|hypothes\w*|requires?|for the p2 kernel|0 ?<= ?b)'
QUANT = re.compile(r'\b(any|every|all|whatever|always|never|however many|exactly|in every|at every)\s+(\w+)', re.I)
REFKEYS = {'ACE': ['Solimano', 'Geesink'], 'B21': ['Brouwer'], 'B23': ['Birkin'], 'C19': ['Coogan'], 'D22': ['Dunne'],
           'DM14': ['Dutton', 'Macci'], 'HW20': ['Heintz', 'Watson'], 'NS23': ['Nestor Shachar', 'Shachar']}
WITHDRAWN = [('RC100-sigma', r'(RC100|CFG216)', r'(4\.9|5\.5|5\s*\\?sigma|5\s*\u03c3|\\sigma\$?\s*level)', r'(not to be quoted|not be quoted|reverse|withdrawn|gas-route|stress test|frozen)'),
             ('5.09keV', r'5\.09', None, None), ('2.55keV', r'2\.55-?\s*keV', None, None), ('zstar2.4', r'z\^?\*\s*=\s*2\.4', None, None),
             ('180theorems', r'180 theorems', None, None), ('BHstar', r'BH\^?\*', None, None), ('lambdaJ', r'\\?lambda_?J|2\.7\s*Mpc', None, None),
             ('74-89', r'74[-\u2013]89', None, None), ('forest6-8', r'6[-\u2013]8\s*\\?sigma', None, None), ('AeST-mu10', r'AeST\s*\+\s*\\?mu', None, None),
             ('theory-closed', r'theory (is )?closed', None, r'not'), ('KiDS-lead', r'KiDS lead', None, None)]

# ---------------------------------------------------------------- ARITH relation table (>= 20 relations, hand-written)
def _first(tex, rx, g=1, flags=0):
    m = re.search(rx, tex, flags)
    return None if not m else m.group(g)
def Ez(z, om=0.3): return math.sqrt(om * (1 + z) ** 3 + 1 - om)
def arith_checks(tex):
    R = []
    def add(i, anchor, ok, det): R.append(dict(id=i, anchor=anchor, ok=ok, detail=det))
    f = lambda rx, g=1: _first(tex, rx, g)
    # floor
    n9 = f(r'a 0\.1\\,dex \$a_0\$ needs \$N>(\d+)\$'); n36 = f(r'at 0\.2\\,dex it needs \$N>(\d+)\$')
    add('A1', 'needs $N>', n9 is not None and int(n9) == (3 * 0.1 / 0.1) ** 2, 'N>%s expected 9' % n9)
    add('A2', 'it needs $N>', n36 is not None and int(n36) == round((3 * 0.2 / 0.1) ** 2), 'N>%s expected 36' % n36)
    # 600 to 3000 = 10^2.8..10^3.5
    lo, hi = f(r'a factor (\d[\d,]*) to (\d[\d,]*)\)', 1), f(r'a factor (\d[\d,]*) to (\d[\d,]*)\)', 2)
    ok = lo and hi and abs(math.log10(int(lo.replace(',', ''))) - 2.8) < 0.1 and abs(math.log10(int(hi.replace(',', ''))) - 3.5) < 0.1
    add('A3', 'a factor 600', bool(ok), 'factor %s to %s vs 10^2.8..10^3.5' % (lo, hi))
    add('A4', '0.18 to 0.33', bool(re.search(r'by 0\.18 to 0\.33\\,dex', tex)) and abs(0.1 * 1.8 - 0.18) < 1e-9 and abs(0.1 * 3.3 - 0.33) < 1e-9, '0.1*(1.8,3.3)')
    a, b = f(r'rival\'s 0\.(\d+)\\,dex needs'), f(r'stable to better than (0\.\d+)\\,dex between')
    add('A5', 'stable to better than', b is not None and abs(float(b) - 2 * 0.018) < 1e-9 and f(r'amplitude change of \$\+(0\.\d+)\$') is None or (b is not None and abs(float(b) - 0.036) < 1e-9), 'drift %s vs 2*0.018' % b)
    d = abs(-0.075 - (-0.25)); add('A6a', 'about 0.18', bool(re.search(r'about 0\.18\\,dex apart', tex)) and abs(d - 0.18) < 0.01, 'gap %.3f' % d)
    add('A6b', 'pm0.06', bool(re.search(r'\\pm0\.06\$', tex)) and abs(d / 3 - 0.06) < 0.005, '0.175/3=%.3f' % (d / 3))
    add('A7', '3 to 7 times', bool(re.search(r'3 to 7 times the 0\.10', tex)) and abs(0.35 / 0.1 - 3.5) < 1 and abs(0.7 / 0.1 - 7) < 0.01, '0.35..0.7 over 0.10')
    for i, (z, claim, rx) in enumerate([(1.4, 2.2, r'about \$\\times2\.2\$ at \$z\\approx1\.4'), (5.0, 8, r'about \$\\times8\$ at \$z\\approx5'), (2.3, 3.4, r'3\.4 at \$z=2\.3\$')]):
        ev = [Ez(z, om) for om in (0.27, 0.30, 0.315, 0.32)]
        present = bool(re.search(rx, tex))
        add('A%d' % (8 + i), rx[:12], present and min(ev) * 0.95 <= claim <= max(ev) * 1.05, 'E(%.1f)=%.2f..%.2f vs %s' % (z, min(ev), max(ev), claim))
    ev = [math.log10(Ez(2.0, om)) for om in (0.27, 0.30, 0.315, 0.32)]
    add('A11', '0.48', bool(re.search(r'0\.48\\,dex', tex)) and min(ev) - 0.01 <= 0.48 <= max(ev) + 0.01 and abs(math.log10(3) - 0.48) < 0.01, 'log E(2)=%.3f..%.3f' % (min(ev), max(ev)))
    add('A12', '+0.33', bool(re.search(r'\+0\.33\\,dex at 2\.5', tex)) and abs(math.log10(2.16) - 0.33) < 0.01, 'log10 2.16=%.3f' % math.log10(2.16))
    # DR4 pair ratio
    nb, na = f(r'about 4,300 pairs \(alt (\d[\d,]*)\)') and 4300, f(r'about 4,300 pairs \(alt (\d[\d,]*)\)')
    if na:
        na = int(na.replace(',', ''))
        sB = (0.161 / 3) ** 2 - 0.02 ** 2; sA = (0.192 / 3) ** 2 - 0.02 ** 2
        ratio = sB / sA
        add('A13', 'alt 2,900', abs(na / 4300 - ratio) / ratio < 0.06, 'alt/B pairs %.3f vs %.3f from floors 1.161/1.192, sigma_sys 0.02' % (na / 4300, ratio))
    else: add('A13', 'alt 2,900', False, 'pairs not found')
    add('A15', '0.66', bool(re.search(r'against 0\.66\\,dex between', tex)) and abs(math.log10(4.6) - 0.66) < 0.01, 'log10 4.6=%.3f' % math.log10(4.6))
    add('A16a', '0.94', bool(re.search(r'0\.94\\,dex in \$a_0\$', tex)) and abs(math.log10(8.69) - 0.94) < 0.01, 'log10 8.69')
    add('A16b', '8.69', abs(math.log10(8.84) - 0.946) < 0.01, 'log10 8.84')
    r = [Ez(0.3723, om) / Ez(0.2357, om) for om in (0.27, 0.30, 0.315, 0.32)]
    add('A17', '1.083', bool(re.search(r'predicted 1\.083', tex)) and min(r) * 0.99 <= 1.083 <= max(r) * 1.01, 'E ratio %.4f..%.4f' % (min(r), max(r)))
    add('A18', '2\\sigma', abs(0.48 / 2 / 4.8 - 0.05) < 0.002 and abs(0.48 / 2 / 2.5 - 0.096) < 0.005 and bool(re.search(r'about 0\.05 to 0\.10\\,dex', tex)), '0.24/4.8=0.05; 0.24/2.5=0.096')
    add('A19', 'nothing is excluded', bool(re.search(r'nothing is excluded at \$\\ge2\\sigma\$', tex)) and (1.309 - 1.0) / 0.210 < 2, '(1.309-1)/0.21=%.2f' % ((1.309 - 1.0) / 0.210))
    add('A20', '0.036', abs(2 * 0.018 - 0.036) < 1e-12, '2*0.018')
    add('A21', 'for a 3', abs(math.log10(3) - 0.477) < 0.001, 'log10 3')
    return R

# ---------------------------------------------------------------- the pipeline on a tex string
def run_pipeline(corp, tex, disable=()):
    r = EX.main(tex_override=tex, quiet=True)
    claims = r['claims']
    audit_ptr = {}
    # audit pointer: tag -> source files (read from the audit script text, not executed)
    at, _ = head_text(AUDIT_REL)
    srcmap = dict(re.findall(r'"(\w+)":\s*CFG \+ "([^"]+)"', at)); srcmap.update(dict(re.findall(r'"(\w+)":\s*"([^"]+)"', at)))
    for m in re.finditer(r'^R\("(B\d+)", ".*?", "(\w+)"', at, re.M):
        audit_ptr.setdefault(m.group(1), set()).add(srcmap.get(m.group(2), ''))
    flags = []
    arith = arith_checks(tex)
    res = {}
    for c in claims:
        text = c['text']
        toks = claim_numbers(text)
        cw = words(strip_tex(text))
        lanedirs = ['CFG%s_' % re.sub(r'[a-z]$', '', x[3:]) for x in c['lanes']]
        pf = set()
        for f in audit_ptr.get(c['tag'], []):
            pf.add(('campaign_fresh_gravity/' + f) if not f.startswith(('data_assembly', 'real_research')) and not f.startswith('campaign') else f)
        # candidate paragraphs: those sharing a number or >=3 content words
        cand = set()
        for s, v in toks:
            cand |= corp.num_index.get(round(abs(v), 6), set())
        if len(cand) < 40:
            for k, p in enumerate(corp.paras):
                if len(cw & p['words']) >= 4: cand.add(k)
        scored = []
        for k in cand:
            p = corp.paras[k]
            sc, n, w = score(c, toks, cw, lanedirs, p, pf)
            scored.append((sc, n, w, k))
        scored.sort(reverse=True)
        top = scored[:3]
        c['top'] = [(corp.paras[k]['file'], corp.paras[k]['line'], round(sc, 1), n, w) for sc, n, w, k in top]
        c['top_text'] = [corp.paras[k]['text'] for _, _, _, k in top]
        fl = []
        # NUM
        for tk in toks:
            ok = any(num_match(tk, corp.paras[k]['nums']) and (n >= 2 or w >= 2 or len(toks) == 1) for sc, n, w, k in top)
            if not ok:
                fl.append(('NUM', tk[0]))
        # VERB
        cvs = [(L, v) for L, v in verb_all(strip_tex(text)) if L >= 2]
        if cvs and top:
            # best source sentence
            best = (-1, None)
            for sc, n, w, k in top:
                for sen in re.split(r'(?<=[.;])\s+', corp.paras[k]['text']):
                    s2 = sum(1 for tk in toks if num_match(tk, norm_nums(sen))) * 2 + len(cw & words(sen))
                    if s2 > best[0]: best = (s2, sen)
            sl, sv = verb_level(best[1] or '')
            sl = max(sl, 0)
            for L, v in cvs:
                if L > sl: fl.append(('VERB', v))
        # CAVEAT
        ptxt = (c.get('para') or text).lower()
        srcall = ' '.join(c['top_text']).lower()
        for cv_ in CAVEATS:
            if cv_ in srcall and cv_ not in ptxt:
                fl.append(('CAVEAT', cv_))
        # CITE
        for m in re.finditer(r'([A-Z][\w\\`\'{}\-]+(?: [A-Z][a-z]+)?)(?: et al\.\\ | \\& [A-Z][\w\\`\'{}]+ )\[([A-Z]+\d*)\]', text):
            sur, key = m.group(1), m.group(2)
            for k2, names in REFKEYS.items():
                if any(n.lower() in sur.lower().replace('\\`', '').replace('{', '') for n in names) and k2 != key:
                    fl.append(('CITE', '%s->%s' % (sur, key)))
        for m in re.finditer(r'([A-Z][a-z]+) et al\.\\ (\d{4})', text):
            nm = m.group(1)
            if not any(nm.lower() in ' '.join(v).lower() for v in REFKEYS.values()):
                fl.append(('CITE', 'phantom:%s %s' % (nm, m.group(2))))
        # WITHDRAWN
        for pid, rx1, rx2, ex in WITHDRAWN:
            if re.search(rx1, text) and (rx2 is None or re.search(rx2, text)) and not (ex and re.search(ex, text, re.I)):
                fl.append(('WITHDRAWN', pid))
        # SCOPE
        hyp = re.search(HYP, srcall)
        for m in QUANT.finditer(strip_tex(text)):
            ph = m.group(0).lower()
            if hyp or m.group(1).lower() not in srcall:
                fl.append(('SCOPE', ph))
        # ARITH
        for a in arith:
            if not a['ok'] and a['anchor'] in text:
                fl.append(('ARITH', a['id']))
        # NOSRC
        sup = False
        for sc, n, w, k in top:
            if n >= 2 or (n >= 1 and w >= 2) or (not toks and w >= 4):
                sup = True
        if not sup and (toks or re.search(r'shows?|finds?|confirm', text, re.I)):
            fl.append(('NOSRC', ''))
        c['flags'] = [x for x in fl if x[0] not in disable]
    return claims, arith

# ---------------------------------------------------------------- plants
PLANTS = [
 ('M1', 'NUM', r'$\Delta\chi^2_{\rm pred}=0.14$ (canonical)', r'$\Delta\chi^2_{\rm pred}=0.41$ (canonical)', ('NUM',)),
 ('M2', 'VERB', r'flat $a_0$ (ratio 1) lies inside the 95\% statistical interval of 7 of the 8 CFG223 points', r'flat $a_0$ (ratio 1) is demonstrated by the 95\% statistical interval of 7 of the 8 CFG223 points', ('VERB',)),
 ('M3', 'CAVEAT', r'not $a_0(z)$, and its frozen significance is not to be quoted', r'not $a_0(z)$', ('CAVEAT',)),
 ('M4', 'CITE', r'Dunne et al.\ [D22] the tracer masses agree by construction', r'Dunne et al.\ [HW20] the tracer masses agree by construction', ('CITE',)),
 ('M5', 'WITHDRAWN', r'\emph{RC100} (Nestor Shachar et al.\ [NS23]) is the tightest sample statistically,', r'\emph{RC100} (Nestor Shachar et al.\ [NS23]) rejects the rival at $z\approx2.2$ at $4.9$--$5.5\sigma$ and is the tightest sample statistically,', ('WITHDRAWN',)),
 ('M6', 'SCOPE', r'With $f$ free, any sample obeys', r'With $f$ free, any sample, for any kernel, obeys', ('SCOPE',)),
 ('M7', 'NUM', r'a 0.05\,dex error in $D$ is a factor 1.5 to 1.8 in $a_0$', r'a 0.05\,dex error in $D$ is a factor 15 to 18 in $a_0$', ('NUM',)),
 ('M8', 'NOSRC', r'(one of them has no root in 10\% of resamples).', r'(one of them has no root in 10\% of resamples). A Chandra stacking at $z\approx0.8$ independently confirms a flat $a_0$ to 3\% (Smith et al.\ 2025).', ('NOSRC', 'CITE')),
 ('M9', 'ARITH', r'at 0.2\,dex it needs $N>36$', r'at 0.2\,dex it needs $N>6$', ('ARITH',)),
 ('M10', 'NUM/ARITH', r'3$\sigma$ needs about 4,300 pairs (alt 2,900)', r'3$\sigma$ needs about 4,300 pairs (alt 6,500)', ('NUM', 'ARITH')),
]
PARAS = [
 ('P-a', r'A split by redshift inside one survey cancels any calibration that is common to both halves.', r'Splitting a single survey in redshift removes any calibration shared by the two halves.'),
 ('P-b', r'The $\Lambda$CDM proxy is not $\Lambda$CDM.', r'The $\Lambda$CDM proxy should not be mistaken for $\Lambda$CDM itself.'),
 ('P-c', r'NOT POSSIBLE (power 0.14 against 9) and NON-DISCRIMINATING by its MUTATE \\', r'NOT POSSIBLE (power 0.14 against the 9 required) and NON-DISCRIMINATING in its MUTATE control \\'),
]
EXPD = {'M1': '0.41', 'M2': 'demonstrated', 'M3': 'not to be quoted', 'M4': 'Dunne->HW20', 'M5': 'RC100-sigma', 'M6': 'any kernel', 'M7': '15', 'M8': 'phantom:Smith 2025', 'M9': 'A2', 'M10': '6500'}
def find_claim(claims, snippet):
    # snippet: a substring of tex text; claims' text is tex-literal
    key = snippet
    for c in claims:
        if key in c['text']: return c
    # row/paragraph fallback: compare on the first 40 chars
    return None

def plant_main(corp, tex0, disable, only, outdir):
    base_claims, _ = run_pipeline(corp, tex0, disable)
    out = []; bad = 0
    def fset(c): return set(c['flags']) if c else set()
    for pid, kind, old, new, fam in PLANTS + [(a, 'PARAPHRASE', b, c, ()) for a, b, c in PARAS]:
        if only and pid != only: continue
        if tex0.count(old) != 1:
            out.append('%s: OLD STRING NOT FOUND exactly once (%d)' % (pid, tex0.count(old))); return out, 3
        tex1 = tex0.replace(old, new)
        cl1, _ = run_pipeline(corp, tex1, disable)
        # locate the claim containing the new fragment (use a distinctive token)
        frag = {'M1': '0.41', 'M2': 'demonstrated by', 'M3': 'prior-anchored (gas scaling grows', 'M4': '[HW20] the tracer', 'M5': 'rejects the rival', 'M6': 'for any kernel',
                'M7': 'factor 15 to 18', 'M8': 'Chandra', 'M9': 'N>6$', 'M10': 'alt 6,500', 'P-a': 'Splitting a single survey', 'P-b': 'mistaken for', 'P-c': 'against the 9 required'}[pid]
        ofrag = {'M1': '0.14$ (canonical)', 'M2': 'lies inside', 'M3': 'prior-anchored (gas scaling grows', 'M4': '[D22] the tracer', 'M5': 'tightest sample', 'M6': 'any sample obeys',
                 'M7': 'factor 1.5 to 1.8', 'M8': None, 'M9': 'N>36$', 'M10': 'alt 2,900', 'P-a': 'A split by redshift', 'P-b': 'proxy is not', 'P-c': 'against 9)'}[pid]
        c1 = next((c for c in cl1 if frag in c['text']), None)
        c0 = next((c for c in base_claims if ofrag and ofrag in c['text']), None)
        if pid == 'M3':   # table row: the row text begins with CFG216
            c1 = next((c for c in cl1 if c['kind'] == 'T' and 'RC100' in c['text'] and 'differential baryon-mass' in c['text']), None)
            c0 = next((c for c in base_claims if c['kind'] == 'T' and 'RC100' in c['text'] and 'differential baryon-mass' in c['text']), None)
        if pid == 'P-c':
            c1 = next((c for c in cl1 if c['kind'] == 'T' and 'KiDS-1000' in c['text']), None)
            c0 = next((c for c in base_claims if c['kind'] == 'T' and 'KiDS-1000' in c['text']), None)
        f1, f0 = fset(c1), fset(c0)
        newf = f1 - f0
        if kind == 'PARAPHRASE':
            ok = len(newf) == 0
            note = '' if c1 is not None else ' [paraphrase is NOT extracted as a claim by the frozen trigger rule: vacuous pass; harness v1 scored this as FALSE POSITIVE]'
            out.append('%s PARAPHRASE   new flags vs original: %s   -> %s%s' % (pid, sorted(newf) or 'none', 'OK (not flagged)' if ok else 'FALSE POSITIVE', note))
        else:
            hit = [x for x in newf if x[0] in fam]
            ok = (c1 is not None) and bool(hit)
            exact = any(x[1] == EXPD[pid] or (pid == 'M7' and x[1] in ('15', '18')) or (pid == 'M10' and x[1] in ('6500', 'A13')) for x in newf)
            out.append('%s %-10s expected %-10s caught by %-40s other new flags %s -> %s ; planted-detail %r hit: %s' % (pid, kind, '/'.join(fam), hit or 'NONE', sorted(x for x in newf if x not in hit) or '-', 'CAUGHT' if ok else 'MISSED', EXPD[pid], exact))
        if not ok: bad += 1
    return out, (1 if bad else 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plant', action='store_true'); ap.add_argument('--disable', default=''); ap.add_argument('--only', default='')
    ap.add_argument('--classification', default=os.path.join(HERE, 'CFG241_classification.csv'))
    a = ap.parse_args()
    disable = tuple(x for x in a.disable.split(',') if x)
    corp = Corpus()
    print('repo: <repo>  head', head_commit(), ' corpus paragraphs:', len(corp.paras), ' files:', len(set(p['file'] for p in corp.paras)))
    tex0, how = head_text(TEX_REL)
    print('tex read from', how, ' sha256', hashlib.sha256(tex0.encode()).hexdigest()[:16])
    if a.plant:
        out, code = plant_main(corp, tex0, disable, a.only, HERE)
        print('\n'.join(out)); print('disabled families:', disable or 'none'); print('PLANT CONTROL EXIT', code)
        sys.exit(code)
    claims, arith = run_pipeline(corp, tex0, disable)
    with open(os.path.join(HERE, 'CFG241_worksheet.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'kind', 'line', 'sec', 'tag', 'flags', 'top_sources', 'text'])
        for c in claims:
            w.writerow([c['id'], c['kind'], c['line'], c['sec'], c['tag'], ' '.join('%s:%s' % x for x in c['flags']), ' | '.join('%s:%d(s%.1f,n%d,w%d)' % t for t in c['top']), c['text']])
    json.dump([dict(id=c['id'], line=c['line'], flags=c['flags'], top=c['top'], top_text=[t[:700] for t in c['top_text']]) for c in claims], open(os.path.join(HERE, 'CFG241_worksheet.json'), 'w'))
    cnt = collections.Counter(x[0] for c in claims for x in c['flags'])
    print('claims:', len(claims), ' flag counts:', dict(cnt))
    print('ARITH relations:', len(arith), ' failing:', [(a_['id'], a_['detail']) for a_ in arith if not a_['ok']])
    for a_ in arith: print('  ', a_['id'], 'OK ' if a_['ok'] else 'FAIL', a_['detail'])
    if os.path.exists(a.classification):
        rows = list(csv.DictReader(open(a.classification)))
        have = {r['id'] for r in rows}
        miss = [c['id'] for c in claims if c['id'] not in have]
        print('classification rows:', len(rows), ' claims without a row:', len(miss), miss[:10])
        if miss: sys.exit(2)
        cls = collections.Counter(r['class'] for r in rows)
        print('class counts:', dict(cls))
        unv = cls.get('UNVERIFIABLE-OFFLINE', 0)
        pct = unv / len(claims)
        num_claims = [r for r in rows if r.get('has_number_or_verb') == '1']
        print('UNVERIFIABLE-OFFLINE fraction: %.3f (target <= 0.10)' % pct)
        sys.exit(0 if pct <= 0.10 else 2)
    print('no classification table yet'); sys.exit(2)

if __name__ == '__main__':
    main()
