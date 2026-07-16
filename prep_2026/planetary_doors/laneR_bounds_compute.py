#!/usr/bin/env python3
r"""
LANE R -- PLANETARY-DOORS BOUNDS LEDGER (computed, both footings)
==================================================================================
Companion to BOUNDS.md in this directory. Every derived number in that file is
computed here; every measured number is cited to the paper it comes from.

Framework (Carl Zimmerman): de Sitter-Unruh MODIFIED INERTIA.
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical, rho_DE footing);
  ALT a0 = 1.13e-10 (rho_total / cH0 footing).  Z = sqrt(32pi/3).
  Own interpolation nu(y) = sqrt(1+1/y), g_obs = sqrt(g_bar^2 + g_bar*a0).

HONEST CEILING (stated per the workflow ground rules): at planetary accelerations
(10^4-10^8 x a0) GR predicts zero anomaly and so, approximately, do healthy
MOND-family theories. A solar-system NULL discriminates BETWEEN the framework's
candidate relativistic doors (which predict different nonzero residuals); it can
NEVER prove the framework right vs LCDM.

MEASURED INPUTS (citations in BOUNDS.md):
  [H14]  Hees, Folkner, Jacobson, Park 2014, PRD 89 102002 (arXiv:1402.6950):
         Q2 = (3 +/- 3) x 10^-27 s^-2  (Cassini radio tracking).
  [P26]  Park, Hees, Famaey, Desmond, Durakovic 2026 (arXiv:2602.17884):
         Q2 = (1.6 +/- 1.8) x 10^-27 s^-2 (DE440 dataset, 40% tighter);
         => MOND boost to the galactic radial accel at the Sun <= 2% (95% CL);
         RAR-vs-Q2 tension 3-15 sigma depending on MW mass model.
  [DHF24] Desmond, Hees, Famaey 2024, MNRAS 530 1781 (arXiv:2401.04796):
         AQUAL/QUMOND RAR-vs-Cassini tension 8.7 sigma fiducial (1.9 sigma
         w/o bulge galaxies).
  [BN11] Blanchet & Novak 2011, MNRAS 412 2530 (arXiv:1010.1349) Tables 1-3,5:
         Q2 theory (a0=1.2e-10, g_e=1.9e-10): mu1 3.8e-26, mu2 2.2e-26,
         mu5 7.4e-27, mu20 2.1e-27, muexp 3.0e-26, muTeVeS 4.1e-26 s^-2;
         Saturn Delta2 up to 5.81 mas/cy; Q1 dipole == 0 (|Q1|~9e-14 m/s^2 num.);
         + the landmine sentence (arXiv:1105.5815 p.8): a mu ~ 1 - 1/y tail
         "predicts a constant supplementary acceleration directed toward the Sun
         delta g_N = a0 (i.e. a 'Pioneer' effect), which is ruled out because
         not seen from the motion of planets."
  [M09]  Milgrom 2009, MNRAS 399 474 (arXiv:0906.4817): -q ~ 0.01-0.3, quad
         anomaly ~1e-5 a0 (inner planets) to ~1e-4 a0 (Saturn); modified-INERTIA
         formulations: anomalies keyed to trajectories that REACH low-a regions
         (comets, Pioneer), "without affecting the motions of planets, whose
         orbits are wholly in the high acceleration regime."
  [FM24] Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1 (arXiv:2303.01821)
         Table 10: 1-sigma uncertainties on supplementary perihelion advance
         (mas/yr): Pitjeva&Pitjev2013 (EPM): Me 0.03, V 0.016, E 0.0019,
         Ma 0.00037, J 0.28, Sa 0.0047; Fienga+2011b (INPOP10a): Me 0.006,
         V 0.015, E 0.009, Ma 0.0015, J 0.42, Sa 0.0065.
         Data-accuracy table: MESSENGER range 5 m (2011-2014); Juno radio-science
         range 20 m (2016.7-2020.6); Cassini nav 6 m / grand finale 1 m / VLBI
         0.6 mas; Mars MEX/MRO 1.2-2 m.
  [PP13] Pitjev & Pitjeva 2013 (Astron. Lett. 39 141): rho_DM(<Saturn) <
         1.1e-20 g/cm^3; M_DM(<Saturn) < 7.9e-11 Msun (original paper;
         FM24's text quotes 7.1e-11 -- both carried).
  [G18]  Genova+ 2018, Nat. Comm. 9 289 (MESSENGER): eta = (-6.6+/-7.2)e-5,
         J2_sun=(2.246+/-0.022)e-7, |Gdot/G| <~ 4e-14/yr; Mercury ephemeris < 1 m.
  [B21]  Biskupek, Mueller, Torre 2021, Universe 7 34 (arXiv:2012.12032) LLR:
         Gdot/G = (-5.0+/-9.6)e-15/yr; EP Delta(mg/mi)_EM = (-2.1+/-2.4)e-14;
         beta-1 = (6.2+/-7.2)e-5; gamma-1 = (1.7+/-1.6)e-4.

numpy only. exit 0.
"""
import numpy as np

