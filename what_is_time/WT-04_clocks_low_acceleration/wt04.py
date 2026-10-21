#!/usr/bin/env python3
"""WT-04: how clocks tick where the framework's extra gravity acts.

Criteria: FROZEN_CRITERIA.md (0493b61a5, committed alone before this script); amendment A1 (c29715ec0, committed alone, before
any number). Settings: kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; Z = 5.7888; cold energy is real
gravitating mass, no particle species; not theory closed; nothing here says the data favour the framework.

Run (one process, small):
  OMP_NUM_THREADS=1 nice -n 10 python3 wt04.py                  -> wt04.out, wt04_results.json
  WT04_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt04.py    -> wt04_MUTATE.out, wt04_results_MUTATE.json
Exit 0 = every control passes (MAIN) / every tooth bites (MUTATE).
"""
import os, sys, io, json, math, time, resource, contextlib
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("WT04_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
RES = {"lane": "WT-04", "criteria": "0493b61a5", "amendment_A1": "c29715ec0", "mutate": MUT, "checks": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def guard(where):
    if rss() > RSS_LIMIT:
        P(f"RSS GUARD: {rss() / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def jclean(x):
    if isinstance(x, dict): return {str(k): jclean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jclean(v) for v in x]
    if isinstance(x, (np.floating, float)):
        v = float(x); return v if math.isfinite(v) else str(v)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, np.ndarray): return jclean(x.tolist())
    return x


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss() / 1e9, 4)
    json.dump(jclean(RES), open(os.path.join(HERE, f"wt04_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"wt04{TAG}.out"), "w").write("\n".join(OUT) + "\n")


# ===================================================================================================== constants and laws
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # read only: footings and nu_mono
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G, C, MSUN, PC, KPC, MPC = C4.G_SI, C4.C_SI, C4.MSUN, C4.PC, C4.KPC, C4.MPC
K = 4 * math.pi * G
SUP = 5.364; FB = 1.0 / (1.0 + SUP)
UPS = 0.61                                                            # as CFG938 (NGC 3198)
SLIP_INJ = 0.1 if MUT else 0.0                                        # MUTATE T1
KMS = 1e3


def law_S2(gN, a0):                                                   # canonical S2: g_N = g^2/(g + a0)
    gN = np.asarray(gN, float)
    if a0 == 0: return gN.copy()
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono(gN, a0):                                                 # CFG687 primary kernel (record's nu_mono)
    gN = np.asarray(gN, float)
    if a0 == 0: return gN.copy()
    return gN * C4.nu_mono(np.maximum(gN, 1e-300) / a0)


KERN = {"mono": law_mono, "S2": law_S2}


def Wfull(u, a0):
    """CFG938 W_full(u) = [-a0 u - a0^2 ln(1 - u/a0)]/K, series for small u/a0 (no cancellation)."""
    u = np.clip(np.asarray(u, float), 0.0, a0 * (1 - 1e-15)); x = u / a0
    ser = x * x / 2 + x ** 3 / 3 + x ** 4 / 4 + x ** 5 / 5 + x ** 6 / 6
    ex = -x - np.log1p(-x)
    return a0 * a0 * np.where(x < 1e-3, ser, ex) / K


def trapz(y, x):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def cumtrapz0(y, x):
    return np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])


def fret_of(lM):                                                      # CFG804 / CFG416 census, verbatim
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def N_of(Mb_msun):                                                    # CFG804 N_of fixed point, verbatim algebra
    f = 0.10; lMb = math.log10(Mb_msun)
    for _ in range(200):
        lMta = lMb - math.log10(f * FB); fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return 1.0 / f, lMta


edge_of = lambda N: math.sqrt(((2 * SUP * N + 1) ** 2 - 1) / 4)       # CFG804 point-mass edge in r_M

P("=" * 112)
P(f"WT-04  clocks where the extra gravity acts   (criteria 0493b61a5, A1 c29715ec0){'   [MUTATE]' if MUT else ''}")
P("kappa = 1/2 FITTED; footings never pooled; Z = 5.7888; cold energy is real gravitating mass; not theory closed")
P(f"footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")
P("=" * 112)

# ===================================================================================================== (a) sympy derivation
P("\n==================== (a) CLOCK POTENTIAL vs LENSING POTENTIAL (sympy) ====================")
t_, r_, th_, ph_ = sp.symbols("t r theta phi", positive=True)
c_, G_ = sp.symbols("c G", positive=True)
al = sp.Function("alpha")(r_); be = sp.Function("beta")(r_)
X = [t_, r_, th_, ph_]
gm = sp.diag(-sp.exp(2 * al) * c_ ** 2, sp.exp(2 * be), r_ ** 2, r_ ** 2 * sp.sin(th_) ** 2)
gi = gm.inv()
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(gm[d, b], X[cc]) + sp.diff(gm[d, cc], X[b]) - sp.diff(gm[b, cc], X[d]))
                         for d in range(4)) / 2) for cc in range(4)] for b in range(4)] for a in range(4)]
Ric = sp.zeros(4, 4)
for b in range(4):
    for d in range(4):
        Ric[b, d] = sp.simplify(sum(sp.diff(Gam[a][b][d], X[a]) for a in range(4)) - sum(sp.diff(Gam[a][b][a], X[d]) for a in range(4))
                                + sum(Gam[a][a][e] * Gam[e][b][d] for a in range(4) for e in range(4))
                                - sum(Gam[a][d][e] * Gam[e][b][a] for a in range(4) for e in range(4)))
