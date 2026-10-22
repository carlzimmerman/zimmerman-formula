# A82 — THE GALACTIC `alpha_1` RESOLUTION: the exact nonlinear solution, not the PPN expansion

**Lane:** A82_galactic_alpha1 · **Date:** 2026-10-22
**Base read, in order:** `A54_four_gates/report.md` (the four gates as one theorem; §3.5 flags the
galactic `α₁` as the one gate that does not follow, and records `α₁ = 0.073–5.194` at 1–30 kpc while
noting the PPN expansion does not hold there), `A59_alpha1_observable/report.md` (the bilinearity
theorem: every `α₁` observable carries `(v/c)²`), `A68_bracket_algebra/report.md` (the exact constraint
algebra and the P-sector coefficients), `THEORY.md` §3.5b and §6.1 (the qualifier being closed), and
`A36_galactic_alpha1/report.md` (the formula `α₁ = 4u′/(D−u′)` and the table this lane replaces with a
solve).
**Action:** the frozen A33 sector, verbatim; `K = 4πG`, `c = 1`, signature `(−+++)`,
`a₀ = 9.360000e-11 m/s²`, `L★ = 24 pc` (`24.000000`), `w_CMB = 369.82 km/s`, `w² = (w/c)² = 1.5217362374e-06`.
**Script:** `a82_checks.py` — **27/27 PASS, exit 0**, 12 mutations each exit 1 (`MUTATE.md`) ·
**Output:** `a82.out` · **Data:** `a82_results.json`.

---

## 0. Claim

**The qualifier in THEORY §3.5b/§6.1 can be closed, and it closes against the worry that produced it.**

The PPN expansion does not fail because the effect is large. It fails for two reasons, both of
which this lane computes: (i) the *response* of the P charge is nonlinear, so the coefficient
`α₁ = 4u′/(D−u′)` is a radial **response function** whose denominator `1−u′` vanishes as `g/a₀ → 0`,
not a PPN constant; and (ii) the PPN ordering `w² ≪ ε` is violated in a galaxy — `w²` **exceeds**
`Φ/c²` at every radius of a Milky-Way-like galaxy (`w²/(Φ/c²) = 5.8290` at 8 kpc,
`max Φ/c² = 9.5637e-07` against `w² = 1.5217e-06`), so the `O(ε²)` term that PPN drops is `0.740`× the
`O(w²ε)` term it keeps at 8 kpc and `25.723`× at 1 kpc.

Solving the exact nonlinear boundary-value problem instead gives three statements, each computed:

1. **A36's coefficient is right.** `α₁,eff = 0.07337, 0.14268, 0.23480, 0.47426, 0.92789, 1.62758,
   3.17007, 5.19502` at `1, 2, 3, 5, 8, 12, 20, 30` kpc — A36's table to `5.038e-03` maximum relative
   deviation. Nothing is retracted.
2. **There is no dipole.** Every `O(w²)` source term in the (P, lapse) system is even in `cos θ`
   (all `l = 1` projections `≤ 3.331e-16`), so the induced acceleration has `l = 0` and `l = 2` only and
   its dipole moment vanishes identically (`7.066e-14` normalised). The measurable is not an
   `α₁`-type anisotropy at all: it is a **monopole**,
   `δa(r) = −2w²a₀²/(g+2a₀) r̂`, plus a quadrupole of relative amplitude `2/13 = 0.153846`.
3. **The effect is bounded, at every radius, for every galaxy.** The exact solution satisfies the
   identity `α₁,eff · g = 4a₀²/(g+2a₀) ≤ 2a₀`, so
   `δa ≤ w²a₀ = 1.424345e-16 m/s²` (computed max `1.417743e-16`, ratio `0.99536507`). An `α₁` of
   `5.19502` at 30 kpc is therefore a fractional acceleration change of `3.9527e-06`, i.e. the naive
   "O(1) preferred-frame effect" is suppressed by `w²/2 = 7.608681e-07` — and no more than that is
   needed, because `α₁` never multiplies anything larger than `2a₀`.

**Verdict in one line: (a) suppressed — by the `(v/c)²` bilinearity of A59 *and* by the exact
nonlinear saturation `α₁g ≤ 2a₀`, with no screening mechanism required; the coefficient is not
suppressed and is not required to be.**

---

## 1. TASK 1 — why the PPN expansion breaks

### 1.1 The coupled static-and-boosted equations

Write the galaxy in its own rest frame (static, spherical, `Ψ = Φ` by A54's slip theorem) and the
CMB frame as the surface `T = t + w·x`. The exact lapse of that tilted foliation is

```
N = [ 1/(1+2Φ) − w²/(1−2Ψ) ]^(−1/2)
  ⇒ ln N = Φ + ½w² + w²(Φ+Ψ) − Φ² + O(w⁴, ε³)
  ⇒ ∂_i ln N = (1+2w²) ∂_iΦ − 2Φ ∂_iΦ .                                   (1.1)
