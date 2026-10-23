# I1_gammaL_causality: what is the causal structure of v4 (AeST + γ_L + capped F)?

## Verdict (frozen rule): ILL-POSED (where the aether twists)

- **Where it is well posed.** On backgrounds where the aether is twist-free (Minkowski, FRW, exact spherical
  symmetry), the γ_L scalar is a **Schrödinger/beam-type** mode. It has real ω = √A k² (A = (2−K_B)L★²/(4K₂)). That is
  Petrovskii-correct, time-reversible and dispersive, not diffusive. There it violates criterion A and meets criterion B.
- **Where it is ill posed.** v4 needs a **twisting** aether to give the law (C1). In any non-symmetric bound system the
  twist is forced (K5). Examples are the Sun in the Galaxy's field and every disc galaxy. No time slice is
  aether-orthogonal there.
  - On any slice tilted by w relative to the aether, the k⁴ term gives two complex roots.
  - Above κ_c ≈ 1/(2√A w) their imaginary part is Im ω → κ/(γw). That is unbounded and linear in κ, like Laplace's
    equation posed as an initial-value problem. So the Cauchy problem is **Hadamard ill-posed**.
  - The same high-k rays close **signal loops** that arrive before they leave (Δt = ∮a·dx). So criterion B is violated
    in principle there.
- **No healthy completion was found (Q3).**
  - A time-derivative partner (q^{μν} → g^{μν}) keeps the static symbol exactly, but brings an Ostrogradsky ghost.
  - An auxiliary field with a Lorentz-invariant kinetic term has Im ω ∝ k for either sign.

**Checks.** 9/9 PASS, exit 0. Run: 5.8 s, 0.47 GB RSS, one thread, nice 15, no downloads.
- The criteria were frozen first (d5e8ba9842). AMENDMENT A1 (fca0b01118) is **pre-result**: it switched the
  illustrative galaxy from Kuzmin to Miyamoto–Nagai, because Kuzmin's twist is identically 0.
- `I1_MUTATE=1` (γ_L → −γ_L, isotropic response) fails K3 and K5 (7/9). The mutated verdict is "ILL-POSED (everywhere)".

κ = ½ FITTED. Both footings, never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework.

## 1. Principal symbol (K1–K3; sympy, from SZ21's `Minkowski_action` on disk + the stiffness term)

- **The stiffness term contains no time derivative (K1, DERIVED).**
  - About Minkowski, with a general h_{μν} (no gauge fixing) and a general aether, the covariant
    (q^{μν}∇_μ∇_νφ + θQ) is exactly ∂_i(∂_iϕ + Q₀A_i) = ∇·V at first order (residual 0). The θQ piece cancels every
    metric ∂_t.
  - On flat FRW it vanishes on the background. At first order it is a⁻²(∇²ϕ + φ̄′∇·B).
  - So the term's symbol is (q^{μν}k_μk_ν)² = p⁴ on every background. It does not depend on F or Y.
- **One propagating scalar (K2, COMPUTED).** The scalar sector (Ψ, Φ, α, ϕ) has det of degree 4 in ω: ω² = 0 twice
  (the dust) plus one branch. That branch equals C5 H10's closed form exactly: ω² = A k⁴ + B k² + M².
- **Petrovskii on aether slices (K3).**
  - Every coefficient of ω²(k) is ≥ 0 for 0 < K_B < 2, K₂ > 0, λ ≥ 0, so Im ω ≡ 0. The system is mixed:
    - tensor and vector modes are hyperbolic (speed 1, vector mass²);
    - the scalar is **Schrödinger/beam-type** (ω ∝ k² at large k);
    - the dust is ω = 0.
  - On FRW the H1/H3 Jeans rate is bounded (≤ √(4πG̃ρ̄)), which is Petrovskii's bounded-Im condition.
  - About the Sun in the Galaxy's field (C6's x_e), only B is changed: it is anisotropic and grows as λ_L ~ y² when
    unscreened. A is unchanged.
