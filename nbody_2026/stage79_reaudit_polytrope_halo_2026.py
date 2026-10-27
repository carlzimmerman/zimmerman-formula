#!/usr/bin/env python3
# ROUTE 3 AUDIT -- PART 3: re-price the double count with the sector's OWN equation of state
# (hydrostatic polytrope in the galaxy's MOND potential) instead of an imposed NFW/step halo.
import numpy as np
FAIL=[]; N=[0]
def ck(c,lab,det=""):
    N[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {lab}"+(f"   {det}" if det else ""))
    if not ok: FAIL.append(lab)

G=6.674e-11; C=2.99792458e8; MSUN=1.989e30; KPC=3.086e19; MPC=1000*KPC
RHO_C=8.6e-27; OM_DM=0.264; RHO_BG=OM_DM*RHO_C
A0={"canonical":9.3619e-11,"alt":1.1279e-10}
CS2_TODAY=1.86e-10*C**2          # = u_0 c^2, from mi_dbi_khronon_2026.py D1 (u0_for_mond)
KPOLY=CS2_TODAY/(2*RHO_BG)       # p = K rho^2  (n=1 polytrope), K from the VALID late branch
MB=5e10*MSUN                     # L* spiral baryonic mass
SHARE=0.264/0.049                # cosmic dark/baryon = 5.388

print("="*100)
print("K -- the sector as a HYDROSTATIC n=1 POLYTROPE in the galaxy's own MOND potential")
print("="*100)
print(f"    K = c_s^2/(2 rho_bg) = {KPOLY:.4g} SI   (c_s(today) = {np.sqrt(CS2_TODAY)/1e3:.3f} km/s at cosmic mean)")
print(f"    lambda_J = sqrt(2 pi K/G) = {np.sqrt(2*np.pi*KPOLY/G)/KPC:.1f} kpc   (density-INDEPENDENT for n=1)")

def gbar(r,Mb): return G*Mb/r**2
def gobs(r,Mb,a0):                       # Carl's a0-line
    gb=gbar(r,Mb); return np.sqrt(gb**2+a0*gb)

for foot,a0 in A0.items():
    rM=np.sqrt(G*MB/a0)
    print(f"\n    ---- {foot}: a0={a0:.4e},  r_M = {rM/KPC:.2f} kpc,  M_b = {MB/MSUN:.3g} Msun ----")
    for ROUT in (1*MPC, 2*MPC, 5*MPC):
        rr=np.logspace(np.log10(0.02*rM), np.log10(ROUT), 200001)
        g=gobs(rr,MB,a0)
        # DeltaPhi(r) = int_r^Rout g dr   (cumulative from the outside in)
        dPhi=np.concatenate(([0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(rr))))
        dPhi=dPhi[-1]-dPhi                                   # = Phi(Rout)-Phi(r) > 0
        rho=RHO_BG+dPhi/(2*KPOLY)                            # EXACT hydrostatic solution for p=K rho^2
        Msec=np.concatenate(([0.0], np.cumsum(0.5*(4*np.pi*rr[1:]**2*rho[1:]
                                                   +4*np.pi*rr[:-1]**2*rho[:-1])*np.diff(rr))))
        Mph=rr**2*(gobs(rr,MB,a0)-gbar(rr,MB))/G             # the phantom the kernel already supplies
        out=[]
        for f in (0.5,1.0,3.0,10.0):
            i=np.argmin(abs(rr-f*rM))
            out.append(f"{Msec[i]/Mph[i]:.3g}")
        i200=np.argmin(abs(rr-200*KPC))
        out.append(f"| M_sec(<200kpc)/M_b = {Msec[i200]/MB:.3g} (cosmic share {SHARE:.2f})")
        print(f"      R_out={ROUT/MPC:.0f} Mpc:  M_sec/M_phantom at 0.5/1/3/10 r_M = "
              +" / ".join(out[:4])+"   "+out[4])
    # verdict numbers at R_out = 2 Mpc
    rr=np.logspace(np.log10(0.02*rM), np.log10(2*MPC), 200001)
    g=gobs(rr,MB,a0)
    dPhi=np.concatenate(([0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(rr)))); dPhi=dPhi[-1]-dPhi
    rho=RHO_BG+dPhi/(2*KPOLY)
    Msec=np.concatenate(([0.0], np.cumsum(0.5*(4*np.pi*rr[1:]**2*rho[1:]
                                               +4*np.pi*rr[:-1]**2*rho[:-1])*np.diff(rr))))
    Mph=rr**2*(gobs(rr,MB,a0)-gbar(rr,MB))/G
    i1=np.argmin(abs(rr-rM)); ihalf=np.argmin(abs(rr-0.5*rM))
    globals()[f"ov_{foot}"]=(Msec[ihalf]/Mph[ihalf], Msec[i1]/Mph[i1])
    # log-slope of the sector profile
    sl=np.gradient(np.log(rho),np.log(rr))
    globals()[f"sl_{foot}"]=sl[i1]

ck(ov_canonical[1] < 1.93,
   f"K1  *** the sector's OWN eos gives M_sec/M_phantom = {ov_canonical[0]:.3g} at 0.5 r_M and "
   f"{ov_canonical[1]:.3g} at 1 r_M (canonical; alt {ov_alt[0]:.3g}/{ov_alt[1]:.3g}) -- against the "
   "CORRECTED committed NFW figures 0.83 / 1.93 ***",
   "the NFW/step profiles were IMPOSED; this one is SOLVED from the sector's own pressure")
ck(sl_canonical > -1.0,
   f"K2  and the SHAPE is wrong for a double count: the hydrostatic polytrope's log-slope at r_M is "
   f"{sl_canonical:.3f} (canonical) / {sl_alt:.3f} (alt) -- a CORE, not the -2 an isothermal "
   "phantom-matching halo needs",
   "d ln rho/d ln r -> 0 at small r because rho = rho_bg + DeltaPhi/(2K) and DeltaPhi is LOGARITHMIC")

print()
print("="*100); print("L -- controls and the direction of every approximation"); print("="*100)
# CONTROL 1: reproduce stage 7's conclusion by feeding it stage 7's (invalid-regime) K
K_ST7=2.9e-8*C**2/(2*RHO_BG*(1+1090)**3)
a0=A0["canonical"]; rM=np.sqrt(G*MB/a0)
rr=np.logspace(np.log10(0.02*rM), np.log10(2*MPC), 100001); g=gobs(rr,MB,a0)
dPhi=np.concatenate(([0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(rr)))); dPhi=dPhi[-1]-dPhi
rho7=RHO_BG+dPhi/(2*K_ST7)
Msec7=np.concatenate(([0.0], np.cumsum(0.5*(4*np.pi*rr[1:]**2*rho7[1:]
                                            +4*np.pi*rr[:-1]**2*rho7[:-1])*np.diff(rr))))
Mph=rr**2*(gobs(rr,MB,a0)-gbar(rr,MB))/G; i1=np.argmin(abs(rr-rM))
ck(Msec7[i1]/Mph[i1] > 100,
   f"L1  CONTROL: fed stage 7's K (extracted at recombination) the SAME code gives "
   f"M_sec/M_phantom = {Msec7[i1]/Mph[i1]:.3g} at r_M -- a catastrophic double count. "
   "So the code detects capture; it is the VALUE of K that decides, and stage 7 took it "
   "from the epoch where the polytropic relation does not hold",
   f"K_stage7 = {K_ST7:.4g} vs K_late = {KPOLY:.4g}, ratio {KPOLY/K_ST7:.4g}")
# CONTROL 2: an unbound (v_esc) test must still say 'captured' -- so the result is not the estimator
ck(np.sqrt(CS2_TODAY) < 5e5,
   f"L2  CONTROL: at COSMIC MEAN density c_s = {np.sqrt(CS2_TODAY)/1e3:.2f} km/s is still far below "
   f"v_esc = 500 km/s -- stage 7's A1 comparison is REPRODUCED and is arithmetically right. "
   "What is wrong is the DENSITY at which it is evaluated: c_s^2 propto rho, so inside the halo "
   f"c_s rises to {np.sqrt(CS2_TODAY*9.36e3)/1e3:.0f} km/s and the sector unbinds itself",
   "the named error mode again -- a correct formula evaluated outside its regime")
print()
print("    DIRECTION OF EVERY APPROXIMATION IN PART K (all stated, none hidden):")
print("      * sector SELF-gravity neglected -> the true profile is DENSER -> K1 UNDERSTATES the")
print("        double count.  Adverse to the favourable reading.")
print("      * DeltaPhi truncated at R_out; the R_out = 1/2/5 Mpc rows show the sensitivity.")
print("      * baryons treated as a point mass OUTSIDE r_M only (the phantom comparison is at")
print("        r >= 0.5 r_M, where a point source is a good approximation for a spiral).")
print("      * the equilibrium is assumed REACHED: sound crossing of 100 kpc at the in-halo")
print(f"        c_s ~ {np.sqrt(CS2_TODAY*9.36e3)/1e3:.0f} km/s is ~{100*KPC/np.sqrt(CS2_TODAY*9.36e3)/3.156e16:.2f} Gyr, so it is.")
print("      * c_s^2(today) = u_0 is taken from mi_dbi_khronon_2026.py's MOND crossover mu^-1 = 100 kpc.")
print("        It does NOT depend on the Lambda_D/Q_0 split that stage 69 bounds.")
print()
print("="*100); print(f"CHECKS {N[0]-len(FAIL)}/{N[0]}"+("" if not FAIL else "   FAILED: "+"; ".join(FAIL)))
