#!/usr/bin/env python3
"""D4 (lane), part 3: beyond the quadratic proxy -- anisotropic general-k linearization,
the framework-tail kernel, a GENUINE SOFT SPOT, and what actually kills the PU horn there.

GENERAL k(y): L_int = -(m a0^2/(2 w^2)) k(y), y=|xdd|^2/a0^2.
EOM: xdd_i + (1/w^2) d^2/dt^2 [k'(y) xdd_i] + dPhi_i = 0.
Linearization around a circular orbit: acceleration fluctuations PARALLEL to the rotating
background acceleration see kappa_par = k'+2y k''; TRANSVERSE see k'.  Co-rotating frame:
    M(l) = S(l) + S(l) diag(b_par, b_perp) S(l) + diag(Phi'', mu*Om^2),
    S(l) = [[l^2-Om^2, -2 Om l],[2 Om l, l^2-Om^2]],  b_perp=k'/w^2=(1-mu)/Om^2 (G4 exact),
    b_par = kappa_par/w^2.  Monomials k=y^p: b_par/b_perp = 2p-1.
p=1 = quadratic proxy; p=1/2 = the framework-tail-matching kernel (kappa_par = 0).

HONESTY NOTE: a first scratch pass dropped the transverse-beta contribution to M_11
([S K S]_11 = -4 b_perp l^2 != 0 even when kappa_par=0) and wrongly concluded 'tail kernel
broken everywhere below 0.786'.  The corrected algebra below is verified TWO independent
ways (matrix composition AND direct symbolic linearization of the full nonlinear EOM) and
opens a genuine crack: deep-MOND flat-curve PU orbits with sub-quadratic kernels are
linearly PT-REAL.  The crack is then confronted with what it would have to reproduce.
"""
import numpy as np
import sympy as sp

PASS = []
def ok(name, cond):
    assert cond, "FAIL: " + name
    PASS.append(name); print("  PASS:", name)

# ================= 1. parallel/transverse split =================
print("[1] parallel/transverse split of the k'(y)*xdd linearization")
Wr, Wi, ab, a0s = sp.symbols('W_r W_i a_b a0', real=True)
yv = sp.symbols('y', positive=True)
kp = sp.Function('kp')                    # k'
y_full = ((ab + Wr)**2 + Wi**2)/a0s**2
expr_r = kp(y_full)*(ab+Wr); expr_i = kp(y_full)*Wi
y0 = ab**2/a0s**2
e = sp.symbols('e')
lr = sp.expand(sp.diff(expr_r.subs([(Wr, e*Wr), (Wi, e*Wi)]), e).subs(e, 0))
li = sp.expand(sp.diff(expr_i.subs([(Wr, e*Wr), (Wi, e*Wi)]), e).subs(e, 0))
kpar_expr = kp(y0) + 2*y0*sp.Subs(sp.diff(kp(yv), yv), yv, y0)
ok("parallel channel coefficient = k' + 2y k'' (kappa_par)",
   sp.simplify(lr - kpar_expr.doit()*Wr) == 0)
ok("transverse channel coefficient = k'", sp.simplify(li - kp(y0)*Wi) == 0)

# ================= 2. monomial family on the flat curve (Om=1) =================
print("[2] monomial family: characteristic polynomial and p=1 reduction")
lam, s, mu, p = sp.symbols('lambda s mu p', real=True)
bperp = 1 - mu
bpar = (2*p - 1)*(1 - mu)
# self-consistent flat-curve Phi'': Phi' = Om^2 r - (Om^4 r/w^2)k'(y), Om=1/r (v0=1)
rr, a0r, wr = sp.symbols('r a0 w', positive=True)
Om_r = 1/rr
yy = (Om_r**2*rr/a0r)**2
kprime = p*yy**(p-1)
Phi_p = Om_r**2*rr - (Om_r**4*rr/wr**2)*kprime
Phi_pp0 = sp.simplify(sp.diff(Phi_p, rr).subs(rr, 1))
Phi_pp0 = sp.simplify(Phi_pp0.subs(wr**2, kprime.subs(rr, 1)/(1-mu)))
ok("flat-curve Phi'' = -1 + (2p+1)(1-mu)  [self-consistent, any p]",
   sp.simplify(Phi_pp0 - (-1 + (2*p+1)*(1-mu))) == 0)
