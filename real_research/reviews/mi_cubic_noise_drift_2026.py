#!/usr/bin/env python3
r"""mi_cubic_noise_drift_2026.py -- LANE N1: THE CUBIC-ORDER NOISE-INDUCED DRIFT. DOES T(a) REACH THE MEAN
EQUATION OF MOTION, AND WITH WHAT COEFFICIENT?

THE QUESTION. mi_ctp_variational_2026.py (50/50, commit 5c676b09) proved that at Gaussian order the CTP mean
equation of motion has an a-INDEPENDENT kernel: the dS dissipation kernel (commutator) is exactly
state-independent, the noise kernel N = N_c omega coth(beta omega/2) carries ALL the temperature dependence,
and the CTP structure keeps the noise out of the mean EOM. Hence I(a) exactly linear, a_0 = 0, q = 0. That
script's own stated remaining address: the noise reaches the mean trajectory only at SECOND order in the noise,
through cubic CTP vertices, where a one-loop tadpole closed with the Keldysh propagator G_K puts
coth(beta omega/2) -- and with it T(a) = sqrt(a^2+H^2)/(2 pi) -- into the mean equation of motion. This script
executes that order.

WHAT IS PROVEN HERE, in order:

 (1) THE CHANNEL IS OPEN. With a MULTIPLICATIVE coupling g(z) = z + (lambda/2) z^2 (coupling depends on the
     trajectory), the cubic sector of the rotated CTP influence action classifies EXACTLY into
        z_q z_cl^2  : real coefficients, built ONLY from the commutator symbols A_ij (deterministic nonlinear
                      force vertices),
        z_q^2 z_cl  : purely imaginary coefficients, built ONLY from the noise symbols S_ij (noise-modulation
                      vertices) -- and this sector IS i*lambda * zc.zq S zq, the TRAJECTORY-DERIVATIVE of the
                      noise coupling g'(z) N g'(z), so d(noise)/d(trajectory) != 0 is exactly what feeds it,
        z_q^3       : real, A-only.
     The one-loop tadpole of the mean EOM (Wick contraction with the exact discrete propagators
     <zc zc> = B^{-1} S B^{-T} (the statistical/Keldysh block, S-carrying), <zc zq> = i B^{-1} (causal,
     lower-triangular), <zq zq> = 0) is NONZERO, REAL, and CARRIES THE NOISE SYMBOLS through BOTH channels:
     the z_q z_cl^2 vertices closed with G_K, and the z_q^2 z_cl vertices closed with the retarded response.
     The z_q^3 vertices contribute EXACTLY zero (<zq zq> = 0). So the Gaussian a_0 = 0 no-go is ORDER-LIMITED,
     precisely as the launchpad predicted: at cubic order the temperature enters the mean equation of motion.

 (2) THE INDUCED LAW HAS THE MOND STRUCTURE -- for the tadpole channel. The drift is
     I_ind(a) = f(T(a)) - f(T_GH) with f(T) = Int w(omega) coth(omega/(2T)) domega, T(a) = sqrt(a^2+H^2)/2pi:
     symbolically, I_ind -> [c1p/(2 pi)] a for a >> H (Newtonian, linear) and
     I_ind -> f'(T_GH) a^2/(4 pi H) for a << H (deep, a^2/H), with the a^0 and a^1 terms EXACTLY zero.
     That is Milgrom 1999's f(T)-difference structure, emerging from a loop rather than a postulate.
     (The OTHER sub-channel, dN/da closed with the response, is NOT MOND: its force goes like a for a << H and
     saturates to a CONSTANT for a >> H -- powers (1, 0) against MOND's (2, 1). Reported as found.)

 (3) *** BUT THE COEFFICIENT IS PRICED, AND IT EXCLUDES kappa = 1/2 FROM THIS CHANNEL. *** Via the master
     formula (mi_crossover_master_formula_2026.py): per spectral mode, r = f'(T_GH)/c1p = x^2/sinh^2(x) with
     x = pi omega/H, which is STRICTLY BELOW 1 and reaches 1 only as x -> 0. Any POSITIVE spectral weight
     w(omega) >= 0 (and the sign choice that makes the induced Newtonian inertia positive forces one-signed w)
     gives r = a weighted mean of x^2/sinh^2 x, hence r < 1 STRICTLY, hence q = 2/r > 2, hence
        a_0(channel) > 2 c H_Lambda = 1.0839e-9 m/s^2   (canonical footing; ALT footing 2 c H_0 = 1.3096e-9).
     The IR boundary r -> 1 IS Milgrom 1999 eq 8 (a_0_hat = 2 c H_Lambda) -- the tadpole channel lands on HIS
     coefficient, not the framework's. kappa = 1/2 needs r = 2Z = 11.578: excluded by a factor >= 11.58 (both
     footings, 11.578 canonical / 11.589 ALT). AGAINST EVERY CAMP EQUALLY: Milgrom's conventional r = 4 pi and
     his eq 10 r = 2 are ALSO > 1 and also excluded; and since the observed a_0 ~ 1.1e-10 is ~10x BELOW the
     channel floor, this channel overshoots EVERYONE, including the boundary value it selects.

 (4) THE m_0 WALL, three roles for one parameter. The loop propagators DIVERGE as m_0 -> 0 (every <zc zc>
     entry has an m_0 power in its denominator; B is singular at m_0 = 0): the tadpole NEEDS the local kinetic
     term. Ghost-freedom needs the same m_0 != 0 (launchpad F4/F4b). But the FULL mean-EOM law is
     I_full(a) = m_0 a + c I_ind(a), whose small-a leading power is 1 for ANY m_0 > 0: the bare linear term
     always dominates the induced a^2. Deep MOND requires m_0 = 0 EXACTLY -- which kills the propagator and
     the ghost constraint simultaneously. So the channel that finally carries T(a) into the mean EOM cannot
     also deliver the deep-MOND limit: the full law has powers (1, 1) -- Newtonian at both ends with an
     a_0-scale crossover and an inner renormalized-Newton regime G_eff/G = 1 + c c1p/(2 pi m_0).

 (5) OSTROGRADSKY: the mean equation of motion stays SECOND order (the drift enters as a nonlinear function
     of z-ddot -- quasi-linear ODE, nondegenerate since m_0 + Phi'(a) > 0). The 4th-order derivatives that the
     acceleration-dependent vertex does generate live entirely in the CONSTRAINT sector (the z_cl-variation),
     every such term carries a factor of z_q, and z_q = 0 on the mean -- enforced, again, by m_0 != 0.

 (6) PARITY CAVEAT, stated against interest of the mechanism: I_ind depends on a only through a^2 (T is even
     in a), so the drift is a force-MAGNITUDE law, even under a -> -a. An inertia law must be odd along the
     worldline direction; the vector completion of this scalar structure is exactly where the corpus's
     established torsion/(v/c)^2 no-go lives (orbital motion). Nothing here evades that wall.

 *** kappa = 1/2 IS FITTED, NOT DERIVED. Nothing here derives it -- the OPPOSITE: this script prices the
 first channel that actually delivers a temperature-dependent mean EOM, and the price q > 2 is on the wrong
 side of the needed q = 1/Z = 0.1727 by more than an order of magnitude, BOTH footings (canonical
 a_0/cH_Lambda = 0.17274, ALT a_0/cH_0 = 0.17258). The apparent IR "selection" of r = 1 is a BOUNDARY of an
 inequality, not a derivation, and the value it selects is Milgrom 1999 eq 8's 2cH_Lambda, not kappa = 1/2. ***

MANDATORY CREDIT. nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9 (his eq 8
fixes a_0_hat = 2 c H_Lambda, i.e. r = 1 -- the boundary value this channel approaches); his eqs 10-11 give a
second coefficient (r = 2); Milgrom 2008 arXiv:0801.3133 sec 7.3.1 notes the mismatch "isn't necessarily
meaningful". a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. T = sqrt(a^2 + Lambda/3)/(2 pi):
Narnhofer, Peter & Thirring 1996 IJMPB 10:1507; five-acceleration: Deser & Levin 1997 CQG 14:L163. Influence
functional: Feynman & Vernon 1963; Caldeira & Leggett 1983 (whose position-nonlinear coupling expansion this
follows). CTP: Schwinger 1961, Keldysh 1964. Multiplicative noise and noise-induced drift in open systems:
Hu & Verdaguer (stochastic gravity). The framework's distinctive content is the COEFFICIENT
a_0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 -- which this channel does NOT produce.

MUTATION TESTS (five, inline, each trips its intended check when activated): (M1) corrupt <zq zq> = 0 to S ->
the z_q^3 sector contributes and B5's zero fails; (M2) Fermi bath (tanh for coth) -> c1p = 0, no Newtonian
limit, the r-identity fails (D4); (M3) freeze T (beta constant) -> dN/da = 0, the drift vertex vanishes (B8b);
(M4) signed spectral weight -> r > 1 explicitly, so the r < 1 cap is POSITIVITY-owned and the escape is an
active bath, the same locator as the launchpad's E6b (D5); (M5) conflate the branches (GFbar := GF) -> the CTP
normalisation S[z,z] = 0 fails for the nonlinear coupling too (A1b).

FLOAT64 HAZARDS honoured: all coth integrals in mpmath at dps = 30; the deep-limit slopes measured at
a/H = 1e-6 where cancellation f(T(a)) - f(T_G) is benign at dps 30; grid/precision refinement shown (D6).
Exit 0 = every check held. Every check can fail: the negative controls prove the machinery bites.
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict

import mpmath as mp
import numpy as np
import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


# framework constants -- BOTH footings carried throughout
A0_CAN = 9.3614e-11          # m/s^2, kappa = 1/2, FITTED not derived
CH_LAMBDA = 5.4194e-10       # m/s^2, canonical temperature floor
INV_SQRT_OL = 1.2082         # 1/sqrt(Omega_Lambda)
A0_ALT = 1.13e-10            # m/s^2, ALT footing (rho_total, cH_0)
CH_0 = CH_LAMBDA * INV_SQRT_OL
Z_NUM = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
TWO_Z = 2.0 * Z_NUM

banner("PART A  THE CUBIC CTP ACTION: MULTIPLICATIVE COUPLING, VERTEX CLASSIFICATION")

n = 4
lam = sp.Symbol("lambda", real=True)     # g''(zbar): the trajectory-derivative of the coupling
zp = sp.Matrix(sp.symbols(f"zp0:{n}", real=True))
zm = sp.Matrix(sp.symbols(f"zm0:{n}", real=True))
Ssym = sp.zeros(n, n)
Asym = sp.zeros(n, n)
S_syms, A_syms = [], []
for i in range(n):
    for j in range(i, n):
        s = sp.Symbol(f"S{i}{j}", real=True)
        S_syms.append(s)
        Ssym[i, j] = s
        Ssym[j, i] = s
for i in range(n):
    for j in range(i + 1, n):
        a_ = sp.Symbol(f"A{i}{j}", real=True)
        A_syms.append(a_)
        Asym[i, j] = a_
        Asym[j, i] = -a_
Gp = Ssym + sp.I * Asym
Gm = Ssym - sp.I * Asym


def th(i, j):
    return sp.Integer(1) if i > j else (sp.Rational(1, 2) if i == j else sp.Integer(0))


GF = sp.Matrix(n, n, lambda i, j: th(i, j) * Gp[i, j] + th(j, i) * Gp[j, i])
GFb = sp.Matrix(n, n, lambda i, j: th(j, i) * Gp[i, j] + th(i, j) * Gp[j, i])


def g_of(x):
    """Multiplicative (trajectory-dependent) coupling: the bath couples to g(z), not to z."""
    return x + lam / 2 * x**2


def s_if(gfb, gfun):
    gp_ = sp.Matrix([gfun(zp[i]) for i in range(n)])
    gm_ = sp.Matrix([gfun(zm[i]) for i in range(n)])
    return sp.expand(sp.I / 2 * (gp_.T * GF * gp_ - gp_.T * Gm * gm_ - gm_.T * Gp * gp_ + gm_.T * gfb * gm_)[0, 0])


S_IF = s_if(GFb, g_of)
diag = {zm[i]: zp[i] for i in range(n)}
check(sp.simplify(S_IF.subs(diag)) == 0,
      "A1  CTP normalisation survives the NONLINEAR coupling: S_IF[z, z] = 0 identically with g(z) = z + "
      "(lambda/2) z^2 on both branches -- the classical-classical sector is empty at EVERY order in lambda, "
      "so no vertex of the form z_cl^k alone exists and no drift can appear at tree level")
S_IF_wrong = s_if(GF, g_of)          # M5: branch conflation
check(sp.simplify(S_IF_wrong.subs(diag)) != 0,
      "A1b MUTATION M5 TRIPS: conflating the branches (G_Fbar := G_F, the single-branch mistake) breaks the "
      "normalisation even here -- A1 is falsifiable, not a theta-function tautology")

zc = sp.Matrix(sp.symbols(f"zc0:{n}", real=True))
zq = sp.Matrix(sp.symbols(f"zq0:{n}", real=True))
rot = {}
for i in range(n):
    rot[zp[i]] = zc[i] + zq[i] / 2
    rot[zm[i]] = zc[i] - zq[i] / 2
S_rot = sp.expand(S_IF.subs(rot, simultaneous=True))

fields = list(zc) + list(zq)
P = sp.Poly(S_rot, *fields)
buckets = defaultdict(list)
for monom, coeff in P.terms():
    buckets[(sum(monom), sum(monom[n:]))].append((monom, sp.expand(coeff)))


def sector(tot, qd):
    out = sp.Integer(0)
    for monom, coeff in buckets.get((tot, qd), []):
        term = coeff
        for f_, e_ in zip(fields, monom):
            term *= f_**e_
        out += term
    return sp.expand(out)


def props(tot, qd):
    cs = [c for _, c in buckets.get((tot, qd), [])]
    hasS = any(any(s in c.free_symbols for s in S_syms) for c in cs)
    hasA = any(any(a in c.free_symbols for a in A_syms) for c in cs)
    allreal = all(sp.simplify(sp.im(c)) == 0 for c in cs)
    allimag = all(sp.simplify(sp.re(c)) == 0 for c in cs)
    return hasS, hasA, allreal, allimag, len(cs)

hS1, hA1_, re1, im1, n1 = props(3, 1)
hS2, hA2_, re2, im2, n2 = props(3, 2)
hS3, hA3_, re3, im3, n3 = props(3, 3)
check((3, 0) not in buckets and n1 > 0 and n2 > 0 and n3 > 0,
      f"A2  the cubic sector exists and classifies completely: z_q z_cl^2 ({n1} terms), z_q^2 z_cl ({n2}), "
      f"z_q^3 ({n3}), and NO pure-classical z_cl^3 term (consequence of A1)")
check(re1 and hA1_ and not hS1,
      "A3  the z_q z_cl^2 vertices (deterministic nonlinear force) are REAL and built ONLY from the "
      "commutator symbols A_ij -- not one of the 10 noise symbols appears. The dissipative sector supplies "
      "the vertex; the statistics will have to come from the LOOP")
check(im2 and hS2 and not hA2_,
      "A4  the z_q^2 z_cl vertices (noise modulation) are PURELY IMAGINARY and built ONLY from the noise "
      "symbols S_ij -- the exact cubic-order image of the launchpad's A8 (the z_q^2 block is the noise, and "
      "only the noise)")
check(re3 and hA3_ and not hS3,
      "A5  the z_q^3 vertices are real and A-only -- they can only close with <z_q z_q>, which Part B proves "
      "is exactly zero, so this class is structurally dead on arrival")

S3 = sector(3, 1) + sector(3, 2) + sector(3, 3)
S3_q1, S3_q2, S3_q3 = sector(3, 1), sector(3, 2), sector(3, 3)
check(sp.expand(S3.subs(lam, 0)) == 0 and sp.degree(sp.Poly(S3, lam)) == 1,
      "A6  the ENTIRE cubic sector is proportional to lambda = g''(zbar) = d(coupling)/d(trajectory): at "
      "lambda = 0 (linear coupling) every cubic vertex vanishes and the Gaussian no-go is exact. "
      "Multiplicative coupling is load-bearing, not decorative")
noise_id = sp.expand(sp.I * lam * sum(zc[j] * zq[j] * Ssym[j, k] * zq[k]
                                      for j in range(n) for k in range(n)))
check(sp.expand(S3_q2 - noise_id) == 0,
      "A7  *** THE NOISE-MODULATION SECTOR IS EXACTLY i lambda zc_j zq_j S_jk zq_k = (i/2) zq [d/dzbar of "
      "g'(zbar) S g'(zbar)] zq. *** The vertex that will feed the drift IS the trajectory-derivative of the "
      "noise kernel's coupling -- d(noise)/d(trajectory) != 0 is what opens the channel, exactly as the "
      "Gaussian-order script predicted")

banner("PART B  THE PROPAGATORS AND THE TADPOLE: THE NOISE REACHES THE MEAN EQUATION OF MOTION")

# Exact discrete propagators from the quadratic sector.  Causal quadratic operator B = m0*I + K_R with
# K_R = -2 A_ij strictly lower-triangular (the launchpad's B3 kernel); m0*I is the nondegenerate LOCAL kinetic
# term the launchpad's F4/F4b proved ghost-freedom requires.  Full quadratic form over v = (zc, zq):
#   S2 = zq.B.zc + (i/2) zq.S.zq   =>   M = [[0, B^T], [B, iS]],   <v v> = i M^{-1}.
m0 = sp.Symbol("m_0", positive=True)
KR = sp.Matrix(n, n, lambda i, j: -2 * Asym[i, j] if i > j else sp.Integer(0))
B = m0 * sp.eye(n) + KR
M2 = sp.zeros(2 * n, 2 * n)
M2[0:n, n:2 * n] = B.T
M2[n:2 * n, 0:n] = B
M2[n:2 * n, n:2 * n] = sp.I * Ssym
Minv = M2.inv()
Binv = B.inv()
qq_block = sp.simplify(Minv[n:2 * n, n:2 * n])
cc_block = Minv[0:n, 0:n]
cq_block = Minv[0:n, n:2 * n]
GK = sp.expand(Binv * Ssym * Binv.T)          # <zc zc> = i * cc_block = B^{-1} S B^{-T}, real
check(qq_block == sp.zeros(n, n),
      "B1  <z_q z_q> = 0 EXACTLY: the quantum-quantum block of the inverse quadratic form vanishes "
      "identically (largest-time / causality structure of Keldysh theory), for arbitrary S, A and m_0")
check(sp.simplify(cc_block - (-sp.I) * Binv * Ssym * Binv.T) == sp.zeros(n, n)
      and sp.simplify(cq_block - Binv) == sp.zeros(n, n),
      "B2  the other two blocks are exact: <zc zc> = i(M^-1)_cc = B^{-1} S B^{-T} -- the STATISTICAL "
      "(Keldysh) propagator G_K, the fluctuation-dissipation chain G_R N G_A, REAL and linear in the noise "
      "-- and <zc zq> = i B^{-1}, the response block")
check(all(sp.simplify(Binv[i, j]) == 0 for i in range(n) for j in range(i + 1, n))
      and all(any(s in sp.expand(GK[i, j]).free_symbols for s in S_syms)
              for i in range(n) for j in range(n)),
      "B3  B^{-1} is strictly CAUSAL (lower-triangular: the response never anticipates) and every entry of "
      "G_K carries noise symbols -- the statistical propagator is the coth-carrier of the loop")


def wick(expr, gqq=None):
    """Gaussian expectation of a field-quadratic expression; gqq!=None corrupts <zq zq> (mutation M1)."""
    out = sp.Integer(0)
    for monom, coeff in sp.Poly(sp.expand(expr), *fields).terms():
        d = sum(monom)
        if d != 2:
            continue                       # <field> = 0 around the mean; only full pairings survive
        ia, ib = [k for k, e in enumerate(monom) for _ in range(e)]
        ta, aa_ = ("c", ia) if ia < n else ("q", ia - n)
        tb, bb_ = ("c", ib) if ib < n else ("q", ib - n)
        if ta == "c" and tb == "c":
            out += coeff * GK[aa_, bb_]
        elif ta == "c" and tb == "q":
            out += coeff * sp.I * Binv[aa_, bb_]
        elif ta == "q" and tb == "c":
            out += coeff * sp.I * Binv[bb_, aa_]
        else:
            out += coeff * (gqq[aa_, bb_] if gqq is not None else 0)
    return sp.expand(out)


drift = [wick(sp.diff(S3, zq[i])) for i in range(n)]
drift_q1 = [wick(sp.diff(S3_q1, zq[i])) for i in range(n)]
drift_q2 = [wick(sp.diff(S3_q2, zq[i])) for i in range(n)]
drift_q3 = [wick(sp.diff(S3_q3, zq[i])) for i in range(n)]
hasS_full = all(any(s in d.free_symbols for s in S_syms) for d in drift)
real_full = all(sp.simplify(sp.im(d)) == 0 for d in drift)
check(all(d != 0 for d in drift) and hasS_full and real_full,
      "B4  *** THE HEADLINE: THE TADPOLE IS NONZERO, REAL, AND CARRIES THE NOISE. *** The one-loop mean "
      "equation of motion <dS3/dz_q,i> is a real drift force containing the noise symbols S_ij in every "
      "component. The temperature-carrying kernel, excluded from the mean EOM at Gaussian order BY STRUCTURE, "
      "enters at cubic order THROUGH THE LOOP. The launchpad's a_0 = 0 no-go is order-limited, exactly as it "
      "itself predicted")
check(all(d == 0 for d in drift_q3),
      "B5  the z_q^3 sector contributes EXACTLY ZERO to the drift (it needs <z_q z_q>, which B1 proved "
      "vanishes) -- a clean structural cancellation, proven not assumed")
GQQ_BAD = Ssym
check(any(wick(sp.diff(S3_q3, zq[i]), gqq=GQQ_BAD) != 0 for i in range(n)),
      "B5b MUTATION M1 TRIPS: corrupting <z_q z_q> from 0 to S makes the z_q^3 sector contribute -- B5's "
      "zero is the Keldysh block structure at work, not an accident of the vertices")
check(all(d != 0 and any(s in d.free_symbols for s in S_syms) for d in drift_q1[1:]),
      "B6  CHANNEL 1, the task's named tadpole: the z_q z_cl^2 vertices (A-built) closed with the KELDYSH "
      "propagator G_K = B^{-1} S B^{-T} give a nonzero S-carrying drift at every interior time -- the "
      "dissipative vertex reads the temperature out of the statistical loop")
check(all(d != 0 and any(s in d.free_symbols for s in S_syms) for d in drift_q2),
      "B7  CHANNEL 2: the z_q^2 z_cl noise-modulation vertices (S-built, = the trajectory-derivative of the "
      "noise coupling, A7) closed with the causal response i B^{-1} also feed the drift -- both open channels "
      "carry the noise, and only the z_q^3 channel dies")
check(all(sp.expand(d.subs(lam, 0)) == 0 for d in drift)
      and all(sp.expand(sum(drift) - sum(drift_q1) - sum(drift_q2) - sum(drift_q3)) == 0 for _ in [0]),
      "B8  the whole drift is proportional to lambda = g''(zbar) (it vanishes for a linear coupling, "
      "restoring the Gaussian no-go as it must) and decomposes exactly into the three sectors")
gk00 = sp.simplify(GK[0, 0])
check(sp.simplify(gk00 - S_syms[0] / m0**2) == 0 and B.subs(m0, 0).det() == 0,
      "B9  *** THE m_0 WALL, first sighting. *** G_K[0,0] = S_00/m_0^2 and B is SINGULAR at m_0 = 0 (strictly "
      "lower-triangular): the loop that carries the temperature DIVERGES without the local kinetic term -- "
      "the same nondegenerate m_0 the launchpad's F4/F4b proved ghost-freedom requires. Remember this m_0: "
      "Part C shows deep MOND needs it to VANISH")

# kernel-level statement of the SAME structure, in the continuum (launchpad D3-D5 extended to the vertex):
w_, bet, Nc, acc, Hf = sp.symbols("omega beta N_c a H", positive=True)
nB = 1 / (sp.exp(bet * w_) - 1)
comm = sp.simplify(Nc * w_ * (1 + nB) - Nc * w_ * nB)       # dissipation kernel
anti = sp.simplify(Nc * w_ * (1 + nB) + Nc * w_ * nB)       # noise kernel
beta_dS = 2 * sp.pi / sp.sqrt(acc**2 + Hf**2)
check(sp.simplify(sp.diff(comm.subs(bet, beta_dS), acc)) == 0
      and sp.simplify(sp.diff(anti.subs(bet, beta_dS), acc)) != 0,
      "B10 continuum kernel level: with T = sqrt(a^2+H^2)/(2 pi), d(dissipation)/da = 0 exactly "
      "(state-independence) while d(noise)/da != 0 -- so the ONLY trajectory-derivative vertex the dS bath "
      "offers is the noise one: dN/da is what feeds the drift, and nothing else can")
check(sp.simplify(sp.diff(anti.subs(bet, 2 * sp.pi / Hf), acc)) == 0,
      "B10b MUTATION M3 TRIPS: freeze the temperature (beta = 2 pi/H, no a-dependence) and dN/da = 0 -- the "
      "drift vertex is gone and the channel closes. The a-dependence of T is the entire mechanism")

banner("PART C  THE STRUCTURE TEST: IS THE INDUCED LAW MOND, AND AT WHAT r?")

a_s, H_s, w0_s, om_s, c_s = sp.symbols("a H w_0 omega c", positive=True)
Tv = sp.Symbol("T", positive=True)
T_of_a = sp.sqrt(a_s**2 + H_s**2) / (2 * sp.pi)
TG = H_s / (2 * sp.pi)
f_mode = w0_s * sp.coth(om_s / (2 * Tv))                 # one spectral mode of f(T) = Int w coth(omega/2T)
c1p = sp.limit(f_mode / Tv, Tv, sp.oo)
fpTG = sp.simplify(sp.diff(f_mode, Tv).subs(Tv, TG))
I_ind = f_mode.subs(Tv, T_of_a) - f_mode.subs(Tv, TG)    # the tadpole-channel induced inertia
check(sp.simplify(c1p - 2 * w0_s / om_s) == 0
      and sp.simplify(sp.limit(I_ind / a_s, a_s, sp.oo) - c1p / (2 * sp.pi)) == 0,
      "C1  NEWTONIAN LIMIT: coth(omega/2T) -> 2T/omega, so f is asymptotically LINEAR with slope "
      "c1p = 2 w_0/omega and I_ind -> [c1p/(2 pi)] a for a >> H. The induced inertia is linear in a -- the "
      "first MOND requirement, delivered symbolically")
ser = sp.series(I_ind, a_s, 0, 4).removeO()
coef0, coef1, coef2 = [sp.simplify(ser.coeff(a_s, k)) for k in (0, 1, 2)]
check(coef0 == 0 and coef1 == 0 and sp.simplify(coef2 - fpTG / (4 * sp.pi * H_s)) == 0
      and sp.simplify(coef2) != 0,
      "C2  DEEP LIMIT: the a^0 and a^1 terms are EXACTLY zero and I_ind = [f'(T_GH)/(4 pi H)] a^2 + O(a^4) "
      "-- const * a^2/H, the second MOND requirement. THE INDUCED PIECE HAS THE FULL MOND STRUCTURE "
      "(I -> const*a Newtonian, I -> const*a^2/H deep): Milgrom 1999's f(T)-difference form, produced by a "
      "loop instead of a postulate")
x_s = sp.Symbol("x", positive=True)
r_mode = sp.simplify(fpTG / c1p)
r_x = sp.simplify(r_mode.subs(om_s, 2 * TG * x_s))
check(sp.simplify(r_x - x_s**2 / sp.sinh(x_s)**2) == 0 and sp.limit(r_x, x_s, 0) == 1,
      "C3  THE MASTER FORMULA PRICES THE MODE: r = f'(T_GH)/c1p = x^2/sinh^2(x) with x = pi omega/H, "
      "EXACTLY, and r -> 1 as x -> 0 (the IR boundary). q = 2/r follows "
      "(mi_crossover_master_formula_2026.py, re-used not re-derived)")
sinh_gap = sp.series(sp.sinh(x_s) - x_s, x_s, 0, 6).removeO()
mp.mp.dps = 30            # float64 CANNOT resolve 1 - x^2/sinh^2(x) ~ x^2/3 below x ~ 1e-8 (corpus hazard)
xs_scan = ([mp.mpf(10)**e for e in np.linspace(-8, 0, 60)]
           + [mp.mpf(float(v)) for v in np.linspace(1.0, 60.0, 400)[1:]])
r_scan = [x * x / mp.sinh(x)**2 for x in xs_scan]
check(sp.simplify(sinh_gap.coeff(x_s, 3) - sp.Rational(1, 6)) == 0
      and all(r < 1 for r in r_scan)
      and all(r_scan[i] > r_scan[i + 1] for i in range(len(r_scan) - 1)),
      f"C4  r < 1 STRICTLY for every mode: sinh x - x = x^3/6 + ... > 0, and a dps-30 scan over x in "
      f"[1e-8, 60] ({len(r_scan)} points; float64 would round r(1e-8) to exactly 1) confirms r(x) < 1 "
      f"everywhere and strictly monotone decreasing (max r = 1 - {float(1 - r_scan[0]):.2e} at x = 1e-8). "
      f"The supremum r = 1 is a BOUNDARY, never attained. Any positive spectral weight w >= 0 averages r(x) "
      f"and stays STRICTLY below 1")
q_can = A0_CAN / CH_LAMBDA
q_alt = A0_ALT / CH_0
floor_can = 2.0 * CH_LAMBDA
floor_alt = 2.0 * CH_0
over_can = 2.0 / q_can
over_alt = 2.0 / q_alt
check(abs(q_can - 1 / Z_NUM) / (1 / Z_NUM) < 5e-4 and over_can > 11.5 and over_alt > 11.5,
      f"C5  *** THE PRICE, BOTH FOOTINGS. *** r < 1 => q = 2/r > 2 => a_0(channel) > 2 c H_Lambda = "
      f"{floor_can:.4e} m/s^2 canonical (ALT: 2 c H_0 = {floor_alt:.4e}). The framework needs q = "
      f"{q_can:.5f} = 1/Z canonical ({q_alt:.5f} ALT): the channel floor overshoots by {over_can:.3f}x "
      f"canonical / {over_alt:.3f}x ALT (= 2Z). kappa = 1/2 (r = 2Z = {TWO_Z:.3f}) is EXCLUDED from this "
      f"channel -- not mis-priced, unreachable")
r_sup = r_scan[0]         # keep as mpf: float() would round 1 - 3.3e-17 to exactly 1.0 (the same hazard)
check(r_sup < 1 and 2.0 > r_sup and 4 * math.pi > r_sup and TWO_Z > r_sup
      and floor_can / 1.2e-10 > 5.0 and floor_alt / 1.2e-10 > 5.0,
      f"C6  AGAINST EVERY CAMP EQUALLY: of the four reference coefficients r = 1 (Milgrom 1999 eq 8), 2 "
      f"(his eq 10), 4 pi = {4*math.pi:.3f} (conventional), 2Z = {TWO_Z:.3f} (kappa = 1/2), only r = 1 "
      f"touches the channel's closure [boundary, IR limit] -- the tadpole channel lands on MILGROM'S eq-8 "
      f"coefficient a_0 = 2 c H_Lambda = {floor_can:.3e}, which is ~10x above the OBSERVED a_0 ~ 1.1e-10. "
      f"The channel overshoots everyone, including the value it selects; it cannot be the whole story for "
      f"ANY camp, and it derives kappa = 1/2 for NO ONE")
I_full = m0 * a_s + c_s * I_ind
ser_full = sp.series(I_full, a_s, 0, 3).removeO()
Geff = sp.simplify(sp.limit(I_full / a_s, a_s, sp.oo) / m0)
check(sp.simplify(ser_full.coeff(a_s, 1) - m0) == 0 and sp.simplify(ser_full.coeff(a_s, 0)) == 0
      and sp.simplify(Geff - (m0 + c_s * c1p / (2 * sp.pi)) / m0) == 0,
      f"C7  *** THE m_0 WALL CLOSES. *** The full law I_full = m_0 a + c I_ind has small-a leading term "
      f"m_0 a for ANY m_0 > 0: the ghost-required bare kinetic term dominates the induced a^2 as a -> 0, so "
      f"the FULL law has powers (1, 1), NOT MOND's (2, 1) -- an inner renormalised-Newton regime with "
      f"G_eff/G = 1 + c c1p/(2 pi m_0). Deep MOND <=> m_0 = 0 <=> the loop diverges (B9) and the ghost "
      f"returns (launchpad F4b). One parameter, three roles, no assignment satisfies all three")
F_N = sp.diff(f_mode.subs(Tv, T_of_a), a_s)              # the dN/da-response sub-channel force
limN_inf = sp.simplify(sp.limit(F_N, a_s, sp.oo))
serN = sp.series(F_N, a_s, 0, 2)
check(sp.simplify(limN_inf - c1p / (2 * sp.pi)) == 0 and serN.coeff(a_s, 0) == 0
      and sp.simplify(serN.coeff(a_s, 1)) != 0,
      "C8  the OTHER sub-channel (dN/da closed with the response) reported as found: its force is "
      "d/da[f(T(a))] -- linear in a for a << H (an inertia renormalisation) and saturating to the CONSTANT "
      "c1p/(2 pi) for a >> H. Powers (1, 0) against MOND's (2, 1): NOT MOND. Only the G_K tadpole channel "
      "has the MOND structure")
a_r = sp.Symbol("a_r", real=True)
check(sp.simplify(T_of_a.subs(a_s, a_r) - T_of_a.subs(a_s, -a_r)) == 0,
      "C9  PARITY CAVEAT, against interest: T (hence I_ind) is EVEN in a, so the drift is a force-MAGNITUDE "
      "law; an inertia term must be odd along the worldline. The vector completion of this scalar structure "
      "is exactly the corpus's standing torsion/(v/c)^2 wall for orbits -- nothing here evades it, and the "
      "claim is limited to the magnitude structure accordingly")

banner("PART D  NUMERICAL CONFIRMATION AT dps = 30 (mpmath), WITH REFINEMENT")

mp.mp.dps = 30
H_num = mp.mpf(1)
TG_num = H_num / (2 * mp.pi)


def w_spec(om):
    return om * mp.e**(-om)


def f_of_T(T, kernel=mp.coth):
    return mp.quad(lambda om: w_spec(om) * kernel(om / (2 * T)), [0, 1, 10, mp.inf])


def T_num(a):
    return mp.sqrt(a * a + H_num * H_num) / (2 * mp.pi)


fTG = f_of_T(TG_num)
I_num = lambda a: f_of_T(T_num(a)) - fTG
a1, a2 = mp.mpf("1e-6"), mp.mpf("2e-6")
slope_deep = mp.log(I_num(a2) / I_num(a1)) / mp.log(2)
b1, b2 = mp.mpf("1e8"), mp.mpf("2e8")
slope_newt = mp.log(I_num(b2) / I_num(b1)) / mp.log(2)
check(abs(slope_deep - 2) < 1e-3 and abs(slope_newt - 1) < 1e-6,
      f"D1  the symbolic limits survive concrete quadrature (w = omega e^-omega, H = 1, dps 30): log-log "
      f"slope of I_ind is {float(slope_deep):.6f} at a/H ~ 1e-6 (deep: 2) and {float(slope_newt):.9f} at "
      f"a/H ~ 1e8 (Newtonian: 1). The MOND powers (2, 1) are real, not grid artefacts")
c1p_num = 2 * mp.quad(lambda om: w_spec(om) / om, [0, 1, 10, mp.inf])
fp_num = mp.diff(f_of_T, TG_num)
r_master = fp_num / c1p_num
r_weight = (mp.quad(lambda om: (w_spec(om) / om) * (mp.pi * om / H_num)**2 / mp.sinh(mp.pi * om / H_num)**2,
                    [0, 1, 10, mp.inf])
            / mp.quad(lambda om: w_spec(om) / om, [0, 1, 10, mp.inf]))
Ihat_c2 = (2 * mp.pi * I_num(a1) / c1p_num) / a1**2 * H_num
q_indep = 1 / Ihat_c2
check(abs(r_master - r_weight) / r_weight < 1e-10 and r_master < 1
      and abs(q_indep - 2 / r_master) / (2 / r_master) < 1e-3,
      f"D2  the master formula and the weighted-mode average agree to {float(abs(r_master-r_weight)/r_weight):.2e} "
      f"(r = {float(r_master):.12f} < 1), and the INDEPENDENT deep-limit extraction gives q = "
      f"{float(q_indep):.6f} against 2/r = {float(2/r_master):.6f}. This concrete positive weight prices at "
      f"q = {float(2/r_master):.3f} > 2, i.e. a_0 = {float(2/r_master)*CH_LAMBDA:.3e} m/s^2 canonical "
      f"({float(2/r_master)*CH_0:.3e} ALT) -- {float((2/r_master)/q_can):.1f}x the framework's own a_0")


def r_of_scale(s):
    s = mp.mpf(s)
    num = mp.quad(lambda om: mp.e**(-om / s) * (mp.pi * om)**2 / mp.sinh(mp.pi * om)**2, [0, s, 10 * s, mp.inf])
    den = mp.quad(lambda om: mp.e**(-om / s), [0, s, 10 * s, mp.inf])
    return num / den


r_scales = [r_of_scale(s) for s in ("0.001", "0.1", "1", "10")]
check(r_scales[0] > mp.mpf("0.9999") and all(r_scales[i] > r_scales[i + 1] for i in range(3))
      and all(r < 1 for r in r_scales),
      f"D3  the IR family w_s = omega e^(-omega/s): r(s) = {', '.join(f'{float(r):.6f}' for r in r_scales)} "
      f"for s = 0.001, 0.1, 1, 10 -- monotone in the IR direction, approaching the boundary r = 1 = MILGROM "
      f"1999 EQ 8 (a_0 = 2 c H_Lambda) as the weight concentrates at omega << H, and never crossing it")
fF = lambda T: f_of_T(T, kernel=mp.tanh)
c1pF = fF(mp.mpf(1e6)) / mp.mpf(1e6)
check(abs(c1pF) / c1p_num < 1e-6,
      f"D4  MUTATION M2 TRIPS: a FERMI bath (tanh for coth) has c1p = lim f/T = {float(c1pF):.2e} ~ 0 "
      f"(bosonic: {float(c1p_num):.3f}) -- f saturates instead of growing linearly, there is NO Newtonian "
      f"limit at all, and the master-formula identity has nothing to price. The bosonic KMS structure is "
      f"load-bearing for the MOND form itself")
r_mode_f = lambda x: x * x / mp.sinh(x)**2
r_mix = (r_mode_f(mp.mpf("0.1")) - mp.mpf("0.5") * r_mode_f(mp.mpf(5))) / (1 - mp.mpf("0.5"))
check(r_mix > 1,
      f"D5  MUTATION M4 TRIPS, and locates the only escape: a SIGNED spectral weight (+1 at x = 0.1, -0.5 at "
      f"x = 5) gives r = {float(r_mix):.4f} > 1 -- the cap r < 1 is owned by POSITIVITY of the weight, and "
      f"negative spectral weight at high frequency means an ACTIVE bath: the same escape hatch, and the same "
      f"passivity price, as the launchpad's E6b. Within a passive bath the cap stands")
mp.mp.dps = 50
fTG_50 = mp.quad(lambda om: om * mp.e**(-om) * mp.coth(om / (2 * TG_num)), [0, mp.mpf("0.5"), 1, 5, 10, 30, mp.inf])
shift = abs(fTG_50 - fTG) / fTG
mp.mp.dps = 30
check(shift < 1e-25,
      f"D6  REFINEMENT: f(T_GH) recomputed at dps 50 with a 6-segment split moves by {float(shift):.1e} "
      f"relative -- the quadrature is converged far beyond every tolerance used above")

banner("PART E  OSTROGRADSKY AT CUBIC ORDER")

t = sp.Symbol("t")
zf = sp.Function("z")(t)
Phi = sp.Function("Phi")
Fx = sp.Symbol("F_ext")


def max_order(expr, fn):
    orders = [d.derivative_count for d in expr.atoms(sp.Derivative) if d.expr == fn]
    return max(orders) if orders else 0


mean_eom = m0 * sp.diff(zf, t, 2) + Phi(sp.diff(zf, t, 2)) - Fx
phi_prime = lambda a: float(mp.diff(lambda aa: f_of_T(T_num(aa)) - fTG, mp.mpf(a)))
nondeg = all(1.0 + phi_prime(a) > 0 for a in (1e-3, 0.1, 1.0, 10.0, 1e3))
check(max_order(mean_eom, zf) == 2 and nondeg,
      "E1  the MEAN equation of motion stays SECOND order: the drift enters as Phi(z-ddot), a NONLINEAR "
      "function of the acceleration, not a higher derivative -- a quasi-linear second-order ODE, "
      "nondegenerate since m_0 + c Phi'(a) > 0 (checked numerically on the concrete weight across five "
      "decades; Phi' >= 0 for a passive weight, so any m_0 > 0 suffices). Ostrogradsky does not apply to the "
      "mean sector")
zcf = sp.Function("z_c")(t)
zqf = sp.Function("z_q")(t)
FF = sp.Function("F")
Lv = FF(sp.diff(zcf, t, 2)) * zqf**2
eq_c, eq_q = sp.euler_equations(Lv, [zcf, zqf], t)
expr_c = sp.expand((eq_c.lhs - eq_c.rhs).doit())
expr_q = sp.expand((eq_q.lhs - eq_q.rhs).doit())
ord_c = max_order(expr_c, zcf)
at_q0 = sp.simplify(expr_c.subs(zqf, 0).doit())
check(ord_c == 4 and at_q0 == 0 and sp.simplify(expr_q.subs(zqf, 0).doit()) == 0,
      f"E2  the acceleration-dependent vertex F(z_c-ddot) z_q^2 DOES generate 4th-order derivatives (order "
      f"{ord_c}) -- but every such term sits in the CONSTRAINT sector (the z_cl-variation, the advanced "
      f"equation for z_q) and carries a factor of z_q: at z_q = 0 the entire higher-derivative content "
      f"vanishes identically. z_q = 0 is enforced by the CTP boundary conditions plus m_0 != 0 (launchpad "
      f"F4) -- the SAME m_0 as B9 and C7. No Ostrogradsky dof propagates")

banner("WHAT THIS DOES AND DOES NOT ESTABLISH")
print(f"""  DELIVERED:
   - THE CHANNEL OPENS. At cubic order in the CTP action the noise kernel -- and with it the entire de
     Sitter-Unruh temperature T(a) -- reaches the mean equation of motion, through two channels (A-vertices
     closed with G_K; S-vertices closed with the response), while the z_q^3 channel dies exactly. The
     Gaussian-order a_0 = 0 no-go is ORDER-LIMITED, as the launchpad itself predicted. The drift is fed by
     d(noise)/d(trajectory) and by nothing else (B10): the vertex IS the trajectory-derivative of the noise
     coupling (A7).
   - THE INDUCED LAW IS MOND-STRUCTURED (tadpole channel): I_ind = f(T(a)) - f(T_GH), linear at a >> H,
     a^2/H at a << H with a^0 = a^1 = 0 exactly. Milgrom 1999's form, from a loop.
   - THE COEFFICIENT IS PRICED: r = weighted mean of x^2/sinh^2(x) < 1 STRICTLY for any passive (positive)
     spectral weight, q = 2/r > 2, a_0(channel) > 2cH_Lambda = {floor_can:.3e} m/s^2 (ALT {floor_alt:.3e}).
     The IR boundary is Milgrom 1999 eq 8, r = 1.

  AND WHAT IT COSTS, the honest headline:
   - kappa = 1/2 needs r = 2Z = {TWO_Z:.3f}: EXCLUDED from this channel by >= {over_can:.2f}x (canonical)
     / {over_alt:.2f}x (ALT). So are Milgrom's r = 2 and r = 4 pi. The channel overshoots even the observed
     a_0 ~ 1.1e-10 by ~10x. It derives nobody's coefficient, and it CUTS AGAINST kappa = 1/2 exactly as
     hard as against the competition.
   - THE m_0 WALL: the loop needs m_0 != 0 (B9), ghost-freedom needs m_0 != 0 (launchpad F4b), deep MOND
     needs m_0 = 0 (C7). The full law has powers (1, 1) with an inner renormalised-Newton regime -- NOT MOND.
   - The dN/da sub-channel is not MOND at all: powers (1, 0).
   - PARITY: the drift is even in a -- a magnitude law; the odd/vector completion is the standing torsion
     wall, untouched.
   - kappa = 1/2 REMAINS FITTED, NOT DERIVED. This script moves the frontier by pricing the first
     temperature-carrying channel -- and the price excludes the fitted value from this channel.""")

banner("RESULT")
nOK = sum(1 for c, _ in ok if c)
print(f"  {nOK}/{len(ok)} checks held.")
if nOK != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. The cubic tadpole puts T(a) into the mean equation of motion (the Gaussian no-go is")
print("  order-limited); the induced law has the exact MOND structure; and the coefficient it prices is")
print("  r < 1 -- the boundary is Milgrom 1999 eq 8, and kappa = 1/2's r = 2Z is excluded from this channel")
print("  by >= 11.6x on both footings. The bare-mass/ghost constraint blocks the deep-MOND limit of the")
print("  full law. kappa = 1/2 remains FITTED, NOT DERIVED.")
