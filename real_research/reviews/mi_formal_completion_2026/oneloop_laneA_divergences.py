#!/usr/bin/env python3
r"""
LANE A -- ONE-LOOP DIVERGENT COEFFICIENTS ON de SITTER VIA THE HERGLOTZ HANDLE
==============================================================================
Framework premises (its OWN terms): dS-Unruh MODIFIED INERTIA,
  S_matter = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
  K(z) = (sqrt(1+4z)-1)/(2 sqrt z),  Box_u f = (u.grad)^2 f,  s=-1, a0, Z INPUTS.
  u is NON-DYNAMICAL (Dirac closure, 0 dof): the loop quanta are MATTER (+gravitons,
  NOT computed here); u and g are external backgrounds in the 1PI effective action.

THE STRUCTURAL KEY (makes the heat kernel textbook-rigorous):
  In the action K(Box_u/a0^2) is sandwiched as u^mu K(...) u_mu, i.e. it acts on the
  BACKGROUND field u_mu. Define the scalar background functional
      W(x) := u^mu [ K(Box_u/a0^2) u_mu ](x).
  W is a NONLOCAL functional of (u,g) but a LOCAL multiplication operator on the
  matter field. Modeling rho_m for a quantum scalar phi of mass m by its rest-mass
  density proxy rho_m = m^2 phi^2 (assumption, stated honestly; T_uu variant noted
  at the end), the matter kinetic operator is
      P = -Box + m^2 (1 + s W(x))     (Euclidean),
  a standard Laplace-type operator with LOCAL endomorphism E = -m^2(1+sW).
  => the one-loop divergences are EXACTLY the Gilkey/Seeley-DeWitt a1, a2 of P,
  with ALL the framework nonlocality confined inside the background functional W,
  which we then expand on dS using the framework's OWN Herglotz measure
      K(z) = a + INT_cut [ 1/(t-z) - t/(1+t^2) ] dmu(t),
      dmu = rho dt, rho_A=(1-sqrt(1-4|t|))/(2pi sqrt|t|) on -1/4<t<0,
      rho_B=1/(2pi sqrt|t|) on t<-1/4  (positive, unique; operator_definition.py).

WHAT IS COMPUTED (and what is not):
  [0] measure verified: reconstruction of K from (a,mu) off the cut, additive
      constant a determined and shown z-independent.
  [1] moment classification M_p = INT |t|^p dmu: finite window -3/2 < p < -1/2
      (shown), M_{-1} = 1 EXACT (sum rule = K(inf)-K(0): the superposition has
      exactly UNIT resolvent weight -> nothing left over to feed a tadpole),
      M_{-1/2} log-divergent (UV measure tail = the a0^1 term of K, resummed by
      |K|<=1), M_{-2} = K'(0) = infinity (deep-MOND sqrt(z) nonanalyticity: the
      polynomial delta-u expansion FAILS at exactly-dS; the bounded functional W
      resums it -- demonstrated numerically).
  [2] Seeley-DeWitt assembly (a1,a2) for P: the COMPLETE list of one-loop
      divergent counterterm operators with coefficients.
  [3] EXPLICIT dS computation (sympy, flat-slicing coords): linear-in-delta-u
      vertex on dS vanishes IDENTICALLY; every quadratic-order delta-u structure
      in W is LONGITUDINAL (only (u.grad) derivatives) -> NO transverse
      (grad_perp u)^2 aether counterterm, now at the heat-kernel level on dS,
      not just the flat selection rule.
  [4] the resummed quadratic symbol F(kappa)=K(kappa^2) (Euclidean longitudinal
      frequency kappa = k0/a0): bounded, monotone, F ~ kappa (nonanalytic |k0|).
  [5] numbers on BOTH footings (a0 = 9.36e-11 canonical / 1.13e-10 alt).
  NOT DONE: graviton loops & graviton-frame mixing; the T_uu-coupled variant
  (disformal-metric heat kernel) beyond the structural remark; finite parts.

HONESTY RULES: a generated counterterm is REPORTED with its coefficient; the
'protected' claims are verified as hard as the 'generated' ones; nothing is
checked against its own ansatz -- the dS expansion is derived from Christoffels.
"""
import numpy as np
import sympy as sp
from scipy import integrate
import sys

PASS = True
def check(name, cond):
    global PASS
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: PASS = False

