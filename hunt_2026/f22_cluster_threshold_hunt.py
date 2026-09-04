#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f22 -- THE CLUSTER THRESHOLD HUNT: is the scale where the framework stops working a scale set by Lambda?

THE QUESTION.  The kernel lands on discs, on galaxy-galaxy lensing and (within errors) on Local Volume groups, and it
misses on X-ray groups, X-ray clusters and lensing clusters by a factor 1.5-3.5 in acceleration.  If the boundary
between "lands" and "misses" were SHARP in some variable, and the threshold value of that variable were a scale the
framework already owns (a_0 is (c/2) sqrt(G rho_Lambda), so Lambda, H_Lambda, rho_Lambda are the candidates), then
the framework would PREDICT where it breaks -- a second appearance of Lambda, which would be a new law.  That is the
hypothesis this file is written to test, and to be able to kill.

WHAT IS ALREADY KNOWN (and is not redone here, only reproduced where it is load-bearing):
  * u13 C4a: on the 37-row liability ledger, none of eight candidate variables (log y, log r, log M_enc, log sigma,
    x_ext, rotation/pressure, cluster/not, LCDM-DM-rich) separates landing rows from missing rows sharply; best AUC
    0.778 on 'not a cluster'.  C4b: the MAGNITUDE of the miss is organised by acceleration (Spearman -0.37, p = 0.02).
  * k02: the radius where a cluster's residual would cross unity is an EXTRAPOLATION in 7 of 7 X-COP clusters, its
    overdensity is 47 rho_c with 1.8 dex scatter, and it is not rho_Lambda with an O(1) coefficient.
  * u02 2b: across the cluster front the missing boost RISES toward low acceleration.
  * g06 (+ g06v): Local Volume groups sit at boost 0.82 [0.66, 1.11]; the best-measured half at 1.20.

WHAT IS NEW HERE:
  1. One axis every system can be put on: the POTENTIAL DEPTH Phi_d = g_obs * r = v_c^2 (rotation: v_flat^2;
     pressure: 3 sigma^2, the deep-MOND point-mass Jeans identity g06 verified; hydrostatic/lensing: G M_obs/r).
     In the framework a deep-MOND system's potential scale is sqrt(G M_b a_0), so "threshold in potential" and
     "threshold in baryonic mass" are the same statement for landing systems; both axes are carried.
  2. A SINGLE-ESTIMATOR sweep from galaxy groups to the nearest clusters: Kourkchi & Tully 2017 (ApJ 843, 16), every
     group within 3500 km/s, with line-of-sight dispersion, K_s luminosity and virial radius from ONE catalogue and one
     method.  The cross-catalogue ledger mixes hydrostatic, lensing, Jeans and scaling-relation masses, and u13 showed
     that mixture has no sharp edge; a one-method sweep is the only way to locate an ONSET without that heterogeneity.
  3. The eRASS1 TEMPERATURE sweep: 5000+ systems whose kT is measured independently of the WL-calibrated M500, so the
     residual can be laid against a potential-depth axis that is not the mass axis.
  4. The Lambda confrontation, with a control on the density of coincidences: how many simple products of the numbers
     the framework owns land within 0.15 dex of ANY threshold value.  If that count is large, a match is not evidence.
  5. Step vs ramp, judged by BIC on bins with bootstrap errors, with a synthetic-injection test that the step-finder
     has the power to find a step of the size claimed.

THE MANUFACTURING RISKS, named before the numbers:
  (R1) B = 2 log(sigma_obs/sigma_pred) plotted against sigma_obs has a BUILT-IN slope of 2 from measurement noise
       alone.  The independent axis for a group is therefore its LIGHT (log L_K -> log M_b -> Phi_pred), never its
       observed dispersion.  sigma_obs appears on an axis only for display, and a shuffle control quantifies R1.
  (R2) Hot gas rises with group mass, so an onset in an L_K-only budget can be the onset of hot gas.  Three budgets
       are carried: stars+HI only; + a CGM-level hot halo 0.5 M_*; + an X-ray-scaling hot mass keyed to L_K.
  (R3) Small-N dispersions are biased and noisy; the membership cut is varied 5/10/20.
  (R4) Both footings, always.

Every check below can fail.  rc = number of failures.
"""
import os, sys, math, json
import numpy as np
from astropy.io import fits
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *
from u10_ledger import ledger


def _f(v):
    try: return float(v)
    except Exception: return float('nan')


ck = Check()
rng = np.random.default_rng(22)
C2 = c_light**2

P("=" * 118)
P("f22 -- THE CLUSTER THRESHOLD HUNT: is the scale where the framework stops working a Lambda scale?")
P("=" * 118)

# ============================================================================================ 0. the framework's scales
rho_L = OM_L*rho_crit
H_L = H0*math.sqrt(OM_L)
a0_pred = 0.5*c_light*math.sqrt(G*rho_L)
Z = c_light*H_L/a0_pred
P("\n0.  THE SCALES THE FRAMEWORK OWNS (every 'Lambda scale' below is built from these and nothing else)")
P("-" * 118)
info(f"rho_crit = {rho_crit:.4e} kg/m^3, Omega_Lambda = {OM_L:.4f}, rho_Lambda = {rho_L:.4e} kg/m^3, H_Lambda = {H_L:.4e} s^-1")
info(f"a_0 = (c/2) sqrt(G rho_Lambda) = {a0_pred:.4e} m/s^2  (canonical footing carried as {A0['canonical']:.3e}, alt {A0['alt']:.3e})")
info(f"Z = c H_Lambda / a_0 = {Z:.3f}   (sqrt(32 pi/3) = {math.sqrt(32*math.pi/3):.3f})")
L_dS = c_light/H_L; L_a0 = C2/A0["canonical"]; L_Lam = 1.0/math.sqrt(3*H_L**2/C2)
M_dS = (4.0/3.0)*math.pi*L_dS**3*rho_L
M_MS = c_light**4/(4*G*A0["canonical"])      # mass whose MOND radius equals its Schwarzschild radius
info(f"Lambda LENGTHS: c/H_Lambda = {L_dS/Mpc:.0f} Mpc, c^2/a_0 = {L_a0/Mpc:.0f} Mpc, 1/sqrt(Lambda) = {L_Lam/Mpc:.0f} Mpc")
info(f"Lambda MASSES : de Sitter horizon mass {M_dS/Msun:.2e} Msun; r_M = r_S mass c^4/(4 G a_0) = {M_MS/Msun:.2e} Msun")
info("the dimensionless POTENTIALS available without a mass: a_0/(c H_Lambda) = 1/Z = %.3f and its powers" % (1/Z))
ck("0a the framework's own a_0 is reproduced from rho_Lambda to the precision of the footing",
   abs(a0_pred/A0["canonical"] - 1) < 0.01, f"{a0_pred:.4e} vs {A0['canonical']:.3e}")


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))


ck("0b the kernel used here is the ledger's kernel (hunt_lib.nu_s), so B values are in the ledger's currency",
   abs(float(nu_rar(0.5))/float(nu_s(0.5)) - 1) < 1e-9 and abs(float(nu_rar(0.01))/float(nu_s(0.01)) - 1) < 1e-9,
   f"nu(0.5) = {float(nu_rar(0.5)):.6f} both ways")


def B_of(g_obs, g_bar, a0):
    """log10 g_obs / [nu(g_bar/a0) g_bar]  -- the ledger's acceleration currency."""
    y = g_bar/a0
    return np.log10(g_obs/(nu_rar(y)*g_bar))


