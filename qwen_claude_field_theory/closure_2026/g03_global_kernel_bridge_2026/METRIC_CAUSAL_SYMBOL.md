# The constrained metric Hamiltonian: a causal-response obstruction

2026-09-05 local date. Follows `METRIC_CONSTRAINT.md`; does not change that
study's archived inputs or outputs. No empirical data were used here.

**Primary verdict: conditional no-go.** The complete spacetime principal
system has an instantaneous curvature response for the exact exponential
law. This cannot be removed by restoring tensor or vector components: those
are included in this calculation. Lifting the result to an unconditional
nonlinear verdict still requires the regular-background and source-domain
assumptions stated below. A complete relativistic MOND theory is not claimed.

## 1. Same Hamiltonian, larger calculation

In c=1 units, with the overall gravitational 1/(16 pi G) suppressed,

\[
H=\int d^3x\left[N\mathcal H_{\rm GR}+N^i\mathcal H_i
-2N\sqrt h a_0^2F(a^2/a_0^2)
+\lambda(\pi-\sqrt h\bar\pi)\right]+H_m,
\]
\[
F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}],\quad
a_i=D_i\ln N,\quad
\bar\pi={\int\pi\,d^3x\over\int\sqrt h\,d^3x}.
\]

The prior report gives its functional variation, static equation, and
separate homogeneous reduction. Here we derive the full spacetime principal
response at a smooth zero-momentum background point with a!=0. We retain
both time and spatial derivatives; this is not a quasistatic approximation.

Choose an orthonormal spatial frame and a Fourier mode with wavevector
(0,0,k), q=k^2>0. There are six independent spatial metric components,
six canonical momenta, three shifts, lapse n and trace multiplier lambda.
For off-diagonal entries, the independent canonical p_ij=2 pi^ij.
The exact principal Hamiltonian constructed in the script is

\[
H_2=\operatorname{tr}(\pi^2)-\tfrac12(\operatorname{tr}\pi)^2
+2(\pi k)\cdot b-L_{R,2}-nR_1-2\alpha q n^2
+\lambda\operatorname{tr}\pi,
\]
\[
R_1=q\operatorname{tr}h-k^Thk,
\]
\[
L_{R,2}=-\tfrac q4\operatorname{tr}(h^2)
+\tfrac q4(\operatorname{tr}h)^2
+\tfrac12|hk|^2-\tfrac12(k^Thk)\operatorname{tr}h.
\]

All quantities are perturbation amplitudes. Minimal matter coupling adds
\(n\rho-\tfrac12h_{ij}S_{ij}-b_iJ_i\), with rho=T00 and S_ij=Tij.
Cosine amplitudes are used for h,n,rho,S_ij and sine amplitudes for b,J.
Time dependence is exp(-i omega t). The source obeys
\(-i\omega\rho+kJ_z=0\) and \(-i\omega J_i-kS_{iz}=0\).
The code parametrizes the general conserved source with rho and five
independent spatial-stress components; no stress is inserted after variation.

We vary all 17 variables, then impose only the three spatial gauge choices
hzz=hxz=hyz=0. The resulting **20 equations** are solved together. Substituting
the solution back gives twenty exact zero residuals. The metric solution
retains the tensor wave poles; for example,

\[
h_{xy}={S_{xy}\over k^2-\omega^2}.
\]

There is no assignment of Phi, Psi, a PPN coefficient or a causal answer.

### All-metric principal Dirac count

The generic nonzero-mode calculation now includes every metric polarization,
not just the scalar block. The computed constraint generations are

1. p_n, p_bx, p_by, p_bz, p_lambda.
2. 4 alpha n+hxx+hyy, p_xz, p_yz, p_zz, p_xx+p_yy.
3. n.
4. lambda.

Their actual 12 by 12 Poisson matrix is in the result JSON. Its computed rank
is 6: six first-class and six second-class constraints in a 22-dimensional
phase space leave **two gravitational canonical pairs**. Further preservation
closes; only the three shift primary multipliers remain free. This remains a
principal quadratic result, not nonlinear closure. The earlier study's k=0
and y=0 analyses are separate; neither is inferred by dividing by k or 1-alpha.

## 2. The observable that prevents a gauge-potential false alarm

Contract the linearized Ricci tensor directly with the local observer's time
direction. In the chosen amplitude convention,

\[
R_{00}^{(1)}=-i\omega k b_z-qn+{\omega^2\over2}\operatorname{tr}h.
\]

The full solution gives, writing S=tr(S_ij),

\[
\boxed{R_{00}^{(1)}={\rho+S\over4}
{q+3\alpha\omega^2\over q(1-\alpha)}.}
\]

In these normalized source units GR gives (rho+S)/4. Restoring the suppressed
source normalization makes that 4 pi G(rho_phys+S_phys). The script derives
the GR cancellation exactly. Tensor wave poles and transverse vector sources
cancel from this contraction, rather than being deleted from the metric.
On a curved background the leading tangent curvature is the leading part of
the local observable R_mu nu u^mu u^nu; observer/background corrections are
lower derivative order.

