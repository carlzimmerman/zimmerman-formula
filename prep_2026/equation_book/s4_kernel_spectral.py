#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M2, SEAM S4 (kernel / spectral)
======================================================
Framework kernel (published action, Zenodo concept 21253644): K(z) = (sqrt(1+4z)-1)/(2 sqrt z),
Herglotz-Nevanlinna with UNIQUE positive measure on the cut t<0:
  region A: rho_A(t) = (1 - sqrt(1-4|t|)) / (2 pi sqrt|t|)   on (-1/4, 0)
  region B: rho_B(t) = 1 / (2 pi sqrt|t|)                     on (-inf, -1/4)
sum rule INT dmu/|t| = 1 (v11).  Operator argument z = (c^2/a0^2) d^2/dtau^2 on a
worldline; frequency map z = -(c w/a0)^2 = -W^2.  tau_mem = 2c/a0.
Both footings: a0 = 9.362e-11 (canonical) / 1.130e-10 (alt).

Derives and verifies:
 E-S4-1  TIME-DOMAIN MEMORY FUNCTION, closed form            [EXACT, new object]
         K-hat f(tau) = f(tau) - INT_0^inf Gamma(s) f(tau - s) ds,  with
           Gamma(s) = (1/tau_mem) * INT_{s/tau_mem}^inf J_1(x)/x dx
                    = (1/tau_mem) * [ 1 + J_1(b) - b J_0(b)
                        - (pi b/2)(J_1(b) H_0(b) - J_0(b) H_1(b)) ],  b = s/tau_mem
         (J = Bessel, H = Struve).  Gamma(0) = 1/tau_mem = a0/(2c);
         INT_0^inf Gamma ds = 1 (the v11 sum rule in the time domain);
         tail Gamma(s) ~ -(1/tau_mem) sqrt(2/pi) b^{-3/2} sin(b - 3pi/4).
 E-S4-2  UNITARITY CIRCLE + PHASE-LAG LAW                    [EXACT]
         On the cut boundary (bound orbits, W = c w/a0 > 1/2):
         K = (sqrt(4W^2-1) + i)/(2W),  |K| = 1 exactly,
         phase  phi(w) = arcsin(a0/(2 c w));  reactive deficit 1-ReK = 1 - sqrt(1-sin^2 phi);
         drift identity 2 w Im K = a0/c (universal; = laneK's secular drift).
 E-S4-3  SPECTRAL DICHOTOMY at the edge w_edge = a0/(2c)      [EXACT]
         w > a0/2c: |K| = 1 (pure phase, zero amplitude response);
         w < a0/2c: Re K = 0 (purely dissipative boundary value), |K| < 1.
 E-S4-4  INVERSE-MOMENT FAMILY M_p = INT dmu/|t|^p, closed form, p in (1/2, 3/2)
         M_p = (2^{2p-1}/pi) * [ 1/(2p-1) - sqrt(pi) Gamma(2-p) / (2 (3-2p) Gamma(5/2-p)) ]...
         (computed symbolically below; M_1 = 1 recovers the sum rule; region-B share 2/pi).
 E-S4-5  WIDE-BINARY PHASE-LAG EQUATION (numbers, both footings)  [reading-B-flagged]
         phi(r) = arcsin[(a0/2c) sqrt(r^3/GM)]; drift r-dot/r = a0/c.
HONESTY: E-S4-2/3/5 live on the OPERATOR (spectral, Reading B) evaluation of the
published kernel. planetary_doors/KERNEL_PLANETS.md shows Reading B is excluded
~250-500x in the drift channel and erases the galactic RAR; the framework's galactic
wins use the constitutive Reading A. These are exact consequences of the published
operator, stated as such -- not endorsed phenomenology.
"""
import sys, math
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
FAIL = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

u, s, b, lam, z, W, p, t = sp.symbols('u s b lam z W p t', positive=True)

# measure in u = sqrt|t| coordinates: dmu_A = (1-sqrt(1-4u^2))/pi du on (0,1/2);
# dmu_B = du/pi on (1/2, inf).   [derived: dt = 2u du into rho_A, rho_B]
print("="*78)
print("measure bookkeeping (u = sqrt|t| substitution) + v11 sum rule")
print("="*78)
rhoA_t = (1 - sp.sqrt(1 - 4*sp.Abs(t)))/(2*sp.pi*sp.sqrt(sp.Abs(t)))
# check the u-substitution: rho_A(t) dt with t=-u^2 -> (1-sqrt(1-4u^2))/pi du
subA = sp.simplify(rhoA_t.subs(sp.Abs(t), u**2) * 2*u - (1 - sp.sqrt(1 - 4*u**2))/sp.pi)
check("dmu_A = (1-sqrt(1-4u^2))/pi du  (from rho_A, dt=2u du)", subA == 0)
# sum rule: M_1 = INT dmu/|t| : region A + region B
MA = sp.integrate((1 - sp.sqrt(1 - 4*u**2))/(sp.pi*u**2), (u, 0, sp.Rational(1, 2)))
MB = sp.integrate(1/(sp.pi*u**2), (u, sp.Rational(1, 2), sp.oo))
check("region-B share == 2/pi (exact)", sp.simplify(MB - 2/sp.pi) == 0)
check("v11 sum rule: INT dmu/|t| == 1 (region A gives 1-2/pi)", sp.simplify(MA + MB - 1) == 0)

print()
print("="*78)
print("E-S4-1  time-domain memory function Gamma(s)")
print("="*78)
# STEP 1 (exact): retarded Green's fn of (d^2/ds^2 + Omega^2) is sin(Omega s)/Omega
Om = sp.symbols('Omega', positive=True)
G = sp.sin(Om*s)/Om
check("retarded Green fn: G'' + Om^2 G == 0, G(0)=0, G'(0)=1",
      sp.simplify(sp.diff(G, s, 2) + Om**2*G) == 0
      and G.subs(s, 0) == 0 and sp.diff(G, s).subs(s, 0) == 1)
# STEP 2 (exact): Laplace closure. In units eps = a0/c = 1 (tau_mem = 2):
#   Gamma(s) = INT dmu(t) sin(sqrt|t| s)/sqrt|t|   and
#   INT_0^inf Gamma(s) e^{-lam s} ds must equal 1 - K(lam^2)   [master identity]
# check per-mode: L[sin(u s)/u](lam) = 1/(lam^2 + u^2)
Lmode = sp.integrate(sp.sin(u*s)/u * sp.exp(-lam*s), (s, 0, sp.oo), conds='none')
check("Laplace per-mode: L[sin(us)/u] == 1/(lam^2+u^2)",
      sp.simplify(Lmode - 1/(lam**2 + u**2)) == 0)
# so L[Gamma](lam) = INT dmu/(|t| + lam^2) = 1 - K(lam^2): verify numerically (mpmath)
def Kfun(zz):
    return (mp.sqrt(1 + 4*zz) - 1)/(2*mp.sqrt(zz))
def dmu_int(f):
    A = mp.quad(lambda uu: (1 - mp.sqrt(1 - 4*uu**2))/mp.pi * f(uu), [0, mp.mpf(1)/2])
    B = mp.quad(lambda uu: f(uu)/mp.pi, [mp.mpf(1)/2, mp.inf])
    return A + B
for zz in (mp.mpf('0.1'), mp.mpf('1'), mp.mpf('100')):
    lhs = dmu_int(lambda uu: 1/(uu**2 + zz))
    rhs = 1 - Kfun(zz)
    check(f"master identity INT dmu/(|t|+z) == 1-K(z) at z={float(zz)}",
          abs(lhs - rhs) < mp.mpf('1e-20'))
# STEP 3 (exact): reduce the spectral integral to the J1 form.
#   Gamma(s) = (1/pi)[ INT_0^inf sin(us)/u du - INT_0^{1/2} sqrt(1-4u^2) sin(us)/u du ]
#   first = pi/2;  second (u=v/2): I(b)=INT_0^1 sqrt(1-v^2) sin(bv)/v dv, b=s/2,
#   with dI/db = INT_0^1 sqrt(1-v^2) cos(bv) dv = pi J1(b)/(2b)
#   (Poisson integral representation of J1; sympy cannot close it -- verified
#    numerically at several b to 1e-25, which is a derivation-step check, not a fit)
for bb in (mp.mpf('0.3'), mp.mpf('2'), mp.mpf('17')):
    lhsP = mp.quad(lambda vv: mp.sqrt(1 - vv**2)*mp.cos(bb*vv), [0, 1])
    rhsP = mp.pi*mp.besselj(1, bb)/(2*bb)
    check(f"Poisson rep: INT_0^1 sqrt(1-v^2)cos(bv)dv == pi J1(b)/(2b) at b={float(bb)}",
          abs(lhsP - rhsP) < mp.mpf('1e-25'))
# therefore Gamma(s) = (1/2)[1 - INT_0^{s/2} J1/x dx] = (1/2) INT_{s/2}^inf J1(x)/x dx
# (using INT_0^inf J1/x dx = 1). Verify INT_0^inf J1(x)/x dx = 1:
J1tot = sp.integrate(sp.besselj(1, u)/u, (u, 0, sp.oo), conds='none')
check("INT_0^inf J1(x)/x dx == 1", sp.simplify(J1tot - 1) == 0)
# numeric cross-check: spectral integral vs (1/2) INT_{s/2}^inf J1/x dx  at several s
def Gam_spec(ss):
    # oscillatory tail: integrate region B with mpmath oscillatory quadrature
    A = mp.quad(lambda uu: (1 - mp.sqrt(1 - 4*uu**2))/mp.pi * mp.sin(uu*ss)/uu,
                [0, mp.mpf(1)/2])
    B = mp.quadosc(lambda uu: mp.sin(uu*ss)/(mp.pi*uu), [mp.mpf(1)/2, mp.inf],
                   period=2*mp.pi/ss)
    return A + B
def Gam_J1(ss):
    bb = ss/2
    return mp.quadosc(lambda xx: mp.besselj(1, xx)/xx, [bb, mp.inf],
                      period=2*mp.pi)/2
for ss in (mp.mpf('0.5'), mp.mpf('3'), mp.mpf('10'), mp.mpf('40')):
    ga, gb = Gam_spec(ss), Gam_J1(ss)
    check(f"Gamma spectral == (1/2)INT_{{s/2}}^inf J1/x dx at s={float(ss)} "
          f"({mp.nstr(ga, 8)})", abs(ga - gb) < mp.mpf('1e-18'))
# STEP 4: Bessel-Struve CLOSED FORM.
#   INT_0^b J1/x dx = INT_0^b J0 dx - J1(b)   [since J1/x = J0 - J1']
J1x_id = sp.simplify(sp.besselj(1, b)/b -
                     (sp.besselj(0, b) - sp.diff(sp.besselj(1, b), b)))
check("identity J1(x)/x == J0(x) - J1'(x)", J1x_id == 0)
#   INT_0^b J0 dx = b J0(b) + (pi b/2)[J1(b) H0(b) - J0(b) H1(b)]  (Struve; verify numerically)
def intJ0(bb):
    return bb*mp.besselj(0, bb) + mp.pi*bb/2*(
        mp.besselj(1, bb)*mp.struveh(0, bb) - mp.besselj(0, bb)*mp.struveh(1, bb))
for bb in (mp.mpf('0.7'), mp.mpf('5'), mp.mpf('20')):
    direct = mp.quad(lambda xx: mp.besselj(0, xx), [0, bb])
    check(f"INT_0^b J0 == Struve closed form at b={float(bb)}",
          abs(direct - intJ0(bb)) < mp.mpf('1e-22'))
def Gam_closed(ss):
    bb = ss/2
    if bb == 0:
        return mp.mpf(1)/2
    return (1 + mp.besselj(1, bb) - intJ0(bb))/2
for ss in (mp.mpf('0.5'), mp.mpf('3'), mp.mpf('10'), mp.mpf('40')):
    check(f"closed form (Bessel-Struve) == J1-integral form at s={float(ss)}",
          abs(Gam_closed(ss) - Gam_J1(ss)) < mp.mpf('1e-20'))
# STEP 5: endpoints + sum rule in time domain (units eps=1, tau_mem=2)
check("Gamma(0) == 1/tau_mem  (= a0/2c)", abs(Gam_closed(mp.mpf(0)) - mp.mpf(1)/2) < 1e-25)
tot = mp.quad(lambda ss: Gam_closed(ss), [0, 5, 20, 60, 120]) + \
      mp.quadosc(lambda ss: Gam_closed(ss), [120, mp.inf], period=4*mp.pi)
check(f"INT_0^inf Gamma ds == 1 (time-domain sum rule; got {mp.nstr(tot, 10)})",
      abs(tot - 1) < mp.mpf('1e-8'))
# STEP 6: tail asymptotics Gamma ~ -(1/tau) sqrt(2/pi) b^{-3/2} sin(b - 3pi/4)
# evaluate at an extremum of sin(b-3pi/4) (|sin|=1) to avoid zero-crossing blowup
bigb = 5*mp.pi/4 + 2*mp.pi*47    # sin(b-3pi/4) = +1
ss = 2*bigb
asym = -mp.sqrt(2/mp.pi)*bigb**mp.mpf('-1.5')*mp.sin(bigb - 3*mp.pi/4)/2
ratio = Gam_closed(ss)/asym
check(f"tail ~ -(1/tau)sqrt(2/pi) b^-3/2 sin(b-3pi/4): ratio {mp.nstr(ratio,6)} -> 1",
      abs(ratio - 1) < 0.01)

print()
print("="*78)
print("E-S4-2 / E-S4-3  unitarity circle, phase-lag law, spectral dichotomy")
print("="*78)
# cut boundary value above the edge (W>1/2): K(-W^2 + i0)
Kbound = (sp.sqrt(4*W**2 - 1) + sp.I)/(2*W)
# derive it: K(z)=(sqrt(1+4z)-1)/(2 sqrt z), z = W^2 exp(i pi) approached from above
zc = W**2 * sp.exp(sp.I*(sp.pi - sp.symbols('d', positive=True)))
dd = sp.symbols('d', positive=True)
Kc = (sp.sqrt(1 + 4*zc) - 1)/(2*sp.sqrt(zc))
Klim = sp.limit(Kc.rewrite(sp.exp), dd, 0, '+')
diffK = sp.simplify(sp.expand_complex(Klim - Kbound).subs(W, sp.Rational(7, 5)))
check("boundary value K(-W^2+i0) == (sqrt(4W^2-1)+i)/(2W)  [derived by limit]",
      sp.Abs(diffK.evalf(30)) < 1e-25)
# exact symbolic re/im on the cut: parametrize W = sqrt(q^2 + 1/4) (q>0 <=> W>1/2),
# so sqrt(4W^2-1) = 2q and sympy's re/im are unambiguous
q = sp.symbols('q', positive=True)
Kq = Kbound.subs(W, sp.sqrt(q**2 + sp.Rational(1, 4)))
Kq = sp.simplify(sp.expand_complex(Kq))
Wq = sp.sqrt(q**2 + sp.Rational(1, 4))
check("|K|^2 == 1 on the cut, W>1/2 (unitarity circle, exact)",
      sp.simplify(sp.re(Kq)**2 + sp.im(Kq)**2 - 1) == 0)
check("Im K == 1/(2W) == a0/(2 c w)  => phase phi = arcsin(a0/2cw)",
      sp.simplify(sp.im(Kq) - 1/(2*Wq)) == 0)
check("Re K == sqrt(1 - 1/(4W^2))  => 1-ReK = 1 - sqrt(1-sin^2 phi)",
      sp.simplify(sp.re(Kq) - sp.sqrt(1 - 1/(4*Wq**2))) == 0)
# drift identity: w in physical units, W = c w/a0:  2 w Im K = 2 w a0/(2 c w) = a0/c
a0s, cs, ws = sp.symbols('a0 c w', positive=True)
check("2 w Im K == a0/c  (universal secular drift, = laneK)",
      sp.simplify(2*ws*(a0s/(2*cs*ws)) - a0s/cs) == 0)
# below the edge (W<1/2): boundary value purely imaginary
Wl = sp.Rational(1, 3)
zc2 = Wl**2 * sp.exp(sp.I*(sp.pi - dd))
Kc2 = sp.limit(((sp.sqrt(1 + 4*zc2) - 1)/(2*sp.sqrt(zc2))).rewrite(sp.exp), dd, 0, '+')
Kc2 = sp.simplify(sp.expand_complex(Kc2))
check("below edge (W=1/3): Re K == 0 (purely dissipative)",
      sp.simplify(sp.re(Kc2)) == 0)
check("below edge: Im K == (1-sqrt(1-4W^2))/(2W), |K|<1",
      sp.simplify(sp.im(Kc2) - (1 - sp.sqrt(1 - 4*Wl**2))/(2*Wl)) == 0
      and float(sp.Abs(Kc2)) < 1)

print()
print("="*78)
print("E-S4-4  inverse-moment family M_p = INT dmu/|t|^p, closed form")
print("="*78)
MpB = sp.integrate(u**(-2*p)/sp.pi, (u, sp.Rational(1, 2), sp.oo),
                   conds='none')          # region B, p>1/2
MpB = sp.simplify(MpB)
check("region B: M_p^B == 2^(2p-1)/(pi(2p-1))",
      sp.simplify(MpB - 2**(2*p - 1)/(sp.pi*(2*p - 1))) == 0)
# region A by integration by parts (boundary term at u=0 vanishes since
# 1-sqrt(1-4u^2) ~ 2u^2, so u^{1-2p}(1-sqrt(1-4u^2)) ~ u^{3-2p} -> 0 for p<3/2):
#  INT_0^{1/2}(1-sqrt(1-4u^2))u^{-2p}du
#    = 2^{2p-1}/(1-2p) + (4/(2p-1)) INT_0^{1/2} u^{2-2p}/sqrt(1-4u^2) du
# and (u = sin(th)/2):  INT u^{2-2p}/sqrt(1-4u^2) du = 2^{2p-4} INT_0^{pi/2} sin^{2-2p}th dth
th = sp.symbols('th', positive=True)
sinpow_expected = sp.sqrt(sp.pi)*sp.gamma(sp.Rational(3, 2) - p)/(2*sp.gamma(2 - p))
# Wallis formula: sympy cannot close the symbolic-p integral in finite time; verify it
# EXACTLY at rational p (sympy closes sin^(1/2) integrals in gamma terms) and
# numerically at a generic irrational-ish p
wall_ok = True
for pr in (sp.Rational(3, 4), sp.Integer(1), sp.Rational(5, 4)):
    ex = sp.integrate(sp.sin(th)**(2 - 2*pr), (th, 0, sp.pi/2), conds='none')
    d_ = sp.simplify(ex - sinpow_expected.subs(p, pr))
    # sympy leaves the fractional-power integral unevaluated; accept 0 either
    # symbolically or at 35-digit precision (still a derivation-step check)
    wall_ok = wall_ok and (d_ == 0 or abs(d_.evalf(35)) < sp.Float('1e-30', 35))
check("Wallis: INT sin^(2-2p) == sqrt(pi)Gamma(3/2-p)/(2Gamma(2-p)) at p=3/4,1,5/4 (35 dgt)",
      wall_ok)
prn = mp.mpf('0.63')
wnum = mp.quad(lambda thh: mp.sin(thh)**(2 - 2*prn), [0, mp.pi/2])
wcf = mp.sqrt(mp.pi)*mp.gamma(mp.mpf(3)/2 - prn)/(2*mp.gamma(2 - prn))
check("Wallis numeric at generic p=0.63", abs(wnum - wcf) < mp.mpf('1e-22'))
Mp_closed = 2**(2*p - 2)*sp.gamma(sp.Rational(3, 2) - p)/(
    sp.sqrt(sp.pi)*(2*p - 1)*sp.gamma(2 - p))
# assemble: M_p = M_p^A + M_p^B with the IBP pieces (pure algebra given Wallis)
MpA = (1/sp.pi)*(2**(2*p - 1)/(1 - 2*p)
                 + (4/(2*p - 1))*2**(2*p - 4)*2*sinpow_expected)
check("M_p == 2^(2p-2) Gamma(3/2-p) / (sqrt(pi)(2p-1)Gamma(2-p))  [assembled]",
      sp.simplify(MpA + MpB - Mp_closed) == 0)
check("M_1 == 1 recovers the v11 sum rule (from the closed form)",
      sp.simplify(Mp_closed.subs(p, 1) - 1) == 0)
# adversarial numeric check of the closed form against the raw measure integral;
# region B uses its (symbolically verified) closed form to avoid slow-decay quad error
def Mp_direct(pr):
    # substitution u = v^5/2 kills the u->0 endpoint singularity for all p < 3/2;
    # 1-sqrt(1-4u^2) = 4u^2/(1+sqrt(1-4u^2)) avoids cancellation at tiny u (exact rewrite)
    def f(vv):
        uu = vv**5/2
        wA = 4*uu**2/(1 + mp.sqrt(1 - 4*uu**2))
        return wA/mp.pi * uu**(-2*pr) * mp.mpf(5)/2*vv**4
    A = mp.quad(f, [0, mp.mpf(1)/2, 1])
    B = 2**(2*pr - 1)/(mp.pi*(2*pr - 1))
    return A + B
for pr in (mp.mpf('0.6'), mp.mpf('0.75'), mp.mpf('1.25'), mp.mpf('1.4')):
    num = Mp_direct(pr)
    cf = (2**(2*pr - 2)*mp.gamma(mp.mpf(3)/2 - pr) /
          (mp.sqrt(mp.pi)*(2*pr - 1)*mp.gamma(2 - pr)))
    check(f"M_p closed form vs direct measure integral at p={float(pr)} "
          f"(closed {mp.nstr(cf, 10)}, numeric {mp.nstr(num, 10)})",
          abs(cf - num) < mp.mpf('1e-12'))
# IBP-step numeric check (the load-bearing reduction, p=0.75)
pr = mp.mpf('0.75')
ibp_lhs = mp.quad(lambda uu: (1 - mp.sqrt(1 - 4*uu**2))*uu**(-2*pr),
                  [0, mp.mpf('1e-8'), mp.mpf(1)/4, mp.mpf(1)/2])
ibp_rhs = 2**(2*pr - 1)/(1 - 2*pr) + (4/(2*pr - 1))*mp.quad(
    lambda uu: uu**(2 - 2*pr)/mp.sqrt(1 - 4*uu**2),
    [0, mp.mpf(1)/4, mp.mpf(1)/2])
check("IBP identity (region A reduction) numeric at p=0.75",
      abs(ibp_lhs - ibp_rhs) < mp.mpf('1e-15'))

print()
print("="*78)
print("E-S4-5  wide-binary phase-lag numbers (Reading-B-flagged), both footings")
print("="*78)
Gn, Msun, AU = 6.67430e-11, 1.98892e30, 1.495978707e11
cn = 2.99792458e8
yr = 3.155815e7
for tag, a0n in (("canonical", 9.362e-11), ("alt", 1.130e-10)):
    print(f"  [{tag}] a0 = {a0n:.4g}:  drift r-dot/r = a0/c = {a0n/cn*yr:.3e} /yr (universal)")
    for rkAU, Mtot in ((3, 1.5), (10, 1.5), (20, 1.5)):
        r = rkAU*1e3*AU
        w = math.sqrt(Gn*Mtot*Msun/r**3)
        Wn = cn*w/a0n
        phi = math.asin(a0n/(2*cn*w))
        print(f"     r={rkAU:>4} kAU (M={Mtot} Msun): W={Wn:.3e}  phi={phi:.3e} rad"
              f"  1-ReK={1-math.sqrt(1-(1/(2*Wn))**2):.3e}  r-dot={a0n/cn*r*yr:.3g} m/yr")
    # edge period (below which response turns dissipative):
    Tedge = 2*math.pi/(a0n/(2*cn))
    print(f"     dichotomy edge: w_edge=a0/2c={a0n/2/cn:.3e}/s  (period {Tedge/yr/1e9:.0f} Gyr)")

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL CHECKS PASS")
sys.exit(1 if FAIL else 0)
