#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG468 -- THE KERNEL FAMILY.  Is there a nu(y) that (i) fits the SPARC RAR as well as nu_mono, (ii) keeps nu -> y^-1/2 (y -> 0)
and nu -> 1 (y -> inf), and (iii) removes the zero-field nonlinear FAIL of the UNGATED chassis (CFG321/322/325/358)?
Criteria frozen first: FROZEN_CRITERIA.md (b0d7274a0).  a0 = kappa c sqrt(G rho_Lambda) is fixed; kappa is FITTED and refit per
kernel; both footings reported (9.36e-11 rho_Lambda / 1.13e-10 rho_crit).

ARM 1 (SPARC): lane V's v_common (imported read-only, sha256 recorded), T-free (Upsilon free per galaxy, all, sigma_int 0.0808) and
T-fix (Upsilon 0.5, MLS16 cuts, sigma_int 0.11); a0 refit per kernel; SPARC-PASS iff Delta chi2 vs nu_mono <= 4 in both.
ARM 2 (zero-field): the CFG321 engine byte-identical (cfg468_engine.py), kernels swapped, one physical unit y*_ref; arrays made by
cfg468_zero_field_runs.py (nu_mono baseline: CFG325's committed-run arrays, re-scored); CFG325's frozen ratio rule on
N = 127/255/511/1023 at eps = 1e-3 and 1e-4, plus the pre-declared BOUNDED class.  VIABLE = SPARC-PASS and CONVERGENT.
SCOPE: the zero-field arm is the UNGATED chassis only (law on everywhere, 1-D, data class D); nothing about candidate B, growth or
sigma_8.
Run from the repository root:   python3 campaign_fresh_gravity/CFG468_kernel_family/cfg468_kernel_family.py
MUTATE:  CFG468_MUTATE=1 ... : the kinked kernel (1/nu piecewise linear in sqrt y) must NOT come out VIABLE (rc = 1 when it does not).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, warnings
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFGD = os.path.dirname(HERE)
REPO = os.path.dirname(CFGD)
EXTROOT = os.path.join(os.path.dirname(REPO), "_external_data")
sys.path.insert(0, HERE)
ENGINE_SHA256 = "bde2fbb6abb12fad4e8392917b792374016fd8127da2a02dcaa8338ff8952174"
_h = hashlib.sha256(open(os.path.join(HERE, "cfg468_engine.py"), "rb").read()).hexdigest()
if _h != ENGINE_SHA256:
    sys.exit(f"ABORT: cfg468_engine.py sha256 {_h} != CFG321's engine")
import cfg468_engine as EN
import cfg468_kernels as KN
import CFG5_common as C5
VDIR = os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "V_evidence_for_the_coefficient")
sys.path.insert(0, VDIR)
import v_common as V
V_SHA = hashlib.sha256(open(os.path.join(VDIR, "v_common.py"), "rb").read()).hexdigest()

MUTATE = os.environ.get("CFG468_MUTATE", "0") == "1"
SLUG = "cfg468_kernel_family" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "CFG468", "frozen": "FROZEN_CRITERIA.md (b0d7274a0)", "mutate": MUTATE, "engine_sha256": _h, "v_common_sha256": V_SHA,
       "checks": {}, "sparc": {}, "zero_field": {}, "table": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    return ok


P(__doc__.strip())
P(f"\n  engine sha256 {_h} == CFG321's engine (verified); v_common sha256 {V_SHA[:16]}...")
if MUTATE:
    P("\n  *** MUTATE=1: the kinked kernel (1/nu piecewise linear in sqrt y; kinks at y = 2.6e-19, 1.0e-18 and 0.01, 0.09, 1, 9, 100)"
      " -- it must NOT come out VIABLE ***")

CAND = ["MUTATE_kink"] if MUTATE else ["nu_simple", "nu_standard", "S1", "S2"]
REFS = [] if MUTATE else ["nu_rar", "nu_p2"]
c_si, G_si, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
H0 = 67.4e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_si)
A_L, A_C = c_si * math.sqrt(G_si * 0.685 * rho_c), c_si * math.sqrt(G_si * rho_c)
P(f"  c sqrt(G rho_Lambda) = {A_L:.4e}, c sqrt(G rho_crit) = {A_C:.4e} (H0 67.4, Omega_L 0.685): kappa = 1/2 -> a0 = {A_L/2:.4e} / {A_C/2:.4e}")

