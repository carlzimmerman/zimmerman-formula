#!/usr/bin/env python3
"""
AS240-r1  derive (sympy, exact algebra)
========================================
Seed AS240 "Compute gravitational-wave amplitude transport" (Tier-0b), CA5-GNC-R
physical-metric branch, homogeneous expanding inactive FRW branch (FINAL_ACTION
sec.7: f=G=0, z=0, a=DU=DZ=0, Q_K=0, Friedmann 3M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d,
G_cosm/G_N = c_N = 1 - alpha/2).

Contents
  D1  Direct action check: quadratic TT-tensor Lagrangian from g = a^2 eta + a^2 h_TT
      (h_+ polarization, plane wave along x^3). Extract coefficient ratio (q')^2 : (dq)^2
      and the Euler-Lagrange operator -> EOM q'' + 2 Hq' - d3^2 q = 0 (speed exactly 1).
  D2  First-order extrinsic-curvature trace for the pure TT mode: K^(1) = 0, so the
      c2 Q_K^2 / a|a-DZ|^2 / gate / heat terms have NO quadratic TT piece (scalar fields
      decouple at quadratic order on a homogeneous isotropic background).
  D3  WKB collector: L[q] with L = d_eta^2 + 2H d_eta - d_x^2 acting on A(eta) e^{i S/eps},
      S = -omega eta + k x.  Collect powers of 1/eps:
        eps^-2 (eikonal):  (k^2 - omega^2) A = 0  ->  omega = +|k|
        eps^-1 (transport): -2 i ( omega (A' + H A) + k A_x ) / eps = 0
        plane envelope A(eta):  A' + H A = 0  ->  A = A0 a0 / a   (substitution residual 0)
        eps^0 (subleading): A'' + 2 H A' = -A0 a0 (H' + H^2)/a  != 0  -> relative
        correction of order (H/omega)^2 (verified numerically in as240_numeric.py N2).
  D4  Luminosity bookkeeping (step 3): with D_L = (1+z) D_M = (1+z)^2 D_A and the
      transport law, the GW flux F = kappa omega^2 A^2 dilutes exactly like the photon
      flux, so the luminosity-distance inferred from the strain equals the EM one:
      D_L^GW = D_L^EM identically (constant M_P^2 = 1/(8 pi G_bare)).
  D5  Negative-control algebra: a changed G-normalization (G_N instead of G_bare,
      c_N = 1 - alpha/2 constant) rescales the strain by sqrt(c_N), a z-INDEPENDENT
      factor (calibration), i.e. d/dz[ln sqrt(c_N) h] = d/dz[ln h]; a genuine friction
      term has d/dz[ln h_fric] = -gamma/(1+z) + ... != 0. Hypothetical z-dependent
      coupling G_* (z): D_L^GW/D_L^EM = sqrt(G_*(z)/G_*(0)) (derived here), which for
      the action's constant G_bare is identically 1.
  D6  Both a0 footings kept separate (canonical 9.3619e-11, alternative 1.1279e-10):
      rho_Lambda at fixed kappa=1/2, kappa_eff at fixed rho_Lambda. The transport law
      itself is dimensionless and contains no a0 -> identical statement on both footings.

All symbolic residuals printed; every check must show residual == 0.
Constants: G=6.67430e-11, c=299792458, M_sun=1.98847e30, pc=3.085677581491367e16 (SI).
"""
import sympy as sp

eta, x3, k, omega, eps = sp.symbols('eta x3 k omega epsilon', positive=True)
A0, a0, aT = sp.symbols('A0 a0 aT', positive=True)          # aT = a(eta0)
Hbar = sp.Function('Hbar')                                   # conformal Hubble H = a'/a
a = sp.Function('a')

print("=" * 78)
print("AS240-r1 derive: exact algebra (sympy), run id AS240-r1-20260928T202950Z-dsv4f-hermes")
print("=" * 78)

