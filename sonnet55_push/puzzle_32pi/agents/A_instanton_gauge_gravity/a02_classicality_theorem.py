#!/usr/bin/env python3
"""a02: can an instanton-number / quantisation condition EVER reach a0?   A structural (dimensional-analysis) theorem, scripted.

Quantities: a0 (acceleration), Lambda (1/length^2), G, hbar, c.   Dimension matrix over (M, L, T) has rank 3 for 5 quantities => exactly TWO
independent dimensionless groups:
      Pi_1 = a0^2 /(c^4 Lambda)          (the puzzle: Pi_1 = 1/(32 pi), no G, no hbar: a CLASSICAL relation)
      Pi_2 = hbar G Lambda / c^3         (= l_P^2 Lambda = 3 l_P^2/L^2 ; the ONLY group containing hbar)
Every instanton / gauge-gravity quantity of the de Sitter theory is a function of Pi_2 and integers (a01):
      g^2 = (16 pi/3) Pi_2,  8 pi^2/g^2 = 3 pi/(2 Pi_2),  S_dS = 3 pi/Pi_2,  S_a0 = pi c^... /(4 Pi_1 Pi_2) (area/(4 hbar G)).
THEOREM (scoped, T1-T7).  Any instanton/quantisation input of the form  Pi_1 = phi(Pi_2; integers):
   (a) if phi depends on g through a power g^p (perturbative) or e^{-8 pi^2 k/g^2} (instanton weight), it is excluded by the observed
       Pi_2 ~ 3e-122 (Pi_1 is O(1e-2)): p must be 0 or the coefficient tuned to 10^{60|p|};   e^{-8 pi^2 k/g^2} ~ e^{-10^{122}} gives 0;
   (b) so the ONLY instanton content that can appear in the puzzle's relation is a Pi_2-INDEPENDENT number (32 pi^2 chi etc.): a coefficient,
       not a quantisation.  A quantisation condition k in Z acts on 1/g^2 = a function of Pi_2 (it quantises Lambda in Planck units);
   (c) integer quantisation of BOTH S_dS and S_a0 gives Pi_1 = M/(12 N) (rational) -- but the lattice is 1e-122 dense, so it cannot select an O(1) value;
   (d) in the framework's own form a0 = (1/2) c sqrt(G rho_Lambda), any mechanism (QCD instantons, condensates ...) that sets rho_Lambda moves a0 and Lambda
       together: Pi_1 = 1/(32 pi) is independent of rho_Lambda.
Exit 0 = all checks and controls behave.
"""
import sys
import sympy as sp
import mpmath as mp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- T1 Buckingham pi
# exponent vectors (M, L, T)
dims = {'a0': (0, 1, -2), 'Lam': (0, -2, 0), 'G': (-1, 3, -2), 'hbar': (1, 2, -1), 'c': (0, 1, -1)}
names = list(dims)
Dm = sp.Matrix([[dims[n][i] for n in names] for i in range(3)])
chk("T1 dimension matrix of (a0, Lambda, G, hbar, c) has rank 3", Dm.rank() == 3)
null = Dm.nullspace()
chk("T1 exactly two independent dimensionless groups (nullspace dimension 2)", len(null) == 2)
def expo(vec): return sp.Matrix(vec)
P1 = sp.Matrix([2, -1, 0, 0, -4])      # a0^2 Lambda^-1 c^-4
P2 = sp.Matrix([0, 1, 1, 1, -3])       # Lambda G hbar c^-3
chk("T1 Pi_1 = a0^2/(c^4 Lambda) and Pi_2 = hbar G Lambda/c^3 are dimensionless", Dm * P1 == sp.zeros(3, 1) and Dm * P2 == sp.zeros(3, 1))
Nsp = sp.Matrix.hstack(*null)
sub = Nsp[[0, 3], :]          # rows = exponents of (a0, hbar) of the two nullspace vectors
half_P1 = sp.Matrix([1, sp.Rational(-1, 2), 0, 0, -2])          # Pi_1^(1/2) = a0/(c^2 sqrt(Lambda)) = a0 L/c^2 up to sqrt3
chk("T1 every dimensionless monomial is labelled by its (a0, hbar) exponents: the (a0, hbar) minor of the nullspace is invertible, and Pi_1^(1/2), Pi_2 have labels (1,0), (0,1)",
    sub.det() != 0 and Dm * half_P1 == sp.zeros(3, 1) and (half_P1[0], half_P1[3], P2[0], P2[3]) == (1, 0, 0, 1))
