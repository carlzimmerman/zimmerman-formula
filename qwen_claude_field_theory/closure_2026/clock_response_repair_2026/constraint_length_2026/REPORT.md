# Action-derived clock length: a metric response and a hierarchy restriction

2026-09-11. Starting commit `64c04ee14`. Full theory: **OPEN**.

Carl Zimmerman's primordial-clock idea and request for a galaxy/cluster
separation mechanism motivated this calculation. This does not introduce a
new particle, select new coefficient functions, or claim a new fundamental
interaction. All previous action and evolution files are unchanged.

## The equation

On the existing stationary profile, at zero cubic coupling,

\[
\boxed{(H\ell)^2=\frac{m(m+2)}{9(m+1)v(1-v)},\qquad
\frac{\Psi_k}{\Psi_{N,k}}=
1+\frac{9\Omega(1-v)/(2m)}{x^2+(H\ell)^{-2}}.}
\]

Here units have c=1; restore the dimensionless length as H ell/c.
The first equation is a background constraint length. The second describes
the initial linear spatial Bardeen potential for a conserved test-baryon
source, with u=udot=0. It is NOT a stationary galaxy solution.

Definitions and hypotheses:

- m=U/(q A)>0, 0<v<1, q=dot(chi), x=k/(a H)>0;
- Omega=(q A+U)/(3 M H^2), where the Python symbol M (`M2`) is the
  **squared reduced Planck mass**, not a mass;
- B0=A(m+2)/(qm), U=mqA, and the unchanged profile equation is
  qdot=-3Hqm v/(m+2)-A m q^2/(2 M H);
- Psi_N=-C/(2 M a k^2), C=a^3 delta-rho_k constant. This is the bare
  Poisson reference, not an assumed experimentally measured Newton constant.

Neither equation selects m or v from first principles. In particular these
results do not derive a0, kappa=1/2, or the exponential MOND kernel.

## Where it comes from

The same covariant candidate used in `../cubic_finite_wavelength/README.md` is

    S = integral sqrt(-g) [ M(R-2Lambda)/2 + P(X,tau)
          + sqrt(Xtau) W(Y,tau) - V(tau) + gamma X Box(chi) ] + S_m.

Its existing P/W/V functions were originally inverse reconstructions. They
are held fixed here, not promoted to first-principles coefficient predictions.
X=-grad(chi)^2, Xtau=-grad(tau)^2 and Y is the spatial chi-gradient squared
on the normalized tau foliation. The pre-existing derivation expands the
actual ADM action and solves its lapse/shift Euler equations. Its independent
compact-action equality, computed rank/null vector and variation checks are
rerun when this calculation imports it.

After the time-dependent change u=sigma-(q/H)zeta and integration by parts,

    L2 = A0 udot^2/2 + J zeta udot + Braw u udot
           + D zeta^2/2 + E zeta u + Craw u^2/2 + source,
    D = D0 + D2 k^2, E = E0 + E2 k^2.

Adding the actual test-source action -C n/2 and re-solving lapse/shift gives

    fz = C (U - 2 gamma q^2 qdot)/(4H(MH + gamma q^3)),
    D zeta + J udot + E u + fz = 0.

With w=zeta+(E2/D2)u and ell^2=a^2 D2/D0, this is

    (1 - ell^2 Delta_phys) w
        = [J udot + (E0-E2 D0/D2)u + fz]/(-D0).

The sign follows from Delta_phys -> -k^2/a^2. We vary the quadratic action,
not an assigned Helmholtz equation. The remaining kinetic coefficient is
Aeff=A0-J^2/D. Divisions require a,H,M,q,Aq+U,MH+gamma q^3,D0,D2,D nonzero;
a real screening length additionally requires D2/D0>0. Physical k=0 is
excluded: the original longitudinal shift inverse fails there.

The metric is independently reconstructed with beta=-a^2 b/k and
Psi=-zeta-H beta. Exact polynomial cancellation checks show that its
denominator really retains D at the selected epoch, for both selected
couplings. It is not just a
length assigned to an unobservable auxiliary field.

## The restriction, not a coefficient fit

Define f=U/(q A+U)=m/(1+m). For m>0 and 0<v<1,

\[
\boxed{\frac89 f\le (H\ell)^2,
\qquad H\ell\le r\ \Longrightarrow\ f\le\frac98 r^2.}
\]

This follows from v(1-v)<=1/4 and m+2>2. Lean checks the bound over the
specified real domain, not a sample of m,v values. f is a **background
coefficient ratio**, NOT the entire clock-dust abundance or its halo fraction.
For example H ell<=10^-5 requires f<=1.125e-10 in this gamma=0 branch.
This necessary condition is not a proof that such a tiny-coefficient branch
is healthy or viable; its singular limit needs separate analysis.

At the unchanged epoch m=1/10,v=1/2,a=1,H^2=4/15:

    (H ell)^2 = 14/165,
    H ell = 0.2912876325017677                       (gamma=0),
    H ell = 0.2912991292825209                       (gamma=1e-6),
    Psi/Psi_N = (28 k^2 + 109)/(28 k^2 + 88)         (gamma=0).

The gamma=0 metric corrections at x=10^4 and 10^5 are respectively
2.8124997e-8 and 2.8125000e-10. The gamma=1e-6 branch has an additional
small high-k normalization offset; it must not be mistaken for a screening
transition or an independently measured G. A cosmological-sized transition
does not supply the proposed strong galaxy-versus-cluster selector in this
initial linear response. This is not a no-go for every nonlinear clock theory.

## Verification and limits

