# Frozen CT09 kinetic handoff

Base contract remains `../CONTRACT.md`, Git checkpoint
`285353a57bc1c21662c5565830bbc97ac5b0f7f9`; use exact `BASE_INPUTS.json` hashes
and each manifest for actual ancestry. Work is confined to this package.

Preferred state: `run_hybrid_bw_001/result.json`, `case.state` and `case.final_N`.
It is a 24-bulk-cell NWA-early/static-BW-late hybrid, mu=2e6 GeV, matched leading
pole potential, Tc=1e-6. Full numeric state, distributions, action, radiation,
work and event count are retained. All 42 manifests validate, including ten
unsuccessful records; 32 have runner status `completed`. Two completed old
phase-splitter records are nevertheless excluded for a code error. See
`RUN_INDEX.json`, `VALIDATION.json` and `inputs_historical/archive_map.json`.

Established only within this closure: coupled charge-state and momentum
feedback can enter the local cold vacuum; the selected fixed-pole channel
leaves an excessive charged yield even after the coordinator's most generous
all-future peak-rate envelope. The named direct conversion source supplies
about .3763% of the reference photino DM density under the approximate U1
branch 1/6. Neither statement is a whole-model no-go or a physical complete
production history.

The next unresolved physical implication is the identification of the
instantaneous, empty-daughter local collision generator with the real
oscillating-background kinetic system. Three distinct continuations are:

1. Time-dependent narrow resonance: use the saved orbit and charged momentum
   distribution to compute pair dephasing/correlation and a neutral parent
   density matrix with its finite decay hazard. Compare one explicitly resolved
   crossing/orbit with the static coherent API. A long parent lifetime alone
   neither proves nor disproves Markov locality. Include energy/charge and
   varying daughter forces; do not rename every neutral final state radiation.
2. Statistical/cascade closure: evolve the actual gaugino occupation and
   inverse conversions with Pauli/Bose factors, plus charged scalar/fermion
   momentum maps and massive neutral endpoints. The independent photino
   phase-space result makes an empty daughter bath an untenable preserved
   assumption for a physical history. Preserve distinct U1 and nonabelian
   neutral distributions.
3. Matched spectrum/potential: match pole masses and the retained finite
   potential at the same order before using sub-linewidth vacuum placement.
   The finite gravity packet and leading tree+CW global action differ in their
   cold minima by enough to change whether the scalar channel is open.

Numerical continuation should preserve source bytes before revision and use
new bounded v2 jobs, wall<=240s, CPU<=235s, one numerical thread, measured RSS,
no address-space/affinity cap. The actual full initial-to-late BW job timed out;
only the explicit hybrid completed. Do not relabel it a full BW history.
Use `resume_bw.py`'s durable state pattern for future bounded work. No extra
scan or precision chase is needed for this frozen checkpoint.
