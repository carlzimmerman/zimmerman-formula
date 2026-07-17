#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M2, SEAM S6 (disformal lensing: point-mass closed forms)
===============================================================================
Framework premises used (prep_2026/mi_field_theory/UNIFICATION.md, re-derived there
from the single action, 17/17):
  - light couples to g~ = g + B u u with B fixed by the SAME kernel: grad B = 4(nu-1) g_bar
    => the deflecting field is EXACTLY the RAR field  g_lens(r) = nu(y) g_bar = g_obs(r)
  - valid where the closure is pinned: SPHERICAL symmetry (gap A off-sphere), weak field,
    thin lens, isolated lens (no EFE). All results below carry those flags.
Framework law: g_obs(r) = sqrt(g_bar^2 + a0 g_bar),  g_bar = GM/r^2 (point mass M),
MOND radius r_M = sqrt(GM/a0). Both footings: a0 = 9.362e-11 / 1.130e-10.

Derives and verifies:
 E-S6-1  MASS HYPERBOLA (effective/lensing mass of a point mass)      [EXACT]
           M_eff(r) = g_obs r^2/G = M sqrt(1 + (r/r_M)^2)
         and the general-spherical MASS-LINE (a0-line in mass form):
           G [M_eff(r)^2 - M_b(r)^2] = a0 M_b(r) r^2   (any spherical system)
 E-S6-2  PHANTOM-HALO CLOSED FORM                                     [EXACT]
           rho_ph(r) = sqrt(G M a0)/(4 pi G) * 1/( r sqrt(r^2 + r_M^2) )
         (1/r cusp inside r_M -> isothermal 1/r^2 outside; NOT NFW, NOT cored)
 E-S6-3  DEFLECTION-ANGLE CLOSED FORM (complete elliptic E)  [EXACT in weak field]
           alpha(b) = (4GM/(c^2 b)) sqrt(1+u^2) E(m),  u = b/r_M,  m = 1/(1+u^2)
         limits: b<<r_M -> 4GM/c^2 b (Einstein);  b>>r_M -> 2 pi sqrt(G M a0)/c^2
         approach law: alpha -> alpha_inf [1 + r_M^2/(4 b^2) + O(u^-4)]
 E-S6-4  PROJECTED PHANTOM SURFACE DENSITY (complete elliptic K)      [EXACT]
           Sigma_ph(b) = sqrt(G M a0)/(2 pi G) * K(m)/sqrt(b^2 + r_M^2)
         SAME modulus m as E-S6-3: the framework point lens is the (K,E) elliptic pair.
 E-S6-5  SELF-CONSISTENCY (shear/convergence closure)                 [EXACT]
           d/db [ M sqrt(1+u^2) E(m) ] = 2 pi b Sigma_ph(b)
         (the E-form deflection and the K-form surface density are one system)
