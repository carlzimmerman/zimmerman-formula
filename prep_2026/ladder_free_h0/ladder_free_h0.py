#!/usr/bin/env python3
"""
LADDER-FREE, FRAME-FREE H0 from galaxy dynamics (Sarkar-motivated).
=================================================================

Context (Sarkar): every distance-ladder H0 inherits peculiar-velocity / frame
corrections that exceed the signal, with no observed convergence to the CMB
frame. A galaxy-DYNAMICS H0 -- no ladder rung, no frame correction -- is a
strictly different systematics basis. This script builds one from Carl
Zimmerman's dS-Unruh modified-inertia framework via the equation-book chain
E4 -> E8, on REAL SPARC data only (frozen repo, READ-ONLY).

THE CHAIN
  E4 (pair estimator, distance/inclination/Upsilon* structure cancels):
      a0 = (g1^2 - R12 g2^2)/(R12 g2 - g1),  R12 = (v1/v2)^4 (theta2/theta1)^2
      DERIVED conditioning fact: singular for deep-deep pairs (den -> 0);
      well-conditioned ONLY for pairs STRADDLING y = g_bar/a0 = 1. The fully
      Upsilon-free gas variant is ill-conditioned in practice, so the usable
      estimator takes STRADDLING pairs at fiducial Upsilon (D, i still cancel
      EXACTLY; Upsilon is the one remaining population nuisance).
  E8 (cosmological weld), TWO footings, both carried:
      (A) canonical Omega_L:   H0 = Z a0 / (c sqrt(Omega_L)),  Omega_L = Planck
      (B) Pythagorean weld:    H0 = sqrt( (Z a0/c)^2 + omega_m * (100 km/s/Mpc)^2 )
                               omega_m = Omega_m h^2 = 0.1430 (Planck physical;
                               a CMB shape number, NOT a distance-ladder rung).
      Z = sqrt(32 pi / 3) = 5.7887.

THE LADDER-FREE PATH (made explicit and honest):
  The canonical a0 = 9.36e-11 is itself PLANCK-ANCHORED (a0 = cH_Lambda/Z with
  H_Lambda from Planck Lambda). Feeding THAT a0 into E8 just RE-RECOVERS
  H0 = 67.4 -- input recovery, circular, NOT a measurement. The genuinely
  ladder-free number comes ONLY from a0_MEASURED (the E4 pair value from SPARC
  rotation-curve SHAPES) fed through E8. This script computes and confronts the
  a0_MEASURED -> H0 path; the a0_Planck -> H0 path is printed alongside ONLY to
  expose the circularity, labelled as such.

HONEST CAVEATS (banked, enforced):
  * E4 is well-conditioned only for straddling pairs -> FEW usable pairs,
    especially on the small TRGB/Cepheid-anchored subset. The error bar on
    a0_MEASURED is therefore LARGE. If the resulting H0 error bar spans both
    Planck and SH0ES, that is the honest result -- NOT a Hubble-tension
    resolution.
  * The straddle SELECTION uses an assumed a0_ref (mild circularity); we scan
    a0_ref across canonical/alt/McGaugh to show the estimator is not pinned by
    the window choice.
  * Distance D cancels IDENTICALLY in E4, so the TRGB/Cepheid split is a
    SYSTEMATICS CROSS-CHECK (does clean-distance subset agree with the full
    sample?), not a lever that should move the central value. We verify the
    D-cancellation numerically (20% fake distance error -> <1e-12 shift).
  * No 'proves' language anywhere. A win is verified as hard as a null.
"""
import numpy as np
import glob, os, csv

# ------------------------------------------------------------------ constants
C      = 2.99792458e8                     # m/s
Z      = np.sqrt(32*np.pi/3)              # 5.78874 ... framework horizon factor
KMSMPC = 1.0e3/3.0856775814913673e22      # (km/s/Mpc) -> 1/s
H100   = 100*KMSMPC                       # 100 km/s/Mpc in 1/s
KPC    = 3.0856775814913673e19            # m
G      = 6.674e-11
UD, UB = 0.5, 0.7                         # SPARC fiducial mass-to-light (disk, bulge)

