# NR4 tail, after UR1's helpers. Reads only.
_ORIG = contract; _F = [1.0]; _FLIP = os.environ.get("NR4_FLIP") == "1"
def contract(r, Mb, M0, F, gnedin=None):
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin); f = 1 - _F[0] if _FLIP else _F[0]
    return (np.maximum.accumulate(M0 + f * (o[0] - M0)),) + tuple(o[1:])
def _cell():
    global CN1_MODE
    SLMAP["m"] = "EM1"; CN1_MODE = "blum"; GHSTORE.clear(); r = dict(sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; return r
_R = {}
for _x in json.loads(os.environ["NR4_FS"]):
    _F[0] = _x; _R[f"{_x:g}"] = _cell(); json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print(f"NR4 f {_x}", flush=True)
print("NR4 done", flush=True); sys.exit(0)
