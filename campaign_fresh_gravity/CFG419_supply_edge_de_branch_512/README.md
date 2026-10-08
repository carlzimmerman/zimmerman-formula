# CFG419: supply-edge confinement with a₀ tracking DESI dark energy. QUEUED after CFG416 (512³ canonical)
Criteria committed first. Launcher `cfg419_run_all.py` (uses CFG416's engine with branch DE).
Control passes: a0_code(1, 'DE') = a0_code(1, 'FLAT') (the branches differ only in a₀(a)).

## RESULT (512³, canonical): INDISTINGUISHABLE
- **DE:** σ₈ 1.0073, max|P−1| 0.0929, GROWTH OK by CFG361's cuts.
- **FLAT (CFG416 canonical):** σ₈ 1.0072, max|P−1| 0.0923.
- The difference is 0.0006, below the 0.01 needed for a preference, so growth cannot tell a₀ tracking DESI's dark energy from flat a₀. That matches CFG421 and CFG426.

The numbers were computed against CFG411's 512³ S0 (the same comparison as `cfg416_analysis.py`). The run finished overnight despite the pause note in CFG416.
