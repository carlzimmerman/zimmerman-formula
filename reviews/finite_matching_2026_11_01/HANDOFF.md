# TP03 handoff

Authorized work: missing finite two-loop diagrams and kinetic/current
matching in weak coupling; determine their effect on the pressure verdict.
Initial shared HEAD 7b1880de2caded85da4b8c34d84b5dc6c005650e. Read README.md.
No previous checkpoint is rewritten. Actual versions are pinned by manifests.

Reached: all ten finite two-loop vacuum graph classes and exact-splitting
one-loop angular phase current, including scalar/vector mixing; normal
heavy vacuum/current/omega^4 response counted once; fixed-X reduced scale
checks; 48 native-phase pressure cases with repeated roots. At e=.01/.03
the boundary is X/Xmin=1.21394372/1.21818639 and endpoint Pex/epsilonex is
.61414732/.60916684. The later negative sound speed remains. Full vacuum
and phase-current finite matching no longer occupy the same uncomputed
status as in TP02. Radial and infrared matching remain distinct.

Useful next dependencies, without assuming a rescue:

1. Derive anomalous R-charge evolution and nonperturbative unbroken-gauge
   effects. The phase state has no protected exact quantum number or
   selected density. A chosen circular occupation is not cosmological
   state selection. Local one-loop current matching does not solve this.
2. For an actual cold massive-mode route, compute gauge/IR-safe pole
   thresholds, allowed decays and collisions, and the population/lifetime.
   The previously noted lighter scalar plus Goldstino channel is not
   closed by the phase-current calculation. Preserve the full rest-mass
   source in any gas pressure law.
3. If a finite-frequency spectrum or inhomogeneous evolution is needed,
   match the radial kinetic coefficient and the higher-derivative/nonlocal
   response of light modes. The thermodynamic IR pressure sign obtained
   here uses the angular/current action; it is not a matched radial gap.
4. A rigorous finite-coupling persistence claim still requires a remainder
   bound or additional higher-order control. The present corrected action
   is solved algebraically; this is not a bound on the extra orders thereby
   resummed. Keep the fixed-Q trial prescription distinct from TP02 running
   prescriptions and never add its CS logs twice to explicit graphs.

Reproduce the exact commands and inputs from each v2 manifest. Use fresh
output directories, one thread and bounded minute-scale runs. The numerical
subroutes have independent source/derivation reviews and failed records.
Do not overwrite source pins or source snapshots when another session moves
HEAD. No commits, external jobs or queue modifications were performed here.
