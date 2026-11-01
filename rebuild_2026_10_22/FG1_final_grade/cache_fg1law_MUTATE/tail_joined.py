# XH1 tail (criteria 530debe21b): runs inside FC1's grader namespace, after its full grade, in place of its last line.
import csv as _csv
from astropy.io import fits as _fits
from scipy.optimize import minimize_scalar as _ms
_REPO = os.path.dirname(REB); _KX = {}
_TS = open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample.py")).read()
_code = _TS[_TS.index("# ------------------------------------------------------------------ X-COP (matched-clumping profiles)"):
            _TS.index("# ------------------------------------------------------------------ graders per law")]
_CJ = json.load(open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample_results.json")))
_S = {"os": os, "np": np, "math": math, "csv": _csv, "fits": _fits, "minimize_scalar": _ms, "brentq": brentq, "REPO": _REPO,
      "check": (lambda k, ok, msg: _KX.__setitem__("CS2_" + k, bool(ok))), "R0C": _CJ["calibration"]["r0_law"]["c"], "R0P": _CJ["calibration"]["r0_law"]["p"], "SREF": 70.50}
exec(compile(_code, "cs2_xcop_block", "exec"), _S)
_XC = _S["XC"]; _cs2 = _S["xcop"](_CJ["calibration"]["A"], _CJ["calibration"]["q"], 70.50); _rf = _CJ["footings"]["canonical"]["CS2"]["xcop"]
_k1 = max(abs(_cs2[k] - _rf[k]) for k in ("mean", "rms", "n", "saturated"))
_PCm = 3.0857e16; _TBG = "A_c2b_refit"; _SMULT = float(os.environ.get("XH1_SMULT", "1"))
_rta_com, _gc2, _MSX = NX["r_ta_com"], NX["_gc2_ext"], NX["MSUN"]
_XM = {}
for _c in _XC:
    _p = os.path.join(_REPO, "real_research", "data", "xcop", _c["name"])
    with _fits.open(os.path.join(_p, f"{_c['name']}_hydro_mass.fits")) as _h: _z = float(_h[1].header["REDSHIFT"]); _r5 = float(_h[1].header["R500"])
    with _fits.open(os.path.join(_p, f"{_c['name']}_fgas_profile.fits")) as _h: _g = _h[1].data.copy(); _rg = _h[1].header["R500"]
    _XM[_c["name"]] = dict(z=_z, r500=_r5, Mg500=_S["li"](_g["RADIUS"] * _rg, _g["MGAS"], _r5))
def _budget(name, fac=1.0):
    m = _XM[name]; Mbx, Mbt = _gc2(m["Mg500"], m["r500"] / 1e3, m["z"], fac * 3.0 * 1.2 * m["Mg500"] * _MSX)
    return Mbt, _rta_com(Mbt) / (1 + m["z"])
def _grade(foot):
    rows = []; per = {}; info = {}; k2 = []; k3 = []; k4 = []; floor = 0; sat0 = SAT["n"]
    for c in _XC:
        nm = c["name"]; Mbt, rta = _budget(nm); k3.append(max(abs(_budget(nm, f_)[0] / Mbt - 1) for f_ in (0.3, 3.0)))
        Mfair = NAT_RRAT * Mbt; Mtot = (Mfair + Mbt) / MSUNE; s0, act = sig_core(foot, _TBG, Mtot, True); floor += 0 if act else 1
        if act: k4.append(abs(s0 / (sigma_coll(_TBG, Mtot)[0] * MSUNE / PC2) / (FC1_F * eta_of(cf_of(Mtot))) - 1))
        s = s0 * _SMULT; n0 = SAT["n"]; r0 = solve_r0(Mfair, rta, s); sat = SAT["n"] > n0
        k2.append(0.0 if sat else abs(math.pi * s * r0 ** 2 * float(B(rta / r0)) / Mfair - 1)); dd = []
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            rm = r * 1e3 * _PCm; Mh = math.pi * s * r0 ** 2 * float(B(min(rm, rta) / r0)); dd.append(dict(cluster=nm, x=x, r_kpc=r, Mh_Msun=Mh / MSUNE, Mb_Msun=mb, MHSE_Msun=mh, d=math.log10(mh * MSUNE / (mb * MSUNE + Mh))))
        rows += dd; per[nm] = float(np.mean([v["d"] for v in dd]))
        info[nm] = dict(logM=math.log10(Mtot), S_pc2=s * _PCm ** 2 / MSUNE, r0_kpc=r0 / _PCm / 1e3, rta_Mpc=rta / NX["MPC"], Mbt_over_Mg500=Mbt / (_XM[nm]["Mg500"] * _MSX), saturated=bool(sat))
    d = np.array([v["d"] for v in rows]); band = [v["d"] for v in rows if 150.0 <= v["r_kpc"] <= 460.0]
    return dict(mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))), n=int(len(d)), saturated=int(SAT["n"] - sat0), on_floor=floor, per_cluster=per, info=info, rows=rows,
                by_x={f"{x:g}": float(np.mean([v["d"] for v in rows if abs(v["x"] - x) < 1e-9])) for x in (0.1, 0.2, 0.3, 0.5, 0.7)},
                band=dict(n=len(band), mean=float(np.mean(band)), R_X=float(10 ** (-np.mean(band)))), k2=max(k2), k3=max(k3), k4=max(k4) if k4 else 0.0)
