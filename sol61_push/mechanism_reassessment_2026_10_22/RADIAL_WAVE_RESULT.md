# Spherical radiation requires a long-range outgoing boundary

The formal reduced model now has a radial wave operator around the finite-stiffness background. Its exterior is long range: polarization gives h~H/r, so the outgoing wave has a logarithmic phase. A finite-radius vacuum boundary is not uniformly accurate at low frequency. This changes how to compute radiation; it does not yet give a halo damping rate.

## Radial equation from the quadratic energy

For radial perturbations delta P=grad sigma about q(r), the radial Hessian is

    h(r)=K[(1-q(r))^(-2)-1].

Within the earlier approximate kinetic reduction, the quadratic action is proportional to

    integral dr r² [B sigma_t² + eta sigma_rt²
                    -h sigma_r²-gamma (Laplacian sigma)²]/2.

Take harmonic time dependence exp(-i omega t) and u=r sigma. The exact radial equation within this model is

    gamma u'''' + (eta omega²-h)u'' - h' u'
      + (h'/r-B omega²)u = 0.

The spatial quadratic form is

    integral dr [h(u'-u/r)²+gamma u''²]/2,

and the kinetic form is integral dr [B u_t²+eta(u_t'-u_t/r)²]/2. Under vanishing boundary terms both are nonnegative. The h'/r term in the differential equation can be negative without implying negative total energy. This positive quadratic form is not a proof of well-posed full-theory evolution or asymptotic decay.

## Exterior phase

For an isolated finite baryonic mass, the reduced background has q~C/r, hence h~H/r with H=2KC. The asymptotic vacuum wavenumber solves

    gamma k⁴-eta omega² k²-B omega²=0, k>0.

An outgoing solution has leading form

    u_out ~ exp[i k r+i alpha ln(r/r0)] [1+O(1/r)],
    alpha = -H k/[2(2 gamma k²-eta omega²)].

Here r0 only fixes a constant phase. Substitution cancels the order 1/r residual; setting alpha=0 does not. The corresponding leading outgoing derivative is i(k+alpha/r)u, not simply i k u. A fourth-order solver also needs the decaying exterior solution; this single derivative relation is not a complete two-condition outer boundary. Higher asymptotic terms or exterior integration and boundary-radius convergence remain necessary.

The logarithmic phase is mathematically familiar in long-range scattering. No global novelty claim is made. This derivation is model-specific and does not import an external scattering theorem.

At low frequency, k~(B/gamma)^(1/4) sqrt(omega). The stiffness/bending crossover can be characterized by h~sqrt(B gamma) omega, giving

    r_cross ~ H/[sqrt(B gamma) omega].

Thus the exterior approaches its vacuum regime only at increasingly large radii for slow disturbances. The limit is not uniform in frequency. This is a reason not to multiply the previous planar transmission coefficient by the homogeneous-vacuum source luminosity and call it a halo cooling law.

## Conditional travel estimates and a failed approximation

Use dimensionless length R and time R sqrt(b)/c, b=(2+3 beta)/beta, beta=0.02798. For gamma/(K R²)=0.01 and eta=gamma, the dimensionless coefficients are B=1, gamma=0.01, eta=0.01/b. The A=1 asymptotic stiffness is h=2/r. These definitions explain why the two dimensionless coefficients called eta and gamma differ despite equal dimensional coefficients.

Using the local dispersion root, the group velocity is

    vg=k(h+2 gamma k²-eta omega²)/[omega(B+eta k²)].

The following integrates 1/vg from radius 10 to r_cross in the idealized h=2/r tail. These are ray estimates, not computed wave delays or damping times.

| Dimensionless omega | r_cross | ray travel time | maximum WKB parameter |
|---|---:|---:|---:|
| 0.01 | 2000 | 31091.6 | 2.236 |
| 0.03 | 666.7 | 5971.63 | 0.745 |
| 0.1 | 200 | 968.847 | 0.223 |
| 0.3 | 66.67 | 174.642 | 0.0722 |
| 1 | 20 | 17.901 | 0.0174 |

The first two clearly do not justify a short-wavelength approximation over the full interval, and 0.1 is marginal. No low-frequency escape-time conclusion is drawn from those numbers. At higher frequencies the local approximation is more favorable, but the exact background, central emission, mode amplitudes and energy loss still need solving. A large travel time is not itself a proof of weak damping; energy may already have left the inner region before reaching the vacuum regime.

## Evidence and next calculation

Seven checks pass: direct radial reduction, separate Euler variation of the quadratic energy, constant-stiffness limit, outgoing logarithmic coefficient, positive local root and group velocity, and numerical dispersion-derivative agreement. radial_wave_run/manifest.json validates. Reversing the logarithmic-phase sign fails the cancellation check (six of seven pass). The early probe preceded addition of the quadratic-form check; the bounded run includes it. Review is self-review.

The appropriate next task is the global forced radial fourth-order problem on the computed q(r), including regular central conditions and both admissible exterior branches, with an exact flux budget and increasing matching radius. Only after that can a source perturbation or free mode be assigned a credible radiated power. Matter backreaction and the missing cold-sector selector remain separate essential obligations; this calculation has not resolved them.
