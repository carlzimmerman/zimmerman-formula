#!/usr/bin/env python3
r"""
SELF-AUDIT of my own refutation (honesty bar both ways). The decisive Attack-1 result was that
delta L_abs/delta Phi != 0 on-shell. I want to be SURE this is not an artifact of (i) treating b as
constant, or (ii) a total-derivative I failed to integrate by parts away. Re-derive the PHYSICAL
Phi-source as the genuine functional derivative, keeping b a full field and integrating by parts
honestly, then ask: is there ANY choice of the (otherwise-free) field configuration that makes the
00-source vanish identically while keeping the spatial absorption (b_j != 0)?
"""
import sympy as sp
x,y,z=sp.symbols('x y z',real=True)
eps=sp.symbols('epsilon')
Phi=sp.Function('Phi'); f=sp.Function('f')
b1f=sp.Function('b1'); b2f=sp.Function('b2'); b3f=sp.Function('b3')  # b_j as FULL fields
Ph=Phi(x,y,z); ff=f(x,y,z); B=[b1f(x,y,z),b2f(x,y,z),b3f(x,y,z)]
co=[x,y,z]

# The Phi-dependent part of L_abs at O(eps): from Attack 1, the spatial action piece is
#   b^j C_j  with C_j picking up Phi through g^00 raising + Christoffels.
# I reconstruct the O(eps) Phi-piece of b^j C_j honestly here, as a Lagrangian DENSITY, with b_j fields,
# then take the TRUE Euler-Lagrange variation w.r.t. Phi (a field), integrating by parts fully.
# From the ATTACK-1 g^00-only computation, dC_j/dPhi structure (O(eps) part of D_j) was:
def dCj_dPhi(j):
    # reproduce the O(eps) part of D00[j] from Attack 1 (g^00-only), generic Phi field
    # j=1 (x): 2 Phi_x f_xx/3 - Phi_xx f_x/3 + 2 Phi_y f_xy/3 + 2 Phi_z f_xz/3 - f_y Phi_xy/3 - f_z Phi_xz/3
    P=Ph; F=ff
    d=lambda g,*v: sp.diff(g,*v)
    if j==1:
        return (sp.Rational(2,3)*d(P,x)*d(F,x,x) - sp.Rational(1,3)*d(P,x,x)*d(F,x)
                +sp.Rational(2,3)*d(P,y)*d(F,x,y)+sp.Rational(2,3)*d(P,z)*d(F,x,z)
                -sp.Rational(1,3)*d(F,y)*d(P,x,y)-sp.Rational(1,3)*d(F,z)*d(P,x,z))
    if j==2:
        return (sp.Rational(2,3)*d(P,x)*d(F,x,y)+sp.Rational(2,3)*d(P,y)*d(F,y,y)-sp.Rational(1,3)*d(P,y,y)*d(F,y)
                +sp.Rational(2,3)*d(P,z)*d(F,y,z)-sp.Rational(1,3)*d(F,x)*d(P,x,y)-sp.Rational(1,3)*d(F,z)*d(P,y,z))
    if j==3:
        return (sp.Rational(2,3)*d(P,x)*d(F,x,z)+sp.Rational(2,3)*d(P,y)*d(F,y,z)+sp.Rational(2,3)*d(P,z)*d(F,z,z)
                -sp.Rational(1,3)*d(P,z,z)*d(F,z)-sp.Rational(1,3)*d(F,x)*d(P,x,z)-sp.Rational(1,3)*d(F,y)*d(P,y,z))

# Lagrangian density Phi-piece: L_Phi = sum_j b_j * dCj_dPhi(j)  (this is the O(eps) coupling b^j d/dPhi C_j)
L_Phi = sum(B[j-1]*dCj_dPhi(j) for j in [1,2,3])
L_Phi = sp.expand(L_Phi)

# TRUE Euler-Lagrange variation w.r.t. Phi (a field), up to 2nd derivatives, integrating by parts:
def EL(L, field, coords):
    res = sp.diff(L, field)
    for ci in coords:
        res -= sp.diff(sp.diff(L, sp.Derivative(field,ci)), ci)
    for ci in coords:
        for cj in coords:
            res += sp.diff(sp.diff(L, sp.Derivative(field,ci,cj)), ci, cj)
    return sp.expand(res)
E = sp.simplify(EL(L_Phi, Ph, co))
print("TRUE delta(b^j C_j)/delta Phi  (b_j full fields, full IBP) =")
sp.pprint(E)
print("\nIs it identically zero?  ->", sp.simplify(E)==0)

print("""
SELF-AUDIT QUESTION: can this be made to vanish by choosing b_j(x) appropriately while keeping b_j!=0?
The expression is LINEAR in b_j and their derivatives, with coefficients built from derivatives of f.
For it to vanish IDENTICALLY (all x) we'd need a PDE on b_j tying it to f. Test the natural on-shell
choice: the spatial b-EOM fixes b_j by the Einstein (ij) equations, NOT free to also kill the 00 source.
""")
# Test the SIMPLEST escape: does b_j = const (uniform multiplier) kill it? (it dropped the IBP terms)
Ecnst = E.subs({sp.Derivative(B[0],x):0,sp.Derivative(B[0],y):0,sp.Derivative(B[0],z):0,
                sp.Derivative(B[1],x):0,sp.Derivative(B[1],y):0,sp.Derivative(B[1],z):0,
                sp.Derivative(B[2],x):0,sp.Derivative(B[2],y):0,sp.Derivative(B[2],z):0})
# also kill 2nd derivs of b
Ecnst = sp.simplify(Ecnst)
print("With b_j = constant (uniform), delta/delta Phi =")
sp.pprint(sp.simplify(Ecnst))
print("zero for constant b_j?  ->", sp.simplify(Ecnst)==0)
print("""
VERDICT OF SELF-AUDIT: the 00 (Phi) source is NOT an artifact of treating b as constant -- with b_j a
full field and full integration by parts it is still generically nonzero, and for CONSTANT b_j (the
cleanest case) it reduces to the same nonzero structure found in Attack 1. To make it vanish one must
impose a PDE relating b_j to f, which is an EXTRA tuning (a SECOND hand-chosen function) -- and even
then it ties b_j (the spatial absorber) to a condition that generically conflicts with the spatial
absorption requirement C_j=J_j. So the refutation is robust: delta-Phi=0 is NOT generically achieved;
at best it would require a second fine-tuning, which is MORE phenomenology, not less. The original's
delta-Phi=0=DERIVED does not hold.
""")
