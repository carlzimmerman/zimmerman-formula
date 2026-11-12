"""AZ2R blind re-grade (READING.md committed first). Own code; data table and SN cuts as in CFG681.
Usage: python azr.py MODE   with MODE in KA1, canonical, alt, canonical_MUTATE, alt_MUTATE
Deterministic: fixed starts, single thread (set OMP/OPENBLAS/MKL_NUM_THREADS=1 before running)."""
import json, os, sys
import numpy as np
from scipy.optimize import minimize, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "..", "..", "_external_data", "pantheonplus_dr")
MODE = sys.argv[1]

# ---- data (DESI DR2 BAO, arXiv 2503.14738, values as typed in CFG681) ----
GAL = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
       ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
       ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500)]
LYA_OLD = ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)
LYA_NEW = ("Lya", 2.330, 39.32, 0.33, 8.600, 0.066, 0.225)          # PROVISIONAL, arXiv 2607.27410 Eq. 26
BGS = (0.295, 7.942, 0.075)

NODES = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33])
DZ = 0.0005
ZG = np.arange(0, 2.5 + DZ / 2, DZ)
assert all(abs(ZG[int(round(n / DZ))] - n) < 1e-12 for n in NODES)

def omr_of_h(h): return 2.469e-5 * (1 + 0.2271 * 3.046) / h ** 2

# footing -> h at fixed Om
G = 6.67430e-11; C = 2.99792458e8; MPC = 3.0856775814913673e22
RHOC100 = 3 * (1e5 / MPC) ** 2 / (8 * np.pi * G)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def h_footing(fp, om):
    rde = (2 * A0[fp] / C) ** 2 / G
    return np.sqrt(rde / ((1 - om) * RHOC100))

class Model:
    def __init__(self, omr, lya, mutate=False):
        self.omr = omr
        lya = list(lya)
        if mutate: lya[4] = 8.270
        self.aniso = GAL + [tuple(lya)]
        self.bgs = BGS
        self._prep()
    def _prep(self):
        self.zi = np.array([a[1] for a in self.aniso]); self.ii = np.rint(self.zi / DZ).astype(int)
        self.d = np.array([[a[2], a[4]] for a in self.aniso])
        self.Ci = []
        for a in self.aniso:
            c = np.array([[a[3] ** 2, a[6] * a[3] * a[5]], [a[6] * a[3] * a[5], a[5] ** 2]]); self.Ci.append(np.linalg.inv(c))
        self.Ci = np.array(self.Ci)
        self.ib = int(round(self.bgs[0] / DZ)); assert abs(ZG[self.ib] - self.bgs[0]) < 1e-12
    def E2(self, om, xn):
        X = np.interp(ZG, NODES, np.r_[1.0, xn])
        return om * (1 + ZG) ** 3 + self.omr * (1 + ZG) ** 4 + (1 - om - self.omr) * X
    def dist(self, om, xn):
        e2 = self.E2(om, xn)
        if np.any(e2 <= 1e-6): return None, None
        f = 1 / np.sqrt(e2)
        I = np.r_[0, np.cumsum(0.5 * (f[1:] + f[:-1]) * DZ)]
        return I, f
    def bao(self, om, xn, I=None, f=None):
        if I is None:
            I, f = self.dist(om, xn)
            if I is None: return 1e9, None
        m = np.c_[I[self.ii], f[self.ii]]
        z = self.bgs[0]; mv = (z * I[self.ib] ** 2 * f[self.ib]) ** (1 / 3)
        num = np.einsum("ni,nij,nj->", m, self.Ci, self.d) + mv * self.bgs[1] / self.bgs[2] ** 2
        den = np.einsum("ni,nij,nj->", m, self.Ci, m) + mv * mv / self.bgs[2] ** 2
        q = num / den; r = self.d - q * m
        return float(np.einsum("ni,nij,nj->", r, self.Ci, r) + ((self.bgs[1] - q * mv) / self.bgs[2]) ** 2), q
    def model_vector(self, om, xn):
        """Replace BAO data by own model (q from bao fit) keeping the errors (KA2)."""
        I, f = self.dist(om, xn); _, q = self.bao(om, xn, I, f)
        self.d = q * np.c_[I[self.ii], f[self.ii]]
        z = self.bgs[0]; self.bgs = (z, q * (z * I[self.ib] ** 2 * f[self.ib]) ** (1 / 3), self.bgs[2])

