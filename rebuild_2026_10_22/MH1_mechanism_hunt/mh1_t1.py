#!/usr/bin/env python3
"""MH1 T1 (FROZEN_CRITERIA.md): formation-order bound with spherical shells. A diagnostic, no rule. kappa = 1/2 FITTED, unused; not theory closed. Cold dark energy, never a particle."""
import json, math, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); Z = json.load(open(os.path.join(HERE, "mh1_ztable.json"))); G = 4.30091e-6 * 1.02271 ** 2; KMS = 1.02271e-3  # kpc^3 / Myr... G in kpc (km/s)^2 / Msun converted below
GK = 4.30091e-6 * (1.02271e-3) ** 2  # kpc^3 Msun^-1 Myr^-2
Om, h = 0.3129, 0.672; H0 = 100 * h / 3.0857e19 * 3.15576e13  # 1/Myr
def t_of_z(z): return 2 / (3 * H0 * math.sqrt(1 - Om)) * np.arcsinh(np.sqrt((1 - Om) / Om) * (1 + np.asarray(z, float)) ** -1.5)
T0 = float(t_of_z(0.0)); N = 3000; DT = 0.25; SR = (2, 3, 4, 6, 8, 10)
def run(M, Md, Rd, hist, p, fb=0.1595):
    f = (np.arange(N) + 0.5) / N; zt = np.interp(np.log(f), np.log(Z["f"]), Z["z"][str(M)]); tc = t_of_z(zt); tta = tc / 2; m0 = M / N; ms = (M * f); r = (8 * GK * ms * tta ** 2 / math.pi ** 2) ** (1 / 3); ra = r.copy(); L2 = 2 * GK * ms * ra * p / (1 + p); v = np.zeros(N); act = np.zeros(N, bool)
    tzf = float(t_of_z(float(np.interp(math.log(.5), np.log(Z["f"]), Z["z"][str(M)])))); ist = tzf / 2 if hist == "P" else tzf
    nC = min(N, int(math.ceil(Md / (fb * m0))))
    def state(t):
        if hist == "N": return np.full(N, m0), 0.0
        if hist in ("L", "P"): d = Md * min(max((t - ist) / (T0 - ist), 0.0), 1.0); return np.full(N, m0 * (1 - d / M)), d
        cl = t >= tc
        if hist == "I": g = Md / M; return np.where(cl, m0 * (1 - g), m0), float(cl.sum()) * m0 * g
        c = cl & (np.arange(N) < nC); return np.where(c, m0 * (1 - fb), m0), float(c.sum()) * m0 * fb
    t = float(tta[0]); out = np.zeros(len(SR)); ns = 0; Rs = np.array(SR) * Rd; t_s = T0 - 500.0; next_s = t_s
    while t < T0:
        act = tta <= t; o = np.argsort(r, kind="stable"); mm, d = state(t); c = np.cumsum(mm[o]); me = np.empty(N); me[o] = c - 0.5 * mm[o]; x = r / Rd; a = -GK * (me + d * (1 - (1 + x) * np.exp(-x))) / r ** 2 + L2 / r ** 3; v[act] += a[act] * DT; r[act] += v[act] * DT; r = np.abs(r); t += DT
        if t >= next_s:
            o = np.argsort(r); c = np.cumsum(mm[o]); out += np.interp(Rs, r[o], c); ns += 1; next_s += 5.0
    return (out / ns).tolist()
def main(mut=False):
    R = {}; EM = dict(a=11.18, b=0.9); Md10 = 10 ** (10 + (10 - EM["a"]) / EM["b"])
    for M, Md, Rd in ((1e12, 6.7187942657e10, 3.565), (1e10, Md10, 1.0)):
        for p in (0.2, 0.05, 0.5):
            N0 = run(M, 0, Rd, "N", p); row = {}
            for h_ in "LPIC": row[h_] = (np.array(run(M, Md, Rd, h_, p)) / np.array(N0)).tolist()
            rho = {h_: (row[h_][1] - 1) / (row[h_ if False else "L"][1] - 1) for h_ in "PIC"}; R[f"{M:g}|{p}"] = dict(Q=row, rho=rho, N0=N0, Md=Md, Rd=Rd); print(f"M {M:g} r_p/r_a {p}: Q(3Rd) " + " ".join(f"{h_} {row[h_][1]:.3f}" for h_ in "LPIC") + " rho " + " ".join(f"{k} {v:.3f}" for k, v in rho.items()), flush=True); json.dump(R, open(os.path.join(HERE, "mh1_t1.json"), "w"), indent=1)
    Q2 = np.array(run(1e12, 2 * 6.7187942657e10, 3.565, "L", .2)) / np.array(R["1e+12|0.2"]["N0"]); mv = (Q2[1] - 1) / (R["1e+12|0.2"]["Q"]["L"][1] - 1) - 1; ql = R["1e+12|0.2"]["Q"]["L"][1] - 1; k = abs(ql / .94 - 1) <= .25; rC = R["1e+12|0.2"]["rho"]["C"]; rD = R["1e+10|0.2"]["rho"]["C"]; lab = "NO LABEL" if not k or mv <= .3 else ("ORDER CAN REACH" if rC * .872 <= .2 and rD > .8 else "ORDER CANNOT REACH, SPHERICAL")
    s = f"K-T1 Q_L-1 (3Rd) {ql:.3f} vs LC1 0.94: {'PASS' if k else 'FAIL'}; MUTATE M_d x2 moves Q-1 by {mv:+.1%}: {'PASS' if mv > .3 else 'FAIL'}\nT1 label: {lab}; rho_C 1e12 {rC:.3f} (x 0.872 = {rC*.872:.3f}), rho_C 1e10 {rD:.3f}"
    print(s); R["label"] = lab; R["K_T1"] = ql; R["MUTATE"] = mv; json.dump(R, open(os.path.join(HERE, "mh1_t1.json"), "w"), indent=1)
main()
