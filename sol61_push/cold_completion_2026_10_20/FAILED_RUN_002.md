# Failed uniform-phase run retained

run_002 is a valid provenance record with status `failed`, not evidence for a
physical phase. Its `liquid_phase.py` reduced grand potential omitted the
interaction `a*chi*I` while retaining it in the stationary field equation.
The solver consequently approached the trivial vacuum and the nonzero-state,
compressibility and derivative controls failed. Inspection of the exact
full potential isolated the mismatch. `liquid_phase_v2.py` restores that term
in both appearances and adds independent full-potential and field-derivative
controls. No threshold or physical parameter changed. The old script, contract
and failed output remain unchanged.
