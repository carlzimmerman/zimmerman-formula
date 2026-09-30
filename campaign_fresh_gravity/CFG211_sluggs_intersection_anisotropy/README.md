# CFG211 — does CFG112's ten-population 2σ intersection open under GC orbital anisotropy?

- **Criteria:** `FROZEN_CRITERIA.md` (0f0fdcea8), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Run:** `python3 campaign_fresh_gravity/CFG211_sluggs_intersection_anisotropy/cfg211_intersection_anisotropy.py`, about 8 minutes.
- **Machinery:** CFG112's script is exec'd read-only up to its controls. The one change is a constant GC anisotropy β in CFG55/h50's σ_r² and σ_los, as CFG113 used them.
- **Runs:**
  - The main run passes 4 of 5 checks and exits 1. The one failure is the headline H1, and that failure is the answer: NO at the measured anisotropies.
  - The MUTATE run (β = 0 for all) also fails H1, reproducing CFG112. As the frozen file said in advance, it is therefore uninformative for H1. K_open and K_close carry the machinery check.

## Bottom line

**At the measured anisotropies the intersection stays empty, so the clause "and not with dynamical SLUGGS masses" stands. A uniform radial anisotropy of β = +0.25 in every galaxy is enough to open it.**

| β configuration | SLUGGS (U5d) 2σ set | ten-population 2σ intersection, canonical / alt |
|---|---|---|
| PRIMARY, measured-anchored (NGC 5846 +0.275, the rest 0) | [0.75, 1.0] / [0.75, 1.0] | **empty / empty**: the other nine end at 0.71 / 0.66; U4 is disjoint from SLUGGS |
| variant: primary with M87 at −0.25 (illustrative) | [0.76, 1.0] | empty / empty |
| S1: β = +0.25 for all 16 | [0.60, 1.0] / [0.57, 1.0] | **[0.60, 0.71] (12 pts) / [0.57, 0.66] (10 pts)** |
| S2: β = +0.5 for all 16 | [0.41, 1.0] / [0.36, 1.0] | **[0.41, 0.71] (31 pts) / [0.36, 0.66] (31 pts)** |

- **H1 (primary):** empty on both footings, so "the clause stands under measured-anchored anisotropy". The gap is narrow: SLUGGS's 2σ set starts at φ = 0.75, and the other nine populations end at 0.71.
- **S1:** the intersection opens. The frozen label is "conditional on uniform radial anisotropy β = +0.25 in every galaxy (measured only for the red GCs of one galaxy outside ~3 R_e)".
- **S2:** it opens wider. The frozen label is "conditional on radial anisotropy at or beyond the edge of the measured range".
- **Where the sources point.**
  - Orbits more tangential than the measured anchor push the gap wider: the variant puts M87's red-GC tangential bias in, and the gap grows from φ = 0.75 to 0.76.
  - The measured systems in CFG113's sources are mixed. NGC 5846's red GCs are radial outside 3 R_e and isotropic near 1 R_e. NGC 1407 has radial metal-rich GCs and tangential metal-poor ones. M87's red GCs are tangential.
  - A uniform β = +0.25 in all 16 galaxies is therefore an assumption, not a measurement.

## Controls (all pass)

- **C1.** β = 0 for all reproduces CFG112's committed U5d scan exactly: maximum difference 0.0, 101 points, both footings.
- **C2.** β = +0.5 for all reproduces CFG113's committed law and rule at β = +0.5 exactly (maximum difference 0.0):
  - canonical: law +0.0738 ± 0.0218, rule +0.0110 ± 0.0196;
  - alt: law +0.0636, rule +0.0131.
- **C3.** CFG75's intersection without SLUGGS is reproduced: [0.23, 0.71] canonical and [0.21, 0.66] alt.
- **K_open / K_close.** With U5d's o = 0 the intersection equals C3's set; with o = 5e it is empty.

## What this does and does not change

- **STANDING is unchanged.** Under measured-anchored anisotropy, one debris fraction does not fit all ten populations at 2σ with dynamical SLUGGS masses.
- **The gap is closed only by isotropic or measured-anchored orbits.** Any qualifier the orchestrator appends should say that the empty intersection is conditional on near-isotropic GC orbits. A uniform β = +0.25, which is not measured for whole GC systems, opens it at φ ≈ 0.6–0.7.
- **Scope.** Constant β only, as in CFG113; radial profiles β(r) are not tested. The slopes are the published ones, unshifted (CFG114 varied them).
