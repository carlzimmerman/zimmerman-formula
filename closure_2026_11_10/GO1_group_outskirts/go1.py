"""GO1 Part A step 3 (FROZEN_CRITERIA.md c1a9527ebf; lensing deprojection per AMENDMENT_A1.md 05f48b8a6d): stack the per-group shear and y (go1_measure.py checkpoint), deproject the
lensing excess mass and the y pressure on the frozen x grid, build the baryon census, find r_ta (delta 5.55 rho_m) and grade f_ret.
python3 -I go1.py <checkpoint.npz>. Writes go1.out, go1.json, go1_MUTATE.out. Both footings; a0 only in the reported law row.
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
YCONST = MUE*MP*511.0*MPC**2/SIGT/MSUN                                              # Msun per (p~ x Vx), p~ = stacked y R500^2/T500[keV]
OMB = 0.0224; RHOB0 = OMB*2.775e11                                                   # Msun/Mpc^3 (physical, h-free)
R_B = 5.41; DTA = 5.55
EDGES = np.geomspace(0.25, 16.0, 13); NB = 12; YEDGES = np.r_[0.0, EDGES]; NY = 13
OUT, MOUT = [], []
def P(s="", m=False): print(s, flush=True); (MOUT if m else OUT).append(str(s))
# ---------------------------------------------------------------- kernels
def shell_SM(R, a, b):
    s = lambda q: np.sqrt(np.clip(q*q - R*R, 0, None))
    Sig = 2*(s(b) - s(a)); Mc = 4*np.pi/3*((b**3 - s(b)**3) - (a**3 - s(a)**3)); return Sig, Mc
def dsig_shell(R, a, b): Sig, Mc = shell_SM(R, a, b); return Mc/(np.pi*R*R) - Sig
def bin_avg(f, lo, hi, n=400):
    u = (np.arange(n) + 0.5)/n; R = np.sqrt(lo*lo + u*(hi*hi - lo*lo)); return f(R).mean()          # area-weighted (uniform sources)
TAILX = np.geomspace(16.0, 64.0, 401)
def lens_K(tail):
    """AMENDMENT A1: point mass inside x = 0.25 + 12 uniform shells on the bin edges; the last shell carries the tail."""
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
    """A1: weighted least squares + Tikhonov on D2(x^2 rho); returns the enclosed excess mass at EDGES[0..12]."""
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
# shell-mean tau for the primary T(x) = T500 x^-0.6 (x >= 1), volume-weighted
TAU = np.ones(NY)
for j in range(IY1, NY):
    xx = np.linspace(YEDGES[j], YEDGES[j + 1], 400); TAU[j] = 1/np.average(xx**0.6, weights=xx**2)   # mass ~ <1/tau>
# ---------------------------------------------------------------- data
CK = dict(np.load(sys.argv[1], allow_pickle=True))["res"].item()
REC = [CK[i] for i in sorted(CK)]; KEEP = [r for r in REC if r["keep"]]
P(f"GO1 Part A. groups selected {len(REC)}, kept {len(KEEP)}; dropped: " + str({w: sum(r['why'] == w for r in REC) for w in ('sources', 'empty bin', 'y mask', 'randoms')}))
n = len(KEEP); z = np.array([r["z"] for r in KEEP]); R5 = np.array([r["R500"] for r in KEEP]); M5 = np.array([r["M500"] for r in KEEP]); MG = np.array([r["Mgas500"] for r in KEEP])
Ez = np.sqrt(0.3*(1 + z)**3 + 0.7); T5 = 8.71*(M5/1e15)**(2/3)*Ez**(2/3); MST = 1.7e12*(M5/1e14)**0.6
def dsig(s, key="numt"): return s[key]/np.where(s["den"] > 0, s["den"], np.inf)/KG_PER_MSUN_PC2/(1 + M_BIAS)
DT = np.array([dsig(r["shear"]) for r in KEEP]); DX = np.array([dsig(r["shear"], "numx") for r in KEEP])
RT = [np.array([dsig(q["shear"]) for q in r["rnd"]]) for r in KEEP]; RX = [np.array([dsig(q["shear"], "numx") for q in r["rnd"]]) for r in KEEP]
var15 = np.array([r["shear"]["var15"]/r["shear"]["den15"]**2/KG_PER_MSUN_PC2**2/(1 + M_BIAS)**2 for r in KEEP])
W = 1/(var15*R5**4); W = W/W.sum()
SC = 1e12*R5**2                                                                       # (Msun/pc^2) -> Msun per unit x^2
MAPS = ("ComptonY", "ComptonY_deproj_cib_1.0_10.7")
YG = {m: np.array([r["y"][m] for r in KEEP]) for m in MAPS}; YR = {m: [np.array([q["y"][m] for q in r["rnd"]]) for r in KEEP] for m in MAPS}
YS = np.array([r["yshift"]["ComptonY"] if r["yshift"] is not None else np.full(NY, np.nan) for r in KEEP])
TPL = {k: np.array([r["y"][k] for r in KEEP]) for k in ("tr_gnfw", "tb_gnfw", "tr_beta", "tb_beta")}
CY = R5**2/T5
patch = np.empty(n, int); patch[np.argsort([r["ra"] for r in KEEP])] = np.arange(n)*30//n
DREAL = DT - np.array([r_.mean(0) for r_ in RT])
def _S(sel): w_ = W[sel]/W[sel].sum(); return (w_[:, None]*DREAL[sel]*SC[sel][:, None]).sum(0)
_reps = np.array([_S(patch != j) for j in range(30)]); SIGL = np.sqrt(29/30*((_reps - _reps.mean(0))**2).sum(0))   # A1 weights, fixed
def KA2():
    rs = 0.25; rho_n = lambda x: 1/((x/rs)*(1 + x/rs)**2); A2 = rho_n(2.0)*4.0
    rho = lambda x: np.where(x <= 64, rho_n(x) + np.where(x > 2, A2*x**-2.0, 0.0), 0.0)
    l = np.geomspace(1e-6, 64, 8000); Rf = np.geomspace(1e-5, 16.5, 4000)
    Sig = np.array([2*np.trapz(rho(np.sqrt(R*R + l*l)), l) for R in Rf]); Mc = np.r_[0, np.cumsum(0.5*(Sig[1:]*Rf[1:] + Sig[:-1]*Rf[:-1])*np.diff(Rf))]*2*np.pi
    DS = lambda R: np.interp(R, Rf, Mc)/(np.pi*R*R) - np.interp(R, Rf, Sig)
    d = np.array([bin_avg(DS, EDGES[i], EDGES[i + 1]) for i in range(NB)]); Sd = _S(np.ones(n, bool)); sig = SIGL*np.abs(d[4]/Sd[4])
    xs = np.geomspace(1e-6, 16, 40000); XT = (1.0, 2.83, 8.0); tr = np.array([np.trapz((4*np.pi*xs**2*rho(xs))[xs <= x], xs[xs <= x]) for x in XT])
    at = lambda Me: np.array([np.interp(math.log(x), np.log(EDGES), Me) for x in XT])
    got = at(deproj(d, sig))/tr; rg = np.random.default_rng(1110); mk = np.array([at(deproj(d + sig*rg.standard_normal(NB), sig)) for _ in range(200)])
    bias = (mk.mean(0) - tr)/mk.std(0)
    return dict(zip(map(str, XT), got.tolist())), bool(np.all(np.abs(got - 1) < 0.05)), bias.tolist(), bool(np.all(np.abs(bias) <= 0.3)), (mk.std(0)/tr).tolist()
P(f"median z {np.median(z):.3f}; weighted mean M500 {np.sum(W*M5):.3e}, Mgas500 {np.sum(W*MG):.3e}, R500 {np.sum(W*R5):.3f} Mpc, T500 {np.sum(W*T5):.2f} keV; "
  f"median theta500 {np.median([r['th500'] for r in KEEP]):.2f}'; randoms per group {np.mean([len(r['rnd']) for r in KEEP]):.2f}")
# ---------------------------------------------------------------- one census from a selection
def census(sel, R=R_B, ltail=-2.0, ytail=None, mapk="ComptonY", beam=True, mg_f=1.0, star_out=1.0, star_all=1.0, dta=DTA,
           lens="real", ysrc="real", tau_mode="primary", lam=LAMN):
    w = W[sel]/W[sel].sum()
    if lens == "real": d = DT[sel] - np.array([RT[i].mean(0) for i in np.where(sel)[0]])
    elif lens == "cross": d = DX[sel] - np.array([RX[i].mean(0) for i in np.where(sel)[0]])
    elif lens == "flip": d = -(DT[sel] - np.array([RT[i].mean(0) for i in np.where(sel)[0]]))
    elif lens == "rr": d = np.array([RT[i][0::2].mean(0) - RT[i][1::2].mean(0) for i in np.where(sel)[0]])
    S = (w[:, None]*d*SC[sel][:, None]).sum(0); Mexc = deproj(S, SIGL, ltail, lam)                                  # at EDGES[0..12]
    if ysrc == "real": yv = YG[mapk][sel] - np.array([YR[mapk][i].mean(0) for i in np.where(sel)[0]])
    elif ysrc == "rr": yv = np.array([YR[mapk][i][0::2].mean(0) - YR[mapk][i][1::2].mean(0) for i in np.where(sel)[0]])
    elif ysrc == "shift":
        ii = np.where(sel)[0]; okk = np.isfinite(YS[ii]).all(1); yv = YS[ii] - np.array([YR[mapk][i].mean(0) for i in ii]); yv[~okk] = 0.0
    q = (w[:, None]*yv*CY[sel][:, None]).sum(0); A, VY = AY[ytail]; p = np.linalg.solve(A, q)
    if beam:
        tr = (w[:, None]*TPL["tr_gnfw"][sel]*CY[sel][:, None]).sum(0); tb = (w[:, None]*TPL["tb_gnfw"][sel]*CY[sel][:, None]).sum(0)
        p = p*np.linalg.solve(A, tr)/np.linalg.solve(A, tb)
    tau = TAU if tau_mode == "primary" else np.ones(NY)
    gy_sh = YCONST*p*VY/tau; Gy = np.r_[0, np.cumsum(np.where(np.arange(NY) >= IY1, gy_sh, 0.0))]          # cumulative at YEDGES
    Vb = lambda x: (w*RHOB0*(1 + z[sel])**3*4*np.pi/3*(x*R5[sel])**3).sum()
    gas5 = mg_f*(w*MG[sel]).sum(); st5 = star_all*(w*MST[sel]).sum(); sbar = st5/(w*M5[sel]).sum()
    X = EDGES[IDX1:]; rows = []
    for k, x in enumerate(X):
        ke = IDX1 + k; me = Mexc[ke]; gy = Gy[IY1 + k] if k > 0 else 0.0
        mb = gas5 + gy + st5 + star_out*sbar*(me - Mexc[IDX1]) + Vb(x) - Vb(1.0); vb = Vb(x)
        mt = me + (1 + R)*vb; rows.append(dict(x=float(x), Mexc=me, Gy=gy, Mb=mb, Mtot=mt, Vb=vb, delta=mt/((1 + R)*vb), f=R*mb/(mt - mb),
                                             fexc=R*(mb - vb)/(me - (mb - vb))))
    # r_ta: outermost crossing of delta = dta going outward; log-log interpolation
    dl = np.array([r_["delta"] for r_ in rows]); xta = None; fta = None; extra = {}
    if dl[-1] < dta and dl.max() >= dta:
        k = max(i for i in range(len(rows) - 1) if dl[i] >= dta and dl[i + 1] < dta)
        t = ((math.log(dl[k]) - math.log(dta))/(math.log(dl[k]) - math.log(dl[k + 1]))) if dl[k + 1] > 0 else (dl[k] - dta)/(dl[k] - dl[k + 1]); xta = math.exp(math.log(X[k]) + t*math.log(X[k + 1]/X[k]))
        def il(key):
            a_, b_ = rows[k][key], rows[k + 1][key]
            return math.exp(math.log(a_) + t*(math.log(b_) - math.log(a_))) if a_ > 0 and b_ > 0 else a_ + t*(b_ - a_)
        mb, mt, vb, gy = il("Mb"), il("Mtot"), il("Vb"), il("Gy") if rows[k]["Gy"] > 0 else rows[k]["Gy"] + t*(rows[k + 1]["Gy"] - rows[k]["Gy"])
        fta = R*mb/(mt - mb); need = mt/(1 + R) - (mb - gy)
        extra = dict(Mb=mb, Mtot=mt, Vb=vb, Gy=gy, need_gy=need, fexc=R*(mb - vb)/(mt - (1 + R)*vb - (mb - vb)))
    def at(x, key):
        lx = np.log(X); return float(np.interp(math.log(x), lx, [r_[key] for r_ in rows]))
    return dict(rows=rows, xta=xta, fta=fta, ta=extra, at={x: {k_: at(x, k_) for k_ in ("f", "Mexc", "Gy", "Mb", "Mtot", "fexc")} for x in (1.0, 2.0, 3.0, 5.0, 8.0)},
                Tmw=None, gas5=gas5, st5=st5, sbar=sbar, p=p)
ALL = np.ones(n, bool)
def jk(fun, sel=ALL):
    full = fun(sel); reps = [fun(sel & (patch != j)) for j in range(30)]; return full, reps
def jsig(vals):
    v = np.array([x for x in vals if x is not None and np.isfinite(x)], float); return float(np.sqrt((len(v) - 1)/len(v)*np.sum((v - v.mean())**2))) if len(v) > 2 else float("nan")
def summary(fun, sel=ALL, label=""):
    full, reps = jk(fun, sel); s = dict(full=full, n_reach=sum(r["xta"] is not None for r in reps))
    s["sig_f"] = jsig([r["fta"] for r in reps]); s["sig_x"] = jsig([r["xta"] for r in reps])
    s["sig_at"] = {x: {k: jsig([r["at"][x][k] for r in reps]) for k in ("f", "Mexc", "Gy", "Mb", "Mtot", "fexc")} for x in (1.0, 2.0, 3.0, 5.0, 8.0)}
    s["sig_rows"] = [{k: jsig([r["rows"][i][k] for r in reps]) for k in ("Mexc", "Gy", "Mb", "f", "delta")} for i in range(len(full["rows"]))]
    return s
def label(prim, lo):
    if prim["full"]["xta"] is None: return "NOT EVALUABLE [r_ta NOT REACHED]"
    if prim["n_reach"] < 27: return f"NOT EVALUABLE [r_ta reached in {prim['n_reach']} of 30 jackknife]"
    if not (prim["sig_f"] <= 0.20): return f"NOT EVALUABLE [sigma f_ret {prim['sig_f']:.2f} > 0.20]"
    f, s = prim["full"]["fta"], prim["sig_f"]; fl, sl = lo["full"]["fta"], lo["sig_f"]
    if fl is not None and fl - 2*sl > 1: return "FAILS FROM ABOVE"
    if f - 2*s > 1: return "ABOVE ON PRIMARY T"
    if abs(f - 1) <= 2*s: return "CLOSES ON HOT GAS"
    return "SHORT AT TURNAROUND [LOWER-BOUND CENSUS]"
# ---------------------------------------------------------------- known answers
P("\n## Known answers")
ka2, ka2ok, ka2b, ka2bok, ka2sd = KA2(); P(f"KA2 (A1 method) analytic NFW + r^-2 excess, M_rec/M_true at x 1, 2.83, 8: " + ", ".join(f"{v:.4f}" for v in ka2.values()) + f" (5 %) -> {'PASS' if ka2ok else 'FAIL'}")
P(f"KA2b 200 noisy mocks at the data's relative errors: bias/sd {np.round(ka2b, 2).tolist()}, rel sd {np.round(ka2sd, 2).tolist()} (|bias| <= 0.3 sd) -> {'PASS' if ka2bok else 'FAIL'}")
# KA3: correction from the gNFW template applied to the beta-model template; shells x 1-4 vs its analytic shell integrals
A, VY = AY[None]; w = W
corr = np.linalg.solve(A, (w[:, None]*TPL["tr_gnfw"]*CY[:, None]).sum(0))/np.linalg.solve(A, (w[:, None]*TPL["tb_gnfw"]*CY[:, None]).sum(0))
pb = np.linalg.solve(A, (w[:, None]*TPL["tb_beta"]*CY[:, None]).sum(0))*corr
xs = np.linspace(0, 16, 200001); bp = (1 + (xs/0.15)**2)**-1.5
truth = np.array([np.trapz((4*np.pi*xs**2*bp)[(xs >= YEDGES[j]) & (xs <= YEDGES[j + 1])], xs[(xs >= YEDGES[j]) & (xs <= YEDGES[j + 1])]) for j in range(NY)])*(w*CY).sum()
rk3 = (pb*VY/truth)[IY1:IY1 + 4]; ka3ok = bool(np.all(np.abs(rk3 - 1) <= 0.10))
P(f"KA3 beta-model template, beam-corrected by the gNFW correction, recovered/true pressure in shells x 1-1.41-2-2.83-4: {np.round(rk3, 3).tolist()} -> {'PASS' if ka3ok else 'FAIL'}")
P(f"     gNFW beam correction per shell x>=1: {np.round(corr[IY1:], 3).tolist()}")
c0 = census(ALL); idok = True
# KA4 identity: zero excess, zero baryon excess -> f = 1
for x in (1.0, 3.0, 8.0):
    vb = RHOB0*4*np.pi/3*x**3; idok &= abs(R_B*vb/((1 + R_B)*vb - vb) - 1) < 1e-12
P(f"KA4 f_ret identity with no excess: {'PASS' if idok else 'FAIL'}")
# ---------------------------------------------------------------- primary
P("\n## Primary (z 0.05-0.30, R 5.41, delta_ta 5.55, lens tail x^-2, y truncated, beam-corrected, T = T500 x^-0.6)")
PR = summary(lambda s: census(s)); LO = summary(lambda s: census(s, tau_mode="iso"))
fr = PR["full"]; P(f"gas500 {fr['gas5']:.3e}, stars500 {fr['st5']:.3e} (s = M*/M500 {fr['sbar']:.4f})")
P("| x | M_exc (lensing) | y gas 1..x (primary T) | M_b | M_tot | delta/rho_m | f_ret | f_ret_lo (isothermal) |"); P("|---|---|---|---|---|---|---|---|")
for i, r in enumerate(fr["rows"]):
    sr = PR["sig_rows"][i]; rl = LO["full"]["rows"][i]; sl = LO["sig_rows"][i]
    P(f"| {r['x']:.2f} | {r['Mexc']:.3e} ± {sr['Mexc']:.2e} | {r['Gy']:.3e} ± {sr['Gy']:.2e} | {r['Mb']:.3e} | {r['Mtot']:.3e} | {r['delta']:.2f} ± {sr['delta']:.2f} | {r['f']:.3f} ± {sr['f']:.3f} | {rl['f']:.3f} ± {sl['f']:.3f} |")
for nm, S in (("primary", PR), ("lower bound", LO)):
    f_ = S["full"]; P(f"{nm}: r_ta = " + (f"{f_['xta']:.2f} ± {S['sig_x']:.2f} R500, f_ret(<r_ta) = {f_['fta']:.3f} ± {S['sig_f']:.3f}, excess-only {f_['ta']['fexc']:.3f}; reached in {S['n_reach']}/30 jackknife" if f_["xta"] else "NOT REACHED"))
for x in (1.0, 2.0, 3.0, 5.0):
    P(f"  x = {x:g}: f_ret {PR['full']['at'][x]['f']:.3f} ± {PR['sig_at'][x]['f']:.3f}, lower bound {LO['full']['at'][x]['f']:.3f} ± {LO['sig_at'][x]['f']:.3f}, excess-only {PR['full']['at'][x]['fexc']:.3f}")
# T_mw check and T_close
iso = census(ALL, tau_mode="iso"); A_, VY_ = AY[None]; gsh = YCONST*iso["p"]*VY_
xb = lambda x, a=0.15: x - a*math.atan(x/a); mbeta = fr["gas5"]*(xb(1.0) - xb(0.5))/xb(1.0)
Tmw = (gsh[3] + gsh[4])/mbeta; P(f"T_mw(0.5-1 R500) / T500 from y over the eRASS1 beta-model gas: {Tmw:.2f} (reported check on the T500 scale)")
if fr["xta"]:
    lam = LO["full"]["ta"]["Gy"]/fr["ta"]["need_gy"] if fr["ta"]["need_gy"] > 0 else float("nan")
    P(f"T_close: the y gas outside R500 closes f_ret(<r_ta) = 1 at an isothermal-equivalent mean T = {lam:.3f} T500 = {lam*np.sum(W*T5):.3f} keV "
      f"(needed y gas {fr['ta']['need_gy']:.3e} vs primary {fr['ta']['Gy']:.3e}, isothermal {LO['full']['ta']['Gy']:.3e})")
LAB = label(PR, LO)
# ---------------------------------------------------------------- nulls
P("\n## Nulls")
def zrow(S, keys):
    return {f"{k}@{x:g}": (S["full"]["at"][x][k], S["sig_at"][x][k], S["full"]["at"][x][k]/S["sig_at"][x][k]) for k, xs_ in keys for x in xs_}
N1 = summary(lambda s: census(s, lens="cross")); z1 = zrow(N1, [("Mexc", (1.0, 3.0, 8.0))])
N2 = summary(lambda s: census(s, lens="rr", ysrc="rr")); z2 = zrow(N2, [("Mexc", (3.0, 8.0)), ("Gy", (3.0, 8.0))])
n1ok = all(abs(v[2]) < 3 for v in z1.values()); n2ok = all(abs(v[2]) < 3 for v in z2.values())
P("N1 cross shear M_exc: " + "; ".join(f"{k} {v[0]:.2e} ± {v[1]:.2e} (z {v[2]:+.2f})" for k, v in z1.items()) + f" -> {'PASS' if n1ok else 'FAIL'}")
P("N2 random-minus-random: " + "; ".join(f"{k} {v[0]:.2e} ± {v[1]:.2e} (z {v[2]:+.2f})" for k, v in z2.items()) + f" -> {'PASS' if n2ok else 'FAIL'}")
if not (n1ok and n2ok): LAB = "NO VERDICT [NULL FAILS]"
# ---------------------------------------------------------------- brackets
P("\n## Brackets (label per bracket)")
BR = {"lens tail x^-1.5": dict(ltail=-1.5), "lens tail x^-3": dict(ltail=-3.0), "lens no tail": dict(ltail=None), "y tail x^-3": dict(ytail=-3.0),
      "no beam correction": dict(beam=False), "CIB-deprojected y": dict(mapk="ComptonY_deproj_cib_1.0_10.7"), "Mgas500 x 0.8": dict(mg_f=0.8),
      "no stars beyond R500": dict(star_out=0.0), "stars x 1.5": dict(star_all=1.5), "R 5.562": dict(R=5.562), "delta_ta 11": dict(dta=11.0), "lambda_n 2.5e-7": dict(lam=2.5e-7), "lambda_n 2.5e-3": dict(lam=2.5e-3)}
BL = {}; zlo = z <= 0.20
for nm, kw in list(BR.items()) + [("z 0.05-0.20", None)]:
    if kw is None: Sp = summary(lambda s: census(s), zlo); Sl = summary(lambda s: census(s, tau_mode="iso"), zlo)
    else: Sp = summary(lambda s, kw=kw: census(s, **kw)); Sl = summary(lambda s, kw=kw: census(s, tau_mode="iso", **kw))
    lb = label(Sp, Sl) if LAB != "NO VERDICT [NULL FAILS]" else LAB; BL[nm] = dict(label=lb, xta=Sp["full"]["xta"], f=Sp["full"]["fta"], sf=Sp["sig_f"], flo=Sl["full"]["fta"], sflo=Sl["sig_f"],
                                                                               f3=Sp["full"]["at"][3.0]["f"], s3=Sp["sig_at"][3.0]["f"])
    P(f"  {nm}: " + (f"r_ta {Sp['full']['xta']:.2f}, f_ret {Sp['full']['fta']:.3f} ± {Sp['sig_f']:.3f}, lower {Sl['full']['fta'] if Sl['full']['fta'] is None else round(Sl['full']['fta'], 3)}" if Sp["full"]["xta"] else "r_ta NOT REACHED")
      + f"; f_ret(3 R500) {Sp['full']['at'][3.0]['f']:.3f} ± {Sp['sig_at'][3.0]['f']:.3f} -> {lb}")
tags = [nm for nm, b in BL.items() if b["label"] != LAB]
FINAL = LAB + (f" [BRACKET-DEPENDENT: {', '.join(tags)}]" if tags else "")
# ---------------------------------------------------------------- footings: f identical; law row (reported)
P("\n## Footings and the law row (reported; a0 enters only here)")
RBAR = float(np.sum(W*R5)); LAW = {}
for ft, a0 in A0.items():
    rowsL = []
    for x in (1.0, 3.0) + ((fr["xta"],) if fr["xta"] else ()):
        mb = np.interp(math.log(x), np.log(EDGES[IDX1:]), [r["Mb"] for r in fr["rows"]]); mt = np.interp(math.log(x), np.log(EDGES[IDX1:]), [r["Mtot"] for r in fr["rows"]])
        gN = G*mb*MSUN/(x*RBAR*MPC)**2; rowsL.append(dict(x=float(x), Mb=float(mb), Mlaw=float(mb*nu_mono(gN/a0)), Mtot=float(mt), gN_over_a0=float(gN/a0)))
    LAW[ft] = dict(f=fr["fta"], rows=rowsL); P(f"  {ft} (a0 {a0:.4e}): f_ret(<r_ta) {fr['fta']}; " + "; ".join(f"x {r['x']:.2f}: M_law/M_tot {r['Mlaw']/r['Mtot']:.3f} (g_N/a0 {r['gN_over_a0']:.3f})" for r in rowsL))
ka5 = LAW["canonical"]["f"] == LAW["alt"]["f"]; P(f"KA5 footings give identical f_ret: {'PASS' if ka5 else 'FAIL'}")
# ---------------------------------------------------------------- MUTATE
P("# GO1 MUTATE", True)
M1 = summary(lambda s: census(s, R=2*R_B))
m1 = (M1["full"]["fta"] is not None and fr["fta"] is not None and abs(M1["full"]["fta"] - fr["fta"]) > 2*PR["sig_f"])
P(f"M1 R x 2: f_ret(<r_ta) {M1['full']['fta']} (r_ta {M1['full']['xta']}) vs {fr['fta']} ± {PR['sig_f']:.3f} -> {'BITES' if m1 else 'DOES NOT BITE'}", True)
M2 = summary(lambda s: census(s, ysrc="shift")); z2s = zrow(M2, [("Gy", (3.0, 8.0))]); zr = zrow(PR, [("Gy", (3.0, 8.0))])
m2 = all(abs(v[2]) < 3 for v in z2s.values()) and any(abs(v[2]) >= 3 for v in zr.values())
P("M2 y at shifted positions: " + "; ".join(f"{k} {v[0]:.2e} ± {v[1]:.2e} (z {v[2]:+.2f})" for k, v in z2s.items()) + " | real: " + "; ".join(f"{k} z {v[2]:+.2f}" for k, v in zr.items()) + f" -> {'BITES' if m2 else 'DOES NOT BITE'}", True)
M3 = census(ALL, lens="flip"); m3 = M3["xta"] is None or M3["rows"][-1]["Mexc"] < 0
P(f"M3 e_t sign flipped: r_ta {M3['xta']}, M_exc(<16) {M3['rows'][-1]['Mexc']:.3e} -> {'BITES' if m3 else 'DOES NOT BITE'}", True)
P(f"\nKA1 (estimator copy vs CFG686 esd): see go1_ka1.out")
P(f"\n# LABEL (both footings): {FINAL}")
P(f"#   canonical: {FINAL}\n#   alt: {FINAL}")
open(os.path.join(HERE, "go1.out"), "w").write("\n".join(OUT) + "\n"); open(os.path.join(HERE, "go1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, np.integer)): return o.item()
    return o
json.dump(clean(dict(label=FINAL, label_frozen_rule=LAB, n=n, primary=dict(full={k: v for k, v in PR["full"].items() if k != "p"}, sig_f=PR["sig_f"], sig_x=PR["sig_x"], n_reach=PR["n_reach"], sig_at=PR["sig_at"], sig_rows=PR["sig_rows"]),
                     lower=dict(full={k: v for k, v in LO["full"].items() if k != "p"}, sig_f=LO["sig_f"], n_reach=LO["n_reach"], sig_at=LO["sig_at"]),
                     KA=dict(KA2=ka2, KA2ok=ka2ok, KA2b=ka2b, KA2bok=ka2bok, KA2sd=ka2sd, KA3=rk3, KA3ok=ka3ok, KA4ok=idok, KA5ok=ka5), Tmw=Tmw, nulls=dict(N1=z1, N2=z2, N1ok=n1ok, N2ok=n2ok),
                     brackets=BL, law=LAW, mutate=dict(M1=m1, M2=m2, M3=m3))), open(os.path.join(HERE, "go1.json"), "w"), indent=1)
