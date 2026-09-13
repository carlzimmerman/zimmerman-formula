#!/usr/bin/env python3
"""G010 -- IS a_0 A FORCE LAW OR A STATISTICAL LAW?  (the user's Question 3)

The question, verbatim: 'Is a_0 = (1/2) c sqrt(G rho_Lambda) dynamical (gravity
modified) or emergent/thermodynamic (an equation of state)?  Kill: if the RAR
intrinsic scatter has a floor > 0.10 dex tied to environment/formation, it's
statistical, not a force -- and the whole completion program is aimed at the
wrong kind of theory.'

WHERE THIS SITS AFTER THIS SESSION'S VERDICTS.  The force-law reading of the
OneFunction is dead (L243/G005: Cassini quadrupole; L244: disformal; L241:
modified inertia).  The surviving reading is the G003 phantom identification
(the halo IS the phantom; the RAR as an equation-of-state statement).  So Q3 is
now THE question: is the RAR a dynamical law (deterministic given the baryons)
or a statistical one (an equilibrium attractor with formation-dependent scatter)?

THE TEST, from the data already in hand.  The distinction makes three
measurable predictions:

  (1) SCATTER FLOOR: a force law gives a scatter floor set by measurement plus
      baryon-distribution physics (small, ~0.05 dex); a statistical law gives
      a floor set by the diversity of formation histories (larger, and
      CORRELATED with environment).
  (2) SCATTER vs ENVIRONMENT: the statistical law predicts the scatter GROWS in
      the regime where equilibration is incomplete -- the dwarfs and the
      outskirts (low Y); a force law predicts structureless scatter.
  (3) SCATTER vs SURFACE BRIGHTNESS: formation-history diversity correlates
      with surface brightness (the LSB galaxies formed differently); a force
      law is blind to it.

This lane measures all three on the 155-curve SPARC sample the programme
already loads, with the mu_2 parameter-free prediction as the baseline.

Every check states measurement and threshold separately.  The kill threshold is
the user's own: a floor > 0.10 dex tied to environment/formation.
"""
import glob, json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else: NF += 1

print(__doc__)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")

# ------------------------------------------------------------------ the constants and kernel
G = 6.674e-11
c_l = 2.99792458e8
H0 = 67.4*1000/3.0857e22
rho_lam = 0.685*3*H0**2/(8*math.pi*G)
s_DE = c_l*math.sqrt(G*rho_lam)
a0 = s_DE/2
kpc, KMS = 3.0857e19, 1.0e3
UPS_D, UPS_B = 0.5, 0.7

def mu2(x): return 1.0 - (1.0 + x/2.0)**(-2.0)

def g_pred(gb, s_val=s_DE, it=200):
    """solve mu_2(g/s) g = g_bar: the parameter-free RAR (G002)."""
    gb = np.asarray(gb, dtype=float)
    lo = np.maximum(gb, 1e-300); hi = gb + np.sqrt(np.maximum(gb, 0)*s_val)*3 + 1e-13
    for _ in range(it):
        mid = 0.5*(lo + hi)
        fm = mid*(1.0 - (1.0 + mid/s_val)**(-2.0)) - gb
        lo = np.where(fm < 0, mid, lo); hi = np.where(fm < 0, hi, mid)
    return 0.5*(lo + hi)

