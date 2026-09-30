# CFG211 — does CFG112's ten-population 2σ intersection open under GC orbital anisotropy? FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's go, before any CFG211 number. **κ = ½ FITTED, NOT DERIVED.**

## The question, and how it differs from CFG114

- **This lane.** CFG112 (published GC slopes, isotropic orbits) found that the ten-population 2σ intersection for one debris fraction φ ∈ [0, 1] stays empty, "but only narrowly", through SLUGGS (U5d). STANDING keeps the clause "and not with dynamical SLUGGS masses". CFG211 asks whether that INTERSECTION opens when U5d's predictions use a constant GC anisotropy β in the Jeans solution and projection (CFG113's machinery). The slopes stay published and unshifted, and nothing else changes.
- **CFG114** varied (slope shift × β) for the SLUGGS deficit alone, the law at φ = 0 and the rule at φ = 1. It found the law's deficit below 2σ only at the corner "every γ_i − 0.4, β = +0.5". It did not compute the ten-population intersection over φ.
- **CFG104 and CFG105** are the independent re-derivations of CFG112 and CFG113. They are read as context and not imported.

## Machinery, read-only

- CFG112's script is exec'd up to its controls: CFG71's harness, `cal` (the φ-scaled JAM calibration, which is independent of the GC β), `inter`, `inside`, GRID, the other nine populations from CFG71's JSON, and the published γ_i.
- **The one change:** U5d's prediction uses `sigma_r2(gf, γ_i, β_i)` and `sigma_los(R, ·, γ_i, β_i)`. These are CFG55/h50's functions, which already take a constant β, as CFG113 used them.

## β assignments (declared now)

**PRIMARY: measured-anchored, per galaxy, from the measurements CFG113 cites (CFG113_FROZEN_CRITERIA.md lines 22–24).**
- **NGC 5846:** β = **+0.275**, the mean of the cited red (≈ 0.4) and blue (≈ 0.15) values outside about 3 R_e. It is applied at all radii, which is an upper value, since the system is isotropic near 1 R_e.
- **NGC 1407 and NGC 4486 (M87):** β = **0**. CFG113 cites only directions, with opposite signs in the two subpopulations: NGC 1407's metal-rich GCs are radial and its metal-poor ones tangential; M87's red GCs are tangential and its blue ones near-isotropic. No single number is cited.
- **The other 13 galaxies:** β = 0 (no measurement cited).

**SENSITIVITY (reported): β = +0.25 and β = +0.5 for all 16 galaxies.**

**Reported variant:** the primary with M87 at β = −0.25. This is the tangential direction its red GCs show, at the bracket's step size. It is illustrative, not a measured value.

## Decision rows

- **H1 [HEADLINE].** With the PRIMARY β, is the ten-population 2σ intersection non-empty on both footings?
  - Yes: "the intersection opens with measured-anchored anisotropy". Any STANDING qualifier is appended by the orchestrator, not here.
  - No: "the clause stands under measured-anchored anisotropy".
  - One footing only: "mixed".
- **S1 (reported).** At β = +0.25 for all:
  - If the intersection opens, the label is "conditional on uniform radial anisotropy β = +0.25 in every galaxy (measured only for the red GCs of one galaxy outside ~3 R_e)".
- **S2 (reported).** At β = +0.5 for all:
  - If the intersection opens only here, the label is "conditional on radial anisotropy at or beyond the edge of the measured range".
- **Also reported, for each configuration:**
  - U5d's 2σ set;
  - the intersection's edges and number of grid points;
  - the populations disjoint from SLUGGS.

## Controls

- **C1.** β = 0 for all reproduces CFG112's committed U5d scan to 1e-9: o and e at 101 points, both footings.
- **C2.** β = +0.5 for all: U5d at φ = 0 and φ = 1 reproduces CFG113's committed law and rule SLUGGS means and errors at β = +0.5, both footings, to 1e-6.
- **C3.** CFG75's intersection without SLUGGS is reproduced: [0.23, 0.71] canonical, [0.21, 0.66] alt.
- **K_open / K_close** (the intersection machinery):
  - With U5d's o(φ) set to 0, the intersection must equal C3's set.
  - With o(φ) set to 5 e(φ), it must be empty.
- **MUTATE=1.** β = 0 for all: the lane's one change is undone. The run must reproduce CFG112's committed empty intersection, so H1 must FAIL and the run exit 1.
  - If the primary also fails H1, this control is uninformative for H1. That is declared now, as in CFG112. K_open and K_close carry the machinery check.

## Hand expectation, disclosed

- CFG113 has the rule's SLUGGS offset at φ = 1 falling from 1.55σ (isotropic) to 0.56σ at β = +0.5. CFG112's gap is narrow.
- So I expect S2 to open. S1 may or may not.
- The primary, where only NGC 5846 moves, probably stays empty.
