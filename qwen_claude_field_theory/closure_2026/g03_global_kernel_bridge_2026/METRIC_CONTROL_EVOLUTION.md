# Fixed-profile failure and the route beyond boundary-jet tuning

2026-09-06. Same CMC Hamiltonian, exact exponential kernel, no new fit.
Base and remote main: `6978397a4bc47f0e1bf1ded52103371a3419fff4`.

**Status: OPEN.** Neither a complete gravity theory nor an unconditional
no-go is claimed. Two previously constructed numerical source profiles fail
the next wall-collar preservation test. More importantly, the calculation
can be organized as a formal leading-amplitude recursion at every time order;
another finite source fit is not the missing evolution theorem.

## 1. Fixed theory and conventions

Use exactly the Hamiltonian and boundary completion in `METRIC_SHARED_DATA.md`:

\[
H=\int[N\mathcal H_{GR}+N^i\mathcal H_i
-2N\sqrt h\,a_0^2F(a^2/a_0^2)
+\lambda(\pi-\sqrt h\bar\pi)]d^3x+H_m,
\]
\[
F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}],\quad
a_i=D_i\log N,\quad\bar\pi=\int\pi/\int\sqrt h.
\]

The static plane background is
\(ds^2=-N(z)^2dt^2+dz^2+A(z)^2(dx^2+dy^2)\).
The action is varied with radial metric factor B *before* setting background
B=1. Induced N,A are fixed at the slab walls; subsequent normal B jets are
not fixed. Write \(u=N'/N,b=A'/A,\chi=(1-u/a_0)e^{-u/a_0}\).
The homogeneous trace mode is solved, never discarded.

Matter is the same three canonical minimally coupled KG fields, with
\(m_i=(1,2,3),r_i=(1,1/2,1/3),v_i=(1,1,1),U_i=(1,-2,1)\), initially
\(\phi_i=\epsilon r_i,\Pi_{i,\pm}=\epsilon(v_i\pm U_i\sigma)\).
Each state's energy is \(3\epsilon^2(1+\sigma^2)>0\) for nonzero epsilon;
a signed difference profile is not negative-energy matter.

All gravitational jets below mean half the difference, divided by
epsilon squared, at epsilon=0. Matter perturbations used for the wall test
are leading order epsilon cubed. Superscripts (n) are time derivatives,
not Taylor coefficients. No uniform control at finite epsilon is inferred.

## 2. The next exact equation

Direct KG stress differentiation on the curved background gives

\[
\rho_2=\rho_3=0,\qquad S_2=-24N^2\sigma,\qquad S_3=288N^3\sigma.
\]

In particular, the third Taylor coefficient of S is \(48N^3\sigma\), not
\(288N^3\sigma\).
Let \(\mathcal J_\ell,\mathcal J_\tau\) be the two linearized spatial
Euler–Lagrange operators computed in `metric_initial_response.py`. Their
full lower-derivative coefficients are retained. For n=2,3 the metric
response is conformal, \(a_n=b_n=w_n\), with fractional lapse jet v_n:

\[
\mathcal J_\ell[w_n,v_n]=0,\qquad
\mathcal J_\tau[w_n,v_n]=-S_n+2d_n/N,
\quad d_n=\delta\bar\pi^{(n+1)}.
\]

Thus, for the same homogeneous boundary and mean conditions, the exact
linear operator identity is

\[
\boxed{\mathcal R_3[\sigma]=-12\mathcal R_2[N\sigma],\qquad
\mathcal M_3[\sigma]=-12\mathcal M_2[N\sigma].}
\]

Here R includes w,v,d and M extracts \((d,w'_L,v'_L,w'_R,v'_R)\).
Cancellation of \(\mathcal M_2[\sigma]\) alone does not imply cancellation
of \(\mathcal M_2[N\sigma]\) on a nonconstant-lapse background. This
identity is derived from the stress equations and linearity, not a fitted
exponent or a claim of historical novelty.

If the earlier w2,v2 vanish **exactly on open wall collars**, the necessary
sixth KG wall jet, normalized by \(2\epsilon^3N^3v_i\), is

\[
Q_6=v_3''-3w_3''-(3b+2u)w_3'
 +(5b+7u+3u\chi)v_3'+d_3/(2N).
\]

The code derives it by the KG product rule and the Hamiltonian normal jet
\(B_5=-Nd_3/2-3N^2[(b+u)w_3'+(b+u\chi)v_3']\).
Omitting B5 produces a nonzero symbolic error. Exact open-collar cancellation
is stronger than the finite numerical cancellation previously obtained.

