# Versioned tile3 force-candidate appendix

`run_tile3_refined.py` and `launch_tile3_refined.py` are new mechanical copies
of the frozen fixed-common-state wrapper and launcher. They add the explicitly
named `tile3` backend and its separate source/library input closure. The
generic frozen `refined_core.py`, H4 map, common saved physical arrays, CTMC,
Plummer law, fixed analytic host, all-particle retention, profiles, remnant
diagnostics and energy/vector-angular-momentum receipts are unchanged.

Tile3 uses a symmetric FP32 product of the two source masses to accumulate
pair forces and pair potential energies. Returning acceleration and specific
potential divides by each particle's true binary64 mass on the CPU. Four
FP32 partial chains and a balanced reduction precede each DS tile merge.
Its raw coordinate representation, precision and selected binary hash are
reported by `tile3_gravity.backend_metadata()`. Select the separately pinned
library through `TILE3_GRAVITY_LIBRARY`. This does not overwrite the tile or
tile2 implementations.

The empirical candidate budget is unchanged: force relative L2 below `5e-7`,
per-particle relative maximum below `2e-6`, maximum relative potential error
and relative total potential-energy error below `5e-7`. The full DS reference
and, for supplied total N at most 32768, native CPU reference are checked at
calls 1, 2, 100, 1000, 6000, 30000, 60000, 120000 and 240000. Maximum absolute
force error normalized by the maximum reference force is also recorded.
No DS `1e-11` admission or native binary64 pair arithmetic is inherited.

Symmetric force accumulation addresses one source of unequal-and-opposite
rounding error. It does not establish exact torque, a precise Hamiltonian
gradient, or acceptable long-time evolution. The existing energy threshold
and normalized vector-J/momentum gates remain unchanged, including the
`1e-7` vector-J gate that the longer tile2 host run exceeded. A fresh bounded
long-host admission and matched profile/timestep checks are required before
physical interpretation. No density core is inserted or assumed.

The launcher freezes the selected tile3 sources and actual binary, common
initial bytes and metadata, CPU/DS references, this appendix and its unchanged
predecessor appendix, the frozen core, CTMC, old diagnostic sources and cold
master equations. Existing case directories and contracts cannot be reused.
No production launch is authorized by unit-test completion alone; the parent
reviews the candidate and bounded admission results.
