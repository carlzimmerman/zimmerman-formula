"""CFG102-A: controls C1-C6 of cfg102_frozen.py (see that file for the frozen criteria).  Run: python3 cfg102_a_controls.py [> out]"""
import os, sys, math, json, hashlib
from types import SimpleNamespace
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cfg102_common import *
from scipy.linalg import lapack
import cfg102_common as C
import scipy.linalg as sl

R = Rep("A")
P = R.P
fz = open(os.path.join(HERE, "cfg102_frozen.py"), "rb").read()
P("frozen doc sha256 (must equal FROZEN_HASH.txt):", hashlib.sha256(fz).hexdigest())
P("repo root:", "(resolved; not printed)")
OUT = {}
LAYERS = {}
for (z, Mb, f) in GAL:
    LAYERS[key(z, Mb, f)] = Layer(z, Mb, f)
P("layers with a gate layer:", sum(L.ok for L in LAYERS.values()), "/ 24")
rng = np.random.default_rng(1)

# ----------------------------------------------------------------------------------------------- C6
P("\nC6  pointwise sign test vs DE12's c_gate2 > c_s^2 (fine grids, all 24 layers)")
bad = 0; tot = 0; worst = 0.0
for k, L in LAYERS.items():
    Gf = L.fine
    W2 = Wd(Gf.t)[2]
    marg_mine = Gf.a - Gf.B * W2                 # < 0 : unstable
    cg2 = Gf.tr["c_gate2"]["perp"]
    a_bool = marg_mine < 0
    b_bool = cg2 > CS2
    mism = a_bool != b_bool
    if mism.any():
        rel = np.abs(marg_mine[mism]) / Gf.a[mism]
        worst = max(worst, float(rel.max()))
        bad += int(np.sum(rel > 1e-12))
    tot += len(a_bool)
R.check("C6 pointwise instability sign (a - B W'' < 0) equals DE12's (c_gate^2 > c_s^2)", f"nodes {tot}; mismatches beyond 1e-12 relative margin: {bad}; worst mismatch margin {worst:.1e}", bad == 0)

# ----------------------------------------------------------------------------------------------- C2
P("\nC2  discrete energy / gradient / Hessian consistency (finite differences)")
L = LAYERS[key(0.25, 1e11, "canonical")]
sub = slice(0, 8000, 20)
trs = {k: (v[sub] if isinstance(v, np.ndarray) and v.shape == L.fine.r.shape else v) for k, v in L.fine.tr.items() if k in ("r", "t", "rho_b", "B", "y", "H", "xce")}
Gs = Grid(trs)
mu, m2 = 1e27, 1e-12
chi = 0.5 + 0.3 * np.sin(np.linspace(0, 7, Gs.N)) + 0.01 * rng.standard_normal(Gs.N)
g0, _, _ = grad_energy(Gs, chi, mu, m2)
v = rng.standard_normal(Gs.N)
eps = 1e-5
Ep, Em = energy(Gs, chi + eps * v, mu, m2), energy(Gs, chi - eps * v, mu, m2)
gd = (Ep - Em) / (2 * eps)
rel_g = abs(gd / float(g0 @ v) - 1)
gp, _, _ = grad_energy(Gs, chi + eps * v, mu, m2)
gm, _, _ = grad_energy(Gs, chi - eps * v, mu, m2)
Hv_fd = (gp - gm) / (2 * eps)
dg, of = hess_bands(Gs, chi, mu, m2)
Hv = dg * v
Hv[:-1] += of * v[1:]
Hv[1:] += of * v[:-1]
rel_H = float(np.max(np.abs(Hv_fd - Hv) / (np.abs(Hv) + 1e-3 * np.max(np.abs(Hv)))))
# dense symmetry on 30 nodes
n = 30
Gs2 = Grid({k: (v_[:n] if isinstance(v_, np.ndarray) else v_) for k, v_ in trs.items()})
c2 = chi[:n].copy()
Hd = np.zeros((n, n))
for j in range(n):
    e = np.zeros(n); e[j] = 1.0
    gp, _, _ = grad_energy(Gs2, c2 + 1e-5 * e, mu, m2)
    gm, _, _ = grad_energy(Gs2, c2 - 1e-5 * e, mu, m2)
    Hd[:, j] = (gp - gm) / 2e-5
sym = float(np.max(np.abs(Hd - Hd.T)) / np.max(np.abs(Hd)))
d2, o2 = hess_bands(Gs2, c2, mu, m2)
Hb = np.diag(d2) + np.diag(o2, 1) + np.diag(o2, -1)
band = float(np.max(np.abs(Hd - Hb)) / np.max(np.abs(Hb)))
R.check("C2 gradient = FD of energy, Hessian-vector = FD of gradient (1e-6), dense FD Hessian symmetric and equal to the tridiagonal (1e-6)",
        f"grad {rel_g:.1e}; Hv {rel_H:.1e}; dense asym {sym:.1e}; dense vs bands {band:.1e}", max(rel_g, rel_H, sym, band) < 1e-6)

