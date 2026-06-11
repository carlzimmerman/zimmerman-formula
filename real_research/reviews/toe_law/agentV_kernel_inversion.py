#!/usr/bin/env python3
"""
agentV — kernel inversion: machine verification (incremental-output build).
Blocks:
  [A] exact pullback / slot-gradient / transform identities (sympy + mpmath)
  [B] route equivalence: s-integral vs u-integral vs by-parts probability form
  [C] the central asymptotics: all-(inverse-)moments-zero class; forward transform
      exponent fits for THREE members (p=-3/2 sin; second zeta; exact-target p=-9/8)
  [D] deep-MOND analyticity obstruction (slope 1.000 vs required 0.25)
  [E] legality: KL endpoint positivity; Tauberian sign-lock; LP cost-of-flatness
  [F] amplitude + zeta numbers (both footings, both a0 conventions; raw)
Output: agentV_kernel_inversion.out (written INCREMENTALLY, line by line)
"""
import sympy as sp
import mpmath as mp
import numpy as np
import os, time

OUTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentV_kernel_inversion.out")
_f = open(OUTPATH, "w")
T0 = time.time()
def P(s=""):
    _f.write(str(s) + "\n"); _f.flush()
    print(s, flush=True)

P("=" * 78)
P("agentV kernel inversion — machine verification run (incremental)")
P("=" * 78)

# ---------------------------------------------------------------- [A] identities
P("\n[A] EXACT IDENTITIES (sympy)")
s_, a_, H_, tau_ = sp.symbols('s a H tau', positive=True)
kap_ = sp.sqrt(a_**2 + H_**2)
beta_ = H_**2 / kap_**2

Z1 = (H_**2 * sp.cosh(kap_*s_) + a_**2) / kap_**2
Z2 = 1 + 2*beta_*sp.sinh(kap_*s_/2)**2
P("[A1] Z(s) two forms equal: %s" % (sp.expand_trig(Z1 - Z2).rewrite(sp.exp).simplify() == 0))
u_expr = Z2 - 1
t_expr = 2*beta_
dZds = sp.diff(Z2, s_)
jac_claim_sq = kap_**2 * u_expr*(u_expr + t_expr)
P("[A1] (dZ/ds)^2 = kappa^2 u(u+t): %s" % (sp.expand_trig(dZds**2 - jac_claim_sq).rewrite(sp.exp).simplify() == 0))

# A2: embedding + slot gradient: e.grad1 Z = a*(Z-1)
M5 = sp.diag(-1, 1, 1, 1, 1)
X = sp.Matrix([sp.sinh(kap_*tau_)/kap_, sp.cosh(kap_*tau_)/kap_, a_/(H_*kap_), 0, 0])
Xp = X.subs(tau_, tau_ - s_)
dot = lambda A, B: (A.T*M5*B)[0, 0]
chk = lambda e: (sp.expand_trig(sp.expand(e)).rewrite(sp.exp).simplify() == 0)
P("[A2] X.X = 1/H^2: %s" % chk(dot(X, X) - 1/H_**2))
u4 = sp.diff(X, tau_)
P("[A2] u.u = -1: %s" % chk(dot(u4, u4) + 1))
udot = sp.diff(u4, tau_)
e_ = (udot - H_**2*X)/a_
P("[A2] e.e = 1, e.u = 0, e.X = 0: %s, %s, %s" % (chk(dot(e_, e_) - 1), chk(dot(e_, u4)), chk(dot(e_, X))))
Zfun = H_**2 * dot(X, Xp)
P("[A2] Z = H^2 X.X' reproduces A1 form: %s" % chk(Zfun - Z1))
lhs = H_**2 * dot(e_, Xp)          # = e.grad1 Z (tangential proj automatic: e.X = 0)
P("[A2] KEY (slot gradient): e.grad1 Z = a*(Z-1) exactly: %s -> e.grad1 W = a (Z-1) W'(Z) for every W" %
  chk(lhs - a_*(Zfun - 1)))
P("[A2] conformal corollary: W = C/(1-Z) => (Z-1)W' = -W => e.grad1 W = -aW (agentB [A2] recovered)")

# A4: probability weight normalization + by-parts kernel identity (substituted: u = t v)
v_ = sp.symbols('v', positive=True)
wnorm = sp.integrate(sp.Rational(1, 2)*v_**sp.Rational(-1, 2)*(1+v_)**sp.Rational(-3, 2), (v_, 0, sp.oo))
P("[A4] weight normalization (t/2)int u^-1/2 (u+t)^-3/2 du = %s (must be 1; u=tv substitution)" % wnorm)
u_, t_ = sp.symbols('u t', positive=True)
byparts = sp.simplify(sp.diff(sp.sqrt(u_)/sp.sqrt(u_+t_), u_) - (t_/2)*u_**sp.Rational(-1, 2)*(u_+t_)**sp.Rational(-3, 2))
P("[A4] d/du[sqrt(u/(u+t))] = (t/2)u^-1/2 (u+t)^-3/2: %s" % (byparts == 0))

