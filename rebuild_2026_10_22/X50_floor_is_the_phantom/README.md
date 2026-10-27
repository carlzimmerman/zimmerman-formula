# X50_floor_is_the_phantom: the a₀/(2πG) floor halo is not the law's phantom halo

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (4d3134a014, committed alone before any script or number).
`AMENDMENT_A1.md` (da6f3136a7, post-result, check implementation only): run 1 failed one K1 sub-test from floating-point
cancellation in Q = √y√(y+4)/2 − y/2 at y > 3e7. K1 now evaluates Q = 1/ν, an identity sympy verifies. Every graded line of
the rerun is identical to run 1 (kept as `*_run1_K1FAIL.*`).

Standing caveats: κ = ½ FITTED; the footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²) are never pooled; cold dark
energy is a gravitating w ≈ 0 field component, not matter and not a particle. No constant is fitted. This is not "theory closed",
and nothing here says the data favour the framework. Literature values are PROVISIONAL.

**Hypothesis PF.** In isolated galaxies, X38's floor halo (Burkert, ρ₀r₀ = Σ_a₀ ≡ a₀/(2πG) = 107 / 129 M☉ pc⁻²) is
quantitatively the law's own phantom halo, ρ_ph = ∇·(ν g_N)/(4πG) − ρ_b, with the record's ν(y) = ½ + √(¼ + 1/y).

## Verdict (frozen rule): **PF FAILS**, on both footings

The phantom halo is **denser at the centre and heavier**, and **shaped like the baryons rather than cored**:

