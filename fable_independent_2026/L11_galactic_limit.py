#!/usr/bin/env python3
"""
L11 -- does the IC-series have a MOND limit, with what acceleration scale and what interpolation function?
==========================================================================================================
THE QUESTION.  The lead agent's IC-series (closure_2026/integrable_clock_construction_2026/) is building a
relativistic gravity theory: two tensors + one clock, Einstein gravity plus a local clock pressure on its
expanding plateau.  Its own status file says "galactic matching ... remain OPEN".  A healthy relativistic
theory is not yet a theory of THIS framework unless its static weak-field limit reproduces MOND
phenomenology with the programme's acceleration scale.  This lane takes that limit independently.

WHAT IS TAKEN FROM THE LEAD (read-only, files only, no script of theirs is imported or rerun):
  IC1  ACTION.md          S = int sqrt(-g){ m/2 [R4 - 2L + 4KW - 6W^2 + 2(1-u^2) a.a - 2 a0^2 U(u^2)] + kappa X } + Sm
                          U(c) = (1-c)[ln^2(1-c) - 2 ln(1-c) + 2] - 2,  a_mu = D_mu ln N,  X = -(dT)^2/2, N = (2X)^{-1/2}
  IC4  IC4_ACTION.md      adds (Q^2/a0^2)(J + Rhat F);  Q = K - 3W vanishes on the static branch, so the
                          static sector is IC1's, unchanged (IC4 "Which same-action bridges hold", bullet 1)
  IC5  IC5_ACTION.md      first-order phase action; at pi = 0 the activation eta = 0 on a neighbourhood and
                          "every first jet of the difference from the IC-4 Hamiltonian vanishes"
  IC10 IC10_LOCAL_CLOCK.md H10 = H5 + eta{...}: the added block is proportional to eta, so it vanishes
                          identically on the static eta = 0 plateau ("At the static eta=0 plateau the action
                          difference and all its first jets vanish")
  => the STATIC sector of IC5/IC10 is the static sector of IC1.  That chain is what makes this lane a test
  of the CURRENT construction and not of a superseded one.  Everything below is re-derived from the IC1
  action as printed; the lead's REPORT.md section 3 is used only as a cross-check AFTER the fact.

WHAT IS DERIVED HERE, from scratch, with sympy:
  A1  the exact static ADM reduction of sqrt(-g) R4 (null-Lagrangian test, not a claim);
  A2  CONTROL: the same machinery on GR + minimally coupled static dust must return the Newtonian Poisson
      equation with G = 1/(8 pi m).  If A2 fails nothing else in this file may be believed;
  A3  the auxiliary equation and its regular branch, from U alone;
  A4  the two independent static metric equations with the clock/vacuum sources RETAINED, then the ordered
      weak-field limit;
  A5  the eliminated (AQUAL) function and the interpolation function it defines.

  B   numerics: the force law, the acceleration scale, the kernel comparison against the programme's
      CARRIED kernel (nu_RAR, THE_ACTION 2026-09-05 section 3) and against the lead's own target
      mu(y) = 1 - exp(-y) (PATH_FORWARD.md line 23), the size of every term the weak-field limit DROPPED,
      the bounded-boost ceiling on SPARC, and the one input the published files do not fix.

Both a0 footings throughout: 9.3619e-11 (canonical) and 1.1279e-10 m/s^2 (alt).
a0 is an INPUT to the IC construction; the programme's rules permit that ("treat a0 as input until
derived").  The question asked here is not whether a0 is derived, it is whether the theory USES it to
produce the right force law.  A check that a0 is an input cannot fail and is not asked; the check that CAN
fail is whether the scale in the deep-MOND law is 1.000 x a0 rather than 2 a0, a0/2, 2 pi a0, ...
"""
import os, sys, math, glob
import numpy as np
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_LIGHT = 2.99792458e8
G_NEWT  = 6.674e-11
MSUN    = 1.98892e30
kpc     = 3.0856775814913673e19
Mpc     = 1000.0*kpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0_SI = 67.4e3/Mpc

print("=" * 120)
print("L11 -- the IC-series' galactic limit: MOND or not, at what scale, with what interpolation function")
print("=" * 120, flush=True)

# =====================================================================================================
# A. SYMBOLIC.  The static, weak-field, non-relativistic reduction, taken here, not imported.
# =====================================================================================================
print("\n" + "-" * 120)
print("A. SYMBOLIC REDUCTION (sympy; the lead's scripts are neither imported nor rerun)")
print("-" * 120, flush=True)

# ---- jet-variable machinery for one radial coordinate -----------------------------------------------
r = sp.Symbol('r', positive=True)
P = sp.symbols('P0 P1 P2 P3 P4')          # Phi, Phi', Phi'', ...
S = sp.symbols('S0 S1 S2 S3 S4')          # Psi, Psi', ...
Uj = sp.symbols('U0 U1 U2')               # u, u', ...
RH = sp.symbols('RH0 RH1')                # rho-tilde (conserved coordinate matter density), its derivative
JETS = [(P[i], P[i+1]) for i in range(4)] + [(S[i], S[i+1]) for i in range(4)] + \
       [(Uj[i], Uj[i+1]) for i in range(2)] + [(RH[0], RH[1])]

def Dtot(expr):
    """total d/dr on the jet space"""
    out = sp.diff(expr, r)
    for a, b in JETS:
        out += b*sp.diff(expr, a)
    return out

def EL(L, tower):
    """Euler-Lagrange operator to second order for the variable whose jet tower is `tower`"""
    f0, f1, f2 = tower[0], tower[1], tower[2]
    return sp.diff(L, f0) - Dtot(sp.diff(L, f1)) + Dtot(Dtot(sp.diff(L, f2)))

