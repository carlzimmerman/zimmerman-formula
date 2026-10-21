# Review and provenance

Base 02f2fae08; criteria-only commit 3a6b85cac. This goal turn makes
progress on protected auxiliary sectors. It does not complete or redefine
the original microscopic normalization goal.

Separate analytic agents developed the chiral fold/fermion calculation,
ordinary vector-auxiliary/Born-Infeld calculation and general auxiliary
criticality tests. The coordinator independently reconstructed the fold,
vacuum energy, local response and timelike physical-mode calculation;
checked the vector Schur relation and exact FI elimination; and corrected
an overbroad null-source-overlap claim using a higher-criticality example.
The frozen criterion required actual propagating-mode checks rather than
identifying an auxiliary Hessian sign with a ghost.

The vector-route author cross-audited the chiral, timelike and force
sections, including primary component coefficients. Reviewed report hash:
8ce795d8692174ecfb49558c97d73154669026dfa493c20fb0911c22e46f61d0.
Verdict: correct within the stated model and branch scope. The separate
auxiliary reviewer cross-audited vector Schur and Born-Infeld formulas;
the initial reviewed report hash was
7756b27fe96f5eb6d2bf4362e145ea4acb3a43bcc438a8d2c1d937b2d7b073d7.
It required distinguishing analytic elimination from C2 elimination.
Its final reread covered report hash
8ce795d8692174ecfb49558c97d73154669026dfa493c20fb0911c22e46f61d0.
The final report makes that distinction explicitly and spells out the
reviewed orientation grad phi parallel B parallel z with wavevector along
x. Parity evenness separates the photon polarizations. General mixed
polarizations remain outside that proof. These two final wording changes
were checked against the reviewer's stated mathematical conditions.
These are independent analytic checks of specified sections, not an
independent complete quantum or gravity proof.

The chiral-route agent implemented ChiralFold.lean. Its first development
compile passed with style warnings; both source snapshots and run outputs
are preserved. After warning removal, dev02 passed. The coordinator then
independently compiled the unchanged final source: final_fold passed in
4.074s with maximum recorded child RSS 873250816 bytes. There were no
admissions or custom axioms. The six critical theorem prints use only
subsets of the three permitted standard axioms.

Coordinator-authored true and false controls passed their intended tests
on their first compiles: final_normal exits 0; final_drop_timelike and
final_regular_fold each exit 1 with exactly the unsolved False goal.
They do not rely on missing imports or type failures. All compiles were
sequential, single-worker and memory capped; no source was changed after
the selected compile. Development records are history, not replacements
for the selected evidence.

The component-to-field dictionary and health interpretation are explicit
analytic leaves. Lean does not prove the source literature, full reduced
field equations, characteristic analysis, quantum consistency, gravitating
stress, force crossover or vacuum selection. The numerical 1/9 theorem
is explicitly nominal Taylor arithmetic and supplies no physical xi.
The report and source cards received a conservative mathematical
self-proofread for notation, hypotheses and claim calibration.
