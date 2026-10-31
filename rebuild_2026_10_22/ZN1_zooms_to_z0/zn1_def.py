# ZN1 (criteria 22d690ccf2, A1, A2): the native z = 0 profile on the cluster path. Injected before grade_clusters in FC1's grader text, after MA1's definition.
ZN1_MODE = os.environ.get("ZN1_MODE", "fs"); ZN1_RX = float(os.environ.get("ZN1_RX", "1")); ZN1_SNAP = os.environ.get("ZN1_SNAP", "nearest"); ZN1_STAT = dict(cells=0, no_tail=0, no_fs=0, gam=[], k4=0.0, ratio=[])
_ZS = json.load(open(os.environ["ZN1_SHAPES"])); _ZX = np.log(np.array(_ZS["x"]))
def zn1_shape(lgM, z):
    k = ZN1_SNAP if ZN1_SNAP != "nearest" else ("0.00" if z < 0.125 else "0.25" if z < 0.375 else "0.50"); a, b = _ZS["1e13"][k], _ZS["1e14"][k]
    w = float(np.clip((lgM - a["lgM"]) / (b["lgM"] - a["lgM"]), 0.0, 1.0)); return (1 - w) * np.array(a["lnm"]) + w * np.array(b["lnm"]), min(a["x_edge"], b["x_edge"])
def zn1_m200_fs(Mb, z):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); thr = 200 * rc * (NAT_OM * (1 + z) ** 3 + 1 - NAT_OM)
    d = (1 + NAT_RRAT) * Mb / (4 / 3 * math.pi * RM ** 3); i = np.where(d >= thr)[0]
    if len(i) == 0: return None, None, thr
    i = int(i.max()); lr = math.log(RM[i]) + (math.log(thr) - math.log(d[i])) / (math.log(d[i + 1]) - math.log(d[i])) * (math.log(RM[i + 1]) - math.log(RM[i])); R = math.exp(lr)
    return thr * 4 / 3 * math.pi * R ** 3, R, thr
def zn1_fn(foot, tag, pp, z):
    if ZN1_MODE == "ma1":
        M = ma1_arg(foot, tag, pp); s = sig_core(foot, tag, M, True)[0]; r0_ = solve_r0(pp["Mfair"], pp["rta"], s); return lambda r: math.pi * s * r0_ ** 2 * B(np.minimum(r, pp["rta"]) / r0_)
    Mfs, Rfs, thr = zn1_m200_fs(pp["Mb"], z)
    if ZN1_MODE == "budget" or Mfs is None:   # AMENDMENT A2 item 6: no fair-share R200 exists for a few gas-poor systems; counted
        M2 = ma1_arg(foot, tag, pp) * MSUNE; R2 = (3 * M2 / (4 * math.pi * thr)) ** (1 / 3); ZN1_STAT["no_fs"] += 0 if ZN1_MODE == "budget" else 1
    else: M2, R2 = Mfs, Rfs
    ln, xe = zn1_shape(math.log10(M2 / MSUNE), z); fc = NAT_RRAT / (1 + NAT_RRAT); ZN1_STAT["cells"] += 1; ZN1_STAT["k4"] = max(ZN1_STAT["k4"], abs((1 + NAT_RRAT) * float(np.interp(R2, RM, pp["Mb"])) / M2 - 1) if (ZN1_MODE == "fs" and Mfs is not None) else 0.0); ZN1_STAT["ratio"].append(M2 / ((pp["Mfair"] + float(pp["Mb"][-1]))))
    lnm = lambda x: np.where(x >= math.exp(_ZX[0]), np.interp(np.log(np.maximum(x, 1e-300)), _ZX, ln), ln[0] + 2 * (np.log(np.maximum(x, 1e-300)) - _ZX[0]))
    re = xe * R2; rta, Mf = pp["rta"], pp["Mfair"]; Mc = lambda r: fc * M2 * np.exp(lnm(np.asarray(r, float) / (R2 * ZN1_RX)))
    if re >= rta: return lambda r: Mc(np.minimum(r, rta))
    Me = float(Mc(re)); k = np.searchsorted(_ZX, math.log(xe / ZN1_RX)); dln = float((ln[k] - ln[k - 8]) / (_ZX[k] - _ZX[k - 8])); rhoe = Me * dln / (4 * math.pi * re ** 3)
    if Me >= Mf:
        ZN1_STAT["no_tail"] += 1; return lambda r: np.where(np.asarray(r, float) <= re, Mc(r), Me)
    L = math.log(rta / re); tgt = (Mf - Me) / (4 * math.pi * rhoe * re ** 3); I_ = lambda g: L if abs(3 - g) < 1e-9 else (math.expm1(min((3 - g) * L, 700.0))) / (3 - g); _lo, _hi = -40.0, 60.0
    while I_(_lo) < tgt: _lo = 3 - 2 * (3 - _lo)
    while I_(_hi) > tgt: _hi = 3 + 2 * (_hi - 3)
    gam = brentq(lambda g: I_(g) - tgt, _lo, _hi, xtol=1e-9, maxiter=500); ZN1_STAT["gam"].append(gam); ZN1_STAT["wide"] = ZN1_STAT.get("wide", 0) + (1 if not (-40.0 <= gam <= 60.0) else 0)
    def f(r):
        r = np.minimum(np.asarray(r, float), rta); y = np.maximum(r / re, 1.0); t_ = np.log(y) if abs(3 - gam) < 1e-9 else (y ** (3 - gam) - 1) / (3 - gam)
        return np.where(r <= re, Mc(r), Me + 4 * math.pi * rhoe * re ** 3 * t_)
    return f