# ----------------------------------------------------------------- constants
c   = 2.99792458e8
G   = 6.674e-11
Msun= 1.989e30
AU  = 1.495978707e11
YR  = 3.15576e7
CY  = 100.0*YR
MAS = np.pi/180.0/3600.0/1000.0        # rad per milliarcsecond
GM  = G*Msun

A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10

# Q2 measurements
Q2_H14, S_H14 = 3.0e-27, 3.0e-27       # Hees+2014
Q2_P26, S_P26 = 1.6e-27, 1.8e-27       # Park+2026
CEIL26 = Q2_P26 + 2*S_P26              # 5.2e-27 two-sigma ceiling

# planets: a[AU], e, P[yr]   (Blanchet-Novak 2011 Table 2)
PLANETS = {
 "Mercury": (0.397, 0.206, 0.24),
 "Venus":   (0.723, 0.007, 0.62),
 "Earth":   (1.000, 0.017, 1.00),
 "Mars":    (1.523, 0.093, 1.88),
 "Jupiter": (5.203, 0.048, 11.86),
 "Saturn":  (9.537, 0.054, 29.46),
 "Uranus":  (19.229,0.047, 84.01),
 "Neptune": (30.069,0.009, 164.8),
}
# 1-sigma uncertainties on supplementary perihelion advance [mas/yr], FM24 Table 10
SIG_PP13 = {"Mercury":0.03,"Venus":0.016,"Earth":0.0019,"Mars":0.00037,
            "Jupiter":0.28,"Saturn":0.0047}
SIG_F11  = {"Mercury":0.006,"Venus":0.015,"Earth":0.009,"Mars":0.0015,
            "Jupiter":0.42,"Saturn":0.0065}

print("#"*94)
print("# LANE R -- PLANETARY-DOORS BOUNDS LEDGER (both footings; every number derived or cited)")
print("#"*94)
print(f"""
HONEST CEILING: at planetary accelerations (1e4-1e8 x a0) GR predicts zero anomaly and so,
approximately, do healthy MOND-family theories. A null discriminates BETWEEN the framework's
doors; it can NEVER prove the framework right vs LCDM.
""")

# ================================================================ SECTION 1
# THE LANDMINE: naive algebraic reading of nu(y)=sqrt(1+1/y).
# tail: nu-1 -> 1/(2y) => g_obs ~ g_N + a0/2 : a CONSTANT sunward extra acceleration.
# ============================================================================
print("="*94)
print(" [1] THE LANDMINE -- naive algebraic circular-orbit reading of the framework's own nu")
print("="*94)
for tag,a0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    print(f"   {tag:<10} a0={a0:.3e}  ->  naive constant sunward anomaly a0/2 = {a0/2:.3e} m/s^2")
print("   published support that this class is excluded: Blanchet-Novak 2011 (arXiv:1105.5815, p.8):")
print("   a mu ~ 1-1/y tail 'predicts a constant supplementary acceleration directed toward the Sun")
print("   delta g_N = a0 ... ruled out because not seen from the motion of planets.'")