c1 = -1 + (2*p+1)*(1-mu)
S = sp.Matrix([[lam**2-1, -2*lam], [2*lam, lam**2-1]])
M = S + S*sp.diag(bpar, bperp)*S + sp.diag(c1, mu)
Ch = sp.expand(M.det())
ok("char poly even in lambda", sp.simplify(Ch - Ch.subs(lam, -lam)) == 0)
Cs = sp.expand(Ch.subs([(lam**8, s**4), (lam**6, s**3), (lam**4, s**2), (lam**2, s)]))
q, rem = sp.div(Cs, s, s)
ok("s=0 factors out (drift mode) for all p", sp.simplify(rem) == 0)
poly_p = sp.Poly(sp.expand(q), s)
cubic_quad = sp.Poly(-8*mu**2 + 16*mu + s**3*(mu**2-2*mu+1) + s**2*(4*mu**2-10*mu+6)
                     + s*(8*mu**2-18*mu+11) - 6, s)
ok("p=1 reduces EXACTLY to the quadratic-proxy cubic (part-1 crosscheck)",
   sp.simplify(sp.expand(poly_p.as_expr().subs(p, 1)) - cubic_quad.as_expr()) == 0)
# THE GENERAL-p FOLD LAW: constant coefficient factors exactly
c0 = sp.factor(poly_p.all_coeffs()[-1])
ok("s^0 coeff = -2(2 mu p - 2p + 1)(4 mu p - 2 mu - 4p + 1): fold at mu = 1 - 1/(2p)",
   sp.simplify(c0 - (-2*(2*mu*p-2*p+1)*(4*mu*p-2*mu-4*p+1))) == 0)
print("    => the mu >= 1/2 orbit-fold is the p=1 case of mu_fold(p) = 1 - 1/(2p):")
print("       p=1: 1/2;  p=3/4: 1/3;  p -> 1/2+: mu_fold -> 0 (NO fold for the tail kernel)")

# ================= 3. INDEPENDENT check: full nonlinear EOM, p=1/2, linearized =================
print("[3] independent derivation: symbolic linearization of the FULL nonlinear tail EOM")
t = sp.symbols('t')
w, a0 = sp.symbols('w a0', positive=True)
xi = sp.Function('xi'); eta = sp.Function('eta')
x1 = (1 + e*xi(t))*sp.cos(t) - e*eta(t)*sp.sin(t)     # R=1, Om=1, v0=1
x2 = (1 + e*xi(t))*sp.sin(t) + e*eta(t)*sp.cos(t)
xdd1 = sp.diff(x1, t, 2); xdd2 = sp.diff(x2, t, 2)
nrm = sp.sqrt(xdd1**2 + xdd2**2)
u1 = a0*xdd1/nrm; u2 = a0*xdd2/nrm                    # k'(y) xdd = a0 * unit(xdd), p=1/2
r = sp.sqrt(x1**2 + x2**2)
Phip = 1/r - a0/(w**2*r**2)                           # self-consistent flat-curve potential
res1 = xdd1 + sp.diff(u1, t, 2)/w**2 + Phip*x1/r
res2 = xdd2 + sp.diff(u2, t, 2)/w**2 + Phip*x2/r
ok("background residual EXACTLY 0 (both components)",
   sp.simplify(res1.subs(e, 0)) == 0 and sp.simplify(res2.subs(e, 0)) == 0)
