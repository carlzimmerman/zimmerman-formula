# L88 — The GW door: tensor speed c_T and scalar polarization of the F(Q)Θ action

**Lane:** L88 (support role). **Script:** `L88_gw_polarization.py` → `L88_gw_polarization.out` (21/21 PASS, ~0.5 s).
Self-contained sympy/numpy; imports nothing from `qwen_claude_field_theory/` (astra's
`ω₀² = Q₀²G''(y₀)/2` and `G''(y)` are re-derived here). Both a₀ footings on every dimensional number.

## The action under test (verified/committed, L80)

S = ∫√−g [ M²/2 R − ΛM² − K(Q) + F(Q)Θ + M²a₀²G(|V|/a₀) ] + S_m[ψ, g],
with Θ = ∇·n (n = clock unit vector), Q = n·∂φ, V_μ = q_μ^ν ∂_νφ, G(y) = y² + 2(1+y)e^{−y} − 2.
The graviton term is **pure Einstein–Hilbert** M²/2 R. astra's ADM principal gate
(`.../fqtheta_clock_dust_2026/ACTUAL_PRINCIPAL_GATE.md`) finds the scalar propagates with characteristic
frequency **ω₀² = Q₀²G''(y₀)/2** — a massive mode for y₀>0, degenerate (massless, strongly coupled) at the
cosmological zero-field point y₀=0 — and G''(y) = 2[1+(y−1)e^{−y}] ≥ 0 (fable L80/L83).

## 1. Tensor speed — P12: **c_T = c EXACTLY. SOLID.**

Symbolically verified on the Minkowski TT plane wave (g_xx=1+εh₊, g_yy=1−εh₊, g_xy=εh_×):

- **C1/C1b (control):** the linearized Einstein–Hilbert equation gives δR_xx = −½(∂_z²−∂_t²)h₊ and the same
  wave operator for h_× → vacuum eq ∂_t²h = ∂_z²h → **c_T² = 1**, two polarizations {+,×}.
- On the TT wave the clock stays n^μ=(1,0,0,0) (h_00=h_0i=0), φ=φ(t) is homogeneous, so:
  - √−g = √(1−ε²(h₊²+h_×²)) — **no linear-in-h term** (TT is traceless) → scalar terms give no linear
    graviton source (M1a).
  - Q = n·∂φ = φ̇ is **h-independent** → K(Q)√−g is a mass term only; EOM contribution has no h_tt/h_zz (M1d).
  - Θ = ∂_t ln√−g = −½∂_t(h₊²+h_×²) is O(h²) and a **pure total time-derivative** → F(Q)Θ contributes
    **nothing** to the graviton EOM (a phantom φ̈ mass term at most), no kinetic piece (M1b/M1e).
  - Λ M² term → de-Sitter-scale graviton **mass**, not a c_T shift (M1c).
  - MOND term M²a₀²G(|V|/a₀) = 0 identically (|V| = transverse gradient of φ(t) = 0; G(0)=0) (M1f).

So M²/2 R is the **sole** kinetic term for the TT graviton → c_T = c exactly, no dispersion, 2 polarizations.
**GW170817 (|c_T/c−1| < ~10⁻¹⁵) is passed structurally**, footing-independent. This *sharpens* P12 from the
explicit action. Confidence **HIGH**.

## 2. Scalar mode — mass scale and screening

**Mass scale.** ω₀ = Q₀√(G''(y₀)/2). Deep-Newtonian/detector regime y₀≫1 → G''→2 → ω₀ = Q₀; cosmological
zero-field y₀→0 → G''→0 → ω₀→0 (massless, strongly coupled). Tying Q₀ to the de Sitter clock rate
H_Λ = 2π a₀/c (a₀ = c²/2πL_dS, L78):

| footing | H_Λ [1/s] | m_φc² [eV] | reduced λ_C = c/H_Λ (= de Sitter radius) | mass-gap f_gap [Hz] |
|---|---|---|---|---|
| canonical a₀=9.3619e−11 | 1.962e−18 | **1.29e−33** | 1.53e26 m ≈ **4.95 Gpc** | 3.12e−19 |
| alternate a₀=1.1279e−10 | 2.364e−18 | **1.56e−33** | 1.27e26 m ≈ **4.11 Gpc** | 3.76e−19 |

The scalar's Compton wavelength **is** the de Sitter radius. m_φc² ~ 10⁻³³ eV — the same de-Sitter/Hubble
scale as the Λ-induced graviton mass.

