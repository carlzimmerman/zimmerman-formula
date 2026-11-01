# DR7 tail, after UR1's helpers. Reads only. Part from DR7_PART: MEDIAN, LOW, HIGH, MUTATE.
import time as _tm, sys as _sys
_sys.path.insert(0, os.environ["DR7_HERE"]); from dr7_cap import cap as _cap
_T0 = _tm.time(); _PT = os.environ["DR7_PART"]; _OUTF = os.environ["SL1_OUT"]; _ORIG = contract; _ST = dict(on=False, cold=False, mul=1.0, rec=None)
_R = json.load(open(_OUTF)) if os.path.exists(_OUTF) else dict(part=_PT, rows={})
def _save():
    json.dump(_R, open(_OUTF + ".tmp", "w"), indent=1, default=float); os.replace(_OUTF + ".tmp", _OUTF)
def contract(r, Mb, M0, F, gnedin=None):
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin)
    if not _ST["on"]: return o
    Mc = o[0]; M, inf = _cap(r, Mb, M0, Mc, 0.0 if _ST["cold"] else SGN * F, rho_mul=_ST["mul"])
    rec = _ST["rec"]
    if rec is not None:
        rh = float(np.interp(0.5 * Mb[-1], Mb, r)); lg = np.log(r); mh = float(np.interp(math.log(rh), lg, M)); ch = float(np.interp(math.log(rh), lg, Mc)); m0 = float(np.interp(math.log(rh), lg, M0)); rec["n"] += 1; rec["bound"] += inf["bound"]; rec["conv"] = max(rec["conv"], inf["conv"]); rec["over"] = max(rec["over"], float(np.max(M / np.maximum(Mc, 1e-300) * (Mc > 0)))); rec["mono"] = min(rec["mono"], float(np.min(np.diff(M)))); rec["edge"] = max(rec["edge"], abs(float(M[-1] / Mc[-1]) - 1)); rec["Mrh"].append(mh / ch); rec["frh"].append((mh - m0) / (ch - m0) if abs(ch - m0) > 1e-6 * m0 else 1.0); w = np.where(M < Mc * (1 - 1e-6))[0]; rec["rx"].append(float(r[w[-1]] / rh) if len(w) else 0.0)
    return (M,) + tuple(o[1:])
def _cell(mp):
    global CN1_MODE
    SLMAP["m"] = mp; CN1_MODE = "blum"; GHSTORE.clear(); r = dict(map=mp, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; return r
def _do(name, fn):
    if name in _R["rows"]: return
    _R["rows"][name] = fn(); _save(); print(f"DR7 {name} {_tm.time() - _T0:.0f} s", flush=True)
def _new(): return dict(n=0, bound=0, conv=0.0, over=0.0, mono=1e300, edge=0.0, Mrh=[], frh=[], rx=[])
def _sum(q): return dict(n=q["n"], bound=q["bound"], conv=q["conv"], over=q["over"], mono=q["mono"], edge=q["edge"], Mrh_med=float(np.median(q["Mrh"])), Mrh_min=float(np.min(q["Mrh"])), frh_med=float(np.median(q["frh"])), rx_med=float(np.median(q["rx"])), rx_p90=float(np.percentile(q["rx"], 90)))
def _capped(mp, full, cold=False, mul=1.0):
    _ST.update(on=True, cold=cold, mul=mul, rec=_new())
    r = _run(mp, "blum") if full else _cell(mp); r["cap"] = _sum(_ST["rec"]); _ST.update(on=False, rec=None, cold=False, mul=1.0); return r
if _PT == "MEDIAN":
    _do("EM1|blum|off", lambda: _run("EM1", "blum")); _do("EM1|blum|cap", lambda: _capped("EM1", True))
    def _rtab(on):
        SLMAP["m"] = "EM1"; _ST.update(on=on); o = _resp_gal(); _ST.update(on=False); return o
    _do("resp|off", lambda: _rtab(False)); _do("resp|cap", lambda: _rtab(True))
    _do("FAIRTA|blum|cap", lambda: _capped("FAIRTA", True)); _do("EM1|blum|cap_coldonly", lambda: _capped("EM1", False, cold=True))
elif _PT in ("LOW", "HIGH"): _do("EM1|blum|cap", lambda: _capped("EM1", False))
else: _do("EM1|blum|cap_mut", lambda: _capped("EM1", False, mul=0.1))
print("DR7 done", flush=True); sys.exit(0)
