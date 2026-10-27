# A finite-density one-fluid infrared constraint beyond the amplitude calculation

19 October 2026. Continuation from `CE-PARTICLE-2026-10-18 / CE-FM-085`, requested initial revision `9516ee01c79f35c04b7556050669ba77b0c98b99`. This is an analytic conditional result in the assigned `collective_response/` scope. It introduces no new mediator, interaction, simulation or shared-state update.

**Result.** A homogeneous zero-temperature local fluid with one conserved positive number density `n>0`, finite chemical potential `mu>0`, and stable causal acoustic mode has a nonzero long-wavelength static mass/energy susceptibility. Its exact equation of state gives

\[
\boxed{\quad
\chi_{NN}=P''(\mu)=\frac{n}{\mu c_s^2},\qquad
\chi_{\rho_0\rho_0}=m^2P''(\mu)=\frac{m^2n}{\mu c_s^2},
\qquad
\chi_{EE}=\mu^2P''(\mu)=\frac{\varepsilon+p}{c_s^2}.
\quad} \tag{1}
\]

The static cross-response of reference density `rho_0=m n` to an actual lapse perturbation is a different quantity,

\[
\boxed{\quad
\delta\rho_0=-\chi_{\rho_0 E}\Phi,\qquad
\chi_{\rho_0 E}=m\mu P''(\mu)=\frac{mn}{c_s^2}.
\quad} \tag{2}
\]

Here the static limit is taken at nonzero `k` before `k -> 0`, in a fixed external probe metric or matter-source problem. The exact constrained zero mode in a fixed-charge box is a separate question. Equation (1) is a thermodynamic/leading-hydrodynamic identity, not an assertion that the original neutral particle bath has reached this one-fluid state.

Consequently the corresponding self-response inverse kernels have finite limits,

\[
h_{\rho_0\rho_0}(0,k\to0)
=\frac{\mu c_s^2}{m^2n},\qquad
h_{EE}(0,k\to0)=\frac{c_s^2}{\varepsilon+p}. \tag{3}
\]

Neither can approach `+K_g/k^2`, `K_g=4piG>0`, at a fixed state satisfying these hypotheses. The lapse cross-response must not be inverted and mislabeled as the reference-density self-energy curvature. This narrows the incompressible-phase loophole for a physical **acoustic mass/energy fluid**; it does not exclude a gapped signed-charge or optical density in the same material, nor every phase of the original action.

## 1. Hypotheses and exact thermodynamics

Assume a homogeneous, isotropic, no-flow zero-temperature phase with one positive conserved number current at the scales of interest. Let its exact thermodynamic energy density be `epsilon(n)` and its local equation of state be twice differentiable in an open neighborhood of a chosen state. Define

\[
\mu=\frac{d\varepsilon}{dn}>0,\quad
p=n\mu-\varepsilon,\quad
w=\varepsilon+p=\mu n>0. \tag{4}
\]

The chemical potential in this note includes rest energy. It is not the NR rotating-frame `mu` used in the atom–molecule example; in its dilute single-sign limit, `mu_full=m+mu_NR`. This distinction is required both in the causal sound relation and in the lapse source vertex.

For a strictly stable compressible state, `mu'(n)>0`, or equivalently the pressure Legendre transform `P(mu)=p` has

\[
n=P'(\mu)>0,\qquad \kappa:=P''(\mu)=\frac{dn}{d\mu}>0. \tag{5}
\]

The isentropic sound speed is

