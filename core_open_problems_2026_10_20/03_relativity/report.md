# Problem 3: a covariant S2 candidate and its first constraint obstruction

**The requested relativistic completion is not achieved.** This checkpoint constructs a specific covariant parent of the **static S2 action**, derives its leading lensing relation and tensor principal symbol, and eliminates the scalar constraints on two specified backgrounds. It gives a new necessary parameter inequality and an explicit short-wavelength failure when that inequality is violated. It does **not** establish the four gates simultaneously, nor embed S3's conserved cold mass. Primary proof-audit verdict for the original four-gate claim: **incomplete, with the smallest missing implication being stability of the full constrained system on nonzero-polarization solutions**. Review provenance: self-review, not independent certification.

Owner: `/root/relativistic_completion`; base commit `431f22bd6fe998759b843d13113762d73356aec6`; task date 2026-10-20 (execution may be UTC 2026-10-21). Write scope is this directory only. Exact source identities are in `source_provenance.json`; executable evidence and software versions are in `run_001/manifest.json` and `run_001/results.json`. The script reads no untracked source, imports no repository module, and does not run other agents' experiments.

## 1. Contract and the authoritative action

The requested conclusion is a single covariant theory whose static weak-field limit is the current saturating law, whose photons and gravitating test bodies infer the same leading potential, whose tensor characteristics coincide with the matter light cone, whose Solar System is Newtonian within its precision tests, and whose physical perturbations are stable throughout the acceleration range, including the endpoints. A static energy Hessian, a diagram of fields, or a homogeneous-background calculation alone does not meet that contract.

The pinned source is `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md`, S2, lines 16–24, corroborated by CFG695 and `argon_push/AG4_law_from_action/IDEA.md`:

\[
 L_{S2}=-\frac{|\nabla\Phi-K\mathbf P|^2}{2K}-\rho_b\Phi
 -W_{\rm rem}(u)-\frac\gamma2|\nabla\mathbf P|^2,
 \quad K=4\pi G,\quad u=K|\mathbf P|,\quad \gamma=KL_*^2/2,
\]
\[
 KW'_{\rm rem}(u)=\frac{u^2}{a_0-u},\qquad 0\le u<a_0.
\]

Take the otherwise arbitrary additive potential constant to be zero at the origin. Then

\[
 W_{\rm full}(u)=\frac{a_0^2}{K}\left[-\frac u{a_0}-\log(1-u/a_0)\right],
 \qquad W_{\rm rem}=W_{\rm full}-\frac{u^2}{2K}.
\]

Expanding the square therefore gives `−|grad Phi|²/(2K)+P·grad Phi−W_full`, **not** `−|grad Phi|²/(2K)+P·grad Phi−W_rem`. The critical quadratic is in `W_full`; it is absent from `W_rem`. The latter starts at `u³/(3Ka0)`. For zero stiffness on a parallel static branch,

\[
g=\frac{u}{1-u/a_0},\quad g_N=g-u=\frac{g^2}{g+a_0},\quad
u=\frac{a_0g}{a_0+g}.
\]

This is the capacity-one canonical law, not the capacity-two quadratic law. At finite stiffness these algebraic relations are not pointwise equations in an arbitrary geometry.

The source's older `5.75 pc` floor is not used as the current bound: CFG820 has the newer `L* >= 24 pc` result. The `1 kpc` point is a tested grid edge, not an independently established upper bound. S3 additionally identifies P with a conserved collisionless mass displacement, `div P = rho−rho_bar`, `Pdot_L=−j_L`, with measured cosmic abundance. The construction below does **not** derive these identifications. It changes the dynamical interpretation of P, while retaining S2's static functional.

## 2. Prior obstructions and the changed premise

The main README and the whitepaper map record scalar, vector, and history-keyed lens-only routes, including photon/graviton cone splitting, lapse-response pollution, and the static equivalence of normalized history keys. Their modified-inertia/lens-only premises are not transplanted here: the candidate modifies the metric potential felt by both light and matter.

The newer CFG938 continuum action uses a projected four-Hessian of a scalar. The existing cold-covariant audit exhibits a homogeneous tensor kinetic correction `Q_T=1−3 gamma chi_dot²/K`; its proposed shear correction is then obstructed by the constrained fluid-vector calculation in the next audit. These are read-only prior results, not new discoveries or rerun experiments in this packet.

