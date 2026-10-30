#!/usr/bin/env python3
"""GH7 velocities: linear reconstruction from BGS on a mesh, and a lognormal mock for r and R. Reads no CMB map."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, healpy as hp, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh7_work")
RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
OM, BETA, CELL, RS = 0.3085, 0.44, 8.0, 12.5; zz = np.linspace(0, 1, 4001); EZ = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM)
CHI = np.r_[0, np.cumsum(.5 * (1 / EZ[1:] + 1 / EZ[:-1]) * np.diff(zz))] * 2997.92458              # Mpc/h
def xyz(ra, de, z):
    c = np.interp(z, zz, CHI); r, d = np.radians(ra), np.radians(de); return np.c_[c * np.cos(d) * np.cos(r), c * np.cos(d) * np.sin(r), c * np.sin(d)].astype(np.float32)
def aH(z): return 100 * np.interp(z, zz, EZ) / (1 + z)                                             # km/s per Mpc/h
L = 2 * (np.interp(.5, zz, CHI) + 2 * RS); N = int(math.ceil(L / CELL)); N += N % 2; L = N * CELL; print("mesh", N, "box", L, flush=True)
def cic(P, w=None):
    m = np.zeros((N, N, N), np.float32); g = (P + L / 2) / CELL - .5; i = np.floor(g).astype(np.int32); f = g - i
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                wt = (f[:, 0] if a else 1 - f[:, 0]) * (f[:, 1] if b else 1 - f[:, 1]) * (f[:, 2] if c else 1 - f[:, 2])
                np.add.at(m, ((i[:, 0] + a) % N, (i[:, 1] + b) % N, (i[:, 2] + c) % N), wt)
    return m
D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); s = (D["z"] >= .05) & (D["z"] <= .5); ra, de, z = D["ra"][s], D["de"][s], D["z"][s]; Ng = len(z); print("tracers", Ng, flush=True)
ng = cic(xyz(ra, de, z)); rng = np.random.default_rng(77)
NS = 64; cnt = np.bincount(hp.ang2pix(NS, ra, de, lonlat=True), minlength=hp.nside2npix(NS)).astype(float); pr = cnt / cnt.sum(); PIX = np.sqrt(hp.nside2pixarea(NS, degrees=True))
nr = np.zeros((N, N, N), np.float32); NR = 10 * Ng
for _ in range(10):
    p = rng.choice(len(pr), Ng, p=pr); r0, d0 = hp.pix2ang(NS, p, lonlat=True); d1 = d0 + rng.uniform(-.5, .5, Ng) * PIX; r1 = r0 + rng.uniform(-.5, .5, Ng) * PIX / np.maximum(np.cos(np.radians(d0)), .05)
    nr += cic(xyz(r1, d1, rng.choice(z, Ng)))
nr /= 10.0; occ = nr > 0; mask = nr > 0.1 * nr[occ].mean(); print("mask cells", int(mask.sum()), "of occupied", int(occ.sum()), flush=True)
def dens(n):
    d = np.zeros_like(n); a = n[mask].sum() / nr[mask].sum(); d[mask] = n[mask] / (a * nr[mask]) - 1; return d
K = sf.fftfreq(N, CELL / (2 * np.pi)).astype(np.float32); KZ = sf.rfftfreq(N, CELL / (2 * np.pi)).astype(np.float32)
KK = K[:, None, None] ** 2 + K[None, :, None] ** 2 + KZ[None, None, :] ** 2; KK[0, 0, 0] = 1.0
def vel_fields(dk, smooth=True):
    """Three mesh components of beta * psi (Mpc/h); v_los = aH(z) * (psi . rhat)."""
    w = BETA * dk * (np.exp(-.5 * KK * RS ** 2) if smooth else 1) / KK; out = []
    for ax, kv in enumerate((K[:, None, None], K[None, :, None], KZ[None, None, :])): out.append(sf.irfftn(1j * kv * w, s=(N, N, N)).astype(np.float32))
    return out
def read_los(F, P, z_):
    i = ((P + L / 2) / CELL).astype(int) % N; r = P / np.linalg.norm(P, axis=1)[:, None]; return aH(z_) * sum(F[a][i[:, 0], i[:, 1], i[:, 2]] * r[:, a] for a in range(3))
LN = np.load(os.path.join(W, "gh7_lenses.npz")); PL = xyz(LN["ra"], LN["dec"], LN["z"])
dk = sf.rfftn(dens(ng)); F = vel_fields(dk); vrec = read_los(F, PL, LN["z"]); np.save(os.path.join(W, "gh7_psi.npy"), np.array(F)); del F; print(f"data: rms v_rec {vrec.std():.1f} km/s", flush=True)
# ---- P(k) from the mesh, window and shot corrected, then the lognormal mock
fw = mask.mean(); kk = np.sqrt(KK).ravel(); kb = np.geomspace(2 * np.pi / L, np.pi / CELL, 40); ib = np.digitize(kk, kb); pw = (np.abs(dk) ** 2).ravel() * (L ** 3 / N ** 6) / fw
wt = np.ones_like(kk); Pk = np.bincount(ib, pw, len(kb) + 1) / np.maximum(np.bincount(ib, wt, len(kb) + 1), 1); kc = np.bincount(ib, kk, len(kb) + 1) / np.maximum(np.bincount(ib, wt, len(kb) + 1), 1)
nbar = ng[mask].mean() / CELL ** 3; shot = 1 / nbar; Pc = np.maximum(Pk - shot, 1.0); g = kc > 0; print("nbar", nbar, "shot", shot, "P(k~0.1)", float(np.interp(.1, kc[g], Pk[g])), flush=True)
PL3 = np.exp(np.interp(np.log(np.sqrt(KK)), np.log(kc[g]), np.log(Pc[g]))).astype(np.float32); PL3[0, 0, 0] = 0
gk = sf.rfftn(rng.normal(size=(N, N, N)).astype(np.float32)) * np.sqrt(PL3 * N ** 3 / L ** 3); G = sf.irfftn(gk, s=(N, N, N)).astype(np.float32); sg2 = float(G.var()); print("sigma_G^2", sg2, flush=True)
dl = np.exp(G - sg2 / 2) - 1; a = ng[mask].sum() / nr[mask].sum(); nm = np.zeros_like(ng); nm[mask] = rng.poisson(np.maximum(a * nr[mask] * (1 + dl[mask]), 0))
Ft = vel_fields(sf.rfftn(dl), smooth=False); vt = read_los(Ft, PL, LN["z"]); del Ft
Fm = vel_fields(sf.rfftn(dens(nm))); vr = read_los(Fm, PL, LN["z"]); del Fm
rm = float(np.corrcoef(vt, vr)[0, 1]); R = float(np.cov(vt, vr)[0, 1] / vr.var()); print(f"mock: r {rm:.3f}, R {R:.3f}, rms v_true {vt.std():.1f}, rms v_rec {vr.std():.1f}", flush=True)
check("K3_mock_r_and_sign", rm > 0.3 and np.mean(vt * vr) > 0, f"r {rm:.3f}, <v_t v_r> {np.mean(vt * vr):.0f}")
RES.update(kc=kc[g].tolist(), Pk=Pk[g].tolist(), r_mock=rm, R=R, rms_true_mock=float(vt.std()), rms_rec_mock=float(vr.std()), rms_rec_data=float(vrec.std()), mesh=N, box=L, N_lens=len(vrec), N_tracer=Ng)
np.savez(os.path.join(W, "gh7_vel.npz"), v=vrec.astype(np.float32)); json.dump(RES, open(os.path.join(HERE, "gh7_vel.json"), "w"), indent=1, sort_keys=True)