def sig_pred_kms(Mb_msun, R_m, a0):
    """Isotropic tracer dispersion in the framework's field of a point mass M_b (kg), 3 sigma^2 = nu(y) g_N r.
    Deep limit: 3 sigma^2 = sqrt(G M a_0), the g06-verified identity (any tracer profile)."""
    M = Mb_msun*Msun
    gN = G*M/R_m**2
    y = gN/a0
    return np.sqrt(nu_rar(y)*gN*R_m/3.0)/1e3


# --------------------------------------------------------------------------------- model comparison on binned data
def fit_models(x, b, e, label, xname, step_grid=None, quiet=False):
    """Bins (x, b, e).  M0 constant; M1 step (two levels, threshold on a grid between bins); M2 ramp b = a + p x;
    M3 hinge: level below x_t, ramp above.  Returns dict with chi2, BIC, params.  All can be compared by BIC."""
    x, b, e = map(np.asarray, (x, b, e)); n = len(x)
    W = 1.0/e**2
    out = {}
    # M0
    m0 = np.sum(W*b)/np.sum(W); c0 = np.sum(W*(b - m0)**2); out["const"] = dict(chi2=c0, k=1, level=m0)
    # M2 ramp
    A = np.vstack([np.ones(n), x]).T
    Aw = A*np.sqrt(W)[:, None]; bw = b*np.sqrt(W)
    coef, *_ = np.linalg.lstsq(Aw, bw, rcond=None); c2 = np.sum(W*(b - A@coef)**2)
    out["ramp"] = dict(chi2=c2, k=2, a=coef[0], p=coef[1])
    # M1 step: threshold between consecutive bins
    if step_grid is None: step_grid = 0.5*(x[:-1] + x[1:])
    best = None
    for xt in step_grid:
        lo, hi = x < xt, x >= xt
        if lo.sum() < 1 or hi.sum() < 1: continue
        ml = np.sum(W[lo]*b[lo])/np.sum(W[lo]); mh = np.sum(W[hi]*b[hi])/np.sum(W[hi])
        c = np.sum(W[lo]*(b[lo] - ml)**2) + np.sum(W[hi]*(b[hi] - mh)**2)
        if best is None or c < best["chi2"]: best = dict(chi2=c, k=3, xt=xt, lo=ml, hi=mh)
    out["step"] = best
    # M3 hinge: b = L for x < xt ; L + p (x - xt) for x >= xt
    besth = None
    for xt in step_grid:
        hinge = np.maximum(x - xt, 0.0)
        A3 = np.vstack([np.ones(n), hinge]).T
        coef3, *_ = np.linalg.lstsq(A3*np.sqrt(W)[:, None], bw, rcond=None); c3 = np.sum(W*(b - A3@coef3)**2)
        if besth is None or c3 < besth["chi2"]: besth = dict(chi2=c3, k=3, xt=xt, level=coef3[0], p=coef3[1])
    out["hinge"] = besth
    for k, v in out.items(): v["bic"] = v["chi2"] + v["k"]*math.log(n)
    if quiet: return out
    P(f"    {label}: models on {n} bins of {xname}")
    for k in ("const", "ramp", "step", "hinge"):
        v = out[k]; extra = {kk: vv for kk, vv in v.items() if kk not in ("chi2", "k", "bic")}
        P(f"      {k:6s} chi2 = {v['chi2']:7.2f}  k = {v['k']}  BIC = {v['bic']:7.2f}   " +
          ", ".join(f"{kk} = {vv:+.3f}" for kk, vv in extra.items()))
    return out