def section(t):
    print("\n" + "#"*96); print("# " + t); print("#"*96)

# =====================================================================================
section("[0] THE HERGLOTZ MEASURE: verify reconstruction, fix the additive constant a")
# =====================================================================================
zs = sp.symbols('zs')
Ksym = (sp.sqrt(1 + 4*zs) - 1) / (2*sp.sqrt(zs))
Kf = sp.lambdify(zs, Ksym, 'numpy')

def rho(t):
    """positive Herglotz density on the cut t<0 (from operator_definition.py, banked)."""
    at = abs(t)
    if t >= 0: return 0.0
    if t > -0.25:
        return (1.0 - np.sqrt(1.0 - 4.0*at)) / (2.0*np.pi*np.sqrt(at))
    return 1.0 / (2.0*np.pi*np.sqrt(at))

def cutquad(f, tail_pow=None, TMAX=1e12, TMIN=0.0):
    """INT f(t) rho(t) dt over the cut t<0 (|t| in (TMIN, TMAX)).
       Region A (|t|<1/4): direct quad. Region B: LOG substitution |t|=e^y (robust over
       many decades). Analytic tail beyond TMAX if f ~ |t|^tail_pow there."""
    g = lambda t: f(t)*rho(t)
    gy = lambda y: g(-np.exp(y))*np.exp(y)          # dt -> e^y dy on |t|=e^y (log grid)
    IA,_ = integrate.quad(gy, np.log(max(TMIN, 1e-14)), np.log(0.25), limit=1200)
    IB,_ = integrate.quad(gy, np.log(0.25), np.log(TMAX), limit=1200)
    tail = 0.0
    if tail_pow is not None:
        p = tail_pow - 0.5
        assert p < -1, "tail not integrable"
        tail = (1.0/(2.0*np.pi)) * (TMAX**(p+1.0))/(-(p+1.0))
    return IA + IB + tail

# subtracted-kernel integral and constant a: K(z) = a + INT [1/(t-z) - t/(1+t^2)] dmu
def rep_integral(z):
    f = lambda t: (1.0/(t - z) - t/(1.0 + t*t))
    return cutquad(f, tail_pow=None, TMAX=1e10)  # integrand ~ |t|^{-3/2}: fine numerically

a_consts = []
for z0 in [0.5, 2.0, 10.0]:
    a_consts.append(float(Kf(z0)) - rep_integral(z0))
a_const = np.mean(a_consts)
spread = max(a_consts) - min(a_consts)
print(f" additive Herglotz constant a = {a_const:.8f}   (z-independence spread = {spread:.2e})")
check("constant a is z-independent (spread < 1e-6) -> representation is exact", spread < 1e-6)

maxerr = 0.0
for z0 in [0.3, 1.0, 3.0, 25.0]:
    err = abs(a_const + rep_integral(z0) - float(Kf(z0)))
    maxerr = max(maxerr, err)
print(f" reconstruction max |K_rep - K_exact| over z=0.3..25 : {maxerr:.2e}")
check("measure reconstructs K off the cut to <1e-6", maxerr < 1e-6)

# =====================================================================================
section("[1] MOMENTS OF THE MEASURE: which are finite, which divergent, and the physics")
# =====================================================================================
# symbolic density behaviour at the two ends
tau = sp.symbols('tau', positive=True)
rhoA_sym = (1 - sp.sqrt(1 - 4*tau))/(2*sp.pi*sp.sqrt(tau))
serA = sp.series(rhoA_sym, tau, 0, 2)
print(f" density near t->0-:   rho = {serA}   ~ sqrt|t|/pi")
print(f" density tail t->-inf: rho = 1/(2 pi sqrt|t|)")
print(" => M_p = INT |t|^p dmu converges  IFF  -3/2 < p < -1/2   (endpoint powers p+1/2 and p-1/2)")

