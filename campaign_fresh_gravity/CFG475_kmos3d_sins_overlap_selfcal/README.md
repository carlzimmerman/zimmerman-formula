# CFG475: the 5 KMOS3D × SINS overlaps cannot support a self-calibrated a₀(z ≈ 2) test. NOT POSSIBLE (0/5 on every mandatory condition)

Criteria committed before the script. Script `cfg475_preflight.py`.

| condition | count |
|---|---|
| Q1: per-radius rotation spanning ≥ 6.4× in g_obs | 0 / 5 (the overlap table carries one SINS V_rot and one KMOS3D V22 per galaxy) |
| Q2: resolved gas surface-density profile (CO/HI) | 0 / 5 (no product under real_research/data names any overlap ID) |
| Q3: resolved stellar-mass profile | 0 / 5 |

- **Why Q2 is mandatory:** the neutrinos chat's CFG400–402 (Genzel+2017) showed that self-calibration frees only the normalisation. An assumed exponential baryon shape makes a₀ absorb the shape mismatch (a 3-dex spread; CFG400 INVALID). For the record, that chat's CFG402 found 5 of 6 Genzel discs consistent with DE-tracking and one ~2σ outlier (zC 406690). That is not this lane's result.
- **MUTATE** (Q2 forced true): still 0 qualifying, because Q1 and Q3 bind. As designed, the MUTATE shows the verdict does not rest on the gas condition alone, so it does not "fire". Disclosed.
- **What would make it runnable:** AO or JWST/NIRSpec inner kinematics plus deep outer curves plus resolved CO (ALMA) maps for the same z ≈ 2 discs. That is a fetch, and an observation where the data don't exist.
