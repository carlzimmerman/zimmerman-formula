"""
agentN2 — MEMORY LANGEVIN for NON-HUYGENS (tail) fields: structure of the
trajectory-dependent dissipation kernel, the acceleration-HISTORY force, the
frequency-domain effective inertia m_eff(Omega), and the high-frequency gate
that the solar-reflex kill (Door IVb, agentE) now demands.

CONTEXT. agentF closed the worldline-bath mechanism for F4 at ALL couplings for
the conformal (Huygens) field: the pulled-back commutator is (i/2pi)d'(s) for
every (a,H), so dissipation is trajectory-blind and the response is kappa-only.
The UNIQUE named bath-side escape: fields whose retarded Green function has a
TAIL (massive, or minimally coupled in dS) — there the dissipation kernel is a
MEMORY integral over the past worldline and CAN know a and H separately.
This script machine-verifies the structural claims of agentN2_memory_langevin.md.
Conditional on the non-Huygens gate; agent N1's verdict is NOT assumed.

PARTS
  A. Geometry: for a GENERIC bi-invariant W(Z) the Deser-Levin pullback is
     genuinely TWO-parameter (kappa-only fails; the conformal case is the unique
     exception), while the single-a force prefactor survives (e.gradW = a *
     [H^2(cosh ks - 1)/k^2] W'(Z)).  Memory times of dS tails (lambda_- kappa);
     flat-space chord identities; the helix (rotating-acceleration) projection
     identities that become the response filters.
  B. The dS4 minimally-coupled massless scalar's flat tail is REAL: the field
     commutator at timelike separation is the CONSTANT -i H^2/(4pi), position-
     independent inside the light cone (closed-form regulated mode integrals).
  C. Endpoint universality of the tail: V(0+) = -(1/8pi)[m^2 + (xi-1/6)R]
     (DeWitt-Schwinger v0): flat massive -m^2/8pi; dS minimal +H^2/4pi
     (matches B); conformal dS exactly 0 (the agentF/Huygens corner).
  D. The memory quantum Langevin equation: internal propagator with tail
     self-energy; stability (argument principle: no poles in the upper
     half-plane) for the flat-tail toy at weak-to-moderate memory coupling.
  E. The helix response filters and the GATE exponents (core verification):
       m_R(Om) = (1/Om^2) INT K(s)(1-cos Om s) ds   [in-phase inertia],
       m_T(Om) = (1/Om^2) INT K(s) sin(Om s) ds     [quadrature],
     on toy tail kernels: T1 flat theta(T-s) [the task's dS toy], T2 exp(-x s),
     T3 massive 2J1(ms)/(ms), T4 carrier-modulated.  Verified: adiabatic limit
     m_R(0) = INT K s^2/2 (LOCAL, analytic in Om^2 — the standard quasi-static
     outcome); high-frequency gate m_R -> M0/Om^2 (p = 2, UNIVERSAL for M0 != 0,
     sharp or smooth kernel); m_T -> K(0)/Om^3 (p = 3); the slowly-varying-a
     functional (moment expansion vs direct convolution) and its breakdown.
  F. The data confrontation: agentE's solar-reflex survival line vs the RAR
     flatness requirement -> the allowed knee window [~2e-14, ~2.5e-9] s^-1.
     The pure-dS tail (knee <= 3H/2) MISSES the window by ~3.9 decades and
     tilts the RAR by orders of magnitude: the task's 1/H-memory toy CANNOT
     serve.  Both footings (H_Lambda, H_0), both normalizations (a0, cH_Lambda).

CONVENTIONS. hbar = c = k_B = 1 in A-E; SI in F. K(s) normalized K(0) = K0 = 1
where applicable: the gate statements are RATIOS (sign- and amplitude-blind);
the sign/shape of the adiabatic tail response is N1-territory, NOT decided here.
"""

import sympy as sp
from mpmath import mp, mpf, mpc, pi as mpi, sin as msin, cos as mcos, exp as mexp
from mpmath import sqrt as msqrt, log as mlog, atan as matan, quad, inf, besselj, diff as mdiff

mp.dps = 20

print("=" * 78)
print("PART A: tails make the pullback TWO-parameter (kappa-only fails);")
print("        the single-a force prefactor survives; memory times; chords")
print("=" * 78)

a, H, tau, s = sp.symbols('a H tau s', positive=True)
k = sp.sqrt(a**2 + H**2)

def dot5(U, V):
    return sp.expand(-U[0]*V[0] + sum(U[i]*V[i] for i in range(1, 5)))

def Xv(t):
    return [sp.sinh(k*t)/k, sp.cosh(k*t)/k, a/(H*k), sp.Integer(0), sp.Integer(0)]

X   = Xv(tau)
Xp  = Xv(tau - s)
Xdd = [sp.diff(c, tau, 2) for c in X]
a_int = [sp.simplify(Xdd[i] - H**2*X[i]) for i in range(5)]
e   = [sp.simplify(c/a) for c in a_int]

# [A1] the slot-1 contraction (agentF [A4] re-run): e(tau).X(tau-s)
eXp = sp.simplify(sp.expand_trig(dot5(e, Xp)).rewrite(sp.exp))
geom = ((a/k**2)*(sp.cosh(k*s) - 1)).rewrite(sp.exp)
print("[A1] e.X' - (a/k^2)(cosh ks - 1) =", sp.simplify(eXp - geom))
print("     With Z = H^2 X.X' and grad_1 Z = H^2 X' (tangential proj.):")
print("     e.grad_1 W(Z) = W'(Z) * H^2 (e.X') = a * [H^2(cosh ks -1)/k^2] * W'(Z)")
print("     => the force vertex carries EXACTLY ONE factor of a on the whole")
print("        stationary family for ANY bi-invariant W(Z)  [tails included]:")
print("        the deep-MOND consistency F -> 0 as a -> 0 survives for tails.")

