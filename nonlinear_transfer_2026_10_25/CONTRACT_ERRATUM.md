# Contract inheritance correction

The development contracts from NT-FULL-AUDIT through the first adaptive runs
have correct finite-carrier assertion strings and pinned full.py, but retain
an obsolete conventions sentence from the initial adiabatic audit describing
a minimized midpoint carrier. That sentence is incorrect for full.py.

The actual finite-carrier action and solver are specified in ACTION.md. Do not
reinterpret the obsolete sentence as evidence that full.py used minimization:
it solves the momentum root and retains p_alpha. No completed contract or run
was overwritten. Further checked contracts replace the conventions explicitly,
and the finite-carrier derivative audit is repeated under a corrected contract.
The earlier runs remain development evidence with this scope correction, not
the final verification records for the corrected assertion.

NT-01 failed before dynamics on a test-array broadcasting error, corrected in
the new NT-02 script. Initial split-step adiabatic pilots hit carrier KKT solve
failures. Those are not successful formation runs and are not merged with the
finite-carrier results. Their scripts, records and outputs remain immutable.
