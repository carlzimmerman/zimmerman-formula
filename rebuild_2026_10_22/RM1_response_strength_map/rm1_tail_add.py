# RM1 tail, after UR1's helpers. Reads only.
import time as _tm
_T0 = _tm.time(); SLDL[0] = 0.0; _PT = os.environ["RM1_PART"]; _OUTF = os.environ["SL1_OUT"]; _R = dict(part=_PT, rows={}, clusters={}); _ORIG = contract; _FG = [1.0]; _FI = [None]; _FLIP = _PT == "MUTATE"
def contract(r, Mb, M0, F, gnedin=None):
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin); Mc = o[0]
    if _FI[0] is None: f = _FG[0]
    else:
        rh = float(np.interp(0.5 * Mb[-1], Mb, r)); t = np.clip(np.log(r / rh) / math.log(3.0), 0, 1); f = _FI[0] + (1 - _FI[0]) * t * t * (3 - 2 * t)
    if _FLIP: f = 1 - f
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
_D = [round(-0.30 + 0.05 * i, 2) for i in range(12)]
def _go(lab):
    _R["clusters"][lab] = _clu()
    for d in _D:
        _R["rows"][f"{lab}|{d:+.2f}"] = _cell(d); json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
    print(f"RM1 {lab} keys {_R['clusters'][lab]['n']} {_tm.time() - _T0:.0f} s", flush=True)
if _PT == "G":
    for i in range(10, -1, -1): _FG[0] = i / 10; _go(f"G{i / 10:.1f}")
elif _PT == "I":
    for x in (0.0, 0.25, 0.5, 0.75): _FI[0] = x; _go(f"I{x:.2f}")
else:
    _D = [0.0]; _FG[0] = 1.0; _go("G1.0")
print("RM1 done", flush=True); sys.exit(0)
