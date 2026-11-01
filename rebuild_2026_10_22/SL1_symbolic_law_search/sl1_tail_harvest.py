# SL1 tail: runs inside NF1's grader namespace (XH1's tail text first, for its X-COP rows), in place of its last line. Dumps what discover_law.py needs. Reads only.
import pickle as _pk, contextlib as _cl, io as _io, time as _tm
_T0 = _tm.time(); _C = {}; _F0 = "canonical"; _TAGS = ("A_c2b_refit", "B_cfg886_bg"); _KN = 24
_MRT = os.path.join(REB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt"); _TAB = {}
for _l in open(_MRT):
    _p = _l.split()
    if len(_p) < 18: continue
    try: _TAB[_p[0]] = dict(inc=float(_p[5]), rd=float(_p[11]), vf=float(_p[15]), Q=int(_p[17]))
    except ValueError: pass
def _halo(tag, M2sun):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); R200 = (3 * M2sun * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); Mt = M2sun / FC1_MC
    s, a_ = sig_core(_F0, tag, Mt); r0 = solve_r0(M2sun * MSUNE, R200, s); sc, zf, _ = sigma_coll(tag, Mt); eta = s / (FC1_F * sc * MSUNE / PC2)
    return dict(M2=M2sun * MSUNE, R200=R200, S=s, r0=r0, eta=eta, zf=zf)
_C["UPS"] = np.asarray(UPS); _C["const"] = dict(GE=GE, MSUNE=MSUNE, MPCE=MPCE, PC2=PC2, FC=FC1_F, A0=dict(A0), FSTAR=FSTAR, NAT_RRAT=NAT_RRAT)
_g = []
for q in GALS:
    t = _TAB.get(q["name"], {}); h = {}
    for tag in _TAGS:
        bg = BGS[tag]; h[tag] = _halo(tag, 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)))
    _g.append(dict(name=q["name"], Rm=q["Rm"], GB=q["GB"], GO=q["GO"], W=q["W"], OK=q["OK"], lMb=q["lMb"], L36=q["meta"]["L36"], MHI=q["meta"]["MHI"], vf=t.get("vf", float("nan")), Q=t.get("Q", 9), inc=t.get("inc", 0.0), halo=h))
_C["gals"] = _g
# LITTLE THINGS, ND1's rows
_RTF = os.path.join(REB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade.py"); _RTT = open(_RTF).read(); _cut = 'RES = dict(criteria="ac267e8bf1"'; _RTN = {"__file__": _RTF, "__name__": "rt1_ro"}; _av = sys.argv; sys.argv = [_RTF]
with _cl.redirect_stdout(_io.StringIO()): exec(compile(_RTT[:_RTT.index(_cut)], _RTF, "exec"), _RTN)
sys.argv = _av; _lt = []
for nm in _RTN["NAMES"]:
    r_ = _RTN["rec"](nm)[0]; d = _RTN["E_rot"](r_, _RTN["A0"]["canonical"], "MSED")
    if not d: continue
    h = {}
    for tag in _TAGS:
        bg = BGS[tag]; h[tag] = _halo(tag, 10 ** (bg["a"] + bg["b"] * (d["logMb"] - 10)))
    _lt.append(dict(name=nm, logMb=d["logMb"], R=d["R"], V=d["V"], Mstar=r_["MSED"][0] * 1e7, halo=h))
_C["lt"] = _lt
# ND1's rule at its own table, for K5
_CE4 = json.load(open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_a4_results.json")))["eta"]; _EA4 = [_CE4[str(e)]["med"] for e in (12, 13, 14)]; _X80 = json.load(open(os.path.join(REB, "X80_low_mass_floor_emergence", "x80_converged.json")))
def _nd1_E(d, tag):
    bg = BGS[tag]; M = 10 ** (bg["a"] + bg["b"] * (d["logMb"] - 10)); rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); Mt = M / FC1_F; lg = math.log10(Mt)
    tr = 10 ** float(np.interp(lg, [10.0, 11.0, 12.0], [math.log10(_X80["r10"]), math.log10(_X80["r11"]), 0.0])); c = FC1_F * float(np.interp(lg, [12, 13, 14], _EA4)) * tr * sigma_coll(tag, max(Mt, 10 ** (7.0 + math.log10(2.0))))[0] * MSUNE / PC2; r0 = solve_r0(M * MSUNE, R200, c)
    Rr = d["R"] * MPCE / 1e3; gN = GE * 10 ** d["logMb"] * MSUNE / Rr ** 2; gh = GE * math.pi * c * r0 ** 2 * float(B(Rr / r0)) / Rr ** 2; return math.log10((d["V"] * 1e3) ** 2 / Rr) - math.log10(gN + gh)
_C["K5_nd1"] = {tag: float(np.median([_nd1_E(d, tag) for d in _lt])) for tag in _TAGS}
# groups at identity and the two mass steps grade_groups uses
_gr = []
for o in GROUPS:
    r = dict(id=o["id"], ls=o["ls"], lM=o["lM"], Re=o["Re"], slope=(group_logsig(o, _F0, 0.01) - group_logsig(o, _F0, -0.01)) / 0.02, logsig0=group_logsig(o, _F0)); bg = BGS["A_c2b_refit"]
    for dl in (0.0, 0.01, -0.01):
        rc_ = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540); M2_ = 10 ** (bg["a"] + bg["b"] * (o["lM"] + dl - 10)) * MS540; R2_ = (3 * M2_ / (4 * math.pi * 200 * rc_)) ** (1 / 3); s_, _ = sig_core(_F0, "A_c2b_refit", M2_ / MSUNE / FC1_MC); r0_ = solve_r0(M2_, R2_, s_); sc_, zf_, _ = sigma_coll("A_c2b_refit", M2_ / MSUNE / FC1_MC); r[f"h{dl:+.2f}"] = dict(M2=M2_, R200=R2_, S=s_, r0=r0_, eta=s_ / (FC1_F * sc_ * MSUNE / PC2), zf=zf_)
    _gr.append(r)
