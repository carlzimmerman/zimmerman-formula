# CFG723: is the carrier's mass "not the mass we think"?

**Label: only a carrier with a mass shell works.** Every route that tries to make cold energy's mass out of something other
than the rest mass of quanta fails at least one data requirement. The failures are large: by 5 to 12 orders of magnitude,
by having no inertia, or by being a single-stream flow.
- What survives is (B) a condensate/medium, and (D5) a rest mass induced by the vacuum. Both are honestly
  **VIABLE-AS-PARTICLE-IN-DISGUISE**: ρ = m n with quanta of mass m > 0.
- The owner's suspicion holds in one limited sense. The *amount* (Ω_c/Ω_b) and the *mass value* need not come from a
  freeze-out relic. But the *kind* of mass has to be inertial rest mass on a massive shell.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (e9238960c), 2026-10-13. The owner's addition (data-first
  evidence list and detection channels) went in before freezing.
- **Script:** `nice -n 10 python3 cfg723.py`. About 1 s, 0.15 GB, exit 0 (K1 and K2 PASS). Outputs: `cfg723.out`,
  `cfg723_results.json`.
  - `CFG723_MUTATE=1` writes the `_MUTATE` outputs and exits 0: M1, M2 and M3 all bite.
- **Settings:**
  - κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled.
  - ρ_DE = a₀²/(κ²c²G) per footing. Ω_b 0.0493 and Ω_DE 0.686 are CFG624's declared values.
  - Cold energy's mass is required. Not "theory closed". No ΛCDM or standard-MOND yardstick in any verdict.
  - Nothing was downloaded. Literature numbers are PROVISIONAL: the Bullet column Σ_x 0.1–0.3 g cm⁻² and the merger speed
    4700 km/s.

## 0. What the evidence says cold energy is (data first)
| # | property | lane |
|---|---|---|
| E1 | amount Ω_c/Ω_b = 5.364 at recombination; measured, not derived | THEORY_v3 §2; CFG642; CFG360 |
| E2 | collisionless and inertial: Bullet lensing follows the galaxies; an instant, inertia-free phantom is excluded (Z_B +7.9) | CFG624 G3; CFG621/623 |
| E3 | gravitates where the law alone is short: X-COP missing 3.09 / 2.75 M_b; cores ×1.8; LG timing; cosmic shear | CFG624 G2, G4a, G5; CFG687 |
| E4 | around galaxies it IS the law's phantom inside the census edge (SPARC unchanged) | CFG624 G1 |
| E5 | settled in bound systems with capacity Σ̄_c ≤ a₀/πG; core excess in massive systems open | CFG722 B8; CFG695 S4; CFG713–715; CFG720 |
| E6 | no non-gravitational signal: P has no visible channel. Detector nulls are context only (no lane) | CFG659 |
| E7 | not the P bound charge (net mass 2.7e-12) | CFG722 Q1 |

## Per-candidate table (canonical / alt where they differ)

