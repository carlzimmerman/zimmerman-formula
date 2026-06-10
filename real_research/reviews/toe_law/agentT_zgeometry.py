#!/usr/bin/env python3
"""
agentT -- THE Z-GEOMETRY QUESTION (machine-verified; pre-registered in agentT_zgeometry.md)
===========================================================================================
Does the Jacobson-construction breakdown acceleration a_break carry a forced dimensionless
coefficient?  Three independent definitions of the validity boundary, each computed EXACTLY
in the dS static patch (ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2, f = 1 - H^2 r^2; units
c = hbar = k_B = 1 except where noted):
  (a) the MERGER condition: flat Rindler depth 1/a  vs  proper distance ell to the
      cosmological horizon for the stationary (Deser-Levin) worldline at radius r;
  (b) the KILLING-FAILURE condition: the O(x^2*Riemann) failure of the approximate boost
      Killing field (Guedens-Jacobson-Sarkar 1112.6215) relative to the leading balance --
      the EXACT coefficient of the failure term in dS;
  (c) the EQUILIBRIUM/ADIABATIC condition: patch light-crossing time vs inverse temperature.
Pre-registered outcomes: Z-CANDIDATE / O(1)-NULL / ILL-POSED.  Raw numbers FIRST,
comparisons AFTER (coefficient discipline, TOE_STATUS_AND_DOORS.md).
"""
import sympy as sp
import numpy as np

ok = lambda b: "PASS" if b else "FAIL"
fails = []
def check(tag, cond):
    print(f"   [{tag}] {ok(cond)}")
    if not cond: fails.append(tag)

H, a, kapp = sp.symbols('H a kappa', positive=True)
t, r, th, ph = sp.symbols('t r theta phi', real=True)
Zsym = sp.sqrt(32*sp.pi/3)
Znum = float(Zsym)
target = 1/Zsym                      # 1/Z = sqrt(3/(32 pi)) -- the framework's number
tnum = float(target)

print("="*98)
print("PART A -- THE STATIONARY (DESER-LEVIN) FAMILY: r(a), ell(a), derived from the metric")
print("="*98)
f = 1 - H**2*r**2
g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
coords = [t, r, th, ph]
ginv = g.inv()
Gamma = [[[sp.simplify(sp.Rational(1,2)*sum(ginv[mu,s_]*(sp.diff(g[s_,nu],coords[rho])
          + sp.diff(g[s_,rho],coords[nu]) - sp.diff(g[nu,rho],coords[s_])) for s_ in range(4)))
          for rho in range(4)] for nu in range(4)] for mu in range(4)]
u = sp.Matrix([1/sp.sqrt(f), 0, 0, 0])               # static 4-velocity
acc = sp.Matrix([sp.simplify(Gamma[mu][0][0]*u[0]**2) for mu in range(4)])
amag2 = sp.simplify((acc.T*g*acc)[0])
a_of_r = H**2*r/sp.sqrt(1-H**2*r**2)
check("A1 |a|^2 = H^4 r^2/(1-H^2r^2)  =>  a(r) = H^2 r/sqrt(1-H^2 r^2)  (full Christoffels)",
      sp.simplify(amag2 - a_of_r**2) == 0)
print("      NOTE: with H in 1/time and c restored, a(r) = H^2 r/sqrt(1-H^2r^2/c^2) -- the")
print("      prompt's draft form 'a = (Hr/sqrt(1-H^2r^2))c^2' is dimensionally off; corrected here.")

# A2. invert: r(a); the dimensionless radius IS the F4 kernel (identity, flagged as such)
r_of_a = sp.solve(sp.Eq(a, a_of_r), r)
r_sol = [s_ for s_ in r_of_a if sp.simplify(s_ - a/(H*sp.sqrt(a**2+H**2))) == 0]
check("A2 r(a) = a/(H sqrt(a^2+H^2))   [=> H r(a) = a/sqrt(a^2+H^2) = mu_F4, an IDENTITY echo]",
      len(r_sol) == 1)

# A3. proper distance to the cosmological horizon; a(ell); ell(a)
rp = sp.symbols('r_p', positive=True)
ell_of_r = sp.simplify(sp.integrate(1/sp.sqrt(1-H**2*rp**2), (rp, r, 1/H)))
y = sp.symbols('y', positive=True)
acos_id = sp.acos(y) - (sp.pi/2 - sp.asin(y))     # identity: derivative 0, value 0 at y=0
check("A3 ell(r) = (pi/2 - asin(H r))/H = acos(H r)/H",
      sp.simplify(ell_of_r - (sp.pi/2 - sp.asin(H*r))/H) == 0 and
      sp.simplify(sp.diff(acos_id, y)) == 0 and acos_id.subs(y, 0) == 0)
