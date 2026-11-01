# GT1 tail, after UR1's helpers; contract wrapped. Reads only.
import time as _tm
from scipy.optimize import brentq as _bq
_T0 = _tm.time(); _OUTF = os.environ["SL1_OUT"]; _ORIG = contract; GT = dict(m=None, a=1.0, j=1.0, rotating=True); _A0 = 9.36e-11
def _r0_slope(r, M0):
    i = len(r) // 3; s = (math.log(M0[i + 2]) - math.log(M0[i - 2])) / (math.log(r[i + 2]) - math.log(r[i - 2])); h = lambda x: float(np.log(B(x * 1.02) / B(x / 1.02)) / np.log(1.02 ** 2))
    try: return r[i] / _bq(lambda x: h(x) - s, 1e-3, 1e4)
    except ValueError: return r[i]
def contract(r, Mb, M0, F, gnedin=None):
    m = GT["m"]
    if m is None or not GT["rotating"]: return _ORIG(r, Mb, M0, F, gnedin=gnedin)
    if m == "h10":
        a0 = _A0 * GT["a"]; gb = GE * Mb / r ** 2; Me = Mb * a0 / (gb + a0); return _ORIG(r, Me, M0, float(Me[-1] / M0[-1]), gnedin=gnedin)
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin); r0 = _r0_slope(r, M0); Vc0 = math.sqrt(GE * float(np.interp(math.log(r0), np.log(r), M0)) / r0); jc = r0 * Vc0 * GT["j"]; jb = r * np.sqrt(np.maximum(GE * Mb / r, 0.0)); fac = 1 / (1 + (jb / jc) ** 2)
    return ((o[0] * fac) if m == "j7" else (M0 + (o[0] - M0) * fac), o[1], o[2])
def _run3(d, m, keys=False, **kw):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLDL[0] = d; CN1_MODE = "blum"; GT.update(m=m, a=1.0, j=1.0, rotating=True); GT.update(kw); GHSTORE.clear(); r = dict(delta=d, m=m, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), lowU=float(np.median(u[lo])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["lt"] = {t: _lt(t) for t in _TG}
    if m != "h10": GT["rotating"] = False
    r["groups"] = _groups()
    if keys: gc = grade_clusters(f); r["keys"] = _keys(gc, f); r["xcop"] = _xcop()
    GT["rotating"] = True; print(f"GT1 {m} {d:+.2f} {kw} U {r['sparc'][_TG[0]]['U']:.3f} tilt {r['sparc'][_TG[0]]['tilt']:+.2f} {_tm.time() - _T0:.0f} s", flush=True); return r
_R = dict(rows={})
_R["rows"]["K1"] = _run3(0.0, None)
for d in (0.0, 0.10):
    _R["rows"][f"h10|{d:+.2f}"] = _run3(d, "h10", keys=d == 0.0); _R["rows"][f"j7|{d:+.2f}"] = _run3(d, "j7"); _R["rows"][f"j7b|{d:+.2f}"] = _run3(d, "j7b")
    json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
_R["MUT_h10"] = _run3(0.10, "h10", a=10.0); _R["MUT_j7b"] = _run3(0.10, "j7b", j=0.1)
_chi = []
for q in GALS:
    iu = int(np.argmin(abs(UPS - 0.5))); gb = np.maximum(q["GB"][:, iu], 0); Vb2 = gb * q["Rm"]; ok = gb > 0; _chi.append(np.minimum(1.0, 2 * (0.5 * Vb2[ok]) / (gb[ok] * q["Rm"][ok])))
_chi = np.concatenate(_chi); _R["K2"] = [float(_chi.min()), float(_chi.max())]
_bg = BGS["A_c2b_refit"]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _M2, _R2 = _SL3M(11.0, _bg, _rc); _s, _ = sig_core("canonical", "A_c2b_refit", _M2 / FC1_MC); _r0 = solve_r0(_M2 * MSUNE, _R2, _s); _rg = np.geomspace(_R2 * 1e-4, _R2, 400); _R["K3"] = abs(_r0_slope(_rg, math.pi * _s * _r0 ** 2 * B(_rg / _r0)) / _r0 - 1)
json.dump(_R, open(_OUTF, "w"), indent=1, default=float); print("GT1 done", flush=True); sys.exit(0)
