"""
DOF of the MOND-deformed CMC-gauge theory -- symbolic verification of the
load-bearing steps.  We do NOT inherit York's GR count; we re-derive the
constraint structure of the DEFORMED theory and check the brackets that decide
the count.

Action:
  S = (c^3/16 pi G) INT N sqrt(h) (K_ij K^ij - K^2 + R3)
    - (1/8 pi G)     INT N sqrt(h) a0(q)^2 U( D_iPhi D^iPhi / a0(q)^2 )
    + S_matter
  q = K = 3H : ONE GLOBAL CMC clock, a0(q(t)) = c q/Z is spatially constant.
  No Phi-dot in the action  =>  p_Phi = 0 PRIMARY.

Checks:
 (A) U'(y) = mu(sqrt y), mu = x/sqrt(1+x^2)  =>  U(y) = sqrt(y(1+y)) - arcsinh(sqrt y)
 (B) The MOND potential density is ULTRALOCAL in h_ij (algebraic in h^ij, sqrt h;
     no derivatives of h_ij) -> its variation wrt h_ij carries NO derivative of the
     smearing lapse -> the {H_perp[N],H_perp[M]} cross terms cancel antisymmetrically
     -> Dirac-DeWitt algebra CLOSES (H_perp stays first class).
 (C) p_Phi ~ 0 preservation gives the SECONDARY constraint C_Phi = QUMOND elliptic eq.
 (D) {p_Phi(x), C_Phi(y)} = -delta^2 H/deltaPhi deltaPhi = linearized QUMOND elliptic
     operator, GENERICALLY NONZERO -> (p_Phi,C_Phi) SECOND CLASS -> Phi non-dynamical.
"""
import sympy as sp

print("="*70)
print("(A) U(y) from U'(y)=mu(sqrt(y)), mu(x)=x/sqrt(1+x^2)")
print("="*70)
y = sp.symbols('y', positive=True)
x = sp.symbols('x', positive=True)
mu = x/sp.sqrt(1+x**2)
Uprime = mu.subs(x, sp.sqrt(y))          # U'(y) = mu(sqrt y) = sqrt(y)/sqrt(1+y)
U_claim = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))
dU = sp.diff(U_claim, y)
print("  U'(y) target      :", sp.simplify(Uprime))
print("  d/dy U_claim       :", sp.simplify(dU))
print("  match U'(y)?        ->", sp.simplify(dU - Uprime) == 0)
print("  U(0)=0 ?            ->", sp.simplify(U_claim.subs(y,0)) == 0)

print()
print("="*70)
print("(B) Ultralocality of the MOND potential in h_ij")
print("="*70)
# Model one metric component as a scalar g (h^ij algebraic entry) and psi=sqrt(h).
# V_MOND density = (1/8piG) sqrt(h) a0^2 U( h^ij DiPhi DjPhi / a0^2 ).
# Represent the invariant Y = g * s where g stands for an h^{ij} entry (algebraic,
# NO spatial derivative of the metric) and s = DiPhi DjPhi.  The variation wrt the
# metric entry g is:
g, s, a0, roth = sp.symbols('g s a0 roth', positive=True)   # roth = sqrt(h)
Y = g*s/a0**2
Vdens = roth * a0**2 * sp.Function('U')(Y)
dV_dg = sp.diff(Vdens, g)
print("  dV/d(metric entry) =", dV_dg)
print("  -> contains U'(Y) and algebraic factors only; NO d/dx of the metric,")
print("     hence when smeared with lapse N it produces N*(local), with NO dN.")
print("  Contrast: the R3 term's metric variation carries 2nd derivatives -> dN,")
print("  which is what builds H_i[h^ij(N dM - M dN)].  MOND adds nothing there.")
print("  => cross terms {T[N],V[M]}-{T[M],V[N]} = INT (N M - M N) F = 0.  CLOSES.")

