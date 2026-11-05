"""Worked numbers quoted in 'The Universe of Knobs'. Run: python3 numbers.py"""
import math
c=2.99792458e8; G=6.674e-11; kpc=3.0857e19; Msun=1.989e30
a0=9.3603e-11; a0_alt=1.1312e-10; kappa=0.5
rho_de=(a0/(kappa*c))**2/G
print(f"rho_DE implied by canonical a0: {rho_de:.4e} kg/m^3 = {rho_de*c**2/1.602e-10:.3f} GeV/m^3")
# Zimmerman Z
Z=2*math.sqrt(8*math.pi/3); print(f"Z = 2 sqrt(8pi/3) = {Z:.4f}")
H0_alt=a0_alt*Z/c; print(f"H0 implied by alt footing cH0/Z: {H0_alt*kpc*1e3/1e3:.2f} km/s/Mpc")
# Lambda pull at 10 kpc
r=10*kpc; gL=8*math.pi*G*rho_de*r/3; print(f"Lambda pull at 10 kpc: {gL:.3e} = {gL/a0:.2e} a0")
# BTFR examples
for Mb in (1e9,1e10,6e10,1e11):
    v=(G*Mb*Msun*a0)**0.25; print(f"BTFR v_flat for Mb={Mb:.0e}: {v/1e3:.1f} km/s")
# MOND radius for MW-like 6e10
Mb=6e10*Msun; rM=math.sqrt(G*Mb/a0); print(f"r_M for 6e10 Msun: {rM/kpc:.2f} kpc")
# bits
def bits(lo,hi,width_dex): return math.log2(math.log10(hi/lo)/width_dex)
print("kappa bits (0.1..10, 5%=0.0212 dex):", round(bits(0.1,10,math.log10(1.05)),2))
print("10^500 vacua bits:", round(500*math.log2(10),1), "; 10^272000:", round(272000*math.log2(10)))
# a0(z) for H(z) rival with flat Om
for z in (1,1.5,2.33):
    E=math.sqrt(0.315*(1+z)**3+0.685); print(f"z={z}: E(z)={E:.3f}; BTFR shift for a0~H: {-math.log10(E):+.3f} dex in Mb at fixed v")
# CPL illustrative
def rde(z,w0,wa): return (1+z)**(3*(1+w0+wa))*math.exp(-3*wa*z/(1+z))
for z in (0.5,1,1.5,2,2.33):
    print(f"CPL(-0.75,-0.80) z={z}: sqrt(rho/rho0) = {math.sqrt(rde(z,-0.75,-0.80)):.3f}")
# deep MOND transition and law inverse example
gN=0.1*a0; g=gN/2+math.sqrt(gN**2/4+gN*a0); print(f"g at gN=0.1 a0: {g/a0:.4f} a0, boost {g/gN:.3f}")
# BIC example: k ln n
n=3373
for k in (1,12,14,1026):
    print(f"BIC penalty k ln n, k={k}: {k*math.log(n):.1f}")
# dex of 0.0415
print("0.0415 dex as percent:", round((10**0.0415-1)*100,2))
# sigma^4 = G Mb a0 /4 isothermal: sigma for 1e10
print("sigma for Mb=1e10:", round((G*1e10*Msun*a0/4)**0.25/1e3,1), "km/s")
# Planck nuisance etc not computed. 
# --- Chapter 6: the c-barrier, halo accelerations built without c
H0=67.4e3/3.0857e22
OmL=0.685
def m(x): return math.log(1+x)-x/(1+x)
M=1e12*Msun
r200=(G*M/(100*H0**2))**(1/3); V200=10*H0*r200
print(f"M200=1e12: r200={r200/kpc:.0f} kpc, V200={V200/1e3:.1f} km/s, c/V200={c/V200:.0f}")
a0_check=0.5*c*H0*math.sqrt(3*OmL/(8*math.pi)); print(f"a0 = 0.5 c H0 sqrt(3 OmL/8pi) = {a0_check:.4e}")
for conc in (7,8,10):
    g_rs=10*H0*V200*conc**2*m(1)/m(conc); g_c=10*H0*V200*conc**2/(2*m(conc))
    print(f"c={conc}: g(r_s)={g_rs/a0:.2f} a0, 2 pi G rho_s r_s={g_c/a0:.2f} a0")
# Lambda coincidence kappa_eff
print("kappa_eff Lambda coincidence:", round(math.sqrt(8*math.pi/3)/(2*math.pi),4))
print("kappa_eff cH0/2pi on rho_DE:", round(math.sqrt(8*math.pi/3)/(2*math.pi)/math.sqrt(OmL),4))
# halo acceleration scaling with H at fixed mass: a ~ M^(1/3) H^(4/3)
for z,Er in ((1,1.76),(1.5,2.35),(2.33,3.49)):
    print(f"z={z}: H ratio {Er} -> halo accel at fixed M and c rises x{Er**(4/3):.2f}")
# --- Chapter 10 table: MOND radius r_M = sqrt(G M / a0)
for Mb in (1e9,1e10,6e10,1e11):
    print(f"r_M for Mb={Mb:.0e}: {math.sqrt(G*Mb*Msun/a0)/kpc:.2f} kpc")