# ----------------------------------------------------------------------------------
# D1  Direct quadratic TT-tensor action from the metric
# ----------------------------------------------------------------------------------
print("\n[D1] Quadratic TT-tensor Lagrangian directly from g = a^2 eta + a^2 h_TT")
# metric in conformal time, mostly-plus; h_+ plane wave along x^3:
#   h_11 = -h_22 = q(eta,x3), TT: h_ii=0, d_i h_ij=0, trace 0.
# use explicit symbols for q and its derivatives
q = sp.Function('q')
q_eta = sp.Function('q_eta')
q_x = sp.Function('q_x')
q_ee = sp.Function('q_ee')
q_ex = sp.Function('q_ex')
q_xx = sp.Function('q_xx')

# Christoffel symbols for g = diag(-a^2, a^2(1+q), a^2(1-q), a^2), indices (eta, x1, x2, x3)
# Compute with sympy's array machinery on explicit symbolic derivatives.
a_sym = sp.Function('a', positive=True)
E = sp.symbols('E', positive=True)  # bookkeeping small parameter for the TT perturbation
# metric components (lower):
g00m = -a_sym(eta) ** 2
g11m = a_sym(eta) ** 2 * (1 + E * q(eta, x3))
g22m = a_sym(eta) ** 2 * (1 - E * q(eta, x3))
g33m = a_sym(eta) ** 2
gm = sp.Matrix([[g00m, 0, 0, 0],
                [0, g11m, 0, 0],
                [0, 0, g22m, 0],
                [0, 0, 0, g33m]])
# inverse metric: exact inverse of the diagonal metric
gu = sp.Matrix([[1 / g00m, 0, 0, 0],
                [0, 1 / g11m, 0, 0],
                [0, 0, 1 / g22m, 0],
                [0, 0, 0, 1 / g33m]])

coords = [eta, sp.Symbol('x1'), sp.Symbol('x2'), x3]

def d(i, f):
    """partial derivative of f w.r.t. coordinate i"""
    if i == 0:
        return sp.diff(f, eta)
    return sp.diff(f, coords[i])

