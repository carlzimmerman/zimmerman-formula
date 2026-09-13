# G007 core v3: fix the sign conventions and validate the linearized algebra exactly.
import sympy as sp

t, x, y, z, s, M4 = sp.symbols('t x y z s M4', real=True)
Xv = sp.Symbol('X', positive=True)
eta = sp.diag(-1, 1, 1, 1)
phit = sp.Function('phi')(t, x, y, z)
dphi = [sp.diff(phit, c) for c in (t, x, y, z)]

# ============================================================================
# 1. Stress tensor derivation, done exactly with an explicit variation.
#    L = M^4 f(X), X = g^{mu nu} d_mu phi d_nu phi / s^2.  Vary g^{mu nu}.
#    Convention: T_{mu nu} = -2/sqrt(-g) delta S/delta g^{mu nu}.
#    S = Int sqrt(-g) L.  delta S = Int sqrt(-g) [ -1/2 g_{mu nu} L + dL/dg^{mu nu} ] delta g^{mu nu}
#    => T_{mu nu} = 2 dL/dg^{mu nu} - g_{mu nu} L.
#    dL/dg^{mu nu} = M^4 f'(X) d_mu phi d_nu phi / s^2.
#    => T_{mu nu} = 2 M^4 f'(X) d_mu phi d_nu phi/s^2 - g_{mu nu} M^4 f(X)
# ============================================================================
def T_mn(f, gco, ginv, dph):
    """T_{mu nu} = 2 M^4 f' d_phi d_phi / s^2 - g_{mu nu} M^4 f, X = g^{ab} d_a d_b/s^2."""
    Xval = sum(ginv[a, b]*dph[a]*dph[b] for a in range(4) for b in range(4))
    return sp.ImmutableMatrix(4, 4, lambda mu, nu:
        sp.simplify(2*M4*sp.diff(f, Xv).subs(Xv, Xval)*dph[mu]*dph[nu]/s**2
                    - gco[mu, nu]*M4*f.subs(Xv, Xval)))

# canonical check: f = -X/2 => L = -M^4 X/2. With M^4/s^2 = 1: L = -(1/2) g^{ab} d_a phi d_b phi.
f_can = -Xv/2
Tc = T_mn(f_can, eta, eta, dphi)
expected00 = sp.Rational(1, 2)*(dphi[0]**2 + dphi[1]**2 + dphi[2]**2 + dphi[3]**2)
got00 = sp.simplify(Tc[0, 0]*s**2/M4)
print("canonical T_00 (scaled):", sp.factor(got00))
print("expected               :", expected00)
print("match:", sp.simplify(got00 - expected00) == 0)
Txx = sp.simplify(Tc[1, 1]*s**2/M4)
exp_xx = dphi[1]**2 + sp.Rational(1, 2)*(dphi[0]**2 - dphi[1]**2 - dphi[2]**2 - dphi[3]**2)
print("canonical T_xx match:", sp.simplify(Txx - exp_xx) == 0)
print()

# ============================================================================
# 2. The OneFunction stress ratios and the phantom sign, exactly.
# ============================================================================
fG = Xv - 2*sp.log(1+sp.sqrt(Xv)) - 2/(1+sp.sqrt(Xv)) + 1
fGp, fGpp = sp.diff(fG, Xv), sp.diff(fG, Xv, 2)
# Static spherical: phi = phi(r).  X = (phi')^2/s^2.
#   T^t_t = -M^4 f(X)            (energy density rho = M^4 f(X)?? T^{tt}=rho => rho = T^{tt} = T_{tt}/|g_tt|^2 ~ -T_{tt} = M^4 f)
# Let's compute rho = T^{t}_{t} * (-1):  T^{mu}_{nu} = g^{mu a} T_{a nu}.
#   T^{t}_{t} = -M^4 f(X)  => rho_phi = -T^t_t = M^4 f(X).
# G002 f: f < 0 for X < 1.4978, f > 0 beyond.  Active energy rho_active = M^4(f(X) - f(0)) = M^4(f+1)
#   = (4/3)M^4 X^{3/2} + ... > 0 deep?! WAIT: f+1 = (4/3)X^{3/2}... > 0.  So the ACTIVE energy is
#   positive deep.  Re-examine: rho_phi(X) = M^4 f(X) crosses zero at X*=1.4978, but the
#   physically relevant statement is rho_phi = M^4 f(X) with f(0)=-1: vacuum -1, active +4/3 X^{3/2}.
#   That is a HEALTHY sign (vacuum energy -1, gradient energy +).
print("f(0) =", sp.simplify(fG.subs(Xv, 0)))
print("rho_active(X)/M^4 = f(X)+1 =", sp.simplify(fG + 1))
print("deep: f+1 -> (4/3) X^{3/2} > 0 : healthy gradient energy")
print()

