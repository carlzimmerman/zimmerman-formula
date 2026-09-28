# AS063 — Identifiability of n and a per-channel slope: derivation

Run: `AS063-r1-20260928T085116Z-dsv4f-hermes`
Seed: `deepseek_push/astra_spawn_ideas/AS063_identifiability_of_n_and_a_per_channel_slope.md`
(sha256 `6171545ff62490322db37b73e04c169671db33259a3173684dff0104e9b9bc57`, verified at start and unchanged since)
Frame: `FRAMEWORK_CONTRACT.md` + `RESULT_CONTRACT.json`; sources PD01, PD08, k01 havehes match the seed pins and `SOURCE_MANIFEST.json` (37e39d1a…, 83f6054c…, 8df5a3ab…).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Named claim (the seed's principal test).** For the conditional MU_n statistical
response family

```
mu(n,lam,Y) := 1 - (1 + lam*Y)^(-n),        n ∈ ℕ, n ≥ 1,  lam > 0 dimensionless,  Y = g/s,
s := c*sqrt(G*rho_Lambda)  (> 0, the vacuum's own acceleration scale),
```

the **deep slope at the origin is the product n·lam** — the channel count times the
per-channel slope — and a spherical deep matching fixes **kappa = a0/s = 1/(n·lam)**:
deep observables determine the product only. The pair (n, lam) is not individually
identifiable from deep data; the transition-shape observable |c2|/c1^2 = (n+1)/(2n)
is lambda-free and would separate the two (an identifiability criterion, not a claim
that current data measure it).

**Symbol dictionary.**

| symbol | meaning | status |
|---|---|---|
| `a0` | `kappa * c * sqrt(G rho_Lambda)`, kappa = 1/2 | framework input (adopted) |
| `G` | 6.67430e-11 m^3 kg^-1 s^-2 | numerics convention |
| `c` | 299792458 m/s | numerics convention |
| `rho_Lambda` | mass density = 4 a0^2/(G c^2) (kg/m^3) | framework cell identity |
| `s` | c sqrt(G rho_Lambda) = 2 a0 on the canonical adopted footing | derived on a0-line |
| `Y` | g/s, dimensionless radial acceleration | boundary: Y ∈ ℝ⁺ (deep = Y≪1, Newtonian = Y≫1) |
| `n` | channel count, ℕ, n ≥ 1 | parameter to be identified |
| `lam` | per-channel deep slope, ℝ, 0 < lam | parameter to be identified |
| `B` | Newtonian (baryonic) acceleration g_N | framework |
| `mu` | `1-(1+lam*Y)^(-n)` | the declared conditional response |
| `p_lam` | per-channel engagement `1-(1+lam*Y)^(-1)` | PD01 A2, lambda-generalised |
| `c1, c2` | Taylor coefficients of mu at Y=0 (c1=deep slope, c2=curvature) | derived |
| `kappa` | a0/s | deep matching coefficient; 1/2 **adopted** elsewhere, derived here as 1/(n·lam) in the MU_n deep cell |

**Boundary conditions / domain.** Y = 0: mu = 0, mu' = n·lam (deep regime start);
Y → +∞: mu → 1 (Newtonian recovery), tail (1+lam·Y)^(-n); the response is defined
for all Y ∈ ℝ and is monotone on ℝ⁺ for n ≥ 1, lam > 0.

**Assumptions.** (i) The response family has the exact power-law form with a single
per-channel slope lam per channel (the seed's declared cell). (ii) All channels share
the same per-channel slope. (iii) Deep regime = first-order Taylor domination at
Y ≪ 1/(n·lam). (iv) kappa = 1/2 is ADOPTED as the framework normalization for the
canonical footing; the alternative footing is carried separately (Section 8).
No observational preference is used as proof (A7 tests exactly this).

**Framework inputs vs conclusions.** Inputs: G, c, a0 (with kappa=1/2), the family
shape and Yg = g/s relation, n≥1, lam>0. Conclusions: c1 = n·lam; c2 = -n(n+1)lam^2/2;
|c2|/c1^2 = (n+1)/(2n); OR-composition identity; spherical matching a0 = s/(n·lam),
i.e. kappa = 1/(n·lam) within this cell; limits and tails; identifiability rank.

---

## 2. Jacobian of the deep observables; rank; which observable breaks the degeneracy

Deep observables (leading order in Y, Y ≪ 1): slope c1 = n·lam; any deep
scale is a function of c1 alone (e.g. v_flat^4 = G·M_b·a0 with a0 = s·kappa and
kappa = 1/c1 within the cell). Take the map F : (n, lam) ↦ (n·lam) — the deep
covariant. Its Jacobian:

```
J1 = d(n·lam)/d(n,lam) = [ lam , n ],   rank(J1) = 1,
nullspace: (dn, dlam) ∝ (-n/lam, 1)   (J1·(-n/lam, 1)ᵀ = 0): the direction that
changes n and lam while keeping the product n·lam fixed leaves every deep observable
invariant.
```

Adding the second-order shape coefficient |c2| (transition curvature), the map
F2 : (n, lam) ↦ (n·lam, |c2|) has

```
J2 = [ lam,            n           ]
     [ lam^2·n/2 + lam^2·(n+1)/2 ,  lam·n·(n+1) ]        det J2 = n·lam^2/2 > 0,
rank(J2) = 2.
```

**Statement.** Deep data identify the product P = n·lam only (rank 1; the kernel
direction (n, −lam)-scaled preserves P). A transition-shape observable — the
lambda-free ratio |c2|/c1^2 = (n+1)/(2n) — would restore rank 2 and separate n
from lam in principle. **Nothing here claims current observations deliver that
shape observable; C3 only demonstrates the criterion is mathematically finite**
(pairwise separations at the 1e-1 level in mu(1), mu'(1) for the diagnostic
triples; orders above the deep ambiguity level).

---

## 3. Intermediate algebra with all scale factors, signs, units

### 3.1 Taylor expansion of the family (Y → 0, exact binomial for ℕ-power form first)

The family with exponent −n is `(1+lam·Y)^(-n) = ((1+lam·Y)^n)^(-1)` for all Y such
that 1+lam·Y ≠ 0 (true on ℝ⁺; Lean side uses the integer-power identity
`zpow_neg` + `zpow_natCast`, total). Expansion:

```
(1 + lam·Y)^(-n) = sum_{k=0}^∞ binom(-n, k) (lam·Y)^k,  |lam·Y| < 1
mu(Y) = -[ binom(-n,1) lam Y + binom(-n,2) lam^2 Y^2 + binom(-n,3) lam^3 Y^3 + ... ]
binom(-n,1) = -n,  binom(-n,2) = n(n+1)/2,  binom(-n,3) = -n(n+1)(n+2)/6

=> c1 := mu'(0)  = n·lam                                (deep slope = PRODUCT)
   c2 := mu''(0)/2 = -n(n+1)·lam^2/2                    (sign: negative, concave onset)
   |c2|/c1^2 = [n(n+1)lam^2/2] / (n·lam)^2 = (n+1)/(2n)   (lambda-free!)
```

Units: Y = g/s is dimensionless, so lam and n·lam are dimensionless; the
physical acceleration slope is ds/dY = c1·s = (n·lam)·c·sqrt(G·rho_Lambda),
units m/s² per unit dimensionless Y.

### 3.2 OR composition (PD01 A2, lambda-generalised)

Per-channel engagement p_lam(Y) = 1 − (1+lam·Y)^(−1). OR composition over n equal
channels: 1 − (1 − p_lam(Y))^n. Since 1 − p_lam(Y) = (1+lam·Y)^(−1),

```
1 - (1 - p_lam(Y))^n = 1 - ((1+lam·Y)^(-1))^n = 1 - (1+lam·Y)^(-n) = mu(n,lam,Y).   [exact]
```

so the family is exactly the OR over n equal channels with per-channel slope lam;
p_lam(0) = 0, p_lam'(0) = lam, p_lam(∞) = 1 (all exact; Lean T1/T8; A2 numerics).

### 3.3 Deep slope by the chain rule (all signs)

d/dY (1+lam·Y)^(-n): exponent rule gives (1+lam·Y)^(-n-1) · (-n) · lam;
at Y=0: (-n)·1·lam; d/dY [1 − (…)] flips the sign:

```
mu'(0) = -[(-n)·lam] = n·lam.     (A1: mu'(0)=lam·n; the per-channel deep slope is lam,
                                    the composed slope is the product n·lam.)
```

Completion robustness (A3): for ANY completion p with p(0)=0, p'(0)=lam, the OR
composition 1−(1−p)^n has slope n·lam — verified symbolically for
p ∈ {lam·Y/(1+lam·Y), 1−exp(−lam·Y), tanh(lam·Y)}, n ∈ {1,2,3},
lam ∈ {1/2, 1, 2} (27 triples, exact sympy limits; all equal n·lam).

### 3.4 Spherical deep matching — all scale factors (A5)

Deep regime of the spherically symmetric Poisson problem with the conditional
response: the integrated deep relation is g·mu(g/s) = B (a0-line algebra), and in
the deep regime mu ≈ (n·lam)·Y = (n·lam)·g/s so

```
g·(n·lam·g/s) = B    =>   g^2 = (s/(n·lam))·B  =  a0·B   with a0 := s/(n·lam).
```

Therefore **kappa := a0/s = 1/(n·lam)** within this cell. With the framework
identity s = c·sqrt(G·rho_Lambda) and rho_Lambda = 4 a0^2/(G c^2): s = 2 a0 and the
canonical deep cell has n·lam = 2 (A8, both footings below). Equivalently
v_flat^4 = G·M_b·a0 = G·M_b·s/(n·lam). Verbatim residual (B3): max
|g^2/(a0·g_N) − 1| = 1.414e-7 at B/s = 1e-14 in the actual first-integral
quadrature ladder.

### 3.5 Limiting regimes with leading neglected terms

**Deep limit** (Y ≪ 1/(n·lam)):
```
mu(Y) = n·lam·Y  [ 1 - (n+1)·lam·Y/2 + O((n+1)(n+2) lam^2 Y^2 /6) ]
mu/(n·lam·Y) - 1  =  -(n+1)lam Y/2 + O(lam^2 Y^2);   leading neglected term:  from c2
(B1 ladder at Y=1e-14: max |mu/(n lam Y) − 1| = 1.250e-14; remainder/c2·Y^2 → 1 to
within 1e-4 at Y=1e-10, confirming the Taylor bound).
```

**Newtonian limit** (Y ≫ 1/(n·lam)): mu → 1 with tail
```
1 - mu(Y) = (1+lam·Y)^(-n) ~ (lam·Y)^(-n) [ 1 - n/(lam·Y) + O((lam·Y)^(-2)) ]
(B2 ladder: |g/B − 1| = 5.000e-19 at B/s=1e18; log-tail slopes -4.000000000002246,
-2.000, -1.000 vs exact -n ∈ {-4,-2,-1}).
```

Both limits are certified for all n ≥ 1, lam > 0 (Lean T7, T8); finite ladders only
confirm to 80-digit precision — D1 records that distinction explicitly.

---

## 4. Independent checks (different representations), with actual residuals

| check | representation | result |
|---|---|---|
| A1–A8 | exact symbolic (sympy) — slopes, endpoints, OR identity, Taylor coefficients, ratio, spherical matching, Jacobian ranks, footings algebra | 8/8 exact |
| B1–B3 | mpmath 80-digit ladders — deep limit residuals, Newtonian tail slopes, a0-line in the integrated first integral | residuals 1.25e-14 / 5.0e-19 / 1.41e-7, tail exponents match −n |
| C1–C3 | least-squares reconstruction + transition-shape separation | see §5, §6 |
| Lean 4 | formal proof (independent representation: no floating point) | 8 theorems, axioms ⊆ {propext, Classical.choice, Quot.sound}, zero sorry (Section 9) |

All finite checks recorded actual residuals (never a Boolean alone); the exact
identities (A1–A8, Lean T1–T8) are symbolic/formal.

---

## 5. Negative control (must be capable of failing) — executed, and it fails as required

**Control C1 (fit n from deep data alone while fixing lam silently).** Generate
deep-window data of the family with n=4, lam=1/2 (product 2); fit n with lam fixed
silently at each of 1/2, 1, 2. Result: n_hat = [4, 2, 1] — **every** choice of lam
fits the same deep data, with RMS 4.2e-5 / 0.0 / 8.5e-5, and n_hat·lam = 2.0 in all
three cells. The conditional assumption thereby identified: **lam = 1 was silently
imposed** (the "one-scale fraction" identification); deep data contain no information
to lift it. This is the identifiability failure of n from deep data.

**The control is capable of failing (C2).** Repeat the fit on a **non-deep** window:
the truth (n=2, lam=1) achieves RMS = 0.000e+00, while wrong lambda choices
(n_hat=4 and 1) give RMS 0.0289 and 0.0545 — i.e. outside the deep regime the fit
correctly rejects wrong lam, so the C1 ambiguity is not an artifact of the fitting
machinery. The deep degeneracy is intrinsic to the regime (Jacobian rank 1, §2).

**Newtonian/deep regime control (B1/B2).** Both limits exist and were checked with
their leading corrections; the exact one-sided limits are certified in Lean T7.

---

## 6. Strongest surviving statement

For the declared conditional MU_n cell (family `1-(1+lam·Y)^(-n)`, Y = g/s,
s = c·sqrt(G·rho_Lambda), n ≥ 1, lam > 0, kappa = 1/2 adopted input):

1. mu'(0) = **n·lam** (product; Lean T2; A1; A3 completion-independent).
2. The family is the OR of n equal per-channel engagements of slope lam
   (Lean T1; A2).
3. Spherical deep matching gives a0 = s/(n·lam), hence kappa = 1/(n·lam)
   within the cell: **deep data fix the product n·lam alone** (Lean T3; A5; B3).
4. The normalized transition curvature |c2|/c1^2 = (n+1)/(2n) is **lambda-free**
   (Lean T4; A4) and the map n ↦ (n+1)/(2n) is injective (Lean T5): among
   equal-product configurations, equal curvature forces n = n' (Lean T6).
5. mu → 1 at Y → +∞ with n-dependent tail (Lean T7); per-channel saturation
   p_lam → 1 (Lean T8).

**Domain of the statements:** all n, n' ≥ 1 (Nat), lam, lam' > 0, s > 0, Y ∈ ℝ;
exact (formal) for the identities; 80-digit finite confirmation for the ladders.

**First additional implication needed to transfer to the full theory:** a
measurement or model of the transition-shape observable (|c2|/c1^2 or an
equivalent curvature) that pins (n+1)/(2n) — plus the identification of the
per-channel engagement mechanism of PD01 from dynamics, not from the adopted
normalization (k01's lambda-free-vacuum premises remain the open coupling side).
Without the shape observable, any statement "n = 2 channels at lam = 1" remains
an adopted choice, indistinguishable from (4, 1/2), (1, 2), … (A7).

---

## 7. Why kappa = 1/2 stays adopted here, and what would remove it

The 1/2 normalization is a framework input (contract). What this task's cell
produces is the **relative** statement kappa = 1/(n·lam): an independent sphere
argument (e.g. a physical per-channel matching that fixes lam, or a mechanism that
fixes n) would remove one degree and then pin kappa absolutely. No such argument
is invented here; the identifiability gap (n vs lam) is itself a missing premise of
the kappa derivation — exactly the audit's target.

---

## 8. Both footings carried separately (A8; contract 2)

The identifiability theorem is dimensionless and applies identically to both
footings; the deep cell product changes with the footing choice:

| cell | input | result |
|---|---|---|
| canonical | a0 = 9.3619e-11 m/s², kappa = 1/2 adopted, rho_L = 4a0²/(Gc²) | s = 2a0; deep product n·lam = 2 (e.g. n=2, lam=1) |
| alternative, rho_L fixed | a0 = 1.1279e-10 m/s² with the SAME rho_Lambda (kappa no longer 1/2) | kappa_eff = 0.602388; product n·lam = 1/kappa_eff = 1.660059 |
| alternative, kappa fixed = 1/2 | a0 = 1.1279e-10 m/s² with kappa = 1/2 (density changed) | rho_Lambda(alt) = 8.483090e-27 kg/m³; product n·lam = 2 again |

Canonical s == 2a0 checked to <1e-12 relative; in every cell deep data fix only the
product — the identifiability statement is footing-independent.

---

## 9. Lean 4 certificate (formal, independent representation)

File: `AS063_certificate.lean` (self-contained, imports Mathlib).
Command: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS063_certificate.lean`
→ exit 0; then axiom probe `raw_outputs/AS063_axioms.lean` → exit 0 with:

| theorem | content |
|---|---|
| as063_or_composition | (1 − p_lam)^n = (1+lam·Y)^(−(n:ℤ)) — OR identity, all Y |
| as063_deep_slope | HasDerivAt (fun Y => mu n lam Y) (n·lam) 0 — the product slope |
| as063_kappa_of_product | s/(n·lam)/s = 1/(n·lam) — kappa depends on product |
| as063_curvature_lambda_free | 2·n·kappaCoef = (n+1)·slope² — lambda-free ratio |
| as063_shape_ratio_injective | (n+1)/n = (n'+1)/n' ⇒ n = n' |
| as063_curvature_separates | slope·slope′ = product and equal curvature ⇒ n = n′ |
| as063_newtonian_recovery | Tendsto (fun Y => mu n lam Y) atTop (𝓝 1), n ≥ 1, lam > 0 |
| as063_per_channel_saturates | p_lam → 1 at +∞ |

Axioms: every theorem: `[propext, Classical.choice, Quot.sound]` only; **zero sorry**
(hard bar of the task met). The derivation used: zpow identities (T1), chain-rule
composition via HasDerivAt.pow + HasDerivAt.inv on the ℝ-embedded ℕ-power form and
the pointwise zpow equality (T2), field algebra (T3), ring algebra (T4), casts and
field/nlinarith (T5, T6), atTop composition machinery (T7, T8).

---

## 10. Branch discipline

Branches Q, RAR, MU2, EXP, MONO kept distinct throughout. This task's cell is the
**MU_n statistical response** (the MU2 branch family generalised to general n with
per-channel slope lam: `mu_n(Y)=1-(1+Y)^(-n)` with `Y=g/s`, `s=2a0` on the adopted
footing is MU2 at n=2; here the generalised cell has Y=g/s with lam·Y). No result
is imported from or transferred to Q/RAR/EXP/MONO; the causal criterion-B and the
filtered-MONO operative target are untouched (no claim about the operative gate is
made). The a0-line used for spherical matching is the framework identity, handled
symbolically.

## 11. Limitations (explicit)

- The family shape and single per-channel slope are assumed (the seed's declared
  cell); the result does not derive the response from an action.
- kappa = 1/2 remains adopted; this task proves only kappa = 1/(n·lam) within MU_n.
- Deep data alone cannot separate n and lam — that is the main negative finding;
  the shape criterion is mathematical, not an empirical measurement.
- Finite ladders confirm, they do not prove; the proofs are the Lean certificates
  and the symbolic identities.
- Criterion-B/operative-gate consequences are untouched by design.