#!/usr/bin/env python3
"""AF1 stage 1: residual table from on-disk data, one file per footing. FROZEN_CRITERIA.md. --mutate: a0 x 1.5.
kappa = 1/2 FITTED; not theory closed. Different samples measure different things; column `method` says which."""
import csv, hashlib, json, math, os, pickle, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; AX = 1.5 if MUT else 1.0
A0 = dict(canonical=9.360324825027975e-11 * AX, alt=1.1312e-10 * AX); C = 299792458.0; G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; KMS2 = 1e6; MPC = 3.0857e22
COLS = "sample,system,split_id,method,r,sigma_r,y,y_gas,y_star,f_gas,ell,x_rad,gas_slope,sig_eff,morph,env_dens,env_halo,x_host,d_host,z,m_sys,kT_cl,lM500,leaky_v2c".split(",")
OUT = []; ICR = {}
def P(s): print(s, flush=True); OUT.append(s)
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def row(**k): return [k.get(c, float("nan")) for c in COLS]
def msys(M_sun, a0): return math.log10(G * M_sun * MS * a0 / C ** 4)
Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))
def sparc(a0):
    meta = {g["name"]: g for g in Q["gals"]}; D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc"); o = []
    tab = {}
    for l in open(os.path.join(D, "SPARC_Lelli2016c.mrt")):
        q = l.split()
        if len(q) >= 18 and q[1].isdigit() and q[17].isdigit():
            tab[q[0]] = dict(T=float(q[1]), D=float(q[2]), L=float(q[7]), SBe=float(q[10]), MHI=float(q[13]))
    env = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "sparc_a0_environment_table.csv")))}
    fl = lambda s: float(s) if s not in ("", None, "nan") else float("nan")
    for n in sorted(meta):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30 or n not in tab: continue
        t = np.atleast_2d(np.loadtxt(os.path.join(D, "rotmod", n + "_rotmod.dat"), comments="#")); Rl = t[:, 0].max(); Mg = np.maximum(np.abs(t[:, 3]) * t[:, 3], 1e-9) * t[:, 0]; sl = np.gradient(np.log(Mg), np.log(t[:, 0])) if len(t) > 1 else np.ones(1); s = tab[n]; e = env.get(n, {})
        for k, (rk, v, ev, vg, vd, vb, *_) in enumerate(t):
            ms_ = 0.5 * abs(vd) * vd + 0.7 * abs(vb) * vb; gs = abs(vg) * vg; m = gs + ms_; R = rk * 1e3 * PC
            if rk <= 0 or v <= 0 or m <= 0: continue
            gN = m * KMS2 / R; go = v * v * KMS2 / R
            o.append(row(sample="SPARC", system=n, split_id=n, method="rotation", r=math.log10(go / law(gN, a0)), sigma_r=2 * ev / v / math.log(10), y=gN / a0, y_gas=max(gs, 0) * KMS2 / R / a0, y_star=max(ms_, 0) * KMS2 / R / a0, f_gas=min(1, max(0, gs / m)), ell=R * a0 / C ** 2, x_rad=rk / Rl, gas_slope=sl[k], sig_eff=G * (0.5 * s["SBe"] * MS / PC ** 2) / a0, morph=s["T"], env_dens=fl(e.get("onepd_2mrs")), env_halo=fl(e.get("logMhalo_host")), z=fl(e.get("cz_kms")) * 1e3 / C, m_sys=meta[n]["lMb"] + math.log10(G * MS * a0 / C ** 4), leaky_v2c=v * v * KMS2 / C ** 2))
    return o
def lt(foot, a0):
    J = json.load(open(os.path.join(RB, "NF1_no_floor_rule", "nf1_lt.json")))["rows"]; ms = {g["name"]: g for g in Q["lt"]}; o = []
    for n, g in sorted(J.items()):
        if n == "IC 1613": continue
        Mb = 10 ** g["lgMb"]; R = g["R"] * 1e3 * PC; gN = G * Mb * MS / R ** 2; go = (g["V"] * 1e3) ** 2 / R; fs = ms[n]["Mstar"] / Mb if n in ms else float("nan")
        o.append(row(sample="LT", system=n, split_id=n, method="rotation outer point", r=math.log10(go / law(gN, a0)), sigma_r=g["sE"], y=gN / a0, y_gas=gN / a0 * (1 - fs), y_star=gN / a0 * fs, f_gas=1 - fs, ell=R * a0 / C ** 2, m_sys=msys(Mb, a0), leaky_v2c=(g["V"] * 1e3) ** 2 / C ** 2))
    return o
