# Execution history

`run_builder/` failed while serializing NumPy boolean controls to JSON.
It produced no usable result and supports no mathematical pass. Its exact
pre-fix model.py, check_builder.py and contract are preserved under
inputs_initial/. The live code subsequently converts controls to native
bool and uses spectrum-relative zero clipping before its first successful
scientific execution. The original manifest and logs are unchanged; its
source paths are historical, not current-input validation targets.

`run_builder_verified/` completed all ten declared builder/vertex controls.
`run_basis/` completed all four basis/scaling/SUSY controls.
`run_gaps/` completed all four actual-gap/IR-bookkeeping controls.
These three v2 records validate their current inputs and output hashes.
No scientific acceptance threshold was changed in response to a failed
physical or mathematical gate.

No old TP01/TP02 input or Git staging/history was changed by this route.
Successful experiments use one numerical thread and supported CPU/wall/log
caps; measured RSS stayed below248MB. No unsupported memory/affinity cap
is claimed on this macOS platform.
