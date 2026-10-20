#!/usr/bin/env python3
"""CFG908 file list: every tracked file that still states kappa is derived (FROZEN_CRITERIA section 6).

Two steps, run from the repo root:
  nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.py extract
      git grep (single thread) at the pinned criteria commit over tracked text files; writes
      cfg908_filelist_candidates.csv (pre-filtered review candidates, with +/-2 lines of context) and
      cfg908_missrate_sample.csv (seed 908, 40 lines of S1 u S2 that the pre-filter did not select).
  python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_filelist.py merge > .../cfg908_filelist.out
      reads the hand classes in cfg908_manual_review.csv and cfg908_missrate_review.csv and writes cfg908_filelist_A.csv.

  nice -n 10 python3 .../cfg908_filelist.py supplement
      POST-FREEZE, DISCLOSED (README): the frozen S1 regex uses [^|], so a markdown table row with kappa and DERIVED in
      different cells is never seen (found because glm53 STATE.md:35, a claim line verified by cfg908_audit K6, is
      missing from the frozen list). This mode rescans kappa/derive co-occurrence across '|' (within 120 characters),
      keeps lines the frozen S1 did not return, applies the same ASSERT (with '.' for '[^|]') and negation filter, and
      writes cfg908_supplement_candidates.csv. Hand classes go in cfg908_supplement_review.csv. The frozen list is not
      changed; merge reports the supplement separately.

Read only: no listed file is edited. Searches are tracked-file only (git grep at a commit); _external_data excluded.
Matching notes: single words of the negation list are matched as whole words, stems (retract, tautolog, underiv,
non-deriv) as prefixes; everything is case-insensitive.
"""
import csv
import os
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PIN = "122af8ada"
PATHSPEC = ["*.md", "*.py", "*.tex", "*.txt", "*.lean", "*.out", "*.json", ":!:_external_data/*"]
CAND = os.path.join(HERE, "cfg908_filelist_candidates.csv")
MISS = os.path.join(HERE, "cfg908_missrate_sample.csv")
MANUAL = os.path.join(HERE, "cfg908_manual_review.csv")
MISSREV = os.path.join(HERE, "cfg908_missrate_review.csv")
OUT_A = os.path.join(HERE, "cfg908_filelist_A.csv")
MAXLEN = 600

K = r"(kappa|κ|\\kappa)"
S1_RE = r"(kappa|κ|\\kappa)[^|]{0,60}deriv|deriv[^|]{0,60}(kappa|κ|\\kappa)"
S2_ANCHORS = ["a0^2", "a0**2", "a_0^2", "a₀²", "a_{0}^2", "s/2", "s / 2", "32 pi", "32pi", "32π", "32\\pi", "32*pi",
              "32*np.pi", "32*math.pi", "32*sp.pi"]
ASSERT = re.compile(K + r"[^|]{0,50}?\b(derived|derivable|derives)\b|\b(derive|derives|derived|derivation of)\s+"
                    r"(the\s+)?(coefficient\s+)?" + K, re.I)
TIE = re.compile(
    r"4\s*\*?\s*a_?\{?0\}?\s*(\^|\*\*)\s*2\s*/\s*\(?\s*G\s*\*?\s*c\s*(\^|\*\*)\s*2"
    r"|4\s*a₀²\s*/\s*\(?\s*G\s*c²"
    r"|\\frac\{4\s*a_\{?0\}?\^2\}\{G\s*c\^2\}"
    r"|(rho|ρ)_?\{?(L|Lambda|Λ|DE|\\Lambda)\}?\s*(\*?\s*c\s*(\^|\*\*)?\s*2|c²)?\s*=\s*4\s*\*?\s*a"
    r"|G\s*\*?\s*(rho|ρ)_?\{?(L|Lambda|Λ|DE|\\Lambda)\}?\s*=\s*4\s*\*?\s*a"
    r"|32\s*\*?\s*(pi|π|\\pi|np\.pi|math\.pi|sp\.pi)\s*\*?\s*a_?\{?0\}?\s*(\^|\*\*)\s*2\s*/\s*\(?\s*c"
    r"|32\s*π\s*a₀²\s*/\s*c⁴"
    r"|a_?\{?0\}?\s*=\s*s(_\{?\\?(text\{)?DE\}?\}?|_de|_DE|_\{DE\})?\s*/\s*2"
    r"|a₀\s*=\s*s(_DE)?\s*/\s*2"
    r"|c\s*\*?\s*(sqrt|√)\s*\(?\s*G\s*\*?\s*(rho|ρ)[^)]{0,14}\)?\s*/\s*2"
    r"|\(1/2\)\s*\*?\s*c\s*\*?\s*(sqrt|√)"
    r"|½\s*c\s*√"
    r"|32\s*(pi|π|\\pi)[^|]{0,40}(deriv|explain)|(deriv|explain)[^|]{0,40}32\s*(pi|π|\\pi)", re.I)
