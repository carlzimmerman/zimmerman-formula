# Nonradial fragmentation and angular-momentum transport

Checkpoint NT-20261022. The route produces a preferred **linear length** and real internal torques in a restricted limit of the reciprocal action. It does not yet produce selected core masses, a population distribution, or a joint dwarf/rotation/growth pass. The full nonlinear mechanism remains open.

## 1. A new length scale in flattened matter

Use ell0 = 0.44042213 kpc, M0 = a0 ell0²/G = 1.30258e8 solar masses, t0 = sqrt(ell0/a0) = 12.0743 Myr. Coordinates and wave numbers below are dimensionless. Density is in M0/(4π ell0³), surface density Σ in M0/(4π ell0²). The inherited canonical core mass is mstar = 0.084081325 M0 = 1.09523e7 solar masses.

In the weak-polarization, fixed-phase, quasistatic limit the three-dimensional potential acting on cold material is

    ψ(K) = -ρ(K)/[K²(1+K²)].

This follows by eliminating the quadratic polarization field; it is not the exact nonlinear logarithmic-W action at large polarization. For a razor-thin sheet, integrate over vertical wave number:

    ψ(k,0) = -Σ/2 [1/k - 1/sqrt(1+k²)].
    γ² = (Σ/2) F(k) - κ²,
    F(k) = k - k²/sqrt(1+k²).

Here κ is the epicyclic frequency. Pressure and velocity dispersion are absent. A uniform rotating background is supplied; its formation is not derived. For the unrotating sheet F is positive, approaches zero at both endpoints, and has a unique maximum. Set u = k/sqrt(1+k²). Then F'(k)=1-2u+u³, whose unique interior zero on (0,1) is u=(sqrt(5)-1)/2. Consequently

    kstar² = (sqrt(5)-1)/2,
    kstar = 0.78615138,
    Fmax = 0.30028311,
    λstar = 2π ell0/kstar = 3.52000 kpc.

This changes the earlier homogeneous 3D result: flattening introduces a finite preferred wave number even in the cold limit. It does not contradict the earlier 3D calculation because the vertical source geometry and Green function have changed.

Define a footprint, not a remnant, as a circle of radius half this wavelength. Its mass is

    Mpatch/M0 = π² Σ/(4 kstar²).

Matching mstar requires **input** Σ=0.02106067, or 1.12546 solar masses/pc². At that input, the nonrotating e-fold time is 214.721 Myr. Changing Σ by factors 1/4 through 4 gives masses 1/4 through 4 times mstar, at the same wavelength. The circle convention is itself an order-unity mass convention; linear theory supplies no bound-core boundary.

Rotation can suppress the axisymmetric instability when κ² ≥ Σ Fmax/2; it does not change its maximizing wave number in this cold, fixed-thickness model. If marginal stability is imposed to determine Σ, the inferred mass instead depends on κ². Neither prescription gives an absolute mass independent of environment.

## 2. Thickness and genuinely nonaxisymmetric waves

Take f_H(z)=exp(-|z|/H)/(2H), fixed during a common planar displacement. Vertically averaging the force over the same profile gives

    T(a) = (2+a)/[2(1+a)²],   q = sqrt(1+k²),
    F_H(k) = k T(kH) - (k²/q) T(qH).

This is a pair-profile average, not a midplane approximation. Nine independent vertical Fourier quadratures agree with F_H/2 within 2e-16. The assumed profile needs vertical support; a cold self-gravitating sheet of prescribed finite thickness is not an equilibrium derived here.

| H/ell0 | Wavelength (kpc) | Footprint mass/mstar at fixed Σ=Σstar |
|---:|---:|---:|
| 0 | 3.520 | 1.000 |
| 0.1 | 3.600 | 1.046 |
| 0.3 | 3.925 | 1.244 |
| 1 | 4.978 | 2.000 |
| 3 | 6.929 | 3.875 |
| 10 | 10.846 | 9.494 |