Rs = sp.simplify(sum(gi[b, d] * Ric[b, d] for b in range(4) for d in range(4)))
Gmix = sp.simplify(gi * Ric - sp.eye(4) * Rs / 2)                    # G^mu_nu
m_ = sp.Function("m")(r_); rho_ = sp.Function("rho")(r_); pr_ = sp.Function("p_r")(r_)
beta_m = -sp.log(1 - 2 * G_ * m_ / (r_ * c_ ** 2)) / 2
Gtt = sp.simplify(Gmix[0, 0].subs(be, beta_m).doit())
tt_res = sp.simplify((Gtt + 8 * sp.pi * G_ * rho_ / c_ ** 2).subs(sp.Derivative(m_, r_), 4 * sp.pi * r_ ** 2 * rho_))
Grr = sp.simplify(Gmix[1, 1].subs(be, beta_m).doit())
alp = sp.Symbol("alpha_p")
alpha_p = sp.solve(sp.Eq(Grr.subs(sp.Derivative(al, r_), alp), 8 * sp.pi * G_ * pr_ / c_ ** 4), alp)[0]
alpha_target = (G_ * m_ / c_ ** 2 + 4 * sp.pi * G_ * r_ ** 3 * pr_ / c_ ** 4) / (r_ ** 2 * (1 - 2 * G_ * m_ / (r_ * c_ ** 2)))
a_ok = sp.simplify(alpha_p - alpha_target) == 0 and tt_res == 0
P(f"  G^t_t = -8 pi G rho/c^2 with e^(-2 beta) = 1 - 2Gm/(r c^2), m' = 4 pi r^2 rho: residual {tt_res}")
P(f"  G^r_r = 8 pi G p_r/c^4  =>  alpha' = {sp.simplify(alpha_target)}   (sympy solve agrees: {a_ok})")
eps = sp.Symbol("epsilon", positive=True)                             # 1/c^2
Phi_p = sp.series((c_ ** 2 * alpha_target).subs(c_, 1 / sp.sqrt(eps)), eps, 0, 2).removeO()
P(f"  Phi' = c^2 alpha' = {sp.expand(Phi_p)}   [eps = 1/c^2; the G^2 m^2 term is nonlinear GR, common to both theories]")
# isotropic coordinates at linear order: r = rt (1 - eps Psi(rt)), e^beta dr = e^mu drt with e^mu = r/rt
rt = sp.Symbol("rtilde", positive=True); Psi = sp.Function("Psi")(rt); mt = sp.Function("m")(rt)
rr = rt * (1 - eps * Psi)
iso = sp.series(sp.exp(G_ * mt * eps / rr) * sp.diff(rr, rt) - rr / rt, eps, 0, 2).removeO()
Psi_sol = sp.solve(sp.Eq(sp.expand(iso).coeff(eps, 1), 0), sp.Derivative(Psi, rt))
psi_ok = len(Psi_sol) == 1 and sp.simplify(Psi_sol[0] - G_ * mt / rt ** 2) == 0
P(f"  isotropic transform (linear): Psi' = {Psi_sol[0] if Psi_sol else None}   (= G m/r^2: {psi_ok})")
dPhi_fw = sp.simplify(Phi_p - Phi_p.subs(pr_, 0))
P(f"  framework minus G0 at the same T00 (same m, same Psi): delta Phi' = {sp.simplify(dPhi_fw / eps)} / c^2")
P("  => Phi_clock - Phi_L = (Phi - Psi)/2 with (Phi - Psi)' = 4 pi G r p_r / c^2. With the tether p_r = -W_full(u) < 0:")
P("     the clock potential is SHALLOWER than lensing's by a stress term; at p_r = 0 it is an identity (Phi = Psi).")
# K2c: Schwarzschild exterior
M_ = sp.Symbol("M", positive=True)
ext = sp.simplify(Phi_p.subs({pr_: 0, m_: M_}).subs(eps, 0))
k2c = sp.simplify(ext - G_ * M_ / r_ ** 2) == 0 and sp.simplify(Psi_sol[0].subs(mt, M_) - G_ * M_ / rt ** 2) == 0
RES["a_sympy"] = dict(alpha_prime=str(alpha_target), Phi_prime=str(sp.expand(Phi_p)), Psi_prime=str(Psi_sol[0]),
                      delta_Phi_prime=str(dPhi_fw), solve_agrees=bool(a_ok), psi_ok=bool(psi_ok))
chk("A_sympy_derivation", a_ok and psi_ok, "alpha' from G^r_r; Psi' = Gm/r^2; delta Phi' = 4 pi G r p_r/c^2 (exact at fixed T00)")
chk("K2c_exterior_Phi_eq_Psi", k2c, "p = 0 exterior: Phi' = Psi' = GM/r^2 (Phi = Psi = -GM/r, gamma_PPN = 1)")
P("  IDENTITY FLAGS (no verdict weight): (i) the clock rate g_00 IS the potential that moves slow baryons (minimal coupling,")
P("  both theories), so clock data = dynamics data exactly; (ii) clock vs lensing differ only by (Phi - Psi)/2, set by p_r.")
guard("A")

# ===================================================================================================== K1a: CFG938 S4 cluster
P("\n==================== K1a: CFG938 S4 cluster slip reproduced ====================")
R938 = json.load(open(os.path.join(LANES, "CFG938_medium_continuum_eft", "cfg938_results.json")))["S4"]["rows"]
k1a_ok = True
for f in FOOTS:
    a0 = A0[f]; M = 1.5e14 * 1.989e30; rr_ = 1000.0 * 3.0857e19
    gg = float(law_S2(G * M / rr_ ** 2, a0)); uu = gg * a0 / (gg + a0)
    s = 4 * math.pi * G * rr_ * float(Wfull(uu, a0)) / (C ** 2 * gg)
    tgt = R938[f"{f}|cluster"]["W"]["s_grad"]; rel = abs(s / tgt - 1)
    k1a_ok &= rel < 1e-6
    P(f"  [{f}] s_grad(W) = {s:.6e}  vs committed {tgt:.6e}  (rel {rel:.1e})")
chk("K1a_CFG938_cluster_slip", k1a_ok, "reproduces 5.0780e-6 / 5.7916e-6 to < 1e-6")

# ===================================================================================================== K1b: CFG804
P("\n==================== K1b: CFG804 census N and edge ====================")
Nk, lk = N_of(10 ** 10.5)
e10 = edge_of(10.0)
k1b = abs(Nk - 10) < 1e-6 and abs(lk - 12.30) < 0.01 and abs(e10 - 54.1) < 0.05
P(f"  log M_b 10.5 -> N = {Nk:.6f}, log M_ta = {lk:.4f}; edge(N=10) = {e10:.3f} r_M (CFG804 bin 1: 54 r_M)")
chk("K1b_CFG804_census_edge", k1b, f"N {Nk:.6f}, log M_ta {lk:.3f}, edge {e10:.2f} r_M")

# ===================================================================================================== K2a, K2b, K3, K4
P("\n==================== K2/K3/K4: integrator and kinematics controls ====================")
Rsun, Msun_ = 6.957e8, MSUN
rg = np.geomspace(Rsun, Rsun * 1e6, 200001)
dsun = (trapz(G * Msun_ / rg ** 2, rg) + G * Msun_ / rg[-1]) / C
chk("K2a_sun_surface_redshift", abs(dsun / KMS / 0.636 - 1) < 1e-3 and abs(dsun / (G * Msun_ / (Rsun * C)) - 1) < 1e-4,
    f"integrator {dsun / KMS:.5f} km/s; analytic GM/(Rc) {G * Msun_ / (Rsun * C) / KMS:.5f} km/s (textbook 0.636)")
bP, MP = 1.0 * KPC, 1e10 * MSUN
rg = np.concatenate([[0.0], np.geomspace(1e-6 * bP, 1e6 * bP, 200001)])
gP = G * MP * rg / (rg ** 2 + bP ** 2) ** 1.5
phi0 = -(trapz(gP, rg) + G * MP / rg[-1])
chk("K2b_plummer_centre", abs(phi0 / (-G * MP / bP) - 1) < 1e-4, f"Phi(0) numeric/analytic = {phi0 / (-G * MP / bP):.7f}")
rsN, rhosN = 0.3 * MPC, 1e-22
gN_nfw = lambda x: (lambda xx: G * 4 * math.pi * rhosN * rsN ** 3 * (np.log1p(xx / rsN) - (xx / rsN) / (1 + xx / rsN)) / xx ** 2)(
    np.maximum(x, 1e-6 * rsN))                                        # run-1 fix (A2): x = 0 gave 0/0 = nan
