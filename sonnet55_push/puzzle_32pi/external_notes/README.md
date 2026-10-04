# External notes (puzzle_32pi)

Notes written outside this repo and filed here for the record. **Nothing in this directory is a
repo result.** Each is a separate author's unreviewed work; our only contribution is the check
script and the status below. Do not cite a number from an external note as a framework result.

## EXT01 -- "The 32pi puzzle: a symmetry identity, constrained vector modes, and a tested clock escape"

- File: `EXT01_gauge_vacuum_identity_and_clock_2026-10-02.md`, a verbatim, unedited copy.
  sha256 `541dcd138c77f724782909904c4f061da7cbdab272719ff04df2e85cf895f65f` (15,998 bytes).
- Provenance: written in a separate conversation workspace and handed to the owner on 2026-10-02.
  It states "standalone", self-reviewed, no repo modified. The scripts behind its "102 checks"
  (`run_all.py`) and the "previous 49-check checkpoint" were NOT supplied, so neither is reproduced here.
- Its own verdict: **the 32pi coefficient is NOT DERIVED.** It asks a narrower question: whether the
  vanishing kinetic coefficient of a proposed gauge vacuum (Blanchet-Seraille cubic convention, isotropic
  SU(2) triad) is an unreduced gauge artifact.

### What the note claims

1. For a minimally coupled `L(F)` on an isotropic triad, the Lorentz + gauge Ward identities fix the
   antisymmetric electric Hessian: `Z_E = Z_A = (rho+p) / (2(E^2+B^2))`, `Z_B = -Z_E`. So an exact
   de Sitter state (`rho+p = 0`) has `Z_A = 0` for every algebraic invariant `L(F)`.
2. In the explicit polynomial benchmark the vector kinetic coefficient `K_sigma` (after the Gauss and
   momentum constraints) is zero at `D = 0` and negative on the `D < 0` side; the homogeneous flow can
   cross `D = 0`, so restricting initial data to `D > 0` is not protected.
3. A Poynting-square term with an extra clock repairs the vector sector (`K_V = 4 lam/(1+lam)`), but the
   minimal `P(X)` clock completion has an unstable scalar principal part
   (`135 lam mu s^2 + mu(48-18 lam)s + lam(55 mu+192) = 0` has no non-negative real root for `0<lam<1`).

### What `ext01_check.py` does (25 checks, `ext01_check.out`; `MUTATE=1` -> `ext01_check_MUTATE.out`)

Independent sympy / numpy re-derivation of everything downstream of the note's *stated* inputs:

- the Ward-identity solution and `Z_E = (rho+p)/(2(E^2+B^2))` (section 1);
- the vector Schur complement `K_sigma` for both helicities, its `D -> 0` slope, its `k -> oo` limit,
  and both rows of the section-2 table (section 2);
- the Jacobian numbers (`tr = -3`, `det = 8/15`, both eigenvalues negative), the `92/45` slope, `E_b(q)`,
  and `D = 3.2251e-6` at the stated start (section 3);
- the Poynting-square Hessian `(2 lam, 2 lam, -2 lam)`, derived from the definition of `J`, and
  `K_V = 4 lam/(1+lam)` (section 4);
- the scalar determinant, which factors as `(-64 k^6 s/153)` times the note's quadratic, the roots
  `-0.2 +- 3.81964 i` at `lam = 2/3, mu = 1/10`, `Gamma/k = 1.41860`, and a 3,600-point grid with no
  non-negative real root (section 5).

Result: **25/25 pass.** Mutation control (the `48` in the claimed quadratic changed to `47`): 22/25, the
three scalar-section checks fail, exit 1, as required. One extra check (3g) is mine, not the note's: on
the slow eigendirection of the note's Jacobian, `D` carries the sign of `delta q` (`+0.95` per unit), so
the approach to the attractor is from the `D < 0` side for `delta q < 0`; the note says only that a
trajectory can cross `D = 0`.

### What is NOT checked

- The helicity velocity Lagrangian of section 2 and the three-field clock action `L_S,UV` of section 5 are
  **taken as stated**; the script verifies what follows from them, not them. An error in those derivations
  would not be caught.
