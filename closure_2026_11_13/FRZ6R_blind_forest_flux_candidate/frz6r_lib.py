#!/usr/bin/env python3
"""FRZ6R library (FROZEN_CRITERIA.md, 4314f23c90): halo-model tables for the crossing-speed split, box realisation, gas, flux,
forest data. Own code except: the record's halo model and layouts (FZS1's fzs1_hm.py prefix, which runs FRZ1's frz1_hm.py prefix
and CFG556's library, executed read-only), and the FGPA step REUSED unchanged from FRZ3R's frz3r_core.py (tau_field, tune_A, p1d,
dv_cell). Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, math, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
import scipy.fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORKERS = 2
FZS1 = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius", "fzs1_hm.py")
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion", "ss1_cosmo.py")
FOOTS = ("canonical", "alt")
ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
ANCH = (2.2, 3.0, 4.4)
CLIGHT = 299792.458

# ------------------------------------------------------------------ the record's layouts (read-only)
_Z = None
def rec():
    global _Z
    if _Z is None:
        code = open(FZS1).read(); cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
        Z = {"__file__": FZS1, "__name__": "fzs1_lib_frz6r"}
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], FZS1, "exec"), Z)
        _Z = Z
    return _Z

# ------------------------------------------------------------------ FGPA step reused from FRZ3R (unchanged)
_C = None
def core():
    global _C
    if _C is None:
        sys.path.insert(0, FRZ3R)
        import frz3r_core as C
        sys.path.pop(0)
        C.WORKERS = WORKERS; _C = C
    return _C

# ------------------------------------------------------------------ the split's boundary (own implementation of the definition)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MPC = 3.0856775814913673e22; H0_SI = 67.4e3 / MPC; XS = 5.41; OL = 0.6847
def vstar(foot, z):
    return A0[foot] / (10.0 * (1.0 + XS) * H0_SI) / 1e3 / math.sqrt((1 - OL) * (1 + z) ** 3 + OL)

def split_fn(foot, z, f, vst):
    """reference layout for v_vir > vst; else the law's cold component rescaled inside R_set = f R_fold, reference beyond."""
    Z = rec(); F = Z["F"]; layout, Bar, rset_com, CUR = Z["layout"], Z["Bar"], Z["rset_com"], Z["CUR"]
    def fn(hb):
        CUR[0] = 0.0
        if F["v_vir"](hb) > vst: return layout(hb, foot, mode="Rb")
        R = rset_com(hb, foot, z, f)
        if R <= 0: return layout(hb, foot, mode="Rb")
        CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
        if inf["regime"] == "L": return rR, MR, inf
        assert np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(np.abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, s=float(s), R_set=R)
    return fn

KT = np.concatenate([[0.0], np.geomspace(4e-3, 160.0, 720)])
def tables(z, cases):
    """cases: {name: (kind, f, vst_mode)}; kind 'R' | 'C' | 'J'. Returns per footing: U (masses x KT), p1, I, P on KT, plus
    population (lM, M, W, Mta) and the count above v*."""
    Z = rec(); F, L = Z["F"], Z["L"]; layout, CUR = Z["layout"], Z["CUR"]
    Z["set_z"](z); D = F["S"]["D"]
    KKs, PLs = L["KK"], L["PL"]
    L["KK"] = KT.copy(); L["PL"] = L["P_lin"](np.maximum(KT, 1e-5)) * D * D
    out = {}
    try:
        for ft in FOOTS:
            vs = vstar(ft, z)
            t = dict(vstar=vs, n_above=int(sum(1 for hb in L["HB"] if F["v_vir"](hb) > vs)), n=len(L["HB"]),
                     lM=np.log10(L["MM"]), M=L["MM"].copy(), W=L["W_M"].copy(), RHO=L["RHO_M"], PL=L["PL"].copy(), U={}, I={}, P={}, p1={})
            for name, (kind, f, vm) in cases.items():
                CUR[0] = 0.0
                if kind == "R": fn = lambda hb: layout(hb, ft, mode="Rb")
                elif kind == "C": fn = lambda hb: layout(hb, ft, mode="B")
                else: fn = split_fn(ft, z, f, {"main": vs, "inf": math.inf, "zero": 0.0}[vm])
                U, _ = L["U_set"](fn); CUR[0] = 0.0
                P, p1, I = L["spectra_ta"](U)
                t["U"][name] = U; t["P"][name] = P; t["p1"][name] = p1; t["I"][name] = I
            t["Mta"] = t["U"]["R"][:, 0].copy()
            out[ft] = t
    finally:
        L["KK"] = KKs; L["PL"] = PLs
    return out