CLAIMW = re.compile(r"deriv|theorem|certif|closes|closure|forced|first[- ]principles|zero free|no free|not a fit|"
                    r"parameter-free|one constant|one number|not fitted", re.I)
BOOST = re.compile(r"not fitted|no longer fitted|not a fit|not measured", re.I)
NEG = re.compile(r"not[ -](derived|derivable|a derivation)|underiv|non-?deriv|\bnever\b[^|]{0,30}deriv|"
                 r"\bno[ -]derivation|\bcannot\b[^|]{0,30}deriv|n't\b|\bfitted\b|\bvoid\b|\bwithdrawn\b|retract|"
                 r"do not cite|never cite|\bcircular\b|tautolog|\bnaming\b|\bunmet\b|\bobligation\b|no-go|\bnothing\b|"
                 r"\bneither\b|\bnor\b|\bnot\b|must not|non_claims|not_derived|\badopted\b|\bquarantine\b|"
                 r"\bimpossible\b", re.I)


def git_grep(args, keep=None):
    """Stream git grep output; store only lines of at most 20000 characters that pass keep()."""
    cmd = ["git", "-C", REPO, "grep", "--threads=1", "-I", "-n"] + args + [PIN, "--"] + PATHSPEC
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rows, nseen = [], 0
    pre = (PIN + ":").encode()
    for raw in proc.stdout:
        nseen += 1
        if not raw.startswith(pre) or len(raw) > 20000:
            continue
        rest = raw[len(pre):].decode("utf-8", errors="replace").rstrip("\n")
        m = re.match(r"(.+?):(\d+):(.*)$", rest)
        if m and (keep is None or keep(m.group(3))):
            rows.append((m.group(1), int(m.group(2)), m.group(3)))
    err = proc.stderr.read()
    if proc.wait() not in (0, 1):
        sys.exit("git grep failed: %s" % err[:500])
    return rows, nseen


NAME_RE = [(re.compile(r"\bCarl\b"), "[owner]"), (re.compile(r"zimmerman", re.I), "[Z.]")]


def redact(text):
    """No personal names in committed files: quoted text and context are redacted (paths are kept as identifiers)."""
    for rx, rep in NAME_RE:
        text = rx.sub(rep, text)
    return text


def negated(text):
    return bool(NEG.search(BOOST.sub(" ", text)))


