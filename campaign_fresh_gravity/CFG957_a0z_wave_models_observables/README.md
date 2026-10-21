# CFG957: a wave in a0(z) — what could make it, and what else it would touch

**The oscillating-a0(z) hypothesis, including its refined form (the wave was larger early and shrinks over time, and today a0
is on the way down from a recent peak), is the owner's idea (2026-10-21).** The owner's sketch was a rough illustration; the
hypothesis is the general family.

## In plain language (for the owner)

Nothing already in the framework makes dark energy, and so a0, oscillate. The record's own natural rates for a dark-energy field
(H_Λ, a0/c, √(Gρ)) are all too slow, so a field with those rates only drifts, and gives no wave now or in the future. The
record's dark-energy partner and its cold-energy exchanges can only push in one direction. A wave needs one new ingredient: a light
scalar field with a mass of roughly 5–40 times the Hubble rate, which brings two new constants. That field gives your picture
naturally: Hubble friction makes the wave much larger early (its size grows as (1+z)³ going back in time), with a period of
1–9 Gyr. Whether a0 is on the way down today is a coin flip set by the mass (about 45–55% of masses), so it would have to be chosen.
How a0 reads dark energy matters a great deal. If a0 reads the energy density (the canonical reading), a0 can only ever decrease in
time: it can never have a peak. The wave appears only if a0 reads the pressure or the potential, the two other readings in the
record. In that case the expansion data see almost nothing, and only kinematic a0 measurements at z ≈ 2.5–5 can test it. Today's
galaxy points cannot. The wave-like pattern they show disappears once baryon-mass systematics are included. And if the CMB angle
θ* worked natively, it would probably shrink the testable high-z wave to below what any planned sample could see.

**Standing wording:**
- κ = ½ FITTED; the footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled.
- "Cold energy" is not a particle species.
- Not a closed theory. Nothing here says the data favour the framework.
- A bound on a wave is not evidence for a wave.

**Frozen design:** criteria 8e884c9a2b (committed alone, before any script or number).

**Split.** CFG956 owns the expansion-data bound (results aaa000a458, README c929d7548a). It is not recomputed here.
- Date note (2026-10-21): this lane's MAIN ran before CFG956 committed. By the frozen rule, no CFG956 number enters any computation
  here. Its committed headline is quoted below as context only.
- That headline: plain wave ε_95 = 0.032–0.08 for P ≤ 1.5 in ln(1+z); damped ε0_95 0.013–0.064 for P ≤ 1; no bound above
  z ≈ 2.5; the illustrative sketch at Δχ² +619.

## 1. Physical models (Part 1)

### The record's own rates: no wave (M1 R)
The threshold for oscillation in a Λ universe is m > (3/2) H_Λ = 1.237 H0 (D1). Every declared vacuum rate of the record (CFG245)
lies below it:

| rate | m / H0 | extrema of a0 in ε, −p, V: z ≤ 5 / z ≤ 10 / future to a = 100 |
|---|---|---|
| H_Λ | 0.825 | 0 / 0 / 0 |
| a0/c (canonical / alt) | 0.142 / 0.172 | 0 / 0 / 0 |
| √(Gρ) (canonical / alt) | 0.285 / 0.344 | 0 / 0 / 0 |

- The counts are the same at r_i = 0.01 and r_i = 1, and φ never crosses zero.
- A field set by the framework's own scales thaws and drifts. It never oscillates, in the past or in the future.

### A light scalar with a new mass (M1 X): the only route to a wave; two new constants (m, r_i)
- **Model:** V = V0 + ½m²φ², canonical, frozen start (φ̇ = 0 at z ≈ 1000), with V0 + ρ_φ(today) fixed to CFG689's best-fit dark energy.
- **Masses:** m/H0 ∈ {3, 5, 10, 20, 40}, declared as a map, never fitted.
- **r_max:** the largest initial field energy allowed by CFG689's 95% band at z = 1.0–2.33 (a band check, not a likelihood) and, in
  the −p reading, by −p ≥ 0.

