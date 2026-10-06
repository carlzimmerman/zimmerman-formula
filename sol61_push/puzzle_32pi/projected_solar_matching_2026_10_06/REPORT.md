# Nonlinear projected-star Solar matching: bounded NR result

## Result and exact scope

The actual projected-source nonlinear Poisson equation gives a conditional visible inner quadrupole approximately **Q2=2.83e-26 s^-2** for Claude p57's T=128.915, a0=9.3603e-11 m/s² and aligned physical external field ge=2.146e-10 m/s². This is a finite-volume numerical estimate with empirical refinement/boundary tests, not a certified continuum error bound, a full Solar likelihood, a healthy covariant solution, or a 32pi selector. The computation advances the previously missing global strong-source NR matching leaf; it does not transfer QUMOND's quadrupole to this different operator.

The primary model has ordinary matter and zero twin density, with

    div[mu(x) grad Phi_star]=4pi GN rho,
    Delta Phi_plus=4pi GN rho, Phi_visible=(Phi_plus+Phi_star)/2,
    x=|grad Phi_star|/a0,
    nu(y)=1+b(y)w(y), b=sqrt(1+1/y)-1, w=1/[1+(y/T)^2],
    x(y)=y(2nu-1), mu(x(y))=y/x(y).

The inherited spherical kernel fixes this mu; the nonspherical solution is obtained from the nonlinear PDE, not from applying nu to a Newtonian vector field. The background aligned dictionary is ge/a0=ye nu(ye), xe=ye(2nu(ye)-1). At the default cutoff ye=1.8466394447, xe=2.7386836753, mue=.6742799329, Le=dlnmu/dlnx=.4167619737. The project NR branch, physical metric interpretation and uniform external alignment are assumptions. Full covariant lapse/shift/clock constraint admission on this sourced solution is unproved; elliptic force inversion does not establish it.

## Global constitutive admission

Write s=sqrt(1+1/y). Then b+yb'=(s+1/s)/2-1>=0 and b<=1/(2y). Differentiation gives

    x'=1+2w(b+yb')-4b w(1-w)
       >=1-2w(1-w)/y
       >=1-9/(8sqrt(3)T).

The last maximization is of z/(1+z²)^2, at z=1/sqrt(3). This sufficient global bound is positive for all three declared cutoffs T=8,128.915,256. Furthermore nu'<0, so mu_x>0; mu+x mu_x=dy/dx=1/x'>0. The operator is strictly monotone at nonzero field, with mu~x/4 at zero and mu->1 at large field. It is not uniformly elliptic at zero. No artificial positive-mu floor is imposed. The logged smallest sampled face coefficient is a discrete diagnostic, not a proof that a continuous external-field saddle is absent.

The inverse is log-PCHIP on 20001 log-spaced points y in exp([-50,50]), with explicit deep/UV asymptotes beyond that table. An independent inverse substitution test spans exp([-18,18]); it tests table interpolation, not numerical PDE convergence. These analytic conditions justify the constitutive branch; the Picard iteration is corroborated by convergence and by reassembly of the actual nonlinear residual at the final field.

## Conservative annulus problem and numerical surrogate

Units are rM=sqrt(GM/a0) and potential a0 rM. The solar GM convention is taken directly from Claude's AU/year normalization: GM=4pi² AU³/year², AU=1.495978707e11 m, year=3.15576e7 s. Thus GM=1.3271745305967791e20 m³/s² and rM=1.1907460108277728e15 m. No astronomical data are fetched.

Set t=cos(theta). In the source-free annulus the equation is

    partial_r[r² mu partial_r Phi_star]
    +partial_t[(1-t²)mu partial_t Phi_star]=0.

Logarithmic radial edges and uniform t cells define a conservative flux balance. Radial cell centers are arithmetic averages of edges. Each face mu uses a reconstructed full radial plus angular gradient, not merely the radial derivative. Frozen-face Picard solves a symmetric sparse conductance matrix, relaxes by .8, and stops at relative potential update tolerance. The final residual is rebuilt using mu of the final field, preventing a frozen-linear residual from impersonating nonlinear convergence. Its reported norm is max absolute algebraic residual divided by 1+max absolute RHS; this is not a discretization-error norm. End angular fluxes vanish at t=+-1. Row-integrated radial flux divided by 4pi gives the unit source mass; all radial rows and the outer face are checked.

Inner boundary: rmin² mu partial_r Phi_star=1+xe rmin² t. This has exactly unit total mass and the high-force uniform-field dipole. It represents an excised compact monopole, **not a resolved solar fluid interior**. Deep inside the strong-force region mu differs from unity at order r^6; the omitted regular inner quadrupole can introduce a decaying r^-3 image, explicitly fitted below. Halving the excision radius tests this regularization, but does not prove convergence for every physical density profile. The zero-source control instead imposes the correct mue xe uniform flux.

