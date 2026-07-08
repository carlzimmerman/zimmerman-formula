"""
CONFRONT.py -- high-z BTFR offset vs z=0: observed data vs Branch A/B/C.

Framework's OWN inertia relation (deep-MOND baryonic TF): v^4 = G*M_b*a0(z).
  fixed M_b:  dlog10(v)   = (1/4)*log10(a0(z)/a0(0))       [velocity axis]
  fixed v  :  dlog10(M_b) = -    log10(a0(z)/a0(0))        [mass axis]
Literature quotes Delta_b = MASS offset at fixed v vs the LOCAL (Lelli+2016) BTFR.
Convert everything to a common VELOCITY-axis offset dlog10(v) = -(1/4)*Delta_b(mass),
so a POSITIVE dlog10(v) => disc ABOVE z=0 BTFR (faster at fixed mass), NEGATIVE => BELOW.

Branch A (declining a0): dlog10(v) < 0 at z>~1  => discs BELOW.  (z=3: -0.033 dex)
Branch B (rising a0)   : dlog10(v) > 0          => discs ABOVE.  (z=3: +0.165 dex)
Branch C (constant)    : dlog10(v) = 0          => ON.
"""
import numpy as np

# ---------------- a0(z) branches (footing cancels in ratio) ----------------
Om, OL = 0.315, 0.685
w0, wa = -0.752, -0.86
def a(z): return 1.0/(1.0+z)
def rhoDE_ratio(z):
    A=a(z); return A**(-3.0*(1.0+w0+wa))*np.exp(3.0*wa*(A-1.0))
def E(z): return np.sqrt(Om*(1.0+z)**3+OL)
def ratA(z): return np.sqrt(rhoDE_ratio(z))
def ratB(z): return E(z)
def dv_fixedMb(ratio): return 0.25*np.log10(ratio)  # velocity-axis offset

# ---------------- observed data (from Scout B table) ----------------
# Each entry: velocity-axis offset dlog10(v) vs z=0 (POSITIVE=ABOVE, NEGATIVE=BELOW),
# with 1-sigma. Literature Delta_b are MASS offsets at fixed v; convert dv = -Delta_b/4.
# weight: quoted zero-point measurements full weight; single-object inferred down-weighted;
# v-definition mismatch (not outer flat v_circ tied to Lelli calibration) down-weighted.
data = [
    # name, z, dv (velocity-axis, dex), sigma_dv, weight, quoted?, note
    # Ubler+2017 KMOS3D z0.9: Delta_b(mass)=-0.44+/-0.05 => dv=+0.11+/-0.0125 ABOVE
    ("Ubler2017_z0.9", 0.9, +0.110, 0.0125, 1.0, True,
     "Delta_b=-0.44 mass @fixed v; pressure-support corrected; uncorrected v -> null"),
    # Ubler+2017 KMOS3D z2.3: Delta_b=-0.27+/-0.05 => dv=+0.0675+/-0.0125 ABOVE
    ("Ubler2017_z2.3", 2.3, +0.0675, 0.0125, 1.0, True,
     "Delta_b=-0.27 mass @fixed v; gas-mass dominated Mbar; PS toggle can null"),
    # MUSE-DARK II 2026 z~1: Delta_b=0.00+/-0.06 => dv=0.00+/-0.015 ON
    ("MUSEDARK_II_z1", 1.0, 0.000, 0.015, 1.0, True,
     "bTFR null; sTFR=-0.42 => offset is M/L+gas artifact not v-shift; N=95"),
    # A&A2024 2406.08934: directional ABOVE, zero-point NOT firm -> half weight, large err
    ("AA2024_z1.0", 1.0, +0.06, 0.05, 0.5, True,
     "shallow slope faster@fixed mass; authors decline firm zero-point; low-M incomplete"),
    # REBELS-25 z7.31 single object inferred: -0.93 to -0.49 dex ABOVE in MASS
    #   take mass ABOVE ~ -0.71+/-0.22 => dv=+0.178+/-0.055; down-weight (single, v-def)
    ("REBELS25_z7.31", 7.31, +0.178, 0.055, 0.15, False,
     "single object; V=372+/-80; Mbar factor~3; i=25deg; inferred"),
    # FRESCO Twister z5.3 single: ~-0.5 dex ABOVE mass (-0.2 upper) => -0.35+/-0.15 mass
    #   dv=+0.088+/-0.038 ; down-weight
    ("FRESCO_z5.3", 5.3, +0.088, 0.038, 0.15, False,
     "single object; V=242+/-50; Mbar/Mdyn~0.5 assumed; inferred"),
    # DiTeodoro2024 z~4.5 ETG-analogue, ON/ABOVE, no dex given -> tiny weight, directional
    ("DiTeodoro_z4.5", 4.5, +0.05, 0.06, 0.10, False,
     "ETG-analogue not late-type BTFR; ON/ABOVE directional; inferred"),
]

