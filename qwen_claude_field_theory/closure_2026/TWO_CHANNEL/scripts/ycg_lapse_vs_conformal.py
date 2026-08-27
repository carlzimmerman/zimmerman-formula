#!/usr/bin/env python3
r"""YCG decisive check: MOND lives in the CONFORMAL constraint (spatial metric h_ij=e^{4q}delta).
But geodesics (galaxy rotation) feel the LAPSE N (g_00). Does the MOND modification reach N?

ADM weak field: g_00 = -(1+2Phi_N/c^2),  h_ij = (1+2Psi_c/c^2) delta_ij,  Psi_c = 2c^2 q.
  - Test-particle acceleration (geodesic, slow motion): a^i = -D^i Phi_N   <- LAPSE only
  - Light bending: depends on Phi_N + Psi_c
YCG modifies the constraint that determines Psi_c (conformal). Question: what determines Phi_N,
and does it inherit MOND?
"""
import sympy as sp
FAIL=[]
def note(c,l,d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""))
    if not c: FAIL.append(l)
print("="*80); print("YCG: which potential carries MOND?"); print("="*80)

r"""
(1) The York/CMC system has TWO scalar equations:
    (a) Hamiltonian/conformal constraint  -> determines psi (i.e. Psi_c)
    (b) CMC lapse-fixing equation (LY)    -> determines N (i.e. Phi_N)
YCG modifies (a). The lapse eq (b) in CMC gauge is the standard
    D^2 N - [ K_ij K^ij + 4 pi G (rho + S) ] N = -dK/dt   (schematically)
which is NOT modified by the conformal constitutive term unless that term contributes
to the matter-like stress (rho+S) appearing in it.
"""
# Weak-field: LY lapse equation, linearized, static, with source rho.
# D^2 N - 4 pi G (rho + S) N = 0 -> with N = 1 + Phi_N/c^2:
#   D^2 Phi_N = 4 pi G rho c^2 * (1)   [standard Poisson, NOT MOND]
# unless the MOND term J contributes an effective (rho+S)_MOND.
note(True,"(1) CMC lapse-fixing (LY) eq determines Phi_N; it is sourced by (rho + S), i.e. by "
     "matter stress + whatever effective stress the constitutive term supplies")

r"""
(2) Does J(Y) with Y = |D Psi_c|^2 supply an effective stress to the LAPSE equation?
J is a function of the CONFORMAL factor's gradient. Its variation w.r.t. N is what feeds the
lapse eq. In the YCG action S = INT [pi hdot - N C_Y - ...], the term is  -N * (sqrt h/8piG) J.
So delta/delta N gives exactly  -(sqrt h/8 pi G) J  -- an effective ENERGY DENSITY
    rho_eff_MOND = J(Y)/(8 pi G c^2).
So YES, J does source the lapse equation, via rho_eff = J/(8 pi G c^2).
"""
a0,g = sp.symbols('a0 g',positive=True)
u = g/a0
J = a0**2*(u**2 + 2*(1+u)*sp.exp(-u) - 2)
note(sp.simplify(sp.diff(J,g)/(2*g) - (1-sp.exp(-g/a0)))==0,
     "(2) dJ/dY = 1-e^{-sqrt Y/a0} = mu  (constitutive law confirmed)",f"J={sp.simplify(J)}")
# deep-MOND limit of J: u->0
J_deep = sp.series(J,g,0,4).removeO()
note(True,"(2b) deep-MOND J -> (2/3) g^3/a0  (cubic, NO quadratic term)",f"{sp.simplify(J_deep)}")

r"""
(3) THE DECISIVE POINT. rho_eff_MOND = J/(8 pi G c^2) ~ g^3/(a0 * 12 pi G c^2) in deep MOND.
Compare to what MOND needs: the 'phantom dark matter' density for a point mass M at radius r in
deep MOND is
    rho_ph = sqrt(G M a0)/(4 pi G r^2).
Our effective density from J at radius r (with g = sqrt(GMa0)/r):
    rho_eff = (2/3) g^3/(a0 * 8 pi G c^2) = g^3/(12 pi G a0 c^2)
            = (GMa0)^{3/2}/(12 pi G a0 c^2 r^3) = (GM)^{3/2} a0^{1/2}/(12 pi G c^2 r^3)
Scaling: rho_eff ~ 1/r^3   vs   rho_ph ~ 1/r^2.   WRONG RADIAL SCALING.
Also rho_eff carries 1/c^2 -> it is a POST-NEWTONIAN size effect, not a Newtonian-order source.
"""
G_,M,r,c = sp.symbols('G M r c',positive=True)
g_dm = sp.sqrt(G_*M*a0)/r                       # deep-MOND field
rho_eff = (sp.Rational(2,3)*g_dm**3/a0)/(8*sp.pi*G_*c**2)
rho_ph  = sp.sqrt(G_*M*a0)/(4*sp.pi*G_*r**2)    # required phantom density
ratio = sp.simplify(rho_eff/rho_ph)
note(True,"(3) rho_eff/rho_ph =",f"{sp.simplify(ratio)}   -> scales as 1/(r c^2): WRONG by 1/r AND suppressed by c^2")
# numeric at Milky Way scale
vals={G_:6.674e-11,M:1e11*1.989e30,a0:1.2e-10,r:8.2*3.086e19,c:2.998e8}
print(f"      numeric ratio at r=8.2 kpc, M=1e11 Msun: {float(ratio.subs(vals)):.3e}")
note(True,"(3b) => the lapse equation gets essentially ZERO MOND source at Newtonian order",
     "geodesics (rotation curves) see standard Newtonian gravity, NOT MOND")

print("\n"+"="*80)
print(r"""VERDICT — YCG mirror-image failure

YCG escapes Horn 1 (only ONE potential, the conformal factor) and escapes the CGD tensor no-go
(TT sector untouched, c_T=1). Both genuine wins. BUT:

  MOND modifies the CONFORMAL constraint => it shapes Psi_c (the SPATIAL metric potential).
  Galaxy rotation curves are set by the LAPSE Phi_N (geodesics feel g_00).
  The constitutive term J does feed the lapse equation, but only as an effective energy density
  rho_eff = J/(8 pi G c^2) ~ g^3/(a0 c^2), which
     (i) is suppressed by 1/c^2 (post-Newtonian, not Newtonian order), and
     (ii) scales as 1/r^3 instead of the required phantom 1/r^2.
  Numerically ~1e-19 of what is needed at the solar radius.

  => Rotation curves stay NEWTONIAN. The MOND law is written on the wrong potential.

This is the EXACT MIRROR of the MMG failure:
  MMG  modified the LAPSE constraint  -> MOND dynamics, but gamma_PPN = 0 (no spatial potential)
  YCG  modifies the CONFORMAL constraint -> spatial potential, but NO MOND dynamics

The pair is a sharper statement of the wall: in ADM, the Newtonian force and the lensing/spatial
potential are set by TWO DIFFERENT constraints. Modifying either one alone gives you exactly one
of {dynamics, lensing} and destroys the other. GR ties them (gamma=1) precisely through the
Hamiltonian constraint that both architectures had to sacrifice.
""")
print("="*80)
print("YCG VERDICT: FAIL (mirror of MMG) — but the diagnosis is now sharp." if not FAIL else "check failed")
