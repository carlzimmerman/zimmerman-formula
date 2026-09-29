"""cfg102_common -- shared machinery for CFG102 (see cfg102_frozen.py for the frozen criteria).  Path-independent: the repository root is
taken from $ZF_REPO, else found by walking up from this file / the cwd for real_research/g03_audit_2026, else ~/new_physics/zimmerman-formula.
DE12's transition() is exec'd read-only exactly as DE13 does (grid as an argument).  Nothing in the repository is written."""
import os, sys, math, json, io, contextlib, time
import numpy as np
import scipy.linalg as sl
from scipy.linalg import lapack

sys.dont_write_bytecode = True


def find_repo():
    env = os.environ.get("ZF_REPO")
    cands = [env] if env else []
    for start in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        p = start
        for _ in range(12):
            cands.append(p)
            p = os.path.dirname(p)
    cands.append(os.path.join(os.path.expanduser("~"), "new_physics", "zimmerman-formula"))
    for c in cands:
        if c and os.path.exists(os.path.join(c, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")) \
                and os.path.exists(os.path.join(c, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")):
            return c
    raise RuntimeError("repository root not found; set ZF_REPO")


REPO = find_repo()
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
P12 = os.path.join(DEDIR, "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_src = open(P12).read()
_head = _src.split("# ============================================================================================ C1 the amplification")[0]
_trans = _src.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]
_GRID_LINE = "r = np.geomspace(1.0, 2e4, 20000) * KPC"
assert _trans.count(_GRID_LINE) == 1
_trans_on = "def transition_on(rgrid, " + _trans.split("def transition(")[1].replace(_GRID_LINE, "r = rgrid")
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans + "\n" + _trans_on).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
transition, transition_on, Wd, G, MS, KPC, A0, CS, nu_of, FB = [D12[k] for k in (
    "transition", "transition_on", "Wd", "G", "MS", "KPC", "A0", "CS", "nu_of", "FB")]
C_LIGHT = D12["L52"]["c"]
W_M = 0.25
FREE_DEFAULT = os.environ.get("CFG102_BC", "D").upper() == "N"     # chi0 boundary condition: D = Dirichlet chi = t (declared main), N = Neumann (post-hoc variant)
TU = 1.0 / (2 * W_M)
CS2 = CS["1e6K"] ** 2
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
WINS = [(0.0, 0.5), (0.125, 0.625), (0.25, 0.75), (0.375, 0.875), (0.5, 1.0)]
FLAG = (2.5, 1e11, "canonical")
SUN = (0.0, 6e10, "canonical", 8.0)   # z, Mb, foot, r_kpc


def key(z, Mb, f):
    return f"{z}/{Mb:.0e}/{f}"


def hfun(tr):
    """gate-variable response h = t_U 4 pi G nu / (H^2 x_c,eff)  (DE13: transverse A = nu)."""
    return TU * 4 * math.pi * G * nu_of(tr["y"]) / (tr["H"] ** 2 * tr["xce"])


class Grid:
    """discrete radial problem on one grid (SI): nodes r, weights, stiffness geometry."""

    def __init__(self, tr):
        self.tr = tr
        self.r, self.t, self.B, self.rho = tr["r"], tr["t"], tr["B"], tr["rho_b"]
        self.h = hfun(tr)
        self.a = CS2 / (self.rho * self.h ** 2)
        r = self.r
        self.dr = np.diff(r)
        self.rm = 0.5 * (r[1:] + r[:-1])
        w = np.zeros_like(r)
        w[1:] += 0.5 * self.dr
        w[:-1] += 0.5 * self.dr
        self.D = r ** 2 * w
        self.geo = self.rm ** 2 / self.dr          # off = mu * geo
        self.N = len(r)
        self.lnr = np.log(r)
        # a static magnitude scale for residual merit (independent of chi)
        self.scale = np.abs(self.t) + 1.0

    def g_eff(self, m2):
        if m2 == math.inf:
            return self.a
        return self.a * m2 / (self.a + m2)


def grad_energy(Gd, chi, mu, m2):
    """gradient of the discrete energy (per node), the Dirichlet ends included as unknowns (caller masks)."""
    off = mu * Gd.geo
    d = chi[1:] - chi[:-1]
    g = np.zeros_like(chi)
    g[1:] += off * d
    g[:-1] -= off * d
    W, W1, W2 = Wd(chi)
    return g + Gd.D * (m2 * (chi - Gd.t) - Gd.B * W1), W1, W2


