#!/usr/bin/env python3
"""
ROUTE 3 FINAL -- the Bullet collision velocity, framework vs LCDM, both-ways verdict
====================================================================================
Consolidates: (A) the AM08 anchor, (B) the framework-footed energy integral, (C) the
LCDM probability (Lee & Komatsu 2010), (D) the modified-INERTIA vs modified-GRAVITY check
(is the velocity edge framework-DISTINCTIVE or MOND-shared?), and (E) the both-ways ledger.

a0 = 9.36e-11 (framework). Quarantine held: a0/Z/kappa not asserted derived; the deep-MOND
infall is a0-WEAK (v ~ (G M a0)^1/4) so the edge survives the whole a0 band.
"""
import numpy as np

G=6.674e-11; Msun=1.989e30; Mpc=3.0857e22; kpc=Mpc/1000.; km=1e3
a0_fw=9.36e-11; a0_can=1.20e-10

# Bullet masses (Angus & McGaugh 2008; Lee & Komatsu main ~1e15 h^-1)
M_main=1.5e15*Msun; M_sub=1.5e14*Msun; f_b=0.17
M_CDM=M_main+M_sub; M_bar=f_b*M_CDM; d=425.*kpc

def g(rr,MM,aa,k):
    gN=G*MM/rr**2
    if k=='newton': return gN
    if k=='dsunruh': return np.sqrt(gN**2+gN*aa)           # framework MI
    if k=='simple':  return 0.5*(gN+np.sqrt(gN**2+4*gN*aa))# Bekenstein-Milgrom MG
def vfall(MM,aa,r_ta,k):
    rr=np.logspace(np.log10(d),np.log10(r_ta),200000)
    return np.sqrt(2*np.trapz(g(rr,MM,aa,k),rr))

print("="*86)
print("ROUTE 3 FINAL -- BULLET COLLISION VELOCITY: framework MOND vs LCDM (both ways)")
print("="*86)

# ---- (A) physically-anchored turnaround radius ----
# Turnaround radius for a pair that collides at z=0.296: spherical-collapse turnaround for a
# ~1.6e15 Msun perturbation is r_ta ~ 20-40 Mpc (Lee&Komatsu measure infall at (2-3)R200,
# R200(main)~2.1 Mpc -> 4-6 Mpc, but that is the LATE-INFALL radius not the TURNAROUND; the
# energy integral from true turnaround ~10-40 Mpc reproduces AM08). We report the band.
print("\n(A) Framework infall velocity at the Hubble-flow turnaround band r_ta = 10-40 Mpc:")
print(f"   {'r_ta[Mpc]':>9} {'Newt-bar':>9} {'FW(dsU)':>9} {'MG(simple)':>11} {'CDM-tot':>9}")
for r_ta in [10,20,40]:
    R=r_ta*Mpc
    print(f"   {r_ta:>9} {vfall(M_bar,a0_fw,R,'newton')/km:>9.0f} {vfall(M_bar,a0_fw,R,'dsunruh')/km:>9.0f} "
          f"{vfall(M_bar,a0_fw,R,'simple')/km:>11.0f} {vfall(M_CDM,a0_fw,R,'newton')/km:>9.0f}")
vFW_lo=vfall(M_bar,a0_fw,20*Mpc,'dsunruh')/km
vFW_hi=vfall(M_bar,a0_fw,40*Mpc,'dsunruh')/km
vNB_lo=vfall(M_bar,a0_fw,20*Mpc,'newton')/km
vNB_hi=vfall(M_bar,a0_fw,40*Mpc,'newton')/km

# ---- (D) modified-INERTIA vs modified-GRAVITY: is the edge framework-distinctive? ----
print("\n(D) Framework-DISTINCTIVE (modified-INERTIA dS-Unruh) vs MOND-shared (modified-GRAVITY):")
for r_ta in [20,40]:
    R=r_ta*Mpc
    vMI=vfall(M_bar,a0_fw,R,'dsunruh')/km
    vMG=vfall(M_bar,a0_fw,R,'simple')/km
    print(f"   r_ta={r_ta} Mpc:  MI(dS-Unruh)={vMI:.0f}  MG(simple-mu)={vMG:.0f}  km/s  -> differ {100*(vMG-vMI)/vMI:+.1f}%")
