# FC-ISO VERDICT: UNIFIED NO-GO (constraint-first 2-DOF MOND, lensing axis)

**Date:** 2026-08-28
**Verdict:** `UNIFIED-NO-GO-constraint-first-MOND`

## One line
The anisotropic constitutive Hessian of any nonlinear isotropic MOND law forces a
nonzero traceless metric stress `Sigma_P != 0` (a lensing slip `Phi != Psi`) in
**every** 2-DOF constraint construction; reaching `Phi = Psi` requires AeST-type
extra propagating structure that a pure 2-DOF constraint theory lacks.

## The theorem (basis: THEOREM, certified `fc_iso_refute.py` 37/37, exit 0)
For an isotropic MOND law `J(s)`, `s = |Dq|`, `J'(s) = mu(s) s`, the metric enters
**only** through `s = sqrt(gamma^{ij} D_i q D_j q)`. Therefore one and the same
constitutive object `mu = J'/s` controls both:

- **(a)** the MOND/AQUAL Gauss law `D_i[mu D^i q] = 4 pi G rho`, and
- **(b)** the on-shell traceless metric stress `Sigma_P`.

Two exhaustive completion classes of the constraint-first program:

- **Class A — covariant / QUMOND carrier** (incl. the committed genuine-2-DOF `sf42`
  carrier `chi|DPhi|^2`, 0 DOF): metric-variation lemma gives
  `Sigma_P^cov = -mu s^2`. Nonzero whenever the force is on (`mu != 0`) — nonzero
  **even at `mu = const`**. Closes the `sf42` open gate (ii) adversely.
- **Class B — lapse-tied second-class multiplier / 4-AC** (naive Legendre): linearity
  of the Gauss constraint in the lapse `N` forces `lambda_i = D_i N`; the tangent
  modulus returns through the Hessian `A^{ij} = mu delta^{ij} + (y mu') u^i u^j`,
  giving `Sigma_P^constr = y mu'` and slip `(mu + y mu')/mu = (y^10+2)/(y^10+1)`:
  `1` (solar) `-> 3/2` (knee) `-> 2` (deep MOND).

`Sigma_P = 0` forces `mu = 0` (no MOND) or `mu' = 0` (linear law). Hence for any
`mu' != 0` the slip is **forced**. Positivity certified for all `y > 0`; the sole
zero is the Newtonian limit `y -> infinity` (solar-system safety verified as hard as
the failure).

## Why construction fails (basis: DERIVATION, `fc_iso_construct.py` 28/28, exit 0)
No `Sigma_P = 0` completion exists in the local, action-based (Hilbert-stress),
<= 2-derivative, algebraically-reducible class. Every escape carries a computed cost:

| Mechanism | Cost | Broken premise |
|---|---|---|
| (i) compensating auxiliary field | wrong-sign (ghost) gradient, or a propagating field | N_grav = 2 |
| (ii) disformal / conformal | conformal inert; lensing-sized disformal splits photon/graviton cone vs GW170817 (2e-15) | c_T = 1 |
| (iii) det-g / trace-only coupling | no Gauss law (MOND force needs g^{ij} to raise the flux index) | MOND law itself |

## The mechanism — AeST contrast (basis: DERIVATION, `fc_iso_aest_contrast.py` 14/14; committed `typeII_direct_variation_2026.py` 44/44, exit 0)
AeST reaches `Phi = Psi` (gamma_PPN = 1, KiDS chi2/dof = 0.64) with the **same** `y mu'`
Hessian because its MOND invariant is contracted with the metric-**independent**
aether-orthogonal projector `h^{munu} = g^{munu} + A^mu A^nu` (`A` unit-timelike). This
removes the anisotropic gradient stress `d_i phi d_j phi` from the gravitational sector;
the residual Bekenstein-Milgrom curl is carried by the **propagating transverse aether
mode**. The cancelling term is `~ A^mu d_mu phi` and **vanishes as `A_mu -> 0`** — the
mechanism is intrinsically the aether's. Cancelling `Sigma_P = y mu'` requires a field
with independent traceless stress (the unit-timelike vector + its transverse mode:
4 extra propagating DOF, ledger 2 + 1 + 3 = 6). A pure 2-DOF theory has only 2 metric
polarizations plus a second-class `q` that carries **zero** traceless stress. It cannot
supply the cancellation.

## Honest residual (not over-closed)
- **C4:** a fully general symmetric-tensor Lagrange multiplier enforcing `Phi = Psi`
  directly. Certified only that the mimetic-scalar instance adds a dust DOF
  (`T_mn = 2 lambda u u`) — evidence it breaks N_grav = 2; the general tensor-multiplier
  Dirac count is NOT machine-certified. Natural next gate.
- **Non-local elliptic phantom-density (QUMOND-as-density):** `Phi = Psi` at single-metric
  2 DOF, but sourced by an isotropic density rather than a healthy Hilbert-stress action;
  causal acceptability is the committed unsettled question (`theory_2026/york` RESULT 4c).
  Genuinely OPEN — leaves the local action-based class by construction.

**Scope:** the no-go is FORCED within the local, action-based, <= 2-derivative,
algebraically-reducible class that constitutes the constraint-first program. It is a
scoped no-go, NOT an absolute all-Lagrangian impossibility theorem.

**Untouched inputs:** `a0^2 = kappa^2 c^2 G rho_Lambda` is a phenomenological TARGET;
`kappa = 1/2`, `Z ~ 21` FITTED, never derived.