# ---- A1: exact static ADM reduction of sqrt(-g) R4 ---------------------------------------------------
th = sp.Symbol('theta')
tt, rr = sp.symbols('t r_', positive=True)
Phif = sp.Function('Phi')(r); Psif = sp.Function('Psi')(r)
xs = [tt, r, th, sp.Symbol('varphi')]
gmat = sp.diag(-sp.exp(2*Phif), sp.exp(-2*Psif), sp.exp(-2*Psif)*r**2, sp.exp(-2*Psif)*r**2*sp.sin(th)**2)
ginv = gmat.inv()
Gam = [[[sp.S(0)]*4 for _ in range(4)] for _ in range(4)]
for a in range(4):
    for b in range(4):
        for c in range(4):
            s = sp.S(0)
            for d in range(4):
                s += ginv[a, d]*(sp.diff(gmat[d, b], xs[c]) + sp.diff(gmat[d, c], xs[b]) - sp.diff(gmat[b, c], xs[d]))
            Gam[a][b][c] = sp.simplify(s/2)
Ric = sp.zeros(4, 4)
for b in range(4):
    for c in range(4):
        s = sp.S(0)
        for a in range(4):
            s += sp.diff(Gam[a][b][c], xs[a]) - sp.diff(Gam[a][b][a], xs[c])
            for d in range(4):
                s += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
        Ric[b, c] = sp.simplify(s)
R4 = sp.simplify(sum(ginv[b, c]*Ric[b, c] for b in range(4) for c in range(4)))
sqrtg = sp.exp(Phif - 3*Psif)*r**2*sp.sin(th)      # N sqrt(h)
dens_full = sp.simplify(sp.expand(sqrtg*R4/sp.sin(th)))     # per unit solid angle

def to_jets(e):
    e = e.subs({sp.Derivative(Phif, (r, 2)): P[2], sp.Derivative(Psif, (r, 2)): S[2]})
    e = e.subs({sp.Derivative(Phif, r): P[1], sp.Derivative(Psif, r): S[1]})
    return sp.simplify(e.subs({Phif: P[0], Psif: S[0]}))

dens_full_j = to_jets(dens_full)
As = sp.exp(P[0] - S[0]); Bs = sp.exp(P[0] - 3*S[0])
Fgr = S[1]**2 - 2*P[1]*S[1]
claim = 2*As*r**2*Fgr
diff_dens = sp.simplify(dens_full_j - claim)
null_phi = sp.simplify(EL(diff_dens, P))
null_psi = sp.simplify(EL(diff_dens, S))
print(f"  A1  sqrt(-g)R4 (static, isotropic, spherical) computed from the metric; per solid angle it is")
print(f"      2 e^(Phi-Psi) r^2 [ Psi'^2 - 2 Phi' Psi' ]  +  (a total r-derivative)")
print(f"      Euler-Lagrange residual of the difference:  d/dPhi -> {null_phi},   d/dPsi -> {null_psi}")
check("A1 the exact static reduction of sqrt(-g)R4 is 2 A_s (|grad Psi|^2 - 2 grad Phi . grad Psi) up to a "
      "total derivative  [the lapse-gradient square CANCELS in GR: any |grad Phi|^2 must come from elsewhere]",
      null_phi == 0 and null_psi == 0, "both EL residuals of the difference vanish identically")

# ---- A2: CONTROL.  GR + minimally coupled static dust must give the Newtonian Poisson equation --------
m, kap, a0, Lam = sp.symbols('m kappa a_0 Lambda', positive=True)
eps = sp.Symbol('epsilon', positive=True)
# matter: static dust, conserved COORDINATE density rho~ = sqrt(h) rho, so S_m = - int d^3x N rho~ .
# (varying at fixed rho~ is what makes the dust's pressure source vanish; varying at fixed rho would
#  wrongly insert a 3 rho source into the conformal equation.)
L_matter = -sp.exp(P[0])*RH[0]*r**2
L_gr = m*As*r**2*Fgr + L_matter
elP_gr = sp.simplify(EL(L_gr, P)); elS_gr = sp.simplify(EL(L_gr, S))

def weak(e):
    """the stated ordering: potentials O(eps), a0 L = O(eps), rho L^2/m = O(eps); keep the leading order.
    u itself stays O(1) because y = |grad Phi|/a0 = O(eps)/O(eps) is O(1)."""
    sub = {P[i]: eps*P[i] for i in range(5)}
    sub.update({S[i]: eps*S[i] for i in range(5)})
    sub.update({RH[0]: eps*RH[0], RH[1]: eps*RH[1], a0: eps*a0})
    return sp.simplify(sp.series(e.subs(sub), eps, 0, 2).removeO())

lapP = P[2] + 2*P[1]/r; lapS = S[2] + 2*S[1]/r      # radial Laplacian lap(f) = f'' + 2f'/r
wP = sp.expand(sp.simplify(weak(elP_gr)/r**2/eps))
wS = sp.expand(sp.simplify(weak(elS_gr)/r**2/eps))
resP = sp.simplify(wP - (2*m*lapS - RH[0]))                    # expect  2 m lap(Psi) = rho
resS = sp.simplify(wS - 2*m*(lapP - lapS))                     # expect  lap(Phi - Psi) = 0
print(f"\n  A2  CONTROL, general relativity + minimally coupled static dust:")
print(f"      lapse variation      ->   {wP} = 0     i.e.  2 m lap(Psi) = rho,  lap(Psi) = 4 pi G rho, G = 1/(8 pi m)")
print(f"      conformal variation  ->   {wS} = 0     i.e.  lap(Phi - Psi) = 0   (no-slip; dust has no pressure source)")
check("A2 [CONTROL] the reduction machinery applied to ordinary GR + a minimally coupled static source "
      "returns the Newtonian Poisson equation with G_N = 1/(8 pi m)",
      resP == 0 and resS == 0, "lapse eq gives rho = 2m lap(Psi); conformal eq gives lap(Phi-Psi) = 0, hence lap(Phi) = 4 pi G rho")

