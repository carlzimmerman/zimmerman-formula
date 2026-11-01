# SP3 hand-core tail, after UR1's helpers, read only. No keys here: they don't read the map.
import time as _tm
_T0 = _tm.time(); _SPT = json.load(open(os.environ["SP3_TABLES"]))
def _setT(nm):
    SLMAP["m"] = "RET"; SLMAP["f"] = lambda lMb, bg, rc: 10 ** float(np.interp(lMb, _SPT[nm][next(t for t in _TG if BGS[t] is bg)]["x"], _SPT[nm][next(t for t in _TG if BGS[t] is bg)]["y"]))
def _run2(mp, mode):
    global CN1_MODE
    SLMAP["m"] = mp; CN1_MODE = mode; GHSTORE.clear(); r = dict(map=mp, mode=mode, sparc={}, Ugal={})
    if mp != "EM1" and mp != "FAIR200": _setT(mp); 
    for t in _TG:
        st = sparc("canonical", t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN}); r["Ugal"][t] = U
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; print(f"SP3 {mp} {mode} {_tm.time() - _T0:.0f} s", flush=True); return r
_R = dict(runs={})
for mp, mo in (("EM1", "off"), ("EM1", "blum"), ("E1", "off"), ("C1", "off"), ("AM1", "off"), ("AM1", "blum")): _R["runs"][f"{mp}|{mo}"] = _run2(mp, mo)
_U = MSUNE / (MPCE / 1e3) ** 2; _G = np.arange(9.0, 15.01, 0.05); _J = dict(lgM=_G.tolist(), S={}, bg={})
for t in _TG:
    _J["S"][t] = [float(sig_core("canonical", t, 10 ** g / FC1_MC)[0] / _U) for g in _G]; _J["bg"][t] = dict(a=BGS[t]["a"], b=BGS[t]["b"], h=BGS[t]["h"])
_R["Stable"] = _J
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("SP3 hand done", flush=True); sys.exit(0)