_C["groups"] = dict(rows=_gr, XG=XG, LXG=LXG, RHO_H=RHO_H, M_H=M_H, HERN_RE=HERN_RE, G=G540, MS=MS540, KP=KP540, K6=grade_groups(_F0))
# X-COP, XH1's rows
_OUTX = {f_: _grade(f_) for f_ in FEET}; _C["xcop"] = {f_: dict(mean=_OUTX[f_]["mean"], rms=_OUTX[f_]["rms"], rows=_OUTX[f_]["rows"], info=_OUTX[f_]["info"]) for f_ in FEET}; _xr = {}
for _c in _XC:
    nm = _c["name"]; Mbt, rta = _budget(nm); Mf = NAT_RRAT * Mbt; Mt_ = (Mf + Mbt) / MSUNE; s, _ = sig_core(_F0, _TBG, Mt_, True); r0 = solve_r0(Mf, rta, s); sc, zf, _ = sigma_coll(_TBG, Mt_); _xr[nm] = dict(Mbt=Mbt, rta=rta, Mfair=Mf, S=s, r0=r0, eta=s / (FC1_F * sc * MSUNE / PC2), zf=zf, z=_XM[nm]["z"])
_C["xcop_halo"] = _xr
# clusters: halo, nodes, linear response, templates
RF_NS = NX["NS2"]["RF"] if "NS2" in NX else None
_cl_out = {}; _RMn = RM; _mpc = NX["MPC"]; _bgA = "A_c2b_refit"
for hk in HK:
    rows = []; DD = NX["DAT"][hk]
    for i in ALLI:
        i = int(i); pp = prep(i, _F0, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE; s, _ = sig_core(_F0, _bgA, Mtot, True); r0 = solve_r0(pp["Mfair"], pp["rta"], s); sc, zf, _ = sigma_coll(_bgA, Mtot); Mh0 = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
        nd = np.geomspace(max(RM[0], 3e-3 * _mpc), pp["rta"], _KN)
        def PS(Mh):
            rho = np.gradient(pp["Mb"] + Mh, RM) / (4 * np.pi * RM ** 2); So = O_(P_(rho), pp["dmpc"]); return A_(DS_(So)) / KG, SB(So)
        P0, S0 = PS(Mh0); LP = np.zeros((8, _KN)); LS = np.zeros((8, _KN)); lr = np.log(RM); ln = np.log(nd); eps = 0.1
        for k in range(_KN - 1):                                                     # the last node stays at rta, where the mass is held
            e_ = np.zeros(_KN); e_[k] = eps; dl = np.interp(lr, ln, e_); Pk, Sk = PS(Mh0 * (1 + dl)); LP[:, k] = (Pk - P0) / eps; LS[:, k] = (Sk - S0) / eps
        rows.append(dict(Mfair=pp["Mfair"], rta=pp["rta"], S=s, r0=r0, zf=zf, eta=s / (FC1_F * sc * MSUNE / PC2), Mbt=float(pp["Mb"][-1]), nd=nd, Mb_nd=np.interp(nd, RM, pp["Mb"]), P0=P0, S0=S0, LP=LP, LS=LS))
    PREP.clear(); _cl_out[hk] = dict(rows=rows, W=DD["W"][ALLI], m2=DD["m2"][ALLI], m=DD["m"][ALLI]); print(f"SL1 harvest {hk} {_tm.time() - _T0:.0f} s, rss {rss():.2f}", flush=True)
_tp = {}
for f_ in FEET:
    for hk in HK:
        cl = f"{f_}|{hk}"; o = M[cl]; r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]; g = {}
        for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"]); g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"]); g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"])
        g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"]); g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"]); g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"]); g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"]); g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"]); g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"])
        for k, A_one in zip(["G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"], [o["M_all|OUTER"]["A"]] + [x_["A"] for x_ in o["M_terc|OUTER"]]):     # RF3 fix_cells: one template
            ma, sa = g[k]; g[k] = (A_one, sa * A_one / ma)
        _tp[cl] = g; _tp[cl + "|vC"] = bsum(DC_[(f_, hk)])
_C["clusters"] = dict(by_hk=_cl_out, tmpl=_tp, I=np.asarray(I), TID=np.asarray(TID), T3M=np.asarray(T3M), X1m=np.asarray(X1m), BN=list(BN), BANDS={b: list(v) for b, v in NX["BANDS"].items()}, N=int(N), NR1_cells={f_: RES["footings"][f_]["clusters"]["cells"] for f_ in FEET})
_C["NR1_sparc"] = {f_: {t: (RES["footings"][f_]["sparc"][t]["U_median"], RES["footings"][f_]["sparc"][t]["rms"]) for t in RES["footings"][f_]["sparc"]} for f_ in FEET}
_wT = [1.0, 2.0]; _kk = np.array([[1.0, 0.3], [1.0, -0.2], [1.0, 0.7]]); _C["wls_probe"] = dict(n=[1.0, 2.0, 3.0], d=[2.0, 1.0, 5.0], X=_kk.tolist(), out=wls1(np.array([1.0, 2.0, 3.0]), np.array([2.0, 1.0, 5.0]), _kk).tolist())
_pk.dump(_C, open(os.environ["SL1_OUT"], "wb"), protocol=4); print(f"SL1 harvest done {_tm.time() - _T0:.0f} s, rss {rss():.2f}", flush=True); sys.exit(0)
