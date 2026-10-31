# NF1_no_floor_rule: FLOOR NOT NEEDED on the SPARC line. The collapse branch alone passes on both footings, with the footings coinciding. This is a SPARC statement, and N0 itself has problems at low mass

Criteria: `FROZEN_CRITERIA.md` (f95621e30a), committed alone before any script or graded number. Scripts `nf1_x74.py`, `nf1_run.py`, `nf1_bins.py`. Outputs `nf1.out`, `nf1_results.json`, `nf1_bins.*`, `NF1_*`. Post-result, reported only: `nf1_verify.py`, `nf1_lt.py` and outputs.

## Frozen grade (X74's grader, FC1's conversions, f★ 0.034, median η): S = f_c η(M_t) Σ_coll(M_t) at every mass, no floor
| variant | η below 10¹² | Υ (A/B) | rms (A/B) | SPARC line |
|---|---|---|---|---|
| FC1, with floor (canonical) | flat | 0.51 / 0.50 | 0.0687 / 0.0700 | pass |
| FC1, with floor (alt) | flat | 0.44 / 0.44 | 0.0719 | fail (X78) |
| **N0** (primary) | flat | **0.71 / 0.73** | **0.0678 / 0.0688** | **pass** |
| **N1** | s 0.0927 per dex | **0.55 / 0.56** | **0.0670 / 0.0681** | **pass** |
| N2 | s 0.1668 per dex | 0.47 / 0.48 | 0.0695 / 0.0706 | fail (Υ) |

**LABEL: FLOOR NOT NEEDED** (SPARC only). Canonical and alt coincide exactly (K2), so X78's alt failure no longer applies to route E. Clusters and groups don't change at all (K3, ΔZ = 0): the floor was never active there. Interpolating linearly between N1 and N2, the line holds for s up to about 0.14.

## By V_flat (Υ 0.50; ΔV km/s over 2–4 R_d)
| V_flat | n | lg M200 | ET1 S need [95 %] | ET2 free S | FC1 floor: S, Υ, ΔV | N0: S, Υ, ΔV | N1: S, Υ, ΔV | N2: S, Υ, ΔV |
|---|---|---|---|---|---|---|---|---|
| 20–60 | 13 | 9.97 | 69 [52, 85] | 70 | 107, 0.30, +3.7 | 47, **1.20**, −5.2 | **72**, 0.30, −1.0 | 100, 0.30, +2.3 |
| 60–100 | 35 | 10.59 | 103 [81, 124] | 108 | 107, 0.48, +2.9 | 69, **1.10**, −6.1 | **91**, 0.59, +0.5 | 115, 0.33, +5.5 |
| 100–150 | 23 | 11.13 | 143 [118, 200] | 158 | 107, 0.73, −6.4 | 94, 0.84, −10.5 | 112, 0.71, −5.5 | **128**, 0.56, −1.6 |
| 150–200 | 25 | 11.76 | 150 [98, 190] | | 136, 0.54, −3.8 | 136, 0.54, −3.8 | 141, 0.53, −2.4 | 145, 0.52, −1.3 |
| 200–250 | 18 | 12.11 | 215 [137, 272] | | 156, 0.60, −16.2 | same | same | same |
| 250–400 | 10 | 12.27 | 412 [182, 596] | | 161, 0.76, −56.7 | same | same | same |

S_rule at lg M200 8 / 9 / 10 / 11: N0 13.8 / 26.0 / 48.1 / 87.4; N1 32.0 / 48.6 / 72.6 / 106.4; N2 62.5 / 80.1 / 100.8 / 124.6.

## Checking the win, post-result
**N0's Υ of 1.1–1.2 at low mass is a warning.** It passes because the line is a median. So I looked where Υ can't compensate.

**rms in dex, free Υ / Υ 0.50, and signed offset log(obs/pred) at 0.50 (background A):**

| sample | FC1 floor canonical | N0 | N1 | N2 | law canonical | law alt |
|---|---|---|---|---|---|---|
| all 175 | 0.0687 / 0.1261 | 0.0678 / 0.1294 | **0.0670 / 0.1247** | 0.0695 / 0.1237 | 0.0541 / 0.1124 | 0.0537 / 0.1029 |
| V 20–60 | 0.187 / 0.194 | 0.119 / 0.144 | 0.129 / 0.141 | 0.179 / 0.187 | 0.122 / 0.142 | 0.138 / 0.158 |
| V 60–100 | 0.156 / 0.178 | 0.139 / 0.193 | 0.147 / 0.179 | 0.165 / 0.185 | 0.107 / 0.159 | 0.122 / 0.163 |
| V 100–150 | 0.056 / 0.109 | 0.066 / 0.129 | 0.059 / 0.110 | 0.058 / 0.099 | 0.059 / 0.098 | 0.056 / 0.086 |
| gas ≥ 0.5 (81), offset | −0.039 | +0.036 | **−0.017** | −0.056 | +0.014 | −0.023 |
| gas ≥ 0.7 (41), offset | **−0.110** | +0.016 | −0.060 | −0.114 | −0.038 | −0.075 |

