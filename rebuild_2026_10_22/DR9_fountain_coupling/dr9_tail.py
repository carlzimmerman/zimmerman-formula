# DR9 tail: galaxy-dependent energy coupling on the response. Appended to UR1's helper section, read only. kappa = 1/2 FITTED, unused; not theory closed.
_D = os.environ["DR9_HERE"]; _G = dict(C=0.0, ret="RET", after=False, invert=False, bypass=False); _CTX = [None]; _CTR0 = contract; _FS = {}; _NZ = [0]
FREQ = 0.175; M_CM1 = 6.18978999038917e11
def _W(rg, Mb, Mc):
    dM = np.diff(Mc); rm = 0.5 * (rg[1:] + rg[:-1]); return -GE * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
def _ESN(Ms): return Ms / 100.0 * 1e44
def _eta(fl): x = (1.0 / (1 + fl)) if _G["invert"] else fl / (1 + fl); return x * x
def _Rf(Ms, Mbt, M2, ret): return min(1.0, (1 + NAT_RRAT) * Mbt / M2) if ret == "RET" else min(1.0, Ms * MSUNE / Mbt)
def _at(r0, rg, X): return float(np.interp(math.log(r0), np.log(rg), X))
def _gate(rg, Mb, M0, Mf, r0, Ms, Mbt, M2):
    if _G["C"] == 0: return 1.0
    Eu = max(0.0, (_W(rg, Mb, M0) - _W(rg, Mb, Mf)) / 2)
    if Eu <= 0: _NZ[0] += 1; return 1.0
    fl = _at(r0, rg, Mb) / _at(r0, rg, Mf if _G["after"] else M0); return 1.0 - min(1.0, _G["C"] * _eta(fl) * _Rf(Ms, Mbt, M2, _G["ret"]) * _ESN(Ms) / Eu)
def contract(r, Mb, M0, F, gnedin=None):
    Mf, c_, x_ = _CTR0(r, Mb, M0, F, gnedin=gnedin)
    if _G["bypass"]: return Mf, c_, x_
    fr = sys._getframe(1).f_locals
    if "Mtot_" in fr and "q" in fr: q_ = fr["q"]; Ms = fr["U"] * q_["meta"]["L36"] * 1e9; x = _gate(r, Mb, M0, Mf, fr["r0"], Ms, fr["Mtot_"], fr["M2"]); _FS[(fr.get("tag"), q_["name"], round(float(fr["U"]), 4))] = x
    else: c = _CTX[0]; x = _gate(r, Mb, M0, Mf, c["r0"], c["Ms"], c["Mbt"], c["M2"]); _FS[("ctx", c["n"], 0)] = x
    return M0 + x * (Mf - M0), c_, x_
