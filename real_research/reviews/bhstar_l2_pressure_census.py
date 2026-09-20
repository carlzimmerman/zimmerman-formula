#!/usr/bin/env python3
"""
bhstar_l2_pressure_census.py -- WAVE L2: the pressure-energy census. DOUBLE HONEST KILL.
================================================================================================
THE PUZZLE (from L1): the K-table (Chandrasekhar 1965) says polytrope GR coefficients are
O(1) (kappa_GR = 2K: 0.905 at n=0, 2.249 at n=3). The certified central-beta chain gives
the central gap Gamma1-4/3 = 7.73e-9 at M = 1e5. The criterion needs
kappa_GR * alpha = 2.249 * 2.788e-6 = 6.27e-6 -- 800x the central gap. Yet SMSs at 1e5-6
EXIST (Saio+24: adiabatic analysis, stable to ~1e5 at low accretion rates). Contradiction?

HYPOTHESIS TESTED HERE (and FALSIFIED): "the envelope's gas-dominated layers stabilize the
mode" -- the pressure-weighted adiabatic criterion sums (Gamma1(r)-4/3) P(r) (div xi)^2 dV,
so if the envelope layers are gas-dominated (Gamma1 -> 5/3), they could hold Gamma1_eff up.

THE CENSUS RESULT: FALSIFIED at the CLOUDY densities.
  At n_H = 1e10 cm^-3, T = 5000 K:  P_g = n k T = 6.9e-4 Pa  vs  P_rad = aT^4/3 = 0.158 Pa
  => beta_env = 4.4e-3: the layer is STILL RADIATION-DOMINATED (my hypothesis's arithmetic
  slipped 3 dex on P_g; the census corrects it). gap_env = Gamma1(beta_env)-4/3 ~ 7.3e-4.
  Envelope term = gap_env * P_env = 1.2e-4 Pa vs central term gap_c * P_c = 5.33e3 Pa:
  the amplitude requirement (div xi_env/div xi_c)^2 >= 4.4e7 -> ratio >= 6700 -- far beyond
  the O(10^2) standard for fundamental modes of centrally-condensed stars.

THE DENSITY THAT WOULD BE NEEDED: gas-domination (beta = 0.5) at T = 5000 K requires
  n_H = P_rad/(k T) = 0.158/6.9e-20 = 2.3e12 cm^-3 -- 230x the CLOUDY densities.
  Even there: gap_env = Gamma1(0.5)-4/3 = 0.098, P_env = 0.32 Pa -> envelope term 0.031 Pa
  -> amplitude ratio >= sqrt(5.33e3/0.031) = 415 -- still above the O(10^2) standard.

THE HONEST VERDICT (double kill):
  1. central-beta-only stability: FALSIFIED (L1, K-table: tabulated kappa_GR are O(1)).
  2. envelope-stabilization at CLOUDY densities: FALSIFIED (this census: the layer is
     radiation-dominated too; amplitude requirement >= 6700).
  WHAT REMAINS: the real Saio+24 eigenproblem with MESA Gamma1(r) profiles -- including the
  H/He IONIZATION ZONES where Gamma1 drops LOCALLY below the background (the classical
  pulsation driving physics) and the accretion-built density structure (denser than the
  Eddington-radius estimate at low accretion rates). The constant-gamma K-table and the
  naive two-zone census are both insufficient: the answer lives in the full eigenproblem.
  THE FRAMEWORK READING unchanged: this is 1PN GR-structure physics; the framework
  INHERITS the ceiling if its 1PN dynamical sector is GR-identical (its GR-limit record:
  Cassini gamma, r = 3M/2). No dark matter particle anywhere.

Run:  python3 reviews/bhstar_l2_pressure_census.py  (stdlib only)
"""

import math, json, os

A_R = 7.5657e-16
K_B = 1.380649e-23
SIGMA = 5.670374e-8
KAPPA_ES = 0.04
C = 2.99772458e8
G = 6.674e-11
MSUN = 1.98892e30
AU = 1.495978707e11

M = 1e5 * MSUN
T_EFF = 5000.0
R = math.sqrt(G * M * C / (KAPPA_ES * SIGMA * T_EFF ** 4))
ALPHA = G * M / (R * C ** 2)
KAPPA_N3 = 2.2490
KAPPA_N0 = 19.0 / 21.0

def gamma1(b):
    return b + 2 * (4 - 3 * b) ** 2 / (24 - 21 * b)

# center (certified in G2)
T_C = 7.23e6
P_RAD_C = A_R * T_C ** 4 / 3.0
GAP_C = gamma1(4.638e-8) - 4.0 / 3.0

