# CC11 energy package — completed finite benchmark

The matched population/action update closes the requested fresh-history
energy test in the finite 25-group model. At the shared warm target
N=.0021690179772784167, the independent energy-plus-FRW-work residual
is 3.59850e-7 of excitation for maximum dN=1e-4 and 1.16579e-7 for
maximum dN=5e-5. Both start from the original N=0 packet, with no inherited
energy-bad prefix or ledger reset. The old preferred residual was .238459.

The actual solution still has first-order time error: coarse-to-fine
action changes +4.8266%, U1 yield -1.7141%, charged yield -.03857%,
and U1 mean momentum -1.3100%. This package meets the finite energy
threshold; it does not certify 1% state accuracy, a full cosmological
history, or cold dark-matter viability.

| Quantity at target | Coarse | Fine |
| --- | ---: | ---: |
| Action J | 2.12177629116e-6 | 2.22418570094e-6 |
| Charged yield | 3.03795083398e-7 | 3.03677916615e-7 |
| U1 yield | 1.04744998330e-9 | 1.02949574134e-9 |
| Mean U1 p/mu | .00614833236 | .00606779127 |
| Orbital excitation /mu^4 | 1.95472429848e-12 | 2.04902834953e-12 |
| Independent work defect /excitation | 3.59850e-7 | 1.16579e-7 |

`run_benchmark001/result.json` and `history.csv` consolidate both completed
ancestries. Coarse ancestry is `run_fresh_coarse002` through `coarse006`;
fine is `run_fresh_fine002` through `fine007`. The nominal maximum steps are explicit in
the scripts, contracts and saved histories. Fresh histories use eight phase
nodes; momentum/phase continuum convergence is not established here.

The frozen reference API is `split_energy_v7.py`, documented in `API.md`.
It uses actual endpoint population increments to conserve the collision
Hamiltonian, a self-consistent midpoint-action/population stage, positive
log-number/vacancy Newton solves, and independent Simpson FRW work.
It accepts a common model/operator factory, including the coordinator's
30-group vector protocol, without a fixed species count. Vectors, decay
matching and the common final physics verdict are separate dependencies.

The local controls reproduce the old energy defect, diagnose the
moving-minimum concavity obstruction, test the corrected midpoint action,
compare Newton initial guesses, and check exactly empty species against a
90-digit toy reference. The small-J control uses an inherited harmonic
geometry approximation below J_initial*1e-7. This is not an action floor;
the completed warm histories never enter it. Nonharmonic cold accuracy
requires the separately owned `../cold_offsets/` oracle.

Optional Anderson geometry guesses in v8 reproduce the tested v7 roots
but have no demonstrated speed benefit. The reference histories stay on v7.
The requested population-midpoint alternative is **not promoted**:
`run_midpoint001` reaches its CPU cap before its first actual endpoint;
`run_midpoint002` completes the smaller one/two-substep cases but not the
four-substep case. A third partial-step residual exceeds its target. Thus
no second-order history or order estimate is established. The known
linear stiff-decay sign and inadmissible-root rejection controls pass.

Earlier failed numerical initializers, the old energy-surface midpoint,
and partial fresh001 attempts remain unchanged. They are numerical-route
records, not physical escape or exclusion. All terminal records and exact
source hashes are inventoried in `PROVENANCE.json`; no jobs remain active.
