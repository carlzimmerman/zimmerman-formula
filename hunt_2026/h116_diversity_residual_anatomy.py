#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h116_diversity_residual_anatomy.py -- HUNT ITEM 116: what is left over after the inner-curve diversity prediction?
===================================================================================================================
Item 23 predicted the inner rotation-curve DIVERSITY -- v(2 kpc)/v_flat -- from the baryonic profile alone, with zero
halo freedom: r = 0.79 across the full observed range, rms residual 0.15 (`h3_h21_h23_structure.py`).  0.15 is well
above the RAR's own 0.06 dex, and the ledger recorded that honestly.  Item 116 asks what the 0.15 IS.

The framework's wish is sharp and falsifiable: the residual should be OBSERVATIONAL.  A correlation with a measurement
systematic (inclination, distance, resolution, quality) supports the framework; a correlation with a PHYSICAL property
(gas fraction, mass, morphology, surface brightness) does not, because the framework has no freedom left to absorb one.

Three independent attacks, because a residual can be observational in two different ways and the tests differ:
  (1) MEAN-SHIFT correlations.  A systematic that biases a measurement shifts the residual's MEAN with the offending
      quantity.  Sixteen predictors, declared in advance as systematic / physical / M/L, Spearman rank, with a
      permutation look-elsewhere test on max |rho| -- not a per-predictor p-value.
  (2) VARIANCE splits.  Random measurement error inflates the residual's SCATTER, not its mean.  Split by quality flag,
      distance method, resolution and by the quoted error itself, and compare rms.
  (3) THE ERROR BUDGET, by Monte Carlo.  Perturb each galaxy by its own quoted distance error, inclination error and
      velocity errors, and by the stellar-population scatter in Upsilon, re-run item 23's estimator end to end, and see
      how much of the 0.15 the observations alone produce.  This is the test with teeth and it is the one that answers.

Bug patterns watched for: (5) an M/L result wearing a_0's clothes -- the bulge coefficient turns out to be exactly that,
and the lever is quoted; (1) the 2 kpc aperture is a FIXED PHYSICAL radius, so a distance error moves which part of the
curve is sampled -- that turns out to be the single largest term.  Both footings.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy import stats
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(116)

# ---------------------------------------------------------------- the distance-method flag, which read_master drops
def read_fD():
    """SPARC column f_D (bytes 25-26): 1 = Hubble flow, 2 = TRGB, 3 = Cepheid, 4 = Ursa Major cluster, 5 = SN Ia."""
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    by_split, by_fixed = {}, {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) >= 18:
            try: by_split[f[0]] = int(f[4])
            except ValueError: pass
        if len(line) >= 99:
            try: by_fixed[line[0:11].strip()] = int(line[24:26])
            except ValueError: pass
    return by_split, by_fixed
FD, FD_FIXED = read_fD()
disagree = sum(1 for k in FD if k in FD_FIXED and FD[k] != FD_FIXED[k])
P("="*116); P("ITEM 116 -- the anatomy of the inner-diversity residual"); P("="*116); P("")
ck("P0 the master table parses the same way whitespace-split and fixed-width, so the distance-method flag is the real one (a guard against silently mis-columned .mrt fields)",
   disagree == 0 and len(FD) == 175,
   f"{len(FD)} rows both ways, {disagree} disagreements; distance methods: " + ", ".join(f"{k}:{sum(1 for v in FD.values() if v==k)}" for k in sorted(set(FD.values()))))

gals = load_sparc()
A0_CAN = A0["canonical"]

