# ER2: conservative gravity can torque an irrotational field; the simplest cold smooth-bar wave channel is inefficient

This independent route audit finds a specific overstatement in DR5: Kelvin's theorem forbids production of circulation under its assumptions, but does **not** forbid gravitational torque or angular momentum transfer. An explicit pre-caustic continuum counterexample is derived and checked below. This correction does not rescue DR5's fitted rotation gate, its energy bookkeeping, or any galaxy fit.

A genuinely frequency-dependent route remains logically open: a rotating bar can launch field waves and transfer energy and angular momentum without creating circulation. For an ordinary barotropic field and a smooth Gaussian quadrupole, however, the outgoing-wave calculation gives a falsifiable obstruction: coupling to a cold field is exponentially suppressed when the forcing wavelength is much shorter than the source. Efficient coupling requires sound speed of order the bar's pattern speed times its radius. That same sound speed enters the static pressure response. An independently specified dispersive completion could separate those regimes; none is supplied here.

No contraction strength or mass-dependent selector is fitted, no SPARC curve is regraded, and no production simulation is run. Cold dark energy remains a gravitating field, never a particle. No stable halo carrier, complete theory or empirical preference is established. Base read: `c2bed2da878ab9843a5d121f0cf6f0315f08c1d4`, shared dirty tree; only this directory was written.

## What the field assumption does and does not permit

For the DR2 single timelike scalar with action density P(X),

\[
X=-\tfrac12\nabla_\mu\phi\nabla^\mu\phi,\quad
u_\mu=-\nabla_\mu\phi/\sqrt{2X},\quad
\rho=2XP_X-P,\quad
c_s^2=\frac{P_X}{P_X+2XP_{XX}}.
\]

The ordinary healthy barotropic branch requires positive P_X and P_X+2XP_XX. Its nonrelativistic flow obeys continuity and Euler equations with a single local velocity and pressure P(rho). The cold limit follows geodesic dust before caustics; that does not provide a phase-mixed halo after stream crossing. These are the assumptions of DR2, not a new identification with particles.

Young's action method instead requires a nonnegative distribution f(J_r,L), an orbit population, an equilibrium potential and sufficiently slow evolution. A classical multistream field completion might justify such a coarse-grained distribution without changing the owner's terminology, but this bridge has to be derived. It is absent for the bare single-valued scalar. LC1's N-body tracer results describe a collisionless response and cannot by themselves supply that bridge.

An additional orbit consistency test is available: a spherical cored equilibrium with finite central potential cannot have positive limiting central radial anisotropy, beta_0>0, within the usual nonnegative DF class, because gamma_0>=2 beta_0. This constrains a proposal to replace the core with a centrally radial equilibrium. It does **not** prohibit eccentric orbits in an isotropic core, constrain beta at every finite radius for arbitrary DFs, or exclude an exact action calculation. DR2's near-radial, still phase-mixing shell experiment is consequently not a ready-made equilibrium core model. [An & Evans, v4, Section 2 and Appendix](https://arxiv.org/pdf/astro-ph/0511686).

## The Kelvin implication fails at its last arrow

For a barotropic continuum with sufficiently decaying density or a free boundary, isotropic pressure exerts no net torque, and internal self-gravity cancels in pairs. Therefore

\[
L_z=\int\rho(xv_y-yv_x)\,d^3x,\qquad
\dot L_z=-\int\rho\,\partial_\varphi\Phi_b\,d^3x.
\]

There is no identity setting this expression to zero because the force is a gradient. It vanishes for an axisymmetric source/response or suitable phase alignment. A nonaxisymmetric, misaligned density need not have that cancellation. Kelvin instead gives conservation of the line integral of velocity around a material loop. Total angular momentum and circulation are different quantities.

A completely single-stream example uses pressureless Euler flow in the conservative potential Phi=x^T K x/2, with K having diagonal entries 1 and off-diagonal K_xy=K_yx=0.1. Begin at rest with a compact ellipsoidal density whose covariance is C_0=diag(4,1,1). One concrete choice is rho proportional to (1-x^2/36-y^2/9-z^2/9)^2 on its positive support. This is a continuous density with no orbit distribution or particle interpretation.

Before the first caustic the exact map and velocity are

\[
x=A(t)x_0,\quad A(t)=\cos(\sqrt K\,t),\quad
v=B(t)x,\quad B(t)=-\sqrt K\tan(\sqrt K\,t).
\]

A and B are symmetric functions of K; hence curl v=0 and v has the single-valued potential x^T B x/2. The transported covariance is C=A C_0 A^T. At t=0, L_z=0 but dot L_z=0.1(C_yy-C_xx)=-0.3 for unit mass. At t=0.5, L_z=-0.1381073084 and dot L_z=-0.2310156217, while curl remains zero. The first affine caustic is at t=pi/(2 sqrt(1.1))=1.497695533. The example only refutes 'no circulation implies no torque'; it is neither an equilibrium halo nor secular heating.

