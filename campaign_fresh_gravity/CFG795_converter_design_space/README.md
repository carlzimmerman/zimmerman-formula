# CFG795: the converter design space for a hypothetical cold-energy ramjet

**Label: CLOSED within the framework. One conditional window outside it, and that window is the framework's own kill test.**

HYPOTHETICAL. All external bounds are quoted from memory or web summaries, so they are provisional. Criteria are in
`FROZEN_CRITERIA.md` (2be9ffbb1). Run `nice python3 cfg795.py` (seconds, exit 0). `CFG795_MUTATE=1` exits 1 by design.

η is the light out divided by the cold-energy power intercepted (ρc²v₀ = 14 W/m²). The target is η ≥ 0.01. The reference
intake is 1 mg/m².

| class | η_max | bound that sets it |
|---|---|---|
| P1 per-mass (nucleons, bound e) | 6e-19 | Earth heat flow (night sky 1000× weaker). τ₀ ≥ 3e17 yr at **any** areal mass |
| P2 free electrons (Al foil) | 7e-18 | Earth's metallic core would out-heat 47 TW |
| P3 axion-like, 2.4 eV / 2.24 meV | 4e-20 / 4e-14 | CAST/HB g, B = 1e3 T, gain 1e6 |
| P4 kinetic mixing, 2.4 eV | 1e-19 | stellar ε ≤ 1e-14, gain 1e6 |
| P4 kinetic mixing, 2.24 meV (native) | 5e-8 | solar-relation ε ≤ 6.25e-9, gain 1e6 |
| P5 superconductor-gated | 1e-16 | SNSPD dark counts (neutron-star heating does not constrain: 2450 K) |
| P6a laser stimulation | 0 | detailed balance: a laser mode fuller than the cold modes reverses the flow |
| P6b phase-locked, 2.4 eV | 0 | phase unmeasurable (ε√N short by 5e11) |
| **P6b phase-locked, 2.24 meV** | **0.6** | quantum phase noise; ε within 1.6× of its weakest bound |
| P7 2–3 eV resonance | 6e-19 | natural matter already has bands at 2–3 eV, so the P1 bound applies |
| P8 gravity only | 1e-50 (ceiling 3e-7) | only kinetic energy is reachable |
| P9 framework screening (R1) | 3e-27 at 10 km | (d/L*)²; η = 0.01 needs a 0.57 pc device |

**Controls.** K1 gives 162.7 lux (CFG792: 160) and K2 gives 38.0× (38): both PASS. MUTATE ρ_c = 0 zeroes both natural
excesses and leaves P9 unchanged, so the tooth bites.

## Reading
1. **Every linear, material or field-gated portal fails by ≥ 2 × 10⁵.**
   - Natural matter always has a far larger column than a device: Earth's air, rock and core.
   - Nature also has the gating states: magnetars, neutron-star superconductors, plasmas at every frequency, and 2–3 eV
     bands.
   - Lab detectors (SNSPDs) see nothing.
   - Stimulating with a laser cannot help, because net flow needs the target mode emptier than the cold field.
   - The 2–3 eV line is the worst case.
2. **The least-constrained window** is coherent, phase-locked extraction.
   - **What it assumes:** cold energy behaves as a 2.24 meV vector field with kinetic mixing ε ≈ 4e-9 to 6e-9.
   - **How it works:** every 0.72 m coherence cell has its phase measured at the quantum limit. It is then nulled by a local
     542 GHz field, all within its 3 μs coherence time. A 100 km² intake holds about 2e8 such cells.
   - **What it needs:** a local field of 6e11 V/m. That is beyond any material. With a 1e6 resonant gain and the dish
     geometry it falls to 1.6e7 V/m.
   - **Why it is marginal:** it needs ε within 1.6× of the solar-relation bound. The XENON10 bound (κm < 3e-12 eV, checked
     after the freeze: ε ≤ 1.3e-9) closes it under the frozen formula. It stays open only under the looser post-hoc
     dish-geometry estimate (s = 150).
   - **The τ₀ in the table is not a real ship time:** the 0.26 yr assumes a 1 mg/m² device, and no phase-locked device
     is that light.
3. **The decisive obstruction is the framework itself.**
   - In reading R1 (cold energy is the bound charge of the stiff P field), stiffness screens any device response by
     (d/L*)² = 3e-27 at 10 km.
   - In reading R2 the record gives cold energy no coupling except gravity, so η ~ 1e-50.
   - The one window requires a visible 542 GHz line. ARGON03/CFG723-E6 pre-registers that line as a framework kill.
   - **So a working converter and this framework cannot both stand.** A sub-mm dish search at ε ≳ 1e-10 decides it either
     way.

**η ≥ 0.01 is reachable nowhere inside the framework.** Outside it, η ≥ 0.01 needs a hand-added portal that sits at
current bounds and that a tabletop search can exclude.

## Disclosures
- The P6b efficiency formula η = 1 − 1/(ε²N) was set after the freeze. The frozen criteria fixed only the
  phase-measurability test ε√N ≥ 1. The dish-geometry s = ε²(c/v)N is a looser post-hoc estimate.
- The XENON10 and SNSPD numbers come from web summaries (arXiv 1401.8287-class reanalysis; Chiles et al. LAMPOST).
- P9 uses the record's (d/L*)² scaling. It is not a solved device problem.
- κ = ½ fitted; not theory closed. No dark matter particle species is adopted. P3/P4/P6 are hypothetical portals.
