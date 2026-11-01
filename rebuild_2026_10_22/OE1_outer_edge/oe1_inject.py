# OE1 (FROZEN_CRITERIA.md): the edge variants. Injected before grade_clusters, after ZN1's and ZN3's definitions. Read only of other lanes.
_oe_orig = zn1_fn; OE1_ROWS = []; OE1_K2 = dict(max=0.0); OE1_CTX = {}
def _oe_parts(foot, tag, pp, z):
    Mfs, Rfs, thr = zn1_m200_fs(pp["Mb"], z)
    if Mfs is None: M2 = ma1_arg(foot, tag, pp) * MSUNE; R2 = (3 * M2 / (4 * math.pi * thr)) ** (1 / 3); fs = False
    else: M2, R2 = Mfs, Rfs; fs = True
    ln, xe = zn1_shape(math.log10(M2 / MSUNE), z); fc = NAT_RRAT / (1 + NAT_RRAT)
    lnm = lambda x: np.where(x >= math.exp(_ZX[0]), np.interp(np.log(np.maximum(x, 1e-300)), _ZX, ln), ln[0] + 2 * (np.log(np.maximum(x, 1e-300)) - _ZX[0]))
    Mc = lambda r: fc * M2 * np.exp(lnm(np.asarray(r, float) / (R2 * ZN1_RX)))
    ie = int(np.where(np.diff(ln) > 1e-9)[0].max()) + 1; xs = math.exp(_ZX[ie])
    return dict(M2=M2, R2=R2, xe=xe, xs=xs, fs=fs, Mc=Mc)
def zn1_fn(foot, tag, pp, z):
    base = _oe_orig(foot, tag, pp, z)
    if OE1_VAR == "OFF": return base
    q = _oe_parts(foot, tag, pp, z); Mc, R2, rta, Mf = q["Mc"], q["R2"], pp["rta"], pp["Mfair"]
    if OE1_VAR == "E1": f = lambda r: Mc(r)
    elif OE1_VAR == "E2":
        cap = max(float(Mc(rta)), Mf); f = lambda r: np.where(np.asarray(r, float) <= rta, Mc(r), np.minimum(Mc(r), cap))
    elif OE1_VAR == "E3":
        if rta <= R2: return base
        a, b = float(Mc(R2)), float(Mc(rta)); F = (Mf - a) / (b - a)
        def f(r):
            r = np.minimum(np.asarray(r, float), rta); return np.where(r <= R2, Mc(r), a + (Mc(r) - a) * F)
    elif OE1_VAR == "M10": f = lambda r: base(r) + 10.0 * (Mc(r) - base(r))
    elif OE1_VAR == "MZ":
        lo, hi = 1.42 * MPCE, 3.0 * MPCE
        def f(r):
            B_ = base(r); ml, mh = float(base(lo)), float(base(hi)); r = np.asarray(r, float); return np.where(r <= lo, B_, np.where(r <= hi, ml, B_ - (mh - ml)))
    else: raise SystemExit("bad OE1_VAR")
    rr_ = np.geomspace(1e-3, 1.0, 40) * min(rta, q["xe"] * R2); OE1_K2["max"] = max(OE1_K2["max"], float(np.max(np.abs(f(rr_) / base(rr_) - 1)))) if OE1_VAR in ("E1", "E2") else OE1_K2["max"]
    return f
def oe1_dec(i, pp, Mh, foot, hk, z, TOT):
    q = _oe_parts(foot, "A_c2b_refit", pp, z); R2, rta, xe = q["R2"], pp["rta"], q["xe"]; re = xe * R2; dm = pp["dmpc"]; Mb = pp["Mb"]; lo, mid, hi = 1.42 * MPCE, 2.06 * MPCE, 3.0 * MPCE
    fr = RF(hk, i, SB(O_(P_(np.gradient(TOT, RM) / (4 * np.pi * RM ** 2)), dm)))[0]
    def piece(S_): rho = np.gradient(S_, RM) / (4 * np.pi * RM ** 2); return DAT[hk]["W"][i] * (A_(DS_(O_(P_(rho), dm))) / KG * fr)
    cut = lambda a, b: np.clip(Mh, float(np.interp(a, RM, Mh)), float(np.interp(max(a, b), RM, Mh))) - float(np.interp(a, RM, Mh)); r1 = min(R2, lo); e_ = min(re, rta); hi2 = max(hi, R2)
    M_ = lambda b: np.minimum(Mh, float(np.interp(b, RM, Mh)))   # cumulative source: cold up to b; a piece is the difference of two cumulative chains, so the pieces telescope to V and a negative piece is seen
    Lv = [("cold_inR200", r1), ("cold_R200_band", lo), ("cold_b6", mid), ("cold_b7", hi), ("cold_out_to_edge", max(e_, hi)), ("cold_tail", max(rta, e_, hi))]; last = piece(Mb); P_V = dict(baryons=last.copy())
    for k_, b_ in Lv: cur = piece(Mb + M_(b_)); P_V[k_] = cur - last; last = cur
    P_V["cold_beyond"] = piece(TOT) - last
    V_ = {k: v[[6, 7]].tolist() for k, v in P_V.items()}; me = float(np.interp(rta, RM, Mh)); j = int(np.searchsorted(RM, min(lo * 1.45, rta))); OE1_ROWS.append(dict(i=int(i), hk=hk, z=z, fs=q["fs"], M200=q["M2"] / MSUNE, R200=R2 / MPCE, rta=rta / MPCE, re=re / MPCE, rs=q["xs"] * R2 / MPCE, Mc_rta=me / MSUNE, Mc_sph=float(q["Mc"](q["xs"] * R2)) / MSUNE, Mfair=pp["Mfair"] / MSUNE, Mc_R200=float(q["Mc"](R2)) / MSUNE, Mb_rta=float(Mb[-1]) / MSUNE, Mb_R200=float(np.interp(R2, RM, Mb)) / MSUNE, pieces=V_, V=piece(TOT)[[6, 7]].tolist()))
