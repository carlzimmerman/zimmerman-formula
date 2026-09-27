# Independent XC1 review — 2026-09-26

**Normalized claim:** the C-H/K action, with L340's `nu_mono` constitutive replacement and positive `alpha_c`, has a strong-coupling scale far above Solar-System probes throughout the supplied parameter window, because its high-momentum interactions reduce to those of the healthy flat-space khronon and the remaining MOND interactions are uniformly heat-suppressed.

**Primary verdict: incomplete, with the smallest missing implication being a bound on the reduced cubic and quartic interactions of the *varied* heat action, with momentum-dependent physical normalization, on an actual nonzero-background solution.** The flat khronon calculation has substantial independent support. The claimed full-action G8 PASS does not follow. This review does **not** find a physical strong-coupling counterexample to C-H/K.

Scope is XC1. The user's two requested constitutive branches, published `nu_RAR` and frozen `mu_exp(x)=1-exp(-x)` with `x=g/a0`, remain distinct. L340's `nu_mono` is a third, explicitly modified branch; its positivity and XC1 estimates cannot be transferred to either requested branch without rebuilding the relevant background Hessian and reduced interactions. The frozen specification is recorded as historical contract evidence, not as permission to discard the user-requested RAR branch.

## Provenance and claim boundaries

The observed base is `f3b848273e635b81bc328882db0ffb4206d86e45`; the repository was dirty and changing. `snapshots.json` pins the exact reviewed files and SHA-256 values. Line citations below refer to those snapshots, which retain the original line numbers. No original script or output was overwritten. No Git operation changed repository state.

Authoritative artifacts:

- `snapshots/XC1_strong_coupling_chk.py`, especially lines 10–19, 21–60, 118–221, 223–264, 267–308, 357–440, and 453–464.
- `snapshots/ACTION.md`: domain and heat operator, lines 24–28 and 60–84; complete action, lines 95–106; lapse-weighted adjoint, lines 134–164; required heat variation, lines 217–229.
- `snapshots/L340_filtered_khronon_completion.py`: changed action and kernel, lines 8–16; limitations, lines 60–63; actual kernel construction, lines 102–120.
- `snapshots/FRIED_CHICKEN_SPEC.md`: same-action condition, lines 3–4 and 53–59; stability and zero-field obligations, lines 33–39; no pass-count promotion, lines 67–69.
- The live recipe's G8 wording at lines 327–328 requires canonical normalization on the **actual** Solar-System background. That is also quoted in XC1 lines 10–12, so the review does not depend on the changing recipe introduction.

## Dependency graph and obligation matrix

```text
Specified C-H action + alpha_c a² - c2 K² + specified kernel
  ├─ freeze metric/flat clock → exact khronon jets → canonical class counting
  │    └─ small-coupling khronometric formula → large UV scale [supported, conditional application]
  ├─ frozen U quadratic block → 2C/(1+C) inertia [supported]
  ├─ fixed-filter radial q expansion → one longitudinal cubic [supported locally]
  └─ all C-H/K physical interactions uniformly negligible
       ├─ metric/clock variations of S [not computed; naive leg bound fails]
       ├─ nonlinear U/lapse/shift elimination and quartic vertices [not computed]
       ├─ physical normalization across filter transition [not held fixed]
       └─ actual nonzero Solar-System background and its derivatives [not supplied]
            → full-action G8 PASS [missing implication]
```

| Obligation | Result | Exact scope |
|---|---|---|
| Flat khronon quadratic and cubic from normalized clock | Passed | Independently reconstructed in 3-vector notation and by an exact 1+1 reduction |
| Quartic khronon scaling classes | Passed on an independent subset | Exact 1+1 jets already realize all eight derivative/coupling classes found by XC1 |
| Literature formula and notation | Passed | 2018 source, small-coupling decoupling regime; not a C-H/K background theorem |
| Rectangular window minimum of that formula | Passed conditionally | Algebraic monotonicity establishes the corner minimum; not just grid sampling |
| Quadratic U elimination | Passed | Frozen Fourier block, k nonzero, C nonnegative |
| All of C-H vanishes when U=ln N | Failed as worded | Only the displayed gradient/acceleration square vanishes; the constitutive term remains |
| Direct longitudinal q cubic coefficient | Passed conditionally | Smooth kernel, nonzero background, fixed filter; not all cubic or quartic terms |
| Heat factor on every varied field leg | Failed | Explicit admissible compact-leaf Fourier witness below |
| A8 expression is the canonically normalized direct cubic at all k | Failed | The normalization and U-elimination denominators depend on k |
| Full G8 on actual Solar-System solution | Not addressed | Flat/frozen surrogate plus unbounded omitted terms |
| y=0 and monotone splice | Not addressed / nonsmooth | Constitutive Taylor expansion is unavailable at both exceptional cases |
| Loops / quantum completion | Out of scope | XC1 explicitly excludes these; no claim inferred |

