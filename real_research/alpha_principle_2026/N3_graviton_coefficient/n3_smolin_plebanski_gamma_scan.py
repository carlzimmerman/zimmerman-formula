#!/usr/bin/env python3
"""N3 -- Smolin, arXiv:0712.0977 (extended Plebanski action, any G containing SO(4)): g_YM^2 = G_N*Lambda*h(gamma)?  Is h a constant?
Source relations used AS PRINTED: (17) B^ab = Sigma^ab + gamma *Sigma^ab, (19) W = (1+2 gamma^2)/(24 gamma), (28)-(29) G_N = G/gamma, Lambda = (1+4 gamma^2+gamma^4)/(4g),
 (31) matter action, (32) B^i = g xi (F - 6 W *F), xi = 96/(1-36 W^2), (34) 1/g_YM^2 = (W xi/(G_N Lambda gamma))(1+4gamma^2+gamma^4)(3 - xi/48 + (3/8) xi W^2).
The source states gamma is arbitrary (must not vanish).  SO(4) Euclidean: *^2 = +1.
PART A  gravity-sector algebra of (26) with ansatz (17) (exact): W_der, potential structure -> compare with printed (19), (29).
PART B  matter sector: from (31) solve B^i; FOUR readings of the index sums (P: sums over a<b, eps B B = 4 sum_{a<b,c<d}; Q: sums over all a,b; each with/without a factor 1/2 on the B.F term).
PART C  h(gamma) = g_YM^2/(G_N Lambda) under three chains: as printed; matter re-derived (reading that reproduces (32)) + printed gravity; matter re-derived + gravity re-derived.
        Whether h is constant; sign; window; poles; maximum; tuning of gamma needed for alpha = 1/137.036 at the observed G_N Lambda.
Run:    python3 n3_smolin_plebanski_gamma_scan.py           (exit 0)
MUTATE: python3 n3_smolin_plebanski_gamma_scan.py MUTATE   (flips the sign of the eps B B term in (31); the check that the solution has the (F - 6 W *F)/(1 - 36 W^2) structure must FAIL -> exit 1)
"""
import sys
import sympy as sp
import mpmath as mp
from itertools import product

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok:
        fails.append(n)

gam, W, g, G = sp.symbols('gamma W g G', positive=True)
eps = sp.LeviCivita

# ---------------- PART A: gravity-sector algebra ----------------
# Euclidean: Sigma^{ab} ^ Sigma^{cd} = eps^{abcd} vol ; Sigma^{ab} ^ *Sigma^{cd} = (d^ac d^bd - d^ad d^bc) vol ; *Sigma ^ *Sigma = eps vol
def dl(a, b, c, d):
    return (1 if (a == c and b == d) else 0) - (1 if (a == d and b == c) else 0)
def BB(a, b, c, d):      # coefficient of vol in B^{ab}^B^{cd}, B = Sigma + gamma *Sigma
    return eps(a, b, c, d) * (1 + gam**2) + 2 * gam * dl(a, b, c, d)
