# CFG725: does the condensate carrier's self-interaction window survive the record's merger and core data?

**Label.**
- **Merger offsets: the window stays OPEN** in every variant run.
  - As frozen: **OPEN-PARTIAL (canonical) / OPEN (alt)**. The merger bound σ/m ≤ 0.708 cm²/g on both footings sits inside
    the condensate window, which starts at 0.146–0.82 (can) / 0.105–0.59 (alt).
  - Post hoc the merger bound is fragile: 0.45 to 10 cm²/g depending on the profile choices. It is never below the window's
    low end, so it never closes the window.
- **Dwarf cores: σ/m-blind (NOT DIAGNOSTIC).**
- **Cluster cores: NOT DIAGNOSTIC as frozen.** The bracket on σ/m_max runs from 0.03 to 1.41 cm²/g, which straddles the window.
  This is where the question will be decided.
- **MUTATE FAILS as frozen.** M1 bites. M2 and M3 bite on the Bullet statistic but not on the Harvey statistic; the cause is
  in Disclosures.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4f9022839), 2026-10-13.
- **Scripts:**
  - `nice -n 10 python3 cfg725.py` → `cfg725.out`, `cfg725_results.json`. About 15 s, 0.18 GB, exit 0 (K1–K4 PASS).
  - `CFG725_MUTATE=1 …` → `cfg725_MUTATE.out`, `cfg725_results_MUTATE.json`. Exit 1: M2 and M3 fail as frozen.
  - `cfg725_posthoc.py` → `cfg725_posthoc.out`, `_results.json`. Not frozen; carries no verdict weight.