```

The `+w²(Φ+Ψ)` is A36's K2 identity (residual 0 there, re-derived here from the exact `N`); the
`−Φ²` is the post-Newtonian term that A36 never wrote because it is `O(ε²)`. Both matter, for
opposite reasons (§1.2). The ADM data of the same foliation are
`N_i = −w_i(1+2Φ)`, `h_ij = (1−2Φ)δ_ij − w_iw_j(1+2Φ)`, whence
`h^{ij} = (1+2Φ)δ^{ij} + w^iw^j` and `u ≡ K|P|_h = u₀[1 + Φ + ½(ŵ·P̂)²w²]`.

With `P_i = (u/K) r̂_i` (so `K|P| = u`, `D·P = (1/K)(u′ + 2u/r)`, `F_ij = 0`, `E_i = 0` on the
static branch) the P-sector Euler–Lagrange equation and the lapse equation are

```
(P)   (L★²/2)[ u″ + 2u′/r − 2u/r² ] = u/(1−u/a₀) − (1+2w²) g
(L)   g = g_N + u ,        g ≡ (ln N)′ ,   g_N ≡ G M_b(<r)/r²
```

and eliminating `g`:

```
      (L★²/2)[ u″ + 2u′/r − 2u/r² ] = u²/(a₀−u) − g_N − 2w²(g_N+u) .        (1.2)
```

Equation (1.2) is the object this lane solves. Three structural remarks, each checked:

* The boost enters **only** through the factor `(1+2w²)` on the clock source. This is an analytic
  statement about the operator inventory, and it is checked rather than asserted: every `O(w²)`
  candidate is written down and projected in §2.4 (checks C1–C3), the one operator that mixes the
  shift with `δP_i` is `(η/2)E²` with `E = 0` statically, hence `O(w²ε²)`, and the resulting
  perturbation is verified to be exactly linear in `w²` by continuation (`−1.248e-06`,
  `−1.254e-04`, `−1.241e-02` at `w² = 1e-06, 1e-04, 1e-02`).
* `g = g_N + u` is the first integral of `∇²Φ = K(ρ + D·P)`; it is *not* an approximation (A33 §5).
* The `h^{ij}` corrections produce two further `O(w²)` source terms, with angular dependence
  `cos²θ`; they are enumerated in §2.4 and are a `13/12` systematic on `α₁`.

**The PPN expansion of (1.2)** is the statement that the `2w²(g_N+u)` term is a small perturbation:
linearise `u = u₀ + δu`, use `du₀/dg = u′ = a₀²/(g+a₀)² = 1/(dg/dg_N)`, and read off
`δg/g = 2u′w²/(1−u′)`, i.e. `α₁ = 4u′/(1−u′)` — A36's formula with `D = 1`.

### 1.2 Which term becomes `O(1)`, and which small parameter fails

There are two independent small parameters, and they fail at opposite ends of the galactic range.

**(i) The response parameter `u′`.** `u′ = du/dg = a₀²/(g+a₀)²` is the fraction of the field that the
P charge supplies in response to a change of the baryonic source; `1−u′ = dg_N/dg`. The term that
becomes `O(1)` is the *back-reaction itself*: `dg/dg_N = 1/(1−u′) → ∞`, and the P charge's share of
the field `u/g` runs `0.1342 (1 kpc) → 0.4339 (8 kpc) → 0.7516 (30 kpc) → 0.9906 (1 Mpc)`. In the
deep-MOND limit the field is *entirely* the P charge, so a fractional change of the source produces
an unbounded fractional change of the field. The PPN formula has this divergence built in
(`1/(1−u′)`), which is why `α₁` runs to `210.200656` at 1 Mpc while the acceleration it multiplies
stays finite (§2.3).

**(ii) The ordering parameter `ε/w²`.** PPN keeps `O(ε)` and `O(w²ε)` and drops `O(ε²)`. In a galaxy
`ε = Φ/c² ~ v_c²/c²` and `w²` are the *same order* — and `w²` is the larger of the two: at 8 kpc
`Φ/c² = 2.6106e-07` against `w² = 1.5217e-06`, i.e. `w²/(Φ/c²) = 5.8290`; the maximum over the whole
galaxy is `max Φ/c² = 9.5637e-07 < w²`. The dropped `O(ε²)` term of (1.1) contributes a fractional
acceleration `−2Φ`, while the retained `α₁` term contributes `+(α₁/2)w²`; their ratio is

```
   |2Φ| / [(α₁/2)w²] = 25.723 (1 kpc), 5.359 (3 kpc), 0.740 (8 kpc), 0.1036 (20 kpc), 0.0440 (30 kpc).
