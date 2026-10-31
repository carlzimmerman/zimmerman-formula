#!/usr/bin/env python3
"""QC1_qcd_volume_ratio (FROZEN_CRITERIA.md): the pasted QCD volume-ratio claim, T1-T10. Particle values PROVISIONAL, from memory."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
HC = 197.32698; R_REC, R_ERR = 5.272, 0.218; OM, H, WB = 0.2976016, 0.6856427, 0.0223081
MPL = 2.435e27; MP = 938.272; MPI0 = 134.9768; MPIC = 139.57039; FPI = 92.2; LQ = 217.0
out = {}
lam0, lamc = HC / MPI0, HC / MPIC
OB = WB / H ** 2; Rnat = (OM - OB) / OB
# T1
T1 = []
def chk(name, claimed, got):
    T1.append(dict(name=name, claimed=claimed, recomputed=got, off_pct=100 * (got / claimed - 1), wrong=bool(abs(got / claimed - 1) > 1e-3)))
chk("lam_pi0 fm", 1.46193, lam0); chk("lam_pi+ fm", 1.4138, lamc)
chk("(lam_pi+/0.8409)^3", 4.753, (lamc / 0.8409) ** 3); chk("x 10/9", 5.281, (lamc / 0.8409) ** 3 * 10 / 9)
chk("(lam_pi0/0.8414)^3", 5.245, (lam0 / 0.8414) ** 3); chk("(lam_pi0/0.8409)^3", 5.274, (lam0 / 0.8409) ** 3)
chk("R_nat from Om_b 0.047466", 5.2698, (OM - 0.047466) / 0.047466); chk("R_nat on the record's omega_b", 5.2698, Rnat)
chk("f_c from 5.274", 0.8406, 5.274 / 6.274); chk("sqrt(f m^2/M) eV", 2.63e-2, math.sqrt(FPI * 1e6 * (MPI0 * 1e6) ** 2 / MPL))
out["T1"] = T1
# T2
rps = {"CODATA2022 0.84075(64)": (0.84075, 0.00064), "CODATA2018 0.8414(19)": (0.8414, 0.0019), "proposal 0.8409": (0.8409, 0.0)}
T2 = {k: dict(ratio=(lam0 / r) ** 3, err=3 * (lam0 / r) ** 3 * e / r, z_vs_R=((lam0 / r) ** 3 - R_REC) / R_ERR) for k, (r, e) in rps.items()}
T2["R_rel_err_pct"] = 100 * R_ERR / R_REC; T2["z_vs_SH0ES_6.12"] = (T2["CODATA2022 0.84075(64)"]["ratio"] - 6.12) / 0.32
out["T2"] = T2
# T3
masses = [MPI0, MPIC, 493.677, 497.611, 547.862, 775.26, 782.66, 500.0, MP, 939.565, LQ, 155.0]
radii = [0.84075, 0.8414, 0.8751, 0.851, 0.67, 2.12778]
pref = [1, 10/9, 8/9, 9/8, 4/3, 3/4, 1/2, 2, 3/2, 2/3, 1/3, 3, 1/4, 4, math.pi, 1/math.pi, 4*math.pi/3, 3/(4*math.pi)]
base = [HC / m / r for m in masses for r in radii] + [a / b for a in masses for b in masses if a != b]
base = np.array(base); ex = np.array([1, 2, 3, 4.])
bare = np.concatenate([base ** n for n in ex])
full = np.concatenate([p * bare + o for p in pref for o in (0, 1, -1)]); full = full[full > 0]
rng = np.random.default_rng(20261031); nulls = np.exp(rng.uniform(np.log(3), np.log(8), 200))
T3 = {}
for lab, arr in (("full", full), ("bare", bare)):
    la = np.sort(np.log(arr)); T3[lab] = dict(n_forms=int(arr.size))
    for wlab, w in (("4.1pct", 0.041), ("0.28pct", 0.0028)):
        cnt = lambda t: int(np.searchsorted(la, np.log(t) + w) - np.searchsorted(la, np.log(t) - w))
        c0 = cnt(R_REC); cs = np.array([cnt(t) for t in nulls])
        T3[lab][wlab] = dict(hits_at_target=c0, null_median=float(np.median(cs)), null_p95=float(np.percentile(cs, 95)), frac_null_ge=float(np.mean(cs >= c0)))
T3["DISTINGUISHED"] = all(T3[l][w]["frac_null_ge"] <= 0.05 for l in ("full", "bare") for w in ("4.1pct", "0.28pct"))
out["T3"] = T3
# T4
V = lambda r: 4 * math.pi / 3 * r ** 3
rp = 0.84075; Vl, Vp = V(lam0), V(rp); HC3 = HC ** 3
eps_virial = MP / 4 / Vp; eps_bag = 145.0 ** 4 / HC3
eps_ta = {g: (9 / 32) * g * 1e12 / HC3 for g in (0.005, 0.012, 0.02)}
T4 = dict(V_cloud_fm3=Vl, density_needed_MeV_fm3=R_REC * MP / Vl, proton_mean_density=MP / Vp,
          R_own_virial=eps_virial * Vl / MP, R_MIT_bag=eps_bag * Vl / MP, R_trace_anomaly={str(g): e * Vl / MP for g, e in eps_ta.items()},
          eps_trace_anomaly={str(g): e for g, e in eps_ta.items()}, eps_virial=eps_virial, eps_MIT=eps_bag, R_shell_only=(lam0 / rp) ** 3 - 1)
T4["PASS"] = bool(abs(T4["R_own_virial"] - R_REC) < R_ERR)
out["T4"] = T4
# T5-T7 at T = 155 MeV
T = 155.0; rhoc = 1.87834e-29 * H ** 2  # g/cm3
nb0 = OB * rhoc * 5.60959e23 / (MP * 1e-3 * 1.0 * 1.0) * 1.0  # GeV/cm3 over GeV
eta_s = nb0 / 2891.2
T567 = {}
for g in (17.0, 62.0):
    s = 2 * math.pi ** 2 / 45 * g * T ** 3; nb = eta_s * s
    pair = 2 * 2 * 2 * (MP * T / (2 * math.pi)) ** 1.5 * math.exp(-MP / T)
    Hub = 1.66 * math.sqrt(g) * T ** 2 / 1.22e22
    T567[f"g{int(g)}"] = dict(nb_MeV3=nb, N_plus_anti_over_net=pair / nb, H_MeV=Hub, Gamma_over_H_400=400 / Hub, Gamma_over_H_700=700 / Hub,
                              spacing_fm=nb ** (-1 / 3) * HC, cloud_fill=Vl * nb / HC3, rho_c_over_MIT_B=R_REC * MP * nb / 145.0 ** 4)
T567["eta_s"] = eta_s; T567["thermal_factor"] = {str(m): math.exp(-m / T) for m in (500, 1000, 1500)}
T567["lifetime_s_at_500MeV_width"] = 6.582e-22 / 500; T567["X1_Gamma_over_H"] = 22.6
out["T5_T6_T7"] = T567
# T8
ev = lambda x: x * 1e6
H0ev = 1.4388e-33 * (H / 0.6856427) * 1.0 * (0.6856427 / 0.6856427)
H0ev = H * 100 * 1e3 / 3.0857e22 * 6.582e-16
rhoL = 3 * H0ev ** 2 * MPL ** 2 * (1 - OM); rl14 = rhoL ** 0.25
a0ev = lambda a: a * 1.0546e-34 / 2.998e8 / 1.602e-19
aq = ev(FPI) ** 2 * ev(MPI0) ** 4 / (8 * math.pi * MPL ** 5)
T8 = dict(rhoL14_eV=rl14, H0_Lq3_14_eV=(H0ev * ev(LQ) ** 3) ** 0.25, ratio_scale=(H0ev * ev(LQ) ** 3) ** 0.25 / rl14,
          sqrt_fm2_M_eV=math.sqrt(ev(FPI) * ev(MPI0) ** 2 / MPL), ratio_sqrt=math.sqrt(ev(FPI) * ev(MPI0) ** 2 / MPL) / rl14,
          f2m2_over_M2_eV2=(ev(FPI) * ev(MPI0) / MPL) ** 2, dimension_of_that="eV^2, while rho is eV^4", a_QCD_eV=aq, a0_eV=a0ev(1.2e-10), a_ratio=aq / a0ev(1.2e-10))
out["T8"] = T8
# T9
G = 6.6743e-11; c = 2.99792458e8; Hs = H * 1e5 / 3.0857e22; rhoLsi = 3 * Hs ** 2 * (1 - OM) / (8 * math.pi * G)
base_a = c * math.sqrt(G * rhoLsi); MSPC2 = 1.98847e30 / 3.0857e16 ** 2
T9 = dict(c_sqrtGrho=base_a, a0_kappa_half=0.5 * base_a, Sigma_4piG_Msun_pc2=base_a / (4 * math.pi * G) / MSPC2, Sigma_a0_2piG=0.5 * base_a / (2 * math.pi * G) / MSPC2,
          identical=True, note="kappa/(2 pi) = 1/(4 pi) is kappa = 1/2 restated; a0 in the law still needs kappa")
out["T9"] = T9
# T10
x = np.logspace(-3, 3, 7)
forms = {"(1+x^2)^-3/2": lambda x: (1 + x ** 2) ** -1.5, "(1+x^4)^-3/4": lambda x: (1 + x ** 4) ** -0.75, "(1+x^2)^-1/2 (1+x^4)^-1/2": lambda x: (1 + x ** 2) ** -0.5 * (1 + x ** 4) ** -0.5}
T10 = {}
for k, f in forms.items():
    d0 = (f(np.array(1e-4)) - 1) / 1e-4; slope = (np.log(f(1e4)) - np.log(f(1e3))) / np.log(10)
    T10[k] = dict(rho_prime_0=float(d0), outer_slope=float(slope))
out["T10"] = T10
out["WORD"] = dict(X1_closed=False, mechanism="see README")
json.dump(out, open(os.path.join(HERE, "qc1_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
