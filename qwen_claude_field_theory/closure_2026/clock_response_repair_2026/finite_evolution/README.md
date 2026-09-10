# Finite-scale test → a constructive entropy-clock dust branch

Base commit: `e17368494d7c5a9144168ca60e7024f18bb02036`. Full-theory objective remains **OPEN**.

**New result:** replacing K(Q) by an explicitly clock-dependent K(Q,τ) admits a reconstructed sector with an exact dust+Λ background, vanishing *linear* total pressure perturbation for every regular finite spatial mode, independently derived equal Newtonian-gauge potentials, and a positive quadratic scalar kinetic coefficient. The construction has a closed-form kinetic profile. It introduces no particle-CDM species; its clock/χ stress nonetheless behaves as an effective dark dust component. This is not yet MOND or a complete theory of gravity.

Carl Zimmerman supplied the primordial-clock direction and the requirement to preserve a global a₀. The calculations below develop that suggestion. The profile is a project construction; no literature-priority claim is made. κ=1/2 remains fitted, and the exponential MOND kernel has not been derived from this sector.

## What the finite-scale test actually found

[evolve.py](evolve.py) derives first-order evolution from the previous quadratic Hamiltonian, retains time-dependent constraint terms, and reconstructs Φ and Ψ separately. Canonical equations, their pressure-trace equivalent, the comoving Poisson identity and a cold Einstein–de Sitter control are checked symbolically. The actual evolved variables are Ψ and dΨ/dln a; poorly conditioned clock-gauge coordinates are not used for integration.

Thirty-six runs compare the repaired K(Q) branch and its r=1 control at three clock amplitudes and six wavenumbers. The imposed initial conditions are Ψ=−1, Ψ'=0 at a=10⁻³, integrated to a=1. They are not primordial adiabatic initial conditions. The comparator is GR pressureless matter+Λ matched to the same present H, not an empirical likelihood.

For the original m=10⁻⁵ example, the final potential ratios to that comparator are approximately 0.999, 0.858, 0.189 and −0.00415 at k/H₀=1,10,30,100. Raising m to 0.0019 does not restore dustlike transfer in this tested family. Three cross-method, tighter-tolerance comparisons agree to about 2×10⁻¹¹ in potential. This is a real finite-scale failure of the illustrative model, not evidence against every clock theory or an observational rejection statistic.

The fixed K(Q) inverse test [inverse_clock.py](inverse_clock.py) tries freeing the clock history at the r=0 boundary. It cannot cancel both pressure responses generically with that single history derivative. This motivated **a changed action**, not further scanning of the same coefficients.

## Explicit new action and background

Use signature −+++, c=1, M²>0 and Λ>0. Let

\[
S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
+U(\tau)\sqrt{-\nabla\tau\cdot\nabla\tau}-V(\tau)
+K(Q,\tau)-C(Q,\tau)Y\right],
\]

\[
n_\mu=-\frac{\nabla_\mu\tau}{\sqrt{-\nabla\tau\cdot\nabla\tau}},\quad
Q=n^\mu\nabla_\mu\chi,\quad
Y=(g^{\mu\nu}+n^\mu n^\nu)\nabla_\mu\chi\nabla_\nu\chi.
\]

K depends on τ but not χ, so the homogeneous charge equation still gives A=K_Q=I/a³. What changes is crucial: Qdot is **not** fixed by −3HA/K_QQ. The clock can exchange energy with χ while ordinary minimally coupled matter, when added, need not acquire a nonmetric coupling. Ordinary-matter perturbations have not been included in this computation.

Choose positive constants I,Q_c,m₀,L and define functions along the background clock τ=t:

\[
m=m_0a^2,\quad q=\frac{Q_c}{1+m},\quad A=Ia^{-3},\quad
\rho_d=Q_cIa^{-3},\quad H^2=\frac\Lambda3+\frac{\rho_d}{3M^2},\quad
U=V=mqA.
\]

Here q is the **background value** of the action argument Q. Define R_Λ=ΛM²/(Q_cI), Ω=1/(1+R_Λa³). These are genuine functions of the scalar clock: for example the expanding branch is explicitly