def _lt2(tag, f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); E = []
    for r_ in _C["lt"]:
        M2, R2 = _SL3M(r_["logMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); R_ = r_["R"] * MPCE / 1e3; Mb = 10 ** r_["logMb"] * MSUNE; rg = np.geomspace(R_ * 1e-3, R2, 600); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = Mb * np.minimum(rg / R_, 1.0) ** 2; _CTX[0] = dict(r0=r0, Ms=float(r_["Mstar"]), Mbt=Mb, M2=M2 * MSUNE, n="lt" + r_["name"]); Mc = float(np.interp(math.log(R_), np.log(rg), contract(rg, Mbg, M0g, Mb / (M2 * MSUNE))[0])); E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(GE * Mb / R_ ** 2 + GE * Mc / R_ ** 2))
    return float(np.median(E))
def _groups2(f="canonical"):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540); d = []; sl = []
    def one(o, dl):
        lMb = o["lM"] + dl; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE; M2, R2 = _SL3M(lMb, bg, rc); s, _ = sig_core(f, "A_c2b_refit", M2 / FC1_MC); r0 = solve_r0(M2 * MS540, R2, s); rr = XG * a
        rg = np.geomspace(min(rr[0], R2 * 1e-4), R2, 800); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = np.interp(np.log(rg), np.log(rr), Mb * M_H); _CTX[0] = dict(r0=r0, Ms=10 ** lMb, Mbt=Mb, M2=M2 * MS540, n="gr"); Mcg = contract(rg, Mbg, M0g, float(Mbg[-1] / M0g[-1]))[0]; Mc = np.interp(np.log(rr), np.log(rg), Mcg)
        gN = M_H / XG ** 2 + Mc / Mb / XG ** 2; s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a; return 0.5 * math.log10(s2) - 3.0
    for o in GROUPS: d.append(o["ls"] - one(o, 0.0)); sl.append((one(o, 0.01) - one(o, -0.01)) / 0.02)
    return NSG["class_stats"](d, sl)
def _row(C=0.0, ret="RET", after=False, invert=False):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLMAP["mut"] = 1.0; CN1_MODE = "blum"; _G.update(C=C, ret=ret, after=after, invert=invert, bypass=False); GHSTORE.clear(); _FS.clear(); _NZ[0] = 0; r = dict(C=C, ret=ret, after=after, invert=invert, sparc={}); f = "canonical"; iu = float(UPS[int(np.argmin(abs(UPS - 0.5)))])
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
        fb = {}
        for l, h in _BIN:
            x = [val for (tg, n, U_), val in _FS.items() if tg == t and U_ == round(iu, 4) and n in _TB and _TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30 and l <= _TB[n]["vf"] < h]
            fb[f"{l}-{h}"] = float(np.median(x)) if x else None
        r["sparc"][t]["f_at_U05"] = fb
    r["fmin"] = float(min(_FS.values())) if _FS else 1.0; r["fmax"] = float(max(_FS.values())) if _FS else 1.0; r["n_eu0_sparc"] = _NZ[0]; r["lt"] = {t: _lt2(t) for t in _TG}; g = _groups2(); r["groups"] = dict(Z=float(g["Z"]), verdict=g["verdict"]); return r
def _energy2(tag="A_c2b_refit", f="canonical"):
    _G.update(bypass=True); bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); ju = int(np.argmin(abs(UPS - 1.0))); ku = int(np.argmin(abs(UPS - 0.75))); RD = {}; nl = 0.0
    for _l in open(_MRT):
        _p = _l.split()
        if len(_p) >= 18:
            try: RD[_p[0]] = float(_p[11]) * 3.0857e19
            except ValueError: pass
    A = []; U = float(UPS[iu])
    for q in GALS:
        t = _TB.get(q["name"]); rd = RD.get(q["name"], 0.0)
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30 or rd <= 0: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 400); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        Mbg = np.maximum.accumulate(Mbg); Mf = _CTR0(rg, Mbg, M0, Mt / (M2 * MSUNE))[0]; Ms = U * q["meta"]["L36"] * 1e9; Eu = max(0.0, (_W(rg, Mbg, M0) - _W(rg, Mbg, Mf)) / 2); Mb0 = _at(r0, rg, Mbg); Mc0 = _at(r0, rg, M0); Mfr = _at(r0, rg, Mf); fl = Mb0 / Mc0; fa = Mb0 / Mfr
        st_g = (q["GB"][:, ju] - q["GB"][:, iu]) / (UPS[ju] - UPS[iu]); gs_g = q["GB"][:, iu] - UPS[iu] * st_g; nl = max(nl, float(np.max(np.abs(gs_g + UPS[ku] * st_g - q["GB"][:, ku]))) / max(float(np.max(np.abs(q["GB"][:, ku]))), 1e-300)); Mgk = np.maximum.accumulate(np.maximum(gs_g * Rm ** 2 / GE, 0.0)); Mg0 = float(np.interp(math.log(r0), np.log(Rm), Mgk)) if r0 > Rm[0] else float(Mgk[0] * (r0 / Rm[0]) ** 2); etag = (Mg0 / (Mb0 + Mc0)) ** 2; dWPG = 40 * Mc0 * GE * (Mb0 + Mc0) / r0 * etag; V = t["vf"] * 1e3
        A.append(dict(name=q["name"], vf=t["vf"], M200=M2, fl=fl, fa=fa, Q=Mfr / Mc0, sf=Ms * MSUNE / Mt, fret=(1 + NAT_RRAT) * Mt / (M2 * MSUNE), eta=(fl / (1 + fl)) ** 2, etaa=(fa / (1 + fa)) ** 2, ESN=_ESN(Ms), Eu=Eu, efull=Eu / _ESN(Ms) if Eu > 0 else 0.0, etag=etag, PG=dWPG / Eu if Eu > 0 else float("inf"), PGsn=dWPG / _ESN(Ms), Trot_Eundo=0.5 * Mt * V ** 2 / Eu if Eu > 0 else float("inf"), fgr0=Mg0 / max(Mb0, 1e-300)))
    for a in A:
        a["R_ret"] = min(1.0, a["fret"]); a["R_star"] = min(1.0, a["sf"]); a["cR"] = a["eta"] * a["R_ret"]; a["cS"] = a["eta"] * a["R_star"]; a["dW_ret"] = a["cR"] * a["ESN"] / a["Eu"] if a["Eu"] > 0 else float("inf"); a["dW_star"] = a["cS"] * a["ESN"] / a["Eu"] if a["Eu"] > 0 else float("inf"); a["dWa_ret"] = a["etaa"] * a["R_ret"] * a["ESN"] / a["Eu"] if a["Eu"] > 0 else float("inf")
    ks = ("fl", "fa", "Q", "sf", "fret", "eta", "etaa", "cR", "cS", "ESN", "Eu", "efull", "etag", "PG", "PGsn", "dW_ret", "dW_star", "dWa_ret", "Trot_Eundo", "fgr0", "M200"); O = {}
    for l, h in _BIN:
        S = [a for a in A if l <= a["vf"] < h]; O[f"{l}-{h}"] = dict(n=len(S), **{k: float(np.median([a[k] for a in S])) for k in ks})
    H = [a for a in A if abs(math.log10(a["M200"] / M_CM1)) <= 0.3]; F = [a for a in A if 150 <= a["vf"] < 200]; mdn = lambda K, S_: float(np.median([a[K] for a in S_]))
    lo = [a for a in A if 20 <= a["vf"] < 100]; hi = [a for a in A if 150 <= a["vf"] < 250]
    res = dict(bins=O, n_cm1=len(H), etaR_cm1=dict(RET=mdn("cR", H), STAR=mdn("cS", H)), C_FIT=dict(RET=float(np.median([(1 - FREQ) * a["Eu"] / (a["cR"] * a["ESN"]) for a in F])), STAR=float(np.median([(1 - FREQ) * a["Eu"] / (a["cS"] * a["ESN"]) for a in F]))), order=dict(dW_ret=mdn("dW_ret", hi) / mdn("dW_ret", lo), dW_star=mdn("dW_star", hi) / mdn("dW_star", lo), cR=mdn("cR", hi) / mdn("cR", lo), cS=mdn("cS", hi) / mdn("cS", lo), efull=mdn("efull", hi) / mdn("efull", lo), PG=mdn("PG", hi) / mdn("PG", lo)), gb_linearity=nl, rrat1=1 + NAT_RRAT, G_ratio=G540 / GE, Ms_ratio=MS540 / MSUNE, n_fret_capped=sum(a["fret"] > 1 for a in A), n=len(A)); _G.update(bypass=False); return res
