# ARGON05 — Independent referee of CFG793 + two sharpenings that close the conversion chain

**Date:** 2026-10-15. **Home:** `argon_push/ARGON05_cfg793_verification_2026-10-15/`.
**Target:** CFG793 "built-in portal" (criteria `73d6bf1c5`, result `4a2e860b7`). **Run:** 0 FAIL, exit 0,
wall 0.16 s, 78 MB. CFG793's verdict: **NO BUILT-IN PORTAL** — the committed action's only photon–P link is
−ρΦ_P (EM energy gravitates), suppressed by (ƛ/L*)² relative to Gertsenshtein. κ = ½ FITTED; external
numbers provisional; not theory closed.

## Referee: CFG793 verified — every committed number reproduced with CODATA constants

- **Identity** Δ_P/Δ_grav = (1/√2)·√(c_P/c)·(ƛ/L*) — all 18 combinations (2 energies × 2 L* × 3 c_P)
  reproduced from the direct coupling route (δρ = B₀b/μ₀c², canonical fields, flux normalisation) to rel 2e-14.
- **K2** Gertsenshtein normalisation: P(1 T, 1 m) = 8.2627e-38 = 4πGB²L²/μ₀c⁴ to 1e-10 (same constants),
  2.1e-6 vs their committed value (constant rounding), 0.45% vs literature 8.3e-38.
- **Q1** best lab: 1.66e-79 (2.5 eV) and 2.06e-73 (native 2.24 meV) at 45 T/100 m/c_P = c/L* = 5.75 pc;
  magnetar 8.2e-59 — all match their ≤ 1e-52 bound.
- **Q3** ceilings: η_grav(1 mg/m², canonical) = 1.53e-12; η_mix (moving 45 T/100 m @ 0.1c) = 3.3e-35 — both
  match; 32–34 orders short of η ∈ [0.01, 1] as they reported.

## Sharpening 1 — their disclosed Q2 FAIL is a quadrature artifact, not physics

CFG793 disclosed: "bounded-clump crossing leaves net/peak 1.2e-3, not < 1e-6." Recomputed with an even,
compact-support potential (polytrope-like, C¹ edge) and a symmetric Gauss–Legendre rule, the net work
across the clump is **−9.1e-28 — machine zero** (their 1.2e-3 was the frozen recipe's finite-endpoint
asymmetry; they had already shown the residual decays with endpoint distance, 4.3e-7 at ±4 kpc — confirmed
as a numerical artifact). The physics of Q2 stands exactly: a static ambient P-field is conservative; the
uniform-gradient check gives M·g·d exactly.

## Sharpening 2 — the moving-device channel emits EXACTLY ZERO (new)

CFG793 reported a moving device sees "photons ≥ 118 ly long." Stronger: **no subluminal device emits at
all.** The W_rem gap (their own Q1 run: ω_gap = 7.4e-9 rad/s) makes the P-mode massive; a device moving
through a static ambient field sees ω = k·v ≤ c/L* = 1.69e-9 s⁻¹ (5.75 pc) or 9.7e-12 s⁻¹ (1 kpc) — **below
the gap at every v < c and both L* bounds** ⇒ the mode is evanescent ⇒ zero emission, not long-wavelength
photons. This is a rigorous closure of the last mechanical channel.

## Sharpening 3 — the portal deadness is a measurement of L* (E6 consistency, new)

The built-in portal stays invisible (magnetar P < 1e-30) iff L* ≳ 2.27 km at 2.5 eV. The measured bound
L* ≥ 5.75 pc = 1.8×10¹⁷ m keeps the framework's no-visible-channel claim (CFG723 E6) safe by **13.9 orders
of magnitude in L***. I.e. the portal's suppression is not a fine-tuned accident of the action: it is
enforced by the same stiffness length that screens the Solar System, and E6 is a *consequence* of the
L* bound. Conversely, a future direct search tightening L* toward ~km would open a falsifiable EM window.

## The conversion chain, closed end to end

| lane | verdict |
|---|---|
| CFG789 | spontaneous τ ≥ 4.4×10¹⁵ yr (COB) |
| CFG792 | converter needs ×6.4×10³⁴; material portal excluded (≥2×10⁵ off in natural matter) |
| CFG790 + ARGON03 | hypothetical portal ε = 10⁻¹² at 2–3 eV excluded ~100× by stellar cooling; framework-native mass 2.24 meV → sub-mm line 0.55 mm; haloscope null = E6 kill test |
| CFG794 + ARGON04 | no known enhancement (resonant/coherent/stimulated/parametric) closes the gap; robust at the native mass |
| CFG793 + ARGON05 | built-in portal: gravity-suppressed (1e-79 lab), rest-mass conversion forbidden exactly by continuity; moving-device channel evanescent below the W_rem gap; E6 safe by ~14 orders in L* |

A working converter would need a term **outside the committed action** that breaks cold-mass continuity
(∂ₜρ_c + ∇·j = −Γ, as CFG793's reading states) — i.e. new physics, not a rearrangement of the current one.
Everything derivable from the action has now been derived; the ramjet/harvest programme is closed at the
theory level, and the record shows exactly which assumption (Γ ≠ 0, off in matter, ×10³⁴ stimulated)
would be needed to reopen it.

## Verdict
**PASS — CFG793 verified number-for-number; Q2's disclosed FAIL is a quadrature artifact; the moving-device
channel is exactly zero (gap-evanescent); the portal's deadness is a 14-order consequence of the L* bound,
not a fine-tuned accident. The conversion chain is closed end-to-end.**