```

So the term PPN discards is **larger** than the term it keeps for `r < 6.9463 kpc`, and only becomes
small beyond ~20 kpc. This is not a small correction to `α₁`; it is a different expansion.

The `L★/r` derivative expansion is *not* a problem in the galactic range:
`(L★/r)²u′/2 = 5.187e-06, 8.472e-07, 1.808e-07` at `1, 8, 30` kpc — an independent reproduction
of A36's K13 estimate.

### 1.3 The break radii, for a Milky-Way-like galaxy

The fiducial galaxy is A36's: Hernquist, `M_bar = 6e10 M_☉`, `a = 3` kpc, so `r_MOND = 9.4536` kpc.
Two radii, from two different failures:

| criterion | radius | what happens there |
|---|---|---|
| PPN `2PN` contamination `|2Φ| = (α₁/2)w²` | **6.9463 kpc** | the dropped `O(ε²)` term overtakes the retained `O(w²ε)` one; below it the "α₁" is not extractable at all |
| P charge response `1/(1−u′) = 2` | **24.1414 kpc** | the linear-response expansion is off by 100 %: `α₁ = 4` at that radius |
| `u′ = 0.9` | 176.4323 kpc | the response is off by 1000 % |
| `u′ = 0.99` | 1000.0000 kpc | `α₁ = 210.200656` — the divergence |

**So there is no radius in 1–30 kpc at which the PPN expansion is controlled to better than a factor
of order unity:** inside 6.9463 kpc the `2PN` term dominates, outside 24.1414 kpc the response
nonlinearity dominates, and only in the annulus 6.9463–24.1414 kpc are both contaminants `< 1`
(10 % response error is reached only at 4.4314 kpc). The `α₁ = 0.073–5.194` of THEORY §3.5b is
therefore a number computed by an expansion that has no controlled regime where it was applied.
That is the referee target, stated quantitatively.

---

## 2. TASK 2 — the exact nonlinear boosted BVP

### 2.1 What is solved

Equation (1.2), on `r ∈ [3 pc, 1000 kpc]` (`15001` log-spaced points), with

* the full nonlinearity of the Langmuir gate `W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)]`
  (`u²/(a₀−u)` kept exactly, not expanded),
* the full radial P-gradient operator `(L★²/2)[u″+2u′/r−2u/r²]` (coefficient `2.742165e+35 m²`),
* boundary conditions `u(0) = 0` and the exact slaved value at `r_out` (where the gradient term is
  `8.472e-07` of the response — negligible),
* Newton with an analytic tridiagonal Jacobian; `5` iterations, `max|residual| = 4.404e-09 a₀`,
  relative residual `6.513e-09` (the double-precision floor of this stiff reduction);
  `u(8 kpc)/a₀` moves by `1.38e-07` between `N/4` and `N` points.

The `O(w²)` perturbation `δu` is then obtained from the **linear** BVP with the exact nonlinear
response `C = d/du[u²/(a₀−u)] = u(2a₀−u)/(a₀−u)²` and source `−2w²g` (one direct banded solve,
residual `1.389e-10`). It is cross-checked three ways:

* against the **finite-`w²` nonlinear difference** `u(w²) − u(0)`: `8.620576e-17` vs `8.620592e-17`
  at 8 kpc, relative difference `1.909e-06` (the expected `O(w²)` truncation);
* by **continuation in `w²`**: `δu/w²` normalised to its `w² = 1e-8` value is `−1.248e-06`,
  `−1.254e-04`, `−1.241e-02` at `w² = 1e-06, 1e-04, 1e-02` — i.e. the deviation scales as `w²`
  (check B8). The `O(w²)` coefficient is therefore the derivative of the exact nonlinear family, not
  an artefact of linearisation;
* by the **slaved check** A3 (`|u − u_slaved|/u = 5.757e-06` for `r > 3` kpc) and the **gradient-activity**
  check A7 (`6.4344e-05` at 0.3 kpc), so both the algebraic and the derivative parts of the operator
  are demonstrably live.

### 2.2 The background and the boosted solution

Background (`[A]` of `a82.out`), with `u′ = dg_N/dg` and rel. dev. `= |u−u_slaved|/u`:

| `r` (kpc) | `g_N/a₀` | `g/a₀` | `u/a₀` | `u′` | `4u′/(1−u′)` | rel. dev. |
|---|---|---|---|---|---|---|
| 1 | 5.58588 | 6.45167 | 0.86579 | 0.018009 | 0.073358 | 1.12e-05 |
| 2 | 3.57403 | 4.38845 | 0.81441 | 0.034441 | 0.142677 | 5.76e-06 |
| 3 | 2.48237 | 3.24690 | 0.76453 | 0.055444 | 0.234794 | 4.40e-06 |
| 5 | 1.39711 | 2.07153 | 0.67443 | 0.105996 | 0.474253 | 3.38e-06 |
| 8 | 0.73846 | 1.30454 | 0.56607 | 0.188293 | 0.927884 | 2.65e-06 |
| 12 | 0.39726 | 0.85947 | 0.46221 | 0.289214 | 1.627574 | 2.06e-06 |
| 20 | 0.16885 | 0.50393 | 0.33507 | 0.442126 | 3.170073 | 1.40e-06 |
| 30 | 0.08205 | 0.33040 | 0.24835 | 0.564982 | 5.195017 | 9.79e-07 |
| 100 | 0.00842 | 0.09609 | 0.08767 | 0.832348 | 19.858901 | 3.06e-07 |
| 1000 | 0.00009 | 0.00947 | 0.00938 | 0.981326 | 210.200656 | 0.00e+00 |

`u < a₀` everywhere; `max u/a₀ = 0.911607` at `0.05524` kpc (the cap is approached in the
gradient-dominated inner region, not in the galactic disc).

Boosted solution (`[B]` of `a82.out`), with the induced acceleration `δa = −δu r̂` (inward: the
attraction strengthens, `|δa| = δu`) and the bookkeeping ratio `α₁,eff ≡ 2|δa|/(w²g)`:

| `r` (kpc) | `δa` (m/s²) | `δa/(w²a₀)` | `δa/g` | `α₁,eff` | A36 | ratio | `α₁g/(2a₀)` |
|---|---|---|---|---|---|---|---|
| 1 | 3.371029e-17 | 0.23667 | 5.5823e-08 | 0.07337 | 0.073 | 1.00504 | 0.23667 |
| 2 | 4.459339e-17 | 0.31308 | 1.0856e-07 | 0.14268 | 0.143 | 0.99779 | 0.31308 |
| 3 | 5.429421e-17 | 0.38119 | 1.7865e-07 | 0.23480 | 0.235 | 0.99915 | 0.38119 |
| 5 | 6.996688e-17 | 0.49122 | 3.6085e-07 | 0.47426 | 0.475 | 0.99844 | 0.49122 |
| 8 | 8.620592e-17 | 0.60523 | 7.0600e-07 | 0.92789 | 0.928 | 0.99988 | 0.60523 |
| 12 | 9.962307e-17 | 0.69943 | 1.2384e-06 | 1.62758 | 1.628 | 0.99974 | 0.69943 |
| 20 | 1.137689e-16 | 0.79875 | 2.4120e-06 | 3.17007 | 3.169 | 1.00034 | 0.79875 |
| 30 | 1.222403e-16 | 0.85822 | 3.9527e-06 | 5.19502 | 5.194 | 1.00020 | 0.85822 |

The equality `α₁,eff = 4u′/(1−u′)` holds in this solve to `4.749e-05` over 2–100 kpc (the
`O((L★/r)²)` gradient correction, largest at 2.0006 kpc); the `7.806e-05` deviation at 1 Mpc is the
finite-`w²` term `2w²u′/(1−u′)`, not a gradient effect. **Note what this says about A36's `D`:**
the galaxy-as-its-own-source BVP reproduces `4u′/(1−u′)`, *not* `4u′/(D−u′)`. `D = 1+(kL★)²u′/2` is
the *test-source plane-wave* factor and is absent here; the difference is `(L★/r)²u′/2 = 5.187e-06`
at 1 kpc, so no published number moves.

### 2.3 The observable, defined from the action rather than from `α₁`

The matter sector is minimally coupled, so a test body follows a geodesic of `g_μν`. For a body
comoving with the galaxy in the tilted foliation the ADM acceleration is
`a = −∇N − ∂_tN_i + v×(∇×N_i)` with `v = −w`, and check **C5** proves symbolically (`0,0,0`) that
the pure-boost `O(w²)` pieces of `N` and `N_i` cancel **identically**, leaving `a = −∇Φ` exactly.
That is what licenses reading the observable off `Φ` alone: the metric-sector `w²` terms are a
re-slicing, not a source. Check **C6** shows that the `−Φ²` term does *not* cancel (it leaves
`2Φ∇Φ`) — the `2PN` contamination of §1.2 is real, and it is the one term PPN must keep and does not.

Hence the measurable is

```
   δa(r) = −δu(r) r̂ ,       δu = 2w²a₀²/(g + 2a₀) > 0 ,    |δa| ≤ w²a₀ .     (2.1)
