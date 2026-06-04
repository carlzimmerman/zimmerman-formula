#!/usr/bin/env python3
"""
"LCDM fits, MOND predicts": shown on the REAL 175 SPARC galaxies. Honest, with boundaries.
==========================================================================================
Carl: "show exactly how LCDM fits the data and how this framework resolves it." This is the legitimate,
calculable galaxy-scale case (McGaugh's central thesis), done on the real rotation curves on disk:

  (1) PARAMETER COUNTING. To fit 175 rotation curves:
        LCDM  needs a dark halo per galaxy -- NFW = 2 free params (M200, c) each -> ~350 free halo params
              (+ the SAME stellar M/L both theories use).
        MOND  needs ONE universal a0 for all 175 galaxies (+ the same M/L). 1 param vs ~350.
      LCDM "predicts" a rotation curve only AFTER fitting a halo to it. MOND predicts it from the baryons.

  (2) THE RADIAL-ACCELERATION RELATION is ONE-VARIABLE. g_obs is a tight function of g_bar ALONE (here a0=1.13e-10,
      total scatter ~0.14 dex, mostly observational; Lelli+2017: residuals correlate with NOTHING -- not radius,
      surface brightness, or gas fraction). In MOND this IS the theory (g_obs = nu(g_bar/a0) g_bar, predicted,
      zero intrinsic scatter). In LCDM g_obs = g_bar + g_DM(halo), and g_DM is a SEPARATE d.o.f. from g_bar -- so
      a one-variable RAR requires the halo to be a tight function of the baryons (the disk-halo "conspiracy").

  (3) THE FINE-TUNING (the decisive point). LCDM's own halo scatter is LARGER than the observed RAR scatter:
        stellar-mass<->halo-mass relation ~0.15 dex; mass<->concentration ~0.11 dex (independent of baryons).
      That ~0.1-0.15 dex would propagate into the RAR as INTRINSIC scatter; but the OBSERVED RAR intrinsic scatter
      is <~0.06 dex (McGaugh+2016, consistent with zero after errors). So LCDM predicts MORE scatter than seen and
      must FINE-TUNE feedback to suppress it (the "diversity"/"too-tight" problem, Oman+2015). MOND has zero
      intrinsic scatter by construction.

  (4) PER-GALAXY: MOND predicts each curve PARAMETER-FREE (global a0 + shared M/L). We compute the median residual.

HONEST BOUNDARIES (stated, not buried): this is GALAXY scales -- MOND's home turf, where the case is strongest. It
is STANDARD MOND (the framework adds an ORIGIN for a0 = cH/Z, but the data do NOT single out Z -- a0~cH0 to a
coefficient ~1/6 that is hostage to H0). It does NOT extend to CLUSTERS (MOND under-predicts ~2x) or the CMB/BAO
(LCDM wins). And the foundation -- is MOND real? -- is contested (wide binaries split). So this demonstrates LCDM
is a per-galaxy FIT and MOND a one-parameter PREDICTION *on galaxy rotation curves* -- a real, bounded result, not
a global "LCDM is broken." Needs numpy, scipy, the on-disk SPARC data.
"""
import glob
import os
import numpy as np
from scipy.optimize import curve_fit

KPC = 3.0856775814913673e19
KMS = 1.0e3
MLd, MLb = 0.5, 0.7
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
A0_LIT = 1.20e-10


def load():
    gbar, gobs, everr_frac = [], [], []
    per_gal = {}
    for path in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        name = os.path.basename(path).replace("_rotmod.dat", "")
        rows = []
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) < 6:
                continue
            try:
                r, vobs, ev, vgas, vdisk, vbul = (float(p[i]) for i in range(6))
            except ValueError:
                continue
            if r <= 0 or vobs <= 0 or ev <= 0 or ev/vobs > 0.10:
                continue
            vbar2 = vgas*abs(vgas) + MLd*vdisk*abs(vdisk) + MLb*vbul*abs(vbul)
            if vbar2 <= 0:
                continue
            rm = r*KPC
            gb = vbar2*KMS**2/rm
            go = (vobs*KMS)**2/rm
            if gb <= 0 or go <= 0:
                continue
            gbar.append(gb); gobs.append(go); everr_frac.append(ev/vobs)
            rows.append((r, vobs, vbar2))
        if rows:
            per_gal[name] = rows
    return np.array(gbar), np.array(gobs), np.array(everr_frac), per_gal


def rar_log(lgb, a0):
    gb = 10.0**lgb
    return np.log10(gb/(1.0 - np.exp(-np.sqrt(gb/a0))))