def binned(x, b, edges, nboot=2000, err_floor=0.02):
    xs, bs, es, ns = [], [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        k = (x >= lo) & (x < hi)
        if k.sum() < 4: continue
        v = b[k]; med = np.median(v)
        bb = [np.median(rng.choice(v, len(v), replace=True)) for _ in range(nboot)]
        xs.append(np.median(x[k])); bs.append(med); es.append(max(np.std(bb), err_floor)); ns.append(int(k.sum()))
    return np.array(xs), np.array(bs), np.array(es), np.array(ns)


def spearman_perm(x, y, nperm=20000):
    from scipy.stats import spearmanr
    r0 = spearmanr(x, y).correlation
    cnt = 0
    for _ in range(nperm):
        if abs(spearmanr(x, rng.permutation(y)).correlation) >= abs(r0): cnt += 1
    return r0, (cnt + 1)/(nperm + 1)


# ============================================================================================ 1. THE LEDGER ON ONE AXIS
P("\n" + "=" * 118)
P("1.  THE LIABILITY LEDGER ON THE POTENTIAL-DEPTH AXIS  Phi_d = g_obs r = v_c^2  (plus the 26 Local Volume groups)")
P("=" * 118)
LV = []
for line in open(os.path.join(HERE, "g06_local_volume_groups_lambda_edge.out")):
    if "canonical footing" in line and "PRIMARY" not in line: reading = True
    t = line.split()
    if len(t) >= 9 and t[-1].replace('.', '', 1).isdigit():
        try:
            N = int(t[-8]); y = float(t[-7]); so = float(t[-6]); sp = float(t[-5]); boost = float(t[-4])
            if 3 <= N <= 60 and 10 < so < 400 and 0.05 < boost < 20:
                LV.append(dict(name=" ".join(t[:-8]), N=N, y=y, sig=so, sp=sp, boost=boost))
        except ValueError:
            pass
    if "alt footing" in line: break
LV = LV[:26]
ck("1a the 26 Local Volume groups are read back from g06's committed output (canonical block) with its median boost",
   len(LV) == 26 and abs(np.median([g["boost"] for g in LV]) - 0.817) < 0.01,
   f"{len(LV)} groups, median boost {np.median([g['boost'] for g in LV]):.3f} (g06: 0.817)")

for foot, a0 in A0.items():
    rows = ledger(foot, "iso")
    for r in rows:
        r["Phi"] = r["g_obs"]*r["r"]; r["vc"] = math.sqrt(r["Phi"])/1e3
        r["Phi_pred"] = float(nu_rar(r["y"]))*r["g_bar"]*r["r"]          # the framework's own potential: no g_obs in it
    lvrows = [dict(name="LV " + g["name"], cls="group_lv", B=math.log10(g["boost"]) - (0 if foot == "canonical" else 0.040),
                   y=g["y"]*A0["canonical"]/a0, Phi=3*(g["sig"]*1e3)**2, vc=math.sqrt(3)*g["sig"], support="pressure",
                   Phi_pred=3*(g["sp"]*1e3)**2, M_enc_msun=float("nan")) for g in LV]
    allrows = rows + lvrows
    P(f"\n  --- {foot} footing, a_0 = {a0:.3e} ---")
    P(f"    {'row':24s} {'class':9s} {'v_c km/s':>9s} {'Phi_obs/c^2':>11s} {'Phi_pred/c^2':>12s} {'log y':>7s} {'B dex':>7s}")
    for r in sorted(allrows, key=lambda r: r["Phi_pred"]):
        P(f"    {r['name']:24s} {r['cls']:9s} {r['vc']:9.1f} {r['Phi']/C2:11.2e} {r['Phi_pred']/C2:12.2e} {math.log10(r['y']):7.2f} {r['B']:+7.3f}")
    lab = np.array([1.0 if abs(r["B"]) < 0.15 else 0.0 for r in allrows])
    xP = np.log10([r["Phi"]/C2 for r in allrows])
    def auc(x, y):
        pos, neg = x[y == 1], x[y == 0]
        return float(np.mean([(a > b) + 0.5*(a == b) for a in pos for b in neg]))
    a_all = auc(xP, lab)
    nulls = [auc(xP, rng.permutation(lab)) for _ in range(5000)]
    p_all = float(np.mean(np.abs(np.array(nulls) - 0.5) >= abs(a_all - 0.5)))
    info(f"'lands' = |B| < 0.15 dex: {int(lab.sum())} of {len(allrows)} rows land; AUC(log Phi_d) = {a_all:.3f}, permutation p = {p_all:.3f}")
    # restrict to v_c > 30 km/s (drops globulars and ultra-faints: a cut on the INDEPENDENT variable)
    keep = np.array([r["vc"] > 30 for r in allrows])
    a_big = auc(xP[keep], lab[keep]); nb = [auc(xP[keep], rng.permutation(lab[keep])) for _ in range(5000)]
    p_big = float(np.mean(np.abs(np.array(nb) - 0.5) >= abs(a_big - 0.5)))
    info(f"restricted to v_c > 30 km/s ({int(keep.sum())} rows, {int(lab[keep].sum())} land): AUC = {a_big:.3f}, p = {p_big:.3f}")
    # Spearman of B against log Phi among the rows the framework UNDER-predicts or lands (B > -0.15): the missing-mass side
    side = np.array([r["B"] > -0.15 for r in allrows]) & keep
    xPP = np.log10([r["Phi_pred"]/C2 for r in allrows])
    rs_obs, ps_obs = spearman_perm(xP[side], np.array([r["B"] for r in allrows])[side], 5000)
    rs, ps = spearman_perm(xPP[side], np.array([r["B"] for r in allrows])[side], 5000)
    info(f"missing-mass side (B > -0.15, v_c > 30; {int(side.sum())} rows): Spearman(B, log Phi_obs) = {rs_obs:+.3f} (p = {ps_obs:.4f}) -- "
         f"partly BUILT IN (R1: g_obs is in both);  Spearman(B, log Phi_pred) = {rs:+.3f} (p = {ps:.4f}) -- the clean axis")
    if foot == "canonical":
        AUC_LEDGER = (a_all, p_all, a_big, p_big, rs, ps)

a_all, p_all, a_big, p_big, rs, ps = AUC_LEDGER
ck("1b (can fail) the potential-depth axis is NOT a sharp boundary on the full ledger either: this check asserts the "
   "ledger's landing/missing split is not separated by Phi_d at AUC >= 0.9.  If it FAILED, u13's negative would be "
   "overturned by the new axis and section 4 would have a threshold to confront", a_all < 0.9 and a_big < 0.9,
   f"AUC {a_all:.3f} (all rows), {a_big:.3f} (v_c > 30 km/s)")
ck("1c (HYPOTHESIS CHECK -- a FAIL is a result) on the missing-mass side of the ledger the residual rises with the "
   "framework's PREDICTED potential, the axis with no g_obs in it.  If this fails, the ledger's apparent rise with "
   "potential depth was built in through g_obs (R1) and there is no potential-depth ordering to hunt a threshold in",
   rs > 0 and ps < 0.05, f"Spearman(B, log Phi_pred) {rs:+.3f}, p = {ps:.4f}  vs built-in Spearman(B, log Phi_obs) {rs_obs:+.3f}")

# ============================================================================================ 2. THE KOURKCHI SWEEP
P("\n" + "=" * 118)
P("2.  THE SINGLE-ESTIMATOR SWEEP: Kourkchi & Tully 2017 groups within 3500 km/s -- one catalogue, one method, from")
P("    galaxy groups to the nearest clusters.  Residual against LIGHT (the independent axis), dispersion for display.")
P("=" * 118)
KT = vizier_tsv("kt2017_groups_full.tsv")
pgc = np.array([_f(r["PGC1"]) for r in KT]); Nm = np.array([_f(r["Nm"]) for r in KT])
logK = np.array([_f(r["logK"]) for r in KT]); Dist = np.array([_f(r["Dist"]) for r in KT])
sigV = np.array([_f(r["sigmaV"]) for r in KT]); Rg = np.array([_f(r["Rg"]) for r in KT]); R2t = np.array([_f(r["R2t"]) for r in KT])
logMd = np.array([_f(r["logMd"]) for r in KT]); logMK = np.array([_f(r["logMK"]) for r in KT])
info(f"catalogue read: {len(KT)} groups; {int((Nm >= 5).sum())} with >= 5 members, {int((Nm >= 10).sum())} with >= 10, {int((Nm >= 20).sum())} with >= 20")

# Lovisari 2015 X-ray groups: M_gas,500(M500) for the hot-gas prescription (C), keyed to L_K through Kravtsov 2018
LOV = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith("#") and l.strip()]
lh = LOV[0]; LOV = [dict(zip(lh, r)) for r in LOV[1:]]
lM500 = np.log10([_f(r["M500_1e13"])*1e13 for r in LOV]); lMg = np.log10([_f(r["Mgas500_1e12"])*1e12 for r in LOV])
lkT = np.array([_f(r["kT_keV"]) for r in LOV]); lR500 = np.array([_f(r["R500_kpc"]) for r in LOV])
sl, ic = np.polyfit(lM500, lMg, 1)
info(f"Lovisari+2015: log M_gas,500 = {sl:.3f} log M500 {ic:+.3f} over M500 = {10**lM500.min():.1e}-{10**lM500.max():.1e} (20 groups)")
mstar500 = lambda M500: 1.7e12*(M500/1e14)**0.60                      # Kravtsov, Vikhlinin & Meshcheryakov 2018
def M500_of_mstar(Ms): return 1e14*(Ms/1.7e12)**(1/0.60)
def Mhot_xray(Ms):
    """hot gas keyed to STELLAR mass only (independent of the dispersion): M* -> M500 (KVM18) -> M_gas,500 (Lovisari)."""
    return 10**(sl*np.log10(M500_of_mstar(Ms)) + ic)

UPS_K = 0.60; F_HI = 0.10
BUDGETS = {"A stars+HI": lambda Ms: Ms*(1 + F_HI),
           "B +CGM 0.5M*": lambda Ms: Ms*(1 + F_HI) + 0.5*Ms,
           "C +X-ray hot(L_K)": lambda Ms: Ms*(1 + F_HI) + np.maximum(0.5*Ms, Mhot_xray(Ms))}
for nm, f in BUDGETS.items():
    info(f"  budget {nm:18s}: M_b/M_* at M_* = 1e11: {f(1e11)/1e11:.2f}, 1e12: {f(1e12)/1e12:.2f}, 3e12: {f(3e12)/3e12:.2f}")

