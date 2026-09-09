# L89 — the External Field Effect of the F(Q)Θ clock-MOND completion

`L89_external_field_effect.py` + `.out` (**15 checks, 15 PASS**, exit 0). The EFE is the sharpest
MOND-vs-dark-matter discriminator: a nonlinear MOND theory violates the strong equivalence principle
(SEP) — a uniform external field partially Newtonises a subsystem's internal dynamics even in free fall —
while cold dark matter produces **zero** such effect. This lane derives the EFE directly from the
F(Q)Θ static equation astra derived and L80 verified, computes the wide-binary and dwarf signals on both
a₀ footings, and confronts the registered DR4 band. Self-contained sympy/numpy; imports nothing from
`qwen_claude_field_theory/`; reads no PREREGISTRATION or `*_HASH` file (registered targets are quoted as
frozen literals).

## The EFE law (derived, not assigned)

From the F(Q)Θ static branch `∇·[(1−e^{−|∇Φ|/a₀})∇Φ] = 4πGρ` (AQUAL with μ(y)=1−e^{−y}), put a uniform
external field **g_ext** along ẑ and linearise in the internal field. The flux Jacobian is computed
symbolically (C1) as `μ_e diag(1,1,q)`, giving the external-field-dominated (EFD) internal equation

```
    μ_e (∂_x² + ∂_y² + q ∂_z²) φ = 4πGρ ,
    μ_e = 1 − e^{−η},   η = g_ext/a₀,   q = 1 + L_e,   L_e = η/(e^η − 1).
```

The point-mass Green function is `φ = −GM/(μ_e√(z²+qR²))` — reproduced here (C2) matching astra's
independently-symbolically-verified `exact_exponential_aqual_efe_kepler_2026` report. The velocity boost
`γ_v² = G_eff/G` is anisotropic:

- **∥ g_ext:** γ_v² = 1/μ_e
- **⊥ g_ext:** γ_v² = 1/(μ_e√q)

**Controls all hold:** C0 the kernel G′(y)/(2y)=1−e^{−y} (reproduces L80(i)); C3 the limits L_e→1, q→2 as
η→0 (standard deep-MOND EFD) and γ_v→1 exactly as η→∞ (full Newtonisation = the DM/GR baseline); C4 the
boost decreases monotonically with g_ext (the physical EFE sign).

## The magnitudes (both footings, g_ext = 1.778e-10 m/s² = 1.90 a₀_can / 1.58 a₀_alt)

| footing | η | μ_e | q | γ_v ∥ | γ_v ⊥ | γ_v orient-avg |
|---|---|---|---|---|---|---|
| canonical | 1.899 | 0.8503 | 1.334 | 1.0845 | 1.0090 | **1.0326** |
| alt | 1.576 | 0.7933 | 1.411 | 1.1228 | 1.0302 | **1.0588** |

The SEP-violation amplitude is **γ_v − 1 ≈ 3.3% (canonical) / 5.9% (alt)**, with an intrinsic
anisotropy of 0.075–0.093 in γ_v between separations parallel and perpendicular to the Galactic-centre
direction.

## Wide binaries — the F(Q)Θ kernel sits BELOW its own registered band (the D1 kernel conflict, quantified)

The registered DR4 **Arm A** (modified-gravity, framework **ν_RAR** kernel, Amdt 10) band is
**1.1614–1.1814 canonical / 1.1917–1.2267 alt**. The F(Q)Θ **exponential** kernel — the one that actually
descends from the completion — predicts only **γ_v ≈ 1.033 / 1.059**, which is **below the Arm A lower edge
by ~0.13 on both footings** (P2b). It lands instead in the **Arm B** covariant-candidate / near-Newton band
(ceilings 1.045 can / 1.03 alt; P2c).

The reason is structural: μ=1−e^{−y} Newtonises faster than ν_RAR at y≈1.9, so its EFD μ_e is closer to 1.
Backing out the effective isotropic μ implied by Arm A gives μ_eff ≈ 0.74, vs the exponential's μ_e ≈ 0.85 —
ν_RAR is "more MOND" at the Galactic field. This is the same **D1 kernel conflict** flagged throughout
FINDINGS (the completion carries the *exponential carrier*, while the registered pipeline and THE_ACTION §3
carry ν_RAR), now made quantitative in the EFE.

**Honest detectability caveat.** γ_v ≈ 1.03–1.06 is only 3–6% above Newton — far weaker than the ν_RAR Arm A
signal (16–23%). DR4 wide binaries are therefore a **weak** discriminator for the exponential kernel:
separating 1.03 from 1.00 at 3σ needs ~10× more deep pairs than separating 1.16 from 1.00. The wide-binary
EFE is, moreover, **observationally contested** — Chae et al. report a MOND-like detection (γ_v ≈ 1.19–1.26)
while Pittordis–Sutherland / Banik analyses lean Newtonian. The F(Q)Θ exponential prediction is
**inconsistent with Chae's central value** (P2d) but **consistent with the Newton-leaning analyses**.

