#!/usr/bin/env python3
"""CW3 triage: the frozen grep (FROZEN_CRITERIA.md), the nu/mu filter (plus AMENDMENTS A2's named functions), and a
machine reading of every nu/mu call for an external-field argument (AMENDMENTS A3).  Reads files only; runs nothing.
Run from anywhere: OMP_NUM_THREADS=1 nice -n 10 python3 -I cw3_triage.py   -> cw3_grep_hits.txt, cw3_triage.json, cw3_triage.out
kappa = 1/2 FITTED; not theory closed."""
import os, re, json, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
GREP = ("git ls-files '*.py' | xargs grep -l -i -E \"external.?field|\\bg_?ext\\w*\\b|\\bgext\\w*\\b|\\bge\\s*=|\\bg_e\\s*=|\\bGE\\s*=|"
        "\\bETA0?\\b|\\befe\\b|1\\.9e-10|2\\.32e-10|1\\.778e-10|2\\.078e-10|200\\s*\\*\\*\\s*2|200e3\\s*\\*\\*\\s*2\"")
hits = sorted(l for l in subprocess.run(GREP, shell=True, cwd=REPO, capture_output=True, text=True).stdout.split("\n") if l.strip())
open(os.path.join(HERE, "cw3_grep_hits.txt"), "w").write("\n".join(hits) + "\n")
TOK = ("nu(", "nu_", "mu(", "mu_", "ν", "μ")
NAMED = re.compile(r"law_v\(|\brar\(|g_mond|gobs_from|mcgaugh\(|interp_fn|simple_interp|standard_interp|def (?:g_obs|gobs|mond)\w*\(", re.I)
CALL = re.compile(r"(?<![A-Za-z0-9_.])((?:nu|mu|ν|μ)(?:_\w+|\d\w*|[A-Z]\w*)?|law_v|rar|g_mond\w*|gobs_from\w*|mcgaugh)\s*\(")
EXTN = (r"ge|g_e|gE|GE|g_ext\w*|gext\w*|G_EXT\w*|GEXT\w*|g_ex|gex|x_e|xe|x_ext\w*|xext\w*|X_EXT\w*|y_e|ye|yE|YE|y_ext\w*|yext\w*|"
        r"Y_EXT\w*|yNe|y_Ne|y_N_ext|gNe|g_Ne|gN_ext|eN|e_N|eta\w*|ETA\w*|ext\w*|EXT\w*|g_host\w*|gx|ghost|g_gal\w*|g_mw\w*|gMW|g_MW\w*")
EXTW = re.compile(r"(?<![A-Za-z0-9_])(" + EXTN + r")(?![A-Za-z0-9_])")
OBS = re.compile(r"1\.9e-10|2\.32e-10|1\.778e-10|2\.078e-10|2\.0592e-10|\b1\.9\s*\*\s*(?:a0|A0)\w*|\(\s*2[0-4]\d(?:\.\d+)?e3\s*\)\s*\*\*\s*2|"
                 r"\b2[0-4]\de3\s*\*\*\s*2|\b200\s*\*\*\s*2|sqrt\(\s*G\w*\s*\*[^)]*a0[^)]*\)\s*/|\b[Vv]_?[cC]\w*\s*\*\*\s*2\s*/\s*\(?\s*R")
INV = re.compile(r"newton_from|y_newt_from_obs|yN_of|invert|inverse|brentq|from_total|_from_obs|y_newt", re.I)
MOND = re.compile(r"(?<![A-Za-z0-9_.])(?:nu|ν)\w*\s*\(|0\.5\s*\*\s*gN\s*\*\s*\(\s*1\s*\+|g_host\w*\s*\(|sqrt\(\s*G\w*\s*\*[^)]*a0")
NEWT = re.compile(r"\bG\w*\s*\*\s*\(?\s*\w*M\w*.*/\s*\(?.*\*\*\s*2")
def args(code, m):
    i = m.end(); d = 1; j = i
    while j < len(code) and d:
        d += {"(": 1, ")": -1}.get(code[j], 0); j += 1
    return code[i:j - 1]
def strip(line):
    s = re.sub(r"(\"\"\"|''').*?\1", "", line); s = re.sub(r"\"[^\"]*\"|'[^']*'", "''", s); return s.split("#", 1)[0]
rows = []; cnt = collections.Counter()
for f in hits:
    try: txt = open(os.path.join(REPO, f), encoding="utf-8", errors="replace").read()
    except OSError: continue
    if not (any(t in txt for t in TOK) or NAMED.search(txt)): continue
    L = txt.split("\n"); efnu, efmu, obs, names = [], [], [], set(); obsvars = set()
    for k, line in enumerate(L, 1):
        code = strip(line)
        if OBS.search(code):
            obs.append(k); mm = re.match(r"\s*([A-Za-z_]\w*)\s*=(?!=)", code)
            if mm: obsvars.add(mm.group(1))
    obsre = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, sorted(obsvars))) + r")(?![A-Za-z0-9_])") if obsvars else None
    for k, line in enumerate(L, 1):
        code = strip(line)
        for m in CALL.finditer(code):
            a = args(code, m); hit = EXTW.findall(a) + (obsre.findall(a) if obsre else [])
            if hit:
                (efmu if m.group(1).startswith(("mu", "μ")) else efnu).append(k); names.update(hit)
    src = collections.Counter()
    for k, line in enumerate(L, 1):
        code = strip(line)
        for n in names:
            if re.match(r"\s*(?:[A-Za-z_]\w*\s*,\s*)*" + re.escape(n) + r"\s*(?:,\s*[A-Za-z_]\w*\s*)*=(?!=)", code):
                rhs = code.split("=", 1)[1]
                tag = "obs" if OBS.search(rhs) else "inv" if INV.search(rhs) else "mond" if MOND.search(rhs) else "newt" if NEWT.search(rhs) else "other"
                src[tag] += 1
    if obsre and (efnu or efmu) and any(obsre.search(strip(L[k - 1])) for k in efnu + efmu): src["obs"] += 1
    c = ("Q?" if efnu and (obs or src["obs"]) else "N?" if efnu else "A?" if efmu else "L?" if obs else "CLEAR")
    cnt[c] += 1
    rows.append(dict(file=f, cls=c, efnu=efnu[:6], efmu=efmu[:6], obs=obs[:6], names=sorted(names)[:8], src=dict(src),
                     first=(L[(efnu or efmu or obs or [1])[0] - 1].strip()[:200])))
json.dump(dict(n_hits=len(hits), n_audit=len(rows), counts=dict(cnt), rows=rows), open(os.path.join(HERE, "cw3_triage.json"), "w"), indent=0)
O = [f"frozen grep hits: {len(hits)}; with a nu/mu call or a named interpolating function: {len(rows)}",
     "classes: Q? = external-field name in a nu call AND an observed-field literal in the file; N? = external-field name in a nu call, no observed literal;",
     "A? = external-field name in a mu call only; L? = observed literal, no external-field name in any nu/mu call; CLEAR = none of these",
     f"counts: {dict(cnt)}"]
for c in ("Q?", "N?", "A?", "L?"):
    O.append(f"\n== {c} ({cnt[c]})")
    for r in rows:
        if r["cls"] == c:
            ln = (r["efnu"] or r["efmu"] or r["obs"])[0]
            O.append(f"{r['file']}:{ln} | src {r['src']} | names {r['names']} | obs-lines {r['obs'][:3]} | {r['first'][:140]}")
open(os.path.join(HERE, "cw3_triage.out"), "w").write("\n".join(O) + "\n")
print("\n".join(O[:4]))
