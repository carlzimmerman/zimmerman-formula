#!/usr/bin/env python3
"""DF3_fluid_next_gates, discs, clusters, MW, lensing. Modes: law | cell G SIG [S] | selfcheck | mutate. CRG1's and HF1's code read-only, patched in memory; reading N and S. Adopts nothing, reinstates nothing. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys
os.environ["OMP_NUM_THREADS"] = "1"; os.nice(19); sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); HF = os.path.join(RB, "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.path.insert(0, HERE)
_a = sys.argv[:]; sys.argv = ["hf1_g23.py"]
import hf1_g23 as H
sys.argv = _a
import numpy as np, df3g_solver as S
_CA = os.environ.get("DF3G_CACHE", "cache_k2"); os.makedirs(os.path.join(HERE, _CA), exist_ok=True); H.CO.CACHE = os.path.join(HERE, _CA); H.FM.solve = S.solve
C, CO, GR, DW, SP = H.C, H.CO, H.GR, H.DW, H.SP; A0 = H.A0; FEET = H.FEET; MSUN = H.MSUN; GF = H.GF; MPC = H.MPC; lw = S.law
DF2 = os.path.join(RB, "DF2_dark_fluid_requirement", "cells"); KPC = 3.0857e19; REC = {}
def rf_of(gam, sig):
    p = json.load(open(os.path.join(DF2, f"P_G{gam:.3f}_s{sig:g}_fit.json")))["params"]; return p["omega_c"] / p["omega_b"]
def setc(gam, sig, rd="N", noeq="H"): S.Cfg.gamma = gam; S.Cfg.sigma = sig * 1e3; S.Cfg.K = 1.0; S.Cfg.reading = rd; S.Cfg.noeq = noeq
def gt(gb, gf, a0): return lw(gb, a0) + gf if S.Cfg.reading == "N" else lw(gb + gf, a0)
def cnt(fn):
    S.STAT.update(rows=0, noeq=0, unres=0); v = fn(); return v, S.STAT["noeq"] / max(S.STAT["rows"], 1)
# ---- patched rows: only g's combination of baryons and fluid differs from HF1's
def build_keys(D, CSS, h, Rf, m, fs, gd, foot, gf=2.0, capf=1.0, info=None):
    a0 = A0[foot]; V = np.zeros((D.N, C.N_BIN)); vC = np.zeros((D.N, C.N_BIN)); g_ = D.geo[h]; gas = 10 ** gd; CS = CSS["own_" + foot]; RM = C.RM
    for i in range(D.N):
        z = D.z[i]; q = g_["q"][i]; c = C.ctx_of(D, h, i); Mg = D.Mgas[i] * q ** 2.5 * gas; Rp = D.R500[i] * q; Mbx, Mb, Mbt, rta = C.chain(Mg, Rp, fs, z, MSUN); Mf, s = H.cluster_fermion(RM, Mb, Mbt, rta, Rp, Rf, m, a0, gf, capf)
        if S.Cfg.reading == "N":
            Msrc = Mb.copy(); pos = Mb > 0; Msrc[pos] = Mb[pos] * CO.nu(GF * Mb[pos] / RM[pos] ** 2 / a0); Msrc = Msrc + soften(Mf, RM)
        else:
            Mt = Mb + Mf; Msrc = Mt.copy(); pos = Mt > 0; Msrc[pos] = Mt[pos] * CO.nu(GF * Mt[pos] / RM[pos] ** 2 / a0)
        V[i] = C.vec(Msrc, c); vC[i] = C.vec(C.m_cstar(Mb, a0, CS), c)
    return V, vC, 0
H.build_keys = build_keys
def soften(Mf, RM, rs=20 * KPC, a=8 * KPC):
    """A2: the keys harness takes density from dM/dr from 1 kpc out, so mass inside its inner edge is lost, and its log-interpolated projection under-counts profiles narrower than about 8 kpc. Mass inside 20 kpc is redistributed as a Plummer of 8 kpc, which leaves M_2D(<R) and Sigma(R) unchanged at R >= 20 kpc, where the keys are measured."""
    M5 = float(np.interp(rs, RM, Mf)); pl = lambda r: r ** 3 / (r * r + a * a) ** 1.5; o = Mf.copy(); w = RM < rs; o[w] = M5 * pl(RM[w]) / pl(rs); return o
def gal_model(g, gb, Y, Rf, m, a0, gf=2.0, capf=1.0, Rsig=None, info=None):
    rg = H.gal_grid(g); Mt = (Y * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MSUN; Mb = H.gal_masses(g, gb, Mt, rg); Mtot = np.maximum(Mb[:, -1], Mt); rta = np.array([H.RTA(x) for x in Mtot]); s = S.solve(rg, Mb, rta, g["R"][-1], Rf * Mtot, a0=a0)
    i0 = np.clip(np.searchsorted(np.log(rg), np.log(g["R"])), 1, rg.size - 1); dl = math.log(rg[1] / rg[0]); t = (np.log(g["R"]) - np.log(rg[i0 - 1])) / dl; Mfr = s["Mf"][:, i0 - 1] * (1 - t) + s["Mf"][:, i0] * t
    return gt(gb, GF * Mfr / g["R"] ** 2, a0), Mfr
H.gal_model = gal_model
def xcop(XC, Rf, foot, fs=0.034):
    a0 = A0[foot]; RM = C.RM; rows = []; E = CO.E; val = []
    for j, c in enumerate(XC):
        Mg = C.li(c["gr"], c["gm"], c["R500"]); Rp = c["R500"] / 1e3; Mbx, Mb, Mbt, rta = C.chain(Mg, Rp, fs, c["z"], E.Msun, seed=3 * 1.2 * Mg * E.Msun); Mf, s = H.cluster_fermion(RM, Mb, Mbt, rta, Rp, Rf, 11.0, a0)
        val.append(dict(name=c["name"], gm=float(s["gmrc2"]), csc=float(s["csc"]), rhalf_kpc=float(s["rhalf"]) / KPC, noeq=bool(s["noeq"]), fair=float(Rf * Mbt / E.Msun), held=float(s["held"] / E.Msun)))
        for x in C.XS:
            r = x * c["R500"]; mh, mg, ms = C.li(c["hr"], c["hm"], r), C.li(c["gr"], c["gm"], r), C.li(c["sr"], c["sm"], r)
            if not all(map(np.isfinite, (mh, mg, ms))): continue
            rm = r * 1e3 * E.pc; mf = float(np.interp(rm, RM, Mf)) / E.Msun; gb = E.G * (mg + ms) * E.Msun / rm ** 2; gf = E.G * mf * E.Msun / rm ** 2; Mm = float(gt(np.array(gb), np.array(gf), a0)) * rm ** 2 / E.G / E.Msun
            rows.append(dict(c=c["name"], j=j, x=x, d=math.log10(mh / Mm), mf=mf, mb=mg + ms))
    d = np.array([q["d"] for q in rows]); mean = float(d.mean()); rms = float(np.sqrt((d ** 2).mean()))
    return dict(mean=mean, rms=rms, passed=bool(abs(mean) <= .05 and rms <= .10), hse_clear=bool(abs(mean) > .05 + .12), by_x={str(x): float(np.mean([q["d"] for q in rows if q["x"] == x])) for x in C.XS}, mfmb={str(x): float(np.median([q["mf"] / q["mb"] for q in rows if q["x"] == x])) for x in C.XS}, valid=val)
def lt_row(x, Rf, a0):
    Mb = x["Mb"] * CO.E.Msun; R = x["R"]; rta = H.RTA(Mb); r = np.geomspace(1e-3 * R, max(rta, 2 * R), 300); Mg = Mb * np.minimum(r / R, 1) ** 2; s = S.solve(r, Mg, rta, R, Rf * Mb, a0=a0); mf = float(np.interp(math.log(R), np.log(r), s["Mf"]))
    return math.log10(x["V"] ** 2 / R) - math.log10(float(gt(np.array(CO.E.G * Mb / R ** 2), np.array(CO.E.G * mf / R ** 2), a0)))
def groups(rows, Rf, a0):
    P_ = GR.P; XG = GR.XG; LX = GR.LX; RH = GR.RHO_H; MH = GR.M_H
    def ls(lM, Re, dl):
        a = Re * (P_.pc * 1e3) / 1.8153; Mb = 10 ** (lM + dl) * P_.Msun; rr = XG * a; rta = H.RTA(Mb); r = np.geomspace(1e-3 * a, max(rta, 4 * a), 300); Mg = Mb * np.interp(np.log(r), LX + math.log(a), MH); s = S.solve(r, Mg, rta, 3 * a, Rf * Mb, a0=a0); mf = np.interp(np.log(rr), np.log(r), s["Mf"], left=0.0); U = P_.G * Mb / a ** 2; gtt = gt(Mb * MH * P_.G / rr ** 2, mf * P_.G / rr ** 2, a0) / U
        return .5 * math.log10(np.trapz(4 * math.pi * XG ** 2 * RH * XG * gtt * XG, LX) / 3 * P_.G * Mb / a) - 3
    d = np.array([x[0] - ls(x[1], x[2], 0.0) for x in rows]); sl = np.array([(ls(x[1], x[2], .01) - ls(x[1], x[2], -.01)) / .02 for x in rows]); mean = d.mean(); se = d.std(ddof=1) / math.sqrt(len(d)); sy = .10 * sl.mean(); tot = math.hypot(se, sy); Z = mean / tot
    return dict(Z=float(Z), cls="NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW")))
def dwarfs(rows, Rf, a0):
    Ev = []
    for q in rows:
        Ms = 10 ** q["lgMs"] * CO.D.Msun; r12 = q["r12"]; rta = H.RTA(Ms); r = np.geomspace(1e-3 * r12, max(rta, 3 * r12), 200); Mg = np.minimum(Ms / 2 * (r / r12) ** 2, Ms); s = S.solve(r, Mg, rta, r12, Rf * Ms, a0=a0); mf = float(np.interp(math.log(r12), np.log(r), s["Mf"])); Ev.append(math.log10(q["gobs"] / float(gt(np.array(q["gN"]), np.array(CO.D.G * mf / r12 ** 2), a0))))
    return DW.boot(rows, np.array(Ev))
# ---- D2 exclusion + Jeans, Upsilon 0.5, V_flat bins
GAMN = {"canonical": {(150, 200): (-0.23, 0.17), (200, 250): (0.09, 0.25)}, "alt": {(150, 200): (-0.45, 0.16), (200, 250): (-0.05, 0.22)}}
TB = {}
for l in open(os.path.join(CO.INP, "sparc", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) == 19:
        try: TB[t[0]] = float(t[11])
        except ValueError: pass
BINS = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]
def disc_rows(G, Rf, foot):
    a0 = A0[foot]; rows = []
    for g in G:
        V = g["Vflat"]
        if not (g["Q"] <= 2 and g["Inc"] >= 30 and V > 0) or g["name"] not in TB: continue
        VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = np.maximum(VB2 * 1e6 / g["R"], 1e-30)[None, :]; rg = H.gal_grid(g); Mt = (np.array([0.5]) * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MSUN; Mb = H.gal_masses(g, gb, Mt, rg); Mtot = np.maximum(Mb[:, -1], Mt); rta = np.array([H.RTA(x) for x in Mtot]); s = S.solve(rg, Mb, rta, g["R"][-1], Rf * Mtot, a0=a0)
        R = g["R"]; n3 = max(1, len(R) // 3); oi = np.arange(len(R) - n3, len(R)); Mf = np.exp(np.interp(np.log(R[oi]), np.log(rg), np.log(np.maximum(s["Mf"][0], 1e-300)))); Mbr = gb[0, oi] * R[oi] ** 2 / GF; Rd = TB[g["name"]] * KPC; lam = []
        for rr in (Rd, 2 * Rd, R[-1]):
            ro = math.exp(np.interp(math.log(rr), np.log(rg), np.log(np.maximum(s["rho"][0], 1e-300)))); cs = float(S.cs_of(ro)); lam.append(dict(rho=ro / S.RHO_A * .05, cs=cs / 1e3, lamJ_over_Rd=cs * math.sqrt(math.pi / (S.G * max(ro, 1e-300))) / Rd))
        rows.append(dict(V=float(V), gamma=float(np.median(Mf / np.maximum(Mbr, 1e-300))), noeq=bool(s["noeq"][0]), retained=float(s["held"][0] / (Rf * Mtot[0])), rhalf_RL=float(s["rhalf"][0]) / float(R[-1]), gm=float(s["gmrc2"][0]), csc=float(s["csc"][0]), lam=lam))
    out = {}
    for lo, hi in BINS:
        q = [r for r in rows if lo <= r["V"] < hi]
        if not q: continue
        ga = [r["gamma"] for r in q]; b = dict(n=len(q), gamma=float(np.median(ga)), noeq=float(np.mean([r["noeq"] for r in q])), retained=float(np.median([r["retained"] for r in q])), rhalf_RL=float(np.median([r["rhalf_RL"] for r in q])), gm=float(np.median([r["gm"] for r in q])), csc=float(np.median([r["csc"] for r in q])), lam={str(i): {k: float(np.median([r["lam"][i][k] for r in q])) for k in ("rho", "cs", "lamJ_over_Rd")} for i in range(3)})
        if (lo, hi) in GAMN[foot]: b["Z"] = (b["gamma"] - GAMN[foot][(lo, hi)][0]) / GAMN[foot][(lo, hi)][1]; b["ok"] = bool(b["Z"] <= 2)
        out[f"{lo}-{hi}"] = b
    return out
# ---- Milky Way, X5's law cells plus the fluid, reading N only
def mw(Rf, foot):
    if S.Cfg.reading != "N": return dict(status="NOT COMPUTED, S isn't additive on X5's stored law")
    J = json.load(open(os.path.join(RB, "X5_mw_joint_baryons", f"x5_grid_{foot}.json"))); P4 = json.load(open(os.path.join(RB, "X5_mw_joint_baryons", "x5_mw_joint_baryons_results.json")))["step0_P4"][foot]["mine"]; a0 = A0[foot]; T = MW_T; line = J["line_chi2"]; vE, eE = J["vc_target"]; Mgas = J["family"]["M_gas"]; res = []; KU = 2 * math.pi * 4.30091e-6 * 1e6
    def fluid(Mth, Mtk, Mbb, Rd):
        rk = np.geomspace(.05, 2000, 300); x = rk / Rd; dsk = lambda u: 1 - (1 + u) * np.exp(-u); Mbr = (Mth + Mtk) * dsk(x) + Mbb * (rk / (rk + .5)) ** 2 + Mgas * dsk(x / 2); Mbt = Mth + Mtk + Mbb + Mgas; rta = H.RTA(Mbt * MSUN); s = S.solve(rk * KPC, Mbr * MSUN, rta, 8.0 * KPC, Rf * Mbt * MSUN, a0=a0); return rk, s["Mf"] / MSUN, s
    def add(c, law):
        rk, Mf, s = fluid(*c); gh = lambda r: 4.30091e-6 * np.interp(np.log(np.asarray(r, float)), np.log(rk), Mf) / np.asarray(r, float) ** 2; r00 = math.hypot(T["R0"], 1.1); K0 = law["K_R0"] + float(gh(r00)) * 1.1 / r00 / KU; vc = math.sqrt(law["vc_R0"] ** 2 + T["R0"] * float(gh(T["R0"]))); cK = None
        if "K" in law: Kk = np.asarray(law["K"]) + gh(np.hypot(T["BR_R"], 1.1)) * 1.1 / np.hypot(T["BR_R"], 1.1) / KU; cK = float(np.sum(((Kk - T["BR_K"]) / T["BR_E5"]) ** 2))
        rho0 = float(np.exp(np.interp(math.log(T["R0"] * KPC), np.log(rk * KPC), np.log(np.maximum(s["rho"], 1e-300))))) / S.RHO_A * .05
        return dict(vc=vc, K0=K0, cK=cK, noeq=bool(s["noeq"]), rho0=rho0, Mf8=float(np.interp(math.log(8.0), np.log(rk), Mf)), L1=bool(abs(vc - vE) <= 2 * eE), L2a=None if cK is None else bool(cK <= line), L2b=bool(abs(K0 - 66.4) <= 2 * 2.2))
    for c in J["cells"]:
        p = c["params"]; res.append(add((p["M_thin"], p["M_thick"], p["M_bb"], p["Rd"]), c["L24"]))
    M_ = add((3.5e10, 1.5e10, 9.0e9, 2.5), P4); M_["note"] = "McMillan-like total, thin and thick split by hand, Mb 6.6e10"; K = [r for r in res if r["L1"] and r["L2a"]]; A = [r for r in K if r["L2b"]]
    return dict(mcmillan=M_, n_cells=len(res), n_vc_kz=len(K), n_all=len(A), n_noeq=sum(r["noeq"] for r in res), best_D=min(max(abs(r["vc"] - vE) / (2 * eE), r["cK"] / line, abs(r["K0"] - 66.4) / 4.4) for r in res), med_vc=float(np.median([r["vc"] for r in res])), med_K0=float(np.median([r["K0"] for r in res])), med_rho0=float(np.median([r["rho0"] for r in res])), Ou="NOT COMPUTED, A1")
# ---- galaxy lensing, BL1's A at window mid g_bar 10^-12.6
def lensing(Rf, foot):
    Bl = json.load(open(os.path.join(RB, "BL1_blue_lens_halo_mass", "bl1_results.json")))["k"]["law"][foot]; a0 = A0[foot]; gm = 10 ** -12.6; gl = float(lw(np.array(gm), a0)); o = {}
    for lg, a_k, col in ((10.5, 4.0, "blue"), (11.0, 6.0, "red")):
        Mb = 10 ** lg * MSUN; r0 = math.sqrt(S.G * Mb / gm); rta = H.RTA(Mb); r = np.geomspace(.01 * KPC, max(rta, 2 * r0), 300); s = S.solve(r, Mb * (r / (r + a_k * KPC)) ** 2, rta, r0, Rf * Mb, a0=a0); mf = float(np.interp(math.log(r0), np.log(r), s["Mf"])); Ga = mf / Mb; Am = float(gt(np.array(gm), np.array(gm * Ga), a0)) / gl; Aob = Bl[col]["A"]; se = Bl[col]["sA"]; o[col] = dict(lgMb=lg, r_kpc=r0 / KPC, Gamma=Ga, A_model=Am, A_obs=Aob, sA=se, Z=(Am - Aob) / se, Z_law=(1 - Aob) / se, noeq=bool(s["noeq"]), ok=bool(abs(Am - Aob) / se <= 2))
    return o
# ---- one class pass
def g3(G, LT, gr, Rf, f, quick=False):
    a0 = A0[f]; (r, t, _), ne = cnt(lambda: H.sparc_fit(G, Rf, 11.0, a0)); w = dict(rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"], sparc_noeq=ne); g_, ng = cnt(lambda: groups(gr, Rf, a0)); w.update(groups=g_["Z"], groups_cls=g_["cls"], groups_noeq=ng); w["S"] = bool(r["rms"] <= .110 and .50 <= r["Y_med"] <= .80); w["Tl"] = bool(abs(t["tilt"]) <= .15); w["G"] = g_["cls"] == "CONSISTENT"
    if not quick:
        h_ = H.hs_slope(G, Rf, 11.0, a0); lt, nl = cnt(lambda: [lt_row(x, Rf, a0) for x in LT]); E_ = np.array(lt); ic = float(E_[[i for i, x in enumerate(LT) if x["name"] == "IC 1613"][0]]); d_, nd = cnt(lambda: dwarfs(DW.load(f), Rf, a0)); w.update(hs=h_["Z"], HS=h_["passed"], lt=float(np.median(E_)), LT=bool(abs(np.median(E_)) <= .10), lt_noeq=nl, ic_Z=ic / .075, dwarfs={k: v["Z"] for k, v in d_["classes"].items()}, dw_noeq=nd)
    return w
def keys(D, CSS, Rf, f, tag):
    fac_ = json.load(open(os.path.join(RB, "DA1_definition_audit", "da1_keys.json")))["F"]; GRD = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]); fa = lambda hn: np.interp(D.z, GRD, fac_[hn])[:, None]
    S.STAT.update(rows=0, noeq=0, unres=0); cells = H.keys_all(D, CSS, Rf, 11.0, 0.034, 0.005, f, tag); ne = S.STAT["noeq"] / max(S.STAT["rows"], 1); T = H.k_table(D, cells, f); o = dict(n_pass=T["n_pass"], failing=T["failing"], worst=T["worst"], noeq=ne)
    if f == "canonical":
        for lab, kw in (("B1", dict(B1=True)), ("nz", dict(fac=fa))):
            t = H.k_table(D, cells, f, **kw); o[lab] = dict(n_pass=t["n_pass"], worst=t["worst"])
    return o
def main():
    mode = sys.argv[1]; D, CSS, XC, G, LT = H.load_common(); gr = GR.load(); global MW_T
    x5 = json.load(open(os.path.join(HERE, "mw_targets.json"))); MW_T = dict(R0=x5["R0"], BR_R=np.array(x5["BR_R"]), BR_K=np.array(x5["BR_K"]), BR_E5=np.array(x5["BR_E5"]))
    if mode == "law":
        out = {}
        for f in FEET:
            setc(1.0, 100.0, "N"); x = xcop(XC, 0.0, f); w = g3(G, LT, gr, 0.0, f); k = keys(D, CSS, 0.0, f, "LAW"); l = lensing(0.0, f); J = json.load(open(os.path.join(RB, "X5_mw_joint_baryons", f"x5_grid_{f}.json"))); out[f] = dict(X=x, G3=w, K=k, lens=l, MW=dict(n_pass=J["n_pass"], n_cells=J["n_cells"]))
            print(f, "X", round(x["mean"], 3), round(x["rms"], 3), "SPARC", round(w["rms"], 4), w["Y"], w["tilt"], "K", k["n_pass"], flush=True)
        json.dump(CO.fmt(out), open(os.path.join(HERE, "df3g_law.json"), "w"), indent=1, sort_keys=True, default=float)
    if mode == "selfcheck":
        o = {}
        for gam, sig, ref in ((5 / 3, 100.0, "G1.667_s100"), (1.0, 100.0, "G1.000_s100")):
            setc(gam, sig, "S"); Rf = rf_of(gam, sig); x = xcop(XC, Rf, "canonical"); R = json.load(open(os.path.join(RB, "DF3_barotrope_settling", f"df3_cell_{ref}.json"))); o[ref] = dict(mine=x["mean"], theirs=R["X"]["canonical"]["all"]["mean"], passed=bool(abs(x["mean"] - R["X"]["canonical"]["all"]["mean"]) <= .02)); print(o[ref], flush=True)
        setc(1.0, 100.0, "S"); xS = xcop(XC, 0.0, "canonical"); setc(1.0, 100.0, "N"); xN = xcop(XC, 0.0, "canonical"); o["N_eq_S_off"] = dict(diff=abs(xS["mean"] - xN["mean"]), mean=xN["mean"], rms=xN["rms"], passed=bool(abs(xS["mean"] - xN["mean"]) < 1e-9 and abs(xN["mean"] - .467) <= .01 and abs(xN["rms"] - .476) <= .01)); print(o["N_eq_S_off"], flush=True)
        o["all"] = all(v["passed"] for v in o.values()); json.dump(CO.fmt(o), open(os.path.join(HERE, "df3g_selfcheck.json"), "w"), indent=1, sort_keys=True, default=float)
    if mode == "cell":
        gam = float(eval(sys.argv[2])); sig = float(sys.argv[3]); rd = sys.argv[4] if len(sys.argv) > 4 else "N"; Rf = rf_of(gam, sig); tag = f"G{gam:.3f}_s{sig:g}_{rd}"; R = dict(gamma=gam, sigma=sig, reading=rd, Rf=Rf, X={}, X_noeq={}, XC={}, G3={}, G3C={}, D={}, lens={}, MW={}, K={})
        K_ = sig ** 2 * 1e6 / gam * S.RHO_A ** (1 - gam)
        if abs(gam - 5 / 3) < 1e-6: R["M_TOV_Msun"] = S.tov_max(S.m_of_K(K_)); print("M_TOV", R["M_TOV_Msun"], flush=True)
        for f in FEET:
            setc(gam, sig, rd, "H"); x, ne = cnt(lambda: xcop(XC, Rf, f)); R["X"][f] = x; R["X_noeq"][f] = ne; w = g3(G, LT, gr, Rf, f, quick=rd == "S"); R["G3"][f] = w
            if rd == "N":
                R["D"][f] = disc_rows(G, Rf, f); R["MW"][f] = mw(Rf, f); R["lens"][f] = lensing(Rf, f); R["K"][f] = keys(D, CSS, Rf, f, tag)
                print(f, "D2", {k: (v.get("gamma"), v.get("Z"), v["noeq"]) for k, v in R["D"][f].items() if k in ("150-200", "200-250")}, "MW", R["MW"][f].get("n_all"), "lens", {c: round(v["Z"], 1) for c, v in R["lens"][f].items()}, "K", R["K"][f]["n_pass"], flush=True)
            setc(gam, sig, rd, "C"); R["XC"][f] = xcop(XC, Rf, f); R["G3C"][f] = g3(G, LT, gr, Rf, f, quick=True); setc(gam, sig, rd, "H")
            print(tag, f, "X", round(x["mean"], 3), round(x["rms"], 3), "NE", round(ne, 2), "XC", round(R["XC"][f]["mean"], 3), "SPARC", round(w["rms"], 4), w["Y"], round(w["tilt"], 2), "NE", round(w["sparc_noeq"], 2), "C", round(R["G3C"][f]["rms"], 4), R["G3C"][f]["Y"], flush=True)
        json.dump(CO.fmt(R), open(os.path.join(HERE, f"df3g_cell_{tag}{TAGM}.json"), "w"), indent=1, sort_keys=True, default=float)
    if mode == "keys":
        for g_, s_ in ((1.0, 100.0), (5 / 3, 100.0), (1.0, 30.0), (5 / 3, 30.0), (2 / 3, 30.0)):
            fn = os.path.join(HERE, f"df3g_cell_G{g_:.3f}_s{s_:g}_N{TAGM}.json"); R = json.load(open(fn)); setc(g_, s_, "N"); Rf = rf_of(g_, s_); R["K_first_pass_lost_core"] = {f: R["K"][f] for f in FEET}
            for f in FEET: R["K"][f] = CO.fmt(keys(D, CSS, Rf, f, f"G{g_:.3f}_s{s_:g}_N")); print(g_, s_, f, R["K"][f]["n_pass"], R["K"][f]["worst"], flush=True)
            json.dump(R, open(fn, "w"), indent=1, sort_keys=True, default=float)
        setc(1.0, 100.0, "N"); L = json.load(open(os.path.join(HERE, "df3g_law.json")))
        for f in FEET: L[f]["K"] = CO.fmt(keys(D, CSS, 0.0, f, "LAW")); print("law", f, L[f]["K"]["n_pass"], flush=True)
        json.dump(L, open(os.path.join(HERE, "df3g_law.json"), "w"), indent=1, sort_keys=True, default=float)
    if mode == "mutate":
        setc(5 / 3, 100.0); Rf = rf_of(5 / 3, 100.0); a = xcop(XC, Rf, "canonical"); b = xcop(XC, 0.1 * Rf, "canonical"); S.Cfg.gself = 4.0; c = xcop(XC, Rf, "canonical"); S.Cfg.gself = 1.0; o = dict(mean=a["mean"], fairx01=b["mean"], gselfx4=c["mean"], bites=bool(abs(a["mean"] - b["mean"]) > .05)); print(o); json.dump(CO.fmt(o), open(os.path.join(HERE, "df3g_run_MUTATE.json"), "w"), indent=1, sort_keys=True, default=float)
TAGM = os.environ.get("DF3G_SUFFIX", "")
if __name__ == "__main__": main()