`ConstraintLength.lean` proves five conditional algebraic theorems, including
the length bound and exact selected-epoch value. `verify.py` reads the actual
Lean definition and checks it against the action-generated expression.
The action variation and this bridge are SymPy calculations, **not Lean
formalizations of covariant calculus**. No proof of a law of nature follows.

Historical run_001 and run_002 preserve earlier script revisions. Their hashes
are not the final source hashes. The metric extension also computes Phi from
n+betadot with the actual canonical acceleration, rather than setting uddot=0
or assigning Phi=Psi. In run_003, 29 modes per coupling span
0.01<=k/(aH)<=100000. Max relative Phi-Psi differences are 5.30e-15
(gamma=0) and 8.58e-15 (gamma=1e-6). Complex-step derivatives at three
step sizes agree within 1.08e-14; centered fourth-order differences provide
an independent check within 1.36e-11. Those numbers are floating numerical
checks, not interval error bounds or an all-mode slip proof.

The two potentials use the same action's canonical acceleration. In
particular p=fv initially, pdot=fu; fixing udot=0 does not set uddot=0.
No late-time integration or disputed radial evolution is used.

Remaining gates include nonlinear dust redistribution, controlled evolution
(the earlier radial tangency issue remains unresolved), the exact MOND law,
static physical force/PPN, CMB and data tests, nonlinear constraints and global
stability. No late-time result from the disputed evolution is used here.

The next unavoidable calculation for this proposed mechanism is the
**inhomogeneous nonlinear constraint spectrum on a finite-density halo**,
with the same P/W/V: can its length shrink without loss of ellipticity,
and does the clock density actually deplete? A background linear length
cannot answer that. Any time evolution must first clear the existing radial
tangency/convergence gate. Adjusting m or reconstructing functions to place
ell at a chosen halo radius is not that calculation.

## Files, commands and exit statuses

All new files are confined to this `constraint_length_2026/` directory:
`derive_length.py`, `test_filter.py`, `verify.py`, `ConstraintLength.lean`,
this report, `contract.json`, `metric_contract.json`, `verify_contract.json`,
and five provenance directories (`run_001`, `run_002`, `run_003`,
`verify_001`, `verify_002`), each containing exactly `manifest.json`,
`result.json`, `stdout.txt`, `stderr.txt`. No existing theory file changed.

Final evidence:

| Command/test | Exit | Meaning |
| --- | --- | --- |
| `derive_length.py`, audited `run_003` | 0 | 13 checks including action identities and 58 numerical metric cases |
| `verify.py`, audited `verify_002` | 0 | Actual Lean definition bridge and five child commands |
| `python3 -m unittest discover -s .../constraint_length_2026 -p test_filter.py` | 0 | Three filter tests |
| `lake env lean .../ConstraintLength.lean` | 0 | Five theorems; only propext, Classical.choice, Quot.sound |
| Existing `point_certificate.py` | 0 | Exact action/Lean selected-epoch sign bridge |
| Existing `tensor_gate.py` | 0 | 26 existing homogeneous tensor checks |
| `lake env lean .../PointSigns.lean` | 0 | Existing selected-epoch certificate |
| Manifest validation with `--root .`, `run_003` and `verify_002` | 0 each | Final input/output hashes match |

Exact expanded child argument lists are in `run_003/manifest.json` and
`verify_002/result.json`; the wrappers and resource caps are recorded in
the manifests. Python ran from the repository root; Lean ran in
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.
Standalone commands for inspecting/repeating the current calculation:

```sh
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/constraint_length_2026/derive_length.py
python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/constraint_length_2026 -p test_filter.py
```

Development failures are not hidden: the initial three tests failed because
the implementation did not yet exist (exit 1); the first fixture then caught
a wrong hand-written sign in its own expected E2/D2 (exit 1, corrected from
7/3 to -7/3). An unnecessarily large negative-control factorization was
interrupted (exit 130) and replaced by an exact rational nonzero witness.
Two intermediate Lean compilations failed (exit 1: wrong inequality rewrite,
then an already-solved goal); both were corrected and final verification is
clean. Historical runs use earlier source hashes and are not current-evidence
certificates. Read-only inspection also encountered a nonexistent guessed
`checks.py` path; the actual existing `run_checks.py` was then inspected.

## Prior-art check

The general filter is not new. Afshordi, Chung, Doran and Geshnizjani,
*Cuscuton Cosmology: Dark Energy meets Modified Gravity*,
[arXiv:astro-ph/0702002v2](https://arxiv.org/abs/astro-ph/0702002v2),
Eq. (19), derive a denominator k^2/a^2-3 Hdot; Eq. (38) gives its Yukawa
real-space form. This is adjacent structure, not an equivalence to our
two-clock/cubic action. Their field and metric conventions differ; no DOF
or causality result is imported.

Bellini and Sawicki, *Maximal freedom at minimum cost: linear large-scale
structure in general modifications of gravity*,
[arXiv:1404.3713v2](https://arxiv.org/html/1404.3713v2), Eq. (27) and
discussion of (28), identify a braiding transition scale, commonly near the
horizon but not universally so. Their Horndeski parameterization is not
established here as equivalent to this clock action.

Checked primary texts on 2026-09-11 through arXiv; discovery queries used
cuscuton/constraint/Yukawa and kinetic-braiding/transition-scale synonyms.
No exhaustive citation-graph, patent or multi-database novelty search was
performed. Classify the compact coefficient relation and bound as **formal
corollaries of this repository's action**, not certified new laws. The
independent reviewer confirmed the two compact identities and bound; the
requested metric-denominator check was added in response to that review.
