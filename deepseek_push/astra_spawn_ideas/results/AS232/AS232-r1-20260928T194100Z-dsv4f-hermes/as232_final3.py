# as232_final3.py — AS232 Tier-0b FINAL.  Exact ε² field equations via action probe with
# CORRECT flat-leaf adjoints w.r.t. the r² dr measure (interior pieces; boundary terms
# are the declared AS143 finite-domain business):
#     chi'' F --> chi * (F'' + 4 F'/r + 2 F/r^2)
#     chi'  F --> -chi * (F' + 2 F/r)
# Lapse EL: hand-IBP family (linear gate verified == AS226 E1).
# Window (S_k -> 0), vacuum, point mass U = sqrt(GM2)/r explicit (rational: no vacuum
# substitution guesses).  Ansatz phi2 = A*U_N^2, psi2 = B*U_N^2 with U_N = U:
# point-harmonic amplitudes: phi2 = A GM2/r^2 etc.  Solve the ε² (1/r^4)-system.
# GATES: G1 linear E1-match; G3 alpha=0 => (A, B) = (0, -3/4) [Einstein isotropic shell,
# pending; if violated the machinery reports the discrepancy honestly]; G4 negative control:
# beta=1 input + Einstein shell at alpha != 0 must fire.
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
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
R4 = R3 - 2*sp.exp(-2*w)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(w))
inv = 1/(1 - 2*Psi)
Va = (alpha*inv*(D0(Phi)-D0(Z))**2 + 4*inv*D0(Phi)*D0(Z)
      - 2*inv*D0(Z)**2 - 4*cN*inv*D0(Z)*D0(Uaux))
M = sp.exp(Phi)*(1-2*Psi)**sp.Rational(3,2)
Dens = M*(R4 + Va)

# ---------- LAPSE EL (hand IBP, verified linear gate) ----------
K1 = M*(-4*sp.exp(-2*w)*D0(Phi) - 2*sp.exp(-2*w)*D0(w)
        + 2*alpha*inv*(D0(Phi)-D0(Z)) + 4*inv*D0(Z))
K2 = M*(-2*sp.exp(-2*w))
E_Phi = sp.expand(sp.series(Dens, eps, 0, 3).removeO()) \
        - sp.expand(sp.series(sp.diff(K1, r), eps, 0, 3).removeO()) \
        + sp.expand(sp.series(L0(K2), eps, 0, 3).removeO())
E_Phi = sp.expand(sp.series(E_Phi, eps, 0, 3).removeO())

# ---------- SPATIAL EL via probe with EXACT flat adjoints (r^2-dr measure) ----------
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
E_Psi = sp.S.Zero
for t in sp.Add.make_args(sp.expand(prob)):
    if t.has(sp.Derivative(chi, (r, 2))):
        Fct = sp.simplify(t / sp.Derivative(chi, (r, 2)))
        E_Psi += chi * sp.expand(sp.diff(Fct, (r, 2)) + 4*sp.diff(Fct, r)/r + 2*Fct/r**2)
    elif t.has(sp.Derivative(chi, r)):
        Fct = sp.simplify(t / sp.Derivative(chi, r))
        E_Psi -= chi * sp.expand(sp.diff(Fct, r) + 2*Fct/r)
    elif t.has(chi):
        E_Psi += t
E_Psi = sp.expand(sp.series(E_Psi, eps, 0, 3).removeO()).subs(chi, 1)

# ---------- linear gate ----------
E1_op = sp.expand(4*cN*L0(Phi1 - ell*Sk*Phi1/4))
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
def linres(f):
    return sp.expand(f.coeff(eps, 1)).subs(Sk, 0).replace(UPP, 0).replace(UP, 0).replace(U, 0)
g1 = sp.simplify(sp.expand(linres(E_Phi) - linres(E1_op)))
print("GATE-1 linear (E_Phi - E1, vac/window):", g1)
assert g1 == 0, "linear gate failed"
g1s = sp.simplify(sp.expand(linres(E_Psi)))
print("GATE-1s spatial linear (vac/window):", g1s, " (0 = shell identity Psi1=Phi1)")

# ---------- ε² system, explicit point mass ----------
GM = sp.sqrt(GM2)
A, B = sp.symbols('A B')
def ps(f):
    f = sp.expand(f.subs(Sk, 0))
    f = f.replace(varphi2, A*GM2/r**2).replace(psi2, B*GM2/r**2)
    f = f.replace(sp.Derivative(varphi2, (r,2)), 6*A*GM2/r**4)
    f = f.replace(sp.Derivative(psi2, (r,2)), 6*B*GM2/r**4)
    f = f.replace(sp.Derivative(varphi2, r), -2*A*GM2/r**3)
    f = f.replace(sp.Derivative(psi2, r), -2*B*GM2/r**3)
    f = f.replace(sp.Derivative(U, r), -GM/r**2).replace(sp.Derivative(U, (r,2)), 2*GM/r**3)
    f = f.replace(U, GM/r)
    f = sp.expand(f).replace(GM**2, GM2)
    return sp.expand(f)
El = ps(sp.expand(E_Phi.coeff(eps, 2)))
Es = sp.expand(ps(E_Psi.coeff(eps, 2)))
t = sp.symbols('t', positive=True)
def harm(f, deg=5):
    f = sp.expand(f.subs(r, 1/t)).replace(GM, sp.sqrt(GM2))
    return sp.expand(sp.series(f, t, 0, deg).removeO())
Hl = sp.expand(harm(El)); Hs = sp.expand(harm(Es))
print("\nlapse EL ε² (t-series):  ", Hl)
print("spatial EL ε² (t-series):", Hs)
# collect t^2..t^4 coefficients per equation; equations at 1/r^4 (t^4) and 1/r^2 (t^2):
def coeff(f, deg):
    return sp.expand(sp.Poly(sp.expand(f), t).coeff_monomial(t**deg)) if sp.Poly(sp.expand(f), t).degree() >= deg else sp.S.Zero
eqs = []
for f, name in ((Hl, 'lapse'), (Hs, 'spatial')):
    for deg in (2, 3, 4):
        c = sp.simplify(coeff(f, deg))
        if c != 0:
            print(f"  {name} t^{deg}: {c}")
            if deg == 4:
                eqs.append((name, c))
sol = None
if len(eqs) == 2:
    sol = sp.solve([e[1] for e in eqs], [A, B], dict=True)
print("solution (t^4):", sol)
if sol:
    As, Bs = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 =", As, "  B = psi2/U_N^2 =", Bs)
    print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + As))
    r1 = sp.simplify(sp.expand(eqs[0][1].subs({A: As, B: Bs})))
    r2 = sp.simplify(sp.expand(eqs[1][1].subs({A: As, B: Bs})))
    print("residuals:", r1, r2)
    A0, B0 = sp.simplify(As.subs(alpha, 0)), sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    ctl = sp.simplify(sp.expand([e[1] for e in eqs if e[0]=='spatial'])[0].subs({A: 0, B: -sp.Rational(3,4)*GM2}))
    print("G4 neg control (A=0, B=-3/4 GM2): spatial resid =", ctl,
          " at alpha=0:", sp.simplify(ctl.subs(alpha, 0)))
with open('as232_final3_out.txt', 'w') as f:
    f.write(f"G1: {g1}\nG1s: {g1s}\nHl = {Hl}\nHs = {Hs}\nsol = {sol}\n"
            f"BETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3: {A0 if sol else '?'} {B0 if sol else '?'}\n"
            f"G4: {ctl if sol else '?'} {sp.simplify(ctl.subs(alpha,0)) if sol else '?'}\n")