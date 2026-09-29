#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG64 -- KERNEL ROBUSTNESS OF THE COMMITTED RULE / UFD / SUPER-SPIRAL LANES: nu_mono (the campaign default) versus P2.

FROZEN QUESTION (verbatim):
  'Is any headline verdict of the committed lanes CFG40, CFG41, CFG42, CFG45, CFG46, CFG51, CFG56 and CFG58/CFG59 (the pass/fail of each declared
   hypothesis, and the sigma of each headline offset) sensitive to the choice of the interpolating kernel, nu_mono (the campaign default) versus P2
   (nu_p2 in CFG7_common/CFG4_common; CFG14 found P2 disfavoured at about 2 sigma by the SPARC transition shape, not excluded)?  A verdict is
   KERNEL-SENSITIVE if its pass/fail flips or its headline offset changes by more than 0.05 dex or by more than 1 sigma under P2 relative to nu_mono;
   otherwise KERNEL-ROBUST.'
Program rules that apply: kappa = 1/2 is FITTED; no tuning after seeing results; a robustness result of any kind is valid; nothing here says the theory is
closed; both a0 footings (9.36e-11 canonical / 1.13e-10 alt) are exercised because every lane already scores both (see FOOTINGS below).

WHAT THE KERNELS ARE (read from CFG4_common, not from the brief): nu_p2(y) = sqrt(1 + 1/y) (g_obs = sqrt(g_bar^2 + g_bar a0)), so nu_p2(1) = sqrt(2) = 1.41421.
nu_mono = FP1's monotone repair of nu_RAR (exec'd read-only inside CFG4_common), nu_mono(1) = 1 + H(1) (a table interpolant; value printed by the harness).  The
brief's alternative form sqrt((1 + sqrt(1 + 4/y))/2) is NOT what CFG4_common calls P2 (its y = 1 value is 1.272) and is not used; the lanes' own P2 is.

THE SWAP (declared).  For every lane a COPY of its script is written to lane_copies/<lane>__<kernel>.py with one line added directly after `import CFG7_common as C`
(a marker that prints nu(1) through C.nu_mono).  The copy is exec'd in a child process with __file__ set to the repo lane path (so HERE / REPO / LANES resolve
to the repo, read-only) and with Report.write redirected to runs/<lane>__<kernel>/ (nothing is written into the repo; bytecode writing is off).  The kernel swap is
done BEFORE the lane runs, at the CODE level: `CFG4_common.nu_mono.__code__` is replaced by P2's (or, for the control, the Newtonian nu = 1) body, keeping the
function object.  That is stricter than `C.nu_mono = C.nu_p2`: every reference to the kernel -- C.nu_mono, C4.nu_mono, KERNELS['nu_mono'], the copies of it inside the
namespaces the lanes exec (CFG36 / CFG7_hierarchy_fg001 / CFG45 prefix / k_contrarian_dwarfefe / hunt_lib) and any function default or argument that captured it
-- becomes P2, with no import-order dependence.  Every P2 call increments a counter (proof the kernel is actually used).  Every other choice is frozen: footings,
floors, thresholds, seeds, data, x_e = 0.40, M_c laws, MUTATE = 0 inside each lane.  Values that a lane READS from a committed results file are not recomputed
(they are data of the lane's controls); they are not swapped and are a declared fragile assumption (README).

EXTENDED SWAP (added after the FIRST RUN, before the second; disclosed).  The first run swapped only nu_mono.  CFG42, CFG46, CFG51 (and the FG001-derived parts of
CFG45, CFG58, CFG59) did not move at all, and G1 failed as designed: their isolated law is NOT nu_mono, despite the docstrings -- CFG7_hierarchy_fg001's a_int calls
hunt_lib.nu_s, the hard-coded exponential RAR form nu_RAR = 1/(1 - exp(-sqrt y)); CFG58's LV dwarfs use k_contrarian_dwarfefe.nu (also nu_RAR, as a default argument).
nu_RAR is the shape nu_mono is the monotone repair of (they agree deep in the MOND regime where the ultra-faints sit), so the intended kernel question for those lanes is
'RAR-form versus P2'.  The swap now also replaces, at the code level, hunt_lib.nu, hunt_lib.nu_s and k_contrarian_dwarfefe.nu.  The classification rules, thresholds and
gates were NOT changed by this; the first run's other results (CFG40 / CFG41 / CFG56 moved by <= 0.03 dex, CFG56 H1 flipped PASS -> FAIL) are unaffected by the extension.
SECOND EXTENSION (after the residual-leak audit R1 of the second run; disclosed): fable_independent_2026/L23_udg_verify.py carries its own boost nu(y) = 1 + Delta(y)/y
(the saturated RAR-type form) which CFG31 exec's (CFG58's UDG population) for its control and floor; the child now wraps CFG4_common.exec_slices so that this nu is swapped
too when it appears.  The audit's other hits are false positives (cosmology / sampling code that uses exp and sqrt) or unused references (CFG4_common.nu_rar, FP1 _h_rar).
POST-RUN SCOPE CORRECTION to G1 (disclosed): a lane that crashes under the alternative kernel (only possible for the Newtonian one) counts as bite -- the swap changed the run.
POST-RUN SCOPE CORRECTION to C2 (disclosed): its clause 'every child wrote results' applies to the P2 children; the Newtonian control crashes in CFG45 and CFG58 (a division
by the zero edge phantom inside their own C2-type controls) and is reported as NOT RUN, as the classification rules already declare.
Also from the first run: the declared control C3 (CFG41 H2 flips under nu = 1) FAILED -- CFG41 H2 stays PASS with the Newtonian law plus the full collapse halo (-1.43 sigma).
It is kept as declared and reported as a FAIL.  Added afterwards (post-hoc, disclosed): all nine lanes are also run under nu = 1 in the main run, and C3b requires at
least one HEADLINE verdict to flip under nu = 1.  A residual-leak audit (reported) scans every function object alive after a lane finishes for RAR-form kernels
(code using exp / expm1 together with sqrt) that were not swapped.

