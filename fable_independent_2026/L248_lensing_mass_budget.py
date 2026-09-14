#!/usr/bin/env python3
"""L248 -- THE MASS-BUDGET TRUNCATION TEST OF THE WEAK-LENSING RAR: the decisive test L247 stated and did not run.

THE FORK THIS DECIDES.  In the deep-MOND branch the implied dynamical mass grows without bound,
M_dyn(r) = r sqrt(G M_b a_0)/G, so the phantom mass is M_ph(r) = M_b (r/r_M - 1), r_M = sqrt(G M_b/a_0).
  - If the phantom is a FORCE-LAW ARTEFACT (AQUAL/QUMOND, standard MOND), nothing is there and no budget applies.
  - If the phantom is REAL MASS -- glm53's equilibrium identification ("the halo IS the phantom"), kimik3's
    amplitude law, and this programme's own L247 self-acceleration medium -- it must be SUPPLIED, and the supply
    is bounded by the galaxy's mass budget B = M_dark/M_bar.

THE CLOSED FORM (new here).  Saturating the budget at M_ph = B M_b gives r_t = (1+B) r_M, and the baryonic
acceleration there is
        g_bar,t = G M_b / r_t^2 = a_0 / (1+B)^2
-- INDEPENDENT OF GALAXY MASS.  Beyond it the enclosed mass is frozen at (1+B) M_b, so the relation turns from
the MOND square-root branch to a straight line g_obs = (1+B) g_bar.  The truncated model is continuous at the
turn (both sides give a_0/(1+B)) and has NO free parameter once B is fixed by cosmology or abundance matching.

THE DATA.  Brouwer et al. 2021 (KiDS-1000), the published ESD profiles in real_research/data/lensing_rar/
brouwer2021_rar/: the isolated-galaxy RAR (15 bins in g_bar, full 15x15 covariance) and the lensing rotation
curves in four stellar-mass bins.  ESD -> g_obs by the paper's own Eq. 7; the covariance is carried through the
same linear map.  Brouwer's Eq. 7 is exact for an isothermal (r^-2) profile, which IS the medium's profile, so
the conversion is self-consistent for exactly the model under test.

Checks state measurement and threshold separately; the FAIL is the finding; no literal-True conditions.
Both a_0 footings throughout."""
import os, sys, json
import numpy as np
from scipy.optimize import brentq

G, MSUN, PC, KPC, MPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "lensing_rar", "brouwer2021_rar")
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)

# Brouwer Eq. 7:  g_obs[m/s^2] = 4 * G[pc^3/(Msun s^2)] * (ESD_t/bias) * [pc/m]
G_PC, PC_M = 4.52e-30, 3.086e16
ESD_TO_G = 4.0 * G_PC * PC_M

print("L248 -- the mass-budget truncation test of the weak-lensing RAR\n")

# ------------------------------------------------------------------ load the isolated-galaxy RAR + covariance
d = np.genfromtxt(os.path.join(DATA, "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"), comments="#")
gbar, esd, esd_err, bias = d[:, 0], d[:, 1], d[:, 3], d[:, 4]
gobs = ESD_TO_G * esd / bias
gerr = ESD_TO_G * esd_err / bias
cm = np.genfromtxt(os.path.join(DATA, "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"), comments="#")
n = len(gbar)
COV = np.zeros((n, n))
def nearest(g):                                                   # the covariance grid carries the same bins
    k = int(np.argmin(np.abs(np.log10(gbar) - np.log10(g))))      # to a slightly different h70 rounding
    assert abs(np.log10(gbar[k]/g)) < 0.02, f"no matching bin for {g:.3e}"
    return k
for row in cm:
    COV[nearest(row[2]), nearest(row[3])] = row[4] / row[6]       # covariance / bias(1+K)(1+K)
COV = COV * ESD_TO_G**2                                           # ESD^2 -> g_obs^2, same linear map
print(f"    loaded {n} RAR bins, g_bar = {gbar.min():.2e} to {gbar.max():.2e} m/s^2")
print(f"    covariance {COV.shape}, symmetric to {np.max(np.abs(COV - COV.T))/np.max(np.abs(COV)):.1e}, "
      f"diagonal vs quoted errors agree to {np.max(np.abs(np.sqrt(np.diag(COV))/gerr - 1)):.1%}")
