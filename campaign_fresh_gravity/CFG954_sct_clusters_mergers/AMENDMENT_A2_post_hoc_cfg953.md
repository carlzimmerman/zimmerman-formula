# CFG954 AMENDMENT A2: POST HOC (2026-10-21, after all four full-data stages). CFG953's SCT specification read against this lane

**When.** CFG953 (the SCT construction) froze its criteria (049a0f867; A1 611bb324a) while this lane was running. Its directory did
not exist when `FROZEN_CRITERIA.md` (68a43b4ff) was written. This file was written after this lane's COMPUTE, K, MUTATE and MAIN
results, so it is POST HOC. As §0 of the criteria requires, it states where CFG953 differs on a point used here and which result
changes. Nothing frozen is edited, no class of R1–R3 changes, and CFG953's files were read only.

## Where CFG953 differs from this lane's working statement
1. **Dust placement.** CFG953 converts a domain's cold dust into a phantom body at collapse. Labelled dust is gravitationally inert
   (R2 there), so the body is the only thing that gravitates.
   - This lane's P-S accounting (active cold-sector mass = the phantom) matches it.
   - This lane's P-I bracket ("dust-held halos survive absorption as Newtonian dust") has no counterpart in CFG953, so the R1 [P-I]
     and R3 [P-I] rows do not describe CFG953's theory.
2. **Satellites and members keep their whole body** until CFG953's merge rule R7 fires (bound fraction < ½, or centroid
   coalescence). There is no tidal truncation of the body and no absorption.
   - None of this lane's R1–R3 is that rule: R1 absorbs at r_J < r_e; R2 and R3 truncate at the King r_J.
   - It is this lane's MUTATE arm MU-NA (ii), "never absorb": whole own-baryon bodies, the host's body the law of the host's own
     baryons, and conserved supply. Under the harness's supply convention (CFG652 P2 branch, Σ_i S_i = S_tot in 652/652
     cluster-footings, K-S), the host body has zero mass.
   - CFG951 found the R7-type trigger fires for about 2e-8 of cluster members at pericentre, so in clusters members persist whole.
3. **Momentum.** CFG953 gives each body its own centroid momentum (R4), with conversion and merge events absorbed inelastically. This
   lane's S3 (carried weights) and its (f) test of an absorption recompute do not apply to CFG953's events. CFG953 tests momentum
   itself (S-P, S-TM).
4. **Unchanged:** the kernel (CFG953's S2 simple kernel is this lane's ν_s), the edge at the kernel's own supply root, own-baryon
   sourcing and the absence of cross-sourcing.

## The result that changes: CFG953's clusters are this lane's MU-NA (ii) row
From `cfg954_results_MUTATE.json` (computed before this file; same harness, ν_s, both footings):

| | eRASS1 A_MID (Z) | eRASS1 A_OUTER (Z) | s (vs 0.896 ± 0.209) | ACCEPT A_OUTER (Z) |
|---|---|---|---|---|
| CFG953 spec ≡ MU-NA (ii), canonical | 1.559 ± 0.098 (+5.68) | 0.771 ± 0.066 (−3.48) | 0.809 | 0.447 ± 0.113 (−4.88) |
| CFG953 spec ≡ MU-NA (ii), alt | 1.470 ± 0.093 (+5.06) | 0.762 ± 0.065 (−3.68) | 0.816 | 0.428 ± 0.109 (−5.26) |
| CFG726 H-MM (K2, for reference) | 1.536 / 1.440 | 0.765 (−3.63) / 0.744 (−4.05) | 0.718 / 0.678 | 0.449 / 0.430 |

**Grade, reported** (by this lane's frozen (a1)/(a2)/(c) rules; it does not enter this lane's overall, which is defined on R1–R3):
- (a1) merger memory INCONSISTENT on both footings;
- (a2) core INCONSISTENT;
- (c) slope CONSISTENT.

CFG953's frozen first-order statement placed its clusters "between CFG951's plain law row and its X-OD row", from the record and
not computed. The computed arm lies outside that bracket on the canonical footing: 0.771 against X-OD's 0.814. Whole bodies are not
truncated, so they hold more memory than L2-truncated media. On the alt footing it lies just inside (0.762 against 0.746). Either
way it sits at the H-MM level of merger memory: own-baryon sourcing removes CFG951's amplification but not the memory itself.

**Other items under CFG953's rule** (reported, from this lane's computed rows; no new computation):
- **Coma UDGs:** whole bodies keep the own law at r½ (r_J/r12 ≥ 4.45 even under truncation), so this lane's "keep" row applies:
  z +1.61 / +1.42, NOT DIAGNOSTIC.
- **Not computed here:**
  - the Bullet under R7: whether the stripped gas (87% of the sub's baryons) makes the sub's bound fraction < ½, which would fire
    R7;
  - the merger toy with R7's blend over τ_m.

κ = ½ FITTED; footings never pooled; not theory closed.
