#!/usr/bin/env python3
r"""
PROBLEM 2 -- PART 4: is A^r=0 a CONSISTENT solution of the A^r EOM, or does the rolling-scalar
cross term FORCE A^r != 0? This is the hinge: if the source vanishes at A^r=0, EJ holds and theta
is pinned; if not, the derived tilt of Part 3 is real and theta is swamped.

We evaluate dL/dA^r AT A^r=0 (the EJ static config). If it is nonzero, A^r=0 is NOT a solution
and the field must tilt to cancel it -> A^r = (that source)/m_A^2. We compute the source = the
A^r-gradient of (-F(Y,Q)) at A^r=0, symbolically, keeping phi=phibar(t)+dphi(r).
"""
import sympy as sp

r = sp.symbols('r', positive=True)
Q0 = sp.symbols('Q_0', real=True)          # phibar-dot (cosmological roll)
Ar = sp.symbols('A_r', real=True)          # the tilt amplitude (we'll set ->0 after differentiating)
Phi = sp.Function('Phi')(r)
varphi = sp.Function('varphi')(r)          # galaxy scalar
vp = sp.diff(varphi, r)

# weak field: g_tt=-(1+2Phi), g_rr=(1-2Phi)~1, A^t from unit constraint
At = sp.sqrt((1 - (1-2*Phi)*Ar**2)/(1+2*Phi))
# Q = A^t Q0 + A^r dphi'
Q = At*Q0 + Ar*vp
# Y = q^{mn} d_m phi d_n phi = g^{mn}d_m phi d_n phi + (A^m d_m phi)^2 = (grad phi)^2_g + Q^2
# (grad phi)^2_g = g^{rr}(dphi/dr)^2 + g^{tt}(dphi/dt)^2 = (1/(1-2Phi))vp^2 - (1/(1+2Phi))Q0^2
gradphi2 = (1/(1-2*Phi))*vp**2 - (1/(1+2*Phi))*Q0**2
Y = gradphi2 + Q**2

# free function derivatives as symbols (evaluated on background)
F_Y, F_Q = sp.symbols('F_Y F_Q', real=True)
# dF/dA^r = F_Y dY/dA^r + F_Q dQ/dA^r
dY_dAr = sp.diff(Y, Ar)
dQ_dAr = sp.diff(Q, Ar)
source = -(F_Y*dY_dAr + F_Q*dQ_dAr)        # the A^r EOM RHS (minus sign from -F in action)

print("="*100)
print("PART 4 -- is A^r=0 a solution? evaluate the source dL/dA^r at A^r=0")
print("="*100)
dQ0 = sp.simplify(dQ_dAr.subs(Ar,0))
dY0 = sp.simplify(dY_dAr.subs(Ar,0))
src0 = sp.simplify(source.subs(Ar,0))
print("  dQ/dA^r |_{A^r=0} =", dQ0)
print("  dY/dA^r |_{A^r=0} =", dY0, "  = 2 Q dQ/dA^r = 2 (A^t Q0) varphi'")
print("  SOURCE dL/dA^r|_{A^r=0} = -(F_Y dY/dA^r + F_Q dQ/dA^r) =")
sp.pprint(src0)
print(f"""
  => dQ/dA^r|_0 = varphi' (the MOND scalar gradient) is NONZERO whenever the galaxy has a scalar
     gradient (i.e. always, in a galaxy). So the source at A^r=0 is:
        dL/dA^r|_0 = -(2 F_Y A^t Q0 + F_Q) varphi'  != 0.
     THEREFORE A^r=0 is NOT a solution of the A^r EOM in AeST-with-rolling-scalar. The aether MUST
     tilt to cancel this source: A^r = (2 F_Y A^t Q0 + F_Q) varphi'/m_A^2 != 0.

  THIS IS THE CORRECTION TO ELING-JACOBSON: EJ is a VACUUM/fluid theorem (no scalar gradient).
  In AeST the rolling scalar's gradient varphi' sources the tilt at A^r=0. The repo's invocation
  of EJ to set A^r=0 EXACTLY is therefore not valid; A^r is small but NONZERO, set by the balance
  above. (It IS valid that the tilt is small -- m_A^2 is large -- but 'small' is the Part-3 number,
  not zero, and theta's 10^5 exposure turns 'small' into an O(1) wobble.)

  CROSS-CHECK -- does the source vanish if varphi'=0 (no galaxy)? src0 with vp->0:""")
print("   ", sp.simplify(src0.subs(vp,0)))
print("""     = 0. GOOD: in an empty universe (no galaxy gradient) A^r=0 IS a solution (EJ recovered).
     The tilt is sourced PRECISELY by the galaxy scalar gradient -- the cross term the prompt flagged.
""")