# ================================================================================================================ kernels
banner("K  THE KERNELS: identity, the nu_n family, the limits (ii), the tails (reporting)")
yy = np.logspace(-6, 6, 241)
check("C-K K0 is the record's standing kernel (CFG5_common.nu_mono itself, XC4), and nu_simple / nu_standard equal the nu_n family "
      "[1/2 + sqrt(1/4 + y^-n)]^(1/n) at n = 1, 2 to 1e-12 on y in [1e-6, 1e6]",
      f"max rel dev n=1 {np.max(np.abs(KN.nu_simple(yy)/KN.nu_n(yy,1)-1)):.1e}, n=2 {np.max(np.abs(KN.nu_standard(yy)/KN.nu_n(yy,2)-1)):.1e}",
      KN.NU["nu_mono"](yy).tolist() == C5.nu_mono(yy).tolist() and np.max(np.abs(KN.nu_simple(yy) / KN.nu_n(yy, 1) - 1)) < 1e-12
      and np.max(np.abs(KN.nu_standard(yy) / KN.nu_n(yy, 2) - 1)) < 1e-12)
LIM = {}
for k in ["nu_mono"] + CAND + REFS:
    nu = KN.NU[k]
    deep = {ye: float(nu(np.array([ye]))[0] * math.sqrt(ye)) for ye in (1e-30, 1e-20, 1e-12)}
    newt = {ye: float(nu(np.array([ye]))[0] - 1) for ye in (1e2, 1e4, 1e6, 1e8)}
    LIM[k] = {"deep_nu_sqrty": deep, "nu_minus_1": newt, "ii": KN.LIMITS_II[k]}
    P(f"    {k:12s}: nu sqrt(y) at y = 1e-30 / 1e-20 / 1e-12: {deep[1e-30]:.6g} / {deep[1e-20]:.6g} / {deep[1e-12]:.6g};  "
      f"nu - 1 at y = 1e2/1e4/1e6/1e8: " + " / ".join(f"{newt[x]:.2e}" for x in (1e2, 1e4, 1e6, 1e8)) + f";  (ii): {KN.LIMITS_II[k]}")
ii_exact = [k for k in LIM if KN.LIMITS_II[k] == "exact"]
check("(ii) numerically: every kernel labelled 'exact' has nu sqrt(y) = 1 to 1e-6 at y = 1e-30 and nu - 1 < 1e-3 at y = 1e8; "
      "the splices are finite at y -> 0 (nu sqrt(y) -> 0), i.e. (ii) only operational, as frozen",
      ", ".join(f"{k}: {LIM[k]['deep_nu_sqrty'][1e-30]:.3g}" for k in LIM),
      all(abs(LIM[k]["deep_nu_sqrty"][1e-30] - 1) < 1e-6 and LIM[k]["nu_minus_1"][1e8] < 1e-3 for k in ii_exact)
      and all(LIM[k]["deep_nu_sqrty"][1e-30] < 1e-3 for k in LIM if k in ("S1", "S2")))
OUT["limits"] = LIM
P("    note: nu - 1 at y = 1e6 (about Saturn) is the bare Solar-System tail; the chassis' heat filter (L340/CFG357) changes it; reporting only")
# --- reporting only (no gate): what each kernel does in the ranges other committed gates read
P("\n  KERNEL STRUCTURE (reporting; used by the README's kernel-dependence flags):")
P("    UFD range y = 0.01-0.1, wide binaries / EFE / clusters y ~ 0.3-10 (nu / nu_mono); Solar-System tail slope d ln(nu-1)/d ln y at 1e6;"
  " min of h' = d[y(nu-1)]/dy over y in [1e-6, 1e8] (phantom monotone iff >= 0; XC5 leaf convexity needs > -1)")
yg = np.logspace(-6, 8, 140001)
STRUCT = {}
for k in ["nu_mono"] + CAND + REFS:
    nu = KN.NU[k]
    rat = {y_: float(nu(np.array([y_]))[0] / KN.nu_mono(np.array([y_]))[0]) for y_ in (0.01, 0.05, 0.3, 1.0, 3.0, 10.0)}
    t1, t2 = float(nu(np.array([1e6]))[0] - 1), float(nu(np.array([1.1e6]))[0] - 1)
    slope = math.log(t2 / t1) / math.log(1.1) if t1 > 0 and t2 > 0 else float("nan")
    hfun = yg * (nu(yg) - 1)
    hp = np.gradient(hfun, yg)
    i0 = int(np.argmin(hp))
    STRUCT[k] = {"ratio_to_nu_mono": rat, "tail_slope_1e6": slope, "nu_minus_1_1e6": t1, "min_hprime": float(hp[i0]), "at_y": float(yg[i0])}
    P(f"    {k:12s}: nu/nu_mono at y = 0.01/0.05/0.3/1/3/10: " + " / ".join(f"{rat[y_]:.3f}" for y_ in rat) +
      f";  tail slope at 1e6 {slope:+.2f};  min h' {hp[i0]:+.4f} at y = {yg[i0]:.3g}")
