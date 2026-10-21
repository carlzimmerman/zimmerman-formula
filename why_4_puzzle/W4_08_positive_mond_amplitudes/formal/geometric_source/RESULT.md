# Geometric attraction, amplitude deformation and curved clock modes

2026-10-20. Criteria-only commit **1a46afd06**, continuing f4d7d0e7a.
**The requested healthy microscopic model forcing R=128pi/9 has not
been found. The original why-4/Lean goal remains active.** This checkpoint
contains new analytic source, deformation and constrained-mode results;
it is not a new determinate normalization trial.

Kappa=1/2 remains FITTED. CFG493 separately reports
kappa_Lambda=0.417+/-0.095 and kappa_crit=0.345+/-0.078. This investigation
uses the dark-energy footing; none of those values, measured accelerations,
Hubble parameters or density ratios enters a selecting equation.

## 1. A real improvement in the attractive source

[GRAVITY_PHASE.md](GRAVITY_PHASE.md) reconstructs the gravitational
order-parameter mechanism of Khoury1602.05961v2. In its leading
weak-static regime, h=|grad Phi| and Phi is the dimensionless metric
potential. The retained order parameter has positive kinetic Z^2 and

    E(h,chi)=M^2 h^2[1/(1+chi^2)+chi^2 h^2/(9a0^2)].

The metric couples universally to baryonic plus superfluid mass, without
a separately chosen phonon charge. Its actual algebraic minimum gives

    E_UV=M^2 h^2,                         h>=3a0,
    E_broken=2M^2 h^3/(3a0)-M^2 h^4/(9a0^2), 0<h<3a0.

The exact interpolation is mu=h/a0-2h^2/(9a0^2) in the broken branch.
General spatial Gauss calibration gives G=1/(8pi M^2) in three dimensions,
and the attractive deep-branch acceleration is sqrt(G m a0)/r when
superfluid mass outside the enclosed source is negligible. Thus

    C2=M^2, C3=2M^2/(3a0),
    R=4epsilon/(9M^2 a0^2), xi=32pi/(9R).

This is a constructive source improvement, but a0 is an input coefficient.
Finite-density superfluid stress is not a positive Lorentz vacuum. Also,
the retained chi mass tends to zero and its gradient cost eventually
dominates the algebraic reduction at fixed Z. No all-radius halo or
healthy microscopic completion follows from this minimum.

Varying the displayed covariant normal-fluid fields gives an additional
Euler current involving n_f Box F. Their bulk quadratic dynamics is absent
at chi=0 in this truncation. A flat-rest diagnostic satisfies that Euler
equation at the leading 1/r MOND order but fails at the next algebraic
order, so the full fluid/metric background cannot simply be prescribed.
This is a missing constrained-background calculation, not a global no-go.

## 2. An explicit obstruction to normalization by those symmetries

Add the permitted positive, bounded potential

    U_A(chi)=epsilon+A chi^6/(1+chi^2)^6, epsilon>0, A>=0.

At chi=0, changing A preserves the homogeneous vacuum stress, Einstein
coefficient and every quadratic variation, including the metric/fluid
constraints. It also preserves the exact high-h minimum and C2. In the
formal local flat-static broken limit, however,

    C3(A)=min_(s>0){M^2[1/s+s/(9a0^2)]+A/s^3},
    dC3/dA=1/s_A^3>0.

This is a concrete symmetry-preserving change of the cubic at fixed
vacuum/UV/quadratic data. It rules out selection by those data in this
specified EFT family. It is not a counterfamily of already certified
healthy curved halos: on a positive-vacuum background the curvature and
normal-fluid equations must also be solved. The flat-static limit cannot
silently be continued to h=0 on de Sitter. A regular positive mass
potential instead restores quadratic response at sufficiently small h.

## 3. Weyl geometry leaves a physical invariant unfixed

[WEYL_SOURCE.md](WEYL_SOURCE.md) treats Scholz2510.17704v3, separately
from the earlier Weyl-Rtilde^2/Proca route. The invariant connection
b=d sigma can survive Einstein gauge, so calling it pure gauge would
be incorrect. But the variational matter/vector prescription matters.
A consistently varied auxiliary unit vector reduces the pure-regime
action, modulo a boundary, to

    L=M^2 R/2-M^2(alpha+4)(partial sigma)^2/2
      -beta M^2[(partial sigma)^2]^(3/2)/(3a)-lambda a^2 M^2.

Literal matter coupling S_m[ghat] has zero direct sigma charge. The
same-compensator massive-particle action confirms this exactly. The
paper's external-vector stress and quoted baryonic trace source need
their own complete off-shell bridge; they cannot be combined with the
different normalized closure above. This is a scoped source obligation,
not a universal inconsistency claim about integrable Weyl geometry.

Even granting the paper's phenomenological source/metric dictionary,

    xi=32pi/(lambda beta^2).

Lambda beta^2 is invariant under compensator reparameterization and
varies continuously within the checked Weyl symmetry. A changed universal
matter metric can supply charge, but introduces q and changes G_UV.
At alpha=-4 the finite-static-gradient scalar has positive kinetic energy
and a wider longitudinal principal cone, while its vacuum kinetic rank
vanishes. No regular transition/quantum completion or ratio selector is
established.

## 4. A genuine curved-background health improvement

[CURVED_CLOCK.md](CURVED_CLOCK.md) returns to the actual c1-only clock
completion of the rational chiral model. Write B=M_Pl^2 and 0<M<B.
Its vacuum obeys H^2=V0/[3(B+M/2)]. Eliminating the metric shift gives
the transverse clock variable V with positive kinetic coefficient M and

    Vddot+3H Vdot+[2H^2+c_V^2 k^2/a^2]V=0,
    c_V^2=(2B-M)/[2(B-M)]>0.

The exact conformal variable aV is an oscillator. In the longitudinal
sector the lapse/shift reduction gives a positive kinetic coefficient
and a positive restoring coefficient for every k!=0. Redshift is included,
and fixed-comoving-k solutions are future bounded. Strict k=0 has a
different constraint rank and is treated separately.

On the actual small-gradient expanding Bianchi background, the homogeneous
physical tilt has restoring term

    2H_perp^2-h^2 j E_X/[(E_X+j)M].

The background equations show that it approaches 2H^2 with integrable
errors; the tilt decays sufficiently near the vacuum for each fixed
0<M<B. This repairs an overbroad extrapolation of the flat-metric tilt
test. It does not contradict the earlier high-frequency growing band in
its own weak-gravity/WKB window. No finite-k finite-gradient halo theorem,
regular auxiliary quantum state or complete microscopic spectrum is claimed.
The independently allowed amplitude/matter deformations remain present.

## Evidence and the next missing implication

The three raw action packets, primary-source cards and independent
cross-reviews are retained alongside this file. [REVIEW.md](REVIEW.md)
records the root's independent algebra and scope checks. EVIDENCE.json
pins document integrity; it does not certify physical equations.
All five inherited evidence validators passed freshly, covering nine
partial Lean modules and61 printed standard-axiom theorem sets. No new
Lean module was added to duplicate a minimum or coefficient identity.
The actual-pi adapter and physical/PDE/quantum bridges remain unverified.

The surviving constructive task is sharper: derive the special NLO
metric response and a positive same-state vacuum from a regular microscopic
action, with a principle that forbids or fixes the explicit amplitude
deformation. Neither universal attraction nor curved clock stability
supplies that principle. No independent second prediction accompanies
a selected normalization, and R=128pi/9 remains unforced.
