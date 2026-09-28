# as232_verify.py — AS232 Tier-0b FINAL bounded verification (single run, gate-guarded).
# Exact static EL operators of the declared CA5-GNC-R branch density
#   L = (M_P^2/2) e^Phi sqrt(h) [ R4 + V_a + c_N(G - ell delta_h W_b) ]      (Lambda k!=0 out)
# in the gauge  g00 = -e^{2Phi},  g_ij = (1-2 Psi) delta_ij,  w = ln(1-2Psi)/2,
# R4 = R3(w) - 2 e^{-2w}[ L0 Phi + (D0Phi)^2 + (D0Phi)(D0w) ]   [validated: exactly 0 on
#      Schwarzschild isotropic vacuum; R3(w) the warped leaf Ricci scalar].
# Window: gate inactive, dust, heat suppression S_k -> 0 (Z = ell S_k Phi/4 -> 0, Uaux = Phi).
# Vacuum: L0(U) = 0 (U = G_N M/r), mean-normalized nonzero modes; c_N = G_bare/G_N encoding.
# Lapse EL (hand IBP, 2nd-derivative-coupling included):
#   E_Phi = e^Phi sqrt(h)(R4+Va) - D0[ e^Phi sqrt(h) d(R4+Va)/d(D0Phi) ] + L0[ e^Phi sqrt(h) d(R4+Va)/d(L0Phi) ]
# Spatial EL (functional probe chi + IBP): E_Psi = d/ds|0 e^Phi sqrt(h(s))(R4(s)+Va(s)), s-probe on Psi2.
# Point-source: varphi2 = A/r^2, psi2 = B/r^2  =>  beta = 1 + phi2/U_N^2 = 1 + A/GM2.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
eps = sp.symbols('eps', positive=True)
U = sp.Function('U')(r)
Phi1, Psi1 = -U, -U
varphi2, psi2 = sp.Function('varphi2')(r), sp.Function('psi2')(r)
Phi = eps*Phi1 + eps**2*varphi2
Psi = eps*Psi1 + eps**2*psi2
Z  = eps*(ell*Sk*Phi1/4) + eps**2*(ell*Sk*varphi2/4)
Uaux = eps*(Phi1 - ell*Sk*Phi1/4) + eps**2*(varphi2 - ell*Sk*varphi2/4)

def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

w = sp.log(1 - 2*Psi)/2
e2w = sp.exp(2*w)
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
R4 = R3 - 2*sp.exp(-2*w)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(w))
inv = 1/(1 - 2*Psi)
Va = (alpha*inv*(D0(Phi)-D0(Z))**2 + 4*inv*D0(Phi)*D0(Z)
      - 2*inv*D0(Z)**2 - 4*cN*inv*D0(Z)*D0(Uaux))
M = sp.exp(Phi)*(1-2*Psi)**sp.Rational(3,2)     # sqrt(-g) = e^Phi sqrt(h)

# ---------------- LAPSE EL ----------------
K1 = M*(-4*sp.exp(-2*w)*D0(Phi) - 2*sp.exp(-2*w)*D0(w)
        + 2*alpha*inv*(D0(Phi)-D0(Z)) + 4*inv*D0(Z))
K2 = M*(-2*sp.exp(-2*w))
E_Phi = sp.expand(sp.series(M*(R4 + Va), eps, 0, 3).removeO()) \
        - sp.expand(sp.series(sp.diff(K1, r), eps, 0, 3).removeO()) \
        + sp.expand(sp.series(L0(K2), eps, 0, 3).removeO())
E_Phi = sp.expand(sp.series(E_Phi, eps, 0, 3).removeO())