chk("T1 Pi_2 is the ONLY group containing hbar (Pi_1 has exponent 0 on hbar and on G)", P1[2] == 0 and P1[3] == 0 and P2[3] == 1)

# ---------------------------------------------------------------- T2 the puzzle is Pi_2-independent
a0, Lam, G, hb, c = sp.symbols('a0 Lambda G hbar c', positive=True)
a0_of = sp.solve(sp.Eq(Lam, 32 * sp.pi * a0 ** 2 / c ** 4), a0)[0]          # the puzzle Lambda = 32 pi a0^2 (c^4 restored)
chk("T2 puzzle a0 = c^2 sqrt(Lambda/32 pi): no G and no hbar (classical)", sp.diff(a0_of, G) == 0 and sp.diff(a0_of, hb) == 0)
rho = sp.symbols('rho', positive=True)
a0_fw = sp.Rational(1, 2) * c * sp.sqrt(G * rho)                              # framework: a0 = (1/2) c sqrt(G rho_Lambda)
Lam_of_rho = 8 * sp.pi * G * rho / c ** 2                                     # Einstein: Lambda = 8 pi G rho/c^2
Pi1_fw = sp.simplify(a0_fw ** 2 / (c ** 4 * Lam_of_rho))
chk("T7(d) with a0 = (1/2) c sqrt(G rho) and Lambda = 8 pi G rho/c^2: Pi_1 = 1/(32 pi) for EVERY rho: whatever sets rho_Lambda cannot move Pi_1",
    sp.simplify(Pi1_fw - 1 / (32 * sp.pi)) == 0 and sp.diff(Pi1_fw, rho) == 0)
Pi1_fw_mut = sp.simplify((sp.Rational(1, 2) * c * sp.sqrt(G * rho) * rho ** sp.Rational(1, 4)) ** 2 / (c ** 4 * Lam_of_rho))
chk("T7(d)-control: if a0 carried an extra rho^(1/4) the ratio WOULD depend on rho (so the test can fail)", sp.diff(Pi1_fw_mut, rho) != 0)

# ---------------------------------------------------------------- T3 instanton quantities are functions of Pi_2 only
L2 = 3 / Lam                                                                   # L^2 = 3/Lambda
g2 = 16 * sp.pi * hb * G / (c ** 3 * L2)                                       # a01: g^2 = 16 pi hbar G/(c^3 L^2)
Pi2 = hb * G * Lam / c ** 3
chk("T3 g^2 = (16 pi/3) Pi_2  (a01)", sp.simplify(g2 - sp.Rational(16, 3) * sp.pi * Pi2) == 0)
chk("T3 8 pi^2/g^2 = 3 pi/(2 Pi_2),  S_dS = pi L^2 c^3/(hbar G) = 3 pi/Pi_2 : both functions of Pi_2 ONLY",
    sp.simplify(8 * sp.pi ** 2 / g2 - 3 * sp.pi / (2 * Pi2)) == 0 and sp.simplify(sp.pi * L2 * c ** 3 / (hb * G) - 3 * sp.pi / Pi2) == 0)
Pi1 = sp.symbols('Pi1', positive=True)
A_a0 = sp.pi * c ** 4 / a0 ** 2                                                # Schwarzschild with surface gravity a0: r_s = c^2/(2 a0), A = 4 pi r_s^2
S_a0 = A_a0 * c ** 3 / (4 * hb * G)                                            # Bekenstein-Hawking S/k_B = A c^3/(4 hbar G)
Pi1_expr = a0 ** 2 / (c ** 4 * Lam)
chk("T3 S_a0 = pi/(4 Pi_1 Pi_2)  (depends on BOTH groups: it is not an instanton-only quantity)", sp.simplify(S_a0 - sp.pi / (4 * Pi1_expr * Pi2)) == 0)

