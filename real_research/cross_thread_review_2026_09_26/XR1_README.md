# XR1: cross-lane consistency registry for the dark-sector and vacuum-gate lanes

This review asks one question of each headline verdict: were all of its stages run at the same settings? The settings checked are the switch cell (p, x_c0), the a0 footing, the kernel, the phantom operator, the switch-variable convention, the carrier trigger and the epoch.

It extends `real_research/peer_review_2026_09_26/dark_sector/REPORT.md` and does not redo it. Nothing outside this prefix was edited, and no simulation was run.

| file | what it is |
|---|---|
| `XR1_registry.json` | 54 stages and 36 headline verdicts. Each stage carries its attributes, derivation specs, evidence (`file` + `pattern` + line at inspection), its imports (with epochs) and a status taken from commits and READMEs. It also records the sha256 and git state of 49 cited files. Snapshot: 2026-09-26 15:49, HEAD 738216fbd. |
| `XR1_consistency_check.py` | Static only: ast and regex on the source, plus results JSON read via `git show HEAD:`. Runs in about 7 s, single-threaded. |
| `XR1_consistency_check.out` | The main run: rc = 0. |
| `XR1_consistency_check_MUTATE.out` | `MUTATE=1` corrupts L381's registered Harvey cell to p2_x2.0. Check D catches the drift, so rc = 1. Trusting the registry alone would have hidden the mismatch. |

Run it from the repository root with `python3 real_research/cross_thread_review_2026_09_26/XR1_consistency_check.py`.

The script re-derives every cell from the code, following each chain back to its source:
- L381 `harvey()` → L371 → L370 `SW_DEF`;
- L388's module-level override on L377's constants;
- L373's `G["SW_DEF"] = SWK`;
- AT3's `HNS["SW_DEF"]`, checked to come after the exec of L372's slice.

The CONTROL asserts that the L381 conflict {p1_x1.5, p2_x2.0} is found from source alone. A negative control asserts that the L388 chain and L373 are not flagged.

## What is consistent (the cell is the same in every switch-dependent stage, derived from the code)
- **The L388 chain is at p1_x2.5 throughout.**
  - L388: `L388.py:42`. The override is at module level, so the spawn-started Pool workers inherit it.
  - Shear: the DE3 JSON cell, asserted at `L388.py:77`.
  - L389: `L389.py:50` and `:82`.
  - L390: `L390.py:41`. L390 was committed as b3ba1f6fa during the review: KiDS passes, −13.1/−7.1.
- **L373 is at p2_x2.0 in the PM, Harvey and shear stages.**
  - PM: `L377.py:94`, with no override.
  - Harvey: `L373.py:228-230`.
  - Shear: `L373.py:380`.
  - The running process (started 15:24:42) postdates the fix (15:24:14).
- **AT3's current source is at p1_x2.5** for Harvey (`AT3.py:358`, after the exec at `:340`) and for shear (`:424`).
- **L377–L380 are at p2_x2.0 throughout.**
- **The per-cell scans carry their own cell per row:** L359, L363, L364, L367, L370 El Gordo, DE1 and DE2.
- **GP1–GP5 have no switch at all.**
- **No cell override sits in a `__main__` guard of a spawn-Pool script** (check C3).

## What is mixed (ranked by consequence)
1. **L381: CELL-CONFLICT (withdrawn, 3151d88f2).**
   - The PM stage is at p2_x2.0 (`L377.py:94`).
   - The Harvey stage is at p1_x1.5 (`L370.py:160` → `L371.py:79-80` → `L381.py:64-68`, which never replaces it).
   - No live verdict has a cell conflict.
2. **The p2_x2.0 verdicts sit on a cell DE1 excludes.** At canonical footing, M_b = 1e11, the shift is −1.134 dex (edge 36.8 < 38.6 kpc), and it fails for all three kernels at HEAD.
   - This covers L380 (scoped), L375, L377, and **L373, which is pending**.
   - Whatever L373 finds is a p2_x2.0 result. It cannot be pooled with the p1_x2.5 chain.
3. **AT3's outputs on disk predate its fix.**
   - The `.out` (15:29:57) was printed by the pre-fix docstring: `HEADER-MISMATCH`. That source's Harvey inherited p1_x1.5 through `L372.py:252`.
   - `AT3_…_results.json` (14:54) is a **FAST-grid run** (y_v0 ∈ {0.01, 0.1}). It carries the main name because `AT3.py:84` has no `_FAST` suffix.
