"""argon_clues: arithmetic audit of the pasted 'CFG780' answers (hot-gas threshold, core trapping, UFD, cold->DE conversion)."""
import math, numpy as np
G=6.6743e-11; c=2.99792458e8; kB=1.380649e-23; mp=1.67262192e-27; pc=3.085677581e16; Msun=1.98847e30; yr=3.15576e7
a0=9.36e-11; Ls=5.75*pc
# P2: crossing time across L* equals tau_rel = sqrt(L*/a0)
tau=math.sqrt(Ls/a0); cs=Ls/tau
print('P2 tau_rel = %.2e s = %.2f Myr (paste 1.27 ok)'%(tau,tau/yr/1e6))
print('   c_s,crit = L*/tau = sqrt(L* a0) = %.2f km/s   (paste says 139 km/s)'%(cs/1e3))
T=0.6*mp*cs**2/((5/3)*kB)
print('   T_crit = %.0f K  (paste says 7e5 K)  -> warm HI at 8000 K and 1e4 K ionized gas would be UNTETHERED, cold HI 100K tethered'%T)
print('   paste check: 139 km/s^2 would need L* a0 = %.2e m^2/s^2, i.e. a0 ~ %.1e m/s^2 or L*~%.0f pc'%((139e3)**2,(139e3)**2/Ls,(139e3)**2/a0/pc))
# P3: 1 + R/(2 pi)
for R in (5.364,4.80): 
    r=1+R/(2*math.pi); print('P3 1+R/2pi, R=%.3f -> %.3f (%.3f dex)'%(R,r,math.log10(r)))
fneed=lambda target,R:(target-1)/R
print('   f_trap needed: ellipticals x1.905 (0.28 dex): %.3f ; clusters x1.80: %.3f ; 1/2pi = %.3f ; they differ -> 2pi is a post-hoc choice, no derivation of f_trap'%(fneed(1.905,4.8),fneed(1.8,4.8),1/(2*math.pi)))
# P4: pasted stiffness_boost and u_arrest
def ufd(M,r_pc,t_gyr=8.0):
    M*=Msun; r=r_pc*pc; gN=G*M/r**2; g=0.5*(gN+math.sqrt(gN**2+4*gN*a0))
    boost=1+(Ls/(r/math.sqrt(3)))**2
    tor=t_gyr*1e9*yr; u=math.sqrt(r*a0)/(tor*math.sqrt(a0/Ls))
    return 0.5*math.log10((g*boost+u)/g), boost, u/g
print('P4 UFD (3e3 Msun, 25 pc): delta dex = %.3f (boost %.2f, arrest/g %.2e)  [target +0.33]'%ufd(3e3,25)[:1]+'' if False else 'P4 UFD (3e3 Msun, 25 pc): (delta dex, boost, arrest/g) = %s  [target +0.33]'%(tuple(round(v,4) for v in ufd(3e3,25)),))
print('   same formula, 2 vs 3e3 Msun: %s ; r=15pc: %s ; r=50pc: %s -> dex set by the hand-built (L*/r)^2 boost (arrest term negligible)'%(tuple(round(v,3) for v in ufd(3e3,25))[0],tuple(round(v,3) for v in ufd(3e3,15))[0],tuple(round(v,3) for v in ufd(3e3,50))[0]))
# P5: back-solve the average (1+z)^3
Ob=0.0493; ODE=0.6847; dR=5.364-4.80
need=(1-0.85**2)*ODE/(Ob*dR)
print('P5 <(1+z)^3> needed to hit a0(2)/a0(0)=0.85 with all depletion dR=%.3f at z<2: %.2f (paste uses 6.84: back-solved, not derived)'%(dR,need))
z=np.linspace(0,6,6001); psi=(1+z)**2.6/(1+((1+z)/2.6)**6.2); psi/=np.trapz(psi,z)
i=np.searchsorted(z,2.0); d=Ob*np.trapz(((1+z[:i+1])**3)*dR*psi[:i+1],z[:i+1])
print('   pasted script P5 (shape psi, dR spread over 0..6): delta Omega_DE(z<2) = %.4f -> a0 ratio = %.3f (paste window 0.82-0.88)'%(d,math.sqrt((ODE-d)/ODE)))
print('   fraction of dR placed below z=2 by psi: %.2f ; 0.564 of 5.364 = 10.5%% depletion itself (R(0)=4.80) is an INPUT, not an output'%(np.trapz(psi[:i+1],z[:i+1])))
print('P1 note: "virial partition 1/2 between |grad Phi|^2/2K and K|P|^2/2" is asserted; the Part A no-go (a0 is a free integration scale in the static action) is correct and consistent with this folder.')
