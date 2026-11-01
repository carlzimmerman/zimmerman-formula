# CP1 tail, appended after UR1's helpers in NF1's grader namespace. Reads only. kappa = 1/2 FITTED; not theory closed. CHOSEN: V_crit 250, n 4.
import time as _tm
_T0 = _tm.time(); _A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); _F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
def _om(tag): p = _F3[tag]["params"]; return (p["omega_b"] + p["omega_cdm"]) / p["h"] ** 2
def _ode(z, tag): m = _om(tag); return (1 - m) / (m * (1 + z) ** 3 + 1 - m)
def _chi(V, Vc, n, z=0.0, tag="A_c2b_refit"): return _ode(z, tag) / _ode(0.0, tag) * math.exp(-(V / Vc) ** n)
_NVF = [0]
def _vof(q):
    t = _TB.get(q["name"])
    if t and t["vf"] > 0: return t["vf"]
    i = np.where(q["OK"])[0][-3:]; _NVF[0] += 1; return float(np.mean(np.sqrt(q["GO"][i] * q["Rm"][i]))) / 1e3
_GF = {}
def _gc(q, f, tag, M2, R2, s, xc):
    """(n_pts, n_ups) G M_f[xc M_c0] / r^2, as CN1's loop."""
    if xc < 1e-9: return np.zeros_like(q["GB"])
    if xc > 1 - 1e-12 and (f, tag, q["name"]) in _GF: return _GF[(f, tag, q["name"])]
    r0 = solve_r0(M2 * MSUNE, R2, s); R_ = q["Rm"]; rg = np.geomspace(R_[0] * 0.05, R2, 300); M0 = xc * math.pi * s * r0 ** 2 * B(rg / r0); gh = np.zeros((len(R_), len(UPS_G)))
    for iu, U in enumerate(UPS_G):
        Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
        Mbg = np.where(rg < R_[0], Mbk[0] * (rg / R_[0]) ** 2, np.interp(np.log(rg), np.log(R_), Mbk)); o_ = rg > R_[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / R_[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        gh[:, iu] = GE * np.interp(np.log(R_), np.log(rg), contract(rg, np.maximum.accumulate(Mbg), M0, Mt / (xc * M2 * MSUNE))[0]) / R_ ** 2
    if xc > 1 - 1e-12: _GF[(f, tag, q["name"])] = gh
    return gh
def _full(q, f, tag, M2, R2, s): return _gc(q, f, tag, M2, R2, s, 1.0)
def _sparcmix(tag, f, Vc, n, readings=("R1",), om1=False):
    """returns {reading: dict}. om1: Omega ratio is 1 anyway at z = 0."""
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); a0 = _A0[f]; O = {}; Rw = {k: [] for k in readings}; Xp = {}
    for q in GALS:
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); xp = _chi(_vof(q), Vc, n, 0.0, tag); xc = 1 - xp; Xp[q["name"]] = (xp, xc, M2); GB = q["GB"]; gp = (0.5 + np.sqrt(0.25 + a0 / np.maximum(GB, 1e-300))) * GB
        gcx = _gc(q, f, tag, M2, R2, s, xc) if ("R1" in readings or "R2" in readings) else None
        for r_ in readings:
            if r_ == "R1": g = xp * gp + xc * GB + gcx
            elif r_ == "R2": g = xp * gp + xc * (GB + gcx)
            elif r_ == "R3": g = xp * gp + xc * (GB + _full(q, f, tag, M2, R2, s))
            elif r_ == "MUT": g = xp * gp + GB + _full(q, f, tag, M2, R2, s)
            elif r_ == "PLAIN": g = GB + _full(q, f, tag, M2, R2, s)
            Rw[r_].append((q["name"], fit_one(q, np.log10(np.maximum(g, 1e-300)))))
    for r_, rows in Rw.items():
        u = {n_: float(UPS[int(x[2])]) for n_, x in rows}; rms = float(math.sqrt(sum(x[0] for _, x in rows) / sum(x[1] for _, x in rows))); U = float(np.median(list(u.values())))
        v = np.array([_TB[k]["vf"] if k in _TB else np.nan for k in u]); Q = np.array([(_TB[k]["Q"] <= 2 and _TB[k]["inc"] >= 30) if k in _TB else False for k in u]); uu = np.array(list(u.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150)
        O[r_] = dict(U=U, rms=rms, line=bool(rms <= 0.110 and 0.5 <= U <= 0.8), tilt=float(np.median(uu[lo]) - np.median(uu[hi])), bins={f"{l}-{h}": float(np.median(uu[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    return O, Xp
def _gmix(Vc, n, reading="R1", f="canonical"):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540); a0 = _A0[f]; d = []; sl = []; X = []
    def one(o, dl):
        lMb = o["lM"] + dl; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE; M2, R2 = _SL3M(lMb, bg, rc); s, _ = sig_core(f, "A_c2b_refit", M2 / FC1_MC); r0 = solve_r0(M2 * MS540, R2, s); rr = XG * a; xp = _chi(math.sqrt(2) * 10 ** o["ls"], Vc, n); xc = 1 - xp
        rg = np.geomspace(min(rr[0], R2 * 1e-4), R2, 800); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = np.interp(np.log(rg), np.log(rr), Mb * M_H)
        if reading == "R3" or reading == "MUT": Mc = np.interp(np.log(rr), np.log(rg), _resp(rg, Mbg, M0g, float(Mbg[-1] / M0g[-1])))
        elif xc < 1e-9: Mc = np.zeros_like(rr)
        else: Mc = np.interp(np.log(rr), np.log(rg), _resp(rg, Mbg, xc * M0g, float(Mbg[-1] / (xc * M0g[-1]))))
        gb_ = M_H / XG ** 2; gphys = G540 * Mb / a ** 2 * gb_; nu = 0.5 + np.sqrt(0.25 + a0 / np.maximum(gphys, 1e-300)); gc_ = Mc / Mb / XG ** 2
        gN = {"R1": xp * nu * gb_ + xc * gb_ + gc_, "R2": xp * nu * gb_ + xc * (gb_ + gc_), "R3": xp * nu * gb_ + xc * (gb_ + gc_), "MUT": xp * nu * gb_ + gb_ + gc_}[reading]
        s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a; return 0.5 * math.log10(s2) - 3.0, xp
    for o in GROUPS: y, xp = one(o, 0.0); X.append(xp); d.append(o["ls"] - y); sl.append((one(o, 0.01)[0] - one(o, -0.01)[0]) / 0.02)
    st = NSG["class_stats"](d, sl); st["chi_pol_median"] = float(np.median(X)); return st
def _ltmix(tag, Vc, n, reading="R1", f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); a0 = _A0[f]; E = []
    for r_ in _C["lt"]:
        M2, R2 = _SL3M(r_["logMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); R_ = r_["R"] * MPCE / 1e3; Mb = 10 ** r_["logMb"] * MSUNE; rg = np.geomspace(R_ * 1e-3, R2, 600); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = Mb * np.minimum(rg / R_, 1.0) ** 2; xp = _chi(r_["V"], Vc, n, 0.0, tag); xc = 1 - xp
        if reading in ("R3", "MUT"): Mc = float(np.interp(math.log(R_), np.log(rg), _resp(rg, Mbg, M0g, Mb / (M2 * MSUNE))))
        elif xc < 1e-9: Mc = 0.0
        else: Mc = float(np.interp(math.log(R_), np.log(rg), _resp(rg, Mbg, xc * M0g, Mb / (xc * M2 * MSUNE))))
        gb_ = GE * Mb / R_ ** 2; gp = gb_ * (0.5 + math.sqrt(0.25 + a0 / gb_)); gc_ = GE * Mc / R_ ** 2
        g = {"R1": xp * gp + xc * gb_ + gc_, "R2": xp * gp + xc * (gb_ + gc_), "R3": xp * gp + xc * (gb_ + gc_), "MUT": xp * gp + gb_ + gc_}[reading]; E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(g))
    return float(np.median(E))
def _row(Vc, n, readings=("R1", "R2", "R3"), f="canonical", gl=True):
    o = {}; Xs = None
    S = {t: _sparcmix(t, f, Vc, n, readings)[0] for t in _TG}
    for r_ in readings:
        o[r_] = dict(sparc={t: S[t][r_] for t in _TG})
        if gl: o[r_]["groups"] = _gmix(Vc, n, r_ if r_ != "PLAIN" else "R1"); o[r_]["lt"] = {t: _ltmix(t, Vc, n, r_ if r_ != "PLAIN" else "R1") for t in _TG}
    print(f"CP1 row Vc {Vc} n {n} {f} {readings} {_tm.time() - _T0:.0f} s", flush=True); return o
def _block(r): s = r["sparc"]; return dict(line=all(s[t]["line"] for t in _TG), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in _TG), groups=abs(r["groups"]["Z"]) <= 2, lt=all(abs(r["lt"][t]) <= 0.10 for t in _TG))
def _k4():
    global dvecN
    # K4 cluster invariance: the mix on through dvecN against off, both modes; rho_c from background A
    _bg = BGS["A_c2b_refit"]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _dv0 = dvecN; _CH = []
    def _wr(i, foot, hk, Msrc):
        pp = prep(i, foot, hk); rho = Msrc / (4 / 3 * math.pi * RM ** 3); j = int(np.where(rho >= 200 * _rc)[0][-1]); R2_ = RM[j]; V2 = math.sqrt(GE * Msrc[j] / R2_) / 1e3; xp = _chi(V2, 250.0, 4.0); _CH.append((V2, xp, i, hk, float(pp["Mfair"] / MSUNE), float(Mb_0 / MSUNE) if False else float(pp["Mb"][-1] / MSUNE), float(pp["rta"] / 3.0857e22), float(R2_ / 3.0857e22))); Mb_ = pp["Mb"]; gb_ = GE * Mb_ / RM ** 2; gp = gb_ * (0.5 + np.sqrt(0.25 + _A0[foot] / np.maximum(gb_, 1e-300)))
        return _dv0(i, foot, hk, xp * gp * RM ** 2 / GE + (1 - xp) * Msrc)
    dvecN = _wr; _on = grade_clusters("canonical"); PREP.clear(); dvecN = _dv0; _off = grade_clusters("canonical"); PREP.clear()
    _R["K4"] = max(abs(_on["cells"][h][k]["pred"] - _off["cells"][h][k]["pred"]) for h in HK for k in _KY); _R["K4_minV200"] = min(a[0] for a in _CH); _R["K4_maxchi"] = max(a[1] for a in _CH); _v = np.array([a[0] for a in _CH]); _R["K4_V200_pct"] = [float(np.percentile(_v, p)) for p in (0, 1, 5, 16, 50, 84, 100)]; _R["K4_n_V_under_400"] = int((_v < 400).sum()); _R["K4_n"] = len(_v); _R["K4_by_key"] = {h: {k: dict(on=_on["cells"][h][k]["pred"], off=_off["cells"][h][k]["pred"], Z_on=(_TP[f"canonical|{h}"][k][0] - _on["cells"][h][k]["pred"]) / _TP[f"canonical|{h}"][k][1], Z_off=(_TP[f"canonical|{h}"][k][0] - _off["cells"][h][k]["pred"]) / _TP[f"canonical|{h}"][k][1]) for k in _KY} for h in HK}; _ii = np.array([a[2] for a in _CH]); _R["K4_V200_by_massterc"] = {str(t_): dict(min=float(_v[np.isin(_ii, np.where(T3M == t_)[0])].min()), max_chi=float(max(a[1] for a in _CH if T3M[a[2]] == t_)), n_chi_over_1e3=len({a[2] for a in _CH if T3M[a[2]] == t_ and a[1] > 1e-3})) for t_ in range(3)}; _R["K4_n_clusters_chi_over_1e3"] = len({a[2] for a in _CH if a[1] > 1e-3}); _R["K4_catalog_low"] = [dict(i=int(j), Mgas500=float(NX["MY"]["Mgas500"][j]), z=float(NX["MY"]["z"][j]), fields=list(NX["MY"].dtype.names)[:30] if hasattr(NX["MY"], "dtype") else list(NX["MY"].keys())[:30]) for j in (60, 88)]; _R["K4_low"] = [list(x) for x in sorted(_CH, key=lambda y: y[0])[:6]]; _R["K4_pmed"] = list(sorted(_CH, key=lambda y: y[0])[len(_CH)//2]); _R["K4_keyN"] = int(N)
SLMAP["m"] = "EM1"; CN1_MODE = "blum"; _MODE = os.environ["CP1_MODE"]; _R = dict(mode=_MODE)
if _MODE == "k4":
    _k4(); print(_R, flush=True)
elif _MODE == "mutate":
    _R["MUTATE"] = _row(250.0, 4.0, ("MUT", "R1"))
elif _MODE == "r2band":
    _R["R2"] = _row(250.0, 4.0, ("R2",))["R2"]
elif _MODE == "r2full":
    _R["R2"] = _row(250.0, 4.0, ("R2",))["R2"]; _R["alt"] = {t: _sparcmix(t, "alt", 250.0, 4.0, ("R2",))[0]["R2"] for t in _TG}; _R["alt_lt"] = {t: _ltmix(t, 250.0, 4.0, "R2", "alt") for t in _TG}; _R["sens"] = {}
    for _n in (2.0, 4.0):
        for _v in (200.0, 225.0, 250.0, 275.0, 300.0):
            if _v == 250.0 and _n == 4.0: continue
            _R["sens"][f"{_v:g}|{_n:g}"] = _row(_v, _n, ("R2",))["R2"]
elif _MODE == "band":
    _R["primary"] = _row(250.0, 4.0, ("R1",))
else:
    _R["forest"] = {t: dict(Om=_om(t), ratio=_ode(3.0, t) / _ode(0.0, t), chi_pol=_chi(150.0, 250.0, 4.0, 3.0, t)) for t in _TG}
    _K0 = _run("EM1", "blum"); _R["EM1_blum_harness"] = _K0; CN1_MODE = "blum"; SLMAP["m"] = "EM1"
    _R["limit_0"] = _row(1e-3, 4.0, ("R1",)); _R["limit_inf"] = _row(1e7, 4.0, ("R1",)); _R["primary"] = _row(250.0, 4.0); _R["primary"]["nofallback_note"] = _NVF[0]
    _R["alt"] = {t: _sparcmix(t, "alt", 250.0, 4.0)[0]["R1"] for t in _TG}; _R["alt_lt"] = {t: _ltmix(t, 250.0, 4.0, "R1", "alt") for t in _TG}; _R["alt_law_limit"] = {t: _sparcmix(t, "alt", 1e7, 4.0)[0]["R1"] for t in _TG}
    _R["sens"] = {}
    for _n in (2.0, 4.0):
        for _v in (200.0, 225.0, 250.0, 275.0, 300.0):
            if _v == 250.0 and _n == 4.0: continue
            _R["sens"][f"{_v:g}|{_n:g}"] = _row(_v, _n, ("R1",))["R1"]
    # K3, what the rule does to the cold mass by V bin, canonical, background A
    _, _Xp = _sparcmix("A_c2b_refit", "canonical", 250.0, 4.0, ("R1",)); _k3 = 0.0; _M = {f"{l}-{h}": [] for l, h in _BIN}
    for q in GALS:
        xp, xc, M2 = _Xp[q["name"]]; _k3 = max(_k3, abs(xp + xc - 1)); v = _vof(q)
        for l, h in _BIN:
            if l <= v < h: _M[f"{l}-{h}"].append((xp, M2, NAT_RRAT * 10 ** q["lMb"], 10 ** q["lMb"]))
    _R["K3"] = _k3; _R["cold_by_bin"] = {k: dict(n=len(v), chi_pol=float(np.median([a[0] for a in v])), M200=float(np.median([a[1] for a in v])), fair=float(np.median([a[2] for a in v])), missing_M200=float(np.median([a[0] * a[1] for a in v])), remaining_over_Mb=float(np.median([(1 - a[0]) * a[1] / a[3] for a in v])), missing_total_over_all_M200=float(sum(a[0] * a[1] for a in v))) for k, v in _M.items() if v}; _R["total_M200"] = float(sum(a[1] for v in _M.values() for a in v))
    _k4()
    _x = []
    for c_ in _XC: nm = c_["name"]; Mbt, rta = _budget(nm); _Mt = (NAT_RRAT + 1) * Mbt; _x.append(math.sqrt(GE * (_Mt * 0.29) / (3 * (_Mt * 0.29) / (4 * math.pi * 200 * _rc)) ** (1 / 3)) / 1e3)
    _R["xcop_V200_min"] = min(_x); _R["n_vflat_fallback"] = sum(1 for q in GALS if not (_TB.get(q["name"]) and _TB[q["name"]]["vf"] > 0))
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("CP1 done", flush=True); sys.exit(0)
