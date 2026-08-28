> ⚠️ **QUARANTINED / SUPERSEDED — NOT the current candidate.** Exact-exponential kernel (μ=1−e⁻ʸ),
> eliminated by Cassini (3.76× ceiling). The frozen candidate is **SHARP-J₁₀ FC-FINAL** in
> `qwen_claude_field_theory/fc8_closure_2026/`. Do not mix the exponential branch into FC-FINAL. Historical record.

# Fable 5 master attack: exact-exponential causal nonlocal MOND

You are not allowed to declare this theory viable because a weak-field limit works. Your job is to kill it or certify it.

## 0. Freeze conventions
Use the exact definitions in THEORY.md and compare every normalization against arXiv:2512.10513v2. Do not silently replace definitions with a different nonlocal model.

## 1. Re-derive the exact MOND branch
Derive f_+(Z) from mu(y)=1-exp(-y), with Z=4y^2. Check the AQUAL primitive and all signs/factors of two.

## 2. Reconstruct a real global f(Z)
Do NOT assume the negative-Z continuation is harmless. Treat it as a separate unknown function constrained by:
- f(0)=0
- f_Z(0^+)=1/2
- sufficient regularity of the pulled-back action through the actual cosmological crossing
- suppression at large negative Z
- compatibility with the cosmological M[g] branch.

Determine whether a continuation can be C^2 or otherwise sufficiently regular in the physical crossing variable without destroying the exact positive-Z MOND law.

## 3. Solve the actual background transition
Use ds^2=-B(t,r)dt^2+A(t,r)dx.dxx with smooth interpolating A and B. Start with at least two qualitatively different profiles. Solve:
(1) the first-order phi equation;
(2) U = Box_ret^{-1}(R_uu);
(3) Z;
(4) the M transport equation.
Map the regions where time transport versus spatial transport dominates.

## 4. Exact static limit
Recover
  div[(1-exp(-|grad Psi|/a0)) grad Psi] = 4 pi G rho_b
and Phi=-Psi at the order needed for lensing.
Check arbitrary spherical density profiles, not just point masses.

## 5. Full second variation
Do not use a toy scalar block as a proxy for the theory. Obtain delta^2 S for the complete localized representation including every auxiliary/multiplier/clock field.

## 6. ADM + Dirac-Bergmann
Perform the ADM decomposition. List all canonical momenta, primary constraints, secondary constraints, tertiary constraints if any, and the full rank of the Poisson-bracket matrix. Continue until closure.

Separately impose the retarded boundary prescription. Prove, rather than assume, whether the retarded prescription is equivalent to a restriction of phase space or removes any apparent localized mode.

## 7. Physical degrees of freedom
Count first-class and second-class constraints. Identify the physical tensor/scalar/vector modes. Do not count a boundary prescription as a Dirac constraint unless the equivalence is explicitly derived.

## 8. Tensor sector
Derive the full quadratic tensor action. Verify Q_T>0 and c_T^2=1 on cosmological and bound-system backgrounds. Check terms from variations of Z and M[g], not just the zeroth-order background value.

## 9. Scalar sector
Derive the reduced scalar kinetic and gradient matrices. Check for ghosts, gradient instabilities, strong coupling, singular coefficients, and loss of hyperbolicity around Z=0.

## 10. Vector sector
Derive the vector action directly from the candidate. Do not import Einstein-aether c_V formulas. Compute the physical principal symbol from the actual metric-only nonlocal theory.

## 11. Zero crossing
Use Z=-W^2 around the cosmological crossing. Expand the COMPLETE action in W and perturbations. Determine whether f_ZZ divergences cancel, are integrable, or generate a genuine divergent quadratic coefficient.

## 12. Cosmology
Derive the FLRW background exactly. Reproduce the pressureless homogeneous component and determine the effect of the exact exponential f only where it is non-negligible.

Then derive scalar cosmological perturbations, growth, slip, lensing, and all stability coefficients.

## 13. Nonlinear transition
Numerically solve a controlled spherical transition from FLRW to a static bound object. Track M[g], Z[g], and both metric potentials continuously. Check whether a universal interpolation actually exists or depends sensitively on arbitrary initial conditions/profiles.

## 14. External-field effect
Add a long-wavelength external potential to a compact bound source. Determine whether the nonlocal functional produces an EFE with the qualitative and quantitative behavior required by MOND data.

## 15. Clusters
Test the competition between the homogeneous M branch and the inhomogeneous -f(Z) branch. Determine whether clusters naturally get the required extra gravity without spoiling galaxies.

## 16. Black holes
Only after the weak-field and full perturbation sectors are understood, test static black-hole backgrounds and regularity at horizons.

## 17. Solar-system/PPN
Compute the weak-field strong-acceleration limit and PPN deviations. Verify recovery of GR to the actual experimental bounds.

## 18. Numerical reproducibility
Every major symbolic result must have a script. Every numerical conclusion must have convergence checks and at least one independent implementation or analytic cross-check.

## 19. Final verdict
Return exactly one:
A = closed/healthy candidate;
B = rigorous no-go within the specified assumptions;
C = unresolved, with the exact obstruction and missing calculation identified.

Do not use optimistic language as a substitute for a calculation.
