# X60_acceleration_dependent_cold_sector: can cold dark energy and dark energy be two phases of one field, keyed on acceleration?

**Provenance.**
- Criteria: `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (c0c90a8425), committed alone before any script or number.
- Amendment A1 (8a9a12b286) is post-result and disclosed. It adds gate R5 at the coordinator's request.

**Standing caveats.**
- κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10 m s⁻²) are never pooled.
- Cold dark energy is the gravitating w ≈ 0 field component paired with dark energy. It is not matter and not a particle.
- This is not "theory closed". Nothing here says the data favour the framework.
- Every number below is from `x60_an.out` / `x60_an_results.json`.

**Hypothesis AN.** One field. It is dust where the gravitational acceleration exceeds g′ (primary g′ = X47's
g_T = 0.2545 a₀; variant g′ = a₀). It is smooth vacuum energy below g′.

## Verdict: **AN EXCLUDED BY R0, R1, R2, R5** (every escape, both footings, both backgrounds)

| escape | field-theory form | Theorem G | verdict (both footings) |
|---|---|---|---|
| E1-a, smoothed key | k-essence-like P(X, Y), Y = W_R ∗ (a_μa^μ)/g′², a_μ the khronon's acceleration; non-latching | spatially nonlocal, so outside G; R_k → 0 is X47's VT-L, inside G | **EXCLUDED BY R0, R1, R2, R5** |
| E1-b, object key (core / virial pull of the collapsed object) | per-object phase switch; uncollapsed field stays dust | nonlocal, outside G | **EXCLUDED BY R0, R2, R5** |
| E2-L, local hysteresis | latch when K > g′, unlatch when K < g′ | as E1-a | **EXCLUDED BY R0, R1, R2, R5** |
| E2-O, object hysteresis | unlatch a relaxed object below g′ | nonlocal, outside G | **EXCLUDED BY R0, R2, R5** |
| E3-P, two-phase fluid, compensation in place | T = T_d + T_v, T_v = −ρ_v g, ⟨Q⁰⟩ = 0 | nonlocal, outside G | **EXCLUDED BY R0, R2, R5** |
| E3-N, two-phase fluid, relocation | dust removed from galaxies reappears elsewhere | nonlocal, outside G | **EXCLUDED BY R0, R5** |

**No verdict uses Theorem G.** Every exclusion rests on this lane's own lines.

## R0: the w = −1 phase cannot hold or carry the converted energy

sympy (K3) gives ∂_μ(−ρ_v η^{μν}) = −∂^ν ρ_v, and T_v^{0i} = 0 for any 4-velocity when p = −ρ. A vacuum phase therefore
has no momentum density and no energy flux.

**Converted energy left in place.** An emptied galaxy may keep only 0.0065 (canonical) / 0.0009 (alt) of its fair cold
share; this is X22's tolerance of 0.0354 / 0.0049 M_b. The vacuum lump would then sit at 152 / 1096 times the residual
dust density. Residual dust can bear a vacuum gradient, at an acceleration of at most a₀, of only:
- 3.6e-7 at the median R_last;
- 6.0e-6 at r_f(10¹²) = 187 kpc.

That falls short by 10^7.4 (canonical) / 10^8.2 (alt). The lump would also gravitate with ρ + 3p = −2ρ_v, turning the
halo into a repulsive core of twice its mass.

**Relocation.** With exactly w = −1 the energy cannot be moved at all.

**The one loophole (reported).** If the vacuum phase is only nearly vacuum (w = −1 + ε) at ambient ρ_DE, emptying a 10¹²
halo through r_f in 1/H₀ needs εγ²v/c ≥ 5.0e-3. The "vacuum" around every galaxy would then have to stream at
relativistic speed. That is an energy carrier (X22's non-gravitational exclusion class), not smooth vacuum energy, and
no action for it exists in the record.

## R1 and the E1 R_k window

The rms linear pull of the total field over k ≤ k_hm = 15.08 h/Mpc, background A:

| z | rms pull (m s⁻²) | / g_T canonical | / g_T alt |
|---|---|---|---|
| 0 | 1.06e-12 | 0.045 | 0.037 |
| 2 | 3.99e-12 | 0.167 | 0.139 |
| 3 | 5.36e-12 | 0.225 | 0.186 |

Background B agrees to within 3 %.

**Monotonicity (MT, check K2).** An object's smoothed key always contains its environment, K_obj² = K_env² + K_own². A
threshold that empties galaxies therefore also exceeds the linear field at the same epoch.

- **Growth window (dust at every z ≤ 3, galaxies below the threshold, clusters above): empty for every R_k in
  0.01–30 Mpc/h (0/31).** This follows from MT by construction, and is stated as such.
- **Forest-only window (non-latching):**
  - it exists for R_k = 0.25–30 Mpc/h, with g′ = 0.045–0.167 g_T (canonical units);
  - neither g_T nor a₀ lies inside it on either footing. The threshold would have to sit at 0.011–0.043 a₀, which is
    not "of order a₀";
  - the linear field then turns vacuum between z ≈ 2 and today, so σ₈ / KiDS growth is lost and the linear cold
    sector is converted (R2).
- **Reported A2 (environment scatter, no verdict weight).** A forest-only window survives at R_k 0.32–3.5 Mpc/h
  (B: 0.32–4.6). Wherever 90 % of galaxies are emptied, at most 10 % of the z = 0 linear field stays dust.
- **K1.** As R_k → 0 the key reproduces X47's local failure: its cumulative matches X47 to 3.7e-7, and 3σ < g_T at
  z ≤ 3.

## R2: conversion budget against X54

**The X54 line.** Step 0 reproduces X54's interval [−0.0034908, +0.0010992]. The line is the cold → DE end,
F = 2.47 % (M-C DES-SN5YR). The robustness line is 5.16 %, the loosest of the six ends (M-D Union3, a late-acting
profile).

**F_conv.** This is the Press–Schechter mass fraction in halos between M_min and the crossover M_x (z = 0, EM1 σ(M)).
Background A; B is within 0.01.

| footing, crossover | M_min 3.0e8 | 4.9e9 | 1e11 | × line | × robust | q_max (line / robust) |
|---|---|---|---|---|---|---|
| canonical, core c_f = 4, 10^12.09 | **0.312** | 0.246 | 0.138 | 12.6 | 6.0 | 0.079 / 0.166 |
| alt, core c_f = 4, 10^12.43 | **0.366** | 0.300 | 0.192 | 14.8 | 7.1 | 0.068 / 0.141 |
| canonical, ng 48, < 10^11.0 | 0.174 | 0.108 | — | 7.0 | 3.4 | 0.142 / 0.297 |
| alt, ng 48, 10^11.16 | 0.191 | 0.125 | 0.017 | 7.7 | 3.7 | 0.130 / 0.270 |

- **E1-a and E2-L** convert at least 1 − f(>10¹²) = 0.539 (B: 0.554).
- **E2-O** has already converted 0.195 / 0.204 of the cold component by z = 3 (for M_hm < M < M_x). That conversion is
  under way during the forest epoch.
- **Galaxies could pass X54 only by converting at most 7–17 % of each halo.** X53 and X55 want the whole halo gone.

## E3: is phase coexistence consistent with ρ_c a³ ≈ const?

**At the background level, yes.** sympy gives d(ρ_d a³)/dt = −Q a³, which vanishes iff ⟨Q⁰⟩ = 0.

**It cannot be realised locally.**
- **In place (E3-P).** The vacuum inside a collapsed cluster region is only ρ_Λ/ρ_c,vir = 0.0038 (10¹⁴) to 0.0055
  (10¹⁵) of its cold mass. All clusters together can therefore compensate only 0.0025 / 0.0022 of the cosmic cold
  sector, against F_conv 0.31 / 0.37. The net exchange is 0.31 / 0.36, more than ten times X54's line.
- **By relocation (E3-N).** The energy would have to travel through the vacuum phase, which has zero flux (R0).

## R5 (Amendment A1): the non-monotone retention pattern

X58 needs dust in dwarfs (10⁸–10¹⁰), vacuum in L* lenses (10^11.35–10^12.05) and dust at 10¹³ and above. **No key here
can produce that.**

- **Object keys (core and virial) are monotone increasing in M,** because Σ_coll rises with mass.
  Σ_coll(10¹⁰)/Σ_coll(10^11.35) = 0.458, so dwarfs sit below L* galaxies, on the vacuum side.
- **The smoothed key's own term is an inverted U in mass.** It peaks where r_f ≈ R_k. That is the opposite of the U
  shape required.
  - The largest margin min(dwarf, ≥ 10¹³) − max(L*), over all R_k, is −1.0e-7 g_T. It is reached at R_k = 30 Mpc/h,
    where every object's key equals its environment's. The margin is never positive.
  - Reported A3: the pattern dwarf > L* < cluster occurs at 0 of 31 R_k (10⁹–10¹⁰ dwarfs).
- **Why.** Dwarfs have lower acceleration than L* galaxies by any average, so a monotone acceleration key cannot put
  them on opposite sides.
- **Caveat.** Σ_coll below 10¹¹ is a log–log extrapolation of X41's table (disclosed in A1).

## R3 and R4 (reported context)

- **Core key at c_f = 4 with g′ = g_T.** The crossover is X43's 10^12.09 / 10^12.43, so R3 (galaxies ≤ 10¹²) and R4
  (≥ 10¹⁴) both pass, inheriting X43's 14/15 cluster grade.
- **ng 48 η.** The crossover falls to below 10^11.0 / 10^11.16, so L* galaxies would be retained.
- **g′ = a₀.** The core key's crossover is 10^14.61 / 10^14.97, so clusters below that are lost.
- **Virial key.** It never reaches g_T or a₀ below 10¹⁵ M☉, so R4 fails.

## Step 0, checks, MUTATE

**Step 0 passes.**
- S0a: X47's table reproduces with deviation 0, and ζ = 0.254484.
- S0b: X54's interval is exact.
- S0c: X43's crossover is 10^12.094 / 10^12.434.

**Checks pass:** K0–K5 (peak RSS 0.25 GB).

**MUTATE** (`X60_MUTATE=1`) applies four deliberate breaks:
- m1: (1+z)³ scaling;
- m2: the M-D grid;
- m3: p_v = 0;
- m4: the own pull subtracted.

As frozen, K0 (S0a, S0b), K1, K2 and K3 FAIL; the verdict is UNDECIDED and the exit code is 1.

**Implementation fixes made before the first graded verdict:**
- the footing values are taken from EM1/C4 (the hard-coded rounded a₀ missed X47's g_T at 3e-6);
- K4 tests erfc(0) = 1 and that σ(M) decreases, as the frozen text says, instead of probing M = 1e-3 M☉, where the P(k)
  table (k ≤ 150 h/Mpc) saturates σ;
- the z_off interpolation was corrected.

The A2 scatter block and the A3 block were added after the first run as REPORTED only. R5 is graded per A1.

## Reading

**What AN would need.** Taking "paired with dark energy" literally as a phase change fails on three counts:
- **R2 (conservation budget).** The galaxies' share is 14–37 % of the cosmic cold sector, 3–15 times what X54 allows (robust line to primary line)
  to turn into dark energy.
- **R0 (locality).** A w = −1 phase can neither hold a lump nor carry energy away.
- **R5 (ordering).** Acceleration orders dwarfs below L* galaxies, but the data need them on opposite sides.

A smoothed key also cannot keep today's linear field dust while emptying galaxies.

**What remains open.** Only the εγ²v/c ≥ 5e-3 streaming-carrier loophole. That loophole is no longer AN's vacuum phase,
and it fails R5 in the same way.

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`, `x60_an.py`, `x60_an.out` / `_results.json`,
`x60_an_MUTATE.out` / `_results_MUTATE.json`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x60_an.py                 # exit 0, ~10 s, 0.25 GB
    X60_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x60_an.py    # exit 1
