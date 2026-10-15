# Independent audit of the moving finite interface

15 October 2026. Independent reconstruction by the dynamic-core agent, not the interface author. This is a same-team mathematical audit, not external peer review or formal verification. Scope: frozen `PROOF.md` plus the current-inertia `AMENDMENT.md`, `check_interface_v2.py`, its contract and `run_v2`. Verdict: **the constructive finite-ball equilibrium and positive all-radial fluid/wall quadratic energy are supported for the explicitly defined fixed-core Newtonian hybrid control**. They do not close the dynamical charged core, nonspherical interface modes, microscopic phase or Einstein theory.

Inspected frozen hashes:

- `PROOF.md`: `4de7bc8143986be100165af930232fcbfdc8d31781c30c361d21981027bfee64`.
- `AMENDMENT.md`: `63979a9b261e9962397d462521106fbd7d2fdc0397e896954c4c9a8615ab45bb`.
- `check_interface_v2.py`: `4f763a3118db1b729ee88d81dc8dba648d2e55dd10c7b25fc4bad1830fceae87`.

The Mathbox validator, run with the repository root, confirms the current v2 input/output hashes. The 32 exact-check output was inspected. The audit below derives the load-bearing equations independently; it does not mistake a valid manifest or finite check count for proof of the infinite-dimensional assertion.

## Hydrostatic existence is an actual bounded construction

For w<=w0, the density stays below rho0 and its derivative with respect to w is at most 5rho0/w0. Direct integration of the fixed uniform core gives the enthalpy drop G Mc/Rc(3/2-Rc/R); the neutral upper density gives 2piG rho0 R^2/3. This verifies the self-map bound, including the source regularity at zero. Applying the same integral kernel to a difference yields the stated Lipschitz constant 10piG rho0 R^2/(3w0). It is strictly below one for the assigned input. Thus a positive contracted hydrostatic solution exists on the whole closed ball and includes its own rest-mass gravity. No sampled profile has been substituted for it.

The prescribed central charge is counted independently of the prescribed central mass. In particular, the source is not asserted to have critical charge/mass or to satisfy its own force balance. All field and material profiles are regular at the center within the declared occupied branch. The charged body and neutral stock interpenetrate in this control; no excluded hard cavity is assumed.

## Moving-wall shape work includes the cross terms

At separately fixed Mc and Ms, spherical symmetry makes the wall interaction exactly -G m_w(R)(Mc+Ms)/R, independently of the interior neutral shape. With m_w=4pi sigma R^2/c^2 and the shell self-energy -G m_w^2/(2R), differentiating gives the wall pressure contribution

\[
 2\sigma/R-G\sigma(M_c+M_s)/(c^2R^2)-6\pi G\sigma^2/c^4.
\]

Its R derivative is -2sigma/R^2+2Gsigma(Mc+Ms)/(c^2R^3). The self-gravity load is constant in R because the specified wall mass scales as R^2. This is consistent with the stated energy model; holding the wall mass fixed during this derivative would define a different model. There is no missing independent wall/neutral density cross term on conserved-Ms spherical paths: the interaction depends only on Ms and R. The restoring form also contains the geometric pressure terms coming from fluid compression, so one must not compare its surface coefficient to V_w'' alone.

The occupied electric Hamiltonian satisfies dH/dD=E and has jump Delta H=D0^2[-x-log(1-x)-x^2/2]. At fixed actual Q, D_b varies as R^-2. Hence the electric boundary derivative is exactly -2D_b(E_in-D_b)/R. It has the correct sign in the potential form and is not an uncounted external pressure reservoir. Normal D is continuous, so no free surface charge is introduced; a jump of the normal E is compatible with the two constitutive phases.

The weak positive tension root is defined using the actual contracted boundary pressure, then held fixed during perturbations. The proof verifies that its load is positive and crossed on the increasing branch below sigma_test. Thus the wall is not assigned a homogeneous-fluid pressure as a surrogate.

## Full radial fluid/gravity/interface form

