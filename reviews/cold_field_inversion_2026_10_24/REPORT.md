# Cluster excess through the framework's field equations

No parameter-free cold-sector dynamics has been found that predicts these cluster profiles and preserves the galaxy law. The new result is more restrictive than the preceding empirical mass-equivalent comparison: the literal khronon encounters its finite-response cap or an outward force; the static mass-term alternative fails a potential-zero-independent test; and an independent positive AQUAL source cannot reproduce several of the central outer-profile shell differences exactly.

These are conditional results for the stated spherical limits and published central mass profiles. They are not a universal exclusion of extra fields, time-dependent solutions, arbitrary screening, or data within full correlated uncertainties. Kappa=1/2 remains FITTED. The existing canonical and alternative a0 values are inputs, not predictions of this calculation.

## 1. Equation selection and source bookkeeping

The repository contains both exploratory scalar EFTs and a specified v3s khronon action. We use the latter's weak-field equations in `covariant_push_2026_10_22/V3_FULL_PICTURE.md`, and its parameter bounds in `V3S_FINAL_VERDICT_2026-10-24.md`. The earlier cubic-coefficient audits do not provide a separately closed cold-source equation.

Let g=Phi' be the physical acceleration magnitude, gb=GMb/r², Xi the khronon potential, and psi=Phi-Xi. In the spherical, negligible-stiffness limit:

    div grad Phi = 4 pi G (rho_b + rho_tau)
    4 pi G rho_tau = div[(1-mu(|grad Xi|/a0)) grad Xi] - mu_K² Xi
    D_t v_tau = -grad(Phi-Xi)
    mu(x) = x/(1+x).

The native cold density includes the response that produces the galaxy law. It cannot be counted once as that response and again as an independent extra source.

The unscreened parent equations and static limit are described in [Blanchet–Skordis 2404.06584v2](https://arxiv.org/html/2404.06584v2), sections 3.2.2–3.2.6. The particular mu, switched stiffness and galaxy bound used here are the repository's choices, not a claim that the paper uniquely fixes them. The additional mass inversion below is our derivation.

Inputs: the same seven X-COP systems and six radii from 0.1 to 1 R500 as the committed matched comparison. Re-reading raw FITS reproduces all 42 stored cluster rows. All quantities inherit photometric stellar masses, hydrostatic mass estimates, spherical enclosed-mass gravity and the raw data's distance conventions. No new a0, concentration, temperature, cold abundance or per-object normalization is fitted.

## 2. Literal cold field: the cap and force have to be satisfied together

First set mu_K=0 and neglect the existing stiffness term on these scales. Impose regular spherical flux, without a singular central integration charge. Poisson fixes the total native field mass:

    M_tau(<r) = (g-gb) r²/G.

Set u=GM_tau/r²=g-gb. The hold equation then requires

    u = a0 Xi'/(a0+Xi'),       0 <= u < a0
    Xi' = a0 u/(a0-u)
    psi' = g-Xi' = gb-u²/(a0-u).

The first equality is on the outward-Xi branch; a negative Xi' gives negative u and cannot repair a positive required mass. At u=a0 the gradient diverges, and u>a0 has no finite allowed branch. Stationary cold dust at rest needs psi'=0. This gives exactly the baryon-only galaxy law g²/(a0+g)=gb: an extra freely adjustable static halo is not another solution of the same algebraic hold equation.

| Baseline field inversion | Canonical a0=9.3603e-11 | Alternative a0=1.1312e-10 |
|---|---:|---:|
| Radial points | 42 | 42 |
| u >= a0: no finite hold branch | 25 | 21 |
| Remaining points with outward cold acceleration, -psi'>0 | 17 | 21 |
| Remaining points with static balance | 0 | 0 |

Above the galaxy-law acceleration but below the cap, psi'<0 exactly. An isotropic pressure that decreases outward adds an outward pressure force; it cannot hold that local state. This is not a theorem excluding every anisotropic, moving, boundary-confined or transient field configuration. Conservation-law initial data and a time-dependent solution would still be needed for those possibilities.

The screening scale Lstar has only a lower bound, not a selected value. Calling its effect negligible here is an explicit regime assumption, not an inferred upper bound. We have not solved the full switched screened operator with arbitrary large Lstar. Similarly these counts do not apply unchanged at finite mu_K, where rho_tau also contains the volume term.

## 3. If an independent cold source is added inside AQUAL

This is a successor theory, not extra freedom already present in the held native field. In spherical symmetry,

    mu(g/a0) g = G(Mb+Mc)/r²,

