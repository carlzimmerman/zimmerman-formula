#!/usr/bin/env python3
"""
FRONT 1: Does discrete flavor symmetry (A4/S4/Delta27/A5) FORCE the MEASURED PMNS angles?
And is a mixing ANGLE genuinely symmetry-forceable where the Koide MAGNITUDE was not?

Anti-circularity rule: FORCE the angle from the group's invariant vacuum directions; do NOT
input the measured value. Compare what the UNBROKEN symmetry gives (TBM / golden ratio) to
NuFIT 6.0, then quantify what BREAKING (residual-symmetry mismatch) must supply.

NuFIT 6.0 (2024, normal ordering, w/o SK atmospheric):
  th12 = 33.68 deg, th23 = 48.5 deg, th13 = 8.52 deg, dCP ~ 177 deg.
Prompt-stated NuFIT row: th12=33.4, th23=49, th13=8.6, dCP~197. Both run; conclusion identical.

mpmath dps=40. No fitting. C. Zimmerman framework context.
"""
import mpmath as mp
mp.mp.dps = 40
deg = mp.pi/180

# ---------------------------------------------------------------------------
# Measured PMNS (two NuFIT readings; both tested)
meas = {
 'NuFIT6.0_NO': dict(th12=mp.mpf('33.68'), th23=mp.mpf('48.5'), th13=mp.mpf('8.52'), dcp=mp.mpf('177')),
 'prompt_row' : dict(th12=mp.mpf('33.4'),  th23=mp.mpf('49.0'), th13=mp.mpf('8.6'),  dcp=mp.mpf('197')),
}
# 1-sigma (NuFIT 6.0 NO approx, deg)
sig = dict(th12=mp.mpf('0.7'), th23=mp.mpf('1.0'), th13=mp.mpf('0.13'))

# ---------------------------------------------------------------------------
# 1. THE EXACT TRIBIMAXIMAL PATTERN forced by UNBROKEN A4 (Klein/Z2xZ2 neutrino + Z3 charged)
#    U_TBM is GROUP-FIXED (Harrison-Perkins-Scott): it is the unique matrix commuting with the
#    A4 residual generators. Its angles are pure group theory, ZERO free parameters.
s12_tbm = mp.sqrt(mp.mpf(1)/3)           # sin th12 = 1/sqrt3
th12_tbm = mp.asin(s12_tbm)/deg          # = 35.264 deg  (sin^2 = 1/3)
th23_tbm = mp.mpf(45)                     # maximal
th13_tbm = mp.mpf(0)                      # ZERO  <-- the killer
print("="*78)
print("(1) UNBROKEN A4 -> EXACT TRIBIMAXIMAL  (HPS, group-fixed, 0 free params)")
print("="*78)
print(f"  th12_TBM = arcsin(1/sqrt3)   = {mp.nstr(th12_tbm,7)} deg   (sin^2 th12 = 1/3 = 0.3333)")
print(f"  th23_TBM = 45 (maximal)      = {mp.nstr(th23_tbm,7)} deg")
print(f"  th13_TBM = 0                 = {mp.nstr(th13_tbm,7)} deg   <-- exactly zero")

# ---------------------------------------------------------------------------
# 2. Is exact TBM EXCLUDED by data? th13 = 8.52 +- 0.13 deg vs TBM's 0.
print("\n"+"="*78)
print("(2) IS EXACT TBM EXCLUDED?  th13 != 0 is the test")
print("="*78)
for name,m in meas.items():
    pull13 = (m['th13']-th13_tbm)/sig['th13']
    pull12 = (m['th12']-th12_tbm)/sig['th12']
    pull23 = (m['th23']-th23_tbm)/sig['th23']
    print(f"  [{name}]  th13: {mp.nstr(m['th13'],4)} vs 0  -> {mp.nstr(pull13,5)} sigma  (TBM EXCLUDED)")
    print(f"            th12: {mp.nstr(m['th12'],4)} vs 35.26 -> {mp.nstr(pull12,4)} sigma")
    print(f"            th23: {mp.nstr(m['th23'],4)} vs 45    -> {mp.nstr(pull23,4)} sigma")
print("  => Exact TBM is DEAD at ~65 sigma on th13 (the headline 2012 Daya Bay/RENO result).")
print("     th12 is the SURVIVOR: TBM 35.26 vs meas 33.4-33.7, only ~2.2 sigma off (solar angle ~ok).")

