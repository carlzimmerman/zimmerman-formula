# HB1 tail, after UR1's helpers and DR3's read-only head. Reads only. kappa = 1/2 FITTED, unused; no a0 in the cold sector; not theory closed.
import time as _tm
_T0 = _tm.time(); _PT = os.environ["HB_PART"]; _HBD = os.environ["HB_HERE"]; _OF = os.environ["SL1_OUT"]; sys.path.insert(0, _HBD); sys.dont_write_bytecode = True; import hb1_core as _H
_CN = contract; _M = dict(form=None, mut=1.0)
def contract(r, Mb, M0, F, gnedin=None):
    if _M["form"] is None or gnedin is not None: return _CN(r, Mb, M0, F, gnedin=gnedin)
    return _H.contract_hb(r, Mb, M0, _M["form"], mutb=_M["mut"])
def _sum():
    S = _H.ST; x = np.array(S.get("xe") or [0.0]); h = np.array(S["Hc"] or [0.0]); n = np.array(S.get("nroots") or [-1]); o = dict(calls=S["calls"], noroot=S["noroot"], wall=S["wall"], shots_per_call=S["shots"] / max(S["calls"], 1), Hc_pct=np.percentile(h, [5, 50, 95]).tolist(), xe_pct=np.percentile(x, [5, 50, 95]).tolist(), null_sample_n=S["nulls"], null_sample_max=S["nullmax"], roots_hist={str(int(k)): int((n == k).sum()) for k in np.unique(n)}); S.update(calls=0, noroot=0, wall=0, shots=0, Hc=[], nulls=0, nullmax=0.0, nroots=[], xe=[]); return o
def _eff(form, tag="A_c2b_refit", f="canonical"):
    """(Q - 1)/(Q_Blum - 1), Upsilon 0.5, by V_flat; Q = M_f/M_0 at r0, 2, 3, 4 R_d"""
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); U = float(UPS[iu]); O = {f"{l}-{h}": [] for l, h in _BIN}; SLMAP["m"] = "EM1"; _M["form"] = form
    for q in GALS:
        t = _TB.get(q["name"])
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30 or q["meta"]["Rdisk"] <= 0: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 300); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        Mbg = np.maximum.accumulate(Mbg); Qb = _CN(rg, Mbg, M0, Mt / (M2 * MSUNE))[0] / M0; Qh = contract(rg, Mbg, M0, Mt / (M2 * MSUNE))[0] / M0; Rd = q["meta"]["Rdisk"] * NE["KPC_S"]; rr = np.array([r0, 2 * Rd, 3 * Rd, 4 * Rd]); lr = np.log(rr); lg = np.log(rg); qa, qb = np.interp(lr, lg, Qb), np.interp(lr, lg, Qh)
        for l, h in _BIN:
            if l <= t["vf"] < h: O[f"{l}-{h}"].append(dict(f=((qb - 1) / np.where(np.abs(qa - 1) > 1e-6, qa - 1, np.nan)).tolist(), Qb=qa.tolist(), Qh=qb.tolist(), a=R2 / r0, fb=float(Mt / (M2 * MSUNE))))
    _M["form"] = None; return {k: {x: np.nanmedian([a[x] for a in v], axis=0).tolist() for x in ("f", "Qb", "Qh", "a", "fb")} | dict(n=len(v)) for k, v in O.items() if v}
