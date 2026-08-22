"""
frozen_dirac_sectors_2026.py
============================================================================
DECISIVE GATE: full DOF count of the FROZEN MINIMAL gravity+CMC action.
Is it 2+0 (2 tensor, NO propagating khronon scalar) or 2+1/3 (a propagating
khronon)?  We DERIVE it -- never "elliptic therefore non-dynamical".

FROZEN action (gravity + CMC sector; the MOND Phi is separately established
second-class = 0 DOF, so it is set aside here -- the question is the
GRAVITY+CMC scalar = the khronon):

  S_grav = (c^3/16piG) INT N sqrt(h) [ K_ij K^ij - lambda K^2 + xi (3)R
                                       + eta a_i a^i ],   a_i = D_i ln N
  S_CMC  = (c^3/16piG) INT N sqrt(h) Lambda_CMC (K - q(t))
           Lambda_CMC = LOCAL multiplier field; q = q(t) GLOBAL clock.

Method = linearized mode analysis around flat space (H->0 local limit), which
IS the local DOF count: a scalar with nonzero reduced kinetic coefficient and
real dispersion = 1 propagating DOF.  We keep (lambda, xi, eta) SYMBOLIC and
let the analysis FIX them (c_T=1 -> xi; the khronon (non)propagation -> eta).

Scalar gauge choice: spatial diffeo xi^i = D^i zeta removes E (longitudinal
metric scalar).  Remaining scalar fields: psi (conformal h), alpha (lapse),
beta (shift potential), dLam (CMC multiplier).  Only psi carries a time
derivative; alpha,beta,dLam are auxiliary.

Sectors:
 (1) TENSOR : c_T^2 = xi -> c_T=1 FIXES xi=1, kinetic +1/2 (no ghost).
 (2) SCALAR : reduce to psi; extract K_kin, c_s^2(lambda,xi,eta).
              -> K_kin = 6 (NONZERO, lambda- and eta-independent for eta!=0)
              -> khronon PROPAGATES: 2+1.  Removed ONLY at eta=0 (a_i a^i off,
                 lapse reverts to a Lagrange multiplier forcing psi=0 -> 2+0).
 (3) NEWTON : static khronon response G_eff(eta); the khronon is an EXTRA
              (dark) scalar since matter couples to Phi, not alpha.
"""
import sympy as sp

t, x, y, z, eps = sp.symbols('t x y z eps')
lam, xi, eta, k = sp.symbols('lambda xi eta k', real=True)

# =====================================================================
# (1) TENSOR SECTOR -- general xi ; lambda,eta do NOT touch TT
# =====================================================================
print("="*72)
print("(1) TENSOR SECTOR: TT graviton, general xi.  lambda*K^2 and eta*a_i a^i")
print("    do NOT contribute (K=0 and a_i=0 for a TT mode).  c_T^2 = xi.")
print("="*72)

gfun = sp.Function('gamma')
gam = gfun(t, z)
h = sp.Matrix([[1, eps*gam, 0],
               [eps*gam, 1, 0],
               [0, 0, 1]])
coords = [x, y, z]

