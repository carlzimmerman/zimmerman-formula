#!/usr/bin/env python3
"""CFG265 common helpers: repo discovery (ZF_REPO or walk up from __file__), reads at the PINNED commit 53f374ae2
(the PAPER39 draft's commit; frozen criteria section 3/3b), tex extraction (section 3 rule).
No absolute home path is ever printed: every path is shown relative to <repo>."""
import os, re, sys, subprocess, hashlib

PIN = "53f374ae2"
TEX_REL = "qwen_claude_field_theory/papers_2026/PAPER39_closure_map_2026.tex"
AUDIT_REL = "qwen_claude_field_theory/papers_2026/PAPER39_audit.py"
TEX_SHA = "cfafe712560b95fb735c36c1bce6907d47d572ea6099f3e0ba1202444b5db58e"


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, ".git")):
        return os.path.abspath(r)
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(d, ".git")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    sys.exit("CFG265: repo root not found (set ZF_REPO)")


REPO = find_repo()
HERE = os.path.dirname(os.path.abspath(__file__))


def scrub(s):
    return s.replace(REPO, "<repo>").replace(HERE, "<lane>").replace(os.path.expanduser("~"), "~")


def pin_text(rel, rev=PIN):
    """file as committed at the pinned commit; falls back to the working tree (untracked) and says so."""
    r = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (rev, rel)], capture_output=True)
    if r.returncode == 0:
        return r.stdout.decode("utf-8", "replace"), rev
    p = os.path.join(REPO, rel)
    if os.path.isfile(p):
        return open(p, encoding="utf-8", errors="replace").read(), "WORKTREE"
    return None, "MISSING"


def ls_pin(prefix, rev=PIN):
    r = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", rev, prefix], capture_output=True)
    return [x for x in r.stdout.decode().split("\n") if x]


def ls_pin_sizes(prefix, rev=PIN):
    r = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "-l", rev, prefix], capture_output=True)
    out = {}
    for ln in r.stdout.decode().split("\n"):
        if not ln.strip():
            continue
        meta, path = ln.split("\t", 1)
        parts = meta.split()
        try:
            out[path] = int(parts[3])
        except (ValueError, IndexError):
            out[path] = 0
    return out


def head_commit():
    return subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()


D = "\u2024"
PROT = ['et al.\\ ', 'i.e.\\ ', 'e.g.\\ ', 'vs.\\ ', 'Eq.~', 'Table~', 'Section~']
TRIG = re.compile(r'\b(shows?|implies|proves?|theorems?|finds?|found|certif\w*|predicts?|exclud\w*|disfavour\w*|consistent|cannot|must|needs?|never|every|only|decisive|strongest|tightest|largest|not|no|none|ill-conditioned|walled|decides?|determine\w*|separate\w*|lean|is|are|fail\w*|no-go|kills?|forc\w*|prefer\w*|reproduc\w*|gives?|requires?|at most|postulat\w*)\b', re.I)
ALLSEC = ('abstract', 'What would decide the rest', 'Limitations')


def split_sentences(t):
    tt = t
    for p in PROT:
        tt = tt.replace(p, p.replace('.', D))
    tt = re.sub(r'(\d)\.(\d)', lambda m: m.group(1) + D + m.group(2), tt)
    out = []
    for p in re.split(r'(?<=[.?!])\s+(?=[A-Z`\\$(]|``)', tt):
        if p.strip():
            out.append(p.replace(D, '.').strip())
    return out


def strip_tex(s):
    return re.sub(r'\\(ref|label|cite|fpath)\{[^}]*\}', '', s)


def extract(tex):
    """frozen section-3 rule. returns dict(units, sents, rows, header, src, start, refs)."""
    src = tex.split('\n')
    start = [i for i, l in enumerate(src) if '\\begin{abstract}' in l][0]
    refs = [i for i, l in enumerate(src) if 'section*{References}' in l][0]
    units = []
    st = dict(sec='front', cur=[], intab=False)

    def flush():
        t = ' '.join(x for _, x in st['cur']).strip()
        if t:
            units.append(dict(line=st['cur'][0][0], sec=st['sec'], text=t, tab=st['intab']))
        st['cur'] = []
    for i in range(start, refs):
        l = src[i]
        if l.startswith('%'):
            continue
        m = re.match(r'\\section\{(.*?)\}', l)
        if m:
            flush(); st['sec'] = m.group(1); continue
        if 'begin{abstract}' in l:
            st['sec'] = 'abstract'; continue
        if '\\begin{longtable}' in l or '\\begin{tabular}' in l:
            flush(); st['intab'] = True; continue
        if '\\end{longtable}' in l or '\\end{tabular}' in l:
            flush(); st['intab'] = False; continue
        if st['intab']:
            flush()
            if l.rstrip().endswith('\\\\') and not any(k in l for k in ['\\toprule', '\\midrule', '\\bottomrule']):
                st['cur'].append((i + 1, l)); flush()
            continue
        if l.strip() == '' or l.strip() in ('{\\small', '}') or any(k in l for k in ['\\begin{', '\\end{', '\\toprule', '\\midrule', '\\bottomrule', '\\setlength', '\\endhead']):
            flush(); continue
        if l.startswith('\\item'):
            flush()
        st['cur'].append((i + 1, l))
    flush()
    sents, rows, header = [], [], []
    for u in units:
        if u['tab']:
            txt = u['text'].rstrip()
            if txt.endswith('\\\\'):
                txt = txt[:-2].strip()
            r = dict(line=u['line'], sec=u['sec'], text=txt, tab=True, para=txt)
            (header if txt.startswith('route &') else rows).append(r)
        else:
            for p in split_sentences(u['text']):
                sents.append(dict(line=u['line'], sec=u['sec'], text=p, tab=False, para=u['text']))
    return dict(units=units, sents=sents, rows=rows, header=header, src=src, start=start, refs=refs)


def is_claim(s):
    return bool(re.search(r'\d', strip_tex(s['text']))) or bool(TRIG.search(s['text'])) or s['sec'].startswith(ALLSEC)


def references(tex):
    """the 12 bibliographic entries: key -> text"""
    out = {}
    for m in re.finditer(r'^\[([A-Z]+\d*)\] (.*?)\\par$', tex, re.M):
        out[m.group(1)] = m.group(2)
    return out


def sha(tex):
    return hashlib.sha256(tex.encode()).hexdigest()