**So the floor is what over-predicts the most gas-rich dwarfs,** by 0.11 dex canonical and 0.15 alt, and the scatter at V < 60 km/s is lower without it. N1 is at the law's level at V 20–60 and is still worse at 60–100. Above 150 km/s the rule is unchanged, and the law stays ahead on scatter everywhere above 60 km/s except 100–150. No variant reaches the law's overall 0.054.

**LITTLE THINGS, independent of SPARC, RT1's single-point recipe, 20 galaxies, median E (negative = over-predicted), rms:**
law canonical −0.025, 0.345; floor canonical −0.041, 0.353; floor alt −0.055, 0.354; N0 **+0.158**, 0.408; N1 +0.078, 0.365; N2 −0.026, 0.354.
So N0 is short here, and this sample prefers s nearer N2. With the SPARC line (s ≲ 0.14), the two give a rough window s ≈ 0.09–0.14.

| Local Group | law | floor can | N0 | N1 | N2 |
|---|---|---|---|---|---|
| IC 1613 | −0.59 (−7.9) | −0.64 (−8.6) | −0.45 (−6.0) | −0.55 (−7.4) | −0.62 (−8.2) |
| WLM | +0.08 (+1.0) | +0.04 (+0.5) | +0.21 (+2.9) | +0.12 (+1.6) | +0.06 (+0.8) |
| DDO 210 | −0.08 (−1.0) | −0.18 (−2.4) | +0.36 (+4.8) | +0.11 (+1.4) | −0.07 (−0.9) |
| DDO 216 | −0.18 (−2.4) | −0.26 (−3.4) | +0.07 (+0.9) | −0.10 (−1.3) | −0.20 (−2.7) |

**IC 1613 stays a failure on every rule.** NF1 doesn't rescue it.

## What it changes, if it stands
- The floor was the only place a₀ entered route E. N0/N1 have no a₀ and no footing in the cold sector. a₀/2πG would just be the collapse S of a roughly 10¹¹ M☉ halo, and a₀ = κc√(Gρ_Λ) would have no role in the cold sector. EM1's T0 already flagged this. **That would change the theory's headline, so it is the owner's call, and this lane changes no standing statement.**
- It predicts X80. The line allows native η(10¹⁰)/η(10¹²) up to about 1.9. ET1 and ET2's medians at the two lowest bins want about 1.5 over N0, their lower bounds about 1.1–1.2. N1 gives 1.53 at 10¹⁰ and 1.24 at 10¹¹. These are converged-cusp η; X80's frozen R(M) uses the ε-cut fit without f_c, so its labels need the cusp fit beside them.
- **A5 can't settle this; X80 can.** The queue has A5 first.

## What gets worse
- **Dwarf ceilings.** PC1's cored ceiling M₃D(<r) ≤ 1.599 S r² falls with S. At lg M200 9 under N1 it drops by 0.34 dex: MW ultra-faints (mean −0.275) reach about +0.07, Draco (+0.148) about +0.49, J0946 gets worse. By hand, not graded. A cusp has ceiling 2π S r², 0.59 dex higher, which would cover these. But that's the shape problem again: zooms make cusps, and SPARC's bright galaxies want cores.
- **The RAR.** With no a₀ in the rule, nothing here explains why rotation curves follow one tight relation with a scale near a₀. The law's rms is still 0.054.

## Checks
K1 (floor restored reproduces FC1, 0.0), K2 (N0 canonical = alt on SPARC, 0.0), K3 (clusters and groups unchanged, 0.0), MUTATE (S × 0.5: Υ 0.71/0.73 → 1.20/1.20, top of grid): all PASS. Cluster η is ng 48 until A4. The inherited K0 prints FAIL by construction, as in X73.

## What this does not show
- It does not measure low-mass S. No zoom has reached these masses. N1 and N2 extrapolate.
- The core shape is still imposed.
- EM1's M200 at low mass is an extrapolated fit (ET2's free fit supports the rise without it).
- It does not address L★ (−16.2 km/s, unchanged), MW, KiDS or contraction (CN1). Contraction was charged only to collapse-branch systems in CN1; with no floor every galaxy is on that branch, so CN1's question widens.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
