# X24b_vacuum_heated_cold: does vacuum heating of the cold sector (Q = ε H ρ_Λ c² per unit volume) give the right sign pattern?

Criteria: `FROZEN_CRITERIA.md` (1d0f8c6967, committed alone first; §3a folds in the coordinator's input from the peer lane
`X24_dwarf_velocity_floor`, received before any number). `AMENDMENT_A1.md` (post-result: one solver bug caught by K2, one
check tolerance, verdict-string code, two reported-only lines). κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never
pooled. Cold component = field mass, never a particle. ε bounded, never fitted or scanned. Not "theory closed". Nothing here
says the data favour the framework. Every number is in `x24b_vacuum_heated_cold.out` / `_results.json` or `x24b_derive.out`.

## Verdict: NO ε WINDOW (both footings), and the sign pattern is WRONG at both edges

- **ε_up (forest + σ₈) = 2.41e-6.** **ε_low (SPARC, late-accreted) = 7.65e-6 canonical / 8.59e-6 alt.** ε_low/ε_up = 3.17 / 3.56.
- **Sign class at both edges, both footings: WRONG SIGN.** The wrong-sign classes are SPARC small, SPARC large, groups,
  cluster T1, the MW disc and the UMa members. LG field is also wrong on canonical (AMBIGUOUS on alt at ε_low). Antlia II is
  wrong on alt only, where X19 labels it NONE.
- **The window is the smaller problem.** The hypothesis's own density inversion keeps early-assembled material cold, and that
  includes the SPARC galaxies' interiors. A SPARC class whose content assembled at z_c 1.5 / 1.2 would reach c_s,need only at
  ε = 1.6e-3 / 8.7e-4 (canonical), **663 / 362 × ε_up**. So even an open window would not empty SPARC.

## Derivation (`x24b_derive.py`, sympy, 5/5)

- **D1:** ū = (ε c²/5)(ρ_Λ/ρ̄_c0) a³ exactly in ΛCDM (H cancels), so c̄_s² = (2ε/15)(Ω_Λ/Ω_c)c² a³. This is X22's p = 2,
  which X22 grades FAIL in its barotropic form.
- **D2:** the entropy K = σ²ρ^{-2/3} obeys dK/dln a = (2/3) ε ρ_Λ c² ρ^{-5/3}. Heating per unit volume is weighted by ρ^{-5/3}.
- **D3:** the linear perturbations are non-barotropic: s′ = (2/3)δ′ − 5(δ + s), with attractor s = −(13/18)δ. That gives
  δp = (5/18) c̄_s² δρ: overdense regions are colder per unit mass, and the effective Jeans pressure is 3.6 times weaker than
  X22's.
- **D4:** ρ_Λ ∝ a^{−ε}, so w_Λ = −1 + ε/3. The thermal energy today is ε ρ_Λ c²/5.
- **D5:** an element held at 1600 ρ̄ from a = ½ gains log 2/2240 = 3.1e-4 of the background's specific heat.

## The ε window

| | canonical | alt |
|---|---|---|
| ε_up: largest ε with forest ≠ FAIL and R_σ₈ ≥ 0.95 (non-barotropic ODE) | 2.4149e-6 | same (FRW is footing-free) |
| background c_s at ε_up, z = 0 / 2 / 3 (km/s) | 274.0 / 52.7 / 34.3 | |
| forest at ε_up | UNDECIDED (T2(k5) z3/z2 0.966 / 0.900); R_σ₈ 0.995; T²(z=0, k = 1 / 10) 0.82 / 0.16 | |
| same history, barotropic (X22 form) | FAIL (T2(k5, z3) 0.879) | |
| late-accreted element (turnaround at a = 1) | ρ_ta/ρ̄ 11.8, k_late 0.00968 (background 0.2) | |
| ε_low (c_s ≥ c_s,need at DTA ρ̄_c0) | 7.6505e-6 (background c_s(z=0) 488 km/s) | 8.5875e-6 (517 km/s) |
| ε_bg (background c_s(z=0) = c_s,need), reported | 1.16e-6 | 1.30e-6 |
| window | **EMPTY** (×3.17) | **EMPTY** (×3.56) |

- The late-accreted element is already ×21 colder per unit mass than the background. This is D2 at work: it spends its last
  e-fold at 3–12 ρ̄.

## Per class (canonical; alt is the same in class; E in dex over the isolated law; * = captured, β at X22's cap)