def item23_residuals(ups_d=UPS_D, ups_b=UPS_B, a0=A0_CAN, dD=None, dinc=None, dv=None, gl=None):
    """item 23's estimator, verbatim, with optional per-galaxy perturbations for the Monte-Carlo budget.
    dD is a multiplicative distance factor (r -> dD r, v_bar -> sqrt(dD) v_bar);  dinc is a shift in degrees applied to
    v_obs through sin i;  dv is a PER-POINT fractional velocity perturbation (SPARC's e_Vobs is a per-ring error, so a
    single galaxy-wide scaling would be the wrong model -- it would largely cancel in the ratio v(2 kpc)/v_flat and
    would double-count the coherent inclination mode, which has its own term)."""
    out = []
    for gi, g in enumerate(gl if gl is not None else gals):
        f = 1.0 if dD is None else dD[gi]
        r = g["r"]*f
        v = g["vobs"].copy()
        if dinc is not None and dinc[gi]:
            v = v*math.sin(math.radians(g["inc"]))/math.sin(math.radians(float(np.clip(g["inc"]+dinc[gi], 5.0, 90.0))))
        if dv is not None: v = v*(1.0 + dv[gi])           # dv[gi] is an ARRAY, one entry per ring
        vg, vd, vb = g["vg"]*math.sqrt(f), g["vd"]*math.sqrt(f), g["vb"]*math.sqrt(f)
        gbar = (vg*np.abs(vg) + ups_d*vd**2 + ups_b*vb**2)/r*KMS2_KPC
        if r[0] > 2.0 or r[-1] < 6.0: continue
        vf = float(np.median(v[-3:]))
        if vf <= 0: continue
        gb2 = float(np.interp(2.0, r, gbar))
        if gb2 <= 0: continue
        v2 = float(np.interp(2.0, r, v))
        vp = math.sqrt(gb2*nu_s(gb2/a0)*2.0*kpc)/1e3
        out.append((gi, g["name"], v2/vf, vp/vf, v2/vf - vp/vf))
    return out

base = item23_residuals()
names = [b[1] for b in base]; obs = np.array([b[2] for b in base]); pred = np.array([b[3] for b in base])
d = np.array([b[4] for b in base]); idx = [b[0] for b in base]
sel = [gals[i] for i in idx]
r23 = float(np.corrcoef(obs, pred)[0, 1])
info(f"item 23 reproduced: N = {len(d)} galaxies, correlation r = {r23:.3f}, residual mean {d.mean():+.4f}, rms {d.std():.4f}; observed range {obs.min():.2f}-{obs.max():.2f}")
ck("P1 item 23 is reproduced exactly from the ledger's numbers before anything is done to its residual",
   abs(r23 - 0.79) < 0.02 and abs(d.std() - 0.15) < 0.01 and len(d) > 100,
   f"r = {r23:.3f} (ledger 0.79), rms = {d.std():.4f} (ledger 0.15), N = {len(d)} (ledger's range 0.22-1.23, here {obs.min():.2f}-{obs.max():.2f})")
for foot, a0 in A0.items():
    dd = np.array([b[4] for b in item23_residuals(a0=a0)])
    info(f"{foot:10} residual mean {dd.mean():+.4f}, rms {dd.std():.4f}")
d_alt = np.array([b[4] for b in item23_residuals(a0=A0["alt"])])
ck("P2 AGAINST INTEREST -- this residual carries no information about a_0 at all.  The two footings, 0.08 dex apart, give residual scatters that differ by under 0.2%.  Whatever the 0.15 is, it cannot be used to measure or to test a_0",
   abs(d.std() - d_alt.std())/d.std() < 0.01,
   f"canonical rms {d.std():.4f}, alt rms {d_alt.std():.4f}: {100*abs(d.std()-d_alt.std())/d.std():.2f}% apart")

# ---------------------------------------------------------------- (1) mean-shift correlations
P(""); P("-"*116); P("(1) MEAN-SHIFT CORRELATIONS -- sixteen predictors, classified in advance"); P("-"*116)
def gas_frac(g):
    ms = UPS_D*g["L36"]*1e9; mg = 1.33*g["MHI"]*1e9; return mg/(mg+ms) if mg+ms > 0 else np.nan
def disc_frac_at2(g):
    r = g["r"]; vd = float(np.interp(2.0, r, g["vd"])); vb = float(np.interp(2.0, r, g["vb"]))
    gb = float(np.interp(2.0, r, g["gbar"]))
    return ((UPS_D*vd**2 + UPS_B*vb**2)/2.0*KMS2_KPC)/gb if gb > 0 else np.nan
