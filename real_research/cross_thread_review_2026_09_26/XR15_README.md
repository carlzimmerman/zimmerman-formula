# XR15 — the last concrete repairs of V0's gate obstruction: door (c), then door (b)

Cross-thread review, 2026-09-26 (night). Read-only on every other file. Two scripts in this folder, each with controls that
reproduce committed numbers exactly and a MUTATE run that must fail. Both a₀ footings in every scan (canonical 9.36e-11,
alt 1.13e-10 m s⁻²). κ = ½ stays a declared input; the dark mass is still required; no new particle species.

**The obstruction** (DE12 `7f84b3546`, DE13 `6daea932c` + `a7abb4d4f`). Varied as an action term, the MOND-sector gate
f = W(U) is a k⁰ negative bulk modulus on edge-layer gas, amplified by A²: Γ = c_gate k, 2–5e4 H at k = 1/kpc. No
gradient energy of any strength repairs it.

## Answer

**Neither door closes the obstruction.**

- **Door (c)**, a smoothed gate variable (1 − ℓ²∇²)χ = U, removes DE12's UV catastrophe. What remains is a residual at the
  layer's own scale that no ℓ removes, at 1.1–2.8 H on 16 of the 24 galaxy layers.
- **One constant ℓ** cannot also keep the flagship: the smallest layers and the largest need smoothing lengths two orders
  of magnitude apart.
- **The κ-capped branch keeps a k⁰ instability.** Smoothing only dilutes it.
- **V0 as written has a gate-dependent constraint determinant** that vanishes inside every layer. Door (c) does not remove
  it. This one is new and is a finding about CV3.
- **Door (b)**, a switched stiffness h(U)|∇U|²: its own switch-off term destabilises every switch zone at every width.

## Door (c): `XR15_smoothed_gate.py` (9/11; the two failures are the pre-declared H1 and H2, recorded)

**Construction** (sympy, A1). The gate is f = W(χ), with ζ[(χ − ℓ²χ″) − U]/(8πG) added and the multiplier entering linearly.

- **The multiplier.** The χ-equation gives (1 − ℓ²∂²)ζ = −8πG B W′(χ), so ζ is the smoothed gate force.
- **Structure kept.** The gate's u-part −Cζ″ cancels its v-part, so the carrier stays blind, and there is no slip. The
  sympy residuals are ≤ 3e-173.

**Exact second variation** of DE12's reduced functional −∫B(y) W(t(χ)), with χ = G_ℓ U:

| term | what it is | under smoothing |
|---|---|---|
| T1 = ∫B W″ t² (G_ℓ δU)² | DE12's k⁰ term | suppressed as (1 + ℓ²k²)⁻² |
| T2 = ∫Ξ δ²U | **the analogue of DE13's background term**: the smoothed gate force Ξ = G_ℓ(B W′ t) times the phantom's own curvature (h″) | not suppressed |
| T3 = 2∫B′ W′ t (G_ℓ δU) | the cross term: the kernel coefficient's response B′ = a₀h(y) δg_N/(4πG) times the gate | suppressed once |
| T4 = ∫B″ W | the gated kernel's own term, i.e. the gas's MOND self-gravity (no W′, W″) | reported as context, neglected with self-gravity (DE13's scope) |

The smoothing is linear, so it has no gradient-of-background term of its own. C3 checks T1–T4 against finite differences
of the discretised functional to ≤ 2.6e-6 of their summed size. Without T2 + T3 the check misses by 11–18% at ℓ = 0.1 r_e.

**Method.** Spherical perturbations are exact in a spherical background, so the ℓ = 0 sector is solved exactly: radial
displacement, δU = C div(A_par δg_N), χ's perturbation on the radial Yukawa operator, and growth from M ξ̈ = −K ξ. DE13's
convention (radial modes carrying A_⊥) is reported beside it.

**Controls.**

- **C1.** ℓ = 0 reproduces DE12's committed c_gate and Γ(1/kpc)/H on all 24 layers and its capped cluster, to 2.2e-16.
- **C2.** The smoothing solver matches the exact spherical Yukawa integral to 2e-3 (at ℓ/Δr ≈ 5) and 5e-6.
- **C4.** At ℓ = 0 every galaxy layer is unstable and gas alone is stable. The discrete growth matches the WKB rate at
  ℓ = 0.02 r_e to within a factor 0.61–0.78.
- **C5.** Converged: 800 vs 1600 points within 3.8%; a 6ℓ vs 9ℓ domain margin within 1.8%.

**Growth vs ℓ per layer** (exact ℓ = 0 sector; R1 has the full grid ℓ/r_e = 0.01…1):

| layers | Γ/H at ℓ = 0.01 r_e | Γ ≤ H | min Γ/H over ℓ ≤ r_e | Γ ≤ the layer's own evolution rate (5.4–11 H) |
|---|---|---|---|---|
| z = 2.5, 4 × 1e10, 1e11 (8) | 580–830 | from ℓ/r_e = 0.06–0.19 (energy-stable) | 0 | ℓ/r_e = 0.06–0.13 |
| z = 0.25, 1 (all masses) and 1e12 at every z (16) | 390–770 | **never** | 1.1–2.8 | ℓ/r_e = 0.12–0.21 |

**The residual has one driver.** At ℓ ≥ 0.3 r_e the residual is carried by T3; gas + T3 alone gives 2.9–3.9 H. It sits
just outside the layer and reaches about 4ℓ beyond it.

- T1 alone is 0–3 H and T2 alone is stable.
- For context, the gas's own MOND Jeans growth (T4) on the same domains is 5–15 H at ℓ ≥ 0.3 r_e (z ≤ 2.5; zero at z = 4,
  1e10). That growth is outside DE12's and DE13's frozen-background scope.