def fetch_contexts(keys):
    """+/-2 lines for each (path, line), one git cat-file --batch process."""
    paths = sorted({p for p, _ in keys})
    proc = subprocess.Popen(["git", "-C", REPO, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    data, _ = proc.communicate(("".join("%s:%s\n" % (PIN, p) for p in paths)).encode())
    blobs, i = {}, 0
    for p in paths:
        j = data.index(b"\n", i)
        hdr = data[i:j].decode().split()
        size = int(hdr[2])
        blobs[p] = data[j + 1:j + 1 + size].decode("utf-8", errors="replace").splitlines()
        i = j + 1 + size + 1
    ctx = {}
    for p, n in keys:
        lines = blobs[p]
        lo, hi = max(1, n - 2), min(len(lines), n + 2)
        ctx[(p, n)] = " ⏎ ".join("%d| %s" % (q, lines[q - 1].strip()[:300]) for q in range(lo, hi + 1))
    return ctx


def extract():
    s1, _ = git_grep(["-i", "-E", S1_RE])
    s2, n2raw = git_grep(sum([["-e", a] for a in S2_ANCHORS], ["-F"]), keep=lambda t: bool(TIE.search(t)))
    cand = {}
    for p, n, t in s1:
        if ASSERT.search(t) and not negated(t):
            cand.setdefault((p, n), ["S1", t])
    for p, n, t in s2:
        if CLAIMW.search(t) and not negated(t):
            if (p, n) in cand:
                cand[(p, n)][0] = "S1+S2"
            else:
                cand[(p, n)] = ["S2", t]
    union = {}
    for p, n, t in s1 + s2:
        union[(p, n)] = t
    nonsel = sorted(k for k in union if k not in cand)
    rng = random.Random(908)
    sample = rng.sample(nonsel, min(40, len(nonsel)))
    keys = sorted(cand) + sorted(sample)
    ctx = fetch_contexts(keys)
    with open(CAND, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["cid", "src", "path", "line", "text", "context"])
        for i, key in enumerate(sorted(cand), 1):
            w.writerow(["c%04d" % i, cand[key][0], key[0], key[1], redact(cand[key][1].strip()[:MAXLEN]), redact(ctx[key])])
    with open(MISS, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["mid", "path", "line", "text", "context"])
        for i, key in enumerate(sorted(sample), 1):
            w.writerow(["m%02d" % i, key[0], key[1], redact(union[key].strip()[:MAXLEN]), redact(ctx[key])])
    print("pinned tree %s" % PIN)
    print("S1 lines (kappa + derive): %d" % len(s1))
    print("S2 anchor lines: %d ; with a tie form (lines <= 20000 chars): %d" % (n2raw, len(s2)))
    print("S1 u S2 lines: %d ; review candidates after the pre-filter: %d (files %d)" %
          (len(union), len(cand), len({p for p, _ in cand})))
    print("miss-rate sample: %d of %d non-selected lines (seed 908)" % (len(sample), len(nonsel)))


SUPP = os.path.join(HERE, "cfg908_supplement_candidates.csv")
SUPPREV = os.path.join(HERE, "cfg908_supplement_review.csv")
S1X_RE = r"(kappa|κ|\\kappa).{0,120}deriv|deriv.{0,120}(kappa|κ|\\kappa)"
ASSERTX = re.compile(K + r".{0,50}?\b(derived|derivable|derives)\b|\b(derive|derives|derived|derivation of)\s+"
                     r"(the\s+)?(coefficient\s+)?" + K, re.I)


def supplement():
    s1, _ = git_grep(["-i", "-E", S1_RE])
    seen = {(p, n) for p, n, _ in s1}
    s1x, _ = git_grep(["-i", "-E", S1X_RE])
    extra = [(p, n, t) for p, n, t in s1x if (p, n) not in seen]
    cand = sorted({(p, n): t for p, n, t in extra if ASSERTX.search(t) and not negated(t)}.items())
    ctx = fetch_contexts([k for k, _ in cand])
    with open(SUPP, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sid", "path", "line", "text", "context"])
        for i, (key, t) in enumerate(cand, 1):
            w.writerow(["s%03d" % i, key[0], key[1], redact(t.strip()[:MAXLEN]), redact(ctx[key])])
    print("supplement (post-freeze): S1x lines %d ; not in frozen S1 %d ; candidates %d" % (len(s1x), len(extra), len(cand)))


def merge():
    cands = {r["cid"]: r for r in csv.DictReader(open(CAND, encoding="utf-8"))}
    man = {r["cid"]: r for r in csv.DictReader(open(MANUAL, encoding="utf-8"))}
    missing = sorted(set(cands) - set(man))
    extra = sorted(set(man) - set(cands))
    cls = Counter(man[c]["class"] for c in man)
    print("CFG908 file list (FROZEN_CRITERIA section 6); pinned tree %s; read only" % PIN)
    print("candidates %d ; hand-classed %d ; unclassed %d ; stray ids %d" % (len(cands), len(man), len(missing),
                                                                           len(extra)))
    print("classes: %s" % dict(sorted(cls.items())))
    rows = []
    for c in sorted(man):
        r = man[c]
        if r["class"].startswith("A"):
            rows.append((cands[c]["path"], int(cands[c]["line"]), r["class"], r.get("copy_of", ""), r.get("note", ""),
                         cands[c]["text"]))
    rows.sort()
    with open(OUT_A, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["path", "line", "class", "copy_of", "note", "text"])
        for row in rows:
            w.writerow(row)
    byfile = defaultdict(list)
    for p, n, k, cp, note, _ in rows:
        byfile[p].append((n, k, cp))
    print("class A lines: %d in %d files (%d lines are generated copies)" %
          (len(rows), len(byfile), sum(1 for r in rows if r[3])))
    for p in sorted(byfile):
        print("  %s: %s" % (p, ", ".join("%d%s%s" % (n, "" if k == "A" else " (%s)" % k, " [copy]" if cp else "")
                                          for n, k, cp in sorted(byfile[p]))))
    if os.path.exists(MISSREV):
        mr = list(csv.DictReader(open(MISSREV, encoding="utf-8")))
        na = sum(1 for r in mr if r["class"].startswith("A"))
        print("miss-rate check: %d of %d sampled non-selected lines are class A" % (na, len(mr)))
        for r in mr:
            if r["class"].startswith("A"):
                print("  missed A: %s %s" % (r["mid"], r.get("note", "")))
    if os.path.exists(SUPPREV):
        sc = {r["sid"]: r for r in csv.DictReader(open(SUPP, encoding="utf-8"))}
        sr = list(csv.DictReader(open(SUPPREV, encoding="utf-8")))
        sa = [r for r in sr if r["class"].startswith("A")]
        print("SUPPLEMENT (post-freeze, disclosed; not part of the frozen list): %d candidates, %d hand-classed, "
              "%d class A" % (len(sc), len(sr), len(sa)))
        for r in sa:
            print("  %s:%s%s  %s" % (sc[r["sid"]]["path"], sc[r["sid"]]["line"], " [copy]" if r.get("copy_of") else "",
                                    r.get("note", "")))
    if missing:
        print("UNCLASSED: %s" % missing)
        sys.exit(2)


if __name__ == "__main__":
    {"extract": extract, "merge": merge, "supplement": supplement}[sys.argv[1] if len(sys.argv) > 1 else "extract"]()
