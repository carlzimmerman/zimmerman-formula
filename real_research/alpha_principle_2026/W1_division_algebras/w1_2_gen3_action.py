#!/usr/bin/env python3
"""w1_2_gen3_action -- Furey (arXiv:1910.08395): 'three generations' as SU(3)_c x U(1)_em content of Cl(6) = End(C x O) under a chosen action.  Pre-registered G1-G4.

The SU(3) x charge content is computed from highest-weight vectors of the 64 x 64 representation matrices (entries in Q(i); numpy complex128, integer-rounded weights, tolerance 1e-9 printed).
Exact sympy is used for the 8 x 8 identities (S = right multiplication, Lambda* = -Lambda, Q* != -Q).
Run (real):    python3 w1_2_gen3_action.py          -> exit 0 if every check passes (2 otherwise)
Run (control): python3 w1_2_gen3_action.py MUTATE   -> uses Q (not its complex conjugate Q*) in all four blocks of the action (19); exit 1 if the control bites, 3 if it does not.
"""
import sys
sys.dont_write_bytecode = True
import itertools
from fractions import Fraction
import numpy as np
import sympy as sp
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import w1_lib as W

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = W.Checks(MUT)
np.seterr(all="ignore")
c1 = 1j
Lr = W.oct_left_np()
Rr = W.oct_right_np()
Ls = W.oct_left_sp()
Is = sp.I
E8s = sp.eye(8)

# ---------------------------------------------------------------- exact 8 x 8 objects (sympy)
a_s = [(-Ls[5] + Is * Ls[4]) / 2, (-Ls[3] + Is * Ls[1]) / 2, (-Ls[6] + Is * Ls[2]) / 2]
ad_s = [(Ls[5] + Is * Ls[4]) / 2, (Ls[3] + Is * Ls[1]) / 2, (Ls[6] + Is * Ls[2]) / 2]
N_s = sum((ad_s[i] * a_s[i] for i in range(3)), sp.zeros(8)).applyfunc(sp.expand)
Q_s = N_s / 3
s_s = (E8s + Is * Ls[7]) / 2
S_direct = (E8s + Is * sp.Matrix(np.rint(Rr[7]).astype(int).tolist())) / 2          # right multiplication by (1 + i e7)/2
S_paper = E8s / 2 + sp.Rational(1, 4) * (-Is * Ls[7] + Is * Ls[1] * Ls[3] + Is * Ls[2] * Ls[6] + Is * Ls[4] * Ls[5])       # eq (16)
chk("G0a S (eq 16, written with left maps) equals right multiplication by (1 + i e7)/2 built independently from the octonion table", (S_paper - S_direct).applyfunc(sp.expand) == sp.zeros(8))
chk("G0b s and S are idempotents, s S = S s, S + S* = 1, and [s, Q] = [S, Q] = 0", (s_s * s_s - s_s).applyfunc(sp.expand) == sp.zeros(8) and (S_paper * S_paper - S_paper).applyfunc(sp.expand) == sp.zeros(8)
    and (s_s * S_paper - S_paper * s_s).applyfunc(sp.expand) == sp.zeros(8) and (s_s * Q_s - Q_s * s_s).applyfunc(sp.expand) == sp.zeros(8) and (S_paper * Q_s - Q_s * S_paper).applyfunc(sp.expand) == sp.zeros(8))
Lam_s = {1: (-ad_s[1] * a_s[0] - ad_s[0] * a_s[1]), 2: (Is * ad_s[1] * a_s[0] - Is * ad_s[0] * a_s[1]), 3: (ad_s[1] * a_s[1] - ad_s[0] * a_s[0]),
         4: (-ad_s[0] * a_s[2] - ad_s[2] * a_s[0]), 5: (-Is * ad_s[0] * a_s[2] + Is * ad_s[2] * a_s[0]), 6: (-ad_s[2] * a_s[1] - ad_s[1] * a_s[2]), 7: (Is * ad_s[2] * a_s[1] - Is * ad_s[1] * a_s[2])}
