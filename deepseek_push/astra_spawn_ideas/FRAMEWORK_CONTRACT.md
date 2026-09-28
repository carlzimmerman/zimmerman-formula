# Framework contract for AS001–AS2000

These are proposed work orders for DeepSeek, not completed calculations. The objective is constructive closure of Zimmerman's gravity framework under the repository's amended thirteen requirements. A falsified construction or proved conditional lemma is useful progress; neither is automatically a completed theory. The 2000 tasks are a dependency-aware portfolio, not 2000 claims that must all become true. Historical reproductions are explicitly diagnostic, not claims of new discoveries.

## Source authority and frozen base

Read `STANDING.md`, then the amendment block in `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`, then the task's specific sources. The September 26 amendment overrides historical wording below it: the operative target is **filtered nu_mono**, and causality is **criterion B**, not a strict metric-cone condition. Older `deepseek_push/THE_THEORY.md`, README and status files contain useful equations and stronger historical claims; they are not independent certificates that supersede the reviewed record.

The catalog began from Git revision `eccd1c0e59459b5ec1acf2e916fb7a05a7f67971` with substantial pre-existing uncommitted and concurrent work. `SOURCE_MANIFEST.json` pins actual source bytes at assembly, not merely HEAD. Before execution, compare current source hashes. Reconcile any changed source with the orchestrator and record an explicit new base rather than mixing revisions. Consult current standing for later supersession; the timestamp of a file alone does not prove that it supersedes another result.

## Mandatory scale and units

Use, as a declared framework input unless a task actually derives it,

```text
a0 = kappa c sqrt(G rho_Lambda),   kappa = 1/2 adopted
rho_Lambda = 4 a0^2/(G c^2)          [mass density, kg/m^3]
epsilon_Lambda = rho_Lambda c^2     [energy density, J/m^3]
Lambda = 32 pi a0^2/c^4             [m^-2, when the Einstein and scale G coincide]
r_M = sqrt(G M_b/a0)
C = sqrt(G M_b a0),   v_flat^4 = G M_b a0
```

`G=6.67430e-11 m^3 kg^-1 s^-2`, `c=299792458 m/s`, `M_sun=1.98847e30 kg`, `pc=3.085677581491367e16 m`, and `k_B=1.380649e-23 J/K` are the default numerical conventions for new calculations. Historical reproduction may use a source's constants, but record them and quantify the resulting difference. `G_N`, `G_bare` and `G_cosmo` are separate symbols until their relation is derived. In an action whose vacuum curvature uses `G_E` but the acceleration relation uses `G_N`, `Lambda_eff=8 pi G_E rho_Lambda/c^2=32 pi (G_E/G_N) a0^2/c^4`. Carry that ratio, and the analogous critical-density ratio, before quoting the familiar same-G vacuum or horizon identities. Enforcing the framework identity is a matching condition on the candidate, not permission to set distinct couplings equal.

Report dimensional examples separately for **canonical** `a0=9.3619e-11 m/s^2` and **alternative** `a0=1.1279e-10 m/s^2`. The latter is an alternative normalization, not simultaneously the same fixed rho_Lambda and fixed kappa. If rho_Lambda is held fixed, compute its effective kappa; if kappa is held fixed, identify the changed density. A dimensionless theorem can be proved once, but its applicability to both footings must be stated. Do not fit a0 per object unless a task explicitly defines an inference diagnostic; such a fit does not count as a parameter-free prediction.

The equilibrium relations `sigma^2=C/2`, `rho_ph=C/(4 pi G r^2)` and `P=sigma^2 rho_ph` are **conditional deep-equilibrium inputs/targets**. Finite boundaries, source coupling, normalization, equilibrium formation and the possible double counting of the logarithmic well need their own derivations. Do not use these relations as if they solved the time-dependent relativistic equations.

## Branch dictionary: never silently identify these laws

Let `B=g_bar=g_N>0`, `y=B/a0`, `g` be total radial acceleration and `x=g/a0`.

