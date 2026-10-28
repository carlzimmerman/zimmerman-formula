# CSM1 MW and dwarf regrade

This scope reconstructs BS1's primary Local Group basin and regrades the MW and dwarfs with the corrected mass-dependent parent switch. It introduces no fitted number. The primary LG mass is **log10(M/Msun)=12.392490566497107**, the sum of member inferred M200 values. The full member/mass record, fitted R0, and field distances equal BS1's committed JSON exactly. The previously quoted 12.345676973 belongs to the excluded summed-baryon variant.

Baseline controls reproduce BS1 primary L 4/T12.3: five dwarf-class medians/Z, all 13 field residuals and S1-S3, MW box counts/classes, and McMillan observables, on both footings. Original GD2/GD1 controls also pass. No old lane is written. The hook records reads through both ordinary Python opens and NumPy/import-level opens and refuses historical writes.

The MW parent selector uses HO2's native log-column interpolation at fixed LG mass, separately for A/B and each footing. Its own halo uses the same S9/column callable at its own mass. Its native rounded floors are 106.879 and 129.165 Msun/pc². X51 retains its separate atomic8 cooling-floor dwarf profile and exact floor units. Dwarf flags use background A at fixed LG mass for satellites/inside-field; outside-field flags use the original BS1 own-mass fallback. Diagnostics use direct column/floor inequalities, never a shared scalar threshold.

| L | MW A, either footing | Cells passing BS1 V+K | Field S1/S2/S3, both footings |
|---|---|---:|---|
|3.75|V+K ONLY|10|pass/pass/fail|
|3.9|FEASIBLE (WIDE PRIORS ONLY)|12|pass/pass/fail|
|4.0|FEASIBLE (WIDE PRIORS ONLY)|13|pass/pass/fail|

These MW classifications include the original outer-rotation L3 line. BS1's narrower MW criterion only requires L1+L2a+L2b, and all three levels satisfy that criterion. The fixed McMillan baryonic point fails L1 and L3 for all three L values. At L 3.75/3.9/4 its canonicalA circular speeds are 197.9400478555/199.2210284137/200.0787168966 km/s and Kz/(2piG)=66.6895191272/67.0008896756/67.2104401277 Msun/pc². Full background B rows and every grid cell are retained in JSON.

Five dwarf-class (median,Z) pairs are identical across the three L values because all their selected branch flags remain identical:

| Class | canonical | alt |
|---|---|---|
|MW ultra-faint|(-0.217722406378,-1.90820639960)|(-0.315631435486,-2.77499639049)|
|bright M31|(-0.0803005537290,-0.726210277362)|(-0.0959461830121,-0.871556691210)|
|M31 others|(0.0285232256434,0.0875205788277)|(-0.0345989385589,-0.104290845173)|
|MW classical|(0.0166050526095,0.243023924251)|(-0.0283219620939,-0.416795647931)|
|LG field|(0.000567192779128,0.00942167839095)|(-0.0359487626043,-0.592478776674)|

Canonical passes all five class criteria; alt fails the ultra-faint class. The 13-object field grade fails S3: IC 1613 is Z=-7.616762416307369 canonical and -8.439534052941923 alt; familywise S3 p = 3.381527127563143e-13/4.141867253829678e-16. Leo T and Phoenix remain individually consistent. The satellite scatter rules and every field residual are reported without loosening cuts.

Actual baryonic fields are solved once in each fresh process; only their observables are cached between L cells. A replay at L 4 exactly reproduces the fresh baseline MW results. Two fresh-process normal outputs are compared byte for byte. The source-flag mutation inverts corrected MW/dwarf decisions and must fail the independent scalar selector check with exit 1. Scientific grade failure is separate from implementation-control success.

Run from the repository root, using the fixed v4 script:

```bash
env PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python3 -I rebuild_2026_10_22/CSM1_consistent_core_switch/heldout/run_heldout_v4.py --output rebuild_2026_10_22/CSM1_consistent_core_switch/heldout/NEW_RUN
```