# [A2] Z itself is genuinely two-parameter at fixed kappa
kap, Hs = sp.symbols('kappa H', positive=True)
Zk = 1 + 2*(Hs**2/kap**2)*sp.sinh(kap*s/2)**2     # = (H^2 cosh ks + a^2)/k^2
Zemb = sp.simplify(Hs**2*((sp.cosh(kap*s) - (1 - kap**2/Hs**2*0))*0 + 0) + 0)  # placeholder no-op
Z_direct = sp.simplify(((Hs**2*sp.cosh(kap*s) + (kap**2 - Hs**2))/kap**2))
print("[A2] Z - [1 + 2(H/k)^2 sinh^2(ks/2)] =", sp.simplify(Z_direct - Zk))
dZdH = sp.simplify(sp.diff(Zk, Hs))
print("     dZ/dH at FIXED kappa =", dZdH, "  != 0:")
print("     => any NON-conformal W(Z) pulled back on the family knows (a,H)")
print("        SEPARATELY: the agentF kappa-only lemma fails exactly here.")
Wc = Hs**2/(8*sp.pi**2*(1 - Zk))
print("[A2] conformal exception: W_conf = H^2/(8pi^2(1-Z)) pulled back =",
      sp.simplify(Wc), "  [H cancels: kappa-only — the Huygens accident]")
WcpW = sp.simplify(sp.together(
    a*0 + sp.simplify((sp.cosh(kap*s) - 1)*(Hs**2/kap**2) *
                      sp.diff(Hs**2/(8*sp.pi**2*(1 - sp.Symbol('Zv'))), sp.Symbol('Zv'))
                      .subs(sp.Symbol('Zv'), Zk) + Wc)))
print("[A2] conformal check of the A1 identity: (coshks-1)(H/k)^2 W' + W =",
      sp.simplify(WcpW), "  [=0 <=> e.gradW = -aW, agentF's identity recovered]")

# [A3] memory times of dS tails on the worldline: W_nu(Z) ~ Z^{-lambda_-},
#      Z ~ (H^2/2k^2) e^{ks}: pullback decay rate lambda_- * kappa.
print("[A3] dS tail memory times: lambda_- = 3/2 - sqrt(9/4 - (m/H)^2);")
print("     pullback decay rate lambda_-*kappa; T_mem = 1/(lambda_- kappa).")
print("     m/H     lambda_-      m^2/3H^2     T_mem*H (kappa=H)")
for mh in [mpf('0.03'), mpf('0.1'), mpf('0.3'), mpf(1), mpf('1.45')]:
    lam = mpf('1.5') - msqrt(mpf('2.25') - mh**2)
    print(f"     {float(mh):5.2f}  {float(lam):11.6f}  {float(mh**2/3):11.6f}"
          f"   {float(1/lam):12.2f}")
print("     [small m: lambda_- -> m^2/3H^2 (Starobinsky-Yokoyama rate m^2/3H);")
print("      m -> 3H/2: T_mem -> (2/3)/H; principal series m > 3H/2: envelope")
print("      rate 3kappa/2, oscillation mu*kappa, mu = sqrt(m^2/H^2 - 9/4) -> m:")
print("      the kernel scale is the FIELD MASS once m >> H (flat-massive limit).")
print("      => the dS-tail knee is bounded by ~max(m, H-class rates).]")

# [A4] flat-space chords: Rindler (a-dependence explicit), helix (O(v^2))
av, sv = sp.symbols('a s', positive=True)
chordR = sp.simplify((sp.sinh(av*tau)/av - sp.sinh(av*(tau - sv))/av)**2 -
                     (sp.cosh(av*tau)/av - sp.cosh(av*(tau - sv))/av)**2)
print("[A4] Rindler chord^2 (t^2-x^2 sign: timelike>0):",
      sp.simplify(chordR - 4*sp.sinh(av*sv/2)**2/av**2), " [= (4/a^2)sinh^2(as/2):")
print("     the massive tail J1(m*chord)/chord on the worldline depends on a")
print("     EXPLICITLY — trajectory-dependent dissipation, as flagged by agentF]")
v, Om0s = sp.symbols('v Omega', positive=True)
# helix: coordinate time Dt = s/sqrt(1-v^2); chord^2 = Dt^2 - 4 rho^2 sin^2(Om Dt/2)
Dt = sv/sp.sqrt(1 - v**2)
chordH = Dt**2 - 4*(v/Om0s)**2*sp.sin(Om0s*Dt/2)**2
ser = sp.series(chordH, v, 0, 3).removeO()
corr = sp.simplify((ser - sv**2)/sv**2)
print("[A4] helix chord^2 = s^2 * [1 + v^2*(1 - sin^2(Om s/2)/(Om s/2)^2) + O(v^4)]")
print("     v^2 coefficient check:", sp.simplify(corr - v**2*(1 - sp.sin(Om0s*sv/2)**2/(Om0s*sv/2)**2)))
vsun = 12.45/2.99792458e8
print(f"     Sun's reflex helix: v = a/(Omega c) = 12.45 m/s -> v^2 = {vsun**2:.2e}:")
print("     the straight-chord (flat-comoving) tail kernel is exact to ~1.7e-15")
print("     on the solar worldline; galactic orbit v^2 ~ 6e-7: also negligible.")

# [A5] the helix projection identities (the source of the response filters)
rho, Omg, tt = sp.symbols('rho Omega t', positive=True)
rvec  = [rho*sp.cos(Omg*tt), rho*sp.sin(Omg*tt)]
rvecp = [rho*sp.cos(Omg*(tt - s)), rho*sp.sin(Omg*(tt - s))]
rhat  = [sp.cos(Omg*tt), sp.sin(Omg*tt)]
that  = [-sp.sin(Omg*tt), sp.cos(Omg*tt)]
proj_r = sp.simplify(sum(rhat[i]*(rvec[i] - rvecp[i]) for i in range(2)))
proj_t = sp.simplify(sum(that[i]*(rvec[i] - rvecp[i]) for i in range(2)))
print("[A5] rhat.(r(t)-r(t-s)) - rho(1-cos Om s) =",
      sp.simplify(proj_r - rho*(1 - sp.cos(Omg*s))))
