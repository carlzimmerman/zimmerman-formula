#!/usr/bin/env python3
"""q5_pajuhaan_checks.py -- lane Q4: checks on the 'Relator / Emergent C-Space' derivation of 1/alpha (Zenodo 16944532 versions; GitHub pajuhaan/AlphaEmergent).
Third-party programs are downloaded (not copied into the repo) to $Q4_CACHE (default: the session scratchpad) and hashed; imports lane D's bar_lib only for constants.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q5_pajuhaan_checks.py            -> exit 0 iff T2, T3, T4, T5 (Amendment 4) and T6 (Amendment 7) assertions hold
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q5_pajuhaan_checks.py --mutate   -> T3 is repeated with Lambda_ind perturbed by +1e-6 relative; the reproduction assertion must fail; exit 1
"""
import sys, os, hashlib, subprocess, re, urllib.request, importlib.util, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import mpmath as mp
import bar_lib as B
mp.mp.dps = 60
MUTATE = "--mutate" in sys.argv
CACHE = os.environ.get("Q4_CACHE", "./q4_cache")
os.makedirs(CACHE, exist_ok=True)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
T = mp.mpf("137.035999177")
SIGABS = mp.mpf("2.1e-8")

def fetch(name, url):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=120) as r:
            open(path, "wb").write(r.read())
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    P("  fetched %-24s sha256 %s  (%s)" % (name, h[:16], url))
    return path

OLD_URL = "https://zenodo.org/api/records/17109113/files/Full%20Alpha%20Geometry%20Calculation.py/content"
NEW_URL = "https://raw.githubusercontent.com/pajuhaan/AlphaEmergent/main/Full%20Alpha%20Geometry%20Calculation.py"
P("== T1: published values by version (transcribed from the version PDFs; record ids are Zenodo) ==")
vers = [("17021330 (2025-09-01)", "137.0359991770873", "0.6916840202841755642869", "Table IV cfg5; 'Emergent alpha input' table"),
        ("17109113 (2025-09-12)", "137.0359991770872", "0.6916840202841763119337", "Table IV cfg2"),
        ("17385707 (2025-10-18)", "137.0359991770872", "0.6916840202841763119337", "Table IV; 'This work (emergent) 0.007297352564326775'"),
        ("19462288 (2026-04-08)", "137.03599916349474199", None, "lock table"),
        ("19819000 (2026-04-27)", "137.035999163494704022", "0.6916831461069910267", "Final primary result")]
for rid, a, lam, note in vers:
    v = mp.mpf(a)
    P("  %-22s 1/alpha = %-24s miss vs 137.035999177 = %s (%s sigma_CODATA rel; %s in the source's 2.1e-8 unit) ; Lambda = %s ; %s" %
      (rid, a, mp.nstr(abs(v / T - 1), 3), mp.nstr(abs(v / T - 1) / mp.mpf("1.6e-10"), 3), mp.nstr(abs(v - T) / SIGABS, 3), lam, note))
dinv = mp.mpf("137.0359991770873") - mp.mpf("137.035999163494704022")
dlam = (mp.mpf("0.6916840202841755642869") - mp.mpf("0.6916831461069910267")) / mp.mpf("0.6916840202841755642869")
P("  drift 2025 -> 2026: 1/alpha changed by %s (%s relative) while Lambda changed by %s relative; with the source's own elasticity d ln alpha/d ln Lambda = 1.0032 the Lambda change alone would move alpha by %s: the scalar evaluator was also changed (a compensating change of size %s)" %
  (mp.nstr(dinv, 4), mp.nstr(dinv / T, 3), mp.nstr(dlam, 4), mp.nstr(dlam * mp.mpf("1.003247"), 4), mp.nstr(dlam * mp.mpf("1.003247") - dinv / T, 3)))

P("== T2: September 2025 program (Zenodo 17109113) ==")
old = fetch("old_calc.py", OLD_URL)
def run_old(patches=None):
    src = open(old, encoding="utf-8").read()
    for a, b in (patches or []):
        assert a in src, a
        src = src.replace(a, b)
    p = os.path.join(CACHE, "old_variant.py"); open(p, "w", encoding="utf-8").write(src)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=600, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    m = re.search(r"alpha_em\^-1\s*=\s*([0-9.]+)", r.stdout)
    return mp.mpf(m.group(1)) if m else None, r
