# Fifty concrete next research steps

Requested 2026-10-08. These are prospective tasks, not fifty completed results or a claim that the theory is almost finished. The current evidence is in REPORT.md. Prioritize steps 1–5, 21–25 and 31–35: failures there can invalidate entire downstream programs. A failed test is useful evidence; it must not be replaced by parameter fitting without being recorded.

## Mathematical completion

1. **Finite-source existence.** Prove existence of a positive weak minimizer on a finite ball with specified outer data, or exhibit a source for which it fails.
2. **Central zero-field point.** Derive the full admissible central expansions and energy domain; determine whether the kinetic form admits a unique evolution through \(F=0\).
3. **Infinite-domain matching.** Construct the decaying exterior solution without an imposed finite-radius P2 endpoint and bound the truncation error.
4. **Linear evolution.** Establish a well-posed initial-boundary value problem for constrained perturbations; positive energy alone is insufficient.
5. **Nonlinear stability.** Turn the local Hessian bound into a nonlinear stability theorem on an annulus, explicitly specifying norm and boundary conditions.
6. **Relative energy at infinity.** Define a finite relative energy for logarithmic MOND potentials and identify the allowed perturbation class.
7. **Source-profile universality.** Repeat matching for several monotone compact densities; separate universal suppression from profile-dependent amplitudes.
8. **Nonmonotone sources.** Determine whether shells or density bumps reverse the correction sign, with an explicit counterexample or sign theorem.
9. **Angular deformation.** Solve a small quadrupolar deformation of the spherical source and compare it with the constrained energy prediction.
10. **Certified numerical error.** Bound discretization, domain and nonlinear-solver errors separately for one reference source solution.

## Observable consequences

11. **Restore physical units.** Produce a complete units dictionary for \(h,Z,a_0,\kappa,F\) and the source radius before interpreting numerical parameters.
12. **Recovery-radius bound.** Derive a radius beyond which the force differs from P2 by less than a declared tolerance, including the matching amplitude.
13. **Mass scaling.** Test the predicted \(M^{1/6}\) decay length across masses while holding the same physical \(\kappa\).
14. **Surface-density dependence.** Quantify the force correction when mass is fixed and source size changes; identify an observable discriminator.
15. **Thin-disc calculation.** Solve the field equation for a resolved disc with controlled thickness; do not apply the spherical algebraic law to it.
16. **External field.** Derive the response to a uniform external acceleration and compare it with the isolated solution.
17. **Rotation-curve likelihood.** Predefine data selection, nuisance parameters and a baseline P2 likelihood before estimating any gradient coefficient.
18. **Cross-system coefficient.** Test whether one \(\kappa\), rather than a separate value for every system, describes the selected systems.
19. **High-acceleration tests.** Translate the known Newtonian gradient limit into bounds using current primary experimental sources.
20. **Discriminating forecast.** Identify a measurement that separates this completion from ordinary AQUAL/P2 even when their asymptotic mass law agrees.

## Physical origin and consistency

21. **Lower-operator obstruction.** Identify all symmetry-allowed \(q\) and \(q^2\) terms and quantify how small they must be over the desired acceleration range.
22. **Canonical gradient obstruction.** Calculate how an allowed \(|\mathcal D_i\Psi|^2\) term competes with flux stiffness; determine the tolerance before the mass offset returns.
23. **Protecting symmetry.** Propose an explicit symmetry that removes those dangerous operators and verify every term of the action under it.
24. **Radiative stability.** In a specified regulator and approximation, test whether the proposed symmetry actually prevents their regeneration.
25. **Microscopic derivation.** Derive the flux-gradient operator from a concrete underlying model or record that it remains a phenomenological choice.
26. **Derivative expansion.** Identify the cutoff and compare omitted operators with the retained term on the matched solution.
27. **Gauge interpretation.** Determine whether the auxiliary U(1) bundle has physical content or merely represents the three-component field redundantly.
28. **Conservation laws.** Derive energy, momentum and angular-momentum currents with matter included; verify boundary contributions.
29. **Dynamical baryons.** Couple a specified fluid or particle source and analyze joint matter-field modes; fixed-source stability does not answer this.
30. **Constraint Hamiltonian.** Count physical degrees of freedom and check the constraint algebra before proposing a relativistic extension.

## Vacuum normalization and the \(32\pi^2\) target

31. **Exact target convention.** Freeze the physical versus geometric acceleration, vacuum mass density and area definitions so the desired ratio is unambiguous.
32. **Stress-energy derivation.** Derive the vacuum stress tensor from an explicitly metric-dependent action; a constant in a Newtonian functional is not sufficient.
33. **Independent vacuum parameter.** Determine whether an additive vacuum counterterm is allowed; if so, prove or acknowledge the resulting normalization freedom.
34. **Coupling-selection equation.** Obtain an independent equation fixing \(h^3/\lambda_6\), without inserting the desired \(a_0\) relation into a boundary condition.
35. **Countermodel test.** Vary the vacuum term while preserving local halo equations; any surviving family defeats a claimed coefficient derivation.
36. **Cosmological background.** Solve the homogeneous equations of the chosen relativistic parent and establish whether a stable de Sitter solution exists.
37. **Local-to-cosmic matching.** Derive the acceleration scale of a localized source on that same background rather than equating unrelated scales.
38. **Branch selection.** Determine which cosmological branch is dynamically reached and whether its coefficient is unique.
39. **Perturbation health.** Check scalar, vector and tensor kinetic/gradient signs on the selected cosmological background.
40. **Robustness of \(32\pi^2\).** Test whether the coefficient survives allowed counterterms, field redefinitions and unit conventions; otherwise classify it as a tuned value.

## Audit and release

41. **Primary-source overlap.** Expand the literature comparison around AQUAL, mixed flux actions, gradient gravity and MOND effective theories.
42. **Independent reconstruction.** Have an authorized independent reviewer derive the source current and Hessian without seeing the author's conclusions.
43. **Constraint audit.** Check the passage from unconstrained vector positivity to scalar-potential perturbations, including boundaries and zero-field exclusions.
44. **Source theorem audit.** Verify every regularity hypothesis in the maximum-principle suppression theorem and test a case outside each one.
45. **Reproducible reference case.** Package one dimensionful source example with pinned dependencies, inputs, output hashes and an independent implementation.
46. **Data provenance.** Record licenses, source versions, exclusions and parameter priors for every observational dataset actually used.
47. **Claim separation.** Maintain separate lists of proved identities, conditional theorems, numerical evidence, model choices and unresolved physical claims.
48. **Short technical manuscript.** Write a bounded paper on the flux completion, source suppression and coercivity result, without claiming a completed gravity theory.
49. **Adversarial replication.** Reproduce the strongest claimed observational and theoretical results using a different implementation and explicit negative controls.
50. **Completion decision.** Assess the original formula and vacuum target against predefined criteria; publish a success claim only for obligations actually closed, and preserve a precise failure or partial-result report otherwise.

## Immediate handoff

Current strongest addition: at an aligned matched spherical background, the unconstrained flux Hessian has lower bound \(5/(3\sqrt3)\), so the physical constrained second variation is positive for perturbations supported away from zero-field points. The model still requires a chosen spatial term and critical tuning. Begin with central regularity and a controlled evolution problem, alongside the symmetry/counterterm obstruction; these are more informative than generating additional numerical matches.