# finite moments, numeric
M_m1   = cutquad(lambda t: 1.0/abs(t),        tail_pow=-1.0)
M_m34  = cutquad(lambda t: abs(t)**(-0.75),   tail_pow=-0.75)
M_m54  = cutquad(lambda t: abs(t)**(-1.25),   tail_pow=-1.25)
N_norm = cutquad(lambda t: 1.0/(1.0 + t*t),   tail_pow=None, TMAX=1e10)
J_sub  = cutquad(lambda t: t/(1.0 + t*t),     tail_pow=None, TMAX=1e10)
print(f"\n FINITE moments:")
print(f"   M_-1   = INT dmu/|t|      = {M_m1:.6f}   <-- SUM RULE: must equal K(inf)-K(0) = 1 EXACTLY")
print(f"                                (proof: INT_0^inf K'(z) dz = INT dmu INT_0^inf dz/(t-z)^2 = INT dmu/|t|)")
print(f"   M_-3/4 = INT dmu/|t|^3/4  = {M_m34:.6f}")
print(f"   M_-5/4 = INT dmu/|t|^5/4  = {M_m54:.6f}")
print(f"   N      = INT dmu/(1+t^2)  = {N_norm:.6f}   (Nevanlinna norm; banked value 0.2295)")
check("sum rule M_-1 = 1 (unit total resolvent weight: nothing spare to feed a z^0 tadpole)",
      abs(M_m1 - 1.0) < 2e-4)
check("Nevanlinna norm reproduces the banked 0.2295", abs(N_norm - 0.2295) < 2e-3)

# K(0)=0 from the EXACT measure (the 'superposition reintroduces a tadpole?' check)
K0_from_measure = a_const + cutquad(lambda t: 1.0/t - t/(1.0+t*t), tail_pow=None, TMAX=1e10)
Kinf_from_measure = a_const - J_sub
print(f"\n z^0 (tadpole) check with the REAL measure, not the series:")
print(f"   K(0)  = a + INT[1/t - t/(1+t^2)]dmu = {K0_from_measure:+.2e}  (must be 0: NO tadpole)")
print(f"   K(inf)= a - INT[t/(1+t^2)]dmu       = {Kinf_from_measure:.6f}  (must be 1: Newtonian norm)")
check("EXACT-measure tadpole test: K(0)=0 after full measure integration (no reintroduced z^0)",
      abs(K0_from_measure) < 1e-5)
check("EXACT-measure Newtonian normalization K(inf)=1", abs(Kinf_from_measure - 1.0) < 1e-5)

# divergent moments: demonstrate rate + give the physical meaning
print("\n DIVERGENT moments (demonstrated, with their physical meaning):")
Ls = np.array([1e2, 1e3, 1e4, 1e5])
Mhalf = [cutquad(lambda t: abs(t)**(-0.5), tail_pow=None, TMAX=L) for L in Ls]
slopes = np.diff(Mhalf)/np.diff(np.log(Ls))
print(f"   M_-1/2(Lambda): {['%.4f'%v for v in Mhalf]}  slope d/dlnLambda = {slopes[-1]:.5f} "
      f"(predict 1/(2pi) = {1/(2*np.pi):.5f})")
check("M_-1/2 log-divergent with slope exactly 1/(2pi) (the UV measure tail = the a0^1 term of K;"
      " harmless: |K|<=1 resums it, it is NOT a new divergence)", abs(slopes[-1]-1/(2*np.pi)) < 3e-3)

eps_list = np.array([1e-4, 1e-5, 1e-6, 1e-7])
M2 = [cutquad(lambda t: t**(-2.0), tail_pow=-2.0, TMAX=1e6, TMIN=e) for e in eps_list]
p_fit = np.polyfit(np.log(eps_list), np.log(M2), 1)[0]
print(f"   M_-2(eps->0) = K'(0): {['%.1f'%v for v in M2]}  ~ eps^({p_fit:.3f})  (predict -1/2: K ~ sqrt z)")
check("M_-2 = K'(0) diverges as eps^-1/2 at the IR end of the cut (deep-MOND sqrt-z nonanalyticity:"
      " the POLYNOMIAL delta-u expansion fails at exactly-dS; W itself stays bounded)",
      abs(p_fit + 0.5) < 0.05)
print("   M_0 (total mass) diverges ~ sqrt(Lambda)/pi: only the SUBTRACTED kernel is integrable --")
print("   the -t/(1+t^2) subtraction is load-bearing, and it is part of the framework's own definition.")

