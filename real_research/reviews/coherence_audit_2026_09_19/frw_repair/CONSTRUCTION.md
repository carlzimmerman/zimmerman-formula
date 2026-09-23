# Constructive continuation: the candidate's own expanding solution

**Superseding physical interpretation:** see [the closure continuation](../closure_resume/STATUS.md). The short unitary-gauge amplitudes in section 3 do not by themselves establish gravitational runaway. The follow-up reconstructs the Bardeen potentials, distinguishes a response transient from physical growth, and supplies longer independent checks. The kinetic theorem and exact background below remain unchanged.

The theory is not closed. This continuation obtains a general positive-kinetic-energy theorem for the corrected scalar sector, derives a consistent expanding background, and evolves both physical scalar modes without deleting a stiff direction. It also tests a concrete response extension. The interpretation of its short-interval amplification is corrected in the follow-up linked above.

The criterion throughout is consistency of the candidate's own action and equations. No reference cosmology's growth curve is imposed. The background below contains the scalar and a cosmological constant; radiation and baryonic perturbations remain additional work. No global novelty claim is made.

This is a continuation of the September 12–19 repository review. The initial review covers selected load-bearing developments among more than 600 commits, rather than every changed file. Existing research files were left unchanged. The reproducible continuation is confined to this new directory.

## 1. A corrected action and an exact background

Use the outside-kernel healing variant permitted by `THE_ACTION_2026-09-05.md`, with \(c_{13}=0\), a hypersurface-orthogonal clock, and one physical metric. Its ADM density, omitting the common positive gravitational normalization, is

\[
N\sqrt h\left[R^{(3)}+K_{ij}K^{ij}-(1+c_2)K^2-2\Lambda
+c_{14}a_i a^i+2(2-K_B)a^iD_i\phi
-(2-K_B)\beta D_i\phi D^i\phi-F(Q)\right]
\]

with the spatial healing term added separately. Here \(a_i=D_i\log N\), \(Q=n^\mu\nabla_\mu\phi\), and \(K_{ij}=(\dot h_{ij}-D_iN_j-D_jN_i)/(2N)\). The quadratic spatial coefficient is \(\beta=(2-K_B)/(2-c_{14})\). Nonlinear MOND terms that start beyond quadratic order about \(Y=0\) are outside this calculation.

The healing operator must differentiate the **projected gradient**. With \(q_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu\),

\[
V_\mu=q_\mu{}^\nu\nabla_\nu\phi,\qquad
A_{\mu\nu}=q_\mu{}^\alpha q_\nu{}^\beta\nabla_\alpha V_\beta
=q_\mu{}^\alpha q_\nu{}^\beta\nabla_\alpha\nabla_\beta\phi+QK_{\mu\nu}.
\]

Thus \(A_{\mu\nu}=0\) on homogeneous flat FRW. Squaring only the projected spacetime Hessian is a different operator. In unitary clock gauge, for a mode along \(x\), the intended quadratic contribution is \(-(2-K_B)\xi^2 P_{,xx}^2/a\). Its tensor-norm and trace-square forms agree in this flat integrated quadratic calculation, not in general nonlinear curved geometry.

For the exponential well \(F=-A\exp[(Q-Q_0)/\epsilon]\), let \(F_1=F_Q\), \(F_2=F_{QQ}\), and \(G_c=1+3c_2/2\). Exact charge conservation and the lapse equation give

\[
a^3F_1=F_{10},\quad Q(a)=Q_0-3\epsilon\log a,\quad
F=\epsilon F_1,\quad F_2=F_1/\epsilon,
\]
\[
6G_cH^2=F-QF_1+2\Lambda,\qquad
\dot Q=-3\epsilon H,\qquad \dot H=\frac{QF_1}{4G_c}.
\]

The normalized density \(R=F-QF_1\) and pressure \(\Pi=-F\) obey \(\dot R+3H(R+\Pi)=0\). `background_check.py` verifies these identities, the minisuperspace lapse variation, and the scalar current's gauge transformation.

An important singular-approximation issue follows: although \(\dot Q=O(\epsilon)\), \(F_2\dot Q=-3HF_1\) is finite. Freezing \(Q\) while evolving \(F_1\propto a^{-3}\) violates this chain rule. A small error in the background energy is therefore not enough to justify that approximation in the perturbations.

## 2. A general theorem, rather than a positive numerical sample

`adm_unitary.py` derives the four scalar equations for lapse, shift, spatial curvature \(\Phi\), and scalar perturbation \(P\). Lapse and shift are algebraic constraints. `general_kinetic.py` eliminates them, including exact time derivatives of their solutions, leaving a two-field second-order system.

Set

\[
\alpha=c_{14}>0,\quad b=c_2>0,\quad t=-F_1>0,\quad
a,\epsilon,k>0,\quad r=3b+2.
\]