# ---- Pantheon+ ----
SN = None
def load_sn():
    global SN
    names = open(os.path.join(EXT, "PantheonPlusSH0ES.dat")).readline().split()
    raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
    cov = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); n = int(round(np.sqrt(cov.size))); cov = cov.reshape(n, n)
    sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
    zhd, zhel, mb = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float)
    Cs = cov[np.ix_(sel, sel)]
    L = np.linalg.cholesky(Cs); W = np.linalg.inv(L)             # whitening
    w1 = W @ np.ones(len(mb))
    # linear-interp weights of zhd on ZG
    j = np.floor(zhd / DZ).astype(int); t = (zhd - ZG[j]) / DZ
    SN = dict(W=W, w1=w1, A=w1 @ w1, mb=mb, zhel=zhel, j=j, t=t, n=int(sel.sum()))
def sn(I):
    s = SN; D = I[s["j"]] * (1 - s["t"]) + I[s["j"] + 1] * s["t"]
    r = s["W"] @ (s["mb"] - 5 * np.log10((1 + s["zhel"]) * D)); b = s["w1"] @ r
    return float(r @ r - b * b / s["A"])

def chi2(M, which, om, xn):
    if not (0.15 <= om <= 0.45): return 1e9
    I, f = M.dist(om, xn)
    if I is None: return 1e9
    c = M.bao(om, xn, I, f)[0]
    if which == "T2": c += sn(I)
    return c

NM = dict(maxiter=40000, maxfev=40000, xatol=1e-7, fatol=1e-8)
PW = dict(maxiter=40000, xtol=1e-7, ftol=1e-10)
def polish(fun, x0):
    r = minimize(fun, x0, method="Nelder-Mead", options=NM)
    r = minimize(fun, r.x, method="Powell", options=PW)
    r = minimize(fun, r.x, method="Nelder-Mead", options=NM)
    return r

STARTS = [np.ones(5), np.linspace(1, 0.7, 5), np.linspace(1, 1.3, 5), np.linspace(1.2, 3.0, 5),
          np.array([1.3, 1.9, 2.1, 3.4, 7.0]), np.array([1.0, 1.0, 0.9, 0.6, 0.2])]

def free_fixed_om(M, which, om):
    best = None
    for s in STARTS:
        r = polish(lambda x: chi2(M, which, om, x), s)
        if best is None or r.fun < best.fun: best = r
    return best

def free_om(M, which):
    best = None
    for om0 in (0.25, 0.30, 0.35):
        for s in STARTS[:5]:
            r = polish(lambda p: chi2(M, which, p[0], p[1:]), np.r_[om0, s])
            if best is None or r.fun < best.fun: best = r
    return best

def const_om(M, which):
    r = minimize_scalar(lambda om: chi2(M, which, om, np.ones(5)), bounds=(0.15, 0.45), method="bounded", options=dict(xatol=1e-8))
    return r

class Profile:
    """chi2 with X5 fixed, nodes 1-4 re-minimised (om fixed, or free if om is None). Warm starts from previous best."""
    def __init__(self, M, which, om, x_free):
        self.M, self.which, self.om = M, which, om; self.cache = {}
        self.base = np.array(x_free)[:-1]                     # params other than X5 (4 nodes, or Om + 4 nodes)
        self.default = np.ones(4) if om is not None else np.r_[0.30, np.ones(4)]
        self.warm = [self.base.copy()]
    def __call__(self, x5):
        x5 = float(x5); k = round(x5, 10)
        if k in self.cache: return self.cache[k][0]
        if self.om is not None: fun = lambda p: chi2(self.M, self.which, self.om, np.r_[p, x5])
        else: fun = lambda p: chi2(self.M, self.which, p[0], np.r_[p[1:], x5])
        best = None
        for s in self.warm[-2:] + [self.base, self.default]:
            r = polish(fun, np.array(s, float))
            if best is None or r.fun < best.fun: best = r
        self.warm.append(np.array(best.x))
        self.cache[k] = (float(best.fun), np.r_[best.x, x5].tolist())
        return float(best.fun)