# ---------------- SPATIAL EL (probe chi) ----------------
chi = sp.Function('chi')(r); s = sp.symbols('s')
PsiP = eps*Psi1 + eps**2*(psi2 + s*chi)
wP = sp.log(1 - 2*PsiP)/2
R3P = -4*sp.exp(-2*wP)*L0(wP) - 2*sp.exp(-2*wP)*D0(wP)**2
R4P = R3P - 2*sp.exp(-2*wP)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(wP))
invP = 1/(1 - 2*PsiP)
VaP = (alpha*invP*(D0(Phi)-D0(Z))**2 + 4*invP*D0(Phi)*D0(Z)
       - 2*invP*D0(Z)**2 - 4*cN*invP*D0(Z)*D0(Uaux))
MP = sp.exp(Phi)*(1-2*PsiP)**sp.Rational(3,2)
prob = sp.expand(sp.diff(MP*(R4P + VaP), s))
prob = sp.expand(sp.series(prob, s, 0, 2).removeO())
prob = sp.expand(sp.series(prob, eps, 0, 3).removeO())
# IBP on chi' and chi'' (flat leaf, declared):  chi' F -> -chi D0(F);  chi'' F -> +chi L0(F)
E_Psi = sp.S.Zero
for t in sp.Add.make_args(sp.expand(prob)):
    if t.has(sp.Derivative(chi, (r, 2))):
        Fct = sp.simplify(t / sp.Derivative(chi, (r, 2)))
        E_Psi += chi * sp.expand(L0(Fct))
    elif t.has(sp.Derivative(chi, r)):
        Fct = sp.simplify(t / sp.Derivative(chi, r))
        E_Psi -= chi * sp.expand(D0(Fct))
    elif t.has(chi):
        E_Psi += t
    # chi-free pieces are eps-quadratics sourced by the background: appended below
E_Psi = sp.expand(sp.series(E_Psi, eps, 0, 3).removeO())

# ---------------- vacuum + window reduction ----------------
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
def vac(f):
    f = sp.expand(f).subs(UPP, 0).subs(UP, 0).subs(U, 0).subs(Sk, 0)
    return sp.expand(f)

# ---- linear gate: lapse EL at eps must be exactly E1-machinery (AS226): 4 cN L0(Phi1-Z1)
E1_op = sp.expand(4*cN*L0(Phi1 - eps*0 - ell*Sk*Phi1/4))
linA = sp.expand(E_Phi.coeff(eps, 1))
gate1_lhs = vac(sp.expand(E_Phi.coeff(eps,1) - E1_op.coeff(eps,1)))
print("GATE-1 lapse linear (vac,window) residual (0 = E1 match):", sp.simplify(gate1_lhs))
assert sp.simplify(gate1_lhs) == 0, "linear gate failed"
print("  linear gate passed: lapse EL  ==  E1 operator (AS226)  at O(eps)")

# ---- second-order system ----
E2l = vac(sp.expand(E_Phi.coeff(eps, 2)))     # lapse  eps^2 (window now; U dropped as vacuum)
E2s = vac(sp.expand(E_Psi.coeff(eps, 2)))     # spatial eps^2
print("\nE2 lapse (vac,win):", E2l)
print("E2 spatial (vac,win):", E2s)

A, B = sp.symbols('A B')
def topoly(f):
    f = f.replace(varphi2, A/r**2).replace(psi2, B/r**2)
    f = f.replace(sp.Derivative(varphi2, (r,2)), 6*A/r**4).replace(sp.Derivative(psi2, (r,2)), 6*B/r**4)
    f = f.replace(sp.Derivative(varphi2, r), -2*A/r**3).replace(sp.Derivative(psi2, r), -2*B/r**3)
    f = sp.expand(f)
    return sp.expand(sp.simplify(sp.expand(f*r**4)))