def _clusters(C, f="canonical"):
    """Diagnostic only: f_local with and without BCG, and coupling against the response's energy change, at each C."""
    _G.update(bypass=True); hk = HK[0]; fs = float(os.environ["X73_FSTAR"]); O = []
    for i in ALLI[::4]:
        i = int(i); pp = prep(i, f, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE; s, _ = sig_core(f, "A_c2b_refit", Mtot, True); r0 = solve_r0(pp["Mfair"], pp["rta"], s); M0 = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0); Mbn = pp["Mb"]; Mbf = Mbn + BCGF[i] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2; Fc = float(np.interp(pp["rta"], RM, Mbf)) / pp["Mfair"]; Mf = _CTR0(RM, Mbf, M0, Fc)[0]; r5 = 0.05 * NX["MPC"]; m = RM <= pp["rta"]; dWr = (_W(RM[m], Mbf[m], M0[m]) - _W(RM[m], Mbf[m], Mf[m])) / 2; Mbt = float(np.interp(pp["rta"], RM, Mbf)); Ms = (fs / (1 + fs) * float(np.interp(pp["rta"], RM, Mbn)) + BCGF[i] * MSUNE) / MSUNE; fl0 = _at(r0, RM, Mbf) / _at(r0, RM, M0); e = (fl0 / (1 + fl0)) ** 2; O.append(dict(r0_Mpc=r0 / NX["MPC"], fl5_noBCG=float(np.interp(r5, RM, Mbn) / np.interp(r5, RM, M0)), fl5_BCG=float(np.interp(r5, RM, Mbf) / np.interp(r5, RM, M0)), Qr5=float(np.interp(r5, RM, Mf) / np.interp(r5, RM, M0)), flr0_BCG=fl0, dWr_J=dWr, ESN=_ESN(Ms), eta=e, ratio_C1=e * _ESN(Ms) / abs(dWr) if dWr != 0 else float("nan"), inward=float(dWr > 0)))
    PREP.clear(); _G.update(bypass=False); return {k: float(np.median([a[k] for a in O])) for k in O[0]}
