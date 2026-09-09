# L92 — does the F(Q)Θ exponential kernel actually fit SPARC galaxies?

`L92_sparc_rar_fit.py` + `.out` (**12 checks, 12 PASS**, exit 0). Self-contained numpy; reads only the
committed SPARC data (`real_research/data/SPARC_Lelli2016c.mrt` + `sparc_data/*_rotmod.dat`); imports
nothing from `qwen_claude_field_theory/`; reads no PREREGISTRATION or `*_HASH` file; all printed paths are
repo-relative.

## The question

The F(Q)Θ completion's galaxy dynamics descend from its **own** static-branch field equation

```
    4 M² ∇·[ (1 − e^{−|∇Φ|/a₀}) ∇Φ ] = ρ_b ,
```

i.e. an AQUAL law with the **exponential** interpolating function μ(x) = 1 − e^{−x} (the "exponential
carrier", FINDINGS L80/L89). The registered wide-binary pipeline and THE_ACTION §3 instead carry the
empirical **ν_RAR** kernel ν(y) = 1/(1 − e^{−√y}) — the standing **D1 kernel conflict**. L89 showed the
exponential kernel Newtonises *faster* than ν_RAR at the external-field scale. This lane asks the
foundational question the completion must pass regardless of D1: **does the exponential kernel fit actual
rotation curves (the radial acceleration relation), and how does it rank against ν_RAR?**

## Convention (this is the whole point)

μ acts on the **physical** field gradient |∇Φ| = g_obs, so spherically the field equation gives the
algebraic relation

```
    μ(x)·x = y ,   x = g_obs/a₀ ,   y = g_bar/a₀ ,   μ(x) = 1 − e^{−x}.
```

This "μ in the AQUAL variable" reading is the correct one: μ(x) → x as x → 0 gives the right deep-MOND
limit **g_obs → √(a₀ g_bar)**. In spherical symmetry AQUAL ≡ QUMOND, so the "boost ν(y) = x/y with
g_obs = g_bar·ν(y)" reading is **numerically identical** (verified to 1e-16 dex, check A3). The **only**
reading that differs is the naive literal one that evaluates μ at the *baryonic* argument,
g_obs = g_bar/(1 − e^{−g_bar/a₀}); that has the **wrong** deep-MOND limit (g_obs → a₀, a constant) and is
a documentation trap, not a physical kernel (Part D). Both a₀ footings carried throughout
(canonical 9.3619e-11, alt 1.1279e-10 m/s²).

## Controls (Part A — all PASS)

| control | result | target |
|---|---|---|
| A1 carried bounded-boost kernel RAR scatter (pipeline validation) | **0.1453 / 0.1421** dex, med +0.030/+0.003 | L61 committed 0.145/0.142 |
| A2 exponential-carrier canonical RAR scatter | **0.1613** dex | FINDINGS L1087: 0.1613 |
| A3 "AQUAL μ-variable" ≡ "QUMOND ν=x/y boost" | max Δ = 9.6e-17 dex | identical |
| A4 both kernels → √(a₀ g_bar) deep MOND (y≤1e-4) | exp 0.25%, ν_RAR 0.50% | shared asymptote |

The SPARC loader (L61 recipe: Vb² = Vg|Vg| + 0.5·Vd|Vd| + 0.7·Vb|Vb|, mask eV/Vo<0.10 & ≥3 pts) yields
**155 galaxies / 2786 points** and reproduces L61's committed gate number exactly — the machinery is sound.

## The exponential kernel on the full SPARC sample (Parts B, C)

| footing | exp kernel rms | exp median | ν_RAR rms | ν_RAR median | Δ(rms) = exp − ν_RAR |
|---|---|---|---|---|---|
| canonical | **0.1613** | +0.075 | 0.1453 | +0.030 | **+0.0160** |
| alt | **0.1507** | +0.047 | 0.1421 | +0.005 | **+0.0086** |

- The exponential kernel **does fit** the RAR: a MOND-like relation at **zero** per-galaxy parameters,
  rms ≈ 0.15–0.16 dex on both footings (per-galaxy median rms 0.122 vs ν_RAR's 0.104).
- It is **measurably worse than ν_RAR on both footings** (+0.016 canonical, +0.009 alt), but the gap sits
  **inside the ~0.01–0.02 dex "comparable" band** — worse, not a different regime. The carried
  bounded-boost kernel (= *saturated* ν_RAR) equals unsaturated ν_RAR to 3 decimals (0.1453/0.1421),
  confirming saturation is irrelevant on SPARC.
- Cross-check C3: exp and ν_RAR diverge by **0.073 dex** at a point — reproduces the D1 number in FINDINGS
  and confirms the two kernels are genuinely not interchangeable.

## The naive g_bar-variable reading is catastrophic (Part D)

Evaluating μ at the baryonic argument, g_obs = g_bar/(1 − e^{−g_bar/a₀}), gives rms **0.388 / 0.440 dex** —
2.4–2.9× worse — because its deep-MOND limit is g_obs → a₀ (a constant floor), not √(a₀ g_bar). Explicit
probe at y=1e-3: correct √(a₀ g_bar) = 2.96e-12, AQUAL = 2.98e-12, literal = 9.37e-11 (= a₀, wrong by 30×).
**This reading must never be used**; the AQUAL implicit solve is the only correct one.

## BTFR (Part E)

Measured with a proper flat V_flat (largest outer run flat to 10%) on standard cuts (Q<3, inc≥30°),
**139 galaxies**, M/L fixed at 0.5:

- **Slope 3.39** (deep-MOND predicts 4.00). Sub-4 is a fixed-M/L + coarse-V_flat regression effect, not a
  kernel property. Free-fit scatter **0.22 dex** (looser than Lelli 2016's 0.10 dex because M/L is fixed
  with no per-galaxy nuisance — a pipeline systematic, identical for both kernels).
- **Zero-point:** the data's own deep-MOND normalisation is **a₀ = 1.41e-10 m/s²**, within **0.10 dex of
  the alt footing** and 0.18 dex of canonical — MOND-consistent within the fixed-M/L systematic.
- **The BTFR does not discriminate the kernels.** Their largest difference over the BTFR points is 0.073
  dex (and 0.048 dex even over the 92 deep-MOND galaxies that set the zero-point — they converge only as
  y→0), well below the 0.22 dex scatter. The deep-MOND asymptote V⁴ = G M a₀ is *identical* for both
  kernels (A4), so **galaxies cannot decide D1** — the external-field / wide-binary scale (L89) is the only
  handle.

## Verdict

**The foundational galaxy fit holds.** With the correct AQUAL reading the F(Q)Θ exponential kernel fits the
SPARC RAR at zero per-galaxy parameters, rms 0.161/0.151 dex on the two footings, and produces a MOND-like
BTFR whose zero-point recovers a₀ to ~0.1 dex. It is **the poorest of the three MOND kernels tested** —
worse than ν_RAR by +0.016/+0.009 dex — but the gap is within the "comparable" band, so this is a ranking,
not a failure. The BTFR is kernel-blind (both share the deep-MOND limit), so it neither favours nor kills
the exponential carrier; the D1 kernel conflict is decided only at the external-field scale (L89 puts the
exponential's wide-binary γ_v ≈ 1.03–1.06 *below* the registered ν_RAR Arm A band). The naive
g_bar-variable reading of μ = 1−e^{−y} is deep-MOND-broken and is excluded here as a documentation trap.

## Confidence

**HIGH** on the RAR numbers (exponential 0.161/0.151, ν_RAR 0.145/0.142, gap +0.016/+0.009) — the pipeline
reproduces two independently committed cross-checks (L61's 0.145/0.142 and FINDINGS L1087's 0.1613) and the
0.073-dex kernel divergence. **HIGH** that the exponential kernel fits but ranks below ν_RAR. **HIGH** that
the naive g_bar reading is catastrophic and that the BTFR cannot discriminate the kernels. **MODERATE** on
the BTFR slope/scatter absolute values (crude V_flat + fixed M/L inflate the scatter to 0.22 dex vs the
literature's 0.10; the sub-4 slope and 0.1-dex zero-point offset are pipeline systematics, not physics).
Nothing here touches the open F(Q)Θ health hinge (L80/L83), BBN tuning (L84/L86), or the D1 resolution
itself — this lane quantifies D1 on galaxies, it does not relitigate it.