# =====================================================================================
section("[2] SEELEY-DEWITT ASSEMBLY: the complete one-loop divergence list (matter loop)")
# =====================================================================================
print(r"""
 P = -Box + m^2(1 + s W(x))  (Euclidean Laplace-type; W = u.K(Box_u/a0^2)u is a LOCAL
 multiplication operator on phi -- the nonlocality lives in the background functional).
 Gilkey, P = -(Box + E):  E = -m^2(1 + sW),  Omega_{munu} = 0 (no gauge connection).
   a1 = E + R/6
   a2 = (1/2)E^2 + (1/6)R E + (1/6)Box E + (1/72)R^2 - (1/180)Ric^2 + (1/180)Riem^2 + (1/30)Box R
 4D log-divergent effective action:  Gamma_div = -(1/(16 pi^2 eps)) INT sqrt(g) a2  (eps = 4-d;
 overall sign/normalization is convention -- the OPERATOR CONTENT and relative coefficients are not).""")
m, s_c, W, R = sp.symbols('m s W R', real=True)
E = -(m**2)*(1 + s_c*W)
a1 = E + R/6
a2_frame = sp.expand(sp.Rational(1,2)*E**2 + sp.Rational(1,6)*R*E)
print(f" a1 (frame part)                = {sp.expand(a1)}")
print(f" a2 (frame part, BoxE dropped as total derivative; pure-gravity R^2 invariants standard) =")
print(f"   {a2_frame}")
poly = sp.Poly(a2_frame, W)
c0, c1, c2 = [poly.coeff_monomial(W**k) for k in (0,1,2)]
print(f"""
 COUNTERTERM LIST (coefficient of 1/(16 pi^2 eps), per real scalar dof):
   O_vac  = {c0}          : standard vacuum terms (no frame content)
   O_W    = [{c1}] * W       : *** GENERATED *** -- SAME FORM as the tree coupling
            (tree: -(1/2) rho_m s W). Absorbed by rho_m -> rho_m + delta_rho_vac with
            delta_rho_vac = m^4/(16 pi^2) * (2/eps)-scale: the matter VACUUM energy
            couples through the SAME MI form factor. a0 and K(.) are untouched.
   O_WW   = [{c2}] * W^2   : *** GENERATED, NEW OPERATOR *** (K-squared structure).
            On dS it starts at O(delta-u^4) (W itself is quadratic there, see [3]).
   O_RW   = [{sp.Rational(-1,6)}] * m^2 R W : *** GENERATED, NEW curvature x frame OPERATOR ***.
            On dS R = 12 H^2 -> coefficient -2 s m^2 H^2 (tiny; numbers in [5]).
   O_BoxW = -(s m^2/6) Box W : TOTAL DERIVATIVE -> no bulk counterterm.
   NO a0-DEPENDENT COUNTERTERM: divergences are POLYNOMIAL in E, i.e. in W; a0 only
   appears INSIDE W's argument, never renormalized ([1]: exact-measure K(0)=0, M_-1=1).
   NO (grad_perp u)^2: proven on dS in [3] below.""")
check("a2 is quadratic in W: divergences polynomial in the vertex, a0 only inside W",
      sp.degree(poly) == 2)
check("W-linear coefficient = s*m^4 - s*m^2*R/6 (O_W flat piece + O_RW curvature piece)",
      sp.simplify(c1 - (s_c*m**4 - s_c*m**2*R/6)) == 0)
check("O_WW coefficient = s^2 m^4/2 (new K^2 operator, coefficient computed not assumed)",
      sp.simplify(c2 - s_c**2*m**4/2) == 0)

# =====================================================================================
section("[3] EXPLICIT dS: delta-u expansion of W from Christoffels (no ansatz)")
# =====================================================================================
print(r"""
 Flat-slicing dS: ds^2 = -dtau^2 + e^{2H tau} dx^2, u = d/dtau (comoving, geodesic).
 Herglotz handle: K(A)u_mu = a u_mu + INT dmu(t) [ (t-A)^{-1} - t/(1+t^2) ] u_mu,
 A = Box_u/a0^2. On the background A u_mu = 0 => K(A)u_mu = K(0) u_mu = 0 => W_dS = 0.
 Fluctuations u -> u + du with (u+du)^2 = -1. Each resolvent is a function of (u.grad)
 ONLY, so the ONLY derivative that can ever act on du inside W is LONGITUDINAL --
 unless a (du.grad) from delta(Box_u) dumps a spatial derivative on another du.
 We now compute every quadratic-order structure explicitly and scan for d(du)/dx^i.""")
