# Adversarial self-review

2026-10-14. Primary audited claim: C3W-001, the six-mode stationary quadratic-energy theorem in PROOF.md, κ=4, B≤1/10, 13Dg²+(3/2)Dη≤1/4 on R³. **Primary verdict: proved as written.** This is self-review, not an independent author or formal proof-assistant certification. Physical propulsion completion is not the audited theorem.

## Dependency graph

Specified covariant action → unchanged target solution → unitary metric variables with four auxiliary fields → exact joint positive form → unique global auxiliary solution → reduced kinetic lower bound. In parallel: flat spatial-curvature Fourier bound + full normalized-Θ static expansion + inverse-source norm bound + elastic gradient/mass → negative static trial form → Schur restoring lower bound. The quadratic Legendre transform then gives the stated energy estimate and stationarity gives conservation for smooth finite-energy solutions.

The radial bump derivative bounds + exact normal Ricci decomposition give an explicit spherical family satisfying the theorem hypotheses. These are analytic implications, not an extrapolation from finite modes. The 3D matrix audit and local-jet computations are separate checks of the action expansions and constants.

## Obligation matrix

| Obligation | Status | Evidence and exact scope |
|---|---|---|
| Same background after κ change | Passed | Added derivative square has C=∂C=0 for arbitrary b; zero first variation |
| Θ versus old projected Q | Passed | Proof uses normalized Θ directly; no planar-only transfer in spherical theorem |
| Nonzero bz and all metric components | Passed | Exact general 3D joint completion; nonzero-trace nonlinear static jets; independent 3D operator |
| Source/strain cancellation | Passed | General normal-frame H coefficients cancel at Q=0; no small-H assumption in kinetic step |
| Auxiliary coercivity and existence | Passed | Positive mass and gradient form; sym-gradient identity; bounded forcing; Hilbert minimization |
| Static trial → physical restoring energy | Passed | Positive auxiliary Hessian makes reduced static Lagrangian no larger; sign checked against independent matrices |
| All wavelengths/directions | Passed | Fourier symbol bound for spatial curvature, universal norm inequalities elsewhere; no finite spectral cutoff |
| Pointwise versus integrated spatial bound | Passed | The 1/8 curvature bound is used only after Fourier integration, not asserted for arbitrary independent spatial jets |
| Numerical constants | Passed | Rational certificates, source/Frobenius bounds, C∞ radial derivatives and explicit R,V arithmetic |
| Conserved energy versus nonlinear evolution | Restricted as stated | Only stationary quadratic energy and smooth finite-energy linear solutions; no nonlinear or full existence theorem claimed |
| Six-mode continuum operator audit | Passed in finite range | Three complete 3D periodic controls, 27 modes, exact-degree quadrature with binary64 error |
| One-action stationary controller family | Passed | Explicit current divergence cancels inverse-source Λ equation; target metric/Φ variations vanish |
| Mixed seven-mode controller energy | Analytic sufficient criterion | Coefficient-array/constant-family argument and finite norm criterion; no expanded numerical Cmix or independent seven-mode matrix check |
| Optical pump | Passed as a postulated interaction | Positive clock-frame Maxwell Hamiltonian, matched controller/EM work; stationary optical shift condition separately stated |
| Capacity energy example | Conditional model estimate | Applies to explicit strong sufficient Fc choice and quadratic controller offset, not a universal or measured fuel cost |
| Finite energy launch and payload backreaction | Not addressed by theorem | No solved trajectory for the complete pumped system |
| Physical carrier and vacuum interface | Not established | Assigned negative background stress and hypothetical couplings persist |
| Literal ordinary-vacuum interpretation | Fails | κ4 tensor speed below sqrt(3/5)c conflicts with primary GW170817 near-light tensor-wave propagation; localized-phase use requires new matching |

## Checks against likely false interpretations

The old κ=1 finite-wall tests do not prove this κ=4 continuum result; the κ change is explicit. The proof does not extend to V near c, arbitrarily thin walls or a controller changing globally at zero cost. The background's negative normal energy remains negative even though the quadratic excitation Hamiltonian is positive. The quadratic energy is not the total nonlinear fuel energy or the GR ADM integral. A physical craft is absent from the exact source.

The optical operator changes only the electromagnetic quadratic block at zero field; operating pump stress enters beyond that background. ε>0 ensures clock-frame optical energy; positive stationary energy also requires the stated flow/phase-speed condition, automatic for the chosen cabin window. A pure F² dilaton coupling would vanish for a plane wave; the specified clock-electric coupling avoids that false inference.

## Remaining program, not theorem gaps

The main still-unproved physical implication is a localized, finite-energy launch solution in the fixed controller/pump theory with craft stress and outgoing momentum accounted for. A numerical stiffness/response analysis for the mixed controller, causal constraint behavior, nonlinear stability, microscopic material realization and the model-specific large activation cost also remain. No source novelty or priority claim has been checked or made.

The initial geometry run failed because a zero Matrix was compared to scalar zero. Its script, contract and traceback are preserved. V2 fixes matrix-zero handling and replaces a redundant source-identity assertion with a nontrivial momentum component check. It does not conceal a scientific counterexample.