## Dwarf spheroidals — the clean discriminator

The EFE makes a dwarf's internal dynamics depend on its Galactocentric distance R_gc through
g_ext(R_gc) = V_c²/R. For a fiducial dwarf (M_b = 10⁶ M_⊙, r_half = 300 pc) in the EFD regime, the predicted
1-D dispersion rises with R_gc and saturates at the isolated-MOND value:

| R_gc [kpc] | g_ext/a₀ (can) | σ_EFE [km/s] (can) |
|---|---|---|
| 40 | 0.280 | 4.42 |
| 80 | 0.140 | 6.05 |
| 160 | 0.070 | 8.40 |
| 250 | 0.045 | 8.62 (→ σ_iso) |

**σ_EFE varies by a factor ~1.9 across 40→250 kpc** (P3a). Dark matter predicts a **flat** σ(R_gc) — the
dwarf's own halo is blind to the host field. This is the DM-distinguishing signature. As a touchstone,
Crater II (R_gc ≈ 117 kpc): isolated-MOND predicts σ ≈ 6.9 / 7.2 km/s, but the EFE pulls it down to
**≈ 2.4 / 2.6 km/s** against σ_obs ≈ 2.7 km/s — the celebrated MOND EFE success, which the DM reading must
instead attribute to tides/stripping (P3b).

## Crisp falsifiable statement

> **F(Q)Θ predicts a nonzero, kernel-specific EFE (a strong-equivalence-principle violation):** wide-binary
> γ_v ≈ **1.03 (canonical) / 1.06 (alt)** — anisotropic, γ_v(∥) ≈ 1.08–1.12 vs γ_v(⊥) ≈ 1.01–1.03 — and a
> dwarf-spheroidal internal σ that scales ~√R_gc (a **~2× rise** across the satellite distance range, with
> Crater-II-like suppression for dwarfs deep in the MW field). **Dark matter predicts exactly γ_v = 1.000
> and σ independent of R_gc.**

**Where decisively testable.** The **dwarf σ–R_gc correlation** is the cleanest test — a ~2× effect DM has
no mechanism for — needing a controlled sample with measured σ, M_b and R_gc (tides controlled). Wide
binaries chiefly test **which kernel** is right: a confirmed γ_v ≈ 1.2 (Chae / Arm A) would **disfavour the
exponential F(Q)Θ kernel** in favour of ν_RAR; a Newton-leaning DR4 result is consistent with it — but is
too close to Newton to separate the exponential EFE from pure DM.

## Consistency ledger

- **Registered DR4 Arm A (ν_RAR MG, 1.16–1.23):** F(Q)Θ's exponential kernel is **below** it on both
  footings — not consistent; documents the kernel conflict rather than a failure of the EFE machinery.
- **Registered DR4 Arm B (covariant candidate ceilings 1.045/1.03):** **consistent** — the exponential
  prediction lands in this low band.
- **Chae et al. WB EFE detection (γ_v ≈ 1.19–1.26):** **not** consistent with the central value; consistent
  with the contested Newton-leaning analyses.
- **Crater II low σ:** **consistent** — the EFE reproduces the suppression.

## Confidence

**HIGH** on the EFE law and its exponential-kernel magnitude (closed-form; matches astra's independently
verified efe_kepler Green function; C0–C4 controls hold). **HIGH** that it sits below Arm A. **MODERATE** on
the exact orientation-averaged γ_v (the WB pipeline fits a scalar to a 3-D-oriented projected-velocity
distribution). **Flagged, not relitigated:** the anisotropy sign in pure AQUAL-EFD is γ_v(∥) > γ_v(⊥), the
**opposite** of the preregistration's quadrature "derived-EFE" Amendment (which has ∥ < ⊥) — a genuine
convention/prescription difference between the AQUAL static equation and the relativistic-quadrature EFE, not
resolved here. **MODERATE** on the dwarf normalisation (structure constant, MW field model); **HIGH** on the
sign and ~2× scale of the σ–R_gc trend, which is the falsifiable core.

## Scope

Does not touch the open F(Q)Θ health hinge (L80 c_bare² = −1 / astra's ADM Dirac chain), the BBN
fine-tuning (L84/L86), or the near-horizon strong coupling (L82/L83). It establishes only what the *static*
MOND kernel implies for the EFE — a real, sharp, DM-distinguishing prediction whose wide-binary amplitude is
uncomfortably small and whose dwarf signal is the place to look.
