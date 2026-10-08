# CFG492 FROZEN CRITERIA: same-galaxy GC vs PN test of the SLUGGS outer deficit

Written 2026-10-08, after the part-A inventory (`cfg492_inventory.py`) and before any planetary-nebula (PN) dispersion, offset or law prediction was computed. The GC per-galaxy offsets of the committed audit (AUDIT_SLUGGS, ν_mono, canonical: NGC 821 +0.142, 1023 +0.104, 3377 +0.064, 4374 +0.201, 4494 −0.103, 5846 +0.213) were read beforehand; they are already in the record.

## Why this synthesis (from part A)
- High z: only 2 objects meet the CFG385 specification (AO inner + deep outer + measured gas: zC 400569, zC 406690), and zC 406690 has no resolved gas shape (the CFG400 lesson). A self-calibrated a0(z) needs ≥ 10. Not run here.
- Local discs: no SPARC galaxy has per-object lensing (1 SPARC galaxy is in the KiDS bright sample; FP21's 2,036 stacked z ~ 0.026 lenses gave S/N 0.1). No dynamical disc mass (DiskMass σ_z) is on disk.
- Clusters: X-COP × lensing is 2 (A2142, Hydra A), from heterogeneous literature fits.
- **Early types: 8 galaxies have GC velocities (SLUGGS), PN velocities (PN.S / Noordermeer+08 / Napolitano+09) and an ATLAS3D JAM inner anchor.** Two of them (NGC 4374, NGC 5846) are among the four group/cluster centrals that carry the SLUGGS deficit (CFG323). The PN files have never been read by any lane.

## Question
Is the SLUGGS outer-GC deficit (law under-predicts the GC dispersion by about +0.09 dex; CFG55/CFG323/AUDIT) a property of the MASS (then the PNe on the same galaxies show it too) or of the GC TRACER (density slope, anisotropy, sub-populations; then the PNe do not)? PNe trace the starlight, so their density profile is the measured stellar profile. That removes the γ systematic that dominates CFG323's Z_sys.

## Fixed inputs (no knobs)
- Law g = ν(g_N/a0) g_N, kernel ν_mono (CFG4_common, read-only), κ = ½ FITTED, both footings a0 = 9.36e-11 (canonical) and 1.13e-10 (alt), never pooled.
- Mass model exactly as AUDIT_SLUGGS: Hernquist, a = R_e/1.8153 (SLUGGS R_e at the SLUGGS distance), total stellar mass from the ATLAS3D JAM calibration ν(G(M/2)/r12²/a0)·M/2 = M_JAM/2 (`jam_mass`), no dark matter, no gas (as the audit headline).
- GC side: the audit's code path unchanged (equal-number bins, n_b = max(2, min(6, N/25)), ≥ 12 per bin, deconvolved ML σ, |v − v_sys| < 1200 km/s then 3σ clip, ≥ 30 clean tracers, outer bins R > max(R_e, 2 kpc), tracer ρ ∝ r^−3, β = 0).
- PN side: the SAME estimator and binning rule. Radius = projected circular distance from the SLUGGS galaxy centre (RAJ2000/DEJ2000 of the SLUGGS table). Tracer density = the Hernquist starlight profile (a = R_e/1.8153), β = 0. Missing velocity errors (Napolitano+09) = 20 km/s. Noordermeer+08 rows with a non-blank n_HV note are excluded in the primary (the note text is not on disk); a reported row keeps them. NGC 3379/3384 PNe (Sluis+06) are not used (no SLUGGS centre or GC sample).
- Jeans: spherical, isotropic, exact line-of-sight projection, general tracer density (the audit's power-law solver generalised; control C2).

## Statistic
Per galaxy g: O_GC(g), O_PN(g) = mean over outer bins of log10(σ_obs/σ_law). Δ(g) = O_PN − O_GC. Paired sample = galaxies with both a GC and a PN offset.
- D = mean Δ over the paired sample. σ_D = the LARGER of (i) the galaxy-to-galaxy std (ddof 1)/√N and (ii) the inverse-variance error from per-galaxy bootstrap errors (500 resamples of each tracer catalogue, seed 492).
- M_PN = mean O_PN over the paired sample, with the same error rule.

## Decision rules (each footing separately; a verdict needs the same class on both footings, otherwise FOOTING-DEPENDENT)
1. **MASS PROPERTY (deficit confirmed by a second tracer):** M_PN > 0 at ≥ 2σ AND |D| < 2σ_D.
2. **TRACER SYSTEMATIC (deficit not seen in starlight):** D < 0 at ≥ 2σ_D AND |M_PN| < 2σ.
3. **PN SURPLUS (law over-predicts the PN dispersions):** M_PN < 0 at ≥ 2σ. Reported as its own law tension, whatever D is.
4. Otherwise **UNDECIDED**. A lean is not a detection.
Requires N_paired ≥ 5; with fewer the verdict is NOT POSSIBLE.

## Expected power (stated before running)
The six GC offsets have a galaxy-to-galaxy std of about 0.12 dex. If the PN offsets scatter similarly, σ_D ≈ 0.07 dex, so a full removal of the deficit (D ≈ −0.10) would show at only about 1.4σ. **The test is expected to be underpowered: UNDECIDED is the most likely outcome unless the PN and GC offsets track each other closely.** It can still decide rule 3 (a PN surplus) if the PN offsets are coherently negative.

## Controls (pass/fail, reported)
- C1: the GC offsets of the paired galaxies reproduce AUDIT_SLUGGS (ν_mono, both footings) within 0.005 dex.
- C2: the general-density Jeans solver with ρ = r^−3 reproduces the audit's power-law solver within 0.002 dex at every bin.
- C3: each PN catalogue is centred on its galaxy: the median PN position lies within 1 R_e of the SLUGGS centre, and its clipped mean velocity is within 150 km/s of the SLUGGS v_sys.
- C4: every paired galaxy has ≥ 30 clean PNe and ≥ 2 PN bins, else it is dropped (stated).

## MUTATE (shuffled cross-match, separate outputs `_MUTATE`)
Each galaxy's PN set, as (R/R_e, v − v_sys, error), is moved to the next galaxy of the paired list (cyclic derangement) and rescaled to that galaxy's R_e and v_sys; GC and mass model stay. The MUTATE fires if rms(Δ) under the shuffle exceeds rms(Δ) of the true pairing. If it does not fire, the pairing carries no information and the paired statistic is reported as uninformative.

## Reported rows (not decision rows)
β = ±0.5 on the PN side; Alabi+17 γ on the GC side (CFG111 relation); PN 2.5σ clip; all bins instead of outer bins; Noordermeer flagged rows kept; the two group centrals (4374, 5846) separately; PN-only galaxies without a GC offset (NGC 3608, 4564); a0/100 sensitivity of O_PN.

Never cite this as a framework win or loss beyond the rule that fired. κ = ½ is fitted.
