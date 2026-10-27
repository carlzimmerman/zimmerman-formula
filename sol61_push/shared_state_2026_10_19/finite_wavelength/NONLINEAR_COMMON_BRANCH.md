# The common-profile branch is invariant under nonlinear common forcing

The exact two-fluid TF control in `modes/SHARED_MODES.md` permits a useful
nonlinear statement without extrapolating a harmonic oscillator. Keep its
declared pressures p_d=K_d rho_d^2,p_b=K_b rho_b^2, fractions a,b and
K_d a=K_b b=K. Consider any smooth one-fluid Euler–Poisson solution

    rho_dot+div(rho v)=0,
    v_dot+(v.grad)v=-grad(2K rho+U+U_ext),
    laplacian U=4piG rho.                                  (1)

Then the fields

    rho_d=a rho, rho_b=b rho, v_d=v_b=v                       (2)

are an **exact solution of the full nonlinear two-fluid equations** under
the same arbitrary common U_ext. Each continuity equation is its fraction
times (1). Each pressure enthalpy is 2K_j rho_j=2K rho, and each Euler
equation is therefore identical to (1). Poisson sees the total rho once.

For smooth flows with uniqueness, initial data satisfying (2) remain in
this submanifold. There is no hidden nonlinear species-separation response
to common gravity along it. Its compensated composition modes can be
excited by differing initial conditions or a differential force, and may
couple to other departures from this special EOS/profile limit. They are
not generated from exactly aligned comoving data just by increasing a
common applied field. This is not a claim of uniqueness after shocks,
stability under all finite departures, or invariance after reinstating the
scalar quantum term or a different baryon EOS.

The energy identity gives the static counterpart. With
rho_d=a rho+eta,rho_b=b rho-eta,

    E=K integral rho^2+W[rho]+K/(ab) integral eta^2,
    source energy=integral U_ext rho,
    integral eta=0, -a rho<=eta<=b rho.                      (3)

For every total profile and any strength of a common static source, eta=0
is the unique minimizing composition at the selected separate mass ratio.
A composition saturation law cannot be extracted from (3)'s common source.

For a diagnostic differential potential DeltaU=U_d-U_b, the local minimizer
at fixed rho instead is

    eta=clip[-ab(DeltaU-C_eta)/(2K), -a rho, b rho],           (4)

where the global multiplier C_eta enforces the separate mass constraint.
This is real population depletion/clipping in that *different source*
problem. It is not the requested rational hardening law and the original
minimal gravitational coupling supplies DeltaU=0. Separate copied host
inertias or a source attached only to the dark density would change that
physical problem and cannot justify using (4) for gravity.

The total-density branch still deforms under non-affine common gravity,
as the computed finite-k susceptibility demonstrates. Its nonlinear
continuation can include moving surfaces, redistribution, fragmentation or
escape. A linear spectrum neither establishes a finite dipole ceiling nor
turns those many-level collective modes into independent two-level sites.
For a bounded source and a genuinely isolated gapped quantum ground state,
the independently audited analytic theorem in OCCUPATIONS.md further rules
out the exact rational zero-field cusp. Critical/nonuniform soft families
remain separate possibilities, with an actual state-selection obligation.