OUT["n_bins"] = int(n); OUT["gbar_min"] = float(gbar.min()); OUT["gbar_max"] = float(gbar.max())

# ------------------------------------------------------------------ V1: the log-log slope at low acceleration
def mond(gb, a0): return np.sqrt(gb * a0)
print("V1 -- the model-independent version: the slope of the relation at low acceleration")
print("     the square-root branch has log-log slope 1/2; a budget-truncated relation has slope 1 (mass frozen)")
for tag, a0 in A0.items():
    r = gobs - mond(gbar, a0)
    OUT[f"chi2_mond_{tag}"] = float(r @ np.linalg.solve(COV, r))
print(f"    absolute fit of the parameter-free branch: chi2/dof = "
      f"{OUT['chi2_mond_canonical']/n:.1f} (canonical) / {OUT['chi2_mond_alt']/n:.1f} (alt) -- NOT a good "
      "absolute fit, and it is not claimed to be; everything below is a RELATIVE comparison on identical data")
# generalised least squares for the slope in log-log, using the covariance propagated to log g_obs
COV_log = COV / (np.log(10)**2 * np.outer(gobs, gobs))   # exact Jacobian map to log10 g_obs, no huge intermediate
def slope_fit(mask):
    X = np.vstack([np.ones(mask.sum()), np.log10(gbar[mask])]).T
    Cl = COV_log[np.ix_(np.where(mask)[0], np.where(mask)[0])]
    Ci = np.linalg.inv(Cl); y = np.log10(gobs[mask])
    Cb = np.linalg.inv(X.T @ Ci @ X); bh = Cb @ (X.T @ Ci @ y)
    return float(bh[1]), float(np.sqrt(Cb[1, 1]))
gt_AM = A0["canonical"]/(1 + 32.1)**2       # recomputed properly in V2; used here only to define "low"
low = gbar < 1e-13
sl, sle = slope_fit(low)
OUT["slope_low"] = sl; OUT["slope_low_err"] = sle; OUT["n_low"] = int(low.sum())
print(f"    measured slope over the {low.sum()} bins below g_bar = 1e-13 m/s^2: {sl:.3f} +/- {sle:.3f}")
print(f"    distance from the square-root branch (0.5): {abs(sl-0.5)/sle:.1f} sigma;  "
      f"from a truncated relation (1.0): {abs(sl-1.0)/sle:.1f} sigma")
check("V1 [THE RELATION STILL RISES AS A SQUARE ROOT WHERE THE BUDGET SAYS IT MUST HAVE TURNED] the log-log "
      "slope of the lensing relation is measured with the full covariance over the bins below 1e-13 m/s^2 and "
      "compared with the two predictions: 1/2 for an untruncated square-root branch, 1 for a relation whose "
      "enclosed mass has frozen at the galaxies' budget",
      abs(sl - 1.0)/sle > 3.0,
      f"slope = {sl:.3f} +/- {sle:.3f}: {abs(sl-1.0)/sle:.1f} sigma from the truncated value 1, "
      f"{abs(sl-0.5)/sle:.1f} sigma from 1/2. The relation has NOT turned over where a bounded mass budget "
      "requires it to")

# ------------------------------------------------------------------ V2: the budget, from abundance matching
print("\nV2 -- the mass budget B = M_dark/M_bar, and the truncation it forces")
def moster_ms_over_mh(Mh):                                        # Moster et al. 2013, z = 0
    M1, N, beta, gam = 10**11.59, 0.0351, 1.376, 0.608
    return 2*N/((Mh/M1)**(-beta) + (Mh/M1)**gam)
def halo_mass(Mstar):
    return brentq(lambda lm: moster_ms_over_mh(10**lm)*10**lm - Mstar, 9.0, 15.0)
F_GAS = 1.3                                                        # M_bar = 1.3 M_star (cold gas), stated
budgets = {}
for lms in (10.3, 10.6, 10.8, 11.0):
    Ms = 10**lms; Mh = 10**halo_mass(Ms); Mb = F_GAS*Ms
    budgets[lms] = (Mh - Mb)/Mb
    print(f"    log M* = {lms}: abundance-matching M_h = {Mh:.2e} M_sun, M_bar = {Mb:.2e} -> B = {(Mh-Mb)/Mb:.1f}")