**H1 [pre-declared]: FAILS, 8/24.** The hypothesis was that some ℓ ≤ 0.3 r_e brings every layer to Γ ≤ H with its own
edges moved < 10%. Where Γ ≤ H is reached, the edges move 0.5–6%.

**H2 [pre-declared], one constant ℓ: FAILS.** No ℓ in 1–1500 kpc brings every layer to Γ ≤ H. The pincer:

| ℓ (kpc) | 10 | 100 | 150 | 300 | 500 | 700 | 1000 |
|---|---|---|---|---|---|---|---|
| max Γ/H, z = 0.25 | 1.2e3 | 87 | 53 | 20 | 6.8 | 3.0 | 3.1 |
| KiDS lens edge shift (1e11, z = 0.25) | 0.0% | 0.6% | 1.5% | 5.7% | 7.5% | 6.0% | 11% |
| z = 4 region edges | 8% | 99% | 99.6% | gone | gone | gone | gone |
| flagship r_F (z = 2.5) | on | on | **off** | off | off | off | off |

- Every layer ≤ 10 H needs ℓ ≥ 500 kpc, and every layer below its own evolution rate needs ℓ ≥ 700 kpc.
- The flagship, KiDS and the Sun hold only to ℓ = 100 kpc.
- The z = 4 regions' edges stay within 10% only to ℓ = 10 kpc.
- The smoothed gate's own force at r_F is ≤ 0.003 dex while MOND is on there. At the Sun it is ≤ 3.3e-8 g at every ℓ, and
  the Galaxy stays on.

**R5, not pre-declared: a smoothing length that depends on cosmic time only.** ℓ(z) is still linear on each leaf. With
ℓ(z) = 0.19–0.26 × MS5's cap length v_cap/(H√x_c,eff), every 1e10–1e12 layer falls below its own evolution rate. It never
reaches Γ ≤ H.

| z | ℓ(z), kpc | max Γ/H | edge shift, 1e10–1e12 | edge shift, 1e9 dwarfs | notes |
|---|---|---|---|---|---|
| 0 | 801 | 3.6 | 27% | 80% | the Sun on |
| 0.25 | 545 | 5.4 | 17% | 69% | KiDS lenses 7.5% |
| 1 | 185 | 9.0 | 8% | 50% | |
| 2.5 | 43 | 10.6 | 8% | 48% | flagship on (t(r_F) ≥ 10.5) |
| 4 | 17 | 10.3 | 8% | 51% | |

This is a lead, not a pass.

**The κ cap with χ (R4).** The natural combination is χ = G_ℓ(U_cap): the cap sits inside U, so the constraint stays
linear.

- **Capped edges.** They move 0.2–0.3% at ℓ = 100 kpc, 3.5–10% at 300 kpc and 31–40% at 1 Mpc (z = 0.25 cluster; MS3's
  z = 0.5 cap).
- **The capped branch's own k⁰ term Ξ U_ρρ is not suppressed by the smoothing, only diluted.** c_ρρ is 1140, 975, 653 and
  336 km/s at ℓ = 0, 100, 300 and 1000 kpc.
- Against 1e6 K gas (117 km/s) that is a UV instability at every ℓ ≤ 1 Mpc. Against ICM-temperature gas (~1000 km/s) it
  is subdominant from ℓ ≳ 100 kpc.

**The constraint determinant and the count (A2, L1).**

- **Count.** The new pair (ζ, χ) adds two fields and two constraints. Neither carries a time derivative, so χ adds no
  propagating mode where det K ≠ 0.
- **det K is not gate-independent.** Its symbol is 2k⁴[G_loop k² − (1 + ℓ²k²)(k² + M²)], with G_loop = U_b W′ t (A − 1).
- **The cause is V0's own structure.** w's source is f ∇²(u − v), and U reads w's phantom, so the gate sits inside the
  constraint that fixes what it reads.
- **CV3's A+ at ℓ = 0 has the same defect.** Its (Ψ, w) entry carries 1 − G_loop, which CV3's G3 matrix omits (sympy,
  residual 5e-175).
- **On the real layers** max G_loop = 1.7–11.8 inside every one of the 24 galaxy layers, in both directions, over 46–70%
  of each layer.
- **So the constraint symbol vanishes inside every layer.** At ℓ = 0 it vanishes on surfaces. For ℓ > 0 it vanishes at
  k* = √(G_loop − 1)/ℓ, unless (1 + Mℓ)² > G_loop. With L361's screening (1/m = 0.2–0.5 Mpc) that needs ℓ ≈ 0.44–3.3 Mpc.