# envelope at the photosphere, CLOUDY density
N_CLOUDY = 1e10 * 1e6
P_G_ENV = N_CLOUDY * K_B * T_EFF
P_RAD_ENV = A_R * T_EFF ** 4 / 3.0
BETA_ENV = P_G_ENV / (P_G_ENV + P_RAD_ENV)
GAP_ENV = gamma1(BETA_ENV) - 4.0 / 3.0

# the density that gas-domination would need
N_GASDOM = P_RAD_ENV / (K_B * T_EFF)

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

print("=" * 78)
print("WAVE L2 -- THE PRESSURE-ENERGY CENSUS (double honest kill)")
print("=" * 78)

print("\n[A] The census (M = 1e5 Msun, Eddington/Hayashi structure, R = %.0f au)" % (R/AU))
print(f"    CENTER:   P_rad,c = {P_RAD_C:.2e} Pa, gap_c = {GAP_C:.2e}")
print(f"              central term gap_c*P_c = {GAP_C*P_RAD_C:.2e} Pa")
print(f"    ENVELOPE (CLOUDY n = 1e10 cm^-3, T = 5000 K):")
print(f"              P_g = {P_G_ENV:.2e} Pa, P_rad = {P_RAD_ENV:.3f} Pa,")
print(f"              beta_env = {BETA_ENV:.2e}  (STILL RADIATION-DOMINATED)")
print(f"              Gamma1_env = {gamma1(BETA_ENV):.6f}, gap_env = {GAP_ENV:.2e}")
print(f"              envelope term = {GAP_ENV*(P_G_ENV+P_RAD_ENV):.2e} Pa")

print("\n[B] The hypothesis test (FALSIFIED)")
req2 = GAP_C * P_RAD_C / (GAP_ENV * (P_G_ENV + P_RAD_ENV))
print(f"    required (div xi_env/div xi_c)^2 >= {req2:.1e}  ->  ratio >= {math.sqrt(req2):.0f}")
check("HYPOTHESIS FALSIFIED: envelope stabilization needs amplitude ratio >> O(10^2)",
      math.sqrt(req2) > 1000.0, f"ratio >= {math.sqrt(req2):.0f} (standard order is O(10^2))")
check("the CLOUDY-density layer is radiation-dominated (beta_env < 0.05)",
      BETA_ENV < 0.05, f"beta_env = {BETA_ENV:.1e}")

print("\n[C] The density gas-domination would require")
print(f"    beta = 0.5 at T = 5000 K needs n_H = P_rad/(k T) = {N_GASDOM/1e6:.1e} cm^-3"
      f"  ({N_GASDOM/1e6/1e10:.0f}x the CLOUDY density)")
check("gas-domination needs n ~ 2.3e12 cm^-3 (230x CLOUDY)",
      abs(N_GASDOM / 1e6 - 2.3e12) / 2.3e12 < 0.2, f"{N_GASDOM/1e6:.1e} cm^-3")
b05 = 0.5
g05 = gamma1(b05) - 4.0 / 3.0
P_env_gd = 2.0 * P_RAD_ENV
req2_gd = GAP_C * P_RAD_C / (g05 * P_env_gd)
print(f"    even there: gap_env = {g05:.3f}, envelope term = {g05*P_env_gd:.3f} Pa")
print(f"    amplitude ratio >= {math.sqrt(req2_gd):.0f}  (still above O(10^2))")
check("even at the gas-domination density the amplitude requirement exceeds O(10^2)",
      math.sqrt(req2_gd) > 300.0, f"ratio >= {math.sqrt(req2_gd):.0f}")

print("\n[D] THE DOUBLE-KILL VERDICT")
print("    1. central-beta-only stability: FALSIFIED (L1, K-table)")
print("    2. envelope-stabilization at CLOUDY densities: FALSIFIED (this census)")
print("    WHAT REMAINS: the full Saio+24 eigenproblem with MESA Gamma1(r) profiles --")
print("    including the H/He ionization zones (classical driving physics) and the")
print("    accretion-built density structure. THE FRAMEWORK READING unchanged: 1PN")
print("    GR-structure physics, INHERITED if the framework's 1PN dynamical sector is")
print("    GR-identical (Cassini gamma, r = 3M/2). No dark matter particle anywhere.")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-L2> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_l2_pressure_census",
           door="pressure-energy census: envelope-stabilization hypothesis FALSIFIED",
           center=dict(P_rad_c=P_RAD_C, gap_c=GAP_C, central_term=GAP_C*P_RAD_C),
           envelope=dict(P_g=P_G_ENV, P_rad=P_RAD_ENV, beta=BETA_ENV, gap=GAP_ENV),
           requirement=dict(ratio_squared=req2, ratio=math.sqrt(req2)),
           gasdom_density_cm3=N_GASDOM/1e6,
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_l2_pressure_census_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
