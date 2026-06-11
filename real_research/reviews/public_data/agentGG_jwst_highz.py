#!/usr/bin/env python3
"""
agentGG: JWST-era high-z kinematics vs the a0(z) branches — the inline confrontation (2026-06-11).

Watch-entry-6 pre-registered response, executed on what JWST/ALMA have actually published by 2026-06.
Provenance (every number traced to a fetched table/section; NO figure-read values):

  REBELS-25 (Rowland+ 2024, arXiv:2405.06025; ALMA [CII], z=7.31):
    Vrot,max = 372 +82/-66 km/s, inclination-CORRECTED (i = 25+/-6 deg, CANNUBI; Table 2 / sec 4.2.4)
               RC "flattens to ~370 km/s at around 2 kpc" (sec 4.2.3); sigma = 33+/-9 (Table 2)
    M*       = 8 +4/-2 e9 Msun (Table 1)
    L_[CII]  = 1.7+/-0.2 e9 Lsun (Table 1)
    Mgas(paper) = 1.1e11 = Mdyn - M*  -> CIRCULAR for any baryonic test; EXCLUDED here.
      Their alpha_[CII] = 62 is Mdyn-derived too (sec 4.2.4). Independent gas bracket used instead:
      alpha_[CII] in [7 (DSFG-like; their 'factor ~10 below 62'), 30 (Zanella+19 SFG median)]
      -> Mgas_indep in [1.2e10, 5.1e10];  Mbar bracket [stars-only 8e9, 5.9e10].
    re = 2.1+/-0.2 kpc (Sersic, Table 2); Mdyn,tot = 1.2+/-0.3 e11 (sec 4.2.4; cross-check only).

  DLA0817g1 "Wolfe disk" (arXiv:2512.05213; JWST/NIRSpec Halpha + ALMA [CII], z=4.26):
    vrot(Re): Halpha 206+/-14, [CII] 235+/-16 km/s (Table 5; inclination-corrected, i ~ 46-60 deg)
    M*   = 10^10.6+/-0.2 (sec 5.2.3; independent of these dynamics)
    Mgas = 10^10.24+/-0.05 ([CII] conversion, Vallini+25; Table 3 — independent of dynamics)
    Mdyn = 10^10.9+/-0.1 (Table 5; cross-check only); Re = 2.0+/-0.1 kpc (Table 1)

  de Graaff+ 2024 (arXiv:2308.09742; NIRSpec MOS, 6 JADES galaxies z=5.5-7.4):
    v(re) = 5-148 km/s (Table 3, NOT inclination-corrected), sigma0 = 37-60, log Mdyn = 9.2-10.2 (Table 3)
    Per-galaxy M* live in Appendix B (not retrievable from the fetched HTML; gas masses SFR-inferred only)
    -> DIRECTIONAL BIN ONLY (no fit entry): their own reading is Mbar-systematics-dominated.

Footing rule (MEMORY.md): both footings run (a0 = 9.36e-11 fw / 1.2e-10 canon); declining branch is the
framework's sqrt(rho_DE(z)) with the repo's two locked CPL sets; rising rival is E(z); C3 fence: every
statement below is keyed to the z>4 data here, none to z=0.
"""
import numpy as np

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"fw 9.36e-11": 9.36e-11, "canon 1.2e-10": 1.2e-10}
OM = 0.315
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + (1 - OM))

def rhoDE_ratio(z, w0, wa):                      # CPL rho_DE(z)/rho_DE0
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))

CPL = [(-0.83, -0.75, "DESI24 BAO+CMB+DESY5 [project_a0_tracks_dark_energy.py]"),
       (-0.752, -0.86, "DESI DR2 [efe_vs_z_recompute.py]")]

def branches(z):
    out = {"constant": 1.0, "rising E(z) [rival]": E(z)}
    for w0, wa, tag in CPL:
        out[f"declining sqrt(rhoDE) {tag}"] = np.sqrt(rhoDE_ratio(z, w0, wa))
    return out

def vflat_kms(mbar_msun, a0):                    # MOND asymptote V^4 = G Mbar a0
    return (G * mbar_msun * MSUN * a0) ** 0.25 / 1e3

def r_mond_kpc(mbar_msun, a0):                   # where g_bar = a0 (point-mass)
    return np.sqrt(G * mbar_msun * MSUN / a0) / KPC

print("=" * 100)
print("agentGG: JWST high-z kinematics vs the a0(z) branches — regime analysis first, verdicts second")
print("=" * 100)