PRED = [
    ("inclination [deg]",        "systematic", lambda g: g["inc"]),
    ("e_inclination [deg]",      "systematic", lambda g: g["einc"]),
    ("e_D/D",                    "systematic", lambda g: g["eD"]/max(g["D"], 1e-9)),
    ("distance [Mpc]",           "systematic", lambda g: g["D"]),
    ("distance method f_D",      "systematic", lambda g: FD.get(g["name"], 0)),
    ("quality flag Q",           "systematic", lambda g: g["Q"]),
    ("2 kpc in arcsec",          "systematic", lambda g: 2.0/g["D"]*206.265),
    ("N points inside 2 kpc",    "systematic", lambda g: float((g["r"] < 2.0).sum())),
    ("innermost radius [kpc]",   "systematic", lambda g: g["r"][0]),
    ("Hubble type T",            "physical",   lambda g: g["T"]),
    ("gas fraction",             "physical",   gas_frac),
    ("log M_bar",                "physical",   lambda g: math.log10(max(g["Mb"], 1.0))),
    ("central SB_disk",          "physical",   lambda g: g["SBdisk"]),
    ("V_flat [km/s]",            "physical",   lambda g: g["Vflat"]),
    ("stellar share of g_bar(2kpc)", "M/L",    disc_frac_at2),
    ("has a bulge",              "M/L",        lambda g: 1.0 if np.any(g["vb"] > 0) else 0.0),
]
X = np.array([[f(g) for _, _, f in PRED] for g in sel], dtype=float)
info(f"{'predictor':32} {'class':11} {'Spearman rho':>13} {'p (nominal)':>12}")
rhos = []
for j, (nm, kd, _) in enumerate(PRED):
    m = np.isfinite(X[:, j])
    rho, p = stats.spearmanr(X[m, j], d[m]) if len(set(X[m, j])) > 1 else (0.0, 1.0)
    rhos.append(rho); info(f"{nm:32} {kd:11} {rho:+13.3f} {p:12.2e}" + ("   <- best" if abs(rho) == max(abs(np.array(rhos))) and j == int(np.argmax(np.abs(rhos))) else ""))
rhos = np.array(rhos)
obs_max = float(np.abs(rhos).max()); best_j = int(np.argmax(np.abs(rhos)))
sysj = [j for j, (_, k, _) in enumerate(PRED) if k == "systematic"]
phyj = [j for j, (_, k, _) in enumerate(PRED) if k == "physical"]
def maxrho(dd, cols):
    return max(abs(stats.spearmanr(X[np.isfinite(X[:, j]), j], dd[np.isfinite(X[:, j])])[0]) for j in cols)
perm_all, perm_sys, perm_phy = [], [], []
for _ in range(3000):
    dp = rng.permutation(d)
    perm_all.append(maxrho(dp, range(len(PRED)))); perm_sys.append(maxrho(dp, sysj)); perm_phy.append(maxrho(dp, phyj))
perm_all, perm_sys, perm_phy = map(np.array, (perm_all, perm_sys, perm_phy))
p_global = float((perm_all >= obs_max).mean())
ms, mp = maxrho(d, sysj), maxrho(d, phyj)
info(f"best predictor overall: {PRED[best_j][0]} ({PRED[best_j][1]}), |rho| = {obs_max:.3f}")
info(f"permutation look-elsewhere null on max |rho| over all 16: median {np.median(perm_all):.3f}, 95th {np.percentile(perm_all,95):.3f}  ->  GLOBAL p = {p_global:.3f}")
info(f"best SYSTEMATIC |rho| = {ms:.3f} (global p over the 9 systematics {float((perm_sys>=ms).mean()):.3f});  best PHYSICAL |rho| = {mp:.3f} (global p over the 5 physicals {float((perm_phy>=mp).mean()):.3f})")
info(f"with N = {len(d)} this machinery can detect |rho| >= {math.sqrt(stats.chi2.ppf(1-0.05/len(PRED),1)/(len(d)-1)):.3f} at a look-elsewhere-corrected 5% -- nothing here reaches it")
ck("116A AGAINST INTEREST -- no predictor correlates with the residual once the look-elsewhere effect is paid for.  Inclination is the strongest at rho = -0.26, nominally p = 0.008, but the permutation null for the largest of sixteen correlations puts it at a GLOBAL p of 0.10.  The item's question cannot be answered by mean-shift correlations on 106 galaxies",
   p_global > 0.05,
   f"max |rho| = {obs_max:.3f} on '{PRED[best_j][0]}', global p = {p_global:.3f}; detectable |rho| at corrected 5% is {math.sqrt(stats.chi2.ppf(1-0.05/len(PRED),1)/(len(d)-1)):.3f}")