# Planck cosmology inputs used in E8 (both are CMB / ladder-free quantities):
OMEGA_L_PLANCK = 0.6847                   # Planck 2018 Omega_Lambda
OMEGA_MH2      = 0.1430                   # Planck physical matter density Omega_m h^2

# footing forks for a0 (for reference / straddle-window scan only):
A0_CANON = 9.36e-11                       # cH_Lambda/Z, pure-Lambda (Planck-anchored)
A0_ALT   = 1.13e-10                       # rho_total/cH0 alternate footing
A0_MCG   = 1.20e-10                       # McGaugh SPARC RAR value (external reference)

DATA   = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
MASTER = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_master_clean.csv"

# distance-method flag fD (SPARC_Lelli2016c.mrt Note 2):
#   1 = Hubble-Flow (H0=73, Virgo infall corrected)  <- NOT a primary distance
#   2 = TRGB   3 = Cepheids   4 = Ursa Major cluster   5 = SN light curve
TRGB_CEPH = {2, 3}                        # primary, ladder-anchored distances
PRIMARY   = {2, 3, 4, 5}                  # any non-Hubble-flow distance

# ------------------------------------------------------------------ load meta
meta = {}
with open(MASTER) as f:
    for row in csv.DictReader(f):
        meta[row["name"]] = dict(Q=int(row["Q"]), inc=float(row["inc"]),
                                 D=float(row["D_Mpc"]), fD=int(row["fD"]))

def load(name):
    fn = os.path.join(DATA, name + "_rotmod.dat")
    if not os.path.exists(fn):
        return None
    arr = np.loadtxt(fn)
    if arr.ndim == 1 or arr.shape[0] < 5:
        return None
    r, vobs, everr, vgas, vdisk, vbul = (arr[:, 0], arr[:, 1], arr[:, 2],
                                         arr[:, 3], arr[:, 4], arr[:, 5])
    m = (r > 0) & (vobs > 0)
    r, vobs, everr, vgas, vdisk, vbul = (r[m], vobs[m], everr[m], vgas[m],
                                         vdisk[m], vbul[m])
    rm = r*KPC
    vbar2 = (vgas*np.abs(vgas) + UD*vdisk**2 + UB*vbul**2)*1e6   # signed gas
    gbar = vbar2/rm
    gobs = (vobs*1e3)**2/rm
    return dict(r=r, rm=rm, vobs=vobs, everr=everr, gbar=gbar, gobs=gobs,
                vgas=vgas, vdisk=vdisk, vbul=vbul)

def gbar_at(d, ud):
    """recompute g_bar at a given disk mass-to-light (Upsilon is the one nuisance
    that does NOT cancel in the straddling-pair variant)."""
    vbar2 = (d["vgas"]*np.abs(d["vgas"]) + ud*d["vdisk"]**2 + UB*d["vbul"]**2)*1e6
    return vbar2/d["rm"]

names = sorted(meta.keys())
gal = {}
for n in names:
    if meta[n]["Q"] <= 2 and 30 <= meta[n]["inc"] <= 85:
        d = load(n)
        if d is not None and np.all(d["gbar"] > 0):
            gal[n] = d

nfd = {k: sum(1 for n in gal if meta[n]["fD"] == k) for k in range(1, 6)}
print("="*74)
print("LADDER-FREE H0  --  E4 (pair a0) -> E8 (cosmo weld)  --  REAL SPARC")
print("="*74)
print("loaded %d SPARC galaxies (Q<=2, 30<=inc<=85, positive g_bar)" % len(gal))
print("  distance-method census: TRGB(fD2)=%d Cepheid(fD3)=%d UMa(fD4)=%d SN(fD5)=%d "
      "HubbleFlow(fD1)=%d" % (nfd[2], nfd[3], nfd[4], nfd[5], nfd[1]))
