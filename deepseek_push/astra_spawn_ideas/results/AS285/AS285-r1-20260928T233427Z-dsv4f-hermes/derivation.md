# AS285 — Action-consistent growth equation in a restricted quasistatic band

**Run:** `AS285-r1-20260928T233427Z-dsv4f-hermes`
**Seed sha256:** `b75303fd8d86509843b0a38ddeb2ee5710e887515f270634898963fdea5a1120` (verified before execution; not renamed or paraphrased).
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent.
**Branch:** CA5-GNC-R (host = FINAL_ACTION.md eq. (4) + R1 dark sector of AS127), **inactive branch**, restricted quasistatic band.
**Outcome:** supports_scoped_claim.

---

## 0. Sources and hashes

| source | sha256 (verified) |
|---|---|
| AS285 seed | `b75303fd…a1120` |
| FINAL_ACTION.md (CA4-GNC host = CA5-GNC-R host) | `b8c04d4e…b546e` |
| breakthrough_review occupied RESULT.md | `6091291f…75d5` |
| FRIED_CHICKEN_SPEC.md (amendment: filtered ν_mono, criterion B) | `98d9149f…8e3f` |
| FRAMEWORK_CONTRACT.md / RESULT_CONTRACT.json | `ca696c7f…ddf9` / `621fdad0…c1517` |
| STANDING.md | `660462eb…bf63` |
| SOURCE_MANIFEST.json | `fe295b80…7fba` |
| upstream: AS127 result.json (lapse density ρ_R = tK_d + W_exc/t + V₀F(t)) | `7a9bdf10…ba12` |
| upstream: AS147 result.json (U(1) current) | `27c07950…34c6` |
| upstream: AS080 result.json (hydrostatic slope) | `e5923a66…f0e1` |
| upstream: AS086 result.json (log-well virial) | `d6e0a79d…4019` |

Prerequisites listed in the seed — AS251, AS279 — have **no completed results** in
`results/` at run time; this is recorded as a dependency gap (the seed's own equations,
eqs. (6), (7), (13) of FINAL_ACTION, are used directly, so the gap does not block the
present band-scoped derivation).

---

## 1. Assignment, action cell, and scope of the claim

The seed asks for, in the stated order:

1. minimally coupled baryon perturbation source in lapse and spatial equations;
2. elimination of auxiliaries with the same source operator; derive both Φ and Ψ;
3. bounded growth equation from baryon continuity + Euler, with the discarded time-derivative error stated;
4. the relation `-q² Φ = 4πG_N μ_g(q,a) ρ_b δ_b`, `Ψ = η_g(q,a) Φ`, with every assumption, and the single downstream calculation enabled/blocked.

**Action cell (pinned):** CA5-GNC-R = CA4-GNC host (FINAL_ACTION.md eq. (4))
with the dark sector replaced by the AS127 reciprocal form
`L_d = t K_d − W_exc/t − V₀ F(t)`, `t = 1+Z−⟨Z⟩_h`, `F = 1+(t+1/t−2)²`,
`K_d = ½Σ_A n(φ_A)²`, `W_exc = ½Σ_A|Dφ_A|²+V_mix`. Host constants:
`0<α<2`, `c_N = 1−α/2`, `c₂>0`, `ξ>0`, `0<ℓ<4`, `θ>0`, `δ=0.05`, `M_P² = 1/(8πG_bare)`,
`G_N = G_bare/c_N` (derived in FINAL_ACTION §5), `G_cosm/G_N = c_N` (eq. (18)).
Branch dictionary: only the **inactive branch** (f = G′ = G = 0, i.e. Y_h = −θ) is
exercised; Q/RAR/MU2/EXP/MONO kernels are NOT exercised (no gate crossing). The
operative filtered-MONO target and criterion B are NOT concluded on; the result is a
scoped input to the cosmological-perturbation gate (requirement 8 of the amended
thirteen).