OUT["structure"] = STRUCT

# ================================================================================================================ C0 adapters
banner("C0  ENGINE ADAPTERS: one physical unit y*_ref; nu_mono adapter == the engine's NuMonoKernel; Q and C_L identities; C^2 joins")
eng = EN.NuMonoKernel(KN.ALPHA_C)
gen = KN.make_engine_kernel("nu_mono_generic")
yh = np.logspace(-12, 1, 600)
dev = {nm: float(np.max(np.abs(getattr(gen, nm)(yh) / getattr(eng, nm)(yh) - 1))) for nm in ("CT", "CL", "Q")}
check("C0a the generic nu_mono adapter reproduces the engine's NuMonoKernel C_T, C_L, Q to <= 1e-10 (relative) on yhat in [1e-12, 10], "
      "with the engine's own y* and C*", f"{dev}; y* {KN.YSTAR:.6e} vs engine {eng.ystar:.6e}",
      max(dev.values()) <= 1e-10 and KN.YSTAR == eng.ystar and KN.CSTAR == eng.Cstar)
idt = {}
for k in CAND:
    K = KN.make_engine_kernel(k)
    y2 = np.logspace(-10, 1, 3000); hh = 1e-5
    dQ = (K.Q(y2 * (1 + hh)) - K.Q(y2 * (1 - hh))) / (2 * hh * y2)
    dC = (y2 * (1 + hh) * K.CT(y2 * (1 + hh)) - y2 * (1 - hh) * K.CT(y2 * (1 - hh))) / (2 * hh * y2)
    msk = np.ones_like(y2, bool)
    if k == "MUTATE_kink":
        for kk in (0.1, 0.4):
            msk &= np.abs(y2 / kk - 1) > 1e-4
    if k in ("S1", "S2"):
        msk &= np.abs(y2 / K.yhs - 1) > 1e-4
    idt[k] = (float(np.max(np.abs(dQ / (2 * y2 * K.CT(y2)) - 1)[msk])), float(np.max(np.abs(dC / K.CL(y2) - 1)[msk])),
              float(np.min(K.CL(y2))), float(np.min(K.CT(y2))))
    P(f"    {k:12s}: dQ/dyhat vs 2 yhat C_T max dev {idt[k][0]:.1e}; d(yhat C_T)/dyhat vs C_L {idt[k][1]:.1e}; min C_L {idt[k][2]:.3e}; "
      f"min C_T {idt[k][3]:.3e} (convex iff C_T, C_L > 0); C_T(1) = {float(K.CT(np.array([1.0]))[0]):.6f}, C_T(1e-4) = {float(K.CT(np.array([1e-4]))[0]):.6g}")
check("C0b every candidate adapter satisfies dQ/dyhat = 2 yhat C_T and C_L = d(yhat C_T)/dyhat to <= 1e-6 (finite differences, away "
      "from kinks/joins) and is convex on the engine range (C_T > 0, C_L > 0)",
      "; ".join(f"{k}: {v[0]:.1e}/{v[1]:.1e}, minCL {v[2]:.2e}" for k, v in idt.items()),
      all(v[0] <= 1e-6 and v[1] <= 1e-6 and v[2] > 0 and v[3] > 0 for v in idt.values()))
if not MUTATE:
    jumps = {}
    for k in ("S1", "S2"):
        # both branches evaluated AT the join: the polynomial branch analytically, the nu_mono branch through the base adapter
        # (dC_L/dyhat of the smooth base by a Richardson-extrapolated central difference, error ~h^4)
        K = KN.make_engine_kernel(k); s = K.yhs
        ct_lo = K.pref * (K.a + K.b + K.c); cl_lo = K.pref * (K.a + 3 * K.b + 5 * K.c); dcl_lo = K.pref * (6 * K.b + 20 * K.c) / s
        ct_hi = float(K.base.CT(np.array([s]))[0]); cl_hi = float(K.base.CL(np.array([s]))[0])
        Dc = lambda hh: float((K.base.CL(np.array([s + hh]))[0] - K.base.CL(np.array([s - hh]))[0]) / (2 * hh))
        hh = 1e-3 * s
        dcl_hi = (4 * Dc(hh / 2) - Dc(hh)) / 3
        jumps[k] = (abs(ct_hi / ct_lo - 1), abs(cl_hi / cl_lo - 1), abs(dcl_hi / dcl_lo - 1))
    check("C0c S1/S2 are C^2 at the join: relative jumps of C_T, C_L and dC_L/dyhat <= 1e-8 (both branches evaluated at y_s)",
          "; ".join(f"{k}: C_T {v[0]:.1e}, C_L {v[1]:.1e}, dC_L {v[2]:.1e}" for k, v in jumps.items()),
          all(v[0] <= 1e-8 and v[1] <= 1e-8 and v[2] <= 1e-8 for v in jumps.values()))