## 3. Why this is the full spacetime principal block

The code expands the full auxiliary density, including lapse/metric mixing.
With a_bar=a0 y zhat, N=N_bar(1+n), h=I+H and d=grad n,

\[
z_1={2\bar a\cdot d-\bar a^TH\bar a\over a_0^2},\qquad
z_2={d^2-2n\bar a\cdot d-2\bar a^THd+\bar a^TH^2\bar a\over a_0^2},
\]
\[
v_1=n+\tfrac12\operatorname{tr}H,\quad
v_2=\tfrac n2\operatorname{tr}H+\tfrac18(\operatorname{tr}H)^2
-\tfrac14\operatorname{tr}(H^2),
\]
\[
L_{{\rm aux},2}=2a_0^2[Fv_2+F_z(z_2+v_1z_1)+\tfrac12F_{zz}z_1^2].
\]

Substituting d -> s d computes derivative degrees: lapse-lapse degree 2,
mixed metric/lapse degree 1, metric-metric degree 0. Thus the complete
order-two addition is 2 d^T M d, where

\[
M=e^{-y}(I-y\hat a\hat a^T),\quad
\alpha(\hat k)={k^TMk\over q},\quad
D=q-k^TMk=\mu_t k_\perp^2+\mu_l k_\parallel^2,
\]
\[
\mu_t=1-e^{-y},\qquad \mu_l=1+(y-1)e^{-y}>0\quad(y>0).
\]

The EH time derivatives are retained at the same order. Canonical momenta
and the trace multiplier scale as one derivative. Volume averaging is a
global zero-mode operation; on a compact smooth leaf its finite-rank
subtraction does not alter the local high-frequency principal symbol.

## 4. Locality theorem for this principal system

Take any smooth compactly supported scalar generator f(t) sigma(x) and the
identically conserved test stress

\[
T^{00}=f\Delta\sigma,\qquad T^{0i}=-f'\partial_i\sigma,
\qquad T^{ij}=f''\sigma\delta^{ij}.
\]

It is a pure scalar source; its tensor and transverse-vector projections
vanish. The all-metric solution, not a scalar-only assumption, yields

\[
\boxed{\frac{\delta R_{00}}{\widehat{f\sigma}}
=-{(q+3\omega^2)^2\over4}\left({1\over D}-{1\over q}\right).}
\]

Here delta denotes the difference from GR for the same source. The response
is polynomial in omega. Its omega^4 coefficient is

\[
C_4(k)=-{9\over4}\left({1\over D}-{1\over q}\right)
=-{9k^TMk\over4qD}.
\]

**Proof of the necessary locality condition.** A frequency polynomial is a
finite sum of time-delta derivatives with spatial-distribution coefficients.
If its kernel is supported in any finite-speed future cone, its support on
t=0 must lie at x=0. Each spatial coefficient must therefore be supported at
x=0. A distribution supported at a point is a finite sum of derivatives of
the point delta: use its finite distributional order and subtract the test
function's Taylor polynomial at that point. Its Fourier transform is a
polynomial. But C4 is homogeneous of spatial degree -2. A nonzero polynomial
cannot have that degree. Consequently C4 must vanish identically, requiring
M=0. This argument also excludes a cancellation between different time-delta
derivatives, which are linearly independent.

The script solves the numerator-coefficient equations, obtaining

\[
\boxed{\text{finite-speed conserved-source response}
\ \Longrightarrow\ \mu_t=\mu_l=1.}
\]

For the exponential law even a transverse wavevector suffices:

\[
\boxed{C_4(k_x,0,0)=-{9\over4k_x^2(e^y-1)}\ne0
\quad\text{for every finite }y>0,\ k_x\ne0.}
\]

Thus this principal model is **DEAD as a causal conserved-source response
model**. It is not a numerical search failure. The result is uniform in
finite positive y and is not based on an expected determinant or rank.
At y=0 the elliptic inverse is singular and this proof does not apply; that
does not repair its failure at positive y. The GR y->infinity limit passes.

### Exact scope of the nonlinear corollary

Suppose this Hamiltonian admits a smooth nonzero-field solution and a
retarded linear response to the above source domain, such that rescaling
both space and time about that point converges distributionally to the
complete principal response just calculated. If the original response has
finite propagation speed, every rescaled kernel is supported in a cone
converging to the local finite-speed cone. Testing against any smooth
function outside that cone gives zero at every scale, hence zero in the
limit. The computed principal kernel contradicts that consequence.

**Therefore lower-derivative terms cannot repair causality while preserving
this regular tangent limit and source domain.** To escape, at least one of
those premises must fail or the leading kinetic/constraint structure must
change. The calculation does not silently assume that principal-symbol
inversion proves convergence of the full Green operator: regular convergence
is an explicit hypothesis, not a result of this script.

