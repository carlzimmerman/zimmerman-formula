# DR3 tail, after UR1's helpers. Reads only. kappa = 1/2 FITTED, unused; not theory closed.
import time as _tm
from scipy.optimize import brentq as _bq
KPC_S = NE["KPC_S"]; _T0 = _tm.time(); _PT = os.environ["DR3_PART"]; _SPD = os.path.join(REB, "..", "real_research", "data", "sparc_data")
_D = dict(on=False, stars="sb", gas="exp", mut=1.0); _FQ = [1.0]; _ORIG = contract; _SB = {}; _GR = {}; _GC = dict(root=0, x2=0, kept=0); _LR = []
def contract(r, Mb, M0, F, gnedin=None):
    o = _ORIG(r, Mb, M0, F, gnedin=gnedin)
    if _FQ[0] == 1.0: return o
    return (np.maximum.accumulate(M0 + _FQ[0] * (o[0] - M0)),) + tuple(o[1:])
for _q in GALS:
    _d = np.genfromtxt(os.path.join(_SPD, _q["name"] + "_rotmod.dat"), comments="#"); assert len(_d) == len(_q["Rm"]) and np.allclose(_d[:, 0] * KPC_S, _q["Rm"]); _Rk = _d[:, 0]; _sb = np.maximum(_d[:, 6], 0.0); _i = np.empty_like(_Rk); _i[0] = 0.5 * _sb[0] * _Rk[0] ** 2
    _i[1:] = 0.5 * (_sb[1:] * _Rk[1:] + _sb[:-1] * _Rk[:-1]) * np.diff(_Rk); _SB[_q["name"]] = 2 * math.pi * 1e6 * np.cumsum(_i); _sbb = np.maximum(_d[:, 7], 0.0); _ib = np.empty_like(_Rk); _ib[0] = 0.5 * _sbb[0] * _Rk[0] ** 2; _ib[1:] = 0.5 * (_sbb[1:] * _Rk[1:] + _sbb[:-1] * _Rk[:-1]) * np.diff(_Rk); _LR.append(float((_SB[_q["name"]][-1] + 2 * math.pi * 1e6 * np.cumsum(_ib)[-1]) / (_q["meta"]["L36"] * 1e9)))
    _mh = _q["meta"]["MHI"] * 1e9; _rh = _q["meta"]["RHI"]
    if _mh <= 0 or _rh <= 0: _GR[_q["name"]] = None; _GC["kept"] += 1; continue
    _w = 2 * math.pi * _rh ** 2 * 1e6 / _mh
    if _w >= 4 * math.exp(-2): _x = 2.0; _GC["x2"] += 1
    else: _x = _bq(lambda x: x * x * math.exp(-x) - _w, 2.0, 200.0); _GC["root"] += 1
    _GR[_q["name"]] = _rh / _x
def _mexp(R_kpc, M, h): x = R_kpc / h; return M * (1 - (1 + x) * np.exp(-x))
def DR3_MBK(q, iu, U, R_):
    if not _D["on"]: return np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0))
    n = q["name"]; Rk = R_ / KPC_S; Lc = _SB[n]
    if _D["stars"] == "exp" and q["meta"]["Rdisk"] > 0: St = _mexp(Rk, float(Lc[-1]), q["meta"]["Rdisk"])
    else: St = Lc
    Mb = U * St * MSUNE + 1.4 * U * (q["Vbul"] * 1e3) ** 2 * R_ / GE
    if _D["gas"] == "inv": Mb = Mb + _GI[n] * MSUNE
    elif _D["gas"] == "exp" and _GR[n] is not None: Mb = Mb + _mexp(Rk, 1.33 * q["meta"]["MHI"] * 1e9, _GR[n]) * MSUNE
    else: Mb = Mb + np.sign(q["Vgas"]) * (q["Vgas"] * 1e3) ** 2 * R_ / GE
    return np.maximum.accumulate(np.maximum(Mb * _D["mut"], 0.0))