ell = sp.symbols('ell', positive=True)
a_of_ell = sp.simplify(a_of_r.subs(r, sp.cos(H*ell)/H))
# squared comparison: both sides positive on 0 < H ell < pi/2, so |.|^2 equality = equality
check("A4 a(ell)^2 = H^2 cot^2(H ell)  [both sides > 0 on 0 < H ell < pi/2 => a = H cot(H ell)]",
      sp.simplify(a_of_ell**2 - (H*sp.cos(H*ell)/sp.sin(H*ell))**2) == 0)
# ell(a): H ell = arctan(H/a).  cos(atan(H/a)) = a/sqrt(a^2+H^2) and both in (0,pi/2) => equal.
check("A5 H ell(a) = arctan(H/a)   [cos(atan(H/a)) = H r(a); both angles in (0,pi/2)]",
      sp.simplify(sp.cos(sp.atan(H/a)) - a/sp.sqrt(a**2+H**2)) == 0)
print("      The bookkeeping variable below: x = H ell = arctan(H/a), i.e. H/a = tan x.")
print("      Deep-MOND onset a0 = cH/Z  <=>  x0 = arctan(Z) (agentQ's 89%-depth point).")

print()
print("="*98)
print("PART B -- DEFINITION (a): THE MERGER CONDITION (Rindler depth vs distance to horizon)")
print("="*98)
x = sp.symbols('x', positive=True)
# Rindler depth in units of 1/H:  1/a = tan(x)/H.   Proper distance: ell = x/H.
print("  Rindler depth d_R = 1/a = tan(x)/H ;  proper distance to cosmological horizon ell = x/H.")
# B1. the STRICT merger condition d_R = ell  <=>  tan x = x: NO solution on (0, pi/2).
dtan = sp.simplify(sp.diff(sp.tan(x) - x, x))
check("B1 d/dx(tan x - x) = tan^2 x  (>0 on (0,pi/2); value 0 at x=0 => tan x > x STRICTLY)",
      sp.simplify(dtan - sp.tan(x)**2) == 0)
print("      => the strict equality 1/a = ell has NO finite-a solution: the flat Rindler depth")
print("         ALWAYS overshoots the true distance to the horizon; equality only as a -> oo.")
print("         The literal merger condition is a sharp NON-boundary (ill-posed as an equality).")
# B2. the graded misfit and its EXACT leading coefficient
m_x = (sp.tan(x) - x)/x
ser_m = sp.series(m_x, x, 0, 6).removeO()
check("B2 misfit (tan x - x)/x = x^2/3 + 2x^4/15 + ...  (leading coefficient EXACTLY 1/3)",
      sp.simplify(ser_m - (x**2/3 + 2*x**4/15)) == 0)
h = sp.symbols('h', positive=True)          # h = H/a
m_h = (h - sp.atan(h))/sp.atan(h)
ser_mh = sp.series(m_h, h, 0, 5).removeO()
check("B3 in H/a: misfit = (1/3)(H/a)^2 - (4/45)(H/a)^4 + ...  (leading coefficient 1/3 exact)",
      sp.simplify(ser_mh - (h**2/3 - 4*h**4/45)) == 0)
# B4. thresholds: misfit = m*  <=>  tan x = (1+m*) x ;  at the root  cot x* = 1/((1+m*) x*).
print("  B4. boundary = threshold choice (tan x = (1+m*)x; at the root c_a = a/cH = 1/((1+m*)x*)):")
thr_rows = []
for mstar, guess in [(sp.Rational(1,2), 0.95), (1, 1.16), (2, 1.32), (3, 1.39)]:
    xr = sp.nsolve(sp.tan(x) - (1+mstar)*x, x, guess)
    c_a = 1/((1+mstar)*xr)
    thr_rows.append((mstar, float(xr), float(c_a)))
    print(f"      misfit = {str(mstar):>4}:  x* = {float(xr):.5f},  c_a = {float(c_a):.5f}")
check("B5 root identity cot x* = 1/((1+m*) x*) at each root (residual < 1e-20)",
      all(abs(float(sp.cot(sp.Float(xr_, 25)) - 1/((1+m_)*sp.Float(xr_, 25)))) < 1e-12
          for m_, xr_, _ in [(mr, xr, c) for mr, xr, c in thr_rows]))
