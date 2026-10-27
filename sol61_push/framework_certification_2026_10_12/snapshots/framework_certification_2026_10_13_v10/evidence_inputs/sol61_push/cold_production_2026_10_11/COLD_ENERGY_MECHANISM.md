# Cold energy mechanism and proposed microscopic framework

Research synthesis dated 12 October 2026. This account combines the carrier, production, force-generation and dynamical calculations in this research lane. It is a candidate framework with explicit missing connections, not a completed unified theory or an experimental discovery.

The strongest result is a division of the problem into two calculable mechanisms. A charge-conserving scalar interaction can convert prepared sources into massive, low-pressure excitations without violating energy conservation. Separately, a proposed fermion medium generates a positive cubic polarization energy and a passive dynamical response. That response can produce an additional inverse-radius force, but its mass dependence changes between controlled regimes. The framework does not yet derive the existence of the medium, connect it to the scalar carrier, or fix the vacuum-linked acceleration scale.

## Physical meaning and target

“Cold energy” here means energy carried predominantly as rest mass, with small material pressure relative to energy density. It does not mean negative temperature, negative energy, or a source of energy without an input. Low pressure at production also does not establish cosmological cold dark matter: free streaming, abundance and structure formation must be calculated.

The galactic target is

$$
g_b(r)=\frac{G_NM_b(<r)}{r^2},\qquad
g_{\rm target}=\nu(g_b/a_0)g_b,
$$

with the deep-acceleration behavior

$$
g_{\rm target}\simeq\sqrt{a_0g_b},\qquad
V_f^4=G_NM_ba_0.
$$

The repository proposes

$$
a_0=\kappa c\sqrt{G_N\rho_{\rm DE}},\qquad \kappa=\tfrac12,
$$

where rho_DE is mass-equivalent vacuum density. In this research lane that normalization is a target input, not a derived result. The full repaired interpolation kernel is recorded in [the earlier carrier equation document](COLD_ENERGY_EQUATIONS.tex); the new force calculations do not derive that kernel.

## Components and notation

Natural units hbar=c=k_B=1 apply to microscopic equations unless SI units are stated. In the nonrelativistic medium, v is a band velocity and need not equal the speed of light.

| Symbol | Meaning |
|---|---|
| Phi, X | Complex daughter and source carrier fields, charges one and two |
| m, M, g_c | Daughter mass, source mass and source-conversion coupling |
| u_*, Delta_c | Daughter momentum divided by m, and M^2-4m^2 |
| psi, b | Nonrelativistic daughter and source annihilation fields |
| varphi, P | Additional scalar force potential and vector polarization |
| C, q_b | Positive force-sector stiffness and baryonic scalar coupling |
| Psi, m_*, k_0, v, h | Fermion field and parameters of its nodal-ring Hamiltonian |
| beta_3 | Coefficient of the generated cubic polarization potential |
| Z_varphi, I_P | Positive bare time-kinetic coefficients of the force fields |
| Phi_N | Ordinary Newtonian gravitational potential |

The notation avoids collisions in the earlier notes: their carrier phi becomes Phi, their force phi becomes varphi, their force stiffness a becomes C, their baryonic coupling alpha becomes q_b, and their cubic beta becomes beta_3. The carrier coupling ratio is called r_lambda below. No parameters from the two sectors are identified by these renamings.

## Charge protected scalar carrier

Choose positive m, Delta_c and lambda_rep, with

$$
M=2m\sqrt{1+u_*^2},\quad
\Delta_c=M^2-4m^2=4m^2u_*^2,\quad
\lambda_{\min}=g_c^2/\Delta_c,\quad
\lambda_{\rm tot}=\lambda_{\min}+\lambda_{\rm rep}.
$$

The proposed relativistic carrier Lagrangian is

$$
\mathcal L_c=\partial_\mu\Phi^*\partial^\mu\Phi+
\partial_\mu X^*\partial^\mu X-V_c,
$$

$$
V_c=m^2|\Phi|^2+4m^2|X|^2+
\left|\sqrt{\Delta_c}X+\frac{g_c}{\sqrt{\Delta_c}}\Phi^2\right|^2
+\lambda_{\rm rep}|\Phi|^4.
$$

