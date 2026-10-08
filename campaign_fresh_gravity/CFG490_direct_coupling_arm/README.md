# CFG490: the direct-coupling arm of the fork. No Lagrangian coupling delivers; the only delivery is a rule (DELIVERS: no clean pass)

**This arm violates G9 by construction.** G9 (CFG329) is the rule that matter couples to the metric only, so the cold fluid
feels baryons only through gravity. Every coupling tested here lets the cold fluid respond to baryons directly. That is the
point of the lane: it is a **labelled experiment** (owner, 2026-10-08), testing arm (a) of the fork in
`WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md`.

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in b385f4306. The script is `cfg490_direct_coupling.py` and
runs in about 18 s.
- Main run: exit 0, because controls K1–K5 pass.
- `CFG490_MUTATE=1`: exit 1. The teeth were detected, as designed.

κ = ½ is FITTED. Both footings (a₀ = 9.36e-11 and 1.13e-10 m/s²) are scored separately and never pooled. The cold fluid's
mass is still required, and its amount (Ω_c/Ω_b = 5.364) is an input. Where a coupling needs a field quantum, that is said
plainly below. This is not "theory closed".

## The question

The G9-respecting arm has failed three ways:
- **CFG461:** no G9 mechanism sets the temperature σ⁴ = G M_b a₀/4.
- **CFG462:** the khronon lapse has no f_b in it, so it cannot stop settling at r_edge = 5.85 r_M. The edge appears only if
  the supply is exactly the cosmic share, 5.364 M_b.
- **CFG488:** the per-galaxy supply can only be enforced with a shared baryon–cold label, which is a direct coupling.

So: does the minimal direct coupling that would enforce the supply rule ("each galaxy settles exactly 5.364 × its own baryons,
within the edge") also deliver the edge and the temperature, with at most one new constant? And does it survive the bounds a
direct coupling must face?

## The couplings (written out; all scored, none dropped)

All of them use the record's F-H settling drive (CFG462). Its mobility and its energy sink (CFG381's +1 coupling) are
inherited from the G9 arm and are not counted here. The sink stays NOT SUPPLIED (CFG462).