def ic1613(a0):
    M = 10 ** 7.944975908412048; R = 2.71e3 * PC; gN = G * M * MS / R ** 2; go = (16.9e3) ** 2 / R; fs = 2.88e7 / M if False else None
    return dict(r=math.log10(go / law(gN, a0)), y=gN / a0, sE=0.075, ell=R * a0 / C ** 2)
LMD = np.load(os.path.join(RB, "LM1_law_missing_mass_map", "cache_BASE_f034", "dump.npz"))
def groups(foot, a0):
    R = LMD["groups_" + foot]; rows = Q["groups"]["rows"]; o = []
    for g, q in zip(rows, R):
        ls, pred, err, lM, Re, yg = q[:6]
        if abs(lM - g["lM"]) > 1e-6: raise SystemExit("groups order")
        R_ = Re * 1e3 * PC * 1e-3 if False else Re * PC; Mb = 10 ** lM; gNe = 0.5 * G * Mb * MS / R_ ** 2; sg = 10 ** ls * 1e3
        o.append(row(sample="groups", system=g["id"], split_id=g["id"], method="dispersion Jeans", r=2 * (ls - (pred if not MUT else math.log10(10 ** pred * AX ** 0.25))), sigma_r=2 * err, y=gNe / a0, y_star=gNe / a0, ell=R_ * a0 / C ** 2, gas_slope=float("nan"), sig_eff=G * (0.5 * Mb * MS / (math.pi * R_ ** 2)) / a0, m_sys=msys(Mb, a0), leaky_v2c=sg * sg / C ** 2))
    return o
def xcop(a0):
    D = os.path.join(REPO, "real_research", "data", "xcop"); o = []
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else float("nan")
    for n in sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits"))):
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (0.1, 0.2, 0.3, 0.5, 0.7):
            rr = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], rr); emh = li(hm["RADIUS"], hm["EM_FORW"], rr); mg = li(ga["RADIUS"] * rg, ga["MGAS"], rr); ms_ = li(st["RADIUS"], st[st.names[1]], rr)
            if not np.all(np.isfinite([mh, mg, ms_])): continue
            R = rr * 1e3 * PC; f = G * MS / R ** 2; gN = f * (mg + ms_); mgb = li(ga["RADIUS"] * rg, ga["MGAS"], rr * 1.05); mga = li(ga["RADIUS"] * rg, ga["MGAS"], rr / 1.05)
            m500 = li(hm["RADIUS"], hm["M_FORW"], r5)
            o.append(row(sample="XCOP", system=n, split_id=n, method="hydrostatic mass", r=math.log10(f * mh / law(gN, a0)), sigma_r=emh / mh / math.log(10), y=gN / a0, y_gas=f * mg / a0, y_star=f * ms_ / a0, f_gas=mg / (mg + ms_), ell=R * a0 / C ** 2, x_rad=x, gas_slope=math.log(mgb / mga) / (2 * math.log(1.05)), z=float(Q["xcop_halo"][n]["z"]) if n in Q["xcop_halo"] else float("nan"), m_sys=msys(mg + ms_, a0), lM500=math.log10(m500), leaky_v2c=G * mh * MS / R / C ** 2))
    return o
def shear_rows(foot, a0, view):
    X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); h = "h0672"; i = 1; d = LMD; T3 = d["T3M"]; N = len(T3); fs = 0.034; RC = d["RC"]
    W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); n = W * B0[None, :] * (X["D"][:, i] - X["leakP"][:, 0, 0]); V = d[f"V_{foot}_{h}"]; Mb = d[f"Mb_{foot}_{h}"]
    if abs(AX - 1) > 0: V = V / np.sqrt(AX)  # MUTATE: mimics a mis-scaled law amplitude; the twin must fail K4
    from astropy.io import fits as F
    E = F.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; nm = {str(s).strip(): k for k, s in enumerate(E["NAME"])}; KT = np.array([float(E["KT"][nm[str(s).strip()]]) if str(s).strip() in nm else np.nan for s in X["name"]]); Mg = np.asarray(X["Mgas500"], float); M5 = np.asarray(X["M500"], float); zc = np.asarray(X["z"], float); R5 = d["R500_" + h]
    if view == "M": groups_ = {f"M{t+1}": np.nonzero(T3 == t)[0] for t in range(3)}
    else: groups_ = {f"T{t+1}": d["I"][d["TID"] == t] for t in range(3)}
    rng = np.random.default_rng(20261102); o = []; dropped = 0; tot = {}
    for nm_, ix in groups_.items():
        for b in range(8):
            w = W[ix, b]; A = n[ix, b].sum() / V[ix, b].sum()
            bs = [n[ix[q], b].sum() / V[ix[q], b].sum() for q in rng.integers(0, len(ix), (400, len(ix)))]
            if A <= 0: dropped += 1; continue
            R = RC[b] * MPC; yy = float((w * (G * Mb[ix, b] * MS / R ** 2 / a0)).sum() / w.sum()); ws = w.sum()
            o.append(row(sample="shear" + view, system=nm_, split_id=f"{nm_}|{b}", method="lensing dDS projected", r=math.log10(A), sigma_r=float(np.std(bs)) / A / math.log(10), y=yy, y_gas=yy / (1 + fs), y_star=yy * fs / (1 + fs), f_gas=1 / (1 + fs), ell=R * a0 / C ** 2, x_rad=RC[b] / float(np.median(R5[ix])), z=float((w * zc[ix]).sum() / ws), m_sys=msys(float(np.median(Mg[ix])) * (1 + fs), a0), kT_cl=float(np.nanmean(KT[ix])), lM500=float(np.log10(np.median(M5[ix])))))
    return o, dropped, (n.sum(0) / V.sum(0))
