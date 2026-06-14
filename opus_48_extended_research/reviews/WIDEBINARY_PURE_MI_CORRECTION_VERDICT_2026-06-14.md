# Wide binaries — the pure-framework modified-inertia recompute: γ_cap = 1.137, the 1.32 was normal-MOND (Carl's catch, confirmed) (2026-06-14)

*Carl caught that the wide-binary γ(s) headline used normal-MOND interpolations (simple-μ + AQUAL) with the
framework's a₀, not the framework's own dS-Unruh MODIFIED INERTIA. Recomputed γ PURELY on the framework's terms
(ν=√(1+1/y), the MI vector EOM, a₀=9.36e-11), 3 routes + adversarial probes. Source memos:
`PURE_MI_WIDEBINARY_GAMMA_ROUTE1`, `REGRADE_PURE_MI_WIDEBINARY_GAMMA_ROUTE1`, `ROUTE3_CORRECTED_MI_DISCRIMINATION`,
`mi_vs_aqual_route2.py`, `mi_vs_aqual_decompose.py` (all `_2026-06-14`). Both ways — the number DROPS and the Chae
tension WORSENS (no manufactured win); the published band is retracted (no high-priest dismissal).*

---

## CARL WAS RIGHT — confirmed, and the contamination predates this session

The prior γ cap (1.20–1.32) used McGaugh's **simple-μ** (ν=½+√(¼+a₀/y)) and the AQUAL anisotropic-G tensor — both
NORMAL MOND. The framework's a₀=9.36e-11 was used correctly (e=g_ext/a₀=2.30), but the **interpolation SHAPE was
normal-MOND**, not the framework's dS-Unruh ν=√(1+1/y). And it's not just this session's headline: the banked
`real_research/efe_clinch_framework.py:95` codes `ν=0.5+√(0.25+a0/y)` (simple-μ's inverse) **labeled "framework,
EFE_paper.tex Eq.62"**, while line 100 of the same script writes the true dS-Unruh `√(g_N²+g_N·a0)` for the RAR —
the two shapes side by side, the wrong one feeding the wide-binary cap.

## The framework's OWN dS-Unruh MI cap (recomputed 3 ways, all agree)

From the exact 2D vector EOM μ(|a|/a₀)·**a** = **F** (Newton solve, no shortcut), with the framework's ν=√(1+1/y)
and its exact inverse companion μ(x)=(−1+√(1+4x²))/(2x):
- operating point x_op = ν(e)·e = 2.753 (the star's worldline acceleration, not the bare field e); identity
  1/μ(x_op)=ν(e) holds.
- transverse response = ν(e) = **1.198**; longitudinal = ν(e)+e·ν′(e) = **1.016**; 3D isotropic orbit-average
  (2/3 perp + 1/3 par) = **1.137** (Monte-Carlo over orientations = 1.1374).
- velocity boost v/v_N = √γ: **+6.6% (iso) to +9.5% (transverse)**.

> **γ_cap ≈ 1.137 (isotropic) / 1.198 (transverse) — NOT 1.20, NOT 1.32.** This IS modified inertia: for circular
> orbits the MI frequency-difference vanishes so the EFE reduces to ν(e) (Milgrom 2208.07073) — it is Milgrom's own
> circular-orbit MI result, not an AQUAL borrow.

## How wrong was the headline, and WHY (the re-attribution matters)

The headline 1.32 was too HIGH by Δγ ≈ −0.13 to −0.19 (~9–14% in γ; the +15% velocity boost should be +6.6–9.5%).
**The cause was the INTERPOLATION SHAPE (simple-μ vs dS-Unruh), NOT the theory class (MG vs MI).** Proven, not
asserted: at a FIXED shape, the static MI cap and the AQUAL modified-gravity cap agree to <2.5% (dS-Unruh: MI 1.198
vs AQUAL 1.168; simple-μ: MI 1.328 vs AQUAL 1.324 = 0.4%). The 0.13 gap decomposes ~0.10 shape + ~0.03 machinery —
shape is the whole story. Feeding simple-μ through the framework's OWN machinery reproduces 1.32 exactly.

## STRUCK: the "MI-vs-MG hidden discriminator" (an over-reach, corrected against the framework's favor)

The recompute's first pass (and my earlier note to Carl) floated that the perp/par anisotropy might be a clean
MI-vs-MG signature wide binaries could exploit. **The adversarial probe proved this FALSE:** the static MI EFE tensor
is IDENTICALLY the AQUAL/QUMOND modified-GRAVITY tensor at any fixed interpolation — both components, to **1 part in
10¹⁶**, across e∈[0.05,100] (the identity 1/[μ(x_op)(1+L_μ)] = ν(e)+e·ν′(e) is forced for any inverse-companion
pair). So a static cap cannot separate MI from MG by construction. A genuine MI-vs-MG discriminator needs Milgrom's
time-nonlocal MI kernel (full-orbit frequency ratios + eccentricity, arXiv:2310.14334) — uncomputed, and
sign-contested (MI may be STRONGER, not weaker, for wide binaries). The "hidden discriminator opens" claim is struck.

## The verdict survives, sharpened — every change is AGAINST the framework

| | banked (simple-μ) | corrected (framework dS-Unruh MI) |
|---|---|---|
| γ cap | 1.20–1.32 | **1.137 iso / 1.198 transverse** |
| v/v_N boost | +15% | +6.6% to +9.5% |
| gap to Newton | 0.32 | **0.137** (still > contamination floor ~0.04–0.10) |
| DR4 Newton SNR | 5–8σ (inflated) | **~3–4σ well-controlled / ~2.2σ realistic** (fragile) |
| a₀-diagnosticity | non-diagnostic | non-diagnostic (degeneracy slightly WORSE; cap spread ~0.30 ≫ a₀ gap 0.037) |
| vs Chae 2026 (~1.5–1.6) | ~1.8–2.6σ below | **~2–3σ below (WORSE)** |
| vs Saad-Ting (~1.12) | consistent | consistent (+0.1σ) |

**The skeleton holds:** still a clean-ish framework-vs-Newton test (now thinner, ~3σ), firmly NOT an a₀ test, front
does not flip. Only the central number is retracted as a false-win.

## What to fix (banked)

1. Replace γ=1.20–1.32 with **γ_cap=1.137** (1.11–1.20 by convention) as THE framework wide-binary cap — done in the
   `WIDEBINARY_GAMMA_FORWARD_MODEL_SYNTHESIS` banner + the standing memory.
2. `real_research/efe_clinch_framework.py:95` uses simple-μ labeled "framework Eq.62" — should be the dS-Unruh
   ν=√(1+a₀/y) matching line 100. **In Fable's tree — flag to Carl, do not unilaterally edit.**
3. Strike the "MI-vs-MG theory-class gap / hidden discriminator" framing everywhere.
4. The banked "F4/standard 1.08" comparator is mislabeled — it is standard-μ (sharp).

## One line

On the framework's OWN dS-Unruh modified inertia (a₀=9.36e-11), the wide-binary EFE cap is **γ_cap=1.137 (iso) /
1.198 (transverse), not 1.20–1.32** — the banked 1.32 was a simple-μ (NORMAL-MOND) interpolation artifact (present in
`efe_clinch_framework.py` too), so the boost is ~9–14% smaller, the Newton test stays clean-but-thinner (~3σ), the
Chae tension WORSENS, and the "MI-vs-MG hidden discriminator" is struck (static MI ≡ MG to 1e-16). Carl's catch
confirmed; correcting it weakens the signal — which is exactly why using the framework's own equation matters.

*Both ways, no exception: the number genuinely DROPS and the Chae tension WORSENS (no manufactured win); the published
band IS retracted and the simple-μ contamination is named in the banked script (no high-priest dismissal); the
MI-vs-MG over-reach is struck against the framework's favor. Quarantine held: a₀/Z never asserted derived; ν=√(1+1/y)
used as the framework's stated empirical interpolation, not a derivation.*