def christoffel(hm, hi):
    G = [[[0]*3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                s = 0
                for d in range(3):
                    s += hi[a, d]*(sp.diff(hm[d, b], coords[c])
                                   + sp.diff(hm[d, c], coords[b])
                                   - sp.diff(hm[b, c], coords[d]))
                G[a][b][c] = sp.Rational(1, 2)*s
    return G

def ricci_scalar(hm):
    hi = hm.inv()
    Ch = christoffel(hm, hi)
    Ric = sp.zeros(3, 3)
    for b in range(3):
        for d in range(3):
            term = 0
            for a in range(3):
                term += sp.diff(Ch[a][b][d], coords[a]) - sp.diff(Ch[a][b][a], coords[d])
                for e in range(3):
                    term += Ch[a][a][e]*Ch[e][b][d] - Ch[a][d][e]*Ch[e][b][a]
            Ric[b, d] = term
    return sp.simplify(sum(hi[b, d]*Ric[b, d] for b in range(3) for d in range(3)))

hinv = h.inv()
sqrth = sp.sqrt(sp.simplify(h.det()))
R3 = ricci_scalar(h)
sqrthR3 = sp.expand(sp.series(sqrth*R3, eps, 0, 3).removeO())
grad_dens = sp.expand(sqrthR3.coeff(eps, 2))
gz, gzz, gt = sp.diff(gam, z), sp.diff(gam, z, 2), sp.diff(gam, t)
grad_ibp = sp.expand(grad_dens.subs(gam*gzz, -gz**2))       # IBP

Kdown = sp.Matrix(3, 3, lambda a, b: -sp.Rational(1, 2)*sp.diff(h[a, b], t))
KK = sum(Kdown[a, b]*Kdown[c, d]*hinv[a, c]*hinv[b, d]
         for a in range(3) for b in range(3) for c in range(3) for d in range(3))
Ktr = sum(hinv[a, b]*Kdown[a, b] for a in range(3) for b in range(3))
# general lambda in kinetic; for TT, Ktr=0 so lambda drops out identically:
kin_dens = sqrth*(KK - lam*Ktr**2)
kin_quad = sp.expand(sp.series(kin_dens, eps, 0, 3).removeO().coeff(eps, 2))

ckin = sp.simplify(kin_quad / gt**2)
cgrad = sp.simplify((xi*grad_ibp) / gz**2)       # gradient carries xi
cT2 = sp.simplify(-cgrad/ckin)
print("  kinetic coeff (d_t gamma)^2 :", ckin, "  (>0 => no ghost)")
print("  gradient coeff (d_z gamma)^2:", cgrad)
print("  c_T^2 = -cgrad/ckin =", cT2)
assert sp.simplify(cT2 - xi) == 0, "c_T^2 should equal xi"
print("  => c_T^2 = xi.  IMPOSE c_T=1  =>  xi = 1  (and kinetic +1/2, no ghost).")

# =====================================================================
# (2) SCALAR SECTOR -- the khronon.  Build the quadratic Lagrangian.
# =====================================================================
print()
print("="*72)
print("(2) SCALAR SECTOR: khronon DOF from the quadratic Lagrangian")
print("="*72)

psi, psidot, alpha, beta, dLam = sp.symbols('psi psidot alpha beta dLam', real=True)

# --- 2a. cross-check the (3)R conformal expansion used below (E=0 gauge) ---
# h_ij = (1+2 psi) delta_ij  (conformally flat).  Verify, with the SAME polynomial
# Ricci routine used in the tensor sector, that
#   INT sqrt(h) (3)R = 2 INT (D psi)^2   to 2nd order.
P = sp.Function('P')(x)                                 # psi profile, amplitude a
a = sp.symbols('a')
conf = 1 + 2*a*P
hc = sp.diag(conf, conf, conf)
sqrthc = sp.sqrt(sp.simplify(hc.det()))
R3c = ricci_scalar(hc)
dens = sp.series(sp.expand(sqrthc*R3c), a, 0, 3).removeO()
dens = sp.expand(dens)
lin = sp.expand(dens.coeff(a, 1))                      # linear = total deriv
qcoef = sp.expand(dens.coeff(a, 2))                    # O(a^2) density
Px, Pxx = sp.diff(P, x), sp.diff(P, x, 2)
qcoef_ibp = sp.expand(qcoef.subs(P*Pxx, -Px**2))       # IBP: drop total deriv
print("  (3)R cross-check: linear-in-psi density =", lin, " (total deriv -> 0)")
print("  quadratic density after IBP =", qcoef_ibp)
coef_grad_R = sp.simplify(qcoef_ibp / Px**2)
print("  => INT sqrt(h)(3)R = ", coef_grad_R, "* INT (D psi)^2   [analytic value: 2]")
assert coef_grad_R == 2, "conformal (3)R quadratic coefficient must be 2"

# --- 2b. assemble the quadratic scalar Lagrangian in Fourier space (mode k) ---
# Perturbations (spatial gauge E=0):
#   h_ij=(1+2psi)delta_ij, N=1+alpha, N_i=d_i beta, Lambda_CMC=dLam, q: no k!=0 part.
# K^(1)_ij = psidot*delta_ij - d_i d_j beta ;  K^(1) = 3 psidot - D^2 beta.
# Fourier: D^2 -> -k^2, (Df)^2 -> k^2 f^2, d_i d_j beta contracted etc.
#
# Kinetic (multiplies 1, since it is already O(2); background K=0):
#   K_ij^(1)K_ij^(1) - lambda (K^(1))^2
Kij_KK = 3*psidot**2 + 2*k**2*psidot*beta + k**4*beta**2      # = 3psi.^2 -2psi.*D^2b +(D^2b)^2
Ktr1sq = (3*psidot + k**2*beta)**2                            # (3psi. - D^2 b)^2 ; D^2b->-k^2 b
L_kin = Kij_KK - lam*Ktr1sq

# (3)R term:  xi * [ 2(Dpsi)^2 - 4 alpha D^2 psi ]  (E=0; N=1+alpha to O(2))
#   Fourier: (Dpsi)^2 -> k^2 psi^2 ; alpha D^2 psi -> -k^2 alpha psi
L_R = xi*(2*k**2*psi**2 + 4*k**2*alpha*psi)

# a_i a^i term:  eta*(D alpha)^2 -> eta k^2 alpha^2
L_a = eta*k**2*alpha**2

# CMC term: dLam * K^(1) = dLam*(3 psidot - D^2 beta) -> dLam*(3 psidot + k^2 beta)
L_cmc = dLam*(3*psidot + k**2*beta)

L2 = sp.expand(L_kin + L_R + L_a + L_cmc)
print()
print("  Quadratic scalar Lagrangian L2 (units c^3/16piG), Fourier mode k:")
print("   ", L2)

# --- 2c. eliminate the auxiliary fields (no time derivative): dLam, beta, alpha ---
print()
print("  Auxiliary fields alpha,beta,dLam carry NO time derivative.")
# dLam EOM  = CMC constraint: K^(1)=0  -> beta = -3 psidot / k^2
beta_sol = sp.solve(sp.diff(L2, dLam), beta)[0]
print("  dLam EOM (CMC constraint K^(1)=0):  beta =", beta_sol)
L2b = sp.expand(L2.subs(beta, beta_sol))
# after this, dLam multiplies (3psidot + k^2 beta)=0 -> dLam drops:
print("  after beta-substitution, coeff of dLam =", sp.simplify(L2b.coeff(dLam)),
      "(dLam is a genuine multiplier -> drops out)")
L2b = sp.expand(L2b.subs(dLam, 0))

print()
print("  --- branch eta != 0: alpha determined ALGEBRAICALLY (elliptic lapse) ---")
alpha_sol = sp.solve(sp.diff(L2b, alpha), alpha)[0]
print("  alpha EOM:  alpha =", sp.simplify(alpha_sol))
L2red = sp.expand(L2b.subs(alpha, alpha_sol))
L2red = sp.simplify(L2red)
Kkin = sp.simplify(L2red.coeff(psidot, 2))
Vgrad = sp.simplify(L2red.coeff(psi, 2))        # coeff of psi^2 (=+ in L)
print()
print("  REDUCED khronon Lagrangian:  L_red = Kkin*psidot^2 + Vgrad*psi^2")
print("     Kkin  =", Kkin, "   (reduced kinetic coefficient)")
print("     Vgrad =", sp.simplify(Vgrad), "   (coeff of psi^2 in L)")
# dispersion: L=Kkin*psidot^2 + Vgrad*psi^2 -> EOM 2Kkin psi.. - 2Vgrad psi=0
#   psi.. = (Vgrad/Kkin) psi  -> omega^2 = -(Vgrad/Kkin) k^2 ... (Vgrad already has k^2)
cs2 = sp.simplify(-Vgrad/Kkin/k**2)
print()
print("  Kkin (simplified)      :", sp.simplify(Kkin))
print("  scalar sound speed^2   : c_s^2 = -Vgrad/(Kkin k^2) =", cs2)
cs2_xi1 = sp.simplify(cs2.subs(xi, 1))
print("  at xi=1 (c_T=1)        : c_s^2 =", cs2_xi1, "  = (2-eta)/(3 eta)")

print()
print("  KEY FACTS (derived, not asserted):")
print("   * Kkin = 6  -- NONZERO, and INDEPENDENT of lambda AND eta (for eta!=0).")
print("     => the lambda*K^2 term and the kinetic-conformal point lambda=1/3 do")
print("        NOT freeze the scalar: the CMC constraint already fixes the trace,")
print("        so lambda drops out.  The khronon PROPAGATES.  ==> 2 + 1  (3 DOF).")
print("   * no ghost: Kkin=6>0.  no gradient instability iff c_s^2>=0 <=> 0<eta<2.")
print("   * c_s^2 -> +inf as eta->0  (mode becomes infinitely stiff = non-dynamical).")

# --- branch eta = 0: alpha becomes a Lagrange multiplier -> psi killed ---
print()
print("  --- branch eta = 0: a_i a^i OFF, alpha is a MULTIPLIER ---")
L2b0 = L2b.subs(eta, 0)
alpha_con = sp.simplify(sp.diff(L2b0, alpha))
print("  alpha EOM (eta=0) gives the Hamiltonian constraint:", alpha_con, "= 0")
print("  => xi*k^2*psi = 0  => psi = 0.  The khronon is REMOVED.  ==> 2 + 0.")
print("  (eta=0 kills the very a_i a^i term the action calls the khronon kinetic")
print("   term; it is GR+CMC, not the frozen khronometric action.)")

# --- 2d. HOSTILE CROSS-CHECK: coupled Euler-Lagrange, no substitution shortcut ---
# Promote fields to functions of t; ansatz f(t)=F*exp(i omega t); auxiliaries have
# no time deriv so their EL eqs are algebraic constraints.  Build the 4x4 system
# in (psi,alpha,beta,dLam), demand det=0, read the nontrivial omega^2(k) branch.
print()
print("  --- hostile cross-check: full 4-field EL system, independent route ---")
om = sp.symbols('omega', real=True)
tt = sp.symbols('tt')
Fpsi, Fal, Fbe, Fdl = (sp.Function('Fpsi')(tt), sp.Function('Fal')(tt),
                       sp.Function('Fbe')(tt), sp.Function('Fdl')(tt))
# Lagrangian as a functional of the four time-functions:
L2t = (3*sp.diff(Fpsi, tt)**2 + 2*k**2*sp.diff(Fpsi, tt)*Fbe + k**4*Fbe**2
       - lam*(3*sp.diff(Fpsi, tt) + k**2*Fbe)**2
       + xi*(2*k**2*Fpsi**2 + 4*k**2*Fal*Fpsi)
       + eta*k**2*Fal**2
       + Fdl*(3*sp.diff(Fpsi, tt) + k**2*Fbe))
def EL(F):
    dL_dXdot = sp.diff(L2t, sp.diff(F, tt))
    dL_dX = sp.diff(L2t, F)
    return sp.expand(sp.diff(dL_dXdot, tt) - dL_dX)
eqs = [EL(Fpsi), EL(Fal), EL(Fbe), EL(Fdl)]
# plane-wave ansatz F_i(t) = Amp_i * exp(i omega t)
Psi, Al, Be, Dl = sp.symbols('Psi Al Be Dl')
sub = {Fpsi: Psi*sp.exp(sp.I*om*tt), Fal: Al*sp.exp(sp.I*om*tt),
       Fbe: Be*sp.exp(sp.I*om*tt), Fdl: Dl*sp.exp(sp.I*om*tt)}
amps = [Psi, Al, Be, Dl]
Mrow = []
for e in eqs:
    e2 = sp.expand((e.subs(sub).doit()) / sp.exp(sp.I*om*tt))
    Mrow.append([sp.simplify(e2.coeff(av)) for av in amps])
Mmat = sp.Matrix(Mrow)
detM = sp.simplify(Mmat.det())
print("    det of 4x4 EL system (should factor out the physical branch):")
print("    det =", sp.factor(detM))
# solve det=0 for omega^2 (drop trivial k-power prefactors)
sol = sp.solve(sp.Eq(detM, 0), om**2)
sol = [sp.simplify(s) for s in sol]
print("    omega^2 solution(s):", sol)
cs2_check = sp.simplify(sol[0].subs(xi, 1)/k**2) if sol else None
print("    => c_s^2 (xi=1) from det route =", cs2_check,
      "  (matches (2-eta)/(3 eta)?", sp.simplify(cs2_check - (2-eta)/(3*eta)) == 0, ")")
assert sol, "system must have a propagating omega^2 branch (khronon dynamical)"
assert sp.simplify(cs2_check - (2-eta)/(3*eta)) == 0, "det-route c_s^2 mismatch"
print("    CONFIRMED by the independent route: exactly ONE propagating scalar branch.")

# =====================================================================
# (3) NEWTONIAN LIMIT -- G_eff and the extra-scalar problem
# =====================================================================
print()
print("="*72)
print("(3) NEWTONIAN LIMIT")
print("="*72)
print("  Matter couples to Phi (MOND scalar), NOT to the lapse alpha: the")
print("  Newtonian force on matter is set by  D.[mu(|DPhi|/a0) DPhi]=4piG rho,")
print("  mu->1  => G_eff(matter) = G by construction of the Phi equation.")
print("  The khronon alpha is therefore an EXTRA (dark) gravitational scalar,")
print("  static response  alpha = -(2 xi/eta) psi,  D^2 psi sourced through the")
print("  coupled (psi,alpha) elliptic system.  With xi=1 its static kernel is")
print("  D^2 alpha - (2/eta) ... ; strength ~ 1/eta.  It is a genuine 3rd DOF")
print("  whose PPN/stability bounds must be met (0<eta<2 for c_s^2>=0), NOT a")
print("  gauge artefact.  There is no G_eff(lambda,eta)=G tuning that removes it;")
print("  removal requires eta=0 (no khronon) OR re-expressing Lambda_CMC as a")
print("  GLOBAL York gauge-fixing (not a local multiplier field).")

# =====================================================================
# (4) DIRAC DOF BOOKKEEPING (per space point)
# =====================================================================
print()
print("="*72)
print("(4) DOF BOOKKEEPING (gravity+CMC scalar sector, per space point)")
print("="*72)
print("""  Phase-space scalars: (psi,p_psi), (E,p_E), plus lapse alpha, shift beta,
  multiplier dLam (all non-dynamical).  Gauge-fix E=0 with the spatial diffeo.

  eta != 0 (frozen action):
    - alpha is AUXILIARY (eta a^2 term) -> its EOM DETERMINES alpha (elliptic
      lapse); it is NOT a first-class Hamiltonian constraint -> it does NOT
      remove psi.
    - dLam enforces ONE constraint K^(1)=0 (CMC) -> fixes beta.
    - Net: 1 first-class constraint pair used on (beta), psi survives with
      Kkin=6 -> 1 propagating scalar.   TENSOR = 2.   TOTAL = 2 + 1 = 3 DOF.

  eta = 0 (a_i a^i off):
    - alpha becomes a LAGRANGE MULTIPLIER -> Hamiltonian constraint xi*D^2 psi=0
      -> psi=0.   With the CMC constraint too, both scalar constraints act ->
      TOTAL = 2 + 0 = 2 DOF (GR in CMC gauge).
""")

# =====================================================================
# VERDICT
# =====================================================================
print("="*72)
print("VERDICT")
print("="*72)
assert sp.simplify(Kkin - 6) == 0, "reduced khronon kinetic must be 6"
assert sp.simplify(cs2_xi1 - (2 - eta)/(3*eta)) == 0, "c_s^2 mismatch"
print("""  The FROZEN MINIMAL gravity+CMC action, taken literally (eta a_i a^i present,
  Lambda_CMC a LOCAL multiplier field), is  2 + 1  = 3 DOF: it PROPAGATES a
  khronon scalar.  Coefficients FIXED by the analysis:
      xi = 1                     (c_T = 1; tensor kinetic +, no ghost)
      Kkin = 6 (>0)              (khronon ghost-free, lambda- & eta-independent)
      c_s^2 = (2 - eta)/(3 eta)  (khronon sound speed at xi=1)
  2+0 is recovered ONLY by eta = 0 (which DELETES the khronon kinetic term, i.e.
  it is no longer the frozen khronometric action -- it is GR+CMC), OR by
  re-expressing the CMC sector as a GLOBAL York gauge-fixing instead of a local
  Lambda_CMC(K-q) multiplier field.  The lambda=1/3 kinetic-conformal escape does
  NOT apply once the CMC multiplier is present (lambda cancels).

  => As frozen, the DECISIVE GATE returns 2+1 (a propagating khronon), NOT 2+0.
""")
print("ALL ASSERTIONS PASSED.")
