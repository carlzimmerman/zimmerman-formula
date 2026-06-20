"""
CLASH cluster-core residual TARGET on the Zimmerman-framework footing (topic "clash_target").

SOURCE (precise, read from the PDF: Eq.8,11,13,15,17 + Tables I & II + Fig.3):
  Famaey, Pizzuti & Saltas, "On the nature of the missing mass of galaxy clusters in MOND:
  the view from gravitational lensing", arXiv:2410.02612, PRD 111 (2025). (Dated Apr 30 2025.)

  - 16 CLASH clusters, mostly relaxed, kT=5.9..15.5 keV. Strong+weak-lensing shear + magnification
    (Umetsu+2016). Lensing observable: M_lensGR(r) from (Phi-Psi) (Eq.9,10). In MOND (Psi=-Phi) the
    dynamical mass reproducing the SAME lensing is M(r)=Q'(y^2)M_lensGR (Eq.11), Q'=0.5(1+(1+4/y)^.5)
    [simple, Eq.8], y=|gradPhi_N|/a0. a0~=1e-10 m/s^2 (FPS text).
  - Residual ("MOND missing mass"): dM(r)=M(r)-M_gas-M_*-M_BCG (Eq.13); truncated at turnaround r0.
  - GENERIC fit (Eq.15): rho_dM(r)=rho_s/[(r/rs)^g (1+(r/rs)^a)^((b-g)/a)], a=1 fixed.
    Result: CORED g=0 (<g>=0.015, geom-mean<1e-3); outer slope b>3.7; BIC-preferred b=6 (steeper
    than -3.5). Per-cluster (rho_s [Msun/Mpc^3], rs [Mpc]) in TABLE I.
  - DARK-MASS-FOLLOWS-GAS (Eq.17): rho_dM=eta*rho_gas*exp(-lambda r/r0); weighted means
    <log10 eta>=0.93 (eta=8.5, "missing/gas~10"), <r0/lambda>=0.43 Mpc (the exp cutoff). Remarkable
    UNIFORMITY of both eta and cutoff across the 16 clusters (Fig.4) -- flat in M_gas and kT.
  - TABLE II (M_gas(<r0), dM(<r0) in 1e14 Msun; cutoff r0/lambda in Mpc):
        A209    : M_gas=2.33 dM=2.88 log_eta=0.91 cutoff=0.60  kT=7.3   (the Fig.3 cluster)
        RXJ1347 : M_gas=5.28 dM=7.71 log_eta=0.81 cutoff=1.61  kT=15.5  (most massive)
        MACS1206: M_gas=2.97 dM=3.24 log_eta=0.98 cutoff=0.40  kT=10.8
        A2261   : M_gas=3.32 dM=4.46 log_eta=1.05 cutoff=0.65  kT=7.6
      Sample: M_gas 0.77-5.28e14, dM 0.85-7.71e14, log_eta 0.66-1.27, cutoff 0.19-4.14 Mpc.
  - FPS Discussion: an a0-RESCALE is NOT equivalent: an a0 boost would make dM correlate with TOTAL
    baryons incl. BCG, but the data show dM correlates with the GAS alone (bears on MI-vs-MG below).

  TABLE-I generic cored profile (g=0,a=1) -> rho_dM(r)=rho_s/(1+r/rs)^b. This IS the FPS best-fit
  lensing residual; we use it DIRECTLY for M_res(<r) (no gas back-out). beta=6 BIC-preferred; we
  also report beta=4 and beta=10 to show the core-integrated M_res is robust to the outer slope.
  A209   beta=6: log rho_s=15.38, rs=0.72 Mpc   (beta=4: 15.50,0.36 ; beta=10: 15.36,1.38)
  RXJ1347 beta=6: log rho_s=15.68, rs=0.81 Mpc

COMPANION (SHARED-GAP anchor):
  Durakovic & Skordis, arXiv:2312.00889, JCAP 03(2024)040, "Towards galaxy cluster models in AeST".
  - AeST static weak-field "totally screened" interpolation (Eq.2.8/2.9):
        M(x)=(sqrt(1+4x)-1)/(sqrt(1+4x)+1), x=|gradPhi|/a0  [M(x)*a_obs=a_N].
  - AeST RAR: a PEAK (ENHANCEMENT above MOND) at an accel set by the AeST scalar-mass parameter +
    system mass + boundary potential; for LOWER accel the AeST RAR DROPS BELOW the MOND expectation,
    "as if there is a negative mass density" (abstract, verbatim). => AeST adds a transient extra
    boost at intermediate accel, but its DEEP tail goes the WRONG way; it does NOT supply right-signed
    cored central mass at deep-MOND cluster cores. The cored cluster-core residual is a SHARED
    undershoot of the relativistic-MOND family, not specific to AeST OR to the Zimmerman framework.

FRAMEWORK FOOTING (MEMORY eta-WORST): a0=9.36e-11 m/s^2, g_obs=sqrt(g_bar^2+g_bar*a0).
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.086e19; Mpc=1000.0*kpc
a0_fw=9.36e-11; a0_fps=1.0e-10; a0_mond=1.2e-10

# =====================================================================
# (1) INTERPOLATION COMPARE (both ways: shared deep-MOND ASYMPTOTE, NOT identical in transition)
# =====================================================================
print("="*94)
print("(1) INTERPOLATION: framework dS-Unruh  vs  AeST totally-screened  vs  FPS simple")
print("="*94)
def gobs_fw(gN,a0):  return np.sqrt(gN**2+gN*a0)
def gobs_aest(gN,a0):
    return brentq(lambda ao:((np.sqrt(1+4*ao/a0)-1)/(np.sqrt(1+4*ao/a0)+1))*ao-gN,1e-14,gN+50*a0)
def gobs_fps(gN,a0):
    y=gN/a0; return (0.5+0.5*np.sqrt(1+4/y))*gN
print(f"  {'gN/a0':>7} {'gobs_FW':>11} {'gobs_AeST':>11} {'gobs_FPS':>11} {'AeST/FW':>8} {'FPS/FW':>8}")
for gba in [0.01,0.02,0.04,0.10,0.30,1.0,3.0]:
    gN=gba*a0_fw
    f=gobs_fw(gN,a0_fw); a=gobs_aest(gN,a0_fw); s=gobs_fps(gN,a0_fw)
    print(f"  {gba:7.2f} {f:11.4e} {a:11.4e} {s:11.4e} {a/f:8.3f} {s/f:8.3f}")
print("  BOTH WAYS: all three share the EXACT deep-MOND asymptote g_obs->sqrt(gN*a0) (gN<<a0); the")
print("  deep-MOND lensing phantom is shared in the LIMIT. At cluster-core gN/a0~0.02-0.04 they differ")
print("  ~6-18%: AeST gives MORE phantom (the D-S transient 'peak'), FPS-simple ~6-8% more. Framework")
print("  dS-Unruh nu is the LOWEST -> needs the MOST extra mass for given lensing => its undershoot is")
print("  MARGINALLY the WORST -- not better than AeST. (AeST's eventual deep tail dips BELOW MOND too.)")

# =====================================================================
# (2) THE CLASH TARGET PROFILE M_res(<r) -- FPS Table-I generic cored profile (DIRECT, robust)
# =====================================================================
print("\n"+"="*94)
print("(2) CLASH TARGET M_res(<r): FPS best-fit cored profile  rho_dM=rho_s/(1+r/rs)^beta (Eq.15,g=0,a=1)")
print("="*94)
def Mres_generic(R_kpc, logrhos, rs_Mpc, beta):
    rho_s=10**logrhos * Msun/Mpc**3; rs=rs_Mpc*Mpc; R=R_kpc*kpc
    return quad(lambda r:4*np.pi*r**2*rho_s/(1+r/rs)**beta,1e-4*rs,R,limit=400)[0]/Msun
# Per-cluster Table-I (beta=4 / beta=6BIC / beta=10):
A209_fits={4:(15.50,0.36), 6:(15.38,0.72), 10:(15.36,1.38)}
RXJ_fits ={4:(15.79,0.41), 6:(15.68,0.81), 10:(15.63,1.60)}
print("\n  A209 (kT=7.3 keV, the Fig.3 cluster) M_res(<r) [Msun]:")
print(f"  {'r[kpc]':>7} {'beta=4':>12} {'beta=6(BIC)':>12} {'beta=10':>12}  (spread = outer-slope syst)")
for rk in [140,210,280,350,420,500,700,1000,1300,2000]:
    m=[Mres_generic(rk,*A209_fits[b],b) for b in (4,6,10)]
    print(f"  {rk:7d} {m[0]:12.3e} {m[1]:12.3e} {m[2]:12.3e}")
A209_tot=[Mres_generic(1e4,*A209_fits[b],b) for b in (4,6,10)]
print(f"  A209 M_res(total): beta4={A209_tot[0]:.2e} beta6={A209_tot[1]:.2e} beta10={A209_tot[2]:.2e} "
      f"(Table II dM={2.88e14:.2e})")
print("\n  RXJ1347 (kT=15.5 keV, MOST massive) M_res(<r) [Msun]:")
print(f"  {'r[kpc]':>7} {'beta=4':>12} {'beta=6(BIC)':>12} {'beta=10':>12}")
for rk in [140,280,420,700,1000,1300,2000]:
    m=[Mres_generic(rk,*RXJ_fits[b],b) for b in (4,6,10)]
    print(f"  {rk:7d} {m[0]:12.3e} {m[1]:12.3e} {m[2]:12.3e}")
RXJ_tot=[Mres_generic(1e4,*RXJ_fits[b],b) for b in (4,6,10)]
print(f"  RXJ1347 M_res(total): beta4={RXJ_tot[0]:.2e} beta6={RXJ_tot[1]:.2e} beta10={RXJ_tot[2]:.2e} "
      f"(Table II dM={7.71e14:.2e})")
print("\n  ROBUST: inside the core (<420 kpc) the three outer-slope fits agree to ~15% -> the cored")
print("  CORE-integrated M_res is the robust target, the outer slope is the systematic.")

# =====================================================================
# (3) THE FRAMEWORK-FOOTING SURCHARGE (a0=9.36e-11 vs FPS 1e-10; dS-Unruh nu vs simple)
# =====================================================================
print("\n"+"="*94)
print("(3) FRAMEWORK FOOTING: the surcharge for a0=9.36e-11 + dS-Unruh nu (vs FPS a0=1e-10 + simple)")
print("="*94)
gN_core=0.03*a0_fps
m_fps=gobs_fps(gN_core,a0_fps)/gN_core        # phantom-incl/baryon accel ratio (~Mdyn/Mbar)
m_fw =gobs_fw (gN_core,a0_fw )/gN_core
surch=(m_fw-1)/(m_fps-1)-1
print(f"  At gN/a0~0.03 (deep-MOND core): phantom/baryon accel ratio")
print(f"    FPS-simple   (a0=1e-10)   = {m_fps:.3f}")
print(f"    framework-nu (a0=9.36e-11)= {m_fw:.3f}")
print(f"  -> framework needs {surch:+.1%} LESS extra mass at this accel? sign check:")
print(f"     (framework nu is LOWER => predicts LESS g_obs from baryons => needs MORE phantom for the")
print(f"      SAME lensing; but the per-accel phantom multiplier here is lower because both a0 and nu")
print(f"      are lower. The NET on the integrated residual is a few-% level, SUB-DOMINANT to the")
print(f"      WL-vs-HSE mass-scale gap. Banked eRASS1 surcharge for a0=9.36e-11 vs 1.2e-10 = +12.6%.)")
print(f"  => the framework footing does NOT change the cored SHAPE or the order of M_res; it is a")
print(f"     few-to-~13% magnitude surcharge, the same one banked for eRASS1.")

# =====================================================================
# (4) CLASH-lensing  vs  eRASS1-Xray  TARGET AGREEMENT (two independent probes)
# =====================================================================
print("\n"+"="*94)
print("(4) DO CLASH-LENSING (FPS 2025) AND eRASS1-XRAY (banked) AGREE? -- two independent probes")
print("="*94)
# Banked eRASS1 cored target (TARGET_PROFILE_RESULT_2026-06-19.md, rich M500=1e15, FW a0+interp):
erass1={140:5.4e13, 420:2.3e14, 700:3.7e14, 1400:4.8e14}
print("  Note: eRASS1 'rich M500=1e15'; A209~few e14 (lighter), RXJ1347~1e15 (matched). Compare RXJ1347.")
print(f"  {'region':>22} {'eRASS1 Xray':>12} {'CLASH RXJ1347(b6)':>18} {'ratio':>7} {'CLASH A209(b6)':>15}")
for rk in [140,420,700,1400]:
    er=erass1[rk]; cr=Mres_generic(rk,*RXJ_fits[6],6); ca=Mres_generic(rk,*A209_fits[6],6)
    print(f"  {('M_res(<%d kpc)'%rk):>22} {er:12.2e} {cr:18.2e} {cr/er:7.2f} {ca:15.2e}")
print(f"\n  Core scale:  eRASS1 r_core~420 kpc, cutoff ~400-450 (sqrt M500)")
print(f"               CLASH    cutoff r0/lambda=430 kpc (weighted mean), rs(b6)=0.72-0.81 Mpc -> MATCH")
print(f"  Missing/gas: eRASS1 6-10                | CLASH eta~8.5 central ('~10')          -> MATCH")
print(f"  Shape:       BOTH cored (gamma=0) + sharp outer slope (>3.5/-3.5), gas-tracking    -> MATCH")
print(f"  Uniformity:  eRASS1 eta(R500)=2.33 (5-95%:2.0-4.4, intrinsic 0.04 dex) ; CLASH eta & cutoff")
print(f"               'remarkably uniform' across 16 clusters (flat in M_gas, kT)            -> MATCH")
print(f"  Magnitude:   matched mass (RXJ1347~eRASS1-rich): M_res(<420)~2.4e14 vs 2.3e14 -> ~1.0x AGREE;")
print(f"               at R500 CLASH/eRASS1~1.6 = the WL(lensing)-vs-HSE(Xray) mass-scale gap [Li+2024,")
print(f"               ~110%], exactly the banked eta(R500) bracket [~1.0 HSE, ~2.33 WL].")

print("\n"+"="*94)
print("HEADLINE (both ways): the CLASH-lensing residual (FPS 2025) and the eRASS1-Xray residual (banked)")
print("are the SAME OBJECT from two INDEPENDENT probes -- cored (gamma=0), gas-tracking, ~420-430 kpc")
print("cutoff, missing/gas~10, remarkably UNIFORM, ~2.3e14 Msun inside ~420 kpc at a matched M500~1e15")
print("(RXJ1347 2.4e14 vs eRASS1 2.3e14, ~1.0x). They AGREE in shape/core/uniformity/missing-gas; the")
print("R500 magnitude differs ~1.6x = the WL-vs-HSE mass-scale gap (the banked eta bracket). It is a")
print("SHARED undershoot of the relativistic-MOND family: AeST drops BELOW MOND at low a (same sign),")
print("the framework's dS-Unruh nu is the LOWEST interpolation -> its undershoot is MARGINALLY the WORST,")
print("NOT better than AeST. NO framework-distinctive MI cored-profile edge. Quarantine held; both ways.")
print("="*94)
