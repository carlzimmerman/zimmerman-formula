#!/usr/bin/env python3
"""FRZ3: paired painted fields and the transmitted flux (FROZEN_CRITERIA.md). One part file per (z, seed):
parts/z<z>_s<seed>.json. Restartable (finished parts are skipped); SIGTERM exits cleanly between parts.
Usage: nice -n 19 python3 frz3_fields.py <mode> <z list comma> <seed list comma>   mode: anchor | primary
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*matmul.*")
import numpy as np, scipy.fft as sf
from scipy.interpolate import CubicSpline
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frz3_layout as F

MODE = sys.argv[1]; assert MODE in ("anchor", "primary", "MUTATE_lowres")
ZS = [float(x) for x in sys.argv[2].split(",")]; SEEDS = [int(x) for x in sys.argv[3].split(",")]
PARTS = os.path.join(HERE, os.environ.get("FRZ3_PARTS", "parts")); os.makedirs(PARTS, exist_ok=True)
FLOOR = float(os.environ.get("FRZ3_FLOOR", "1e-3"))     # A1 floor; A2 floor-off check sets 1e-9
STOP = {"flag": False}
def _term(s, f): STOP["flag"] = True; print("SIGTERM: stopping after the current part", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, _term)

# ------------------------------------------------------------------ frozen settings (FROZEN_CRITERIA.md section 2)
LBOX, NG = 20.0, 384; VC = (LBOX / NG) ** 3; DX = LBOX / NG
STRIDE = 8
T0, GAM = 1.2e4, 1.4
LAMP_KPC = 80.0                                     # pressure smoothing, proper kpc (field filter exp(-k^2 lam^2 / 2))
def lam_c(z, fac=1.0): return fac * LAMP_KPC * 1e-3 * (1 + z) * F.h          # comoving Mpc/h
def Fbar(z): return math.exp(-(0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132))   # Becker et al. 2013 tau_eff (PROVISIONAL)
FOOTS = ("canonical", "alt")
KU = np.geomspace(0.01, 160.0, 800)
PBINS = np.geomspace(0.3, 35.0, 51)

kx = (2 * np.pi * np.fft.fftfreq(NG, d=DX)).astype(np.float32); kz = (2 * np.pi * np.fft.rfftfreq(NG, d=DX)).astype(np.float32)
KMAG = np.sqrt(kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2).astype(np.float32)
def sinc(x): return np.sinc(x / np.pi)
WCIC = (sinc(kx * DX / 2)[:, None, None] ** 2 * sinc(kx * DX / 2)[None, :, None] ** 2 * sinc(kz * DX / 2)[None, None, :] ** 2).astype(np.float32)
KFINE = np.geomspace(0.1, 130.0, 6000)
_lf = (np.log(np.maximum(KMAG, KFINE[0])) - math.log(KFINE[0])) / math.log(KFINE[1] / KFINE[0])
KIDX = np.clip(np.floor(_lf), 0, len(KFINE) - 2).astype(np.int32); KW = np.clip(_lf - KIDX, 0, 1).astype(np.float32); del _lf
def ugrid(Uf): return Uf[KIDX] * (1 - KW) + Uf[KIDX + 1] * KW          # linear in ln k on the fine grid (not nearest)
PIDX = np.digitize(KMAG, PBINS).astype(np.int32)          # 0 below the first edge; bin j = j - 1
PCNT = np.bincount(PIDX.ravel(), minlength=len(PBINS) + 1)[1:len(PBINS)]
# rfft half-plane weights (modes with 0 < kz < Nyquist count twice)
WHALF = np.full(len(kz), 2.0, np.float32); WHALF[0] = 1.0; WHALF[-1] = 1.0
PNW = np.bincount(PIDX.ravel(), weights=np.broadcast_to(WHALF[None, None, :], KMAG.shape).ravel(), minlength=len(PBINS) + 1)[1:len(PBINS)]

def pk_binned(dk):
    p = np.abs(dk) ** 2; p *= WHALF[None, None, :]
    s = np.bincount(PIDX.ravel(), weights=p.ravel(), minlength=len(PBINS) + 1)[1:len(PBINS)]
    return (s / np.maximum(PNW, 1) * VC ** 2 / LBOX ** 3).tolist()

def skewers(real):
    a = real[:, ::STRIDE, ::STRIDE].reshape(NG, -1).T
    b = real[::STRIDE, :, ::STRIDE].transpose(0, 2, 1).reshape(-1, NG)
    c = real[::STRIDE, ::STRIDE, :].reshape(-1, NG)
    return np.concatenate([a, b, c]).astype(np.float64)

def broaden(tau, Delta, dv, gam):
    """tau(v_j) = sum_i tau_i dv / (sqrt(pi) b_i) exp(-((v_j - v_i) / b_i)^2), periodic; b = 12.85 sqrt(T / 1e4 K) km/s."""
    b = 12.85 * np.sqrt(T0 * Delta ** (gam - 1) / 1e4)
    K = int(min(NG // 2 - 1, math.ceil(5.0 * float(b.max()) / dv)))
    amp = tau * dv / (math.sqrt(math.pi) * b); nib2 = -(dv * dv) / b ** 2
    out = amp.copy()
    for m in range(1, K + 1):
        e = amp * np.exp(m * m * nib2)
        out += np.roll(e, m, axis=1); out += np.roll(e, -m, axis=1)
    return out

def solve_A(tt, fb):
    lo, hi = -40.0, 25.0
    for _ in range(80):
        mid = 0.5 * (lo + hi); m = np.mean(np.exp(-math.exp(mid) * tt))
        if m > fb: lo = mid
        else: hi = mid
    A = math.exp(0.5 * (lo + hi)); return A, float(np.mean(np.exp(-A * tt)))

def p1d(dfield):
    fk = np.fft.rfft(dfield, axis=1); return (np.mean(np.abs(fk[:, 1:NG // 2 + 1]) ** 2, axis=0)).tolist()

def flux_set(g, z, dv, gam=GAM, thin=False):
    """g: skewers of 1 + delta_gas. Returns flux P1D, the matched A and mean flux, and the tau P1D (saturation removed)."""
    nfl = int((g < FLOOR).sum()); g = np.maximum(g, FLOOR)              # amendments A1, A2: floor (also touches the deepest lognormal voids)
    if thin:
        tt = g.copy(); fb = 1 - 1e-7
    else:
        beta = 2 - 0.7 * (gam - 1); tt = broaden(g ** beta, g, dv, gam); fb = Fbar(z)
    A, mf = solve_A(tt, fb); Fx = np.exp(-A * tt)
    out = dict(A=A, meanF=mf, target=fb, P_F=p1d(Fx / Fx.mean() - 1), n_floored=nfl, frac_floored=nfl / g.size)
    if not thin: out["P_tau"] = p1d(tt / tt.mean() - 1)
    return out

def one(z, seed):
    fn = os.path.join(PARTS, f"z{z:.1f}_s{seed}.json")
    if os.path.exists(fn): print("skip", fn, flush=True); return
    t0 = time.time(); res = dict(lane="FRZ3", z=z, seed=seed, mode=MODE, NG=NG, LBOX=LBOX, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    dv = DX * 100 * F.Ez(z) / (1 + z); res["dv_kms"] = dv
    res["kpar_skm"] = (2 * np.pi * np.arange(1, NG // 2 + 1) / (NG * dv)).tolist()
    rng = np.random.default_rng(seed)
    wk = sf.rfftn(rng.standard_normal((NG, NG, NG), dtype=np.float32), workers=4)
    PLk = F.plin(np.maximum(KMAG, 1e-4), z).astype(np.float32)
    def smooth_field(lfac):
        dG = sf.irfftn(wk * np.sqrt(PLk / VC) * np.exp(-0.5 * KMAG ** 2 * lam_c(z, lfac) ** 2), s=(NG, NG, NG), workers=4)
        s2 = float(dG.var()); one_p = np.exp(dG - 0.5 * s2); one_p /= one_p.mean()
        return one_p.astype(np.float32), s2
    sm, s2 = smooth_field(1.0); res["sigmaG2"] = s2
    # catalogue: Poisson counts per mass point, painting bins of 2 mass points (0.05 dex), biased positions
    Bc = {f: F.build(z, f, KU) for f in FOOTS}
    W, bias, Mta = Bc["canonical"]["W"], Bc["canonical"]["bias"], Bc["canonical"]["Mta"]
    Ncnt = rng.poisson(W * LBOX ** 3)
    lsm = np.log(sm.ravel().astype(np.float64))
    bins = [list(range(i, min(i + 2, len(F.MM)))) for i in range(0, len(F.MM), 2)]
    cat = []
    for bi in bins:
        n = int(Ncnt[bi].sum())
        if n == 0: continue
        bb = float(np.sum(Ncnt[bi] * bias[bi]) / n)
        q = np.exp(bb * (lsm - lsm.max())); cq = np.cumsum(q)
        cells = np.searchsorted(cq, rng.random(n) * cq[-1]); cells = np.minimum(cells, NG ** 3 - 1)
        ix, iy, iz = np.unravel_index(cells, (NG, NG, NG))
        pos = (np.stack([ix, iy, iz], 1) + rng.random((n, 3))) * DX
        cat.append((bi, n, pos))
    res["n_halo"] = int(sum(c[1] for c in cat)); res["n_paint_bins"] = len(cat)
    Mhalo = float(sum(np.sum(Ncnt[bi] * Mta[bi]) for bi, n, p in cat)); fs = 1 - Mhalo / (F.RHO * LBOX ** 3); res["f_smooth"] = fs
    assert fs > 0.05, fs
    def cic(pos):
        g = np.zeros((NG, NG, NG), np.float32); u = pos / DX - 0.5; i0 = np.floor(u).astype(np.int64); f1 = (u - i0).astype(np.float32)
        for dx_ in (0, 1):
            for dy_ in (0, 1):
                for dz_ in (0, 1):
                    w = (f1[:, 0] if dx_ else 1 - f1[:, 0]) * (f1[:, 1] if dy_ else 1 - f1[:, 1]) * (f1[:, 2] if dz_ else 1 - f1[:, 2])
                    np.add.at(g, ((i0[:, 0] + dx_) % NG, (i0[:, 1] + dy_) % NG, (i0[:, 2] + dz_) % NG), w)
        return g
    del lsm
    res["t_catalogue"] = time.time() - t0
    FS = sf.rfftn(sm - 1.0, workers=4); del sm
    lams = {"p": 1.0} if MODE == "primary" else {"p": 1.0, "lh": 0.5, "l2": 2.0}
    SMK = {}
    for key, lf in lams.items():
        if key == "p": SMK[key] = FS
        else: SMK[key] = sf.rfftn(smooth_field(lf)[0] - 1.0, workers=4)
    del wk, PLk
    res["foot"] = {}
    for foot in FOOTS:
        B = Bc[foot]
        variants = ["R", "L"] if MODE == "primary" else ["R", "L", "remnfw", "V", "RV", "Lmmin"]
        acc = {v: np.zeros(KMAG.shape, np.complex64) for v in variants}
        for bi, nh, pos in cat:
            ck = sf.rfftn(cic(pos), workers=4) / WCIC                     # count-field transform, CIC window removed
            n = Ncnt[bi]; wts = n / n.sum()
            for v in variants:
                src = "L" if v == "Lmmin" else v
                if v == "Lmmin" and F.LM[bi].mean() < 10.0: src = "R"
                U = np.sum(B["U"][src][bi] * wts[:, None], 0)
                Uf = CubicSpline(np.log(KU), U)(np.log(KFINE)).astype(np.float32)
                acc[v] += ck * (ugrid(Uf) / np.float32(F.RHO * VC))
        R = {}
        # matter power (smooth part + halos, unsmoothed), k = 0 dropped
        mat = {}
        for v in variants:
            dk = fs * FS + acc[v]; dk[0, 0, 0] = 0; mat[v] = pk_binned(dk)
        R["Pm"] = mat; R["Pm_kbins"] = PBINS.tolist(); R["Pm_nmodes"] = PCNT.tolist()
        # gas skewers per smoothing scale and variant
        gs = {}
        for key, lf in lams.items():
            filt = np.exp(-0.5 * KMAG ** 2 * lam_c(z, lf) ** 2).astype(np.float32)
            for v in (variants if key == "p" else ["R", "L"]):
                dk = fs * SMK[key] + acc[v] * filt; dk[0, 0, 0] = 0
                gs[(key, v)] = 1.0 + skewers(sf.irfftn(dk, s=(NG, NG, NG), workers=4))
        del acc
        out = {}
        gR, gL = gs[("p", "R")], gs[("p", "L")]
        assert gR.min() > 0 and gL.min() > 0, (gR.min(), gL.min())
        fields = {"R": gR, "L": gL}
        out["P_gas"] = {k: p1d(v / v.mean() - 1) for k, v in fields.items()}
        out["flux"] = {k: flux_set(v, z, dv) for k, v in fields.items()}
        out["thin"] = {k: flux_set(v, z, dv, thin=True) for k, v in fields.items()}
        out["KAa_zero_diff"] = flux_set(gR + 0.0 * (gL - gR), z, dv)["P_F"]
        if MODE == "anchor":
            g2 = 2 * gL - gR; gV = gR + (gs[("p", "V")] - gs[("p", "RV")])
            ext = {"L2x": g2, "remnfw": gs[("p", "remnfw")], "V": gV, "Lmmin": gs[("p", "Lmmin")]}
            out["P_gas"].update({k: p1d(v / v.mean() - 1) for k, v in ext.items()})
            out["flux"].update({k: flux_set(v, z, dv) for k, v in ext.items()})
            for gk, gv in (("glo", 1.2), ("ghi", 1.6)):
                out["flux_" + gk] = {k: flux_set(v, z, dv, gam=gv) for k, v in fields.items()}
            for key in ("lh", "l2"):
                ff = {"R": gs[(key, "R")], "L": gs[(key, "L")]}
                out["flux_" + key] = {k: flux_set(v, z, dv) for k, v in ff.items()}
                out["P_gas_" + key] = {k: p1d(v / v.mean() - 1) for k, v in ff.items()}
        out["gas_min"] = float(min(gR.min(), gL.min())); out["gas_max"] = float(max(gR.max(), gL.max()))
        R.update(out); res["foot"][foot] = R
        del gs
        print(f"z {z:.1f} seed {seed} {foot} done [{time.time() - t0:.0f}s]", flush=True)
    res["t_total"] = time.time() - t0
    tmp = fn + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, fn)
    print("wrote", os.path.basename(fn), f"{res['t_total']:.0f}s n_halo {res['n_halo']} f_s {fs:.3f}", flush=True)

if __name__ == "__main__":
    for z in ZS:
        for s in SEEDS:
            one(z, s)