With metric signature (+---), its field equations are

$$
(\Box+m^2)\Phi+2g_cX\Phi^*+2\lambda_{\rm tot}|\Phi|^2\Phi=0,
\qquad (\Box+M^2)X+g_c\Phi^2=0.
$$

The transformation (Phi,X) to (exp(i theta)Phi,exp(2i theta)X) preserves the action. The conserved charge and positive-square potential give E greater than or equal to m|Q| in the stated isolated, nongravitating classical theory. They do not permit extracting unlimited kinetic energy by repeated source conversion.

At a fixed finite regulator the leading nonrelativistic Hamiltonian has a stronger operator statement. Define

$$
\delta=M-2m,\quad c_3=\frac{g_c}{2m\sqrt{2M}},\quad
k_c=\frac{\lambda_{\rm tot}}{4m^2},\quad
Q=\int(\psi^\dagger\psi+2b^\dagger b)\,d^3x.
$$

Then H=mQ+D_c, with

$$
D_c=T+\int\delta\left(b+\frac{c_3}{\delta}\psi^2\right)^\dagger
\left(b+\frac{c_3}{\delta}\psi^2\right)d^3x
+\left(k_c-\frac{c_3^2}{\delta}\right)\int\psi^{\dagger2}\psi^2d^3x,
$$

$$
k_c-\frac{c_3^2}{\delta}
=\frac{\lambda_{\rm rep}}{4m^2}
+\frac{g_c^2}{8m^2M(M+2m)}>0.
$$

Consequently 0 <= <T> <= <D_c>. For N initially resting sources, Q=2N and D_c=delta N, so the initial excess-energy fraction is delta/(2m), approximately u_*^2/2. This regulated result is not a continuum quantum-field-theory proof. Adding gravity or another interacting sector requires accounting for its energy; the carrier-only bound cannot automatically be transferred to the combined system.

Here the nonnegative kinetic operator is

$$
T=\int\left[\frac{|\nabla\psi|^2}{2m}+\frac{|\nabla b|^2}{2M}\right]d^3x.
$$

The interaction-inclusive volume-averaged pressure bound is also available. Put r_c^2=c_3^2/(delta k_c)<1 and

$$
b_\pm=\frac12\left(1\pm\frac1{\sqrt{1-r_c^2}}\right),\qquad
d=\frac{\langle D_c\rangle}{m\langle Q\rangle}.
$$

Under the fixed-regulator homogeneous-expansion assumptions,

$$
b_-D_c\le PV\le b_+D_c,\qquad
\frac{|P|}{\rho_E}\le\frac{b_+d}{1+d}.
$$

Here P is scalar material pressure, distinct from the bold polarization vector. This is not a sound-speed or perturbation-transfer-function bound. Derivations and assumptions: [quantum energy](NR_QUANTUM_BOUND.md) and [quantum pressure](NR_QUANTUM_PRESSURE.md).

## Production and scattering

A resting source can decay into two daughters with

$$
p_*=m u_*,\quad
v_*=\frac{u_*}{\sqrt{1+u_*^2}},\quad
\frac{P_{\rm free}}{\rho_E}=\frac{u_*^2}{3(1+u_*^2)},
$$

$$
\Gamma_c=\frac{g_c^2}{8\pi M}\sqrt{1-\frac{4m^2}{M^2}},
\qquad \tau_c=\hbar/\Gamma_c.
$$

The decay transfers energy already stored in the source. Preparing the source and its charge is an unresolved physical input. A finite Hermitian source–pair model gives daughter-pair probability 0.9999549 after ten nominal lifetimes at its finest tested grid, while conserving total probability and Hamiltonian energy. This is a one-source resonant-band calculation, not a cosmological yield or many-source field solution. See [unitary production](DILUTE_UNITARY_DECAY.md).

Away from the source pole, the tree-level scattering screen uses

$$
x=\frac{s-4m^2}{\Delta_c},\quad
\lambda_{\rm eff}=\lambda_{\min}\left(r_\lambda-\frac{x}{1-x}\right),\quad
r_\lambda=\lambda_{\rm rep}/\lambda_{\min},
$$

