_x39 = open(os.path.join(REB if "REB" in globals() else RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); _ct = _x39[_x39.index("def contract(r, Mb, M0, F, gnedin=None):"):_x39.index('P("\\n=== checks")')]
_OPD = """
SGN = 1; OP3_FQ = float(os.environ["OP3_FQ"]); OP3_MB = float(os.environ.get("OP3_MB", "1")); OP3_UP = np.round(np.arange(0.30, 1.2001, 0.01), 2); OP3S = {}; OP3_K = {}
""" + _ct + """
ER1_EPS = float(os.environ["ER1_EPS"]) if os.environ.get("ER1_EPS") else None; ER1_BH = os.environ.get("ER1_BH") == "1"; ER1_FG = np.linspace(0, 0.872, 21); ER1_TF = [0, .1, .2, .3, .4, .5, .6, .7, .872, 1.0]; ER1E = {}
def er1_W(rg, Mb, Mc):
    dM = np.diff(Mc); rm = 0.5 * (rg[1:] + rg[:-1]); return -GE * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
def er1_budget(U, q, bh=None):
    bh = ER1_BH if bh is None else bh; Ms = U * q["meta"]["L36"] * 1e9 * MSUNE; return Ms / MSUNE / 100.0 * 1e44 + (0.1 * 0.005 * Ms * 2.99792458e8 ** 2 if bh else 0.0)
def op3_gh(q, M2, rc_, R2):
    R_ = q["Rm"]; rg = np.geomspace(R_[0] * 0.05, R2 * 1.2, 300); M0 = zn2_mass(M2, rc_, rg, None); gh = np.zeros((len(R_), q["GB"].shape[1])); assert q["GB"].shape[1] == len(OP3_UP)
    for iu, U in enumerate(OP3_UP):
        Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0)); Mtot_ = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
        Mbg = np.where(rg < R_[0], Mbk[0] * (rg / R_[0]) ** 2, np.interp(np.log(rg), np.log(R_), Mbk)); out_ = rg > R_[-1]
        if out_.any():
            t_ = np.clip(np.log(rg[out_] / R_[-1]) / math.log(3.0), 0, 1); Mbg[out_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mtot_) * t_)
        Mbg = OP3_MB * np.maximum.accumulate(Mbg); Mf_, _c, _x = contract(rg, Mbg, M0, OP3_MB * Mtot_ / float(M0[-1]))
        _dM = Mf_ - M0; _fu = OP3_FQ
        if ER1_EPS is not None:
            _b = ER1_EPS * er1_budget(U, q); _w0 = er1_W(rg, Mbg, M0 + 0.872 * _dM); _fu = 0.872
            for _ff in ER1_FG:
                if max(0.0, (er1_W(rg, Mbg, M0 + _ff * _dM) - _w0) / 2) <= _b: _fu = float(_ff); break
        if abs(U - 0.5) < 1e-9 and ETA_USE["v"] == ETA: _w0 = er1_W(rg, Mbg, M0 + 0.872 * _dM); ER1E[q["name"]] = dict(E=[max(0.0, (er1_W(rg, Mbg, M0 + _ff * _dM) - _w0) / 2) for _ff in ER1_TF], SN=er1_budget(U, q, False), BH=er1_budget(U, q, True) - er1_budget(U, q, False), lM=math.log10(M2 / MSUNE))
        gh[:, iu] = GE * np.interp(np.log(R_), np.log(rg), M0 + _fu * _dM) / R_ ** 2
    return gh
"""
sub('def sparc(f, tag, rule=True):', _OPD + 'def sparc(f, tag, rule=True):')
sub('rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))', '''_gh3 = op3_gh(q, M200 * MSUNE, rc, R200) if (ZN2["on"] and rule and ETA_USE["v"] == ETA) else (GE * Mh / q["Rm"] ** 2)[:, None] * np.ones_like(q["GB"]); rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + _gh3, 1e-300)))); OP3S[(f, tag, q["name"])] = (rows[-1], _gh3)''')
sub('json.dump(_ZO, open(os.environ["ZN2_OUT"], "w"), indent=1, default=float)', '''_ZO["bins3"] = {}
for _lo, _hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
    _U, _D = [], []
    for _q in GALS:
        _t = _TB.get(_q["name"]); _e = OP3S.get(("canonical", "A_c2b_refit", _q["name"]))
        if _e is None or _t is None or not (_lo <= _t["vf"] <= _hi and _t["Q"] <= 2 and _t["inc"] >= 30): continue
        _U.append(float(_UP[_e[0][2]])); _x = _q["Rm"] / _KP / _t["rd"]; _m = (_x >= 2) & (_x <= 4) & _q["OK"][:, _I5]
        if _m.any(): _D.append(float(np.mean(np.sqrt((_q["GB"][:, _I5] + _e[1][:, _I5]) * _q["Rm"])[_m] / 1e3 - _q["Vobs"][_m])))
    _ZO["bins3"][f"{_lo}-{_hi}"] = dict(n=len(_U), U=float(np.median(_U)) if _U else None, dV=float(np.median(_D)) if _D else None)
_uu = {_q["name"]: (float(_UP[OP3S[("canonical", "A_c2b_refit", _q["name"])][0][2]]), _TB.get(_q["name"])) for _q in GALS if ("canonical", "A_c2b_refit", _q["name"]) in OP3S}
_lo3 = [u for u, t in _uu.values() if t and 0 < t["vf"] < 100 and t["Q"] <= 2 and t["inc"] >= 30]; _hi3 = [u for u, t in _uu.values() if t and t["vf"] > 150 and t["Q"] <= 2 and t["inc"] >= 30]; _ZO["tilt"] = float(np.median(_lo3) - np.median(_hi3)); _ZO["er1E"] = {k: dict(v, vf=_TB[k]["vf"], ok=bool(_TB[k]["Q"] <= 2 and _TB[k]["inc"] >= 30)) for k, v in ER1E.items() if k in _TB}
json.dump(_ZO, open(os.environ["ZN2_OUT"], "w"), indent=1, default=float)''')
