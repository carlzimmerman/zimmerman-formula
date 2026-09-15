#!/usr/bin/env python3
"""L259 -- DOES THE n = 2 SELECTION SURVIVE A FREE STELLAR MASS-TO-LIGHT RATIO PER GALAXY?
L232 selected n = 2 in mu_n(Y) = 1 - (1+Y)^-n, Y = g/s, s = c sqrt(G rho), with Upsilon fixed at 0.5/0.7.
Here one nuisance per galaxy scales both stellar components, Upsilon_d = 0.5 f, Upsilon_b = 0.7 f,
f on a 41-point grid with Upsilon_d in [0.2, 1.2] (the G013 window), chosen per galaxy and per (n, footing)
to minimise that galaxy's rms; the pooled rms over points and the equal-galaxy mean are then compared across n.
Same data, same cuts, same 155 galaxies as L232 (eV/V < 0.10, >= 3 points).  Both density conventions."""
import os, glob, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "sparc_data")
kpc, KMS, G, c, MPC = 3.0857e19, 1.0e3, 6.674e-11, 2.99792458e8, 3.0857e22
H0 = 67.4e3 / MPC; rho_c = 3 * H0**2 / (8 * math.pi * G); S = {"Lambda": c * math.sqrt(G * 0.685 * rho_c), "crit": c * math.sqrt(G * rho_c)}
FGRID = np.linspace(0.4, 2.4, 41)                           # Upsilon_d = 0.5 f in [0.2, 1.2]
Yt = np.logspace(-8, 8, 40001)
def inv(n):                                                 # Y = F_n^{-1}(g_bar/s), F_n(Y) = Y (1 - (1+Y)^-n), monotone
    F = Yt * (1 - (1 + Yt)**(-n)); return lambda x: np.exp(np.interp(np.log(x), np.log(F), np.log(Yt)))
INV = {n: inv(n) for n in (1, 2, 3, 4)}
gal = []
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6)); m = (R > 0) & (Vo > 0) & (eV > 0) & (eV / Vo < 0.10)
    if m.sum() < 3: continue
    R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
    if (Vg * np.abs(Vg) + 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb) > 0).sum() < 3: continue
    gal.append((R * kpc, Vo**2 * KMS**2 / (R * kpc), Vg * np.abs(Vg) * KMS**2, (0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb)) * KMS**2))
print(f"L259 -- free M/L per galaxy and the integer selection: {len(gal)} galaxies (L232: 155)\n")
OUT = {}
for tag, s in S.items():
    print(f"[{tag} convention] s = {s:.4e} m/s^2, a0 = s/2 = {s/2:.4e}")
    print(f"    n   fixed-ML pooled rms   free-ML pooled rms   free-ML galaxy-mean rms   galaxies preferring n   f at bounds")
    best_per_gal = {n: [] for n in (1, 2, 3, 4)}; pooled = {}; fixed = {}; gmean = {}; nbound = {}
    for n in (1, 2, 3, 4):
        res_fixed, res_free, rms_gal, nb = [], [], [], 0
        for r, gobs, gg, gs in gal:
            best = None
            for f in FGRID:
                gbar = (gg + f * gs) / r; ok = gbar > 0
                if ok.sum() < 3: continue
                resid = np.log10(gobs[ok] / (s * INV[n](gbar[ok] / s))); rms = float(np.sqrt(np.mean(resid**2)))
                if f == 1.0: res_fixed.append(resid)
                if best is None or rms < best[0]: best = (rms, f, resid)
            res_free.append(best[2]); rms_gal.append(best[0]); nb += best[1] in (FGRID[0], FGRID[-1]); best_per_gal[n].append(best[0])
        pooled[n] = float(np.sqrt(np.mean(np.concatenate(res_free)**2))); fixed[n] = float(np.sqrt(np.mean(np.concatenate(res_fixed)**2)))
        gmean[n] = float(np.mean(rms_gal)); nbound[n] = nb
    pref = {n: int(sum(1 for i in range(len(gal)) if min(best_per_gal[k][i] for k in (1, 2, 3, 4)) == best_per_gal[n][i])) for n in (1, 2, 3, 4)}
    for n in (1, 2, 3, 4):
        print(f"    {n}        {fixed[n]:.4f}               {pooled[n]:.4f}                 {gmean[n]:.4f}                  {pref[n]:3d}                 {nbound[n]}")
    win = min(pooled, key=pooled.get); gap = sorted(pooled.values())[1] - pooled[win]
    print(f"    free-ML winner: n = {win} (next-best +{gap:.4f} dex); galaxy-mean winner: n = {min(gmean, key=gmean.get)}; most galaxies prefer n = {max(pref, key=pref.get)}\n")
    OUT[tag] = dict(fixed=fixed, free_pooled=pooled, free_galaxy_mean=gmean, galaxies_preferring=pref, f_at_bounds=nbound, winner=win)
json.dump(OUT, open(os.path.join(HERE, "L259_results.json"), "w"), indent=1)
