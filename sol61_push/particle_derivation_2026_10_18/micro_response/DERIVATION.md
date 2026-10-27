# Gravitational response from the stated scalar actions

18 October 2026 local / 19 October UTC. This is a new response derivation, not a halo fit or an update to a publication/current file. The initial requested repository base is `3d8900c10d8b778e2756838f2d00779dc43510ab`. HEAD changed concurrently during this lane; `source_pins.json` and the runner manifest identify the actual source bytes and both observed revisions. No Git mutation was performed here.

**Result.** The dilute scalar carrier and the separate canonical charged host generate ordinary density/compressibility response, with quantum pressure and finite-range mediator corrections. In the stated nonsingular static-amplitude regime, they do not generate the polarization action or its full residual `R(u)=u²/(a0−u)`. A separately declared critical tuning of the host does construct a positive three-body interaction and a nonanalytic phonon pressure proportional to `X_NR^(3/2)`. Its exact positive-density branch requires `S=omega_local²−|∇theta|²−m²>0`; the leading controlled NR branch requires `X_NR>0` when omitted relativistic terms are small compared with `m|X_NR|`. The gradient-dominated MOND branch and a baryon source are not supplied by that tuning.

Natural units apply except when the Newton constant is written explicitly. `Phi_N` is the Newtonian potential, negative near a positive isolated mass; it is distinct from the complex carrier `Phi`. Fourier convention is `∇→ik`, and `k>0` unless a thermodynamic limit is explicitly taken. Homogeneous calculations fix a reservoir chemical potential/coordinate phase frequency; in a fixed-total-charge box the exact spatial zero mode is constrained. Response at nonzero `k` is unaffected by that one-mode restriction.

## 1. Actual dilute carrier, retaining the source channel

The action in `MASTER_COLD_ENERGY_EQUATIONS.md` has canonical complex fields with charges one and two and positive-square potential. Its stated regulated positive-frequency/rotating-wave NR reduction is

$$
H=mQ+\int\left[\frac{|\nabla\psi|^2}{2m}+
 \frac{|\nabla b|^2}{2M}+\delta|b|^2
 +c_3(b^*\psi^2+b\psi^{*2})+k_c|\psi|^4\right]d^3x,
\quad Q=\int(|\psi|^2+2|b|^2)d^3x,
$$

$$
\delta=M-2m>0,\qquad
k_{\rm eff}=k_c-c_3^2/\delta
=\frac{\lambda_{\rm rep}}{4m^2}
 +\frac{g_c^2}{8m^2M(M+2m)}>0.
$$

Cold, weak gravity couples at leading rest-energy order to `rho=m(|psi|²+2|b|²)`. The exact relativistic stress also contains detuning, interaction and gradient energies. Corrections suppressed by the cold-energy fraction do not alter the analytic operator structure below. Keeping only `m|psi|²` is the further dilute-source limit, not an exact identity for a stock of sources.

A homogeneous coherent daughter state is a **state assumption** used to compute an allowed response of this action; the production calculation does not establish that its daughters condense. Choose the common rotating background

$$
\psi=f e^{-i\mu t},\quad b=b_0e^{-2i\mu t},\quad n_0=f^2,
\quad \Delta=\delta-2\mu,
\quad b_0=-c_3n_0/\Delta,
\quad \mu=2(k_c-c_3^2/\Delta)n_0.
$$

For real canonical amplitudes `s=sqrt(2)delta f`, `t=sqrt(2)delta b`, the static grand-energy Hessian and the leading mass source are

$$
K_{\rm NR}(k)=
\begin{pmatrix}
4k_cn_0+k^2/(2m)&2c_3\sqrt{n_0}\\
2c_3\sqrt{n_0}&\Delta+k^2/(2M)
\end{pmatrix},\qquad
q_Q=\sqrt2m\begin{pmatrix}\sqrt{n_0}\\2b_0\end{pmatrix}.
$$

Consequently, within this leading NR gravity convention,

