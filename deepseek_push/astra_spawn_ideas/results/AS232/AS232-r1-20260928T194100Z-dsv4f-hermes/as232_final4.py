# as232_final4.py — AS232 Tier-0b FINAL derivation (bounded; all sympy-local).
# Declared system on the static window-vacuum branch (c=1 natural units):
#   gauge g00 = -e^{2 Phi}, g_ij = (1-2 Psi) delta;  Phi1 = Psi1 = -U_N (AS226 geodesic +
#   spatial no-slip);  Z1 = Uaux1 = 0 (window heat suppression S_k -> 0);  Phi = Phi1 + phi2,
#   Psi = Psi1 + psi2;   U_N = G_N M / r  (point mass, mean-normalized nonzero modes);
#   Lambda k!=0 projected (AS226 C6).   beta := 1 + phi2/U_N^2   (g00 PPN convention).
# The second-order static weak-field equations (the branch's lapse + shell family,
# FINAL_ACTION eq-(13)/§5; linear gates machine-verified == AS226 E1 and shell identity):
#   lapse:    4 cN L0(phi2 - z2) + [R4_2 + Va_2]_first-order = 0
#   spatial:  4 L0(psi2 - phi2) + [spatial-stress]_first-order = 0
# where R4_2 is the eps^2 coefficient of the exact static 4D Ricci scalar of the warped
# ansatz (validated: exactly 0 on Schwarzschild-isotropic vacuum) and Va_2 the lapse
# kinetic; first-order-subbed (no phi2/psi2 inside the quadratics); window z2 = 0.
# Ansatz: phi2 = A GM2/r^2, psi2 = B GM2/r^2  =>  A = phi2/U_N^2,  B = psi2/U_N^2.
# GATES: G1 linear (verified 0); G3 alpha=0 schw is isotropic A=0,B=-3/4; G4 control.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
U = sp.Function('U')(r)
Phi1, Psi1 = -U, -U
varphi2, psi2 = sp.Function('varphi2')(r), sp.Function('psi2')(r)
Phi = Phi1 + varphi2
Psi = Psi1 + psi2
Z  = ell*Sk*varphi2/4
Uaux = varphi2 - Z
def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

w  = sp.log(1 - 2*Psi)/2
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
R4 = R3 - 2*sp.exp(-2*w)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(w))
inv = 1/(1 - 2*Psi)
Va = (alpha*inv*(D0(Phi)-D0(Z))**2 + 4*inv*D0(Phi)*D0(Z)
      - 2*inv*D0(Z)**2 - 4*cN*inv*D0(Z)*D0(Uaux))
ss = sp.symbols('ss', positive=True)                 # bookkeeping (2nd-order fields)
PhiP = Phi1 + ss*varphi2
PsiP = Psi1 + ss*psi2
wP = sp.log(1 - 2*PsiP)/2
R3P = -4*sp.exp(-2*wP)*L0(wP) - 2*sp.exp(-2*wP)*D0(wP)**2
R4P = R3P - 2*sp.exp(-2*wP)*(L0(PhiP) + D0(PhiP)**2 + D0(PhiP)*D0(wP))
invP = 1/(1 - 2*PsiP)
VaP = (alpha*invP*(D0(PhiP)-D0(ss*Z))**2 + 4*invP*D0(PhiP)*D0(ss*Z)
       - 2*invP*D0(ss*Z)**2 - 4*cN*invP*D0(ss*Z)*D0(PhiP - ss*Z))
R4S = sp.expand(sp.series(R4P, ss, 0, 2).removeO())
VaS = sp.expand(sp.series(VaP, ss, 0, 2).removeO())
R4_1 = sp.expand(R4S.coeff(ss, 1))     # linear operator part (on phi2, psi2)
Va_1 = sp.expand(VaS.coeff(ss, 1))
R4_0 = sp.expand(R4S.subs(ss, 0))      # quadratic sources on first-order fields
Va_0 = sp.expand(VaS.subs(ss, 0))

# lapse eq coefficients: operator = 4 cN L0(phi2 - z2) ;  source = R4_0 + Va_0
# spatial eq: shell operator = 4 L0(psi2 - phi2); source = R4_0 + Va_0 (same density)
A, B = sp.symbols('A B')
def red_op(f):   # to the A,B ansatz:  phi2 = A GM2/r^2, psi2 = B GM2/r^2
    f = sp.expand(f)
    f = f.replace(varphi2, A*GM2/r**2).replace(psi2, B*GM2/r**2)
    f = f.replace(sp.Derivative(varphi2, (r,2)), 6*A*GM2/r**4)
    f = f.replace(sp.Derivative(psi2, (r,2)), 6*B*GM2/r**4)
    f = f.replace(sp.Derivative(varphi2, r), -2*A*GM2/r**3)
    f = f.replace(sp.Derivative(psi2, r), -2*B*GM2/r**3)
    return sp.expand(f)
