from adaptive_physical_checked import main
main({'case': 'boundary_minus', 'dt_Myr': 0.005, 'duration_Myr': 100.0, 'wall_seconds': 240, 'coupling': True, 'step_energy_tolerance': 1e-09, 'energy_roundoff_floor': 5e-13, 'wave_R_kpc': 10000.0, 'wave_h_kpc': 2.0, 'equilibrium': 'nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz'})