$$
\delta\rho(k)=-\chi_Q(k)\Phi_N(k),\qquad
\chi_Q=q_Q^TK_{\rm NR}^{-1}q_Q.
$$

This retains the source amplitude and its range. Strict static material stability follows from `Delta>0` and `k_c Delta>c3²`. These conditions hold sufficiently near the dilute branch when `k_eff>0`; they must be rechecked at larger density. The matrix inverse is a rational function of `k²`. Its daughter Schur denominator is

$$
4k_cn_0+\frac{k^2}{2m}
-\frac{4c_3^2n_0}{\Delta+k^2/(2M)}
=4n_0(k_c-c_3^2/\Delta)
+k^2\left[\frac1{2m}+\frac{2c_3^2n_0}{M\Delta^2}\right]+O(k^4).
$$

This is the finite-range/contact and derivative correction actually produced by the source channel. Its relevant small denominator is the detuning `Delta`, not merely the relativistic source mass `M`. Close to the conversion resonance the local elimination is invalid. A real population of `b` must be evolved as a population, not removed as if it were only a virtual mediator.

There is a small but important matching distinction before calling this the complete low-energy response of the relativistic action. The full same-charge threshold amplitude is `−4lambda_rep`, so its fully threshold-matched daughter contact is `g2_match=lambda_rep/(2m²)`. The positive-frequency Hamiltonian above instead has `4m² k_eff=lambda_rep+g_c²/[2M(M+2m)]`. Decomposing the exact source propagator,

$$
\frac1{4m^2-M^2}=\frac1{2M}\left[\frac1{2m-M}-\frac1{2m+M}\right],
$$

shows that the removed negative-frequency source adds an analytic contact correction `delta k=−g_c²/[8m²M(M+2m)]`. Including it in the retained-source NR kernel means replacing `k_c` by `k_c+delta k`. The corrected dilute limit has `k_eff_match=lambda_rep/(4m²)>0`. The original positive-square bound remains a statement about its stated uncorrected regulated Hamiltonian, and is not silently transferred to the newly matched Hamiltonian. This correction changes the coefficient, not the analytic kernel or Jeans conclusion. The narrow independent check of the matching and exchange note is `EXCHANGE_REVIEW.md`.

In the dilute limits `mu/delta≪1`, `|b0|²/n0≪1`, and `k²/(2M Delta)≪1`, the effective daughter energy is

$$
E=\int\left[\frac{|\nabla\psi|^2}{2m}
+\frac{g_2}{2}n^2+m\Phi_Nn\right]d^3x,
\quad g_2=g_{2,\rm match}=\lambda_{\rm rep}/(2m^2)>0.
$$

Writing `psi=sqrt(n)e^{i theta}` retains quantum pressure. Linearizing `mu=g2 n+m Phi_N−∇²sqrt(n)/(2m sqrt(n))` gives

$$
\boxed{\quad
\delta\rho(k)=-\frac{m^2}{g_2+k^2/(4mn_0)}\Phi_N(k),\qquad
\chi_\rho(k)=\frac{\rho_0}{c_s^2+k^2/(4m^2)},\quad
c_s^2=\frac{g_2n_0}{m}.\quad}
$$

The time-dependent density mode has denominator `c_s²k²+k⁴/(4m²)−Omega²`. Restoring self-gravity using `∇²Phi_N=4pi G(rho_b+delta rho)` gives

$$
\frac{\delta\rho_c}{\rho_b}
=\frac{4\pi G\rho_0}
 {c_s^2k^2+k^4/(4m^2)-4\pi G\rho_0},\qquad
\Omega^2=c_s^2k^2+\frac{k^4}{4m^2}-4\pi G\rho_0.
$$

Thus the gravitational enhancement is a Jeans response. It has no controlled static stable `k→0` limit in an infinite self-gravitating homogeneous medium. Use a finite box, imposed background or modes above the Jeans threshold when interpreting the static susceptibility. Instability is not a MOND interpolation.

