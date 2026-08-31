"""Skeptic-1 lens: alpha_1 anchor + cancellation, independent re-derivation.

A. Published Foster-Jacobson alpha_1/alpha_2 (Jacobson status report 0801.1547 Eqs)
   evaluated INDEPENDENTLY at the wf3 control points -> guards against the
   control run validating against a mis-transcribed FJ target (circularity).
   Then the Maxwell/base locus c1=K_B, c3=-K_B, c2=c4=0 -> alpha_1 = -4K_B.
B. delta-Q structural content: linearize Q = A^mu d_mu phi about
   A=(1,0,0,0)+pert, phi = Q0*t + chi, metric pert incl. h_0i, unit-norm
   constraint -> show transverse aether NEVER enters delta Q at linear order,
   so -F_QQ (dQ)^2 cannot contribute to (or cancel) the transverse O(w)
   response; its only Q0-free quadratic piece is (w.q)^2 chi^2 (w_par only).
C. eta_K = (K_B J_Y + 2)/(J_Y + 1): limits and zero locus; alpha_1 bounds on
   healthy locus; the K_B<2.5e-5 escape under both formulas.
"""
import sympy as sp

# ---------- A. Foster-Jacobson anchor ----------
c1, c2, c3, c4, KB = sp.symbols('c1 c2 c3 c4 K_B', real=True)
c14 = c1 + c4
c123 = c1 + c2 + c3
alpha1_FJ = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
alpha2_FJ = alpha1_FJ/2 - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)/(c123*(2 - c14))

pts = [((sp.Rational(3,10), sp.Rational(1,5), sp.Rational(1,10), sp.Rational(1,20)),
        (sp.Rational(-5,13), sp.Rational(-461,572))),
       ((sp.Rational(1,5), sp.Rational(2,5), sp.Rational(-1,10), sp.Rational(1,10)),
        (sp.Rational(-24,37), sp.Rational(-428,3145)))]
print("A. FJ independent evaluation vs wf3 control targets:")
for (cv, (a1t, a2t)) in pts:
    s = dict(zip((c1,c2,c3,c4), cv))
    a1 = sp.nsimplify(alpha1_FJ.subs(s)); a2 = sp.nsimplify(sp.together(alpha2_FJ.subs(s)))
    print("  c=%s  alpha1=%s (target %s, match=%s)  alpha2=%s (target %s, match=%s)"
          % (cv, a1, a1t, sp.simplify(a1-a1t)==0, a2, a2t, sp.simplify(a2-a2t)==0))

# Maxwell locus
sM = {c1: KB, c2: 0, c3: -KB, c4: 0}
a1M = sp.simplify(alpha1_FJ.subs(sM))
print("  Maxwell locus (c1=K_B,c3=-K_B,c2=c4=0): alpha_1 =", a1M, " (anchor -4K_B:",
      sp.simplify(a1M + 4*KB) == 0, ")")
print("  c123 at Maxwell locus =", sp.simplify(c123.subs(sM)),
      " -> alpha_2_FJ denominator vanishes (spin-0 singular w/o scalar):",
      sp.simplify(c123.subs(sM)) == 0)
# spin-1 speed at Maxwell locus (Jacobson): s1^2=(2c1-c1^2+c3^2)/(2 c14 (1-c13))
s1sq = sp.simplify(((2*c1 - c1**2 + c3**2)/(2*c14*(1-(c1+c3)))).subs(sM))
print("  spin-1 speed^2 at Maxwell locus =", s1sq, "(K_B-independent)")

# ---------- B. delta-Q structural content ----------
print("\nB. delta-Q content (linearized, clock background Q0):")
t, x, y, z, eps = sp.symbols('t x y z eps', real=True)
Q0 = sp.symbols('Q0', real=True)
# perturbations: keep FULL generality: dA0, aL (longitudinal), aT (transverse),
# metric h00, h0L, h0T, chi. Represent Fourier-like: q along z.
q, wpar, wperp = sp.symbols('q w_par w_perp', real=True)
dA0, aL, aT1, aT2, chi, h00, h0L, h0T1, h0T2 = sp.symbols(
    'dA0 aL aT1 aT2 chi h00 h0L h0T1 h0T2', real=True)
