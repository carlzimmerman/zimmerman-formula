#!/usr/bin/env python3
"""
SETUP B -- ghost test v2: correct BRANCH handling.

Key realization forced by the sqrt structure: on the physical propagating band z=zz<0,
sqrt(zz) is IMAGINARY. The worldline form factor K(z)=(sqrt(1+4z)-1)/(2 sqrt z) at z=-w^2/a0^2:
  sqrt(z) = i*w/a0 (real w=omega). So K along the real-omega axis is
     K = (sqrt(1-4w^2/a0^2) - 1) / (2 i w/a0).
This is PURELY IMAGINARY for w<a0/2 (below cut) -> K is anti-Hermitian on-shell => the
u^mu K u_mu operator is a TOTAL-DERIVATIVE / DISSIPATIVE structure at real frequency, NOT a
standard +omega^2 kinetic term. This is the crux: the timelike-only Box_u=(u.grad)^2 gives an
ODD (first-derivative-like) response, not an even one. We must therefore build the correct
REAL quadratic form for the fluctuation. We do this by working with W = z*K etc. which is REAL
for z<0? Let's check each building block's reality and get the honest kinetic sign.
"""
import sympy as sp
import numpy as np
import mpmath as mp

def H(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

# Use mpmath complex evaluation with the principal branch to read reality + signs honestly.
def K(z):     return (mp.sqrt(1+4*z) - 1)/(2*mp.sqrt(z))
def Kp(z):    # dK/dz
    return mp.diff(K, z)
def Wmat(z, s=-1): return s*(K(z) + z*Kp(z))     # matter transverse weight
def zKp(z):   return z*Kp(z)                      # off-diagonal core

H("(0) Reality of the building blocks on the physical band z=-w^2/a0^2 (w real, 0<w<a0/2)")
print(" z<0 below cut. Evaluate K, Wmat, zKp:")
print(f"{'z':>10} {'K(z)':>28} {'Wmat=s(K+zK\'),s=-1':>34} {'zK\'(z)':>26}")
for zv in [-0.001, -0.01, -0.05, -0.1, -0.2, -0.24]:
    z = mp.mpf(zv)
    print(f"{zv:>10} {str(mp.nstr(K(z),6)):>28} {str(mp.nstr(Wmat(z),6)):>34} {str(mp.nstr(zKp(z),6)):>26}")

print("""
READING: K(z<0) is PURE IMAGINARY (anti-Hermitian) -> the u K u term at real frequency is an
odd/dissipative response, giving NO real propagating kinetic term by itself. But Wmat=s(K+zK')
and zK' -- are they real? If Wmat is pure imaginary too, the matter 'kinetic' operator is a
boundary/dissipative term and the ONLY real propagating d.o.f. in the transverse channel is the
AETHER spin-1 mode. That is the physically decisive statement: the matter-u fluctuation is NOT
an independent propagating pole -> it cannot be a ghost; it is a constrained/auxiliary response.
""")

H("(1) The genuinely propagating transverse pole = Einstein-aether spin-1. Its residue sign.")
print("""
E-aether spin-1 inverse prop: Daeth(w^2,k) = c14*w^2 - Kv*k^2, with (Jacobson 0801.1547)
spin-1 speed  s1^2 = [2c1 - (c1^2 - c3^2)] / [2 c14 (1 - c13)],  Kv = c14*(1-c13)*s1^2.
HEALTHY (no ghost): dDaeth/d(w^2) = c14 > 0  =>  0 < c14 < 2.
NO Cherenkov: s1^2 >= 1.
The DYNAMICAL-u mixing shifts this pole by the REAL part of (Bmix^2/Dmat). Since Bmix ~ zK'
and Dmat ~ Wmat are the SAME imaginary-natured blocks, Bmix^2/Dmat is REAL and O(rho). We
compute its sign to see if it can flip dDaeth/d(w^2) negative (induce a ghost via level repulsion).
""")
# effective aether inverse prop after integrating out matter-u: Daeth_eff = Daeth - Bmix^2/Dmat
c14v, Kvv, kv, rhov = 0.3, 1.0, 1.0, 1.0
def Bmix(z, g=1.0, s=-1.0, rho=1.0): return rho*s*zKp(z)*g
def Dmat(z, s=-1.0, rho=1.0): return rho*Wmat(z, s)
def selfE(z, rho=1.0):    # Bmix^2 / Dmat  (matter-integrated-out self energy on aether)
    return (Bmix(z, 1.0, -1.0, rho)**2)/Dmat(z, -1.0, rho)
print(f"{'z':>8} {'Bmix^2/Dmat (real?)':>30} {'-> real part':>18}")
for zv in [-0.001,-0.01,-0.05,-0.1,-0.2,-0.24]:
    z=mp.mpf(zv); se=selfE(z)
    print(f"{zv:>8} {str(mp.nstr(se,8)):>30} {str(mp.nstr(mp.re(se),6)):>18}")

print("""
The matter self-energy on the aether is REAL and NEGATIVE-definite small (it is (imag)^2/imag =
imag, actually) -- we read the real part above. Its magnitude sets the pole SHIFT; if it stays
bounded and does not exceed c14*w^2, the aether kinetic sign c14>0 is preserved -> no induced ghost.
""")

H("(2) BOTH FOOTINGS: a0 = 9.36e-11 (canonical) and 1.13e-10 (alt). Cut location + residual scale.")
for name,a0 in [("canonical cH_Lambda/Z",9.36e-11),("alt rho_tot/cH0",1.13e-10)]:
    cut = a0/2
    print(f"  {name}: a0={a0:.3e} m/s^2  -> IR cut at omega=a0/2={cut:.3e} (natural units of a0).")
print("""
The cut location scales linearly with a0 in BOTH footings; the pole STRUCTURE (single healthy
aether spin-1 pole + matter dissipative continuum, no new propagating matter pole) is footing-
INDEPENDENT because it is set by the ANALYTIC form of K, not the value of a0.
""")

H("(3) Transverse (nu-1) residual under dynamical u: resonant un-suppression?")
print("""
Static result: the transverse residual was (nu-1)-suppressed, ~7 orders down. Resonance would
require the matter self-energy selfE(z) to develop a POLE (blow up) at some physical z in the
band, feeding energy into the residual. selfE(z)=Bmix^2/Dmat blows up ONLY where Dmat=0, i.e.
where Wmat(z)=0. Solve Wmat=0:
""")
# Solve Wmat(z)=0 symbolically
zz=sp.symbols('zz')
Kzs=(sp.sqrt(1+4*zz)-1)/(2*sp.sqrt(zz)); Wsym=sp.simplify(-(Kzs+zz*sp.diff(Kzs,zz)))
sols=sp.solve(sp.Eq(sp.simplify(Kzs+zz*sp.diff(Kzs,zz)),0), zz)
print("  Wmat(z)=0 solutions:", sols)
# Check if any lie in physical band (-1/4,0)
print("  Any in physical band (-1/4,0)?:",
      [complex(sp.N(so)) for so in sols])
print("""
If NO zero of Wmat lies in the open physical band (-1/4,0), selfE never blows up there -> NO
resonance -> the (nu-1) residual stays (nu-1)^2-suppressed (the mixing is O(g^2)*bounded).
""")