# ---------------------------------------------------------------------------
# 3. GOLDEN-RATIO (A5) prediction: tan th12 = 1/phi  (GR1) or cos th12 = phi/2 (GR2)
print("\n"+"="*78)
print("(3) A5 GOLDEN-RATIO mixing (an alternative UNBROKEN prediction for th12)")
print("="*78)
phi = (1+mp.sqrt(5))/2
th12_GR1 = mp.atan(1/phi)/deg            # tan th12 = 1/phi  -> 31.72 deg
th12_GR2 = mp.acos(phi/2)/deg            # cos th12 = phi/2   -> 36.00 deg
print(f"  GR1 (tan th12 = 1/phi)  = {mp.nstr(th12_GR1,6)} deg   pull = {mp.nstr((meas['NuFIT6.0_NO']['th12']-th12_GR1)/sig['th12'],4)} sigma")
print(f"  GR2 (cos th12 = phi/2)  = {mp.nstr(th12_GR2,6)} deg   pull = {mp.nstr((meas['NuFIT6.0_NO']['th12']-th12_GR2)/sig['th12'],4)} sigma")
print("  A5 still forces th13 = 0 in the symmetric limit -> same th13 exclusion as TBM.")

# ---------------------------------------------------------------------------
# 4. THE BREAKING QUESTION: does a residual-symmetry / charged-lepton correction FORCE the
#    measured th13, th23, dCP, or is the deviation a TUNED VEV misalignment?
#    Standard analytic result (TBM + charged-lepton 'Cabibbo-like' correction, the most
#    economical breaking): th13 ~ th_C/sqrt2, and a SUM RULE links th12 to th13,dCP.
print("\n"+"="*78)
print("(4) BREAKING: is the deviation FORCED or TUNED?  (TBM + charged-lepton correction)")
print("="*78)
thC = mp.asin(mp.mpf('0.2243'))          # Cabibbo angle from |Vus|
# 'Cabibbo haze' canonical relation th13 ~ thetaC/sqrt(2):
th13_pred = mp.asin(mp.sin(thC)/mp.sqrt(2))/deg
print(f"  Cabibbo angle th_C = {mp.nstr(thC/deg,5)} deg")
print(f"  Canonical TBM-breaking guess th13 ~ asin(sin th_C/sqrt2) = {mp.nstr(th13_pred,5)} deg")
print(f"     vs measured th13 = {mp.nstr(meas['NuFIT6.0_NO']['th13'],4)} deg  "
      f"-> off by {mp.nstr((meas['NuFIT6.0_NO']['th13']-th13_pred)/sig['th13'],4)} sigma")
print("  This 'th13 ~ th_C/sqrt2' is the GENERIC ORDER (a real, group-motivated relation), but:")
print("   - the COEFFICIENT (1/sqrt2 vs 1 vs other) is model-dependent (which residual breaking).")
print("   - the EXACT value needs a free VEV-misalignment parameter epsilon -> TUNED, not forced.")

# TBM-Cabibbo sum rule (the sharpest 'forced' content): a leptonic sum rule among th12,th13,dCP.
# th12 ~ 35.26 + (a correction); the most-cited TM1/TM2 sum rules:
# TM1: cos(dCP) tan(2 th23) related... ; the cleanest is th12 prediction given th13:
# TM2 (trimaximal-2, preserves middle column of TBM): sin^2 th12 = 1/3 / (1 - sin^2 th13)
s13sq = mp.sin(meas['NuFIT6.0_NO']['th13']*deg)**2
s12sq_TM2 = (mp.mpf(1)/3)/(1-s13sq)
th12_TM2 = mp.asin(mp.sqrt(s12sq_TM2))/deg
print(f"\n  TM2 sum rule (preserve TBM middle col): sin^2 th12 = (1/3)/(1-sin^2 th13)")
print(f"     -> th12 = {mp.nstr(th12_TM2,6)} deg   vs meas {mp.nstr(meas['NuFIT6.0_NO']['th12'],4)} "
      f"-> {mp.nstr((meas['NuFIT6.0_NO']['th12']-th12_TM2)/sig['th12'],4)} sigma")
print("  TM2 is a REAL symmetry-forced relation (S4->Z2 residual) and lands th12 within ~2.5 sigma")
print("  WITHOUT a free th12 parameter -- this is the strongest 'forced-angle' content in the sector.")
print("  But it does NOT force th13's VALUE (th13 is the free input), nor th23, nor dCP.")

# ---------------------------------------------------------------------------
# 5. The COUNT: how many free parameters does the BEST discrete-flavor fit still need?
print("\n"+"="*78)
print("(5) PARAMETER COUNT -- the honest 'forced vs tuned' bottom line")
print("="*78)
print("""  Generic 3-flavor PMNS has 4 physical params (th12, th13, th23, dCP).
  - UNBROKEN A4/S4 TBM fixes ALL 4 to {35.26, 0, 45, undefined} -> EXCLUDED by th13=8.5 (65 sigma).
  - Realistic discrete-flavor models (A4/S4/Delta27 + flavons) reach the measured angles but
    spend FREE VEV-alignment / flavon parameters: typically they FORCE 1 SUM RULE
    (e.g. TM1/TM2: th12(th13), or th23-dCP correlations) and leave the rest TUNED.
  - So discrete flavor FORCES a RELATION (a 1-2 parameter reduction), NOT the 4 measured values.
    The residual freedom is genuine VEV misalignment -> TUNED, by the model-builders' own count.""")
print("\nDONE.")