For the deliberately failing twin, use `run_mutation.py` in place of `run_heldout_v4.py` and add `--mutate`. The mutation wrapper clears argv only while loading the original X51 profile, keeping its independent historical cooling-mu mutation disabled; corrected selector flags are then inverted at their source. `nice -n 15` was attempted, but macOS returned `setpriority: Operation not permitted`; subsequent commands use the permitted priority. All numerical thread variables are 1. RSS is observed rather than enforced through unsupported macOS RLIMIT_AS. Command/version/input/output hashes and resources reside in each run manifest and resources file.

Scope: calibration owner supplies SPARC/groups/clusters/lensing. HO1 hot-gas and HO2 SLUGGS failures remain unchanged and are not rerun here. The data were already known; these are corrected finite regrades, not blind predictions. Kappa=1/2 remains fitted, basin selection remains a posit, and the empirical/theoretical framework is not closed.

Development evidence is retained: run 001 completed science but failed manifest-path recording; run 002/003 had a declared-result metadata omission; run 004 has a valid manifest, and run 005 sharpened floor diagnostics/independent scalar auditing. Primary evidence is run 006_final (7/7 controls), fresh-process run 007_repeat (byte-identical science JSON), and run 009_MUTATE (baseline passes, all 882 source flags per L inverted and detected, expected exit 1). Their manifests validate with statuses completed/completed/failed, respectively. Run 008_MUTATE stopped at baseline because the historical X51 --mutate argument leaked into its cooling-mu control; the isolated wrapper corrects that control-harness issue. No earlier record is silently overwritten.

Authoritative scientific result SHA256: `224a894992f9d48b3113b465d9eb34352ccdd9b40e01ccd40cebd7cc1c5c6c66`. Normal run 006 uses 214 observed input hashes and peaks at 0.625082368 GB in 19.1708 seconds. The separate feasibility review audited all 2646 normal selector logs with zero disagreements. `HANDOFF.json` contains exact summaries, paths and hashes; `LEDGER.jsonl` records checkpoints and retained development failures.

The gate-confirmed sole-L challenge now uses **L=2.5090648745652686**, defined by the actual full-precision X43 canonical A floor at logM12.3. Initial run010 at2.5090595510216196 is retained as displayed-a0 precision-error history. The definition-corrected run011 and independent fresh-process run012 are byte-identical, SHA256 `b693dda108714a66fa27121fbc5e6245e7909ffaacf4f0586e5167d108c88fa2`; both manifests validate completed with7/7 controls. This corrects the precision of one frozen target and adds no new target or fit.

At that challenge level, canonical A remains V+K ONLY (8 cells pass BS1's V+K condition; no cell passes all four lines), while canonical B and both alt MW branches are law and INFEASIBLE. Canonical dwarf classes remain unchanged. Alt switches to the law and fails MW ultra-faint Z=+4.874405424798004 and M31 others Z=+2.1173300753989723. Field S3 fails on both footings. The native MW canonical A diagnostic crossing is12.29998124669089 rather than exactly12.3 because its own table and floor representation remain native; every actual decision uses its direct column comparison.

The separately requested necessary MW lower bound from maximum radial speed over all175 box cells is **vacuous: L>=0 only**. The actual L1 speed interval is219.9–238.3 km/s; forcing the floor halo on already gives max Vc=285.27749701237315 canonical and287.30009642213355 alt at L=0. Thus that particular necessary relaxation has no positive root. It does not say any L=0 cell satisfies the full MW constraints. Baryonic observables reconstructed from validated baseline totals replay all registered speeds to5.684341886080802e-14 km/s; all175 cells have R0=8.122 kpc below R200 (minimum182.39925176797254 kpc).

The exact-arithmetic compact-Burkert monotonicity argument, including Sigma floor and saturation, is in `MW_BURKERT_MONOTONICITY.md`; independent review and its essential halo-branch restriction are in `MW_MONOTONICITY_AUDIT.md`. The full switched model is not claimed monotone. `mw_bound_001/manifest.json` validates completed. This scalar constraint is not an extra model candidate or fit.