If the actual daughters form a dilute gas instead, its state enters the answer. Use the specific energy `E=v²/2+Phi_N` and a prescribed decreasing number distribution in velocity space, `f(x,v)=F(E)`, normalized by `n=∫f d³v`. Then `delta rho=m∫F'(v²/2) d³v Phi_N`. If `F` were instead defined as a function of total particle energy, the derivative formula would contain an additional factor of `m`. A Maxwell distribution of one-dimensional dispersion `sigma` gives `chi_rho=rho0/sigma²`. The same Poisson closure gives a Jeans denominator. A perfectly cold pressureless gas has no finite static compressibility. Neither the scalar action nor its production energy bound independently fixes the distribution, halo normalization, or `a0`.

## 2. Separate canonical charged host with a real mediator

This is the explicitly separate action from `MEDIATOR_COMPLETION_AND_VALIDITY.tex`, not the MeV carrier relabeled:

$$
\mathcal L=-|\partial\Psi|^2-\tfrac12(\partial\chi)^2-V,
\quad V=m_h^2I+\lambda I^2+a\chi I+U(\chi),\quad I=|\Psi|^2,
$$

$$
m_h=1,\quad \lambda=2-1/M,\quad a=2M,
\quad U=\frac{M^2\chi^2}{2}-\frac{M\chi^3}{8}+\frac{\chi^4}{4}.
$$

Take `Psi=f exp(i omega t)`, `I=f²`, with `V_I=omega²` and `V_chi=0`. On a homogeneous background let

$$
A=4\lambda I,\qquad B=\sqrt2a\sqrt I,\qquad D=U''(\chi),
\quad A_{\rm eff}=A-B^2/D.
$$

For canonical real amplitudes `s=sqrt(2)delta f`, `t=delta chi`, the complete static amplitude kernel is

$$
K(k)=\begin{pmatrix}k^2+A&B\\B&k^2+D\end{pmatrix}.
$$

It is positive for `D>0`, `A_eff>0`. In this model `D=3(chi−M/8)²+61M²/64>0` exactly; positivity of `A_eff` is a separate host-state condition.

To derive rather than guess its gravitational source, use the static lapse probe `ds²=−N²dt²+dx²`, `N=1+Phi_N`, holding the spatial metric fixed. At fixed coordinate frequency the homogeneous action density is

$$
L(N,f,\chi)=\omega^2I/N-NV.
$$

Its amplitude source is `q=(2sqrt(2)omega²sqrt(I),0)`, and `L_NN=2omega²I` at `N=1`. Integrating both amplitudes therefore yields the physical local-energy response

$$
\boxed{\quad
-\frac{\delta\rho}{\delta\Phi_N}(k)
=2\omega^2 I+
\frac{8\omega^4I}{k^2+4\lambda I-2a^2I/(k^2+U'')}.\quad}
$$

The first term is the explicit lapse second derivative (often called a seagull). It must be included when comparing with thermodynamics. The denominator has low-momentum expansion

$$
A_{\rm eff}+Zk^2+O(k^4),\qquad Z=1+B^2/D^2>0.
$$

The full coupled dynamics also contains the gapless charge phase. With `Omega` the frequency, its exact quadratic determinant is

$$
(k^2-\Omega^2)[(k^2+A-\Omega^2)(k^2+D-\Omega^2)-B^2]
-4\omega^2\Omega^2(k^2+D-\Omega^2)=0.
$$

At `k=0`, there is a Goldstone root and two amplitude gaps equal to the eigenvalues of `[[A+4omega²,B],[B,D]]`. The static curvature eigenvalues of `[[A,B],[B,D]]` are not those dynamical gaps. The sound speed and thermodynamic identity are

$$
c_s^2=\frac{A_{\rm eff}}{A_{\rm eff}+4\omega^2},\qquad
\rho+p=2\omega^2I,\qquad
\chi_\rho(0)=\frac{\rho+p}{c_s^2}.
$$

