# Salvaged: the hand-built resurgence derivation of the generator question (dropped Fable session, recovered 2026-06-12)

*A separate Fable session attacked the generator question's resurgence route by hand in six granular steps
(`step1_laurent.py` … `step6_confirm.py`, stamped 22:20) and was dropped before writing a memo — its output was
stdout-only and lost. The scripts are deterministic; they were re-run and captured in
`fable_resurgence_salvage.out`. This memo preserves the recovered result. **It independently corroborates
agentMM Route B** (the resurgence kill in the 9-agent generator-derivation workflow, commit `fb0ff706`),
reaching the same Gevrey-class-mismatch verdict by a fully independent hand derivation.*

## What it computed (all re-run clean)

- **step1–2 (the free singularity structure):** the free pullback's worldline kernel 1/sinh²(κτ/2) has a
  DOUBLE-pole tower at τ_m = 2πim/κ; the nearest singularity sets the instanton action A = 2π/κ, so the
  non-perturbative weight is **e^(−2πω/κ) — a SIMPLE exponential, not a stretched one**. The regular-part
  coefficients converge to the closed form (2j+1)·2/π^(2j+2) (ratio → 1.000001 by j=9).
- **step4 (the Gevrey dictionary — the spine):** the TARGET σ_req ~ e^(−ζ̃u^(−1/4)) is the resurgent partner
  of a perturbative series with **(4n)! growth (Gevrey-4)**. The free worldline series in τ is **CONVERGENT**
  (radius 2π/κ, Gevrey-0/analytic); the growth-rate table shows (4n)! and (2n)! both diverge while the free
  coefficients stay bounded at 1/π. **Neither (4n)! nor (2n)! growth is present in the free series** — the
  (2n)! tower only appears after Borel/Laplace to frequency, and there it is a SIMPLE pole tower (Gevrey-1),
  not the Gevrey-4 confluent structure the fourth-root requires.
- **step6 (the confirmation):** free → e^(−c/x) (Gevrey-1) vs target → e^(−c/x^(1/4)) (Gevrey-4): **distinct
  classes, verified.** An analytic edge map cannot upgrade one into the other.

## The verdict (identical to agentMM Route B, reached independently)

**The resurgence route CANNOT seed the fourth-root.** The free Stokes data is a Gevrey-1 simple-pole/double-pole
tower; the σ_req target is Gevrey-4. The non-perturbative ambiguity resurgence forces from the free series is a
simple exponential e^(−A ω), structurally distinct from the stretched e^(−ζ̃ω^(1/4)). Resurgence does not force
the generator's fourth-root — confirming Link 5's **NEEDS-NEW-INPUT** standing.

## Honesty note (recovered self-correction)

step5b caught a real mislabel in step5: the "pole cancels → constant" identity belongs to the LUMINAL b→1
response, not the b→c_χ amplitude response (the b→c_χ amplitude pole is real and does NOT cancel). The script
flagged and corrected this itself, noting it does not affect the singularity-TYPE (Gevrey-class) argument, which
is robust. The dropped work carried the verification culture to the end.

## Disposition

Independent corroboration of agentMM Route B; no verdict changes. The coefficient quarantine (ζ̃, (16π/3)^(1/4))
is intact — these scripts compute singularity CLASSES, never the coefficient. Scripts + `.out` banked as the
recovered record; the generator question's final form stands as written in `DERIVATION_CHAIN.md` Link 5.