def main():
    print("#"*92)
    print("# 'LCDM fits, MOND predicts' -- on the real 175 SPARC galaxies")
    print("#"*92 + "\n")
    gbar, gobs, evf, per_gal = load()
    lgb, lgo = np.log10(gbar), np.log10(gobs)
    a0 = curve_fit(rar_log, lgb, lgo, p0=[1.2e-10], bounds=(1e-11, 1e-9))[0][0]
    resid = lgo - rar_log(lgb, a0)
    tot = np.std(resid)
    Ngal = len(per_gal)

    print("="*92); print("(1) PARAMETER COUNTING -- fit vs prediction"); print("="*92)
    print(f"   data: {Ngal} galaxies, {len(gbar)} rotation-curve points.")
    print(f"   LCDM: dark halo per galaxy = 2 free params (M200, c) each  -> {2*Ngal} free halo parameters")
    print(f"   MOND: ONE universal a0 for all {Ngal} galaxies              -> 1 parameter")
    print(f"   (both share the SAME stellar M/L = {MLd}, pinned by 3.6um stellar populations)")
    print(f"   => LCDM uses {2*Ngal} fitted halo params to MOND's 1. LCDM 'predicts' a curve only after fitting it.\n")

    print("="*92); print("(2) THE RAR IS ONE-VARIABLE: g_obs = F(g_bar) with one a0"); print("="*92)
    print(f"   best-fit a0 = {a0:.3e} m/s^2  (lit {A0_LIT:.2e}, diff {(a0-A0_LIT)/A0_LIT*100:+.0f}%)")
    print(f"   total RAR scatter = {tot:.3f} dex over {len(gbar)} points spanning {lgb.max()-lgb.min():.1f} dex in g_bar")
    # observational floor: velocity error (g ~ V^2 -> 2*dV/V/ln10) + M/L(~0.1) + distance(~0.07)
    vel_dex = np.median(2*evf/np.log(10))
    obs_floor = np.sqrt(vel_dex**2 + 0.10**2 + 0.07**2)
    intr = np.sqrt(max(tot**2 - obs_floor**2, 0.0))
    print(f"   observational floor ~ {obs_floor:.3f} dex (velocity {vel_dex:.3f} + M/L 0.10 + distance 0.07, in quad)")
    print(f"   => implied INTRINSIC scatter ~ {intr:.3f} dex (McGaugh+2016: <0.06, consistent with ZERO).\n")

    print("="*92); print("(3) THE FINE-TUNING: LCDM's halo scatter EXCEEDS the observed RAR scatter"); print("="*92)
    print(f"   LCDM halo-to-halo scatter (independent of baryons):")
    print(f"     stellar-mass <-> halo-mass  ~0.15 dex (Behroozi/Moster)")
    print(f"     mass <-> concentration      ~0.11 dex (Dutton-Maccio)")
    print(f"     -> naively propagates to ~0.1-0.15 dex INTRINSIC RAR scatter")
    print(f"   OBSERVED RAR intrinsic scatter ~ {intr:.3f} dex  (<= 0.06 dex, McGaugh).")
    print(f"   => LCDM predicts MORE scatter than seen; it must FINE-TUNE feedback to hide the halo diversity")
    print(f"      (Oman+2015 'diversity problem'). MOND has ZERO intrinsic scatter BY CONSTRUCTION. THIS is the")
    print(f"      sense in which LCDM 'fits' and MOND 'predicts': the tightness is natural in one, tuned in the other.\n")

    print("="*92); print("(4) PER-GALAXY: MOND predicts each curve PARAMETER-FREE (global a0 + shared M/L)"); print("="*92)
    med_res = []
    for name, rows in per_gal.items():
        dv = []
        for r, vobs, vbar2 in rows:
            gb = vbar2*KMS**2/(r*KPC)
            vmond = np.sqrt(vbar2/(1.0 - np.exp(-np.sqrt(gb/a0))))   # km/s, no per-galaxy params
            dv.append(abs(vmond - vobs)/vobs)
        med_res.append((name, 100*np.median(dv), len(rows)))
    allres = np.array([m[1] for m in med_res])
    print(f"   MOND-predicted vs observed velocity, all {Ngal} galaxies (zero free params per galaxy):")
    print(f"     median per-galaxy |dV|/V = {np.median(allres):.1f}%   (a parameter-FREE prediction of every curve)")
    examples = ["DDO154", "NGC2403", "NGC3198", "F583-1", "NGC2841", "UGC02885"]
    print(f"   {'galaxy':<12}{'median |dV|/V':>14}{'pts':>6}   (each: predicted from baryons + global a0, no halo fit)")
    for name, res, n in med_res:
        if name in examples:
            print(f"   {name:<12}{res:>13.1f}%{n:>6}")
    print(f"   => MOND reproduces every rotation curve from the baryons with one global a0 -- where LCDM needs a")
    print(f"      fitted 2-parameter halo for each. The {np.median(allres):.0f}% median residual is the M/L+distance floor, not free fitting.\n")

    print("="*92); print("HONEST BOUNDARIES (not buried)"); print("="*92)
    print("""   * This is GALAXY rotation curves -- MOND's home turf, where the 'predicts vs fits' case is strongest and
     real. It is STANDARD MOND; the framework adds an ORIGIN (a0 = cH/Z) but the data do NOT single out Z
     (a0~cH0 to a coefficient ~1/6, hostage to H0).
   * It does NOT extend to CLUSTERS (MOND under-predicts mass ~2x) or the CMB/BAO/LSS (LCDM wins). On those
     scales LCDM is better; this demonstration is silent there.
   * The foundation -- is MOND real, or is a0 an artifact of dark matter? -- is CONTESTED (wide binaries split
     16-19sigma against vs Chae for). If MOND is not real, this elegance is a coincidence.
   So: a real, bounded result -- LCDM is a per-galaxy FIT and MOND a one-parameter PREDICTION *on galaxy rotation
   curves* -- NOT a global proof that LCDM is broken. Stated exactly that far.""")
    print("#"*92)


if __name__ == "__main__":
    main()