\[
a^3(\tau)=R_\Lambda^{-1}\sinh^2\!\left[\tfrac12\sqrt{3\Lambda}(\tau-\tau_B)\right],\qquad \tau>\tau_B.
\]

This reconstructs functions in a covariant action; it does not derive the chosen clock history or its constants microphysically.

The new constitutive law is

\[
K(Q,\tau)=A(\tau)[Q-q(\tau)]+\frac{B(\tau)}2[Q-q(\tau)]^2,
\qquad
C(Q,\tau)=\frac{K_Q(Q,\tau)^2}{2[QK_Q(Q,\tau)+U(\tau)]}.
\]

The construction is restricted to a neighborhood with timelike clock, K_Q>0 and QK_Q+U>0. It does not certify all off-background field values. The coefficient C is the r=0 boundary of the prior inverse family, now with a changed K. Its vanishing UV gradient is intentional and must not be mislabeled strictly positive sound speed.

The background has K=0, ρ_χ=qA, ρ_τ=U, and ρ_χ+ρ_τ=ρ_d. The code checks the clock background equation Vdot=K_τ−3HU and exact combined dust conservation. χ and the clock exchange energy; they are not separately asserted to be conserved fluids.

## How B is constructed rather than fitted

[inverse_entropy_clock.py](inverse_entropy_clock.py) recomputes the clock constraint by canonical preservation. In particular, its extra term (Qdot+3HA/B)p_σ is retained; copying the old K(Q) constraint fails the independent no-slip test.

At finite k, requiring the two coefficients of δP_total to vanish fixes a first-order equation for B. Its solution is independent of k. With N=ln a and

\[
e=\frac{\dot q}{H}+\frac{qU}{2M^2H^2},\quad
v=-\frac{Be}{3A},\quad m=m_0a^s,
\]

the inverse equation reduces to

\[
v'=v(v-1)\frac{3\Omega s-3\Omega+2s^2-4s}{2s-3\Omega}.
\]

Choosing s=2 gives the explicit solution

\[
\boxed{v(a)=\frac{1+4R_\Lambda a^3}{1+(4R_\Lambda+L)a^3},\qquad
B(a)=-\frac{3A(a)v(a)}{e(a)}}.
\]

For a>0, R_Λ≥0 and L>0, 0<v<1. Moreover

\[
e=\frac{qm}{1+m}\left(\frac32\Omega-2\right)<0,\quad
B>0,\quad f:=Be+3A=3A(1-v)>0.
\]

[entropy_health.py](entropy_health.py) differentiates the profile, verifies the inverse equation, and checks 37 epochs over 10⁻⁶≤a≤10³ using 70-digit arithmetic. Each epoch also checks three finite-wavenumber kinetic coefficients. Factored/high-precision expressions are needed because v approaches one closely at early times. This sampling is a numerical cross-check; the profile interval and sign implications have a separate algebraic argument.

The combined linear pressure response vanishes for every regular finite k, not merely in the short-wavelength limit. Since the independently reconstructed potentials satisfy Φ=Ψ, the **sector-only linear** Einstein pressure equation is the dust+Λ potential equation. This is not a PPN γ calculation, not a galactic MOND lensing result, and not a radiation-era CMB calculation.

## Fresh action and constraint checks

[entropy_quadratic.py](entropy_quadratic.py) expands the new K(Q,τ) action in ADM variables before reduction. It verifies the full finite-k quadratic action with independent Qdot. Its reduced kinetic coefficient is

\[
\mathcal K(k)=B-\frac{f^2}{ef-(k^2/a^2)D/H^2},\qquad
D=\frac{qA m^2}{1+m}>0.
\]

The established B>0, e<0, f>0 imply positive kinetic energy for every regular finite k. The quadratic gradient is pressureless, not a strictly hyperbolic positive-sound-speed wave. This does not settle nonlinear strong coupling, dust caustics or physical instantaneous response.

The reduced finite-k primary and secondary constraints have a computed two-by-two bracket matrix of rank two, with coefficient a³[3Af/B+(k²/a²)D/H²]>0. Thus that reduced scalar system has one canonical pair, openly associated with the clock/χ matter sector; no zero-DOF auxiliary count is claimed for χ.