## Supported reconstruction

Write `q=pi_t`, `v=grad pi`, `b=grad pi_t`, `T=pi_tt`, and `H=Hess pi`. For `tau=t+e pi`, expanding the definitions with signature `(-+++)` gives

```text
a_i = -e b_i + e²(T v_i + q b_i + (H v)_i) + O(e³),
a_0 = -e² v.b + O(e³),
K   = -e tr H + e²(2 v.b + q tr H) + O(e³).
```

Consequently `L2=alpha |b|²-c2(tr H)²` and

```text
L3 = 2 c2 tr H (2 v.b + q tr H)
     - 2 alpha [T v.b + q |b|² + b.Hv].
```

These agree with XC1 lines 153–159; the jet construction at lines 134–151 has the correct signs. Independently, restricting to dependence on `(t,x)`, the exact acceleration and expansion have numerators

```text
A = (1+pi_t) pi_x pi_tt - [(1+pi_t)²+pi_x²] pi_tx
    + pi_x(1+pi_t) pi_xx,
B = -pi_x² pi_tt + 2(1+pi_t)pi_x pi_tx -(1+pi_t)²pi_xx,
L = (alpha A²-c2 B²)/[(1+pi_t)²-pi_x²]³.
```

Expanding this rational expression independently reproduces the cubic and gives all eight class tuples `(fields,coupling,time derivatives,total derivatives)` used in A2. Their sound-speed exponents are `3/2, 1/2, -1/2`. With `phi=M sqrt(alpha)|k| pi`, `t_tilde=c_s t`, and `phi_tilde=sqrt(c_s)phi`, the transformed coefficient is

```text
g M^(2-F) alpha^(-F/2) c_s^(n_t-F/2-1).
```

The resulting suppression scale is a momentum scale in these rescaled coordinates. This supports XC1's flat-sector power counting, not a full scattering-unitarity theorem or an exhaustive all-order analysis.

For XC1's superluminal khronometric formula,

```text
k_sc^4 = M^4 alpha_c³ (2+3c2)/[c2(2-alpha_c)].
```

It increases with `alpha_c` and decreases with `c2` on the positive parameter rectangle used here. Thus the lowest corner is `alpha_c=9.6240479669e-14`, `c2=1/15`: `c_s≈7.9356e5`, `k_sc≈8.4799e8 GeV`, approximately `6.523e4` times 13 TeV. The scale is large **if** this local khronometric truncation controls the physical UV interactions. The external source and the omitted vertices do not establish that last hypothesis.

## Decisive missing heat interaction

XC1 lines 58–60 explicitly omit the metric/foliation Fréchet vertices. Nevertheless lines 263–264 and 456–458 say the UV theory *is* the BPS khronon, and lines 437–440 extend a one-variable exponential maximum to *every* MOND vertex. These are stronger than the implemented computation.

Here is a counterexample to the operator-level exponential-per-leg inference within ACTION.md's compact-leaf domain. On `T³`, vary the leaf metric by

```text
h_ij(epsilon)=exp(2 epsilon sigma(x)) delta_ij.
```

This is a smooth positive metric for small real epsilon. In three spatial dimensions,

```text
delta Delta = -2 sigma Delta + grad sigma.grad,
(delta Delta)_(p,q) = (3|q|²-p.q) sigma_(p-q).
```

Duhamel's formula from ACTION.md lines 217–218 therefore gives, for unequal squared momenta,