Outer boundary is the leading external-dominated anisotropic star Green function:

    Phi_bc=xe R t-1/[mue sqrt(1+Le) R sqrt(1-Le t²/(1+Le))].

This is used only at the boundary. The full interior operator remains nonlinear. Doubling R tests residual boundary sensitivity; no claim that this leading far expansion is exact at finite R. Newton's plus potential has no regular l=2 term for this source/uniform field.

## Extraction, signs and actual convergence evidence

The l=2 star profile is (5/2) times the cell-integrated P2 projection. Its weights exactly eliminate an isotropic radial profile and the uniform l=1 field. The piecewise-constant projection has a finite angular bias: midpoint samples of exact P2 are returned with factor 1-5/Nt²+4/Nt⁴, not unity; refinement controls this bias. Each inner window is fitted to A2_star r²+B r^-3. Columns are normalized before least squares. The primary window is r=.01..025, with .015..035 as a stability check; larger windows are retained as diagnostics of radial/nonlinear contamination. Because Phi_visible is half the Newton-plus-star sum and Phi_Q=-Q2 r² P2/3,

    Q2_visible=-(3/2) A2_star a0/rM.

The negative sign is part of the declared quadrupole potential convention. Dropping the physical half is an explicit mutation control. Raw l2 profiles, all five window fits, histories, boundary constants, actual residuals and flux ranges are saved in results.json.

| case | Nr x Nt | rmin | R | Q2 visible (s^-2) |
|---|---:|---:|---:|---:|
| coarse |120 x64|.0025|40|2.81440496e-26|
| medium |200 x96|.0025|40|2.82414097e-26|
| reference |240 x128|.0025|40|2.82665213e-26|
| inner radius half, matched log spacing |214 x96|.00125|40|2.82416935e-26|
| outer radius double, matched log spacing |229 x96|.00125|80|2.82416565e-26|
| tighter Picard tolerance 1e-12 |240 x128|.0025|40|2.82665214e-26|
| fine |320 x160|.00125|40|2.82809917e-26|

Fine's paired 160x80 same-domain value is 2.82047802e-26, a .270% change. Medium-reference change is .089%; matched inner-radius change is .00101%; doubled-domain change is .000131%; Picard tolerance is negligible. These are **observed changes, not uncertainty bounds**. Angular and radial discretization are changed together, with no rigorous order extrapolation; a degenerate-field saddle and inner-source geometry remain continuum limitations. Newton and zero-source tests give Q2 below 1e-31, checking geometric cancellation and mass dependence.

Nonselected cutoff comparisons at fixed 200x96, rmin=.0025,R40 are T=8:2.94625006e-26 and T=256:2.81959284e-26, versus T=128.915:2.82414097e-26. Each recomputes the external background to retain the same physical ge. This is a model sensitivity check, not a target fit or a universal solar screening theorem. The strong-tail change is modest here; it does not make the inner coefficient identical to an external-field linear coefficient.

## Solar benchmark, previous work and remaining arrow

The inherited primary-source registry authenticates Hees2014's quadrupole convention and Park2026 v2's updated (1.6+-1.8)e-27 s^-2 fit. Our number is larger than this benchmark scale; the checkpoint intentionally does **not** attach a statistical exclusion. The actual likelihood/source systematics, Sun interior, other gravitational effects, and full admissibility of the projected covariant source branch have not been quantified. The p57 QUMOND value is only used as a rejected-transfer control; equal spherical nu does not imply equal external-field PDE or Q2.

The first unresolved full-theory implication is that this NR annulus solution extends to a regular sourced solution of the full two-metric/common-clock constraints and matter equations. Independently, numerical refinement is not a proof of continuum accuracy or global regular-source matching. Nothing fixes the interaction offset, cutoff, vacuum coefficient or 32pi. Earlier EFE work established only the far anisotropic response; this child supplies a direct nonlinear strong-source numerical discriminator for the actual new operator.

## Reproduction and preserved development

contract.json lists exact execution inputs, software and bounds. Main and fine runs plus omit_half, transfer_QUMOND and no_source controls use the standard mathbox bounded runner, single-thread cooperative BLAS caps, CPU45s/wall60s per run, max140 Picard steps and per-solve wall40s. RUNS.json holds actual status/hash validation after freeze and is not an execution input. The three controls must each fail only its false assertion.

preflight preserves the complete development trail. The initial solver_a/scan_a used an older memorized GM and wider primary window; they are historical experiments, not current units/results. Later solver_c/checks_c/results_c used corrected units but unmatched-radius grid controls. results_d is the final current-main preflight; results_fine is the fine preflight. Numerical-library oversubscription made earlier unthreaded fine scans slower; current runs explicitly cap threads. No silently discarded resource failure is used as evidence. No original primary PDF bytes are distributed; inherited exact URLs/version locators and registry hash allow source reauthentication.