**Domain.** Linear, ordinary, pressureless baryon perturbations about the homogeneous
vacuum background (carrier fields at the potential origin, φ_A = 0, so
`K_d = W_exc = 0`, `ρ_R0 = V₀` on the background, `F′(1) = 0`), Newtonian gauge
`ds² = −(1+2Φ)dt² + a²(1−2Ψ)δ_ij dx^i dx^j`, comoving wavenumber `q`,
**quasistatic band `q ≫ aH`** (numerically `10 ≤ q/(aH) ≤ 10³`), flat k = 0 leaves,
fixed host parameters. `κ = 1/2` adopted as input (framework contract).

---

## 2. Perturbation setup and the linearized constraint system

Background: homogeneous FRW leaf, `W_b = const`, `Y_h = −θ < 0`, `f = G = 0`,
`a = DZ = DU = 0`, `z = 0`, `Q_K = 0`; Friedmann eqs. (18). Lapse and shift of the
background: `N = 1+Φ` at linear order (since `g₀₀ = −(1+2Φ)` and `N = √(−g⁰⁰)⁻¹ · …`
gives `N = √(1+2Φ) ≈ 1+Φ`), `N^i = 0`. Hence the acceleration vector
`a_i = D_i ln N = D_i Φ`. For every Fourier mode with q ≠ 0 the sqrt(h)-means of first
order perturbations vanish, so `z = Z`, `⟨N ρ_R⟩_h = ρ_R0`, `Q_K = −3Ψ̇`, `A_K = ⟨N Q_K⟩_h = 0`.

**E1 — linearized lapse constraint** (FINAL_ACTION (13), inactive branch, quasistatic
band). Linear terms, in order of appearance in (13):

- `(M_P²/2) R⁽³⁾`: for `h_ij = a²(1−2Ψ)δ_ij`, `R⁽³⁾ = 4D²Ψ` (computed from
  `Γ^k_ij = −(Ψ_i δ_j^k + Ψ_j δ_i^k − Ψ_k δ_ij)`, `R_ij = Ψ_{ij}+ΔΨ δ_ij`, `R = 4ΔΨ`);
  Fourier: `4D²Ψ = −4k²Ψ`, with `k² = (q/a)²`.
- `−T_K`, `−2Λ`: `T_K = K_ijK^ij − K²`; linear part `+12HΨ̇` (from `K^i_j = (H−Ψ̇)δ^i_j`,
  `T_K = −6(H−Ψ̇)² = −6H² + 12HΨ̇`). **Discarded in the quasistatic band** (error budget §8).
  `Λ` sits in the background equation.
- `c₂[−Q_K² + 2KQ_K − 2KA_K/N]`: linear `2KQ_K = 2·3H·(−3Ψ̇) = −18HΨ̇`, `Q_K²`, `A_K` are
  second order/zero. **Discarded** with the Ψ̇ channel.
- `V_a − div_N[2α(a−DZ)+4DZ]`: `V_a = α|a−DZ|² + 4a·DZ − 2|DZ|² − 4c_NDZ·DU` is
  quadratic in first order fields ⇒ **zero at linear order**. The divergence term,
  linearized with `a = DΦ`: `−div_N[2α(a−DZ)+4DZ] = −[2α(D²Φ−D²Z) + 4D²Z]
  = −2αD²Φ + 2αD²Z − 4D²Z`; Fourier: `+2αk²Φ − 2αk²Z + 4k²Z`.
- `c_N[G(Y_h) − ℓΔ_hW_b]`: `G = 0` (inactive); `W_b = S_h U`, `Δ_hW_b → −k²S_k U`
  with `S_k = exp(−(ξ²/2)(q/a)²)` (heat-kernel factor, `b = ξ²/2`, physical Laplacian
  on the mode); term: `+ c_N ℓ k² S_k U`.