rg = np.concatenate([[0.0], np.geomspace(1e-7 * rsN, 30 * rsN, 200001)])
dnum = cumtrapz0(gN_nfw(rg), rg)
dana = -4 * math.pi * G * rhosN * rsN ** 3 * np.log1p(rg[1:] / rsN) / rg[1:] + 4 * math.pi * G * rhosN * rsN ** 2
chk("K3_NFW_potential", np.max(np.abs(dnum[1:] - dana) / np.abs(dana).max()) < 1e-4,
    f"max |numeric - analytic|/max = {np.max(np.abs(dnum[1:] - dana)) / np.abs(dana).max():.2e}")
rng = np.random.default_rng(404)


def lightcone_mc(sig, n, Lslab):
    """particles uniform in a slab, Gaussian v_z, antithetic pairs sharing D0; keep those whose past-light-cone crossing
    (t + (D0 + v t)/c = 0  ->  D_x = D0 c/(c + v)) falls in the central half. Mean v_z of the kept = the light-cone shift."""
    h = n // 2
    v = rng.normal(0, sig, h); D0 = rng.uniform(-Lslab, Lslab, h)
    vv = np.concatenate([v, -v]); DD = np.concatenate([D0, D0])
    keep = np.abs(DD * C / (C + vv)) < Lslab / 2
    Nk = keep.sum(); s_ = vv * keep; pair = s_[:h] + s_[h:]
    return s_.sum() / Nk, math.sqrt(np.sum(pair ** 2)) / Nk, float(np.sum(vv ** 2 * keep) / Nk)


mlc, elc, vz2 = lightcone_mc(1000 * KMS, 400000, 10 * MPC)
ztd = np.mean(1 / np.sqrt(1 - np.sum(rng.normal(0, 1000 * KMS, (200000, 3)) ** 2, 1) / C ** 2) - 1) * C
k4a = abs(mlc - vz2 / C) < 3 * elc
k4b = abs(ztd / (1.5 * (1000 * KMS) ** 2 / C) - 1) < 0.01
chk("K4_kinematic_terms", k4a and k4b, f"light cone: MC {mlc / KMS:+.3f} +- {elc / KMS:.3f} km/s vs <v_z^2>/c {vz2 / C / KMS:+.3f}; "
    f"TD: MC {ztd / KMS:.4f} vs (3/2) sigma^2/c {1.5 * (1000 * KMS) ** 2 / C / KMS:.4f} km/s")
mlc2, elc2, vz22 = lightcone_mc(0.05 * C, 400000, 10 * MPC)
P(f"  report-only light-cone run at sigma = 0.05c: shift {mlc2 / C:.5f} c +- {elc2 / C:.5f} vs <v_z^2>/c^2 = {vz22 / C ** 2:.5f}"
  f"  (z = {(mlc2 - vz22 / C) / elc2:+.2f})")
RES["K4"] = dict(lc_mc_kms=mlc / KMS, lc_err_kms=elc / KMS, lc_pred_kms=vz2 / C / KMS, td_mc_kms=ztd / KMS,
                 lc_005c=dict(shift_c=mlc2 / C, err_c=elc2 / C, pred=vz22 / C ** 2))
guard("K")

# ===================================================================================================== (b) isolated galaxies
P("\n==================== (b) TIME-DILATION DEPTH OF ISOLATED GALAXIES ====================")


def load_sparc(name):
    d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", f"{name}_rotmod.dat"), comments="#")
    R = d[:, 0] * KPC; Vg, Vd, Vb = d[:, 3] * KMS, d[:, 4] * KMS, d[:, 5] * KMS
    Vb2 = Vg * np.abs(Vg) + UPS * Vd ** 2 + UPS * Vb ** 2
    return R, np.maximum(Vb2 * R / G, 0.0), d


class Galaxy:
    def __init__(self, R, Menc):
        self.R, self.Menc, self.Mb = R, Menc, float(Menc[-1])

    def Mb_of(self, r):
        r = np.asarray(r, float)
        inner = self.Menc[0] * (r / self.R[0]) ** 3
        mid = np.interp(r, self.R, self.Menc)
        return np.where(r < self.R[0], inner, np.where(r > self.R[-1], self.Mb, mid))

    def gN(self, r):
        return G * self.Mb_of(r) / np.asarray(r, float) ** 2


def galaxy_field(gal, a0, kern, Mc, efe=0.0, edge_fixed=None):
    """returns (Re, g(r) callable, Mcold(r) callable). Law out to Re where phantom = Mc, Keplerian (M_b + Mc) beyond."""
    law = KERN[kern]

    def g_law(r):
        gn = gal.gN(r)
        if efe > 0:                                                    # E1: g = g_N nu((g_N + g_Ne)/a0), report-only
            ge = efe * a0; tot = law(gn + ge, a0)
            return gn * tot / (gn + ge)
        return law(gn, a0)

    def Mph(r):
        r = np.asarray(r, float); return (g_law(r) - gal.gN(r)) * r ** 2 / G

    if edge_fixed is not None:
        Re = edge_fixed; Mc_eff = float(Mph(Re))
    elif (not math.isfinite(Mc)) or a0 == 0:
        Re, Mc_eff = math.inf, math.inf
    else:
        rr = np.geomspace(gal.R[0], 1e6 * MPC, 20001); mp = Mph(rr)
        idx = np.where(mp >= Mc)[0]
        if len(idx) == 0: Re, Mc_eff = math.inf, math.inf
        else:
            i = idx[0]; Re = brentq(lambda x: float(Mph(x)) - Mc, rr[max(i - 1, 0)], rr[i], rtol=1e-13); Mc_eff = Mc

    def g(r):
        r = np.asarray(r, float)
        return np.where(r < Re, g_law(r), G * (gal.Mb_of(r) + (Mc_eff if math.isfinite(Mc_eff) else 0.0)) / r ** 2)

    def Mcold(r):
        r = np.asarray(r, float); return np.where(r < Re, np.maximum(Mph(r), 0.0), Mc_eff)

    return Re, g, Mcold


def depth_L(gal, g, Mcold, L, n_per_dec=4000, brk=()):
    """D_L = (1/c^2)[int_0^L g dr + G M_tot(<L)/L] (A1 item 1); inner piece analytic (g ~ linear in r below 1e-3 kpc)."""
    r0 = 1e-3 * KPC
    nd = max(int(n_per_dec * math.log10(L / r0)), 2000)
    bk = np.array([b for b in brk if math.isfinite(b) and r0 < b < L])
    rg = np.unique(np.concatenate([np.geomspace(r0, L, nd), gal.R[(gal.R > r0) & (gal.R < L)], bk]))
    gv = g(rg)
    I = 0.5 * gv[0] * r0 + trapz(gv * rg, np.log(rg))
    Mt = float(gal.Mb_of(L) + Mcold(L))
    return (I + G * Mt / L) / C ** 2


