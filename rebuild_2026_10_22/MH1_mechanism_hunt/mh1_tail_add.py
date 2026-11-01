# MH1 tail, after UR1's helpers. Reads only. Rows are dumped one by one, so a killed run resumes.
import time as _tm
_T0 = _tm.time(); SLDL[0] = 0.0; _OUTF = os.environ["SL1_OUT"]; _PART = "MUTATE" if "MUTATE" in _OUTF else "RUN"; _ORIG = contract; _KPC = 3.0857e19; _KB = 1.380649e-23; _MP = 1.6726e-27
_R = json.load(open(_OUTF)) if os.path.exists(_OUTF) else dict(rows={}, clusters={}, gal={})
_MR = {}
for _l in open(_MRT):
    _p = _l.split()
    if len(_p) < 18: continue
    try: _MR[_p[0]] = dict(Rd=float(_p[11]), RHI=float(_p[14]), SBd=float(_p[12]))
    except ValueError: pass
_BUL = {}
for q in GALS:
    _f = os.path.join(REB, "..", "real_research", "data", "sparc_data", q["name"] + "_rotmod.dat"); _a = [[float(x) for x in l.split()] for l in open(_f) if l.strip() and not l.startswith("#")]; _a = np.array(_a); _BUL[q["name"]] = float(np.max(_a[:, 5] ** 2 * _a[:, 0] * 1e6 * _KPC / GE)) if np.any(_a[:, 5] > 0) else 0.0  # at Upsilon 1: V^2 r / G, kg
_CFG = dict(F_c=0.0, vdi=None, cs=math.sqrt(_KB * 1e4 / (1.22 * _MP)), invert=False)
_CS0 = _CFG["cs"]; assert abs(_CS0 - 8.2e3) < 200
def _W(r, Mb, Mc): dM = np.diff(Mc); rm = 0.5 * (r[1:] + r[:-1]); return -GE * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
def _sigcrit(M, Rd, r, M0):
    R = 2 * Rd; Sig = M * math.exp(-2) / (2 * math.pi * Rd ** 2); M0R = float(np.interp(math.log(R), np.log(r), M0)); V = math.sqrt(GE * (0.594 * M + M0R) / R); kap = math.sqrt(2) * V / R; return math.pi * GE * Sig / kap, V, Sig, kap, R, M0R
