#!/usr/bin/env python3
"""DF3 runs. Modes: lawzero | map | cell G SIG | planted. HF1 gate 2-3 code read-only, its solver swapped in memory. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); HF = os.path.join(RB, "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
_argv = sys.argv[:]; sys.argv = ["hf1_g23.py"]
import hf1_g23 as H
sys.argv = _argv
import numpy as np, df3_solver as S
H.FM.solve = S.solve; os.makedirs(os.path.join(HERE, "cache"), exist_ok=True); H.CO.CACHE = os.path.join(HERE, "cache")
C, CO, GR, DW, SP = H.C, H.CO, H.GR, H.DW, H.SP; A0 = H.A0; FEET = H.FEET; MSUN = H.MSUN
DF2 = os.path.join(RB, "DF2_dark_fluid_requirement", "cells")
def rf_of(gam, sig):
    d = json.load(open(os.path.join(DF2, f"P_G{gam:.3f}_s{sig:g}_fit.json"))); p = d["params"]; return p["omega_c"] / p["omega_b"]
def setc(gam, sig): S.Cfg.gamma = gam; S.Cfg.sigma = sig * 1e3; S.Cfg.K_mult = 1.0
def counted(fn):
    S.STAT.update(rows=0, noeq=0); v = fn(); return v, (S.STAT["noeq"] / max(S.STAT["rows"], 1))
def disc_numbers(G, Rf, a0):
    """Y 0.5, 0.7: fluid at R_last over rho_a, M_f/M_b at R_last, half-mass radius over R_last."""
    rows = []
    for g in G:
        VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = np.maximum(VB2 * 1e6 / g["R"], 1e-30)[None, :]; rg = H.gal_grid(g); Mt = (np.array([0.5]) * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MSUN; Mb = H.gal_masses(g, gb, Mt, rg); Mtot = np.maximum(Mb[:, -1], Mt); rta = np.array([H.RTA(x) for x in Mtot]); s = S.solve(rg, Mb, rta, g["R"][-1], Rf * Mtot, a0=a0)
        RL = g["R"][-1]; mf = float(np.interp(math.log(RL), np.log(rg), s["Mf"][0])); rho = float(np.exp(np.interp(math.log(RL), np.log(rg), np.log(np.maximum(s["rho"][0], 1e-300))))); Mbl = float(gb[0, -1] * RL ** 2 / H.GF); tot = s["Mf"][0, -1]; rh = float(rg[np.argmax(s["Mf"][0] >= .5 * tot)])
        rows.append(dict(name=g["name"], V=g["Vflat"], lgMb=g["lgMb"], rho_over_a=rho / S.RHO_A, mf_mb=mf / Mbl, rh_RL=rh / RL, noeq=bool(s["noeq"][0]), retained=float(tot / (Rf * Mtot[0]))))
    def med(key, sel): v = [r[key] for r in rows if sel(r)]; return float(np.median(v)) if v else None
    S_ = [("all", lambda r: True), ("V<100", lambda r: r["V"] < 100), ("V>200", lambda r: r["V"] > 200)]
    return {n: dict(rho_over_a=med("rho_over_a", f), mf_mb=med("mf_mb", f), rh_RL=med("rh_RL", f), noeq=float(np.mean([r["noeq"] for r in rows if f(r)])), retained=med("retained", f)) for n, f in S_}
def xline(lab, x, ne): return f"  X-COP {lab}: mean {x['all']['mean']:+.3f} rms {x['all']['rms']:.3f} {'PASS' if x['all']['passed'] else 'FAIL'}; train {x['train']['mean']:+.3f}, holdout {x['holdout']['mean']:+.3f}; by x {[round(v, 3) for v in x['by_x'].values()]}; M_f/M_b {[round(v, 2) for v in x['mf_over_mb_by_x'].values()]}; NO EQUILIBRIUM {ne:.2f}"
def g3(G, LT, gr, Rf, f, full=True):
    a0 = A0[f]; (r, t, _), ne = counted(lambda: H.sparc_fit(G, Rf, 11.0, a0)); w = dict(rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"], sparc_noeq=ne); g_, ng = counted(lambda: H.groups_stat(gr, Rf, 11.0, a0)); w.update(groups=g_["Z"], groups_cls=g_["cls"], groups_noeq=ng); w["S"] = bool(r["rms"] <= .110 and .50 <= r["Y_med"] <= .80); w["Tl"] = bool(abs(t["tilt"]) <= .15); w["G"] = g_["cls"] == "CONSISTENT"
    if full:
        h_ = H.hs_slope(G, Rf, 11.0, a0); lt, nl = counted(lambda: [H.lt_row(x, Rf, 11.0, a0) for x in LT]); E_ = np.array([v[0] for v in lt]); ltm = float(np.median(E_)); ic = float(E_[[i for i, x in enumerate(LT) if x["name"] == "IC 1613"][0]]); d_, nd = counted(lambda: H.dwarf_E(DW.load(f), Rf, 11.0, a0)); w.update(hs=h_["Z"], HS=h_["passed"], lt=ltm, LT=bool(abs(ltm) <= .10), lt_noeq=nl, ic_Z=ic / .075, dwarfs={k: v["Z"] for k, v in d_["classes"].items()}, dw_noeq=nd); w["pass"] = bool(w["S"] and w["Tl"] and w["HS"] and w["LT"] and w["G"])
    return w
def bullet(Rf, a0=A0["canonical"]):
    KPC = 3.0857e19; out = {}
    import csv; rows = {(w["system"], w["sub"]): w for w in csv.DictReader(open(os.path.join(RB, "MG1_merger_sample", "mg1_table.csv")))}
    for k in (("Bullet", "main"), ("Bullet", "sub")):
        w = rows[k]; ML = float(w["M_lens"]); Mgas = float(w["M_gas"]) if w["M_gas"] not in ("", "DEFAULT") else .12 * ML; Mst = float(w["M_star"]) if w["M_star"] not in ("", "DEFAULT") else .02 * ML; ag = float(w["a_gas"] or 300) * KPC; ast = float(w["a_star"] or 200) * KPC; Mbt = (Mgas + Mst) * MSUN; rta = H.RTA(Mbt); r = np.geomspace(1 * KPC, rta, 400); M0 = Mst * MSUN * (r / (r + ast)) ** 2 + Mgas * MSUN * (r / (r + ag)) ** 2; s = S.solve(r, M0, rta, 300 * KPC, Rf * Mbt, a0=a0); rho = s["rho"]; Sig = float(2 * np.trapz(rho * r, np.log(r))); rc = float(rho[0]); cs = S.Cfg.sigma * (rc / S.RHO_A) ** ((S.Cfg.gamma - 1) / 2); Rh = float(r[np.argmax(s["Mf"] >= .5 * s["Mf"][-1])])
        out[k[1]] = dict(column_Msun_pc2=Sig / (MSUN / (3.0857e16) ** 2), rho_c_Msun_pc3=rc / S.RHO_A * .05, cs_core_kms=cs / 1e3, mach_4700=4700e3 / cs, half_mass_kpc=Rh / KPC, retained=float(s["Mf"][-1] / (Rf * Mbt)), noeq=bool(s["noeq"]))
    return out
def full_cell(gam, sig, D, CSS, XC, G, LT):
    setc(gam, sig); Rf = rf_of(gam, sig); tag = f"G{gam:.3f}_s{sig:g}"; out = []; R = dict(gamma=gam, sigma=sig, Rf=Rf)
    def P(s): print(s, flush=True); out.append(s)
    P(f"\n=== Gamma {gam:.3f}, sigma {sig:g} km/s, omega_f/omega_b {Rf:.3f}")
    R["X"] = {}; R["X_noeq"] = {}
    for f in FEET:
        x, ne = counted(lambda: H.xcop_rows(XC, Rf, 11.0, f)); R["X"][f] = {k: x[k] for k in ("all", "train", "holdout", "by_x", "mf_over_mb_by_x", "per_cluster")}; R["X_noeq"][f] = ne; P(xline(f, x, ne))
    R["bullet"] = bullet(Rf); P(f"  Bullet, order of magnitude: {json.dumps(R['bullet'], default=float)}")
    gr = GR.load(); R["G3"] = {}
    for f in FEET:
        w = g3(G, LT, gr, Rf, f); w["discs"] = disc_numbers(G, Rf, A0[f]); R["G3"][f] = w; P(f"  Gate 3 {f}: rms {w['rms']:.4f} Y {w['Y']:.2f} tilt {w['tilt']:+.2f} SB Z {w['hs']:+.2f} LT {w['lt']:+.3f} groups Z {w['groups']:+.2f} {w['groups_cls']} Dw {[round(v, 2) for v in w['dwarfs'].values()]} IC Z {w['ic_Z']:+.1f}; {'PASS' if w['pass'] else 'FAIL'}; NO EQ sparc {w['sparc_noeq']:.2f} groups {w['groups_noeq']:.2f} LT {w['lt_noeq']:.2f} dw {w['dw_noeq']:.2f}")
        P(f"    discs {json.dumps(w['discs'], default=float)}")
    R["K"] = {}; info = []
    FA = json.load(open(os.path.join(RB, "DA1_definition_audit", "da1_keys.json")))["F"]; GRD = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]); fac = lambda hn: np.interp(D.z, GRD, FA[hn])[:, None]
    for f in FEET:
        S.STAT.update(rows=0, noeq=0); cells = H.keys_all(D, CSS, Rf, 11.0, 0.034, 0.005, f, tag, info=info if f == "canonical" else None); ne = S.STAT["noeq"] / max(S.STAT["rows"], 1); T = H.k_table(D, cells, f); R["K"][f] = dict(n_pass=T["n_pass"], failing=T["failing"], worst=T["worst"], noeq=ne); P(f"  Keys {f}: {T['n_pass']} of 15; worst {T['worst']}; failing {T['failing']}; NO EQUILIBRIUM {ne:.2f}")
        if f == "canonical":
            for lab, kw in (("B=1", dict(B1=True)), ("n(z)", dict(fac=fac))):
                t = H.k_table(D, cells, f, **kw); R["K"]["cano_" + lab] = dict(n_pass=t["n_pass"], worst=t["worst"]); P(f"    DA1 {lab}: {t['n_pass']} of 15; worst {t['worst']}")
    R["gate2"] = {f: bool(R["X"][f]["all"]["passed"] and R["K"][f]["n_pass"] == 15) for f in FEET}; P(f"  gate 2 {R['gate2']}; gate 3 { {f: R['G3'][f]['pass'] for f in FEET} }")
    json.dump(CO.fmt(R), open(os.path.join(HERE, f"df3_cell_{tag}.json"), "w"), indent=1, sort_keys=True, default=float); open(os.path.join(HERE, f"df3_cell_{tag}.out"), "w").write("\n".join(out) + "\nkappa = 1/2 FITTED. Not theory closed.\n")
def main():
    mode = sys.argv[1]; D, CSS, XC, G, LT = H.load_common()
    if mode == "lawzero":
        setc(5 / 3, 100.0); x = H.xcop_rows(XC, 0.0, 11.0, "canonical"); r, t, _ = H.sparc_fit(G, 0.0, 11.0, A0["canonical"]); ck = dict(xmean=x["all"]["mean"], xrms=x["all"]["rms"], rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"]); ck["passed"] = bool(abs(x["all"]["mean"] - .467) <= .01 and abs(x["all"]["rms"] - .476) <= .01 and abs(r["rms"] - .0541) <= 2e-4)
        setc(5 / 3, 3.0); w = g3(G, LT, GR.load(), rf_of(5 / 3, 30), "canonical", full=True); ck["planted"] = {k: w[k] for k in ("rms", "Y", "tilt", "pass")}; ck["planted_fails"] = not w["pass"]; print(json.dumps(ck, indent=1, default=float)); json.dump(ck, open(os.path.join(HERE, "df3_lawzero.json"), "w"), indent=1, default=float)
    if mode == "cell": full_cell(float(eval(sys.argv[2])), float(sys.argv[3]), D, CSS, XC, G, LT)
    if mode == "map":
        Rf = rf_of(5 / 3, 30); gr = GR.load(); T = {}; out = []
        for gam, gn in ((5 / 3, "5/3"), (1.0, "1"), (2 / 3, "2/3")):
            for sig in (3, 10, 30, 100, 300, 1000):
                setc(gam, float(sig)); x, ne = counted(lambda: H.xcop_rows(XC, Rf, 11.0, "canonical")); w = g3(G, LT, gr, Rf, "canonical", full=False); T[f"{gn}_{sig}"] = dict(x_mean=x["all"]["mean"], x_rms=x["all"]["rms"], by_x=x["by_x"], x_pass=x["all"]["passed"], x_noeq=ne, **w)
                ln = f"G {gn:>3s} s {sig:5d}: X {x['all']['mean']:+.3f} {x['all']['rms']:.3f} by x {[round(v, 2) for v in x['by_x'].values()]} NE {ne:.2f}; SPARC {w['rms']:.4f} Y {w['Y']:.2f} tilt {w['tilt']:+.2f} NE {w['sparc_noeq']:.2f}; groups {w['groups']:+.2f} NE {w['groups_noeq']:.2f}; {'ALL THREE' if (x['all']['passed'] and w['S'] and w['Tl'] and w['G']) else ''}"
                print(ln, flush=True); out.append(ln); open(os.path.join(HERE, "df3_map.out"), "w").write("\n".join(out) + "\n"); json.dump(T, open(os.path.join(HERE, "df3_map.json"), "w"), indent=1, default=float)
main()
