# Same-action head-on pair experiment and symplectic mode projection

20 October 2026. Independent analytic experiment/projection design. Exact source bytes are pinned in `sources_projection.json`. No pair evolution, stationary solve, projection experiment or outgoing solve is run here. All proposed numerical choices and acceptance thresholds belong in a new pre-run contract; existing criteria/results remain unchanged.

**Discriminating objective:** evolve an actual pair using the specified full action, then measure a persistent internal ell=2,m=0 excitation of a matched single remnant. An overlap of two separated cores with a quadrupole template is not that measurement. A head-on axisymmetric experiment has zero orbital angular momentum and cannot close the galactic orbital-J obligation.

## 1. Exact action and full evolution

Use the already declared alternative common classical action

    L=|Psi_t|^2-|grad Psi|^2+|X_t|^2-|grad X|^2
          +(chi_t^2-|grad chi|^2)/2-V,
    V=m^2|Psi|^2+MX^2|X|^2+g(X*Psi^2+X Psi*^2)
          +lambda|Psi|^4+a chi|Psi|^2+U(chi),
    U(chi)=M^2 chi^2/2-M chi^3/8+chi^4/4.

The pinned parameters are m=1, MX^2=4.0016, g=.002168, lambda=1.9900011745861654, a=200 and M=100. The field equations are

    Psi_tt-Delta Psi+(m^2+2lambda|Psi|^2+a chi)Psi+2g X Psi*=0,
    X_tt-Delta X+MX^2 X+g Psi^2=0,
    chi_tt-Delta chi+M^2 chi-3M chi^2/8+chi^3+a|Psi|^2=0.

For axisymmetry, Delta=partial_rho^2+(1/rho)partial_rho+partial_z^2, with regularity at rho=0. Keep all five real fields and their momenta. Algebraically eliminating chi or transferring the protected original action would change this experiment. The heavy chi mass imposes a real time-resolution requirement even when its initial profile is smooth; stability of a time step is not adequate phase/energy accuracy.

Prefer a radial finite-volume operator self-adjoint in the cylindrical volume weight 2pi rho d_rho d_z, with a regular axis flux. Energy and charge must use the same spatial discretization and weight. Specify the integrator, axis stencil, boundary flux and any absorber before the run. Keep allocated/observed memory and retained outputs below1GB; stream scalar diagnostics and a few declared snapshots rather than storing every time slice. A modest axisymmetric pilot and time/grid refinement can fit this limit; no 3D evolution is required.

## 2. Pair initial data and controls against injected ringing

Choose equal incoming fragments, opposite z velocities, zero impact parameter and a declared relative U(1) phase. In the proposed 80000+80000 case the relaxed profiles supply both f,b,h and their derivatives. The phase of X is twice the phase of Psi: rotating the two fields independently changes the interaction state.