| class | z_c | c_s at ε_low / ε_up (km/s) | σ | E_pred | E_obs ± s | pred vs X19 |
|---|---|---|---|---|---|---|
| SPARC small | 1.5 | 13.1 / 7.4 * | 45 | +0.874 | −0.046 ± 0.027 | EXTRA vs NONE: **wrong** |
| SPARC large | 1.2 | 17.8 / 10.0 * | 107 | +0.960 | −0.047 ± 0.015 | **wrong** |
| Groups | 0.8 | 28.2 / 15.8 * | 144 | +0.244 | +0.020 ± 0.065 | **wrong** |
| Clusters T1 | 0.6 | 36.5 / 20.5 * | 449 | +0.847 | +0.040 ± 0.133 | **wrong** |
| Clusters T2 / T3 | 0.5 / 0.4 | 41.8 / 48.2 * | 507 / 631 | +1.012 / +1.177 | +0.268 / +0.264 | right sign, OVER (Z_res −8.5 / −22.3) |
| MW disc | 1.2 | 17.8 * | 162 | +1.180 | −0.143 ± 0.014 | **wrong** |
| LG field | 2.0 | 8.5 / 4.8 | 9.3 | +0.30 / +1.34 | +0.055 ± 0.080 | **wrong** (z_c band EXTRA/NONE/EXTRA) |
| MW ultra-faint | 8.0 | 0.56 / 0.31 * | 3.7 | +0.786 | +0.625 ± 0.111 | right, REPRODUCED (Z_res −1.44) |
| bright M31 | 3.0 | 4.2 / 2.4 * | 7.8 | +0.852 | +0.249 ± 0.092 | right, OVER (−6.5); z_c band not robust at ε_low |
| M31 others | 4.0 | 2.4 / 1.4 * | 7.1 | +0.855 | +0.644 ± 0.283 | right, REPRODUCED (−0.75) |
| Crater II | 3.0 | 4.2 / 2.4 | 2.3 | +0.003 / +0.102 | −0.443 ± 0.134 | right (NONE) |
| UMa members | 1.2 | 17.8 * | 97 | +0.909 | −0.063 ± 0.027 | **wrong** |
| TDGs | 0.1 | 76.7 / 43.1 | 17 | 0.000 | −0.691 ± 0.102 | right (NONE): heated, as the hypothesis says |
| DF2/DF4 | 1.0 | 22.2 / 12.5 | 7.4 | 0.000 | −0.843 ± 0.209 | right (NONE): heated |

- Classes that are not decisive: MW classical, Antlia II (canonical) and Coma UDGs are all predicted EXTRA.
- **The pattern.** Everything assembled before z ≈ 1 retains its cold component in full, at X22's cap. Only systems
  assembled after z ≈ 1 out of diffuse material (TDGs, DF2/DF4), or very shallow ones (Crater II, σ 2.3), lose it. That is
  the inversion the hypothesis claims, but its dividing line sits at z_c ≈ 1, not between SPARC and the dwarfs.
- **Variant (reported):** ρ_in = the fair share at the measured ρ_b instead of ρ_vir. It changes one decisive label: Antlia II on alt at
  ε_low, from EXTRA to NONE.

## Dwarfs, per system (A0: hosted and field together, N 82; 55 with log M★ < 6)

| | canonical ε_low | canonical ε_up | alt ε_low | alt ε_up |
|---|---|---|---|---|
| log M★ < 6: predicted EXTRA / NONE | 33 / 8 → **line RIGHT** | 36 / 4 → RIGHT | 33 / 8 → RIGHT | 35 / 3 → RIGHT |
| Spearman(E, log M★): predicted vs observed | **+0.451** vs −0.632 | **+0.965** vs −0.632 | +0.429 vs −0.631 | +0.967 vs −0.631 |
| Spearman(E, log r_half): predicted vs observed | +0.458 vs −0.591 | +0.807 vs −0.591 | +0.446 vs −0.589 | +0.828 vs −0.589 |
| \|E_obs − E_pred\| < 2s | 0.646 | 0.561 | 0.659 | 0.561 |
| hosted / field median E_pred | +0.694 / +0.090 | +0.700 / +0.746 | +0.691 / +0.022 | +0.697 / +0.739 |

- **Sign right, trend wrong.** VHC gives the small dwarfs extra mass, but its extra **rises with M★ and r_half**. The
  observed extra falls toward low M★ and small r_half.
- The hosted / field contrast at ε_low comes only from the transcribed z_c (field 2.0 vs hosted 3–8). It is not a host
  effect, which agrees with the peer lane.