The force is a physically admissible local quadratic gravitational field: its trace gives positive external density and its off-diagonal harmonic part is an external tide. The compact support can be placed wholly inside the region where this local potential applies during the checked interval.

## A real absorption criterion, without an assumed damping coefficient

Linearize Euler-Poisson locally around density rho_0 and neglect background gradients. For Fourier convention exp(i k.x-i omega t), define delta rho=-chi Phi_b. The propagating branch has

\[
\chi(k,\omega)=\frac{\rho_0k^2}
 {c_s^2k^2-\omega_J^2-(\omega+i0)^2},\qquad
\omega_J^2=4\pi G\rho_0.
\]

The i0 is the outgoing retarded boundary condition, not a physical damping parameter chosen to produce a desired answer. Away from a real pole in a closed finite conservative system, the real susceptibility gives a reversible deformation with no sustained cycle-averaged absorption. A continuum of propagating outgoing waves can instead carry energy away. For a rotating m-fold perturbation, omega=m Omega_p,

\[
\overline P=\frac{\omega}{2}
 \int\frac{d^3k}{(2\pi)^3}|\Phi_{b,k}|^2\,\operatorname{Im}\chi,
\qquad \overline T=\overline P/\Omega_p.
\]

This homogeneous calculation is **not** a global halo solution. Long-wavelength Jeans-unstable modes must be excluded from this stationary propagating-wave calculation, and a stable equilibrium, mode spectrum, boundary and absorption/escape prescription must be furnished before applying it to a halo. In particular, a pressureless static homogeneous medium does not become a supported halo by writing this Green function.

For a concrete smooth m=2 source, take the infinitesimal baryonic density quadrupole

\[
\delta\rho_b=\operatorname{Re}\left[
 \frac{\epsilon M_b}{(2\pi R^2)^{3/2}}
 \frac{(x+iy)^2}{R^2}\,e^{-r^2/(2R^2)}e^{-i\omega t}
 \right].
\]

This is a linear perturbation, not a proposed full signed baryon density; it arises at first order from a deforming positive Gaussian source. Its potential Fourier amplitude is

\[
\Phi_{b,k}=4\pi G\epsilon M_bR^2
 \frac{(k_x+ik_y)^2}{k^2}e^{-k^2R^2/2}.
\]

The propagating pole is

\[
k_*^2=(\omega^2+\omega_J^2)/c_s^2,\qquad K=k_*R.
\]

Using Im chi=pi rho_0 k^2 delta(c_s^2 k^2-omega_J^2-omega^2) for omega>0 and the angular integral integral sin^4(theta) dOmega=32 pi/15 gives

\[
\boxed{\overline P=\frac{16\pi}{15}
 G^2\epsilon^2M_b^2\rho_0\,\omega R^4
 \frac{k_*^3}{c_s^2}\,e^{-K^2}.}
\]

At fixed frequency, density and source, all sound-speed dependence is proportional to

\[
W(K)=K^5e^{-K^2},\qquad K_{\rm peak}=\sqrt{5/2}.
\]

For omega_J=0 this peaks at c_s=2 Omega_p R/sqrt(5/2). Nonzero self-gravity raises K; once K exceeds the peak, it further suppresses this channel at fixed c_s. If q=Omega_p R/V>=0.5 and c_s/V<=0.1, then K>=10 and W/W_peak<=10^(-38.33856)=4.59e-39. Those inequalities are a falsifiable conditional discriminator, not measured pattern speeds. For q=1 and c_s/V=0.3 the ratio is still 10^(-15.09155); at c_s/V=1 it becomes 0.723.

The Gaussian's exponential tail is source dependent. Sharp structures or small clumps have a different Fourier spectrum; this is not a universal bound for all bars or a replacement for the clump audit. Collisionless orbital resonances use an entirely different response kernel and are not constrained by this acoustic calculation.

The same low-frequency P(X) theory supplies both this c_s and the static derivative dP/d rho. Thus raising c_s toward a spiral's characteristic speed is not a new mechanism evading the existing static pressure objection. A field with independently derived dispersive, nonlocal or additional dynamical terms might have a different finite-frequency spectrum; its action, stability, scales and cold cosmological limit would have to be specified first. Replacing i0 by a fitted gamma and declaring heating would assume precisely the missing absorption.

## Finite bar budget and the dwarf requirement

For a fixed-shape rotating perturbation, partial_t Phi_b=-Omega_p partial_phi Phi_b, so the exact exchange relation is dE_h=Omega_p dL_h. A finite bar must pay both quantities. In a rigid bar of fixed moment I, the available slowdown energy is I(Omega_i^2-Omega_f^2)/2 and available angular momentum is I(Omega_i-Omega_f). A time-varying amplitude/shape adds explicit work terms and has to be included in the baryon evolution; a prescribed forever-rotating potential is an external power supply.

A real candidate must independently compute, on the **same** halo/baryon baseline,