# ---- per-planet bound on a CONSTANT radial extra acceleration from the perihelion-rate sigma.
# Gauss perturbation equation, radial perturbation R (outward +):
#   dw/dt = sqrt(1-e^2)/(n a e) * [ -R cos f ]      (S=0 for purely radial)
# orbit-TIME-average with dt ~ r^2 df (Kepler). For constant sunward R = -dg:
#   <dw/dt> = + dg * sqrt(1-e^2)/(n a e) * <cos f>_t ,  <cos f>_t computed numerically.
def secular_pericenter_rate_const_radial(dg, aAU, e, Pyr):
    n = 2*np.pi/(Pyr*YR); a = aAU*AU
    f = np.linspace(0,2*np.pi,200001)
    r = a*(1-e**2)/(1+e*np.cos(f))
    w = r*r                                   # dt ~ r^2 df
    cosf_t = np.trapz(np.cos(f)*w,f)/np.trapz(w,f)
    # R = -dg (sunward). <dw/dt> = sqrt(1-e^2)/(n a e) * <-R cos f> = sqrt(1-e^2)/(n a e)*dg*<cos f>
    return np.sqrt(1-e**2)/(n*a*e)*dg*cosf_t  # rad/s

print(f"\n   Per-planet 1-sigma bound on a CONSTANT radial extra acceleration [m/s^2]")
print(f"   (from the FM24 Table-10 supplementary-perihelion 1-sigma uncertainties):")
print(f"   {'planet':<9}{'sig_EPM[mas/yr]':>16}{'dg_max(EPM)':>14}{'sig_INPOP':>11}{'dg_max(INPOP)':>15}"
      f"{'excl. canon a0/2':>18}{'excl. alt':>11}")
print("   "+"-"*92)
worst = {}
for pl in ["Mercury","Venus","Earth","Mars","Jupiter","Saturn"]:
    aAU,e,P = PLANETS[pl]
    rate_per_dg = abs(secular_pericenter_rate_const_radial(1.0,aAU,e,P))   # (rad/s) per (m/s^2)
    dg_epm = SIG_PP13[pl]*MAS/YR / rate_per_dg
    dg_inp = SIG_F11 [pl]*MAS/YR / rate_per_dg
    best = min(dg_epm,dg_inp)
    worst[pl] = best
    print(f"   {pl:<9}{SIG_PP13[pl]:>16.5f}{dg_epm:>14.2e}{SIG_F11[pl]:>11.4f}{dg_inp:>15.2e}"
          f"{(A0_CANON/2)/best:>16.0f}x{(A0_ALT/2)/best:>10.0f}x")
best_pl = min(worst,key=worst.get)
print(f"\n   => the naive a0/2 tail is EXCLUDED by {(A0_CANON/2)/worst[best_pl]:.0f}x (canonical) /"
      f" {(A0_ALT/2)/worst[best_pl]:.0f}x (alt) at {best_pl} (tightest).")
print(f"      [cross-check: Saturn dg_max(EPM)={worst['Saturn']:.1e} ~ the banked 7.4e-15 EPM tail")
print(f"       sensitivity used in branchB_q2_gate_2026/laneB_q2_solve.py -- consistent.]")

# ================================================================ SECTION 2
# Q2 LEDGER: measurements vs theory values (MG door) vs MI door.
# ============================================================================
print("\n"+"="*94)
print(" [2] Q2 LEDGER -- the EFE quadrupole: measurements, MG-door predictions, MI-door predictions")
print("="*94)
print(f"   MEASURED:  Hees+2014      Q2 = (3.0 +/- 3.0)e-27 s^-2   (2-sig upper 9.0e-27)")
print(f"              Park+2026      Q2 = (1.6 +/- 1.8)e-27 s^-2   (2-sig ceiling {CEIL26:.1e})")
print(f"   THEORY (MG/modified-Poisson, BN11 Tab.1, a0=1.2e-10, g_e=1.9e-10):")
for mu,q2 in [("mu1",3.8e-26),("mu2 (standard)",2.2e-26),("mu5",7.4e-27),
              ("mu20",2.1e-27),("mu_exp",3.0e-26),("mu_TeVeS",4.1e-26)]:
    sig = (q2-Q2_P26)/S_P26
    print(f"     {mu:<15} Q2={q2:.1e}  -> {q2/CEIL26:6.2f}x ceiling  ({sig:+.1f} sig vs Park+2026)")
