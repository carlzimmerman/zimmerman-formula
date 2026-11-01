# Finite-relaxation waterbag comparator roots

Freeze before execution. At each e=.01,.03,.05,.1 use central rg2 potential
plus the finite normal-relaxation potential from the full spectral tadpoles.
This uses the old stipulated waterbag source and tests the *vacuum* matching
piece only; its microscopic occupied-state coupling is not claimed derived.
The native-phase complete occupied square is delegated to matter_coupling/.

Find the nearby Us=0 minimum in .7..1.3 TP01minimum and Uss-3Us=0 in
1.01..1.6 times that minimum. Use 5point logstencil h=.005, independent
h=.01 at both roots and X/Xmin=1.2. Float64 spectralgradient addition is
not differentiated by mp.diff; direct50digit derivatives of the baseline
plus a separate h=.0025 stencil of deltaU form an independent composed
check at the witness. Numerical errors are reported relative to resolved
Us/Uss scales, not mistaken for a bound on missing finite2loop graphs.

Report root/density shifts, Us,Wss and pressure witness signs, geometric
angular correction and normal relative shifts. Retain missingbracket
outcomes. One thread,180wall/170CPU seconds, measured RSS, v2 provenance.
