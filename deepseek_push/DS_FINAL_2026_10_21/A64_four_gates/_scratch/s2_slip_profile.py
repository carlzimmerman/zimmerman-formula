import numpy as np
G = 6.67430e-11; C = 2.99792458e8; MSUN = 1.98892e30; PC = 3.0856775814913673e16
K = 4*np.pi*G/C**2          # m/kg  (geometric)
A0 = 9.36e-11               # m/s^2
A0g = A0/C**2               # 1/m
MBAR = 5e10*MSUN; AH = 3e3*PC
print("K =", K, " a0(1/m) =", A0g, " L*a0 =", (24*PC)*A0g)

def gN(r):
    Mb = MBAR*r**2/(r+AH)**2
    return G*Mb/r**2

def gMOND(gn):
    return 0.5*gn*(1+np.sqrt(1+4*A0/gn))

rr = np.geomspace(1e-3*PC, 3e8*PC, 400001)
gn = gN(rr); g = gMOND(gn); u = (g-gn)                     # m/s^2
ug = u/C**2                                                # 1/m
x = ug/A0g                                                 # u/a0
Pi = ug**2/(K*(1-x))                                       # kg/m^3
integrand = Pi/rr
seg = 0.5*(integrand[1:]+integrand[:-1])*np.diff(rr)
outer = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])  # int_r^inf Pi/r' dr'
for mult in (2.0, 3.0):
    print(f"--- coefficient {mult:g}K")
    for rk in (10.0, 100.0):
        r0 = rk*1e3*PC
        j = int(np.argmin(abs(rr-r0)))
        fp = -mult*K*r0*outer[j]
        # f(r) = int_r^inf ... : f(r) = int_r^inf 2K r' int_r'^inf Pi/r'' dr'' dr'
        # integrate f' from r to infinity
        segf = 0.5*(np.abs(-mult*K*rr*outer)[1:]+np.abs(-mult*K*rr*outer)[:-1])*np.diff(rr)
        fabs = np.concatenate([np.cumsum(segf[::-1])[::-1], [0.0]])[j]
        Psi = g[j]*r0/C**2
        print(f"  r={rk:5.1f} kpc  u/a0={x[j]:.4f}  Psi={Psi:.3e}  |Phi-Psi|={fabs:.3e}  |1-Phi/Psi|={fabs/Psi:.3e}  (Pi/sigma)/(Psi)={-(ug[j]**2/K)/(ug[j]/(K*r0))/Psi if True else 0:.4f}")