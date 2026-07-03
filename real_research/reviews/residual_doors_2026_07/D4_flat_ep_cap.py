#!/usr/bin/env python3
"""D4 (lane): THE FLAT-CURVE EP CLOSURE -- Theorem IV's named residual, done in full.

Fourth Horn residual (pt_gates_verify_2026-07.py [A3]): the flat-curve PT cap was
ESTIMATED mu >= (2+sqrt(2))/4 ~ 0.854 via the scalar epicyclic anchor kappa^2=2*mu*Omega^2
-- 'PLAUSIBLE only (Coriolis-coupled 8th-degree polynomial not done)'.  Here we do the
full radial-azimuthal linearization of the PU-modified equations around a circular orbit
in the self-consistent flat-rotation-curve potential, no scalar shortcut.

MODEL (quadratic PU proxy, k'=1 absorbed into w=w_eff):
    xddot_i + (1/w^2) x''''_i + dPhi/dx_i = 0        (preferred-frame PU modified inertia)
Circular orbit R, Omega:  mu := 1 - (Omega/w)^2,  Phi'(R) = mu*Omega^2*R  (exact, G4).
Flat curve v(R)=v0 => the self-consistent potential is Phi'(r) = v0^2/r - v0^4/(w^2 r^3).

METHOD: complex coordinate z=(R+zeta)e^{i Omega t}, zeta=xi+i*eta.  The linearized
operator is P(D)zeta with P(D)=(D+i*Om)^2 + eps*(D+i*Om)^4, plus force terms
Phi''*xi + i*mu*Om^2*eta.  Real/imag split -> 2x4th-order system -> degree-8 even
characteristic polynomial = s * cubic(s), s=lambda^2 (s=0 double root = azimuthal drift).
Unbroken PT <=> all 3 cubic roots real and negative.  EP <=> discriminant sign change.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

PASS = []
def ok(name, cond):
    assert cond, "FAIL: " + name
    PASS.append(name); print("  PASS:", name)

# ================= 1. SYMBOLIC DERIVATION (Omega=1 units) =================
print("[1] linearized 2x2 system and the reduced cubic (full Coriolis, no shortcut)")
lam, s, mu, eps, c1 = sp.symbols('lambda s mu epsilon c1', real=True)

# P(D) = (D+i)^2 + eps*(D+i)^4 split into even/odd parts acting on zeta=xi+i*eta:
D = sp.symbols('D')
P = (D + sp.I)**2 + eps*(D + sp.I)**4
A_op = sp.re(sp.expand(P).subs(D, lam)) if False else None
Pex = sp.expand(P)
A = sp.simplify(Pex.subs(sp.I, 0).subs(D, lam)) if False else None
# do it cleanly: collect even (real-coefficient) and odd (i-coefficient) parts
Pex = sp.expand((D + sp.I)**2 + eps*(D + sp.I)**4)
A_D = sp.simplify((Pex + Pex.subs(sp.I, -sp.I))/2).subs(D, lam)      # even part
B_D = sp.simplify((Pex - Pex.subs(sp.I, -sp.I))/(2*sp.I)).subs(D, lam)  # odd part
ok("A(l) = l^2-1+eps(l^4-6l^2+1)", sp.simplify(A_D - (lam**2-1+eps*(lam**4-6*lam**2+1))) == 0)
ok("B(l) = 2l+4*eps*l(l^2-1)", sp.simplify(B_D - (2*lam+4*eps*lam*(lam**2-1))) == 0)
# P(D)(xi+i eta) = (A xi - B eta) + i(B xi + A eta): equations
#   (A + Phi'') xi - B eta = 0 ;  B xi + (A + mu) eta = 0   [Phi'/R = mu Om^2, Om=1]
charpoly = sp.expand((A_D + c1)*(A_D + mu) + B_D**2)     # degree 8, even in lambda
ok("char poly even in lambda", sp.simplify(charpoly - charpoly.subs(lam, -lam)) == 0)
Cs = sp.expand(charpoly.subs(lam**2, s).subs(lam**4, s**2).subs(lam**6, s**3).subs(lam**8, s**4))
Cs = sp.expand((A_D**2).subs(lam, sp.sqrt(s))*0 + ((sp.sqrt(s)**2-1+eps*(s**2-6*s+1)+c1) *
      (s-1+eps*(s**2-6*s+1)+mu) + 4*s*(1+2*eps*(s-1))**2))
# self-consistent flat curve: Phi'(r)=v0^2/r - v0^4/(w^2 r^3); Phi''(R0) with Om0=1,v0=1:
r, w = sp.symbols('r w', positive=True)
Phi_p = 1/r - eps/r**3            # v0=1, 1/w^2 = eps
Phi_pp = sp.diff(Phi_p, r).subs(r, 1)
ok("flat-curve background: Phi'(1) = 1-eps = mu", sp.simplify(Phi_p.subs(r,1) - (1-eps)) == 0)
ok("flat-curve Phi'' = 2-3*mu  (with eps=1-mu)", sp.simplify(Phi_pp.subs(eps, 1-mu) - (2-3*mu)) == 0)
Cs_flat = sp.expand(Cs.subs([(c1, 2-3*mu), (eps, 1-mu)]))
q, rem = sp.div(Cs_flat, s, s)
ok("s=0 factors out exactly (azimuthal drift mode)", sp.simplify(rem) == 0)
cubic = sp.Poly(sp.expand(q), s)
print("    reduced cubic:", cubic.as_expr())
# Newtonian limit mu->1: cubic -> s+2 => kappa^2 = 2*Omega^2 (flat-curve epicyclic)
lim = sp.factor(cubic.as_expr().subs(mu, 1))
ok("mu->1 limit: roots s=-2 (kappa=sqrt(2)Om) -- correct flat epicyclic", sp.simplify(lim - (s+2)*(s+4)**0) != None and sp.solve(sp.Eq(lim,0), s) == [-2])

# ================= 2. EXACT EP LOCATION: cubic discriminant =================
print("[2] exact PT-breaking zones on the flat curve")
disc = sp.factor(sp.discriminant(cubic.as_expr(), s))
print("    disc =", disc)
Q = sp.Poly(664*mu**4 - 3036*mu**3 + 5086*mu**2 - 3681*mu + 971, mu)
ok("disc = -4(mu-1)^3 (2mu-1) Q(mu), Q=664mu^4-3036mu^3+5086mu^2-3681mu+971",
   sp.simplify(disc - (-4*(mu-1)**3*(2*mu-1)*Q.as_expr())) == 0)
rr = [complex(z) for z in Q.nroots(n=15)]
real_rr = sorted(z.real for z in rr if abs(z.imag) < 1e-12 and 0 < z.real < 1)
mu_lo, mu_hi = real_rr
print(f"    Q real zeros in (0,1): mu_lo = {mu_lo:.10f}, mu_hi = {mu_hi:.10f}")
ok("flat-curve EP band edges: 0.7579886 / 0.8947874",
   abs(mu_lo-0.7579885564) < 1e-8 and abs(mu_hi-0.8947873767) < 1e-8)

# classify all zones by direct root inspection (rational mu, exact division)
def zones(mu_val, alpha=None):
    m = sp.Rational(mu_val).limit_denominator(10**6)
    co = [float(cc) for cc in [c.subs(mu, m) for c in cubic.all_coeffs()]]
    rt = np.roots(co)
    cplx = np.any(np.abs(rt.imag) > 1e-7*np.maximum(1, np.abs(rt)))
    pos  = np.any((np.abs(rt.imag) <= 1e-7*np.maximum(1, np.abs(rt))) & (rt.real > 1e-9))
    return rt, cplx, pos
for m_, expect in [(0.97,'real-'), (0.92,'real-'), (0.85,'complex'), (0.77,'complex'),
                   (0.70,'real-'), (0.55,'real-'), (0.45,'complex+pos'), (0.20,'complex+pos')]:
    rt, cplx, pos = zones(m_)
    tag = '+'.join([t for t, f in (('complex', cplx), ('pos', pos)) if f]) or 'real-'
    ok(f"mu={m_}: spectrum {tag} (expected {expect})", tag == expect)
print("    ZONES (flat curve, quadratic PU): mu in (0.8948,1] UNBROKEN;")
print("    (0.7580,0.8948) PT-BROKEN (complex quartet); (0.5,0.7580) RE-ENTRANT real;")
print("    mu < 0.5: complex quartet AND a real POSITIVE root (radial saddle = the branch")
print("    fold seen dynamically) -- doubly unstable, strictly worse than the band.")

# predicted runaway rate inside the band at mu=0.85
rt85 = zones(0.85)[0]
lam85 = np.sqrt(rt85.astype(complex))
rate_pred = float(max(np.abs(lam85.real)))
print(f"    mu=0.85 predicted runaway rate: Re(lambda) = {rate_pred:.4f} * Omega "
      f"({rate_pred*2*np.pi:.2f} e-folds/orbit)")

# ================= 3. NUMERIC CROSS-CHECK: 8x8 companion eigenvalues =================
print("[3] 8x8 rotating-frame companion matrix vs cubic roots")
def companion(mu_val):
    e = 1.0 - mu_val; c1v = 2 - 3*mu_val
    M = np.zeros((8, 8))
    # state (xi, xi', xi'', xi''', eta, eta', eta'', eta''')
    for i in (0, 1, 2, 4, 5, 6):
        M[i, i+1] = 1.0
    # eps*xi'''' = -[(1-6e)xi'' + (e-1+c1)xi - 2eta' - 4e(eta'''-eta')]
    M[3, 2] = -(1-6*e)/e; M[3, 0] = -(e-1+c1v)/e; M[3, 5] = (2-4*e)/e; M[3, 7] = 4*e/e
    # eps*eta'''' = -[(1-6e)eta'' + (e-1+mu)eta + 2xi' + 4e(xi'''-xi')]
    M[7, 6] = -(1-6*e)/e; M[7, 4] = -(e-1+mu_val)/e; M[7, 1] = -(2-4*e)/e; M[7, 3] = -4*e/e
    return M
for m_ in (0.85, 0.65, 0.92):
    ev = np.linalg.eigvals(companion(m_))
    s_num = np.sort_complex(np.array(sorted(ev**2, key=lambda z: (round(z.real,6), round(z.imag,6)))))
    rt = np.sort_complex(np.roots([float(cc.subs(mu, sp.Rational(m_).limit_denominator(10**6))) for cc in cubic.all_coeffs()]))
    s_nz = np.array(sorted([z for z in s_num if abs(z) > 1e-8], key=lambda z: (z.real, z.imag)))[::2]
    match = all(min(abs(a-b) for b in rt) < 1e-6*max(1, abs(a)) for a in s_nz)
    ok(f"mu={m_}: companion eigenvalues^2 reproduce the cubic roots", match)

# ================= 4. FULL NONLINEAR ORBIT INTEGRATION (inertial frame) =================
print("[4] direct integration in the self-consistent flat-curve potential")
def integrate(mu_val, tmax, pert=1e-8):
    e = 1.0 - mu_val; w2 = 1.0/e
    def rhs(t, sv):
        x = sv[0:2]; v = sv[2:4]; a = sv[4:6]; j = sv[6:8]
        rn = np.hypot(x[0], x[1])
        g = -(1.0/rn - e/rn**3) * x/rn        # v0=1
        return np.concatenate([v, a, j, w2*(g - a)])
    s0 = np.array([1.0+pert, 0, 0, 1.0, -1.0, 0, 0, -1.0])
    sol = solve_ivp(rhs, [0, tmax], s0, rtol=1e-11, atol=1e-13, dense_output=True, max_step=0.05)
    return sol
# (a) in-band mu=0.85: runaway at the predicted rate
sol = integrate(0.85, 55.0)
tt = np.linspace(5, 48, 2000)
dev = np.abs(np.hypot(sol.sol(tt)[0], sol.sol(tt)[1]) - 1.0)
# envelope fit over windows
nw = 12; rates = []
tw = np.array_split(tt, nw); dw = np.array_split(dev, nw)
env_t = np.array([t_.mean() for t_ in tw]); env_d = np.array([d_.max() for d_ in dw])
rate_num = np.polyfit(env_t, np.log(env_d), 1)[0]
print(f"    mu=0.85: measured growth {rate_num:.4f}, predicted {rate_pred:.4f} Omega")
ok("in-band runaway rate matches EP prediction to <5%", abs(rate_num-rate_pred)/rate_pred < 0.05)
# (b) re-entrant mu=0.65: bounded over 50 orbits
sol2 = integrate(0.65, 50*2*np.pi)
tt2 = np.linspace(0, 50*2*np.pi, 8000)
dev2 = np.abs(np.hypot(sol2.sol(tt2)[0], sol2.sol(tt2)[1]) - 1.0)
amp_ratio = dev2.max()/1e-8
print(f"    mu=0.65 (re-entrant): max radial deviation / initial = {amp_ratio:.1f} over 50 orbits")
ok("re-entrant zone: bounded (no runaway) over 50 orbits", amp_ratio < 50)

print(f"\nALL {len(PASS)} CHECKS PASS.")
print("""
D4 VERDICT (quadratic PU proxy, flat curve, FULL Coriolis -- the named residual DONE):
  The crude scalar-anchor cap 0.854=(2+sqrt2)/4 was WRONG in both directions:
  - true PT-broken band = mu in (0.75799, 0.89479): upper edge HIGHER than 0.854 (broken
    zone starts earlier coming down the curve),
  - but a genuine RE-ENTRANT real-spectrum window mu in (0.5, 0.758) exists that the
    scalar shortcut missed (Krein collision is avoided there),
  - below mu = 1/2 a real positive root appears: radial SADDLE = the orbit-branch fold.
  Deep MOND (mu << 1/2) remains excluded on flat curves FOR THIS PROXY -- by the
  saddle/fold + complex quartet, not by the (0.758,0.895) band alone.
  CAVEAT -> see D4_tail_kernel_kill_margin.py: the quadratic proxy is NOT the whole PU
  class.  For sub-quadratic kernels (incl. the framework-tail k'=y^-1/2) the fold law is
  mu_fold = 1-1/(2p) -> 0 and the deep-MOND zone is PT-REAL: the EP kill is
  quadratic-proxy-specific; those kernels die by profile inversion instead.
EXIT 0""")