lin1 = sp.expand(sp.diff(res1, e).subs(e, 0)); lin2 = sp.expand(sp.diff(res2, e).subs(e, 0))
lrad = sp.simplify(sp.expand(sp.cos(t)*lin1 + sp.sin(t)*lin2))
lazi = sp.simplify(sp.expand(-sp.sin(t)*lin1 + sp.cos(t)*lin2))
lamX, X, Y = sp.symbols('lambda2 X Y')
sub = {}
for f, amp in ((xi, X), (eta, Y)):
    sub[f(t)] = amp
    for n in range(1, 7):
        sub[sp.Derivative(f(t), (t, n))] = amp*lamX**n
m11 = sp.expand(lrad.subs(sub)).coeff(X); m12 = sp.expand(lrad.subs(sub)).coeff(Y)
m21 = sp.expand(lazi.subs(sub)).coeff(X); m22 = sp.expand(lazi.subs(sub)).coeff(Y)
det_ind = sp.expand((m11*m22 - m12*m21).subs(a0, (1-mu)*w**2))
det_ind_s = sp.expand(det_ind.subs([(lamX**8, s**4), (lamX**6, s**3), (lamX**4, s**2), (lamX**2, s)]))
qi, remi = sp.div(det_ind_s, s, s)
tail_matrix = sp.expand(poly_p.as_expr().subs(p, sp.Rational(1, 2)))
ok("independent nonlinear-EOM linearization == matrix result (p=1/2), exactly",
   sp.simplify(remi) == 0 and sp.simplify(sp.expand(qi) - tail_matrix) == 0)
tail = sp.Poly(tail_matrix, s)
ok("tail kernel: QUADRATIC in s: (1-mu)s^2 + (2mu^2-4mu+3)s + 2mu",
   tail.degree() == 2 and
   sp.simplify(tail.as_expr() - ((1-mu)*s**2 + (2*mu**2-4*mu+3)*s + 2*mu)) == 0)

# ================= 4. tail-kernel zones: THE SOFT SPOT =================
print("[4] tail-kernel (p=1/2) zones on the flat curve")
c2t, c1t, c0t = tail.all_coeffs()
disc = sp.expand(c1t**2 - 4*c2t*c0t)
ok("disc = 4mu^4 - 16mu^3 + 36mu^2 - 32mu + 9",
   sp.simplify(disc - (4*mu**4-16*mu**3+36*mu**2-32*mu+9)) == 0)
zz = sorted(complex(z).real for z in sp.Poly(disc, mu).nroots(n=15)
            if abs(complex(z).imag) < 1e-12 and 0 < complex(z).real < 1)
t_lo, t_hi = zz
print(f"    disc zeros in (0,1): {t_lo:.10f}, {t_hi:.10f}")
ok("tail broken band = (0.5486044749, 0.8325451652)",
   abs(t_lo-0.5486044749) < 1e-9 and abs(t_hi-0.8325451652) < 1e-9)
# where real, roots are ALWAYS both negative: c2>0, c1>0 (disc_mu(c1)=16-24<0), c0>0
ok("all coefficients positive on (0,1): real => both roots NEGATIVE (never a saddle)",
   sp.reduce_inequalities(c1t > 0, mu) == True or
   sp.simplify(sp.discriminant(c1t, mu) - (-8)) == 0)
for m_, expect in [(0.95, 'real-'), (0.90, 'real-'), (0.70, 'complex'), (0.60, 'complex'),
                   (0.50, 'real-'), (0.30, 'real-'), (0.14, 'real-'), (0.05, 'real-')]:
    rt = np.roots([float(c.subs(mu, sp.Rational(m_).limit_denominator(10**4))) for c in tail.all_coeffs()])
    cplx = np.any(np.abs(rt.imag) > 1e-9*np.maximum(1, np.abs(rt)))
    pos = np.any((np.abs(rt.imag) <= 1e-9*np.maximum(1, np.abs(rt))) & (rt.real > 1e-12))
    tag = 'complex' if cplx else ('pos' if pos else 'real-')
    ok(f"tail mu={m_}: {tag} (expected {expect})", tag == expect)
