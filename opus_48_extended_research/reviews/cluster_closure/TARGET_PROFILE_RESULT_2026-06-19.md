# TARGET PROFILE the cluster closure (routes 2/3) must reproduce (2026-06-19)

*Pins the residual eta(R), eta-vs-M500, post-XRISM true eta(R500), and the implied
MISSING-MASS profile M_res(<R) [Msun] the closure must supply at the cluster CORE.
Framework a0=9.36e-11, dS-Unruh interpolation g_pred=sqrt(gbar^2+gbar*a0) (MEMORY footing
rule). Built on the banked eRASS1 + CLUSTER*.md ledgers; code+run in this dir. Both ways,
quarantine held, galaxy veto enforced.*

Code: `target_profile.py` (run produces every number below). Data anchor:
`real_research/data/erass1cl_primary_v3.2.fits` (Bulbul+2024, N=9830 clean).

---

## (a) Residual radial profile eta(R) — CENTRAL, dies outward (eRASS1-anchored, eta(R500)=2.33)

| r/R500 | r [kpc] RICH(1e15) | eta RICH | r [kpc] GROUP(1e14) | eta GROUP |
|---|---|---|---|---|
| 0.05 | 70   | 15.1 | 36  | 23.0 |
| 0.10 | 140  | 9.4  | 72  | 13.9 |
| 0.20 | 280  | 6.0  | 143 | 8.3  |
| 0.30 | 420  | 4.8  | 214 | 6.1  |
| 0.50 | 700  | 3.6  | 358 | 4.2  |
| 0.70 | 980  | 3.0  | 500 | 3.2  |
| 1.00 | 1400 | 2.33 | 715 | 2.33 |
| 1.30 | 1820 | 1.92 | 930 | 1.83 |

Monotone-decreasing outward (9/9 in the banked check), validated vs the banked
`CLUSTER_DENSITY_A0_SHAPE_RECONCILED` table (0.10->8.5 vs banked 7.66; 1.30->1.78 vs 1.55;
shape match within ~10-15%, profile-detail robust). The deficit is a CORE phenomenon.

## (b) eta vs M500 — FLAT to slightly rising (NON-tautological eRASS1 result, real data)

| M500 bin | N | eta_med(R500) | R500_med | gbar/a0 |
|---|---|---|---|---|
| 5e13-1e14 | 1219 | 2.29 | 602 kpc | 0.016 |
| 1e14-2e14 | 3141 | 2.29 | 715 kpc | 0.030 |
| 2e14-4e14 | 3480 | 2.34 | 854 kpc | 0.048 |
| 4e14-7e14 | 1144 | 2.38 | 1063 kpc | 0.072 |
| 7e14-2e15 | 284  | 2.42 | 1280 kpc | 0.095 |

eta does NOT shrink where the baryon budget is most complete -> not a missing-baryon
artifact at R500. Median over all 9830: **eta(R500)=2.33** (5-95%: 2.00-4.43; intrinsic
scatter ~0.04 dex). Core-cutoff scale ~ sqrt(M500): r_core ~ 450 kpc*sqrt(M500/1e15)
(142 kpc @1e14, 636 kpc @2e15) -> Famaey ~450 kpc @ the CLASH 1e15 scale.

## (c) Post-XRISM TRUE eta(R500) — BOTH-WAYS bracket [~1.0, 2.33]

- WL-calibrated catalog (eta-worst): **2.33**.
- Hydrostatic/kinematic branch (Li+2024, WL ~110% above HSE): **1.02** (eta-best).
- **XRISM both-ways correction (Abell 2029 relaxed, arXiv:2505.06533 / 2501.05514):
  non-thermal pressure <=2% at all radii, HSE mass bias ~2% only** -> for RELAXED
  clusters the X-ray hydrostatic mass is RELIABLE (not biased low). So XRISM does NOT
  deflate eta via turbulence; it REMOVES the "hydrostatic is biased low so eta is really 2"
  escape, pulling the equilibrium eta DOWN. The 2.33->~1 deflation is driven by the
  WL-vs-hydrostatic MASS-SCALE gap + disequilibrium skirt, not non-thermal pressure.
- **TRUE eta(R500) target window: [~1.0 (relaxed, HSE-reliable), ~2.33 (WL-calibrated)];
  best single equilibrium estimate ~1.0-1.6.** A central residual survives in relaxed
  gas-complete clusters; the outer 2x is WL/disequilibrium-inflated.

## (d) Implied MISSING-MASS profile M_res(<R) [Msun] — what the closure must supply

Collisionless residual = the NEWTONIAN-equivalent mass that, added to baryons and re-run
through the framework's OWN interpolation, lands g_obs (eRASS1-anchored to eta(R500)=2.33):

| region | RICH M500=1e15 | GROUP M500=1e14 |
|---|---|---|
| M_res(<0.10 R500) | 5.4e13 (~140 kpc) | 6.1e12 (~72 kpc) |
| M_res(<0.30 R500) | **2.3e14 (~420 kpc, CORE)** | **2.3e13 (~214 kpc, CORE)** |
| M_res(<0.50 R500) | 3.7e14 (~700 kpc) | 3.3e13 (~358 kpc) |
| M_res(<R500) | 4.8e14 | 3.2e13 |

**CORE TARGET (the make-or-break): supply ~2e14 Msun (rich) / ~2e13 Msun (group)
collisionless mass inside ~300-450 kpc, that tracks the gas (missing/gas ratio ~10,
Famaey 2025; my shell ratio ~6, order-consistent), cored, with a ~400-450 kpc exp cutoff,
DYING to ~0 by 1.3 R500.** Bullet cross-check (BULLET_CLUSTER_GEOMETRIC_MODEL): ~1.2e15
Msun residual on the galaxies in the merger (full-LOS) -> same kind, scaled.

## THE GALAXY VETO (make-or-break, enforced)

On galaxies the framework RAR IS the data (0.13 dex on 175 SPARC) -> eta=1, **M_res=0**.
Any cluster-core closure (matter profile OR dynamic) MUST leave this untouched:
M_res(galaxy disk) = 0. 40 years of MOND cluster fixes died here. The banked density-a0
shape (right-signed, flattens raw [1.55->7.66] to [0.75->1.30] zero-param) FAILS the veto
(same law on a galaxy disk, rho~1e5-1e6 rho_DE, boosts a0 ~300-1000x and erases the RAR)
and over-closes the outskirts -> a SHAPE target, NOT a delivered cure.

## ROBUSTNESS / both ways
- Robust to cosmic-density a0(z): at z=0.296 a0=9.9e-11 moves the residual <1%; curing
  needs a0~4e-10 (banked). NOT a footing artifact.
- eta(R500)=2.33 is the framework's OWN interpolation + a0 (eta-WORST footing; canonical
  a0=1.2e-10 gives 2.07; the framework pays a ~+12% surcharge for its lower a0).
- Inner eta values (>10 at <0.1 R500) carry NFW-cusp + low-central-gas model dependence
  (~10-15%); the SHAPE and the CORE-integrated M_res (~2e14/~2e13) are the robust targets,
  not the innermost point estimate.

## ONE LINE
The closure must supply a CENTRAL, gas-tracking, cored ~2e14 Msun (rich) / ~2e13 Msun
(group) collisionless residual inside ~300-450 kpc (cutoff ~sqrt(M500)), reproducing
eta(R) that rises from ~2.33 at R500 to ~5-15 in the core and dies to ~1 by 1.3 R500 --
with the equilibrium R500 magnitude bracketed [~1.0, 2.33] -- WITHOUT supplying any M_res
on galaxy scales (the veto). This is what routes 2/3 must hit.
