# CFG112 — with published GC slopes, does one debris fraction fit all ten populations at 2σ? FROZEN CRITERIA

Written 2026-09-29, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

The adopted STANDING page says: "The derived rule has no clean support left. One debris fraction fits all populations only at 2σ (0.52–0.71), and not with dynamical SLUGGS masses (CFG59, CFG62, CFG75)."

- **CFG75:** with CFG71's dynamical SLUGGS masses, the 2σ intersection of the ten populations is empty only because of SLUGGS, which sits at 2.6σ at φ = 1. Without SLUGGS the intersection is [0.23, 0.71] (canonical) and [0.21, 0.66] (alt).
- **CFG71's SLUGGS row uses γ = 3** for every galaxy.
- **CFG111** (6e1b04092): with each galaxy's published GC density slope (Alabi+2017), the rule's JAM-calibrated SLUGGS offset at φ = 1 falls to 1.55σ.

The question: with the published slopes, is the ten-population 2σ intersection still empty?

## Machinery (declared)

- **CFG71's harness,** exec'd read-only up to its scan (`GRID = np.round(...)`), with MUTATE forced to 0 for that exec. From it:
  - `calib_mass_phi` (the φ-scaled JAM calibration);
  - `debris_phi`;
  - CFG55's Jeans functions (`sigma_r2`, `sigma_los`).
- **One change:** U5d's prediction uses γ_i per galaxy in `sigma_r2` and `sigma_los`, where γ_i is CFG111's `gamma_rel` = clip(−0.63 log M*_SLUGGS + 9.81, 2, 4). The calibration does not depend on γ. Nothing else changes.
- **The other nine populations** (U1–U4, U6–U10): their o(φ) and e(φ) are read from CFG71's committed results JSON (`scan`), on CFG71's 101-point grid on [0, 1].
- **The intersection at k σ** follows CFG75's definition: the grid points where |o| ≤ k e for every population. Its reported edges are the first and last such points.

## Checks

- **C1 CONTROL:** with γ_i = 3 for every galaxy, the patched U5d reproduces CFG71's committed U5d scan, o and e at all 101 grid points on both footings, to 1e-9.
- **C2 CONTROL:** with the published γ_i, U5d at φ = 0 and φ = 1 reproduces CFG111's committed law and rule means and errors (canonical and alt) to 1e-6.
- **C3 CONTROL:** CFG75's committed 2σ intersection without SLUGGS is reproduced from CFG71's JSON: [0.23, 0.71] canonical, [0.21, 0.66] alt, to the printed precision.
- **H1 [HEADLINE; MUTATE must fail]:** with the published slopes, the ten-population 2σ intersection is non-empty on both footings.

## Reported rows

- **R1:** U5d's 1σ and 2σ intervals with the published slopes, both footings.
- **R2:** the ten-population intersections at 1σ and 3σ with the published slopes.
- **R3:** the same 2σ question with SLUGGS's own population masses for the 16 (CFG71's reference U5s, debris φ-scaled in the prediction only), with the published slopes.
- **R4:** the 2σ intersection with every γ_i shifted by ±0.2. These are CFG111's R2 brackets.

## MUTATE

MUTATE=1 sets γ_i = 3 for every galaxy, which undoes the lane's one change. The 2σ intersection must then be empty, reproducing CFG75. So H1 must fail and the script must exit 1.

If the main run's H1 also fails, both runs fail the same check. The control is then uninformative, and the README will say so.

## Readings (declared)

- **H1 PASS** (non-empty on both footings): with realistic GC slopes, one debris fraction fits all ten populations at 2σ. The STANDING clause "and not with dynamical SLUGGS masses" is superseded. The 1σ NO stands, since CFG75 has the 1σ intersection empty even without SLUGGS.
- **H1 FAIL:** the 2σ intersection stays empty with the published slopes, and the clause stands. The binding population will be reported.
- **One footing only:** reported as mixed.
- **Caveat:** orbits are still assumed isotropic. Anisotropy is CFG113.

κ = ½ and Ω_c h² stay fitted. A common φ at 2σ is a statement about the acceptance level, not a derived fraction. Nothing here says the data favour either model, or that the theory is closed.
