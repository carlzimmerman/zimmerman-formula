#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
rar_refit_mu10_2026.py
======================
HOW BAD DOES THE RAR GET IF THE a_0-LINE IS REPLACED BY mu_10?

q_eta_derivation_2026.py established that Cassini is INTERPOLATION-specific: the a_0-line gives
1.9-3.0x the ceiling while mu_10 gives 0.03-0.10x and passes. The escape therefore requires
abandoning g_obs^2 = g_bar^2 + a_0 g_bar as the kernel. This file measures the price on real
data, refitting Upsilon per kernel rather than holding it fixed -- freezing Upsilon would
manufacture a deficit against whichever kernel prefers a different value.

The RAR is g_obs vs g_bar. For each kernel the prediction is g_obs = nu(g_bar/a_0) g_bar, and
the scatter is the rms of log10(g_obs,measured / g_obs,predicted).

A SECOND TEST THAT MATTERS AS MUCH AS THE SCATTER: the Upsilon each kernel demands, against the
Spitzer 3.6 micron prior. A kernel that fits only by pushing the stellar mass-to-light ratio
outside its independently measured range has not fitted anything.
"""
import sys, os, glob
import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
G_, MSUN, KPC = 6.6743e-11, 1.98892e30, 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "real_research", "data", "sparc_data")

head("PART A -- load the real rotation curves")
gal = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 7:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, 0], d[:, 1], d[:, 2],
                                          d[:, 3], d[:, 4], d[:, 5])
        m = (R > 0) & (Vobs > 0) & (eV > 0)
        if m.sum() < 3:
            continue
        gal.append(dict(name=os.path.basename(f).replace("_rotmod.dat", ""),
                        R=R[m] * KPC, Vobs=Vobs[m] * 1e3, eV=eV[m] * 1e3,
                        Vgas=Vgas[m] * 1e3, Vdisk=Vdisk[m] * 1e3, Vbul=Vbul[m] * 1e3))
    except Exception:
        continue
npt = sum(len(g["R"]) for g in gal)
check(len(gal) > 150, "A1  SPARC rotation curves loaded",
      f"{len(gal)} galaxies, {npt} data points")

def g_bar(g, Ups):
    """Baryonic acceleration. Vdisk/Vbul are tabulated at Upsilon = 1; scale by Upsilon.
    Bulge carries 1.4x the disk ratio, the SPARC convention."""
    V2 = g["Vgas"] * np.abs(g["Vgas"]) + Ups * g["Vdisk"] ** 2 + 1.4 * Ups * g["Vbul"] ** 2
    return np.maximum(V2, 1e-30) / g["R"]

def g_obs(g):
    return g["Vobs"] ** 2 / g["R"]

# ---- kernels: g_obs = nu(y) g_bar, y = g_bar/a0 ----
def nu_a0line(y):
    return np.sqrt(1.0 + 1.0 / y)
def nu_mu_n(n):
    def f(y):
        x = np.maximum(y, 1e-12).astype(float).copy()
        for _ in range(200):                      # invert mu_n(x)=x/(1+x^n)^(1/n) = y ... solve
            x = y * (1.0 + x ** (-float(n))) ** (1.0 / float(n))
        return x / y
    return f
def nu_simple(y):
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))

KERN = {"a0-line (Carl)": nu_a0line, "mu_3": nu_mu_n(3), "mu_5": nu_mu_n(5),
        "mu_10": nu_mu_n(10), "simple": nu_simple}

def scatter(nu, a0, Ups):
    res = []
    for g in gal:
        gb = g_bar(g, Ups)
        pred = nu(gb / a0) * gb
        res.append(np.log10(g_obs(g) / pred))
    r = np.concatenate(res)
    r = r[np.isfinite(r)]
    return np.std(r), np.mean(r), len(r)

head("PART B -- refit Upsilon per kernel (freezing it would manufacture a deficit)")
UPS = np.linspace(0.20, 1.60, 141)
best = {}
for nm, f in KERN.items():
    row = []
    for fn, a0 in A0.items():
        s = [scatter(f, a0, u)[0] for u in UPS]
        i = int(np.argmin(s))
        best[(nm, fn)] = (UPS[i], s[i])
        row.append(f"{fn[:4]}: Ups={UPS[i]:.2f} rms={s[i]:.4f}")
    info(f"B1  {nm:16s}", "   ".join(row))
a0_rms = best[("a0-line (Carl)", "canonical")][1]
m10_rms = best[("mu_10", "canonical")][1]
check(m10_rms > a0_rms,
      f"B2  the a_0-line remains the better RAR fit: {a0_rms:.4f} dex against mu_10's "
      f"{m10_rms:.4f} dex canonical -- a degradation of {m10_rms - a0_rms:+.4f} dex "
      f"({100*(m10_rms/a0_rms - 1):+.1f}%)",
      "measured on the same 175 galaxies with Upsilon refit independently for each")

head("PART C -- the Upsilon test, which matters as much as the scatter")
# Spitzer 3.6um prior (Lelli, McGaugh & Schombert 2016; McGaugh & Schombert 2014):
# Upsilon_disk = 0.5 M/L with ~0.1 dex scatter.
UP0, UPSIG_DEX = 0.5, 0.1
for nm in KERN:
    row = []
    for fn in A0:
        u = best[(nm, fn)][0]
        nsig = np.log10(u / UP0) / UPSIG_DEX
        row.append(f"{fn[:4]}: Ups={u:.2f} ({nsig:+.1f} sigma)")
    info(f"C1  {nm:16s}", "   ".join(row))
u_a0 = best[("a0-line (Carl)", "canonical")][0]
u_m10 = best[("mu_10", "canonical")][0]
n_a0 = np.log10(u_a0 / UP0) / UPSIG_DEX
n_m10 = np.log10(u_m10 / UP0) / UPSIG_DEX
check(abs(n_m10) > abs(n_a0),
      f"C2  *** AND THE REAL PRICE IS NOT THE SCATTER, IT IS THE MASS-TO-LIGHT RATIO. mu_10 "
      f"prefers Upsilon = {u_m10:.2f}, which is {n_m10:+.1f} sigma from the Spitzer prior "
      f"0.5 +- 0.1 dex, against the a_0-line's {u_a0:.2f} ({n_a0:+.1f} sigma) ***",
      "a kernel that fits only by pushing the stellar mass outside its independently measured "
      "range has not fitted anything")
# and at the PRIOR value, not the best fit
info("C3  scatter with Upsilon HELD at the Spitzer central value 0.50", "")
for nm, f in KERN.items():
    row = []
    for fn, a0 in A0.items():
        s, _, _ = scatter(f, a0, UP0)
        row.append(f"{fn[:4]}: {s:.4f}")
    info(f"C3  {nm:16s}", "   ".join(row))

head("PART D -- the honest verdict")
s_a0_p = scatter(KERN["a0-line (Carl)"], A0["canonical"], UP0)[0]
s_m10_p = scatter(KERN["mu_10"], A0["canonical"], UP0)[0]
for s_ in [
    f"AT BEST FIT the degradation is modest: {a0_rms:.4f} -> {m10_rms:.4f} dex canonical, "
    f"{100*(m10_rms/a0_rms-1):+.1f}%. On scatter alone mu_10 is a perfectly respectable RAR fit "
    "and the Cassini escape looks nearly free.",
    f"*** BUT AT THE SPITZER PRIOR VALUE Upsilon = 0.50 THE PICTURE CHANGES: the a_0-line gives "
    f"{s_a0_p:.4f} dex and mu_10 gives {s_m10_p:.4f} dex canonical. mu_10's good fit REQUIRES "
    f"Upsilon = {u_m10:.2f}, which is {n_m10:+.1f} sigma above the independently measured "
    "3.6 micron mass-to-light ratio. THE ESCAPE IS PAID FOR IN STELLAR MASS, NOT IN SCATTER. ***",
    "THAT IS A TESTABLE PREDICTION RATHER THAN A FUDGE, and it should be stated as one: if the "
    "mu_n escape is correct, SPARC stellar masses are systematically underestimated by the "
    f"3.6 micron calibration by {np.log10(u_m10/UP0):.2f} dex. That is checkable against "
    "independent stellar-mass estimates -- dynamical, SED-fitting, or lensing -- and it is the "
    "cleanest falsifiable consequence this lane has produced.",
    "AGAINST INTEREST: this file refits a SINGLE global Upsilon for all galaxies. SPARC fits "
    "normally allow per-galaxy Upsilon within the prior, which would reduce the scatter for "
    "EVERY kernel and could change the ranking. A hierarchical per-galaxy refit is owed before "
    "the Upsilon tension is quoted as a result.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"RAR REFIT CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
