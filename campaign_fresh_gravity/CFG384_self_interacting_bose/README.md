# CFG384: can a self-interaction λ|Φ|⁴ relax the ~eV cold fluid to CFG383's condensate split? MARGINAL

Criteria in FROZEN_CRITERIA.md. Script `cfg384_si_bose.py`: 2/2 checks.

**MUTATE FAILS and is kept.** Removing the Bose enhancement shrinks the window by 0.59 dex, not the frozen > 1 dex. The degeneracy in clusters is only about 5, so the frozen threshold was set too high.

**Result (g = 1, m = 0.62–1.04 eV).**
- Relaxation within the age needs λ ≥ 2.4e-11 to 1.4e-10.
- The Bullet bound (σ/m < 1 cm²/g) allows λ ≤ 2.1e-11 to 4.6e-11.
- The window is closed by 0.05 dex (×1.3 in σ) at 0.62 eV and by 0.5 dex at 1.04 eV, so the frozen verdict is MARGINAL.
- With particle + antiparticle (g = 2) it is open by 0.04–0.10 dex at 0.62–0.66 eV.
- The dust and Jeans gates (G3) are far from binding (λ up to about 1e-4 allowed).
- At the Bullet-limit coupling, the Milky Way relaxes about 8e4 times per Hubble time, so galaxies relax easily; clusters are the bottleneck.

**Reading.**
- A self-interacting ~0.6–0.7 eV field sits right at the edge: relaxed in clusters only if σ/m ≈ 1 cm²/g, the classical Bullet limit.
- That is a sharp, falsifiable statement. Cluster-merger and halo-shape limits that tighten to σ/m ≲ 0.5 cm²/g would close it.
- It inherits CFG383's caveats (next section).

**CFG383 caveats (from the CFG382 target audit, f982f4a34).**
- m is a calibration, not a test: the "half-unsettled cluster" target moves 0.41 → 0.91 over hydrostatic bias b = 0 → 0.3.
- The condensate picture gives groups only 3% unsettled and UFDs about 0. The bias-robust data ordering has groups at about 2× clusters' excess per present baryon, and UFDs measured high.
- So either the excess in groups and UFDs is not "unsettled fluid" (it is baryon depletion and history, as in CFG338/344), or the split fails there.

κ = ½ is fitted. The cold fluid's amount is not derived.
