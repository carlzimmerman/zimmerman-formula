#!/usr/bin/env python3
"""DW2 second implementation for pending rows 11, 12, 15. Own loader (real_research/data), own contraction, time stepping, orbit Monte Carlo, Schrodinger-Poisson ground state. Shares no function with dw2_core or dw2_proc; a0 values and ZN2's table are data. Numbers from these rows are particle-like, not adopted, reinstate nothing. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.linalg import eigh_tridiagonal
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
GC = 4.30091e-6  # kpc (km/s)^2 / Msun
AF = dict(canonical=9.3603e-11, alt=1.1312e-10); KM2 = 1e6 / 3.0857e19  # (km/s)^2/kpc to m/s^2
RC = 3 * 0.672 ** 2 * 1e4 / (8 * math.pi * GC) * 1e-6  # Msun/kpc^3
Z = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); LXX = np.log(np.array(Z["x"])); TG = sorted((float(Z[k]["0.00"]["lgM"]), np.array(Z[k]["0.00"]["lnm"])) for k in ("1e10", "1e11", "1e12", "1e13", "1e14")); LGM = np.array([t[0] for t in TG]); TB = np.array([t[1] for t in TG])
META = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) >= 18:
        try: META[t[0]] = dict(Inc=float(t[5]), L=float(t[7]) * 1e9, HI=float(t[13]) * 1e9, Vf=float(t[15]), Q=float(t[17]))
        except ValueError: pass
GL = []
d_ = os.path.join(REPO, "real_research", "data", "sparc_data")
for n, m in sorted(META.items()):
    p = os.path.join(d_, n + "_rotmod.dat")
    if not os.path.exists(p) or m["Q"] > 2 or m["Inc"] < 30: continue
    a = np.genfromtxt(p, comments="#")
    if a.ndim != 2 or len(a) < 3: continue
    GL.append(dict(n=n, r=a[:, 0], v=a[:, 1], vg2=np.sign(a[:, 3]) * a[:, 3] ** 2, vd2=a[:, 4] ** 2, vb2=a[:, 5] ** 2, **m))
EDGES = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]; SETS = [[q for q in GL if a <= q["Vf"] < b] for a, b in EDGES]
def m200(q, mass): M = 0.5 * q["L"] + 1.33 * q["HI"]; return 10 ** (11.18 + 0.9 * (math.log10(M) - 10)) if mass == "em1" else 6.35 * M
def natM(M, r):
    R = (3 * M / (4 * math.pi * 200 * RC)) ** (1 / 3); s = np.array([np.interp(math.log10(M), LGM, TB[:, j]) for j in range(TB.shape[1])]); x = np.log(np.clip(r / R, 1e-9, 1)); return (5.35 / 6.35) * M * np.exp(np.where(x >= LXX[0], np.interp(x, LXX, s), s[0] + 2 * (x - LXX[0]))), R
def profile(q, mass, f, U=.5):
    """Grid r kpc, M_c final, M_* (<r), M_b(<r)."""
    r = q["r"]; Vb2 = q["vg2"] + U * q["vd2"] + 1.4 * U * q["vb2"]; Mbr = np.maximum.accumulate(np.maximum(Vb2 * r / GC, 0)); Vs2 = U * q["vd2"] + 1.4 * U * q["vb2"]; Msr = np.maximum.accumulate(np.maximum(Vs2 * r / GC, 0)); M = m200(q, mass); _, R2 = natM(M, r); rg = np.geomspace(r[0] * .05, R2 * 1.2, 160); M0, _ = natM(M, rg); Mt = max(Mbr[-1], U * q["L"] + 1.33 * q["HI"]); Mb = np.interp(np.log(rg), np.log(r), Mbr); Mb[rg < r[0]] = Mbr[0] * (rg[rg < r[0]] / r[0]) ** 2; o = rg > r[-1]; Mb[o] = np.exp(np.interp(np.log(rg[o] / r[-1]) / math.log(3), [0, 1], [math.log(max(Mbr[-1], 1)), math.log(max(Mt, 1))])); Mb = np.maximum.accumulate(Mb)
    F = Mt / M0[-1]; rf = rg.copy()
    for _ in range(8):  # Newton-ish fixed point with bracketing replaced by secant in log
        pass
    a, b = rg * 1e-3, rg * 1.001; T = rg * M0 * (1 + F)
    for _ in range(30):
        c = np.sqrt(a * b); v = c * (np.interp(np.log(c), np.log(rg), Mb) + M0); a, b = np.where(v < T, c, a), np.where(v < T, b, c)
    rf = np.maximum.accumulate(np.sqrt(a * b)); Mf = np.interp(np.log(rg), np.log(rf), M0, left=0, right=M0[-1]); Mc = M0 + f * (Mf - M0); Ms = np.interp(np.log(rg), np.log(r), Msr); Ms[rg < r[0]] = Msr[0] * (rg[rg < r[0]] / r[0]) ** 2; return rg, Mc, Ms
def retained(rg, Mc, Ms, sg, T=13.8e9, local=False, steps=20):
    """dM_shell/dt = -sg rho_* M_shell, time stepping with stars growing linearly from 0 to now (own, real history form)."""
    rho = Ms / (4 / 3 * math.pi * rg ** 3) * 1e-9 if not local else np.maximum(np.gradient(Ms, rg), 0) / (4 * math.pi * rg ** 2) * 1e-9; dm = np.diff(Mc, prepend=0.0); m = dm.copy(); dt = T / steps
    for k in range(steps): m = m * np.exp(-sg * rho * (k + .5) / steps * 2 * dt) if False else m * np.exp(-sg * rho * dt)  # constant stars: same as row 11's analytic form; growth option below
    return np.cumsum(m)
def law(g, a): return .5 * g + np.sqrt(.25 * g * g + a * g)
def dgal(q, gc, a, U=.5):
    r = q["r"]; gO = q["v"] ** 2 / r * KM2; gb = np.maximum((q["vg2"] + U * q["vd2"] + 1.4 * U * q["vb2"]) / r * KM2, 1e-20); m = (r >= r.max() * 2 / 3) & (q["v"] > 0); return float(np.mean(np.log10(gO[m] / (law(gb[m], a) + gc[m]))))
def floors(a):
    fl = []
    for s in SETS:
        D = np.array([dgal(q, np.zeros(len(q["r"])), a) for q in s]); rg = np.random.default_rng(20261102); b = np.median(D[rg.integers(0, len(D), (2000, len(D)))], axis=1).std(); fl.append((float(np.median(D)), min(float(np.median(D)), 0) - 2 * float(b)))
    return fl
PF = {}
def gc_star(q, mass, f, sg, local=False, T=13.8e9):
    k = (q["n"], mass, f)
    if k not in PF: PF[k] = profile(q, mass, f)
    rg, Mc, Ms = PF[k]; Mx = retained(rg, Mc, Ms, sg, T, local); return GC * np.interp(np.log(q["r"]), np.log(rg), Mx) / q["r"] ** 2 * KM2
def binD(sg, mass, f, a, local=False):
    return [float(np.median([dgal(q, gc_star(q, mass, f, sg, local), a) for q in s])) for s in SETS]
# ---------- row 11
P("== Row 11, stars. sigma fitted so the tighter of 150-200, 200-250 sits on its floor, f_Q, reading N. Exposure rho_*(<r) T = 13.8 Gyr; 'local' uses the shell density.")
RES["star"] = {}
xc = {.1: (136., 8.61e11), .3: (407., 1.68e12), .5: (679., 2.83e12)}; XE = {.1: .056, .3: .086, .5: .131}
for ft, a in AF.items():
    FL = floors(a)
    for mass in ("em1", "share"):
        for loc in (False, True):
            lo, hi = 1e-10, 1e-3
            for _ in range(26):
                c = math.sqrt(lo * hi); D = binD(c, mass, .872, a, loc); ok = all(D[i] >= FL[i][1] for i in (3, 4)); lo, hi = (lo, c) if ok else (c, hi)
            sg = hi; D = binD(sg, mass, .872, a, loc); margin = [D[i] - FL[i][1] for i in range(6)]
            ret = [float(np.median([np.interp(q["r"].max(), PF[(q["n"], mass, .872)][0], retained(*PF[(q["n"], mass, .872)], sg, 13.8e9, loc)) / np.interp(q["r"].max(), PF[(q["n"], mass, .872)][0], PF[(q["n"], mass, .872)][1]) for q in s])) for s in SETS]
            cl = {x: 1 - math.exp(-sg * v[1] / (4 / 3 * math.pi * v[0] ** 3) * 1e-9 * 13.8e9) for x, v in xc.items()}
            RES["star"][f"{ft}|{mass}|{'local' if loc else 'mean'}"] = dict(sigma=sg, d=D, floor=[f[1] for f in FL], margin=margin, retained=ret, cl=cl)
            P(f"  {ft:9s} {mass:6s} {'local' if loc else 'mean ':5s} sigma {sg:.2e}; retained R_last " + " ".join(f"{x:.2f}" for x in ret) + " | d - floor " + " ".join(f"{x:+.3f}" for x in margin) + " | X-COP lost x .1 .3 .5 " + " ".join(f"{v:.3f}" for v in cl.values()) + " (own error " + " ".join(f"{v:.3f}" for v in XE.values()) + ")")
# stellar heat: conversion rate per solar mass of stars, against the Sun's luminosity
sg = RES["star"]["canonical|em1|mean"]["sigma"]; rho_c_sun = 0.01  # Msun/pc^3 native inner, order
dm = sg * rho_c_sun; Lper = dm * 1.989e33 * (2.998e10) ** 2 / 3.156e7; RES["star_heat"] = dict(rate=dm, L_erg_s=Lper, ratio=Lper / 3.83e33); P(f"  Conversion per solar mass of stars at rho_c {rho_c_sun}: {dm:.1e} Msun/yr; if the rest energy reached the star: {Lper:.1e} erg/s, x{Lper / 3.83e33:.0f} L_sun; so the channel must be dark to about 1 part in {Lper / 3.83e33 * 100:.0e}, and it is a stated coupling with no action")
# ---------- row 12 orbit Monte Carlo
P("\n== Row 12, kick. Orbit Monte Carlo: isotropic kick on circular orbits, leapfrog in a spherical potential; mass fraction time-averaged inside R over 3 Gyr. No constant set by hand beyond tau, v_k.")
def orbits(Mtot, r0, vk, Rm, n=200, seed=7, T=3.0):
    """Mtot(r) Msun callable, r0 start radii kpc, units kpc, km/s, Gyr (1 km/s = 1.0227 kpc/Gyr)."""
    rng = np.random.default_rng(seed); K = 1.0227; idx = rng.integers(0, len(r0), n); x = np.zeros((n, 3)); x[:, 0] = r0[idx]; vc = np.sqrt(GC * Mtot(r0[idx]) / r0[idx]); vel = np.zeros((n, 3)); vel[:, 1] = vc; u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; vel += vk * u
    def acc(x): rr = np.maximum(np.linalg.norm(x, axis=1), 1e-3); return -(GC * Mtot(rr) / rr ** 3)[:, None] * x * K ** 2
    dt = min(0.002, 0.05 * float(np.min(r0) / (vc.max() + vk) / K)); dt = max(dt, 2e-4); ns = int(T / dt); inR = np.zeros(n); vel = vel * K; a_ = acc(x)
    for i in range(ns):
        vel += .5 * dt * a_ / 1.0 * 1.0; x += dt * vel; a_ = acc(x); vel += .5 * dt * a_
        if i % 10 == 0: inR += np.linalg.norm(x, axis=1) < Rm
    return float(np.mean(inR / max(ns // 10 + (1 if ns % 10 else 0), 1)))
def kick_sys(Mh, Mb, Rb, Rm, vk, mass_label):
    Mc = lambda r: natM(Mh, r)[0]; R2 = natM(Mh, np.array([1.]))[1]
    def Mtot(r):
        rr = np.asarray(r, float); M = Mh * np.where(rr <= R2, Mc(rr) / (5.35 / 6.35) / Mh, 1 + (rr - R2) / R2 * 0.3) * (1.0); return M + Mb * rr ** 2 / (rr + Rb / 2) ** 2
    rr = np.geomspace(Rm * .02, Rm, 40); dm = np.diff(Mc(rr), prepend=0); p = dm / dm.sum(); rng = np.random.default_rng(3); r0 = rng.choice(rr, 300, p=p) * math.exp(-0.5 * math.log(rr[1] / rr[0])); return orbits(Mtot, r0, vk, Rm)
K12 = {}
RTIGHT = 0.80
for vk in (200., 300., 382., 500., 700.):
    t = {}
    for lab, Mh, Mb, Rb, Rm in (("150-200", 5.78e11, 4.43e10, 8., 29.2), ("200-250", 1.28e12, 1.07e11, 12., 41.2), ("250-400", 1.87e12, 1.64e11, 12., 42.2), ("group 1e13", 1e13, 1e12, 40., 200.), ("X-COP x.1", 6e14, 2.8e12, 60., 136.), ("X-COP x.3", 6e14, 1.7e13, 200., 407.), ("X-COP x.5", 6e14, 3.6e13, 300., 679.)):
        t[lab] = kick_sys(Mh, Mb, Rb, Rm, vk, lab)
    K12[vk] = t; P(f"  v_k {vk:.0f}: fraction of decayed stuff still inside R: " + " ".join(f"{k} {v:.2f}" for k, v in t.items()) + f" | at decayed share {RTIGHT}: cold retained 150-200 {1 - RTIGHT * (1 - t['150-200']):.2f}, X-COP loss x .1 .3 .5 " + " ".join(f"{RTIGHT * (1 - t[k]):.3f}" for k in ("X-COP x.1", "X-COP x.3", "X-COP x.5")))
RES["kick"] = K12
# ---------- row 15 Schrodinger-Poisson
P("\n== Row 15, scalar. Ground state of Schrodinger-Poisson in the baryon monopole, radial grid, self-consistent, soliton mass from the core-halo fit (PROVISIONAL). No fit for r_c: the state's size comes from the solve.")
HBC = 1.97327e-7  # eV m
def sp(mb_fun, Msol, m22, Rmax=None, N=1500):
    m = m22 * 1e-22; L = HBC / m * 2.998e8 / 1e3 / 3.0857e19  # hbar/m in kpc km/s
    Rmax = Rmax or 400 * L ** .5; r = np.linspace(Rmax / N, Rmax, N); h = r[1] - r[0]; Vself = np.zeros(N); u = None; Pb = np.cumsum(GC * mb_fun(r) / r ** 2)[-1] - np.cumsum(GC * mb_fun(r) / r ** 2); Vext = -Pb * h
    for it in range(120):
        D = L ** 2 / h ** 2 + Vext + Vself; E = -0.5 * L ** 2 / h ** 2 * np.ones(N - 1); w, v = eigh_tridiagonal(D, E, select="i", select_range=(0, 0)); un = v[:, 0] ** 2; un /= un.sum() * h; u = un if u is None else .5 * u + .5 * un; M = np.cumsum(u) * h * Msol; dPhi = GC * M / r ** 2; Pn = (np.cumsum(dPhi[::-1])[::-1]) * h; Vs = -Pn; Vself = .6 * Vself + .4 * Vs if it else Vs
    return r, M, float(w[0])
for lab, Mh, Mb, Rb, Rl in (("150-200", 5.78e11, 4.43e10, 8., 29.2), ("200-250", 1.28e12, 1.07e11, 12., 41.2)):
    Mn = float(natM(Mh, np.array([Rl]))[0][0]); rows = []
    for m22 in (.003, .004, .006, .01):
        rc = 1.6 / m22 * (Mh / 1e9) ** (-1 / 3); rho0 = .019 / m22 ** 2 / rc ** 4 * 1e9; x = np.linspace(0, 3.3 * rc, 4000); Msol = float(np.trapz(4 * math.pi * x ** 2 * rho0 / (1 + .091 * (x / rc) ** 2) ** 8, x)); MbF = lambda r: Mb * r ** 2 / (r + Rb / 2) ** 2
        r0, M0_, _ = sp(lambda r: 0 * r, Msol, m22, Rmax=max(20 * rc, 3 * Rl)); r1, M1, _ = sp(MbF, Msol, m22, Rmax=max(20 * rc, 3 * Rl)); rows.append((m22, rc, Msol, float(np.interp(Rl, r0, M0_)) / Mn, float(np.interp(Rl, r1, M1)) / Mn, float(r0[np.searchsorted(M0_, .5 * Msol)]), float(r1[np.searchsorted(M1, .5 * Msol)])))
    RES.setdefault("sp", {})[lab] = rows; P(f"  {lab} M_c native (R_last) {Mn:.2e}:"); [P(f"     m22 {a:.3f} fit r_c {b:.0f} kpc, M_sol {c:.2e}; M(<R_last)/native, no baryons {d:.2f}, in baryon well {e:.2f}; half-mass r {f:.0f} -> {g_:.0f} kpc") for a, b, c, d, e, f, g_ in rows]
json.dump(RES, open(os.path.join(HERE, "dw2_second_results.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, "dw2_second.out"), "w").write("\n".join(OUT) + "\n")
