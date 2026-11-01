# SR1 tail, after UR1's helpers; contract wrapped; caller's arrays read from its frame, nothing altered.
import time as _tm
_T0 = _tm.time(); _OUTF = os.environ["SL1_OUT"]; _ORIG = contract; GT = dict(m=None, ms=1.0, ex=None); _EF = {}
_RD = {}
for _l in open(_MRT):
    _p = _l.split()
    if len(_p) < 18: continue
    try: _RD[_p[0]] = float(_p[11])
    except ValueError: pass
def _core(r, Mb, Mst, M0, F, lit):
    lr = np.log(r); at = lambda y, x: np.interp(np.log(np.maximum(x, r[0])), lr, y); rf = r.copy()
    for _ in range(100):
        Mb_ = at(Mb, rf); chi = at(Mst, rf) / np.maximum(M0, 1e-300); Me = Mb_ / (1 + chi ** 2)
        rn = r / (1 + Me / np.maximum(M0, 1e-300)) if lit else r * M0 * (1 + F) / np.maximum(Me + M0, 1e-300)
        rf = 0.5 * rf + 0.5 * rn
    order = np.maximum.accumulate(rf); return np.interp(lr, np.log(order), M0, left=0.0, right=M0[-1]), float(np.max(np.abs(rn / rf - 1))), 0
def contract(r, Mb, M0, F, gnedin=None):
    m = GT["m"]
    if m is None: return _ORIG(r, Mb, M0, F, gnedin=gnedin)
    fr = sys._getframe(1); L = fr.f_locals; lit = m == "lit"
    if "q" in L and "UPS_G" in globals():
        q = L["q"]; R_ = q["Rm"]; gs = (q["GB"][:, -1] - q["GB"][:, 0]) / (UPS_G[-1] - UPS_G[0]); Ms = np.maximum.accumulate(np.maximum(0.5 * gs * R_ ** 2 / GE, 0.0)); Mt = max(float(Ms[-1]), 0.5 * q["meta"]["L36"] * 1e9 * MSUNE); y = np.where(r < R_[0], Ms[0] * (r / R_[0]) ** 2, np.interp(np.log(r), np.log(R_), Ms)); o_ = r > R_[-1]
        if o_.any(): t_ = np.clip(np.log(r[o_] / R_[-1]) / math.log(3.0), 0, 1); y[o_] = np.exp(np.log(max(Ms[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        y = np.maximum.accumulate(y) * GT["ms"]; O = _core(r, Mb, y, M0, F, lit)
        if abs(L.get("U", 0) - 0.5) < 1e-9 and q["name"] in _RD and _RD[q["name"]] > 0:
            x = math.log(2.2 * _RD[q["name"]] * MPCE / 1e3); B1 = _ORIG(r, Mb, M0, F)[0]; a = float(np.interp(x, np.log(r), O[0] - M0)); b = float(np.interp(x, np.log(r), B1 - M0)); _EF[q["name"]] = dict(f=a / b if b > 0 else float("nan"), chi=float(np.interp(x, np.log(r), y) / np.interp(x, np.log(r), M0)))
        return O
    if "Mbf" in L and "pp" in L: return _core(r, Mb, (L["Mbf"] - L["pp"]["Mb"]) * GT["ms"], M0, F, False)
    up = fr.f_back.f_locals if fr.f_back else {}
    if "r_" in up: return _core(r, Mb, Mb * up["r_"]["Mstar"] / 10 ** up["r_"]["logMb"] * GT["ms"], M0, F, lit)
    if "o" in up and "dl" in up: return _core(r, Mb, Mb * GT["ms"], M0, F, lit)
    return _ORIG(r, Mb, M0, F, gnedin=gnedin)

def _run5(d, m, keys=False, **kw):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLDL[0] = d; CN1_MODE = "blum"; GT.update(m=m, ms=1.0); GT.update(kw); GHSTORE.clear(); _EF.clear(); r = dict(delta=d, m=m, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["lt"] = {t: _lt(t) for t in _TG}; r["groups"] = _groups()
    if keys: gc = grade_clusters(f); r["keys"] = _keys(gc, f); r["keys_alt"] = _keys(grade_clusters("alt"), "alt")["bad"]; r["xcop"] = _xcop()
    print(f"SR2 {m} {d:+.2f} {kw} U {r['sparc'][_TG[0]]['U']:.3f} tilt {r['sparc'][_TG[0]]['tilt']:+.2f} {_tm.time() - _T0:.0f} s", flush=True); return r
_R = dict(rows={}); _R["rows"]["K2"] = _run5(0.0, None, keys=True); _R["rows"]["sat|+0.00"] = _run5(0.0, "sat", keys=True); json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
for d in (-0.05, -0.10): _R["rows"][f"sat|{d:+.2f}"] = _run5(d, "sat"); json.dump(_R, open(_OUTF, "w"), indent=1, default=float)
_R["MUT"] = _run5(0.0, "sat", keys=True, ms=0.1); json.dump(_R, open(_OUTF, "w"), indent=1, default=float); print("SR2 done", flush=True); sys.exit(0)