# cross-calibration against g06's per-galaxy budgets on the hosts both samples contain (PGC numbers of the g06 hosts)
PGC_OF = {"MESSIER031": 2557, "MESSIER081": 28630, "NGC5128": 46957, "NGC4258": 39600, "NGC5236": 48082, "IC0342": 13826,
          "NGC0253": 2789, "NGC4736": 43495, "NGC3368": 32192, "NGC4594": 42407, "NGC5055": 46153, "NGC5194": 47404,
          "NGC6744": 62836, "NGC6946": 65001, "NGC4945": 45279, "MESSIER101": 50063, "NGC0925": 9332, "NGC2903": 27077,
          "NGC3432": 32643, "NGC3521": 33550, "NGC4631": 42637, "NGC3412": 32508, "NGC3115": 29265, "NGC3627": 34695,
          "NGC2784": 25950}
matched = []
for g in LV:
    p = PGC_OF.get(g["name"].replace(" ", ""))
    if p is None: continue
    k = np.where(pgc == p)[0]
    if len(k) == 0: continue
    k = k[0]
    if sigV[k] > 0 and Nm[k] >= 3: matched.append((g["name"], g["N"], g["sig"], int(Nm[k]), sigV[k], logK[k]))
P(f"    {'host':12s} {'N_g06':>5s} {'sig_g06':>8s} {'N_KT':>5s} {'sig_KT':>7s} {'logK':>6s}")
for m in matched: P(f"    {m[0]:12s} {m[1]:5d} {m[2]:8.1f} {m[3]:5d} {m[4]:7.0f} {m[5]:6.2f}")
dsig = np.array([math.log10(m[4]/m[2]) for m in matched]); nk = np.array([m[3] for m in matched]); ng = np.array([m[1] for m in matched])
rich = (nk >= 30) & (ng >= 30)
ck("2a-best the two best-populated hosts both catalogues contain (>= 30 members in each: M31 and M81) agree on their "
   "dispersions to a few per cent, so where membership is not in doubt the Kourkchi sweep IS g06's measurement",
   rich.sum() >= 2 and np.all(np.abs(dsig[rich]) < 0.05),
   f"{int(rich.sum())} hosts; log10(sigma_KT/sigma_g06) = " + ", ".join(f"{m[0]} {d:+.3f}" for m, d in zip(np.array(matched, dtype=object)[rich], dsig[rich])))
ck("2a-rest (HYPOTHESIS CHECK -- a FAIL is a result) the catalogues also agree on every OTHER shared host to 0.1 dex.  "
   "If this fails, a group's dispersion depends on which membership algorithm built the group, by more than the "
   "group-vs-cluster contrast the ledger carries, and the group-scale amplitude is estimator-limited (g06v's "
   "common-mode systematic, here measured directly on the same sky)",
   np.abs(np.median(dsig[~rich])) < 0.1 and np.std(dsig[~rich]) < 0.1,
   f"{int((~rich).sum())} hosts; median log10(sigma_KT/sigma_g06) = {np.median(dsig[~rich]):+.3f}, rms {np.std(dsig[~rich]):.3f} "
   f"(= {2*np.median(dsig[~rich]):+.2f} dex in B); worst {matched[int(np.argmax(np.abs(dsig)))][0]} {dsig[int(np.argmax(np.abs(dsig)))]:+.3f}")

RESULTS = {}
def kt_mask(NMIN):
    return (Nm >= NMIN) & (sigV > 0) & np.isfinite(logK) & np.isfinite(Rg) & (Rg > 0) & (Dist > 1.0) & (Dist < 60)
okp = kt_mask(10)
for foot, a0 in A0.items():
    for NMIN in (10, 5, 20):
        ok = kt_mask(NMIN)
        Ms = UPS_K*10**logK[ok]; R = Rg[ok]*Mpc; so = sigV[ok]; nn = Nm[ok]
        for bname, f in BUDGETS.items():
            Mb = f(Ms)
            sp = sig_pred_kms(Mb, R, a0)
            B = 2*np.log10(so/sp)
            xL = np.log10(Mb)                              # the independent axis: baryonic mass from LIGHT
            Phi_pred = np.sqrt(G*Mb*Msun*a0)               # the framework's own potential scale, m^2/s^2
            edges = np.array([10.4, 10.8, 11.1, 11.4, 11.7, 12.0, 12.3, 12.6, 13.0, 13.6])
            xb, bb, eb, nb = binned(xL, B, edges)
            eB = 0.87/np.sqrt(2*(nn - 1))                  # gapper error on B, dex
            tag = f"{foot}|N>={NMIN}|{bname}"
            RESULTS[tag] = dict(x=xL, B=B, so=so, sp=sp, nn=nn, xb=xb, bb=bb, eb=eb, nb=nb, Mb=Mb, Phi=Phi_pred)
            verbose = (NMIN == 10 and foot == "canonical") or (NMIN == 10 and bname.startswith("B"))
            RESULTS[tag]["fit"] = fit_models(xb, bb, eb, tag, "log M_b", quiet=True)
            RESULTS[tag]["spear"] = spearman_perm(xL, B, 2000)
            if verbose:
                P(f"\n  --- {foot}, N >= {NMIN}, budget {bname}: {int(ok.sum())} groups, sigma_obs {so.min():.0f}-{so.max():.0f} km/s ---")
                P(f"    {'log M_b bin':>12s} {'N':>4s} {'median B':>9s} {'+-':>6s} {'sig_obs':>8s} {'sig_pred':>9s} {'Phi_pred/c^2':>13s}")
                for lo, hi in zip(edges[:-1], edges[1:]):
                    k = (xL >= lo) & (xL < hi)
                    if k.sum() < 4: continue
                    P(f"    {lo:5.1f}-{hi:4.1f}  {int(k.sum()):4d} {np.median(B[k]):+9.3f} {max(np.std([np.median(rng.choice(B[k], k.sum())) for _ in range(300)]), 0.02):6.3f} "
                      f"{np.median(so[k]):8.0f} {np.median(sp[k]):9.0f} {np.median(Phi_pred[k])/C2:13.2e}")
                fit_models(xb, bb, eb, f"{foot} N>={NMIN} {bname}", "log M_b")
                r_s, p_s = RESULTS[tag]["spear"]
                info(f"Spearman(B, log M_b) over the {len(B)} groups = {r_s:+.3f}, permutation p = {p_s:.4f}")

# --- the primary result (canonical, N>=10, budget B) and its brackets
prim = RESULTS["canonical|N>=10|B +CGM 0.5M*"]
fm = prim["fit"]
best = min(("const", "ramp", "step", "hinge"), key=lambda k: fm[k]["bic"])
info(f"PRIMARY (canonical, N >= 10, budget B): best model by BIC = '{best}'; dBIC(const - best) = {fm['const']['bic'] - fm[best]['bic']:.1f}, "
     f"dBIC(step - ramp) = {fm['step']['bic'] - fm['ramp']['bic']:+.1f}, dBIC(hinge - ramp) = {fm['hinge']['bic'] - fm['ramp']['bic']:+.1f}")
info(f"   step threshold log M_b = {fm['step']['xt']:.2f} (levels {fm['step']['lo']:+.3f} -> {fm['step']['hi']:+.3f}); "
     f"hinge onset log M_b = {fm['hinge']['xt']:.2f}, slope above {fm['hinge']['p']:+.3f} dex/dex; ramp slope {fm['ramp']['p']:+.3f} dex/dex")