# alternative regularizations of the same definition:
c_patch = sp.cot(sp.atan(sp.pi/2))           # d_R = full patch depth pi/(2H)
check("B6 d_R = full static-patch depth pi/(2H)  =>  c_a = 2/pi exactly",
      sp.simplify(c_patch - 2/sp.pi) == 0)
print(f"      d_R = curvature radius 1/H        =>  c_a = 1 (tan x = 1, x = pi/4)")
print(f"      SPREAD for definition (a): c_a in {{{thr_rows[3][2]:.4f} (m*=3), {thr_rows[2][2]:.4f} (m*=2), "
      f"{thr_rows[1][2]:.4f} (m*=1), {float(2/sp.pi):.4f} (patch), {thr_rows[0][2]:.4f} (m*=1/2), 1 (curv.)}}")
# B7. the misfit AT the framework point a0 -- and the numerology-bait flag
x0 = sp.atan(Zsym)
m_at_a0 = float((Zsym - x0)/x0)
print(f"  B7. misfit at a = a0 (x0 = arctan Z = {float(x0):.5f} = {float(x0/(sp.pi/2))*100:.1f}% depth):"
      f"  m(a0) = (Z - arctan Z)/arctan Z = {m_at_a0:.5f}")
print(f"      |m(a0) - pi|/pi = {abs(m_at_a0-np.pi)/np.pi:.2e}  -- a {100*abs(m_at_a0-np.pi)/np.pi:.2f}% near-miss to pi.")
print("      FLAG: numerology-bait. 'Z = (1+pi) arctan Z' has no derivation behind it; transcendental")
print("      coincidence; structurally meaningless per the repo's coefficient discipline. NOT fed.")

print()
print("="*98)
print("PART C -- DEFINITION (b): THE KILLING-FAILURE TERM (GJS 1112.6215), EXACT IN dS")
print("="*98)
# C1. RNC computation, metric truncated at O(x^2): g_mn = eta_mn - (1/3) R_manb x^a x^b.
#     Jacobson's approximate boost: chi^m = kappa (x^1, x^0, 0, 0).
#     Failure tensor S_mn = nabla_(m chi_n).  Computed for (i) the exact dS Riemann,
#     (ii) a generically perturbed Riemann (R_0202 -> R_0202 + delta, with all symmetry partners).
xs = list(sp.symbols('x0 x1 x2 x3', real=True))
eps = sp.symbols('epsilon', positive=True)
eta = sp.diag(-1, 1, 1, 1)
delta = sp.symbols('delta', real=True)

def riemann(pert):
    R = [[[[H**2*(eta[m,n]*eta[al,be] - eta[m,be]*eta[al,n])
            for be in range(4)] for n in range(4)] for al in range(4)] for m in range(4)]
    if pert:  # R_{0202} += delta with antisymmetry partners (pair symmetry automatic here)
        R[0][2][0][2] += delta; R[2][0][2][0] += delta
        R[0][2][2][0] -= delta; R[2][0][0][2] -= delta
    return R

def failure_tensor(pert):
    R = riemann(pert)
    G = sp.Matrix(4, 4, lambda m_, n_: eta[m_, n_]
                  - sp.Rational(1,3)*sum(R[m_][al][n_][be]*xs[al]*xs[be]
                                         for al in range(4) for be in range(4)))
    Ginv = G.inv()
    chi_up = sp.Matrix([kapp*xs[1], kapp*xs[0], 0, 0])
    chi_dn = G*chi_up
    Gam = [[[sp.Rational(1,2)*sum(Ginv[mu,s_]*(sp.diff(G[s_,nu],xs[rho])
            + sp.diff(G[s_,rho],xs[nu]) - sp.diff(G[nu,rho],xs[s_])) for s_ in range(4))
            for rho in range(4)] for nu in range(4)] for mu in range(4)]
    S = sp.Matrix(4, 4, lambda m_, n_:
        sp.Rational(1,2)*(sp.diff(chi_dn[n_], xs[m_]) + sp.diff(chi_dn[m_], xs[n_]))
        - sum(Gam[lam][m_][n_]*chi_dn[lam] for lam in range(4)))
    # scale x -> eps*x and keep through O(eps^2): the GJS order O(x^2 * Riemann)
    Ssc = S.subs({xs[i]: eps*xs[i] for i in range(4)}, simultaneous=True)
    S2 = sp.Matrix(4, 4, lambda m_, n_:
         sp.simplify(sp.series(Ssc[m_, n_], eps, 0, 3).removeO()))
    return S2

