"""AS3 block: quadratic action on Minkowski from first-order pieces. Shares no code with as2_engine or the record.
On Minkowski with aether A_mu = (-1,0,0,0), phi = Q0 t, every extra term is a product of two quantities that vanish on the background
(D_ab = nabla_a A_b, V_i, dQ, F_Q(Q0) = 0), and the Einstein-Hilbert GammaGamma form is a product of two first-order Gammas. So first-order pieces suffice: exact at second order.
Plane wave f exp(i(k z - w t)); fields depend on (t, z). L = f^dag M f + f^dag J + c.c. form; EOM M f = -J/2 (real-wave average). MUTATE flips EH and the a.V sign. 16 pi G~ = 1."""
import os
import sympy as sy
MUT = os.environ.get("AS3_MUTATE") == "1"
SGN = -1 if MUT else 1
ETA = [-1, 1, 1, 1]
w, k = sy.symbols("w k", real=True)

def piece(names):
    return {n: sy.Integer(0) for n in names}
def add(a, b, cb=1):
    o = dict(a)
    for n, v in b.items():
        o[n] = o.get(n, 0) + cb * v
    return o
def mul(a, c):
    return {n: c * v for n, v in a.items()}

class Block:
    """sector 's': Phi Psi B e Az pi. sector 'v': Bx ex Ax. Derivative d = (-i w, 0, 0, i k) acting on a ket."""
    def __init__(self, sector):
        self.sector = sector
        self.names = ["Phi", "Psi", "B", "e", "Az", "pi"] if sector == "s" else ["Bx", "ex", "Ax"]
        self.d = [-sy.I * w, 0, 0, sy.I * k]
    def h(self):
        """h_ab as linear forms."""
        z = piece(self.names); H = [[dict(z) for _ in range(4)] for _ in range(4)]
        def one(n, c=1):
            o = dict(z); o[n] = sy.Integer(c); return o
        if self.sector == "s":
            H[0][0] = one("Phi", -2)
            H[1][1] = H[2][2] = one("Psi", -2)
            H[3][3] = add(one("Psi", -2), one("e", 2))
            H[0][3] = H[3][0] = one("B")
        else:
            H[0][1] = H[1][0] = one("Bx")
            H[1][3] = H[3][1] = one("ex")
        return H
    def gamma(self):
        """Gamma^c_ab first order, index c up."""
        H, d = self.h(), self.d
        G = [[[None] * 4 for _ in range(4)] for _ in range(4)]
        for c in range(4):
            for a in range(4):
                for b in range(4):
                    t = add(add(mul(H[b][c], d[a]), mul(H[a][c], d[b])), mul(H[a][b], d[c]), -1)
                    G[c][a][b] = mul(t, sy.Rational(ETA[c], 2))
        return G
    def DA(self):
        """D_ab = d_a dA_b - Gamma^c_ab A_c, A_c = (-1,0,0,0), dA_0 = h00/2."""
        G, H, d = self.gamma(), self.h(), self.d
        z = piece(self.names); A = [mul(H[0][0], sy.Rational(1, 2)), dict(z), dict(z), dict(z)]
        if self.sector == "s":
            A[3] = dict(z); A[3]["Az"] = sy.Integer(1)
        else:
            A[1] = dict(z); A[1]["Ax"] = sy.Integer(1)
        D = [[add(mul(A[b], d[a]), G[0][a][b]) for b in range(4)] for a in range(4)]
        return D, A

def bil(M, names, x, y, c):
    """add c * Re(conj(x) y), so that M is Hermitian. conj taken at real k, w."""
    for i, n in enumerate(names):
        for j, m in enumerate(names):
            xi, yj, xj, yi = x.get(n, 0), y.get(m, 0), x.get(m, 0), y.get(n, 0)
            M[i, j] += c * (sy.conjugate(xi) * yj + sy.conjugate(yi) * xj) / 2

