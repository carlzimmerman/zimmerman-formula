#!/usr/bin/env python3
"""CMB1 (FROZEN_CRITERIA.md a66f9d1254 / origin 0b04506ce2): anatomy of the primary-CMB cold requirement.
Uses F1A's own likelihood code (f1a.py: CamSpec P-ACT cut + ACT DR6), its footing rule and CAMB call. Nothing from
QX3 / QX10 / QX15.  Usage:
  cmb1.py base               block A + B at F1A's cold and MB fits, KA-1, M2, M1, KA-E
  cmb1.py fit <E|B> <foot>   block C fit
  cmb1.py post               block A + B at the block C fits
One thread, < 1 GB. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); F1A = os.path.join(HERE, "../F1A_primary_cmb_audit")
sys.path.insert(0, F1A)
import f1a                                            # own F1A likelihood code
from f1a import lik, PA, camb_theory, footing_h, CamSpec, OMR, TCMB, LTH, rss, FOOT
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
NOTE = "kappa = 1/2 FITTED; not theory closed"
def dump(n, o): json.dump(o, open(os.path.join(PARTS, n), "w"), indent=1, default=float)
def load(n, d=PARTS): return json.load(open(os.path.join(d, n)))
def f1a_fit(foot, mode): return load(f"fit_B2_{foot}_{mode}.json", os.path.join(F1A, "parts"))

# ------------------------------------------------------------------ theory with the smooth matter-like fluid X
def camb_fluid(h, ob, oX, lnA, ns, tau, cs2=1.0, background_only=False):
    """Lambda + smooth dust X carried by one CAMB fluid: w(a) = -rho_L / (rho_L + rho_X a^-3), sound speed cs2."""
    import camb
    from camb.dark_energy import DarkEnergyFluid
    OL = 1 - (ob + 1e-7 + oX) / h ** 2 - OMR / h ** 2
    if OL <= 0: raise ValueError("no room for Lambda")
    OX = oX / h ** 2; a = np.logspace(-9, 0, 2000); w = -OL / (OL + OX * a ** -3)
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=ob, omch2=1e-7, tau=tau, mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
    p.DarkEnergy = DarkEnergyFluid(cs2=cs2); p.DarkEnergy.set_w_a_table(a, w)
    if background_only: return camb.get_background(p)
    p.InitPower.set_params(As=math.exp(lnA) * 1e-10, ns=ns); p.set_for_lmax(LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
    cl = camb.get_results(p).get_total_cls(LTH, CMB_unit="muK"); return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}

def theory(pars):
    if "oX" in pars: return camb_fluid(pars["h"], pars["ob"], pars["oX"], pars["lnA"], pars["ns"], pars["tau"], pars.get("cs2", 1.0))
    return camb_theory(pars["h"], pars["ob"], pars["oc"], pars["lnA"], pars["ns"], pars["tau"])

# ------------------------------------------------------------------ labels for every data point
_LAB = {}
def labels():
    if _LAB: return _LAB
    P = lik("Pcut"); spec, ell = [], []
    for name, ells in P.blocks: spec += [name] * len(ells); ell += list(ells)
    _LAB["P"] = (np.array(spec), np.array(ell, float))
    A = lik("A"); spec, ell = [], []
    for pol, ls, W, _ in A.blocks:
        le = (ls[:, None] * W).sum(0) / W.sum(0); spec += [pol.upper()] * len(le); ell += list(le)
    _LAB["A"] = (np.array(spec), np.array(ell))
    _LAB["CP"] = np.linalg.inv(P.Ci); _LAB["CA"] = np.linalg.inv(A.Ci)
    return _LAB

def pieces():
    """(piece name, likelihood, mask fn on (spec, ell))."""
    TTP = ("143x143", "217x217", "143x217")
    out = []
    for lo, hi in ((30, 500), (500, 1000)):
        out.append((f"Planck TT {lo}-{hi}", "P", lambda s, l, lo=lo, hi=hi: np.isin(s, TTP) & (l >= lo) & (l < hi + (hi == 1000))))
        for cs in TTP: out.append((f"  Planck {cs} {lo}-{hi}", "Pr", lambda s, l, lo=lo, hi=hi, cs=cs: (s == cs) & (l >= lo) & (l < hi + (hi == 1000))))
    for sp in ("TE", "EE"):
        for lo, hi in ((30, 500), (500, 600)):
            out.append((f"Planck {sp} {lo}-{hi}", "P", lambda s, l, lo=lo, hi=hi, sp=sp: (s == sp) & (l >= lo) & (l < hi + (hi == 600))))
    for sp in ("TT", "TE", "EE"):
        for lo, hi in ((600, 1000), (1000, 2000), (2000, 1e9)):
            nm = f"ACT {sp} {lo}-{int(hi)}" if hi < 1e8 else f"ACT {sp} >2000"
            out.append((nm, "A", lambda s, l, lo=lo, hi=hi, sp=sp: (s == sp) & (l >= lo) & (l < hi)))
    return out

def contrib(pars, nuis):
    """Additive per-point chi2 contributions c_i = r_i (C^-1 r)_i at given nuisances."""
    D = theory(pars); P, A = lik("Pcut"), lik("A")
    nuP = np.array(nuis["Pcut"]); nuA = nuis["A"]
    rP = P.resid(D, nuP); cP = rP * (P.Ci @ rP)
    rA = A.d - A.model(D, nuA[0], nuA[1]); cA = rA * (A.Ci @ rA)
    return D, dict(rP=rP, cP=cP, rA=rA, cA=cA, prior=CamSpec.prior(nuP))

def block_A(cb):
    L = labels(); res = {}
    for name, which, m in pieces():
        key = "P" if which in ("P", "Pr") else "A"; s, l = L[key]; mask = m(s, l)
        c = cb["c" + key][mask].sum(); r = cb["r" + key][mask]; C = L["C" + key][np.ix_(mask, mask)]
        own = float(r @ np.linalg.solve(C, r)) if mask.sum() else 0.0
        res[name] = dict(additive=float(c), own_block=own, n=int(mask.sum()))
    res["calibration priors"] = dict(additive=float(cb["prior"]), own_block=float(cb["prior"]), n=0)
    res["L < 30"] = dict(additive=0.0, own_block=0.0, n=0, note="no data in PA")
    tot = float(cb["cP"].sum() + cb["cA"].sum() + cb["prior"])
    return res, tot

# ------------------------------------------------------------------ block B estimators
WIN = {"P1": (170, 280), "P2": (480, 600), "P3": (760, 880)}
def _feat_vec(y143, l143, yAtt, lAtt):
    f = {}
    for k, (lo, hi) in WIN.items():
        m = (l143 >= lo) & (l143 <= hi); lc = 0.5 * (lo + hi); x = (l143[m] - lc) / 100.0
        X = np.vstack([np.ones_like(x), x, x ** 2]).T; Wm = _EST["W"][k]
        b = np.linalg.solve(X.T @ Wm @ X, X.T @ Wm @ y143[m])
        xs = -b[1] / (2 * b[2]); f["L" + k[1]] = lc + 100 * xs; f["H" + k[1]] = b[0] - b[1] ** 2 / (4 * b[2])
    hi_ = (lAtt >= 2000) & (lAtt <= 3000); lo_ = (lAtt >= 600) & (lAtt <= 1000)
    out = dict(F_oe=f["H1"] / f["H2"], F_32=f["H3"] / f["H2"], F_damp=yAtt[hi_].mean() / yAtt[lo_].mean(),
               F_pos1=f["L1"], F_sp=(f["L3"] - f["L1"]) / 2)
    out.update({k: v for k, v in f.items()}); return out
_EST = {}
def estimator_setup():
    if _EST: return _EST
    L = labels(); P, A = lik("Pcut"), lik("A")
    s, l = L["P"]; m143 = s == "143x143"; C143 = L["CP"][np.ix_(m143, m143)]; l143 = l[m143]
    W = {}
    for k, (lo, hi) in WIN.items():
        mm = (l143 >= lo) & (l143 <= hi); W[k] = np.linalg.inv(C143[np.ix_(mm, mm)])
    sA, lA = L["A"]; mTT = sA == "TT"; CAtt = L["CA"][np.ix_(mTT, mTT)]
    _EST.update(W=W, m143=m143, l143=l143, mTT=mTT, lAtt=lA[mTT], C143=C143, CAtt=CAtt)
    feats = _feat_vec(P.d[m143], l143, A.d[mTT], lA[mTT])
    rng = np.random.default_rng(20261107); L1 = np.linalg.cholesky(C143); L2 = np.linalg.cholesky(CAtt)
    draws = [_feat_vec(P.d[m143] + L1 @ rng.standard_normal(len(l143)), l143, A.d[mTT] + L2 @ rng.standard_normal(mTT.sum()), lA[mTT]) for _ in range(1000)]
    sig = {k: float(np.std([d[k] for d in draws])) for k in feats}
    _EST.update(data=feats, sigma=sig); return _EST

def model_vectors(D, nuis):
    """The model's predicted 143x143 and ACT TT data vectors at its own nuisances."""
    E = estimator_setup(); P, A = lik("Pcut"), lik("A"); nuP = np.array(nuis["Pcut"])
    mP = P.d - P.resid(D, nuP); mA = A.model(D, nuis["A"][0], nuis["A"][1])
    return mP[E["m143"]], mA[E["mTT"]]

