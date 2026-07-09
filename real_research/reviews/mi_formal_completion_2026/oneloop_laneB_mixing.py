#!/usr/bin/env python3
r"""
LANE B -- GRAVITON-FRAME MIXING WITH CURVATURE ON dS (the named dangerous channel).

Framework premises (reason from THESE):
  * Modified inertia. S_int = -(s/2) INT sqrt(-g) rho_m u^mu K(Box_u/a0^2) u_mu,
    Box_u = (u.grad)^2 (covariant composition of D = u^a grad_a on the covector index),
    K Herglotz: K(Box_u) = INT dmu(t) [resolvent combination], INT dmu/(1+t^2)=0.2295 finite.
    Resolvent expansion => the u-sector quadratic form is the mu-weighted tower of
    B_n = u^mu (D^{2n} u)_mu  with weight a0^{-2n} x (moment of mu). So the momentum
    structure of EVERY B_n decides the momentum structure of the full nonlocal vertex.
  * u is constrained unit-timelike, NO kinetic term (0 frame dof banked via curved Dirac closure).
  * dS background, flat slicing: ds^2 = -dt^2 + a^2 dx^2, a = e^{Ht}; comoving ubar geodesic;
    grad_mu ubar_nu = H P_perp_{mu nu};  R_{mu a nu b} ubar^a ubar^b = -H^2 P_perp_{mu nu}.

BANKED FLAT-SPACE CRUX (v4):
  * bare transverse block: k0^2 (-|V_perp|^2)  -- pure TIME derivative, NO spatial gradient,
    characteristic double root k0=0, no wave cone (transverse_mode_analysis.py);
  * khronon sector symbol: S_n = (-1)^n ksp^2 k0^{2n} -- overall spatial-gradient factor (A6b).

LANE B QUESTION (compute, don't assert): on dS, do the curvature commutators
[grad,grad] ~ H^2 convert the longitudinal insertions into TRANSVERSE structure that
(i) generates a standalone kinetic-type term for delta_u_perp (k0^2 with an H^2-shifted norm),
(ii) breaks the 'no spatial gradient in the transverse block' property (=> wave cone!), or
(iii) only generates k-free MASS-type H^2 |delta_u_perp|^2 terms (harmless: soaked by the
     algebraic second-class constraint pair, no Cauchy data)?

We do the EXACT tensor component algebra on dS:
  PART 0: Riemann identity + commutator conversion rule (4D, exact).
  PART 1: bare delta_u parametrization (3D t,x,y suffices for one transverse + one
          longitudinal polarization): quadratic form of B_n, n=1,2; classify every term.
  PART 2: khronon parametrization (2D t,x): dS-corrected symbol S_n^{dS}, n=1,2,3;
          check the overall ksp^2 factor, hunt for ksp^3/ksp^4 cone-forming terms.
  PART 3: selection rules for the loop (eps^1 vertex vanishing => matter-loop channels
          multiplicative), Seeley-DeWitt coefficients, numbers on BOTH footings.

HONESTY: if a cone-forming or norm-promoting term appears, we print it with its coefficient
and say UNFAVORABLE. No hand-written ansatz is 'verified against itself': the perturbations
are generic functions of t times plane waves in x; unit-norm is solved exactly to O(eps^2).
"""
import sympy as sp
import numpy as np

eps = sp.symbols('epsilon', real=True)
H, k = sp.symbols('H k', real=True, positive=True)
om = sp.symbols('omega', real=True)
X = sp.symbols('X', positive=True)   # X = exp(I k x) after substitution

def trunc2(e):
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps*e.coeff(eps, 1) + eps**2*e.coeff(eps, 2)

def christoffel(g, coords):
    n = len(coords); ginv = g.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for mu in range(n):
            for nu in range(n):
                Gam[l][mu][nu] = sp.simplify(sum(ginv[l, s]*(sp.diff(g[s, mu], coords[nu])
                                 + sp.diff(g[s, nu], coords[mu]) - sp.diff(g[mu, nu], coords[s]))
                                 for s in range(n))/2)
    return Gam

def Dop(w_low, u_up, Gam, coords):
    """(D w)_mu = u^a (partial_a w_mu - Gamma^l_{a mu} w_l), truncated at O(eps^2)."""
    n = len(coords); out = []
    for mu in range(n):
        e = 0
        for al in range(n):
            e += u_up[al]*(sp.diff(w_low[mu], coords[al])
                           - sum(Gam[l][al][mu]*w_low[l] for l in range(n)))
        out.append(trunc2(e))
    return sp.Matrix(out)

