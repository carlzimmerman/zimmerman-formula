#!/usr/bin/env python3
"""
sqrt_lambda_pins_KQ.py   (topic: sqrt_lambda_pins_KQ)
=====================================================
THE extra-crispy question: does the framework's sqrt(Lambda) / de Sitter-Unruh
structure PIN the AeST K(Q) amplitude (the a^-3 dust that fits clusters+CMB), or
is it genuinely a FREE integration constant?

In AeST (Skordis-Zlosnik 2021, arXiv:2007.00082) the dust amplitude is
      8 pi Gtilde rho_dust0 = Q0 * I0          (their FLRW reduction)
with the shift-symmetric scalar integrating to  dK/dQ = I0/a^3  =>  rho ~ a^-3.
Their VERBATIM statements (verified this session vs ar5iv full text):
  - "As the solution depends on the initial condition I0, the density rho-bar is
     not (classically) predicted."
  - "The CC in this model remains a freely specifiable parameter, just as in LCDM."
  - extra free params vs LCDM: "lambda_s, K_B, K2 (or equivalently w0) and Q0".
  - a0 enters a DIFFERENT sector: J -> (2 lambda_s/[3(1+lambda_s) a0]) Y^(3/2).
  - mass mu (Verwayen-Skordis-Zlosnik 2024, MNRAS 531 272): "for our purposes we
     treat it as a free parameter" -- empirically pinned by rotation-curve extent,
     NO stated mu=f(Lambda).

This script does NOT re-derive AeST. It tests, BOTH WAYS, whether the FRAMEWORK's
own de Sitter / Unruh / holographic identities supply a relation that AeST itself
lacks -- i.e. could sqrt(Lambda) fix (i) the amplitude I0/Omega_dust, or (ii) the
mass mu^2/K2 -- WITHOUT manufacturing one. Quarantine held (a0/Z/kappa not derived).
"""
import numpy as np

# ---- constants ----
c    = 2.99792458e8        # m/s
G    = 6.674e-11           # SI
Mpc  = 3.0857e22           # m
H0   = 67.7*1e3/Mpc        # s^-1
hbar = 1.0546e-34
kB   = 1.381e-23

OmL  = 0.685
OmM  = 0.315
Omb  = 0.0493
Omdm = OmM - Omb           # ~0.266 cold dark / dust the CMB+clusters need

# Lambda and a0 (framework, pure-Lambda footing)
Lambda = 3*OmL*H0**2/c**2                 # m^-2
a0     = c**2*np.sqrt(Lambda/(32*np.pi))  # m/s^2
H_L    = c*np.sqrt(Lambda/3)              # de Sitter Hubble of the Lambda-only dS
Z      = np.sqrt(32*np.pi/3)

print("="*78)
print("FRAMEWORK ANCHORS (what sqrt(Lambda) DOES set)")
print("="*78)
print(f"  Lambda                 = {Lambda:.4e} m^-2")
print(f"  a0 = c^2 sqrt(L/32pi)  = {a0:.4e} m/s^2   (target 9.36e-11)")
print(f"  Z = sqrt(32pi/3)       = {Z:.4f}")
print(f"  cH_Lambda = c*sqrt(L/3)= {a0*Z:.4e}  (= a0*Z, the dS-Unruh anchor)")
print(f"  => a0 fixes the DARK-ENERGY face: Omega_DE = {OmL:.3f}  (REAL z=0 unification)")
print()
print("  Bridge-1 theorem (banked): a0 is PROVABLY ABSENT from LINEAR perturbation")
print("  theory (Y=0 on FRW; the Y^3/2 term is O(delta phi^3)). So a0/sqrt(Lambda)")
print("  adds EXACTLY 0 to the CMB/growth transfer functions that the dust feeds.")