- **Physical content of the ω ∝ k² mode.**
  - It is a **propagating** mode: positive Krein (C5 H10, H3), not a constraint.
  - It is **dispersive** (real ω), not diffusive. There is no backward-heat problem.
  - Its group speed is 2√A k = c_s√K_B L★ k: unbounded. At k = 1/km it is 1.7e13–2.8e15 c on the declared grid.

## 2. Tilted slices and the twist (K4–K7)

**K4: ill-posed on any tilted slice.**
- Write the aether-frame relation s² = A p⁴ + B p² + M², with s = −u·k and p² = q^{μν}k_μk_ν, in a frame whose slice
  normal moves at w relative to the aether. It becomes quartic in the slice frequency.
- For κ ⟂ w, exactly: the roots are complex iff κ² > κ_c² = (1−Bw²)²/(4Aw²) − M²w². They are real at w = 0.
- Numerically, at 10³ κ_c, Im ω/(κ/γw) is 0.045 along w, rising to 1.000 at κ ⟂ w (7 directions).

**K5: the twist is forced.** In v4's static transverse equation, (ℓ_F²/2)∇×∇×V_T + M_T V_T = −Π(MδV), and the aether
velocity is a_T = V_T/Q₀.
- The capped-F response is M = diag(1+y, 1+y, (1+y)²). Its transverse source is |ΠMk̂| = (1+y)y|sinθ cosθ|, which is
  nonzero at every y > 0 off the symmetry axes.
- The Sun's own twist is ∇×V_T = −(1+y)y(GM/L★²) r sinθ cosθ/(2ℓ_F²) φ̂ (residual 0).
- It vanishes only for exact spherical, planar or cylindrical symmetry, or an isotropic response (the mutation).

**K6: signal loops.** A ray moving at speed v relative to the aether has Δt = ℓ/v + ∮a·dx (residual 0). So a relay loop
arrives before it is sent if v > ℓ/|∮a·dx|. Such speeds exist because v is unbounded.

**K7: sizes.** These use an ILLUSTRATIVE Miyamoto–Nagai Galaxy with the law applied pointwise, on the declared grid:
K_B 0.05/1, c_s 1/0.1, μ⁻¹ 1/10 Mpc, L★ 24/50/90 pc, both footings. The grid converges to 3.9 %. The Kuzmin sanity
twist is ≤ 1e-16.

| quantity | range on grid | reference (canonical, K_B 0.05, c_s 1, μ⁻¹ 1 Mpc, L★ 24 pc) |
|---|---|---|
| minimal tilt over 100 AU around the Sun | 3e-23 – 3e-20 | 2.7e-20 |
| λ_c (ill-posed below this wavelength), Solar System | 15 μm – 12 cm | 2.8 cm |
| growth rate at 2κ_c, Solar System | 9e29 – 7e36 s⁻¹ | 4e30 s⁻¹ |
| minimal tilt over 1 kpc near the Sun | 1e-15 – 1e-12 | 9.6e-13 |
| λ_c, 1 kpc region | 0.5 – 4200 km | 1000 km |
| growth rate at 2κ_c, 1 kpc region | 7e14 – 6e21 s⁻¹ | 3e15 s⁻¹ |
| Galactic loop (ϖ 4–12 kpc, z 0–2 kpc): time gained ∮a·dx/c | 4 ms – 3.9 s | 3.5 s |
| speed / wavelength needed to close it | 5e11 – 5e14 c / 0.9 – 7400 km | 6e11 c / 1800 km |
| Solar-System loop (100 AU): time gained | 3e-18 – 3e-15 s | 2.7e-15 s |
| wavelength needed to close it | 7 μm – 6 cm | 1.4 cm |

**Reading.**
- The ill-posed and loop-closing modes are classical-sized: centimetres in the Solar System, kilometres in a kpc region.
- The Solar-System tilt is set by the **Galaxy's** twist. The Sun's own twist is about 1e-9 of it.
- An EFT cutoff above κ_c would hide all of this. The record derives none, so it would be a new posit.

## 3. Criterion A size (K9) compared with C8

- The static response is v4's γ_L hedgehog, the same as C8's. So the lab signal (1000 kg moved 1 m, read at 1 km) is
  **1.22e-46 m/s²** at L★ = 24 pc, reproducing C8. It is 8.7e-48 at 90 pc.