Here \(t\) in the theorem denotes the positive quantity \(-F_1\), not the time coordinate. \(H,Q\) are arbitrary real numbers. The positive denominator is

\[
D=4H^2a^2\epsilon r+a^2btQ^2+2\alpha b\epsilon k^2.
\]

The reduced kinetic matrix is

\[
K_{11}=\frac{4a^3r(a^2tQ^2+2\alpha\epsilon k^2)}D,\quad
K_{12}=\frac{4Ha^5tQr}D,\quad
K_{22}=\frac{2a^3t(2H^2a^2r+\alpha b k^2)}D.
\]

Its determinant factors as

\[
\boxed{\det K=\frac{8a^6\alpha t k^2(3b+2)}D>0.}
\]

Together with \(K_{11}>0\), this proves positive kinetic energy for every nonzero scalar velocity pair. `PositiveKinetic.lean` proves denominator positivity, the determinant identity, positive principal minors, the two-dimensional Sylvester implication, and the resulting quadratic-form positivity. Its axiom output uses only `propext`, `Classical.choice`, and `Quot.sound`.

An independent analytic derivation explains the factorization. Write \(v=\dot\Phi\), \(u=\dot P\), lapse perturbation \(\psi\), and shift divergence \(\sigma=\Delta B/a\). The terms governing the velocity Hessian are

\[
L_2/a^3=-3r(v+H\psi)^2-2r(v+H\psi)\sigma-b\sigma^2
+\alpha(k/a)^2\psi^2+\frac{t}{2\epsilon}(u-Q\psi)^2.
\]

The shift equation gives \(\sigma=-r(v+H\psi)/b\). Substitution leaves

\[
\frac{2r}{b}(v+H\psi)^2+
\frac{t}{2\epsilon}(u-Q\psi)^2+
\alpha(k/a)^2\psi^2.
\]

Eliminating the lapse from these positive squares reproduces every matrix entry above. `kinetic_independent.py` independently checks the Schur complement and its equality to the full ADM reduction. `minkowski_control.py` additionally matches all 16 matrix entries against the separately reconstructed covariant calculation on an on-shell Minkowski vacuum.

**Scope:** this is a quadratic scalar kinetic theorem, conditional on the specified action-to-matrix derivation. Lean checks the matrix algebra; it does not formalize differential geometry or the variational derivation. There is no claim of gradient stability, nonlinear health, or a uniform lower kinetic bound as \(k\to0\) or \(\alpha\to0\). The chosen \(\beta\) relation also requires \(\alpha\ne2\). The numerical examples use \(0<\alpha<2\).

## 3. What happens when both modes are evolved

The constant-coefficient example uses \(K_B=1/5\), \(c_{14}=1/40000\), \(c_2=c_{14}/(1-2c_{14})\), \(\epsilon=10^{-9}\), \(Q_0=1\), and \(F_{10}=-1.86/(1-\epsilon)\). Units set \(H(a=1)=1\); \(\Lambda=3G_c-(\epsilon-1)F_{10}/2\) enforces that normalization. The healing length is 4 pc. The charge amplitude is an explicit illustrative input, not a derived cosmic abundance. The conversion \(c/H_0=299792458/67400\) Mpc only defines the quoted wavelength units.

The full two-mode system retains a fast direction. A 65-digit instantaneous spectrum scan covers \(a\in\{1,.5,.1,.01,.001\}\), \(k\in\{.01,.1,1\}\,\mathrm{Mpc}^{-1}\). All sampled kinetic matrices are positive. An instantaneous eigenvalue alone is not an integrated growth history.

To go beyond that diagnostic, `evolve_local.py` evolves the time-dependent equations in \(N=\log a\), including \(\dot Q,\dot H,\dot F_1\). Initial data select the largest-real-eigenvalue direction at the interval start. Linear amplitudes can be scaled arbitrarily small.

| Example | Interval | Wavenumber | Amplification of \(\Phi\) | Amplification of \(P\) |
|---|---|---|---|---|
| Constant coefficients | \(a=.1\) to \(.1e^{.01}\) | \(.1\,\mathrm{Mpc}^{-1}\) | 22.43 | 22.61 |
| Response trial below | \(a=.5\) to \(.5e^{.004}\) | \(.001\,\mathrm{Mpc}^{-1}\) | 17.81 | 17.86 |

These are bounded numerical amplification witnesses, not universal instability theorems or predictions for an arbitrary primordial state. DOP853 at two tolerances and Radau agree; independent 50-digit RK4 evolution with 200/400-step convergence agrees to better than \(2\times10^{-9}\) in the final state relative to the tighter adaptive run. Step-doubling discrepancies are below \(1.2\times10^{-8}\). This is numerical validation, not interval certification.

## 4. A constructive response extension and its initial test