Lam_s = {k: v.applyfunc(sp.expand) for k, v in Lam_s.items()}
Hb_s = (ad_s[0] * a_s[0] + ad_s[1] * a_s[1] - 2 * ad_s[2] * a_s[2]).applyfunc(sp.expand)            # = -sqrt(3) Lambda_8
chk("G0c Lambda_j* = -Lambda_j (j=1..7, and H_b): every colour generator is a purely imaginary matrix (i Lambda_j is real)", all((Lam_s[k].conjugate() + Lam_s[k]).applyfunc(sp.expand) == sp.zeros(8) for k in Lam_s) and (Hb_s.conjugate() + Hb_s).applyfunc(sp.expand) == sp.zeros(8))
chk("G0d Q* != -Q (Q = N/3 is not purely imaginary), the point where the action must be modified (paper p.4)", (Q_s.conjugate() + Q_s).applyfunc(sp.expand) != sp.zeros(8))

# ---------------------------------------------------------------- numpy 8 x 8 objects
def npm(M): return np.array(M.tolist(), dtype=complex)
Lam = {k: npm(v) for k, v in Lam_s.items()}
Hb = npm(Hb_s)
Q = npm(Q_s)
s = npm(s_s); sc = np.eye(8) - s
S = npm(S_paper); Sc = np.eye(8) - S
I8 = np.eye(8)
def vec_ad(G): return np.kron(G, I8) - np.kron(I8, G.T)              # row-major vec of [G, X]
def vec_lr(A, B): return np.kron(A, B.T)                              # vec of A X B
blocks = {"1": (S, s), "2": (Sc, sc), "3": (Sc, s), "4": (S, sc)}      # (left projector, right projector) of S Cl s, S* Cl s*, S* Cl s, S Cl s*
P = {b: vec_lr(*AB) for b, AB in blocks.items()}
ranks = {b: int(np.linalg.matrix_rank(P[b], tol=1e-9)) for b in P}
chk("G0e the four blocks S Cl s, S* Cl s*, S* Cl s, S Cl s* are 16-dimensional and orthogonal projections summing to the identity on the 64", all(r == 16 for r in ranks.values()) and np.max(np.abs(sum(P.values()) - np.eye(64))) < 1e-12, str(ranks))

# ---------------------------------------------------------------- SU(3) x Q content from highest-weight vectors
def content(rho_lam, rho_hb, rho_q, label=""):
    """rho_*: 64x64 matrices of the (hermitian-normalised) generators Lambda_1..7, H_b, Q acting on Cl(6) (as vectors).  Returns a sorted list of ((p,q), Q, mult) plus diagnostics."""
    T = {k: rho_lam[k] for k in rho_lam}
    E1 = (T[1] + 1j * T[2]) / 2
    E2 = (T[6] + 1j * T[7]) / 2
    T3 = T[3] / 2
    Yc = -rho_hb / 3
    # identify the raising operators by their weights: [T3, E1] = +E1, and [Yc, E2] = +E2 with [T3, E2] = -1/2 E2
    def commut(A, B): return A @ B - B @ A
    okE1 = np.max(np.abs(commut(T3, E1) - E1)) < 1e-9
    okE2 = np.max(np.abs(commut(T3, E2) + 0.5 * E2)) < 1e-9 and np.max(np.abs(commut(Yc, E2) - E2)) < 1e-9
    if not (okE1 and okE2):
        return None, dict(okE1=okE1, okE2=okE2)
    # rep check
    M = np.vstack([E1, E2])
    u, sv, vh = np.linalg.svd(M)
    nullmask = np.concatenate([sv < 1e-9, np.ones(vh.shape[0] - len(sv), bool)]) if vh.shape[0] > len(sv) else sv < 1e-9
    Bm = vh[nullmask].conj().T                                          # columns: highest-weight vectors (64 x k)
    k = Bm.shape[1]
    def restrict(A): return np.linalg.lstsq(Bm, A @ Bm, rcond=None)[0]
    mq, mt, my = restrict(rho_q), restrict(T3), restrict(Yc)
    res = max(np.max(np.abs(Bm @ mq - rho_q @ Bm)), np.max(np.abs(Bm @ mt - T3 @ Bm)), np.max(np.abs(Bm @ my - Yc @ Bm)))
    K = mq + 17 * mt + 289 * my
    w, V = np.linalg.eig(K)
    out = {}
    for idx in range(k):
        v = V[:, idx]
        q = (v.conj() @ mq @ v) / (v.conj() @ v)
        t3 = (v.conj() @ mt @ v) / (v.conj() @ v)
        yc = (v.conj() @ my @ v) / (v.conj() @ v)
        p_ = 2 * t3
        q_ = -t3 + 1.5 * yc
        key = (int(round(p_.real)), int(round(q_.real)), Fraction(q.real).limit_denominator(12))
        assert abs(p_ - round(p_.real)) < 1e-6 and abs(q_ - round(q_.real)) < 1e-6 and abs(q.real - float(key[2])) < 1e-6, (p_, q_, q)
        out[key] = out.get(key, 0) + 1
    return sorted(((kk[0], kk[1]), kk[2], m) for kk, m in out.items()), dict(okE1=okE1, okE2=okE2, restrict_residual=float(res), n_irreps=k)