# A5: Laplace representation of the kernel (u+t -> single variable q)
q_, tt = sp.symbols('q tt', positive=True)
lap = sp.integrate(tt**sp.Rational(-1, 2)*sp.exp(-q_*tt), (tt, 0, sp.oo))
P("[A5] int tau^-1/2 e^-q tau dtau = sqrt(pi/q): %s  (=> F = double-Laplace of rho; inversion = unique)" %
  (sp.simplify(lap - sp.sqrt(sp.pi)/sp.sqrt(q_)) == 0))
P("[A] block done (%.0fs)" % (time.time()-T0))

# ------------------------------------------------- [B] route equivalence (mpmath)
P("\n[B] ROUTE EQUIVALENCE (toy cut density sigma(1+u) = e^-u, mpmath dps=30)")
mp.mp.dps = 30
def routes(a, H):
    kap = mp.sqrt(a*a + H*H)
    t = 2*H*H/(kap*kap)
    sig = lambda u: mp.e**(-u)
    us = lambda s: 2*(H*H/(kap*kap))*mp.sinh(kap*s/2)**2
    # finite cutoff where u(s_cut) = 80 (tail of u e^-u beyond: ~1e-33, below comparison floor);
    # NEVER evaluate exp(-u) at doubly-huge u (mpmath argument-reduction blowup — the v1 hang)
    s_cut = (2/kap)*mp.asinh(mp.sqrt(80*kap*kap/(2*H*H)))
    Fs = kap*mp.quad(lambda s: us(s)*sig(us(s)), [0, float(s_cut)/3, float(s_cut)])
    Fu = mp.quad(lambda u: mp.sqrt(u)*sig(u)/mp.sqrt(u+t), [0, 1, 80])
    T = lambda u: -mp.e**(-u)                      # T(u) = -int_u^inf sigma; T' = sigma
    Fp = -(t/2)*mp.quad(lambda u: T(u)/(mp.sqrt(u)*(u+t)**mp.mpf('1.5')), [0, 1, 80])
    return Fs, Fu, Fp
for (a, H) in [(0.7, 1.0), (2.3, 0.4)]:
    Fs, Fu, Fp = routes(a, H)
    P("[B1] (a,H)=(%.1f,%.1f): s-route %.15e  u-route %.15e  rel.diff %.2e" %
      (a, H, float(Fs), float(Fu), abs(float((Fs-Fu)/Fu))))
    P("[B2]              by-parts probability route %.15e  rel.diff %.2e" %
      (float(Fp), abs(float((Fp-Fu)/Fu))))
P("[B] block done (%.0fs)" % (time.time()-T0))

# ------------------------------------------- [C] the central class + forward fit
P("\n[C] THE REQUIRED CLASS: all-inverse-moments-zero + forward exponent")

# C1: saddle composition (numeric verification of the algebra, mpmath complex)
mp.mp.dps = 30
c_num, tau_num, u_num = mp.mpf('1.37'), mp.mpf('17.3'), mp.mpf('0.0021')
R = (c_num/(4*tau_num))**(mp.mpf(4)/5)
tstar = R*mp.e**(4j*mp.pi/5)
phi_star = tstar*tau_num - c_num*tstar**(mp.mpf(-1)/4)
pred1 = 5*mp.mpf(4)**(mp.mpf(-4)/5)*c_num**(mp.mpf(4)/5)*tau_num**(mp.mpf(1)/5)*mp.e**(4j*mp.pi/5)
P("[C1] layer-1 saddle: |phi(t*) - 5*4^(-4/5) c^(4/5) tau^(1/5) e^(4i pi/5)| = %.2e ; |phi'(t*)| = %.2e" %
  (abs(phi_star - pred1), abs(tau_num + (c_num/4)*tstar**(mp.mpf(-5)/4))))
s0 = 5*mp.mpf(4)**(mp.mpf(-4)/5)*c_num**(mp.mpf(4)/5)*mp.e**(-1j*mp.pi/5)
taustar = (s0/(5*u_num))**(mp.mpf(5)/4)
psi_star = u_num*taustar - s0*taustar**(mp.mpf(1)/5)
pred2 = -c_num*mp.e**(-1j*mp.pi/4)*u_num**(mp.mpf(-1)/4)
P("[C1] layer-2 saddle: |psi(tau*) - (-c e^(-i pi/4) u^(-1/4))| = %.2e ; |psi'(tau*)| = %.2e" %
  (abs(psi_star - pred2), abs(u_num - (s0/5)*taustar**(mp.mpf(-4)/5))))