| m / H0 | r_max (ε, V / −p) | onset z_osc | T_a0 = π/m | P_ln at z 0 / 1 / 2.33 | β fit | extrema z ≤ 5 (ε / −p / V) | a0 today (ε / −p / V) |
|---|---|---|---|---|---|---|---|
| 3 | 0.45 / 0.45 | 1.95 | 15.1 Gyr | 1.05 / 1.92 / 3.70 | — | 0 / 0 / 0 (10 future) | down / down / down |
| 5 | 0.67 / 0.67 | 3.24 | 9.1 Gyr | 0.63 / 1.15 / 2.23 | 3.85 | 0 / 2 / 2 | down / down / down |
| 10 | 2.48 / 2.48 | 5.79 | 4.5 Gyr | 0.31 / 0.57 / 1.13 | 3.34 | 0 / 5 / 4 | down / up / down |
| 20 | 17.9 / 7.90 | 9.75 | 2.3 Gyr | 0.16 / 0.29 / 0.56 | 3.21 | 0 / 11 / 10 | down / up / down |
| 40 | 57.5 / 7.73 | 16.1 | 1.1 Gyr | 0.08 / 0.14 / 0.28 | 3.13 | 0 / 22 / 22 | down / up / down |

- **Damping (larger early): natural.**
  - Field amplitude ∝ a^(−3/2), oscillation energy ∝ a⁻³ (D3), so the a0 wave's relative size grows as (1+z)^β with β → 3.
  - K4 gives 2.975 at m = 40 H0; the fits over [0, z_osc/2] give 3.1–3.9, above 3 where H/m is not small.
  - Above z_osc the field is frozen and a0 sits on a high plateau, √(1 + r_i) in −p.
  - In the ε reading the ripple is smaller by 3H/(2m) (D6), with β_ε ≈ 4.4.
- **Period: a chirp.**
  - The wave is periodic in cosmic time, with period π/m (the a0 frequency is 2m, D4).
  - In ln(1+z) its period is πH(z)/m, which lengthens with z. CFG956's fixed-P family is the e-fold version of this; the physical
    β ≈ 3 lies beyond CFG956's damped grid (β ≤ 2).
- **Phase today ("on the way down"): CHOSEN.**
  - On 400 masses in [3, 40] H0, a0 is falling today for 45.3% (−p) and 55.0% (V).
  - So "on the way down now" picks out about half the masses: a selection on m, not a prediction.
- **The ε reading: a THEOREM (D5).** dε/dt = −3Hφ̇² ≤ 0, so a0 never rises.
  - It is always "on the way down" (100% of masses), with zero extrema in every run.
  - "From a recent peak" is impossible for any canonical field.
  - A peak needs phantom dark energy (w < −1) or an energy inflow.
- **CFG689's own best-fit node curve** (D11, added after the criteria, report only) has exactly the owner's shape:
  - a0 is 1.12 × today at z ≈ 0.7, falling since;
  - in the ε reading that needs w_eff = −1.83 between z 1.0 and 0.7, which no canonical field can give;
  - CFG956 grades its significance (1.77σ from the z ≈ 0.7 peak). Constant dark energy is not rejected.
- **Energy and stability.**
  - No ghost; c_s² = 1; m² > 0; the null energy condition holds, so a canonical field cannot reproduce DESI's phantom crossing.
  - −p ≥ 0 binds at r_i ≈ 7.7–25. The frozen field keeps only ~1/π² of its energy at the first kinetic maximum (EdS j0, D2).
    My frozen hand estimate (r_i ≲ 1) was wrong by that factor.
- **CFG288's complex field on a circular orbit** has p_osc ≡ 0 (D4): no wave in any reading.

### The record's dark-energy partner (M2: CFG542 Pb, CFG630, CFG935 R-d): no wave
- u = ½φ̇² obeys du/dt = −6Hu − V′φ̇ + Q. At u = 0, du/dt = Q > 0 (D7), so the sourced partner can never turn around.
- MUTATE M-d confirms this: with Q = 0 the field has 3 sign changes of φ̇; with Q > 0 it has none, and min φ̇ > 0.
- The record's sink and an oscillating partner are therefore incompatible.
- Any rise is capped by ∫Q (CFG630: ≤ 3.8e-6 of ρ_DE), i.e. ≤ 8.3e-7 dex in a0.