```text
(delta S)_(p,q)
 = [exp(-b|q|²)-exp(-b|p|²)]/(|p|²-|q|²)
   * (3|q|²-p.q) sigma_(p-q).
```

The equal-eigenvalue divided difference is `b exp(-b|q|²)`.

Take `sigma=cos((K-1)x)`, `U=cos(Kx)`, and `b=1/2`. The `cos(x)` output of `delta S U` has coefficient

```text
(3K²-K)/(2(K²-1)) [exp(-1/2)-exp(-K²/2)]
    → (3/2) exp(-1/2) ≈ 0.909796.
```

At `K=20` this coefficient is `0.896875`, whereas the purported hard-input exponential is `1.3839e-87`. The output is nonconstant, so its spatial gradient is not killed in the constitutive term. Taking real cosine modes and a conformal metric makes this an admissible smooth variation, not an arbitrary operator surrogate.

This proves that varying the filter can transfer a hard metric/scalar pair to a soft output without a hard-leg Gaussian. It does **not** prove a physical amplitude is large: constraints, metric normalization, other vertices, and cancellations still matter. Computing or bounding those is exactly the missing implication. The observation that an omitted term carries `alpha_M²` or background derivatives is not a bound after differentiation of `q`, division by powers of the small clock kinetic coefficient, and constraint elimination.

The A3 identity likewise annihilates only `2|DU-a|²` at `U=ln N`. The separate action term `2 alpha_M² q(|D S U|²/alpha_M²)` is generally nonzero there. On a fixed flat leaf, `ln N=-pi_t+(pi_t²+|grad pi|²)/2+...`; the heat operator on a product damps the product's total momentum, not each constituent momentum. The full intrinsic-foliation expansion and nonlinear auxiliary elimination are required before deciding whether such terms cancel.

## Other explicitly missing vertices and normalization

Let `w=D S delta U`, decompose it into parallel `w_L` and transverse `w_T` parts relative to a smooth nonzero background, and put `C_T=q'(y²)`, `C_L=C_T+y C_T'`. Direct expansion of the **fixed-filter** constitutive density gives

```text
L3_q = (1/alpha_M)[(2/3) C_L' w_L³
                          + 2 C_T' w_L |w_T|²],
L4_q = (1/alpha_M²)[(C_L''/6)w_L⁴
                          + C_T'' w_L²|w_T|²
                          + (C_T'/(2y))|w_T|⁴].
```

XC1 lines 359–397 check only the first cubic coefficient and five nonzero backgrounds. The quartic expansion at A1 is the khronometric `alpha a²-c2 K²` sector; it does not supply these constitutive quartics. Nonlinear elimination of `U` starts contributing additional quartic terms even when the cubic may be evaluated on the linear auxiliary solution.

Even for the one direct cubic retained, A8 freezes the A6 scale while `C(k)=C0 exp(-xi²k²)`, `U1=-pi_t/(1+C(k))`, the inertia, and the speed all vary. Within XC1's own decoupling-style normalization, the quantity replacing its fixed scale is

```text
g3(k) k² c_s(k)^(1/2) / [M alpha_eff(k)^(3/2)],
g3(k)=|C_L'(y)| exp(-3xi²k²/2)/[3 alpha_M (1+C(k))³],
alpha_eff(k)=alpha_c+2C(k)/(1+C(k)).
```

The run substitutes the exact frozen-block speed
`c_s²=c2(2-alpha_eff)/(alpha_eff(2+3c2))`. At the five A6 backgrounds, using the canonical a0, xi=0.031 pc, alpha_c at the supplied minimum, and c2=0.000631, the maximum lies near `xi²k²≈25–31`. It is roughly `4.2e4–2.4e6` larger than the corresponding fixed-normalization expression, but remains at most approximately `1.1e-33` in this diagnostic. **This is not an amended full-action G8 bound.** It shows precisely why the scalar maximum `max x exp(-3x/2)` is not the physical calculation, while preserving the evidence that this particular retained channel is very weak on these samples. The c2 value is a L350 cap used by XC1, below L340's tracking floor; no simultaneous cosmological/galactic parameter viability is inferred.

## Nonanalytic monotone splice

L340 lines 108–117 and XC1 lines 315–330 define

