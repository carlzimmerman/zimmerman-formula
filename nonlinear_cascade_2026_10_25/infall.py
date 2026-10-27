from spectral import main
main({'case': 'dilated', 'dt_Myr': 0.0025, 'duration_Myr': 30.0, 'wall_seconds': 240, 'step_energy_tolerance': 1e-09, 'energy_roundoff_floor': 5e-13, 'wave_R_kpc': 10000.0, 'wave_h_kpc': 2.0, 'equilibrium': 'nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz'})
