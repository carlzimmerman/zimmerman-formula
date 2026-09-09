# Local winding-clock checkpoint — 2026-09-09

## Verdict

**OPEN, not closed.** The first action-derived checkpoint is reproducible and
passes every gate implemented here, but it does not yet certify the full
relativistic theory. In particular, the full functional ADM algebra, PPN
parameters, nonlinear perturbation stability, causal propagation, and an
empirical galaxy/cluster likelihood remain open.

## Candidate action

The audited reduced action is the IC1 exponential sector together with

\[
 S_{Q\lambda}=\int\!\sqrt{-g}\,\lambda
       (n^\mu\nabla_\mu Q-\Theta),\qquad
 S_c=\int\!\sqrt{-g}\,e^{-\beta Q}
       \left[-\frac12 g^{\mu\nu}\nabla_\mu\chi_c\nabla_\nu\chi_c
             -\frac12m_c^2\chi_c^2\right],
\]

with baryons minimally coupled to the same metric. The primary winding rate
is signed, \(\mathcal W(\Theta)=\Theta\). The smooth absolute-value rate is
reported only as a negative control.

## Derived results

1. **Exact constitutive law.** SymPy differentiates

   \[
   G(y)=y^2+2(1+y)e^{-y}-2
   \]

   and obtains \(G'(y)/(2y)=1-e^{-y}\) exactly. Independent variation of
   the static lapse and conformal potentials gives

   \[
   \Psi''-\Phi''=0,
   \qquad
   2m\,\partial_x[(1-e^{-\Phi'/a_0})\Phi']=\rho_b
   \]

   on the baryon-only branch. Thus \(\Phi\) and \(\Psi\) were varied
   separately; \(\Phi=\Psi\) is the regular-boundary solution of the second
   equation, not an input. The high-acceleration coupling is
   \(G_{\rm measured}=1/(8\pi m)\).

2. **Actual reduced Dirac chain.** In both sectors \(k\ne0\) and \(k=0\),
   the generated primary constraints are
   \(p_N\simeq0\), \(p_\lambda\simeq0\), and
   \(C_Q=p_Q-a^3\lambda\simeq0\). Their three computed secondary
   constraints are preserved by solving the actual multiplier matrix. The
   full six-by-six Poisson matrix is antisymmetric and has computed generic
   rank 6, with 0 first-class and 6 second-class constraints in this finite
   homogeneous block; the resulting phase-space dimension is 4. No rank or
   determinant was inserted by hand. The absolute-winding control spends a
   velocity-Hessian direction and is kept separate.

3. **Ward identities.** The minimally coupled baryon representative obeys
   the exact variational identity
   \(\nabla_\mu T_b^{\mu\nu}-E_b\nabla^\nu\psi_b=0\), and its divergence
   vanishes after the baryon equation of motion. The cold scalar is not
   separately conserved when \(\beta\ne0\): its computed on-shell exchange is

   \[
   \mathcal E_c=\frac{\beta}{2}e^{-\beta Q}
       (\dot\chi_c^2-m_c^2\chi_c^2)\dot Q,
   \]

   which is explicitly balanced by the \(Q\)-equation source. This preserves
   ordinary baryon conservation without falsely declaring the cold sector
   separately conserved.

4. **Expanding FLRW branch.** Variation is performed before setting the
   lapse to one. An explicit family with \(\Lambda>0\) is

   \[
   N=1,\quad a=a_{\rm ref}e^{Q_0+Ht},\quad
   Q=Q_0+Ht,\quad \lambda=\lambda_0e^{-3Ht},\quad \chi_c=0,
   \quad H=\sqrt{\Lambda/3}\ne0.
   \]

   Every displayed lapse, scale-factor, memory, multiplier, and cold-scalar
   Euler residual reduces to zero. The cold kinetic coefficient is
   \(e^{-\beta Q}/2>0\) on the stated branch. This is an existence result,
   not a perturbative stability proof.

5. **Assembly-history diagnostic.** Using the independently rerun L75 values,
   \(Q_{\rm rec}=0\), \(Q_{\rm gal}=\ln3\), and
   \(Q_{\rm cl}=\ln1.7\). For \(\eta=e^{-\beta Q}\), the galaxy ceiling
   \(\eta_{\rm gal}\le0.248\) implies
   \(\beta\ge-\ln(0.248)/\ln3\); the computed ordering is
   \(\eta_{\rm rec}>\eta_{\rm cl}>\eta_{\rm gal}\) at the boundary. This
   is a bounded calibration diagnostic, not a derivation of the coupling or
   halo formation history.

6. **Principal-symbol stress test.** The quadratic fixed-FLRW patch derives
   the memory equations \(\dot{\delta\lambda}=0\) and
   \(\dot{\delta Q}-\delta\Theta=0\). With the metric perturbation held fixed,
   the actual Fourier matrix has determinant
   \(D_{Q\lambda}(\omega,k)=-\omega^2\), independent of \(k\), and the
   velocity Hessian has computed rank zero. The cold scalar, by contrast, has
   \(D_c=f_Q(k^2-\omega^2)\) and kinetic coefficient \(f_Q/2>0\). This is an
   action-derived zero-gradient/strong-coupling risk for the clock memory,
   not a healthy propagating scalar and not a pass of the stability gate.

7. **Scoped architectural no-go.** For the exact local term
   \(A\lambda(\dot Q-\delta\Theta)\), the action-derived momenta are
   \(p_Q=A\lambda\) and \(p_\lambda=0\), with computed bracket
   \(\{p_\lambda,p_Q-A\lambda\}=A\ne0\). The velocity Hessian has rank zero,
   while the Fourier determinant is \(-A^2\omega^2\) for every \(k\). Adding
   a standard \(Q\) kinetic/gradient regulator raises the computed Hessian rank
   from 0 to 1 but leaves the \(\lambda\)-equation exactly unchanged. Therefore
   the strict architecture cannot become a healthy hyperbolic clock without
   changing the multiplier constraint or the field content. This is a scoped
   no-go for this local realization, not a universal theorem about all
   nonlocal/elliptic MOND actions.

## Exact files created

- `action_variation.py`, `test_action_variation.py`
- `dirac_gate.py`, `test_dirac_gate.py`
- `weak_field_ward_gate.py`, `test_weak_field_ward_gate.py`
- `flrw_winding_gate.py`, `test_flrw_winding_gate.py`
- `winding_calibration.py`
- `stability_causality_gate.py`, `test_stability_causality_gate.py`
- `winding_no_go.py`, `test_winding_no_go.py`
- `run_local_winding.py`, `test_local_winding.py`
- `lean_ready_identities.json`, `lean_ready_identities.lean`
- `contract.json`
- `run_001/local_winding_results.json`, `run_001/manifest.json`
- this `REPORT.md`

Only these package files are intended for the scoped commit; the repository
contains unrelated dirty and untracked work from earlier research runs.

## Commands and exit statuses

| command | exit |
|---|---:|
| `python3 -B -m unittest -v test_action_variation.py` (package directory) | 0 |
| `python3 -B -m unittest -v test_dirac_gate.py` (package directory) | 0 |
| `python3 -B -m unittest -v test_weak_field_ward_gate.py` (package directory) | 0 |
| `python3 -B -m unittest -v test_flrw_winding_gate.py` (package directory) | 0 |
| `python3 -B -m unittest -v test_local_winding.py` (package directory) | 0 |
| `python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/local_winding_clock_2026 -p 'test_*.py' -v` | 0 (15 tests) |
| `python3 -B run_local_winding.py --output-dir run_001` | 0; report status OPEN |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/local_winding_clock_2026/run_001/manifest.json` | 0; valid legacy manifest |
| `python3 -B -m unittest -v test_integrable_clock.py` (IC1 directory) | 0 (9 tests) |
| `python3 -B -m unittest -v test_localized_v4.py` (localized V4 directory) | 0 (13 tests) |
| `python3 -B -m unittest -v test_dw_localized_repairs_2026.py` (fried_chicken directory) | 0 (7 tests) |
| `python3 -B fable_independent_2026/L75_clock_winding_transmission.py` | 0; 10/10 checks |

## Requirement status

| requirement | checkpoint status |
|---|---|
| exact \(\mu=1-e^{-y}\), Newtonian/high-acceleration branch | derived in static gate |
| separate \(\Phi,\Psi\) variation | derived; regular slip branch shown |
| ordinary baryon Ward identity | exact representative identity |
| expanding \(H\ne0\) FLRW family | derived existence branch |
| reduced memory constraints, both k sectors | computed closure |
| full gravitational \(N_{\rm grav}=2\) | OPEN: finite block is not full ADM |
| \(\gamma_{\rm PPN},\beta,\alpha_1,\alpha_2,\alpha_3\) | OPEN |
| \(c_T=c\), no ghost/gradient/strong coupling | OPEN; clock block has zero-gradient risk |
| full nonlinear metric Ward identity | OPEN |
| empirical galaxy/cluster fit | OPEN |
| Lean-checked proof | OPEN; Lean unavailable |

## Strongest result and next unavoidable calculation

The strongest constructive result is that the signed local winding multiplier
can be action-varied, has an explicitly computed closed reduced constraint
chain, preserves baryon conservation, retains the exact exponential MOND
static branch, and supports \(H\ne0\) FLRW. This is a real opening, not a
complete theory: the finite rank-6 result cannot be promoted to
\(N_{\rm grav}=2\), and the independently computed \(D_{Q\lambda}=-\omega^2\)
principal symbol flags a zero-gradient/strong-coupling obstruction unless the
full IC1 metric sector supplies a demonstrably healthy gradient without adding
an unwanted scalar mode.

The next unavoidable calculation is the **full covariant ADM/Dirac analysis of
the combined IC1 metric-clock action plus the \((Q,\lambda,\chi_c)\) sector,
followed immediately by the nonzero- k scalar/vector/tensor quadratic action**.
That calculation must determine whether the local winding clock leaves only
the two tensor gravitational modes and whether its scalar exchange is healthy;
only after that can a boosted PPN solve and empirical cluster gate be
meaningful.

The no-go makes the design fork explicit: either accept a pressureless,
zero-gradient clock with a strong-coupling risk, or replace the exact
multiplier transport law by a covariant higher-derivative/elliptic sector and
recompute all constraints, PPN coefficients, and wave characteristics from
that new action. There is no honest way to declare both branches equivalent.
