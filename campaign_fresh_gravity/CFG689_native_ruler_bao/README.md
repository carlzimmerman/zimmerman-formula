# CFG689 — BAO with the framework's own ruler, and the whole BAO chain (CFG681–689) in one place

**Frozen design:** criteria 1c237145d; addendum A1 0db6da294 (no-ΛCDM audit, curvature free); addendum A2 bb21587be (θ*, SN swaps, P6).
**Code:** script 5bd973fb1 → 00f304d98 → fa3f1eedc (guard) → 07259c4c6 (A2) → 238cf0978 (parallel watchdog) → fb8d4bba4 (post-hoc B12c).
**Runs:** all 30 frozen modes rc 0, 2026-10-20 14:43–15:14, plus B12c (post hoc). Every number below is in `cfg689_summary.md`,
written by `cfg689_summary.py` from the run JSONs.
**Standing wording:** κ fitted; cold energy mass required; not theory closed; **nothing here says the data favour the framework over
ΛCDM.**

## Bottom line

1. **BAO cannot separate the framework from ΛCDM.**
   - Before the switch acts, both have the same ingredients: GR, photons, neutrinos, baryons, a cold component and dark energy
     (CFG654 principle).
   - At most 3% of the cold mass is made after recombination (CFG253).
   - So the expansion history, and therefore BAO, is the same.
   - What BAO can do is fix **the framework's own a0(z) prediction**. That is what CFG689 does.
2. **The dark degeneracy that stopped CFG681–685 is broken (P1: DEGENERACY BROKEN in every frozen headline mode).**
   - Why it breaks: the sound horizon r_d is not a free nuisance. It is pre-switch physics (CFG654 A1 pair → 147.07 Mpc), and ρ_m(z) =
     ω_m(1+z)³ (CFG253).
   - So each DESI D_H/r_d is an absolute H(z), and ρ_DE(z) follows per redshift.
   - No CMB late-time fit, no CPL, no flatness assumption and no ΛCDM model enters.
3. **The framework's native a0(z):** a0(z)/a0(0) = √X(z).

   | z | curvature free (primary) | flat + θ* (TF) | rival a0 ∝ H(z) |
   |---|---|---|---|
   | 1.0 | 0.91 [0.76, 1.03] | [0.88, 1.00] | 1.76 |
   | 1.5 | 0.94 [0.71, 1.12] | [0.80, 1.05] | 2.35 |
   | 2.33 | 0.91 [0.33, 1.21] | [0.68, 1.05] | 3.49 |

   - That is **flat within about 1σ, with a mild decline preferred**. The bump is at z ≈ 0.7 (node w = 0.39 vs 0.31 at z = 0), the
     same shape as the record's M-DEC curve, but now native.
4. **Constant dark energy is NOT rejected.**
   - P2 runs from 1.97σ (primary, curvature free) to 2.61σ (flat + θ* + Union3).
   - No frozen combination reaches 3σ. The P2-with-θ* rule across Pantheon+/DES-SN5YR/Union3 gives **HINT**.
   - The primary (1.97σ, CONSISTENT) and the flat bracket (2.10σ, HINT) sit either side of the 2σ line, which triggers the frozen
     **FLATNESS-SENSITIVE** flag.
5. **Curvature:** flat. Ω_k = +0.011 [−0.037, +0.059], and with θ* +0.001 [0.000, 0.003].
6. **Native H0** (BAO + SN shape + pre-switch physics): **67.70 [67.09, 68.31]**.
   - Bracket B5c (no CMB ω_c, SH0ES h 0.7304) needs ρ_DE ≤ 0 by z ≈ 1.5 (3.45σ "evolving").
   - The tracking law cannot accommodate that: a0 would vanish at cosmic noon. That bracket is reported only.
7. **The decisive framework-vs-ΛCDM measurement (P6).**
   - Target: one clean deep-MOND a0 point at z ≈ 2.5, against ΛCDM's own emergent-scale law (DM14, record 9d40e9c15c).
   - Required error for 20:1: **≈ 0.10 dex** in the primary; 0.11 flat; 0.11–0.13 with θ*. The record's 0.13 dex assumed an exactly
     flat a0.
   - z = 2.5 is extrapolated beyond the last BAO node. At z = 2.0 (interpolated) the requirement is 0.074 dex.
   - P6 names the measurement; it is not a result. Big Wheel's single point gives log10 B = +0.48: reported only, N = 1, too coarse.
8. **Tracking vs the rival a0 ∝ H(z).**
   - 3σ needs a0 to 0.055 / 0.072 / 0.074 / 0.084 dex at z 1.0 / 1.2 / 1.5 / 2.33 (primary).
   - Before this lane, the CMB-free target was 0.02–0.05 dex.
   - No public sample reaches it (CFG685: best 0.4–0.5 dex). RC100/CRISTAL at its optimistic 0.125 dex would LEAN (S 2.57); flat
     F gives S 3.33.

## No ΛCDM assumption left unbounded (addendum A1 audit)