| per-galaxy metric (175 SPARC galaxies, P4's Υ, X38 halo on bg A) | canonical | alt | gate |
|---|---|---|---|
| M1: log M_ph/M_X38 at R_last, median (16–84 %) | **+0.109** (+0.039, +0.189) | +0.100 (+0.039, +0.183) | \|median\| ≤ 0.10, half-width ≤ 0.20: FAIL / pass (alt 0.0999, on the edge) |
| M2: log peak-pull ratio (primary surface-density measure), median (16–84 %) | **+0.255** (−0.034, +0.522) | **+0.206** (−0.076, +0.506) | \|median\| ≤ 0.10: **FAIL / FAIL** |
| M3: shape rms of log g_ph/g_X38 within the data, median (16–84 %) | **0.180** (0.081, 0.356) | **0.166** (0.079, 0.346) | ≤ 0.10: **FAIL / FAIL** |

- **How PF fails.** The phantom's pull-equivalent ρ₀r₀ is **1.80 / 1.60 Σ_a₀** (median; the floor is 1.00). It pulls harder
  than the floor halo in 77 % / 67 % of galaxies. It is heavier at R_last in 90 % / 91 %. Its per-galaxy shape differs by
  0.17–0.18 dex rms.
- **The phantom's core density is not constant.** It tracks the baryons: Spearman(log s, log Σ_b(0)) = **+0.74 / +0.75**.
  The floor is the same in every galaxy by construction.
- **Variants do not move the class.** On bg B, M1/M2/M3 are +0.099/+0.255/0.185 (canonical) and +0.088/+0.205/0.171
  (alt). At X38's own Υ they are +0.146/+0.293/0.182 and +0.136/+0.255/0.167.
- **Reported descriptors:**
  - A free Burkert fit to each phantom M(<r) gives ρ₀r₀ = **2.00 / 1.85 Σ_a₀** (median, 0 fits at the bounds).
  - Over the data range the outer density slopes agree: phantom −1.45 against X38 −1.37 (canonical), −1.47 against −1.49
    (alt). The data stop at R_last ≈ 2.1–2.4 r₀, before the r⁻² against r⁻³ tails separate.
- **The data's per-galaxy Σ spread is partly the phantom.** X47's free per-galaxy Σ fit, recomputed here, reproduces X47:
  168/175 constrained, with medians +0.070 / −0.020 dex. Its Spearman correlation with the phantom's pull-equivalent Σ is
  **+0.60** on both footings, and the phantom sits +0.13 / +0.18 dex above the free fit. So X47's ±0.32 dex spread is not
  only noise: galaxies whose phantom is denser also want denser fitted cores. But the phantom overshoots what the
  Burkert fits want.

## Analytic part (sympy; checks K1–K3)

Write y = g_N/a₀ and Q(y) ≡ y(ν − 1) = g_ph/a₀.

- **A1, the bound that does exist.** Q = **1/ν** < 1, and lim Q = 1. So the phantom's own pull obeys
  **|g_ph| < a₀ = 2πG Σ_a₀** (exact in spherical symmetry and 1D; in QUMOND, up to the curl field).
  - In X38/X47's peak-pull convention this caps the pull-equivalent ρ₀r₀ at **1/c_B = 3.93 Σ_a₀**.
  - Equivalently, the mean enclosed phantom surface density M_ph(<r)/(πr²) stays below **2 Σ_a₀**.
  - The phantom pulls as hard as the floor's peak (c_B a₀ = 0.2545 a₀) at y = 0.0869. Above that it is denser than the
    floor.
- **A2, the central column of a thin disc (exact QUMOND on the axis).**
  - The column is **Σ_ph(0) = Σ_a₀ S(y_s)**, with S(y) = ∫₀^y (ν − 1) dt = ½√(y(y+4)) − y/2 + 2 ln[(√y + √(y+4))/2]
    and y_s = 2πGΣ_b(0)/a₀.
  - Limits: S ≈ 2√y_s at low y_s; S − ln y_s → 1 at high y_s. **For the simple ν the column has no finite maximum; it grows
    logarithmically.**
  - S = 1 (column = Σ_a₀) at y_s = 0.330. S = π/2, the floor Burkert's own central column (π/2) Σ_a₀, at y_s = 0.985.
  - K2 checks this on a numerical exponential disc (Hankel fields, finite-difference divergence, sheet term) to
    ≤ 2.0e-4 relative at y_s = 0.1, 1 and 10.
  - On SPARC, with Σ_b(0) = Υ·SBdisk (reported), the disc-centre column is **1.21 / 1.10 × the floor's column** (median).
    It is above the floor column in 58 % / 52 % of galaxies; the 16–84 % ranges are ×0.59–2.26 / ×0.53–2.12.
- **A3, profile shape.**
  - **Point mass:** M_ph(<r)/M = √(x² + ¼) − ½ with x = r/√(GM/a₀), and ρ_ph = M r_M⁻³ / (2πx√(4x² + 1)). It has a **1/r
    cusp** at the centre and a **√(GMa₀)/(4πG r²)** tail.
  - **Cored baryon sphere:** the central log-slope of ρ_ph is **−½**.
  - **Spherical-equivalent exponential disc:** the central log-slope is **−1** at y_c = 0.1, 1 and 10.
  - **Burkert:** a flat core (slope 0) and an r⁻³ tail.
  - So the phantom never has a flat core, and its tail is shallower.
- **A4, what Σ_ph,max is.** The strict bound is on the phantom's pull, |g_ph| < a₀. It is equivalent to a mean enclosed
  phantom surface density below 2 a₀/(2πG), and to a pull-equivalent Burkert ρ₀r₀ below 3.93 a₀/(2πG).
  - The disc-centre column is a₀/(2πG) × S(y_s). There a₀/(2πG) is the **scale**, not a cap: for the simple ν, S grows as
    ln y_s.
  - (PROVISIONAL context: Milgrom 2009, MNRAS 398, 1023, states a bounded phantom central surface density of order
    a₀/(2πG). For ν that approach 1 faster than the simple ν, S would saturate.)
  - The label "a₀/(2πG)" therefore matches X38's ρ₀r₀ in name only. In the same convention the two quantities differ:
    - peak pull: the phantom reaches up to a₀, the floor 0.2545 a₀;
    - central column: the phantom has Σ_a₀ S(y_s), the floor (π/2) Σ_a₀.

## Dwarfs and ultra-faints (frozen sub-question)

The phantom is computed for **isolated** dwarfs. That is an upper bound: an external field only lowers it. X49's data path is
used, with its seed. X49's floor medians and Z are reproduced to ≤ 7e-7 dex and ≤ 7e-6 in Z. The reported flag in the JSON
says `False` only because its 1e-9 tolerance is tighter than the 1e-5 relative a₀ difference between CFG4_common and X49's
literal constant.

| class | canonical phantom E (Z) | floor E (Z) | M_ph/M_floor(<r₁₂) | alt phantom E (Z) | M_ph/M_floor |
|---|---|---|---|---|---|
| MW ultra-faint (31) | **+0.592 (+5.22)** | +0.476 (+3.80) | 0.80 | **+0.552 (+4.87)** | 0.85 |
| bright M31 (25) | +0.227 (+2.20) | +0.176 (+1.70) | 0.74 | +0.187 (+1.81) | 0.78 |
| M31 others (5) | +0.747 (+2.29) | +0.571 (+1.71) | 0.72 | +0.707 (+2.12) | 0.75 |
| MW classical (8) | +0.245 (+1.69) | +0.125 (+0.91) | 0.73 | +0.206 (+1.42) | 0.74 |
| LG field (13) | +0.046 (+0.57) | −0.034 (−0.49) | 0.73 | +0.007 (+0.08) | 0.75 |

**UFD answer: PHANTOM NOT HEAVIER**, on both footings. Even isolated, the phantom holds 0.72–0.85 of the floor halo's mass
inside r₁₂, so the ultra-faints get worse (Z +5.2 / +4.9). The dwarfs are deep (g_N/a₀ ≈ 0.001–0.014), where Q ≈ √y falls
below the floor's c_B. The phantom does not supply the heavier UFD halos that X49 lacked.

### Against `X51_dwarf_cooling_floor`'s M200 (reported only; coordinator request; criteria unchanged)

The peer lane `X51_dwarf_cooling_floor` (f029a8c37b) sets M200 = max(EM1 extrapolation, M_cool), with the atomic-cooling
mass M_cool = 1.1314e8 M☉ recomputed here from X51's formula; it matches X51's UFD M200. X51's floor-halo medians are
reproduced to the printed digits. The phantom prediction does not change; only the floor halo it is compared with does.

| class | canonical floor (X51) E (Z) | M_ph/M_floor,X51(<r₁₂) | alt floor (X51) E (Z) | M_ph/M_floor,X51 |
|---|---|---|---|---|
| MW ultra-faint | −0.218 (−1.91) | **0.162** | −0.316 (−2.78) | **0.140** |
| bright M31 | −0.080 (−0.73) | 0.356 | −0.096 (−0.87) | 0.370 |
| M31 others | +0.029 (+0.09) | 0.179 | −0.035 (−0.10) | 0.164 |
| MW classical | +0.017 (+0.24) | 0.479 | −0.028 (−0.42) | 0.462 |
| LG field | −0.054 (−0.88) | 0.725 | −0.098 (−1.56) | 0.751 |

**UFD answer against X51's M200: PHANTOM NOT HEAVIER**, on both footings, and by much more. With the cooling-floor mass,
the floor halo holds 6–7 × the phantom's mass inside r₁₂ for the ultra-faints. That floor halo fits them on canonical, and
overshoots them on alt. The phantom stays at Z +5.2 / +4.9. So the gap between "law fundamental" and "floor halo" widens in the dwarfs
once the dwarf halo-mass trend is fixed by the cooling floor.

## Clusters (reported only)

At X40b's committed cluster-core baryon pull, the phantom's pull-equivalent Σ is below the floor:

| footing | g_b/a₀ (KT T1 / T2 / T3) | phantom pull-equivalent Σ | X43's required core η Σ_coll (η 14.83), at 1e14 / 1e15 M☉ |
|---|---|---|---|
| canonical | 0.048 / 0.055 / 0.073 | 0.77 / 0.82 / 0.93 Σ_a₀ | 2.84 / 4.82 Σ_a₀ |
| alt | 0.041 / 0.048 / 0.064 | 0.72 / 0.77 / 0.88 Σ_a₀ | 2.35 / 3.98 Σ_a₀ |

So in clusters the phantom gives about the floor level or less, a factor ≈ 3–6 short of the cores X43 and X48 need. That
is consistent with the X43/X48 reading that the cluster excess comes from collapse (η Σ_coll), not from the floor. It also
adds a mismatch: the phantom sits **above** the floor in galaxies (M2) and **below** it in cluster cores and dwarfs.
**The floor's constancy does not follow from the phantom in any of the three regimes.**

## Reading

- **"Law fundamental" and "cold dark energy settled at the floor" do not coincide quantitatively.**
  - The phantom is a baryon-tracing, cuspy halo whose core surface density scales with the baryons. It runs about
    √(Σ_b Σ_a₀) at low y_s and grows logarithmically at high y_s.
  - The floor is a constant-Σ cored halo.
- **They share the scale a₀/(2πG) and the order of magnitude:** the median pull-equivalent Σ is 1.6–1.8 Σ_a₀, and the masses
  at R_last agree to +0.10 dex.
- **The difference is consistent with what SPARC shows** (an interpretation, not graded). It would explain why X38 needs Υ ≈ 0.77 / 0.60 where the law takes 0.52 / 0.44: the floor
  halo is lighter in the inner disc, so the stars make up the difference. It would also explain why the law fits more tightly (rms
  0.054 against 0.073–0.080).
- **The tether is therefore not "cold dark energy fills the phantom profile".** Filling the phantom profile would reproduce
  the law, not X38. It would lose the dwarfs further (the UFDs get worse), and it would leave the clusters as short as the
  law is.
- **One positive thread.** The data's per-galaxy core Σ correlates with the phantom's (Spearman +0.60). Whatever settles
  cold dark energy appears to know about the baryon surface density. A pure constant floor ignores that.

## Checks and MUTATE

- **Checks 6/6.**
  - **K0a:** X38's four SPARC rows are reproduced: rms 0.0795 / 0.0792 / 0.0729 / 0.0729 at Υ 0.77 / 0.76 / 0.60 / 0.60.
  - **K0b:** P4's law row is reproduced: 0.054087 / 0.053718 at Υ 0.52 / 0.44.
  - **K1:** sympy confirms lim Q = 1, Q = 1/ν, Q monotone and < 1, and dS/dy = ν − 1. The closed form of S matches
    quadrature to 8e-15.
  - **K2:** the disc column matches to ≤ 2.0e-4.
  - **K3:** the point-mass tail is 0.9950 at 100 r_M, and the quadrature is exact.
  - **K4:** 0.21 GB, 31 s.
- **MUTATE** (`X50_MUTATE=1`, ν → 1, no phantom):
  - **K0b fails:** the law row becomes Newtonian, rms 0.2528 at Υ 1.20.
  - **K1, K2 and K3 fail.**
  - The verdict is **UNDECIDED (step 0)** and the run exits 1, as frozen.

## Files and commands

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`, `x50_phantom_floor.py`, `x50_phantom_floor.out` /
`_results.json`, `_MUTATE.out` / `_results_MUTATE.json`, `x50_phantom_floor_run1_K1FAIL.out` / `_results_run1_K1FAIL.json`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x50_phantom_floor.py                 # exit 0, 6/6, ~31 s, 0.21 GB
    X50_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x50_phantom_floor.py    # exit 1, K0b/K1/K2/K3 fail