- RHS: baryon density perturbation `ρ_b0 δ_b` (minimally coupled, `S_b[g]`) plus the
  dark-sector density perturbation `δρ_R = 0` on the vacuum carrier origin (carriers
  decouple at linear order: every linear source term is ∝ background φ_A or ∂φ_A = 0;
  and `δρ_R = F′(1)V₀δz + … = 0` because `F′(1) = 0` — see §3).

```text
E1:  (M_P^2/2) { -4k^2 Psi + 2α k^2 Phi - 2α k^2 Z + 4k^2 Z + c_N ℓ k^2 S_k U } = ρ_b0 δ_b
```

**E2 — Z auxiliary** (FINAL_ACTION (6), f = 0, `a = DΦ`, measure terms first order):
`4Δ_N Z = S†[div_N(ℓa)]` ⇒ `4D²Z = ℓ S_k D²Φ` ⇒ Fourier:
```text
E2:  -4k^2 Z + ℓ S_k k^2 Phi = 0        ⟹   Z = (ℓ/4) S_k Phi
```

**E3 — Z/U–projection constraint** (FINAL_ACTION (7) with ρ_R):
`2M_P²c_N div_N(DZ − a + DU) + ρ_R − ⟨Nρ_R⟩_h/N = 0`. Linear: `div_N(…) = D²(Z−Φ+U)`;
`ρ_R − ⟨Nρ_R⟩_h/N = (ρ_R0+δρ_R) − ρ_R0(1−Φ) = δρ_R + ρ_R0 Φ  (q≠0)`, and `δρ_R = 0`:
```text
E3:  2 M_P^2 c_N (-k^2)(Z - Phi + U) + ρ_R0 Phi = 0
```

**E4 — independent spatial trace equation.** Einstein quadratic part
`2|DΨ|² − 4DΦ·DΨ` (FINAL_ACTION §5) gives the E–L trace
`(M_P²/2)·4D²(Φ−Ψ)`; the projector stress (9) `ΔT^ij_mean = −[⟨Nρ_R⟩/N] z h^ij`
contributes `(1/2)T^ij δh_ij/δΨ = 3ρ_R0 Z` (with `h^ij δ_ij = 3`). Linear filter and
gate stress vanish (quadratic in first-order fields; `δS_h` variation is second
order). Dust baryons have no linear anisotropic stress:
```text
E4:  2 M_P^2 (-k^2)(Phi - Psi) + 3 ρ_R0 Z = 0
```

All four equations are re-derived symbolically in `compute_as285.py` (symbols as
above; residuals checked exactly). Sign conventions are anchored by the pinned
static matrix (16) — see control C2/C5.

---

## 3. Carrier decoupling (dark-sector answer to step 1)

Linearized carrier equations (8) around the vacuum origin: every source term is
proportional to background field values or gradients (composite-lapse coupling
`N_d = Ne^{−z}` enters only through products with ∂φ_A or φ_A), which vanish at the
origin. Hence the five carriers stay at the origin to linear order, and

```text
δρ_R = 0   (exactly, to linear order)
```

for baryon-induced perturbations. The dark sector enters the growth response only
through (i) the homogenous barrier density `ρ_R0 = V₀` in the projection terms of
E3/E4 and the lapse constraint, and (ii) the background expansion. This is a genuine
content statement: **on its homogeneous vacuum background, the CA5-GNC-R dark sector
is inert to linear baryon growth**; the scale-dependent response is produced by the
host's compensator/filter block.

---

## 4. Step 2 — elimination of auxiliaries

Fourier symbols: `k² = (q/a)²`, `S = S_k`. Solving E2, E3, E4 for (Z, U, Ψ) (linear,
unique for `M_P² c_N k² ≠ 0`; residuals verified exactly zero in sympy and Lean):

```text
Z   = (ℓ/4) S Φ                                  (E2)
U   = Φ − Z + ρ_R0 Φ / (2 M_P^2 c_N k^2)
    = Φ [ 1 − ℓS/4 + ρ_R0/(2 M_P^2 c_N k^2) ]    (E3)
Ψ   = Φ [ 1 − 3ℓS ρ_R0 / (8 M_P^2 k^2) ]         (E4)
```