Starting from delta rho=-rho d-xi rho', delta P=-Gamma P d-xi P' and delta g_s=-4piG rho xi, substitute P'=-rho g and g'=4piG(rho+rho_c)-2g/r. The force reduces to

\[
 (\Gamma P d)'+\rho(4g/r-4\pi G\rho_c)\xi.
\]

This retains the core density term and neutral self-gravity; the sign agrees with the proof. The finite neutral density at the material edge does not require an extra uncounted bulk term: the Eulerian surface distribution from moving the edge is incorporated by the Lagrangian pressure variation and impermeability. Total Ms is fixed; the exterior neutral mass perturbation vanishes.

Integrating this force against r^2xi produces the displayed bulk potential form. The Lagrangian boundary condition -Gamma Pb d=P_ext' xi+sigma ddot xi/c^2 then gives precisely the surface restoring coefficient and positive wall inertia. Terms involving m_w'(R) dot R^2 are beyond the linearized rest background and do not add a missing quadratic kinetic term.

The amplitude-inertia distinction in `AMENDMENT.md` is necessary. For the inherited flat-space barotropic-current kinetic expansion, the fluid inertia is rho+6P/c^2, while the postulated Newtonian gravitational force remains the rest-density force. This is a consistent explicitly defined hybrid variational comparison. It is not the result of covariantly coupling that full stress tensor to an Einstein metric. The frozen proof's rho-inertia Rayleigh bound applies only to its narrower Newtonian kinetic convention. The amended enthalpy inertia gives the correct current-kinetic bound >43/1000; the old >46/1000 must not be quoted for it. The potential form and its positive coefficient are unchanged.

## Infinite-dimensional bound and assigned input

For d=xi'+2xi/r, regularity gives r^2xi=integral_0^r s^2d(s)ds. Cauchy-Schwarz gives xi(r)^2<=J_r/(3r). Integrating once and reversing the order yields integral xi^2r^2dr<=R^2J/6. These identities justify the trace and bulk estimates for the whole finite-energy radial form domain by approximation, rather than for a finite set of modes.

Using g<=Omega^2r, rho<=rho0 and P>=Pmin, dropping the positive core term and positive wall cross-gravity term gives exactly the lower coefficient C in the proof. Independent arithmetic agrees with the conservative rational value

\[
 C_{\rm lower}=92209711/11707031250
              =0.00787643844377\ldots>39/5000.
\]

The conservative full-current inertia cap is (1.06)/6+0.0051/3, giving (39/5000)/cap=234/5351>43/1000. The contracted density lower bound, actual positive tension root, finite wall mass upper bound and maximum occupied field x=1/250 all have strict margins. The principal gate is separately valid in its declared pure-electric occupied domain; it does not prove nonspherical or magnetic-interface stability.

## Scope, holders and flux

“Global” here means that this specified boundary-value model covers the center, the occupied finite ball, the moving material surface and the Maxwell exterior with finite counted masses and field energy. It does not mean that every physical component is dynamical or that a global covariant PDE theorem has been proved. The central mass/charge source is prescribed and held. Its forces may require substantial mechanical support. Since its positions and currents are static, its holder does no mechanical power in the present comparison, but the holder and charged-body force balance are absent from the claimed dynamical system. Their stability cannot be inferred from Q>0.

Neutral impermeability fixes its mass, and fixed Gauss charge excludes an uncounted charge flux. Spherical B is zero, so no independent radiative spherical electromagnetic mode is being discarded. Energy exchanged when the material phase moves is exactly the electric jump and wall pressure work already retained. Nonspherical radiation, surface currents, charge-carrying wall microphysics, tension/phase production and permeability need new equations.

Poisson gravity counts the specified rest masses, including the changing area wall mass and its self-gravity; it omits internal/gauge/kinetic gravitational sources and relativistic wall tension effects. Those omissions are explicit model choices, not Einstein junction identities. Under these limits the reciprocal spherical energy bookkeeping is sound. No claim of original-theory completion, parameter-free surface physics, full current/metric health or empirical viability follows.