# UR1 tail, in NF1's grader namespace after XH1's X-COP helpers. Reads only.
import pickle as _pk
_SL1 = os.environ["UR1_SL1"]; _C = _pk.load(open(os.path.join(_SL1, "cache", "sl1_cache.pkl"), "rb")); _TP = _C["clusters"]["tmpl"]; _KY = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]; _TG = ("A_c2b_refit", "B_cfg886_bg"); _OUTU = {}; _BIN = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400))
_MRT = os.path.join(REB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt"); _TB = {}
for _l in open(_MRT):
    _p = _l.split()
    if len(_p) < 18: continue
    try: _TB[_p[0]] = dict(inc=float(_p[5]), vf=float(_p[15]), Q=int(_p[17]))
    except ValueError: pass
_rta = NX["r_ta_com"]
def _gals_U(tag, f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); U = {}; R = {}
    for q in GALS:
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, a_ = sig_core(f, tag, M2 / FC1_MC)
        if a_ and CN1_MODE != "off": gh = GHSTORE[(f, tag, q["name"])]; r0 = None
        else: r0 = solve_r0(M2 * MSUNE, R2, s); gh = (GE * math.pi * s * r0 ** 2 * B(np.minimum(q["Rm"], R2) / r0) / q["Rm"] ** 2)[:, None]
        U[q["name"]] = float(UPS[int(fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300)))[2])])
    return U
def _keys(gc, f):
    o = {}
    for hk in HK:
        o[hk] = {k: (_TP[f"{f}|{hk}"][k][0] - gc["cells"][hk][k]["pred"]) / _TP[f"{f}|{hk}"][k][1] for k in _KY}
    bad = sorted({k for hk in HK for k in _KY if abs(o[hk][k]) > 2}); return dict(Z=o, bad=bad, n=15 - len(bad), preds={hk: {k: gc["cells"][hk][k]["pred"] for k in _KY} for hk in HK})
def _resp(rg, Mb, M0, F):
    if CN1_MODE == "off": return M0
    return contract(rg, Mb, M0, F, gnedin=(0.85, 0.8, rg[-1]) if CN1_MODE == "gnedin" else None)[0]
def _xcop(f="canonical"):
    D_ = []; bx = {}
    for c_ in _XC:
        nm = c_["name"]; Mbt, rta = _budget(nm); m = _XM[nm]; Mbx, _ = _gc2(m["Mg500"], m["r500"] / 1e3, m["z"], 3.0 * 1.2 * m["Mg500"] * _MSX); Mf = NAT_RRAT * Mbt; Mt_ = (Mf + Mbt) / MSUNE; s, _ = sig_core(f, _TBG, Mt_, True); r0 = solve_r0(Mf, rta, s); M0 = math.pi * s * r0 ** 2 * B(np.minimum(RM, rta) / r0); Mc = _resp(RM, Mbx, M0, Mbt / Mf) if CN1_MODE != "off" else M0
        for x, r, mh, mb in c_["rows"]:
            if x > 0.75: continue
            rm = r * 1e3 * _PCm; v = math.log10(mh * MSUNE / (mb * MSUNE + float(np.interp(rm, RM, Mc)))); D_.append(v); bx.setdefault(x, []).append(v)
    d = np.array(D_); return dict(mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))), by_x={f"{k:g}": float(np.mean(v)) for k, v in bx.items()}, PASS=bool(abs(d.mean()) <= 0.05 and np.sqrt(np.mean(d ** 2)) <= 0.10))
def _groups(f="canonical"):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540); d = []; sl = []
    def one(o, dl):
        lMb = o["lM"] + dl; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE; M2, R2 = _SL3M(lMb, bg, rc); s, _ = sig_core(f, "A_c2b_refit", M2 / FC1_MC); r0 = solve_r0(M2 * MS540, R2, s); rr = XG * a; M0 = math.pi * s * r0 ** 2 * B(np.minimum(rr, R2) / r0)
        if CN1_MODE != "off":
            rg = np.geomspace(min(rr[0], R2 * 1e-4), R2, 800); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = np.interp(np.log(rg), np.log(rr), Mb * M_H); Mcg = _resp(rg, Mbg, M0g, float(Mbg[-1] / M0g[-1])); Mc = np.interp(np.log(rr), np.log(rg), Mcg)
        else: Mc = M0
        gN = M_H / XG ** 2 + Mc / Mb / XG ** 2; s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a; return 0.5 * math.log10(s2) - 3.0
    for o in GROUPS: d.append(o["ls"] - one(o, 0.0)); sl.append((one(o, 0.01) - one(o, -0.01)) / 0.02)
    st = NSG["class_stats"](d, sl); return st
