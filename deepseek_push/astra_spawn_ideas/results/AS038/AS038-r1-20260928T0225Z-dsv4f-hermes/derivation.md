# AS038 — Recover an AQUAL energy primitive

Run: `AS038-r1-20260928T0225Z-dsv4f-hermes`
Worker: deepseek/deepseek-v4-flash-0731 (provider: openrouter), Hermes Agent focused subagent (delegate `sa-7-c46835ee`).
Audited cell per task step 2: **MU2**. Comparison cells: **Q** (closed form), historical **EXP** (closed form), **RAR** (numeric quadrature), operative **MONO** (comparison only; the operative filtered-MONO target is NOT concluded on — the heat filter S is not exercised).

---

## 1. Claim, symbols, boundaries, assumptions (task step 1)

**Claim (dimensionless, scale-free in a0).** Let `X = |grad Phi|^2 / a0^2` and let the AQUAL-type action density be

```
L = (a0^2 / 8 pi G) F(X) + rho_b Phi,      F'(X) = mu(sqrt X),     F(0) = 0,
```

with `x = g/a0 = |grad Phi|/a0` and `y = B/a0 = g_bar/a0` (B = standard Newtonian acceleration). Then the Euler–Lagrange variation reproduces the declared branch field equation

```
div( mu(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b            (EXP form, all branches),
```

for each branch kernel μ listed below, **provided F is the primitive (energy density scale) defined by the branch response**:

```
F(X) = integral_0^X mu(sqrt t) dt,   equivalently  P(x) = F(x^2),  P'(x) = 2 x mu(x) = 2 y(x).
```

The recovered primitive for the audited MU2 cell is closed form:

```
F_2(X) = X - 8 ln(1 + sqrt(X)/2) - 16/(sqrt(X) + 2) + 8,          F_2(0) = 0,
mu2(x) = 1 - (1 + x/2)^(-2),   response  y = x mu2(x)  (implicit algebraic: (x-y)(x+2)^2 = 4x).
```

Boundaries: `x >= 0` (g >= 0), `y > 0`, `X >= 0`; F(0) = 0 pins the additive constant (no field -> no energy). Assumptions: the branch kernels of the framework contract (§Branch dictionary), `kappa = 1/2` ADOPTED framework input (not derived), `G = 6.67430e-11 SI`, `c = 299792458 m/s`, `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`; `G_N = G_bare = G_cosmo = G` separation not needed: every identity here is homogeneous in G-free dimensionless variables and the dimensional examples carry only the explicit a0 footings.

## 2. Variation with the source sign (task steps 2–3)

Vary `Phi -> Phi + eta` with eta compactly supported. With `X = a0^{-2} |grad Phi|^2`:

```
delta L = (a0^2/8 pi G) F'(X) delta X + rho_b delta Phi
delta X = a0^{-2} * 2 grad Phi . grad eta
```

so stationarity gives (integration by parts)

```
-(1/(4 pi G)) div( F'(X) grad Phi ) + rho_b = 0   ==>   div( mu(|grad Phi|/a0) grad Phi ) = 4 pi G rho_b,
```

using F'(X) = μ(√X) = μ(x). **The source term is +4πG rho_b on the right** (attractive gravity for rho_b > 0) — the sign follows from the +rho_b Phi coupling; a `-rho_b Phi` convention would flip BOTH the field equation and the energy sign (section 5) coherently.

**Scale factors:** `a0^2/(8 pi G)` carries units `(m^2 s^-2)/(m^3 kg^-1 s^-2) = kg m^-3`... in SI: a0²/(8πG) = 5.224953290932738e-12 J·? (kg/m³) — evaluated dimensionally: [a0²]/[G] = (m²/s⁴)/(m³/kg/s²) = kg/(m·s²) = J/m³ ✓ so (a0²/8πG)·F(X) is an energy density; F(X) is dimensionless in X. The factor 1/2 in the standard AQUAL normalization is absorbed: the contract's comparison branch EXP uses `mu = 1 - e^{-x}` with exactly this 4πG normalization; the framework's kappa = 1/2 enters only through a0's definition, never through the field equation's 4πG (that is the EXP/AQUAL normalization itself, adopted as the branch convention).

