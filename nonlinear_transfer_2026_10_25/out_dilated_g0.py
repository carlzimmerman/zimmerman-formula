from adaptive_out import main
main({'case': 'dilated', 'dt_Myr': 0.005, 'duration_Myr': 100.0, 'wall_seconds': 240, 'coupling': False, 'step_energy_tolerance': 1e-09, 'energy_roundoff_floor': 5e-13, 'wave_R_kpc': 10000.0, 'equilibrium': 'nonlinear_transfer_2026_10_25/run_equilibrium_stable/state.npz'})
