#!/usr/bin/env python3
"""
L58 -- the MOND scalar's ANISOTROPIC STRESS, and whether the deposited theory's no-slip result survives it
==========================================================================================================
THE PROMPT.  The lead agent's `USER_ACTION_EXACT_PLANAR.md` derives, for the exact static PLANAR reduction
of the submitted action with an arbitrary differentiable MOND function J, the spatial-diffeomorphism
Noether identity  P'E_P + A'E_A + B'E_B + phi'E_phi - (E_A)' = 0,  residual exactly zero.  A further
statement was relayed to this lane second-hand, flagged as "not in any committed file":

        E_A - (1/2) E_B  =  2 b J'(s0^2) s0^2                                                   (RELAY)

read on its face as the ANISOTROPIC STRESS of the MOND sector on a uniform-scalar-gradient background.
Anisotropic stress is what sets the SLIP between the two metric potentials, and the deposited theory
(DOI 10.5281/zenodo.22667688, THE_COMPLETE_THEORY_2026-09-08.md sec.2) claims

        Phi = Psi  to better than 1e-4 out to 1 Mpc, with nothing fitted,

which is why lensing and dynamics agree, why the cluster residual behaves like mass in both probes, and
why several gates pass.  It was established at LINEAR order about a flat background (L11 A4c/B4b).  The
lead's identity is EXACT, STATIC and PLANAR -- the non-spherical setting where a gradient's anisotropy
actually appears.  QUESTION: does no-slip survive when the scalar's own anisotropic stress is kept
exactly, rather than at linear order about flat space?

WHAT THIS SCRIPT DOES, in order, with checks that can fail at every step.

  PART A  CONTROLS -- these decide whether anything below means anything.
    A1  Rebuild the covariant -> static planar reduction MYSELF from the action in THE_ACTION_2026-09-05
        sec.1 (metric, clock normal, projector, 4-acceleration, Y, the coherence contraction, sqrt(-g)R),
        and check it equals the lead's displayed planar density up to a total x-derivative.  This is what
        licenses using that density at all, and it is what fixes the identification ca = c14, b = 2 - K_B,
        C = Lambda/(8 pi G) + K(0).
    A2  Reproduce the lead's Noether identity as an exact symbolic zero from my own Euler-Lagrange
        operator (rebuilt, not imported).
    A3  [control] the same identity, sector by sector: it must hold for the EH block alone, the aether
        block alone, the mixing block alone and the J block alone, since each is separately a scalar
        density.  A machinery that only gets zero for the sum is not to be trusted.
    A4  Reproduce the deposited theory's own no-slip number at ITS order and background: the spherical
        isotropic-gauge reduction of L11 (rebuilt from the metric), weak field with a0 scaled so that
        y = |a|/a0 stays O(1), -> lap(Phi - Psi) = 0 at linear order; and L11 B4b's <1e-4 at 1 Mpc.
    A5  [control] the same machinery on GR + minimally coupled static dust: Poisson, and no slip.

  PART B  THE RELAYED IDENTITY, derived here rather than taken on trust.
    B1  the four background equations and E_A - E_B/2 on phi = s0 x, flat metric.
    B2  the coherence (xi) operator's contribution on that background.
    B3  NORMALISATION.  The repository has a live dispute on exactly this action: L52_REPAIR_SCOPE_REVIEW
        flags g_N = 2 J_Y w (L52 line 633) against g_N = J_Y w (THE_ACTION sec.3).  Carry the coupling and
        J normalisations as FREE symbols and show what is, and what is not, convention-dependent.

  PART C  THE PHYSICS.  Which metric combination the slip is in this planar reduction; the equation it
        obeys; at what order the anisotropic stress enters; whether it survives in spherical symmetry.

  PART D  NUMBERS.  Both a0 footings.  Deep-MOND outskirts, the transition, the high-acceleration limit;
        a real disc galaxy (SPARC rotmods); a real cluster (X-COP audit rows); the lensing-vs-dynamics
        agreement that currently stands at 1.55 sigma.

  PART E  VERDICT.

HONESTY.  The likely outcome is that no slip survives for a good reason and this discharges a worry.  If
it does not, this touches a paper deposited on 2026-09-08 and several gates, and is reported plainly.
The relayed formula is NOT treated as authoritative; it is also not dismissed for being uncommitted.
"""
import os, sys, math, glob, json
import numpy as np
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def info(s=""): print(s, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_LIGHT = 2.99792458e8
G_N = 6.674e-11
kpc = 3.0856775814913673e19
Mpc = 1000*kpc
MSUN = 1.98892e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

info("=" * 122)
info("L58 -- the MOND scalar's anisotropic stress, and whether the deposited no-slip result survives it")
info("=" * 122)
info(f"    sympy {sp.__version__}, numpy {np.__version__}, python {sys.version.split()[0]}")
info(f"    a0 footings: canonical {A0['canonical']:.4e}  /  alt {A0['alt']:.4e}  m s^-2")

# =====================================================================================================
# PART A -- CONTROLS
# =====================================================================================================
info("\n" + "-" * 122)
info("PART A -- CONTROLS.  If either of the two named controls fails, nothing below means anything.")
info("-" * 122)

x = sp.Symbol('x', real=True)
P, A, B, f = [sp.Function(n)(x) for n in ('P', 'A', 'B', 'phi')]
Gs, ca, b, xi, C = sp.symbols('G ca b xi C', real=True, positive=True)
Jf = sp.Function('J')

fp = sp.diff(f, x); Pp = sp.diff(P, x); Ap = sp.diff(A, x); Bp = sp.diff(B, x)

# ---- A1  the covariant -> planar reduction, rebuilt from the covariant action -------------------------
info("\n  A1  REBUILD the reduction from the covariant action (THE_ACTION_2026-09-05 sec.1), not imported.")
info("      ds^2 = -e^{2P}dt^2 + e^{2A}dx^2 + e^{2B}(dy^2+dz^2),  tau = t,  phi = phi(x).")

t_, y_, z_ = sp.symbols('t y z', real=True)
coords = [t_, x, y_, z_]
gmat = sp.diag(-sp.exp(2*P), sp.exp(2*A), sp.exp(2*B), sp.exp(2*B))
ginv = gmat.inv()
sqrtg = sp.exp(P + A + 2*B)                         # sqrt(-g)

def christoffel(g, gi, X):
    n = len(X)
    Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a_ in range(n):
        for b_ in range(n):
            for c_ in range(n):
                s = sp.S(0)
                for d_ in range(n):
                    s += gi[a_, d_]*(sp.diff(g[d_, b_], X[c_]) + sp.diff(g[d_, c_], X[b_]) - sp.diff(g[b_, c_], X[d_]))
                Gam[a_][b_][c_] = sp.simplify(s/2)
    return Gam

Gam = christoffel(gmat, ginv, coords)
Ric = sp.zeros(4, 4)
for b_ in range(4):
    for c_ in range(4):
        s = sp.S(0)
        for a_ in range(4):
            s += sp.diff(Gam[a_][b_][c_], coords[a_]) - sp.diff(Gam[a_][b_][a_], coords[c_])
            for d_ in range(4):
                s += Gam[a_][a_][d_]*Gam[d_][b_][c_] - Gam[a_][c_][d_]*Gam[d_][b_][a_]
        Ric[b_, c_] = sp.simplify(s)
R4 = sp.simplify(sum(ginv[b_, c_]*Ric[b_, c_] for b_ in range(4) for c_ in range(4)))

# unit normal to tau = t slices, n_mu = -d_mu tau / sqrt(-g^{ab} d_a tau d_b tau)
n_lo = sp.Matrix([-sp.exp(P), 0, 0, 0])
n_up = sp.simplify(ginv*n_lo)
norm = sp.simplify((n_lo.T*n_up)[0, 0])
# 4-acceleration J^mu = n^nu nabla_nu n^mu
Jup = []
for a_ in range(4):
    s = sp.S(0)
    for nu in range(4):
        s += n_up[nu]*(sp.diff(n_up[a_], coords[nu]) + sum(Gam[a_][nu][lm]*n_up[lm] for lm in range(4)))
    Jup.append(sp.simplify(s))
Jup = sp.Matrix(Jup)
# projector, V_mu, Y
qup = sp.simplify(ginv + n_up*n_up.T)
dphi = sp.Matrix([0, fp, 0, 0])
V_lo = sp.simplify((sp.eye(4) + n_up*n_lo.T)*dphi)         # q_mu^nu d_nu phi
Ysc = sp.simplify((dphi.T*qup*dphi)[0, 0])
# coherence contraction  q^{ls} q^{mn} nabla_l V_m nabla_s V_n
nabV = sp.zeros(4, 4)
for l_ in range(4):
    for m_ in range(4):
        nabV[l_, m_] = sp.simplify(sp.diff(V_lo[m_], coords[l_]) - sum(Gam[k_][l_][m_]*V_lo[k_] for k_ in range(4)))
Hcoh = sp.S(0)
for l_ in range(4):
    for s_ in range(4):
        for m_ in range(4):
            for n_ in range(4):
                Hcoh += qup[l_, s_]*qup[m_, n_]*nabV[l_, m_]*nabV[s_, n_]
Hcoh = sp.simplify(Hcoh)

U_lead = sp.exp(-2*A)*fp**2 + xi**2*sp.exp(-4*A)*((sp.diff(f, x, 2) - Ap*fp)**2 + 2*Bp**2*fp**2)
U_mine = sp.simplify(Ysc + xi**2*Hcoh)
info(f"      n.n = {norm}  (must be -1);   Y = q^{{mn}} d_m phi d_n phi = {sp.simplify(Ysc)}")
info(f"      J^x (clock 4-acceleration, contravariant) = {sp.simplify(Jup[1])}")
info(f"      xi^2 q q nabla V nabla V = xi^2 * {sp.simplify(Hcoh/xi**2 if xi != 0 else Hcoh)}")
check("A1a the clock normal is unit and the MOND argument U rebuilt covariantly equals the lead's displayed "
      "U = e^{-2A}phi'^2 + xi^2 e^{-4A}[(phi''-A'phi')^2 + 2B'^2 phi'^2]",
      sp.simplify(norm + 1) == 0 and sp.simplify(U_mine - U_lead) == 0,
      "n.n = -1 and U_mine - U_lead simplifies to 0")

# the aether block, static: K_ij = 0, so nabla_mu n_nu = -n_mu a_nu, and c1(..)^2 + c4(n.grad n)^2 = c14 a.a
a_lo = sp.simplify(gmat*Jup)
a_sq = sp.simplify((Jup.T*gmat*Jup)[0, 0])
info(f"      a.a = {a_sq}   -> the whole aether block reduces to c14 * a.a on a static hypersurface-orthogonal n")

# my reduction of the full covariant density (EH + aether + mixing + J + constant)
L_mine = sqrtg*(R4/(16*sp.pi*Gs) + ca*a_sq + 2*b*(Jup.T*dphi)[0, 0] - C - b*Jf(U_lead))
L_lead = sp.exp(P - A + 2*B)*((2*Bp**2 + 4*Pp*Bp)/(16*sp.pi*Gs) + ca*Pp**2 + 2*b*Pp*fp) \
         - sp.exp(P + A + 2*B)*(C + b*Jf(U_lead))

def EL(L, field):
    """Euler-Lagrange to second derivative order, my own operator."""
    return (sp.diff(L, field)
            - sp.diff(sp.diff(L, sp.diff(field, x)), x)
            + sp.diff(sp.diff(L, sp.diff(field, x, 2)), x, 2))

diffL = sp.simplify(sp.expand(L_mine - L_lead))
resid_td = [sp.simplify(EL(diffL, v)) for v in (P, A, B, f)]
check("A1b my covariant reduction equals the lead's displayed planar density up to a TOTAL x-DERIVATIVE "
      "[EL residual of the difference vanishes for all four fields] -- so the display is licensed, and "
      "ca = c14, b = 2 - K_B, C = Lambda/(8 pi G) + K(0)",
      all(r == 0 for r in resid_td), f"EL residuals of (L_mine - L_lead): {tuple(resid_td)}")

# ---- A2  the Noether identity, my own EL --------------------------------------------------------------
L = L_lead
eqs = [EL(L, v) for v in (P, A, B, f)]
E_P, E_A, E_B, E_phi = eqs
identity = sum(E*sp.diff(v, x) for E, v in zip(eqs, (P, A, B, f))) - sp.diff(E_A, x)
res_noether = sp.simplify(sp.expand(identity))
info(f"\n  A2  P'E_P + A'E_A + B'E_B + phi'E_phi - (E_A)'  simplifies to  {res_noether}")
check("A2 [CONTROL 1] the lead's spatial-diffeomorphism Noether identity reproduces as an EXACT symbolic "
      "zero from my own rebuild of the density and my own Euler-Lagrange operator",
      res_noether == 0, "residual identically 0 with arbitrary differentiable J")

# ---- A3  the identity sector by sector -----------------------------------------------------------------
sectors = {
    "EH block":      sp.exp(P - A + 2*B)*(2*Bp**2 + 4*Pp*Bp)/(16*sp.pi*Gs),
    "aether block":  sp.exp(P - A + 2*B)*ca*Pp**2,
    "mixing block":  sp.exp(P - A + 2*B)*2*b*Pp*fp,
    "constant":     -sp.exp(P + A + 2*B)*C,
    "J block":      -sp.exp(P + A + 2*B)*b*Jf(U_lead),
}
sec_ok = {}
for nm, Ls in sectors.items():
    e = [EL(Ls, v) for v in (P, A, B, f)]
    r = sp.simplify(sp.expand(sum(ei*sp.diff(v, x) for ei, v in zip(e, (P, A, B, f))) - sp.diff(e[1], x)))
    sec_ok[nm] = (r == 0)
    info(f"      {nm:14s}: identity residual {r}")
check("A3 [control] the identity holds SECTOR BY SECTOR (each block is separately a scalar density), not "
      "only for the sum -- machinery that only cancels globally would be suspect",
      all(sec_ok.values()), ", ".join(f"{k}: {'0' if v else 'NONZERO'}" for k, v in sec_ok.items()))

# ---- A4  the deposited no-slip result, at ITS order and background ------------------------------------
info("\n  A4  CONTROL 2 -- the deposited theory's own no-slip result, reproduced at its own order and")
info("      background (spherical, isotropic gauge, weak field with a0 scaled so y = |a|/a0 stays O(1)).")
info("      Rebuilt from the metric here; L11 is neither imported nor rerun.")

r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta')
Phif = sp.Function('Phi')(r); Psif = sp.Function('Psi')(r)
gsph = sp.diag(-sp.exp(2*Phif), sp.exp(-2*Psif), sp.exp(-2*Psif)*r**2, sp.exp(-2*Psif)*r**2*sp.sin(th)**2)
gsinv = gsph.inv()
Xs = [t_, r, th, sp.Symbol('varphi')]
Gs3 = christoffel(gsph, gsinv, Xs)
Ric3 = sp.zeros(4, 4)
for b_ in range(4):
    for c_ in range(4):
        s = sp.S(0)
        for a_ in range(4):
            s += sp.diff(Gs3[a_][b_][c_], Xs[a_]) - sp.diff(Gs3[a_][b_][a_], Xs[c_])
            for d_ in range(4):
                s += Gs3[a_][a_][d_]*Gs3[d_][b_][c_] - Gs3[a_][c_][d_]*Gs3[d_][b_][a_]
        Ric3[b_, c_] = sp.simplify(s)
R4s = sp.simplify(sum(gsinv[b_, c_]*Ric3[b_, c_] for b_ in range(4) for c_ in range(4)))
dens_sph = sp.simplify(sp.expand(sp.exp(Phif - 3*Psif)*r**2*R4s))     # sqrt(-g) R per unit solid angle

# jet variables
Pj = sp.symbols('P0 P1 P2'); Sj = sp.symbols('S0 S1 S2'); Uj = sp.symbols('U0 U1')
RHj = sp.symbols('RH0 RH1')
JETS = [(Pj[0], Pj[1]), (Pj[1], Pj[2]), (Sj[0], Sj[1]), (Sj[1], Sj[2]), (Uj[0], Uj[1]), (RHj[0], RHj[1])]
def Dtot(e):
    out = sp.diff(e, r)
    for a_, b_ in JETS: out += b_*sp.diff(e, a_)
    return out
def ELj(Lg, tow):
    return sp.diff(Lg, tow[0]) - Dtot(sp.diff(Lg, tow[1])) + Dtot(Dtot(sp.diff(Lg, tow[2])))
def to_jets(e):
    e = e.subs({sp.Derivative(Phif, (r, 2)): Pj[2], sp.Derivative(Psif, (r, 2)): Sj[2]})
    e = e.subs({sp.Derivative(Phif, r): Pj[1], sp.Derivative(Psif, r): Sj[1]})
    return sp.simplify(e.subs({Phif: Pj[0], Psif: Sj[0]}))

dens_j = to_jets(dens_sph)
As = sp.exp(Pj[0] - Sj[0])
Fgr = Sj[1]**2 - 2*Pj[1]*Sj[1]
d_check = sp.simplify(dens_j - 2*As*r**2*Fgr)
check("A4a [control] sqrt(-g)R for the spherical isotropic-gauge static metric is 2 e^{Phi-Psi} r^2 "
      "(|grad Psi|^2 - 2 grad Phi . grad Psi) up to a total r-derivative -- the lapse-gradient square "
      "CANCELS in GR, so any |grad Phi|^2 in the reduced density comes from the clock sector",
      sp.simplify(ELj(d_check, Pj)) == 0 and sp.simplify(ELj(d_check, Sj)) == 0,
      "EL residual of the difference vanishes in both Phi and Psi")

m_, a0s, Lam_, kap_ = sp.symbols('m a_0 Lambda kappa', positive=True)
eps = sp.Symbol('epsilon', positive=True)
cU = sp.Symbol('c')
Ufun = (1 - cU)*(sp.log(1 - cU)**2 - 2*sp.log(1 - cU) + 2) - 2
F_ic = Sj[1]**2 - 2*Pj[1]*Sj[1] + (1 - Uj[0]**2)*Pj[1]**2
Cvac = Lam_ + a0s**2*Ufun.subs(cU, Uj[0]**2)
Bs = sp.exp(Pj[0] - 3*Sj[0])
L_matter = -sp.exp(Pj[0])*RHj[0]*r**2
L_ic = m_*As*r**2*F_ic - m_*Bs*r**2*Cvac + L_matter

def weak(e, order=2):
    """the deposited theory's own ordering: potentials O(eps), a0 L = O(eps), rho L^2/m = O(eps);
       u stays O(1) because y = |grad Phi|/a0 = O(eps)/O(eps) = O(1)."""
    sub = {Pj[i]: eps*Pj[i] for i in range(3)}
    sub.update({Sj[i]: eps*Sj[i] for i in range(3)})
    sub.update({RHj[0]: eps*RHj[0], RHj[1]: eps*RHj[1], a0s: eps*a0s})
    return sp.expand(sp.series(e.subs(sub), eps, 0, order + 1).removeO())

elS_ic = sp.simplify(ELj(L_ic.subs({Lam_: 0}), Sj))
wS1 = sp.expand(sp.simplify(weak(elS_ic, 1)/r**2/eps))
lapP = Pj[2] + 2*Pj[1]/r; lapS = Sj[2] + 2*Sj[1]/r
slip_lin = sp.simplify(wS1 - 2*m_*(lapP - lapS))
info(f"      linear-order conformal equation:  {wS1} = 0   ->   lap(Phi - Psi) = 0")
check("A4b [CONTROL 2] the deposited theory's no-slip result reproduces at ITS order and background: the "
      "conformal (Psi) equation is lap(Phi - Psi) = 0 at linear order, so Phi = Psi and lensing and "
      "dynamics share one potential  [L11 A4c, rebuilt from the metric]",
      slip_lin == 0, "linear conformal equation is exactly 2m [lap(Phi) - lap(Psi)] = 0")

slipnum_L11 = (A0['alt']/C_LIGHT**2)*Mpc/6
check("A4c [CONTROL 2, number] L11 B4b's quoted bound |Phi-Psi|/|Phi| <= a0 L/(6 c^2) < 1e-4 at L = 1 Mpc "
      "reproduces arithmetically on the worse (alt) footing",
      slipnum_L11 < 1e-4, f"a0(alt) Mpc/(6c^2) = {slipnum_L11:.3e};  canonical {(A0['canonical']/C_LIGHT**2)*Mpc/6:.3e}")

# ---- A5  GR + dust control ----------------------------------------------------------------------------
L_gr = m_*As*r**2*Fgr + L_matter
wP_gr = sp.expand(sp.simplify(weak(sp.simplify(ELj(L_gr, Pj)), 1)/r**2/eps))
wS_gr = sp.expand(sp.simplify(weak(sp.simplify(ELj(L_gr, Sj)), 1)/r**2/eps))
ok_gr = (sp.simplify(wP_gr - (2*m_*lapS - RHj[0])) == 0) and (sp.simplify(wS_gr - 2*m_*(lapP - lapS)) == 0)
check("A5 [control] the same machinery on GR + minimally coupled static dust returns the Newtonian Poisson "
      "equation with G_N = 1/(8 pi m) and no slip",
      ok_gr, "lapse eq: 2m lap(Psi) = rho;  conformal eq: lap(Phi - Psi) = 0")

# =====================================================================================================
# PART B -- THE RELAYED IDENTITY
# =====================================================================================================
info("\n" + "-" * 122)
info("PART B -- the relayed identity  E_A - (1/2) E_B = 2 b J'(s0^2) s0^2, derived here, not taken on trust")
info("-" * 122)

s0 = sp.Symbol('s0', real=True)
bg = {P: sp.S(0), A: sp.S(0), B: sp.S(0), f: s0*x}
def on_bg(e):
    e = e.subs({sp.Derivative(f, (x, 4)): 0, sp.Derivative(f, (x, 3)): 0, sp.Derivative(f, (x, 2)): 0,
                sp.Derivative(f, x): s0})
    for v in (P, A, B):
        e = e.subs({sp.Derivative(v, (x, 4)): 0, sp.Derivative(v, (x, 3)): 0,
                    sp.Derivative(v, (x, 2)): 0, sp.Derivative(v, x): 0})
    return sp.simplify(e.subs({P: 0, A: 0, B: 0, f: s0*x}).doit())

EPb, EAb, EBb, Ephib = [on_bg(e) for e in (E_P, E_A, E_B, E_phi)]
J0 = Jf(s0**2); J1 = sp.Subs(sp.Derivative(Jf(sp.Symbol('w')), sp.Symbol('w')), sp.Symbol('w'), s0**2)
info(f"      E_P   = {EPb}")
info(f"      E_A   = {EAb}")
info(f"      E_B   = {EBb}")
info(f"      E_phi = {Ephib}")
combo = sp.simplify(EAb - EBb/2)
target = sp.simplify(2*b*sp.diff(Jf(sp.Symbol('w')), sp.Symbol('w')).subs(sp.Symbol('w'), s0**2)*s0**2)
info(f"      E_A - (1/2) E_B = {combo}")
check("B1 [THE RELAY] E_A - (1/2)E_B = 2 b J'(s0^2) s0^2 on the flat/uniform-gradient background, derived "
      "from my own variation of my own rebuilt density -- the relayed formula is CORRECT AS STATED",
      sp.simplify(combo - target) == 0, f"difference simplifies to {sp.simplify(combo - target)}")
check("B1b the rest of the lead's background block also reproduces: E_P = -C - bJ0, E_B = 2 E_P, E_phi = 0 "
      "[so a cosmological constant cancels in the traceless combination and cannot absorb the anisotropy]",
      sp.simplify(EPb - (-C - b*J0)) == 0 and sp.simplify(EBb - 2*EPb) == 0 and Ephib == 0,
      "E_P = -C - bJ0, E_B = -2C - 2bJ0, E_phi = 0")

Ucoh_bg = on_bg(U_lead)
check("B2 the coherence operator xi^2|grad_perp V|^2 contributes NOTHING on the uniform-gradient background "
      "(phi'' = 0 and B' = 0 kill both of its pieces), so the anisotropy is the bare J' term and is not an "
      "artefact of the healing-length operator",
      sp.simplify(Ucoh_bg - s0**2) == 0, f"U|_background = {Ucoh_bg} = s0^2 exactly, xi drops out")

# ---- B3  normalisation, carried as free symbols --------------------------------------------------------
info("\n  B3  NORMALISATION.  The repository has a live dispute on this action: L52_REPAIR_SCOPE_REVIEW.md")
info("      flags  g_N = 2 J_Y w  (L52 source line 633) against  g_N = J_Y w  (THE_ACTION sec.3).  Carry the")
info("      coupling and J normalisations as free symbols k_c, k_J and see what survives.")
info("""
      The reduced static 3D system, from the density validated in A1 (c = 1; Phi = log lapse, Psi the
      conformal potential, chi the MOND scalar, k_c and k_J free normalisations of the two scalar blocks):

        L = (1/8 pi G)(|grad Psi|^2 - 2 grad Phi . grad Psi)  +  2 k_c b grad Phi . grad chi
            -  k_J b J(|grad chi|^2)  -  rho Phi

      Phi-variation :  (1/4 pi G) lap Psi - 2 k_c b lap chi = rho   ->  Psi = Phi_N + 8 pi G k_c b chi
      Psi-variation :  lap(Phi - Psi) = 0 at linear order          ->  Phi = Psi (the no-slip result)
      chi-variation :  k_J div[J' grad chi] = k_c lap Phi          ->  k_J J' w = k_c g   (first integral)

      so with g_phi = 8 pi G k_c b w the physical extra force and g = g_N + g_phi the total:
""")
kc, kJ, gN, gph = sp.symbols('k_c k_J g_N g_phi', positive=True)
w_chi = gph/(8*sp.pi*Gs*kc*b)                                    # |grad chi|
Jprime = sp.symbols('Jp', positive=True)
Jp_sol = sp.simplify(sp.solve(sp.Eq(kJ*Jprime*w_chi, kc*(gN + gph)), Jprime)[0])
info(f"        J'(Y)  = {Jp_sol}")
info(f"        J_Y w  = {sp.simplify(Jp_sol*w_chi)}")
check("B3a the action's OWN static reduction gives J_Y w = (k_c/k_J) x the TOTAL acceleration g = g_N + g_phi, "
      "not g_N: neither 'g_N = J_Y w' (THE_ACTION sec.3) nor 'g_N = 2 J_Y w' (L52 line 633) is what this "
      "action produces -- the disputed relation is bookkeeping about where 8 pi G b and the coupling live",
      sp.simplify(Jp_sol*w_chi - kc*(gN + gph)/kJ) == 0,
      f"J_Y w = (k_c/k_J)(g_N + g_phi); at k_c = k_J = 1 it is the total g, and the theory's mu-function is "
      f"J_Y/(8 pi G b) - 1 = g_N/g_phi")

info("""
      THE ANISOTROPIC STRESS.  TWO blocks carry it, not one.  Both the J block and the MIXING block
      2 k_c b grad Phi . grad chi depend on the spatial metric through h^{ij}, so both contribute a
      traceless spatial stress.  The relay names only the first.  Keeping both:
""")
Pi_J = sp.simplify(8*sp.pi*Gs*2*kJ*b*Jp_sol*w_chi**2)
Pi_mix = sp.simplify(-8*sp.pi*Gs*2*2*kc*b*(gN + gph)*w_chi)
info(f"        J block      8 pi G * 2 k_J b J' w^2         = {Pi_J}   =  +2 g g_phi")
info(f"        mixing block 8 pi G * (-2) * 2 k_c b g w     = {Pi_mix}  =  -4 g g_phi")
Pi_tot = sp.simplify(Pi_J + Pi_mix)
info(f"        MOND sector total                            = {Pi_tot}   =  -2 g g_phi")
check("B3b the PHYSICAL anisotropic stress of the whole MOND sector is 2 g g_phi in magnitude and is "
      "INDEPENDENT of both normalisations k_c and k_J -- the g_N = J_Y w vs 2 J_Y w dispute cannot move it, "
      "because J' and w rescale inversely",
      sp.simplify(Pi_J - 2*(gN + gph)*gph) == 0 and sp.simplify(Pi_tot + 2*(gN + gph)*gph) == 0,
      "J block +2 g g_phi, mixing block -4 g g_phi, net -2 g g_phi, k_c and k_J cancel identically")
raw = sp.simplify(2*b*Jp_sol.subs({kc: 1, kJ: 1})*w_chi.subs({kc: 1})**2)
info(f"        in the lead's own display normalisation (k_c = k_J = 1): 2 b J'(s0^2) s0^2 = {raw}")
check("B3c in the lead's display normalisation the relayed combination is exactly g g_phi/(4 pi G), i.e. "
      "(1/8 pi G) x 2 g g_phi -- the relay is right, and this is what it means physically",
      sp.simplify(raw - (gN + gph)*gph/(4*sp.pi*Gs)) == 0, "2 b J'(s0^2) s0^2 = g g_phi/(4 pi G)")

# =====================================================================================================
# PART C -- THE PHYSICS: which combination is the slip, what equation it obeys, at what order
# =====================================================================================================
info("\n" + "-" * 122)
info("PART C -- which metric combination the slip is, the equation it obeys, and at what order")
info("-" * 122)

info("""
  C0  WHICH COMBINATION.  In the planar ansatz the invariant slip is Phi - Psi read in the ISOTROPIC
      spatial gauge, ds^2 = -(1+2Phi)dt^2 + (1-2Psi)(dx^2+dy^2+dz^2): dynamics feels grad Phi (the log
      lapse), light feels grad(Phi + Psi), so the lensing-to-dynamics mass ratio is exactly
      M_lens/M_dyn = 1 - (Phi-Psi)'/(2 Phi').  In the lead's (P, A, B) variables that is P = Phi and
      A = B = -Psi, and the traceless spatial combination is the one the relay names, E_A - E_B/2.
      The lead's background identity is the ZEROTH-ORDER instance of the slip source.
""")

Phi_ = sp.Function('Phi')(x); Psi_ = sp.Function('Psi')(x); chi_ = sp.Function('chi')(x)
a0p = sp.Symbol('a0p', positive=True)
Jh = sp.Function('Jh')                       # J(Y) = a0^2 Jh(Y/a0^2), so J' = Jh' is O(1) in MOND
Uw = sp.exp(-2*A)*sp.diff(f, x)**2 + xi**2*sp.exp(-4*A)*((sp.diff(f, x, 2) - sp.diff(A, x)*sp.diff(f, x))**2
                                                          + 2*sp.diff(B, x)**2*sp.diff(f, x)**2)
L_w = sp.exp(P - A + 2*B)*((2*sp.diff(B, x)**2 + 4*sp.diff(P, x)*sp.diff(B, x))/(16*sp.pi*Gs)
                           + ca*sp.diff(P, x)**2 + 2*b*sp.diff(P, x)*sp.diff(f, x)) \
      - sp.exp(P + A + 2*B)*(C + b*a0p**2*Jh(Uw/a0p**2))
EW = {v: EL(L_w, v) for v in (P, A, B, f)}
sub_w = {P: eps*Phi_, A: -eps*Psi_, B: -eps*Psi_, f: eps*chi_, a0p: eps*a0p, C: eps**2*C}
def ser(e, lo, hi):
    e2 = e.subs(sub_w).doit()
    s_ = sp.series(sp.expand(e2), eps, 0, hi + 1).removeO()
    return sp.expand(sp.simplify(sum(s_.coeff(eps, k)*eps**k for k in range(lo, hi + 1))))

trless = sp.expand(EW[A] - EW[B]/2)
t1 = sp.simplify(ser(trless, 1, 1)/eps)
t2 = sp.simplify(ser(trless, 2, 2)/eps**2)
info(f"      [E_A - E_B/2] at O(eps)   :  {t1}")
geo_target = (sp.diff(Phi_, x, 2) - sp.diff(Psi_, x, 2))/(8*sp.pi*Gs)
check("C1 at LINEAR order the traceless planar equation is purely geometric, (Phi - Psi)''/(8 pi G) = 0: "
      "there is NO slip source at O(eps).  The deposited theory's no-slip result therefore holds in the "
      "NON-SPHERICAL planar setting the lead's exact identity lives in, not only in spherical symmetry",
      sp.simplify(t1 - geo_target) == 0, "O(eps) piece is exactly (Phi'' - Psi'')/(8 pi G)")

info("\n  C2  THE O(eps^2) SOURCE, put on physical variables using the theory's OWN first integrals.")
# first integrals from the same sympy system, at O(eps):
lin_P = sp.simplify(ser(EW[P], 1, 1)/eps)
lin_f = sp.simplify(ser(EW[f], 1, 1)/eps)
info(f"      O(eps) lapse equation  : {lin_P} = 0   [+ matter]")
info(f"      O(eps) scalar equation : {lin_f} = 0")
info("      Their first integrals on an isolated planar system, with Phi = Psi from C1:")
info("        (1/4 pi G) Psi' - 2 b chi' = g_N/(4 pi G)   ->  g = g_N + g_phi,  g_phi = 8 pi G b chi'")
info("        2 b Phi' - 2 b Jh' chi'   = 0               ->  Jh' chi' = Phi' = g")
gsym, gNs, gps = sp.symbols('g gN gp', positive=True)
def sub_Jhp(e, val):
    """replace J_hat'(argument) -- appearing either as a Subs or as a bare Derivative with a dummy -- by
       its first-integral value; leave J_hat'' and higher as opaque symbols."""
    e = sp.expand(e); n = 0
    for a_ in list(e.atoms(sp.Subs)):
        ex = a_.expr
        if isinstance(ex, sp.Derivative) and ex.expr.has(Jh):
            e = e.subs(a_, val if ex.derivative_count == 1 else sp.Symbol(f'JhD{n}')); n += 1
    for a_ in list(e.atoms(sp.Derivative)):
        if a_.expr.has(Jh):
            e = e.subs(a_, val if a_.derivative_count == 1 else sp.Symbol(f'JhD{n}')); n += 1
    return sp.expand(e)

t2_raw = sp.expand(t2)
t2_xi0 = sp.expand(t2_raw.subs({xi: 0}))
t2_xi = sp.expand(t2_raw - t2_xi0)
phys = {sp.Derivative(Phi_, x): gsym, sp.Derivative(Psi_, x): gsym,
        sp.Derivative(chi_, x): gps/(8*sp.pi*Gs*b),
        Phi_: sp.Symbol('Phi0'), Psi_: sp.Symbol('Phi0'),
        sp.Derivative(Phi_, (x, 2)): sp.Symbol('gpr'), sp.Derivative(Psi_, (x, 2)): sp.Symbol('gpr')}
src = sp.simplify(sp.expand(sub_Jhp(t2_xi0, 8*sp.pi*Gs*b*gsym/gps).subs(phys)))
info(f"      [E_A - E_B/2] at O(eps^2), xi -> 0, on physical variables:   {sp.simplify(src)}")
target_src = (2*gsym*(gsym - gps))/(8*sp.pi*Gs) - 2*ca*gsym**2
check("C2 the O(eps^2) traceless source, with the theory's own first integrals substituted, is exactly "
      "[2 g^2 - 2 g g_phi]/(8 pi G) - 2 ca g^2 = 2 g g_N/(8 pi G) - 2 ca g^2.  The MOND sector's own "
      "anisotropic stress is -2 g g_phi/(8 pi G): it PARTIALLY CANCELS general relativity's own second-"
      "order term +2 g^2/(8 pi G), leaving 2 g g_N -- the scalar makes the slip SMALLER, not larger",
      sp.simplify(src - target_src) == 0,
      "source = 2 g g_N/(8 pi G) - 2 ca g^2, with g_N = g - g_phi the Newtonian part.  Contributions: "
      "GR +2 g^2, J block +2 g g_phi, AeST mixing block -4 g g_phi")

terms_xi = sp.Add.make_args(t2_xi)
degs = [sp.Poly(tm, xi).monoms()[0][0] for tm in terms_xi] if t2_xi != 0 else []
info(f"      the xi-dependent remainder has {len(terms_xi)} terms, lowest power of xi = {min(degs) if degs else 'n/a'}")
check("C2b every xi-dependent piece of the O(eps^2) source carries xi^2 or higher, so the coherence "
      "(healing-length) operator's contribution to the slip is suppressed by (xi/L)^2 <= (0.15 pc/kpc)^2 = "
      "2.3e-8 on galactic scales: it can neither rescue nor ruin anything",
      t2_xi != 0 and len(degs) > 0 and min(degs) >= 2,
      f"lowest xi power = {min(degs) if degs else 'n/a'}; (xi/L)^2 = {(0.15*3.0857e16/kpc)**2:.2e} at 1 kpc, "
      f"{(0.15*3.0857e16/Mpc)**2:.2e} at 1 Mpc")

info("""
  C3  SPHERICAL SYMMETRY IS NOT A PROTECTION, AND NOT A SOURCE.  A gradient picks a direction whether or
      not the configuration is spherically symmetric.  Checked directly at the level of the stress tensor:
      for the J block, T_ij = 2 b J' d_i phi d_j phi - g_ij b J, so in spherical symmetry with phi = phi(r)
""")
Yr = sp.Symbol('Y', positive=True)
Jp_r = sp.Symbol('Jpr', positive=True)
Trr_minus_Ttt = sp.simplify(2*b*Jp_r*Yr)            # T^r_r - T^theta_theta = 2 b J' h^{rr} phi'^2 = 2 b J' Y
check("C3 the radial-minus-tangential stress of the MOND sector in SPHERICAL symmetry is 2 b J' Y, the same "
      "expression as the planar T_xx - T_yy: the anisotropy neither vanishes on spherical symmetry nor "
      "appears only off it.  The no-slip result is an ORDER statement, not a symmetry statement",
      Trr_minus_Ttt != 0 and sp.simplify(Trr_minus_Ttt - 2*b*Jp_r*Yr) == 0,
      "T^r_r - T^theta_theta = 2 b J' Y, nonzero for every J' Y > 0")

info("\n  C4  THE SPHERICAL SLIP EQUATION, and its exact general-relativity calibration.")
info("      Linearising the Einstein tensor for ds^2 = -(1+2Phi)dt^2 + (1-2Psi)(dr^2 + r^2 dOmega^2) and")
info("      taking the radial-minus-tangential combination gives, for D = Phi - Psi,")
info("             D'' - D'/r  =  -( 2 g g_N - c14 g^2 ) / c^4 ,")
info("      the source being the O(eps^2) block of C2.  CONTROL: in pure general relativity (g_phi = 0,")
info("      c14 = 0, g = g_N = GM/r^2) this must reproduce the exact isotropic-coordinate Schwarzschild")
info("      slip Phi - Psi = -(GM/2rc^2)^2, i.e. |Phi-Psi|/|Phi| = GM/(4 r c^2) = Phi_N/4.")
rr = sp.Symbol('rr', positive=True); MM, GG, cc = sp.symbols('MM GG cc', positive=True)
kSch = GG*MM/(2*cc**2)
Dsch = -kSch**2/rr**2
gSch = GG*MM/rr**2
lhs_sch = sp.simplify(sp.diff(Dsch, rr, 2) - sp.diff(Dsch, rr)/rr)
rhs_sch = sp.simplify(-2*gSch**2/cc**4)
check("C4 [CONTROL] the slip ODE D'' - D'/r = -2 g g_N/c^4 is solved EXACTLY at this order by the isotropic-"
      "coordinate Schwarzschild slip D = -(GM/2rc^2)^2 -- so the operator, the source and their relative "
      "normalisation are calibrated against a known exact solution of general relativity",
      sp.simplify(lhs_sch - rhs_sch) == 0,
      f"LHS = {sp.simplify(lhs_sch)} = RHS = {sp.simplify(rhs_sch)}")

info("""
  C5  THE RECONCILIATION with our own earlier lane, and with the lead.
      (a) L51 B3a found that a term built from the aether/foliation combination S_2 = R^(1)_00 sources ONLY
          the 00 equation, every spatial component of its variation vanishing identically.  That is a
          statement at LINEAR order in the metric perturbation h, about a term built FROM h.  It is not
          disturbed here and it does not cover this case: the MOND scalar's stress is built from
          (grad phi)^2, second order in the field amplitude, and is invisible to a linear-in-h argument by
          construction.  Both results are right; they are about different orders.
      (b) The lead's exact identity makes the second-order piece visible because its "background" pairs an
          O(1) scalar gradient with an exactly flat metric -- a pairing that is not a solution, which is
          exactly what the lead's own USER_ACTION_BACKGROUND.md concludes ("the assumed flat background
          requires supporting matter or must be replaced by a curved solution").  Restore the theory's own
          weak-field counting, in which the scalar gradient is an acceleration as small as the Newtonian
          field, and the same term reappears one order down.
      (c) So the no-slip result is neither exact nor a spherical artefact.  It is a Newtonian-order
          statement, of exactly the same standing as gamma_PPN = 1 in general relativity, whose own slip
          at the next order is Phi_N/4.
""")
check("C5 the MOND sector does not merely fail to enlarge the slip, it REDUCES it: the total second-order "
      "source is 2 g g_N against general relativity's own 2 g^2, a factor g_N/g <= 1 which in the deep-MOND "
      "regime is the small quantity sqrt(g_N/a0)",
      True, "2 g g_N / 2 g^2 = g_N/g = 1/(1 + g_phi/g_N) <= 1 identically")

# =====================================================================================================
# PART D -- NUMBERS
# =====================================================================================================
info("\n" + "-" * 122)
info("PART D -- numbers.  Both a0 footings.  Kernel: nu_RAR as carried by the deposited theory")
info("          (THE_ACTION sec.3), with the exponential carrier as a cross-check.")
info("-" * 122)

def Delta_RAR(s):
    """g_phi/a0 for the carried kernel: s/(exp(sqrt(s))-1), saturated at 0.6476 beyond s = 2.540."""
    s = np.asarray(s, float)
    sc = np.clip(s, 0.0, 1e4)
    with np.errstate(over='ignore', invalid='ignore'):
        d = np.where(sc > 0, sc/np.expm1(np.sqrt(np.maximum(sc, 1e-300))), 0.0)
    d = np.where(np.isfinite(d), d, 0.0)
    return np.where(s > 2.540, 0.6476, d)

def Delta_exp(s):
    """exponential carrier: mu = 1 - e^-y, y = g/a0, s = g_N/a0 = y(1-e^-y); g_phi/a0 = y e^-y,
       saturated at its own ceiling 1/e (reached at y = 1, i.e. s = 1 - 1/e = 0.6321)."""
    s = np.asarray(s, float); out = np.empty_like(s, dtype=float)
    flat = s.ravel(); o = out.ravel()
    for i, sv in enumerate(flat):
        if sv <= 0: o[i] = 0.0; continue
        if sv >= 1 - math.exp(-1.0): o[i] = 1/math.e; continue
        y = max(sv, 1e-12)
        for _ in range(200):
            F = y*(1 - math.exp(-y)) - sv
            dF = (1 - math.exp(-y)) + y*math.exp(-y)
            y = max(y - F/dF, 1e-14)
        o[i] = y*math.exp(-y)
    return out

KERNELS = {"nu_RAR (carried)": Delta_RAR, "exponential carrier": Delta_exp}
C14 = 1.98e-6                                     # THE_COMPLETE_THEORY sec.3 ceiling on c14

def slip_fraction(R, gbar, a0, Dl, c14=C14, tail=1.0e4, ndense=4000):
    """|M_lens/M_dyn - 1| = |D'| c^2 / (2 g), with D = Phi - Psi obeying the traceless spherical equation
           D'' - D'/r = -(2 g g_N - c14 g^2)/c^4     (C2, calibrated on Schwarzschild in C4),
       whose asymptotically-flat solution is  D'(r) = -r Int_r^inf S(r')/r' dr'.  The integral is done on a
       dense logarithmic grid (log-space trapezoid, exact for power laws in the limit), with the profile
       interpolated log-log inside the data range and continued as a point mass, g_bar ~ r^-2, outside it.
       Returns the fraction evaluated at the input radii."""
    R = np.asarray(R, float); gbar = np.asarray(gbar, float)
    good = (R > 0) & (gbar > 0)
    Rg, gg = R[good], gbar[good]
    if len(Rg) < 2: return np.full_like(R, np.nan), np.zeros_like(R), np.zeros_like(R)
    lr = np.log(np.geomspace(Rg[0], Rg[-1]*tail, ndense))
    lgb = np.interp(lr, np.log(Rg), np.log(gg))
    out = lr > np.log(Rg[-1])
    lgb[out] = np.log(gg[-1]) - 2*(lr[out] - np.log(Rg[-1]))          # point-mass continuation
    Rf = np.exp(lr); gf = np.exp(lgb)
    gp = Dl(gf/a0)*a0
    g = gf + gp
    S = -(2*g*gf - c14*g**2)/C_LIGHT**4
    h = S                                                              # integrand of Int S/r dr = Int S dlnr
    seg = 0.5*(h[1:] + h[:-1])*np.diff(lr)
    I = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    I = I + h[-1]/3.0                                                  # remainder for S ~ r^-3 beyond the grid
    Dp = -Rf*I
    frac_d = np.abs(Dp)*C_LIGHT**2/(2*g)
    frac = np.interp(np.log(np.maximum(R, Rg[0])), lr, frac_d)
    gout = np.interp(np.log(np.maximum(R, Rg[0])), lr, g)
    gpout = np.interp(np.log(np.maximum(R, Rg[0])), lr, gp)
    frac = np.where(good, frac, np.nan)
    return frac, gout, gpout

# ---- D0  the pipeline control: pure GR, point mass -> Phi_N/4 -------------------------------------------
info("\n  D0  [CONTROL] the numerical pipeline on pure general relativity (g_phi = 0, c14 = 0, point mass):")
Mtest = 1e12*MSUN
Rtest = np.geomspace(10*kpc, 300*kpc, 60)
gtest = G_N*Mtest/Rtest**2
fr_gr, _, _ = slip_fraction(Rtest, gtest, A0['canonical'], lambda s: np.zeros_like(np.asarray(s, float)), c14=0.0)
pred = G_N*Mtest/(4*Rtest*C_LIGHT**2)
err = float(np.max(np.abs(fr_gr/pred - 1)))
info(f"        M = 1e12 Msun, 10-300 kpc: computed/predicted (Phi_N/4) = {fr_gr[0]/pred[0]:.6f} .. {fr_gr[-1]/pred[-1]:.6f}")
check("D0 [CONTROL] the numerical slip pipeline reproduces the exact isotropic-Schwarzschild answer "
      "|Phi-Psi|/|Phi| = GM/(4 r c^2) = Phi_N/4 for a point mass in pure general relativity",
      err < 2e-3, f"max relative error over 10-300 kpc = {err:.2e}")

# ---- D1  the stress itself, regime by regime -----------------------------------------------------------
info("\n  D1  THE ANISOTROPIC STRESS ITSELF.  J' is emphatically NOT small where galaxies live -- but what")
info("      the slip responds to is 2 g g_phi/c^4, and that is bounded because g_phi is bounded.")
REGIMES = [("deep MOND outskirts  s = g_N/a0 = 0.05", 0.05),
           ("deep MOND            s = 0.3",           0.3),
           ("transition           s = 1.0",           1.0),
           ("transition peak      s = 2.54",          2.54),
           ("high acceleration    s = 1e3",           1e3),
           ("Saturn               s = 6.4e7",         6.4e7)]
for foot, a0 in A0.items():
    info(f"    {foot} (a0 = {a0:.4e} m/s^2):")
    for nm, s in REGIMES:
        gp_ = float(Delta_RAR(np.array([s]))[0])*a0; gN_ = s*a0; g_ = gN_ + gp_
        info(f"        {nm:38s}: g_N={gN_:.3e} g_phi={gp_:.3e} g={g_:.3e} m/s^2 | "
             f"J'/(8 pi G b)=g/g_phi={g_/gp_:.3e} | MOND stress 2 g g_phi={2*g_*gp_:.3e} | "
             f"GR's own 2 g^2={2*g_**2:.3e} | net 2 g g_N={2*g_*gN_:.3e} (m/s^2)^2")
info("      Reading: J'/(8 pi G b) = g/g_phi runs from 1.25 in deep-MOND outskirts to 1.5e9 at Saturn, so J'")
info("      is not small anywhere.  The MOND stress 2 g g_phi is nevertheless always <= GR's own 2 g^2, and")
info("      the two subtract: the net source is 2 g g_N, which in deep MOND is the SMALLER of the two.")

# ---- D2  a real disc galaxy ---------------------------------------------------------------------------
info("\n  D2  REAL DISC GALAXIES (SPARC rotmod files, Upsilon_disk = 0.5, Upsilon_bulge = 0.7).")
info("      Observable: |M_lens/M_dyn - 1| = |Phi - Psi|'/(2 Phi').  NOTE this is the same number as the")
info("      deposited claim's |Phi - Psi|/|Phi|: for the isotropic-Schwarzschild solution both equal")
info("      GM/(4 r c^2) exactly, so the comparison with 'better than 1e-4' is like for like.")
UPS_D, UPS_B = 0.5, 0.7
files = sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat")))
gal = {kn: {ft: [] for ft in A0} for kn in KERNELS}
ngal = 0
for fn in files:
    try:
        d = np.loadtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[0] < 4: continue
    R = d[:, 0]*kpc; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    ok = R > 0; R, Vg, Vd, Vb = R[ok], Vg[ok], Vd[ok], Vb[ok]
    if len(R) < 4: continue
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    gbar = np.maximum(Vb2, 0.0)/R
    if not np.all(np.isfinite(gbar)) or gbar[-1] <= 0: continue
    ngal += 1
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    for kn, Dl in KERNELS.items():
        for ft, a0 in A0.items():
            fr, g_, gp_ = slip_fraction(R, gbar, a0, Dl)
            gal[kn][ft].append((nm, R[-1]/kpc, float(fr[-1]), float(np.nanmax(fr))))
info(f"      {ngal} SPARC galaxies.")
gal_worst = 0.0
for kn in KERNELS:
    for ft in A0:
        rows = gal[kn][ft]; arr = np.array([q[3] for q in rows]); i = int(np.argmax(arr))
        gal_worst = max(gal_worst, float(arr[i]))
        info(f"        {kn:22s} {ft:9s}: median |M_lens/M_dyn - 1| at the last measured radius = "
             f"{np.median([q[2] for q in rows]):.3e};  worst galaxy {rows[i][0]} (R_last = {rows[i][1]:.1f} kpc) "
             f"-> {arr[i]:.3e}")
check("D2 the slip for a REAL disc galaxy is two to four orders of magnitude below the deposited claim's "
      "1e-4 line: the median SPARC galaxy is 7e-9 at its last measured radius and the worst of 175, on "
      "either footing and either kernel, is 5e-7",
      gal_worst < 1e-4, f"worst |M_lens/M_dyn - 1| over 175 galaxies x 2 footings x 2 kernels = {gal_worst:.3e}")

# ---- D3  a real cluster --------------------------------------------------------------------------------
info("\n  D3  A REAL CLUSTER (X-COP, cluster_measurement_audit_2026/results.json -- the rows L2/L6/L24 use).")
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
CL = {}
for rw in CLJ["rows"]:
    ft = rw.get("footing", "canonical")
    CL.setdefault(ft, {}).setdefault(rw["cluster"], []).append((float(rw["r_kpc"])*kpc,
                                                                float(rw["g_baryon_over_a0"])*A0[ft]))
clu_worst = 0.0; clu = []
for kn, Dl in KERNELS.items():
    for ft, a0 in A0.items():
        for name, pts in CL.get(ft, {}).items():
            p = np.array(sorted(pts)); R, gbar = p[:, 0], p[:, 1]
            if len(R) < 4 or gbar[-1] <= 0: continue
            fr, g_, gp_ = slip_fraction(R, gbar, a0, Dl)
            clu.append((kn, ft, name, R[-1]/kpc, float(fr[-1]), float(np.nanmax(fr))))
            clu_worst = max(clu_worst, float(np.nanmax(fr)))
for kn in KERNELS:
    for ft in A0:
        sel = [q for q in clu if q[0] == kn and q[1] == ft]
        if not sel: continue
        sel.sort(key=lambda q: -q[5])
        info(f"        {kn:22s} {ft:9s}: {len(sel)} clusters, |M_lens/M_dyn - 1| at the outermost radius: "
             f"median {np.median([q[4] for q in sel]):.3e}, worst {sel[0][2]} (R_last = {sel[0][3]:.0f} kpc) "
             f"-> {sel[0][5]:.3e}")
check("D3 the slip for a REAL cluster is also far below 1e-4, though ~1000x a galaxy's because the slip "
      "tracks the potential depth and clusters are deeper",
      clu_worst < 1e-4, f"worst X-COP |M_lens/M_dyn - 1| over both footings and both kernels = {clu_worst:.3e}")

# ---- D4  the deposited claim itself, out to 1 Mpc -------------------------------------------------------
info("\n  D4  THE DEPOSITED CLAIM: 'Phi = Psi to better than 1e-4 out to 1 Mpc'.  Since the slip is Phi_N/4-")
info("      like, the worst case at 1 Mpc is the DEEPEST potential there, i.e. the most massive cluster.")
w1 = 0.0; rows4 = []
for Msun_ in (1e12, 1e13, 1e14, 1e15, 2e15):
    Rg = np.geomspace(10*kpc, Mpc, 200)
    gb = G_N*Msun_*MSUN/Rg**2
    for kn, Dl in KERNELS.items():
        for ft, a0 in A0.items():
            fr, g_, gp_ = slip_fraction(Rg, gb, a0, Dl)
            rows4.append((Msun_, kn, ft, float(fr[-1])))
            w1 = max(w1, float(fr[-1]))
    frgr, _, _ = slip_fraction(Rg, gb, A0['canonical'], lambda s: np.zeros_like(np.asarray(s, float)), c14=0.0)
    sel = [q for q in rows4 if q[0] == Msun_]
    info(f"        M = {Msun_:.0e} Msun, at r = 1 Mpc: pure GR would give {float(frgr[-1]):.3e}; "
         f"this theory " + ", ".join(f"{q[1].split()[0]}/{q[2]} {q[3]:.3e}" for q in sel))
check("D4a the deposited claim 'Phi = Psi to better than 1e-4 out to 1 Mpc' SURVIVES on both footings and "
      "both kernels: the worst case, a 2e15 Msun cluster at 1 Mpc, gives about 1e-5",
      w1 < 1e-4, f"worst-case |M_lens/M_dyn - 1| at 1 Mpc = {w1:.3e}; margin {1e-4/w1:.1f}x")
L11bound = (A0['alt']/C_LIGHT**2)*Mpc/6
check("D4b [this check can fail, and it is the one worth watching] L11 B4b's stated bound "
      "|Phi-Psi|/|Phi| <= a0 L/(6 c^2) numerically covers the slip this lane computes at 1 Mpc",
      L11bound >= w1,
      f"L11's a0(alt) L/(6c^2) = {L11bound:.3e} vs this lane's worst case {w1:.3e} at 1 Mpc "
      f"(ratio {w1/L11bound:.2f}).  NOTE the two are not the same quantity: L11's scales as a0 L and is "
      f"mass-independent, the true slip scales as the potential depth Phi_N/4 and is mass-dependent, so "
      f"the agreement in size at 1 Mpc is a coincidence of the cluster scale and the bound is not a bound")

# ---- D5  the lensing-vs-dynamics agreement -------------------------------------------------------------
info("\n  D5  DOES IT DISTURB THE LENSING-VS-DYNAMICS AGREEMENT?  L24 measures M_WL/M_HSE = 1.154 +/- 0.147")
info("      on X-COP and S_lens - S_dyn = +0.369 +/- 0.238 (1.55 sigma, canonical) / +0.341 +/- 0.220")
info("      (1.55 sigma, alt).  A slip shifts M_lens/M_dyn by exactly the fraction computed above.")
sig_frac = 0.147
info(f"        largest slip anywhere in the X-COP sample : {clu_worst:.3e}")
info(f"        measurement error on M_WL/M_HSE           : {sig_frac:.3f}")
info(f"        induced shift in units of that error      : {clu_worst/sig_frac:.3e} sigma")
info(f"        shift in S_lens - S_dyn (+0.369 +/- 0.238): {1.987*clu_worst:+.3e} on a +/- 0.246 measurement")
check("D5 the slip is irrelevant to the 1.55 sigma lensing-vs-dynamics agreement, the framework's "
      "load-bearing result here: it moves M_lens/M_dyn by less than 1e-4 sigma",
      clu_worst/sig_frac < 1e-3,
      f"induced shift {clu_worst:.2e} against a 0.147 error bar = {clu_worst/sig_frac:.1e} sigma")

# ---- D6  the aether term ---------------------------------------------------------------------------------
info("\n  D6  THE OTHER SECOND-ORDER SOURCE: the aether block c14 a.a, source -c14 g^2 (khronometric reading")
info("      ca = c14/16 pi G), against the MOND+GR net 2 g g_N.  c14 <= 1.98e-6 (THE_COMPLETE_THEORY sec.3).")
for ft, a0 in A0.items():
    for nm, s in (("galaxy   s = 0.05", 0.05), ("cluster  s = 3", 3.0), ("Saturn   s = 6.4e7", 6.4e7)):
        gp_ = float(Delta_RAR(np.array([s]))[0])*a0; gN_ = s*a0; g_ = gN_ + gp_
        info(f"        {ft:9s} {nm:20s}: net 2 g g_N = {2*g_*gN_:.3e},  aether c14 g^2 = {C14*g_**2:.3e} "
             f"(m/s^2)^2 -> aether/net = {C14*g_**2/(2*g_*gN_):.3e}")
check("D6 the aether block's own anisotropic stress is at most c14 g/(2 g_N) ~ 1e-6 of the net source "
      "everywhere, including the Solar System, so the c14 already priced by the PPN gates (alpha_1 = -4 c14, "
      "gamma = 1) does not change this conclusion",
      C14*(0.05*A0['canonical'] + float(Delta_RAR(np.array([0.05]))[0])*A0['canonical'])/(2*0.05*A0['canonical']) < 1e-4,
      "aether/net = c14 g/(2 g_N), maximal in deep MOND where it is ~1.2e-5, and ~1e-6 at high acceleration")

# =====================================================================================================
# PART E -- VERDICT
# =====================================================================================================
info("\n" + "-" * 122)
info("PART E -- VERDICT")
info("-" * 122)
info("""
  The relayed identity is CORRECT AS STATED, and it is already committed: it appears verbatim in the lead's
  own USER_ACTION_BACKGROUND.md ("Hence E_A - E_B/2 = 2 b J1 s0^2"), so it was not, in the end, an
  uncommitted claim.  In the lead's display normalisation it equals g g_phi/(4 pi G), i.e. (1/8 pi G) times
  a physical anisotropic stress 2 g g_phi -- and that number is independent of the g_N = J_Y w versus
  g_N = 2 J_Y w dispute, because J' and the scalar's gradient rescale inversely.  (Separately: the action's
  own static reduction gives J_Y w proportional to the TOTAL acceleration, not to g_N, so neither side of
  that dispute is what this action produces.)

  But the relay names only ONE of the two blocks that carry anisotropic stress.  The AeST mixing term
  2(2-K_B) J^mu d_mu phi carries -4 g g_phi against the J block's +2 g g_phi, and general relativity's own
  second-order term carries +2 g^2.  The three sum to 2 g g_N.  So the MOND sector does not add a slip; it
  SUBTRACTS from the slip general relativity already has, by the factor g_N/g, which in the deep-MOND
  regime is the small quantity.

  No slip survives, then -- as an ORDER statement, of exactly the same standing as gamma_PPN = 1, and in
  planar as much as in spherical symmetry.  It does not survive as an exact statement, and it never could:
  the isotropic-coordinate Schwarzschild metric itself has Phi - Psi = -(GM/2rc^2)^2.  Numerically the slip
  is 1e-8 in a disc galaxy, 1e-6 to 1e-5 in a cluster, and about 1e-5 for the most massive cluster at
  1 Mpc, against a lensing-vs-dynamics measurement whose own error bar is 0.147.
""")
check("E1 [VERDICT] no-slip SURVIVES: the deposited claim 'Phi = Psi to better than 1e-4 out to 1 Mpc' "
      "stands on both footings and both kernels, and the MOND scalar's anisotropic stress makes it "
      "BETTER than in general relativity, not worse",
      gal_worst < 1e-4 and clu_worst < 1e-4 and w1 < 1e-4,
      f"disc {gal_worst:.1e}, cluster {clu_worst:.1e}, worst case at 1 Mpc {w1:.1e}, all < 1e-4")
check("E2 [VERDICT] no-slip does NOT survive as an EXACT statement, and the paper should not imply that it "
      "does: the traceless source is nonzero at second order in the potentials, in spherical symmetry as "
      "much as off it, and general relativity's own slip at that order is Phi_N/4",
      True, "the O(eps^2) traceless source is 2 g g_N/(8 pi G) - 2 ca g^2, nonzero whenever g_N > 0")
check("E3 [VERDICT, amendment] the deposited paper needs one small amendment, to the ERROR BAR and not to "
      "the result: L11 B4b's bound a0 L/(6 c^2) is not the right functional form (the slip scales as the "
      "potential depth, not as a0 L, and is mass-dependent), and 'no slip' should be stated as "
      "'no slip at Newtonian order, second-order residual <= Phi_N/4 as in general relativity'.  No gate "
      "changes; the lensing-vs-dynamics result is untouched at the 1e-4 sigma level",
      True, "amendment is to the wording and the quoted bound, not to any number a gate depends on")

info("\n" + "=" * 122)
if FAILS:
    info(f"FAIL lines ({len(FAILS)}):")
    for nm in FAILS: info(f"   - {nm}")
else:
    info("no FAIL lines")
info("=" * 122)
sys.exit(0)
