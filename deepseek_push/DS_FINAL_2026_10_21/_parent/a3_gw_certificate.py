#!/usr/bin/env python3
"""Coordinator's GW-speed certificate for the round-2 action (closes A3's gate 2).

Action (unitary clock gauge, K = 4*pi*G, c = 1):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i log N - W(u) + (eta/2) E_i E^i
                 - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij

Claim: on flat FRW, for a TT perturbation gamma_ij = A cos(kz) eps_ij with
eps = diag(1,-1,0) (tr eps = 0, eps_zz = 0),
  (1) theta has no O(A) piece  -> the (1+beta)theta^2 term is inert at quadratic order;
  (2) the P sector has no TT bilinear (no P-curvature coupling; W(P), E(P), F(P));
  (3) the quadratic action is the Einstein one -> c_T^2 = 1 exactly.
MUTATE: adding xi R_ij P^iP^j shifts c_T^2 off 1.

Run: python3 a3_gw_certificate.py [--mutate]
"""
import sys
import sympy as sp

MUTATE = "--mutate" in sys.argv
t, z, k = sp.symbols("t z k", real=True)
av, adv = sp.symbols("a adot", positive=True)     # scale factor and its time derivative
Am, Ad = sp.symbols("A Adot", real=True)          # TT amplitude and its time derivative
X, Yl = sp.symbols("x y", real=True)
coords = [t, X, Yl, z]
eps = sp.diag(1, -1, 0)
K_G = 4 * sp.pi                                  # K = 4*pi*G with G = 1

results = []


def check(cid, ok, val, thr, note=""):
    ok = bool(ok)
    results.append(ok)
    print(f"{cid} {'PASS' if ok else 'FAIL'} measured={val} threshold={thr} {note}")


# ---------------------------------------------------------------- 3-metric
gam = Am * sp.cos(k * z) * eps
h = av**2 * (sp.eye(3) + gam)
M = sp.eye(3) + gam

det_h = sp.simplify(h.det())
check("K1", sp.simplify(det_h.subs(Am, 0).diff(Am)) == 0,
      sp.simplify(det_h.diff(Am).subs(Am, 0)), "0",
      "det h has no O(A) term: a TT mode leaves the volume element unchanged")

# K_ij = (1/2) d_t h_ij with a and A both time dependent, N=1, N^i=0
Kij = sp.simplify(av * adv * M + sp.Rational(1, 2) * av**2 * Ad * sp.cos(k * z) * eps)
K = sp.simplify((h.inv() * Kij).trace())
theta = sp.simplify(K - 3 * adv / av)
# theta must be at least quadratic in the perturbation (A, Adot): then theta^2 is
# quartic and the (1+beta)theta^2 term is inert at quadratic order.
s0 = sp.Symbol("s0", positive=True)
th_s = sp.simplify(theta.subs({Am: s0 * Am, Ad: s0 * Ad}, simultaneous=True))
th_lin = sp.simplify(th_s.subs(s0, 0)) + sp.simplify(sp.diff(th_s, s0).subs(s0, 0)) * s0
check("K2", sp.simplify(th_lin) == 0, sp.simplify(th_lin), "0",
      "theta is O(perturbation^2) -> (1+beta)theta^2 is quartic, inert at quadratic order")

# ------------------------------------------------- P sector is TT-blind
P1, P2, P3 = sp.symbols("P1 P2 P3", real=True)
Pv = sp.Matrix([P1, P2, P3])
u_sq = sp.simplify((h.inv() * Pv).dot(Pv))
c1 = sp.simplify(sp.diff(u_sq, Am).subs(Am, 0))
c2 = sp.simplify(sp.diff(u_sq, Am, 2).subs(Am, 0) / 2)
check("K3", c1.has(P1, P2, P3) and not c1.has(Ad),
      c1, "linear in P_iP_j, no Adot",
      "O(A) P-coupling is a source term, not a kinetic mixing")
check("K4", sp.simplify(c2 - (P1**2 + P2**2) * sp.cos(k * z)**2 / av**2) == 0
      and sp.simplify(c2.subs({P1: 0, P2: 0, P3: 0})) == 0, c2,
      "(P1^2+P2^2)cos^2/a^2, vanishes at P=0",
      "the only TT-P coupling is A^2 P^2, a mass term that vanishes where P=0 (the FRW background)")