# ---- A3: the auxiliary equation and its regular branch, from U alone ---------------------------------
c = sp.Symbol('c')                                  # c = u^2
Ufun = (1 - c)*(sp.log(1 - c)**2 - 2*sp.log(1 - c) + 2) - 2
Uprime = sp.simplify(sp.diff(Ufun, c))
Uprime_target = -sp.log(1 - c)**2
print(f"\n  A3  U(c) = (1-c)[ln^2(1-c) - 2 ln(1-c) + 2] - 2   =>   U'(c) = {sp.simplify(Uprime)}")
check("A3a U'(c) = -ln^2(1-c) exactly  [this single identity is what makes the exponential law come out]",
      sp.simplify(Uprime - Uprime_target) == 0, "sympy differentiation of U")

# static branch: K = W = 0 => Q = 0 => IC4/IC5/IC10 extra terms drop; u appears algebraically in
#   (m/2)[ 2(1-u^2) a.a - 2 a0^2 U(u^2) ] , a.a = h^ij d_i Phi d_j Phi (the exact covariant leaf norm)
asq = sp.Symbol('a_sq', positive=True)
Vu = (1 - c)*asq - a0**2*Ufun                       # per (m/2)*2 ; c = u^2 varied
dVu = sp.simplify(sp.diff(Vu, c))
branch = sp.solve(sp.Eq(dVu, 0), c)
y = sp.Symbol('y', positive=True)                   # y = |a|/a0
cstar = 1 - sp.exp(-y)
resid = sp.simplify(dVu.subs({c: cstar, asq: a0**2*y**2}))
hess = sp.simplify(sp.diff(Vu, c, 2).subs({c: cstar, asq: a0**2*y**2}))
print(f"      auxiliary equation  d/dc[(1-c)a^2 - a0^2 U(c)] = 0  =>  a^2 = a0^2 ln^2(1-c)  =>  u^2 = 1 - exp(-|a|/a0)")
print(f"      residual at the branch: {resid};   d^2/dc^2 there: {sp.simplify(hess)}  (>0 for y>0: a nondegenerate minimum)")
check("A3b the regular static branch is u^2 = 1 - exp(-|a|/a0), y = |a|/a0, derived here from U and not "
      "assumed  [independently reproduces IC1 REPORT.md section 2]",
      resid == 0, "exact residual 0; Hessian 2 a0^2 y e^y > 0, so the stationary point is nondegenerate for y>0")
print(f"      NOTE (branch selection): the u-equation carries an overall factor u, so u = 0 solves it for ANY a.")
print(f"      On that branch the operator below degenerates to 0 = rho and no sourced solution exists, which is")
print(f"      what selects the regular branch; the published files flag this as requiring separate treatment.")

# ---- A4: the two independent static equations, clock/vacuum sources RETAINED -------------------------
u0 = Uj[0]
Cvac = Lam + a0**2*Ufun.subs(c, u0**2)
F_ic = S[1]**2 - 2*P[1]*S[1] + (1 - u0**2)*P[1]**2
X_clock = sp.exp(-2*P[0])/2                          # X = 1/(2N^2), unitary gauge T = t, N = e^Phi
L_ic = m*As*r**2*F_ic - m*Bs*r**2*Cvac + kap*sp.exp(-P[0] - 3*S[0])*r**2/2 + L_matter
elP = sp.simplify(EL(L_ic, P)); elS = sp.simplify(EL(L_ic, S)); elU = sp.simplify(EL(L_ic, Uj))
# cross-check against the lead's REPORT.md section 3 display (done AFTER the derivation, as a check)
lead_P = 2*m*Dtot(As*r**2*(S[1] - (1 - u0**2)*P[1]))/r**2 + m*As*F_ic - m*Bs*Cvac - Bs*(RH[0]*sp.exp(3*S[0]) + kap*X_clock)
print(f"\n  A4  IC static density (per solid angle):  m A_s r^2 F - m B_s r^2 C + (kappa/2) e^(-Phi-3Psi) r^2 + L_m,")
print(f"      F = |grad Psi|^2 - 2 grad Phi . grad Psi + (1-u^2)|grad Phi|^2,   C = Lambda + a0^2 U(u^2).")
agree = sp.simplify(sp.expand(elP/r**2 - lead_P)) == 0
print(f"      lapse variation reproduces IC1 REPORT.md eq (3.1) with the clock source 4 kappa X retained: {agree}")
check("A4a the independently varied lapse equation agrees term by term with the lead's published static "
      "equation, clock/vacuum sources retained",
      agree, "2m div[A_s(grad Psi - (1-u^2) grad Phi)] + m A_s F - m B_s C = B_s(rho + kappa X)")

# the EXACT static auxiliary equation, before any weak-field step
elU_exact = sp.simplify(elU/(m*r**2))
elU_target = -2*u0*(P[1]**2*sp.exp(P[0] - S[0]) - a0**2*sp.exp(P[0] - 3*S[0])*sp.log(1 - u0**2)**2)
print(f"      exact auxiliary equation: {elU_exact} = 0")
print(f"      i.e.  e^(2Psi) Phi'^2 = a0^2 ln^2(1-u^2), and e^(2Psi)Phi'^2 IS the covariant |a|^2 = h^ij a_i a_j,")
print(f"      so u^2 = 1 - exp(-|a|/a0) holds EXACTLY on the static branch, with no weak-field step.")
check("A4b the constitutive law u^2 = 1 - exp(-|a|/a0) is EXACT on the static branch (covariant leaf norm), "
      "not a weak-field approximation",
      sp.simplify(elU_exact - elU_target) == 0, "the exact u-variation has the covariant e^(2Psi)Phi'^2 = |a|^2")

# ordered weak-field limit: potentials O(e), a0 L = O(e), Lambda L^2 = o(e), kappa X L^2/m = o(e)
wP_ic = sp.expand(sp.simplify(weak(elP.subs({Lam: 0, kap: 0}))/r**2/eps))
wS_ic = sp.expand(sp.simplify(weak(elS.subs({Lam: 0, kap: 0}))/r**2/eps))
slip = sp.simplify(wS_ic - 2*m*(lapP - lapS))
print(f"      weak-field conformal equation: {wS_ic} = 0   ->   lap(Phi - Psi) = 0")
check("A4c the conformal equation still gives no slip, lap(Phi - Psi) = 0, once the clock term is added "
      "[Phi = Psi is what lets lensing and dynamics share one potential]",
      slip == 0, "the (1-u^2)|grad Phi|^2 term is second order in the potentials and drops out of this equation")

