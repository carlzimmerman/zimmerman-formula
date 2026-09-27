# CD26-2 lapse construction evidence

All six accepted manifests were validated with the installed mathbox
`validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula`.
All returned exit 0, including current input and output hash checks. Execution
success is distinct from the interpretations and scope in `REPORT.md`.

| Accepted run | Exact checks / declarations | Runtime | Commit recorded |
|---|---:|---:|---|
| `run_lapse_004` | 27 passing checks | 3.147396 s | `9092fc0fd02b904e87c708971335cd63adb18151` |
| `run_ppn_gyro_001` | 16 passing checks | 1.927643 s | `3151d88f29f751df4f599d489f8dac1cbbb77774` |
| `run_integrated_001` | 13 passing checks | 1.486159 s | `9092fc0fd02b904e87c708971335cd63adb18151` |
| `run_offshell_001` | 22 passing checks | 1.051578 s | `9092fc0fd02b904e87c708971335cd63adb18151` |
| `run_lean_001` | 11 compiled declarations | 118.091823 s | `9092fc0fd02b904e87c708971335cd63adb18151` |
| `run_spectral_reduction_002` | 37 passing checks | 1.306546 s | `7daaa5426076a2d78a50f3316007c7093255ce9a` |

Each symbolic count includes its explicitly named negative controls; counts do
not represent independent physical requirements closed. Symbolic software was
Python 3.9.6 and SymPy 1.14.0. Exact command arrays, resource caps, input hashes,
dirty state, full results, and stdout/stderr reside in each run directory.
No random samples were used.

The final Lean compile used Lean 4.34.0-rc2 and the pinned local mathlib
`lake-manifest.json`. It exited 0 without warnings or errors. All eleven
declarations use only `propext`, `Classical.choice`, and `Quot.sound`.

- Lean source SHA256: `28321e322c4ad0c0e98c966bf1885566fcd685eebde38f5c1bda7fba1c900f8c`
- Lean results SHA256: `db9e07a97d3988f0c8c693e7701a7a5e7b0bc758c2d78c7f15accda52606cc24`
- Lean stdout SHA256: `7d4027baa73fe60a214857ecaf3f087fa4e841e07a941af79d283d7539a409d9`

The Lean statements concern the contact-locus polynomial identity, scalar
speed sign, positive-cell bounds, the supplied PPN/speed algebra, and the
nonvanishing gyro quartic coefficient. They do not certify a covariant action
variation, a full Dirac count, a continuum causal-support theorem, a global
well-posedness theorem, or an empirical PPN pass.

Scientific result SHA256 values:

- `run_lapse_004/results.json`: `4ebc20cf57fdee7dad334f7c9bc012246d1843d0f9965b7153a7ad8b168b55e5`
- `run_ppn_gyro_001/results.json`: `9b8ce21d0c8ff9c2d6f4d3b164c083da7cd86cd685879586dd10461000230907`
- `run_integrated_001/results.json`: `aa8d1ce8e034bc5695748f1f4775116854c62164c9de6a3e0351f2189ae56c41`
- `run_offshell_001/results.json`: `350b6b056d947ed90e073462795da8372db4ac60ef8dce72747bd6a85e4da086`
- `run_spectral_reduction_002/results.json`: `68b0ab20c234b30657665423dda5f882f23314e08bdc5381bbae3072cf92ad5d`

The sixth run is a separately requested, bounded audit of normalized spectral
lapse reduction. Its continuum conditional reasoning and additional limits
are in `SPECTRAL_REDUCTION_AUDIT.md`; it adds no Lean theorem or full-theory
constraint certification.

## Retained incomplete attempts

`run_lapse_001` and `run_lapse_002` reached the CPU cap; `run_lapse_003`
reached its wall-clock cap. They produced no scientific result artifact and
are not accepted. The second and third stdout logs show all action, source,
and pole residuals passed before contact-polynomial expression expansion
exhausted the budget. Rewriting that division in independent contraction
variables made `run_lapse_004` complete in 3.15 s without changing the assertion.

The exact original inputs are preserved as `archive/check_lapse_run001.py`,
`archive/check_lapse_run002.py`, and `archive/check_lapse_run003.py`; their
hashes match the respective failed manifests. Old failed manifests naturally
do not certify freshness of the now-revised live `check_lapse.py`.

Development Lean compiles exposed an insufficient denominator rewrite; the
first source is retained as `archive/PushLapse_initial_compile.lean`. Only the
final clean bounded run is accepted. No proof admission or custom axiom is
present in the accepted source.

The first spectral-reduction run failed because the default symbolic
simplifier left an exact rotated quadratic-form identity unreduced. Expanding
angle sums and their products before trigonometric reduction resolved it,
after an independent minimal rotation check. The source is preserved as
`archive/check_spectral_reduction_run001.py` and matches the failed manifest.
Only `run_spectral_reduction_002` is accepted.

The current spec was independently hashed as
`851e44ab8f8a67f2779f16aa01945b149e62d30a7292b73e7ca2419c2b4e0390` at commit
`9092fc0fd02b904e87c708971335cd63adb18151`. Its operative `nu_mono`/criterion-B
revision is distinct from the pinned exact-exponential research branch here.