def phi_profile(gal, g, Mcold, L, rq):
    """Phi(r)/c^2 at radii rq with Phi(inf) = 0, using D_L matching at L."""
    r0 = 1e-3 * KPC
    rg = np.unique(np.concatenate([np.geomspace(r0, L, 60000), gal.R[(gal.R > r0) & (gal.R < L)], rq[rq < L]]))
    gv = g(rg); cum = 0.5 * gv[0] * r0 + cumtrapz0(gv, rg)
    DL = (cum[-1] + G * float(gal.Mb_of(L) + Mcold(L)) / L) / C ** 2
    return np.interp(rq, rg, cum) / C ** 2 - DL, DL                   # Phi(r)/c^2 = [Phi(r)-Phi(0) - (Phi(inf)-Phi(0))]/c^2


def delta_phi_tether(Mcold, a0, Re, rq, Lmax):
    """delta Phi(r)/c^2 = +int_r^inf 4 pi G r' W(u)/c^4 dr', u = G M_cold(<r)/r^2 (framework minus G0 at the same T00)."""
    rg = np.geomspace(1e-3 * KPC, Lmax, 80000)
    u = G * Mcold(rg) / rg ** 2
    integ = 4 * math.pi * G * rg * Wfull(u, a0) / C ** 4
    cum = cumtrapz0(integ, rg); tot = cum[-1]
    Mc_end = float(Mcold(rg[-1]))
    tail = (G * Mc_end) ** 2 / (4 * C ** 4 * Lmax ** 2)                # u^2/(2K) tail beyond Lmax
    return np.interp(rq, rg, tot - cum) + tail


GAL = {}
depth = {}
FINITE = {}
Fb, Fa = [], []
for name in ("NGC3198", "DDO154"):
    R, Menc, raw = load_sparc(name); gal = Galaxy(R, Menc); GAL[name] = gal
    Nn, lMta = N_of(gal.Mb / MSUN)
    vflat = float(raw[-1, 1])
    P(f"\n  {name}: M_b = {gal.Mb / MSUN:.3e} Msun (Upsilon {UPS}), R_last = {R[-1] / KPC:.2f} kpc, V_obs(last) {vflat:.1f} km/s, "
      f"census N = {Nn:.3f} (log M_ta {lMta:.2f}), supply M_c = {SUP * Nn * gal.Mb / MSUN:.3e} Msun")
    # Newtonian baryons only
    DN = (0.5 * float(gal.gN(1e-3 * KPC)) * 1e-3 * KPC + trapz(gal.gN(np.geomspace(1e-3 * KPC, R[-1], 200001)),
                                                            np.geomspace(1e-3 * KPC, R[-1], 200001)) + G * gal.Mb / R[-1]) / C ** 2
    depth[name] = {"Newton": DN}
    for f in FOOTS:
        a0 = A0[f]; Mc = SUP * Nn * gal.Mb
        rM = math.sqrt(G * gal.Mb / a0)
        Re, g, Mcold = galaxy_field(gal, a0, "S2", Mc)
        D10, D1000 = depth_L(gal, g, Mcold, 10 * Re, brk=(Re,)), depth_L(gal, g, Mcold, 1000 * Re, brk=(Re,))
        fin = math.isfinite(Re) and abs(D1000 / D10 - 1) < 1e-6
        # no-edge law
        _, gne, Mne = galaxy_field(gal, a0, "S2", math.inf)
        Dne = {f"{L}Mpc": depth_L(gal, gne, Mne, L * MPC) for L in (1, 10, 100)}
        Dne10, Dne1000 = depth_L(gal, gne, Mne, 10 * Re), depth_L(gal, gne, Mne, 1000 * Re)
        # variants (report only)
        Rem, gm_, Mcm = galaxy_field(gal, a0, "mono", Mc); Dmono = depth_L(gal, gm_, Mcm, 10 * Rem, brk=(Rem,))
        R3, g3, M3 = galaxy_field(gal, a0, "S2", Mc, edge_fixed=3 * MPC); D3 = depth_L(gal, g3, M3, 30 * MPC)
        Re2, g2, M2 = galaxy_field(gal, a0, "S2", 2 * Mc); D2 = depth_L(gal, g2, M2, 10 * Re2, brk=(Re2,))
        efe = {}
        for ge in (0.01, 0.03):
            Ree, ge_, Mce = galaxy_field(gal, a0, "S2", Mc, efe=ge)
            efe[f"E1_{ge}_edge_Re_kpc"] = Ree / KPC
            efe[f"E1_{ge}_edge"] = depth_L(gal, ge_, Mce, 10 * Ree if math.isfinite(Ree) else 1e4 * MPC, brk=(Ree,))
            _, gx, Mx = galaxy_field(gal, a0, "S2", math.inf, efe=ge)
            efe[f"E1_{ge}_noedge_100Mpc"] = depth_L(gal, gx, Mx, 100 * MPC)
            efe[f"E1_{ge}_noedge_10Gpc"] = depth_L(gal, gx, Mx, 1e4 * MPC)
        # clock contrast and tether stress (framework minus G0)
        rq = np.array([1e-3 * KPC, 10 * KPC, 30 * KPC, R[-1], Re, 3 * Re])
        phi, DL = phi_profile(gal, g, Mcold, 10 * Re, rq)
        phiN_q = np.array([-(DN - (trapz(gal.gN(np.geomspace(1e-3 * KPC, x, 20001)), np.geomspace(1e-3 * KPC, x, 20001)))
                              / C ** 2) for x in rq])
        dphi = delta_phi_tether(Mcold, a0, Re, rq, 1000 * Re) + SLIP_INJ * np.abs(phi)
        Fb.append(float(dphi[0] / DL)); Fa.append(float(np.max(np.abs(dphi / phi))))
        Dkey = dict(Re_kpc=Re / KPC, Re_over_rM=Re / rM, D_law=D10, D_L1000Re=D1000, finite=fin, ratio_law_newton=D10 / DN,
                    noedge=Dne, noedge_10Re=Dne10, noedge_1000Re=Dne1000, D_mono=Dmono, D_edge3Mpc=D3, D_supply_x2=D2,
                    dD_dlnRe=(D2 - D10) / math.log(Re2 / Re), vRe2_c2=float(g(np.array([Re * 0.999999]))[0]) * Re / C ** 2,
                    efe=efe, phi_c2=dict(zip(["centre", "10kpc", "30kpc", "Rlast", "Re", "3Re"], phi.tolist())),
                    phiN_c2=dict(zip(["centre", "10kpc", "30kpc", "Rlast", "Re", "3Re"], phiN_q.tolist())),
                    dphi_tether_c2=dict(zip(["centre", "10kpc", "30kpc", "Rlast", "Re", "3Re"], dphi.tolist())),
                    F_b=float(dphi[0] / DL), F_a=float(np.max(np.abs(dphi / phi))),
                    lag_over_13p8Gyr_yr=D10 * 13.8e9, lagN_over_13p8Gyr_yr=DN * 13.8e9)
        depth[name][f] = Dkey; FINITE[f"{name}|{f}"] = fin
        P(f"  [{f}] edge R_e = {Re / KPC:.1f} kpc = {Re / rM:.2f} r_M | D(law+edge) = {D10:.4e} (FINITE: {fin}; D_L 10R_e vs "
          f"1000R_e rel {abs(D1000 / D10 - 1):.1e}) | D(Newton) = {DN:.4e} | law/Newton = {D10 / DN:.2f}")
        P(f"         no edge: D_L(1, 10, 100 Mpc) = {Dne['1Mpc']:.4e}, {Dne['10Mpc']:.4e}, {Dne['100Mpc']:.4e}  (grows ~ v^2 ln L)")
        P(f"         variants: nu_mono {Dmono:.4e} | edge at 3 Mpc {D3:.4e} | supply x2 {D2:.4e} (dD/dlnR_e = {Dkey['dD_dlnRe']:.3e}, "
          f"v(R_e)^2/c^2 = {Dkey['vRe2_c2']:.3e}) | E1 EFE 0.01/0.03 a0 with edge {efe['E1_0.01_edge']:.4e} / {efe['E1_0.03_edge']:.4e}; "
          f"no edge (100 Mpc, 10 Gpc) {efe['E1_0.01_noedge_100Mpc']:.4e}, {efe['E1_0.01_noedge_10Gpc']:.4e} / "
          f"{efe['E1_0.03_noedge_100Mpc']:.4e}, {efe['E1_0.03_noedge_10Gpc']:.4e}")
        P(f"         Phi/c^2 (law): centre {phi[0]:.4e}, 10 kpc {phi[1]:.4e}, 30 kpc {phi[2]:.4e}, R_e {phi[4]:.4e} | Newton: centre "
          f"{phiN_q[0]:.4e}, 30 kpc {phiN_q[2]:.4e}")
        P(f"         tether stress: delta Phi/c^2 at centre {dphi[0]:+.3e} (F_b = {Dkey['F_b']:.2e}); max |delta Phi/Phi| = {Dkey['F_a']:.2e}")
        P(f"         a clock at the centre loses {D10 * 13.8e9:.0f} yr per 13.8 Gyr against one at infinity (Newton-baryons: "
          f"{DN * 13.8e9:.0f} yr)")