print("     that.(r(t)-r(t-s)) - rho sin(Om s)   =",
      sp.simplify(proj_t - rho*sp.sin(Omg*s)))
print("     => for an acceleration vector rotating at Omega, the tail force")
print("        response per unit |a| is filtered by (1-cos Om s)/Om^2 (in-phase)")
print("        and sin(Om s)/Om^2 (quadrature): Omega enters EXACTLY as the")
print("        Fourier variable conjugate to memory time.  [rho = a/Omega^2]")

print()
print("=" * 78)
print("PART B: the dS4 minimal massless tail is REAL — commutator constant")
print("        -i H^2/4pi inside the cone (closed-form regulated mode integrals)")
print("=" * 78)
# C(x,x') = (i H^2/2pi^2)(1/r) * [ Deta*I2 - I1 - eta*eta'*I3 ],  with
# I2 = INT sin(kr)cos(k Deta)/k, I1 = INT sin(kr)sin(k Deta)/k^2,
# I3 = INT sin(kr)sin(k Deta),  all with regulator e^{-eps k}  (BD modes
# u_k = H(1+ik eta) e^{-ik eta}/sqrt(2k^3);  Im[u u'*] assembled by hand).
def I2_closed(r, d, eps):
    return (matan((r + d)/eps) + matan((r - d)/eps))/2

def Flog(t, c):
    # antiderivative of ln(t^2+c^2): t ln(t^2+c^2) - 2t + 2c atan(t/c)
    if c == 0:
        return t*mlog(t**2) - 2*t
    return t*mlog(t**2 + c**2) - 2*t + 2*c*matan(t/c)

def I1_closed(r, d, eps):
    # I1(eps) = 1/4 { pi(r+d) - pi|r-d| - [F(eps,r+d) - F(eps,|r-d|)] }
    cp, cm = r + d, abs(r - d)
    return (mpi*cp - mpi*cm - (Flog(eps, cp) - Flog(eps, cm)))/4

def I3_closed(r, d, eps):
    return (eps/(eps**2 + (d - r)**2) - eps/(eps**2 + (d + r)**2))/2

# numeric spot-verification of the three regulated closed forms (eps = 0.05):
epsv = mpf('0.05'); rv, dv = mpf('0.7'), mpf('1.0')
n2 = quad(lambda kk: mexp(-epsv*kk)*msin(rv*kk)*mcos(dv*kk)/kk, [0, 1, 10, 100, 400])
n1 = quad(lambda kk: mexp(-epsv*kk)*msin(rv*kk)*msin(dv*kk)/kk**2, [0, 1, 10, 100, 400])
n3 = quad(lambda kk: mexp(-epsv*kk)*msin(rv*kk)*msin(dv*kk), [0, 1, 10, 100, 400])
print("[B1] regulated Laplace integrals, closed vs numeric (r=0.7, Deta=1, eps=0.05):")
print(f"     I2: {float(I2_closed(rv,dv,epsv)):+.8f} vs {float(n2):+.8f}")
print(f"     I1: {float(I1_closed(rv,dv,epsv)):+.8f} vs {float(n1):+.8f}")
print(f"     I3: {float(I3_closed(rv,dv,epsv)):+.8f} vs {float(n3):+.8f}")

def C_tail_coeff(r, d, eta, etap, eps):
    """assembled (2pi^2/H^2)*r * [coefficient of i in C]; target -(pi/2) r /r = -(pi/2)
       i.e. we return [Deta*I2 - I1 - eta*etap*I3]/r ; constancy = -pi/2."""
    return (d*I2_closed(r, d, eps) - I1_closed(r, d, eps)
            - eta*etap*I3_closed(r, d, eps))/r

print("[B2] assembled commutator coefficient (2pi^2/(i H^2)) * C * r/r:")
print("     target = -pi/2 =", float(-mpi/2), " (=> C = -i H^2/4pi, CONSTANT)")
pts = [(mpf('0.3'), mpf(1), mpf('-0.2'), mpf('-1.2')),
       (mpf('0.7'), mpf(1), mpf('-0.2'), mpf('-1.2')),
       (mpf('0.7'), mpf(1), mpf('-1.0'), mpf('-2.0')),
       (mpf('0.5'), mpf('2.5'), mpf('-0.4'), mpf('-2.9')),
       (mpf('2.0'), mpf('2.5'), mpf('-3.0'), mpf('-5.5'))]
for (rv, dv, ev, epv) in pts:
    val = C_tail_coeff(rv, dv, ev, epv, mpf('1e-6'))
    print(f"     r={float(rv):4.1f} Deta={float(dv):4.1f} eta={float(ev):5.2f} "
          f"eta'={float(epv):5.2f}:  {float(val):+.8f}"
          f"   (rel.err {float(abs(val + mpi/2)/(mpi/2)):.1e})")
print("     => POSITION-INDEPENDENT (eta, eta', r, Deta all drop): a PURE-MEMORY")
print("        flat tail; the worldline memory kernel of the m=0 minimal field")
print("        in dS is theta(s)*H^2/4pi for ALL s — the task's toy kernel is")
print("        the EXACT m->0 limit, with the cutoff 1/H replaced by the light-")
print("        field decay e^{-lambda_- kappa s} at small mass ([A3]).")

print()
print("=" * 78)
print("PART C: endpoint universality V(0+) = -(1/8pi)[m^2 + (xi-1/6)R]")
print("=" * 78)
ms = sp.symbols('m', positive=True)
Vflat = -(ms/(4*sp.pi))*sp.besselj(1, ms*s)/s
print("[C1] flat massive tail -(m/4pi)J1(ms)/s at s->0:",
      sp.limit(Vflat, s, 0), " = -(1/8pi) m^2  [xi-term absent, R=0]")
xi, R = sp.symbols('xi R')
v0 = -(sp.Rational(1, 8)/sp.pi)*(ms**2 + (xi - sp.Rational(1, 6))*R)
print("[C2] v0 formula at dS minimal (xi=0, R=12H^2, m=0):",
      sp.simplify(v0.subs([(xi, 0), (R, 12*Hs**2), (ms, 0)])),
      " = +H^2/4pi  [MATCHES Part B magnitude]")