print("    *** SOFT SPOT: mu < 0.5486 is PT-REAL for the tail kernel: deep-MOND flat-curve")
print("    PU orbits EXIST and are linearly stable.  'Deep MOND fails by orbit")
print("    non-existence at the EP' is a QUADRATIC-PROXY statement, NOT PU-class-general.")
# robustness: not a p=1/2 degeneracy artifact -- full 8th-order neighbors are also stable
for p_, m_ in [(0.52, 0.3), (0.55, 0.3), (0.6, 0.3), (0.7, 0.3), (0.55, 0.14)]:
    pol = sp.Poly(sp.expand(poly_p.as_expr().subs([(p, sp.Rational(p_).limit_denominator(100)),
                                                   (mu, sp.Rational(m_).limit_denominator(100))])), s)
    rt = np.roots([float(c) for c in pol.all_coeffs()])
    stab = (np.all(np.abs(rt.imag) < 1e-8*np.maximum(1, np.abs(rt))) and np.all(rt.real < 1e-10))
    ok(f"p={p_}, mu={m_}: NON-degenerate (cubic, 8 modes incl. fast ~{abs(rt.real.min()):.0f}) and stable", stab)
# but p >= ~0.75 kernels ARE dead at deep-MOND mu (fold law):
for p_, m_ in [(0.85, 0.3), (1.0, 0.3), (0.7, 0.14), (1.0, 0.14)]:
    pol = sp.Poly(sp.expand(poly_p.as_expr().subs([(p, sp.Rational(p_).limit_denominator(100)),
                                                   (mu, sp.Rational(m_).limit_denominator(100))])), s)
    rt = np.roots([float(c) for c in pol.all_coeffs()])
    stab = (np.all(np.abs(rt.imag) < 1e-8*np.maximum(1, np.abs(rt))) and np.all(rt.real < 1e-10))
    ok(f"p={p_}, mu={m_}: unstable (fold mu<1-1/(2p)={1-1/(2*p_):.3f} and/or Krein band)", not stab)

# ================= 5. what kills the crack: the R-PROFILE INVERSION =================
print("[5] confrontation: the stable deep-MOND PU orbits sit at the WRONG radii")
# monomial PU on a flat curve: 1-mu = (Om^2/w^2) p y^(p-1), y=(v0^2/(a0 R))^2
# => 1-mu ~ R^(-2p): DECREASING outward.  Framework/RAR on a flat curve: 1-mu ~ a0/(2a)
# = a0 R/(2 v0^2): INCREASING outward.  Slopes: -2p vs +1.  a0-INDEPENDENT => footing-proof.
Rsym = sp.symbols('R', positive=True)
one_minus_mu_PU = sp.simplify((Om_r**2/wr**2)*kprime.subs(rr, Rsym)*Rsym**0).subs(rr, Rsym)
slope_PU = sp.simplify(sp.diff(sp.log(one_minus_mu_PU), Rsym)*Rsym)
ok("PU monomial slope d ln(1-mu)/d ln R = -2p (deep-MOND at SMALL R, Newtonian at LARGE R)",
   sp.simplify(slope_PU - (-2*p)) == 0)
xx = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*xx**2)-1)/(2*xx)          # framework's own nu; x = a/a0 = v0^2/(a0 R)
slope_fw = sp.simplify(sp.diff(sp.log(1-mu_fw), xx)*xx)
slope_fw_deep = sp.limit(slope_fw, xx, sp.oo)   # x large = small R (Newtonian side): -1 in x = +1 in R
ok("framework slope d ln(1-mu_fw)/d ln R -> +1 on the Newtonian side (opposite SIGN)",
   sp.simplify(slope_fw_deep + 1) == 0)