- The 102-check suite, the 49-check checkpoint, the Blanchet-Seraille eq. (74) convention, any novelty or
  priority claim (the note makes none), and the gauge-flation conventions were not consulted.
- The rejection covers one clock completion (Poynting square + `P(X)`), as the note says, not all clocks.

### Reading (ours; no literature consulted)

- The identity `Z_A = (rho+p)/(2(E^2+B^2))` has the structure of the Goldstone kinetic term
  `~ -M_P^2 Hdot` in the effective field theory of inflation, so a zero on exact de Sitter is expected;
  the non-trivial content is that it survives the constraint reduction and sits next to a ghost sign.
- It does not touch `a0`, `kappa`, or the rational 4 in `G rho_Lambda = 4 a0^2`. Its section 6 says the same.
  Interaction and clock coefficients are prescribed, so it matches the campaign verdict
  (see `../README.md`): every route ends at one hand-set number. **`kappa = 1/2` stays FITTED.**

## EXT02 -- six pasted "derivations" of a0 = c^2 sqrt(Lambda/(32 pi)) (2026-10-02)

- File: `EXT02_pasted_32pi_derivations_2026-10-02.md` (chat text from an outside AI conversation, pasted by
  the owner one after another; transcribed, edits marked). Pasted Lean blocks: `ext02_lean/pasted_P*.lean`.
- **Verdict: none works. All six are one equation, `a0^2 = Lambda/(32 pi)`, restated with a new label each
  time; the label is chosen to give the target, so each reply moves the free number somewhere else.**
  Paste 6's own Lean file is an "equivalence graph" of three restatements, which says the same.

| Paste | Claimed mechanism | What fails (check id in `ext02_check.out`) |
|---|---|---|
| 1 | postulate `A Lambda = 32 pi^2`, A = "Rindler disk" | the postulate is the target; `A Lambda = C` gives `a0^2 = pi Lambda/C` for any C (1d); `pi/a0^2` is the Euclidean (tau,rho) disc, not a horizon cross-section (1c) |
| 2 | same + GHY term + Lean axiom | GHY term computed, never used (1e); the Lean axiom quantifies over all Lambda, a0 and proves `False` (Lean 1) |
| 3 | "unconditional" Lean proof + heat-kernel boundary anomaly | conditional on the premise; does not compile here; its own density never gives the claimed `4 a0^3` (1f); its stated balance gives `Lambda/(32 pi^2)`, not `Lambda/(32 pi)` (1g); `8 pi a0^2 A = 8 pi^2` has no a0 (1h) |
| 4 | spin sum rule `7N0 - 28N1/2 + 86N1 = 720` | its balance gives `a0^2 = 180 Lambda/S`, i.e. `Lambda/4` at 720 (2b); `Lambda/(32 pi)` needs S = 5760 pi, irrational (2c); SYM miscounted, "exact" solution is 716, scalar adds 7 not 4 (2d-2f); 39 integer solutions: a knob (2g); its Lean statement is FALSE (Lean 2) |
| 5 | "d = 4 is unique" | arithmetic reproduces (3a, 3b), but the postulate equates length^(d-4) to a number, so it is dimensionally consistent only at d = 4 by construction (3c, 3d); in d = 4 it is the p08 identity (3e) |
| 6 | `Vol(D2 x S2)/Vol(S4) = 16 pi` | steps right (4a), but the "fraction" is 50.3 > 1 (4b), the disc radius 5.79 R_dS exceeds pi R_dS so D2 is not inside S^4 (4c, cf. p06), `= 16 pi` is a free choice (4d) and unit-dependent as a "coupling" (4e) |

- `ext02_check.py`: 28/28 (`ext02_check.out`); `MUTATE=1` corrupts the de Sitter radius formula, 26/28, exit 1
  (`ext02_check_MUTATE.out`).