print("[C3] conformal dS (xi=1/6, m=0): V(0+) =",
      sp.simplify(v0.subs([(xi, sp.Rational(1, 6)), (ms, 0)])),
      "  [the agentF/Huygens corner sits exactly at the tail's zero]")
print("[C4] light massive minimal in dS: V(0+) = -(1/8pi)(m^2 - 2H^2):")
print("     sign FLIPS at m^2 = 2H^2 — the tail's endpoint (hence the leading")
print("     quadrature coefficient K(0)) has no fixed sign: the anti-MOND")
print("     positivity agentF proved for the Huygens bath does NOT extend to")
print("     tails automatically.  [Adiabatic sign/shape: N1 territory, OPEN.]")

print()
print("=" * 78)
print("PART D: the memory quantum Langevin equation — structure and stability")
print("=" * 78)
print("  Qdd + Om0^2 Q + lam^2 INT_0^inf [K_loc(s) + V(tau,tau-s)] Q(tau-s) ds")
print("     = -lam phi_in(z(tau));   K_loc -> 2 gam Qd + dOm^2 Q, gam = lam^2/8pi")
print("     (trajectory-BLIND, agentF lemma);  V = the tail: trajectory-DEPENDENT.")
print("  Dressed internal propagator: h~(w) = 1/(Om_R^2 - w^2 - 2i gam w + lam^2 V~(w)).")
print("  Flat-tail toy V~(w) = V0 (1 - e^{iwT})/(-iw),  V~(0) = V0*T = M0 (static).")

def Dfun(w, OmR, gam, cmem, T):
    if abs(w) < mpf('1e-12'):
        Vt = T
    else:
        Vt = (1 - mexp(1j*w*T))/(-1j*w)
    return OmR**2 - w**2 - 2j*gam*w + cmem*Vt

def winding_uhp(OmR, gam, cmem, T):
    """winding number of D(w) along the boundary of the upper-half rectangle
    [-60,60] x [1e-3, 50] — counts zeros (instabilities) inside."""
    import math
    path = []
    N1, N2 = 2400, 400
    for i in range(N1 + 1):
        path.append(mpc(-60 + 120*mpf(i)/N1, mpf('1e-3')))
    for i in range(1, N2 + 1):
        path.append(mpc(60, mpf('1e-3') + (50 - mpf('1e-3'))*mpf(i)/N2))
    for i in range(1, N1 + 1):
        path.append(mpc(60 - 120*mpf(i)/N1, 50))
    for i in range(1, N2 + 1):
        path.append(mpc(-60, 50 - (50 - mpf('1e-3'))*mpf(i)/N2))
    tot = mpf(0)
    zprev = Dfun(path[0], OmR, gam, cmem, T)
    import cmath
    argprev = cmath.phase(complex(zprev))
    for w in path[1:] + [path[0]]:
        z = Dfun(w, OmR, gam, cmem, T)
        argn = cmath.phase(complex(z))
        d = argn - argprev
        while d > math.pi:
            d -= 2*math.pi
        while d < -math.pi:
            d += 2*math.pi
        tot += d
        argprev = argn
    return int(round(float(tot/(2*mpi))))

print("[D1] zeros of the dressed denominator in the UPPER half-plane")
print("     (Om_R=1, gam=0.05, T=20 i.e. knee 0.05; c_mem = lam^2 V0):")
for cm in [mpf('0.02'), mpf('-0.02'), mpf('0.2'), mpf('-0.2'),
           mpf('1.0'), mpf('-1.0')]:
    nz = winding_uhp(mpf(1), mpf('0.05'), cm, mpf(20))
    tag = "STABLE" if nz == 0 else f"UNSTABLE ({nz} pole(s) in UHP)"
    print(f"     c_mem = {float(cm):+5.2f}:  N_UHP = {nz}   {tag}")
print("     [SHARP-cutoff toy: BOTH signs destabilize once |c_mem|*T ~ Om_R^2 —")
print("      the abrupt kernel edge rings.  Smooth-kernel comparison below.]")
print("[D2] smooth memory (exp kernel, V~(w) = c/(x - iw), x = 0.05): roots of")
print("     the cubic (Om_R^2 - w^2 - 2i gam w)(x - iw) + c  [all must have Im<0]:")
from mpmath import polyroots
OmR0, gam0, kx0 = mpf(1), mpf('0.05'), mpf('0.05')
for cm in [mpf('0.2'), mpf('1.0'), mpf('4.0'), mpf('-0.02'), mpf('-0.049'),
           mpf('-0.051'), mpf('-0.2')]:
    # i w^3 - (x+2gam) w^2 - i(Om^2+2 gam x) w + (Om^2 x + c) = 0
    rts = polyroots([1j, -(kx0 + 2*gam0), -1j*(OmR0**2 + 2*gam0*kx0),
                     OmR0**2*kx0 + cm], maxsteps=200, extraprec=80)
    mx = max(float(r.imag) for r in rts)
    stat = "STABLE" if mx < 0 else "UNSTABLE"
    print(f"     c_mem = {float(cm):+6.3f}:  max Im(root) = {mx:+.4f}   {stat}"
          f"   [static dressed gap^2 = {float(OmR0**2 + cm/kx0):+.2f}]")
cpass = 2*gam0*(kx0**2 + OmR0**2)
for cm in [mpf('0.09'), mpf('0.11')]:
    rts = polyroots([1j, -(kx0 + 2*gam0), -1j*(OmR0**2 + 2*gam0*kx0),
                     OmR0**2*kx0 + cm], maxsteps=200, extraprec=80)
    mx = max(float(r.imag) for r in rts)
    stat = "STABLE" if mx < 0 else "UNSTABLE"
    print(f"     c_mem = {float(cm):+6.3f}:  max Im(root) = {mx:+.4f}   {stat}"
          f"   [passivity threshold 2gam(x^2+Om_R^2) = {float(cpass):+.3f}]")
