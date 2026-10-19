# CFG823 — can the dSphs' total cold-energy supply pay for their inner mass at all?

Criteria: `FROZEN_CRITERIA.md` (37fab0eee, before the script). Run: `python3 cfg823.py` (MUTATE: `CFG823_MUTATE=1`). Seconds, 1 core.

## Result — CLASS (Υ = 2, primary): **BUDGET TIGHT** (median q = 0.303, at the 0.30 boundary)
q = cold mass needed inside r_1/2 ÷ the catchment's TOTAL cold supply (5.364 M_b / f_ret = 53.6 M_b at the census floor).

| Υ | median q | max q | q > 1 at > 2σ | class |
|---|---|---|---|---|
| 1 | 0.62 | 2.20 | Antlia II, Ursa Minor | BUDGET FAILS |
| **2** | **0.30** | **1.10** | none | **BUDGET TIGHT** |
| 4 | 0.15 | 0.54 | none | BUDGET OK |

- At Υ = 2 the faint dSphs need about half to all of their whole catchment's cold energy inside r_1/2, which is ~1% of r_ta
  (median r_1/2 / r_ta = 0.011): Antlia II 1.10, Sextans 0.99, CVn I 0.62, Ursa Minor 0.56, Draco 0.50.
- Fornax, Leo I, Sculptor and Leo II need ≤ 13%; the bright dSphs are not the problem.
- **Reading:** the census supply is not excluded outright at Υ = 2, but it survives only if nearly all of a faint dSph's
  cold energy is packed inside its stellar half-light radius, which no settled or infall profile the framework has produced
  does. At Υ = 1 it fails outright. Together with CFG821/822 this pins the dwarf problem: the framework needs a mechanism that
  binds cold energy to dwarfs' stellar cores far more tightly than the galaxy law, or a larger supply than the baryon census.
- For scale, the uncapped settled law alone gives q_settled > 1 for Antlia II and Crater II (their law-settled mass exceeds
  the whole supply), and 0.04–0.42 for the rest.

## Controls
- K1 PASS: Draco M_req reproduces the G = 4.3009e-6 kpc (km/s)² / M_⊙ form to 2.5e-4 (constant convention; the criteria said
  1e-6, which the two G conventions cannot meet; disclosed).
- MUTATE bites: f_ret = 1 (no expelled gas) → every q rises ×10 (median 3.03), BUDGET FAILS at every Υ. Without the expelled
  gas's cold energy, the dSphs are excluded outright.

κ = ½ fitted; cold energy mass required; not theory closed.
