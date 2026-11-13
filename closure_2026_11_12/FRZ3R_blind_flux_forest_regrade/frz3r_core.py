#!/usr/bin/env python3
"""FRZ3R core: halo-model tables (FRZ1's layout, executed read-only), field realisation, gas, flux, statistics.
Own code (blind re-grade of the forest row at flux level). kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, io, math, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
import scipy.fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("FRZ3R_REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ1 = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z", "frz1_hm.py")
WORKERS = 4
CLIGHT = 299792.458

# ------------------------------------------------------------------ halo model (FRZ1's code, prefix executed read-only)
_NS = None
def frz1():
    global _NS
    if _NS is None:
        src = open(FRZ1).read(); cut = src.index("# ------------------------------------------------------------------ checkpointed run")
        ns = {"__file__": FRZ1, "__name__": "frz1_lib_frz3r"}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], "frz1_hm", "exec"), ns)
        _NS = ns
    return _NS

KT = np.concatenate([[0.0], np.geomspace(1e-3, 400.0, 900)])     # h/Mpc, table grid for U(k)

def Uk(L, r, Mc, k):
    dM = np.diff(Mc); rm = 0.5 * (r[1:] + r[:-1]); x = np.outer(k, rm)
    j0 = np.where(x > 1e-6, np.sin(x) / np.maximum(x, 1e-30), 1.0)
    return Mc[0] + j0 @ dM

def hm_tables(z, foot, lmin=8.0, lmax=15.0):
    """per grid mass: W (number density per slot), bias, U_std, U_Lta, U_Rb, U_B on KT; plus FRZ1-convention R_cold on KK."""
    ns = frz1(); L = ns["L"]; ns["set_z"](z); layout = ns["layout"]
    LM = L["LM"]; sel = (LM >= lmin - 1e-9) & (LM <= lmax + 1e-9)
    idx = np.nonzero(sel)[0]
    out = dict(lM=LM[idx], M=L["MM"][idx], W=L["W_M"][idx], b=L["BIAS"][idx], RHO=L["RHO_M"], D=ns["S"]["D"])
    U = {k: np.empty((len(idx), len(KT))) for k in ("std", "Lta", "Rb", "B")}
    for j, i in enumerate(idx):
        hb = L["HB"][i]
        r = L["rgrid"](hb, hb["r200"]); U["std"][j] = Uk(L, r, L["M_L"](hb, r), KT)
        for key, mode in (("Lta", "L"), ("Rb", "Rb"), ("B", "B")):
            r, Mc, _ = layout(hb, foot, mode=mode); U[key][j] = Uk(L, r, Mc, KT)
    out["U"] = U
    # FRZ1 convention (whole mass grid) for reference
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLt, _, _ = L["spectra_ta"](UL)
    UB, _ = L["U_set"](lambda hb: layout(hb, foot, mode="B")); PB, _, _ = L["spectra_ta"](UB)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    out["KK"] = L["KK"].copy(); out["R_cold"] = (1 + (PB - PLt) / Pstd) / (1 + (PR - PLt) / Pstd)
    out["Pstd_Rbar"] = Pstd + (PR - PLt); out["A_MISS"] = L["A_MISS"]
    out["Plin_fn"] = (lambda k, D=ns["S"]["D"]: L["P_lin"](k) * D * D)
    return out

def matched_C(Uref, UB, URb):
    """effective difference profile: (Uref + C)^2 - Uref^2 = UB^2 - URb^2 per mass and k (READING section 2)."""
    s = Uref ** 2 + UB ** 2 - URb ** 2
    return -Uref + np.sqrt(np.maximum(s, 0.0)), int(np.sum(s < 0))

# ------------------------------------------------------------------ grid helpers
class Grid:
    def __init__(self, N, Lbox):
        self.N, self.L = N, Lbox; self.dx = Lbox / N
        kf = 2 * np.pi * sfft.fftfreq(N, d=self.dx).astype(np.float32); kz = 2 * np.pi * sfft.rfftfreq(N, d=self.dx).astype(np.float32)
        self.kx = kf[:, None, None]; self.ky = kf[None, :, None]; self.kz = kz[None, None, :]
        self.k = np.sqrt(self.kx ** 2 + self.ky ** 2 + self.kz ** 2).astype(np.float32)
        s = lambda q: np.sinc(q * self.dx / (2 * np.pi))
        self.wcic = (s(self.kx) * s(self.ky) * s(self.kz)) ** 2
        self.wcic = np.maximum(self.wcic, 0.05).astype(np.float32)
        # interpolation index into KT (linear in ln k; k = 0 handled by KT[0] = 0 node)
        kk = self.k.ravel(); lk = np.log(np.maximum(kk, 1e-30)); lt = np.log(np.maximum(KT, 1e-30))
        i = np.clip(np.searchsorted(KT, kk) - 1, 0, len(KT) - 2)
        w = np.where(i == 0, kk / KT[1], (lk - lt[i]) / (lt[i + 1] - lt[i]))
        self.ti = i.astype(np.int32); self.tw = np.clip(w, 0, 1).astype(np.float32)
    def on_grid(self, Ut):
        return ((1 - self.tw) * Ut[self.ti] + self.tw * Ut[self.ti + 1]).reshape(self.k.shape).astype(np.float32)
    def rfft(self, a): return sfft.rfftn(a, workers=WORKERS)
    def irfft(self, a): return sfft.irfftn(a, s=(self.N,) * 3, workers=WORKERS).astype(np.float32)

def cic(grid, pos):
    N = grid.N; x = pos / grid.dx - 0.5; i0 = np.floor(x).astype(np.int64); f = (x - i0).astype(np.float64)
    out = np.zeros(N ** 3, np.float64)
    for dx_ in (0, 1):
        wx = f[:, 0] if dx_ else 1 - f[:, 0]; ix = (i0[:, 0] + dx_) % N
        for dy_ in (0, 1):
            wy = f[:, 1] if dy_ else 1 - f[:, 1]; iy = (i0[:, 1] + dy_) % N
            for dz_ in (0, 1):
                wz = f[:, 2] if dz_ else 1 - f[:, 2]; iz = (i0[:, 2] + dz_) % N
                out += np.bincount((ix * N + iy) * N + iz, weights=wx * wy * wz, minlength=N ** 3)
    return out.reshape(N, N, N).astype(np.float32)

# ------------------------------------------------------------------ profile sets per footing (READING section 2)
def prepare(tab, PstdRbar_on_KT):
    """adds: ref, C1 (matched 1-halo), dU (plain), expected 1h_ref, D2h (FRZ1 two-halo difference) on KT."""
    ns = frz1(); L = ns["L"]; U = tab["U"]; W = tab["W"]; rho = tab["RHO"]; b = tab["b"]
    tab["ref"] = U["std"] + U["Rb"] - U["Lta"]
    tab["C1"], tab["n_neg"] = matched_C(tab["ref"], U["B"], U["Rb"])
    tab["dU"] = U["B"] - U["Rb"]
    tab["p1_ref"] = np.sum(W[:, None] * (tab["ref"] / rho) ** 2, 0)
    tab["PstdRbar_KT"] = PstdRbar_on_KT
    return tab

def frz1_curves_on_KT(z, foot):
    """FRZ1-convention spectra on the long table grid KT (whole FRZ1 mass grid): P_std R_bar and the two-halo part of P_B - P_Rb."""
    ns = frz1(); L = ns["L"]; ns["set_z"](z); layout = ns["layout"]; KKs = L["KK"]
    L["KK"] = KT[1:].copy(); L["PL"] = L["P_lin"](L["KK"]) * ns["S"]["D"] ** 2
    try:
        Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
        UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLt, _, _ = L["spectra_ta"](UL)
        UB, _ = L["U_set"](lambda hb: layout(hb, foot, mode="B")); PB, p1B, IB = L["spectra_ta"](UB)
        UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, p1R, IR = L["spectra_ta"](UR)
        PSR = Pstd + PR - PLt; D2 = L["PL"] * (IB ** 2 - IR ** 2); D1 = p1B - p1R
    finally:
        L["KK"] = KKs; L["PL"] = L["P_lin"](KKs) * ns["S"]["D"] ** 2
    pad = lambda a: np.concatenate([[a[0]], a])
    return pad(PSR), pad(D2), pad(D1)

# ------------------------------------------------------------------ realisation
def white(grid, seed):
    return grid.rfft(np.random.default_rng(seed).standard_normal((grid.N,) * 3).astype(np.float32))

def lognormal_smooth(grid, wk, PT_KT):
    """lognormal field with target power PT (on KT): Gaussian power from xi_G = ln(1 + xi_T) on the grid. Returns (delta_k, G_k, info)."""
    N, V = grid.N, grid.L ** 3
    PT = grid.on_grid(PT_KT); PT.flat[0] = 0.0
    xiT = sfft.irfftn(PT.astype(np.float64), s=(N,) * 3, workers=WORKERS) * N ** 3 / V
    xi_min = float(xiT.min())
    xiG = np.log1p(np.maximum(xiT, -0.999)); del xiT
    PG = sfft.rfftn(xiG, workers=WORKERS).real * V / N ** 3; del xiG
    nneg = int(np.sum(PG < 0)); PG = np.maximum(PG, 0.0); PG.flat[0] = 0.0
    Gk = (wk * np.sqrt(PG / grid.dx ** 3)).astype(np.complex64); del PG
    G = grid.irfft(Gk); s2 = float(np.var(G, dtype=np.float64))
    e = np.exp(G.astype(np.float64) - 0.5 * s2); e /= e.mean()
    dk = grid.rfft((e - 1.0).astype(np.float32)); dk.flat[0] = 0.0
    return dk, Gk, dict(sigG2=s2, xiT_min=xi_min, PG_neg_modes=nneg)

def halo_parts(grid, tab, seed, keys, dlog=0.1, cluster_G=None, Rf=0.5):
    """Poisson halo catalogue on 0.1 dex painting bins (count-weighted mean profile per bin); positions uniform (primary) or
    ~ exp(b G_f) (clustered bracket). Accumulates the k-space density contrast of the halo part for every profile set in keys
    in one pass (positions shared). Returns ({key: complex grid}, painted mass of 'ref', n halos)."""
    rng = np.random.default_rng(7919 + seed)
    N, V = grid.N, grid.L ** 3
    lM, W, b = tab["lM"], tab["W"], tab["b"]
    edges = np.arange(8.0 - 1e-9, lM[-1] + dlog, dlog); bid = np.digitize(lM, edges) - 1
    if cluster_G is not None:
        gf = grid.irfft(cluster_G * np.exp(-0.5 * (grid.k * Rf) ** 2)).ravel().astype(np.float64)
    acc = {k: np.zeros(grid.k.shape, np.complex64) for k in keys}; Mh = 0.0; ntot = 0
    for ib in range(bid.max() + 1):
        m = bid == ib; Ne_i = W[m] * V; Ne = float(Ne_i.sum())
        if Ne <= 0: continue
        n = int(rng.poisson(Ne))
        if n == 0: continue
        wts = Ne_i / Ne
        if cluster_G is None:
            pos = rng.random((n, 3)) * grid.L
        else:
            bb = float(np.sum(wts * b[m])); lw = bb * gf; lw -= lw.max(); p = np.exp(lw); p /= p.sum()
            cells = rng.choice(N ** 3, size=n, p=p)
            pos = (np.stack(np.unravel_index(cells, (N,) * 3), 1) + rng.random((n, 3))) * grid.dx
        nk = grid.rfft(cic(grid, pos)) / grid.wcic
        for key in keys:
            Ut = np.sum(wts[:, None] * tab[key][m], 0)
            acc[key] += nk * (grid.on_grid(Ut) / (tab["RHO"] * grid.dx ** 3))
            if key == "ref": Mh += n * Ut[0]
        ntot += n; del nk
    return acc, Mh, ntot

def build_fields(grid, tab, seed, clustered=False, which=("R", "BM", "BP", "BM2", "BM0")):
    """k-space density contrasts. R = reference; BM = matched graded field; BP = plain painting (reported);
    BM2 = matched difference doubled (mutation M2); BM0 = matched difference x 0 through the same path (known answer a)."""
    V = grid.L ** 3; RHO = tab["RHO"]
    wk = white(grid, seed)
    f_h_exp = float(np.sum(tab["W"] * tab["M"])) / RHO          # expected painted mass fraction (U_ref(0) = M)
    fs_exp = 1.0 - f_h_exp
    S = np.maximum(tab["PstdRbar_KT"] - tab["p1_ref"], 1e-12)
    dsk, Gk, linfo = lognormal_smooth(grid, wk, S / fs_exp ** 2); del wk
    keys = ["ref", "C1"] + (["dU"] if "BP" in which else [])
    acc, Mh, nh = halo_parts(grid, tab, seed, keys, cluster_G=Gk if clustered else None)
    fs = 1.0 - Mh / (RHO * V)
    T2m1 = grid.on_grid(np.sqrt(np.maximum(1.0 + tab["D2h_KT"] / S, 0.0))) - 1.0
    info = dict(fs=fs, fs_exp=fs_exp, n_halo=nh, **linfo)
    base = acc["ref"] + fs * dsk
    dM = acc["C1"] + fs * dsk * T2m1
    out = {}
    for w in which:
        if w == "R": fk = base.copy()
        elif w == "BM": fk = base + dM
        elif w == "BM2": fk = base + 2.0 * dM
        elif w == "BM0": fk = base + 0.0 * dM
        elif w == "BP": fk = base + acc["dU"]
        fk.flat[0] = 0.0; out[w] = fk
    del acc, base, dM
    return out, Gk, info

# ------------------------------------------------------------------ gas, flux, P1D
def gas(grid, fk, lam):
    g = grid.irfft(fk * np.exp(-0.5 * (grid.k * lam) ** 2).astype(np.float32)) + 1.0
    return g

def los_velocity(grid, Gk, z, PL_KT, PG_proxy=None):
    """linear-theory LOS (axis 2) peculiar velocity in km/s from the smooth field's Gaussian G (bracket only)."""
    ns = frz1(); L = ns["L"]; Om = L["Om"]
    a = 1 / (1 + z); Ez = math.sqrt(Om * (1 + z) ** 3 + 1 - Om); f = (Om * (1 + z) ** 3 / Ez ** 2) ** 0.55
    k2 = np.maximum(grid.k ** 2, 1e-12)
    vk = 1j * a * 100.0 * Ez * f * grid.kz / k2 * Gk          # km/s (comoving Mpc/h with H in h km/s/Mpc)
    vk.flat[0] = 0.0
    return grid.irfft(vk.astype(np.complex64))