| ingredient | outcome |
|---|---|
| Flatness | removed (primary curvature free); flat = bracket F |
| DESI fiducial cosmology | **P4 INSIDE TESTED SPAN**: our α_iso 0.975–0.997 and α_AP 0.976–1.021, inside DR1 Table 10's c001–c004 span (residual bias ≤ 0.1%) |
| ΛCDM nonlinear damping / reconstruction growth | **P5 NEGLIGIBLE**: framework vs Newtonian same-seed PM power differs by ≤ 3.9% at k ≤ 0.33 h/Mpc (NC1x/NCS0, T1x/P0, T2x/P0), so Δα ≤ 3.9e-4 < 7e-4 |
| Reconstruction itself | **B12** (DESI DR1 pre-recon α_iso) and the **post-hoc control B12c** (DR1 post-recon, same conversion) show the same z ≈ 1 zigzag (node w(1.0) −0.03 pre vs +0.09 post). That pattern comes from the DR1 isotropic-only data, not from reconstruction; removing reconstruction moves the result by less than its errors. Both flip P1 to PARTLY BROKEN (isotropic distances cannot separate adjacent nodes). Full removal = lane L2 (raw DR1 catalogues) |
| CMB ω_b/ω_c extraction | B8 (σ ×2): no class change; B1 (BBN ω_b): P2 → 2.00σ HINT |
| SN peculiar velocities (Pantheon+) | B7 (zCMB > 0.03): P2 2.35σ HINT |
| SN set | D5 (DES5) 1.38σ; U3 (Union3) 2.20σ; P1 BROKEN in all |
| Cold-mass conservation (CFG253 ±3%) | B4m: band shifts up; B4p: z 2.33 lower edge → 0. The high-z band is the most sensitive item |
| m_ν, ω correlation, node count | B2, B3, B6: no P1 change; P2 wobbles across 2σ |

**Brackets with no reading:**
- B9 (no CMB, no H0, positivity only): K4 FAIL. ω_c runs to its 0.05 floor, so positivity alone does not fix ω_m.
- B10 (no Lyα): K4 FAIL. z ≥ 1.5 is unconstrained without the forest.

## Checks, controls, disclosures

**Checks**
- K1, K2, K3, K5, K7 and K8 pass. These include:
  - CFG681's χ² reproduced (10.5515 / 1400.143);
  - DESI's own fiducial Lyα distances reproduced to 0.03%;
  - CFG654's θ*-solved h reproduced (100θ* 1.041092).
- **K9 FAILED as frozen.** The emulator error passes (≤ 5e-5), but z* spreads 1.24 over the ±2σ corners against a frozen limit < 1.
  - Post hoc: c/H(z*) ≈ 0.19 Mpc per unit z, so ±0.62 moves D_M(z*) by about 9e-6, under A2.1's 1e-5 tolerance (≈ 0.03σ of θ*).
  - The θ* numbers are kept, with this disclosed.
- K4 passes in every mode except B9 and B10 (above).

**MUTATE**
- M1 (constant truth) PASS: Δχ² 0.00.
- M2 (vanishing dark energy) PASS: Δχ² 66.5 (7.2σ), nodes recovered.
- M3 (r_d × 1.02) BITES at 1.89σ: the result rests on the ruler.
- M4 (θ* truth) PASS: 100θ* recovered to 2e-16.
- Curvature-free M1k and M2k also recover (reported only).

**Disclosures**
- Hand estimates were made and frozen into the criteria before any code (base §1). The run agrees with them in shape.
- **Run plan changed by owner decision** (2026-10-20, "small runs in parallel"). The modes ran beside the NC2x 1024³ job: two
  single-thread slots, with a watchdog that exits on swap +1 GB or free < 8 GB. No guard tripped, and NC2x's swap stayed flat.
- Numpy's Accelerate backend printed spurious matmul warnings. K3 reproduces CFG681's χ² exactly.
- The analysis header reads "Pantheon+ shape" in the D5/U3/TD5F/TU3F modes. That is cosmetic: the SN line at the top of each `.out`
  gives the set actually used.
- B12c was added post hoc, after every frozen mode had run.

**P3 (κ = ½, reported only, NOT a footing change):** native ρ_DE(0) gives a0 = 9.35e-11 m s⁻² against the canonical footing's
9.36e-11. That is a consistency check, not a derivation (κ is fitted).

## The chain this completes

| lane | finding |
|---|---|
| CFG681 (e6d43c49a) | Raw BAO + SN, no CMB/CPL/ΛCDM: constant dark energy fine (1.3σ BAO; 2.1σ with SN); AP fine; duality conserved; **dark degeneracy** with r_d profiled |
| CFG682 (468748e2e) | Flat a0 ⇒ Ω_m 0.3085 ± 0.0075, consistent with Planck. A consistency pass ΛCDM shares |
| CFG683 (0568d6fa4) | The rival a0 ∝ H(z) is pinned to ±1.5%; tracking stays degenerate CMB-free |
| CFG684/685 (0a580fd32) | Chronometers and SN swaps do not break it; no public sample reaches the target |
| **CFG689** | The framework's own ruler breaks it. Native a0(z) band; no ΛCDM assumption unbounded; constant dark energy survives; decisive z ≈ 2.5 target ≈ 0.10 dex |

**Next:**
- Lane L2: raw DESI DR1 catalogues with a native pipeline. Needs an id and download approval.
- A clean deep-MOND a0 point at z ≈ 2–2.5 (JWST/ALMA). The CFG570/571 sealed galaxies at z 1.2–2 are released 11-06 and 11-28.
- **Canon:** fold in per `HANDOFF_TO_ORCHESTRATOR.md`.
