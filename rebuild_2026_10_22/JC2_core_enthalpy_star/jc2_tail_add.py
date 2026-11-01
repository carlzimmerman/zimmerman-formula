# JC2 tail, after UR1's helpers. Reads only.
import time as _tm
from scipy.optimize import brentq as _bq
_T0 = _tm.time(); _MUT = os.environ.get("JC2_MUTATE") == "1"; _OUTF = os.environ["SL1_OUT"]; _R = dict(rows={}, clusters={}, edge={}); JM = ["k"]; _E = []
def _r0_slope(r, M0):
    i = len(r) // 3; s = (math.log(M0[i + 2]) - math.log(M0[i - 2])) / (math.log(r[i + 2]) - math.log(r[i - 2])); h = lambda x: float(np.log(B(x * 1.02) / B(x / 1.02)) / np.log(1.02 ** 2))
    try: return r[i] / _bq(lambda x: h(x) - s, 1e-3, 1e4)
    except ValueError: return r[i]
def _share(r):
    fr = sys._getframe(2)
    while fr is not None:
        L = fr.f_locals
        if "q" in L and "iu" in L and "U" in L and "UPS_G" in fr.f_globals:
            q = L["q"]; G = q["GB"]; U_ = fr.f_globals["UPS_G"]; R_ = q["Rm"]; k = R_ ** 2 / GE; M1 = np.maximum.accumulate(np.maximum(G[:, 0] * k, 0.0)); M2 = np.maximum.accumulate(np.maximum(G[:, -1] * k, 0.0)); Mu = np.maximum(G[:, L["iu"]] * k, 1e-300); Mg = np.maximum(M1 - U_[0] * (M2 - M1) / (U_[-1] - U_[0]), 0.0); sh = np.clip(1 - Mg / Mu, 0, 1); _SH.setdefault(q["name"], float(np.median(sh))); return np.interp(np.log(r), np.log(R_), sh)
        if fr.f_code.co_name == "one": return np.ones_like(r)
        fr = fr.f_back
    return np.zeros_like(r)
_SH = {}
def contract(r, Mb, M0, F, gnedin=None):
    lr = np.log(r); Mb_at = lambda x: np.interp(np.log(np.maximum(x, r[0])), lr, Mb, left=Mb[0], right=Mb[-1]); m = JM[0]
    r0 = _r0_slope(r, M0); Ms = np.maximum(M0 + float(np.interp(math.log(r0), lr, M0)) * r / r0, 1e-300); _E.append(float(Ms[-1] / M0[-1])); sh = 0.0 * r if (m.endswith("0") or _MUT) else _share(r); Ms_ = Mb * sh; rf = r.copy()
    for _ in range(100):
        ch = (np.interp(np.log(np.maximum(rf, r[0])), lr, Ms_) / Ms) ** 2; top = np.ones_like(r) if m.startswith("lit") else 1 + (F * M0 / Ms) / (1 + ch); new = r * top / (1 + (Mb_at(rf) / Ms) / (1 + ch)); rf = 0.5 * rf + 0.5 * new
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
JM[0] = "lit0"; _R["rows"]["lit0|+0.00"] = _cell(0.0); JM[0] = "norm0"; _R["rows"]["norm0|+0.00"] = _cell(0.0); _dump()
for m in ("lit", "norm"):
    JM[0] = m; _E.clear(); _R["clusters"][m] = _clu()
    for d in (-0.10, -0.05, 0.0, 0.05, 0.10):
        _R["rows"][f"{m}|{d:+.2f}"] = _cell(d); _dump()
        if _MUT: break
    _R["edge"][m] = dict(min=min(_E), median=float(np.median(_E)), max=max(_E)); _R["share"] = dict(_SH); _dump(); print("JC2", m, _R["clusters"][m]["n"], f"{_tm.time() - _T0:.0f} s", flush=True)
print("JC2 done", flush=True); sys.exit(0)