They follow independently from `n=2omega I`, `dI/domega=2omega/(2lambda−a²/D)`. A Goldstone mode exists, but its derivative coupling does not turn this static finite-density compressibility into `|P|³` at tree level.

At the four exact coexistence states in the source family, the new calculation finds:

| M/m_h | A_eff | c_s² | chi_rho(0), in host mass units |
|---:|---:|---:|---:|
| 1 | 0.561789 | 0.153023 | 5.394742 |
| 10 | 0.954922 | 0.235680 | 28.590259 |
| 100 | 0.999115 | 0.248982 | 296.485117 |
| 1000 | 0.999990 | 0.249909 | 2996.094306 |

A second calculation solves the nonlinear stationary equations at lapses `1±epsilon`, at two epsilon values. Its worst relative discrepancy with the susceptibility is `6.36e−9`. Twenty direct `2x2` inverse comparisons at four masses and five momenta check the finite-range formula. This is a matter susceptibility in an explicitly specified external metric probe; a relativistic self-gravitating host also requires the spatial metric and pressure/stress constraints. It is not a completed Einstein/galaxy solution.

## 3. Why this is not the material polarization action

For the actual regulated carrier, `Q=∫(psi†psi+2b†b)>0` in a nonvacuum positive-charge sector, and `H≥mQ`. These are operator statements. An identity `rho=div P` with a periodic or decaying local `P` would instead give `∫rho=0`. It cannot be the identity for that positive rest-mass stock. A background-plus-fluctuation decomposition `rho=rhobar+div P` can represent zero-total-mass perturbations, but does not identify a new local vector degree of freedom.

In fact, a density perturbation may always be represented at `k≠0` by

$$
P_L(k)=-\frac{ik}{k^2}\delta\rho(k).
$$

This is a nonlocal inverse derivative, and it fixes only the longitudinal part. If the material density energy is `|delta rho|²/(2chi_rho(k))`, this representation gives

$$
E_{\rm matter}^{(2)}=\frac12\frac{k^2}{\chi_\rho(k)}|P_L|^2,
\qquad
E_{\rm grav}^{(2)}=-\frac{4\pi G}{2}|P_L|^2.
$$

An analytic finite compressibility produces `k² P_L²`, plus higher derivatives. A matter term `+(4pi G)P²/2` requires a density energy kernel `4pi G/k²`, hence a new long-range restoring interaction or a separately established operator constraint. Canonical contact interactions and a massive mediator do not supply it. The gravitational negative term then gives the Jeans instability, rather than an automatic positive tether canceling gravity at all small `k`.

The target corrected action uses `K_g=4pi G`, `u=K_g|P|` and

$$
W_{\rm full}=\frac{-a_0u-a_0^2\log(1-u/a_0)}{K_g},\qquad
W_{\rm rem}=W_{\rm full}-\frac{u^2}{2K_g},
$$

$$
K_g\frac{dW_{\rm rem}}{du}=\frac{u^2}{a_0-u},\qquad
W_{\rm rem}=\frac{K_g^2}{3a_0}|P|^3
+\frac{K_g^3}{4a_0^2}|P|^4+\cdots.
$$

Here the displayed derivative is with respect to `u`; with `p=|P|`, `dW_rem/dp=u²/(a0−u)`. There are **two** missing ingredients: the correctly normalized local quadratic tether, and the nonanalytic leading cubic. They must not be conflated with the existence of a heavy mediator.

For the stated analytic polynomial action, eliminating a finite set of amplitudes at a nonsingular static Hessian gives a regular local expansion in the sources and `k²`: solve the stationary equations recursively using the invertible Hessian. In an isotropic unpolarized state a local analytic scalar function of a genuine vector `P` expands in `(P²)^j`. It cannot contain `|P|³`, which is not analytic at `P=0`. Once its quadratic term is tuned away the next analytic restoring vector is proportional to `|P|²P`, not `|P|P`. This tree-level analytic obstruction applies on a branch continuously connected to `P=0` with a finite static amplitude gap. It does not exclude a phase boundary, singular elimination, anisotropic/polarized state, deliberately nonanalytic microscopic coupling, or gapless fluctuation effects. A full all-loop claim would require retaining and analyzing the gapless phase. The explicit linear kernels above already suffice to reject an identification of these calculated finite-gap responses with the target action.

