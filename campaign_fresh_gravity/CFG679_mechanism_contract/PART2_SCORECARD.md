# CFG679 Part 2 scorecard: controls and the record's catalogue against the mechanism contract

Criteria: `FROZEN_CRITERIA.md` (8b77a75fc) and `PART2_FROZEN_CRITERIA.md` (41ad7a730). Reading lane, no new runs; every cell
cites a committed lane or document. κ = ½ fitted; both footings, never pooled; the cold energy's mass is required; no particle
species; not theory closed.

## Controls (each must FAIL its named gate)

| control | gate | result | source | tooth |
|---|---|---|---|---|
| K1 class-A settling | R0 | **FAIL**: the drift is v_s = −α τ∇ψ with ∇²ψ = 4πG(ρ_ph − ρ_c); ρ_ph is the law's phantom density | CFG638 system table | bites |
| K2 GR + Λ, no sector | M1a | **FAIL**: Newton rms 0.27548 dex on both footings > 0.110 | `CFG4_galaxy_law_results.json` | bites |
| K3 non-lensing response (conformal stiff sector) | M3a | **FAIL**: CFG663 class H-NL EXCLUDED, Δ = +0.155 / +0.158 dex, 2000/2000 draws ≥ 0.03 | CFG663 | bites |
| K4 CFG660 stress, independent density | M1c | **FAIL**: Im ω = 2.5 / 21 / 214 per τ_ff at k = 10 / 10³ / 10⁵ (∝ √k) | CFG660 S5 | bites |

All four controls fail as required. The contract has teeth on R0, M1a, M1c and M3a. M2a, M2b, C3 and D2 have no dedicated
control in the contract. They borrow their source lanes' own teeth: CFG48 Noether identity, CFG541–544, CFG529 T1/T2, CFG596
NZ1.

## Catalogue (MECHANISM_JOINT §7 + astra's stable φ + P sector)

| candidate | R0 | M1a | M1c | M2b | M3a | first S fail (§7) | verdict, first failing gate |
|---|---|---|---|---|---|---|---|
| BE reading of ν_mono + dS bath | **FAIL**: a rewriting of ν_mono | – | – | – | – | S1 | FAIL, R0 |
| Superfluid phonons (Berezhiani–Khoury) | **R0-SHAPED**: P(X) ∝ X^{3/2} chosen to give deep MOND | UNTESTED | – | – | – | S2; particle species | FAIL, S2 + framework rule |
| Dipolar medium (Blanchet) | **R0-SHAPED**: potential coefficients phenomenological (astra POLARIZATION_REPAIR_GATE) | – | **FAIL**: growing mode; no finite friction makes an attractor | – | – | S2 | FAIL, M1c |
| astra stable φ + P stiff sector | **R0-SHAPED**: "choosing the critical square and cubic norm is a phenomenological assumption" | **UNTESTED**: conservative minimum; "attraction requires a derived energy-loss mechanism" | CONDITIONAL: δ²H ≥ 0 for fixed baryons only | **FAIL**: no reservoir field | **FAIL**: CFG663 (conformal, does not lens) | S4 | FAIL, M2b + M3a |
| Emergent gravity (Verlinde) | UNTESTED | UNTESTED (static) | – | – | – | S5 (CFG117) | FAIL, S5 |
| AeST / single-metric relativistic MOND | **R0-SHAPED**: free function chosen for the MOND limit | – (no cold mass to move) | – | – | – | S2 (DC-013, DC-019, PAPER44) | FAIL, S2 |
| Modified inertia | **FAIL**: μ inserted | – | – | – | – | S4 / S2 per horn | FAIL, R0 |
| Nonlocal kernels (Mashhoon) | **R0-SHAPED**: kernel fitted to flat curves | – | – | – | – | S5 (CFG120) | FAIL, S5 |
| Local stress, any EoS | **FAIL**: built from F (dP∥/dg = (g/4πG)(1/F′ − 1)) | – | **FAIL** (CFG660, CFG661) | – | – | S3 | FAIL, R0 |
| Thermal equilibrium + universal edge | UNTESTED | **FAIL**: no regular solution (CFG665) | – | – | – | S6 | FAIL, M1a |
| Baryon heating Q = C a₀ v ρ_b | PASS (letter; no law input) | – (scored against CFG541's target) | – | **FAIL**: wrong sign; 8–56 × the baryons' kinetic energy needed (CFG643) | – | S9 | FAIL, M2b |
| Energy-bounded settling | **FAIL**: caps the settled phantom; knob η (CFG645) | – | – | – | – | – | FAIL, R0 + R1 |
| Fixed-flux four-form portal | PASS (letter) | UNTESTED: "does not derive a halo selector" | – | – | – | S2 / S3 | FAIL, S2/S3 |
| Feedback-driven gravitational work | **PASS**: "no radial target was inserted" | **FAIL**: rapid profiles differ by 38% of supplied mass; neither evolves to the target | – | – | – | S5 / S6 | FAIL, M1a |
| Unruh / dS temperature for σ | PASS (letter) | **FAIL**: one σ for all galaxies, not σ⁴ ∝ M_b (CFG461 C3a) | – | – | – | S1 | FAIL, M1a |

Sources not named in a cell are those given for the row in MECHANISM_JOINT §7.

## Result

- **No candidate passes the mechanism contract. None reaches M3 without a FAIL.**
- **R0 splits the catalogue in two.**
  - Every candidate that gets the law's shape either inserts the law (FAIL: BE reading, modified inertia, local stress,
    energy-bounded settling, class-A settling) or picks a form to match it (R0-SHAPED: phonons, dipolar, astra's sector, AeST,
    nonlocal kernels).
  - Every candidate that passes R0 outright fails to produce the profile or the energy: heating (M2b), feedback (M1a), Unruh σ
    (M1a), four-form (S2/S3).
  - **Not one entry on record both passes R0 and produces the law's profile.** That is the missing mechanism, stated as a
    gate.
- **The closest structure** is astra's stable sector. It is the only entry with a non-trivial M1c pass (conditional, fixed
  baryons). Three further things would be needed:
  1. a form for its cubic term fixed by something other than the law (R0);
  2. a dissipation channel into a named reservoir field that makes the minimum an attractor (M1a, M2b);
  3. a coupling that lenses, for example disformal, or a gravitating stiff sector (M3a, CFG663 reading 2).

  This is a specification, not a construction. The field theory is astra's side and is not edited here.
- Lane counts: R0 outright PASS 4 of 15 (heating, four-form, feedback, Unruh σ). Reaching M3 without a FAIL: 0 of 15.
