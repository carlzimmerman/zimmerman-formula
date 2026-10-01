#!/usr/bin/env python3
"""CFG241 common helpers: repo discovery (ZF_REPO or walk up from __file__), git-HEAD reads, tex extraction.
No absolute home path is ever printed: every path is shown relative to <repo>."""
import os, re, sys, subprocess, hashlib

def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, ".git")):
        return os.path.abspath(r)
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(d, ".git")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    sys.exit("CFG241: repo root not found (set ZF_REPO)")

REPO = find_repo()
HERE = os.path.dirname(os.path.abspath(__file__))
TEX_REL = "qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.tex"
AUDIT_REL = "qwen_claude_field_theory/papers_2026/PAPER38_audit.py"

def scrub(s):
    return s.replace(REPO, "<repo>").replace(HERE, "<lane>").replace(os.path.expanduser("~"), "~")

def head_text(rel):
    """file as committed at HEAD; falls back to working tree (untracked) and says so via the second return value."""
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel], capture_output=True)
    if r.returncode == 0:
        return r.stdout.decode("utf-8", "replace"), "HEAD"
    p = os.path.join(REPO, rel)
    if os.path.isfile(p):
        return open(p, encoding="utf-8", errors="replace").read(), "WORKTREE"
    return None, "MISSING"

def ls_head(prefix):
    r = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", "HEAD", prefix], capture_output=True)
    return [x for x in r.stdout.decode().split("\n") if x]

def head_commit():
    return subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()

D = "\u2024"
PROT = ['et al.\\ ', 'i.e.\\ ', 'e.g.\\ ', 'Eq.~', 'Table~', 'vs.\\ ', 'Sect.~']
TRIG = re.compile(r'\b(shows?|implies|proves?|theorems?|finds?|found|certif\w*|predicts?|exclud\w*|disfavour\w*|consistent|cannot|must|needs?|never|every|only|decisive|strongest|tightest|largest|not|no|none|ill-conditioned|walled|decides?|determine\w*|separate\w*|lean|is|are)\b', re.I)
ALLSEC = ('abstract', 'The differential route' , 'What would decide it', 'Limitations and what is not claimed')

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
    s = re.sub(r'\\(ref|label)\{[^}]*\}', '', s)
    return s

def extract(tex):
    """returns (units, sentences, rowclaims, secs). Legacy mode reproduces the frozen throwaway enumerator exactly."""
    src = tex.split('\n')
    start = [i for i, l in enumerate(src) if '\\begin{abstract}' in l][0]
    refs = [i for i, l in enumerate(src) if 'section*{References}' in l][0]
    units = []; sec = 'front'; cur = []; cur_start = [None]; intab = False
    rows = []
    def flush():
        nonlocal cur
        t = ' '.join(x for _, x in cur).strip()
        if t:
            units.append(dict(line=cur[0][0], sec=sec, text=t, tab=intab))
        cur = []
    pending_tag = None
    for i in range(start, refs):
        l = src[i]
        if l.startswith('%'):
            continue
        m = re.match(r'\\section\{(.*?)\}', l)
        if m:
            flush(); sec = m.group(1); continue
        if 'begin{abstract}' in l:
            sec = 'abstract'; continue
        if '\\begin{tabular}' in l:
            flush(); intab = True; continue
        if '\\end{tabular}' in l:
            flush(); intab = False; continue
        if l.strip() == '' or any(k in l for k in ['\\begin{', '\\end{', '\\toprule', '\\midrule', '\\bottomrule', '\\setlength']):
            flush(); continue
        if l.startswith('\\item'):
            flush()
        cur.append((i + 1, l))
    flush()
    # sentences (legacy): units incl. tables collapsed
    sents = []
    for u in units:
        for p in split_sentences(u['text']):
            sents.append(dict(line=u['line'], sec=u['sec'], text=p, tab=u['tab'], para=u['text']))
    # row claims: split table units at the row terminator '\\\\'
    rowclaims = []
    for u in units:
        if u['tab']:
            # each source line of the unit is one row; recover by re-reading lines
            pass
    # rebuild rows from the source lines directly
    intab = False; sec2 = 'front'; hdr_seen = False
    for i in range(start, refs):
        l = src[i]
        if l.startswith('%'): continue
        m = re.match(r'\\section\{(.*?)\}', l)
        if m: sec2 = m.group(1)
        if '\\begin{tabular}' in l: intab = True; hdr_seen = False; continue
        if '\\end{tabular}' in l: intab = False; continue
        if intab and l.rstrip().endswith('\\\\') and not any(k in l for k in ['\\toprule', '\\midrule', '\\bottomrule']):
            if not hdr_seen:
                hdr_seen = True; continue    # header row
            rowclaims.append(dict(line=i + 1, sec=sec2, text=l.rstrip()[:-2].strip(), tab=True, para=l.rstrip()[:-2].strip()))
    return units, sents, rowclaims, src, start, refs

def is_claim(s):
    return bool(re.search(r'\d', strip_tex(s['text']))) or bool(TRIG.search(s['text'])) or any(s['sec'].startswith(k) for k in ('abstract', 'What would decide it', 'Limitations'))