# ------------------------------------------------------------------ box (own)
class Box:
    def __init__(self, N=384, Lbox=20.0):
        self.N, self.L = N, Lbox; self.dx = Lbox / N
        kf = (2 * np.pi * sfft.fftfreq(N, d=self.dx)).astype(np.float32); kr = (2 * np.pi * sfft.rfftfreq(N, d=self.dx)).astype(np.float32)
        kx, ky, kz = kf[:, None, None], kf[None, :, None], kr[None, None, :]
        self.k = np.sqrt(kx * kx + ky * ky + kz * kz).astype(np.float32)
        w = lambda q: np.sinc(q * self.dx / (2 * np.pi)).astype(np.float32) ** 3       # TSC window per axis
        self.wtsc = np.maximum(w(kx) * w(ky) * w(kz), np.float32(0.01))
        kk = self.k.ravel(); j = np.clip(np.searchsorted(KT, kk, side="right") - 1, 0, len(KT) - 2)
        self.j = j.astype(np.int32); self.u = ((kk - KT[j]) / (KT[j + 1] - KT[j])).clip(0, 1).astype(np.float32)
    def tab(self, T):
        T = np.asarray(T, np.float32); a = T[self.j]; b = T[self.j + 1]; b -= a; b *= self.u; a += b; del b
        return a.reshape(self.k.shape)
    def rfft(self, a): return sfft.rfftn(a, workers=WORKERS)
    def irfft(self, a): return sfft.irfftn(a, s=(self.N,) * 3, workers=WORKERS).astype(np.float32)

def tsc_deposit(box, pos):
    """triangular-shaped-cloud counts; cell i has its centre at (i + 0.5) dx."""
    N = box.N; x = pos / box.dx - 0.5; i0 = np.rint(x).astype(np.int64); d = x - i0
    w = [0.5 * (0.5 - d) ** 2, 0.75 - d ** 2, 0.5 * (0.5 + d) ** 2]
    out = np.zeros(N ** 3, np.float32)
    for a in range(3):
        ix = (i0[:, 0] + a - 1) % N; wa = w[a][:, 0]
        for b in range(3):
            iy = (i0[:, 1] + b - 1) % N; wb = wa * w[b][:, 1]
            for c in range(3):
                iz = (i0[:, 2] + c - 1) % N
                idx = (ix * N + iy) * N + iz; o = np.argsort(idx, kind="stable"); u_, st = np.unique(idx[o], return_index=True)
                out[u_] += np.add.reduceat((wb * w[c][:, 2])[o], st).astype(np.float32)
    return out.reshape(N, N, N)

def streams(iz, s):
    ss = np.random.SeedSequence([6, 61, iz, s]); a, b = ss.spawn(2)
    return np.random.default_rng(a), np.random.default_rng(b)

