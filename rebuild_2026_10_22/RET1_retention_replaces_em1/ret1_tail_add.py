# RET1 tail: UR1's helpers above, read only. Retention map, line tables, rows. kappa = 1/2 FITTED, unused; not theory closed.
import time as _tm
_T0 = _tm.time(); _VSN2 = 2 * (1e51 * 1e-7) / (100 * 1.989e30) / 1e6; _PSN = 3e5 / 100.0  # (km/s)^2, km/s; PROVISIONAL, from memory
_gl = [(q["lMb"], math.log10(0.5 * q["meta"]["L36"] * 1e9), math.log10((0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9), q["name"]) for q in GALS if q["meta"]["L36"] > 0]
_xs = np.array([g[0] for g in _gl]); _ys = np.array([g[1] for g in _gl]); _fsb, _fsa = np.polyfit(_xs - 10, _ys, 1); _K8 = float(np.max(np.abs(_xs - np.array([g[2] for g in _gl]))))
_OWN = {round(g[0], 9): g[1] for g in _gl}
_TAGOF = lambda bg: next(t for t in _TG if BGS[t] is bg)
_RC = lambda t: 3 * (100 * BGS[t]["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
def _lMs(lMb, own=False, fac=1.0):
    k = round(lMb, 9)
    if own and k in _OWN: return min(lMb, _OWN[k] + math.log10(fac))
    return min(lMb, _fsa + _fsb * (lMb - 10) + math.log10(fac))
def _V2(M, tag, rc, Mb, launch="r0", zero="inf", addb=False, N=1200):
    R = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s, _ = sig_core("canonical", tag, M / FC1_MC); r0 = solve_r0(M * MSUNE, R, s); r1 = min(r0, 0.999 * R) if launch == "r0" else min(1e-3 * r0, 0.5 * R); rg = np.geomspace(r1, R, N); Mr = math.pi * s * r0 ** 2 * B(rg / r0); v = 2 * (float(np.trapz(GE * Mr / rg, np.log(rg))) + GE * M * MSUNE / R)
    if zero == "ta": v -= 2 * GE * M * MSUNE / max(float(NX["r_ta_com"](Mb * MSUNE)), R)
    if addb: v += 2 * GE * Mb * MSUNE / r0
    return v / 1e6
def _mubase(mode, V2): return _VSN2 / V2 if mode == "E" else _PSN / math.sqrt(V2)
_CA = {}
def _solve(lMb, tag, mode, eps, own=False, fac=1.0, launch="r0", zero="inf", addb=False):
    k = (round(lMb, 10), tag, mode, eps, own, fac, launch, zero, addb)
    if k in _CA: return _CA[k]
    rc = _RC(tag); Mb = 10 ** lMb; Ms = 10 ** _lMs(lMb, own, fac); lo = math.log10(NAT_RRAT) + lMb
    if eps == 0: _CA[k] = lo; return lo
    F = lambda lM: lM - math.log10(NAT_RRAT * (Mb + eps * _mubase(mode, _V2(10 ** lM, tag, rc, Mb, launch, zero, addb)) * Ms)); a, b = lo, lo + 8.0
    for _ in range(50):
        c = 0.5 * (a + b)
        if F(c) > 0: b = c
        else: a = c
    _CA[k] = 0.5 * (a + b); return _CA[k]
def _set(mode, eps, own=False):
    """eps: number, or dict by background."""
    SLMAP["m"] = "RET"; SLMAP["f"] = lambda lMb, bg, rc: 10 ** _solve(lMb, _TAGOF(bg), mode, eps[_TAGOF(bg)] if isinstance(eps, dict) else eps, own)
def _epsreq(lMb, tag, mode, M=None):
    M = M if M is not None else 10 ** (BGS[tag]["a"] + BGS[tag]["b"] * (lMb - 10)); Mb = 10 ** lMb; Ms = 10 ** _lMs(lMb); V2 = _V2(M, tag, _RC(tag), Mb); return (M / NAT_RRAT - Mb) / (_mubase(mode, V2) * Ms), math.sqrt(V2)
_EPS = {m: {t: _epsreq(10.0, t, m)[0] for t in _TG} for m in "EP"}
_K = _run("EM1", "off"); _NR = json.load(open(_NR2J))["footings"]["canonical"]; _k1 = max(max(abs(_K["sparc"][t]["U"] - _NR["sparc"][t]["U_median"]), abs(_K["sparc"][t]["rms"] - _NR["sparc"][t]["rms"])) for t in _TG); _k1c = max(abs(_K["keys"]["preds"][h][k] - _NR["clusters"]["cells"][h][k]["pred"]) for h in HK for k in _KY)
_R = dict(K1=[_k1, _k1c], K8=_K8, fs=[float(_fsa), float(_fsb)], EPS=_EPS, RNAT=float(NAT_RRAT), VSN=math.sqrt(_VSN2), PSN=_PSN, runs={"EM1|off": _K})
_R["runs"]["EM1|blum"] = _run("EM1", "blum"); _R["runs"]["FAIR200|off"] = _run("FAIR200", "off")
_set("E", 0); _R["runs"]["eps0|off"] = _run("RET", "off")
for nm, mo, ep, own, md in (("E1", "E", 1.0, False, ("off", "blum")), ("P1", "P", 1.0, False, ("off", "blum")), ("EF", "E", _EPS["E"], False, ("off", "blum")), ("PF", "P", _EPS["P"], False, ("off", "blum")), ("PF_own", "P", _EPS["P"], True, ("off",)), ("P1_own", "P", 1.0, True, ("off",))):
    for m_ in md: _set(mo, ep, own); _R["runs"][f"{nm}|{m_}"] = _run("RET", m_)
_M = {}
for nm, mo, ep in (("E1x4", "E", 4.0), ("P1x4", "P", 4.0)):
    _set(mo, ep); _M[nm] = _run("RET", "off")
json.dump(_M, open(os.environ["SL1_OUT"].replace("_results.json", "_MUTATE.json"), "w"), indent=1, default=float)
# lines
_GR = [7, 7.5, 8, 8.5, 9, 9.5, 10, 10.25, 10.5, 10.75, 11, 11.5, 12, 12.5, 13, 13.5, 14]; _L = {}
for t in _TG:
    bg = BGS[t]; O = dict(EM1={str(x): bg["a"] + bg["b"] * (x - 10) for x in _GR}, FAIR={str(x): math.log10(NAT_RRAT) + x for x in _GR}); rows = dict(E1=("E", 1.0), P1=("P", 1.0), EF=("E", _EPS["E"][t]), PF=("P", _EPS["P"][t]))
    for n, (mo, ep) in rows.items(): O[n] = {str(x): _solve(x, t, mo, ep) for x in _GR}
    O["epsreq_E"] = {str(x): _epsreq(x, t, "E")[0] for x in _GR}; O["epsreq_P"] = {str(x): _epsreq(x, t, "P")[0] for x in _GR}; O["Vesc_EM1"] = {str(x): _epsreq(x, t, "E")[1] for x in _GR}; O["lMs"] = {str(x): _lMs(x) for x in _GR}
    if t == _TG[0]:
        O["var"] = {}
        for n, kw in dict(centre=dict(launch="c"), zero_ta=dict(zero="ta"), baryons=dict(addb=True), return04=dict(fac=1 / 0.6), Y035=dict(fac=0.7), Y070=dict(fac=1.4)).items():
            O["var"][n] = {f"{mo}1": {str(x): _solve(x, t, mo, 1.0, **kw) for x in (9, 10, 11)} for mo in "EP"}
            O["var"][n].update({f"{mo}F": {str(x): _solve(x, t, mo, _EPS[mo][t], **kw) for x in (9, 10, 11)} for mo in "EP"})
    _L[t] = O
_R["lines"] = _L
# K7, K2, K4
_t = _TG[0]; _rc = _RC(_t); _a = []; _rs = []
for _x in (8.0, 10.0, 12.0):
    _lm = _solve(_x, _t, "E", 1.0); _M_ = 10 ** _lm; _a.append(abs(0.5 * math.log10(_V2(_M_, _t, _rc, 10 ** _x) / _V2(_M_, _t, _rc, 10 ** _x, N=2400)))); _rs.append(abs(_M_ / (NAT_RRAT * (10 ** _x + _mubase("E", _V2(_M_, _t, _rc, 10 ** _x)) * 10 ** _lMs(_x))) - 1))
_R["K7"] = [max(_a), max(_rs)]; _R["K9"] = max(abs(_solve(10.0, t, m, _EPS[m][t]) - BGS[t]["a"]) for t in _TG for m in "EP")
SLMAP["m"] = "FAIRTA"; _bg = BGS["A_c2b_refit"]; _rc = _RC("A_c2b_refit"); _m2, _r2 = _SL3M(10.0, _bg, _rc); _R["K4"] = abs(_m2 / (NAT_RRAT * 1e10) - 1)
SLMAP["m"] = "EM1"; CN1_MODE = "blum"; _rr = np.geomspace(1e18, 1e22, 4000); _R["K2"] = float(np.max(np.abs(contract(_rr, np.zeros_like(_rr), 1e20 * _rr, 0.0)[0] / (1e20 * _rr) - 1)[5:-5]))
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("RET1 done", flush=True); sys.exit(0)
