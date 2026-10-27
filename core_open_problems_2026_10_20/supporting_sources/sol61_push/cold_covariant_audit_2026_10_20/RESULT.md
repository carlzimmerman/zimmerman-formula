# New canonical-action arrival: a tensor counterexample and a separate binding obstruction

**Primary audit verdict: refuted, with a homogeneous-shear counterexample, for CFG938's stated structural claim c_T=c.** The adopted tidal stiffness changes the tensor kinetic coefficient on its own homogeneous expanding background. With the declared medium abundance already present at the quoted early-universe epoch, that coefficient is negative. This conclusion applies to the displayed action and background assumptions. It is not an exclusion of other actions, late medium production or an unspecified completion.

A proposed operator change cancels this particular tensor correction while preserving the static limit. Its complete coupled stability and dynamical consistency are untested. It leaves the canonical medium's Newtonian self-attraction cancellation unchanged, so it does not itself produce dwarf cores or a four-galaxy selector.

## Source identity and what Claude established

CFG938 criteria are `7a0d41e8b6e3cc12b09326a236dcc39a0f9f3558`; finalized derivation, code and results are `92606e049be780aa6ac7d57de60d97e2324c74b3`; the ledger arrival is `a947836f7f6b47d6b6e325092b9e207b11b87cf7`. Exact committed-byte receipts are in `formation/sources_cfg938.json` and `numerical/CFG938_NUMERICAL_AUDIT_v2.json`. The latter checks 15 source/dependency identities and 48 saved arithmetic/provenance obligations. The first audit's use of rounded footings is preserved as a failed precision attempt; the corrected audit reads the pinned full FP0 values.

The reported main 30 checks, K3 and MUTATE6 checks reproduce as saved. The retained first run has 28 checks with S3e false, despite printing a conditional class. Claude's recorded final lane class is COVARIANT PARENT CONDITIONAL. This audit preserves that historical classification and separately challenges the stated covariant claims. Its useful advances include an explicit continuum action, static stress/accounting, a homogeneous dust background and a conditional static-rest-frame dispersion calculation. The early failed gradient-flow run and post hoc disclosures remain visible. Its slip maximum 1.53979990379e-5 is a declared law-profile estimate, not a solved full finite-stiffness covariant equilibrium or four-dwarf likelihood.

The present audit does not rerun that lane or rewrite its frozen classification. It tests the separate A5 assertion in DERIVATION §8 and the scope of the expanding-background claims. The static checks do not compute this tensor sector.

## Displayed action and precise claim card

Use K=4piG and c=1 for the algebra. The displayed terms are

    L = R_GR/(4K) - m n - W_full(u)
        - 3 gamma tau_munu tau^munu/(4K^2)
        + lambda [h^munu nabla_mu nabla_nu chi - K m n],
    u^2 = h^munu partial_mu chi partial_nu chi,
    h^munu = g^munu + u_medium^mu u_medium^nu.

Here tau is the trace-free spatial projection of the **four-dimensional** Hessian of chi, as defined in the source. Its connection dependence matters even though no explicit curvature scalar multiplies matter. The claim being audited is that an unmodified Einstein-Hilbert term and absence of explicit curvature couplings imply c_T=c structurally. The source also treats chi/lambda as instantaneously elliptic from a flat frozen-projector check. Neither assertion follows merely from that check.

Dependencies for the tensor counterexample are the displayed action, comoving labels, homogeneous chi, the same homogeneous constraint and the Einstein dust/radiation background. No observational gravitational-wave limit, external theorem or alternative cosmological model enters its verdict.

## Exact shear derivation

Take synchronous comoving coordinates and

    g_ij = a^2 exp(2 beta_i) delta_ij,   sum_i beta_i=0,
    H_i = H + beta_dot_i,             chi=chi_bar(t).

This parametrization keeps the volume exactly a^3. Direct connection contraction gives

    D^2 chi = -3 H chi_dot,
    tau_i^j = -chi_dot beta_dot_i delta_i^j,
    tau_munu tau^munu = chi_dot^2 sum_i beta_dot_i^2.

The Ricci scalar was independently reconstructed from that metric's Christoffel symbols. Subtracting the explicit Einstein-Hilbert time boundary gives

    L_EH,shear = a^3/(4K) sum_i beta_dot_i^2,
    L_tidal,shear = -3 gamma a^3 chi_dot^2/(4K^2) sum_i beta_dot_i^2,
    Q_T = 1 - 3 gamma chi_dot^2/K.

There is no principal cancellation from the other displayed terms:

- For comoving labels, sqrt(-g)n=1 exactly, so dust supplies no shear-rate term.
- The projected gradient of homogeneous chi vanishes, so W_full supplies none.
- The multiplier density is a^3 lambda[-3H chi_dot-Kmn], exactly independent of trace-free beta. This holds even before choosing a background value of lambda.
- Scalar auxiliary adjustments do not linearly mix with a TT perturbation on an isotropic background.

Equivalently, for a small propagating TT metric perturbation,

    delta tau_ij = -a^2 chi_dot h_dot_ij^TT/2,
    S_T,principal = integral a^3/(16K)
                   [Q_T h_dot_ij^2 - a^-2 (partial_k h_ij)^2].

The added Hessian term contains metric time derivatives through Gamma^0_ij. On homogeneous chi it supplies no matching tensor spatial-gradient term. Therefore c_T^2=1/Q_T within this displayed derivative action. The exact homogeneous-shear calculation fixes the kinetic coefficient; the TT principal-gradient statement follows directly from Gamma^0_ij=partial_t g_ij/2 in synchronous coordinates.

A smallest healthy-sign counterexample is K=H=rho_c=gamma=1, rho_total=3/2 and chi_dot=-1/3. It satisfies the homogeneous constraint and Friedmann relation at an instant, has positive densities, and gives Q_T=2/3 and c_T^2=3/2. Changing gamma to4 gives Q_T=-1/3. These are algebraic counterexamples to the unrestricted structural assertion, not fitted physical benchmark values.

## Declared early-universe branch

The source's own constraint gives

    -3H chi_dot = K rho_c,
    Q_T = 1 - gamma K rho_c^2/(3H^2).

With H^2=2K rho_total/3,

    Q_T = 1 - (gamma rho_c^2/2)/rho_total        [c=1].

In SI, defining all rho as mass-equivalent densities,

    Q_T = 1 - [gamma rho_c^2/2]/[rho_total c^2],
    -3H(dchi/dt)/c^2 = K rho_c,
    Q_T = 1 - 3 gamma(dchi/dt)^2/(K c^6).

The source's hypothetical local-EoS stiffness energy, although absent from the exact adopted FRW background energy, thus reappears as this tidal action's tensor kinetic deficit. Recomputing its declared dust/radiation inputs at z=4e8 gives matter/radiation 8.516830057e-6 and:

| L* | Saved stiffness/radiation ratio | Tensor Q_T including declared matter in H |
|---|---:|---:|
|24pc|1326.4301466|-1325.4188497|
|1000pc|2302830.115636|-2302809.502990|

This is a branch-specific negative tensor kinetic coefficient with the ordinary positive Einstein spatial-gradient term. It defeats the inference that making the background stiffness vanish automatically removes the early-universe problem. A different formation epoch, background, density-dependent coefficient or changed operator requires a fresh analysis. No numerical bound on those alternatives is supplied here.

`tensor/run_001/` is a bounded new symbolic/arithmetic audit with 26 passing controls, a validated v2 manifest and measured RSS 54.4MB. It uses exact copied source bytes and does not execute Claude's code. A first invocation was rejected before execution because the relative contract path had the wrong cwd; `tensor/launch_attempt_001.json` preserves it. Source/contract and scientific criteria did not change for the successful invocation. The analytic derivation, rather than the count of checks, supplies the counterexample.

## A narrowly tested operator change

Let sigma_munu be the medium's projected symmetric trace-free velocity gradient and dot_chi=u_medium^alpha partial_alpha chi. Consider the **new** family

    tau^(alpha)_munu = tau_munu + alpha dot_chi sigma_munu.

On homogeneous shear, sigma_i^j=beta_dot_i delta_i^j, hence

    Q_T(alpha) = 1 - 3 gamma chi_dot^2(1-alpha)^2/K.

Within this family alpha=1 removes this tensor kinetic correction. For a static medium and static chi, both sigma and dot_chi vanish; the new cross/correction terms and their first variation vanish, preserving the original static S2 equations in that sector. These identities are checked exactly. The choice is an operator proposal, not a derived microscopic mechanism or an adopted theory change.

It also introduces medium velocity-gradient couplings. In the restricted fixed-metric longitudinal calculation with C=dot_chi and frozen Poisson elimination, the velocity-squared coefficient is

    L_(v^2) = 1/2 [rho-C^2/K-gamma alpha^2 C^2 k^2/K^2] |v|^2.