def wmean(entries):
    o=np.array([e[2] for e in entries]); s=np.array([e[3] for e in entries])
    w=np.array([e[4] for e in entries])/s**2  # weight * inverse-variance
    m=np.sum(w*o)/np.sum(w)
    err=np.sqrt(1.0/np.sum(w))  # formal
    # scatter-inflated error (like a scale factor)
    chi2=np.sum(w*(o-m)**2); dof=max(len(entries)-1,1)
    scale=np.sqrt(max(chi2/dof,1.0))
    return m, err, err*scale, scale

print("="*78)
print("OBSERVED velocity-axis BTFR offset dlog10(v) vs z=0  (+ = ABOVE, - = BELOW)")
print("="*78)
print(f"{'name':<18}{'z':>5}{'dv':>9}{'sig':>8}{'wt':>6}  quoted note")
for e in data:
    print(f"{e[0]:<18}{e[1]:>5}{e[2]:>+9.3f}{e[3]:>8.3f}{e[4]:>6.2f}  {str(e[5]):<5}")

# ---- primary estimate: quoted zero-point studies only, z in discriminator band ----
quoted = [e for e in data if e[5]]
allpts = data
band   = [e for e in data if 0.8<=e[1]<=3.0]  # z where A predicts a real (tiny) signal

for label, subset in [("QUOTED-ONLY (all z)", quoted),
                      ("ALL POINTS (incl inferred, down-weighted)", allpts),
                      ("DISCRIMINATOR BAND z=0.8-3.0", band)]:
    m,err,errsc,scale = wmean(subset)
    print(f"\n[{label}]  N={len(subset)}")
    print(f"  weighted mean dv = {m:+.4f} dex   formal +/-{err:.4f}   "
          f"scatter-inflated +/-{errsc:.4f} (scale {scale:.2f})")

# ---------------- predicted offsets at representative z ----------------
print("\n"+"="*78)
print("PREDICTED dlog10(v) at fixed M_b (velocity axis)")
print("="*78)
for z in [1.0,2.0,2.3,3.0]:
    print(f"  z={z}:  A={dv_fixedMb(ratA(z)):+.4f}   B={dv_fixedMb(ratB(z)):+.4f}   C=+0.0000")

# systematic floor
SYS_FLOOR = 0.06          # net quadrature residual (Scout C)
SYS_FLOOR_WORST = 0.14    # coherent uncorrected beam+asym-drift
A_z3 = dv_fixedMb(ratA(3.0))
print(f"\nBranch A signal @z=3 = {A_z3:+.4f} dex ; systematic floor ~{SYS_FLOOR} "
      f"(worst-coherent {SYS_FLOOR_WORST}) ; signal/floor = {abs(A_z3)/SYS_FLOOR:.2f}")

# ---------------- provisional bound ----------------
m,err,errsc,scale = wmean(quoted)
print("\n"+"="*78)
print("PROVISIONAL BOUND (quoted zero-point studies, scatter-inflated)")
print("="*78)
print(f"  dlog10(v)_highz - dlog10(v)_z0 = {m:+.3f} +/- {errsc:.3f} dex  (velocity axis)")
print(f"  In MASS at fixed v: Delta_b = {-4*m:+.3f} +/- {4*errsc:.3f} dex")
lo,hi = m-errsc, m+errsc
print(f"  1-sigma interval on dv: [{lo:+.3f}, {hi:+.3f}]")
print(f"  Branch A predicts dv<0 (BELOW). Observed central sign: "
      f"{'ABOVE (+)' if m>0 else 'BELOW (-)' if m<0 else 'ON'}")
