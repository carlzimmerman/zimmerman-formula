# HM1 tail, inside the grader after ZN1's tail. kappa = 1/2 FITTED, unused; not theory closed.
_PF = os.environ["HM1_PART"]; _PART = json.load(open(_PF)) if os.path.exists(_PF) else {}
_rr = np.geomspace(RM[0], RM[-1], 2000)
def _hmcells(gc):
    O = {}
    for h in ("h0672", "h0686"):
        m = _OUT["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in gc["cells"][h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
_Z0 = lambda r_: float(np.max(np.abs(contract(RM, np.zeros_like(RM), r_, 0.0)[0] / np.maximum(r_, 1e-300) - 1)[5:-5]))
for _lab, _cfg in json.loads(os.environ["HM1_CELLS"]):
    if _lab in _PART: continue
    HM.update(path=_cfg.get("path", "native"), f=_cfg.get("f", 0.0), gn=_cfg.get("gn", False), bcg=_cfg.get("bcg", False), fmode=_cfg.get("fmode", "own"), amend=_cfg.get("amend", False), K4d=[], K4=[], ratio=[], flip=[], dump={} if _cfg.get("dump") else None, K3=0.0); _t = time.time() if "time" in globals() else 0
    PREP.clear(); gc = grade_clusters("canonical"); O = _hmcells(gc); x = _grade("canonical"); r_ = dict(cells=O, xcop=dict(mean=x["mean"], rms=x["rms"], by_x=x["by_x"], per=x["per_cluster"], rows=[dict(c=v["cluster"], x=v["x"], r=v["r_kpc"], Mh=v["Mh_Msun"], Mb=v["Mb_Msun"], d=v["d"]) for v in x["rows"]] if _cfg.get("dump") else None), K4=max(HM["K4"]) if HM["K4"] else 0.0, K4n=int(sum(v > 1e-3 for v in HM["K4"])), ratio=[float(np.percentile(HM["ratio"], q_)) for q_ in (16, 50, 84)] if HM["ratio"] else None)
    r_["K4b"] = [float(np.max(HM.get("K4b", [0.0]))), int(sum(v_ > 1e-3 for v_ in HM.get("K4b", [])))]; HM["K4b"] = []
    r_["K4d"] = [v_ for v_ in HM["K4d"] if abs(v_[2]) > 1e-3][:400]
    if HM["flip"] and HM["path"] == "hybrid": _fl = HM["flip"]; r_["hyb_M3"] = {k_: [float(np.percentile([v_[k_] for v_ in _fl if isinstance(v_, dict) and v_["T3"] == 2], q_)) for q_ in (16, 50, 84)] for k_ in ("rx", "step", "Mrta")}; r_["hyb"] = {k_: [float(np.percentile([v_[k_] for v_ in _fl if isinstance(v_, dict)], q_)) for q_ in (16, 50, 84)] for k_ in ("rx", "step", "Mrta")}
    elif HM["flip"]: r_["flip"] = np.median(np.array([v_ for v_ in HM["flip"] if not isinstance(v_, dict)]), axis=0).tolist()
    if _cfg.get("alt"): PREP.clear(); _ga = grade_clusters("alt"); r_["alt"] = {h_: {k_: dict(pred=v_["pred"], Z=v_["Z"]) for k_, v_ in _ga["cells"][h_].items()} for h_ in _ga["cells"]}
    if HM["dump"] is not None:
        D = HM["dump"]; vC = bsum(DC_[("canonical", "h0672")]); m_ = T3M == 2; rawC = DC_[("canonical", "h0672")]; r_["dump"] = dict(clusters=D["clusters"], shares={k_: dict(OUTER=float(v_[m_][:, [6, 7]].sum() / rawC[m_][:, [6, 7]].sum()), MID=float(v_[m_][:, [3, 4, 5]].sum() / rawC[m_][:, [3, 4, 5]].sum()), INNER=float(v_[m_][:, [0, 1, 2]].sum() / rawC[m_][:, [0, 1, 2]].sum()), bins=[float(v_[m_, b_].sum() / rawC[m_, b_].sum()) for b_ in range(8)]) for k_, v_ in D["V"].items()})
    _PART[_lab] = r_; json.dump(_PART, open(_PF + ".tmp", "w"), default=float); os.replace(_PF + ".tmp", _PF); print("HM1 cell", _lab, flush=True)
_X1 = []
for c_ in _XC:
    nm = c_["name"]; Mbt, rta = _budget(nm); Mfair = NAT_RRAT * Mbt; _mbx = _gc2(_XM[nm]["Mg500"], _XM[nm]["r500"] / 1e3, _XM[nm]["z"], 3.0 * 1.2 * _XM[nm]["Mg500"] * _MSX)[0]; HM.update(path="native", f=0.0); fn_ = zn1_fn("canonical", _TBG, dict(Mb=_mbx, Mfair=Mfair, rta=rta), _XM[nm]["z"]); s_ = sig_core("canonical", _TBG, (Mfair + Mbt) / MSUNE, True)[0]; r0_ = solve_r0(Mfair, rta, s_)
    for x, r, mh, mb in c_["rows"]:
        if abs(x - 1.0) > 1e-9: continue
        rm = r * 1e3 * _PCm; Mn_ = float(fn_(np.array([min(rm, rta)]))[0]); Ms_ = math.pi * s_ * r0_ ** 2 * float(B(min(rm, rta) / r0_)); _X1.append(dict(c=nm, r=r, N=math.log10(mh * MSUNE / (mb * MSUNE + Mn_)), S=math.log10(mh * MSUNE / (mb * MSUNE + Ms_)), Mfair=Mfair / MSUNE, Mh=mh, Mb=mb, MnF=Mn_ / Mfair, MsF=Ms_ / Mfair))
_OUT["hm1_x1"] = _X1
_OUT["hm1"] = _PART; _OUT["hm1_K3"] = max(_Z0(zn1_fn("canonical", "A_c2b_refit", prep(int(i_), "canonical", "h0672"), NX["CL"][int(i_)]["z"])(RM)) for i_ in ALLI[::16]); _OUT["hm1_R"] = dict(RMmin=float(RM[0] / NX["MPC"]), RMmax=float(RM[-1] / NX["MPC"]), n=len(RM)); _OUT["hm1_T3"] = T3M.tolist()