def x_average(e, xvar):
    """drop oscillating exp(I m k x) pieces: substitute exp(I k x)->X, keep X^0 terms."""
    e = sp.expand(e).subs(xvar, sp.log(X)/(sp.I*k))
    e = sp.expand(sp.powsimp(e))
    return sum(t for t in e.as_ordered_terms() if not t.has(X))

def blocks(e, w1, w1c, w2, w2c):
    """split quadratic form into (w2,w2c)=transverse block, (w1,w1c)=longitudinal, cross."""
    T = 0; L = 0; C = 0
    for t in sp.expand(e).as_ordered_terms():
        hasT = t.has(w2) or t.has(w2c); hasL = t.has(w1) or t.has(w1c)
        if hasT and not hasL: T += t
        elif hasL and not hasT: L += t
        else: C += t
    return sp.simplify(T), sp.simplify(L), sp.simplify(C)

print("="*100)
print(" PART 0 -- 4D dS: curvature DOES produce the transverse projector (exact), and the")
print("           commutator conversion rule is ALGEBRAIC (k0^2 -> H^2, never -> ksp^2)")
print("="*100)
t4, x4, y4, z4 = sp.symbols('t x y z', real=True)
c4 = [t4, x4, y4, z4]
a4 = sp.exp(H*t4)
g4 = sp.diag(-1, a4**2, a4**2, a4**2)
Gam4 = christoffel(g4, c4)
# Riemann R^l_{m a b} = d_a Gam^l_{b m} - d_b Gam^l_{a m} + Gam^l_{a s}Gam^s_{b m} - Gam^l_{b s}Gam^s_{a m}
Riem = [[[[sp.simplify(sp.diff(Gam4[l][b][m], c4[a]) - sp.diff(Gam4[l][a][m], c4[b])
        + sum(Gam4[l][a][s]*Gam4[s][b][m] - Gam4[l][b][s]*Gam4[s][a][m] for s in range(4)))
        for b in range(4)] for a in range(4)] for m in range(4)] for l in range(4)]
ub4 = sp.Matrix([1, 0, 0, 0])            # ubar^mu
# R_{mu a nu b} ubar^a ubar^b  (lower all: R_{l m a b} = g_{l s} R^s_{m a b}; want R_{mu a nu b} u^a u^b)
Ruu = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Ruu[mu, nu] = sp.simplify(sum(g4[mu, s]*Riem[s][al][nu][be]*ub4[al]*ub4[be]
                                      for s in range(4) for al in range(4) for be in range(4)))
Pperp = sp.simplify(g4 + (g4*ub4)*(g4*ub4).T)   # P_perp_{mu nu} = g + u_mu u_nu (lower)
chk0 = sp.simplify(Ruu + H**2*Pperp)
print("  R_{mu a nu b} ubar^a ubar^b + H^2 P_perp_{mu nu} =", list(chk0), " (must be all 0)")
assert chk0 == sp.zeros(4, 4)
print("  ==> EXACT: R_{mu a nu b} u^a u^b = -H^2 P_perp_{mu nu}. Curvature produces TRANSVERSE")
print("      projector structure times H^2 -- the named channel is real. What matters is the")
print("      OPERATOR it multiplies. Commutator rule (exact identity, no CAS needed):")
print("      ubar^a V^b [grad_a, grad_b] w_mu = -R^l_{mu a b} ubar^a V^b w_l")
print("        = H^2 ( ubar_mu (V.w) - V_mu (ubar.w) )   [dS Riemann substituted]")
print("      -- PURELY ALGEBRAIC in w: each commutator REMOVES two derivatives (one D = one k0")
print("      factor per slot) and inserts H^2 x (projector algebra). It never inserts a spatial")
print("      gradient. So curvature converts k0^2 -> H^2 in the symbol; it cannot manufacture")
print("      ksp^2. This is the structural reason behind the CAS results below; the CAS is the proof.")