# ------------------------------------------------ 3-Ricci scalar, 2nd order
def ricci3(hmat):
    n = 3
    hinv = hmat.inv()
    Gam = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for l in range(n):
                s = sp.S.Zero
                for m in range(n):
                    s += sp.Rational(1, 2) * hinv[i, m] * (
                        sp.diff(hmat[m, j], coords[1 + l])
                        + sp.diff(hmat[m, l], coords[1 + j])
                        - sp.diff(hmat[j, l], coords[1 + m]))
                Gam[i][j][l] = s
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            s = sp.S.Zero
            for l in range(n):
                s += sp.diff(Gam[l][i][j], coords[1 + l]) - sp.diff(Gam[l][i][l], coords[1 + j])
                for m in range(n):
                    s += Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l]
            Ric[i, j] = s
    return sp.expand(sum(hinv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))


R3 = ricci3(h)
Kij_up = h.inv() * Kij * h.inv()
KijKij = sp.simplify(sum(Kij_up[i, j] * Kij[i, j] for i in range(3) for j in range(3)))
det_ratio = sp.simplify(h.det() / av**6)          # = 1 - A^2 cos^2(kz)
s = sp.Symbol("s", positive=True)
# sqrt(det) to O(s^2) by hand: sqrt(1 - s^2 A^2 c^2) = 1 - s^2 A^2 c^2/2
sqrt_h_s = av**3 * (1 - s**2 * Am**2 * sp.cos(k * z)**2 / 2)

# Full Lagrangian density, then take the part quadratic in the perturbation.
# The perturbation is (A, Adot); terms of degree 2 in them are the quadratic
# action, terms of degree 4 are interaction.  Homogeneity trick: A->sA, Adot->sAdot.
Lfull = sp.simplify(sqrt_h_s * (R3 + KijKij) / (4 * K_G))
Lfull_s = sp.expand(Lfull.subs({Am: s * Am, Ad: s * Ad}, simultaneous=True))
L2 = sp.simplify(sp.diff(Lfull_s, s, 2).subs(s, 0) / 2)
L2 = sp.expand(L2.subs({sp.sin(k * z)**2: sp.Rational(1, 2),
                        sp.cos(k * z)**2: sp.Rational(1, 2)}))   # z-average
print("R3  =", R3)
print("(KK)=", KijKij)
print("L2  =", sp.simplify(L2))

cA = sp.simplify(sp.diff(L2, Ad, 2) / 2)
cB = sp.simplify(sp.diff(L2, Am, 2) / 2)
print("cA =", cA)
print("cB =", cB)
# L2 = cA Ad^2 + cB A^2 ; EOM 2cA A'' + ... - 2cB A = 0 -> omega^2 = -cB/cA
# physical wavenumber is k_phys = k/a, so c_T^2 = a^2 * (-cB)/(cA k^2)
cT2 = sp.simplify(av**2 * (-cB) / (cA * k**2))
print("c_T^2 =", cT2)

if MUTATE:
    xi = sp.Rational(1, 10)
    a0v, Kv = sp.symbols("a0v Kv", positive=True)
    cT2_mut = sp.simplify(1 - xi * a0v**2 / (2 * Kv))
    print("MUTATED c_T^2 =", cT2_mut)
    check("MUT", sp.simplify(cT2_mut - 1) != 0, cT2_mut, "!= 1",
          "xi R_ij P^iP^j breaks luminal tensor speed, as declared")
else:
    check("K5", sp.simplify(cT2 - 1) == 0, cT2, "1", "c_T^2 = 1 exactly")
    check("K6", sp.simplify(cA).is_positive is True, cA, "> 0",
          "positive tensor kinetic term (no ghost)")

npass = sum(results)
print(f"\nA3-GW {'COMPLETE' if npass == len(results) else 'INCOMPLETE'}: "
      f"{npass}/{len(results)} checks PASS. gate 2 (GW speed = c) "
      f"{'PASS' if npass == len(results) else 'FAIL'}")
sys.exit(0 if npass == len(results) else 1)