# ---------------------------------------------------------------- T4 observed numbers
mp.mp.dps = 30
hbar_v, G_v, c_v = mp.mpf('1.054571817e-34'), mp.mpf('6.67430e-11'), mp.mpf('299792458')
Lam_v = mp.mpf('1.1e-52')                    # m^-2, order of magnitude of the observed cosmological constant (Planck-like)
a0_v = mp.mpf('1.2e-10')                     # m s^-2, order of magnitude of the SPARC/MOND scale (observational input, quoted to 1 digit)
Pi2_v = hbar_v * G_v * Lam_v / c_v ** 3
Pi1_v = a0_v ** 2 / (c_v ** 4 * Lam_v)
print("   observed (order of magnitude): Pi_2 = %s,  Pi_1 = %s (puzzle value 1/(32 pi) = %s),  8 pi^2/g^2 = %s" %
      (mp.nstr(Pi2_v, 3), mp.nstr(Pi1_v, 3), mp.nstr(1 / (32 * mp.pi), 3), mp.nstr(3 * mp.pi / (2 * Pi2_v), 3)))
chk("T4 Pi_2 ~ 3e-122 (so g^2 ~ 1e-121: the gravitational 'instanton weight' e^{-8 pi^2/g^2} = e^{-1e122})", 1e-123 < Pi2_v < 1e-121 and 3 * mp.pi / (2 * Pi2_v) > mp.mpf('1e121'))
chk("T4 Pi_1 is O(1e-2) at that Pi_2 (a0 ~ c H0/ (2 pi..6) is the empirical statement Pi_1 ~ 1e-2 with Pi_2 ~ 1e-122)", mp.mpf('1e-3') < Pi1_v < mp.mpf('1e-1'))

# ---------------------------------------------------------------- T5 power laws / instanton weights in g are excluded
lg2 = mp.log10(Pi2_v)
def p_window(logC_lo, logC_hi, Pi1_lo, Pi1_hi):
    # Pi_1 = C Pi_2^p  ->  p = (log10 Pi_1 - log10 C)/log10 Pi_2
    ps = [(mp.log10(P) - lc) / lg2 for P in (Pi1_lo, Pi1_hi) for lc in (logC_lo, logC_hi)]
    return min(ps), max(ps)
lo, hi = p_window(-3, 3, mp.mpf('1e-3'), mp.mpf('1e-1'))
print("   allowed exponent window for Pi_1 = C Pi_2^p, |log10 C| <= 3, Pi_1 within [1e-3, 1e-1]:  p in [%s, %s]" % (mp.nstr(lo, 3), mp.nstr(hi, 3)))
chk("T5 a coefficient C within 10^{+-3} allows only |p| < 0.05: no perturbative g^p with |p| >= 1/2 (or 1, 2, 4...) can reproduce Pi_1", max(abs(lo), abs(hi)) < 0.05)
need = [(p, (mp.log10(mp.mpf('0.00995')) - p * lg2)) for p in (mp.mpf('0.5'), 1, 2)]
print("   coefficient needed: " + ", ".join("p=%s -> C ~ 10^%s" % (mp.nstr(p, 2), mp.nstr(v, 4)) for p, v in need))
chk("T5 for p = 1/2, 1, 2 the required C is 10^+60, 10^+120, 10^+240 (tuning) ", abs(need[0][1] - 60) < 2 and abs(need[1][1] - 120) < 2 and abs(need[2][1] - 240) < 3)
chk("T5 the k-instanton weight e^{-8 pi^2 k/g^2} = exp(-%s k) underflows to 0: cannot be an O(1) coefficient" % mp.nstr(3 * mp.pi / (2 * Pi2_v), 3), 3 * mp.pi / (2 * Pi2_v) > 1e100)
# control: the argument has teeth only because Pi_2 is tiny -- for an O(1) coupling the same window is wide open
Pi2_ctrl = mp.mpf('0.3'); lgc = mp.log10(Pi2_ctrl)
ps = [(mp.log10(P) - lc) / lgc for P in (mp.mpf('1e-3'), mp.mpf('1e-1')) for lc in (-3, 3)]
chk("T5-control: at an O(1) coupling Pi_2 = 0.3 the window is |p| ~ 10 (NOT excluded): the exclusion comes from the observed Pi_2, as claimed", max(abs(p) for p in ps) > 5)

