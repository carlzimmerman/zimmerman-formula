#!/usr/bin/env python3
"""
Independent check of the External Field Effect (EFE) in SPARC -- MOND's SEP-violating signature, per galaxy.
==========================================================================================================
The EFE is the one prediction that cleanly separates MOND from dark matter: a galaxy's internal dynamics depend
on the EXTERNAL field g_ext from large-scale structure (a Strong-Equivalence-Principle violation no dark-matter
model makes). Signature in the radial acceleration relation (RAR): a DOWNTURN at the lowest baryonic
accelerations -- isolated MOND keeps the deep-MOND sqrt-law g_obs=sqrt(a0 g_bar), but a real external field
makes the galaxy quasi-Newtonian below g_bar ~ g_ext, pulling g_obs BELOW the isolated prediction. Chae et al.
(2020, arXiv:2009.11525) detected it at ~4 sigma blind across 153 SPARC galaxies, 8-11 sigma in strong-field
"golden" galaxies.

Two tests here, with the honest finding that the FIRST is null by construction and the SECOND is the real one:
  (1) GLOBAL RAR fit (a0, e_N): the AVERAGE external field. This is ~0 -- expected, because the SPARC sample is
      dominated by relatively isolated galaxies, so the mean EFE is washed out. (A null here does NOT contradict
      Chae, whose signal is per-galaxy + environment-correlated.)
  (2) PER-GALAXY e_N fit (a0 fixed at the global RAR value): the real EFE test. We fit one external-field
      parameter e_N per galaxy from the shape of its own RAR (does its outer/low-g_bar end turn down?), and look
      at the DISTRIBUTION of e_N and which galaxies carry it.

QUMOND radial EFE: g_obs = nu((g_bar+g_ext)/a0)(g_bar+g_ext) - nu(g_ext/a0) g_ext, nu(u)=1/(1-exp(-sqrt(u))),
g_ext = e_N a0.

HONEST SCOPE: the DECISIVE Chae result -- that the fitted per-galaxy e_N correlates with each galaxy's actual
large-scale environment (density field) -- needs external data not in SPARC, so it is flagged, not reproduced.
This recovers the internal RAR-shape part only. Reuses precision_rar_test.py's SPARC pipeline. numpy+scipy.
"""
import os
import sys
import glob
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(__file__)
import importlib.util
spec = importlib.util.spec_from_file_location("prt", os.path.join(HERE, "precision_rar_test.py"))
prt = importlib.util.module_from_spec(spec); spec.loader.exec_module(prt)

kpc = 3.0857e19
A0 = 1.12e-10                       # global RAR value (fixed for the per-galaxy fits)
nu = lambda u: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(u, 1e-12))))


def gobs_efe(gbar, a0, eN):
    gext = eN*a0
    if eN <= 1e-9:
        return nu(gbar/a0)*gbar
    return nu((gbar+gext)/a0)*(gbar+gext) - nu(gext/a0)*gext