Substitution of (Z, U, Ψ) into the lapse constraint E1 gives the exact reduced form

```text
(M_P^2/2) k^2 Φ A_tot = ρ_b0 δ_b
A_tot = A0 + 2ℓS ρ_R0/(M_P^2 k^2)
A0    = -4 + 2α + ℓS (1 + c_N − α/2) − (c_N/4)(ℓS)^2
(sympy: E1 − [(M_P^2/2) k^2 Φ A_tot − ρ_b0 δ_b]  ≡  0  exactly)
```

so

```text
Φ = 2 ρ_b0 δ_b / (M_P^2 k^2 A_tot)        (A_tot < 0 ⇒ Φ < 0 for δ_b > 0)
-k^2 Φ = 4πG_N ρ_b0 δ_b · ( −4c_N / A_tot )
```

using `4πG_N M_P^2 = 1/(2c_N)` (with `G_N = G_bare/c_N`; check:
`−2/(M_P²A_tot) = −16πG_bare/A_tot = −16πG_Nc_N/A_tot = 4πG_N·(−4c_N/A_tot)`):

```text
│                  -q^2 Φ = 4π G_N μ_g(q,a) ρ_b0 δ_b,   q^2 ≡ k^2 a^2 ... (convention below)
│  μ_g(q,a) = -4 c_N / A_tot
│  η_g(q,a) = Ψ/Φ  =  1 − 3ℓS ρ_R0/(8 M_P^2 k^2)
```

**Convention.** The seed writes `-q²Φ = 4πG_N μ_g ρ_b δ_b`. In this document
`q` denotes the **physical** wavenumber `q = q_com/a`, so `q² = k²` and the relation
reads exactly as stated with `μ_g = −4c_N/A_tot`. In comoving form it is
`−q_com² Φ = 4πG_N a² μ_g ρ_b δ_b`. Dimensionless combinations below use
`q/(aH)` (physical wavenumber over Hubble).

**Pinned-matrix consistency (crucial sign/size anchor).** In the pure-host static
limit (α = 0, c_N = 1, ρ_R0 = 0): `A0 = −4(1−ℓS/4)² = −4Q²` ⇒

```text
μ_g = 1/Q^2,   Q = 1 − ℓS/4        (exactly the Φ-entry of the pinned matrix (16))
U = Q Φ = u_b/Q,   Φ − Z = Q Φ = u_b/Q   with u_b = Q²Φ      (the Q⁻¹ entries)
Ψ = Φ                                    (the leading-order no-slip of FINAL_ACTION §5)
```

All three entries of the baryon column of (16) are reproduced symbolically exactly
(control C2/C5), which fixes every sign in E1–E4.

---

## 5. Step 3 — the bounded growth equation

Dust continuity and Euler (comoving gradient, physical k):

```text
δ̇  + i k v = 0            (continuity)
v̇  + H v  = −i k Φ        (Euler; baryons feel the lapse potential Φ)
⇒  δ̈ + 2H δ̇ = −k² Φ
```

with the modified Poisson law from §4: `−k²Φ = 4πG_N μ_g ρ_b0 δ_b` ⇒ in
`s = ln a`, `′ = d/ds`:

```text
│  δ_b'' + (2 + H'/H) δ_b' = (3/2) Ω_b(a) μ_g(q,a) δ_b            (G)
│  Ω_b(a) = 8πG_N ρ_b0 a^{-3} / (3H^2) = Ω_b0 a^{-3}/E(a)^2
│  H'/H   = −(3/2) c_N Ω_b0 a^{-3}/E(a)^2          (G_cosm = c_N G_N, eq. (18))
│  E(a)^2 = c_N (Ω_b0 a^{-3} + Ω_R0) + Ω_L0,   Ω_L0 = 1 − c_N(Ω_b0 + Ω_R0)
```

