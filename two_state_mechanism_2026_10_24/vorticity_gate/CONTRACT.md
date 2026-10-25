# TS-B: a kinematic barrier, not a galaxy-type switch

Base revision f458ddcc2668a361fd06551922ec6fccf5914db1. User explicitly asked
to build/test a physical interaction that protects disks and allows dwarf and
cluster conversion without galaxy labels. This is a proposed effective
interaction, not a microscopic derivation or a claim of novelty.

## Routes

1. A common thermal activation scale: previously failed common-gap/bath
   ordering; retain as a control, do not repeat it as a new mechanism.
2. A rotation-dependent binding gap: test its unavoidable gradient force.
3. A barrier-only coupling to local vorticity and centered velocity dispersion:
   implement the energy and dissipative dynamics, including spatially coupled
   T density. The barrier vanishes at both endpoints, so it can change
   metastability without adding an endpoint force. This is the active route.

## Interaction selected before running

Internal coordinate x in [0,1], h(x)=3x^2-2x^3 is the tethered fraction;
s(x)=x^2(1-x)^2. Actual masses are rho_T=h rho_c and rho_F=(1-h)rho_c.
Both gravitate. For the paper's W_full, add the local energy density

    E_barrier = beta C s(x) u W_full'(u),   u=4 pi G |P|.

This form is an ansatz. It contains one dimensionless coupling beta and
positive terms. Define

    C = |curl v_b|^2 / (|curl v_b|^2 + sigma_b^2/L_rho^2),
    L_rho^-2 = |grad log rho_b|^2 + ||Hess log rho_b||_F,
    sigma_b^2 = trace(centered velocity covariance)/3.

All inputs are local moments/derivatives. No object name, mass cut, class
flag, or separately assigned free fraction enters the equations. The density
length definition and coupling strength are modeling assumptions. Their
microscopic origin and smoothing scale are not derived.

## Tests and declared interpretation

- Use all four previous Plummer mass/size profiles with the same continuous
  streaming family, independently of their names. Set v_phi=f v_c r/sqrt(r^2+
  (0.1 b)^2) with f in {0,.3,.7,.95,.99}. The finite core avoids a singular
  central streaming gradient. Compute pressure dispersion from the radial
  Jeans integral including centrifugal support, rather than assigning it by
  type. These are local/midplane spherical-background approximations, not
  complete axisymmetric distribution functions.
- Scan beta={0,10,20,40}; beta=20 is the predeclared illustrative candidate.
  Solve coupled internal-state gradient flow at frozen total density using
  the enclosed *tethered* mass to compute P. Never replace this by local
  P=h(r)P_initial, which violates the density constraint for varying h.
- Start at x=0.999 and evolve to dimensionless time 100. This is an initially
  tethered experiment; a reverse history starts at x=0.001. No Gyr conversion
  is allowed without a physical relaxation coefficient.
- Record final T fractions, receiver energy and residual forces. A protection
  target is T fraction>=.95 for f>=.95; a conversion target is T fraction<=.1
  for f<=.3. Report failures; do not use these as observed confidence limits.
- Test gravitational contamination from any converted core using the exact
  coexistence source g_b+g_F and an illustrative 0.05-dex RAR tolerance.
  This is conditional on enough T to re-equilibrate; check that supply and
  report the unrelaxed original mass distribution separately.
- Check gradients against finite differences, endpoint barrier forces, mass
  accounting, energy+receiver to 1e-5 relative, and invariance under a uniform
  velocity boost, coordinate rotation and relabeling. Use N=64 initially;
  refine selected N=128/256 cases without changing beta or the criteria.
- Test finite thermal escape through the barrier and reversed assembly
  history. Keeping a pre-existing T state is not creating T from F.

## Non-claims

No observational fit, fundamental particle interaction, relativistic theory,
live baryon backreaction, spatial halo relaxation, real disk geometry, saddle
completion, or absolute conversion timescale. A positive phase-selection
result alone cannot close the original scientific target. The earlier bound
mass impulse result does not automatically transfer to gradual conversion.