def _put(n, o):
    p = os.path.join(_D, n); open(p + ".tmp", "w").write(json.dumps(o, indent=1, default=float)); os.replace(p + ".tmp", p)
def _ck(n, fn):
    p = os.path.join(_D, n)
    if os.path.exists(p): return json.load(open(p))
    o = fn(); _put(n, o); print("DR9", n, flush=True); return o
_E = _ck("dr9_energy.json", _energy2); _cm = json.load(open(os.path.join(REB, "CM1_outflow_coupling", "cm1_results.json")))["setup"]; _wP = json.load(open(os.path.join(REB, "CM1_outflow_coupling", "cm1_run_PRIMARY.json")))["W"]; _eCM = _wP * _cm["Eunit_erg"] / json.load(open(os.path.join(REB, "CM1_outflow_coupling", "cm1_results.json")))["E_SN_erg"]
_CS = dict(eps_CM1=_eCM, RET_CM1=_eCM / _E["etaR_cm1"]["RET"], STAR_CM1=_eCM / _E["etaR_cm1"]["STAR"], RET_FIT=_E["C_FIT"]["RET"], STAR_FIT=_E["C_FIT"]["STAR"]); _put("dr9_constants.json", _CS)
_ck("dr9_clusters.json", lambda: _clusters(1.0))
for _n, _a in (("C0", dict(C=0.0)), ("CINF", dict(C=1e9)), ("RET_C1", dict(C=1.0)), ("RET_CM1", dict(C=_CS["RET_CM1"])), ("RET_FIT", dict(C=_CS["RET_FIT"])), ("STAR_C1", dict(C=1.0, ret="STAR")), ("STAR_CM1", dict(C=_CS["STAR_CM1"], ret="STAR")), ("STAR_FIT", dict(C=_CS["STAR_FIT"], ret="STAR")), ("RET_FIT_AFTER", dict(C=_CS["RET_FIT"], after=True)), ("MUTATE", dict(C=_CS["RET_FIT"], invert=True)), ("MUTATE_A1", dict(C=_CS["RET_FIT"] * 0.01))):
    _ck(f"dr9_row_{_n}.json", lambda: _row(**_a))
print("DR9 done", flush=True); sys.exit(0)
