# CFG795 FROZEN CRITERIA: the converter design space (committed before any script)

HYPOTHETICAL. The owner asks how a device could turn ambient cold energy into light for a photon ramjet (CFG791/792).
This lane maps the allowed design space against existing data and names the least-constrained window, if any.

Inputs (as CFG792): ρ_c = 0.01 M☉ pc⁻³, ρc² = 6.1e-5 J/m³, cold energy at rest in the Galaxy, v₀ = 230 km/s, flux
F₀ = ρc²v₀ ≈ 14 W/m². Ramjet efficiency η = light power out / cold-energy power intercepted. Reference intake: a 1 mg/m²
sheet (graphene, CFG791 D1); e-fold time τ₀ = Σ/(ηρc). Target: η ≥ 0.01 (CFG791: α Cen in ~95 yr). All external bounds
are quoted from memory or a web summary and are PROVISIONAL.

## Portal classes and the bound each must face
- **P1 per-mass (nucleons / bound electrons), linear in column.** Rate per unit areal mass k (m²/kg); η = 1 − exp(−kΣ).
  Natural-matter bounds: (a) whole-atmosphere column 1.03e4 kg/m² must give ≤ 1e-3 lux of night glow; (b) the whole
  Earth (mean chord column) must give ≤ 47 TW; (c) Moon heat flow ≈ 20 mW/m² vs F₀/4. Strongest one sets k_max.
- **P2 free (conduction) electrons.** Rate per free electron. Natural bound: Earth's metallic core (column ~1e36 e/m²)
  heat ≤ 47 TW; ionosphere (TEC ~1e17 e/m²) night glow. Device: 1 mg/m² Al foil (3 free e per atom).
- **P3 photon / B-field (axion-like).** Dish formula η = G·(gB/m)²·(c/v₀). g ≤ 6.6e-11 GeV⁻¹ (CAST/HB, most permissive
  for both masses), B ≤ 1e3 T (destructive pulsed), engineered gain G ≤ 1e6 (resonant stack/cavity). Masses: 2.4 eV
  (CFG790 line) and 2.24 meV (ARGON03 native).
- **P4 kinetic mixing (dark-photon-like).** η = G·ε²·(c/v₀). ε ≤ 1e-14 at 2–3 eV (stellar, Caputo et al. band edge);
  ε ≤ 6.25e-9 at 2.24 meV (solar relation, ARGON03 G5; the weakest bound on record, used deliberately).
- **P5 superconductor / condensate-gated.** Natural analogues: neutron-star cores (geometric + focused flux; report T).
  Lab bound: an SNSPD film (A = 1e-8 m², dark counts ≤ 1e-5 Hz, ≥ 10% of products absorbed, ≥ 1 eV each).
- **P6 laser stimulation (Bose enhancement).** Detailed balance: net transfer cold→mode ∝ (N_cold − N_mode). A laser
  mode with N_mode > N_cold reverses the flow. Phase-locked coherent extraction needs the cold field's phase, measurable
  only if ε√N_cold ≥ 1 per coherence cell. Report N_cold per cell (both masses) and the ε this needs.
- **P7 material resonance at 2–3 eV.** Natural matter has electronic bands across 2–3 eV (widths ≫ the cold line width
  (v/c)² ≈ 6e-7). A resonance is therefore present in nature: P1 bounds apply.
- **P8 gravity-only (moving / oscillating mass).** With no non-gravitational portal (the record's cold energy couples only
  gravitationally), a device can extract at most the kinetic energy: η ≤ (v₀/c)²/2.
- **P9 framework screening (reading R1: cold energy = bound charge of the stiff P field).** Response of P on device
  scale d is suppressed by (d/L*)² (the record's own scaling, CFG770 T2 / CFG772 L2), L* ≥ 5.75 pc. Report η ≤ (d/L*)²
  for d = 1 m, 10 km, and the d needed for η = 0.01. Under reading R2 (independent collisionless medium) P9 does not apply.

## Outputs and classes
For each class: η_max (1 mg/m² sheet or stated device), τ₀ at η_max, natural-matter "off" factor needed, device "on"
factor needed for η = 0.01. Verdict: **WINDOW OPEN** if any class allows η ≥ 0.01; **CLOSED** otherwise. Name the
least-constrained window (largest η_max) and the decisive obstruction.

## Controls
- **K1:** reproduce CFG792's ground light ≈ 160 lux (within 5%) for full conversion in the upper air.
- **K2:** reproduce CFG792's Earth interception ≈ 38× the 47 TW heat flow (within 5%).
- **MUTATE** (`CFG795_MUTATE=1`, separate outputs `*_MUTATE.*`): ρ_c → 0. Must zero the natural-matter excesses
  (K1/K2 → 0) and leave the P9 screening factor unchanged (two-sided tooth). Exit 1 by design.

κ = ½ fitted; not theory closed. No dark matter particle species is introduced: portals are hypothetical couplings.