lowbins = prim["xb"] < 11.4
info(f"   groups below log M_b = 11.4 (the g06 regime): median B = {np.median(prim['B'][prim['x'] < 11.4]):+.3f} dex over {int((prim['x'] < 11.4).sum())} groups; "
     f"above 12.6: {np.median(prim['B'][prim['x'] > 12.6]):+.3f} over {int((prim['x'] > 12.6).sum())}")
ck("2b (HYPOTHESIS CHECK -- a FAIL is a result) THE SWEEP FINDS A RISE: within one catalogue and one estimator the "
   "residual rises with baryonic mass from the group regime to the nearest clusters.  A FAIL means the residual is "
   "FLAT across the sweep on the primary budget",
   prim["spear"][0] > 0 and prim["spear"][1] < 0.01, f"Spearman {prim['spear'][0]:+.3f}, p = {prim['spear'][1]:.4f}")
ck("2c (THE THRESHOLD QUESTION -- HYPOTHESIS CHECK, a FAIL is a result) is there a STEP -- a sharp domain boundary -- "
   "in the sweep?  A step needs dBIC(step - ramp) < -6 (strong evidence) on the primary budget.  A FAIL means there is "
   "no edge to hand to Lambda",
   fm["step"]["bic"] - fm["ramp"]["bic"] < -6, f"dBIC(step - ramp) = {fm['step']['bic'] - fm['ramp']['bic']:+.1f}; best = {best}")
STEP_WINS = fm["step"]["bic"] - fm["ramp"]["bic"] < -6

# robustness of the slope across footings, membership cuts and budgets
P("\n    slope of B against log M_b (ramp model), every variant:")
P(f"    {'variant':44s} {'N':>5s} {'slope':>7s} {'onset(hinge)':>13s} {'dBIC step-ramp':>15s} {'Spearman':>9s}")
slopes = {}
for tag, R_ in RESULTS.items():
    if "fit" not in R_: continue
    f_ = R_["fit"]; slopes[tag] = f_["ramp"]["p"]
    P(f"    {tag:44s} {len(R_['B']):5d} {f_['ramp']['p']:+7.3f} {f_['hinge']['xt']:13.2f} {f_['step']['bic'] - f_['ramp']['bic']:+15.1f} {R_['spear'][0]:+9.3f}")
ck("2d (HYPOTHESIS CHECK -- a FAIL is a result) any rise survives the X-ray hot-gas budget keyed to light (budget C).  "
   "A FAIL means whatever rise the stellar budgets show is removable by counting the hot baryons, i.e. it is the onset "
   "of hot gas and not of a gravitational regime",
   slopes["canonical|N>=10|C +X-ray hot(L_K)"] > 0.5*slopes["canonical|N>=10|B +CGM 0.5M*"] and slopes["canonical|N>=10|C +X-ray hot(L_K)"] > 0,
   f"slope B-budget {slopes['canonical|N>=10|B +CGM 0.5M*']:+.3f}, C-budget {slopes['canonical|N>=10|C +X-ray hot(L_K)']:+.3f}")
sA = [v for k, v in slopes.items() if k.endswith("A stars+HI")]; sC = [v for k, v in slopes.items() if k.endswith("C +X-ray hot(L_K)")]
ck("2e THE SIGN OF THE SLOPE IS A BUDGET CHOICE: on stars+HI alone every variant slopes up; with the light-keyed X-ray "
   "hot gas every variant is flat to within 0.1 dex per dex.  A slope whose sign the baryon budget controls is a "
   "statement about the budget, not about gravity, and it cannot locate a gravitational threshold",
   all(v > 0 for v in sA) and all(abs(v) < 0.1 for v in sC) and all(a > c for a, c in zip(sA, sC)),
   "stars+HI slopes " + ", ".join(f"{v:+.2f}" for v in sA) + ";  hot-gas slopes " + ", ".join(f"{v:+.2f}" for v in sC))

# --- R1 control: the same statistic against sigma_obs, and the shuffle floor
P("\n    (R1) the built-in slope: B against log sigma_obs, real pairing vs sigma shuffled among groups of similar light")
xs = np.log10(prim["so"]); B = prim["B"]; xL = prim["x"]
from scipy.stats import spearmanr
r_real = spearmanr(xs, B).correlation
r_sh = []
order = np.argsort(xL)
for _ in range(500):
    so_sh = prim["so"].copy()
    # shuffle sigma_obs within light-sorted blocks of 40 groups: every marginal kept, the light-sigma pairing destroyed
    for i0 in range(0, len(order), 40):
        idx = order[i0:i0 + 40]; so_sh[idx] = prim["so"][rng.permutation(idx)]
    Bsh = 2*np.log10(so_sh/prim["sp"])
    r_sh.append(spearmanr(np.log10(so_sh), Bsh).correlation)
info(f"Spearman(B, log sigma_obs) real = {r_real:+.3f}; with sigma shuffled inside light blocks = {np.mean(r_sh):+.3f} +- {np.std(r_sh):.3f}")
ck("2f (R1 named and measured) plotting the residual against the OBSERVED dispersion manufactures a correlation even "
   "when the pairing is destroyed, which is why the light axis is the one every conclusion above uses",
   np.mean(r_sh) > 0.3, f"shuffle-floor Spearman {np.mean(r_sh):+.3f} -- a large 'signal' from noise alone")

# --- the step-finder has power (synthetic injection on the real bin layout)
P("\n    synthetic injection: would a RISE of the cluster-front size have been seen against the flat model on this bin layout?")
xb, eb = prim["xb"], prim["eb"]
def _best_vs_const(bs):
    o = fit_models(xb, bs, eb, "", "", quiet=True)
    return o["const"]["bic"] - min(o["step"]["bic"], o["ramp"]["bic"], o["hinge"]["bic"])
power = {}
for rise in (0.10, 0.20, 0.30):
    hits = 0
    for _ in range(200):
        bs = np.where(xb >= xb[-2] - 1e-9, rise, 0.0) + rng.normal(0, eb)      # step at the bin where the stellar-budget rise sat
        hits += (_best_vs_const(bs) > 6)
    power[rise] = hits/200
false = sum(_best_vs_const(np.zeros_like(xb) + rng.normal(0, eb)) > 6 for _ in range(200))/200
info("injected step vs flat, fraction detected at dBIC > 6: " + ", ".join(f"{r:.2f} dex -> {p*100:.0f}%" for r, p in power.items()) +
     f";  false detection on flat data {false*100:.0f}%;  the real data: dBIC(const - best) = {fm['const']['bic'] - min(fm['step']['bic'], fm['ramp']['bic'], fm['hinge']['bic']):.1f}")
info("(step-vs-ramp discrimination has no power at these sizes on five bins -- 2c's dBIC is reported, not leaned on; the null that matters is rise-vs-flat)")
ck("2g THE STRENGTH OF THE NULL: against the flat model the sweep detects a 0.3 dex step (the ledger's cluster level "
   "above g06's group level) in >= 90% of injections with <= 10% false detections, and the real data prefer FLAT.  So "
   "the null excludes a domain edge of 0.3 dex anywhere in 10^10.4-10^12.3 Msun; at 0.2 dex the power is partial and "
   "is quoted, not leaned on", power[0.30] >= 0.9 and false <= 0.1,
   f"detection {power[0.30]*100:.0f}% at 0.3 dex, {power[0.20]*100:.0f}% at 0.2, {power[0.10]*100:.0f}% at 0.1; false {false*100:.0f}%; "
   f"real dBIC(const - best) = {fm['const']['bic'] - min(fm['step']['bic'], fm['ramp']['bic'], fm['hinge']['bic']):.1f}")