P("[C1] => the two layers COMPOSE to r0 = c e^(-i pi/4): zeta = xi = c/sqrt(2) (the -pi/4 diagonal), exactly")

# C2: closed-form vanishing of inverse moments
P("[C2] closed form: M_k(p,phi) prop. Gamma(m+1) cos(phi + pi(m+1)/4)/(zeta sqrt2)^(m+1), m = 4k-4p-3")
P("[C2]   p=-3/2, phi=pi/2 (sin member): m+1 = 4k+4 -> cos(pi/2 + pi(k+1)) = 0 for ALL k")
P("[C2]   p=-9/8, phi=-pi/8 (exact-target member): m+1 = 4k+5/2 -> cos(-pi/8 + 5pi/8 + k pi) = 0 for ALL k")
for k in range(4):
    mk = sp.integrate(sp.Symbol('w', positive=True)**(4*k+3)*sp.exp(-sp.Symbol('w', positive=True))
                      * sp.sin(sp.Symbol('w', positive=True)), (sp.Symbol('w', positive=True), 0, sp.oo))
    P("[C2] sympy: int_0^inf w^%d e^-w sin w dw = %s (k=%d, must be 0)" % (4*k+3, sp.nsimplify(mk), k))

# C3: numeric inverse moments + cancellation scale (scale = Gamma via |sin|<=1 envelope)
mp.mp.dps = 30
zeta = mp.mpf(1)
P("[C3] numeric inverse moments of rho* = u^-3/2 e^{-u^-1/4} sin(u^-1/4) (w = u^-1/4 form):")
for k in range(0, 7):
    Ik = mp.quad(lambda w: 4*w**(4*k+3)*mp.e**(-w)*mp.sin(w), [0, 5, 20, 60, mp.inf])
    scale = 4*mp.gamma(4*k+4)
    P("[C3] k=%d: M_k = %+.3e   envelope scale 4*Gamma(4k+4) = %.3e -> cancellation %.1e" %
      (k, float(Ik), float(scale), float(abs(Ik)/scale)))
# fractional moments for the exact-target member p=-9/8, phi=-pi/8
P("[C3] exact-target member p=-9/8, phi=-pi/8: m_k = 4k+3/2:")
for k in range(0, 4):
    Ik = mp.quad(lambda w: 4*w**(4*k+mp.mpf('1.5'))*mp.e**(-w)*mp.cos(w - mp.pi/8), [0, 5, 20, 60, mp.inf])
    scale = 4*mp.gamma(4*k+mp.mpf('2.5'))
    P("[C3] k=%d: M_k = %+.3e   envelope 4*Gamma = %.3e -> cancellation %.1e" %
      (k, float(Ik), float(scale), float(abs(Ik)/scale)))
P("[C3] block done (%.0fs)" % (time.time()-T0))

# C4: THE forward transforms
P("[C4] forward transform F(t) = int rho(u)(u+t)^-1/2 du, w = u^-1/4 substitution; dps=40")
mp.mp.dps = 40
def Ffwd(t, z, p, phi):
    # integrand: 4 w^(-4p-3) e^{-z w} cos(z w + phi) (1 + t w^4)^(-1/2)
    pw = -4*p - 3
    return 4*mp.quad(lambda w: w**pw*mp.e**(-z*w)*mp.cos(z*w + phi)/mp.sqrt(1 + t*w**4),
                     [0, 3/z, 12/z, 40/z, 120/z, mp.inf])