### Cold-energy ↔ dark-energy exchange (M3: CFG131, CFG253, CFG360-DE C1, CFG630): no wave
- A w = −1 vacuum obeys ρ̇_DE = −Q exactly (D8), so ρ_DE can oscillate only if Q changes sign periodically. Every record Q is one-signed.
- Relaxation Q = Γ(ρ_c − Rρ_DE) gives det = −3HΓR < 0: a saddle.
- The only fixed point has ρ_c = 0, so complex roots would drive ρ_c negative.
- A sign-alternating exchange needs its own clock, which leads back to M1.

### Physical-model classes
| model | class |
|---|---|
| M1 with the record's rates | **NO WAVE** |
| M1 with a new mass m ≳ 5 H0 (−p or V reading) | **WAVE ONLY WITH NEW CONSTANTS** (m, r_i) |
| M1, ε reading (any m) | **NO WAVE** (theorem: monotone) |
| M1, complex circular field (CFG288 form) | **NO WAVE** |
| M2 the record's partner | **NO WAVE** (no turning point) |
| M3 exchange | **NO WAVE** (one-signed Q; saddle) |
| **Overall** | **NO PHYSICAL MODEL IN THE FRAMEWORK** |

## 2. Other observables (Part 2)

### (a) Galaxy dynamics over time
- **Predicted log10 a0(z)/a0(0)** at r_max (band-only; `cfg957.json` → `M1_X`):
  - low window (z 0.5–2): |Δ| ≤ 0.13 dex for every mass and reading, and ≤ 0.03 dex at z 0.5;
  - high window (z 2.5–5): up to +0.5 dex (ε, m 20), with the −p wave at m = 10 running −0.07 … +0.23 over z 1.5–5 and dipping to
    −0.70 at z 3 for m 20 (near −p = 0).
- **Testability** (frozen rule: |Δ| ≥ 0.15 dex at ≥ 2 redshifts):
  - low window: no curve qualifies;
  - high window: 6 / 4 / 5 redshifts for m 10 (ε / −p / V), 6 / 3 / 4 for m 20, 5 / 1 / 2 for m 40, and none for m 3 and 5.
- **Committed points** (panel d; K1 reproduces all 9 to 0):
  - no curve moves a z ≤ 2.3 point by more than 0.47 σ_stat;
  - at z 4.56 (ALPINE) the band-only ε curves at m 20–40 move it by 2.4–3.5 σ_stat;
  - with the 0.375-dex systematic floor every Δχ² is ≤ 1 in size.
- **Wave statistic T** (80 cosmic-time templates, look-elsewhere calibrated):
  - T_obs = 16.69, p_stat = 0.0005 (T_3σ 12.92); with the systematic floor T = 2.09, p_sys = 0.72.
  - **Label: PATTERN IN STATISTICAL ERRORS ONLY.**
  - The pattern is ALESS 122.1 (+0.95 dex) and ALPINE (+0.64 dex) sitting about 3σ above MeerKAT's level. Any rising curve takes it
    up, the rival too.
  - The 53 no-root galaxies at z ≈ 2–5 are excluded from the points, which biases them high, and baryon masses move s* by factors
    of 2–10 (CFG223).
  - Not a detection, and not evidence for a wave. With CRISTAL R_e in place of R_out: T 16.82, p 0.0010.
- **Galaxy response.**
  - T_a0 ≥ 1.1 Gyr against orbital times of 0.3–1.2 Gyr: adiabatic for m ≲ 20 H0. At m = 40 H0 the outer discs only partly follow.
  - In deep MOND a disc breathes as r ∝ a0^(−1/4).
  - A bin of Δ ln(1+z) = 0.2 keeps 0.81 / 0.96 of the wave at z 1 / 2.5 for m 10, but only 0.22 / 0.42 for m 40: short periods wash
    out in binned samples.
- **What would detect it:** kinematic deep-MOND a0 at ≤ 0.05 dex at ≥ 2–3 redshifts across z 2.5–5, spaced closer than half a local
  period. The record's decisive single point (z ≈ 2.5 at 0.10 dex, CFG689 P6) separates flat from a0 ∝ H(z); it does not see a
  wave on its own.

### (b) Today's d a0/dt
- (1/a0) d a0/dt runs from −0.27 to +0.08 H0 over every curve, i.e. |…| ≤ 1.9e-11 yr⁻¹.
  - m 10: ε −0.054, −p +0.019, V −0.018 H0.
