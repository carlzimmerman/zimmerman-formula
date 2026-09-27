# XR10: the answer validator — is every row the answer calls an M* result run on M*?

The final answer (`ANSWER_AS_IT_STANDS.md`) is assembled from lanes run by parallel sessions. On 2026-09-26 results
were silently mixed across settings five times: switch cells, switch branches, cap forms, force operators and epochs.
XR10 is the gate that catches this before anything is committed. It reads the **code**, not docstrings or README rows.

Nothing outside the `XR10_` files was edited, and no simulation was run. The validator imports nothing from the lanes.
It reads source (the committed blob for committed lanes, the working tree for uncommitted ones) and committed
results JSON / `.out` files. A run takes about 5 s.

| file | what it is |
|---|---|
| `XR10_answer_validator.py` | The gate. M* is the `MSTAR` block at its top. |
| `XR10_answer_rows.json` | The registry: 54 rows (one per result that bears on M*), 14 shared traces ("atoms"), 12 rules (5 enabled, 7 candidates). Each row's `recorded` block holds its commit, committed verdict, status and every axis's file:line at the snapshot. |
| `XR10_answer_validator.out` | The main run: rc = 0. |
| `XR10_answer_validator_MUTATE.out` | `MUTATE=1`: DE10's registered cap form is corrupted to `kappa_MS5`, hiding its withdrawn local form. Check D catches it from the source: rc = 1. |
| `XR10_answer_validator_SCORECARD.out` | `XR10_SCORECARD=1`: the answer page's scorecard rows are treated as claimed M* results. rc = 1: none of them is on M* today (table below). |

Run it from the repository root:
`python3 real_research/cross_thread_review_2026_09_26/XR10_answer_validator.py` (add `MUTATE=1` or `XR10_SCORECARD=1`).
`XR10_SNAPSHOT=1` rewrites each row's `recorded` block (commit, verdict, status, file:line per axis) from the code as it
is now. Later runs report traces that moved; that is never an rc = 1.

## How it works

**Traces.** Each axis of each row carries `src` (a file), `pattern` (a regex that finds the defining line) and a
derivation:
- `classify`: a signature table in the validator maps the line to a category (switch reading, cap form, kernel,
  carrier, operator). The registry's value is never used to classify.
- `float` / `floats` / `power`: numbers are parsed from the line. `power` reads p off `x_c0 * E2 ** p`, where no
  exponent means p = 1.
- `footings`: `canonical` / `alt` tokens (`A0C`, `A0A`) are collected over every matching line.
- `absent`: "none", asserted because no cap signature appears anywhere in the listed files.
- `present`: the line must exist, and the value is taken as registered. This is weak, and not allowed on an M* claim.
- `na`: the axis does not enter this row. A reason is required; a file:line is optional.

An entry may also carry:
- `via`: import or call links that must still exist;
- `use`: the stage it belongs to (`pm_dynamics`, `halo_model_shear`, `harvey_map`, `kids_gate`, ...);
- `classify_on`: classify only part of the line, e.g. one entry of a dict;
- `same_as`: inherit the axis's traces from another row.

**Statuses per axis.**
- MATCH.
- COMPAT: an enabled rule applies, meaning a committed lane showed the difference is controlled for this row's gates
  and the row's `scope` states the rule's id in brackets.
- MISMATCH.
- N/A.

**Row statuses.**
- ON-M*.
- ON-M*~: on M* with stated approximations.
- OFF-M*.
- PARTIAL: a core axis is not traced.
- n/a: the row does not instantiate the model.

A row's status describes its **settings**, not its result. DE12 is ON-M*, and its result is an obstruction.

**Flags.**
- CAP-SPLIT: two stages of one row use different cap forms, one of them a mismatch.
- SWITCH-SPLIT: the same, for switch readings.
- FOOTING-PARTIAL.
- EPOCH-MIXED: carrier retention measured more than `epoch_dz_tol` away from the epoch it is scored at.