def fit_run(z, p, phi, label, kmax=12):
    ts = [mp.mpf(10)**(-mp.mpf(k)/2) for k in range(2, kmax+1)]   # t = 1e-1 .. 1e-6
    Fs = [Ffwd(t, z, p, phi) for t in ts]
    signs = sorted(set(int(mp.sign(F)) for F in Fs))
    Amat = np.array([[1.0, float(mp.log(t)), -float(t**(mp.mpf(-1)/4))] for t in ts])
    yv = np.array([float(mp.log(abs(F))) for F in Fs])
    coef, _, _, _ = np.linalg.lstsq(Amat, yv, rcond=None)
    lnA, q, cfit = coef
    resid = float(np.max(np.abs(Amat@coef - yv)))
    P("[C4] %s:" % label)
    P("[C4]   fitted c = %.6f vs predicted sqrt(2)*zeta = %.6f (ratio %.6f)" %
      (cfit, float(mp.sqrt(2)*z), cfit/float(mp.sqrt(2)*z)))
    P("[C4]   prefactor power q = %.4f (branch-point law predicts q = p + 5/8 = %.4f); lnA=%.3f; max resid %.1e" %
      (q, float(p) + 0.625, lnA, resid))
    P("[C4]   sign(F) constant: %s (signs=%s); F(t_min) = %.6e" % (len(signs) == 1, signs, float(Fs[-1])))
    locs = []
    for i in range(len(ts)-1):
        num = mp.log(abs(Fs[i+1])) - mp.log(abs(Fs[i]))
        den = -(ts[i+1]**(mp.mpf(-1)/4) - ts[i]**(mp.mpf(-1)/4))
        locs.append(float(num/den))
    P("[C4]   local exponent sequence (last 4): %s" % ", ".join("%.5f" % v for v in locs[-4:]))
    return cfit, q

fit_run(mp.mpf(1), mp.mpf('-1.5'), mp.pi/2, "canonical member p=-3/2, phi=pi/2 (sin), zeta=1")
P("[C4] (%.0fs)" % (time.time()-T0))
fit_run(mp.mpf('1.7'), mp.mpf('-1.5'), mp.pi/2, "universality: same member at zeta=1.7")
P("[C4] (%.0fs)" % (time.time()-T0))
fit_run(mp.mpf(1), mp.mpf('-1.125'), -mp.pi/8, "EXACT-TARGET member p=-9/8, phi=-pi/8 (q must be -1/2)")
P("[C4] block done (%.0fs)" % (time.time()-T0))

# ------------------------------------------------- [D] deep-MOND analyticity
P("\n[D] DEEP-MOND OBSTRUCTION: E_t[T] analytic at t=2 (slope 1 in eps = 2-t prop. a^2)")
mp.mp.dps = 30
def Eavg(t, T):
    return (t/2)*mp.quad(lambda u: T(u)/(mp.sqrt(u)*(u+t)**mp.mpf('1.5')), [0, 1, 10, mp.inf])
for name, T in [("e^-u", lambda u: mp.e**(-u)),
                ("(1+u)^-0.3 (light-field h-=0.3 class)", lambda u: (1+u)**mp.mpf('-0.3'))]:
    M2 = Eavg(mp.mpf(2), T)
    eps_list = [mp.mpf(10)**(-k) for k in range(1, 6)]
    Ds = [Eavg(2-e, T) - M2 for e in eps_list]
    slopes = [float(mp.log(abs(Ds[i+1]/Ds[i]))/mp.log(eps_list[i+1]/eps_list[i]))
              for i in range(len(Ds)-1)]
    P("[D] T = %s: slopes of [E(2-eps)-E(2)] vs eps: %s  (analytic; target needs 0.25)" %
      (name, ", ".join("%.5f" % s for s in slopes)))
P("[D] => m_ind analytic in a^2 at a=0 whenever the geodesic adiabatic response converges:")
P("    NO-KERNEL for mu ~ sqrt(a/a0) (or any non-integer power of a^2) at the deep-MOND endpoint.")
P("[D] block done (%.0fs)" % (time.time()-T0))

# ------------------------------------------------- [E] LEGALITY numerics
P("\n[E] LEGALITY")
# E1: (h+)_k (h-)_k = prod_{j<k}(x + j(j+3)), x = M_eff^2/H^2 - ... (nu^2 = 9/4 - x)
x_s = sp.symbols('x', positive=True)
nu_s = sp.sqrt(sp.Rational(9, 4) - x_s)
for k in range(1, 5):
    poch = sp.rf(sp.Rational(3, 2)+nu_s, k)*sp.rf(sp.Rational(3, 2)-nu_s, k)
    prod_claim = sp.prod([x_s + j*(j+3) for j in range(k)])
    P("[E1] (h+)_%d (h-)_%d = prod_(j<%d)(x + j(j+3)): %s  (POSITIVE for all x>0)" %
      (k, k, k, (sp.expand(poch - prod_claim).simplify() == 0)))
P("[E1] => every u-derivative of the mass-M cut at the cone = (M^2-2H^2) x POSITIVE number:")
P("    flatness tower == all polynomial moments of nu = (x-2) d rho vanish;")
P("    0 = int (x-2)^2 Q(x)^2 d rho for all polys Q => rho = delta at the conformal point (zero tail). ILLEGAL in class (i).")

