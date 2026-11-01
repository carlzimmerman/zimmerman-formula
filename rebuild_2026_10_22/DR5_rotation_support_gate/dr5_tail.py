# DR5 tail: gated contraction on SPARC and LITTLE THINGS only. Appended to UR1's helper section, read only.
_SIG = dict(mode="f0", swap=False); _CURV = [None]; _CTR0 = contract
def _f_gate(V):
    m = _SIG["mode"]
    if m == "f0": f = 0.0
    elif m == "f1": f = 1.0
    else:
        s2 = (V / 3.0) ** 2 if m == "RATIO3" else float(m) ** 2; S = V ** 2 / (V ** 2 + 3 * s2); f = 1.0 - S
        if _SIG["swap"]: f = S
    return f
def _vgal(q):
    t = _TB.get(q["name"]); return t["vf"] if t and t["vf"] > 0 else float(np.nanmax(q["Vobs"]))
def contract(r, Mb, M0, F, gnedin=None):
    fr = sys._getframe(1).f_locals; q_ = fr.get("q"); V = _vgal(q_) if isinstance(q_, dict) and "Vobs" in q_ else _CURV[0]; Mf, c_, x_ = _CTR0(r, Mb, M0, F, gnedin=gnedin); return M0 + _f_gate(V) * (Mf - M0), c_, x_
def _lt2(tag, f="canonical"):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); E = []
    for r_ in _C["lt"]:
        _CURV[0] = r_["V"]; M2, R2 = _SL3M(r_["logMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); R_ = r_["R"] * MPCE / 1e3; Mb = 10 ** r_["logMb"] * MSUNE; rg = np.geomspace(R_ * 1e-3, R2, 600); M0g = math.pi * s * r0 ** 2 * B(rg / r0); Mbg = Mb * np.minimum(rg / R_, 1.0) ** 2; Mc = float(np.interp(math.log(R_), np.log(rg), contract(rg, Mbg, M0g, Mb / (M2 * MSUNE))[0])); E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(GE * Mb / R_ ** 2 + GE * Mc / R_ ** 2))
    return float(np.median(E))
def _run2(mode, swap=False):
    global CN1_MODE
    SLMAP["m"] = "EM1"; SLMAP["mut"] = 1.0; CN1_MODE = "blum"; _SIG.update(mode=mode, swap=swap); GHSTORE.clear(); r = dict(mode=mode, swap=swap, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in U]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in U]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], line=bool(st["rms"] <= 0.110 and 0.5 <= st["U_median"] <= 0.8), tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN})
    r["lt"] = {t: _lt2(t) for t in _TG}; r["f_by_bin"] = {f"{l}-{h}": _f_gate(math.sqrt(l * h)) for l, h in _BIN}; print("DR5", mode, swap, flush=True); return r
def _W(rg, Mb, Mc):
    dM = np.diff(Mc); rm = 0.5 * (rg[1:] + rg[:-1]); return -GE * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
def _energy(tag="A_c2b_refit", f="canonical"):
    _SIG.update(mode="f1", swap=False); bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); iu = int(np.argmin(abs(UPS - 0.5))); RD = {}
    for _l in open(_MRT):
        _p = _l.split()
        if len(_p) >= 18:
            try: RD[_p[0]] = float(_p[11]) * 3.0857e19
            except ValueError: pass
    O = {f"{l}-{h}": [] for l, h in _BIN}
    for q in GALS:
        t = _TB.get(q["name"]); rd = RD.get(q["name"], 0.0)
        if not t or t["vf"] <= 0 or t["Q"] > 2 or t["inc"] < 30 or rd <= 0: continue
        M2, R2 = _SL3M(q["lMb"], bg, rc); s, _ = sig_core(f, tag, M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R2, 400); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
        Mbg = np.maximum.accumulate(Mbg); Mf = _CTR0(rg, Mbg, M0, Mt / (M2 * MSUNE))[0]; V = t["vf"] * 1e3; Trot = 0.5 * Mt * V ** 2; Eun = max(0.0, (_W(rg, Mbg, M0) - _W(rg, Mbg, Mf)) / 2); Eb = abs(_W(rg, Mbg, M0)) / 2; m5 = rg <= 5 * rd; dM = np.diff(M0[m5]); rm = 0.5 * (rg[m5][1:] + rg[m5][:-1]); Ein = GE * float(np.sum(0.5 * (Mbg[m5][1:] + Mbg[m5][:-1] + M0[m5][1:] + M0[m5][:-1]) * dM / rm)); Mc5 = float(np.interp(5 * rd, rg, M0)); Mb5 = float(np.interp(5 * rd, rg, Mbg)); vL = 2 * Mt * rd * V / (2.0 / 3.0 * Mc5 * 5 * rd); Om = V / (5 * rd)
        for l, h in _BIN:
            if l <= t["vf"] < h: O[f"{l}-{h}"].append(dict(McMb=M2 * MSUNE / Mt, Mc5Mb5=Mc5 / Mb5, Trot_J=Trot, Trot_Eundo=Trot / Eun if Eun > 0 else float("inf"), Trot_Ebind=Trot / Eb, Trot_Ein=Trot / Ein, cent=(vL / V) ** 2, Om=Om, m_eV_phi1=1.0546e-34 * Om / V ** 2 * (2.998e8) ** 2 / 1.602e-19, phi_v_floor=Om * 1.0546e-34 / (2e-19 * 1.602e-19 / (2.998e8) ** 2 * V ** 2)))
    return {k: dict(n=len(v), **{a: float(np.median([x[a] for x in v])) for a in v[0]}) for k, v in O.items() if v}
if os.environ.get("DR5_K1B"):
    _gs = np.geomspace; np.geomspace = lambda a, b, n: _gs(a, b, int(os.environ["DR5_K1B"]) if n == 300 else n); _r = {m: _run2(m) for m in os.environ["DR5_MODES"].split(",")}; json.dump(_r, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); sys.exit(0)
_R = dict(runs={m: _run2(m) for m in ("f0", "f1", "10", "RATIO3", "30")}); _R["MUTATE"] = _run2("10", swap=True); _SIG.update(mode="RATIO3", swap=False); _R["K3"] = abs(_f_gate(47.0) - 0.25); _R["energy"] = _energy()
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("DR5 done", flush=True); sys.exit(0)
