# XH1_xcop_native_rule: route E's current rule FAILS X-COP's hydrostatic masses at both f★, too heavy from 0.2 to 0.7 R500

Criteria: `FROZEN_CRITERIA.md` (530debe21b), committed alone before any script or number. Script `xh1_xcop.py`, tail `xh1_tail.py`. Numbers: `xh1.out`, `xh1_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen verdict: X-COP FAIL, both f★, both footings (HO1's line: |mean Δ| ≤ 0.05, rms ≤ 0.10)
Δ = log₁₀[M_HSE/(M_b + M_h)], so Δ > 0 means the model is too light. 35 points, 7 clusters. No cluster saturated, none on the floor.

| Rule | mean | rms | x 0.1 | 0.2 | 0.3 | 0.5 | 0.7 |
|---|---|---|---|---|---|---|---|
| **FC1, f★ 0.034** | **−0.073** | **0.139** | +0.115 | −0.064 | −0.119 | −0.142 | −0.157 |
| **FC1, f★ 0.0615** | **−0.077** | **0.143** | +0.115 | −0.066 | −0.123 | −0.148 | −0.165 |
| HO1's CL2 picture | −0.002 | 0.126 | +0.193 | +0.029 | −0.034 | −0.082 | −0.117 |

Comparators from CS2: OS1 rms 0.124 canonical, 0.092 alt; CS2 law 0.205. Both fail reasons are real here: the mean is too heavy and the shape is wrong. Per cluster, mean Δ runs from −0.126 (ZW1215) to +0.024 (A644). S is 582–711 M☉/pc², r₀ 257–360 kpc.

## What it does and doesn't say about the shear
My reason for running this was that G-IN-Mall, which decides the cluster grade, might be a bad shear band. Half of that survives.

- **Frozen band read: SHEAR BAND OUTLIER.** In 0.15–0.46 Mpc, X-COP has the model over by × 1.23 (f★ 0.034, 14 points) and × 1.24 (f★ 0.0615). G-IN-Mall has it over by × 1.90 and × 1.92. That band also fails its cross-shear null (IC1 D2). So the size of G-IN-Mall's excess is out of line with hydrostatic masses, which is a conflict and not proof of which is biased. X-COP is 7 massive clusters; eRASS1 is 326 lighter ones, in 3D mass against projected shear.
- **But the over-prediction itself is real.** X-COP's × 1.3–1.44 at 0.3–0.7 R500 matches the shear keys in MID and OUTER (G-MID-T3 × 1.20, G-OUT-all × 1.29). Two independent data sets say the rule is too heavy. I can't blame the band for that.
- **A hydrostatic bias can't carry it.** XRISM's non-thermal pressure is a few percent in the cores (0.013 dex for 3 %), and Eckert+19's X-COP median is about 6 % at R500 (0.027 dex). The miss is 0.12–0.16 dex.
- **The core is too light at x 0.1 (+0.115).** A smooth core is short of mass there, and the zooms make cusps (X81). This is the shape half of the fail.

## What-ifs (η at 10¹³, 10¹⁴ × g; reported, not graded)
| g | f★ | mean | rms | x 0.1 | x 0.7 | band model/data |
|---|---|---|---|---|---|---|
| 0.90 | 0.034 | −0.038 | 0.134 | +0.169 | −0.140 | 1.122 |
| 1.1144 | 0.034 | −0.109 | 0.154 | +0.058 | −0.174 | 1.357 |
| 0.90 | 0.0615 | −0.041 | 0.137 | +0.170 | −0.147 | 1.129 |
| 1.1144 | 0.0615 | −0.113 | 0.158 | +0.059 | −0.182 | 1.368 |

Lowering S fixes the mean and not the rms, which stays above 0.10.

## What it led to
The per-cluster table shows log M 15.31–15.69 as S's mass argument: the whole mass inside r_ta, about 3× M200. `../MA1_cluster_mass_argument/` follows that up.

## Limits
7 clusters. M_FORW only. Gas tail slope from X-COP's own gas, used by the rule as elsewhere. The cluster η is still ng 48; `xh1_xcop.py --A4` reruns this once CE1's A4 tables exist.

## Checks
K0 FC1's cluster predictions |d| 0; K1 CS2's law read |d| 0; K2 1.7e-14; K3 9.5e-8; K4 2.2e-16; RSS 0.66 GB: all pass. MUTATE S × 2 moves the mean by −0.213: bites.