def energy(Gd, chi, mu, m2):
    off = mu * Gd.geo
    d = chi[1:] - chi[:-1]
    W = Wd(chi)[0]
    return 0.5 * np.sum(off * d * d) + np.sum(Gd.D * (0.5 * m2 * (chi - Gd.t) ** 2 - Gd.B * W))


def hess_bands(Gd, chi, mu, m2):
    off = mu * Gd.geo
    _, W1, W2 = Wd(chi)
    diag = Gd.D * (m2 - Gd.B * W2)
    diag[1:] += off
    diag[:-1] += off
    return diag, -off


def solve_chi0(Gd, mu, m2, free=None, maxit=300):
    """Background chi0 = t + delta as a LOCAL MINIMUM of the discrete energy (modified Newton: Cholesky-regularised Hessian, Armijo on the exact
    energy difference dE(delta), fall back to the residual merit near convergence).  Unknown is delta = chi - t (no cancellation at t >> 1).
    Dirichlet delta = 0 at both ends unless free (natural / Neumann).  Start: the B = 0 linear solution.
    Returns chi, info(converged, iterations, merit, strict_layer_rel, delta)."""
    free = FREE_DEFAULT if free is None else free
    t = Gd.t
    N = Gd.N
    D = Gd.D
    off = mu * Gd.geo
    sD = np.sqrt(D)
    dt = t[1:] - t[:-1]
    Kt = np.zeros(N)
    Kt[1:] += off * dt
    Kt[:-1] -= off * dt
    sl_ = slice(0, N) if free else slice(1, N - 1)
    n = N if free else N - 2
    Wt = Wd(t)[0]
    sscale = (m2 + mu / Gd.r ** 2) * Gd.scale + Gd.B * 10.0 + 1e-300

    def grad(dl):
        dd = dl[1:] - dl[:-1]
        Kd = np.zeros(N)
        Kd[1:] += off * dd
        Kd[:-1] -= off * dd
        W, W1, W2 = Wd(t + dl)
        return Kt + Kd + D * (m2 * dl - Gd.B * W1), W1, W2

    def dE(dl):
        dd = dl[1:] - dl[:-1]
        W = Wd(t + dl)[0]
        return float(0.5 * np.sum(off * dd * dd) + np.sum(off * dt * dd) + np.sum(D * (0.5 * m2 * dl * dl - Gd.B * (W - Wt))))

    def merit(g):
        return float(np.max(np.abs(g[sl_] / D[sl_]) / sscale[sl_]))

    def sym_bands(W2, lam):
        dg = (D * (m2 - Gd.B * W2)) / D
        dg = dg.copy()
        dg[1:] += off / D[1:]
        dg[:-1] += off / D[:-1]
        of = -off / (sD[1:] * sD[:-1])
        ab = np.zeros((2, n))
        ab[1] = (dg[sl_] if not free else dg) + lam
        ab[0, 1:] = of[sl_.start:sl_.start + n - 1] if not free else of
        return ab

    dl = np.zeros(N)
    # linear start
    g0, W1, W2 = grad(dl)
    ab = sym_bands(np.zeros(N), 0.0)
    try:
        c, _ = lapack.dpbtrf(ab.copy(), lower=0)
        q, _ = lapack.dpbtrs(c, (-g0[sl_] / sD[sl_]).copy(), lower=0)
        dl[sl_] = q / sD[sl_]
    except Exception:
        pass
    g, W1, W2 = grad(dl)
    m0 = merit(g)
    Ecur = dE(dl)
    its = 0
    for its in range(1, maxit + 1):
        if m0 <= 1e-10:
            break
        # regularised PD system
        solved = False
        for lam in [0.0] + [1e-22 * 10 ** (k / 1.0) for k in range(0, 27)]:
            ab = sym_bands(W2, lam)
            c, info = lapack.dpbtrf(ab.copy(), lower=0)
            if info == 0:
                q, _ = lapack.dpbtrs(c, (-g[sl_] / sD[sl_]).copy(), lower=0)
                p = np.zeros(N)
                p[sl_] = q / sD[sl_]
                solved = True
                break
        if not solved or not np.all(np.isfinite(p)):
            break
        gp = float(g[sl_] @ p[sl_])
        a_ = 1.0
        acc = False
        for _ in range(40):
            new = dl + a_ * p
            En = dE(new)
            gn, W1n, W2n = grad(new)
            mn = merit(gn)
            if (En <= Ecur + 1e-4 * a_ * gp + 1e-13 * abs(Ecur)) or (mn < 0.5 * m0):
                acc = True
                break
            a_ *= 0.5
        if not acc:
            break
        dl, g, W2, m0, Ecur = new, gn, W2n, mn, En
    chi = t + dl
    F = g / D
    Lchi = np.zeros(N)
    Lchi[1:] += off * (chi[1:] - chi[:-1])
    Lchi[:-1] -= off * (chi[1:] - chi[:-1])
    _, W1, _ = Wd(chi)
    terms = np.abs(Lchi / D) + np.abs(m2 * dl) + np.abs(Gd.B * W1) + 1e-300
    inl = (Gd.t > 0) & (Gd.t < 1)
    if not free:
        inl[0] = inl[-1] = False
    strict = float(np.max(np.abs(F[inl]) / terms[inl])) if inl.any() else 0.0
    return chi, dict(converged=bool(m0 <= 1e-8), iterations=its, merit=float(m0), strict_layer_rel=strict, delta=dl)