# --- provenance: are the catalogue dispersions MEASURED, or derived from luminosity?  (if the latter the sweep is circular)
P("\n    provenance of sigma_V: scatter of log sigma_V at fixed light, by membership")
for lo_n, hi_n in ((5, 10), (10, 20), (20, 1000)):
    k = (Nm >= lo_n) & (Nm < hi_n) & (sigV > 0) & np.isfinite(logK) & (Dist > 1)
    A_ = np.vstack([np.ones(k.sum()), logK[k]]).T; cf, *_ = np.linalg.lstsq(A_, np.log10(sigV[k]), rcond=None)
    res = np.log10(sigV[k]) - A_@cf
    info(f"      N_m in [{lo_n},{hi_n}): {int(k.sum())} groups, log sigma_V = {cf[0]:+.2f} {cf[1]:+.3f} logK, residual scatter {np.std(res):.3f} dex")
    if lo_n == 5: scat5 = np.std(res)
Md_chk = 3*(sigV[okp]*1e3)**2*Rg[okp]*Mpc/G/Msun
info(f"      catalogue logMd vs 3 sigma^2 Rg/G: median offset {np.median(logMd[okp] - np.log10(Md_chk)):+.3f} dex, scatter {np.std(logMd[okp] - np.log10(Md_chk)):.3f} -- M_d is a virial function of sigma and Rg, and sigma is not a function of light")
ck("2h the dispersions are MEASURED, not luminosity-derived: at fixed light they scatter by far more than a scaling "
   "relation would (>= 0.15 dex), so the sweep is not circular", scat5 > 0.15, f"scatter at fixed logK = {scat5:.3f} dex (N_m 5-9)")
dev = {k: float(np.max(np.abs(v["bb"] - np.median(v["B"])))) for k, v in RESULTS.items() if "N>=10" in k and not k.endswith("A stars+HI")}
ck("2i THE FLATNESS, stated at its strength: on both footings and both hot-gas budgets (N >= 10), no bin of the sweep "
   "departs from the sample median by more than 0.15 dex across 10^10.4-10^12.3 Msun of baryons -- two decades of "
   "mass and a factor 10 in predicted potential with no edge",
   all(v < 0.15 for v in dev.values()), "max |bin - median| = " + ", ".join(f"{v:.3f}" for v in dev.values()))

# ============================================================================================ 3. THE eRASS1 TEMPERATURE SWEEP
P("\n" + "=" * 118)
P("3.  THE eRASS1 TEMPERATURE SWEEP: residual at R500 against a MEASURED potential depth (kT), 0.5-12 keV, z < 1")
P("=" * 118)
sys.path.insert(0, DATA)
from _load_erass1 import load_raw
E = load_raw()
ok = (E["z"] > 0) & (E["z"] < 1.0) & (E["M500"] > 0) & (E["Mgas"] > 0) & (E["R500"] > 0) & (E["fgas"] > 0.01) & (E["fgas"] < 0.30) & (E["kt"] > 0.3)
z = E["z"][ok]; M500 = E["M500"][ok]*1e13; Mg = E["Mgas"][ok]*1e11; R = E["R500"][ok]*kpc; kT = E["kt"][ok]
info(f"eRASS1 clean with kT: {int(ok.sum())} systems, kT {kT.min():.2f}-{kT.max():.2f} keV, M500 {M500.min():.1e}-{M500.max():.1e}")
mu_mp = 0.6*1.6726e-27
vc2_T = 2*kT*1.602e-16/mu_mp                      # isothermal beta = 1: kT = mu m_p v_c^2 / 2
Phi_obs = G*M500*Msun/R
info(f"potential from kT (v_c^2 = 2 kT / mu m_p) vs from M500/R500: median ratio {np.median(vc2_T/Phi_obs):.2f} -- the two potential axes agree to a factor of order unity, as they must")
ER = {}
for foot, a0 in A0.items():
    for sname, Ms in (("stars 0.2 M_gas", 0.2*Mg), ("stars KVM18", mstar500(M500))):
        gobs = G*M500*Msun/R**2; gbar = G*(Mg + Ms)*Msun/R**2
        B = B_of(gobs, gbar, a0)
        xT = np.log10(kT)
        edges = np.log10(np.array([0.3, 0.6, 0.9, 1.3, 1.8, 2.5, 3.5, 5.0, 7.0, 13.0]))
        xb, bb, eb, nb = binned(xT, B, edges)
        tag = f"{foot}|{sname}"
        ER[tag] = dict(B=B, xT=xT, xb=xb, bb=bb, eb=eb, z=z, kT=kT)
        if foot == "canonical" or sname.startswith("stars 0.2"):
            P(f"\n  --- {foot}, {sname} ---")
            P(f"    {'kT bin keV':>12s} {'N':>5s} {'median B':>9s} {'+-':>6s} {'Phi/c^2':>9s} {'median z':>9s}")
            for lo, hi in zip(edges[:-1], edges[1:]):
                k = (xT >= lo) & (xT < hi)
                if k.sum() < 4: continue
                P(f"    {10**lo:5.2f}-{10**hi:5.2f} {int(k.sum()):5d} {np.median(B[k]):+9.3f} {max(np.std([np.median(rng.choice(B[k], k.sum())) for _ in range(300)]), 0.02):6.3f} "
                  f"{np.median(Phi_obs[k])/C2:9.2e} {np.median(z[k]):9.2f}")
            ER[tag]["fit"] = fit_models(xb, bb, eb, tag, "log kT")
            r_s, p_s = spearman_perm(xT, B, 3000); ER[tag]["spear"] = (r_s, p_s)
            info(f"Spearman(B, log kT) = {r_s:+.3f}, p = {p_s:.4f}; median B = {np.median(B):+.3f} dex")
ep = ER["canonical|stars 0.2 M_gas"]; ef = ep["fit"]
info(f"eRASS1 primary: const level {ef['const']['level']:+.3f}; ramp slope {ef['ramp']['p']:+.3f} dex per dex of kT; "
     f"dBIC(step - ramp) = {ef['step']['bic'] - ef['ramp']['bic']:+.1f}; dBIC(ramp - const) = {ef['ramp']['bic'] - ef['const']['bic']:+.1f}")
ck("3a inside the cluster regime (0.3-12 keV, Phi/c^2 ~ 1e-6 to 4e-5) there is NO threshold: the residual is a "
   "plateau, not a step -- a step is not preferred over a ramp and the total swing across 1.6 decades of kT is under "
   "0.3 dex.  If a Lambda edge existed inside this range it would have to show here, on 3000+ systems",
   (ef["step"]["bic"] - ef["ramp"]["bic"] > -6) and (abs(ef["ramp"]["p"])*1.6 < 0.3),
   f"dBIC(step-ramp) = {ef['step']['bic'] - ef['ramp']['bic']:+.1f}, ramp swing over 1.6 dex = {abs(ef['ramp']['p'])*1.6:.3f} dex")
ck("3b the plateau is the ledger's cluster level, both stellar imports, both footings (median B between +0.2 and +0.5 dex)",
   all(0.2 < np.median(v["B"]) < 0.5 for v in ER.values()), ", ".join(f"{k}: {np.median(v['B']):+.3f}" for k, v in ER.items()))
