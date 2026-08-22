#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate2_sparc_alpha_2026.py -- GATE 2: MEASURE, do not assume, how much environment
dependence of the MOND transition shape SPARC allows.

Carl's Gate 2, verbatim intent: "Don't assume n ~ M^alpha. Fit it."

MODEL (Gate 1's controlled microscope; asymptotics are n-independent BY CONSTRUCTION)
    g_obs = nu_n(g_bar/a0) * g_bar ,   nu_n(y) = [(1+sqrt(1+4y^-n))/2]^(1/n)
    ln n_i = ln n0 + alpha * ln(T_i / T_pivot)
    T_i  = a0^{3/2} / sqrt(G M_bar,i)          <- the environmental scalar, = a0/R_M,i
So alpha is EXACTLY the exponent in n ~ T^alpha, and since T ~ M^{-1/2},  n ~ M^{-alpha/2}.

PER-GALAXY NUISANCES, all with literature priors (Li et al. 2018 / McGaugh & Schombert 2014):
    Upsilon_disk  log-normal about 0.50 Msun/Lsun, 0.10 dex
    Upsilon_bulge log-normal about 0.70 Msun/Lsun, 0.10 dex
    distance      Gaussian about catalogue D with catalogue e_D
    inclination   Gaussian about catalogue i with catalogue e_i
GLOBAL: ln n0, alpha, ln f_int (fractional intrinsic scatter).  a0 fixed at the framework
canonical value in the primary fit; refit free as a variant.

THREE CONFOUND TESTS, because a non-zero alpha is worthless without them:
  (C1) x-control: let n depend on each galaxy's MEDIAN ACCELERATION instead of its mass.
       If that fits as well or better, the "mass dependence" is really a misspecified
       universal mu, not an environmental effect.
  (C2) surface-brightness control: z = SBdisk instead of mass.
  (C3) permutation null: shuffle the mass labels and refit alpha many times, to get the
       null distribution of alpha-hat rather than trusting the asymptotic error bar.
"""
import os, sys, glob, json, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "real_research", "data", "sparc_data")
MRT  = os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")

G_, MSUN, KPC = 6.6743e-11, 1.98892e30, 3.0857e19
A0_CANON = 9.3619e-11
UPS_D, UPS_D_DEX = 0.50, 0.10
UPS_B, UPS_B_DEX = 0.70, 0.10
M_PIVOT = 1.0e10 * MSUN

def head(t): print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100, flush=True)
def info(l, d=""): print(f"  [info] {l}" + (f"   {d}" if d else ""), flush=True)

# ------------------------------------------------------------------ catalogue
def load_master():
    out = {}
    for ln in open(MRT):
        if len(ln) < 99: continue
        name = ln[0:11].strip()
        try:
            D, eD = float(ln[13:19]), float(ln[19:24])
            inc, einc = float(ln[26:30]), float(ln[30:34])
            L36 = float(ln[34:41]); SBdisk = float(ln[66:74]); Q = int(ln[96:99])
        except ValueError:
            continue
        if D <= 0 or inc <= 0: continue
        out[name] = dict(D=D, eD=max(eD, 0.01*D), inc=inc, einc=max(einc, 1.0),
                         L36=L36, SBdisk=SBdisk, Q=Q)
    return out

def load_galaxies(master, qmax=2, incmin=30.0, nmin=5):
    gals, skipped = [], {"nomaster": 0, "quality": 0, "inc": 0, "npts": 0, "badfile": 0}
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        m = master.get(name)
        if m is None: skipped["nomaster"] += 1; continue
        try: d = np.genfromtxt(f, comments="#")
        except Exception: skipped["badfile"] += 1; continue
        if d.ndim != 2 or d.shape[1] < 6: skipped["badfile"] += 1; continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        ok = (R > 0) & (Vobs > 0) & (eV > 0) & np.isfinite(Vobs)
        R, Vobs, eV, Vgas, Vdisk, Vbul = (a[ok] for a in (R, Vobs, eV, Vgas, Vdisk, Vbul))
        if len(R) < nmin: skipped["npts"] += 1; continue
        if m["Q"] > qmax: skipped["quality"] += 1; continue
        if m["inc"] < incmin: skipped["inc"] += 1; continue
        gals.append(dict(name=name, R=R*KPC, Vobs=Vobs*1e3, eV=eV*1e3,
                         Vgas=Vgas*1e3, Vdisk=Vdisk*1e3, Vbul=Vbul*1e3, **m))
    return gals, skipped

# ------------------------------------------------------------------ per-galaxy chi2
def gal_chi2(g, p, n_i, a0, f_int):
    """p = [ln Ud, ln Ub, ln fd, di_deg].  Returns chi2 including nuisance priors."""
    lUd, lUb, lfd, di = p
    Ud, Ub, fd = np.exp(lUd), np.exp(lUb), np.exp(lfd)
    R = g["R"]*fd
    Vg2 = np.sign(g["Vgas"])*g["Vgas"]**2*fd
    Vd2 = g["Vdisk"]**2*fd
    Vb2 = g["Vbul"]**2*fd
    Vbar2 = Vg2 + Ud*Vd2 + Ub*Vb2
    Vbar2 = np.maximum(Vbar2, 1.0)
    gbar = Vbar2/R
    gobs = nu_n(gbar/a0, n_i)*gbar
    Vpred = np.sqrt(gobs*R)
    inc = np.clip(g["inc"] + di, 15.0, 90.0)
    sc = np.sin(np.radians(g["inc"]))/np.sin(np.radians(inc))
    Vo, eVo = g["Vobs"]*sc, g["eV"]*sc
    s2 = eVo**2 + (f_int*Vo)**2
    c2 = np.sum((Vo - Vpred)**2/s2) + np.sum(np.log(s2))
    c2 += ((lUd - np.log(UPS_D))/(UPS_D_DEX*np.log(10)))**2
    c2 += ((lUb - np.log(UPS_B))/(UPS_B_DEX*np.log(10)))**2 if np.any(g["Vbul"] > 0) else 0.0
    c2 += (fd - 1.0)**2/(g["eD"]/g["D"])**2
    c2 += (di/g["einc"])**2
    return c2

def gal_mbar(g, p, fd_only=False):
    lUd, lUb, lfd, di = p
    Ud, Ub, fd = np.exp(lUd), np.exp(lUb), np.exp(lfd)
    R = g["R"]*fd
    Vbar2 = np.sign(g["Vgas"])*g["Vgas"]**2*fd + Ud*g["Vdisk"]**2*fd + Ub*g["Vbul"]**2*fd
    j = np.argmax(R)
    return max(Vbar2[j]*R[j]/G_, 1e4*MSUN)

# ------------------------------------------------------------------ global fit
class Fitter:
    def __init__(self, gals, a0=A0_CANON, zmode="mass"):
        self.g = gals; self.a0 = a0; self.zmode = zmode
        self.warm = {gg["name"]: np.array([np.log(UPS_D), np.log(UPS_B), 0.0, 0.0]) for gg in gals}
        self.zoverride = None
    def zvals(self, mbar):
        if self.zoverride is not None: return self.zoverride
        if self.zmode == "mass":
            T = self.a0**1.5/np.sqrt(G_*np.asarray(mbar))
            return np.log(T/(self.a0**1.5/np.sqrt(G_*M_PIVOT)))
        raise ValueError(self.zmode)
    def total(self, ln_n0, alpha, ln_fint, npass=2):
        f_int = np.exp(ln_fint); tot = 0.0
        mbar = np.array([gal_mbar(gg, self.warm[gg["name"]]) for gg in self.g])
        for _ in range(npass):
            z = self.zvals(mbar); tot = 0.0
            for k, gg in enumerate(self.g):
                n_i = float(np.clip(np.exp(ln_n0 + alpha*z[k]), 0.25, 150.0))
                fun = lambda p: gal_chi2(gg, p, n_i, self.a0, f_int)
                r = minimize(fun, self.warm[gg["name"]], method="Nelder-Mead",
                             options=dict(maxiter=600, xatol=1e-4, fatol=1e-4))
                self.warm[gg["name"]] = r.x; tot += r.fun
            mbar = np.array([gal_mbar(gg, self.warm[gg["name"]]) for gg in self.g])
        self.last_mbar = mbar
        return tot
    def fit_globals(self, alpha_fixed=None, x0=(0.0, 0.0, np.log(0.05))):
        if alpha_fixed is None:
            f = lambda v: self.total(v[0], v[1], v[2])
            r = minimize(f, np.array(x0), method="Nelder-Mead",
                         options=dict(maxiter=140, xatol=2e-3, fatol=0.05))
            return r.x, r.fun
        f = lambda v: self.total(v[0], alpha_fixed, v[1])
        r = minimize(f, np.array([x0[0], x0[2]]), method="Nelder-Mead",
                     options=dict(maxiter=90, xatol=2e-3, fatol=0.05))
        return np.array([r.x[0], alpha_fixed, r.x[1]]), r.fun

if __name__ == "__main__":
    t0 = time.time()
    print(__doc__)
    head("PART A -- the sample")
    master = load_master(); gals, sk = load_galaxies(master)
    info("A1  loaded", f"{len(gals)} galaxies after cuts (Q<=2, inc>=30 deg, >=5 pts); skipped {sk}")
    npts = sum(len(g["R"]) for g in gals)
    info("A2  data points", f"{npts}")
    F = Fitter(gals)
    mb0 = np.array([gal_mbar(g, F.warm[g["name"]]) for g in gals])
    info("A3  baryonic mass range (at prior Upsilon)",
         f"{mb0.min()/MSUN:.2e} to {mb0.max()/MSUN:.2e} Msun  "
         f"= {np.log10(mb0.max()/mb0.min()):.2f} decades")
    Trange = A0_CANON**1.5/np.sqrt(G_*mb0)
    info("A4  environmental scalar T = a0/R_M",
         f"{Trange.min():.3e} to {Trange.max():.3e} s^-2 = {np.log10(Trange.max()/Trange.min()):.2f} decades; "
         f"ln-lever arm {np.log(Trange.max()/Trange.min()):.2f}")
    T_SS = A0_CANON**1.5/np.sqrt(G_*MSUN)
    info("A5  Solar-System T for comparison",
         f"{T_SS:.3e} s^-2 -- ln(T_SS/T_median) = {np.log(T_SS/np.median(Trange)):.2f}")

    head("PART B -- primary fit: free (ln n0, alpha, ln f_int), a0 fixed canonical")
    v, chi = F.fit_globals()
    ln_n0, alpha_hat, ln_fint = v
    info("B1  best fit", f"n0 = {np.exp(ln_n0):.3f}   alpha = {alpha_hat:+.4f}   "
                          f"f_int = {np.exp(ln_fint):.4f}   -2lnL = {chi:.1f}")
    res = dict(n_gal_pivot=float(np.exp(ln_n0)), alpha_hat=float(alpha_hat),
               f_int=float(np.exp(ln_fint)), chi_best=float(chi),
               ngal=len(gals), npts=int(npts),
               lnT_lever_sparc=float(np.log(Trange.max()/Trange.min())),
               lnT_SS_over_median=float(np.log(T_SS/np.median(Trange))))

    head("PART C -- profile likelihood in alpha (Delta chi2 = 1 and 4)")
    grid = np.round(np.arange(-0.30, 0.3001, 0.05), 3)
    prof = {}
    for a in grid:
        vv, cc = F.fit_globals(alpha_fixed=float(a), x0=(ln_n0, 0, ln_fint))
        prof[float(a)] = float(cc)
        info(f"C1  alpha={a:+.2f}", f"-2lnL = {cc:.1f}   Delta = {cc-chi:+.1f}   n0={np.exp(vv[0]):.3f}")
    res["profile"] = prof
    ks = np.array(sorted(prof)); vs = np.array([prof[k] for k in ks]); d = vs - vs.min()
    def band(th):
        ok = ks[d <= th]
        return (float(ok.min()), float(ok.max())) if len(ok) else (np.nan, np.nan)
    res["alpha_1sig"] = band(1.0); res["alpha_2sig"] = band(4.0)
    info("C2  alpha 1sigma", f"{res['alpha_1sig']}")
    info("C3  alpha 2sigma", f"{res['alpha_2sig']}")

    head("PART D -- CONFOUND C1: is it mass, or is it just acceleration range?")
    xmed = []
    for k, g in enumerate(gals):
        p = F.warm[g["name"]]; Ud, Ub, fd = np.exp(p[0]), np.exp(p[1]), np.exp(p[2])
        R = g["R"]*fd
        Vbar2 = np.sign(g["Vgas"])*g["Vgas"]**2*fd + Ud*g["Vdisk"]**2*fd + Ub*g["Vbul"]**2*fd
        xmed.append(np.median(np.maximum(Vbar2, 1.0)/R/A0_CANON))
    xmed = np.array(xmed)
    info("D0  median x = g_bar/a0 per galaxy", f"{xmed.min():.3f} to {xmed.max():.3f}")
    rho = np.corrcoef(np.log(xmed), np.log(mb0))[0, 1]
    info("D1  corr(ln x_med, ln M_bar)", f"{rho:+.3f}  <- if this is large the two controls are degenerate")
    F.zoverride = np.log(xmed/np.median(xmed))
    vx, cx = F.fit_globals()
    info("D2  x-control fit", f"alpha_x = {vx[1]:+.4f}   -2lnL = {cx:.1f}   "
                               f"vs mass-model {chi:.1f}  (Delta = {cx-chi:+.1f})")
    res["xcontrol"] = dict(alpha=float(vx[1]), chi=float(cx), corr_lnx_lnM=float(rho))
    F.zoverride = None

    head("PART E -- CONFOUND C2: surface brightness instead of mass")
    sb = np.array([max(g["SBdisk"], 1.0) for g in gals])
    F.zoverride = np.log(sb/np.median(sb))
    vs2, cs2 = F.fit_globals()
    info("E1  SB-control fit", f"alpha_SB = {vs2[1]:+.4f}   -2lnL = {cs2:.1f}   (Delta = {cs2-chi:+.1f})")
    res["sbcontrol"] = dict(alpha=float(vs2[1]), chi=float(cs2))
    F.zoverride = None

    head("PART F -- CONFOUND C3: permutation null for alpha-hat")
    rng = np.random.default_rng(20260821)
    zt = F.zvals(F.last_mbar)
    nulls = []
    for it in range(40):
        F.zoverride = rng.permutation(zt)
        vp, cp = F.fit_globals(x0=(ln_n0, 0.0, ln_fint))
        nulls.append(float(vp[1]))
        if it % 8 == 0: info(f"F1  perm {it}", f"alpha = {vp[1]:+.4f}")
    F.zoverride = None
    nulls = np.array(nulls)
    res["perm_null"] = dict(mean=float(nulls.mean()), sd=float(nulls.std(ddof=1)),
                            p_two_sided=float(np.mean(np.abs(nulls) >= abs(alpha_hat))),
                            n=len(nulls))
    info("F2  permutation null", f"mean {nulls.mean():+.4f}  sd {nulls.std(ddof=1):.4f}  "
         f"|alpha_hat|={abs(alpha_hat):.4f}  p(two-sided) = {res['perm_null']['p_two_sided']:.3f}")

    json.dump(res, open(os.path.join(HERE, "gate2_result.json"), "w"), indent=1)
    head("GATE 2 SUMMARY")
    info("G1  n at the 1e10 Msun pivot", f"{np.exp(ln_n0):.3f}")
    info("G2  alpha_RAR", f"{alpha_hat:+.4f}   1sigma {res['alpha_1sig']}   2sigma {res['alpha_2sig']}")
    info("G3  runtime", f"{time.time()-t0:.0f} s")
    print("\nwrote gate2_result.json")
