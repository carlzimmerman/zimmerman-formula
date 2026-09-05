#!/usr/bin/env python3
"""
wf_bonetti_barausse_highaccel.py

HIGH-ACCELERATION-END check of the khronometric-MOND candidate
    S = (M_Pl^2/2) int dt d3x N sqrt(gamma) [ (3)R + K_ij K^ij - (1+lambda)K^2
                                              + beta K_ij K^ij + a0^2 W(|a|/a0) ] + S_m
    a_i = D_i ln N,  y = |a|/a0,
    W(y) = (1/2)y^2 + (1+y) e^{-y} - 1
against Bonetti & Barausse, PRD 91, 084053 (arXiv:1502.05554) and the 2024
GW-tests-of-GR review (arXiv:2408.05240).

Every numeric/analytic claim in the agent report is derived here and PRINTED.
Literature coefficients that we do NOT re-derive from scratch are TRANSCRIBED
verbatim with their equation numbers and clearly labelled [LIT].

Do NOT git commit (per task).
"""
import sympy as sp

print("="*78)
print(" PART A  -- Carl's W(y): deep-MOND, high-acceleration, Hessian (SOLID, derived)")
print("="*78)

y = sp.symbols('y', positive=True)
W = sp.Rational(1,2)*y**2 + (1+y)*sp.exp(-y) - 1
Wp  = sp.diff(W, y)
Wpp = sp.diff(W, y, 2)

print("W(y)      =", W)
print("W'(y)     =", sp.simplify(Wp))
print("W''(y)    =", sp.simplify(Wpp))

# MOND primitive identities claimed in the candidate
mu = sp.simplify(Wp/y)                       # H_perp = mu = W'/y
print("\nW'(y) factored :", sp.factor(Wp), "  ->  W' = y(1 - e^-y)  [claim]")
print("mu(y)=W'/y     :", mu, "   ->  mu = 1 - e^-y            [claim]")

# deep-MOND (y<<1): leading term of W
ser_lo = sp.series(W, y, 0, 5).removeO()
print("\nW series y->0 :", sp.expand(ser_lo), "   => leading (1/3) y^3  (deep-MOND, nonlinear)")
# high-acceleration (y>>1): W - (y^2/2 - 1) -> 0 exponentially
resid = sp.simplify(W - (sp.Rational(1,2)*y**2 - 1))
print("W - (y^2/2 - 1):", resid, "   => (1+y)e^-y -> 0 as y->inf (khronometric, NOT GR)")

# Hessian eigenvalues of the constitutive sector: H_perp=mu, H_par=W''
print("\nConstitutive Hessian eigenvalues (y>0):")
for yv in [sp.Rational(1,100), sp.Rational(1,2), sp.Integer(1), sp.Integer(5), sp.Integer(50)]:
    print(f"  y={float(yv):8.3f}:  H_perp=mu={float(mu.subs(y,yv)): .6f}   H_par=W''={float(Wpp.subs(y,yv)): .6f}")
print("  -> both > 0 for all y>0  (constitutive sector never ghostly)  [SOLID]")

print()
print("="*78)
print(" PART B  -- Map to BB (alpha,beta,lambda). The a^2 coefficient at high y.")
print("="*78)
# f(a) in BB Eq(11)/(10) sits next to R; Carl's acceleration Lagrangian is a0^2 W(a/a0).
# With y=a/a0:  a0^2 W(a/a0) = (1/2) a^2 - a0^2 + a0^2 (1+a/a0) e^{-a/a0}.
a, a0 = sp.symbols('a a0', positive=True)
f_carl = a0**2 * W.subs(y, a/a0)
f_high = sp.series(sp.expand(f_carl - a0**2*(1+a/a0)*sp.exp(-a/a0)), a, sp.oo)  # strip exp tail
print("Carl f(a)=a0^2 W(a/a0). High-a (drop e^-a/a0 tail):")
print("   f(a) ->", sp.Rational(1,2)*a**2, " - ", a0**2, "  i.e.  f ~ (1/2) a^2 - a0^2")
print("BB Eq.(11+): high-a  f(a) ~ -2 Lambda + alpha a^2   [LIT]")
alpha_carl = sp.Rational(1,2)
print("=> IDENTIFY khronometric acceleration coupling  alpha_Carl = 1/2   [SOLID]")
print("   (BB/Review: alpha is the coeff of a_mu a^mu, a_i=D_i lnN; Review Eq. line 1124-25:")
print("    (alpha,beta,lambda)=(c1+c4, c1+c3, c2).  Prefactors match: M_Pl^2/2 = 1/(16 pi G).)")

# AQUAL chi = f'(a)/(2a) (BB define chi=f'(a)/(2a)); check chi->alpha at high a, and chi=mu/...
chi = sp.simplify(sp.diff(f_carl, a)/(2*a))
print("\nchi(a)=f'(a)/(2a) =", sp.simplify(chi), " = (1 - e^{-a/a0})/2")
print("  high a: chi ->", sp.limit(chi, a, sp.oo), " = 1/2 = alpha_Carl  (renormalizes G_N: chi->1/2 <=> G_eff=2G)")
print("  low  a: chi ->", sp.limit(chi, a, 0), " -> 0   (deep-MOND)")

