# Physical state required by the cold mass interpretation

The current equations do not identify a unique substance. Under their real-mass interpretation, they require a gravitating medium with a dynamically selected distribution of energy and orbital motion. A massive interacting field with occupied excited modes is a concrete candidate. The present evidence does not distinguish that carrier from a particle description with the same stress and transport. Calling it a field, condensate, or cold energy does not yet explain the formula.

This continuation starts from `65fa05a07`, after the counter-transport study `b0f40dd56`. Scope: analytic support constraints and a read-only audit of the Bose relaxation calculation. No changes to Claude's source lanes, no claim of a completed theory, and no new observation.

There are two substantive findings: a stationary single-mode condensate cannot support the ideal deep-law profile through its usual quantum-pressure term, and CFG428's quantitative thermal rejection contains a factor-1000 unit error. The latter weakens that particular rejection but leaves its declared window outside its own 13.8 Gyr cutoff.

For a spherical outer halo in the ideal deep limit, define

\[
V_f^4=GM_ba_0,\qquad
\rho_c=\frac{V_f^2}{4\pi G r^2},\qquad g=\frac{V_f^2}{r}.
\]

Hydrostatic balance for isotropic pressure gives

\[
\frac{dp}{d\rho_c}\frac{-2\rho_c}{r}
=-\rho_c\frac{V_f^2}{r}
\quad\Rightarrow\quad
\frac{dp}{d\rho_c}=\frac{V_f^2}{2}.
\]

If two baryonic masses share a density interval, a single universal barotrope p(rho) cannot meet both requirements: the derivative at the same density would differ. A halo-dependent entropy, velocity distribution, anisotropic stress, or further state variable can evade this restricted obstruction. This is established project ground: [CFG44](../../campaign_fresh_gravity/CFG44_fluid_target/README.md) and [CFG472](../../campaign_fresh_gravity/CFG472_settling_force_l2/README.md) already contain the barotropic and isothermal constraints. The 1/2 here is a hydrostatic ratio of squared speeds; it does not derive kappa in the cosmological acceleration formula.

For the exponential kernel written in THEORY_v1 and explicitly used by CFG541/556, with point baryons, q = r_M/r and r_M = sqrt(G M_b/a0),

\[
\rho_c=\frac{M_b}{4\pi r_M^3}\frac{q^4}{4\sinh^2(q/2)},\qquad
\frac{d\ln\rho_c}{d\ln r}=-4+q\coth(q/2).
\]

For q >= 4 the density increases outward. Hydrostatic support then requires negative dp/drho, excluding a stable positive-compressibility barotrope on that region. This is a point-baryon, exact-profile condition, not an exclusion of extended baryons or approximate observed rotation curves. A positive distribution derived for a different interpolation kernel cannot be imported without rechecking it.

A coherent nonrelativistic field has the Madelung potential per unit mass

\[
Q=-\frac{\hbar^2}{2m^2}\frac{\nabla^2\sqrt{\rho_c}}{\sqrt{\rho_c}}.
\]

On an exact r-to-the-minus-two annulus, sqrt(rho_c) is proportional to 1/r, and the spherical Laplacian of 1/r vanishes away from the origin. Therefore Q = 0 there. A stationary field with no bulk flow has no quantum-pressure support against the nonzero gravitational force. A stationary spherical through-flow does not fix this: continuity makes r^2 rho v constant, hence v constant, so v dv/dr also vanishes. A quartic contact interaction supplies p proportional to rho^2 and an acceleration proportional to r^-3; it cannot balance an r^-1 force over an extended exact annulus.

For the exponential kernel's outer expansion, the quantum term is instead Q = hbar^2 r_M^2/(8 m^2 r^4) + O(r^-6); its force falls as r^-5. It remains asymptotically too steep. These are constraints on the stated stationary, spherical, single-mode description. Incoherent mode populations, angular structure, time dependence and other interactions remain outside them. A symbolic differentiation independently checks the zero-Laplacian identity and the expansion coefficient.

**Kernel clarification added after efe91e23b:** the earlier wording called this exponential formula nu_mono, following THEORY_v1. The legacy function bearing that name in CFG4_common is a different, monotone-repaired interpolation. The formulas above remain correct for the explicitly specified exponential kernel, including recent CFG541/556. They must not be transferred to every lane using the name nu_mono. [The kinetic support gate](KINETIC_GATE.md) identifies the source definitions and proves why the distinction matters. It also strengthens the hollow obstruction: an arbitrary nonthermal isotropic f(E) does not escape it.