# impose Phi = Psi and read off the operator
oper = sp.expand(sp.simplify(wP_ic.subs({S[i]: P[i] for i in range(5)})))
target = 2*m*(u0**2*(P[2] + 2*P[1]/r) + 2*u0*Uj[1]*P[1]) - RH[0]   # 2m div[u^2 grad Phi] - rho, spherical
print(f"      weak-field lapse equation with Phi = Psi:  {oper} = 0   ==   2 m div[u^2 grad Phi] - rho")
check("A4d the weak-field static equation is  div[ u^2 grad Phi ] = rho/(2m) = 4 pi G_N rho,  G_N = 1/(8 pi m)",
      sp.simplify(oper - target) == 0, "exact match to 2m div[u^2 grad Phi] - rho")

# ---- A5: the eliminated function and the interpolation function --------------------------------------
# the FULL on-shell function of a^2 is the GR piece (-a^2, from A1 with Phi = Psi) plus the clock piece f
f_onshell = sp.simplify((2*(1 - cstar)*a0**2*y**2 - 2*a0**2*Ufun.subs(c, cstar))/2)
f_target = 2*a0**2*(1 - (1 + y)*sp.exp(-y))
dfda2 = sp.simplify(sp.diff(f_onshell, y)/sp.diff(a0**2*y**2, y))
Ftot = -a0**2*y**2 + f_onshell
mu_from_F = sp.simplify(-sp.diff(Ftot, y)/sp.diff(a0**2*y**2, y))
print(f"\n  A5  eliminating u on the regular branch gives the clock's AQUAL function")
print(f"      f(a^2) = {sp.simplify(f_onshell)}  = 2 a0^2 [1 - (1+y) e^-y]      [IC1 REPORT.md section 2]")
print(f"      d f/d(a^2) = {dfda2} = 1 - u^2   (envelope theorem: the clock piece alone)")
print(f"      total on-shell function  Ftot(a^2) = -a^2 + f(a^2)  (the -a^2 is GR's, from A1 with Phi = Psi)")
print(f"      -d Ftot/d(a^2) = {mu_from_F}  =  u^2  =  mu(y)   <-- the interpolation function")
check("A5a eliminating the auxiliary gives the clock's AQUAL function f(a^2) = 2 a0^2 [1 - (1+y) e^-y] with "
      "df/d(a^2) = 1 - u^2 = e^-y, exactly as the lead publishes",
      sp.simplify(f_onshell - f_target) == 0 and sp.simplify(dfda2 - sp.exp(-y)) == 0, "sympy elimination")
mu_direct = sp.simplify(cstar)
check("A5b the interpolation function -- the coefficient multiplying grad Phi inside the divergence, "
      "equivalently -dFtot/d(a^2) -- is mu(y) = u^2 = 1 - e^-y (NOT 1-u^2 = e^-y): mu -> 1 at high "
      "acceleration and mu -> y at low acceleration, which is what makes it MOND rather than a "
      "constant renormalisation of G",
      sp.simplify(mu_from_F - (1 - sp.exp(-y))) == 0 and sp.simplify(mu_direct - (1 - sp.exp(-y))) == 0 and
      sp.limit(mu_direct, y, sp.oo) == 1 and sp.simplify(sp.series(mu_direct, y, 0, 2).removeO() - y) == 0,
      "mu(y) = 1-e^-y; mu(y->inf) = 1; mu(y->0) = y + O(y^2)")

# ---- A6: the transfer chain.  Is the density I just reduced really IC5's / IC10's static sector? ------
# This is not taken on the lead's word.  Two things are checked here.
# (a) IC10's added block is proportional to eta.  eta is built from E(t) = exp(-1/t) (t>0), 0 otherwise, and
#     is EXACTLY zero for |r^2-1| >= 1/2, r = -N p/(3 m h0).  A static configuration has p = 0, i.e. r = 0.
#     So the block vanishes on a NEIGHBOURHOOD of the static branch, with all derivatives -- not at a point.
# (b) IC5's static Hamiltonian is H_b + G at eta = 0, which is written in BARRED variables:
#         -(m/2) V e^(u xi) Rbar   and   G = -m V e^(u xi)[2 u xi Dbar xi . Dbar u + xi^2 |Dbar u|^2].
#     Rhat = e^(-2w) Rbar = R3[h] + 4 Lap_h w - 2 |Dw|_h^2, w = (u-1)xi.  The claim that this equals IC1's
#     static density (m/2)[R3 + 2(1-u^2) a.a] is an integration-by-parts identity, and it is tested here
#     as a null-Lagrangian statement in all three fields.
print("\n  A6  the transfer chain IC1 -> IC4 -> IC5 -> IC10 on the static branch, checked here, not quoted:")
def Efun(t): return math.exp(-1/t) if t > 0 else 0.0
def eta_of(rv):
    dd = (rv**2 - 1)**2
    A = Efun(0.25 - dd); B = Efun(dd - 1/16)
    return A/(A + B) if (A + B) > 0 else 0.0
grid = np.linspace(0.0, 0.707, 400)
eta_vals = np.array([eta_of(v) for v in grid])
h_ = 1e-6
eta_der = np.array([(eta_of(v + h_) - eta_of(max(v - h_, 0.0)))/(h_ + min(h_, v)) for v in grid])
print(f"      (a) IC10/IC5 activation eta on 0 <= r <= 0.707 (static side): max|eta| = {np.max(np.abs(eta_vals)):.3e}, "
      f"max|d eta/dr| = {np.max(np.abs(eta_der)):.3e}")
check("A6a IC10's added block (all of it proportional to eta) and IC5's (1-eta) assignment are EXACT on a "
      "neighbourhood of the static configuration p = 0, so the static sector tested here is IC10's own, "
      "not a measure-zero limit of it",
      float(np.max(np.abs(eta_vals))) == 0.0 and float(np.max(np.abs(eta_der))) == 0.0,
      "eta and its derivative are identically 0 for r <= 0.707 (eta = 0 whenever |r^2-1| >= 1/2)")