so the required enclosed source is

    Mc(<r) = [g²/(a0+g) - gb] r²/G.

This differs from both the native total M_tau and the preceding empirical effective mass [g-gref(gb)]r²/G. The numerical forward solution

    g = [gN + sqrt(gN²+4a0 gN)]/2,  gN=G(Mb+Mc)/r²,

recovers every input acceleration. This is inversion, not prediction from cold dynamics.

| Baseline source requirement | Canonical | Alternative |
|---|---:|---:|
| Positive enclosed Mc values | 42/42 | 42/42 |
| Median Mc/Mgas at 0.1 R500 | 7.13 | 6.66 |
| Median Mc/Mgas at R500 | 1.17 | 0.90 |
| Median Mc(R500), solar masses | 1.55e14 | 1.20e14 |
| Negative shell differences out of 35 | 6 | 9 |

All seven finite-range log(Mc/Mgas) slopes are negative: −0.89 to −0.49 canonical and −0.96 to −0.52 alternative. The required excess is more centrally concentrated relative to the gas than the naive effective-mass diagnostic suggested.

**Positive enclosed mass does not guarantee positive density.** Canonical negative shells occur in A1795, A2029, A2319 and A85 between 0.7 and 1 R500, and in A644 between 0.5–0.7 and 0.7–1 R500. Thus five systems cannot match these central values with an everywhere-positive spherical additional source. No negative shell is clipped or replaced by zero.

This is a profile-consistency warning, not a measured negative substance or statistical exclusion. Hydrostatic mass systematics, their radial variation, baryonic mass models, asphericity and correlated uncertainties can alter the differences. The six-radius sampling constrains shell averages, not a resolved pointwise density. A statistical test would require a joint profile likelihood that is not supplied by this run.

## 4. A test of finite mu_K that eliminates the potential zero point

In a static, negligible-stiffness state Xi=Phi+C and the field equation is

    div[mu(g/a0) grad Phi] + mu_K²(Phi+C) = 4 pi G rho_b.

Therefore the source density reconstructed in section 3 would have to be

    rho_c(r) = -mu_K² [Phi(r)+C]/(4 pi G).

The constant C is often an unselected extra datum. It is unnecessary for a shape test. For adjacent shells define the volume average <Phi> and rho_shell=Delta Mc/Delta V. Subtracting their equations gives the necessary identity

    mu_K² = -4 pi G [rho_shell,j+1-rho_shell,j]
                     / [<Phi>_j+1-<Phi>_j].

The potential averages are computed by integrating a piecewise power-law interpolation of observed g, with exact segment antiderivatives and numerical volume averages. The arbitrary lower-limit potential cancels. No zero point or mass scale is fitted.

Baseline results:

- Canonical: 27/28 adjacent-shell pairs demand positive mu_K, ranging **0.679–5.988 Mpc^-1**; one demands negative mu_K². None is below the inherited isolated-galaxy bound **0.1 Mpc^-1**.
- Alternative: 27/28 demand positive mu_K, ranging **0.572–5.788 Mpc^-1**; one demands negative mu_K². None passes the bound.
- In each cluster the inferred mass scale changes with radius: a single constant mu_K does not reproduce these central shell averages even if the galaxy bound is ignored.

This is a necessary static shape condition, including shells whose inferred source is negative; a negative mass-term density is mathematically possible after the potential crosses zero and was not discarded. A negative inferred mu_K², by contrast, cannot be supplied by the specified positive quadratic K coefficient. The test is conditional on the acceleration interpolation and mass estimates and is not a complete nonlinear or time-dependent finite-mu_K calculation.

## 5. Dynamical candidates and why an equilibrium is not yet a prediction

**Pressureless stationary independent cold source.** For a component that follows the physical metric, zero velocity and zero stress give 0=-grad Phi, incompatible with the nonzero cluster field. It must flow, have velocity dispersion or carry other stresses. Native dust follows psi instead, with the different obstruction in section 2.

**Isothermal independent source.** Where consecutive shell densities are positive, the approximate local isothermal requirement is

    sigma_iso² = -[Phi(r2)-Phi(r1)] / log[rho(r2)/rho(r1)].

Shell-average densities are assigned to geometric shell centers for this diagnostic. It is not an exact shell-averaged Jeans solution. The positive requirements span **453–1193 km/s canonical**, and **610–1189 km/s alternative**. Their values change within systems. Six canonical and nine alternative shell-pair evaluations are invalid because at least one inferred density is nonpositive. The code records every invalid pair. These numbers are an inverse stress requirement, not a newly predicted temperature or evidence for a universal 600 km/s constant. No isothermal amplitude is fitted.