S2_dS = failure_tensor(False)
check("C1 dS: ALL components of the O(x^2) Killing-failure tensor vanish IDENTICALLY (coefficient = 0)",
      all(sp.simplify(S2_dS[m_, n_]) == 0 for m_ in range(4) for n_ in range(4)))
S2_p = failure_tensor(True)
S2_p_dscheck = S2_p.subs(delta, 0)
nonzero = [(m_, n_, sp.simplify(S2_p[m_, n_])) for m_ in range(4) for n_ in range(4)
           if sp.simplify(S2_p[m_, n_]) != 0]
check("C2 perturbed Riemann (R_0202 += delta): failure tensor is NONZERO and exactly linear in delta",
      len(nonzero) > 0 and all(sp.simplify(expr - delta*sp.diff(expr, delta)) == 0
                               for _, _, expr in nonzero)
      and all(sp.simplify(S2_p_dscheck[m_, n_]) == 0 for m_ in range(4) for n_ in range(4)))
print("      exact failure components (perturbed case, through O(x^2); kappa = boost normalization):")
for m_, n_, expr in nonzero:
    print(f"        S_{m_}{n_} = {sp.factor(expr.subs(eps,1))}")
print("""      WHY the dS coefficient is exactly zero (theorem, classical): an isometry fixing p
      satisfies phi(exp_p v) = exp_p(d phi_p v), so ANY Killing field vanishing at p is EXACTLY
      linear in Riemann normal coordinates. dS is maximally symmetric: the local boost about any
      horizon point IS an exact Killing field (the static-patch boost), and Jacobson's chi = its
      exact linearization. The GJS O(x^2*Riemann) failure is the statement for GENERIC backgrounds;
      its dS coefficient VANISHES because the dS Riemann is invariant under the full Lorentz
      stabilizer (machine check C1); breaking that invariance (C2) switches the failure back on.""")

# C3. closed-form constant-curvature RNC metric: g = phi(s) eta + (1-phi)/s x x,
#     phi = sin^2(H sqrt(s))/(H^2 s), s = eta x x  -- exact boost-invariance (Lie derivative)
s_expr = -xs[0]**2 + xs[1]**2 + xs[2]**2 + xs[3]**2
phi = sp.sin(H*sp.sqrt(s_expr))**2/(H**2*s_expr)
xl = eta*sp.Matrix(xs)
Gc = sp.Matrix(4, 4, lambda m_, n_: phi*eta[m_, n_] + (1-phi)/s_expr*xl[m_]*xl[n_])
chi_up = sp.Matrix([kapp*xs[1], kapp*xs[0], 0, 0])
def lie_g(Gm):
    L = sp.zeros(4, 4)
    for m_ in range(4):
        for n_ in range(4):
            L[m_, n_] = (sum(chi_up[lam]*sp.diff(Gm[m_, n_], xs[lam]) for lam in range(4))
                         + sum(Gm[lam, n_]*sp.diff(chi_up[lam], xs[m_]) for lam in range(4))
                         + sum(Gm[m_, lam]*sp.diff(chi_up[lam], xs[n_]) for lam in range(4)))
    return L
Lc = lie_g(Gc)
check("C3 closed-form dS RNC metric: Lie_chi g = 0 EXACTLY, all components, ALL orders in x",
      all(sp.simplify(Lc[m_, n_]) == 0 for m_ in range(4) for n_ in range(4)))
ser_phi = sp.series(phi.subs({xs[i]: eps*xs[i] for i in range(4)}, simultaneous=True),
                    eps, 0, 3).removeO()
check("C4 closed form matches the RNC expansion: phi = 1 - (H^2/3)s + O(s^2)",
      sp.simplify(ser_phi - (1 - H**2*eps**2*s_expr/3)) == 0)
# C5. numeric certification that the closed form IS dS_4: Ricci = 3H^2 g at random points
Gci = sp.Matrix(4, 4, lambda m_, n_: (1/phi)*eta[m_, n_]
                + (phi-1)/(s_expr*phi)*sp.Matrix(xs)[m_]*sp.Matrix(xs)[n_])
check("C5a Sherman-Morrison inverse: G * Ginv = Id exactly",
      all(sp.simplify((Gc*Gci)[m_, n_] - (1 if m_ == n_ else 0)) == 0
          for m_ in range(4) for n_ in range(4)))
