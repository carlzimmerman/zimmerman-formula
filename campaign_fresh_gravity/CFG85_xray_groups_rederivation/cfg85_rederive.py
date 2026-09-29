#!/usr/bin/env python3
r"""
CFG85 -- INDEPENDENT RE-DERIVATION of CFG81's headline (LCDM comparator for CFG34's X-ray groups).
FROZEN BEFORE ANY RUN.  Written from CFG81_FROZEN_CRITERIA.md, the CFG81 README, the CFG34 README/docstring, the h7 docstring, the
CFG4/CFG45 READMEs and the data file real_research/data/lovisari2015_groups.tsv.  CFG81's script, .out and _results.json were NOT
opened before this run.  Not used: any CFG34/CFG81 code (own implementation of everything).

QUESTION.  Through CFG34's pipeline (20 Lovisari+2015 groups, radii R2500 and R500, statistic = median over groups of
log10(M_HSE/M_model), the same floor), (a) does B (M_B = M_b + max(M_ph, 5.364 M_b)) show a 1.88x / 2.57 sigma shortfall at R2500 and
1.41x / 1.80 sigma at R500; (b) does a LCDM shape-design halo -- M_L(<r) = M_b(<r) + (1-f_b) M_NFW(<r; M_200c, c_Duffy-full-200c(M_200c)),
M_200c solved per group so M_L(<R500) = M500_HSE, every overdensity in the data's own critical density rho_c,g = 3 M500/(4 pi 500 R500^3),
f_b = 0.02237/0.14237, baryons = the lane's own -- reproduce M2500 (headline: ratio 1.05, +0.020 dex, +0.25 sigma); (c) what is B's
shape-only deficit (per-group log(M_HSE/M_B)@R2500 minus @R500: 1.37 sigma canonical, 1.79 alt)?
(d) SHARED CAVEAT: the lane's stars are 1.7e12 (M500_HSE/1e14)^0.6 (Kravtsov+2018), i.e. a function of the HYDROSTATIC M500 -> how do
B and LCDM change when the stars are varied +-0.2 dex or drawn independently of M500_HSE (as far as the data allow)?

MODEL AS I READ IT.
 B      : M_b(R500) = Mgas500 + M*500; M_b(R2500) = Mgas2500 + 0.65 M*500; M*500 = 1.7e12 (M500/1e14)^0.6 Msun (M500 in Msun, h70 units
          used as published); g_N = G M_b / r^2 (monopole); y = g_N/a0; nu = RAR kernel 1/(1-exp(-sqrt y)) [CFG45 README: equals nu_mono
          to 3e-9 for y<=0.1; I check y<=0.1 for every group/radius, else the substitution is declared invalid]; M_ph=(nu-1)M_b;
          M_B = M_b + max(M_ph, COSMIC M_b), COSMIC = 0.1200/0.02237.  a0 = 9.3603e-11 (canonical), 1.1312e-10 (alt) m/s^2.
          Constants CODATA (G=6.6743e-11, Msun=1.98847e30, kpc=3.0856776e19 m).
 stats  : per-group d = log10(M_HSE/M_model); med = median; err = std(d, ddof=1)/sqrt(20); star = 0.5|med(stars x1.5)-med(stars /1.5)|
          with the whole chain (incl. the LCDM R500 normalisation) re-run; HSE = log10 1.2; tot = sqrt(err^2+star^2+HSE^2); z=med/tot.
 LCDM   : NFW m(t)=ln(1+t)-t/(1+t); M_NFW(<r)=M_h m(c x)/m(c), x=r/R200 clipped [1e-4,5], R200=(3 M_h/(4 pi 200 rho_c,g))^(1/3);
          c = 5.71 (M_h/(2e12/0.674))^-0.084 (Duffy+08 full 200c z=0), M_h by brentq on [1e10,1e18].  Prediction at the MEASURED R2500.
 shape-only B: d(R2500)-d(R500) per group; med, err=std/sqrt20 of the difference, star = 0.5|bracket spread of median difference|, HSE 0.0792.
 variants (reported): V1 Dutton-Maccio c (log c = 0.905-0.101 log10(M/(1e12/h)), h=.674); V2 Duffy relaxed 200c (6.71 (M/(2e12/h))^-0.091);
          V3/V4 normalisation mass x1.2/x0.8 with R2500 still vs measured M2500; V3u/V4u M500 and M2500 both x1.2/x0.8; V5 total mass as ONE
          NFW no baryons (f_b->0, M_b->0); V6 rho_c = 3H^2/(8 pi G), H0=67.4 (in the R200 definition only, normalisation still at measured R500).
          rho_c,g in V3/V4/V3u/V4u = 3*(normalisation mass)/(4 pi 500 R500^3) [my reading; the unscaled-rho_c reading is reported as V3'/V4'].
 MUTATE=1: every LCDM concentration x0.1 (B untouched).  Expected: LCDM gate fails.

PASS LINES (each reported PASS / DIFF; DIFF is a valid outcome, no tuning afterwards).
 P1  B: R500 canonical 1.41, +0.150 dex, +1.80 sigma; alt 1.33, +0.124, +1.49.   R2500 canonical 1.88, +0.275, +2.57; alt 1.88, +0.274, +2.63.
     Floor terms R2500 (canonical) groups 0.017, stars 0.070, allowance 0.079.  Tolerance: ratio 0.01, dex 0.001, sigma 0.01.
 P2  LCDM base R2500: 1.05, +0.020 dex, +0.25 sigma (same tolerances); median c 4.42 (range 3.96-4.69); class SPECIFIC-TO-B on both footings
     (|z_L|<=2 while |z_B|>2).  R500 offset zero by construction.
 P3  B shape-only: +0.126 dex, +1.37 sigma (canonical); +0.161, +1.79 (alt).
 P4  MUTATE model (c x0.1) R2500: +0.265 dex, +3.30 sigma, median c 0.41 -> gate fails, i.e. the test discriminates.
 P5  variants V1..V6 within tolerance of CFG81's table (V1 -0.008/-0.10, V2 +0.002/+0.02, V3 -0.044/-0.55, V4 +0.100/+1.23,
     V3u +0.035/+0.43, V4u +0.003/+0.04, V5 +0.011/+0.14, V6 +0.025/+0.31).
 P6  CIRCULARITY (own test; no target numbers): stars x10^{+-0.2}; stars=0; stars permuted across groups (independent of own M500,
     500 draws); stars = Kravtsov(M500) x 10^N(0,0.2) per-group scatter (500 draws).  Report B z and LCDM z, and whether classes change.
     Pass rule for 'robust': LCDM |z|<=2 and B |z|>2 in every stellar variation (both footings for B).  The data have no independent stellar
     mass (Lovisari tabulates none); a fully independent draw is impossible, the permutation and scatter draws are the closest available.
CONTROLS (a failed control is a failure)
 C1 data read: 20 groups, R500/R2500 finite; rho_c implied by (M500,R500) vs (M2500,R2500) agree to 2% per group (rho_c,g convention).
 C2 NFW engine: M(<R200)=M_h to 1e-12 (M_h=1e12..1e15, three c relations); M_NFW(<r) equals numerical integral of the NFW density to 1e-7;
    mean NFW density within r_Delta from the fixed-point (m(c x)/m(c) = (Delta/200) x^3) equals Delta rho_c to 1e-9 for 500 and 2500.
 C3 closed-form limits: (i) B with nu=1 gives M_B/M_b = 1+COSMIC exactly; (ii) LCDM with f_b=0, no baryons is a single NFW: its M(<R2500)/M(<R500)
    equals the closed form m(c x2500)/m(c x500); (iii) SYNTHETIC CLOSURE: groups generated from the LCDM model itself (Duffy c, same baryons,
    M2500 := M_L(<R2500)) return offset 0 to 1e-9 -- fails under MUTATE (mutated model vs Duffy-generated data) by construction of the test;
    (iv) synthetic B closure: M_HSE := M_B returns B offset 0.
 C4 normalisation: |M_L(<R500)/target - 1| < 1e-9 for all groups in every LCDM run (base, bracket ends, variants, MUTATE).
 C5 c used equals c_Duffy_full(M_h) x (0.1 if MUTATE) to 1e-12 (self-consistency); y<=0.1 everywhere for B (kernel substitution valid).
 MUTATE: exit 1 expected through C3(iii) (and the P4 gate).  Main run exit 1 only on a failed control.
Run: python3 cfg85_rederive.py ; MUTATE=1 python3 cfg85_rederive.py
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

MUTATE = os.environ.get("MUTATE", "0") == "1"
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/lovisari2015_groups.tsv"
OUT = []
def P(s=""):
    print(s); OUT.append(s)
fails = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")
    if not ok: fails.append(name)

G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
COSMIC = 0.1200 / 0.02237
FB = 0.02237 / (0.02237 + 0.1200)
HSE = math.log10(1.2)
H = 0.674
CMUT = 0.1 if MUTATE else 1.0

# ------------------------------------------------------------------ data
rows = []
for l in open(DATA):
    if l.startswith("#") or l.startswith("name") or not l.strip(): continue
    f = l.rstrip("\n").split("\t")
    rows.append(f)
names = [r[0] for r in rows]
def col(i): return np.array([float(r[i]) for r in rows])
M500 = col(6) * 1e13; R500 = col(4); Mg500 = col(8) * 1e12
R2500 = col(10); M2500 = col(12) * 1e13; Mg2500 = col(14) * 1e12
N = len(names)
def mstar500(M): return 1.7e12 * (M / 1e14) ** 0.6
STAR = mstar500(M500)   # Msun
FIN = 0.65

# ------------------------------------------------------------------ B
def nu_rar(y): return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def MB(Mb, r_kpc, a0, nu_on=True):
    g = G * Mb * MSUN / (r_kpc * KPC) ** 2
    y = g / a0
    if not nu_on: return Mb * (1 + COSMIC), y
    Mph = (nu_rar(y) - 1.0) * Mb
    return Mb + np.maximum(Mph, COSMIC * Mb), y

def stat(d, extra_star=None):
    med = float(np.median(d)); err = float(np.std(d, ddof=1) / math.sqrt(len(d)))
    return med, err

def B_d(stars_fac_array, a0):
    """returns d500, d2500 arrays and max y"""
    st = STAR * stars_fac_array
    Mb5 = Mg500 + st; Mb25 = Mg2500 + FIN * st
    MB5, y5 = MB(Mb5, R500, a0); MB25, y25 = MB(Mb25, R2500, a0)
    return np.log10(M500 / MB5), np.log10(M2500 / MB25), max(y5.max(), y25.max()), MB5, MB25

def full_stat(fn):
    """fn(fac) -> d array (fac: stellar multiplier scalar or array); returns dict with med, err, star, tot, z"""
    d0 = fn(1.0); d_hi = fn(1.5); d_lo = fn(1 / 1.5)
    med, err = stat(d0); star = 0.5 * abs(np.median(d_hi) - np.median(d_lo))
    tot = math.sqrt(err ** 2 + star ** 2 + HSE ** 2)
    return dict(med=med, err=err, star=star, tot=tot, z=med / tot, ratio=10 ** med)

# ------------------------------------------------------------------ NFW / LCDM
def m_nfw(t): return np.log(1 + t) - t / (1 + t)
def c_duffy_full(M): return 5.71 * (M / (2e12 / H)) ** -0.084
def c_duffy_relaxed(M): return 6.71 * (M / (2e12 / H)) ** -0.091
def c_dm(M): return 10 ** (0.905 - 0.101 * np.log10(M / (1e12 / H)))
def nfw_M(r_mpc, Mh, c, rhoc):
    R200 = (3 * Mh / (4 * math.pi * 200 * rhoc)) ** (1 / 3)
    x = np.clip(r_mpc / R200, 1e-4, 5.0)
    return Mh * m_nfw(c * x) / m_nfw(c)
RHO_C_V6 = 3 * (67.4e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * G) * (3.0856775814913673e22) ** 3 / MSUN  # Msun/Mpc^3

def lcdm_solve(i, target, cfun, rhoc, fb, Mb5, Mb25, Mh_lo=1e10, Mh_hi=1e18, cmul=None):
    """solve M_h so M_L(<R500)=target; return Mh, c, M_L(<R2500), M_L(<R500)"""
    cm = CMUT if cmul is None else cmul
    r5 = R500[i] / 1e3; r25 = R2500[i] / 1e3
    def f(lm):
        Mh = 10 ** lm
        return Mb5[i] + (1 - fb) * nfw_M(r5, Mh, cm * cfun(Mh), rhoc) - target
    lo, hi = math.log10(Mh_lo), math.log10(Mh_hi)
    assert f(lo) * f(hi) < 0, ("no sign change", names[i])
    lm = brentq(f, lo, hi, xtol=1e-14, rtol=1e-14, maxiter=500)
    Mh = 10 ** lm; c = cm * cfun(Mh)
    ML5 = Mb5[i] + (1 - fb) * nfw_M(r5, Mh, c, rhoc)
    ML25 = Mb25[i] + (1 - fb) * nfw_M(r25, Mh, c, rhoc)
    return Mh, c, ML25, ML5

def rho_g(Mnorm):  # Msun/Mpc^3, data-defined critical density from the normalisation mass at R500
    return 3 * Mnorm / (4 * math.pi * 500 * (R500 / 1e3) ** 3)

def lcdm_run(fac=1.0, cfun=c_duffy_full, fb=FB, norm_fac=1.0, m2500_fac=1.0, rho_mode="g", stars_arr=None, baryons=True, cmul=None):
    st = (STAR * fac if stars_arr is None else stars_arr * fac)
    Mb5 = (Mg500 + st) if baryons else np.zeros(N)
    Mb25 = (Mg2500 + FIN * st) if baryons else np.zeros(N)
    tgt = M500 * norm_fac
    rc = rho_g(tgt) if rho_mode == "g" else (rho_g(M500) if rho_mode == "g0" else np.full(N, RHO_C_V6))
    d25 = np.zeros(N); d5 = np.zeros(N); Mh = np.zeros(N); cc = np.zeros(N); ML25a = np.zeros(N); maxdev = 0.0
    for i in range(N):
        Mh[i], cc[i], ML25a[i], ML5 = lcdm_solve(i, tgt[i], cfun, rc[i], fb, Mb5, Mb25, cmul=cmul)
        maxdev = max(maxdev, abs(ML5 / tgt[i] - 1))
        d25[i] = math.log10(M2500[i] * m2500_fac / ML25a[i])
        d5[i] = math.log10(M500[i] * norm_fac / ML5) if m2500_fac != 1.0 or norm_fac != 1.0 else math.log10(M500[i] / ML5)
    return d25, d5, Mh, cc, maxdev, ML25a

def L_stat(**kw):
    """full statistic at R2500 with the stellar bracket re-run (whole chain)"""
    devs = []
    def fn(fac):
        d25, d5, Mh, cc, md, ML = lcdm_run(fac=fac, **kw); devs.append(md); return d25
    res = full_stat(fn)
    res["maxdev"] = max(devs)
    d25, d5, Mh, cc, md, ML = lcdm_run(fac=1.0, **kw)
    res.update(cmed=float(np.median(cc)), cmin=float(cc.min()), cmax=float(cc.max()), d25=d25, d5=d5, Mh=Mh, c=cc, ML25=ML)
    return res

def cls(zB, zL):
    if abs(zB) <= 1: return "B-ok"
    if abs(zL) <= 2: return "SPECIFIC-TO-B"
    return "SHARED" if zL * zB > 0 else "LCDM-WORSE"

def fmt(r): return f"{r['ratio']:.2f} ({r['med']:+.3f} dex) err {r['err']:.3f} star {r['star']:.3f} tot {r['tot']:.3f} -> z {r['z']:+.2f}"

def near(a, b, tol): return abs(a - b) <= tol + 1e-12
tally = []
def P_line(name, mine, theirs, tol, fmtstr="{:+.3f}"):
    ok = near(mine, theirs, tol)
    tally.append((name, mine, theirs, ok))
    P(f"  [{'MATCH' if ok else 'DIFF '}] {name}: mine {fmtstr.format(mine)}  target {fmtstr.format(theirs)}  (tol {tol})")

P(__doc__.split("Run: python3")[0].strip()); P()
P("=" * 100); P(f"CFG85 run   MUTATE={MUTATE}   N={N}   FB={FB:.5f}   COSMIC={COSMIC:.4f}   RHO_C(V6)={RHO_C_V6:.4e}"); P("=" * 100)

# ------------------------------------------------------------------ C1
P("\nC1 data / rho_c convention")
rho5 = 3 * M500 / (4 * math.pi * 500 * (R500 / 1e3) ** 3); rho25 = 3 * M2500 / (4 * math.pi * 2500 * (R2500 / 1e3) ** 3)
dev = np.abs(rho25 / rho5 - 1)
check("C1a 20 groups read, all finite", N == 20 and np.all(np.isfinite([M500, R500, Mg500, R2500, M2500, Mg2500])), f"N={N}")
check("C1b rho_c implied at R500 and R2500 agree to 2% per group", dev.max() < 0.02, f"max dev {dev.max():.4f}")
P(f"      rho_c,g / RHO_C(H0=67.4): min {rho5.min()/RHO_C_V6:.3f} median {np.median(rho5)/RHO_C_V6:.3f} max {rho5.max()/RHO_C_V6:.3f}")

# ------------------------------------------------------------------ B
P("\nB (candidate B, own implementation)")
BR = {}
ymax = 0
for foot, a0 in A0.items():
    r5 = full_stat(lambda f: B_d(f, a0)[0]); r25 = full_stat(lambda f: B_d(f, a0)[1])
    d5, d25, ym, MB5, MB25 = B_d(1.0, a0)
    ymax = max(ymax, ym)
    Mb5 = Mg500 + STAR; Mb25 = Mg2500 + FIN * STAR
    _, y5 = MB(Mb5, R500, a0); _, y25 = MB(Mb25, R2500, a0)
    ph5 = int(np.sum((nu_rar(y5) - 1) * Mb5 > COSMIC * Mb5)); ph25 = int(np.sum((nu_rar(y25) - 1) * Mb25 > COSMIC * Mb25))
    # shape-only
    def sh(fac): a, b, *_ = B_d(fac, a0); return b - a
    rs = full_stat(sh)
    BR[foot] = dict(r5=r5, r25=r25, shape=rs, d5=d5, d25=d25, ph5=ph5, ph25=ph25)
    P(f"  {foot:10s} R500 : {fmt(r5)}   phantom wins {ph5}/20   (y max {y5.max():.3f})")
    P(f"  {foot:10s} R2500: {fmt(r25)}   phantom wins {ph25}/20   (y max {y25.max():.3f})")
    P(f"  {foot:10s} SHAPE-ONLY (R2500-R500): {fmt(rs)}")
check("C5a kernel substitution valid: y <= 0.1 at every group/radius (B, both footings)", ymax <= 0.1, f"y max {ymax:.4f}")
P("\nP1 (B numbers)")
for foot, tg in (("canonical", dict(r5=(1.41, .150, 1.80), r25=(1.88, .275, 2.57))), ("alt", dict(r5=(1.33, .124, 1.49), r25=(1.88, .274, 2.63)))):
    for k in ("r5", "r25"):
        r = BR[foot][k]
        P_line(f"B {foot} {k} ratio", r["ratio"], tg[k][0], 0.01, "{:.2f}")
        P_line(f"B {foot} {k} dex", r["med"], tg[k][1], 0.001)
        P_line(f"B {foot} {k} sigma", r["z"], tg[k][2], 0.01, "{:+.2f}")
r = BR["canonical"]["r25"]
P_line("B canonical R2500 err (groups)", r["err"], 0.017, 0.0006, "{:.4f}"); P_line("B canonical R2500 star", r["star"], 0.070, 0.0006, "{:.4f}")
P_line("B canonical R500 err", BR["canonical"]["r5"]["err"], 0.014, 0.0006, "{:.4f}")
P("\nP3 (B shape-only)")
P_line("B shape canonical dex", BR["canonical"]["shape"]["med"], 0.126, 0.001); P_line("B shape canonical sigma", BR["canonical"]["shape"]["z"], 1.37, 0.01, "{:+.2f}")
P_line("B shape alt dex", BR["alt"]["shape"]["med"], 0.161, 0.001); P_line("B shape alt sigma", BR["alt"]["shape"]["z"], 1.79, 0.01, "{:+.2f}")

# ------------------------------------------------------------------ C2 NFW engine
P("\nC2 NFW engine")
worst = 0
for cf in (c_duffy_full, c_duffy_relaxed, c_dm):
    for Mh in (1e12, 1e13, 1e14, 1e15):
        rc = 1.36e11; R200 = (3 * Mh / (4 * math.pi * 200 * rc)) ** (1 / 3)
        worst = max(worst, abs(nfw_M(R200, Mh, cf(Mh), rc) / Mh - 1))
check("C2a M_NFW(<R200)=M_h to 1e-12", worst < 1e-12, f"max {worst:.2e}")
worst = 0
for Mh, c, r in [(1e13, 4.4, 0.2), (1e13, 4.4, 0.5), (1e14, 4.0, 0.3), (1e14, 4.0, 1.0), (1e12, 5.5, 0.15)]:
    rc = 1.36e11; R200 = (3 * Mh / (4 * math.pi * 200 * rc)) ** (1 / 3)
    rho0 = Mh / (4 * math.pi * R200 ** 3 / c ** 3 * m_nfw(c)) # rho_s * ... NFW: M(<r)=4 pi rho_s rs^3 m ; rs=R200/c
    rs = R200 / c; rhos = Mh / (4 * math.pi * rs ** 3 * m_nfw(c))
    num = quad(lambda q: 4 * math.pi * q * q * rhos / ((q / rs) * (1 + q / rs) ** 2), 0, r, epsabs=0, epsrel=1e-13)[0]
    worst = max(worst, abs(num / nfw_M(r, Mh, c, rc) - 1))
check("C2b M_NFW(<r) = numerical integral of NFW density to 1e-7", worst < 1e-7, f"max {worst:.2e}")
worst = 0
for Mh in (1e12, 1e13, 1e14, 1e15):
    for cf in (c_duffy_full, c_dm, c_duffy_relaxed):
        c = cf(Mh); rc = 1.36e11; R200 = (3 * Mh / (4 * math.pi * 200 * rc)) ** (1 / 3)
        for Dl in (500, 2500):
            x = 1.0
            for _ in range(200):
                xn = ((Dl / 200) ** -1 * m_nfw(c * x) / m_nfw(c)) ** (1 / 3)   # m(cx)/m(c) = (D/200) x^3  -> x = (m(cx)/m(c) * 200/D)^(1/3)
                if abs(xn - x) < 1e-16: x = xn; break
                x = xn
            rD = x * R200; MD = Mh * m_nfw(c * x) / m_nfw(c)
            worst = max(worst, abs(3 * MD / (4 * math.pi * rD ** 3) / (Dl * rc) - 1))
check("C2c fixed-point r_Delta gives mean density Delta rho_c to 1e-9 (500, 2500)", worst < 1e-9, f"max {worst:.2e}")

# ------------------------------------------------------------------ LCDM
P("\nLCDM shape design (base)")
base = L_stat(); ALLDEV = [base["maxdev"]]
P(f"  R2500: {fmt(base)}")
P(f"  M_200c range {base['Mh'].min():.2e}-{base['Mh'].max():.2e}; c median {base['cmed']:.2f} (range {base['cmin']:.2f}-{base['cmax']:.2f})")
zc = {f: cls(BR[f]["r25"]["z"], base["z"]) for f in A0}
P(f"  class per footing: {zc}")
P(f"  per-group R500 offset max |d| = {np.max(np.abs(base['d5'])):.2e}")
P("\nP2")
P_line("LCDM base ratio", base["ratio"], 1.05, 0.01, "{:.2f}"); P_line("LCDM base dex", base["med"], 0.020, 0.001); P_line("LCDM base sigma", base["z"], 0.25, 0.01, "{:+.2f}")
P_line("LCDM c median", base["cmed"], 4.42, 0.005, "{:.2f}"); P_line("LCDM c min", base["cmin"], 3.96, 0.005, "{:.2f}"); P_line("LCDM c max", base["cmax"], 4.69, 0.005, "{:.2f}")
P_line("LCDM err", base["err"], 0.016, 0.0006, "{:.4f}"); P_line("LCDM star", base["star"], 0.003, 0.0006, "{:.4f}")
# C5
cexp = CMUT * c_duffy_full(base["Mh"])
check("C5b c used equals c_Duffy_full(M_h) (x0.1 if MUTATE) to 1e-12", np.max(np.abs(base["c"] / cexp - 1)) < 1e-12, f"max {np.max(np.abs(base['c']/cexp-1)):.1e}")
check("C5c c used equals UNMUTATED Duffy c at solved M_h [mutation detector; must fail under MUTATE]",
      np.max(np.abs(base["c"] / c_duffy_full(base["Mh"]) - 1)) < 1e-12)

# RM: mutated model inside main run
rm = L_stat(cmul=0.1) if not MUTATE else base
ALLDEV.append(rm["maxdev"])
P(f"\nRM (every c x0.1): {fmt(rm)}   c median {rm['cmed']:.2f}   gate |z|<2: {'PASS' if abs(rm['z'])<2 else 'FAIL'}")
P("P4"); P_line("RM dex", rm["med"], 0.265, 0.001); P_line("RM sigma", rm["z"], 3.30, 0.01, "{:+.2f}"); P_line("RM c median", rm["cmed"], 0.41, 0.005, "{:.2f}")
flip = (abs(base["z"]) < 2) != (abs(rm["z"]) < 2)
P(f"  MUTATE flips the gate outcome (base vs RM): {flip} -> {'informative' if flip else 'NON-DISCRIMINATING'}")

# variants
P("\nP5 variants at R2500")
VAR = {}
def runvar(name, target, **kw):
    r = L_stat(**kw); ALLDEV.append(r["maxdev"]); VAR[name] = r
    P_line(f"{name} dex", r["med"], target[0], 0.001); P_line(f"{name} sigma", r["z"], target[1], 0.01, "{:+.2f}")
    P(f"      class {cls(BR['canonical']['r25']['z'], r['z'])}/{cls(BR['alt']['r25']['z'], r['z'])}   c median {r['cmed']:.2f}")
runvar("V1 DM14 c", (-0.008, -0.10), cfun=c_dm)
runvar("V2 Duffy relaxed", (0.002, 0.02), cfun=c_duffy_relaxed)
runvar("V3 norm x1.2", (-0.044, -0.55), norm_fac=1.2)
runvar("V4 norm x0.8", (0.100, 1.23), norm_fac=0.8)
runvar("V3u M500&M2500 x1.2", (0.035, 0.43), norm_fac=1.2, m2500_fac=1.2)
runvar("V4u M500&M2500 x0.8", (0.003, 0.04), norm_fac=0.8, m2500_fac=0.8)
runvar("V5 one NFW no baryons", (0.011, 0.14), fb=0.0, baryons=False)
runvar("V6 RHO_C(67.4)", (0.025, 0.31), rho_mode="c")
for nm, kw in (("V3' norm x1.2, unscaled rho_c,g", dict(norm_fac=1.2, rho_mode="g0")), ("V4' norm x0.8, unscaled rho_c,g", dict(norm_fac=0.8, rho_mode="g0"))):
    r = L_stat(**kw); ALLDEV.append(r["maxdev"]); P(f"  {nm}: {r['med']:+.3f} dex  z {r['z']:+.2f}  (own reading alternative)")
# R6 : allowance removed
def noHSE(r): return r["med"] / math.sqrt(r["err"] ** 2 + r["star"] ** 2)
P(f"  R6-like (allowance removed both sides): LCDM z {noHSE(base):+.2f}; B canonical {noHSE(BR['canonical']['r25']):+.2f}; alt {noHSE(BR['alt']['r25']):+.2f}")

# R5 implied concentration
def c_implied(i):
    r5 = R500[i] / 1e3; r25 = R2500[i] / 1e3; rc = rho_g(M500)[i]
    target = M2500[i] / M500[i]
    # single NFW with M(<R500)=M500: ratio M(<R2500)/M(<R500) = m(c x25)/m(c x5) with x = r/R200 ; R200 from M_200 in terms of c: R200^3 ∝ M500 * (200/500)... solve via fixed x5/200 relation
    def ratio(c):
        # find x5 = R500/R200 with m(c x5)/m(c) = (500/200) x5^3 -> mean density in x5 is 500 rho_c
        # NFW: R500 is defined by data; the NFW's r_500/R200 = x5 solves m(c x)/m(c) = (500/200) x^3
        x5 = brentq(lambda x: m_nfw(c * x) / m_nfw(c) - 2.5 * x ** 3, 1e-4, 1.0, xtol=1e-14)
        x25 = x5 * r25 / r5
        return m_nfw(c * x25) / m_nfw(c * x5)
    f = lambda c: ratio(c) - target
    try:
        return brentq(f, 0.3, 60, xtol=1e-10)
    except ValueError:
        return float("nan")
ci = np.array([c_implied(i) for i in range(N)]); ok = np.isfinite(ci)
# Duffy c at the M_200c of that implied NFW
cD = []
for i in range(N):
    if not ok[i]: cD.append(float("nan")); continue
    c = ci[i]; x5 = brentq(lambda x: m_nfw(c * x) / m_nfw(c) - 2.5 * x ** 3, 1e-4, 1.0, xtol=1e-14)
    R200 = (R500[i] / 1e3) / x5; M200 = 200 * (4 * math.pi / 3) * rho_g(M500)[i] * R200 ** 3
    cD.append(c_duffy_full(M200))
cD = np.array(cD)
P(f"\nR5 implied c of a single total-mass NFW: median {np.nanmedian(ci):.2f} (range {np.nanmin(ci):.2f}-{np.nanmax(ci):.2f}); solved {ok.sum()}/20; Duffy at same M200 median {np.nanmedian(cD):.2f}; {int(np.nansum(ci>cD))}/20 above Duffy")

# ------------------------------------------------------------------ C3 closed forms
P("\nC3 closed-form limits and synthetic closure")
Mb_test = 3.3e12; a0 = A0["canonical"]
# (i) nu=1
mb_, _ = MB(np.array([Mb_test]), np.array([400.0]), a0, nu_on=False)
check("C3i B with nu=1: M_B/M_b = 1+COSMIC exactly", abs(mb_[0] / Mb_test - (1 + COSMIC)) < 1e-14)
# (ii) single NFW closed form
worst = 0
for i in range(N):
    Mh, c, ML25, ML5 = lcdm_solve(i, M500[i], c_duffy_full, rho_g(M500)[i], 0.0, np.zeros(N), np.zeros(N), cmul=1.0)
    rc = rho_g(M500)[i]; R200 = (3 * Mh / (4 * math.pi * 200 * rc)) ** (1 / 3)
    x5 = R500[i] / 1e3 / R200; x25 = R2500[i] / 1e3 / R200
    cf = c_duffy_full(Mh)
    worst = max(worst, abs(ML25 / ML5 - m_nfw(cf * x25) / m_nfw(cf * x5)))
check("C3ii single NFW (f_b=0, no baryons): M(<R2500)/M(<R500)=m(c x2500)/m(c x500)", worst < 1e-12, f"max {worst:.1e}")
# (iii) synthetic closure: data generated from the unmutated Duffy model; recovered by model with CMUT
Mb5 = Mg500 + STAR; Mb25 = Mg2500 + FIN * STAR
syn_d = []
Mh_l = []
for i in range(N):
    Mh, c, ML25, ML5 = lcdm_solve(i, M500[i], c_duffy_full, rho_g(M500)[i], FB, Mb5, Mb25, cmul=1.0)
    ML25_syn = ML25
    Mh2, c2, ML25b, ML5b = lcdm_solve(i, M500[i], c_duffy_full, rho_g(M500)[i], FB, Mb5, Mb25)  # with CMUT
    syn_d.append(math.log10(ML25_syn / ML25b))
check("C3iii synthetic closure: Duffy-generated M2500 recovered by the model in use (offset 0 to 1e-9) [fails under MUTATE]", np.max(np.abs(syn_d)) < 1e-9, f"max |offset| {np.max(np.abs(syn_d)):.2e}")
P(f"      synthetic-data offset by the model in use: median {np.median(syn_d):+.4f} dex")
# (iv) B synthetic closure
mb_arr, _ = MB(Mb5, R500, a0)
check("C3iv B synthetic closure: M_HSE:=M_B gives offset 0", np.max(np.abs(np.log10(mb_arr / mb_arr))) == 0)
check("C4 normalisation at R500 (all LCDM runs)", max(ALLDEV) < 1e-9, f"max {max(ALLDEV):.1e}")

# ------------------------------------------------------------------ P6 circularity
P("\nP6 CIRCULARITY: stars varied / decoupled from M500_HSE")
P("  Note: Lovisari tabulates no stellar mass; kT, R500, Mgas are all tied to HSE. A fully independent stellar mass is NOT available from the data.")
def both(stars_arr, label, fac_arr_for_B=None):
    out = {}
    sf = stars_arr / STAR
    for foot, a0 in A0.items():
        out[foot] = full_stat(lambda f: B_d(sf * f, a0)[1])
        out[foot + "5"] = full_stat(lambda f: B_d(sf * f, a0)[0])
    L = L_stat(stars_arr=stars_arr)
    return out, L
def show(label, out, L):
    zb = out["canonical"]["z"]; za = out["alt"]["z"]
    P(f"  {label:34s} B R2500 z {zb:+.2f}/{za:+.2f} ({out['canonical']['med']:+.3f}/{out['alt']['med']:+.3f} dex) | B R500 z {out['canonical5']['z']:+.2f}/{out['alt5']['z']:+.2f} | LCDM R2500 {L['med']:+.3f} dex z {L['z']:+.2f}  class {cls(zb, L['z'])}/{cls(za, L['z'])}")
robust = True
CIRC = {}
for label, mult in (("stars x10^+0.2", 10 ** 0.2), ("stars x10^-0.2", 10 ** -0.2), ("stars x10^+0.5", 10 ** 0.5), ("stars x10^-0.5", 10 ** -0.5)):
    o, L = both(STAR * mult, label); ALLDEV.append(L["maxdev"]); show(label, o, L)
    CIRC[label] = (o["canonical"]["z"], o["alt"]["z"], L["z"])
    if label.endswith("0.2"): robust &= (abs(L["z"]) <= 2 and o["canonical"]["z"] > 2 and o["alt"]["z"] > 2)
# stars=0 (gas-only baryons), B evaluated with tiny stars
o, L = both(STAR * 1e-9, "stars=0"); ALLDEV.append(L["maxdev"]); show("stars ~0 (gas only)", o, L)
rng = np.random.default_rng(85)
NMC = 500
res_perm = []; res_sc = []
for k in range(NMC):
    perm = STAR[rng.permutation(N)]
    o, L = both(perm, "perm"); res_perm.append((o["canonical"]["z"], o["alt"]["z"], L["z"], L["med"], o["canonical"]["med"]))
    sc = STAR * 10 ** rng.normal(0, 0.2, N)
    o, L = both(sc, "sc"); res_sc.append((o["canonical"]["z"], o["alt"]["z"], L["z"], L["med"], o["canonical"]["med"]))
for label, arr in (("permuted across groups", np.array(res_perm)), ("Kravtsov x10^N(0,0.2) per group", np.array(res_sc))):
    q = lambda j: np.percentile(arr[:, j], [16, 50, 84])
    P(f"  {label:34s} ({NMC} draws)  B z canon {q(0)[1]:+.2f} [{q(0)[0]:+.2f},{q(0)[2]:+.2f}]  alt {q(1)[1]:+.2f} [{q(1)[0]:+.2f},{q(1)[2]:+.2f}]  |  LCDM z {q(2)[1]:+.2f} [{q(2)[0]:+.2f},{q(2)[2]:+.2f}]  LCDM dex {q(3)[1]:+.3f}")
    frac_spec = np.mean((np.abs(arr[:, 2]) <= 2) & (arr[:, 0] > 2) & (arr[:, 1] > 2))
    P(f"      fraction of draws with LCDM |z|<=2 AND both B z>2 (SPECIFIC-TO-B robust): {frac_spec:.3f}; B canon z>2 in {np.mean(arr[:,0]>2):.3f}, LCDM |z|<=2 in {np.mean(np.abs(arr[:,2])<=2):.3f}")
    CIRC[label] = frac_spec
P(f"  robust in +-0.2 dex uniform shifts (LCDM |z|<=2 and both B>2): {robust}")
# leave-out sensitivities: derivative of LCDM offset wrt stellar normalisation
P("  d(LCDM offset)/d(log10 stars): " + ", ".join(f"{lab}: {L_stat(stars_arr=STAR*m)['med']:+.4f}" for lab, m in (("x0.316", 10**-0.5), ("x1", 1.0), ("x3.16", 10**0.5))))
check("C4b normalisation held in every stellar variation", max(ALLDEV) < 1e-9, f"max {max(ALLDEV):.1e}")

# ------------------------------------------------------------------ summary
P("\nSUMMARY of P-lines: " + f"{sum(t[3] for t in tally)}/{len(tally)} MATCH")
for t in tally:
    if not t[3]: P(f"   DIFF: {t[0]}: mine {t[1]:+.4f} target {t[2]:+.4f}")
P(f"\nCONTROLS FAILED: {fails if fails else 'none'}")
suf = "_MUTATE" if MUTATE else ""
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, f"cfg85{suf}.out"), "w").write("\n".join(OUT))
json.dump(dict(mutate=MUTATE, B={f: {k: {kk: vv for kk, vv in BR[f][k].items()} for k in ("r5", "r25", "shape")} for f in A0},
               lcdm=dict(base={k: v for k, v in base.items() if not isinstance(v, np.ndarray)}, rm={k: v for k, v in rm.items() if not isinstance(v, np.ndarray)}),
               variants={k: {kk: vv for kk, vv in v.items() if not isinstance(vv, np.ndarray)} for k, v in VAR.items()},
               fails=fails, tally=[(a, float(b), float(c), bool(d)) for a, b, c, d in tally]),
          open(os.path.join(here, f"cfg85{suf}_results.json"), "w"), indent=1, default=float)
sys.exit(1 if fails else 0)