# ----------------------------------------------------------------------------------------------- C3
P("\nC3  closed-form limit: constant coefficients, radial Dirichlet window, lowest eigenvalue = mu (pi/L)^2 + g")
N = 4000
rr = np.linspace(2.0, 5.0, N)
fake = SimpleNamespace(r=rr, B=np.zeros(N), g_eff=lambda m2: 0.7 * np.ones(N))
mu3 = 3.0
mask = np.ones(N, bool)
dgn, ofn, wt = win_matrix(fake, np.zeros(N), mu3, 1.0, mask)
ev = sl.eigh_tridiagonal(dgn / wt, ofn / np.sqrt(wt[:-1] * wt[1:]), select="i", select_range=(0, 0), eigvals_only=True)[0]
exact = mu3 * (math.pi / 3.0) ** 2 + 0.7
R.check("C3 lowest eigenvalue vs mu (pi/L)^2 + g", f"{ev:.6f} vs {exact:.6f} (rel {abs(ev / exact - 1):.1e})", abs(ev / exact - 1) < 1e-3)

# ----------------------------------------------------------------------------------------------- C4
P("\nC4  Schur elimination = 2-field inertia (Haynsworth)")
ok4 = True; det4 = []; anyneg = False
for k in (key(0.25, 1e11, "canonical"), key(2.5, 1e11, "canonical"), key(4.0, 1e10, "alt")):
    L = LAYERS[k]
    Gf = L.fine
    idx = np.arange(0, 8000, 32)
    trs = {kk: (vv[idx] if isinstance(vv, np.ndarray) and vv.shape == Gf.r.shape else vv) for kk, vv in Gf.tr.items() if kk in ("r", "t", "rho_b", "B", "y", "H", "xce")}
    Gs = Grid(trs)
    it = int(np.argmin(np.abs(Gs.t - 0.5)))
    unit = Gs.B[it] * Gs.r[it] ** 2
    m2c = 1e-12
    for fac in (1e-4, 1e-2, 1.0, 1e2):
        mu = fac * unit
        _, _, W2 = Wd(Gs.t)
        n = Gs.N
        off = mu * Gs.geo
        Kd = Gs.D * 0.0
        Kd[1:] += off
        Kd[:-1] += off
        K = np.diag(Kd) - np.diag(off, 1) - np.diag(off, -1)
        Dm = np.diag(Gs.D)
        H2 = np.block([[K + np.diag(Gs.D * (m2c - Gs.B * W2)), -Dm * m2c], [-Dm * m2c, np.diag(Gs.D * (Gs.a + m2c))]])
        s = 1 / np.sqrt(np.concatenate([Gs.D, Gs.D]))
        H2s = H2 * s[:, None] * s[None, :]
        # drop Dirichlet end nodes of both fields
        keep = np.concatenate([np.arange(1, n - 1), n + np.arange(1, n - 1)])
        ev2 = sl.eigvalsh(H2s[np.ix_(keep, keep)])
        n2 = int(np.sum(ev2 < 0))
        base = Gs.g_eff(m2c) - Gs.B * W2
        Hr = np.diag(base * Gs.D) + np.diag(Kd) - np.diag(off, 1) - np.diag(off, -1)
        Hrs = Hr * s[:n, None] * s[None, :n]
        ev1 = sl.eigvalsh(Hrs[1:-1, 1:-1])
        n1 = int(np.sum(ev1 < 0))
        det4.append((k, fac, n2, n1))
        ok4 &= (n1 == n2)
        anyneg |= n1 > 0
P("    (key, mu/(B r^2), n_neg 2-field, n_neg Schur): " + str(det4))
R.check("C4 Schur count equals the 2-field count in all 12 cases, and the test has teeth (some count > 0)", f"equal={ok4}; some negative={anyneg}", ok4 and anyneg)

# ----------------------------------------------------------------------------------------------- C5a
P("\nC5a  m2 large: chi0 -> t inside the layer")
L = LAYERS[key(0.25, 1e11, "canonical")]
chi, info = L.chi0(2e28, 1e-3)
inl = (L.full.t > 0) & (L.full.t < 1)
dmax = float(np.max(np.abs(chi - L.full.t)[inl]))
R.check("C5a m2 = 1e-3, mu = 2e28: max |chi0 - t| in the layer <= 1e-3 and solver converged", f"{dmax:.2e}; {info}", dmax <= 1e-3 and info["converged"])

# ----------------------------------------------------------------------------------------------- C5c / C7 (added after run 1 of B: solver rewritten)
P("\nC5c  the solver's chi0 is an independent-implementation stationary point and a local minimum; C7 grid-resolution independence of the costs")
okc = True; det = []
for k in (key(0.25, 1e11, "canonical"), key(2.5, 1e11, "canonical"), key(4.0, 1e12, "alt")):
    L = LAYERS[k]
    for m2c in (1e-12, 1e-16):
        chi, info = L.chi0(2e28, m2c)
        Gd = L.full
        g, W1, W2 = grad_energy(Gd, chi, 2e28, m2c)      # chi-form gradient (independent of the solver's delta-form)
        inl = (Gd.t > -0.5) & (Gd.t < 10.0)
        inl[0] = inl[-1] = False
        s_ = (m2c + 2e28 / Gd.r ** 2) * Gd.scale + Gd.B * 10.0
        res = float(np.max(np.abs(g[inl] / Gd.D[inl]) / s_[inl]))
        dg, of = hess_bands(Gd, chi, 2e28, m2c)
        Dh = Gd.D
        Sd = dg[1:-1] / Dh[1:-1]
        So = of[1:-1] / np.sqrt(Dh[1:-1][1:] * Dh[1:-1][:-1])
        ab = np.zeros((2, len(Sd))); ab[1] = Sd; ab[0, 1:] = So
        _, inf_ = lapack.dpbtrf(ab, lower=0)
        pd = (inf_ == 0)
        det.append((k, m2c, f"{res:.1e}", "PD" if pd else "notPD", info["converged"]))
        okc &= (res < 1e-7) and pd and info["converged"]
