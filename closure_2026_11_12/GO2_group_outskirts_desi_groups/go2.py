"""GO2 step 2 (FROZEN_CRITERIA.md df55a3237c): stack the isolated DESI groups' shear and y (go2_measure.py checkpoint), deproject with
GO1's A1 method, build the census (gas inside R500 from y), find r_ta (delta 5.55 rho_m), grade f_ret(<r_ta) per footing.
Known answers, nulls, brackets and mutations as frozen. GO1's go1.py copied for the kernels, deprojection and census.
python3 -I go2.py <go2 checkpoint.npz> <GO1 checkpoint.npz>. Writes go2.out, go2.json, go2_MUTATE.out.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity")); import CFG4_common as C4
nu_mono, A0 = C4.nu_mono, C4.A0
assert abs(A0["canonical"] - 9.3603e-11) < 1e-14 and abs(A0["alt"] - 1.1312e-10) < 1e-14, A0
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG_PER_MSUN_PC2 = MSUN/(3.0857e16)**2; M_BIAS = -0.01
SIGT = 6.6524587e-29; MP = 1.6726e-27; MUE = 1.14
YCONST = MUE*MP*511.0*MPC**2/SIGT/MSUN
OMB = 0.0224; RHOB0 = OMB*2.775e11
R_B = 5.41; DTA = 5.55; GASFRAC_BR = 0.0536
EDGES = np.geomspace(0.25, 16.0, 13); NB = 12; YEDGES = np.r_[0.0, EDGES]; NY = 13
OUT, MOUT = [], []
def P(s="", m=False): print(s, flush=True); (MOUT if m else OUT).append(str(s))
# ---------------------------------------------------------------- kernels (GO1 verbatim)
def shell_SM(R, a, b):
    s = lambda q: np.sqrt(np.clip(q*q - R*R, 0, None))
    Sig = 2*(s(b) - s(a)); Mc = 4*np.pi/3*((b**3 - s(b)**3) - (a**3 - s(a)**3)); return Sig, Mc
def dsig_shell(R, a, b): Sig, Mc = shell_SM(R, a, b); return Mc/(np.pi*R*R) - Sig
def bin_avg(f, lo, hi, n=400):
    u = (np.arange(n) + 0.5)/n; R = np.sqrt(lo*lo + u*(hi*hi - lo*lo)); return f(R).mean()
TAILX = np.geomspace(16.0, 64.0, 401)
def lens_K(tail):
    sh = [(EDGES[j], EDGES[j + 1]) for j in range(NB)]
    K = np.array([[bin_avg(lambda R: dsig_shell(R, a, b), EDGES[i], EDGES[i + 1]) for (a, b) in sh] for i in range(NB)])
    if tail is not None:
        tk = np.zeros(NB)
        for a, b in zip(TAILX[:-1], TAILX[1:]):
            amp = (np.sqrt(a*b)/16.0)**tail; tk += amp*np.array([bin_avg(lambda R: dsig_shell(R, a, b), EDGES[i], EDGES[i + 1], 100) for i in range(NB)])
        K[:, -1] += tk
    Kp = np.array([bin_avg(lambda R: 1/(np.pi*R*R), EDGES[i], EDGES[i + 1]) for i in range(NB)])
    V = np.r_[1.0, [4*np.pi/3*(b**3 - a**3) for a, b in sh]]; return np.c_[Kp, K], V
XM = np.sqrt(EDGES[1:]*EDGES[:-1]); D2 = np.zeros((NB - 2, NB + 1))
for k_ in range(NB - 2): D2[k_, 1 + k_], D2[k_, 2 + k_], D2[k_, 3 + k_] = XM[k_]**2, -2*XM[k_ + 1]**2, XM[k_ + 2]**2
LAMN = 2.5e-5
def deproj(S, sig, tail=-2.0, lam=LAMN):
    K, V = KL[tail]; sref = np.median(sig); A_ = np.r_[K/sig[:, None], math.sqrt(lam)/sref*D2]; b_ = np.r_[S/sig, np.zeros(NB - 2)]
    r = np.linalg.lstsq(A_, b_, rcond=None)[0]; return np.r_[r[0], r[0] + np.cumsum(r[1:]*V[1:])]
def onion_A(tail):
    def Vc(Rc, r): return 4/3*math.pi*(r**3 - max(r*r - Rc*Rc, 0)**1.5) if r > 0 else 0.0
    def VI(R1_, R2_, r1, r2): return Vc(R2_, r2) - Vc(R1_, r2) - Vc(R2_, r1) + Vc(R1_, r1)
    E = YEDGES; A = np.array([[VI(E[i], E[i + 1], E[j], E[j + 1])/(math.pi*(E[i + 1]**2 - E[i]**2)) for j in range(NY)] for i in range(NY)])
    if tail is not None:
        for a, b in zip(TAILX[:-1], TAILX[1:]):
            amp = (math.sqrt(a*b)/16.0)**tail; A[:, -1] += amp*np.array([VI(E[i], E[i + 1], a, b)/(math.pi*(E[i + 1]**2 - E[i]**2)) for i in range(NY)])
    V = np.array([4*math.pi/3*(E[j + 1]**3 - E[j]**3) for j in range(NY)]); return A, V
KL = {t: lens_K(t) for t in (-2.0, -1.5, -3.0, None)}; AY = {t: onion_A(t) for t in (None, -3.0)}
IDX1 = 4; assert abs(EDGES[IDX1] - 1) < 1e-12; IY1 = 5; assert abs(YEDGES[IY1] - 1) < 1e-12
TAU = np.ones(NY)
for j in range(IY1, NY):
    xx = np.linspace(YEDGES[j], YEDGES[j + 1], 400); TAU[j] = 1/np.average(xx**0.6, weights=xx**2)
MAPS = ("ComptonY", "ComptonY_deproj_cib_1.0_10.7")
def dsig(s, key="numt"): return s[key]/np.where(s["den"] > 0, s["den"], np.inf)/KG_PER_MSUN_PC2/(1 + M_BIAS)
# ---------------------------------------------------------------- a data set (GO1 build, generalised)
def build(KEEP, gasmode):
    D = dict(n=len(KEEP), gasmode=gasmode, KEEP=KEEP)
    z = np.array([r["z"] for r in KEEP]); R5 = np.array([r["R500"] for r in KEEP]); M5 = np.array([r["M500"] for r in KEEP])
    D.update(z=z, R5=R5, M5=M5, MG=np.array([r.get("Mgas500", np.nan) for r in KEEP]))
    D["DT"] = np.array([dsig(r["shear"]) for r in KEEP]); D["DX"] = np.array([dsig(r["shear"], "numx") for r in KEEP])
    D["RT"] = [np.array([dsig(q["shear"]) for q in r["rnd"]]) for r in KEEP]; D["RX"] = [np.array([dsig(q["shear"], "numx") for q in r["rnd"]]) for r in KEEP]
    var15 = np.array([r["shear"]["var15"]/r["shear"]["den15"]**2/KG_PER_MSUN_PC2**2/(1 + M_BIAS)**2 for r in KEEP])
    W = 1/(var15*R5**4); D["W"] = W/W.sum(); D["SC"] = 1e12*R5**2
    D["YG"] = {m: np.array([r["y"][m] for r in KEEP]) for m in MAPS}; D["YR"] = {m: [np.array([q["y"][m] for q in r["rnd"]]) for r in KEEP] for m in MAPS}
    D["YS"] = np.array([r["yshift"]["ComptonY"] if r["yshift"] is not None else np.full(NY, np.nan) for r in KEEP])
    D["TPL"] = {k: np.array([r["y"][k] for r in KEEP]) for k in ("tr_gnfw", "tb_gnfw", "tr_beta", "tb_beta")}
    patch = np.empty(len(KEEP), int); patch[np.argsort([r["ra"] for r in KEEP])] = np.arange(len(KEEP))*30//len(KEEP); D["patch"] = patch
    DREAL = D["DT"] - np.array([r_.mean(0) for r_ in D["RT"]])
    def _S(sel): w_ = D["W"][sel]/D["W"][sel].sum(); return (w_[:, None]*DREAL[sel]*D["SC"][sel][:, None]).sum(0)
    reps = np.array([_S(patch != j) for j in range(30)]); D["SIGL"] = np.sqrt(29/30*((reps - reps.mean(0))**2).sum(0)); D["S_full"] = _S(np.ones(len(KEEP), bool))
    return D
def census(D, sel, R=R_B, ltail=-2.0, ytail=None, mapk="ComptonY", beam=True, mg_f=1.0, star_out=1.0, star_all=1.0, dta=DTA,
           lens="real", ysrc="real", tau_mode="primary", lam=LAMN, gas5mode=None, m5f=1.0):
    z, R5 = D["z"][sel], D["R5"][sel]; M5 = D["M5"][sel]*m5f; ii = np.where(sel)[0]
    Ez = np.sqrt(0.3*(1 + z)**3 + 0.7); T5 = 8.71*(M5/1e15)**(2/3)*Ez**(2/3); MST = 1.7e12*(M5/1e14)**0.6; CY = R5**2/T5
    w = D["W"][sel]/D["W"][sel].sum(); RT, RX, YR = D["RT"], D["RX"], D["YR"]
    if lens == "real": d = D["DT"][sel] - np.array([RT[i].mean(0) for i in ii])
    elif lens == "cross": d = D["DX"][sel] - np.array([RX[i].mean(0) for i in ii])
    elif lens == "flip": d = -(D["DT"][sel] - np.array([RT[i].mean(0) for i in ii]))
    elif lens == "rr": d = np.array([RT[i][0::2].mean(0) - RT[i][1::2].mean(0) for i in ii])
    S = (w[:, None]*d*D["SC"][sel][:, None]).sum(0); Mexc = deproj(S, D["SIGL"], ltail, lam)
    if ysrc == "real": yv = D["YG"][mapk][sel] - np.array([YR[mapk][i].mean(0) for i in ii])
    elif ysrc == "rr": yv = np.array([YR[mapk][i][0::2].mean(0) - YR[mapk][i][1::2].mean(0) for i in ii])
    elif ysrc == "shift":
        okk = np.isfinite(D["YS"][ii]).all(1); yv = D["YS"][ii] - np.array([YR[mapk][i].mean(0) for i in ii]); yv[~okk] = 0.0
    q = (w[:, None]*yv*CY[:, None]).sum(0); A, VY = AY[ytail]; p = np.linalg.solve(A, q)
    if beam:
        tr = (w[:, None]*D["TPL"]["tr_gnfw"][sel]*CY[:, None]).sum(0); tb = (w[:, None]*D["TPL"]["tb_gnfw"][sel]*CY[:, None]).sum(0)
        p = p*np.linalg.solve(A, tr)/np.linalg.solve(A, tb)
    tau = TAU if tau_mode == "primary" else np.ones(NY)
    gy_sh = YCONST*p*VY/tau; Gy = np.r_[0, np.cumsum(np.where(np.arange(NY) >= IY1, gy_sh, 0.0))]
    gas5y = float(gy_sh[:IY1].sum())                                                   # T = T500 inside R500 (TAU = 1 there)
    gm = gas5mode or D["gasmode"]
    gas5 = mg_f*(gas5y if gm == "y" else (w*D["MG"][sel]).sum() if gm == "catalogue" else GASFRAC_BR*(w*M5).sum())
    Vb = lambda x: (w*RHOB0*(1 + z)**3*4*np.pi/3*(x*R5)**3).sum()
    st5 = star_all*(w*MST).sum(); sbar = st5/(w*M5).sum()
    X = EDGES[IDX1:]; rows = []
    for k, x in enumerate(X):
        ke = IDX1 + k; me = Mexc[ke]; gy = Gy[IY1 + k] if k > 0 else 0.0
        mb = gas5 + gy + st5 + star_out*sbar*(me - Mexc[IDX1]) + Vb(x) - Vb(1.0); vb = Vb(x)
        mt = me + (1 + R)*vb; rows.append(dict(x=float(x), Mexc=me, Gy=gy, Mb=mb, Mtot=mt, Vb=vb, delta=mt/((1 + R)*vb), f=R*mb/(mt - mb),
                                             fexc=R*(mb - vb)/(me - (mb - vb))))
    dl = np.array([r_["delta"] for r_ in rows]); xta = None; fta = None; extra = {}
    if dl[-1] < dta and dl.max() >= dta:
        k = max(i for i in range(len(rows) - 1) if dl[i] >= dta and dl[i + 1] < dta)
        t = ((math.log(dl[k]) - math.log(dta))/(math.log(dl[k]) - math.log(dl[k + 1]))) if dl[k + 1] > 0 else (dl[k] - dta)/(dl[k] - dl[k + 1]); xta = math.exp(math.log(X[k]) + t*math.log(X[k + 1]/X[k]))
        def il(key):
            a_, b_ = rows[k][key], rows[k + 1][key]
            return math.exp(math.log(a_) + t*(math.log(b_) - math.log(a_))) if a_ > 0 and b_ > 0 else a_ + t*(b_ - a_)
        mb, mt, vb = il("Mb"), il("Mtot"), il("Vb"); gy = il("Gy") if rows[k]["Gy"] > 0 else rows[k]["Gy"] + t*(rows[k + 1]["Gy"] - rows[k]["Gy"])
        fta = R*mb/(mt - mb); need = mt/(1 + R) - (mb - gy)
        extra = dict(Mb=mb, Mtot=mt, Vb=vb, Gy=gy, need_gy=need, fexc=R*(mb - vb)/(mt - (1 + R)*vb - (mb - vb)))
    def at(x, key):
        lx = np.log(X); return float(np.interp(math.log(x), lx, [r_[key] for r_ in rows]))
    A_ = {x: {k_: at(x, k_) for k_ in ("f", "Mexc", "Gy", "Mb", "Mtot", "fexc", "delta")} for x in (1.0, 2.0, 3.0, 5.0, 8.0, 11.3137, 16.0)}
    for x in A_: A_[x]["gas5"] = gas5
    return dict(rows=rows, xta=xta, fta=fta, ta=extra, at=A_, gas5=gas5, gas5y=gas5y, st5=st5, sbar=sbar, p=p, T5=float((w*T5).sum()))
def jsig(vals):
    v = np.array([x for x in vals if x is not None and np.isfinite(x)], float); return float(np.sqrt((len(v) - 1)/len(v)*np.sum((v - v.mean())**2))) if len(v) > 2 else float("nan")
XK = (1.0, 2.0, 3.0, 5.0, 8.0, 11.3137, 16.0); KK = ("f", "Mexc", "Gy", "Mb", "Mtot", "fexc", "delta", "gas5")
def summary(D, fun):
    ALL = np.ones(D["n"], bool); full = fun(D, ALL); reps = [fun(D, D["patch"] != j) for j in range(30)]
    s = dict(full=full, n_reach=sum(r["xta"] is not None for r in reps), sig_f=jsig([r["fta"] for r in reps]), sig_x=jsig([r["xta"] for r in reps]))
    s["sig_at"] = {x: {k: jsig([r["at"][x][k] for r in reps]) for k in KK} for x in XK}
    s["sig_rows"] = [{k: jsig([r["rows"][i][k] for r in reps]) for k in ("Mexc", "Gy", "Mb", "f", "delta")} for i in range(len(full["rows"]))]
    return s
def label(prim, lo, nkeep):
    if nkeep < 150: return "NOT EVALUABLE [too few groups]"
    if prim["full"]["xta"] is None: return "NOT EVALUABLE [r_ta NOT REACHED]"
    if prim["n_reach"] < 27: return f"NOT EVALUABLE [r_ta reached in {prim['n_reach']} of 30 jackknife]"
    if not (prim["sig_f"] <= 0.20): return f"NOT EVALUABLE [sigma f_ret {prim['sig_f']:.2f} > 0.20]"
    f, s = prim["full"]["fta"], prim["sig_f"]
    if f + 2*s < 1: return "CENSUS FALLS SHORT"
    fl, sl = lo["full"]["fta"], lo["sig_f"]
    return "CENSUS REACHES THE FULL SHARE" + (" [OVERSHOOT]" if fl is not None and fl - 2*sl > 1 else "")
# ---------------------------------------------------------------- data
CK = dict(np.load(sys.argv[1], allow_pickle=True))["res"].item(); REC = [CK[i] for i in sorted(CK)]
cnt = {s_: dict(total=sum(r["sample"] == s_ for r in REC), kept=sum(r["keep"] and r["sample"] == s_ for r in REC),
                drop={w: sum(r["why"] == w and r["sample"] == s_ for r in REC) for w in ('sources', 'empty bin', 'y mask', 'randoms')}) for s_ in ("iso", "ctl")}
P(f"GO2. isolated groups measured {cnt['iso']['total']}, kept {cnt['iso']['kept']}, dropped {cnt['iso']['drop']}; M1 control measured {cnt['ctl']['total']}, kept {cnt['ctl']['kept']}")
DI = build([r for r in REC if r["keep"] and r["sample"] == "iso"], "y"); DC = build([r for r in REC if r["keep"] and r["sample"] == "ctl"], "y")
z = DI["z"]; W = DI["W"]
P(f"isolated: median z {np.median(z):.3f}; weighted mean M_HALO {np.sum(W*[r['M_HALO'] for r in DI['KEEP']]):.3e} (Msun/h), M500 {np.sum(W*DI['M5']):.3e}, R500 {np.sum(W*DI['R5']):.3f} Mpc; "
  f"median theta500 {np.median([r['th500'] for r in DI['KEEP']]):.2f}'; randoms per group {np.mean([len(r['rnd']) for r in DI['KEEP']]):.2f}; "
  f"weighted mean visible member stellar mass {np.sum(W*[r['Mstar_members'] for r in DI['KEEP']]):.3e} (catalogue units)")
S_ = DI["S_full"]; P("stacked Delta Sigma x R500^2 per bin (Msun per unit x^2), S/N per bin: " + ", ".join(f"{a:.2e}({a/b:+.1f})" for a, b in zip(S_, DI["SIGL"])) + f"; total S/N {math.sqrt(np.sum((S_/DI['SIGL'])**2)):.1f}")
# ---------------------------------------------------------------- known answers
P("\n## Known answers")
KAOK = {}
ka1a = open(os.path.join(HERE, "go2_ka1a.out")).read().strip(); P(ka1a); KAOK["KA1a"] = ka1a.endswith("PASS")
CK1 = dict(np.load(sys.argv[2], allow_pickle=True))["res"].item(); D1 = build([CK1[i] for i in sorted(CK1) if CK1[i]["keep"]], "catalogue")
g1 = json.load(open(os.path.join(REPO, "closure_2026_11_10", "GO1_group_outskirts", "go1.json")))["primary"]["full"]["rows"]
c1 = census(D1, np.ones(D1["n"], bool)); worst = 0.0
for i in (0, 3, 6, 7, 8):
    for k in ("delta", "Mexc"): worst = max(worst, abs(c1["rows"][i][k]/g1[i][k] - 1))
KAOK["KA1b"] = worst < 1e-6; P(f"KA1b GO2 stacker on GO1's checkpoint (catalogue Mgas500) vs go1.json delta, M_exc at x 1, 4, 8, 11.3, 16: max rel diff {worst:.1e} -> {'PASS' if KAOK['KA1b'] else 'FAIL'}")
P(f"     (GO1 reproduced: delta at x 8 / 11.3 / 16 = {c1['rows'][6]['delta']:.2f} / {c1['rows'][7]['delta']:.2f} / {c1['rows'][8]['delta']:.2f})")
def KA2m(D):
    rs = 0.25; rho_n = lambda x: 1/((x/rs)*(1 + x/rs)**2); A2 = rho_n(2.0)*4.0
    rho = lambda x: np.where(x <= 64, rho_n(x) + np.where(x > 2, A2*x**-2.0, 0.0), 0.0)
    l = np.geomspace(1e-6, 64, 8000); Rf = np.geomspace(1e-5, 16.5, 4000)
    Sig = np.array([2*np.trapz(rho(np.sqrt(R*R + l*l)), l) for R in Rf]); Mc = np.r_[0, np.cumsum(0.5*(Sig[1:]*Rf[1:] + Sig[:-1]*Rf[:-1])*np.diff(Rf))]*2*np.pi
    DS = lambda R: np.interp(R, Rf, Mc)/(np.pi*R*R) - np.interp(R, Rf, Sig)
    d = np.array([bin_avg(DS, EDGES[i], EDGES[i + 1]) for i in range(NB)]); sig = D["SIGL"]*np.abs(d[4]/D["S_full"][4])
    xs = np.geomspace(1e-6, 16, 40000); XT = (1.0, 2.83, 8.0); tr = np.array([np.trapz((4*np.pi*xs**2*rho(xs))[xs <= x], xs[xs <= x]) for x in XT])
    at = lambda Me: np.array([np.interp(math.log(x), np.log(EDGES), Me) for x in XT])
    got = at(deproj(d, D["SIGL"]))/tr; rg = np.random.default_rng(1112); mk = np.array([at(deproj(d + sig*rg.standard_normal(NB), D["SIGL"])) for _ in range(200)])
    bias = (mk.mean(0) - tr)/mk.std(0); return got, bias, mk.std(0)/tr
got, bias, rsd = KA2m(DI); KAOK["KA3 deproj"] = bool(np.all(np.abs(got - 1) < 0.05) and np.all(np.abs(bias) <= 0.3))
P(f"KA3 A1 deprojection NFW + r^-2: M_rec/M_true at x 1, 2.83, 8 {np.round(got, 4).tolist()} (5 %); mocks bias/sd {np.round(bias, 2).tolist()}, rel sd {np.round(rsd, 2).tolist()} -> {'PASS' if KAOK['KA3 deproj'] else 'FAIL'}")
w = W; Ez = np.sqrt(0.3*(1 + z)**3 + 0.7); T5 = 8.71*(DI["M5"]/1e15)**(2/3)*Ez**(2/3); CY = DI["R5"]**2/T5; A, VY = AY[None]
corr = np.linalg.solve(A, (w[:, None]*DI["TPL"]["tr_gnfw"]*CY[:, None]).sum(0))/np.linalg.solve(A, (w[:, None]*DI["TPL"]["tb_gnfw"]*CY[:, None]).sum(0))
pb = np.linalg.solve(A, (w[:, None]*DI["TPL"]["tb_beta"]*CY[:, None]).sum(0))*corr
xs = np.linspace(0, 16, 200001); bp = (1 + (xs/0.15)**2)**-1.5
truth = np.array([np.trapz((4*np.pi*xs**2*bp)[(xs >= YEDGES[j]) & (xs <= YEDGES[j + 1])], xs[(xs >= YEDGES[j]) & (xs <= YEDGES[j + 1])]) for j in range(NY)])*(w*CY).sum()
rk3 = (pb*VY/truth); KAOK["KA3 y"] = bool(np.all(np.abs(rk3[IY1:IY1 + 4] - 1) <= 0.10))
P(f"KA3 beta-model y template, gNFW beam-corrected, recovered/true per shell (inner sphere, 0.25 ... 16): {np.round(rk3, 3).tolist()}; graded shells 1-4 -> {'PASS' if KAOK['KA3 y'] else 'FAIL'}")
P(f"     gNFW beam correction per shell: {np.round(corr, 3).tolist()}")
idok = all(abs(R_B*RHOB0*4*np.pi/3*x**3/((1 + R_B)*RHOB0*4*np.pi/3*x**3 - RHOB0*4*np.pi/3*x**3) - 1) < 1e-12 for x in (1.0, 3.0, 8.0)); KAOK["KA3 identity"] = idok
P(f"KA3 f_ret identity with no excess: {'PASS' if idok else 'FAIL'}")
def zrow(S, keys): return {f"{k}@{x:g}": (S["full"]["at"][x][k], S["sig_at"][x][k], S["full"]["at"][x][k]/S["sig_at"][x][k]) for k, xs_ in keys for x in xs_}
N1 = summary(DI, lambda D, s: census(D, s, lens="cross")); z1 = zrow(N1, [("Mexc", (1.0, 3.0, 8.0))])
N2 = summary(DI, lambda D, s: census(D, s, lens="rr", ysrc="rr")); z2 = zrow(N2, [("Mexc", (3.0, 8.0, 16.0)), ("gas5", (1.0,)), ("Gy", (3.0, 8.0))])
KAOK["KA2 cross"] = all(abs(v[2]) < 3 for v in z1.values()); KAOK["KA2 random stack"] = all(abs(v[2]) < 3 for v in z2.values())
P("KA2 cross shear M_exc: " + "; ".join(f"{k} {v[0]:.2e} ± {v[1]:.2e} (z {v[2]:+.2f})" for k, v in z1.items()) + f" -> {'PASS' if KAOK['KA2 cross'] else 'FAIL'}")
P("KA2 random-position stack (random minus random): " + "; ".join(f"{k} {v[0]:.2e} ± {v[1]:.2e} (z {v[2]:+.2f})" for k, v in z2.items()) + f" -> {'PASS' if KAOK['KA2 random stack'] else 'FAIL'}")
# ---------------------------------------------------------------- primary
P("\n## Primary (isolated, z 0.05-0.30, R 5.41, delta_ta 5.55, lens tail x^-2, y truncated, beam-corrected, gas500 from y at T500, T = T500 x^-0.6 outside)")
PR = summary(DI, lambda D, s: census(D, s)); LO = summary(DI, lambda D, s: census(D, s, tau_mode="iso"))
fr = PR["full"]; P(f"gas500 (y, T500) {fr['gas5']:.3e} ± {PR['sig_at'][1.0]['gas5']:.2e}; gas500 bracket 0.0536 M500 = {GASFRAC_BR*np.sum(W*DI['M5']):.3e}; stars500 (KVM18) {fr['st5']:.3e}; weighted T500 {fr['T5']:.2f} keV")
P("| x | M_exc (lensing) | y gas 1..x (primary T) | M_b | M_tot | delta/rho_m | f_ret | f_ret_lo (isothermal) |"); P("|---|---|---|---|---|---|---|---|")
for i, r in enumerate(fr["rows"]):
    sr = PR["sig_rows"][i]; rl = LO["full"]["rows"][i]; sl = LO["sig_rows"][i]
    P(f"| {r['x']:.2f} | {r['Mexc']:.3e} ± {sr['Mexc']:.2e} | {r['Gy']:.3e} ± {sr['Gy']:.2e} | {r['Mb']:.3e} | {r['Mtot']:.3e} | {r['delta']:.2f} ± {sr['delta']:.2f} | {r['f']:.3f} ± {sr['f']:.3f} | {rl['f']:.3f} ± {sl['f']:.3f} |")
for nm, S in (("primary", PR), ("lower bound", LO)):
    f_ = S["full"]; P(f"{nm}: r_ta = " + (f"{f_['xta']:.2f} ± {S['sig_x']:.2f} R500 ({f_['xta']*np.sum(W*DI['R5']):.2f} Mpc), M_tot(<r_ta) {f_['ta']['Mtot']:.3e}, M_b(<r_ta) {f_['ta']['Mb']:.3e}, "
                                            f"f_ret(<r_ta) = {f_['fta']:.3f} ± {S['sig_f']:.3f}, excess-only {f_['ta']['fexc']:.3f}; reached in {S['n_reach']}/30 jackknife" if f_["xta"] else f"NOT REACHED (reached in {S['n_reach']}/30 jackknife)"))
P(f"M_b(<R500) = {fr['rows'][0]['Mb']:.3e} ± {PR['sig_rows'][0]['Mb']:.2e}; M_tot(<R500) = {fr['rows'][0]['Mtot']:.3e}")
for x in (1.0, 2.0, 3.0, 5.0):
    P(f"  x = {x:g}: f_ret {PR['full']['at'][x]['f']:.3f} ± {PR['sig_at'][x]['f']:.3f}, lower bound {LO['full']['at'][x]['f']:.3f} ± {LO['sig_at'][x]['f']:.3f}")
Tclose = None
if fr["xta"] and fr["ta"]["need_gy"] > 0:
    Tclose = LO["full"]["ta"]["Gy"]/fr["ta"]["need_gy"]
    P(f"T_close: y gas outside R500 closes f_ret(<r_ta) = 1 at isothermal-equivalent T = {Tclose:.3f} T500 = {Tclose*fr['T5']:.3f} keV (needed {fr['ta']['need_gy']:.3e}, primary {fr['ta']['Gy']:.3e})")
LAB = label(PR, LO, DI["n"]); fails = [k for k, v in KAOK.items() if not v]
if fails: LAB = f"NO VERDICT [KNOWN ANSWER FAILS: {', '.join(fails)}]"
# ---------------------------------------------------------------- brackets
P("\n## Brackets (label per bracket)")
BR = {"lens tail x^-1.5": dict(ltail=-1.5), "lens tail x^-3": dict(ltail=-3.0), "lens no tail": dict(ltail=None), "y tail x^-3": dict(ytail=-3.0),
      "no beam correction": dict(beam=False), "CIB-deprojected y": dict(mapk="ComptonY_deproj_cib_1.0_10.7"), "gas500 = 0.0536 M500": dict(gas5mode="frac"),
      "no stars beyond R500": dict(star_out=0.0), "stars x 1.5": dict(star_all=1.5), "R 5.562": dict(R=5.562), "delta_ta 11": dict(dta=11.0),
      "lambda_n 2.5e-7": dict(lam=2.5e-7), "lambda_n 2.5e-3": dict(lam=2.5e-3), "M500 x 0.7": dict(m5f=0.7), "M500 x 1.4": dict(m5f=1.4)}
BL = {}; DZ = build([r for r in DI["KEEP"] if r["z"] <= 0.20], "y")
for nm, kw in list(BR.items()) + [("z 0.05-0.20", None)]:
    if kw is None: Sp = summary(DZ, lambda D, s: census(D, s)); Sl = summary(DZ, lambda D, s: census(D, s, tau_mode="iso")); nk = DZ["n"]
    else: Sp = summary(DI, lambda D, s, kw=kw: census(D, s, **kw)); Sl = summary(DI, lambda D, s, kw=kw: census(D, s, tau_mode="iso", **kw)); nk = DI["n"]
    lb = label(Sp, Sl, nk) if not fails else LAB
    BL[nm] = dict(label=lb, xta=Sp["full"]["xta"], f=Sp["full"]["fta"], sf=Sp["sig_f"], n_reach=Sp["n_reach"], d16=Sp["full"]["rows"][-1]["delta"])
    P(f"  {nm}: " + (f"r_ta {Sp['full']['xta']:.2f} ({Sp['n_reach']}/30), f_ret {Sp['full']['fta']:.3f} ± {Sp['sig_f']:.3f}" if Sp["full"]["xta"] else f"r_ta NOT REACHED, delta(16) {Sp['full']['rows'][-1]['delta']:.2f}") + f" -> {lb}")
tags = [nm for nm, b in BL.items() if b["label"] != LAB]
FINAL = LAB + (f" [BRACKET-DEPENDENT: {', '.join(tags)}]" if tags else "")
# ---------------------------------------------------------------- footings
P("\n## Footings and the law row (reported; a0 enters only here)")
RBAR = float(np.sum(W*DI["R5"])); LAW = {}
for ft, a0 in A0.items():
    rowsL = []
    for x in (1.0, 3.0) + ((fr["xta"],) if fr["xta"] else ()):
        mb = np.interp(math.log(x), np.log(EDGES[IDX1:]), [r["Mb"] for r in fr["rows"]]); mt = np.interp(math.log(x), np.log(EDGES[IDX1:]), [r["Mtot"] for r in fr["rows"]])
        gN = G*mb*MSUN/(x*RBAR*MPC)**2; rowsL.append(dict(x=float(x), Mb=float(mb), Mlaw=float(mb*nu_mono(gN/a0)), Mtot=float(mt), gN_over_a0=float(gN/a0)))
    LAW[ft] = dict(f=fr["fta"], label=FINAL, rows=rowsL); P(f"  {ft} (a0 {a0:.4e}): f_ret(<r_ta) {fr['fta']}; " + "; ".join(f"x {r['x']:.2f}: M_law/M_tot {r['Mlaw']/r['Mtot']:.3f} (g_N/a0 {r['gN_over_a0']:.3f})" for r in rowsL))
ka5 = LAW["canonical"]["f"] == LAW["alt"]["f"]; P(f"KA3 footings give identical f_ret: {'PASS' if ka5 else 'FAIL'}")
if not ka5: FINAL = "NO VERDICT [KNOWN ANSWER FAILS: footings]"
# ---------------------------------------------------------------- MUTATE
P("# GO2 MUTATE", True)
CT = summary(DC, lambda D, s: census(D, s)); x11 = 11.3137
dI, sI = PR["full"]["at"][x11]["delta"], PR["sig_at"][x11]["delta"]; dC, sC = CT["full"]["at"][x11]["delta"], CT["sig_at"][x11]["delta"]
m1 = (dC - dI) > 2*math.hypot(sI, sC)
P(f"M1 isolation off ({DC['n']} kept non-isolated groups): delta(11.3 R500) control {dC:.2f} ± {sC:.2f} vs isolated {dI:.2f} ± {sI:.2f}; delta(16) control {CT['full']['rows'][-1]['delta']:.2f} vs isolated {fr['rows'][-1]['delta']:.2f}; "
  f"control r_ta {CT['full']['xta']} -> {'BITES' if m1 else 'DOES NOT BITE'}", True)
P("   control delta profile x 1..16: " + ", ".join(f"{r['delta']:.1f}" for r in CT["full"]["rows"]), True)
M2 = census(DI, np.ones(DI["n"], bool), lens="flip"); m2 = M2["xta"] is None or M2["rows"][-1]["Mexc"] < 0
P(f"M2 e_t sign flipped: r_ta {M2['xta']}, M_exc(<16) {M2['rows'][-1]['Mexc']:.3e} -> {'BITES' if m2 else 'DOES NOT BITE'}", True)
M3 = summary(DI, lambda D, s: census(D, s, ysrc="shift")); zs3 = M3["full"]["gas5"]/M3["sig_at"][1.0]["gas5"]; zr3 = fr["gas5"]/PR["sig_at"][1.0]["gas5"]
m3 = abs(zs3) < 3 and zr3 >= 3
P(f"M3 y at shifted positions: gas inside R500 {M3['full']['gas5']:.2e} (z {zs3:+.2f}) vs real {fr['gas5']:.2e} (z {zr3:+.2f}) -> {'BITES' if m3 else 'DOES NOT BITE'}", True)
if fr["fta"] is not None:
    M4 = summary(DI, lambda D, s: census(D, s, R=2*R_B)); m4 = M4["full"]["fta"] is not None and abs(M4["full"]["fta"] - fr["fta"]) > 2*PR["sig_f"]
    P(f"M4 R x 2: f_ret(<r_ta) {M4['full']['fta']} vs {fr['fta']:.3f} ± {PR['sig_f']:.3f} -> {'BITES' if m4 else 'DOES NOT BITE'}", True)
else: m4 = None; P("M4 R x 2: cannot run (no r_ta)", True)
P(f"\n# LABEL\n#   canonical: {FINAL}\n#   alt: {FINAL}")
open(os.path.join(HERE, "go2.out"), "w").write("\n".join(OUT) + "\n"); open(os.path.join(HERE, "go2_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    return o
json.dump(clean(dict(label=dict(canonical=FINAL, alt=FINAL), label_frozen_rule=LAB, counts=cnt, n_iso_kept=DI["n"], n_ctl_kept=DC["n"],
                     primary=dict(rows=fr["rows"], sig_rows=PR["sig_rows"], xta=fr["xta"], fta=fr["fta"], ta=fr["ta"], sig_f=PR["sig_f"], sig_x=PR["sig_x"], n_reach=PR["n_reach"], gas5=fr["gas5"]),
                     lower=dict(rows=LO["full"]["rows"], xta=LO["full"]["xta"], fta=LO["full"]["fta"], sig_f=LO["sig_f"]), Tclose=Tclose,
                     KA=dict(ok=KAOK, KA1b_worst=worst, KA3_deproj=got, KA3_bias=bias, KA3_y=rk3, cross=z1, random=z2, footings=ka5), brackets=BL, law=LAW,
                     mutate=dict(M1=m1, M2=m2, M3=m3, M4=m4, control_rows=CT["full"]["rows"]))), open(os.path.join(HERE, "go2.json"), "w"), indent=1)