## 4. Concrete changed route: critical three-body host

Keep the same canonical real mediator and set the bare host quartic to `lambda=2+epsilon`, instead of its original `2−m_h/M`. Restore a general host vacuum mass `m_h=m` in this section. Direct series solution of the unique mediator equation gives

$$
\chi_*(I)=-\frac{2I}{M}+\frac{3I^2}{2M^3}
+\frac{23I^3}{4M^5}+O(I^4/M^7),
$$

$$
\boxed{\quad
V_{\rm eff}=m^2 I+\epsilon I^2+\frac{I^3}{M^2}
+\frac{23I^4}{8M^4}+O(I^5/M^6).\quad}
$$

The mediator expansion requires `I/M²≪1`. The original host has `epsilon=−m/M`; the new critical branch declares `epsilon=0`. Nothing in its `U(1)` symmetry selects or protects that quartic cancellation.

There is an exact useful parameterization at `epsilon=0`. Put `chi=−x`, `x≥0`. Mediator stationarity and the host equation imply

$$
I(x)=\frac{Mx}{2}+\frac{3x^2}{16}+\frac{x^3}{2M},\qquad
S(x):=V_{{\rm eff},I}-m^2=\frac{3x^2}{4}+\frac{2x^3}{M}.
$$

Both are strictly increasing for `x>0`, and

$$
V_{{\rm eff},II}
=4-\frac{4M^2}{M^2+3Mx/4+3x^2}>0\quad(x>0).
$$

Thus the density branch is stable and unique for `S>0`, while no nonzero homogeneous branch exists for `S<0`. This sign restriction on `S` is exact for the tuned polynomial action, not a sextic-truncation artifact. For a constant phase gradient, `S=omega_local²−|∇theta|²−m²`. Positivity of `S` implies positivity of the leading NR invariant only when the relativistic remainder is negligible relative to `2m|X_NR|`, as specified below. At the zero-density endpoint the static density curvature vanishes: this is precisely a singular state limit omitted by the finite-density analytic expansion.

Integrating `dP_rel/dS=I(S)` gives

$$
I(S)=\frac{M}{\sqrt3}\sqrt S-\frac{23}{36}S+O(S^{3/2}/M),\quad
P_{\rm rel}(S)=\frac{2M}{3\sqrt3}S^{3/2}
-\frac{23}{72}S^2+O(S^{5/2}/M),\quad S>0.
$$

For a controlled NR reduction use `Psi=e^(−imt)psi/sqrt(2m)`, `I=n/(2m)` and phase `psi=sqrt(n)e^(−i theta)`, `theta=mu_NR t+pi`. Up to quantum pressure,

$$
L=nX_{\rm NR}-\frac{g_2n^2}{2}-\frac{g_3n^3}{3}+\cdots,
\quad X_{\rm NR}=\mu_{\rm NR}+\dot\pi-m\Phi_N-
 \frac{|\nabla\pi|^2}{2m},
$$

$$
g_2=\frac{\epsilon}{2m^2},\qquad g_3=\frac{3}{8m^3M^2}>0.
$$

The omitted quantum-pressure term is `−|∇n|²/(8mn)`. At `epsilon=0` the constrained Legendre transform over physical `n≥0` is

$$
n=\sqrt{X_{\rm NR}/g_3},\qquad
\boxed{\quad P(X_{\rm NR})=\frac{2X_{\rm NR}^{3/2}}{3\sqrt{g_3}},
\quad P_X=n>0,\quad P_{XX}=\frac1{2\sqrt{g_3X_{\rm NR}}}>0\quad}
$$