$$
\sigma_0=\frac{\lambda_{\rm rep}^2}{8\pi m^2},\qquad
\frac{\sigma(s)}{\sigma_0}
=\left(\frac{\lambda_{\rm eff}}{\lambda_{\rm rep}}\right)^2\frac{4m^2}{s}.
$$

A bare pole cannot be integrated as a physical collision rate. The resonance requires finite-width treatment, and real-source conversion must not be counted a second time as a separate process in the same inclusive rate.

The revised screening benchmark is m=1 MeV, u_*=0.02, r_lambda=2 and sigma_0/m=0.3 cm^2/g. It gives g_c about 2168 eV, lambda_tot about 0.00881292, lifetime about 3.52096e-13 seconds, and free pressure/energy about 1.33280e-4. Its daughters initially move at about 0.02c. A specified running-width and Maxwell-distribution calculation gives effective cluster scattering about 0.28761 cm^2/g at mean relative speed 1900 km/s.

This branch was chosen after the larger cross section encountered a cluster constraint. It is not an independent prediction or a globally allowed dark-matter model. The earlier 4 cm^2/g halo simulations and the older unitary-production benchmark must not be relabeled as calculations of the revised branch. Source epoch, abundance and free streaming are still missing. See [the resonance audit](empirical_2026_10_12/RESONANCE_FOLLOWUP.md).

## Why ordinary carrier evolution did not finish the mechanism

The dilute carrier's Newtonian starting equations are a kinetic equation and Poisson equation,

$$
\partial_t f+\mathbf v\cdot\nabla_x f-
\nabla\Phi_N\cdot\nabla_v f=C_{22}[f],\qquad
\rho_c=m\int f\,d^3v,
$$

$$
\nabla^2\Phi_N=4\pi G_{\rm grav}(\rho_b+\rho_c)
$$

for the original carrier-only Newtonian model. Elastic collisions conserve local mass, momentum and kinetic energy. Their redistribution of energy does not select a universal halo normalization by itself.

The performed isolated formation, gas-cycle and rotating-source tests did not select the target profile. Some configurations gained energy; others cooled because the source history and orbital phases mattered. Distinct initially settled halos retained substantial profile differences. A fixed rotating driver could demand more angular momentum than its nominal reservoir. These are failures of the tested finite setups, not a proof that cosmological assembly cannot work. Evidence: [formation](HALO_FORMATION.md), [settled halos](mechanism_2026_10_12/SETTLED_HALO_RESULT.md), and [torque](mechanism_2026_10_12/TORQUE_RESULT.md).

This motivates investigating an additional response field. It does not justify inserting the target halo density into the kinetic equation and calling it a prediction.

## Additional force sector and its microscopic candidate

A phenomenological force sector uses

$$
\mathcal L_{\varphi P}=
\frac{Z_\varphi}{2}\dot\varphi^2+\frac{I_P}{2}|\dot{\mathbf P}|^2
-\frac C2\left|\nabla\varphi-\frac{\mathbf P}{C}\right|^2
-q_b\rho_b\varphi,
$$

with C,Z_varphi,I_P positive. Extra counterterms and the fermion determinant complete this candidate effective action. The square makes a particular critical relation between quadratic coefficients explicit; no symmetry has yet been shown to protect it.

The new fermion Hamiltonian is

$$
H_F=\frac{k_x^2+k_y^2-k_0^2}{2m_*}\Gamma_1
+vk_z\Gamma_2+h\sum_{j=1}^3P_j\Gamma_{j+2},
\qquad \{\Gamma_i,\Gamma_j\}=2\delta_{ij}.
$$

An explicit four-component representation is Gamma_1=sigma_x tensor 1, Gamma_2=sigma_z tensor 1, and Gamma_3,4,5=sigma_y tensor (sigma_x,sigma_y,sigma_z). The eigenvalues are

$$
E_\pm=\pm\sqrt{q_1^2+q_2^2+\Delta_f^2},\quad
q_1=\frac{k_x^2+k_y^2-k_0^2}{2m_*},\quad
q_2=vk_z,\quad \Delta_f=h|\mathbf P|.
$$