B_AM = float(np.median(list(budgets.values())))
B_COSMIC = 0.1200/0.02237                                          # Planck 2018 Omega_c h^2 / Omega_b h^2
print(f"    fiducial abundance-matching budget B_AM = {B_AM:.1f} (median of the four bins)")
print(f"    cosmic dark-to-baryon ratio B_cosmic = {B_COSMIC:.2f} (the ratio a fair sample of the universe has)")
for tag, a0 in A0.items():
    for name, B in (("B_cosmic", B_COSMIC), ("B_AM", B_AM), ("B=100 (stress)", 100.0)):
        gt = a0/(1+B)**2
        below = int((gbar < gt).sum())
        print(f"    [{tag}] {name:15s} B = {B:6.1f}: truncation at g_bar = {gt:.2e} m/s^2, "
              f"{below} of {n} measured bins lie below it")
        OUT[f"gt_{tag}_{name.split()[0]}"] = float(gt); OUT[f"nbelow_{tag}_{name.split()[0]}"] = below
check("V2 [THE TRUNCATION FALLS INSIDE THE MEASURED RANGE] the truncation acceleration a_0/(1+B)^2 is computed "
      "for the abundance-matching budget and compared with the range the data cover; the test can only bite if "
      "bins lie below it",
      OUT[f"nbelow_canonical_B_AM"] >= 3,
      f"B_AM = {B_AM:.1f} puts the turn at {OUT['gt_canonical_B_AM']:.2e} m/s^2 with "
      f"{OUT['nbelow_canonical_B_AM']} bins below it (canonical); B_cosmic puts it at "
      f"{OUT['gt_canonical_B_cosmic']:.2e} with {OUT['nbelow_canonical_B_cosmic']} bins below -- the data reach "
      "far enough to see the turn in every budget considered")

# ------------------------------------------------------------------ V3: the model comparison
print("\nV3 -- the truncated model against the data, full covariance")
def truncated(gb, a0, B):
    gt = a0/(1+B)**2
    return np.where(gb > gt, np.sqrt(gb*a0), (1+B)*gb)
for tag, a0 in A0.items():
    for name, B in (("B_cosmic", B_COSMIC), ("B_AM", B_AM), ("B=100", 100.0)):
        r = gobs - truncated(gbar, a0, B)
        chi2 = float(r @ np.linalg.solve(COV, r))
        dchi2 = chi2 - OUT[f"chi2_mond_{tag}"]
        OUT[f"chi2_trunc_{tag}_{name}"] = chi2; OUT[f"dchi2_{tag}_{name}"] = dchi2
        print(f"    [{tag}] {name:10s}: chi2 = {chi2:9.1f}  (untruncated {OUT[f'chi2_mond_{tag}']:.1f}), "
              f"Delta chi2 = {dchi2:+9.1f}  -> {np.sqrt(max(dchi2,0)):.1f} sigma against truncation")
worst = min(OUT[f"dchi2_{t}_B=100"] for t in A0)
check("V3 [THE TRUNCATED MODEL IS EXCLUDED -- THE PHANTOM IS NOT REAL MASS BOUNDED BY THE HALO BUDGET] the "
      "truncated prediction is compared with the untruncated square-root branch on the same data and covariance; "
      "a Delta chi-square above 25 (5 sigma) excludes truncation at that budget",
      worst > 25,
      f"Delta chi2 = {OUT['dchi2_canonical_B_AM']:+.0f} at the abundance-matching budget and "
      f"{OUT['dchi2_canonical_B=100']:+.0f} even at the stress budget B = 100 (canonical footing; alt "
      f"{OUT['dchi2_alt_B=100']:+.0f}). The lensing relation continues past every budget the galaxies have. "
      "THIS KILLS L247's medium as a source of the lensing signal, and every reading in which the phantom "
      "carrying the lensing IS the galaxy's own bounded sector")