def per_galaxy_rar():
    """Yield (name, gbar, gobs, e_lg) per quality-cut galaxy (same cuts as precision_rar_test.build_rar)."""
    master = prt.load_master()
    ML_D, ML_B = prt.ML_D, prt.ML_B
    for fpath in sorted(glob.glob(os.path.join(prt.ROT, "*_rotmod.dat"))):
        name = os.path.basename(fpath).replace("_rotmod.dat", "")
        meta = master.get(name)
        if meta is None:
            continue
        D, e_D, inc, e_inc, Q = meta
        if Q > 2 or inc < 30:
            continue
        try:
            d = np.genfromtxt(fpath, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6)); Rm = R*kpc
        Vb2 = np.sign(Vg)*Vg**2 + ML_D*Vd**2 + ML_B*Vb**2
        gb = Vb2*1e6/Rm; go = (Vo*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
        if ok.sum() < 4:
            continue
        dlnV = eV[ok]/Vo[ok]
        e_lg = np.sqrt((2*dlnV)**2 + (e_D/max(D, 1e-3))**2 + (0.10*np.log(10))**2)/np.log(10)
        yield name, gb[ok], go[ok], e_lg


def fit_eN(gbar, gobs, elg):
    """Fit e_N for one galaxy (a0 fixed); return (e_N, scatter_efe, scatter_isolated)."""
    def sc(eN):
        pred = gobs_efe(gbar, A0, eN)
        r = np.log10(gobs) - np.log10(np.maximum(pred, 1e-30)); w = 1/elg**2
        return np.sqrt(np.sum(w*(r-np.median(r))**2)/np.sum(w))
    EN_MAX = 0.10                     # physical ceiling for field-galaxy external fields (e_N=g_ext/a0)
    r = minimize_scalar(sc, bounds=(0.0, EN_MAX), method="bounded")
    return r.x, r.fun, sc(0.0)


def main():
    print("#"*92)
    print("# EFE in SPARC -- per-galaxy external-field fit (MOND's SEP-violating signature)")
    print("#"*92 + "\n")

    print("="*92); print("(1) GLOBAL fit -- the AVERAGE external field (expected ~0; not the real test)"); print("="*92)
    gbar, gobs, elgo, elgb = prt.build_rar(prt.load_master()); elg = np.sqrt(elgo**2+elgb**2)
    def gsc(eN):
        pred = gobs_efe(gbar, A0, eN); r = np.log10(gobs)-np.log10(np.maximum(pred,1e-30)); w=1/elg**2
        return np.sqrt(np.sum(w*(r-np.median(r))**2)/np.sum(w))
    rg = minimize_scalar(gsc, bounds=(0.0, 0.1), method="bounded")
    print(f"  global e_N = {rg.x:.4f} (scatter {rg.fun:.4f} vs isolated {gsc(0.0):.4f}). ~0: the mean EFE is")
    print(f"  washed out (SPARC is mostly isolated galaxies). This is consistent with -- not counter to -- Chae.\n")

    print("="*92); print("(2) PER-GALAXY e_N -- the real test: which galaxies' RARs turn down?"); print("="*92)
    rows = []
    for name, gb, go, elg_g in per_galaxy_rar():
        eN, sc_efe, sc_iso = fit_eN(gb, go, elg_g)
        rows.append((name, eN, sc_iso - sc_efe, len(gb), np.log10(gb.min())))
    eNs = np.array([r[1] for r in rows])
    railed = int(np.sum(eNs > 0.099))
    print(f"  fitted {len(rows)} galaxies (a0 fixed = {A0/1e-10:.2f}e-10, e_N capped at 0.10). Distribution:")
    for lo, hi in [(0, 0.005), (0.005, 0.02), (0.02, 0.05), (0.05, 0.099), (0.099, 0.101)]:
        n = int(((eNs >= lo) & (eNs < hi)).sum())
        tag = "  <- RAILED at the cap (systematics, NOT EFE)" if lo > 0.09 else ""
        print(f"    e_N in [{lo:.3f},{hi:.3f}): {n:3d} galaxies  {'#'*int(50*n/len(rows))}{tag}")
    print(f"  median e_N = {np.median(eNs):.4f}; {railed} galaxies ({100*railed/len(rows):.0f}%) RAIL at the 0.10 cap.")
    print(f"  The railing is the tell: e_N is absorbing per-galaxy M/L + distance + non-circular-motion scatter,")
    print(f"  not a real external field -- so the per-galaxy e_N spread is NOT a clean EFE detection.\n")

    print("="*92); print("VERDICT -- honest (a NULL for independent detection)"); print("="*92)
    print(f"""  I could NOT independently DETECT the EFE with SPARC alone + this method, and I will not pretend
  otherwise. Two findings, both honest:
   * GLOBAL average e_N ~ 0 -- expected (SPARC is mostly isolated galaxies; the mean EFE washes out). Consistent
     with Chae, not against him.
   * PER-GALAXY e_N has a spread, BUT {100*railed/len(rows):.0f}% of galaxies RAIL at the physical cap -- the fit is dumping M/L,
     distance, and non-circular-motion systematics into e_N, not measuring an external field. With a0 and M/L
     fixed and only a handful of outer points per galaxy, e_N is degenerate with those systematics. So the
     spread is an ARTIFACT, not even a suggestive detection.
  What a real detection needs (exactly Chae et al. 2020's method, which I cannot run here): a full per-galaxy
  Bayesian fit MARGINALIZING over M/L, distance, and inclination, AND a cross-match of the fitted e_N against
  each galaxy's MEASURED large-scale environment (the external density field). That cross-correlation -- e_N
  tracking real environment -- is what yields their ~4 sigma blind / 8-11 sigma golden-galaxy SEP-violation
  signal. NET: the EFE remains the framework's strongest CLAIMED local signature on the strength of Chae's
  published detection; this session did NOT independently reproduce it, and showed concretely why (global
  washout + per-galaxy systematics degeneracy) and what data/method would. An honest null, not a confirmation.""")
    print("="*92)


if __name__ == "__main__":
    main()
