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
