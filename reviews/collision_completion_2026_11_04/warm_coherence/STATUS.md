# Warm four-singlet coherence: sizable locally, small tested whole-current budget

The actual four parents are **S1_1**, mass sqrt(.006), degeneracy four.
S1_0 is the massless two-state modulus. All amplitudes were rebuilt at actual
warm x; no late-pole coefficients were transplanted.

At the two saved warm states, full four-state stationary P-mediated charged
currents are **35.6% and 60.6% lower** than the isotropic-parent closure.
Unequal diagonal populations alone leave substantial differences: coherent
currents are .7499 and .4336 of that control in the stated adapted basis.
This is a real internal-state/branching diagnostic, subject to the declared
frozen-bath Markov equation and bare degenerate Hamiltonian.

Its absolute importance in the tested whole25 warm operator is small.
After reconstructing every saved field phase and using exact angular
integration, the common-frame averaged-matrix correction triangle is only
**0.017315% and 0.019829%** of the whole phase-averaged charged-current
magnitude. The corresponding absolute budgets are 1.01804e-22 and
7.20809e-23 mu^4. These are conditional current bounds, not multipliers for
an uncomputed full history.

A stronger trace/operator-norm argument now bounds **any PSD periodic parent
response** of the declared frozen eight-phase coefficients, even with an
arbitrary Hermitian within-parent Hamiltonian: its correction relative to
the stored isotropic parent current is at most **0.54051% and 0.63955%** of
the whole saved charged-current magnitude. Phase-uniform bounds are
0.54219%/0.63963%; comparing coherent and isotropic periodic responses gives
0.58076%/0.63995%. These do not assume instantaneous steady state. The bound
uses max Tr(Gamma_gain)/min eig(D) at each parent momentum and positive phase
and momentum weights. It remains conditional on the frozen coefficient model;
it does not bound an unspecified changing bath or rematched channel rates.

The full phase-averaged charged-loss currents are +5.87956e-19 and
-3.63516e-19 mu^4; the latter is charged return at that frozen old snapshot.
The two input histories were bounded checkpoints with failed target-reaching
records. They are used as explicitly pinned finite occupation states, not
promoted to completed physical histories. Warm002 independent sub-ulp holes
are retained; warm001 only provides rounded Y.

Checks include actual-x full cubic/Yukawa construction, exact daughter-angle
availability/gain matrices at all 40 parent nodes, thermal detailed balance,
segmented GL32 agreement, independent scalar-parent normalization, actual
parent channel coverage at every phase, and a common parent projector to
below 1e-15. Current damping/H exceeds 6.8e4, but damping/omega can be .011;
instant-phase steady elimination is therefore not claimed. An expensive
many-momentum periodic matrix solve was deferred because the directly tested
absolute whole-current correction is below .02% and its rigorous periodic
trace envelope is below .64% in this declared model. The coordinator
authorized this local/current scope.

Reusable `matrix_api.py` exposes actual-x matrices, exact angular weighting,
current holes and the local density/current comparison. `run_phase001` also
saves common-frame averaged matrices and densities for later integration.
The exact first remaining bridge is phase-dependent coherent evolution with
daughter feedback and a matched dispersive medium Hamiltonian; this check
does not provide a complete Kadanoff-Baym or physical history theorem.
Broken-vector channels are excluded from this FFS/SSS matrix operator and
are not certified negligible; their warm thresholds can be open.

Four fresh v2 runs completed with all declared checks: local001 (4.77s,
517.44MB RSS), fraction001 (1.59s,513.52MB), phase001 (13.38s,636.27MB).
The trace envelope run took 13.13s with 557.45MB measured peak RSS.
All use one numerical thread and required wall/CPU caps. Commands, hashes,
statuses and validations are in `PROVENANCE.json`; proof/interpretation and
the checked primary matrix-kinetic source are in DERIVATION.md/SOURCES.md.
No prior scope or Git state was edited.