# ---------------------------------------------------------------- T6 integer quantisation of both entropies gives a rational Pi_1 (and a dense lattice)
M, N = sp.symbols('M N', positive=True, integer=True)
Pi2_q = sp.solve(sp.Eq(3 * sp.pi / sp.Symbol('P2', positive=True), M), sp.Symbol('P2', positive=True))[0]       # S_dS = M
Pi1_q = sp.solve(sp.Eq(sp.pi / (4 * sp.Symbol('P1', positive=True) * Pi2_q), N), sp.Symbol('P1', positive=True))[0]   # S_a0 = N
chk("T6 S_dS = M, S_a0 = N (integers) => Pi_1 = M/(12 N): RATIONAL", sp.simplify(Pi1_q - M / (12 * N)) == 0)
chk("T6 the puzzle's 1/(32 pi) is irrational (Lindemann) -- integer-integer quantisation cannot hit it exactly", not sp.nsimplify(1 / (32 * sp.pi)).is_rational)
mp.mp.dps = 400
target = 1 / (32 * mp.pi)
M0 = 3 * mp.pi / Pi2_v                        # ~ S_dS ~ 1e122
# best rational approximations M/(12N) to 1/(32 pi) with 12 N ~ 1e61.. via continued fraction convergents of 12*target^-1 ... use identify
def best_rational(x, maxden):
    return mp.identify(x) if False else None
# continued-fraction convergents of the target
def convergents(x, n):
    a = []; y = x
    for _ in range(n):
        ai = int(mp.floor(y)); a.append(ai); fr = y - ai
        if fr < mp.mpf(10) ** (-100): break
        y = 1 / fr
    h0, h1, k0, k1 = 0, 1, 1, 0
    out = []
    for ai in a:
        h0, h1 = h1, ai * h1 + h0
        k0, k1 = k1, ai * k1 + k0
        out.append((h1, k1))
    return out
cv = convergents(target, 300)
den_big = [(p, q) for p, q in cv if q > 10 ** 60][0]
err = abs(target - mp.mpf(den_big[0]) / den_big[1])
print("   a rational p/q with q ~ 1e60 approximates 1/(32 pi) to %s (lattice spacing at S ~ 1e122 is ~1e-122)" % mp.nstr(err, 3))
chk("T6 integers of size S ~ 1e122 approximate ANY O(1) target to ~1e-122: a quantisation lattice this dense cannot single out 1/(32 pi)", err < mp.mpf('1e-118'))
chk("T6-control: the same procedure on a rational target (7/12) terminates exactly (continued fraction ends): the test distinguishes rational from irrational",
    len(convergents(mp.mpf(7) / 12, 30)) <= 6 and convergents(mp.mpf(7) / 12, 30)[-1] == (7, 12))

# ---------------------------------------------------------------- T7(b): what an instanton quantisation quantises
kk = sp.symbols('k', positive=True, integer=True)
Pi2_of_k = sp.solve(sp.Eq(3 * sp.pi / (2 * sp.Symbol('P2', positive=True)), kk * 1), sp.Symbol('P2', positive=True))[0]
chk("T7(b) setting the instanton action 8 pi^2/g^2 = k (integer) fixes Pi_2 = 3 pi/(2k): it quantises Lambda in Planck units (hbar G Lambda) and says nothing about Pi_1",
    sp.simplify(Pi2_of_k - 3 * sp.pi / (2 * kk)) == 0)
print("\n   VERDICT of the theorem: instanton data enter only through Pi_2; the puzzle is a statement about Pi_1; the only admissible instanton content is a Pi_2-independent number.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
