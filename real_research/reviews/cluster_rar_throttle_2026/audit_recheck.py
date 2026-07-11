import numpy as np
Z=np.sqrt(32*np.pi/3); yc=Z/2; a0=9.36e-11
nu=lambda y:np.sqrt(1+1/y)
T=lambda y,n:np.minimum(1,(yc/y)**n)
gt=lambda y,n:1+(nu(y)-1)*T(y,n)   # throttled ratio
# independent hand re-derivation at y=5,10
for y in [5,10]:
    r_m=nu(y); r_t=gt(y,1)
    dex=np.log10(r_m/r_t); loss=100*(r_t/r_m-1)
    print(f"y={y}: nu={r_m:.5f} throt={r_t:.5f} dex={dex:.4f} loss={loss:.2f}%")
print()
# ACTUAL Tian+2020 g_bar coverage -> framework y (a0=9.36e-11)
print("Tian+2020 REAL g_bar axis: log10 ~ -11 to -10 (bulk); innermost BCG point higher")
for lg in [-11,-10.5,-10,-9.7,-9.4,-9]:
    gb=10**lg; print(f"  log g_bar={lg}: g_bar={gb:.2e}  y=g_bar/a0={gb/a0:.2f}")
print()
print(f"y_c (break) = {yc:.3f}  -> g_bar_break = {yc*a0:.2e} m/s^2 = log10 {np.log10(yc*a0):.2f}")
print(f"fingerprint PEAK at y~6.1 -> g_bar = {6.1*a0:.2e} = log10 {np.log10(6.1*a0):.2f}")
print()
# intrinsic scatter of Tian: 14.7% lognormal -> dex
sig_ln=0.147; sig_dex=sig_ln/np.log(10)
print(f"Tian intrinsic scatter: 14.7% lognormal = sigma_ln {sig_ln} = {sig_dex:.4f} dex")
print(f"predicted break peak (n=1) 0.017 dex  =>  {0.017/sig_dex:.2f}x the scatter floor")
print(f"predicted break peak (n=2) 0.026 dex  =>  {0.026/sig_dex:.2f}x the scatter floor")
# physical g_bar estimates at cluster radii (massive CLASH cluster)
print()
G=6.674e-11; Msun=1.989e30; kpc=3.086e19
def gbar(M_Msun,r_kpc): return G*M_Msun*Msun/(r_kpc*kpc)**2
print("Physical g_bar estimates (baryon = gas+BCG stars), massive cluster:")
for M,r,lab in [(5e11,14,'BCG core 14kpc'),(8e11,30,'BCG 30kpc'),(8e12,100,'gas 100kpc'),(2e13,200,'gas 200kpc')]:
    gb=gbar(M,r); print(f"  {lab:18s}: g_bar={gb:.2e}  y={gb/a0:.2f}")
