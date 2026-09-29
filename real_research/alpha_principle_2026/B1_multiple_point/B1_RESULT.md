# B1 result: the Multiple Point Principle against lane Y1's Planck-scale couplings

**Bottom line.** The published MPP predictions (Bennett and Nielsen: 1/alpha at the Planck scale of about 56 for U(1)_Y, 49.5 for SU(2), 56.7 for SU(3)) lie within their own stated uncertainties of Y1's validated values (55.23, 49.20, 52.97), so the route PASSES the pre-registered 2-sigma test on all three couplings, but every pass is WEAK because the stated uncertainties are 8 to 15% of the prediction, and a flat guess of about 52 with a similar width would pass too. Under a broad declared prior the chance of all three passing at random is about 3%, so the test is not empty, but it is not sharp. The U(1) number is the authors' own and I could not recompute it, and it depends on a choice among eight printed variants (two of the eight, at 66 and 69, would fail). The route cannot give more than about 1 to 2 digits of the low-energy alpha (1/alpha(0) = 138.4 +- 8.3, i.e. 6%), and that uses the measured running from M_Z to zero energy as input, so it is a mechanism-level result and not a derivation of 1/137.035999177. Expected outcome was UNKNOWN; the outcome is a weak pass, and nothing here supports or refutes the kappa = 1/2 framework.

## Pass/fail per coupling (script `b1_mpp_confrontation.py`, output `b1_mpp_confrontation.out`, exit 0; criteria of `B1_PREREGISTRATION.md` and its Amendment 1)

| Coupling | MPP prediction (primary, authors' stated sigma) | Y1 target | z | Status | Alternative uncertainty (my propagation of the printed MC errors; U(1): viewpoint b) | Robust |
|---|---|---|---|---|---|---|
| 1/alpha_Y | 56.25 +- 4.50 (8.0%) | 55.234 | +0.23 | PASS-WEAK | 59.7 +- 3.5: z = +1.28, PASS-WEAK | yes |
| 1/alpha_2 | 49.5 +- 6.95 (14%) | 49.203 | +0.04 | PASS-WEAK | 49.5 +- 3.7: z = +0.08, PASS-WEAK | yes |
| 1/alpha_3 | 56.7 +- 8.49 (15%) | 52.971 | +0.44 | PASS-WEAK | 56.7 +- 5.6: z = +0.66, PASS-WEAK | yes |

No coupling is INFORMATIVE (none has stated uncertainty 5% or below). Using the unrounded recomputation of SU(2) and SU(3) instead of the printed values (49.78 and 58.24) changes nothing (z = +0.08, +0.62).

## Verified and unverified (full table in `B1_SOURCE_LEDGER.md`)

| Item | Status |
|---|---|
| Bennett-Nielsen hep-ph/9311321, Bennett thesis hep-ph/9607341, Bennett-Nielsen hep-ph/9607278: formulae, triple points, tables, stated uncertainties | VERIFIED (read in text) |
| SU(2) and SU(3) triple-point couplings (0.54, 2.4) and (0.8, 5.4) | VERIFIED as the authors' graphical readings of published figures; the lattice papers behind them NOT read |
| U(1) critical values (Wilson 1.0106, Villain 0.643) | VERIFIED as printed; my recalled 1.0111 not used |
| U(1) enhancement factor and continuum coupling | VERIFIED as printed; NOT recomputable by me (they rest on the authors' Monte Carlo fit and hexagonal-lattice model) |
| hep-ph/9411438 (task text), Froggatt-Nielsen 1996 as a gauge-coupling source, a separate 1995 U(1) paper | wrong id / not read / not located; not used |

## Checks worth knowing

* The papers' SU(3) table is rounded (25.45 carried as 25); an unrounded recomputation is 0.3 to 0.5 higher per group (1.5 at the Planck scale). The first script run failed this internal check and is kept as `b1_mpp_confrontation_FIRSTRUN.out` (exit 1); the check was split and disclosed in Amendment 2. The verdict did not change.
* The papers do not state what M_Planck is. Moving it by a factor 3 shifts Y1's targets by about 1.2 in 1/alpha_Y and 1/alpha_3 and 0.5 in 1/alpha_2, well under the stated MPP uncertainties.
* MUTATE control (`b1_mpp_confrontation_MUTATE.out`, exit 1 as required): replacing the U(1) weakening factor 6.5 by the naive 3 moves 1/alpha_Y to 25.6 (z = -6.6) and the route verdict to MIXED. The control fires.

## Scope caveats (these matter for reading the pass)

1. **Zero-knob only conditionally.** The authors' choices are fixed by their papers, but the model premises (a triple gauge group SMG^3 with N_gen = 3, a Planck-scale lattice regulator, a 'desert' with one Higgs) are assumptions, and in 1993 the U(1) factor 6 was introduced as phenomenologically desirable before it was given a derivation. The U(1) headline is one of eight printed variants (51.8 to 69.3), the authors' starred subset and their viewpoint a were selected in papers that compare against the extrapolated data (I cannot tell whether that selection preceded the comparison), and the SU(2)/SU(3) inputs are graphical readings with 5 to 20% errors.
2. **The test has little power.** The three Planck-scale couplings all sit near 49 to 55, so any prediction near 52 with a width near 10% passes. A pass at this width is compatible with MPP being right and with it being an accident of near-unification.
3. **Ceiling.** The best case fixes the Planck-scale couplings to 8 to 15%. The low-energy 1/alpha from this route is 138.4 +- 8.3 (the papers' own 136.8 +- 9), one leading digit and a fraction of the next; the measured value has eleven digits. The bar the campaign set (miss at or below 5e-10) is about 10^9 times beyond it. The M_Z-to-zero running is measured input (hadronic vacuum polarisation, charged-fermion masses), so even that is not a derivation. The additive boundary-shift approximation used for this line was not checked at two loops (its effect is far below the uncertainty).
4. **Independent of this programme.** MPP uses neither kappa = 1/2 nor Z; nothing here bears on those.
5. **A sharper test exists in principle.** Better triple-point Monte Carlo (the 1990s readings have 5 to 20% errors) and a modern recomputation of the U(1) enhancement could shrink the uncertainty to the 1 to 2% level, at which the test would become informative. That is a lattice-gauge-theory computation outside this lane.

alpha stays an INPUT; kappa = 1/2 FITTED; SM-mass wall unchanged, and this positive (weak) finding is a mechanism-level result with a few-percent-to-15% ceiling, not a derivation of the measured digits.