else:
    K = KN.make_engine_kernel("MUTATE_kink"); e = 1e-7
    jA = K.CL(np.array([0.1 * (1 + e)]))[0] / K.CL(np.array([0.1 * (1 - e)]))[0]
    jB = K.CL(np.array([0.4 * (1 + e)]))[0] / K.CL(np.array([0.4 * (1 - e)]))[0]
    check("C0c the MUTATE kinks are real: C_L jumps by x0.5 at yhat = 0.1 and x1.5 at yhat = 0.4 (to 1%), C_T continuous",
          f"C_L ratio across 0.1: {jA:.4f}; across 0.4: {jB:.4f}", abs(jA - 0.5) < 0.005 and abs(jB - 1.5) < 0.015)

# ================================================================================================================ ARM 1 SPARC
banner("ARM 1  SPARC RAR (lane V machinery): a0 refit per kernel, two treatments, Delta chi2 vs nu_mono; PASS iff <= 4 in both")
gals = V.load_sparc()
TREAT = {"T-free": (gals, {}, 0.0808),
         "T-fix": ([g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30], dict(ufixed=0.5), 0.11)}
P(f"  SPARC: {len(gals)} galaxies (SPARC_Lelli2016c.mrt + rotmod); T-free {len(TREAT['T-free'][0])} galaxies, T-fix {len(TREAT['T-fix'][0])}")
A61 = np.exp(np.linspace(math.log(0.5e-10), math.log(2.5e-10), 61))
rep = {}
for tn, (sel, kw, si) in TREAT.items():
    rep[tn] = float(V.Profile(sel, KN.make_IF(KN.nu_p2), **kw).scan(A61, si).min())
check("C-S the SPARC code reproduces p35's printed exact-law (P2) chi2_min on p35's 61-point grid: T-fix 4596.5, T-free 3139.8 (to 0.1)",
      f"T-fix {rep['T-fix']:.1f}, T-free {rep['T-free']:.1f}", abs(rep["T-fix"] - 4596.5) <= 0.1 and abs(rep["T-free"] - 3139.8) <= 0.1)
AG = np.exp(np.linspace(math.log(0.5e-10), math.log(2.5e-10), 161))
SP = {}
for k in ["nu_mono"] + CAND + REFS:
    SP[k] = {}
    for tn, (sel, kw, si) in TREAT.items():
        prof = V.Profile(sel, KN.make_IF(KN.NU[k]), **kw)
        ch = prof.scan(AG, si)
        ahat, sln = V.parabola_min(AG, ch)
        cmin = float(prof.chi2(ahat, si)[0])
        if cmin > ch.min():                                    # the parabola can only improve on the grid
            ahat, cmin = float(AG[int(np.argmin(ch))]), float(ch.min())
        SP[k][tn] = {"a0": ahat, "sig_ln": sln, "chi2_min": cmin, "kappa_L": ahat / A_L, "kappa_crit": ahat / A_C,
                     "edge": bool(int(np.argmin(ch)) in (0, len(AG) - 1)), "npts": prof.npts}
for k in SP:
    for tn in TREAT:
        SP[k][tn]["dchi2"] = SP[k][tn]["chi2_min"] - SP["nu_mono"][tn]["chi2_min"]
    SP[k]["pass"] = all(SP[k][tn]["dchi2"] <= 4.0 for tn in TREAT)
    SP[k]["indistinguishable_p35"] = all(abs(SP[k][tn]["dchi2"]) < 2.0 for tn in TREAT)
P(f"  {'kernel':12s} | {'T-free: a0':>11s} {'kappa_L':>8s} {'kappa_c':>8s} {'chi2':>9s} {'dchi2':>8s} | {'T-fix: a0':>10s} {'kappa_L':>8s} "
  f"{'kappa_c':>8s} {'chi2':>9s} {'dchi2':>8s} | PASS (<= 4 both)")
for k in SP:
    a, b = SP[k]["T-free"], SP[k]["T-fix"]
    P(f"  {k:12s} | {a['a0']:11.4e} {a['kappa_L']:8.3f} {a['kappa_crit']:8.3f} {a['chi2_min']:9.1f} {a['dchi2']:+8.2f} | "
      f"{b['a0']:10.4e} {b['kappa_L']:8.3f} {b['kappa_crit']:8.3f} {b['chi2_min']:9.1f} {b['dchi2']:+8.2f} | {SP[k]['pass']}"
      f"{'  (grid edge!)' if a['edge'] or b['edge'] else ''}")