print()
print("="*100)
print(" PART 1 -- BARE delta_u on dS (3D: t,x,y): exact quadratic form of B_n = u.(D^{2n}u), n=1,2")
print("="*100)
t3, x3, y3 = sp.symbols('t x y', real=True)
c3 = [t3, x3, y3]
a3 = sp.exp(H*t3)
g3 = sp.diag(-1, a3**2, a3**2)
g3inv = g3.inv()
Gam3 = christoffel(g3, c3)
E = sp.exp(sp.I*k*x3)
wx = sp.Function('w_x')(t3); wxc = sp.Function('wbar_x')(t3)   # longitudinal (along k)
wy = sp.Function('w_y')(t3); wyc = sp.Function('wbar_y')(t3)   # TRANSVERSE polarization
dux = eps*(wx*E + wxc/E)
duy = eps*(wy*E + wyc/E)
# unit norm solved EXACTLY then expanded: -u0^2 + a^-2(dux^2+duy^2) = -1, ubar_0 = -1 branch
u0 = -sp.sqrt(1 + (dux**2 + duy**2)/a3**2)
u0 = sp.series(u0, eps, 0, 3).removeO()
u_low = sp.Matrix([trunc2(u0), dux, duy])
u_up = sp.Matrix([trunc2(sp.expand(sum(g3inv[m, n]*u_low[n] for n in range(3)))) for m in range(3)])

for n in (1, 2):
    v = u_low
    for _ in range(2*n):
        v = Dop(v, u_up, Gam3, c3)
    Bn = trunc2(sp.expand(sum(u_up[m]*v[m] for m in range(3))))
    e0 = sp.simplify(Bn.coeff(eps, 0))
    e1 = sp.simplify(Bn.coeff(eps, 1))
    print(f"\n  ---- n={n} ----")
    print("  background  B_n[ubar]      =", e0, "  (geodesic comoving frame => 0: NO TADPOLE on dS)")
    print("  linear      B_n^(1)        =", e1, "  (must be 0: vertex has NO linear delta_u piece on dS)")
    assert e0 == 0 and e1 == 0
    e2 = x_average(Bn.coeff(eps, 2), x3)
    T, L, C = blocks(e2, wx, wxc, wy, wyc)
    print("  TRANSVERSE block (w_y wbar_y):")
    print("     ", sp.simplify(T))
    print("     contains spatial momentum k?  ->", T.has(k))
    # symbol: w -> e^{i om t} formal (a(t) factors kept explicitly)
    subsym = {wy: sp.exp(sp.I*om*t3), wyc: sp.exp(-sp.I*om*t3)}
    sigT = sp.simplify(sp.expand(T.subs({wy.diff(t3, j): sp.diff(subsym[wy], t3, j) for j in range(2*n, -1, -1)}
                                        | {wyc.diff(t3, j): sp.diff(subsym[wyc], t3, j) for j in range(2*n, -1, -1)})))
    sigT = sp.simplify(sigT)
    print("     transverse symbol sigma_T(omega; H) =", sigT)
    roots = sp.solve(sp.Eq(sp.expand(sigT*a3**2), 0), om)
    print("     characteristic roots omega =", roots, " (k-INDEPENDENT -> zero group velocity, no cone)"
          if not any(sp.simplify(r).has(k) for r in roots) else "  *** k-DEPENDENT ROOT: CONE! ***")
    assert not sigT.has(k)
    print("  LONGITUDINAL block:", sp.simplify(L))
    print("  CROSS block (T-L mixing):", sp.simplify(C), " (k-dependence here is harmless: it feeds the")
    print("      longitudinal/khronon sector, which carries its own ksp^2 factor -- see PART 2)")

print(r"""
  READING OF n=1 (exact): B_1^(2) = -|D delta_u|^2 + total-D-derivative. In LOWER comoving
  components the H's cancel EXACTLY in delta(Du)_i = d_t(delta u_i) - H delta u_i + H delta u_i
  [the connection term -H du_i against grad ubar = +H P_perp du_i]: the kinetic norm of the
  transverse block is H-UNDRESSED. In the ORTHONORMAL frame (vhat = delta u_i / a) the same
  block reads -(vhat' + H vhat)^2 = -(vhat')^2 - 2H vhat vhat' - H^2 vhat^2: the ONLY H^2 term
  is the k-free MASS-type partner inside a perfect square (plus a total derivative; note the
  framework's own dust measure sqrt(-g) rho_m = a^3 rho_m = const makes t-integration by parts
  exact). NO standalone H^2 k0^2 kinetic-norm shift at n=1; NO ksp^2 anywhere in the block.
  For n=2 the H^2 k0^2 dressings of the SUBLEADING tower appear (coefficients printed above),
  but they live in the SAME k0-only tower: roots stay k-independent, |omega| = O(H).""")

