# Continue from the faint HI candidate, not a gravity claim

User requested wrapping this phase and pushing the results so Claude can
continue. This packet is the current result. Theory closure and the physical
memory problem remain open. Do not restart the earlier attractive/capture/
polarization routes merely because those older packets are included.

Read `README.md`, `CHECKPOINT.json`, `audit/FAMILY_REVIEW.md`,
`audit/stats_RESULT.md`, `audit/stats_FOLLOWUP.md` and
`recovery/KNOWN_EXTENSIONS.md` first. The exact preferred TiRiFiC model was
not recovered. The authentic author baseline and the graph reconstruction
must never be conflated. The finite family is not a posterior.

The highest scan residual(−220,−60,−49.44) is a known published extension.
Its amplitude mismatch is real relative to this reconstruction, but it is
not an isolated unknown feature. The candidate worth a bounded next check
is near(x,z,u)=(−20,+100,+24.72),40×40arcsec×24.72km/s, with a related
37.08km/s box. See frozen IDs `followup_03` and `guarded_broad_positive` in
`followup_candidates.json`. Common40 flux minus empirical blank mean:
HR0.01780 with scatter0.00339; LR0.01139/0.00199; WHISP0.01018/0.01694.
HR/LR share visibilities. The old cube is too shallow for confirmation or
exclusion, and the negative control `followup_04` recurs in both products.

The next useful work is a discriminating observational/systematics check:

1. Inspect the frozen patch's spatial/channel coherence and sign against
   negative controls and the actual residual dirty beam. Split independent
   HALOGAS observing tracks if released visibility material allows it;
   HR/LR are not that split. Check calibration, CLEAN/deconvolution and
   channel-dependent local background before assigning it to HI.
2. Review the bounded later-cloud-catalog comparison in
   `recovery/LATER_CLOUD_CHECK.md` if marked unresolved. Exact sky/velocity
   membership matters; spatial proximity or an unmatched name is insufficient.
3. Recover the exact preferred file or obtain an adequate conventional tracer
   reconstruction before claiming a robust physical remainder. The best
   current central fit is7.93 blank-scatter RMS, and every three-amplitude
   calibration hits a bound. Full206-parameter covariance is unknown.
4. Seek deeper genuinely separate observations only if the patch survives
   those checks. WHISP would see the HALOGAS amplitude at only~one empirical
   scatter; its nondetection is underpowered. Do not combine sigmas or call
   reused older material blind replication.

Do not add a halo, LambdaCDM prior, the project acceleration law, or a fitted
new-force parameter to explain a tracer-model mismatch. No memory state is
identified by these data. Do not widen an uncertainty envelope until the
signal disappears and call that an explanation. Preserve the original scan,
source classification, all failed training cases and the negative controls.

Useful execution/state paths:

- `forward_model_v2.py`: audited full source renderer, native-grid operator.
- `uncertainty_scenarios.json` plus `trace_scenarios.json`:104+14 fixed cases.
- `family_run001`, `trace_run001`, `controls_run001`: saved component arrays,
  fits, bounds and numerical controls. `nominal_run001` is olderV1 history;
  its direct fine-grid variant is not same-operator convergence.
- `analysis_run002/arrays.npz`:118 predictions/components, masks, measured
  blanks, amplitude perturbations, finite numerical discrepancy and scans.
- `followup_model.py`, `followup_run001`: exact native grids for all imaging
  products, common40 family predictions with original HR amplitudes and
  no older-data fit. See native channel/frame/LSF caveats in audit.
- `extension_run001`: post-scan conservative known-extension sensitivity;
  not a recovered author segmentation or fresh blind search.
- `plot_run002`: final scientific figures and their bounded render record.

Every bounded runner manifest includes exact argv, software, input hashes,
status and limits. Start with existing arrays; do not rerun the full family
until a justified source/model/control change requires it. No install is
needed for the retained Python3.9/NumPy1.26/SciPy1.11 execution. Raw cubes
are omitted from Git because of size; reacquire exact files using
`../ngc5023_cube_2026_10_20/data/ACQUISITION.json`,
`../ngc5023_cube_2026_10_20/independent/acquisition.json` and the retained
bounded acquisition script. Verify the recorded SHA256 before execution.
Large raw products are still present in the original local checkout.

The push uses a separate `codex/` branch based on the observed owner HEAD;
only this chat's review packets/pointer and handoff packaging are added.
No owner campaign/scientific files are integrated, reset, stashed or merged.
