import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; c=3e8
a0=9.36e-11
M=5e10*Msun
def nu(gbar): return np.sqrt(1+np.sqrt(1+4*a0/gbar))/np.sqrt(2)
print("T3 CRUX: is the a0 enhancement '1e6 too small' (reported verdict) or 'right order' (framework script)?")
print("Compare the EXTRA lensing POTENTIAL needed, (nu-1)*Phi_bar, to the a0 potential a0*r/c^2.")
print(f"{'r[kpc]':>7} {'gbar':>10} {'nu':>6} {'Phi_bar':>10} {'(nu-1)Phi_bar':>13} {'a0*r/c^2':>10} {'ratio a0term/needed':>18}")
for rk in (5,10,20,40,100,300):
    r=rk*kpc; gbar=G*M/r**2; n=nu(gbar)
    Phib=G*M/r/c**2
    need=(n-1)*Phib
    a0term=a0*r/c**2
    print(f"{rk:>7} {gbar:>10.2e} {n:>6.2f} {Phib:>10.2e} {need:>13.2e} {a0term:>10.2e} {a0term/need:>18.2f}")
print()
print("Now the ENERGY-BUDGET core (Lane2): enclosed effective mass needed vs baryon rest mass.")
print(f"{'r[kpc]':>7} {'nu':>6} {'M_eff/M_bar=(nu-1)':>18}   (>1 => exceeds baryon energy budget)")
for rk in (5,10,20,21,40,100,300):
    r=rk*kpc; gbar=G*M/r**2; n=nu(gbar)
    print(f"{rk:>7} {n:>6.2f} {n-1:>18.3f}")