def dwarfs(foot, a0):
    G5, MS5, PC5 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; arr = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")))); af = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in arr}; med = float(np.median(list(af.values())))
    CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); o = []; ICr = None
    for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))):
        if r["footing"] != foot or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] else None; b = af.get(r["name"], med if (mv is not None and mv > -7.7) else 1.0); sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC5; Mb = 10 ** float(r["logMstar"]); go = 3 * (sc * 1e3) ** 2 / r12; gN = G5 * (Mb / 2) * MS5 / r12 ** 2
        if r["name"] == "IC 1613": ICR[foot] = math.log10(go / (0.5 * gN + math.sqrt(0.25 * gN * gN + a0 * gN))); continue
        o.append(row(sample="dwarfs", system=r["name"] + "|" + r["cls"], split_id=r["name"], method="half-light dispersion", r=math.log10(go / (0.5 * gN + math.sqrt(0.25 * gN * gN + a0 * gN))), sigma_r=float(r["sdMC[Newton]"]), y=gN / a0, y_star=gN / a0, f_gas=0.0, ell=r12 * a0 / C ** 2, sig_eff=G5 * (0.5 * Mb * MS5 / (math.pi * (float(r["rh_pc"]) * PC5) ** 2)) / a0, x_host=float(r["x_e_mid"]) if r["x_e_mid"] else float("nan"), d_host=float(r["d_host_kpc"]) if r["d_host_kpc"] else float("nan"), m_sys=msys(Mb, a0), morph=float("nan"), leaky_v2c=(sc * 1e3) ** 2 / C ** 2))
    return o
def mw(a0):
    cf = os.path.join(HERE, f"mw_newton.json")
    if not os.path.exists(cf):
        sys.path.insert(0, os.path.join(RB, "X5_mw_joint_baryons")); import x5_lib as L
        ns = L.load_p4(); PS = ns["S"]; ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14); a = L.A0_SI["canonical"]; Mu = PS.mass_unit(a); g = ns["mw_grid"](6.6e10 / Mu); rho = g.rho_axisym(lambda R, z: ns["rho_mcm"](R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho * g.vol)); pr = PS.Problem(g, rho, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton(); R = np.r_[ns["R0_MW"], ou[:, 0]]; vb = L.vc_plane(ns, g, Phi, a, R); json.dump(dict(R=R.tolist(), vb=vb.tolist(), vo=ou[:, 1].tolist(), eo=np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(ou[:, 0] <= 22.0, 0.03, 0.15) * ou[:, 1]).tolist(), Mb=Mt * Mu), open(cf, "w"))
    J = json.load(open(cf)); R = np.array(J["R"][1:]); vb = np.array(J["vb"][1:]); vo = np.array(J["vo"]); eo = np.array(J["eo"]); o = []
    # gas share: McMillan 2017's HI and H2 sheets, values PROVISIONAL from the published form, spherical enclosed approximation, flagged in README
    Rg = np.geomspace(0.05, 60, 4000); Sg = 53.1 * np.exp(-4 / Rg - Rg / 7) + 2180 * np.exp(-12 / Rg - Rg / 1.5); Mg = np.cumsum(2 * np.pi * Rg * Sg * np.gradient(Rg)) * 1e6
    for rk, v, e, vbk in zip(R, vo, eo, vb):
        rm = rk * 1e3 * PC; gN = (vbk * 1e3) ** 2 / rm; go = (v * 1e3) ** 2 / rm; gg = min(G * float(np.interp(rk, Rg, Mg)) * MS / rm ** 2, gN); 
        o.append(row(sample="MW", system=f"MW_R{rk:.2f}", split_id=f"MW_R{rk:.2f}", method="rotation curve, model baryons", r=math.log10(go / law(gN, a0)), sigma_r=2 * e / v / math.log(10), y=gN / a0, y_gas=gg / a0, y_star=(gN - gg) / a0, f_gas=gg / gN, ell=rm * a0 / C ** 2, m_sys=msys(J["Mb"], a0), leaky_v2c=(v * 1e3) ** 2 / C ** 2))
    return o
