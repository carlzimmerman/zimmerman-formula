# PAPER9 v2 amendment — closing the cubic-and-higher gap in the lensing lock

**Status:** drop-in amendment, not yet integrated. PAPER9 (`qwen_claude_field_theory/papers_2026/PAPER9_foliation_theorem_2026.tex`) is the lead track's file and is **not edited here**; this document supplies the replacement text and the supporting lane so the lead can integrate it.

**Supporting lane:** `fable_independent_2026/L265_curvature_order_pincer.py` / `.out` / `.json` — 9/9 checks PASS, rc = 0; `MUTATE=1` asserts that degree-3 invariants reach the linear response and the pincer breaks (A2 FAIL, rc = 1), so the hinge is load-bearing. The curvature pipeline is validated against the exact Schwarzschild Kretschmann (Riem² = 8(A:A) = 48(GM)²/r⁶) and vacuum Ric² = 0 **before** any new claim is made.

---

## 1. What this amends

PAPER9 §"What is not proved" currently closes its hypothesis-(iv) item with:

> **Genuinely open, and labelled:** the degree-1 theorem assumes asymptotic homogeneity, so an interpolating *F* that is never a power law is uncovered; η = 3/4 is a linear-response value; and **cubic and higher invariants were not enumerated, though the method extends to them.**

The third clause can now be struck. The first two are untouched by this amendment and remain open.

## 2. The argument, in one paragraph

The Riemann tensor is O(h) about flat space, so a curvature scalar that is a homogeneous polynomial of degree *n* is O(hⁿ). The **linearised** field equations — which carry *both* the weak-field force law and the lensing deflection — come from the O(h²) part of the action. Hence only curvature degree ≤ 2 can touch them. Degree ≥ 3 is invisible to the linear response, so it cannot modify a rotation curve or a deflection angle at all. And `□⁻¹` is a **linear** operator, so it preserves h-degree: the `□⁻¹` dressing that rescued the *quadratic* invariant in L59 (turning a star-dominated local invariant into a coherent-dominated nonlocal one) cannot promote a *cubic* invariant into the linear response. This is why L59's mechanism does not extend upward, and it is the reason the enumeration L59 deferred is not needed: the cubic-and-higher sector is excluded wholesale rather than case by case.

This closes the gap **in the opposite direction** from the one the deferred enumeration was expected to settle. L264 (`L264_lensing_lock_second_order.py`) had found that cubic invariants **do** generically separate Φ from Ψ — a second independent Riemann contraction breaks the Φ↔Ψ degeneracy on 7 of 8 random configurations, where the quadratic invariants cannot (R² = 0, Ric² = |A−B|², Riem² = 4(|A|²+|B|²), coefficient matrix singular). That separation is real. It is simply unreachable: the objects that possess it do not enter the equations that would have to be modified.

## 3. Drop-in replacement text (LaTeX)

Replace the final sentence of the hypothesis-(iv) item in `\section{What is not proved}` with:

```latex
\textbf{The cubic-and-higher sector is now closed, and by a structural argument rather than an
enumeration.} The Riemann tensor is $O(h)$ about flat space, so a curvature scalar that is a
homogeneous polynomial of degree $n$ is $O(h^{n})$, while the linearised field equations --- which
carry both the weak-field force law and the lensing deflection --- come from the $O(h^{2})$ part of
the action. Only degree $\le 2$ can therefore touch them: computed, the order-$h^{2}$ coefficient
of $\sqrt{-g}\,R^{n}$ is non-zero for $n=1,2$ and \emph{exactly zero} for $n=3,4$, and every
non-zero Riemann component carries leading order $h^{1}$, so the result extends to every degree-$n$
tensor invariant ($R_{\mu\nu\rho\sigma}^{\ \ 3}$, $R\,R_{\mu\nu}R^{\mu\nu}$, \ldots) without
expanding them (\texttt{L265\_curvature\_order\_pincer.py}, on a pipeline first validated against the
exact Schwarzschild Kretschmann $48(GM)^{2}/r^{6}$ and vacuum $R_{\mu\nu}R^{\mu\nu}=0$). Because
$\dal^{-1}$ is \emph{linear} it preserves $h$-degree, so the $\dal^{-1}$ dressing that makes the
quadratic invariant coherent-dominated cannot promote a cubic invariant into the linear response ---
which is precisely why L59's mechanism does not extend upward. The separation itself is real and was
verified: cubic invariants \emph{do} generically break the $\Phi\leftrightarrow\Psi$ degeneracy that
the quadratic ones cannot ($R^{2}=0$, $R_{\mu\nu}R^{\mu\nu}=|A-B|^{2}$,
$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}=4(|A|^{2}+|B|^{2})$ with $A=\mathrm{Hess}\,\Phi$,
$B=\mathrm{Hess}\,\Psi$; singular coefficient matrix), separating on $7$ of $8$ random configurations
at cubic order (\texttt{L264\_lensing\_lock\_second\_order.py}). It is unreachable rather than absent.
Two escapes are priced and both fail. A non-analytic power is the only way to drop a cubic invariant
into the $O(h^{2})$ action ($J^{2/3}\sim h^{2}$), and $f''(J)$ \emph{diverges} as $J\to0$: there is no
perturbative vacuum about Minkowski. And an $f(R)$-type scalar long-range enough to give a MOND-like
enhancement is Brans--Dicke with $\omega=0$, hence $\gamma_{\rm PPN}=1/2$ --- lensing sees $(1+\gamma)/2
=3/4$ of the dynamical mass, the lock in another costume --- while screening it to recover
$\gamma\to1$ removes the enhancement. \textbf{Hypothesis (iv) is therefore discharged against the
entire curvature-built class, local and nonlocal alike}, and not merely against the known nonlocal
models. What remains genuinely open is narrower: nonlocal objects \emph{not} built from curvature
(which violate hypotheses (ii) or (iii) instead), non-flat backgrounds, the asymptotic-homogeneity
proviso of the degree-$1$ theorem, and the linear-response status of $\eta=3/4$.
```

## 4. Abstract patch

In the abstract, the clause

> the locality hypothesis is discharged against the known nonlocal class rather than in general

should become

> the locality hypothesis is discharged against the entire curvature-built class, local and nonlocal alike --- the second-order residual is excluded three ways and the cubic-and-higher sector by an order-counting pincer (a degree-$n$ invariant is $O(h^n)$ while the linear response lives at $O(h^2)$, and $\dal^{-1}$ preserves degree) --- though not against nonlocal objects built from something other than curvature

## 5. Provenance, stated against interest

`L264_lensing_lock_second_order.py` was written without knowledge of `L59_second_order_scalars.py` and **duplicates its principal findings**: the identity `□⁻¹Q = ½|∇Φ|²`, the coherence reversal, and the correction to PAPER9's "nearest-star dominated" justification were all established first in L59, which additionally quantified the reversal (2.2×10⁶) and supplied the three independent exclusions. L264 adds only the degree-2 Φ↔Ψ degeneracy in explicit form and the cubic-order separation scan; PAPER9 should cite L59 as the primary source and L264 only for those two items. L264's own record additionally carries a retracted intermediate result (check C2): a degenerate configuration pair with all six invariants equal but different |∇Φ|² was briefly read as a decisive no-go, and a robustness scan showed such pairs are measure zero (1 in 8). That reading is not part of this amendment.

## 6. What this does **not** claim

It does not claim that a frame-free MOND theory is impossible in general — only that no theory whose MOND scalar is built from curvature (with or without `□⁻¹`) can both modify the linear response and separate the Newtonian from the lensing potential. It says nothing about non-curvature-built nonlocal structures, about non-flat backgrounds, or about whether nature is MONDian. The other two labelled-open items in PAPER9 §"What is not proved" stand unchanged.