- The difference from C8 is the carrier.
  - C8's khronon signal is an instantaneous leaf constraint.
  - Here it is a propagating dispersive wave: at 1 km scales it arrives at ~1e14 c, effectively instantaneously.
- Instantaneous-minus-retarded sizes:
  - Jupiter's hedgehog at the Sun (a_P = 2.3e-19 m/s²): 1.0e-23 m/s² at 24 pc.
  - A galaxy: about a₀v/c = 6.2e-14 (canonical) / 7.5e-14 (alt) m/s² at v = 200 km/s.
- The Solar System and galaxies have no bound at these levels.

## 4. Q3: completions (K8)

| addition | static symbol | health | counted? |
|---|---|---|---|
| time partner: q^{μν} → g^{μν}, i.e. (□φ + θQ)² | identical (residual 0); Cassini (C6) and globulars (D10) unchanged | adds φ̈ and Ḣ₀₀ (fourth order in time). Reduced roots: Krein +6.4e3 and **−7.6e3** → **Ostrogradsky ghost** | no |
| auxiliary σ with ε(∂σ)²/2 | changed at k² ~ 1/(εβ) | Im ω/k = 2.54 (ε > 0) and 1.80 (ε < 0) at k = 10–1000 → **Hadamard ill-posed** | no |
| hypersurface-orthogonal aether (no twist) | not AQUAL away from symmetry (C1) | this is v3/C8, which is well posed but fails growth (F3) | — |

**Result: none found.** Nothing in AeST's action supplies a cone for the γ_L term. Any partner is a posit, and the two
natural ones are a ghost and an ill-posed system.

## 5. Status under the owner's criteria

| background | well posed? | A (v ≤ c) | B (global time order) |
|---|---|---|---|
| Minkowski, FRW, exact spherical | yes (Schrödinger-type, on aether slices) | **violated** (unbounded group speed; lab signal 1.2e-46 m/s², = C8) | met (aether hypersurface-orthogonal) |
| any non-symmetric bound system (Sun in Galaxy field, discs) | **no**: Hadamard ill-posed for λ < λ_c on every slicing | violated | **violated in principle** (closed signal loops, ms–s around the Galaxy) |

**Compared with v3/C8.** C8's Khronon is twist-free by construction, so it is well posed with B met. v4 trades v3's
growth failure for this.

## What this does not show

- It is frozen-coefficient (WKB) and linear only. No nonlinear or variable-coefficient theorem is given, and no
  Hamiltonian count is made.
- The Galactic magnitudes are ILLUSTRATIVE: Miyamoto–Nagai disc, law pointwise along g_N, tilt ≈ |∇×a|·D/2.
  - The structural result (K4 + K5) does not depend on them.
  - K_B, K₂ and μ are not fixed by any lane; the grid is a reported range, not a fit.
- Whether a UV/EFT cutoff exists above κ_c is OPEN. One is not derived anywhere in the record.
- The literature AeST action is SZ21 on disk. The γ_L term is C1/C3's posit (+1 term, +1 constant).

## Inputs

| input | class | source |
|---|---|---|
| SZ21 `Minkowski_action` + dispersions | literature, on disk | `../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex` |
| stiffness term, β_L = (2−K_B)L★²/2 | POSTULATED (C1, C3) | C1, C3 READMEs |
| capped-F response λ_T = y, λ_L = (1+y)²−1 | FRAMEWORK-NATIVE | C5 H10 |
| x_e (canonical 1.30–2.60, alt 1.15–2.15) | FRAMEWORK-NATIVE / survey-calibrated MW fields | D7d `R2_scan` via C5 json |
| C8 lab signal 1.217e-46 | FRAMEWORK-NATIVE | C8 json `signal_illustration` |
| K_B, c_s, μ⁻¹ grid; Miyamoto–Nagai disc; Jupiter orbit | declared / ILLUSTRATIVE | FROZEN_CRITERIA §1, A1 |
| a₀ footings, L★ | FITTED | doors BRIEF, D10 |