**Collisionless stress closure.** Even if a positive profile were established, spherical steady Jeans balance only provides

    dP_r/dr + 2 beta(r) P_r/r = -rho_c g,
    P_r = rho_c sigma_r².

With I(r)=exp[integral 2 beta(s) ds/s], its solution is

    P_r(r) = { I(R) P_r(R) + integral_r^R I(s) rho_c(s) g(s) ds } / I(r).

An anisotropy function beta(r), outer pressure P_r(R), density/abundance history and a physically admissible distribution or field state remain to be selected. Satisfying this moment equation alone does not guarantee a nonnegative distribution function or a microscopic field completion. Setting beta=0 and P_r(R)=0 would be chosen boundary data, not a derivation from vacuum energy. A cold wave completion also requires its actual action and scale; none is supplied here.

The repository's already-tested isothermal partial-retention family is not retried as a new mechanism: X30_sheet_cluster_profile found it too extended in outer lensing. Its assumptions and different data are distinct from this X-COP calculation. That result is context, not an independent new test performed here.

## 6. Preserving the galaxy law is a separate, restrictive condition

For a spherical galaxy originally obeying g0²/(a0+g0)=gb, let f=Mc/Mb be a new positive enclosed source fraction. The same response gives

    mu(g/a0)g = (1+f) mu(g0/a0)g0.

The left side increases strictly with g. Exact preservation of g=g0 therefore requires **f=0**. If an independently chosen observational tolerance allows g<=q g0, then

    f <= q²(a0+g0)/(a0+q g0) - 1,

which becomes f<=q²-1 in the deep-MOND limit. No tolerance was selected to make a candidate pass. The full disk problem requires its actual nonspherical field solve; this is the spherical necessary comparison.

Consequently, reproducing a cluster profile by choosing a Jeans equilibrium is not enough. A successor must derive how its extra source is retained in clusters and sufficiently absent from galaxies, with the abundance and phase-space state determined independently. The present equations do not supply that selection. Their conservation equations permit initial data; they do not choose the unique cosmological charge or halo history from the vacuum scale.

## 7. Sensitivities and scope

Each variant changes one assumption; these are not full correlated error bounds.

| Variant | Canonical negative shells /35 | Alternative negative shells /35 | Canonical mu_K-bound pairs /28 | Alternative mu_K-bound pairs /28 |
|---|---:|---:|---:|---:|
| Baseline | 6 | 9 | 0 | 0 |
| HSE bias 0.2 | 6 | 6 | 0 | 1 |
| HSE bias 0.3 | 5 | 6 | 0 | 0 |
| Stellar masses x0.5 | 6 | 9 | 0 | 0 |
| Stellar masses x2 | 6 | 9 | 0 | 0 |

The single alternative-footing pair passing the mass bound at bias 0.2 does not supply a constant scale for the full cluster or sample. All variants have positive enclosed masses, some negative shell masses, and native cap violations; every remaining valid native baseline/sensitivity point has outward force. A constant HSE correction does not test arbitrary radial bias.

## 8. Evidence, review and continuation

The baseline and deliberately corrupted computations are bounded and single-threaded. The baseline passes ten controls, including an independent numerical root inversion, exact power-law potential fixture, zero-cold galaxy limit, force-sign test, potential-zero cancellation and input-row reproduction. The mutation doubles inferred source mass and fails forward reconstruction. Manifests hash code, source definitions and raw profiles. The plot shows baseline canonical results; both footings and all variants are in result.json and CSV files.

Self-review distinguishes three mathematical objects (native total field mass, independent AQUAL source, empirical effective mass), removes potential-zero freedom before testing shape, and retains negative shells. No independent peer review or uncertainty-marginalized exclusion is claimed.

The requested mechanism remains open. Completed routes now constrain its task:

- Native held dust: no static solution in the tested zero-mass, negligible-stiffness limit for these central profiles.
- Static finite-mass route: radial difference identity incompatible with a single galaxy-allowed mu_K on the tested profiles and sensitivities.
- Independent source: inversion gives a required profile, not a predicted one; positive-source realizability fails for several central profiles, and stress/history plus galaxy exclusion remain unselected.

An actionable continuation first needs a positive source-profile likelihood after radial hydrostatic/baryonic uncertainties, then a specified successor action and independently selected initial/boundary data. A full time-dependent or screened solve remains deferred, not excluded; running one without selected Lstar, mu_K and cosmological charge would introduce the very input freedom the user asks to remove. No candidate currently supplied in this lane resolves those dependencies.
