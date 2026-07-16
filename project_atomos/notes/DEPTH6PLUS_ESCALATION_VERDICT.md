# DEPTH 6+ ESCALATION VERDICT — constructive forced-interlock sweep past the depth-5 null

**Status: ESCALATION COMPLETE. Depths 6 and 7 = CLEAN NULLS (gates fire, 0 certified). Depth 8 = the FEASIBILITY WALL (memory).**
Continuation of the committed depth-3/4/5 clean nulls (commit `9230fbd`). Machine used: `exhaust_depthN_forced.py`.
No git commit. RULE 3 held (zero diff on `gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py exhaust_depth5_forced.py`, start/mid/end).

---

## Per-depth table

| Depth | Scale-skeleton (splits b_s,g_s) | Constructive raw | Distinct dim. values | Completeness | Gates fired | In-window hits (21 tgts) | Certified | Re-labeled | Peak RSS | Wall-clock | Verdict |
|------:|---------------------------------|-----------------:|---------------------:|:------------:|:-----------:|-------------------------:|:---------:|:----------:|---------:|-----------:|---------|
| 6 | 2-scale: (1,4)(2,3) | 236,624 | 107,719 | OK (0/0) | YES | 259 | 0 | 0 | 347 MB | 13.2 s | **CLEAN NULL** |
| 7 | 3-scale: (1,5)(2,4)(3,3) | 1,566,116 | 498,848 | OK (0/0) | YES | 1,248 | 0 | 0 | 1,378 MB | 95.3 s | **CLEAN NULL** (last runnable) |
| 8 | 4-scale: (1,6)(2,5)(3,4)(4,3) | 8,123,807 | 2,207,173 | OK (0/0)\* | YES\* | 0 (single-tgt probe) | 0 | 0 | 5,910 MB | 515 s/tgt | **WALL (memory)** |

\* Depth-8 completeness (`b_s=4` split 1147==1147, 0 missed/0 extra) and a0 heads verified in isolation; the full 21-target
12-worker sweep is un-runnable within the 6 GB cap (see wall).

### Tightest hit at every depth (identical, an honest degenerate re-label of 2/3)
`((((( c/c )/3)*sqrt(8pi/3))/sqrt(8pi/3))*2)` = 0.66666667, target `koide_Q_lep` rel_err = 9.23e-06, n_sigma 0.91.
- Gate B kernel **PASS** (B=True): 2 forced germs present (`3`, `sqrt(8pi/3)`), 1 free O(1).
- Gate C interlock **FAIL** (C=False): single target, no cross-sector partner.
- Gate A **FDR-DEAD**: E_chance = 8.242e-02 (< 1, sparse), surplus = **-0.0 bits** (< 10-bit PASS threshold), mult=21 look-elsewhere.
- This is `sqrt(8pi/3)/sqrt(8pi/3)` × `2` on `c/c=1` — i.e. **2/3 re-labeled**, the germs cancel; correctly killed. Not new physics.

**ZERO CERTIFIED, ZERO RE-LABELED survivors at every depth.** Hits grow with depth (259 → 1248) but the growth is FDR-dense
noise, not signal — every hit dies at Gate A. Neither a win nor a manufactured dismissal.

---

## FEASIBILITY WALL — wall_depth = 8, binding resource = MEMORY (6 GB hard cap)

- A **single** depth-8 target build (`r_mu_e`) peaks at **5.77 GB** (96% of the 6 GB watchdog cap, zero headroom) at **515 s/target**.
- The mandated sweep needs **12 parallel workers**, each an independent ~5.77 GB build. Launched, combined RSS hit **11.5 GB after
  only 90 s** (~15% into builds), macOS compressor active (444,562 pages) — projecting to **~69 GB**, the exact swap-thrash the
  memory brief forbids (a prior depth-5 run was KILLED at 35 GB swap). Killed before damage.
- **Depth 7 is the last cleanly runnable depth.** Depth 9+ is hopeless on memory, time, AND validation (single build already 515 s).

### HONEST CAVEAT on the wall (reconciled from the fidelity adversary — CONFIRMED correct)
The 5.77 GB peak is driven by **materializing the `reach` list of `Reachable` objects** (each holds a full `ExprNode` + formula
string, kept for reporting the winning formulae), **NOT** by the deduped distinct-VALUE set the memory brief says to keep — a
value-only probe stays ~0.15 GB through 600k+ distinct values. So **wall_depth=8 is the memory-footprint ceiling of THIS
reporting implementation, not an intrinsic value-set explosion**; a build that streamed Reachables to disk or kept only value-keys
could push past depth 8. This does NOT change any verdict: depths 6/7 are genuine clean nulls, and the depth-8 per-worker watchdog
would abort the required 12-worker sweep regardless. It reframes "8 is the ceiling" honestly as an engineering ceiling of the
reporting build, reachable-further only at the cost of dropping formula reporting.

