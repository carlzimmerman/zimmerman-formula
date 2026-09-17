# SW00_INDEX — glm_moe_push (the nonlocal-door lane, 2026-09-17)

Swing per the 2026-09-17 swarm brief: find a nonlocal construction with an internal/external
asymmetry ≥ 6.4× at x = 2.5. Committed and pushed at the owner's request on 2026-09-17, overriding
brief stop rule (iii) ("no commits; leave files for review") — the lane script and outputs are
versioned as-is; SW01-B remains OPEN, not accepted. Lane script mirrors the
kappa_slot_2026 SW convention (check() with computed booleans only, both a₀ footings, sympy
identities, MUTATE=1 switch, FAILs recorded as findings).

## Candidates

**SW01 — the environmental-scalar response** (`PROPOSER_SW01_envscalar.md`, `SW01_envscalar_response.py`)
Replace μ(|g|/a₀) with a response to two nonlocal functionals of the Newtonian field on the Gauss
sphere: Γ (angular variance — the field's own structure) and η (the sphere's l=1 component — the
environment); g_obs = g_N + S(η)(ν_RAR(Γ/a₀)−1)g_N,enc, S(η) = 1/(1+(η/η_c)²). A uniform external
field is pure l=1 — it enters η, never Γ — so it cannot trigger the response by itself: the system
is defined by the flux structure, no hand-drawn boundary.

- **First gate (fixed computation): PASS both variants.** (a) isolated point mass at x = 2.5:
  departure 0.2590; (b) same mass in a 2.5a₀ uniform field: 0.0357 (SW01-A) / 0.0020 (SW01-B).
  Ratios 7.25 and 128.0 vs the 6.4 gate. [MUTATE=1 verified: break S → ratio = 1.00, gate FAILs.]
- **Quadrupole gate: PASS** — scalar capping has no l=2 moment at leading order; the residual from
  the η-gradient across r_M is ≤ 6.0e-5 ceilings (both footings), vs L243's 6.44 for vector capping.
- **BTFR slope: PASS** — v = (GMa₀)^¼ exact (sympy), slope 4.0 vs measured 3.98 ± 0.06.
- **KILL — SW01-A (η_c = 1, the no-free-number stress-balance variant):** KILLED by the Oort
  budget: ρ_dark = 1.92·S(2.5) = 0.265 M☉/pc³ = 17.7× the 0.015 budget (L263 C1). One-line kill:
  *stress balance caps the stellar phantom ~20× too weakly for the solar-neighbourhood budget; the
  environmental stress needed is η_c ≈ 0.22, and no force balance supplies it.*
- **SW01-B (η_c = 0.222, Oort-calibrated): OPEN**, with declared calibration (G2 FAIL is the
  finding: no second independent derivation — the 08-09 near-miss rule) and three pre-registered
  falsifiers: (1) γ_v(DR4) = 1.0010 vs the registered 1.16–1.23 band, 2026-12-02; (2) any
  AQUAL-level EFE quadrupole detection kills the whole class; (3) satellites at η ≳ 1 showing
  deep-MOND dispersions (per-object Jeans per L263 E decides).

## Audit finding incidental to this lane

The record's alt-footing a₀ = 1.1279e-10 does not reproduce from its stated recipe
(a₀ = ½c√(Gρ_crit) at H₀ = 67.4): the recipe gives 1.1312e-10 (+0.27%), implying H₀ ≈ 67.2 —
a README-rule-5 convention audit item (check A2, FAIL is the finding). The canonical footing
rebuilds to 4.4e-5 and all gate ratios are footing-independent.

## Status

One candidate killed (SW01-A), one standing (SW01-B). Stop rule (ii) (three kills → synthesis) not
triggered. Deferred, stated openly: R3 ghost theorem and the action formulation (G03-class);
R6 cluster residual; the dSph/η ≳ 1 tension. The words "derived", "closed", "breakthrough" appear
nowhere above because nothing here has earned them yet.
