#!/usr/bin/env python3
"""r2_program_history.py -- lane R1: run the author's published programs as published (Zenodo 17021330/17109113; GitHub commits 3ebb273, a635b6e, 0468974, 27da3a1, 3a2614a)
and test, by perturbation, whether the reference alpha (alpha_exp) enters the value each program reports.

Third-party programs are NOT copied into the repo: they are downloaded into $R1_CACHE (default: the session scratchpad) and their SHA-256 is printed.
Licence: the two Zenodo programs are CC-BY-4.0 (Zenodo API); the GitHub repository has no licence file, so its programs are run locally for verification only.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 r2_program_history.py
              -> exit 0 iff the flag vector equals the pre-registered one (R1_PREREGISTRATION.md):
                 {sep_reproduces: True, aug30_bytes_equal_zenodo17021330: True, a635b6e_depends_on_alpha_exp: True, later_commits_independent_of_alpha_exp: True}
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 r2_program_history.py --mutate
              -> the 'depends on alpha_exp' flag is evaluated on the SEPTEMBER program's logging constant (unused per the record) instead of a635b6e; it must come out False,
                 which breaks the recorded vector: exit 1.
"""
import sys, os, re, json, hashlib, subprocess, time, urllib.request
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
CACHE = os.environ.get("R1_CACHE", "./r1_cache")
os.makedirs(os.path.join(CACHE, "prog"), exist_ok=True)
os.makedirs(os.path.join(CACHE, "run"), exist_ok=True)
import mpmath as mp
mp.mp.dps = 40

def P(*a):
    print(" ".join(str(x) for x in a), flush=True)

GH = "https://raw.githubusercontent.com/pajuhaan/AlphaEmergent/%s/Full%%20Alpha%%20Geometry%%20Calculation.py"
ZEN = "https://zenodo.org/api/records/%s/files/Full%%20Alpha%%20Geometry%%20Calculation.py/content"
PROGS = [
    ("zen17021330", "Zenodo 17021330 (2025-09-01)", ZEN % "17021330"),
    ("zen17109113", "Zenodo 17109113 (2025-09-12)", ZEN % "17109113"),
    ("gh3ebb273", "GitHub 3ebb273 (2025-08-30)", GH % "3ebb273165b703159ef2ce6eb26868d634a474a7"),
    ("gha635b6e", "GitHub a635b6e (2026-04-08 10:51 UTC)", GH % "a635b6e7fe9eb69dbd73a7cedf4f6d774236bbd9"),
    ("gh0468974", "GitHub 0468974 (2026-04-08 15:02 UTC)", GH % "0468974d898ab3d4560f37d9cd789160b88025ef"),
    ("gh27da3a1", "GitHub 27da3a1 (2026-04-08 17:06 UTC)", GH % "27da3a120f0d679af762949514c7e968daf8cc64"),
    ("gh3a2614a", "GitHub 3a2614a (2026-04-16 12:02 UTC)", GH % "3a2614ae3503b9efe86c6b0b995ff4a7d14eed4d"),
]
path = {}; sha = {}
P("== fetch and hash ==")
for key, lab, url in PROGS:
    p = os.path.join(CACHE, "prog", key + ".py")
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(p, "wb").write(r.read())
    path[key] = p
    sha[key] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    P("  %-13s %-42s sha256 %s  lines %d" % (key, lab, sha[key][:16], open(p, encoding="utf-8").read().count("\n")))
aug30_eq = sha["gh3ebb273"] == sha["zen17021330"]
P("  GitHub 3ebb273 program bytes == Zenodo 17021330 program bytes: %s" % aug30_eq)

