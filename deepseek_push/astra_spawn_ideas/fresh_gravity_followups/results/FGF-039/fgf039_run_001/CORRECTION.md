# FGF039 independent-audit correction

The independent auditor /root/metric_intake identified a literal error in section4 of the initial frozen proof: “Equality in (8) forces psi=eta=0 and n=rho.” This is false as written. Taking psi=eta=0 and any admissible n differing from rho saturates inequality(8), with both sides equal to the generally positive cs²D(n|rho).

The corrected sentence is: “Zero excess energy Delta E=0 forces psi=eta=0 and n=rho.” Nonnegativity of the lower-bound terms proves this statement. No coefficient, energy inequality, entropy minimizer, L1 estimate or conditional scale barrier is changed. This correction preserves the intended strict-minimum conclusion while withdrawing the erroneous equality characterization.

The exact original bytes are retained as DERIVATION_PRE_CORRECTION.md, SHA256 71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3, and result_pre_correction.json, SHA256 c6a0f4289ea47959a825ad102f39d52e93aca78391269031c778a2b5a343b363. The historical result snapshot refers to the original candidate paths/hashes and is not a current-file validation record. The current result.json pins the corrected proof and the preserved revision artifacts. The auditor independently retained the same original proof hash in its own scope before this correction.

The correction was made after the independent proof audit and before orchestrator acceptance. It is openly attributed to the auditor; this was not a change discovered by a numerical computation.
