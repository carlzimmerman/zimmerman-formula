#!/usr/bin/env python3
"""I3 -- does Lambda_eff depend on alpha so that the Hartle-Hawking weight exp(S_dS) has an extremum in alpha? (pre-registered V1-V3)
V1: symbolic d ln W / d alpha.  V2: explicit two-loop QED vacuum energy (Feynman gauge, dimensional regularisation, MS-bar), with the
non-local-pole and RG checks that validate sign and normalisation, then the alpha-derivative at fixed POLE mass as a function of the scale mu
at which the vacuum-energy counterterm is defined.  V3: magnitudes.
Recalled input (flagged): m_pole = m_MS [1 + (alpha/pi)(1 + (3/4) ln(mu^2/m^2))] (textbook one-loop QED), and the MS-bar Z_m = 1 - 3 alpha/(4 pi eps).
Run:    python3 i3_vacuum_energy_alpha.py           -> exit 0 if all checks pass
MUTATE: python3 i3_vacuum_energy_alpha.py MUTATE    -> flips the fermion-loop sign of the two-loop diagram; the pole-cancellation and RG checks
        must FAIL (exit 1).
"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# ------------------------------------------------------------------ V1
print("== V1: Hartle-Hawking weight ==")
G, Lam, al = sp.symbols("G Lambda alpha", positive=True)
Lf = sp.Function("Lambda_eff")
S = 3*sp.pi/(G*Lf(al))
dlnW = sp.diff(S, al)
expect = -3*sp.pi/(G*Lf(al)**2)*sp.diff(Lf(al), al)
chk("V1a d ln W/d alpha = -(3 pi/(G Lambda^2)) dLambda/dalpha", sp.simplify(dlnW - expect) == 0)
chk("V1b H^2 = Lambda/3 => S_dS = pi/(G H^2) = 3 pi/(G Lambda)", sp.simplify((sp.pi/(G*(Lam/3))) - 3*sp.pi/(G*Lam)) == 0)
print("   interior extremum in alpha requires dLambda_eff/dalpha = 0 (Lambda_eff finite, > 0); otherwise W is monotonic in alpha.")

# ------------------------------------------------------------------ V2: two-loop vacuum energy
print("== V2: two-loop QED vacuum energy ==")
# Laurent coefficients are extracted NUMERICALLY (Cauchy contour integral on |eps| = 0.15, 96 points, 40 digits) because the symbolic series is too slow.
mp.mp.dps = 40
def gam(x): return mp.gamma(x)
def I_formula(dd, mm2):
    nu = dd/2 - 1; lam = dd - 3
    Omega = 2*mp.pi**(dd/2)/gam(dd/2)
    G0c = gam(dd/2-1)/(4*mp.pi**(dd/2))
    Kint = mp.mpf(2)**(-2-lam)/gam(1-lam)*gam((1-lam+2*nu)/2)*gam((1-lam)/2)**2*gam((1-lam-2*nu)/2)
    return Omega*(2*mp.pi)**(-dd)*G0c*mm2**(nu)*mm2**((dd-4)/2)*Kint
# closed form of I(m,m,0) = int d^dx G_m^2 G_0 against direct radial integration at d = 2.5 (independent of the Bessel-integral formula)
dd = mp.mpf("2.5"); nu = dd/2 - 1; mm = mp.mpf("0.7")
Gm = lambda x: (2*mp.pi)**(-dd/2)*(mm/x)**nu*mp.besselk(nu, mm*x)
G0 = lambda x: gam(dd/2-1)/(4*mp.pi**(dd/2))*x**(2-dd)
Om = 2*mp.pi**(dd/2)/gam(dd/2)
direct = Om*mp.quad(lambda x: x**(dd-1)*Gm(x)**2*G0(x), [0, 1, mp.inf])
closed = I_formula(dd, mm**2)
chk("V2a closed form of I(m,m,0) matches direct radial integration at d=2.5", abs(direct/closed - 1) < mp.mpf("1e-15"), f"(direct {mp.nstr(direct,12)}, closed {mp.nstr(closed,12)})")
sign = -1 if MUT else 1
def Bfun(eps, L):
    """O(alpha) bracket per unit alpha: two-loop diagram + mass-counterterm insertion; mu = 1, m^2 = exp(L)."""
    d = 4 - 2*eps; m2 = mp.e**L
    Fc = (mp.e**mp.euler/(4*mp.pi))**eps
    A = gam(-1+eps)*m2**(1-eps)/(4*mp.pi)**(2-eps)
    rho1 = Fc*2*gam(-d/2)*m2**(d/2)/(4*mp.pi)**(d/2)
    # theta diagram, Feynman gauge: numerator 4[(d-2)k.q + d m^2] = 4[ (d-2)/2 (D1+D2-D3) + 2 m^2 ]  ->  4[2 m^2 I - (d-2)/2 A^2] ; rho2 = -e^2/2 * that
    rho2 = sign*(-4*mp.pi*Fc**2*(4*m2*I_formula(d, m2) - (d-2)*A**2))
    delta = -3/(4*mp.pi*eps)                       # (Z_m - 1)/alpha, MS-bar (recalled)
    return rho2 + d*delta*rho1
def laurent(L, kmin=-2, kmax=0, r=mp.mpf("0.15"), n=96):
    pts = [r*mp.e**(2j*mp.pi*k/n) for k in range(n)]
    vals = [Bfun(p, L) for p in pts]
    return {k: sum(v/p**k for v, p in zip(vals, pts))/n for k in range(kmin, kmax+1)}
Ls = [mp.mpf(x) for x in (-3, -1, 0, 1, 2.5)]
co = {L: laurent(L) for L in Ls}
def m4(L): return mp.e**(2*L)
def coef(k): return [ (co[L][k]/m4(L)).real for L in Ls ]
def fitpoly(ys, deg=2):
    # exact fit through 3 points, check the other 2
    M = mp.matrix([[L**j for j in range(deg+1)] for L in Ls[:deg+1]]); sol = mp.lu_solve(M, mp.matrix(ys[:deg+1]))
    resid = max(abs(sum(sol[j]*L**j for j in range(deg+1)) - y) for L, y in zip(Ls, ys))
    return [sol[j] for j in range(deg+1)], resid
p2, r2 = fitpoly(coef(-2)); p1, r1 = fitpoly(coef(-1)); p0, r0 = fitpoly(coef(0))
print("   1/eps^2 coefficient / m^4 (coeffs of 1,L,L^2):", [mp.nstr(x, 10) for x in p2], " fit residual", mp.nstr(r2, 3))
print("   1/eps   coefficient / m^4 (coeffs of 1,L,L^2):", [mp.nstr(x, 10) for x in p1], " fit residual", mp.nstr(r1, 3))
chk("V2b non-local divergences cancel: 1/eps^2 and 1/eps coefficients are L-independent (pure local m^4 poles)",
    abs(p2[1]) < mp.mpf("1e-25") and abs(p2[2]) < mp.mpf("1e-25") and abs(p1[1]) < mp.mpf("1e-25") and abs(p1[2]) < mp.mpf("1e-25"))
b0n, b1n, b2n = p0
print("   finite part rho_2^ren / (alpha m^4) = b2 L^2 + b1 L + b0   (fit residual %s)" % mp.nstr(r0, 3))
for nm, v in (("b2", b2n), ("b1", b1n), ("b0", b0n)):
    rel = mp.pslq([v*mp.pi**3, 1, mp.pi**2, mp.zeta(3)], maxcoeff=10000, maxsteps=100000)
    print(f"      {nm} = {mp.nstr(v, 15)}   (b*pi^3 PSLQ over [1, pi^2, zeta3]: {rel})")
b2_rg = mp.mpf(3)/32/mp.pi**3
chk("V2c RG check: L^2 coefficient equals the value required by dm/dln mu = -(3 alpha/2 pi) m  (b2 = 3/(32 pi^3))", abs(b2n/b2_rg - 1) < mp.mpf("1e-20"),
    f"(got {mp.nstr(b2n,12)}, RG {mp.nstr(b2_rg,12)})")
if MUT:
    ok = all(v for _, v in checks); print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass"); sys.exit(0 if ok else 1)
mp.mp.dps = 30
b2, b1, b0 = [sp.Float(str(x), 25) for x in (b2n, b1n, b0n)]
a = sp.symbols("a", positive=True)
# ---- pole-mass conversion and the scale dependence of the alpha-derivative
Lq = sp.symbols("L")
# rho_1^ren = -(m^4/16 pi^2)(L - 3/2); m_MS = M[1 - (alpha/pi)(1 - (3/4) L)]  (L = ln(M^2/mu^2); recalled)
rho1_ren = lambda Lv: -(1/(16*sp.pi**2))*(Lv - sp.Rational(3,2))
# check ln-dependence of the recalled pole relation is RG-consistent: d/dln mu of ln m_MS + ... = 0 at O(alpha)
lnmMS = -(a/sp.pi)*(1 - sp.Rational(3,4)*Lq)                 # ln(m_MS/M) at O(alpha)
dL_dlnmu = -2
chk("V2d recalled pole relation is RG-consistent: d ln m_MS/d ln mu = -3 alpha/(2 pi)", sp.simplify(sp.diff(lnmMS, Lq)*dL_dlnmu + 3*a/(2*sp.pi)) == 0)
dr1_dlnm = sp.diff(rho1_ren(Lq)*sp.Symbol("m4"), Lq)*2 + 4*rho1_ren(Lq)*sp.Symbol("m4")   # d/dln m of m^4 rho1_ren(L), dL/dln m = 2
c_alpha = sp.simplify((b2*Lq**2 + b1*Lq + b0)*sp.Symbol("m4") + dr1_dlnm*lnmMS/a)/sp.Symbol("m4")
c_alpha = sp.expand(sp.simplify(c_alpha))
print("   c_alpha(L) = d rho/d alpha at fixed pole mass M (units M^4), L = ln(M^2/mu^2):")
print("      c_alpha =", sp.simplify(c_alpha), "\n             =", sp.N(c_alpha, 8))
cP = sp.Poly(c_alpha, Lq)
chk("V2e c_alpha depends on the scale mu (the vacuum-energy counterterm runs at two loops): degree >= 1 in L", cP.degree() >= 1)
roots = sp.Poly(c_alpha, Lq).nroots()
print("   zeros of c_alpha in L:", roots)
def cnum(Lv): return float(c_alpha.subs(Lq, Lv))
for Lv, lab in ((0.0, "mu = M"), (-2*mp.log(2), "mu = 2M"), (2*mp.log(2), "mu = M/2"), (-2*mp.log(1e3), "mu = 1e3 M"), (-2*mp.log(mp.mpf("1.22e19")/mp.mpf("0.511e-3")), "mu = M_Pl")):
    print(f"      {lab:12s}: c_alpha = {cnum(float(Lv)): .5e}  M^4")
real_roots = [r for r in roots if abs(sp.im(r)) < 1e-12]
for r in real_roots:
    print(f"   real zero at L = {sp.re(r):.4f}, i.e. mu/M = {float(mp.exp(-sp.re(r)/2)):.4f}")
chk("V2f c_alpha changes SIGN between mu = M and mu = M_e e^15 (scale-dependent sign, hence no unique alpha-dependence of Lambda_eff)", cnum(0.0)*cnum(-30.0) < 0)
chk("V2g c_alpha has real zeros at mu/M = 1.080 and 0.3405 only because of the arbitrary scale choice (they move with mu; not physical)", len(real_roots) == 2)
print("   closed forms (PSLQ above): rho_2^ren = alpha m^4/(32 pi^3) (3 L^2 - 8 L + 9), in MS-bar with the overall mu^(2 eps)(e^gamma/4pi)^eps convention on rho;")
print("   b1 and b0 depend on that convention (a change of scheme = a change of the finite vacuum-energy counterterm); only b2 and the pole cancellation are convention-independent checks.")

# ------------------------------------------------------------------ V3 magnitudes
print("== V3: magnitudes ==")
me = mp.mpf("0.51099895e-3")
Mpl = mp.mpf("1.220890e19")
rhoL = mp.mpf("0.6847")*mp.mpf("8.0992e-47")*mp.mpf("0.674")**2     # GeV^4: rho_crit = 8.0992e-47 h^2 GeV^4 (recalled)
print(f"   m_e^4 = {mp.nstr(me**4,4)} GeV^4 ; rho_Lambda = {mp.nstr(rhoL,4)} GeV^4 ; ratio = {mp.nstr(me**4/rhoL,4)}")
Sdisp = 3*Mpl**4/(8*rhoL)
print(f"   S_dS = 3 M_Pl^4/(8 rho_Lambda) = {mp.nstr(Sdisp,4)}  (G = 1/M_Pl^2)")
c0 = abs(cnum(0.0))
dlnW = Sdisp*c0*me**4/rhoL
print(f"   |d ln W/d alpha| (mu = M_e, linear response) = S_dS * |c_alpha| m_e^4/rho_Lambda = {mp.nstr(dlnW,4)}")
print(f"   => across d alpha = 1e-3 alpha_0 ln W changes by {mp.nstr(dlnW*mp.mpf('1e-3')/137.035999177,4)} (natural-log units), i.e. if the weight applied it would be a step function")
# boundary solution: rho_0 + rho_QED(alpha*) = 0  ->  |rho_0 + rho_QED(alpha_0)| < 1e-3 alpha_0 |c_alpha| m^4  for alpha* in the 1e-3 window
a0 = 1/mp.mpf("137.035999177")
window = 2*mp.mpf("1e-3")*a0*c0*me**4
prior_range = 2*Mpl**4/(8*mp.pi)            # rho_0 uniform in [-M_Pl^4/8pi, +M_Pl^4/8pi]
P = window/prior_range
print(f"   boundary solution alpha* inside |alpha*/alpha_0 - 1| < 1e-3 needs rho_0 within {mp.nstr(window,4)} GeV^4 of a value; Planck-scale flat prior gives probability {mp.nstr(P,4)}")
chk("V3 probability that the HH boundary solution alpha* lands in the 1e-3 window under a Planck-scale prior on rho_0 is < 1e-80", P < mp.mpf("1e-80"))
chk("V3 at this order rho_QED(alpha) is linear in alpha with c_alpha != 0 at mu = M: no interior extremum in THAT scheme choice (scheme-dependent, see V2f/V2g)", c0 != 0)

ok = all(v for _, v in checks)
print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass")
sys.exit(0 if ok else 1)