RES["b_depth"] = depth
guard("b")

# ===================================================================================================== (c) clusters
P("\n==================== (c) CLUSTER GRAVITATIONAL REDSHIFT ====================")
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
MG7, R57 = np.asarray(PC7["mg"], float), np.asarray(PC7["R500"], float)
J949 = json.load(open(os.path.join(LANES, "CFG949_clusters_untethered", "cfg949_results.json")))["main"]["B0_primary"]["medians"]


def gas_shape_M(r, R500, rcf=0.15):                                   # beta = 2/3: M ~ x - atan x, cut at 3 Mpc
    rc = rcf * R500; x = np.minimum(r, 3.0) / rc
    return rc ** 3 * (x - np.arctan(x))


ratio = gas_shape_M(np.full_like(R57, 3.0), R57) / gas_shape_M(R57, R57)
k1c = abs(np.median(ratio) - 4.57) < 0.01
chk("K1c_CFG949_gas_extrapolation", k1c, f"median M_gas(<3 Mpc)/M_gas500 = {np.median(ratio):.4f} (16-84%: "
    f"{np.percentile(ratio, 16):.2f}-{np.percentile(ratio, 84):.2f}; CFG949: 4.57 (3.60-5.78))")
CL = {}
for q in (16, 50, 84):
    Mq = float(np.percentile(MG7, q)); sel = np.abs(np.log10(MG7) - math.log10(Mq)) < 0.1
    CL[q] = dict(Mgas500=Mq, R500=float(np.median(R57[sel])), n_sel=int(sel.sum()))
    P(f"  cluster {q}%: M_gas500 = {Mq:.3e} Msun, R500 = {CL[q]['R500']:.3f} Mpc (median of {sel.sum()} within 0.1 dex)")

RGc = np.geomspace(1e-4, 100.0, 8001)                                 # Mpc
RGm = RGc * MPC
M_BCG, A_BCG = 1e12, 15.0 / 1.8153 / 1e3                              # Msun, Mpc (CFG922 convention)


def m_nfw(x):
    x = np.asarray(x, float); return np.where(x < 1e-3, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4, np.log1p(x) - x / (1 + x))


def cluster_reading(cl, reading, a0=None, kern="mono", edge=True, bcg=False):
    """mass model on RGc. Returns dict(g, Mtot, Mtr_tot (BCG-free), Mgas, rt_tot, u (tether field) , info)."""
    Mg = cl["Mgas500"] * gas_shape_M(RGc, cl["R500"]) / gas_shape_M(np.array([cl["R500"]]), cl["R500"])[0]   # Msun
    Mbcg = M_BCG * RGc ** 2 / (RGc + A_BCG) ** 2 if bcg else np.zeros_like(RGc)
    Mb = 1.2 * Mg + Mbcg
    Mb3 = 1.2 * float(Mg[-1]) + (M_BCG if bcg else 0.0)
    gN = G * Mb * MSUN / RGm ** 2
    info = {}
    if reading == "LAW":
        Nn, lMta = N_of(Mb3); Mc = SUP * Nn * Mb3
        gL = KERN[kern](gN, a0); Mph = (gL - gN) * RGm ** 2 / G / MSUN
        Re = math.inf
        if edge and a0 > 0:
            idx = np.where(Mph >= Mc)[0]
            if len(idx):
                i = max(idx[0], 1); Re = float(np.interp(Mc, Mph[i - 1:i + 1], RGc[i - 1:i + 1]))
        Mcold = np.where(RGc < Re, np.maximum(Mph, 0.0), Mc)
        g = np.where(RGc < Re, gL, G * (Mb + Mc) * MSUN / RGm ** 2)
        rt = max(3.0, Re) if math.isfinite(Re) else 10.0
        if not edge: rt = 10.0
        u = G * Mcold * MSUN / RGm ** 2
        info = dict(N=Nn, log_Mta=lMta, Mc=Mc, Re_Mpc=Re, Mb3=Mb3)
    elif reading == "HUT":
        c9, rs9, Mta9 = J949["c"], J949["rs"] / 1e3, J949["Mta"]; rb9 = c9 * rs9
        Mcold = (1 - FB) * Mta9 * m_nfw(np.minimum(RGc, rb9) / rs9) / float(m_nfw(c9))
        g = G * (Mb + Mcold) * MSUN / RGm ** 2
        rt = max(3.0, rb9); u = np.zeros_like(RGc)
        info = dict(c=c9, rs_Mpc=rs9, rb_Mpc=rb9, Mta=Mta9, Mcold_tot=(1 - FB) * Mta9)
    elif reading == "NEWTON":
        Mcold = np.zeros_like(RGc); g = gN; rt = 10.0; u = np.zeros_like(RGc)   # run-1 fix (A2): truncation set by the density, as R-LAW
    Mtr = 1.2 * Mg + Mcold
    rho_tr = rho_of(Mtr); pos = np.where(rho_tr > 1e-12 * rho_tr.max())[0]
    rt = min(rt, float(RGc[pos[-1]])) if len(pos) else rt               # A1 item 3: tracer ends where its density ends
    return dict(g=g, Mtot=Mb + Mcold, Mtr=Mtr, Mgas=Mg, rt=rt, u=u, Mcold=Mcold, info=info)