At P=0 the bands touch on a momentum-space ring. Assume N=2 filled negative-energy bands, zero temperature and chemical potential at that touching energy. For an energy tube Lambda below k_0^2/(2m_*), define A=N m_*/(2 pi v). Integrating the occupied bands gives

$$
V_F(\Delta_f)-V_F(0)=
-\frac A3\left[(\Lambda^2+\Delta_f^2)^{3/2}-\Lambda^3-|\Delta_f|^3\right].
$$

After subtracting the analytic quadratic term, the leading nonanalytic term is

$$
V_{F,\rm ren}=\frac{\beta_3}{3}|\mathbf P|^3+\cdots,
\qquad \beta_3=Ah^3=\frac{Nm_*h^3}{2\pi v}>0.
$$

The cubic sign and coefficient are calculated consequences of this band model. The quadratic counterterm, existence of the medium, occupation state, and symmetry protection of the ring are separate assumptions. The cubic term is not also added as an independent bare interaction when retaining the same fermions; that would double-count its contribution.

Before eliminating the fermions, the force-sector equations can be written as

$$
i\partial_t\Psi=H_F(-i\nabla,\mathbf P)\Psi,\qquad
Z_\varphi\ddot\varphi-\nabla\cdot(C\nabla\varphi-\mathbf P)=-q_b\rho_b,
$$

$$
I_P\ddot P_j+P_j/C-\partial_j\varphi
+h\langle\Psi^\dagger\Gamma_{j+2}\Psi\rangle
+\frac{\delta E_{\rm counterterms}}{\delta P_j}=0.
$$

The expectation value requires the specified fermion state and regulator. Replacing it by a local cubic derivative or a retarded linear kernel is an approximation to these equations, not an additional independent force. Live baryons would require their own coupled equations; the fixed-source calculations prescribe rho_b.

The Hamiltonian is local as a nonrelativistic differential operator. Its regulated band interpretation is not a relativistic ultraviolet completion. Nodal rings observed in ordinary solids provide an analogy, not evidence for a cosmic dark medium. Derivation, matrix representation and thermal tests: [fermion origin](mechanism_2026_10_12/NODAL_RING_ORIGIN.md).

## Static force and mass dependence

Define

$$
\mathbf D=C\nabla\varphi-\mathbf P,\quad
\nabla\cdot\mathbf D=q_b\rho_b,\quad
\mathbf g_s=-q_b\nabla\varphi,\quad
\mathbf D/C=\delta F_F/\delta\mathbf P.
$$

In the local cubic approximation, D/C=beta_3 |P|P. Outside a spherical baryonic source,

$$
\mathbf P=\frac B r\hat{\mathbf r},\quad
B=\sqrt{\frac{q_bM_b}{4\pi C\beta_3}},
$$

$$
g_s=\frac{q_b^2M_b}{4\pi C r^2}+\frac{q_bB}{Cr},\qquad
V_\infty^4=\mathcal K M_b,\quad
\mathcal K=\frac{q_b^3}{4\pi C^3\beta_3}
=\frac{q_b^3v}{2Nm_*C^3h^3}.
$$

This reproduces the desired mass exponent only in its specified approximation. It does not fix the coefficient. The inverse-square scalar term must also be included when calibrating the measured Newtonian constant; G_grav cannot simply be identified with measured G_N without that accounting.

A single ring has anisotropic spatial response. For a uniformly oriented ensemble with equal radial and axial band speeds, the generated weak-field spatial energy has Hessian eta |k|, with

$$
\eta=\frac{Ah^2\pi^2v}{16}=\frac{Nm_*h^2\pi}{32}.
$$

The weak-source limit instead obeys

$$
\mathbf D/C=\eta|\nabla|\mathbf P,\qquad
V_\infty^2=\frac{q_b^2M_b}{2\pi^2C^2\eta},\qquad
V_\infty^4\propto M_b^2.
$$

Here |grad| has Fourier multiplier |k|. A finite Gaussian source confirms that the change in exponent is not a point-source singularity. In the opposite large-gap, slowly varying regime the leading generated gradient correction gives

$$
V_\infty^4\simeq\mathcal K(M_b-M_{\rm off}),\qquad
M_{\rm off}=\frac{8\pi C A h v^2}{9q_b}.
$$

