# HM1 (FROZEN_CRITERIA.md): response on the native cluster path. Injected before grade_clusters. X39's contract, CN1's BCG, unchanged. kappa = 1/2 FITTED, unused; not theory closed.
SGN = 1
_x39s = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(_x39s[_x39s.index("def contract(r, Mb, M0, F, gnedin=None):"):_x39s.index('P("\\n=== checks")')])
_LANES = os.path.join(os.path.dirname(REB), "campaign_fresh_gravity"); _P687 = np.load(os.path.join(_LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); _CEN = json.load(open(os.path.join(_LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
_MY, _T3M, _N = NX["MY"], NX["T3M"], NX["N"]; _J9 = np.full(_N, -1)
for _i in range(_N):
    _dd = np.hypot((_P687["ra"] - _MY["ra"][_i]) * np.cos(np.radians(_MY["dec"][_i])), _P687["dec"] - _MY["dec"][_i]) * 3600; _j = int(np.argmin(_dd))
    if _dd[_j] < 5 and abs(_P687["z"][_j] - _MY["z"][_i]) < 1e-3: _J9[_i] = _j
_meas = np.array([_j >= 0 and not _CEN[_j].get("not_measured", False) for _j in _J9]); _bcg = np.array([float(_CEN[_j]["bcg_med"]) if _j >= 0 else np.nan for _j in _J9]); BCG_RAW = np.where(_meas & (_bcg > 0), _bcg, np.nan); BCGF = BCG_RAW.copy()
for _t in range(3):
    _m = _T3M == _t; BCGF[_m & ~np.isfinite(BCG_RAW)] = float(np.nanmedian(BCG_RAW[_m]))
HM = dict(path="native", f=0.0, gn=False, bcg=False, fmode="own", K4=[], K4n=[], ratio=[], K3=0.0, flip=[], dump=None)
def hm1_resp(Mb, M0, rta, Mfair, gn_v=None):
    "M_c after response on RM. Mb clipped at r_ta, so nothing moves across it. F is M0's own unless fmode = cn1."
    if HM["f"] == 0.0: return M0
    Mbc = Mb if HM["fmode"] == "cn1" else np.interp(np.minimum(RM, rta), RM, Mb); M0r = float(np.interp(rta, RM, M0)); F = float(np.interp(rta, RM, Mbc)) / (Mfair if HM["fmode"] == "cn1" else M0r)   # cn1: CN1's text exactly, no clip
    Mf = contract(RM, np.maximum.accumulate(Mbc), M0, F, gnedin=(0.85, 0.8, rta) if HM["gn"] else None)[0]; Mc_ = M0 + HM["f"] * (Mf - M0)
    if HM.get("amend"): Mc_ = np.where(RM >= rta, M0r, np.minimum(Mc_, M0r))   # AMENDMENT_A1, post-result: mass pushed past r_ta returned as a shell at r_ta
    return Mc_
def hm1_S(pp, s):
    r0 = solve_r0(pp["Mfair"], pp["rta"], s); return math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
_HM_SH = [("baryons", None, None), ("c<R200", 0, "R"), ("c R200-1.42", "R", 1.42), ("c 1.42-2.06", 1.42, 2.06), ("c 2.06-3", 2.06, 3.0), ("c 3-rta", 3.0, "t")]
def hm1_pieces(i, foot, hk, pp, Mb_, Mc_, R2):
    "Shares of the eight stacked bins by source shell. fr from the whole source, so the pieces add to the whole."
    Ms = Mb_ + Mc_; piece = lambda S_: DAT[hk]["W"][i] * (A_(DS_(O_(P_(np.gradient(S_, RM) / (4 * np.pi * RM ** 2)), pp["dmpc"]))) / KG * fr); fr, _ = RF(hk, i, SB(O_(P_(np.gradient(Ms, RM) / (4 * np.pi * RM ** 2)), pp["dmpc"]))); O = {}; MPC_ = NX["MPC"]; last = piece(Mb_); O["baryons"] = last.copy()
    # cumulative chain, as OE1: a piece is the difference of two cumulative sources, so pieces telescope to the whole and a negative piece is seen
    for nm, lo, hi in _HM_SH[1:]:
        b = R2 if hi == "R" else pp["rta"] * 1.0001 if hi == "t" else hi * MPC_; b = max(b, R2) if hi != "R" else b; cur = piece(Mb_ + np.minimum(Mc_, float(np.interp(b, RM, Mc_)))); O[nm] = cur - last; last = cur
    O["c beyond"] = piece(Ms) - last
    return O
def hm1_src(i, foot, hk, pp, Mh, s, tag, z):
    Mb = pp["Mb"]; Mbf = Mb + BCGF[i] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2 if HM["bcg"] else Mb; rta, Mf_ = pp["rta"], pp["Mfair"]
    if HM["path"] == "hybrid":
        Ms_ = hm1_S(pp, s); Mn_ = Mh; _bg = BGS["A_c2b_refit"]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _thr = 500 * _rc * (NAT_OM * (1 + z) ** 3 + 1 - NAT_OM); _d = (1 + NAT_RRAT) * Mb / (4 / 3 * math.pi * RM ** 3); _ii = np.where(_d >= _thr)[0]; rx = 0.75 * RM[int(_ii.max())] if len(_ii) else 0.5 * NX["MPC"]; Mh = np.where(RM <= rx, Mn_, np.maximum(Mn_, Ms_)); Mh = np.maximum.accumulate(Mh); HM["flip"].append(dict(rx=rx / NX["MPC"], step=float((np.interp(rx * 1.02, RM, Mh) - np.interp(rx, RM, Mn_)) / Mf_), T3=int(NX["T3M"][i]), Mrta=float(np.interp(rta, RM, Mh) / Mf_)))
    Mc = hm1_resp(Mbf, Mh, rta, Mf_)
    if HM["f"] != 0.0:
        m0r, mfr = float(np.interp(rta, RM, Mh)), float(np.interp(rta, RM, Mc)); HM["K4"].append(abs(mfr / m0r - 1)); HM["ratio"].append(m0r / Mf_); _j4 = min(int(np.searchsorted(RM, rta)) + 1, len(RM) - 1); HM.setdefault("K4b", []).append(abs(float(Mc[_j4]) / float(Mh[_j4]) - 1)); HM.setdefault("K4d", []).append((int(i), hk, mfr / m0r - 1, float(np.interp(rta, RM, np.interp(np.minimum(RM, rta), RM, Mbf))) / m0r, m0r / Mf_, rta / NX["MPC"], int(NX["T3M"][i]), float(np.max(np.abs(np.diff(Mc) / np.maximum(Mc[1:], 1e-300))))))
        if len(HM["flip"]) < 2000 and hk == "h0672": HM["flip"].append(tuple(float(np.interp(q_ * NX["MPC"], RM, Mc) / np.interp(q_ * NX["MPC"], RM, Mh)) for q_ in (0.05, 0.15, 0.3, 0.46, 1.0, 2.0)))
    elif HM["dump"] is not None and foot == "canonical" and hk == "h0672":
        HM["ratio"].append(float(np.interp(rta, RM, Mh)) / Mf_)
    if HM["dump"] is not None and foot == "canonical" and hk == "h0672" and int(NX["T3M"][i]) == 2:
        _R = [0.05, 0.1, 0.2, 0.3, 0.46, 0.7, 1.0, 1.42, 2.06, 3.0, 4.5]; _rho = np.gradient(Mc, RM) / (4 * np.pi * RM ** 2); _M2, _R2, _ = zn1_m200_fs(Mb, z); _R2 = _R2 if _R2 else 1.2 * NX["MPC"]
        HM["dump"].setdefault("clusters", []).append(dict(i=i, R200=_R2 / NX["MPC"], rta=rta / NX["MPC"], Mfair=Mf_ / MSUNE, Mrta=float(np.interp(rta, RM, Mc)) / MSUNE, M200_c=float(np.interp(_R2, RM, Mc)) / MSUNE, Mc=[float(np.interp(q_ * NX["MPC"], RM, Mc)) / MSUNE for q_ in _R], Mb=[float(np.interp(q_ * NX["MPC"], RM, Mbf)) / MSUNE for q_ in _R], rho=[float(np.interp(q_ * NX["MPC"], RM, _rho)) * NX["MPC"] ** 3 / MSUNE for q_ in _R]))
        HM["dump"].setdefault("V", {}); _P = hm1_pieces(i, foot, hk, pp, Mbf, Mc, _R2)
        for k_, v_ in _P.items(): HM["dump"]["V"].setdefault(k_, np.zeros((NX["N"], 8)))[i] = v_
    return Mbf + Mc
def hm1_x(fn, mbx, rta, Mfair, Mbt, foot):
    "X-COP: as XH1 (no BCG). f = 0, native: fn itself, so ZN4 is reproduced exactly. S path: s at the fair total, as UR1's _xcop, not MA1's argument."
    if HM["path"] == "native" and HM["f"] == 0.0: return fn
    if HM["path"] == "S": s_ = sig_core(foot, "A_c2b_refit", (Mfair + Mbt) / MSUNE, True)[0]; r0_ = solve_r0(Mfair, rta, s_); M0 = math.pi * s_ * r0_ ** 2 * B(np.minimum(RM, rta) / r0_)
    else: M0 = fn(np.minimum(RM, rta))
    Mc = hm1_resp(mbx, M0, rta, Mfair); return lambda r: np.interp(r, RM, Mc)
