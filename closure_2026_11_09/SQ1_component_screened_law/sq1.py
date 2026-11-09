#!/usr/bin/env python3
"""SQ1 (FROZEN_CRITERIA.md 7e8fa69c63): variant Q, component-screened law. Q1 depletion dynamics (spherical shells, sign G graded,
R reported), KiDS / SPARC (readings G and C), groups / X-COP (f_ret rule, local S), Q2 volume filling (Boolean spheres, P_2p, S8),
Q3 / Q4 reported, Bullet (screened, galaxy-traced Newtonian via PD1 A2's child), KA-S1..S4, MUTATE MS1 / MS2.
    python3 sq1.py   -> sq1.json / sq1.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PD1 = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust")
CRIT = "7e8fa69c63"; T0 = time.time(); L = []
def P(s): print(s, flush=True); L.append(str(s))
src = open(os.path.join(PD1, "pd1.py")).read(); ns = {"__file__": os.path.join(PD1, "pd1.py"), "__name__": "pd1_lib"}
exec(compile(src[:src.index("# ---------------- run")], "pd1_prefix", "exec"), ns)
np, G, MS, KPC, MPC, glaw, A0, FOOTS, C = ns["np"], ns["G"], ns["MS"], ns["KPC"], ns["MPC"], ns["glaw"], ns["A0"], ns["FOOTS"], ns["C"]
footing_bg, gsmf, LE, GALS, PRE, XC, GR, R500X, Q8, G_KPC, TR1 = ns["footing_bg"], ns["gsmf"], ns["LE"], ns["GALS"], ns["PRE"], ns["XC"], ns["GR"], ns["R500X"], ns["Q8"], ns["G_KPC"], ns["TR1"]
from scipy.integrate import solve_ivp
CL = 2.99792458e8; VST = {"canonical": 265.8, "alt": 288.1}; F_CAP = 0.76
def nu(y): y = np.maximum(np.asarray(y, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def rho_s(B, f): return A0[f] * B.H0s / (2 * math.pi * G * CL)
def S_of(x): return 1.0 / (1.0 + np.asarray(x, float) ** 2)
RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
# ---------------- KA-S1, KA-S4
for f in FOOTS:
    B = footing_bg(f); r1 = rho_s(B, f) / B.RHOC; r2 = 4 * A0[f] / (3 * CL * B.H0s); x0 = B.RHO_D0 / rho_s(B, f)
    RES.setdefault(f, {})["screen"] = dict(rho_screen_over_rho_crit=r1, closed=r2, KA_S1=bool(abs(r1 / r2 - 1) < 1e-12), x0_mean_today=x0, S_mean_today=float(S_of(x0)))
    P(f"[{f}] rho_screen / rho_crit {r1:.4f} (4 a0/3cH0 {r2:.4f}; KA-S1 {'PASS' if abs(r1/r2-1)<1e-12 else 'FAIL'}); mean component today x0 {x0:.3f}, S(mean) {float(S_of(x0)):.3f}")
yy = 1e-6; Fp = 2 * yy * (float(nu(yy)) - 1); RES["KA_S4"] = dict(ratio=Fp / (2 * yy ** 0.5), pass_=bool(abs(Fp / (2 * yy ** 0.5) - 1) < 1e-3))
P(f"KA-S4 F'(y) = 2y(nu-1) vs deep 2 sqrt(y) at y 1e-6: ratio {RES['KA_S4']['ratio']:.5f}")
# ---------------- Q1 shells
def shells(B, f, Mb_sun, sign, force_on=True, N=120, qmax=8.0, rs_mult=1.0, soft_kpc=50.0):
    """Lagrangian comoving radii q 0.2..qmax Mpc; central excess M_b (1 + R) (galaxy + its collapsed share), softened at soft_kpc
    (first run void: the unsoftened inner shells collapsed onto the point mass and the integrator stalled; disclosed in RESULT).
    Component force a = sign |S'(rho)| (a0^2 / 2 pi G) y^2 (nu - 1) / r, y = G M_b / (r^2 a0), rho = the shell's own density."""
    a0 = A0[f]; rs = rho_s(B, f) * rs_mult; q = np.geomspace(0.2, qmax, N) * MPC; Mb = Mb_sun * MS; dM = Mb * (1 + B.R); eps = soft_kpc * KPC
    Mbg = B.RHO_M0 * 4 * math.pi / 3 * q ** 3; rhoL = B.RHO_D0          # background mass inside each shell; softened comovingly with the excess
    ai = 1 / 1001.0; Y0 = np.concatenate([ai * q, B.Hs(ai) * ai * q, [ai]])
    def rhs(t, Y):
        a = Y[-1]; r = Y[:N]; v = Y[N:2 * N]; r2 = r * r + (a * eps) ** 2                 # comoving softening (a x soft_kpc): far shells exact, inner shells regular
        acc = -G * (Mbg + dM) * r / r2 ** 1.5 + (8 * math.pi * G / 3) * B.OL * B.RHOC * r - (8 * math.pi * G / 3) * B.Orr * B.RHOC / a ** 4 * r      # radiation, as WL1's shell (KA-S3)
        if force_on:
            dr = np.gradient(r, q); rho = rhoL * q ** 2 / np.maximum(r2 * np.abs(dr), 1e-300); x = rho / rs
            Sp = 2 * x / (rs * (1 + x * x) ** 2); rr = np.sqrt(r2); y = G * Mb / (r2 * a0)
            acc = acc + sign * Sp * (a0 ** 2 / (2 * math.pi * G)) * y ** 2 * (nu(y) - 1) / rr * np.sign(r)
        return np.concatenate([v, acc, [a * B.Hs(a)]])
    def end(t, Y): return Y[-1] - 1.0
    end.terminal = True
    so = solve_ivp(rhs, (0, 1e19), Y0, events=end, rtol=1e-7, atol=np.concatenate([np.full(N, 1e3), np.full(N, 1e-6), [1e-12]]), method="DOP853", max_step=2e15)
    Yf = so.y_events[0][0] if so.t_events[0].size else so.y[:, -1]; r = np.abs(Yf[:N]); v = Yf[N:2 * N]
    inside = r < 3 * MPC; dMs = np.diff(np.concatenate([[(rhoL * 4 * math.pi / 3 * (0.2 * MPC) ** 3)], rhoL * 4 * math.pi / 3 * q ** 3]))
    Mchi_in = B.R * Mb + rhoL * 4 * math.pi / 3 * (0.2 * MPC) ** 3 + float(np.sum(dMs[inside]))
    dens = Mchi_in / (4 * math.pi / 3 * (3 * MPC) ** 3); cross = bool(np.any(np.diff(r) <= 0))
    j = np.where(v < 0)[0]; rta = float(np.interp(0.0, [v[j[-1]], v[j[-1] + 1]], [r[j[-1]], r[j[-1] + 1]])) if (len(j) and j[-1] + 1 < N) else float("nan")
    return dict(density_in_3Mpc_over_rho_screen=dens / rho_s(B, f), shell_crossing=cross, r_turnaround_Mpc=rta / MPC, success=bool(so.success and so.t_events[0].size), message=str(so.message), a_end=float(Yf[-1]),
                displacement_at_q1Mpc_kpc=float(np.interp(1.0, q / MPC, (r - q) / KPC)), r_final_of_q3Mpc_Mpc=float(np.interp(3.0, q / MPC, r / MPC)))
for f in FOOTS:
    B = footing_bg(f); q1 = {}
    for lm in (10.0, 10.5, 11.0):
        g_ = shells(B, f, 10 ** lm, -1.0); r_ = shells(B, f, 10 ** lm, +1.0); n_ = shells(B, f, 10 ** lm, 0.0, force_on=False)
        q1[f"{lm}"] = dict(G=g_, R=r_, force_off=n_)
        P(f"[{f}] Q1 M_b 1e{lm}: density in 3 Mpc / rho_screen: sign G {g_['density_in_3Mpc_over_rho_screen']:.3f}, sign R {r_['density_in_3Mpc_over_rho_screen']:.3f}, force off {n_['density_in_3Mpc_over_rho_screen']:.3f} (line <= 0.2); "
          f"shell at q 1 Mpc displaced G {g_['displacement_at_q1Mpc_kpc']:.0f} / R {r_['displacement_at_q1Mpc_kpc']:.0f} / off {n_['displacement_at_q1Mpc_kpc']:.0f} kpc; q 3 Mpc ends at G {g_['r_final_of_q3Mpc_Mpc']:.2f} / R {r_['r_final_of_q3Mpc_Mpc']:.2f} / off {n_['r_final_of_q3Mpc_Mpc']:.2f} Mpc; ok {g_['success'] and r_['success'] and n_['success']}  [{time.time()-T0:.0f}s]")
    # KA-S3: force off turnaround vs WL1 / PD1 solver
    rt_off = q1["11.0"]["force_off"]["r_turnaround_Mpc"]; rt_wl1 = B.r_ta(1e11 * MS * (1 + B.R), 0.0)[0] / MPC
    RES[f]["Q1"] = dict(rows=q1, status=("PASS" if all(v["G"]["density_in_3Mpc_over_rho_screen"] <= 0.2 for v in q1.values()) else "FAIL") if all(v[k]["success"] for v in q1.values() for k in ("G", "R", "force_off")) else "NO VERDICT (integration)",
                        KA_S3=dict(r_ta_shells=rt_off, r_ta_WL1=rt_wl1, pass_=bool(abs(rt_off / rt_wl1 - 1) < 0.01)))
    P(f"[{f}] Q1 {RES[f]['Q1']['status']}; KA-S3 force-off turnaround {rt_off:.3f} vs WL1 solver {rt_wl1:.3f} Mpc -> {'PASS' if RES[f]['Q1']['KA_S3']['pass_'] else 'FAIL'}")
# ---------------- local gates
def prim(B, Mb_sun, z=0.55): H = C.halo(Mb_sun, B.R, B.h, B.Om, z=z); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; return H
def rho_SIS(H, r_kpc): return H["fchi"] * H["M200"] / (4 * math.pi * H["R200"] * r_kpc ** 2) * MS / KPC ** 3 if r_kpc < H["R200"] else 0.0
def kids(B, f, reading, rs_mult=1.0):
    a0 = A0[f]; rs = rho_s(B, f) * rs_mult; x0 = B.RHO_D0 / rs; sh = []
    for p in LE:
        Mb = p["Mb"] / MS; R = math.sqrt(G * p["Mb"] / p["gbar"]); rk = R / KPC; gN = p["gbar"]; ph = float(glaw(gN, a0)) - gN
        if reading == "law": g = gN + ph
        elif reading == "G":
            H = prim(B, Mb); rh = rho_SIS(H, rk); x = (rh + (B.RHO_D0 if rk >= H["R200"] else 0.0)) / rs; g = gN + G * float(H["Menc"](rk)) * MS / R ** 2 + float(S_of(x)) * ph
        else:
            Sc = float(S_of(0.2)); defic = -(B.RHO_D0 - 0.2 * rho_s(B, f)) * 4 * math.pi / 3 * min(R, 3 * MPC) ** 3; g = gN + G * defic / R ** 2 + Sc * ph
        sh.append(math.log10(max(g, 1e-300) / float(glaw(gN, a0))))
    sh = np.array(sh); return dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), mean=float(sh.mean()))
def sparc(B, f, reading):
    a0 = A0[f]; rs = rho_s(B, f); rows = []
    for q, Tf in zip(GALS, PRE[f]):
        R = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mbp = np.maximum(np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)), 1e3); g = q["GB"]
        if reading == "law": ge = glaw(g, a0)
        elif reading == "G":
            H = prim(B, float(Mbp[-1])); fk = np.asarray(H["Menc"](R)) / Mbp; x = np.array([rho_SIS(H, r_) for r_ in R]) / rs; Sx = S_of(x)[:, None]
            ge = g * (1 + fk)[:, None] + Sx * (glaw(g, a0) - g)
        else: ge = g + float(S_of(0.2)) * (glaw(g, a0) - g)
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]; return dict(all=pooled(range(len(rows))), massive=pooled(massive))
def fret(u, v, f):
    gp = np.maximum((u / (0.05 + u)) * (1 - 0.42 * u), 1e-12); return (1 / math.sqrt(2)) * np.exp(-(VST[f] / v) ** 2 / gp)
def cluster_sys(B, f, Msys, force_law=False):
    H = prim(B, Msys); v = math.sqrt(G_KPC * H["M500"] / H["R500"]); rg = np.geomspace(1e-3 * H["R500"], H["R200"], 600); dM = H["fchi"] * H["M200"] / H["R200"] * np.gradient(rg)
    fr = fret(rg / H["R500"], v, f); Mc = np.cumsum(dM * fr)
    Mchi = lambda r: float(np.interp(r, rg, Mc, left=0.0, right=Mc[-1])); rho = lambda r: float(np.interp(r, rg, fr)) * rho_SIS(H, r) if r < H["R200"] else 0.0
    return dict(H=H, v_vir=v, Mchi=Mchi, rho=rho, Mchi_R200=float(Mc[-1]))
def cl_g(B, f, S_, r_kpc, Mb_r, force_law=False):
    a0 = A0[f]; rm = r_kpc * KPC; gNb = G * Mb_r * MS / rm ** 2; Sx = 1.0 if force_law else float(S_of(S_["rho"](r_kpc) / rho_s(B, f)))
    return gNb + G * S_["Mchi"](r_kpc) * MS / rm ** 2 + Sx * (float(glaw(gNb, a0)) - gNb), S_["Mchi"](r_kpc), Sx
def xcop(B, f, force_law=False):
    d = []; xr = []; fm = []; sv = []
    for name in R500X:
        pts = [z for z in XC if z["name"] == name]; S_ = cluster_sys(B, f, pts[0]["Mb_last"][0])
        for z in pts:
            g, mc, Sx = cl_g(B, f, S_, z["r_kpc"], z["M_b"], force_law); rm = z["r_kpc"] * KPC; d.append(math.log10(z["M_obs"] / (g * rm ** 2 / G / MS))); xr.append(z["r_kpc"] / R500X[name]); fm.append(mc / z["M_obs"]); sv.append(Sx)
    d, xr, fm, sv = map(np.array, (d, xr, fm, sv)); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
    for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None, f_miss=float(np.median(fm[m])) if m.sum() else None, S_median=float(np.median(sv[m])) if m.sum() else None, TR1=TR1[b_]))
    amp = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; ok = all(b["within"] for b in bins if b["graded"])
    return dict(status="PASS" if (amp and ok) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), bins=bins)
def groups(B, f, force_law=False):
    o = {}
    for fst in (0, 1):
        npass = 0; med = []; sv = []; vv = []
        for gp in GR:
            S_ = cluster_sys(B, f, gp["g5"] * (1 + fst)); vv.append(S_["v_vir"]); ok = True
            for p in gp["pts"]:
                g, mc, Sx = cl_g(B, f, S_, p["r_kpc"], p["M_gas"] * (1 + fst), force_law); rm = p["r_kpc"] * KPC; dl = math.log10(p["M_obs"] / (g * rm ** 2 / G / MS)); med.append(dl); sv.append(Sx); ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
            npass += ok
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)), S_median=float(np.median(sv)), v_vir_median=float(np.median(vv)))
    return dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
for f in FOOTS:
    B = footing_bg(f); r = RES[f]; base = sparc(B, f, "law")
    st = lambda s: "PASS" if (s["all"]["rms"] <= base["all"]["rms"] + 0.010 and abs(s["all"]["mean"]) <= 0.05 and s["massive"]["rms"] <= base["massive"]["rms"] + 0.010 and abs(s["massive"]["mean"]) <= 0.05) else "FAIL"
    kG, kC, kL, k10 = kids(B, f, "G"), kids(B, f, "C"), kids(B, f, "law"), kids(B, f, "G", 10.0); sG, sC = sparc(B, f, "G"), sparc(B, f, "C"); sG["status"], sC["status"] = st(sG), st(sC)
    xg, gg = xcop(B, f), groups(B, f); xl = xcop(B, f, True)
    r.update(KiDS=dict(G=kG, C=kC), SPARC=dict(G=sG, C=sC, L0=base), groups=gg, XCOP=xg, KA_S2=dict(kids_law=kL["max_abs"], xcop_law_no_component=None), MS1_rho_screen_x10=dict(kids_G=k10))
    P(f"[{f}] KiDS G {kG['status']} max {kG['max_abs']:.3f} ({kG['n_over']}/59, mean {kG['mean']:+.3f}); C {kC['status']} max {kC['max_abs']:.3f}; KA-S2 law {kL['max_abs']:.1e}; MS1 rho_screen x10: G max {k10['max_abs']:.3f}")
    P(f"[{f}] SPARC G {sG['status']} rms {sG['all']['rms']:.4f} (line {base['all']['rms']+0.010:.4f}); C {sC['status']} rms {sC['all']['rms']:.4f}")
    P(f"[{f}] groups {gg['status']} {gg['fst0']['n_pass']}/{gg['fst1']['n_pass']} med {gg['fst0']['median_res']:+.2f}/{gg['fst1']['median_res']:+.2f} (S med {gg['fst0']['S_median']:.2f}, v_vir med {gg['fst0']['v_vir_median']:.0f}); X-COP {xg['status']} {xg['mean']:+.3f}/{xg['rms']:.3f} bins "
      + " ".join(f"{b['mean']:+.2f} (f_miss {b['f_miss']:.2f}, S {b['S_median']:.1e}, TR1 {b['TR1']})" for b in xg['bins'] if b['graded']))
# ---------------- Q2 volume filling (reading C)
from classy import Class
for f in FOOTS:
    B = footing_bg(f); rs = rho_s(B, f); per = gsmf(B.h); LFg = np.arange(10.0, 12.0001, 0.01); n = float(np.trapz([per(m) for m in LFg], LFg))
    Rd = 3.0; V = 4 * math.pi / 3 * Rd ** 3; p_unc = math.exp(-n * V); fV = 1 - p_unc; rb = B.RHO_D0
    rho_lo = 0.2 * rs; rho_hi = (rb - rho_lo * fV) / p_unc; disp = fV * (rb - rho_lo) / rb; A = (rho_hi - rho_lo) / rb
    rr = np.linspace(1e-4, 2 * Rd, 4000); Vx = (math.pi / 12) * (4 * Rd + rr) * (2 * Rd - rr) ** 2; Cr = math.exp(-2 * n * V) * (np.exp(n * Vx) - 1)
    ka = abs(Cr[0] / (p_unc * (1 - p_unc)) - 1)
    def P2(kh): k = kh * B.h; return A ** 2 * float(np.trapz(Cr * 4 * math.pi * rr ** 2 * np.sinc(k * rr / math.pi), rr))
    M = Class(); M.set({'output': 'mPk', 'h': B.h, 'omega_b': B.OB, 'omega_cdm': B.OD, 'A_s': 2.1e-9, 'n_s': 0.9674, 'N_ur': 3.046, 'P_k_max_1/Mpc': 10.0}); M.compute()
    s8_ref = float(M.sigma8()); A_s = 2.1e-9 * (0.8 / s8_ref) ** 2                               # normalisation only for the ratio table (disclosed)
    kk = np.geomspace(1e-3, 8.0, 800); W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; R8 = 8 / B.h
    Pref = np.array([M.pk_lin(k, 0.0) for k in kk]); P2k = np.array([P2(k / B.h) for k in kk])
    s8r = math.sqrt(np.trapz(Pref * W(kk * R8) ** 2 * kk ** 3 / (2 * math.pi ** 2), np.log(kk))); s2p = math.sqrt(np.trapz(P2k * W(kk * R8) ** 2 * kk ** 3 / (2 * math.pi ** 2), np.log(kk)))
    fc = B.OD / (B.OB + B.OD); s8n = math.sqrt(s8r ** 2 + (fc * s2p) ** 2); chg = s8n / s8r - 1
    tab = {f"k {kh} h/Mpc": float(P2(kh) * fc ** 2 / M.pk_lin(kh * B.h, 0.0)) for kh in (0.3, 1.0, 3.0)}; M.struct_cleanup(); M.empty()
    RES[f]["Q2"] = dict(n_Mstar_gt_1e10=n, f_V=fV, displaced_fraction=disp, rho_hi_over_mean=rho_hi / rb, S_complement=float(S_of(rho_hi / rs)), sigma8_ref=s8r, sigma_2p_8=s2p, S8_change=chg,
                        status="PASS" if abs(chg) <= 2 * 0.0225 / 0.759 else "FAIL", P2p_over_Pref=tab, KA_C0=float(ka))
    P(f"[{f}] Q2 n(M*>1e10) {n:.4f} /Mpc^3, f_V {fV:.3f}; displaced {100*disp:.0f} % of the component into {100*p_unc:.0f} % of space at {rho_hi/rb:.2f} x mean (S there {float(S_of(rho_hi/rs)):.3f}); sigma_2p(8) {s2p:.3f} vs sigma8 {s8r:.3f} -> S8 {100*chg:+.1f} % -> {RES[f]['Q2']['status']}; P_2p/P_ref " + " ".join(f"{k}:{v:.3g}" for k, v in tab.items()) + f"; KA C(0) {ka:.1e}")
# ---------------- Q3, Q4
for f in FOOTS:
    B = footing_bg(f); rs = rho_s(B, f); x0 = B.RHO_D0 / rs; Mh = 3.76e12; Hu = C.halo(Mh / (1 + F_CAP * B.R), B.R, B.h, B.Om, M200=Mh, Mchi=Mh * F_CAP * B.R / (1 + F_CAP * B.R), z=0.0)
    vh = math.sqrt(G_KPC * Mh / Hu["R200"]); rho15 = Mh * B.R / (1 + B.R) * MS / (4 * math.pi / 3 * (1.5 * MPC) ** 3)
    RES[f]["Q3"] = dict(UMa_host_M200=Mh, v_vir=vh, depleted_under_C=bool(vh < VST[f]), S_at_host_mean_density_G=float(S_of(rho15 / rs)))
    RES[f]["Q4"] = {f"z {z}": dict(S_mean=float(S_of(x0 * (1 + z) ** 3)), S_depleted_C=float(S_of(0.2))) for z in (0.0, 0.3, 0.5, 1.0, 1.5)}
    P(f"[{f}] Q3 UMa host v_vir {vh:.0f} km/s (v_stiff {VST[f]}): C depletes it {vh < VST[f]}; G: S at host mean density in 1.5 Mpc {RES[f]['Q3']['S_at_host_mean_density_G']:.3f}. Q4 S(mean) " + " ".join(f"{k} {v['S_mean']:.3f}" for k, v in RES[f]['Q4'].items()))
# ---------------- Bullet (screened, Newtonian + retained component, galaxy-traced)
def call(arg):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(PD1, "pd1_a2.py"), "nchild", arg, "newton"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("PD1CHILD ")]
    if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
    return json.loads(line[0][9:])
o0 = call("{}"); mm = o0["masses"]; Mb = [mm["M_gas_sub"][j] + mm["M_star_sub"][j] for j in range(2)]; Md = {}
for f in FOOTS: B = footing_bg(f); Md[f] = [cluster_sys(B, f, Mb[j])["Mchi_R200"] for j in range(2)]
on = call(json.dumps(Md))
for f in FOOTS:
    b = on[f]["row"]; RES[f]["Bullet"] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, retained=Md[f])
    P(f"[{f}] Bullet (screened, galaxy-traced Newtonian) {b['label']}: cls {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; retained component in R200 " + ", ".join(f"{x:.2e}" for x in Md[f]))
json.dump(RES, open(os.path.join(HERE, "sq1.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "sq1.out"), "w").write("\n".join(L) + "\n")
P(f"done {time.time()-T0:.0f} s")