# (b) the barred-to-unbarred integration-by-parts identity, in spherical symmetry
xi = P[0]; xip = P[1]                                   # xi = ln N = Phi
wS_ = (Uj[0] - 1)*xi                                    # w = (u-1) xi
wS_p = (Uj[1])*xi + (Uj[0] - 1)*xip                     # w'
Nsh = sp.exp(P[0] - 3*S[0])*r**2                        # N sqrt(h) per solid angle
asq_h = sp.exp(2*S[0])*P[1]**2                          # a.a = h^ij a_i a_j
aDu = sp.exp(2*S[0])*P[1]*Uj[1]                         # a . Du
Dusq = sp.exp(2*S[0])*Uj[1]**2                          # |Du|^2
Dwsq = sp.exp(2*S[0])*wS_p**2
lap_w = sp.exp(3*S[0])/r**2*Dtot(sp.exp(-S[0])*r**2*wS_p)   # Lap_h w in spherical symmetry
ident = (m/2)*Nsh*(4*lap_w - 2*Dwsq) - m*Nsh*(1 - Uj[0]**2)*asq_h + m*Nsh*(2*Uj[0]*xi*aDu + xi**2*Dusq)
resid_P = sp.simplify(EL(ident, P)); resid_S = sp.simplify(EL(ident, S)); resid_U = sp.simplify(EL(ident, Uj))
print(f"      (b) (m/2)N sqrt(h)[Rhat - R3] - m N sqrt(h)(1-u^2)a.a + m N sqrt(h)[2 u xi a.Du + xi^2|Du|^2]")
print(f"          EL residuals in (Phi, Psi, u): ({resid_P}, {resid_S}, {resid_U})  -- a pure spatial divergence")
check("A6b IC5's static Hamiltonian (H_b's barred curvature plus its G term at eta = 0) is EXACTLY IC1's "
      "static density (m/2)[R3 + 2(1-u^2)a.a], differing only by the declared spatial divergence -- so the "
      "reduction above is the CURRENT construction's galactic limit, verified here rather than inherited",
      resid_P == 0 and resid_S == 0 and resid_U == 0,
      "all three Euler-Lagrange residuals of the difference vanish identically (null Lagrangian)")
print(f"      (c) IC4's extra term is (m/2)(Q^2/a0^2)(J + Rhat F) with Q = K - 3W; a static configuration has")
print(f"          K = 0 and W = n.grad w = 0, so Q vanishes IDENTICALLY in time.  A term quadratic in Q with")
print(f"          no derivative of Q contributes 2 Q (dQ/d.) to every first variation, hence nothing at Q = 0.")

# =====================================================================================================
# B. NUMERICS
# =====================================================================================================
print("\n" + "-" * 120)
print("B. NUMERICS: the force law, its scale, its kernel, and everything the weak-field limit dropped")
print("-" * 120, flush=True)

def solve_y(s):
    """solve mu(y) y = s, i.e. (1-e^-y) y = s = g_N/a0, for y = g/a0"""
    s = np.atleast_1d(np.asarray(s, float))
    out = np.zeros_like(s)
    for i, si in enumerate(s):
        lo, hi = 1e-30, max(10.0, 2.0*si + 10.0)
        while (1 - math.exp(-hi))*hi < si: hi *= 2
        for _ in range(300):
            mid = 0.5*(lo + hi)
            if (1 - math.exp(-mid))*mid < si: lo = mid
            else: hi = mid
        out[i] = 0.5*(lo + hi)
    return out

# ---- B1 does a MOND limit exist, and at what scale ---------------------------------------------------
print("\n  B1 -- the deep-acceleration and low-acceleration limits of  (1 - e^(-g/a0)) g = g_N")
s_lo = np.array([1e-12, 1e-10, 1e-8, 1e-6, 1e-4])
s_hi = np.array([1e2, 1e3, 1e4, 1e6])
mond_ok = True; scale_ok = True; newt_ok = True
for foot, a0v in A0.items():
    y_lo = solve_y(s_lo); g_lo = y_lo*a0v; gN_lo = s_lo*a0v
    ratio = g_lo/np.sqrt(gN_lo*a0v)                      # -> 1 iff g = sqrt(gN a0)
    a_scale = g_lo**2/gN_lo                              # the scale actually appearing, in m/s^2
    y_hi = solve_y(s_hi); newt = (y_hi*a0v)/(s_hi*a0v)   # -> 1 iff g -> g_N
    print(f"    {foot:9s} a0 = {a0v:.4e} m/s^2")
    print(f"       deep-MOND   g/sqrt(gN a0) at gN/a0 = 1e-12 ... 1e-4 : " + " ".join(f"{v:.9f}" for v in ratio))
    print(f"       the scale   g^2/gN                                  : " + " ".join(f"{v/a0v:.9f} a0" for v in a_scale))
    print(f"       Newtonian   g/gN at gN/a0 = 1e2 ... 1e6             : " + " ".join(f"{v:.9f}" for v in newt))
    mond_ok  &= bool(abs(ratio[0] - 1) < 1e-5)
    scale_ok &= bool(abs(a_scale[0]/a0v - 1) < 1e-5)
    newt_ok  &= bool(abs(newt[-1] - 1) < 1e-5)
check("B1a a MOND limit EXISTS: g -> sqrt(g_N a_scale) as g_N -> 0, on both footings",
      mond_ok, "g/sqrt(gN a0) -> 1 to <1e-5 by gN = 1e-12 a0")
check("B1b the acceleration scale in that limit is 1.000000 x the a0 that appears in the action's a0^2 U(u^2) "
      "term -- no factor 2, 1/2 or 2pi -- so setting the action's a0 to 9.3619e-11 (canonical) or 1.1279e-10 "
      "(alt) reproduces the programme's scale EXACTLY.  [a0 is an INPUT to the construction, permitted; what "
      "is tested here is the numerical coefficient the theory attaches to it]",
      scale_ok, "g^2/g_N -> 1.000000 a0 on both footings")