**"Bounded":** for fixed host parameters, over the band, `1 ≤ μ_g ≤ (1−ℓ/4)⁻²·(1+O(Ω_R0 (aH/q)²))`
(μ_g monotonically decreases with q through S_k; numerically 1.0016–1.0208 in the
illustration cell), so the growth response is a bounded, scale-dependent enhancement:
growth is **enhanced** at long wavelengths by the compensator, recovering Newton at
high q. The mass term `(3/2)Ω_b μ_g δ` uses the measured `G_N`; the background uses
`G_cosm = c_N G_N` — the ratio is carried explicitly (framework contract).

**Discarded time-derivative error (stated precisely).** (i) In the lapse constraint:
`(M_P²/2)(12−18c₂)HΨ̇` (from `T_K` and `2KQ_K`), relative to the retained
`(M_P²/2)4k²Ψ`: `ε_QS = |12−18c₂|/4 · (aH/q)² · |Ψ̇|/(H|Ψ|)`; growing modes have
`|Ψ̇|/(H|Ψ|) = O(1)`, so `ε_QS ≤ 1.5(aH/q)²` at c₂ = 1 ($= 1.5×10⁻²$ at q = 10aH,
$1.7×10⁻³$ at q = 30aH, $1.5×10⁻⁶$ at q = 10³aH). (ii) In the metric-potential
sources of the continuity/Euler combination: the standard quasistatic treatment keeps
`−k²Φ` with the fast and slow time-derivative pieces `Φ̇, Ψ̇` of the *full*
relativistic system dropped; those enter at the same `(aH/q)²` order (they are not
independently re-derived here — see limitations). (iii) The `c₂`-sector slip channel
`−2KA_K/N = 0` exactly on q ≠ 0 modes. Within the band the truncation error is
`≤ 1.5(aH/q)²` in the illustration cell.

---

## 6. Step 4 — the requested relation and its controlled properties

```text
-q^2 Φ = 4π G_N μ_g(q,a) ρ_b0 δ_b ,    Ψ = η_g(q,a) Φ
μ_g = -4c_N / [ -4 + 2α + ℓS_k(1+c_N−α/2) − (c_N/4)(ℓS_k)^2 + 2ℓS_k ρ_R0/(M_P^2 k^2) ]
η_g = 1 − 3ℓS_k ρ_R0/(8 M_P^2 k^2)  =  1 − (9/8) ℓS_k Ω_R0 (aH/q)^2
ρ_R0/(M_P^2 k^2) = 3 Ω_R0 (aH/q)^2        (dimensionless, c = 1)
```

Assumptions: inactive branch; vacuum carrier origin; quasistatic band q ≫ aH; flat
k=0 background; no slip beyond the retained projector stress; κ = 1/2, α, c₂, ℓ, ξ,
θ, δ and the density partition are inputs.

**Both footings.** The response functions are dimensionless in a₀ (a₀ cancels; κ
independent), so **one proof applies to both footings**. The two footings enter
through the illustrative assignment `V₀ = ρ_Λ c²`:
canonical a₀ = 9.3619×10⁻¹¹ m/s² ⇒ ρ_Λ = 5.8444×10⁻²⁷ kg/m³ ⇒ Ω_R0 (V₀) = 0.685;
alternative a₀ = 1.1279×10⁻¹⁰ m/s² ⇒ ρ_Λ = 8.4831×10⁻²⁷ kg/m³ ⇒ Ω_R0 (V₀) = 0.994.
(Separately: ratio 1.2047768; holding ρ_Λ fixed, effective κ = 0.6023884; holding
κ = 1/2 fixed, ρ-ratio 1.4514872 — the two footings never share fixed ρ_Λ AND fixed
κ.) The alternative footing would make the barrier nearly closure-density; both are
labelled illustrative inputs, not predictions.

**Controls (implemented symbolically and numerically; all in raw_output.json):**