print("     => TWO physical bounds, both machine-confirmed:")
print("        (i) PASSIVITY: Im of the toy self-energy c w/(x^2+w^2) is anti-")
print("        damping for c > 0; instability onsets at c = 2gam(x^2+Om_R^2)")
print("        (bracketed at +0.09/+0.11 vs threshold 0.100): a PHYSICAL field")
print("        tail must have Im(self-energy) <= 0 at w > 0 (radiation), which")
print("        a real-positive pure-decay toy violates — the roots flag it.")
print("        (ii) STATIC TACHYON: gap-REDUCING memory destabilizes exactly at")
print("        Om_R^2 + V~(0) = 0 (bracketed at -0.049/-0.051): a memory-MOND")
print("        (response-reducing) amplitude is bounded by stability.  Recorded;")
print("        neither bound touches the worldline-inertia gate of Part E.")

print()
print("=" * 78)
print("PART E: helix response filters — adiabatic localization and the gate")
print("=" * 78)
# closed forms (sympy) for T1 (flat) and T2 (exponential):
Omq, kq, Tq = sp.symbols('Omega varkappa T', positive=True)
mR_T1 = sp.integrate((1 - sp.cos(Omq*s)), (s, 0, Tq))/Omq**2
mT_T1 = sp.integrate(sp.sin(Omq*s), (s, 0, Tq))/Omq**2
mR_T2 = sp.simplify(sp.integrate(sp.exp(-kq*s)*(1 - sp.cos(Omq*s)), (s, 0, sp.oo))/Omq**2)
mT_T2 = sp.simplify(sp.integrate(sp.exp(-kq*s)*sp.sin(Omq*s), (s, 0, sp.oo))/Omq**2)
print("[E1] closed forms (K0=1):")
print("     T1 flat:  m_R =", sp.simplify(mR_T1), ";  m_T =", sp.simplify(mT_T1))
print("     T2 exp :  m_R =", mR_T2, ";  m_T =", mT_T2)
print("     limits: m_R(0):  T1 ->", sp.limit(mR_T1, Omq, 0), " (= INT K s^2/2 = T^3/6);",
      "  T2 ->", sp.limit(mR_T2, Omq, 0), " (= 1/x^3)")
print("     gate:   T2 m_R(Om)/m_R(0) = x^2/(x^2+Om^2)  — EXACT Lorentzian knee.")
print("     high-Om: T1 -> T/Om^2, T2 -> 1/(x Om^2):  = M0/Om^2 with M0 = INT K ds")
print("     quadrature high-Om: m_T -> K(0)/Om^3  [T2: 1/Om^3]   [p = 3]")

# T3: massive kernel K(s) = 2 J1(m s)/(m s); closed-form sub/super-threshold:
def mR_T3(Om, m):
    if Om < mpf('1e-3')*m:
        x = (Om/m)**2          # series branch: avoids 1-sqrt(1-x) cancellation
        return (1/m**3)*(1 + x/4 + x**2/8)
    if Om < m:
        return (2/(m*Om**2))*(1 - msqrt(1 - (Om/m)**2))
    return 2/(m*Om**2)

def mR_T3_quad(Om, m):
    f = lambda u: 2*besselj(1, m*u)/(m*u)*(1 - mcos(Om*u))
    per = mpi/(m + Om)
    ptsl = [j*per for j in range(0, 4001, 40)]
    return quad(f, ptsl)/Om**2

def mT_T3_quad(Om, m):
    f = lambda u: 2*besselj(1, m*u)/(m*u)*msin(Om*u)
    per = mpi/(m + Om)
    ptsl = [j*per for j in range(0, 4001, 40)]
    return quad(f, ptsl)/Om**2

print("[E2] T3 massive kernel 2J1(ms)/(ms), m=1: closed form vs direct quad:")
for Omv in [mpf('0.1'), mpf('0.5'), mpf('0.9'), mpf(2), mpf(10)]:
    cf = mR_T3(Omv, mpf(1)); nq = mR_T3_quad(Omv, mpf(1))
    print(f"     Om={float(Omv):5.2f}: closed {float(cf):+.6e}  quad {float(nq):+.6e}"
          f"   ratio {float(nq/cf):.5f}")
print("     m_R(0) = 1/m^3 = INT K s^2/2 (Abel)  [verified by the Om->0 row];")
print("     sub-threshold gate g(Om) = 2(m/Om)^2 (1 - sqrt(1-(Om/m)^2)):")
print(f"     g(0.9 m) = {float(mR_T3(mpf('0.9'),mpf(1))/mR_T3(mpf('0.001'),mpf(1))):.3f}"
      "  [threshold bump <= 2: a system AT Om ~ m sees up to 2x the adiabatic")
print("      response — relevant if the knee sits near a probe's frequency];")
print(f"     g(10 m)  = {float(mR_T3(mpf(10),mpf(1))/mR_T3(mpf('0.001'),mpf(1))):.4f}"
      "   [= 2(m/Om)^2: p = 2 with coefficient M0 = 2/m]")

print("[E3] gate exponents by log-log slope (numeric, between Om/knee 100 and 3000):")
def slope(f, x1, x2):
    return float((mlog(abs(f(x2))) - mlog(abs(f(x1))))/(mlog(x2) - mlog(x1)))
kq0 = mpf(1)
fT2R = lambda Om: 1/(kq0*(kq0**2 + Om**2))
fT2T = lambda Om: 1/(Om*(kq0**2 + Om**2))
fT1R = lambda Om: (mpf(20) - msin(Om*20)/Om)/Om**2     # T=20, knee ~ 1/T
fT3R = lambda Om: mR_T3(Om, mpf(1))
print(f"     T2 m_R: p = {-slope(fT2R, mpf(100), mpf(3000)):.4f}   (expect 2)")
print(f"     T2 m_T: p = {-slope(fT2T, mpf(100), mpf(3000)):.4f}   (expect 3)")
print(f"     T1 m_R: p = {-slope(fT1R, mpf(100)/20, mpf(3000)/20):.4f}   (expect 2;"
      " sinc ripple O(1/(Om T)) on top — the SHARP-cutoff toy still gates at p=2:")
