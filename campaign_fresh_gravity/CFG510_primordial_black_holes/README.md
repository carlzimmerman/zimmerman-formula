# CFG510: can the cold energy be primordial black holes? VIABLE-CONDITIONAL; the amount is a RESTATEMENT

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in 7d80348d8. The script is `cfg510_pbh.py` and runs in about 1 s.
- Main run: exit 0, because controls K1 and K2 pass.
- `CFG510_MUTATE=1`: exit 1. Both teeth were detected, as designed.

κ = ½ is FITTED. Both footings are scored separately and never pooled. PBHs add no new particle, but the cold energy's mass is still
required, and its amount (Ω_c/Ω_b = 5.364) is still an input. This is not "theory closed".

**Data caveat.** No PBH constraint curves are on disk. Every literature bound used here is RECALLED and UNVERIFIED. The curves that
would verify them need the owner's go; they are listed in section 6 of the criteria.

## Bottom line

Primordial black holes of about 1e17 to 1e22 g ("asteroid mass") could make up all of the cold energy. The conditions:
1. **The settling postulate.** The settled picture needs the cold energy to settle into the law's phantom. No mechanism for that is on
   the record, and PBHs close two of the routes the record had been trying.
2. **The recalled bounds.** The window's edges come from recalled literature values, not from curves on disk.
3. **A spike in the primordial spectrum.** It must be about 7 orders of magnitude above the CMB level, at k ~ 1e12 to 1e14 per Mpc,
   and its height must be tuned to about 0.03%.

The amount is not explained. The spike's height has to be chosen so that Ω_PBH equals the measured Ω_c, so the amount is a
RESTATEMENT: the input moves into the spike.

## Part A: L49 D1's ×1.82 galaxy failure, re-examined

**Where ×1.82 came from.**
- In L49 the MOND kernel was sourced by the TOTAL potential, and the cold mass was added as an abundance-matched NFW halo at f = 1.
  The kernel therefore amplified the added mass (double counting).
- K1 reproduces L49's row: median −0.259 dex, a factor of 1.816.
- PBHs failed in L49 only because every cold component failed that way. L49 never scored a PBH mass window.

**In the current (settled) picture.**
- The law reads the baryons only, and the settled cold mass IS the phantom. The rotation curve is then the law's by construction: the
  identity holds to 4e-16 (A1).
- **So the ×1.82 disappears, but only by the settling postulate, and for any cold component.** That is accounting, not a test.

| check | result |
|---|---|
| A2: can an isotropic collisionless population (PBHs, which have no pressure) sit in the phantom? (Eddington inversion, Hernquist host; Plummer control K2 good to 1e-5) | **Yes.** f(E) ≥ 0 at a = 0.3 r_M and a = 1 r_M. The result is the same at half and at double resolution. In units of r_M the 3 masses × 2 footings are one profile. Cutting the phantom off sharply at r_edge gives f/max ≈ −3e-4, inside tolerance. |
| A3: does granularity matter? (masses where two-body relaxation or dynamical friction acts within 13.8 Gyr: 31 cold-dominated MW UFDs and 3 disc hosts) | The smallest such mass is 0.27 Msun, in a UFD; the discs give 5e3 to 1e7 Msun. That is **10.7 dex above the window's top**, so in the window PBHs behave as a smooth collisionless fluid. Relaxation could only drive settling at masses Part B excludes. |
| A4: which settling routes are open to PBHs? | Superfluid pressure (FL1): **no**. The direct phonon coupling (CFG490): **no**, because a black hole carries no baryon charge; G9 then holds automatically. The khronon coupling: only through black-hole "sensitivities" (recalled, not computed). Relaxation: only above m_rlx. |

**Verdict: DISAPPEARS CONDITIONALLY (settling postulate). It is not RESOLVED.**

## Part B: the mass window for f_PBH = 1

**Open windows.**
- Robust table: **1.0e17 to 1.0e22 g** (5.0 dex).
- Maximal table, which adds the claimed extensions: **4.1e17 to 3.0e21 g** (3.9 dex).
- Everything else is closed by recalled bands:
  - evaporation below 1e17 g;
  - HSC, EROS/MACHO and OGLE microlensing, from 1e22 g to 30 Msun;
  - LVK merger rates, 0.5 to 300 Msun;
  - UFD heating, wide binaries, CMB accretion, Lyman-α and disc heating, from about 5 Msun upward.

**Derived cross-checks.**