# BUT the homogeneous (timelike) fluctuation: phi = phi0 + var(t), X = X0 - var_t^2/s^2 + ...
#   quadratic kinetic coeff = -M^4 f'(X0)/s^2.  f' = mu_2 > 0 => NEGATIVE = ghost.
#   The static energy is fine but the PROPAGATING timelike mode is a phantom.
# Verify by direct expansion (1-D, x-only, background phi0 = q x):
q = sp.Symbol('q', positive=True)
var = sp.Function('var')(t, x)
Xtot = (-(sp.diff(q*x + var, t))**2 + (sp.diff(q*x + var, x))**2)/s**2
Ltot = M4 * fG.subs(Xv, Xtot)
# quadratic part in var:
dvt, dvx = sp.diff(var, t), sp.diff(var, x)
Lq = sp.expand(Ltot)
# coefficient of var_t^2:
c_tt = sp.simplify(sp.diff(Ltot, dvt, 2).subs(var, 0)/2)
c_xx = sp.simplify(sp.diff(Ltot, dvx, 2).subs(var, 0)/2)
print("background phi0 = q x (X0 = q^2/s^2):")
print("  quadratic kinetic (var_t^2) coeff:", sp.simplify(c_tt))
print("  quadratic radial  (var_x^2) coeff:", sp.simplify(c_xx))
# substitute X0 = q^2/s^2:
subsX0 = {q**2: sp.Symbol('X0', positive=True)*s**2}
print("  kinetic -> -M^4 f'(X0)/s^2      :", sp.simplify(c_tt.subs(q**2, sp.Symbol('X0')*s**2)))
print("  radial  -> -M^4(f'+2X f'')/s^2  :", sp.simplify(c_xx.subs(q**2, sp.Symbol('X0')*s**2)))
print()
print("=> G002's f' = +mu_2 > 0: the timelike kinetic coefficient is NEGATIVE (phantom ghost)")
print("   The fused healthy sign f_h = -f - 2 has f_h' = -mu_2 < 0: healthy timelike kinetic,")
print("   but then rho_active = -M^4(f+1) < 0 deep (phantom static energy) -- cannot have both.")
print()

# ============================================================================
# 3. THE KEY STRUCTURAL FACT: the timelike ghost is a property of the SIGN OF f'.
#    For ANY f with f' > 0 on a spacelike-gradient background (the MOND regime),
#    the timelike fluctuation is a phantom.  This is exact and sign-independent
#    of the chassis: it kills G002's chassis as a standalone k-essence.
#    BUT: this is the SINGLE-METRIC G002 chassis, not the bimetric chassis.
#    In the bimetric chassis ghat is built from (g, phi) and the scalar couples
#    to g only through F(X) -- the same algebra applies.  Demonstrate on the
#    minimal bimetric chassis below.
# ============================================================================

