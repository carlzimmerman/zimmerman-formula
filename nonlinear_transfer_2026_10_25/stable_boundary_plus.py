from adaptive_stable import main
main({'case': 'boundary_plus', 'dt_Myr': 0.005, 'duration_Myr': 20.0, 'wall_seconds': 240, 'step_energy_tolerance': 1e-09, 'equilibrium': 'nonlinear_transfer_2026_10_25/run_equilibrium_stable/state.npz'})