**rc = 1 if:**
- (D) a committed row's code no longer says what the registry says (drift or a lost trace);
- (M) a row claimed `"M*"` has any MISMATCH, is uncommitted, or has a defining axis asserted rather than derived;
- (E) an enabled rule's committed evidence fails;
- (C1) the control fails: L395's cell (c) must be flagged from its source. Its particle-mesh dynamics use the withdrawn
  local cap (`L395.py:127`), and its shear is scored with the hard 1.75 Mpc radius (`L395.py:92`): CAP-SPLIT;
- (C2) a negative control fails:
  - MS5's κ-form shear must MATCH on cap form;
  - MS3's hard radius on halo-model shear must be COMPAT;
  - L396's κ cap in the dynamics plus the hard radius in its shear must not be split;
- (C3) the positive control fails: MS5's κ-form shear row, re-evaluated with the epoch tolerance widened, must pass
  an M* claim. The claim gate is not vacuous: the epoch is the only thing that keeps that row off M*.

## M* and the rules

M* (`MSTAR`):
- the switch reads CV3's constrained form;
- the cap is MS5's κ form;
- p = 1, x_c0 = 2.5, 0 < w ≤ 0.25;
- the kernel is ν_mono, and σ = 1;
- the operator is A;
- the carrier is L388's density trigger, kicked at 575–650 km/s;
- both footings;
- retention within 0.1 in z of the scoring epoch.

MS1's `lap(Phi − v)` (phiX) is recorded and is a MATCH for data gates. **For action-level rows it is a MISMATCH:**
CV3 G3/G3b find that it reads the multiplier Φ, and its lapse constraint goes singular. This is the one place the
validator is stricter than the brief, and it affects only structural rows (MS1.A3, MS5.A1).