def E2_rival(omr, om): return om * 3.33 ** 3 + omr * 3.33 ** 4 + (1 - om - omr)

def grade_cell(M, which, om):
    """Returns dict for one cell. om None = Om profiled (reported only)."""
    if om is None:
        fr = free_om(M, which); xf = fr.x; x5f = xf[-1]
    else:
        fr = free_fixed_om(M, which, om); xf = fr.x; x5f = xf[-1]
    P = Profile(M, which, om, xf)
    P(x5f)
    bm = minimize_scalar(P, bounds=(0.81, 1.21), method="bounded", options=dict(xatol=1e-4))
    grid = sorted(set(np.round(np.r_[np.arange(-1.0, 4.01, 0.25), np.linspace(x5f - 0.5, x5f + 0.5, 11)], 6)))
    prof = {float(g): P(g) for g in grid}
    xr = E2_rival(M.omr, om if om is not None else 0.30)
    crival = P(xr)
    chi_min = min([fr.fun] + [v[0] for v in P.cache.values()])
    gap = min(v[0] for v in P.cache.values()) - fr.fun        # KA3: profile min - free fit
    # best X5 from the profile (lowest evaluated) and from the free fit
    kbest = min(P.cache, key=lambda k: P.cache[k][0])
    x5best = kbest if P.cache[kbest][0] < fr.fun else x5f
    D_band = float(bm.fun - chi_min); D_rival = float(crival - chi_min)
    d = {g: v - chi_min for g, v in prof.items()}
    ok95 = [g for g, v in d.items() if v <= 3.84]
    out = dict(om=om, omr=M.omr, chi2_free=float(fr.fun), chi2_min=float(chi_min), free_nodes=list(map(float, xf)),
               X5_best=float(x5best), sqrtX_best=float(np.sqrt(max(x5best, 0))), D_band=D_band,
               X5_at_band_min=float(bm.x), X5_rival=float(xr), D_rival=D_rival, KA3_gap=float(gap),
               KA3_pass=bool(gap > -0.1 and gap < 0.1 + 1e9), X5_grid95=[min(ok95), max(ok95)] if ok95 else None,
               chi2_X1=float(chi2(M, which, om, np.ones(5))) if om is not None else None)
    # KA3 as frozen: profile minimum within 0.1 of the free fit (either sign)
    out["KA3_pass"] = bool(abs(gap) <= 0.1)
    out["label"] = label(D_band, D_rival)
    return out

def label(Db, Dr):
    if Db >= 9: return "FLAT FAILS"
    if Db < 4 and Dr < 4: return "NO POWER"
    if Db < 4: return "FLAT HOLDS"
    return "FLAT HOLDS (HINT)"

def ap_T3(M):
    def c(om):
        I, f = M.dist(om, np.ones(5)); s = 0
        for a, i in zip(M.aniso, M.ii):
            F = a[2] / a[4]; sF = F * np.sqrt((a[3] / a[2]) ** 2 + (a[5] / a[4]) ** 2 - 2 * a[6] * a[3] * a[5] / (a[2] * a[4]))
            s += ((F - I[i] / f[i]) / sF) ** 2
        return s
    r = minimize_scalar(c, bounds=(0.15, 0.45), method="bounded", options=dict(xatol=1e-8))
    return float(r.fun), float(r.x)