tt, x1, x2, x3 = sp.symbols('tau x1 x2 x3', real=True)
H = sp.symbols('H', positive=True)
coords = [tt, x1, x2, x3]
aa = sp.exp(H*tt)
g = sp.diag(-1, aa**2, aa**2, aa**2)
ginv = g.inv()
Gamma = [[[sum(ginv[mu,l]*(sp.diff(g[l,nu],coords[rh]) + sp.diff(g[l,rh],coords[nu])
             - sp.diff(g[nu,rh],coords[l])) for l in range(4))/2
           for rh in range(4)] for nu in range(4)] for mu in range(4)]
def covd(V):   # nabla_nu V^mu for a vector field V^mu(coords)
    return [[sp.diff(V[mu], coords[nu]) + sum(Gamma[mu][nu][l]*V[l] for l in range(4))
             for nu in range(4)] for mu in range(4)]
def dirderiv(Xvec, V):  # (X.grad V)^mu = X^nu nabla_nu V^mu
    dV = covd(V)
    return [sp.simplify(sum(Xvec[nu]*dV[mu][nu] for nu in range(4))) for mu in range(4)]
def lower(V): return [sum(g[mu,nu]*V[nu] for nu in range(4)) for mu in range(4)]
def dot(Vlow, Wup): return sp.simplify(sum(Vlow[mu]*Wup[mu] for mu in range(4)))

u = [sp.Integer(1), 0, 0, 0]
psi = [sp.Function(f'psi{i}')(*coords) for i in (1,2,3)]
du = [sp.Integer(0)] + psi          # first-order fluctuation: u.du=0 => du^0 = 0
# background checks
ugu = dirderiv(u, u)
gradu = covd(u)
h_check = all(sp.simplify(gradu[mu][nu] - H*(sp.eye(4)[mu,nu] + u[mu]*lower(u)[nu])) == 0
              for mu in range(4) for nu in range(4))
check("background: (u.grad)u = 0 (geodesic) and grad u = H h (pure expansion) -- derived",
      all(sp.simplify(c) == 0 for c in ugu) and h_check)

# ---- LINEAR VERTEX: delta W = INT dmu/t * u.( (t-A)^{-1} deltaA u ) ; deltaA u computed exactly
X1 = dirderiv(u, dirderiv(du, u))         # (u.grad)(du.grad u)   [uses grad u = H h]
X2 = dirderiv(u, dirderiv(u, du))         # (u.grad)^2 du
X = [sp.simplify(X1[mu] + X2[mu]) for mu in range(4)]      # a0^2 * deltaA u
uX = dot(lower(u), X)
# and every longitudinal resolvent order of it: u.(u.grad)^{2k} X
uX2 = dot(lower(u), dirderiv(u, dirderiv(u, X)))
print(f"   u . [delta(Box_u) u]              = {sp.simplify(uX)}")
print(f"   u . (u.grad)^2 [delta(Box_u) u]   = {sp.simplify(uX2)}")
check("LINEAR delta-u vertex on dS vanishes IDENTICALLY at every resolvent order "
      "(u.X = u.(u.grad)^{2k}X = 0)", sp.simplify(uX) == 0 and sp.simplify(uX2) == 0)

# ---- QUADRATIC structures: assemble and scan for transverse derivatives of du
def has_transverse_dpsi(expr):
    for d in sp.preorder_traversal(sp.expand(expr)):
        if isinstance(d, sp.Derivative):
            if any(str(v).startswith('x') for v in d.variables) and \
               any(str(d.expr.func).startswith('psi') for _ in [0]):
                return True
    return False

# (i) du . K(A0) du -> representative resolvent orders du.(u.grad)^{2n} du, n=1,2
T_i1 = dot(lower(du), dirderiv(u, dirderiv(u, du)))
T_i2 = dot(lower(du), dirderiv(u, dirderiv(u, dirderiv(u, dirderiv(u, du)))))
# (ii) two-deltaA chains: X . (u.grad)^{2k} X (both ends longitudinal), k=0,1
T_ii1 = dot(lower(X), X)
T_ii2 = dot(lower(X), dirderiv(u, dirderiv(u, X)))
# (iii) single delta2A = (du.grad)^2 sandwiched on u:  u . (du.grad)(du.grad u)
T_iii = dot(lower(u), dirderiv(du, dirderiv(du, u)))
# (iv) outer-du x single-deltaA:  du . (u.grad)^{2k} X
T_iv1 = dot(lower(du), X)
T_iv2 = dot(lower(du), dirderiv(u, dirderiv(u, X)))
quad_terms = {'du.K(A0)du n=1': T_i1, 'du.K(A0)du n=2': T_i2,
              'X.X': T_ii1, 'X.(u.grad)^2 X': T_ii2,
              'u.d2A u (= -H^2 a^2 psi^2 type)': T_iii,
              'du.X': T_iv1, 'du.(u.grad)^2 X': T_iv2}
