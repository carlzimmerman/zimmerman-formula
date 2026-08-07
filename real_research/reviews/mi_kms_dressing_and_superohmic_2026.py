#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
mi_kms_dressing_and_superohmic_2026.py -- LANE Z (doors F3 + F4), 2026-08-07
============================================================================

PART 1 (F3): Can a linear tau-convolution dressing  G = G_seed + q^2 K * G
break KMS at all?

  Frequency space:  Ghat(w) = Ghat_seed(w) / (1 - q^2 Khat(w)).
  CONVENTION (stated, tracked): Ghat(w) = Int dtau e^{+i w tau} G(tau);
  KMS  <=>  Ghat(-w) = e^{-beta w} Ghat(w).
  Under the dressing the KMS ratio maps to
      e^{-beta w} * (1 - q^2 Khat(w)) / (1 - q^2 Khat(-w)),
  so KMS is inherited  <=>  Khat(-w) = Khat(w) on the support of Ghat_seed.

  CLOSURE OF THE EVASIONS (each exhibited numerically below):
   (i)  K real AND dressed G a valid correlator (hermitian <=> Ghat real):
        real K gives Khat(-w) = conj Khat(w); Ghat_dressed real forces Khat
        real; together Khat is EVEN  =>  KMS inherited.  THEOREM.
   (ii) K real + CAUSAL (theta(tau) e^{-tau/tc}): Khat(-w) = conj Khat(w)
        with Im Khat != 0 (Kramers-Kronig), so the KMS ratio is broken in
        PHASE ONLY (|ratio| preserved EXACTLY) -- and Im Ghat_dressed != 0,
        i.e. the dressed object is NOT the Wightman function of any state.
        Unphysical; not a NESS.
   (iii) Khat real but NON-even (KMS genuinely broken with Ghat still real
        positive) REQUIRES a complex ACAUSAL kernel: causal K => Khat is the
        boundary value of a UHP-analytic function; Im Khat = 0 on the axis
        + UHP analyticity + decay => Khat = const (Liouville/KK), and const
        is even.  Exhibited: Khat(w) = 1/(1+(w-1)^2)  <->
        K(tau) = (1/2) e^{-|tau|} e^{-i tau}: hermitian (K(-tau)=conj K(tau)),
        manifestly supported at tau < 0 (ACAUSAL), complex.
  VERDICT: NESS-by-LINEAR-resummation dies BY THEOREM for every real causal
  kernel.  The sole mathematical escape is a complex acausal hermitian
  kernel -- not dynamics.  (Nonlinear / state-dependent kernels are OUTSIDE
  this theorem's scope and stay open.)

  Numerical seed: the actual Bunch-Davies kernel, conformally coupled scalar
  in dS4 on a comoving worldline,
      G(tau) = -(H^2/16 pi^2) / sinh^2( H(tau - i eps)/2 ),   beta = 2 pi/H,
  exact FT (proved by contour shift, verified by quadrature here):
      Ghat(w) = (w/2 pi) / (1 - e^{-beta w}).

PART 2 (F4): super-ohmic EQUILIBRIUM.  J(w) = eta_s w^s exp(-w/w_cut),
beta = 2 pi/H (Gibbons-Hawking),
      delta_m  propto  P Int_{w0}^inf dw  J(w) coth(beta w/2) / w^2
(standard Caldeira-Leggett normalisation).  The integrand is POINTWISE
POSITIVE on (0, inf) for EVERY s: coth(beta w/2) > 0, w^{s-2} > 0, e^{-w/wc}
> 0.  The principal value is VACUOUS -- there is no interior pole; the only
singularity is the IR ENDPOINT.  Signs computed for s = 1,2,3,4 over w0 and
w_cut scans, both a0 footings: ALL POSITIVE, no flip anywhere.
  IR honesty: s=1 diverges as 1/(pi w0) (verified slope -1); s=2 ALSO
  diverges, logarithmically, with coefficient 1/pi = 2/(beta) * (beta/2pi)
  (verified) -- the task sheet's "the s=1 case is IR-divergent" UNDERSTATES
  the problem; s=3,4 are IR-finite (exact series/polygamma cross-checks).
  VERDICT: no admissible s flips the sign in equilibrium; delta_m > 0 for
  eta_s > 0 = inertia INCREASE = ANTI-MOND.  The anti-MOND no-go GENERALISES
  to the whole (super-)ohmic family.  The NESS detour was NOT redundant --
  and Part 1 closes the linear version of it.

Footings (report both on any dimensional number; sign is footing-blind):
  canonical a0 = 9.3614e-11 m/s^2 (rho_DE + cH_Lambda, cH_Lambda=5.4194e-10)
  ALT       a0 = 1.13e-10   m/s^2 (rho_total + cH0), ratio x1.2082.
  kappa = 1/2 is FITTED, NOT DERIVED.

CREDITS: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA
253:273 eqs 6-9; his eqs 10-11 give a second coefficient; Milgrom 2008
arXiv:0801.3133 sec 7.3.1 notes the mismatch "isn't necessarily meaningful".
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys.229:384.  Temperature
sqrt(a^2+Lambda/3)/2pi: Narnhofer-Peter-Thirring 1996 IJMPB 10:1507.
Five-acceleration: Deser-Levin 1997 CQG 14:L163.  Bunch-Davies kernel:
Birrell-Davies.  Ghost condensate: Arkani-Hamed-Cheng-Luty-Mukohyama 2004.
Bath machinery: Caldeira-Leggett.  Empirical a0 = 1.2e-10: McGaugh /
Lelli-McGaugh-Schombert (SPARC).
"""

import sys
import numpy as np
import sympy as sp
from mpmath import mp, mpf, mpc

mp.dps = 20

RESULTS = []


def check(name, ok, detail=""):
    tag = "[OK]  " if ok else "[FAIL]"
    print("%s %s" % (tag, name))
    if detail:
        print("       %s" % detail)
    RESULTS.append(bool(ok))


def ns(x, n=8):
    return mp.nstr(x, n)


print("=" * 78)
print("PART 1 (F3): linear tau-convolution dressing vs KMS")
print("=" * 78)
print("Convention: Ghat(w) = Int dtau e^{+i w tau} G(tau);"
      "  KMS <=> Ghat(-w) = e^{-beta w} Ghat(w).")

# ---------------------------------------------------------------- sympy part
w, beta, q = sp.symbols('w beta q_c', positive=True)
Gs = sp.Function('Gs')

# (1) even Khat -- represent evenness structurally as Khat(w) = k(w^2)
k = sp.Function('k')
Gd_even = lambda x: Gs(x) / (1 - q**2 * k(x**2))
ratio1 = (Gd_even(-w) / Gd_even(w)).subs(Gs(-w), sp.exp(-beta * w) * Gs(w))
res1 = sp.simplify(ratio1 - sp.exp(-beta * w))
check("F3-01 [sympy] Khat even => dressed KMS ratio == e^{-beta w} EXACTLY",
      res1 == 0, "residual = %s" % res1)

# (2) generic Khat -- the exact deviation factor, hence the iff condition
Kh = sp.Function('Kh')
Gd_gen = lambda x: Gs(x) / (1 - q**2 * Kh(x))
ratio2 = (Gd_gen(-w) / Gd_gen(w)).subs(Gs(-w), sp.exp(-beta * w) * Gs(w))
factor = sp.simplify(ratio2 / sp.exp(-beta * w))
res2 = sp.simplify(factor - 1 - q**2 * (Kh(-w) - Kh(w)) / (1 - q**2 * Kh(-w)))
check("F3-02 [sympy] deviation factor == 1 + q^2(Kh(-w)-Kh(w))/(1-q^2 Kh(-w))"
      "  => KMS preserved <=> Khat(-w)=Khat(w) on the support",
      res2 == 0, "residual = %s" % res2)

# ------------------------------------------------------------- numeric seed
H1 = mpf(1)                # units H = 1
BETA1 = 2 * mp.pi / H1     # Gibbons-Hawking beta = 2 pi / H
EPS = mpf('0.5')           # finite i-epsilon, corrected EXACTLY by e^{w eps}
J = mpc(0, 1)


def G_BD_ct(z):
    """BD Wightman kernel at complex time z (conformal scalar, dS4)."""
    return -(H1**2 / (16 * mp.pi**2)) / mp.sinh(H1 * z / 2)**2


def Ghat_quad(wv):
    wv = mpf(wv)
    f = lambda t: mp.e**(J * wv * t) * G_BD_ct(t - J * EPS)
    I = mp.quad(f, [-45, 0, 45], maxdegree=10)
    return mp.e**(wv * EPS) * I     # exact contour-shift correction


def Ghat_exact(wv):
    wv = mpf(wv)
    return (wv / (2 * mp.pi)) / (-mp.expm1(-BETA1 * wv))   # expm1: no underflow


# (3) analytic beta-periodicity of the BD kernel itself (imaginary time)
t0, ep = mpf('0.9'), mpf('0.3')
lhs = G_BD_ct(t0 - J * (BETA1 - ep))
rhs = G_BD_ct(-t0 - J * ep)
dev_per = abs(lhs - rhs) / abs(rhs)
check("F3-03 [numeric] BD kernel beta-periodic in imaginary time: "
      "G(t - i(beta-eps)) == G(-t - i eps)", dev_per < mpf('1e-18'),
      "rel dev = %s at t=0.9, eps=0.3" % ns(dev_per))

WS = [mpf('0.3'), mpf('0.7'), mpf('1.2'), mpf('2.0')]
Gq = {}
for wv in WS:
    Gq[float(wv)] = Ghat_quad(wv)
    Gq[float(-wv)] = Ghat_quad(-wv)

# (4) quadrature vs the exact closed form (independent derivation)
relerrs = []
imfracs = []
for wv in WS:
    for sgn in (1, -1):
        wx = sgn * wv
        gq = Gq[float(wx)]
        ge = Ghat_exact(wx)
        relerrs.append(abs(gq - ge) / abs(ge))
        imfracs.append(abs(mp.im(gq)) / abs(gq))
check("F3-04 [numeric] BD quadrature == (w/2pi)/(1-e^{-beta w})  (8 points, "
      "+/-w in {0.3,0.7,1.2,2.0})", max(relerrs) < mpf('1e-10'),
      "max rel err = %s ; max |Im|/|G| = %s (seed hermitian)"
      % (ns(max(relerrs)), ns(max(imfracs))))

# (5) KMS of the seed, from quadrature values only
kmsdev = []
for wv in WS:
    r = Gq[float(-wv)] / Gq[float(wv)]
    kmsdev.append(abs(r - mp.e**(-BETA1 * wv)) / mp.e**(-BETA1 * wv))
check("F3-05 [numeric] seed KMS from quadrature: Ghat(-w)/Ghat(w) == "
      "e^{-beta w}", max(kmsdev) < mpf('1e-10'),
      "max rel dev = %s" % ns(max(kmsdev)))

q2 = mpf('0.25')
KhE = lambda x: 1 / (1 + x**2)               # real even
KhC = lambda x: 1 / (1 - J * x)              # real CAUSAL kernel theta(t)e^{-t}
KhA = lambda x: 1 / (1 + (x - 1)**2)         # real NON-even (acausal, complex K)

# (6) resummation algebra: Neumann series == 1/(1 - q^2 Khat)
wv = mpf('0.7')
series = mp.fsum([(q2 * KhE(wv))**n for n in range(120)]) * Ghat_exact(wv)
closed = Ghat_exact(wv) / (1 - q2 * KhE(wv))
res6 = abs(series - closed) / abs(closed)
check("F3-06 [numeric] Neumann resummation sum_n (q^2 Khat)^n == "
      "1/(1-q^2 Khat)", res6 < mpf('1e-15'), "rel dev = %s" % ns(res6))

# (7) even dressing preserves KMS (Khat evaluated independently at +w and -w)
devE = []
for wv in WS:
    gd_p = Gq[float(wv)] / (1 - q2 * KhE(wv))
    gd_m = Gq[float(-wv)] / (1 - q2 * KhE(-wv))
    devE.append(abs(gd_m / gd_p - mp.e**(-BETA1 * wv)) / mp.e**(-BETA1 * wv))
check("F3-07 [numeric] even dressing Khat=1/(1+w^2), q^2=0.25: KMS ratio "
      "still e^{-beta w}", max(devE) < mpf('1e-10'),
      "max rel dev = %s" % ns(max(devE)))

# (8) the causal kernel: verify its FT and the reality symmetry
ft_dev = []
for wv in (mpf('0.7'), mpf('2.0'), mpf('-1.2')):
    num = mp.quad(lambda t: mp.e**(J * wv * t - t), [0, 45], maxdegree=10)
    ft_dev.append(abs(num - KhC(wv)) / abs(KhC(wv)))
conj_dev = max(abs(KhC(-wv) - mp.conj(KhC(wv))) for wv in WS)
check("F3-08 [numeric] K = theta(tau) e^{-tau} (causal, L1): Khat = 1/(1-iw) "
      "verified by FT; Khat(-w) == conj Khat(w) (real kernel)",
      max(ft_dev) < mpf('1e-12') and conj_dev < mpf('1e-18'),
      "max FT rel err = %s ; max conj-sym dev = %s"
      % (ns(max(ft_dev)), ns(conj_dev)))

# (9) causal dressing BREAKS KMS -- but in PHASE ONLY (modulus preserved)
devC, modC, imC = [], [], []
for wv in WS:
    gd_p = Gq[float(wv)] / (1 - q2 * KhC(wv))
    gd_m = Gq[float(-wv)] / (1 - q2 * KhC(-wv))
    r = gd_m / gd_p
    e = mp.e**(-BETA1 * wv)
    devC.append(abs(r - e) / e)
    modC.append(abs(abs(r) - e) / e)
    imC.append(abs(mp.im(gd_p)) / abs(gd_p))
check("F3-09 [numeric] causal dressing: KMS ratio BROKEN (dev > 2%) yet "
      "|ratio| preserved to machine precision (phase-only breaking)",
      max(devC) > mpf('0.02') and max(modC) < mpf('1e-10'),
      "max |ratio - e^{-bw}|/e^{-bw} = %s ; max modulus dev = %s"
      % (ns(max(devC)), ns(max(modC))))

# (10) ... and the dressed object is NOT a correlator: Im Ghat != 0
check("F3-10 [numeric] causal dressing violates hermiticity: max |Im Ghat_d|"
      "/|Ghat_d| > 2%  => not the Wightman function of ANY state",
      max(imC) > mpf('0.02'), "max Im fraction = %s" % ns(max(imC)))

# (11) the ONLY genuine evasion: Khat real, non-even => complex ACAUSAL K
KtA = lambda t: mpf('0.5') * mp.e**(-abs(t)) * mp.e**(-J * t)
ftA_dev = []
for wv in (mpf('-2'), mpf('0.7'), mpf('2')):
    num = mp.quad(lambda t: mp.e**(J * wv * t) * KtA(t), [-45, 0, 45],
                  maxdegree=10)
    ftA_dev.append(abs(num - KhA(wv)) / abs(KhA(wv)))
acaus = abs(KtA(mpf(-2)))          # = e^{-2}/2: support at tau < 0
herm_dev = max(abs(KtA(-tv) - mp.conj(KtA(tv)))
               for tv in (mpf('0.5'), mpf('2')))
check("F3-11 [numeric] Khat = 1/(1+(w-1)^2) <-> K = (1/2)e^{-|tau|}e^{-i tau}"
      " (FT verified): hermitian, COMPLEX, ACAUSAL (|K(-2)| = e^-2/2 > 0)",
      max(ftA_dev) < mpf('1e-10') and acaus > mpf('0.01')
      and herm_dev < mpf('1e-18'),
      "max FT rel err = %s ; |K(-2)| = %s ; hermiticity dev = %s"
      % (ns(max(ftA_dev)), ns(acaus), ns(herm_dev)))

devA, imA, reA = [], [], []
for wv in WS:
    gd_p = Gq[float(wv)] / (1 - q2 * KhA(wv))
    gd_m = Gq[float(-wv)] / (1 - q2 * KhA(-wv))
    e = mp.e**(-BETA1 * wv)
    devA.append(abs(gd_m / gd_p - e) / e)
    imA.append(abs(mp.im(gd_p)) / abs(gd_p))
    imA.append(abs(mp.im(gd_m)) / abs(gd_m))
    reA.append(mp.re(gd_p))
    reA.append(mp.re(gd_m))
check("F3-12 [numeric] that acausal kernel DOES break KMS (dev > 2%) while "
      "Ghat_d stays real and positive -- so the loophole costs CAUSALITY, "
      "nothing less", max(devA) > mpf('0.02') and max(imA) < mpf('1e-10')
      and min(reA) > 0,
      "max KMS dev = %s ; max Im fraction = %s ; min Re = %s"
      % (ns(max(devA)), ns(max(imA)), ns(min(reA))))

print()
print("F3 THEOREM: a linear tau-convolution dressing with a REAL kernel that")
print("keeps G a correlator has Khat real+even  =>  KMS is INHERITED, exactly.")
print("Real causal kernels only break the PHASE and destroy hermiticity;")
print("the one genuine KMS-breaking class is complex+hermitian+ACAUSAL.")
print("=> NESS-by-LINEAR-resummation dies by theorem for physical kernels.")
print("   (Nonlinear / state-dependent kernels remain outside this theorem.)")

# ===========================================================================
print()
print("=" * 78)
print("PART 2 (F4): super-ohmic equilibrium sign, J(w) = eta_s w^s e^{-w/wc}")
print("=" * 78)

BETA2 = 2 * mp.pi          # beta = 2 pi / H, units H = 1


def integrand(x, s, wc):
    # J(w) coth(beta w/2) / w^2  with eta_s = 1  (sign question)
    return x**(s - 2) * mp.e**(-x / wc) / mp.tanh(BETA2 * x / 2)


def Ipart(s, w0, wc):
    w0 = mpf(w0)
    wc = mpf(wc)
    pts = [w0] + [p for p in (mpf('0.1'), mpf(1), wc) if p > w0] + [mp.inf]
    return mp.quad(lambda x: integrand(x, s, wc), pts, maxdegree=8)


def Iexact_ir_finite(s, wc):
    # w0 = 0, s >= 3:  coth = 1 + 2 sum_n e^{-n beta w}  =>
    # I = Gamma(s-1) wc^{s-1} + 2 Gamma(s-1) sum_n (1/wc + n beta)^{-(s-1)}
    wc = mpf(wc)
    g = mp.gamma(s - 1)
    tail = mp.nsum(lambda n: (1 / wc + n * BETA2)**(-(s - 1)), [1, mp.inf])
    return g * wc**(s - 1) + 2 * g * tail


# (13) pointwise positivity of the integrand (the P is vacuous: no pole in
# the interior of (0, inf); the only singularity is the IR endpoint)
wgrid = np.logspace(-6, 4, 4001)
coth = 1.0 / np.tanh(np.pi * wgrid)
minvals = []
for s in (1, 2, 3, 4):
    vals = wgrid**(s - 2) * np.exp(-wgrid / 100.0) * coth
    minvals.append(vals.min())
check("F4-13 [numeric] integrand J coth(beta w/2)/w^2 pointwise POSITIVE, "
      "s=1..4, w in [1e-6, 1e4] H (4001 log pts; no underflow-to-zero)",
      min(minvals) > 0.0,
      "min sampled value = %.3e (s=%d)" % (min(minvals),
                                           1 + int(np.argmin(minvals))))

# (14) exact IR-finite cross-checks, s = 3 and s = 4 (thermal part resolved:
# wc = 0.5 makes it 19% / 3.4% of the total, so the check bites)
dev3 = abs(Ipart(3, 0, 0.5) - Iexact_ir_finite(3, 0.5)) / Iexact_ir_finite(3, 0.5)
dev4 = abs(Ipart(4, 0, 0.5) - Iexact_ir_finite(4, 0.5)) / Iexact_ir_finite(4, 0.5)
check("F4-14 [numeric] s=3,4 IR-FINITE: quadrature == exact Matsubara series "
      "Gamma(s-1)[wc^{s-1} + 2 sum_n (1/wc + n beta)^{-(s-1)}]  (wc=0.5)",
      dev3 < mpf('1e-10') and dev4 < mpf('1e-10'),
      "rel dev s=3: %s ; s=4: %s" % (ns(dev3), ns(dev4)))

# (15) s=1 IR divergence: I ~ 1/(pi w0), slope -1 in log-log
I1a = Ipart(1, mpf('1e-4'), 100)
I1b = Ipart(1, mpf('1e-3'), 100)
slope = mp.log(I1a / I1b) / mp.log(mpf('1e-4') / mpf('1e-3'))
check("F4-15 [numeric] s=1 IR-divergent: d ln I / d ln w0 == -1 "
      "(I ~ 1/(pi w0); detector frequency w0 is a hard cutoff)",
      abs(slope + 1) < mpf('0.02'),
      "slope = %s ; I(w0=1e-4)=%s, I(1e-3)=%s" % (ns(slope), ns(I1a), ns(I1b)))

# (16) s=2 ALSO IR-divergent (log) -- coefficient 1/pi (= 2T/H units)
I2a = Ipart(2, mpf('1e-4'), 100)
I2b = Ipart(2, mpf('1e-3'), 100)
coef = (I2a - I2b) * mp.pi / mp.log(10)
check("F4-16 [numeric] s=2 ALSO IR-divergent (log), coefficient 1/pi: "
      "[I(w0)-I(10 w0)]*pi/ln10 == 1  (task sheet said only s=1 diverges)",
      abs(coef - 1) < mpf('0.01'), "coefficient/exact = %s" % ns(coef))

# (17) THE SIGN SCAN: s x w0 x wc, count non-positive results
neg = 0
ntot = 0
scan_min = mp.inf
for s in (1, 2, 3, 4):
    for w0 in ('1e-4', '1e-3', '1e-2', '1e-1', '1'):
        for wc in (10, 100, 1000):
            v = Ipart(s, mpf(w0), wc)
            ntot += 1
            if v <= 0:
                neg += 1
            if v < scan_min:
                scan_min = v
check("F4-17 [numeric] SIGN: delta_m integral > 0 at EVERY point of the scan "
      "s in {1,2,3,4} x w0 in {1e-4..1}H x wc in {10,100,1000}H  (%d quads)"
      % ntot, neg == 0 and ntot == 60,
      "non-positive count = %d / %d ; smallest value = %s (all in H units)"
      % (neg, ntot, ns(scan_min)))

# (18) footings -- report BOTH on every dimensional number
c_SI = 2.99792458e8
cHL = 5.4194e-10          # m/s^2, canonical
a0_can = 9.3614e-11
a0_alt = 1.13e-10
Zc = 5.7888100366
d1 = abs(a0_can * Zc - cHL) / cHL
rat = a0_alt / a0_can
d2 = abs(rat - 1.2082)
check("F4-18 [numeric] footing self-consistency: a0_can * Z == cH_Lambda ; "
      "a0_ALT/a0_can == 1.2082", d1 < 1e-3 and d2 < 2e-3,
      "rel dev a0*Z vs cH_L = %.2e ; ratio = %.5f (dev %.2e; ALT quoted to "
      "3 sig figs)" % (d1, rat, d2))

H_can = cHL / c_SI                    # 1/s
H_alt = H_can * 1.2082
beta_can = 2 * np.pi / H_can          # s
beta_alt = 2 * np.pi / H_alt

print()
print("Dimensional table (reference point w0 = 0.01 H, wc = 100 H, eta_s = 1;")
print("I_s has dimension w^{s-1}; SI value = I_s[H units] * H^{s-1}):")
print("  canonical: H = %.5e /s, beta_GH = %.5e s" % (H_can, beta_can))
print("  ALT:       H = %.5e /s, beta_GH = %.5e s" % (H_alt, beta_alt))
Iref = {}
for s in (1, 2, 3, 4):
    Iref[s] = Ipart(s, mpf('0.01'), 100)
    si_can = float(Iref[s]) * H_can**(s - 1)
    si_alt = float(Iref[s]) * H_alt**(s - 1)
    print("  s=%d: I = %-12s [H^%d]  -> SI canonical %.4e, ALT %.4e  [s^-%d]"
          % (s, ns(Iref[s], 7), s - 1, si_can, si_alt, s - 1))
print("Sign is footing-BLIND (positive-definite integrand); only the")
print("dimensional magnitude moves by (1.2082)^{s-1} between footings.")
print()
print("s=1 sensitivity to the detector frequency w0 (wc = 100 H):")
for w0 in ('1e-4', '1e-3', '1e-2', '1e-1', '1'):
    print("  w0 = %-5s H : I_1 = %s  (~ 1/(pi w0) + O(1))"
          % (w0, ns(Ipart(1, mpf(w0), 100), 7)))
print()
print("F4 VERDICT: no admissible s flips the sign in EQUILIBRIUM.  delta_m")
print("has the sign of eta_s for every s, w0, wc, footing: inertia INCREASE")
print("= ANTI-MOND.  The s-dependence CANNOT flip it (positivity is pointwise")
print("and the Caldeira-Leggett prefactor is s-independent).  The anti-MOND")
print("no-go GENERALISES to the whole (super-)ohmic family; the NESS detour")
print("was necessary -- and Part 1 kills its LINEAR implementation by theorem.")

# ===========================================================================
print()
npass = sum(RESULTS)
ntot_checks = len(RESULTS)
print("%d/%d checks held." % (npass, ntot_checks))
if npass != ntot_checks:
    sys.exit(1)