for `X_NR>0`. For `X_NR≤0`, the maximum is the vacuum `n=0`, `P=0`; it is not the negative-`X` MOND branch. This constructs a fractional-power phase pressure from the actual changed particle action. It does not construct a fractional-power potential for the material mass-polarization vector.

With a residual quartic, the locally stable positive-density branch satisfies

$$
X_{\rm NR}=g_2n+g_3n^2,\qquad
n=\frac{-g_2+\sqrt{g_2^2+4g_3X_{\rm NR}}}{2g_3},\qquad
U''(n)=g_2+2g_3n>0.
$$

For `g2>0`, sufficiently weak fields instead have `P≈X_NR²/(2g2)`. For `g2<0`, stable positive-density states can reach negative chemical potential, but a first-order coexistence occurs at `n_t=−3g2/(4g3)`, `X_t=−3g2²/(16g3)`; the spinodal is `n_s=−g2/(2g3)`, `X_s=−g2²/(4g3)`. These expressions are for the NR cubic truncation. They show why retaining the original attractive quartic is not the same critical three-body construction.

The simultaneous controlled three-body window is, parametrically,

$$
\frac{2}{3}|\epsilon|M^2\ll I
\ll\min(M^2,mM),\qquad
k^2\ll8mX_{\rm NR},\qquad |X_{\rm NR}|/m\ll1.
$$

The lower inequality suppresses the quartic in the chemical potential; the upper ones control the mediator and NR expansions. The use of the sign of `X_NR` additionally requires `|S−2mX_NR|≪2m|X_NR|`, a condition not uniform near a cancellation of its chemical and gradient terms. For a stationary `pi` at flat lapse, `S=2mX_NR+mu_NR²`; a time-dependent `pi` instead gives the squared remainder `(mu_NR+dot pi)²`. For example, `|∇pi|²=2m mu_NR+mu_NR²/2` gives `X_NR=−mu_NR²/(4m)<0` while exact `S=mu_NR²/2>0`; the leading NR sign test is invalid at that near-cancellation point. A parametric window for `M≫m` needs `|epsilon|≪m/M`. The original `epsilon=−m/M` does not have this window. Its self-bound phase has `I≈mM/2` and a binding chemical potential of order `−m/8` in the NR truncation, so increasing `M/m` alone does not make that coexistence phase arbitrarily nonrelativistic. Quantum pressure becomes essential near `X_NR=0` since its allowed wavenumber tends to zero. The gapless limit must be taken with this ordering of scales.

## 5. First discriminating check and the direct baryon source

In a static configuration the phase invariant is

$$
X_{\rm NR}=\widehat\mu-\frac{|\nabla\pi|^2}{2m},\qquad
\widehat\mu=\mu_{\rm NR}-m\Phi_N.
$$

A phase action proportional to `−|∇pi|³` would arise from the familiar formal continuation `P=A X sqrt(|X|)` on a gradient-dominated `X<0` branch. It is unavailable in this controlled gradient-dominated regime: the leading NR transform gives `P=A X^(3/2)` only for `X>0`, and its sign is faithful to the exact branch when `|S−2mX|≪2m|X|`. Tiny negative `X` inside the near-cancellation remainder are not excluded by exact `S>0`; they do not constitute the gradient-dominated regime. Continuing as `A X sqrt(|X|)` gives `P_X>0` but `P_XX<0` for `X<0`, hence a negative time kinetic coefficient. Continuing instead as `A|X|^(3/2)` gives negative number density. The exact `S(x)>0` formula provides a first discriminating check before a halo simulation: **the tuned canonical mediator model fails the well separated gradient-dominated branch while producing a stable positive-`S` compressibility.** A changed derivative or multicomponent finite-temperature action would have to be specified and checked; it cannot be imported from the potential matching.