_BYR0 = {}
for q in GALS: _BYR0.setdefault(round(math.log(q["Rm"][0] * 0.05), 9), []).append(q)
def _which(r):
    c = _BYR0.get(round(math.log(r[0]), 9))
    if not c: return None
    if len(c) == 1: return c[0]
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); return min(c, key=lambda q: abs(math.log(_SL3M(q["lMb"], bg, rc)[1] / r[-1])))
def contract(r, Mb, M0, F, gnedin=None):
    Fu = max(F, _CFG["F_c"]) if _CFG["F_c"] > 0 else F; o = _ORIG(r, Mb, M0, Fu, gnedin=gnedin)
    if _CFG["vdi"] is None or CN1_MODE == "off": return o
    n = len(r); Mc = o[0]
    if n in (300, 400):
        q = _which(r); assert q is not None; t = _MR.get(q["name"])
        if not t or t["Rd"] <= 0: return o
        M = (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE; Rd = t["Rd"] * _KPC
    elif n == 600: M = float(Mb[-1]); Rd = (r[0] * 1e3) / 2.2; q = None
    else: return o
    sc, V, Sig, kap, R, M0R = _sigcrit(M, Rd, r, M0); sel = sc > _CFG["cs"]; sel = (not sel) if _CFG["invert"] else sel
    if q is not None and _CFG.get("rec") is not None and q["name"] not in _CFG["rec"]:
        lam = 4 * math.pi ** 2 * GE * Sig / kap ** 2; MT = min(math.pi * Sig * (lam / 2) ** 2, M); dM = np.gradient(M0, r); rho = float(np.interp(math.log(R), np.log(r), dM / (4 * math.pi * r ** 2))); lnL = math.log(1 + (0.594 * M + M0R) / MT); Ecold = M * 4 * math.pi * GE ** 2 * MT * rho * lnL * 0.428 / V * (300e6 * 3.15576e7); Eu = (_W(r, Mb, M0) - _W(r, Mb, Mc)) / 2; _CFG["rec"][q["name"]] = dict(sc=sc / 1e3, sel=bool(sel), D=Ecold / max(Eu, 1e-300), MT_over_M=MT / M, Bfrac=_BUL[q["name"]] * 0.5 / M, Eu=Eu)
    if not sel: return o
    if _CFG["vdi"] == "zero": return (np.maximum.accumulate(M0.copy()),) + tuple(o[1:])
    if q is None: return o
    U = float(np.clip((Mb[-1] / MSUNE / 1e9 - 1.33 * q["meta"]["MHI"]) / max(q["meta"]["L36"], 1e-9), 0.3, 1.2)); Ms = U * _BUL[q["name"]]
    if Ms <= 0: return o
    t_ = _MR[q["name"]]; Ri = t_["RHI"] * _KPC if t_["RHI"] > 0 else q["Rm"][-1]; Ri = min(Ri, r[-1]); rf_ = r[0] / 0.05; mk = (r >= rf_) & (r <= Ri); MT_ = Mb + Mc
    if mk.sum() < 2: return o
    wav = Ms * (GE * float(np.trapz(MT_[mk] / r[mk], np.log(r[mk]))) + GE * float(np.interp(math.log(Ri), np.log(r), MT_)) / Ri / 2); W1 = _W(r, Mb, Mc)
    def E(f): return (_W(r, Mb, M0 + f * (Mc - M0)) - W1) / 2
    if E(0.0) <= wav: return (np.maximum.accumulate(M0.copy()),) + tuple(o[1:])
    lo, hi = 0.0, 1.0
    for _ in range(14):
        m = 0.5 * (lo + hi)
        if E(m) > wav: lo = m
        else: hi = m
    f = 0.5 * (lo + hi); return (np.maximum.accumulate(M0 + f * (Mc - M0)),) + tuple(o[1:])
def _cell(name, d=0.0, mode="blum", clu=False, **kw):
    global CN1_MODE
    if name in _R["rows"] and (not clu or name in _R["clusters"]): return _R["rows"][name]
    _CFG.update(F_c=0.0, vdi=None, cs=_CS0, invert=False, rec=None); _CFG.update(kw); SLMAP["m"] = "EM1"; SLDL[0] = d; CN1_MODE = mode; GHSTORE.clear(); r = dict(delta=d, sparc={}); f = "canonical"
    for t in _TG:
        st = sparc(f, t); U = _gals_U(t); nm = list(U); v = np.array([_TB[n]["vf"] if n in _TB else np.nan for n in nm]); Q = np.array([(_TB[n]["Q"] <= 2 and _TB[n]["inc"] >= 30) if n in _TB else False for n in nm]); u = np.array(list(U.values())); lo = Q & (v > 0) & (v < 100); hi = Q & (v > 150); r["sparc"][t] = dict(U=st["U_median"], rms=st["rms"], tilt=float(np.median(u[lo]) - np.median(u[hi])), bins={f"{l}-{h}": float(np.median(u[Q & (v >= l) & (v < h)])) for l, h in _BIN}, per=U if t == _TG[0] else None)
    r["groups"] = _groups(); r["lt"] = {t: _lt(t) for t in _TG}; _R["rows"][name] = r
    if clu: GHSTORE.clear(); PREP.clear(); gc = grade_clusters("canonical"); k = _keys(gc, "canonical"); PREP.clear(); _R["clusters"][name] = dict(n=k["n"], bad=k["bad"], Z=k["Z"], xcop=_xcop())
    if _CFG.get("rec") is not None: _R["gal"][name] = _CFG["rec"]
    _dump(); s = r["sparc"][_TG[0]]; print(f"MH1 {name} U {s['U']:.3f} rms {s['rms']:.4f} tilt {s['tilt']:+.2f} LT {r['lt'][_TG[0]]:+.3f} Z {r['groups']['Z']:+.2f} bins {[round(x, 2) for x in s['bins'].values()]} {_tm.time() - _T0:.0f} s", flush=True); return r
def _dump(): _t = _OUTF + ".tmp"; json.dump(_R, open(_t, "w"), indent=1, default=float); os.replace(_t, _OUTF)
_RN = NAT_RRAT; print("MH1 R_nat", _RN, "c_s", _CS0, flush=True)
if _PART == "MUTATE":
    _cell("MUT_MB_x2", F_c=2 / _RN); _cell("MUT_VDI_invert", vdi="zero", invert=True)
    print("MH1 done", flush=True); sys.exit(0)
_cell("off", mode="off", clu=True); _cell("blum", clu=True); _cell("K2_none", vdi="zero", cs=1e12); _cell("MB", F_c=1 / _RN, clu=True); _cell("VDI0", vdi="zero", rec={}, clu=True); _cell("VDIE", vdi="energy"); _cell("VDI0+MB", vdi="zero", F_c=1 / _RN); _cell("VDI0_cs11.7", vdi="zero", cs=_CS0 * math.sqrt(1.22 / 0.6)); _cell("VDI0_d+0.05_FITTED", d=0.05, vdi="zero")
# K4 and the MB prediction: exponential disc in EM1's halo, inner cold mass with and without the budget
_bg = BGS["A_c2b_refit"]; _rc = 3 * (100 * _bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); _P = {}
SLMAP["m"] = "EM1"; SLDL[0] = 0.0; CN1_MODE = "blum"; _CFG.update(F_c=0.0, vdi=None)
for _nm, _lMb, _Rd in (("MW", 10.827, 3.565), ("1e10", 8.69, 1.0)):
    M2, R2 = _SL3M(_lMb, _bg, _rc); s, _ = sig_core("canonical", "A_c2b_refit", M2 / FC1_MC); r0 = solve_r0(M2 * MSUNE, R2, s); rg = np.geomspace(R2 * 1e-4, R2, 800); M0 = math.pi * s * r0 ** 2 * B(rg / r0); Mb = 10 ** _lMb * MSUNE * (1 - (1 + rg / (_Rd * _KPC)) * np.exp(-rg / (_Rd * _KPC))); Fo = float(Mb[-1] / M0[-1]); A = _ORIG(rg, Mb, M0, Fo)[0]; C = _ORIG(rg, Mb, M0, 1 / _RN)[0]; R8 = (8 if _nm == "MW" else 2) * _KPC; _i = lambda a: float(np.interp(math.log(R8), np.log(rg), a)); _P[_nm] = dict(M200=M2, F_obs=Fo, F_c=1 / _RN, M0=_i(M0) / MSUNE, blum=_i(A) / MSUNE, MB=_i(C) / MSUNE, r_kpc=R8 / _KPC); _e = [(_W(rg, Mb, M0 + f_ * (A - M0)) - _W(rg, Mb, A)) / 2 for f_ in (1, .75, .5, .25, 0)]; _P[_nm]["K4"] = [abs(_e[0]), bool(np.all(np.diff(_e) >= 0))]
_R["pred"] = _P; _dump(); print("MH1 pred", _P, flush=True); print("MH1 done", flush=True); sys.exit(0)