```text
h_mono'(y)=max(h_RAR'(y), 0.05 h_peak/(y+y_peak)).
```

The branch switch occurs at `y*=2.3374124053`, **before** the quoted phantom peak `y_peak=2.5396382822`. At the switch,

```text
C_L=0.006639363412,
C_L'(left) = -0.03610606160,
C_L'(right)= -0.001361348044.
```

Thus even the ideal continuum version has a continuous Hessian but no unique longitudinal cubic Taylor coefficient at this background. The tabulated, interpolated implementation introduces its own additional derivative boundaries. XC1's analytic `dCL` picks one branch and never samples the switch in A6. A smooth replacement or a separate nonsmooth analysis is needed; silently smoothing changes the specified kernel. This is additional to the original `y=0` nonanalyticity, which ACTION.md lines 90–93 already recognizes. A global claim cannot be obtained by sampling only `y≥0.01` away from the splice.

## External and formal dependencies

The 2018 primary source was checked directly: Gümrükçüoğlu, Saravani and Sotiriou, *Hořava Gravity after GW170817*, [arXiv:1711.08845v2](https://arxiv.org/pdf/1711.08845v2), 9 February 2018; [DOI 10.1103/PhysRevD.97.024032](https://doi.org/10.1103/PhysRevD.97.024032). Equations (2), (4), (15), and Appendix B support the action convention, scalar speed, and two small-coupling decoupling scale branches. Dictionary: source `alpha=alpha_c`, `beta=0`, `gamma=c2`, and `M_AE≈M_reduced` in that regime. It does not analyze C-H, a heat operator, the constitutive background, or Solar-System nonlinear vertices. The cited 2010 calculation is discussed by the 2018 authors, but was not separately authenticated in this bounded review. The 2021 alpha=beta=0 result and the 2015 meV comparison are not used as load-bearing evidence here. Literature-cache lookup found no existing cache; full text was inspected via the primary arXiv PDF, without writing a repository-wide cache.

The auxiliary A7 identity follows algebraically **if** `a0=kappa c sqrt(G rho)` is supplied. It neither derives this relation from the action nor establishes dark-energy dynamics. The action explicitly treats a0 and Lambda as independent at ACTION.md lines 18–22.

The Lean certificate was inspected read-only. Its own lines 6–8 say that vertex expansions and window numbers are external computations. `filter_max` at lines 109–128 proves the scalar inequality; it contains no fields, metric, heat operator, canonical normalization, or constraint reduction. `class_exponents` at lines 136–148 evaluates eight prescribed rational expressions. These are appropriate algebraic certificates and cannot close the omitted physical implication. No Lean build was needed for this scope conclusion.

## Reproduction and smallest next calculation

`independent_checks_v2.py` is the current independent computation. `run2/results.json`, `run2/stdout.txt`, and `run2/manifest.json` record the exact/finite results. The manifest was generated by the computation-audit bounded runner and validates against the pinned inputs. Environment: Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4; timeout and CPU cap 60 seconds, output cap 1 MiB, numerical-library thread request 1. No random sampling. The original XC1 script was not rerun because it writes original outputs and its pass count would not decide the missing implication.

An initial independent run is retained under `run/` for transparency. SymPy's definite integration returned an incorrect *unused* equal-eigenvalue Piecewise branch. The corrected v2 writes the divided difference explicitly and verifies its continuous diagonal limit. Only `run2` supports the report; none of the numeric witness modes or other reported results changed.

The cheapest discriminating next calculation is to select a smooth nonzero background for **each** specified constitutive branch and compute the reduced cubic vertex containing one metric/foliation variation of the heat operator and two scalar fluctuations, retaining hard-hard-to-soft momenta. Include the lapse/shift/U constraints and the true quadratic eigenmode normalization. If this vertex is harmless, perform the associated quartic contact/exchange calculation, including the nonlinear auxiliary solution, before asserting a uniform G8 bound. Actual Solar-System background derivatives and the exceptional y=0/splice cases remain separate obligations.

**Strongest safe statement:** positive `alpha_c` yields a large flat khronometric suppression scale, and the sampled fixed-filter longitudinal MOND cubic is very weak under the stated approximations. Neither result presently proves full-action Solar-System strong-coupling safety.