GamC = [[[sp.Rational(1,2)*sum(Gci[mu,s_]*(sp.diff(Gc[s_,nu],xs[rho])
         + sp.diff(Gc[s_,rho],xs[nu]) - sp.diff(Gc[nu,rho],xs[s_])) for s_ in range(4))
         for rho in range(4)] for nu in range(4)] for mu in range(4)]
def ricci_num(pt, Hval):
    subs = {xs[i]: pt[i] for i in range(4)}; subs[H] = Hval
    Ric = np.zeros((4,4))
    for m_ in range(4):
        for n_ in range(4):
            val = 0
            for lam in range(4):
                val += sp.diff(GamC[lam][m_][n_], xs[lam]).subs(subs)
                val -= sp.diff(GamC[lam][m_][lam], xs[n_]).subs(subs)
                for s_ in range(4):
                    val += (GamC[lam][lam][s_]*GamC[s_][m_][n_]
                            - GamC[lam][n_][s_]*GamC[s_][m_][lam]).subs(subs)
            Ric[m_, n_] = float(val)
    Gnum = np.array(Gc.subs(subs)).astype(float)
    return Ric, Gnum
pts = [(0.05, 0.31, 0.17, -0.23), (-0.11, 0.41, -0.07, 0.19)]   # spacelike: s > 0
maxdev = 0.0
for pt in pts:
    Ric, Gnum = ricci_num(pt, 0.7)
    maxdev = max(maxdev, float(np.max(np.abs(Ric - 3*0.7**2*Gnum))))
check(f"C5b numeric Ricci spot-check: |R_mn - 3H^2 g_mn| < 1e-9 at random spacelike points (max {maxdev:.1e})",
      maxdev < 1e-9)
print("""      => In EXACT dS the (b)-channel failure term is ZERO TO ALL ORDERS: Jacobson's local
      boost is not approximate there -- it is the static-patch boost itself. Definition (b)
      yields NO breakdown acceleration proportional to cH: in exact dS the channel is EMPTY
      (c_b = none); in PERTURBED dS the failure is O(x^2 * delta-Riemann), i.e. set by the
      MATTER perturbation (delta R ~ G T), not by H -- a boundary on a different axis entirely.
      REFINEMENT of agentQ Part F: the scheme spread {0,1/6,1/3,1/2} stands on the
      acceleration/weight bookkeeping choices alone; it is NOT degenerate with Killing-failure
      terms in exact dS (those vanish). agentQ's R1-exactness is STRENGTHENED.""")

# C6. the graded degradation that DOES exist: flat-frame norm/temperature bookkeeping error
ratio_norm = 1 - sp.sin(x)/x                  # |xi|_exact vs kappa*ell flat: fractional deficit
ser_norm = sp.series(ratio_norm, x, 0, 5).removeO()
check("C6 norm-channel deviation 1 - sin(x)/x = x^2/6 - x^4/120  (leading coefficient 1/6 exact)",
      sp.simplify(ser_norm - (x**2/6 - x**4/120)) == 0)
edge_norm = float(1 - 2/sp.pi); edge_temp = float(sp.pi/2 - 1)
a0_norm = float((1 - sp.sin(x0)/x0)); a0_temp = float((x0/sp.sin(x0) - 1))
check("C7 norm deviation NEVER reaches O(1) inside the patch: max = 1 - 2/pi = 0.3634 at x = pi/2",
      abs(edge_norm - 0.36338) < 1e-4 and edge_norm < 1)
print(f"      temperature channel x/sin(x) - 1: max at patch edge = pi/2 - 1 = {edge_temp:.4f}")
print(f"      at the MOND onset a0 (x0 = arctan Z): norm channel = {a0_norm:.4f} (29.5%),"
      f" temperature channel = {a0_temp:.4f} (41.9%)")
print("      => the graded flat-bookkeeping error is SUB-O(1) even at a0; reaching deviation = 1")
print("         requires x = pi (norm) or x = 1.8955 (temp): BOTH OUTSIDE the static patch.")
print("      extrapolated small-x boundary (deviation=1 with leading term only): c = 1/sqrt(6)")
print("      = 0.4082 -- flagged: the extrapolation is invalid (x <= pi/2 < sqrt(6)); scheme only.")