def matrix(sector, c=(0, 0, 0, 0), KB=0, F=0, Nf=0, Q0=0, K2=0, wb=1):
    """Lagrangian: wb sqrt(-g) R - K^ab_cd D D (Einstein-aether with c1..c4) - (KB/2) F^2 + 2 Nf a.V - F V^2 + K2 dQ^2.
    AeST: Nf = F_base = 2 - K_B, F = (2-K_B)(1+J_Y), K2 enters with the sign stated by the caller."""
    b = Block(sector); names = b.names; n = len(names)
    M = sy.zeros(n, n)
    G = b.gamma(); D, A = b.DA()
    # Einstein-Hilbert, GammaGamma form: g^bc (Gamma^a_bd Gamma^d_ca - Gamma^a_ad Gamma^d_bc)
    tr = [None] * 4
    for d_ in range(4):
        t = piece(names)
        for a in range(4):
            t = add(t, G[a][a][d_])
        tr[d_] = t
    eh = SGN * wb
    for bb in range(4):
        for a in range(4):
            for d_ in range(4):
                bil(M, names, G[a][bb][d_], G[d_][bb][a], eh * ETA[bb])
    for bb in range(4):
        for d_ in range(4):
            bil(M, names, tr[d_], G[d_][bb][bb], -eh * ETA[bb])
    # Einstein-aether
    c1, c2, c3, c4 = c
    th = piece(names)
    for i in range(4):
        th = add(th, D[i][i], ETA[i])
    for a_ in range(4):
        for b_ in range(4):
            e_ = ETA[a_] * ETA[b_]
            if c1:
                bil(M, names, D[a_][b_], D[a_][b_], -c1 * e_)
            if c3:
                bil(M, names, D[a_][b_], D[b_][a_], -c3 * e_)
    if c2:
        bil(M, names, th, th, -c2)
    a_i = [D[0][i] for i in (1, 2, 3)]   # a_b = A^a D_ab, A^0 = 1
    if c4:
        for x in a_i:
            bil(M, names, x, x, c4)
    # Maxwell term: -(KB/2) F_ab F^ab
    if KB:
        for a_ in range(4):
            for b_ in range(4):
                Fab = add(D[a_][b_], D[b_][a_], -1)
                bil(M, names, Fab, Fab, -sy.Rational(1, 2) * KB * ETA[a_] * ETA[b_])
    # scalar pieces
    z = piece(names)
    if sector == "s":
        V = [dict(z), dict(z), dict(z)]
        V[2] = dict(z); V[2]["pi"] = sy.I * k; V[2]["Az"] = sy.sympify(Q0)
        dQ = dict(z); dQ["pi"] = -sy.I * w; dQ["Phi"] = -sy.sympify(Q0)
    else:
        V = [dict(z), dict(z), dict(z)]
        V[0] = dict(z); V[0]["Ax"] = sy.sympify(Q0)
        dQ = dict(z)
    if Nf or F:
        for x, y in zip(a_i, V):
            bil(M, names, x, y, 2 * Nf * SGN)
            bil(M, names, y, y, -F)
    if K2:
        bil(M, names, dQ, dQ, K2)
    return b, M

def source(sector, names, v):
    """L_m = (1/2) h_ab T^ab with T00 = 1, T0i = v, Tij = v v; returned as J in f^dag J."""
    b = Block(sector); H = b.h(); J = sy.zeros(len(names), 1)
    if sector == "s":
        T = {(0, 0): 1, (0, 3): v, (3, 0): v, (3, 3): v ** 2}
    else:
        T = {(0, 0): 1, (0, 1): v, (1, 0): v, (1, 1): v ** 2}
    for (a, c), t in T.items():
        for i, n in enumerate(names):
            J[i] += sy.Rational(1, 2) * t * H[a][c].get(n, 0)
    return J

def solve(sector, v, kval=1, keep=None, **kw):
    """Exact solve at omega = k v_along_k, gauge B = e = 0 (scalar), ex = 0 (vector) AFTER variation.
    Returns dict field -> value and the residual of all rows. v_long is the speed along k (scalar sector); in the vector sector pass vk for omega and v for T^0x."""
    vk = kw.pop("vk", None)
    b, M = matrix(sector, **kw)
    names = b.names
    om = kval * (v if sector == "s" else (vk if vk is not None else 0))
    M = M.subs({k: kval, w: om})
    J = source(sector, names, v)
    keep = keep or ([n for n in ("Phi", "Psi", "Az", "pi")] if sector == "s" else ["Bx", "Ax"])
    live = lambda x: any(sy.simplify(q) != 0 for q in M[names.index(x), :])
    keep = [x for x in keep if live(x)]
    idx = [names.index(x) for x in keep]
    use = [names.index(x) for x in (keep if sector == "v" else keep)]
    A = M[use, idx]; R = -J[use, 0] / 2
    x = A.LUsolve(R) if A.free_symbols else A.inv() * R
    x = x.applyfunc(sy.cancel)
    res = (M[:, idx] * x + J / 2).applyfunc(sy.cancel)
    return dict(zip(keep, x)), res
