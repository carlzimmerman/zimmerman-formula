# Nonlinear saturation during nonradial collapse

NS-20261022; base c9039eccdcc6949c19b77e01b8025c630fceda51. The original goal remains open. **The exact nonlinear polarization breaks the quadratic mass-scaling symmetry and can reverse contraction. It does not, in these tests, select a core mass or a population distribution.** Preserved dwarf fits, rotation curves and cosmological growth have not been jointly established.

The distinction matters: the previous quadratic approximation omitted the same logarithmic saturation already present in the original static core fits. Restoring it is necessary for testing collapse, but it is not a new adjustable interaction.

## What was actually solved

The field potential W(p)=-p-ln(1-p) is retained exactly. Its conjugate W*(s)=s-ln(1+s) gives the nonlinear elliptic equation

    ρ = h - div[grad h/(1+|grad h|)],
    P = -grad h/(1+|grad h|).

This is the fixed-phase, quasistatic field equation in three dimensions. It was solved on Cartesian grids for nonradial clouds, rather than replaced by a modified pair force. The convex dual, its phase generalization and limits are derived in DERIVATION.md.

The numerical portfolio includes sixteen triaxial source cases plus refinement controls, twelve Gaussian radius extrema, six initial affine collapse runs plus a finer continuation and two convergence runs, and nine relaxed-phase probes. The affine matter model permits three different evolving widths and spin; it cannot split into fragments or eject matter. None of these runs includes field radiation or dynamical baryons.

## Scaling breaks appreciably in compact clouds

For axes (1.2,0.8,1)R and masses M/Mstar=0.5,1,2,4, compare the nonlinear acceleration per unit source mass at the same geometry. At R=0.4 ell0, the fourfold-mass force differs from four times the reference force by **54.6% on the initial grid and 53.3% on refinement**, measured by the grid L2 norm. At R=0.9 ell0 the initial-grid difference is only2.4%. At R=1.3 ell0 it is0.59%.

Thus the exact similarity is broken in the regime where saturation matters and recovered toward weak fields. The initial compact heavy cloud reaches max|P|=0.462; its homology energy derivative is negative, so expansion lowers its energy. The same shape at the reference mass still favors contraction. These are source-conditioned forces, not evolved remnant masses.

Sixteen source residual tests and one dual-gradient test were recorded. One weak-source residual is1.25e-5, narrowly above its predeclared1e-5 threshold; it remains a failed numerical gate. The stronger compact sources have residuals of order1e-7. This failure does not control the refined53.3% scaling result, but is not silently reclassified as a pass.

## Saturation supports a family of radii

To remove the large periodic Newtonian image offset, the Gaussian calculations use exact isolated gravitational energy and derivatives. The nonlinear field is still solved in a finite periodic box. Fixed-χ Gaussian widths at energy extrema are:

| M/Mstar | Gaussian width R/ell0, grid64 box6 | Width in kpc | E/M in units a0 ell0 |
|---:|---:|---:|---:|
| 0.5 | 0.27566 | 0.1214 | -0.014634 |
| 1 | 0.32632 | 0.1437 | -0.027722 |
| 2 | 0.38787 | 0.1708 | -0.052092 |
| 4 | 0.46122 | 0.2031 | -0.097150 |

Mstar=1.09523e7 solar masses and ell0=0.44042213kpc. R is a Gaussian standard deviation, not the earlier finite-boundary core radius. These are extrema in a restricted profile family, not exact cold Euler equilibria or fitted dwarfs. Their radii change by at most1.78% with grid refinement and0.144% with the box-size repeat at matched spacing. A finite-difference shape-energy check agrees with the envelope derivative within9.6e-9. All four extrema also have positive finite-difference curvature in log radius.

There is no singled-out mass in this family. Energy per unit mass becomes more negative with increasing mass. Splitting a relaxed parent into two infinitely separated half-mass Gaussian minima costs positive energy:0.00110,0.00410 and0.01515 in M0 a0 ell0 units for parent masses1,2,4 Mstar. These are restricted-profile comparisons, not lower bounds on all possible fragments.

This agrees with the stronger earlier passive-equilibrium identity, which does not assume spherical symmetry:

    d(E/M)/dM < 0

along a differentiable isolated stationary branch at fixed couplings, with the stated decay and finite-energy assumptions. Nonlinear saturation can stabilize size without creating an interior minimum of binding energy per mass. Rotation, a branch endpoint, external supply or a nonstationary partition requires a separate argument.

## Nonradial contraction and rebound