- **Settings:**
  - κ = ½ FITTED. Footings are never pooled.
  - "Cold energy"; its mass is required. Not "theory closed". No ΛCDM or standard-MOND yardstick in a verdict.
  - 1 cm²/g = 0.1 m²/kg (CFG428's correction, asserted in K4).
  - Nothing was downloaded. PROVISIONAL inputs: the Bullet lensing masses (Paraficz+16, recalled), Harvey+15's
    β = −0.04 ± 0.07, and the LITTLE THINGS baryon subtraction.

## (a) Merger offset vs σ/m (derived)

**Which population the merger probes.**
- At merger speed every quantum scatters, tethered or free. Superfluidity breaks at a Landau ratio of ~1e6 (CFG723 B5), and the
  tether is a mean-field force that does not depend on velocity.
- The sub's lensing peak inside 250 kpc is mostly the **free** population: 1 − Σ_cap/Σ̄_dark = 0.77 / 0.73 (can / alt).
- The primary branch ALL lets every quantum scatter. The brief's FREE-only branch gives a weaker bound: 1.26.

**Kinematics (derived, Monte Carlo check K3 to ≤ 0.5%).**
- Scattering is isotropic, between equal masses, by contact (s-wave; independent of velocity for an eV-scale λ|ψ|⁴ well
  below any resonance).
- The bound remnant keeps a fraction η = x⁴/2 of the relative momentum per scattering, with x = min(v_esc/V, 1). Quanta that
  escape leave without moving the remnant's centroid.
- Drag: a_d = η(σ/m)ρ_tgt V². The galaxy–carrier separation then obeys δ̈ = a_d − ω²δ, with ω² = (4π/3)Gρ₀,sub.
- In the impulse limit:

  **δ_max ≈ η (σ/m) Σ_tgt V / ω, and β ≈ w δ / d_SG**, where w is the carrier's share of the lensing peak.

  Numbers: Σ_tgt(0) ≈ 2000 M☉ pc⁻² (r_c = 100), V ≈ 3900 km/s, T_osc = 0.56 Gyr. This gives max|δ| = 41 / 44 kpc per cm²/g.

**Scored with CFG623's own estimator** on its VALID α = 0 runs, with the SI shift added to the sub's lensing peak:

| σ/m (cm²/g) | f (can) | Z_B | β̄ (can) | Z_H | status |
|---|---|---|---|---|---|
| 0 | +0.181 | +1.09 | +0.063 | +1.47 | ALLOWED (= CFG623, M1 to 0) |
| 0.1 | +0.196 | +1.20 | +0.060 | +1.42 | ALLOWED |
| 1 | +0.325 | +2.24 | +0.030 | +1.00 | EXCLUDED (by f) |
| 10 | +1.62 | +12.6 | −0.270 | −3.29 | EXCLUDED |

- **σ/m_max (merger, primary configuration) = 0.708 / 0.708 cm²/g.** The Bullet's f does the excluding. Harvey's β̄ *falls* as
  σ/m rises, because its window (0.2–0.6 Gyr after pericentre) samples the second half-cycle of the galaxy–carrier oscillation.
- **Variants (post hoc unless frozen as a bracket):**

  | variant | σ/m_max (cm²/g) |
  |---|---|
  | r_c 50 / 100 / 150 (frozen bracket) | 4.5 / 0.71 / 0.45 (can); 4.0 / 0.71 / 0.45 (alt) |
  | FREE branch | 1.26 |
  | seeds 603–605 | 1.0–1.4 (can seed 605: baseline unscorable, the known R-2 issue) |
  | v_esc 3500 / 3000 / 2500 / 2000 km/s | 1.1 / 2.0 / 4.0–4.5 / 10 |
  | phase-mixing damping Q = 2 / 1 | 1.0–1.1 / 1.3–1.4 |

- **Fragility, verified as hard as a pass.** The frozen v_esc of 4110 km/s comes from a data-normalised pseudo-isothermal sub
  of 7.2e14 M☉ in total. That is 4.8× CFG623's sub progenitor (1.5e14), so x = 1 and η sits at the drag-limit value ½. The
  frozen primary bound is therefore the *tight-side* end.
- Every variant gives ≥ 0.45 cm²/g. That is above the condensate's least demanding threshold (0.146 / 0.105), so **no merger
  variant closes the window.**

## (b) Cores vs σ/m (derived)

**Tethered population.**
- Its static minimum is the law's profile (CFG722 B4/B5). A quiescent condensate has no relative motion, so nothing scatters.
  **Its core does not depend on σ/m.**
- DW1, LITTLE THINGS (22 dwarfs, 742 points, checksum OK): 2.2% / 1.8% of points lie above Σ_cap, and only DDO 101 and
  NGC 3738 (can) / NGC 3738 (alt) are > 2σ above. The median Σ_dark(<R) is 29 M☉ pc⁻², about 0.14 of the capacity.
- So dwarfs hold no free population (NGC 3738 is the one exception, see Disclosure 5), and **dwarf cores carry no σ/m
  information in this theory (NOT DIAGNOSTIC)**. Dwarf-core SIDM limits do not transfer.

**Free population (cluster cores).**
- It is an isothermal sphere in its own potential plus the baryons plus the tethered mass at capacity, with central density
  ρ₀ = A/((σ/m)⟨v_rel⟩t_age).
- Derived relation (self-gravitating case, σ_v = 1000 km/s, t = 10 Gyr, A = 1):

  **r₀ ≈ 280 kpc (σ/m / 0.1)^½ (σ_v/1000)^{3/2} (t/10 Gyr)^½ A^−½ and Σ₀ ∝ (σ/m)^−½**

  Fitted slopes are exactly +0.500 / −0.500. Examples: Σ₀ = 1170 M☉ pc⁻² at 0.1 cm²/g and 370 at 1 cm²/g.
- Thermalisation threshold for the Bullet's free cores (observed free Σ̄(<250 kpc) = 812 / 728 can; 768 / 684 alt):
  σ_th = 0.065–0.40 cm²/g. **So the condensate branch predicts thermalised, cored free cluster cores.**
- Data bound over the 24 frozen bracket corners: **σ/m_max = 0.032–1.41 cm²/g → NOT DIAGNOSTIC.**
  - The A = 1, t = 10 Gyr, σ_v = 1000 corners give 0.06, below the window. The A = 4, t = 5, σ_v = 1300 corners give 1.1–1.4.
  - Even at σ/m → 0 an isothermal free population with σ_v = 1000 km/s barely reaches the observed column. It saturates at the
    singular-isothermal ceiling of ~700 M☉ pc⁻² (M1 log). So σ_v, the age and the matching factor A set the answer, and none
    of them is measured on disk.
- Context only, not a verdict input: Sagunski+21's cluster limit of 0.35 cm²/g (ΛCDM-halo Jeans modelling) falls inside this
  NOT-DIAGNOSTIC band.

## (c)/(d) Combined window and verdict

| footing | condensate needs σ/m ≥ | merger σ/m_max (primary) | cores | S_max | verdict as frozen |
|---|---|---|---|---|---|
| can | 0.146 (1e9 M☉) … 0.820 (1e12) | 0.708 | NOT DIAGNOSTIC (0.03–1.41) | 0.708 | **OPEN-PARTIAL**: halos with M_b 1e9–1e11 can condense; 1e12 would need 0.82 |
| alt | 0.105 … 0.589 | 0.708 | NOT DIAGNOSTIC | 0.708 | **OPEN** |

Reading:
- The window is open for dwarf to L* halos on both footings in every variant.
- Condensation in MW-mass (1e12) halos on the canonical footing is excluded only by the tight-side merger configuration. The
  post-hoc v_esc and damping variants (bounds 1.0–10) re-open it. This is not a robust exclusion.
- Wittman+18 (record row A09d) would weaken the Harvey side further. That side does not bind here.

## The single cleanest deciding measurement
**The central density of the free cold-energy component in relaxed cluster cores**: ρ₀,free = ρ_lens − ρ_baryon − ρ_tether(cap),
from strong lensing plus BCG stellar kinematics inside 10–300 kpc.
- The condensate branch requires ρ₀,free ≤ A/((σ/m)⟨v_rel⟩t). With σ/m ≥ 0.146, σ_v = 1000 km/s and t = 10 Gyr, that is
  **ρ₀,free ≲ 1.4–5.7 × 10⁻³ M☉ pc⁻³** (A = 1–4). For condensation up to 1e12 halos (0.82) it is ≲ 2.5–10 × 10⁻⁴.
- A free core denser than ~6e-3 M☉ pc⁻³ in an old relaxed cluster closes the condensate branch. A core radius growing as
  (σ/m)^½ σ_v^{3/2}, with r₀ of a few hundred kpc, is its positive signature.
- A measured free-component σ_v and the core age are needed alongside, because they are what leaves the on-disk bracket open.

## Controls and MUTATE
- K1: oscillator vs analytic, 2.0e-12. K2: isothermal asymptote 3.2% (≤ 10%); projection 8e-13; the reported 2-D check is
  2.6e-4. K3: isotropic-scattering Monte Carlo, 0.04–0.5%. K4: units. **All PASS.**
- **M1 bites:** σ/m = 0 reproduces CFG623 α = 0 to 0.0, and the core model gives no bound at 1e-6.
- **M2 FAILS as frozen.** σ/m 0.3 → 3: f 0.224 → 0.612 and Σ̄_free 328 → 53 both move as derived, but β̄ 0.053 → −0.037.
- **M3 FAILS as frozen.** With the drag flipped, β̄ = 0.163 > 0.063. The f half bites: f = −0.25 vs +0.18.

## Disclosures
1. **MUTATE β̄ teeth were mis-specified.** Both failures have one cause. Harvey's window (opening at d_SG ≥ 200 kpc, 0.21 Gyr
   after pericentre) falls in the second half of the T = 0.56 Gyr galaxy–carrier oscillation, where an undamped offset has
   reversed sign.
   - With phase-mixing damping Q = 1, β̄ rises with σ/m, as the frozen tooth assumed: 0.065 → 0.080 (post hoc).
   - The verdict rests on f, whose teeth bite. MUTATE exit 1 stands as recorded.