**Yukawa screening — adversarial, and the answer is NO.** At every GW band the frequency is far above the
mass gap: f/f_gap ≈ **9.6×10⁹ (PTA), 3.2×10¹⁵ (LISA), 3.2×10²⁰ (LVK)**. A mode this far above its gap
propagates luminally (group velocity → c); Yukawa evanescence applies only to quasi-static fields at
r > λ_C. **"massive ⇒ screened" is FALSE here.** To screen even the lowest (PTA) band the clock rate Q₀
would have to exceed H_Λ by ~10¹⁰× — implausible for a cosmological clock. So the scalar is **robustly
effectively massless at all GW detector bands.**

**Coupling — clean protections vs the honest residual.**
- **Clean (M4a):** no φR non-minimal term → the scalar does **not** mix into the TT graviton at linear order;
  the two tensor modes are pure GR.
- **Clean (M4b):** ordinary matter S_m[ψ,g] is minimally coupled (∂S_m/∂φ = ∂S_m/∂n = 0) → astrophysical GW
  sources carry **no scalar charge** → no scalar monopole/dipole radiation at linear order (unlike
  Brans–Dicke, where matter has scalar charge via φR). Scalar emission is only metric-mediated.
- **Honest residual (M4c):** F(Q)Θ (Θ = ∇·n) **does** couple the clock into the metric-*scalar* sector — that
  is exactly how it builds the MOND potential Φ — so the transverse-breathing channel is **not identically
  closed**. The radiation-zone amplitude ∝ F_Q is uncomputed.
- **(M4d):** astra's k→0 symplectic collapse (Ω_ζπ ∝ k², L83) suppresses the scalar only at *super-horizon*
  (cosmological) k, **not** at detector-band k (LVK k~2×10⁻⁶/m, PTA k~10⁻²⁵/m are nowhere near k→0). It does
  **not** protect the detector band.

## 3. Falsifiable statement — P13 (restated honestly)

P13 as written ("no scalar breathing mode, contingent on a non-propagating cuscuton") is **not delivered by
astra's current gate and should be restated**: the gate finds the scalar *propagates* (one local DOF for
generic k), so the cuscuton premise is **contradicted**, and the de-Sitter-scale mass does **not**
Yukawa-screen it at any band.

> **The framework predicts a subdominant, gravitationally-sourced scalar GW polarization (transverse
> breathing ± longitudinal), NOT Yukawa-screened (effectively massless at all bands, mass gap ~3×10⁻¹⁹ Hz),
> whose amplitude relative to the tensor modes is set by the F(Q)Θ coupling F_Q. It is NOT a clean "no scalar
> mode."**

Discriminators:
- Detection of an extra polarization consistent with a massless-to-de-Sitter-mass scalar → **consistent** with
  the propagating clock scalar (and would fix F_Q).
- A confirmed pure-tensor result (only {+,×}) at improving PTA/LVK/LISA polarization sensitivity → drives F_Q
  down / pressures the F(Q)Θ metric-scalar mixing.
- Scalar speed ~ c (near-luminal at high ω; astra P12 c_T=c) → **no gravitational Cherenkov violation**,
  unlike sub-luminal khronon modes.

**Consistency with current bounds:** LVK GWTC polarization tests and PTA (NANOGrav 15yr / EPTA) correlation
analyses do not require extra polarizations and set only weak upper limits on scalar/longitudinal admixtures,
so a subdominant scalar mode is **presently allowed** — no current tension, no current detection.

## Verdicts and confidence

| item | verdict | confidence |
|---|---|---|
| **c_T (P12)** | **c_T = c exactly**, 2 polarizations, GW170817 passed structurally | **HIGH** (structural, symbolic) |
| scalar mass scale | m_φc² ~ 1.3–1.6×10⁻³³ eV (de Sitter scale), λ_C = de Sitter radius (~4–5 Gpc) | MED-HIGH (rests on Q₀~H_Λ) |
| Yukawa screening | **NOT screened** at any GW band (f/f_gap ~ 10¹⁰–10²⁰); effectively massless | HIGH |
| **P13 "no scalar mode"** | **NOT supported as a clean absence** → suppressed, near-luminal, effectively-massless scalar polarization, amplitude ~ F_Q (uncomputed); currently consistent with data but a genuine falsifiable target | MEDIUM (below current bounds; radiation-zone amplitude is astra's open item) |

**Net:** the tensor door is clean (P12 solid). The scalar door is *not* the clean null P13 claimed — the honest
prediction is a subdominant, effectively-massless, near-luminal scalar polarization whose amplitude ∝ F_Q is
the live discriminator, presently consistent with (but not required by) PTA/LVK/LISA data. The radiation-zone
amplitude calculation is astra's open item; nothing here modifies files under `qwen_claude_field_theory/`.
