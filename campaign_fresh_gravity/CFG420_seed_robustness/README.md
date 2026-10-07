# CFG420: seed robustness of the corrected-filter best rule (256³, canonical). ROBUST
Seeds 359 / 360 / 361, each against its own S0 (RES + corrected MIX-A, R_c = 3):

| seed | σ₈ | max\|P−1\| |
|---|---|---|
| 359 | 1.0193 | 0.153 |
| 360 | 1.0169 | 0.142 |
| 361 | 1.0181 | 0.139 |

- The spread in max|P−1| is 0.014, inside the frozen ≤ 0.03.
- The category is unchanged: TENSION in every seed.
- So the 256³ growth verdicts are not one-realisation flukes.
- Outputs are in ../_external_data/cfg411_work/; launcher `run_420_421.py`.