This expression cannot be extrapolated to M_b=M_off as a minimum-mass theorem. With the still-free scale M_s=4 pi C beta_3 v^2/(q_b h^2), the two dimensionless asymptotes are

$$
x=M_b/M_s,\quad y=V_\infty^4/(\mathcal K M_s),\qquad
y_{\rm weak}\simeq(32/\pi^3)^2x^2,\quad
y_{\rm gapped}\simeq x-2/9.
$$

![Separate calculated force limits and the unresolved crossover](mechanism_2026_10_12/nodal_force_limits.png)

The transition has not been solved. An interpolation formed by simply adding the gapless kernel to the cubic potential is not an established nonlinear fermion effective action. See [the force calculation](mechanism_2026_10_12/NODAL_FORCE_LIMITS.md).

## Temperature and occupancy are physical constraints

At zero chemical potential and finite T, the same homogeneous determinant gives

$$
\frac{dV_F}{d\Delta_f}
=2AT\Delta_f\ln\!\left[2\cosh\left(\frac{\Delta_f}{2T}\right)\right].
$$

For Delta_f much less than T, the leading potential is A T ln(2) Delta_f^2, not a cubic. At T=0 and finite chemical potential,

$$
\frac{dV_F}{d\Delta_f}=A\Delta_f\max(\Delta_f,|\mu|).
$$

Thus either finite temperature or shifted occupancy changes the sufficiently weak local response back to a linear constitutive law. In that local approximation the far force returns to inverse-square behavior. Spatial nonlocality must also be included before predicting an actual crossover profile. Neither “cold” nor a small mean pressure guarantees that the required fermion state persists.

## Time dependent response and energy conservation

For a homogeneous gap Delta_f and axial energy momentum q, use exp(-i omega t), z=omega+i0 and s=sqrt(q^2-z^2). The retarded polarization Hessians are

$$
\frac{\Pi_\parallel}{Ah^2}=\Delta_f+
\frac{s^2+4\Delta_f^2}{2s}\arctan\frac{s}{2\Delta_f},\qquad
\frac{\Pi_\perp}{Ah^2}=\Delta_f+\frac s2\arctan\frac{s}{2\Delta_f}.
$$

At small frequency and zero momentum their induced inertias are Ah^2/(6 Delta_f) and Ah^2/(4 Delta_f), both positive. Their absorption is nonnegative above the pair threshold sqrt(q^2+4 Delta_f^2). A positive oscillator-bath representation verifies the retained homogeneous linear stability when the static field Hessian and bare kinetic terms are positive.

For the assumed isotropic ensemble at zero gap,

$$
\Pi_R(\omega,k)=\frac{Ah^2\pi vk}{4}F(\omega/(vk)),
$$

$$
F(x)=\frac\pi4(1-x^2)
-\frac i2[x-(1-x^2)\operatorname{atanh}x],\qquad 0<x<1.
$$

The coupled mode equation is

$$
(Ck^2-Z_\varphi\omega^2)
[C^{-1}+\Pi_R(\omega,k)-I_P\omega^2]-k^2=0.
$$

Its small-k resonance has

$$
\omega=\omega_0-i\Gamma_d,\quad
\omega_0^2\simeq\frac{C^2\eta}{Z_\varphi}k^3,\quad
\Gamma_d\simeq\frac{C^2}{2Z_\varphi}
\frac{Ah^2\pi}{12v^2}\omega_0^2.
$$

The computed complex poles decay in the tested homogeneous setting. Fermion absorption moves energy into excitations; it does not erase energy. The damping time grows as k^-3 at long wavelength, so stability does not establish settling within a galaxy's lifetime. Physical times cannot be assigned without the unfixed coefficients. These results are detailed in [the dynamics audit](mechanism_2026_10_12/NODAL_DYNAMICS.md).

## The missing connection between the two mechanisms

A proposed full framework would need, schematically,

$$
S_{\rm total}=S_{\rm gravity}+S_{\rm baryons}+S_c+
S_{\varphi P}+S_F+S_{\rm bridge}+S_{\rm counterterms}.
$$