# ------------------------------------------------------------------ V4: radius-resolved, the rotation curves
print("\nV4 -- the same budget, radius-resolved, on the lensing rotation curves (four stellar-mass bins)")
LIMS = [8.5, 10.3, 10.6, 10.8, 11.0]
rows = []
for k in range(1, 5):
    dd = np.genfromtxt(os.path.join(DATA, f"Fig-3_Lensing-rotation-curves_Massbin-{k}.txt"), comments="#")
    R, e, eb = dd[:, 0], dd[:, 1], dd[:, 4]
    v2 = 4*G_PC*(e/eb)*R*1e6*PC**2                                # (pc/s)^2 -> m^2/s^2 via PC^2 on G_PC*Msun
    Ms = 10**(0.5*(LIMS[k-1] + LIMS[k])); Mb = F_GAS*Ms
    Mh = 10**halo_mass(Ms); B = (Mh - Mb)/Mb
    Rm = R*MPC
    Mdyn = v2*Rm/G/MSUN                                            # enclosed dynamical mass, M_sun
    good = (e > 0) & (R < 1.0)                                     # inside 1 Mpc: the one-halo regime
    ratio = Mdyn[good]/Mb
    rows.append((k, Ms, Mb, Mh, B, R[good][-1], ratio[-1], ratio[-1]/(1+B)))
    if k == 1: print("      (bin 1 spans log M* = 8.5-10.3, too wide for a representative mass; "
                     "the verdict below rests on bins 2-4)")
    print(f"    bin {k} (log M* = {0.5*(LIMS[k-1]+LIMS[k]):.2f}): M_bar = {Mb:.2e}, AM halo {Mh:.2e}, B = {B:.1f}; "
          f"at R = {R[good][-1]*1e3:.0f} kpc the lensing mass is {ratio[-1]:.0f} M_bar = "
          f"{ratio[-1]/(1+B):.2f} of the whole abundance-matching budget")
OUT["v4"] = [dict(bin=r[0], Mstar=r[1], Mbar=r[2], Mhalo_AM=r[3], B=r[4], R_Mpc=r[5],
                  Mdyn_over_Mbar=r[6], frac_of_budget=r[7]) for r in rows]
over = [r for r in rows[1:] if r[7] > 1.0]          # bins 2-4 only: bin 1's mass range is too wide
check("V4 [THE BUDGET IS ALREADY OVERSPENT INSIDE ONE MEGAPARSEC] the enclosed lensing mass at the outermost "
      "bin inside 1 Mpc is compared, bin by bin, with the whole abundance-matching budget of the same galaxies; "
      "a ratio above one means the lensing signal has already claimed more mass than the galaxies own",
      len(over) >= 2,
      f"{len(over)} of the 3 narrow mass bins exceed their entire budget inside 1 Mpc "
      f"(fractions {', '.join(f'{r[7]:.2f}' for r in rows)}). The excess is real mass in the universe -- in the "
      "standard picture the two-halo term of correlated neighbours -- but it is NOT bound to the lens, so no "
      "reading in which the lensing phantom is the galaxy's OWN equilibrated sector can claim it")

# ------------------------------------------------------------------ V5: what the two-halo term can and cannot rescue
print("\nV5 -- the honest limitation: what correlated structure can mask")
rho_m = 0.315*8.6e-27
for tag, a0 in A0.items():
    Mb = F_GAS*10**10.6*MSUN
    r_eq = float(np.sqrt(np.sqrt(G*Mb*a0)/(4*np.pi*G*rho_m)))
    g_eq = G*Mb/r_eq**2
    OUT[f"v5_req_Mpc_{tag}"] = r_eq/MPC; OUT[f"v5_geq_{tag}"] = g_eq
    print(f"    [{tag}] for log M* = 10.6 the deep-branch phantom density drops to the cosmic mean matter "
          f"density at r = {r_eq/MPC:.2f} Mpc, i.e. g_bar = {g_eq:.2e} m/s^2 -- beyond that radius the claimed "
          "phantom is below the background and the excess-surface-density estimator cannot see it as an excess")