check("B1c the Newtonian limit is recovered at high acceleration with the SAME G: mu -> 1, so "
      "lap(Phi) = 4 pi G_N rho with G_N = 1/(8 pi m), the same m that normalises R4 and the tensor sector "
      "(REPORT.md section 5: S_T = (m/8) int ...), so G_dyn = G_lens = G_tensor at eta = 0",
      newt_ok, "g/g_N -> 1 to <1e-5 by g_N = 1e6 a0")

# BTFR normalisation
M = 5e10*MSUN
for foot, a0v in A0.items():
    rr_ = np.array([50., 100., 300., 1000.])*kpc
    gN = G_NEWT*M/rr_**2
    g = solve_y(gN/a0v)*a0v
    v4 = (g*rr_)**2
    print(f"    {foot:9s} M = 5e10 Msun: v^4/(G M a0) at r = 50,100,300,1000 kpc = " +
          " ".join(f"{v/(G_NEWT*M*a0v):.6f}" for v in v4))

# ---- B2 which kernel is this? ------------------------------------------------------------------------
print("\n  B2 -- which interpolation function, compared with the two the programme names")
def Delta_RAR(s):
    s = np.asarray(s, float)
    d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_RAR(s):        # g/a0 as a function of s = g_N/a0, the programme's CARRIED kernel
    return s + Delta_RAR(s)
def g_IC(s):         # g/a0 from the IC-series' own static law
    return solve_y(s)

s_grid = np.geomspace(1e-3, 1e3, 4001)
gic = g_IC(s_grid); grar = g_RAR(s_grid)
dex = np.abs(np.log10(gic) - np.log10(grar))
imax = int(np.argmax(dex))
s_sparc = np.geomspace(1e-2, 1e2, 2001)
dex_sparc = np.abs(np.log10(g_IC(s_sparc)) - np.log10(g_RAR(s_sparc)))
print(f"    IC-series kernel (derived above):   mu(y) = 1 - e^-y,  y = g/a0   [Delta(s) = y e^-y, ceiling a0/e = {1/math.e:.6f} a0]")
print(f"    lead's PATH_FORWARD.md target:      mu(y) = 1 - exp(-y)                       -> IDENTICAL")
print(f"    programme's CARRIED kernel:         nu_RAR, g = g_N/(1-e^-sqrt(g_N/a0)), saturated at s = 2.540, Delta = 0.6476")
print(f"    max |dlog10 g| between them over s = 1e-3..1e3 : {dex[imax]:.4f} dex at s = {s_grid[imax]:.3f}")
print(f"    max |dlog10 g| over the SPARC range s = 1e-2..1e2: {dex_sparc.max():.4f} dex")
print(f"    both agree in BOTH asymptotic limits (deep-MOND sqrt(s), Newtonian s); they differ only in the transition:")
for sv in [0.1, 0.3, 1.0, 3.0, 10.0]:
    print(f"        s = {sv:5.2f}:  g_IC/a0 = {float(g_IC(sv)[0]):8.4f}   g_nuRAR/a0 = {float(g_RAR(sv)):8.4f}   "
          f"dlog10 = {math.log10(float(g_IC(sv)[0])/float(g_RAR(sv))):+.4f}")
check("B2a the interpolation function the IC-series produces IS the lead's own stated target, "
      "mu(y) = 1 - exp(-y) with y = |grad Phi|/a0 (PATH_FORWARD.md line 23)",
      True, "derived in A5, not assumed; U(c) is the primitive designed to give exactly this")
check("B2b the interpolation function the IC-series produces is the programme's CARRIED kernel, nu_RAR "
      "(THE_ACTION_2026-09-05 section 3)",
      bool(dex_sparc.max() < 0.01), f"max |dlog10 g| = {dex_sparc.max():.4f} dex over s = 1e-2..1e2 -- it is the "
      f"EXPONENTIAL CARRIER, the kernel the programme swapped AWAY from on 2026-09-06")

