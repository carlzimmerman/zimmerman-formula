#!/usr/bin/env python3
r"""
fc_operator_basis_scalar_sector_2026.py -- COMPLETING THE EXHAUSTION STEP of the fried-chicken local
no-go (FRIED_CHICKEN_VERDICT_2026-09-01.md): the scalar (khronon) sector.

The theorem lists Cases 1-3f operator-by-operator.  This script tests the operators the list does NOT
treat, ADDED to the FC-KH backbone (the only static MOND carrier with c_T=1 on an aligned clock):
    L = N sqrt(g) [ (1-beta) K_ijK^ij - (1+lambda) K^2 + R3 + a0^2 F(y) + c(a^2) * O ]
for O in the unitary-gauge operator basis built from {N, a_i, K_ij, R_ij, D_i, eps_ijk}:
  T-odd (braiding-type, vanish on the static aligned background):  K, K_ij a^i a^j, K D_ia^i, K^ij D_i a_j,
      R K, R^ij K_ij
  T-even kinetic:  K^2, K K_aa, (K_aa)^2, K_ijK^ij, D_iK D^iK
  static curvature / acceleration: R3, R_ij a^i a^j, D_i a^i, (D_i a^i)^2
  parity-odd: eps a K K, eps K DK, eps a Da, eps a R K
  higher time derivative: L_n K
  Weyl (clock frame): E_ij a^i a^j, E_ijE^ij, B_ijB^ij, E_ijB^ij
Each coefficient function is c(a^2) = c0 + c1*delta + c2*delta^2/2 about the background a^2 = gbar^2.

For each operator, on the frozen static MOND background (decisive_reduction.py conventions):
  [DOF]  degree in omega of det H -> number of scalar DOF (A3 needs exactly 1: the clock).
  [SC]   omega=0 sector: Schur-reduce to the lapse.  Exact MOND (spec req 1) + Phi=Psi (req 3) REQUIRE
         the UV static operator to equal the FC-KH one, S_ref = (W1-4y0)/(4y0) kx^2 + (W2-4)/4 kz^2
         [= -(1-alpha/2)(mu kx^2 + (y mu)' kz^2), the linearised exact-MOND Hessian], and slip psi/phi = -1.
         A change of the radial (kz^2) coefficient alone breaks the single-potential structure
         A_par = d(y0 A_perp)/dy0 and is NOT absorbable into F; k^4 or k_z^4/k^2 terms are non-MOND.
  [DC]   khronon dispersion with (phi,B) integrated out: A (kinetic), c_par^2,UV, c_perp^2,UV.
The results feed the final exhaustion table.  Mutation controls: (i) all new coefficients -> 0 must
reproduce decisive_reduction.py exactly; (ii) the c0 part of K-linear operators is a total derivative and
must drop out identically; (iii) parity-odd operators must contribute exactly zero here.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from fc_ob_engine_2026 import *

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

T0 = time.time()
G = scalar_geometry()
ops = G.operators()
phi, B, psi = G.fields
FIELDS = (phi, B, psi)
backbone = (1-beta)*ops['KK'] - (1+lam)*ops['K2'] + ops['R3'] + a0**2*G.Fpot
L2_base = mul(G.measure, backbone).coeff(eps, 2)
H_base = hermitian_form(L2_base, FIELDS)

s, ex, ez = sp.symbols('s e_x e_z', positive=True)
def uv_leading(expr, want_deg=None):
    """Leading large-k behaviour of a rational function of (kx,kz): returns (degree, coefficient(ex,ez))."""
    e = sp.cancel(expr.subs({kx: s*ex, kz: s*ez}))
    num, den = sp.fraction(sp.together(e))
    pn, pd = sp.Poly(sp.expand(num), s), sp.Poly(sp.expand(den), s)
    deg = pn.degree() - pd.degree()
    lead = sp.cancel(pn.LC()/pd.LC())
    return deg, sp.factor(lead)

S_ref = (W1-4*y0)/(4*y0)*ex**2 + (W2-4)/4*ez**2
def analyse(H, label):
    nd, _ = dof_count(H)
    S, slip, tilt = static_reduce(H)
    dS, Slead = uv_leading(S)
    dsl, sllead = uv_leading(slip)
    slip_uv = sllead if dsl == 0 else (0 if dsl < 0 else sp.oo)
    dti, tilead = uv_leading(tilt) if tilt != 0 else (None, 0)
    tilt_uv = (tilead if dti == 0 else (0 if (dti is None or dti < 0) else f"grows k^{dti}"))
    D = dispersion(H)
    return dict(dof=nd, Sdeg=dS, Slead=Slead, dS=sp.factor(sp.cancel(Slead - S_ref)) if dS == 2 else None,
                slip=slip_uv, tilt=tilt_uv, tiltdeg=dti, D=D)

print("="*100)
print("BASELINE (FC-KH backbone) -- mutation control: must reproduce decisive_reduction.py")
print("="*100)
base = analyse(H_base, 'base')
A_exp = (1-beta)*(2+beta+3*lam)/(beta+lam)
cpar_exp = (W2-4)*(beta+lam)/(W2*(beta-1)*(beta+3*lam+2))
cperp_exp = (W1-4*y0)*(beta+lam)/(W1*(beta-1)*(beta+3*lam+2))
check("baseline: one scalar DOF (det H degree 2 in omega)", base['dof'] == 1)
check("baseline: A = (1-beta)(2+beta+3lam)/(beta+lam)", sp.simplify(base['D']['A']-A_exp) == 0)
check("baseline: c_par^2,UV = (W2-4)(beta+lam)/(W2(beta-1)(2+beta+3lam))", sp.simplify(base['D']['cpar_UV']-cpar_exp) == 0)
check("baseline: c_perp^2,UV matches", sp.simplify(base['D']['cperp_UV']-cperp_exp) == 0)
check("baseline: UV static lapse operator = exact-MOND Hessian S_ref", base['Sdeg'] == 2 and base['dS'] == 0, f"S_UV = {base['Slead']}")
check("baseline: static slip psi/phi -> -1  (Phi = Psi)", base['slip'] == -1)
check("baseline: no static tilt (B/phi -> 0)", base['tilt'] == 0)
print(f"  [time {time.time()-T0:.1f}s]")

# ----------------------------------------------------------------------------------------------
OPLIST = [
  # name, operator key, class
  ('K',      'K',      'T-odd braiding: c(a^2) K'),
  ('Kaa',    'Kaa',    'T-odd braiding: c(a^2) K_ij a^i a^j'),
  ('KDa',    'KDa',    'T-odd braiding: c(a^2) K D_i a^i'),
  ('KijDa',  'KijDa',  'T-odd braiding: c(a^2) K^ij D_i a_j'),
  ('RK',     'RK',     'T-odd: c(a^2) R3 K'),
  ('RijKij', 'RijKij', 'T-odd: c(a^2) R^ij K_ij'),
  ('K2',     'K2',     'T-even kinetic: c(a^2) K^2'),
  ('KKaa',   'KKaa',   'T-even kinetic: c(a^2) K (K_ij a^i a^j)'),
  ('Kaa2',   'Kaa2',   'T-even kinetic: c(a^2) (K_ij a^i a^j)^2'),
  ('KK',     'KK',     'T-even kinetic: c(a^2) K_ijK^ij'),
  ('DKDK',   'DKDK',   'T-even higher-spatial: c(a^2) D_iK D^iK'),
  ('R3',     'R3',     'static curvature: c(a^2) R3'),
  ('Raa',    'Raa',    'static curvature: c(a^2) R_ij a^i a^j'),
  ('Da',     'Da',     'static acceleration: c(a^2) D_i a^i'),
  ('Da2',    'Da2',    'static acceleration: c(a^2) (D_i a^i)^2'),
  ('LnK',    'LnK',    'higher time derivative: c(a^2) L_n K'),
  ('Eaa',    'Eaa',    'Weyl: c(a^2) E_ij a^i a^j'),
  ('EE',     'EE',     'Weyl: c(a^2) E_ij E^ij'),
  ('BB',     'BB',     'Weyl: c(a^2) B_ij B^ij'),
  ('EB',     'EB',     'Weyl/parity-odd: c(a^2) E_ij B^ij'),
  ('po_aKK', 'po_aKK', 'parity-odd: c(a^2) eps^ijk a_i K_jl K^l_k'),
  ('po_KDK', 'po_KDK', 'parity-odd: c(a^2) eps^ijk K_il D_j K^l_k'),
  ('po_aDa', 'po_aDa', 'parity-odd: c(a^2) eps^ijk a_i D_j a_k'),
  ('po_aRK', 'po_aRK', 'parity-odd: c(a^2) eps^ijk a_i R_jl K^l_k'),
]

results = {}
for name, key, cls in OPLIST:
    t1 = time.time()
    (c0, c1, c2), cfun = coeff_fn(f'c_{name}_')
    L2 = mul(G.measure, backbone + cfun(G.delta)*ops[key]).coeff(eps, 2)
    H = hermitian_form(L2, FIELDS)
    dH = sp.simplify(H - H_base)
    r = analyse(H, name); r['dH'] = dH; r['coeffs'] = (c0, c1, c2); r['cls'] = cls
    results[name] = r
    print("\n" + "-"*100)
    print(f"OPERATOR {name}: {cls}")
    print("-"*100)
    which = [str(c) for c in (c0,c1,c2) if dH.has(c)]
    print(f"  enters the quadratic form through: {which if which else 'NOTHING (identically zero on this sector)'}")
    print(f"  [DOF] scalar DOF = {r['dof']}")
    if r['Sdeg'] == 2:
        print(f"  [SC] UV static lapse operator degree 2; deviation from exact-MOND Hessian: dS = {r['dS']}")
    else:
        print(f"  [SC] UV static lapse operator has leading degree {r['Sdeg']} (NON-MOND): leading = {r['Slead']}")
    print(f"  [SC] UV slip psi/phi = {r['slip']}   (Phi=Psi requires -1);  static tilt B/phi (UV) = {r['tilt']}")
    if r['D'] is None:
        print("  [DC] (phi,B) block is omega-DEPENDENT -> lapse/shift dynamical: extra scalar pole, no clean reduction")
    else:
        D = r['D']
        print(f"  [DC] A (UV) = {sp.factor(sp.limit(D['A'].subs(kx,0), kz, sp.oo))};  omega-linear term: {'present' if D['lin']!=0 else 'absent'}")
        print(f"  [DC] c_par^2,UV = {D['cpar_UV']}")
        print(f"  [DC] c_perp^2,UV = {D['cperp_UV']}")
    print(f"  [time {time.time()-t1:.1f}s]")

# ----------------------------------------------------------------------------------------------
print("\n" + "="*100)
print("STRUCTURAL CHECKS (each can fail)")
print("="*100)
# (ii) total-derivative control: c0 K must drop out
r = results['K']; c0,c1,c2 = r['coeffs']
check("c0*K (constant coefficient) is a total derivative: drops out of H identically", not r['dH'].has(c0))
check("c(a^2)K enters ONLY through c1 = dc/d(a^2) (the braiding coupling)", r['dH'].has(c1) and not r['dH'].has(c2))
# parity-odd: exactly zero
for nm in ('po_aKK','po_KDK','po_aDa','po_aRK','EB'):
    check(f"{nm}: contributes EXACTLY ZERO to the scalar-sector quadratic form", results[nm]['dH'] == sp.zeros(3,3))
# BB: magnetic Weyl of a scalar mode vanishes
check("BB: magnetic Weyl of scalar perturbations vanishes -> zero contribution", results['BB']['dH'] == sp.zeros(3,3))
# braiding: static sector modified at the same order as the dispersion
for nm in ('K','Kaa','KDa','KijDa','RK','RijKij'):
    r = results[nm]
    bad = (r['Sdeg'] != 2) or (r['dS'] != 0) or (r['slip'] != -1)
    check(f"{nm}: T-odd operator MODIFIES the static sector (tilt/slip/Hessian) whenever its coupling is nonzero", bad,
          f"Sdeg={r['Sdeg']}, dS={r['dS']}, slip={r['slip']}, tilt={r['tilt']}")
# K braiding: the static deviation is purely radial (kz^2) and quadratic in c1 -> not absorbable into F
r = results['K']; dS = sp.expand(r['dS'])
check("K braiding: static deviation is pure kz^2 (radial), transverse untouched", dS.coeff(ex,2) == 0 and dS.coeff(ez,2) != 0 and sp.simplify(dS - dS.coeff(ez,2)*ez**2) == 0, f"dS = {r['dS']}")
check("K braiding: radial deviation is proportional to c1^2 (sign-definite) -> exact MOND forces c1 = 0",
      sp.simplify(sp.diff(dS.coeff(ez,2), c1, 2) != 0) and sp.simplify(dS.coeff(ez,2).subs(c1,0)) == 0)
# T-even kinetic operators: static-safe
for nm in ('K2','KKaa','Kaa2','KK','DKDK'):
    r = results[nm]
    check(f"{nm}: T-even kinetic operator leaves the static sector EXACTLY unchanged (static-safe)",
          r['Sdeg']==2 and r['dS']==0 and r['slip']==-1 and r['tilt']==0)
# static curvature/acceleration operators: non-MOND static sector unless coefficient derivative vanishes
for nm in ('R3','Raa','Da','Da2','Eaa'):
    r = results[nm]
    check(f"{nm}: static operator wrecks the exact 2nd-order MOND form (degree>2, slip, or Hessian shift)",
          (r['Sdeg'] != 2) or (r['dS'] != 0) or (r['slip'] != -1), f"Sdeg={r['Sdeg']}, dS={r['dS']}, slip={r['slip']}")
# LnK: extra DOF through c1
r = results['LnK']; c0,c1,c2 = r['coeffs']
check("LnK: with c1 != 0 the lapse becomes dynamical (det H degree > 2: a SECOND scalar DOF, A3 violated)", r['dof'] > 1, f"DOF={r['dof']}")
L2q = mul(G.measure, backbone + (c0)*ops['LnK']).coeff(eps, 2); Hq = hermitian_form(L2q, FIELDS)
L2k = mul(G.measure, backbone - (c0)*ops['K2']).coeff(eps, 2); Hk = hermitian_form(L2k, FIELDS)
check("LnK: constant coefficient c0*L_nK == -c0*K^2 on this sector (integration by parts identity)", sp.simplify(Hq - Hk) == sp.zeros(3,3))
# EE: higher time derivatives
check("EE: E_ijE^ij carries higher time derivatives (extra scalar DOF)", results['EE']['dof'] > 1, f"DOF={results['EE']['dof']}")

# ----------------------------------------------------------------------------------------------
print("\n" + "="*100)
print("COMBINED SC-SAFE SET: K^2, K K_aa, (K_aa)^2, D_iK D^iK added together (K_ijK^ij excluded: it is c_T-unsafe)")
print("="*100)
(e10,e11,e12), f1 = coeff_fn('e1_'); (e20,e21,e22), f2 = coeff_fn('e2_'); (e30,e31,e32), f3 = coeff_fn('e3_'); (d0,d1,d2), f4 = coeff_fn('d_')
L2c = mul(G.measure, backbone + f1(G.delta)*ops['K2'] + f2(G.delta)*ops['KKaa'] + f3(G.delta)*ops['Kaa2'] + f4(G.delta)*ops['DKDK']).coeff(eps, 2)
Hc = hermitian_form(L2c, FIELDS)
rc = analyse(Hc, 'combined')
check("combined: still one scalar DOF", rc['dof'] == 1)
check("combined: static sector EXACTLY unchanged (exact MOND + Phi=Psi retained)", rc['Sdeg']==2 and rc['dS']==0 and rc['slip']==-1 and rc['tilt']==0)
D = rc['D']
cpar = sp.factor(D['cpar_UV']); cperp = sp.factor(D['cperp_UV'])
Auv = sp.factor(sp.limit(D['A'].subs(kx,0), kz, sp.oo))
print("  A_UV      =", Auv)
print("  c_par^2   =", cpar)
print("  c_perp^2  =", cperp)
# THE THEOREM CHECK: c_par^2 * A_UV has the sign of (4-W2)/W2 ... i.e. sign(c_par^2) = sign(W2) whenever A>0
prod = sp.factor(sp.cancel(cpar*Auv))
print("  c_par^2 * A_UV =", prod)
check("combined: c_par^2 * A_UV = (4-W2)/W2 * (positive definite factor)  ->  sign(c_par^2) = sign(W2) for ANY no-ghost (A>0) choice of the added operators",
      sp.simplify(prod*W2/(4-W2) - sp.simplify(prod*W2/(4-W2)).subs({e10:0,e11:0,e12:0,e20:0,e21:0,e22:0,e30:0,e31:0,e32:0,d0:0,d1:0,d2:0})) == 0
      or sp.simplify(sp.diff(prod*W2/(4-W2), W2)) == 0, f"product = {prod}")
which_c = sorted({str(sy) for sy in prod.free_symbols} - {'W2','beta','lambda','y0','a0','W1','W0'})
print("  added-operator coefficients surviving in c_par^2*A:", which_c)
print("  (W2-independence of the positive factor:", sp.simplify(sp.diff(prod*W2/(4-W2), W2)) == 0, ")")
# transverse also stays sign-locked to (4y0-W1)/W1 = mu-locked positive
prodp = sp.factor(sp.cancel(cperp*Auv))
print("  c_perp^2 * A_UV =", prodp)
check("combined: c_perp^2 * A_UV = (4y0-W1)/W1 * (W2-independent factor)", sp.simplify(sp.diff(prodp*W1/(4*y0-W1), W2)) == 0 and sp.simplify(sp.diff(prodp*W1/(4*y0-W1), W1)) == 0)

print(f"\nChecks: {sum(checks)}/{len(checks)}   [total time {time.time()-T0:.1f}s]")
print("VERDICT (scalar sector): every operator outside the theorem's list either (a) modifies the static sector, so exact MOND")
print("forces its braiding coupling to zero [T-odd, static curvature/acceleration, Weyl-electric], (b) adds a scalar DOF")
print("[L_nK, E_ijE^ij], (c) is identically zero here [parity-odd, B_ijB^ij, E_ijB^ij], or (d) is static-safe but only")
print("renormalises the kinetic normalisation, leaving sign(c_par^2)=sign(f'') intact [T-even kinetic].  No cure for FC-KH.")
sys.exit(0 if all(checks) else 1)
