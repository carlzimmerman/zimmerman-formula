# CFG112 — with published GC slopes, does one debris fraction fit all ten populations at 2σ?

- **Criteria:** frozen in `CFG112_FROZEN_CRITERIA.md` (663f73877), before any number.
- **Script:** `CFG112_universal_fraction_published_slopes.py`. It took about 8 minutes on a heavily loaded machine.
- **Runs:**
  - The main run passes 7 of 8 and exits 1. The one failure is the headline H1, and that failure is the answer: NO.
  - The MUTATE run (γ = 3 for every galaxy) fails H1 and exits 1, reproducing CFG75's empty 2σ intersection.
  - Both runs fail H1, so, as the frozen file said in advance, the control is uninformative for H1.

## Bottom line

**No. With the published slopes, the ten-population 2σ intersection stays empty, but only narrowly.** So the STANDING clause "and not with dynamical SLUGGS masses" stands.

- **SLUGGS (dynamical masses, published slopes) fits at 2σ only for φ in [0.77, 1]** on both footings.
- **The other nine populations share [0.23, 0.71]** (alt [0.21, 0.66]).
- The gap is 0.06 in φ (alt 0.11). The population that binds against SLUGGS is the M31 LVD, on both footings.

| φ | 0 (the law) | 0.25 | 0.5 | 0.71 | 0.75 | 1 (the rule) |
|---|---|---|---|---|---|---|
| SLUGGS offset, canonical | +0.082 (3.60σ) | 3.13σ | 2.56σ | 2.11σ | 2.03σ | +0.028 (1.55σ) |
| alt | 3.22σ | 2.85σ | 2.43σ | 2.09σ | 2.03σ | 1.64σ |

**How fragile the NO is:**
- **With every γ_i lowered by 0.2,** the intersection opens: [0.37, 0.71] (alt [0.28, 0.66]). Raised by 0.2, it stays empty.
- **With SLUGGS's own population masses,** SLUGGS no longer binds and the ten share [0.23, 0.71] (alt [0.21, 0.66]).
- **At 3σ,** all ten share [0.31, 1] (alt [0.16, 1]).
- **At 1σ,** the intersection is empty with or without SLUGGS (CFG75), and SLUGGS's own 1σ set is empty.

## Controls

- **C1:** with γ = 3 for every galaxy, the patched SLUGGS row reproduces CFG71's committed scan exactly: 101 points, both footings.
- **C2:** with the published slopes, the SLUGGS row at φ = 0 and φ = 1 reproduces CFG111's committed law and rule exactly: means and errors, both footings.
- **C3:** CFG75's committed 2σ intersection without SLUGGS is reproduced from CFG71's scan: [0.23, 0.71] canonical, [0.21, 0.66] alt.
- **MUTATE** (γ = 3): the 2σ intersection is empty, as in CFG75. SLUGGS then has no 2σ window in [0, 1] (2.58σ at φ = 1), and its 3σ intersection reproduces CFG75's: [0.77, 1], alt [0.71, 1].

## Caveats

- **The intersection uses CFG75's grid-point definition** on CFG71's 101-point grid. The edges quoted are grid points, 0.01 apart.
- **Orbits are isotropic here.** CFG113 finds that radial GC orbits (β = +0.5) lower the rule's SLUGGS offset at φ = 1 from 1.55σ to 0.56σ. That could open this narrow gap, but it is not computed here.
- **Only SLUGGS changes.** The other nine populations are CFG71's committed rows, unchanged.

## Reading

- **The STANDING line stands as written:** "One debris fraction fits all populations only at 2σ (0.52–0.71), and not with dynamical SLUGGS masses".
- **Add CFG111 and CFG112 as qualifiers:**
  - with published GC slopes, the rule fits SLUGGS on its own (1.55σ);
  - but its 2σ window, [0.77, 1], misses the other nine's [0.23, 0.71] by 0.06 in φ;
  - the verdict turns on the GC slopes to within 0.2.
- **The 1σ NO and the satellite failures** do not depend on SLUGGS.

κ = ½ and Ω_c h² stay fitted. A common φ at 2σ would be a statement about the acceptance level, not a derived fraction. Nothing here says the data favour either model, or that the theory is closed.

## Addendum after the independent re-derivations CFG104–CFG106 (appended 2026-09-29; the text above is unchanged)

- **CFG104** (independent re-derivation of CFG112) reproduces it exactly. Its reading: the NO is a boundary, not a conflict. All ten populations share a φ at 2.07σ (alt 2.09σ) against the 2σ line, and at 2.62σ with γ = 3. Only SLUGGS and the M31 LVD are in tension. The result is a knife edge: every γ_i shifted by −0.1 opens the ten-set, and +0.1 empties SLUGGS's window. The other nine populations are CFG71's committed rows. Read 'not with dynamical SLUGGS masses' as 'only at 2.07σ with dynamical masses and the published slopes'. **The slopes are 3-D.** Alabi+2017 define γ as the slope of the de-projected GC number-density profile, as checked in the paper's arXiv HTML on 2026-09-29. So the Jeans solution's ρ ∝ r^−γ uses it as intended; the case of projected slopes, which would put SLUGGS at +5.6σ at φ = 1, does not arise. The 'published slopes' are one mass relation, γ = clip(−0.63 log M* + 9.81, 2, 4) (2.49–3.43), not per-galaxy measurements.