ck("116B the DIRECTION nonetheless favours the framework's wish: the best systematic beats the best physical property, and it does so on a class of nine predictors versus five",
   ms > mp, f"best systematic {ms:.3f} ({PRED[int(np.argmax([abs(rhos[j]) if j in sysj else 0 for j in range(len(PRED))]))][0]}) vs best physical {mp:.3f} ({PRED[int(np.argmax([abs(rhos[j]) if j in phyj else 0 for j in range(len(PRED))]))][0]})")

# ---------------------------------------------------------------- the bulge coefficient is an M/L statement
P(""); P("-"*116); P("THE BULGE COEFFICIENT IS AN UPSILON STATEMENT (bug pattern 5, caught in the act)"); P("-"*116)
has_b = np.array([1.0 if np.any(g["vb"] > 0) else 0.0 for g in sel])
info(f"{'Upsilon_bulge':>14} {'bulged mean':>12} {'bulgeless':>11} {'difference':>11} {'overall rms':>12}")
diffs = []
for ub in (0.3, 0.4, 0.5, 0.52, 0.6, 0.7, 0.9, 1.2):
    dd = np.array([b[4] for b in item23_residuals(ups_b=ub)])
    diffs.append((ub, dd[has_b > 0].mean() - dd[has_b == 0].mean()))
    info(f"{ub:14.2f} {dd[has_b>0].mean():+12.4f} {dd[has_b==0].mean():+11.4f} {diffs[-1][1]:+11.4f} {dd.std():12.4f}")
null_ub = np.interp(0.0, [x[1] for x in diffs][::-1], [x[0] for x in diffs][::-1])
t_b = stats.ttest_ind(d[has_b > 0], d[has_b == 0], equal_var=False)
ck("116C the 'bulge' correlation is not physics and not a_0: it is the assumed bulge mass-to-light ratio.  At the committed Upsilon_b = 0.7 the 22 bulged galaxies sit 0.092 BELOW the bulgeless ones (p = 0.02); the offset passes through zero at Upsilon_b = 0.52, and every physical correlation in the table above dies with it",
   abs(null_ub - 0.7) > 0.1 and t_b.pvalue < 0.10,
   f"bulged - bulgeless = {d[has_b>0].mean()-d[has_b==0].mean():+.4f} at Upsilon_b = 0.70 (Welch p = {t_b.pvalue:.3f}); the offset nulls at Upsilon_b = {null_ub:.2f}, i.e. essentially the disc value")
sub_j = [j for j in range(len(PRED)) if PRED[j][1] == "physical"]
d_nb = d[has_b == 0]; X_nb = X[has_b == 0]
info("the same table on the 84 BULGELESS galaxies, where no bulge M/L is assumed:")
for j, (nm, kd, _) in enumerate(PRED):
    m = np.isfinite(X_nb[:, j])
    if len(set(X_nb[m, j])) < 2: continue
    rho, p = stats.spearmanr(X_nb[m, j], d_nb[m])
    info(f"   {nm:32} {kd:11} rho = {rho:+.3f}  p = {p:.3f}")
