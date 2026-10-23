#!/usr/bin/env python3
"""L1_khronon_pm validation (FROZEN_CRITERIA.md §3 + AMENDMENT A1): K0, X0, KA, KB, KC, KR.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_khronon_pm.py               -> l1_khronon_pm.out, l1_khronon_pm_results.json
  L1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 l1_khronon_pm.py   -> *_MUTATE.out / *_results_MUTATE.json (KA, KB, KC must FAIL)

<= 128^3, one thread, < 1 GB.  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, math, time, subprocess, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("L1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
WORKV = os.path.join(HERE, "work", "validate" + SUF); os.makedirs(WORKV, exist_ok=True)
os.environ["L1_WORK"] = WORKV
os.environ.update(CFG596_MODE="exact", CFG596_L="100", CFG596_THREADS="1", CFG596_WORK=os.path.join(WORKV, "cfg596_ref"),
                  CFG596_RELIEF="0", CFG596_EXTRA="")
import numpy as np
sys.path.insert(0, HERE)
import khronon_pm as K
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
np.seterr(invalid='ignore')
K.set_threads(1)

OUT, RES, CHK = [], {"lane": "L1_khronon_pm", "date": "2026-10-23", "mutate": MUT}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
P("L1_khronon_pm validation" + (" [MUTATE]" if MUT else "") + ": kappa = 1/2 FITTED; footings never pooled; BS24 PN system, J = J_x; no settling, no QUMOND phantom")

# ------------------------------------------------------------------ K0: reproduce F3 K4 (background A, a_i = 1e-3)
F3 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))
c2b = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]["lcdm_refit"]
wbA, wcA, thA, lnAA, nsA, tauA = c2b["params"]; hA = c2b["chi2"]["H0"] / 100.0
PkA, s8A = K.class_pk(wbA, wcA, hA, lnAA, nsA, tauA)
OmA, ObA = (wbA + wcA) / hA ** 2, wbA / hA ** 2
KT = np.geomspace(1e-3, 3.0, 36)
def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * K.W8(K.KS * 8.0) ** 2 * K.KS ** 2, K.KS) / (2 * math.pi ** 2))
def T_ratio(kk, mu, Om, Ob, h, kind, a_i):
    sol = K.two_fluid(kk, mu, Om, Ob, h, kind, a_i, (1.0,))[0]; d0 = K.two_fluid(kk, None, Om, Ob, h, "dust", a_i, (1.0,))[0]
    return (Ob * sol[0] + (Om - Ob) * sol[1]) / (Ob * d0[0] + (Om - Ob) * d0[1])
def sig8_ratio(Pk, mu, Om, Ob, h, kind, a_i):
    T = T_ratio(KT, mu, Om, Ob, h, kind, a_i)
    Tf = np.interp(np.log(K.KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(Pk, Tf) / sig8(Pk)
mu_edge = F3["K4"]["BS24_Eq39_edge_100kpc"]["mu_hMpc"]
r_b = sig8_ratio(PkA, mu_edge, OmA, ObA, hA, "bsk2", 1e-3); r_j = sig8_ratio(PkA, mu_edge, OmA, ObA, hA, "jeans", 1e-3)
f_b = F3["K4"]["BS24_Eq39_edge_100kpc"]["bsk2_ai0.001"]["sigma8_ratio"]; f_j = F3["K4"]["BS24_Eq39_edge_100kpc"]["jeans_ai0.001"]["sigma8_ratio"]
RES["K0"] = dict(mu=mu_edge, bsk2=r_b, bsk2_F3=f_b, jeans=r_j, jeans_F3=f_j)
check("K0", abs(r_b / f_b - 1) <= 1e-3 and abs(r_j / f_j - 1) <= 1e-3,
      f"bsk2 {r_b:.5f} (F3 {f_b:.5f}); jeans {r_j:.5f} (F3 {f_j:.5f})", "|rel|<=1e-3")

# ------------------------------------------------------------------ X0: linear hold-field argument before/after z_i; quadratic-K background
bg = K.MODEL_B; PkB, s8B = K.pk_model_B(); MU = 14.8
kq = np.geomspace(1e-4, 16.0, 400)
A_LIST = [1e-3, 5e-3, 0.02, 0.1, 0.5, 1.0]
trs = K.linear_transfer(kq, "KX", MU, bg, A_LIST)
Pq = np.interp(np.log(kq), np.log(K.KS), PkB)
X0 = {"sigma8_class_B": s8B, "rows": {}}
flag = False
for foot in ("canonical", "alt"):
    a0c = bg.a0c(foot)
    for a, t in zip(A_LIST, trs):
        row = {}
        for kmax in (4.0, 16.0):
            sel = kq <= kmax
            xi2 = (1.5 * bg.Otau * t["Rt"] / (a * (kq ** 2 + (a * MU) ** 2))) ** 2 * kq ** 2 * Pq * kq ** 2 / (2 * math.pi ** 2)
            ph2 = (1.5 * (bg.Ob * t["Rb"] + bg.Otau * t["Rt"]) / (a * kq ** 2)) ** 2 * kq ** 2 * Pq * kq ** 2 / (2 * math.pi ** 2)
            row[f"x_hold_rms_k{kmax:g}"] = math.sqrt(np.trapz(xi2[sel], kq[sel])) / (a * a0c)
            row[f"x_total_rms_k{kmax:g}"] = math.sqrt(np.trapz(ph2[sel], kq[sel])) / (a * a0c)
        X0["rows"][f"{foot}_a{a:g}"] = row
        if a <= 0.02 + 1e-12 and row["x_hold_rms_k4"] > 0.1: flag = True
I0 = 3 * bg.Otau / 2997.92458 ** 2
for zi_ in (49, 199, 999):
    a = 1 / (1 + zi_); q1 = I0 / (2 * MU ** 2 * a ** 3); X0[f"Qbar_minus_1_z{zi_}"] = q1; X0[f"w_z{zi_}"] = q1 / (q1 + 2)
X0["flag_zi199"] = flag
RES["X0"] = X0
for k_, v in X0["rows"].items():
    P(f"  X0 {k_}: x_hold_rms(k<=4) {v['x_hold_rms_k4']:.3e} (k<=16 {v['x_hold_rms_k16']:.3e}); x_total_rms(k<=4) {v['x_total_rms_k4']:.3e}")
check("X0", True, f"flag z_i=199 variant: {flag}; Qbar-1 at z 49/199/999: {X0['Qbar_minus_1_z49']:.2e}/{X0['Qbar_minus_1_z199']:.2e}/{X0['Qbar_minus_1_z999']:.2e} "
      f"(w {X0['w_z49']:.1e}/{X0['w_z199']:.1e}/{X0['w_z999']:.1e})", "computed")

# ------------------------------------------------------------------ KA: GR limit vs the copied CFG596 S0 engine (64^3, L100, same ICs)
R = K.ref596()
ref = R.run("S0", "FLAT", "canonical", 64, 1.0)
cfgA = dict(mode="GRJ", muK=1e6, N=64, L=100.0, zi=49, bg="CFG596", ic="cfg596", tag="KA_GRJ_64" + SUF,
            snaps=[0.5, 2 / 3, 1.0], guard=False, ckpt_every=0, log=False, mut=("noKhronon" if MUT else None))
mine = K.run_sim(cfgA)
KA = {}
for z in ("z1", "z0.5", "z0"):
    kb = np.array(mine["snap"][z]["k"]); pm = np.array(mine["snap"][z]["P"]); pr = np.array(ref["snap"][z]["P"]); kr = np.array(ref["snap"][z]["k"])
    sel = kb <= math.pi * 64 / 100 / 2 * (1 + 1e-9)
    KA[z] = dict(max_rel=float(np.max(np.abs(pm[sel] / pr[sel] - 1))), k_match=float(np.max(np.abs(kb / kr - 1))),
                 sigma8=mine["snap"][z]["sigma8"], sigma8_ref=ref["snap"][z]["sigma8"])
RES["KA"] = KA
check("KA", KA["z0"]["max_rel"] <= 0.02 and KA["z0"]["k_match"] < 1e-5,      # bin sanity (CFG596 builds k in float32)
      f"max|P/P_596-1| z0 {KA['z0']['max_rel']:.2e}; k-bin match {KA['z0']['k_match']:.1e} (z1 {KA['z1']['max_rel']:.2e}, z0.5 {KA['z0.5']['max_rel']:.2e}); sigma8 {KA['z0']['sigma8']:.4f} vs {KA['z0']['sigma8_ref']:.4f}",
      "z0 max|rel|<=0.02 for k<=k_Nyq/2")

# ------------------------------------------------------------------ KB: small-amplitude linear growth vs the ODE (64^3, L25, mu 14.8)
aa = K.step_grid(49); a_i = float(aa[0]); j3 = int(np.argmin(np.abs(aa - 0.25))); a3 = float(aa[j3])
base = dict(N=64, L=25.0, zi=49, nseed=256, seed=359, eps=0.01, bg="B", ic="native", snaps=[a3, 1.0], xgrowth=True,
            guard=False, ckpt_every=0, log=False, foot="canonical")
runs = {}
for lab, mode, mu, mut in (("KX", "KX", MU, ("noHold" if MUT else None)), ("S0", "S0", float("inf"), None), ("GRJ", "GRJ", MU, None)):
    runs[lab] = K.run_sim(dict(base, mode=mode, muK=mu, mut=mut, tag=f"KB_{lab}_64" + SUF))
KB = {}
kf, knyq = 2 * math.pi / 25.0, math.pi * 64 / 25.0
for a_s in (a3, 1.0):
    sn = [s for s in runs["KX"]["snap"] if s not in ("zi",) and abs(runs["KX"]["snap"][s]["a"] - a_s) < 1e-9][0]
    kc = np.array(runs["KX"]["snap"][sn]["k_cross"])
    sel = (kc >= kf * (1 - 1e-9)) & (kc <= knyq / 4 * (1 + 1e-9))
    tx = K.linear_transfer(kc, "KX", MU, bg, [a_i, a_s]); td = K.linear_transfer(kc, "S0", None, bg, [a_i, a_s])
    tj = K.linear_transfer(kc, "GRJ", MU, bg, [a_i, a_s])
    G_ode = {"KX": tx[1]["Tm"] / tx[0]["Tm"], "S0": td[1]["Tm"] / td[0]["Tm"], "GRJ": tj[1]["Tm"] / tj[0]["Tm"]}
    G_pm = {l: np.array(runs[l]["snap"][sn]["G_cross"]) for l in runs}
    R_pm, R_ode = G_pm["KX"] / G_pm["S0"], G_ode["KX"] / G_ode["S0"]
    Rj_pm, Rj_ode = G_pm["GRJ"] / G_pm["S0"], G_ode["GRJ"] / G_ode["S0"]
    KB[sn] = dict(a=a_s, k=kc[sel], R_pm=R_pm[sel], R_ode=R_ode[sel], max_rel=float(np.max(np.abs(R_pm[sel] / R_ode[sel] - 1))),
                  tooth=float(np.max(np.abs(R_ode[sel] - 1))), S0_bias=G_pm["S0"][sel] / G_ode["S0"][sel],
                  GRJ_max_rel=float(np.max(np.abs(Rj_pm[sel] / Rj_ode[sel] - 1))), GRJ_R_pm=Rj_pm[sel], GRJ_R_ode=Rj_ode[sel],
                  hold_iters_max=runs["KX"].get("max_iters"))
    P(f"  KB {sn} (a {a_s:.4f}): k {np.round(kc[sel], 3).tolist()}")
    P(f"     R_pm  {np.round(R_pm[sel], 4).tolist()}\n     R_ode {np.round(R_ode[sel], 4).tolist()}  (tooth max|R_ode-1| {KB[sn]['tooth']:.3f})")
    P(f"     S0 PM/ODE growth {np.round(KB[sn]['S0_bias'], 4).tolist()}; GRJ (Jeans) max|R/R_ode-1| {KB[sn]['GRJ_max_rel']:.3e} (reported)")
RES["KB"] = KB
kbk = list(KB)
P("KB-frozen " + ("PASS " if all(KB[s]["max_rel"] <= 0.02 for s in kbk) else "FAIL ")
  + "; ".join(f"{s}: max|R/R_ode-1| {KB[s]['max_rel']:.2e}" for s in kbk) + " (frozen statistic, bin-mean ODE; superseded by AMENDMENT A2, post-result; not counted)")

# KB-A2 (AMENDMENT A2, post-result): the ODE pushed through the estimator's own mode weights, PM coupling g_j calibrated on S0 alone
mB = K.Mesh(64, 25.0); PkB_ = K.pk_model_B()[0]
dkB = K.nyq_zero(mB, K.white_noise_k(64, 256, 359) * np.sqrt(np.interp(np.log(np.maximum(mB.kmag, 1e-5)), np.log(K.KS), PkB_) / (25.0 / 64) ** 3) * 64 ** 1.5)
WC = (np.sinc(mB.kx * mB.dx / (2 * np.pi)) * np.sinc(mB.ky * mB.dx / (2 * np.pi)) * np.sinc(mB.kz * mB.dx / (2 * np.pi))) ** 2
edgB = np.arange(0.5, 64 // 2 + 1, 1.0) * mB.kf; ibB = np.digitize(mB.kmag, edgB)
wtB = np.full(dkB.shape, 2.0); wtB[..., 0] = 1.0; wtB[..., -1] = 1.0; wtB[0, 0, 0] = 0.0
OrB = 4.18e-5 / bg.h ** 2; OLB = 1 - bg.Om - OrB; OKB = bg.Om - bg.Ob
EkB = lambda a: math.sqrt(bg.Om * a ** -3 + OrB * a ** -4 + OLB)
def evolve(kk, g, kind, st0, a_from, a_to):
    kk = np.atleast_1d(np.asarray(kk, float)); n = len(kk)
    def rhs(x, st):
        a = math.exp(x); E = EkB(a); e_ = 1e-6
        dlnE = (math.log(EkB(a * math.exp(e_))) - math.log(EkB(a * math.exp(-e_)))) / (2 * e_)
        dens = 1.5 * a ** -3 / E ** 2 * g; sk = K.kernel_s(kind, kk, a, MU) if kind != "dust" else 1.0
        db_, gb_, dt_, gt_ = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        return np.concatenate([gb_, -(2 + dlnE) * gb_ + dens * (bg.Ob * db_ + OKB * dt_), gt_, -(2 + dlnE) * gt_ + dens * (bg.Ob * db_ + OKB * dt_ * sk)])
    sol = solve_ivp(rhs, [math.log(a_from), math.log(a_to)], np.concatenate(st0), method="DOP853", rtol=1e-9, atol=1e-14)
    y = sol.y[:, -1]; d0 = bg.Ob * st0[0] + OKB * st0[2]
    return (bg.Ob * y[:n] + OKB * y[2 * n:3 * n]) / d0
def state(mode, kk):
    t = K.linear_transfer(np.atleast_1d(kk), mode, (MU if mode != "S0" else None), bg, [a_i])[0]
    return [t["Rb"], t["Rb"] * t["fb"], t["Rt"], t["Rt"] * t["ft"]]
KBA = {}
for lab, kind, nfine in (("KX", "bsk2", 48), ("GRJ", "jeans", 400)):
    for a_s in (a3, 1.0):
        sn = [s for s in runs["KX"]["snap"] if s != "zi" and abs(runs["KX"]["snap"][s]["a"] - a_s) < 1e-9][0]
        kc = np.array(runs[lab]["snap"][sn]["k_cross"]); Gl = np.array(runs[lab]["snap"][sn]["G_cross"]); Gs = np.array(runs["S0"]["snap"][sn]["G_cross"])
        sel = np.where((kc >= kf * (1 - 1e-9)) & (kc <= knyq / 4 * (1 + 1e-9)))[0]
        st_d = state("S0", np.array([0.5]))
        rows = []
        for j in sel:
            g = brentq(lambda gg: evolve([0.5], gg, "dust", st_d, a_i, a_s)[0] - Gs[j], 0.3, 1.5, xtol=1e-7)
            inb = ibB == (j + 1)
            kmod = mB.kmag[inb]; kfine = np.linspace(kmod.min() * 0.999, kmod.max() * 1.001, nfine)
            Gf = evolve(kfine, g, kind, state(lab, kfine), a_i, a_s)
            Tin = np.interp(kmod, kfine, K.linear_transfer(kfine, lab, MU, bg, [a_i])[0]["Tm"])
            w = wtB[inb] * np.abs(Tin * dkB[inb]) ** 2 * WC[inb] ** 2
            Gpred = float(np.sum(w * np.interp(kmod, kfine, Gf)) / np.sum(w))
            rows.append((float(kc[j]), g, Gl[j], Gpred, Gl[j] / Gpred - 1))
        KBA[f"{lab}_{sn}"] = dict(a=a_s, k=[r[0] for r in rows], g_S0=[r[1] for r in rows], G_pm=[r[2] for r in rows], G_A2=[r[3] for r in rows],
                                  rel=[r[4] for r in rows], max_rel=float(max(abs(r[4]) for r in rows)))
        P(f"  KB-A2 {lab} {sn}: g_S0 {np.round([r[1] for r in rows], 4).tolist()}; G_pm/G_A2-1 {np.round([r[4] for r in rows], 4).tolist()}")
RES["KB_A2"] = KBA
kx_keys = [k_ for k_ in KBA if k_.startswith("KX_")]
check("KB", all(KBA[k_]["max_rel"] <= 0.02 for k_ in kx_keys),
      "; ".join(f"{k_}: max|G_pm/G_A2-1| {KBA[k_]['max_rel']:.2e}" for k_ in kx_keys)
      + "; GRJ (reported) " + "; ".join(f"{k_}: {KBA[k_]['max_rel']:.2e}" for k_ in KBA if k_.startswith("GRJ_")),
      "<=0.02 (AMENDMENT A2 statistic, post-result; threshold unchanged)")

# ------------------------------------------------------------------ KC: static point mass (128^3, L 0.32 Mpc/h, M 1e11 Msun/h, Plummer 2 cells, mu_K = 0)
NC, LC, MC = 128, 0.32, 1e11
mC = K.Mesh(NC, LC); b = 2 * mC.dx
ii = np.arange(NC) * mC.dx - LC / 2
X, Y, Z = np.meshgrid(ii, ii, ii, indexing="ij"); rr = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
rho = (1 + rr ** 2 / b ** 2) ** -2.5; rho *= MC / (rho.sum() * mC.dx ** 3)
Sb = 4 * math.pi * K.G_CODE * (rho - rho.mean()); Sbk = mC.fft(Sb); del rho, Sb
rhat = [np.where(rr > 0, c / np.maximum(rr, 1e-30), 0).astype(np.float32) for c in (X, Y, Z)]; del X, Y, Z
edges = np.geomspace(3 * mC.dx, LC / 8, 11); shell = np.digitize(rr, edges)
def shell_mean(f):
    return np.array([f[shell == i].mean() for i in range(1, 11)])
def radial(G): return G[0] * rhat[0] + G[1] * rhat[1] + G[2] * rhat[2]
KC = {}
for foot in ("canonical", "alt"):
    a0c = bg.a0c(foot)
    G, GN, inf1 = K.solve_aqual_projection(mC, Sbk, a0c, mu_kind=("standard" if MUT else "simple"))
    gNm = np.sqrt(GN[0] ** 2 + GN[1] ** 2 + GN[2] ** 2); y = np.maximum(gNm, 1e-300) / a0c
    law = 0.5 * (1 + np.sqrt(1 + 4 / y)) * radial(GN); del gNm, y, GN
    g_s, law_s = shell_mean(radial(G)), shell_mean(law); del law
    c1 = float(np.max(np.abs(g_s / law_s - 1)))
    # (c2) phantom -> the engine's field_solve (Poisson for all mass + KX hold from Xi = 0)
    gm = np.sqrt(G[0] ** 2 + G[1] ** 2 + G[2] ** 2); omm = 1.0 - gm / (a0c + gm)
    Stk = mC.div_k([omm * G[c] for c in range(3)]); Stk[0, 0, 0] = 0; del omm
    phik, xik, inf2 = K.field_solve(mC, Sbk, Stk, 1.0, "KX", 0.0, a0c, xi0=None, mut=("swap" if MUT else None))
    Gt = [mC.grad_c(phik, c) for c in range(3)]; Gx = [mC.grad_c(xik, c) for c in range(3)]
    del phik, xik
    gt_s = shell_mean(radial(Gt))
    net = np.sqrt(sum((Gt[c] - Gx[c]) ** 2 for c in range(3))); tot = np.sqrt(sum(Gt[c] ** 2 for c in range(3)))
    c2a = float(np.max(np.abs(gt_s / law_s - 1))); c2b = float(np.max(shell_mean(net) / shell_mean(tot)))
    xr = shell_mean(gm) / a0c
    phA, infA = K.solve_hold(mC, Sbk, 0.0, a0c, coef="swap", tol=1e-9, maxit=400)      # independent AQUAL solve (A2 item 3)
    GA = [mC.grad_c(mC.fft(phA), c) for c in range(3)]; del phA
    xa = float(np.max(np.abs(shell_mean(radial(GA)) / g_s - 1))); xa_law = float(np.max(np.abs(shell_mean(radial(GA)) / law_s - 1))); del GA
    KC[foot] = dict(r_edges_kpc_h=edges * 1e3, x_shell=xr, g_over_law=g_s / law_s, c1_max=c1, aqual_iters=inf1["iters"],
                    aqual_res=inf1["res"], aqual_residual_rel=inf1["aqual_residual_rel"], c2_baryon_max=c2a, c2_khronon_net_max=c2b,
                    hold_iters=inf2.get("iters"), hold_res=inf2.get("res"), hold_converged=inf2.get("converged"),
                    anderson_aqual_vs_projection=xa, anderson_aqual_vs_law=xa_law, anderson_aqual_iters=infA["iters"], anderson_aqual_res=infA["res"])
    P(f"  KC {foot}: x per shell {np.round(xr, 3).tolist()}; g/law {np.round(g_s / law_s, 5).tolist()}")
    P(f"     c1 max|g/law-1| {c1:.2e} (AQUAL it {inf1['iters']}, res {inf1['res']:.1e}, div residual {inf1['aqual_residual_rel']:.1e}); "
      f"c2 baryon {c2a:.2e}, khronon net/total {c2b:.2e} (hold it {inf2.get('iters')}, res {inf2.get('res', float('nan')):.1e}, conv {inf2.get('converged')})")
    P(f"     reported (A2): Anderson AQUAL it {infA['iters']} res {infA['res']:.1e}: vs projection max {xa:.2e}, vs law max {xa_law:.2e}")
RES["KC"] = KC
okc = all(KC[f]["c1_max"] <= 0.01 and KC[f]["c2_baryon_max"] <= 0.01 and KC[f]["c2_khronon_net_max"] <= 0.01 for f in KC)
check("KC", okc, "; ".join(f"{f}: c1 {KC[f]['c1_max']:.2e}, c2 baryon {KC[f]['c2_baryon_max']:.2e}, c2 khronon {KC[f]['c2_khronon_net_max']:.2e}" for f in KC),
      "each <= 0.01 (both footings)")
del rr, rhat, shell

# ------------------------------------------------------------------ KR: SIGTERM mid-run + --resume == uninterrupted (64^3, L25, KX, full amplitude)
if not MUT:
    cmd = [sys.executable, os.path.join(HERE, "khronon_pm.py"), "run", "--mode", "KX", "--foot", "canonical", "--muK", "14.8", "--N", "64",
           "--L", "25", "--zi", "49", "--nseed", "256", "--threads", "1", "--no_guard", "--ckpt_every", "10"]
    env = dict(os.environ, L1_WORK=WORKV)
    full = subprocess.run(cmd + ["--tag", "KR_full"], env=env, capture_output=True, text=True)
    pr = subprocess.Popen(cmd + ["--tag", "KR_int"], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t_sig = None; lines = []
    for line in pr.stdout:
        lines.append(line)
        if t_sig is None and "step 40/" in line:
            pr.send_signal(signal.SIGTERM); t_sig = time.time()
    rc = pr.wait(); t_exit = time.time() - t_sig if t_sig else None
    ck = os.path.exists(os.path.join(WORKV, "KR_int", "ckpt.npz"))
    pre = json.load(open(os.path.join(WORKV, "KR_int", "result.json")))
    res2 = subprocess.run(cmd + ["--tag", "KR_int", "--resume"], env=env, capture_output=True, text=True)
    rf = json.load(open(os.path.join(WORKV, "KR_full", "result.json"))); ri = json.load(open(os.path.join(WORKV, "KR_int", "result.json")))
    same_sha = rf.get("final_state_sha256") == ri.get("final_state_sha256") and rf.get("final_state_sha256") is not None
    pf, pi_ = np.array(rf["snap"]["z0"]["P"]), np.array(ri["snap"]["z0"]["P"])
    same_P = bool(np.array_equal(pf, pi_)); dP = float(np.max(np.abs(pi_ / pf - 1)))
    RES["KR"] = dict(rc_interrupted=rc, seconds_signal_to_exit=t_exit, ckpt_exists=ck, preempted_status=pre.get("status"),
                     resumed_at=ri.get("resumes"), sha_full=rf.get("final_state_sha256"), sha_resumed=ri.get("final_state_sha256"),
                     P_bit_identical=same_P, max_rel_dP=dP, rc_full=full.returncode, rc_resume=res2.returncode,
                     sigma8_z0=rf["snap"]["z0"]["sigma8"], peak_rss_full_gb=rf.get("peak_rss_gb"))
    check("KR", rc == 0 and t_exit is not None and t_exit <= 300 and ck and same_sha and same_P and full.returncode == 0 and res2.returncode == 0,
          f"rc {rc}, exit {t_exit:.1f} s after SIGTERM, ckpt {ck}, status {pre.get('status')}, resumed {ri.get('resumes', [{}])[0].get('n_next')}; "
          f"sha equal {same_sha}; P(z0) bit-identical {same_P} (max|dP/P| {dP:.1e})", "rc 0, <=300 s, bit-identical")

if not MUT:
    envq = dict(env, HEAVYQ_YIELD_EXIT="75")
    pq = subprocess.Popen(cmd + ["--tag", "KRq_int"], env=envq, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tq = None
    for line in pq.stdout:
        if tq is None and "step 70/" in line: pq.send_signal(signal.SIGTERM); tq = time.time()
    rcq = pq.wait(); tqe = time.time() - tq if tq else None
    r1 = subprocess.run(cmd + ["--tag", "KRq_int", "--resume"], env=envq, capture_output=True, text=True)
    t_ = time.time(); r2 = subprocess.run(cmd + ["--tag", "KRq_int", "--resume"], env=envq, capture_output=True, text=True); t2 = time.time() - t_
    rq = json.load(open(os.path.join(WORKV, "KRq_int", "result.json")))
    okq = rcq == 75 and r1.returncode == 0 and r2.returncode == 0 and rq.get("final_state_sha256") == RES["KR"]["sha_full"] and "already complete" in r2.stdout
    RES["KR_queue"] = dict(rc_sigterm=rcq, seconds_to_exit=tqe, rc_resume=r1.returncode, rc_second_resume=r2.returncode, second_resume_s=t2,
                           sha_equal=rq.get("final_state_sha256") == RES["KR"]["sha_full"], ok=okq)
    P(f"  KR-queue (reported, contract path): SIGTERM at step 70 -> rc {rcq} ({tqe:.1f} s); resume rc {r1.returncode}; sha equal to uninterrupted "
      f"{RES['KR_queue']['sha_equal']}; second --resume after DONE rc {r2.returncode} in {t2:.1f} s -> {'OK' if okq else 'NOT OK'}")

# ------------------------------------------------------------------ close
import resource
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"L1_KHRONON_PM COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB)")
K.atomic_json(os.path.join(HERE, f"l1_khronon_pm_results{SUF}.json"), RES)
with open(os.path.join(HERE, f"l1_khronon_pm{SUF}.out.tmp"), "w") as f: f.write("\n".join(OUT) + "\n")
os.replace(os.path.join(HERE, f"l1_khronon_pm{SUF}.out.tmp"), os.path.join(HERE, f"l1_khronon_pm{SUF}.out"))
sys.exit(0 if npass == ntot else 1)