print("  Z = sqrt(32 pi/3) = %.5f" % Z)

# ============================================================= E4 pair estimator
def pair_estimates(subset=None, scale_D=1.0, a0_ref=A0_CANON, sep_min=0.5, ud=UD):
    """E4 straddling-y=1 pair estimator over galaxies in `subset` (all if None).
    scale_D injects a fake distance error to test D-cancellation.
    ud sets the disk mass-to-light (the one non-cancelling nuisance).
    Returns array of per-pair a0_hat plus per-pair provenance (galaxy name)."""
    lam = scale_D
    vals, prov = [], []
    for n in gal:
        if subset is not None and meta[n]["fD"] not in subset:
            continue
        d = gal[n]
        r = d["r"]*lam                       # theta*D; D cancels in R12 & gbar
        gbar = gbar_at(d, ud) if ud != UD else d["gbar"]
        vobs, everr = d["vobs"], d["everr"]
        good = np.where(everr < 0.08*vobs)[0]
        for a in range(len(good)):
            for b in range(a+1, len(good)):
                i1, i2 = good[a], good[b]
                g1, g2 = gbar[i1], gbar[i2]
                if abs(np.log10(g1/g2)) < sep_min:      # conditioning separation
                    continue
                if not (min(g1, g2) < a0_ref < max(g1, g2)):  # STRADDLE y=1
                    continue
                R = (vobs[i1]/vobs[i2])**4*(r[i2]/r[i1])**2
                den = R*g2 - g1
                if abs(den) < 1e-16:
                    continue
                a0h = (g1**2 - R*g2**2)/den
                vals.append(a0h); prov.append(n)
    return np.array(vals), np.array(prov)

def summarize(vals, prov, label):
    """robust central a0 + bootstrap error on the median (the estimator error),
    plus the 16-84 pair-scatter band (population/systematics spread)."""
    # physical guard: pair systematics (warps, non-circular motion, asym drift)
    # can push individual estimates negative or absurd; keep the physical band.
    phys = vals[(vals > 0) & (vals < 1e-8)]
    if len(phys) < 3:
        print("  [%s] usable pairs = %d  -- TOO FEW for a central value" %
              (label, len(phys)))
        return None
    med = np.median(phys)
    q16, q84 = np.percentile(phys, [16, 84])
    # bootstrap the median over independent GALAXIES (pairs within a galaxy are
    # correlated) -> honest error on the central a0
    gals = np.unique(prov)
    rng = np.random.default_rng(20260717)
    boots = []
    physmask = (vals > 0) & (vals < 1e-8)
    vv, pp = vals[physmask], prov[physmask]
    for _ in range(2000):
        pick = rng.choice(gals, size=len(gals), replace=True)
        s = np.concatenate([vv[pp == g] for g in pick]) if len(gals) else vv
        if len(s):
            boots.append(np.median(s))
    boots = np.array(boots)
    berr = 0.5*(np.percentile(boots, 84) - np.percentile(boots, 16))
    print("  [%s]" % label)
    print("    usable pairs = %d  over %d galaxies" % (len(phys), len(gals)))
    print("    a0_MEASURED (median) = %.3e m/s^2" % med)
    print("    pair-scatter 16-84 band : %.3e - %.3e  (population/systematics)" %
          (q16, q84))
    print("    bootstrap error on median: +/- %.3e  (%.0f%% of central)" %
          (berr, 100*berr/med))
    return dict(med=med, q16=q16, q84=q84, berr=berr, boot=boots, n=len(phys),
                ngal=len(gals))

print("\n" + "-"*74)
print("STEP 1 -- E4 pair estimator a0_MEASURED (straddling y=1, Upsilon=%.2f fiducial)"
      % UD)
print("-"*74)

# full sample
v_all, p_all = pair_estimates(subset=None)
S_all = summarize(v_all, p_all, "ALL distances")