**Floor reading (peer lane c₀ = 4.59 / 4.05 km/s).** VHC's own c_s in the smallest systems is 0.3–0.6 km/s (ultra-faints)
and 1.4–4.4 km/s (bright M31, M31 others, classical). The σ increment that the retained cold component implies for
log M★ < 6 has median 3.8 / 5.3 km/s (canonical ε_low / ε_up). Its size is of order c₀, but it is **not a floor**:
Spearman(increment, log M★) is +0.55 / +0.99 (canonical), +0.48 / +0.99 (alt). It grows with mass, the reverse of the
behaviour that makes c₀ work.

## Clusters and KT

- VHC captures the cold component in every tercile.
- E_pred for T1 / T2 / T3 is +0.85 / +1.01 / +1.18 (canonical). It rises, as X21's KT-tercile A_MID does (1.10 / 1.65 / 2.13).
  The rise comes from the capped content scaling with M_b, not from VHC.
- The amplitude is ×3–4 too large (Z_res −8.5 / −22.3), and T1 is predicted EXTRA where none is measured. This is the same
  failure as X23_late_heating_graded: VHC's c_s in clusters (20–50 km/s) is far below σ.

## Reported

- **Energy.** At ε_low the vacuum puts ε/5 = 1.5e-6 / 1.7e-6 of ρ_Λc² into heat today, and w_Λ + 1 = ε/3 = 2.6e-6 / 2.9e-6.
  At ε_up the figures are 4.8e-7 and 8.1e-7. That is invisible to DESI (w₀ + 1 ~ 0.1–0.3, PROVISIONAL), and the a₀ drift to
  z = 1 is 1e-6 dex. The ~1e-6 scale the brief expected is confirmed.
- **Action status: none in the record.**
  - CFG131's identity ∂_μρ_Λ = −Q u_μ, for a Lorentz-invariant vacuum, requires the vacuum to vary along the cold flow and
    the flow to be irrotational with potential ρ_Λ/Q.
  - `sol61_push/cold_completion_2026_10_20/GRAVITY_ACTION_AUDIT.md` §5: an exactly constant vacuum cannot absorb a finite
    exchange without a dynamical receiver.
  - A local action must replace the global H by a local θ/3. Q then changes sign in collapsing regions (cooling during
    infall) and vanishes in virialised ones. CFG944 Theorem G blocks local θ-keyed terms.
- **Runaway (reported).** A region that loses cold mass heats faster per unit mass (Q/ρ_c), so evaporation is unstable. This
  does not rescue SPARC, because SPARC interiors keep the full share.
- **Bullet Cluster.** The retained cold component is a collisional fluid at c_s 20–50 km/s, far below the ~4700 km/s
  collision speed. It would shock and stay with the gas, against the lensing peaks seen with the galaxies (qualitative).
- **Fossil groups.** Early assembly means more retained cold, so VHC predicts larger excesses in fossil groups.

## Checks

- **Main run: 5/5, exit 0.**
  - K0: c_s,need 190.014 / 201.315; X22's p = 2 and p = 3 rows reproduced (dev 0); X23's E_pred reproduced (dev 1.1e-16).
  - K1: D1–D5.
  - K2: EdS δ_lin 1.6907 and ρ_ta/ρ̄ 5.5517; background k = a⁵/5 to 6e-7.
  - K3: ε → 0 gives T² − 1 = 8e-9; s/δ = −0.72241.
  - K4: 0.09 GB. Runtime 20 s.
- **MUTATE (`X24B_MUTATE=1`, heating per unit mass): exit 1.**
  - The named checks fail as required: K1 (D2, D3 attractor +1/9, D5 ratio 5/3) and K3 (s/δ = +0.111).
  - The background is identical by construction.
- The derivation's MUTATE twin, `x24b_derive_MUTATE.out`, also exits 1.

## What this does not show

- The collapse epochs are PROVISIONAL, from memory.
- The grader is X23's flat-well isothermal profile with X22's cap convention, unchanged. Captured classes are graded at the
  cap.
- The class c_s is the entropy at X22's normalisation density. A polytropic profile would be hotter inside and is not
  computed.
- The forest gate is linear only, the record's proxy.
- The KT test in the C* potential is the peer lane `X23_late_heated_cold`'s and is not repeated here.

## Files and commits

| commit | content |
|---|---|
| 1d0f8c6967 | `FROZEN_CRITERIA.md` (alone, before any script or number) |
| (next) | scripts, `.out` / `_results.json` (main and MUTATE), `AMENDMENT_A1.md`, README |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X24b_vacuum_heated_cold/x24b_derive.py                 # exit 0
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X24b_vacuum_heated_cold/x24b_vacuum_heated_cold.py      # exit 0
PYTHONHASHSEED=0 X24B_MUTATE=1 ... x24b_derive.py ; X24B_MUTATE=1 ... x24b_vacuum_heated_cold.py                                 # exit 1 by design
```