---

## Completeness proof (per completed depth) — RECONCILED and HARDENED

**The shape argument.** A Gate-B-passable dimensionless depth-D tree factors as
{ dimensionless scale skeleton, budget b_s } × { germ recipe over {3, sqrt(8pi/3)} + 1 free, budget g_s }, b_s+g_s = D-1, g_s ≥ 3.
Germ factors commute → the germ layer is enumerated canonically by NET EXPONENT per germ (half-exponents {1, ½} so POW/sqrt
distributes), one canonical decorate sequence per net — order-free, so associativity/interleaving of the POW-wrapped product is
irrelevant after value-dedup.

**In-script checks (reproduced):** per-split skeleton value-set == independent brute (depth-6: 13==13, 73==73, 0 missed/0 extra),
and the committed brute depth-4 anchor reproduced (11,209 == 11,209 all-Gate-B distinct; dimensionless≤4 empty both sides).

**Gap the completeness adversary raised (VALID) + closure (RECONCILED — I ran the checks myself):** the in-script self-check
brutes the SKELETON sub-layer, but not explicitly the germ sub-layer as a standalone brute. I closed both sub-layers and the
product independently:

1. **GERM sub-layer — independent EXACT brute (precision-proof).** Enumerated every full order×op×exp germ sequence of length g_s
   over the 3 Gate-B germ keys (forced `3`, `sqrt(8pi/3)`, + one free, each present ≥1) and deduped by the EXACT net signed-exponent
   signature (`Fraction`, not float — germs are algebraically independent so equal signature ⇔ equal value). Compared to the scheme's
   canonical `_germ_recipes`: **brute == scheme, 0 MISSED / 0 EXTRA at g_s = 3, 4, 5** (1472/1472, 6992/6992, 18308/18308 — all
   germ budgets appearing at completed depths 6 and 7). *(A first pass showed "MISSED=1" at g_s=3; I traced it to a
   float multiplication-ORDER ULP split in my own check — the scheme provably reaches that exact value {3^−½, sqrt(8pi/3)^+1,
   free^+1} = 0.626657 — a check-side rounding artifact, NOT a scheme hole. The exact-Fraction signature removes it: 0/0.)*

2. **FULL PRODUCT at the anchor depth — whole-tree brute.** The in-script anchor is a genuine WHOLE-TREE brute
   (`enumerate_depth4_filtered`, real tree enumerator, not skeleton-only): reproduced **11,209** all-Gate-B distinct values and **0**
   dimensionless (the depth-4 theorem) — so the two-layer product IS brute-closed at depth 4, where the germ layer is fully exercised.

3. **Product order-freedom.** Germ factors commute → the two-layer product's value is layout-independent after value-dedup; the
   interleaving worry (a POW wrapping the germ-decorated product, e.g. `sqrt((Lam_QCD/v_EW)*3*sqrt(8pi/3)*pi)`) is REACHED via
   half-exponents {1, ½}. Combined with the skeleton brute (0/0) and germ brute (0/0), **no missed tree at depths 6/7.**