\[
\int\overline P\,dt\ge\Delta E_{\rm required},\qquad
\Delta L_h\le L_{b,i}-L_{b,f}
\]

with all material inflows, outflows and other angular-momentum reservoirs included if present. It must also predict a sufficiently small change in the dwarf response. No energy-only rank ordering supplies that mass dependence. In the smooth-wave approximation, fixed c_s and q make K increase with V, so the spectral overlap on the cold tail becomes worse in large spirals; the full heating rate also has source-dependent prefactors and has not been graded here.

DR5's existing all-disc rotation-energy bookkeeping has median T_rot/E_undo=0.61335 and 0.75082 in the 150–200 and 200–250 bins. That is already short of complete undo in that prescription before allowing for finite bar fraction and retention of stellar rotation. It is not a theorem excluding all partial secular evolution or changing bar inertia/baryon binding energy. ER1's required undo fractions use a different native-profile baseline and are deliberately **not** multiplied by these DR5 ratios.

BT1 also shows the present unbarred classified subset misses the Upsilon line (0.38/0.38 with contraction), so a mechanism requiring a present bar in every failing spiral is contradicted by that limited classification. Past bars, spirals, other nonaxisymmetric history and unclassified objects are separate inputs, not a derived escape.

## What was checked, and what remains

[quadrupole_check.py](quadrupole_check.py) verifies exact affine continuum moments, an independent compact-ellipsoid volume quadrature, zero curl, nonzero torque, finite-difference Ldot against torque, the outgoing source's angular normalization, the analytic peak and a 14-cell dimensionless spectral table. The greatest Ldot/torque absolute discrepancy is 1.41e-11; compact-ellipsoid torque is -0.29999999999999954. This is a bounded diagnostic, not a halo simulation. [Result](run_001/result.json), [manifest](run_001/manifest.json) and [contract](contract.json) record the assertion, versions, input hash and unchanged input. Status completed; manifest validation passed. The proof and interpretation are self-reviewed within this independent route audit; no fresh second reviewer has checked the Fourier normalization.

Regeneration command, with a new run directory and the script's result path changed together for a new run:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract /Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/ER2_response_theory/contract.json --input rebuild_2026_10_22/ER2_response_theory/quadrupole_check.py --output rebuild_2026_10_22/ER2_response_theory/run_001 --result rebuild_2026_10_22/ER2_response_theory/run_001/result.json --timeout 20 --max-output-bytes 65536 --max-cpu-seconds 15 --max-threads 1 -- python3 rebuild_2026_10_22/ER2_response_theory/quadrupole_check.py
```

Read-only inputs included DR2, DR3, DR4, DR5, DR7, LC1, CR1, the cold-sector specification, ER1, BT1 and the November 1 spin/contraction report. No existing verdict or source was edited. In particular, no simple rotation gate, conserved-charge gate, orbit-count gate or phase-space cap is being reopened under a different name.

The cheapest decisive next input is a **specified field action and stable halo background**, yielding its retarded m=2 susceptibility or mode spectrum, together with a measured/independently modeled bar history. If it reduces to the ordinary cold barotropic kernel and a smooth source, the derived cold-tail test applies immediately. If it gives a different propagating or absorptive response, that change is the physical claim to audit before a long run. Present evidence establishes a correction to an overbroad torque statement and a conditional obstruction for one honest field-wave realization; it does not establish a solution to spiral contraction.

## Primary-source checks

- [Sellwood & McGaugh, astro-ph/0507589v1, July 26 2005](https://arxiv.org/pdf/astro-ph/0507589), Section 3: checked the stated invariance f_0(J_r,L)=f_n(J_r,L), radial-action/energy inversion and iterative density/potential construction. Application is conditional on a collisionless-type DF or an independently justified multistream field limit. This is distinct from assuming a fitted overall response strength.
- [Gnedin et al., astro-ph/0406247v2, December 15 2004](https://arxiv.org/pdf/astro-ph/0406247), introductory model and improved invariant: checked that the orbit-averaged prescription is an empirical correction for eccentric particle orbits, rather than a new conservation law forbidding compression. It is already present in DR3 and does not supply the missing field completion.
- [An & Evans, astro-ph/0511686v4, March 27 2006](https://arxiv.org/pdf/astro-ph/0511686), Section 2 and Appendix: checked gamma_0>=2 beta_0, its finite-potential assumptions and the constant-anisotropy density integral. Only the central constraint stated above is imported.
- [Goldreich & Nicholson, published 1989, DOI 10.1086/167664](https://authors.library.caltech.edu/records/ytmkh-p0496): authenticated the primary archive metadata and its stated abstract result that an inviscid fluid may receive an external tidal torque while waves transport angular momentum. Full PDF fetch failed, so its detailed theorem is **not** a verified dependency. The torque counterexample and wave calculation above are direct derivations.

Checked November 1, 2026. No fetched full text was retained in the repository and no novelty claim is made. No `.mathbox` ledger evidence was recorded. Source authentication, extraction and conditional application are distinguished above.