P("    (layer, m2, in-layer residual [chi-form gradient], chi-only Hessian, converged): " + str(det))
R.check("C5c chi0 is a stationary point (independent chi-form gradient, in-layer residual < 1e-7 of the static scale) AND a local minimum (chi-only Hessian PD)", f"{okc}", okc)
def sub(Gd, k):
    return Grid({kk: (vv[::k] if isinstance(vv, np.ndarray) and vv.shape == Gd.r.shape else vv) for kk, vv in Gd.tr.items()})
GF_ = cost_setup(*FLAG); GS_ = cost_setup(SUN[0], SUN[1], SUN[2])
worst = 0.0; rows7 = []
for m2c, muc in ((1e-12, 1.4736e28), (1e-10, 1.5e28)):
    for lab, G0 in (("F", GF_), ("S", GS_)):
        vals = []
        for kk in (1, 2, 4):
            Gd = sub(G0, kk) if kk > 1 else G0
            chi, info = solve_chi0(Gd, muc, m2c)
            ph = phi_chi(Gd, info, m2c)
            vals.append(flagship_costs(Gd, ph)["phi_over_vf2"] if lab == "F" else sun_cost(Gd, ph))
        worst = max(worst, abs(vals[2] / vals[0] - 1)); rows7.append((m2c, lab, vals))
P("    " + str(rows7))
R.check("C7 flagship / Sun potentials unchanged (<= 1%) between the 20000-node grid and a 5000-node subsample", f"worst {worst:.2e}", worst < 0.01)

# ----------------------------------------------------------------------------------------------- C1
P("\nC1  m2 = inf (chi0 = t, g_eff = a): per-layer minimal mu, eta_U and N1 (DE13's numbers)")
mu_inf = {}
for k, L in LAYERS.items():
    mu_inf[k] = L.mu_min(math.inf, "slaved")
P("    per-layer mu_min(m2=inf) [J/m]:")
for k, v in mu_inf.items():
    P(f"       {k:24s} {v:.4e}   mu_U = t_U^2 mu = {TU ** 2 * v:.4e}   eta_U = {8 * math.pi * G * TU ** 2 * v / C_LIGHT ** 4:.3e}")
mu_uni_inf = max(mu_inf.values())
kk = max(mu_inf, key=mu_inf.get)
eta = 8 * math.pi * G * TU ** 2 * mu_uni_inf / C_LIGHT ** 4
P(f"    universal mu_t = {mu_uni_inf:.4e} J/m (set by {kk}); mu_U = t_U^2 mu = {TU ** 2 * mu_uni_inf:.4e}; eta_U = {eta:.3e}")
GF = cost_setup(*FLAG)
PhiF = phi_inf(GF, mu_uni_inf)
fc = flagship_costs(GF, PhiF)
GS = cost_setup(SUN[0], SUN[1], SUN[2])
PhiS = phi_inf(GS, mu_uni_inf)
sc = sun_cost(GS, PhiS, SUN[3])
P(f"    N1 (m2 = inf): flagship |Phi|/v_f^2 = {abs(fc['phi_over_vf2']):.4g} (r_F = {fc['rF_kpc']:.1f} kpc); Sun |Phi|/v_f^2 = {abs(sc):.4g}")
R.check("C1a eta_U (universal, galaxies) = 3.2e-14 (2 digits)", f"{eta:.3e}", abs(eta / 3.2e-14 - 1) < 0.016)
R.check("C1b N1 flagship 31.8 v_f^2 (3 digits)", f"{abs(fc['phi_over_vf2']):.4g}", abs(abs(fc['phi_over_vf2']) / 31.8 - 1) < 0.0016)
R.check("C1c N1 Sun 2.13e8 v_f^2 (3 digits)", f"{abs(sc):.4g}", abs(abs(sc) / 2.13e8 - 1) < 0.0024)
OUT["mu_inf"] = mu_inf
OUT["mu_uni_inf"] = mu_uni_inf
OUT["eta_U"] = eta
OUT["N1"] = dict(flag=fc, sun=sc)
OUT["controls"] = [(n_, ok, lb) for n_, ok, lb in R.checks]
nlb = R.finish(False)
json.dump(OUT, open(os.path.join(HERE, "cfg102_a_results.json"), "w"), indent=1, default=str)
sys.exit(1 if nlb else 0)
