# Native ng64: completed seed outputs, partial ensemble

This package publishes finished seed snapshots as they arrive so Claude can
inspect the completed data before the full NL1 ensemble is available.
`completed_results.json` records the observed seed set, metadata, completion
checks and hashes. `completed/` contains byte-identical copies of each finished
snapshot, `done.json` and final run log. No rolling checkpoint is included.

At the initial publication, seeds **3 and 7 of 9** have finished, with 895
and 991 integration steps respectively; both have 57,777 particles. The other
seven runs remain pending. This is a partial ensemble, with **no aggregate
concentration estimate or observational grade**. The original NL1 scorer
requires at least seven valid measurements before grading; it has not produced
a result at this checkpoint. Snapshot `meta.L` is the simulation box length,
not the inferred concentration level `L_nat`.

Current published inventory: **7 of 9**, seeds **1, 2, 3, 5, 7, 8 and 9**.
Seeds4and6 remain pending. The seven-seed primary extension is in
measurement_005_seven/;
no aggregate NL1 grade is asserted.

Publication checks verify seed/grid/mass identity, finite position/velocity
arrays, particle count/mass, agreement of final snapshot metadata with the
completion marker and final log, stable source hashes, and exact copied bytes.
These checks establish completed-file integrity, not simulation convergence
or a successful scientific model. No run was restarted or modified.

Reproduce the publication/integrity check from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python3 -I rebuild_2026_10_22/NATIVE_PARTIAL_2026-10-28/publish_completed.py
```

The script adds only complete seed sets and refuses to replace an existing
snapshot with different bytes. It refreshes the observation timestamp and
completion inventory. It does not invoke NL1 or compute any new fitted number.
Read the corrected-model result in `../CSM1_consistent_core_switch/README.md`:
the old fixed-T NL1 primary grade cannot establish a corrected linked-T pass,
and a native level near 4 would not itself restore the lost lensing pass.

## Preliminary measurements of seeds 3, 7 and 8

The unchanged primary X48 estimator gives:

| Seed | Primary c_f | Conditional per-seed L proxy | Estimator flag |
|---:|---:|---:|---|
|3|3.138159|1.972446|ok|
|7|2.441598|1.534632|ok|
|8|4.010123|2.520507|ok|

These use NL1's existing normalization `L_proxy = 7.31*c_f/11.630199473419035`.
Seed 8 is higher than 3 and 7, but all three proxies remain below L near 4,
conditional on that resolution-transfer prescription. The value c_f=4.010
for seed 8 is not L=4: NL1 normalizes it to the displayed L proxy of 2.521.
Three early-finishing seeds are not a representative ensemble and supply no
reliable confidence interval. Do not call this L derived or a full NL1 result.
The separately reported NFW profile fits remain diagnostics, not replacements
for the predeclared primary estimator. No observational harness was run here.

`measurement_002_three/results.json` preserves the earlier three-seed
diagnostics; its bounded manifest pins source, snapshots and criteria. All five
implementation controls pass: original synthetic c=4 benchmark, rejection of
synthetic c=8 as nominal c=4, A2 reference values, exact reproduction of the
entire prior results for seeds 3 and 7, and stable input hashes.
`measure_three.py`, `three_seed_contract.json` and `THREE_SEED_CRITERIA.md`
document this unchanged-method extension. The criteria precede the new numbers.

The initial two-seed evidence remains unchanged in `measurement_001/`, with
`measure_completed.py`, `measurement_contract.json` and
`MEASUREMENT_CRITERIA.md`; its four original controls still pass.

Seed1 completed with1043 steps and57777 particles. Its unchanged primary
c_f=6.0951168067 and L_proxy=3.8310008318 are in measurement_003_four/.
Five extension controls pass, including exact prior3/7/8 reproduction. This
single primary value near4 is not evidence of ensemble convergence or a
robust derived L; the demonstrated binning instability remains unresolved.

Seed9 completion: primary c_f15.0898076731, L_proxy9.4844885801, ok;
601particles inside its first selected crossing. measurement_004_five/
passes5controls and reproduces all prior four measurements exactly. The high
primary value is not an ensemble estimate or evidence of estimator robustness.


New completions2and5: final snapshot/done/log copies pass63 total completion
checks across seven seeds. Seed2 primary c_f9.2357491476, L_proxy5.8050015757,
2885particles inside the selected crossing; seed5 c_f10.0179451332,
L_proxy6.2966399752,1340particles. measurement_005_seven passes5controls and
reproduces all prior five results exactly. All seven primary flags are ok;
this does not establish robust derived L or a corrected linked-T pass. The
first-crossing/binning instability already demonstrated is retained. No
completion-order ensemble summary or alternative estimator is substituted.


Seed4 completion: final snapshot/done/log copies pass72 total completion
checks across eight seeds. Unchanged primary c_f14.4959394876,
L_proxy9.1112209981,995particles inside the selected first crossing;1180steps.
measurement_006_eight passes5controls and reproduces all prior seven results
exactly. Only seed6 remains pending. Eight ok flags or individual high/near4
proxies establish no robust derivedL, ensemble result or corrected linked-T
pass. The first-crossing/binning instability and original fixed-T grade scope
remain explicit; no alternate estimator or fitted number was introduced.
