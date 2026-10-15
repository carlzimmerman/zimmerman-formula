# Calculations ready for Claude: CPC-001/002

This is a repository handoff; no chat message was sent. It concerns the proper
F(B,C) finite-source propulsion candidate, not the separate MOND constitutive
law or neutral-atmosphere programs. Base and predecessor commits: [BASE.json](BASE.json).

The missing controller contribution to the clock equation is now calculated:

    div[N² W + N sqrt(gamma) A partial_t Lambda] = 0,
    A = M² Lambda (partial_x sigma², partial_y sigma², 0)/4.

A uniform speed ramp with the old instantaneous target fails by
M² Lambda Lambda_dot Delta_perp(sigma²)/4. A lapse-only perturbative repair
fails at the regular radial current centers for |Lambda sigma|<1.

There is an exact clock-only repair, with gamma=I,N=1:

    L = 4h I + F0 I - S*,
    delta B = -Lambda_dot L^{-1} A,
    delta beta = +Lambda_dot L^{-1} A.

It makes the total clock current equal the stationary divergence-free current.
A sufficiently large compact h plateau with a buffer around the wall makes L
uniformly invertible on the correction support and makes the correction smooth
through the vacuum boundary. This is not a stability theorem for that choice.

Do not promote this to a launch solution. The stress correction and remaining
controller equation are explicitly derived in [PROOF.md](PROOF.md), sections
4–5. A globally homogeneous controller ramp has infinite kinetic energy when
F_c>0, so it cannot be used for a finite-energy drive.

Completed evidence: 26 clock identities/checks and 9 stress/controller/energy
checks, both exact SymPy runs, with bounded-run manifests and hashes. Review is
adversarial self-review, not independent review.

Still open for this action:

1. Full nonlinear constraint classification, including controller terms and
   material/vacuum interfaces; the pure-core bracket is not first class modulo
   the bare Hamiltonian constraint alone.
2. A finite-energy localized controller evolution satisfying the clock,
   controller and ten Einstein equations together, with payload and momentum
   accounting. The correction above is an input to this calculation, not its result.
3. Reduced curved-background stability and well-posedness of the coupled system.
4. A physical source for the inverse-engineered negative normal energy and
   constitutive coefficients; no demonstrated cold carrier or conversion exists.

The original propulsion/theory goal remains open. These calculations remove an
omitted clock term and provide a precise conditional compensation; they do not
finish all calculations needed to establish the theory.