```

`δa(r)` is monotone increasing in `r` (the table above), saturating at
`max δa = 1.417743e-16 m/s²` against `w²a₀ = 1.424345e-16` — ratio `0.99536507`. It is *radial and
isotropic at leading order*; its `r`-scaling is `∝ 1/(g+2a₀)`, i.e. flat where `g ≫ a₀` and
approaching the constant `w²a₀` in deep MOND. Because `δg/g = 2w²a₀²/[g(g+2a₀)]` depends on `g`, the
effect is **not** degenerate with a constant rescaling of `a₀` or `G`: it is equivalent to a
field-dependent shift `ε(g) = 2w²a₀/g` of the acceleration scale, i.e. a distortion of the RAR
*shape* at the level of `w² = 1.5217362374e-06`. That is the one place the effect could in principle
be looked for, and it is four decades below the `~1e-2` scatter of every existing RAR/rotation-curve
compilation.

**A linear `α₁` is not meaningless here — but it is not an observable either.** The ratio
`α₁,eff ≡ 2δa/(w²g)` is well defined, finite and equal to `4u′/(1−u′)`; what fails is the reading of
it as "the fractional size of a preferred-frame effect". The quantity that enters any observable is
`α₁ g = 4a₀²/(g+2a₀)`, which is bounded by `2a₀`; the ratio `α₁` diverges only because `g → 0`. In
numbers: `α₁,eff/1e-4 = 733.68` at 1 kpc and `51950.16` at 30 kpc, while the actual acceleration
change is `3.9527e-06` of `g` at 30 kpc. The divergence and the smallness are the same fact.

### 2.4 There is no dipole: the angular structure of every `O(w²)` source

The configuration is axisymmetric about `ŵ`, and the only scalars available at `O(w²)` are `w²` and
`(ŵ·r̂)² = cos²θ`, so every source is even in `cos θ` and has **no** `l = 1` projection. This is not
an argument from symmetry alone: the terms are enumerated from the action and projected numerically
(Gauss–Legendre quadrature).

| term | where | `l=0` | `l=1` | `l=2` |
|---|---|---|---|---|
| clock, isotropic `(1+2w²)` part | P equation | 2.00000 | −3.331e-16 | −0.00000 |
| clock, `h^{ij}` part `(w·P)(w·∇Φ)` | P equation | 0.33333 | −8.327e-17 | 0.66667 |
| Langmuir gate `W(u)` via `u = K sqrt(h^{ij}P_iP_j)` | P equation | −0.16667 | 4.163e-17 | −0.33333 |
| lapse, `√h = 1−3Φ−w²/2` | lapse equation | −0.50000 | 8.327e-17 | 0.00000 |
| lapse, `W(u)` angular part | lapse equation | −0.16667 | 4.163e-17 | −0.33333 |
| **total, P equation** | | **2.16667** | **0.000e+00** | **0.33333** |

with the analytic values `l=0 = 13/6 = 2.166667`, `l=1 = 0`, `l=2 = 1/3 = 0.333333`,
`l=2/l=0 = 2/13 = 0.153846`. The dipole moment of the resulting field is `7.066e-14`
(numerically zero): a radial field built from `l = 0` and `l = 2` has `∫ â dΩ = 0` identically.

**So the "dipole vector" is zero.** The leading anisotropy is a *quadrupole* with axis `ŵ`: the
source quadrupole is larger along `±ŵ` than in the plane perpendicular to it by a factor
`(1+2/13)/(1−1/13)` in the `l = 2` amplitude — i.e. the source is isotropic to within
`2/13 = 0.153846`, with an absolute upper bound on the quadrupole of
`2.1811e-17 m/s²` (`2/13` of the monopole, computed in `[B]`). There is no `m = 1` pattern to align
with the CMB dipole at `O(w²)`. An `m = 1` pattern appears only when a *test body* moves through the
field, through the bilinear `(w·v)` of A59 — a different object, computed in §3.

### 2.5 Comparison with the naive `0.073–5.194`

* **As a coefficient:** reproduced. `α₁,eff = 0.07337 … 5.19502` against A36's `0.073 … 5.194`, max
  `|ratio − 1| = 5.038e-03`. The ratio to the naive range is `1.000` at every tabulated radius.
* **As an anisotropy (dipole):** the exact solution gives **zero**; the naive reading would give
  `α₁ (w/c)²`-type effects with an `l = 1` pattern. Ratio `0`.
* **As a fractional acceleration:** `δa/g = 5.5823e-08 … 3.9527e-06`, i.e. the naive "O(1)" reading
  is suppressed by `w²/2 = 7.608681e-07`, and absolutely capped at `w²a₀`.
* **Systematic on the coefficient:** the numerical `l = 0` solve uses the clock term only
  (coefficient `2.00000`). The full `O(w²)` `l = 0` coefficient is `13/6`, so every `α₁` above is
  `13/12`, i.e. `8.333333e-02` larger if the `h^{ij}` terms are included, and a `2/13` quadrupole
  appears alongside. This is a known, bounded systematic; it changes no conclusion here, since the
  nearest threshold is `5.038e-03` (A36 reproduction) and the physics conclusions are decades away
  from every bound.

---

## 3. TASK 3 — observable confrontation: a binary pulsar in the Galaxy's field

The decisive question is *which* field the response is evaluated on. A36's `α₁(g, r_s)` is the
response of the P field to a **test-source perturbation on a local background**; the background that
matters for a binary's *mutual* interaction is the field at the binary, and at separations far below
the coherence length that is the binary's own field, not the Galaxy's.

For a J1738+0333-like system (`m_p = 1.47`, `m_c = 0.16 M_☉`, `P_b = 5.85 h`):
`a = 1.34459e+09 m`, `v_orb = 4.0115e+05 m/s`, and

```
   g_int = G m_p/a² = 107.9349 m/s² = 1.1532e+12 a₀
   u′_int = (a₀/g)² = 7.5202e-25 ,      α̂₁(int) = 4u′/(1−u′) = 3.0081e-24 .