## 3. Fixed profiles fail the next finite control

The previous ten-bump controls are regenerated, then used without refitting.
Actual forcing probes record what entered the new integrator. Independent
RK45 and DOP853 integrations solve for the global d3 and both shooting slopes.

| Background (y0, Lambda/a0 squared, L) | Third control / refinement error | Q6 left | Q6 right |
|---|---:|---:|---:|
| (0.5, 0, 0.02) | 8,247 | −4.35327e−5 | −4.73526e−5 |
| (10.5, 32 pi, 0.002) | 320,262 | −2.23465e−5 | +2.03754e−5 |

The third controls' scaled norms are 1.706e−4 and 2.245e−3. Their
refinement errors are 2.069e−8 and 7.009e−9. Both fixed-profile next-collar
gates FAIL. Boundary residuals are below 6e−21; finite-difference ODE
residuals are below 9e−7. All numerical ranks are computed from the actual
matrices and reported; none is an exact rank certificate.

The displayed Q6 values are conditional diagnostics: refinement measures
this solve, **not** uncertainty in an exact lift of the preceding numerical
control, nor all omitted spatial derivatives of earlier jets. The fixed
numerical profiles' nonzero third controls are the direct bounded result.
The proportional-column check is a solver-linearity sanity check, not an
independent derivation of the operator. No universal invariant-subspace
no-go follows from these two profiles.

## 4. A formal recursion, including the terms needed from order four

This supplies a reusable leading-amplitude organization, not a nonlinear
Dirac closure or a convergent time evolution. The plane canonical momenta
are \(P_A=4A\pi^{xx},P_B=2B\pi^{zz}\), giving

\[
H_{kin}=N[-P_AP_B/(4A)+BP_B^2/(8A^2)].
\]

For n at least one, let a_n,b_n,v_n be fractional metric jets and set

\[
k^A_n=-NP_{B,n-1}/(4A^2),\quad
k^B_n=N[-P_{A,n-1}/(4A)+P_{B,n-1}/(4A^2)],
\quad a_n=k^A_n+w_n,\ b_n=k^B_n+w_n.
\]

Here \(w_n=\ell_{eff}^{(n-1)}/2\) and the mean of ell_eff vanishes.
For general independent a,b,v let delta E denote the spatial linearization
of the *same* action, not just its conformal restriction. Solve

\[
\mathcal J_\ell[w_n,v_n]=\rho_n-\delta E_\ell[k^A_n,k^B_n,0],
\]
\[
\mathcal J_\tau[w_n,v_n]=-S_n+2d_n/N
-\delta E_\tau[k^A_n,k^B_n,0],
\]
\[
w_n|_{walls}=-k^A_n|_{walls},\quad v_n|_{walls}=0,
\quad\int A^2w_n\,dz=0.
\]

Then update

\[
P_{A,n+1}=\delta EL_A[a_n,b_n,v_n]+2NAp_{\perp,n},
\quad
P_{B,n+1}=\delta EL_B[a_n,b_n,v_n]+NA^2p_{z,n}.
\]

The code derives the general 2-by-9 spatial coefficient matrix, verifies
all twelve coefficients of its conformal restriction, and derives both
pressure-force factors from the canonical KG Hamiltonian. At n=4 the
known momentum terms generally do not vanish: imposing a=b or zero w at
the walls would change the calculation.

Trace consistency gives
\(2k^A_n+k^B_n=-N\delta\bar\pi^{(n-1)}/2\).
Kinetic, volume-weight, and multiplier–momentum products enter at epsilon
to the fourth power about this static vacuum, not at the retained order.