There is freedom to alter perturbations without changing this homogeneous background. The operators \(a_i a^i\) and \(D_i\phi D^i\phi\) vanish on the background. Their coefficients can therefore depend on \(Q\). At quadratic order they are background coefficients; their perturbations multiply quadratic operators and first contribute at cubic order. Their **time derivatives** must still be retained when differentiating the constraints.

I tested

\[
c_{14}(Q)=\frac{\alpha_{\max}v(Q)}{\alpha_{\max}+v(Q)},\qquad
v(Q)=10^{-7}\exp\!\left[\frac{4(Q-Q_0)}{3\epsilon}\right],\qquad
\alpha_{\max}=1/2,
\]

with \(c_2=.03\) and \(\beta(Q)=(2-K_B)/(2-c_{14}(Q))\). On the exact background, \(v=10^{-7}a^{-4}\) and \(\dot c_{14}=-4Hc_{14}(1-c_{14}/\alpha_{\max})\). This preserves the selected quadratic MOND cancellation. It does not establish the full nonlinear galactic law for a varying coefficient.

The first grid \(k=.01,.1,1\,\mathrm{Mpc}^{-1}\) appeared encouraging: the largest instantaneous rate was about \(1.605H\). Extending to \(k=.0001,.001\,\mathrm{Mpc}^{-1}\) exposed rates above \(1200H\) near \(a=.5\), including \(k/(aH)\approx5.07\) for \(k=.001\,\mathrm{Mpc}^{-1}\). The time-dependent witness in the table confirms rapid amplification of selected unitary-gauge data there. **Correction:** the follow-up finds no comparable Bardeen-potential growth over that short interval, so this observation alone does not disqualify the response. A separate longer physical-transfer test at a different epoch is documented in the closure continuation. This response is not a certified repair.

The general kinetic theorem survives. It provides a constraint on future constructions: an allowed positive response can be explored without repeatedly rediscovering the absence of kinetic ghosts. But a response must also control the actual evolution over wavelengths and epochs, and its nonlinear interactions must be checked. In particular, steep \(Q\)-dependence has not been shown to avoid strong coupling. I have not carried out a full PPN calculation for this modified theory.

The power-two prototype, the narrower power-four scan, and a timed-out direct covariant FRW build are preserved as exploratory records. The final verification uses the independent ADM route and the **extended** power-four grid. The failed direct build is not evidence for a mathematical obstruction.

## 5. The reframing that would move closure forward

Use a single reduced action to connect three questions that have too often been tested separately: the homogeneous charge, the MOND response, and the two physical scalar modes. The original well-shape scan conflates these. We now have an exact background and a reusable positive-kinetic theorem; the unresolved implication is a bound on the evolution of the remaining physical modes for the same action and parameter choices.

A concrete next mathematical target is a coercive, physically normalized quadratic energy \(E_k(N)=z^TP_k(N)z\) for the exact reduced system \(z_N=A_k(N)z\), satisfying

\[
P_k\succ0,\qquad P_k'+A_k^TP_k+P_kA_k\preceq C(N)P_k,
\]

with an explicit controlled integral of \(C\), wavelength range, and bounds comparing \(P_k\) to physical perturbation amplitudes. Those comparison bounds are essential: an arbitrarily rescaled energy could otherwise hide the growth. A pointwise eigenvalue scan does not provide this theorem. A candidate satisfying it would then need galactic/cluster solutions and a selection mechanism for their amplitudes, derived from the same action.

The numerical normalization \(\kappa=1/2\) is a distinct remaining issue. This construction does not remove the written action's freedom to choose its vacuum constant independently of the MOND scale. To derive the coefficient, an additional physical relation must actually remove that freedom; a Lean proof of a relation inserted as an assumption cannot do so. That is a structural target for a new principle, not a requirement to imitate another cosmology.

## 6. Reproduction and status

`constructive_contract.json` fixes the action, domains, grids, parameter choices, and non-claims. `run_verified/manifest.json` pins execution inputs and output hashes; `summary.json` separates successful checks from the still-incomplete physical goal. `run_verified/` also contains the generated equations, reduced matrices, spectra, and local evolution witnesses.

For a direct rerun, supply a new evidence directory:

```bash
python3 real_research/reviews/coherence_audit_2026_09_19/frw_repair/verify_constructive.py real_research/reviews/coherence_audit_2026_09_19/frw_repair/run_direct
```

The direct command refreshes intermediate output directories. Use the computation-audit runner with the contract and a fresh output directory to obtain a new manifest. Existing `run_verified` snapshots document this review's executed checkpoint.

Five further Lean theorems supplement the initial review's thirteen bounded algebraic certificates. Their number is not evidence of physical closure. The substantive new result here is the universal kinetic factorization, supported by two independent derivations, together with an exact two-mode evolution system that can test the next proposed mechanism coherently.
