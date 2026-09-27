# The first-principles derivation chain (FP lanes)

One covariant action at the root, every observable varied out of it, nothing posited by hand below the postulates.
Each lane `FPn_*.py` is a runnable script with named checks, a verdict line
`N/M checks pass; load-bearing failures: K`, a results JSON carrying its `ledger`, and a `MUTATE=1` control that must
fail (rc = 1). `run_chain.py` assembles every lane's ledger into `CHAIN_STATUS.md` and enforces that contract.

```bash
python3 real_research/derivation_chain_2026/run_chain.py
```

Status words: DERIVED (varied out of the chain above, with a script), TIED (an input implemented as an exact
action-level relation, coupling chosen), POSTULATED (an input), FITTED (a constant set by data), CONSTRAINT (a derived
requirement on a lower link), OPEN (owed), FAILS (derived and contradicted by data).

## The inputs

- a0 = kappa c sqrt(G rho_DE), with the form forced by (G, c, rho) and kappa = 1/2 FITTED (FP0). On a true Lambda, a0 is
  flat in z. The link to Lambda is TIED inside the action by the Henneaux-Teitelboim unimodular multiplier (the hub's
  XR20, a075ad7f7). Under evolving dark energy, an action-level field tie reads sqrt(V), not sqrt(rho_DE) (FP0 L2a').
  In the khronon's own terms, a0 = (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda) the asymptotic expansion
  (XR30, 2a2d81f61). The khronon's CMC clock and the unimodular clock stay two structures (unimodular shape dynamics):
  the local count is unchanged and the global count gains one pair.
- The galaxy law P2, g_obs = sqrt(g_bar^2 + g_bar a0): an infrared law (FP0 R2).

## The action as it stands (per 1/16 pi G, c = 1)

The gravity core (FP7's AQUAL-type repair of the C-H/K root, with FP14's eliminations):

    R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi
      - 2 alpha^2 J_Y(h^mn D_m phi D_n phi/alpha^2) + [2 lambda (n.d phi)^2] + heat pair (chi = S_h phi) + S_m[g]

The cosmology separator is H_K1 (FP19), the well-posed repair of H_S (FP13, ill-posed as written; see errata). It reads the
state only through the leaf-averaged expansion <K>_h:

    chi = (S_xi - S_B) phi,   B = L^2/2,   L = L_Lambda 3 Lambda/<K>_h^2
    J_Y = J_P2(Y) + 2 y_th sqrt(Y),   y_th = max(0, 1 + Omega_r - 9 Lambda/<K>_h^2) (<K>_h^2/3 - Lambda) L/alpha   (c_y = 2)

with lambda > 0 required as a regulator (the yield vanishes below z = 0.635). It awaits the hub's XR18-style re-audit and
XR21 stage 2; H_Y (FP9; four declared constants) is the fallback. The dark sector is FK1's internal splitting (FP10), a
light complex scalar whose own rest energy powers the kick.

## What is derived, and what is not (knob ledger; kappa = 1/2 accepted)

| sector | constant | status | lane |
|---|---|---|---|
| core | lambda (inertia) | eliminated under H_Y (lambda = 0); required > 0 under H_S and H_K1 (below z = 0.635). NOT a pure regulator at c_2 = infinity (the hub's XR25): inert for strong-field observables, but a MOND-regime knob across (0, 274.4] (tracking speed 17,300 -> 1,800 km/s, galaxy alpha_2 v^2 1.3e-3 -> 0.12); inert only for lambda <~ 0.03. Counts as a knob unless that range is shown free of trouble (XR18b) | FP14, FP13, FP19, XR25 |
| core | c_2 | ELIMINATED on Minkowski and FRW (c_2 -> infinity: a multiplier). At black holes the limit is not uniform: at c_2 = infinity with alpha_c > 0 the multiplier diverges logarithmically at the universal horizon (r = 3M/2), a curvature singularity at O(alpha_c); finite c_2 is regular. OPEN (XR25) | FP14, XR25 |
| core | alpha_c | REGULATOR (every observable moves <= 1.6e-9) | FP14 |
| core | xi (heat filter) | KNOB: irreducible by a threshold-mass theorem; to be MEASURED by wide binaries (Gaia DR4) | FP17, the hub's XR22 |
| separator | L_Lambda | DECLARED in H_K1: 2.9 Mpc, inside the window 2.65-4.6 (sigma_8 <= 1.02 needs <= 3.0); zero modes alone cannot give it (FP19) | FP19 |
| separator | n = 2, the q = 0 ramp, c_y = 2 | natural choices in H_K1 (c_y chosen after scoring: the only one of four natural normalizations passing both yardsticks); H_Y's y_Lambda and p' are gone | FP13, FP19 |
| dark | eps | IRREDUCIBLE (the only Z4-odd term; a khronon-frame coupling only relabels it) and FITTED (the flagship sets the window's lower end, Harvey its upper) | FP10, FP15 |
| dark | zeta (lambda_0), q, m | FITTED BY DATA: zeta's band is x1.16 wide at the mass floor; sharing q with the separator FAILS the web; m is pinned on the canonical footing, bounded on alt. The yield-onset trigger removes q but keeps zeta and adds a postulated gate form | FP15 |
| dark | cross quartic | POSTULATED (radiatively stable) | FP15 |
| dark | amount, misalignment | initial data (the amount has the status of LCDM's omega_c) | FP10, FP15 |

## Where the theory fails or is undecided

- The group-scale outer profile: R0 overshoots by +0.20 dex for the Local Group, M81 and IC 342 (Cen A matches); fixing
  it costs KiDS (FP11, FP12). FP18 finds the tension is in the data itself: at face value no profile fits both KiDS and
  the Hubble-flow R0 (9.8 sigma, LCDM included); six comparability systematics bring it to 2.3 sigma (UNDECIDED). FP21
  measures the lensing of isolated spirals at 0.3-1.5 Mpc, which decides it.
- Re-accretion of the kicked dark component: FP16 (semi-analytic) finds the window EMPTY. Clusters recapture the escaped
  daughters, so X-COP fails at every kick from 575 to 650 km/s; the flagship, galaxies, KiDS and S8 pass. Only the hub's
  particle-mesh run (XR21 stage 3) could overturn it.
- The small-scale (sub-L) power boost and its cosmic-shear cost need the particle-mesh run (the hub's XR21). Under H_K1 the
  per-mode boost at z = 0 is +0.03/+0.14/+1.34 at k = 0.3/0.5/1 h/Mpc (FP19).
- H_K1's prices (FP19): KiDS for lenses at z = 0.7 comes out at +496, a sharp prediction the data can test; the Local
  Group R0 still fails (1.41/1.46 Mpc). All of FP19's numbers are in the all-matter reading and use FP6's projection, so
  they are provisional until FP20 and FP22.
- Strong lensing (the hub's XR33, 92fe59705): SLACS ellipticals from baryons plus the phantom need a stellar IMF
  0.118 +- 0.013 dex above the spectroscopic relation (CvD12's heaviest); the phantom supplies only 9.5-11% of the
  Einstein mass (g_N ~ 9-11 a0). LCDM's own IMF for the same lenses is off by +0.021 dex.
- No-go results that constrain any repair: local gates (FP3 lemma), the MOND-sector kick (FP4, FP8 reciprocity), and
  xi from (a0, Lambda, G, c) (FP17 theorem).

## Errata

- **FP13 A1 is WRONG at the action level** (corrected by the hub's XR18 N3, 53854a459). The leaf-averaged state term
  does add a local term. Through the O(V) leaf integral, dS/d delta is an O(1) local force with coefficient R_B ~ 7-8 at
  z <= 0.635, so the psi-constraint symbol k^2(1 - R_B) changes sign on k = 0.12-1.62 h/Mpc. H_S as written is linearly
  ill-posed. FP19 carries the correction in its ledger and tests the repairs (stationary B, a <K>_h-only readout).
- **FP9's H_Y fails KiDS at z = 0.4** (+20.6; found by FP13). Its z = 0.25 KiDS pass stands.
- **FP6's KiDS projection `esd_of_M` under-projects** (found by FP18): -59% at 35 kpc, -5 to -14% at 0.3-2.6 Mpc on a
  singular isothermal sphere. Every KiDS chi^2 that used it (FP1, FP6, FP9, FP11, FP12, FP13, FP14) is provisional
  until FP20 re-scores it with an exact projection.
- **FP7's sigma_8 failure used the all-matter reading** (the MOND scalar sourced by, and acting on, the total delta),
  while FP10's dark component does not source the phantom. FP22 derives which reading the action implies and re-scores
  sigma_8, the forest and KiDS in it.
- **FP14's "sigma_8 unchanged for lambda = 0-100"** was measured at the c_2 floor, where lambda_eff = lambda + 277 (the
  hub's XR25, 43cfa1692). At that floor the lambda window is empty, so a required lambda > 0 (FP13, FP19) needs
  c_2 > 7.289e-3; FP14's "c_2 -> infinity is regular" holds on Minkowski and FRW but not uniformly at black holes.
- **FP16's MUTATE banner** names R1, G3 and G9 as the flips; the observed flips are R1, G7 and G9 (without recapture
  X-COP fails on the other side, which G3 does not distinguish). Wording only; no number changes.
- **Numerology is flagged, never claimed:** eps/m^2 = kappa^19 (FP10); (c^2/a0)(32 pi)^-6 = 0.030 pc and
  ((hbar/m)^2/a0)^(1/3) (FP14, FP17); (hbar c/G)^(3/2)/m_p^2 (FP17).