print(f"  Does interval include Branch A (-0.033)? {'YES' if lo<=-0.033<=hi else 'NO'}")
print(f"  Does interval include Branch C (0.000)?  {'YES' if lo<=0.0<=hi else 'NO'}")
print(f"  Does interval include Branch B (+0.165 @z=3)? "
      f"{'YES' if lo<=0.165<=hi else 'NO'}")

# ---------------- PROVE-BY-MOVING #1: swap a0 footing ----------------
print("\n"+"="*78)
print("PROVE-BY-MOVING #1: swap a0(0) footing 9.36e-11 <-> 1.13e-10")
print("="*78)
a0_can, a0_alt = 9.36e-11, 1.13e-10
for z in [2.0,3.0]:
    rA=ratA(z)
    dv_can = 0.25*np.log10((a0_can*rA)/a0_can)
    dv_alt = 0.25*np.log10((a0_alt*rA)/a0_alt)
    print(f"  z={z}: dv(canonical)={dv_can:+.5f}  dv(alt)={dv_alt:+.5f}  "
          f"identical? {np.isclose(dv_can,dv_alt)}")
print("  => footing CANCELS in the ratio; predicted offset unchanged; verdict stable.")

# ---------------- PROVE-BY-MOVING #2: toggle asymmetric-drift correction ----------------
print("\n"+"="*78)
print("PROVE-BY-MOVING #2: toggle asymmetric-drift (pressure-support) correction")
print("="*78)
# AD correction moves observed v BELOW when UNDER-corrected. Model: apply an extra
# coherent BELOW bias delta_AD to the quoted (corrected) points and re-mean.
for delta_AD in [0.0, -0.045, -0.098]:  # iso-3sigma vs Burkert exp-disk residual range
    shifted = [(e[0],e[1],e[2]+delta_AD,e[3],e[4],e[5],e[6]) for e in quoted]
    m2,_,errsc2,_ = wmean(shifted)
    lo2,hi2=m2-errsc2,m2+errsc2
    verdict = ("ABOVE(->B/falsifies A)" if lo2>0 else
               "BELOW(->A-like)" if hi2<0 else "ON/consistent-with-C&A-floor")
    print(f"  delta_AD={delta_AD:+.3f}: dv={m2:+.3f}+/-{errsc2:.3f}  [{lo2:+.3f},{hi2:+.3f}]  {verdict}")
print("  => a single AD-prescription swing (0.045-0.098 dex) exceeds the |A| signal (0.033);")
print("     it can drag the null/above result down toward A, i.e. A-vs-C is AD-degenerate.")

# ---------------- final verdict logic ----------------
print("\n"+"="*78)
print("VERDICT LOGIC")
print("="*78)
m,err,errsc,scale = wmean(quoted)
print(f"  Observed (quoted): dv = {m:+.3f} +/- {errsc:.3f} (central sign {'ABOVE' if m>0 else 'BELOW/ON'}).")
print(f"  Branch B (+0.165 @z=3): observed does NOT reach it AND wrong for a rising law at z~2-3")
print(f"     (would need growing +offset; KMOS3D z2.3=+0.068 < z0.9=+0.110). B disfavored too.")
print(f"  Branch A (-0.033): observed central sign is OPPOSITE (leans ABOVE/ON), but")
print(f"     |A signal| {abs(A_z3):.3f} < systematic floor {SYS_FLOOR}; AD toggle spans the signal.")
print(f"  => A is NOT cleanly separable from C at the in-hand precision.")
print(f"  HONEST VERDICT: INCONCLUSIVE for A-vs-C (systematics-dominated);")
print(f"     data leans ON/ABOVE (C, with a B-ward tail that is M/L+gas-fraction artifact),")
print(f"     no measurement shows the BELOW sign Branch A requires.")