\[
c_s^2=\frac{dp}{d\varepsilon}
=\frac{n\mu'(n)}{\mu}
=\frac{n}{\mu\kappa}. \tag{6}
\]

No weak-coupling or mean-field expansion enters these thermodynamic identities. Quantum corrections may be included in the exact equation of state. The remaining physical hypotheses are that a local one-fluid acoustic description exists with derivative corrections that vanish at long wavelength, and that its stable sound speed obeys `0<c_s^2<=1` in units with the limiting microscopic light speed equal to one. The sound-speed inequality is a declared causal-fluid condition; it is not independently proved here for every state of the microscopic model.

These conditions imply

\[
\kappa=\frac{n}{\mu c_s^2}\ge\frac n\mu>0,\qquad
\chi_{EE}=\frac{w}{c_s^2}\ge w>0,\qquad
\chi_{\rho_0\rho_0}\ge\frac{m^2n}{\mu}>0. \tag{7}
\]

Thus the required vanishing static susceptibility `chi ~ k^2/K_g` cannot occur in the acoustic density at this fixed nonzero-density state. An ideal incompressible limit `kappa -> 0` with fixed finite `n,mu` would require `c_s^2 -> infinity`; it leaves the causal-fluid hypothesis. A soft limit `c_s^2 -> 0` instead makes the susceptibility diverge and the inverse curvature tend to zero, also the wrong direction for a positive `1/k^2` stiffness. Varying the background state with `k` is not the response of one fixed state and does not evade this conclusion.

The vacuum/zero-enthalpy case `n=0` or `w=0` is excluded explicitly. A cosmological-constant stress with `p=-epsilon` is not a positive-density acoustic bath to which the argument applies.

## 2. Number source, reference-mass source and lapse source

Let `U_N` be an external scalar appearing linearly in the Hamiltonian as `U_N n`. Local equilibrium gives `mu_eff=mu-U_N`, hence

\[
\delta n=-\kappa U_N,\qquad \chi_{NN}=\kappa. \tag{8}
\]

A source `U_0` coupled instead to reference density `rho_0=m n`, with constant microscopic reference mass `m>0`, has `U_N=mU_0`. Consequently

\[
\delta\rho_0=-m^2\kappa U_0,
\qquad \chi_{\rho_0\rho_0}=m^2\kappa. \tag{9}
\]

Equivalently, the quadratic thermodynamic cost for nonzero-momentum density perturbations, after the linear fixed-background chemical-potential term cancels, is `delta n^2/(2kappa)=delta rho_0^2/(2m^2 kappa)`. This identifies the self-response inverse as a material density curvature under the declared Legendre convention.

An actual static lapse is different. Take `ds^2=N(x)^2dt^2-dx^2` with the spatial metric held fixed, `N=1+Phi`. Static perfect-fluid balance gives

\[
\nabla p=-w\nabla\log N.
\]

Using `dp=n dmu` and `w=mu n`, this integrates locally to `N mu_local=mu`, with `mu` the fixed coordinate-time chemical potential. To first order,

\[
\delta\mu_{\rm local}=-\mu\Phi,
\quad \delta n=-\mu\kappa\Phi,
\quad \delta\rho_0=-m\mu\kappa\Phi,
\quad \delta\varepsilon=-\mu^2\kappa\Phi. \tag{10}
\]

This proves both the lapse cross-response (2) and the energy response in (1). In particular `m^2 kappa`, `m mu kappa`, and `mu^2 kappa` are not interchangeable. They coincide at leading cold order when `mu/m -> 1`, but the exact response operators differ. Pressure and spatial metric constraints also matter in a full self-gravitating relativistic calculation; the present result is the fixed-spatial-metric external-lapse matter response.

## 3. Lapse action and the explicit metric contact term

For a zero-temperature irrotational fluid/superfluid, the same result follows from the leading local phase action

\[
S=\int d^4x\sqrt{-g}\,P(X),\qquad
X=\sqrt{g^{\mu\nu}\partial_\mu\Theta\partial_\nu\Theta},
\qquad\Theta=\mu t\ \hbox{on the background}. \tag{11}
\]

With `Theta` fixed to the homogeneous stationary phase and `N` varied, the coordinate-time Lagrangian density is

\[
\mathcal L(N)=N P(\mu/N). \tag{12}
\]

Direct differentiation, without dropping the measure or redshift terms, gives

\[
\mathcal L_N=P(X)-XP'(X)=-\varepsilon(X),\qquad
\mathcal L_{NN}=\frac{X^2}{N}P''(X),\quad X=\mu/N.
\]
\[
\boxed{\quad \left.\mathcal L_{NN}\right|_{N=1}
=\mu^2P''(\mu)=w/c_s^2.\quad} \tag{13}
\]

This includes the complete explicit metric contact contribution at this order. It is not obtained by differentiating `P(mu-m Phi)` with an assigned particle mass, nor by computing only an amplitude exchange diagram.

More explicitly let `Theta=mu t+pi`. To second order in `pi,Phi`, with the spatial metric fixed,

\[
\mathcal L=P(\mu)-\varepsilon\Phi+n\dot\pi
+\frac\kappa2(\dot\pi-\mu\Phi)^2
-\frac{n}{2\mu}|\nabla\pi|^2+\cdots. \tag{14}
\]

The terms from the lapse measure cancel the extra `n mu Phi^2` and `n Phi dot pi` contributions from the nonlinear expansion of `X`. The surviving quadratic lapse term is `kappa mu^2 Phi^2/2`. At zero frequency and nonzero momentum the smooth phase cannot cancel this response by a time shift. At nonzero frequency and zero momentum it can, consistently with total energy conservation. Thus the contact term and phase exchange are both essential to the order of limits.

In a finite fixed-number box, an exactly uniform static change can shift the global chemical potential to preserve total number. That one-mode constraint does not remove the nonzero-momentum static susceptibility or change its thermodynamic long-wavelength limit.

## 4. Dynamic Ward/thermodynamic response

Linearizing one-fluid number continuity and momentum balance around the rest state gives

\[
\dot{\delta n}+n\nabla\cdot v=0,\qquad
w\dot v+\nabla\delta p+n\nabla U_N=0,
\quad \delta p=n\mu'(n)\delta n. \tag{15}
\]

They imply the retarded number self-response

\[
\boxed{\quad
\chi_{NN}(\omega,k)
=\frac{(n/\mu)k^2}{c_s^2k^2-(\omega+i0)^2}
+\hbox{subleading derivative terms}.
\quad} \tag{16}
\]

For a lapse perturbation the force in momentum balance is `w grad Phi`, equivalently `U_N=mu Phi` at linear order. Using `delta epsilon=mu delta n`, the self/cross responses at leading hydrodynamic order are

\[
\chi_{\rho_0\rho_0}(\omega,k)
=\frac{(m^2n/\mu)k^2}{c_s^2k^2-(\omega+i0)^2},
\]
\[
\chi_{\rho_0E}(\omega,k)
=\frac{mn k^2}{c_s^2k^2-(\omega+i0)^2},\qquad
\chi_{EE}(\omega,k)
=\frac{w k^2}{c_s^2k^2-(\omega+i0)^2}. \tag{17}
\]

Equation (14), including its explicit lapse contact term, yields the same final energy response after the smooth phase is eliminated. Static `omega=0` gives (1)–(2). For fixed nonzero frequency the numerator instead enforces `chi=O(k^2)`: this is the finite-frequency conservation limit, not an incompressible static response. The infrared inverse kernel reads, for example,

\[
\chi_{EE}^{-1}(\omega,k)
=\frac{c_s^2}{w}-\frac{(\omega+i0)^2}{w k^2}+\cdots. \tag{18}
\]

The nonlocal spatial inverse at nonzero frequency is inertia, exactly as in the explicit atom–molecule collective calculation. On the static axis the first term survives. Higher-gradient corrections may change finite momentum behavior, but cannot remove the nonzero constant limit while the local fluid and equation-of-state hypotheses stay valid.

## 5. Hyperuniform equal-time density is not zero static susceptibility

At zero temperature, use the spectral convention in the collective note: a mode with `chi=F(k)/[Omega(k)^2-(omega+i0)^2]` has equal-time one-quantum squared matrix-element weight `F/(2Omega)`. The number sound mode has `F_NN=(n/mu)k^2` and `Omega=c_s k`, so

\[
S_{NN}(k)=\frac{n k}{2\mu c_s}+\cdots\ \longrightarrow 0,
\]
\[
S_{\rho_0\rho_0}(k)=\frac{m^2n k}{2\mu c_s}+\cdots,\qquad
S_{EE}(k)=\frac{w k}{2c_s}+\cdots. \tag{19}
\]

Such suppressed equal-time fluctuations are sometimes described as hyperuniform. Static susceptibility uses a different spectral moment: `chi(k,0)=2 sum_j |<j|rho_k|0>|^2/Omega_j`, whereas the equal-time fluctuation is the same sum without `2/Omega_j`. For sound, the factor of `k` in the matrix-element weight is canceled by the `1/(c_s k)` energy denominator. The result is a finite nonzero compressibility, not a positive `1/k^2` inverse density force. Observing or postulating `S(k)->0` alone therefore does not establish the required static interaction.

## 6. Why signed-charge and multicomponent loopholes remain distinct

A neutral material can have zero signed conserved-charge density and a gapped charge/optical mode while carrying positive mass and enthalpy. An argument about an insulating `Q_+-Q_-` density does not identify the gravitational source with that charge. A gapped internal charge response can have `chi_QQ(0,k) proportional to k^2`; equation (1) does not apply to it unless it is the positive acoustic fluid number used in (4)–(5). Likewise, a finite gap for atom–molecule conversion does not gap the common positive-number acoustic mode on a compressible branch.

For the original neutral particle model, the candidate positive count is only the conditional conservative NR reference current `N=N_++N_-`. To use the present theorem as its exact low-energy description one must establish a state and scale hierarchy supporting that current, one-fluid coflow, thermodynamic equilibrium or a zero-temperature coherent phase, and removal or controlled retention of composition/counterflow degrees of freedom. The microscopic exact signed `U(1)` by itself does not supply these assumptions. The full equal-density neutral coherent saddle analyzed in `COLLECTIVE_RESPONSE.md` has an odd instability, so it is not an example of a stable single-fluid equilibrium satisfying all the premises.

Finite-temperature two-fluid hydrodynamics, multiple independently conserved chemical potentials, normal kinetic states, solids, states with external support or momentum relaxation, topological/gauge constraints, and nonlocal critical phases are outside this one-current zero-temperature proof. In a genuine multicomponent fluid the acoustic susceptibility is a matrix and cross-responses can have different projections. No claim about its smallest eigenvalue follows by substituting a signed neutral density into (1).

The current conclusion therefore narrows the remaining route: a proposed restoring mechanism must either fail the positive acoustic-fluid premises in a physically established way, or exhibit an additional source/operator sector. An incompressible signed-charge mode or equal-time suppression alone cannot supply the missing gravitational-density kernel.

## 7. Primary-source check, provenance and continuation

Primary source authenticated on 19 October 2026: D. T. Son, *Low-Energy Quantum Effective Action for Relativistic Superfluids*, [arXiv:hep-ph/0204199v2](https://arxiv.org/pdf/hep-ph/0204199v2), version dated 20 May 2002. Equations (19)–(20) give the leading-derivative pressure action; equations (24)–(25) identify sound speed from the exact equation of state; equation (31) gives perfect-fluid stress and enthalpy. Its scope excludes omitted higher derivatives and finite-temperature hydrodynamics. Our `Theta=mu t+pi` corresponds to `Theta=mu t-varphi` in its background-source convention. Our `epsilon,p,n,mu` correspond directly to its energy, pressure, number and chemical potential. This verifies the superfluid EFT input and thermodynamic dictionary, conditional on the fluid phase; it does not establish that phase for the present particle model. The lapse/source algebra and static-force conclusion above were derived here. No full source file was retained, so no retained-PDF hash is claimed.

Evidence label: **analytic conditional theorem**. There is no new finite computation or scientific numerical run. The thermodynamic and Euler derivations are mutually consistent; the phase/lapse calculation independently checks the source factors and metric contact term. A fresh sibling derivation of the exact pressure/lapse source identities remains the coordinator's review obligation. The note does not claim a universal nonperturbative classification of the original quantum field theory. Its use of an exact equation of state allows corrections beyond mean field **within** the stated fluid effective description.

Continuation: the next discriminating input is an actual state of the original neutral system and its positive-energy acoustic projection. If it is a local stable causal one-current zero-temperature fluid with fixed `n,mu>0`, the positive `1/k^2` static tether is excluded in its mass/energy channel by (1)–(7). If it is another phase, compute its stress-energy source matrix and static spectral susceptibility before identifying an internal gapped or constrained density with gravitational mass. The rational nonlinear restoring law remains unconstructed.