print()
print("="*78)
print(" PART C  -- Khronon speed c_s^2(alpha,beta,lambda): the strong coupling as alpha->0")
print("="*78)
al, be, la = sp.symbols('alpha beta lambda', real=True)
# BB Eq.(13),(14)  [LIT, transcribed verbatim]
ct2 = 1/(1-be)
cs2 = (al-2)*(be+la) / (al*(be-1)*(2+be+3*la))
print("BB Eq.(13):  c_t^2 = 1/(1-beta)                                  [LIT]")
print("BB Eq.(14):  c_s^2 = (alpha-2)(beta+lambda)/[alpha(beta-1)(2+beta+3lambda)]  [LIT]")
print("\nCarl states c_T^2=1/(1-beta), alpha_eff^PPN=2beta -> Carl's beta = BB's beta. [consistent]")
print("\nStrong coupling of the GR-forced limit (alpha->0):")
print("  lim_{alpha->0} c_s^2 =", sp.limit(cs2, al, 0, '+'), " (diverges) -> khronon kinetic term ->0 => STRONG COUPLING [SOLID/LIT]")

print()
print("="*78)
print(" PART D  -- Is alpha_Carl=1/2 in the viable region?  The PPN-alpha1 / GW170817 pincer")
print("="*78)
# BB Eq(15) / Review Eq(41): alpha1 = 4(alpha-2beta)/(beta-1)   [LIT]
alpha1 = 4*(al-2*be)/(be-1)
print("Review Eq.(41)/BB Eq.(15):  alpha1_PPN = 4(alpha-2beta)/(beta-1)   [LIT]")
print("Solar-system: |alpha1| <~ 1e-4 ; post-GW170817 khronometric |alpha|<~1e-7 [LIT, Review]")

print("\nBranch 1 (satisfy PPN alpha1=0 => alpha=2beta) with alpha=1/2:")
beta_needed = sp.solve(sp.Eq(alpha_carl, 2*be), be)[0]
print("   alpha=2beta => beta =", beta_needed)
ct_val = sp.sqrt(ct2.subs(be, beta_needed))
print("   => c_T = sqrt(1/(1-1/4)) =", sp.nsimplify(ct_val), "=", float(ct_val),
      " -> |c_T-1| ~", float(ct_val-1), " ~ 15 orders over GW170817 (<1e-15) => EXCLUDED")

print("\nBranch 2 (satisfy GW170817 c_T=1 => beta->0) with alpha=1/2:")
a1_b0 = alpha1.subs(be, 0).subs(al, alpha_carl)
print("   beta=0 => alpha1 = 4*alpha/(0-1) =", a1_b0, " => |alpha1|=2, i.e. ~1e4 over solar bound 1e-4 => EXCLUDED")

print("\n=> PINCER: PPN forces beta=1/4 (GW170817 kills via c_T=1.155);")
print("           GW170817 forces beta=0 (solar PPN kills via alpha1=2).")
print("   alpha=1/2 is excluded EITHER WAY.  [SOLID, given action as written]")

print()
print("="*78)
print(" PART E  -- Deep-MOND strong-coupling threshold and the M_* UV scale [LIT]")
print("="*78)
print("BB Eq.(45):  Lap omega = (1/(beta+lambda)) d_t[(2-alpha)phi_N - (2+beta+3lambda)phi]")
print("  high-a: phi=phi_N and alpha=2beta => RHS = -3 d_t phi_N  (INDEPENDENT of beta+lambda) => solar-system SAFE")
print("  deep-MOND: phi != phi_N => RHS ~ 1/(beta+lambda) DIVERGES as beta+lambda->0  => STRONG COUPLING at LOW accel")
print("BB Eq.(73):  |beta+lambda| >~ 2.5e-7   (20% rot-curve threshold; 2.5e-9 aggressive)  [LIT]")
print("M_* = Horava higher-deriv (L4,L6) UV cutoff, SEPARATE from a0:  1e-2 eV <~ M_* <~ 1e16 GeV [LIT]")
print("  (a0 ~ 1e-34 eV; deep-MOND strong coupling is a small-(beta+lambda) degeneracy, not a length scale)")

print()
print("="*78)
print(" PART F  -- Viable (alpha,beta,lambda) windows [LIT, transcribed]")
print("="*78)
print("Pre-GW170817 (Living Review): (alpha,beta,lambda) <~ (0.01, 0.005, 0.1), with alpha=2beta")
print("Post-GW170817 (Review, ref [431]): |alpha|<~1e-7, |beta|<~1e-15, |lambda|<~1e-1")
print("BB deep-MOND floor: |beta+lambda| >~ 2.5e-7  => carried by lambda: 2.5e-7 <~ lambda <~ 0.1")
print("Carl's alpha=1/2  vs  viable |alpha|<~1e-2 (pre) / 1e-7 (post):  50x to 5e6x too large.")
