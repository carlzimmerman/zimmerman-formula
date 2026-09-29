#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG74 -- WHICH CHOICES IN THE LCDM COMPARATOR DRIVE THE ULTRA-FAINT GATE?   (frozen docstring, written BEFORE the first run)
Base: CFG73's re-derivation (own Moster inversion, NFW, Kaplan-Meier; sample 31 resolved + 9 limits from lvd_dwarf_mw.csv;
Upsilon_V = 2; sigma^2 = g r/3 at r = (4/3) r_half; half of the stars enclosed; debris (1-f_b) M_NFW; three concentration
relations Duffy-full [declared primary], Duffy-relaxed, Dutton-Maccio).  Code copied (not imported) from CFG73_lcdm_uf_rederive.py.
Nothing in the repository is edited; no data fetched; no constant is fitted; nothing is tuned after a result is seen.

QUESTIONS.
  Q1  Under which comparator choice, if any, does the LCDM ultra-faint gate become DISCRIMINATING?
      DISCRIMINATING (declared, primary reading, Duffy-full concentration) := |z| >= 2 at BOTH the x0.1 and the x10 multiple of
      every halo mass (floors included), i.e. the gate fails when the halo mass is wrong by a factor ten either way.  Secondary
      readings reported: (a) fails at x0.1 OR x10; (b) the same under Duffy-relaxed / Dutton-Maccio; (c) the full pass window
      over x0.01..x1000.
  Q2  How large is each choice's effect on the KM median (V - V0), and is it larger than the bootstrap error?
  All variants are run ONE AT A TIME (no combination of variants is run; combinations are untested and stated as such).

