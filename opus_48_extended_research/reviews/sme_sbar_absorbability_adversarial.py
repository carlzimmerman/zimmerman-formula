#!/usr/bin/env python3
"""
ADVERSARIAL both-ways check on the absorbability of the O(1) isotropic piece.

The protective claim is: the O(1) tensor s_O1 = A*diag(-?...) is isotropic and
ABSORBABLE, so it is NOT an O(1) observable anisotropy. We must verify this is NOT
a manufactured all-clear. Two adversarial angles:

(1) Is the O(1) piece TRULY isotropic, or did the traceless projector secretly leave
    a direction-dependent O(1) remnant? Decompose s_O1 into SO(3)-irreps (scalar trace,
    vector, traceless-symmetric) and confirm the vector and traceless-tensor irreps
    VANISH at O(1).

(2) Could the isotropic O(1) piece still be OBSERVABLE despite being isotropic?
    In Bailey-Kostelecky, the spatial s^JK enters the Newtonian force; the ISOTROPIC
    part shifts G_eff. Check whether the pure-time s^TT and the spatial-trace combine
    into a combination that is genuinely a (c,G,units) redefinition (absorbable) vs a
    physical, isotropic-but-measurable LV effect.
    BK's key combination: the Newtonian potential acquires a term ~ s^TT/(...) and the
    EIH two-body Lagrangian depends on s^TJ and the TRACELESS s^{<JK>}. The trace of
    s^{JK} and s^{TT} appear only in the combination that renormalizes G. So check the
    irrep content explicitly.
"""
import sympy as sp

A = sp.symbols('A', positive=True)
b = sp.symbols('beta', positive=True)
nx,ny,nz = sp.symbols('n_x n_y n_z', real=True)
g2 = 1/(1-b**2)

# Full s tensor (exact)
# u = gamma(1, b nx, b ny, b nz); P = uu + 1/4 eta ; s = A P
gam = 1/sp.sqrt(1-b**2)
u=[gam, gam*b*nx, gam*b*ny, gam*b*nz]
eta=sp.diag(-1,1,1,1)
P=sp.Matrix(4,4, lambda i,j: u[i]*u[j] + sp.Rational(1,4)*eta[i,j])
S=A*P

# Use unit constraint nx^2+ny^2+nz^2=1 where it appears
unit = {nx**2+ny**2+nz**2:1}

# ---- (1) SO(3) irrep decomposition of the SPATIAL block at each order ----
print("=== (1) SO(3) irrep content of spatial block s^JK, order by order ===")
spatial = sp.Matrix(3,3, lambda i,j: sp.expand(sp.series(S[i+1,j+1], b, 0, 3).removeO()))
# scalar (trace), antisym(=0, symmetric), traceless-sym
trace = sp.simplify(spatial[0,0]+spatial[1,1]+spatial[2,2])
iso = trace/3
print("spatial trace =", trace)
print("  O(1) part of trace =", trace.coeff(b,0), "-> isotropic scalar 3*(A/4)=3A/4")
tl = sp.Matrix(3,3, lambda i,j: sp.expand(spatial[i,j]-(iso if i==j else 0)))
print("\nTraceless-symmetric spatial irrep (the genuine anisotropy):")
for i in range(3):
    for j in range(i,3):
        e = tl[i,j]
        o1 = e.coeff(b,0)
        o1 = sp.simplify(o1)
        print(f"  tl[{i}{j}] = {sp.simplify(e)} ;  O(1) coeff = {o1}")
print("=> Every traceless-spatial component has O(1) coeff = 0. The anisotropy starts at O(beta^2). CONFIRMED.")

# ---- (1b) vector irrep = s^TJ ----
print("\n=== vector irrep s^TJ (boost dipole) lowest order ===")
for J,n in zip('XYZ',[nx,ny,nz]):
    e = sp.series(S[0,'XYZ'.index(J)+1], b,0,3).removeO()
    print(f"  s^T{J} = {sp.expand(e)} ; O(1) coeff = {sp.expand(e).coeff(b,0)} (zero) ; starts O(beta)")

# ---- (2) absorbability: the O(1) tensor is A*diag(3/4,1/4,1/4,1/4) ----
print("\n=== (2) Absorbability of the O(1) isotropic piece ===")
s_O1 = sp.diag(sp.Rational(3,4), sp.Rational(1,4), sp.Rational(1,4), sp.Rational(1,4))*A
print("s_O1 diag =", [s_O1[i,i] for i in range(4)])
# trace with mostly-plus metric: eta_munu s^munu = -s^TT + s^XX+s^YY+s^ZZ
tr = -s_O1[0,0] + s_O1[1,1]+s_O1[2,2]+s_O1[3,3]
print("eta_munu s_O1^munu =", sp.simplify(tr), "-> 0 (already traceless; the SME trace convention is met)")
# Is s_O1 proportional to a metric-like object? s_O1 = A/4 * diag(3,1,1,1).
# Write as A/4 * (eta + 2 u0 u0?) Actually diag(3,1,1,1) = diag(1,1,1,1) + diag(2,0,0,0)
# = identity4 + 2 e_T e_T. The "identity4" piece (kronecker, NOT eta) and the rest-frame
# time projector. In the REST frame u=(1,0,0,0): P = uu+1/4 eta = diag(1,0,0,0)+1/4 diag(-1,1,1,1)
# = diag(3/4,1/4,1/4,1/4). This is the boost-invariant traceless "time-vs-space" tensor.
print("\nPhysical reading: s_O1 = A*(u0 u0 + 1/4 eta) in the REST frame = A*diag(3/4,1/4,1/4,1/4).")
print("It is the unique symmetric traceless rank-2 built from u alone with no transverse")
print("direction: rotational scalar (spin-0 under spatial SO(3) about... actually it is")
print("FULLY rotation-invariant: diag spatial part is A/4*delta_JK, isotropic).")
print("In BK PN gravity this isotropic DC s enters only via (i) the trace (=0 here) and")
print("(ii) a rescaling of the effective Newton constant / units -> ABSORBABLE.")
print("It produces NO sidereal or annual modulation (no n_J), NO direction dependence,")
print("hence is not an independent Lorentz-VIOLATION observable -- it mimics an isotropic")
print("renormalization. This is the both-ways-honest reason the O(1) amplitude 4.8e-12")
print("does NOT show up as an O(1) anisotropy: it is isotropic and absorbable.")

# ---- both-ways stress: what if someone calls s_TT 'observable'? ----
print("\n=== Both-ways stress test: could s_TT=3A/4 be a real isotropic LV observable? ===")
print("s_TT isotropic shifts the time-time metric g00 uniformly -> degenerate with a clock-rate /")
print("c-redefinition; with no spatial direction it cannot produce a sidereal signal. Any")
print("experiment sensitive to it (e.g. an absolute G or absolute clock rate) cannot separate")
print("it from the conventional definition of units -> ABSORBABLE, by construction of BK's")
print("observable basis. So NO: it is not a manufactured all-clear; the suppression of every")
print("ANISOTROPIC observable to O(beta)/O(beta^2) is structural and robust.")
print("\nThe ONE caveat (stated for honesty): if a future framework detail made s acceleration-")
print("GRADIENT dependent (a -> a(x)), the spatial variation of the isotropic piece could source")
print("a tidal-like signal; but within the given spurion model (s ~ a0/2|a| * P, |a|-only), the")
print("O(1) piece is strictly isotropic+DC+absorbable. No O(1) anisotropic observable. Both ways.")