best_phy_nb = max(abs(stats.spearmanr(X_nb[np.isfinite(X_nb[:, j]), j], d_nb[np.isfinite(X_nb[:, j])])[0]) for j in phyj)
best_sys_nb = max(abs(stats.spearmanr(X_nb[np.isfinite(X_nb[:, j]), j], d_nb[np.isfinite(X_nb[:, j])])[0]) for j in sysj)
ck("116D on the bulgeless subsample every PHYSICAL correlation dissolves (best |rho| falls from 0.21 to 0.18, nominal p = 0.11) while inclination survives as the strongest single correlate.  The gas-fraction and mass 'signals' of the full sample were the bulge M/L in disguise",
   best_sys_nb >= best_phy_nb,
   f"bulgeless: best systematic |rho| = {best_sys_nb:.3f}, best physical |rho| = {best_phy_nb:.3f}, N = {len(d_nb)}, rms {d_nb.std():.4f}")

# ---------------------------------------------------------------- the Monte-Carlo error budget (computed here, printed as section 3)
NMC = 300
def induced(kind):
    """returns (global rms induced on the residual, per-galaxy rms) for one error source"""
    acc = []
    for _ in range(NMC):
        kw = {}
        if kind == "velocity":
            kw["dv"] = [rng.normal(0, np.clip(gals[i]["ev"]/gals[i]["vobs"], 0.005, 0.5)) for i in range(len(gals))]
        elif kind == "distance":
            kw["dD"] = np.array([max(0.2, rng.normal(1.0, gals[i]["eD"]/max(gals[i]["D"], 1e-9))) for i in range(len(gals))])
        elif kind == "inclination":
            kw["dinc"] = np.array([rng.normal(0, max(gals[i]["einc"], 1.0)) for i in range(len(gals))])
        elif kind == "Upsilon":
            u = 0.5*10**rng.normal(0, 0.11)
            kw = dict(ups_d=u, ups_b=UPS_B*u/UPS_D)
        pert = {b[1]: b[4] for b in item23_residuals(**kw)}
        acc.append([pert.get(n, np.nan) for n in names])
    A = np.array(acc) - d[None, :]
    return float(np.sqrt(np.nanmean(A**2))), np.sqrt(np.nanmean(A**2, axis=0))
budget, sig_gal = {}, {}
for kind in ("velocity", "distance", "inclination", "Upsilon"):
    budget[kind], sig_gal[kind] = induced(kind)
sig_tot = np.sqrt(sum(v**2 for v in sig_gal.values()))    # per-galaxy predicted observational sigma

# ---------------------------------------------------------------- (2) variance splits
P(""); P("-"*116); P("(2) VARIANCE SPLITS -- random error inflates SCATTER, not the mean"); P("-"*116)
info("'predicted' below is the rms the Monte-Carlo budget says each half should have, given a common unexplained floor")
floor2 = max(d.var() - float(np.nanmean(sig_tot**2)), 0.0)
def vsplit(nm, mask, l1, l2):
    a, b = d[mask], d[~mask]
    pa = math.sqrt(floor2 + float(np.nanmean(sig_tot[mask]**2))); pb = math.sqrt(floor2 + float(np.nanmean(sig_tot[~mask]**2)))
    lev = stats.levene(a, b)
    info(f"{nm:30} {l1:24} N={len(a):3d} rms={a.std():.4f} | {l2:22} N={len(b):3d} rms={b.std():.4f}   ratio {a.std()/b.std():.2f} (predicted {pa/pb:.2f}), Levene p = {lev.pvalue:.3f}")
    return a.std()/b.std(), lev.pvalue, pa/pb
