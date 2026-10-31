# XH1 tail (criteria 530debe21b): runs inside FC1's grader namespace, after its full grade, in place of its last line.
import csv as _csv
from astropy.io import fits as _fits
from scipy.optimize import minimize_scalar as _ms
_REPO = os.path.dirname(REB); _KX = {}
_TS = open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample.py")).read()
_code = _TS[_TS.index("# ------------------------------------------------------------------ X-COP (matched-clumping profiles)"):
            _TS.index("# ------------------------------------------------------------------ graders per law")]
_CJ = json.load(open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample_results.json")))
_S = {"os": os, "np": np, "math": math, "csv": _csv, "fits": _fits, "minimize_scalar": _ms, "brentq": brentq, "REPO": _REPO,
      "check": (lambda k, ok, msg: _KX.__setitem__("CS2_" + k, bool(ok))), "R0C": _CJ["calibration"]["r0_law"]["c"], "R0P": _CJ["calibration"]["r0_law"]["p"], "SREF": 70.50}
exec(compile(_code, "cs2_xcop_block", "exec"), _S)
_XC = _S["XC"]; _cs2 = _S["xcop"](_CJ["calibration"]["A"], _CJ["calibration"]["q"], 70.50); _rf = _CJ["footings"]["canonical"]["CS2"]["xcop"]
_k1 = max(abs(_cs2[k] - _rf[k]) for k in ("mean", "rms", "n", "saturated"))
_PCm = 3.0857e16; _TBG = "A_c2b_refit"; _SMULT = float(os.environ.get("XH1_SMULT", "1"))
_rta_com, _gc2, _MSX = NX["r_ta_com"], NX["_gc2_ext"], NX["MSUN"]
_XM = {}
for _c in _XC:
    _p = os.path.join(_REPO, "real_research", "data", "xcop", _c["name"])
    with _fits.open(os.path.join(_p, f"{_c['name']}_hydro_mass.fits")) as _h: _z = float(_h[1].header["REDSHIFT"]); _r5 = float(_h[1].header["R500"])
    with _fits.open(os.path.join(_p, f"{_c['name']}_fgas_profile.fits")) as _h: _g = _h[1].data.copy(); _rg = _h[1].header["R500"]
    _XM[_c["name"]] = dict(z=_z, r500=_r5, Mg500=_S["li"](_g["RADIUS"] * _rg, _g["MGAS"], _r5))
def _budget(name, fac=1.0):
    m = _XM[name]; Mbx, Mbt = _gc2(m["Mg500"], m["r500"] / 1e3, m["z"], fac * 3.0 * 1.2 * m["Mg500"] * _MSX)
    return Mbt, _rta_com(Mbt) / (1 + m["z"])
def _grade(foot):
    rows = []; per = {}; info = {}; k2 = []; k3 = []; k4 = []; floor = 0; sat0 = SAT["n"]
    for c in _XC:
        nm = c["name"]; Mbt, rta = _budget(nm); k3.append(max(abs(_budget(nm, f_)[0] / Mbt - 1) for f_ in (0.3, 3.0)))
        Mfair = NAT_RRAT * Mbt; Mtot = (Mfair + Mbt) / MSUNE; s0, act = sig_core(foot, _TBG, Mtot, True); floor += 0 if act else 1
        if act: k4.append(abs(s0 / (sigma_coll(_TBG, Mtot)[0] * MSUNE / PC2) / (FC1_F * eta_of(cf_of(Mtot))) - 1))
        s = s0 * _SMULT; n0 = SAT["n"]; r0 = solve_r0(Mfair, rta, s); sat = SAT["n"] > n0
        k2.append(0.0 if sat else abs(math.pi * s * r0 ** 2 * float(B(rta / r0)) / Mfair - 1)); dd = []
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            rm = r * 1e3 * _PCm; Mh = math.pi * s * r0 ** 2 * float(B(min(rm, rta) / r0)); dd.append(dict(cluster=nm, x=x, r_kpc=r, Mh_Msun=Mh / MSUNE, Mb_Msun=mb, MHSE_Msun=mh, d=math.log10(mh * MSUNE / (mb * MSUNE + Mh))))
        rows += dd; per[nm] = float(np.mean([v["d"] for v in dd]))
        info[nm] = dict(logM=math.log10(Mtot), S_pc2=s * _PCm ** 2 / MSUNE, r0_kpc=r0 / _PCm / 1e3, rta_Mpc=rta / NX["MPC"], Mbt_over_Mg500=Mbt / (_XM[nm]["Mg500"] * _MSX), saturated=bool(sat))
    d = np.array([v["d"] for v in rows]); band = [v["d"] for v in rows if 150.0 <= v["r_kpc"] <= 460.0]
    return dict(mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))), n=int(len(d)), saturated=int(SAT["n"] - sat0), on_floor=floor, per_cluster=per, info=info, rows=rows,
                by_x={f"{x:g}": float(np.mean([v["d"] for v in rows if abs(v["x"] - x) < 1e-9])) for x in (0.1, 0.2, 0.3, 0.5, 0.7)},
                band=dict(n=len(band), mean=float(np.mean(band)), R_X=float(10 ** (-np.mean(band)))), k2=max(k2), k3=max(k3), k4=max(k4) if k4 else 0.0)
_OUT = dict(fstar=FSTAR, shape=SHAPE["s"], B1=float(B(1.0)), k1_cs2=_k1, cs2_blockchecks=_KX, smult=_SMULT, footings={f_: _grade(f_) for f_ in FEET})
_ref0 = os.environ.get("XH1_K0_REF")
if _ref0:
    _J = json.load(open(_ref0)); _OUT["k0"] = max(abs(RES["footings"][f_]["clusters"]["cells"][h_][k_]["pred"] - _J["footings"][f_]["clusters"]["cells"][h_][k_]["pred"]) for f_ in FEET for h_ in HK for k_ in _J["footings"][f_]["clusters"]["cells"][h_])
_OUT["rss_gb"] = rss(); json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)
sys.exit(0)