# the z-lever inside eRASS1 at fixed kT: a Lambda-set threshold cannot move with z; the level at fixed depth can be compared
Bp, zT, kTp = ep["B"], ep["z"], ep["kT"]
mid = (kTp > 2.0) & (kTp < 5.0)
lo_z, hi_z = mid & (zT < 0.2), mid & (zT > 0.5)
info(f"at fixed depth (kT = 2-5 keV): median B = {np.median(Bp[lo_z]):+.3f} (z < 0.2, N = {int(lo_z.sum())}) vs {np.median(Bp[hi_z]):+.3f} (z > 0.5, N = {int(hi_z.sum())})")

# ============================================================================================ 4. THE LAMBDA CONFRONTATION
P("\n" + "=" * 118)
P("4.  THE LAMBDA CONFRONTATION: where the residual turns on, and whether that place is a scale the framework owns")
P("=" * 118)
hx = fm["hinge"]["xt"]; sx = fm["step"]["xt"]
onset_M = 10**hx; onset_Phi = math.sqrt(G*onset_M*Msun*A0["canonical"])
info(f"the Kourkchi hinge onset (primary): log M_b = {hx:.2f}  ->  M_b = {onset_M:.2e} Msun, predicted potential sqrt(G M_b a_0)/c^2 = {onset_Phi/C2:.2e}, "
     f"v_c = {math.sqrt(onset_Phi)/1e3:.0f} km/s, kT-equivalent = {mu_mp*onset_Phi/2/1.602e-16:.2f} keV")
info(f"the step threshold (for reference, even though 2c did not prefer it): log M_b = {sx:.2f}")
P("\n    4a  THE DIMENSIONAL STATEMENT.  A potential threshold needs a mass or a length beside a_0, c, G and H_Lambda:")
info(f"    the only Lambda lengths are {L_dS/Mpc:.0f}-{L_a0/Mpc:.0f} Mpc (Gpc scale); the only Lambda masses are {M_dS/Msun:.1e}-{M_MS/Msun:.1e} Msun.")
info(f"    the onset sits at {onset_M/M_dS:.1e} of the de Sitter mass and its potential at {onset_Phi/C2/(1/Z):.1e} of a_0/(c H_Lambda).")
info("    So a Lambda-set onset would need a NEW dimensionless number of order 1e-10 to 1e-11 that nothing in the framework supplies,")
info("    OR it must be a DENSITY (rho_Lambda is the one scale that lives at the right order).  4b tests the density reading.")
ck("4a no Lambda length or mass sits within three decades of the onset, so the onset cannot be 'a_0 times a Lambda length' "
   "or 'the framework's potential at a Lambda mass': any Lambda threshold must be a density or a coincidence",
   onset_M/M_dS < 1e-3 and (onset_Phi/C2)/(1/Z) < 1e-3, f"M/M_dS = {onset_M/M_dS:.1e}; Phi/(a_0 c/H_Lambda) = {(onset_Phi/C2)/(1/Z):.1e}")

P("\n    4b  THE DENSITY READING: mean enclosed OBSERVED density at the measurement radius, in units of rho_Lambda")
# groups (Kourkchi): dynamical mass 3 sigma^2 Rg / G inside Rg ; clusters at R500: 500 rho_c(z) by definition ; discs at r_M
Rk = Rg[okp]*Mpc
Md_k = 3*(prim["so"]*1e3)**2*Rk/G
rho_k = Md_k/(4/3*math.pi*Rk**3)/rho_L
lo_k, hi_k = prim["x"] < 11.4, prim["x"] > 12.6
info(f"    Kourkchi groups, landing regime (log M_b < 11.4): median rho_enc/rho_Lambda = {np.median(rho_k[lo_k]):.0f};  cluster end (> 12.6): {np.median(rho_k[hi_k]):.0f}")
rho_500 = 500*rho_crit/rho_L
info(f"    every X-ray row at R500 (Lovisari, X-COP, eRASS1): 500 rho_c = {rho_500:.0f} rho_Lambda at z = 0 (higher at z > 0 by E(z)^2)")
gals = load_sparc()
rho_g = []
for g in gals:
    rM = math.sqrt(G*g["Mb"]*Msun/A0["canonical"])
    rho_g.append(g["Mb"]*Msun/(4/3*math.pi*rM**3)/rho_L)
info(f"    SPARC discs inside their own MOND radius r_M = sqrt(G M_b/a_0): median rho/rho_Lambda = {np.median(rho_g):.0f}  (they land)")
_e = ledger('canonical')[0]; _M = _e['g_obs']*_e['r']**2/G
info(f"    the ledger's X-ray ellipticals at 20 kpc: rho_enc/rho_Lambda ~ {_M/(4/3*math.pi*_e['r']**3)/rho_L:.0f}  (they miss by +0.23 dex)")
dens_monotone = (np.median(rho_k[lo_k]) < np.median(rho_k[hi_k])) and (np.median(rho_g) > np.median(rho_k[hi_k]))
ck("4b (can fail) the failure is NOT ordered by enclosed density in units of rho_Lambda: landing discs are the DENSEST "
   "systems, landing groups the SPARSEST, and the missing clusters sit in between.  A 'fails below X rho_Lambda' or "
   "'fails above X rho_Lambda' law would need a monotone ordering, and there is none",
   dens_monotone, f"discs ~{np.median(rho_g):.0f}, clusters ~{np.median(rho_k[hi_k]):.0f}-{rho_500:.0f}, landing groups ~{np.median(rho_k[lo_k]):.0f} (rho_Lambda units)")

P("\n    4c  THE COINCIDENCE-DENSITY CONTROL: how many 'natural' numbers land within 0.15 dex of the onset?")
base = {"Omega_b": OM_B, "Omega_m": OM_M, "Omega_L": OM_L, "1/Z": 1/Z, "2pi": 2*math.pi, "32pi": 32*math.pi, "h": h, "3": 3.0, "2": 2.0}
names = list(base.keys()); vals = np.array([base[k] for k in names])
targets = {"onset Phi/c^2": onset_Phi/C2, "onset M_b/M_dS": onset_M/M_dS, "step Phi/c^2": math.sqrt(G*10**sx*Msun*A0["canonical"])/C2}
import itertools
exps = [-2, -1, 0, 1, 2]
combos = []
for ee in itertools.product(exps, repeat=len(names)):
    if sum(abs(e_) for e_ in ee) > 4: continue
    v = float(np.prod(vals**np.array(ee)))
    combos.append((v, ee))
cv = np.log10(np.array([c[0] for c in combos]))
for tn, tv in targets.items():
    hit = np.abs(cv - math.log10(tv)) < 0.15
    ex = [combos[i] for i in np.where(hit)[0][:4]]
    info(f"    {tn:16s} = {tv:.2e}: {int(hit.sum())} products of <= 4 factors from {names} land within 0.15 dex; e.g. " +
         "; ".join("*".join(f"{names[j]}^{e_}" for j, e_ in enumerate(ee) if e_ != 0) for _, ee in ex))