This is an inventory of required sectors, not a completed action: S_bridge has not been specified or derived, and the relativistic carrier and preferred-frame band medium have not been embedded in a common covariant theory. Setting S_bridge=0 leaves two independent mechanisms. A nonzero bridge can change the carrier energy bound, fermion temperature and chemical potential, and must be recalculated rather than assumed harmless.

The observed baryonic force would include ordinary gravity and the new scalar force. If the carrier also supplies a real halo, its gravitational field must be included once. The effective density inferred from the scalar force is not automatically the mass density of the carrier. Adding a target dark halo and the scalar force without a joint calculation risks counting the same inferred discrepancy twice.

Rotation curves and lensing are also distinct obligations. A force on baryons does not specify how photons propagate. The proposed nonrelativistic scalar coupling does not yet predict the lensing metric, gravitational waves or relativistic cosmological perturbations.

Finally, no calculation links the independent vacuum energy to the force coefficients. Adding a constant vacuum offset leaves the nongravitating constitutive equations unchanged. The desired identities remain

$$
\mathcal K\stackrel{?}{=}G_Na_0,\qquad
a_0\stackrel{?}{=}\frac c2\sqrt{G_N\rho_{\rm DE}}.
$$

An explanation of these relations must supply an interaction, symmetry or cosmological boundary condition that actually connects the quantities. Choosing their values to satisfy the equalities is calibration, not derivation.

## Observations and their assumptions

The released SPARC table contains 2693 acceleration pairs. The existing descriptive calculation gives RMS log-acceleration residual 0.13712 dex for the frozen repaired target at the canonical scale, versus 0.51398 dex for the baryons-only Newtonian comparison. These are results for the target relation, not predictions from the new fermion model. The relation's historical use of SPARC, correlated radial points and absent full covariance prevent interpreting this as independent microscopic validation or a model-selection significance. See [the empirical audit](empirical_2026_10_12/EVIDENCE.md) and the [released table](https://astroweb.case.edu/SPARC/RAR.mrt).

The same audit records weak-lensing support for an extended acceleration relation under isolation, mass-estimation and deprojection assumptions; a cluster self-scattering constraint under halo-model assumptions; and low-mass dwarf departures from unrestricted universality. None directly detects Phi, X, Psi or P. The revised carrier benchmark's cluster comparison depends on its resonance prescription and velocity distribution.

Respecting the observations means retaining those uncertainties, including inconvenient regimes, and comparing predictions to observables before adjusting parameters. No data set is presumed assumption-free. For this candidate the most useful distinct predictions are a low-mass change in the mass–velocity relation, finite-temperature or occupancy transitions, and the response times implied by its medium. Their physical scales must be fixed independently before a meaningful test.

## Claim status and evidence map

| Claim | What is established here | What remains necessary |
|---|---|---|
| Protected cold carrier | Classical energy structure and regulated quantum inequalities | Continuum completion and survival with added interactions |
| Near-threshold production | Kinematics, rate estimates and finite unitary transfer | Physical source preparation, abundance and production epoch |
| Carrier halo formation | Explicit finite evolution tests | A mechanism that selects the target rather than initial-condition memory |
| Cubic force interaction | Positive contribution from a specified fermion band Hamiltonian | Existence of that medium and critical quadratic matching |
| Spatial force | Controlled weak and gapped limits with different mass scaling | Nonlinear crossover, anisotropy and inhomogeneous source solution |
| Dynamics | Passive homogeneous response and decaying resonances | Live matter, halo stability and physical settling time |
| Vacuum acceleration | A target numerical relationship | A derivation linking vacuum density to interaction coefficients |
| Empirical identification | Phenomenological comparisons with stated assumptions | Independent tests of the microscopic candidate and lensing completion |

Each linked research note contains its computational contract and run directory. [The concise equation index](mechanism_2026_10_12/EQUATIONS.md) provides a shorter entry point. Numerical checks verify specific implementations and finite assertions; their count is not independent empirical support. Failed numerical attempts and rejected mechanisms remain in the archive rather than being rewritten as successes.

The framework is therefore ready to be inspected as an explicit candidate with equations and failure conditions. It is not ready to be presented as a demonstrated source of usable energy, a unified dark sector, or a derivation of the repository's complete acceleration law.