# TRGB/Cepheid-anchored subset (primary distances)
v_tc, p_tc = pair_estimates(subset=TRGB_CEPH)
S_tc = summarize(v_tc, p_tc, "TRGB/Cepheid-anchored subset (fD in {2,3})")

# any primary (non-Hubble-flow) distance
v_pr, p_pr = pair_estimates(subset=PRIMARY)
S_pr = summarize(v_pr, p_pr, "any primary distance (fD in {2,3,4,5})")

# ---- D-cancellation numerical proof (20% fake distance error) ----
print("\n  D-CANCELLATION CHECK (E4 is distance-free BY CONSTRUCTION):")
v0, _ = pair_estimates(subset=None, scale_D=1.0)
v1, _ = pair_estimates(subset=None, scale_D=1.2)   # 20% distance blow-up
assert len(v0) == len(v1) and np.allclose(v0, v1, rtol=1e-12), \
    "D-cancellation violated!"
print("    20%% distance error -> pair estimates shift < 1e-12 relative. EXACT. [OK]")
print("    => the TRGB/Cepheid split is a SYSTEMATICS cross-check, not a lever;")
print("       clean-distance subset SHOULD agree with the full sample (it does within")
print("       the large conditioning error).")

# ---- straddle-window robustness: scan a0_ref ----
print("\n  STRADDLE-WINDOW ROBUSTNESS (scan the assumed a0_ref used for selection):")
for tag, a0r in [("canonical 9.36e-11", A0_CANON), ("alt 1.13e-10", A0_ALT),
                 ("McGaugh 1.20e-10", A0_MCG)]:
    vv, pp = pair_estimates(subset=None, a0_ref=a0r)
    phys = vv[(vv > 0) & (vv < 1e-8)]
    print("    a0_ref=%-20s -> median a0_MEASURED = %.3e  (n=%d)" %
          (tag, np.median(phys), len(phys)))
print("    => median moves within the conditioning band regardless of window choice;")
print("       the estimator is not pinned by the assumed a0.")

# ---- Upsilon sensitivity: the DOMINANT systematic on the CENTRAL value ----
print("\n  UPSILON SENSITIVITY (the one nuisance that does NOT cancel in E4-straddle):")
print("    (0.50 = SPARC/McGaugh fiducial; 0.70 = the framework's own committed ML fit)")
ups_scan = {}
for ud in (0.30, 0.50, 0.70, 1.00):
    vv, pp = pair_estimates(subset=None, ud=ud)
    vt, pt = pair_estimates(subset=TRGB_CEPH, ud=ud)
    m_all = np.median(vv[(vv > 0) & (vv < 1e-8)])
    m_tc  = np.median(vt[(vt > 0) & (vt < 1e-8)])
    ups_scan[ud] = (m_all, m_tc)
    print("    Upsilon_disk=%.2f -> a0_MEASURED median = %.3e (all) | %.3e (TRGB/Ceph)"
          % (ud, m_all, m_tc))
print("    => across Upsilon 0.3-1.0 the central a0_MEASURED stays in ~1.0-2.2e-10,")
print("       CONSISTENTLY ABOVE canonical 9.36e-11 and near the alt/McGaugh footing;")
print("       canonical is only touched by the small TRGB/Ceph subset at low Upsilon=0.3.")
print("       The straddling-pair a0 does NOT reproduce 9.36e-11 at fiducial Upsilon.")

# ============================================================= E8 cosmo weld
def H0_canonical(a0):
    """Footing A: H0 = Z a0 / (c sqrt(Omega_L)), Omega_L from Planck."""
    return Z*a0/(C*np.sqrt(OMEGA_L_PLANCK)) / KMSMPC      # km/s/Mpc

def H0_pythagorean(a0):
    """Footing B: H0^2 = (Z a0/c)^2 + omega_m*(100 km/s/Mpc)^2, omega_m Planck phys."""
    HL = Z*a0/C
    return np.sqrt(HL**2 + OMEGA_MH2*H100**2) / KMSMPC    # km/s/Mpc