def build_rho(block_cfg, plain=False):
    """block_cfg[b] = (use_conj, sign) for the charge generator in block b: G_Q = i * sign * (Q or Q*) * s_b ; colour: G_j = i Lambda_j s_b (paper).  plain: ordinary adjoint of (i Lambda_j, i Q) on all of Cl(6)."""
    rl = {}
    if plain:
        for j in range(1, 8): rl[j] = vec_ad(1j * Lam[j]) / 1j
        rhb = vec_ad(1j * Hb) / 1j
        rq = vec_ad(1j * Q) / 1j
        return rl, rhb, rq
    for j in range(1, 8):
        rl[j] = sum(vec_ad(1j * Lam[j] @ blocks[b][1]) @ P[b] for b in blocks) / 1j
    rhb = sum(vec_ad(1j * Hb @ blocks[b][1]) @ P[b] for b in blocks) / 1j
    rq = 0
    for b, (use_conj, sign) in block_cfg.items():
        Qb = Q.conj() if use_conj else Q
        rq = rq + vec_ad(1j * sign * Qb @ blocks[b][1]) @ P[b]
    rq = rq / 1j
    return rl, rhb, rq

# the target (20) of the paper
def T(pq, q, m): return (pq, Fraction(q).limit_denominator(12), m)
F = Fraction
# merge the two (0,0),(Q=0) entries (3 x 1_0 in each half => 6 x 1_0 in total) and the two octets (8_0 twice)
def merge(lst):
    d = {}
    for pq, q, m in lst:
        d[(pq, q)] = d.get((pq, q), 0) + m
    return sorted(((k[0], k[1], m) for k, m in d.items() if m))
target20 = merge([((1, 1), F(0), 1), ((1, 0), F(2, 3), 3), ((1, 0), F(-1, 3), 3), ((0, 0), F(0), 3), ((0, 0), F(-1), 3),
                  ((1, 1), F(0), 1), ((0, 1), F(-2, 3), 3), ((0, 1), F(1, 3), 3), ((0, 0), F(0), 3), ((0, 0), F(1), 3)])
def show(c): return ", ".join(f"{('8' if pq == (1, 1) else '3' if pq == (1, 0) else '3bar' if pq == (0, 1) else '1' if pq == (0, 0) else str(pq))}_{q}x{m}" for pq, q, m in c)

paper_cfg = {"1": (True, -1), "2": (False, +1), "3": (False, +1), "4": (True, -1)}
if MUT:
    paper_cfg = {b: (False, sg) for b, (cj, sg) in paper_cfg.items()}          # MUTATE: Q instead of Q* in every block

# ---------------------------------------------------------------- G1: SU(3) content of the 64 under (a) plain adjoint, (b) the paper's block action (colour part only)
rl_p, rhb_p, rq_p = build_rho(None, plain=True)
cp, dp = content(rl_p, rhb_p, rq_p)
def su3_only(c):
    d = {}
    for pq, q, m in c: d[pq] = d.get(pq, 0) + m
    return d
