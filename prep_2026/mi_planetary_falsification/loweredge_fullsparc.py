#!/usr/bin/env python3
r"""
HARDEN THE LOWER EDGE OF THE JOINT omega_c WINDOW FROM THE FULL SPARC DEEP-MOND DISTRIBUTION
============================================================================================
(de Sitter-Unruh MODIFIED INERTIA, Carl Zimmerman -- judged on its OWN terms.)

WHAT THIS FIXES.  The joint-window script `window_joint.py` (this dir) set the LOWER edge of the
allowed crossover-corner window from a SINGLE representative deep-MOND orbit (v=25 km/s, y=0.8):
    window_joint.py:73-75  V_DWARF=25e3 ; Y_DEEP=0.8 ; GATE_KEEP=0.90
    window_joint.py:110-112 om_gal = Y_DEEP*a0/V_DWARF ;  k=sqrt(GATE_KEEP/(1-GATE_KEEP)) ; omega_lo=k*om_gal
That is a SOFT SPOT: omega_gal scales with the orbit.  omega_gal = v/r (the orbital ANGULAR frequency)
rises for deeper/faster-in-angle orbits.  The gate is a single-pole low-pass Re G=1/(1+(omega/omega_c)^2);
it must stay OPEN (Re G >= 0.90) at EVERY confirmed deep-MOND orbit or it gates the rotation curves off.
The BINDING lower edge is therefore  3 * MAX(omega_gal)  over the WHOLE confirmed-deep-MOND sample, not
one orbit.  If that MAX is large enough, the lower edge crosses the fixed LLR upper edge and the window
CLOSES -> the framework FAILS at the solar system.  This script recomputes it from real SPARC data.

WHY omega_gal = v_rot / r IS THE FREQUENCY THE MEMORY GATE SEES.  In a circular orbit the centripetal
acceleration vector a_c (magnitude v^2/r, pointing at the center) ROTATES with the orbit at angular rate
omega_orbit = v/r.  The de Sitter-Unruh modified-inertia response acts on the time-dependence of the
acceleration the body actually experiences; the AC content of that acceleration is a tone at exactly the
orbital frequency omega_orbit = v/r (plus harmonics for eccentric orbits, higher still).  So the memory
kernel's low-pass gate G(omega) is probed at omega = omega_orbit = v/r.  (Identically, omega = a_c/v =
(v^2/r)/v = v/r.)  For the deep-MOND onset a_c ~ a0, this is a0/v -- the exact quantity window_joint.py
used, but here evaluated point-by-point on real orbits instead of one representative (v,y).

REUSED MACHINERY (unchanged -- only the lower-edge DRIVER changes):
  * gate + gate-open constant k = sqrt(GATE_KEEP/(1-GATE_KEEP)) with GATE_KEEP=0.90 -> k=3
    (window_joint.py:79 ReG, :110-112 lower edge).
  * LLR upper edge: d ln r/dt = a0 omega_c/g_N <= LLR 2-sigma Gdot/G = 2.42e-14/yr
    (window_joint.py:66-68,136-142) -> omega_hi = (llr_2sig/yr) g_N(Moon)/a0
    = 2.21e-14 (canon) / 1.83e-14 (alt) rad/s.  Recomputed here from the SAME formula, not hard-coded.

SELECTION (stated; the SAME deep-MOND / quality cuts the RAR uses):
  * quality  Q <= 2   (SPARC flag; Q=3 = poor / asymmetric, dropped -- Lelli+2016)
  * inclination >= 30 deg  (below this V_rot deprojection is unreliable)
  * deep-MOND: g_bar = V_bar^2 / r < a0   (y = g_bar/a0 < 1), BOTH a0 footings for the cut
  * V_bar^2 = sign(Vgas)Vgas^2 + Ud Vdisk^2 + Ub Vbul^2, Ud=0.70, Ub=1.4Ud=0.98
    -- the framework's OWN best-fit M/L (rar_framework_a0_mlfit.py:56-61, 0.108 dex).
  * Vobs>0, finite g's.  MAX taken over ALL surviving points across all 175 galaxies.

Every load-bearing number printed; checks compare COMPUTED quantities (no hard-coded verdicts). exit 0/1.
"""
import numpy as np, glob, os, csv, sys

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond); print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