# g_{munu} = eta + eps*h ; A^mu = (1+eps*dA0u, eps*a^i) with a^z=aL, a^x=aT1, a^y=aT2
# unit constraint g_mn A^m A^n = -1 at O(eps): -(1+eps h00... ) ...
h = sp.zeros(4,4)
h[0,0] = h00; h[0,3] = h0L; h[3,0] = h0L; h[0,1] = h0T1; h[1,0] = h0T1
h[0,2] = h0T2; h[2,0] = h0T2
eta = sp.diag(-1,1,1,1)
g = eta + eps*h
Aup = sp.Matrix([1 + eps*dA0, eps*aT1, eps*aT2, eps*aL])
norm = (Aup.T*g*Aup)[0,0]
# O(eps) of norm+1 = 0 fixes dA0:
normO1 = sp.expand(norm + 1).coeff(eps, 1)
dA0_sol = sp.solve(sp.Eq(normO1, 0), dA0)[0]
print("  unit-norm O(eps): dA0 =", dA0_sol, " (no h0i, no a^i -> pure h00)")
# phi = Q0*t + eps*chi(t,z-ish). Q = A^mu d_mu phi.
# d_mu phi = (Q0 + eps*chi_t, eps*chi_x, eps*chi_y, eps*chi_z); chi has only
# gradient along q(z) and convective t-dep: chi_t = -i w.q chi (symbolic markers)
chi_t, chi_z = sp.symbols('chi_t chi_z', real=True)  # placeholders
dphi = sp.Matrix([Q0 + eps*chi_t, 0, 0, eps*chi_z])
Qfull = sp.expand((Aup.T*dphi)[0,0])
QO1 = Qfull.coeff(eps, 1).subs(dA0, dA0_sol)
QO2 = Qfull.coeff(eps, 2).subs(dA0, dA0_sol)
print("  delta Q at O(eps)  =", sp.simplify(QO1))
print("  delta Q at O(eps^2)=", sp.simplify(QO2))
hasT_O1 = any(s in QO1.free_symbols for s in (aT1, aT2, h0T1, h0T2))
hasT_O2 = any(s in QO2.free_symbols for s in (aT1, aT2, h0T1, h0T2))
print("  transverse fields (aT,h0T) in dQ O(eps):", hasT_O1, " O(eps^2):", hasT_O2)
print("  -> -F_QQ (dQ)^2 quadratic action contains NO transverse aether/metric;")
print("     it cannot shift or cancel alpha_1's transverse response. Q0-free")
print("     piece of (dQ^(1))^2 = chi_t^2 -> (w.q)^2 chi^2 (convective), w_par-only.")

# ---------- C. eta_K formula: limits, zero locus, escape hatch ----------
print("\nC. eta_K = (K_B J_Y + 2)/(J_Y + 1):")
JY = sp.symbols('J_Y', positive=True)
etaK = (KB*JY + 2)/(JY + 1)
print("  J_Y->oo limit:", sp.limit(etaK, JY, sp.oo), " (= K_B base anchor: ok)")
print("  J_Y=1 (deep field mu->1):", sp.simplify(etaK.subs(JY,1)), "-> alpha_1 =",
      sp.simplify(-4*etaK.subs(JY,1)))
print("  zero locus: solve eta_K=0 ->", sp.solve(sp.Eq(etaK,0), KB),
      " (needs K_B = -2/J_Y < 0: outside no-ghost K_B>0)")
a1_full = -4*etaK
a1_at = [(kb, sp.nsimplify(a1_full.subs({KB: kb, JY: 1}))) for kb in
         (sp.Rational(1,4), sp.Rational(1,100), sp.Rational(1,10**6))]
print("  alpha_1(J_Y=1) at K_B=1/4, 1e-2, 1e-6:", a1_at)
print("  inf over K_B in (0,1/4] of |alpha_1| at J_Y=1:",
      sp.limit(sp.Abs(a1_full.subs(JY,1)), KB, 0), " (>=4: no K_B escape)")
# Route-3 counterfactual: alpha_1 = -4K_B -> LLR bound 1e-4 -> K_B < 2.5e-5
print("  Route-3 counterfactual: |{-4K_B}|<1e-4 -> K_B <", sp.nsimplify(1e-4)/4)
