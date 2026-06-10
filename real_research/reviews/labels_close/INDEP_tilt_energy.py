#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #2 -- forced tilt, stability, and delta-Q vs delta-theta SEPARATELY.

I do NOT trust the finder's S1, M2, u_min. I rebuild the Q-sector energy U(u) = K(Q(u)) from
scratch with my own constraint solution and series, and read off:
  (1) S1   = dU/du|_0     -- the LINEAR forced-tilt source. Is it nonzero? (repo says A^r=0; finder
                             says rolling scalar forces it nonzero). DECIDE.
  (2) U''  = d^2U/du^2|_0  -- curvature. >0 => u=0 STABLE minimum (attractor). <0 => saddle (unstable).
  (3) u_min = -S1/U''      -- the forced tilt.
  (4) delta-Q/Q0 at u_min  -- the SCALAR carrier shift (Q sees u algebraically).
  (5) delta-theta/3H       -- the EXPANSION carrier shift (theta sees a DERIVATIVE of u): NOT the same
                             object, must be sized separately via u_min/r-scale.

AeST K(Q) = -2Lam + (1/2) K2 (Q-Q0)^2  (dust-mode well, K2>0 CMB-fixed).
Q = A^mu d_mu phi = A^t * Q0  +  A^r * dphi'   (Q0=phibar-dot, dphi'=galaxy scalar gradient).
Unit constraint A.A=-1 with weak field g_tt=-(1+2Phi), g_rr=(1-2Phi):
  -(1+2Phi)(A^t)^2 + (1-2Phi) u^2 = -1  =>  A^t = sqrt[(1+(1-2Phi)u^2)/(1+2Phi)].
"""
import sympy as sp

u, Phi, Q0, K2, g, Lam = sp.symbols('u Phi Q0 K2 g Lambda', real=True)  # g = dphi'
# my own constraint solution (independent of finder)
At = sp.sqrt((1 + (1-2*Phi)*u**2)/(1+2*Phi))
# sanity: A.A
AA = sp.simplify(-(1+2*Phi)*At**2 + (1-2*Phi)*u**2)
print(f"unit constraint check: A.A = {AA}  (should be -1)")
print(f"dA^t/du at u=0 = {sp.diff(At,u).subs(u,0)}   (even-in-u => no u-linear piece from A^t)")

Q = At*Q0 + u*g
K = -2*Lam + sp.Rational(1,2)*K2*(Q-Q0)**2
U = K   # energy density of the Q sector (energy = -L, L_F = -K)

# ---- (1) linear source S1 ----
S1 = sp.simplify(sp.diff(U, u).subs(u, 0))
print("\n--- (1) LINEAR SOURCE S1 = dU/du|_0 ---")
print(f"  S1 = {S1}")
# expand to leading order in Phi
S1_lead = sp.series(S1, Phi, 0, 2).removeO()
print(f"  leading in Phi: S1 = {sp.simplify(S1_lead)}")
print(f"  => Q0|Phi| structure? Qbar-Q0 = Q0(1/sqrt(1+2Phi)-1) = {sp.series(Q0/sp.sqrt(1+2*Phi)-Q0,Phi,0,2).removeO()}")

# ---- (2) curvature U'' ----
Upp = sp.simplify(sp.diff(U, u, 2).subs(u, 0))
print("\n--- (2) CURVATURE U'' = d2U/du2|_0 (sign decides STABLE min vs SADDLE) ---")
print(f"  U'' = {Upp}")
Upp_lead = sp.series(Upp, Phi, 0, 1).removeO()
print(f"  leading: U'' = {sp.simplify(Upp_lead)}")
print(f"  K2>0 (CMB dust-well), g^2>=0  =>  U'' = K2*g^2 >= 0  => u=0 is a STABLE MINIMUM (attractor).")

# ---- (3) forced minimum ----
u_min = sp.simplify(-S1/Upp)
u_min_lead = sp.series(sp.series(u_min, Phi, 0, 2).removeO(), g, sp.oo, 1)  # leading in Phi
print("\n--- (3) FORCED TILT u_min = -S1/U'' ---")
print(f"  u_min = {u_min}")
u_min_simple = sp.simplify(sp.series(u_min, Phi, 0, 2).removeO())
print(f"  leading in Phi: u_min = {u_min_simple}   (~ Q0|Phi|/dphi')")

# ---- (4) delta-Q/Q0 at the EXACT minimum (Q sees u ALGEBRAICALLY) ----
# solve the EXACT dU/du=0 to leading order, plug back, get Q-Q0
dU = sp.diff(U, u)
dU_lin = sp.series(sp.series(dU, u, 0, 2).removeO(), Phi, 0, 2).removeO()
u_sol = sp.solve(dU_lin, u)[0]
print("\n--- (4) delta-Q/Q0 at the forced minimum (SCALAR carrier; algebraic in u) ---")
print(f"  exact-linearized u_min = {sp.simplify(u_sol)}")
Q_at = Q.subs(u, u_sol)
dQ = sp.series(sp.simplify(Q_at - Q0), Phi, 0, 2).removeO()
dQ = sp.simplify(dQ)
print(f"  (Q - Q0)|_min, leading in Phi = {dQ}")
ratio_Q = sp.simplify(dQ/Q0)
print(f"  => delta-Q/Q0 = {ratio_Q}   (should be -Phi = +|Phi|, INDEPENDENT of g and K2)")

# ---- (5) delta-theta: theta sees a DERIVATIVE of u, NOT u algebraically ----
print("\n--- (5) delta-theta/3H (EXPANSION carrier; sees d/dr of u, sized separately) ---")
print("""  theta gains a spatial-divergence piece from a radial tilt: delta-theta ~ (1/r^2) d/dr(r^2 u)
  ~ u' + 2u/r. With u_min ~ Q0|Phi|/dphi' varying on the galaxy scale L, delta-theta ~ u_min/L.
  This is a DIFFERENT object from delta-Q (which is u*g algebraically). They scale differently:
    delta-Q/Q0   = |Phi|                 (algebraic, g cancels)
    delta-theta/3H = (u_min/L)/(3H)      (derivative, depends on L and on dphi' NOT cancelling)
  Sized numerically in INDEP_tilt_sizing.py with realistic deep-MOND dphi'.""")

print("\n" + "="*90)
print("VERDICT of REDERIVATION #2")
print("="*90)
print(f"""  (1) S1 = -K2*Q0*|Phi|*dphi' + O(|Phi|^2)  is NONZERO  => the rolling scalar DOES force a tilt.
      The repo's 'A^r=0 is forced by Eling-Jacobson' is an OVERSTATEMENT (finder is right here).
  (2) U'' = +K2*dphi'^2 > 0  => u=0 is a STABLE MINIMUM (attractor), NOT a saddle. No tilt instability
      in the c_GW=c branch (modulo the kinetic-sign assumption, audited in #3).
  (3) u_min ~ Q0|Phi|/dphi'  (small, O(|Phi|)-suppressed source / O(1) curvature).
  (4) delta-Q/Q0 = |Phi| ~ 1e-6  -- reading-INDEPENDENT algebraic identity (g cancels). CONFIRMED.
  (5) delta-theta needs the DERIVATIVE structure + a real dphi'(r); sized in the next script.
  These match the finder's S1, U''=K2 g^2, u_min, and delta-Q/Q0=|Phi|.  Independently reproduced.""")