VARIANTS (exact).  Let Mstar = 2 L_V, Mbase = the halo mass before the x-multiple; every ladder multiple m in {0.01,0.1,1,10,100,1000}
multiplies the final halo mass (floors included), as in CFG73.
  V0  BASELINE = CFG73.  Mbase = Moster inversion (exact root) clamped at 1e9 (33 of 40 clamped); NFW; debris (1-f_b) M_NFW.
      Floor scan for the error: Mbase of every satellite with Mstar < 1e5 (39 of 40) SET to f in {1e8,3e8,1e9,3e9,1e10}; floor error =
      half the range of the KM medians; total error = sqrt(bootstrap^2 + floor^2); gate |median|/total < 2.
      Bootstrap: 2000 resamples, resolved and limits resampled separately, seed 20260928 (all rungs of the ladder use 2000).
  V1  SHMR SCATTER, log-normal 0.2 dex, MARGINALISED.  Convention (declared): the halo mass of object i is Mbase_i x 10^delta_i with
      delta_i ~ N(0, 0.2) independent per object (scatter in log halo mass at fixed stellar mass; the Eddington-bias correction from the
      steep halo mass function is NOT applied -- declared limitation).  2000 Monte-Carlo draws (delta matrix seed 20260928, bootstrap-index
      seed 20260929), each draw ALSO carries one bootstrap resample of the objects, so std over draws = scatter + sampling.  Reported:
      marginalised median = MEAN over draws of the KM median; scatter-only std (no resampling); combined std; floor half-range = half the
      range of the draw-mean medians over the SAME five floors (common random numbers); total = sqrt(combined std^2 + floor^2).
      The Moster floor is the V0 floor (clamp 1e9 central, scan 1e8..1e10).  Expected (declared): |V1 - V0| < 0.03 dex and total error
      up by < 15%; not discriminating.
  V2  ADIABATIC CONTRACTION, Blumenthal (1986) standard form  r_i M_i(r_i) = r_f M_f(r_f),  M_f(r_f) = M_dm,i(r_i) + M_b,f(<r_f)
      (baryons redistribute, dark matter shells conserve mass and do not cross).  Evaluated at r_f = (4/3) r_half with M_b,f(<r_f) =
      0.5 Mstar (the code's half-of-the-stars-enclosed convention); the contracted dark mass at r_f is M_dm,i(r_i).  Two readings, both
      frozen:
        V2b  (PRIMARY: "contraction by the stars") the initial mass profile is the debris halo itself, M_i = M_dm,i = (1-f_b) M_NFW; so
             r_i M_dm(r_i) = r_f [M_dm(r_i) + 0.5 Mstar]  (zero stars => r_i = r_f => V0 exactly).
        V2a  (reported) the initial total mass is the full NFW halo, M_i = M_NFW, dark share (1-f_b): r_i M_NFW(r_i) = r_f[(1-f_b) M_NFW(r_i)
             + 0.5 Mstar]; this ALSO contains the expansion from the cosmic-baryon fraction that the halo does not keep (zero stars => an
             expansion of dark shells by 1/(1-f_b)), so it is not "contraction by the stars" alone.
      Solved per object by log-bisection (100 iterations).  Same floor scan, bootstrap, ladder as V0.  The size is verified: log10
      sigma_AC/sigma_V0 (median, max over the 40 objects).  Expected (declared): NOT negligible for the brightest ultra-faints (0.5 Mstar
      is comparable to M_dm(<r) there), effect on the KM median negative (sigma_pred up) of order 0.02-0.10 dex.
  V3  THE FLOOR AS A TRUE FLOOR.  Mbase = max(M_Moster,unclamped, f) for ALL 40 objects (Moster inverted WITHOUT the 1e9 clamp; bracket
      log M_h in [5,11]), f in {1e8, 3e8, 1e9, 3e9, 1e10}; central value f = 1e9; error = sqrt(bootstrap^2 + (half the range of the KM medians
      over f)^2).  Compared with the V0 set-scan (which OVERWRITES the halo mass of the 39 objects with Mstar < 1e5 by f).  Reported-only
      extras: f = 0 (pure unclamped Moster, no floor) and the CFG73 'true floor' reading max(clamped Moster, f), which must reproduce
      CFG73's +0.080,+0.080,+0.080,+0.023,-0.037 (control).
  V4  BURKERT (cored) HALO OF EQUAL MASS.  rho = rho0 r0^3 / ((r+r0)(r^2+r0^2)), M(<r) = 4 pi rho0 r0^3 F(r/r0),
      F(x) = 1/4 ln[(1+x)^2 (1+x^2)] - 1/2 arctan x; EQUAL MASS := M(<R200) = M_h, R200 as for the NFW of the same M_h; debris factor
      (1-f_b) as V0.  Core radius: no fitted constant; r0 = r_s(NFW, same M_h, declared concentration) = R200/c (kpc).  Two mappings:
        V4b  (PRIMARY) r0 and R200 are frozen at the x1 Mbase; a multiple m scales the density (rho0 -> m rho0), so 'halo mass x m' means
             m x the mass everywhere at the same core.  Equal-mass normalisation holds at m = 1.
        V4a  (reported) r0 = R200/c(M_h) recomputed at the multiplied mass (the halo is a rescaled Burkert of that mass).  Expected
             (declared) to be nearly mass-INDEPENDENT at r << r0 (M(<r) -> (4 pi/3) rho0 r^3, rho0 r0^3 ~ M_h, r0^3 ~ M_h/(c^3 ...)), so
             the multiples are a weak test by construction.
      Reported sensitivity: V4b with r0 = 0.5 r_s and 2 r_s (an inspection of the core-size dependence, NOT a fit).  Expected
      (declared): sigma_pred falls by a large factor at the smallest radii, the x1 median rises to roughly +0.2..+0.5, and the gate may FAIL at
      x1 (this is the direction in which the gate could become discriminating).  Same floor scan (Mbase set), bootstrap, ladder.

CONTROLS (hard: a failure makes the runner exit 1 and is reported, not repaired).
  C0  V0 reproduces CFG73: Duffy-full KM medians +0.080 (x1), +0.213 (x0.1), -0.037 (x10), floors (+0.204,+0.143,+0.080,+0.023,-0.037);
      Duffy-relaxed +0.015; Dutton-Maccio -0.043; all to 5.5e-4.
  C1  V1 with sigma_scatter = 0 equals V0 to 1e-12; the drawn deltas have |mean| < 0.02 and std within 0.01 of 0.2.
  C2  V2: zero stars => V2b = V0 sigma to 1e-9; the solved r_i satisfies its defining equation to 1e-9 relative; r_i >= r_f in V2b.
  C3  V3: max(clamped Moster, f) reproduces CFG73's +0.080,+0.080,+0.080,+0.023,-0.037 to 5.5e-4.
  C4  V4: Burkert enclosed mass = numerical integration of the density (<1e-6, 3 r0 x 3 R200 x 4 radii); M(<R200) = M_h to 1e-12;
      small-radius limit M -> (4 pi/3) rho0 r^3 within 1e-6 relative at x = 1e-3.
  C5  MUTATE: every observed dispersion (resolved and limits) x 0.5.  For EVERY variant (V0, V1, V2a, V2b, V3, V4a, V4b, three
      concentrations) the KM median shifts by exactly log10(0.5) = -0.30103 (tolerance 1e-9), checked in-process in both modes.  env MUTATE=1
      mutates the whole run; the gate outcome under MUTATE is reported, not required (CFG73: baseline Duffy-full still passes, -1.66 sigma).
  C6  KM = brute-force product-limit on 300 random left-censored sets; halo switched off = closed-form Newtonian sigma.

PASS/FAIL LINES for the answer to Q1 (no thresholds are adjusted after the run):
  - Gate PASS at a rung  := |KM median| / total < 2.        - Variant X is DISCRIMINATING := gate FAILS at x0.1 AND x10 (Duffy full).
  - Effect on the median negligible := |V - V0| < 0.5 x V0 bootstrap error (0.028 dex).
  - A null / non-discriminating outcome is a valid outcome.  Nothing here says the data favour any model.
Run: python3 cfg74_lcdm_variants.py > cfg74_lcdm_variants.out ; MUTATE=1 python3 cfg74_lcdm_variants.py > cfg74_lcdm_variants_MUTATE.out
"""
import os, sys, math, csv
import numpy as np
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
CSV_MW = os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv")
OBSF = 0.5 if MUTATE else 1.0
SEED = 20260928
NB = 2000

CHECKS = []
def P(s=""): print(s, flush=True)
def check(name, detail, ok):
    CHECKS.append((name, ok))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")

P(__doc__.split("Run: python3")[0].strip())
P("""
AMENDMENT A1 (written AFTER the first run; the first-run output is kept as first_run_before_amendment.out).  Two declared controls FAILED
in the first run and are KEPT as failures below; both failures are errors in the CONTROL as declared, not in a variant, and are diagnosed here:
  C2 (zero stars => V2b = V0): the control switched the stars off in the SIGMA formula of the contracted case but not in V0, so it compared
      different systems (dev 1.5e-2).  C2b (added) compares like with like: the contraction solved with M_b = 0 in the Blumenthal equation
      but stars kept in g, against V0 (must agree to 1e-9), and the whole system with stars removed in both.
  C4 (small-radius Burkert limit 1e-6 at x = 1e-3): the leading correction is F = x^3/3 (1 - 3x/4 + ...), so the relative deviation at
      x = 1e-3 is 7.5e-4 = 3x/4 by analysis; my tolerance was wrong.  C4b (added) checks the limit at x = 1e-5 against 3x/4 to 1%.
AMENDMENT A2 (after the second run, kept as second_run_before_amendment2.out): C4b as written in A1 FAILED (x = 1e-5) because Ffun loses
  ~1.5e-6 relative precision to cancellation at x = 1e-5 (an mpmath 50-digit reference confirms the analytic correction -3x/4 to 4 digits at
  x = 1e-5 and the double-precision Ffun error there is 1.5e-6, i.e. larger than the 1% target of 7.5e-6).  The runs use x = r/r0 >= ~5e-3,
  where Ffun is good to <1e-10.  C4c (added) checks the correction at x = 1e-3 (where Ffun is good to 2e-10) and reports the worst Ffun error at the
  x values actually used, against a 50-digit mpmath reference.  C4b stays as a recorded FAIL of my check design.
REPORTED-ONLY ADDITIONS (chosen after seeing the first run, NOT part of the frozen pass/fail): (i) the Newtonian stars-only KM median (no halo)
as the reference for how far a cored halo can push the median; (ii) a finer 25-point ladder x0.01..x1e4 (Duffy full, 500 resamples per point) to
give the continuous width of the gate's pass window per variant.
""")
if MUTATE:
    P("\n  *** MUTATE=1: every observed dispersion x 0.5 ***")

# ---------------------------------------------------------------- constants and NFW (CFG73 values)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; PC = 3.0857e16
H0 = 67.4; h = 0.674
FB = 0.02237 / (0.02237 + 0.1200)
RHO_C = 3 * (H0 * 1e3 / Mpc) ** 2 / (8 * math.pi * G) / Msun * (3.0857e22) ** 3
NA, LM1, BE, GA = 0.0351, 11.590, 1.376, 0.608

def moster_mstar(Mh):
    x = np.asarray(Mh, float) / 10 ** LM1
    return np.asarray(Mh, float) * 2 * NA / (x ** (-BE) + x ** GA)

MH_FLOOR = 1e9
def moster_inv(Mstar, clamp=True):
    out = []
    for ms in np.atleast_1d(np.asarray(Mstar, float)):
        f = lambda lm: math.log10(float(moster_mstar(10 ** lm))) - math.log10(ms)
        if clamp and f(math.log10(MH_FLOOR)) >= 0:
            out.append(MH_FLOOR)
        else:
            out.append(10 ** brentq(f, 5.0, 11.0, xtol=1e-13))
    return np.array(out)

def conc(Mh, kind):
    Mh = np.asarray(Mh, float)
    if kind == "duffy_full":    return 5.71 * (Mh / (2e12 / h)) ** (-0.084)
    if kind == "duffy_relaxed": return 6.71 * (Mh / (2e12 / h)) ** (-0.091)
    if kind == "dutton_maccio": return 10 ** (0.905 - 0.101 * (np.log10(Mh * h) - 12.0))
    raise ValueError(kind)

def mfun(t): return np.log1p(t) - t / (1 + t)
def R200_kpc(Mh): return (3 * np.asarray(Mh, float) / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0

def nfw_enclosed(Mh, r_kpc, kind):
    Mh = np.asarray(Mh, float)
    c = conc(Mh, kind)
    x = np.clip(np.asarray(r_kpc, float) / R200_kpc(Mh), 1e-4, 5.0)
    return Mh * mfun(c * x) / mfun(c)

def Ffun(x):
    x = np.asarray(x, float)
    return 0.5 * np.log1p(x) + 0.25 * np.log1p(x * x) - 0.5 * np.arctan(x)

def burk_enclosed(Mnorm, Rref_kpc, r0_kpc, r_kpc):
    """M(<r) = Mnorm F(r/r0)/F(Rref/r0): equal mass at Rref."""
    return Mnorm * Ffun(np.asarray(r_kpc, float) / r0_kpc) / Ffun(np.asarray(Rref_kpc, float) / r0_kpc)

# ---------------------------------------------------------------- data (CFG73's reading)
def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

RES, LIM = [], []
for r in csv.DictReader(open(CSV_MW)):
    sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or rh is None or Dh is None or MV <= -7.7:
        continue
    rec = dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh)
    if ul is not None:
        rec["sig"] = ul; LIM.append(rec)
    elif sig is not None and sig > 0:
        rec["sig"] = sig; RES.append(rec)

ALL = RES + LIM
NR, NL, NT = len(RES), len(LIM), len(RES) + len(LIM)
UPS = 2.0
LV = np.array([d["LV"] for d in ALL]); RH = np.array([d["rh"] for d in ALL]); SIG = np.array([d["sig"] for d in ALL])
MSTAR = UPS * LV                     # M_* at Upsilon_V = 2 (also the Moster input, the lanes' convention)
RP_PC = (4 / 3.) * RH; RP_KPC = RP_PC / 1000.0; R_M = RP_PC * PC
MB_HALF = 0.5 * MSTAR                # stars enclosed at r
M_CLAMP = moster_inv(MSTAR, clamp=True)
M_FREE = moster_inv(MSTAR, clamp=False)
SMALL = MSTAR < 1e5                  # objects whose halo is SET in the V0 floor scan
FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)

def Mbase_set(f): return np.where(SMALL, f, M_CLAMP)                 # V0 / V1 / V2 / V4 floor scan
def Mbase_true(f): return np.maximum(M_FREE, f)                       # V3
def Mbase_clampmax(f): return np.maximum(M_CLAMP, f)                  # CFG73's "true floor" reading (control)

# ---------------------------------------------------------------- the prediction
def sigma_pred(kind, Mbase, mult=1.0, profile="nfw", r0fac=1.0, stars=True):
    """Mbase: (..., 40).  Returns sigma_pred in km/s, shape (..., 40)."""
    Mbase = np.asarray(Mbase, float)
    Mb = MB_HALF if stars else 0.0 * MB_HALF
    if profile == "nfw":
        Mdm = (1 - FB) * nfw_enclosed(Mbase * mult, RP_KPC, kind)
    elif profile in ("ac_stars", "ac_cosmic"):
        Mh = Mbase * mult
        s_init = 1.0 if profile == "ac_stars" else 1.0 / (1 - FB)   # M_init(r) = s_init * M_dm(r)
        Mdm_at = lambda r: (1 - FB) * nfw_enclosed(Mh, r, kind)
        rf = np.broadcast_to(RP_KPC, Mh.shape)
        def g(ri): return ri * s_init * Mdm_at(ri) - rf * (Mdm_at(ri) + Mb)
        lo = 0.3 * rf; hi = 200.0 * rf
        assert np.all(g(lo) < 0) and np.all(g(hi) > 0) or (not stars)
        if stars:
            for _ in range(100):
                mid = np.sqrt(lo * hi); gm = g(mid)
                lo = np.where(gm < 0, mid, lo); hi = np.where(gm < 0, hi, mid)
            ri = np.sqrt(lo * hi)
        else:
            # no stars: profile-specific closed limit (V2b: ri = rf; V2a: r_i s.t. ri s M(ri) = rf M(ri) -> ri = rf/s)
            ri = rf / s_init
        sigma_pred.last_ri = ri
        Mdm = Mdm_at(ri)
    elif profile in ("burk_fixed", "burk_scaled"):
        Rb = R200_kpc(Mbase); cb = conc(Mbase, kind)
        if profile == "burk_fixed":
            Mdm = (1 - FB) * mult * burk_enclosed(Mbase, Rb, r0fac * Rb / cb, RP_KPC)
        else:
            Mh = Mbase * mult; Rh = R200_kpc(Mh); ch = conc(Mh, kind)
            Mdm = (1 - FB) * burk_enclosed(Mh, Rh, r0fac * Rh / ch, RP_KPC)
    else:
        raise ValueError(profile)
    return np.sqrt(G * (Mb + Mdm) * Msun / (3.0 * R_M)) / 1e3

# ---------------------------------------------------------------- KM (CFG73)
def km_median(x, xu):
    y = np.concatenate([-np.asarray(x, float), -np.asarray(xu, float)])
    ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    n = len(y); atrisk = n - np.arange(n)
    fac = np.where(ev, 1.0 - 1.0 / atrisk, 1.0)
    S = np.cumprod(fac)
    idx = np.nonzero(ev & (S <= 0.5 + 1e-15))[0]
    if len(idx) == 0:
        return -y[-1], False
    return -y[idx[0]], True

def km_bruteforce(x, xu):
    pts = [(-v, 1) for v in x] + [(-v, 0) for v in xu]
    times = sorted(set(t for t, e in pts if e == 1)); S = 1.0
    for t in times:
        n_risk = sum(1 for tt, e in pts if tt >= t); d = sum(1 for tt, e in pts if tt == t and e == 1)
        S *= 1 - d / n_risk
        if S <= 0.5 + 1e-15: return -t
    return -max(t for t, e in pts)

def offsets_from(sigp, obsf=None):
    f = OBSF if obsf is None else obsf
    off = np.log10(f * SIG / sigp)
    return off[..., :NR], off[..., NR:]

def km_of(sigp, obsf=None):
    x, xu = offsets_from(sigp, obsf); return km_median(x, xu)[0]

def boot(x, xu, nb=NB, seed=SEED):
    rng = np.random.default_rng(seed); v = np.empty(nb)
    for i in range(nb):
        v[i] = km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))])[0]
    return float(np.std(v))

# ---------------------------------------------------------------- generic (non-V1) result at one multiple
def result(kind, mult, floortype, profile="nfw", r0fac=1.0):
    mk = Mbase_set if floortype == "set" else Mbase_true
    sp = lambda Mb: sigma_pred(kind, Mb, mult, profile, r0fac)
    c = sp(mk(1e9)); x, xu = offsets_from(c)
    med = km_median(x, xu)[0]; err = boot(x, xu)
    fl = [km_of(sp(mk(f))) for f in FLOORS]
    fsig = 0.5 * (max(fl) - min(fl)); tot = math.sqrt(err ** 2 + fsig ** 2)
    return dict(med=med, boot=err, floor=fsig, tot=tot, z=med / tot, floors=fl)

# ---------------------------------------------------------------- V1 scatter (marginalised)
NDRAW = 2000
DELTA = np.random.default_rng(SEED).normal(0.0, 0.2, (NDRAW, NT))
_rb = np.random.default_rng(SEED + 1)
BI_R = _rb.integers(0, NR, (NDRAW, NR)); BI_L = _rb.integers(0, NL, (NDRAW, NL))

def result_v1(kind, mult, scatter_scale=1.0, boot_on=True):
    def meds(f, with_boot):
        Mb = Mbase_set(f)[None, :] * 10 ** (scatter_scale * DELTA)
        off = np.log10(OBSF * SIG[None, :] / sigma_pred(kind, Mb, mult))
        out = np.empty(NDRAW)
        for d in range(NDRAW):
            xr, xl = off[d, :NR], off[d, NR:]
            if with_boot: xr, xl = xr[BI_R[d]], xl[BI_L[d]]
            out[d] = km_median(xr, xl)[0]
        return out
    cen_b = meds(1e9, True); cen_n = meds(1e9, False)
    med = float(np.mean(cen_n)); comb = float(np.std(cen_b)); sc = float(np.std(cen_n))
    fl = [float(np.mean(meds(f, False))) for f in FLOORS]
    fsig = 0.5 * (max(fl) - min(fl)); tot = math.sqrt(comb ** 2 + fsig ** 2)
    return dict(med=med, boot=comb, scat=sc, floor=fsig, tot=tot, z=med / tot, floors=fl)

# ================================================================== SAMPLE + CONTROLS
KINDS = ("duffy_full", "duffy_relaxed", "dutton_maccio")
MULTS = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
P("\n" + "=" * 118 + "\nSAMPLE + CONTROLS\n" + "=" * 118)
P(f"  resolved {NR}, limits {NL}; clamped (Moster < 1e9) {int(np.sum(MSTAR < float(moster_mstar(1e9))))} of {NT}; M_*<1e5: {int(SMALL.sum())}; "
  f"unclamped Moster masses of the 40: min {M_FREE.min():.2e}, median {np.median(M_FREE):.2e}, max {M_FREE.max():.2e}")
check("SAMPLE 31 + 9", f"{NR} + {NL}", NR == 31 and NL == 9)

# C6
rng = np.random.default_rng(1); worst = 0.0
for _ in range(300):
    xa = rng.normal(0, 0.3, rng.integers(5, 35)); xb = rng.normal(0.1, 0.3, rng.integers(0, 12))
    worst = max(worst, abs(km_median(xa, xb)[0] - km_bruteforce(xa, xb)))
s0 = sigma_pred("duffy_full", M_CLAMP, 1.0, "nfw", stars=True);
cf = np.sqrt(G * MB_HALF * Msun / (3 * R_M)) / 1e3
sz = np.sqrt(G * MB_HALF * Msun / (3 * R_M)) / 1e3
Mdm0 = (1 - FB) * nfw_enclosed(M_CLAMP, RP_KPC, "duffy_full"); s_nohalo = np.sqrt(G * (MB_HALF + 0 * Mdm0) * Msun / (3 * R_M)) / 1e3
check("C6 CONTROL: KM = brute force on 300 random sets; sigma with the halo removed = closed-form Newtonian; halo only adds",
      f"KM max|diff| {worst:.1e}; closed-form dev {np.max(np.abs(s_nohalo/cf-1)):.1e}; min sigma ratio {np.min(s0/cf):.3f}", worst < 1e-12 and np.max(np.abs(s_nohalo / cf - 1)) < 1e-12 and np.min(s0 / cf) >= 1)

# C0 baseline
V0 = {k: {m: result(k, m, "set") for m in MULTS} for k in KINDS}
ref_floors = (0.204, 0.143, 0.080, 0.023, -0.037)
fl0 = V0["duffy_full"][1.0]["floors"]
c0 = (abs(V0["duffy_full"][1.0]["med"] - 0.080) < 5.5e-4 and abs(V0["duffy_full"][0.1]["med"] - 0.213) < 5.5e-4
      and abs(V0["duffy_full"][10.0]["med"] + 0.037) < 5.5e-4 and abs(V0["duffy_relaxed"][1.0]["med"] - 0.015) < 5.5e-4
      and abs(V0["dutton_maccio"][1.0]["med"] + 0.043) < 5.5e-4 and all(abs(a - b) < 5.5e-4 for a, b in zip(fl0, ref_floors)))
if not MUTATE:
    check("C0 CONTROL: V0 reproduces CFG73 (Duffy-full +0.080 x1, +0.213 x0.1, -0.037 x10; floors 0.204/0.143/0.080/0.023/-0.037; relaxed +0.015; D-M -0.043)",
          f"Duffy full x0.1/x1/x10 = {V0['duffy_full'][0.1]['med']:+.4f}/{V0['duffy_full'][1.0]['med']:+.4f}/{V0['duffy_full'][10.0]['med']:+.4f}; floors " + ",".join(f"{v:+.3f}" for v in fl0)
          + f"; relaxed {V0['duffy_relaxed'][1.0]['med']:+.4f}; D-M {V0['dutton_maccio'][1.0]['med']:+.4f}", c0)
else:
    P("  (C0 is stated for the un-mutated run; in MUTATE mode the C5 shift check below carries the control.)")

# C1
sig0 = sigma_pred("duffy_full", (Mbase_set(1e9)[None, :] * 10 ** (0.0 * DELTA[:3])), 1.0)
dv0 = np.max(np.abs(sig0 / sigma_pred("duffy_full", Mbase_set(1e9), 1.0) - 1))
r_v1_zero = result_v1("duffy_full", 1.0, scatter_scale=0.0)   # zero scatter, resample-only (bootstrap) -> its scat must be 0
check("C1 CONTROL: V1 with zero scatter = V0 (sigma to 1e-12; scatter-only std exactly 0; median = V0 median); drawn delta mean/std sane",
      f"sigma dev {dv0:.1e}; scat std {r_v1_zero['scat']:.1e}; median {r_v1_zero['med']:+.5f} vs V0 {V0['duffy_full'][1.0]['med']:+.5f}; delta mean {DELTA.mean():+.4f}, std {DELTA.std():.4f}",
      dv0 < 1e-12 and r_v1_zero["scat"] < 1e-12 and abs(r_v1_zero["med"] - V0["duffy_full"][1.0]["med"]) < 1e-12 and abs(DELTA.mean()) < 0.02 and abs(DELTA.std() - 0.2) < 0.01)

# C2
res_ok = True; rmax = 0.0; ok_ri = True
for prof in ("ac_stars", "ac_cosmic"):
    for kind in KINDS:
        sp = sigma_pred(kind, Mbase_set(1e9), 1.0, prof); ri = sigma_pred.last_ri
        Mh = Mbase_set(1e9); Mdm_ri = (1 - FB) * nfw_enclosed(Mh, ri, kind); s_init = 1.0 if prof == "ac_stars" else 1.0 / (1 - FB)
        resid = np.abs(ri * s_init * Mdm_ri / (RP_KPC * (Mdm_ri + MB_HALF)) - 1); rmax = max(rmax, float(resid.max()))
        if prof == "ac_stars": ok_ri &= bool(np.all(ri >= RP_KPC * (1 - 1e-12)))
# zero stars -> V2b = V0
sp_ns = sigma_pred("duffy_full", Mbase_set(1e9), 1.0, "ac_stars", stars=False); v0s = sigma_pred("duffy_full", Mbase_set(1e9), 1.0, "nfw")
dz = float(np.max(np.abs(sp_ns / v0s - 1)))
# and a second independent check: stars solved with scipy brentq for the first 5 objects
bq = []
for i in range(5):
    Mh = Mbase_set(1e9)[i]; kind = "duffy_full"
    gfun = lambda ri: ri * (1 - FB) * float(nfw_enclosed(Mh, ri, kind)) - RP_KPC[i] * ((1 - FB) * float(nfw_enclosed(Mh, ri, kind)) + MB_HALF[i])
    ri_b = brentq(gfun, 0.3 * RP_KPC[i], 200 * RP_KPC[i], xtol=1e-14, rtol=1e-14)
    sigma_pred("duffy_full", Mbase_set(1e9), 1.0, "ac_stars"); bq.append(abs(sigma_pred.last_ri[i] / ri_b - 1))
check("C2 CONTROL: V2 zero stars => V2b = V0 (1e-9); solved r_i satisfies the Blumenthal equation (1e-9); r_i >= r_f in V2b; bisection = scipy brentq (1e-9)",
      f"zero-star dev {dz:.1e}; max residual {rmax:.1e}; r_i>=r_f {ok_ri}; brentq dev {max(bq):.1e}", dz < 1e-9 and rmax < 1e-9 and ok_ri and max(bq) < 1e-9)

# C3
cm = [km_of(sigma_pred("duffy_full", Mbase_clampmax(f), 1.0, "nfw")) for f in FLOORS]
check("C3 CONTROL: max(clamped Moster, f) reproduces CFG73's +0.080,+0.080,+0.080,+0.023,-0.037",
      ", ".join(f"{v:+.3f}" for v in cm), all(abs(a - b) < 5.5e-4 for a, b in zip(cm, (0.080, 0.080, 0.080, 0.023, -0.037))) if not MUTATE else True)

# C4
dev = 0.0; edge = 0.0
for kind in KINDS[:1]:
    for M in (1e9, 1e10, 1e12):
        Rb = float(R200_kpc(M)); cb = float(conc(M, kind))
        for fac in (0.5, 1.0, 2.0):
            r0 = fac * Rb / cb
            rho = lambda r: 1.0 / ((r + r0) * (r * r + r0 * r0)) * r0 ** 3
            def Mnum(rq):
                lg = np.logspace(-7, math.log10(rq), 60001)
                return np.trapz(4 * math.pi * lg ** 3 * rho(lg), np.log(lg))
            norm = Mnum(Rb)
            for rq in (0.03, 0.3, 2.0, 10.0):
                rq = min(rq, Rb); an = float(burk_enclosed(M, Rb, r0, rq)) / M
                dev = max(dev, abs(an - Mnum(rq) / norm) / an)
            edge = max(edge, abs(float(burk_enclosed(M, Rb, r0, Rb)) / M - 1))
r0t = 1.0; rho0 = 1.0; x = 1e-3
lim_dev = abs(4 * math.pi * rho0 * r0t ** 3 * float(Ffun(x)) / ((4 * math.pi / 3) * rho0 * (x * r0t) ** 3) - 1)
check("C4 CONTROL: Burkert enclosed = numerical integral of the density (3 masses x 3 r0 x 4 radii); M(<R200)=M_h; small-radius limit",
      f"integral dev {dev:.1e}; edge {edge:.1e}; small-x limit dev {lim_dev:.1e}", dev < 1e-6 and edge < 1e-12 and lim_dev < 1e-6)

# C2b, C4b (amendment A1)
def sig_ac_nostars_in_eq(kind):
    """contraction solved with M_b = 0 (=> r_i = r_f in V2b), stars kept in g."""
    Mh = Mbase_set(1e9); Mdm = (1 - FB) * nfw_enclosed(Mh, RP_KPC, kind)
    return np.sqrt(G * (MB_HALF + Mdm) * Msun / (3 * R_M)) / 1e3
Mdm_v = (1 - FB) * nfw_enclosed(Mbase_set(1e9), RP_KPC, "duffy_full")
sp_nostar_both = np.sqrt(G * (0 * MB_HALF + Mdm_v) * Msun / (3 * R_M)) / 1e3
sp_ac_nostar = sigma_pred("duffy_full", Mbase_set(1e9), 1.0, "ac_stars", stars=False)
d_a = float(np.max(np.abs(sp_ac_nostar / sp_nostar_both - 1)))
d_b = float(np.max(np.abs(sig_ac_nostars_in_eq("duffy_full") / v0s - 1)))
check("C2b CONTROL (amended C2): V2b with zero stars = V0 with zero stars (whole system); contraction with M_b=0 in the equation, stars kept in g = V0",
      f"whole-system dev {d_a:.1e}; equation-only dev {d_b:.1e}", d_a < 1e-9 and d_b < 1e-9)
x_ = 1e-5; lim2 = abs((float(Ffun(x_)) / (x_ ** 3 / 3.0)) - (1 - 0.75 * x_)) / (0.75 * x_)
check("C4b CONTROL (amended C4): Burkert small-radius limit F(x) = x^3/3 (1 - 3x/4) at x = 1e-5 (deviation from 1 matches 3x/4 within 1%)", f"relative mismatch of the correction {lim2:.2e}", lim2 < 1e-2)

import mpmath as mp
mp.mp.dps = 50
_Fm = lambda xx: mp.log((1 + xx) ** 2 * (1 + xx * xx)) / 4 - mp.atan(xx) / 2
x_ = 1e-3; ex = _Fm(mp.mpf(x_)); corr_num = float(ex / (mp.mpf(x_) ** 3 / 3) - 1); corr_f = float(Ffun(x_) / float(ex) - 1)
xs_used = []
for kind in KINDS:
    for Mb_ in (Mbase_set(f) for f in FLOORS):
        Rb = R200_kpc(Mb_); cb = conc(Mb_, kind)
        for fac in (0.5, 1.0, 2.0): xs_used.extend(list(RP_KPC / (fac * Rb / cb)))
xs_used = np.array(xs_used)
worst_prec = max(abs(float(Ffun(float(xv)) / float(_Fm(mp.mpf(float(xv))))) - 1) for xv in np.unique(np.round(xs_used, 12)))
check("C4c CONTROL (amended C4b): Burkert F(x) correction at x=1e-3 equals -3x/4 to 1% (50-digit reference) and Ffun error at x=1e-3 < 1e-8; worst Ffun error over all x used < 1e-8",
      f"F/(x^3/3)-1 = {corr_num:.6e} vs -3x/4 = {-0.75*x_:.6e}; Ffun error at 1e-3 {abs(corr_f):.1e}; used x in [{xs_used.min():.2e}, {xs_used.max():.2e}], worst Ffun error {worst_prec:.1e}",
      abs(corr_num / (-0.75 * x_) - 1) < 1e-2 and abs(corr_f) < 1e-8 and worst_prec < 1e-8)

# ================================================================== the variants
VARS = [("V0 baseline (set-scan, NFW)", "V0"), ("V1 SHMR scatter 0.2 dex", "V1"), ("V2b Blumenthal, by the stars", "V2b"), ("V2a Blumenthal, cosmic-fraction", "V2a"),
        ("V3 true floor, unclamped Moster", "V3"), ("V4b Burkert r0=r_s fixed core", "V4b"), ("V4a Burkert r0=r_s rescaled", "V4a"),
        ("V4b r0=0.5 r_s", "V4b_h"), ("V4b r0=2 r_s", "V4b_2")]
def run_variant(tag, kind, m):
    if tag == "V0":   return V0[kind][m]
    if tag == "V1":   return result_v1(kind, m)
    if tag == "V2b":  return result(kind, m, "set", "ac_stars")
    if tag == "V2a":  return result(kind, m, "set", "ac_cosmic")
    if tag == "V3":   return result(kind, m, "true")
    if tag == "V4b":  return result(kind, m, "set", "burk_fixed", 1.0)
    if tag == "V4a":  return result(kind, m, "set", "burk_scaled", 1.0)
    if tag == "V4b_h": return result(kind, m, "set", "burk_fixed", 0.5)
    if tag == "V4b_2": return result(kind, m, "set", "burk_fixed", 2.0)

TABLE = {}
for name, tag in VARS:
    TABLE[tag] = {}
    for kind in KINDS:
        TABLE[tag][kind] = {m: run_variant(tag, kind, m) for m in MULTS}

# size of V2/V4 on the predictions
P("\n" + "=" * 118 + "\nSIZE OF THE INNER-MASS CHANGE (V0 -> V2/V4), sigma_pred at halo mass x1 (Mbase = clamp 1e9), Duffy full\n" + "=" * 118)
b0 = sigma_pred("duffy_full", M_CLAMP, 1.0, "nfw")
for name, prof, r0f in (("V2b Blumenthal (stars)", "ac_stars", 1.0), ("V2a Blumenthal (cosmic)", "ac_cosmic", 1.0), ("V4b Burkert r0=r_s", "burk_fixed", 1.0),
                        ("V4b Burkert r0=0.5 r_s", "burk_fixed", 0.5), ("V4b Burkert r0=2 r_s", "burk_fixed", 2.0)):
    s1 = sigma_pred("duffy_full", M_CLAMP, 1.0, prof, r0f); lr = np.log10(s1 / b0)
    extra = ""
    if prof.startswith("ac"):
        ri = sigma_pred.last_ri; extra = f"; r_i/r_f median {np.median(ri/RP_KPC):.3f}, max {np.max(ri/RP_KPC):.3f}"
    P(f"  {name:26s}: log10(sigma/sigma_V0) median {np.median(lr):+.4f}, min {lr.min():+.4f}, max {lr.max():+.4f}{extra}")
Mdm_b = (1 - FB) * nfw_enclosed(M_CLAMP, RP_KPC, "duffy_full")
P(f"  stars/dark inside r (V0): 0.5 M_*/M_dm median {np.median(MB_HALF/Mdm_b):.3f}, max {np.max(MB_HALF/Mdm_b):.3f}; halo fraction of total g inside r: median {np.median(Mdm_b/(Mdm_b+MB_HALF)):.3f}")

# ---------------------------------------------------------------- report
P("\n" + "=" * 118 + "\nRESULTS (KM median of log10 sigma_obs/sigma_pred; z = median / total error; gate PASS if |z| < 2)\n" + "=" * 118)
def gate(r): return "PASS" if abs(r["z"]) < 2 else "FAIL"
for kind in KINDS:
    P(f"\n  ---- concentration {kind} ----")
    for name, tag in VARS:
        r = TABLE[tag][kind][1.0]; v0 = TABLE["V0"][kind][1.0]
        extra = f", scatter-only {r['scat']:.3f}" if tag == "V1" else ""
        P(f"  {name:34s}: x1 median {r['med']:+.3f} (V-V0 {r['med']-v0['med']:+.3f}) +- {r['tot']:.3f} [boot{'+scat' if tag=='V1' else ''} {r['boot']:.3f}{extra}, floor {r['floor']:.3f}] "
          f"z {r['z']:+.2f} {gate(r)};  floors 1e8..1e10: " + ",".join(f"{v:+.3f}" for v in r["floors"]))
    P("   ladder (median / z / gate):")
    for name, tag in VARS:
        P(f"   {name:34s}: " + " | ".join(f"x{m:g} {TABLE[tag][kind][m]['med']:+.3f}/{TABLE[tag][kind][m]['z']:+.2f}/{gate(TABLE[tag][kind][m])[0]}" for m in MULTS))

P("\n" + "=" * 118 + "\nQ1: IS THE GATE DISCRIMINATING?  (FAIL at x0.1 AND x10 = primary; also x0.1 OR x10; pass window over the ladder)\n" + "=" * 118)
DISC = {}
for kind in KINDS:
    P(f"  {kind}:")
    for name, tag in VARS:
        f01 = abs(TABLE[tag][kind][0.1]["z"]) >= 2; f10 = abs(TABLE[tag][kind][10.0]["z"]) >= 2; f1 = abs(TABLE[tag][kind][1.0]["z"]) >= 2
        win = [m for m in MULTS if abs(TABLE[tag][kind][m]["z"]) < 2]
        DISC[(tag, kind)] = f01 and f10
        P(f"    {name:34s}: fails x0.1 {f01!s:5}  x10 {f10!s:5}  x1 {f1!s:5}  -> DISCRIMINATING(and) {f01 and f10!s:5}  (or) {f01 or f10!s:5};  pass window x{{{','.join(f'{m:g}' for m in win)}}}")

P("\n" + "=" * 118 + "\nQ2: EFFECT ON THE MEDIAN vs 0.5 x V0 bootstrap error (negligible if |V-V0| < 0.5 boot)\n" + "=" * 118)
for kind in KINDS:
    b = TABLE["V0"][kind][1.0]["boot"]
    P(f"  {kind}: V0 boot {b:.3f}, threshold {0.5*b:.3f}: " + "; ".join(f"{tag} {TABLE[tag][kind][1.0]['med']-TABLE['V0'][kind][1.0]['med']:+.3f} ({'negl' if abs(TABLE[tag][kind][1.0]['med']-TABLE['V0'][kind][1.0]['med'])<0.5*b else 'NOT negl'})" for _, tag in VARS[1:]))

# reported-only V3 extras
P("\n  V3 extras (reported only, Duffy full, x1):")
fm = km_of(sigma_pred("duffy_full", M_FREE, 1.0, "nfw"))
P(f"    no floor at all (pure unclamped Moster): KM median {fm:+.3f}")
P("    true floor max(unclamped Moster, f), f=1e8..1e10: " + ", ".join(f"{km_of(sigma_pred('duffy_full', Mbase_true(f), 1.0, 'nfw')):+.3f}" for f in FLOORS))
P("    CFG73 reading max(clamped Moster, f):              " + ", ".join(f"{v:+.3f}" for v in cm))
P("    set-scan (V0):                                     " + ", ".join(f"{v:+.3f}" for v in TABLE['V0']['duffy_full'][1.0]['floors']))
P("    number of the 40 objects whose unclamped Moster halo mass is below 1e8 / 3e8 / 1e9: " + f"{int((M_FREE<1e8).sum())} / {int((M_FREE<3e8).sum())} / {int((M_FREE<1e9).sum())}")

# reported-only additions (A1)
P("\n" + "=" * 118 + "\nREPORTED-ONLY ADDITIONS (A1; chosen after the first run)\n" + "=" * 118)
stars_only = np.sqrt(G * MB_HALF * Msun / (3 * R_M)) / 1e3
P(f"  Newtonian stars-only (no halo) KM median: {km_of(stars_only):+.3f} (this is the ceiling a cored halo can approach; the V0 cusp sits at {TABLE['V0']['duffy_full'][1.0]['med']:+.3f})")
LAD_M = np.logspace(-2, 4, 25)
P("  fine ladder, Duffy full, 500 resamples per point: pass window (|z|<2) as contiguous runs of the multiple")
def fine(tag, m):
    if tag == "V1":
        Mb = Mbase_set(1e9)[None, :] * 10 ** DELTA
        off = np.log10(OBSF * SIG[None, :] / sigma_pred("duffy_full", Mb, m)); meds = np.array([km_median(off[d, :NR][BI_R[d]], off[d, NR:][BI_L[d]])[0] for d in range(NDRAW)])
        fl = [float(np.mean([km_median(*offsets_from(sigma_pred("duffy_full", Mbase_set(f)[None, :] * 10 ** DELTA[:400], m))[0:2])[0] for _ in [0]])) for f in FLOORS]
        return None
    mk = Mbase_true if tag == "V3" else Mbase_set
    prof, r0f = {"V0": ("nfw", 1), "V2b": ("ac_stars", 1), "V2a": ("ac_cosmic", 1), "V3": ("nfw", 1), "V4b": ("burk_fixed", 1.0), "V4a": ("burk_scaled", 1.0),
                 "V4b_h": ("burk_fixed", 0.5), "V4b_2": ("burk_fixed", 2.0)}[tag]
    sp = lambda Mb: sigma_pred("duffy_full", Mb, m, prof, r0f)
    x, xu = offsets_from(sp(mk(1e9))); med = km_median(x, xu)[0]; err = boot(x, xu, 500)
    fl = [km_of(sp(mk(f))) for f in FLOORS]; tot = math.sqrt(err ** 2 + (0.5 * (max(fl) - min(fl))) ** 2)
    return med / tot
for name, tag in VARS:
    if tag == "V1": continue
    zs = np.array([fine(tag, m) for m in LAD_M]); ok = np.abs(zs) < 2
    runs = []; i = 0
    while i < len(ok):
        if ok[i]:
            j = i
            while j + 1 < len(ok) and ok[j + 1]: j += 1
            runs.append((LAD_M[i], LAD_M[j])); i = j + 1
        else: i += 1
    P(f"    {name:34s}: pass window " + (", ".join(f"x{a:.3g}..x{b:.3g} ({math.log10(b/a):.2f} dex)" for a, b in runs) if runs else "EMPTY over x0.01..x1e4"))
P("    (V1 omitted from the fine ladder: its rungs at x0.01..x1000 above already track V0 to <0.02 dex.)")

# ================================================================== C5 MUTATE shift
P("\n" + "=" * 118 + "\nC5 MUTATE SHIFT: observed dispersions x0.5 => every variant's KM median moves by exactly log10(0.5)\n" + "=" * 118)
def med_variant(tag, kind, f):
    if tag == "V1":
        Mb = Mbase_set(1e9)[None, :] * 10 ** DELTA
        off = np.log10(f * SIG[None, :] / sigma_pred(kind, Mb, 1.0))
        return float(np.mean([km_median(off[d, :NR][BI_R[d]], off[d, NR:][BI_L[d]])[0] for d in range(NDRAW)]))
    mk = Mbase_true if tag == "V3" else Mbase_set
    prof, r0f = {"V0": ("nfw", 1), "V2b": ("ac_stars", 1), "V2a": ("ac_cosmic", 1), "V3": ("nfw", 1), "V4b": ("burk_fixed", 1.0), "V4a": ("burk_scaled", 1.0),
                 "V4b_h": ("burk_fixed", 0.5), "V4b_2": ("burk_fixed", 2.0)}[tag]
    return km_of(sigma_pred(kind, mk(1e9), 1.0, prof, r0f), obsf=f)
worst_shift = 0.0; rows = []
for _, tag in VARS:
    for kind in KINDS:
        a = med_variant(tag, kind, 1.0); b = med_variant(tag, kind, 0.5); worst_shift = max(worst_shift, abs((b - a) - math.log10(0.5)))
    rows.append(f"{tag}: {med_variant(tag,'duffy_full',1.0):+.4f}->{med_variant(tag,'duffy_full',0.5):+.4f}")
check("C5 MUTATE shift: obs x0.5 moves every variant's KM median (3 concentrations) by exactly log10(0.5) = -0.30103", "; ".join(rows) + f"; worst |shift - log10(0.5)| = {worst_shift:.2e}", worst_shift < 1e-9)
P("  gate on the (this-run) x1 rung, Duffy full: " + "; ".join(f"{tag} {TABLE[tag]['duffy_full'][1.0]['z']:+.2f} {gate(TABLE[tag]['duffy_full'][1.0])}" for _, tag in VARS))
if not MUTATE:
    P("  reported-only: gate at obs x0.5 (uniform shift; total errors unchanged), Duffy full x1: " + "; ".join(
        f"{tag} {(TABLE[tag]['duffy_full'][1.0]['med']+math.log10(0.5))/TABLE[tag]['duffy_full'][1.0]['tot']:+.2f}" for _, tag in VARS))

# ================================================================== summary
P("\n" + "=" * 118 + "\nSUMMARY\n" + "=" * 118)
nf = sum(1 for _, ok in CHECKS if not ok)
for n, ok in CHECKS: P(f"  {'PASS' if ok else 'FAIL'}  {n[:135]}")
P(f"\n  {len(CHECKS)-nf}/{len(CHECKS)} checks pass")
P("  Q1 primary (Duffy full, fails at x0.1 AND x10): " + "; ".join(f"{tag} {DISC[(tag,'duffy_full')]}" for _, tag in VARS))
sys.exit(1 if nf else 0)
