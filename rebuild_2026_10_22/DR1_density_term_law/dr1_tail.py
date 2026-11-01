# DR1 tail, in NF1's grader namespace after XH1's X-COP helpers. Reads only. Law rows through the grader's own dvecN. kappa = 1/2 FITTED; not theory closed.
import pickle as _pk, time as _tm
_T0 = _tm.time(); _DR = json.loads(os.environ["DR1_RUN"]); _O = os.environ["SL1_OUT"]; _RES = json.load(open(_O)) if os.path.exists(_O) else {}
_C = _pk.load(open(os.path.join(os.environ["UR1_SL1"], "cache", "sl1_cache.pkl"), "rb")); _KY = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
def _tmpl(f_, hk):
    cl = f"{f_}|{hk}"; o = M[cl]; r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]; g = {}
    for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"]); g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"]); g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"])
    g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"]); g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"]); g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"]); g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"]); g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"]); g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"])
    for k, A_one in zip(["G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"], [o["M_all|OUTER"]["A"]] + [x_["A"] for x_ in o["M_terc|OUTER"]]):
        ma, sa = g[k]; g[k] = (A_one, sa * A_one / ma)
    return g
def _comb(gb, gs, a0, rd):
    if rd == "R1": return 0.5 * gb + np.sqrt(0.25 * gb ** 2 + a0 * gs)
    if rd == "R2": return gb + np.sqrt(a0 * gs)
    return np.sqrt(gb ** 2 + a0 * gs)
_LAW = dict(on=False, rd="R1", c=0, mut=None); _dv0 = dvecN; _ST = dict(S=[], Sr={})
def _msrc(Mb, foot):
    Mb = np.maximum(Mb, 1e-300 + 1e-12 * float(Mb[-1])); gb = GE * Mb / RM ** 2; S = np.maximum(np.gradient(np.log(Mb), np.log(RM)), 0.0)
    if _LAW["mut"] == "zero": S = S * 0
    if _LAW["mut"] == "three": S = S * 0 + 3.0
    return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), A0[foot], _LAW["rd"]) / GE, S
def dvecN(i, foot, hk, Msrc):
    if not _LAW["on"]: return _dv0(i, foot, hk, Msrc)
    pp = prep(i, foot, hk); m, S = _msrc(pp["Mb"], foot); r_ = float(1.4 * NX["MPC"]); _ST["S"].append(float(np.interp(r_, RM, S))); return _dv0(i, foot, hk, m)
def _keys(gc, f):
    o = {}; pr = {}
    for hk in HK:
        tp = _tmpl(f, hk); o[hk] = {k: (tp[k][0] - gc["cells"][hk][k]["pred"]) / tp[k][1] for k in _KY}; pr[hk] = {k: gc["cells"][hk][k]["pred"] for k in _KY}
    bad = sorted({k for hk in HK for k in _KY if abs(o[hk][k]) > 2}); return dict(Z=o, bad=bad, n=15 - len(bad), preds=pr)
def _grp(f, rd, c, mut=None):
    a0 = A0[f]; S = np.maximum(np.gradient(np.log(M_H), np.log(XG)), 0.0); S = S * 0 if mut == "zero" else (S * 0 + 3.0 if mut == "three" else S)
    def one(o, dl):
        Mb = 10 ** (o["lM"] + dl) * MS540; a = o["Re"] * KP540 / HERN_RE; u = G540 * Mb / a ** 2; gb = M_H / XG ** 2 * u; g = _comb(gb, gb * (1 + c * S / 3), a0, rd) / u; s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * g * XG, LXG) / 3.0) * G540 * Mb / a; return 0.5 * math.log10(s2) - 3.0
    d = [o["ls"] - one(o, 0.0) for o in GROUPS]; sl = [(one(o, 0.01) - one(o, -0.01)) / 0.02 for o in GROUPS]; st = NSG["class_stats"](d, sl); return dict(Z=st["Z"], mean=st["mean"], verdict=st.get("verdict"))
def _save(): 
    json.dump(_RES, open(_O + ".tmp", "w"), indent=1, default=float); os.replace(_O + ".tmp", _O)
if "K2" not in _RES and _DR.get("k2"):
    gc = grade_clusters("canonical"); ref = _C["clusters"]["NR1_cells"]["canonical"]; a = max(abs(gc["cells"][h][k]["pred"] - ref[h][k]["pred"]) for h in HK for k in _KY); tp = _C["clusters"]["tmpl"]; b = max(abs(_tmpl("canonical", h)[k][i] - tp[f"canonical|{h}"][k][i]) for h in HK for k in _KY for i in (0, 1)); _RES["K2"] = dict(pred=a, tmpl=b); _save(); PREP.clear(); print("K2", a, b, flush=True)
_LAW["on"] = True
for rd, c, ft, mut in _DR["rows"]:
    k = f"{rd}|c{c}|{ft}" + (f"|{mut}" if mut else "")
    if k in _RES: continue
    _LAW.update(rd=rd, c=c, mut=mut); _ST["S"] = []; gc = grade_clusters(ft); PREP.clear(); r = _keys(gc, ft); r["S_1p4Mpc_med"] = float(np.median(_ST["S"])); r["groups"] = _grp(ft, rd, c, mut); _RES[k] = r; _save(); print(k, r["n"], r["bad"], f"{_tm.time() - _T0:.0f} s", flush=True)
_RES["done"] = True; _save(); print("DR1 done", flush=True); sys.exit(0)
