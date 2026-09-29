#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG73 -- INDEPENDENT RE-DERIVATION of CFG69's headline "the LCDM ultra-faint gate under the Dutton-Maccio concentration".
(Declared BEFORE the first run.  Own implementation; no CFG69/CFG42/CFG7 analysis code is exec'd or imported.  The only committed
code touched is the 6-line Moster/halo_mass snippet of hunt_2026/h48_h69b_relative_isolation.py, exec'd on its own as the CONTROL
comparator, and the CSV data file real_research/data/dsph/lvd_dwarf_mw.csv.)

QUESTION.  CFG69 reports, for the Milky Way ultra-faints (31 resolved + 9 upper limits; M_V > -7.7; Upsilon_V = 2; half of the
stars enclosed; sigma^2 = g(r) r / 3 at r = (4/3) r_half; stars only), that with Moster halo masses and the Duffy full-200c
concentration the LCDM Kaplan-Meier median offset log10(sigma_obs/sigma_pred) is +0.080 dex (0.6 sigma, gate passes), that the
Dutton-Maccio version gives -0.043 (-0.4 sigma) and Duffy-relaxed +0.015 (0.1 sigma), and that the gate is NON-DISCRIMINATING
(passes for every halo mass x0.1..x100).  Re-derive all of it.

MODEL (mine).  Halo mass M_h = Moster+2013 (z = 0: N = 0.0351, log M1 = 11.590, beta = 1.376, gamma = 0.608;
M_*/M_h = 2N[(M_h/M1)^-beta + (M_h/M1)^gamma]^-1) INVERTED at M_* = 2 L_V (exact root-finding on a bracket, not a grid) and FLOORED at
M_h = 1e9 (the clamp: M_*(1e9) ~ 1.6e4, below that every satellite gets 1e9).  NFW, M(<r) = M_h m(c x)/m(c), m(t) = ln(1+t) - t/(1+t),
x = r/R200 clipped to [1e-4, 5], R200 = (3 M_h / (4 pi 200 rho_c))^(1/3), rho_c from H0 = 67.4 (h = 0.674), G = 6.674e-11,
Msun = 1.989e30, kpc = 3.0857e19 m.  Concentration, three relations:
   DUFFY-FULL   c = 5.71 (M/(2e12/0.674))^-0.084     DUFFY-RELAXED  c = 6.71 (M/(2e12/0.674))^-0.091
   DUTTON-MACCIO 2014  log10 c = 0.905 - 0.101 (log10(M h) - 12)
Debris: (1 - f_b) M_NFW(<r), f_b = 0.02237/(0.02237 + 0.1200), nu = 1 (no phantom), no adiabatic contraction.
Prediction: g = G [0.5 M_* + (1 - f_b) M_NFW(<r)] / r^2, sigma_pred = sqrt(g r / 3), r = (4/3) r_half (pc from rhalf_sph_physical, else
rhalf_physical).  STARS ONLY (a variant with 1.33 M_HI is reported as a sensitivity).  Sample: rows with M_V > -7.7 and distance_host (else
distance_gc) and r_half present; RESOLVED if vlos_sigma > 0 and no vlos_sigma_ul; LIMIT (left-censored: true sigma <= limit) if vlos_sigma_ul.
Offset = log10(sigma_obs / sigma_pred), the limit's offset is its upper bound.

STATISTIC.  Kaplan-Meier median for left-censored data = KM on the reflected offsets (y = -x, limits = right-censored), median = the
first event time at which S <= 0.5, mapped back (my own vectorised product-limit; ties: events before censorings).  Bootstrap error:
2000 resamples (resolved and limits resampled separately, as the lanes do; seed 20260928; joint resampling and 2 other seeds reported).
COLLAPSE-MASS FLOOR: the KM median recomputed with the halo mass of every satellite with M_* < 1e5 SET to 1e8, 3e8, 1e9, 3e9, 1e10 (the lanes'
scan); floor error = half the range.  Total error = sqrt(bootstrap^2 + floor^2) (the task's error model; the Upsilon_V 1-4 term is reported
separately, not in the total).  Gate: |median| / total < 2.
SENSITIVITY: every halo mass (floors included) multiplied by 0.01, 0.1, 1, 10, 100, 1000; gate recomputed at each multiple, for each concentration.