print("="*100)
print(" PART 2 -- KHRONON parametrization on dS (2D: t,x): dS-corrected crux symbol S_n^{dS}")
print("="*100)
t2, x2 = sp.symbols('t x', real=True)
c2 = [t2, x2]
a2v = sp.exp(H*t2)
g2 = sp.diag(-1, a2v**2)
g2inv = g2.inv()
Gam2 = christoffel(g2, c2)
E2 = sp.exp(sp.I*k*x2)
P = sp.Function('P')(t2); Pc = sp.Function('Pbar')(t2)
T_kh = t2 + eps*(P*E2 + Pc/E2)
dT = sp.Matrix([sp.diff(T_kh, cc) for cc in c2])
norm2 = sum(g2inv[i, i]*dT[i]**2 for i in range(2))
N = sp.sqrt(-norm2)
u_low2 = sp.Matrix([trunc2(sp.series(-dT[i]/N, eps, 0, 3).removeO()) for i in range(2)])
u_up2 = sp.Matrix([trunc2(sp.expand(sum(g2inv[m, n]*u_low2[n] for n in range(2)))) for m in range(2)])

for n in (1, 2, 3):
    v = u_low2
    for _ in range(2*n):
        v = Dop(v, u_up2, Gam2, c2)
    Bn = trunc2(sp.expand(sum(u_up2[m]*v[m] for m in range(2))))
    e1 = sp.simplify(Bn.coeff(eps, 1))
    assert e1 == 0
    e2 = x_average(Bn.coeff(eps, 2), x2)
    # symbol: P -> e^{i om t}
    sub = {}
    for j in range(2*n + 2, -1, -1):
        sub[P.diff(t2, j)] = sp.diff(sp.exp(sp.I*om*t2), t2, j)
        sub[Pc.diff(t2, j)] = sp.diff(sp.exp(-sp.I*om*t2), t2, j)
    sig = sp.simplify(sp.expand(e2.subs(sub)))
    sig = sp.simplify(sp.expand(sig))
    poly = sp.Poly(sp.expand(sig*a2v**4), k)   # clear a-powers for bookkeeping; exact rescale
    kpows = sorted(poly.as_dict().keys())
    print(f"\n  ---- n={n} ----   S_n^dS(omega, k; H, a) = {sig}")
    print("     value at k=0:", sp.simplify(sig.subs(k, 0)), "  (khronon = time reparam at k=0 -> must be 0)")
    assert sp.simplify(sig.subs(k, 0)) == 0
    cf = {p[0]: sp.simplify(poly.as_dict()[p]) for p in poly.as_dict()}
    print("     k-powers present:", [p[0] for p in kpows])
    for p in sorted(cf):
        print(f"       coeff of k^{p}: ", cf[p])
    danger = [p for p in cf if p >= 3 and sp.simplify(cf[p]) != 0]
    if danger:
        print("     *** k^3/k^4-type terms PRESENT -- checking whether they form a cone ...")
    else:
        print("     NO k^3/k^4 terms: symbol = ksp^2 x (polynomial in omega, H) EXACTLY.")
    # roots of the k^2-stripped polynomial in omega
    red = sp.simplify(sp.expand(sig*a2v**2/k**2)) if not danger else sig
    roots = sp.solve(sp.Eq(sp.expand(sp.simplify(sig)), 0), om)
    kdep = [r for r in roots if sp.simplify(r).has(k)]
    print("     characteristic roots omega:", roots)
    print("     k-dependent roots (cone test):", kdep if kdep else "NONE -> no wave cone on dS")
    print("     flat limit H->0 of symbol:", sp.simplify(sig.subs(H, 0)), "  [banked: (-1)^n k^2 om^{2n}]")

print(r"""
  STRUCTURAL THEOREM (why ksp^4 can NEVER appear at quadratic order, any n):  each spatial
  gradient d_x in a D-string needs a u^x coefficient; u^x is O(eps) (one khronon leg) -- so at
  O(eps^2) at most ONE d_x can act on the other leg. k-factors come only from (i) the two legs
  themselves (u_x ~ ik P: max k^2), (ii) that single d_x on the conjugate leg (max one more k).
  Max power = k^3, and the CAS above shows what actually survives. A cone needs k^4 vs k^2 (or a
  surviving k^3 root); the roots printed above are the verdict.""")