Three routes were discriminated:

1. **Original CFG938/shear-repaired family:** retains the known tensor or vector obstruction; no unchanged rerun.
2. **Legendre elimination into a khronon acceleration function:** reproduces S2 when stiffness and P kinetics are removed, but does not solve screening or the critical zero-acceleration endpoint.
3. **Independent clock plus polarization one-form with Hodge spatial stiffness:** pursued below. This changes the operator and the physical field content. It retains the entire flat static vector action, not only a curl-free sector, but its S3 bridge is missing.

No novelty claim is made. The khronon host is established prior art; the precise screened polarization proposal below was analyzed in this task, not located as a published completed theory.

## 3. The actual candidate action

Use `c=1`, signature `(-+++)`, positive K, and time and space coordinates with length units. Define

\[
n_\mu=-\frac{\partial_\mu T}{\sqrt{-g^{\alpha\beta}\partial_\alpha T\partial_\beta T}},\quad
h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,\quad
a_\mu=n^\alpha\nabla_\alpha n_\mu,\quad \theta=\nabla_\mu n^\mu.
\]

T has a timelike gradient. P is a covector constrained by `n^mu P_mu=0`, so `u=K sqrt(P_mu P^mu)`. D is the intrinsic spatial covariant derivative, and

\[
F_{\mu\nu}=2\nabla_{[\mu}P_{\nu]},\quad E_\mu=n^\alpha F_{\alpha\mu},\quad
F^\perp_{\mu\nu}=h_\mu{}^\alpha h_\nu{}^\beta F_{\alpha\beta},\quad d=D_\mu P^\mu.
\]

The proposal is

\[
S=\int\!\sqrt{-g}\left[
\frac{R-2\Lambda-\beta\theta^2}{4K}+P^\mu a_\mu-W_{\rm full}(u)
+\frac\eta2 E_\mu E^\mu-\frac\gamma2 d^2
-\frac\gamma4F^\perp_{\mu\nu}F_\perp^{\mu\nu}+\lambda n^\mu P_\mu
\right]d^4x+S_m[g,\mathrm{matter}].
\]

Here beta and eta are **new unfixed coefficients**; `beta>0`, `eta>0` are the branch tested. Beta is dimensionless; `[eta]=[gamma]=[K] length²`. In geometrized units `[u]=[a0]=length^−1`, `[P]=[u]/[K]`; the physical acceleration used in SI is `c²u`. Thus the high-frequency polarization speed in units of c is `sqrt(gamma/eta)`. A multiplier enforces orthogonality; it is eliminated exactly in adapted coordinates, not discarded as a perturbation.

In `T=t` gauge, `P_0=N^i P_i`, and the action density divided by `N sqrt(h)` is exactly

\[
\frac{{}^{(3)}R+K_{ij}K^{ij}-(1+\beta)\theta^2-2\Lambda}{4K}
+P^iD_i\log N-W_{\rm full}
+\frac\eta2 E_iE^i-\frac\gamma2(D_iP^i)^2-\frac\gamma4F_{ij}F^{ij},
\]
\[
K_{ij}=\frac{\dot h_{ij}-D_iN_j-D_jN_i}{2N},\quad
E_i=N^{-1}(\dot P_i-\mathcal L_{\mathbf N}P_i),\quad F_{ij}=\partial_iP_j-\partial_jP_i.
\]

This expression fixes every operator and the clock/shift dependence. It is not shorthand for an unspecified covariantization.

### Field equations used in the checks

Let `f(u)=K W_full'(u)=u/(1−u/a0)`. The exact spatial P equation in this gauge is

\[
\frac{\eta}{N\sqrt h}(\partial_t-\mathcal L_{\mathbf N}^{\rm density})
(\sqrt h E)^i
=a^i-f(u)\widehat P^i+\frac\gamma N D^i(Nd)
+\frac\gamma N D_j(NF^{ji}).
\]

The Lie derivative on the left acts on a vector density. At the origin `f(u) P_hat` extends continuously as `K P` to linear order. Lapse variation gives