| control | content | result |
|---|---|---|
| A | substitution-back residuals of E2, E3, E4 and of the reduced E1 | exactly 0 (sympy) |
| B | Einstein recovery: ℓ=α=ρ_R0=0, c_N=1 ⇒ μ_g = η_g = 1 | PASS (exact) |
| C | pure-host pinned matrix (16): μ_g = 1/Q², U = u_b/Q, Φ−Z = u_b/Q | PASS (exact) |
| D | high-k in-band recovery S_k→0: μ_g → 1, η_g → 1 (with c_N = 1−α/2) | PASS (exact) |
| E | no-gate limit ℓ→0: μ_g → 1 (G_N-normalization recovery) | PASS (exact) |
| F | **negative control**: set Ψ = Φ by hand; E4 residual `= 3ρ_R0 Z = (3/4)ℓS_k ρ_R0 Φ ≠ 0` | **fires as required** (grid: 5.85×10⁻⁴ … 4.7×10⁻⁹ at Φ = 1) |
| G | growth ODE integrator calibration: ΛCDM (0.3, 0.7), μ ≡ 1 ⇒ f(z=0) = 0.5128 (expected ≈ 0.51; independent solve_ivp: 0.5128); EdS: δ = a exactly | PASS |
| H | numerical band grid: residuals of the true solution vs. control residual; monotone μ_g(q) | PASS |

**Growth outputs (illustration cell, q/(aH) quoted at a = 1, z = 0):**

| q/(aH) | μ_g | η_g − 1 | f(z=0) | f/f_Einstein − 1 |
|---|---|---|---|---|
| 10 | 1.0208 | −2.92×10⁻⁴ | 0.1858 | +1.28% |
| 100 | 1.0198 | −2.85×10⁻⁶ | 0.1856 | +1.17% |
| 1000 | 1.0016 | −2.3×10⁻⁹ | 0.1835 | +0.012% |
| (μ≡1 ref) | 1 | 0 | 0.1835 | — |

The scale-dependent growth enhancement saturates at the long-wavelength plateau
`(1−ℓ/4)⁻² ≈ 1.0203` and dies out at high q: the growth response is a **bounded,
scale-dependent, small enhancement** in the inactive band — it cannot by itself
produce a MOND-scale (order-one) growth anomaly; the operative filtered-MONO gate
lives outside this band (see §9).

**Single downstream calculation enabled/blocked.** *Enabled:* the CA5-GNC-R
inactive-branch RSD prediction `fσ₈(q, z)` (needs only the survey forward model) and
the lensing combination `Σ(q,a) = μ_g(1+η_g)/2 ≈ 1/Q² + O((aH/q)²)` — both are now
well defined on the band. *Blocked:* the active-branch (gate-on, y > 0) growth
response — the perturbation of `Y_h = J(DS_hU) + ℓΔ_hW_b − θ` with f≠0 requires the
heated-field sector (W_b, L, λ₀ perturbations) — and any statement outside the
quasistatic band, which needs the full time-dependent system.

---

## 7. Lean 4 certificate

`AS285_growth_response.lean` — 11 theorems, self-contained, `lake env lean` exit 0,
**zero sorry**, unfiltered `#print axioms` exactly `{propext, Classical.choice,
Quot.sound}` for every theorem (`AS285_growth_response_axioms.lean`). Certified
content: Z-elimination residual; U-elimination residual (E3); Ψ-elimination residual
(E4); negative-control residual formula `3ρ_R0(ℓS/4)Φ` and its nonvanishing;
`A0(α=0,c_N=1) = −4Q²`; pure-host `μ_g = 1/Q²`; Einstein limits of μ_g and η_g; slip
multiplication identity `8M_P²k²(Φ−Ψ) = 3ℓSρ_R0Φ`; high-k recovery
`−4c_N = A0 (S→0)` with `c_N = 1−α/2`. No inequality theorems were certified (the
bounds in §8 are numerical estimates with analytic structure, stated in the
derivation rather than Lean).

---

## 8. Parameter cell (illustration, all inputs)