At k=0, the independent homogeneous tertiary contains Qdot+3HA/B. Its constraint-basis determinant is H²f/B>0 on the constructed branch, allowing reduction to the homogeneous basis checked in the script. The computed four-by-four matrix has rank four. This controls the linear homogeneous sector on the regular background; the nonlinear gravitational constraint algebra and limiting singular endpoints are still open. No constraint enforces H=0.

Three Lean statements certify the profile interval, rational flow identity and positive B,f implication. The profile's derivative and its reduction from the action are checked in SymPy, **not** formalized in Lean here. The installed calculus imports failed due to conflicting cached declarations; no package replacement or system change was attempted.

### All-wavelength formal extension

[AllScales.lean](AllScales.lean) adds four successfully compiled theorems: the background e is negative for q,m>0 and Ω≤1; the kinetic denominator is negative and 𝒦(k)>B>0 for every p=k²/a²≥0 under B,f,H,D>0 and e<0; the finite-k bracket coefficient and its squared determinant are positive; and the independently derived homogeneous constraint-basis determinant is positive. Together with the profile file, these are **seven new conditional Lean algebra certificates**, not a formalization of the entire action.

[check_all_scales.py](check_all_scales.py) eliminates ζ from the reduced action, computes the actual velocity Hessian, and verifies the exact formula used by Lean against a separate Schur-complement calculation. It also verifies D=qAm²/(1+m) from the constructed constitutive coefficient. This closes the quadratic formula-to-sign gap for all wavelengths, rather than relying on the 111 sampled signs. The p=0 value of the finite-k formula is only its formal limit; the homogeneous action retains its separate check above.

## Remaining requirements and next calculation

This is a constructive field-based dust sector, not the full requested theory. It does not yet derive the exponential MOND law, a₀–Λ coefficient, nonlinear N_grav=2, galactic no-slip, full PPN, nonlinear stability or joint empirical fits. In particular, adding a MOND operator from another file invalidates inherited health claims until the combined action is varied again.

The next two calculations are specific: (1) include separately varied radiation and baryons and recompute the clock response, including the radiation-era background and isocurvature modes; (2) derive the cubic action and nonlinear constraints on a spatially inhomogeneous χ background. Both are necessary before connecting this sector to a MOND geometry operator. A linear pressureless mode may develop caustics or pathological strong coupling; positive quadratic kinetic energy does not rule those out.

There are no empirical data or newly validated observational predictions in this checkpoint. The action functions are reconstructed, not all derived from first principles. The original full-theory goal remains active.

## Reproduction, provenance and failed attempts

Run [run_checks.py](run_checks.py) with a fresh `--result-file` path. The bounded computation record contains exact commands, environments, source hashes, exits and complete outputs. It includes the previous 67-check action regression and its five Lean certificates separately; their physical conclusions are not transferred to this changed action.

For the complete ten-case checkpoint use [run_certificates.py](run_certificates.py) with a fresh `--result-file` path. `run_001` records the original eight-case checkpoint; `run_002` adds the action-to-Lean bridge and four all-wavelength theorems while rerunning all eight original cases. Each manifest hashes its declared inputs; no input of `run_001` was changed by the all-wavelength extension.

Development failures were informative and are not hidden: integration in clock-gauge coordinates was interrupted because of poor numerical conditioning; the exact r=1 control needed symbolic specialization to avoid floating-point cancellation; the first K(Q,τ) draft incorrectly reused the old tertiary and failed its no-slip check; a generic symbolic matrix inverse was interrupted and replaced by testing pressure coefficients directly; the new spatial integration-by-parts check caught a missing d(k²/a²)/dt term. The final checks retain independent canonical, metric and pressure identities. The initial Lean calculus import failed; only the three successfully compiled algebra statements are counted.

Math proofreading covered these new equations and their hypotheses. The research-program workflow kept the full objective intact while the failed fixed-K route led to the constructed clock-dependent one; the computation-audit workflow records evidence without calling exit zero a theory certificate.