P("  chi2 counts independent points; lane V's crude clustering deflation is about x18 (p36), so dchi2/18 is the clustered reading "
  "(reported, not used).  Distances: SPARC as tabulated (lane V convention).")
check("SPARC grid: every best fit is interior to the a0 grid (no edge minimum)", [k for k in SP if SP[k]["T-free"]["edge"] or SP[k]["T-fix"]["edge"]],
      not any(SP[k]["T-free"]["edge"] or SP[k]["T-fix"]["edge"] for k in SP))
OUT["sparc"] = {"reproduction_p35": rep, "kernels": SP, "tolerance": "Delta chi2 <= 4 in both treatments (p36), independent points",
                "a0_grid": [float(AG[0]), float(AG[-1]), len(AG)]}

# ================================================================================================================ ARM 2 zero-field
banner("ARM 2  ZERO-FIELD (UNGATED chassis, 1-D, data class D): CFG325's frozen ratio rule on N = 127/255/511/1023, kernels swapped")
NS = (127, 255, 511, 1023)
EPSS = (1e-3, 1e-4)
DELTAS = (0.0, 1e-3, 1e-5)
ZERO = 0.005
T1D = 80.0


def arr_path(kern, n, eps, delta):
    if kern == "nu_mono":
        return os.path.join(EXTROOT, "cfg325_work", f"cfg325_main_nu_mono_n{n}_eps{eps:.0e}_delta{delta:.0e}.npz")
    d = "cfg468_work" + ("_MUTATE" if kern == "MUTATE_kink" else "")
    return os.path.join(EXTROOT, d, f"cfg468_main_{kern}_n{n}_eps{eps:.0e}_delta{delta:.0e}.npz")