def rho_of(M):                                                        # Msun/Mpc^3 from cumulative Msun on RGc
    return np.maximum(np.gradient(M, RGc) / (4 * math.pi * RGc ** 2), 0.0)


RBINS = np.array([0.6, 1.6, 3.3, 5.2])
RAPG = np.unique(np.concatenate([np.geomspace(1e-3, 6.0, 160), RBINS, [3.0]]))


def los(model, tracer, extra_phi=None):
    """LOS-weighted profiles on RAPG: Delta_grav (km/s), <sigma^2>/c (km/s), Sigma_tracer."""
    g = model["g"]; rt = model["rt"] if tracer == "tot" else 3.0
    n = rho_of(model["Mtr"] if tracer == "tot" else model["Mgas"]); n = np.where(RGc <= rt, n, 0.0)
    dphi = cumtrapz0(g, RGm) + 0.5 * g[0] * RGm[0]                     # Phi(r) - Phi(0), J/kg (inner piece g ~ r)
    if extra_phi is not None: dphi = dphi + extra_phi
    ng = n * g; nsig = np.concatenate([np.cumsum((0.5 * (ng[1:] + ng[:-1]) * np.diff(RGm))[::-1])[::-1], [0.0]])  # int_r^rt n g dr
    lr = np.log(RGc)
    dg, s2, Sg = [], [], []
    for Rv in RAPG:
        if Rv >= rt: dg.append(0.0); s2.append(0.0); Sg.append(0.0); continue
        zmax = math.sqrt(rt ** 2 - Rv ** 2)
        z = np.concatenate([[0.0], np.geomspace(min(1e-5, 0.1 * zmax), zmax, 3000)])
        rr = np.sqrt(Rv ** 2 + z ** 2); lq = np.log(rr)
        nq = np.interp(lq, lr, n); S0 = trapz(nq, z)
        if S0 <= 0: dg.append(0.0); s2.append(0.0); Sg.append(0.0); continue
        dg.append(-trapz(nq * np.interp(lq, lr, dphi), z) / S0 / C / KMS)
        s2.append(trapz(np.interp(lq, lr, nsig), z) / S0 / C / KMS)
        Sg.append(2 * S0)
    return np.array(dg), np.array(s2), np.array(Sg)


def aperture(prof, Sg, Rap):
    m = RAPG <= Rap + 1e-12; w = Sg[m] * RAPG[m]
    return trapz(prof[m] * w, RAPG[m]) / trapz(w, RAPG[m]) if trapz(w, RAPG[m]) > 0 else float("nan")


def tether_dphi(model, a0):
    """delta Phi(r) - delta Phi(0) (J/kg) from the tether stress, framework minus G0, on RGc."""
    integ = 4 * math.pi * G * RGm * Wfull(model["u"], a0) / C ** 2     # d(delta Phi)/dr = -4 pi G r p_r/c^2 * (-1): p_r = -W
    # delta Phi'(r) = 4 pi G r p_r / c^2 = -4 pi G r W / c^2  ->  delta Phi(r) - delta Phi(0) = -int_0^r 4 pi G r W/c^2 dr
    return -cumtrapz0(integ, RGm)


DSB = (0.0, 2.0, 4.0)
DATA = [("W11", -7.7, 3.0, 3.0), ("S15", -11.0, 7.0, 5.0), ("R23", -11.4, 3.3, 3.3)]   # PROVISIONAL (A1 item 7)
clus = {}
Fc = {f: [] for f in FOOTS}
band = {f: [] for f in FOOTS}
prim = {}
hut = None
for f in FOOTS:
    a0 = A0[f]
    for q in (16, 50, 84):
        for kern in ("mono", "S2"):
            for edge in (True, False):
                for bcg in (False, True):
                    mdl = cluster_reading(CL[q], "LAW", a0, kern, edge, bcg)
                    tdp = tether_dphi(mdl, a0)
                    inj = SLIP_INJ * cumtrapz0(mdl["g"], RGm)
                    for tr in ("tot", "gas"):
                        dg, s2, Sg = los(mdl, tr)
                        dgf, _, _ = los(mdl, tr, extra_phi=tdp + inj)
                        for Rap in (3.0, 6.0):
                            gA = aperture(dg, Sg, Rap); gfA = aperture(dgf, Sg, Rap); sA = aperture(s2, Sg, Rap)
                            Fc[f].append(abs(gfA - gA) / abs(gA))
                            for dsb in DSB:
                                tot = gfA + (2.5 - dsb) * sA
                                key = dict(q=q, kern=kern, edge=edge, bcg=bcg, tracer=tr, Rap=Rap, dsb=dsb, P=tot, grav=gfA,
                                           grav_G0=gA, kin=(2.5 - dsb) * sA, sig2c=sA)
                                band[f].append(key)
                                if q == 50 and kern == "mono" and edge and (not bcg) and tr == "tot" and Rap == 6.0 and dsb == 2.0:
                                    prim[f] = dict(key, info=mdl["info"], profile=dict(zip(map(str, RBINS), [float(np.interp(x, RAPG, dgf)) if np.interp(x, RAPG, Sg) > 0 else float("nan") for x in RBINS])),
                                                   profile_kin=dict(zip(map(str, RBINS), [float((2.5 - dsb) * np.interp(x, RAPG, s2)) for x in RBINS])),
                                                   sigma_los_kms=float(math.sqrt(sA * C * KMS) / KMS))
                    guard("c-loop")
    pr = prim[f]
    P(f"\n  [{f}] R-LAW primary (median cluster, nu_mono, edge, rho_tot tracer, no BCG, R_ap 6 Mpc, delta_SB 2):")
    P(f"         census N = {pr['info']['N']:.3f}, M_b(<3 Mpc) = {pr['info']['Mb3']:.3e}, supply M_c = {pr['info']['Mc']:.3e} Msun, "
      f"edge R_e = {pr['info']['Re_Mpc']:.3f} Mpc")
    P(f"         Delta_grav = {pr['grav']:+.3f} km/s, kinematic (TD + LC - SB) = {pr['kin']:+.3f} km/s (sigma_LOS ~ "
      f"{pr['sigma_los_kms']:.0f} km/s), total P = {pr['P']:+.3f} km/s")
    P("         profile Delta_grav at R = 0.6/1.6/3.3/5.2 Mpc: " + ", ".join(f"{v:+.2f}" for v in pr["profile"].values())
      + " km/s; kinematic: " + ", ".join(f"{v:+.2f}" for v in pr["profile_kin"].values()))
    Ps = np.array([b["P"] for b in band[f]])
    P(f"         band over the declared grid ({len(Ps)} members): [{Ps.min():+.2f}, {Ps.max():+.2f}] km/s; "
      f"Delta_grav alone [{min(b['grav'] for b in band[f]):+.2f}, {max(b['grav'] for b in band[f]):+.2f}]")
    P(f"         tether stress in Delta_grav: max F_c = {max(Fc[f]):.2e} (framework minus G0 at the same T00)")
    blo = min(band[f], key=lambda b: b["P"]); bhi = max(band[f], key=lambda b: b["P"])
    show = lambda b: f"q{b['q']} {b['kern']} edge={b['edge']} bcg={b['bcg']} tracer={b['tracer']} Rap={b['Rap']} dSB={b['dsb']}"
    P(f"         [report only, added after run 1] band ends: lo {blo['P']:+.2f} ({show(blo)}); hi {bhi['P']:+.2f} ({show(bhi)})")
    for qq in (16, 50, 84):
        Pq = [b["P"] for b in band[f] if b["q"] == qq]; Gq = [b["grav"] for b in band[f] if b["q"] == qq]
        P(f"         [report only] cluster {qq}%: P band [{min(Pq):+.2f}, {max(Pq):+.2f}], Delta_grav [{min(Gq):+.2f}, {max(Gq):+.2f}] km/s")