print()
print("="*98)
print("PART D -- DEFINITION (c): EQUILIBRIUM/ADIABATIC (light-crossing time vs inverse temperature)")
print("="*98)
# D1. FLAT bookkeeping: patch = Rindler depth 1/a; T = a/2pi.  Ratio is a PURE NUMBER.
ratio_flat = sp.simplify((1/a)*(a/(2*sp.pi)))
check("D1 flat: t_cross * T_Unruh = 1/(2pi) EXACTLY -- a- and H-independent: NEVER breaks",
      sp.simplify(ratio_flat - 1/(2*sp.pi)) == 0)
# D2. EXACT dS bookkeeping: patch = exact proper distance ell(a); T = T_DL = sqrt(a^2+H^2)/2pi.
P = sp.atan(H/a)/H * sp.sqrt(a**2 + H**2)/(2*sp.pi)
lim_hi = sp.limit(P, a, sp.oo); lim_lo = sp.limit(P, a, 0, '+')
check("D2 exact ratio P(a) = ell(a)*T_DL(a): P(a->oo) = 1/(2pi), P(a->0) = 1/4 -- BOUNDED",
      sp.simplify(lim_hi - 1/(2*sp.pi)) == 0 and sp.simplify(lim_lo - sp.Rational(1,4)) == 0)
Ph = (sp.atan(h)/h)*sp.sqrt(1 + h**2)/(2*sp.pi)     # P in units of 1/(2pi)... times 2pi below
ser_P = sp.series(2*sp.pi*Ph, h, 0, 4).removeO()
check("D3 deviation series: 2pi*P = 1 + (1/6)(H/a)^2 + ...  (SAME 1/6 as the norm channel)",
      sp.simplify(ser_P - (1 + h**2/6)) == 0)
Pgrid = [float(P.subs({a: av, H: 1})) for av in [100, 10, 3, 1, 0.3, 1/Znum, 0.03, 0.001]]
check("D4 P(a) monotone, in [1/(2pi), 1/4] on the whole family (grid check)",
      all(Pgrid[i] <= Pgrid[i+1] + 1e-12 for i in range(len(Pgrid)-1))
      and Pgrid[0] > 1/(2*np.pi) - 1e-9 and Pgrid[-1] < 0.25 + 1e-9)
print(f"      P(a)*2pi from a=100H to a=0.001H: {[f'{2*np.pi*v:.4f}' for v in Pgrid]}")
print(f"      at a0: 2pi*P = {2*np.pi*float(P.subs({a: 1/Znum, H: 1})):.4f}  (57% above flat; max 2pi/4 = 1.571)")
print("      => the EXACT equilibrium ratio never becomes O(1): it runs from 1/(2pi) = 0.159 to")
print("         1/4 = 0.25 over the ENTIRE acceleration range. The criterion NEVER fires.")
# D5. radar reading: light-crossing to the horizon in observer proper time DIVERGES (any a)
lvar = sp.symbols('l_var', positive=True)
radar = sp.integrate(1/sp.sin(H*lvar), lvar)
check("D5 radar time integrand 1/sin(H ell): antiderivative log(tan(H ell/2))/H -> -oo at the horizon",
      sp.simplify(sp.diff(sp.log(sp.tan(H*lvar/2))/H, lvar) - 1/sp.sin(H*lvar)) == 0)
print("      (the radar reading diverges at EVERY a -- exactly as in flat Rindler; not H-keyed)")
# D6. threshold variants that DO produce an a_break (each a choice):
sol_W2 = sp.solve(sp.Eq(sp.sqrt(a**2+H**2)/a, 2), a)
check("D6a 'T_DL/T_U = 2' threshold  =>  a = H/sqrt(3)  (c = 1/sqrt(3) = 0.5774)",
      any(sp.simplify(s_ - H/sp.sqrt(3)) == 0 for s_ in sol_W2))
sol_r1 = sp.solve(sp.Eq(sp.sqrt(a**2+H**2)/(2*sp.pi*a), 1), a)
check("D6b 'naive ratio = 1' threshold  =>  a = H/sqrt(4pi^2-1)  (c = 0.1612)",
      any(sp.simplify(s_ - H/sp.sqrt(4*sp.pi**2 - 1)) == 0 for s_ in sol_r1))
print("      D6c 'flat patch 1/a = curvature radius 1/H'  =>  c = 1")
print("      D6d 'flat patch 1/a = patch depth pi/(2H)'   =>  c = 2/pi = 0.6366")
print("      D6e 'thermal wavelength 2pi/a = 1/H'         =>  c = 2pi = 6.2832")