print("              the helix filter's M0/Om^2 term dominates ANY integrable tail)")
print(f"     T3 m_R: p = {-slope(fT3R, mpf(100), mpf(3000)):.4f}   (expect 2)")

print("[E4] adiabatic LOCALIZATION at small Om (the standard quasi-static-tail")
print("     outcome, stated at full weight): m_R(Om) - m_R(0) ~ c2 Om^2, no |Om|")
print("     or Om ln Om term  [T2 closed form; T3 closed form]:")
mp.dps = 30
for Omv in [mpf('1e-3'), mpf('1e-2'), mpf('1e-1')]:
    r2 = (fT2R(Omv) - 1/kq0**3)/Omv**2          # m_R(0) = 1/x^3 exact
    r3 = (mR_T3(Omv, mpf(1)) - 1)/Omv**2        # m_R(0) = 1/m^3 = 1 exact
    print(f"     Om={float(Omv):7.0e}:  [m_R-m_R(0)]/Om^2:  T2 {float(r2):+.6f}"
          f"   T3 {float(r3):+.6f}")
mp.dps = 20
print("     => constants: ANALYTIC in Om^2.  At Om << knee the memory force is")
print("        indistinguishable from a LOCAL (a,H,m)-dependent inertia plus")
print("        local gradient corrections: memory per se adds NOTHING in-band;")
print("        the MOND shape must come from the ADIABATIC response m_resp(a,H,m)")
print("        — whose kappa-only census protection IS broken for tails ([A2]),")
print("        but whose sign/shape remains UNDERIVED here (N1 territory).")

print("[E5] the slowly-varying-a functional (part 1 of the task):")
print("     dF(tau) = -M1 dv(tau) + INT_0^inf M(u) da(tau-u) du,")
print("     M(u) = INT_u^inf (s-u) K(s) ds   [double-integrated tail kernel].")
print("     T2 (x=1): M(u) = e^{-u}; moments c_n = INT u^n M /n! = 1 for all n.")
def Mker(u):
    return mexp(-u)
da_slow = lambda t: mexp(-(t/25)**2)            # slow Gaussian, T_s = 25 T_mem
t0 = mpf(5)
direct = quad(lambda u: Mker(u)*da_slow(t0 - u), [0, 1, 5, 20, 60])
serv = sum((-1)**n * mdiff(da_slow, t0, n) for n in range(0, 7))
print(f"     SLOW (Gaussian, T_s = 25 T_mem): direct = {float(direct):+.8e}")
print(f"                              moment-series(6) = {float(serv):+.8e}  MATCH")
omf = mpf(10)
da_fast = lambda t: mcos(omf*t)                  # oscillatory, omega = 10/T_mem
d1 = quad(lambda u: Mker(u)*da_fast(t0 - u), [0, 1, 5, 20, 60])
d2 = quad(lambda u: Mker(u)*da_fast(t0 + mpi/(2*omf) - u), [0, 1, 5, 20, 60])
amp_num = msqrt(d1**2 + d2**2)                   # two quadrature samples
amp_pred = 1/msqrt(1 + omf**2)                   # |M~(omega)| = 1/sqrt(1+w^2)
serv_f = sum((-1)**n * mdiff(da_fast, t0, n) for n in range(0, 7))
print(f"     FAST (cos(10 u/T_mem)):  response amplitude (two-phase) = "
      f"{float(amp_num):.6f}")
print(f"                              predicted |M~(w)| = 1/sqrt(1+w^2) = "
      f"{float(amp_pred):.6f}   ratio {float(amp_num/amp_pred):.5f}")
print(f"                              moment-series(6) = {float(serv_f):+.3e}"
      "   DIVERGES (~w^6)")
print("     => SLOW: the moment (local/adiabatic) expansion IS the response;")
print("        FAST: the local expansion does not exist, and the true response")
print("        of an OSCILLATORY acceleration history is suppressed by the gate")
print("        amplitude |M~| ~ (knee/w): the memory window AVERAGES the history;")
print("        frequencies above the knee are erased.  [Same physics as E3.]")

# [E6] carrier-modulated kernel (gapped internal detector), honest caveat:
print("[E6] T4 carrier kernel K = e^{-x s} cos(Om0 s) (gapped detector, gap Om0):")
def mR_T4(Om, kx, Om0):
    F = lambda x: kx/(kx**2 + x**2)
    return (F(Om0) - (F(Om0 + Om) + F(Om0 - Om))/2)/Om**2
for (kx, Om0v) in [(mpf(1), mpf(0)), (mpf(1), mpf('0.5')), (mpf(1), mpf(1e4))]:
    row = [mR_T4(Omv, kx, Om0v) for Omv in [mpf('1e-3'), mpf(1), mpf(30),
                                            mpf(1000)]]
    print(f"     Om0={float(Om0v):8.1f}: m_R(Om=1e-3,1,30,1000) = "
          + ", ".join(f"{float(x):+.3e}" for x in row))
print("     => Om0 = 0 (charge/self-force-type coupling, Quinn/Galley-Hu class):")
print("        knee at x as in T2.  Om0 >> x OFF-resonant: response collapses by")
print("        ~(x/Om0)^4-class and the knee MIGRATES to ~Om0 (no astronomical")
print("        gate).  The astronomically-gated memory inertia therefore lives in")
print("        the SOFT/charge-type sector (or resonant |Om0 - m| <~ knee), not")
print("        in far-detuned gapped dressing — a structural restriction, recorded.")

