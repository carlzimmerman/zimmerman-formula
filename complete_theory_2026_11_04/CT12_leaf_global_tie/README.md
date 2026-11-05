# CT12: leaf-global, time-local tie (a0(tau)^2 = kappa^2 c^2 G <rho_DE>_leaf inside v3s). RESULT: FAILS G0 (health, early universe), both footings

Grading lane under owner decision D1 and `../CT_GATES_COMMON.md`. Gates frozen in `FROZEN_CRITERIA.md` before any number. A go to grade, not an adoption; the 2026-11-01 retirement stands; no particle. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Not theory closed. Nothing here says the data favour the framework.

Script `ct12_leaf_tie.py` (sympy, numpy, scipy; 0.6 s, 0.11 GB, one thread) writes `ct12_leaf_tie.out` and `ct12_results.json`. The control `CT12_MUTATE=1` replaces the leaf average with the local value (CT7's C' energy portal). It then fails (d2) inside stars, with epsbar 9.95e9 (`ct12_leaf_tie_MUTATE.out`:23). That shows the grader can see a failure.

## Record check
- On record, but in the other direction (Lambda set by an average of the MOND sector): sequestering K206 (k02, five orders short), K279, K303.
- Leaf-mean subtractions are on record as constructions: L350 (STANDING.md:206) and CFG172D.
- astra's heat-field action has a whole-leaf mean-one constraint. It is astra's work and was read only.
- Not found on record: an a0 tie to the leaf average of rho_DE.
- Literature, PROVISIONAL (from memory): HT/unimodular, Kaloper-Padilla, and projectable Horava's leaf-integrated Hamiltonian constraint.

## The action
v3s with its bare Lambda removed, a minimally coupled DE sector, and

    + ∫ sqrt(-g) lambda(tau) [sigma(tau) - T^DE_nn],   a0(tau)^2 = xi G sigma(tau)

- sigma and lambda are functions of khronon time only.
- The leaf equations are:
  - sigma = <T_nn>_leaf, a lapse-weighted volume average;
  - lambda = -eps <h(x)>_leaf, with h = 2f - s f' and eps = kappa^2/8pi (`.out`:4-6).

## Gates
- **G0 health: FAIL** (`.out`:7-39).
  - (a) DOF: 4. sigma and lambda add no local and no global DOF.
  - (b) No ghost.
  - (c) CT5's band is absent. a0 does not respond to the local g, so M_L >= 1.002 (`.out`:15-16). A finite leaf moves a0 by at most 5.8e-12 (`.out`:17).
  - (d) **Reciprocity.** The DE field's gradient term becomes (1 - epsbar), with epsbar = eps <h>_leaf (`.out`:7). This is CT7's C' instability, with the local h replaced by its leaf average. The threshold is <h> = 100.53, i.e. x = 108.9 (`.out`:12).
    - Exact FRW: epsbar = 0.
    - Today: epsbar <= 2.3e-6 / 1.8e-6 (`.out`:23, 25).
    - Earlier leaves, in v3s's own cosmology: the khronon charge is the dust, and the hold flux is capped, so x >= g_lin/a0. epsbar reaches 1 at z = 8.6e3 / 1.0e4 (central) and at 7.5e4 / 9.1e4 (/10 bracket). At BBN it is 5.9e3 to 5.9e5 (`.out`:29-37).
    - The cap is reached at z ≈ 235, which matches X18's 200-500 (X18 README:158).
  - (e) W4b is inherited and still UNDECIDED.
- **G1-G3 were not graded.** UNGRADED READINGS:
  - law S deviation 1.2e-12 dex;
  - environment spread 2.5e-12 dex;
  - tracking 2.2e-5 dex, slope 0.4997 / 0.4999 in B2 / B3 (`.out`:42-47).
  - kappa^2 = xi: a TRADE.
- **G4 was not reached.**

## Causality
- a0 is set instantaneously over each leaf. Criterion B (ordering in tau) is kept.
- Criterion A (nothing faster than c) is violated in principle, as in C8. Its size is at most 5.8e-12 per order-unity change of DE in a Mpc region.
- On an infinite leaf the average needs a homogeneity prescription.

## What would reopen it (named, not graded)
- The khronon carries at most 1.8e-5 / 2.2e-5 of the dust's charge perturbation (`.out`:32, 36). That needs a dust phase the khronon does not feel (CT8/CT11), against v3s's alpha ≡ 1.
- A tie on V only: this repeats CT7's slope failure.
- A turned-off J: this fails Q2 (C4).

## Hand-set constants
xi, the tie measure, the infinite-leaf prescription, the DE sector's V0, shape and initial data, L*, mu_K, J_x's form, and the dust abundance.

kappa = 1/2 FITTED; not theory closed.