## 5. Healthy matter is a substantive issue, not a positivity slogan

An arbitrary signed conserved test stress is not automatically a complete
physical matter experiment. We also compute a useful independent check with
three ordinary canonical Klein-Gordon fields,

\[
V=\tfrac12(\phi_1^2+4\phi_2^2+9\phi_3^2),\quad
\bar\phi(0)=(1,\tfrac12,\tfrac13),\quad
\dot{\bar\phi}(0)=(1,1,1),
\]
\[
\delta\phi(0)=0,\qquad
\delta\dot\phi(0,x)=(1,-2,1)\sigma(x).
\]

The kinetic terms and masses are positive. The two initial velocity choices
v +/- epsilon u sigma have exactly the same positive energy
3+3 epsilon^2 sigma^2 and the same initial stress. Solving KG in a time-series
on flat space gives the linearized stress jets

\[
\delta\rho=-\tfrac13t^4\Delta\sigma+O(t^5),\qquad
\delta J_i=\tfrac43t^3\partial_i\sigma+O(t^4),
\]
\[
\delta T_{ij}=(-4t^2+16t^3)\sigma\delta_{ij}+O(t^4),
\quad \delta\ddot S(0)=-24\sigma.
\]

The script derives these coefficients and checks conservation through the
computed orders. Their leading terms match the formal generator f=-t^4/3.
This removes the elementary objection that a signed perturbation requires
negative-energy matter. It does **not** supply a solved coupled gravity/KG
background at nonzero acceleration, or show that arbitrary compact
time-switched stresses are generated by that matter model.

## 6. Dependency audit and interpretation

| Obligation | Verdict |
|---|---|
| Full principal canonical action and minimal source coupling | Passed algebraically; independently reviewed |
| All 20 metric/gauge equations | Exact residuals zero |
| All-metric principal Dirac preservation | Closed, computed two gravitational pairs |
| GR control and tensor/vector inclusion | Passed |
| Exponential kernel's nonlocal curvature coefficient | Exact nonzero expression |
| Principal finite-speed locality theorem | Proved for the stated conserved-source domain |
| Lower-order rescue with a regular tangent limit | Excluded by support-limit argument |
| Existence of required solved nonlinear background and regular inverse limit | Not established |
| Complete physical realization of source experiment on that background | Not established; healthy local jets checked |
| Full nonlinear PPN/cosmology/stability and novelty | Not established |

The falsified combination is this **specified Hamiltonian**, nontrivial
metric MOND, and a regular finite-speed response to admissible conserved test
stresses. It is not a universal prohibition of MOND, a proof that every
two-tensor theory fails, or evidence that galaxy measurements are wrong.
The broader field-theory objective remains **OPEN**. The nonlinear candidate
has a **conditional no-go**, not an unconditional completed falsification.

A kernel-only retuning within this principal structure is not a cure:
locality forces the transverse MOND coefficient to one. A future candidate
must change the leading kinetic/constraint structure, or explicitly resolve
the background/source-domain assumptions; importing PPN or MOND results from
another action does neither.

## 7. Prior art and source scope

The local trace-momentum mechanism is related to kinetic-conformal Hořava
gravity, not a certified new architecture. Bellorin and Restuccia,
*Quantization of the Hořava theory at the kinetic-conformal point*,
[arXiv:1606.02606v2, 5 October 2016](https://arxiv.org/html/1606.02606v2),
equations (2.13)-(2.22), display the trace constraint and general-potential
canonical Hamiltonian. On the local trace constraint surface the difference
between our GR trace kinetic term and their trace-free kinetic term vanishes.
Their theory does not authenticate our global mean subtraction, MOND
potential, or sourced causal no-go. The source was checked for architectural
attribution only; its vacuum tensor analysis is not a matter-response proof.
Search scope: this named kinetic-conformal connection, not global novelty.
The locality proof above is supplied directly; no unverified Peetre citation
is used as a proof dependency.

## 8. Reproduction

New files only: `metric_causal_symbol.py`, `test_metric_causal_symbol.py`,
`metric_causal_symbol_results.json`, `METRIC_CAUSAL_SYMBOL.md`,
`metric_causal_symbol_manifest.json`. Existing files were not changed.

From repository root:

```bash
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol.py --require-causal-conserved-source-response
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol_manifest.json
git diff --check
```

The ordinary calculation exits 0 on its ten algebraic checks; the strict
causal-response gate exits 2. The manifest records test results, hashes,
arithmetic conventions, the independent review, and the initial implementation
bug: SymPy left some residuals as `0*I` after factorization. Exact cancellation
reduced them to zero; no physical criterion was weakened. No commit/push.
The combined directory regression run passed all 47 tests (exit 0), including
the earlier closure probes; this is not a run of every script in the repo.
HEAD moved from 9ff805406 to 5e31f0166 during this work. The intervening g03m/n
commits concern a different candidate's dark-sector capture estimates; they
do not change the Hamiltonian or input code used here.