# R-HUT (footing independent), median cluster
hut_band = []
for bcg in (False, True):
    mdl = cluster_reading(CL[50], "HUT", bcg=bcg)
    inj = SLIP_INJ * cumtrapz0(mdl["g"], RGm)
    for tr in ("tot", "gas"):
        dg, s2, Sg = los(mdl, tr, extra_phi=inj)
        for Rap in (3.0, 6.0):
            gA = aperture(dg, Sg, Rap); sA = aperture(s2, Sg, Rap)
            for dsb in DSB:
                k_ = dict(bcg=bcg, tracer=tr, Rap=Rap, dsb=dsb, P=gA + (2.5 - dsb) * sA, grav=gA, kin=(2.5 - dsb) * sA)
                hut_band.append(k_)
                if (not bcg) and tr == "tot" and Rap == 6.0 and dsb == 2.0:
                    hut = dict(k_, info=mdl["info"], profile=dict(zip(map(str, RBINS), [float(np.interp(x, RAPG, dg)) for x in RBINS])),
                               sigma_los_kms=float(math.sqrt(sA * C * KMS) / KMS))
mN = cluster_reading(CL[50], "NEWTON"); dgN, s2N, SgN = los(mN, "tot")
newton_grav = aperture(dgN, SgN, 6.0)
P(f"\n  R-HUT (CFG949 primary-corner medians c {hut['info']['c']:.2f}, r_s {hut['info']['rs_Mpc'] * 1e3:.1f} kpc, r_b {hut['info']['rb_Mpc']:.2f} Mpc, "
  f"M_cold {hut['info']['Mcold_tot']:.3e} Msun; footing independent):")
P(f"         Delta_grav = {hut['grav']:+.3f}, kinematic {hut['kin']:+.3f}, total P = {hut['P']:+.3f} km/s; profile "
  + ", ".join(f"{v:+.2f}" for v in hut["profile"].values()) + " km/s")
Ph = np.array([b["P"] for b in hut_band])
P(f"         band [{Ph.min():+.2f}, {Ph.max():+.2f}] km/s.  Newtonian baryons only (median, rho tracer, 6 Mpc): Delta_grav {newton_grav:+.3f} km/s")
internal = {f: prim[f]["grav"] / hut["grav"] for f in FOOTS}
P("  FRAMEWORK-INTERNAL: Delta_grav(R-LAW)/Delta_grav(R-HUT) = " + ", ".join(f"{f} {internal[f]:.3f}" for f in FOOTS)
  + "  (the law's core deficit seen by clocks)")


def classify(Pmid, Plo, Phi_):
    rows = []; cls_mid = True; tension = False
    for nm, m, ep, em in DATA:
        sig_mid = ep if Pmid > m else em
        zm = (Pmid - m) / sig_mid
        if Plo <= m <= Phi_: zn = 0.0
        else:
            near = Plo if m < Plo else Phi_
            zn = abs(near - m) / (ep if near > m else em)
        rows.append(dict(meas=nm, m=m, z_mid=zm, z_near=zn)); cls_mid &= abs(zm) < 2; tension |= zn >= 3
    cls = "CONSISTENT" if cls_mid else ("TENSION" if tension else "NOT DIAGNOSTIC")
    return cls + " (PROVISIONAL)", rows


DCLS = {}
for f in FOOTS:
    Ps = [b["P"] for b in band[f]]
    DCLS[f"R-LAW|{f}"] = classify(prim[f]["P"], min(Ps), max(Ps))
DCLS["R-HUT"] = classify(hut["P"], float(Ph.min()), float(Ph.max()))
P("\n  DATA CLASS (c), frozen rule:")
for k, (cl_, rows) in DCLS.items():
    P(f"    {k:18s}: {cl_:32s} " + "; ".join(f"{r['meas']} z_mid {r['z_mid']:+.2f}, z_near {r['z_near']:.2f}" for r in rows))
P("    J15 (~ -10 km/s, no uncertainty): reported, not graded.")
RES["c_cluster"] = dict(clusters=CL, primary=prim, hut=hut, newton_grav_median=newton_grav, internal_ratio=internal,
                        band_LAW={f: dict(lo=min(b["P"] for b in band[f]), hi=max(b["P"] for b in band[f]),
                                          grav_lo=min(b["grav"] for b in band[f]), grav_hi=max(b["grav"] for b in band[f])) for f in FOOTS},
                        band_HUT=dict(lo=float(Ph.min()), hi=float(Ph.max())), data=DATA,
                        classes={k: dict(cls=v[0], rows=v[1]) for k, v in DCLS.items()}, Fc_max={f: max(Fc[f]) for f in FOOTS},
                        band_members_LAW=band, band_members_HUT=hut_band)
guard("c")

# G1 comparator (report only): dispersion-supported cold component in R-HUT
mdl = cluster_reading(CL[50], "HUT"); rc_ = rho_of(mdl["Mcold"]) * MSUN / MPC ** 3
nsig_c = np.concatenate([np.cumsum((0.5 * ((rc_ * mdl["g"])[1:] + (rc_ * mdl["g"])[:-1]) * np.diff(RGm))[::-1])[::-1], [0.0]])
dG1 = cumtrapz0(4 * math.pi * G * RGm * nsig_c / C ** 2, RGm)          # p_r = rho sigma^2 > 0: deeper clock potential
dgG1, _, SgG1 = los(dict(mdl, g=mdl["g"]), "tot", extra_phi=dG1)
dg0, _, Sg0 = los(mdl, "tot")
G1frac = abs(aperture(dgG1, SgG1, 6.0) - aperture(dg0, Sg0, 6.0)) / abs(aperture(dg0, Sg0, 6.0))
P(f"  G1 (report only): a dispersion-supported cold halo (p_r = rho sigma^2 > 0) shifts Delta_grav by {G1frac:.2e} (opposite sign to the tether)")
RES["c_cluster"]["G1_fraction"] = G1frac

