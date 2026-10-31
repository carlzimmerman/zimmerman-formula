#!/usr/bin/env python3
"""CR1_carrier_requirements (FROZEN_CRITERIA.md): numbers behind the carrier grade. Literature values PROVISIONAL, from memory."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R, MP, HC = 5.272, 938.272, 197.32698; ETA_S = 8.664849e-11  # QC1
# ET1 table: lg M200, S, 95 % bounds
T = np.array([[9.97, 68.6, 51.6, 85.0], [10.59, 102.7, 81.0, 124.2], [11.13, 143.2, 118.4, 199.8], [11.76, 150.2, 97.9, 190.5], [12.11, 215.1, 136.6, 272.1], [12.27, 411.7, 181.6, 596.0]])
x, y = T[:, 0], np.log10(T[:, 1]); sig = (np.log10(T[:, 3]) - np.log10(T[:, 2])) / 4
w = 1 / sig ** 2; xb = np.sum(w * x) / w.sum(); slope = np.sum(w * (x - xb) * y) / np.sum(w * (x - xb) ** 2); eslope = 1 / math.sqrt(np.sum(w * (x - xb) ** 2))
def chi2(b):
    a = np.sum(w * (y - b * x)) / w.sum(); return float(np.sum(w * (y - a - b * x) ** 2))
fit = dict(slope=slope, err=eslope, chi2_best=chi2(slope), dof=4, exponents={str(b): dict(chi2=chi2(b), z=(b - slope) / eslope, within_2sigma=bool(abs(b - slope) < 2 * eslope)) for b in (1.0, 2 / 3, 1 / 3, 0.0)})
# D
meff = {str(q): R * MP / q for q in (1, 2, 3)}; M = R * MP
def Tend(M, g=106.75): return (M ** 4 / (R * MP * ETA_S * 2 * math.pi ** 2 / 45 * g)) ** (1 / 3)
D = dict(m_eff_MeV_q=meff, m_eff_range_R_1sigma=[(R - 0.218) * MP, (R + 0.218) * MP], T_dust_end_GeV=Tend(M) / 1e3, T_dust_end_GeV_Mx3=Tend(3 * M) / 1e3, T_dust_end_GeV_Mover3=Tend(M / 3) / 1e3, T_sphaleron_GeV=130.0, window_exists=bool(Tend(M / 3) / 1e3 > 130), preinflation_dilution_N60=math.exp(-180.0), delta_today=None)
# rho_c today over M^4
rho0 = 1.87834e-29 * 0.6856427 ** 2 * 0.2976016 * 0.84 * 5.60959e23 * 1e9 * (1.97327e-5) ** 3  # eV^4
D["rho_c0_eV4"] = rho0; D["rho_c0_over_M4"] = rho0 / (M * 1e6) ** 4
# F: Schive 2014: rho_c = 1.9 (m/1e-23)^-2 (r_c/kpc)^-4 Msun/pc3; r_c = 1.6 (m/1e-22)^-1 (M/1e9)^(-1/3) kpc
def schive(m22, M):
    rc = 1.6 / m22 * (M / 1e9) ** (-1 / 3); rho = 1.9 * (10 * m22) ** -2 * rc ** -4; return rc, rho * rc * 1e3
target_M, target_S = 10 ** 11.76, 150.2
m22 = target_S / schive(1.0, target_M)[1]
floor_lo, floor_hi = 2e-19, 5e-19
F = dict(m_match_eV=m22 * 1e-22, r_c_kpc_at_match=schive(m22, target_M)[0], floor_L383_eV=[floor_lo, floor_hi], m_short_of_floor=[floor_lo / (m22 * 1e-22), floor_hi / (m22 * 1e-22)],
         S_vs_table={f"{a:.2f}": dict(wave=schive(m22, 10 ** a)[1], need=s) for a, s, _, _ in T}, S_at_floor_1e12=schive(floor_lo / 1e-22, 1e12)[1], rc_at_floor_1e12_pc=schive(floor_lo / 1e-22, 1e12)[0] * 1e3,
         q_per_baryon_at_floor=[R * MP * 1e6 / floor_hi, R * MP * 1e6 / floor_lo])
# G: fixed R_TF, S ~ V^2/(G R): needed r0 at lg M 11.94 is 14 kpc (brief 3b); r0 ~ V^2/(G S)
r0 = {f"{a:.2f}": (lambda M, S: (M / (163.0 * (M / 1e12) ** (1 / 3) * 1e3)) / S / 1e3)(10 ** a, s) for a, s, _, _ in T}
out = dict(ET1_fit=fit, D=D, F=F, G=dict(r0_scale_kpc=r0, spread=max(r0.values()) / min(r0.values()), note="V^2/(G S), order of magnitude; fixed R_TF needs spread 1"))
json.dump(out, open(os.path.join(HERE, "cr1_results.json"), "w"), indent=1); print(json.dumps(out, indent=1))