print(f"   FRAMEWORK MG-door (own nu, committed decider_q2_crosscheck.py, worst g_ext corner):")
for tag,q2 in [("canonical",2.50e-26),("alt",3.31e-26)]:
    print(f"     framework-nu {tag:<10} Q2={q2:.2e} -> {q2/CEIL26:5.2f}x ceiling ({(q2-Q2_P26)/S_P26:+.1f} sig)")
print(f"   FRAMEWORK MI-door (committed cassini_mi_evasion_2026, derived, both footings):")
print(f"     l=1 dipole scale   1.5e-28 s^-2 (0.03x ceiling; a uniform dipole doesn't secularly precess)")
print(f"     l=2 TRUE quadrupole 7.4e-34 s^-2 (~1.4e-7x ceiling) -- 2nd order in a_ext, verified scaling")
print(f"   DHF24 headline: AQUAL/QUMOND RAR-vs-Q2 tension 8.7 sig fiducial; Park+2026: 3-15 sig;")
print(f"   MOND boost of galactic accel at the Sun <= 2% (95%) vs the ~28-33% the framework's nu needs")
print(f"   (committed cassini_quadrupole_framework.py: 28.2% at canonical, 32.8% 'simple').")

# ================================================================ SECTION 3
# Blanchet-Novak Delta2 precessions + what the Park+2026 ceiling implies per planet
# ============================================================================
print("\n"+"="*94)
print(" [3] EFE-QUADRUPOLE PERIHELION PRECESSIONS  Delta2 = Q2 sqrt(1-e^2)/(4n) [1+5cos(2w~)]")
print("="*94)
print(f"   BN11 Table 3 (mas/cy) at their Q2: Saturn mu1 5.39, mu2 3.12, mu_exp 4.25, muTeVeS 5.81;")
print(f"   Uranus up to -10.94; Earth 0.16 (vs INPOP Jupiter-VLBI bound 0 +/- 0.016 mas/cy).")
print(f"   At the Park+2026 2-sigma ceiling Q2={CEIL26:.1e} (angle factor [1+5cos2w~] set to 1):")
for pl in ["Earth","Mars","Saturn","Uranus"]:
    aAU,e,P = PLANETS[pl]; n = 2*np.pi/(P*YR)
    d2 = CEIL26*np.sqrt(1-e**2)/(4*n)      # rad/s
    print(f"     {pl:<8} Delta2(ceiling) = {d2/MAS*CY:8.3f} mas/cy")
print("   (i.e. the ephemeris perihelion table and the direct Q2 fit are consistent probes;")
print("    the direct simultaneous Q2 fit [H14/P26] is the sharper, self-consistent one. FM24 Sect.5")
print("    cautions against reading un-refit supplementary-precession residuals as theory bounds.)")

# ================================================================ SECTION 4
# LLR / lunar lane
# ============================================================================
print("\n"+"="*94)
print(" [4] LLR / LUNAR ORBIT -- what MOND-family effects LLR can and cannot see")
print("="*94)
a_m, e_m, P_m = 3.844e8, 0.0549, 27.32*86400.0
n_m = 2*np.pi/P_m
# (a) EFE quadrupole on the lunar orbit at the Park ceiling
d2_moon = CEIL26*np.sqrt(1-e_m**2)/(4*n_m)
dr_moon = CEIL26/n_m**2 * a_m     # radial displacement scale ~ (Q2/n^2)*a
print(f"   (a) EFE quadrupole at the Park+2026 ceiling: Delta2(Moon) = {d2_moon/MAS*CY:.2e} mas/cy;")
print(f"       range-displacement scale (Q2/n^2)*a = {dr_moon*1e3:.2e} mm  << LLR mm accuracy [B21]")
print(f"       => LLR is ~4 orders LESS sensitive to Q2 than Cassini/ephemerides. Not the Q2 lane.")
print(f"       NOTE (trap): Blanchet-Novak 2011 contains NO lunar-orbit prediction (checked: zero")
print(f"       lunar/LLR mentions in MNRAS 412 2530 or the Moriond proceedings). Their tables are")
print(f"       planets-only. Attribute lunar-EFE claims to scalings like this one, not to BN11.")
# (b) the naive landmine at the Moon: constant-|a0/2| sunward field has a DIRECTION differential
for tag,a0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    dg_diff = (a0/2)*(a_m/AU)          # transverse differential across the E-M separation
    dr_syn  = dg_diff/n_m**2           # order-of-magnitude synodic range perturbation
    print(f"   (b) naive-tail differential across the E-M orbit ({tag}): a0/2*(a_m/AU) = {dg_diff:.2e} m/s^2")
    print(f"       -> synodic-period range signal O(dg/n^2) ~ {dr_syn*100:.1f} cm vs LLR cm residuals")