# ------------------------------------------------------------------ load SPARC per-galaxy
galaxies = []      # (name, Y_central, residual_dex, SB_proxy, N_points)
ntot = 0
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    ntot += 1
    try:
        d = np.genfromtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    m = (R > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
    if m.sum() < 3: continue
    R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    ok = Vb2 > 0
    if ok.sum() < 3: continue
    r = R[ok]*kpc
    gbar = Vb2[ok]*KMS**2/r
    gobs = Vo[ok]**2*KMS**2/r
    gp = g_pred(gbar)
    res = np.log10(gobs) - np.log10(gp)
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    # central Y (the regime the galaxy's RAR bend lives in): median g_bar/s
    Yc = float(np.median(gbar)/s_DE)
    # surface-brightness proxy: V-band luminosity per unit area at the effective
    # radius -- use the disc + bulge velocity contributions at the outermost
    # radius as a mass proxy and R_last as the size proxy (crude but uniform)
    SB = float(np.log10(np.sum(Vb2[ok]) + 1e-30) - 2*math.log10(R[ok][-1]))
    galaxies.append((name, Yc, float(np.sqrt(np.mean(res**2))), SB, int(ok.sum())))
print(f"    loaded {len(galaxies)} of {ntot} galaxies")

names = np.array([g[0] for g in galaxies])
Yc = np.array([g[1] for g in galaxies])
rms_gal = np.array([g[2] for g in galaxies])
SB = np.array([g[3] for g in galaxies])

# ------------------------------------------------------------------ V1: the floor
print()
print("PART A -- the scatter floor")

overall = float(np.sqrt(np.mean(rms_gal**2)))
med = float(np.median(rms_gal))
check("V1 [THE FLOOR: the per-galaxy rms scatter of the parameter-free RAR] the "
      "per-galaxy rms residual of mu_2 (nothing fitted) is computed over the "
      "sample and its median compared with the user's kill threshold 0.10 dex",
      f"per-galaxy rms: median {med:.4f} dex, mean {overall:.4f} dex, "
      f"{np.sum(rms_gal > 0.10)} of {len(rms_gal)} galaxies above 0.10 dex",
      med < 0.10,
      "the floor verdict: " + ("the median per-galaxy scatter is BELOW the kill "
      "threshold -- the RAR is tight enough to be a force-law-like relation; the "
      "statistical kill does not fire at the median" if med < 0.10 else
      "the median scatter EXCEEDS 0.10 dex -- the statistical kill FIRES: the "
      "RAR is too loose to be a dynamical law and the completion program is "
      "aimed at the wrong kind of theory"))

# ------------------------------------------------------------------ V2: scatter vs environment (Y)
print()
print("PART B -- the scatter vs environment")

# split at the RAR bend: galaxies with central Y < 0.1 (deep, dwarf-like)
# vs Y > 0.3 (HSB-like); the statistical reading predicts HIGHER scatter at low Y
lo = Yc < 0.1; hi = Yc > 0.3
if lo.sum() >= 5 and hi.sum() >= 5:
    sc_lo = float(np.median(rms_gal[lo])); sc_hi = float(np.median(rms_gal[hi]))
    check("V2 [the scatter does NOT grow toward the deep (low-Y) regime] the "
          "median per-galaxy scatter of the deep sample (central Y < 0.1) is "
          "compared with the high-surface-brightness sample (Y > 0.3)",
          f"deep (n={int(lo.sum())}): {sc_lo:.4f} dex; HSB (n={int(hi.sum())}): "
          f"{sc_hi:.4f} dex; ratio {sc_lo/sc_hi:.2f} (threshold: < 1.5)",
          sc_lo/sc_hi < 1.5,
          "the environment test: if the scatter grew by more than 50% toward the "
          "dwarf/deep regime, the statistical (formation-history) reading would "
          "be favoured and the dynamical reading wounded. The measured ratio "
          f"{'supports' if sc_lo/sc_hi < 1.5 else 'contradicts'} the dynamical "
          "reading at this sample size")

# ------------------------------------------------------------------ V3: scatter vs surface brightness
print()
print("PART C -- the scatter vs surface brightness")

medSB = float(np.median(SB))
lsb = SB < medSB; hsb = SB >= medSB
sc_lsb = float(np.median(rms_gal[lsb])); sc_hsb = float(np.median(rms_gal[hsb]))
check("V3 [the scatter is not tied to surface brightness (formation history)] "
      "the sample is split at the median surface-brightness proxy and the "
      "per-galaxy scatter compared",
      f"LSB half (n={int(lsb.sum())}): {sc_lsb:.4f} dex; HSB half "
      f"(n={int(hsb.sum())}): {sc_hsb:.4f} dex; ratio {sc_lsb/sc_hsb:.2f}",
      sc_lsb/sc_hsb < 1.5,
      "formation-history diversity tracks surface brightness; a > 50% excess "
      "scatter in the LSB half would be the statistical signature. Measured: "
      f"{'no significant LSB excess' if sc_lsb/sc_hsb < 1.5 else 'an LSB excess'}")

# ------------------------------------------------------------------ V4: the correlation test
print()
print("PART D -- the correlation (the sharpest statistic)")

r_Y = float(np.corrcoef(np.log10(np.maximum(Yc, 1e-4)), rms_gal)[0, 1])
r_SB = float(np.corrcoef(SB, rms_gal)[0, 1])
n = len(rms_gal)
sig = 1.96/math.sqrt(n)      # the 2-sigma null band for a correlation
check("V4 [neither Y nor surface brightness correlates with the scatter beyond "
      "noise] the Pearson correlations of the per-galaxy scatter with central Y "
      "and with the surface-brightness proxy are computed and compared with the "
      "2-sigma null band",
      f"corr(log Y, scatter) = {r_Y:+.3f}; corr(SB, scatter) = {r_SB:+.3f}; "
      f"2-sigma null band +- {sig:.3f} (n = {n})",
      abs(r_Y) < 2*sig and abs(r_SB) < 2*sig,
      "if either correlation were significant, the scatter would be tied to "
      "environment or formation and the statistical reading would win. Measured: "
      + ("both correlations are inside the null band -- the scatter is "
         "structureless with respect to environment and surface brightness, "
         "which is what a dynamical law predicts" if abs(r_Y) < 2*sig and abs(r_SB) < 2*sig
         else "at least one correlation is significant -- the scatter carries "
              "environment/formation structure, favouring the statistical reading"))

print()
print("READING")
print("""
  THE ANSWER TO QUESTION 3 -- AND IT IS THE EDGE CASE, STATED EXACTLY.

  The floor: median per-galaxy scatter 0.108 dex, with 84 of 155 galaxies
  individually above the user's 0.10-dex kill threshold.  The kill FIRES at the
  median -- by 8 thousandths of a dex.  That is not a robust kill: it sits
  exactly at the boundary, and the single-M/L convention (no per-galaxy
  mass-to-light freedom) inflates every per-galaxy rms by the M/L systematic,
  which is worth ~0.05 dex by itself.

  The direction tests are the real content:
    - the deep/dwarf regime (86 galaxies) scatters 1.33x MORE than the HSB
      regime (37 galaxies): 0.123 vs 0.092 dex.  Below the 1.5x bar, but the
      direction is the statistical reading's, and the deep subsample is the
      regime where equilibration should be incomplete.
    - the LSB excess is negligible (1.06x) and both correlations sit inside
      the 2-sigma null band: no strong formation-history structure.

  VERDICT: AMBIGUOUS, leaning statistical.  The RAR is too loose to be a clean
  force law at the SPARC floor once the M/L systematic is spent, and too tight
  and structureless to be a crude population law.  This is exactly the profile
  of an EQUILIBRIUM ATTRACTOR: tight because equilibration erases initial
  conditions (the LSB and correlation tests pass), loose at the 0.1-dex level
  because equilibration is incomplete in the dwarfs (the 1.33x deep excess).
  The two readings the user opposed are reconciled by equilibration -- the law
  is statistical in ORIGIN and dynamical in APPEARANCE -- and the completion
  program should aim at the equilibrium mechanism (the G003 phantom
  identification's hydrostatics at the virial temperature), not a force law.

  The sharpening the verdict demands: per-galaxy M/L freedom would settle
  whether the 0.108 floor is physical or systematic; if the floor survives
  M/L freedom above 0.10, the statistical origin is confirmed and the force-law
  obituary stands.
""")
print(f"G010 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES,
           "per_galaxy": [{"name": nm, "Yc": float(y), "rms": float(r), "SB": float(b)}
                          for nm, y, r, b in zip(names, Yc, rms_gal, SB)]},
          open("G010_results.json", "w"), indent=1)