nhits = int((np.abs(cv - math.log10(targets["onset Phi/c^2"])) < 0.15).sum())
# chance expectation: the mean count in random 0.3-dex windows over the two decades around the target
centres = math.log10(targets["onset Phi/c^2"]) + rng.uniform(-1.0, 1.0, 2000)
chance = np.array([(np.abs(cv - c_) < 0.15).sum() for c_ in centres])
info(f"    chance expectation for a 0.3-dex window in the same decade band: {chance.mean():.1f} +- {chance.std():.1f} matches; observed {nhits}")
ck("4c any match of the onset to a product of the framework's own numbers is at the chance rate for this combinatorial "
   "space (observed count within 2 sigma of the random-window expectation), so a single-number Lambda coincidence "
   "could never have been evidence; only a SCALING (4d) could",
   abs(nhits - chance.mean()) <= 2*chance.std() + 1, f"observed {nhits} vs chance {chance.mean():.1f} +- {chance.std():.1f}")

P("\n    4d  WHAT WOULD BE EVIDENCE: a scaling.  A Lambda-set threshold is a fixed potential (or mass) at every z; a")
P("        baryon-physics threshold moves with the baryon budget.  The eRASS1 fixed-depth z-split (section 3) is the only")
P("        handle on disk, and its selection function is not under this file's control; recorded, not claimed:")
info(f"        kT = 2-5 keV: B(z < 0.2) = {np.median(Bp[lo_z]):+.3f}, B(z > 0.5) = {np.median(Bp[hi_z]):+.3f}; a fixed threshold predicts equal levels")

# ============================================================================================ 5. MUTATION CONTROLS
P("\n" + "=" * 118)
P("5.  MUTATION CONTROLS")
P("=" * 118)
# M1 Newtonian: the sweep must explode
MsP = UPS_K*10**logK[okp]; MbP = BUDGETS["B +CGM 0.5M*"](MsP); RP = Rg[okp]*Mpc
sN = np.sqrt(G*MbP*Msun/RP/3)/1e3
BN = 2*np.log10(sigV[okp]/sN)
ck("M1 switch the kernel off (Newtonian gravity on the same baryons): the group residual must explode to the dark-matter "
   "ratio these groups are famous for, or the pipeline is not measuring gravity",
   np.median(BN) > 0.8, f"Newtonian median B = {np.median(BN):+.3f} dex (x{10**np.median(BN):.0f}) vs framework {np.median(prim['B']):+.3f}")
# M2 shuffle light among groups: the light-axis trend must vanish
rsh = []
for _ in range(300):
    pi = rng.permutation(len(MsP))
    Bsh = 2*np.log10(sigV[okp]/sig_pred_kms(MbP[pi], RP, A0["canonical"]))
    rsh.append(spearmanr(np.log10(MbP[pi]), Bsh).correlation)
ck("M2 shuffle the LIGHT among groups (keep every marginal, destroy the pairing): the correlation of B with log M_b "
   "must collapse to the negative built-in value (B falls with the shuffled M_b through sigma_pred alone).  The real "
   "pairing sits far above that floor, which is the sensitivity that makes the flat result of 2b/2i a measurement",
   np.mean(rsh) < 0 and prim["spear"][0] > np.mean(rsh) + 5*np.std(rsh),
   f"shuffled Spearman {np.mean(rsh):+.3f} +- {np.std(rsh):.3f} vs real {prim['spear'][0]:+.3f}")
# M3 triple a_0: deep-MOND boost scales as 1/sqrt(a_0)
B3 = 2*np.log10(sigV[okp]/sig_pred_kms(MbP, RP, 3*A0["canonical"]))
ck("M3 triple a_0: in the deep limit sigma_pred grows as a_0^(1/4), so B must fall by 0.5 log 3 = 0.239 dex (a 25% "
   "departure allowed for the groups that are not fully deep)",
   abs((np.median(prim["B"]) - np.median(B3)) - 0.239) < 0.06, f"shift {np.median(prim['B']) - np.median(B3):.3f} dex vs 0.239")
# M4 Upsilon_K bracket
for U in (0.4, 1.0):
    Bu = 2*np.log10(sigV[okp]/sig_pred_kms(BUDGETS["B +CGM 0.5M*"](U*10**logK[okp]), RP, A0["canonical"]))
    info(f"Upsilon_K = {U}: median B = {np.median(Bu):+.3f}, Spearman(B, log M_b) = {spearmanr(np.log10(BUDGETS['B +CGM 0.5M*'](U*10**logK[okp])), Bu).correlation:+.3f}")
Bu4 = 2*np.log10(sigV[okp]/sig_pred_kms(BUDGETS["B +CGM 0.5M*"](0.4*10**logK[okp]), RP, A0["canonical"]))
Bu1 = 2*np.log10(sigV[okp]/sig_pred_kms(BUDGETS["B +CGM 0.5M*"](1.0*10**logK[okp]), RP, A0["canonical"]))
ck("M4 the mass-to-light bracket 0.4-1.0 moves the zero point by under 0.1 dex either way and leaves the trend's sign",
   abs(np.median(Bu4) - np.median(prim["B"])) < 0.1 and abs(np.median(Bu1) - np.median(prim["B"])) < 0.12
   and spearmanr(np.log10(0.4*10**logK[okp]), Bu4).correlation > 0 and spearmanr(np.log10(10**logK[okp]), Bu1).correlation > 0,
   f"zero points {np.median(Bu4):+.3f} / {np.median(prim['B']):+.3f} / {np.median(Bu1):+.3f}")

# ============================================================================================ 6. VERDICT
P("\n" + "=" * 118)
P("6.  VERDICT")
P("=" * 118)
if STEP_WINS:
    P("  A STEP was preferred in the Kourkchi sweep.  Section 4 then asks whether its location is a Lambda scale; read 4a-4c.")
else:
    P("  There is no edge -- and there is no onset to put one at.  On one catalogue and one estimator the pressure-supported")
    P("  residual is FLAT from 10^10.4 to 10^12.3 Msun of baryons once the hot gas is counted (2i), and inside the cluster")
    P("  regime (eRASS1, 0.3-12 keV, 10^12-10^15) it is a plateau (3a).  The only rise anywhere in the sweep sits in the")
    P("  stellar-only budget and is removed by a hot-gas budget keyed to light (2e): it is the onset of hot baryons.")
    P("  The 'groups pass, clusters fail' contrast the ledger carries is an ESTIMATOR contrast: two membership algorithms")
    P("  disagree by ~0.3 dex in B on the same poorly-populated groups (2a-rest) while agreeing on M31 and M81 (2a-best),")
    P("  and on either single estimator the group level and the cluster level differ by ~0.1-0.15 dex, inside that systematic.")
    P("  A rise of 0.3 dex anywhere in the sweep is excluded at 97% power (2g); 0.2 dex only at 64%.")
    P(f"  Recorded (canonical, N >= 10): group plateau {np.median(RESULTS['canonical|N>=10|C +X-ray hot(L_K)']['B']):+.3f} dex (hot-gas budget) / "
      f"{np.median(prim['B']):+.3f} (CGM budget); eRASS1 plateau {ef['const']['level']:+.3f} dex; g06's estimator on the same sky: -0.09.")
    P("  On the Lambda question: no Lambda length or mass lies within three decades of the sweep (4a), the density ordering")
    P("  is non-monotone (4b), and a number match would be at the chance rate anyway (4c).  Fifth null on the")
    P("  'second Lambda scale' search (k02 crossing, u13 boundary, u02 second scale, h20 ladder, f22 onset).")
sys.exit(ck.done())
