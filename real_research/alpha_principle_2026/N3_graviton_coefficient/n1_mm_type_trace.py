#!/usr/bin/env python3
"""N1 -- MacDowell-Mansouri-type action  Int <X F ^ F>  on spin(1+N,3): which h-invariant compensators X give a spin(N) gauge term?
h = spin(1,3) + spin(N).  Exact Clifford algebra Cl(1+N,3) (blade representation, rational arithmetic), scalar part = the trace <.> of the sources.
Generators (spinor-representation normalisation, D = d + H):  J_ab = (1/2) g_a g_b (Lorentz), J_mn = (1/2) g_m g_n (internal), J_am = (1/2) g_a g_m (off-diagonal).
Invariant basis of Cl under h (elements commuting with all J_ab, J_mn):  {1, G_L = g0g1g2g3, G_N = g4...g_{3+N}, G_L G_N}.
CHECKS (N = 3 and N = 10):
  (a) X = 1:  <J_mn J_pq> = -(1/4) delta  (nonzero: this is the metric-free Pontryagin term <F^F> = topological, NOT a kinetic term);
  (b) X in {G_L, G_N, G_L G_N}:  <X J_mn J_pq> = 0 for ALL internal pairs (m<n),(p<q)  -> no spin(N) F^F coefficient;
  (c) same X:  <X J_am J_bn> = 0 (off-diagonal block also gives nothing);
  (d) gravity block: <G_L J_ab J_cd> = -(1/4)(eps_abcd)*const with |const| fixed, so <G_L F_L F_L> ~ eps_abcd L^ab L^cd with L = R - (phi^2/4) e e, i.e. the MM form R - (Lambda/3) e e with Lambda = 3 phi^2/4.
Run:    python3 n1_mm_type_trace.py           (exit 0)
MUTATE: python3 n1_mm_type_trace.py MUTATE   (adds the NON-invariant X = g4 g5 g6 g7 to the list of X that must give zero; check (b) must FAIL -> exit 1)
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations
from clifford_lib import Cl, lorentz_plus_internal

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok:
        fails.append(n)

half = Fr(1, 2)
for N in (3, 10):
    cl = lorentz_plus_internal(N)
    L_idx = [0, 1, 2, 3]
    N_idx = list(range(4, 4 + N))
    one = {0: Fr(1)}
    GL = cl.word(L_idx)
    GN = cl.word(N_idx)
    GLGN = cl.mul(GL, GN)
    Xs = {"G_L": GL, "G_N": GN, "G_L G_N": GLGN}
    if MUT and N >= 4:
        Xs["MUT g4g5g6g7 (not h-invariant)"] = cl.word([4, 5, 6, 7])
    # invariance check of the basis under J_mn and J_ab (commutator zero)
    def commutes(X, Y):
        return cl.add(cl.mul(X, Y), cl.mul(Y, X), -1) == {}
    Jint = {(m, n): cl.word([m, n], half) for m, n in combinations(N_idx, 2)}
    Jlor = {(a, b): cl.word([a, b], half) for a, b in combinations(L_idx, 2)}
    inv_ok = all(commutes(X, J) for name, X in list(Xs.items())[:3] for J in list(Jint.values()) + list(Jlor.values()))
    chk("N=%d: 1, G_L, G_N, G_L G_N commute with all J_ab, J_mn (h-invariant)" % N, inv_ok)
    # (a) X = 1
    pairs = list(Jint.items())
    ok_a = True
    for (k1, J1) in pairs:
        for (k2, J2) in pairs:
            v = cl.scalar(cl.mul(J1, J2))
            want = Fr(-1, 4) if k1 == k2 else Fr(0)
            if v != want:
                ok_a = False
    chk("N=%d: X=1 gives <J_mn J_pq> = -(1/4) delta (topological Pontryagin structure, nonzero)" % N, ok_a)
    # (b) must-vanish
    for name, X in Xs.items():
        vmax = max(abs(cl.scalar(cl.mul(X, cl.mul(J1, J2)))) for (_, J1) in pairs for (_, J2) in pairs)
        chk("N=%d: X=%s gives <X J_mn J_pq> = 0 for all pairs" % (N, name), vmax == 0, "max|.| = %s" % vmax)
    # (c) off-diagonal block J_am J_bn
    Joff = [cl.word([a, m], half) for a in L_idx for m in N_idx[:4]]
    for name, X in list(Xs.items())[:3]:
        vmax = max(abs(cl.scalar(cl.mul(X, cl.mul(J1, J2)))) for J1 in Joff for J2 in Joff)
        chk("N=%d: X=%s gives <X J_am J_bn> = 0" % (N, name), vmax == 0, "max|.| = %s" % vmax)
    # X=1 on off-diagonal block, for information
    v = cl.scalar(cl.mul(Joff[0], Joff[0]))
    print("   info N=%d: <J_0m J_0m> = %s (X=1, time-internal block; the Pontryagin term also has this off-diagonal piece)" % (N, v))
    # (d) gravity block
    eps_vals = {}
    for (a, b) in combinations(L_idx, 2):
        for (c, d) in combinations(L_idx, 2):
            v = cl.scalar(cl.mul(GL, cl.mul(Jlor[(a, b)], Jlor[(c, d)])))
            if v != 0:
                eps_vals[(a, b, c, d)] = v
    # each nonzero entry must be +-1/4 * (signature product of G_L^2 factors): all |v| equal
    absvals = set(abs(v) for v in eps_vals.values())
    chk("N=%d: <G_L J_ab J_cd> nonzero exactly on the 3 complementary pairings (eps_abcd), |value| equal" % N,
        len(eps_vals) == 6 and len(absvals) == 1, "values %s" % sorted(set(eps_vals.values())))

# MM relation Lambda/3 = phi^2/4 from H_E^2 (sympy-free rational check): (E^E)_ab = (1/16) phi^m phi^n (g_a g_m g_b g_n - g_b g_m g_a g_n) = -(1/8) phi^2 g_a g_b
cl = lorentz_plus_internal(3)
phi = [Fr(2), Fr(-1), Fr(3)]           # arbitrary internal vector phi^m
phi2 = sum(p * p for p in phi)
tot = {}
for a, b in ((0, 1), (1, 2), (2, 3), (0, 3)):
    acc = {}
    for i, pm in enumerate(phi):
        for j, pn in enumerate(phi):
            m, n = 4 + i, 4 + j
            t1 = cl.word([a, m, b, n], Fr(1, 16) * pm * pn)
            t2 = cl.word([b, m, a, n], Fr(1, 16) * pm * pn)
            acc = cl.add(acc, cl.add(t1, t2, -1))
    want = cl.word([a, b], Fr(-1, 8) * phi2)
    chk("(E^E)_{%d%d} = -(1/8) phi^2 g_a g_b  (so F_L = (1/4)[R^ab - (phi^2/4) e^a e^b] g_ab, MM: Lambda/3 = phi^2/4)" % (a, b),
        cl.add(acc, want, -1) == {})
print("READING: for every h-invariant compensator X, <X F_N ^ F_N> is either the metric-free topological term (X=1) or identically zero.")
print("A kinetic term F_N ^ *F_N needs a Hodge star, i.e. a metric-dependent operator that an action Int <X F^F> (X constant) cannot supply;")
print("the MM-type extension therefore carries NO spin(N) gauge kinetic coefficient (ABSENT), consistent with the Krasnov-Percacci remark.")
print("SCOPE: constant compensators only; a field-dependent Phi (as in LSS, checked in n2) is a different construction.")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