- The record has no local constraint:
  - the Solar System is Newtonian through the stiffness term (CFG770);
  - the sealed wide-binary envelope has no a0 in it (CFG740);
  - the outer globulars are screened (CFG820);
  - there is no pulsar, LLR or laboratory a0 limit.
- **ALLOWED BUT UNTESTABLE NOW.**

### (c) Structure growth (the shear engine)
- **Lever.** The record's footing lever (Δa0 21%) is dΔχ²_KiDS/d ln a0 = 3.64 native (NC2x − NC1x) and 2.75 inherited (T2x − T1x).
  The footings differ in more than a0, so this is order of magnitude only.
- **The engine rectifies the wave.** It fills deficits and never removes surpluses (CFG932 Q4), so its cold energy tracks the
  running maximum of a0, not the average.
  - One-sided shift: |ΔΔχ²| ≤ 2.3 (maximum over z ≤ 3), ≤ 6.7 counting the frozen-era plateau to z 10.
  - Two-sided time average: ≤ 0.36.
- **No class change:** CONSISTENT → TENSION needs +13.4.
- **Sign.** A higher effective a0 adds cold energy and raises the lensing amplitude, so the wave can only reduce the framework's
  amplitude-driven lead (CFG909).
- **Fossil.**
  - The largest deep-MOND fossil, E_σ = ¼ ln(a0_max/a0_0), is +0.46 (m 40, ε, band-only r_max, frozen-era a0 × 6.3). That exceeds the
    dwarfs' +0.38, but only at amplitudes the θ*-tight bracket removes (estimate ≤ 0.17 there).
  - The one-sided rule would also leave the fossil in early-settled rotators, which sit on the law.
  - By CFG926's reading rule, a0 higher in the past is evidence about a0(z), not a rescue.