The full-engine `enumerate_trees` whole-tree brute at depth 5 (the adversary's 192==192) is also consistent but was too slow to
re-run to completion here at 40-dps (10.5M trees > timeout); the three checks above establish the same closure by sub-layer
brutes + the depth-4 whole-tree anchor. Optional hardening (not required): fold the germ-layer exact brute into the in-script
per-depth self-check.

---

## a0 validity (RULE 2 — targeted construction, not brute) — reproduced

At every completed depth, a0 = (c/Z)·H_Λ is re-found by **direct construction**, never by bruting the dimensionful depth-D space.
- LEG 1 (committed depth-4 dimensional re-derivation, verbatim): `((c/Z)*H_L)` = 9.36018e-11 m/s², rel_err 1.97e-05. PASS.
- LEG 2 (explicit depth-D a0 × cancelling identity through the real pipeline): e.g. depth-6 `(((((c*H_L)/Z)*3)/3))^1`
  = 9.36018e-11 m/s², dims L/T² ✓, value==a0 (<1%) ✓; gate verdict **FDR-DEAD** (one forced provenance → not overdetermined →
  correctly NOT certified). Reproduced at depths 6, 7, 8.

a0 is the EXPECTED FDR-DEAD: it carries a single forced provenance chain, so it can never be Gate-B-overdetermined. Working as designed.

---

## FDR honesty (RULE 3 non-smuggle) — reproduced and CONFIRMED not smuggled

- The Gate-A density is over the **REALISTIC FULL 25-germ library**, not a sparsified pool. Independently reconstructed:
  `_germ_pool_from_alpha` → **25 germs** (asserted), `build_value_set` → **64,881 values** (exact match to the adversary's number).
- E_chance(koide_Q_lep) reconstructs to **8.2417e-02** vs the run's 8.242e-02 — exact. mult = n_targets = 21 applied.
- The **-0.0 surplus bits** is honest arithmetic: min(1, E_chance)·21 = 1.73 > 1 → capped to chance=1.0 → -log2(1) = 0.
- **Robustness (not a defect):** the FDR-DEAD verdict does NOT hinge on the ×21 look-elsewhere — even at mult=1 the surplus is only
  ~3.60 bits, still far below the 10-bit PASS threshold. Full-library density alone kills it.
- **Cosmetic caveat (confirmed):** the Gate-A tell prints the TIGHT-window hit count ("190 hits") while E_chance is (correctly)
  derived from the ±10% WIDE band. E_chance, surplus, mult, and the FDR-DEAD verdict are all correct and reproduce exactly; only
  the human-readable count label is the narrower quantity. No number the verdict rests on is wrong.

---

## Both-ways standing / HONEST CEILING

**What the escalating null proves.** Over the forced-germ vocabulary {3 (N_gen), sqrt(8pi/3) (a0 kernel)} + exactly 1 free O(1),
enumerated CONSTRUCTIVELY and value-completely up to the feasibility wall (depth 7 fully, depth 8's completeness/a0 heads verified),
the SM parameter sector stays **KERNEL-FREE**: no over-determined multi-sector forced interlock survives all three gates + cross-sector.
The single recurring tightest hit is a degenerate re-label of Koide 2/3, correctly FDR-killed. This is the honest, expected outcome —
it CERTIFIES the null, it does not manufacture a deficit.

**What it does NOT prove.** It does NOT rule out (a) a NEW forced germ beyond {3, sqrt(8pi/3)}, (b) a new forced mechanism/kernel
(a genuine Yukawa/gauge kernel that the current germ library cannot express), or (c) a survivor at depth ≥ 8 that the reporting-memory
wall prevents this implementation from reaching (the wall is engineering, not a value-set explosion). The null is scoped to the
committed forced vocabulary and to depth ≤ 7 (fully) / depth 8 (heads only).

**Standing: UNCHANGED. Do NOT re-open the SM sector** absent a NEW forced gauge/Yukawa kernel. Consistent with the standing prior
(SM mass sector walled+closed; number-field obstruction; E8/J3(O) HOSTS-not-FORCES). No survivor appeared; nothing to escalate to
candidate-needing-scrutiny.

---

## Reproduction commands (from `/Users/carlzimmerman/new_physics/project_atomos`)

```
# Depth-6 completeness + a0:
python3 exhaust_depthN_forced.py --depth 6 --self-check --a0-check
# Depth-6 soundness (real gate.forced_kernel on 300 sampled candidates):
python3 exhaust_depthN_forced.py --depth 6 --target koide_Q_lep --soundness
# Depth-6 full gate on the tightest target (shows FDR-DEAD):
python3 exhaust_depthN_forced.py --depth 6 --target koide_Q_lep
# Full escalating sweep (D=6,7,8...) to the wall (12-worker parallel):
python3 exhaust_depthN_forced.py --escalate --workers 12
# RULE 3 clean check:
git diff --stat gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py exhaust_depth5_forced.py
```

Reconciliation checks I ran (scratchpad, not committed): germ-layer EXACT-signature brute vs scheme
(0/0 at g_s=3,4,5); depth-4 whole-tree anchor `enumerate_depth4_filtered` → 11,209 / 0-dimensionless;
`build_value_set` over `_germ_pool_from_alpha` → 25 germs / 64,881 values (FDR non-smuggle); depth-6
`--soundness` → 300/300 real `gate.forced_kernel`; depth-6 `--target koide_Q_lep` → FDR-DEAD reproduced.

Peak RSS per depth printed by the watchdog (`_mem_watchdog`, SELF+CHILDREN, 6 GB hard cap). HEAD `9230fbd`, no commit.
