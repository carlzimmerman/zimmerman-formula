# Independent gravity and synthesis review

20 October 2026. Reviewer: `/root/merger_bounds`. **Accepted within its explicitly limited classical matter-model scope.** The report is not a completed force/gravity theory, and it now states that distinction correctly. Exact reviewed report/code/result hashes are pinned in `sources_review_gravity.json`.

This review reads the synthesis and raw completed results; it does not rerun stationary or fluid experiments and does not modify their sources. Current runner-v2 records for run_001 and run_003 validate against the repository inputs. A successful manifest is provenance evidence; the formula and interpretation checks below are separate.

## Action and source choice

The new action minimally couples two complex charged scalars and one real neutral scalar to ordinary GR. It contains **no** polarization P sector. The report explicitly states that the repository's additional acceleration law is not derived or silently added. Consequently real scalar stress is counted once in this candidate, and a prediction of observed matter profiles remains required. This avoids transferring canonical ID's cancelled self-gravity into a model that actually uses Newtonian/GR attraction.

The corrected polarization dictionary is separately reproduced:

    K=4piG, u_vec=KP, u=|u_vec|,
    K W_full,u = a0u/(a0-u),
    K W_rem,u  = u^2/(a0-u),
    W_rem=W_full-u^2/(2K).

Variation of the completed square yields `div(grad Phi-KP)=K rho_b` and `grad Phi-KP=R(u) uhat-gamma laplacian P`. Those signs and factors match the independent action audit. The spherical/simple-law and negligible-stiffness qualifications are present. The Class-A exponential interpolation is correctly distinguished from the simple interpolation.

The report also correctly leaves kappa, abundance, physical parameter mapping, galaxy profiles, scalar–polarization bridge, metric response beyond minimal GR and observational closure unresolved. Minimal GR gives lensing from the **actual** stress of a solution; it does not establish that the solved static fragments produce the observed halos or an extra polarization force.

## Conserved quantities and bound

The q=1 and q=2 charges, the interaction `g(X*Psi^2+X Psi*^2)`, reciprocal equations and positive-charge convention are consistent. For signature (-+++), the stated flat equations use `Box_+=dt^2-laplacian`; the displayed Hamiltonian, energy flux and momentum density agree with that convention. Global flat E and spatial J require the stated boundary conditions and must not be imported as invariant global quantities in arbitrary evolving spacetime.

The new potential's exact rational certificate supports `V >= (17/20)^2 (|Psi|^2+4|X|^2)`. Completing the time-derivative squares then gives `E >= (17/20)|Q|` for the isolated/periodic classical flat model. This is a bound on net conserved charge, not a quantum/renormalized protection theorem, a global ground-state theorem, or the old `E>=|Q|` result. The report explicitly withdraws transfer of the old bound, scattering benchmark and pressure results. The Sturm-polynomial coefficients, cutoff and sign variations agree with run_001.

The action contains a linear parametric daughter-production channel around a **prepared** homogeneous source. That is the demonstrated sense in which production can coexist structurally with binding and a uniform floor. No nonlinear cosmological yield, seed-generation process, source abundance or final cold population has been demonstrated, and the body of the report preserves those qualifications.

## Numerical transcription

The displayed parameters exactly match run_001's inputs, including lambda=1.9900011745861654 and protected-limit remainder 1.9870635345861651. The refined Q=80000/160000 energies, frequencies, E/Q and X charge fractions match their quoted rounding. The stationary gap is 2978.7248809586163, fraction 0.019557970008913617. The reported box/tolerance energy differences are about 1.2e-11, consistent with the stated 1.3e-11 ceiling; that is a finite collocation comparison, not an a priori continuum error bound.

The corrected uniform-state values also match run_003: I=49.00650744444027, chi=-0.976461506496568, X=-0.10747017781677803, omega=0.8678983025671659, q=85.14552193768695, e=73.8976539609139 and cs^2=0.24792301922176127. The grand-potential stationarity, q=2omega(I+4b^2), P=-Omega, e=omega q-P and cs^2=q/(omega dq/domega) are consistent.

The local amplitude Hessian and compressibility support the declared local/adiabatic dense-phase candidate. They do not establish every perturbation mode, a global phase diagram, a stable cosmological dilute bath, or a cooling rate. The report says so. A stationary merger energy difference remains potential available energy, not escaped energy or measured galactic torque. The separately retained failed run_002 is not represented as success.

## Viscous transport formula and correction

For shellular rotation v_phi=r sin(theta) Omega_g(r), with isotropic dynamic shear viscosity eta(r),

    T_rphi,visc = eta r sin(theta) dOmega_g/dr,
    F_J,visc = -(8pi/3) eta r^4 dOmega_g/dr.

Integrating positive viscous heating over a spherical shell gives

    d(heating power)/dr
      = (8pi/3) eta r^4 (dOmega_g/dr)^2
      = -F_J,visc dOmega_g/dr >= 0.

The original draft mislabeled the left side `dE_heat/dr`, which has the wrong units if E means energy. The reviewed version fixes it to **heating power per radius** and explicitly notes that advective and field-stress angular fluxes are additional. This resolves the actionable finding sent during review.

These are constitutive identities under that fluid closure; they do not derive eta or establish that the fragment gas lies in a local viscous regime. Positive eta does not determine the sign of Omega_g', so an outward torque is not already proved. The synthesis preserves all of these limits.

## Interpretation boundary and next gate

The new minimal-GR matter action is a concrete alternative candidate, not an adoption of the canonical polarization action or proof that the original theory has been completed. The astronomical stock, selection, stellar-heating and torque-transfer gates remain active. The proposed next test targets actual stability and channel-resolved flux in the **same action**, with no transfer of an unrelated kernel. That is an appropriate continuation.

No further material gravity/conservation overclaim was found in the pinned reviewed version. Future edits change the review target; the source receipt should be checked rather than assuming this acceptance applies to later wording or results.
