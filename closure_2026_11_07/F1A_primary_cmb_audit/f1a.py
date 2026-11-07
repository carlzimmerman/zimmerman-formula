#!/usr/bin/env python3
"""F1A (FROZEN_CRITERIA.md 56879e50da): independent audit of fact F1 (primary CMB needs a cold component).
Own CamSpec-NPIPE (P-ACT cut) + ACT DR6 likelihoods, CLASS theory, own Newtonian-gauge fluid check. Imports nothing from
QX3 / QX10 / QX15.  Usage:  f1a.py ka | fit <B1|B2> <canonical|alt> <cold|MB> | cal | g4 | mutate2 | grade
One thread, < 1 GB. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import solve_ivp
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
EXT = os.path.join(REPO, "_external_data/qx15_cmb_primary"); CS = os.path.join(EXT, "camspec/CamSpec_NPIPE")
NOTE = "kappa = 1/2 FITTED; not theory closed"
G = 6.67430e-11; CL = 2.99792458e8; MPC = 3.0856775814913673e22; TCMB = 2.7255
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
RHO_C100 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)
OMR = 2.4728e-5 * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
LTH = 7000
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def dump(name, obj): json.dump(obj, open(os.path.join(PARTS, name), "w"), indent=1, default=float)

# ------------------------------------------------------------------ CamSpec NPIPE (own reader)
SPEC_NAMES = ["100x100", "143x143", "217x217", "143x217", "TE", "EE"]
class CamSpec:
    """Gaussian CamSpec with power-law residual foregrounds (use_fg_residual_model 0) on a chosen L range per spectrum."""
    def __init__(self, ranges):
        rng = [l.split() for l in open(os.path.join(CS, "like_NPIPE_12.6_unified_data_ranges.txt"), encoding="utf-8-sig") if l.strip()]
        spectra = np.loadtxt(os.path.join(CS, "like_NPIPE_12.6_unified_spectra.txt"))
        off = 0; idx = []; self.blocks = []; data = []
        for name, lmn, lmx in rng:
            lmn, lmx = int(lmn), int(lmx); n = lmx - lmn + 1
            if name in ranges:
                a, b = ranges[name]; ells = np.arange(max(a, lmn), min(b, lmx) + 1)
                idx.append(off + ells - lmn); self.blocks.append((name, ells)); data.append(spectra[ells, SPEC_NAMES.index(name)])
            off += n
        self.nX = off; idx = np.concatenate(idx); self.d = np.concatenate(data); self.n = len(idx); self.idx = idx
        mm = np.memmap(os.path.join(CS, "like_NPIPE_12.6_unified_cov.bin"), dtype=np.float32, mode="r", shape=(off, off))
        if self.n <= 4000:   # row by row with plain reads (no mapped pages held), float64 inverse
            del mm; C = np.empty((self.n, self.n))
            with open(os.path.join(CS, "like_NPIPE_12.6_unified_cov.bin"), "rb") as fh:
                for i, r_ in enumerate(idx):
                    fh.seek(int(r_) * off * 4); C[i] = np.fromfile(fh, dtype=np.float32, count=off)[idx]
            self.Ci = np.linalg.inv(C); self.chol = None; mm = None
        else:  # full TTTEEE (KA-P only): float32 in-place Cholesky, filled by row blocks to stay < 1 GB
            import scipy.linalg as SL
            A = np.empty((self.n, self.n), dtype=np.float32, order="F")
            for s in range(0, self.n, 500): A[s:s + 500, :] = mm[idx[s:s + 500]][:, idx]
            self.chol = SL.cho_factor(A, lower=True, overwrite_a=True, check_finite=False); self.Ci = None
        del mm
    def resid(self, D, nu):
        Ap, a143, a217, a1x2, n143, n217, n1x2, cTE, cEE = nu
        amp = {"143x143": (a143, n143), "217x217": (a217, n217), "143x217": (a1x2, n1x2)}
        out = []
        for name, ells in self.blocks:
            if name in amp:
                a, t = amp[name]; m = (D["tt"][ells] + a * (ells / 1500.0) ** t) / Ap ** 2
            elif name == "TE": m = D["te"][ells] / (cTE * Ap ** 2)
            elif name == "EE": m = D["ee"][ells] / (cEE * Ap ** 2)
            else: m = D["tt"][ells] / Ap ** 2           # 100x100 (not used: amp_100 = 0)
            out.append(m)
        return self.d - np.concatenate(out)
    def chi2(self, D, nu):
        r = self.resid(D, nu)
        if self.Ci is not None: return float(r @ self.Ci @ r)
        import scipy.linalg as SL
        x = SL.cho_solve(self.chol, r.astype(np.float32), check_finite=False); return float(np.dot(r, x.astype(np.float64)))
    @staticmethod
    def prior(nu): return ((nu[0] - 1) / 0.0025) ** 2 + ((nu[7] - 1) / 0.01) ** 2 + ((nu[8] - 1) / 0.01) ** 2
    BOUNDS = [(0.9, 1.1), (0, 50), (0, 50), (0, 50), (0, 5), (0, 5), (0, 5), (0.9, 1.1), (0.9, 1.1)]
    X0 = np.array([1.0, 10.0, 20.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    def profile(self, D, x0=None):
        f = lambda x: self.chi2(D, x) + self.prior(x)
        best = None
        for s in ([x0] if x0 is not None else []) + [self.X0]:
            r = minimize(f, s, method="L-BFGS-B", bounds=self.BOUNDS, options=dict(maxiter=400))
            if best is None or r.fun < best.fun: best = r
        return float(best.fun), best.x

P_CUT = {"143x143": (30, 1000), "217x217": (500, 1000), "143x217": (500, 1000), "TE": (30, 600), "EE": (30, 600)}
P_FULL = {"143x143": (0, 9999), "217x217": (0, 9999), "143x217": (0, 9999), "TE": (0, 9999), "EE": (0, 9999)}

# ------------------------------------------------------------------ ACT DR6 CMB-only (own SACC reader)
class ACT:
    def __init__(self):
        h = fits.open(os.path.join(EXT, "act/v1.0/dr6_data_cmbonly.fits"))
        win = {}
        for x in h:
            if x.name == "window:Bandpower": win[int(x.header["SACCNAME"])] = (np.array(x.data["values"], int), np.array(x.data["weight"], float))
        self.blocks = []; vals = []; i0 = 0
        for hdu, pol in (("data:cl_00", "tt"), ("data:cl_0e", "te"), ("data:cl_ee", "ee")):
            d = h[hdu].data; ls, W = win[int(d["window"][0])]; wi = np.array(d["window_ind"], int)
            keep = (d["ell"] >= 600) & (d["ell"] <= 6500)
            self.blocks.append((pol, ls, W[:, wi[keep]], np.arange(i0, i0 + len(d))[keep])); vals.append(np.array(d["value"], float)); i0 += len(d)
        self.d = np.concatenate(vals); C = np.array(h["covariance"].data, float)
        allk = np.concatenate([b[3] for b in self.blocks]); self.d = self.d[allk]; self.Ci = np.linalg.inv(C[np.ix_(allk, allk)])
    def model(self, D, A, Pp):
        out = []
        for pol, ls, W, _ in self.blocks:
            th = np.zeros(len(ls)); ok = ls < len(D[pol]); th[ok] = D[pol][ls[ok]]
            th = th / A ** 2 / Pp ** pol.count("e"); out.append(W.T @ th)
        return np.concatenate(out)
    def chi2(self, D, A=1.0, Pp=1.0):
        r = self.d - self.model(D, A, Pp); return float(r @ self.Ci @ r)
    def profile(self, D, x0=None):
        f = lambda x: self.chi2(D, x[0], x[1])
        r = minimize(f, x0 if x0 is not None else [1.0, 1.0], method="L-BFGS-B", bounds=[(0.5, 1.5), (0.9, 1.1)]); return float(r.fun), r.x

_L = {}
def lik(name):
    if name not in _L: _L[name] = {"Pcut": lambda: CamSpec(P_CUT), "P": lambda: CamSpec(P_FULL), "A": ACT}[name]()
    return _L[name]
def PA(D, x0=None):
    x0 = x0 or {}
    cp, xp = lik("Pcut").profile(D, x0.get("Pcut")); ca, xa = lik("A").profile(D, x0.get("A"))
    return dict(PA=cp + ca, Pcut=cp, A=ca, nuis=dict(Pcut=xp.tolist(), A=xa.tolist()))

# ------------------------------------------------------------------ theory (CLASS)
def camb_theory(h, ob, oc, lnA, ns, tau, nonlin=False):
    """A1: graded theory = CAMB 1.6.6, lmax 7000, lpa 1, linear lensing unless nonlin (reported HMCode reading)."""
    import camb
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(oc, 1e-7), tau=tau, mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
    p.InitPower.set_params(As=math.exp(lnA) * 1e-10, ns=ns); p.set_for_lmax(LTH, lens_potential_accuracy=1)
    p.NonLinear = camb.model.NonLinear_lens if nonlin else camb.model.NonLinear_none
    cl = camb.get_results(p).get_total_cls(LTH, CMB_unit="muK"); return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}

def class_D(h, ob, oc, lnA, ns, tau, nonlin=False, extra=None, lmax=3000):
    """A1: CLASS kept as an independent theory check on Pcut only (l_max 3500 keeps RSS < 1 GB)."""
    from classy import Class
    LT = lmax
    M = Class(); p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LT + 500, 'h': h, 'omega_b': ob,
                      'omega_cdm': max(oc, 1e-7), 'A_s': math.exp(lnA) * 1e-10, 'n_s': ns, 'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': TCMB}
    if nonlin: p['non_linear'] = 'hmcode'
    if extra: p.update(extra)
    M.set(p); M.compute(); cl = M.lensed_cl(LT); M.struct_cleanup()
    L = np.arange(LT + 1); f = L * (L + 1) / (2 * math.pi) * (TCMB * 1e6) ** 2
    return {k: cl[k] * f for k in ("tt", "te", "ee")}

def footing_h(foot, ob, od):
    w = 4 * FOOT[foot] ** 2 / (G * CL ** 2) / RHO_C100
    return math.sqrt(w + ob + od + OMR) if foot == "canonical" else math.sqrt(w)

def theta_to_pars(bg, foot, mode, th):
    if bg == "B1":
        od, lnA, tau = th; ob, ns, h = 0.0215, 0.95, 0.65
    else:
        ob, od, lnA, ns, tau = th; h = footing_h(foot, ob, 0.0 if mode == "MB" else od)
    if mode == "MB": od = 1e-7
    return dict(h=h, ob=ob, oc=od, lnA=lnA, ns=ns, tau=tau)

def do_fit(bg, foot, mode):
    lo = {"B1": [0.0, 1.5, 0.01], "B2": [0.0215, 0.0, 1.5, 0.80, 0.01]}[bg]; hi = {"B1": [0.40, 4.5, 0.15], "B2": [0.0230, 0.40, 4.5, 1.30, 0.15]}[bg]
    state = dict(best=None, x0={}, n=0)
    def f(x):
        x = np.asarray(x)
        pen = float(np.sum(np.clip(np.array(lo) - x, 0, None) ** 2 + np.clip(x - np.array(hi), 0, None) ** 2)) * 1e6
        xc = np.clip(x, lo, hi)
        if mode == "MB": xc[0 if bg == "B1" else 1] = 0.0
        try:
            pr = theta_to_pars(bg, foot, mode, xc); g = PA(camb_theory(**pr), state["x0"]); v = g["PA"] + pen
            state["x0"] = {k: np.array(vv) for k, vv in g["nuis"].items()}
        except Exception as e:
            v = 1e9; g = None
        state["n"] += 1
        if g is not None and (state["best"] is None or v < state["best"][0]): state["best"] = (v, xc.tolist(), g)
        return v
    if bg == "B1":
        starts = [np.array([0.12, 3.05, 0.06]), np.array([0.20, 3.3, 0.10])]; step = np.array([0.01, 0.05, 0.02])
        if mode == "MB": starts = [np.array([0.0, 3.05, 0.06]), np.array([0.0, 2.3, 0.12])]
    else:
        starts = [np.array([0.0223, 0.120, 3.05, 0.965, 0.06]), np.array([0.0225, 0.14, 3.2, 0.95, 0.09])]; step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])
        if mode == "MB": starts = [np.array([0.0223, 0.0, 3.05, 0.965, 0.06]), np.array([0.0220, 0.0, 2.1, 1.25, 0.12])]
    for s in starts:
        simplex = [s] + [s + np.eye(len(s))[i] * step[i] for i in range(len(s))]
        minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=300, xatol=1e-5, fatol=0.02))
    v, x, g = state["best"]; pr = theta_to_pars(bg, foot, mode, np.array(x))
    res = dict(bg=bg, foot=foot, mode=mode, theta=x, pars=pr, chi2=g, nfev=state["n"], peak_rss_GB=rss(), note=NOTE)
    if mode == "cold" and bg == "B2":
        res["chi2_hmcode_reported"] = PA(camb_theory(**pr, nonlin=True))["PA"]
    Dc = class_D(**pr); res["class_check_Pcut"] = dict(camb=g["Pcut"], class_=lik("Pcut").profile(Dc)[0])
    res["class_check_Pcut"]["diff"] = res["class_check_Pcut"]["class_"] - res["class_check_Pcut"]["camb"]
    dump(f"fit_{bg}_{foot}_{mode}.json", res); print(json.dumps({k: res[k] for k in ("bg", "foot", "mode", "theta", "pars", "nfev")}, default=float), res["chi2"]["PA"], flush=True)

# ------------------------------------------------------------------ KA
def camb_D(cosmo, As, ns, halofit=None, logl=None):
    import camb
    p = camb.CAMBparams(); p.set_cosmology(**cosmo); p.InitPower.set_params(As=As, ns=ns); p.set_for_lmax(9000, lens_potential_accuracy=8)
    if halofit: p.NonLinearModel.set_params(halofit_version=halofit)
    if logl: p.min_l_logl_sampling = logl
    cl = camb.get_results(p).get_total_cls(9000, CMB_unit="muK"); return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}

def do_ka():
    A = camb_D(dict(ombh2=0.022, omch2=0.117, cosmomc_theta=104.09e-4, tau=0.065, mnu=0.06, num_massive_neutrinos=1, TCMB=TCMB), 2e-9, 0.96, logl=6000)
    ka_a = lik("A").chi2(A, 1.0, 1.0); print("KA-A", ka_a, flush=True)
    Pd = camb_D(dict(ombh2=0.02235048, omch2=0.12121379, cosmomc_theta=1.04240171e-2, tau=0.05, mnu=0.06, num_massive_neutrinos=1, TCMB=TCMB),
                math.exp(3.04920413) * 1e-10, 0.96399503, halofit="mead2020")
    nuP = np.array([0.99818025, 10.35947284, 18.67072461, 7.54932654, 0.83715482, 0.94987418, 1.23385364, 0.98781552, 1.013345])
    try:
        ka_p = lik("P").chi2(Pd, nuP); _L.pop("P", None); note = "float32 in-place Cholesky"
    except MemoryError:
        ka_p = None; note = "not run (memory)"
    res = dict(KA_A=dict(chi2=ka_a, ref=790.96, pass_=abs(ka_a - 790.96) <= 1.0),
               KA_P=dict(chi2=ka_p, ref_qx15_camb166=11321.74, published=11337.34, pass_=(ka_p is not None and abs(ka_p - 11321.74) <= 1.0), note=note),
               peak_rss_GB=rss(), note=NOTE)
    dump("ka.json", res); print(json.dumps(res, default=float), flush=True)

def do_cal():
    # Cobaya NPIPE test cosmology with CLASS (H0 given there; one 0.06 eV neutrino)
    import camb
    p = camb.CAMBparams(); p.set_cosmology(ombh2=0.02235048, omch2=0.12121379, cosmomc_theta=1.04240171e-2, tau=0.05, mnu=0.06, num_massive_neutrinos=1, TCMB=TCMB)
    p.InitPower.set_params(As=math.exp(3.04920413) * 1e-10, ns=0.96399503); p.set_for_lmax(LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
    cl = camb.get_results(p).get_total_cls(LTH, CMB_unit="muK"); D = {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}
    g = PA(D); dump("cal.json", dict(chi2_cal=g, chi2_cal_CLASS_preA1=3802.378556611808, note=NOTE)); print("chi2_cal", g["PA"], g["Pcut"], g["A"], flush=True)

# ------------------------------------------------------------------ G4: own Newtonian-gauge fluid code
def g4():
    """Fluids: radiation (w = cs2 = 1/3), baryons (dust), cold (dust), X (w_X, cs2_X). conformal time; x = ln a. H0 = 1/2997.92458 per Mpc."""
    f = json.load(open(os.path.join(PARTS, "fit_B2_canonical_cold.json")))["pars"]
    h = f["h"]; H0 = h / 2997.92458
    Ob, Od, Or = f["ob"] / h ** 2, f["oc"] / h ** 2, OMR / h ** 2; ODE = 1 - Ob - Od - Or
    def run(k, fl, zend=1100.0):
        names = list(fl)
        def rho(a): return np.array([fl[n][0] * a ** (-3 * (1 + fl[n][1])) for n in names])
        def rhs(x, y):
            a = math.exp(x); r = rho(a) + ODE_bg(a); Hc = a * H0 * math.sqrt(r.sum() if False else (rho(a).sum() + ODE_bg(a)))
            rr = rho(a); tot = rr.sum() + ODE_bg(a)
            phi = y[0]; d = y[1::2]; th = y[2::2]
            dphi = -Hc * phi + 1.5 * Hc ** 2 / k ** 2 * sum(rr[i] / tot * (1 + fl[n][1]) * th[i] for i, n in enumerate(names))
            out = [dphi]
            for i, n in enumerate(names):
                w, cs2 = fl[n][1], fl[n][2]
                dd = -(1 + w) * (th[i] - 3 * dphi) - 3 * Hc * (cs2 - w) * d[i] - 9 * Hc ** 2 * (1 + w) * (cs2 - w) * th[i] / k ** 2
                dt = -Hc * (1 - 3 * cs2) * th[i] + cs2 * k ** 2 * d[i] / (1 + w) + k ** 2 * phi
                out += [dd, dt]
            return np.array(out) / Hc
        def ODE_bg(a): return ODE_rem
        ODE_rem = 1 - sum(v[0] for v in fl.values())     # the smooth remainder (Lambda), keeps flatness
        ai = 1e-6; tau_i = 1 / (ai * H0 * math.sqrt(Or)) * ai     # radiation era: tau = a / (a H) ~ 1/(H0 sqrt(Or)) a
        tau_i = ai / (H0 * math.sqrt(Or)); phi0 = 1.0
        y0 = [phi0]
        for n in names:
            w = fl[n][1]; y0 += [-1.5 * (1 + w) * phi0, 0.5 * k ** 2 * tau_i * phi0]
        s = solve_ivp(rhs, (math.log(ai), math.log(1 / (1 + zend))), y0, method="LSODA", rtol=1e-7, atol=1e-12)
        y = s.y[:, -1]; a = 1 / (1 + zend); rr = rho(a)
        return {n: dict(drho=float(rr[i] * y[1 + 2 * i]), delta=float(y[1 + 2 * i])) for i, n in enumerate(names)}
    ks = [0.02, 0.05, 0.1, 0.2, 0.3]; out = dict(bg=dict(h=h, Ob=Ob, Od=Od, Or=Or, ODE=ODE), rows=[])
    for k in ks:
        ref = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "d": (Od, 0, 0)})
        x1 = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "d": (Od, 0, 0), "X": (ODE, -0.95, 1.0)})
        x2 = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "X": (Od, 0.0, 1.0)})
        kag = run(k, {"r": (Or, 1 / 3, 1 / 3), "b": (Ob, 0, 0), "X": (Od, 0.0, 0.0)})
        q1 = abs(x1["X"]["drho"]) / abs(ref["d"]["drho"]); q2 = abs(x2["X"]["drho"]) / abs(ref["d"]["drho"]); qk = abs(kag["X"]["drho"]) / abs(ref["d"]["drho"])
        out["rows"].append(dict(k=k, Q_X1=q1, Q_X2=q2, KA_dust=qk, delta_dust=ref["d"]["delta"], delta_X1=x1["X"]["delta"], delta_X2=x2["X"]["delta"],
                                delta_b_with_X2=x2["b"]["delta"], delta_b_ref=ref["b"]["delta"]))
        print(json.dumps(out["rows"][-1]), flush=True)
    sub = [r for r in out["rows"] if r["k"] >= 0.05]
    out["reproduced"] = bool(all(r["Q_X1"] <= 0.05 and r["Q_X2"] <= 0.05 for r in sub))
    out["KA_G4_pass"] = bool(all(abs(r["KA_dust"] - 1) <= 1e-3 for r in out["rows"]))
    out["note"] = NOTE; dump("g4.json", out); print("G4 reproduced", out["reproduced"], "KA", out["KA_G4_pass"], flush=True)

def mutate2():
    res = {}
    for foot in FOOT:
        f = json.load(open(os.path.join(PARTS, f"fit_B2_{foot}_cold.json"))); pr = dict(f["pars"]); c0 = f["chi2"]["PA"]
        D0 = camb_theory(**pr); pr2 = dict(pr); pr2["ob"] = 0.0300
        if foot == "canonical": pr2["h"] = footing_h(foot, 0.0300, pr["oc"])
        D2 = camb_theory(**pr2); g = PA(D2)
        L = np.arange(len(D0["tt"])); w = (L > 100) & (L < 400)
        p0 = int(L[w][np.argmax(D0["tt"][w])]); p2 = int(L[w][np.argmax(D2["tt"][w])])
        res[foot] = dict(chi2_best=c0, chi2_ob030=g["PA"], dchi2=g["PA"] - c0, peak1_best=p0, peak1_ob030=p2,
                         pass_=bool(g["PA"] - c0 > 25 and p0 != p2))
        print(foot, json.dumps(res[foot]), flush=True)
    dump("mutate_M2.json", dict(M2=res, note=NOTE))

if __name__ == "__main__":
    a = sys.argv[1:]; t0 = time.time()
    if a[0] == "ka": do_ka()
    elif a[0] == "cal": do_cal()
    elif a[0] == "fit": do_fit(a[1], a[2], a[3])
    elif a[0] == "g4": g4()
    elif a[0] == "mutate2": mutate2()
    print(f"done {a} {time.time() - t0:.0f} s, peak RSS {rss():.2f} GB", flush=True)