def run(src_path, extra_args=(), patches=(), tag="x", timeout=900):
    src = open(src_path, encoding="utf-8").read()
    for a, b in patches:
        assert a in src, "patch text not found: %r" % a
        src = src.replace(a, b)
    scratch = os.path.join(CACHE, "run", tag + ".py")
    open(scratch, "w", encoding="utf-8").write(src)
    t0 = time.time()
    r = subprocess.run([sys.executable, scratch] + list(extra_args), capture_output=True, text=True, timeout=timeout,
                       cwd=os.path.join(CACHE, "run"), env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.stdout, r.returncode, time.time() - t0

def cells(text, label, nth=0):
    """cells of the nth table row whose first cell contains `label` (rich/tabulate box tables)."""
    k = 0
    for line in text.splitlines():
        if "│" in line:
            cs = [c.strip() for c in line.strip().strip("│").split("│")]
            if len(cs) >= 2 and cs[0] == label:
                if k == nth: return cs
                k += 1
    return None

results = {"sha": {k: v for k, v in sha.items()}, "aug30_bytes_equal_zenodo17021330": aug30_eq}
P("\n== September-2025 program as published (Zenodo 17109113 and 17021330, GitHub 3ebb273) ==")
sep = {}
for key in ("zen17109113", "zen17021330", "gh3ebb273"):
    out, rc, dt = run(path[key], tag="run_" + key)
    a = re.search(r"alpha_em\^-1\s*=\s*([0-9.]+)", out); l = re.search(r"Λ_eff \(final\)\s*=\s*([0-9.]+)", out)
    sep[key] = (mp.mpf(a.group(1)), mp.mpf(l.group(1)), rc, dt)
    P("  %-12s exit %d  %.1fs  alpha^-1 = %s  Lambda_eff = %s" % (key, rc, dt, a.group(1), l.group(1)))
sep_val = sep["zen17109113"][0]
sep_repro = abs(sep_val - mp.mpf("137.0359991769773")) < mp.mpf("1e-9") and all(abs(v[0] - sep_val) < mp.mpf("1e-12") for v in sep.values())
P("  all three Sept-2025 programs print the same alpha^-1 and it equals the printed cfg-1 value 137.0359991769773 (to 1e-9): %s" % sep_repro)
results["sep"] = {k: [str(v[0]), str(v[1])] for k, v in sep.items()}

P("\n== April-2026 lineage: programs as published (defaults) ==")
apr = {}
out, rc, dt = run(path["gha635b6e"], tag="run_a635b6e")
r5 = cells(out, "Current article scalar branch (rank-5)"); r100 = cells(out, "Refined no-free-parameter branch (rank-100)"); ll = cells(out, "Lambda_lock")
apr["a635b6e"] = dict(rank5_inv=r5[2], rank100_inv=r100[2], lambda_lock=ll[1])
P("  a635b6e (exit %d, %.1fs): rank-5 alpha^-1 = %s ; refined rank-100 alpha^-1 = %s ; Lambda_lock = %s" % (rc, dt, r5[2][:24], r100[2][:24], ll[1][:24]))
for key, nm in (("gh0468974", "0468974"), ("gh27da3a1", "27da3a1")):
    out, rc, dt = run(path[key], tag="run_" + nm)
    ai = cells(out, "alpha_article^-1"); lg = cells(out, "Lambda_geom")
    apr[nm] = dict(alpha_article_inv=ai[1], lambda_geom=lg[1])
    P("  %s (exit %d, %.1fs): alpha_article^-1 = %s ; Lambda_geom = %s" % (nm, rc, dt, ai[1][:24], lg[1][:24]))
out, rc, dt = run(path["gh3a2614a"], tag="run_3a2614a", extra_args=("--output-txt", os.path.join(CACHE, "run", "3a2614a_report.txt")))
la = re.search(r"Λ_geom = ([0-9.]+)", out); aa = re.search(r"α_pred\s*=\s*([0-9.]+)", out)
lam3 = la.group(1); a3 = mp.mpf(aa.group(1))
apr["3a2614a"] = dict(alpha_pred_inv=str(1 / a3), lambda_geom=lam3)
P("  3a2614a (exit %d, %.1fs): alpha_pred^-1 = %s ; Lambda_geom = %s" % (rc, dt, mp.nstr(1 / a3, 22), lam3[:24]))
results["apr"] = apr

P("\n== dependency test: does the reference alpha (alpha_exp) enter the value the program reports?  (alpha_exp^-1 := 137.035999177 -> 137.035999177 x (1 + 1e-9)) ==")
PERT = "137.035999314736"   # 137.035999177 * (1 + 1e-9), rounded to 15 digits
rel = (mp.mpf(PERT) - mp.mpf("137.035999177")) / mp.mpf("137.035999177")
P("  perturbation: relative %s in alpha_exp^-1" % mp.nstr(rel, 4))
dep = {}
# (a) a635b6e: the default lock is built from alpha_exp
out2, rc, dt = run(path["gha635b6e"], patches=[('ALPHA_INV_EXP = mp.mpf("137.035999177")', 'ALPHA_INV_EXP = mp.mpf("%s")' % PERT)], tag="pert_a635b6e")
r5p = cells(out2, "Current article scalar branch (rank-5)"); llp = cells(out2, "Lambda_lock")
el5 = (1 / mp.mpf(r5p[2]) - 1 / mp.mpf(r5[2])) / (1 / mp.mpf(r5[2])) / (-rel)   # d ln alpha_out / d ln alpha_exp  (alpha ~ 1/inv; rel is on the inverse)
ell = (mp.mpf(llp[1]) - mp.mpf(ll[1])) / mp.mpf(ll[1])
P("  a635b6e: rank-5 alpha^-1 %s -> %s ; d ln(alpha_out)/d ln(alpha_exp) = %s ; Lambda_lock shifts by %s relative" % (r5[2][:22], r5p[2][:22], mp.nstr(el5, 6), mp.nstr(ell, 4)))
dep["a635b6e"] = float(el5)
# (b) 0468974 and 27da3a1: alpha_exp is a diagnostic only
for key, nm, old in (("gh0468974", "0468974", 'alpha_inv_exp=mp.mpf("137.035999177")'), ("gh27da3a1", "27da3a1", 'alpha_inv_exp=mp.mpf("137.035999177")')):
    src = open(path[key], encoding="utf-8").read()
    k = src.count(old)
    out2, rc, dt = run(path[key], patches=[(old, 'alpha_inv_exp=mp.mpf("%s")' % PERT)], tag="pert_" + nm)
    ai2 = cells(out2, "alpha_article^-1")
    d = abs(mp.mpf(ai2[1]) - mp.mpf(apr[nm]["alpha_article_inv"]))
    P("  %s: alpha_exp occurrences patched = %d ; alpha_article^-1 %s -> %s ; |change| = %s" % (nm, k, apr[nm]["alpha_article_inv"][:22], ai2[1][:22], mp.nstr(d, 3)))
    dep[nm] = float(d)
# (c) 3a2614a at reduced settings (Q4 showed reduced settings reproduce the full value to 1.5e-11)
red = ("--dps", "60", "--max-odd-mode", "41", "--gl-nodes", "256", "--workers", "2", "--output-txt", os.path.join(CACHE, "run", "3a2614a_red.txt"))
outb, rc, dt = run(path["gh3a2614a"], extra_args=red, tag="red_3a2614a")
outp, rc2, dt2 = run(path["gh3a2614a"], extra_args=red, patches=[('ALPHA_INV_REF = mp.mpf("137.035999177")', 'ALPHA_INV_REF = mp.mpf("%s")' % PERT)], tag="pert_3a2614a")
ab = mp.mpf(re.search(r"α_pred\s*=\s*([0-9.]+)", outb).group(1)); ap = mp.mpf(re.search(r"α_pred\s*=\s*([0-9.]+)", outp).group(1))
P("  3a2614a (reduced settings, %.0fs+%.0fs): alpha_pred %s -> %s ; |change| = %s" % (dt, dt2, mp.nstr(ab, 20), mp.nstr(ap, 20), mp.nstr(abs(ap - ab), 3)))
dep["3a2614a"] = float(abs(ap - ab))
# (d) September program: the logging constant
src = open(path["zen17109113"], encoding="utf-8").read()
oldref = "ALPHA_REF = mp.mpf('7.297352564311e-3')"
assert oldref in src
outs, rcs, dts = run(path["zen17109113"], patches=[(oldref, "ALPHA_REF = mp.mpf('7.4e-3')")], tag="pert_sep")
a_s = mp.mpf(re.search(r"alpha_em\^-1\s*=\s*([0-9.]+)", outs).group(1))
P("  Sept-2025 program (ALPHA_REF 7.297352564311e-3 -> 7.4e-3): alpha^-1 %s -> %s ; |change| = %s" % (mp.nstr(sep_val, 18), mp.nstr(a_s, 18), mp.nstr(abs(a_s - sep_val), 3)))
dep["sep"] = float(abs(a_s - sep_val))
results["dependency"] = dep

TOL_INDEP = 1e-12
h6 = (dep["sep"] > 1e-9) if MUTATE else (dep["a635b6e"] > 0.5)
later_indep = dep["0468974"] < TOL_INDEP and dep["27da3a1"] < TOL_INDEP and dep["3a2614a"] < 1e-15
P("\n== derived comparisons (numbers from the programs above) ==")
lam_lock = mp.mpf(apr["a635b6e"]["lambda_lock"]); lam_geom = mp.mpf(lam3); lam_sep = sep["zen17109113"][1]
P("  Lambda back-solved from alpha_exp (a635b6e, Apr 8 morning)      = %s" % mp.nstr(lam_lock, 20))
P("  Lambda 'mean' representative pasted in 0468974 (Apr 8 afternoon) = %s" % apr["0468974"]["lambda_geom"][:22])
P("  Lambda_geom computed by 3a2614a (Apr 16)                        = %s" % mp.nstr(lam_geom, 20))
P("  relative difference Lambda_geom(3a2614a) vs Lambda_lock(alpha_exp) = %s  (in alpha^-1 at the April elasticity 1.0032: %s relative)" % (mp.nstr((lam_geom - lam_lock) / lam_lock, 4), mp.nstr(1.003247 * (lam_geom - lam_lock) / lam_lock, 4)))
P("  Lambda_eff Sept-2025 program                                    = %s" % mp.nstr(lam_sep, 20))
dl = (lam_geom - lam_sep) / lam_sep
inv_apr = 1 / a3; inv_sep = sep_val
dalpha = (inv_sep - inv_apr) / inv_sep     # relative change of alpha from Sep to Apr (alpha ~ 1/inv)
P("  Sep -> Apr:  Lambda changed by %s (relative); alpha changed by %s (relative)" % (mp.nstr(dl, 5), mp.nstr(dalpha, 4)))
P("               at the April elasticity d ln alpha/d ln Lambda = 1.003247 the Lambda change alone would move alpha by %s ; so the scalar evaluator changed alpha by %s (compensation) ; residual/compensation = %s"
  % (mp.nstr(1.003247 * dl, 5), mp.nstr(dalpha - 1.003247 * dl, 5), mp.nstr(abs(dalpha / (1.003247 * dl)), 4)))
results["derived"] = dict(lam_lock=str(lam_lock), lam_geom=str(lam_geom), lam_sep=str(lam_sep), dl=str(dl), dalpha=str(dalpha))
json.dump(results, open(os.path.join(HERE, "r2_results%s.json" % ("_MUTATE" if MUTATE else "")), "w"), indent=1, default=str)

flags = dict(sep_reproduces=bool(sep_repro), aug30_bytes_equal_zenodo17021330=bool(aug30_eq), a635b6e_depends_on_alpha_exp=bool(h6), later_commits_independent_of_alpha_exp=bool(later_indep))
expected = dict(sep_reproduces=True, aug30_bytes_equal_zenodo17021330=True, a635b6e_depends_on_alpha_exp=True, later_commits_independent_of_alpha_exp=True)
P("\nflags   :", flags)
P("expected:", expected)
ok = flags == expected
P("VERDICT of script: %s" % ("recorded flag vector reproduced (exit 0)" if ok else "flag vector differs from the recorded one (exit 1)"))
sys.exit(0 if ok else 1)
