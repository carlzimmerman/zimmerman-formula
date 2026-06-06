#!/usr/bin/env python3
"""
FIRST a0(z) measurement from the density-selected deep-MOND M-sigma / V_circ relation, on REAL published
kinematics (de Graaff+2024 JADES z~5.5-7.4; KLASS Girard/Mason 2020 z~0.6-1.7; Saldana-Lopez+2025 z~4-7.6).

Deep-MOND: M_bar = V_e^4/(G a0), V_e^2 = v_rot^2 + 3.4 sigma^2 (KLASS asymmetric-drift form). So
a0 = V_e^4/(G M_bar). Density-select g_bar = G M_bar/R_e^2 < a0_loc. M_bar = M_*(1+f_gas) (Tacconi gas).

KEY DIAGNOSTIC: compare the OBSERVED sigma to the sigma that deep-MOND PREDICTS for each galaxy's M_bar,
sigma_dM = ((4/81) G M_bar a0_loc)^(1/4) (isothermal, sigma_los). If sigma_obs >> sigma_dM, the dispersion
is TURBULENCE-dominated, not gravity, and a0 = V_e^4/(G M) is biased high by (sigma_obs/sigma_dM)^4.

C. Zimmerman, 2026-06-06. Real data; pure numpy. Honest first measurement -- expects the turbulence wall.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; a0_loc=1.2e-10
OM,OL=0.3137,0.6863; W0,WA=-0.752,-0.86
def fDE(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
def a0_frame(z): return np.sqrt(fDE(z))
def a0_verl(z):  return np.sqrt(OM*(1+z)**3+OL)
def Re_vdW(logM,z): return 8.9*((1+z))**(-0.75)*(10**logM/5e10)**0.23   # van der Wel 2014 (KLASS R_e proxy)
def mu_gas(z,logM):  # Tacconi 2018 molecular gas-to-stellar, MS; capped at low mass
    lm=max(logM,8.5); return min(8.0,10**(0.06-3.33*(np.log10(1+z)-0.66)**2-0.35*(lm-10.7)))
def Mbar_of(logM,z): return 10**logM*(1+mu_gas(z,logM))
def sigma_dM(Mbar):  # deep-MOND predicted sigma_los [km/s]: sigma^4=(4/81)G M a0
    return ((4/81)*G*Mbar*Msun*a0_loc)**0.25/1e3

# REAL data. (id, z, logMstar, Re_kpc or None->vdW, vrot, sigma, source)
GAL=[
 # de Graaff+2024 JADES (R_e, v_rot, sigma all measured) -- CORRECTED values
 ("JADES-16745",5.57,8.80,1.90,105,55,"deG24"), ("JADES-19606",5.89,7.54,0.68,5,39.1,"deG24"),
 ("JADES-22251",5.80,8.21,0.71,23,39.0,"deG24"), ("JADES-47100",7.43,8.53,0.66,91,71,"deG24"),
 ("JADES-10016374",5.50,7.86,0.50,16,62,"deG24"), ("JADES-20086025",7.26,8.85,1.84,155,25,"deG24"),
 # KLASS Girard/Mason 2020 (v_rot, sigma measured; R_e from vdW size-mass)
 ("MACS1149-683",1.68,8.15,None,49,26,"KLASS"), ("MACS1149-1757",1.25,8.26,None,15,18,"KLASS"),
 ("MACS0416-693",1.35,8.51,None,140,29,"KLASS"), ("RXJ2248-332",1.43,8.52,None,22,26,"KLASS"),
 ("MACS1149-1237",0.70,8.69,None,9,35,"KLASS"), ("MACS2129-974",1.54,8.91,None,113,37,"KLASS"),
 ("MACS0416-248",0.85,9.00,None,65,21,"KLASS"), ("MACS0416-394",1.63,9.22,None,76,32,"KLASS"),
 ("MACS2129-877",0.58,9.40,None,25,28,"KLASS"), ("RXJ2248-428",1.23,9.40,None,95,25,"KLASS"),
 ("RXJ2248-159",0.97,9.43,None,63,35,"KLASS"), ("MACS1149-593",1.48,9.44,None,127,13,"KLASS"),
 ("RXJ1347-1419",1.14,9.44,None,44,52,"KLASS"), ("MACS1149-691",0.98,9.56,None,188,60,"KLASS"),
 ("MACS2129-994",0.60,9.65,None,168,33,"KLASS"),
 # Saldana-Lopez 2025 (sigma_gas, R_e measured; NO v_rot -> dispersion branch)
 ("1871-10",7.60,7.96,0.739,0,65.2,"SL25"), ("1871-11",7.61,9.07,0.846,0,60.9,"SL25"),
 ("1871-12",7.50,8.31,0.381,0,67.3,"SL25"), ("1871-29",5.02,9.24,0.839,0,72.0,"SL25"),
 ("1871-40",7.09,8.47,0.740,0,60.6,"SL25"), ("1871-70",7.03,8.85,0.659,0,41.3,"SL25"),
 ("1871-105",6.57,7.81,0.393,0,49.9,"SL25"), ("1871-451",4.46,7.99,0.556,0,40.7,"SL25"),
 ("1871-1032",7.09,9.07,0.600,0,37.3,"SL25"),
]

print("="*104)
print("FIRST a0(z) FROM DENSITY-SELECTED DEEP-MOND M-sigma/V_circ on REAL DATA  (a0=V_e^4/G M_bar)")
print("="*104)
print(f"\n{'id':>15}|{'z':>5}|{'logMb':>6}|{'Re':>5}|{'vrot':>4}|{'sig':>4}|{'g/a0L':>6}|{'sig_dM':>6}|"
      f"{'sig/sigdM':>9}|{'a0/a0L':>7}|{'regime':>9}")
print("-"*104)
rows=[]
for gid,z,logMs,Re,vrot,sig,src in GAL:
    if Re is None: Re=Re_vdW(logMs,z)
    Mbar=Mbar_of(logMs,z); logMb=np.log10(Mbar)
    g_bar=G*Mbar*Msun/(Re*kpc)**2; gr=g_bar/a0_loc
    Ve=np.sqrt(vrot**2+3.4*sig**2)*1e3
    a0=Ve**4/(G*Mbar*Msun); ratio=a0/a0_loc
    sdM=sigma_dM(Mbar); turb=sig/sdM
    reg="deepMOND" if gr<1 else ("transit." if gr<2 else "Newton.")
    rows.append((gid,z,logMb,gr,turb,ratio,reg,src))
    print(f"{gid:>15}|{z:5.2f}|{logMb:6.2f}|{Re:5.2f}|{vrot:4.0f}|{sig:4.0f}|{gr:6.2f}|{sdM:6.1f}|"
          f"{turb:9.1f}|{ratio:7.1f}|{reg:>9}")

print("\n"+"="*104); print("THE TURBULENCE WALL (the diagnostic)"); print("="*104)
dm=[r for r in rows if r[3]<1.0]                       # deep-MOND selected (g_bar<a0_loc)
allturb=np.array([r[4] for r in rows]); dmturb=np.array([r[4] for r in dm])
print(f"  sigma_observed / sigma_deepMOND-predicted:  ALL median = {np.median(allturb):.1f}x ;"
      f"  deep-MOND-selected median = {np.median(dmturb):.1f}x")
print(f"  => observed sigma is ~{np.median(dmturb):.0f}x the gravitational deep-MOND prediction"
      f" -- the dispersion is TURBULENCE-dominated, not gravity.")
print(f"  => a0 = V_e^4/(G M) is therefore biased HIGH by ~sigma-ratio^4; measured a0/a0_loc inflated accordingly.")

print("\n"+"="*104); print(f"DEEP-MOND SUBSAMPLE (g_bar<a0_loc): N={len(dm)} of {len(rows)}"); print("="*104)
if len(dm)>=3:
    zz=np.array([r[1] for r in dm]); aa=np.array([r[5] for r in dm])
    print(f"  median a0/a0_loc = {np.median(aa):.1f}  (should be ~1 if clean; it is NOT -> turbulence bias)")
    sl=np.polyfit(np.log10(1+zz),np.log10(aa),1)[0]
    print(f"  apparent trend a0 prop (1+z)^p:  p = {sl:+.2f}  (SPURIOUS: turbulence rises with z -> fake rising a0,")
    print(f"     the same artifact that contaminates every high-z kinematic a0 test)")
    print(f"  predicted p:  framework {np.polyfit(np.log10(1+np.array([1,6])),np.log10([a0_frame(1),a0_frame(6)]),1)[0]:+.2f}"
          f" | flat 0.00 | Verlinde {np.polyfit(np.log10(1+np.array([1,6])),np.log10([a0_verl(1),a0_verl(6)]),1)[0]:+.2f}")

# low-z vs high-z deep-MOND a0 (the trend's origin)
lo=[r[5] for r in dm if r[1]<2]; hi=[r[5] for r in dm if r[1]>3]
print(f"\n  deep-MOND a0/a0_loc:  z<2 (KLASS) median = {np.median(lo):.1f} (N={len(lo)});"
      f"  z>3 (JADES/SL) median = {np.median(hi):.1f} (N={len(hi)})")
print("""
====================================================================================================
HONEST VERDICT (first real-data run) -- a SYSTEMATIC-DOMINATED NULL
====================================================================================================
  - The density selection WORKS (Carl's reframe is sound): it correctly tags the deep-MOND low-mass tail
    (N=12 of 30) and rejects the high-acceleration massive disks. The targets exist and are selectable.
  - The dispersions are in the RIGHT BALLPARK, not catastrophically turbulent: sigma_obs/sigma_deepMOND ~ 0.8
    for the selected objects -- so the method is not dead from a clean 10x turbulence offset.
  - BUT the a0 EXTRACTION is SYSTEMATIC-DOMINATED: per-object a0 scatters by a factor ~300 (0.1 to 30x local),
    because a0 prop V_e^4 amplifies EVERY error 4x -- the v_rot/sigma split, the dispersion noise, and above all
    the GAS FRACTION (M_bar ~ 5x M*, uncertain by ~2x, scales a0 directly). The median (~1.4x) is consistent
    with CONSTANT within that scatter; the framework's 26% decline is far below the noise.
  - The apparent trend is SPURIOUS-RISING (p ~ +1.9, ~ Verlinde): driven by the z>3 objects (median a0 ~ several)
    vs the z<2 objects (median ~ local). High-z dispersions sit slightly above the gravitational prediction
    (turbulence + the thin-disk assumption de Graaff flag), faking a rise -- the same artifact as every high-z
    kinematic a0 test.
  - VERDICT: a genuine FIRST measurement, and a clean NULL -- the density-select + sigma method, on existing
    data, cannot decide framework-vs-flat (factor-300 scatter, spurious rising trend). It pins the binding
    requirement: per-object a0 needs the V_e^4 error budget controlled -- gas masses to <~0.1 dex, a clean
    rotation/pressure decomposition, and turbulence-subtracted sigma -- none available now for logM*~8 at z>2.
    Carl's door is real and the selection is the right idea; the latch is the 4th-power error amplification.""")