print()
print("="*78)
print("TEST 1 -- CAN sqrt(Lambda) FIX THE AMPLITUDE I0 (Omega_dust)?  [the prize]")
print("="*78)
# The honest test: is there ANY framework relation Omega_dust = f(Lambda, a0, Z)?
# Enumerate the only candidate 'holographic/dS' identities that exist and check
# whether ANY lands on Omega_dust ~ 0.26 WITHOUT a tuned O(1) put in by hand.
print(f"  Target to be 'pinned': Omega_dust ~ {Omdm:.3f}  (= Omega_dm, the a^-3 amount)")
print(f"  why-now ratio Omega_dust/Omega_DE = {Omdm/OmL:.3f}  (the O(1) number to explain)")
print()
print("  Candidate dS/holographic identities and what they give:")
cands = []
# (a) equality Omega_dust = Omega_DE (a 'coincidence' relation):
cands.append(("Omega_dust = Omega_DE",                 OmL,            "predicts 0.685, OFF by 2.6x"))
# (b) Omega_dust = (1-Omega_DE) trivially = Omega_M (circular: that's the def):
cands.append(("Omega_dust = 1 - Omega_DE (=Om_M)",     1-OmL,          "= Om_M by DEFN; includes baryons; circular, sets nothing"))
# (c) a Z-suppression of dark energy:  Omega_DE / Z:
cands.append(("Omega_DE / Z",                          OmL/Z,          f"predicts {OmL/Z:.3f}, OFF (no reason for /Z)"))
# (d) sqrt(Omega_DE)*something / holographic 1/sqrt:
cands.append(("Omega_DE^(3/2)",                        OmL**1.5,       f"predicts {OmL**1.5:.3f}, ~coincidentally near 0.57? still not 0.26"))
# (e) a holographic entropy ratio S_dust/S_dS -- but S_dust is not defined w/o I0:
cands.append(("holographic S ratio (needs I0)",        np.nan,         "CIRCULAR: any holographic dust entropy already CONTAINS I0"))
for name,val,note in cands:
    sval = f"{val:.3f}" if val==val else "  -- "
    print(f"    {name:32s} -> {sval}   {note}")
print()
print("  VERDICT TEST 1: NONE of the dimensionless dS/holographic identities lands")
print("  on Omega_dust~0.26 without a hand-tuned O(1). The ONLY ways to 'hit' 0.26")
print("  are (i) put the O(1) in by hand (= tuning I0, exactly what AeST already")
print("  does) or (ii) define a dust entropy that already contains I0 (circular).")
print("  KEY structural reason it CANNOT be pinned: I0 is an INTEGRATION CONSTANT of")
print("  the shift-symmetric phi-bar EOM -- it is fixed by an INITIAL DATUM (the")
print("  displacement of Q from Q0 at early times), NOT by the action's couplings.")
print("  Lambda, a0, Z are all ACTION COUPLINGS (Lagrangian constants). A boundary/")
print("  initial constant is orthogonal to the bulk couplings by construction; no")
print("  amount of dS-Unruh thermodynamics on the couplings can set an initial datum.")

print()
print("="*78)
print("TEST 2 -- CAN sqrt(Lambda) FIX THE MASS mu^2 (the K2 / V(Q) curvature)?")
print("="*78)
# mu is the metric-potential mass from spontaneous breaking of time-diffs.
# Verwayen-Skordis-Zlosnik 2024: treated as FREE; empirically mu^-1 ~ extent of
# flat rotation curves (~ tens-hundreds kpc). Compare to the ONLY framework length
# scales: the dS/Hubble radius and the a0-crossover (MOND) radius.
mu_inv_emp_lo = 50*1e-3*Mpc     # ~50 kpc lower (rotation-curve extent)
mu_inv_emp_hi = 1.0*Mpc         # ~1 Mpc upper (CMB coherence / Verwayen)
R_dS  = c/H_L                   # de Sitter horizon ~ Hubble radius
# a0-crossover radius for a galaxy of mass M: R_a0 = sqrt(GM/a0). use M_MW~1e11 Msun
Msun = 1.989e30
M    = 1e11*Msun
R_a0 = np.sqrt(G*M/a0)
print(f"  mu^-1 empirical (Verwayen+24 / rotation-curve extent): ~{mu_inv_emp_lo/Mpc*1e3:.0f} kpc - {mu_inv_emp_hi/Mpc:.1f} Mpc")
print(f"  framework length scales for comparison:")
print(f"    de Sitter horizon  c/H_Lambda          = {R_dS/Mpc:.0f} Mpc   (~{R_dS/Mpc/ (mu_inv_emp_hi/Mpc):.0f}x too big)")
print(f"    a0-crossover R=sqrt(GM/a0) (M=1e11Msun) = {R_a0/Mpc*1e3:.0f} kpc  (galaxy scale -- RIGHT ballpark)")
print()
print("  The a0-crossover radius IS galaxy-scale -- so the mu^-1 ~ rotation-curve")
print("  extent is in the SAME ballpark as the MOND radius. BUT this is a")
print("  CONSEQUENCE, not a pin: mu^-1 ~ R_MOND only because BOTH are tuned to the")
print("  observed flat-curve extent. AeST's mu is NOT mu = f(a0): it is a separate")
print("  combination of {lambda_s, K_B, K2}, and the Mistele/cluster SQUEEZE")
print("  (galaxy-WL wants m^2/f_G < 1 Mpc^-2, clusters want > 1 Mpc^-2) shows it is")
print("  pulled OPPOSITE ways by data -- exactly what a FREE, non-pinned constant")
print("  does. If mu were = f(Lambda) there would be no squeeze freedom to exploit.")
print("  VERDICT TEST 2: mu^2/K2 is FREE; the de Sitter horizon is ~10^3 x too big;")
print("  the galaxy-scale coincidence is the a0-crossover, which is a RESTATEMENT of")
print("  a0, not an independent pin of the dust/CMB sector.")