objs = [
    dict(name="REBELS-25", z=7.31, V=372.0, Vlo=66.0, Vhi=82.0, r_kpc=2.0,
         mbar_lo=8e9, mbar_hi=5.9e10, mbar_note="stars-only -> stars + alpha_CII in [7,30]"),
    dict(name="DLA0817g1 (Halpha)", z=4.26, V=206.0, Vlo=14.0, Vhi=14.0, r_kpc=2.0,
         mbar_lo=10 ** (10.6 - 0.2) + 10 ** (10.24 - 0.05),
         mbar_hi=10 ** (10.6 + 0.2) + 10 ** (10.24 + 0.05),
         mbar_note="M* + Mgas_[CII], both dynamics-independent"),
    dict(name="DLA0817g1 ([CII])", z=4.26, V=235.0, Vlo=16.0, Vhi=16.0, r_kpc=1.9,
         mbar_lo=10 ** (10.6 - 0.2) + 10 ** (10.24 - 0.05),
         mbar_hi=10 ** (10.6 + 0.2) + 10 ** (10.24 + 0.05),
         mbar_note="same Mbar, [CII] tracer"),
]

for o in objs:
    r_m = o["r_kpc"] * KPC
    g_obs = (o["V"] * 1e3) ** 2 / r_m
    print(f"\n--- {o['name']}  (z = {o['z']}) ---")
    print(f"  V(outer) = {o['V']:+.0f} +{o['Vhi']:.0f}/-{o['Vlo']:.0f} km/s at r = {o['r_kpc']} kpc")
    print(f"  g_obs = V^2/r = {g_obs:.3e} m/s^2")
    print(f"  Mbar bracket [{o['mbar_lo']:.2e}, {o['mbar_hi']:.2e}] Msun  ({o['mbar_note']})")
    for a0name, a0 in A0.items():
        print(f"  footing {a0name}:  g_obs = {g_obs / a0:6.1f} a0")
        # g_bar at the measured radius (point-mass upper bound x enclosed-fraction bracket 0.5-1.0)
        for tag, mb in [("Mbar_lo", o["mbar_lo"]), ("Mbar_hi", o["mbar_hi"])]:
            gbar_pm = G * mb * MSUN / r_m ** 2
            print(f"    {tag}: g_bar(point-mass) = {gbar_pm:.2e} ({gbar_pm / a0:5.1f} a0);"
                  f" enclosed-frac 0.5 -> {0.5 * gbar_pm / a0:5.1f} a0")
        # the three-branch MOND asymptote and where it would be measurable
        print(f"    branch predictions (V_flat^4 = G Mbar a0(z); r_MOND = sqrt(G Mbar / a0(z))):")
        for bname, fac in branches(o["z"]).items():
            a0z = a0 * fac
            vlo, vhi = vflat_kms(o["mbar_lo"], a0z), vflat_kms(o["mbar_hi"], a0z)
            rlo, rhi = r_mond_kpc(o["mbar_lo"], a0z), r_mond_kpc(o["mbar_hi"], a0z)
            print(f"      {bname:55s} a0(z)/a0 = {fac:5.3f} | V_flat = [{vlo:5.0f},{vhi:5.0f}] km/s"
                  f" | r_MOND = [{rlo:4.1f},{rhi:4.1f}] kpc")

print("\n" + "=" * 100)
print("(2) THE REGIME VERDICT — predicted V at the MEASURED radius, per branch x Mbar endpoint")
print("=" * 100)
nu = lambda y: np.sqrt(1.0 + 1.0 / y)            # the framework's own baseline shape (agentCC locked)
for o in objs:
    r_m = o["r_kpc"] * KPC
    g_obs = (o["V"] * 1e3) ** 2 / r_m
    for a0name, a0 in A0.items():
        print(f"  {o['name']:22s} [{a0name:14s}]  g_obs = {g_obs / a0:5.1f} a0 ;"
              f" V_obs = {o['V']:.0f} +{o['Vhi']:.0f}/-{o['Vlo']:.0f} km/s at r = {o['r_kpc']} kpc")
        for bname, fac in branches(o["z"]).items():
            a0z = a0 * fac
            vp = []
            for mb in (o["mbar_lo"], o["mbar_hi"]):
                gbar = G * mb * MSUN / r_m ** 2          # point-mass (upper bound on enclosed gbar)
                gpred = gbar * nu(gbar / a0z)
                vp.append(np.sqrt(gpred * r_m) / 1e3)
            print(f"      {bname:55s} V_pred(r_meas) = [{vp[0]:5.0f},{vp[1]:5.0f}] km/s")