# ============================================================================
# 4. The PPN computation for the bimetric chassis, in the Newtonian gauge.
#    S = (1/16 pi G) Int sqrt(-g)[R + F(X)] + S_m[g].
#    Field equations: G_{mu nu}(g) = 8 pi G/c^4 T^{matter}_{mu nu} + (1/2) g_{mu nu} F - F' d phi d phi/s^2
#    (the F-term's stress; overall factors absorbed into the definition of the source scale).
#    Static spherical, matter point source rho = M delta^3(r):
#      (i)  G^t_t:  -2 nabla^2 Psi = 8 pi G rho/c^2 + [F-stress trace pieces]
#      (ii) the slip from the i=j equation and the traceless part.
#    We did the general linearized Einstein tensor above. Now source it with:
#      T^t_t(matter) = -rho,  T^t_t(phi) = -M^4 f(X),  T^r_r(phi) = M^4(f - 2 X f')...
#    Compute T^r_r and T^t_t for the k-essence exactly.
# ============================================================================
# static, phi = phi(r): X = (phi')^2/s^2.
#   T_{tt} = -M^4 f g_{tt}... wait g_tt = -1 so T_{tt} = -(-1)M^4 f = +M^4 f?? recompute:
#   T_{mu nu} = 2 M^4 f' d_mu phi d_nu phi/s^2 - g_{mu nu} M^4 f.
#   T_{tt} = -g_{tt} M^4 f = +M^4 f (g_tt = -(1+2Phi) ~ -1).  T^t_t = g^{tt} T_{tt} = -M^4 f.
#   T_{rr} = 2 M^4 f' (phi')^2/s^2 - g_{rr} M^4 f = 2 M^4 f' X - M^4 f (to leading order).
#   T^r_r = g^{rr} T_{rr} = 2 M^4 f' X - M^4 f.
#   T^th_th = -M^4 f (angular).
# So the k-essence perfect-fluid + anisotropic decomposition:
#   rho_phi = M^4 f(X),  p_phi = -M^4 f(X),  pi^r_r(phi) = 2 M^4 f' X (radial extra)
#   i.e. T^r_r = -rho_phi + pi^r_r with pi^r_r = 2 M^4 f' X - wait T^r_r = 2M^4 f' X - M^4 f
#   and p = -rho = -M^4 f so T^r_r = p + pi^r_r => pi^r_r = 2 M^4 f' X.
print("k-essence static stress (exact, closed form):")
print("  rho_phi = M^4 f(X),  p_phi = -M^4 f(X),  pi^r_r = 2 M^4 f'(X) X,  pi^th_th = 0")
print()
# The slip equation: from G^r_r + G^t_t (the Phi+Psi combination):
#   G^r_r + G^t_t = 8 pi G (T^r_r + T^t_t) = 8 pi G (pi^r_r + matter pieces)
# Linearized: G^r_r + G^t_t = -2/r d/dr [ r (Psi - Phi) ]  (standard; verify symbolically)
rr = sp.Symbol('r', positive=True)
Ph = sp.Function('Phi')(rr)
Ps = sp.Function('Psi')(rr)
eps = sp.Symbol('epsilon')
g = sp.diag(-(1+2*eps*Ph), (1-2*eps*Ps), (1-2*eps*Ps)*rr**2, (1-2*eps*Ps)*rr**2)
ginv = sp.diag(-1/(1+2*eps*Ph), 1/(1-2*eps*Ps), 1/((1-2*eps*Ps)*rr**2), 1/((1-2*eps*Ps)*rr**2))
coords = (t, rr, sp.Symbol('theta'), sp.Symbol('phi4'))
Gam = [[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            ssum = 0
            for si in range(4):
                ssum += ginv[l, si]*(sp.diff(g[si, n], coords[m]) + sp.diff(g[si, m], coords[n])
                                    - sp.diff(g[m, n], coords[si]))
            Gam[l][m][n] = sp.simplify(sp.expand(ssum/2))
Ric = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        ssum = 0
        for l in range(4):
            ssum += sp.diff(Gam[l][mu][nu], coords[l]) - sp.diff(Gam[l][l][nu], coords[mu])
            for m in range(4):
                ssum += Gam[l][m][mu]*Gam[m][l][nu] - Gam[l][m][l]*Gam[m][mu][nu]
        Ric[mu, nu] = ssum
def mixed(mu, nu):
    return sp.simplify(sp.expand(sp.series(Ric[mu, nu] - sp.Rational(1,2)*g[mu, nu]*sum(ginv[a,b]*Ric[a,b] for a in range(4) for b in range(4)), eps, 0, 2).removeO()))
# G^mu_nu = g^{mu a} G_{a nu}
def Gmix(mu, nu):
    return sp.simplify(sp.expand(sp.series(sum(ginv[mu, a]*(Ric[a, nu] - sp.Rational(1,2)*g[a, nu]*sum(ginv[c,d]*Ric[c,d] for c in range(4) for d in range(4))) for a in range(4)), eps, 0, 2).removeO()))
Gtt = Gmix(0, 0)
Grr = Gmix(1, 1)
Gth = Gmix(2, 2)
nabla2 = lambda uu: sp.diff(uu, rr, 2) + 2/rr*sp.diff(uu, rr)
print("G^t_t (linear) =", sp.simplify(Gtt.coeff(eps, 1)))
print("G^r_r (linear) =", sp.simplify(Grr.coeff(eps, 1)))
print("G^th_th(linear) =", sp.simplify(Gth.coeff(eps, 1)))
print()
lhs_sum = sp.simplify((Gtt + Grr).coeff(eps, 1))
target = -2/rr*sp.diff(rr*(Ps - Ph), rr)
print("G^t_t + G^r_r =", lhs_sum)
print("target -2/r d[r(Psi-Phi)]/dr =", sp.simplify(target))
print("identity holds:", sp.simplify(lhs_sum - target) == 0)
print()
lhs_tt = sp.simplify(Gtt.coeff(eps, 1))
print("G^t_t == 2 nabla^2 Psi ?", sp.simplify(lhs_tt - 2*nabla2(Ps)) == 0)
print("G^t_t =", lhs_tt)
