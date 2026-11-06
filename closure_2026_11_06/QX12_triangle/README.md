# QX12: the constraint triangle. Every sector class graded FAILS; one non-barotropic class is left, ungraded

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: COLD DARK ENERGY, no particle, no LCDM inputs.
- Criteria: FROZEN_CRITERIA.md (7a1afa9b6b), iter_3 criteria b605c9fd7c, iter_3 Amendment A1 9c7497b4cc.
- Lean: fable_independent_2026/lean_2026/QX12_triangle.lean, 5 theorems, standard axioms. The MUTATE twin fails 3/3.

## The triangle

Any extra gravitating sector must meet three conditions together:
- **T1:** cold for z > 10 (CMB peaks and lensing shape).
- **T2:** almost absent from isolated galaxies (KiDS lensing and the ellipticals).
- **T3:** present in X-COP clusters and in groups at their measured boosts.

The cosmic ratio is R = omega_d/omega_b = 5.562. Every bound is written through the exact inverse of the law,
g_N = g^2/(g + a0) (Lean `law_inverse`).

| Iter | Class | Label | Key number |
|---|---|---|---|
| 1 | Every barotropic sector in equilibrium with the sea, rho = H_t(depth) (theorem, Lean `baro_order` / `baro_nogo`) | **ALIVE** (static); no-go does not fire | X-COP sits 32-33x deeper than any galaxy when depth is measured through the total mass to turnaround; 0 violating pairs; post-result power check fires once depths overlap |
| 2 | Host-temperature step: cold above b_t = max galaxy b, at the cosmic ratio, no cluster input | **FAIL**, near miss | X-COP -0.075/0.110 (gas-trace -0.037/0.105) from the plain law's +0.47; groups over-massed by 0.1-0.3 dex |
| 3 | Isothermal sector, c_s0 fixed by galaxies (246.5 km/s) | **FAIL**, class dead for every c_s0 | X-COP best rms 0.44-0.46 anywhere on 100-6000 km/s: Boltzmann retention is all-or-nothing |
| (b) | Sound speed set by the khronon charge D.P | ARGUMENT, DEAD | D.P is the phantom density, a local function of g/a0 (AQUAL). That is QX2's universal-nu class: X-COP and SPARC share g/a0 but need different boosts |
| (c) | Decays at z ~ 1-3 except where confined | ARGUMENT, reduces to (a)/iter_2 | "Confined" needs a key that tells hosts apart. Depth is iter_1/3; temperature is iter_2 |

## What the triangle leaves (stated, not graded)

Together, iterations 2 and 3 say:
- The sector must be retained at about the cosmic ratio in clusters, which gives X-COP within 0.04-0.10 dex with no
  cluster input.
- Groups must keep less than the cosmic ratio.
- Galaxies must keep almost none.
- In each cluster the sector needs a temperature close to that cluster's own virial temperature, or its profile
  either collapses or empties.

A barotropic or isothermal fluid can't do that. A sector heated by accretion shocks to each host's virial temperature,
with an entropy floor, behaves like preheated gas: it is non-barotropic, it is retained at the cosmic share above the
floor and depleted below it. That is the one class the triangle leaves open. Its constants (the floor entropy and the
heating epoch) would have to come from the forest and galaxies before clusters are predicted. Its growth (T1 late) and
Bullet-type offsets are owed. The class was not tested here.

## Door labels

- **Clusters: FAIL** for every sector class graded (QX2, QX5, QX6, QX7, QX10, QX12 iter_2/3). The closest no-input
  result in the record is QX12 iter_2: X-COP -0.04 to -0.10 dex, rms 0.105-0.127.
- **CMB lensing / growth:** unchanged. QX12 adds static constraints only.