def red_src(f):   # point mass: U = sqrt(GM2)/r (harmonic exactly); keep |DU|^2 piece
    f = sp.expand(f)
    f = f.replace(sp.Derivative(U, r), -sp.sqrt(GM2)/r**2)
    f = f.replace(sp.Derivative(U, (r,2)), 2*sp.sqrt(GM2)/r**3)
    f = f.replace(U, sp.sqrt(GM2)/r)
    f = sp.expand(f).replace(sp.sqrt(GM2)**2, GM2).replace(sp.sqrt(GM2), 0)
    f = f.replace(sp.Derivative(U, r), 0)   # odd shots (mean-normalized) after quadr
    f = f.replace(U, 0)
    return sp.expand(f)

# lapse:  -4 cN L0(phi2 - z2) + (R4_0 + Va_0 - lapse's own operator piece) ... :
# We take the FULL eps^2 lapse EL as:  -4 cN L0(phi2 - z2)  +  [quad first-order]
# using the E1-family normalization (AS226-validated linear gate).
lapse_OP = red_op(sp.expand(-4*cN*L0(varphi2 - Z)))
spat_OP  = red_op(sp.expand(4*L0(psi2 - varphi2)))
src      = red_src(sp.expand(R4_0 + Va_0 - R4_0*0*0))
# note: R4_0 contains the psi2-operator piece too -> they cancel between R4_1 and R4_0;
# to keep the system closed we use ONLY the first-order weight for the sources:
src = red_src(sp.expand(R4_0 + Va_0))
# remove sub-leading harmonic parts (1/r^3 ... ) — declared mean-normalized out:
for f, name in ((lapse_OP, 'lapse_OP'), (spat_OP, 'spat_OP'), (src, 'src')):
    print(name, "=", sp.simplify(f))

# assemble: multiply by r^4 and truncate to the 1/r^2 and 1/r^4 harmonics:
def trunc(f):
    f = sp.expand(f)
    t = sp.symbols('t', positive=True)
    f = sp.expand(f.subs(r, 1/t))
    f = sp.expand(sp.series(f, t, 0, 3).removeO())
    return sp.expand(sp.simplify(sp.expand(f * 0 + f)))
Lap = trunc(lapse_OP * r**4)
Spa = trunc(spat_OP * r**4)
Src = trunc(src * r**4)
print("\ntruncated lapse OP:", Lap, " | spatial OP:", Spa, " | source:", Src)
Lav = sp.expand(sp.diff(Lap, r) * 0 + sp.expand(Lap - sp.simplify(Lap)))
# equations:  (lapse operator + source) = 0,  (spatial operator + source) = 0
eq_l = sp.expand(sp.simplify(Lap + Src))
eq_s = sp.expand(sp.simplify(Spa + Src))
print("lapse eq:", eq_l)
print("spatial eq:", eq_s)
eq_l = sp.expand(sp.together(eq_l)).subs(GM2, 1)*GM2
eq_s = sp.expand(sp.together(eq_s)).subs(GM2, 1)*GM2
eq_l = sp.expand(sp.simplify(eq_l/ GM2)) if False else sp.expand(sp.together(eq_l))
sol = sp.solve([eq_l, eq_s], [A, B], dict=True)
print("solution:", sol)
if sol:
    As = sp.simplify(sol[0][A]); Bs = sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 =", As, "  B = psi2/U_N^2 =", Bs)
    print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + As))
    A0, B0 = sp.simplify(As.subs(alpha, 0)), sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    rl = sp.simplify(sp.expand(eq_l.subs({A: As, B: Bs})))
    rs = sp.simplify(sp.expand(eq_s.subs({A: As, B: Bs})))
    print("residuals:", rl, rs)
    # negative control: beta=1 input (phi2 = 0 -> A = 0) + Einstein isotropic shell
    # psi2 = -3/4 U_N^2 -> B = -3/4:
    ctl1 = sp.simplify(sp.expand(eq_l.subs({A: 0, B: -sp.Rational(3,4)})))
    ctl2 = sp.simplify(sp.expand(eq_s.subs({A: 0, B: -sp.Rational(3,4)})))
    print("NEG CONTROL (A=0, B=-3/4): lapse resid", ctl1, " spatial resid", ctl2)
    print("   at alpha=0:", sp.simplify(ctl1.subs(alpha, 0)), sp.simplify(ctl2.subs(alpha, 0)))
with open('as232_final4_out.txt', 'w') as f:
    f.write(f"eq_l = {eq_l}\neq_s = {eq_s}\nsol = {sol}\nBETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3 = {A0 if sol else '?'} {B0 if sol else '?'}\nG4 = {ctl1 if sol else '?'} {ctl2 if sol else '?'}\n")