The affine model evolves three Gaussian widths with a quasistatic nonlinear field at every step. Its reduced kinetic energy is M sum(adot_i²)/2; spin adds L²/[2M(a1²+a2²)]. The initial axes are(1.08,0.72,0.9)ell0. Masses0.5,1,2,4 Mstar are tested at spin energy0.02 times the Newtonian binding magnitude, with an additional heavy0.05-spin case.

All six initial runs stop when an axis drops below1.5 grid cells. Small energy error cannot override that resolution limit. The grid32 heavy run already shows one axis reversing while another is still contracting.

The grid40 continuation reaches15t0=181Myr without hitting the resolution guard. Its minimum widths are approximately(0.506,0.299,0.277)ell0. By the end, all widths are expanding and have reached(0.760,1.069,0.612)ell0. Peak fractional energy drift is2.44e-4; the final drift is about1.1e-7. The model undergoes a bounce, not dissipative settlement. Over the shared interval through12t0, halving the time step changes widths by at most0.000186ell0; grid40→48 changes them by at most0.00264ell0. Both repeats show rebound along all three axes. These checks validate bulk widths in the restricted model, not pointwise continuum profiles.

This is a real time evolution of a restricted nonradial shape, **not a full three-dimensional fragmentation simulation**. Its one-cloud mass is conserved by construction; it cannot answer whether a full flow ejects mass, forms multiple cores, or develops a preferred remnant spectrum. Fixed spin is likewise an imposed conserved coordinate, not measured exchange between fragments. No conclusion of universal mass retention is drawn from this ansatz.

For scale, the heavy initial reduced energy is about-0.02445. Two separated2Mstar Gaussian minima have combined energy about-0.01752. That specified final state plus nonnegative outgoing energy cannot follow from that initial state by cooling alone. This excludes only those particular separated Gaussian endpoints. Different profiles, a bound envelope, interactions between fragments or changed phase parameters are not covered.

## Relaxing the phase does not yet resolve the gap

The phase was also eliminated quasistatically, including its positive gradient energy. If A=a-d∇², then

    χ=1+(1/2)A^-1(h²),

and the dual gains the nonlocal quartic term(1/8)<h²,A^-1(h²)>. An independent directional-gradient check agrees to2.1e-10. This preserves reciprocity and introduces no damping prescription.

At the compact heavy probe R=0.3 ell0, λ=100 gives χmax≈1.512 and max|P|≈0.721. That source is poorly resolved and is only an exploratory probe. At R=0.6 ell0, χmax changes from1.1036 to1.0774 when the box doubles at fixed spacing. The phase excess changes25.3%, failing the declared5% boundary-convergence gate. The long phase tail therefore needs further domain refinement before predicting profiles. The relaxed phase is not a simulation of finite-inertia radiation or energy export.

## Observational and cosmological checks

**Dwarfs:** no remnant mass, central occupation or stationary formed density profile has been selected. The Gaussian family cannot be substituted for the previously calibrated cores without a new dynamical fit. Saturation-induced rebound is not a preservation test for stellar dispersions. Dynamical baryons remain missing.

**Rotation curves:** unchanged couplings do not ensure unchanged curves after matter redistribution. The exterior fixed-mass monopole alone is insufficient for stars inside an extended or evolving core. No galaxy fit is certified by these runs.

**Clusters:** neither the number of cores nor their center-of-mass phase-space distribution is produced. No cluster excess or lensing prediction follows from the one-cloud affine model.

**Growth:** the unpumped linear kernel survives exactly at first order. W(p)=p²/2+O(p³); the polarization correction begins at second order in the perturbation, and χ-1 is sourced at second order. Thus these saturation terms do not change the earlier homogeneous linear response about P=h=0, χ=1. This is a perturbative statement, not a complete cosmological growth pass: early nonlinear core formation, radiation stress, phase-background shifts, discreteness and transport are not computed. The action still lacks the completed covariant cosmology needed for that broader claim.

## Decision and continuation

The narrow question is answered positively: **nonlinear saturation breaks mass scaling and can arrest contraction transiently.** The stronger mechanism is not established: a supported radius or rebound is not a selected inventory, and passive binding still favors growth on the stationary branch.

The next unresolved implication is a converged material partition with the full nonlinear fields and a kinetic closure through crossings: bound fragments, bound envelope, ejecta and outgoing field energy, with angular-momentum exchange measured separately. Such a calculation must include enough spatial degrees of freedom to permit fragmentation. Its mass spectrum and settled profiles must then be tested with live baryons and a cosmological background. This is an open continuation, not an exhausted mechanism and not a successful joint fit.
