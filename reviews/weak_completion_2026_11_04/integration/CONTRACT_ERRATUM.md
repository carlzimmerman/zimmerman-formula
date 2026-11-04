# Original joint-run contract description correction

The immutable `contract_joint.json` and `run_joint001/manifest.json` inherited
three stale descriptions from the 25-group energy template. The actual command
and pinned source use the fresh **30-group** initial vector packet, not
`energy/run_fresh_coarse002`; the maximum step is 0.0001, not the unused
`dN` list; and this is a new vector history. The result correctly records its
ancestry, phase count, step size, complete 1200-coordinate state and scope.
All historical bytes are preserved. Subsequent segment contracts correct the
descriptions before execution. This changes no numerical result.