The negative high-k contribution is a warning, not a ghost verdict for the full constrained theory: the frozen sub-block has not eliminated the actual FRW metric/projector/chi/lambda constraints. Whether a crossing is inside a justified EFT range is also unestablished. Its full scalar/vector/metric/chi/lambda constraint system, possible extra modes, high-k kinetic signs, background evolution and nonlinear well-posedness have not been eliminated or proven. The flat-projector static tests cannot be reused as a pass for it. See `formation/REPAIR_SCOPE.md` for the restricted diagnostic and remaining obligation. Full coupled quadratic reduction is the next test before claiming a viable repair.

## The separate cold-core binding obstruction

The source's reported loss of Newtonian self-gravity is structural in the static longitudinal action. Since

    W_full(u) = u^2/(2K) + W_rem(u),

using an unaveraged Fourier-mode normalization, eliminating the two Newtonian potentials for baryon amplitude B and two tethered-medium amplitudes C1,C2 yields

    L_eff,quadratic = K[(B+C1+C2)^2-(C1+C2)^2]/(2k^2)
                    = K[B^2+2B(C1+C2)]/(2k^2).

CFG938 S8 instead uses phase-averaged real cosine amplitudes, giving half this expression, K[B^2+2B(C1+C2)]/(4k^2). That normalization difference changes no force-cancellation conclusion. The cold-cold Newtonian attraction cancels, including its host/satellite cross term. The residual nonlinear R(u) interaction remains, so this is not an absence of all interaction. The saved two-component Newtonian growth reduction gives p=.609544717456 for delta proportional to a^p under its declared post-recombination approximation. A full perturbation calculation of the covariant expanding action is still missing; that static/Newtonian growth result cannot validate it.

The spherical static equation is R(u)=g_b+gamma rho_c', with R(u)=u^2/(a0-u). For an interval with zero baryonic gravitational acceleration g_b=0, 0<u<a0 and gamma>=0, a decreasing density gives a positive outward net force R(u)-gamma rho_c'>0. It cannot be a hydrostatic decreasing core there. Positivity over the entire interval follows by u=a0*x/(1+x), x>0, which gives R=a0*x^2/(1+x)>0. The script's representative u=a0/2 sign control is only a hand-check; it is not a numerical proof over all u. This restricted corollary excludes neither baryon-bound cores, external-pressure/gravity configurations, multistream/time-dependent structures nor other matter actions.

Consequently the alternative Psi/X/chi action's self-bound fragments and merger radiation cannot be silently inserted into this canonical tethered medium. A common binding interaction, free component, gravity source, physical normalization and transition rule must be derived. The tensor-only operator change above leaves this static cancellation intact.

## CFG935/939 receiver updates

`shell/CFG939_FINAL_ARRIVAL.md` reconciles newly finalized commit `d1259e62582e09fdee0fdf33757a58f80c66c1f4` and 27 tracked files, superseding only the earlier provisional status in `shell/SHELL_AUDIT.md`. Its primary shell result remains unassigned/borderline: m5=.949087374 falls just below the frozen .95 tether line. A2 report-only runs give .958327/.956318/.994213 but have no primary class weight, and C2a values .432/.427/.517 all fail the required .9. Crossing the shells does not establish a newly decoupled, normally self-gravitating free population.

The reported 43.8% outbound positive-own-rank-energy material beyond R0 differs from the 1.35% satisfying the stricter endpoint escape predicate beyond 10R0. A candidate outbound receiver is not demonstrated 44% asymptotic escape. This distinction must remain in any dwarf mass and energy budget.

CFG935's new A1 commit `67999405006d326b5a8132212031f6c27bf91fa2` repairs a real finite-N issue: its old exact step-shell barrier has finite approach work, whereas the midpoint-in-mass discretization has an infinite barrier. Those are different finite-N Hamiltonians/domains even if they approximate the same continuum away from the singular wall. Near-wall N-convergence is still needed. Captured live935 NaN records are unusable; they were not treated as finalized physical results or rerun. The finalized939 source retains an uncounted ceiling clip, so barrier avoidance is not certified by its sampled controls.

## Consequence and exact next test

The usable new result is a concrete expanding-background counterexample, together with a narrowly checked operator route and a distinct core-binding obligation. The full theory and Draco/Sextans versus Fornax/Leo I selectivity remain open. No frozen source, criteria, publication or prior evidence was edited; no live Claude experiment was duplicated; no messages were sent to other chats or publication endpoints.

Next, derive the **full coupled quadratic action** about the declared expanding background for both original and proposed operators. Keep the medium labels, lapse/shift, chi and lambda until their constraints are actually eliminated. Check tensor, scalar and vector principal kinetic/gradient matrices, high-k limits and degree count. Only a passing consistent action should then be used for actual core formation, multistream transitions, an E/Q/J receiver or dwarf mass profiles. Additional cooling efficiency cannot repair a missing attractive binding interaction by itself.
