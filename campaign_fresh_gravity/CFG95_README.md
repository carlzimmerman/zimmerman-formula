# CFG95 — does B's own stellar-mass calibration account for the KiDS early/late split?

- **Criteria:** frozen in `CFG95_FROZEN_CRITERIA.md`, before any number. It was first committed as CFG90 in 32abb6e12 and renumbered in 05a819f04 after a number collision; the criteria are unchanged.
- **Script:** `CFG95_kids_split_own_calibration.py`, about 45 s, both footings.
- **Runs:**
  - The main run passes 9 of 11. H1 and H2 fail, and it exits 1.
  - The MUTATE run (calibration removed) also fails H1 and H2, so for the headline it is uninformative (see Controls).
- **Outputs:** `.out` / `_results.json`, and the `_MUTATE` pair.

## Bottom line

**The KiDS split survives B's own stellar-mass calibration. The calibration reduces the split but does not remove it.**

- **What B's calibration supplies.**
  - B's ATLAS3D dynamics make early-type stellar masses +0.15 dex heavier than their Chabrier catalogue values (α_dyn ≈ 0.80 × Salpeter at the early class's median σ ≈ 170 km/s).
  - SPARC makes discs +0.09 dex heavier.
  - The net differential is only **+0.07 dex**.
- **What the split needs.** Early-type lenses need **0.18–0.5 dex** more baryons than late types for p > 0.05 on the released data, with the best fit near 0.35–0.4 dex. The re-measured data need **0.23–0.5 dex**.
- **The result with the calibration:**

| data | no calibration (CFG61 / CFG88) | with B's calibration, canonical | alt |
|---|---|---|---|
| released split, 1-halo bins | 28.1/7 (3.7σ) | **20.3/7, p = 0.005 (2.8σ)** | 18.6/7 (2.6σ) |
| re-measured split, jackknife covariance | 35.0/7 (4.4σ) | **26.7/7, p = 3.8 × 10⁻⁴ (3.6σ)** | 24.8/7 (3.3σ) |

- **The most favourable case.** Leave the discs at catalogue mass, i.e. no SPARC correction. The released split then reaches p = 0.052, but the re-measured split stays at p = 0.007.
- **What closing it would take.** A differential near 0.35 dex means early-type stellar masses about 2.2× their Chabrier values relative to discs. That is more than a Salpeter IMF (1.78×) for every early type. B's own ATLAS3D dynamics do not support it: α_dyn stays below 1 × Salpeter at every σ below 300 km/s.

## The calibration (as frozen)

- **Early types:**
  - δ_early = log10 α_dyn(σ) + 0.25. α_dyn is refitted here from ATLAS3D (N = 187) with CFG55's `law_mass`. The canonical fit reproduces CFG33 exactly; the alt fit is a = −0.093, b = +0.244.
  - σ comes from an ATLAS3D fit: log σ = 2.219 + 0.279 (log M_Salp − 11), with scatter 0.085 dex.
  - Over the KiDS mass range δ_early runs from +0.08 (log M* 9.5, σ 74 km/s) to +0.20 (log M* 11.5, σ 268 km/s). The M_gal-weighted mean is +0.154.
- **Late types:** δ_late = log10(0.61 / 0.5) = +0.086 (canonical), and log10(0.57 / 0.5) = +0.057 (alt).
- **How it enters the model.** Each lens keeps its measured-mass radius. The law's ΔΣ at the true M_b is interpolated between CFG61's profile nodes, and the true point mass is added.

## Controls

- **C1:** with δ = 0, the stack reproduces CFG61's committed law stacks to 2 × 10⁻¹⁶, and the released χ² equals 28.0727.
- **C2:** the canonical α_dyn fit reproduces CFG33: slope +0.204 and ×0.72 / ×0.83 / ×0.90 at σ = 100 / 200 / 300 km/s.
- **C3:** the log-M_b interpolation matches directly computed profiles at three off-node masses to 3 × 10⁻⁴.
- **MUTATE:** removing the calibration returns CFG61's 28.07/7 and fails H1 and H2, as required. The main run fails them too, so for the headline the control is uninformative; this possibility was declared up front. The machinery check is C1's exact reproduction.

## Reported rows

- **R2, the late-type bracket:**
  - δ_late = 0: released 14.0/7 (p = 0.052); re-measured 19.6/7 (p = 0.007).
  - Reference Υ_3.6 = 0.6: released 14.4 (p = 0.044); re-measured 20.1 (p = 0.005).
- **R3, the Salpeter/Chabrier offset:**
  - 0.30 dex: released 15.2 (p = 0.034); re-measured 21.0 (p = 0.004).
  - 0.20 dex: released 25.9; re-measured 32.7.
- **R4, a constant α at σ = 170 km/s:** 20.3 / 26.6, the same as the σ-dependent calibration.
- **R5, the diagnostic: a uniform differential Δ.**
  - Released: p > 0.0027 for Δ ≥ 0.075; p > 0.05 for Δ ≥ 0.175. The minimum is 3.8/7 near Δ = 0.35–0.40.
  - Re-measured: p > 0.0027 for Δ ≥ 0.15; p > 0.05 for Δ ≥ 0.225. The minimum is about 4.2 near 0.45.
- **R6, the absolute profiles with the calibration (released):**
  - Early: 23.1/7, down from 51.9 without the calibration.
  - Late: 15.1/7, up from 12.6.
  - The calibration helps the early-type profile and costs the late one.

## Caveats

- **The conversions.** The KiDS LePhare masses are read as Chabrier-IMF masses; the Salpeter/Chabrier offset is 0.25 dex; the SPARC SPS reference is Υ_3.6 = 0.5. R2 and R3 bracket these, and no combination tested brings the re-measured split to p > 0.01.
- **The extrapolation.** The ATLAS3D calibration is for E/S0 galaxies, and it is extended to KiDS red lenses (u−r > 2.0, which includes some red spirals) through an ATLAS3D M–σ fit.
- **The added stars act as a point mass.** That is appropriate beyond 44 kpc. The gas masses are left at the catalogue relation.

## Reading

B's colour-blind law needs early-type lenses to hold about 2.2–2.5× the baryons their catalogue masses imply, relative to discs (a differential of 0.35–0.4 dex). B's own dynamical calibration supplies about a fifth of that differential with SPARC's disc correction (0.07 dex), and about two fifths without it (0.15 dex). **So the KiDS split stays B's one specific failure, now at 2.6–2.8σ (released) and 3.3–3.6σ (re-measured) after the calibration.** It remains a failure that every colour-blind dark mass shares (CFG77).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