print("      plain adjoint, (SU(3), Q) content:", show(cp) if cp else dp)
chk("G1a plain adjoint action of su(3) on End(V): raising operators have the fundamental-type weights and the highest-weight decomposition is consistent", cp is not None, str(dp))
if cp:
    d_plain = su3_only(cp)
    print("      plain adjoint, SU(3) content:", d_plain)
    dim_plain = sum(m * (1 if pq == (0, 0) else 3 if pq in ((1, 0), (0, 1)) else 8 if pq == (1, 1) else 6 if pq in ((2, 0), (0, 2)) else -10**6) for pq, m in d_plain.items())
    chk("G1b plain adjoint content sums to 64 and contains 6 / 6bar (from 3 x 3 in V x V*): it is NOT the 2x8 + 6x3 + 6x3bar + 12x1 pattern of the paper (eq 14)", dim_plain == 64 and ((2, 0) in d_plain or (0, 2) in d_plain), str(d_plain))
block_cfg = paper_cfg
rl, rhb, rq = build_rho(block_cfg)
cb, db = content(rl, rhb, rq)
chk("G3a the paper's four-block action (19) yields consistent su(3) raising operators (weights of E_alpha as in the fundamental)", cb is not None, str(db))
if cb:
    d_blk = su3_only(cb)
    print("      block action (19), SU(3) content:", d_blk)
    chk("G1c the block action (19), colour part only: 2 x 8 + 6 x 3 + 6 x 3bar + 12 x 1 = 64 (eqs 12-14)", d_blk == {(1, 1): 2, (1, 0): 6, (0, 1): 6, (0, 0): 12}, str(d_blk))
    print("      block action (19), (SU(3), Q) content:", show(cb))
    print("      paper eq (20):                        ", show(target20))
    chk("G3b the block action (19) with Q* in blocks 1 and 4 reproduces the paper's content (20) EXACTLY (multiset of (SU(3) irrep, Q))", cb == target20)
if cp:
    chk("G2 the plain adjoint (SU(3), Q) content differs from the paper's (20)", cp != target20)

# ---------------------------------------------------------------- G4: how many alternatives reproduce (20)?
hits2 = []
cache = {}
def content_cfg(cfg):
    rl_, rhb_, rq_ = build_rho(cfg)
    c_, _ = content(rl_, rhb_, rq_)
    return c_
for conj_bits in itertools.product([False, True], repeat=4):
    cfg = {b: (cj, paper_cfg_sign) for b, cj, paper_cfg_sign in zip("1234", conj_bits, (-1, +1, +1, -1))}
    c_ = content_cfg(cfg)
    if c_ == target20: hits2.append(conj_bits)
hits4 = []
for bits in itertools.product([(False, 1), (False, -1), (True, 1), (True, -1)], repeat=4):
    cfg = {b: v for b, v in zip("1234", bits)}
    c_ = content_cfg(cfg)
    if c_ == target20: hits4.append(bits)
print(f"      alternatives keeping the paper's signs, conj yes/no per block: {len(hits2)} of 16 reproduce (20): {hits2}")
print(f"      amendment-1 enumeration (conj yes/no x sign per block, 4^4 = 256): {len(hits4)} reproduce (20)")
chk("G4a the paper's choice (Q*, Q, Q, Q*) is among the alternatives reproducing (20) and the two uniform choices (all Q, all Q*) are not", (True, False, False, True) in hits2 and (False, False, False, False) not in hits2 and (True, True, True, True) not in hits2, f"{len(hits2)} of 16 reproduce (20)")
print(f"      G4b (statement, not a check): {len(hits2)} of 16 (paper signs) and {len(hits4)} of 256 (all conj/sign choices) block prescriptions reproduce (20). Within this family the prescription is therefore FIXED by the demand to reproduce the SM content (20); nothing in C x O selects the family or the demand.")
print("      G verdict: the count '3' is the multiplicity of V x V* blocks under a prescription the author leaves unexplained (open question in the paper's outlook);")
print("      the ratios of charges (1/3, 2/3, 1) come from Q = N/3 (w1_1); the size of the charge unit remains a free normalisation.")
chk.finish("w1_2")
