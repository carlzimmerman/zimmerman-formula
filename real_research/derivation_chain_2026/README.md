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
- The galaxy law P2, g_obs = sqrt(g_bar^2 + g_bar a0): an infrared law (FP0 R2).

## The action as it stands (per 1/16 pi G, c = 1)

The gravity core (FP7's AQUAL-type repair of the C-H/K root, with FP14's eliminations):

    R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi
      - 2 alpha^2 J_Y(h^mn D_m phi D_n phi/alpha^2) + [2 lambda (n.d phi)^2] + heat pair (chi = S_h phi) + S_m[g]

The cosmology separator is H_Y (FP9; linearly healthy, four declared constants), pending the repair of H_S (FP13 -> FP19;
see errata). The dark sector is FK1's internal splitting (FP10), a light complex scalar whose own rest energy powers the
kick.

## What is derived, and what is not (knob ledger; kappa = 1/2 accepted)

| sector | constant | status | lane |
|---|---|---|---|
| core | lambda (inertia) | eliminated under H_Y (lambda = 0); a regulator (lambda > 0, any value) under H_S | FP14, FP13; the hub's XR25 settles it |
| core | c_2 | ELIMINATED (c_2 -> infinity: a multiplier) | FP14 |
| core | alpha_c | REGULATOR (every observable moves <= 1.6e-9) | FP14 |
| core | xi (heat filter) | KNOB: irreducible by a threshold-mass theorem; to be MEASURED by wide binaries (Gaia DR4) | FP17, the hub's XR22 |
| separator | L_Lambda, n, y_Lambda, p' | declared in H_Y; replaced by state readouts in H_S (ill-posed as written; FP19 repairing) | FP9, FP13, FP19 |
| dark | eps | FITTED (the kick) | FP10 |
| dark | m, lambda_0, q | DECLARED | FP10, FP15 |
| dark | amount, misalignment | initial data | FP10, FP15 |

## Where the theory fails or is undecided

- The group-scale outer profile: R0 overshoots by +0.20 dex for the Local Group, M81 and IC 342 (Cen A matches); fixing
  it costs KiDS (FP11, FP12). FP18 tests whether the tension is in the data itself.
- Re-accretion of the kicked dark component decides X-COP, cosmic shear and Harvey (FP10: optimistic window 575-600
  km/s; in place empty). FP16 is the semi-analytic answer; the hub's XR21 stage 3 is the particle-mesh one.
- The small-scale (sub-L) power boost and its cosmic-shear cost need the particle-mesh run (the hub's XR21).
- No-go results that constrain any repair: local gates (FP3 lemma), the MOND-sector kick (FP4, FP8 reciprocity), and
  xi from (a0, Lambda, G, c) (FP17 theorem).

## Errata

- **FP13 A1 is WRONG at the action level** (corrected by the hub's XR18 N3, 53854a459). The leaf-averaged state term
  does add a local term. Through the O(V) leaf integral, dS/d delta is an O(1) local force with coefficient R_B ~ 7-8 at
  z <= 0.635, so the psi-constraint symbol k^2(1 - R_B) changes sign on k = 0.12-1.62 h/Mpc. H_S as written is linearly
  ill-posed. FP19 carries the correction in its ledger and tests the repairs (stationary B, a <K>_h-only readout).
- **FP9's H_Y fails KiDS at z = 0.4** (+20.6; found by FP13). Its z = 0.25 KiDS pass stands.
- **Numerology is flagged, never claimed:** eps/m^2 = kappa^19 (FP10); (c^2/a0)(32 pi)^-6 = 0.030 pc and
  ((hbar/m)^2/a0)^(1/3) (FP14, FP17); (hbar c/G)^(3/2)/m_p^2 (FP17).