Cross-flag: alpha_inf = 2 pi v_flat^2/c^2 with v_flat^4 = G M a0 (deep-MOND lensing
isothermality) is KNOWN MOND literature (Milgrom, Mortlock & Turner 2001); what is
claimed as new here is the exact all-radii elliptic closed form FOR THIS nu.
"""
import sys, math
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
FAIL = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

r, b, l, G, M, a0, c, u_ = sp.symbols('r b l G M a0 c u', positive=True)
rM = sp.sqrt(G*M/a0)
gbar = G*M/r**2
gobs = sp.sqrt(gbar**2 + a0*gbar)

print("="*78)
print("E-S6-1  mass hyperbola + mass-line")
print("="*78)
Meff = sp.simplify(gobs*r**2/G)
check("M_eff(r) == M sqrt(1+(r/r_M)^2)  (EXACT)",
      sp.simplify(Meff - M*sp.sqrt(1 + r**2/rM**2)) == 0)
check("mass hyperbola: M_eff^2 - M^2 == (a0/G) M r^2  (point mass)",
      sp.simplify(Meff**2 - M**2 - a0*M*r**2/G) == 0)
# general spherical: M_b(r) arbitrary positive function
Mb = sp.Function('M_b', positive=True)(r)
gb_gen = G*Mb/r**2
gob_gen = sp.sqrt(gb_gen**2 + a0*gb_gen)
Meff_gen = gob_gen*r**2/G
check("mass-line (any spherical system): G(M_eff^2 - M_b^2) == a0 M_b r^2",
      sp.simplify(G*(Meff_gen**2 - Mb**2) - a0*Mb*r**2) == 0)

print()
print("="*78)
print("E-S6-2  phantom halo closed form")
print("="*78)
rho_eff = sp.simplify(sp.diff(Meff, r)/(4*sp.pi*r**2))
rho_claim = sp.sqrt(G*M*a0)/(4*sp.pi*G) / (r*sp.sqrt(r**2 + rM**2))
check("rho_ph(r) == sqrt(GMa0)/(4 pi G) / (r sqrt(r^2+r_M^2))  (EXACT)",
      sp.simplify(rho_eff - rho_claim) == 0)
# asymptotics: 1/r cusp inside, isothermal 1/r^2 outside
inner = sp.limit(rho_claim*r, r, 0)
outer = sp.limit(rho_claim*r**2, r, sp.oo)
check("inner cusp: rho_ph -> sqrt(GMa0)/(4 pi G r_M) * 1/r",
      sp.simplify(inner - sp.sqrt(G*M*a0)/(4*sp.pi*G*rM)) == 0)
check("outer: rho_ph -> sqrt(GMa0)/(4 pi G) * 1/r^2  (isothermal)",
      sp.simplify(outer - sp.sqrt(G*M*a0)/(4*sp.pi*G)) == 0)

print()
print("="*78)
print("E-S6-3  deflection closed form alpha(b) = (4GM/c^2 b) sqrt(1+u^2) E(m)")
print("="*78)
# derivation: alpha(b) = (2/c^2) INT g_obs(r) (b/r) dl,  r = sqrt(b^2+l^2)
#   g_obs = sqrt(GM) sqrt(GM + a0 r^2)/r^2 = sqrt(GM a0) sqrt(r_M^2+r^2)/r^2
#   -> alpha = (2 b sqrt(GM a0)/c^2) INT_-inf^inf sqrt(A^2+l^2)/(b^2+l^2)^{3/2} dl, A^2=r_M^2+b^2
# STEP 1 (exact, sympy): the l-integral in trig form. l = b tan(psi):
#   INT = (1/b^2) INT_{-pi/2}^{pi/2} sqrt(A^2 - (A^2-b^2) sin^2 psi) dpsi = (2A/b^2) E(m),
#   m = (A^2-b^2)/A^2 = r_M^2/(r_M^2+b^2)
psi, A = sp.symbols('psi A', positive=True)
integrand_l = sp.sqrt(A**2 + l**2)/(b**2 + l**2)**sp.Rational(3, 2)
sub = integrand_l.subs(l, b*sp.tan(psi))*sp.diff(b*sp.tan(psi), psi)
sub = sp.simplify(sp.trigsimp(sub.rewrite(sp.cos)))
target = sp.sqrt(A**2 - (A**2 - b**2)*sp.sin(psi)**2)/b**2
# equality of integrands on (-pi/2, pi/2) given A > b (substitute A = sqrt(b^2 + k^2))
k = sp.symbols('k', positive=True)
dif = sp.simplify((sub - target).subs(A, sp.sqrt(b**2 + k**2)))
dif = sp.simplify(dif.subs(sp.Abs(sp.cos(psi)), sp.cos(psi)))  # psi in (-pi/2,pi/2)
check("trig substitution: integrand -> sqrt(A^2-(A^2-b^2)sin^2 psi)/b^2 (exact)",
      dif == 0)
m = sp.symbols('m', positive=True)
ell = sp.integrate(sp.sqrt(A**2 - (A**2 - b**2)*sp.sin(psi)**2),
                   (psi, -sp.pi/2, sp.pi/2), conds='none')
ell_expected = 2*A*sp.elliptic_e((A**2 - b**2)/A**2)
ell_ok = sp.simplify(ell - ell_expected) == 0
if not ell_ok:
    # fallback: verify the elliptic reduction numerically on a grid (still exact math,
    # just checked pointwise to 1e-25)
    ok = True
    for bb, kk in ((0.3, 1.0), (2.0, 1.0), (1.0, 5.0)):
        AA = mp.sqrt(bb**2 + kk**2)
        lhsn = mp.quad(lambda ps: mp.sqrt(AA**2 - (AA**2 - bb**2)*mp.sin(ps)**2),
                       [-mp.pi/2, mp.pi/2])
        rhsn = 2*AA*mp.ellipe((AA**2 - bb**2)/AA**2)
        ok = ok and abs(lhsn - rhsn) < mp.mpf('1e-25')
    ell_ok = ok
check("angular integral == 2 A E(m), m=(A^2-b^2)/A^2", ell_ok)
# STEP 2: assembled closed form vs direct numerical LOS integration (adversarial grid)
def alpha_direct(bb, GM=1.0, a0n=1.0):
    rMn = mp.sqrt(GM/a0n)
    f = lambda ll: mp.sqrt(GM)*mp.sqrt(GM + a0n*(bb**2 + ll**2)) / \
        (bb**2 + ll**2)**mp.mpf('1.5') * bb
    return 2*mp.quad(f, [0, bb, 10*max(bb, rMn), mp.inf])*2   # c=1; even integrand x2
def alpha_closed(bb, GM=1.0, a0n=1.0):
    rMn = mp.sqrt(GM/a0n)
    uu = bb/rMn
    mm = 1/(1 + uu**2)
    return (4*GM/bb)*mp.sqrt(1 + uu**2)*mp.ellipe(mm)
gridok = True
for uu in (0.03, 0.3, 1.0, 3.0, 30.0):
    ad, ac = alpha_direct(mp.mpf(uu)), alpha_closed(mp.mpf(uu))
    rel = abs(ad - ac)/ac
    gridok = gridok and rel < mp.mpf('1e-20')
    print(f"   u=b/r_M={uu:>5}: direct={mp.nstr(ad,12)}  closed={mp.nstr(ac,12)}  rel={mp.nstr(rel,3)}")
check("alpha(b) closed form == direct LOS integral (grid u=0.03..30, rel<1e-20)", gridok)
# STEP 3: exact limits
uu, tt = sp.symbols('u t', positive=True)
alpha_expr = 4*G*M/(c**2*b)*sp.sqrt(1 + uu**2)*sp.elliptic_e(1/(1 + uu**2))
newt = sp.limit(sp.sqrt(1 + uu**2)*sp.elliptic_e(1/(1 + uu**2)), uu, 0)
check("Newtonian limit: b<<r_M -> alpha = 4GM/c^2 b  (factor -> E(1)=1)",
      sp.simplify(newt - 1) == 0)
deep = sp.limit(sp.sqrt(1 + uu**2)*sp.elliptic_e(1/(1 + uu**2))/uu, uu, sp.oo)
check("deep limit: b>>r_M -> alpha = 2 pi sqrt(GMa0)/c^2  (factor/u -> pi/2)",
      sp.simplify(deep - sp.pi/2) == 0)
# approach law: series in t = 1/u^2
fac = sp.sqrt(1 + uu**2)*sp.elliptic_e(1/(1 + uu**2))/uu*2/sp.pi
ser = sp.series(fac.subs(uu, 1/sp.sqrt(tt)), tt, 0, 2).removeO()
check("approach law: alpha/alpha_inf = 1 + (1/4)(r_M/b)^2 + O(u^-4)",
      sp.simplify(ser - (1 + tt/4)) == 0)

print()
print("="*78)
print("E-S6-4  Sigma_ph(b) = sqrt(GMa0)/(2 pi G) K(m)/sqrt(b^2+r_M^2)")
print("="*78)
# Sigma_ph(b) = INT rho_ph dl; the l-integral: INT_0^inf dl/(sqrt(b^2+l^2) sqrt(b^2+r_M^2+l^2))
#             = K(m)/sqrt(b^2+r_M^2)  -- verify numerically on adversarial grid (c=1,GM=1,a0=1)
def Sig_direct(bb, GM=1.0, a0n=1.0):
    rMn = mp.sqrt(GM/a0n)
    f = lambda ll: mp.sqrt(GM*a0n)/(4*mp.pi) / \
        (mp.sqrt(bb**2 + ll**2)*mp.sqrt(bb**2 + ll**2 + rMn**2))
    return 2*mp.quad(f, [0, bb, 10*max(bb, rMn), mp.inf])
def Sig_closed(bb, GM=1.0, a0n=1.0):
    rMn = mp.sqrt(GM/a0n)
    mm = rMn**2/(bb**2 + rMn**2)
    return mp.sqrt(GM*a0n)/(2*mp.pi)*mp.ellipk(mm)/mp.sqrt(bb**2 + rMn**2)
gridok = True
for uu2 in (0.03, 0.3, 1.0, 3.0, 30.0):
    sd, scl = Sig_direct(mp.mpf(uu2)), Sig_closed(mp.mpf(uu2))
    rel = abs(sd - scl)/scl
    gridok = gridok and rel < mp.mpf('1e-20')
    print(f"   u={uu2:>5}: direct={mp.nstr(sd,12)}  closed={mp.nstr(scl,12)}  rel={mp.nstr(rel,3)}")
check("Sigma_ph closed form == direct LOS integral (grid, rel<1e-20)", gridok)

print()
print("="*78)
print("E-S6-5  closure: d/db[M sqrt(1+u^2) E(m)] == 2 pi b Sigma_ph(b)")
print("="*78)
# symbolic, using sympy's elliptic derivatives; u = b/r_M kept explicit
rMs = sp.symbols('r_M', positive=True)
M2D = M*sp.sqrt(1 + (b/rMs)**2)*sp.elliptic_e(1/(1 + (b/rMs)**2))
lhs = sp.simplify(sp.diff(M2D, b))
Sig = (M/rMs**2)/(2*sp.pi)*sp.elliptic_k(rMs**2/(b**2 + rMs**2))/sp.sqrt(
    (b**2 + rMs**2)/rMs**4)/rMs**2   # sqrt(GMa0)/(2piG) = M/(2 pi r_M) etc; use pure form:
Sig = M/(2*sp.pi*rMs)*sp.elliptic_k(rMs**2/(b**2 + rMs**2))/sp.sqrt(b**2 + rMs**2)
rhs = sp.simplify(2*sp.pi*b*Sig)
check("dM_2D/db == 2 pi b Sigma_ph  (E- and K-forms are one system, EXACT)",
      sp.simplify(lhs - rhs) == 0)

print()
print("="*78)
print("numbers, both footings (isolated point/compact lens; spherical-pinned)")
print("="*78)
Gn, Msun, cn = 6.67430e-11, 1.98892e30, 2.99792458e8
kpc = 3.0857e19
arcsec = math.pi/180/3600
for tag, a0n in (("canonical", 9.362e-11), ("alt", 1.130e-10)):
    print(f"  [{tag}] a0={a0n:.4g}")
    for Mgal in (1e10, 1e11, 1e12):
        rMn = math.sqrt(Gn*Mgal*Msun/a0n)
        ainf = 2*math.pi*math.sqrt(Gn*Mgal*Msun*a0n)/cn**2
        vf = (Gn*Mgal*Msun*a0n)**0.25
        print(f"     M={Mgal:.0e} Msun: r_M={rMn/kpc:6.1f} kpc  alpha_inf={ainf/arcsec:.3f}\""
              f"  v_flat={vf/1e3:.0f} km/s")

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL CHECKS PASS")
sys.exit(1 if FAIL else 0)