inc = X[:, 0]; eD = X[:, 2]; ang = X[:, 6]; Q = X[:, 5]; fdm = X[:, 4]
ratios = []
ratios.append(vsplit("quality flag", Q == 1, "Q = 1 (high)", "Q = 2 (medium)"))
ratios.append(vsplit("distance method", fdm == 1, "Hubble flow", "direct"))
ratios.append(vsplit("inclination", inc >= np.median(inc), "i >= median", "i < median"))
ratios.append(vsplit("distance error", eD >= np.median(eD), "e_D/D above median", "below median"))
ratios.append(vsplit("angular size of 2 kpc", ang >= np.median(ang), "well resolved", "poorly resolved"))
ratios.append(vsplit("the budget's own sigma", sig_tot >= np.median(sig_tot), "predicted sigma high", "predicted sigma low"))
n2 = len(d)//2
Fcrit = stats.f.ppf(0.975, n2-1, n2-1)
hi = sig_tot >= np.median(sig_tot)
obs_var_ratio = d[hi].var(ddof=1)/d[~hi].var(ddof=1); pred_var_ratio = ratios[-1][2]**2
p_alloc = float(stats.f.cdf(obs_var_ratio/pred_var_ratio, hi.sum()-1, (~hi).sum()-1))
info(f"the last split is the sharp one: it divides the sample by the budget's OWN predicted per-galaxy sigma, so it is where")
info(f"the budget makes its strongest prediction -- variance ratio {pred_var_ratio:.2f} predicted, {obs_var_ratio:.2f} observed, and the F test")
info(f"at {hi.sum()} vs {(~hi).sum()} galaxies resolves anything above {Fcrit:.2f}.  Under the budget's model the observed ratio has p = {p_alloc:.1e}.")
ck("116E AGAINST MY OWN ESTIMATOR -- the budget's TOTAL is right (check 116F) but its PER-GALAXY ALLOCATION is refuted.  Split by the budget's own predicted sigma, it demands a variance ratio near 2.8 between the halves; the data give 0.9, in the opposite direction, and this is the one split an F test on 53 galaxies a side can actually resolve.  The most likely culprit is SPARC's Hubble-flow distance allowances -- a blanket 14-30% covering peculiar-velocity systematics, treated here as Gaussian per-galaxy errors, which over-assigns scatter to exactly the galaxies carrying the largest quoted e_D",
   pred_var_ratio > Fcrit and obs_var_ratio < pred_var_ratio and p_alloc < 0.01,
   f"predicted variance ratio {pred_var_ratio:.2f} (resolvable threshold {Fcrit:.2f}), observed {obs_var_ratio:.2f}, p = {p_alloc:.1e}; the other five splits are all within noise (largest observed rms ratio {max(r for r,_,_ in ratios):.2f}, smallest Levene p {min(p for _,p,_ in ratios):.3f}) and none of them is resolvable")
info("Consequence: the 81% observational share below is a match of TOTALS, not a demonstration that the residual is")
info("distributed the way the quoted errors say it is.  Quote it with that caveat attached.")

# ---------------------------------------------------------------- (3) the Monte-Carlo error budget
P(""); P("-"*116); P("(3) THE ERROR BUDGET -- perturb each galaxy by its own quoted errors and re-run item 23 end to end"); P("-"*116)
for kind in ("velocity", "distance", "inclination", "Upsilon"):
    info(f"{kind:14}: re-running item 23 with this error alone induces an rms of {budget[kind]:.4f} on the residual")
tot = math.sqrt(sum(v*v for v in budget.values()))
unex = math.sqrt(max(d.var() - tot*tot, 0.0))
info(f"{'quadrature sum':14}: {tot:.4f}     observed residual rms: {d.std():.4f}     implied unexplained: {unex:.4f}")
info(f"observational share of the VARIANCE: {100*tot*tot/d.var():.0f}%")
ck("116F (the answer, with check 116E's caveat attached) IN TOTAL the residual is mostly observational -- 81% of its variance.  Re-running item 23's estimator with each galaxy's own quoted distance error, inclination error and velocity errors, plus the stellar-population scatter in Upsilon, produces 0.139 of the observed 0.154 rms with nothing tuned.  The LARGEST single term is the DISTANCE, at 0.087, because '2 kpc' is a fixed PHYSICAL aperture and a distance error changes which part of the rotation curve is sampled.  116E shows this agreement is between totals only",
   tot > 0.75*d.std() and budget["distance"] == max(budget.values()),
   f"velocity {budget['velocity']:.4f}, distance {budget['distance']:.4f}, inclination {budget['inclination']:.4f}, Upsilon {budget['Upsilon']:.4f} -> quadrature {tot:.4f} vs observed {d.std():.4f}; unexplained {unex:.4f} ({100*unex**2/d.var():.0f}% of the variance)")
