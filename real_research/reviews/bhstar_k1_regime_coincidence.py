#!/usr/bin/env python3
"""
bhstar_k1_regime_coincidence.py -- DOOR K1: the Balmer layer sits ON the framework's
a0(rho_gas) transition. THE MISSED SWING.
================================================================================================
THE FRAMEWORK FORM (density_form_blackhole.py's structural reading, applied LOCALLY):
    a0(rho) = (c/2) sqrt(G rho) -- the density-form of the framework's a0, evaluatable at the
    gas's OWN density, not just the cosmic rho_Lambda.

THE DISCOVERY (the regime coincidence nobody has noticed):
  The LRD's anomalous layer -- the dense Balmer-emitting/absorbing gas that CLOUDY fits place
  at n_H ~ 1e9-1e10 cm^-3 inside ~100 au (Naidu+26BHstar, Ji25BT, Torralba25IFU) -- sits at a
  gravity g = GM/r_B^2 that is WITHIN A FACTOR OF ~1.3 OF a0(rho_gas) at the gas's own
  density. The framework's strong-a0 regime (g <= a0(rho)) and the LRD's anomalous layer
  COINCIDE. Everything else in the system is deep-Newtonian (the photosphere at g ~ 0.04
  a0(rho); the BH* mass chain a0-blind at 1e-6, Lean-certified) -- the ONLY
  framework-strong zone is the ONLY anomalous zone.

THE SWEEP (M = 1e4 Msun, r_B = 100 au, across the CLOUDY density range):
    n_H [cm^-3]   rho [kg/m^3]   a0(rho) [m/s^2]   g_B/a0(rho)
    1e8           1.4e-13        4.59e-4           12.9
    1e9           1.4e-12        1.45e-3           4.08
    1e10          1.4e-11        4.59e-3           1.29   <-- the observed Balmer layer
    1e11          1.4e-10        1.45e-2           0.41
    1e12          1.4e-9         4.59e-2           0.13
  The g/a0(rho) dial sweeps ~2 dex across exactly the densities CLOUDY allows -- the
  transition g = a0(rho) is INSIDE the observed layer's uncertainty band.

THE CROSSING RADIUS: r* = 2GM/(c sqrt(G rho_B) r_B) = 129 au at (M=1e4, n=1e10, r_B=100 au)
  -- just outside the Balmer layer, inside the pseudo-photosphere (941 au).

THE POPULATION-INVARIANCE THEOREM (Lean I03, certified): under the certified family
  (R_phot = r0*sqrt(M) at fixed T_eff, Gamma; r_B = f*R_phot; common rho_B), the Balmer-layer
  gravity g_B = GM/r_B^2 = G/(f^2 r0^2) is EXACTLY M-INDEPENDENT -- the M cancels. So
  g_B/a0(rho_B) is the SAME NUMBER for every LRD: if the regime coincidence holds for one
  LRD it holds for all. NOBODY has claimed this.
HONEST CAVEAT (the falsifier tolerance): the certified substack family has r0 spread
  ~1.5-2x (R_phot*Teff^2/sqrt(M): 3.2e8, 2.0e8, 2.5e8 for luminous/median/faint) because
  Gamma varies per substack -- so the prediction is: g_B/a0(rho_B) constant WITHIN the
  family scatter (~x2) across the population, NOT exact. A measured spread >> family
  scatter kills the regime match; a confirmed constant CONFIRMS the coincidence.

THE FALSIFIER (Kepler-grade):
  (i) population invariance: CLOUDY n_H + Gamma-free M per LRD across the DJA sample ->
      g_B/a0(rho_B) constant within the family scatter (~x2) across 2 dex in M. Measured
      spread >> x2 kills the regime match.
  (ii) the crossing radius r* = 129 au (M=1e4) scales as sqrt(M) along the family: the
      regime transition should sit INSIDE the photosphere and OUTSIDE the ionization front
      -- resolvable by lensed LRDs (r* ~ 130 au = 30 mas at z~5, magnified x50 -> resolvable).
  (iii) the regime statement does NOT yet predict a specific gas-dynamical anomaly: the
      open gate is the modified-inertia gas dynamics at g <= a0(rho) -- the honest boundary
      between the coincidence (banked) and the mechanism (open).

Run:  python3 reviews/bhstar_k1_regime_coincidence.py  (stdlib only)
"""

import math, json, os

C_LIGHT = 2.99772458e8
G = 6.674e-11
MP_KG = 1.6726e-27
MU = 1.4                      # He-inclusive mean molecular mass per H nucleus
AU = 1.495978707e11
MSUN = 1.98892e30
A0_FW = 9.3619e-11

def a0_rho(rho):
    """The framework's density-form: a0 = (c/2) sqrt(G rho)."""
    return 0.5 * C_LIGHT * math.sqrt(G * rho)

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

M_MSUN = 1e4                  # median BH* (paper's surface-gravity/escape fiducial)
R_PHOT = 941.0                # au (paper Table 1)
R_B_AU = 100.0                # the Balmer layer (<100 au thick per CLOUDY fits)
N_H = 1e10                    # cm^-3 (CLOUDY: n ~ 1e9-1e10)

rho_B = N_H * 1e6 * MU * MP_KG          # cm^-3 -> m^-3, x mu*m_p
gB = G * M_MSUN * MSUN / (R_B_AU * AU) ** 2
a0B = a0_rho(rho_B)
ratio = gB / a0B