\[
\frac{{}^{(3)}R-K_{ij}K^{ij}+(1+\beta)\theta^2-2\Lambda}{4K}
-d-W_{\rm full}-\frac\eta2E^2-\frac\gamma2d^2-\frac\gamma4F^2=\rho_n,
\]

where `rho_n=−(1/sqrt(h)) delta S_m/delta N`. The exact shift equation is

\[
\frac1{2K}D_j[K^{ji}-(1+\beta)\theta h^{ji}]
+\eta[P^iD_jE^j+E^jF_j{}^i]+J_m^i=0,
\]

with `J_m^i=(1/sqrt(h)) delta S_m/delta N_i` fixing the momentum sign convention. The spatial metric equations are the remaining variations of the displayed ADM action. Their full nonlinear expansion, clock constraint propagation, and full degree count have **not** been completed here. Covariance gives the T equation from projected variation of n, `nabla_mu(N_T h_nu^mu E_n^nu)=0`; this identity alone is not a well-posedness proof.

## 4. Static recovery and lensing actually derived

On a static clock-aligned weak-field branch, `E=theta=0`. For fields decaying sufficiently at infinity, or compatible periodic boundary conditions,

\[
\int[(\partial_iP^i)^2+\tfrac12F_{ij}F_{ij}]d^3x
=\int\partial_iP_j\partial_iP_j\,d^3x.
\]

This proves recovery of S2 including independent transverse P, up to a flat spatial boundary term. On curved leaves the difference is a spatial Ricci coupling; it cannot be silently equated to the rough covariant-gradient norm.

For `ds²=−(1+2Phi)dt²+(1−2Psi)dx²`, retain the leading slow-motion, weak-potential action (restoring potentials divided by c² if using SI):

