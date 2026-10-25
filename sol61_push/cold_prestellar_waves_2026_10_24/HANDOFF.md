# Continue from CCT-007

Read RESULT.md and summary.json before relying on any plotted percentage. This is the NEW selectively coupled wave candidate, not v3s/AeST/SCT-M. No four-dwarf closure or protected stellar population was found.

New positive mechanism evidence: isolated, nonspherical finite-mode Schrodinger-Poisson collapse emits outgoing positive-energy mass and J. Source-free emission persists after repairing a failed coarse timestep. In the gas-cycle Sextans L=4 calculation, ~339 million Msun exits, carrying ~51% of initial aligned spin; retained mass ~570 million Msun. This is not angularly converged: L=2 changes the spin selectivity. Do not turn 51% into a physical prediction.

New negative result: the remnants are much too centrally concentrated and variable. Sextans has ~185 million Msun inside 486 pc in the L=4 run, versus ~9 million in the illustrative CCT-006 survey-fit profile. Its spherical-monopole actual-position Jeans diagnostic is grossly worse. Draco's long L=2 case also overconcentrates. Fornax/Leo I pilots flag large stellar gravity but their escape boundaries are not resolved; do not call them converged final controls.

Strict seed test: initial l=2,m=1 and l=2,m=2 only, no l=0, produces ~14.1 million Msun in l=0 but only ~2.9 million in the inner aperture. Most of the ~264-million-Msun inner aperture remains in other modes and is not low-spin. Initial J is tilted; its Jz sink ledger is not a full-vector ledger. The total retained ~422 million Msun is close to the target mass but does NOT fit the profile. This is a useful counterexample to total-mass closure.

All initial clouds are already bound. Capture from initially unbound incoming waves and cosmological supply remain unproved. The source gas is prescribed, with cold-field work accounted for but no physical gas-energy/reaction calculation. Eta, catchment and angular spectrum are benchmark choices, not deductions from Lambda. No binary collision term is used.

Next work should target selective radial partition and the initial angular/energy spectrum, not merely make cooling stronger. Require common physical parameters and a data-independent reason for different assembly histories. Before physical spin percentages: L>=6/angular convergence, simultaneous radial/dt/boundary controls, full vector-J fluxes and a remnant stability test. Before stars: pass the remnant profile and stationarity gate, then use a full nonspherical live stellar DF. Offline monopole circular cohorts here are only counterfactual stress diagnostics.

Reproduction examples (OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1):

    python3 sol61_push/cold_prestellar_waves_2026_10_24/wave_v2.py --galaxy Sextans --tag reproduce_L4 --nr 512 --lmax 4 --dt .04 --T 160 --rmax 28 --absorb 16
    python3 sol61_push/cold_prestellar_waves_2026_10_24/wave_controls.py --galaxy Sextans --tag reproduce_nogas --nr 512 --lmax 2 --dt .01 --T 160 --rmax 28 --absorb 16 --gas none
    python3 sol61_push/cold_prestellar_waves_2026_10_24/wave.py --galaxy Sextans --tag reproduce_boundary --nr 768 --lmax 2 --dt .02 --T 160 --rmax 40 --absorb 20 --gamma 1
    python3 sol61_push/cold_prestellar_waves_2026_10_24/wave_initial.py --galaxy Sextans --tag reproduce_noseed --nr 512 --lmax 2 --dt .02 --T 160 --rmax 28 --absorb 16 --gamma 1 --initial noseed
    python3 sol61_push/cold_prestellar_waves_2026_10_24/verify.py --tag sextans_L4
    python3 sol61_push/cold_prestellar_waves_2026_10_24/analyze.py
    python3 sol61_push/cold_prestellar_waves_2026_10_24/stars.py

Original log-grid pilots reproduce with wave_pilot.py. New tags preserve the existing auditable runs; do not overwrite them or any frozen criteria. No heavy jobs, monitors, external chats or remote repository state were changed.