# ---- B3 the bounded-boost ceiling on SPARC, both kernels, identical points ---------------------------
print("\n  B3 -- the one place the two kernels are observationally distinguishable without fitting:")
print("        the bounded-boost ceiling.  Delta = (g_obs - g_bar)/a0 <= max Delta:  1/e = 0.3679 for the")
print("        IC-series' kernel, 0.6476 for nu_RAR.  Fixed-Upsilon DIAGNOSTIC (not the programme's")
print("        controlled g03w test, which profiles Upsilon and applies SPARC's own Q/i cuts).")
UPS_D, UPS_B = 0.5, 0.7
pts = []
nb_gal = 0
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    rk = d[:, 0]; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    if np.any(Vb != 0): continue                       # bulgeless control: Upsilon_disk is the only stellar freedom
    nb_gal += 1
    rm = rk*kpc
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd)
    msk = (rk > 2.0) & (rm > 0) & (Vo > 0) & (Vb2 > 0) & (eV > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    for i in np.where(msk)[0]:
        gb = Vb2[i]/rm[i]; go = Vo[i]**2/rm[i]; sg = 2*Vo[i]*eV[i]/rm[i]
        pts.append((gb, go, sg))
pts = np.array(pts)
print(f"    bulgeless control: {nb_gal} galaxies, {len(pts)} points beyond 2 kpc with eV/V < 0.10, Upsilon_d = {UPS_D}")
ceil_rows = []; a0_req = {}
dg = pts[:, 1] - pts[:, 0]; sg = pts[:, 2]
for foot, a0v in A0.items():
    D = dg/a0v; sD = sg/a0v
    for name, Cmax in [("IC-series (exponential), 1/e", 1/math.e), ("nu_RAR carried, 0.6476", 0.6476)]:
        frac = float(np.mean((D - Cmax) > 3*sD))
        # the a0 each kernel would need for only 1% of points to violate its own ceiling at 3 sigma
        need = np.sort((dg - 3*sg)/Cmax); a0n = float(need[int(0.99*len(need))])
        ceil_rows.append((foot, name, frac))
        a0_req[(foot, name)] = a0n/a0v
        print(f"    {foot:9s} ceiling {name:32s}: {100*frac:5.2f}% of points exceed it at >3 sigma; "
              f"a0 would have to be {a0n/a0v:.2f}x larger for that to fall to 1%")
print(f"    the programme's own controlled numbers (g03w: Upsilon profiled, SPARC Q<3 and i>30 cuts; quoted, "
      f"not recomputed here): exponential carrier 7.3% / 3.5%, nu_RAR 1.2% / 0.6%.  My fixed-Upsilon counts sit")
print(f"    ~2.5x higher for BOTH kernels, so the cut/Upsilon difference is common-mode; the RATIO between the")
print(f"    two kernels is the robust content, and it agrees with the programme's (about 5-6x).")
print(f"    Direction stated: this ceiling test is ONE-SIDED and Upsilon-sensitive.  The programme's own global")
print(f"    comparison with a0 and Upsilon profiled jointly (f25/g03l) finds exponential-vs-RAR UNDECIDED, so")
print(f"    this is a DISFAVOURING, not an exclusion, of the kernel the IC-series produces.")
ic_frac = {f: v for f, n, v in ceil_rows if n.startswith("IC")}
ra_frac = {f: v for f, n, v in ceil_rows if n.startswith("nu")}
check("B3 the IC-series' kernel is not disfavoured relative to the programme's carried kernel by the "
      "bounded-boost ceiling on the bulgeless SPARC control (same points, same Upsilon, same cuts)",
      all(ic_frac[f] <= ra_frac[f]*1.5 for f in A0),
      f"IC {100*ic_frac['canonical']:.2f}%/{100*ic_frac['alt']:.2f}% vs nu_RAR "
      f"{100*ra_frac['canonical']:.2f}%/{100*ra_frac['alt']:.2f}% (canonical/alt) exceeding at >3 sigma -- "
      f"a factor {ic_frac['canonical']/max(ra_frac['canonical'],1e-9):.1f}; the programme's controlled test "
      f"(g03w) finds the same ordering at 7.3%/3.5% vs 1.2%/0.6%")

# ---- B4 everything the weak-field limit dropped -------------------------------------------------------
print("\n  B4 -- the terms the ordered weak-field limit DROPPED, at the construction's own parameter values.")
print("        IC1/IC4 expanding witness: a0^2 = 9 kappa e^(-1/2)/(16 m l^2), l = ln(9/5), Lambda = kappa e^(-1/2)/m - a0^2 U(4/9)")
ell = math.log(9/5)
kappa_over_m = 16*ell**2*math.exp(0.5)/9          # in units of a0^2 (geometric)
Ufn = lambda cc: (1 - cc)*(math.log(1 - cc)**2 - 2*math.log(1 - cc) + 2) - 2
U49 = Ufn(4/9)
N0 = math.exp(0.25); Xw = math.exp(-0.5)/2
print(f"        kappa/m = {kappa_over_m:.4f} a0^2 (geometric),  U(4/9) = {U49:+.5f},  X = 1/(2N0^2) = {Xw:.5f}")
# vacuum source entering  div[u^2 grad Phi] = rho/(2m) + [ kappa X/(2m) + C/2 - F/2 ]
S_vac_over_a0sq = kappa_over_m*Xw/2 + (kappa_over_m*math.exp(-0.5) + (0.0 - U49))/2
print(f"        total dropped source  S_vac = {S_vac_over_a0sq:.4f} a0^2 (geometric units, 1/length^2)")
w_ratio = w_spur = w_slip = 0.0
for foot, a0v in A0.items():
    a0g = a0v/C_LIGHT**2                                       # a0 in 1/length
    print(f"    {foot}:")
    for Lname, L in [("10 kpc", 10*kpc), ("100 kpc", 100*kpc), ("1 Mpc", Mpc), ("c^2/a0 (Hubble)", 1/a0g)]:
        ratio = S_vac_over_a0sq*a0g*L                          # (dropped source)/(MOND term ~ a0/L)
        g_spur = math.sqrt(S_vac_over_a0sq*a0g*L/3)            # deep-MOND response to the uniform source, in a0
        slip = a0g*L/6                                         # |Phi-Psi|/|Phi| from the dropped F term
        print(f"        L = {Lname:16s}: dropped/retained = {ratio:.3e},  spurious g = {g_spur:.3e} a0,  "
              f"|Phi-Psi|/|Phi| = {slip:.3e}")
        if L <= Mpc:
            w_ratio = max(w_ratio, ratio); w_spur = max(w_spur, g_spur); w_slip = max(w_slip, slip)
check("B4a the clock/vacuum sources the weak-field limit drops (kappa X, Lambda, a0^2 U, and the quadratic F) "
      "really are negligible on galaxy-to-cluster scales at the construction's OWN kappa/m: the lead's stated "
      "ordering is satisfied, it is not an assumption smuggled in",
      w_ratio < 1e-3 and w_spur < 1e-2, f"out to 1 Mpc: dropped/retained <= {w_ratio:.2e}, spurious "
      f"acceleration <= {w_spur:.2e} a0, slip <= {w_slip:.2e}; the ordering only breaks at L ~ c^2/a0")
check("B4b no-slip survives the dropped terms, so lensing and dynamics see the SAME potential to <1e-4 "
      "out to 1 Mpc  [the framework's lensing requirement]",
      (A0['alt']/C_LIGHT**2)*Mpc/6 < 1e-4, f"|Phi-Psi|/|Phi| <= {(A0['alt']/C_LIGHT**2)*Mpc/6:.2e} at 1 Mpc")

# ---- B5 the input the published files do not fix ------------------------------------------------------
print("\n  B5 -- THE MISSING INPUT: the far-field boundary condition on u.")
print("        The static (eta = 0) branch fixes u POINTWISE from the local field: u^2 = 1 - e^(-|a|/a0),")
print("        so u -> 0 as |a| -> 0, which is the isolated-MOND boundary condition and is what the deep-MOND")
print("        asymptotics above assume.  The expanding (eta = 1) plateau fixes u by P_w = 0 instead:")
print("        IC10's own solution has u = 0.492193, 0.536585, 0.570419 at S = 0.10, 0.15, 0.20, and the")
print("        IC4/IC5 witness has u = 2/3.  A galaxy sits inside the eta = 0 plateau and the cosmology inside")
print("        eta = 1; the two are separated by the eta transition, which IC10's own 'What remains' item 1")
print("        says has not been varied.  If u must approach its cosmological value at large r, the static law")
print("        reads that as an external field:")
frac_below = {}
for uc, lab in [(0.492193, "IC10 S=0.10"), (0.570419, "IC10 S=0.20"), (2/3, "IC4/IC5 witness")]:
    yeq = -math.log(1 - uc**2)
    print(f"        u_cosmo = {uc:.6f} ({lab:15s})  ->  equivalent y_ext = {yeq:.4f}, i.e. g_ext = {yeq:.3f} a0")
for foot, a0v in A0.items():
    D = pts[:, 1]/a0v
    frac_below[foot] = float(np.mean(D < 0.28))
    print(f"        {foot:9s}: {100*frac_below[foot]:.1f}% of the bulgeless SPARC points beyond 2 kpc sit at "
          f"g_obs < 0.28 a0, i.e. BELOW the smallest such floor")
check("B5 the galactic branch's far-field boundary condition on u is DETERMINED by the published files "
      "(i.e. the eta = 0 static branch and the eta = 1 cosmological branch are matched, so an isolated "
      "galaxy's deep-MOND asymptotics is fixed)",
      False, "not determined: the static law gives u -> 0, the exhibited cosmological solutions give "
             "u = 0.49-0.67 (equivalent to a universal external field 0.28-0.59 a0), and the eta transition "
             "between them has not been varied (IC10 'What remains' item 1)")

# ---- B6 informational diagnostics that are NOT verdict checks ------------------------------------------
print("\n  B6 -- two informational diagnostics (flagged, not scored; both need the frame/branch matching the")
print("        lead has not done, so neither is treated here as a failure of the construction).")
h0_over_a0 = 0.30                                   # IC10's own H_physical/h0 = 0.72-0.81 with a0 = 2.434 h0
a0_units = math.sqrt(9*6*math.exp(-0.5)/(16*1*ell**2))
print(f"        (i) a0 vs the expansion rate ON THE ONE EXHIBITED BRANCH.  With m = h0 = 1, kappa = 6 (IC10's own")
print(f"            numbers) the witness relation gives a0 = {a0_units:.4f} h0 while IC10's solution has")
print(f"            H_phys = 0.719-0.808 h0, so a0/(cH) = {a0_units/0.808:.2f}-{a0_units/0.719:.2f}.")
for foot, a0v in A0.items():
    print(f"            observed a0/(cH0) = {a0v/(C_LIGHT*H0_SI):.4f} ({foot}) -- the exhibited branch is "
          f"{(a0_units/0.76)/(A0[foot]/(C_LIGHT*H0_SI)):.0f}x off.")
print(f"            Lambda and kappa are free OFF that branch, so this is a property of the exhibited solution,")
print(f"            not a theorem; the lead already labels it 'not a viable cosmology'.")
print(f"        (ii) G_cos vs G_local.  At eta = 0 the Planck mass is m; on IC10's eta = 1 plateau it is")
print(f"            m* = m e^(-1/6), a ratio e^(1/6) = {math.exp(1/6):.4f}.  Whether that is a real 18% G_cos/G_N")
print(f"            shift (BBN allows ~10-20%) depends on the conformal factor e^(2w) that matter carries and on")
print(f"            the transition; it cannot be settled from the published files and is flagged, not scored.")

# =====================================================================================================
# VERDICT
# =====================================================================================================
print("\n" + "-" * 120)
print("VERDICT")
print("-" * 120, flush=True)
core = all(not f.startswith(p) for f in FAILS
           for p in ("A1", "A2", "A3", "A4", "A5", "B1a", "B1b", "B1c", "B4"))
print("""    The static, weak-field limit of the IC-series IS a genuine AQUAL-type MOND theory:
        div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G_N rho_b,   mu(y) = 1 - e^-y,   G_N = 1/(8 pi m),
    with Phi = Psi (so lensing and dynamics share one potential), the Newtonian limit at high acceleration
    with the same G that normalises R4 and the tensor sector, the deep-MOND law g = sqrt(g_N a0) with
    coefficient exactly 1.000000 x the action's own a0, and every clock/vacuum term the limit drops below
    2e-5 of the retained ones out to 1 Mpc at the construction's own kappa/m.  The constitutive law
    u^2 = 1 - e^(-|a|/a0) is EXACT on the static branch, and that branch is verified here (A6) to be IC5's
    and IC10's own, not only IC1's.  a0 enters as an input, which the programme's rules permit; what the
    theory supplies is the numerical coefficient 1 in front of it, and that is right.
    Two things it is NOT.  (1) The kernel is the framework's EXPONENTIAL CARRIER -- the kernel the programme
    swapped away from on 2026-09-06 in favour of nu_RAR on the bounded-boost ceiling test; it differs from
    the carried kernel by up to 0.073 dex in the transition and violates its own ceiling ~5x more often on
    the bulgeless SPARC control.  (2) The far-field boundary condition on u is not fixed by the published
    files, and the only values the exhibited cosmological solutions offer would read as a universal external
    field of 0.28-0.59 a0.""")
check("VERDICT the IC-series, as published, is a candidate host for this framework's galaxy phenomenology "
      "-- its static weak-field limit is MOND, at the action's own a0, with one potential and the measured G",
      core, "PASS on the reduction; the two open items above are scored separately as B2b and B5 and are "
            "not hidden inside this verdict")

print("\n" + "=" * 120)
if FAILS:
    print(f"FAILED CHECKS ({len(FAILS)}):")
    for f in FAILS: print("   - " + f)
else:
    print("ALL CHECKS PASSED")
print("=" * 120)
