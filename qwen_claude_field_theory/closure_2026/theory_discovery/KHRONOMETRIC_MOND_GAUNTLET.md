# KHRONOMETRIC / Horava + MOND — the 5-gate health gauntlet (2026-08-29)

**Theory under test (the surviving direction after nine chassis died this session):**
single physical metric `g` (matter minimally coupled), a khronon `T` defining a preferred
foliation `u_mu = -d_mu T/sqrt(-(dT)^2)`, `a_mu = u^nu nabla_nu u_mu`, `theta = nabla_mu u^mu`.

```
S = (1/16 pi G) INT sqrt(-g) [ R + lam_K theta^2 + beta a_mu a^mu - g_mond(chi) a_mu a^mu ]
  - (1/16 pi G) INT sqrt(-g) V(chi)  +  S_m[g, psi]
```

Newton gate FORCES `g_mond(chi) = -(1-chi)` ⇒ effective `a^2` coefficient `eta(y) = 2(1-chi) = 2 e^-y`,
`y = c^2|a|/a0 = |D ln N| c^2/a0`. `V'(chi) = [ln(1-chi)]^2` FROZEN ⇒ `chi = mu(y) = 1-e^-y`.
`chi` auxiliary (algebraic, non-propagating).

**Verdict: `VIABLE_CANDIDATE` (conditional).** All five gates pass. `c_T = 1` exact; healthy
`lam_K` window; `alpha_1, alpha_2` self-screened by `e^-y`; lensing MOND-boosted; 3 DOF. The single
gating worry is *outside* G1–G5: the EFT strong-coupling scale in the `eta→0` Solar-System corner is
**not computed** (BPS's own caveat). This is the first coherent surviving class of the session — but
it is **3 DOF (2 tensor + 1 khronon), not the 2-DOF dream.**

Committed script: `khronometric_mond_gauntlet_2026.py` (35/35 checks, exit 0) + `.out`.
Trusted reused machinery (all committed, GR-validated, BPS-anchored, re-checked in-line):
`mond_compiler_2026/routeA_alpha12_ppn_2026.py` (41/41, BPS 1007.3503 Eq. 5.34@β=0);
`theory_2026/first_principles/sec12_scalar_sector.py`;
`real_research/reviews/mi_khronon_spin0_health_2026.py`;
`theory_2026/first_principles/sec10_canonical_analysis.py`.

## Parameter dictionary (verified by limit-matching in-script)

| canonical ADM `L = N√h[K_ijK^ij − λK² + ξR3 + η a²]` | maps to |
|---|---|
| `λ` (the `K²` / Horava param; GR at `λ=1`) | `= lam_K` (task health param) `= 1 + lam2` (routeA) |
| `η` (the `a²` coupling) | `= alph` (routeA) `= alpha_khrono`; MOND locus `η(y) = 2 e^-y` |
| `ξ` (the `R3` / tensor-gradient coeff) | `= 1` **locked by the single 4D `R`** |
| `β` (any `K_ijK^ij` deformation) | `= 0` (none) ⇒ `c_T = 1` |

---

## G1 — `c_T = 1`  ·  PASS [PROVEN]

Derived the TT quadratic action from the ADM pieces: on transverse-traceless `h_ij`, `K = 0` and
`a_i = 0`, so `λK²` and `η a²` vanish **identically**. Only `K_ijK^ij` (time-kinetic, coeff 1/4 > 0,
no tensor ghost) and `ξ R3` (gradient) survive ⇒ **`c_T² = ξ`**. Because the single 4D Ricci scalar
`R` supplies `K_ijK^ij` and `R3` with the *same* unit coefficient, **`ξ = 1` exactly, for all `lam_K`
and all `eta`.**

- **`c_T = 1` exactly (`|c_T − 1| = 0 < 1e-15`, GW170817-safe).**
- **`beta` forced value: `beta = 0`** — there is no independent `K_ijK^ij` deformation; the tensor
  speed rides on `ξ = 1` locked by the 4D `R`. (The prompt's `c_T² = 1/(1−β)` refers to a
  `K_ijK^ij`-deformation `β` that this single-metric action simply does not contain.)

## G2 — Khronon health  ·  PASS [COMPUTATIONALLY_VERIFIED] + PARTIAL (strong coupling)

Re-derived the scalar quadratic action (BPS-validated route): with `N=1+α`, `N_i=∂_i B`,
`h_ij=(1+2ζ)δ_ij`, both `α` and `B` are non-dynamical (constraints). Eliminating them:

- **Khronon kinetic coefficient `K_s = 2(1−3λ)/(1−λ)`.**
- **`c_s² = ξ(2ξ−η)(1−λ)/[η(1−3λ)]`; at `ξ=1`: `c_s² = (2−η)(λ−1)/[η(3λ−1)]`.**
- GR reproduced: at `η=0` the `α`-constraint forces `ζ=0` (GR has no scalar mode) — so the mode
  found is genuinely the Lorentz-violating one.

Health conditions:
- **No ghost `K_s > 0` ⟺ `lam_K > 1` or `lam_K < 1/3`.**
- **No gradient instability `c_s² ≥ 0` ⟺ `0 < η < 2`** (with that `λ` window).

MOND-locus running coupling `η(y) = 2 e^-y ∈ (0,2]` for all `y > 0` (`=2` only at the deep-MOND
point `y=0`, where `c_s²=0` marginally). So for **`lam_K > 1` (or `< 1/3`) the khronon is
classically HEALTHY at every `y > 0`** (`K_s > 0`, `c_s² > 0`).

**Healthy `lam_K` range:** `lam_K > 1` **or** `lam_K < 1/3`. Intersecting the BBN bound
`lam_K ∈ [0.923, 1.100]` (the `<1/3` branch is BBN-excluded) narrows the physical window to
**`1 < lam_K ≤ 1.100`** — narrow but nonempty.

**PARTIAL / the sharpest open worry (genuine-mode vs strong-coupling):** as `η → 0` in the Solar
System (`y` large), `c_s² → +∞` — not a ghost or gradient instability (both stay healthy) but an
**instantaneous / elliptic mode**. This is the known BPS strong-coupling corner: the EFT
strong-coupling scale falls with `η` and **is not computed here.** If it drops below Solar-System
scales, the perturbative screening (G3) needs a nonlinear (Vainshtein-type) justification. Honest
label: PARTIAL. This is the one uncomputed gate that keeps the overall verdict *conditional*.

## G3 — Self-screening of `alpha_1, alpha_2`  ·  PASS [COMPUTATIONALLY_VERIFIED] + kernel caveat

Using the BPS-anchored, GR-validated routeA formulas (`alpha_1 = -4α/(1−α/2)`,
`alpha_2 = α(α−lam2)/(2 lam2)`, both re-validated against the committed rationals, e.g.
`alpha_1(α=1/1000) = −8/1999`), with `α = η = 2 e^-y` and `lam2 = lam_K − 1` at the healthy value:

- **`alpha_1 = −8 e^-y`**, **`alpha_2 ≈ −e^-y`** (`= e^-y(2e^-y − lam2)/lam2 ~ −e^-y` for `lam2 ≫ e^-y`).
- Solar System `y ~ 6e4–3e12` ⇒ `e^-y < 1e-30000` (underflows every float inside ~100 AU):
  `|alpha_1| < 4e-5` (LLR/pulsars) and `|alpha_2| < 1.2e-7` (solar spin axis) passed by ~`1e30000`.

**CRUCIAL make-or-break cross-check — does the constant `lam_K` (`θ²`) generate its OWN unscreened
`alpha`?** NO. Setting `α = 0` with `lam2 ≠ 0` (the `θ²` term present, MOND coupling off) gives
**`alpha_1 = 0` AND `alpha_2 = 0` exactly.** Both alphas are *strictly proportional to the `a²`
coupling `α = 2 e^-y`; the `θ²/K²` deformation enters only the `c_s²` and `alpha_2` denominators,
never as an independent `O(1)`/`O(lam_K)` preferred-frame source.** The screening is real, not a
`lam2=0` vacuous zero (negative control NC3 confirms the alphas are nonzero when MOND is on).

**BOTH-WAYS KERNEL CAVEAT (framework rule 4):** the `1e30000` pass is a property of the theory's
*own frozen exponential* kernel `mu = 1−e^-y`. The framework's *phenomenological power-law* RAR
kernel `g_obs = √(g_bar² + g_bar·a0)` has `1−mu ~ 1/(2y)`, giving `|alpha_2| ~ 1/(2y) ≈ 7×10⁻⁶` at
Neptune — **~60× OVER the `1.2e-7` bound.** So the screening verdict is **kernel-dependent**: only
the exponential kernel screens hard. (Additionally, standard PPN assumes *constant* alphas while
`alpha(y)` is position-dependent, so the bound assignment is itself open.) For the theory *as
specified* (frozen exponential) G3 passes; if the physical interpolation is forced to the power-law
RAR shape, the preferred-frame gate is in tension.

## G4 — Lensing  ·  PASS [COMPUTATIONALLY_VERIFIED]

Reusing routeA's static ADM reduction [S1a–c]: the `ψ`-equation is `∇²(Φ+ψ) = 0`, solved by
`ψ = −Φ` ⇒ **`Ψ = Φ` (no slip, `gamma_PPN = 1`), sourced by the single-metric GR sector alone**
(khronon/MOND-independent). The MOND sector adds `div[mu_eff ∇Φ] = 4πGρ` with `mu_eff = mu(y)`, and
since `Ψ = Φ` **both potentials obey the same MOND-boosted equation** ⇒ `g_lens = g_dyn =`
`mu`-enhanced (deep-MOND boost `1/mu > 1`). This is **not** the factor-2 *under*-lensing that killed
TTA-1 (which tied `Ψ` to the un-boosted `chi·Φ' = g_N`).

## G5 — DOF count  ·  PASS [PROVEN]

Khronometric Dirac count (committed `dirac_chi_Q` PART H; `sec10_canonical_analysis`):
`N_local = (20 − 12 − 2)/2 = 3 = 2 tensor + 1 khronon`. `H_perp` is **second class** (the khronon
breaks time diffeos) — this is **Horava-class and expected/healthy**, not the pathology of a demoted
first-class constraint. The spatial momentum constraints `H_i` survive first class. **It is 3 DOF,
not the 2-DOF dream.**

---

## Bottom line

| gate | result | label |
|---|---|---|
| G1 `c_T = 1` | `c_T = 1` exact; `β = 0`; `ξ = 1` locked by 4D `R` | **PASS / PROVEN** |
| G2 khronon health | `K_s>0` & `c_s²>0` for `lam_K>1` (or `<1/3`), `η∈(0,2)`; BBN ⇒ `1<lam_K≤1.10` | **PASS / COMP-VERIFIED** + PARTIAL (uncomputed strong-coupling scale as `η→0`) |
| G3 self-screening | `alpha_1=−8e^-y`, `alpha_2~−e^-y`, ∝ `α` only; constant-`lam_K` sources zero | **PASS / COMP-VERIFIED** + kernel-dependent (power-law RAR kernel → `alpha_2~7e-6` at Neptune) |
| G4 lensing | `Ψ=Φ`, `γ_PPN=1`, both potentials MOND-boosted (no TTA-1 under-lensing) | **PASS / COMP-VERIFIED** |
| G5 DOF | `N_local = 3` (2 tensor + 1 khronon), `H_perp` second class | **PASS / PROVEN** |

**Healthy `lam_K`:** `> 1` (or `< 1/3`); BBN-narrowed to `(1, 1.100]`. **`beta = 0`
(⇒ `c_T = 1`).** `c_s² = (2−η)(lam_K−1)/[η(3 lam_K−1)]`, superluminal-and-safe (Cherenkov OK under a
preferred frame), `→ +∞` in the Solar-System `η→0` corner.

**Not fabricated as a clean pass.** Two honest deductions against interest are carried in the verdict:
(1) the Solar-System strong-coupling scale is uncomputed — the perturbative screening rests on it;
(2) the `e^-y` screening is a property of the frozen exponential kernel and does **not** survive the
framework's power-law RAR kernel. The theory is coherent and passes all five posed gates, but it is
`3 DOF` and its "viable" status is conditional on those two items.
