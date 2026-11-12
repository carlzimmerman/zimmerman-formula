# FINAL-13 — LEAN-AUDIT

Lean certification bookkeeping for the `fable_independent_2026/lean_2026/` tree.
No new physics. This lane adopts nothing.

κ = ½ is FITTED; not theory closed.

**Audit snapshot** (sha256 of the exact bytes audited — re-verified identical after compiling):

| audited file | sha256 |
|---|---|
| `FINAL9to12/FINAL9_StaticHalo.lean` | `afaf2dc44c4e3a0b1a1caef5bcb798dfa5e517c1af09dcd7e51dd89a654b0875` |
| `FINAL9to12/Final10Stress.lean` | `ac79188955aef00b97fd820ed3e563dc1c9ef5f55661f764ecf89a0850e6bc9c` |
| `FINAL9to12/Final11Budget.lean` | `88241b19ff8427b0ef555e4bafe6f681835c947dd71a2b9ad9e440a119ab2375` |
| `FINAL9to12/FINAL12_background_conservation.lean` | `670524a19b3a8a619d29aeb19587c722f3de26a94918eba46993f3ba5b911da9` |

---

## 1. Baseline manifest — 354 pre-existing `.lean` sources hashed

`manifest_baseline.sha256` holds `sha256 ./<name>` for **every** pre-existing `.lean` file under
`fable_independent_2026/lean_2026/`, excluding the `.lake` build/package tree
(9947 `.lean` files live under `.lake/packages`; those are vendored mathlib, not this project's sources).

```
354 files hashed, sha256 (shasum -a 256)
```

Coverage: 331 root modules + `A83/` (4) + `ChainCert/` (20).
All 354 are git-tracked at `HEAD`; at T0 the only dirty file in the tree was `_probe.lean`.

---

## 2. Recompile of the NEW files from lanes FINAL-9..12

**Working recipe** (the one the existing lanes use, e.g. `ChainCert/verify_chain.sh`):

```
cd fable_independent_2026/lean_2026 && lake env lean <module>.lean
```

Toolchain: `leanprover/lean4:v4.34.0-rc2`, Lake 5.0.0, mathlib `v4.34.0-rc2` (prebuilt, 8758 oleans).

The four lane modules were copied into the lake project at `FINAL9to12/` and compiled there, so what
was audited is what the project builds. Lane originals were left untouched.

| file | lane | theorems declared | headline (`#print axioms`) | axioms printed | exit code | errors | warnings | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `FINAL9to12/FINAL9_StaticHalo.lean` | FINAL-9 lean_static | 23 | 18 | 18 | **0** | 0 | 20 | **PASS** |
| `FINAL9to12/Final10Stress.lean` | FINAL-10 lean_stress | 61 | 0 | 0 | **1** | 20 | 7 | **FAIL** |
| `FINAL9to12/Final11Budget.lean` | FINAL-11 lean_budget | 33 | 8 | 8 | **0** | 0 | 0 | **PASS** |
| `FINAL9to12/FINAL12_background_conservation.lean` | FINAL-12 lean_background | 30 | 30 | 30 | **1** | 2 | 16 | **FAIL** |

**Standard axioms** throughout: `[propext, Classical.choice, Quot.sound]`.

### `#print axioms` output, line by line

**FINAL-9** — 18/18 standard, zero `sorryAx`:
```
'FINAL9.quad_pos_root'          [propext, Classical.choice, Quot.sound]
'FINAL9.law_forward'            [propext, Classical.choice, Quot.sound]
'FINAL9.law_backward'           [propext, Classical.choice, Quot.sound]
'FINAL9.X_nonneg'               [propext, Classical.choice, Quot.sound]
'FINAL9.X_quad'                 [propext, Classical.choice, Quot.sound]
'FINAL9.X_mul_one_add'          [propext, Classical.choice, Quot.sound]
'FINAL9.X_le_sq'                [propext, Classical.choice, Quot.sound]
'FINAL9.X_strictMono'           [propext, Classical.choice, Quot.sound]
'FINAL9.Mc_zero'                [propext, Classical.choice, Quot.sound]
'FINAL9.X_hasDeriv'             [propext, Classical.choice, Quot.sound]
'FINAL9.Mc_hasDeriv'            [propext, Classical.choice, Quot.sound]
'FINAL9.rhoC_closed'            [propext, Classical.choice, Quot.sound]
'FINAL9.rhoC_closed_x'          [propext, Classical.choice, Quot.sound]
'FINAL9.rhoC_column_limit'      [propext, Classical.choice, Quot.sound]
'FINAL9.rhoC_outer_limit'       [propext, Classical.choice, Quot.sound]
'FINAL9.vInf_sq'                [propext, Classical.choice, Quot.sound]
'FINAL9.vInf_four'              [propext, Classical.choice, Quot.sound]
'FINAL9.vInf_sq_rM'             [propext, Classical.choice, Quot.sound]
```

**FINAL-10** — the file contains **no `#print axioms` directives at all**; the `axioms`
report it advertises in its header is absent. Elaboration aborts with 20 errors, e.g.
```
FINAL9to12/Final10Stress.lean:204:33: error: linarith failed to find a contradiction
FINAL9to12/Final10Stress.lean:313:4:  error: `field_simp` made no progress on the goal
FINAL9to12/Final10Stress.lean:321:6:  error: `fun_prop` was unable to prove `ContinuousOn (fun u ↦ 2 * (u - log (1 + u))) (Set.Ici 0)`
FINAL9to12/Final10Stress.lean:369:6:  error: Tactic `rewrite` failed: Did not find an occurrence of the pattern
FINAL9to12/Final10Stress.lean:588:52: error: unsolved goals
```

**FINAL-11** — 8/8 standard, zero `sorryAx`:
```
'Final11.X_pos_and_quad'        [propext, Classical.choice, Quot.sound]
'Final11.X_break'               [propext, Classical.choice, Quot.sound]
'Final11.X_break_full'          [propext, Classical.choice, Quot.sound]
'Final11.ratio_break'           [propext, Classical.choice, Quot.sound]
'Final11.demand_over_budget'    [propext, Classical.choice, Quot.sound]
'Final11.share_over_delivered'  [propext, Classical.choice, Quot.sound]
'Final11.gas_column_canonical'  [propext, Classical.choice, Quot.sound]
'Final11.gas_column_alternative'[propext, Classical.choice, Quot.sound]
```

**FINAL-12** — 30 printed; 24 standard, **6 carry `sorryAx`**:
```
'FINAL12.nExp_deriv'            [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
'FINAL12.cs2_exponential'       [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
'FINAL12.cad2_exponential'      [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
'FINAL12.exp_w_minus_cs2'       [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
'FINAL12.kJ2_exponential'       [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
'FINAL12.kJ2_exponential_ratio' [propext, sorryAx, Classical.choice, Quot.sound]   <-- sorryAx
(+ 24 further theorems, all [propext, Classical.choice, Quot.sound])
```
Root cause, from the same run:
```
FINAL9to12/FINAL12_background_conservation.lean:211:4:  error: Type mismatch: After simplification, term
FINAL9to12/FINAL12_background_conservation.lean:348:61: error: unsolved goals
```

---

## 3. `sorry` — proof terms, not file text

Command run per file:

```
grep -cE '(^|[^`])sorry([^`]|$)' <file>
```

| file | regex count | raw `sorry` (any case, incl. backticked) | classification of matches |
|---|---:|---:|---|
| `FINAL9to12/FINAL9_StaticHalo.lean` | **0** | 0 | none |
| `FINAL9to12/Final10Stress.lean` | **0** | 1 | line 25, `` `sorry` `` — backtick-quoted word inside the header `/--` doc comment. Inspected: not a proof term. |
| `FINAL9to12/Final11Budget.lean` | **0** | 1 | line 8, `` `sorry` `` — backtick-quoted inside the header doc comment. Inspected: not a proof term. |
| `FINAL9to12/FINAL12_background_conservation.lean` | **0** | 0 | none |

So no file contains a `sorry` in a proof term. Both raw hits are the *word* "sorry" in prose, back-ticked,
exactly the case the regex is designed to exclude — inspected rather than assumed clean.

### `sorryAx` in axioms lines

`sorryAx` is Lean's error-recovery placeholder: it is inserted when a declaration's proof fails to
elaborate. It is therefore a **proof-term `sorry` that is invisible to any text grep**.

| file | `sorryAx` in axioms lines |
|---|---|
| `FINAL9to12/FINAL9_StaticHalo.lean` | **none** ✔ |
| `FINAL9to12/Final10Stress.lean` | **none** (but no axioms printed at all — file does not elaborate) |
| `FINAL9to12/Final11Budget.lean` | **none** ✔ |
| `FINAL9to12/FINAL12_background_conservation.lean` | **6** ✘ — `FINAL12.nExp_deriv`, `FINAL12.cs2_exponential`, `FINAL12.cad2_exponential`, `FINAL12.exp_w_minus_cs2`, `FINAL12.kJ2_exponential`, `FINAL12.kJ2_exponential_ratio` |

FINAL-9 is the instructive case: at 23:24 its own log showed 11 `sorryAx` theorems; by the audited
snapshot it was down to 0 with exit 0. Its text never contained `sorry` at any point — only the
axioms line reveals it.

---

## 4. DELTA — re-hash of the pre-existing sources

```
PRE-EXISTING (T0) : 354
NOW               : 362
new names         : 8
overlap           : 354
deleted/renamed   : 0
byte-identical    : 354 / 354  -> YES
```

**Every one of the 354 pre-existing sources is byte-identical.** Nothing in the pre-existing tree was
moved, rewritten, or deleted while the lanes ran.

Breakdown of the 8 new names:

| new name | provenance |
|---|---|
| `FINAL9to12/FINAL9_StaticHalo.lean` | FINAL-13 audit copy of lane FINAL-9 (lean_static) |
| `FINAL9to12/Final10Stress.lean` | FINAL-13 audit copy of lane FINAL-10 (lean_stress) |
| `FINAL9to12/Final11Budget.lean` | FINAL-13 audit copy of lane FINAL-11 (lean_budget) |
| `FINAL9to12/FINAL12_background_conservation.lean` | FINAL-13 audit copy of lane FINAL-12 (lean_background) |
| `FINAL9to12.lean` | FINAL-13 root aggregator for the new `[[lean_lib]]` |
| `probe_f14.lean` | sibling-lane scratch (out of scope; not FINAL-9..12) |
| `fastprobe.lean` | sibling-lane scratch (out of scope) |
| `_probe_f18.lean` | sibling-lane scratch (out of scope) |

Note: `_probe.lean` was already dirty at T0 (pre-existing modification, not counted as new).

---

## 5. Lake registration — real `[[lean_lib]]`, `defaultTargets` unchanged

`lakefile.toml` now carries a fourth target, following the A83 precedent verbatim:

```toml
# FINAL-9..12 closure modules (LEAN-STATIC / LEAN-STRESS / LEAN-BUDGET, audited by lane
# FINAL-13).  Added as a separate library so `lake build FINAL9to12` is a real project
# target; `defaultTargets` above is unchanged, so the default build stays as it was.
[[lean_lib]]
name = "FINAL9to12"
```

**`defaultTargets = ["Mondlean", "ChainCert"]` is unchanged** (still line 4, byte-for-byte the
same as at T0). The new library is *not* a default target.

A root aggregator `FINAL9to12.lean` was added, matching how `A83.lean` and `ChainCert.lean`
anchor their libraries — without it Lake looks for a module named `FINAL9to12` and fails with
`no such file or directory`.

### Verified

| check | command | result |
|---|---|---|
| config still parses | `lake env printenv LEAN_PATH` | `EXIT=0` ✔ |
| **default build green** | `lake build` | `Build completed successfully (8785 jobs)`, `EXIT=0` ✔ (baseline T0: `EXIT=0`, 5m52s) |
| **new target is real** | `lake build FINAL9to12` | resolves and elaborates `FINAL9to12.Final11Budget`, `FINAL9to12.FINAL9_StaticHalo`; fails on genuine lane-source errors — **not** "unknown target" ✔ |

**`lake build FINAL9to12` is currently `EXIT=1`.** The target is registered and wired correctly,
but two of the four lane modules do not elaborate. That is a defect in the lane sources, not in the
registration — the build is red because the proofs are, and it will go green exactly when FINAL-10 and
FINAL-12 are fixed.

### No disconnected toolchain

One lake project, one toolchain (`lean-toolchain`: `leanprover/lean4:v4.34.0-rc2`), one mathlib
(`.lake/packages/mathlib`). `defaultTargets` was not widened, so the historical default build
(`Mondlean` + `ChainCert`) is bit-for-bit the build it was before this lane.

---

## Files written by FINAL-13

| path | what |
|---|---|
| `fable_independent_2026/lean_2026/lakefile.toml` | **modified** — added `[[lean_lib]] FINAL9to12`; `defaultTargets` untouched |
| `fable_independent_2026/lean_2026/FINAL9to12.lean` | root aggregator for the new lib |
| `fable_independent_2026/lean_2026/FINAL9to12/{FINAL9_StaticHalo,Final10Stress,Final11Budget,FINAL12_background_conservation}.lean` | audited copies of the lane modules |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/AUDIT.md` | this report |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/manifest_baseline.sha256` | T0 hashes, 354 pre-existing sources |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/manifest_now.sha256` | T1 hashes, 362 files |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/baseline_names.txt` | T0 name list (for the delta) |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/baseline_marker.txt` | T0 timestamp |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/audit_lean.py` | audit harness: compile + axioms + sorry census |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/delta.py` | re-hash and diff |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/audit_new.json` | first (stale-snapshot) compile pass |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/audit_final.json` | audited compile pass, full raw output |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/rows.json` | table rows |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/default_build_T0.log` | default build at T0 |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/lake_verify.log` | default build + first target attempt |
| `hy4_preview_push/FINAL-13_LEAN_AUDIT/lake_verify2.log` | default build + `lake build FINAL9to12` after the fix |

---

## Caveats

1. **Lanes were concurrent.** FINAL-9..12 were still writing while this audit ran. Every verdict above
   is pinned to the sha256 listed at the top; the source files changed several times during the run
   (FINAL-9 was fixed from 11 `sorryAx` theorems to 0 mid-audit). Re-run `audit_lean.py` to re-certify.
2. **FINAL-12 changed after the snapshot** (source mtime 00:00:16 vs. the 23:53:11 bytes audited here),
   so its FAIL reflects the snapshot, not necessarily its current state.
3. **FINAL-10 is incomplete**, not merely broken: it ships 61 theorem declarations but no `#print axioms`
   report, so there is nothing to certify yet.
4. The `.lake` tree is excluded from the manifest: 9947 of the 9947+354 `.lean` files are vendored
   mathlib under `.lake/packages`, not project sources.