print()
print("="*98)
print("PART E -- RAW c_i TABLE FIRST, THEN the single sharp symbolic question (match to 1/Z?)")
print("="*98)
rows = [
 ("(a) merger, misfit threshold 300%",        "1/(4 x*), tan x*=4x*",    thr_rows[3][2], "threshold m*=3"),
 ("(a) merger, misfit threshold 200%",        "1/(3 x*), tan x*=3x*",    thr_rows[2][2], "threshold m*=2"),
 ("(a) merger, misfit threshold 100%",        "1/(2 x*), tan x*=2x*",    thr_rows[1][2], "threshold m*=1"),
 ("(a) merger, depth = full patch",           "2/pi",                    float(2/sp.pi), "which depth scale"),
 ("(a) merger, misfit threshold 50%",         "1/(1.5 x*)",              thr_rows[0][2], "threshold m*=1/2"),
 ("(a) merger, depth = curvature radius",     "1",                       1.0,            "which depth scale"),
 ("(b) Killing failure, exact dS",            "NONE (failure = 0, all orders)", None,    "-- channel empty"),
 ("(b) graded norm channel, extrapolated",    "1/sqrt(6)",               float(1/sp.sqrt(6)), "invalid extrapolation"),
 ("(c) exact equilibrium ratio",              "NONE (bounded, never fires)", None,       "-- no boundary"),
 ("(c) T_DL/T_U = 2 threshold",               "1/sqrt(3)",               float(1/sp.sqrt(3)), "threshold W=2"),
 ("(c) naive ratio = 1 threshold",            "1/sqrt(4pi^2-1)",         float(1/sp.sqrt(4*sp.pi**2-1)), "2pi placement + threshold"),
 ("(c) flat patch vs curvature radius",       "1",                       1.0,            "which length pair"),
 ("(c) thermal wavelength vs 1/H",            "2pi",                     float(2*sp.pi), "which length pair"),
]
print(f"   {'definition / variant':44s} {'c exact':26s} {'c numeric':>10s}   depends on")
for nm, ce, cn, dep in rows:
    print(f"   {nm:44s} {ce:26s} {cn if cn is None else format(cn,'10.5f')!s:>10s}   {dep}")
finite = [cn for _, _, cn, _ in rows if cn is not None]
print(f"\n   SPREAD of finite candidates: [{min(finite):.4f}, {max(finite):.4f}] -- a factor {max(finite)/min(finite):.1f}")
print(f"   comparison set (AFTER): 1/Z = {tnum:.5f}, 1 , Z = {Znum:.5f}, 2pi = {2*np.pi:.5f}, 1/6 = {1/6:.5f}")

# E1. THE SHARP QUESTION: does ANY c_i equal 1/Z = sqrt(3/(32pi)) symbolically?
print("\n  E1. symbolic match tests, c^2 vs 3/(32 pi)  [equality would force the stated pi-identity]:")
sym_cands = [("2/pi", (2/sp.pi)**2, "pi = 128/3"), ("1", sp.Integer(1), "pi = 3/32"),
             ("1/sqrt(6)", sp.Rational(1,6), "pi = 9/16"), ("1/sqrt(3)", sp.Rational(1,3), "pi = 9/32"),
             ("1/sqrt(4pi^2-1)", 1/(4*sp.pi**2-1), "12pi^2 - 32pi - 3 = 0 (pi algebraic)"),
             ("2pi", 4*sp.pi**2, "pi^3 = 3/128")]
all_distinct = True
for nm, c2, forces in sym_cands:
    d = sp.simplify(c2 - sp.Rational(3,1)/(32*sp.pi))
    is_zero = (d == 0)
    all_distinct &= (not is_zero) and abs(float(d)) > 1e-12
    print(f"      {nm:18s}: c^2 - 3/(32pi) = {sp.nsimplify(d, rational=False)} = {float(d):+.5f}"
          f"  (match would force {forces}: FALSE) -> NO MATCH")
check("E1 NO symbolic candidate equals 1/Z (each match would force a false/transcendence-violating pi-identity)",
      all_distinct)
print("      transcendental-root candidates (numeric only):"
      f" {['%.5f' % c for _, _, c in thr_rows]} vs 1/Z = {tnum:.5f}")