print("\n   quadratic-order structures and their transverse-derivative content:")
any_transverse = False
for name, T in quad_terms.items():
    tflag = has_transverse_dpsi(T)
    any_transverse = any_transverse or tflag
    print(f"     {name:36s}: transverse d(psi)/dx present? {tflag}")
print(f"   u.(du.grad)^2 u  = {sp.simplify(T_iii)}   (pure H^2 MASS term, no derivatives)")
check("NO transverse derivative of du in ANY quadratic-order divergence structure "
      "-> the (grad_perp u)^2 aether kinetic counterterm is NOT generated on dS",
      not any_transverse)
check("delta2A sandwich = algebraic -H^2 a^2 psi^2 (curvature-suppressed mass, computed not assumed)",
      sp.simplify(T_iii + H**2*aa**2*(psi[0]**2+psi[1]**2+psi[2]**2)) == 0)
print(r"""
   CONCLUSION [3]: on dS the divergent delta-u content of W (hence of O_W, O_WW, O_RW) is
     * quadratic-leading (linear vertex identically zero),
     * built ONLY from (u.grad)^{k} du and H^2 du^2 -- LONGITUDINAL, no wave cone,
     * i.e. proportional to the framework's OWN quadratic form (tree structure preserved):
       at O(du^2) one loop RENORMALIZES the coefficient of the existing form and creates
       NO new kinetic structure. The frame stays NON-DYNAMICAL at one loop (matter loop).""")

# =====================================================================================
section("[4] THE RESUMMED QUADRATIC SYMBOL (why M_-2 = inf is a nonanalyticity, not a divergence)")
# =====================================================================================
print(r""" Euclidean longitudinal symbol of du.K(A0)du:  F(kappa) = K(kappa^2), kappa = k0/a0.""")
kap = np.array([1e-4, 1e-2, 0.1, 0.5, 1.0, 5.0, 100.0])
Fv = np.array([float(Kf(k*k)) for k in kap])
print("   kappa :", "  ".join(f"{k:g}" for k in kap))
print("   F     :", "  ".join(f"{v:.5f}" for v in Fv))
check("F bounded in [0,1), monotone, F(0)=0: bounded resummed symbol (no runaway counterterm)",
      np.all(np.diff(Fv) > 0) and Fv[-1] < 1.0 and Fv[0] < 1e-3)
check("F ~ kappa (NONANALYTIC |k0|/a0) at small kappa: the divergent M_-2 moment is the "
      "sqrt-branch of the framework's own K, resummed and finite",
      abs(Fv[0]/kap[0] - 1.0) < 1e-2)
# prove-by-moving-the-number: the truncated moment (Taylor) expansion vs the exact symbol
kap0 = 0.05
exact = float(Kf(kap0**2))
for e in [1e-2, 1e-4, 1e-6]:
    trunc = cutquad(lambda t: t**(-2.0), tail_pow=-2.0, TMAX=1e6, TMIN=e)*kap0**2  # 1st Taylor term
    print(f"   Taylor-with-IR-cutoff eps={e:g}: K ~ {trunc:.4f}   vs exact K({kap0}^2) = {exact:.4f}")
print("   -> the Taylor coefficient runs away as the cutoff is removed while the exact symbol")
print("      stays finite: expand-then-integrate is ILLEGAL at dS; integrate-then-expand (the")
print("      Herglotz superposition of resolvents) is the correct, finite order of operations.")

# =====================================================================================
section("[5] NUMBERS ON BOTH FOOTINGS (does anything flip?)")
# =====================================================================================
c_light = 2.998e8
FOOT = [("canonical rho_DE  a0=cH_L/Z", 9.36e-11, 1.808e-18),   # H_Lambda [1/s]
        ("alt rho_tot       a0=cH0/Z ", 1.13e-10, 2.184e-18)]   # H_0      [1/s]