ck("116G what is NOT observational is a residual of about 0.066 in v(2 kpc)/v_flat, roughly 10% in velocity, and this script does not identify it.  The leading suspects are known repo bug patterns rather than the kernel: item 23 applies the SPHERICAL relation g_obs = nu(g_bar/a_0) g_bar to a DISC (bug pattern 2 -- the AQUAL/QUMOND disc correction is a few per cent to ten per cent in v and varies with disc shape), and Upsilon varies galaxy to galaxy beyond the 0.11 dex assumed here",
   unex > 0.02,
   f"unexplained rms {unex:.4f} on a ratio whose median value is {np.median(obs):.2f}, i.e. {100*unex/np.median(obs):.0f}% in v(2 kpc); the observational budget already covers {100*tot*tot/d.var():.0f}% of the variance")

# ---------------------------------------------------------------- mutation
P(""); P("-"*116); P("MUTATION CONTROL"); P("-"*116)
fake = rng.normal(size=len(d))
info(f"a random column correlates with the residual at rho = {stats.spearmanr(fake, d)[0]:+.3f} (p = {stats.spearmanr(fake, d)[1]:.3f})")
d_shuf = rng.permutation(d)
info(f"shuffling the residual across galaxies: best |rho| over the 16 predictors = {maxrho(d_shuf, range(len(PRED))):.3f} (measured {obs_max:.3f}; permutation 95th percentile {np.percentile(perm_all,95):.3f})")
ck("M116 the machinery has no built-in signal: a random column finds nothing, and a shuffled residual reproduces the same size of 'best correlation' the real one does -- which is the point of check 116A",
   abs(stats.spearmanr(fake, d)[0]) < 0.25 and maxrho(d_shuf, range(len(PRED))) < 0.4,
   f"random column rho = {stats.spearmanr(fake,d)[0]:+.3f}; shuffled best |rho| = {maxrho(d_shuf, range(len(PRED))):.3f} vs measured {obs_max:.3f}")

P(""); P("="*116); P("VERDICT -- item 116"); P("="*116)
P("  The framework's wish is GRANTED by the budget and NOT by the correlations, and the two are not in conflict.")
P("")
P("  Granted, in total: an end-to-end Monte Carlo of SPARC's own quoted errors -- distance, inclination, velocity --")
P("  plus the 0.11 dex stellar-population scatter in Upsilon reproduces 0.139 of the observed 0.154 rms, i.e. 81% of")
P("  the variance, with nothing fitted.  The largest single contributor is the distance error acting through a FIXED")
P("  PHYSICAL 2 kpc aperture, which is a feature of item 23's estimator and not of the framework.")
P("")
P("  Not granted, twice.  (i) No single predictor correlates significantly once the look-elsewhere effect over sixteen")
P("  predictors is paid for (global p = 0.10).  The strongest correlate is a systematic (inclination, rho = -0.26) and")
P("  the strongest PHYSICAL ones -- gas fraction and mass -- were the assumed BULGE mass-to-light ratio in disguise:")
P("  the bulged/bulgeless offset nulls at Upsilon_b = 0.52 and every physical correlation dissolves on the bulgeless")
P("  subsample.  That is the hunt's bug pattern 5, caught again.  (ii) More seriously, and against my own estimator:")
P("  the budget's per-galaxy ALLOCATION is refuted.  Split by the budget's own predicted sigma it demands a variance")
P("  ratio near 2.8 between the halves; the data give 0.9, in the opposite direction, and that split is the one an F")
P("  test on this sample can resolve.  So the 81% is an agreement of TOTALS.  The honest reading is that SPARC's")
P("  blanket Hubble-flow distance allowances (14-30%, one value per method) are not Gaussian per-galaxy errors.")
P("")
P("  Left over: about 0.066 in the ratio, roughly 10% in v(2 kpc), unexplained.  It is NOT an a_0 effect -- the two")
P("  footings give the same scatter to 0.2%, so item 23's residual is useless as an a_0 diagnostic -- and the leading")
P("  suspect is that item 23 uses the SPHERICAL kernel relation on a DISC.  Closing that gap needs the repository's")
P("  own AQUAL/QUMOND disc solve, not another correlation.")
sys.exit(ck.done())
