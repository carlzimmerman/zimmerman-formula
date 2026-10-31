# MA1 (criteria b22583d196): collapsed mass as the cluster path's argument. Injected before grade_clusters in FC1's grader text.
MA1_MODE = os.environ.get("MA1_MODE", "m200"); MA1_MULT = float(os.environ.get("MA1_MULT", "1")); MA1_STAT = dict(cells=0, maxit=0, k2=0.0, nonconv=0, over=0, ratio=[], sratio=[])
def ma1_arg(foot, tag, pp):
    Mta = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
    if MA1_MODE == "off" or SHAPE["s"] != "S": return Mta
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    thr = 200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc
    Mb_, rta, Mt, conv, it = pp["Mb"], pp["rta"], Mta, False, 0
    for it in range(1, 101):
        s = sig_core(foot, tag, MA1_MULT * Mt, True)[0]; r0 = solve_r0(pp["Mfair"], rta, s)
        mt_ = lambda r: float(np.interp(r, RM, Mb_)) + math.pi * s * r0 ** 2 * float(B(r / r0))
        R2 = math.exp(brentq(lambda lr: math.log(mt_(math.exp(lr)) / (thr * 4 / 3 * math.pi * math.exp(3 * lr))), math.log(rta * 1e-3), math.log(rta), xtol=1e-12))
        Mn = thr * 4 / 3 * math.pi * R2 ** 3 / MSUNE; d = abs(math.log(Mn / Mt)); Mt = Mn
        if d <= 1e-8: conv = True; break
    if ETA_USE["v"] == ETA:
        St = MA1_STAT; St["cells"] += 1; St["maxit"] = max(St["maxit"], it); St["nonconv"] += 0 if conv else 1; St["over"] += 0 if Mt < Mta else 1
        St["k2"] = max(St["k2"], abs(mt_(R2) / (thr * 4 / 3 * math.pi * R2 ** 3) - 1)); St["ratio"].append(Mt / Mta); St["sratio"].append(sig_core(foot, tag, MA1_MULT * Mt, True)[0] / sig_core(foot, tag, Mta, True)[0])
    return MA1_MULT * Mt