print()
print("=" * 78)
print("PART F: the data window — agentE's solar kill vs RAR flatness (SI units)")
print("=" * 78)
c0 = 2.99792458e8
hbar_eV = 6.582119569e-16
yr = 3.15576e7
a0 = 9.36e-11
Zc = 5.789
cHL = Zc*a0                      # 5.4185e-10, rho_DE footing (hostile bath norm)
cH0 = 6.55e-10                   # rho_total footing
HL, H0 = cHL/c0, cH0/c0
GN, Msun, AUm, pc = 6.674e-11, 1.989e30, 1.4959787e11, 3.0857e16
print(f"[F0] footings: H_Lambda = {HL:.3e} s^-1 ; H_0 = {H0:.3e} s^-1")
OmJ  = 2*3.141592653589793/(11.862*yr)
OmJS = 2*3.141592653589793/(19.859*yr)
OmSa = 2*3.141592653589793/(29.447*yr)
a_sun = 2.091e-7                 # agentE mean |a_sun|
Om_band_top = a0/2.0e4           # MOND-active, v = 20 km/s
Om_band_bot = 0.05*a0/3.0e5      # a = 0.05 a0 at v = 300 km/s (giant outskirts)
Om_gal_sun = 2.33e5/(8.2*1e3*pc) # solar galactic orbit v/R
Om_WB = (GN*1.5*Msun/(1.0e4*AUm)**3)**0.5
Om_GC = 4.0e3/(3.0e17)           # outer-halo GC, sigma~4 km/s, r~10 pc
Om_cl = 1.0e6/(1.0*1e6*pc/1.0)   # cluster sigma~1000 km/s, r~1 Mpc
print(f"[F1] frequency ladder (s^-1):")
print(f"     H_Lambda            = {HL:.3e}   (1/H = {1/HL/yr/1e9:.1f} Gyr)")
print(f"     RAR MOND band       = [{Om_band_bot:.2e}, {Om_band_top:.2e}]"
      f"   (= [{Om_band_bot/HL:.0f}, {Om_band_top/HL:.0f}] H)")
print(f"     Sun galactic orbit  = {Om_gal_sun:.2e}")
print(f"     wide binaries       = {Om_WB:.2e}   (10 kAU, 1.5 Msun)")
print(f"     outer-halo GC       = {Om_GC:.2e}")
print(f"     cluster crossing    = {Om_cl:.2e}")
print(f"     Saturn line         = {OmSa:.3e}")
print(f"     J-S synodic line    = {OmJS:.3e}")
print(f"     Jupiter line (main) = {OmJ:.3e}")
print(f"     => solar reflex vs galactic band: {OmJ/Om_band_top:.1e}x"
      f" ... {OmJ/Om_band_bot:.1e}x apart in frequency")

# gate need from agentE (survival line s_max = 3.21e-11 .. 3.76e-11):
dmm_fw  = 0.5*(a0/a_sun)**2
dmm_ho  = 0.5*(cHL/a_sun)**2
allow_c = 0.5*(3.21e-11/a_sun)**2
allow_k = 0.5*(3.76e-11/a_sun)**2
Gneed_fw_c, Gneed_fw_k = dmm_fw/allow_c, dmm_fw/allow_k
Gneed_ho_c, Gneed_ho_k = dmm_ho/allow_c, dmm_ho/allow_k
print(f"[F2] solar gate requirement (F4 shape, agentE survival line):")
print(f"     |dm/m|(Sun): framework {dmm_fw:.3e} ; hostile {dmm_ho:.3e}")
print(f"     allowed    : {allow_c:.3e} (conservative) .. {allow_k:.3e} (kitchen-sink)")
print(f"     gate factor needed: framework x{Gneed_fw_c:.1f} (cons) / x{Gneed_fw_k:.1f} (ks)")
print(f"                         hostile   x{Gneed_ho_c:.0f} (cons) / x{Gneed_ho_k:.0f} (ks)")
print(f"     [consistency: framework x{Gneed_fw_c:.1f} = agentE's x8.5 residual excess]")

# ceilings: Lorentzian gate 1/(1+(Om/x)^2) >= Gneed  =>  x <= Om/sqrt(Gneed-1)
print(f"[F3] knee CEILINGS x_max = Om_line/sqrt(G_need-1)  [T2-Lorentzian gate]:")
for (nm, Oml) in [("Jupiter 11.86yr", OmJ), ("J-S syn 19.86yr", OmJS),
                  ("Saturn 29.45yr", OmSa)]:
    cfw = Oml/(Gneed_fw_c - 1)**0.5
    cho = Oml/(Gneed_ho_c - 1)**0.5
    print(f"     {nm}:  framework {cfw:.2e}   hostile {cho:.2e}")
ceil_fw = OmSa/(Gneed_fw_c - 1)**0.5
ceil_ho = OmSa/(Gneed_ho_c - 1)**0.5
ceil_fw_T3 = OmSa/(2*Gneed_fw_c)**0.5
ceil_ho_T3 = OmSa/(2*Gneed_ho_c)**0.5
print(f"     T3 (massive, 2(m/Om)^2 gate): framework {ceil_fw_T3:.2e}"
      f"   hostile {ceil_ho_T3:.2e}")

# floor: RAR flatness: 1/(1+(Om_top/x)^2) >= 0.95
floor = Om_band_top/(1/0.95 - 1)**0.5
print(f"[F4] knee FLOOR from RAR flatness (gate >= 0.95 across the MOND band;")
print(f"     deep-MOND: dlog g_obs = 0.5 dlog a0_eff: 5% gate tilt = 0.011 dex,")
print(f"     inside the 0.057-dex observed RAR scatter budget):")
print(f"     x_min = Om_band_top/0.2294 = {floor:.2e} s^-1")
print(f"[F5] THE WINDOW (knee x = sqrt(2 M0/M2), the kernel scale):")
import math as _m
print(f"     framework: [{floor:.2e}, {ceil_fw:.2e}] s^-1"
      f"  = {_m.log10(ceil_fw/floor):.1f} decades  -> NON-EMPTY")
print(f"     hostile  : [{floor:.2e}, {ceil_ho:.2e}] s^-1"
      f"  = {_m.log10(ceil_ho/floor):.1f} decades  -> NON-EMPTY")
print(f"     memory time T_mem = 1/x: between {1/ceil_fw/yr:.0f} yr (fw ceiling)"
      f" / {1/ceil_ho/yr:.0f} yr (hostile) and {1/floor/yr/1e6:.1f} Myr (floor)")