def ldl_count(diag, offd):
    """number of negative pivots of a symmetric tridiagonal (exact inertia, Sylvester)."""
    cnt = 0
    d = 0.0
    dl = diag.tolist()
    ol = (offd ** 2).tolist()
    d = dl[0]
    cnt = 1 if d < 0 else 0
    for i in range(1, len(dl)):
        d = dl[i] - ol[i - 1] / (d if d != 0 else 1e-300)
        if d < 0:
            cnt += 1
    return cnt


def is_pd(diag, offd, wts):
    """positive definiteness of the scaled tridiagonal (congruence by diag(wts)^-1/2 keeps the inertia)."""
    s = 1.0 / np.sqrt(wts)
    dg = diag * s * s
    of = offd * s[:-1] * s[1:]
    ab = np.zeros((2, len(dg)))
    ab[1] = dg
    ab[0, 1:] = of
    _, info = lapack.dpbtrf(ab, lower=0)
    return info == 0


def win_matrix(Gf, chi0f, mu, m2, mask, mode="cons", gate_field=None):
    """interior tridiagonal of E2 on the window `mask` of the grid Gf.  base = g_eff - B W''(chi0)."""
    _, _, W2 = Wd(chi0f)
    base = Gf.g_eff(m2) - Gf.B * W2
    r = Gf.r[mask]
    dr = np.diff(r)
    rm = 0.5 * (r[1:] + r[:-1])
    w = np.zeros_like(r)
    w[1:] += 0.5 * dr
    w[:-1] += 0.5 * dr
    off = mu * rm ** 2 / dr
    diag = base[mask] * r ** 2 * w
    diag[1:] += off
    diag[:-1] += off
    return diag[1:-1], -off[1:-1], (r ** 2 * w)[1:-1]


def stable_all(Gf, chi0f, mu, m2, fieldvals=None, wins=WINS):
    """True if no negative mode in ANY of the windows (windows in the variable `fieldvals`, default Gf.t)."""
    fv = Gf.t if fieldvals is None else fieldvals
    for lo, hi in wins:
        m = (fv >= lo) & (fv <= hi)
        if m.sum() < 5:
            continue
        dg, of, wt = win_matrix(Gf, chi0f, mu, m2, m)
        if not is_pd(dg, of, wt):
            return False
    return True


def max_neg(Gf, chi0f, mu, m2, fieldvals=None, wins=WINS):
    fv = Gf.t if fieldvals is None else fieldvals
    out = 0
    for lo, hi in wins:
        m = (fv >= lo) & (fv <= hi)
        if m.sum() < 5:
            continue
        dg, of, wt = win_matrix(Gf, chi0f, mu, m2, m)
        out = max(out, ldl_count(dg, of))
    return out


