#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG80 -- A LCDM COMPARATOR FOR CFG33 (the SLACS Einstein radii against ATLAS3D dynamics, a lensing-versus-dynamics consistency test inside
candidate B).  Through CFG33's IDENTICAL pipeline, does a standard LCDM halo show B's lensing-dynamics gap?  SPECIFIC-TO-B, SHARED,
LCDM-WORSE or NON-DISCRIMINATING?

Criteria frozen and committed before this script existed and before any LCDM prediction for these data: campaign_fresh_gravity/
CFG80_FROZEN_CRITERIA.md (commit fe0c1c040).  kappa = 1/2 is FITTED for B; nothing is tuned; nothing here says the data favour B or LCDM,
and nothing says the theory is closed.

IDENTICAL TO CFG33 (exec'd READ-ONLY with CFG69's exec_prefix pattern, a read-only open, its MUTATE forced off): h53's 70 SLACS lenses
(R_E; h53's M_E = pi R_E^2 Sigma_crit in Auger's cosmology; Auger's Salpeter f_* and M_Salp; the SDSS dispersion); h9's ATLAS3D sample
(258, of which 187 have JAM quality >= 1); log alpha_dyn fitted linearly in (log sigma_e - 2.3) and evaluated at each lens's dispersion; the
median statistic; 2000 bootstrap resamples (lenses and calibration set, the fit redone); the 0.10-dex floor.  B's four cells come from it.

THE LCDM MODEL (declared once; CFG69's "base"): stars alpha x the lane's Salpeter mass (lens: projected alpha f_*,Salp M_E, Auger's measured
fraction; ATLAS3D: half the stars inside r_1/2) plus (1 - f_b) M_NFW.  M_h = h48's Moster+2013 halo_mass(M_*) (via CFG45's exec, as CFG69)
at the stellar mass the model solves for, M_* = alpha M_Salp (CFG69's tie).  Duffy+2008 full 200c at z = 0 (rho_c(z = 0), H0 = 67.4:
h48's RHO_C).  c_duffy_full, c_duffy_relaxed, c_dm, _m_nfw, make_nfw and jam_mass_lcdm are copied verbatim from CFG69.  Lensing uses the
analytic untruncated projected NFW mass (Bartelmann 1996 / Wright & Brainerd 2000).  Newtonian; no adiabatic contraction and no SHMR
scatter (both untested).  LCDM has no a0: one set of numbers serves both footings, and (no contraction) its V and I rows are identical by
construction.
  lens   kappa_bar(alpha) = alpha f_* + (1 - f_b) M_2D,NFW(<R_E; M_h(alpha M_Salp)) / M_E = 1, solved in log M_* in [8, 13.5]
  JAM    0.5 M_* + (1 - f_b) M_NFW(<r_1/2; M_h(M_*)) = M_JAM / 2, log M_* in [8, 13.5] (CFG69's jam_mass_lcdm)
  no root in the bracket -> the system is excluded and counted (as CFG69 does for SLUGGS).

PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG33's committed B numbers reproduced through this exec, to its printed precision (its four H2 lines verbatim in the
               committed .out; the JSON within half a printed unit); and the generic estimator used for LCDM reproduces B's four differences
               and bootstrap errors to 1e-12 with CFG33's seed and draw order.
  C2  CONTROL  make_nfw: M(<R_200c) = M_h to 1e-12 (three c relations, M_h 1e9-1e17.5), monotone; the copied functions are CFG69's source
               text; RHO_C = 3 H0^2 / (8 pi G) at H0 = 67.4 (z = 0) to 1e-12.
  C3  CONTROL  the analytic projected NFW mass equals a direct numerical projection of the 3D NFW density (shells into the cylinder; the
               line-of-sight Sigma integrated over the disc) to 1e-4.
  C4  CONTROL  solve residuals 1e-9 (kappa_bar = 1; M(<r_1/2) = M_JAM / 2); halo off -> alpha_lens = 1 / f_*, alpha_dyn = M_JAM / M_Salp to
               1e-9; the halo only lowers alpha.
  C5  MUTATE WITNESS  the halo mass entering every base solve is the Moster value of its stellar mass (ratio 1 to 1e-12): passes in the main
               run and FAILS under MUTATE by construction (ratio 100).  It guarantees rc = 1 and a different failing set under MUTATE; it
               says nothing about whether the science responds.
  H1  [HEADLINE] LCDM PASSES CFG33's GATE: H1a >= 35 of 70 lenses solved; H1b >= 94 of 187 calibration galaxies calibrated; H1c |Delta| <=
               2 sigma_tot (bootstrap + 0.10 dex).  Outcome PASS / FAIL+ / FAIL- / UNFIT.  PASS -> SPECIFIC-TO-B; FAIL+ (B's sign) -> SHARED;
               FAIL- -> LCDM-WORSE; UNFIT -> no class.
  C6  (load-bearing in the MUTATE run only; R6 in the main run) the gate outcome changes when every M_h is x 100 (both multipliers
               computed in-process in every run); unchanged -> NON-DISCRIMINATING.
  R1-R7 (reported) the statistical-only z and class; B - LCDM (paired bootstrap); the variants V1 Dutton-Maccio c, V2 Duffy relaxed, V3 / V4
               every M_h x 1/3, x 3; CFG33's dispersion bins and the slopes; diagnostics (M_h, dark fractions, the Moster-grid clamp,
               make_nfw's inner clip, exclusions); the x 100 gate (C6 / R6); the 5 R_200 saturation of the projection.
MUTATE=1: every LCDM halo mass x 100 (base and variants, lenses and ATLAS3D; B not mutated) -- rc = 1 (C5); C6 asks whether H1's outcome
changes.
Run: python3 campaign_fresh_gravity/CFG80_lcdm_slacs.py   (then MUTATE=1 for the control; about 20 s each)
"""
import os, sys, io, math, json, ast, contextlib, time, warnings
sys.dont_write_bytecode = True
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = HERE
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG80_lcdm_slacs", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every LCDM halo mass x 100 -- rc must be 1 (C5 witness); C6 asks whether the LCDM gate outcome changes ***")
HMUT = 100.0 if MUTATE else 1.0            # this run's multiplier on every LCDM halo mass
HOTHER = 1.0 if MUTATE else 100.0          # the other multiplier, computed in-process in every run (C6 / R6)
TAG = "  [MUTATE: every M_h x 100]" if MUTATE else ""
FOOTS, BANDS = ("canonical", "alt"), ("V", "I")
NaN = float("nan")


# ================================================================================================ read-only exec of the lanes (their own MUTATE forced off)
def exec_prefix(fname, marker, replace=None):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    pre = src[:src.index(marker)]
    for a, b in (replace or []):
        assert pre.count(a) == 1
        pre = pre.replace(a, b)
    g = {"__file__": os.path.join(LANES, fname), "__name__": "lane_" + fname, "open": C.C4._ro_open}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(pre, fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


BAR = "# ================================================================================================ "
g45 = exec_prefix("CFG45_rule_readings.py", BAR + "P3 SPARC", [('READ = ("L", "S", "M", "E")', 'READ = ("L", "S")')])
FB, halo_mass, RHO_C = g45["FB"], g45["halo_mass"], g45["RHO_C"]
LMS_TOP = float(halo_mass.__globals__["_LMS"][-1])          # log M_* at the top of h48's Moster grid (M_h = 10^15.5); above it M_h is clamped
g33 = exec_prefix("CFG33_slacs_lensing_vs_dynamics.py", 'R.banner("R1-R4  REPORTED")')
assert g33["MUTATE"] is False and g33["FMUT"] == 1.0
S, ET, Q = g33["S"], g33["ET"], g33["Q"]
LENS, DYN, RES33 = g33["LENS"], g33["DYN"], g33["RES"]
LSIG_A, LSIG_L, PIV, FLOOR = g33["LSIG_A"], g33["LSIG_L"], g33["PIV"], g33["FLOOR"]
g53 = g33["g53"]
HH = 0.674
NL, NQ = len(S), int(Q.sum())
NL_MIN, ND_MIN = math.ceil(NL / 2), math.ceil(NQ / 2)
P(f"\n  exec'd read-only: CFG45's prefix (f_b {FB:.4f}; rho_c(z = 0) {RHO_C:.4e} Msun/Mpc^3; Moster grid top log M_* {LMS_TOP:.3f}); CFG33 up to "
  f"its reported rows: {NL} lenses, {len(ET)} ATLAS3D, {NQ} with JAM quality >= 1 (H1a needs >= {NL_MIN}, H1b >= {ND_MIN})   {R.el()}")


# ================================================================================================ the LCDM halo: copied VERBATIM from CFG69 (C2 compares the source text)
def c_duffy_full(Mh):
    return 5.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.084)


def c_duffy_relaxed(Mh):
    return 6.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.091)


def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * (np.log10(np.asarray(Mh, float) * 0.674) - 12.0))


def _m_nfw(t):
    return np.log1p(t) - t / (1 + t)


def make_nfw(cfn):
    def f(Mh, r_kpc):
        Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
        c = cfn(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        x = np.clip(r_kpc / R200, 1e-4, 5.0)
        return Mh * _m_nfw(c * x) / _m_nfw(c)
    return f


def jam_mass_lcdm(g, cfg):
    prof, hmf, halo = cfg["prof"], cfg["hmf"], cfg["halo"]

    def fr(lm):
        Ms = 10 ** lm
        return math.log10(0.5 * Ms + (1 - FB) * float(prof(halo(Ms) * hmf, g["r12"]))) - math.log10(g["Mjam"] / 2)
    if fr(8.0) * fr(13.5) > 0:
        return float("nan")
    return 10 ** brentq(fr, 8.0, 13.5, xtol=1e-12)


# ================================================================================================ lensing: the analytic projected NFW mass (new here; C3 checks it)
def h_proj(X):
    """Bartelmann 1996 / Wright & Brainerd 2000: the untruncated NFW's projected mass inside R is 4 pi rho_s r_s^3 h(X), X = R / r_s, with
    h = ln(X/2) + 2/sqrt(1-X^2) artanh sqrt((1-X)/(1+X)) (X < 1), ln(X/2) + 2/sqrt(X^2-1) arctan sqrt((X-1)/(X+1)) (X > 1), 1 + ln(1/2) (X = 1).
    For X < 0.5 the X < 1 expression is evaluated in the algebraically identical, cancellation-free form h = [ln(2/X) q + ln(1 - q/2)] /
    sqrt(1 - X^2), q = X^2 / (1 + sqrt(1 - X^2)): in double precision the literal form loses accuracy below X ~ 1e-3 (the artanh argument
    tends to 1), e.g. 2.6e-5 relative at X = 7e-5 (a unit test on synthetic inputs, before any data run; the rewrite matches a 50-digit
    evaluation of the literal form to machine precision)."""
    X = np.atleast_1d(np.asarray(X, float)); out = np.empty_like(X)
    sm = X < 0.5
    lo, hi = (X >= 0.5) & (X < 1 - 1e-6), X > 1 + 1e-6
    mid = ~(sm | lo | hi)
    xs, xl, xh = X[sm], X[lo], X[hi]
    sq = np.sqrt(1 - xs ** 2); q = xs ** 2 / (1 + sq)
    out[sm] = (np.log(2 / xs) * q + np.log1p(-q / 2)) / sq
    out[lo] = np.log(xl / 2) + 2 / np.sqrt(1 - xl ** 2) * np.arctanh(np.sqrt((1 - xl) / (1 + xl)))
    out[hi] = np.log(xh / 2) + 2 / np.sqrt(xh ** 2 - 1) * np.arctan(np.sqrt((xh - 1) / (xh + 1)))
    out[mid] = 1 + np.log(0.5) + (X[mid] - 1) / 3.0          # h(1) = 1 + ln(1/2), h'(1) = F(1) = 1/3 (used only for |X - 1| < 1e-6)
    return out


def make_nfw_proj(cfn):
    """M_2D(<R) of make_nfw's halo (same c, same R_200c, normalised to M_h at R_200); the line of sight is NOT truncated."""
    def f(Mh, R_kpc):
        Mh = float(Mh); c = float(cfn(Mh)); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        return Mh * float(h_proj(c * float(R_kpc) / R200)[0]) / float(_m_nfw(c))
    return f


def r200_of(Mh):
    return (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0


# ================================================================================================ the configurations (declared in the frozen file)
def make_cfgs(mult):
    d = {
        "base": dict(label="base: Moster + Duffy full 200c (THE declared LCDM)", cfn=c_duffy_full, hmf=mult),
        "V1": dict(label="V1 Moster + Dutton-Maccio c", cfn=c_dm, hmf=mult),
        "V2": dict(label="V2 Moster + Duffy relaxed 200c", cfn=c_duffy_relaxed, hmf=mult),
        "V3": dict(label="V3 base, every M_h x 1/3", cfn=c_duffy_full, hmf=mult / 3.0),
        "V4": dict(label="V4 base, every M_h x 3", cfn=c_duffy_full, hmf=mult * 3.0),
    }
    for v in d.values():
        v["prof"], v["proj"], v["halo"] = make_nfw(v["cfn"]), make_nfw_proj(v["cfn"]), (lambda Ms: float(halo_mass(Ms)))
    return d


CFGS = make_cfgs(HMUT)
OTHER = make_cfgs(HOTHER)["base"]; OTHER["label"] = f"base with every M_h x {HOTHER:g} (in-process; C6 / R6)"
ZERO = make_cfgs(1e-30)["base"]; ZERO["label"] = "halo switched off (M_h x 1e-30; C4)"


def lens_kappa(d, cfg, Ms, rec=None):
    """mean convergence inside the observed R_E: stars (Auger's measured projected fraction, scaled) plus (1 - f_b) the projected NFW."""
    Mh = cfg["halo"](Ms) * cfg["hmf"]
    if rec is not None:
        rec.append(Mh)
    return Ms / 10 ** d["lMs"] * d["Fs"] + (1 - FB) * float(cfg["proj"](Mh, d["RE"])) / d["ME"]


def lens_mass_lcdm(d, cfg):
    """the lens analogue of CFG69's jam_mass_lcdm: the stellar mass at which stars + (1 - f_b) NFW give mean convergence 1 at R_E."""
    def fr(lm):
        return math.log10(lens_kappa(d, cfg, 10 ** lm))
    if fr(8.0) * fr(13.5) > 0:
        return float("nan")
    return 10 ** brentq(fr, 8.0, 13.5, xtol=1e-12)


def jam_model(g, cfg, Ms, rec=None):
    """the model's total mass inside r_1/2 (jam_mass_lcdm's expression, for the residual and the witness)."""
    Mh = cfg["halo"](Ms) * cfg["hmf"]
    if rec is not None:
        rec.append(Mh)
    return 0.5 * Ms + (1 - FB) * float(cfg["prof"](Mh, g["r12"]))


MSL = np.array([10 ** d["lMs"] for d in S]); MSA = np.array([e["Msalp"] for e in ET])
FS = np.array([d["Fs"] for d in S]); JR = np.array([e["Mjam"] / e["Msalp"] for e in ET])


def run_config(cfg):
    Ml = np.array([lens_mass_lcdm(d, cfg) for d in S])
    Md = np.array([jam_mass_lcdm(e, cfg) for e in ET])
    return dict(Ml=Ml, Md=Md, al=Ml / MSL, ad=Md / MSA)


# ================================================================================================ CFG33's statistic, generic (C1 checks it against CFG33's own)
def gstat(al, ad, il, idd):
    b_, a_ = np.polyfit(LSIG_A[idd] - PIV, np.log10(ad[idd]), 1)
    return float(np.median(np.log10(al[il]) - (a_ + b_ * (LSIG_L[il] - PIV)))), float(b_), float(a_)


def gboot(al, ad, lset, dset, rng, n=2000):
    out = np.empty((n, 2))
    for k in range(n):
        il = lset[rng.integers(0, len(lset), len(lset))]
        idd = rng.choice(dset, len(dset))
        d_, b_, _ = gstat(al, ad, il, idd)
        out[k] = (d_, b_)
    return out


def outcome_of(nl, nd, z):
    if nl < NL_MIN or nd < ND_MIN or not np.isfinite(z):
        return "UNFIT"
    return "PASS" if abs(z) <= 2 else ("FAIL+" if z > 0 else "FAIL-")


def score(res):
    al, ad = res["al"], res["ad"]
    lset = np.where(np.isfinite(al))[0]; dset = np.where(Q & np.isfinite(ad))[0]
    out = dict(n_lens=int(len(lset)), n_cal=int(len(dset)), lset=lset, dset=dset)
    if len(lset) >= 3 and len(dset) >= 3:
        d0, b0, a0_ = gstat(al, ad, lset, dset)
        bs = gboot(al, ad, lset, dset, np.random.default_rng(33))
        err = float(np.std(bs[:, 0])); tot = math.hypot(err, FLOOR)
        out.update(delta=d0, err=err, tot=tot, z=d0 / tot, z_stat=d0 / err, slope=b0, slope_err=float(np.std(bs[:, 1])),
                   lens_med=float(np.median(np.log10(al[lset]))), dyn_at_lens=float(np.median(a0_ + b0 * (LSIG_L[lset] - PIV))))
    else:
        out.update(delta=NaN, err=NaN, tot=NaN, z=NaN, z_stat=NaN, slope=NaN, slope_err=NaN, lens_med=NaN, dyn_at_lens=NaN)
    out["outcome"] = outcome_of(out["n_lens"], out["n_cal"], out["z"])
    return out


def cls_of(z, dl, dB, outcome=None):
    if outcome == "UNFIT" or not np.isfinite(z):
        return "UNFIT"
    if abs(z) <= 2:
        return "SPECIFIC-TO-B"
    return "SHARED" if np.sign(dl) == np.sign(dB) else "LCDM-WORSE"


def pub(sc):
    return {k: v for k, v in sc.items() if k not in ("lset", "dset")}


def line_of(sc):
    if not np.isfinite(sc["delta"]):
        return f"lenses solved {sc['n_lens']}/{NL}, calibrated {sc['n_cal']}/{NQ}: too few to score; outcome {sc['outcome']}"
    return (f"lenses solved {sc['n_lens']}/{NL}, calibrated {sc['n_cal']}/{NQ}; median log alpha_lens {sc['lens_med']:+.3f} (x{10 ** sc['lens_med']:.2f}); "
            f"alpha_dyn at the lenses' dispersions {sc['dyn_at_lens']:+.3f} (x{10 ** sc['dyn_at_lens']:.2f}); Delta {sc['delta']:+.3f} +- {sc['err']:.3f} (stat) "
            f"-> {sc['z']:+.2f} sigma with the floor ({sc['z_stat']:+.1f} without); outcome {sc['outcome']}")


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG33's committed B numbers through this script's exec of its pipeline (printed precision); the generic estimator")
o33 = open(os.path.join(LANES, "CFG33_slacs_lensing_vs_dynamics.out")).read()
j33 = json.load(open(os.path.join(LANES, "CFG33_slacs_lensing_vs_dynamics_results.json")))["numbers"]["H2"]


def line33(f, b, v):
    return (f"    {f:9s} {b}: median log alpha_lens {v['lens_med']:+.3f} (x{10 ** v['lens_med']:.2f} Salpeter); alpha_dyn at the lenses' "
            f"dispersions {v['dyn_at_lens']:+.3f} (x{10 ** v['dyn_at_lens']:.2f}); difference {v['delta']:+.3f} +- {v['err']:.3f} (stat) -> "
            f"{v['z']:+.2f} sigma with the {FLOOR} dex floor ({v['z_nofloor']:+.1f} without)")


HALF = dict(lens_med=5e-4, dyn_at_lens=5e-4, delta=5e-4, err=5e-4, tot=5e-4, z=5e-3, z_nofloor=5e-2)
lines_ok = all(line33(f, b, RES33[(f, b)]) in o33 for f in FOOTS for b in BANDS)
jdev = {k: max(abs(RES33[(f, b)][k] - j33[f"{f}|{b}"][k]) for f in FOOTS for b in BANDS) for k in HALF}
json_ok = all(jdev[k] <= HALF[k] for k in HALF)
rng_c1 = np.random.default_rng(33); QIDX = np.where(Q)[0]; LALL = np.arange(NL)
gdev = 0.0
for f in FOOTS:
    for b in BANDS:
        al_, ad_ = LENS[(f, b)][1], DYN[f]
        d_ = gstat(al_, ad_, LALL, QIDX)[0]
        e_ = float(np.std(gboot(al_, ad_, LALL, QIDX, rng_c1)[:, 0]))
        gdev = max(gdev, abs(d_ - RES33[(f, b)]["delta"]), abs(e_ - RES33[(f, b)]["err"]))
        P(line33(f, b, RES33[(f, b)]))
check("C1 CONTROL: CFG33's committed B numbers reproduced through this exec to its printed precision (alpha_lens, alpha_dyn at the lenses' "
      "dispersions, the difference +- stat, z with and without the floor; four cells), and the generic estimator used for LCDM reproduces "
      "B's four differences and bootstrap errors to 1e-12 (CFG33's seed and draw order)",
      f"the four H2 lines rebuilt from the exec appear verbatim in the committed .out: {lines_ok}; max |exec - committed JSON|: "
      + ", ".join(f"{k} {v:.1e}" for k, v in jdev.items()) + f"; generic estimator vs CFG33 (difference and bootstrap error): max dev {gdev:.1e}",
      lines_ok and json_ok and gdev <= 1e-12)

# ================================================================================================ C2
R.banner("C2  CONTROL: the NFW profile (M(<R_200c) = M_h), the verbatim copies from CFG69, rho_c at z = 0")
dev_r200, mono = 0.0, True
for cf_ in (c_duffy_full, c_duffy_relaxed, c_dm):
    f_ = make_nfw(cf_)
    for Mh in np.logspace(9.0, 17.5, 18):
        R200 = r200_of(Mh)
        dev_r200 = max(dev_r200, abs(float(f_(Mh, R200)) / Mh - 1.0))
        rr = np.logspace(math.log10(1.001e-4 * R200), math.log10(0.999 * 5 * R200), 200)
        mono = mono and bool(np.all(np.diff(np.asarray(f_(Mh, rr))) > 0))
src69 = open(os.path.join(LANES, "CFG69_lcdm_comparator.py")).read()
src80 = open(os.path.abspath(__file__)).read()


def fsrc(src, name):
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(src, node)
    return None


COPIED = ("c_duffy_full", "c_duffy_relaxed", "c_dm", "_m_nfw", "make_nfw", "jam_mass_lcdm")
same_src = {n: (fsrc(src69, n) is not None and fsrc(src69, n) == fsrc(src80, n)) for n in COPIED}
rho_c_z0 = 3 * (67.4 * 1e3 / g53["Mpc"]) ** 2 / (8 * math.pi * g53["G"]) / g53["Msun"] * (3.0857e22) ** 3
dev_rho = abs(RHO_C / rho_c_z0 - 1)
check("C2 CONTROL: make_nfw gives M(<R_200c) = M_h to 1e-12 (Duffy full / relaxed / Dutton-Maccio c, M_h 1e9-1e17.5), monotone; the copied "
      "functions are CFG69's source text; RHO_C is rho_c(z = 0) at H0 = 67.4 in h48's constants to 1e-12",
      f"max |M(<R200)/M_h - 1| {dev_r200:.1e}; monotone {mono}; verbatim: " + ", ".join(f"{n} {v}" for n, v in same_src.items())
      + f"; RHO_C {RHO_C:.6e} vs {rho_c_z0:.6e} Msun/Mpc^3 (dev {dev_rho:.1e})",
      dev_r200 <= 1e-12 and mono and all(same_src.values()) and dev_rho <= 1e-12)

# ================================================================================================ C3
R.banner("C3  CONTROL: the analytic projected NFW mass against a direct numerical projection of the 3D density")
QK = dict(epsabs=0.0, epsrel=1e-11, limit=400)


def f3(t):
    return t / (1.0 + t) ** 2                               # 4 pi r^2 rho(r) dr in units of 4 pi rho_s r_s^3, t = r / r_s


def proj_shells(Mh, R_kpc, cfn):
    """spherical shells projected into the cylinder: inside R all of a shell, outside the fraction 1 - sqrt(1 - R^2/r^2)."""
    c = float(cfn(Mh)); X = c * R_kpc / r200_of(Mh)
    I_c = integrate.quad(f3, 0.0, c, **QK)[0]
    I_in = integrate.quad(f3, 0.0, X, **QK)[0]

    def w_out(ph):                                          # t = X / sin(ph); 1 - cos(ph) = 2 sin^2(ph / 2); dt = X cos(ph) / sin^2(ph) dph
        s = math.sin(ph)
        return f3(X / s) * 2.0 * math.sin(0.5 * ph) ** 2 * X * math.cos(ph) / s ** 2 if s > 0 else 0.0
    brk = [p for p in np.geomspace(max(X, 1e-12) / 10.0, 1.0, 12) if 0.0 < p < math.pi / 2]
    I_out = integrate.quad(w_out, 0.0, math.pi / 2, points=brk, **QK)[0]
    return Mh * (I_in + I_out) / I_c


def proj_los(Mh, R_kpc, cfn):
    """Sigma(xi) = 2 rho_s r_s int_0^inf du / (1 + xi cosh u)^2 (z = xi sinh u along the line of sight), integrated over the disc."""
    c = float(cfn(Mh)); X = c * R_kpc / r200_of(Mh)
    I_c = integrate.quad(f3, 0.0, c, **QK)[0]

    def J(xi):
        u0 = math.log(2.0 / xi) if xi < 2.0 else 0.0
        U = 60.0 + max(0.0, u0)
        return integrate.quad(lambda u: 1.0 / (1.0 + xi * math.cosh(u)) ** 2, 0.0, U, points=[u0] if 0.0 < u0 < U else None,
                              epsabs=0.0, epsrel=1e-10, limit=400)[0]
    return Mh * integrate.quad(lambda xi: xi * J(xi), 0.0, X, epsabs=0.0, epsrel=1e-9, limit=400)[0] / I_c


dev_sh, dev_los, npts, Xs = 0.0, 0.0, 0, []
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for cf_ in (c_duffy_full, c_duffy_relaxed, c_dm):
        pa = make_nfw_proj(cf_)
        grid = [(Mh, Rk) for Mh in (1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17) for Rk in (0.3, 1.0, 3.0, 5.0, 8.0, 30.0, 100.0)]
        grid += [(Mh, r200_of(Mh) / float(cf_(Mh))) for Mh in (1e11, 1e13, 1e15)]          # X = 1 exactly (R = r_s)
        for Mh, Rk in grid:
            a = pa(Mh, Rk)
            Xs.append(float(cf_(Mh)) * Rk / r200_of(Mh))
            dev_sh = max(dev_sh, abs(proj_shells(Mh, Rk, cf_) / a - 1.0))
            dev_los = max(dev_los, abs(proj_los(Mh, Rk, cf_) / a - 1.0))
            npts += 1
check("C3 CONTROL: the analytic projected NFW mass (Bartelmann 1996 / Wright & Brainerd 2000, untruncated) equals a direct numerical "
      "projection of the 3D NFW density to 1e-4 (shells into the cylinder; the line-of-sight Sigma integrated over the disc)",
      f"{npts} points (3 c relations x [8 masses 1e10-1e17 x 7 radii 0.3-100 kpc + 3 at X = 1 exactly]; X {min(Xs):.1e} to {max(Xs):.1e}): "
      f"max |analytic / shells - 1| {dev_sh:.1e}; max |analytic / line of sight - 1| {dev_los:.1e}",
      dev_sh <= 1e-4 and dev_los <= 1e-4)

# ================================================================================================ the LCDM engine
R.banner("THE LCDM ENGINE: every configuration through CFG33's lenses and ATLAS3D calibration set" + TAG)
LC = {k: run_config(v) for k, v in CFGS.items()}
LC_OTHER, LC_ZERO = run_config(OTHER), run_config(ZERO)
SC = {k: score(v) for k, v in LC.items()}
SC_OTHER = score(LC_OTHER)
for k, v in SC.items():
    P(f"    {CFGS[k]['label']:52s} (M_h x {CFGS[k]['hmf']:g}): {line_of(v)}")
P(f"    {OTHER['label']:52s} (M_h x {OTHER['hmf']:g}): {line_of(SC_OTHER)}")
P("    (LCDM has no a0: these numbers serve both footings; without adiabatic contraction the stellar profile does not enter, so V = I)")
P(f"    B (CFG33, exec'd): " + "; ".join(f"{f} {b} {v['delta']:+.3f} +- {v['err']:.3f} ({v['z']:+.2f} sigma with the floor, {v['z_nofloor']:+.1f} stat)"
                                        for (f, b), v in RES33.items()) + f"   {R.el()}")
base, sb = LC["base"], SC["base"]

# ================================================================================================ C4
R.banner("C4  CONTROL: the solves (residuals; the halo switched off; the halo only adds mass)" + TAG)
res_l = max([abs(lens_kappa(d, CFGS["base"], base["Ml"][i]) - 1.0) for i, d in enumerate(S) if np.isfinite(base["Ml"][i])] or [NaN])
res_d = max([abs(jam_model(e, CFGS["base"], base["Md"][j]) / (e["Mjam"] / 2) - 1.0) for j, e in enumerate(ET) if np.isfinite(base["Md"][j])] or [NaN])
z_all = bool(np.all(np.isfinite(LC_ZERO["al"])) and np.all(np.isfinite(LC_ZERO["ad"])))
dz_l = float(np.nanmax(np.abs(LC_ZERO["al"] * FS - 1.0))); dz_d = float(np.nanmax(np.abs(LC_ZERO["ad"] / JR - 1.0)))
okl, okd = np.isfinite(base["al"]), np.isfinite(base["ad"])
adds = bool(np.all(base["al"][okl] <= (1.0 / FS[okl]) * (1 + 1e-9)) and np.all(base["ad"][okd] <= JR[okd] * (1 + 1e-9)))
check("C4 CONTROL: the solves -- kappa_bar(alpha_lens) = 1 and M(<r_1/2) = M_JAM / 2 to 1e-9; with the halo switched off alpha_lens = 1 / f_* and "
      "alpha_dyn = M_JAM / M_Salp to 1e-9 at every system; the halo only lowers alpha (it adds mass, never removes it)",
      f"max residual: lenses {res_l:.1e} ({int(okl.sum())} solved), ATLAS3D {res_d:.1e} ({int(okd.sum())} solved of {len(ET)}); halo off: all solved "
      f"{z_all}, max dev {dz_l:.1e} (lenses) / {dz_d:.1e} (ATLAS3D); alpha_LCDM <= the stars-only value everywhere: {adds}",
      res_l <= 1e-9 and res_d <= 1e-9 and z_all and dz_l <= 1e-9 and dz_d <= 1e-9 and adds)

# ================================================================================================ C5
R.banner("C5  MUTATE WITNESS: the halo mass entering every base-model solve is the declared Moster value of its stellar mass")
wdev, nw = 0.0, 0
for i, d in enumerate(S):
    if np.isfinite(base["Ml"][i]):
        rec = []; lens_kappa(d, CFGS["base"], base["Ml"][i], rec)
        wdev = max(wdev, abs(rec[0] / float(halo_mass(base["Ml"][i])) - 1.0)); nw += 1
for j, e in enumerate(ET):
    if Q[j] and np.isfinite(base["Md"][j]):
        rec = []; jam_model(e, CFGS["base"], base["Md"][j], rec)
        wdev = max(wdev, abs(rec[0] / float(halo_mass(base["Md"][j])) - 1.0)); nw += 1
check("C5 MUTATE WITNESS: the halo mass entering every base-model solve (lens and JAM) equals halo_mass(M_*) of that solve's stellar mass "
      "to 1e-12 -- passes in the main run and FAILS under MUTATE by construction (ratio 100); it guarantees rc = 1 and a failing set "
      "different from the main run's, and says nothing about whether the science responds",
      f"max |M_h entering / halo_mass(M_*) - 1| = {wdev:.1e} over {nw} solves" + TAG, wdev <= 1e-12)

# ================================================================================================ H1
R.banner("H1  THE HEADLINE: CFG33's gate applied to the LCDM halo, through the identical pipeline" + TAG)
h1a, h1b = sb["n_lens"] >= NL_MIN, sb["n_cal"] >= ND_MIN
h1c = bool(np.isfinite(sb["z"]) and abs(sb["z"]) <= 2)
check(f"H1 [HEADLINE] LCDM PASSES CFG33's GATE through the identical pipeline: H1a >= {NL_MIN} of {NL} lenses solved; H1b >= {ND_MIN} of {NQ} "
      "calibration galaxies calibrated; H1c |Delta_LCDM| <= 2 sigma_tot (bootstrap + the 0.10-dex floor)" + TAG,
      f"H1a {sb['n_lens']}/{NL} ({'pass' if h1a else 'FAIL'}); H1b {sb['n_cal']}/{NQ} ({'pass' if h1b else 'FAIL'}); H1c Delta {sb['delta']:+.3f} +- "
      f"{sb['tot']:.3f} dex -> {sb['z']:+.2f} sigma ({'pass' if h1c else 'FAIL'}); outcome {sb['outcome']}",
      h1a and h1b and h1c)

# ================================================================================================ C6 / R6
R.banner("C6 / R6  DOES THE GATE SEE THE HALO?  the outcome with every M_h x 1 against x 100 (both computed in-process)")
S1, S100 = (sb, SC_OTHER) if not MUTATE else (SC_OTHER, sb)
same = S1["outcome"] == S100["outcome"]
mj = ""
if MUTATE:
    pj = os.path.join(HERE, "CFG80_lcdm_slacs_results.json")
    if os.path.exists(pj):
        o_main = json.load(open(pj))["numbers"].get("lcdm_x1", {}).get("outcome")
        mj = f"; the main run's committed JSON says x 1 -> {o_main} ({'consistent' if o_main == S1['outcome'] else 'INCONSISTENT'} with the in-process x 1)"
    else:
        mj = "; the main run's JSON was not found (the in-process x 1 is used)"
check("C6 (load-bearing in the MUTATE run only; R6 in the main run) the LCDM gate outcome changes when every M_h is multiplied by 100; "
      "unchanged -> NON-DISCRIMINATING",
      f"x 1: {S1['outcome']} (Delta {S1['delta']:+.3f}, {S1['z']:+.2f} sigma); x 100: {S100['outcome']} (Delta {S100['delta']:+.3f}, {S100['z']:+.2f} sigma, "
      f"{S100['n_lens']}/{NL} lenses, {S100['n_cal']}/{NQ} calibrated); Delta moves {S100['delta'] - S1['delta']:+.3f} dex -> "
      + ("UNCHANGED: NON-DISCRIMINATING" if same else "changed: the gate sees the halo mass") + mj,
      (not same) if MUTATE else True, load_bearing=MUTATE)

# ================================================================================================ the classification (reported)
R.banner("THE CLASSIFICATION (reported): the declared model (x 1), with the x 100 test")
per_cell = {f"{f}|{b}": cls_of(S1["z"], S1["delta"], v["delta"], S1["outcome"]) for (f, b), v in RES33.items()}
cset = sorted(set(per_cell.values()))
cls3 = cset[0] if len(cset) == 1 else "MIXED"
final = "NON-DISCRIMINATING" if same else cls3
check("CLASS (reported) B's gap under CFG69's classes (floor-inclusive z; B's sign +): SPECIFIC-TO-B / SHARED / LCDM-WORSE, overridden by "
      "NON-DISCRIMINATING if the x 100 outcome is unchanged",
      "B (CFG33): " + "; ".join(f"{f} {b} {v['delta']:+.3f} ({v['z']:+.2f} / {v['z_nofloor']:+.1f} stat)" for (f, b), v in RES33.items())
      + f" | LCDM x 1 (both footings, V = I): {S1['delta']:+.3f} ({S1['z']:+.2f} / {S1['z_stat']:+.1f} stat), outcome {S1['outcome']} -> three-way "
      f"{cls3}; x 100 outcome {S100['outcome']} -> FINAL: {final}", True, load_bearing=False)

# ================================================================================================ R1-R7 (reported)
R.banner("R1-R7  REPORTED" + TAG)
cls_stat = {f"{f}|{b}": (("SPECIFIC-TO-B" if abs(sb["z_stat"]) <= 2 else ("SHARED" if np.sign(sb["delta"]) == np.sign(v["delta"]) else "LCDM-WORSE"))
                         if np.isfinite(sb["z_stat"]) else "UNFIT") for (f, b), v in RES33.items()}
check("R1 (reported) LCDM's statistical-only z and the class it would give (NOT the classification)",
      f"Delta {sb['delta']:+.3f} +- {sb['err']:.3f} (stat) -> {sb['z_stat']:+.1f} sigma; class under the statistical z: "
      + ", ".join(sorted(set(cls_stat.values()))), True, load_bearing=False)

LS, DS = sb["lset"], sb["dset"]
R2 = {}
if len(LS) >= 3 and len(DS) >= 3:
    for (f, b), v in RES33.items():
        alB, adB = LENS[(f, b)][1], DYN[f]
        rng = np.random.default_rng(33); dif = np.empty(2000)
        for k in range(2000):
            il = LS[rng.integers(0, len(LS), len(LS))]; idd = rng.choice(DS, len(DS))
            dif[k] = gstat(alB, adB, il, idd)[0] - gstat(base["al"], base["ad"], il, idd)[0]
        pt = gstat(alB, adB, LS, DS)[0] - gstat(base["al"], base["ad"], LS, DS)[0]
        R2[f"{f}|{b}"] = dict(diff=pt, err=float(np.std(dif)))
check("R2 (reported) B minus LCDM per B cell (dex), paired bootstrap (the same 2000 resamples for both models; statistical only -- the "
      "floor's zero-point shift moves both alphas almost equally and is not added)",
      "; ".join(f"{k.replace('|', ' ')} {v['diff']:+.3f} +- {v['err']:.3f} ({v['diff'] / v['err']:+.1f} sigma)" for k, v in R2.items()) or "not scorable",
      True, load_bearing=False)

VAR = {}
for k in ("V1", "V2", "V3", "V4"):
    v = SC[k]
    VAR[k] = dict(pub(v), cls=cls_of(v["z"], v["delta"], RES33[("canonical", "V")]["delta"], v["outcome"]))
check("R3 (reported) the declared variants (not tuned): V1 Dutton-Maccio c; V2 Duffy relaxed 200c; V3 / V4 every M_h x 1/3 and x 3",
      "; ".join(f"{k}: Delta {v['delta']:+.3f} +- {v['err']:.3f} -> {v['z']:+.2f} sigma ({v['z_stat']:+.1f} stat), {v['n_lens']}/{NL} lenses, "
                f"{v['n_cal']}/{NQ} calibrated, outcome {v['outcome']} ({v['cls']})" for k, v in VAR.items()), True, load_bearing=False)

bins = [(2.20, 2.35), (2.35, 2.45), (2.45, 2.60)]
rows = []
for lo, hi in bins:
    ml = (LSIG_L >= lo) & (LSIG_L < hi) & np.isfinite(base["al"]); md = Q & np.isfinite(base["ad"]) & (LSIG_A >= lo) & (LSIG_A < hi)
    rows.append(f"log sigma {lo:.2f}-{hi:.2f}: lenses {int(ml.sum())} x{10 ** np.median(np.log10(base['al'][ml])):.2f}, ATLAS3D {int(md.sum())} "
                f"x{10 ** np.median(np.log10(base['ad'][md])):.2f}" if ml.sum() and md.sum() else f"log sigma {lo:.2f}-{hi:.2f}: too few")
lslope = float(np.polyfit(LSIG_L[LS] - PIV, np.log10(base["al"][LS]), 1)[0]) if len(LS) >= 3 else NaN
lslope_B = float(np.polyfit(LSIG_L - PIV, np.log10(LENS[("canonical", "V")][1]), 1)[0])
check("R4 (reported) LCDM's alpha_lens and alpha_dyn in CFG33's dispersion bins; LCDM's dynamics slope (CFG33 H3's analogue) and the lenses' slope",
      "; ".join(rows) + f"; d log alpha_dyn / d log sigma_e {sb['slope']:+.3f} +- {sb['slope_err']:.3f} ({sb['slope'] / sb['slope_err']:+.1f} sigma; B canonical: "
      f"{g33['sl0']:+.3f} +- {float(np.std(g33['sl'])):.3f}); lens slope {lslope:+.2f} (B canonical V: {lslope_B:+.2f})", True, load_bearing=False)

cb = CFGS["base"]
mh_l = np.array([cb["halo"](base["Ml"][i]) * cb["hmf"] for i in LS])
fdm_l = np.array([(1 - FB) * cb["proj"](cb["halo"](base["Ml"][i]) * cb["hmf"], S[i]["RE"]) / S[i]["ME"] for i in LS])
mh_d = np.array([cb["halo"](base["Md"][j]) * cb["hmf"] for j in DS])
fdm_d = np.array([(1 - FB) * float(cb["prof"](cb["halo"](base["Md"][j]) * cb["hmf"], ET[j]["r12"])) / (ET[j]["Mjam"] / 2) for j in DS])
n_clamp_l = int(np.sum(base["Ml"][LS] > 10 ** LMS_TOP)); n_clamp_d = int(np.sum(base["Md"][DS] > 10 ** LMS_TOP))
n_clip = int(sum(ET[j]["r12"] < 1e-4 * r200_of(m_) for j, m_ in zip(DS, mh_d)))
ex_l = [i for i in range(NL) if not np.isfinite(base["Ml"][i])]
ex_d = [j for j in np.where(Q)[0] if not np.isfinite(base["Md"][j])]
ex_l_over = sum(lens_kappa(S[i], cb, 1e8) > 1 for i in ex_l)
ex_d_over = sum(jam_model(ET[j], cb, 1e8) > ET[j]["Mjam"] / 2 for j in ex_d)
R5 = dict(med_lMh_lens=float(np.median(np.log10(mh_l))) if len(mh_l) else NaN, med_fdm_RE=float(np.median(fdm_l)) if len(fdm_l) else NaN,
          med_lMh_cal=float(np.median(np.log10(mh_d))) if len(mh_d) else NaN, med_fdm_r12=float(np.median(fdm_d)) if len(fdm_d) else NaN,
          n_clamp_lens=n_clamp_l, n_clamp_cal=n_clamp_d, n_inner_clip=n_clip, excluded_lens=len(ex_l), excluded_lens_overshoot=int(ex_l_over),
          excluded_cal=len(ex_d), excluded_cal_overshoot=int(ex_d_over), lMh_lens_range=[float(np.log10(mh_l.min())), float(np.log10(mh_l.max()))] if len(mh_l) else None)
check("R5 (reported) diagnostics at the base solution: halo masses, dark fractions, the Moster-grid clamp, make_nfw's inner clip, exclusions",
      f"median log M_h: lenses {R5['med_lMh_lens']:.2f} (range {R5['lMh_lens_range'][0]:.2f}-{R5['lMh_lens_range'][1]:.2f}), calibration set "
      f"{R5['med_lMh_cal']:.2f}; median projected dark fraction inside R_E {R5['med_fdm_RE']:.2f}; median 3D dark fraction inside r_1/2 {R5['med_fdm_r12']:.2f}; "
      f"stellar masses above the Moster grid (M_* > 10^{LMS_TOP:.2f}, M_h clamped): {n_clamp_l} lenses, {n_clamp_d} calibration galaxies; make_nfw's inner "
      f"clip active at {n_clip} calibration galaxies; excluded: {len(ex_l)} lenses ({ex_l_over} halo-overshoot), {len(ex_d)} calibration galaxies ({ex_d_over} "
      f"halo-overshoot)" if len(mh_l) and len(mh_d) else "not scorable", True, load_bearing=False)


def beyond(Mh, R_kpc, cfn, T=5.0):
    """the untruncated NFW's mass beyond T R_200 that projects inside R (what make_nfw's saturation at 5 R_200 removes)."""
    c = float(cfn(Mh)); X = c * R_kpc / r200_of(Mh)
    I_c = integrate.quad(f3, 0.0, c, **QK)[0]
    wf = lambda t: f3(t) * (X * X / (t * t)) / (1.0 + math.sqrt(1.0 - X * X / (t * t)))
    return Mh * integrate.quad(wf, c * T, np.inf, epsabs=0.0, epsrel=1e-10, limit=400)[0] / I_c


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    rel7, dk7 = [], []
    for i in LS:
        Mh_ = cb["halo"](base["Ml"][i]) * cb["hmf"]
        bm = beyond(Mh_, S[i]["RE"], cb["cfn"])
        rel7.append(bm / cb["proj"](Mh_, S[i]["RE"])); dk7.append((1 - FB) * bm / S[i]["ME"])
check("R7 (reported) the projected halo with the line of sight saturated at 5 R_200 (make_nfw's outer clip) against the untruncated analytic "
      "form, at each lens's R_E and base solution",
      f"max relative difference in the halo's M_2D {max(rel7):.1e}; max |Delta kappa_bar| {max(dk7):.1e}" if rel7 else "not scorable",
      True, load_bearing=False)

READINGS = {
    "SPECIFIC-TO-B": "a standard NFW halo shows no lensing-dynamics gap at > 2 sigma (with the floor) through CFG33's pipeline; B's statistical "
                     "gap is a property of B's law (its projected phantom at R_E is small next to what the law supplies inside r_1/2), not of the "
                     "pipeline, the two surveys' zero points, the aperture or the redshift difference.  B itself is within 2 sigma with the floor, so "
                     "this is a statement about the statistical gap; R1 and R2 say how much of it LCDM shares",
    "SHARED": "a standard halo shows the same-sign gap: it is generic to the pipeline and data (zero points, apertures, a local calibration set "
              "against lenses at z ~ 0.2), and B7's residual is not evidence against B specifically",
    "LCDM-WORSE": "in this pipeline a standard halo's lenses need less stellar mass than its dynamics at the same dispersion, at > 2 sigma; B's gap "
                  "has the opposite sign; R2 gives the difference",
    "NON-DISCRIMINATING": "the gate cannot tell the Moster halo from one 100 times heavier, so in this pipeline it carries no information about the "
                          "dark halo; the three-way reading is reported but not used",
    "UNFIT": "the declared LCDM model cannot be run through the pipeline for most systems; no class",
    "MIXED": "the four B cells give different classes (not expected: LCDM is one number and B's sign is the same in every cell)",
}
P(f"\n    READING (declared; the declared model at x 1): {final} -- {READINGS[final]}")
if MUTATE:
    P(f"    (this MUTATE run scored H1 on every M_h x 100: outcome {sb['outcome']}; C6 {'passes' if not same else 'FAILS'}: the control is "
      + ("informative for the headline" if not same else "uninformative for the headline (only the C5 witness fails by construction)") + ")")

R.num("B_cfg33", {f"{f}|{b}": v for (f, b), v in RES33.items()})
R.num("C1", dict(lines_ok=lines_ok, json_dev=jdev, generic_dev=gdev))
R.num("C2", dict(dev_r200=dev_r200, monotone=mono, verbatim=same_src, rho_c=RHO_C, dev_rho=dev_rho))
R.num("C3", dict(n=npts, dev_shells=dev_sh, dev_los=dev_los, X_range=[min(Xs), max(Xs)]))
R.num("C4", dict(res_lens=res_l, res_jam=res_d, zero_all=z_all, zero_dev_lens=dz_l, zero_dev_jam=dz_d, adds=adds))
R.num("C5_witness", dict(dev=wdev, n=nw, hmut=HMUT))
R.num("lcdm_this_run", {k: dict(pub(v), hmf=CFGS[k]["hmf"]) for k, v in SC.items()})
R.num("lcdm_other", dict(pub(SC_OTHER), hmf=HOTHER))
R.num("lcdm_x1", pub(S1)); R.num("lcdm_x100", pub(S100))
R.num("class", dict(per_cell=per_cell, three_way=cls3, x100_unchanged=same, final=final, stat_only=cls_stat))
R.num("R2_B_minus_LCDM", R2); R.num("R3_variants", VAR); R.num("R4", dict(bins=rows, lens_slope=lslope, lens_slope_B=lslope_B))
R.num("R5", R5); R.num("R7", dict(max_rel=max(rel7) if rel7 else None, max_dkappa=max(dk7) if dk7 else None))
R.num("per_object_base", dict(lens=[dict(name=S[i]["name"], alpha_lens=base["al"][i], sig=S[i]["sig"]) for i in range(NL)],
                               atlas3d=[dict(name=ET[j]["name"], alpha_dyn=base["ad"][j], q=bool(Q[j])) for j in range(len(ET))]))
R.num("reading", dict(final=final, text=READINGS[final]))
nf = R.write()
sys.exit(1 if nf else 0)