# ------------------------------------------------------------------ constants (match window_joint.py)
C   = 2.99792458e8
YR  = 3.15576e7
MYR = YR*1e6
GYR = YR*1e9
kpc = 3.0857e19
GMearth = 3.986004418e14
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}

# framework M/L (rar_framework_a0_mlfit.py best fit)
UD = 0.70; UB = 1.4*UD

# gate-open requirement (window_joint.py:75,111)
GATE_KEEP = 0.90
K_GATE = np.sqrt(GATE_KEEP/(1.0-GATE_KEEP))     # = 3.0 exactly

# LLR upper edge inputs (window_joint.py:67-68,137-138)
GDOT_LLR_1SIG = 9.6e-15
GDOT_LLR_CEN  = 5.0e-15
LLR_2SIG = GDOT_LLR_CEN + 2*GDOT_LLR_1SIG        # 24.2e-15 /yr

# selection thresholds
Q_MAX   = 2
INC_MIN = 30.0

DATA = os.path.join("/Users/carlzimmerman/new_physics/zimmerman-formula/real_research","data")
SPARC = os.path.join(DATA,"sparc_data")

def ReG(omega, wc): return 1.0/(1.0+(omega/wc)**2)

# ------------------------------------------------------------------ gate sanity (reused, not re-derived)
print("#"*100); print("# GATE reuse check: k = sqrt(GATE_KEEP/(1-GATE_KEEP)) with GATE_KEEP=0.90 -> lower edge = k*MAX(omega_gal)")
print("#"*100)
check("k == 3 exactly (window_joint.py:111 constant reused)", abs(K_GATE-3.0)<1e-12)
# at omega = omega_c/k the gate is exactly GATE_KEEP open:
check("Re G(omega_gal, wc=k*omega_gal) == GATE_KEEP (the lower-edge condition is self-consistent)",
      abs(ReG(1.0, K_GATE) - GATE_KEEP) < 1e-12)

# ------------------------------------------------------------------ LLR upper edge (reused formula)
gN_moon = GMearth/3.844e8**2
UPPER = {lab: (LLR_2SIG/YR)*gN_moon/a0 for lab,a0 in A0.items()}
print(f"\n LLR upper edge (window_joint.py:136-142 formula, recomputed): d ln r/dt = a0 wc/g_N <= {LLR_2SIG:.2e}/yr")
print(f"   g_N(Moon) = {gN_moon:.4e} m/s^2  ->  omega_hi = (LLR2sig/yr) g_N/a0 =")
for lab in A0: print(f"      {lab}: {UPPER[lab]:.3e} rad/s")
check("canon upper edge reproduces window_joint.py value 2.21e-14 (+-2%)", abs(UPPER['canon']/2.21e-14-1)<0.02)
check("alt   upper edge reproduces window_joint.py value 1.83e-14 (+-2%)", abs(UPPER['alt']/1.83e-14-1)<0.02)

# ------------------------------------------------------------------ load master table (Q, inc)
meta = {}
with open(os.path.join(DATA,"sparc_master_clean.csv")) as fh:
    for row in csv.DictReader(fh):
        meta[row["name"].strip()] = (float(row["inc"]), int(float(row["Q"])), float(row["Vflat"]))
print(f"\n master table: {len(meta)} galaxies with (inc, Q, Vflat)")

def galname(path):
    b = os.path.basename(path)
    return b[:-len("_rotmod.dat")] if b.endswith("_rotmod.dat") else b

# ------------------------------------------------------------------ scan every rotmod point, both footings
print("\n"+"#"*100); print("# SCAN: omega_gal = v_rot/r over ALL confirmed deep-MOND points (Q<=2, inc>=30, g_bar<a0)")
print("#"*100)
files = sorted(glob.glob(os.path.join(SPARC,"*_rotmod.dat")))
print(f" rotmod files found: {len(files)}")