def load(kern, n, eps, delta):
    fn = arr_path(kern, n, eps, delta)
    if not os.path.exists(fn):
        return None
    z = np.load(fn, allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    rec = {k_[4:]: z[k_].tolist() for k_ in z.files if k_.startswith("rec_")}
    return dict(meta, rec=rec, snaps_w=z["snap_w"], snaps_t=z["snap_t"])


def pair_D(rb, rp):
    m = min(len(rb["snaps_w"]), len(rp["snaps_w"]))
    return np.array([float(np.linalg.norm(a_ - c_) / max(np.linalg.norm(a_), 1e-300))
                     for a_, c_ in zip(rb["snaps_w"][:m], rp["snaps_w"][:m])])


def lyap(D, t, lo=1e-4, hi=1e-1):
    sel = (D >= lo) & (D <= hi)
    if sel.sum() < 8:
        return None, None, None, int(sel.sum())
    x, y = t[sel], np.log(D[sel])
    c, cov = np.polyfit(x, y, 1, cov=True)
    pred = np.polyval(c, x)
    r2 = 1 - np.sum((y - pred) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-300)
    return float(c[0]), float(math.sqrt(cov[0, 0])), float(r2), int(sel.sum())


def zero(x):
    return abs(x) < ZERO


def ratio(num, den):
    if zero(den):
        if zero(num):
            return 0.0
        return float("inf") if num >= ZERO else None
    return num / den


def score_kernel(kern, ns=NS):
    res = {"sets": {}, "runs": [], "complete": True}
    branched = False; regular = True
    for eps in EPSS:
        lam, amax, rms_sat = {}, {}, {}
        ok_set = True; have = True; reg_set = True
        for n in ns:
            b, p3, p5 = (load(kern, n, eps, d) for d in DELTAS)
            if b is None or p3 is None or p5 is None:
                have = False; lam[n] = None; amax[n] = None; continue
            for lab, rr in (("base", b), ("d1e-3", p3), ("d1e-5", p5)):
                ok_ = rr["status"] == "ok" and rr["n_indef"] == 0 and rr["max_res"] <= 1e-8
                reg_set &= ok_
                if rr["status"] != "ok" or rr["n_indef"] > 0:
                    branched = True
                res["runs"].append({"eps": eps, "n": n, "pair": lab, "status": rr["status"], "n_indef": rr["n_indef"],
                                    "max_res": rr["max_res"], "n_refac": rr.get("n_refac"), "wall_s": rr.get("wall")})
            t = np.array(b["rec"]["t"])
            D5 = pair_D(b, p5)
            tt = t[:len(D5)]
            lam[n] = lyap(D5, tt)[0]
            amax[n] = float(D5.max() / 1e-5) if len(D5) else float("nan")
            sel = tt >= T1D / 2
            rms_sat[n] = float(np.mean(np.array(b["rec"]["yrms"])[:len(tt)][sel])) if sel.any() else None
        regular &= reg_set
        if not have:
            res["complete"] = False
            res["sets"][eps] = {"lambda": lam, "Amax": amax, "class": "INCOMPLETE"}
            continue
        reached = all(lam[n] is not None for n in ns)
        d1 = d2 = d3 = r2_ = r3_ = lam_inf = None; conv = fail = False
        if reached:
            d1, d2, d3 = lam[ns[1]] - lam[ns[0]], lam[ns[2]] - lam[ns[1]], lam[ns[3]] - lam[ns[2]]
            r2_, r3_ = ratio(d2, d1), ratio(d3, d2)
            if r3_ is not None and r3_ < 1:
                lam_inf = lam[ns[3]] + (d3 * r3_ / (1 - r3_) if r3_ != 0 else 0.0)
            else:
                lam_inf = float("inf") if r3_ is not None and r3_ >= 1 and d3 > 0 else None
            conv = (r2_ is not None and r3_ is not None and abs(r2_) <= 0.6 and abs(r3_) <= 0.6
                    and lam_inf is not None and math.isfinite(lam_inf))
            fail = (d3 >= ZERO and r3_ is not None and r3_ >= 0.9)
        bounded = reg_set and all(amax[n] is not None and amax[n] <= 10.0 for n in ns)
        cls = ("CONFIRMED-FAIL" if fail else "RESOLVED-CONVERGENT" if conv else "BOUNDED" if bounded else "OPEN")
        res["sets"][eps] = {"lambda": lam, "Amax": amax, "rms_sat": rms_sat, "increments": [d1, d2, d3], "r2": r2_, "r3": r3_,
                            "lambda_inf": lam_inf, "reached": reached, "convergent": conv, "fail": fail, "bounded": bounded,
                            "regular": reg_set, "class": cls}
    if not res["complete"]:
        verdict = "INCOMPLETE"
    elif branched or any(s["class"] == "CONFIRMED-FAIL" for s in res["sets"].values()):
        verdict = "FAIL" + (" (BRANCHED)" if branched else "")
    elif regular and all(s["class"] in ("RESOLVED-CONVERGENT", "BOUNDED") for s in res["sets"].values()):
        verdict = "CONVERGENT"
    else:
        verdict = "OPEN"
    res["verdict"] = verdict; res["regular"] = regular; res["branched"] = branched
    return res


fr = lambda x_: "None" if x_ is None else ("inf" if x_ == float("inf") else f"{x_:.4f}")
ZF = {}
for k in ["nu_mono"] + CAND:
    ZF[k] = score_kernel(k)
    P(f"\n  --- {k} ---  zero-field verdict: {ZF[k]['verdict']}")
    for eps, s in ZF[k]["sets"].items():
        P(f"    eps {eps:.0e}: lambda " + ", ".join(f"N{n} {fr(s['lambda'][n])}" for n in NS) + "; Amax " +
          ", ".join(f"{s['Amax'][n]:.1f}" if s["Amax"][n] is not None else "-" for n in NS))
        if s["class"] != "INCOMPLETE":
            P(f"      increments {[fr(x) for x in s['increments']]}; r2 {fr(s['r2'])}, r3 {fr(s['r3'])}; lambda_inf {fr(s['lambda_inf'])}; "
              f"<rms yhat>[T/2,T] {[None if s['rms_sat'][n] is None else round(s['rms_sat'][n], 4) for n in NS]}; class {s['class']}")
OUT["zero_field"] = {k: {"verdict": v["verdict"], "regular": v["regular"], "branched": v["branched"],
                         "sets": {f"eps{e:.0e}": {kk: ({str(a): b for a, b in vv.items()} if isinstance(vv, dict) else vv)
                                                 for kk, vv in s.items()} for e, s in v["sets"].items()}, "runs": v["runs"]}
                     for k, v in ZF.items()}

base_ok = ZF["nu_mono"]["verdict"] == "OPEN" and all(
    abs(ZF["nu_mono"]["sets"][e]["lambda"][n] - x) < 5e-5
    for e, row in {1e-3: {127: 0.0414, 255: 0.0663, 511: 0.0721, 1023: 0.0709}, 1e-4: {127: 0.0569, 255: 0.0762, 511: 0.0916, 1023: 0.0875}}.items()
    for n, x in row.items())
check("C1 the nu_mono baseline re-scored from CFG325's committed-run arrays reproduces CFG325's lambda table (4 decimals) and its OPEN verdict",
      f"{ZF['nu_mono']['verdict']}; eps 1e-3 {[fr(ZF['nu_mono']['sets'][1e-3]['lambda'][n]) for n in NS]}; eps 1e-4 "
      f"{[fr(ZF['nu_mono']['sets'][1e-4]['lambda'][n]) for n in NS]}", base_ok)
if not MUTATE:
    c1p = []
    for eps, (l0, a0_) in {1e-3: (0.0414, 338.7), 1e-4: (0.0569, 897.2)}.items():
        b, p5 = load("nu_mono_generic", 127, eps, 0.0), load("nu_mono_generic", 127, eps, 1e-5)
        if b is None or p5 is None:
            c1p.append((eps, None, None, l0, a0_)); continue
        D5 = pair_D(b, p5); t = np.array(b["rec"]["t"])[:len(D5)]
        c1p.append((eps, round(lyap(D5, t)[0], 4), round(float(D5.max() / 1e-5), 1), l0, a0_))
    check("C1' the generic-adapter driver (nu_mono_generic, N = 127, both eps) reproduces CFG325's lambda (4 decimals) and Amax (1 decimal)",
          "; ".join(f"eps {e:.0e}: {l}/{l0}, {a}/{a0_}" for e, l, a, l0, a0_ in c1p),
          all(l == l0 and a == a0_ for e, l, a, l0, a0_ in c1p))
    p1 = {}; p1n = {}
    for k in ("nu_simple", "nu_standard"):
        devs = [abs(ZF[k]["sets"][e]["lambda"][n] - ZF["nu_mono"]["sets"][e]["lambda"][n]) for e in EPSS for n in NS
                if ZF[k]["sets"][e]["lambda"].get(n) is not None and ZF["nu_mono"]["sets"][e]["lambda"].get(n) is not None]
        p1[k] = max(devs) if devs else None; p1n[k] = len(devs)
    # cells done outside the scorer (a set is only scored when complete): direct lambda per (N, eps) cell
    for k in ("nu_simple", "nu_standard"):
        extra = []
        for e in EPSS:
            for n in NS:
                if ZF[k]["sets"][e]["lambda"].get(n) is not None:
                    continue
                b, p5 = load(k, n, e, 0.0), load(k, n, e, 1e-5)
                if b is None or p5 is None:
                    continue
                D5 = pair_D(b, p5); t = np.array(b["rec"]["t"])[:len(D5)]
                lk = lyap(D5, t)[0]; lm = ZF["nu_mono"]["sets"][e]["lambda"][n]
                if lk is not None and lm is not None:
                    extra.append(abs(lk - lm))
        if extra:
            p1[k] = max([p1[k]] + extra) if p1[k] is not None else max(extra); p1n[k] += len(extra)
    P(f"    P1: max |lambda_k - lambda_nu_mono| over the (N, eps) cells available (of 8): " +
      ", ".join(f"{k} {fr(v)} ({p1n[k]} cells)" for k, v in p1.items()))
    check("P1 (prediction frozen before any run) the class-(ii) kernels reproduce nu_mono's lambda(N) to within 0.001 at every N and eps "
          "(evaluated on every available cell; the full 8-cell ladder is required for at least one class-(ii) kernel)",
          {k: (fr(v), p1n[k]) for k, v in p1.items()},
          all(v is None or v <= 0.001 for v in p1.values()) and max(p1n.values()) == 8)
    if any(v is not None and v > 0.005 for v in p1.values()):
        P("    *** FLAG: a class-(ii) kernel differs from nu_mono by > 0.005 in lambda: the analytic picture is WRONG (frozen flag) ***")
    OUT["P1_cells"] = p1n
    OUT["P1"] = p1

# ================================================================================================================ table + verdict
banner("TABLE  kernel x gate  (VIABLE = SPARC-PASS and zero-field CONVERGENT; (ii) reported beside it)")
rows = []
for k in ["nu_mono"] + CAND + REFS:
    zf = ZF.get(k)
    zc = (zf["sets"][1e-3]["class"], zf["sets"][1e-4]["class"], zf["verdict"]) if zf else ("not run", "not run", "class (ii): = nu_mono by P1")
    viable = bool(SP[k]["pass"] and zf is not None and zf["verdict"] == "CONVERGENT")
    if SP[k]["pass"] and zf is not None and zf["verdict"] == "INCOMPLETE":
        viable = "UNDECIDED (zero-field incomplete)"
    rows.append(dict(kernel=k, ii=KN.LIMITS_II[k], dchi2_free=SP[k]["T-free"]["dchi2"], dchi2_fix=SP[k]["T-fix"]["dchi2"],
                     kappa_L_free=SP[k]["T-free"]["kappa_L"], kappa_crit_free=SP[k]["T-free"]["kappa_crit"],
                     kappa_L_fix=SP[k]["T-fix"]["kappa_L"], sparc_pass=SP[k]["pass"], zf_eps1e3=zc[0], zf_eps1e4=zc[1], zf=zc[2],
                     viable=viable, viable_with_ii_exact=(viable is True) and KN.LIMITS_II[k] == "exact"))
P(f"  {'kernel':12s} {'(ii)':26s} {'dchi2 free/fix':>16s} {'kappa_L free/fix':>17s} {'SPARC':>6s} {'ZF eps1e-3':>20s} {'ZF eps1e-4':>20s} "
  f"{'ZF verdict':>16s} {'VIABLE':>7s}")
for r in rows:
    P(f"  {r['kernel']:12s} {r['ii']:26s} {r['dchi2_free']:+7.2f}/{r['dchi2_fix']:+7.2f} {r['kappa_L_free']:8.3f}/{r['kappa_L_fix']:7.3f} "
      f"{str(r['sparc_pass']):>6s} {r['zf_eps1e3']:>20s} {r['zf_eps1e4']:>20s} {r['zf']:>16s} {str(r['viable'])[:9]:>9s}")
OUT["table"] = rows
viable = [r["kernel"] for r in rows if r["viable"] is True]
viable_exact = [r["kernel"] for r in rows if r["viable_with_ii_exact"]]
incomplete = any(ZF[k]["verdict"] == "INCOMPLETE" for k in ZF)
# the answer is undecided only if a kernel with (ii) exact that PASSES SPARC lacks its zero-field verdict
undecided_exact = [r["kernel"] for r in rows if r["viable"] not in (True, False) and r["ii"] == "exact"]

banner("VERDICT (frozen rule)")
if MUTATE:
    m = [r for r in rows if r["kernel"] == "MUTATE_kink"][0]
    mut_ok = (m["viable"] is False) and m["zf"] != "INCOMPLETE"
    P(f"  MUTATE kinked kernel: SPARC-PASS {m['sparc_pass']} (dchi2 {m['dchi2_free']:+.2f} / {m['dchi2_fix']:+.2f}); zero-field {m['zf']} "
      f"({m['zf_eps1e3']}, {m['zf_eps1e4']}); VIABLE {m['viable']}")
    P("  secondary reading (not load-bearing): " + ("the zero-field arm ALSO converges for the kinked kernel -> zero-field convergence "
      "cannot be credited to smoothness" if m["zf"] == "CONVERGENT" else f"the zero-field arm alone does not pass the kinked kernel ({m['zf']})"))
    check("MUTATE the kinked kernel (1/nu piecewise linear in sqrt y) does NOT come out VIABLE", f"VIABLE {m['viable']}; incomplete {incomplete}", mut_ok)
    OUT["verdict"] = {"mutate_not_viable": mut_ok, "sparc_pass": m["sparc_pass"], "zero_field": m["zf"]}
else:
    ans = "YES" if viable_exact else ("UNDECIDED" if undecided_exact else "NO")
    undec = [r["kernel"] for r in rows if r["viable"] not in (True, False)]
    if incomplete:
        P(f"  incomplete zero-field ladders: {[k for k in ZF if ZF[k]['verdict'] == 'INCOMPLETE']}; VIABLE undecided for: {undec if undec else 'none'} "
          "(a kernel failing SPARC is not VIABLE whatever its zero-field verdict)")
    P(f"  VIABLE kernels: {viable if viable else 'none'};  VIABLE with (ii) exact: {viable_exact if viable_exact else 'none'}")
    P(f"  ANSWER to the question (a kernel with (i) + (ii) exact + (iii)): {ans}")
    for k in viable:
        if KN.LIMITS_II[k] != "exact":
            P(f"    {k}: VIABLE only with (ii) operational -- it adds a declared constant (the splice point), against the zero-knob rule: an OPTION, not adopted")
    P("  Scope: the zero-field arm concerns the UNGATED chassis only (law on everywhere, open FRW background, 1-D, data class D); "
      "nothing about candidate B, growth or sigma_8.  N = 2047 not run (a CONVERGENT at 1023 needs it: nu_mono's OPEN at 1023 became FAIL at 2047).")
    OUT["verdict"] = {"viable": viable, "viable_ii_exact": viable_exact, "answer": ans}

npass = sum(1 for c_ in CH if c_[1])
P(f"\n  {npass}/{len(CH)} checks pass; wall {time.time() - T0:.0f} s")
OUT["summary"] = {"pass": npass, "total": len(CH), "wall_s": time.time() - T0}
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (None if isinstance(o, float) and not math.isfinite(o) else str(o)))
if MUTATE:
    sys.exit(1 if OUT["verdict"]["mutate_not_viable"] else 0)
sys.exit(0 if npass == len(CH) else 1)
