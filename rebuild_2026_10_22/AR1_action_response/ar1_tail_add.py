# AR1 tail, after UR1's helpers. Prints no graded number. kappa = 1/2 FITTED, unused; not theory closed.
import time as _tm
_T0 = _tm.time(); _PT = os.environ["AR1_PART"]; _HE = os.environ["AR1_HERE"]; sys.path.insert(0, _HE); sys.dont_write_bytecode = True; import ar1_solver as _A
_GK = dict(nE=384, nY=64, nT=128); _ORIG = contract; _M = dict(v="blum", stats={}, F=[]); _ST = {}
def _stf(r, M0):
    return _A.Start(r, M0)
def contract(r, Mb, M0, F, gnedin=None):
    if _M["v"] == "blum" or gnedin is not None: return _ORIG(r, Mb, M0, F, gnedin=gnedin)
    return _A.act_contract(r, Mb, M0, F, stats=_M["stats"], **_GK)
_PF = os.environ["SL1_OUT"] + ".part"; _RES = json.load(open(_PF)) if os.path.exists(_PF) else dict(runs={})
def _cells(gc): return {h: {k: dict(pred=gc["cells"][h][k]["pred"], Zg=gc["cells"][h][k]["Z"], meas=gc["cells"][h][k]["meas"]) for k in _KY} for h in HK}
def _go(lab, v):
    if lab in _RES["runs"]: return
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLMAP["mut"] = 1.0; CN1_MODE = "blum"; _M.update(v=v, stats={}); PREP.clear(); gc = grade_clusters("canonical"); r = dict(keys=_keys(gc, "canonical"), cells=_cells(gc), groups=_groups(), xcop=_xcop(), lt={t: _lt(t) for t in _TG}, stats=dict(_M["stats"])); _M["v"] = "blum"; _RES["runs"][lab] = r; json.dump(_RES, open(_PF + ".tmp", "w"), indent=1, default=float); os.replace(_PF + ".tmp", _PF); print(f"AR1 {lab} done {_tm.time() - _T0:.0f} s", flush=True)
_go("EM1|blum", "blum"); _go("EM1|act", "act")
# K3, K7 and the effective response on the clusters' own M0, canonical, h first
if "eff" not in _RES:
    _Cq = {k: [] for k in ("0.05", "0.15", "0.3", "0.46", "1", "r0/2", "r0", "2r0")}; _K3 = 0.0; _K7 = 0.0; hk = HK[0]; _fo = {}
    for _n, i in enumerate(ALLI[::4]):
        i = int(i); pp = prep(i, "canonical", hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE; s, _ = sig_core("canonical", "A_c2b_refit", Mtot, True); r0 = solve_r0(pp["Mfair"], pp["rta"], s); M0 = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0); Mbf = pp["Mb"] + BCGF[i] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2; Fc = float(np.interp(pp["rta"], RM, Mbf)) / pp["Mfair"]; Ma = _A.act_contract(RM, Mbf, M0, Fc, **_GK)[0]; Mb_ = _ORIG(RM, Mbf, M0, Fc)[0]; _K3 = max(_K3, float(np.max(np.abs(_A.act_contract(RM, 0 * RM, M0, 0.0)[0] / np.maximum(M0, 1e-300) - 1)[M0 > 0])))
        if _n % 20 == 0:
            Md = _A.act_contract(RM, Mbf, M0, Fc, nE=768, nY=128, nT=128)[0]; sel = (RM >= 0.1 * r0) & (RM <= pp["rta"]); _K7 = max(_K7, float(np.max(np.abs(Md[sel] / Ma[sel] - 1))))
        for k in _Cq:
            rm = {"r0/2": 0.5 * r0, "r0": r0, "2r0": 2 * r0}.get(k, 0.0) or float(k) * NX["MPC"]; m0 = float(np.interp(rm, RM, M0)); _Cq[k].append((float(np.interp(rm, RM, Ma)) / m0, float(np.interp(rm, RM, Mb_)) / m0, float(np.interp(rm, RM, Mbf)) / m0))
    PREP.clear(); _RES["eff"] = {k: dict(Qact=float(np.median([a[0] for a in v])), Qblum=float(np.median([a[1] for a in v])), fl=float(np.median([a[2] for a in v]))) for k, v in _Cq.items()}; _RES["K3_clusters"] = _K3; _RES["K7_clusters"] = _K7; _RES["cosmic"] = 1 / NAT_RRAT
    json.dump(_RES, open(_PF + ".tmp", "w"), indent=1, default=float); os.replace(_PF + ".tmp", _PF)
json.dump(_RES, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); os.remove(_PF) if os.path.exists(_PF) else None; print("AR1 done", flush=True); sys.exit(0)