results = {}
for lab, a0 in A0.items():
    n_gal_used=0; n_gal_nometa=0; n_pts_total=0; n_pts_deep=0
    best = None            # (omega_gal, galaxy, r_kpc, v, gbar, y)
    per_gal_max = []       # (omega_gal_max_in_gal, galaxy)
    best_noinner = None    # robustness: drop each galaxy's single innermost radius (rising-curve / beam-smear guard)
    for f in files:
        d = np.genfromtxt(f, comments="#")
        if d.ndim!=2 or d.shape[1]<6: continue
        name = galname(f)
        if name not in meta:
            n_gal_nometa+=1; continue
        inc, Q, vflat = meta[name]
        if Q>Q_MAX or inc<INC_MIN: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul = (d[:,i] for i in range(6))
        order = np.argsort(R)                    # innermost = first in radius
        Rm = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + UD*Vdisk**2 + UB*Vbul**2
        gbar = Vbar2*1e6/Rm                     # m/s^2
        gobs = (Vobs*1e3)**2/Rm
        om   = (Vobs*1e3)/Rm                    # omega_gal = v_rot/r  [rad/s]
        ok = (gbar>0)&(gobs>0)&(Vobs>0)&np.isfinite(gbar)&np.isfinite(gobs)&(R>0)
        deep = ok & (gbar < a0)                 # y = gbar/a0 < 1
        n_pts_total += int(ok.sum()); n_pts_deep += int(deep.sum())
        # robustness mask: exclude the single innermost radius of this galaxy
        inner_idx = order[0]
        noinner = deep.copy(); noinner[inner_idx] = False
        if deep.any():
            n_gal_used += 1
            idx = np.where(deep)[0]
            j = idx[np.argmax(om[idx])]
            gmax = om[j]
            per_gal_max.append((gmax, name))
            if best is None or gmax>best[0]:
                best = (gmax, name, R[j], Vobs[j], gbar[j], gbar[j]/a0)
        if noinner.any():
            idx2 = np.where(noinner)[0]
            j2 = idx2[np.argmax(om[idx2])]
            if best_noinner is None or om[j2]>best_noinner[0]:
                best_noinner = (om[j2], name, R[j2], Vobs[j2], gbar[j2]/a0)
    per_gal_max.sort(reverse=True)
    om_max = best[0]
    omega_lo = K_GATE*om_max
    omega_hi = UPPER[lab]
    open_ = omega_hi > omega_lo
    om_crit = omega_hi/K_GATE               # the MAX(omega_gal) at which lower edge == upper edge (closes)
    results[lab] = dict(om_max=om_max, lo=omega_lo, hi=omega_hi, open=open_, best=best,
                        top=per_gal_max[:8], n_gal=n_gal_used, n_deep=n_pts_deep, n_tot=n_pts_total,
                        om_crit=om_crit, best_noinner=best_noinner)

    print(f"\n"+"="*100)
    print(f" FOOTING = {lab}  (a0={a0:.3e},  deep-MOND cut g_bar<a0)")
    print("="*100)
    print(f"   galaxies passing Q<=2 & inc>=30 with >=1 deep-MOND point: {n_gal_used}")
    print(f"   points: total-usable {n_pts_total}, deep-MOND (g_bar<a0) {n_pts_deep}")
    print(f"   TOP 8 galaxies by max omega_gal (rad/s):")
    for g,nm in per_gal_max[:8]:
        print(f"      {nm:<14} omega_gal_max = {g:.3e}   (tau = {1/g/MYR:.1f} Myr)")
    bg = best
    print(f"\n   >>> BINDING MAX(omega_gal) = {om_max:.3e} rad/s")
    print(f"       set by galaxy {bg[1]} at r={bg[2]:.2f} kpc, V_rot={bg[3]:.1f} km/s, "
          f"g_bar={bg[4]:.3e} (y=g_bar/a0={bg[5]:.3f})")
    print(f"   HARDENED LOWER EDGE = 3 x MAX = {omega_lo:.3e} rad/s   (tau = {1/omega_lo/MYR:.2f} Myr)")
    print(f"   LLR UPPER EDGE (fixed)         = {omega_hi:.3e} rad/s   (tau = {1/omega_hi/MYR:.2f} Myr)")
    if open_:
        print(f"   ==> WINDOW SURVIVES: omega_c in [{omega_lo:.3e}, {omega_hi:.3e}] rad/s  width x{omega_hi/omega_lo:.3f}")
    else:
        print(f"   ==> WINDOW CLOSES: lower edge {omega_lo:.3e} > upper edge {omega_hi:.3e}  "
              f"(lower exceeds upper by x{omega_lo/omega_hi:.2f}) -> FALSIFIED at planets")
    # SENSITIVITY: how close is the closure boundary?  Any confirmed deep-MOND orbit with
    # omega_gal > om_crit = omega_hi/3 closes this footing.
    margin = om_crit/om_max
    print(f"   SENSITIVITY: footing CLOSES if MAX(omega_gal) > omega_hi/3 = {om_crit:.3e} rad/s.")
    print(f"                current MAX = {om_max:.3e} is x{margin:.3f} below that => headroom {100*(margin-1):+.1f}%"
          f"  (any deep-MOND orbit faster than {om_crit:.3e} rad/s would FALSIFY this footing)")
    bn = best_noinner
    lo_ni = K_GATE*bn[0]
    print(f"   ROBUSTNESS (drop each galaxy's innermost radius): MAX->{bn[0]:.3e} ({bn[1]}, r={bn[2]:.2f} kpc, "
          f"V={bn[3]:.1f}) -> lower edge {lo_ni:.3e} => window {'SURVIVES' if omega_hi>lo_ni else 'CLOSES'}"
          f" (width x{omega_hi/lo_ni:.3f})")