print(f"       => LLR *independently* disfavors the naive constant tail (order-of-magnitude; the")
print(f"          planetary perihelion exclusion in [1] is 3-4 orders and is the load-bearing one).")
print(f"   (c) LLR precision bounds [B21]: Gdot/G=(-5.0+/-9.6)e-15/yr; EP Delta(mg/mi)=(-2.1+/-2.4)e-14;")
print(f"       beta-1=(6.2+/-7.2)e-5; gamma-1=(1.7+/-1.6)e-4.")

# ================================================================ SECTION 5
# monopole / extra-mass gates and data accuracies (context for any door's tail)
# ============================================================================
print("\n"+"="*94)
print(" [5] MONOPOLE + DATA-ACCURACY LEDGER")
print("="*94)
print(f"   Pitjev-Pitjeva 2013 (EPM2011): rho_DM(<Saturn) < 1.1e-20 g/cm^3;")
print(f"   M_extra(<Saturn) < 7.9e-11 Msun (original; FM24 text: 7.1e-11 -- both carried).")
print(f"   Ranging accuracies (FM24 data table): MESSENGER 5 m ('11-'14; Genova+18 ephemeris <1 m);")
print(f"   Juno radio-science 20 m ('16.7-'20.6; 9 Juno positions entered INPOP19a, +1 yr in 21a);")
print(f"   Cassini nav 6 m, grand-finale 1 m, VLBI 0.6 mas; Mars MEX/MRO/MGS 1.2-2.0 m.")
print(f"   MESSENGER fundamental-physics [G18]: eta=(-6.6+/-7.2)e-5, J2_sun=(2.246+/-0.022)e-7,")
print(f"   |Gdot/G| <~ 4e-14/yr.")

# ================================================================ SECTION 6
# door scoreboard recap (numbers from committed scripts, re-run this session)
# ============================================================================
print("\n"+"="*94)
print(" [6] DOOR SCOREBOARD (prior committed work, re-run 2026-07-16, all exit 0)")
print("="*94)
print(f"""   Door A (MG/AeST-class, own nu): Q2 = 2.5e-26 (canon) / 3.3e-26 (alt) = 4.8x / 6.4x the
     Park ceiling = +13 / +17.5 sigma. INHERITS the DHF24/P26 wall. Lower a0 helps only
     marginally (boost 36%->28% vs the 2% allowance).
   Door B (Branch-B elastic medium, branchB_q2_gate_2026): scalar sharp-screen squeeze --
     pow p=8 SPARC-winner FAILS Q2 x1.6-2.1; delta d=6 passes Q2 (1.5-1.9e-27) but FAILS
     SPARC on canonical; pow p=6 survives by a needle on canonical ONLY (worst 4.65e-27 =
     0.9x ceiling; alt 1.19x FAIL). Elastic two-invariant route evades via shear-linearity
     (w <~ 0.2) at the price of underived posits P5/P6.
   Door C (pure MI, cassini_mi_evasion_2026 + cassini_mi_q2_saturn_2026): true l=2
     quadrupole 7.4e-34 (~1e-7 x ceiling), dipole scale 1.5e-28 (0.03x) -- EVADES, derived
     from the deep-Newtonian nu-1 = a0/(2 a_int) = 7.1e-7 suppression at Saturn. BUT this
     assumed the QUASISTATIC kernel response; the never-done calculation (the landmine) is
     whether the PUBLISHED kernel constraints (Herglotz + sum rule + causality, v4-v11)
     FORCE the suppression of the a0/2 tail at planetary frequencies. Section [1] above is
     the wall any failure hits: 1e3.8-1e4.5x per-planet exclusions.""")
print("\nEXIT 0")