def block_B(D, nuis):
    E = estimator_setup(); y143, yA = model_vectors(D, nuis)
    f = _feat_vec(y143, E["l143"], yA, E["lAtt"])
    return {k: dict(model=float(f[k]), data=float(E["data"][k]), sigma=E["sigma"][k], z=float((f[k] - E["data"][k]) / E["sigma"][k])) for k in f}

# ------------------------------------------------------------------ base: cold + MB anatomy, KA-1, M2, M1, KA-E
def base():
    out = dict(note=NOTE); E = estimator_setup()
    out["features_data"] = E["data"]; out["features_sigma"] = E["sigma"]
    for foot in FOOT:
        r = {}
        for mode in ("cold", "MB"):
            f = f1a_fit(foot, mode); D, cb = contrib(f["pars"], f["chi2"]["nuis"])
            A_, tot = block_A(cb); r[mode] = dict(pars=f["pars"], chi2_F1A=f["chi2"]["PA"], chi2_rebuilt=tot, A=A_, B=block_B(D, f["chi2"]["nuis"]))
            print(foot, mode, "rebuilt", tot, "F1A", f["chi2"]["PA"], flush=True)
        dMB = r["MB"]["chi2_rebuilt"] - r["cold"]["chi2_rebuilt"]; dF = r["MB"]["chi2_F1A"] - r["cold"]["chi2_F1A"]
        r["DeltaMB"] = dMB; r["DeltaMB_F1A"] = dF; r["KA1_pass"] = abs(dMB - dF) <= 0.1
        r["A_delta"] = {k: r["MB"]["A"][k]["additive"] - r["cold"]["A"][k]["additive"] for k in r["cold"]["A"]}
        top = [k for k in r["A_delta"] if not k.startswith("  ")]
        ssum = sum(r["A_delta"][k] for k in top); r["M2_sum"] = ssum; r["M2_pass"] = abs(ssum - dMB) <= 1e-6 * abs(dMB)
        # M1: swap omega_b and omega_d at the cold best fit (nuisances held)
        pc = dict(r["cold"]["pars"]); ps = dict(pc); ps["ob"], ps["oc"] = pc["oc"], pc["ob"]
        if foot == "canonical": ps["h"] = footing_h(foot, ps["ob"], ps["oc"])
        Bs = block_B(camb_theory(**ps), f1a_fit(foot, "cold")["chi2"]["nuis"]); Bc = r["cold"]["B"]
        doe = (Bs["F_oe"]["model"] - Bc["F_oe"]["model"]) / E["sigma"]["F_oe"]; d32 = (Bs["F_32"]["model"] - Bc["F_32"]["model"]) / E["sigma"]["F_32"]
        ratio = d32 / doe if doe != 0 else float("inf")
        r["M1"] = dict(pars_swapped=ps, B_swapped=Bs, dF_oe_sigma=doe, dF_32_sigma=d32, ratio=ratio,
                       pass_=bool(abs(doe) > 5 and (ratio < 0.5 or ratio > 2)))
        print(foot, "M1", r["M1"]["dF_oe_sigma"], r["M1"]["dF_32_sigma"], r["M1"]["pass_"], flush=True)
        # KA-E: fluid apparatus at the cold best fit
        import camb
        pcd = dict(pc); b0 = camb.get_background(_std_params(pc)); b1 = camb_fluid(pc["h"], pc["ob"], pc["oc"], 0, 0, 0, background_only=True)
        zs = [0, 0.5, 2, 100, 1100, 1e4, 1e6]; dh = max(abs(b1.hubble_parameter(z) / b0.hubble_parameter(z) - 1) for z in zs)
        dth = abs(b1.get_derived_params()["thetastar"] / b0.get_derived_params()["thetastar"] - 1)
        Dfl = camb_fluid(pc["h"], pc["ob"], pc["oc"], pc["lnA"], pc["ns"], pc["tau"], cs2=1e-6); gfl = PA(Dfl)
        O = abs(gfl["PA"] - r["cold"]["chi2_F1A"])
        r["KA_E"] = dict(max_dH=dh, dtheta=dth, bg_pass=bool(dh <= 1e-5 and dth <= 1e-5), chi2_fluid_cs2_1e6=gfl["PA"], offset_O=O)
        print(foot, "KA-E", json.dumps(r["KA_E"]), flush=True)
        out[foot] = r
    dump("base.json", out)

