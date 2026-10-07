# CFG425 FROZEN CRITERIA: confirm CFG424's zero-knob pass across seeds and at 512³
(committed before any run; owner 2026-10-07: "keep pushing the doors")

**Engine.** cfg424_pm.py, unchanged except for a seed environment option (CFG424_SEED, default 359; the default path is byte-for-byte the same physics). The mode is RC = 0, i.e. turnaround-catchment mass conservation, with f_ret ≡ 1.

**Runs.**
- R1, R2: 256³, canonical, seeds 360 and 361, against CFG420's same-seed S0 (cfg411_S0_..._seed360/361).
- R3: 512³, canonical, seed 359 (NSEED 512), against CFG411's 512³ S0. It starts after CFG416's 512³ jobs.

**Decision (CFG361 cuts).**
- **CONFIRMED:** R1, R2 and R3 are all GROWTH OK.
- **NOT CONFIRMED:** any of them is TENSION or FAIL. That run is reported, and CFG424 stays a single-seed 256³ result.
- If R3 has not run (machine time), the verdict is PROVISIONAL on R1 and R2.

**Caveats.** As for CFG424: bookkeeping cold fluid; κ, f_b and ρ_Λ not derived; the switch ε and the MIX-A filter inherited.
