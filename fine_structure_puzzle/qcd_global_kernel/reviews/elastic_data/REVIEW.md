# Independent final audit: finite lattice proton full-Born functional

**Claim:** the specified 19 printed proton Sachs pairs, fixed source mass 0.9389 GeV, supplied full angular Born kernel and normalization 1/(2π²) determine the declared finite z-trapezoid and conditional linear statistical ceiling.

**Primary verdict: computationally verified only in the stated range.** The finite assertion is independently reproduced and its implementation is independently checked. No blocking defect found in the frozen target. This is a bounded independent audit by a fresh subagent; it is not a new review of all preceding angular/tensor normalization. The starting kernel and global normalization are premises here. Exact audited revisions are the SHA-256 pins in AUDITED_PINS.json, unchanged at closeout.

## Independent construction and dependencies

PRETARGET.md was written before opening author implementation or results. It derives the quadratic Sachs coefficients directly from the supplied full-Born kernel, the finite trapezoid weights and both sensitivities, and proves the Cauchy-Schwarz covariance ceiling (including its sharpness for arbitrary PSD covariance with fixed diagonals). The normalization C was left unspecified there until reading the target definition.

Dependency graph: supplied full angular B and Sachs convention → independent quadratic coefficients → 19 authenticated local table rows at fixed mass → declared z weights and 1/(2π²) → finite functional and gradients → first-order covariance ceiling. Source scope/extraction conventions and absence of complete covariance are separate external leaves. No claim about full mass or alpha follows from this graph.

## Obligations

| Obligation | Status | Evidence |
|---|---|---|
| Sachs conversion and full-Born algebra | passed under supplied premise | PRETARGET.md and independent quadratic implementation |
| Nineteen nonzero points, proton columns, decimal error units | passed | all 19 exact TeX rows checked against INPUTS.json; all source pairs also inspected in PDF page26 image/text |
| Q²=0 magnetic NA excluded, no extrapolation | passed | source row explicitly checked; no synthetic endpoint |
| Quadrature in z rather than Q² | passed | independent Decimal sqrt(Q²)/(2m), 18 segments and nodal agreement, constant/linear invariants |
| Complete Born subtraction | passed | all pointwise decomposition identities and independent component sums |
| Analytic sensitivities | passed | independent quadratic derivatives, centered difference of exact quadratic, all 38 author gradient comparisons |
| Cauchy-Schwarz ceiling and scope | passed | fixed-input, linear fluctuation only; no independence or nonlinear standard deviation inferred |
| Source mass/current/flavor/extraction disclosure | passed | EM_PRD.tex passages at lines 71–74,116–138,271–285,323,552–565,617–620,625–645,658 and1225–1229 |
| Earlier tensor-angle derivation and overall normalization | out of scope | accepted supplied B and target 1/(2π²); no repeated angular controls |
| Continuum interpolation/tails, all-flavor/non-Born amplitudes, scale/systematic covariance, matching | out of scope | absent and explicitly excluded by target |
| Full proton mass response or alpha prediction | not established | target correctly makes no such claim |

The source explicitly states that strange loops are excluded (EM_PRD.tex line658). Nf=2+1+1 describes dynamical sea flavors, not included strange/charm current insertions. The empirical average physical nucleon mass sets the source scale at line272. Conserved connected current and the disconnected local-current ZV=.728(1) are imported. Plateau/two-state/summation analyses and jackknife point extraction are imported QCD evidence, so “no fit” is correctly limited to no new Q² ansatz or target fit. The public source archive and receipt do not supply a joint GE/GM configuration covariance in the inspected retained package; this audit did not undertake a new network search for one.

## Decisive finite result

Independent stdlib Decimal arithmetic (65 digits, no mpmath or author imports) gives:

    I_tab = 0.0025229926968935731491907210036788215182268912825652676792866517280
    elastic = 0.013772451332589844268839093381128997304273590918544722472280161724
    subtraction = -0.011249458635696271119648372377450175786046699635979454792993509997
    4 pi I_tab = 0.031704861286486197446936403709046176327855826655540338453309051923
    linearized covariance ceiling = 0.00070000972762248977729345200207751139664575246943070122645648865287

The maximum difference from author saved point kernels is 4.7392e-46; from sensitivities 3.9335e-48. These are compatible with author 45-significant-digit output rounding. Agreement beyond source precision is a reproducibility property, not physical accuracy.

## Provenance and bounded execution

All retained receipt hashes/byte sizes were checked. Archived table_ffs.tex and EM_PRD.tex bytes exactly match the extracted files. The PDF page26 image was visually inspected; pdftotext independently extracted page26 to page26.txt, matching the nineteen pairs and zero magnetic NA row. This authenticates linkage and transcription among the retained source artifacts; the original remote acquisition was not repeated in this bounded review.

The installed mathbox computation-audit runner executed independent_check.py with CONTRACT.json and all 18 declared inputs, wall 30s, CPU20s, logs1MiB and numerical thread cap1; no macOS RLIMIT_AS requested. run_001/manifest.json has status completed, valid under validate_manifest.py --root. The author run_001/manifest.json also validates against current inputs with status completed. Its source, code and results were not overwritten. The complete argv, observed versions, input hashes, timings and outputs are in the review v2 manifest.

Commands used for validation:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/reviews/elastic_data/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

No failed run, changed audit pin or unresolved numerical check occurred. Only files in reviews/elastic_data were authored by this reviewer. The strongest safe statement is an evaluated finite printed-point functional in the source light-current elastic sector, conditional on its empirical mass calibration and the supplied kernel convention. The exact remaining physical gap is the continuum/all-current/non-Born and matching completion plus missing covariance/systematics. No additional numerical bound extension is needed to validate this finite assertion.