The plane momentum constraint is
\(\mathcal H_z=A'P_A-BP_B'+\sum p_\phi\phi'\).
At the retained order its preservation follows from the computed spatial
Noether identity and the independently differentiated canonical KG identity

\[
\dot J=N'A^2\rho-2NAA'p_\perp+(NA^2p_z)',
\qquad J=\sum p_\phi\phi'.
\]

Indeed, the gravitational contribution is −N' delta EL_N, which cancels
the remaining matter term using delta EL_N=A squared rho.

**Formal scope.** Fix a regular background whose augmented spatial
boundary operator is invertible, as proved for sufficiently small slabs
in `METRIC_SHARED_DATA.md`. At each finite time order, previously computed
momenta and smooth KG jets are known sources. The same invertible spatial
operator supplies the next w,v,d, including the inhomogeneous w boundary
values. Induction constructs a unique formal leading-amplitude jet sequence
for this plane branch with the chosen global normalization. KG-wall jets
are allowed to follow the equations. This does not prescribe independent
fixed KG wall histories. No convergence, uniform derivative estimates,
full nonlinear evolution, or general-sector constraint classification is
proved by this induction.

The epsilon-cubed KG backreaction requires the additional forced KG
recursion, using both common and difference metric responses. That system
is triangular once those metric jets are supplied. The formal result here
does not claim that this next amplitude order has been implemented at every
time order; the explicit fifth/sixth wall calculations only sample it.

## 5. The causal question does not require identical distant matter walls

The physically relevant conditional statement can be sharpened without
another source fit. Use the original compact positive bump and its exact
small-slab exterior-response argument from `METRIC_SHARED_DATA.md`.
Choose an interior observer separated from that bump and from both walls.

Assume the two exact common nonlinear initial-data families admit compatible
smooth coupled evolutions, sufficiently C2 in epsilon for the indicated
mixed derivatives. Allow their KG-wall histories to differ; keep the same
induced metric-wall histories. Assume local geometric uniqueness with a
finite domain of dependence.

The common first-preservation solve supplies equal physical extrinsic
curvature and lapse velocity, not merely equal canonical pi. In particular,
\(\dot h_{ij}=2w_{common}h_{ij}\) and
\(K_{ij}=w_{common}h_{ij}/N\). The initial data agree near the observer.
An independent connection calculation now gives the spacetime-scalar result

\[
\boxed{\frac{{}^{(4)}R_+-{}^{(4)}R_-}{2}
=\frac{6\epsilon^2w_2}{N_0^2}+o(\epsilon^2).}
\]

The corresponding normal Ricci projection is −3 epsilon squared w2/N0
squared. This is a difference in the **initial curvature value**, not a
later derivative of curvature. The prior small-slab argument supplies a
nonzero exterior w2. Local geometric uniqueness would instead equate the
scalars in the common domain before either remote boundary or the changed
matter can affect the observer. These assumptions are therefore incompatible.

This is still conditional: formal wall jets, or smooth wall functions with
those jets, do not establish actual coupled solutions. The open obligation
is a local existence/admissibility analysis for the mixed elliptic–evolution
system. A universal claim about all MOND theories does not follow.

## 6. Latest Claude work and next unavoidable calculation

The verified latest commit, `6978397a4`, adds g03r for THE_ACTION's different
dynamical scalar/khronon model. It changes no files implementing this CMC
Hamiltonian. Its hydrostatic surrogate is numerically stable in a reported
refinement, but the cluster-profile slope check fails; the stiff-fluid
evolution remains unconverged. Its gates cannot be imported into this theory.

**Next:** establish or refute local well-posedness/admissibility of the same
CMC–KG mixed system with compatible, not necessarily identical, matter-wall
histories. The formal recursion identifies the required equations and the
first anisotropic terms. Uniform estimates or an actual converged coupled
evolution are needed; another finite stacked source control would not fill
this gap. If regular solutions exist for the shared local data, the scalar
curvature calculation already obstructs finite-speed local evolution.

Neither PPN, full nonlinear DOF counting, stability, expanding cosmology,
nor the y=0 and global homogeneous sectors is newly certified here. The
global trace jet was retained; that is not a full k=0 sector classification.

## 7. Reproduction and file inventory

Only five new files belong to this continuation: this report,
`metric_control_evolution.py`, `test_metric_control_evolution.py`,
`metric_control_evolution_results.json`, and
`metric_control_evolution_manifest.json`. Earlier work is preserved.
No commit or push was made.

Run from the repository root:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_control_evolution.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_control_evolution.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_control_evolution_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_control_evolution.py --require-preserved-collar
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
```

Final verification: new tests **8/8, exit 0**; full local closure suite
**88/88, exit 0** (53.391 seconds); producer **exit 0**; strict preservation
requirement **exit 2**. The separate read-only g03r H1/X1 rerun **exited 1**
because X1 failed. Its exact command is preserved in the manifest. Remote
inspection first failed with sandbox DNS exit 128; the authorized read-only
retry exited 0 and matched the base commit. `git diff --check` exited 0.

Verification results and hashes are recorded in the manifest. Ordinary
producer exit 0 means the *audit* completed consistently. The strict
requirement exits 2 for a failed or unresolved collar gate; neither means
the theory passes. Test-first runs also exited 1 while new implementations
and evidence fields were absent, then were rerun after implementation.