| | coupling | form | new constants |
|---|---|---|---|
| C1 | Berezhiani–Khoury phonon (the owner's named form) | L_int = −(αΛ/M_Pl) θ ρ_b, P(X) ∝ Λ(2m)^{3/2} X\|X\|^{1/2}, a₀ = α³Λ²/M_Pl | m, α, relaxation rate = 3 |
| C2 | neutralising U(1): the minimal **Lagrangian** enforcer | L_int = −A_μ(e_b J_B^μ − e_c J_c^μ), massless vector on baryon number and the cold current | α_N = 1 (the charge ratio is derived) |
| C3a | supply-transfer gate, auxiliary field: the minimal **rule-level** enforcer | ∂_t ρ_s + ∇·(ρ_s v_s) = +J, ∂_t ρ_u + ∇·(ρ_u v_u) = −J, J = Γ ρ_u Θ(−E·ĝ), ∇·E = 4πG(s ρ_b − ρ_c) | s = Ω_c/Ω_b inserted = 1 (flag R) |
| C3b | the same gate, reading the sign of C2's gauged field | as C3a with E the U(1) field | α_N = 1 (value irrelevant) |
| C4 | drag (momentum exchange) | ∂_t v_c ⊃ −ρ_b κ_d \|v_rel\| (v_c − v_b), κ_d = σ_T/(m_χ + m_p) | κ_d = 1 |

**Why C2's charge ratio is not a free constant.** In a homogeneous, isotropic universe a gauged charge must have zero mean
density: there can be no background field, so Gauss's law forces neutrality. That fixes e_c n_c = e_b n_B, so per unit mass
the cold charge is 1/S of the baryon charge (K1b). The galaxy is then neutral exactly when it has settled S × its baryons.

## Verdict

| coupling | DELIVERS | SURVIVES | constants | field quantum (dark-matter particle)? |
|---|---|---|---|---|
| C1 BK | FAIL | FAIL | 3 | **yes**: a superfluid of quanta, m = 1.0 eV at α = 1 in the best case |
| C2 U(1) | FAIL (window closed by 2.6–3.0 dex) | FAIL (MICROSCOPE by 14.4 dex at the strength it needs) | 1 | **yes**: a charged cold field, plus a massless baryon-number gauge boson |
| C3a gate | PASS-R (the one constant IS the edge definition) | VACUOUS (no listed bound can see it) | 1 | no (an auxiliary field, no Lagrangian) |
| C3b gate | PASS-NA (gate unreadable: thermal contrast 2.4e-16) | PASS (CONDITIONAL on inherited settling physics) | 1 | **yes**, as C2 |
| C4 drag | FAIL | FAIL (CMB by 5.8 dex, Bullet by 2.6 dex) | 1 | **yes**: a scattering cross section needs quanta |

**Lane verdict: arm (a) does NOT deliver cleanly.**
- No Lagrangian coupling delivers supply, edge and temperature together.
- The only delivery is the rule-level gate (C3). It delivers either as the edge definition written into a coupling (C3a), or
  as a sign gate on a gauged charge too weak for any local mechanism to read (C3b).

## The numbers

### DELIVERS gates

Edges are log₁₀(E/5.8498 r_M), with E the 99.9% radius of the settled cold mass. Supply is the settled mass inside E over
S × the galaxy's baryons. T is CFG461's R0 amplitude. The lines are 0.05 / 0.05 / 0.1 dex and 5% for the law.

| coupling, host | edge | supply | T | law | gates |
|---|---|---|---|---|---|
| C2 at α_N = 0 (= the uncoupled F-H fill, CAT 23.63 M_b) | +0.615 / +0.620 | +0.644 | +0.018 / +0.007 | 1e-8 | edge, supply FAIL |
| C2, α_N = 0.01 (law within 5%) | +0.616 / +0.621 | +0.644 | +0.015 / +0.004 | 0.008 / 0.004 | edge, supply FAIL |
| C2, α_N = 100 (supply capped) | +0.87 / +1.20 | +0.02 | −1.6 / −2.3 | 18 / 8 | edge, T, law FAIL |
| C3, point mass | −0.0004 | −0.0004 | +0.073 | 0 | ALL PASS |
| C3, Hernquist a = 0.3 r_M (scored) | −0.023 | **−0.046** | +0.028 | 0 | ALL PASS (supply margin 0.004 dex) |
| C3, Hernquist a = 1 r_M (reported) | −0.082 | −0.163 | −0.090 | 0 | edge, supply FAIL |
| C1 best case (12 combinations) | −0.33 … +0.32 | −0.67 … +0.67 | −0.58 … +0.74 | 0.65–2.8 | all FAIL |
| C4, static equilibrium | +0.615 | +0.644 | +0.018 | 0 | edge, supply FAIL |

All six cells (10⁹, 10^10.5, 10^11.5 M☉ × 2 footings) give the same C2, C3 and C4 numbers to the digits shown, because the
problems are self-similar in r_M. Only the catchment's edge in r_M units (x_ta = 74–213) and C1 differ by cell.

Physical scale (point host): r_edge = 7.1 / 40.1 / 126.9 kpc canonical (6.5 / 36.5 / 115.5 kpc alt). σ_t = 42.0 / 99.5 /
177.0 km/s canonical (44.0 / 104.4 / 185.6 km/s alt).

### SURVIVES: the U(1)'s α_N limit from each bound, against the strengths it needs

| bound | α_N limit | C2 needs 280 (the cap) | C3b scored at 5.5e-13 |
|---|---|---|---|
| B1 Eöt-Wash (Be–Ti, Earth) | 1.6e-10 | FAIL, −12.2 dex | PASS |
| B2 MICROSCOPE (Ti–Pt; record 1e-15) | 1.1e-12 | FAIL, −14.4 dex | PASS |
| B3 Cassini (a vector does not couple to light) + ephemerides (composition anomaly ≤ 1.27e-5 a₀) + bound orbits | 2.8e-9 | FAIL, −11.0 dex | PASS |
| B4 binary pulsars (vector dipole; J0737 binds) | 9.1e-5 | FAIL, −6.5 dex | PASS |
| B5 Bullet (extra pull ≤ 25% of the offset in 0.2 Gyr) | 18.8 | FAIL, −1.2 dex | PASS (inherited settling rate: CONDITIONAL) |
| B6 CMB/BAO (relative-mode coupling ≤ 1%; declared estimate) | 0.29 | FAIL, −3.0 dex | PASS (inherited: CONDITIONAL) |
| B7 DR3 / no-EFE (material phantom kept; bound pairs need α_N < 1) | 1 | FAIL, −2.4 dex | PASS |

The pulsar dipole/GR ratio is 892 α_N (J1738+0333), 688 α_N (J0348+0432) and 1.43 α_N (J0737-3039A/B). These use NS binding
from a recalled formula with R = 12 km; R = 11–13 km moves the limits by ±20%.

**C2 fails even at the largest strength its own law tolerates** (α_N = 0.34): B1, B2, B3, B4 and B6 fail there. At strengths
the bounds allow (≤ 1e-12), C2 is the uncoupled F-H fill: edge +0.615 dex.

**C1 BK** (Reading B = BK as written; CFG122 showed environmental screening is impossible):
- Eöt-Wash η = 7.5e-9 (1.9e4 × the bound);
- MICROSCOPE 3.1e-9 (3.1e6 ×);
- Cassini |γ − 1| = 2.5e-4 (10.9 ×);
- the MOND force is the phonon force on baryons, so it is caught in the EFE triangle (CFG447 / PAPER44): B7 FAIL.
- Pulsars and the Bullet were not computed (N-C); CMB is CFG122 G2's UNDECIDED.

**C4 drag:**
- To lock each cold parcel to its partner baryons within one dynamical time at the edge needs κ_d ≥ 2.8e3 cm²/g (canonical) /
  2.3e3 (alt), independent of mass.
- CMB allows ≤ 5e-3 (recalled, unverified): FAIL by 5.8 dex. The Bullet plasma column (0.044 g/cm²) allows ≤ 6.8: FAIL by
  2.6 dex.
- The static fifth-force tests (B1–B4) do not apply to a contact drag (N-C).

## What was found

1. **The edge is the neutral point of a composition charge, for any coupling strength (K1c).**
   - Give baryons charge +1 and the cold fluid −1/S per unit mass. The enclosed charge vanishes exactly at 5.8498 r_M for a
     point host: |m* − S| ≤ 2e-8 for α_N from 1e-6 to 1e6.
   - So a gauged composition charge "knows" where the edge is. That is the constructive piece of this lane.
2. **A conservative (Lagrangian) coupling cannot make that point a sharp edge without destroying the law (C2).**
   - Inside the edge the charge is positive and pulls the cold fluid toward the baryons. Outside it repels the excess.
   - Gravity-normalised, the law needs α_N ≤ 0.34 (point) / 0.44 (a = 0.3), and the cap needs α_N ≥ 280. The window is
     closed by 2.9 / 2.8 dex. The F-H-normalised scan agrees (3.0 / 2.6 dex), and that ratio does not depend on the settling
     functional's weight.
   - At large α_N the cold fluid collapses onto the baryons (point host: 4.165 M_b within 1e-3 r_M at α_N = 100). It neutralises
     locally instead of following the law.
   - **Coincidence caught:** the point-mass E sweeps through 5.85 r_M at α_N = 5.0e3–6.3e3, passing from +0.39 to −0.17 dex as
     the fluid collapses. The law deviation there is 22.9 (the settled mass is ~24 × the law's). This is not an edge.
3. **The seesaw (K1a) makes this general for analytic exchange couplings.** For any number of same-spin mediators,
   α_bc² ≤ α_bb α_cc.
   - The supply rule needs the cold fluid to respond to baryons at O(1).
   - The EP tests force α_bb ≤ 1e-12, so the cold fluid's self-force must be ≥ 1e12 × gravity, which no clustering cold fluid
     survives.
   - A scalar + vector pair can cancel the baryon–baryon force (the K1a loophole), but only between equal charges. A scalar
     couples to mass and a vector to baryon number, so the residual is α × Δ(B m_u/M): the MICROSCOPE signal again.
4. **The only delivery is a gate, and it is not a coupling in the field-theory sense (C3).**
   - J = Γ ρ_u Θ(−E·ĝ) lets cold fluid settle only where the enclosed composition is baryon-rich. With the law as the target
     this gives:
     - point host: edge −0.0004 dex, supply −0.0004, T +0.073;
     - a = 0.3: edge −0.023, supply −0.046 (inside the line by 0.004), T +0.028.
   - Its supply is S × the baryons **inside** the edge, not S × M_b. The reported a = 1 r_M host fails (supply −0.163,
     edge −0.082). Galaxies with extended gas discs sit near or past that line.
   - **C3a:** the gate's threshold s must be set equal to Ω_c/Ω_b by hand. That is CFG488's finding 5 again: the edge
     definition written as a law. No listed bound can see it (there is no force), so it survives vacuously.
   - **C3b:** reading the sign of C2's gauged field derives s (FRW neutrality), and the delivery does not depend on α_N. But
     a thermally activated gate's open/closed contrast is 4.4e-4 α_N.
     - At the strongest α_N the bounds allow (5.5e-13) the contrast is 2.4e-16.
     - A gate that can actually be read needs α_N ≥ 2.3e3. That fails every bound (B1–B7), as C2 does.
5. **Drag cannot hold a static cap (C4).** A drag vanishes when nothing moves. The static equilibrium is therefore the
   uncoupled catchment fill (+0.615 dex). The "locked" transient makes the cold fluid trace the baryons (law off by 23× /
   10×), and the locking strength fails the CMB and the Bullet.
6. **BK (C1) does not enforce the supply at all.**
   - Its condensate mass at fixed x = r/r_M scales as (M_b/a₀)^{1/2} (K1d, sympy). Over the cells that is a 1.33 dex supply
     spread, so the best single constant misses by ±0.6 dex.
   - The best case lands at m = 1.0 eV for α = 1, in BK's own fiducial range.
7. **The temperature does not discriminate once the law is the target** (stated in the criteria before the run). The uncoupled
   catchment fill already gives T = +0.018 dex with its edge at 24 r_M. Under the F-H drive the settled region carries the
   law, so σ follows the law wherever the edge is. The discriminating results are the supply and the edge.

## What a G9 violation would mean for the framework (plainly)

- **What is given up.** G9 is the framework's statement that the cold fluid and the baryons interact only through gravity (the
  Bianchi identity with matter coupled to the metric). Giving it up makes the cold fluid a dark sector with its own
  non-gravitational interaction with ordinary matter.
- **What that needs.** On every Lagrangian route tested here, it needs a field quantum (a dark-matter particle) and, for C2/C3b,
  a new long-range force on baryon number. That moves the framework toward superfluid- or dark-force dark-matter models, and
  away from "the law is gravity's".
- **What it would buy:** nothing on the record.
  - The supply and the edge follow only from a rule whose one number is the edge definition (C3a), or from a gate no local
    physics can read (C3b).
  - Every coupling with real dynamics fails both the frozen gates and the bounds.
- **Where the fork stands.** Both arms now fail to derive the 5.85 r_M supply edge: the G9 arm (CFG461/462/488) and the
  coupled arm (CFG490). On the record the cosmic share inside the edge is an input, a boundary condition, not a result.
- **Unchanged:**
  - the law's target is still carried by the lapse with zero constants (CFG373);
  - the energy sink still needs CFG381's coupling;
  - the cold fluid's mass is still required.

## Reported rows (not verdict inputs)

- **Clusters (CFG488).**
  - Free placement leaves u = 0 inside R500, against [0.433, 0.628] canonical and [0.368, 0.584] alt.
  - In-place placement gives 0.452 / 0.389.
  - C3's gate decides neither, because it depends on the sign of the outskirts' composition: UNDECIDED.
- **C3b has its own external-field effect.**
  - In a 6e10 M☉ host (edge 55 kpc), the host's composition field at a satellite is 2.4 × the satellite's own at 20 kpc, and
    0.06 × at 50 kpc. This holds for any satellite mass.
  - So inner satellites would have their supply set by the host.
- **C3b counts all baryons, hot CGM included.** Extra counted baryons of 5% / 20% / 50% of M_b inside the edge move it by
  +0.020 / +0.073 / +0.164 dex.
- **Gauging B − L instead of B** (the anomaly-free choice) makes hydrogen neutral. The gate would then count neutrons, not M_b.
- **The energy sink:** NOT SUPPLIED in every coupling (CFG462, inherited).

## Controls

- **K1 PASS (sympy):**
  - (a) the Lagrange identity behind the seesaw, plus the mixed-spin loophole;
  - (b) FRW neutrality and the C2 force law;
  - (c) the neutral point, numerically;
  - (d) BK's exponent of ½;
  - (e) R0 = 1.18354;
  - (f) the dipole ratio 5/48.
- **K2 PASS.** C2 at α_N = 0 reproduces CFG462's committed F-H catchment edge: 23.38017 against 23.38018 r_M (−4.5e-7).
- **K3 PASS.** The C3 point edge is 5.8497613 r_M; the ν_mono inverse round trip is accurate to 2e-15.
- **K4 PASS.** Every C2 root is nondecreasing in r (161 α_N × 3 hosts); the root residual is ≤ 7.6e-10.
- **K5 PASS.** These reproduce CFG122's Δ(B/μ)_Ti,Pt = 9.0516e-4 and its Reading-B η = 3.106e-9, and CFG291's J1738 GR
  Ṗ_b = −2.7461e-14.

## MUTATE (`CFG490_MUTATE=1`, exit 1 = teeth detected)

- **(M-a)** Every coupling set to zero loses the edge. C2, C3 and C4 return to the uncoupled fill, +0.615 dex. C1 at α → 0
  (fixed m, Λ) loses its baryon-sourced condensate.
- **(M-b)** Every coupling with a strength violates a bound at 100 × its scored value:
  - C3b at 5.5e-11 fails MICROSCOPE;
  - C2 at 2.8e4 fails all seven;
  - C4 at 2.8e5 cm²/g fails the CMB and the Bullet;
  - C1 already fails, and its force is α-free under the a₀ tie.
- **C3a has no strength to scale:** VACUOUS, as frozen.

## Disclosures (after the first output; none moves a verdict)

- The (M-a) text for C1 was reworded after the first run to say α → 0 is taken at fixed m and Λ. Under the a₀ tie, α → 0 is
  singular. Text only.
- The C2 edge-sweep coincidence (item 2) was noticed in the output. It is reported here and as a labelled POST-RUN line in
  the .out, which was added together with the point-host collapse line (4.165 M_b inside 1e-3 r_M at α_N = 100). Both are
  print-only; the results JSON is unchanged byte for byte.

## Caveats

- Everything is spherical and static, and the F-H drive is the record's declared flow. Its weight cancels from C2's window but
  sets C2's absolute α_N on the scan, which is why SURVIVES uses the gravity-normalised cap.
- The U(1) is taken as unscreened in the Solar System. For α_cc ~ 1 the cold fluid's Debye length is ~kpc, far above an AU.
- **Inputs recalled from the literature (UNVERIFIED):**
  - Eöt-Wash 3.9e-13;
  - MICROSCOPE's final result (the record's 1e-15 is the one scored);
  - ⁹Be's mass, and the Sun, Saturn and Earth compositions;
  - the NS binding formula;
  - the Bullet's time since pericentre (0.1–0.2 Gyr);
  - the CMB drag bound 5e-3 cm²/g.
- B6's 1% relative-mode tolerance is a declared estimate, not a published bound.
- No verdict sits near any of these numbers except C3's a = 0.3 supply (margin 0.004 dex) and C2's Bullet row (1.2 dex).
- G-REAL is a declared construct. Any gate whose decision energy is ~1e-16 of the fluid's thermal energy is unreadable by a
  local mechanism, whatever the exact criterion.

## Run

```
python3 campaign_fresh_gravity/CFG490_direct_coupling_arm/cfg490_direct_coupling.py                 # exit 0
CFG490_MUTATE=1 python3 campaign_fresh_gravity/CFG490_direct_coupling_arm/cfg490_direct_coupling.py  # exit 1 = teeth detected
```

Inputs, all read-only:
- `CFG4_common` (ν_mono, constants)
- `CFG462_lapse_settling_edge/cfg462_results.json`
- `CFG488_cosettling_supply/cfg488_results.json`
- `CFG291_khronon_binary_pulsar/cfg291_khronon_binary_pulsar_results.json`
- the Bullet Table 2 values used by `CFG4_clusters.py` (Clowe 2006)