### (d) CMB: distance to last scattering and ISW (both see only ε, whatever a0 reads)
- **Distance.** At band-only r_max, δD_M(z*)/D_M = −0.77% to −1.87%, i.e. 27–65 σ of the θ* datum with no refit.
- **But the record cannot grade it.** CFG689's θ* rows are held back (K9 failed as frozen).
- **Post hoc (PH1, no weight):**
  - with curvature free, each shift is absorbed by ΔΩ_k = +0.005 to +0.012, inside CFG689 primary's ±0.048;
  - so θ* alone cannot exclude these amplitudes;
  - a joint θ* + BAO + SN fit (CFG689's T modes, Ω_k [0.000, 0.003]) probably would.
- **Post hoc (PH2, no weight):** the θ*-tight bracket (|δD_M/D_M| ≤ 3 × 0.029%, no refit) allows r_i ≤ 0.039 / 0.074 / 0.23 / 0.80
  / 2.9 for m 3–40. There every curve stays within 0.08 dex at z 2.5–5: **untestable**.
- **ISW proxy:** +4% to +8%, below the 20% an ISW detection could see.

### (e) BAO and SNe
- CFG956 (aaa000a458).

### (f) The signature
- **Flat, ΛCDM's emergent proxy and a0 ∝ H(z) are monotone.** The physical wave is not:
  - 2–22 extrema of a0 in z ≤ 5 (−p, V);
  - an amplitude rising with z as (1+z)^~3 to a frozen-era plateau;
  - a period of π/m in cosmic time.
- **It also breaks the tie between a0 and the expansion.** Kinematic a0 departs from √(ρ_DE(z)) inferred from BAO/SN by up to
  0.10 dex (m 10, −p) and 0.23–0.41 dex (m 20–40, V) at z 2.5–5.
- **Smoking gun:** a non-monotonic kinematic a0(z) at z 2.5–5 (a rise and a fall between neighbouring redshifts), larger at higher
  z, with no matching feature in the expansion history.
  - In the ε reading such a peak cannot occur (D5). Seeing one would mean phantom dark energy or a reading other than ε.
- **When:**
  - not with today's data: the best public a0 errors at z ≥ 2 are 0.4–0.5 dex (CFG685), and CFG689 P1 finds no sample at its 3σ
    needs;
  - not with the sealed ALMA discs (2026-11-06, 2026-11-28): single discs at z 1.42 and 2.0, below the window;
  - it needs a JWST/ALMA kinematic program with ≥ 3 deep-MOND points at ≤ 0.05 dex across z 2.5–5. No date is set.

## 3. Classes on both axes

| sub-hypothesis | phenomenology | physical model |
|---|---|---|
| H1 a wave at z ≤ 2.33 | **ALLOWED BUT UNTESTABLE NOW**: within CFG956's ε bound (3–8%); in M1 every curve is ≤ 0.13 dex at z ≤ 2, and no point moves > 0.47 σ | NO PHYSICAL MODEL IN THE FRAMEWORK (M1 X with two new constants, −p/V readings only) |
| H2 a wave at z 2.5–5, larger early | **ALLOWED AND TESTABLE** by the frozen rule. Window z 2.5–5; measurement: kinematic a0 at ≤ 0.05 dex at ≥ 2–3 redshifts. m ≈ 10–20 H0 qualify in −p and 10–40 H0 in V; m 3–5 do not. **FRAGILE:** the post-hoc θ*-tight bracket makes every curve untestable, and θ* is blocked by CFG689 K9 | same |
| H3 a0 on the way down today | **ALLOWED BUT UNTESTABLE NOW**: \|ȧ0/a0\| ≤ 1.9e-11 yr⁻¹; no local probe | M1: CHOSEN (about half the masses); ε reading: always down, but never from a peak (theorem) |
| H4 large low-z swings (like the sketch) | **EXCLUDED** by CFG956's committed likelihood (sketch Δχ² +619, aaa000a458; not computed here). Not reachable in M1 (≤ 0.03 dex at z 0.5) | NO PHYSICAL MODEL |

## 4. Controls

| | |
|---|---|
| **K** (cfg957_K.out) | 9/9 PASS: K1 points (worst 0), K2 band quantiles (0) and h (0.67683 vs 0.67696), K3a r_i = 0 → ratios ≡ 1, K3b EdS j0 7.5e-7, K3c energy identity 4.2e-9, K3d de Sitter (0 vs 10 crossings), K4 β_ρ 2.975, K5 rival (0) |
| **MUTATE** (cfg957_MUTATE.out) | 4/4 PASS: M-a planted wave at 3× the real errors detected 100% (T_3σ 12.92); M-b false positives 0.0047; M-c reversed friction β −6.0 vs 2.975; M-d partner 3 vs 0 sign changes |
| **Derivations** (cfg957_derivations.out) | 23/23 sympy checks PASS (D1–D10; D11 report only) |

## 5. Disclosures and post-hoc items (dated 2026-10-21)
1. **Order of runs.** MAIN ran before CFG956 committed, so "CFG956 pending" applied. CFG956's numbers above are quoted context; none
   enters a computation.
2. **Choices not fixed in the criteria,** made before the runs:
   - r_i ∈ {0.01, 1} for the record-rate runs;
   - φ_i = 1e-3 in K3b/K3d;
   - grid sizes;
   - seed 9575 for the CRISTAL R_e variant's null.
3. **D11 was added after the criteria** (report only).
4. **The post-hoc script** `cfg957_posthoc.py` (PH1, PH2) was written after MAIN. No class weight.
5. **The hand estimate for −p positivity was wrong** (r_i ≲ 1; the numerics give 7.7–25). D10's r ≤ 1 holds for the WKB
   oscillation energy, not for the frozen-era r_i (see D2).
6. **β fits** over [0, z_osc/2] include non-WKB stretches at small m (3.85 at m 5). The WKB limit is 3 (D3, K4).
7. **The band check** uses CFG689's marginal per-node 95% quantiles, not a likelihood.

## Files and rerun
- `FROZEN_CRITERIA.md` (8e884c9a2b)
- `cfg957_derivations.py` → `.out`, `.json`
- `cfg957.py` (`CFG957_MODE` = K, MAIN, MUTATE) → `cfg957_K.*`, `cfg957.*`, `cfg957_MUTATE.*`
- `cfg957_posthoc.py` → `cfg957_posthoc.*`
- `cfg957_figure.py` → `cfg957_a0z_envelopes.png`

Every run uses one core, nice 10, and < 0.35 GB; each takes seconds to half a minute:

```
OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_derivations.py
OMP_NUM_THREADS=1 nice -n 10 env CFG957_MODE=K python3 cfg957.py      # then MAIN, then MUTATE
OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_posthoc.py
OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_figure.py
```

The owner's idea (2026-10-21). κ = ½ FITTED; footings never pooled; not theory closed.
