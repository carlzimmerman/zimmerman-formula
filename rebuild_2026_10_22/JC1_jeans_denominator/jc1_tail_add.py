# JC1 tail, after UR1's helpers. Reads only.
import time as _tm
from scipy.optimize import brentq as _bq
_T0 = _tm.time(); _MUT = os.environ.get("JC1_MUTATE") == "1"; _OUTF = os.environ["SL1_OUT"]; _R = dict(rows={}, clusters={}, edge={}); JM = ["k"]; _E = []
def _r0_slope(r, M0):
    i = len(r) // 3; s = (math.log(M0[i + 2]) - math.log(M0[i - 2])) / (math.log(r[i + 2]) - math.log(r[i - 2])); h = lambda x: float(np.log(B(x * 1.02) / B(x / 1.02)) / np.log(1.02 ** 2))
    try: return r[i] / _bq(lambda x: h(x) - s, 1e-3, 1e4)
    except ValueError: return r[i]
def contract(r, Mb, M0, F, gnedin=None):
    lr = np.log(r); Mb_at = lambda x: np.interp(np.log(np.maximum(x, r[0])), lr, Mb, left=Mb[0], right=Mb[-1]); m = JM[0]
    if m == "k": Ms = 2 * M0 if _MUT else M0
    else: r0 = _r0_slope(r, M0); Ms = M0 + float(np.interp(math.log(r0), lr, M0)) * r / r0; _E.append(float(Ms[-1] / M0[-1]))
    top = np.ones_like(r) if m == "lit" else 1 + F * M0 / np.maximum(Ms, 1e-300); rf = r.copy()
    for _ in range(100): new = r * top / (1 + Mb_at(rf) / np.maximum(Ms, 1e-300)); rf = 0.5 * rf + 0.5 * new
    conv = float(np.max(np.abs(new / rf - 1))); order = np.maximum.accumulate(rf); cross = int(np.sum(rf < order - 1e-12 * order)); return np.interp(lr, np.log(order), M0, left=0.0, right=M0[-1]), conv, cross
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
_R["rows"]["k|+0.00"] = (lambda: _cell(0.0))(); _dump()
if _MUT: sys.exit(0)
for m in ("lit", "norm"):
    JM[0] = m; _E.clear(); _R["clusters"][m] = _clu()
    for d in (-0.10, -0.05, 0.0, 0.05, 0.10): _R["rows"][f"{m}|{d:+.2f}"] = _cell(d); _dump()
    _R["edge"][m] = dict(min=min(_E), median=float(np.median(_E)), max=max(_E)); _dump(); print("JC1", m, _R["clusters"][m]["n"], f"{_tm.time() - _T0:.0f} s", flush=True)
print("JC1 done", flush=True); sys.exit(0)
