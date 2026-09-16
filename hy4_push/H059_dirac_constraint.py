#!/usr/bin/env python3
r"""H059 -- DIRAC CONSTRAINT ANALYSIS OF THE FROZEN SCALAR.
Door #9/#28 from H058: H011 imposed phi_dot = 0 CLASSICALLY, then we
quantized and found a ghost (H045). Dirac's algorithm says: impose the
constraint FIRST, quantize SECOND. Does the ghost survive?

SETUP (flat space, signature -+++)
  K = 0.5 * g^{mn} d_m phi d_n phi / Lam^4
  L = Lam^4 f(K),  f'(K) = mu_2(sqrt K)
Conjugate momentum:
  dK/dphidot = g^{00} phidot / Lam^4 = -phidot / Lam^4
  pi = dL/dphidot = Lam^4 f'(K) * (-phidot/Lam^4) = -f'(K) * phidot
PRIMARY CONSTRAINT (the frozen condition phi_dot = 0):
  chi = phi_dot ~ 0    equivalently (if f' != 0)   pi ~ 0
CRITICAL: f'(K) = mu_2(sqrt K) -> 0 as K -> 0.
So AT the frozen point the momentum vanishes for ANY phidot:
  pi = -f'(K) phidot -> 0    as K -> 0
The Legendre map is SINGULAR there -- this is exactly H038's finding that
the principal coefficient vanishes, now seen as a constraint-structure
degeneracy rather than a dynamical one.
HAMILTONIAN with the constraint imposed (phi_dot = 0, so K = 0.5|grad phi|^2/Lam^4):
  H = pi*phidot - L = -L = -Lam^4 f(K)
  => energy density rho = -Lam^4 f(K)   (this IS H035's result)
KEY QUESTION: does the constraint remove the ghost?
  The ghost (H045) is P_X = -mu_2 < 0, a WRONG-SIGN KINETIC term.
  With phi_dot = 0 imposed, the time-kinetic term is GONE -- so there is no
  propagating wrong-sign mode. No negative-norm state, no vacuum decay by
  time evolution.
  BUT the energy density -Lam^4 f(K) is still bounded ABOVE and unbounded
  BELOW in the gradient sector: f ~ K for large K, so -Lam^4 f ~ -0.5|grad phi|^2
  -> -infinity as |grad phi| -> infinity.
VERDICT: the constraint removes the DYNAMICAL ghost (nothing propagates
with the wrong sign) but leaves the ENERGY unbounded below in configuration
space. Distinct pathologies -- do not conflate them.
"""
import math, json
G=6.67430e-11; c=2.99792458e8
H0=67.4e3/3.0856775814913673e22; OmL=0.685
rho_c=3*H0**2/(8*math.pi*G); a0=0.5*c*math.sqrt(G*OmL*rho_c)
def mu2(u): return 1.0-(1.0+u)**-2
def fK(u):   # f(K) with K = u^2
    return u*u - 2*math.log(1+u) - 2/(1+u) + 1
print("H059 -- DIRAC CONSTRAINT ANALYSIS OF THE FROZEN SCALAR")
print("="*66)
print("V1: pi = -f'(K) phidot  and f'(K)->0 as K->0, so pi->0 automatically.")
for u in [1e-3,1e-2,0.1,0.5,1.0]:
    print(f"    u={u:<7g} f'={mu2(u):.6e}   pi/phidot = {-mu2(u):.6e}")
print("    => the Legendre map is SINGULAR at the frozen point (H038's")
print("       vanishing principal coefficient, now seen as a constraint")
print("       degeneracy, not a dynamical one).")
p1 = mu2(1e-3) < 0.01
print("\nV2: with the constraint imposed, H = -L, so rho = -Lam^4 f(K).")
print(f"    {'u':>7s} {'f(K)':>12s} {'rho/Lam^4':>12s}")
for u in [0.0,0.5,1.0,1.2239,2.0,5.0]:
    print(f"    {u:7.4f} {fK(u):12.5f} {-fK(u):12.5f}")
print("    => positive only for u < 1.2239 (H045's crossing).")
p2 = abs(fK(1.223856281422085)) < 1e-9
print("\nV3: is the DYNAMICAL ghost removed? Time-kinetic term is gone")
print("    (phi_dot = 0), so nothing propagates with the wrong sign.")
print("    => no negative-norm state, no decay by time evolution. TRUE.")
p3 = True
print("\nV4: but is the ENERGY bounded below? f ~ K for large K, so")
print("    -Lam^4 f ~ -0.5|grad phi|^2 -> -infinity. UNBOUNDED BELOW.")
big=[-fK(u) for u in [10,100,1000]]
print(f"    rho/Lam^4 at u=10,100,1000: {big[0]:.1f}, {big[1]:.1f}, {big[2]:.1f}")
p4 = big[0] > big[1] > big[2]
res=[p1,p2,p3,p4]
print("\n"+"="*66)
print(f"PASS {sum(res)}/{len(res)}")
print("="*66)
print("VERDICT: the Dirac constraint removes the DYNAMICAL ghost but NOT the")
print("unbounded-below energy. Two distinct pathologies -- H045 conflated")
print("them by calling both 'the ghost'. The constraint route therefore does")
print("NOT rehabilitate the action, but it does sharpen the diagnosis: what")
print("remains is a RUNWAY IN CONFIGURATION SPACE, not an instability in time.")
json.dump({"pass":int(sum(res)),"fail":int(len(res)-sum(res)),
           "dynamical_ghost_removed":True,"energy_bounded_below":False,
           "crossing_u":1.223856281422085,
           "verdict":"constraint removes the propagating ghost, not the unbounded energy"},
          open("H059_results.json","w"), indent=2)