def dv_cell(grid, z):
    ns = frz1(); Om = ns["L"]["Om"]; Ez = math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
    return 100.0 * Ez / (1 + z) * grid.dx                       # km/s per cell (h cancels)

def tau_field(grid, rho, z, beta, gam, T0=1.0e4, broaden=True, vlos=None, nclass=12):
    """FGPA optical depth per pixel (unit amplitude), thermal broadening with b(T) in nclass classes of log b (class-centre b),
    optional redshift-space shift along axis 2 (CIC along the line of sight). Ringing below 0 is clipped."""
    N = grid.N; dv = dv_cell(grid, z)
    t = np.power(rho, np.float32(beta), dtype=np.float32)
    if not broaden and vlos is None: return t
    if broaden:
        lb = (math.log(12.85 * math.sqrt(T0 / 1e4)) + 0.5 * (gam - 1) * np.log(rho)).astype(np.float32)
        edges = np.linspace(float(lb.min()) - 1e-6, float(lb.max()) + 1e-6, nclass + 1)
        cls = (np.digitize(lb, edges) - 1).astype(np.int8); del lb
    else:
        edges = np.array([-50.0, -49.0]); cls = np.zeros(rho.shape, np.int8); nclass = 1
    if vlos is not None:
        sh = vlos / np.float32(dv) + np.arange(N, dtype=np.float32)[None, None, :]
        i0 = np.floor(sh).astype(np.int64); fr = (sh - i0).astype(np.float32); del sh
        base = (np.arange(N, dtype=np.int64)[:, None, None] * N + np.arange(N, dtype=np.int64)[None, :, None]) * N
        f0 = (base + i0 % N).ravel(); f1 = (base + (i0 + 1) % N).ravel(); del i0, base
    kk = 2 * np.pi * sfft.rfftfreq(N, d=1.0)
    out = np.zeros((N, N, N // 2 + 1), np.complex64)
    for c in range(nclass):
        m = cls == c
        if not m.any(): continue
        bc = math.exp(0.5 * (edges[c] + edges[c + 1])) / dv if broaden else 0.0
        src = np.where(m, t, np.float32(0.0)); del m
        if vlos is not None:
            src = (np.bincount(f0, weights=(src * (1 - fr)).ravel(), minlength=N ** 3)
                   + np.bincount(f1, weights=(src * fr).ravel(), minlength=N ** 3)).reshape(N, N, N).astype(np.float32)
        out += sfft.rfft(src, axis=2, workers=WORKERS) * np.exp(-0.25 * (kk * bc) ** 2).astype(np.float32)[None, None, :]
        del src
    return np.maximum(sfft.irfft(out, n=N, axis=2, workers=WORKERS), 0.0).astype(np.float32)   # FFT ringing clipped at 0

def tune_A(tau1, Fbar, linear=False):
    t = tau1.astype(np.float64).ravel()
    if linear: return (1 - Fbar) / t.mean()
    lo, hi = -30.0, 15.0
    sub = t[:: max(1, t.size // 2_000_000)]
    from scipy.optimize import brentq
    f = lambda la, x: float(np.mean(np.exp(-math.exp(la) * x))) - Fbar
    la0 = brentq(lambda la: f(la, sub), lo, hi, xtol=1e-8)
    la = brentq(lambda la: f(la, t), la0 - 0.2, la0 + 0.2, xtol=1e-12)
    return math.exp(la)

def p1d(grid, z, dF):
    N = grid.N; dv = dv_cell(grid, z)
    Fk = sfft.rfft(dF.astype(np.float64), axis=2, workers=WORKERS)
    p = (np.abs(Fk) ** 2).mean(axis=(0, 1)) * dv / N
    kv = 2 * np.pi * sfft.rfftfreq(N, d=dv)
    return kv, p

def flux_p1d(grid, rho, z, beta, gam, Fbar, broaden=True, vlos=None, mode="exp"):
    """mode exp: F = exp(-A tau); lin: F = 1 - A tau (mutation M1); thin: exp with 1 - <F> = 1e-7."""
    t1 = tau_field(grid, rho, z, beta, gam, broaden=broaden, vlos=vlos)
    if mode == "lin":
        A = tune_A(t1, Fbar, linear=True); F = 1.0 - A * t1.astype(np.float64)
    elif mode == "thin":
        A = 1e-7 / float(t1.astype(np.float64).mean()); F = np.exp(-A * t1.astype(np.float64))
    else:
        A = tune_A(t1, Fbar); F = np.exp(-A * t1.astype(np.float64))
    mF = float(F.mean())
    kv, p = p1d(grid, z, F / mF - 1.0)
    return kv, p, dict(A=A, meanF=mF)
def pk3d(grid, fk, nbins=40, kmin=0.3, kmax=None):
    kmax = kmax or 0.9 * np.pi / grid.dx
    w = np.full(grid.k.shape, 2.0, np.float32); w[:, :, 0] = 1.0
    if grid.N % 2 == 0: w[:, :, -1] = 1.0
    e = np.geomspace(kmin, kmax, nbins + 1); kc = np.sqrt(e[1:] * e[:-1])
    ib = np.digitize(grid.k.ravel(), e) - 1; ok = (ib >= 0) & (ib < nbins)
    p = np.abs(fk.ravel()) ** 2 * w.ravel()
    s = np.bincount(ib[ok], weights=p[ok], minlength=nbins); c = np.bincount(ib[ok], weights=w.ravel()[ok], minlength=nbins)
    return kc, s / np.maximum(c, 1) * grid.dx ** 6 / grid.L ** 3