For one fragment with signed velocity v, centre z0 at t=0, gamma_v=(1-v^2)^(-1/2), define

    z'=gamma_v(z-z0-vt), tau=gamma_v[t-v(z-z0)],
    r'=sqrt(rho^2+z'^2),
    Psi=e^(i omega tau+i theta)f(r'),
    X=e^(2i omega tau+2i theta)b(r'), chi=h(r').

Initial momenta must include both the phase rate omega gamma_v and the profile advection `r'_t=-gamma_v v z'/r'`; the X phase rate is twice as large. A Galilean phase pasted onto an uncontracted profile is not the exact Lorentz-boosted seed of this relativistic action. Summing two well-separated boosted fields is only approximate because their tails overlap: compute the actual initial E,Q and interaction residual rather than resetting them to twice a target.

Minimum discriminating controls are: an isolated static fragment on the evolution grid; an isolated boosted fragment at the chosen speed; increased initial separation with the same collision parameters; and declared time-step/spatial refinements. The static/boosted controls measure discretization and initialization excitation at the very mode frequency being sought. Equal/opposite momentum and reflection symmetry should maintain the common centre and zero net Pz/J; their drift must be reported. A bounded single relative phase/velocity run establishes only that specified collision. Other phase choices or incoming velocities require separately declared cases.

Record full Noether charge

    Q=integral[2 Im(Psi*Psi_t)+4 Im(X*X_t)]d^3x,

energy, Pz, and one consistent boundary/absorber ledger. If momentum damping `field_tt ...=-eta field_t` is used, its local energy debit is eta[2|Psi_t|^2+2|X_t|^2+chi_t^2] and charge debit eta times the local charge density. These are numerical sink accounts, not automatically the physical outgoing power; do not count the same escaped energy both at an interior flux sphere and again as absorber removal in a single conserved total.

## 3. A reference remnant must exist before projection

Require an actual single surviving core, a common centre/rest frame, and a core charge/phase that is approximately stationary over the fitting interval. Exclude detached fragments and outgoing radiation from the bound-core inventory with a predeclared aperture/plateau diagnostic. A spherical reference with Q=160000 cannot be presumed if charge has escaped or the collision has not merged.

Use a same-action stationary reference at the measured bound charge and common carrier frequency, with one shared U(1) phase for Psi and X. The reference must match the evolution discretization or have a measured convergent interpolation/discretization error. Existing radial caches at Q80000/160000 are templates/seeds; their exact finite radial stationarity does not imply exact stationarity on a cylindrical grid. If no sufficiently close remnant reference exists, report an unsuccessful/inconclusive mode-excitation test rather than treating a strongly deformed two-core field as a linear oscillator.

In a frozen rest-frame fitting window, rotate Psi by exp(-i theta(t)) and X by exp(-2i theta(t)), theta_t=omega_ref. Define canonical residuals

    u=sqrt(2)[Re(Psi_rot)-f_ref], v=sqrt(2)Im(Psi_rot),
    s=sqrt(2)[Re(X_rot)-b_ref], t_X=sqrt(2)Im(X_rot),
    xi=chi-h_ref,

ordered `(u,s,xi,v,t_X)`. Derivatives must also be transformed: for example `Psi_rot,t=exp(-i theta)(Psi_t-i omega_ref Psi)` in the frozen rest frame. A moving centre, varying reference charge/profile or varying phase fit adds transport/family derivatives that must be removed or bounded. Independently fitting the X phase is not allowed.

For axisymmetric data the normalized angular coefficient is

    delta z_20(r)=2pi integral_-1^1 Y20(mu) delta z(r,mu)dmu,
    q(r)=r delta z_20(r), v(r)=r partial_t delta z_20(r).

Y20=sqrt(5/(16pi))(3mu^2-1). Here v denotes the full five-vector velocity in the projection formulas, not solely the phase component named v above. Spherical extraction needs declared interpolation/quadrature and a stable fit aperture. Alternatively evaluate the same inner products directly on the cylindrical grid with modal template Z(r)Y20/r and volume weight 2pi rho d_rho d_z.

## 4. Canonical symplectic projection

For the matched linearized radial problem,

    q_tt+G q_t+W q=0, G^T=-G, W^T=W,
    (W-Omega^2+i Omega G)Z=0.

Canonical momentum is p=q_t+Gq/2. For the complex mode, let P=(i Omega+G/2)Z and R=(Z,P). Use the complex bilinear symplectic form

    S((q1,p1),(q2,p2))=integral(q1^T p2-p1^T q2)dr.

The no-half energy normalization is

    kappa=integral[Omega^2 Z†Z+Z†WZ]dr,
    S(R*,R)=i kappa/Omega.

For real snapshot data `(q,v=q_t)`, the positive-time modal coefficient is therefore

    c=S(R*,(q,p))/S(R*,R)
      =-i Omega/kappa integral Z†[v+(G+i Omega)q]dr.

On a uniform reduced radial grid, use the same dr quadrature as the mode normalization. For the existing kappa=1 cache,

    c=-i Omega dr Z†[v+(G+i Omega)q],
    K_20=|c|^2,
    q_mode=c Z+c*Z*.

In a pure linear mode, c(t)=c0 exp(i Omega t). This formula includes velocity and the gyro term. A displacement-only L2 overlap is not the canonical mode amplitude and can misclassify a static ellipticity, a translated core or another oscillation as stored mode energy. The equivalent direct full-space expression uses the same ZY20/r template and cylindrical measure. It needs the matching reference operator/inner product, not an arbitrary rescaling of a different-grid template.

Required extraction controls: synthetic real and imaginary mode phases recover the prescribed c and K; a pure reference yields negligible c; a translated reference and a common phase/frequency perturbation do not produce a resolved physical ell2 excitation after recentering/gauge treatment; the isolated boosted/static evolution controls stay below the claimed collision signal. Test at least two independent snapshots/oscillation phases, and check the projected reconstruction against the original canonical field and velocity.

Nonlinear self-mixing creates a static ell2 component and a 2Omega ell2 response. Both can pollute an instantaneous c. Where a weak near-stationary remnant is available, fit the projected time series to its coherent fundamental plus a static offset and resolved harmonics, over several periods if the budget permits. Report residuals, window/aperture/reference sensitivity, frequency and amplitude drift. A short strongly nonlinear interval is only a raw projection diagnostic, not a measured persistent bound-mode energy. Real-harmonic bare charge can also contain oscillatory quadratic terms: total charge conservation belongs to the full fields, not a mode-only reconstruction.

## 5. Axisymmetric Y20 loss coefficient from the existing standing calculation

A head-on axisymmetric remnant excites m=0, not the earlier H=(Y22+Y2,-2)/sqrt(2) angular pattern. The exact normalized product is

    Y20^2=D0 Y00+D2 Y20+D4 Y40,
    D0=1/sqrt(4pi), D2=sqrt(5)/(7sqrt(pi)), D4=3/(7sqrt(pi)).

For a spherical background and the same unit-K radial mode, the outgoing response depends on ell but not m. D0 equals the earlier standing C0, D2=-C2, and

    D4^2=9/(49pi)=C4^2+C44^2/2.

Thus the **summed leading unit-K gamma is identical** to the existing standing-pattern gamma. This follows by matching the squared source weight in each ell sector; it does not require the two angular patterns to be related by a spatial rotation. All axisymmetric outgoing components have m=0 and J=0. The static/field angular profiles differ, so the previous chiral or H-pattern DC correction must not be reused unchanged as the Y20 correction.

The correspondence is conditional on the matched radial/background reference, weak amplitude and slowly varying single-mode reduction. If the measured collision leaves multiple strong modes, shifted thresholds or a substantially nonstationary remnant, applying one gamma to the entire collision energy is unsupported. No new outgoing solve is needed merely to change from this real standing angular pattern to Y20 under the stated hypotheses.

## 6. Energy sufficiency and permitted conclusion

Report actual E_initial and Q_initial, outgoing/removed E,Q, fitted bound-core charge, stationary reference energy, centre-motion debit and the residual excitation energy. For 80000+80000, the stationary binding difference `2E80000-E160000` is about2978.72488 in this action, but incoming kinetic energy and initial overlap are additional separate accounts. A measured mode energy must not exceed the compatible remnant excitation budget within errors, and no kinetic contribution should be relabeled as a demonstrated fraction of stationary binding energy.

For a verified weak mode, its measured K0 and matching gamma imply the conditional secular time `t_half=1/(gamma K0)`. The adiabatic rate condition includes gamma K0/Omega much less than one, and field-deformation, frequency-shift and threshold-margin checks are separate. If these fail, a linear projection can still be reported but the weak damping law cannot be extrapolated as a quantitative capture/cooling history.

A successful bounded pilot can establish: this specified same-action collision forms a remnant and excites a specified coherent quadrupole energy above matched single-fragment/grid artefacts. It cannot establish generic merger rates or phase distributions, conversion of galactic orbital J, physical action/mass units, cosmological fragment abundance, or sufficiency for Draco/Sextans while avoiding Fornax/Leo I. The latter requires the physical unit bridge, population/encounter histories, surviving stock and aperture/selection constraints. Preserve failure or nonmerger outcomes as evidence rather than changing the source/criteria after inspection.

## 7. Implemented analysis and bounded synthetic control

`pair_projection.py` implements `analyze_snapshot(snapshot, mode_path, profile_path, Qref=160000, ...)`. It reads the declared32-byte little-endian CEPAIR1 header and ten lab-field arrays, fits a shared carrier in a declared inner sphere, subtracts the correct charge-one/charge-two carrier velocities, and applies the symplectic formula above. Cubic or bilinear cell interpolation uses regular even reflection at rho=0 and rejects spheres outside the available grid. The gyro frequency remains pinned to the supplied mode; fitted/reference frequency mismatch and continuum-profile/finite-grid-background mismatch are reported explicitly.

The returned `conditional_K_coordinate` is |c|^2. It is deliberately not an automatic persistent-mode-energy claim. The reported reconstruction residual uses the positive state norm integral[Omega^2|q|^2+|v|^2]dr, not an asserted energy decomposition. Aperture charge fractions, a near-axis peak count and shared-phase/coherence diagnostics describe the snapshot; none automatically identifies bound mass or a merged core. Residual fractions are not informative when the entire extracted signal is at numerical noise level.

The predeclared `projection_synthetic_run_001` completed with28/28 passed checks and a validated v2 manifest. It generated no pair evolution: independent lab-frame snapshots contained a known c, the exact mode velocity, the common carrier phase .37, and a spherical reference. At dx=.2, two known |c|=.1 phases were recovered with relative complex-coordinate errors about1.04e-5; the dx=.4 comparison had error3.27e-4. The pure spherical negative control gave false |c|^2=1.08e-12. Carrier-frequency fit error in the perturbed controls was below5.6e-8. Peak measured RSS was219070464 bytes and retained synthetic snapshots totaled about53MB, below the declared1GB limits. These validate the interpolation/normalization/velocity pipeline for the supplied synthetic data, not its physical reference assumptions on a collision. Static/boosted evolution and actual-remnant acceptance controls remain required.
