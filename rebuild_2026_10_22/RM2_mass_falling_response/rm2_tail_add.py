# RM2 tail, after UR1's helpers. Reads only.
import time as _tm
_T0 = _tm.time(); SLDL[0] = 0.0; _MUT = os.environ.get("RM2_MUTATE") == "1"; _OUTF = os.environ["SL1_OUT"]; _R = dict(rows={}, clusters={}, mb=[]); _ORIG = contract; _FM = [10.0, 1.0]
def contract(r, Mb, M0, F, gnedin=None):
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin); Mc = o[0]; m = float(Mb[-1]); lm = math.log10(m / (MSUNE if m > 1e30 else 1.0)); _R["mb"] = [min(_R["mb"][0], lm), max(_R["mb"][1], lm)] if _R["mb"] else [lm, lm]
    t = float(np.clip((lm - _FM[0] + 0.5), 0, 1)); S = t * t * (3 - 2 * t); f = _FM[1] + (1 - _FM[1]) * (1 - S); f = 1 - f if _MUT else f
    return (np.maximum.accumulate(M0 + f * (Mc - M0)),) + tuple(o[1:])
def _cell(d):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLDL[0] = d; CN1_MODE = "blum"; GHSTORE.clear(); r = dict(delta=d, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; return r
def _clu():
    global CN1_MODE
    CN1_MODE = "blum"; GHSTORE.clear(); PREP.clear(); gc = grade_clusters("canonical"); k = _keys(gc, "canonical"); PREP.clear(); return dict(bad=k["bad"], n=k["n"], Z=k["Z"], xcop=_xcop())
def _dump(): json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
_FM[:] = [10.0, 1.0]; _R["rows"]["K|10.0|1.0|+0.00"] = _cell(0.0); _dump()
if _MUT: print("RM2 done", flush=True); sys.exit(0)
for lc in (9.5, 10.0, 10.5):
    for fh in (0.0, 0.2, 0.4, 0.6, 0.8):
        _FM[:] = [lc, fh]; _R["clusters"][f"{lc}|{fh}"] = _clu()
        for d in (-0.10, -0.05, 0.0, 0.05, 0.10): _R["rows"][f"{lc}|{fh}|{d:+.2f}"] = _cell(d); _dump()
        print(f"RM2 {lc} {fh} keys {_R['clusters'][f'{lc}|{fh}']['n']} {_tm.time() - _T0:.0f} s", flush=True)
print("RM2 done", flush=True); sys.exit(0)