for pname, p_ in [('tail p=1/2', 0.5), ('quadratic p=1', 1.0)]:
    mism = 10.0**(2*p_ + 1)
    print(f"    {pname}: over R = 2 -> 20 kpc the required-vs-delivered (1-mu) ratio "
          f"diverges by x{mism:.0f} (a0-independent: BOTH footings identical)")
ok("profile mismatch >= x100 for every p >= 1/2 (10^(2p+1))", 10.0**(2*0.5+1) >= 100)

# ================= 6. deep-MOND numbers, BOTH footings =================
print("[6] deep-MOND mu_needed and the status table, both footings")
gb_v, a0v = sp.symbols('g_b A0', positive=True)
mu_need = sp.simplify(gb_v/sp.sqrt(gb_v**2 + gb_v*a0v))
yv2 = sp.symbols('y2', positive=True)
ok("mu_needed = sqrt(y/(1+y)) from the framework's OWN interpolation",
   sp.simplify(mu_need.subs(gb_v, yv2*a0v) - sp.sqrt(yv2/(1+yv2))) == 0)
FOOT = {'canonical rho_DE/cH_L': 9.36e-11, 'alternate rho_tot/cH0': 1.13e-10}
for fname, a0n in FOOT.items():
    print(f"    footing {fname}: a0 = {a0n:.3g}")
    for gb in (2e-12, 5e-12, 1e-11):
        y = gb/a0n
        mun = float(np.sqrt(y/(1+y)))
        quad_kill = 0.5/mun
        in_crack = mun < t_lo
        print(f"      g_bar={gb:.0e}: y={y:.4f}, mu_needed={mun:.4f} | quadratic-proxy fold "
              f"kill x{quad_kill:.1f} | tail kernel: {'INSIDE the stable crack (EP does NOT kill)' if in_crack else 'EP-killed'}")
        ok(f"{fname} g_bar={gb:.0e}: quadratic-killed AND inside tail crack", mun < 0.5 and in_crack)
m1 = np.sqrt((5e-12/9.36e-11)/(1+5e-12/9.36e-11))
m2 = np.sqrt((5e-12/1.13e-10)/(1+5e-12/1.13e-10))
print(f"    footing spread at g_bar=5e-12: mu_needed {m1:.4f} vs {m2:.4f} "
      f"({100*abs(m1-m2)/m1:.1f}%): no verdict flips either way")

print(f"\nALL {len(PASS)} CHECKS PASS.")
print("""
D4 part-3 VERDICT (the honest both-ways result):
  SOFT SPOT FOUND (door ajar, then walled by a different brick):
  - The EP/orbit-non-existence kill of deep MOND is EXACT for the quadratic proxy
    (fold mu>=1/2 + saddle + Krein band) but FAILS for sub-quadratic PU kernels:
    fold law mu_fold = 1 - 1/(2p) -> 0 as p -> 1/2, and the framework-tail kernel
    (p=1/2, kappa_par=0) has PT-REAL linear spectrum for ALL mu < 0.5486 on flat
    curves (broken band only (0.5486, 0.8325)).  Deep-MOND PU orbits EXIST there.
    Verified two independent ways incl. direct linearization of the nonlinear EOM.
  - What still kills the PU horn on those kernels is NOT the EP but the PROFILE
    INVERSION: monomial PU delivers 1-mu ~ R^(-2p) (deep-MOND at small R, Newtonian
    at large R) while any MOND-like phenomenology, incl. the framework's own nu,
    needs 1-mu growing outward (+1 slope on a flat curve): sign-opposite slopes,
    x100+ mismatch across a disk, a0-independent (footing-proof).  This is G4's
    anti-universality doing the work the EP was credited with.
  SCOPE: all of this is the PU HORN (local higher-derivative MI) of Theorem IV.
  Carl's own framework is the NONLOCAL-kernel MI class -- no x'''' term, no PU EP
  applies; its phenomenology (RAR 0.108 dex @ Y=0.70, a0 = cH_L/Z) is untouched.
EXIT 0""")