def _setup():
    O = {}; t = "A_c2b_refit"; bg = BGS[t]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); KS = NE["KPC_S"]
    for lg in (10.0, 11.0, 12.0, 13.0, 14.0, 15.0):
        M2 = FC1_MC * 10 ** lg; R2 = (3 * M2 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s, a_ = sig_core("canonical", t, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); O[f"{lg:g}"] = dict(M_c=M2, R200_kpc=R2 / KS, r0_kpc=r0 / KS, a=R2 / r0, Sigma_kg_m2=s, A_kms2=4 * math.pi * GE * s * r0 / 1e6, rho_c_kg_m3=s / r0, M_r0=float(math.pi * s * r0 ** 2 * B(np.asarray(1.0))) / MSUNE)
    O["rho_crit_kg_m3"] = rc; O["OM"] = float(NAT_OM); O["G"] = GE; O["fc"] = float(FC1_MC); return O
_RES = dict(part=_PT, setup=_setup(), runs={}, stats={}, eff={})
if os.path.exists(_OF + ".part"): _RES = json.load(open(_OF + ".part"))   # checkpoint between rows
def _save(): json.dump(_RES, open(_OF + ".part.tmp", "w"), indent=1, default=float); os.replace(_OF + ".part.tmp", _OF + ".part")
def _go(lab, form, mode="blum", dr3=None, mut=1.0, branch=0, eff=False):
    if lab in _RES["runs"]: return
    _M.update(form=form, mut=mut); _H.BRANCH[0] = branch
    if dr3: _D.update(on=True, stars="sb", gas=dr3, mut=1.0)
    _RES["runs"][lab] = _run("EM1", mode); _RES["stats"][lab] = _sum(); _D["on"] = False; _H.BRANCH[0] = 0; _M.update(form=None, mut=1.0)
    if eff: _H.BRANCH[0] = branch; _RES["eff"][lab] = _eff(form); _H.BRANCH[0] = 0; _sum()
    _save(); print(f"HB1 {lab} done {_tm.time() - _T0:.0f} s; stats {_RES['stats'][lab]}", flush=True)
if _PT == "MAIN":
    _go("EM1|off", None, "off"); _go("EM1|blum", None); _go("FormB_E1", "E1", eff=True); _go("FormA", "A", eff=True); _go("FormA_Prho", "A2"); _go("FormB_E2", "E2", eff=True); _go("FormB_E3", "E3", eff=True); _go("FormB_E1_low", "E1", branch=1, eff=True); _go("FormB_E1_high", "E1", branch=2, eff=True)
    _go("FormB_E1_DR3", "E1", dr3="exp")
    if "FormB_E1_GI" not in _RES["runs"]:
        from dr3_gasinv import invert as _inv; _GI = {}
        for _q in GALS: _GI[_q["name"]], _e = _inv(_q["Rm"] / KPC_S, np.sign(_q["Vgas"]) * _q["Vgas"] ** 2, 1.33 * _q["meta"]["MHI"] * 1e9)
        _go("FormB_E1_GI", "E1", dr3="inv")
    _go("NULL_Mbx0", "E1", mut=0.0)
    # continuation on real galaxies, sample
    if "continuation" not in _RES:
        bg = BGS[_TG[0]]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); U = float(UPS[iu]); Cn = []
        for q in GALS[::7]:
            M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core("canonical", _TG[0], M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 300); C = math.pi * s * r0 ** 2; M0 = C * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
            if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
            Mbg = np.maximum.accumulate(Mbg); x = rg / r0; E = _H.eos("E1"); hs = [_H.solve_scaled(x, l * Mbg / C, x[-1], float(M0[-1]) / C, E)[1] for l in np.linspace(0, 1, 21)]; _, hc, _, _, _ = _H.solve_scaled(x, Mbg / C, x[-1], float(M0[-1]) / C, E, branch=1); nr = _H.LASTN[0]; Cn.append(dict(name=q["name"], a=x[-1], Hc=hs[-1], step=float(np.max(np.abs(np.diff(np.log(hs))))), nroots=nr, Mt_over_Mc=Mt / (M2 * MSUNE)))
        _RES["continuation"] = Cn; _save()
elif _PT == "G5":   # gas +0.005 in the driver
    _go("EM1|off", None, "off"); _go("EM1|blum", None); _go("FormB_E1", "E1"); _go("FormA", "A")
elif _PT == "MUTATE":
    _go("MUTATE_Phib_x2_B", "E1", mut=2.0)
elif _PT == "A215":
    _go("FormA_215", "A215", eff=True)
elif _PT == "K3":
    _go("K3_nsub4_B", "E1"); _go("K3_nsub4_A", "A")
elif _PT in ("LOW", "HIGH", "GRID4"):
    _go("EM1|off", None, "off"); _go("EM1|blum", None); _go("FormB_E1", "E1")
os.replace(_OF + ".part", _OF); print("HB1 done", flush=True); sys.exit(0)