print(f"     field-mass window (knee = mass scale, self-force/soft sector):")
print(f"       framework: mc^2 in [{hbar_eV*floor:.1e}, {hbar_eV*ceil_fw:.1e}] eV")
print(f"       hostile  : mc^2 in [{hbar_eV*floor:.1e}, {hbar_eV*ceil_ho:.1e}] eV")
print(f"     [m >> H throughout: principal series; dS corrections O(H/m)^2"
      f" <= {(HL/floor)**2:.0e} — the flat-massive tail analysis is valid]")

print(f"[F6] the PURE-dS tail (the task's 1/H toy; any m <~ H field):")
print(f"     max knee ~ 3H/2 = {1.5*HL:.2e} (Lambda) / {1.5*H0:.2e} (total):")
print(f"     misses the floor by {_m.log10(floor/(1.5*HL)):.2f} / "
      f"{_m.log10(floor/(1.5*H0)):.2f} decades  [footing-robust]")
g_bot = 1/(1 + (Om_band_bot/HL)**2)
g_top = 1/(1 + (Om_band_top/HL)**2)
print(f"     in-band gate at x = H_Lambda: g(bottom) = {g_bot:.2e},"
      f" g(top) = {g_top:.2e}")
print(f"     => a0_eff tilt ACROSS the RAR band: x{g_bot/g_top:.0f}"
      f" = {_m.log10(g_bot/g_top):.1f} dex (g_obs tilt ~{0.5*_m.log10(g_bot/g_top):.1f} dex)")
print(f"        vs observed total RAR scatter 0.057-0.11 dex: DEAD by >>10x.")
g_cl = 1/(1 + (Om_cl/HL)**2)
g_mid = 1/(1 + (1.0e-15/HL)**2)
print(f"     clusters vs galaxies: g(cluster)/g(band-mid) = {g_cl/g_mid:.0f}x")
print(f"        (a0_eff ~10^3 LARGER in clusters; data allow ~2x): absurd. DEAD.")
print(f"     absolute galactic suppression at x = H: 1/g(mid) = {1/g_mid:.0f}x")
print(f"        amplitude boost required — and everything slower (clusters,")
print(f"        cosmological flows) overshoots by its own (Om)^-2. DEAD.")
print(f"     ==> the dS light-field tail CANNOT serve as the gate: the knee")
print(f"         MUST be a NEW scale (a field mass), 4-9 decades above H.")

# quadrature margin at the reactive ceiling:
mT_over_mR0 = lambda x, Om: x**3/(Om*(x**2 + Om**2))
q_fw = mT_over_mR0(ceil_fw, OmSa)
q_ho = mT_over_mR0(ceil_ho, OmSa)
print(f"[F7] quadrature (dissipative) channel at the reactive ceiling")
print(f"     [m_T/m_R(0) = x^3/(Om(x^2+Om^2)), p=3; allowance = 1/G_need]:")
print(f"     framework: {q_fw:.3f} vs allowed {1/Gneed_fw_c:.3f}"
      f"  -> margin x{(1/Gneed_fw_c)/q_fw:.1f}  PASS")
print(f"     hostile  : {q_ho:.4f} vs allowed {1/Gneed_ho_c:.4f}"
      f"  -> margin x{(1/Gneed_ho_c)/q_ho:.1f}  PASS")
print(f"     [caveat: assumes quadrature fit-sensitivity ~ in-phase; a true")
print(f"      re-fit with the gated template is the registry follow-up]")

print(f"[F8] discriminators inside the window:")
print(f"     wide binaries at {Om_WB:.1e} s^-1: knee > {3*Om_WB:.1e}"
      f" (mc^2 > {hbar_eV*3*Om_WB:.1e} eV) -> WBs MONDian;")
print(f"       knee < {Om_WB/3:.1e} (mc^2 < {hbar_eV*Om_WB/3:.1e} eV)"
      f" -> WBs Newtonian:")
print(f"       the contested Gaia WB signal is a KNEE-POSITION measurement.")
print(f"     outer-halo GCs at {Om_GC:.1e} ~ the floor: knees near the floor")
print(f"       suppress GC MONDianity (GCs are observed Newtonian — usually")
print(f"       attributed to EFE; a knee just above the band mimics this). FLAG.")
print(f"     Sun's galactic acceleration ({Om_gal_sun:.1e} s^-1, quasi-DC over")
print(f"       T_mem): passes the gate at FULL strength but is common-mode")
print(f"       across the solar system: no internal ephemeris residual.")

print()
print("=" * 78)
print("RAW SUMMARY (no tuning anywhere):")
print("  - tails: dissipation kernel = trajectory-dependent memory ([A2],[A4]);")
print("    single-a prefactor survives ([A1]); kappa-only census premise FAILS")
print("  - dS m=0 minimal tail = constant H^2/4pi inside the cone ([B]): the")
print("    flat-tail toy is exact; endpoint V(0+) = -(1/8pi)[m^2+(xi-1/6)R] ([C])")
print("  - memory Langevin: smooth memory stable up to the static-tachyon point")
print("    (gap-reducing amplitude bounded by stability); sharp-cutoff toy rings ([D])")
print("  - helix filters: m_R(0) = INT K s^2/2 (LOCAL, analytic in Om^2 — the")
print("    standard quasi-static localization, full weight); gate m_R -> M0/Om^2:")
print("    p = 2 UNIVERSAL (sharp AND smooth kernels); m_T -> K(0)/Om^3: p = 3;")
print("    moment expansion valid slow, fails fast, response averaged out ([E])")
print("  - window for the knee: [2.0e-14, 2.5e-9] s^-1 (framework, conservative)")
print("    [2.0e-14, 4.0e-10] (hostile): NON-EMPTY, 4.3-5.1 decades;")
print("    mc^2 ~ [1.3e-29, 1.6e-24] eV; T_mem ~ decades..1.6 Myr ([F])")
print("  - the PURE-dS tail (knee <= 3H/2) misses the window by ~3.9 decades,")
print("    tilts the RAR by ~4.9 dex, overdrives clusters x1000: EXCLUDED ([F6])")
print("=" * 78)
