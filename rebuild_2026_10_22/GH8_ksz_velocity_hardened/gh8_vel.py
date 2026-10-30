#!/usr/bin/env python3
"""GH8 velocities: regional randoms, iterative RSD removal, CIC read; forward-matched lognormal catalogue mock for R. Reads no CMB map."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, healpy as hp, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh8_work"); os.makedirs(W, exist_ok=True)
RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
OM, BETA, CELL, RS = 0.3085, 0.44, 6.0, 12.5; zz = np.linspace(0, 1, 4001); EZ = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM)
CHI = np.r_[0, np.cumsum(.5 * (1 / EZ[1:] + 1 / EZ[:-1]) * np.diff(zz))] * 2997.92458
def xyz(ra, de, z):
    c = np.interp(z, zz, CHI); r, d = np.radians(ra), np.radians(de); return np.c_[c * np.cos(d) * np.cos(r), c * np.cos(d) * np.sin(r), c * np.sin(d)].astype(np.float32)
def aH(z): return 100 * np.interp(z, zz, EZ) / (1 + z)
L = 2 * (np.interp(.5, zz, CHI) + 2 * RS); N = int(math.ceil(L / CELL)); N += N % 2; L = N * CELL; print("mesh", N, "box", L, flush=True)
def stencil(P):
    g = (P + L / 2) / CELL - .5; i = np.floor(g).astype(np.int32); f = (g - i).astype(np.float32); return i, f
def cic(P):
    m = np.zeros((N, N, N), np.float32); i, f = stencil(P)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                np.add.at(m, ((i[:, 0] + a) % N, (i[:, 1] + b) % N, (i[:, 2] + c) % N), (f[:, 0] if a else 1 - f[:, 0]) * (f[:, 1] if b else 1 - f[:, 1]) * (f[:, 2] if c else 1 - f[:, 2]))
    return m
def read(F, P):
    i, f = stencil(P); o = np.zeros((len(P), 3), np.float32)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                w = (f[:, 0] if a else 1 - f[:, 0]) * (f[:, 1] if b else 1 - f[:, 1]) * (f[:, 2] if c else 1 - f[:, 2])
                for ax in range(3): o[:, ax] += w * F[ax][(i[:, 0] + a) % N, (i[:, 1] + b) % N, (i[:, 2] + c) % N]
    return o
D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); s = (D["z"] >= .05) & (D["z"] <= .5); ra, de, z = D["ra"][s], D["de"][s], D["z"][s]; Ng = len(z); north = (de > 32.375) & (ra > 90) & (ra < 280); print("tracers", Ng, "north", int(north.sum()), flush=True)
Sg = xyz(ra, de, z); rng = np.random.default_rng(88); NS = 64; PIX = np.sqrt(hp.nside2pixarea(NS, degrees=True)); nr = np.zeros((N, N, N), np.float32)
for reg in (north, ~north):
    ct = np.bincount(hp.ang2pix(NS, ra[reg], de[reg], lonlat=True), minlength=hp.nside2npix(NS)).astype(float); pr = ct / ct.sum(); n = int(reg.sum())
    for _ in range(10):
        p = rng.choice(len(pr), n, p=pr); r0, d0 = hp.pix2ang(NS, p, lonlat=True); d1 = d0 + rng.uniform(-.5, .5, n) * PIX; r1 = r0 + rng.uniform(-.5, .5, n) * PIX / np.maximum(np.cos(np.radians(d0)), .05)
        nr += cic(xyz(r1, d1, rng.choice(z[reg], n)))
nr /= 10.0; occ = nr > 0; mask = nr > 0.1 * nr[occ].mean(); print("mask cells", int(mask.sum()), flush=True); KEEP = mask.mean()
def dens(n):
    d = np.zeros_like(n); a = n[mask].sum() / nr[mask].sum(); d[mask] = n[mask] / (a * nr[mask]) - 1; return d
K = sf.fftfreq(N, CELL / (2 * np.pi)).astype(np.float32); KZ = sf.rfftfreq(N, CELL / (2 * np.pi)).astype(np.float32); KK = K[:, None, None] ** 2 + K[None, :, None] ** 2 + KZ[None, None, :] ** 2; KK[0, 0, 0] = 1.0; KM = np.sqrt(KK)
SM = np.exp(-.5 * KK * RS ** 2).astype(np.float32)
def fields(dk, smooth=True):
    w = BETA * dk * (SM if smooth else 1) / KK; return [sf.irfftn(1j * kv * w, s=(N, N, N)).astype(np.float32) for kv in (K[:, None, None], K[None, :, None], KZ[None, None, :])]
def rhat(P): return P / np.linalg.norm(P, axis=1)[:, None]
def recon(S, n_iter=3):
    """Iterated RSD removal; returns the final psi fields, which carry beta."""
    X = S; rh = rhat(S); F = None
    for it in range(n_iter + 1):
        F = fields(sf.rfftn(dens(cic(X))))
        if it < n_iter: X = S - np.sum(read(F, X) * rh, axis=1)[:, None] * rh
    return F
def lens_v(F, S_l, z_l):
    rh = rhat(S_l); return aH(z_l) * np.sum(read(F, S_l - np.sum(read(F, S_l) * rh, axis=1)[:, None] * rh) * rh, axis=1)
kb = np.geomspace(2 * np.pi / L, np.pi / CELL, 40); ib = np.digitize(KM.ravel(), kb); nb = np.maximum(np.bincount(ib, minlength=len(kb) + 1), 1); kc = np.bincount(ib, KM.ravel(), len(kb) + 1) / nb; gk = np.bincount(ib, minlength=len(kb) + 1) > 0
def pk(n): return np.bincount(ib, (np.abs(sf.rfftn(dens(n))) ** 2).ravel() * (L ** 3 / N ** 6) / KEEP, len(kb) + 1) / nb
ng = cic(Sg); Pd = pk(ng); nbar = ng[mask].mean() / CELL ** 3; shot = 1 / nbar; print("P data k~0.002,0.01,0.1:", [round(float(np.interp(q, kc[gk], Pd[gk]))) for q in (.002, .01, .1)], flush=True)
LN = np.load(os.path.join(EXT, "gh7_work", "gh7_lenses.npz")); Sl = xyz(LN["ra"], LN["dec"], LN["z"]); zl = LN["z"]
F = recon(Sg); v = lens_v(F, Sl, zl); F0 = fields(sf.rfftn(dens(ng))); print(f"data: rms v_rec {v.std():.1f}, corr with no-iteration {np.corrcoef(v, np.sum(read(F0, Sl) * rhat(Sl), axis=1) * aH(zl))[0, 1]:.3f}", flush=True); del F0
np.save(os.path.join(W, "gh8_psi.npy"), np.array(F)); np.save(os.path.join(W, "gh8_v.npy"), v); del F
A_ = ng[mask].sum() / nr[mask].sum(); P0 = np.maximum(Pd - shot, 1.0)
def interpP(P): return np.exp(np.interp(np.log(KM), np.log(kc[gk]), np.log(np.maximum(P[gk], 1e-3)))).astype(np.float32)
def mock(Pin, seed, full):
    r = np.random.default_rng(seed); P3 = interpP(Pin); P3[0, 0, 0] = 0; G = sf.irfftn(sf.rfftn(r.normal(size=(N, N, N)).astype(np.float32)) * np.sqrt(P3 * N ** 3 / L ** 3), s=(N, N, N)).astype(np.float32); dl = np.exp(G - G.var() / 2) - 1; del G
    Ft = fields(sf.rfftn(dl), smooth=False); cnt = np.zeros_like(nr, dtype=np.int32); cnt[mask] = r.poisson(np.maximum(A_ * nr[mask] * (1 + dl[mask]), 0)); idx = np.repeat(np.arange(N ** 3), cnt.ravel()); ii = np.stack(np.unravel_index(idx, (N, N, N)), 1); X = (ii + r.uniform(size=ii.shape)) * CELL - L / 2; X = X.astype(np.float32)
    rh = rhat(X); S = X + np.sum(read(Ft, X) * rh, axis=1)[:, None] * rh; Pm = pk(cic(S))
    if not full: return Pm
    vt = aH(zl) * np.sum(read(Ft, Sl) * rhat(Sl), axis=1); del Ft
    vr = lens_v(recon(S), Sl, zl); v0 = lens_v(recon(S, 0), Sl, zl); return Pm, vt, vr, v0
def matched(Pstart, seed):
    Pin = Pstart.copy()
    for it in range(2):
        Pm = mock(Pin, seed + it, False); Pin = Pin * np.clip(Pd / np.maximum(Pm, 1), .1, 10); print(f" match iter {it}: P_mock/P_data at k .01,.1: {np.interp(.01, kc[gk], (Pm / Pd)[gk]):.2f} {np.interp(.1, kc[gk], (Pm / Pd)[gk]):.2f}", flush=True)
    return Pin
ZB = np.quantile(zl, np.linspace(0, 1, 11)); IZ = np.clip(np.searchsorted(ZB, zl) - 1, 0, 9)
def demean(a):
    o = a.copy()
    for b in range(10): o[IZ == b] -= o[IZ == b].mean()
    return o
def stats(Pin, seed, lab):
    Pm, vt, vr, v0 = mock(Pin, seed, True); print(f"{lab} raw: rms rec {vr.std():.0f}, shell means {np.round([vr[IZ == b].mean() for b in range(10)])}", flush=True); vr, v0 = demean(vr), demean(v0); r1, r0 = float(np.corrcoef(vt, vr)[0, 1]), float(np.corrcoef(vt, v0)[0, 1]); R = float(np.cov(vt, vr)[0, 1] / vr.var()); q = (kc > .03) & (kc < .3) & gk; dev = float(np.max(np.abs(Pm[q] / Pd[q] - 1))); print(f"{lab}: r {r1:.3f} (no iteration {r0:.3f}), R {R:.3f}, rms true {vt.std():.0f}, rms rec {vr.std():.0f}; max |P/P_d-1| k .03-.3 {dev:.3f}", flush=True); return dict(r=r1, r_noiter=r0, R=R, rms_true=float(vt.std()), rms_rec=float(vr.std()), Pdev=dev)
Pf = matched(P0, 200); RES["fm"] = stats(Pf, 300, "R_fm")
qk = (kc > .02) & (kc < .05) & gk; sl = np.polyfit(np.log(kc[qk]), np.log(P0[qk]), 1); Pc = P0.copy(); lo = (kc < .02) & gk; Pc[lo] = np.exp(np.polyval(sl, np.log(kc[lo]))); print("cut slope", sl[0], "P_cut k~.002,.01", np.round(np.exp(np.polyval(sl, np.log([.002, .01])))), flush=True)
Pc2 = matched(Pc, 400); Pc2[lo] = Pc[lo]; RES["cut"] = stats(Pc2, 500, "R_cut")
vd = demean(v); print(f"data: shell means {np.round([v[IZ == b].mean() for b in range(10)])}, rms raw {v.std():.1f}, demeaned {vd.std():.1f}", flush=True); Rctx = float(.64 * 300 / vd.std()); RES.update(rms_demeaned=float(vd.std()), R_fm=RES["fm"]["R"], R_cut=RES["cut"]["R"], R_ctx=Rctx, rms_data=float(v.std()), mesh=N, box=L, N_lens=len(v)); print(f"R_ctx {Rctx:.3f}", flush=True)
check("K1_iteration_no_worse", RES["fm"]["r"] >= RES["fm"]["r_noiter"], f"{RES['fm']['r']:.3f} vs {RES['fm']['r_noiter']:.3f}"); check("K2_mock_P_matches", RES["fm"]["Pdev"] < .1, f"max dev {RES['fm']['Pdev']:.3f}"); check("K3_mock_r", RES["fm"]["r"] > .3, f"r {RES['fm']['r']:.3f}")
json.dump(RES, open(os.path.join(HERE, "gh8_vel.json"), "w"), indent=1, sort_keys=True)