**Enabled rules** (the coordinator's; each re-checked in committed files on every run):
- `OP_B_FOR_A`: the PM operator for the action's. XR5 gives monopole ≤ 2.2e-3 and Harvey |Δβ| ≤ 5e-5. It holds
  for every gate except the EFE family (cluster-infall BTFR, LV dwarfs, Coma UDGs, LG zero velocity).
- `ABS_FOR_CONSTRAINED`: MS3's door (ρ_b plus the positive untruncated phantom) for CV3's form (MS1 A3, CV3 G1/G2).
  Data gates only.
- `SIGMA0_FOR_SIGMA1`: KiDS (DE8, |ΔΔχ²| ≤ 0.40) and Harvey (XR5 H1) only.
- `HARDW_FOR_SMOOTH`: a hard switch for w ≤ 0.25. DE9's C2 must pass, and DE9's MOND-sector window at M*'s p must
  contain M*'s x_c0 at w = 0.1 and 0.25.
- `HARDCAP_FOR_KAPPA_SHEAR`: the hard 1.75 Mpc radius for κ, on halo-model shear only. MS5 S1 must equal MS3 K1.
  The evidence is at x_c0 = 2.5.

**Candidates** (reported, never applied; set `"enabled": true` in the JSON to adopt one — the owner's call):
- `C_FOR_A_HARVEY`: XR5 H1 includes C.
- `NU_RAR_BELOW_YSTAR`: ν_RAR = ν_mono for y ≤ 2.337; the flagship is scored at y = 0.1.
- `CAP_NONBINDING_KIDS`: DE10 S1 scaling 1.0000, and MS3 K1.
- `FLAGSHIP_CAP_NONBINDING`: ℓ_cap(2.5) = 216 kpc, against r_F ≤ 38.6 kpc.
- `FOREST_CAP_NONBINDING`, `DE11_CONSERVATIVE_OP`, `DE11_CONSERVATIVE_CARRIER`: DE11's own arguments, not controls.

## How an owner adds a row

1. Add an object to `rows` in `XR10_answer_rows.json`. Copy a similar row, e.g. `DE10.kids` for a KiDS score or
   `L396.msck` for a particle-mesh cell, and edit it:
   ```json
   {"id": "L396.msck", "lane": "L396", "script": "real_research/dark_sector_2026/L396_msc_cell_575.py",
    "results": ".../L396_msc_cell_575_results.json", "out": ".../L396_msc_cell_575.out",
    "claim": "pending", "scorecard": true, "kind": "data",
    "gates": ["s8", "forest", "clearing", "xcop", "cosmic_shear_halo_model"],
    "scope": "... MS3's door [ABS_FOR_CONSTRAINED] ... L377's PM [OP_B_FOR_A] ...",
    "headline_check": "R1",
    "axes": {"switch_reading": [{"value": "mond_sector_abs", "use": "pm_dynamics", "src": "...L396_msc_cell_575.py",
                                 "pattern": "xms = 1\\.5 \\* Om_a\\(a\\) \\* \\(rb \\+ np\\.maximum\\(dph_all, 0\\.0\\)\\)",
                                 "derive": "classify"}],
             "cap_form": [...], "p": [...], "x_c0": [...], "w": [...], "kernel": [...], "sigma": [...],
             "operator": [...], "carrier": [...], "kick": [...], "footings": [...],
             "epoch": [{"role": "score", "value": 0.5, "use": "halo_model_shear", ...},
                       {"role": "retention", "value": 0.0, "use": "halo_model_shear", "what": "...", ...}]}}
   ```
   - Every axis needs a code line.
   - `claim` is one of `"M*"` (the answer cites it as an M* result), `"comparison"`, `"structural"` or `"pending"`.
   - Gate names in the EFE family matter for `OP_B_FOR_A`.
   - Put a rule's id in brackets in `scope` only if the lane itself states that approximation.
2. If a line's category is new, add a regex to `SIG` in the validator. The classifier requires exactly one category.
3. Run the validator:
   - every trace must resolve (no `TRACE LOST`, no drift);
   - a row claimed `"M*"` must be committed and ON-M* or ON-M*~;
   - its switch, cap and carrier must be classified from code;
   - its p and x_c0 must be parsed from code.
4. Record the row with `XR10_SNAPSHOT=1`. This writes its commit, verdict and file:line per axis into `recorded`.
5. When a lane's code changes, the committed row drifts and rc = 1. Update the pattern or the value, and re-run.

## After XR9 moves x_c0

Re-run with the new cell, e.g. `XR10_XC0=3.5 python3 .../XR10_answer_validator.py`, or edit `MSTAR`. Also:
- `XR10_P`, `XR10_WMAX` and `XR10_EPOCH_TOL` override the other parameters.

What changes:
- Every row at x_c0 = 2.5 becomes a MISMATCH on `x_c0`. XR9's scans stay MATCH, because they contain the new cell.
- `HARDW_FOR_SMOOTH` is re-checked against DE9's window at the new x_c0. At 3.5 it falls outside [1.667, 3.448] at
  w = 0.1, so hard-switch rows become mismatches.
- `HARDCAP_FOR_KAPPA_SHEAR`'s evidence exists only at x_c0 = 2.5, so it stops applying. Add committed evidence at the
  new cell before re-enabling it; XR9_cosmic_shear computes the κ form's ℓ_cap per cell. C2's and C3's hard-radius
  checks are skipped.
- rc stays 0 unless a row claimed M* is now off M*. Tested: `XR10_XC0=3.5` gives rc = 0 and 0 rows on M*.

## The table today (HEAD 6daea932c, 2026-09-26 night)

**On M\*:**
- **DE12** (7f84b3546) is on M*'s gate: CV3's constrained form, the κ branch, p = 1, x_c0 = 2.5, both footings. Its
  verdict is an **action-level obstruction**: the varied gate makes transition-layer gas unstable.
- **DE13** (6daea932c) tests the repair on the same gate, 10/11 with R1's pre-declared λ range recorded as failed.
  - A gradient energy on f (form ii) stabilises no galaxy layer (E2).
  - The |∇U|² form stabilises 32/32 layers (F1, reported).
- **No data row is on M\*.** A claim on any of them fails today.

**The scorecard's rows, and what keeps each off M\*** (`XR10_SCORECARD=1`: rc = 1):

| row | commit | off M* because | nearest fix |
|---|---|---|---|
| MS2 flagship | 2a5def6d9 | kernel ν_RAR (DE4 → L320); no cap; carrier cleared by hand (S = 0; S ≤ 0.059 still passes), not L388's retention at r_F | candidates NU_RAR_BELOW_YSTAR and FLAGSHIP_CAP_NONBINDING cover two axes; L388's z = 2.5 retention at r_F is measured nowhere |
| MS3 K1 / MS4 S1 / MS5 S1 κ shear | 2a5def6d9, 969a15e7f, 61a3a0858 | **EPOCH-MIXED**: L388's retention by mass is at z = 0 (clusters, `L388.py:116`), the galaxy anchor is the z = 2 fixed-cell clearing (`L388.py:121`), and both are scored at z = 0.5 | score with retention measured at z ≈ 0.4–0.5 (C3 shows the epoch is the only blocker) |
| DE10 KiDS | dabce1b73 | cap = the withdrawn local form (`DE10.py:150`), non-binding; carrier = L375's shell model (a matter-only trigger), not L388's | the candidate CAP_NONBINDING_KIDS covers the cap; the carrier is a real difference |
| DE11 forest | aa6588d56 | no cap; an all-matter single-fluid operator; no carrier clearing | DE11's own conservative argument (three candidates) |
| L391 RAR/RC100 | 441d811e2 | no switch; L376's shell carrier | — |
| XR6 EFE/UDG (A) and LG | 6566c53b3 | cap = the withdrawn local form | XR9's κ re-score (pending) |
| L396 (pending, the decisive run) | uncommitted | PM canonical only (`A0C` at `L396.py:183`); shear retention z = 0 / z = 2 used at z = 0.5 | one alternative-footing box; shear from its own z = 0.4 retention (RB4, already computed) |
| L389 → L397 Harvey (pending) | uncommitted | **SWITCH-SPLIT**: the Harvey lensing root and 3-d phantom map use L370's ABSOLUTE MATTER mask (`L370.py:230`, `:296`: ρ_b + carrier, no phantom); σ = 0 and operator C not stated in scope; canonical only | a MOND-sector mask in L370's Harvey step; state [SIGMA0_FOR_SIGMA1] |

The other rows are comparisons, off M* by design:
- **Curvature or matter switch:** MS1.N1, DE1, DE2, DE4–DE9, L388, L390, L392, AT3, XR2.
- **L372 two-mode carrier:** L392, L393, L394.
- **AT acceleration-triggered carrier:** AT1–AT4.
- **Structural:** CV1–CV4, MS1.A3, MS5.A1, DE7, XR5, XR7, and DE12/DE13 (on M*'s gate).

**Pending** (sources traced from the working tree; drift is reported, not failed): DE11b, L389, L393, L394, L395
(a/b/c), L396, L397, and XR9 (kids, shear, environment). XR9.kids is on M* in everything but the carrier (L375's
shell model).

**Action-level note.** MS5's κ cap reads Φ_X = Φ − v, the multiplier Φ, which CV3's reading B also reads. CV3 G6
checked capped gates built from the constrained fields only in local-v forms. The κ form on the constrained fields
has not been checked.

## Limits

- A trace proves that a line exists and what it says, not that the line runs on the path that produced the result.
  The via-links cover the import chains. Branches inside functions are not followed.
- A few traces read docstrings. The XR6 CANDIDATE block, XR9_environment's cap and DE12's switch are labelled as
  such in the rows. Code lines should replace them when those lanes are next edited.
- The halo model and the radial point-mass profiles have no field operator. They are N/A on `operator`.
- The categories, the epoch tolerance and the core-axis set are this review's choices, stated above. The owners own
  the rows; the coordinator owns the rules.