print()
print("="*78)
print("TEST 3 -- THE DECISIVE SEPARATION: ACTION-COUPLING vs INITIAL-CONDITION")
print("="*78)
print("  a0, Lambda, Z  = couplings IN the Lagrangian K(Y,Q) (the Y^3/2 coeff = a0;")
print("                   the -2Lambda term = Lambda). Fixed by the THEORY.")
print("  I0 (=> Omega_dust) = INTEGRATION CONSTANT of the phi-bar field equation;")
print("                   fixed by an INITIAL DATUM (Q-Q0 at early times). A choice.")
print("  Q0             = the location of the K-expansion point (a free K constant).")
print("  mu^2 ~ K2      = curvature of K at Q0 (a free coupling, empirically pinned).")
print()
print("  => a0=sqrt(Lambda) lives ENTIRELY in the {Y-sector coupling} + {Lambda term}.")
print("     The dust that does clusters+CMB lives in {Q0, I0, K2} -- a DISJOINT slot")
print("     of the same free function, and its AMPLITUDE is an initial condition.")
print("     NO de Sitter/Unruh/holographic identity converts a bulk coupling into an")
print("     initial datum. To claim sqrt(Lambda) pins I0 you must MANUFACTURE an O(1).")

print()
print("="*78)
print("BOTH-WAYS SUMMARY")
print("="*78)
print(f"  CREDIT (do not under-claim): a0<->Lambda IS a real unification of the")
print(f"    dark-ENERGY face (Omega_DE={OmL}); AeST genuinely fits the full CMB incl.")
print(f"    3rd peak via the a^-3 K(Q) dust; the framework's dS-Unruh aether is the")
print(f"    natural microphysical origin for AeST's postulated A_mu (embedding holds")
print(f"    at the {{a0=MOND scale, A_mu=cosmic rest frame}} level).")
print(f"  KILL (do not over-claim): sqrt(Lambda) does NOT pin the K(Q) amplitude.")
print(f"    Omega_dust~{Omdm:.2f} is the FREE integration constant I0 ('rho-bar not")
print(f"    classically predicted'); mu^2/K2 is a FREE empirically-pinned mass; the")
print(f"    why-now ratio Omega_dust/Omega_DE~{Omdm/OmL:.2f} is an O(1) the framework")
print(f"    does NOT set (Bridge-1: a0 absent from linear theory). NO dS/Unruh/holo")
print(f"    identity ties a bulk coupling (Lambda) to a boundary integration constant.")
print(f"  NET: ZERO-free-numbers is FALSE; ONE-free-number is the honest prize, and it")
print(f"    is really TWO+ free numbers in the dark sector ({{I0, Q0, K2/mu, lambda_s,")
print(f"    K_B}}), of which the amplitude I0~Omega_dust is the load-bearing one. The")
print(f"    framework is a COMPLETE relativistic MOND host (galaxies+clusters+CMB+")
print(f"    lensing+Cassini) FOUNDED on de Sitter-Unruh, with the MOND scale a0 tied")
print(f"    to Lambda -- but the dark-MATTER-mimic AMPLITUDE stays FREE. Not zero.")
