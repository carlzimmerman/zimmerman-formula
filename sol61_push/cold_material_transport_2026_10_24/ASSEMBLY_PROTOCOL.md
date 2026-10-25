# Exact saved assembly commands

All commands start with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_material_transport_2026_10_24/`. Use fresh --tag values for reproduction. All physical eta/supply/pulse defaults remain common; changes below are numerical controls.

- `assembly.py --galaxy Fornax --tag fornax_preflight_8192 --nr 8192 --lmax 4 --mmax 4 --T 0`
- `assembly_v2.py --galaxy Fornax --tag fornax_preflight_16384 --nr 16384 --lmax 4 --mmax 4 --T 0`
- `assembly_v2.py --galaxy 'Leo I' --tag leoi_preflight_4096 --nr 4096 --lmax 4 --mmax 4 --T 0`
- `assembly_v2.py --galaxy Fornax --tag fornax_matched_L8 --nr 16384 --lmax 8 --mmax 4 --T 130 --dt .01 --wall-seconds 600`
- `assembly_v2.py --galaxy 'Leo I' --tag leoi_matched_L8 --nr 4096 --lmax 8 --mmax 4 --T 130 --dt .01 --wall-seconds 600`
- The first larger-basis `assembly_bounded.py` runs use L12,M8 and the same nr/dt/T/wall, tags fornax_matched_L12M8/leoi_matched_L12M8. Their phases were regenerated; these are not exact initial-state comparisons.
- `assembly_matched.py --galaxy Fornax --tag fornax_fixed_initial_L12M8 --initial-from fornax_matched_L8 --nr 16384 --lmax 12 --mmax 8 --T 130 --dt .01 --wall-seconds 600`
- `assembly_matched.py --galaxy 'Leo I' --tag leoi_fixed_initial_L12M8 --initial-from leoi_matched_L8 --nr 4096 --lmax 12 --mmax 8 --T 130 --dt .01 --wall-seconds 600`

The --initial-from run copies the committed incoming wave into the larger basis, not an evolved endpoint. nr/r/w are checked, new modes are zero. The source-generated phase is replaced; logging takes the copied parent's kinetic reference. No target cold profile enters the evolution; target energies are diagnostics only.

The5% m/l-edge stop is checked at saved diagnostics, so the recorded first exceeded value may be larger than5%. All requested t130 runs stopped early and are scientifically inconclusive as late dwarf controls. Do not bypass the numerical stop to obtain a nominal pass. The1% initial kinetic test and M/E/J interpretation limits remain distinct from the5% emergency ledger stop inherited by the producer.

For source-free material replays see MATERIAL_PROTOCOL.md. Read the local-source warning before assigning physical meaning to labels. `analyze.py` reads canonical tags and writes the combined scoped summary; copy it to new output names for added evidence rather than overwriting the preserved final audit.

`record_runs.py` reconciles observed outputs into typed records, retaining its provenance limitations. Regenerating records or changing canonical source/results stales the final audit. Fresh phase-toy execution uses phase_benchmark_v2.py OUTPUT under phase_contract.json; the committed phase_benchmark_001 manifest records the actual bounded execution. It is a1D constant-carrier toy only.