| candidate | R1 amount (1+z = 1100) | R2 collisionless + inertial | R3 cluster / galaxy budget | R4 clusters like matter | R5 EP | R6 new constants | verdict |
|---|---|---|---|---|---|---|---|
| **A** P field energy (W + gradients + field) | e_max/(ρ_c,req c²) = **7.5e-12** (z = 0: 1.0e-2) | field-bound to baryons; no independent lump (CFG722 B2) | W/(ρ_ph c²) = **7e-9 to 6e-6**; ∫(W + phantom field)/(M_ph c²) ≤ **1.8e-5** (galaxies 1e9–1e12 at 0.1–10 r_M; cluster 1e14 at 1 Mpc) | w = −1 (W), −1/3 (gradients): not dust | yes (it is T⁰⁰), irrelevant | 0 | **FAILS** R1, R3, R4 |
| **B** condensate / superfluid medium, P = displacement | by input (abundance = Ω_c/Ω_b) | yes as a dilute gas: Bullet needs σ/m ≤ **3.3–10** cm²/g; the condensate needs σ/m ≥ **0.10–0.82** (thermalise at r_M in 13.8 Gyr) → window **OPEN**. Landau speed 0.13–3.7 m/s ≪ 4700 km/s, so superfluidity breaks in the collision | CONDITIONAL. It holds any amount. The core ×1.8 is the open CFG720 question, and under ID the tether expels core overflow (CFG722 Q4) | yes if produced cold non-thermally (an eV thermal relic is hot); m ≫ 2e-20 eV | exact (rest mass) | m (degenerate condensate needs m ≤ **16–143 eV**), σ/m, the production mechanism; plus the ID identification and basin anchor (structure, CFG722) | **VIABLE-AS-PARTICLE-IN-DISGUISE** |
| **C** vacuum-displaced energy | the vacuum must give up **5.1e8 ρ_DE0** by recombination. Late conversion is capped by flat a₀ (ρ_DE < 2% for z ≤ 5) at **0.052** of today's cold mass | vacuum (ρ+p)/c² = **0**: no inertia until it becomes w = 0 matter | local deposit of one rest mass needs η = (c/v)² = **2.2e6** (200 km/s) / **9.0e4** (1000 km/s), so the reaction force is ~1e5–1e6 × halo gravity (astra local_sink_reaction) | only after conversion to dust | the local reaction breaks momentum balance | conversion epoch / efficiency (+1) | **FAILS** (R1 late, R2, local energy-momentum). Early conversion = particle-in-disguise + 1 constant |
| D1 gravitating mass without inertia (phantom) | — | no (Bullet Z +7.9) | — | — | violates m_g = m_i | 0 | **FAILS** R2 |
| D2 coherent oscillation energy of P itself | amplitude free | — | — | quantum ħω₀ = **4.7e-31 to 6.6e-27 eV** (t_resp 0.28 Gyr → c_P = c); Jeans length **10–1400 Mpc** vs 6–7 kpc at 2e-20 eV | ok | amplitude (+1) | **FAILS** R4 |
| D3 baryon binding energy | (V_f/c)² = **3.9e-8 to 1.2e-5** (1e9–1e14 M☉) | — | — | — | — | 0 | **FAILS** R1 |
| D4 irrotational geometric dust (mimetic-type) | amount = integration constant (free) | single-valued flow fails stream crossing / mergers (CFG288, L374) | — | — | ok | +1 | **FAILS** R2 |
| D5 rest mass induced by the vacuum, m(ρ_DE) | by input | as B or plain collisionless | as B | as B | ok while ρ_DE is homogeneous and flat (< 2%) | coupling for m(ρ_DE) | **VIABLE-AS-PARTICLE-IN-DISGUISE** |

**General statement (sympy, in the script).** A cold, collisionless, multistream component obeys a Vlasov equation on a mass
shell. Its group velocity is v = pc²/E. That velocity goes to 0 as p → 0 only if m > 0. With m = 0, every quantum moves at c
(hot); M3 bites. So R2 together with R4 forces a massive shell. This is why A, C, D1–D4 cannot pass:
- A and D3 energies are bound to baryons and suppressed by (V/c)².
- Vacuum energy has no inertia.
- The phantom has no inertia.
- Geometric dust is single-stream.

## Answers to the brief
- **(A)** P's energy density is set by a₀²/G ~ 4e-3 ρ_DE c² (from W(a₀/2) = 0.193 a₀²/4πG). It is about the gravitational
  binding energy of the system it sits in: (V/c)² of the rest mass. In halos ρ_ph/ρ_DE = 1e2–1e7, and the field energy covers
  only 1e-8 to 2e-5 of the needed phantom mass. At recombination it falls short by 1.3e11. It is also not dust. M1 confirms that
  the whole deficit is the (V/c)² factor: rescaling by (c/V_f)² brings A1 to 0.48.
- **(B)** The medium supplies CFG722's identification for free. With ∂_tP = −j, continuity gives ∇·P = ρ − ρ̄ exactly
  (sympy; 1-D numeric 3.5e-13), so the tether selector of CFG722 fits naturally onto any medium. The saturating W is still the
  framework's input, not a property derived from the condensate.
  - Its mass is m n, a particle with a free mass.
  - The condensate branch needs m ≤ 16–143 eV, and a self-interaction window 0.1–0.8 ≤ σ/m ≤ 3.3 cm²/g (Bullet bracket
    PROVISIONAL). It also needs cold non-thermal production.
  - **Side finding:** astra's cold-production benchmark daughter (m = 193.5 eV, BOSE_ENDPOINT) is *above* m_deg at r_M for
    every halo mass here. Its condensate endpoint would therefore be a non-degenerate gas inside halos. The 0.62 eV
    microscopic-carrier benchmark is degenerate.
  - In the Bullet the relative speed is ~1e6 × the coherent sound speed, so the subclusters pass as normal collisionless gas
    (τ < 1), not as a superfluid.
- **(C)** Supplying the cold mass from the vacuum requires either:
  - a vacuum ≥ 5e8 ρ_DE0 that was emptied before z = 1100. Then a₀ = κc√(Gρ_DE) would have been ≥ 2e4 × larger then, and the
    abundance becomes a free conversion constant. After conversion it is ordinary dust, i.e. a particle-in-disguise; or
  - late conversion. Flat a₀ caps that at 5% of the need, and the local deposit forces a reaction 1e5–1e6 × halo gravity.

  Vacuum energy has zero inertial density, so before conversion it cannot be the Bullet's inertial mass.