def main():
    P(f"AF1 stage 1{' MUTATE a0 x 1.5' if MUT else ''}; kappa = 1/2 FITTED; not theory closed"); CHK = {}; RES = {}
    LMV = json.load(open(os.path.join(RB, "LM1_law_missing_mass_map", "lm1_results.json")))["canonical"]["obs_over_law"]; LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))["footings"]
    for foot, a0 in A0.items():
        R = sparc(a0) + lt(foot, a0) + groups(foot, a0) + xcop(a0); sM, dM, fac = shear_rows(foot, a0, "M"); sT, dT, _ = shear_rows(foot, a0, "T"); D = dwarfs(foot, a0); M = mw(a0); R = R + sM + sT + D + M
        o = os.path.join(HERE, f"af1_table_{foot}{TAG}.csv")
        with open(o, "w", newline="") as f:
            w = csv.writer(f); w.writerow(COLS)
            for r in R: w.writerow([("" if isinstance(c, float) and not math.isfinite(c) else (f"{c:.7g}" if isinstance(c, float) else c)) for c in r])
        S = {}; ar = np.array([r[COLS.index("r")] for r in R], float); sm = np.array([r[0] for r in R]); sy = np.array([r[1] for r in R])
        for s in sorted(set(sm)):
            m = sm == s; S[s] = dict(n=int(m.sum()), systems=len(set(sy[m])), mean=float(ar[m].mean()), median=float(np.median(ar[m])), rms=float(np.sqrt((ar[m] ** 2).mean()))); P(f"[{foot}] {s:8s} rows {S[s]['n']:5d} systems {S[s]['systems']:4d} mean {S[s]['mean']:+.3f} median {S[s]['median']:+.3f} rms {S[s]['rms']:.3f}")
        cov = {}
        for c in COLS[6:]:
            k = COLS.index(c); cov[c] = {s: float(np.mean([isinstance(r[k], (int, float)) and math.isfinite(r[k]) for r, q in zip(R, sm) if q == s])) for s in sorted(set(sm))}
        ic = ic1613(a0); RES[foot] = dict(samples=S, coverage=cov, ic1613=ic, shear_dropped=dict(M=dM, T=dT)); P(f"[{foot}] IC 1613 E {ic['r']:+.3f}; shear cells dropped M {dM}, T {dT}")
        kx = (+0.467, 0.476) if foot == "canonical" else (+0.434, 0.444); CHK[f"K1 {foot}"] = bool(abs(S["XCOP"]["mean"] - kx[0]) <= .002 and abs(S["XCOP"]["rms"] - kx[1]) <= .002)
        gm = 0.5 * S["groups"]["mean"]; CHK[f"K2 {foot}"] = bool(abs(gm - (0.0100 if foot == "canonical" else -0.0103)) <= .002)
        if foot == "canonical": CHK["K3 canonical"] = bool(abs(ic["r"] + 0.593) <= .01); CHK["K4 canonical"] = bool(np.max(np.abs(fac - np.array(LMV))) <= .02); RES["K4_dev"] = float(np.max(np.abs(fac - np.array(LMV))))
        cl = {}
        for r in D: cl.setdefault(r[1].split("|")[1], []).append(r[COLS.index("r")])
        cl["LG field"].append(ICR[foot])  # K5 compares LW1's classes, which still hold IC 1613; the table doesn't
        dv = {c: float(np.median(v) - LW[foot]["rows"]["plain"][c]["median"]) for c, v in cl.items()}; CHK[f"K5 {foot}"] = bool(max(abs(x) for x in dv.values()) <= .03); RES[foot]["K5"] = dv
    Jm = json.load(open(os.path.join(HERE, "mw_newton.json"))); CHK["K6"] = bool(abs(Jm["vb"][0] - 177.09) <= 2); RES["K6"] = Jm["vb"][0]
    for k, v in CHK.items(): P(f"{k}: {'PASS' if v else 'FAIL'}")
    RES["checks"] = CHK; json.dump(RES, open(os.path.join(HERE, f"af1_stage1{TAG}.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, f"af1_stage1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
main()
