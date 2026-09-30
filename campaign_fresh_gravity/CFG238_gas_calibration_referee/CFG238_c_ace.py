#!/usr/bin/env python3
"""CFG238 attack c: ACE metallicity extrapolation and the '0.2 to 0.7 dex' claim (frozen D13 and section 6c). Exit 0."""
import sys
from CFG238_common import *

outp, jp = out_paths("CFG238_c_ace")
T = Tee(outp)
banner(T, "CFG238 attack c (ACE offset: slope, range, prescriptions, conversion-free ratio, internal consistency)")
R = {}
LINES = []
HK = 0.04799  # h/k in K per GHz


def line(lid, ok, msg):
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {msg}")


def Bnu_rel(nu_ghz, Tk):
    return nu_ghz ** 3 / np.expm1(HK * nu_ghz / Tk)


AC = [r for r in load_ace() if r["both"]]
n = len(AC)
ZA = np.array([r["OH"] for r in AC]); zA = np.array([r["z"] for r in AC])
logMd = np.array([r["logMdust"] for r in AC])
logMm = np.array([math.log10(r["Mmol"] * 1e10) for r in AC])
LpCO = np.array([r["logLpCO32"] for r in AC]); Lnu = np.array([r["logLnu873"] for r in AC])
R_ace = logMd - logMm
S = load_s82()
Rs = np.array([r["logMdust"] - r["logMgas_CO"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
Zs = np.array([r["Z_12logOH"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
Zb, Rb = Zs.mean(), Rs.mean()
Xs = np.column_stack([np.ones_like(Zs), Zs])
bet, bse, rsd = ols(Xs, Rs)
bo = ols_boot(Xs, Rs, 10000, 238)
T(f"ACE N {n}: R mean {R_ace.mean():.3f} SD {R_ace.std(ddof=1):.3f}; Z mean {ZA.mean():.3f} range {ZA.min():.2f}-{ZA.max():.2f}")
T(f"Stripe82 N {len(Rs)}: R mean {Rb:.3f}; Z mean {Zb:.3f} range {Zs.min():.2f}-{Zs.max():.2f}; OLS slope {bet[1]:+.3f} (analytic SE {bse[1]:.3f}, bootstrap SD {bo[:, 1].std(ddof=1):.3f}), residual SD {rsd:.3f}")
fb = float((ZA < Zs.min()).mean())
T(f"EXTRAPOLATION: fraction of ACE galaxies with 12+log(O/H) below the lowest Stripe82 value ({Zs.min():.2f}): {fb:.2f}; ACE mean is {Zs.min() - ZA.mean():.2f} dex below the lowest S82 galaxy; S82 covers {Zs.max() - Zs.min():.2f} dex, ACE covers {ZA.max() - ZA.min():.2f} dex")
R["extrap"] = dict(frac_below=fb, s82_range=(Zs.min(), Zs.max()), ace_range=(ZA.min(), ZA.max()), gap=Zs.min() - ZA.mean())
seA = R_ace.std(ddof=1) / math.sqrt(n)


def offset(s, Rv=None, Zv=None):
    Rv = R_ace if Rv is None else Rv
    Zv = ZA if Zv is None else Zv
    if s == "OLS":
        return float((Rv - (bet[0] + bet[1] * Zv)).mean())
    return float((Rv - (Rb + s * (Zv - Zb))).mean())


T("\n== 1. Offset and K against the assumed metallicity slope s of the local relation (S82 mean intercept)")
SL = ["OLS", 0.0, 0.5, 0.85, 1.0, 1.2, 1.7, 2.0]
R["slopes"] = {}
for s in SL:
    D = offset(s)
    Kd = Kfun(D, seA)
    T(f"  s={s}: offset {D:+.3f}  K {Kd:.3f} [{Kclass(Kd)}]")
    R["slopes"][str(s)] = dict(D=D, K=Kd)
a_lin = offset(0.0)
T(f"  algebra check Delta(s) = Delta(0) + s x (Zbar_S82 - Zbar_ACE): slope coefficient {Zb - ZA.mean():.4f}; Delta(1) {a_lin + (Zb - ZA.mean()):+.4f} vs {offset(1.0):+.4f}; zero crossing s = {-a_lin / (Zb - ZA.mean()):.3f}")
for tg, nm in ((0.85, "Leroy+11 (Stripe82's own dust-to-gas, eq.13)"), (1.0, "proportional to Z"), (1.2, "ACE's own slope")):
    zs_an = (bet[1] - tg) / bse[1]; zs_bo = (bet[1] - tg) / bo[:, 1].std(ddof=1)
    T(f"  S82 OLS slope {bet[1]:+.2f} differs from {tg} ({nm}) by {abs(zs_an):.1f} sigma (analytic) / {abs(zs_bo):.1f} sigma (bootstrap)")
    R[f"sigma_vs_{tg}"] = (zs_an, zs_bo)
line("H-C12a", abs(offset(1.2) + 0.148) <= 0.015 and abs(Kfun(offset(1.2), seA) - 0.09) <= 0.015, f"s=1.2 offset {offset(1.2):+.3f} (estimate -0.15), K {Kfun(offset(1.2), seA):.3f} (estimate 0.09)")
line("H-C12b", abs(-a_lin / (Zb - ZA.mean()) - 1.68) <= 0.05, f"zero crossing {-a_lin / (Zb - ZA.mean()):.2f} (estimate 1.68)")
line("H-C13a", bet[1] < 0 and abs((bet[1] - 1.0) / bse[1]) > 4, f"S82 OLS slope negative and > 4 sigma below +1: {(bet[1] - 1.0) / bse[1]:.1f} sigma (analytic)")
# subsamples
sub = {}
for nm, msk in (("Z <= 8.85", Zs <= 8.85), ("Z >= 8.70", Zs >= 8.70), ("Z >= 8.75", Zs >= 8.75)):
    X_ = Xs[msk]; y_ = Rs[msk]
    if msk.sum() > 10:
        b_, se_, r_ = ols(X_, y_)
        bo_ = ols_boot(X_, y_, 5000, 238)
        D_ = float((R_ace - (b_[0] + b_[1] * ZA)).mean())
        sub[nm] = dict(N=int(msk.sum()), slope=float(b_[1]), se=float(se_[1]), boot_sd=float(bo_[:, 1].std()), D=D_, K=Kfun(D_, seA))
        T(f"  S82 subsample {nm}: N {msk.sum()} OLS slope {b_[1]:+.2f} +- {se_[1]:.2f} (boot {bo_[:, 1].std():.2f}); offset to ACE {D_:+.3f} K {Kfun(D_, seA):.3f}")
R["subsamples"] = sub
line("H-C13b", sub["Z >= 8.70"]["slope"] < 0, f"slope for Z >= 8.70 is {sub['Z >= 8.70']['slope']:+.2f} (estimate: still negative)")

# ------------------------------------------------------------------ 2. ACE internal consistency (H-C14, H-C15)
T("\n== 2. ACE internal consistency and recipe recomputation")
allace = load_ace()
d1 = np.array([abs(r["logMmol_b"] - math.log10(r["Mmol"] * 1e10)) for r in AC if r["logMmol_b"] is not None])
d2 = np.array([abs(r["logMdust"] - math.log10(r["Mdust21040"] * 1e7)) for r in AC if r["Mdust21040"] is not None])
T(f"  M_mol (table 2609.20926 'logMmol') vs M_mol (table 2609.21072): N {len(d1)} median |diff| {np.median(d1):.3f} max {d1.max():.3f}")
T(f"  M_dust (2609.20926) vs M_dust (2609.21040): N {len(d2)} median |diff| {np.median(d2):.3f} max {d2.max():.3f}; signed mean {np.mean([r['logMdust'] - math.log10(r['Mdust21040'] * 1e7) for r in AC if r['Mdust21040']]):+.3f}")
line("H-C14a", np.median(d1) <= 0.05, f"median |diff| of the two M_mol tables {np.median(d1):.3f} <= 0.05")
line("H-C14b", np.median(d2) <= 0.10, f"median |diff| of the two M_dust tables {np.median(d2):.3f} <= 0.10")
R["internal"] = dict(mmol_med=float(np.median(d1)), mdust_med=float(np.median(d2)))
# M_mol implied alpha
al_impl = np.log10(10 ** logMm * 0.77 / 10 ** LpCO)
al_A0 = 14.752 - 1.632 * ZA
T(f"  implied alpha_CO (from file M_mol, r31 = 0.77, L'CO32): median {10 ** np.median(al_impl):.2f}; log alpha implied minus Accurso(no Delta MS): mean {np.mean(al_impl - al_A0):+.3f} SD {np.std(al_impl - al_A0, ddof=1):.3f} (the Delta MS term is 0.062 log Delta MS)")
T(f"  [post hoc] log alpha implied minus (Accurso no Delta MS + log 1.36): mean {np.mean(al_impl - al_A0 - math.log10(1.36)):+.3f} SD {np.std(al_impl - al_A0, ddof=1):.3f}: the file's alpha_CO equals the Accurso formula times the He factor 1.36 (log 1.36 = 0.1335) to 0.01 dex on average")
R["alpha_impl"] = dict(mean_resid=float(np.mean(al_impl - al_A0)), sd=float(np.std(al_impl - al_A0, ddof=1)), median=float(10 ** np.median(al_impl)))
# dust recompute
const = {}
best = None
for lab, nu_mode in (("rest = obs x (1+z)", 1), ("rest = obs", 0)):
    nu_obs = 343.5
    nu_r = nu_obs * (1 + zA) if nu_mode else np.full(n, nu_obs)
    kap = 4.0 * (nu_r / 1199.17) ** 2.08          # cm2/g: 0.4 m2/kg at 250 um
    Bcgs = 2 * 6.626e-27 * (nu_r * 1e9) ** 3 / (2.998e10) ** 2 / np.expm1(HK * nu_r / 25.0)
    Md = 10 ** Lnu / (4 * math.pi * kap * Bcgs) / 1.989e33
    dd = np.log10(Md) - logMd
    const[lab] = (float(np.median(dd)), float(np.std(dd, ddof=1)))
    T(f"  recompute M_dust from logLnu873, T_d = 25 K, beta = 2.08, kappa = 0.4 m2/kg at 250 um ({lab}): mine - file median {np.median(dd):+.3f} SD {np.std(dd, ddof=1):.3f}")
    if best is None or abs(np.median(dd)) < abs(best[1]):
        best = (lab, float(np.median(dd)), float(np.std(dd, ddof=1)))
R["dust_recompute"] = const
line("H-C15", abs(best[1]) <= 0.05, f"best recipe ({best[0]}): median difference {best[1]:+.3f}, SD {best[2]:.3f} (estimate: within 0.05 median)")
kap850 = 4.0 * (352.73 / 1199.17) ** 2.08 * 0.1
T(f"  kappa_850 equivalent of the ACE kappa (0.4 m2/kg at 250 um, beta 2.08): {kap850:.4f} m2/kg; Dunne+22 0.071, Bourne+19 0.077 -> mass-scale difference {math.log10(0.071 / kap850):.2f} / {math.log10(0.077 / kap850):.2f} dex")
R["kappa850"] = kap850

# ------------------------------------------------------------------ 3. prescription swap grid
T("\n== 3. Prescription swap: ACE-minus-Stripe82 offset (R_ACE' - local relation) under alternative ACE alpha_CO and dust recipes (Stripe82 side unchanged)")
nu_r = 343.5 * (1 + zA)
alpha = {"file (Accurso + Delta MS)": 10 ** al_impl,
         "Accurso, no Delta MS": 10 ** al_A0,
         "Accurso x 1.36 (He), no Delta MS [post hoc]": 1.36 * 10 ** al_A0,
         "constant 4.35 (MW incl. He)": np.full(n, 4.35),
         "G12-like 4.35 x 10^(-1.3 (Z-8.67)) [from memory, unverified]": 4.35 * 10 ** (-1.3 * (ZA - 8.67))}
dust = {"T=25 K, kappa_ACE (file)": np.zeros(n)}
for Tk in (20.0, 30.0, 35.0):
    dust[f"T={Tk:.0f} K, kappa_ACE"] = np.log10(Bnu_rel(nu_r, 25.0) / Bnu_rel(nu_r, Tk))
for k850 in (0.071, 0.077):
    dust[f"T=25 K, kappa_850 = {k850}"] = np.full(n, math.log10(kap850 / k850))   # M ~ 1/kappa
grid = {}
for an, av in alpha.items():
    Mm_ = np.log10(av * 10 ** LpCO / 0.77)
    for dn, dv in dust.items():
        Rv = (logMd + dv) - Mm_
        grid[(an, dn)] = {str(s): offset(s, Rv) for s in ("OLS", 0.0, 1.0)}
T("  cells: alpha_CO variant x dust variant -> offsets at slope OLS / 0 / +1 (negative = ACE below Stripe82)")
for (an, dn), v in grid.items():
    T(f"   {an[:38]:38s} | {dn:28s} | OLS {v['OLS']:+.3f}  s0 {v['0.0']:+.3f}  s+1 {v['1.0']:+.3f}")
rng_ = {k: (min(v[k] for v in grid.values()), max(v[k] for v in grid.values())) for k in ("OLS", "0.0", "1.0")}
T(f"  range of the offset across the {len(grid)} prescription cells: OLS {rng_['OLS'][0]:+.3f} to {rng_['OLS'][1]:+.3f} (span {rng_['OLS'][1] - rng_['OLS'][0]:.2f}); slope 0 {rng_['0.0'][0]:+.3f} to {rng_['0.0'][1]:+.3f} (span {rng_['0.0'][1] - rng_['0.0'][0]:.2f}); slope +1 {rng_['1.0'][0]:+.3f} to {rng_['1.0'][1]:+.3f} (span {rng_['1.0'][1] - rng_['1.0'][0]:.2f})")
R["grid"] = {f"{a}|{d}": v for (a, d), v in grid.items()}
R["grid_range"] = rng_
mw = grid[("constant 4.35 (MW incl. He)", "T=25 K, kappa_ACE (file)")]
T(f"  constant-MW alpha_CO only (dust as in the file): offset to S82 mean {mw['0.0']:+.3f} (frozen comparison: {offset(0.0):+.3f})")
line("H-C11", abs(mw["0.0"]) < 0.30, f"ACE with constant MW alpha_CO: offset to S82 mean {mw['0.0']:+.3f} (estimate: shrinks below 0.30 from 0.52)")
T(f"  disagreement (i): offset moves by more than 0.3 dex across the prescription swaps at fixed slope? OLS {rng_['OLS'][1] - rng_['OLS'][0]:.2f}, s0 {rng_['0.0'][1] - rng_['0.0'][0]:.2f}, s+1 {rng_['1.0'][1] - rng_['1.0'][0]:.2f}  ->  {any(rng_[k][1] - rng_[k][0] > 0.3 for k in rng_)}")

# ------------------------------------------------------------------ 4. conversion-free comparison
T("\n== 4. Conversion-free luminosity ratio: ACE log(L_850,rest / L'CO(1-0)) vs local Dunne CO+dust galaxies (z < 0.6)")
M, keys = load_master()
loc = []; locp = []
for r in M:
    z_, l8, lc = fl(r["z"]), fl(r["logL850py"]), fl(r["logLCO"])
    if z_ is not None and z_ < 0.6 and l8 is not None and lc is not None:
        loc.append(l8 - lc)
        if lc > 0:
            locp.append(l8 - lc)
loc = np.array(loc); locp = np.array(locp)
T(f"  NOTE: {len(loc) - len(locp)} of the {len(loc)} local rows have non-positive log L'CO (catalogue placeholders, log L'CO down to -9.4: implausible as luminosities); the frozen rule (all finite) is scored; the rows with log L'CO > 0 are a labelled POST HOC variant: N {len(locp)} mean {locp.mean():.3f} SD {locp.std(ddof=1):.3f} median {np.median(locp):.3f}")
T(f"  local (master z<0.6, L850py and L'CO both): N {len(loc)} mean {loc.mean():.3f} SD {loc.std(ddof=1):.3f} SE {loc.std(ddof=1) / math.sqrt(len(loc)):.3f} (log of L850[W/Hz]/L'CO[K km/s pc2])")
fr = {}
for Tk in (20.0, 25.0, 30.0, 35.0):
    nu2 = 343.5 * (1 + zA)
    mv = (352.73 / nu2) ** 2.08 * Bnu_rel(352.73, Tk) / Bnu_rel(nu2, Tk)
    L850 = Lnu - 7 + np.log10(mv)
    Rl = L850 - (LpCO - math.log10(0.77))
    fr[Tk] = Rl
    T(f"  ACE frame moved to rest 850 um at T = {Tk:.0f} K, beta 2.08: log(L850/L'CO10) mean {Rl.mean():.3f} SD {Rl.std(ddof=1):.3f} (r31 0.77); ACE minus local (frozen, all finite) {Rl.mean() - loc.mean():+.3f} +- {math.sqrt(Rl.var(ddof=1) / n + loc.var(ddof=1) / len(loc)):.3f}; POST HOC (log L'CO > 0) {Rl.mean() - locp.mean():+.3f} +- {math.sqrt(Rl.var(ddof=1) / n + locp.var(ddof=1) / len(locp)):.3f}")
R["convfree"] = dict(local_mean=float(loc.mean()), local_sd=float(loc.std(ddof=1)), local_pos_mean=float(locp.mean()), local_pos_sd=float(locp.std(ddof=1)), diff_pos={str(k): float(v.mean() - locp.mean()) for k, v in fr.items()}, ace={str(k): float(v.mean()) for k, v in fr.items()}, diff={str(k): float(v.mean() - loc.mean()) for k, v in fr.items()})
d25 = fr[25.0].mean() - loc.mean()
line("H-C16", abs(d25) < 0.25, f"ACE minus local conversion-free ratio at T 25 K {d25:+.3f} (estimate within 0.25); range over T 20-35 K: {min(v.mean() for v in fr.values()) - loc.mean():+.3f} to {max(v.mean() for v in fr.values()) - loc.mean():+.3f}")
d25p = fr[25.0].mean() - locp.mean()
T(f"  [INFO] H-C16post (post hoc, rows with log L'CO > 0): ACE minus local at 25 K {d25p:+.3f}; over T 20-35 K {min(v.mean() for v in fr.values()) - locp.mean():+.3f} to {max(v.mean() for v in fr.values()) - locp.mean():+.3f}; within 0.25: {abs(d25p) < 0.25}")
# within-ACE dependence of the observable ratio on Z
ratio_obs = Lnu - LpCO
bz, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), ZA]), ratio_obs, rcond=None)
T(f"  within ACE: observable log(Lnu873/L'CO32) versus 12+log(O/H): slope {bz[1]:+.2f} (ACE abstract-level statement: nearly constant)")
R["ace_obs_slope"] = float(bz[1])
T("  what the 0.21-0.67 means: a mass-level offset between two prescription sets; the conversion-free ratio comparison above is the part that does not depend on alpha_CO or dust opacity.")
R["lines"] = LINES
dump(jp, R)
T.close()
sys.exit(0)