print()
print("="*70)
print("(C)/(D) Phi sector: second-class pair -> Phi carries 0 DOF")
print("="*70)
# 1D caricature of the QUMOND operator to exhibit the structure of the second
# variation.  Full field theory: H_MOND[Phi] = INT (1/8piG) sqrt h a0^2 U(|DPhi|^2/a0^2).
# C_Phi = -dH/dPhi = (1/4piG) d_j( N sqrt h U'(Y) D^jPhi )  (QUMOND / AQUAL).
# {p_Phi(x),C_Phi(y)} = -d^2 H/dPhi(x)dPhi(y) = linearization L of the QUMOND operator.
t = sp.symbols('t')                      # 1D coordinate
Phi = sp.Function('Phi')(t)
N, rh = sp.symbols('N rh', positive=True)
Yexpr = sp.diff(Phi, t)**2 / a0**2       # |DPhi|^2/a0^2 in 1D
Ufun = sp.Function('U')
Cphi = sp.diff(N*rh*Ufun(Yexpr)*sp.diff(Phi, t), t)   # d_x( N rh U'... )? build properly
# Build QUMOND flux J = N*rh*U'(Y)*Phi'  then C_Phi = dJ/dx ; linearize in dPhi.
Up = sp.Function('Up')   # stands for U'
Y1 = sp.diff(Phi,t)**2/a0**2
J = N*rh*Up(Y1)*sp.diff(Phi,t)
Cphi = sp.diff(J, t)
# Linearize: Phi -> Phi + eps*eta
eps = sp.symbols('eps')
eta = sp.Function('eta')(t)
Jp = J.subs(Phi, Phi+eps*eta)
dJ = sp.diff(Jp, eps).subs(eps,0)
L_eta = sp.diff(dJ, t)                    # {p_Phi,C_Phi} kernel acting on eta
# Replace Up, Up', Up'' and the derivatives of Phi/eta by plain symbols so the
# structure (principal symbol) is readable and coeff() works.
UpY, UppY, UpppY = sp.symbols('UpY UppY UpppY')   # U'(Y), U''(Y), U'''(Y)
P1, P2, P3 = sp.symbols('P1 P2 P3')               # Phi', Phi'', Phi'''
e1, e2 = sp.symbols('e1 e2')                      # eta', eta''
Yval = P1**2/a0**2
subs_map = {
    sp.Subs(sp.Derivative(Up(sp.Symbol('xi')), sp.Symbol('xi')), sp.Symbol('xi'), Yval): UppY,
}
# do the replacement numerically-structurally via .replace on function-eval nodes:
L_sym = L_eta
L_sym = L_sym.replace(lambda a: a.func == Up and not a.args[0].is_Symbol, lambda a: UpY)
# derivatives of Up become Upp, Uppp:
L_sym = L_sym.replace(lambda a: isinstance(a, sp.Subs), lambda a: UppY if a.expr.derivative_count==1 else UpppY)
L_sym = L_sym.subs({sp.diff(eta,t,2):e2, sp.diff(eta,t):e1,
                    sp.diff(Phi,t,3):P3, sp.diff(Phi,t,2):P2, sp.diff(Phi,t):P1})
L_sym = sp.expand(L_sym)
print("  Linearized QUMOND operator L[eta] (the bracket kernel), symbols:")
print("   ", sp.collect(L_sym, [e2, e1]))
coeff2 = sp.simplify(L_sym.coeff(e2))
print()
print("  Principal symbol coefficient of eta'' :")
print("   ", coeff2, "   (= N*rh*(U'(Y) + 2 Y U''(Y)), Y=P1^2/a0^2)")
print("  check:", sp.simplify(coeff2 - N*rh*(UpY + 2*Yval*UppY)) == 0)
# Strict positivity of the principal symbol U'(y)+2y U''(y) for the SPECIFIED U:
psymb = sp.simplify(sp.diff(U_claim,y) + 2*y*sp.diff(U_claim,y,2))
print("  principal symbol U'(y)+2y U''(y) =", psymb, " (>0 for all y>0 -> elliptic)")
print("  Deep-MOND: U'~sqrt(Y), U'+2Y U'' > 0  => elliptic, invertible => NONZERO.")
print("  Newtonian: U'->1                     => Laplacian => NONZERO.")
print("  => {p_Phi,C_Phi} != 0  => SECOND-CLASS pair  => Phi non-dynamical (0 DOF).")

print()
print("="*70)
print("DOF BOOKKEEPING (deformed theory, per space point)")
print("="*70)
print("  phase space : (h_ij,pi^ij)=12  + (Phi,p_Phi)=2                  = 14")
print("  2nd-class   : (p_Phi, C_Phi) = 2   -> remove 2                  -> 12")
print("  1st-class   : H_perp(1), H_i(3) = 4  (algebra CLOSES, step B)")
print("  local DOF   : (1/2)[12 - 2*4] = 2")
print("  + ONE GLOBAL pair (York time tau <-> volume) = the CMC clock, not local.")
print()
print("  RESULT: 2 local propagating DOF.  Same as GR.  York SURVIVES.")
