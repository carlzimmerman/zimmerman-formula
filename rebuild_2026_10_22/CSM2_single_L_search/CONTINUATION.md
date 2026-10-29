# CSM2 live continuation

Owner: this chat. Target: fixed corrected model's single-L feasibility.
Ancestry and frozen definitions are in `TARGET.md` and per-run manifests.

Completed: paired-resolution/binning diagnostic and independent crossing
reconstruction. Estimator instability is demonstrated for seeds 3 and 7;
seed 8 is stable under the tested binning changes. No replacement is adopted.

Active: `launch.py run_001`, launched once, exec session 39935. Bound: wall
1800 seconds, CPU 1200 seconds per process, one numerical thread. Partial
`run_001/results.json` is refreshed per completed cell; `manifest.json` appears
when finished. Do not launch a duplicate or edit the pinned driver/contract/
TARGET while it runs. Both CSM1 baseline controls passed before new cells.

Next actions:

1. On completion validate manifest/hashes and independently recompute group
   PASS and lens delta-law from raw source results. Preserve finite failures.
2. A necessary-test survivor must receive the full CSM1 calibration and heldout
   grades at that same L. No extra T, changed cut, profile or data repair.
3. With no survivors, publish the finite result and actual transition regions.
   Continue the continuous-L question through interval bounds or a valid
   profile/covariance reduction. Do not assume likelihood/Z monotonicity or
   turn a grid into a theorem.
4. Lower native L proxies can be excluded through the existing actual LG
   threshold and fixed-UFD two-state reduction without redundant full fits.

Await remaining native seeds. Resolve estimator robustness before claiming a
derived level, even if the old scorer obtains seven `ok` flags. The completed
diagnostic does not prescribe a new crossing rule or disprove the physical
model. User authorizes bounded discriminating work and pushing verified
checkpoints; publish completed evidence separately from active outputs and
preserve unrelated staged/dirty work.