4. **The KiDS stage is switch-free while the Harvey stage is switched** (CELL-OMITTED).
   - This affects L372 (committed, relayed at `PAPER34…tex:163` without its cell) and AT3.
   - The KiDS scoring path is `L357.py:328` (web-blind kernel) → `L355.py:22` ("No switch").
5. **The L388 chain is same-cell but not the same model.** It mixes four phantom operators:
   - PM: `L377.py:123,125`, all baryons, masked;
   - Harvey: `L370.py:291,296`, per-region FFT;
   - shear: `L363.py:125,154`, Dirichlet;
   - KiDS: L352, spherical compensated.

   It mixes four switch-variable conventions:
   - `L377.py:120`: background-subtracted, matter only;
   - `L370.py:290`: absolute density;
   - `L363.py:138`: phantom-inclusive, seeded;
   - L352 and DE1: on-branch.

   It also mixes:
   - epochs: retention at z = 0 (`L388.py:116`) is used at Harvey's z = 0.4 (`L371.py:85`);
   - footings: the PM and Harvey stages run canonical only;
   - kernels: RAR and RC100 come from L376's `nu_RAR` (`L376.py:52`);
   - triggers: L390 uses the matter-only trigger, L388 the phantom-inclusive one.
6. **L370's docstring does not match its code.** Line 19 describes a background-subtracted gate; the code at `:224` and `:290` uses the absolute density. Every consumer inherits the code, not the docstring.
7. **Smaller items:**
   - L373 has no halo ≥ 3e14 at z = 0.4 (n = 0), so the 1e15 main cluster takes the 3e14 bin's retention (`L373.py:409`).
   - L375 and L390 fit the baryonic masses once, on the canonical footing, and score both footings with them (`L375.py:180`, `L390.py:72`).
   - DE2's linear-gate interval uses L367's Newtonian single-box transfer (`DE2.py:120`, as its SCOPE says).

## What each thread should change
- **dark_sector (L388/L389):**
  - Save the z = 0.4 fields in L388, as L373 does, so that L389 scores Harvey on retention measured at its own epoch.
  - Run the alt footing in at least one box.
  - State that RAR and RC100 are L376's `nu_RAR` numbers, or re-run them with `nu_mono`.
  - Before any claim of one theory, do the operator bridge the peer review asked for. It applies to shear (PM transfer + region-Dirichlet phantom) as well as to Harvey.
- **merger_infall:**
  - Fix `L370.py:19`, or change the code to the background-subtracted gate that L377, L352 and DE1 use.
  - Make the cell a required argument of `solve_real`/`phantom_felt` callers, with no module default to inherit.
  - Label L373 "p2_x2.0 only (DE1-excluded at canonical)", or re-run it at p1_x2.5, and record the n = 0 fallback.
  - L372 (and PAPER34:163): state Harvey at p1_x1.5 and KiDS switch-free. Re-score at p1_x2.5 with the switched KiDS machinery (L360/L390) before it joins the chain.
- **acceleration_trigger:**
  - Re-run AT3 from the current source.
  - Add `_FAST` to its SLUG.
  - Do not commit the 14:54 JSON or the 15:29 `.out`.
  - Score KiDS with L390's switched fit at p1_x2.5, or declare it switch-free. Note that retention is switch-independent in code, but Harvey and shear are not.
- **dark_energy:**
  - The per-kernel edges are now committed (0b4e319b7).
  - DE2's membership of p1_x2.5 is conditional on L367's switch-free transfer. L388's own pooled transfer against DE3's T_max is what confirms it.
- **g03_audit, generated_phantom:** nothing to change for cell consistency.

## What is live (from commits and READMEs; the registry has the full list)
- **Stands:**
  - L357 (with its flagship price), L367, L369 (as gated), L375, L376, L377, L379;
  - L370 (El Gordo at every cell; Harvey at p1_x1.5), L371 (as a failure), L372 (alt set);
  - L359, L360, L363, L364;
  - GP1–GP3, GP5;
  - DE1, DE2 (scoped), DE3 and L390, both committed during this review.
- **Scoped:**
  - L380: the p2_x2.0 cell only.
  - GP4: its window is closed at high z by GP5. KiDS against the realisable floor is +19.1..+21.5, not +8.
- **Withdrawn or superseded:** L381 (3151d88f2), L368 (by L369), L365 and L366 (by L369), and L378's clearing reading (by L379 → L380).
- **Stopped:** L386 and L387 (absent on disk).
- **Pending:** L388 (running), L389 (waits for L388), L373 (running), AT1, AT2 and AT3 (all uncommitted).

The registry is a snapshot, so re-run the checker after any lane edit. Check D fails when the code no longer says what the registry says. File-hash changes alone are only reported.