class Layer:
    def __init__(self, z, Mb, foot):
        self.z, self.Mb, self.foot = z, Mb, foot
        self.key = key(z, Mb, foot)
        self.full = Gd = Grid(transition(z, Mb, foot, W_M))
        tr = Gd.tr
        t, r = tr["t"], tr["r"]
        self.ok = bool(((t > 0) & (t < 1)).any())
        ri = float(np.interp(0.996, t[::-1], r[::-1]))
        ro = float(np.interp(0.004, t[::-1], r[::-1]))
        self.fine = Grid(transition_on(np.geomspace(ri, ro, 8000), z, Mb, foot, W_M))
        self.r_edge_t = float(np.interp(0.5, t[::-1], r[::-1]))
        self._chi_cache = {}

    def chi0_on(self, chi_full, grid):
        return np.interp(grid.lnr, self.full.lnr, chi_full)

    def chi0(self, mu, m2, free=None):
        free = FREE_DEFAULT if free is None else free
        k = (mu, m2, free)
        if k not in self._chi_cache:
            if len(self._chi_cache) > 64:
                self._chi_cache.clear()
            if m2 == math.inf:
                self._chi_cache[k] = (self.full.t.copy(), dict(converged=True, iterations=0, rel_resid=0.0))
            else:
                self._chi_cache[k] = solve_chi0(self.full, mu, m2, free=free)
        return self._chi_cache[k]

    def stable(self, mu, m2, mode="cons"):
        if mode == "cons":
            chi, _ = self.chi0(mu, m2)
            cf = self.chi0_on(chi, self.fine)
        else:
            cf = self.fine.t
        return stable_all(self.fine, cf, mu, m2)

    def mu_min(self, m2, mode="cons", lo=20.0, hi=34.0, nstep=24):
        """bisection on log10 mu (assumes monotone: stable above).  Returns mu or None (unstable even at 10^hi)."""
        if not self.stable(10 ** hi, m2, mode):
            return None
        if self.stable(10 ** lo, m2, mode):
            return 10 ** lo
        for _ in range(nstep):
            mid = 0.5 * (lo + hi)
            if self.stable(10 ** mid, m2, mode):
                hi = mid
            else:
                lo = mid
        return 10 ** hi

    def edge_chi(self, chi):
        """radius where chi crosses 1/2 nearest the t-edge (None if no crossing)."""
        r = self.full.r
        s = chi - 0.5
        idx = np.where(s[:-1] * s[1:] < 0)[0]
        if len(idx) == 0:
            return None
        rc = []
        for i in idx:
            f = s[i] / (s[i] - s[i + 1])
            rc.append(r[i] * (r[i + 1] / r[i]) ** f)
        rc = np.array(rc)
        return float(rc[np.argmin(np.abs(np.log(rc / self.r_edge_t)))])


# ------------------------------------------------------------------------------------------------ costs
def cost_setup(z, Mb, foot):
    tr = transition(z, Mb, foot, W_M)
    return Grid(tr)


def phi_chi(Gd, info, m2):
    """Phi_chi = -4 pi G t_U m2 delta/(H^2 x_c), delta = chi0 - t taken from the solver (info['delta'], no cancellation); m2 = inf: use phi_inf."""
    tr = Gd.tr
    return -4 * math.pi * G * TU * m2 * info["delta"] / (tr["H"] ** 2 * tr["xce"])


def phi_inf(Gd, mu):
    """m2 -> inf, chi0 = t: Phi = -4 pi G C t_U (B W'(t) + mu lap t)."""
    tr = Gd.tr
    r, t = Gd.r, Gd.t
    lap = np.gradient(r ** 2 * np.gradient(t, r), r) / r ** 2
    W1 = Wd(t)[1]
    return -4 * math.pi * G * TU * (Gd.B * W1 + mu * lap) / (tr["H"] ** 2 * tr["xce"])


def flagship_costs(Gd, Phi, foot="canonical", Mb=1e11):
    tr = Gd.tr
    a0 = A0[foot]
    rF = math.sqrt(G * Mb * MS / (0.1 * a0))
    gg = -np.gradient(Phi, Gd.r)
    gM = float(nu_of(0.1)) * 0.1 * a0
    return dict(rF_kpc=rF / KPC, phi_over_vf2=float(np.interp(rF, Gd.r, Phi) / tr["vf2"]),
                force_over_gM=float(np.interp(rF, Gd.r, gg) / gM))


def sun_cost(Gd, Phi, rkpc=8.0):
    return float(np.interp(rkpc * KPC, Gd.r, Phi) / Gd.tr["vf2"])


def uv_speed(Gd, m2, mask=None):
    v2 = CS2 + m2 * Gd.h ** 2 * Gd.rho
    if mask is not None:
        v2 = v2[mask]
    return float(np.sqrt(np.max(v2)) / C_LIGHT)


# ------------------------------------------------------------------------------------------------ reporting helpers
class Rep:
    def __init__(self, name):
        self.name, self.checks, self.nums, self.t0 = name, [], {}, time.time()

    def P(self, *a):
        print(*a, flush=True)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append((name, bool(ok), load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def finish(self, mutate, extra=None):
        nlb = sum(1 for _, ok, lb in self.checks if lb and not ok)
        self.P(f"\n  {sum(ok for _, ok, _ in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nlb}   [{time.time() - self.t0:.0f}s]")
        return nlb
