#!/usr/bin/env python3
"""CN1_contraction_on_cold_share: X74's grader with FC1's conversions plus X39's contraction on collapse-branch systems (see FROZEN_CRITERIA.md). Called by cn1_run.py.
    CN1_R=<softening> CN1_MODE=off|blum|gnedin X74_CF=<table> X73_FSTAR=.. X73_SLOPE=.. python3 cn1_x74.py   kappa = 1/2 FITTED; not theory closed."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
X74F = os.path.join(REB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
X39S = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read()
CT = X39S[X39S.index("def contract(r, Mb, M0, F, gnedin=None):"):X39S.index('P("\\n=== checks")')]
INJ = r'''
_cf_line = "def cf_of(M): return float(np.interp(math.log10(M), CFLM, CFV))\n"
sub(_cf_line, _cf_line + """_FCN = NAT_RRAT / (1 + NAT_RRAT); FC1_F = _FCN; FC1_MC = _FCN; CN1_R = float(os.environ.get("CN1_R", "1")); CN1_MODE = os.environ.get("CN1_MODE", "blum"); SGN = -1 if os.environ.get("CN1_MUT") == "1" else 1
""" + CONTRACT_TEXT + """
def _bind(q, foot):                                               # SPARC baryon arrays by Upsilon, as X39
    return None
""")
sub('    sc = (eta_of(cf_of(M)) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2',
    '    sc = (FC1_F * eta_of(cf_of(M)) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2')
sub('s, a_ = sig_core(f, tag, M200, rule); act += a_', 's, a_ = sig_core(f, tag, M200 / (FC1_MC if ETA_USE["v"] == ETA else 1.0), rule); act += a_')
sub('sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE)', 'sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE / (FC1_MC if ETA_USE["v"] == ETA else 1.0))')
sub("""        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
        rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))""",
"""        if a_ and ETA_USE["v"] == ETA and CN1_MODE != "off":
            M2 = M200 * MSUNE; si = CN1_R * s; r0 = solve_r0(M2, R200, si); R_ = q["Rm"]; rg = np.geomspace(R_[0] * 0.05, R200, 300); M0 = math.pi * si * r0 ** 2 * B(rg / r0); gh = np.zeros((len(R_), len(UPS_G)))
            for iu, U in enumerate(UPS_G):
                Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0)); Mtot_ = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
                Mbg = np.where(rg < R_[0], Mbk[0] * (rg / R_[0]) ** 2, np.interp(np.log(rg), np.log(R_), Mbk)); out_ = rg > R_[-1]
                if out_.any():
                    t_ = np.clip(np.log(rg[out_] / R_[-1]) / math.log(3.0), 0, 1); Mbg[out_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mtot_) * t_)
                Mbg = np.maximum.accumulate(Mbg); Mf_, _c, _x = contract(rg, Mbg, M0, Mtot_ / M2, gnedin=(0.85, 0.8, R200) if CN1_MODE == "gnedin" else None)
                gh[:, iu] = GE * np.interp(np.log(R_), np.log(rg), Mf_) / R_ ** 2
            GHSTORE[(f, tag, q["name"])] = gh; rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))))
        else:
            r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
            rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))""")
sub("""            r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
            V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)""",
"""            if a_ and ETA_USE["v"] == ETA and CN1_MODE != "off":
                si = CN1_R * s; r0 = solve_r0(pp["Mfair"], pp["rta"], si); M0 = math.pi * si * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0); Mbf = pp["Mb"] + BCGF[int(i)] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2
                Fc_ = float(np.interp(pp["rta"], RM, Mbf)) / pp["Mfair"]; Mf_, _c, _x = contract(RM, Mbf, M0, Fc_, gnedin=(0.85, 0.8, pp["rta"]) if CN1_MODE == "gnedin" else None); V[i] = dvecN(int(i), foot, hk, Mbf + Mf_)
            else:
                r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
                V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)""")
sub('O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))\n',
    'O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))\n' + BCG_TEXT)
sub("x74ok = k2x\n", """x74ok = k2x
_rr = np.geomspace(1e18, 1e22, 40000); _k = 1e20; _Mz, _c0, _ = contract(_rr, np.zeros_like(_rr), _k * _rr, 0.0); _k2a = float(np.max(np.abs(_Mz / (_k * _rr) - 1)[5:-5]))
_Mp = 1e41; _F = 0.2; _Mt, _ct, _ = contract(_rr, np.full_like(_rr, _Mp), _k * _rr, _F); _sel = (_rr > 3e18) & (_rr < 3e21); _rf = _rr[_sel]; _mf = _Mt[_sel]; _ri = _mf / _k; _k2b = float(np.max(np.abs((_rf * (_Mp + _mf)) / (_ri * _k * _ri * (1 + _F)) - 1)))
RES["x74"]["cn1"] = dict(R=CN1_R, mode=CN1_MODE, k2a=_k2a, k2b=_k2b, n_bcg=int(np.isfinite(BCG_RAW).sum()), UPS_n=len(UPS_G))
P(f"CN1 R {CN1_R}, mode {CN1_MODE}; K2 identity {_k2a:.1e}, point-mass closed form {_k2b:.1e}; BCG matched {int(np.isfinite(BCG_RAW).sum())}")
""")
'''
BCG = r'''
_LANES = os.path.join(os.path.dirname(REB), "campaign_fresh_gravity"); _P687 = np.load(os.path.join(_LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); _CEN = json.load(open(os.path.join(_LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
_MY, _T3M, _N = NX["MY"], NX["T3M"], NX["N"]; _J9 = np.full(_N, -1)
for _i in range(_N):
    _dd = np.hypot((_P687["ra"] - _MY["ra"][_i]) * np.cos(np.radians(_MY["dec"][_i])), _P687["dec"] - _MY["dec"][_i]) * 3600; _j = int(np.argmin(_dd))
    if _dd[_j] < 5 and abs(_P687["z"][_j] - _MY["z"][_i]) < 1e-3: _J9[_i] = _j
_meas = np.array([_j >= 0 and not _CEN[_j].get("not_measured", False) for _j in _J9]); _bcg = np.array([float(_CEN[_j]["bcg_med"]) if _j >= 0 else np.nan for _j in _J9]); BCG_RAW = np.where(_meas & (_bcg > 0), _bcg, np.nan); BCGF = BCG_RAW.copy()
for _t in range(3):
    _m = _T3M == _t; BCGF[_m & ~np.isfinite(BCG_RAW)] = float(np.nanmedian(BCG_RAW[_m]))
UPS_G = NE["UPS"]; GHSTORE = {}
'''
TX = TX.replace("sys.argv = [SRC]\n", "CONTRACT_TEXT = " + repr(CT) + "\nBCG_TEXT = " + repr(BCG) + "\n" + INJ + "sys.argv = [SRC]\n"); assert "CONTRACT_TEXT" in TX
exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"})