def run_ka1():
    M = Model(omr_of_h(0.68), LYA_OLD); load_sn(); res = {}
    for which in ("T1", "T2"):
        c0 = const_om(M, which); f1 = free_om(M, which)
        res[which] = dict(chi2_const=float(c0.fun), om_const=float(c0.x), chi2_free=float(f1.fun), free=list(map(float, f1.x)),
                          dchi2=float(c0.fun - f1.fun), fixed={})
        for om in (0.25, 0.30, 0.35):
            g = free_fixed_om(M, which, om)
            res[which]["fixed"][str(om)] = dict(chi2=float(g.fun), X5=float(g.x[-1]), sqrtX=float(np.sqrt(max(g.x[-1], 0))))
        print(which, json.dumps(res[which]), flush=True)
    res["T3"] = dict(zip(("chi2", "om"), ap_T3(M)))
    tgt = dict(T1=(7.41, [1.93, 1.14, 0.00]), T2=(12.08, [1.97, 1.24, 0.00]))
    chk = {}
    for w in ("T1", "T2"):
        chk[w + "_dchi2"] = abs(res[w]["dchi2"] - tgt[w][0]) <= 0.10
        for om, t in zip(("0.25", "0.3", "0.35"), tgt[w][1]): chk[f"{w}_sqrtX_{om}"] = abs(res[w]["fixed"][om]["sqrtX"] - t) <= 0.05
    chk["T3"] = abs(res["T3"]["chi2"] - 5.98) <= 0.05
    res["checks"] = chk; res["KA1_pass"] = bool(all(chk.values()))
    return res

def run_grade(fp, mutate):
    load_sn(); res = dict(footing=fp, mutate=mutate, cells={})
    # KA2 (flat injection, T1, Om 0.30, this footing's Or, new-pair errors)
    if not mutate:
        Mk = Model(omr_of_h(h_footing(fp, 0.30)), LYA_NEW); Mk.model_vector(0.30, np.ones(5))
        k = grade_cell(Mk, "T1", 0.30)
        res["KA2"] = dict(D_band=k["D_band"], sqrtX_best=k["sqrtX_best"], chi2_min=k["chi2_min"],
                          pass_=bool(k["D_band"] < 0.05 and abs(k["sqrtX_best"] - 1) <= 0.03))
        print("KA2", json.dumps(res["KA2"]), flush=True)
    for which in ("T1", "T2"):
        for om in (0.25, 0.30, 0.35):
            M = Model(omr_of_h(h_footing(fp, om)), LYA_NEW, mutate)
            c = grade_cell(M, which, om); c["h"] = float(h_footing(fp, om))
            res["cells"][f"{which}_{om}"] = c
            print(which, om, json.dumps({k: c[k] for k in ("h", "chi2_free", "chi2_min", "sqrtX_best", "D_band", "X5_at_band_min", "X5_rival", "D_rival", "KA3_gap", "KA3_pass", "X5_grid95", "label")}), flush=True)
        M = Model(omr_of_h(h_footing(fp, 0.30)), LYA_NEW, mutate)      # Om-profiled row, reported only (Or at Om 0.30's h)
        c = grade_cell(M, which, None); res["cells"][f"{which}_omfree"] = c
        print(which, "Om free", json.dumps({k: c[k] for k in ("chi2_free", "free_nodes", "sqrtX_best", "D_band", "D_rival", "KA3_gap", "X5_grid95")}), flush=True)
    hl = res["cells"]["T2_0.3"]["label"]
    others = [res["cells"][f"T2_{o}"]["label"] for o in (0.25, 0.35)]
    ka3 = all(res["cells"][f"{w}_{o}"]["KA3_pass"] for w in ("T1", "T2") for o in (0.25, 0.3, 0.35))
    res["KA3_all_pass"] = bool(ka3)
    res["headline"] = hl + (" / EXPANSION-MODEL DEPENDENT" if any(o != hl for o in others) else "")
    print("HEADLINE", res["headline"], "KA3 all", ka3, flush=True)
    return res

if __name__ == "__main__":
    if MODE == "KA1": r = run_ka1()
    else:
        fp = MODE.split("_")[0]; r = run_grade(fp, MODE.endswith("MUTATE"))
    json.dump(r, open(os.path.join(HERE, f"azr_{MODE}.json"), "w"), indent=1, default=float)
    print("done", MODE)