For shear parameter q_s=1, κ²=2Ω² and kx=ky(-4+Ωt). With a=i v, the real amplitude equations are

    δdot = -kx ax - ky ay,
    axdot = 2Ω ay - A(k) kx δ/k²,
    aydot = -Ω ax - A(k) ky δ/k²,
    A(k) = Σ F_H(k)/2.

Thirty initial-value problems cover H=0,1; κ²/Amax=0.3,0.9,1.2; ky/kpeak=0.25,0.5,1,2,4. Starting δ=1e-5, evolution stops at |δ|=0.1 or kx=4ky. Seven cases hit the cutoff. Even at κ²/Amax=1.2, the ky/kpeak=0.5 waves amplify by factors 493.1 (thin) and 469.8 (H=1). Thus absence of an axisymmetric growing mode does not prevent transient nonaxisymmetric amplification. These are density amplitudes, not numbers or masses of fragments. Three tighter repeats agree to about 2e-12 relatively; an independent constant-k eigenvalue check recovers γ²=A-κ².

The shearing-sheet setup is consistent with the local orbital framework in [Binney, arXiv:1906.11696v1](https://arxiv.org/pdf/1906.11696), section 2. That paper treats stellar dynamics; none of its stellar dispersion results are substituted for this action's kernel.

## 3. Actual nonradial torque experiment

The quadratic quasistatic kernel gives a pair energy

    Uij = -mi mj (1-exp(-s))/s,
    s = sqrt(|xi-xj|² + ε²).

The force used is the exact gradient of this softened energy. Softening is a numerical modification, not a new action parameter. Seven isolated planar particle experiments use a deterministic initially elliptical disk of radius about 8 ell0, total baseline mass 4 mstar, and rigid initial spin energy C/|U|=0.02 or 0.05. There is no matter damping, external torque, or radiative energy sink. Initial geometry is imposed, not formed from the previous spherical seeds. N=96 is repeated at N=192; dt=0.04 t0 at 0.02 t0; ε=0.2 ell0 at 0.1 ell0. Baseline duration is 120 t0 = 1.449 Gyr.

Individual angular momenta change while their sum is conserved. Track a fixed set of initially inner-quarter particle labels, so the diagnostic measures torque rather than just material crossing a radial boundary:

| Case | Initial share of total L | Final share of total L |
|---|---:|---:|
| N96, spin 0.02 | 0.06185 | 0.27186 |
| N96, spin 0.05 | 0.06185 | 0.55170 |
| N96, half time step | 0.06185 | 0.27186 |
| N192, spin 0.02 | 0.06162 | 0.24810 |
| N96, half softening | 0.06185 | 0.21770 |

The initially inner labels **gain** angular momentum in these runs; this is not evidence for universally outward transport. Total L error stays below 6.1e-15 and peak fractional energy error below 3.7e-5. The independent energy-gradient check agrees to 5.4e-13. Halving dt changes final positions by at most 8.85e-5 ell0. Particle/softening changes move the angular-momentum shares by 0.024/0.054, so the declared 0.01 absolute precision gate fails. No converged fragment finder or stationary core profile is claimed. The baseline final half-mass radius is about 8.80 ell0; this is not a compact settled endpoint.

There is a decisive scaling obstruction **in this limit**. For fixed geometry and softening, multiplying every particle mass by b gives

    x_b(t) = x_1(sqrt(b) t),
    v_b(t) = sqrt(b) v_1(sqrt(b) t),
    L_b = b^(3/2) L_1.

The spin ratio is unchanged. Any geometrically defined fragments therefore have the same mass fractions and masses multiplied by b at corresponding stages. Numerical b=1/2 and 2 repeats reproduce final positions within 7.6e-13 ell0. The uniform argument, rather than the finite repeats, excludes an absolute mass attractor for this family. It does not exclude mass selection after nonlinear polarization, phase evolution, radiation, baryon coupling or a specified environmental supply breaks the similarity.

Internal torques conserve energy; they can exchange orbital energy and L and allow some material to escape, but they do not by themselves supply the field-radiation channel. Nonlinear contraction may leave the quadratic regime. Polarization/phase amplitudes were not evolved or bounded here, so these runs establish properties of the reduced model, not controlled approximations to the full late collapse.

## 4. Can previous modest-spin seeds supply the sheet?

The preferred half-wavelength is 3.996 ell0 = 1.760 kpc. Previous spherical seeds have 95%-mass radii only 1.32–2.64 ell0 over M/mstar=0.5–4. A local sheet calculation actually needs a background larger than the wavelength; half a wavelength is only an optimistic geometric yardstick.

Using the previous seed angular-momentum inventory, consider circular orbits at R=3.996 around a central mass equal to the entire seed. The quadratic-kernel specific circular angular momentum is

    j_circ = sqrt(M R [1-(1+R) exp(-R)]).

If all remaining angular momentum is nonnegative and no external torque acts, the inventory permits a fraction no larger than L/(M j_circ) on those particular orbits. Across the eight prior mass/spin combinations this is 0.054–0.122. This is a conditional central-potential benchmark, **not** a rigorous bound on a self-gravitating extended disk: its enclosed mass and force law differ; counterrotation and external tides also remove the inference. It shows why importing a large, long-lived sheet from modest-spin compact seeds needs a formation calculation.

## 5. Dwarfs, rotation curves, clusters and growth

- **Dwarfs:** no selected final mass, central occupation or stationary profile. At a chosen surface density the footprint can equal the previous fitted mass, but that is calibration. Its 1.76-kpc radius is not the previous compact core radius; subsequent contraction, mass partition and baryonic response remain to be solved. No new dwarf fit is certified.
- **Rotation curves:** fixed mass and centroid protect the distant Newtonian monopole. They do not protect the force inside an extended fragment population or the nonlinear polarization response. The simulated cloud expands to kiloparsec scales and is time dependent. No new rotation-curve preservation claim is warranted.
- **Clusters:** local instability determines neither the supply of sheets nor the center-of-mass orbital phase space of their remnants. Cluster abundance, radial distribution and lensing therefore remain unpredicted. No population is added by hand to claim success.
- **Cosmological growth:** ell0 and the homogeneous linear kernel are unchanged in these calculations. A useful limited protection is exact for compensated local redistribution: if mass and centroid are preserved, the normalized Fourier-profile change begins at order k². For a profile u(k)=<exp(i k·x)> with <x>=0,

      |u(k)-1| ≤ (1/2) <(k·x)²>.

  For the final baseline cloud at z=0, comparison with the same mass placed at its centroid gives 6.46e-8 at k=0.1/Mpc and 6.46e-6 at k=1/Mpc. Both satisfy the bound. This is a profile-form-factor statement, not a growth-factor calculation; for two extended profiles the two bounds add. At formation redshift, physical lengths must be converted to comoving lengths. Creation of new mass, uncorrelated core placement, uncompensated shot noise, long-range transport, radiation stress or changing the homogeneous phase is not covered. The inherited conditional growth diagnostic is not a test of this forming population.

## Decision

Flattened instability is a surviving mechanism for an environmental fragmentation length. Angular-momentum exchange is demonstrated in a conservative reduced model. Universal core-mass selection by this quadratic transport route is excluded by similarity; a quantitative distribution prediction fails the current resolution gate. The overall theory is neither validated nor ruled out by these results.

The next discriminating continuation is to derive the surface-density/thickness supply and follow nonlinear field saturation during nonradial collapse with a kinetic closure through crossings and reciprocal baryon evolution. It must produce a converged bound mass partition and profile, and account for exported energy and material separately. That is an open continuation, not something these finite runs establish. Repeating the same quadratic disk at more masses cannot remove its exact scaling obstruction.

Reproduction and provenance: three completed bounded runs, with scripts, contracts and manifests in this directory. AUDIT.md distinguishes ordinary numerical checks from failed interpretation gates. No manuscript changes, commits or external publication.
