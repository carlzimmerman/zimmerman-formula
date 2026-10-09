# CFG508: dark energy vs cold energy. Two different things in every measured property; "one substance" is NOT DECIDABLE

**Files and runs.**
- The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in 7e07bbe99.
- The script is `cfg508_unity.py`. It runs in about 8 s with `nice -n 15` and at most 4 processes.
- Main run: `cfg508.out` and `cfg508_results.json`. Exit 0; controls K1–K5 all pass.
- `CFG508_MUTATE=1` runs a unified fluid with c_s² = 0.01. Outputs are `cfg508_MUTATE.out` and `cfg508_results_MUTATE.json`. That fluid is **EXCLUDED** (Δχ² +504 baryon, +481 total) and fails the growth cut, as the criteria require.
- Data, all already on disk: the DESI DR2 w0wa chains (cmb, +Pantheon+, +Union3, +DESY5); the DESI DR1 ShapeFit fσ8 table as transcribed in L181; CAMB for the ΛCDM P_lin; stock CLASS for validation.
- Nothing was downloaded. The parallel lane CFG507 (where the cold energy comes from) had no content when this ran, so nothing from it was used.

**Bottom line.**
- In every property that has been measured, dark energy and cold energy behave as two different components (table below).
- Every "one substance" model that predicts something different from two components is excluded, or forced so close to two components that the difference cannot be seen:
  - an adiabatic unified fluid (|α| ≤ 1e-6);
  - a fixed cold-to-dark ratio (the ratio changes by a factor of about 8 by z = 1 and about 36 by z = 2);
  - the unified-fluid reading of DESI's w(z): DESI does not prefer it, and it has the wrong shape.
- One unified option survives: a single field whose cold part has zero sound speed by construction (U-0). It is identical to two components and uses the same two constants.
- So the frozen verdict is **NOT DECIDABLE**. Nothing on the record fixes the cold amount from the dark-energy field.

## 1. Property table

| property | dark energy | cold energy | record / source |
|---|---|---|---|
| equation of state w(z) | ≈ −1. DESI DR2 prefers w0 ≈ −0.67 to −0.84 with wa < 0 (chains above) | 0 (dust), which is what the CMB sees as ω_c = 0.120 | DESI DR2 chains; CFG417; PAPER42 (w = −1 if the kernel is fixed) |
| sound speed c_s² | 1 for a scalar, or undefined for Λ. It does not cluster below the horizon | ≈ 0. Here c_s² ≤ 7e-7 (T1a+T1b) if it shares a fluid with dark energy | this lane, T1 |
| clustering | smooth: it does not fall into potentials | clumps; settles into the law's phantom; behaves like CDM on every scale the record tests | CFG474; CFG424–460 (PM, growth OK 3.3–4.0% at 512³) |
| coupling to the law | sets the scale, a0 = κc√(Gρ_DE), κ = ½ FITTED. If ρ_DE evolves, a0 tracks it (DESI: a0(2.5)/a0(0) ≈ 0.78–0.83) | supplies the phantom's mass, drawn halo by halo from the turnaround catchment (a postulate, not derived) | PAPER42; CFG452; CFG424; CFG461/462/488/490 |
| role in growth | background only (H(z)); slows growth late | the growing mode itself. A₀ tracking ρ_DE is indistinguishable from flat a0 in growth (Δσ8 ≤ 0.0006) | CFG419/421/426 |
| CMB: acoustic peaks | negligible at z = 1100 | sets the peak-height ratios (ω_c) | standard |
| CMB: ISW | drives the late potential decay (dlnΦ/dlna = −0.47 today, scale-free in ΛCDM) | none on its own. A unified fluid with sound speed makes the decay scale-dependent (−1.71 at k = 0.1 at the T1a bound) | this lane, ISW proxy |
| BAO | through H(z) and D_M(z) | through r_drag (ω_c) and H(z) | standard; DESI chains |
| lensing | none directly; only distances | the lensing mass. The additive reading is excluded, B is not; the KiDS 1h–2h model is still inadequate | CFG363; CFG502–504 |
| amount | ρ_Λ, input; PAPER42 trades it for y_t ≈ 94 | Ω_c/Ω_b = 5.364, input; one-field label only, amount FREE | PAPER42; CFG288; CFG360 (baryon tie NO-GO) |
| a link between them | none beyond the law itself | — | CFG496 (0 of 15 clues; Buckingham C07) |
| energy exchange | not preferred by DESI in any of four forms | — | CFG368 (criteria only; its results are uncommitted and its K1 failed, so not cited as a result) |
| shear side | the dark-energy gate as an action is unstable | — | DE1–DE13 (DE5b, DE12/13) |

## 2. Unified hypotheses tested

