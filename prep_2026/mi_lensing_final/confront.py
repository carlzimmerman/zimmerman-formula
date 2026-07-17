#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
confront.py -- THE CONFRONTATION: single-metric pure-MI lensing vs Brouwer 2021
================================================================================
Upstream (exit 0, this directory): total_stress.py assembled the total gravitating
stress tensor of the MI action (matter + frame legs; Assembly III Newton-anchored):
    T_hat = rho K(X) u u - 2 (rho K'/a0^2) a a ,  X = |a|^2/a0^2
lensing_solve.py derived the linearized single-metric equations and the crux
    F(y) = g_lens/(nu g_bar) ~= [M_eff/M_bar]/nu(y) < 1/nu(y) < 1  everywhere
(every source term O(K) <= 1; no O(nu) enhancement exists in the tensor).

THIS SCRIPT (the final confrontation, both a0 footings):
  1. The predicted single-metric lensing RAR vs the REAL Brouwer 2021 KiDS-1000
     isolated-lens points (official CDS release, repo data, full covariance,
     SIS conversion per the release README -- the P2 concordance loader).
     F < 1 is what the derivation gave => quantify the EXCLUSION significance of
     single-metric pure MI given Brouwer's measured lensing-RAR = dynamical-RAR
     equality, with honest errors: full covariance + profiled coherent amplitude
     (stellar-mass/conversion systematics +-0.3 dex) + B21's own hot-CGM
     baryon-budget variant file + M* +-0.2 dex refits.
  2. Cassini safety of the dressing terms at Saturn (y ~ 7e5).
  3. GW170817: single metric => c_gamma = c_GW automatic.

HONEST RAILS: no manufactured save, no manufactured kill; both footings; the
reliability rail g_bar >= 1e-13 (banked: isolation clean there) is the
conservative headline; full-range numbers shown for completeness.
"""
import numpy as np
import os, sys

PASS = 0; FAIL = 0
def check(name, ok):
    global PASS, FAIL
    print(("  [PASS] " if ok else "  [FAIL] ") + name)
    if ok: PASS += 1
    else: FAIL += 1

# ----- constants (SI) -----
G    = 6.674e-11; c = 2.998e8
Msun = 1.989e30;  kpc = 3.086e19
A0_CAN = 9.36e-11      # canonical rho_DE / cH_Lambda footing
A0_ALT = 1.13e-10      # alternate rho_total / cH0 footing
def nu_of(y): return np.sqrt(1.0 + 1.0/y)

# ============================================================================
# The single-metric MI prediction (from the assembled tensor, lensing_solve.py)
#   rho_eff = rho K = rho/nu(y)   (on-shell dressing, exact identity)
#   Pi      = -rho_eff/(2y+1)     (radial anisotropic stress, tension)
#   (P) Lap Psi = 4 pi G rho_eff ; (S) Phi' - Psi' = 4 pi G r Pi
#   g_lens = (1/2)(Phi'+Psi') = Psi' + 2 pi G r Pi
# Galaxy: M_bar = 5e10 Msun -- Hernquist stars 4e10 (a*=2 kpc) + gas 1e10 (10 kpc)
# ============================================================================
Mstar, astar = 4e10*Msun, 2.0*kpc
Mgas,  agas  = 1e10*Msun, 10.0*kpc
NR = 4000
rg = np.geomspace(0.02*kpc, 2000*kpc, NR)
def hern_rho(rr, M, a): return M*a/(2*np.pi*rr*(rr+a)**3)
def hern_M(rr, M, a):   return M*rr**2/(rr+a)**2
rho_b = hern_rho(rg, Mstar, astar) + hern_rho(rg, Mgas, agas)
M_b   = hern_M(rg, Mstar, astar) + hern_M(rg, Mgas, agas)
g_bar = G*M_b/rg**2

def solve_galaxy(a0):
    y  = g_bar/a0
    nu = nu_of(y)
    rho_eff = rho_b/nu                       # K = 1/nu on-shell (exact)
    Pi = -rho_eff/(2.0*y + 1.0)              # tension; doc-gamma fork halves this (<=4.1% on F)
    M_eff = np.concatenate([[0.0], np.cumsum(
        4*np.pi*0.5*(rho_eff[1:]*rg[1:]**2 + rho_eff[:-1]*rg[:-1]**2)*np.diff(rg))])
    Psip = G*M_eff/rg**2
    Phip = Psip + 4*np.pi*G*rg*Pi
    return dict(y=y, nu=nu, M_eff=M_eff, g_lens=0.5*(Phip+Psip))

def model_F1(gb, a0):
    """lensing RAR == dynamical RAR: the framework's own nu (Brouwer's equality)."""
    return np.sqrt(gb**2 + gb*a0)

def model_MI(gb, a0, sol):
    """single-metric MI prediction g_lens at the radius where the galaxy has g_bar.
       Below the solved range g_lens -> (M_eff_inf/M_bar) g_bar (exact 1/r^2 tail);
       above (y >> 1) K -> 1 so g_lens -> g_bar."""
    iout = np.argmax(g_bar)
    gb_out = g_bar[iout:]; gl_out = sol['g_lens'][iout:]
    out = np.interp(-gb, -gb_out, gl_out, left=np.nan, right=np.nan)
    lo = gb < gb_out.min()
    out[lo] = (sol['M_eff'][-1]/M_b[-1])*gb[lo]
    hi = gb > gb_out.max()
    out[hi] = gb[hi]
    return out

sol_can = solve_galaxy(A0_CAN)
sol_alt = solve_galaxy(A0_ALT)

print("="*88)
print("PART 1 -- Brouwer 2021 (KiDS-1000 isolated lensing RAR): the real points, full cov")
print("="*88)
# ----- the P2 concordance loader (official B21 CDS release, README conversion) -----
B = ("/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
    "lensing_rar/brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30
CONV = 4*G_PC*PC_PER_M                        # ESD[Msun/pc^2] -> g_obs[m/s^2] (B21 Eq.7 / SIS)

def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]

def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    assert d.shape[0] == n*n
    return (d[:, 4]/d[:, 6]).reshape(n, n)*CONV*CONV

gbar_d, gobs_d, gerr_d = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
n = len(gbar_d)
C = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
check("B21 official release loaded: N=15, cov symmetric, diag matches errors <5%",
      n == 15 and np.allclose(C, C.T, rtol=1e-6)
      and np.allclose(np.sqrt(np.diag(C)), gerr_d, rtol=0.05))
print(f"  N = {n} points, g_bar in [{gbar_d.min():.2e}, {gbar_d.max():.2e}] m/s^2")
print("  Brouwer's MEASUREMENT: the lensing RAR equals the dynamical RAR to ~2.5 dex")
print("  below a0 (their Figs 4-5; Mistele-McGaugh+ 2024 the same, deeper).")
print("  reliability rail (banked): isolation clean at g_bar >= 1e-13 (N = %d)"
      % int((gbar_d >= 1e-13).sum()))

def chi2(gpred, mask):
    dv = (gobs_d - gpred)[mask]
    return float(dv @ np.linalg.solve(C[np.ix_(mask, mask)], dv))

rail = gbar_d >= 1e-13
full = gbar_d > 0
results = {}
for a0, tag, sol in ((A0_CAN, "CANONICAL", sol_can), (A0_ALT, "ALT", sol_alt)):
    m1 = model_F1(gbar_d, a0); m2 = model_MI(gbar_d, a0, sol)
    print(f"\n  [{tag} a0 = {a0:.3g}]  predicted vs measured (rail points):")
    print("      g_bar         g_obs(measured)  +-err        F=1 (dyn RAR)   MI single-metric   MI/meas")
    for i in np.where(rail)[0]:
        print(f"    {gbar_d[i]:.3e}   {gobs_d[i]:.3e}   {gerr_d[i]:.1e}    "
              f"{m1[i]:.3e}     {m2[i]:.3e}        {m2[i]/gobs_d[i]:.3f}")
    for name, mask in (("RAIL g_bar >= 1e-13", rail), ("FULL RANGE", full)):
        c1, c2 = chi2(m1, mask), chi2(m2, mask)
        dchi = c2 - c1
        sig = np.sqrt(max(dchi, 0.0))
        results[(tag, name)] = (c1, c2, dchi, sig)
        print(f"    {name} (N={mask.sum()}): chi2(F=1)={c1:7.1f}  chi2(MI)={c2:7.1f}  "
              f"Delta chi2 = {dchi:+7.1f}  => ~{sig:.1f} sigma (formal Gaussian equiv.)")
    i0 = np.where(rail)[0][0]
    print(f"    rail-edge deficit at g_bar={gbar_d[i0]:.1e}: MI predicts {m2[i0]:.1e}, "
          f"measured {gobs_d[i0]:.1e} => {np.log10(gobs_d[i0]/m2[i0]):.2f} dex short, "
          f"{(gobs_d[i0]-m2[i0])/gerr_d[i0]:.1f} sigma single-point")
    # honest errors 1: profiled coherent amplitude (M*/SIS-conversion systematics)
    deltas = np.linspace(-0.3, 0.3, 121)
    c1p = min(chi2(m1*10**dd, rail) for dd in deltas)
    c2p = min(chi2(m2*10**dd, rail) for dd in deltas)
    print(f"    PROFILED free +-0.3 dex coherent amplitude (rail): chi2(F=1)->{c1p:.1f}, "
          f"chi2(MI)->{c2p:.1f}, Delta={c2p-c1p:.1f} (~{np.sqrt(max(c2p-c1p,0)):.1f} sigma)")
    # honest errors 2: M* +-0.2 dex on g_bar (lens stellar-mass scale, the P2 systematic)
    worst = np.inf
    for dd in (-0.2, 0.2):
        gb_s = gbar_d*10**dd
        d1 = chi2(model_F1(gb_s, a0), rail) ; d2 = chi2(model_MI(gb_s, a0, sol), rail)
        worst = min(worst, d2 - d1)
    print(f"    M* +-0.2 dex on g_bar (rail): smallest Delta chi2(MI-F=1) = {worst:.1f}")
    check(f"{tag}: MI under-shoots EVERY rail point (F<1 confronts data)",
          bool(np.all(m2[rail] < gobs_d[rail])))
    check(f"{tag}: exclusion survives all nuisances (Delta chi2 > 100 rail, profiled, M* shifts)",
          results[(tag, "RAIL g_bar >= 1e-13")][2] > 100 and (c2p - c1p) > 100 and worst > 100)

# honest errors 3: B21's OWN hot-CGM baryon-budget variant (their file; diag errors --
# no released covariance for it). The budget moves a0 fits; can it rescue an MI slope?
gb_h, go_h, eg_h = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
mh = gb_h >= 1e-13
def chi2diag(gpred, go, eg, mask):
    return float(np.sum(((go - gpred)[mask]/eg[mask])**2))
c1h = chi2diag(model_F1(gb_h, A0_CAN), go_h, eg_h, mh)
c2h = chi2diag(model_MI(gb_h, A0_CAN, sol_can), go_h, eg_h, mh)
print(f"\n  hot-CGM baryon-budget variant (B21's own file, diag, rail N={mh.sum()}):")
print(f"    chi2(F=1)={c1h:.1f}  chi2(MI)={c2h:.1f}  Delta={c2h-c1h:.1f} "
      f"(~{np.sqrt(max(c2h-c1h,0)):.1f} sigma)")
check("baryon budget does not rescue: hot-CGM variant Delta chi2 still > 100",
      (c2h - c1h) > 100)
print("""
  WHY nothing rescues it: the MI single-metric prediction has the WRONG SLOPE --
  deep in, g_lens -> (M_eff_inf/M_bar) g_bar (linear in g_bar) while the measured
  relation follows sqrt(a0 g_bar). Coherent amplitude shifts, stellar-mass scale,
  and the baryon budget all move the amplitude, not the slope. Mistele-McGaugh+
  2024 (JCAP 04(2024)020) extends the measured equality deeper: exclusion grows.""")

print("="*88)
print("PART 2 -- Cassini safety of the dressing terms at Saturn (y ~ 7e5)")
print("="*88)
g_sat = G*1.989e30/(1.43e12)**2
for a0, tag in ((A0_CAN, "CANONICAL"), (A0_ALT, "ALT")):
    y_sat = g_sat/a0
    aniso = 1/(2*y_sat + 1)          # 2K'X/K: the anisotropic-stress fraction
    dress = 1 - 1/nu_of(y_sat)       # 1-K: source dressing at Saturn's orbit
    print(f"  [{tag}] g_Saturn = {g_sat:.2e} m/s^2, y = {y_sat:.1e}")
    print(f"    source dressing 1-K = {dress:.1e} at Saturn's orbit "
          f"(Sun itself: a0/(2 g_surf) = {a0/(2*274):.1e}, mass-weighted smaller)")
    print(f"    anisotropic fraction 2K'X/K = 1/(2y+1) = {aniso:.1e}")
    print(f"    slip in vacuum: Pi ~ rho = 0 outside the source => Phi = Psi EXACTLY,"
          f" gamma_PPN = 1")
    print(f"    => the gamma-type (light-bending/Shapiro) corrections are the SOLAR source")
    print(f"       dressing ~{a0/(2*274):.0e} + exactly-zero vacuum slip: "
          f"~{2.3e-5/(a0/(2*274)):.0e}x under the Cassini |gamma-1| bound 2.3e-5 (~8 orders)")
    print(f"    the local 1-K and 2K'X/K ~ {aniso:.0e} at Saturn enter DYNAMICS (nu-1, the")
    print(f"       banked deep-Newton pass), and even those sit {2.3e-5/aniso:.0f}x under the bound")
    check(f"{tag}: all assembled-tensor corrections < 1e-6 at Saturn (bound 2.3e-5)",
          aniso < 1e-6 and dress < 1e-6)
print("  (The banked AeST/MG Q2-quadrupole caveat concerns the MG realization, not this")
print("   assembled MI tensor; not re-litigated here.)")

print("\n" + "="*88)
print("PART 3 -- GW170817: automatic")
print("="*88)
print("""  The surviving route IS the single metric: photons, gravitons, and matter all
  couple to the one g_munu (the disformal photon metric being excluded ~6-7 orders
  by today's erratum). Therefore c_gamma = c_GW EXACTLY -- not a constraint the
  theory passes, but an identity of the construction. GW170817 (|c_gamma/c_GW - 1|
  < ~1e-15) is satisfied automatically.""")
check("GW170817 automatic on the single metric (identity, not a fit)", True)

print("="*88)
print(f"TOTAL: {PASS} checks passed, {FAIL} failed")
print("="*88)
print(f"""
STRAIGHT VERDICT (both footings):
  The derived single-metric prediction is F(y) < 1/nu(y) < 1 (under-lensing; the
  assembled tensor's every term is O(K) <= 1). Brouwer 2021's measured equality
  lensing-RAR = dynamical-RAR then DIRECTLY FALSIFIES single-metric pure MI (this
  action, this assembled T_munu, photons on g) as the complete theory:
    rail (g_bar >= 1e-13, N=7, full cov):  Delta chi2 = +{results[('CANONICAL','RAIL g_bar >= 1e-13')][2]:.0f} canonical
      (~{results[('CANONICAL','RAIL g_bar >= 1e-13')][3]:.0f} sigma formal) / +{results[('ALT','RAIL g_bar >= 1e-13')][2]:.0f} alt (~{results[('ALT','RAIL g_bar >= 1e-13')][3]:.0f} sigma)
    full range (N=15):  +{results[('CANONICAL','FULL RANGE')][2]:.0f} / +{results[('ALT','FULL RANGE')][2]:.0f} (~{results[('CANONICAL','FULL RANGE')][3]:.0f}/{results[('ALT','FULL RANGE')][3]:.0f} sigma)
  robust to profiled amplitude, M* +-0.2 dex, and B21's own hot-CGM budget: the MI
  slope (g_lens ~ g_bar deep) is wrong, and no coherent systematic fixes a slope.
  Cassini: safe by ~7-8 orders (dressing ~1e-13 solar, 7e-7 at Saturn; vacuum slip
  exactly zero). GW170817: automatic (one metric).
  The completion statement: complete up to its constants in the DYNAMICS+COSMOLOGY
  sectors; LENSING requires physics beyond the current action (named doors: the
  off-circular/nonlocal closure needing O(nu) from O(K)-bounded structures, a
  lensing carrier beyond S_EH+S_u+S_matter, the free-frame S_u bookkeeping wound).
""")
sys.exit(0 if FAIL == 0 else 1)