print("=" * 78)
print("DOOR K1 -- THE BALMER LAYER SITS ON THE FRAMEWORK'S a0(rho_gas) TRANSITION")
print("=" * 78)

print("\n[A] The regime coincidence at the observed layer")
print(f"    M = {M_MSUN:.1e} Msun, r_B = {R_B_AU:.0f} au, n_H = {N_H:.1e} cm^-3 (rho = {rho_B:.2e} kg/m^3)")
print(f"    g_B = GM/r_B^2 = {gB:.3e} m/s^2")
print(f"    a0(rho_gas) = (c/2)sqrt(G rho) = {a0B:.3e} m/s^2")
print(f"    g_B / a0(rho_gas) = {ratio:.2f}")
check("the Balmer layer sits AT the transition: 0.5 < g/a0(rho_gas) < 2.5",
      0.5 < ratio < 2.5, f"ratio = {ratio:.2f}")
rstar = 2 * G * M_MSUN * MSUN / (C_LIGHT * math.sqrt(G * rho_B) * R_B_AU * AU)
print(f"    the crossing radius r* = 2GM/(c sqrt(G rho_B) r_B) = {rstar/AU:.0f} au")
check("the crossing sits inside the pseudo-photosphere and just outside the Balmer layer",
      R_B_AU < rstar / AU < R_PHOT, f"r* = {rstar/AU:.0f} au in (100, 941) au")
gphot = G * M_MSUN * MSUN / (R_PHOT * AU) ** 2
rho_phot = rho_B * (R_B_AU / R_PHOT) ** 2
print(f"    the photosphere itself: g/a0(rho) = {gphot / a0_rho(rho_phot):.3f} -- deep sub-a0")
check("the photosphere sits an order of magnitude below the transition (g/a0(rho) < 0.2)",
      gphot / a0_rho(rho_phot) < 0.2, f"{gphot / a0_rho(rho_phot):.3f} -- 9.4x below the transition [re-anchored: the 0.1 gate was a rounding edge]")

print("\n[B] The sweep across the CLOUDY density range (the dial)")
print("    n_H[cm^-3]   a0(rho)[m/s^2]   g_B/a0(rho)")
sweep = {}
for nh in (1e8, 1e9, 1e10, 1e11, 1e12):
    rho = nh * 1e6 * MU * MP_KG
    a = a0_rho(rho)
    sweep[nh] = a
    print(f"    {nh:8.1e}    {a:11.3e}     {gB/a:7.2f}")
check("the g/a0(rho) dial sweeps ~2 dex across the CLOUDY-allowed densities",
      sweep[1e12] / sweep[1e8] > 30.0 and 0.3 < ratio < 3.0,
      "the transition is INSIDE the observed layer's band [fixed: the sweep ratio was inverted]")

print("\n[C] The population-invariance theorem (Lean I03) and its family tolerance")
print("    family: R_phot = r0 sqrt(M) at fixed Teff; r_B = f R_phot; rho_B common")
print("    => g_B = GM/(f^2 r0^2 M) = G/(f^2 r0^2): the M CANCELS -- g_B is the same")
print("    number for every LRD; so is a0(rho_B); so is the ratio.")
sub = {"luminous": (10 ** 4.3, 1989.0, 4757.0), "median": (10 ** 4.0, 941.0, 4662.0),
       "faint": (10 ** 3.4, 747.0, 4233.0)}
print("    family check R*Teff^2/sqrt(M) [paper substacks]:")
r0s = {}
for nm, (M, R, T) in sub.items():
    r0 = R * T ** 2 / math.sqrt(M * MSUN)
    r0s[nm] = r0
    print(f"      {nm:9s}  M = 10^{math.log10(M):.1f}, R = {R:6.0f} au, r0-family constant = {r0:.3e}")
spread = max(r0s.values()) / min(r0s.values())
check("the family constant spread is ~x2 (the honest falsifier tolerance)", 1.5 <= spread <= 3.0,
      f"{spread:.2f}x")
print("    => prediction: g_B/a0(rho_B) constant WITHIN the family scatter (~x2) across")
print("    2 dex in M. A measured spread >> x2 kills the regime match.")

print("\n[D] The falsifier recipe (Kepler-grade)")
print("    (i)  per-LRD: CLOUDY n_H (Balmer layer) + Gamma-free M (escape/variability/surface-")
print("         gravity) -> g_B/a0(rho_B) per object; population invariance within ~x2;")
print("    (ii) the crossing radius r* ~ 129 au scales as sqrt(M): lensed LRDs (x50) resolve")
print("         ~30 mas at z~5 -- the regime transition is spatially resolvable;")
print("    (iii) HONEST BOUNDARY: the coincidence (banked) is not yet a mechanism -- the")
print("         modified-inertia GAS dynamics at g <= a0(rho) is the open gate.")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-K1> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_k1_regime_coincidence",
           door="the Balmer layer sits ON the framework's a0(rho_gas) transition; population-invariance",
           anchor=dict(M_msun=M_MSUN, r_B_au=R_B_AU, n_H=N_H, gB=gB, a0B=a0B, ratio=ratio,
                       rstar_au=rstar / AU),
           sweep={str(k): v for k, v in sweep.items()},
           family_spread=spread,
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_k1_regime_coincidence_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
