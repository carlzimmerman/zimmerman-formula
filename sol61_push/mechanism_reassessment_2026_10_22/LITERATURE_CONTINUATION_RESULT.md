# Literature boundary and a concrete continuation route

Checked 2026-10-22. This checkpoint concerns the weakly damped radial candidate in HARMONIC32_RESULT.md, not the whole theory's novelty. No new physical decay rate is established here.

## Authenticated sources and scope

**Fouvry and Prunet, Linear response theory and damped modes of stellar clusters**, arXiv:2105.01371v1 (4 May 2021), related DOI 10.1093/mnras/stab3020. Primary version: https://arxiv.org/html/2105.01371v1 . Read sections 2–3, equations (1)–(15), and the application in section 4. Their method aligns an integration coordinate with resonance frequency, expands the resulting numerator in Legendre polynomials, and applies the Landau prescription to the analytic basis integrals. Their demonstrated application is an isotropic isochrone cluster's dipole response. Numerical truncation can produce spurious structure. Authentication and method extraction are complete; application to our radial medium is **conditional**, requiring our own frequency map, measure, kernel, and convergence checks. Overlap: **partial or adjacent result only**. The general continuation technique is established, not our invention.

**Christopher Straub, Numerical experiments on stationary, oscillating, and damped spherical galaxy models**, arXiv:2405.01235v1 (2 May 2024), related DOI 10.1016/j.physd.2024.134351. Primary version: https://arxiv.org/html/2405.01235v1 . Read the model, section 4.2/Observation 4.2, and section 4.3. These are gravitational Vlasov–Poisson equilibria. Numerical observations connect oscillatory versus damped responses to orbital periods and spectral location. The cited existence criteria concern that operator; they do not establish our medium's spectrum. Authentication and extraction of the numerical comparison are complete. Direct theorem transfer is **inapplicable** without a new operator argument. Overlap: **partial or adjacent result only**. Radial collisionless oscillation and damping are already studied phenomena.

**Martin D. Weinberg, Weakly Damped Modes in Star Clusters and Galaxies**, arXiv:astro-ph/9306020v1 (22 June 1993), related DOI 10.1086/173665. https://arxiv.org/abs/astro-ph/9306020v1 . Metadata and abstract checked; full theorem/method extraction was not performed here. The abstract reports weakly damped modes in stable stellar models. This supports historical attribution only; project application is **unverified**. Overlap: **partial or adjacent result only**.

No full texts were retained locally; cache hash and cached extraction are not requested. These are primary web reads, not cached-source verification. SciSpace supplied discovery candidates, not proof. Its duplicate repository dates were not substituted for primary version dates.

## Project-specific derivation: use the absorption matrix as a spectral density

This paragraph is our algebraic translation of the existing response, not a result attributed to the papers. Write u=L², s=n Omega_r(E,u)>0, and C_n for the vector of potential Fourier coefficients. The action measure is dGamma=pi T_r du dE and f_E=-F inside the occupied domain. Our existing upper-half-plane response is

    Pi(z) = F pi sum_n integral du dE T_r 2s² C_n C_n^T/(z²-s²).

Partition each fixed-u energy interval into monotone frequency branches. On regular branches with nonzero Omega_E, define

    W_n(s) = 2 pi² F integral du sum_{E: n Omega_r=s}
                         C_n C_n^T / |Omega_E|,
    W(s) = sum_n W_n(s).

Then changing variables on each branch and using T_r=2pi/Omega_r gives

    Pi(z) = integral_0^infinity W(s) [1/(z-s)-1/(z+s)] ds.

The positive-frequency boundary value obeys -Im Pi(omega+i0)=pi W(omega). Thus the existing direct resonant matrices B(omega) already sample **pi times the required spectral density**. They are more than an isolated linewidth diagnostic: they provide the numerator for a controlled continuation calculation. The cancellation of the harmonic number in W_n follows from the Jacobian dE=ds/(n|Omega_E|); harmonic dependence remains in the roots and coefficients.

Near a positive regular frequency, if W has an analytic local extension and no intervening endpoint or critical-frequency singularity, the retarded continuation below the axis is

    Pi_L(z) = Pi_direct_lower(z) - 2 pi i W(z).

This sign follows from our denominator z-s: its upper boundary is PV minus i pi W, whereas the direct lower integral has PV plus i pi W. The negative-frequency cut is separate from this local positive-frequency crossing. The mode equation remains det[S-Pi_L(z)]=0. Substituting a negative imaginary part into the finite action-quadrature sum alone does not perform this continuation.

## What must be done before claiming a pole

1. Map frequency support and critical points for every retained harmonic. Split monotone branches and handle tangencies/endpoints explicitly; PCHIP root brackets are not a completeness proof.
2. Evaluate W on a frequency mesh, preserving the matrix structure. Check pi W against the independently calculated B and reconstruct upper-half-plane Pi against existing action quadrature.
3. Approximate W on regular intervals with an analytic representation, checking order and interval sensitivity. Compact occupation support and orbit-boundary changes can introduce nonanalytic structure; a global polynomial fit must not silently erase it.
4. Solve the continued matrix equation near .822797-i6.8e-5, varying spectral representation, field basis, orbital harmonics, and action integration. Verify a pole residual and stability, rather than fitting three boundary eigenvalues again.

This is an implementation route, not an executed or validated continued-pole calculation. The algebra was checked against kinetic_weight.py and resonant_h32.py, including the response sign and 2pi³F absorption normalization. No new numerical experiment was run for this checkpoint.

## Novelty and physical interpretation

The generic mechanism of collisionless resonant transfer and weakly damped collective motion cannot be claimed as new. What remains potentially distinctive is this particular medium's self-consistent radial response, harmonic coupling and occupation dependence; its novelty is **unestablished**. The present evidence may diagnose why the near-law cold branch settles slowly. It does not select that branch, create the required fine-grained occupation, derive kappa, or complete the dynamical parent.

Search scope: SciSpace and web discovery, English astrophysics/kinetic theory, checked on 2026-10-22; queries included “Weinberg weakly damped modes spherical stellar systems 1994”, “spherically symmetric Vlasov Poisson oscillations damping polytropic steady states radial modes”, and the exact Fouvry–Prunet title. A same-searcher second strategy searched radial polytrope dynamics rather than dipole response. Fouvry–Prunet's backward discussion of Weinberg was inspected, but no systematic forward-citation audit was completed. Plasma literature, all modified-gravity antecedents and unpublished work were not exhaustively covered. No “apparently new” or global-priority claim follows from this bounded search.