# E2: Tauberian sign-lock (flat caricature): positive power-tail weight => sigma(u) = 1 - C sqrt(u) + O(u), C>0
mp.mp.dps = 25
jfun = lambda x: 2*mp.besselj(1, x)/x if x != 0 else mp.mpf(1)
CT = mp.quad(lambda x: (1 - jfun(x))/x**2, [mp.mpf('1e-12'), 4, 40, 400, mp.inf])
us = [mp.mpf(10)**(-k) for k in range(3, 8)]
rows = []
for u in us:
    y = mp.sqrt(u)
    s_val = y*mp.quad(lambda x: x**-2*jfun(x), [y, 4, 40, 400, mp.inf])
    rows.append((u, s_val))
Am = np.array([[1.0, float(mp.sqrt(u)), float(u)] for u, _ in rows])
yv = np.array([float(s) for _, s in rows])
coefE2 = np.linalg.lstsq(Am, yv, rcond=None)[0]
P("[E2] positive power-tail KL weight (flat caricature, w(M)=M^-4 on [1,inf)):")
P("[E2] sigma(u) fit = %.6f %+.6f sqrt(u) %+.4f u" % tuple(coefE2))
P("[E2] sqrt(u) coefficient %.6f vs sign-locked -C = %.6f (C = int x^-2 (1-j) dx > 0 since j<=1)" %
  (coefE2[1], float(-CT)))
P("[E2] => heavy-tail positive measures give SIGN-DEFINITE ALGEBRAIC lightcone terms, never exponential flatness. ILLEGAL in class (ii).")

# E3: LP cost-of-flatness
P("[E3] LP cost-of-flatness (positive measure, J flatness conditions + unit positive-part normalization):")
try:
    from scipy.optimize import linprog
    xs = np.linspace(0.05, 40.0, 500)
    nu_fac = xs - 2.0
    def cond_row(k):
        r = np.ones_like(xs)
        for j in range(k):
            r = r*(xs + j*(j+3))
        r = nu_fac*r
        return r/np.max(np.abs(r))
    norm_row = np.where(xs > 2.0, nu_fac, 0.0)
    for J in range(0, 11):
        A_eq = np.vstack([cond_row(k) for k in range(J+1)] + [norm_row])
        b_eq = np.array([0.0]*(J+1) + [1.0])
        res = linprog(c=np.ones_like(xs), A_eq=A_eq, b_eq=b_eq,
                      bounds=[(0, None)]*len(xs), method='highs')
        P("[E3] J=%2d  status=%d  min total mass = %s" %
          (J, res.status, ("%.4e" % res.fun) if res.status == 0 else "INFEASIBLE/failed"))
    P("[E3] (mass growth/infeasibility with J = the positive-measure cost of lightcone flatness diverging)")
except Exception as ex:
    P("[E3] scipy LP unavailable (%s) -- the theorem stands on the [E1] positivity proof; LP was an echo only." % ex)
P("[E] block done (%.0fs)" % (time.time()-T0))

# ------------------------------------------------- [F] raw numbers
P("\n[F] RAW NUMBERS (both footings / conventions, per the working rule)")
cc = 2.99792458e8
HL, H0 = 1.81e-18, 2.19e-18
for label, a0, H in [("framework a0=9.36e-11, H_Lambda", 9.36e-11, HL),
                     ("canonical a0=1.2e-10,  H_Lambda", 1.2e-10, HL),
                     ("framework a0, hostile H0 footing", 9.36e-11, H0)]:
    eta = a0/(cc*H)
    z = 2**(-0.25)/eta**0.5
    P("[F] %s: eta = a0/cH = %.5f ; zeta = 2^(-1/4) eta^(-1/2) = %.4f" % (label, eta, z))
P("[F] structural: ANY O(1) dimensionless zeta in this class gives a0 = cH/(sqrt(2) zeta^2) -- a0 prop. cH automatic.")
P("[F] amplitude (corollary 1): lambda^2 <Q^2> >= m/(2 H sup|T|): cosmologically large universal charge per mass;")
P("    m_eff(0)=0 saturates the N2 static-tachyon stability cap exactly at a=0.")
Zr = sp.sqrt(32*sp.pi/3)
ident = sp.simplify(2**sp.Rational(-1, 4)*sp.sqrt(Zr) - (16*sp.pi/3)**sp.Rational(1, 4))
P("[F] quarantined identity: 2^(-1/4) sqrt(Z) - (16pi/3)^(1/4) = %s  (zeta_framework = (16pi/3)^(1/4) = %.4f;" %
  (ident, float((16*sp.pi/3)**0.25)))
P("    a re-expression of the eta = 1/Z convention, NOT a derivation of Z).")

P("\nDONE in %.0fs." % (time.time()-T0))
_f.close()
