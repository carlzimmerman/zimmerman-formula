#!/usr/bin/env python3
# ROUTE 3 AUDIT -- PART 4: hydrostatic polytrope with MASS CONSERVATION imposed, and the
# resulting RAR shift priced against route5's own theorem.
import numpy as np
from scipy.optimize import brentq
FAIL=[]; N=[0]
def ck(c,lab,det=""):
    N[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {lab}"+(f"   {det}" if det else ""))
    if not ok: FAIL.append(lab)
G=6.674e-11; C=2.99792458e8; MSUN=1.989e30; KPC=3.086e19; MPC=1000*KPC
RHO_BG=0.264*8.6e-27
CS2=1.86e-10*C**2; K=CS2/(2*RHO_BG)
A0={"canonical":9.3619e-11,"alt":1.1279e-10}
SHARE=0.264/0.049

def gobs(r,Mb,a0):
    gb=G*Mb/r**2; return np.sqrt(gb**2+a0*gb)
def profile(Re,Mb,a0,ngrid=60001):
    r=np.logspace(np.log10(1e-4*Re),np.log10(Re),ngrid)
    g=gobs(r,Mb,a0)
    cum=np.concatenate(([0.0],np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(r))))
    dPhi=cum[-1]-cum                              # Phi(Re)-Phi(r) >= 0
    rho=dPhi/(2*K)                                # rho(Re)=0 truncation (ambient rho_bg negligible)
    M=np.concatenate(([0.0],np.cumsum(0.5*(4*np.pi*r[1:]**2*rho[1:]+4*np.pi*r[:-1]**2*rho[:-1])*np.diff(r))))
    return r,rho,M
print("="*100)
print("M -- MASS-CONSERVED hydrostatic polytrope: the galaxy gets its COSMIC SHARE and no more")
print("="*100)
print(f"    K = {K:.4g} SI, c_s(cosmic mean) = {np.sqrt(CS2)/1e3:.3f} km/s, lambda_J = {np.sqrt(2*np.pi*K/G)/KPC:.0f} kpc")
res={}
for MbMsun in (1e10, 5e10, 1e11):
    Mb=MbMsun*MSUN
    for foot,a0 in A0.items():
        rM=np.sqrt(G*Mb/a0); Mav=SHARE*Mb
        f=lambda Re: profile(Re,Mb,a0)[2][-1]-Mav
        Re=brentq(f, 0.2*rM, 500*KPC, xtol=1e17)
        r,rho,M=profile(Re,Mb,a0)
        Mph=r**2*(gobs(r,Mb,a0)-G*Mb/r**2)/G
        row=[]
        for fac in (0.5,1.0,3.0,10.0):
            i=np.argmin(abs(r-fac*rM))
            row.append(M[i]/Mph[i] if r[-1]>fac*rM else np.nan)
        i1=np.argmin(abs(r-rM))
        lam=1+M[i1]/Mb
        res[(MbMsun,foot)]=(Re/KPC, rM/KPC, row, lam, M[i1]/Mb)
        print(f"    M_b={MbMsun:8.3g} Msun  {foot:9s}  r_M={rM/KPC:6.2f} kpc  R_edge={Re/KPC:6.1f} kpc "
              f"({Re/rM:5.1f} r_M)   M_sec/M_phantom at 0.5/1/3/10 r_M = "
              + " / ".join(f"{v:.4g}" if np.isfinite(v) else "  --" for v in row))
print()
ov=[res[k][2][1] for k in res]
ck(max(ov)<0.2,
   f"M1  *** with mass conservation imposed the double count at r_M is {min(ov):.4g}-{max(ov):.4g} "
   "across 1e10-1e11 Msun and BOTH footings -- against the committed 25.7x (step halo) and the "
   "corrected 1.93x (NFW at the cosmic share) ***",
   "the sector cannot deliver its share inside r_M because its pressure gives it a CORE")
print("="*100)
print("N -- the RAR shift, priced against route5's OWN theorem (no new machinery)")
print("="*100)
print("    route5: g_obs = a0 N(y), 1/2 <= dlnN/dlny <= 1  =>  source x lambda  =>  g_obs x R in [sqrt(lam), lam]")
print(f"    route5's INPUT was lambda = 1 + Om_dm/Om_b = {1+SHARE:.4f}  ->  0.402-0.805 dex (6.7-13.4x the 0.06 dex floor)")
print(f"    {'M_b':>10s} {'foot':>10s} {'lambda(r_M)':>12s} {'shift dex':>18s} {'/ 0.06 dex floor':>18s}")
worst=0
for k,v in res.items():
    lam=v[3]; lo=np.log10(np.sqrt(lam)); hi=np.log10(lam); worst=max(worst,hi)
    print(f"    {k[0]:10.3g} {k[1]:>10s} {lam:12.5f} {lo:8.4f}-{hi:.4f} {lo/0.06:11.3f}-{hi/0.06:.3f}")
ck(worst < 0.06,
   f"N1  *** the WORST-CASE RAR shift is {worst:.4f} dex, i.e. {0.06/worst:.1f}x BELOW the 0.06 dex "
   "intrinsic scatter -- route5's theorem is untouched; what falls is its INPUT lambda ***",
   "hypothesis (iii) 'the sector is dust' enters route5 only through lambda = 6.375; a warm sector "
   f"gives lambda = {min(v[3] for v in res.values()):.4f}-{max(v[3] for v in res.values()):.4f} at r_M")
print()
print("="*100); print("O -- where this construction is VULNERABLE (stated before anyone else finds it)"); print("="*100)
print("    1. TOTAL BUDGET.  The sector still carries full Omega_dm; it is now spread over")
print(f"       R_edge ~ {min(v[0] for v in res.values()):.0f}-{max(v[0] for v in res.values()):.0f} kpc rather than concentrated. Clusters (r_200 ~ 2 Mpc >> lambda_J = 603 kpc)")
print("       KEEP their dark mass, which is the sign the framework needs -- but the CLUSTER")
print("       profile must now be recomputed, and it is NOT done here.")
print("    2. LYMAN-ALPHA.  Part 2/J: k_J = 1.9-3.8 /Mpc at z = 5-2, inside the forest window.")
print("       The corpus's committed forest work used a different c_s^2 and does not cover this.")
print("    3. STAGE 69's BOUND.  Lambda_D/Q_0 <= 3.1e-6; the (u_0, nu_0-floor) pair used here gives")
print("       8.7e-6, 2.8x OVER. It is relieved by moving nu_0 to ~6e-5 (inside the stage17 window),")
print("       which leaves c_s^2(today) = u_0 UNCHANGED -- but that reshuffle is owed a check.")
print("    4. EIGENMODES.  c_s^2 is the SECTOR's adiabatic speed; the AeST scalar eigenmodes are")
print("       mixtures. Flagged in RETRACTIONS.md 2026-08-19 and still open.")
print("    5. EQUILIBRIUM.  Assumed reached (crossing time ~0.25 Gyr) and spherical.")
print("    6. SELF-GRAVITY of the sector neglected -> true profile slightly DENSER -> M1 is a mild")
print("       UNDERSTATEMENT of the double count. Direction stated.")
print("="*100); print(f"CHECKS {N[0]-len(FAIL)}/{N[0]}"+("" if not FAIL else "   FAILED: "+"; ".join(FAIL)))