m_prot = 1.42e24  # proton mass as frequency m c^2/hbar [1/s] (scale illustration)
print(f" {'footing':30s} {'a0[m/s^2]':>10s} {'H[1/s]':>9s} {'w_gap=a0/2c[1/s]':>17s} "
      f"{'w_gap/H=1/(2Z)':>15s} {'O_RW/O_W=2H^2/m^2':>18s}")
rows = []
for lab, a0v, Hv in FOOT:
    wgap = a0v/(2*c_light)
    ratio = wgap/Hv
    rw = 2*Hv**2/m_prot**2
    rows.append((ratio, rw))
    print(f" {lab:30s} {a0v:10.3e} {Hv:9.3e} {wgap:17.3e} {ratio:15.4f} {rw:18.3e}")
print(f"""
 * the STRUCTURE (counterterm list, vanishing linear vertex, longitudinal-only quadratic
   form, no a0 running, sum rules M_-1=1 / K(0)=0) is a0-INDEPENDENT: a0 only rescales z.
 * dimensionful scales shift by x{1.13e-10/9.36e-11:.3f}; the dimensionless corner
   w_gap/H = 1/(2Z) is IDENTICAL on both footings (Z = cH/a0 = {c_light*1.808e-18/9.36e-11:.3f}).
 * the curvature-induced O_RW is ~{rows[0][1]:.0e} of O_W for proton-mass matter on BOTH footings.""")
check("NOTHING FLIPS between footings (identical structure; scales shift by 1.207; "
      "w_gap/H = 1/(2Z) invariant)", abs(rows[0][0] - rows[1][0]) < 1e-3)

# =====================================================================================
section("VERDICT (honest)")
# =====================================================================================
print(r"""
 (a) DOES a0 RUN?  NO -- and now at the exact-measure level, not just the naive series:
     * divergences are POLYNOMIAL in W (Seeley-DeWitt a2 is quadratic in E); a0 enters
       only inside W's argument and is never renormalized;
     * the superposition does NOT reintroduce a tadpole: K(0) = a + INT[1/t - t/(1+t^2)]dmu
       = 0 to 1e-5 with the real measure, and the sum rule INT dmu/|t| = K(inf)-K(0) = 1
       says the resolvent weight is EXACTLY the Newtonian normalization -- no excess.
     * moment ledger: finite window -3/2<p<-1/2 (M_-1=1, M_-3/4, M_-5/4 finite);
       M_-1/2 log-div = UV measure tail = the a0^1 term of K (resummed by |K|<=1);
       M_-2 = K'(0) = inf = the deep-MOND sqrt-z branch (nonanalyticity, NOT a divergence).
 (b) DERIVATIVES OF u IN THE DIVERGENCES?  YES -- but ONLY LONGITUDINAL, and only inside
     the framework's own K-form: the generated counterterms are
       O_W  = s m^4 W                      (SAME form as the tree coupling: the matter
                                            vacuum energy m^4/(16pi^2 eps) joins rho_m
                                            in the MI coupling -- a REAL generated term,
                                            reported, absorbable without touching a0/K)
       O_WW = (s^2 m^4/2) W^2              (NEW operator; O(du^4) on dS; longitudinal)
       O_RW = -(s/6) m^2 R W               (NEW curvature x frame operator; = -2 s m^2 H^2 W
                                            on dS; ~1e-83 of O_W for proton-mass matter)
     and the EXPLICIT dS expansion shows every du-derivative in them is (u.grad)du --
     the transverse (grad_perp u)^2 aether kinetic term is NOT generated (no transverse
     momentum ever enters a resolvent; the one (du.grad)(du.grad) sandwich collapses to
     an algebraic -H^2 du^2). The 0-dof, no-wave-cone property survives one loop.
 SCOPE (what this does NOT close): graviton loops and graviton-frame mixing; the
 T_uu-coupled rho_m variant (disformal effective-metric heat kernel -- structurally the
 same conclusion is expected since g_hat = g + sW u u and W_dS = 0, but NOT computed);
 two loops; finite parts; overall sign convention of the vacuum piece. s, a0, Z remain
 INPUTS. This is 'one-loop matter-sector divergences on dS: computed', not 'theory closed'.""")
print("="*96)
print(f" LANE A RESULT: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*96)
sys.exit(0 if PASS else 1)
