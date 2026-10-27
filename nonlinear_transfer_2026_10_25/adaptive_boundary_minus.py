from adaptive import main
main({'case': 'boundary_minus', 'dt_Myr': 0.005, 'duration_Myr': 40.0, 'wall_seconds': 240, 'coupling': True, 'step_energy_tolerance': 1e-09, 'equilibrium': 'nonlinear_transfer_2026_10_25/run_equilibrium/state.npz'})