| Label | Equation and scope |
|---|---|
| Q | Algebraic a0-line: `g^2=B^2+a0 B`. A radial relation; not by itself a nonspherical field equation. |
| RAR | `nu_RAR(y)=1/(1-exp(-sqrt(y)))`; in spherical unfiltered use `g=B nu_RAR(y)`. |
| MU2 | Implicit response `mu2(x)=1-(1+x/2)^(-2)`, `mu2(x)g=B`; equivalently `mu_n(Y)=1-(1+Y)^(-n)` at `n=2`, `Y=g/s=x/2`, `s=2a0` on the adopted footing. |
| EXP | Historical exact AQUAL: `mu_EXP(x)=1-exp(-x)`, `div[mu_EXP(|grad Phi|/a0) grad Phi]=4pi G rho_b`. This is a comparison branch, retired as the operative target. |
| MONO | Operative monotone-phantom continuation of RAR, described below, through the specified heat filter. |

For MONO, define `h_RAR(y)=y(nu_RAR(y)-1)`, peak `y_p` and `h_p=h_RAR(y_p)`, and `delta=0.05`. Its derivative is `h'_mono=max(h'_RAR,delta h_p/(y+y_p))`, joined continuously from the RAR segment. Solve for the actual crossing; `y_star≈2.3374` and `y_p≈2.5396` are rounded landmarks. On the continuation,

```text
h_mono(y)=h_RAR(y_star)+delta h_p log[(y+y_p)/(y_star+y_p)]
nu_mono(y)=1+h_mono(y)/y.
Delta u=4 pi G rho_b
Delta Phi=4 pi G rho_b + S* div[(nu_mono(|grad S u|/a0)-1) grad S u]
S=exp[(xi^2/2) Delta].
```

Specify the metric, measure, domain and boundary conditions that define `S` and its adjoint `S*`; self-adjointness in one measure does not imply it in another. Vary the metric/lapse dependence of S when varying an action. Smoothing, changing a source gate or changing the branch creates a different mathematical model unless equivalence is derived. The quoted small force difference between MONO and RAR cannot transfer derivative, stability or regularity results.

## Same-theory discipline

For every candidate, pin the **action/Hamiltonian revision, matter coupling, kernel, filter, gate, vacuum convention, initial/boundary data and parameter values**. A shared parameter cell means all these coincide across tests. CA4 and CA5-GNC-R are candidate constructions with scoped results. Gated or occupied branches can change the exact global static target; derive that change before using a baryon-only force formula. Observational success with prescribed carrier dynamics does not derive those dynamics from the action.

Exactly two **gravitational** propagating degrees of freedom are required; allowed matter/clock fields must be counted and shown healthy separately. Derive both metric potentials, ordinary-matter conservation, measured Newton coupling, PPN and tensor dynamics. Criterion B permits leafwise instantaneous channels and speeds exceeding the metric speed if a consistent global preferred time exists, no backward-time signals or closed causal curves occur, and the mixed Cauchy problem is well posed. Homogeneous `k=0`, zero-acceleration and finite nonzero modes are separate obligations.

Do not insert an extra particle species, arbitrary halo, fitted per-object force correction or imported gravity law to make a task pass. A clearly labelled extension can be investigated as a **candidate** when the task asks for it, with every new function/constant counted and the altered equations varied. GR limits, reference models and observations are legitimate comparisons, not substitute mechanisms. Quantum, Standard-Model and absolute-value-of-G derivations are not required to satisfy the amended thirteen-item effective gravity target.

## Evidence rules

Prove identities from equations; do not cite old PASS counts as proof. An empirical preference is not a mechanism. A finite grid is not a universal theorem. A symbolic formula under assumptions proves only that implication. Lean certifies its actual declarations and axioms, not surrounding physical claims. A program exiting zero does not establish a physical result.

Use project-local sources first. If an external theorem or measured bound is essential, verify its exact primary source, hypotheses, conventions and date; record the version and cache/hash permitted source material. Without source access, mark that dependency blocked. No invented catalog rows, citations, uncertainties or current bounds. Read existing code before execution; many historical scripts overwrite their own outputs. Reproduce into the task's unique output directory and preserve original artifacts.