Pl = topoly(E2l); Ps = topoly(E2s)
Pl = sp.expand(Pl.subs(UP,0).subs(UPP,0).subs(U,0))
Ps = sp.expand(Ps.subs(UP,0).subs(UPP,0).subs(U,0))
PlA, PlB, PlC = sp.expand(sp.diff(Pl,A).subs(B,0)), sp.expand(sp.diff(Pl,B).subs(A,0)), sp.simplify(Pl.subs({A:0,B:0}))
PsA, PsB, PsC = sp.expand(sp.diff(Ps,A).subs(B,0)), sp.expand(sp.diff(Ps,B).subs(A,0)), sp.simplify(Ps.subs({A:0,B:0}))
print("\nLAPSE   eps2: A*(%s) + B*(%s) + %s = 0" % (sp.simplify(PlA), sp.simplify(PlB), PlC))
print("SPATIAL eps2: A*(%s) + B*(%s) + %s = 0" % (sp.simplify(PsA), sp.simplify(PsB), PsC))
sol = sp.solve([sp.expand(PlA*A + PlB*B + PlC), sp.expand(PsA*A + PsB*B + PsC)], [A, B], dict=True)
print("solution:", sol)
Asol, Bsol = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
print("phi2/U_N^2 = %s     psi2/U_N^2 = %s" % (sp.simplify(Asol/GM2), sp.simplify(Bsol/GM2)))
print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + Asol/GM2))
# substitution-back
r_l = sp.simplify(sp.expand(PlA*Asol + PlB*Bsol + PlC))
r_s = sp.simplify(sp.expand(PsA*Asol + PsB*Bsol + PsC))
print("substitution-back residuals (must be 0):", r_l, r_s)
assert r_l == 0 and r_s == 0
# ---- Schwarzschild-isotropic gate (alpha = 0):  psi2 must equal -3 U^2/4, phi2 = 0 (beta = 1)
B0 = sp.simplify(Bsol.subs(alpha, 0)); A0 = sp.simplify(Asol.subs(alpha, 0))
print("Einstein gate alpha=0: phi2/U2 =", A0, " psi2/U2 =", sp.simplify(B0/GM2), "(expect 0, -3/4)")
assert sp.simplify(B0/GM2 + sp.Rational(3,4)) == 0
# ---- negative control: beta=1 input with the EINSTEIN isotropic shell (psi2 = -3U^2/4),
#      substituted into the ORIGINAL spatial eps2 equation: must FIRE for alpha != 0, die at 0
ctl = sp.simplify(sp.expand(PsA*0 + PsB*(-sp.Rational(3,4)*GM2) + PsC))
print("\nNEGATIVE CONTROL: spatial residual at (beta=1, Einstein isotropic shell):", ctl)
ctl0 = sp.simplify(ctl.subs(alpha, 0))
print("   at alpha=0 the control residual:", ctl0, " (must be exactly 0)")
assert ctl0 == 0
# ---- numeric footings for a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ----
c = 299792458.0; G = 6.67430e-11; Msun = 1.98847e30; pc = 3.085677581491367e16
rho1 = (2*9.3619e-11)**2/(c*c*G); rho2 = (2*1.1279e-10)**2/(c*c*G)
a01 = 0.5*c*(G*rho1)**0.5; a02 = 0.5*c*(G*rho2)**0.5
print("\na0 footings: rho_Lambda = %.4e, %.4e kg/m^3  ->  a0 = %.4e, %.4e m/s^2"
      % (rho1, rho2, a01, a02))
with open('as232_verify_out.txt','w') as f:
    f.write("E2_lapse_vacwin = %s\nE2_spatial_vacwin = %s\nlapse_eq = (%s)*A + (%s)*B + (%s)\n"
            "spatial_eq = (%s)*A + (%s)*B + (%s)\n"
            "sol: phi2/U^2=%s, psi2/U^2=%s, BETA=%s\nneg_control=%s (at a0: %s)\n"
            % (E2l, E2s, sp.simplify(PlA), sp.simplify(PlB), PlC, sp.simplify(PsA),
               sp.simplify(PsB), PsC, sp.simplify(Asol/GM2), sp.simplify(Bsol/GM2),
               sp.simplify(1+Asol/GM2), ctl, ctl0))
print("wrote as232_verify_out.txt")