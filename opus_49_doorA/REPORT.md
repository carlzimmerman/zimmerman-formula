# opus_49 doorA -- PULSATIONAL CEILING FROM FIRST PRINCIPLES: VERDICT FAIL

2026-09-22. Lane: `pulsational_ceiling_lane.py` (own RK4 Lane-Emden n=3; numpy only).
Spine: `fable_independent_2026/lean_2026/I13_bhstar_pulsation.lean` (certified kernels and
scalar crossing).

## What was computed (all self-produced, no fitted numbers)

| quantity | value | note |
|---|---|---|
| xi1 (n=3 LE first zero) | 6.8968486 | lit 6.89684862 |
| u = -xi1^2 theta'(xi1) | 2.0182360 | framework Wave Q uses 2.01824 |
| **C_gr (n=3 homology, H=∫8GPmr+8πGPρr^4+G^2ρm^2 dr)** | **3.373422934888** | registered 3.373422935937; H·R/(18GM·W_gr)=1.124474311629 vs 1.124474311979 |
| beta(r) profile | **constant** (Eddington standard model): g(beta)=beta/(1-beta)^{1/4} const on the polytrope | exact, verified 1e-12 |
| kernel | 3Γ1-4 = beta(4-3beta)/(8-7beta) | Lean-certified |
| x* = W_beta/(C_gr W_gr) = kernel(beta_c)/C_gr | 1.3167e-4 (T pinned, beta_c=8.883e-4) | |
| quartic M_E (mu=0.59) | 51.765 Msun | register 51.8 (Lean I08) |
| **M_puls** (T_rec=5000K) | **6.56e7 Msun** (4.56e7 @6000K, 1.03e8 @4000K) | |

Mass conversion uses ONLY framework-registered relations: quartic (1-beta)/beta^4=(M/M_E)^2
(Wave Q/Lean I08, M_E=51.8) and the recombination-pinned L_Edd family
R=sqrt(GMc/(kappa sigma T^4)); kappa=0.34 (task-specified electron scattering).

## Verdict

**FAIL** against the registered pulsational ceiling [1e5, 1e6] Msun (LF cutoff 1e5.7):
the computed M_puls = 6.6e7 Msun lies ~1.9 dex ABOVE 1e6, and robustly so over the full
T_rec sweep 4000-6000 K ([4.6e7, 1.03e8] Msun).

## Exact obstruction

The certified scalar spine, evaluated on the n=3 polytrope + gas+radiation EOS, returns the
**global equilibrium-homologous** ceiling — M_puls lands inside the framework's own registered
global band [5.09e7, 1.21e8] Msun (Wave N) — and NOT the pulsational band. The pulsational
ceiling 1e5-1e6 is an **accreting, non-homologous, non-adiabatic MESA-type** number (Saio+24:
M_inst = 8e4 -> 1e6 Msun across accretion rates; fundamental homologous mode per Shibata+24).
The Laplacian input to this lane (n=3 homology, constant beta, recombination-pinned radius)
cannot produce it: the scalar crossing contains no accretion history, no thermal/quasi-static
evolution, and no finite-compactness GR remainder. This matches the i13 audit dependency item
("Mass cutoff 10^5-10^6 M_sun from I13 alone: not established; no mass sequence or profile
import", spectral_spine_closure_2026_09_22/i13/REPORT.md §6). Closing to 1e5-6 numerically
requires the accreting structure itself (MESA profiles + exact GR form), which no committed
repo input currently supplies.