def _std_params(pc):
    import camb
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * pc["h"], ombh2=pc["ob"], omch2=pc["oc"], tau=pc["tau"], mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
    return p

# ------------------------------------------------------------------ block C fits
def do_fit(kind, foot):
    if kind == "E":
        lo, hi = [0.0215, 0.0, 1.5, 0.80, 0.01], [0.0230, 0.40, 4.5, 1.30, 0.15]
        def pars(x): return dict(h=footing_h(foot, x[0], x[1]), ob=x[0], oX=x[1], lnA=x[2], ns=x[3], tau=x[4])
        starts = [np.array([0.0223, 0.12, 3.05, 0.965, 0.06]), np.array([0.0223, 0.05, 2.5, 1.10, 0.10])]; step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])
    else:
        lo, hi = [0.0215, 1.5, 0.80, 0.01], [0.20, 4.5, 1.30, 0.15]
        def pars(x): return dict(h=footing_h(foot, x[0], 0.0), ob=x[0], oc=1e-7, lnA=x[1], ns=x[2], tau=x[3])
        starts = [np.array([0.0223, 2.1, 1.25, 0.12]), np.array([0.12, 3.0, 0.97, 0.06])]; step = np.array([0.005, 0.05, 0.02, 0.02])
    st = dict(best=None, x0={}, n=0)
    def f(x):
        x = np.asarray(x); pen = float(np.sum(np.clip(np.array(lo) - x, 0, None) ** 2 + np.clip(x - np.array(hi), 0, None) ** 2)) * 1e6
        xc = np.clip(x, lo, hi)
        try:
            g = PA(theory(pars(xc)), st["x0"]); v = g["PA"] + pen; st["x0"] = {k: np.array(vv) for k, vv in g["nuis"].items()}
        except Exception:
            v = 1e9; g = None
        st["n"] += 1
        if g is not None and (st["best"] is None or v < st["best"][0]): st["best"] = (v, xc.tolist(), g)
        return v
    for s in starts:
        simplex = [s] + [s + np.eye(len(s))[i] * step[i] for i in range(len(s))]
        minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=300, xatol=1e-5, fatol=0.02))
    v, x, g = st["best"]
    res = dict(kind=kind, foot=foot, theta=x, pars=pars(np.array(x)), chi2=g, nfev=st["n"], peak_rss_GB=rss(), note=NOTE)
    dump(f"fit_{kind}_{foot}.json", res); print(json.dumps({k: res[k] for k in ("kind", "foot", "pars", "nfev")}, default=float), g["PA"], flush=True)

def post():
    out = dict(note=NOTE)
    for foot in FOOT:
        for kind in ("E", "B"):
            f = load(f"fit_{kind}_{foot}.json"); D, cb = contrib(f["pars"], f["chi2"]["nuis"]); A_, tot = block_A(cb)
            out[f"{kind}_{foot}"] = dict(pars=f["pars"], chi2=f["chi2"]["PA"], chi2_rebuilt=tot, A=A_, B=block_B(D, f["chi2"]["nuis"]))
            print(kind, foot, f["chi2"]["PA"], tot, flush=True)
    dump("post.json", out)

if __name__ == "__main__":
    a = sys.argv[1:]; t0 = time.time()
    if a[0] == "base": base()
    elif a[0] == "fit": do_fit(a[1], a[2])
    elif a[0] == "post": post()
    print(f"done {a} {time.time() - t0:.0f} s, peak RSS {rss():.2f} GB", flush=True)
