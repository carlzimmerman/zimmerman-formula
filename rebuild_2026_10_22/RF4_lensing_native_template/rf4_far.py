#!/usr/bin/env python3
"""RF4 (criteria 5632124ef4): tangential and cross shear at 1.1-15 Mpc by FFT on pixelised sources, sampled at every lens and comparison centre. Point-z rule Z_B > z_l + 0.2, native background.
    OMP_NUM_THREADS=1 nice -n 15 python3 rf4_far.py <kids_source_cache> <work_dir> <si3_work_dir>       RF4_MUTATE=1: sources rotated 45 deg
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, math, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
T0 = time.time(); HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); sys.path.insert(0, os.path.join(REB, "SI3_nested_isolation"))
from si3_hole import patch_edges, apply_patches
MUT = os.environ.get("RF4_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def P(s): print(f"[{time.time() - T0:7.0f} s, {rss():.2f} GB] {s}", flush=True)
CACHE, WORK, SI3W = sys.argv[1:4]; OMN, HN = 0.2976016, 0.6856427; ZG = np.linspace(0, 3.0, 6001); EE = np.sqrt(OMN * (1 + ZG) ** 3 + 1 - OMN); CHI = np.r_[0, np.cumsum(0.5 * (1 / EE[1:] + 1 / EE[:-1]) * np.diff(ZG))] * 299792.458 / (100 * HN); chi = lambda z: np.interp(z, ZG, CHI)
c_ms, G_SI, Mpc = 2.998e8, 6.674e-11, 3.0857e22; TO = (3.0857e16) ** 2 / 1.989e30
REDG = np.r_[1.1, 1.6, 2.2, 3.0, np.geomspace(3.0, 15.0, 5)[1:]]; NRB = len(REDG) - 1; ZE = np.arange(0.06, 0.62, 0.04); NZ = len(ZE) - 1; DP = 0.01
LN = np.load(os.path.join(DATA, "lr_lenses.npz")); lra, lde, lz, llm = (np.array(LN[k], "f8") for k in ("ra", "dec", "z", "logM")); E = patch_edges(lra, lde); LB = np.digitize(llm, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
cat = np.load(os.path.join(WORK, "rf4_cats.npz")); froz = np.load(os.path.join(SI3W, "si3_cats.npz")); CENS = {}
for s in ("S10", "S_strict", "S_x300"):
    mem = np.unique(cat[f"I_{s}_li"]); CENS[f"{s}_L"] = (lra[mem], lde[mem], mem); CENS[f"{s}_R"] = (froz[f"R_{s}_ra"], froz[f"R_{s}_dec"], froz[f"R_{s}_li"])
    n = len(cat[f"I_{s}_li"]); ic = np.arange(n); keep = ic[(ic % (n // len(mem))) < 4]; CENS[f"{s}_I"] = (cat[f"I_{s}_ra"][keep], cat[f"I_{s}_dec"][keep], cat[f"I_{s}_li"][keep])
OUT = {f"{k}_{q}": np.zeros((50, 4, NRB)) for k in CENS for q in ("WG", "WX", "WW")}
cell = None
def rd(k): return np.load(os.path.join(CACHE, f"{k}.npy"), mmap_mode="r")
RA, DE = rd("ra"), rd("dec"); Z_, E1, E2, WT = rd("zb"), rd("e1"), rd("e2"), rd("w")
for region in ("north", "south"):
    south = region == "south"; ix = np.flatnonzero(np.asarray(DE) < -15.0) if south else np.flatnonzero(np.asarray(DE) >= -15.0); ra = np.asarray(RA[ix], "f8"); de = np.asarray(DE[ix], "f8"); zb = np.asarray(Z_[ix], "f8"); e1 = np.asarray(E1[ix], "f8"); e2 = np.asarray(E2[ix], "f8"); w = np.asarray(WT[ix], "f8"); del ix
    if MUT: e1, e2 = -e2, e1
    rau = (ra + 180.0) % 360.0 if south else ra; dc = 0.5 * (de.min() + de.max()); cd = math.cos(math.radians(dc)); x0, y0 = rau.min() * cd, de.min(); ipx = ((rau * cd - x0) / DP).astype(np.int32); ipy = ((de - y0) / DP).astype(np.int32); del rau, ra
    PADP = int(2.3 / DP); nx, ny = int(ipx.max()) + 1 + PADP, int(ipy.max()) + 1 + PADP; flat = ipx.astype(np.int64) * ny + ipy; shape = (nx, ny); chis = chi(zb); P(f"{region}: {len(zb):,} sources, grid {shape}")
    Fx = np.fft.fftfreq(nx, 1 / nx); Fy = np.fft.fftfreq(ny, 1 / ny); gx = np.where(np.arange(nx) < nx / 2, np.arange(nx), np.arange(nx) - nx) * DP; gy = np.where(np.arange(ny) < ny / 2, np.arange(ny), np.arange(ny) - ny) * DP; GX, GY = np.meshgrid(gx, gy, indexing="ij"); RR = np.hypot(GX, GY); PH = np.exp(2j * np.arctan2(GY, GX)); PH[0, 0] = 0
    for iz in range(NZ):
        zm = 0.5 * (ZE[iz] + ZE[iz + 1]); chil = float(chi(zm)); Dl = chil / (1 + zm); Ds = chis / (1 + zb); Dls = (chis - chil) / (1 + zb); isc = np.clip(4 * math.pi * G_SI / c_ms ** 2 * (Dl * Mpc) * (Dls / np.maximum(Ds, 1e-6)), 0, None) * (zb > zm + 0.2)
        A = np.bincount(flat, w * isc * e1, nx * ny) + 1j * np.bincount(flat, w * isc * e2, nx * ny); Wm = np.bincount(flat, w * isc * isc, nx * ny); FA = np.fft.fft2(A.reshape(shape)); FW = np.fft.fft2(Wm.reshape(shape)); del A, Wm
        idx = {}
        for k_, (cra, cde, li) in CENS.items():
            sel = ((cde < -15.0) if south else (cde >= -15.0)) & (lz[li] >= ZE[iz]) & (lz[li] < ZE[iz + 1]) & (LB[li] >= 0) & (LB[li] < 4)
            if sel.sum() == 0: continue
            r_ = (cra[sel] + 180.0) % 360.0 if south else cra[sel]; px = np.floor((r_ * cd - x0) / DP).astype(int); py = np.floor((cde[sel] - y0) / DP).astype(int); g = (px >= 0) & (px < nx) & (py >= 0) & (py < ny); idx[k_] = (px[g], py[g], apply_patches(cra[sel][g], cde[sel][g], E), LB[li[sel]][g])
        for rb in range(NRB):
            th0, th1 = np.degrees(REDG[rb] / Dl), np.degrees(REDG[rb + 1] / Dl); ring = (RR >= th0) & (RR < th1); G = np.fft.ifft2(FA * np.fft.fft2(ring * PH)); Wr = np.fft.ifft2(FW * np.fft.fft2(ring.astype(float))).real
            for k_, (px, py, pa, mb) in idx.items():
                v = G[px, py]; np.add.at(OUT[f"{k_}_WG"], (pa, mb, rb), -v.real * TO); np.add.at(OUT[f"{k_}_WX"], (pa, mb, rb), v.imag * TO); np.add.at(OUT[f"{k_}_WW"], (pa, mb, rb), Wr[px, py])
        P(f"{region} slice {zm:.2f}")
    del flat, chis, zb, e1, e2, w, de, ipx, ipy, GX, GY, RR, PH
OUT["REDG"] = REDG; np.savez(os.path.join(WORK, f"rf4_far{TAG}.npz"), **OUT); P("done")