# ===================================================================================================== (d) Fermat potential
P("\n==================== (d) STRONG-LENS FERMAT POTENTIAL ====================")
Fd = {}
Mlens, alens = 2e11 * MSUN, 5.0 / 1.8153 * KPC
Rl = np.geomspace(0.01 * KPC, 50 * KPC, 400)
lens = Galaxy(Rl, Mlens * Rl ** 2 / (Rl + alens) ** 2)
lens.Mb_of = lambda r, M=Mlens, a=alens: M * np.asarray(r, float) ** 2 / (np.asarray(r, float) + a) ** 2
Nl, _ = N_of(Mlens / MSUN)
for f in FOOTS:
    a0 = A0[f]; Re, g, Mcold = galaxy_field(lens, a0, "S2", SUP * Nl * Mlens)
    rg = np.geomspace(1e-3 * KPC, 1e4 * MPC, 120000)
    u = G * Mcold(rg) / rg ** 2
    dPhip = -4 * math.pi * G * rg * Wfull(u, a0) / C ** 2               # delta Phi' (framework minus G0, same T00)
    gv = g(rg)
    gLfw = gv + 0.5 * dPhip + 0.5 * SLIP_INJ * gv                      # Phi_L' = (Phi' + Psi')/2
    Rimg = np.linspace(2 * KPC, 8 * KPC, 61)

    def alpha(gl):
        out = []
        for Rv in Rimg:
            z = np.concatenate([[0.0], np.geomspace(1e-4 * KPC, 1e4 * MPC, 20000)]); rr = np.sqrt(Rv ** 2 + z ** 2)
            out.append(2 * trapz(np.interp(np.log(rr), np.log(rg), gl) * Rv / rr, z))
        return np.array(out)

    a_fw, a_G0 = alpha(gLfw), alpha(gv)
    dpsi_fw, dpsi_G0 = trapz(a_fw, Rimg), trapz(a_G0, Rimg)
    Fd[f] = abs(dpsi_fw - dpsi_G0) / abs(dpsi_G0)
    P(f"  [{f}] lens M_b 2e11 Msun, census N {Nl:.2f}, edge {Re / KPC:.0f} kpc: Fermat-potential difference (2 -> 8 kpc) "
      f"framework vs G0 at the same T00: fractional {Fd[f]:.2e}; at fixed Sigma_lens: 0 (identity)")
RES["d_fermat"] = Fd
guard("d")

# ===================================================================================================== (e) theory verdict
P("\n==================== (e) THEORY VERDICT (frozen rule: SAME iff every F < 1e-3 on both footings) ====================")
Fall = {}
for f in FOOTS:
    fa = max(depth[n][f]["F_a"] for n in GAL); fb = max(abs(depth[n][f]["F_b"]) for n in GAL)
    Fall[f] = dict(F_a=fa, F_b=fb, F_c=max(Fc[f]), F_d=Fd[f]); Fall[f]["max"] = max(Fall[f].values())
    P(f"  [{f}] F_a {fa:.2e}  F_b {fb:.2e}  F_c {max(Fc[f]):.2e}  F_d {Fd[f]:.2e}  -> max {Fall[f]['max']:.2e}")
same = all(Fall[f]["max"] < 1e-3 for f in FOOTS)
THEORY = "SAME AS GR WITH SAME MASS" if same else "DISTINCT SIGNATURE"
if not same:
    worst = max(((f, k, v) for f in FOOTS for k, v in Fall[f].items() if k != "max"), key=lambda x: x[2])
    THEORY += f" (largest: {worst[1]} on {worst[0]} = {worst[2]:.2e})"
P(f"  THEORY CLASS: {THEORY}")
RES["e_theory"] = dict(F=Fall, cls=THEORY)

# ===================================================================================================== MUTATE teeth
if MUT:
    P("\n==================== MUTATE TEETH ====================")
    t1 = THEORY.startswith("DISTINCT")
    chk("T1_slip_injection_flips_class", t1, f"theory class with s = 0.1 injected: {THEORY}")
    gal = GAL["NGC3198"]; ok2 = True
    DN = depth["NGC3198"]["Newton"]
    Re0, g0, M0 = galaxy_field(gal, 0.0, "S2", SUP * 10 * gal.Mb)
    D0 = depth_L(gal, g0, M0, 100 * MPC)
    ok2 &= abs(D0 / DN - 1) < 1e-6
    m0 = cluster_reading(CL[50], "LAW", 0.0, "mono", True, False); dg0, _, Sg0 = los(m0, "tot")
    g0c = aperture(dg0, Sg0, 6.0)
    ok2 &= abs(g0c / newton_grav - 1) < 1e-6
    chk("T2_a0_zero_gives_Newton", ok2, f"D(a0=0) / D(Newton) = {D0 / DN:.9f}; cluster Delta_grav(a0=0) / baryons-only = {g0c / newton_grav:.9f}")
    Re_main = depth["NGC3198"]["canonical"]["Re_kpc"] * KPC
    _, gi_, Mi_ = galaxy_field(gal, A0["canonical"], "S2", math.inf)
    Da, Db = depth_L(gal, gi_, Mi_, 10 * Re_main), depth_L(gal, gi_, Mi_, 1000 * Re_main)
    t3 = not (abs(Db / Da - 1) < 1e-6)
    chk("T3_no_supply_edge_not_finite", t3, f"N = inf: D_L(10 R_e) {Da:.4e} vs D_L(1000 R_e) {Db:.4e} (rel {abs(Db / Da - 1):.2e}); FINITE fails")
    ok = t1 and ok2 and t3
else:
    ctrl = [k for k in RES["checks"] if k.startswith(("K", "A_"))]
    ok = all(RES["checks"][k]["pass"] for k in ctrl)
    if not ok: P("  A CONTROL FAILED: classes withheld (NOT CLASSIFIED) until a dated amendment fixes it")

P("\n==================== SUMMARY ====================")
P(f"  theory (e): {THEORY}")
for f in FOOTS:
    d1 = depth["NGC3198"][f]; d2 = depth["DDO154"][f]
    P(f"  [{f}] NGC 3198 depth {d1['D_law']:.3e} (Newton {depth['NGC3198']['Newton']:.3e}, x{d1['ratio_law_newton']:.2f}, edge {d1['Re_kpc']:.0f} kpc); "
      f"DDO 154 {d2['D_law']:.3e} (Newton {depth['DDO154']['Newton']:.3e}, x{d2['ratio_law_newton']:.2f}, edge {d2['Re_kpc']:.0f} kpc)")
    P(f"         cluster R-LAW P = {prim[f]['P']:+.2f} km/s (grav {prim[f]['grav']:+.2f}); class {DCLS[f'R-LAW|{f}'][0]}")
P(f"  R-HUT P = {hut['P']:+.2f} km/s (grav {hut['grav']:+.2f}); class {DCLS['R-HUT'][0]}")
P(f"  checks: {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])} pass; peak RSS {rss() / 1e9:.3f} GB; {time.time() - T0:.1f} s")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
RES["ok"] = bool(ok)
dump()
sys.exit(0 if ok else 1)
