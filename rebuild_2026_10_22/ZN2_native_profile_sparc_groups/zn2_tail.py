# ZN2 tail: in place of the grader's last line.
_ZO = dict(sparc={t_: {k_: RES["footings"]["canonical"]["sparc"][t_][k_] for k_ in ("rms", "U_median", "line")} for t_ in BGS}, groups={k_: RES["footings"]["canonical"]["groups"][k_] for k_ in ("mean", "Z", "verdict", "PASS")}, stat=dict(below=ZN2["below"], n=ZN2["n"]), checks={k_: bool(v_) for k_, v_ in checks}, rss_gb=rss())
if os.environ.get("ZN2_K1"):
    _b = sparc("canonical", "A_c2b_refit"); _g = grade_groups("canonical"); _t = "A_c2b_refit"; _bg = BGS[_t]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _Xg = np.geomspace(1e-3, 40.0, 500); _Z2X = np.log(_Xg); _Z2T = []; _fc = NAT_RRAT / (1 + NAT_RRAT)
    for _l in np.arange(7.5, 15.5, 0.02):
        _Mt = 10.0 ** _l; _M2 = _fc * _Mt * MSUNE; _R = (3 * _M2 / (4 * math.pi * 200 * _rc)) ** (1 / 3); _s = sig_core("canonical", _t, _Mt)[0]; _r0 = solve_r0(_M2, _R, _s); _Z2T.append((float(_l), np.log(math.pi * _s * _r0 ** 2 * B(_Xg * _R / _r0) / _M2)))
    ZN2["on"] = True; _b2 = sparc("canonical", "A_c2b_refit"); _g2 = grade_groups("canonical"); _ZO["k1"] = dict(rms=abs(_b["rms"] - _b2["rms"]), U=abs(_b["U_median"] - _b2["U_median"]), gZ=abs(_g["Z"] - _g2["Z"]))
else:
    _MRT = os.path.join(REB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt"); _TB = {}
    for _l in open(_MRT):
        _p = _l.split()
        if len(_p) < 18: continue
        try: _TB[_p[0]] = dict(inc=float(_p[5]), rd=float(_p[11]), vf=float(_p[15]), Q=int(_p[17]))
        except ValueError: pass
    _UP = np.round(np.arange(0.30, 1.2001, 0.01), 2); _I5 = int(np.argmin(abs(_UP - 0.50))); _KP = MPCE / 1e3; _bg = BGS["A_c2b_refit"]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _rows = {}
    for _q in GALS:
        _M2 = 10 ** (_bg["a"] + _bg["b"] * (_q["lMb"] - 10)) * MSUNE; _gh = GE * zn2_mass(_M2, _rc, _q["Rm"], None) / _q["Rm"] ** 2; _r = fit_one(_q, np.log10(np.maximum(_q["GB"] + _gh[:, None], 1e-300))); _rows[_q["name"]] = (_r, _gh, math.log10(_M2 / MSUNE / (NAT_RRAT / (1 + NAT_RRAT))))
    _ZO["bins"] = {}
    for _lo, _hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
        _U, _D = [], []
        for _q in GALS:
            _t = _TB.get(_q["name"])
            if _t is None or not (_lo <= _t["vf"] <= _hi and _t["Q"] <= 2 and _t["inc"] >= 30): continue
            _r, _gh, _ = _rows[_q["name"]]; _U.append(float(_UP[_r[2]])); _x = _q["Rm"] / _KP / _t["rd"]; _m = (_x >= 2) & (_x <= 4) & _q["OK"][:, _I5]
            if _m.any(): _D.append(float(np.mean(np.sqrt((_q["GB"][:, _I5] + _gh) * _q["Rm"])[_m] / 1e3 - _q["Vobs"][_m])))
        _ZO["bins"][f"{_lo}-{_hi}"] = dict(n=len(_U), U=float(np.median(_U)) if _U else None, dV=float(np.median(_D)) if _D else None)
    _tag0 = _Z2T[0][0]; _ab = [_q for _q in GALS if _rows[_q["name"]][2] > _tag0]; _rr = [_rows[_q["name"]][0] for _q in _ab]
    if _rr: _st = pooled([r_[0] for r_ in _rr], [r_[1] for r_ in _rr], [r_[2] for r_ in _rr]); _ZO["above"] = dict(n=len(_ab), rms=_st["rms"], U_median=_st["U_median"])
if not os.environ.get("ZN2_K1") and os.environ.get("ZN2_TAGS", "").startswith("1e10"):
    from scipy.stats import spearmanr as _spr
    _A = json.load(open(os.path.join(REB, "AM1_native_abundance_match", "am1_results.json")))["curve"]; _ALT = dict(fair=lambda q_: NAT_RRAT * 10 ** q_["lMb"], am1=lambda q_: 10 ** float(np.interp(q_["lMb"], _A["lMb"], _A["lM200"]))); _ZO["alt"] = {}
    for _nm, _fn in _ALT.items():
        _rr = [fit_one(_q, np.log10(np.maximum(_q["GB"] + (GE * zn2_mass(_fn(_q) * MSUNE, _rc, _q["Rm"], None) / _q["Rm"] ** 2)[:, None], 1e-300))) for _q in GALS]; _st = pooled([r_[0] for r_ in _rr], [r_[1] for r_ in _rr], [r_[2] for r_ in _rr]); _ZO["alt"][_nm] = dict(rms=_st["rms"], U_median=_st["U_median"])
    _SBe = {}
    for _l in open(_MRT):
        _p = _l.split()
        if len(_p) >= 18:
            try: _SBe[_p[0]] = float(_p[10])
            except ValueError: pass
    _X, _Y = [], []
    for _q in GALS:
        _t = _TB.get(_q["name"])
        if _t is None or not (60 <= _t["vf"] <= 120 and _t["Q"] <= 2 and _t["inc"] >= 30) or _SBe.get(_q["name"], 0) <= 0: continue
        _gh = _rows[_q["name"]][1]; _Rk = _q["Rm"] / _KP; _ok = _q["OK"][:, _I5]; _R2 = 2 * _t["rd"]
        if _ok.sum() < 2 or not (_Rk[_ok].min() <= _R2 <= _Rk[_ok].max()): continue
        _Vm = np.sqrt(np.maximum((_q["GB"][:, _I5] + _gh) * _q["Rm"], 0)) / 1e3; _X.append(math.log10(_SBe[_q["name"]])); _Y.append(float(np.interp(math.log(_R2), np.log(_Rk[_ok]), _Vm[_ok] / _q["Vobs"][_ok] - 1)))
    _X, _Y = np.array(_X), np.array(_Y); _rg = np.random.default_rng(1); _bs = [float(np.polyfit(_X[k_], _Y[k_], 1)[0]) for k_ in (_rg.integers(0, len(_X), len(_X)) for _ in range(4000))]; _ZO["hs1"] = dict(n=len(_X), b=float(np.polyfit(_X, _Y, 1)[0]), s=float((np.percentile(_bs, 84) - np.percentile(_bs, 16)) / 2), rho=float(_spr(_X, _Y)[0]), mean=float(_Y.mean()), rms=float(np.sqrt(np.mean(_Y ** 2))))
json.dump(_ZO, open(os.environ["ZN2_OUT"], "w"), indent=1, default=float)
sys.exit(0)