# Christoffel: Gamma^mu_{nu rho} = (1/2) g^{mu sigma} (d_nu g_{sigma rho} + d_rho g_{sigma nu} - d_sigma g_{nu rho})
Gam = [[[None] * 4 for _ in range(4)] for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        for rho in range(4):
            s = 0
            for sigma in range(4):
                s += gu[mu, sigma] * (d(nu, gm[sigma, rho]) + d(rho, gm[sigma, nu]) - d(sigma, gm[nu, rho]))
            Gam[mu][nu][rho] = sp.expand(s / 2)

# Ricci: R_{mu nu} = d_rho Gamma^rho_{mu nu} - d_nu Gamma^rho_{mu rho} + Gamma^rho_{rho sigma} Gamma^sigma_{mu nu} - Gamma^rho_{nu sigma} Gamma^sigma_{mu rho}
Ric = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        s = 0
        for rho in range(4):
            s += d(rho, Gam[rho][mu][nu]) - d(nu, Gam[rho][mu][rho])
        for rho in range(4):
            for sigma in range(4):
                s += Gam[rho][rho][sigma] * Gam[sigma][mu][nu] - Gam[rho][nu][sigma] * Gam[sigma][mu][rho]
        Ric[mu, nu] = sp.expand(s)

# R = g^{mu nu} R_{mu nu}; scalar curvature
Rsc = sp.expand(sum(gu[mu, nu] * Ric[mu, nu] for mu in range(4) for nu in range(4)))
# sqrt(-g)
gmdet = sp.expand(gm.det())
sdet = sp.sqrt(sp.simplify(-gmdet))

# quadratic-in-q Lagrangian density (per unit coordinate volume, M_P^2/2 prefactor dropped for now)
Ldens = sp.series(sp.expand(sdet * Rsc), E, 0, 3).removeO()
L2 = sp.expand(sp.diff(Ldens, E, 2) / 2)   # E^2 coefficient (action density ~ sqrt(-g) R, quad. part)

# --- exact Euler-Lagrange operator on L2 (q depends on (eta,x3), a on eta only) ---
Dq = sp.Derivative(q(eta, x3), eta)
Dqx = sp.Derivative(q(eta, x3), x3)
Dq2 = sp.Derivative(q(eta, x3), (eta, 2))
Dqxx = sp.Derivative(q(eta, x3), (x3, 2))
Dqex = sp.Derivative(q(eta, x3), eta, x3)

def Deta(f):
    return sp.expand(sp.diff(f, eta))
def Dx3(f):
    return sp.expand(sp.diff(f, x3))

EL = sp.expand(
    sp.diff(L2, q(eta, x3))
    - Deta(sp.diff(L2, Dq))
    - Dx3(sp.diff(L2, Dqx))
    + Deta(Deta(sp.diff(L2, Dq2)))
    + Dx3(Dx3(sp.diff(L2, Dqxx)))
    + Deta(Dx3(sp.diff(L2, Dqex)))
)
EL = sp.expand(EL)
# normal form: collect the four independent derivative patterns
pats = [sp.Derivative(q(eta, x3), (eta, 2)), sp.Derivative(q(eta, x3), (x3, 2)),
        sp.Derivative(q(eta, x3), eta), sp.Derivative(q(eta, x3), x3), q(eta, x3)]
co = {p: sp.simplify(sp.diff(EL, p)) for p in pats}
EL_res = sp.expand(EL - sum(co[p] * p for p in pats))
print("EL residual after exact coefficient extraction (must be 0):", sp.simplify(EL_res))
assert sp.simplify(EL_res) == 0
kappa = sp.simplify(co[pats[0]])            # coefficient of q''
kappa2 = sp.simplify(-co[pats[1]])          # expected +kappa for the -q_xx term
fric = sp.simplify(co[pats[2]] / kappa)     # friction coefficient / kappa
print("kappa (coeff q''):", sp.factor(kappa))
print("-coeff q_xx (must equal kappa):", sp.factor(kappa2))
print("friction/kappa - 2 a'/a (must be 0):", sp.factor(fric - 2 * sp.diff(a_sym(eta), eta) / a_sym(eta)))
assert sp.simplify(kappa2 - kappa) == 0, "D1 speed^2 != 1"
assert sp.simplify(fric - 2 * sp.diff(a_sym(eta), eta) / a_sym(eta)) == 0, "D1 friction != 2H"
# canonical (IBP-normalized) kinetic and spatial coefficients of the quadratic action density L2
c1 = sp.simplify(sp.diff(L2, Dq, 2) / 2)                         # coeff of q'^2
c2 = sp.simplify(sp.diff(sp.diff(L2, Dq2), q(eta, x3)))          # coeff of q''*q  (-> -q'^2 under IBP)
c3 = sp.simplify(sp.diff(L2, Dqx, 2) / 2)                        # coeff of q_x^2
c4 = sp.simplify(sp.diff(sp.diff(L2, Dqxx), q(eta, x3)))         # coeff of q_xx*q (-> -q_x^2 under IBP)
c_kin = sp.simplify(c1 - c2)                                     # canonical kinetic coefficient
c_spa = sp.simplify(c3 - c4)                                     # canonical gradient coefficient
print("canonical kinetic coefficient (must be +a^2/2 > 0):", sp.factor(c_kin))
print("canonical gradient coefficient:", sp.factor(c_spa))
assert sp.simplify(c_kin - a_sym(eta) ** 2 / 2) == 0, "D1 canonical kinetic != +a^2/2 (tensor kinetic sign!)"
assert sp.simplify(-c_spa / c_kin - 1) == 0, "D1 canonical speed^2 != 1"
print("[D1] FAIL-CAPABLE action check: EOM = kappa * [q'' + 2 H q' - d3^2 q] = 0, kappa =",
      sp.factor(kappa), "; quadratic action = (M_P^2/2)*(a^2/2)[q'^2 - (d3 q)^2] -> POSITIVE tensor kinetic "
      "energy (requirement 6), speed^2 = 1 exactly, friction +2H (expanding branch damps).")

# ----------------------------------------------------------------------------------
# D2  K^{(1)} for the pure TT mode vanishes -> no quadratic TT piece from c2 Q_K^2 etc.
# ----------------------------------------------------------------------------------
print("\n[D2] First-order trace of extrinsic curvature for pure TT mode")
# cosmic-time convention N=1, shift=0: K_ij = (1/2) ḣ_ij + ... ; conformal: K^(1)_ij = (1/(2a^2)) h_ij'
# trace: K^(1) = h^(0)ij K^(1)_ij = (1/(2a^2)) δ_ij h_ij'  (comoving indices)
h11p = sp.Function('q')(eta, x3).diff(eta)
K1_trace = sp.simplify((1 / (2 * a_sym(eta) ** 2)) * (h11p - h11p))   # h_11' + h_22' = q' - q' = 0
print("K^(1) for h_+ mode (q,-q,0):", K1_trace, " -> exactly 0")
assert sp.simplify(K1_trace) == 0
print("[D2] Q_K^(1) = K^(1) - <K^(1)>_h = 0; the (K^(1))^2 quadratic-TT piece of c2 Q_K^2 vanishes. "
      "Scalar/tensor decoupling at quadratic order on the homogeneous isotropic background -> "
      "the TT operator is the Einstein one (FINAL_ACTION sec.6 reduced form, weight a^2 in conformal time).")

# ----------------------------------------------------------------------------------
# D3  WKB collector
# ----------------------------------------------------------------------------------
print("\n[D3] WKB: L[q] = d_eta^2 + 2 H d_eta - d_x^2 on A(eta) e^{i S/eps}, S = -omega eta + k x")
Hf = sp.Function('H')(eta)          # conformal Hubble, = a'/a
A = sp.Function('A')(eta)
S = -omega * eta + k * x3
psi = A * sp.exp(sp.I * S / eps)
def applyL(f):
    return sp.diff(f, eta, 2) + 2 * Hf * sp.diff(f, eta) - sp.diff(f, x3, 2)
res = sp.expand(applyL(psi))
# factor out exp(i S/eps); expand around eps = infinity -> collect powers of 1/eps
res_series = sp.series(res * sp.exp(-sp.I * S / eps), eps, sp.oo, 3).removeO()
# terms: c0 + c1 * (1/eps) + c2 * (1/eps^2); extract
def coeff_of_inv_pow(fexpr, n):
    return sp.expand(sp.simplify(sp.diff(fexpr * eps ** n, eps, n) / sp.factorial(n)) .subs(eps, sp.oo))
# simpler: substitute u = 1/eps and expand in u at 0
u = sp.symbols('u')
res_u = sp.simplify(sp.series((res * sp.exp(-sp.I * S / eps)).subs(eps, 1 / u), u, 0, 3).removeO())
c0 = sp.expand(sp.simplify(res_u.coeff(u, 0)))
c1 = sp.expand(sp.simplify(res_u.coeff(u, 1)))
c2 = sp.expand(sp.simplify(res_u.coeff(u, 2)))
print("eps^-2 (eikonal) coefficient:", sp.factor(c2))
print("eps^-1 (transport) coefficient:", sp.factor(c1))
print("eps^0  coefficient:", sp.factor(c0))
# eikonal: with omega = |k| the eps^-2 piece vanishes:
c2_sub = sp.simplify(c2.subs(omega, k))
print("eikonal residual at omega = k :", c2_sub, " (must be 0)")
assert sp.simplify(c2_sub) == 0
# transport for plane envelope (A independent of x3): -2 i omega (A' + H A) = 0
c1_A = sp.simplify(c1.subs(sp.diff(A, x3), 0))
print("transport coefficient (A_x = 0):", sp.factor(c1_A))
t1 = sp.simplify(c1_A / (-2 * sp.I * omega))
print("transport equation: A' + H A = 0  (residual form:", sp.factor(t1), ")")
# substitute the solution A = A0 a0/a (a in conformal time; H = a'/a)
solve_sub = sp.simplify(t1.subs(A, A0 * a0 / a_sym(eta)).subs(Hf, sp.diff(a_sym(eta), eta) / a_sym(eta)))
print("substitution residual of A = A0 a0/a into the transport equation:", solve_sub, " (must be 0)")
assert sp.simplify(solve_sub) == 0
print("[D3] transport law: A(eta) = A0 a0 / a(eta);  substitution residual 0 EXACT.")
# eps^0 piece with the WKB amplitude: (A'' + 2 H A') - nonzero -> O((H/omega)^2) correction
c0_sub = sp.simplify(c0.subs(A, A0 * a0 / a_sym(eta)).subs(Hf, sp.diff(a_sym(eta), eta) / a_sym(eta)))
c0_sub = sp.simplify(c0_sub.subs(sp.diff(a_sym(eta), eta, 2), sp.diff(a_sym(eta), eta) ** 2 / a_sym(eta) + (sp.diff(a_sym(eta), eta) / a_sym(eta)).diff(eta) * a_sym(eta)))
print("eps^0 residual with A = A0 a0/a:", sp.factor(c0_sub), " (!= 0: subleading correction, relative order (H/omega)^2)")

# ----------------------------------------------------------------------------------
# D4  Luminosity-distance identity (step 3)
# ----------------------------------------------------------------------------------
print("\n[D4] D_L^GW = D_L^EM for constant M_P (flux bookkeeping)")
z, DL, rM, kap, Lem = sp.symbols('z DL rM kap Lem', positive=True)
aem = sp.symbols('aem', positive=True)          # a at emission
aob = sp.symbols('aob', positive=True)          # a at observer
Aem, om_e, Aob, om_o = sp.symbols('Aem om_e Aob om_o', positive=True)
oneplusz = aob / aem                            # 1+z
# transport: Aob = Aem * aem/aob, om_o = om_e * aem/aob  (redshift of frequency)
Aob_t = Aem * aem / aob
omo_t = om_e * aem / aob
# source-frame luminosity through the emission sphere of comoving radius rM:
L_gw = 4 * sp.pi * (aem * rM) ** 2 * kap * om_e ** 2 * Aem ** 2
# D_L^GW defined by 4 pi D_L^2 F_obs = L, F_obs = kap om_o^2 Aob^2 with the transport (Aob_t, omo_t):
D_LGW2 = sp.simplify(L_gw / (4 * sp.pi * kap * omo_t ** 2 * Aob_t ** 2))
print("D_L^GW^2 = ", sp.factor(D_LGW2))
D_LGW = sp.simplify(sp.sqrt(D_LGW2))
# EM: D_L = (1+z) D_M, D_M = aob * rM  (flat FRW, c=1)
D_LEM = sp.simplify(oneplusz * aob * rM)
print("D_L^EM   = ", D_LEM)
ratio_DL = sp.simplify(D_LGW / D_LEM)
print("D_L^GW / D_L^EM - 1 =", sp.simplify(ratio_DL - 1), " (must be 0)")
assert sp.simplify(ratio_DL - 1) == 0
print("[D4] D_L^GW = D_L^EM identically (constant M_P^2 = 1/(8 pi G_bare)); no extra damping, "
      "no varying mass, same null rays of the single physical metric g.")
# dimensionless statement: applies to both a0 footings (no a0 anywhere in D4)

# ----------------------------------------------------------------------------------
# D5  Negative control: G-normalization vs propagation friction
# ----------------------------------------------------------------------------------
print("\n[D5] Negative control algebra: G_N normalization is calibration, not friction")
cN = sp.symbols('cN', positive=True)            # c_N = 1 - alpha/2 = G_N/G_bare (FINAL_ACTION eq.18)
z0 = sp.symbols('z0', positive=True)
h_true = sp.Function('h')(z)                    # strain from the true transport
h_cal = sp.sqrt(cN) * h_true                    # mis-calibrated strain (G_N instead of G_bare)
# z-dependence of the log ratio: calibration is z-independent
res_cal = sp.simplify(sp.diff(sp.log(h_cal / h_true), z))
print("d/dz ln(h_cal/h) =", res_cal, " (must be 0: calibration is z-independent)")
assert sp.simplify(res_cal) == 0
# genuine friction form exp(-gamma phi(z)): its log derivative is z-dependent
gam, phi = sp.symbols('gam', positive=True), sp.Function('phi')(z)
h_fric = h_true * sp.exp(-gam * phi)
res_fric = sp.simplify(sp.diff(sp.log(h_fric / h_true), z))
print("d/dz ln(h_fric/h) =", res_fric, " (z-dependent for non-constant phi: friction)")
assert sp.simplify(res_fric) != 0
# hypothetical z-dependent coupling G_*(z): derived strain-distance ratio
Gst = sp.Function('Gst')(z)
h_Gst = sp.sqrt(Gst) * h_true / sp.sqrt(Gst.subs(z, 0))      # relative to z=0 coupling
ratio_Gst = sp.simplify(h_Gst / h_true)
print("hypothetical G_*(z): h/h0 = sqrt(G_*(z)/G_*(0)) -> D_L^GW/D_L^EM =", sp.simplify(1 / ratio_Gst))
res_Gst = sp.simplify(sp.diff(sp.log(ratio_Gst), z))
print("d/dz ln(ratio) for varying G_*:", res_Gst, " (nonzero iff G_* varies)")
# action cell: G_bare constant by the action -> c_N constant -> residual 0 for ALL z => distinction checked
print("[D5] In CA5-GNC-R the tensor kinetic coupling M_P^2 = 1/(8 pi G_bare) is constant and "
      "G_cosm/G_N = c_N = 1 - alpha/2 is exactly z-independent, so a wrong-G_N calibration is "
      "absorbed by sqrt(c_N) (amplitude calibration) and CANNOT masquerade as a friction term. "
      "Numeric discrimination in as240_numeric.py (NC-1, NC-2, NC-3).")

# ----------------------------------------------------------------------------------
# D6  Footings
# ----------------------------------------------------------------------------------
print("\n[D6] Both a0 footings, separate")
Gc = sp.Float("6.67430e-11"); c = sp.Float("299792458")
a0c = sp.Float("9.3619e-11"); a0a = sp.Float("1.1279e-10")
rhoL_c = 4 * a0c ** 2 / (Gc * c ** 2)
rhoL_a = 4 * a0a ** 2 / (Gc * c ** 2)
kap_eff = a0a / (sp.sqrt(Gc * rhoL_c) * c)
rhoL_a_fk = 4 * a0a ** 2 / (Gc * c ** 2)
epsL_c = rhoL_c * c ** 2
epsL_a = rhoL_a * c ** 2
print("canonical  a0 = 9.3619e-11 m/s^2 (kappa = 1/2 adopted): rho_Lambda =", sp.N(rhoL_c, 16), "kg/m^3;",
      " eps_Lambda =", sp.N(epsL_c, 16), "J/m^3;  kappa = 1/2 (adopted input, not derived)")
print("alternative a0 = 1.1279e-10 m/s^2 at fixed rho_Lambda (canonical): kappa_eff =", sp.N(kap_eff, 10), "(!= 1/2)")
print("alternative a0 = 1.1279e-10 m/s^2 at fixed kappa = 1/2: rho_Lambda' =", sp.N(rhoL_a_fk, 16), "kg/m^3;",
      " eps_Lambda' =", sp.N(epsL_a, 16), "J/m^3")
print("Transport law is dimensionless (A prop 1/a; D_L^GW/D_L^EM = 1): identical on BOTH footings; "
      "a0 enters only the static/gate sector, absent in the propagation-only tensor law.")
assert sp.N(kap_eff, 6) != sp.Float("0.5")
assert abs(sp.N(rhoL_c / sp.Float("5.844412454e-27"), 6) - 1) < 1e-5
assert abs(sp.N(rhoL_a_fk / sp.Float("8.483090e-27"), 6) - 1) < 1e-4
print("footing cross-consistency with AS658/AS215 run constants: OK")

print("\nALL DERIVE CHECKS PASSED (D1-D6, residuals exact 0 where required).")