- `ext02_lean/ext02_lean_checks.lean` (repo Mathlib pin, `fable_independent_2026/lean_2026`): (1) the paste-2 axiom
  proves `False`; (2) the paste-4 theorem statement is false (counterexample Lambda = a0 = 1, N = (0,5,10));
  (3) for fairness, the algebra itself is true: a working proof of `(pi/a0^2) Lambda = 32 pi^2 -> a0 = sqrt(Lambda/(32 pi))`
  and of F1 <-> F3. Standard axioms only (except (1), which uses the pasted axiom by design). MUTATE (N = (0,5,9))
  fails. The four pasted Lean files all fail to compile in this pin (`pasted_P*.out`); P2 and P4 contain `sorry`.
- What would count as progress (the screen we apply to the next idea): the matching condition must come out of an
  action or principle that would have produced a DIFFERENT number if kappa were different; it must be dimensionally
  consistent in general d before d = 4 is set; and it must predict something besides a0. None of the six passes the
  first test. **`kappa = 1/2` stays FITTED.**

## EXT03 -- external 32pi handoff, phases 05-10 ("Euler dynamics and the quantum anomaly", 2026-10-04)

- Source: a ZIP handed to the owner on 2026-10-04 (`32pi_new_files_agent_handoff_2026-10-04.zip`,
  sha256 `d1ec538411f16cf59db338b688e6c9c37af12b989a5c7835d64f49ea1eb60ae9`, 97 files). **Not copied here**
  (it carries personal names); only the hash, this summary and our check are filed. Its own verdict on every
  page: **the target `a0 = c^2 sqrt(Lambda/(32 pi))` is NOT_DERIVED.**
- Bundle integrity: its `verify_bundle.py` passes (97 hashes); `REPRODUCE.py --phase all-continuations` reruns
  all six phases cleanly in a scratch copy (phase 10: 42 exact checks). Integrity is not correctness.

### What it claims (phase 10, the new work) and what `ext03_check.py` re-derives (17/17; `MUTATE=1` 14/17, exit 1)

| Claim | Ours |
|---|---|
| scalar-Euler action, constant-roll dS: `q = 8 alpha H^3`, `Lambda_b = 3H^2 + 160 alpha^2 H^6` | 1b, 1c from a lapse-kept minisuperspace; 1e: the a-equation is consistent. So `Lambda_b > 0` is required (1d): no self-supported dS. |
| regular star: `phi' = 16 alpha M^2/(r^5(1-2M/r))`, no monopole | 2a, 2b: falls as r^-5, not MOND's r^-1 |
| two-horizon roll `q = 8 alpha (kappa_b+kappa_c)/(r_b^2+r_c^2)` | 3a (numeric SdS, M=0.1, Lambda=0.2); 3b it is not the cosmological roll |
| anomaly dS: `rho = 3 a_E H^4/(8 pi^2)`, `H^2 = pi/(G a_E)`, `A/4G = a_E`, `Lambda A = 12 pi` | 4a-4d (bare vacuum set to zero, as the bundle says) |
| target restated: `a0^2 = 3/(32 G a_E)` | 4e: a restatement, not a prediction |
| same a_E, different c_E (11 scalars vs 1 Dirac) | 5a, 5b |

Extra check (ours, 5c): for the observed Lambda the anomaly branch needs `a_E ~ 3e122`, i.e. ~1e122 free conformal
fields; the route explains Lambda's size only by putting that number into field content.

Mutation: the Gauss-Bonnet boundary factor 8 -> 7 breaks 1b, 1c, 1e, as required.

### Not checked
Phases 05-09 (gauge vacuum, clock regulator, critical boundary, geometric bridge) beyond the bundle's own rerun;
phase 05-06 overlap EXT01. The P(X) extension, tensor diagnostic and Horndeski cross-check of phase 10 are taken as stated.

### Reading (ours)
Every equation we re-derived is right, and the bundle is honest about scope. None of it produces a0: the classical
route gives a scalar profile with the wrong fall-off (r^-5), the quantum route fixes H but not a galactic force law,
and `a0^2 = 3/(32 G a_E)` is the target in new variables. On the screen (EXT02): (1) no principle here would give a
different number if kappa differed -- FAILS; (2) dimensional consistency -- passes; (3) predicts something besides a0
-- only Lambda, and only with a_E ~ 1e122 set by hand. **`kappa = 1/2` stays FITTED.**
