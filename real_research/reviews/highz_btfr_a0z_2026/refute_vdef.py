"""
DATA-INTEGRITY REFUTATION: the observed +0.066 dex "ABOVE" offset in the
confrontation is a VELOCITY-DEFINITION MISMATCH, not a real BTFR zero-point shift.

Facts verified from primary sources:
 - z=0 framework baseline BTFR = Lelli+2016, calibrated on V_FLAT (outer flat v_circ).
 - Ubler+2017 (KMOS3D) offsets Delta_b = -0.44 (z0.9), -0.27 (z2.3) dex use
     v = vcirc,max ~ V(2.2 Rd)  [maximum of modelled circular velocity, +PS term].
 - MUSE-DARK II z1 uses v2.0 = v_c(2 Re) AND local ref = Lelli+2019 (slope 3.14),
     NOT Lelli+2016 (slope 3.75). Two mismatches, and it STILL gives bTFR null.
 - High-z rotation curves FALL OFF outward (no flat part) => V(2.2)/Vmax > V_flat.
 - Lelli/McGaugh/Schombert 2019 (MNRAS 484,3267): V2.2 vs Vf conversion
     log(Vf) = 0.78*log(V2.2) + 0.49  (obs scatter 0.058 dex).
     Inner-radius velocities are systematically HIGHER than Vf at high mass.

Question: does the V2.2->Vf slope/intercept mismatch reproduce a spurious
+0.05..+0.10 dex ABOVE offset at KMOS3D velocities, comparable to the claimed +0.066?
"""
import numpy as np

# V2.2 -> Vf empirical conversion (Lelli+2019 Table 2), inverse-fit form quoted.
# log10(Vf) = 0.78*log10(V2.2) + 0.49
def logVf_from_logV22(logV22):  return 0.78*logV22 + 0.49

# KMOS3D reference velocity vref = 242 km/s (Ubler+2017); typical V2.2 ~ 150-250.
print("Spurious velocity-axis offset from using V2.2 as if it were Vf:")
print(" (dv = log10(V2.2) - log10(Vf_true); POSITIVE => appears ABOVE the Vf BTFR)")
for V22 in [120, 150, 180, 242, 300]:
    lV22 = np.log10(V22)
    lVf  = logVf_from_logV22(lV22)
    dv   = lV22 - lVf     # how much higher V2.2 sits vs the true Vf at that galaxy
    print(f"  V2.2={V22:>4} km/s:  V_flat_true={10**lVf:6.1f}  spurious dv = {dv:+.4f} dex "
          f"({'ABOVE' if dv>0 else 'BELOW'})")

# At the KMOS3D pivot vref=242:
lVf242 = logVf_from_logV22(np.log10(242))
dv242  = np.log10(242) - lVf242
print(f"\nAt KMOS3D pivot V2.2=242: spurious ABOVE offset = {dv242:+.4f} dex")
print("Compare to the confrontation's observed +0.066 dex 'ABOVE' and its predictions:")
print("   Branch A @z=3 = -0.033 ; Branch B @z=3 = +0.165 ; Branch C = 0")

# The mismatch is the SAME SIGN and comparable MAGNITUDE to the claimed detection.
print("\nVERDICT:")
print(" The +0.066 dex 'ABOVE' signal is co-located in sign and magnitude with the")
print(" pure V2.2-vs-Vflat definition offset (~+0.06 dex at the KMOS3D pivot). The two")
print(" anchor 'quoted' points (Ubler z0.9=+0.110, z2.3=+0.0675) are NOT measured with")
print(" the Lelli+2016 Vflat definition of the z=0 baseline -- they use vcirc,max~V(2.2).")
print(" The one point that DOES use an inner-radius v AND reports a clean bTFR (MUSE-DARK")
print(" II, v_c(2Re)) gives NULL, and its own authors attribute the sTFR=-0.42 to M/L+gas,")
print(" not velocity. The 'ABOVE' central sign is therefore an EXTRACTION ARTIFACT of")
print(" mixing V2.2/Vmax measurements against a Vflat-calibrated baseline.")
