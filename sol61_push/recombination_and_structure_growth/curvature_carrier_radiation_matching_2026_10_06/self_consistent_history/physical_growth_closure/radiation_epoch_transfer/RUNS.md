# Authoritative bounded runs

REPORT is outside execution_artifacts; code, source registry, provenance and dependency closure are pinned in the standard manifests.

- main_a: 46/46; manifest validation return 0. Failed assertions: .

  100 DOP853: nfev=3596, total_rhs_calls=3596, Fmin=0.03454566196, Cmax=2.5589e-08, charge=3.7915e-09, source-decomposition defect=8.5117e-08.

  100 Radau: nfev=45708, total_rhs_calls=53580, Fmin=0.03454565908, Cmax=5.003e-09, charge=2.1357e-10, source-decomposition defect=1.2027e-07.

  1000 DOP853: nfev=9968, total_rhs_calls=9968, Fmin=0.08313458678, Cmax=4.3265e-08, charge=1.5955e-08, source-decomposition defect=6.1493e-06.

  1000 Radau: nfev=130780, total_rhs_calls=149180, Fmin=0.08313456983, Cmax=5.841e-09, charge=5.3479e-10, source-decomposition defect=1.6273e-06.

  Independent solver common-vector errors: [2.1705921448360107e-07, 6.682633105782274e-07].

- control_trace_a: 38/46; manifest validation return 0. Failed assertions: Hamiltonian_100_DOP853, actual_source_decomposition_100_DOP853, Hamiltonian_100_Radau, actual_source_decomposition_100_Radau, Hamiltonian_1000_DOP853, actual_source_decomposition_1000_DOP853, Hamiltonian_1000_Radau, actual_source_decomposition_1000_Radau.

- control_source_a: 42/46; manifest validation return 0. Failed assertions: actual_source_decomposition_100_DOP853, actual_source_decomposition_100_Radau, actual_source_decomposition_1000_DOP853, actual_source_decomposition_1000_Radau.


Historical preflight 37/38 and preflight_b 45/46 have the old 60000 nfev cap failure and are preserved with their exact scripts; neither supplies authoritative success. Explicit-Jacobian final scientific inputs were frozen before the larger declared-resource run.