den = sp.expand(sum(BB(a, b, a, b) for a, b in product(range(4), repeat=2)))
num = sp.expand(sum(BB(a, b, c, d)**2 for a, b, c, d in product(range(4), repeat=4)))
chk("(18): B^ab ^ B_ab = 24 gamma vol", sp.simplify(den - 24 * gam) == 0, str(den))
W_der = sp.simplify(sp.Rational(1, 24) * sum(eps(a, b, c, d) * BB(a, b, c, d) for a, b, c, d in product(range(4), repeat=4)) / (24 * gam) * 24 / 24)
# W is defined by B^ab^B^cd = (eps W + rho d) B^B => contract with eps_{abcd}/24: W = eps.BB /(24 * den)
W_der = sp.simplify(sum(eps(a, b, c, d) * BB(a, b, c, d) for a, b, c, d in product(range(4), repeat=4)) / (24 * den))
pot_struct = sp.simplify(num / den)          # (B^B)(B^B)/(B^B) in units of vol
print("   derived: W_der = %s ; (B^ab^B^cd)^2/(B^B) = %s vol" % (W_der, sp.factor(pot_struct)))
W_pr = (1 + 2 * gam**2) / (24 * gam)
Lam_pr_struct = 1 + 4 * gam**2 + gam**4
chk("printed (19) W = (1+2 gamma^2)/(24 gamma) is NOT reproduced (declared expectation: not)", sp.simplify(W_der - W_pr) != 0)
chk("printed (29) Lambda-structure (1+4gamma^2+gamma^4) is NOT reproduced: derived structure is (1+6gamma^2+gamma^4)/gamma", sp.simplify(pot_struct - (1 + 6 * gam**2 + gam**4) / gam) == 0)
Lam_der = sp.simplify((1 + 6 * gam**2 + gam**4) / (4 * g * gam**2))   # (gamma/G)(Lambda/2) = (1/G)(1/8g)(...)/gamma with G_N = G/gamma
print("   derived: Lambda_der = (1+6gamma^2+gamma^4)/(4 g gamma^2) [G_N = G/gamma kept: 1/G_N = gamma/G from the *Sigma^F term]")

# ---------------- PART B: matter sector ----------------
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
Star = sp.zeros(6, 6)
for i, (a, b) in enumerate(pairs):
    for j, (c, d) in enumerate(pairs):
        Star[i, j] = eps(a, b, c, d)
chk("Euclidean star^2 = +1 on the 6 independent 2-form components", Star * Star == sp.eye(6))
Fv = sp.Matrix(sp.symbols('f0:6'))
xi = 96 / (1 - 36 * W**2)
cand32 = g * xi * (Fv - 6 * W * Star * Fv)
sgn = -1 if MUT else 1
readings = {}
for nm, fac, t1 in (("P", 1, 1), ("P-half", 1, sp.Rational(1, 2)), ("Q", 2, 1), ("Q-half", 2, sp.Rational(1, 2))):
    Bv = sp.Matrix(sp.symbols('b0:6'))
    Lg = t1 * (Bv.T * Star * Fv)[0] - W / (64 * g) * fac * (Bv.T * Bv)[0] - sgn * 1 / (24 * 64 * g) * 4 * (Bv.T * Star * Bv)[0]
    sol = sp.solve([sp.diff(Lg, x) for x in Bv], list(Bv), dict=True)[0]
    Bs = sp.Matrix([sol[x] for x in Bv])
    # ratio to printed (32): constant?
    ratio = sp.simplify(Bs[0] / cand32[0]) if cand32[0] != 0 else None
    ok_struct = all(sp.simplify(Bs[k] - ratio * cand32[k]) == 0 for k in range(6)) and ratio is not None and not ratio.has(W)
    Lm = sp.expand(sp.simplify(Lg.subs(sol)))
    A = sp.simplify(sp.Poly(Lm, *list(Fv)).coeff_monomial(Fv[0]**2))
    xis = 96 / (1 - 36 * W**2)
    Apr = g * W * xis * (3 - xis / 48 + sp.Rational(3, 8) * xis * W**2)      # printed (34) numerator (up to the fixed factor 1/G etc.)
    rA = sp.simplify(A / Apr)
    readings[nm] = dict(Bs=Bs, A=A, ratio=ratio, ok=ok_struct, rA=rA)
    print("   reading %-7s: B_sol/(printed (32)) = %s ; structure (F-6W*F)/(1-36W^2): %s ; A/A_printed(34) = %s" % (nm, ratio, ok_struct, rA))