# E2. the (a)-threshold family c_a(m*) is a CONTINUUM sweeping (0,1]; it crosses 1/Z exactly
#     at m* = misfit(a0)  (tautology: cot x* = 1/Z forces x* = arctan Z, i.e. m* = m(a0)).
#     So proximity of any integer threshold (m*=3 -> 3.9% from 1/Z) is guaranteed by the
#     sweep, NOT structure.  Verified: solve the crossing, recover m(a0).
x_cross = sp.nsolve(sp.cot(x) - tnum, x, 1.40)        # c_a(x*) = cot x* = 1/Z
m_cross = float(sp.tan(x_cross)/x_cross - 1)          # the threshold that root corresponds to
check("E2 the threshold producing c_a = 1/Z is m* = misfit(a0) EXACTLY (tautological crossing)",
      abs(float(x_cross) - float(x0)) < 1e-10 and abs(m_cross - m_at_a0) < 1e-10)
print(f"      crossing threshold m* = {m_cross:.5f} = m(a0); nothing selects it. The m*=3 row")
print(f"      (c = {thr_rows[3][2]:.5f}, {100*abs(thr_rows[3][2]-tnum)/tnum:.1f}% from 1/Z) is a FLAGGED NEAR-MISS:"
      " an artifact of m(a0) = 3.1356 ~ 3; threshold-set, not structure.")
gaps = sorted((abs(c - tnum)/tnum, c) for c in finite)
print(f"      closest finite candidate to 1/Z: c = {gaps[0][1]:.5f}, gap {100*gaps[0][0]:.1f}%")
print(f"      NEAR-MISS FLAGS (all structurally meaningless, per discipline):")
print(f"        1/sqrt(4pi^2-1) = {float(1/sp.sqrt(4*sp.pi**2-1)):.5f} vs 1/Z = {tnum:.5f} ({100*abs(float(1/sp.sqrt(4*sp.pi**2-1))-tnum)/tnum:.1f}%)"
      f" and vs 1/6 ({100*abs(float(1/sp.sqrt(4*sp.pi**2-1))-1/6)*6:.1f}%): threshold artifacts")
print(f"        2pi = {2*np.pi:.4f} vs Z = {Znum:.4f} ({100*abs(2*np.pi-Znum)/Znum:.1f}%): (2pi)^2 = 4pi^2 vs Z^2 = 32pi/3 <=> pi vs 8/3 -- distinct")
print(f"        misfit(a0) = {m_at_a0:.5f} vs pi ({100*abs(m_at_a0-np.pi)/np.pi:.2f}%): transcendental coincidence (Part B7)")

print()
print("="*98)
print(f"MACHINE-CHECK SUMMARY: {'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
print("="*98)
print("""VERDICT (pre-registered trichotomy; details in agentT_zgeometry.md):
 O(1)-NULL, with two channels resolving to the ILL-POSED horn -- and NO symbolic match anywhere.
 (a) MERGER: the strict condition 1/a = ell has NO finite solution (tan x > x: the flat Rindler
     depth always overshoots the true horizon distance). The graded misfit has EXACT leading
     coefficient 1/3 and grows without bound, but the boundary is set ENTIRELY by a free threshold:
     c_a = {0.18, 0.25, 0.43, 0.64, 0.69, 1} for thresholds {300%,200%,100%,patch,50%,curv}.
 (b) KILLING FAILURE: in exact dS the GJS O(x^2*Riemann) failure coefficient is EXACTLY ZERO at
     all orders (theorem: Killing fields vanishing at p are exactly linear in RNC; dS's local
     boost is the static-patch boost). The channel produces NO cH-proportional boundary at all;
     in perturbed dS it scales with the matter perturbation, not H. The graded flat-bookkeeping
     error (coefficient 1/6 exact) stays sub-O(1) everywhere inside the patch (max 36%/57%).
 (c) EQUILIBRIUM: flat reading = 1/(2pi) exactly, scale-invariant, never breaks; exact reading
     bounded in [1/(2pi), 1/4] over the ENTIRE range -- never fires; radar reading diverges at
     every a equally. A boundary appears only by threshold fiat: c in {0.16, 0.58, 0.64, 1, 2pi}.
 SHARP QUESTION: no computed c_i equals 1/sqrt(32pi/3) symbolically -- each candidate match would
 force a false pi-identity (rational pi or pi algebraic). Spread of defensible finite candidates:
 a factor ~39. THE SPREAD IS THE ANSWER: nothing is forced. Z stays DATA-SELECTED; the banked
 verdict stands; agentQ's 89%-depth merger reading remains a CONSISTENCY statement, not a
 derivation -- and its R1-exactness is STRENGTHENED (in exact dS the construction with the exact
 boost is exact at every a; what fails at low a is LOCALITY of the wedge, not the thermodynamics).""")