v_old, _ = run_old()
P("  1/alpha = %s ; printed 137.0359991769773 ; |difference| = %s" % (mp.nstr(v_old, 16), mp.nstr(abs(v_old - mp.mpf("137.0359991769773")), 3)))
t2 = abs(v_old - mp.mpf("137.0359991769773")) < mp.mpf("1e-9")
P("  T2 reproduces: %s ; miss vs 2022 = %s relative" % (t2, mp.nstr(abs(v_old / T - 1), 3)))

P("== T4: September 2025 program, switches the source calls 'optional' ==")
variants = [("CHI_LADDER_ON = False", [("CHI_LADDER_ON    = True", "CHI_LADDER_ON    = False")]),
            ("SELF_LADDER_ON = False", [("SELF_LADDER_ON    = True", "SELF_LADDER_ON    = False")]),
            ("both ladders off", [("CHI_LADDER_ON    = True", "CHI_LADDER_ON    = False"), ("SELF_LADDER_ON    = True", "SELF_LADDER_ON    = False")]),
            ("CURV_SERIES_ORDER = 4", [("CURV_SERIES_ORDER = 12", "CURV_SERIES_ORDER = 4")]),
            ("OUT_LMAX = 41", [("OUT_LMAX  = 19", "OUT_LMAX  = 41")])]
shifts = []
for lab, pt in variants:
    try:
        v, r = run_old(pt)
    except AssertionError as e:
        P("  %-26s : patch text not found (%s)" % (lab, e)); continue
    if v is None:
        P("  %-26s : no result parsed" % lab); continue
    sh = v - v_old
    shifts.append((lab, sh))
    P("  %-26s : 1/alpha = %s ; shift vs the printed configuration = %s (%s relative; bar miss is 5e-10) ; miss vs 2022 = %s" % (lab, mp.nstr(v, 16), mp.nstr(sh, 4), mp.nstr(abs(sh) / v_old, 3), mp.nstr(abs(v / T - 1), 3)))
t4 = any(abs(sh) / v_old > mp.mpf("5e-10") for lab, sh in shifts)
P("  T4 at least one 'optional' switch moves 1/alpha by more than 5e-10 relative: %s" % t4)

P("== T6: does the September 2025 program take the target as input? ==")
v_none, _ = run_old([("ALPHA_REF = mp.mpf('7.297352564311e-3')", "ALPHA_REF = None")])
v_wrong, _ = run_old([("ALPHA_REF = mp.mpf('7.297352564311e-3')", "ALPHA_REF = mp.mpf('1')/137")])
P("  ALPHA_REF -> None      : 1/alpha = %s ; difference from the printed configuration = %s" % (mp.nstr(v_none, 16), mp.nstr(v_none - v_old, 3)))
P("  ALPHA_REF -> 1/137     : 1/alpha = %s ; difference from the printed configuration = %s" % (mp.nstr(v_wrong, 16), mp.nstr(v_wrong - v_old, 3)))
t6a = abs(v_none - v_old) < mp.mpf("1e-13") and abs(v_wrong - v_old) < mp.mpf("1e-13")
v_p, _ = run_old([("EPS_GIND         = mp.mpf('0')", "EPS_GIND         = mp.mpf('1e-9')")])
v_m, _ = run_old([("EPS_GIND         = mp.mpf('0')", "EPS_GIND         = mp.mpf('-1e-9')")])
P("  EPS_GIND -> +1e-9      : 1/alpha = %s ; shift = %s (%s relative)" % (mp.nstr(v_p, 16), mp.nstr(v_p - v_old, 3), mp.nstr(abs(v_p - v_old) / v_old, 3)))
P("  EPS_GIND -> -1e-9      : 1/alpha = %s ; shift = %s (%s relative)" % (mp.nstr(v_m, 16), mp.nstr(v_m - v_old, 3), mp.nstr(abs(v_m - v_old) / v_old, 3)))
t6b = abs(v_p - v_old) / v_old > mp.mpf("5e-10")
P("  T6 (i) target constant is logging-only (unchanged when replaced): %s ; (ii) the offset knob is load-bearing at > 5e-10 relative (it is set to 0 by the author): %s" % (t6a, t6b))

