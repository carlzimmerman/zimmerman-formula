# UW1 test A: tree 2->2 about a static gradient, s-wave, angle-averaged. MUTATE=1 swaps in the planted F and 2 pi G. One thread, seconds.
import itertools, json, os
import numpy as np
import sympy as sp

MUT = os.environ.get("MUTATE") == "1"
here = os.path.dirname(os.path.abspath(__file__))
eta = np.diag([-1.0, 1.0, 1.0, 1.0])

Ys = sp.symbols("Y", positive=True)
def derivs(Fexpr, Y):
    return [float(sp.diff(Fexpr, Ys, k).subs(Ys, Y)) for k in range(1, 5)]
F0 = sp.symbols("F0")
F_law = Ys - 2 * sp.sqrt(Ys) + 2 * sp.log(1 + sp.sqrt(Ys)) + F0
blind = all(not sp.diff(F_law, Ys, k).has(F0) for k in range(1, 5))

def amplitude(k, Y, D):
    """k: four all-incoming on-shell momenta in rescaled coordinates. Returns M for canonical fluctuations."""
    F1, F2, F3, F4 = D
    Z = (F1 + 2 * F2 * Y) / F1
    G = np.diag([-1.0, 1.0, 1.0, 1.0 / Z])
    n = np.array([0, 0, 0, 1.0 / np.sqrt(Z)])       # n.d_pi in rescaled coordinates
    Nf = np.sqrt(F1) * Z**0.25                      # pi = pi_c / Nf
    vol = np.sqrt(Z)
    v = lambda p: 1j * (n @ p)
    W = lambda p, q: -(p @ G @ q)                   # (ip).(iq) with G
    a3 = -0.5 * 2 * F2 * np.sqrt(Y) * vol / Nf**3    # v W
    b3 = -0.5 * (4 / 3) * F3 * Y**1.5 * vol / Nf**3  # v^3
    def V3(p, q, r):
        t = 0j
        for x, y, z in itertools.permutations((p, q, r)):
            t += a3 * v(x) * W(y, z) + b3 * v(x) * v(y) * v(z)
        return t
    a4 = -0.5 * 0.5 * F2 * vol / Nf**4               # W W
    b4 = -0.5 * 2 * F3 * Y * vol / Nf**4             # v v W
    c4 = -0.5 * (2 / 3) * F4 * Y**2 * vol / Nf**4    # v^4
    M = 0j
    for x, y, z, u in itertools.permutations(k):
        M += a4 * W(x, y) * W(z, u) + b4 * v(x) * v(y) * W(z, u) + c4 * v(x) * v(y) * v(z) * v(u)
    for (i, j, l, m) in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
        q = k[i] + k[j]
        q2 = q @ eta @ q
        if abs(q2) < 1e-12:
            continue
        M += V3(k[i], k[j], -q) * V3(q, k[l], k[m]) / q2
    return M

def kin(direction, cos_t, phi):
    """COM at s = 1. direction: unit 3-vector of the beam."""
    E = 0.5
    d = direction / np.linalg.norm(direction)
    a = np.cross(d, [1, 0, 0]) if abs(d[0]) < 0.9 else np.cross(d, [0, 1, 0])
    a /= np.linalg.norm(a); b = np.cross(d, a)
    o = cos_t * d + np.sqrt(1 - cos_t**2) * (np.cos(phi) * a + np.sin(phi) * b)
    p = lambda s, e: np.array([s * E, *(s * E * e)])  # all incoming: outgoing with minus sign
    return [p(1, d), p(1, -d), p(-1, o), p(-1, -o)]

def B_of(Y, D, nb=48, nt=64, nphi=24):
    xb, wb = np.polynomial.legendre.leggauss(nb)
    xt, wt = np.polynomial.legendre.leggauss(nt)
    tot, im, mx = 0.0, 0.0, 0.0
    for cb, wbi in zip(xb, wb):
        d = np.array([np.sqrt(1 - cb**2), 0, cb])
        inner = 0j
        for ct, wti in zip(xt, wt):
            for ph in (np.arange(nphi) + 0.5) * 2 * np.pi / nphi:
                inner += wti * amplitude(kin(d, ct, ph), Y, D) / nphi
        tot += 0.5 * wbi * inner.real; im += 0.5 * wbi * abs(inner.imag)
    return tot, im

res = {"mode": "MUTATE" if MUT else "normal", "derivatives_blind_to_F0": blind}
# Control, at Y small with planted F, F = Y - 2 c Y^2
c = 0.3
planted = Ys - 2 * c * Ys**2
Yc = 1e-8
Bc, _ = B_of(Yc, derivs(planted, Yc), nb=6, nt=32, nphi=6)
Bexp = 2 * c * (1 + 2 * (1 / 3))  # int dcos (s^2+t^2+u^2) = s^2 (2 + 2/3 + ... ) checked below
ct = sp.symbols("x")
intg = sp.integrate(1 + ((1 - ct) / 2)**2 + ((1 + ct) / 2)**2, (ct, -1, 1))
Bexp = 2 * c * float(intg)
res["control_B"] = Bc; res["control_expected"] = Bexp; res["control_pass"] = bool(abs(Bc - Bexp) < 1e-3 * abs(Bexp))
Fuse = planted if MUT else F_law.subs(F0, 0)
coupling = 2 if MUT else 4     # a0^2 = coupling pi G M^4
for Y in (1.0, 0.1, 10.0):
    D = derivs(Fuse, Y)
    B, im = B_of(Y, D)
    row = {"F1..F4": D, "c_par2": D[0] / (D[0] + 2 * D[1] * Y), "B": B, "imag_abs": im}
    if B > 0:
        # s*^2 = N a_max pi M^4 / B with a = B s^2/(N pi M^4); kappa^2 = coupling pi M^4/epsilon, epsilon = s*^2
        cells = {}
        for N in (32, 64):
            for amax in (0.5, 1.0):
                cells[f"N{N}_amax{amax}"] = float(np.sqrt(coupling * B / (N * amax)))
        row["kappa_cells"] = cells
    res[f"Y={Y}"] = row
for k, v in res.items():
    print(k, v)
with open(os.path.join(here, f"uw1{'_MUTATE' if MUT else ''}.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