| check | result |
|---|---|
| D1 Hawking | T_H(1e17 g) = 106 keV. The edge at 1e17 g is an emission bound, so it cannot be derived without data; it stays recalled. |
| D2 HSC lower edge | Wave optics gives 3.3e22 g (+0.5 dex): it **supports** the edge. Finite source with Sun-size stars gives 1.8e23 to 1e26 g: the derivation would **widen** the window upward. Flagged; the narrower recalled edge is kept for scoring. |
| D3 UFD heating (record UFDs, real cold mass) | Median m_max = 32 Msun (6 with the 1-D σ); the strictest UFDs give 1.0, 2.5 and 3.1 Msun. Recalled value: 5 Msun. **SUPPORTED** (+0.8 dex). |
| D4 LVK | With the recalled rate formula and its 1e-3 suppression, f = 1 is excluded only up to 62 Msun. The band edge is 300 Msun (+0.68 dex): **SUPPORTED** under the 1-dex rule, but the result is soft. Above 60 Msun other bands cover the range anyway. |
| D5 Poisson isocurvature on CMB scales | Δ²_S/A_s ≤ 5e-19: negligible. |

**Framework modifications.**
- **FM1.** The settled phantom is REAL mass; CFG447 excludes the force reading. So the dynamical bounds apply at full strength, with no
  relief.
- **FM2.** Settled halos, cut off at r_edge plus a smooth reservoir, give microlensing optical depths 0.67 to 0.85 × NFW, both to the
  LMC and to M31. The local cold density is 0.0057 / 0.0065 Msun/pc³, against NFW's 0.0076. **The bands are unchanged.**
- The phantom disc was not computed.

## Part C: formation and the amount

- **What it takes.** Making all of the cold energy from 1e17 to 1e22 g needs a formation fraction β ~ 4e-17 to 1e-14 (formation at
  T ~ 1e7 to 4e4 GeV). With δ_c = 0.45 that requires **P_ζ ≈ 0.015 to 0.018, about 7–9 × 10⁶ × A_s**, at k ≈ 7e11 to 2e14 per Mpc.
- **Compatible with the CMB.** The spike sits far beyond the CMB, large-scale-structure and μ-distortion range (all recalled), and the
  PBHs are adiabatic on CMB scales.
- **Tuning.** The exponential sensitivity is d ln f/d ln P_ζ ≈ 29 to 34. Holding Ω_c to its 1% Planck error therefore needs P_ζ to
  **0.03%**.
- **Not tied to the baryons.** Formation happens well before baryogenesis, so 5.364 would be a coincidence between the spike's height
  and η_b.
- **AMOUNT: RESTATEMENT.**

## Part D: distinctive predictions (if PBHs in the window are the cold energy)

- **Scalar-induced gravitational waves.** The peak runs from 1.2 mHz (1e22 g) to 0.36 Hz (1e17 g), with Ω_GW h² ~ 4–5e-9. That is
  about 1e3–1e4 above LISA's sensitivity (recalled). LISA/Taiji/TianQin, or DECIGO near 1 Hz, would either see the background or rule
  out Gaussian adiabatic formation across most of the window. Non-Gaussian spikes would weaken this.
- **A Hawking tail.**
  - With a critical-collapse mass function peaked at 2e17 g, 5.5% of the mass lies below 1e17 g, so it would show up in 511 keV / MeV
    gamma rays (COSI-class data).
  - Peaked at 1e18 g, the fraction below 1e17 g is 1.4e-4.
  - In effect, an extended mass function raises the window's lower edge.
- **Solar-System flybys.**
  - About 2 per year come within 1 AU at 1e17 g, and 2e-5 per year at 1e22 g.
  - An impulse at 1 AU moves a planet by about 0.1 m per decade at 1e20 g, and about 10 m at 1e22 g.
  - The top of the window could be tested by planetary ranging; this is a recalled proposal, and the data would need the owner's go.
- **Microlensing.** Wave optics (3e22 g) predicts chromatic, sub-geometric events at the window's top edge.

## MUTATE

- 1 Msun, 1e-9 Msun, 1e15 g and 1e4 Msun are each EXCLUDED, with the excluding bands named.
- Moving HSC's lower edge to 1e17 g closes the window, and the overall verdict becomes EXCLUDED.

## Caveats

- **The recalled bounds are the weakest link.** The window's edges move with the literature. In particular, newer evaporation analyses
  push the lower edge up, and HSC's lower edge is disputed. Disputed white-dwarf/neutron-star and retracted GRB-femtolensing bounds are
  not scored.
- **Assumed forms.** Press–Schechter with a recalled δ_c range, γ = 0.2, P_ζ = (81/16)σ², the critical-collapse form, the SIGW
  prefactor, the LVK rate formula and the halo inputs (MW 6e10 / M31 1.5e11 baryons; NFW 1e12 / 1.5e12) are all recalled. Each is
  flagged where it is used.
- **Part A tests whether a settled state can exist,** not whether the cold energy gets there. The settling mechanism is the open item for
  every cold reading on the record, and PBHs inherit it with fewer routes.
