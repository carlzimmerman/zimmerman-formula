"""
COSMOLOGY for Parts C,D -- DESI DR2 CPL fluid.
w(a) = w0 + wa(1-a),  w0=-0.752, wa=-0.86, Om=0.315, OL=0.685 (flat).
rho_DE(a)/rho_DE0 = a^{-3(1+w0+wa)} exp(-3 wa (1-a))
E(z) = H/H0 = sqrt(Om(1+z)^3 + OL * rho_DE(a)/rho_DE0)   [flat, ignore radiation]

Framework ansatz: T(z) ∝ sqrt(rho_DE(z))  => ln T = const + (1/2) ln rho_DE.
Therefore  d ln T/dt = (1/2) d ln rho_DE/dt.

For a CPL fluid, the continuity equation gives EXACTLY:
   d ln rho_DE / d ln a = -3(1+w(a))
   d ln rho_DE / dt     = -3(1+w(a)) * H        (since d ln a/dt = H)
   => d ln T/dt = -(3/2)(1+w(a)) H
   => |d ln T/dt| = (3/2)|1+w(a)| H    (note 1+w>0 here since w>-1 throughout for these params? check)
This is GATE-INDEPENDENT input; the gate multiplies it.

H_DE: an "effective DE Hubble rate". Define via the DE density alone:
   H_DE(z) = sqrt( (8 pi G/3) rho_DE(z) ) = H0 sqrt(OL * rho_DE(a)/rho_DE0).
At z=0: H_DE(0) = H0 sqrt(OL) = H0*sqrt(0.685).
"""
import numpy as np

# Params (DESI DR2 CPL)
w0, wa, Om, OL = -0.752, -0.86, 0.315, 0.685
H0 = 1.0  # work in units of H0; restore where needed

def a_of_z(z): return 1.0/(1.0+z)
def w_of_a(a): return w0 + wa*(1.0-a)
def rhoDE_ratio(a):  # rho_DE(a)/rho_DE0
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))
def E_of_z(z):
    a=a_of_z(z); return np.sqrt(Om*(1+z)**3 + OL*rhoDE_ratio(a))
def H_of_z(z):  # in units H0
    return H0*E_of_z(z)
def H_DE_of_z(z):  # effective DE Hubble (DE density only), units H0
    a=a_of_z(z); return H0*np.sqrt(OL*rhoDE_ratio(a))
def dlnT_dt(z):   # = -(3/2)(1+w) H  ; returns signed (units H0)
    a=a_of_z(z); return -1.5*(1.0+w_of_a(a))*H_of_z(z)
def abs_dlnT_dt(z):
    return abs(dlnT_dt(z))

print("z      a       w(a)     1+w     rhoDE/rhoDE0   E(z)=H/H0   H_DE/H0   |dlnT/dt|/H0")
for z in [0,0.4,1,2,3,5,10]:
    a=a_of_z(z)
    print(f"{z:<5} {a:.4f}  {w_of_a(a):+.4f} {1+w_of_a(a):+.4f}   {rhoDE_ratio(a):.5f}      "
          f"{E_of_z(z):.4f}     {H_DE_of_z(z):.4f}   {abs_dlnT_dt(z):.5f}")

# Zero-lag decline a0(3)/a0(0) = sqrt(rhoDE(3)/rhoDE(0)) since a0 ∝ sqrt(rhoDE), T∝sqrt(rhoDE)
r3 = rhoDE_ratio(a_of_z(3))/rhoDE_ratio(a_of_z(0))
print(f"\nZERO-LAG a0(3)/a0(0) = sqrt(rhoDE(3)/rhoDE(0)) = sqrt({r3:.5f}) = {np.sqrt(r3):.5f}")
print("  (problem statement quotes ~0.737)")

# sign of 1+w: is DE ever phantom (w<-1) in 0..10?
zz=np.linspace(0,10,1000); aa=a_of_z(zz)
print("min(1+w) on z in [0,10]:", (1+w_of_a(aa)).min(), " max:", (1+w_of_a(aa)).max())
print("  => 1+w sign on this range; w0=-0.752 (today), wa=-0.86 (more neg in past->")
print("     at a->0, w-> w0+wa = ", w0+wa, " => 1+w =", 1+w0+wa, "(still > 0: quintessence-like, never phantom here)")
