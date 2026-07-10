import math
# Fresh-session independent re-derivation (no imports from lane3 script)
G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19; AU=1.496e11
Z=math.sqrt(32*math.pi/3)
a0=9.36e-11; a0V=Z*a0          # cH_Lambda on the framework's own medium footing
print("Z =",Z, " cH_Lambda =",a0V)

# Verlinde 2016 point-mass relation: int_0^r G M_D^2/r'^2 dr' = M_b a0V r / 6
# ansatz M_D = A r  ->  G A^2 r = M_b a0V r/6  ->  A = sqrt(a0V M_b/(6G)).  Consistent.
# g_D = G M_D/r^2 = sqrt(a0V G M_b /6)/r = sqrt(a0V g_bar/6).  Matches report formulas.

# DECISIVE DEEP RATIO: required M_eff -> sqrt(a0 M_b/G) r ; candidate M_D = sqrt(a0V M_b/(6G)) r
print("deep coefficient M_D/M_eff = sqrt(Z/6) =", math.sqrt(Z/6))
print("equivalent a0_eff/a0 = Z/6 =", Z/6, " -> a0_eff =", a0*Z/6)

# spot ratio at r=5 kpc, M_b=1e11 Msun
Mb=1e11*Msun
for rk in (5,10,20,50,100):
    r=rk*kpc
    gbar=G*Mb/r**2; y=gbar/a0
    nu=math.sqrt(1+1/y)
    Meff=Mb*(nu-1)
    MD=math.sqrt(a0V*Mb/(6*G))*r
    print(f"r={rk:4d} kpc  y={y:8.3f}  M_D/M_eff={MD/Meff:6.3f}")

# high-g overshoot: g_D/((nu-1)g_bar) = sqrt(a0V g_bar/6)/((nu-1)g_bar)
for y in (6,600,7e5):
    gbar=y*a0
    gD=math.sqrt(a0V*gbar/6)
    greq=(math.sqrt(1+1/y)-1)*gbar
    print(f"y={y:9.0f}  overshoot={gD/greq:9.1f}x")

# Saturn unscreened enclosed M_D vs ephemeris bound
rS=9.58*AU
MD_S=math.sqrt(a0V*Msun/(6*G))*rS/Msun
bound=1.7e-10
print(f"Saturn M_D={MD_S:.3e} Msun; /bound={MD_S/bound:.2e} = {math.log10(MD_S/bound):.2f} orders")
# nu-screened bare monopole
gbarS=G*Msun/rS**2; yS=gbarS/a0
nuS=math.sqrt(1+1/yS)
print(f"Saturn y={yS:.3e}; M(nu-1)={nuS-1:.3e} Msun; orders over={math.log10((nuS-1)/bound):.2f}; dg tail={(nuS-1)*gbarS:.3e} (a0/2={a0/2:.3e})")
# cross-check with Verlinde's own cH0
H0=67.4e3/3.0857e22; print("cH0 =",c*H0, " deep cross ratio sqrt(cH0/(6 a0)) =", math.sqrt(c*H0/(6*a0)))
# Q2 sigma from banked numbers
for q in (1.2e-26,2.0e-26): print(f"MG Q2={q:.1e}: sigma=({q}-1.6e-27)/1.8e-27 = {(q-1.6e-27)/1.8e-27:.1f}")