chk("some reading reproduces the (F - 6 W *F)/(1 - 36 W^2) structure of (32) with a W-independent factor", any(r["ok"] for r in readings.values()))
if not MUT:
    chk("reading P-half reproduces (32) EXACTLY (factor 1)", readings["P-half"]["ratio"] == 1)
    chk("printed (34) is NOT reproduced under the reading that reproduces (32): A/A_printed depends on W", readings["P-half"]["rA"].has(W))
    Aph = sp.simplify(readings["P-half"]["A"])
    chk("re-derived YM coefficient (reading P-half) = -(3/2) g W xi", sp.simplify(Aph + sp.Rational(3, 2) * g * W * xi) == 0, "A = %s" % sp.factor(Aph))
    brk = 3 - xi / 48 + sp.Rational(3, 8) * xi * W**2
    chk("identity: printed bracket (3 - xi/48 + (3/8) xi W^2) = (1 - 72 W^2)/(1 - 36 W^2), a W-dependent factor absent from the re-derivation",
        sp.simplify(brk - (1 - 72 * W**2) / (1 - 36 * W**2)) == 0)
    chk("printed/re-derived YM coefficient = -(2/3)(1-72W^2)/(1-36W^2): not constant", sp.simplify((g * W * xi * brk) / Aph + sp.Rational(2, 3) * (1 - 72 * W**2) / (1 - 36 * W**2)) == 0)

# ---------------- PART C: h(gamma) ----------------
Wg = W_pr
xig = 96 / (1 - 36 * Wg**2)
bracket = 3 - xig / 48 + sp.Rational(3, 8) * xig * Wg**2
h_pr = sp.simplify(gam / (Wg * xig * (1 + 4 * gam**2 + gam**4) * bracket))                 # printed chain: g_YM^2/(G_N Lambda)
# re-derived matter (reading P-half): canonical -(1/(4 g_YM^2)) F^{iab}F_iab with F.F(a<b) = (1/2) F^{iab}F_iab  =>  1/g_YM^2 = -2 A / G,  A = -(3/2) g W xi
inv_g2_G = sp.simplify(-2 * sp.Rational(-3, 2) * g * W * xi)          # = 3 g W xi   [times 1/G]
def h_from(Wf, Lam_expr):        # g_YM^2 / (G_N Lambda), G = gamma G_N, g = solved from Lambda = Lam_expr(g)
    gsol = sp.solve(sp.Eq(sp.Symbol('Lam'), Lam_expr), g)[0]            # g in terms of Lambda
    inv = inv_g2_G.subs({W: Wf, g: gsol})                               # 1/g_YM^2 * G
    return sp.simplify(gam / (inv * sp.Symbol('Lam')))          # g_YM^2/(G_N Lambda) with G = gamma G_N
h_alt = h_from(Wg, (1 + 4 * gam**2 + gam**4) / (4 * g))                 # re-derived matter + printed gravity
Wd = W_der
xid = 96 / (1 - 36 * Wd**2)
h_full = h_from(Wd, (1 + 6 * gam**2 + gam**4) / (4 * g * gam**2))       # re-derived matter + re-derived gravity
chains = {"printed (19),(29),(34)": (h_pr, Wg), "P-half matter + printed gravity": (h_alt, Wg), "P-half matter + re-derived gravity": (h_full, Wd)}
mp.mp.dps = 30
x_obs = mp.mpf('2.8485e-122')
alpha_T = 1 / mp.mpf('137.035999177')
gT2 = 4 * mp.pi * alpha_T
hneeded = gT2 / x_obs
print("h needed for alpha = 1/137.036 at the observed G_N Lambda = 2.85e-122:  h = %.3e" % hneeded)
for nm, (h, Wf) in chains.items():
    hf = sp.lambdify(gam, h, 'mpmath')
    grid = [mp.mpf(k) / 200 for k in range(1, 2000)]
    vals = []
    for t in grid:
        try:
            vals.append((t, hf(t)))
        except ZeroDivisionError:
            pass
    pos = [(t, v) for t, v in vals if v > 0]
    neg = [(t, v) for t, v in vals if v < 0]
    hmax = max((abs(v) for t, v in vals if abs(v) < mp.mpf('1e12')), default=None)
    is_const = (max(abs(v) for t, v in vals) - min(abs(v) for t, v in vals)) < mp.mpf('1e-9')
    print("  chain '%s': gamma grid (0,10): %d positive-h points, %d negative-h points; h(1)=%s h(0.3)=%s h(3)=%s" %
          (nm, len(pos), len(neg), mp.nstr(hf(mp.mpf(1)), 6), mp.nstr(hf(mp.mpf('0.3')), 6), mp.nstr(hf(mp.mpf(3)), 6)))
    print("      max |h| on the finite grid = %s  (grid spacing 0.005)" % (mp.nstr(hmax, 6) if hmax else None))
    chk("h(gamma) is NOT constant on gamma in (0,10)  [chain %s]" % nm, not is_const)