P("== T3: current program (GitHub AlphaEmergent), reduced settings, one worker ==")
new = fetch("new_calc.py", NEW_URL)
spec = importlib.util.spec_from_file_location("relator_calc", new)
calc = importlib.util.module_from_spec(spec); sys.modules["relator_calc"] = calc; spec.loader.exec_module(calc)
def run_new(lam_ind_rel=0.0, patches=None, max_odd=41, dps=60, gl=256):
    mp.mp.dps = dps
    saved = {}
    if lam_ind_rel:
        saved["LAMBDA_IND"] = calc.LAMBDA_IND; calc.LAMBDA_IND = calc.LAMBDA_IND * (1 + mp.mpf(lam_ind_rel))
    for k, rel in (patches or {}).items():
        saved[k] = getattr(calc, k); setattr(calc, k, getattr(calc, k) * (1 + mp.mpf(rel)))
    try:
        ld = calc.evaluate_lambda_geom(max_odd, 1, dps, gl)
        base = calc.build_base_shell_geometry()
        sc = calc.build_current_scalar_scenario(calc.ARTICLE_RANK, base)
        dc = calc.dc_lock_from_lambda(ld.lambda_geom)
        a = calc.solve_alpha_for_scenario(dc, sc)
    finally:
        for k, v in saved.items():
            setattr(calc, k, v)
    return 1 / a, ld.lambda_geom
t0 = time.time()
v_new, lam_new = run_new(0.0)
P("  reduced settings (odd modes <= 41, 256 nodes, dps 60): 1/alpha = %s ; Lambda_geom = %s ; %.0f s" % (mp.nstr(v_new, 16), mp.nstr(lam_new, 16), time.time() - t0))
pub = mp.mpf("137.0359991634947040218")
P("  published (full settings; reproduced by hand at 137.0359991634947040218): |difference| = %s" % mp.nstr(abs(v_new - pub), 3))
mp.mp.dps = 60
if MUTATE:
    v_chk, _ = run_new(1e-6)
    P("  MUTATE: Lambda_ind perturbed by +1e-6 relative: 1/alpha = %s ; |difference from published| = %s" % (mp.nstr(v_chk, 16), mp.nstr(abs(v_chk - pub), 3)))
else:
    v_chk = v_new
t3 = abs(v_chk - pub) < mp.mpf("5e-9")
P("  T3 reproduces the published value to 5e-9: %s ; miss vs 2022 of the published value = %s relative (%s sigma_CODATA)" % (t3, mp.nstr(abs(pub / T - 1), 3), mp.nstr(abs(pub / T - 1) / mp.mpf("1.6e-10"), 3)))

P("== T5: current program, log-elasticities of alpha to six hand-built constants (+1e-4 relative perturbation each) ==")
ok5 = True
for k in ("LAMBDA_IND", "C0_GAUSS", "GAMMA_GEOM", "A_UV", "B_IR", "K_GEOMETRIC"):
    va, _ = run_new(0.0, {k: "1e-4"})
    el = (mp.log(1 / va) - mp.log(1 / v_new)) / mp.log(1 + mp.mpf("1e-4"))
    tol = mp.mpf("5e-10") / abs(el) if el != 0 else mp.inf
    ok5 = ok5 and (el != 0)
    P("  %-12s = %s : d ln alpha / d ln x = %s ; to keep the bar's 5e-10 the constant must be right to %s relative" % (k, mp.nstr(getattr(calc, k), 10), mp.nstr(el, 6), mp.nstr(tol, 3)))
P("  T5 all six elasticities nonzero: %s" % ok5)
P("  a constant that enters at first order must be 'right' to <= 5e-10/elasticity; the alternatives the author lists (e.g. ln 2, gamma, pi combinations) differ from each other by O(1) relative")
ok = t2 and t3 and t4 and ok5 and t6a and t6b
if MUTATE:
    P("MUTATE: T3 %s (a live control fails here); exit %d" % ("holds" if t3 else "FAILS", 0 if ok else 1))
    open(os.path.join(HERE, "q5_pajuhaan_checks_MUTATE.out"), "w").write("\n".join(out) + "\n")
    sys.exit(0 if ok else 1)
P("T2=%s T3=%s T4=%s T5=%s T6=%s/%s" % (t2, t3, t4, ok5, t6a, t6b))
open(os.path.join(HERE, "q5_pajuhaan_checks.out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if ok else 1)