| class | what it is | dark constants | result |
|---|---|---|---|
| H2 | two independent components | 2 | reference |
| U-A | adiabatic generalized-Chaplygin fluid, c_s² = −αw | 3 | **T1a (DESI fσ8):** contiguous allowed range −5.6e-6 ≤ α ≤ 5.6e-5. **T1b (CFG361 growth cut):** \|α\| ≤ 1e-6. Together: **\|α\| ≤ 1e-6**, i.e. c_s² today ≤ 7e-7. α < 0 has an imaginary sound speed and blows up for \|α\| ≥ 3e-5 |
| U-X | U-A read as vacuum plus dust exchanging energy | 3 | a0(z) at the bound changes by < 1e-4 to z = 2.5, so it looks exactly like H2 |
| U-0 | a single scalar with c_s² ≡ 0 plus a constant potential | 2 | identical to H2 in background and linear perturbations by construction. **Survives, with the same constant count** |
| U-R | a fixed ratio ρ_c/ρ_DE | — | **EXCLUDED.** r(z)/r(0) = 7.5–8.2 at z = 1 and 35–38 at z = 2, with 95% intervals far from 1 on all four chains. Scrambled cosmology: independent of R′ (5.6e-16), 0 of 200 false passes |
| U-F | the PAPER42 MOND-field vacuum plus a condensed cold part of the same field | ≥ 2 | no committed lane fixes Ω_c from the field (CFG428: one Bose field DEAD; CFG288/360: amount free; CFG496: no clue) |

**T2 (DESI DR2 background).**
- No α is preferred. The best Δχ² values are −0.06 (Pantheon+), −0.22 (Union3) and −2.16 (DESY5), against the −4 needed. The criteria therefore declare no clash.
- The shape is wrong. U-A gives (w0, wa) on the line wa ≈ +1.4 (w0 + 1), so wa always has the same sign as w0 + 1. It cannot make DESI's w0 > −1 together with wa < 0.
- The a0 consequence runs the opposite way. DESI's best α (−0.01 to −0.05) would give a0 rising to 1.01–1.07× by z = 2.5. DESI's non-interacting fit gives 0.78–0.83×. Both of those α values are in any case excluded by T1 (instability).

## 3. Disclosures (the fail checked as hard as a win)

- **Non-contiguous T1a set.** The frozen T1a rule excludes only when BOTH tracers exclude. For α in 1.8e-4 to 5.6e-3, and at 3.2e-2 and 5.6e-2, the TOTAL tracer's fσ8 drifts back near 1. Post-freeze check P1b shows why: the fluid's density is suppressed to 5% of ΛCDM, but its acoustic velocity is 1.4×. That flow is not a galaxy velocity. In the same models the baryon tracer gives Δχ² = +26 to +327, and both tracers fail the growth cut (σ8 total 0.07–0.27).
- The solver is not the cause: rtol 1e-7 and 1e-9 agree to 2e-5 (P1).
- Under the strict frozen reading, T1a alone does not bound |α| below 1e-3. That puts the verdict in the "bound looser than 1e-3" branch of NOT DECIDABLE. The contiguous-from-zero reading lands in the U-0 branch, which is also NOT DECIDABLE, so the verdict does not depend on this.
- **Scales behind the α < 0 exclusion.** It comes from k ≳ 0.3 h/Mpc inside the 8 Mpc/h window. At k ≤ 0.2 h/Mpc, α = −3e-5 changes the baryon δ by only 1–2% (P2).
- **Limitations.**
  - Sub-horizon Newtonian gauge, with radiation neglected after z = 200.
  - The background change of U-A is ignored in the DESI fσ8 (Alcock–Paczynski) comparison. It is below 3e-5 in w0 at the bound.
  - The DESI chains are used as 2-D Gaussians in (w0, wa); the Ω_m shift is ignored.
- **K2.** The solver agrees with stock CLASS to 0.0033 (fluid with c_s² = 1e-6, at k = 0.1, 0.3 and 1).

## 4. Observables that would separate "two components" from "one substance in two phases"

1. **A sound speed in the cold part.** Any unified fluid needs one. Current reach is c_s² ≲ 1e-6. DESI full-shape, Euclid and Lyman-α P(k) push this down; a detection of a Jeans-like cutoff or oscillation that tracks w(z) would favour unity.
2. **Scale-dependent ISW.** Unity with c_s² ≠ 0 makes the potential decay depend on k (×3.6 at k = 0.1 at the T1a bound). Two components give a decay that is the same at every k. The test is an ISW–galaxy cross-correlation as a function of scale.
3. **w(z) together with growth and a0(z).** In a unified exchange, w(z) departures, growth suppression and a0(z) move together, with a0(z) following ρ_v and not the non-interacting fit. For two components, a0(z) = √(ρ_DE(z)/ρ_DE(0)) from the non-interacting w0wa fit, ≈ 0.8 at z ≈ 2.5. a0 measured at z ≈ 2.5 to 0.1 dex (the record's decisive test) separates the two.
4. **A ratio fixed by physics.** Unity would be favoured if some relation fixed Ω_c/Ω_Λ, or Ω_c, from the field's constants and held at two epochs. None exists (CFG496, T3).
5. **The settled fraction vs local dark energy.** If the vacuum part converts into the clumped part where matter is dense, ρ_DE, and therefore a0, would vary with environment. The record's a0 is universal across SPARC, MeerKAT and wide binaries within its errors (≈ 0.1 dex), which roughly limits local changes in ρ_DE to ≲ 0.2 dex (a rough estimate, not computed here). A sharper environmental a0 test (field vs cluster discs) would tighten this.

## 5. Verdict (frozen rule)

**NOT DECIDABLE.** U-0, which is one field whose dust part has zero sound speed, survives. It has the same two dark constants as H2 and cannot be told apart from it. Every unified version that predicts something different is excluded or pushed to |α| ≤ 1e-6. The data that would decide are items 1–3 and 5 above.

**Standing.** κ = ½ is fitted. The cold energy's mass is still required, and its amount is an input. No dark-matter particle is claimed. This is not "theory closed".