\[
L_{\rm weak}=\frac{(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi}{2K}
-\rho_b\Phi+P\cdot\nabla\Phi-W_{\rm full}-\frac\gamma2|\nabla P|^2.
\]

Varying both potentials independently gives

\[
\Delta\Psi-K\nabla\cdot P=K\rho_b,\quad
\Delta(\Phi-\Psi)=0.
\]

With the same isolated boundary condition for the two potentials, `Psi=Phi`. P variation gives

\[
\nabla\Phi=f(u)\widehat P-\gamma\Delta P.
\]

Massive geodesics respond to Phi; weak deflection responds to `(Phi+Psi)/2=Phi`. The equality follows from the metric variation, rather than from assigning a phantom mass to photons. It is a **leading-order static result**. W and stiffness have anisotropic stresses at higher order; exact equality of the full relativistic potentials is not proved and generally should not be expected. Boundary conditions, clock alignment, slow motion, and the stated weak-field ordering are hypotheses, not outputs.

Removing eta and gamma and eliminating P gives an acceleration function `V(g)=a0[g−a0 log(1+g/a0)]/K`, equivalently `f_BM=−2K V` and `chi=f_BM'/(2g)=−a0/(a0+g)`. This translates the candidate's unscreened algebraic branch into the Blanchet–Marsat notation. Their published model and Flanagan's follow-up derive leading `Psi=Phi`, but their stability results do not establish the present model's stability. In particular, our `f_BM` is unbounded as `g→infinity`, unlike BM's stated high-acceleration asymptotic condition. [Blanchet & Marsat, PRD 84, 044056, §§II–IV](https://www2.iap.fr/users/blanchet/images/PhysRevD.84.044056.pdf); [Flanagan, arXiv:2302.14846v3, Eqs. 1–9, 14, 26 and §IV](https://arxiv.org/html/2302.14846v3).

## 5. Tensor principal symbol, including polarized backgrounds

Freeze coefficients at a regular background point in a clock-rest frame and take wavevector `k` along z. Keep arbitrary `P=(Px,Py,Pz)`. A spatial TT perturbation obeys `k_i hTT_ij=0`, `tr hTT=0`. Its derivative contributions satisfy

\[
\delta d|_{\partial h}=-P_j\partial_i h^{TT}_{ij}=0,\quad
\delta F^\perp|_{\partial h}=0,\quad
\delta E|_{\partial h}=0,\quad
\delta\theta|_{\partial h}=0.
\]

The electric identity uses **covector** P as the independent ADM variable; otherwise time derivatives of the metric can appear merely from a field redefinition. The acceleration coupling has a possible `hTT_ij P_j partial_i(delta N)` term, which is zero at principal order by transversality. Nonzero background gradients multiplying second variations supply at most one derivative on the metric perturbation here, not a competing tensor kinetic term. The principal TT action is consequently

\[
S_{TT,\rm principal}^{(2)}=\frac1{16K}\int[(\dot h^{TT}_{ij})^2-(\partial_kh^{TT}_{ij})^2]d^4x.
\]

**Result: c_T=c with positive tensor kinetic sign in the regular local principal system.** This is stronger than a P=0 check, but remains a classical geometric-optics statement. It is not a finite-frequency waveform, graviton decay, loop stability, or proof that the other constraint sectors remain regular.

An adversarial control replaces Hodge stiffness by the naive `−gamma |DP|²/2`. With `hxx=hplus`, `hyy=−hplus`, `hxy=hcross`, direct Christoffel contraction gives

\[
|\delta(D_iP_j)|^2=\tfrac12 k^2|P|^2(h_+^2+h_\times^2),
\]

which changes the tensor spatial coefficient and gives `c_T²=1+2K gamma |P|²` for that alternative. Vanishing corrections at P=0 therefore prove nothing about its polarized tensor cone. The executable check verifies both TT polarizations with arbitrary P components.

## 6. Dynamics: distinguish a static Hessian from the constrained modes

For `0<u<a0`, the Cartesian P-Hessian of W_full has eigenvalues

\[
M_\perp=\frac K{1-u/a_0},\qquad M_\parallel=\frac K{(1-u/a_0)^2}.
\]

Eliminating the Newtonian potential subtracts `K khat khat^T`; thus its static quadratic energy is strictly positive for nonzero u, with additional `gamma k² I`. At u=0 it is semidefinite at k=0. None of these statements determines clock/metric kinetic signs.

### Auxiliary zero-acceleration Minkowski reduction

Take `Lambda=0`, no matter, `T=t`, P=0, N=1, `hij=deltaij`: an exact solution of the **auxiliary action family in which Lambda and finite a0 are independent parameters**. This is not the physical target-vacuum endpoint when S1 ties `a0=kappa c sqrt(G rho_DE)` to pure cosmological-constant dark energy: setting Lambda to zero then also sends a0 to zero, so the fixed-finite-a0 calculation below cannot be transplanted to that endpoint. It is a flat-background algebra check and a candidate local-flat approximation whose applicability requires a scale analysis. The finite-a0 target endpoint instead requires a de Sitter background and a fresh coupled clock/polarization reduction, which is not performed here.

Within that auxiliary family, in scalar spatial gauge `hij=e^(2zeta)deltaij`, set `N=1+n`, `Y=div Nshift` and use complex Fourier modes at `k>0`. The lapse constraint fixes

\[
p_L=-ik\zeta/K.
\]

The unreduced scalar quadratic action, with a common real-mode normalization, is

\[
L_0^{(2)}=\frac{-(6+9\beta)\dot\zeta^2+(4+6\beta)\dot\zeta Y-\beta Y^2+2k^2\zeta^2}{4K}
+\frac{\eta k^2}{2K^2}\dot\zeta^2-\frac{(K+\gamma k^2)k^2}{2K^2}\zeta^2.
\]

Eliminating the shift gives `Y=(2+3beta) zetadot/beta` and

\[
L_{0,red}^{(2)}=\tfrac12[Q_0(k)\dot\zeta^2-\gamma k^4\zeta^2/K^2],\quad
Q_0=\frac{2+3\beta}{K\beta}+\frac{\eta k^2}{K^2},
\]
\[
\omega_0^2=\frac{\gamma k^4}{K(2+3\beta)/\beta+\eta k^2}>0.
\]

The two transverse P modes have `L_T=eta |pdot_T|²/2−(K+gamma k²)|p_T|²/2`, hence `omega_T²=(K+gamma k²)/eta`. Vector metric shifts have their usual positive spatial constraint term and vanish in this P=0 vacuum. Together with two tensors these are the modes of this **linearized regular nonzero-k sector**, not a nonlinear degree-count theorem. The EH scalar coefficient agrees with the established khronometric result after `lambda_BPS=1+beta`, `M_P²=1/(2K)`. [Blas, Pujolàs & Sibiryakov, arXiv:0909.3525v1, Eqs. 11–19](https://arxiv.org/html/0909.3525v1).

As `k→0`, `omega_0²~gamma beta k⁴/[K(2+3beta)]`; as `k→infinity`, its front-speed squared tends to `gamma/eta`. The exactly homogeneous `k=0` constraint rank and `beta=0` branch must be treated separately. A positive finite-k spectrum does not show absence of strong coupling, nonlinear caustics, or a well-posed global evolution at u=0. No such assertion is made.

### Polarized aligned high-frequency reduction and an actual failure interval

For a static clock-aligned background with P nonzero, choose `k parallel P`. Denote `P=|Pbar|`, and let q be the longitudinal covector perturbation. At high k the lapse equation gives `zeta=iKq/k+O(k^−2)`. Keep the shift through elimination. Its leading scalar block is

\[
L_{\parallel,principal}^{(2)}=\frac\eta2(\dot q-PY)^2-\frac\beta{4K}Y^2-\frac\gamma2 k^2q^2.
\]

In variables `(qdot,Y)`, the kinetic/constraint matrix is

\[
\begin{pmatrix}\eta&-\eta P\\-\eta P&\eta P^2-\beta/(2K)\end{pmatrix}.
\]

This is a high-frequency block, not a finite-k approximation to a fully solved halo. Lower background derivatives and potential curvature contribute subleading terms at fixed regular `u<a0`. For

\[
D=\beta-2K\eta P^2\ne0,
\quad Y=-\frac{2K\eta P}{D}\dot q,
\]
\[
L_{\parallel,red}^{(2)}=\tfrac12\left[\frac{\eta\beta}{D}\dot q^2-\gamma k^2q^2\right],\quad
c_\parallel^2=\frac\gamma\eta\frac D\beta.
\]

If D is negative, the reduced scalar kinetic coefficient is negative **and** `omega²/k²` is negative: this block has a short-wavelength instability when these wavelengths lie within the candidate's intended validity range. At D=0 the shift equation is `−eta P qdot=0`; the formula cannot be continued through that rank-changing constraint. It is not an infinite-frequency mode.

The critical polarization is

\[
u_{crit}=\sqrt{\frac{\beta K}{2\eta}}.
\]

If `beta<2 eta a0²/K`, this lies strictly inside the allowed saturation domain; the adverse interval is `ucrit<u<a0`. On the unscreened algebraic branch its finite acceleration is `gcrit=a0 ucrit/(a0−ucrit)`. Example: `K=eta=gamma=beta=1`, `a0=2`, `u=1` gives D=−1 and `c_parallel²=−1`, with u below the cap. The example is a local principal-symbol counterexample, not a solved global astrophysical background.

Thus **beta >= 2 eta a0²/K is necessary to avoid this aligned failure at every finite interior u; strict > is required for a uniform nonzero shift margin up to saturation**. This is not sufficient for full stability. If eta=gamma, the strict inequality in SI is `beta>(a0 L*/c²)²`. For oblique waves the shift determinant has factor `1−2K eta P_L²/beta+4K eta |P_T|²`; the executable verifies this independent matrix identity. No all-angle reduced-mode positivity claim follows from that determinant alone.

As `u→a0`, the potential Hessian diverges and the endpoint is outside the action's finite-energy domain. With a strict shift margin the displayed kinetic obstruction is avoided in this limit, but arbitrary acceleration is **not** uniformly controlled: potential eigenfrequencies, background length scales and the order of the high-k/saturation limits need an EFT analysis. Sending `u→a0` before freezing a finite Hessian invalidates the stated principal reduction.

## 7. Solar System and the four-gate board

On the screened spherical inner branch, `P` is small even when the baryonic field is large. Linearizing W_full gives `grad Phi=KP−gamma Delta P`; outside a point baryonic source Gauss gives `grad Phi−KP=(GM/r²) rhat`. The radial vector Laplacian then has the particular solution

\[
P_r=GM/(2\gamma),\quad u_{inner}=GM/L_*^2,\quad u_{inner}/g_N=r^2/L_*^2.
\]

For the Sun this is `2.42e−16 m/s²` at 24 pc and `1.39e−19 m/s²` at 1 kpc; the fractional values at 1 AU are `4.08e−14` and `2.35e−17`. These are calculated from the stated solar GM, AU and parsec constants. They show the static screening scale, **not** an ephemeris likelihood or the full boundary-matched solution. Homogeneous radial terms and the Galactic external field need matching. The independent clock introduces preferred-frame effects: its PPN parameters, moving-source response, binary radiation, and strong-coupling scale were not computed. The Solar System gate therefore remains open.

| Gate | Result in this checkpoint | Remaining qualification |
|---|---|---|
| Lensing equals dynamics | Derived at leading static weak-field order, with isolated boundary conditions | Higher-order anisotropic stress and nonstationary/unaligned clock solutions uncomputed |
| `c_GW=c` | Derived for the regular classical tensor principal symbol with arbitrary local P | A singular non-tensor constraint system is not rescued by this identity; finite-frequency/quantum effects untested |
| Newtonian Solar System | The S2 static screening asymptote is reproduced | Full PPN/preferred-frame and exterior-field boundary problem not passed |
| Stable at every acceleration | Auxiliary unpolarized Minkowski finite-k spectrum is positive when Lambda and finite a0 are treated independently; aligned principal inequality derived | S1-linked finite-a0 de Sitter endpoint, general on-shell backgrounds, oblique modes, nonlinear well-posedness and strong coupling unproved; forbidden coefficient range has an explicit failure |

The original four-gate goal is open even on the candidate's own field content. In addition, S3's conserved mass/current interpretation and cosmological abundance are not consequences of this action. Merely adding `−mn` or identifying the clock with the three-label medium would change the constraint system and require repeating the calculation; the prior CFG938/vector obstruction explains why that step is load-bearing.

## 8. Evidence, source checks and continuation

`checks.py` performs exact symbolic identities, direct connection contraction, independent shift-matrix determinant checking, two genuine sign/operator mutations, and dimensional Solar System arithmetic. It does not fit data, solve a halo, integrate cosmology, or prove nonlinear stability. The analytic reductions above supply the scope; a count of checks cannot broaden it. Run from this directory with the installed computation-audit runner, `contract.json`, input `checks.py`, output a **new** `run_XXX` directory and result `run_XXX/results.json`; the exact invocation is in `run_001/manifest.json`. Validate that manifest with `validate_manifest.py --root` set to this directory.

External-source checks on 2026-10-21 UTC:

- **Blanchet & Marsat:** authenticated author-hosted published PRD PDF, DOI 10.1103/PhysRevD.84.044056; extracted khronon/acceleration definitions and static weak-field metric result. Translation is verified only for the eta=gamma=beta=0 acceleration-function branch. Its all-acceleration conditions do not certify this candidate. No full-text copy retained.
- **Flanagan:** authenticated arXiv v3 dated 2023-09-24; extracted its restricted low-acceleration/symmetric-background stability scope and warning about nonstationary clock effects. Application as an all-background theorem here is **inapplicable**. No full-text copy retained. The HTML acceleration-number rendering is inconsistent with the published BM value and is not used numerically.
- **Blas–Pujolàs–Sibiryakov:** authenticated arXiv v1 dated 2009-09-21; extracted Eq. 12's khronometric scalar kinetic coefficient. The convention dictionary above checks that limited coefficient; its different action and positivity conditions are not transferred as a health certificate. Initial attempts at nonexistent v2 PDFs failed; v1 HTML was then read successfully.

The durable source-provenance record pins local file bytes and these exact external locators. External pages were read but not retained as source files, so no external-content hash is asserted.

The next discriminating step is a full constrained quadratic reduction on an **actual static polarized solution** of this candidate, retaining the lapse, all shifts, both P transverse components, and clock equations, with arbitrary k/P angle. Impose the derived shift margin first; do not re-test already forbidden coefficients. For the physical zero-acceleration endpoint, enforce S1 and derive the de Sitter-plus-clock quadratic system at finite a0; the auxiliary Lambda=0 check does not settle it. Then compute cubic normalization and the zero-momentum constraint branch before calling that endpoint healthy. A separate indispensable decision is whether this new P one-form can realize S3's conserved cold-mass current without changing those results. Only after that bridge should preferred-frame/PPN and cosmological perturbations be scored. These are deferred open routes, not exhausted impossibility claims.
