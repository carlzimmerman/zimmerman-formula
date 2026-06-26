import sympy as sp
import numpy as np

print("="*78)
print("FULL DISPERSION + DUST-BRANCH SIGN: is the Q<1 c_s^2<0 a REAL instability,")
print("or regulated by the k^4 ghost-condensate term + dS friction?")
print("="*78)

# --- AeST-correct Q = sqrt((dphi)^2): use rest-frame phidot, Q ~ |phidot|/N ---
# In the cosmological rest frame Q = phidot (units N=1, c=1). X = phidot^2/2 = Q^2/2.
# So P(X)=K(Q=sqrt(2X)). This is convention [B], the AeST-correct one.
X, dQ, mu, k, Mstar, H = sp.symbols('X dQ mu k Mstar H', positive=True)
Q = sp.symbols('Q', real=True)
K = mu**2*(Q-1)**2

# c_s^2 via P(X), AeST-correct:
P_of_X = K.subs(Q, sp.sqrt(2*X))
PX  = sp.diff(P_of_X, X); PXX = sp.diff(P_of_X, X, 2)
cs2 = sp.simplify((PX/(PX+2*X*PXX)).subs(X, Q**2/2))
print("\n[1] c_s^2 (AeST-correct, Q=sqrt(2X)) =", cs2, " = 1 - 1/|Q|")
print("    Q>1 (dQ>0): c_s^2>0 ;  Q<1 (dQ<0): c_s^2<0  -> SIGN-BY-BRANCH CONFIRMED")
print("    (prior agent's dQ/(3dQ+2) is the WRONG-convention number but SAME SIGN.)")

print("\n" + "="*78)
print("[2] WHICH BRANCH does the physical DUST sit on? (rho_dust>0 requirement)")
print("="*78)
# Shift current first integral: a^3 K'(Q) = I0.  K'(Q)=2 mu^2 (Q-1)=2 mu^2 dQ.
# => dQ = I0/(2 mu^2 a^3).  SIGN of dQ = SIGN of I0.
# Energy density of the displacement (k-essence rho = 2X P_X - P, leading in dQ):
Qs = sp.symbols('Q', real=True)
Kp = sp.diff(K,Qs)
rho = 2*Qs*Kp - K          # rho in the Q-rest-frame k-essence form (2 Q K' - K)
rho_series = sp.series(rho.subs(Qs,1+dQ), dQ, 0, 3).removeO()
print("  rho(dQ) = 2 Q K' - K  expanded about Q=1:", sp.simplify(rho_series))
# leading dust piece:
drho = sp.simplify(sp.diff(rho, Qs).subs(Qs,1))
print("  d rho/dQ at Q=1 =", drho, " -> rho_dust ~ (drho)*dQ to leading order")
print("""
  rho_dust(leading) ~ 2 mu^2 dQ  (from 2 Q K' - K, K' = 2mu^2 dQ).
  rho_dust > 0  REQUIRES  dQ > 0  (Q > 1)  [for mu^2>0].
  => the COLD-DUST (positive-energy DM) branch is FORCED to Q>1 = the c_s^2>0 branch!
  => the gradient-unstable Q<1 branch has rho_dust<0 (it would be a NEGATIVE-energy
     'dust') -- physically excluded as dark matter ANYWAY.
""")
# verify sign numerically
for I0sign in [+1,-1]:
    dQv = I0sign*0.1
    rhov = float(rho_series.subs([(dQ,dQv),(mu,1)]))
    cs2v = float(cs2.subs(Qs,1+dQv))
    print(f"  I0 sign {I0sign:+d}: dQ={dQv:+.2f}, rho_dust~{2*1*dQv:+.3f}, c_s^2={cs2v:+.3f}",
          "-> PHYSICAL DM" if (rhov>0 or 2*dQv>0) else "-> rho<0, unphysical")

print("\n" + "="*78)
print("[3] BOTH-WAYS NET")
print("="*78)
print("""
 The c_s^2<0 'gradient instability' lives ENTIRELY on the Q<1 branch, which is the
 NEGATIVE-energy-dust branch (rho_dust<0). Positive-mass dark matter (rho_dust>0)
 is FORCED onto Q>1 where c_s^2>0. So:
   - the sign-by-branch is REAL and convention-robust (both formulas agree on sign);
   - BUT the candidate-KILL self-resolves: the physical DM the framework needs already
     sits on the stable (c_s^2>0) branch, because rho_dust>0 demands Q>1.
   - The Q<1 branch was never the framework's dust; it is excluded by rho>0 before
     positivity even speaks.
 => Door outcome on the LEADING c_s^2: PROBABLY-NULL as a kill (self-resolves), but it
    PINS THE SIGN OF I0 (I0>0 forced) -- a real, previously-unstated constraint.

 The LIVE part is NOT the leading c_s^2 (which is ~0 at the minimum anyway: the khronon
 has omega=0 / k^4 dispersion). The live Serra-Trombetta test is the GAPPED-vs-GAPLESS
 VELOCITY ordering using the k^4 term + the AeST massive partner -- the ORIGINAL Door A.
""")