# ------------------------------------------------------------------ compare to the old single-orbit edge
print("\n"+"#"*100); print("# COMPARISON to the old SINGLE-ORBIT lower edge (window_joint.py:110, v=25km/s y=0.8)")
print("#"*100)
for lab, a0 in A0.items():
    old_om_gal = 0.8*a0/25e3
    old_lo = K_GATE*old_om_gal
    new = results[lab]
    print(f" [{lab}] old omega_gal(1 orbit) = {old_om_gal:.3e} -> old lower edge {old_lo:.3e}")
    print(f"        FULL-SPARC MAX omega_gal = {new['om_max']:.3e} -> hardened lower edge {new['lo']:.3e}"
          f"  (x{new['lo']/old_lo:.2f} higher)")

# ------------------------------------------------------------------ VERDICT
print("\n"+"="*100)
allopen = all(results[l]["open"] for l in results)
if allopen:
    print(" VERDICT: window SURVIVES the full-SPARC hardening on BOTH footings.")
    for lab in A0:
        r=results[lab]
        print(f"   {lab}: [{r['lo']:.3e}, {r['hi']:.3e}] rad/s (width x{r['hi']/r['lo']:.3f}); "
              f"MAX set by {r['best'][1]} (r={r['best'][2]:.2f} kpc, V={r['best'][3]:.1f} km/s)")
    print("   The framework's gated Reading C still passes the solar system -- but the window is NARROWER")
    print("   than the single-orbit estimate; the corner remains a FREE 5th constant (not forced).")
else:
    print(" VERDICT: window CLOSES on at least one footing -> the framework is FALSIFIED at the solar system.")
    for lab in A0:
        r=results[lab]
        state = "SURVIVES" if r["open"] else "CLOSES"
        print(f"   {lab}: lower {r['lo']:.3e} vs upper {r['hi']:.3e} -> {state}")
print("="*100)
print(f" loweredge_fullsparc: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
sys.exit(0 if PASS else 1)