def realise(box, TT, iz, seed, names):
    """both footings at once (shared white noise, counts, positions). Returns {foot: {name: delta_k}}, info."""
    N, V = box.N, box.L ** 3
    rw, rh = streams(iz, seed)
    t0 = TT[FOOTS[0]]; lM, W = t0["lM"], t0["W"]
    edges = 8.0 + 0.125 * np.arange(0, 66); bid = np.digitize(lM + 1e-9, edges) - 1
    acc = {ft: {nm: np.zeros(box.k.shape, np.complex64) for nm in names} for ft in FOOTS}
    Mp = {ft: 0.0 for ft in FOOTS}; nh = 0
    for ib in range(bid.max() + 1):
        m = np.nonzero(bid == ib)[0]
        if len(m) == 0: continue
        cnt = rh.poisson(W[m] * V)
        n = int(cnt.sum())
        if n == 0: continue
        pos = rh.random((n, 3)) * box.L
        dk = box.rfft(tsc_deposit(box, pos)) / box.wtsc
        for ft in FOOTS:
            T = TT[ft]; Mp[ft] += float(np.sum(cnt * T["Mta"][m]))
            for nm in names:
                Ub = (cnt[:, None] * T["U"][nm][m]).sum(0) / n
                g = box.tab(Ub / (T["RHO"] * box.dx ** 3)); g = dk * g; acc[ft][nm] += g; del g
        nh += n; del dk
    # smooth component: lognormal, target S / fs_exp^2, S = P_lin I_R^2
    wk = box.rfft(rw.standard_normal((N,) * 3).astype(np.float32))
    out = {}; info = dict(n_halo=nh)
    for ft in FOOTS:
        T = TT[ft]; S = T["PL"] * T["I"]["R"] ** 2
        fs_exp = 1.0 - float(np.sum(T["W"] * T["Mta"])) / T["RHO"]; fs = 1.0 - Mp[ft] / (T["RHO"] * V)
        PT = box.tab(S / fs_exp ** 2); PT.flat[0] = 0.0
        xi = sfft.irfftn(PT.astype(np.float64), s=(N,) * 3, workers=WORKERS) * N ** 3 / V; del PT
        xmin = float(xi.min()); xi = np.log1p(np.maximum(xi, -0.999))
        PG = sfft.rfftn(xi, workers=WORKERS).real * V / N ** 3; del xi
        nneg = int(np.sum(PG < 0)); PG = np.maximum(PG, 0.0); PG.flat[0] = 0.0
        G = box.irfft((wk * np.sqrt(PG / box.dx ** 3)).astype(np.complex64)); del PG
        s2 = float(np.var(G, dtype=np.float64)); e = np.exp(G.astype(np.float64) - 0.5 * s2); e /= e.mean(); del G
        dsk = box.rfft((e - 1.0).astype(np.float32)); del e
        dsk.flat[0] = 0.0
        out[ft] = {}
        for nm in names:
            fac = box.tab(np.abs(T["I"][nm] / T["I"]["R"])) if nm != "R" else np.float32(1.0)
            fk = acc[ft][nm] + np.float32(fs) * dsk * fac; fk.flat[0] = 0.0; out[ft][nm] = fk
            acc[ft][nm] = None
        info[ft] = dict(fs=fs, fs_exp=fs_exp, sigG2=s2, xiT_min=xmin, PG_neg=nneg, M_painted=Mp[ft])
        del dsk
    del wk
    return out, info

def pk3d(box, fk, kc=(1.0, 3.0, 5.0)):
    """binned 3D power in 24 log bins from 0.3 to 0.9 k_Nyq; returned with the bin centres."""
    kmax = 0.9 * np.pi / box.dx; e = np.geomspace(0.3, kmax, 25); c = np.sqrt(e[1:] * e[:-1])
    w = np.full(box.k.shape, 2.0, np.float32); w[:, :, 0] = 1.0; w[:, :, -1] = 1.0
    ib = np.digitize(box.k.ravel(), e) - 1; ok = (ib >= 0) & (ib < 24)
    p = (np.abs(fk.ravel()) ** 2 * w.ravel())[ok]
    s = np.bincount(ib[ok], weights=p, minlength=24); n = np.bincount(ib[ok], weights=w.ravel()[ok], minlength=24)
    return c, s / np.maximum(n, 1) * box.dx ** 6 / box.L ** 3

# ------------------------------------------------------------------ gas and flux
LAM0 = 0.079 * 0.6736          # 79 comoving kpc in Mpc/h
def lam_kpc(x): return x * 1e-3 * 0.6736
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132
def beta_of(g): return 2.0 - 0.7 * (g - 1.0)

def gas(box, fk, lam):
    g = box.irfft(fk * np.exp(-0.5 * (box.k * np.float32(lam)) ** 2).astype(np.float32)) + np.float32(1.0)
    fl = float(np.mean(g < 1e-6)); return np.maximum(g, np.float32(1e-6)), fl

def flux_p1d(box, rho, z, gam=1.5, stau=1.0):
    C = core()
    t1 = C.tau_field(box, rho, z, beta_of(gam), gam)
    Fb = math.exp(-stau * tau_eff(z)); A = C.tune_A(t1, Fb)
    F = np.exp(-A * t1.astype(np.float64)); mF = float(F.mean()); del t1
    kv, p = C.p1d(box, z, F / mF - 1.0); del F
    return kv, p, dict(A=A, meanF=mF, target=Fb)

# ------------------------------------------------------------------ forest data (the record's forest_setup, read-only)
def forest_data():
    import hashlib, tarfile
    from scipy.linalg import cho_factor
    src = open(SS1).read(); a = src.index("def forest_setup():"); b = src.index("KF = np.exp(", a)
    ns = dict(os=os, io=io, math=math, np=np, hashlib=hashlib, tarfile=tarfile, cho_factor=cho_factor, REPO=REPO, CLIGHT=CLIGHT)
    exec(compile(src[a:b], "ss1_forest_setup", "exec"), ns)
    return ns["forest_setup"]()