The useful candidate is therefore a field in an excited kinetic state, whose stresses and energy transport are computed from its occupied modes and interactions. This can in principle carry the energy needed by the previous outer-envelope proposal. It has not been shown to select the RAR profile. Even ordinary energy-conserving collisions allow a family of equilibrium temperatures; a relaxation rate alone cannot set the required galaxy-dependent normalization.

The numerical audit changes one premise used to dismiss that candidate. [CFG428 line 9](../../campaign_fresh_gravity/CFG428_one_bose_field_ledger/cfg428_ledger.py) uses 1e-4 m^2/kg for 1 cm^2/g. The correct conversion is (1e-2 m)^2/(1e-3 kg) = 0.1 m^2/kg. Under its own unchanged density, velocity, occupation factor and cross-section ceiling:

| Mass in eV/c^2 | Original relaxation time in Gyr | Corrected time in Gyr |
| --- | --- | --- |
| 0.62 | 14120 | 14.12 |
| 0.81 | 37011 | 37.01 |
| 1.04 | 79692 | 79.69 |

The lightest node still exceeds 13.8 Gyr, by 2.3%. The same rate is monotone increasing with mass at fixed other inputs, so the continuous interval [0.62, 1.04] also misses that threshold. The analytic boundary is 0.6162412353 eV/c^2. The lower endpoint is a calibrated cluster bracket, not a universal particle-mass bound; even its unrounded value, 0.6191343270, remains above the boundary. What fails is the claimed thousands-fold margin, not the sign of the frozen thermal verdict. The quantum-depletion cross sections also need the factor-1000 conversion correction and remain catastrophically above the adopted bound. The audit retains the old rate approximation and cross-section ceiling; it does not establish that either is a current physical constraint. [CFG384](../../campaign_fresh_gravity/CFG384_self_interacting_bose/README.md) had already described self-interaction as marginal.

The [audit code](thermal_audit.py), [contract](thermal_contract.json) and [results](thermal_results.json) preserve the exact source hashes, original constants, independent unit paths and deliberately wrong conversion check. All 18 checks pass. This verifies the arithmetic correction and its scope, not the microscopic rate law. The depletion and thermal routes are alternatives under CFG428's declared criteria; no claim combines their failures into a universal field exclusion.

There is a physical discriminator to develop, rather than just another profile fit. In the audited approximation,

\[
\Gamma=\rho_c\frac{\sigma_{\rm scat}}m\,v(1+\mathcal N),\qquad
\mathcal N\propto\frac{\rho_c}{m^4v^3}.
\]

At fixed particle mass and constant cross section per mass, the highly occupied limit gives Gamma proportional to rho_c^2/v^2, whereas dilute classical scattering gives Gamma proportional to rho_c v. Bose-enhanced rates of this form are established estimates; see [Berezhiani and Khoury, section 2](https://arxiv.org/html/1507.01019v2#S2). The numerical normalization and validity must come from the actual collision operator. Velocity-dependent scattering and differing assembly histories can mimic parts of this contrast.

The next discriminating computation is to derive that operator for a declared field action, evolve its energy and orbital occupations, and test whether one common interaction predicts the density and velocity dependence of settling without inserting the target profile. A suggested age trend alone is insufficient: CFG585's frozen result is NOT CONFIRMED, with Z = 1.51. Subsequent CFG586 finds that its measured companion-count correction does not remove the secondary K9 signal (Z = 2.69); this weakens that specific contamination explanation. The K9 band followed an earlier post-hoc choice, the original band remains Z = 1.51, and colour, stellar populations and unmeasured environmental differences still limit an interpretation as a measured settling clock.

The second missing ingredient is the dark-energy connection. In [CFG288](../../campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md), adding a constant vacuum energy to a massive-field potential does not change its local field derivative or select the cold abundance. A successful theory must supply an actual coupling or dynamical boundary condition that selects a0; sharing one field name does not do it. Neither the corrected thermal calculation nor the support identities derive kappa, the abundance, the interpolation kernel, or the 32 pi squared coefficient.
