# SP3: added to ZN2's grader after OP3's x. The map, tilt and LITTLE THINGS on the native shape. kappa = 1/2 FITTED, unused; not theory closed.
exec(open(os.environ["SP3_OP3X"]).read())
_SPDEF = """
_SPT = json.load(open(os.environ["SP3_TABLES"])); _SPN = os.environ["SP3_MAP"]; _SPD = float(os.environ.get("SP3_DELTA", "0"))
def _spm(lMb, bg):
    if _SPN == "EM1": return bg["a"] + bg["b"] * (lMb - 10) + _SPD
    if _SPN == "FAIR200": return math.log10(NAT_RRAT) + lMb
    tg = next(t_ for t_ in BGS if BGS[t_]["a"] == bg["a"] and BGS[t_]["h"] == bg["h"]); t_ = _SPT[_SPN][tg]; return float(np.interp(lMb, t_["x"], t_["y"]))
"""
sub('def sparc(f, tag, rule=True):', _SPDEF + 'def sparc(f, tag, rule=True):')
sub('lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)', 'lM = _spm(q["lMb"], bg); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)')
sub('M200 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)', 'M200 = 10 ** _spm(lMb, bg) * MS540; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)')
_SPTAIL = """
import pickle as _pk
_ZO["sp3"] = dict(tilt={}, binsU={}, lt={}, Ugal={})
_LT = _pk.load(open(os.path.join(REB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["lt"]
for _tg in BGS:
    _Us = {}
    for _q in GALS:
        _t = _TB.get(_q["name"]); _e = OP3S.get(("canonical", _tg, _q["name"]))
        if _e is None or _t is None or not (_t["vf"] > 0 and _t["Q"] <= 2 and _t["inc"] >= 30): continue
        _Us[_q["name"]] = (float(_UP[_e[0][2]]), _t["vf"])
    _u = np.array([a_[0] for a_ in _Us.values()]); _v = np.array([a_[1] for a_ in _Us.values()]); _ZO["sp3"]["tilt"][_tg] = float(np.median(_u[_v < 100]) - np.median(_u[_v > 150])); _ZO["sp3"]["binsU"][_tg] = {f"{l_}-{h_}": float(np.median(_u[(_v >= l_) & (_v < h_)])) for l_, h_ in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400))}; _ZO["sp3"]["Ugal"][_tg] = {k_: a_[0] for k_, a_ in _Us.items()}
    _bg = BGS[_tg]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _E = []
    for _r in _LT:
        _M2 = 10 ** _spm(_r["logMb"], _bg) * MSUNE; _R2 = (3 * _M2 / (4 * math.pi * 200 * _rc)) ** (1 / 3); _Rr = _r["R"] * MPCE / 1e3; _Mb = 10 ** _r["logMb"] * MSUNE; _rg = np.geomspace(_Rr * 1e-3, max(_R2 * 1.2, _Rr * 2), 600); _M0 = zn2_mass(_M2, _rc, _rg, None); _Mbg = _Mb * np.minimum(_rg / _Rr, 1.0) ** 2; _Mf = contract(_rg, _Mbg, _M0, _Mb / float(_M0[-1]))[0]; _Mc = float(np.interp(math.log(_Rr), np.log(_rg), _M0 + OP3_FQ * (_Mf - _M0))); _E.append(math.log10((_r["V"] * 1e3) ** 2 / _Rr) - math.log10(GE * _Mb / _Rr ** 2 + GE * _Mc / _Rr ** 2))
    _ZO["sp3"]["lt"][_tg] = float(np.median(_E))
json.dump(_ZO, open(os.environ["ZN2_OUT"], "w"), indent=1, default=float)"""
sub('json.dump(_ZO, open(os.environ["ZN2_OUT"], "w"), indent=1, default=float)', _SPTAIL)
