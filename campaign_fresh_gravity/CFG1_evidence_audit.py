#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG1 -- THE EVIDENCE AUDIT.  Every empirical result the fresh-gravity campaign must answer, how it was measured, the model
assumptions built into its pipeline, how far a framework-consistent but physically defensible treatment could move it (the
SAME treatment applied to LCDM's use of the same data), and a class for each.  Then the record's own "equipment": the
computational approximations that decided or bent past verdicts, with their status and commits.  Then the framework's OWN
empirical results, audited the same way (the author's rule 0, relayed 2026-09-27).  It ends with the requirements list.

THE BASE.  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED and not derived (Z = kappa-form = 2 sqrt(8 pi/3) = 5.7888, never ~21);
both footings everywhere a0 enters: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (read from FP0's committed results).  Nothing
here says the theory is closed.  The dark component, where one is needed, is the framework's own field, and a mass is still
required.

METHOD.
  * Numbers are READ from committed result files (git-tracked and unmodified; each file's sha256 is recorded) or COMPUTED here
    from committed machinery re-executed read-only (FP18's pincer, FP20's projectors, XR26's lensing Limber and band powers, FP6's
    linear spectrum and kernel).  Published values not on disk are cited in the row that uses them.
  * Numbers from lanes still in flight (uncommitted when this lane ran: XR34, FP24, XR35, XR24, XR28) are quoted as PENDING and never
    decide a class; this script records whether each is committed at run time.  FP22 (bfe9a2fe5), FP20b (3924bb8c2), XR32 (fa341733d)
    and XR18b (3c0cf3c37) were committed while this lane was being written; they are cited by commit (XR32 carries the hub's
    "re-run pending" flag).
  * Every shift is applied to the DATA, through one function (`seen`), so the framework and LCDM are scored against the same
    shifted data; LCDM's pull at the shift the framework needs is printed beside it.

THE CLASS RULE (declared before the first full run; applied mechanically in `classify`).
  1. CONTESTED if at least two published analyses (or the record's own independent analyses) of the same observable disagree by
     more than their combined quoted uncertainties; the disagreement is printed.
  2. Otherwise the STAKE is computed.  For a record FAIL: the favourable data shift that brings the framework's MOST FAVOURABLE
     scored variant (either construction -- M* or the derivation chain -- and either footing) to the record's own gate; a failure
     is only called model-independent if it survives for the variant most charitable to the framework.  For a record PASS: the
     unfavourable shift that would push its LEAST favourable variant over the gate.  Where no verdict is scored, the stake is the
     smallest discrepancy the campaign's gates register (stated per row).
  3. The BUDGET is the documented data-side systematics (published budgets or the record's committed machinery), each at its edge
     in the relevant direction, combined in quadrature ("defensible"); the aligned corner (linear sum) is printed beside it.
  4. SOFT if BUDGET >= STAKE, MODEL-INDEPENDENT otherwise.  The class is a property of the result at the level at stake; it says
     nothing about whether the framework is right.
  5. (Clarified after the development run, before the recorded runs; disclosed.)  If a record FAIL's most favourable variant already
     lies inside the gate, the FAIL is not established for that variant; the stake is then that variant's margin to the gate (the
     shift that would make it fail), as for a PASS.  Where LCDM's number is a per-object fit (a halo mass fitted to each object), it
     refits under any shift, so no LCDM pull at a shifted datum is printed for it.

PRE-DECLARED HYPOTHESES (written before the first full run; scored in section H, kept as run).
  H1  the three controls reproduce FP18's pincer (T 102.0 face value, 7.50 profiled), FP20's projector errors and XR26's Planck
      lensing amplitude (1.1492 linear / 2.1344 halofit, f* 0.618 / 0.178) exactly (relative deviation <= 1e-9).
  H2  MODEL-INDEPENDENT includes at least: the Solar-System quadrupole, GW speed, BBN (Y_P, D/H), the CMB primary spectra, the CMB
      lensing amplitude (data side), BAO, the RAR's shape, the cluster mass beyond MOND and the Bullet offsets.
  H3  the Local Group row: the R0 measurement is at least SOFT at the pincer level (FP18: 9.8 -> 2.3 sigma), and the chain's own
      R0 overshoot stays >= 2 sigma with FP18's honest errors.
  H4  at least two of the three external-field samples (cluster-infall BTFR slope, LV-dwarf statistic C, Coma UDGs) are
      MODEL-INDEPENDENT: their documented data-side systematics cannot bring even the most favourable variant to 2 sigma.
  H5  the CMB-lensing FAIL is equipment-dependent in magnitude: with XR21's real-space box numbers mapped onto XR26's committed
      A(f), the linear-base amplitude in the baryons-only reading lies within 2 sigma of Planck 2018 (8-400), while the
      all-matter reading fails on the halofit base at every mapped factor.
  H6  X-COP (FP16's too-much-mass failure) is SOFT: the hydrostatic/non-thermal bias it needs lies inside the published range
      (<= 0.2) but above X-COP's own 6%.
  H7  SLACS is CONTESTED (the published IMF methods disagree by more than the shift the framework needs).
  H8  the forest: DE11b's pass survives the kernel-argument factor estimated from FP6's own kernel (worst <= 0.02 against 0.10),
      and the chain's linear forest proxies are not established.
  H9  the fairness check passes in the main run and FAILS in the MUTATE run.
  H10 the framework's own results: the SN-Ia host step is MODEL-INDEPENDENT as a step with its a0 attribution untested; the
      environmental null is MODEL-INDEPENDENT; kappa is SOFT; flat a0(z) is CONTESTED; the directional EFE, the comet anisotropy,
      the vertical force and the forest b-cutoff are SOFT or CONTESTED, none MODEL-INDEPENDENT.

CHECKS
  K1  CONTROL: FP18's pincer re-executed read-only (its own main() body, its own module namespace, up to the profiled statistic):
      T_nominal (stack + LG, honest errors) and T_profiled equal the committed values.
  K2  CONTROL: FP20's projector audit (its own source through its V section, file writes refused): every projector error equals
      the committed table.
  K3  CONTROL: XR26's CMB-lensing pipeline (header, K and L sections of its own source; patched-CLASS build and C section skipped;
      output paths neutralised): the Planck 2018 8-400 amplitude (linear and halofit) and the phantom budget f* equal the committed.
  K4  every committed source the ledger reads is git-tracked and unmodified (sha256 recorded); in-flight sources are labelled.
  K5  every commit the ledger cites exists.
  K6  the footings (FP0) and Z.
  A   the ledger rows (Part A); O the framework's own results; B the equipment audit (Part B); N the verdicts not established.
  F1  [load-bearing; MUTATE must fail] FAIRNESS: for every shifted row, the framework and LCDM were scored against identical data.
  F2  [load-bearing] every SOFT row carries a quantified budget, its source, and LCDM's pull at the shift.
  F3  [load-bearing] every row has a class, a measurement description, assumptions and at least one citation.
  H1-H10 the pre-declared hypotheses, scored (reported).
MUTATE=1: the audit's scoring applies every systematic to the FRAMEWORK'S comparison only (LCDM keeps the unshifted data) -- the
special pleading rule 3 of the charter forbids.  F1 must FAIL (rc = 1).  Outputs *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  An audit, not a new model: no construction is scored here beyond what the record has scored; every "shift" is on the data
side, and every theory-side ambiguity (EFE form, reading, yardstick) is reported as equipment or as a variant, never as a data
systematic.  At most 2 threads (BLAS 1; CLASS's OpenMP 2 inside XR26's re-execution); a few minutes.

DISCLOSURES.  Exploratory runs (scratch, not committed) preceded the first full run: three prototypes of the controls (FP20's V
section, FP18's main body, XR26's K/L sections) confirmed exact reproduction (0.0 pp; 101.967/7.4974; 1.149178110466443 /
2.1343605455837484); one XR26 prototype was stopped early so that two jobs would not exceed the 2-thread cap.  A read-only search
agent located the own-results' committed scripts; every number used from its report was re-read at source before use.  Development
runs of this script (outputs to scratch via CFG1_OUTDIR, never to the lane folder) preceded the recorded runs.  The first one showed:
(i) `classify` returned MODEL-INDEPENDENT for a zero stake, contradicting rule 4 (fixed); (ii) rule 5 was needed where a record FAIL's
most favourable variant already passes (X-COP's canonical turned-around-web cell, CMB lensing's baryons-only linear base); (iii) the
CMB-lensing budget had used the Planck-ACT difference's uncertainty (0.036) instead of the measured difference (0.002); (iv) LCDM pulls
were printed for per-object fits (Coma UDGs, the MW census, the LG's fitted halo), which refit under any shift.  The hypotheses were not
changed; H6 had already fallen in that run and falls again here (the most favourable X-COP cell needs no bias at all).

Run from the repository root:  MUTATE=1 python3 campaign_fresh_gravity/CFG1_evidence_audit.py ; python3 campaign_fresh_gravity/CFG1_evidence_audit.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, io, re, json, math, time, hashlib, builtins, contextlib, subprocess, inspect, textwrap, warnings
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
XR = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "CFG1_evidence_audit"
OUTDIR = os.environ.get("CFG1_OUTDIR") or HERE                        # development runs only; the record's runs use the lane folder
TXT = os.path.join(OUTDIR, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(OUTDIR, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T0 = time.time()
LINES = []
CH = []
OUT = {"lane": "CFG1", "mutate": MUTATE, "checks": {}, "numbers": {}, "sources": {}, "pending": {}, "ledger": [], "own": [],
       "equipment": [], "not_established": [], "requirements": {}, "hypotheses": {}}


def P(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(cid, name, measured, ok, load_bearing=True, reading=""):
    ok = bool(ok)
    CH.append((cid, ok, load_bearing))
    OUT["checks"][cid] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {cid} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return [jclean(v) for v in o.tolist()]
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


def git(*args):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG1 refuses to write {file!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
    """MUTATE=0 while a record lane is re-executed (the lanes read it), its stdout captured, the thread settings restored."""
    keep = {k: os.environ.get(k) for k in ("MUTATE", "FP20_SECTIONS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                           "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS")}
    os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    out0 = sys.stdout
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        sys.stdout = out0
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


SOURCES = {}


def src(rel):
    """register a committed source the ledger reads; returns its absolute path."""
    SOURCES[rel] = None
    return os.path.join(REPO, rel)


def jload(rel):
    return json.load(open(src(rel)))


def text(rel):
    return open(src(rel)).read()


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every systematic is applied to the FRAMEWORK'S comparison only; LCDM keeps the unshifted data.  "
      "F1 (fairness) must FAIL, rc = 1 ***")

# ====================================================================================================================== K6 footings
banner("K  CONTROLS: the footings; FP18's pincer; FP20's projectors; XR26's CMB lensing; the sources; the commits")
FP0 = jload("real_research/derivation_chain_2026/FP0_core_postulates_results.json")["numbers"]
A0 = {"canonical": float(FP0["a0_canonical"]), "alt": float(FP0["a0_rho_total"])}
ZK = 2 * math.sqrt(8 * math.pi / 3)
check("K6", "THE FOOTINGS AND Z: FP0's committed a0 values are the charter's 9.3603e-11 / 1.1312e-10 m/s^2 (to 1e-4); Z = 2 sqrt(8 pi/3) = "
      "5.7888 (kappa = 1/2 FITTED, the same number)", f"a0 canonical {A0['canonical']:.5e}, alt {A0['alt']:.5e}; Z = {ZK:.4f}",
      abs(A0["canonical"] / 9.3603e-11 - 1) < 1e-4 and abs(A0["alt"] / 1.1312e-10 - 1) < 1e-4 and abs(ZK - 5.7888) < 5e-5)
OUT["numbers"]["footings"] = dict(a0=A0, Z=ZK, kappa="1/2 FITTED")

# ====================================================================================================================== K1 FP18
tK = time.time()
with lane_env():
    sys.path.insert(0, CHAIN)
    import FP18_kids_vs_hubble_flow_data as F18
    _b = inspect.getsource(F18.main).split("\n", 1)[1]
    _b = textwrap.dedent(_b[:_b.index('    PROFI = profile(("stack", "LG"), full=True, infl=INFL)')])
    exec(compile(_b, F18.__file__, "exec"), F18.__dict__)
N18 = F18.__dict__
R18 = jload("real_research/derivation_chain_2026/FP18_kids_vs_hubble_flow_data_results.json")["numbers"]
t_nom = float(N18["Tj_nom"])
t_nom_c = R18["F1"]["stack/i"]["honest"]["T"] + R18["F1"]["LG/i"]["honest"]["T"]
t_pro = float(N18["PROF"]["T"])
t_pro_c = R18["S"]["profiled"]["T"]
dx18 = max(abs(a - b) for a, b in zip(N18["PROF"]["x"], R18["S"]["profiled"]["x"]))
check("K1", "CONTROL -- FP18'S PINCER, RE-EXECUTED READ-ONLY: T_nominal (stack + LG, honest R0 errors, free profile) and the profiled T "
      "(six comparability systematics under their priors) equal FP18's committed values, and so do the profiled nuisances",
      f"T_nominal {t_nom:.6f} vs {t_nom_c:.6f}; T_profiled {t_pro:.6f} vs {t_pro_c:.6f}; max |d nuisance| {dx18:.1e} ({time.time() - tK:.0f} s)",
      abs(t_nom / t_nom_c - 1) < 1e-9 and abs(t_pro / t_pro_c - 1) < 1e-9 and dx18 < 1e-9)
OUT["numbers"]["K1"] = dict(T_nominal=t_nom, T_profiled=t_pro, committed=[t_nom_c, t_pro_c])

# ====================================================================================================================== K2 FP20
tK = time.time()
_p20 = os.path.join(CHAIN, "FP20_esd_projection_fix.py")
_s20 = open(_p20).read()
_i = _s20.index("B  the anatomy of the bug")
_s20 = _s20[:_s20.rfind("\n", 0, _i) + 1]
N20 = {"__file__": _p20, "__name__": "fp20_readonly", "open": ro_open}
with lane_env():
    os.environ["FP20_SECTIONS"] = "V"
    exec(compile(_s20, _p20, "exec"), N20)
R20 = jload("real_research/derivation_chain_2026/FP20_esd_projection_fix_results.json")["numbers"]
_new, _ref = N20["OUT"]["numbers"]["V_errors_percent"], R20["V_errors_percent"]
d20 = max(float(np.max(np.abs(np.array(_ref[a][b]) - np.array(_new[a][b])))) for a in _ref for b in _ref[a])
sis35 = _new["SIS V=200"]["P1 committed (FP6/FP1/L355, point)"][0]
check("K2", "CONTROL -- FP20'S PROJECTOR AUDIT, RE-EXECUTED READ-ONLY: every projector's error against the analytic profiles (SIS, "
      "three NFW, point masses, the chain's phantom, the carrier templates) at the 15 KiDS radii equals FP20's committed table",
      f"max |d| over {sum(len(v) for v in _ref.values())} projector rows {d20:.1e} pp; esd_of_M on the SIS at 35 kpc {sis35:+.2f}% "
      f"({time.time() - tK:.0f} s)", d20 < 1e-9 and abs(sis35 + 58.5558) < 1e-3)
OUT["numbers"]["K2"] = dict(max_dev_pp=d20, sis_35kpc_percent=sis35)

# ====================================================================================================================== K3 XR26
tK = time.time()
_p26 = os.path.join(XR, "XR26_cmb.py")
_s26 = open(_p26).read()
_BAR = "# " + "=" * 96 + " "
_m_build, _m_K = _s26.index(_BAR + "the patched CLASS"), _s26.index(_BAR + "K controls")
_m_C, _m_L = _s26.index(_BAR + "C the chain at z >~ 10"), _s26.index(_BAR + "L late-time lensing")
_m_L3 = _s26.index("# L3/L4 the lensed spectra")
_head = _s26[:_m_build]
for _a, _b2 in (('TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))', "TXT = None"),
                ('JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))', "JSN = None"),
                ("TEE = _Tee(TXT)\nsys.stdout = TEE", "TEE = None")):
    assert _head.count(_a) == 1, _a
    _head = _head.replace(_a, _b2)
X26 = {"__file__": _p26, "__name__": "xr26_readonly", "open": ro_open}
with lane_env():
    exec(compile(_head, _p26, "exec"), X26)
    X26["build_ok"] = False
    exec(compile("\n" * _s26[:_m_K].count("\n") + _s26[_m_K:_m_C], _p26, "exec"), X26)
    exec(compile("\n" * _s26[:_m_L].count("\n") + _s26[_m_L:_m_L3], _p26, "exec"), X26)
R26 = jload("real_research/cross_thread_review_2026_09_26/XR26_cmb_results.json")["numbers"]
HEAD26 = X26["HEAD"]
a26 = {b: X26["L2"]["8-400"]["rows"][(HEAD26, b)]["amp"] for b in ("lin", "NL")}
a26c = {b: R26["L2"]["8-400"]["rows"][f"{HEAD26} || {b}"]["amp"] for b in ("lin", "NL")}
fs26, fs26c = X26["FSTAR"], R26["L2b"]["f_star"]
dmax26 = max([abs(a26[b] / a26c[b] - 1) for b in a26] + [abs(fs26[b] / fs26c[b] - 1) for b in fs26]
             + [abs(x / y - 1) for b in ("lin", "NL") for x, y in zip(X26["AMPS"][b], R26["L2b"]["amps"][b])])
check("K3", "CONTROL -- XR26'S CMB-LENSING PIPELINE, RE-EXECUTED READ-ONLY (CAMB + CLASS at the Planck 2018 best fit, FP13's yardstick, "
      "Limber, Planck 2018 VIII's MV band powers): the chain's 8-400 amplitude (linear and halofit bases), the phantom budget f* and the "
      "whole A(f) table equal XR26's committed numbers",
      f"amplitude lin {a26['lin']:.6f} vs {a26c['lin']:.6f}, halofit {a26['NL']:.6f} vs {a26c['NL']:.6f}; f* {fs26['lin']:.4f}/{fs26['NL']:.4f}; "
      f"max relative deviation {dmax26:.1e} ({time.time() - tK:.0f} s)", dmax26 < 1e-9)
OUT["numbers"]["K3"] = dict(amp=a26, f_star=fs26, amps=X26["AMPS"], f_grid=X26["FS"], max_rel_dev=dmax26)
P(f"    {el()}")

# ====================================================================================================================== the fairness engine
FAIR = []


def seen(rid, tag, model, shifted, unshifted):
    """THE single entry point for scoring under a systematic: both models get the SAME shifted data (MUTATE: the framework only)."""
    use = shifted if (model == "fw" or not MUTATE) else unshifted
    FAIR.append((rid, tag, model, float(use)))
    return use


def pulls_at(rid, tag, d, s, fw, lcdm, S):
    """pulls |p - (d + S)|/s for every framework variant and every LCDM variant, through `seen`."""
    dfw, dl = seen(rid, tag, "fw", d + S, d), seen(rid, tag, "lcdm", d + S, d)
    return ({k: abs(v - dfw) / s for k, v in fw.items()}, {k: abs(v - dl) / s for k, v in lcdm.items()})


def classify(contested, budget, stake):
    """the declared rule: CONTESTED if published analyses disagree; otherwise SOFT if the budget reaches the stake."""
    if contested:
        return "CONTESTED"
    if stake is None:
        return "MODEL-INDEPENDENT"
    return "SOFT" if budget >= stake else "MODEL-INDEPENDENT"


def quad(xs):
    return math.sqrt(sum(float(x) ** 2 for x in xs))


ROWS = []


def row(rid, scale, title, **kw):
    r = dict(id=rid, scale=scale, title=title)
    r.update(kw)
    ROWS.append(r)
    return r


def gauss_row(rid, scale, title, *, d, s, fw, lcdm, budget, gate=2.0, fail=True, contested=None, units="", **kw):
    """the common case: a measurement d +- s (statistical), framework variants fw, LCDM variants lcdm, a data-side budget
    {name: magnitude} (data units).  FAIL rows: stake = the favourable shift that brings the most favourable variant to the gate.
    PASS rows: stake = the unfavourable shift that pushes the least favourable variant over it."""
    pf = {k: (v - d) / s for k, v in fw.items()}
    k0 = min(pf, key=lambda k: abs(pf[k])) if fail else max(pf, key=lambda k: abs(pf[k]))
    if abs(pf[k0]) > gate:                                              # the deciding variant fails: the stake is its rescue
        mode, stake = "rescue", (abs(pf[k0]) - gate) * s
        sgn = math.copysign(1.0, fw[k0] - d)
    else:                                                               # it passes: the stake is its margin (rule 5)
        mode, stake = "margin", (gate - abs(pf[k0])) * s
        sgn = -math.copysign(1.0, fw[k0] - d) if fw[k0] != d else 1.0
    bq, bl = quad(budget.values()), sum(float(v) for v in budget.values())
    S_need = sgn * stake
    S_bud = sgn * bq
    p0f, p0l = pulls_at(rid, "face", d, s, fw, lcdm, 0.0)
    pnf, pnl = pulls_at(rid, "stake", d, s, fw, lcdm, S_need)
    pbf, pbl = pulls_at(rid, "budget", d, s, fw, lcdm, S_bud)
    cls = classify(contested, bq, stake)
    num = dict(d=d, s=s, fw=fw, lcdm=lcdm, variant=k0, mode=mode, stake=stake, budget_quad=bq, budget_corner=bl, budget=budget,
               shift_needed=S_need, pulls_face=dict(fw=p0f, lcdm=p0l), pulls_at_stake=dict(fw=pnf, lcdm=pnl),
               pulls_at_budget=dict(fw=pbf, lcdm=pbl), units=units)
    return row(rid, scale, title, cls=cls, numbers=num, contested=contested, **kw)


def rng(sv):
    """'2.35-5.30' -> (2.35, 5.30); '4.61' -> (4.61, 4.61); '2.9/2.9' -> (2.9, 2.9)."""
    v = [float(x) for x in re.findall(r"[0-9]+\.?[0-9]*", str(sv))]
    return (min(v), max(v))


def grab(pat, s, cast=float, group=1, flags=0):
    m = re.search(pat, s, flags)
    if m is None:
        raise ValueError(f"CFG1: pattern not found in a committed source: {pat!r}")
    return cast(m.group(group))


def commit_msg(h):
    return git("log", "-1", "--format=%B", h)[1]


# ====================================================================================================================== A  the ledger
banner("A  THE LEDGER (Part A): each result, how it was measured, its pipeline's assumptions, the quantified shift, the class")
XR9T = jload("real_research/cross_thread_review_2026_09_26/XR9_gate_table_results.json")["numbers"]["table"]["p1_x2.5"]
XR27N = jload("real_research/cross_thread_review_2026_09_26/XR27_gate_table_results.json")["numbers"]
X27I, X27M = XR27N["table"]["inf"], XR27N["Mstar"]

# ---- A01 the Solar System -----------------------------------------------------------------------------------------------------
f17 = text("real_research/derivation_chain_2026/FP17_screening_without_xi.out")
_m = re.search(r"measured: cumulative at v = 100: (.*?); max dev", f17)
Q2R = [float(x) for x in re.findall(r"(?:can|alt) ([0-9.]+)", _m.group(1))]
Q2_CEIL, Q2_MEAS, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
text("real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md")
gauss_row("A01", "Solar System", "Cassini light-time (gamma) and the planetary-ephemeris anomalous quadrupole Q2",
          d=Q2_MEAS, s=Q2_SIG, units="s^-2",
          fw={"strict P2 law, canonical, lowest Galactic field": Q2R[0] * Q2_CEIL, "strict P2 law, alt, highest field": Q2R[5] * Q2_CEIL},
          lcdm={"GR (no external-field quadrupole)": 0.0},
          budget={"analysis-to-analysis change of the 2-sigma ceiling (the 2026 re-analysis is 40% tighter)": 0.4 * 2 * Q2_SIG / 0.6},
          measured="Cassini 2002 conjunction Doppler (gamma - 1 = (2.1 +- 2.3)e-5) and Cassini/planetary ranging in the INPOP/DE "
                   "ephemeris fits (Q2 = (1.6 +- 1.8)e-27 s^-2, 2-sigma ceiling 5.2e-27 used as FP17's gate)",
          cite=["Bertotti, Iess & Tortora 2003, Nature 425, 374", "Hees et al. 2014, PRD 89, 102002",
                "Desmond, Hees & Famaey 2024, MNRAS 530, 1781", "arXiv:2602.17884 (as transcribed in real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md)"],
          assumptions=["GR + PPN ephemeris model; asteroid-belt and trans-Neptunian mass models", "solar J2 and Lense-Thirring terms",
                       "Cassini plasma and tracking calibration", "the anomaly is modelled as a static quadrupole aligned with the Galactic centre"],
          fw_standing=f"the strict law (no screening) gives Q2 = {Q2R[0]:.2f}-{Q2R[5]:.2f} x the ceiling (FP17 K3, FP14 X5); it passes only with the "
                      "heat-filter length xi >= 0.0243/0.0268 pc, a knob no chain link fixes (FP17)",
          lcdm_standing="GR predicts no external-field quadrupole: passes",
          equipment=[], scorecard=["charter: Solar System"],
          commits=["a60b18e02 (FP17)", "03db97f14 (FP14)"])

# ---- A02 wide binaries --------------------------------------------------------------------------------------------------------
X22 = jload("real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic_results.json")["numbers"]["V1"]
_fl = {}
for _k, _v in X22.items():
    _f, _xi = _k.split("|")
    if _f not in _fl or float(_xi) < _fl[_f][0]:
        _fl[_f] = (float(_xi), _v["reg"])
row("A02", "Wide binaries", "Gaia DR3 wide-binary relative velocities at 1-30 kAU (the low-acceleration boost gamma)",
    cls="CONTESTED", contested="published low-acceleration boosts range from ~1.0 (Newtonian; Banik et al. 2024; Pittordis & Sutherland 2023) "
                               "to ~1.4 (Chae 2023, 2024; Hernandez 2023) on the same Gaia DR3 catalogue -- different hidden-triple, "
                               "error and selection models",
    numbers=dict(chain_ceiling={f: v[1] for f, v in _fl.items()}, xi_floor_pc={f: v[0] for f, v in _fl.items()},
                 kill_from_above=[1.157, 1.174], prereg_arm_A=[1.1614, 1.1814], prereg_arm_A_alt=[1.1917, 1.2267], lcdm=1.0),
    measured="Gaia DR3 astrometry and radial velocities of wide pairs; the statistic compares sky-projected relative velocities with "
             "the Newtonian expectation (the frozen DR4 pre-registration's gamma_hat)",
    cite=["Chae 2023, ApJ 952, 128", "Chae 2024, ApJ 960, 114", "Hernandez 2023, MNRAS 525, 1401", "Banik et al. 2024, MNRAS 527, 4573",
          "Pittordis & Sutherland 2023, OJAp 6, 4"],
    assumptions=["hidden triples / unresolved companions (fraction and mass-ratio model)", "velocity error model and projection "
                 "(eccentricity distribution)", "mass-luminosity relation", "chance alignments; distance and RUWE cuts"],
    fw_standing=f"the chain's law gives a CEILING gamma_hat = {_fl['canonical'][1]:.4f} (canonical) / {_fl['alt'][1]:.4f} (alt) at xi's floor, "
                "1.000 for xi >= 0.3 pc (XR22); DR4 can kill it only from above (gamma_hat >~ 1.157 / 1.174)",
    lcdm_standing="GR: gamma = 1.000", shift="the published analyses themselves span ~1.0-1.4; DR4 (2026-12-02) decides",
    equipment=["B17"], scorecard=["charter: Wide binaries"], commits=["661ea3cff (XR22)"])

# ---- A03 the radial acceleration relation at z ~ 0 ---------------------------------------------------------------------------
ET = text("EMPIRICAL_TESTS.md")
_rar = float(re.search(r"\*\*([0-9.]+) dex\*\* at .=0\.70", ET).group(1))
L391 = jload("real_research/dark_sector_2026/L391_inner_galaxies_nu_mono_results.json")["numbers"]
row("A03a", "Galaxies", "The RAR's shape and tightness (SPARC, 175 galaxies, 3389 points)", cls="MODEL-INDEPENDENT",
    numbers=dict(scatter_dex=_rar, rc_carrier_shift_dex=L391.get("rar_worst")),
    measured="Spitzer 3.6-micron photometry (stellar mass) plus HI and H-alpha rotation curves (SPARC); g_obs = V^2/R against g_bar from "
             "the baryonic mass model", cite=["Lelli, McGaugh & Schombert 2016, AJ 152, 157", "McGaugh, Lelli & Schombert 2016, PRL 117, 201101",
                                             "Li et al. 2018, A&A 615, A3"],
    assumptions=["stellar mass-to-light ratio at 3.6 micron", "distances and inclinations", "gas mass (1.33 M_HI)", "circular orbits"],
    fw_standing=f"the core law: scatter {_rar} dex at Upsilon = 0.70 on 175 SPARC (EMPIRICAL_TESTS A1); M*'s carrier moves it by <= 1.24e-4 dex "
                "(L391); the framework's strength",
    lcdm_standing="accommodated, not predicted: hydrodynamical simulations reproduce a RAR-like relation with feedback-dependent scatter",
    stake="no verdict is at stake at < 0.05 dex; the RAR's form is established across analyses (Li et al. 2018: a0 universal)",
    shift="Upsilon, distance and inclination systematics move individual galaxies (marginalised per galaxy by Li et al. 2018) but not the "
          "relation's form", equipment=[], scorecard=["charter: Galaxies", "scorecard: RAR, RC100 (z ~ 0 part)"],
    commits=["441d811e2 (L391)"])
gauss_row("A03b", "Galaxies", "The RAR's acceleration scale (a0 normalisation) against the fitted g-dagger", d=1.20e-10, s=0.02e-10,
          units="m/s^2", fw={"canonical footing": A0["canonical"], "alt footing": A0["alt"]}, lcdm={},
          budget={"stellar M/L systematic (McGaugh, Lelli & Schombert 2016)": 0.24e-10},
          measured="the same SPARC RAR fitted with nu = 1/(1 - exp(-sqrt(y))): g-dagger = 1.20 +- 0.02 (random) +- 0.24 (systematic) x 1e-10",
          cite=["McGaugh, Lelli & Schombert 2016, PRL 117, 201101"],
          assumptions=["the interpolating function (the framework's P2 / nu_mono differ; the record's own kappa fits use them: see O3)",
                       "the 3.6-micron M/L zero point"],
          fw_standing="a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 FITTED: 9.36e-11 (canonical) / 1.13e-10 (alt)",
          lcdm_standing="no a0 is predicted (no counterpart)", equipment=[], scorecard=["charter: Galaxies"], commits=["6123bd25b (FP0)"])

# ---- A04 the high-z RAR, BTFR and a0(z) ---------------------------------------------------------------------------------------
x17 = text("real_research/cross_thread_review_2026_09_26/XR17_flagship_row_numbers.out")
_sh17 = [float(x) for x in re.findall(r"worst shift at z = 2\.5 \+([0-9.]+) dex", x17)]
_scrit = float(re.search(r"S_crit \(worst host, on\): ([0-9.]+)", x17).group(1))
text("real_research/A0Z_MUSE_DARK_III_CONFRONTATION.md")
row("A04", "Galaxies (high z)", "The RAR/BTFR at z = 0.3-2.5 and the evolution of a0 (MUSE-DARK III, KMOS3D, RC100)", cls="CONTESTED",
    contested="MUSE-DARK III fits a0(z) = a0(0) + a1 z with a1 = +1.59 (+0.11/-0.10) x 1e-10 per unit z (15 sigma from flat at face value), "
              "while McGaugh et al. 2024 find no clear evolution in the BTFR / dark fraction to z ~ 2.5; a LCDM simulation (Magneticum) "
              "produces an APPARENT rise x2.3-3 by z ~ 2",
    numbers=dict(muse_a1=[1.59, 0.105], muse_Mstar_shift_dex=[0.2, 0.45], flagship_shift_dex=_sh17, S_crit=_scrit,
                 lcdm_native_offset_dex=0.33),
    measured="IFU kinematics (MUSE HUDF, 79 galaxies at 0.33 < z < 1.44; KMOS3D/SINS; RC100 at z = 0.6-2.5) with asymmetric-drift "
             "corrections; stellar masses from SED fits; gas from scaling relations",
    cite=["Ciocan, Bouche, Fensch et al. 2026, A&A 709, L16 (MUSE-DARK III)", "McGaugh, Schombert, Lelli & Franck 2024, ApJ 976, 13",
          "Mayer, Teklu, Dolag & Remus 2023, MNRAS 518, 257", "Nestor Shachar et al. 2023, ApJ 944, 78 (RC100)", "Milgrom 2017, arXiv:1703.06110"],
    assumptions=["stellar M/L and IMF at high z (the MUSE rise flattens only if M* is 0.2-0.45 dex larger, which its authors do not "
                 "support)", "pressure support (V/sigma) and beam smearing", "molecular gas from scaling relations", "halo profile in the fits"],
    fw_standing=f"the core law: a0 flat to < 1% for z <= 5; M*: RC100 passes (carrier shift <= 1.24e-4 dex, L391); M*'s flat-a0 flagship at "
                f"z = 2.5 is NOT established (XR17: +{min(_sh17):.3f} to +{max(_sh17):.3f} dex residue against S_crit {_scrit})",
    lcdm_standing="LCDM's apparent a0 rises (Magneticum x2.3-3 by z ~ 2), closer to MUSE's x4 than the flat law",
    shift="the stellar-mass scale: +0.2 to +0.45 dex would flatten MUSE's rise (disowned by its authors); see O4 for the registered "
          "z ~ 2.5 test", equipment=[], scorecard=["charter: Galaxies (flat a0(z))", "scorecard: flat-a0 flagship", "scorecard: RC100"],
    commits=["b667f56bb (XR17)", "441d811e2 (L391)"])

# ---- A05 the external-field systems -------------------------------------------------------------------------------------------
cb = text("hunt_2026/k_contrarian_clusterbtfr.out")
_cb = {m.group(1).strip(): (float(m.group(2)), float(m.group(3)))
       for m in re.finditer(r"^\s{4}(baseline[^\n]*?|tighter[^\n]*?|narrower[^\n]*?|deprojected[^\n]*?)\s+\d+\s+([+-][0-9.]+)\+/-([0-9.]+)", cb, re.M)}
_base = [v for k, v in _cb.items() if k.startswith("baseline")][0]
_narrow = [v for k, v in _cb.items() if k.startswith("narrower")][0]
_deproj = [v for k, v in _cb.items() if k.startswith("deprojected")][0]
S_CB = 0.0304
_mst = XR9T["EFE_clusters_sigma"]
_chn = rng(X27I["clusters (record gate)"][1])
gauss_row("A05a", "Dwarfs / external field", "Cluster-infall BTFR: the slope of the BTFR residual against the host's field (N = 314)",
          d=0.0033, s=S_CB, units="dex per dex",
          fw={"M* most favourable form (XR9)": 0.0033 - _mst[0] * S_CB, "M* least favourable (XR9)": 0.0033 - _mst[1] * S_CB,
              "chain L->inf most favourable (XR27)": 0.0033 - _chn[0] * S_CB, "chain L->inf least favourable (XR27)": 0.0033 - _chn[1] * S_CB},
          lcdm={"strong equivalence principle": 0.0},
          budget={"membership (2 sigma_v cut; k_contrarian robustness table)": abs(_narrow[0] - _base[0]),
                  "deprojection r = 1.3 R_proj": abs(_deproj[0] - _base[0]),
                  "Upsilon x1.5 (k_contrarian cb-6: < 0.5 bootstrap sigma)": 0.5 * S_CB},
          measured="ALFALFA alpha.100 HI line widths (W50, unresolved) with SDSS b/a inclinations and Durbala et al. 2020 stellar masses, "
                   "for spirals within 5 R500 and 3 sigma_v of Planck PSZ2 clusters; the host field from an NFW normalised to M_SZ",
          cite=["Haynes et al. 2018, ApJ 861, 49 (ALFALFA alpha.100)", "Durbala et al. 2020, AJ 160, 271", "Planck 2015 XXVII (PSZ2)",
                "Wang et al. 2016, MNRAS 460, 2143 (M_HI - D_HI)"],
          assumptions=["W50 -> V_flat at an R_HI from the M_HI-D_HI relation (unresolved line width)", "HI stripping in clusters "
                       "(truncated discs lower W50, biasing the measured slope toward an apparent deficit, the framework's own sign; "
                       "correcting it would move the slope away from the framework, so it adds nothing to the favourable budget)",
                       "cluster membership and 3-D radius", "NFW host profile scaled to the SZ mass"],
          fw_standing=f"fails: M* {_mst[0]:.2f}-{_mst[1]:.2f} sigma (XR9), the chain at L -> inf {_chn[0]:.2f}-{_chn[1]:.2f} sigma (XR27); "
                      "the spread is the EFE form (scalar-sum / subtract / flux), a theory-side ambiguity",
          lcdm_standing="SEP gives slope 0: 0.11 sigma", equipment=["B17"], scorecard=["scorecard: EFE, cluster-infall BTFR"],
          commits=["d4343a4b3 (k_contrarian_clusterbtfr)", "e39cb4420 (XR9 gate table)", "3e55fdff2 (XR27)"])
dw = text("hunt_2026/k_contrarian_dwarfefe.out")
_sub = {m.group(1).strip(): float(m.group(2)) for m in re.finditer(r"^\s{4}([A-Za-z][^\n]*?)\s+\d+\s+[+-][0-9.]+\+/-[0-9.]+\s+[+-][0-9.]+\s+([0-9.]+)\s+[0-9.]+\s*$", dw, re.M)}
_ups = re.search(r"predicted ([+-][0-9.]+) -> ([+-][0-9.]+)", dw)
_uobs = re.search(r"observed ([+-][0-9.]+) -> ([+-][0-9.]+)", dw)
X6D = jload("real_research/cross_thread_review_2026_09_26/XR6_efe_udg_under_candidate_results.json")["numbers"]["dwarfs"]["canonical"]
D_DW, S_DW = X6D["obs"], X6D["err"]
_mdw = XR9T["EFE_dwarfs_sigma"]
_cdw = rng(X27I["LV dwarfs"][1])
_all = _sub["all"]
_bin = _all - _sub["brighter than M_V = -6 (drop ultra-faints)"]
_tid = _all - _sub["drop the 10 nearest to their host"]
_upsn = (float(_uobs.group(1)) - float(_uobs.group(2))) + (float(_ups.group(2)) - float(_ups.group(1)))
gauss_row("A05b", "Dwarfs / external field", "Local Volume dwarfs: statistic C, the slope of log sigma_los against the host field at fixed "
          "M* and r_half (N = 92)", d=D_DW, s=S_DW, units="dex per dex",
          fw={"M* most favourable (XR9)": D_DW - _mdw[0] * S_DW, "M* least favourable": D_DW - _mdw[1] * S_DW,
              "chain L->inf most favourable (XR27)": D_DW - _cdw[0] * S_DW},
          lcdm={"strong equivalence principle": 0.0},
          budget={"binaries (drop the ultra-faints, M_V > -6)": max(0.0, _bin) * S_DW, "tides (drop the 10 nearest)": max(0.0, _tid) * S_DW,
                  "Upsilon_V x1.5 (observed and predicted together)": max(0.0, _upsn)},
          measured="line-of-sight velocity dispersions, half-light radii and luminosities of MW, M31 and field dwarfs from the Local Volume "
                   "Database; host baryonic fields from MW 6.0e10 and M31 1.2e11 Msun",
          cite=["Pace 2024, Local Volume Database (LVD)", "McMillan 2017, MNRAS 465, 76", "Tamm et al. 2012, A&A 546, A4"],
          assumptions=["dynamical equilibrium (tides)", "binary-star inflation of sigma for ultra-faints", "Upsilon_V (the record uses 2)",
                       "host distances and 3-D separations"],
          fw_standing=f"fails: M* {_mdw[0]:.2f}-{_mdw[1]:.2f} sigma (XR9), chain {_cdw[0]:.2f}-{_cdw[1]:.2f} sigma (XR27); L-independent",
          lcdm_standing=f"slope 0: {abs(D_DW) / S_DW:.2f} sigma (the observed slope is POSITIVE)", equipment=["B17"],
          scorecard=["scorecard: EFE, LV dwarfs"], commits=["d4343a4b3 (k_contrarian_dwarfefe)", "6566c53b3 (XR6)", "3e55fdff2 (XR27)"],
          note=f"subsamples (k_contrarian dw-8): {', '.join(f'{k} {v:.2f}' for k, v in _sub.items())} sigma")
X6U = jload("real_research/cross_thread_review_2026_09_26/XR6_efe_udg_under_candidate_results.json")["numbers"]["udg"]
_me = X6U["candidate"]["me"]
_sig_tot = _me["canonical/0.13"] / X6U["candidate"]["sigma"][0]
_floor = X6U["candidate"]["floor"]
_s_stat = math.sqrt(max(_sig_tot ** 2 - _floor ** 2, 1e-12))
_bud_udg = dict(X6U["candidate"]["budget"])
gauss_row("A05c", "Dwarfs / external field", "Coma ultra-diffuse galaxies: the dynamical excess over the EFE-suppressed prediction (11 UDGs)",
          d=0.0, s=_s_stat, units="dex (observed minus predicted)",
          fw={f"framework {k}": -v for k, v in _me.items()}, lcdm={},
          budget=_bud_udg,
          measured="stellar and globular-cluster velocity dispersions of 11 Coma UDGs (Keck/KCWI and others) compiled by Freundlich et al. "
                   "2022, with their stellar masses and effective radii; Coma's baryonic field from a beta model",
          cite=["Freundlich et al. 2022, A&A 658, A26", "van Dokkum et al. 2019, ApJ 880, 91 (DF44)"],
          assumptions=["stellar M/L and IMF", "aperture and orbital anisotropy", "the sigma-to-acceleration estimator", "3-D position in Coma",
                       "equilibrium in the cluster's tidal field"],
          fw_standing=f"fails: M* 4.20-4.35 sigma (XR9), chain L->inf 4.61 (XR27); even with no EFE the UDGs sit +0.40 dex high (1.8 sigma)",
          lcdm_standing="UDG dispersions are fitted with dwarf-mass halos: no tension (accommodated)", equipment=["B17"],
          scorecard=["scorecard: Coma UDGs"], commits=["6566c53b3 (XR6)", "3e55fdff2 (XR27)"],
          note=f"the record's sigma includes XR6's systematic floor ({_floor:.3f} dex, quadrature of its budget); here the floor's components "
               f"are the budget and the statistical error alone ({_s_stat:.3f} dex) sets the stake")
_c2 = rng(X27I["Crater II"][1])
row("A05d", "Dwarfs / external field", "Crater II and the M31 dwarf spheroidals: dispersions in the EFE regime", cls="SOFT",
    numbers=dict(crater2_record=_c2, crater2_literature_convention=[0.06, 2.48], m31_record=rng(X27I["M31 dwarfs"][1]),
                 m31_offsets_dex={"isolated": 0.121, "with EFE": 0.300}),
    measured="Crater II's sigma = 2.7 +- 0.3 km/s (Caldwell et al. 2017) and M31 dSph dispersions (Collins et al. 2013; LVD)",
    cite=["Caldwell et al. 2017, ApJ 839, 20", "Collins et al. 2013, ApJ 768, 172", "McGaugh 2016, ApJ 832, L8"],
    assumptions=["Upsilon_V (the record uses 2; the M31 dSphs need 14-24 in the record's statistic)", "the mass and radius convention "
                 "(full mass + projected R_h in the literature vs the record's)", "equilibrium"],
    fw_standing=f"fails in the record's statistic: Crater II {_c2[0]:.2f}-{_c2[1]:.2f} sigma, M31 dSphs 2.8-4.7 sigma (XR27)",
    lcdm_standing="accommodated with tidally stripped halos",
    stake="Crater II: from 4.2 sigma to 2 sigma", budget_text="the literature convention (full mass, projected R_h) gives 0.06-2.48 sigma: "
                                                           "the convention alone moves Crater II across the gate",
    shift="the convention and Upsilon_V", equipment=["B17"], scorecard=["charter: Dwarfs"], commits=["3e55fdff2 (XR27)"])
row("A05e", "Dwarfs / external field", "NGC 1052-DF2 / DF4: the dark-matter-deficient UDGs", cls="CONTESTED",
    contested="the distance is disputed: ~13 Mpc (Trujillo et al. 2019) against 22.1 +- 1.2 Mpc (TRGB, Shen et al. 2021) for DF2",
    numbers=dict(df2_record=rng(X27I["DF2"][1]), df4_record=rng(X27I["DF4"][1])),
    measured="GC and stellar velocity dispersions (van Dokkum et al. 2018; Emsellem et al. 2019) and distances",
    cite=["van Dokkum et al. 2018, Nature 555, 629", "Trujillo et al. 2019, MNRAS 486, 1192", "Shen et al. 2021, ApJ 914, L12",
          "Emsellem et al. 2019, A&A 625, A76"],
    assumptions=["distance", "GC-based dispersion with small N", "the host's field (Newtonian 0.023 a0 is below the internal field)"],
    fw_standing="1.2-3.5 sigma (DF2), 1.2-4.6 sigma (DF4) across distance and estimator (XR27)", lcdm_standing="accommodated (tidal stripping)",
    equipment=[], scorecard=["charter: Dwarfs, UDGs"], commits=["3e55fdff2 (XR27)"])
row("A05f", "Dwarfs / external field", "Chae's EFE signal in SPARC rotation curves", cls="SOFT",
    numbers=dict(chain_Linf={"D2": X27I["Chae D2 (catalogued)"][1], "D1": X27I["Chae D1 (any geometry)"][1]},
                 Mstar_D2=X27M["Chae D2 (catalogued)"][1], catalogued_vs_collapsed_at_separators="D2 2.8-2.9 vs 1.0-1.3 sigma"),
    measured="outer rotation-curve shapes of SPARC galaxies fitted with an EFE parameter e_N; environmental fields from 2M++",
    cite=["Chae et al. 2020, ApJ 904, 51", "Chae et al. 2021, ApJ 921, 104", "Lavaux & Hudson 2011, MNRAS 416, 2840 (2M++)"],
    assumptions=["Chae's fitting function with a0 = 1.2e-10 (no re-fit on disk)", "the 2M++ environment reconstruction (catalogued vs "
                 "group-collapsed geometry; redshift-space distances)", "M/L"],
    fw_standing="the chain passes only at L -> inf (D2 0.0, D1 0.8 sigma); at the separators' L it fails (catalogued) or passes "
                "(collapsed); M* fails D2 at 2.9 sigma (XR27)", lcdm_standing="no EFE: the signal would be a systematic",
    stake="D2 at the separators: from 2.9 to 2 sigma", budget_text="the environment geometry (catalogued vs group-collapsed) moves D2 by "
                                                                  "1.6-1.9 sigma (XR27)",
    shift="the environment reconstruction", equipment=[], scorecard=["charter: external field"], commits=["3e55fdff2 (XR27)"])
P(f"    {el()}")

# ---- A06 strong lensing (SLACS) -------------------------------------------------------------------------------------------------
X33 = jload("real_research/cross_thread_review_2026_09_26/XR33_lensing_imf_results.json")["numbers"]["I"]
_sn_ch = X33["canonical"]["SNELLS_la_salp"] - X33["canonical"]["slacs_sig280"]
row("A06", "Strong lensing", "SLACS Einstein masses and aperture dispersions of massive ellipticals", cls="CONTESTED",
    contested=f"published IMF methods disagree: SNELLS lenses need an IMF {abs(_sn_ch):.3f} dex (chain) / {abs(X33['lcdm_same_tests']['diff']):.3f} dex "
              "(LCDM) lighter than SLACS lenses at sigma >= 280 km/s, more than the shift the framework needs",
    numbers=dict(chain_minus_CvD=[X33["canonical"]["dCvD_mean"], X33["canonical"]["dCvD_err"]], alt_minus_CvD=X33["alt"]["dCvD_mean"],
                 relation_rms=X33["CvD12b_fit"]["rms"], lcdm_minus_CvD=X33["lcdm_same_tests"]["treu_minus_cvd"],
                 snells_minus_slacs=dict(chain=_sn_ch, lcdm=X33["lcdm_same_tests"]["diff"])),
    measured="HST imaging (Einstein radii) and SDSS fibre dispersions of 59 SLACS lenses; stellar masses from SPS fits with a Chabrier "
             "or Salpeter IMF (Auger et al. 2009/2010)", cite=["Bolton et al. 2008, ApJ 682, 964", "Auger et al. 2010, ApJ 724, 511",
             "Treu et al. 2010, ApJ 709, 1195", "Conroy & van Dokkum 2012, ApJ 760, 71", "Smith, Lucey & Conroy 2015, MNRAS 449, 3441 (SNELLS)"],
    assumptions=["the stellar IMF (the free normalisation at stake)", "de Vaucouleurs / Sersic light profiles", "isotropic orbits in the "
                 "Jeans model", "the lens-galaxy environment (external convergence)"],
    fw_standing=f"the chain needs log alpha_Salp {X33['canonical']['dCvD_mean']:+.3f} +- {X33['canonical']['dCvD_err']:.3f} dex above the "
                f"spectroscopic alpha-sigma relation (alt {X33['alt']['dCvD_mean']:+.3f}), the heaviest spectroscopic IMF (XR33)",
    lcdm_standing=f"LCDM's own SLACS IMF sits {X33['lcdm_same_tests']['treu_minus_cvd']:+.3f} dex from the relation (Treu et al. 2010)",
    shift=f"the spectroscopic relation's own rms is {X33['CvD12b_fit']['rms']:.3f} dex; SNELLS vs SLACS differ by 0.26-0.30 dex in both frameworks",
    equipment=[], scorecard=["charter: Strong lensing (SLACS)"], commits=["92fe59705 (XR33)"])

# ---- A07 weak lensing around isolated galaxies (KiDS-1000) ------------------------------------------------------------------------
_f18o = text("real_research/derivation_chain_2026/FP18_kids_vs_hubble_flow_data.out")
_r03 = re.search(r"R <= 0\.3 Mpc only \(B21's range for analytic models\): face value stack ([0-9.]+), LG ([0-9.]+)", _f18o)
F20R = R20["R10_flips"] if "R10_flips" in R20 else []
row("A07a", "Weak lensing", "KiDS-1000 isolated-lens excess surface density inside 0.3 Mpc (Brouwer et al. 2021, four mass bins)",
    cls="MODEL-INDEPENDENT", numbers=dict(face_T_R03={"stack": float(_r03.group(1)), "LG": float(_r03.group(2))}, fp20_P1_error_35kpc_percent=sis35),
    measured="KiDS-1000 shear around KiDS-bright isolated lenses (photometric redshifts, 0.1 < z < 0.5), GAaP photometry and stellar "
             "masses; Delta Sigma at 35-300 kpc", cite=["Brouwer et al. 2021, A&A 650, A113", "Giblin et al. 2021, A&A 645, A105"],
    assumptions=["the stellar-mass scale (>= 0.2 dex systematic; B21 Sect. 5.2)", "the shear calibration (multiplicative bias)",
                 "the boost / source-dilution convention (FP21: ~10% on the inner bins)"],
    fw_standing="the chain passes (FP13/FP19 with FP20's exact projection: -8.6/-10.3 at z = 0.25); M* passes (-29.0, XR9; provisional "
                "until XR35 re-scores the P2 projector); the core's weak-lensing RAR passes (EMPIRICAL_TESTS A2)",
    lcdm_standing="NFW + galaxy fits it (FP18 L1)",
    stake="the chain's KiDS passes sit ~17-19 in Delta chi^2 below the gate at z = 0.25",
    shift=f"FP20 moved the model's inner Delta Sigma by up to {abs(sis35):.0f}% at 35 kpc (and 4-14% outside) and no deciding verdict flipped; "
          "the data-side budget inside 0.3 Mpc (M* scale ~0.1 dex in the MOND prediction, boost ~0.04 dex) is smaller than that perturbation",
    equipment=["B02", "B09", "B13"], scorecard=["scorecard: KiDS-1000", "charter: Weak lensing"],
    commits=["09990b398 (FP18)", "7a8c25321 (FP20)", "bb368ad2a (FP21)"])
_opt = R18["S"]["at_optimum"]
X21V = jload("real_research/derivation_chain_2026/FP21_isolated_spiral_lensing_results.json")["numbers"]["V"]
row("A07b", "Weak lensing", "KiDS-1000 isolated-lens excess surface density at 0.3-2.6 Mpc", cls="SOFT",
    numbers=dict(b21_leakage_factor=1 / 1.3, gama_over_kids_out=R18["S"]["gama_over_kids"][0], type_contrast_out=R18["S"]["delta"]["out"],
                 fp18_adjusted_out_dex={"stack": _opt["stack"]["adj_out"], "LG": _opt["LG"]["adj_out"]},
                 fp21=dict(A=X21V["A"], sA=X21V["sA"], T=X21V["T"], p=X21V["p"], N_decide=X21V["N3"])),
    measured="as A07a, 0.3-2.6 Mpc; isolation from photometric redshifts (no neighbour with > 10% of the lens's M* within 3 Mpc)",
    cite=["Brouwer et al. 2021, A&A 650, A113 (App. A: photo-z leakage)", "FP21's spectroscopic 2M++ re-measurement (bb368ad2a)"],
    assumptions=["photometric-redshift isolation: B21's own MICE test puts the ESD ~30% high beyond 0.3 Mpc (GAMA/KiDS 0.75 +- 0.13, FP18)",
                 "galaxy type (the LV analogs are spirals; blue/red contrast 0.50 +- 0.04 beyond 0.3 Mpc)", "the stellar-mass scale", "the 2-halo term"],
    fw_standing="the chain and M* pass against the published (mixed-type, leakage-inflated) bins; neither model has been scored against the "
                "leakage-corrected signal",
    lcdm_standing="B21 compare LCDM mocks built with the same photometric selection",
    stake="the record's verdicts at > 0.3 Mpc (the KiDS passes and the KiDS-R0 pincer) turn on shifts of 0.1-0.5 dex",
    shift=f"B21's leakage alone is -{math.log10(1.3):.3f} dex; FP18's profiled comparability shift for LV-like spirals is "
          f"{_opt['stack']['adj_out']:+.2f} / {_opt['LG']['adj_out']:+.2f} dex (nuisances within ~1.5 sigma of published priors); FP21's "
          f"isolated late types give A = {X21V['A']:.2f} +- {X21V['sA']:.2f} of the mixed level (undecided; ~{X21V['N3']} lenses decide)",
    budget_text="0.11-0.5 dex against a stake of 0.1-0.5 dex", equipment=["B02", "B09", "B13"], scorecard=["scorecard: KiDS-1000"],
    commits=["09990b398 (FP18)", "bb368ad2a (FP21)"])
row("A07c", "Groups / weak lensing", "The KiDS-versus-Local-Volume pincer: one mass profile for KiDS isolated lenses and the LV Hubble flow",
    cls="SOFT", numbers=dict(T_face=t_nom, T_profiled=t_pro, sigma_profiled=2.3, lcdm_R0_kids_calibrated=[1.85, 1.94]),
    measured="FP18's data-only joint test (B21 lensing + K&K 2018 zero-velocity radii), re-executed here (K1)",
    cite=["Brouwer et al. 2021, A&A 650, A113", "Kashibadze & Karachentsev 2018, A&A 609, A11"],
    assumptions=["spherical symmetry, a Lagrangian (published-convention) zero-velocity shell", "comparability: galaxy type, isolation "
                 "leakage, M* scale, R0 method, eq. (4) coefficient, epoch"],
    fw_standing="the chain's and M*'s outer profiles overshoot R0 (A08) while fitting KiDS", lcdm_standing="LCDM's KiDS-fitted halos turn "
                "around at 1.85-1.94 Mpc against 0.91-0.93: the same pincer (FP18 L1)",
    stake="from 9.8 sigma (face value) to below 3 sigma", shift=f"six comparability systematics profiled under published priors: T {t_nom:.1f} -> "
    f"{t_pro:.2f} (2.3 sigma); the extreme corner 4.77", budget_text="the profile itself (K1)", equipment=["B12"],
    scorecard=["charter: Groups, Local Group"], commits=["09990b398 (FP18)", "bb368ad2a (FP21)"])

# ---- A08 the Local Group zero-velocity radius ----------------------------------------------------------------------------------
_R12V = jload("real_research/derivation_chain_2026/FP12_local_volume_groups_r0_results.json")["numbers"]["V"]
R12, _R12S = _R12V["delta_primary"], _R12V["sigma"]
_e = R18["E"]
_lg14, _lg35 = _e["LG14"]["R0"], _e["LG35"]["R0"]
_s_lg = R18["E"]["honest"]["LG"] / 0.96 / math.log(10)
_d_lg = math.log10(0.96)
_ldx = XR9T["LG_dex_decay"]
gauss_row("A08", "Groups, Local Group", "The Local Group zero-velocity radius R0 (log10 R0)", d=_d_lg, s=_s_lg, units="dex",
          fw={"chain canonical (FP12)": _d_lg + R12["LG"][0], "chain alt (FP12)": _d_lg + R12["LG"][1],
              "M* most favourable (XR9)": _d_lg + _ldx[0], "M* least favourable (XR9)": _d_lg + _ldx[1]},
          lcdm={"KiDS-calibrated NFW at the LG central's mass (FP18 L1)": math.log10(1.85)},
          budget={"R0 method: centre/attractor choices (K&K Table 8; FP18's prior)": 0.05,
                  "sample: 14 MW/M31-disturbed vs all 35 LG galaxies (FP18 E)": abs(math.log10(_lg35 / _lg14))},
          measured="TRGB distances and radial velocities of 35 galaxies around the LG, fitted with V = H0 R - H0 R0 (R0/R)^(1/2) "
                   "(K&K 2018 eq. 14); R0 = 0.91 (K&K adopted) / 0.96 (Karachentsev 2009) Mpc",
          cite=["Kashibadze & Karachentsev 2018, A&A 609, A11", "Karachentsev et al. 2009, MNRAS 393, 1265"],
          assumptions=["spherical infall with Lambda (point mass)", "the barycentre and attractor frame", "the distance ladder (TRGB, ~5%)",
                       "no coherent bulk flow of the whole group"],
          fw_standing="fails: the chain +0.20 dex (FP12), M* +0.18 to +0.24 dex (XR9); FP12's significances used the quoted errors, which "
                      "omit the velocity scatter (FP18 E1: the honest error is 4-6x larger)",
          lcdm_standing="passes with a per-system halo mass; its KiDS-calibrated halo overshoots by +0.31 dex (FP18 L1)",
          equipment=["B12"], scorecard=["scorecard: Local Group zero-velocity radius", "charter: Groups, Local Group"],
          commits=["59e537955 (FP12)", "09990b398 (FP18)", "e39cb4420 (XR9)"])

# ---- A09 clusters -------------------------------------------------------------------------------------------------------------
_ih = text("real_research/INHAND_CALCS_RESULTS_2026-07.md")
_eta = re.search(r"η\(R500\) = ([0-9.]+) \[envelope ([0-9.]+)–([0-9.]+)\]", _ih)
ETA = [float(_eta.group(i)) for i in (1, 2, 3)]
row("A09a", "Clusters", "The mass beyond MOND in clusters (eRASS1 / X-COP hydrostatic masses)", cls="MODEL-INDEPENDENT",
    numbers=dict(eta_R500=ETA, eta_after_bias={b: ETA[0] / (1 - b) for b in (0.06, 0.1, 0.2)}),
    measured="X-ray temperature and density profiles (eROSITA eRASS1; XMM X-COP with Planck SZ pressure) giving hydrostatic masses, "
             "against MOND on the observed baryons", cite=["Bulbul et al. 2024, A&A 685, A106 (eRASS1)", "Ettori et al. 2019, A&A 621, A39",
             "Eckert et al. 2019, A&A 621, A40", "Sanders 2003, MNRAS 342, 901"],
    assumptions=["hydrostatic equilibrium; the non-thermal pressure support (X-COP median 6% at R500)", "spherical symmetry", "gas clumping",
                 "the temperature calibration"],
    fw_standing=f"MOND on the baryons leaves eta(R500) = {ETA[0]} [{ETA[1]}-{ETA[2]}] (INHAND_CALCS 2026-07): a dark component is required; "
                "the chain's dark-sector window is empty so far (FP16)", lcdm_standing="CDM supplies it (the cosmic baryon fraction at R500)",
    stake="any shift that lowers eta toward 1", shift=f"every hydrostatic systematic moves it the wrong way: eta/(1 - b) = "
    f"{ETA[0] / 0.94:.2f} / {ETA[0] / 0.8:.2f} for b = 0.06 / 0.2", budget_text="none in the favourable direction",
    equipment=[], scorecard=["charter: Clusters"], commits=["6837cef2be (INHAND_CALCS)"])
F16 = jload("real_research/derivation_chain_2026/FP16_daughter_reaccretion_results.json")["numbers"]
_rat = {}
for _vk, _v in F16["G3"]["per_kick"].items():
    for _rd in ("ratio_raw", "ratio_cal"):
        for _f in ("canonical", "alt"):
            _rat[f"halo {_vk} km/s {_rd[6:]} {_f}"] = _v[_rd][_f]
for _key, _v in F16["G11"]["xcop"].items():
    for _rd in ("ratio_raw", "ratio_cal"):
        for _f in ("canonical", "alt"):
            _rat[f"web {_key} {_rd[6:]} {_f}"] = _v[_rd][_f]
B_NEED = {k: max(0.0, 1 - 1.2 / r) for k, r in _rat.items()}
_kbest = min(B_NEED, key=B_NEED.get)
_kworst = max(B_NEED, key=B_NEED.get)
B_XCOP, B_MAX = 0.06, 0.20
_bf = seen("A09b", "bias", "fw", B_NEED[_kbest], 0.0)
_bl = seen("A09b", "bias", "lcdm", B_NEED[_kbest], 0.0)
_bfw = seen("A09b", "bias_worst", "fw", B_NEED[_kworst], 0.0)
_blw = seen("A09b", "bias_worst", "lcdm", B_NEED[_kworst], 0.0)
row("A09b", "Clusters", "X-COP total masses at R500 against the chain's dark sector (FP16: too much retained mass)",
    cls=classify(None, B_MAX, B_NEED[_kbest]),
    numbers=dict(ratio=_rat, b_needed=B_NEED, most_favourable=[_kbest, B_NEED[_kbest]], least_favourable=[_kworst, B_NEED[_kworst]],
                 b_xcop=B_XCOP, b_budget=B_MAX, lcdm_fgas_ratio_at_b=dict(best=(1 - _bl) / (1 - B_XCOP), worst=(1 - _blw) / (1 - B_XCOP)),
                 fw_ratio_after_b=dict(best=_rat[_kbest] * (1 - _bf), worst=_rat[_kworst] * (1 - _bfw)), v_k_needed=F16["G10"]),
    measured="X-COP: XMM-Newton density and temperature profiles joined to Planck SZ pressure out to R200; hydrostatic masses for 12 "
             "clusters (the record's real_research/data/xcop)", cite=["Ettori et al. 2019, A&A 621, A39", "Eckert et al. 2019, A&A 621, A40",
             "von der Linden et al. 2014, MNRAS 443, 1973", "Hoekstra et al. 2015, MNRAS 449, 685", "Smith et al. 2016, MNRAS 456, L74"],
    assumptions=["hydrostatic equilibrium", "non-thermal pressure: X-COP's own 6% median (derived by requiring the universal baryon "
                 "fraction, a LCDM input)", "spherical symmetry and clumping"],
    fw_standing=f"FP16: the chain's dark sector keeps M_dyn/M_HSE = {min(_rat.values()):.3f}-{max(_rat.values()):.3f} against the 20% gate",
    lcdm_standing="LCDM + CDM fits X-COP by construction (f_gas calibrated at b = 0.06)",
    stake=f"the hydrostatic bias b that brings the most favourable cell inside the gate, |ratio (1 - b) - 1| <= 0.2: b = {B_NEED[_kbest]:.3f} "
          f"({_kbest}); the least favourable needs {B_NEED[_kworst]:.3f}",
    shift=f"published bias calibrations span b ~ 0.05-0.3 (weak-lensing (1 - b) = 0.69 +- 0.07 / 0.76 +- 0.08 / 0.95 +- 0.04; simulations "
          f"~0.1-0.2); the defensible budget used is b <= {B_MAX}", budget_text=f"b <= {B_MAX}",
    lcdm_same=f"at the same b, LCDM's X-COP gas fraction is {(1 - _bl) / (1 - B_XCOP):.3f} (most favourable cell) / {(1 - _blw) / (1 - B_XCOP):.3f} "
              "(least) of its universal-fraction calibration", equipment=["B07", "B15"], scorecard=["scorecard: S8, clearing, X-COP (not run on M*)",
              "charter: Clusters"], commits=["b3f5759a4 (FP16)"])
row("A09c", "Clusters", "Collisionless mass offsets in merging clusters (the Bullet Cluster)", cls="MODEL-INDEPENDENT",
    numbers=dict(offset_significance_sigma=8),
    measured="weak + strong lensing mass maps (HST, Magellan) against Chandra X-ray gas in 1E 0657-56", cite=["Clowe et al. 2006, ApJ 648, L109"],
    assumptions=["the lensing reconstruction (convergence maps)", "the X-ray gas mass model"],
    fw_standing="requires a collisionless component; the framework's dark field is collisionless in kind (FL1/FK1), not scored on the chain",
    lcdm_standing="CDM is collisionless: passes", stake="any offset < 8 sigma", shift="none documented that removes an 8-sigma lensing-gas offset",
    budget_text="none", equipment=[], scorecard=["charter: Clusters"], commits=[])
L389R = jload("real_research/dark_sector_2026/L389_harvey_same_cell_linear_gate_results.json")["numbers"]["results"]
_hb = max(L389R["v575"]["MEAN"]["S2_med"].values())
row("A09d", "Clusters", "Dark-matter-star offsets in 72 cluster collisions (Harvey et al. 2015)", cls="CONTESTED",
    contested="Harvey et al. 2015 bound sigma/m < 0.47 cm^2/g from the stacked offsets; Wittman, Golovich & Dawson 2018 re-analyse the "
              "offsets and find them consistent with zero with a much weaker bound (~2 cm^2/g)",
    numbers=dict(Mstar_beta_575=_hb, gate=0.10),
    measured="HST weak/strong lensing and Chandra centroids of 30 systems (72 substructures)",
    cite=["Harvey et al. 2015, Science 347, 1462", "Wittman, Golovich & Dawson 2018, ApJ 869, 104"],
    assumptions=["centroid estimators of lensing and gas", "the fractional-drag model beta"],
    fw_standing=f"M*: knife-edge, beta = +{_hb:.3f} against +0.10 at 575 km/s only (L389); its MUTATE never ran", lcdm_standing="collisionless: passes",
    equipment=["B14"], scorecard=["scorecard: Harvey"], commits=["6dc375e88 (L389)"])

# ---- A10 / A11 the CMB -------------------------------------------------------------------------------------------------------
row("A10", "CMB", "Planck 2018 TT/TE/EE primary spectra and the compressed distance priors", cls="MODEL-INDEPENDENT",
    numbers=dict(chain_shift=R26["C1"]["shift"], class_precision=R26["K2"]["class_precision"], dp_chi2_diff=R26["C2"]["chi2_test"] - R26["C2"]["chi2_lcdm"]),
    measured="Planck HFI/LFI maps; Plik/CamSpec high-l likelihoods; Chen, Huang & Wang 2019 distance priors",
    cite=["Planck 2018 VI, A&A 641, A6", "Chen, Huang & Wang 2019, JCAP 02, 028"],
    assumptions=["foreground models (dust, CIB, point sources)", "calibration and beams", "the reionisation optical depth"],
    fw_standing=f"the chain's early universe is GR + CDM: spectra move by {R26['C1']['shift']:.1e} against CLASS's own precision "
                f"{R26['K2']['class_precision']:.1e} (XR26)", lcdm_standing="the reference model",
    stake="any departure the spectra can register (> 1e-3)", shift="foreground and calibration choices move the spectra by far less than any "
    "model difference at stake here (the chain's is 1e-7)", budget_text="n/a", equipment=[], scorecard=["charter: CMB"], commits=["68135cb7a (XR26)"])
_m32 = commit_msg("fa341733d")
_x32 = dict(s8k=grab(r"S8 ([0-9.]+) \(KiDS-1000 set-up\)", _m32), s8d=grab(r"S8 [0-9.]+ \(KiDS-1000 set-up\), ([0-9.]+) \(DES-Y3\)", _m32),
            cmbl=grab(r"CMB lensing amplitude ([0-9.]+)", _m32), counts=grab(r"cluster counts ([0-9.]+-[0-9.]+) of LCDM", _m32, cast=str),
            rsd=grab(r"f sigma_8 ([0-9.]+-[0-9.]+)% low", _m32, cast=str), rsd_sig=grab(r"% low \(([+-][0-9.]+) sigma\)", _m32))
X21 = jload("real_research/cross_thread_review_2026_09_26/XR21_s1_separator_linear_results.json")["numbers"]
_BK, _KHF, _ZL, _k4 = X26["BK"][HEAD26], X26["KHF"], X26["Z_L"], X26["k4pb"]
FEFF = {}
for _z in (0.0, 0.25):
    for _k in (0.3, 0.5, 1.0):
        _Bpm = float(np.interp(math.log(_k), np.log(_KHF), _BK[_ZL.index(_z)]))
        _Cpm = math.sqrt(_Bpm / (1 + _k4[_z][_k])) - 1
        _ma, _La = X21["P4"]["real_HS_chain_canonical"][f"{_z}/{_k}/fp9"]
        _mb, _bb, _Lb = X21["P4"]["real_HS_chain_canonical"][f"{_z}/{_k}"]
        FEFF[f"z={_z} k={_k}"] = dict(C_permode=_Cpm, f_allmatter_real=(math.sqrt((1 + _La) / (1 + _ma)) - 1) / _Cpm,
                                       f_baryons_real=(math.sqrt((1 + _Lb) / (1 + _mb)) - 1) / _Cpm)
_fa = [v["f_allmatter_real"] for v in FEFF.values()]
_fb = [v["f_baryons_real"] for v in FEFF.values()]
FS26, AM26 = X26["FS"], X26["AMPS"]
Aof = lambda f, b: float(np.interp(f, FS26, AM26[b]))
AMPMAP = {"XR26 headline, per-mode, all matter": {"lin": a26["lin"], "NL": a26["NL"]},
          "real-space, all matter (lowest mapped f)": {"lin": Aof(min(_fa), "lin"), "NL": Aof(min(_fa), "NL")},
          "real-space, all matter (highest mapped f)": {"lin": Aof(max(_fa), "lin"), "NL": Aof(max(_fa), "NL")},
          "real-space, baryons only (lowest mapped f)": {"lin": Aof(min(_fb), "lin"), "NL": Aof(min(_fb), "NL")},
          "real-space, baryons only (highest mapped f)": {"lin": Aof(max(_fb), "lin"), "NL": Aof(max(_fb), "NL")}}
gauss_row("A11", "CMB lensing, growth", "The CMB lensing amplitude (Planck 2018, 8 <= L <= 400; ACT DR6)", d=1.011, s=0.028, units="A_lens",
          fw={f"{k} [{b}]": v[b] for k, v in AMPMAP.items() for b in ("lin", "NL")}, lcdm={"LCDM (Planck best fit)": 1.0},
          budget={"pipeline and fiducial dependence, measured as Planck 2018 minus ACT DR6 (independent instrument, sky, noise and "
                  "foreground treatment; the difference is 0.002 +- 0.036)": 0.002},
          measured="quadratic-estimator lensing reconstruction from CMB temperature and polarisation maps; band powers debiased with "
                   "realisation-dependent N0 and a fiducial N1; A = 1.011 +- 0.028 (Planck MV 8-400), 1.013 +- 0.023 (ACT DR6)",
          cite=["Planck 2018 VIII, A&A 641, A8", "Madhavacheril et al. 2024, ApJ 962, 113", "Qu et al. 2024, ApJ 962, 112"],
          assumptions=["the fiducial LCDM spectra in the normalisation and N1 (corrected to first order in both likelihoods)",
                       "foreground mitigation (tSZ, CIB)", "the Gaussian-field approximation for the band-power covariance"],
          fw_standing=f"XR26: the chain fails at +4.9 sigma (linear base) / +40 sigma (halofit), on FP13's per-mode, all-matter yardstick; mapped "
                      f"onto XR26's own A(f) with XR21's real-space box, f = {min(_fa):.2f}-{max(_fa):.2f} (all matter) and "
                      f"{min(_fb):.2f}-{max(_fb):.2f} (baryons only) -- see B01, B04.  FP22 (bfe9a2fe5): the action as written (all matter) "
                      "is excluded in every cell; the chain has adopted the baryons-only reading (08548fc85), which passes Planck and ACT on "
                      f"the linear base and fails ACT on the halofit base (undecided until the nonlinear phantom is computed); the fluid's "
                      f"conversion alone gives A = {_x32['cmbl']} (-1.6 sigma vs ACT; XR32)",
          lcdm_standing="A = 1 by construction (pull -0.39 sigma)", equipment=["B01", "B03", "B04", "B07"],
          scorecard=["charter: CMB lensing, growth"], commits=["68135cb7a (XR26)", "b4bf5b2ae (XR21)"],
          note="A_L from TT/TE/EE (1.180 +- 0.065, Planck 2018 VI) is a separate, contested lensing-like smoothing excess (PR4 re-analyses "
               "reduce it); it is not the reconstruction amplitude scored here")
OUT["numbers"]["A11_mapping"] = dict(f_eff=FEFF, amplitudes=AMPMAP)

# ---- A12 large-scale structure ------------------------------------------------------------------------------------------------
_c3 = R26["C3"]["rows"]["PPN edge (alpha_c = 3.2e-9)"]
row("A12a", "Large-scale structure", "BAO, the P(k) shape and RSD growth", cls="MODEL-INDEPENDENT",
    numbers=dict(chain_dr_d_over_r_d=_c3["dr_d_over_r_d"], chain_dH0_kms=_c3["dH0_kms_cmb_bao"]),
    measured="galaxy and quasar clustering (BOSS/eBOSS, DESI) with reconstruction; RSD from anisotropic clustering",
    cite=["Alam et al. 2021, PRD 103, 083533 (eBOSS)", "DESI Collaboration 2025 (DR2 BAO)"],
    assumptions=["a fiducial cosmology for the distance conversion (Alcock-Paczynski, corrected)", "the reconstruction model"],
    fw_standing=f"the chain's background is LCDM's (unimodular Lambda; r_d moves by {_c3['dr_d_over_r_d']:.1e}, XR26 C3); late linear growth "
                f"sigma_8 1.012-1.015 x LCDM on the per-mode yardstick (FP19); the fluid's conversion leaves BAO untouched but puts DESI's "
                f"f sigma_8 {_x32['rsd']}% low ({_x32['rsd_sig']} sigma; XR32, hub re-run pending)", lcdm_standing="the reference",
    stake="percent-level shifts in r_d or in the P(k) shape", shift="the fiducial-cosmology dependence is corrected in the published analyses",
    budget_text="sub-percent", equipment=["B01", "B03"], scorecard=["charter: Large-scale structure"], commits=["68135cb7a (XR26)", "0c18c582f (FP19)"])
X19 = jload("real_research/cross_thread_review_2026_09_26/XR19_web_runaway_results.json")
_s8x19 = re.search(r'"S8": ([0-9.]+)', json.dumps(X19)).group(1)
row("A12b", "Large-scale structure", "S8 from weak-lensing surveys", cls="CONTESTED",
    contested="KiDS-1000 S8 = 0.759 (+0.024/-0.021) vs KiDS-Legacy 0.815 (+0.016/-0.021) vs Planck 2018 0.832 +- 0.013 (DES Y3 3x2pt "
              "0.776 +- 0.017): the same survey's two analyses straddle the Planck value",
    numbers=dict(published=dict(KiDS1000=0.759, KiDSLegacy=0.815, DESY3=0.776, Planck=0.832), chain_XR19_S8=float(_s8x19),
                 chain_XR32_inferred=dict(KiDS_setup=_x32["s8k"], DES_setup=_x32["s8d"])),
    measured="cosmic-shear two-point statistics with photometric redshifts and shear calibration",
    cite=["Asgari et al. 2021, A&A 645, A104", "Wright et al. 2025, arXiv:2503.19441 (KiDS-Legacy)", "DES Collaboration 2022, PRD 105, 023520",
          "Planck 2018 VI, A&A 641, A6"],
    assumptions=["baryonic feedback on small-scale power (marginalised)", "intrinsic alignments", "photo-z calibration"],
    fw_standing=f"the dark fluid's conversion (no phantom) gives the S8 a survey would infer: {_x32['s8k']} (KiDS-1000 set-up) / {_x32['s8d']} "
                "(DES-Y3 set-up) -- on KiDS-1000/DES/HSC and ~2.3 sigma below KiDS-Legacy (XR32, fa341733d; hub re-run pending; XR19's linear "
                f"S8 {float(_s8x19):.3f})",
    lcdm_standing="Planck-normalised LCDM sits at the top of the band", equipment=["B07"], scorecard=["charter: Large-scale structure (S8)"],
    commits=["b55775ce0 (XR19)", "fa341733d (XR32)"])
row("A19", "Clusters", "Cluster abundance (number counts)", cls="CONTESTED",
    contested="the published cluster-count cosmologies disagree: eRASS1 S8 = 0.86 +- 0.01 (Ghirardini et al. 2024) against SPT S8 = "
              "0.795 +- 0.029 (Bocquet et al. 2024)",
    numbers=dict(published=dict(eRASS1=[0.86, 0.01], SPT=[0.795, 0.029]), chain_counts_over_lcdm=_x32["counts"]),
    measured="X-ray (eROSITA eRASS1) and SZ (SPT) selected clusters with weak-lensing mass calibration",
    cite=["Ghirardini et al. 2024, A&A 689, A298", "Bocquet et al. 2024, PRD 110, 083510"],
    assumptions=["the mass-observable relation and its weak-lensing calibration", "the selection function", "the halo mass function"],
    fw_standing=f"the fluid's conversion puts the counts at {_x32['counts']} of LCDM: it fits SPT and sits 5-9 sigma below eRASS1 (XR32, hub re-run pending)",
    lcdm_standing="Planck LCDM fits eRASS1; SPT prefers a lower S8", equipment=["B07"], scorecard=["charter: Clusters"], commits=["fa341733d (XR32)"])

# ---- A13 the Lyman-alpha forest -----------------------------------------------------------------------------------------------
DE11B = jload("real_research/dark_energy_2026/DE11b_forest_convergence_results.json")["numbers"]["worst"]
_w11 = max(DE11B.values())
NU = N18["M6"]["nu_p2"]
_yz = {3.0: (0.100, 0.377), 2.0: (0.056, 0.212)}                       # XR34's analytic-halo y range at z = 3, 2 (both footings)
KFAC = {}
for _zz, (_y0, _y1) in _yz.items():
    _ys = np.geomspace(_y0, _y1, 50)
    _num = np.array([float(np.asarray(NU(np.array([y])))[0]) - 1 for y in _ys])
    _den = np.array([float(np.asarray(NU(np.array([(1 + _zz) * y])))[0]) - 1 for y in _ys])
    KFAC[str(_zz)] = [float(np.min(_num / _den)), float(np.max(_num / _den))]
_kmax = max(v[1] for v in KFAC.values())
row("A13", "Lyman-alpha forest", "Small-scale power at z = 2-3 from the 1D flux power", cls="SOFT",
    numbers=dict(record_gate=0.10, mcdonald2005_DeltaL2=[0.452, 0.069, 0.057], DE11b_worst=_w11, kernel_factor=KFAC,
                 DE11b_worst_estimated_after_fix=_w11 * _kmax, XR12_fluid_conversion=[0.113, 0.080]),
    measured="high-resolution and SDSS/DESI quasar spectra; the 1D flux power at fixed mean transmission; small-scale power inferred through "
             "hydrodynamical IGM emulators", cite=["McDonald et al. 2005, ApJ 635, 761", "Palanque-Delabrouille et al. 2015, JCAP 11, 011",
             "Irsic et al. 2017, PRD 96, 023522", "Becker et al. 2013, MNRAS 430, 2067"],
    assumptions=["the IGM thermal history (T0, gamma) and pressure smoothing", "the UV background and patchy reionisation", "the mean "
                 "transmission", "FGPA-level modelling in the record's boxes"],
    fw_standing=f"M*'s switch passes (DE11b worst {_w11:.4f}; with FP6's own kernel the committed (1+z) argument under-weights MOND by up to "
                f"x{_kmax:.2f} at z = 2-3, so the corrected worst is ~{_w11 * _kmax:.3f} against 0.10 -- an estimate, XR34 re-scores it); the "
                "chain's forest 'passes' are linear per-mode proxies, not flux runs (not established, B06); the fluid's conversion sits at the "
                "line (11.3% / 8.0%, XR12)", lcdm_standing="the reference (emulators are LCDM-trained)",
    stake="deviations of 8-11% (XR12) against the record's 10% line", shift="the forest-only linear amplitude at k ~ 1 h/Mpc is known to "
    "+-14% after IGM marginalisation (McDonald et al. 2005: Delta_L^2 = 0.452 +0.069/-0.057 at z = 3)", budget_text="10-15%",
    equipment=["B05", "B06", "B07"], scorecard=["scorecard: Lyman-alpha forest (switch)", "scorecard: Lyman-alpha forest (fluid)",
    "charter: Lyman-alpha forest"], commits=["e35112739 (DE11b)", "b667f56bb (XR12)"])

# ---- A14 the first galaxies ---------------------------------------------------------------------------------------------------
X23B = jload("real_research/cross_thread_review_2026_09_26/XR23_mass_function_ceiling_results.json")["numbers"]["B1"]
_pub = X23B["published|Salpeter|7.5|z_eff|LCDM"]["eps_req"]
_rev = [v["eps_req"] for k, v in X23B.items() if k.startswith("revised|Salpeter|7.5|") and k.endswith("|LCDM")]
_rev = _rev[0] if _rev else float("nan")
_ch = [v["eps_req"] for k, v in X23B.items() if "Chabrier" in k and "|7.5|" in k and k.endswith("|LCDM")]
_ch = _ch[0] if _ch else _pub * 0.61
row("A14", "First galaxies (JWST)", "The abundance of massive galaxies at z ~ 7-10 against the baryon ceiling", cls="SOFT",
    numbers=dict(eps_published_salpeter=_pub, eps_chabrier=_ch, eps_revised=_rev, chain_equals_lcdm=True),
    measured="JWST NIRCam photometry (Labbe et al. 2023) with SED-fitted stellar masses; spectroscopic revisions (AGN, redshifts)",
    cite=["Labbe et al. 2023, Nature 616, 266", "Boylan-Kolchin 2023, Nat. Astron. 7, 731", "Kocevski et al. 2023, ApJ 954, L4",
          "Wang et al. 2024, ApJ 969, L13", "Carniani et al. 2024, Nature 633, 318"],
    assumptions=["the IMF (Salpeter vs Chabrier: x0.61)", "AGN contamination of the continuum", "photometric redshifts", "dust"],
    fw_standing="the chain's halo abundance equals LCDM's at M >= 1e11 Msun (XR23): the same ceiling", lcdm_standing="the same",
    stake=f"from eps = {_pub:.3f} to 1", shift=f"Chabrier masses give eps = {_ch:.3f}; the spectroscopically revised bin gives {_rev:.3f} "
    f"(a factor {_pub / _rev:.1f})", budget_text="IMF (0.21 dex) and revisions (0.67 dex)", equipment=["B03"],
    scorecard=["charter: First galaxies (JWST)"], commits=["6b7ab8243 (XR23)"])

# ---- A15 / A16 BBN and the GW speed ------------------------------------------------------------------------------------------
BBN = jload("real_research/cross_thread_review_2026_09_26/XR26_bbn_results.json")["numbers"]
row("A15a", "BBN", "Primordial helium and deuterium", cls="MODEL-INDEPENDENT",
    numbers=dict(pulls={k: v["pulls"] for k, v in BBN["B2"].items()}),
    measured="Y_P from HII-region He recombination lines; D/H from damped Lyman-alpha systems toward quasars",
    cite=["Aver et al. 2021, JCAP 03, 027", "Cooke, Pettini & Steidel 2018, ApJ 855, 102", "PDG 2024 (Fields, Molaro & Sarkar)"],
    assumptions=["the nuclear rates (d(p,gamma)3He dominates the D/H spread between PRIMAT and PArthENoPE)", "HII-region temperature structure"],
    fw_standing="standard BBN: the chain shifts Y_P by -1.6e-10 (XR26)", lcdm_standing="the same standard BBN", stake="any departure > 1e-3",
    shift="the D/H code spread (-2.1 to +1.0 sigma) is shared exactly by both models", budget_text="shared", equipment=[], scorecard=["charter: BBN"],
    commits=["68135cb7a (XR26 BBN)"])
row("A15b", "BBN", "Primordial lithium-7", cls="SOFT", numbers=dict(ratio=BBN["B3"]["ratio"], sigma=BBN["B3"]["sigma"]),
    measured="the Spite plateau of metal-poor halo stars", cite=["PDG 2024 eq. 24.4", "Fields et al. 2020, JCAP 03, 010", "Korn et al. 2006, Nature 442, 657"],
    assumptions=["stellar depletion (atomic diffusion, turbulent mixing)", "stellar atmosphere models"],
    fw_standing=f"inherits the factor {BBN['B3']['ratio']:.2f} ({BBN['B3']['sigma']:.1f} sigma) unchanged", lcdm_standing="the same factor",
    stake="0.26 dex (to 2 sigma)", shift="atomic diffusion depletes Li by ~0.2-0.3 dex in globular-cluster turn-off stars (Korn et al. 2006)",
    budget_text="~0.25 dex (shared)", equipment=[], scorecard=["charter: BBN"], commits=["68135cb7a (XR26 BBN)"])
row("A16", "GW speed", "The speed of gravitational waves (GW170817 / GRB 170817A)", cls="MODEL-INDEPENDENT",
    numbers=dict(bound=[-3e-15, 7e-16]), measured="the 1.7 s delay between the LIGO/Virgo merger and the Fermi/INTEGRAL gamma-ray burst at 40 Mpc",
    cite=["Abbott et al. 2017, ApJ 848, L13"], assumptions=["the intrinsic emission delay (bounded by the burst physics)"],
    fw_standing="c_T = c (FP2, XR25)", lcdm_standing="c_T = c", stake="any |c_T/c - 1| > 1e-15", shift="none", budget_text="none",
    equipment=[], scorecard=["charter: BBN, GW speed"], commits=["43cfa1692 (XR25)"])

# ---- A17 the Milky Way --------------------------------------------------------------------------------------------------------
X29F = jload("real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve_results.json")["numbers"]["fits"]
_mw = [f["Mstar_all"] for f in X29F if f.get("model") == "McM17"]
_gd = {f["data"]: f.get("gamma_data") for f in X29F if f.get("model") == "McM17" and f.get("foot") == "canonical"}
row("A17a", "Galaxies (Milky Way)", "The Milky Way's outer rotation curve (Gaia DR3, 13-27 kpc)", cls="CONTESTED",
    contested="the published DR3 curves disagree on the outer decline: power-law index -0.47 (Jiao et al. 2023) and -0.56 (Ou et al. 2024) "
              "against -0.19 to -0.40 in XR29's fits of the same tables; Eilers et al. 2019 and Zhou et al. 2023 decline more gently",
    numbers=dict(gamma_data_fits=_gd, published={"J23": -0.47, "O24": -0.56}, model_gamma=[-0.14, -0.09]),
    measured="Gaia DR3 astrometry + APOGEE/LAMOST velocities of disc tracers; Jeans-equation circular velocities",
    cite=["Eilers et al. 2019, ApJ 871, 120", "Zhou et al. 2023, ApJ 946, 73", "Jiao et al. 2023, A&A 678, A208", "Ou et al. 2024, MNRAS 528, 693",
          "Coquery & Blanchard 2025, A&A 703, A88"],
    assumptions=["axisymmetric equilibrium Jeans modelling", "the tracer density profile and velocity anisotropy", "disc non-equilibrium "
                 "(warp, flare)"], fw_standing="the law reproduces every curve's outer points at the fitted mass (XR29)",
    lcdm_standing="its NFW needs a concentration 1.9-3.8 sigma above the c-M relation (XR29)", equipment=[],
    scorecard=["charter: Galaxies (MW)"], commits=["633c161b5 (XR29)"])
gauss_row("A17b", "Galaxies (Milky Way)", "The Milky Way's stellar mass needed by the inner rotation curve, against the census", d=5.43e10,
          s=0.57e10, units="Msun", fw={"most favourable fit (XR29)": min(_mw), "least favourable fit (XR29)": max(_mw)},
          lcdm={}, budget={"census method spread (Licquia & Newman 6.08 vs McMillan 5.43)": 0.65e10},
          measured="structural censuses of the Galaxy's stellar mass (star counts, microlensing, dynamics): McMillan 5.43 +- 0.57, Cautun 5.04, "
                   "Licquia & Newman 6.08 +- 1.14, Bland-Hawthorn & Gerhard 5 +- 1 (x1e10)", cite=["McMillan 2017, MNRAS 465, 76",
                   "Cautun et al. 2020, MNRAS 494, 4291", "Licquia & Newman 2015, ApJ 806, 96", "Bland-Hawthorn & Gerhard 2016, ARA&A 54, 529"],
          assumptions=["the IMF and M/L of the disc", "the bulge/bar model", "R0 and V0 of the Sun"],
          fw_standing=f"the chain needs M* = {min(_mw) / 1e10:.2f}-{max(_mw) / 1e10:.2f} x1e10 (XR29); the 8-19 kpc slope misfits (-2.2 to -2.9 "
                      "against -1.7 km/s/kpc)", lcdm_standing="uses the census baryons; pays in concentration instead",
          equipment=[], scorecard=["charter: Galaxies (MW)"], commits=["633c161b5 (XR29)"])

# ---- A18 cosmic shear at small scales (the scorecard's shear row) --------------------------------------------------------------
MS4 = jload("real_research/mond_sector_gate_2026/MS4_smooth_gate_shear_results.json")["numbers"]["table"]
gauss_row("A18", "Large-scale structure", "Cosmic-shear power at k ~ 0.3-3 h/Mpc, z ~ 0.5 (the record's R(k) gate)", d=1.0, s=0.10,
          units="P_lens/P_LCDM (the record's +-20% gate = 2 x 0.10)", fail=False,
          fw={"M* capped, canonical (MS4)": MS4["0.25/2.5/1.75"]["canonical"], "M* capped, alt (MS4)": MS4["0.25/2.5/1.75"]["alt"],
              "M* capped, two-sided minimum (XR9)": XR9T["shear_min"]}, lcdm={"LCDM": 1.0},
          budget={"baryonic feedback on P(k) at k ~ 1 h/Mpc (van Daalen et al. 2011; marginalised by the surveys)": 0.10},
          measured="KiDS / DES / HSC shear two-point functions interpreted through a nonlinear P(k) model",
          cite=["van Daalen et al. 2011, MNRAS 415, 3649", "Asgari et al. 2021, A&A 645, A104"],
          assumptions=["the nonlinear matter power (HMcode) and its baryonic-feedback parameter", "intrinsic alignments"],
          fw_standing=f"M* passes with the kappa-form cap ({MS4['0.25/2.5/1.75']['canonical']:.3f}/{MS4['0.25/2.5/1.75']['alt']:.3f}); uncapped it "
                      f"fails ({MS4['0.25/2.5/inf']['canonical']:.2f}/{MS4['0.25/2.5/inf']['alt']:.2f}); a halo-model estimate, mock-based passes "
                      "are not established (MS3, DE5b)", lcdm_standing="the reference", equipment=["B07", "B10"],
          scorecard=["scorecard: cosmic shear (halo model, kappa cap)"], commits=["969a15e7f (MS4)", "e39cb4420 (XR9)"])
P(f"    {el()}")


# ====================================================================================================================== O  the own results
OWN = []


def own(oid, title, **kw):
    r = dict(id=oid, title=title)
    r.update(kw)
    OWN.append(r)
    return r


banner("O  THE FRAMEWORK'S OWN RESULTS (rule 0): the same equipment and model-dependence treatment, a class each, and what to keep")
_m1, _m2, _m3 = commit_msg("d266228be6"), commit_msg("9618b81d1a"), commit_msg("87812ee4ec")
_step = [grab(r"gamma =\s*(-?[0-9.]+)\+/-", _m1), grab(r"gamma =\s*-?[0-9.]+\+/-([0-9.]+) mag", _m1), grab(r"\(([0-9.]+) sigma\)", _m1)]
_pa, _pm = grab(r"partial corr\(HR, log g/a0 \| logM\) = ([+-][0-9.]+)", _m2), grab(r"partial corr\(HR, logM \| log g/a0\) = ([+-][0-9.]+)", _m2)
_pow = [grab(r"fires ([0-9]+)% of the time", _m3), grab(r"\(([0-9]+)% alt footing\)", _m3), grab(r"80% power needs D = ([0-9.]+) mag", _m3)]
src("real_research/snia_massstep_acceleration_test.py"); src("real_research/snia_hoststep_sizextmatch.py")
src("real_research/snia_hoststep_localSB.py"); src("real_research/reviews/mi_snia_power_curve_2026.py")
own("O1", "The SN-Ia host-mass step at the a0 scale", cls="MODEL-INDEPENDENT",
    numbers=dict(step_mag=_step[:2], step_sigma=_step[2], partial_accel_given_mass=_pa, partial_mass_given_accel=_pm,
                 power_percent=_pow[:2], D_for_80pc_power=_pow[2], crossing_logMstar=[9.6, 10.2], step_logMstar=10.0),
    measured="Pantheon+ (N = 1548 Hubble-flow SNe), re-standardised from the raw SALT2 parameters (mu = mB + alpha x1 - beta c; the released "
             "MU already removes the step through its bias corrections); host masses from the release; hosts matched to SDSS DR17 by "
             "position for sizes (N = 449) and local surface brightness (N = 450)",
    cite=["commit d266228be6 (the step)", "commit 9618b81d1a (fixed-mass test)", "commit 405b304f1b (local SB)", "commit 87812ee4ec (power)",
          "Scolnic et al. 2022, ApJ 938, 113", "Brout et al. 2022, ApJ 938, 110", "Kelly et al. 2010, ApJ 715, 743", "Sullivan et al. 2010, MNRAS 406, 782"],
    assumptions=["SALT2 standardisation (alpha, beta)", "SED host masses (IMF, SPS)", "the disc mass-size relation that turns M* into g_bar",
                 "host association by position (SDSS)"],
    standing=f"a real step of {_step[0]:+.3f} +- {_step[1]:.3f} mag ({_step[2]} sigma) sits where g_bar crosses a0 (log M* 9.6-10.2 vs the step "
             f"at 10); the decisive fixed-mass test finds acceleration adds nothing beyond mass (partial {_pa:+.3f} vs mass {_pm:+.3f}) but "
             f"has only {_pow[0]:.0f}% ({_pow[1]:.0f}% alt) power against the framework's own step model",
    shift="the crossing mass moves with the mass-size relation (+-0.3 dex) and the footing (Sigma_a0 x1.21 on the alt footing); the step's "
          "amplitude moves with the standardisation (Pantheon+'s bias correction carries -0.070 mag)",
    lcdm_same="LCDM reads the same step as a progenitor age / dust / metallicity effect; the fixed-mass null is equally consistent with it",
    note="the step is model-independent; its a0 ATTRIBUTION is untested (underpowered), not refuted",
    keep=f"keep the step ({_step[0]:+.3f} +- {_step[1]:.3f} mag at log M* ~ 10); any construction that ties it to a0 must predict a fixed-mass "
         f"acceleration dependence, which the present sample cannot see (80% power needs a {_pow[2]:.3f} mag step)")
_env = grab(r"ρ_local excluded \*\*([0-9]+)–[0-9]+σ\*\*", ET, cast=int), grab(r"ρ_local excluded \*\*[0-9]+–([0-9]+)σ\*\*", ET, cast=int)
src("real_research/predictions/a0_environmental_fork_test.py"); src("real_research/predictions/project_bigsparc_a0_environment.py")
own("O2", "The environmental null: a0 tracks rho_Lambda, not the local density (the BIG-SPARC pipeline)", cls="MODEL-INDEPENDENT",
    numbers=dict(rho_local_excluded_sigma=list(_env), predicted_rho_local_slope=0.5),
    measured="per-galaxy deep-MOND a0 fits on 175 SPARC galaxies against internal surface density, Ursa Major cluster membership and the "
             "NGC 1052 group; the BIG-SPARC (~4000 galaxies) pipeline is frozen and waits for the release",
    cite=["commit 542c9f343b (a0_environmental_fork_test.py)", "commit 3d8c0388f0 (project_bigsparc_a0_environment.py)",
          "EMPIRICAL_TESTS.md A14", "Li et al. 2018, A&A 615, A3", "Haubner, Lelli et al. 2024, arXiv:2411.13329 (BIG-SPARC)"],
    assumptions=["M/L (the naive correlation vanishes in gas-dominated and Q = 1 subsamples)", "distances and inclinations",
                 "the EFE confound (environment also enters through the external field)"],
    standing=f"the rho_local fork (d log a0/d log rho_env = +1/2) is excluded at {_env[0]}-{_env[1]} sigma on 175 SPARC; no committed .out "
             "(the number is the committed ledger EMPIRICAL_TESTS.md A14)",
    shift="a +1/2 slope over the density range probed is far beyond the ~0.1 dex M/L systematics; residual trends of 0.02-0.05 dex need BIG-SPARC",
    lcdm_same="LCDM has no a0; its emergent RAR scale is also environment-independent in simulations",
    note="the no-circularity rule holds: a0 from each galaxy's own points, density from an external catalogue",
    keep="a0 must not depend on the ambient density (|d log a0/d log rho_env| << 1/2); the source is the cosmic rho_Lambda")
ST = text("STANDING.md")
_kb = grab(r"κ is \*\*measured\*\*: ([0-9.]+) ± ([0-9.]+) \(BTFR\)", ST), grab(r"κ is \*\*measured\*\*: [0-9.]+ ± ([0-9.]+) \(BTFR\)", ST)
_kd = grab(r"and ([0-9.]+) ± [0-9.]+ \(distance-free\)", ST), grab(r"and [0-9.]+ ± ([0-9.]+) \(distance-free\)", ST)
PN = text("qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2/paper_numbers.out")
_kbud = {n: grab(rf"{re.escape(n)} ([0-9.]+)", PN) for n in ("disc M/L", "bulge M/L", "full M/L grid half-range", "bootstrap over galaxies")}
_disc = [grab(r"Δχ² ([0-9.]+) vs ([0-9.]+)", ET, group=1), grab(r"Δχ² ([0-9.]+) vs ([0-9.]+)", ET, group=2)]
own("O3", "The measured kappa", cls="SOFT",
    numbers=dict(btfr=_kb, distance_free=_kd, distance_free_budget=_kbud, discriminability_dchi2=_disc, fitted=0.5,
                 pulls_of_half=dict(btfr=(0.5 - _kb[0]) / _kb[1], distance_free=(0.5 - _kd[0]) / _kd[1])),
    measured="SPARC (Q <= 2, i >= 30 deg): the BTFR intercept (M_bar = Upsilon_d L + 1.4 Upsilon_d L_bul + 1.33 M_HI, Upsilon_d = 0.70) and a "
             "distance-free g_bar estimator; kappa from a0 = kappa c sqrt(G rho_Lambda)",
    cite=["commit 62f905dd9b (mi_btfr_intercept_kappa_door_2026.py; no committed .out)", "commit a49751b6c (paper_numbers.out)",
          "commit 2b25fb72e (mi_a0_profile_likelihood_sparc_2026.py)", "commit ed238836d2 (the H0-convention audit)", "STANDING.md rev. 9"],
    assumptions=["disc and bulge M/L (the bulge M/L cannot be pinned)", "the helium factor and gas scale", "H0 (a Planck-consistent H0 moves "
                 "0.465 -> 0.450 and 0.551 -> 0.591)", "the interpolating function"],
    standing=f"kappa = 1/2 is FITTED and sits {abs(0.5 - _kb[0]) / _kb[1]:.2f} sigma from the BTFR value and {abs(0.5 - _kd[0]) / _kd[1]:.2f} sigma "
             f"from the distance-free one; the two estimators share galaxies (not independent); 1/2 vs 1/(2 pi): Delta chi^2 {_disc[0]} vs {_disc[1]} "
             "(~2.2 sigma, forecast-grade)",
    shift=f"the distance-free value's error is M/L-dominated (bulge {_kbud['bulge M/L']}, grid half-range {_kbud['full M/L grid half-range']}); the "
          "superseded 0.551 +- 0.043 held the bulge M/L fixed; EMPIRICAL_TESTS.md's header value 0.529 +- 0.034 is a hard-coded string (see B18)",
    lcdm_same="no counterpart (LCDM predicts no a0)", note="kappa stays FITTED; it is underivable in the record's actions (k01-k03)",
    keep=f"any construction that ties kappa must land inside {_kb[0]} +- {_kb[1]} (BTFR) and {_kd[0]} +- {_kd[1]} (distance-free); the record "
         "carries kappa = 1/2 as fitted")
ZE = text("real_research/z2_eta_2026/Z2ETA_eta_bound_a0.out")
_zg = grab(r"measured: ([0-9]+) / 2 required", ZE, cast=int)
_zp = [grab(r"median \+- se = ([+-][0-9.]+) \+- ([0-9.]+) dex", ZE, group=1), grab(r"median \+- se = ([+-][0-9.]+) \+- ([0-9.]+) dex", ZE, group=2)]
_s4i = [grab(r"one at 0\.13: ([0-9.]+):1", PN), grab(r"three at 0\.10: ([0-9.]+):1", PN)]
own("O4", "Flat a0(z): the z ~ 2.5 deep-MOND BTFR zero point and the MUSE confrontation", cls="CONTESTED",
    contested="MUSE-DARK III measures a rising a0 (a1 = +1.59 +- 0.105 x1e-10 per unit z) while McGaugh et al. 2024 and the record's KMOS3D "
              "archive are flat to declining (see A04)",
    numbers=dict(registered_test_objects=[_zg, 2], proxy_offset_dex=_zp, framework=0.00, lcdm_native=0.33, odds_one_object_0p13=_s4i[0],
                 odds_three_objects_0p10=_s4i[1], muse_a1=[1.59, 0.105]),
    measured="high-z rotators (KMOS3D, RC100, lensed discs) placed on the deep-MOND BTFR; the registered test needs deep-MOND objects "
             "(g_bar/a0 < 0.3) at z >= 2",
    cite=["commit 9f7572c58 (Z2ETA_eta_bound_a0.out)", "commit 8e6a39952 (PAPER7 v3, DOI 10.5281/zenodo.22833314)",
          "commit d8097e02c (PAPER14 v2 correction)", "commit a49751b6c (paper_numbers.out S4i)", "real_research/A0Z_MUSE_DARK_III_CONFRONTATION.md"],
    assumptions=["M/L and molecular gas at z ~ 2.5", "pressure support and beam smearing", "lens magnification", "disc-size evolution"],
    standing=f"the registered test cannot run ({_zg} of 2 deep-MOND rotators); the on-disk proxy ({_zp[0]:+.3f} +- {_zp[1]:.3f} dex) is at high "
             "acceleration and is NOT the registered test; the framework predicts 0.00 against LCDM-native +0.33 dex",
    shift=f"PAPER14 v2 corrected the one-object claim: with intrinsic and halo-to-halo scatter one object at 0.13 dex gives {_s4i[0]}:1, three "
          f"at 0.10 dex give {_s4i[1]}:1; STANDING.md's '20:1 from one object' is stale (B18)",
    lcdm_same="LCDM's apparent a0 rises (Magneticum); a flat deep-MOND zero point at z ~ 2.5 needs halo dilution to 0.61 of N-body in LCDM",
    note="CFG6's a0 ~ sqrt(rho_DE(z)) branch gives 0.87 of today's a0 at z = 2 on DESI's w0wa; the unimodular tie keeps it flat",
    keep="a0(z) flat to < 1% for z <= 5 on a true Lambda (the distinctive prediction); the decisive test needs 3 deep-MOND rotators at +-0.10 "
         "dex or 4 at +-0.20 dex at z ~ 2.5")
H12 = text("hunt_2026/h12_h14_satellites_and_oort.out")
_oq = [grab(r"Oort-spike LPCs \(a > 10\^4 AU\)\s+N =\s+60: quadrupole along g_ext = ([+-][0-9.]+) \+- ([0-9.]+)", H12, group=i) for i in (1, 2)]
_oj = [grab(r"Jupiter-family CONTROL\s+N =\s+927: quadrupole along g_ext = ([+-][0-9.]+) \+- ([0-9.]+)", H12, group=i) for i in (1, 2)]
_on = grab(r"so N ~ ([0-9]+) spike comets are needed", H12, cast=int)
own("O5", "The Oort-cloud comet anisotropy as an external-field instrument (DOI 10.5281/zenodo.21966646)", cls="SOFT",
    numbers=dict(spike_quadrupole=_oq, jfc_control_quadrupole=_oj, predicted_A=0.12, N_needed=_on, nu0_bound=2.36e-6),
    measured="aphelion directions of 60 Oort-spike long-period comets (JPL SBDB, osculating elements) about the Galactic-centre axis",
    cite=["commit f33d4e86a (h12_h14_satellites_and_oort.out)", "commit e32db65d12 (OORT_CLOUD_EFE_INSTRUMENT.md)",
          "commit 9be932ff7 (stage76: nu0 <= 2.36e-6)", "Wiegert & Tremaine 1999, Icarus 137, 84"],
    assumptions=["survey selection (the Jupiter-family control shows a 14-sigma quadrupole)", "osculating vs original 1/a (the spike "
                 "position is not runnable from SBDB)", "the Newtonian Galactic-tide anisotropy, to be modelled and subtracted"],
    standing=f"spike quadrupole {_oq[0]:+.4f} +- {_oq[1]:.4f} (0.7 sigma) against a predicted A ~ 0.12: UNDERPOWERED (N ~ {_on} needed), "
             "recorded as such, not as a null; the nu0-correlated pair with DR4 collapses to 16.7%, indistinguishable from constant-a0 17%, "
             "once stage76's nu0 bound applies",
    shift=f"selection dominates: the JFC control's quadrupole {_oj[0]:+.3f} +- {_oj[1]:.3f} exceeds the predicted signal",
    lcdm_same="GR predicts only the Newtonian tide anisotropy; the same selection function applies",
    note="three of the lane's checks pass on a literal True (reported by the search; the numbers above are the measured lines)",
    keep="no constraint yet; a prospective instrument that needs original 1/a and ~3000 spike comets")
FF = text("prep_2026/aligned_firing/FIRST_FIRING.md")
WB = text("prep_2026/wallaby_firing/fire_wallaby.out")
_a16 = [grab(r"Ahat = ([+-][0-9.]+) \(perm p1 = ([0-9.]+), p2 = ([0-9.]+)", FF, group=i) for i in (1, 2, 3)]
_w = re.search(r"ALL \| canonical a0=9\.36e-11 \| maxclu\s+([0-9]+)\s+([+-][0-9.]+)\s+([0-9.]+)\s+[0-9.]+\s+[+-][0-9.]+\s+([0-9.]+)", WB)
_a25 = [int(_w.group(1)), float(_w.group(2)), float(_w.group(3)), float(_w.group(4))]
own("O6", "The directional external-field test (rotation-curve asymmetry toward the external field)", cls="CONTESTED",
    contested=f"the record's two firings disagree in sign: n = 16 (WHISP) Ahat = {_a16[0]:+.2f} (one-sided p = {_a16[1]}); n = {_a25[0]} (WALLABY) "
              f"Ahat = {_a25[1]:+.2f} +- {_a25[2]:.2f} (p = {_a25[3]}) -- the first did not reproduce",
    numbers=dict(n16=dict(Ahat=_a16[0], p1=_a16[1], p2=_a16[2]), n25=dict(n=_a25[0], Ahat=_a25[1], sd=_a25[2], p=_a25[3]),
                 mi_dipole_percent=[4.2, 22.3], N_needed=dict(stale=1157, route_A=[1385, 1705], R1R2=6000)),
    measured="per-side HI kinematics (WHISP; WALLABY) stacked with a matched filter on the external-field direction (Chae et al. 2021 "
             "amplitudes; 2M++ directions), with an isotropic permutation null",
    cite=["commit f617640aeb (fire_aligned_n16.py, FIRST_FIRING.md, fire_wallaby.out)", "commit 8dd40f7b0c (mi_efe_derived_general_2026)",
          "commit d7733f9f48 (the Route A re-solve)", "van Eymeren et al. 2011, A&A 530, A29"],
    assumptions=["the external-field reconstruction (direction and amplitude)", "a direction-blind systemic-velocity offset (mean A = +0.092 "
                 "diagnosed in the n = 25 sample)", "Virgo dominates the n = 16 sample (15 of 16)"],
    standing="an exploratory ~2-sigma-at-best hint that did not reproduce; the AQUAL floor signal registers at only ~0.3 sigma in the n = 16 "
             "stack; 'pure MI predicts exactly zero' was retracted (the derived dipole is 4.2-22.3%)",
    shift="the vsys-corrected diagnostic moves the n = 25 stack from -1.70 to +0.42; the external-field reconstruction owns the amplitude",
    lcdm_same="GR predicts no dipole: both firings are consistent with zero",
    note="EMPIRICAL_TESTS.md C2 ('fired once') omits the n = 25 non-reproduction in the same commit; N ~ 1157 is stale (B18)",
    keep="no constraint yet (consistent with zero); a construction's predicted dipole (4-22% for the MI class) needs ~1400-6000 galaxies")
_rA = [grab(r"Route A \*\*([0-9.]+)σ\*\* canonical", ST), grab(r"and ([0-9.]+)σ alt, while", ST)]
_rp = grab(r"on 3 effective dof, \$p=([0-9.]+)\$", ST)
_rf = [grab(r"\*\*([0-9.]+) / ([0-9.]+)\*\*, above the highest", ST, group=i) for i in (1, 2)]
_a12 = [grab(r"\*\*\+([0-9.]+)σ\*\*; Eilers rotation-curve slope \+([0-9.]+)σ", ET, group=i) for i in (1, 2)]
src("real_research/reviews/mi_vertical_force_resolved_2026.py"); src("real_research/reviews/mi_aqual_mond_refit_2026.py")
src("real_research/reviews/mi_routeA_box_clearance_verified_2026.py")
own("O7", "The Milky Way's local vertical force", cls="SOFT",
    numbers=dict(full_aqual_sigma=_a12[0], eilers_slope_sigma=_a12[1], routeA_box_sigma=_rA, routeA_p=_rp, kernel_floor_Sigma_dyn=_rf,
                 data=dict(holmberg_flynn=[74, 6], bovy_rix=[68, 4], mcmillan_fit=73.9), f_M_needed=1.3),
    measured="the dynamical surface density within |z| < 1.1 kpc at R0 from vertical kinematics of disc stars (Holmberg & Flynn 2004; Bovy & "
             "Rix 2013), with the rotation-curve normalisation v_c(R0)",
    cite=["commit ccfe387ef0 (mi_vertical_force_resolved_2026.py)", "commit d7733f9f48 (mi_aqual_mond_refit_2026.py)", "EMPIRICAL_TESTS.md A12",
          "STANDING.md (Route A box)", "Holmberg & Flynn 2004, MNRAS 352, 440", "Bovy & Rix 2013, ApJ 779, 115", "Lisanti et al. 2019, PRD 100, 083009"],
    assumptions=["the disc's stellar surface density prior (38 +- 4)", "the stellar-mass budget (f_M ~ 1.3 needed by the radial normalisation)",
                 "which vertical-force determination (68 +- 4 vs 74 +- 6)"],
    standing=f"full AQUAL on McMillan-2017 baryons matches the vertical force at +{_a12[0]} sigma (Eilers slope +{_a12[1]} sigma) but only with "
             f"~30% more stellar mass for v_c; Route A's joint box clears at {_rA[0]} sigma (p = {_rp}, a minimax criterion) and its floor "
             f"Sigma_dyn(1.1 kpc) {_rf[0]}/{_rf[1]} exceeds Bovy & Rix's 68 +- 4",
    shift="the vertical-force datum (68 +- 4 vs 74 +- 6) and the +-10-20% stellar-mass budget move the verdict across the gate",
    lcdm_same="LCDM fits both with a halo; the same stellar-mass prior", note="the MW's radial normalisation need is the same as XR29's (A17b)",
    keep="Sigma_dyn(|z| < 1.1 kpc) = 68-74 (+-4-6) Msun/pc^2 at R0 with census-compatible baryons, jointly with v_c(R0)")
FT = text("real_research/reviews/mi_forest_total_acceleration_2026.out")
FK = text("real_research/reviews/mi_forest_a0_footing_forks_2026.out")
_bs = [grab(r"statistical channel \(Hiss Table 4 \+err, 0\.33-1\.37 km/s\) : ([0-9.]+) - ([0-9.]+) sigma", FT, group=i) for i in (1, 2)]
_bc = [grab(r"calibration channel \(3\.36 km/s method systematic\) : ([0-9.]+) - ([0-9.]+) sigma", FT, group=i) for i in (1, 2)]
_sign = "sign is robust; the magnitude is convention-owned" in FK
own("O8", "The Lyman-alpha forest b-cutoff sign", cls="SOFT",
    numbers=dict(statistical_sigma=_bs, calibration_sigma=_bc, calibration_kms=3.36, sign_robust=_sign, withdrawn="6-8 sigma"),
    measured="the lower cutoff b0(z) of the Doppler-parameter distribution of forest absorbers (Hiss et al. 2018, 8 bins at z = 2.0-3.4), "
             "against the framework's gas acceleration at the forest's density",
    cite=["commit 20d8b52da5 (mi_forest_total_acceleration_2026.out and the convention audits)", "Hiss et al. 2018, ApJ 865, 42",
          "Rudie et al. 2012, ApJ 750, 67", "RETRACTIONS.md (the withdrawn 6-8 sigma)"],
    assumptions=["the b0 calibration (Hiss vs Rudie: 3.36 km/s)", "which acceleration counts for forest gas (the x-convention spans 3.4 dex)",
                 "the reference column density"],
    standing=f"the framework's b sits above the measured b0 in every bin (the sign is robust) at {_bs[0]}-{_bs[1]} sigma on the statistical "
             f"channel but only {_bc[0]}-{_bc[1]} sigma on the calibration channel; the magnitude is convention-owned (a factor ~32)",
    shift="the 3.36 km/s calibration systematic exceeds every statistical bar", lcdm_same="thermal broadening alone: no cutoff shift",
    note="a weak, convention-dominated tension, not an exclusion", keep="the b0 cutoff sign (framework b above b0) must not grow beyond the "
    "calibration channel's 0.4-0.9 sigma in a construction's forest-gas acceleration")
for _o in OWN:
    P(f"  {_o['id']}  [{_o['cls']:17s}] {_o['title']}\n        standing: {_o['standing']}\n        keep:     {_o['keep']}")
P(f"    {el()}")


# ====================================================================================================================== B  the equipment
banner("B  THE RECORD'S OWN EQUIPMENT (Part B): the computational approximations that decided or bent verdicts; status and commits")
M6 = N18["M6"]
_h, _Om, _Ob, _omb, _Tc, _ns, _s8 = (M6[k] for k in ("h", "Om", "Ob", "om_b", "T_CMB", "ns", "SIG8"))


def T_textbook(kh):
    """Eisenstein & Hu 1998 no-wiggle transfer as published: q = (k / h Mpc^-1) Theta^2 / Gamma_eff (eq. 28), and the sound-horizon
    term 0.43 k s with k in Mpc^-1 (eq. 31) -- the two places FP6's T_EH98 is called with the wrong units (XR23's flag)."""
    th = _Tc / 2.7
    s = 44.5 * math.log(9.83 / (_Om * _h * _h)) / math.sqrt(1 + 10 * _omb ** 0.75)
    ag = 1 - 0.328 * math.log(431 * _Om * _h * _h) * (_Ob / _Om) + 0.38 * math.log(22.3 * _Om * _h * _h) * (_Ob / _Om) ** 2
    ge = _Om * _h * (ag + (1 - ag) / (1 + (0.43 * kh * _h * s) ** 4))
    q = kh * th * th / ge
    L = math.log(2 * math.e + 1.8 * q)
    return L / (L + (14.2 + 731.0 / (1 + 62.5 * q)) * q * q)


_lk = np.linspace(math.log(1e-4), math.log(100.0), 6000)
_kk = np.exp(_lk)
_W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_Pc = np.array([k ** _ns * M6["T_EH98"](k * _h) ** 2 for k in _kk])
_Pt = np.array([k ** _ns * T_textbook(k) ** 2 for k in _kk])
_cl = X26["cl_fid"]
_hc = X26["H_FID"]
_kk30 = _kk[_kk <= 25.0]
_Pcl = np.array([_cl.pk_lin(k * _hc, 0.0) * _hc ** 3 for k in _kk30])
_norm = lambda P, kk, lk: math.sqrt(np.trapz(kk ** 3 * P * _W(8 * kk) ** 2 / (2 * math.pi ** 2), lk[:len(kk)]))
_nc, _nt, _ncl = _norm(_Pc, _kk, _lk), _norm(_Pt, _kk, _lk), _norm(_Pcl, _kk30, _lk)
EH = {}
for _q in (0.01, 0.1, 1.0, 10.0, 100.0):
    _i = int(np.argmin(abs(_kk - _q)))
    EH[str(_q)] = dict(vs_textbook=float((_Pc[_i] / _nc ** 2) / (_Pt[_i] / _nt ** 2)),
                       vs_CLASS=(float((_Pc[_i] / _nc ** 2) / (_Pcl[_i] / _ncl ** 2)) if _q <= 25 else None))
EQUIP = []


def equip(bid, name, **kw):
    r = dict(id=bid, name=name)
    r.update(kw)
    EQUIP.append(r)
    return r


_p3s = [v[2] for v in X21["P3"]["H_S vs FP13 H4"].values()]
_p3y = [v[2] for v in X21["P3"]["H_Y vs FP9 H2c"].values()]
equip("B01", "FP9/FP13's per-mode linear yardstick against XR21's real-space operator", status="OPEN",
      what="the per-mode rule evaluates each mode's MOND kernel at that mode's own field; the model's real-space operator responds to every "
           "mode with one coefficient set by the whole band-passed field",
      numbers=dict(real_over_permode_b=dict(H_S=[min(_p3s), max(_p3s)], H_Y=[min(_p3y), max(_p3y)]),
                   cmb_lensing_f_eff=dict(all_matter=[min(_fa), max(_fa)], baryons_only=[min(_fb), max(_fb)]),
                   cmb_lensing_amplitudes=AMPMAP),
      quantified=f"real/per-mode boost b = {min(_p3s):.2f}-{max(_p3s):.2f} (H_S) and {min(_p3y):.2f}-{max(_p3y):.2f} (H_Y) at k = 0.3-1, z = 0-0.25 "
                 f"(XR21 P3); mapped onto XR26's own A(f), CMB lensing moves from {a26['lin']:.3f} / {a26['NL']:.3f} (per-mode) to "
                 f"{AMPMAP['real-space, all matter (lowest mapped f)']['lin']:.3f}-{AMPMAP['real-space, all matter (highest mapped f)']['lin']:.3f} "
                 f"(linear) / {AMPMAP['real-space, all matter (lowest mapped f)']['NL']:.3f}-{AMPMAP['real-space, all matter (highest mapped f)']['NL']:.3f} "
                 "(halofit), all matter",
      verdicts=["FP9/FP13/FP19 sigma_8 passes: conservative (the true linear boost is smaller) -- they stand",
                "FP9/FP13/FP19 forest-proxy passes: optimistic (the real-space rms field reaches the yield at z ~ 1-2) -- NOT established",
                "XR26's CMB-lensing FAIL: its magnitude (+4.9 / +40 sigma) is yardstick-dependent; with the real-space operator it persists on the "
                "halofit base in the all-matter reading"],
      commits=["b4bf5b2ae (XR21, flag)", "27faacc84 (FP13)", "b510eebfe (FP9)", "0c18c582f (FP19)", "68135cb7a (XR26)"],
      pending="FP22 (bfe9a2fe5) re-scored sigma_8, the forest and CMB lensing on both yardsticks (the real-space cut f_eff = 0.52-1.35 of the "
              "per-mode phantom in the all-matter reading, 0.13-0.26 in the baryons-only one); XR21 stage 2 is the nonlinear arbiter")
_v4 = R20["V4"]["L352"]
equip("B02", "The Abel projection defect: FP6's esd_of_M (P1) and L352's project_M2 / DE8's esd_from_mlens (P2)", status="P1 FIXED; P2 PENDING",
      what="P1 treated the projected mass inside 20 kpc as a flat disc and skipped the 1/sqrt end interval; P2 shares the end-interval defect "
           "and its inner term is exact only for Sigma ~ 1/R",
      numbers=dict(P1_sis_percent_35kpc=sis35, P2=_v4, flips=R20.get("R10_flips")),
      quantified=f"P1: SIS {sis35:+.1f}% at 35 kpc, -4 to -14% outside (reproduced here, K2); P2: SIS {_v4['SIS V=200'][0]:+.2f}..{_v4['SIS V=200'][1]:+.2f}%, "
                 f"NFW up to {max(v[1] for k, v in _v4.items() if k.startswith('NFW')):+.1f}%, carrier templates "
                 f"{_v4['carrier cap x_v0=700 (L360 bin 4)'][1]:+.0f}% / {_v4['carrier cleared x_v0=1000 (L360 bin 4)'][0]:+.0f}% at 35 kpc",
      verdicts=["P1 (FP6/FP9/FP11-FP14/FP17, L355/L357/AT1/AT3): re-scored by FP20 -- no deciding verdict flips; L360's passing pairs 70 -> 35, "
                "FP13's A3 window edges and FP11 P1's band edge flip",
                "P2 (L352/L359/L360/AT3's switched gate/DE8/DE10/XR9/XR14/XR28/XR29, FP15/FP16/FP19 via kids_switched): NOT re-scored -- M*'s "
                "'KiDS pass ON M*' (XR14), DE10's -37/-34 and XR9's KiDS cap 4.42 are NOT established until XR35"],
      commits=["09990b398 (FP18, found)", "7a8c25321 (FP20, fixed P1)", "42480dcd8 (answer page correction)", "3924bb8c2 (FP20b)"],
      pending="FP20b (3924bb8c2) re-scored FP15/FP16/FP19 with the exact projector: no headline verdict flips (FP16's KiDS passes hold at every "
              "kick); XR35 (DE10 -> XR9 -> XR14, M*'s path) is in flight")
equip("B03", "The T_EH98 h-units error in the record's linear spectrum", status="PENDING",
      what="FP6's T_EH98 (from L341; also in FP3/FP7/FP9 and the bs_khronon lanes) is called with k in 1/Mpc but evaluates EH98's q with k "
           "where h/Mpc is required and the sound-horizon term with an extra 1/h",
      numbers=dict(ratio_at_fixed_sigma8=EH),
      quantified="the committed spectrum over the textbook form at fixed sigma_8: " + ", ".join(f"k = {k}: {v['vs_textbook']:.2f}" for k, v in EH.items())
                 + " h/Mpc; over CLASS: " + ", ".join(f"{k}: {v['vs_CLASS']:.2f}" for k, v in EH.items() if v["vs_CLASS"] is not None),
      verdicts=["FP13's state at high z (z_close 17.4 vs 13.6 on the textbook spectrum) and A6 -- absolute scales, NOT established",
                "sigma_8 and forest ratios to LCDM on the same spectrum partly cancel (FP22 C0, bfe9a2fe5: 1.0202 -> 1.0177 for H_S)",
                "XR26's B(k, z) was built on T_EH98 (FP22 L2 on CLASS, bfe9a2fe5: CMB lensing 1.149 -> 1.172 linear, 2.134 -> 2.373 halofit: "
                "the error UNDER-stated the all-matter lensing failure)"],
      commits=["6b7ab8243 (XR23, flag)", "9d9e75369 (FP6)"], pending="FP24 (transfer-function fix) is in flight")
_ra = {}
for _key in ("0.0/0.3", "0.0/0.5", "0.0/1.0", "0.25/0.3", "0.25/0.5", "0.25/1.0"):
    _b3 = X21["P4"]["real_HS_chain_canonical"][_key]
    _a2 = X21["P4"]["real_HS_chain_canonical"][_key + "/fp9"]
    _ra[_key] = dict(matter=_b3[0] / _a2[0], lensing=_b3[2] / _a2[1])
equip("B04", "Who feels MOND: the all-matter reading (FP9/FP13's yardstick) against the baryons-only reading (FP10's reciprocity)",
      status="DECIDED (FP22 bfe9a2fe5; the chain adopts the baryons-only reading, 08548fc85)",
      what="FP9/FP13 source and apply the MOND scalar with the total delta; FP10's dark sector neither sources nor feels it",
      numbers=dict(baryons_over_allmatter=_ra),
      quantified="the baryons-only reading cuts the total-matter boost to " + f"{min(v['matter'] for v in _ra.values()):.3f}-{max(v['matter'] for v in _ra.values()):.3f}"
                 + " of the all-matter one but the LENSING boost only to " + f"{min(v['lensing'] for v in _ra.values()):.2f}-{max(v['lensing'] for v in _ra.values()):.2f}"
                 + " (XR21 P4, real space, H_S)",
      verdicts=["FP7's sigma_8 failure (18-27x): the reading does not remove the need for a separator (FP22: (b) still fails at 1.45-2.2x without one)",
                "XR26's CMB lensing: the action AS WRITTEN (all matter) is excluded in every cell (FP22); in the adopted baryons-only reading the "
                "linear base passes Planck and ACT and the halofit base fails ACT -- the verdict hinges on the nonlinear phantom (A11)",
                "FP10/FP15/FP16's dark orbits are Newtonian: the adopted reading; its price is a dark-baryon equivalence-principle violation "
                "wherever the phantom is on (X-COP median 0.47 at R500; FP22 A5)"],
      commits=["b4bf5b2ae (XR21, flag)", "bfe9a2fe5 (FP22)", "08548fc85 (adoption)", "b3f5759a4 (FP16)", "df13605e0 (FP10 full)"],
      pending="none for the reading; the nonlinear phantom (XR21 stage 2) decides CMB lensing in it")
equip("B05", "The (1+z) kernel-argument error in the record's forest PM codes", status="PENDING",
      what="L346, L347, L358 (via L347's run), L359, L362, DE11 and DE11b feed the kernel |grad phi_N|/a^2 = (1+z) x the physical field",
      numbers=dict(factor_from_FP6_kernel=KFAC, DE11b_worst=_w11, DE11b_estimate=_w11 * _kmax),
      quantified=f"with FP6's own P2 kernel, (nu(y) - 1)/(nu((1+z)y) - 1) = {KFAC['2.0'][0]:.2f}-{KFAC['2.0'][1]:.2f} at z = 2 and "
                 f"{KFAC['3.0'][0]:.2f}-{KFAC['3.0'][1]:.2f} at z = 3 over XR34's halo range of y; DE11b's worst {_w11:.4f} scales to ~{_w11 * _kmax:.3f} "
                 "(an estimate) against 0.10",
      verdicts=[f"DE11/DE11b forest PASS: very likely survives (margin ~{0.10 / (_w11 * _kmax):.0f}x after the factor) -- pending XR34's re-score",
                "L347 (borderline at x_c = 5), L358's failing cell (0.174), L362's pincer, L359's forest window, DE2's constant-threshold table, "
                "L360's window and PAPER34's forest numbers: deviations UNDER-stated -- their failures stand or worsen, their borderline passes "
                "are NOT established",
                "fable_independent_2026 L176/L178/L179 (matter power, lensing): same line, not in the forest"],
      commits=["b4bf5b2ae (XR21, flag)", "aa6588d56 (DE11)", "e35112739 (DE11b)", "b48b224c5 (L347)", "c3a5ce8a8 (L362)", "b13dc17af (L359)",
               "8644887d5 (L346)"], pending="XR34 (uncommitted, running): confirms the bug (QUMOND kick 33-43% low at z = 2-3) and re-scores")
equip("B06", "Linear forest proxies against flux runs", status="OPEN",
      what="FP9/FP13/FP19 score the forest as 'the IGM sits below the yield' on the linear per-mode field; no flux run of the chain exists",
      quantified="XR21: the real-space rms field reaches H_Y's yield near z ~ 2 and H_S's near z ~ 1, so the proxies' 'forest 0' does not "
                 "carry over; XR12's halo-model flux proxy for the fluid's conversion sits at 11.3% / 8.0% against the 10% line",
      verdicts=["the chain's forest PASS (FP9/FP13/FP19): NOT established", "the fluid's own conversion on the forest (XR12): NOT established"],
      commits=["b4bf5b2ae (XR21)", "b667f56bb (XR12)"], pending="XR21 stage 2, set C (the forest box)")
equip("B07", "Halo-model and semi-analytic estimates against particle-mesh runs", status="OPEN",
      what="cosmic shear (MS3/MS4 halo model; retention taken at z = 0/2 and scored at z = 0.5), the forest (XR12), re-accretion (FP16), the web "
           "channel (XR19), FP13's halofit stand-in for the nonlinear field",
      quantified="FP16's semi-analytic model over-predicts the committed PM's retention by +0.07-0.11 at the massive end and up to +0.40 at "
                 "1-2.5e14 Msun (V1/V2); XR21's box and XR19's Zel'dovich census disagree on the turned-around share (0.12 vs 0.32 at z = 2)",
      verdicts=["the cosmic-shear PASS on M* (MS3/MS4): NOT established (mock-based; DE5b)", "FP16's X-COP FAIL: its bias runs toward a stronger "
                "failure (and see A09b: SOFT on the data side)", "FP13's KiDS / sigma_8 with halofit standing in: conditional"],
      commits=["969a15e7f (MS4)", "2a5def6d9 (MS3)", "b3f5759a4 (FP16)", "b55775ce0 (XR19)", "b667f56bb (XR12)"], pending="XR21 stages 2-3")
equip("B08", "Frozen-coefficient and local-WKB stability audits", status="OPEN (for rates ~ H)",
      what="DE12, DE13, XR11, XR15 and FP2 L8b linearise on frozen backgrounds with local WKB (k >> 1/layer)",
      quantified="where growth rates are O(H) the background evolves as fast as the mode: XR15's smoothed gate leaves 16 of 24 layers growing at "
                 "1.1-2.8 H; DE13's first-run lambda = 241 was a WKB artefact (it missed the background term; corrected in the committed run); "
                 "sign flips of a principal symbol (XR18's H_S) are not frozen-coefficient-sensitive",
      verdicts=["XR15's smoothed-gate instability at 1.1-2.8 H: NOT established in magnitude", "XR11's fluid instability on the z = 0.25 layers: "
                "scope-limited (frozen background)", "DE12's gate instability (c_gate 1500-3700 km/s against gas <= 117 km/s): rates >> H, stands",
                "XR18's H_S ill-posedness: stands; XR18b (3c0cf3c37) finds FP19's repair H_K1 linearly well posed and causal (criterion B)"],
      commits=["7f84b3546 (DE12)", "a7abb4d4f (DE13)", "b667f56bb (XR11, XR15)", "53854a459 (XR18)", "3c0cf3c37 (XR18b)"])
equip("B09", "The web's external field in the kernel, omitted from the committed isolated-lens KiDS models", status="PENDING",
      what="the committed KiDS models score an isolated lens in vacuum; the chain's kernel also reads the web's field around it",
      quantified="FP22 D2 (bfe9a2fe5; a uniform-rms upper-side estimate): +200 (baryons-only) to +600 (all-matter) in Delta chi^2 with H_Y or H_K1",
      verdicts=["the chain's KiDS PASS (FP13/FP19 after FP20): NOT established until the web's field is scored"],
      commits=["7a8c25321 (FP20)", "0c18c582f (FP19)", "bfe9a2fe5 (FP22)"], pending="a scored treatment of the web's field (FP22 L22l: OPEN)")
equip("B10", "The cosmic-shear gate's reading: one-sided (R <= 1.2, MS3/MS4's code) or two-sided (0.8 <= R <= 1.2, MS3's text)",
      status="OPEN", quantified=f"two-sided, only x_c0 <= 3.5 (p = 1) passes; M*'s capped minimum is {XR9T['shear_min']:.3f} (XR9)",
      verdicts=["M*'s shear PASS holds under both readings at its cell; neighbouring cells flip"], commits=["e39cb4420 (XR9)", "969a15e7f (MS4)"])
equip("B11", "The Brouwer et al. 2021 covariance reshape", status="FIXED",
      quantified=f"the plain reshape is indefinite (min eigenvalue {R18['K']['eig_plain']:.1f}); the (m, n, i, j) order is positive definite "
                 f"({R18['K']['eig_good']:.2e})", verdicts=["the pre-2026-09-03 KiDS chi^2 (corrected then; FP18 K1 exhibits it)"],
      commits=["09990b398 (FP18 K1)"])
equip("B12", "The published R0 errors and FP12's fit form", status="FIXED in FP18 (FP12 not re-scored)",
      quantified=f"K&K's quoted +-0.02 (stack) is their distance-only Monte Carlo; the bootstrap over galaxies gives +-{R18['E']['stack']['boot']:.3f} "
                 f"(LG +-{R18['E']['LG14']['boot']:.3f}); FP12's fit form returns R0 = {R18['E']['fp12_form_R0']:.2f} on K&K's own table",
      verdicts=[f"FP12's R0 significances (the LG at {R12['LG'][0] / _R12S['LG']:.1f} sigma on the quoted errors): OVERSTATED -- the offsets "
                f"stand; with the honest error the chain's LG overshoot is {R12['LG'][0] / _s_lg:.1f} sigma, and "
                f"{R12['LG'][0] / math.hypot(_s_lg, 0.05):.1f} sigma with the method systematic added"],
      commits=["09990b398 (FP18)", "59e537955 (FP12)"])
equip("B13", "The lensing boost against uniform randoms (FP21)", status="FIXED",
      quantified="applying the boost moves B21's bins 2/3 from A = 0.91/1.15 to 1.00/1.28 -- photometric lenses avoid masked holes, so the "
                 "boost is confounded; B21's no-boost convention is used", verdicts=["FP21's K6 as first declared (reported failing)"],
      commits=["bb368ad2a (FP21)"])
equip("B14", "Harvey same-cell (L389): no MUTATE run", status="OPEN", quantified=f"beta = +{_hb:.3f} against +0.10 at 575 km/s only",
      verdicts=["M*'s Harvey PASS: uncontrolled, NOT established"], commits=["6dc375e88 (L389)"])
equip("B15", "FP16's semi-analytic retention against the committed PM", status="OPEN",
      quantified="over-prediction +0.07-0.11 (massive end), +0.17-0.40 (6e13-2.5e14 Msun); V4 reads the PM's own most massive halos, which "
                 "also keep a median above X-COP's window", verdicts=["FP16's X-COP FAIL: robust to the model's bias (V4), SOFT on the data side (A09b)"],
      commits=["b3f5759a4 (FP16)"])
equip("B16", "The record's first-order leapfrog drift (XR21)", status="FLAGGED",
      quantified="a free-streaming daughter's travel from z = 3 is overstated by 1.8% at dlna = 0.02", verdicts=["stage-3 escape distances: use dlna = 0.01"],
      commits=["b4bf5b2ae (XR21)"])
equip("B17", "Statistic and convention choices on the EFE and wide-binary tests", status="OPEN (theory-side forms)",
      quantified="scalar-sum vs subtract forms differ by ~1-4 sigma on the cluster slope; Crater II is 4.2 sigma in the record's convention and "
                 "0.06-2.48 sigma in the literature's; the frozen DR4 rows carry no entry for the chain's law (XR22)",
      verdicts=["the EFE FAILs are form-dependent in size (A05a is SOFT for the gentlest form, A05b/A05c are not)",
                "DR4 can kill the chain only from above"], commits=["3e55fdff2 (XR27)", "661ea3cff (XR22)", "d4343a4b3 (k_contrarian)"])
equip("B18", "Bookkeeping of the framework's own results", status="OPEN (record-keeping; this lane edits nothing)",
      quantified="EMPIRICAL_TESTS.md (compiled 2026-08-18) cites memory tags for A5/A9/A13; its header kappa 0.529 +- 0.034 is a hard-coded "
                 "string (stage75); C2 'fired once' omits the n = 25 non-reproduction in the same commit; 'N ~ 1157' is stale (1385/1705; R1/R2 "
                 "need ~6000); STANDING.md's 'one object at +-0.13 dex decides at 20:1' was corrected to 3.8:1 by PAPER14 v2",
      verdicts=["the own-results' headline claims above are restated in O1-O8 with the corrected numbers"],
      commits=["f617640aeb", "94dd69206c", "d8097e02c", "a49751b6c"])
for _e2 in EQUIP:
    P(f"  {_e2['id']}  [{_e2['status']}] {_e2['name']}\n        {_e2['quantified']}")
    for _v in _e2["verdicts"]:
        P(f"          - {_v}")
OUT["numbers"]["T_EH98"] = EH
P(f"    {el()}")


# ====================================================================================================================== the ledger table
def fmt(x, u=""):
    if x is None:
        return "-"
    if isinstance(x, float):
        return (f"{x:.3g}" if (abs(x) < 1e-3 or abs(x) >= 1e4) and x != 0 else f"{x:.4g}") + (f" {u}" if u else "")
    return str(x)


banner("A  THE LEDGER TABLE (class, stake, budget, LCDM under the same shift)")
for r in ROWS:
    n = r.get("numbers", {})
    if "stake" in n and "budget_quad" in n:
        pl = n["pulls_at_stake"]["lcdm"]
        lc = ", ".join(f"{k} {v:.2f}" for k, v in pl.items()) if pl else "no LCDM counterpart"
        sb = (f"stake {fmt(n['stake'], n['units'])} (variant: {n['variant']}); budget {fmt(n['budget_quad'], n['units'])} (quadrature), "
              f"{fmt(n['budget_corner'], n['units'])} (corner); LCDM pull at the needed shift: {lc}")
    else:
        sb = f"stake: {r.get('stake', '-')}; budget: {r.get('budget_text', r.get('shift', '-'))}"
    P(f"  {r['id']:5s} [{r['cls']:17s}] {r['scale']}: {r['title']}")
    P(f"        framework: {r.get('fw_standing', '-')}")
    P(f"        LCDM:      {r.get('lcdm_standing', '-')}")
    P(f"        {sb}")
    if r.get("contested"):
        P(f"        contested: {r['contested']}")
OUT["ledger"] = ROWS
OUT["own"] = OWN
OUT["equipment"] = EQUIP

# ====================================================================================================================== N  not established
banner("N  THE PAST VERDICTS THAT ARE NOT ESTABLISHED (they rest on the record's own approximations or on soft data)")
NOTEST = [
    dict(verdict="XR26: the chain FAILS Planck CMB lensing at +4.9 sigma (linear) / +40 sigma (halofit)", kind="FAIL (as the chain now stands)",
         rests_on=["B01", "B03", "B04"], note="it holds for the action as written (all matter; FP22: every cell excluded); in the reading the chain "
         "has adopted (baryons only) the linear base passes Planck and ACT and the halofit base fails ACT, so the verdict is open until the "
         "nonlinear phantom is computed"),
    dict(verdict="FP9 / FP13 / FP19: the forest passes ('forest 0')", kind="PASS", rests_on=["B06", "B01"], note="linear per-mode proxies"),
    dict(verdict="M*: KiDS-1000 passes ON M* (XR14), DE10's -37/-34, XR9's KiDS cap 4.42", kind="PASS", rests_on=["B02"], note="P2 projector on "
         "carrier templates (+187% / -123% at 35 kpc); XR35 in flight"),
    dict(verdict="the chain: KiDS passes at z = 0.25-0.4 (FP13/FP19 after FP20)", kind="PASS", rests_on=["B09", "A07b"],
         note="the web's field in the kernel is omitted; the outer bins carry B21's own 30% leakage"),
    dict(verdict="M*: the cosmic-shear pass (MS3/MS4, 1.049/1.124)", kind="PASS", rests_on=["B07", "B10", "A18"], note="halo model, mock-based; "
         "within the baryonic-feedback budget"),
    dict(verdict="M*: Harvey passes at 575 km/s (L389)", kind="PASS", rests_on=["B14"], note="no MUTATE; knife-edge"),
    dict(verdict="FP16: the dark sector's window is EMPTY because X-COP fails at every kick", kind="FAIL", rests_on=["A09b", "B04", "B07"],
         note="SOFT on the data side (hydrostatic bias; the canonical turned-around-web cell already sits at the gate); FP20b keeps its KiDS "
              "passes; scored in the reading the chain has adopted (baryons only)"),
    dict(verdict="L347 / L358 / L359 / L362 / DE2: the forest verdicts of the constant-threshold and window lanes", kind="PASS and FAIL",
         rests_on=["B05"], note="deviations under-stated by the (1+z) kernel argument; failures stand or worsen, borderline passes are open"),
    dict(verdict="XR15 / XR11: instability of the smoothed gate and of the fluid's edge layers at O(H) rates", kind="FAIL (magnitude)",
         rests_on=["B08"], note="frozen-background WKB at rates ~ H"),
    dict(verdict="FP12: the LG / M81 / IC 342 R0 overshoots at high significance", kind="FAIL (significance)", rests_on=["B12"],
         note=f"the offsets stand (+0.20 dex); the significance is {R12['LG'][0] / math.hypot(_s_lg, 0.05):.1f}-{R12['LG'][0] / _s_lg:.1f} sigma "
              f"with honest errors (and the method systematic), not {R12['LG'][0] / _R12S['LG']:.0f} on the quoted ones"),
    dict(verdict="FP13: the state at high z (z_close) and its A6 systematic", kind="derived number", rests_on=["B03"], note="the T_EH98 units error"),
    dict(verdict="M*: the flat-a0 flagship at z = 2.5", kind="PASS (was)", rests_on=["A04"], note="already 'not established' on the answer page (XR17)"),
]
for _n in NOTEST:
    P(f"  - [{_n['kind']}] {_n['verdict']}  <- {', '.join(_n['rests_on'])}: {_n['note']}")
OUT["not_established"] = NOTEST

# ====================================================================================================================== R  the requirements list
REQ = {
    "A01": "Newtonian where g >> a0: Q2 <= 5.2e-27 s^-2 (2 sigma) and gamma - 1 = (2.1 +- 2.3)e-5",
    "A03a": "the RAR's form and tightness (0.1 dex on 175 SPARC), deterministic in the baryons",
    "A03b": "a0 = 0.94-1.13 x1e-10 m/s^2 (both footings) is inside g-dagger = 1.20 +- 0.24 (sys); kappa = 1/2 stays fitted",
    "A05a": (lambda n: f"the cluster-infall BTFR slope +0.003 +- 0.030 with ~{n['budget_quad']:.3f} data-side: an external-field deficit slope no "
             f"steeper than {n['d'] - n['budget_quad'] - 2 * n['s']:+.3f} (the data shifted by the whole budget, then the 2-sigma gate): "
             f"QUMOND's gentlest (scalar-sum) form, {min(n['fw'].values(), key=abs):+.3f}, fits inside it; the least favourable (subtract) "
             f"form, {min(n['fw'].values()):+.3f}, does not")(
             next(r for r in ROWS if r["id"] == "A05a")["numbers"]),
    "A05b": "LV dwarfs: statistic C = +0.080 +- 0.047 -- no host-field suppression of dwarf dispersions at 50-300 kpc (robust to binaries, tides, Upsilon)",
    "A05c": f"Coma UDGs are dynamically hot: no visible EFE suppression at 0.2-2.3 Mpc (+{min(_me.values()):.2f} to +{max(_me.values()):.2f} dex "
            "over the EFE-suppressed prediction; +0.40 dex even over isolated MOND)",
    "A05d": "Crater II / M31 dSphs: the verdict is set by Upsilon_V and the radius convention (0.06-2.5 sigma in the literature's convention)",
    "A05f": "Chae's SPARC EFE: 1.0-2.9 sigma depending on the environment geometry",
    "A07a": "KiDS isolated-lens Delta Sigma inside 0.3 Mpc (Brouwer et al. 2021, four mass bins)",
    "A07b": "KiDS beyond 0.3 Mpc: the published bins carry ~30% photo-z leakage (-0.11 dex); for LV-like isolated spirals the signal may be "
            "up to ~0.5 dex lower (FP18) -- A = 2.19 +- 1.46 of the mixed level measured (FP21)",
    "A07c": "the KiDS-R0 pincer: 2.3 sigma after comparability systematics, shared by LCDM",
    "A08": "the LG zero-velocity radius R0 = 0.96 (0.91) +- 0.11 Mpc (honest) with a 0.05-dex method systematic",
    "A09a": "clusters need mass beyond MOND on the baryons: eta(R500) = 2.33 [1.55-2.80]; hydrostatic corrections only raise it",
    "A09b": "X-COP totals at R500 with a hydrostatic bias b in 0.06-0.2 (a b above 0.06 lowers LCDM's gas fraction by the same factor)",
    "A09c": "collisionless lensing mass offset from the gas in mergers (Bullet: 8 sigma)",
    "A10": "the CMB primary spectra: GR + CDM at z >~ 10 with omega_c ~ 0.120, omega_b ~ 0.0224",
    "A11": "CMB lensing amplitude 1.011 +- 0.028 (Planck 8-400) and 1.013 +- 0.023 (ACT DR6)",
    "A12a": "BAO and the P(k) shape: the LCDM background and linear growth to ~1%",
    "A13": "small-scale linear power at z = 2-3 within ~10-15% of LCDM (after IGM marginalisation)",
    "A14": "early massive galaxies need eps = 0.27-1.27 of the baryon ceiling, set by the IMF and spectroscopy (same for any model with LCDM's "
           "halo abundance)",
    "A15a": "standard BBN: Y_P ~ 0.245-0.247, D/H ~ 2.45-2.59e-5 at omega_b = 0.0224",
    "A15b": "lithium-7: the factor ~3 is shared; stellar depletion ~0.25 dex",
    "A16": "c_T = c to 1e-15",
    "A17b": "the MW's stellar mass 5.0-6.1 (+-0.6-1.1) x1e10 Msun from the censuses, jointly with the 8-19 kpc slope -1.7 km/s/kpc",
    "A18": "cosmic-shear power at k ~ 1 h/Mpc within the ~10% baryonic-feedback budget of LCDM",
    "A02": "wide binaries: state gamma_hat at the pre-registration's primary field and its xi dependence; DR4 (2026-12-02) decides",
    "A04": "a0(z): state the high-z BTFR zero point at z ~ 2.5 (the flat law: 0.00 dex; LCDM-native +0.33 dex); the MUSE rise is contested",
    "A05e": "DF2/DF4: state the prediction at both 13 and 20-22 Mpc",
    "A06": "SLACS: state the IMF the construction needs; the published IMF methods disagree by 0.26-0.30 dex",
    "A09d": "Harvey-type offsets: state the fractional drag; the published bounds disagree (0.47 vs ~2 cm^2/g)",
    "A12b": "S8: state it; the survey values span 0.76-0.82 (Planck 0.83)",
    "A19": "cluster counts: state them; the eRASS1 (S8 0.86 +- 0.01) and SPT (0.795 +- 0.029) cosmologies disagree",
    "A17a": "the MW's outer decline: state the curve at 20-27 kpc; the published indices span -0.19 to -0.56",
}
RQ = {"MODEL-INDEPENDENT": [], "SOFT": [], "CONTESTED": []}
for r in ROWS:
    if r["id"] in REQ:
        RQ[r["cls"]].append(dict(id=r["id"], fact=REQ[r["id"]]))
RQ["OWN (keep)"] = [dict(id=o["id"], cls=o["cls"], fact=o["keep"]) for o in OWN]
banner("R  THE REQUIREMENTS LIST")
for k, lst in RQ.items():
    P(f"  {k}:")
    for it in lst:
        P(f"    {it['id']:5s} {('[' + it['cls'] + '] ') if 'cls' in it else ''}{it['fact']}")
OUT["requirements"] = RQ

# ====================================================================================================================== K4 / K5 / F
banner("K4 / K5 / F  THE SOURCES, THE COMMITS, THE FAIRNESS CHECKS")
_bad = []
for rel in sorted(SOURCES):
    tr = git("ls-files", "--error-unmatch", rel)[0] == 0
    cl = tr and git("diff", "--quiet", "HEAD", "--", rel)[0] == 0
    sha = hashlib.sha256(open(os.path.join(REPO, rel), "rb").read()).hexdigest()[:16]
    OUT["sources"][rel] = dict(tracked=tr, clean=cl, sha256_16=sha, commit=git("log", "--format=%h", "-1", "--", rel)[1] if tr else "")
    if not (tr and cl):
        _bad.append(rel)
check("K4", "every committed source the ledger reads is git-tracked and unmodified (sha256 recorded)",
      f"{len(SOURCES)} sources; not tracked or modified: {_bad if _bad else 'none'}", not _bad)
PEND = {"FP22 (who feels MOND)": "real_research/derivation_chain_2026/FP22_who_feels_mond.py",
        "FP20b (P2 re-score of FP15/FP16/FP19)": "real_research/derivation_chain_2026/FP20b_rescore_fp15_fp16_fp19.py",
        "FP24 (the T_EH98 fix)": "real_research/derivation_chain_2026/FP24_transfer_function_fix.py",
        "XR34 (kernel-argument re-score)": "real_research/cross_thread_review_2026_09_26/XR34_kernel_argument.py",
        "XR35 (KiDS re-score on M*)": "real_research/cross_thread_review_2026_09_26/XR35_kids_rescore.py",
        "XR32 (S8 tension)": "real_research/cross_thread_review_2026_09_26/XR32_matter_power.py",
        "XR24 (LG numerical action)": "real_research/cross_thread_review_2026_09_26/XR24_numerical_action.py",
        "XR28 (cluster splashback)": "real_research/cross_thread_review_2026_09_26/XR28_controls.py"}
for k, rel in PEND.items():
    ex = os.path.exists(os.path.join(REPO, rel))
    tr = ex and git("ls-files", "--error-unmatch", rel)[0] == 0
    OUT["pending"][k] = dict(path=rel, exists=ex, committed=tr, status="committed" if tr else ("in flight" if ex else "not started"))
    P(f"    {k:40s} {OUT['pending'][k]['status']}")
_cm = set()
for coll in (ROWS, EQUIP):
    for r in coll:
        for c in r.get("commits", []):
            _cm.add(c.split()[0])
for o in OWN:
    for c in o.get("cite", []):
        if c.startswith("commit "):
            _cm.add(c.split()[1])
_miss = sorted(c for c in _cm if git("cat-file", "-e", c + "^{commit}")[0] != 0)
check("K5", "every commit the ledger cites exists in the repository", f"{len(_cm)} commits; missing: {_miss if _miss else 'none'}", not _miss)
OUT["numbers"]["commits_cited"] = sorted(_cm)
_groups = {}
for rid, tag, model, val in FAIR:
    _groups.setdefault((rid, tag), {})[model] = val
_asym = [f"{rid}/{tag}" for (rid, tag), v in _groups.items() if "fw" in v and "lcdm" in v and v["fw"] != v["lcdm"]]
check("F1", "FAIRNESS: under every systematic, the framework and LCDM were scored against identical (shifted) data",
      f"{len(_groups)} (row, shift) scorings; asymmetric: {len(_asym)}" + (f" ({', '.join(_asym[:8])}{' ...' if len(_asym) > 8 else ''})" if _asym else ""),
      not _asym, reading=("MUTATE: the systematics were applied to the framework only -- the special pleading the charter forbids is caught"
                          if MUTATE else ""))
_soft_bad = []
for r in ROWS:
    if r["cls"] == "SOFT":
        n = r.get("numbers", {})
        has_b = ("budget_quad" in n) or bool(r.get("budget_text")) or bool(r.get("shift"))
        has_l = ("pulls_at_stake" in n) or bool(r.get("lcdm_standing")) or bool(r.get("lcdm_same"))
        if not (has_b and has_l):
            _soft_bad.append(r["id"])
check("F2", "every SOFT row carries a quantified budget with its source and LCDM's standing under the same shift",
      f"SOFT rows {sum(r['cls'] == 'SOFT' for r in ROWS)}; incomplete: {_soft_bad if _soft_bad else 'none'}", not _soft_bad)
_f3 = [r["id"] for r in ROWS + OWN if r.get("cls") not in ("MODEL-INDEPENDENT", "SOFT", "CONTESTED") or not r.get("measured")
       or not r.get("assumptions") or not r.get("cite")]
check("F3", "every ledger and own-result row has a class, a measurement description, assumptions and a citation",
      f"{len(ROWS)} ledger rows, {len(OWN)} own results; incomplete: {_f3 if _f3 else 'none'}", not _f3)

# ====================================================================================================================== H  the hypotheses
banner("H  THE PRE-DECLARED HYPOTHESES, AS THEY FELL (reported)")
C = {r["id"]: r["cls"] for r in ROWS}
CO = {o["id"]: o["cls"] for o in OWN}
_a08 = next(r for r in ROWS if r["id"] == "A08")["numbers"]["pulls_face"]["fw"]
_lin_b = [AMPMAP["real-space, baryons only (lowest mapped f)"]["lin"], AMPMAP["real-space, baryons only (highest mapped f)"]["lin"]]
_nl_a = [AMPMAP["real-space, all matter (lowest mapped f)"]["NL"], AMPMAP["real-space, all matter (highest mapped f)"]["NL"],
         AMPMAP["XR26 headline, per-mode, all matter"]["NL"]]
_a09 = next(r for r in ROWS if r["id"] == "A09b")["numbers"]
HY = {
    "H1": (OUT["checks"]["K1"]["ok"] and OUT["checks"]["K2"]["ok"] and OUT["checks"]["K3"]["ok"], "K1, K2, K3"),
    "H2": (all(C.get(k) == "MODEL-INDEPENDENT" for k in ("A01", "A16", "A15a", "A10", "A11", "A12a", "A03a", "A09a", "A09c")),
           ", ".join(f"{k} {C.get(k)}" for k in ("A01", "A16", "A15a", "A10", "A11", "A12a", "A03a", "A09a", "A09c"))),
    "H3": (C.get("A07c") in ("SOFT", "CONTESTED") and _a08["chain canonical (FP12)"] >= 2.0,
           f"A07c {C.get('A07c')}; the chain's LG pull with honest errors {_a08['chain canonical (FP12)']:.2f} sigma; A08 {C.get('A08')}"),
    "H4": (sum(C.get(k) == "MODEL-INDEPENDENT" for k in ("A05a", "A05b", "A05c")) >= 2, ", ".join(f"{k} {C.get(k)}" for k in ("A05a", "A05b", "A05c"))),
    "H5": (all(abs(a - 1.011) <= 2 * 0.028 for a in _lin_b) and all(abs(a - 1.011) > 2 * 0.028 for a in _nl_a),
           f"baryons-only linear {_lin_b[0]:.3f}-{_lin_b[1]:.3f}; all-matter halofit {min(_nl_a):.3f}-{max(_nl_a):.3f} (2-sigma edge 1.067)"),
    "H6": (C.get("A09b") == "SOFT" and _a09["most_favourable"][1] > 0.06, f"A09b {C.get('A09b')}; b needed {_a09['most_favourable'][1]:.3f}-"
           f"{_a09['least_favourable'][1]:.3f}"),
    "H7": (C.get("A06") == "CONTESTED", f"A06 {C.get('A06')}"),
    "H8": (_w11 * _kmax <= 0.02, f"DE11b estimate {_w11 * _kmax:.4f}"),
    "H9": (OUT["checks"]["F1"]["ok"] == (not MUTATE), f"F1 {'PASS' if OUT['checks']['F1']['ok'] else 'FAIL'} in the {'MUTATE' if MUTATE else 'main'} run"),
    "H10": (CO.get("O1") == "MODEL-INDEPENDENT" and CO.get("O2") == "MODEL-INDEPENDENT" and CO.get("O3") == "SOFT" and CO.get("O4") == "CONTESTED"
            and all(CO.get(k) in ("SOFT", "CONTESTED") for k in ("O5", "O6", "O7", "O8")), ", ".join(f"{k} {v}" for k, v in CO.items())),
}
for k, (ok, why) in HY.items():
    OUT["hypotheses"][k] = dict(held=bool(ok), measured=why)
    P(f"  {k}: {'HELD' if ok else 'FELL'} -- {why}")

# ====================================================================================================================== verdict
banner("VERDICT" + ("  [MUTATE]" if MUTATE else ""))
cnt = {c: sum(r["cls"] == c for r in ROWS) for c in ("MODEL-INDEPENDENT", "SOFT", "CONTESTED")}
cno = {c: sum(o["cls"] == c for o in OWN) for c in ("MODEL-INDEPENDENT", "SOFT", "CONTESTED")}
P(f"  Part A: {len(ROWS)} results -- MODEL-INDEPENDENT {cnt['MODEL-INDEPENDENT']}, SOFT {cnt['SOFT']}, CONTESTED {cnt['CONTESTED']}")
P(f"  Own results: {len(OWN)} -- MODEL-INDEPENDENT {cno['MODEL-INDEPENDENT']}, SOFT {cno['SOFT']}, CONTESTED {cno['CONTESTED']}")
P(f"  Part B: {len(EQUIP)} equipment items; {len(NOTEST)} past verdicts not established")
P("  kappa = 1/2 is fitted (Z = 5.7888); both footings carried; not 'closed'.")
OUT["numbers"]["counts"] = dict(partA=cnt, own=cno, equipment=len(EQUIP), not_established=len(NOTEST))
n_ok = sum(1 for _, ok, _ in CH if ok)
n_lb = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb}; wrote {os.path.basename(JSN)}   {el()}")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_lb, time.time() - T0
json.dump(jclean(OUT), open(JSN, "w"), indent=1)
rc = 1 if n_lb else 0
LINES.append(f"rc={rc}")
open(TXT, "w").write("\n".join(LINES) + "\n")
sys.exit(rc)
