#!/usr/bin/env python3
"""SRF1R (READING.md, cc3d45432d) stage 1: flux-level response of the settled layout, per (variant, z, seed, footing).
Background B = smooth lognormal (target P_2h / f_s^2) + light haloes (Poisson, Rb profiles, CIC, k-space); heavy haloes
(>= 10^10.8 Msun/h) inserted one at a time with importance weights w = N_true / K on skewers around them (reference = B +
g_R, settled = B + g_R + dg_f). FGPA with thermal broadening (16 log-b classes), mean flux matched on B, linear-response
retune eps for the settled field. Part files parts/<variant>_<foot>_z<z>_s<seed>.json (restartable; SIGTERM -> exit 75).
  nice -n 19 python3 srf1r_flux.py <variant> <foot|both> <z> <seed>     (variants: P, M1, M2, B1..B10)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
import scipy.fft as sf
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = [False]
def _term(sig, frm): STOP[0] = True
signal.signal(signal.SIGTERM, _term)

L = 20.0; H0H = 100.0
OM = 0.3138                       # replaced from the table run below (CFG556's Om is written into the part file)
FB_A, FB_N = 0.751, 2.90
T0 = 1.0e4; NCLS = 16; BLO, BHI = 2.0, 800.0
KMIN_PER_BIN, KMAX_PER_BIN = 16, 32                  # AMENDMENT A1 item 3
VARIANTS = {
    "P": dict(), "M1": dict(linear=True, fsub=[1.0, 2.0]), "M2": dict(fsub=[1.0], rset2=True),
    "B1": dict(lam="half"), "B2": dict(lam="dbl"), "B3": dict(lam="pk100"), "B4": dict(gamma=1.2), "B5": dict(gamma=1.6),
    "B6": dict(teff=0.9), "B7": dict(teff=1.1), "B8": dict(clustered=True), "B9": dict(N=256), "B10": dict(tcap=1e5)}
BR_F = [0.70, 1.00, 1.25, 1.60, 2.00, 3.00]           # AMENDMENT A1 item 4

def Ez(z, Om): return math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
def Fbar(z, teff_fac=1.0): return math.exp(-teff_fac * (FB_A * ((1 + z) / 4.5) ** FB_N - 0.132))

def broaden(t0, b, dv):
    """t0, b: (n, N) arrays; Gaussian exp(-v^2/b^2) per log-b class along axis 1 (periodic)."""
    n, N = t0.shape; kv = 2 * math.pi * np.fft.rfftfreq(N, d=dv)
    w = (math.log10(BHI) - math.log10(BLO)) / NCLS
    cls = np.clip(np.floor((np.log10(np.maximum(b, 1e-3)) - math.log10(BLO)) / w), 0, NCLS - 1).astype(np.int8)
    out = np.zeros((n, N), np.float32)
    for c in np.unique(cls):
        bc = 10 ** (math.log10(BLO) + (c + 0.5) * w)
        tc = np.where(cls == c, t0, 0.0)
        out += sf.irfft(sf.rfft(tc, axis=1) * np.exp(-kv ** 2 * bc ** 2 / 4).astype(np.float32)[None, :], n=N, axis=1)
    return np.maximum(out, 0.0)

def tau_unit(gas, beta, gamma, dv, tcap):
    T = T0 * gas ** (gamma - 1)
    if tcap: T = np.minimum(T, tcap)
    return broaden(gas ** beta, 12.85 * np.sqrt(T / 1e4), dv)

def flux(tau1, A, linear):
    A = np.float32(A) if tau1.dtype == np.float32 else A
    return np.float32(1.0) - A * tau1 if (linear and tau1.dtype == np.float32) else (1.0 - A * tau1 if linear else np.exp(-A * tau1))

def p1d_sum(dF):
    """sum over skewers of |FFT|^2 (float64)."""
    X = sf.rfft(dF, axis=1); return np.sum(X.real.astype(np.float64) ** 2 + X.imag.astype(np.float64) ** 2, axis=0)

# ---------------------------------------------------------------- worker state (fork-shared)
W_ = {}
def work(chunk):
    gas = W_["gas"]; N = gas.shape[0]; cell = L / N; c = W_["cfg"]; T = W_["tab"]
    zc = (np.arange(N) + 0.5) * cell; A, Fb = W_["A"], W_["Fbar"]
    nf = len(W_["fidx"]); nk = N // 2 + 1
    dP = np.zeros((nf, nk)); dF = np.zeros(nf); dPref = np.zeros(nk); grp = np.zeros((nf, 3, nk))
    lam = T["lam"]; cid = T["lamc"]
    for (x, y, zh, j, w) in chunk:
        rta = T["rta"][j]; reval = T["REV"][j]
        RD = rta + 4 * lam + cell
        R_atts = [T["RSET"][j, q] + 4 * lam + cell if T["RSET"][j, q] > 0 else -1.0 for q in W_["fidx"]]
        RDref = RD if W_["ref_full"] else max(max(R_atts), 0.0)
        RDmax = max(RDref, max(R_atts))
        m = int(math.ceil(RDmax / cell)) + 1
        ix0 = int(math.floor(x / cell)); iy0 = int(math.floor(y / cell))
        ii = np.arange(ix0 - m, ix0 + m + 1); jj = np.arange(iy0 - m, iy0 + m + 1)
        dx = (ii + 0.5) * cell - x; dy = (jj + 0.5) * cell - y
        d2 = dx[:, None] ** 2 + dy[None, :] ** 2
        sel = d2 <= RDmax ** 2
        if not sel.any(): continue
        I, J = np.nonzero(sel); DD = np.sqrt(d2[I, J]); GI = ii[I] % N; GJ = jj[J] % N
        dz = zc - zh; dz -= L * np.round(dz / L)
        g = 0 if T["lM"][j] < 12 else (1 if T["lM"][j] < 13 else 2)
        for b0 in range(0, len(DD), 2048):
            dd = DD[b0:b0 + 2048]; gi = GI[b0:b0 + 2048]; gj = GJ[b0:b0 + 2048]
            r = np.sqrt(dd[:, None] ** 2 + dz[None, :] ** 2).astype(np.float32)
            gB = gas[gi, gj, :]
            gR = np.maximum(gB + np.interp(r, reval, T["gR"][j, cid], right=0.0).astype(np.float32), np.float32(1e-6))
            FR = flux(tau_unit(gR, c["beta"], c["gamma"], c["dv"], c["tcap"]), A, c["linear"])
            inref = dd <= RDref
            if inref.any():
                tB = tau_unit(np.maximum(gB[inref], 1e-6), c["beta"], c["gamma"], c["dv"], c["tcap"])
                dPref += w * (p1d_sum(FR[inref] / Fb - 1) - p1d_sum(flux(tB, A, c["linear"]) / Fb - 1))
            for a, q in enumerate(W_["fidx"]):
                if R_atts[a] <= 0: continue
                s2 = dd <= R_atts[a]
                if not s2.any(): continue
                dgv = np.interp(r[s2], reval, T["dg"][j, q, cid], right=0.0)
                gS = np.maximum(gR[s2] + dgv.astype(np.float32), np.float32(1e-6))
                FS = flux(tau_unit(gS, c["beta"], c["gamma"], c["dv"], c["tcap"]), A, c["linear"])
                v = w * (p1d_sum(FS / Fb - 1) - p1d_sum(FR[s2] / Fb - 1))
                dP[a] += v; grp[a, g] += v; dF[a] += w * float(np.sum(FS - FR[s2], dtype=np.float64))
    return dP, dF, dPref, grp

# ---------------------------------------------------------------- one part
def run_part(var, foot, z, seed):
    vc = VARIANTS[var]; N = vc.get("N", 384); cell = L / N
    tag = f"{var}_{foot}_z{z:.1f}_s{seed}"; out = os.path.join(HERE, "parts", tag + ".json")
    if os.path.exists(out): return
    t0 = time.time()
    Z = np.load(os.path.join(HERE, "tables", f"tab_{foot}_z{z:.1f}.npz"))
    OmL = float(json.load(open(os.path.join(HERE, "tables", "cosmo.json")))["Om"])
    LAMK = list(Z["LAMK"]); lk = vc.get("lam", "p"); lam = float(Z["LAMV"][LAMK.index(lk)]); cid = LAMK.index(lk)
    gamma = vc.get("gamma", 1.5); beta = 2 - 0.7 * (gamma - 1); tcap = vc.get("tcap"); linear = vc.get("linear", False)
    vfac = H0H * Ez(z, OmL) / (1 + z); dv = cell * vfac; Lv = N * dv
    Fb = Fbar(z, vc.get("teff", 1.0))
    FGRID = list(Z["FGRID"])
    if "fsub" in vc: flist = vc["fsub"]
    elif var.startswith("B"): flist = BR_F
    elif seed == 0: flist = FGRID if round(z, 1) == 2.2 else [f for f in FGRID if f < 4.0]   # A1, A2, A3 item 2
    else: flist = [0.0, 0.70, 1.00, 1.25, 1.60, 2.00, 3.00]                             # A3 item 3 (seed scatter)
    fidx = [FGRID.index(f) if f in FGRID else int(np.argmin([abs(x - f) for x in FGRID])) for f in flist]
    if vc.get("rset2"): fidx = [FGRID.index(2.0)]
    # ---- k grid and white noise (seed only)
    kx = 2 * math.pi * sf.fftfreq(N, d=cell); kz = 2 * math.pi * sf.rfftfreq(N, d=cell)
    K = np.sqrt(kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2).astype(np.float32)
    Vc = cell ** 3
    Wk = sf.rfftn(np.random.default_rng(seed).standard_normal((N, N, N), dtype=np.float32), workers=4)
    KT = Z["KTAB"]
    def onk(tab):
        return np.interp(K.ravel(), KT, tab).reshape(K.shape).astype(np.float32)
    PT = onk(Z["P2h"] / float(Z["fs"]) ** 2); PT.flat[0] = 0.0
    xi = sf.irfftn(PT, s=(N, N, N), workers=4) / Vc; del PT
    xiG = np.log1p(np.maximum(xi, -0.99)).astype(np.float32); del xi
    PG = np.maximum(sf.rfftn(xiG, workers=4).real * Vc, 0.0).astype(np.float32); del xiG
    Gk = Wk * np.sqrt(PG / Vc); del PG
    Gx = sf.irfftn(Gk, s=(N, N, N), workers=4); sG2 = float(np.var(Gx))
    fs = float(Z["fs"]); mx = (fs * np.exp(Gx - 0.5 * sG2)).astype(np.float32)
    # ---- light haloes (Poisson per 0.1 dex bin; same draws for both footings: seeded by seed and z)
    rng = np.random.default_rng(1000 + seed * 37 + int(round(z * 10)))
    lM, Wm = Z["lM"], Z["W"]; li = Z["light_idx"]; Ul = Z["URt_light"]
    RHO = float(json.load(open(os.path.join(HERE, "tables", "cosmo.json")))["RHO_M"])
    V = L ** 3; wc = np.ones_like(K)
    s1 = lambda kk: np.sinc(kk * cell / (2 * math.pi))
    wc = (s1(kx)[:, None, None] * s1(kx)[None, :, None] * s1(kz)[None, None, :]) ** 2
    wc = np.maximum(wc, 0.1).astype(np.float32)
    Hk = np.zeros(K.shape, np.complex64); bins = np.floor((lM[li] - 8.0) / 0.1 + 1e-9).astype(int); nlight = 0
    for b in np.unique(bins):
        ms = li[bins == b]; nexp = float(np.sum(Wm[ms])) * V; n = rng.poisson(nexp)
        if n == 0: continue
        pos = rng.random((n, 3)) * L; nlight += n
        Ub = np.sum(Wm[ms][:, None] * Ul[bins == b], 0) / np.sum(Wm[ms])
        g = pos / cell - 0.5; i0 = np.floor(g).astype(int); fr = g - i0
        grid = np.zeros(N ** 3, np.float32)
        for ox in (0, 1):
            for oy in (0, 1):
                for oz in (0, 1):
                    wt = (fr[:, 0] if ox else 1 - fr[:, 0]) * (fr[:, 1] if oy else 1 - fr[:, 1]) * (fr[:, 2] if oz else 1 - fr[:, 2])
                    idx = (((i0[:, 0] + ox) % N) * N + (i0[:, 1] + oy) % N) * N + (i0[:, 2] + oz) % N
                    grid += np.bincount(idx, weights=wt, minlength=N ** 3).astype(np.float32)
        Hk += sf.rfftn(grid.reshape(N, N, N), workers=4) / wc * onk(Ub / (RHO * Vc))
    mk = sf.rfftn(mx, workers=4) + Hk; del Hk, mx
    # matter 3D power of B (40 log bins 0.3 to 40 h/Mpc)
    kb = np.geomspace(0.3, 40.0, 41); P3 = np.abs(mk) ** 2 * Vc / N ** 3
    wt2 = np.ones(K.shape, np.float32); wt2[:, :, 1:-1 if N % 2 == 0 else None] = 2.0
    ib = np.digitize(K.ravel(), kb) - 1; ok = (ib >= 0) & (ib < 40)
    P3b = np.bincount(ib[ok], weights=(P3.ravel() * wt2.ravel())[ok], minlength=40) / np.maximum(np.bincount(ib[ok], weights=wt2.ravel()[ok], minlength=40), 1)
    kc = np.sqrt(kb[1:] * kb[:-1]); del P3, wt2, ib, ok
    mean_m = float(mk.flat[0].real) / N ** 3
    gas = sf.irfftn(mk * np.exp(-K ** 2 * lam ** 2 / 2), s=(N, N, N), workers=4).astype(np.float32)
    floor_frac = float(np.mean(gas < 1e-6)); gas = np.maximum(gas, 1e-6)
    Gsm = None
    if vc.get("clustered"):
        Rs = 0.5; Gsm = sf.irfftn(Gk * np.exp(-K ** 2 * Rs ** 2 / 2), s=(N, N, N), workers=4)
    del Gk
    # ---- full-grid flux of B
    tau1 = np.empty((N, N, N), np.float32); SL = 16
    for a in range(0, N, SL):
        g2 = gas[a:a + SL].reshape(-1, N).astype(np.float64)
        tau1[a:a + SL] = tau_unit(g2, beta, gamma, dv, tcap).reshape(-1, N, N).astype(np.float32)
    if linear:
        A = (1 - Fb) / float(np.mean(tau1, dtype=np.float64))
    else:
        lo, hi = -12.0, 8.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if float(np.mean(np.exp(-math.exp(mid) * tau1), dtype=np.float64)) > Fb: lo = mid
            else: hi = mid
        A = math.exp(0.5 * (lo + hi))
    Fm = float(np.mean(flux(tau1, A, linear), dtype=np.float64))
    nk = N // 2 + 1; PB = np.zeros(nk); PE = np.zeros(nk); AtF = 0.0; e0 = 1e-3
    for a in range(0, N, SL):
        t2 = tau1[a:a + SL].reshape(-1, N).astype(np.float64); F0 = flux(t2, A, linear); F1 = flux(t2, A * (1 + e0), linear)
        PB += p1d_sum(F0 / Fb - 1); PE += p1d_sum(F1 / Fb - 1)
        AtF += float(np.sum(A * t2 * (F0 if not linear else 1.0)))
    Nsk = N * N; norm = Lv / N ** 2
    PB *= norm / Nsk; dPde = (PE * norm / Nsk - PB) / e0; AtF /= Nsk * N
    del tau1
    # ---- heavy haloes: sample (same for both footings; seeded by seed and z)
    rh = np.random.default_rng(2000 + seed * 41 + int(round(z * 10)))
    hidx = Z["heavy_idx"]; lMh = lM[hidx]; Wh = Wm[hidx]; bns = np.floor((lMh - 10.8) / 0.1 + 1e-9).astype(int)
    halos = []
    if Gsm is not None:
        Gsm = (Gsm - Gsm.mean()) / Gsm.std(); sl = float(json.load(open(os.path.join(HERE, "tables", "cosmo.json")))["sig_lin_0p5"][f"{z:.1f}"])
    for b in np.unique(bns):
        js = np.where(bns == b)[0]; Nt = float(np.sum(Wh[js])) * V
        if Nt <= 0: continue
        Kb = KMIN_PER_BIN if Nt < KMIN_PER_BIN else KMAX_PER_BIN; w = Nt / Kb
        pj = Wh[js] / np.sum(Wh[js]); jsel = rh.choice(js, size=Kb, p=pj)
        if Gsm is None:
            pos = rh.random((Kb, 3)) * L
        else:
            bias = float(np.sum(Wh[js] * Z["BIAS"][hidx][js]) / np.sum(Wh[js]))
            pr = np.exp(bias * sl * Gsm.ravel().astype(np.float64)); cp = np.cumsum(pr); cp /= cp[-1]
            ci = np.searchsorted(cp, rh.random(Kb)); ci = np.minimum(ci, N ** 3 - 1)
            ijk = np.stack(np.unravel_index(ci, (N, N, N)), 1); pos = (ijk + rh.random((Kb, 3))) * cell
        for p_, j in zip(pos, jsel): halos.append((float(p_[0]), float(p_[1]), float(p_[2]), int(j), float(w)))
    del Gsm
    del K, Wk, mk, wc, Gx
    T = dict(rta=Z["rta"], REV=Z["REV"], gR=Z["gR"], dg=Z["dg"], RSET=Z["RSET"][:, :len(FGRID)].copy(), lM=lMh, lam=lam, lamc=cid)
    if vc.get("rset2"):
        T["RSET"][:, FGRID.index(2.0)] = Z["RSET"][:, FGRID.index(2.0)]
    W_.update(gas=gas, cfg=dict(beta=beta, gamma=gamma, dv=dv, tcap=tcap, linear=linear), tab=T, A=A, Fbar=Fb, fidx=fidx,
              ref_full=False)                                   # AMENDMENT A1 item 1
    order = sorted(range(len(halos)), key=lambda i: -T["rta"][halos[i][3]])
    chunks = [[halos[i] for i in order[k::32]] for k in range(32)]
    dP = np.zeros((len(fidx), nk)); dF = np.zeros(len(fidx)); dPref = np.zeros(nk); grp = np.zeros((len(fidx), 3, nk))
    with get_context("fork").Pool(4) as pool:
        if os.environ.get("SRF1R_TIMING"):                         # timing only: no part written, no statistic
            t1 = time.time(); work(chunks[0]); print(f"TIMING one chunk of 32: {time.time() - t1:.1f} s; bg {t1 - t0:.0f} s", flush=True); sys.exit(0)
        for r_ in pool.imap_unordered(work, chunks):
            dP += r_[0]; dF += r_[1]; dPref += r_[2]; grp += r_[3]
            if STOP[0]:
                pool.terminate(); print("SIGTERM: part not written; rerun to resume", flush=True); sys.exit(75)
    dP *= norm / Nsk; grp *= norm / Nsk; dPref *= norm / Nsk; dF /= Nsk * N
    eps = dF / AtF
    Pref = PB                                                      # AMENDMENT A1 item 1
    RF = 1 + (dP + eps[:, None] * dPde[None, :]) / Pref[None, :]
    kv = 2 * math.pi * np.arange(nk) / Lv
    res = dict(variant=var, foot=foot, z=z, seed=seed, N=N, lam=lam, gamma=gamma, tcap=tcap, linear=linear, Fbar=Fb, A=A,
               meanF_B=Fm, meanF_relerr=abs(Fm - Fb) / Fb, floor_frac=floor_frac, mean_m=mean_m, n_light=nlight, n_heavy=len(halos),
               f=[FGRID[q] if not vc.get("rset2") else "Rset_x2_at_f1" for q in fidx], kv=kv.tolist(), P1D_B=PB.tolist(), dP1D_ref=dPref.tolist(),
               dPde=dPde.tolist(), AtauF=AtF, dP=dP.tolist(), dFbar=dF.tolist(), eps=eps.tolist(), R_F=RF.tolist(),
               dP_groups_lt12_12to13_gt13=grp.tolist(), P3_B=P3b.tolist(), k3=kc.tolist(), sec=time.time() - t0,
               note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
    json.dump(res, open(out + ".tmp", "w"), default=lambda o: None if o is None or (isinstance(o, float) and math.isinf(o)) else str(o))
    os.replace(out + ".tmp", out)
    print(f"[{tag}] done: A {A:.4g}, <F> err {res['meanF_relerr']:.1e}, heavy {len(halos)}, light {nlight}, floor {floor_frac:.1e}  [{time.time() - t0:.0f} s]", flush=True)

if __name__ == "__main__":
    var, foot, z, seed = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    for ft in (("canonical", "alt") if foot == "both" else (foot,)):
        run_part(var, ft, z, seed)
        if STOP[0]: sys.exit(75)
