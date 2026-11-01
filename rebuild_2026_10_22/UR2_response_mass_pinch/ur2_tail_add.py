# UR2 tail, after UR1's helpers. Reads only. Clusters and X-COP don't read the map, so they're not rerun.
import time as _tm
_T0 = _tm.time(); SLDL[0] = 0.0; _OUTF = os.environ["SL1_OUT"]; _R = dict(rows={}); _ORIG = contract; _MUT = [1.0]
def contract(r, Mb, M0, F, gnedin=None): return _ORIG(r, Mb * _MUT[0], M0, F, gnedin=gnedin)
def _run2(d, mode):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLDL[0] = d; CN1_MODE = mode; GHSTORE.clear(); r = dict(delta=d, mode=mode, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; print(f"UR2 {mode} {d:+.2f} U {r['sparc'][_TG[0]]['U']:.3f} {_tm.time() - _T0:.0f} s", flush=True); return r
_G = [round(-0.5 + 0.05 * i, 2) for i in range(15)]
for mo in ("off", "blum", "gnedin"):
    for d in _G:
        _R["rows"][f"{mo}|{d:+.2f}"] = _run2(d, mo); json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
_MUT[0] = 2.0; _R["MUTATE"] = {f"{d:+.2f}": _run2(d, "blum") for d in _G[::2]}; _MUT[0] = 1.0
json.dump(_R, open(_OUTF, "w"), indent=1, default=float); print("UR2 done", flush=True); sys.exit(0)