- **(D)** Only D5 survives, and it is a particle whose mass is set by the vacuum. That is a genuine "not the mass the way we
  think" option for the *origin of m*, but not for the *kind* of mass.

## Most promising route and what would test it
The surviving route is **B + D5**: a cold, collisionless medium of quanta whose displacement IS P (so ∇·P = ρ_c − ρ̄_c and the
CFG722 tether follows kinematically), with its rest mass possibly set by the vacuum. Tests:
1. The self-interaction window. A condensate branch predicts σ/m between ~0.1–0.8 and ~3 cm²/g. That would show as
   merger-offset / core-shape effects. A firm σ/m < 0.1 cm²/g kills the *condensate* branch but leaves the plain
   collisionless branch.
2. The merger lag set by the action (CFG720, queued). Under ID the carrier oscillates back onto the instantaneous all-baryon
   law on 0.05–2.4 Gyr.
3. Whether the core ×1.8 can be held at all under ID (CFG722 Q4 says the tether expels it). This is the sharpest internal
   test.

## Detection / interaction channels for the survivors (B, D5)
| channel | size | sensitivity / status | label |
|---|---|---|---|
| finite supply / census edge in galaxy lensing or satellites | edge beyond R_HI for f_ret ~ 0.1 (CFG624); SAGA LAW-FLAT but FRAGILE (CFG562) | existing lensing / satellite data only marginally sensitive | FUTURE |
| double-pulsar extra decay / c_P floor | closest P channel at **4.2e-2** of the allowed room; c_P > 1.7e-3 c at L* 5.75 pc | CFG659 | BELOW THRESHOLD (near-term timing could reach it) |
| Gaia DR4 MW vertical force / wide binaries | sealed values | pre-reg, release 2026-12-02 | FUTURE |
| Bullet-like merger lag | d = v t_resp = **288–1346 kpc** in the slow corner (t_resp 0.06–0.28 Gyr); ID oscillation 0.05–2.4 Gyr | CFG720 queued; observed offset f_obs 0.045 ± 0.125 (CFG624) | OBSERVABLE (existing mergers) |
| self-interaction implied by a condensate | σ/m 0.1–0.8 to 3.3 cm²/g | merger offsets, cluster cores (literature PROVISIONAL) | OBSERVABLE |
| lab / Solar System | unscreened law δg/g ~ a₀/g_N = **9.5e-12** (Earth surface), **1.6e-8** (1 AU), **1.4e-6** (Saturn); the absolute anomaly ~ a₀ would be excluded by ephemerides unless screened. The record screens below L* = 5.75 pc (CFG691); not re-adjudicated here | — | BELOW THRESHOLD (conditional on CFG691 screening) |
| direct detection / light | the carrier couples only gravitationally (no SM or A_μ term, CFG659) | zero signal predicted | BELOW THRESHOLD (null predicted) |
| a₀ flat with z (ρ_DE flat; constrains C and D5) | a₀ ∝ √ρ_DE | ALMA U4_27928 (11-06), GS4_24110 (11-28) | FUTURE |

## Controls and MUTATE
- K1: phantom density integrates to M_b(ν_s − 1), max relative error ≤ 1e-6. PASS.
- K2: ∇·P = ρ − ρ̄ under ∂_tP = −j holds in sympy and numerically to 3.5e-13. PASS.
- M1: field energy at (c/V_f)² weight brings A1 to 0.48. Bites.
- M2: vacuum with w = 0 gains inertia. Bites.
- M3: m = 0 shell cannot be cold. Bites.

## Disclosures
1. **A2 as frozen is ill-posed.** With a point mass, ∫g²/8πG diverges as 1/r_in (the baryons' own Newtonian self-energy).
   The frozen number (r_in = 1e-4 r) is reported unchanged and reaches 6.9 at 0.1 r_M for 1e12 M☉. It measures the baryons'
   binding, not a cold mass.
   - A post-hoc A2′ = ∫[W + (g² − g_N²)/8πG]dV/(M_ph c²) excludes it and is ≤ 1.8e-5.
   - The A verdict rests on A1, A3 and A2′. A1 and A3 alone already fail by ≥ 5 orders.
2. Verdict strings for C, D1, D3, D4 and D5 are structural (from cited lanes and sympy), not thresholded numbers. The
   verdicts for A, B and D2 are computed from the frozen thresholds.
3. B2 uses a pure-contact rate n σ v with no Bose enhancement, and the density at r_M only. The criteria disclose
   back-of-envelope orders held before freezing.
4. The Solar-System line is unscreened arithmetic. Whether the law's absolute residual ~ a₀ survives ephemerides depends on
   the CFG691 screening, which this lane does not test.