- **The fix exists.** If U reads the phantom of an *ungated* auxiliary (a further pair, ∇²w̃ = ∇²(u − v)), then
  det K = 2k⁶(k² + M²)(1 + ℓ²k²): gate-free. DE12's reduction, and every stability number above, price that variant.
- **Owners' decision** (CV3 / the V0 writer): which gate reading is V0's.

**MUTATE** drops the smoothing inside the second variation. S1 fails: min Γ/H is 1.8e3–7.5e3 at every ℓ. C5 fails with
it, because the unsmoothed growth is grid-limited. rc = 1.

## Door (b): `XR15_switched_stiffness.py` (3/4; the failure is the pre-declared H_b, recorded)

**Construction.** The repair is (1/2) h(U)|∇U|² with h = μ S(U) and S = 1 − W(ln(U/U₁)/ln R), U₁ = 1 + w. So S = 1 across
the whole layer and S = 0 for U ≥ U₁R.

- **The switch's own term** is −[(1/2) h″|∇U|² + h′∇²U]. B2 checks it against finite differences to 1.4e-6; without it the
  check misses by 7.5e-2.
- **μ is one constant: DE13's universal μ_U.** B1 reproduces DE13's committed λ_U exactly.
- **The flagship caps the width.** The repair must be off at r_F, which gives R ≤ R_max = 11.9 (1e11 at z = 2.5). At z = 4
  it would be 1.6.

**Results.**

- **Every switch width is unstable.** For every R from 1.5 to 1000, every one of the 24 galaxy layers' switch zones has a
  negative mode (B3). At R ≤ R_max the growth runs from 45 H (z = 4, 1e12) to 3.3e4 H (z = 0.25, 1e10), and reaches 8e4 H
  at R = 1000.
- **A wider switch does not help.** It only moves the switch inward, where μ/r² is larger.
- **The universal μ is far above most layers' need.** It is 1–6300× what each layer needs.
- **Per-layer μ does not rescue it either.** Even with each layer's own μ_U, 17–24 of 24 layers stay unstable, at 16–67 H
  at R_max.
- **The exact radial convention agrees.** 24/24 unstable, up to 2.8e3 H.
- **The repair's own force at R_max is large.** In the regions' interior (0.3–1.2 Mpc around a z = 0.25 L\* lens) it is
  |Φ| ≈ 4–5 v_f² and |g|/g_MOND ≈ 400. That is an order-unity-plus change to the lensing.

**H_b [pre-declared]: FAILS.** No R clears all layers. **MUTATE** drops K0: B3 fails, rc = 1, and without its own term the
door would appear open.

## What is left

- DE13's door (a), a prescribed and unvaried gate.
- CV6's dynamical gate field.
- The ℓ(z) ≈ 0.2 ℓ_cap(z) lead. It reaches Γ ≤ evolution rate, never Γ ≤ H, and has open costs:
  - dwarf regions' edges move 41–80%;
  - the capped branch stays UV-unstable;
  - the T3 residual depends on B's variation, which DE12's reduction takes as a₀²q(y²)/(8πG) of the ungated field (V0's
    full B carries Ψ terms and reads the gated w).
- Separately, CV3 owes a decision on the loop (L1).

## Development record (disclosed)

- **Exploration before the pre-declaration.** Single-layer runs on z = 0.25/1e11 and 1e12, z = 2.5/1e11 and z = 4/1e10
  (canonical) were used to build the machinery before H1/H2 were written.
- **A sign error caught before any recorded number.** A relative sign between δU and δg_N was wrong in the first assembly.
  C3's finite-difference check caught it.
- **The first full run used a 2ℓ domain margin, which truncated the fastest mode.** C5 now reports those values
  (e.g. 1.15 H vs the converged 2.64 H). H1 went from 18/24 to 8/24 when the margin was converged; the hypothesis text did
  not change.
- **Door (b)'s hypothesis was written before its main run.**

## Files

| file | contents |
|---|---|
| `XR15_smoothed_gate.py` | door (c) script |
| `XR15_smoothed_gate.out`, `XR15_smoothed_gate_MUTATE.out` | door (c) main and MUTATE outputs, rc = 1 each |
| `XR15_smoothed_gate_results.json`, `XR15_smoothed_gate_results_MUTATE.json` | door (c) results |
| `XR15_switched_stiffness.py` | door (b) script |
| `XR15_switched_stiffness.out`, `XR15_switched_stiffness_MUTATE.out` | door (b) main and MUTATE outputs, rc = 1 each |
| `XR15_switched_stiffness_results.json`, `XR15_switched_stiffness_results_MUTATE.json` | door (b) results |

Run from the repository root (about 111 s and 34 s):

```
python3 real_research/cross_thread_review_2026_09_26/XR15_smoothed_gate.py
python3 real_research/cross_thread_review_2026_09_26/XR15_switched_stiffness.py
```

Add `MUTATE=1` for the controls. DE12 and DE13 are loaded by extracting their definitions only; their checks never run and
their JSONs are only read.