print("""
  CAVEAT on absolutes: V_pred uses POINT-MASS g_bar (all Mbar inside r_meas) = an UPPER bound;
  with the realistic enclosed fraction ~0.5 at r ~ Re every bracket shifts x0.71 (DLA0817g1's
  [300,425] -> [212,300], consistent with the observed 206-235). Only branch DIFFERENCES at fixed
  Mbar are the test here — absolutes test the mass model, and are consistent within it.

  Reading (computed above, not asserted): the measured points sit at g_obs = 5.7-24 a0.
  - CONSTANT and both DECLINING branches are Newtonian-degenerate at the measured radii: their
    V_pred(r_meas) brackets differ by <4% — far below the >=20% Mbar-driven width. Indistinguishable.
  - The RISING branch is NOT Newtonian there (its a0_eff(z=7.3) = 13.5 a0 puts REBELS-25 at 2 kpc
    INSIDE its MOND regime, boost ~x1.5-2) — but its V_pred bracket still overlaps the observation
    because the x7 Mbar bracket absorbs the difference.
  -> No branch is discriminated: const/declining are blocked by RADIUS (the fork lives at
     r > r_MOND, beyond every last measured point), the rising rival is blocked by the MASS BUDGET
     (Mbar known only to x7). Any 'BTFR offset' built from these V's tests gas fraction / IMF /
     the Mdyn estimator, not a0(z) — see the de Graaff bin below.
""")

print("=" * 100)
print("(3) THE FORK THAT *IS* WITHIN REACH — deep [CII] RC of REBELS-25 to ~6-10 kpc")
print("=" * 100)
zR = 7.31
for a0name, a0 in A0.items():
    print(f"  footing {a0name} (Mbar bracket [8e9, 5.9e10]):")
    for bname, fac in branches(zR).items():
        a0z = a0 * fac
        vlo, vhi = vflat_kms(8e9, a0z), vflat_kms(5.9e10, a0z)
        print(f"    {bname:55s} V(r >> r_MOND) -> [{vlo:5.0f},{vhi:5.0f}] km/s")
print("""
  At fixed Mbar the rising/declining split is x[ E(7.31)/sqrt(rhoDE_ratio) ]^(1/4) ~ x2.3-2.4 in the
  asymptotic velocity — far larger than the ~20% velocity errors. ONE deep ALMA [CII] map of a
  REBELS-class disc reaching ~3-4x Re settles the branch IF the baryonic mass is pinned
  independently (the current x7 Mbar bracket is the co-blocker: JWST IMF/SED + a non-dynamical gas
  tracer must close it to <~x2 for the fork to open).
""")

print("=" * 100)
print("(4) DIRECTIONAL BIN — de Graaff+ 2024 (6 JADES dwarfs, z=5.5-7.4) and the rest of the sweep")
print("=" * 100)
dg = [("00016745", 5.566, 105, 55, 1.6, 10.23), ("00019606", 5.890, 5, 39.1, 0.6, 9.17),
      ("00022251", 5.799, 148, 37, 0.6, 9.68), ("00047100", 6.679, 120, 53, 0.6, 9.60),
      ("10016374", 6.840, 75, 48, 0.4, 9.22), ("20086025", 7.440, 30, 60, 1.5, 10.06)]
print("  ID          z      v(re)  sigma0  re_kpc  logMdyn   g_dyn/a0(canon)")
for gid, z, v, s, re, lmd in dg:
    gdyn = G * 10 ** lmd * MSUN / (re * KPC) ** 2
    print(f"  {gid}  {z:5.3f}  {v:5.0f}  {s:6.1f}  {re:6.1f}  {lmd:7.2f}   {gdyn / 1.2e-10:8.1f}")
print("""
  All six sit at g_dyn ~ 8-100 a0 (compact, dispersion-supported): the Mdyn/M* = 10-40 excess is a
  high-acceleration mass-budget statement (their own reading: large gas masses or M* systematics),
  NOT a low-acceleration gravity statement — non-diagnostic for a0(z) AND for the a* floor.
  No object from the sweep reaches g < 5e-12 m/s^2: nothing enters the agentCC a* window either.

  Unprocessed sweep candidates (extraction blocked by the spend-limit kill; for a future pass):
    2403.03192 (GN20, z=4: non-circular flagged), 2506.04310 (15 quiescent z~2, stellar Jeans),
    2501.17145 (16 sub-L* z=4-7.6, dispersion bin), 2503.21863 (272 grism emitters, population-level),
    2507.14936 (2 dwarfs z=7.66, outflow-contaminated). None tabulates a low-g rotation point.
""")
print("VERDICT: REGIME-INSUFFICIENT (not data-insufficient in the generic sense): published JWST-era")
print("high-z kinematics all sit at g_obs > 5 a0 where the branches degenerate; the named opener is a")
print("deep [CII] RC of a REBELS-class disc + an independent Mbar to x2. Registered as a watch trigger.")