There is also a source restriction. The minimal action has an exact global charge symmetry. Its phase equation is a continuity equation. In a regular static spherical state without a charge flux through the origin,

$$
\nabla\cdot(n\nabla\pi/m)=0
\quad\Longrightarrow\quad r^2n\pi'/m=0.
$$

Baryonic gravity changes `X_NR` and density, but supplies no phase monopole. To obtain the usual direct phonon force one might add `L_int=−g_b pi rho_b`. In the chosen phase convention this yields

$$
-\dot n+\nabla\cdot(n\nabla\pi/m)=g_b\rho_b.
$$

Thus the original Noether charge current has a baryonic source (the sign reverses with the current convention). This explicitly breaks the original exact `U(1)`. It is incompatible with asserting that the same source-free current is identically a background current plus the divergence of an antisymmetric two-form, unless an additional baryon/receiver current is assigned the compensating charge and included in the total current. A derivative coupling `J_b^mu ∂_mu pi` integrates by parts to `−pi ∂_mu J_b^mu` plus a boundary term, so a conserved stationary baryon current provides no local phase source that way. This is a restriction on the direct sourced-phonon fifth-force route, not a theorem excluding all shift-invariant metric couplings.

For comparison only, Berezhiani and Khoury explicitly study `P(X)∝X sqrt(|X|)` with a separate baryon phase coupling, distinguish the stable `X>0` branch from the unstable zero-temperature MOND branch, and state the same obstruction for a canonical stable hexic potential. Exact primary version, locators and translation are in `LITERATURE.md`. None of their derivative completion or finite-temperature operators is part of this host. In their parameter notation the positive-branch coefficient here corresponds to `Lambda=M/sqrt(3)`; that is a coefficient dictionary, not a calculation of `a0`.

## 6. Other changed gapless branch, kept separate

The repository's additional nodal-ring fermion model is an explicit example that violates the finite-gap premise. With a gap `Delta=h|P|`, two transverse linear-energy directions, filled negative-energy bands and density-of-states coefficient `A`, direct radial integration gives

$$
\Delta V=-A\int_0^\Lambda q\,[\sqrt{q^2+\Delta^2}-q]dq
=-\frac A3[(\Lambda^2+\Delta^2)^{3/2}-\Lambda^3-|\Delta|^3].
$$

After the analytic quadratic subtraction, `V_ren=Ah³|P|³/3+O(P⁴/Lambda)`. The script independently differentiates this integral and checks its cubic coefficient. The carrier contains no such fermions or candidate vector mass operator; the existence and occupation of this extra medium are new assumptions. Even this added determinant supplies only a leading cubic. It does not fix the full logarithmic `W_full`, its critical quadratic cancellation, `a0`, or vacuum normalization. Its zero-gap finite-momentum response is nonlocal, so the homogeneous local potential must not replace the full kernel near a sourced critical configuration.

## 7. Evidence, interpretation and limits

`check_response.py` plus `contract.json` define the new bounded calculation. `run_002/results.json` records **78 passing exact/finite checks**, and `run_002/manifest.json` is a validated runner-v2 evidence record with status `completed`, actual software versions and before/after input hashes. Run 001 is the earlier successful 75-check calculation, before adding the three exact full-propagator matching checks. The finite checks cover four host masses and five momenta; they are not a numerical survey of all states. The formulas and restrictions above provide the analytic arguments. The maximum independent nonlinear lapse-response discrepancy was `6.36e−9`; the declared diagnostic gate was `8e−6` because binary64 root subtraction degrades at large `M`.

The source `MASTER_COLD_ENERGY_EQUATIONS.md` was already dirty and some closure/action sources were untracked at the requested base. Their actual bytes are pinned; this lane did not change them. No queue, heavy simulation, current contract, frozen artifact, or manuscript was modified. No new empirical or novelty claim is made. The achieved result is the explicit gravitational susceptibility and a precisely delimited constructive critical-phase branch, together with the operator/source/branch mismatches preventing either from being called the requested full gravitational law.