def _lt(tag, f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); E = []
    for r_ in _C["lt"]:
        M2, R2 = _SL3M(r_["logMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); R_ = r_["R"] * MPCE / 1e3; Mb = 10 ** r_["logMb"] * MSUNE; rg = np.geomspace(R_ * 1e-3, R2, 600); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = Mb * np.minimum(rg / R_, 1.0) ** 2; Mc = float(np.interp(math.log(R_), np.log(rg), _resp(rg, Mbg, M0g, Mb / (M2 * MSUNE)))); E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(GE * Mb / R_ ** 2 + GE * Mc / R_ ** 2))
    return float(np.median(E))
def _resp_gal(tag="A_c2b_refit", f="canonical"):
    """Effective response at r0 by V_flat, Upsilon 0.50; clusters at their inner band."""
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); O = {f"{l}-{h}": [] for l, h in _BIN}
    for q in GALS:
        t = _TB.get(q["name"]);
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 400); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        Mf_ = contract(rg, np.maximum.accumulate(Mbg), M0, Mt / (M2 * MSUNE))[0]; i = int(np.argmin(abs(rg - r0)))
        for l, h in _BIN:
            if l <= t["vf"] < h: O[f"{l}-{h}"].append(dict(Q=float(Mf_[i] / M0[i]), fl=float(np.interp(r0, rg, Mbg) / M0[i])))
    Rb = {k: dict(Q=float(np.median([x["Q"] for x in v])), fl=float(np.median([x["fl"] for x in v]))) for k, v in O.items()}
    Cq = {"0.05": [], "0.15": [], "0.3": [], "0.46": [], "1": []}; hk = HK[0]
    for i in ALLI[::4]:
        i = int(i); pp = prep(i, f, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE; s, _ = sig_core(f, "A_c2b_refit", Mtot, True); r0 = solve_r0(pp["Mfair"], pp["rta"], s); M0 = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0); Mbn = pp["Mb"]; Mbf = Mbn + BCGF[i] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2; Fc = float(np.interp(pp["rta"], RM, Mbf)) / pp["Mfair"]; Mf1 = contract(RM, Mbf, M0, Fc)[0]; Mf2 = contract(RM, Mbn, M0, float(np.interp(pp["rta"], RM, Mbn)) / pp["Mfair"])[0]
        for k in Cq:
            rm = float(k) * NX["MPC"]; Cq[k].append((float(np.interp(rm, RM, Mf1) / np.interp(rm, RM, M0)), float(np.interp(rm, RM, Mf2) / np.interp(rm, RM, M0)), float(np.interp(rm, RM, Mbn) / np.interp(rm, RM, M0))))
    PREP.clear(); return dict(gal=Rb, clusters={k: dict(with_BCG=float(np.median([a[0] for a in v])), gas_stars_only=float(np.median([a[1] for a in v])), fl=float(np.median([a[2] for a in v]))) for k, v in Cq.items()}, cosmic=1 / NAT_RRAT)
def _run(mp, mode, mut=1.0):
    global CN1_MODE
    SLMAP["m"] = mp; SLMAP["mut"] = mut; CN1_MODE = mode; GHSTORE.clear(); r = dict(map=mp, mode=mode, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    gc = grade_clusters(f); r["keys"] = _keys(gc, f); r["keys_alt"] = _keys(grade_clusters("alt"), "alt")["bad"]; r["groups"] = _groups(); r["xcop"] = _xcop(); r["lt"] = {t: _lt(t) for t in _TG}
    print(f"UR1 {mp} {mode} {_tm.time() - _T0:.0f} s", flush=True); return r
# FG1 law tail, after UR1's helpers. Reads only: the a0 law on UR2's galaxies, grid and LITTLE THINGS systems. kappa = 1/2 FITTED.
_MUT = os.environ.get("FG1_MUTATE") == "1"; _A = dict(canonical=9.3603e-11, alt=1.1312e-10); _R = {}
def _nu(gN, a0): return np.ones_like(gN) if _MUT else 0.5 + np.sqrt(0.25 + a0 / np.maximum(gN, 1e-300))
for f_, a0 in _A.items():
    _R[f_] = {}
    for t in _TG:
        U = {}
        for q in GALS: U[q["name"]] = float(UPS[int(fit_one(q, np.log10(np.maximum(q["GB"] * _nu(q["GB"], a0), 1e-300)))[2])])
        v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); E = []
        for r_ in _C["lt"]:
            R_ = r_["R"] * MPCE / 1e3; gN = GE * 10 ** r_["logMb"] * MSUNE / R_ ** 2; E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(gN * float(_nu(np.array(gN), a0))))
        _R[f_][t] = dict(U=float(np.median(u)), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN}, lt=float(np.median(E)))
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("FG1 law done", flush=True); sys.exit(0)