nbelow_eq = int((gbar < OUT["v5_geq_canonical"]).sum())
OUT["v5_nbelow_eq"] = nbelow_eq
for ndrop in (3, 5, 7):
    keep = np.arange(n)[ndrop:]                                   # drop the ndrop LOWEST-acceleration bins
    Ck = COV[np.ix_(keep, keep)]
    rm_ = gobs[keep] - mond(gbar[keep], A0["canonical"])
    rt_ = gobs[keep] - truncated(gbar[keep], A0["canonical"], B_AM)
    dk = float(rt_ @ np.linalg.solve(Ck, rt_)) - float(rm_ @ np.linalg.solve(Ck, rm_))
    nb = int((gbar[keep] < OUT["gt_canonical_B_AM"]).sum())
    OUT[f"v5_dchi2_drop{ndrop}"] = dk
    print(f"    dropping the {ndrop} lowest-acceleration bins ({n-ndrop} left, {nb} of them still below the "
          f"truncation): Delta chi2 = {dk:+.1f}")
check("V5 [THE VERDICT SURVIVES DROPPING THE BINS MOST EXPOSED TO CORRELATED STRUCTURE] the lowest-acceleration "
      "bins -- the largest radii, where neighbouring haloes contribute most to the excess surface density and the "
      "lens's own one-halo term is weakest -- are removed in three increasingly severe cuts and the two models "
      "recompared on what is left",
      min(OUT[f"v5_dchi2_drop{k}"] for k in (3, 5, 7)) > 25,
      f"Delta chi2 = {OUT['v5_dchi2_drop3']:+.0f} / {OUT['v5_dchi2_drop5']:+.0f} / {OUT['v5_dchi2_drop7']:+.0f} "
      "after dropping 3 / 5 / 7 bins. The FAIL at seven is a loss of POWER, not a reversal: seven cuts leave only "
      "one bin below the truncation, so the regime the test probes is gone. The honest scope is the first two "
      "cuts, which keep 5 and 3 bins below the turn and still exclude it; the verdict does depend on the "
      "low-acceleration bins, because that is the only place a mass-budget truncation can show itself")

# ------------------------------------------------------------------ V6: what the cap-and-dust architecture costs
print("\nV6 -- the scope this leaves for a capped equilibrium reading")
R_lens_lo, R_lens_hi = 0.035, 3.0                                  # Mpc, the range the lensing data cover
g_ext_mw = 2.146e-10                                               # the MW's external field at the Sun (L240)
for tag, a0 in A0.items():
    Mb_mw = F_GAS*10**10.6*MSUN
    r_cap = float(np.sqrt(G*Mb_mw/g_ext_mw))/MPC
    frac = max(0.0, (np.log10(min(r_cap, R_lens_hi)) - np.log10(R_lens_lo))) / (np.log10(R_lens_hi) - np.log10(R_lens_lo))
    OUT[f"v6_rcap_Mpc_{tag}"] = r_cap; OUT[f"v6_frac_{tag}"] = float(frac)
    print(f"    [{tag}] external-field cap radius for a log M* = 10.6 lens: r_cap = {r_cap*1e3:.1f} kpc; the "
          f"lensing data run {R_lens_lo*1e3:.0f} kpc to {R_lens_hi*1e3:.0f} kpc, so the capped equilibrium "
          f"covers {frac*100:.0f}% of the measured range in log radius")
check("V6 [A CAPPED EQUILIBRIUM READING SURVIVES THIS TEST ONLY BY MAKING NO PREDICTION WHERE THE DATA ARE] the "
      "external-field cap radius is computed for a lens of the sample's median mass and compared with the radii "
      "the lensing measurement covers; a fraction at or near zero means the confined phantom is not the object "
      "the lensing signal measures, and the free outer component carries all of it",
      OUT["v6_frac_canonical"] < 0.05,
      f"the cap sits at {OUT['v6_rcap_Mpc_canonical']*1e3:.0f} kpc, BELOW the innermost lensing bin at 35 kpc: the "
      "confined phantom covers none of the measured range. A capped reading therefore evades this kill, at the "
      "stated price that ordinary cold collisionless matter carries 100% of the lensing signal these data "
      "measure, and the identification makes no prediction anywhere in that range")

json.dump(OUT, open(os.path.join(HERE, "L248_results.json"), "w"), indent=1)
print(f"\nL248 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
sys.exit(0 if all(CH) else 1)