# poles of the printed chain
h_pr_num, h_pr_den = sp.fraction(sp.together(h_pr))
poles = sp.solve(sp.Eq(h_pr_den, 0), gam)
poles_pos = [sp.N(p_, 20) for p_ in poles if p_.is_real and p_ > 0]
print("   printed chain: poles (g_YM^2 -> infinity, 1/g_YM^2 = 0) at gamma =", poles_pos)
# near-pole behaviour: 1/g^2 ~ c (gamma-gamma0)^2  => h ~ 1/(c (gamma-gamma0)^2)
g0 = sp.sqrt(2) / 2
c2 = sp.limit(1 / (h_pr * (gam - g0)**2) if False else (1 / h_pr) / (gam - g0)**2, gam, g0)
c2n = sp.N(c2, 20)
print("   printed chain: 1/h ~ c2 (gamma - 1/sqrt2)^2 with c2 = %s" % c2n)
if c2n != 0:
    dgam = mp.sqrt(abs(mp.mpf(str(c2n))) / hneeded)
    print("   => to reach alpha = 1/137.036 at the observed G_N Lambda one needs |gamma - 1/sqrt(2)| = %.3e (a fitted real; sign of h at that point: %s)" %
          (dgam, "positive" if c2n > 0 else "negative (ghost sign)"))
    chk("printed chain needs gamma tuned to <1e-50 around the pole (a fitted real), h has the wrong sign there or not: reported", dgam < mp.mpf('1e-50'))
for nm2, h2 in (("P-half matter + printed gravity", h_alt), ("P-half matter + re-derived gravity", h_full)):
    d2 = sp.fraction(sp.together(h2))[1]
    rts = [r for r in sp.Poly(sp.numer(sp.together(d2)), gam).nroots(n=20) if abs(sp.im(r)) < 1e-12 and sp.re(r) > 0]
    hm = max(abs(sp.N(h2.subs(gam, sp.Rational(k, 1000)))) for k in range(1, 12000))
    chk("[%s] no finite pole at gamma > 0 and sup|h| <= 0.05 on gamma in (0,12): alpha bounded by ~1e-124, not reachable by tuning" % nm2,
        (len(rts) == 0) and hm < 0.05, "real positive denominator roots = %s, max|h| = %.5f" % (rts, hm))
# sign of printed chain on the whole line
chk("printed chain: 1/g_YM^2 <= 0 for G_N Lambda > 0 at every sampled gamma > 0 (sign as printed; convention-laden, reported)", all(sp.N(1 / h_pr.subs(gam, sp.Rational(k, 7))) <= 0 for k in range(1, 60)))
# window claim: W(gamma) covers [Wmin, inf), gamma arbitrary => W free (source: 'gamma ... is arbitrary but must not vanish')
Wmin = sp.simplify(W_pr.subs(gam, 1 / sp.sqrt(2)))
chk("W(gamma) of (19) is onto [1/(6 sqrt2), infinity) as gamma ranges over (0, inf): W is a free label, not fixed by the action", sp.simplify(Wmin - 1 / (6 * sp.sqrt(2))) == 0 and sp.limit(W_pr, gam, 0, '+') == sp.oo and sp.limit(W_pr, gam, sp.oo) == sp.oo)
print("READING: in Smolin's construction g_YM^2/(G_N Lambda) is a function h(gamma) of the free label gamma of the solution (17); no chain (printed or re-derived) makes it constant.")
print("MIXED with a free real: at the observed G_N Lambda ~ 3e-122 the coupling is ~1e-124 unless gamma is fitted (printed chain: to ~1e-61 at a double pole).")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