def _eff(tag="A_c2b_refit", f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); U = float(UPS[iu]); O = {f"{l}-{h}": [] for l, h in _BIN}; SLMAP["m"] = "EM1"
    for q in GALS:
        t = _TB.get(q["name"])
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30 or q["meta"]["Rdisk"] <= 0: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 400); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mt0 = (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE; Qs = []; Mbs = []
        for on in (False, True):
            _D["on"] = on; Mbk = DR3_MBK(q, iu, U, Rm); Mt = max(float(Mbk[-1]), Mt0); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
            if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
            Mbg = np.maximum.accumulate(Mbg); Mf = _ORIG(rg, Mbg, M0, Mt / (M2 * MSUNE))[0]; Qs.append(Mf / M0); Mbs.append(Mbg)
        _D["on"] = False; rr = np.array([r0, 2 * q["meta"]["Rdisk"] * KPC_S, 3 * q["meta"]["Rdisk"] * KPC_S, 4 * q["meta"]["Rdisk"] * KPC_S]); lr = np.log(rr); lg = np.log(rg); qa, qb = np.interp(lr, lg, Qs[0]), np.interp(lr, lg, Qs[1]); ma, mb = np.interp(lr, lg, Mbs[0]), np.interp(lr, lg, Mbs[1])
        for l, h in _BIN:
            if l <= t["vf"] < h: O[f"{l}-{h}"].append(dict(ratio=((qb - 1) / np.where(np.abs(qa - 1) > 1e-6, qa - 1, np.nan)).tolist(), mb=(mb / np.maximum(ma, 1e-300)).tolist(), Qoff=qa.tolist(), Qdr3=qb.tolist()))
    return {k: {x: np.nanmedian([a[x] for a in v], axis=0).tolist() for x in ("ratio", "mb", "Qoff", "Qdr3")} | dict(n=len(v)) for k, v in O.items() if v}
_RES = dict(gas_counts=_GC, K4_L_ratio=float(np.median(_LR)), K4_L_ratio_16_84=[float(np.percentile(_LR, 16)), float(np.percentile(_LR, 84))], runs={})
def _go(lab, mode, on, stars="sb", gas="exp", mut=1.0, fq=1.0):
    _D.update(on=on, stars=stars, gas=gas, mut=mut); _FQ[0] = fq; _RES["runs"][lab] = _run("EM1", mode); _D["on"] = False; _FQ[0] = 1.0; json.dump(_RES, open(os.environ["SL1_OUT"] + ".part", "w"), indent=1, default=float); print(f"DR3 {lab} done {_tm.time() - _T0:.0f} s", flush=True)
if _PT == "GASINV":
    sys.path.insert(0, os.environ["DR3_HERE"]); from dr3_gasinv import invert as _inv; _GI = {}; _FE = []
    for _q in GALS:
        _Rk = _q["Rm"] / KPC_S; _GI[_q["name"]], _e = _inv(_Rk, np.sign(_q["Vgas"]) * _q["Vgas"] ** 2, 1.33 * _q["meta"]["MHI"] * 1e9); _FE.append(_e)
    _RES["gasinv_fit_rms_median"] = float(np.median(_FE)); _RES["gasinv_ratio_to_vg2r"] = {}; print(f"inversion done {_tm.time() - _T0:.0f} s, fit rms median {np.median(_FE):.4f}", flush=True)
    for _f in (1.0, 2.0, 4.0):
        _o = []
        for _q in GALS:
            if _q["meta"]["Rdisk"] <= 0: continue
            _Rk = _q["Rm"] / KPC_S; _x = _f * _q["meta"]["Rdisk"]
            if _x < _Rk[0] or _x > _Rk[-1]: continue
            _m0 = float(np.interp(_x, _Rk, np.maximum.accumulate(np.maximum(np.sign(_q["Vgas"]) * (_q["Vgas"]) ** 2 * _Rk / 4.30091e-6, 0.0)))); _o.append(float(np.interp(_x, _Rk, _GI[_q["name"]])) / max(_m0, 1.0))
        _RES["gasinv_ratio_to_vg2r"][f"{_f:g}Rd"] = float(np.median(_o))
    _go("DR3|blum", "blum", True); _go("GASINV|blum", "blum", True, gas="inv"); _go("GASINV|gnedin", "gnedin", True, gas="inv"); _go("GASINVxFQ|blum", "blum", True, gas="inv", fq=0.872)
elif _PT == "MUTATE":
    _go("DR3|blum|MUT2", "blum", True, mut=2.0)
else:
    _go("EM1|off", "off", False); _go("OFF|blum", "blum", False); _go("OFF|gnedin", "gnedin", False); _go("DR3|blum", "blum", True); _go("DR3|gnedin", "gnedin", True); _go("EXP|blum", "blum", True, stars="exp"); _go("GASKEPT|blum", "blum", True, gas="kept"); _go("DR3xFQ|blum", "blum", True, fq=0.872); _RES["eff"] = _eff(); _RES["eff_B"] = _eff("B_cfg886_bg")
json.dump(_RES, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); os.remove(os.environ["SL1_OUT"] + ".part"); print("DR3 done", flush=True); sys.exit(0)