print("="*100)
print(" PART 3 -- LOOP BOOKKEEPING (selection rules -> which counterterms are generated) + NUMBERS")
print("="*100)
print(r"""
 One-loop 1PI diagrams that could produce a delta_u_perp^2 term (matter quanta + gravitons only;
 NO aether propagator exists -- 0 frame dof, banked curved Dirac closure):

  (i) matter loop, TWO vertices rho_m F[u]:  needs (delta F)^2. COMPUTED ABOVE: B_n^(1) = 0
      identically on dS for every n (PART 1/2 assertion e1==0; operator proof: Dubar=0 geodesic +
      ubar.(D^m delta_u) = D^m(ubar.delta_u) = 0 + K(0)=0 from the framework's own IR kernel).
      ==> this channel generates NOTHING quadratic in delta_u. PROTECTED BY THE FRAMEWORK'S OWN
      GEOMETRY (comoving frame geodesic) AND ITS OWN KERNEL (K ~ sqrt(z) -> K(0)=0).

  (ii) matter loop, ONE vertex (tadpole channel): <rho_m>_loop x F^(2)[delta_u]. GENERATED.
      Counterterm = delta_rho_div x [the SAME tree quadratic form computed in PARTS 1-2].
      Momentum structure IDENTICAL to tree (multiplicative). Divergent coefficient via the
      Herglotz reduction: each resolvent insertion (t - Box_u/a0^2)^{-1} is a local massive
      resolvent; INT dmu/(1+t^2) = 0.2295 < inf => the superposition of standard heat kernels
      converges. Log-divergent piece per matter mode of mass m on dS (Seeley-DeWitt a2, R=12H^2,
      R_ab R^ab = 36 H^4, R_abcd R^abcd = 24 H^4, minimal coupling):
          a2 = m^4/2 - 2 m^2 H^2 + (29/15) H^4
      => delta_rho_div ~ (1/16pi^2) [ m^4/2 - 2 m^2 H^2 + (29/15) H^4 ] ln(Lambda) + power terms.
      This renormalizes the rho_m NORMALIZATION of the vertex (absorbed in the matter density /
      G renormalization). a0 is NOT shifted: no z-dependent reweighting of K appears (the
      operator K(Box_u/a0^2) is untouched; consistent with the banked no-z^0-tadpole rule).

  (iii) graviton-frame mixing: tree-level h-delta_u mixing EXISTS (it is the framework's own
      MOND-sector force: rho_bar_m x dF/dh != 0 because the frame is not geodesic for g+h).
      Loops dress it multiplicatively (channel (i) logic applies to the delta_u side of every
      mixed vertex: the delta_u leg still enters through F, whose linear piece vanishes and whose
      quadratic piece is the PART-1 block). Integrating out the CONSTRAINED h_{0i} (shift) sector
      cannot create Cauchy data for the frame: constraint elimination preserves the Dirac count
      (banked det 4(u.u)^2 -> 4 block is ALGEBRAIC -- the H^2 dressings computed here enter
      coefficient functions, not the symplectic structure). Any rho_m-dependent pole generated in
      the effective delta_u action after eliminating h is the MATTER sector's collective
      (Jeans-type) mode, carried by matter dof -- not a frame dof.
""")
# ---- numbers, BOTH footings ----
c_SI = 2.99792458e8
H0 = 67.4*1000/3.0857e22          # s^-1  (Planck 2018)
OmL, Omm = 0.685, 0.315
HL = H0*np.sqrt(OmL)
for tag, a0v, Hv in (("canonical  a0 = cH_Lambda/Z (rho_DE footing)", 9.36e-11, HL),
                     ("alt        a0 = cH0/Z'     (rho_total footing)", 1.13e-10, H0)):
    r = (c_SI*Hv/a0v)**2
    print(f"  [{tag}]")
    print(f"     H = {Hv:.3e} s^-1,  H^2 = {Hv**2:.3e} s^-2,  a0 = {a0v:.3e} m/s^2")
    print(f"     dimensionless curvature-dressing ratio (cH/a0)^2 = Z^2 = {r:.2f}")
    print(f"     mass-type transverse term: sigma_T root |omega| = O(H) = {Hv:.2e} s^-1 "
          f"(~1/{1/(Hv*3.156e16):.1f} x 1/Gyr^-1 scale)")
    print(f"     graviton-vector-block induced norm / EH norm ~ 3 Om_m (cH0/a0)^2 x (k0/k)^2 = "
          f"{3*Omm*(c_SI*H0/a0v)**2:.1f} x (k0/k)^2   [k0-only term, no cone -> constrained sector]")
print(f"     loop factor 1/16pi^2 = {1/(16*np.pi**2):.3e};  Herglotz norm INT dmu/(1+t^2) = 0.2295 (finite)")
print(r"""
  BOTH FOOTINGS: the dressing ratio (cH/a0)^2 = Z^2 ~ 33.6 is FOOTING-INVARIANT by construction
  (a0 = cH/Z on each footing); H^2 itself shifts by (H0/H_Lambda)^2 = 1.46. Nothing structural
  flips: same selection rules, same block structure, same verdict on both footings.
""")
print("LANE B: script completed, all assertions passed.")