α = 0.5 (c_N = 0.75), c₂ = 1.0, ℓ = 0.04 (the action's own illustrative value,
FINAL_ACTION §5), ξ = 10 Mpc (heat-filter width, illustrative), θ, δ irrelevant on
the inactive branch, H₀ = 67.4 km/s/Mpc, Ω_b0 = 0.05, Ω_R0 = 0.65 (G_N-normalized
inputs ⇒ Ω_L0 = 1 − c_N(Ω_b0+Ω_R0) = 0.475), G_N = 6.67430×10⁻¹¹,
c = 299792458, M_sun = 1.98847×10³⁰, pc = 3.085677581491367×10¹⁶.
No per-object fit; no gate on. Units: SI for inputs; response functions dimensionless.

**Execution bounds (actually enforced):** wall 120 s via in-process SIGALRM
(measured 0.52 s), 1 thread, 512 MB declared ceiling (measured peak RSS 86 MB —
declaration only; macOS rlimit not set). Prototype: sympy (exact) + numpy/math,
41-point band grid × 3 scale factors, 4 RK4 integrations × 6000 steps.

---

## 9. Limitations, unresolved implication, follow-ups

**Does not establish:** active-branch (MONO-gated) growth response; anything outside
q ≫ aH (in particular the long-wavelength quenching μ_g → 0 as q → 0, which the
band-exact formula shows but which is outside the controlled band); the full
time-dependent scalar system (Ψ̇ channels, momentum constraint used only through dust
conservation); the magnitude of V₀; abundance/initial data of the carriers; η_g ≠ 1
beyond the (aH/q)² correction, which is comparable to the discarded truncation error
(so the slip's sign/magnitude is a band-level statement, not a beyond-band claim);
prerequisites AS251/AS279 have no completed results.

**Next unresolved implication:** the active-branch growth response: linearize the
heated-gate sector (W_b, L, λ₀ perturbations of FINAL_ACTION §3) around the
homogeneous background with δY_h > −θ − J(0) … threshold crossing, and derive
μ_g^act(q,a), η_g^act(q,a) in the band where the quasistatic error is controlled —
the single missing input between this result and the operative filtered-MONO growth
target.

**Child proposals (specs written for the orchestrator; not dispatched — no runner
mechanism in this subagent):**
- `AS285.C01` — active-branch growth response with the heated-gate sector (parent
  AS285-r1 run; fingerprint: action b8c04d4e… + R1, active branch, f≠0, band q ≫ aH;
  target: μ_g^act, η_g^act; control: recover the inactive result as θ → ∞; dependency:
  heated-field variation (11)).
- `AS285.C02` — lensing combination Σ = μ_g(1+η_g)/2 and the CMB-lensing/weak-lensing
  proxy on the inactive band (fingerprint: observable forwarding; control: Einstein
  limit Σ → 1; dependency: C01 inactive result, survey geometry input).
- `AS285.C03` — exact two-cell compact-leaf check of the projection term
  `ρ_R0Φ` in E3 (finite-difference in ln N and in the Fourier mode, mirroring
  AS127's control style; fingerprint: compact-leaf projection, q≠0 mode, ρ_R0 coupling;
  control: ρ_R0 = 0 kills the term).

**Closure implication:** supplies the first controlled growth response of CA5-GNC-R
for the amended thirteen-item target's cosmological-perturbation gate (requirement 8,
"viable cosmology" + perturbation structure): the inactive-branch μ_g, η_g and the
growth ODE (G) are exact within the stated band, and the result explicitly does NOT
close the framework — the active-branch response and the beyond-band (aH/q)⁰ terms
remain open; `closure_candidate = null`.

## 10. Artifacts

`derivation.md`, `result.json`, `compute_as285.py`, `raw_output.json`,
`AS285_growth_response.lean`, `AS285_growth_response_axioms.lean`,
`lean_compile_out.txt`, `lean_axioms_out.txt`, `run_stdout.txt`,
`raw_output.stderr` (hashes in result.json).
