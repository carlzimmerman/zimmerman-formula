#!/usr/bin/env python3
"""
agentVV placement: place the NEW (2024-2026) data points on the agentCC two-branch a* plane
(floor at a* vs pure sqrt deep-MOND law), BOTH footings, framework convention from
agentCC_astar_hunt.py (g_obs vs g_bar; d_sqrt = log10 g_obs - 0.5 log10(g_bar*a0)).

NEW points pinned 2026-06-13 (agentVV):
  1. AGC 114905 -- Mancera Pina+ 2024 (A&A 689, A344 = arXiv:2502.08717 imaging companion 2502...,
     the GTC deep-imaging inclination paper aa50230-24): i = 31 +- 2 deg from STELLAR disc axis ratio
     b/a = 0.86 +- 0.02; V_out ~ 35-40 km/s at r ~ 7.4 kpc; M_bar = 1.47e9 Msun; isolated (e_N ~ 0.01).
     MOND ruled out unless i ~ 12 deg, which the new stellar imaging EXCLUDES (would need b/a ~ 0.98).
     => the floor-shaped object is DEFENDED at i ~ 31 deg, the i=15 reconciliation contested/weakened.
"""
import numpy as np
G = 6.674e-11; kpc = 3.086e19; Msun = 1.989e30
A0_FW, A0_CN = 9.36e-11, 1.2e-10

def dsqrt(gobs, gbar, a0): return np.log10(gobs) - 0.5*np.log10(gbar*a0)
def gobs_of(V, R): return V**2 / R
def gbar_of(Mb, R): return G*Mb / R**2

print("="*78)
print("agentVV -- AGC 114905 on the agentCC two-branch plane (NEW 2024 GTC i=31+-2deg)")
print("="*78)

# --- The new 2024 A&A measured point (i = 31 deg, the defended inclination) ---
# Outer measured circular speed ~35 km/s at r ~ 7.4 kpc (aa50230-24 / aa2024 fetch).
# Use the agentCC-stored inner V_flat=23 km/s at 10 kpc as a CONSERVATIVE cross-check too.
Mb = 1.47e9 * Msun
for label, V, R in [("2024 outer (V=35 km/s @ 7.4 kpc, i=31)", 35e3, 7.4*kpc),
                    ("agentCC stored (V=23 km/s @ 10 kpc)",     23e3, 10.0*kpc)]:
    go = gobs_of(V, R); gb = gbar_of(Mb, R)
    print(f"\n{label}")
    print(f"  g_bar = {gb:.2e} m/s^2  ({gb/A0_FW:.4f} a0_fw / {gb/A0_CN:.4f} a0_cn)")
    print(f"  g_obs = {go:.2e} m/s^2  ({go/A0_FW:.4f} a0_fw / {go/A0_CN:.4f} a0_cn)")
    print(f"  d_sqrt(fw) = {dsqrt(go,gb,A0_FW):+.2f} dex   d_sqrt(cn) = {dsqrt(go,gb,A0_CN):+.2f} dex")

# --- Inclination lever: how much does g_obs move from i=31 to i=15? ---
print("\n" + "-"*78)
print("Inclination lever (V deprojected ~ 1/sin i):  g_obs scales as (sin i_meas / sin i_alt)^2")
V0, R = 35e3, 7.4*kpc
gb = gbar_of(Mb, R)
for i_alt in [31, 25, 20, 15, 12]:
    Valt = V0 * np.sin(np.deg2rad(31)) / np.sin(np.deg2rad(i_alt))
    go = gobs_of(Valt, R)
    print(f"  i={i_alt:2d} deg: V_dep = {Valt/1e3:5.1f} km/s, g_obs = {go:.2e} "
          f"({go/A0_FW:.3f} a0_fw)  d_sqrt(fw) = {dsqrt(go,gb,A0_FW):+.2f}")

# --- Where on the a* axis does the i=31 deviation sit (if interpreted as a floor)? ---
print("\n" + "-"*78)
print("If the i=31 downturn is a floor, a* ~ g_obs at the downturn:")
go31 = gobs_of(35e3, 7.4*kpc)
print(f"  a*_implied ~ g_obs(i=31) = {go31:.2e} m/s^2 = {go31/A0_FW:.3f} a0_fw / {go31/A0_CN:.3f} a0_cn")
print(f"  Band line (binding): a* < 0.05 a0 = {0.05*A0_FW:.2e} (fw) / {0.05*A0_CN:.2e} (cn)")
print(f"  agentCC SPARC direct bound: a* <~ 0.08-0.11 a0")
print(f"  --> a*_implied is {'INSIDE' if go31 < 0.05*A0_FW else 'ABOVE'} the binding band window (fw).")

print("\n" + "="*78)
print("CRISTAL / REBELS-25 a0(z) fork: radial-extent gate (agentGG convention)")
print("="*78)
print("agentGG fork: need a [CII] RC reaching ~3-4 R_e (r >~ 6-10 kpc, past r_MOND) to split")
print("declining/constant/rising by x2.3-2.4 in V_asym at fixed M_bar.")
print("CRISTAL (2507.11600 / aa55362-25): kinematics traced to ~1.5-3 R_e, R_out ~ 9-20 kpc;")
print("  EXCEPTION CRISTAL-23c reaches ~9 R_e. Most disks show velocity FALL-OFF (baryon-dominated).")
print("  BUT: ~50% are in multiple-component/interacting systems within ~20 kpc -> NOT isolated,")
print("  median sigma ~70 km/s, V/sigma ~2 -> dispersion-dominated outer pressure support.")
print("REBELS-25 (2405.06025): unchanged since agentGG; M_bar still x7-bracketed (no independent")
print("  alpha_[CII] published 2024-2026); RC reaches only ~2 kpc (inside r_MOND) -> fork still BLOCKED.")