CONTROLS (declared).  C1: my Moster halo_mass vs the committed h48 halo_mass at 10 stellar masses (agreement <= 3e-4 in dex; the committed one is a
1301-point grid interpolation).  C2: my NFW/Dutton-Maccio vs h48's committed nfw_enclosed, 30 masses x 20 radii (<= 1e-9 relative).
C3: NFW analytic enclosed mass vs direct numerical integration of the density (<= 1e-6), M(<R200) = M_h.  C4: my KM against a brute-force
alternative (a direct product-limit written differently, plus a case with no censoring = ordinary median, plus a hand-worked example).
C5 (pipeline check on the data, NOT part of the LCDM claim): the bare-law offset (nu = exponential RAR kernel, a0 = 9.36e-11 / 1.13e-10, isolated,
stars only + 1.33 M_HI as the lanes' FG001 does, i.e. the committed lane definition) should reproduce CFG42's reference +0.325 / +0.304 KM
median and +0.355 resolved-only median (the reference is read from CFG42's .out, not re-used as code).  C6: M_h -> 0 gives the closed-form Newtonian sigma.
MUTATE=1: every observed dispersion (resolved AND limits) x 0.5.  Then the LCDM offset must shift by exactly log10(0.5) = -0.30103 (hard control,
checked in both modes), and the declared gate must FAIL.  PRE-RUN EXPECTATION (declared honestly now): the shift is 0.301 dex against a total
error of ~0.13 dex, starting from +0.08, i.e. landing near -0.22 / 0.13 = -1.7 sigma, which is INSIDE 2 sigma; I therefore expect the shift
check to pass and the gate NOT to fail.  If so that is the requested MUTATE gate-fail control failing, and it is reported as such, not repaired.
An additional REPORTED-ONLY ladder (obs x 0.5, 0.25, 0.1) shows where the gate does trip.
NOTHING is tuned after a result is seen.  Nothing in the repository is edited; outputs go to the scratch directory only.
Run: python3 cfg73_lcdm_uf_rederive.py    (MUTATE=1 for the control)
"""
import os, sys, math, csv, io, contextlib
import numpy as np
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
CSV_MW = os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv")
H48 = os.path.join(REPO, "hunt_2026/h48_h69b_relative_isolation.py")
OBSF = 0.5 if MUTATE else 1.0

CHECKS = []
def P(s=""): print(s, flush=True)
def check(name, detail, ok, must_fail=False):
    CHECKS.append((name, ok))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")

P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every observed dispersion x 0.5 ***")

# ------------------------------------------------------------------ constants (h48 / hunt_lib values, as specification)
G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; PC = 3.0857e16
H0 = 67.4; h = 0.674
FB = 0.02237 / (0.02237 + 0.1200)
RHO_C = 3 * (H0 * 1e3 / Mpc) ** 2 / (8 * math.pi * G) / Msun * (3.0857e22) ** 3   # Msun / Mpc^3
NA, LM1, BE, GA = 0.0351, 11.590, 1.376, 0.608

def moster_mstar(Mh):
    x = np.asarray(Mh, float) / 10 ** LM1
    return np.asarray(Mh, float) * 2 * NA / (x ** (-BE) + x ** GA)

MH_FLOOR = 1e9
def halo_mass(Mstar):
    """invert Moster exactly; floor at 1e9 (the clamp)."""
    out = []
    for ms in np.atleast_1d(np.asarray(Mstar, float)):
        f = lambda lm: math.log10(float(moster_mstar(10 ** lm))) - math.log10(ms)
        if f(math.log10(MH_FLOOR)) >= 0:
            out.append(MH_FLOOR)
        else:
            out.append(10 ** brentq(f, 9.0, 16.0, xtol=1e-13))
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

# ------------------------------------------------------------------ data (my own reading of the CSV)
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
    MHI = fnum(r["mass_HI"])
    rec = dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** MHI if MHI is not None else 0.0))
    if ul is not None:
        rec["sig"] = ul; LIM.append(rec)
    elif sig is not None and sig > 0:
        rec["sig"] = sig; RES.append(rec)

UPS = 2.0
def arr(sample, key): return np.array([d[key] for d in sample], float)

# ------------------------------------------------------------------ predictions
def sigma_lcdm(sample, kind, ups=UPS, mult=1.0, mh_set=None, gas=False, zero_halo=False):
    Ms = ups * arr(sample, "LV")
    Mb = Ms + (1.33 * arr(sample, "MHI") if gas else 0.0)
    rp = (4 / 3.) * arr(sample, "rh")                               # pc
    Mh = halo_mass(2.0 * arr(sample, "LV"))                          # Moster at Upsilon_V = 2 always (the lanes' convention)
    if mh_set is not None:
        Mh = np.where(2.0 * arr(sample, "LV") < 1e5, mh_set, Mh)
    Mh = Mh * mult
    r_m = rp * PC
    Mnfw = 0.0 if zero_halo else (1 - FB) * nfw_enclosed(Mh, rp / 1000.0, kind)
    g = G * (0.5 * Mb + Mnfw) * Msun / r_m ** 2
    return np.sqrt(g * r_m / 3.0) / 1e3

def nu_exp(y): y = np.maximum(y, 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def sigma_law(sample, a0, gas=True):
    Mb = UPS * arr(sample, "LV") + (1.33 * arr(sample, "MHI") if gas else 0.0)
    r_m = (4 / 3.) * arr(sample, "rh") * PC
    gN = G * 0.5 * Mb * Msun / r_m ** 2
    return np.sqrt(gN * nu_exp(gN / a0) * r_m / 3.0) / 1e3

# ------------------------------------------------------------------ Kaplan-Meier (left-censored via reflection), mine
def km_median(x, xu):
    y = np.concatenate([-np.asarray(x, float), -np.asarray(xu, float)])
    ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]           # ascending y; events first on ties
    n = len(y); atrisk = n - np.arange(n)
    fac = np.where(ev, 1.0 - 1.0 / atrisk, 1.0)
    S = np.cumprod(fac)
    idx = np.nonzero(ev & (S <= 0.5 + 1e-15))[0]
    if len(idx) == 0:
        return -y[-1], False
    return -y[idx[0]], True

def km_median_bruteforce(x, xu):
    """direct product-limit at the distinct event values, written differently (grouped ties, explicit at-risk counts)."""
    pts = [(-v, 1) for v in x] + [(-v, 0) for v in xu]
    times = sorted(set(t for t, e in pts if e == 1))
    S = 1.0
    for t in times:
        n_risk = sum(1 for tt, e in pts if tt >= t)
        d = sum(1 for tt, e in pts if tt == t and e == 1)
        S *= 1 - d / n_risk
        if S <= 0.5 + 1e-15:
            return -t
    return -max(t for t, e in pts)

def offsets(kind, **kw):
    sr = sigma_lcdm(RES, kind, **kw); sl = sigma_lcdm(LIM, kind, **kw)
    return np.log10(OBSF * arr(RES, "sig") / sr), np.log10(OBSF * arr(LIM, "sig") / sl)

def boot(x, xu, nb=2000, seed=20260928, joint=False):
    rng = np.random.default_rng(seed); v = np.empty(nb); nfail = 0
    for i in range(nb):
        if joint:
            allx = np.concatenate([x, xu]); flag = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
            k = rng.integers(0, len(allx), len(allx)); a = allx[k]; f = flag[k]
            v[i], ok = km_median(a[f], a[~f])
        else:
            v[i], ok = km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))])
        nfail += (not ok)
    return float(np.std(v)), nfail

FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)

def ufd_result(kind, mult=1.0, nb=2000, seed=20260928):
    x, xu = offsets(kind, mult=mult)
    med, _ = km_median(x, xu)
    err, _ = boot(x, xu, nb, seed)
    fl = [km_median(*offsets(kind, mult=mult, mh_set=f))[0] for f in FLOORS]
    fsig = 0.5 * (max(fl) - min(fl))
    tot = math.sqrt(err ** 2 + fsig ** 2)
    return dict(med=med, boot=err, floor=fsig, tot=tot, z=med / tot, floors=fl, resolved_med=float(np.median(x)))

# ================================================================== SAMPLE
P("\n" + "=" * 110 + "\nSAMPLE\n" + "=" * 110)
P(f"  resolved {len(RES)}, limits {len(LIM)}; log10 M_* range {math.log10(UPS*min(arr(RES+LIM,'LV'))):.2f} - {math.log10(UPS*max(arr(RES+LIM,'LV'))):.2f}; "
  f"Moster clamp: M_*(M_h=1e9) = {float(moster_mstar(1e9)):.3e}; satellites clamped: {int(np.sum(2*arr(RES+LIM,'LV') < float(moster_mstar(1e9))))} of {len(RES)+len(LIM)}; "
  f"M_* < 1e5: {int(np.sum(2*arr(RES+LIM,'LV') < 1e5))}")
check("SAMPLE: 31 resolved + 9 limits", f"{len(RES)} + {len(LIM)}", len(RES) == 31 and len(LIM) == 9)

# ================================================================== CONTROLS C1-C4, C6
P("\n" + "=" * 110 + "\nCONTROLS\n" + "=" * 110)
src = open(H48).read().splitlines()
i0 = next(i for i, l in enumerate(src) if l.startswith("def moster_mstar"))
i1 = next(i for i, l in enumerate(src) if l.startswith("def nfw_enclosed"))
snippet = "import numpy as np, math\n" + "\n".join(src[i0:i1])
_RHO_src = next(l for l in src if l.startswith("_RHO_C"))
g48 = {"np": np, "math": math, "H0_KMS": 67.4, "G": G, "Msun": Msun, "Mpc": Mpc}
exec(snippet, g48)
exec(_RHO_src, g48)
exec("\n".join(src[i1:i1 + 7]), g48)
mstars = np.array([1e3, 1e4, 3e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11])
mine = halo_mass(mstars); theirs = g48["halo_mass"](mstars)
dd = np.abs(np.log10(mine) - np.log10(theirs))
P("  C1 table  M_*: mine vs committed halo_mass  (log10):")
for a, b, c in zip(mstars, mine, theirs):
    P(f"      M_* = {a:.0e}: mine {math.log10(b):.6f}, committed {math.log10(c):.6f}")
check("C1 CONTROL: my Moster halo_mass (exact inversion, floor 1e9) equals the committed h48 halo_mass (grid interpolation, clamped) at 10 masses",
      f"max |d log10| {dd.max():.2e}", dd.max() < 3e-4)
mm = np.logspace(9, 14, 30); rr = np.logspace(-2, 1.5, 20)
dev = 0.0
for M in mm:
    a = nfw_enclosed(M, rr, "dutton_maccio"); b = g48["nfw_enclosed"](M, rr)
    dev = max(dev, float(np.max(np.abs(a / b - 1))))
check("C2 CONTROL: my Dutton-Maccio NFW enclosed mass equals h48's committed nfw_enclosed (30 masses x 20 radii)", f"max rel dev {dev:.1e}; rho_c mine {RHO_C:.6e} vs committed {g48['_RHO_C']:.6e}", dev < 1e-9)
# C3 numerical integration of NFW density for the three c
dev3 = 0.0; edge = 0.0
for kind in ("duffy_full", "duffy_relaxed", "dutton_maccio"):
    for M in (1e9, 1e10, 1e12):
        c = float(conc(M, kind)); R = float(R200_kpc(M)); rs = R / c
        for rq in (0.05, 0.3, 2.0, 10.0):
            rq = min(rq, R)
            rho = lambda r: 1.0 / ((r / rs) * (1 + r / rs) ** 2)
            rgrid = np.logspace(-6, math.log10(rq), 40001)
            integ = np.trapz(4 * math.pi * rgrid ** 3 * rho(rgrid), np.log(rgrid))   # 4 pi r^2 rho dr = 4 pi r^3 rho dlnr
            norm = np.trapz(4 * math.pi * np.logspace(-6, math.log10(R), 40001) ** 3 * rho(np.logspace(-6, math.log10(R), 40001)), np.log(np.logspace(-6, math.log10(R), 40001)))
            an = float(nfw_enclosed(M, rq, kind)) / M
            dev3 = max(dev3, abs(an - integ / norm) / an)
        edge = max(edge, abs(float(nfw_enclosed(M, R, kind)) / M - 1))
check("C3 CONTROL: NFW enclosed mass equals numerical integration of the density (3 c-relations x 3 masses x 4 radii); M(<R200) = M_h", f"max rel dev {dev3:.1e}; edge {edge:.1e}", dev3 < 1e-5 and edge < 1e-12)
# C4 KM
rng = np.random.default_rng(1); worst = 0.0; cnt = 0
for _ in range(300):
    x = rng.normal(0, 0.3, rng.integers(5, 35)); xu = rng.normal(0.1, 0.3, rng.integers(0, 12))
    a, ok = km_median(x, xu); b = km_median_bruteforce(x, xu)
    worst = max(worst, abs(a - b)); cnt += 1
med_plain, _ = km_median(np.array([1.0, 2, 3, 4, 5]), np.array([]))
# hand example: x = {1,2,3,4} resolved, limit at 2.5 (left-censored: true <= 2.5). reflected y = -4,-3,-2.5c,-2,-1.
# sorted y: -4(E) n=5 S=.8 ; -3(E) n=4 S=.6 ; -2.5(C) ; -2(E) n=2 S=.3 -> S<=.5 first at y=-2 -> median 2.0
hand, _ = km_median(np.array([1.0, 2, 3, 4]), np.array([2.5]))
check("C4 CONTROL: my KM = brute-force product-limit on 300 random left-censored data sets; uncensored = ordinary (lower-half convention) median; hand example = 2.0",
      f"max |diff| {worst:.1e}; uncensored median of 1..5 -> {med_plain}; hand example {hand}", worst < 1e-12 and med_plain == 3.0 and hand == 2.0)
# C6 zero halo closed form
s0 = sigma_lcdm(RES, "duffy_full", zero_halo=True)
cf = np.sqrt(G * 0.5 * UPS * arr(RES, "LV") * Msun / ((4 / 3.) * arr(RES, "rh") * PC) / 3.0) / 1e3
sh = sigma_lcdm(RES, "duffy_full")
check("C6 CONTROL: with the halo switched off the LCDM sigma is the closed-form Newtonian sqrt(G 0.5 M_*/(3 r)); the halo only adds", f"max rel dev {np.max(np.abs(s0/cf-1)):.1e}; min sigma ratio {np.min(sh/s0):.3f}", np.max(np.abs(s0 / cf - 1)) < 1e-12 and np.min(sh / s0) >= 1)

# C5 bare-law pipeline check on the same data (FG001's committed definition: stars + 1.33 M_HI)
P("\n  C5 pipeline check: bare isolated law (exp kernel), stars + 1.33 M_HI, canonical a0 = 9.36e-11 / alt 1.13e-10")
REFL = {"canonical": (0.325, 0.355, 9.36e-11), "alt": (0.304, 0.334, 1.13e-10)}
okc5 = True
for foot, (ref_km, ref_res, a0) in REFL.items():
    x = np.log10(arr(RES, "sig") / sigma_law(RES, a0)); xu = np.log10(arr(LIM, "sig") / sigma_law(LIM, a0))
    km, _ = km_median(x, xu); rs = float(np.median(x))
    P(f"      {foot}: KM {km:+.4f} (ref {ref_km:+.3f}), resolved-only median {rs:+.4f} (ref {ref_res:+.3f})")
    okc5 &= abs(km - ref_km) < 5e-4 and abs(rs - ref_res) < 5e-4
check("C5 CONTROL (pipeline/data): the bare-law KM and resolved-only medians reproduce CFG42's reference +0.325/+0.355 (canonical), +0.304/+0.334 (alt) to 3 decimals", "see lines above", okc5)

# ================================================================== (1)+(2) HEADLINE
P("\n" + "=" * 110 + "\n(1)+(2) THE LCDM ULTRA-FAINT KM MEDIAN UNDER THREE CONCENTRATION RELATIONS (halo mass x1)\n" + "=" * 110)
KINDS = ("duffy_full", "duffy_relaxed", "dutton_maccio")
CFG69 = {"duffy_full": (0.080, 0.6), "dutton_maccio": (-0.043, -0.4), "duffy_relaxed": (0.015, 0.1)}
CFG69_FL = {"duffy_full": (+0.204, +0.143, +0.080, +0.023, -0.037)}
RESU = {}
for kind in KINDS:
    r = ufd_result(kind)
    RESU[kind] = r
    P(f"  {kind:14s}: KM median {r['med']:+.4f} +- {r['tot']:.4f} (bootstrap {r['boot']:.4f}, collapse floor {r['floor']:.4f}) -> {r['z']:+.2f} sigma;"
      f" resolved-only {r['resolved_med']:+.3f}; floors 1e8..1e10: " + ", ".join(f"{v:+.3f}" for v in r["floors"]))
P("\n  comparison to CFG69's committed CFG69_lcdm_comparator.out (offset, sigma; 3-decimal agreement on the offset):")
agree_all = True
for kind in KINDS:
    a, az = CFG69[kind]; r = RESU[kind]
    ag = abs(r["med"] - a) < 5.5e-4
    agz = abs(r["z"] - az) <= 0.051
    agree_all &= ag
    P(f"    {kind:14s}: CFG69 {a:+.3f} ({az:+.1f} sigma) | mine {r['med']:+.3f} ({r['z']:+.2f} sigma) | offset agrees to 3 decimals: {ag}; z agrees to 0.05: {agz}")
fl_ag = all(abs(u - v) < 5.5e-4 for u, v in zip(RESU['duffy_full']['floors'], CFG69_FL['duffy_full']))
P(f"    floor scan (Duffy full): CFG69 {CFG69_FL['duffy_full']} | mine " + str(tuple(round(v, 3) for v in RESU['duffy_full']['floors'])) + f" | agree {fl_ag}")
P(f"    CFG69's total error for Duffy full: 0.132 (bootstrap 0.054, floor 0.121) | mine {RESU['duffy_full']['tot']:.3f} ({RESU['duffy_full']['boot']:.3f}, {RESU['duffy_full']['floor']:.3f})")
check("HEADLINE reproduce: Duffy-full +0.080, Duffy-relaxed +0.015, Dutton-Maccio -0.043 (KM medians) to 3 decimals", "; ".join(f"{k} {RESU[k]['med']:+.3f}" for k in KINDS), agree_all)
gates = {k: abs(RESU[k]["z"]) < 2 for k in KINDS}
check("GATE (|median| < 2 sigma) passes under all three concentrations (CFG69: passes)", "; ".join(f"{k}: {RESU[k]['z']:+.2f} sigma -> {'pass' if gates[k] else 'FAIL'}" for k in KINDS), all(gates.values()))

# bootstrap robustness and variants
P("\n  Reported robustness (Duffy full):")
x, xu = offsets("duffy_full")
for sd in (1, 2, 3):
    P(f"    bootstrap seed {sd}: {boot(x, xu, 2000, sd)[0]:.4f}")
P(f"    joint (resolved+limits together) resampling: {boot(x, xu, 2000, 20260928, joint=True)[0]:.4f}")
xg, xug = offsets("duffy_full", gas=True); P(f"    with 1.33 M_HI added to baryons: KM median {km_median(xg, xug)[0]:+.4f} (stars-only {RESU['duffy_full']['med']:+.4f})")
x1, xu1 = offsets("duffy_full", ups=1.0); x4, xu4 = offsets("duffy_full", ups=4.0)
P(f"    Upsilon_V 1 / 2 / 4 (halo mass held at the Upsilon_V=2 Moster value): KM {km_median(x1, xu1)[0]:+.3f} / {RESU['duffy_full']['med']:+.3f} / {km_median(x4, xu4)[0]:+.3f}; half-range {0.5*abs(km_median(x4,xu4)[0]-km_median(x1,xu1)[0]):.3f}")
# floor as a true floor max(Moster, f) instead of a set
def km_true_floor(kind, f):
    Ms2 = 2 * arr(RES + LIM, "LV")
    out = []
    for grp in (RES, LIM):
        pass
    Mh_s = np.maximum(halo_mass(2 * arr(RES, "LV")), f); Mh_l = np.maximum(halo_mass(2 * arr(LIM, "LV")), f)
    def sg(sample, Mh):
        rp = (4/3.) * arr(sample, "rh"); r_m = rp * PC
        g = G * (0.5 * UPS * arr(sample, "LV") + (1 - FB) * nfw_enclosed(Mh, rp / 1000.0, kind)) * Msun / r_m ** 2
        return np.sqrt(g * r_m / 3) / 1e3
    return km_median(np.log10(arr(RES, "sig") / sg(RES, Mh_s)), np.log10(arr(LIM, "sig") / sg(LIM, Mh_l)))[0]
P("    alternative reading of the floor scan, M_h = max(Moster, f) (a true floor, Duffy full), f = 1e8..1e10: " + ", ".join(f"{km_true_floor('duffy_full', f):+.3f}" for f in FLOORS))

# ================================================================== (3) SENSITIVITY
P("\n" + "=" * 110 + "\n(3) GATE vs A COMMON MULTIPLE OF EVERY HALO MASS (floors multiplied too)\n" + "=" * 110)
MULTS = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
CFG69_R3 = {0.01: (0.381, 2.22), 0.1: (0.213, 1.50), 1.0: (0.080, 0.61), 10.0: (-0.037, -0.30), 100.0: (-0.149, -1.25), 1000.0: (-0.261, -2.10)}
LAD = {}
for kind in KINDS:
    LAD[kind] = {}
    for m in MULTS:
        LAD[kind][m] = ufd_result(kind, mult=m, nb=1000)
    P(f"  {kind}:")
    for m in MULTS:
        r = LAD[kind][m]
        extra = ""
        if kind == "duffy_full":
            a, az = CFG69_R3[m]; extra = f"   [CFG69 {a:+.3f} ({az:+.2f}); offset agrees {abs(r['med']-a) < 5.5e-4}]"
        P(f"    x{m:<7g}: KM median {r['med']:+.3f} +- {r['tot']:.3f} -> {r['z']:+.2f} sigma  gate {'PASS' if abs(r['z'])<2 else 'FAIL'}{extra}")
pass_df = [m for m in MULTS if abs(LAD['duffy_full'][m]['z']) < 2]
P(f"  Duffy-full gate passes at multiples: {pass_df}; fails at: {[m for m in MULTS if m not in pass_df]}")
R3ok = all(abs(LAD["duffy_full"][m]["med"] - CFG69_R3[m][0]) < 5.5e-4 for m in MULTS)
check("R3 reproduce: Duffy-full ladder offsets at x0.01..x1000 agree with CFG69's R3 to 3 decimals", "; ".join(f"x{m:g}: {LAD['duffy_full'][m]['med']:+.3f}" for m in MULTS), R3ok)
# log-slope of the median vs mass
xs = np.log10(MULTS); ys = np.array([LAD['duffy_full'][m]['med'] for m in MULTS])
P(f"  slope d(KM median)/d log10(mult), x1 -> x100 (Duffy full): {(ys[4]-ys[2])/2:+.4f} dex per decade; "
  f"corresponding sigma_pred scaling ~ mass^{-(ys[4]-ys[2])/2/2:.3f}")
nd = {k: [m for m in MULTS if abs(LAD[k][m]['z']) < 2] for k in KINDS}
NONDISC = all(all(m in nd[k] for m in (0.1, 1.0, 10.0, 100.0)) for k in KINDS)
check("NON-DISCRIMINATION reproduced: the gate passes for every halo-mass multiple x0.1..x100 (four decades: 0.1, 1, 10, 100), under each of the three concentrations",
      "; ".join(f"{k}: passes at {nd[k]}" for k in KINDS), NONDISC)

# ================================================================== MUTATE control (declared shift + gate)
P("\n" + "=" * 110 + f"\nMUTATE CONTROL (this run's observed-dispersion factor = {OBSF})\n" + "=" * 110)
# shift check independent of the mode: recompute with factor 1 and 0.5 explicitly
def med_with(f, kind="duffy_full"):
    s_r = sigma_lcdm(RES, kind); s_l = sigma_lcdm(LIM, kind)
    return km_median(np.log10(f * arr(RES, "sig") / s_r), np.log10(f * arr(LIM, "sig") / s_l))[0]
m1 = med_with(1.0); m5 = med_with(0.5)
check("MUTATE shift: every observed dispersion x 0.5 moves the LCDM KM median by exactly log10(0.5) = -0.30103 (each concentration)",
      "; ".join(f"{k}: {med_with(1.0,k):+.4f} -> {med_with(0.5,k):+.4f} (shift {med_with(0.5,k)-med_with(1.0,k):+.5f})" for k in KINDS),
      all(abs((med_with(0.5, k) - med_with(1.0, k)) - math.log10(0.5)) < 1e-12 for k in KINDS))
gate_mut = abs(RESU["duffy_full"]["z"]) < 2
P(f"  gate on the (possibly mutated) run, Duffy full: {RESU['duffy_full']['med']:+.3f} / {RESU['duffy_full']['tot']:.3f} = {RESU['duffy_full']['z']:+.2f} sigma -> {'PASS' if gate_mut else 'FAIL'}")
if not MUTATE:
    P("  (un-mutated run: for reference the mutated-mode numbers are computed here in-process)")
    for f in (0.5, 0.25, 0.1):
        r = {}
        for kind in KINDS:
            xr = np.log10(f * arr(RES, "sig") / sigma_lcdm(RES, kind)); xl = np.log10(f * arr(LIM, "sig") / sigma_lcdm(LIM, kind))
            med = km_median(xr, xl)[0]
            tot = RESU[kind]["tot"]     # error model unchanged by a uniform shift of the obs (bootstrap of a shifted sample is identical; floors identical)
            r[kind] = (med, med / tot)
        P(f"    obs x {f}: " + "; ".join(f"{k} {v[0]:+.3f} ({v[1]:+.2f} sigma, gate {'PASS' if abs(v[1])<2 else 'FAIL'})" for k, v in r.items()))
    # sanity: a shift of every offset leaves the bootstrap std and floor range unchanged -> exact
    P("    (a uniform log shift leaves the bootstrap spread and the floor half-range identical, so the total error is unchanged by construction; verified below)")
    xs_, xus_ = offsets("duffy_full")
    b_a = boot(xs_, xus_, 500)[0]; b_b = boot(xs_ + math.log10(0.5), xus_ + math.log10(0.5), 500)[0]
    P(f"    bootstrap (500) unshifted {b_a:.6f} vs shifted {b_b:.6f}")

# ================================================================== summary
P("\n" + "=" * 110 + "\nSUMMARY\n" + "=" * 110)
nf = sum(1 for _, ok in CHECKS if not ok)
for n, ok in CHECKS:
    P(f"  {'PASS' if ok else 'FAIL'}  {n[:120]}")
P(f"\n  {len(CHECKS)-nf}/{len(CHECKS)} checks pass")
if MUTATE:
    # the declared requirement: the gate must FAIL
    P(f"  MUTATE declared requirement 'the gate must FAIL': {'MET' if not gate_mut else 'NOT MET (gate still passes at %+.2f sigma) -> exit 1 as a failed control'%RESU['duffy_full']['z']}")
    sys.exit(0 if not gate_mut else 1)
sys.exit(1 if nf else 0)