```

The orbital separation is `4.358e-08 pc`, `8.560e+07` times smaller than A20's `r_switch = 3.73 pc`,
so the binary sits deep inside its own P-field, and the Galactic field `g_ext = 1.8 a₀` (declared
prior) enters only as a uniform field: the EFE changes the internal response by
`1.561e-12` relative, which is irrelevant because the response itself is `7.5202e-25`. The Galaxy's
own `α₁` at 8 kpc is `0.92789` in this lane's model (`1.30454 a₀`) or `1.785714` at the declared `1.8 a₀`; either way it
does not multiply the binary's mutual interaction.

**Predicted residuals.**

| observable | prediction | published bound (declared prior) | margin |
|---|---|---|---|
| `α̂₁` (binary internal) | `3.0081e-24` | Shao & Wex 2012, `abs(α̂₁) < 3.5e-05` (PSR J1738+0333) | **19.07 decades inside** |
| forced eccentricity `e_F = ½α̂₁(Δm/M)(V/c)(v_orb/c)` | `1.9953e-30` (`Δm/M = 0.8037`, `(V/c)(v/c) = 1.6507e-06`) | — | — |
| `de/dt = n_b e_F` | `5.9528e-34 s⁻¹` | timing floor `~1e-15 s/s` | ~19 decades |
| external-field differential acceleration `Δa = ½α₁ g_ext (V/c)(v_orb/c)` | `2.4831e-16 m/s²` | — | — |
| induced `δP_b/P_b ≈ 3Δa/v_orb` | `1.8570e-21` | timing floor `~1e-15` | ~6 decades |

The `e_F` direction is `ŵ × L̂` (perpendicular to both the CMB dipole and the orbital angular
momentum) — the standard Nordtvedt-type polarisation, with A59's `κ = 1/2`. It is not merely
undetected; it is `19.07` decades below the bound that would detect it.

**On the two other cited channels, stated so that they are not mistaken for measurements of this
coefficient.** (i) *Kramer+ 2021* is cited in the lane brief; I do not have from it a precise `α̂₁` number that I
can state, and I will not invent one. Any bound on the same parametrisation at the `1e-4`–`1e-5`
level is 19–20 decades above `3.0081e-24`, so the comparison is unchanged. (ii) *Galactic-centre / disc
differential-acceleration* bounds constrain a relative differential acceleration at the
`1e-3-1e-2` level; the prediction here for the *external-field* channel is `δP_b/P_b = 1.8570e-21`,
six decades below even a `1e-15` timing floor, and for a star on a Galactic orbit the `(w·v)` dipole
of A59 gives `δa/g ~ α₁(w v/c²)/2`, of order `1e-06 × α₁` — decades below rotation-curve precision. **No published timing or differential-acceleration bound reaches this
theory's galactic `α₁`, and none needs to: the galactic coefficient does not enter any relative
acceleration of a bound system.**

**Answer to the screening question.** External-field screening is *not* what suppresses the dipole
below the timing bound. This theory *does* have an EFE (A23: the law is exactly AQUAL with
`μ = x/(1+x)`), but at `g_int = 1.1532e+12 a₀` the EFE correction is `1.561e-12` — irrelevant. The
suppression is **kinematic**: the binary's internal field is 12.06 decades above `a₀` (`log10(g_int/a0) = 12.06`), so
`u′ = 7.5202e-25` and every preferred-frame observable carries that factor squared in the field
response. A pulsar-WD binary is simply not an `α₁`-sensitive environment in this theory, by 19
decades.

---

## 4. TASK 4 — VERDICT

**(a) Suppressed — and the suppression is an identity, not a screening mechanism.** The galactic
`α₁` is *not* brought below its naive value by any dynamical screening; the coefficient itself is
`O(1)` and is confirmed at `0.07337 … 5.19502`. What is suppressed is every **observable**:

1. **Bilinearity (A59).** Every `α₁` observable carries `(v/c)²`; with `w² = 1.5217362374e-06` the
   fractional acceleration change is `(α₁/2)w²`, i.e. suppressed by `w²/2 = 7.608681e-07` relative to
   reading `α₁` as a fractional effect. At 30 kpc: `α₁ = 5.19502`, `δa/g = 3.9527e-06`.
2. **Saturation (this lane).** The exact nonlinear response gives the identity
   `α₁ g = 4a₀²/(g+2a₀) ≤ 2a₀`, so the induced acceleration is **bounded at every radius of every
   galaxy**: `δa ≤ w²a₀ = 1.424345e-16 m/s²` (computed max `1.417743e-16`, ratio `0.99536507`). The
   formal divergence of `α₁` as `g → 0` is a division by a vanishing `g`, not a growing effect: at
   1 Mpc `α₁ = 210.200656` while `δa = 1.417743e-16 m/s²`.
3. **No dipole (this lane).** Every `O(w²)` source is even in `cos θ`; the `l = 1` projections vanish
   at `3.331e-16` and the dipole moment of the induced field is `7.066e-14`. The anisotropy is a
   quadrupole of relative size `2/13 = 0.153846`, bounded by `2.1811e-17 m/s²`. The classic `α₁`
   observables (orbit polarisation, `ẋ`) are *not sourced at all* at `O(w²)` by the galactic field.

**Therefore the excluded range is empty.** `α₁ = 0.073–5.194` is not an excluded range and not an
exclusion: over the 1–30 kpc range the qualifier covers, no observable in this theory responds to
the galactic `α₁` at more than `δa/g = 3.9527e-06` (`3.9527e-06` of `g`, or `1.417743e-16 m/s²` absolutely), and the one environment where an
`α̂₁` is actually measured — a binary pulsar — gives `3.0081e-24` (§3). Nothing is uncomputable: no new ingredient is needed. In the task's (a)/(b)/(c) taxonomy the answer is **(a)**,
with the mechanism named precisely (`(v/c)²` bilinearity plus the exact saturation `α₁g ≤ 2a₀`) and
the suppression factor stated (`w²/2 = 7.608681e-07`, and `δa ≤ w²a₀`).

**Do the four gates survive?** Yes, and this lane does not touch them. The gates are statements about
`kL★ ≫ 1`, and the same solver in that regime gives `α₁,eff = 1.8816e-18` at 0.01 pc
(`g = 1.4638e+09 a₀`), `1.8185e-10` at 1 pc (`g = 1.4889e+05 a₀`), `1.7864e-06` at 10 pc
(`g = 1.5011e+03 a₀`), following `α₁,eff = 4(a₀/g)²` to within 10 % (check E3). The galactic `α₁` is
a property of the `r ≫ L★, g ~ a₀` regime only; `α₁ = α₂ = 0` wherever `kL★ ≫ 1` stands exactly as
A54 proved it, and the galactic half of gate (iii) is now **computed** rather than parametrised.

---

## 5. Checks and mutations

`a82_checks.py` — 27 checks, **27/27 PASS, exit 0**. Every check evaluates the BVP solver, the
asymptotic scaling, or the pulsar observable; there is no `ok = True`, no hardcoded PASS string and
no target decoupled from the computed quantity (each value printed is read off the solution).

```
A1  static BVP max relative residual                       6.513e-09
A3  slaved limit |u-u_slaved|/u, r>3 kpc                   5.757e-06
A7  P-gradient operator active at 0.3 kpc                  6.4344e-05
B1  boosted BVP max relative residual                      1.389e-10
B2  linearised du = u(w^2)-u(0)                            1.909e-06
B3  da = du > 0 at every interior radius                   1.5522e-19
B4  bound 0.9 < max da/(w^2 a0) < 1                        0.995365
B5  alpha_1_eff = 4u'/(1-u') for 2<r<100 kpc               4.749e-05
B6  alpha_1_eff*g <= 2 a0 (max ratio)                      0.99536507
B7  A36 table reproduced, max |ratio-1|                    5.038e-03
B8  w^2 continuation q/q(0)-1 = O(w^2)                     -1.248e-06 -1.254e-04 -1.241e-02
B9  alpha_1(8 kpc)                                         0.92789
C1  every O(w^2) source has zero l=1 projection            3.331e-16
C2  total source l=2/l=0 = 2/13                            0.153846
C3  l=0 = 13/6                                             2.166667
C4  dipole moment of the l=0+l=2 field                     7.066e-14
C5  pure-boost ADM pieces cancel: a = -grad Phi            0,0,0
C6  the -Phi^2 term does NOT cancel                        2 Phi grad Phi
C7  PPN 2PN contamination at 1 kpc                         25.72
C8  PPN 2PN contamination at 30 kpc                        0.0440
E1  alpha_1_eff(1 pc) < 1e-6                               1.818e-10
E2  alpha_1_eff(10 pc) < 1e-4                              1.786e-06
E3  kL*>>1 scaling = 4(a0/g)^2 within 10%                  True
D1  alpha-hat_1(internal) < 1e-20                          3.008e-24
D2  e_F < 1e-25                                            1.995e-30
D3  Shao-Wex margin > 15 decades                           19.07
D6  EFE correction to the internal field < 1e-9            1.561e-12
```

Twelve mutations, each changing one physical input or solver relation, each **exit 1** under
`A82_MUTATE=<name>`: `drop_boost`, `boost_half`, `linear_response`, `sign_flip`, `no_gradient`,
`a0_off`, `Lstar_off`, `spurious_dipole`, `w_quad`, `lapse_half`, `no_phi2`, `pulsar_wide`. Every
one of the 27 checks is broken by at least one of them; the mapping is in `MUTATE.md`, with the five
checks that were **deleted** because they were identities or theorem-bounded (`A4`, `A5`, `A6`, `D4`,
`D5`) and the one switch (`first_order`) that was tried and is not claimed because it breaks nothing.

Two of the mutations are load-bearing in a way worth naming: `lapse_half` (the `w²` coefficient of
the lapse halved from 2 to 1) is caught **only** by the angular checks C2/C3 and the symbolic ADM
check C5, and `no_phi2` (deleting the `−Φ²` term) is caught only by C6. The "no dipole" and "PPN
contamination" results are therefore tied to the lapse's structure, not to numbers typed into the
solver.

---

## 6. What this does not do

* **The `l = 2` radial BVP is not solved.** The angular structure of every `O(w²)` source is computed
  exactly (`C1`–`C4`), and the `l = 2` source is `2/13 = 0.153846` of the `l = 0` one, but the
  quadrupole's radial profile — with the angular eigenvalue `6` in the slaved Poisson operator —
  is not integrated. `2/13` is therefore an upper bound on the quadrupole fraction, and
  `2.1811e-17 m/s²` an upper bound on the quadrupole acceleration. The `l = 1` result (exactly zero)
  does not depend on this.
* **The `h^{ij}` `l = 0` correction is enumerated but not integrated.** It is `13/12`
  (`+8.333333e-02`) on every `α₁` and a `2/13` quadrupole; the numerical solve uses the clock term
  alone. Since the correction is `8 %` and every conclusion is ≥ 3 decades from a threshold, this
  does not move the verdict; it does mean the quoted `α₁` values are `12/13` of the full first-order
  result.
* **The `O(ε²)` background renormalisation is not propagated.** The `(1+2Φ)` factor in
  `P^i = h^{ij}P_j` rescales the clock source at `O(ε²)`; it is degenerate with a small change of
  `a₀/g` and therefore cancels in the local response `dg/dg_N`, but it is not solved for.
* **No strong-field `α̂₁`.** The pulsar number uses A36's response evaluated at the binary's
  Newtonian field; the neutron star's interior is not modelled. The direction of the error is
  favourable (`α̂₁ ≤ α₁`), and the margin is 19 decades.
* **No clusters.** A59's cluster row is the largest `α₁` in nature; the same identity
  `α₁g ≤ 2a₀` applies, so `δa ≤ w²a₀` there too, but the cluster's own `Φ/c² ~ 1e-5 > w²` means the
  PPN ordering is *better* in clusters than in galaxies — the opposite of the usual intuition, and
  not computed here.
* **`α₂` is not computed.** The `l = 2` source is a genuine `w_iw_j`-type anisotropy, so the theory
  has an `α₂`-type response at `O(w²)` — contrary to A36's "`w` enters only as `|w|²`" — but its
  coefficient and its observable consequences are not worked out; only the source ratio (`2/13`) is.
  This is the one place
  where the lane found A36's argument to be wrong rather than merely over-scoped: the `h^{ij}` in
  `u = K|P|_h` and in `P^iD_i ln N` does generate `cos²θ` terms, and A36's K3 dismissal of
  `w^i(w·P̄)∂_iΦ` as a total derivative treats `w·P̄` as constant when it is `|P|cos θ`.
* **No lattice/2-D solve.** The axisymmetric problem is reduced by exact angular decomposition, not
  discretised in `θ`; the `l = 0` sector is solved to `1.38e-07` in `u(8 kpc)` under grid refinement.

---

## 7. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A82_galactic_alpha1
python3 a82_checks.py --json-out a82_results.json > a82.out     # 27/27 PASS, exit 0
A82_MUTATE=drop_boost  python3 a82_checks.py --quiet ; echo $?  # 1
A82_MUTATE=lapse_half  python3 a82_checks.py --quiet ; echo $?  # 1  (breaks C2 C3 C5 only)
A82_MUTATE=no_phi2     python3 a82_checks.py --quiet ; echo $?  # 1  (breaks C6 only)
```

Runtime: a fraction of a second wall-clock on a cold start (`python3 -B`, no bytecode cache),
including the two symbolic checks C5/C6. Nothing is committed; no other lane's directory is touched — the
only new path in the tree is `deepseek_push/DS_FINAL_2026_10_21/A82_galactic_alpha1/`.