FOOTINGS.  Every lane in scope scores both footings inside one run (H rows name "canonical" and "alt"; CFG40 / CFG41 / CFG56 report the alt footing in an R row).
"Also run under the alt footing" is therefore satisfied by the lanes' own two-footing evaluation: the classification below uses every H row (both footings where
the row carries both) and additionally the R rows whose name says 'alt footing' (companions, reported and classified by the same rule; the lane classification
is the union).

THE HYPOTHESES AND HEADLINES (from each lane's own docstring; not chosen by result):
  CFG40 H2   CFG41 H2   CFG42 H1   CFG45 H1   CFG46 H1   CFG51 H1   CFG56 H2   CFG58 H1   CFG59 H1        (headline = the first-named [HEADLINE] hypothesis)
  A 'declared hypothesis' = every check of the lane whose name begins 'H<digit>' (including the reported ones).

CLASSIFICATION RULES (declared before the first run; the frozen question's rule made operational):
  * VERDICT FLIP: the check's ok flag differs between nu_mono and the alternative kernel.  For the three reported rows whose verdict is embedded in text
    (CFG45 H2 'which readings pass', CFG58 H2 'the classification', CFG59 H2 'the universal-phi answer'), the verdict is the detail string with every decimal number
    masked; a difference in that masked string is a verdict flip.
  * OFFSET CHANGE: the decimal tokens of the row's detail string are extracted in order (regex [+-]?\d+\.\d+, exponent forms and tokens preceded by '> ' or
    followed by '?)' are skipped; the H3 rows of CFG41 / CFG42, whose numbers are fractions f_ex, are numerically skipped; 'phi_needed' values are skipped).  A token is a
    SIGMA token if it is followed by 'sigma' (also in 'a/b sigma') or is enclosed in parentheses; every other token is a DEX token (offsets in dex; CFG58 H1's
    numbers are dex changes by that lane's own units).  Aligned by position when the two strings have the same token count (otherwise the row is flagged MISALIGNED and
    classified on the verdict alone).  A row is offset-sensitive if any aligned DEX token changes by > 0.05 or any aligned SIGMA token changes by > 1.0
    (strict inequality, the question's wording).
  * A hypothesis is KERNEL-SENSITIVE if either rule fires; else KERNEL-ROBUST.  A lane is KERNEL-SENSITIVE if any of its hypotheses is; its HEADLINE is classified
    separately.  A lane that crashes under the alternative kernel is reported 'NOT RUN' and counted as a swap failure, not a verdict.
  * Controls / other checks of a lane (C*, R* not naming alt) are reported for information; committed-value controls are EXPECTED to fail under P2 (they compare to
    nu_mono numbers) and are not verdicts.

CHECKS OF THIS HARNESS:
  C1  CONTROL  the nu_mono copies reproduce every committed lane result (check names, ok flags and detail strings identical) -- the harness is the lane.
  C2  CONTROL  the swap plumbing: nu_p2(1) != nu_mono(1) by > 0.01; after the swap nu(1) equals sqrt(2) to 1e-12 in every P2 child (Newtonian: 1); every alternative
               child called the swapped kernel > 10 times; every child completed and wrote its results.
  G1  GATE     'the swap has bite': for EVERY lane at least one decimal token of some check differs between nu_mono and the alternative kernel by > 1e-6.
  C3  CONTROL  the absurd kernel: with nu = 1 (Newtonian), CFG41 H2 (its headline; PASS under nu_mono) FLIPS to FAIL.  (As declared before the first run.)
  C3b CONTROL  (added after the first run, disclosed): with nu = 1 in ALL nine lanes, at least one headline verdict flips its pass/fail (the classifier can see a flip).
  H1  [HEADLINE; MUTATE must fail]  every one of the nine headline verdicts is KERNEL-ROBUST under the alternative kernel.  (A FAIL here is a valid result: it says
      at least one headline is kernel-sensitive.)
  H2  (reported) every declared hypothesis of the nine lanes is KERNEL-ROBUST; the sensitive ones are listed.
MUTATE=1: the alternative kernel is the absurd Newtonian nu = 1 for ALL lanes (instead of P2) -- H1 must FAIL (rc = 1), and does so only if the classifier can see flips.
RESIDUAL-LEAK AUDIT (reported, R1): RAR-form functions alive after each P2 lane that were not swapped.
Run: python3 cfg64_kernel_robustness.py   (MUTATE=1 for the control).  Outputs in the scratch directory holding this file.
"""
import os, sys, re, json, subprocess, time, math
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
NAMES = ["CFG40_super_spirals", "CFG41_massive_spirals_hi", "CFG42_satellites_rule", "CFG45_rule_readings", "CFG46_ufd_binary_corrected",
         "CFG51_walker_ufd", "CFG56_super_spirals_bulge", "CFG58_rule_more_populations", "CFG59_universal_debris_fraction"]
HEADLINE = {"CFG40_super_spirals": "H2", "CFG41_massive_spirals_hi": "H2", "CFG42_satellites_rule": "H1", "CFG45_rule_readings": "H1",
            "CFG46_ufd_binary_corrected": "H1", "CFG51_walker_ufd": "H1", "CFG56_super_spirals_bulge": "H2", "CFG58_rule_more_populations": "H1",
            "CFG59_universal_debris_fraction": "H1"}
EMBEDDED = {("CFG45_rule_readings", "H2"), ("CFG58_rule_more_populations", "H2"), ("CFG59_universal_debris_fraction", "H2")}
NUM_SKIP = {("CFG41_massive_spirals_hi", "H3"), ("CFG42_satellites_rule", "H3")}
DEX_TOL, SIG_TOL = 0.05, 1.0
MARK = "CFG64 marker: kernel nu(1) = "
MARKRE = re.escape(MARK) + r"\s*([-+0-9.eE]+)"


# ================================================================================================ child: one lane, one kernel
def child(lane, kern, outdir):
    sys.path.insert(0, LANES)
    import numpy as np
    import CFG7_common as C
    import CFG4_common as C4
    nu = C4.nu_mono
    assert C.nu_mono is nu and C4.KERNELS["nu_mono"] is nu
    sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
    import hunt_lib as HL
    import k_contrarian_dwarfefe as KD
    nu1_mono = float(nu(np.array([1.0]))[0]); nu1_p2 = float(C.nu_p2(np.array([1.0]))[0])
    CALLS = [0]
    body = {"p2": "def _cfg64_k(y):\n    import numpy as _np\n    _CFG64_CALLS[0] += 1\n    y = _np.maximum(_np.asarray(y, float), 1e-300)\n    return _np.sqrt(1.0 + 1.0 / y)\n",
            "newton": "def _cfg64_k(y):\n    import numpy as _np\n    _CFG64_CALLS[0] += 1\n    return _np.ones_like(_np.asarray(y, float))\n"}
    swapped = []
    if kern != "mono":
        for lab, f in (("CFG4_common.nu_mono", nu), ("hunt_lib.nu", HL.nu), ("hunt_lib.nu_s", HL.nu_s), ("k_contrarian_dwarfefe.nu", KD.nu)):
            ns_ = f.__globals__
            ns_["_CFG64_CALLS"] = CALLS
            exec(body[kern], ns_)
            f.__code__ = ns_["_cfg64_k"].__code__
            swapped.append(lab)
    swapped_codes = {f.__code__ for f in (nu, HL.nu, HL.nu_s, KD.nu)} if kern != "mono" else set()
    if kern != "mono":
        _orig_es = C4.exec_slices

        def _es(*a, **k):                                                   # L23's own nu (fable_independent_2026/L23_udg_verify.py) appears only inside exec'd namespaces
            res = _orig_es(*a, **k)
            f = res[0].get("nu")
            if callable(f) and getattr(f, "__code__", None) is not None and f.__code__.co_filename.endswith("L23_udg_verify.py") and f.__code__ not in swapped_codes:
                f.__globals__["_CFG64_CALLS"] = CALLS
                exec(body[kern], f.__globals__)
                f.__code__ = f.__globals__["_cfg64_k"].__code__
                swapped_codes.add(f.__code__); swapped.append("L23_udg_verify.nu (exec'd)")
            return res
        C4.exec_slices = _es
    nu1_after = float(nu(np.array([1.0]))[0])
    os.makedirs(outdir, exist_ok=True)
    orig = C.Report.write
    C.Report.write = lambda self, here=None: orig(self, here=outdir)
    src = open(os.path.join(LANES, lane + ".py")).read()
    key = "import CFG7_common as C\n"
    assert src.count(key) == 1
    marker = f'print("{MARK}", float(C.nu_mono(__import__("numpy").array([1.0]))[0]), flush=True)  # CFG64: kernel swapped before this point\n'
    cp = os.path.join(HERE, "lane_copies", f"{lane}__{kern}.py")
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    text = src.replace(key, key + marker)
    open(cp, "w").write(text)
    g = {"__file__": os.path.join(LANES, lane + ".py"), "__name__": "__main__"}
    rc, err = None, None
    try:
        exec(compile(text, cp, "exec"), g)
        rc = 0
    except SystemExit as e:
        rc = int(e.code or 0)
    except BaseException as e:                                   # a crash under an absurd kernel is data
        import traceback
        rc, err = -1, traceback.format_exc()
    import gc, types
    leaks = []
    for o in gc.get_objects():
        if isinstance(o, types.FunctionType) and o.__code__ not in swapped_codes:
            nm = set(o.__code__.co_names)
            if "sqrt" in nm and ("exp" in nm or "expm1" in nm) and o.__module__ not in ("scipy", "numpy"):
                fl = o.__code__.co_filename
                if "site-packages" not in fl and "/Library/" not in fl:
                    leaks.append(f"{os.path.basename(fl)}:{o.__code__.co_firstlineno} {o.__qualname__}")
    json.dump(dict(rc=rc, err=err, nu1_mono=nu1_mono, nu1_p2=nu1_p2, nu1_after=nu1_after, calls=CALLS[0], swapped=swapped, leaks=sorted(set(leaks))),
              open(os.path.join(outdir, "status.json"), "w"))
    sys.exit(0)


if len(sys.argv) > 1 and sys.argv[1] == "--child":
    child(sys.argv[2], sys.argv[3], sys.argv[4])

# ================================================================================================ parent
sys.path.insert(0, LANES)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
ALT = "newton" if MUTATE else "p2"
R = C.Report("cfg64_kernel_robustness", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the alternative kernel is the absurd Newtonian nu = 1 for every lane -- H1 must FAIL ***")


def run_one(job):
    lane, kern = job
    out = os.path.join(HERE, "runs", f"{lane}__{kern}" + ("__MUT" if MUTATE else ""))
    if os.path.isdir(out):
        for f in os.listdir(out):
            os.remove(os.path.join(out, f))
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, MUTATE="0", PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--child", lane, kern, out], env=env, capture_output=True, text=True, timeout=1500)
    open(os.path.join(out, "stdout.txt"), "w").write(p.stdout); open(os.path.join(out, "stderr.txt"), "w").write(p.stderr)
    st = json.load(open(os.path.join(out, "status.json"))) if os.path.exists(os.path.join(out, "status.json")) else dict(rc=None, err=p.stderr[-2000:], calls=0)
    resp = os.path.join(out, lane + "_results.json")
    res = json.load(open(resp)) if os.path.exists(resp) else None
    m = re.search(MARKRE, p.stdout)
    st["marker_nu1"] = float(m.group(1)) if m else None
    st["seconds"] = round(time.time() - t0, 1)
    return (lane, kern), dict(st=st, res=res, out=out)


jobs = [(l, k) for k in ("mono", "p2", "newton") for l in NAMES]
P(f"\n  running {len(jobs)} lane copies (nu_mono, P2, Newtonian nu = 1; 9 lanes each) in 6 worker processes; the alternative kernel scored by H1 is {ALT} ...")
with ThreadPoolExecutor(6) as ex:
    RUN = dict(ex.map(run_one, jobs))
P(f"  done ({sum(v['st']['seconds'] for v in RUN.values()):.0f} s of lane time)")

TOK = re.compile(r"[+-]?\d+\.\d+(?:e[+-]?\d+)?")


def tokens(detail, skip=False):
    out = []
    if skip:
        return out
    for m in TOK.finditer(detail):
        tk = m.group(0)
        before, after = detail[max(0, m.start() - 3):m.start()], detail[m.end():m.end() + 30]
        if "e" in tk.lower() or before.endswith("> ") or after.startswith("?)") or detail[max(0, m.start() - 11):m.start()] == "phi_needed ":
            continue
        sig = bool(re.match(r"(?:/[+-]?\d+\.\d+)*\)?\s*sigma", after)) or (detail[max(0, m.start() - 1):m.start()] == "(" and after.startswith(")")) or (detail[max(0, m.start() - 1):m.start()] == "(" and after.startswith(" sigma"))
        out.append(("sigma" if sig else "dex", float(tk)))
    return out


def masked(detail):
    return TOK.sub("#", detail)


def hrows(res):
    return {c["name"].split()[0]: c for c in res["checks"] if re.match(r"H\d", c["name"])}


def altrows(res):
    return {c["name"].split()[0]: c for c in res["checks"] if not re.match(r"H\d", c["name"]) and "alt footing" in c["name"].lower()}


def classify(lane, rid, cm, ca):
    """cm, ca: the nu_mono and alternative-kernel check dicts for one row."""
    flip = cm["ok"] != ca["ok"]
    emb = (lane, rid) in EMBEDDED
    txtflip = emb and masked(cm["detail"]) != masked(ca["detail"])
    sk = (lane, rid) in NUM_SKIP
    tm, ta = tokens(cm["detail"], sk), tokens(ca["detail"], sk)
    mis = len(tm) != len(ta)
    dd = ds = 0.0
    pairs = []
    if not mis:
        for (rm, vm), (ra, va) in zip(tm, ta):
            pairs.append((rm, vm, va))
            if rm == "dex":
                dd = max(dd, abs(va - vm))
            else:
                ds = max(ds, abs(va - vm))
    off = (dd > DEX_TOL) or (ds > SIG_TOL)
    return dict(flip=bool(flip or txtflip), off=bool(off), misaligned=bool(mis), max_ddex=dd, max_dsig=ds, ok_mono=cm["ok"], ok_alt=ca["ok"],
                sensitive=bool(flip or txtflip or off), pairs=pairs, det_mono=cm["detail"], det_alt=ca["detail"])


# ---------------------------------------------------------------------------------------------- C1
R.banner("C1  the nu_mono copies reproduce the committed lanes")
dev = []
for lane in NAMES:
    r = RUN[(lane, "mono")]["res"]
    com = json.load(open(os.path.join(LANES, lane + "_results.json")))
    if r is None:
        dev.append(f"{lane}: no result"); continue
    a = [(c["name"], c["ok"], c["detail"]) for c in r["checks"]]; b = [(c["name"], c["ok"], c["detail"]) for c in com["checks"]]
    if a != b:
        bad = [x[0][:30] for x, y in zip(a, b) if x != y] + (["length"] if len(a) != len(b) else [])
        dev.append(f"{lane}: {bad[:3]}")
check("C1 CONTROL: the nu_mono copies reproduce every committed lane result exactly (check names, ok flags, detail strings)",
      "all 9 lanes identical" if not dev else "; ".join(dev), not dev)

# ---------------------------------------------------------------------------------------------- C2
R.banner("C2  the swap plumbing")
kv = RUN[(NAMES[0], "mono")]["st"]
nu1_mono, nu1_p2 = kv["nu1_mono"], kv["nu1_p2"]
P(f"  nu_mono(1) = {nu1_mono:.6f}   nu_p2(1) = {nu1_p2:.6f}   (sqrt 2 = {math.sqrt(2):.6f})   difference {abs(nu1_mono - nu1_p2):.4f}")
plumb = []
for kk, target in (("p2", math.sqrt(2)), ("newton", 1.0)):
    for lane in NAMES:
        s_ = RUN[(lane, kk)]["st"]
        plumb.append((lane, kk, s_.get("nu1_after"), s_.get("marker_nu1"), s_.get("calls", 0), s_.get("rc"), RUN[(lane, kk)]["res"] is not None, target))
        P(f"  {kk:6s} {lane:34s} nu(1) after swap {s_.get('nu1_after')}   marker in the lane copy {s_.get('marker_nu1')}   swapped-kernel calls {s_.get('calls')}   rc {s_.get('rc')}   results written {RUN[(lane, kk)]['res'] is not None}   swapped: {len(s_.get('swapped', []))} functions")
mono_ok = all(RUN[(l, "mono")]["st"].get("marker_nu1") is not None and abs(RUN[(l, "mono")]["st"]["marker_nu1"] - nu1_mono) < 1e-12 for l in NAMES)
c2 = (abs(nu1_mono - nu1_p2) > 0.01) and mono_ok and all(x[2] is not None and abs(x[2] - x[7]) < 1e-12 and x[3] is not None and abs(x[3] - x[7]) < 1e-12 for x in plumb) \
    and all(x[4] > 10 for x in plumb if x[0] != "CFG51_walker_ufd") and all(x[6] for x in plumb if x[1] == "p2")
check("C2 CONTROL: nu_p2(1) != nu_mono(1); after the swap nu(1) is the alternative's in every child (also as printed inside the lane copy); the swapped kernel was called > 10 times in every lane (CFG51 exempt from the count: it is a 4-galaxy lane); every P2 child wrote results (Newtonian crashes are reported as NOT RUN)",
      f"nu_mono(1) {nu1_mono:.5f}, nu_p2(1) {nu1_p2:.5f}; min calls (P2) {min(x[4] for x in plumb if x[1] == 'p2')}; lanes with results (P2/Newton): {sum(x[6] for x in plumb if x[1] == 'p2')}/9, {sum(x[6] for x in plumb if x[1] == 'newton')}/9", c2)

# nu_RAR versus nu_mono in the regime of the FG001-derived lanes (reported)
import numpy as _np
_y = _np.logspace(-4, -1, 7)
_rel = float(_np.max(_np.abs(C.C4.nu_rar(_y) / C.nu_mono(_y) - 1.0)))
_relhi = float(_np.max(_np.abs(C.C4.nu_rar(_np.logspace(-1, 1.5, 12)) / C.nu_mono(_np.logspace(-1, 1.5, 12)) - 1.0)))
check("R0 (reported) nu_RAR (what hunt_lib.nu_s / k_contrarian.nu compute) against nu_mono: max |ratio - 1| over y = 1e-4..0.1 and over y = 0.1..30",
      f"{_rel:.2e} (ultra-faint regime); {_relhi:.2e} (y up to 30)", True, load_bearing=False)

# ---------------------------------------------------------------------------------------------- classification
def analyse(altk, verbose):
    rows, notrun = {}, []
    for lane in NAMES:
        rm, ra = RUN[(lane, "mono")]["res"], RUN[(lane, altk)]["res"]
        if rm is None or ra is None:
            notrun.append(lane); continue
        hm, ha = hrows(rm), hrows(ra)
        for rid in hm:
            if rid not in ha:
                rows[(lane, rid)] = dict(sensitive=True, flip=True, off=False, misaligned=False, max_ddex=0, max_dsig=0, ok_mono=hm[rid]["ok"], ok_alt=None, pairs=[], det_mono=hm[rid]["detail"], det_alt="(row absent)", kind="H"); continue
            d = classify(lane, rid, hm[rid], ha[rid]); d["kind"] = "H"; rows[(lane, rid)] = d
        am, aa = altrows(rm), altrows(ra)
        for rid in am:
            if rid in aa:
                d = classify(lane, rid, am[rid], aa[rid]); d["kind"] = "altR"; rows[(lane, rid)] = d
        if verbose:
            P(f"\n  {lane}  (headline {HEADLINE[lane]})")
            for (l2, rid), d in rows.items():
                if l2 != lane:
                    continue
                lab = "SENSITIVE" if d["sensitive"] else "ROBUST"
                why = ("verdict FLIP " if d["flip"] else "") + ("offset " if d["off"] else "") + ("MISALIGNED " if d["misaligned"] else "")
                hd = "  [HEADLINE]" if (d["kind"] == "H" and rid == HEADLINE[lane]) else ""
                P(f"    {rid:3s} ({d['kind']}) {'PASS' if d['ok_mono'] else 'FAIL'} -> {'PASS' if d['ok_alt'] else 'FAIL'}  max d(dex) {d['max_ddex']:.3f}  max d(sigma) {d['max_dsig']:.2f}  {lab}{hd} {why}")
                P(f"         mono: {d['det_mono'][:230]}")
                P(f"         alt : {d['det_alt'][:230]}")
    hs = {l: (rows[(l, HEADLINE[l])]["sensitive"] if (l, HEADLINE[l]) in rows else None) for l in NAMES}
    return rows, notrun, hs


def summary(altk, rows, notrun, hs):
    allsens = [(l, r) for (l, r), d in rows.items() if d["kind"] == "H" and d["sensitive"]]
    altsens = [(l, r) for (l, r), d in rows.items() if d["kind"] == "altR" and d["sensitive"]]
    flips = [(l, r) for (l, r), d in rows.items() if d["flip"]]
    for l in NAMES:
        h = hs[l]
        P(f"  {l:34s} headline {HEADLINE[l]}: " + ("NOT RUN" if h is None else ("KERNEL-SENSITIVE" if h else "KERNEL-ROBUST")))
    P(f"  sensitive hypotheses (H rows): {allsens}")
    P(f"  sensitive alt-footing companion rows: {altsens}")
    P(f"  pass/fail flips (any row): {flips}")
    if notrun:
        P(f"  NOT RUN under this kernel (no results): {notrun}")
    return allsens, altsens, flips


R.banner(f"CLASSIFICATION  nu_mono versus {'the Newtonian nu = 1' if MUTATE else 'P2'} (every declared hypothesis; alt-footing companions)")
ROWS, NOTRUN, head_sens = analyse(ALT, True)
R.banner("SUMMARY under " + ALT)
allsens, altsens, flips_alt = summary(ALT, ROWS, NOTRUN, head_sens)
OTHER = "p2" if MUTATE else "newton"
R.banner(f"REFERENCE: the same classification under the other kernel ({OTHER}), summary only")
ROWS_O, NOTRUN_O, head_sens_O = analyse(OTHER, False)
allsens_O, altsens_O, flips_O = summary(OTHER, ROWS_O, NOTRUN_O, head_sens_O)

# ---------------------------------------------------------------------------------------------- G1
R.banner("G1  the swap has bite")
bite = {}
for lane in NAMES:
    rm, ra = RUN[(lane, "mono")]["res"], RUN[(lane, ALT)]["res"]
    if rm is None and ra is None:
        bite[lane] = None; continue
    if ra is None:                                                          # crashed under the alternative kernel: the swap changed the run (post-run scope correction, disclosed)
        bite[lane] = float("inf"); P(f"  {lane:34s} crashed under the alternative kernel (counts as bite)"); continue
    mx = 0.0
    for cm, ca in zip(rm["checks"], ra["checks"]):
        tm = [float(x) for x in TOK.findall(cm["detail"])]; ta = [float(x) for x in TOK.findall(ca["detail"])]
        if len(tm) == len(ta):
            mx = max([mx] + [abs(a - b) for a, b in zip(tm, ta)])
        elif tm != ta:
            mx = max(mx, 1.0)
    bite[lane] = mx
    P(f"  {lane:34s} largest token change between the two kernels: {mx:.4g}")
check("G1 GATE: the swap has bite -- in every lane at least one decimal token differs between nu_mono and the alternative kernel by > 1e-6",
      "; ".join(f"{k[:6]} {('%.3g' % v) if v is not None else 'NOT RUN'}" for k, v in bite.items()), all(v is not None and v > 1e-6 for v in bite.values()))

# ---------------------------------------------------------------------------------------------- C3 / C3b
R.banner("C3  the absurd kernel")
ln = "CFG41_massive_spirals_hi"
rn = RUN[(ln, "newton")]["res"]; sn = RUN[(ln, "newton")]["st"]
h0 = hrows(RUN[(ln, "mono")]["res"])["H2"]; h1 = hrows(rn)["H2"] if rn else None
check("C3 CONTROL (declared before the first run): with nu = 1 (Newtonian) CFG41's headline H2 flips PASS -> FAIL",
      f"nu_mono: {'PASS' if h0['ok'] else 'FAIL'}; Newtonian: " + (f"{'PASS' if h1['ok'] else 'FAIL'} ({h1['detail'][:150]}); nu(1) printed in the copy {sn['marker_nu1']}; calls {sn['calls']}" if rn else "crashed"),
      h0["ok"] and (rn is None or not h1["ok"]) and sn["marker_nu1"] == 1.0)
ROWS_N, NOTRUN_N, head_N = (ROWS, NOTRUN, head_sens) if MUTATE else (ROWS_O, NOTRUN_O, head_sens_O)
flipped = [l for l in NAMES if (l, HEADLINE[l]) in ROWS_N and ROWS_N[(l, HEADLINE[l])]["flip"]]
check("C3b CONTROL (added after the first run, disclosed): with nu = 1 in all nine lanes at least one HEADLINE verdict flips its pass/fail",
      f"headlines flipped under nu = 1: {[(l[:6], HEADLINE[l]) for l in flipped] or 'none'}; lanes not run: {NOTRUN_N or 'none'}", len(flipped) >= 1)

# ---------------------------------------------------------------------------------------------- residual leak audit
R.banner("R1  residual-leak audit: RAR-form functions alive after each P2 lane that were NOT swapped")
allleaks = {}
for lane in NAMES:
    lk = RUN[(lane, "p2")]["st"].get("leaks", [])
    allleaks[lane] = lk
    P(f"  {lane:34s} {lk if lk else 'none'}")
check("R1 (reported) residual RAR-form functions after the P2 runs (not swapped; each is inspected in the README)", "; ".join(f"{k[:6]}: {len(v)}" for k, v in allleaks.items()), True, load_bearing=False)

# ---------------------------------------------------------------------------------------------- headline verdict table
R.banner("HEADLINES AND HYPOTHESES")
lane_sens = {l: any(d["sensitive"] for (l2, r), d in ROWS.items() if l2 == l) for l in NAMES if l not in NOTRUN}
P("  lane-level (" + ALT + "): " + "; ".join(f"{l[:6]} {'SENSITIVE' if v else 'ROBUST'}" for l, v in lane_sens.items()))
check("H1 [HEADLINE] EVERY HEADLINE VERDICT IS KERNEL-ROBUST: the nine headline hypotheses keep their pass/fail and move by <= 0.05 dex and <= 1 sigma" + ("  [MUTATE: alt kernel = Newtonian]" if MUTATE else ""),
      "; ".join(f"{l[:6]} {HEADLINE[l]} " + ("NOT RUN" if head_sens[l] is None else ("SENSITIVE" if head_sens[l] else "robust")) for l in NAMES),
      all(v is False for v in head_sens.values()))
check("H2 (reported) every declared hypothesis of the nine lanes is KERNEL-ROBUST (alt-footing companion rows included)",
      f"sensitive hypotheses: {allsens or 'none'}; sensitive alt-footing companions: {altsens or 'none'}", not allsens and not altsens, load_bearing=False)

R.num("kernel_nu1", dict(nu_mono=nu1_mono, nu_p2=nu1_p2))
R.num("alt_kernel", ALT)
R.num("rows", {f"{l}|{r}": {k: v for k, v in d.items() if k not in ("det_mono", "det_alt")} | dict(det_mono=d["det_mono"][:400], det_alt=d["det_alt"][:400]) for (l, r), d in ROWS.items()})
R.num("rows_other_kernel", {f"{l}|{r}": dict(flip=d["flip"], off=d["off"], sensitive=d["sensitive"], max_ddex=d["max_ddex"], max_dsig=d["max_dsig"], ok_mono=d["ok_mono"], ok_alt=d["ok_alt"]) for (l, r), d in ROWS_O.items()}); R.num("headline_sensitive_other", head_sens_O); R.num("leaks", allleaks); R.num("headline_sensitive", head_sens); R.num("lane_sensitive", lane_sens); R.num("not_run", NOTRUN)
R.num("run_status", {f"{l}|{k}": v["st"] for (l, k), v in RUN.items()})
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