2. **The SI layer post-processes CFG623's collisionless run.** It is not an N-body run with scattering.
   - The galaxies' back-reaction enters only through ω.
   - Mass loss changes the peak height but not its position.
   - Stability flags are as-run.
   - CFG623's progenitors underweight the Bullet (CFG625 M-RAW not met).
3. **The frozen v_esc comes from an over-massive truncated profile** (7.2e14 vs 1.5e14 M☉). The merger bound of 0.708 is the
   tight-side value (disclosure P1/P2).
4. **The core model's isothermal ρ₀ matching factor A, σ_v and t_age are brackets, not derived.** In this theory the free
   population's formation profile is not derived (CFG722: a phase label on the carrier), which is why the core relation has an
   open O(1) matching.
5. LITTLE THINGS DM-only curves depend on Oh+15's stellar M/L.
   - DDO 101 crosses the capacity at one point only (0.26 kpc, 216 M☉ pc⁻², > 2σ).
   - **NGC 3738 is above capacity over its whole measured curve** (0.08–1.75 kpc; 2σ-lower Σ up to 880 M☉ pc⁻², 2–4× the
     capacity). It is the one dwarf that could hold a free population, so it is the one dwarf whose core could carry σ/m
     information here. It was not evaluated, and it does not change the frozen DW1 rule (≤ 3 galaxies).
6. Back-of-envelope orders were seen before freezing (stated in the criteria). The numbers in this README are from the committed
   outputs.