## 3. The five branch kernels and their primitives

For every branch, `mu(x)` is the constitutive kernel; the response `y = x mu(x)` must equal `B/a0`; `x(y)` inverts it.

### 3.1 Q (algebraic a0 line): `g^2 = B^2 + a0 B`
`mu_Q(x) = y/x` with exact inverse `y_Q(x) = (sqrt(1+4x^2)-1)/2`, `y_Q^2 + y_Q = x^2` (Lean-certified). Primitive:

```
P_Q(x) = (x/2) sqrt(1+4x^2) + asinh(2x)/4 - x,   P_Q'(x) = sqrt(1+4x^2) - 1 = 2 y_Q(x).
```

### 3.2 MU2 (audited cell): `mu2(x) = 1 - (1 + x/2)^(-2)`, `y = x mu2(x)`
Integration (step 2). With s = x:

```
P2'(x) = 2x mu2(x) = 2x - 8x/(x+2)^2           [note -8/(x+2) + 16/(x+2)^2 = -8x/(x+2)^2]
P2(x)  = x^2 - 8 ln(1 + x/2) - 16/(x+2) + C.
```

Additive constant: `P2(0) = 0 - 8 ln 1 - 8 + C = C - 8`, so the pin F(0)=0 forces **C = +8** (the closed form in §1). Additive shift is the zero mode of the field equation: P2 and P2−8 give identical Euler chains (NC2 measured |P2'(1) − (P2−8)'(1)| = 0 at 80 dps); only the energy density carries the constant. The implicit response relation is algebraic: `(x − y)(x+2)^2 = 4x` (Lean-certified). Root inversion on the physical domain: bisection of x·μ2(x) − y (brackets verified: f(x_lo) < 0 < f(x_hi), μ2 increasing).

### 3.3 EXP (historical exact AQUAL, comparison): `mu_EXP(x) = 1 - e^{-x}`
```
P_exp(x) = x^2 - 2 + 2(1+x) e^{-x},   P_exp(0) = 0,   P_exp'(x) = 2x(1-e^{-x}) = 2y.
```

### 3.4 RAR: `nu_RAR(y) = 1/(1 - exp(-sqrt y))`, `x = y nu_RAR(y)`, `mu_RAR(x) = y(x)/x`
No closed form; primitive by y-domain quadrature:

```
F(y) = 2 integral_0^y s x'(s) ds,   x'(s) = 1/(1-q) - s q/(2 sqrt(s) (1-q)^2),  q = e^{-sqrt s}.
```

### 3.5 MONO (operative splice, comparison only): h'_mono = max(h'_RAR, delta h_p/(y+y_p))
Contract splice with δ = 0.05; landmarks **solved** here (not rounded): y_p = 2.539638282 (h_p = 0.647610238, h_RAR peak: root of h'_RAR), y* = 2.337412405 (root of h'_RAR(y) = δ h_p/(y+y_p); crossing residual 5.9e-122 on the 400-iteration bisection). Continuation h_mono(y) = h_RAR(y*) + δ h_p ln((y+y_p)/(y*+y_p)); F_mono from the same quadrature with integrand 2s(1 + δ h_p/(s+y_p)) on s > y*. MONO ≡ RAR below y*. The operative filtered-MONO target (heat filter S = exp((ξ²/2)Δ)) is NOT exercised — see limitations.

## 4. Domain, convexity, and the energy density sign

F is defined for all X ≥ 0 on every branch. Strict convexity (ellipticity of the field equation): F''(X) = μ'(x)/(2x), equivalently the parallel eigenvalue λ_∥ = μ + x μ' = dy/dx:

- Q: 2x/√(1+4x²) > 0; MU2: 1 − 4/(x+2)² + 8x/(x+2)³ > 0; EXP: (1+x)e^{-x} > 0 — each strictly positive (exact).
- RAR: dμ/dy = (h − y h')/(y+h)² > 0 ⟺ h/y decreasing — proven monotone involution; numerically min λ_RAR = 5.68e-4348 (at y=1e8, mpf; float would underflow — kept as mpf by design).
- MONO: min λ = 1.159e-16 > 0 on the grid (C¹ splice; positive by the max-continuation construction).

Energy density of the static field Hamiltonian:

```
eps_Phi = -(a0^2/8 pi G) F(X)   (< 0 for all X > 0 on every branch; = 0 at X = 0)
W(X) = 2X F'(X) - F(X)  >= 0    (k-essence superpotential; W = 4x y/... in x variables: W = 2x^2 mu - F)
```

The sign: the kinetic term (a0²/8πG)F(X) enters the Hamiltonian as +L_kin in L = L_kin − rho_b Φ... for the static configuration the Hamiltonian density is −L_kin (phantom-type negative-energy density of the scalar field, the standard AQUAL/MOND scalar phenomenology — the total galactic Hamiltonian is not the point of this cell). Physics statement recorded, not a global-energy theorem.

## 5. Regimes (leading neglected terms)

Deep (x → 0): F → (2/3)X^{3/2} with branch-specific leading corrections at y=1e-10 (grid x ≈ 1.000e-5), measured F/((2/3)X^{3/2}) − 1: Q −6.00e-11 (∝ x²), MU2 −5.625e-06 (∝ x²), EXP −3.750e-06 (∝ x²), RAR −7.500e-06 (∝ x), MONO −7.500e-06 (RAR/MONO identical below y*; approach RATES are branch-specific — matching one asymptote is not matching the law). Deep equality of the (2/3)X^{3/2} asymptote is NOT branch identity — finite-y primitives differ (NC5): at y = 0.1: F_Q = 2.2926e-2, F_MU2 = 2.5237e-2, F_EXP = 2.3889e-2, F_RAR = F_MONO = 2.6397e-2; ratios F_Q/F_MU2 = 0.90843, F_EXP/F_MU2 = 0.94656, F_RAR/F_MU2 = 1.04603.

Newtonian tail (F − X at the largest grid x, y=1e8): Q −1.0000e8 (−x exactly: F − X → −x); MU2 −134.94 (−8ln(x/2)+8-type log tail); EXP −2.0000 (exact: F = X − 2 once 2(1+x)e^{−x} → 0); RAR −26.00 (finite constant, −2∫₀^∞ h_RAR(s)ds = −25.98); MONO −2.3195e8 and → −∞ (the log splice makes h(y) ~ δh_p ln y grow, so x − y is unbounded and the tail is the slowest of the five — as the contract's splice construction implies).

## 6. Numerical protocol and controls (task step 4)

mpmath 80 dps, single thread, `signal.alarm(120)` enforced (observed 7.32 s wall, well inside the bound; memory bound 512 MB declared — RLIMIT_AS not enforceable on this macOS host, process trivially small; 1 thread enforced). Diagnostic grid y = 10^k, k = −10..8 step 0.1 (181 points), roots bisection-bracketed (400 iterations) — explicitly a finite diagnostic grid, not a proof (the Lean file is the proof layer).

Independent representation checks (all residuals saved, not booleans):

| check | object | observed | tolerance |
|---|---|---|---|
| CK1 | Q round trip |Q: max|yQ(x) − y| = 1.41e-73 | < 1e-70 |
| CK2 | Euler chains by direct differentiation, Q/MU2/EXP | max rel |P'(x) − 2xμ| = 1.9e-81 | < 1e-35 |
| CK2b | RAR/MONO: dF/dy vs 2y x'(y) (differentiating the quadrature primitive) | max 4.0e-81 | < 1e-30 |
| CK3 | RAR two representations: y-domain segment sums vs x-space inversion quadrature | max 3.53e-47 | < 1e-30 |
| CK4 | MONO splice continuity (h(y*) = continuation; crossing residual 5.9e-122); deviation from RAR max 0.0103228 dex at y = 15.8489 | PASS | ≤ 0.0104 dex claim |
| CK5 | F→0 at y=1e-60 per branch (Q 6.7e-91, MU2 0.0, EXP 2.1e-81, RAR/MONO 6.7e-91) | PASS | < 1e-50 |
| CK6 | knee x(1): Q √2 = 1.41421, MU2 1.48929, EXP 1.34998, RAR = MONO 1.58198 (distinct) | PASS | Q exact |
| CK7 | deep limit → (2/3)X^{3/2} with distinct approach rates (above) | PASS | < 1e-3 |
| CK8 | Newtonian tails (above) | PASS | recorded |
| CK9 | min μ > 0 (all branches 1.000e-05 at grid deep end) | PASS | > 0 |
| CK10 | min λ_∥ > 0 (Q/MU2/EXP 2.000e-05; RAR 5.68e-4348 mpf; MONO 1.159e-16) | PASS | > 0 |
| CK11 | min W = 1.333e-15 > 0 (deep W = (4/3)x³ + ...) | PASS | ≥ 0 |
| CK12 | energy sign: ε = −(a0²/8πG)F < 0 at all 7 selected X × 5 branches, both footings | PASS | < 0 |
| CK14 | dimensional: r_M(1e11 M_sun) = 12201.97 pc (canonical) / 11116.72 pc (alt.); ε at y=1 per branch −(5.4…6.6)e-12 (can) / −(7.9…9.6)e-12 (alt) J/m³ | PASS | recorded |
| CK15 | MONO C¹ splice: h'' jump at y*: −0.03611 (left) vs −0.001361 (right) — F'''(X)-type discontinuity as per the peer-review splice note | PASS | jump recorded |

Quadrature infrastructure (80 dps): composite Gauss–Legendre over log-spaced segments (60/decade, 24 nodes; first segment integrated in s = t² to remove the √s branch point at 0, verified against tanh-sinh to 1e-45+); Newton inversion (tolerance scaled to running dps) with bisection fallback; y-domain and x-space representations share only the segment skeleton and agree to 3.5e-47.

## 7. Negative controls (task step 5; all capable of failing and measured)

- **NC1 (mandated)**: differentiate w.r.t. x instead of X without the factor 2x. The naive primitive N(x) = ∫₀ˣ μ(s)ds has N'(x) = μ(x) EXACTLY; the correct chain needs P'(x) = 2xμ(x) = 2y. Residual |2y − N'|/|2y| = |2x−1|/(2x): measured max 0.8419 (MU2 and EXP; the numeric spot checks), → 1 deep (100% error), single accidental zero at x = 1/2. Wrong operator: div(μ grad Φ/x) = 8πG ρ_b; no spherical solution for y ≥ 1/2 (μ bounded < 1 can't equal 2y); deep "solution" x = 2y ⇒ Newtonian deep force — the deep g² = a0 B law is destroyed. FAILS as required.
- **NC2**: perturbed primitives rejected. Drop the log term: max Euler residual 21.47 (must fail); shifted constant: P2(0)−8 = −8 (normalization fails); zero mode: |P2'(1) − (P2−8)'(1)| = 0 (additive constant invisible to the field equation).
- **NC3**: W-identity dW/dx = 2x(μ + xμ') numerically over the whole grid (Q): max 6.72e-73 — a sign error in W would break this.
- **NC4**: float64 cancellation: F2(x=1e12) — float64 reports F − X = 0.0 (both F and X round to the same float64 grid; also float64(1e12)² = 1e24 − 2²⁴ exactly) while the 80-dps tail = −207.5029915. Grid-tail diagnostics MUST be mpf at ≥ 50 digits; float64 would falsely report a vanishing tail.
- **NC5**: branch fidelity: identical deep asymptotes do not make primitives equal (finite-y differences ~ −10%…+5%, §5).

## 8. Lean certificate

`AS038_aqual_primitive.lean` (Mathlib v4.34.0-rc2, `lake env lean`, exit 0, 5 theorems, **zero sorry**, axioms of all 5 ⊆ {propext, Classical.choice, Quot.sound} — verified by `#print axioms` in `AS038_aqual_primitive_axioms.lean`):

- `qbranch_response_identity (x) : yQ x^2 + yQ x = x^2` — the Q algebraic response identity restated exactly;
- `qbranch_yQ_at_zero : yQ 0 = 0` — physical boundary;
- `mu2_response_algebraic (x) (hx2 : x+2 ≠ 0) : (x − x·mu2(x))(x+2)² = 4x` — the audited branch's implicit response relation in algebraic form;
- `mu2_euler_chain (x) (hx : 0 < x) : deriv P2 x = 2·x·mu2(x)` — the AQUAL energy chain of the recovered primitive (the task's "2z f'(z) = μ(x) x relationship restated exactly");
- `P2_at_zero : P2 0 = 0` — additive constant pinned.

Transcendental branches (RAR/MONO quadrature primitives) stay in the Python lane; only the algebraic/closed-form cells are Lean-certified.

## 9. Dimensional examples — both footings, separately

a0 = 9.3619e-11 (canonical) and 1.1279e-10 m/s² (alternative). The result is dimensionless; SI maps: r_M(1e11 M☉) = 12.202 kpc / 11.117 kpc; ε scale a0²/(8πG) = 5.224953e-12 / 7.583953e-12 J/m³; ε(y=1) per branch: Q −5.997/ −8.705, MU2 −6.166/−8.950, EXP −5.439/−7.894, RAR = MONO −6.608/−9.592 (×1e-12 J/m³). Footing relation: a0_alt/a0_can = 1.2047768 ⇒ fixed-ρ effective κ = 0.60239 (of the adopted 1/2) or fixed-κ density ratio 1.4515 — never both fixed simultaneously.

## 10. Strongest surviving statement

On the declared separate branches (Q, RAR, MU2, historical EXP, operative MONO), the AQUAL primitive F(X) = ∫₀ˣ μ dt with F'(X) = μ(√X) and F(0) = 0 is:
- closed form for Q (asinh form), MU2 (log form, §1) and EXP (e^{-x} form);
- numerically recovered for RAR and MONO by quadrature, cross-checked in two independent representations to 3.5e-47 and against the analytic derivative to 4e-81;
- strictly convex (μ > 0, λ_∥ > 0) on all five branches over the full grid;
- energy sign ε = −(a0²/8πG)F < 0 with W ≥ 0 (k-essence superpotential);
- consistent with the exact Euler chain (MU2 Lean-certified) and with the deep F→(2/3)X^{3/2} and the branch-specific Newtonian tails (Q −x; EXP −2 exact; RAR −26.0; MU2 −8ln(x/2)+…; MONO −2δh_p·y·ln y → −∞).

The primary audited cell MU2 survives all controls.

## 11. Limitations

- Operative target NOT concluded: MONO here is the unfiltered contract splice; the filtered operand (heat filter S) and criterion-B causality are not exercised; a transfer needs the filter bridge (child AS038.C01).
- kappa = 1/2 remains adopted, not derived; the primitive is dimensionless in a0 and cannot remove the normalization freedom.
- ε < 0 is the field-sector energy density of the static Hamiltonian; no claim about total galactic Hamiltonian, stability, or the relativistic completion.
- Grid numbers are finite consistency evidence; exact identities are certified only for the algebraic/closed-form cells (Lean) — RAR/MONO recovery is numerical (80 dps, two-representation agreement 3.5e-47).
- No dynamics, no PPN, no lensing, no time evolution; static quasistatic scalar cell only.

## 12. First additional implication (transfer step)

For the operative filtered-MONO target one must compute how the recovered F_mono enters the filtered equation: the filter S commutes with the constitutive map only if the smoothing scale ξ and the kernel scale a0 factorize; otherwise the effective action is NOT of the recovered AQUAL form and the primitive must be re-derived inside the filtered dynamics. The child proposal quantifies the change.

## 13. Child proposals

- **AS038.C01** — "Filter bridge for the recovered primitive": derive the effective energy density of the filtered MONO equation (S = exp((ξ²/2)Δ), spherical sources) and the exact band of ε_eff/ε_mono over y ∈ (0, ∞) and ξ/a0 ∈ (0, 1]; controls: ξ → 0 recovers ε_mono (control capable of failing), deep limit (2/3)X^{3/2} preserved, Newtonian tail −2δh_p y ln y preserved, full-grid two-representation recheck; parent this run; NOT DISPATCHED (no spawn mechanism; ready spec for the orchestrator).