print("   => the MI-vs-MG velocity difference is only ~4-5%: the deep-MOND tail (g=sqrt(GMa0)/r)")
print("      is IDENTICAL in both -> the velocity edge is MOND-FAMILY-SHARED, not distinctive.")

# ---- (C) LCDM probability (Lee & Komatsu 2010) ----
print("\n(C) LCDM probability of the required infall velocity (Lee & Komatsu 2010, MICE sim):")
print("   Adopted infall velocity (X-ray fit, Mastropietro&Burkert): 3000 km/s at 2 R200")
print("   P(v_infall >= 3000 km/s | LCDM, Mmain>=0.7e15 h^-1) = 3.3e-11 .. 3.6e-9  (6.5 / 5.8 sigma)")
print("   None of 1135 (z=0) / 78 (z=0.5) bullet-like LCDM systems reaches 3000 km/s.")
print("   No-tension threshold: v_infall < 1800 km/s at 2 R200.")
print("   Observed gas-shock (Markevitch&Vikhlinin 2007): 4740 (+710/-550) km/s")
print("   De-biased MASS bulk speed (Springel&Farrar 2007; Milosavljevic 2007): ~2700-3100 km/s")

# ---- (E) both-ways ledger ----
print("\n"+"="*86)
print("(E) BOTH-WAYS LEDGER")
print("="*86)
print(f"""
CREDIT (full weight) -- a GENUINE MOND-favorable result:
 * For the SAME observed BARYONIC mass ({M_bar/Msun:.2e} Msun), the framework's long-range
   (g=sqrt(GMa0)/r, 1/r) force pulls the pair from a deeper LOG-divergent well and reaches
   v ~ {vFW_lo:.0f}-{vFW_hi:.0f} km/s (dS-Unruh, a0=9.36e-11) at r_ta=20-40 Mpc -- IN the observed
   shock band (4740 +710/-550) and well above the de-biased bulk (2700-3100).
 * Newton on the SAME baryons caps at v ~ {vNB_lo:.0f}-{vNB_hi:.0f} km/s -- a MOND boost of ~{vFW_hi/vNB_hi:.2f}x.
   AM08's apples-to-apples 'CDM with MOND's baryon mass' = 2300-2700 km/s confirms this.
 * LCDM gets the high v ONLY by adding ~6x dark mass; even then Lee&Komatsu find the required
   3000 km/s infall is a 5.8-6.5 sigma tail (P~3e-11..4e-9). The Bullet is a genuine LCDM
   velocity strain that the framework's faster (MOND) structure formation accommodates.

CONCEDE (full weight) -- the edge is bounded, not a kill:
 * MOND-SHARED, not framework-distinctive: MI(dS-Unruh) vs MG(simple-mu) differ by only ~4-5%
   in v -- the deep-MOND asymptote sqrt(GMa0) is identical. This is a Lambda-MOND-family edge.
 * Gas-shock != mass bulk: the raw 4740 km/s is the GAS shock; hydrodynamics ADD ~600-1300 km/s
   over the DM/galaxy bulk speed (~2700-3100, Springel&Farrar 2007; Milosavljevic 2007). The
   apples-to-apples gravitational target is the BULK ~3000 km/s, which the framework clears
   comfortably but which LATER LCDM sims (Thompson&Nagamine 2012, Kraljic&Sarkar 2015) recover
   as rare-but-allowed -> a DING on LCDM, not a clean kill.
 * a0-quarantine: a0=9.36e-11 not derived; but v ~ (G M a0)^1/4 is a0-WEAK -- framework v is only
   {100*(1-(a0_fw/a0_can)**0.25):.1f}% below canonical a0=1.2e-10, so the edge survives the whole a0 band.

NET: a real, credited, MOND-shared, SOFT pro-framework result. The Bullet's high velocity is
NATURAL in the framework (and all of Lambda-MOND) and a 5.8-6.5 sigma STRAIN for LCDM -- the
opposite polarity from the 'Bullet proves dark matter' slogan. Not a framework-distinctive win
(MI~MG in the tail) and softened by the shock-vs-bulk distinction; not a manufactured debunk.
""")