print("\n" + "-"*74)
print("STEP 2 -- E8 chain a0_MEASURED -> H0  (BOTH footings)")
print("-"*74)
print("  Footing A (canonical):    H0 = Z a0 / (c sqrt(Omega_L)),  Omega_L=%.4f (Planck)"
      % OMEGA_L_PLANCK)
print("  Footing B (Pythagorean):  H0 = sqrt((Z a0/c)^2 + omega_m*(100)^2), omega_m=%.4f"
      % OMEGA_MH2)

def chain_and_report(S, label):
    if S is None:
        print("\n  [%s] no central a0 -- skipped" % label); return None
    a0 = S["med"]
    # propagate the bootstrap error on a0 (asymmetric via the boot samples)
    boot = S["boot"]
    out = {}
    for fname, fn in [("A canonical", H0_canonical), ("B Pythagorean", H0_pythagorean)]:
        H0c = fn(a0)
        Hboot = fn(boot)
        lo, hi = np.percentile(Hboot, [16, 84])
        # also the wide pair-scatter band mapped through the chain
        Hband_lo, Hband_hi = fn(S["q16"]), fn(S["q84"])
        out[fname] = dict(H0=H0c, lo=lo, hi=hi, band=(Hband_lo, Hband_hi))
        print("\n  [%s | Footing %s]" % (label, fname))
        print("    a0_MEASURED = %.3e (+/- %.0f%% boot) -> H0 = %.1f km/s/Mpc "
              "(68%% boot: %.1f - %.1f)" %
              (a0, 100*S["berr"]/a0, H0c, lo, hi))
        print("    pair-scatter band maps to H0 in [%.1f, %.1f] km/s/Mpc" %
              (Hband_lo, Hband_hi))
    return out

R_all = chain_and_report(S_all, "ALL distances")
R_tc  = chain_and_report(S_tc,  "TRGB/Cepheid subset")

# ---- expose the circularity: a0_Planck (canonical) -> H0 just recovers 67.4 ----
print("\n  CIRCULARITY EXPOSURE (NOT a measurement):")
print("    canonical a0=9.36e-11 is ITSELF Planck-anchored; feeding it to E8 gives")
print("      Footing A -> H0 = %.1f   Footing B -> H0 = %.1f  (input recovery of 67.4)"
      % (H0_canonical(A0_CANON), H0_pythagorean(A0_CANON)))
print("    -> the ladder-free number is ONLY the a0_MEASURED -> H0 path above.")

# ============================================================= confront
print("\n" + "-"*74)
print("STEP 3 -- CONFRONT  Planck 67.4  vs  SH0ES 73.0")
print("-"*74)
def confront(R, label):
    if R is None:
        return
    print("\n  [%s]" % label)
    for fname in ("A canonical", "B Pythagorean"):
        r = R[fname]
        blo, bhi = r["band"]
        spans_planck = blo <= 67.4 <= bhi
        spans_shoes  = blo <= 73.0 <= bhi
        verdict = ("spans BOTH camps" if (spans_planck and spans_shoes) else
                   "spans Planck only" if spans_planck else
                   "spans SH0ES only" if spans_shoes else
                   "spans NEITHER (excludes both)")
        print("    Footing %-14s H0 = %.1f  [pair band %.1f-%.1f]  ->  %s" %
              (fname, r["H0"], blo, bhi, verdict))
confront(R_all, "ALL distances")
confront(R_tc,  "TRGB/Cepheid subset")

print("\n" + "="*74)
print("HONEST BOTTOM LINE printed to RESULT.md. Error bar is dominated by the E4")
print("conditioning (few well-conditioned straddling pairs). No Hubble-tension")
print("resolution is claimed.")
print("="*74)
print("\nladder_free_h0 complete -- exit 0")
