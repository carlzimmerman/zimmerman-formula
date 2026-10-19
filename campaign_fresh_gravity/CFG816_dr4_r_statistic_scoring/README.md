# CFG816: the DR4 R statistic (scoring script and controls)

Criteria: `FROZEN_CRITERIA.md` (d9eed26eb, committed alone before this script). Script: `cfg816_r.py`. Status 2026-10-16: **script written; controls C0, C1, C2, C3, C5 and MUTATE run on synthetic
pairs and pass; C4 (the DR3 code-path run) is NOT RUN; no DR3 or DR4 data have been read; no result.** κ = ½ is fitted; the cold mass is still required.

## Use
| command | what it does |
|---|---|
| `python3 cfg816_r.py` | controls C0-C3 and C5 on synthetic pairs (about 40 s, one core); writes `cfg816_r.out`, `cfg816_r_results.json`; exit 0 if all run controls pass |
| `python3 cfg816_r.py --mutate` | MUTATE (×1.2 at x > 1 on a synthetic null); exit 1 = detected = the test bites; writes `*_MUTATE.*` |
| `python3 cfg816_r.py --dr3 TABLE` | C4 on the registered DR3 sample (needs the owner's yes and the download); once only |
| `python3 cfg816_r.py --dr4 TABLE` | THE RUN, once, after DR4 is public and only on the owner's yes; refuses a second run; a change goes under "Departures" below |

Pair table (CSV): `sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc` (the registered `ingest_csv` columns) plus `plx_err_frac, ruwe1, ruwe2, ipd1, ipd2, vt_err, drv_kms` (blank if no RV), `nss1, nss2`.
The script refuses a table that lacks any checklist column. The converter `make_pair_table.py` builds that table (section "The converter" below).

## Results of the controls (synthetic; Rayleigh ṽ with median 0.489, x log-uniform 0.05-5, M = 1.8 M☉)
- **C0 (added):** the ṽ computed here equals the registered `wide_binary_pipeline.ingest_csv` ṽ exactly (difference 0).
- **C3:** the class arithmetic reproduces Amendment 22: σ_tot = 0.0896 / 0.0507 / 0.0385 / 0.0276 / 0.0225 at N = 1421 / 5000 / 10⁴ / 3×10⁴ / 10⁵; KILLED needs R ≥ 1.269 / 1.152 / 1.116 / 1.083 / 1.068; CONSISTENT unavailable.
- **C1:** R is recovered within 2σ_R in 200/200 repeats for each R_true ∈ {1.00, 1.05, 1.20} at N = 1421 and 30000 (this is easy to pass, because σ_R carries the 0.02 floor).
- **C2:** the bootstrap σ is calibrated: at N = 1421 its mean is 0.0454 against an empirical scatter of R of 0.0456; coverage 66.9% (target 68% ± 5%); KILLED never fires on 1000 null repeats. Coverage with σ_R is 97.7% (over-covers, by design; interpretation I3).
- **C5 (added):** the CSV path round-trips exactly; a boost carried only by NSS-flagged pairs comes out CONTAMINATION-LIMITED; a boost carried by every pair comes out KILLED.
- **MUTATE:** R = 1.208 at (R − 1)/σ_R = 7.0: detected.

## Interpretations made while implementing the frozen text (none changes a frozen threshold)
I1 N = pairs that enter R (numerator + denominator); numerator-only is printed as a sensitivity. I2 stratified bootstrap (within each regime). I3 C2 coverage is applied to the bootstrap σ alone; σ_tot carries an
assumed 0.02 systematic that synthetic data lack. I4 C2 uses 300 resamples per repeat (the run uses 2000). I5 C4 passes if R − 1 < 2σ_R on the DR3 primary (the second leg, (1.20 − R)/σ_R > 1, was dropped on 2026-10-17 before any R was computed: the registered DR3 catalogue gives only 175 + 173 pairs in the two regimes, σ_R ≈ 0.18, and that leg would demand R < 1.02). I6 C0 added. I7 C5 added.
I8 the f_tail z-test applies only if both regimes hold ≥ 5 pairs with ṽ > 2, else "n/a (<5 events)" (found by MUTATE: on a clean sample, one or two stray events gave a spurious 2.1σ).

## Known weaknesses, stated against interest
1. **The frozen f_tail rule can over-flag a genuine boost.** A real 20% broadening of the ṽ distribution also raises the fraction above ṽ = 2, so a significant f_tail difference does not by itself identify contamination. The label is reported with the raw
   numbers and is never the only output, and the rule only ever makes a kill harder, but it is a weakness of the frozen text. Changing it needs a new dated file, not an edit.
2. **f_tail is ≈ 0 in the synthetic samples** (a Rayleigh tail), so the controls cannot exercise it; real data have a percent-level tail.
3. **C4 has not run**, so the full control set is incomplete; the script says so in its own output.
4. **σ_tot is a registered assumption, not a measurement**; at every N it exceeds the bootstrap σ (0.0126 against 0.0298 at N = 30000), so the classes are set by the floor, not by the data's precision.

## Departures
None yet (no data read).

## The converter (`make_pair_table.py`, written 2026-10-17)
`python3 make_pair_table.py --catalogue <stage-G CSV> --per-star <per-star .npz> --out <pairs.csv>` joins the registered stage-G catalogue (`sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc, source_id1, source_id2`) with the per-star
columns by source_id and writes the table `cfg816_r.py` reads, plus `<out>.manifest.json` (input and output SHA-256, counts, every choice). It computes no R. `--self-test` runs nine synthetic checks (all pass), including
that a missing source_id, a missing column and a constant column are all REFUSED, never silently filled. Choices P1-P5 are listed in its docstring (the larger parallax fraction of the two stars; ΔRV only where both stars have an RV;
a leading-order ṽ error, not Cookson's full Jacobian; the per-star NSS flag; v_perp, masses and distance taken unchanged from stage G).

**DR3 pair table built (no download; the on-disk extract):** `pairs_dr3.csv` from `real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv` (6210 pairs, SHA-256 in the manifest) and `stage_A.npz`; 0 source_ids missing. The primary
sample (d < 130 pc, RUWE < 1.25, ipd = 0, ΔRV < 10, ṽ ≤ 2.5, ṽ error < 0.1) has 1307 pairs; **175 in the outer regime (x > 1) and 173 in the inner (x < 0.3), so N = 348 enter R** and σ_R ≈ 0.18 (σ_tot 0.1775). A
KILLED label at that N would need R ≥ 1.53. DR3 is a code-path test, never a result (Amendment 7(e)); **the DR3 run `--dr3` has NOT been made** (its once-only slot is untouched).

### Two findings about the registered catalogue that the frozen design did not anticipate
1. **Every catalogue pair is already NSS-clean.** The registered stage G applies cut 12 (NSS screen) before it writes the catalogue (`build_catalog.py`, `frozen_cuts`; PLAN.md Q2: 0 flagged components), so `nss1 = nss2 = 0` for all
   12,420 stars. With the registered catalogue as input, **the "NSS-screened" branch is identical to the primary and the NSS leg of the CONTAMINATION-LIMITED rule can never fire**; only the f_tail leg can. To realise the frozen
   design, the R analysis needs a catalogue built WITHOUT cut 12 (flags joined per star), which is a new, separately declared run of the registered driver. The converter's constant-column guard caught this (`--declare-neutral non_single_star`
   was needed, and is recorded in the manifest as constant by construction).
2. **No catalogue pair is wider than 30 kAU** (stage G keeps 2 < s < 30 kAU; DR3 maximum 29.6). The frozen primary's numerator cap of 50 kAU is therefore moot on this catalogue: the primary is the "r_sky ≤ 30 kAU" branch (identical counts, 175/173).
   Pairs between 30 and 50 kAU would need a rebuilt catalogue.
Both are decisions for the owner before 12-02; neither changes a frozen number.

## Checks queued behind the 1024³ chain (2026-10-18)
The owner chose "queue behind chain6" (no computation beside a 1024³ run). `_external_data/overnight_chain/cfg816_checks_waiter.sh` (untracked, like the other chain scripts; pid 28884 when armed, sleeping, ~2 MB) waits for an
idle window (no chain script, no heavy-run process, no process over 4 GB or 120% CPU, on three consecutive polls 120 s apart), then runs once at the lowest priority: the three frozen-file hash checks, `make_pair_table.py --self-test`,
`cfg816_r.py`, `cfg816_r.py --mutate`, and, only if all pass and `cfg816_r_dr3_results.json` does not exist, the once-only `cfg816_r.py --dr3 pairs_dr3.csv` (C4). Log: `_external_data/overnight_chain/cfg816_checks.log`; per-step logs
`cfg816_checks_<step>.log`; done marker `cfg816_checks_state/done`. Cancel with `kill 28884`. **The delay is unknown**: ARGON11 is queued behind chain6, so the first idle window may be days away.
Disclosure: the 2026-10-17 controls and converter run (13:50-13:51) probably overlapped a T2x 1024³ run (your notes give its start as 13:47); they were about 40 s on one core at `nice 10`, under 200 MB, and the run survived.

## Checks RUN (2026-10-18 21:37, owner: run beside the 1024³ job, 1 core, nice 19)
The queued checks ran once via `cfg816_checks_now.sh` (the waiter with the idle-window wait removed; same steps, same order). All passed:
frozen-file hashes OK; self-test rc 0; controls rc 0; mutate rc 1 (the test bites); C4 rc 0.
**C4 (DR3 code path, I5): PASS**, (R − 1)/σ_R = −0.15 on the NSS-screened primary (R = 0.973 ± 0.178, N = 348: 175 / 173).
Label UNDECIDED, as expected at DR3 size: R lies within 1.3 σ_R of every registered number (Newton −0.15, Arm A canonical −1.06,
alt −1.23, MOND 1.15 −1.00, MOND 1.20 −1.28). The a0-footing regime splits give R = 1.097 ± 0.163 (canonical) and 0.997 ± 0.173 (alt).
This is a code-path control, not a verdict: DR3 cannot separate the arms. Outputs: `cfg816_r_dr3.out`, `cfg816_r_dr3_results.json`.

## The catalogue variant (2026-10-18) and the DR3 C4 result
`build_variant_catalogue.py` builds the R-analysis input: the registered stage G minus the NSS cut and with the cap at 50 kAU (declaration and validation in `CATALOGUE_VARIANT_2026-10-18.md`; self-test 10/10 PASS, byte-identical with both
switches off). `wide_binaries_dr3_variant.csv` (6,308 pairs) and `pairs_dr3_variant.csv` are the DR3 results of the build and the converter. **Official C4 (made 2026-10-18 21:37, owner override beside T2x, on the registered-catalogue table
`pairs_dr3.csv`): R = 0.9728, σ_R = 0.1775, UNDECIDED, PASS.** The variant table has not been scored; doing so is a second DR3 run and needs the once-only guard relaxed with a tag (to be listed under Departures).

## Departure D-variant (2026-10-18): R on the variant table
**Information only. The official C4 stands** (2026-10-18 21:37, `pairs_dr3.csv`: R = 0.9728, σ_R = 0.1775, N = 348, UNDECIDED, PASS; `cfg816_r_dr3.out` and `cfg816_r_dr3_results.json` unchanged, SHA-256 checked before and after).
This is a second DR3 code-path run on a different input, made after the official one, so it is listed here as a departure; DR3 is never a result (Amendment 7(e)) and the frozen criteria are untouched.
- **Guard change (the smallest opt-in):** `cfg816_r.py` now accepts `CFG825_DEPARTURE_TAG=<word>` with `--dr3` only (refused with `--dr4`; the word must be alphanumeric). With it, the run writes only
  `cfg816_r_dr3_<word>_DEPARTURE.out` / `cfg816_r_dr3_<word>_DEPARTURE_results.json`, refuses if those exist, and never writes the official files; the C4 rule is printed and stored as `C4_rule_information_only`, not `C4_pass`.
  Without the tag the script behaves exactly as before (the once-only guard on `cfg816_r_dr3_results.json` still refuses).
- **Command:** `CFG825_DEPARTURE_TAG=variant OMP_NUM_THREADS=1 nice -n 19 python3 cfg816_r.py --dr3 pairs_dr3_variant.csv` (beside the T2x 1024³ run on the owner's authorisation; 1 core, under 0.2 s, about 110 MB).
- **Result (primary):** R = 0.9223 (R − 1 = −0.078), σ_R = 0.1783 (σ_tot; bootstrap 0.096), N = 345 (170 outer / 175 inner), f_tail 0/0 events, **UNDECIDED**; the C4 rule would read PASS ((R − 1)/σ_R = −0.44; (1.20 − R)/σ_R = +1.56).
  Distance in σ_R: Newton −0.44, Arm A canonical −1.34, alt −1.51, MOND 1.15 −1.28, MOND 1.20 −1.56. a0-footing branches: R = 1.114 ± 0.164 (9.36×10⁻¹¹) and 0.932 ± 0.174 (1.13×10⁻¹⁰).
- **Shift from the registered R:** ΔR = −0.051 (−0.28 σ_R, about half the bootstrap σ). Within the variant, the NSS-screened branch (168 / 173) and the r_sky ≤ 30 kAU branch give the same R as the primary (0.9223), so the
  intended additions (NSS-flagged and wider pairs) do not move R on DR3; the shift comes from the changed pair membership, which `CATALOGUE_VARIANT_2026-10-18.md` attributes to the stage-G Monte-Carlo flip (about 2% of pairs each way; not separately tested here).
- Outputs: `cfg816_r_dr3_variant_DEPARTURE.out`, `cfg816_r_dr3_variant_DEPARTURE_results.json`. Nothing here says the data favour the framework; κ = ½ is fitted.
