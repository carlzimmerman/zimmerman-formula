"""QX4 iteration 1: the action's exact static field (axisymmetric AQUAL solve) on AGC 114905 and Malin 1.

Criteria: FROZEN_CRITERIA.md (c0d7f31b1e), iteration 1. Inputs come from UD1/UD2's committed figure-reading code,
executed read-only (their files are not written). Both footings, never pooled. Kappa = 1/2 FITTED; not theory closed.
One galaxy excludes nothing.

usage: python3 iter1_exact_aqual.py [main|MUTATE] [--quick]
   MUTATE: mu = 1 in the graded runs (must reproduce UD1/UD2's Newtonian chi2); outputs iter1_MUTATE.*
"""
import io, json, os, sys, contextlib, time
import numpy as np
from scipy.special import ellipk
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import aqual as A

MODE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "main"
QUICK = "--quick" in sys.argv
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
UD1 = os.path.join(ROOT, "rebuild_2026_10_22", "UD1_agc114905_udg_rotation", "ud1.py")
UD2 = os.path.join(ROOT, "rebuild_2026_10_22", "UD2_malin1_giant_lsb", "ud2.py")
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
RUNGS = [(120, 36), (240, 72)] if QUICK else [(240, 72), (480, 144)]
OUT, RES = [], {}
MU_ONE = MODE == "MUTATE"


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)


def nu(y): y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))


def label(p): return "RESCUED" if p >= 0.05 else "NOT RESCUED"


def load(path, stop, argv):
    """Execute a UD script's source up to a marker, read-only, in its own namespace (no output files written)."""
    src = open(path).read(); cut = src.index(stop)
    ns = dict(__file__=path, __name__="ud_import")
    old = sys.argv; sys.argv = argv
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], path, "exec"), ns)
    finally:
        sys.argv = old
    return ns


P(f"QX4 iter1 exact AQUAL, mode {MODE}{' QUICK' if QUICK else ''}. kappa = 1/2 FITTED; not theory closed.")
t0 = time.time()

# =================================================================== known answers K1, K2 (solver)
a0c = A.a0_kpc(FOOT["canonical"])
g = A.Grid(0.01, 3000.0, *RUNGS[-1], p=3)
Mp, bp = 1e9, 1.0
rho_pl = lambda R, z: 3 * Mp / (4 * np.pi * bp ** 3) * (1 + (R * R + z * z) / bp ** 2) ** -2.5
Phi, res, it = A.solve(g, g.deposit(rho_pl), a0c)
r = np.array([1.0, 3.0, 10.0, 30.0])
gN = A.G * Mp * r / (r * r + bp * bp) ** 1.5
k1 = float(np.max(np.abs(A.radial_g(g, Phi, r, g.nt // 2) / (nu(gN / a0c) * gN) - 1)))
P(f"K1 Plummer, exact vs algebraic radial g at r = {r.tolist()} kpc: max rel {k1:.2e} (line 1e-3) -> {'PASS' if k1 <= 1e-3 else 'FAIL'}"
  f"  [res {res:.1e}, {it} it]")
Mk, ak = 1e9, 2.0; hk = 0.02 * ak
rho_kz = lambda R, z: Mk * ak / (2 * np.pi * (R * R + ak * ak) ** 1.5) * np.exp(-0.5 * (z / hk) ** 2) / (np.sqrt(2 * np.pi) * hk)
Phi, res, it = A.solve(g, g.deposit(rho_kz), a0c)
r = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
gR = A.G * Mk * r / (r * r + ak * ak) ** 1.5; gmag = A.G * Mk / (r * r + ak * ak)
vex = A.midplane_vc(g, Phi, r)
k2 = float(np.max(np.abs(vex / np.sqrt(nu(gmag / a0c) * gR * r) - 1)))
k2_inplane = (vex / np.sqrt(nu(gR / a0c) * gR * r) - 1)
P(f"K2 Kuzmin h/a 0.02, exact midplane V vs Brada-Milgrom 1995 algebraic form g = nu(|g_N|/a0) g_N (|g_N| just above the"
  f" disc, the point-mass field): max rel {k2:.4f} (line 0.02) -> {'PASS' if k2 <= 0.02 else 'FAIL'}")
P(f"   (reported) the same exact V vs the in-plane RAR form nu(g_N,R/a0) g_N,R: {np.round(k2_inplane, 4).tolist()}"
  f" at R = {r.tolist()} -- the action's exact field sits BELOW the in-plane law where the vertical Newtonian field is large")
RES["K1"] = k1; RES["K2"] = dict(bm95=k2, inplane=k2_inplane.tolist())

# =================================================================== AGC 114905 (UD1)
ud1 = load(UD1, "# ---- K0a", [UD1, "law"])
Rk, V, E = np.asarray(ud1["Rk"]), np.asarray(ud1["V"]), np.asarray(ud1["E"])
vb2_ring = np.asarray(ud1["vb2"]); D0, kas = ud1["D0"], ud1["as2kpc"](ud1["D0"])
zd = ud1["zd_star"](); hg = 1.3
sig_s, sig_g = ud1["sig_star"], ud1["sig_gas"]
AMAX = 80.0


def rho_agc(R, z):
    Ras = R / kas
    S_s = np.where(Ras < AMAX, np.clip(sig_s(Ras), 0, None), 0) * 1e6
    S_g = np.where(Ras < AMAX, np.clip(sig_g(Ras), 0, None), 0) * 1e6
    return S_s / np.cosh(z / zd) ** 2 / (2 * zd) + S_g * np.exp(-0.5 * (z / hg) ** 2) / (np.sqrt(2 * np.pi) * hg)


# =================================================================== Malin 1 (UD2): Sigma by Toomre inversion
ud2 = load(UD2, "# ---- grade", [UD2, "law"])
RT, VT, ET = ud2["RT"], ud2["VT"], ud2["ET"]
dr2 = ud2["dr"]; X2, Y2 = ud2["X"], ud2["Y"]
cols = dict(gas=(0.0, 1.0, 0.0), lsb=(0.0, 1.0, 1.0), hsb=(1.0, 0.55, 0.0))
curves = {}
for nm, col in cols.items():
    c = ud2["curve"](dr2, col, 61, (40, 70)); rr, vv = X2(c[:, 0]), Y2(c[:, 1]); o = np.argsort(rr)
    rr, vv = rr[o], np.maximum(vv[o], 0)
    keep = np.concatenate([[True], np.diff(rr) > 1e-6]); curves[nm] = (rr[keep], vv[keep])
P(f"Malin 1 component curves read: R ranges { {k: [round(v[0][0],2), round(v[0][-1],2)] for k, v in curves.items()} } kpc")


def v2_ext(rr, vv):
    """V^2(r) on [0, inf): curve inside its range (V^2 -> 0 at r -> 0), Keplerian beyond."""
    r_end, v2_end = rr[-1], vv[-1] ** 2
    return lambda q: np.where(q <= r_end, np.interp(q, np.concatenate([[0.0], rr]), np.concatenate([[0.0], vv ** 2])),
                              v2_end * r_end / np.maximum(q, 1e-9))


EPS = 0.3                                                                       # kpc ring softening (numerical; thin-disc limit)


def annulus_v2(edges, Rq, nsub=200):
    """Thin midplane V^2 at Rq of unit-mass uniform annuli (ring sums), one column per annulus."""
    cols = []
    for a, b in zip(edges[:-1], edges[1:]):
        aa = a + (np.arange(nsub) + 0.5) * (b - a) / nsub; m = aa / aa.sum()            # uniform Sigma: mass ~ a da
        def phi(R):
            s2 = (R + aa[:, None]) ** 2 + EPS ** 2; kk = np.clip(4 * aa[:, None] * R / s2, 0, 1 - 1e-12)
            return -np.sum(2 * A.G * m[:, None] / np.pi * ellipk(kk) / np.sqrt(s2), axis=0)
        cols.append(Rq * (phi(Rq * 1.001) - phi(Rq * 0.999)) / (0.002 * Rq))
    return np.array(cols).T


EDGES = np.exp(np.linspace(np.log(0.3), np.log(200.0), 61))
def nnls_sigma(rr, vv, edges=None):
    """A1: non-negative annulus masses matching plotted V^2 (weight 1/V^2) on the plotted range."""
    from scipy.optimize import nnls
    Rq = np.linspace(rr[0], rr[-1], 300); v2 = np.interp(Rq, rr, vv ** 2); w = 1.0 / np.maximum(v2, 1.0)
    E_ = EDGES if edges is None else edges
    Amat = annulus_v2(E_, Rq); m, _ = nnls(Amat * w[:, None], v2 * w)
    area = np.pi * (E_[1:] ** 2 - E_[:-1] ** 2)
    return m / area                                                                  # Msun/kpc^2 per annulus


def sig_from_annuli(sig_ann, edges=None):
    E_ = EDGES if edges is None else edges
    return lambda R: np.where((R >= E_[0]) & (R < E_[-1]),
                              sig_ann[np.clip(np.searchsorted(E_, R, side="right") - 1, 0, len(sig_ann) - 1)], 0.0)


Rs = np.exp(np.linspace(np.log(0.05), np.log(3000.0), 6000))
SIGF = {nm: sig_from_annuli(nnls_sigma(*curves[nm])) for nm in ("gas", "lsb")}
SIG = {nm: SIGF[nm](Rs) for nm in ("gas", "lsb")}
EDGES_A2 = np.exp(np.linspace(np.log(0.3), np.log(curves["gas"][0][-1]), 61))            # A2 (post-result)
SIGF_A2 = {nm: sig_from_annuli(nnls_sigma(*curves[nm], EDGES_A2), EDGES_A2) for nm in ("gas", "lsb")}
Mh_r, Mh_v = curves["hsb"]
Mhsb = lambda q: v2_ext(Mh_r, Mh_v)(q) * q / A.G                                 # Msun inside q (sphere)
qg = np.exp(np.linspace(np.log(1e-3), np.log(3e4), 4000)); Mq = Mhsb(qg)
rho_hsb_tab = np.gradient(Mq, qg) / (4 * np.pi * qg ** 2)


def ring_sum_thin(Sig_tab, Rgrid, Rq):
    """Thin-disc midplane V^2 by ring sums (UD1's method with z -> 0)."""
    a = np.exp(np.linspace(np.log(0.05), np.log(3000.0), 6000)); am = 0.5 * (a[1:] + a[:-1]); da = np.diff(a)
    m = 2 * np.pi * am * np.interp(am, Rgrid, Sig_tab) * da
    def phi(R):
        s2 = (R + am) ** 2 + EPS ** 2; kk = np.clip(4 * am * R / s2, 0, 1 - 1e-12)
        return -np.sum(2 * A.G * m / np.pi * ellipk(kk) / np.sqrt(s2))
    return np.array([R * (phi(R * 1.001) - phi(R * 0.999)) / (0.002 * R) for R in Rq])


k4 = {}
for nm in ("gas", "lsb"):
    vrec = np.sqrt(np.maximum(ring_sum_thin(SIG[nm], Rs, RT), 0)); vplot = np.sqrt(v2_ext(*curves[nm])(RT))
    k4[nm] = float(np.max(np.abs(vrec / vplot - 1)))
    P(f"K4 Malin 1 {nm}: inverted Sigma -> thin ring-sum V {np.round(vrec,1).tolist()} vs plotted {np.round(vplot,1).tolist()}"
      f" max rel {k4[nm]:.4f} (line 0.03) -> {'PASS' if k4[nm] <= 0.03 else 'FAIL'}")
RES["K4"] = k4
k4b = {}
for nm in ("gas", "lsb"):
    vrec = np.sqrt(np.maximum(ring_sum_thin(SIGF_A2[nm](Rs), Rs, RT), 0)); vplot = np.sqrt(v2_ext(*curves[nm])(RT))
    k4b[nm] = float(np.max(np.abs(vrec / vplot - 1)))
    P(f"K4 (A2) Malin 1 {nm}: V {np.round(vrec,1).tolist()} max rel {k4b[nm]:.4f} -> {'PASS' if k4b[nm] <= 0.03 else 'FAIL'};"
      f" mass {np.trapz(2*np.pi*Rs*SIGF_A2[nm](Rs), Rs):.3e}")
RES["K4_A2"] = k4b
P(f"   masses: gas {np.trapz(2*np.pi*Rs*SIG['gas'], Rs):.3e}, LSB {np.trapz(2*np.pi*Rs*SIG['lsb'], Rs):.3e},"
  f" HSB {Mhsb(3e4):.3e} Msun")


def rho_malin(h, SF=None):
    SF = SIGF if SF is None else SF
    def f(R, z):
        r3 = np.sqrt(R * R + z * z)
        disc = (SF["gas"](R) + SF["lsb"](R)) * np.exp(-0.5 * (z / h) ** 2) / (np.sqrt(2 * np.pi) * h)
        return disc + np.interp(r3, qg, rho_hsb_tab)
    return f


vb2_malin = (ud2["comp"]["gas"] ** 2 + ud2["comp"]["lsb"] ** 2 + ud2["comp"]["hsb"] ** 2)

# =================================================================== graded runs
GAL = dict(
    AGC114905=dict(rho=rho_agc, rmin=0.01, rmax=3000.0, R=Rk, V=V, E=E, vb2=vb2_ring, newton_chi2_ud=55.0),
    Malin1=dict(rho=rho_malin(1.0), rmin=0.05, rmax=3.0e4, R=RT, V=VT, E=ET, vb2=vb2_malin, newton_chi2_ud=1752.6),
    Malin1_A2=dict(rho=rho_malin(1.0, SIGF_A2), rmin=0.05, rmax=3.0e4, R=RT, V=VT, E=ET, vb2=vb2_malin, newton_chi2_ud=1752.6),
)
for gname, gd in GAL.items():
    RES[gname] = {}
    sols = {}
    for rung in RUNGS:
        gg = A.Grid(gd["rmin"], gd["rmax"], *rung, p=3); Mc = gg.deposit(gd["rho"])
        PhiN, _, _ = A.solve(gg, Mc, a0c, mu_one=True)
        vN = A.midplane_vc(gg, PhiN, gd["R"])
        sols[rung] = dict(g=gg, Mc=Mc, vN=vN)
    vN = sols[RUNGS[-1]]["vN"]; k3 = float(np.max(np.abs(vN / np.sqrt(gd["vb2"]) - 1)))
    P(f"\n=== {gname}: hemisphere mass x2 = {2*sols[RUNGS[-1]]['Mc'].sum():.4e} Msun")
    P(f"K3 Newton (mu = 1) solver V {np.round(vN,2).tolist()} vs the UD lane's V_bar {np.round(np.sqrt(gd['vb2']),2).tolist()}:"
      f" max rel {k3:.4f} (line 0.01; Malin 1's UD V_bar is the paper's thin-disc curves, ours has h = 1 kpc) -> {'PASS' if k3 <= 0.01 else 'FAIL'}")
    RES[gname]["K3"] = k3
    for f, a0s in FOOT.items():
        a0 = A.a0_kpc(a0s); vex = {}
        for rung in RUNGS:
            s = sols[rung]
            Phi, res, it = A.solve(s["g"], s["Mc"], a0, mu_one=MU_ONE)
            vex[rung] = A.midplane_vc(s["g"], Phi, gd["R"])
        v = vex[RUNGS[-1]]; conv = float(np.max(np.abs(vex[RUNGS[0]] / v - 1)))
        gNs = vN ** 2 / gd["R"]                                                    # solver's own in-plane Newtonian g
        valg_self = np.sqrt((1.0 if MU_ONE else nu(gNs / a0)) * gNs * gd["R"])
        valg_ud = np.sqrt((1.0 if MU_ONE else nu(gd["vb2"] / gd["R"] / a0)) * gd["vb2"])
        c, p = chi2p(gd["V"], gd["E"], v); c_alg, _ = chi2p(gd["V"], gd["E"], valg_ud)
        RES[gname][f] = dict(V_exact=v.tolist(), V_alg_self=valg_self.tolist(), V_alg_ud=valg_ud.tolist(),
                             exact_over_alg=(v / valg_self).tolist(), conv=conv, chi2=c, p=p, chi2_alg_ud=c_alg,
                             label=(label(p) if conv <= 0.01 else "NO VERDICT (convergence)"), res=res)
        P(f"[{f}] exact V {np.round(v,2).tolist()} (data {np.round(gd['V'],1).tolist()})")
        P(f"   exact/algebraic (same Newtonian field) {np.round(v/valg_self,4).tolist()}; ladder max rel {conv:.2e} (line 0.01)")
        P(f"   chi2 exact {c:.1f}/{len(v)} p {p:.2e} (algebraic, UD baryons: {c_alg:.1f}) -> {RES[gname][f]['label']}")
        if MU_ONE:
            ok = abs(c / gd["newton_chi2_ud"] - 1) <= 0.02
            P(f"   MUTATE reproduction: Newton chi2 {c:.1f} vs UD {gd['newton_chi2_ud']} -> {'PASS' if ok else 'FAIL'} (line 2 %)")
            RES[gname][f]["mutate_repro"] = ok

# =================================================================== Malin 1 thickness (reported)
if not MU_ONE:
    RES["Malin1_thickness"] = {}
    for h in (0.5, 2.0):
        gg = A.Grid(0.05, 3.0e4, *RUNGS[-1], p=3); Mc = gg.deposit(rho_malin(h)); row = {}
        for f, a0s in FOOT.items():
            Phi, _, _ = A.solve(gg, Mc, A.a0_kpc(a0s)); v = A.midplane_vc(gg, Phi, RT); c, p = chi2p(VT, ET, v)
            row[f] = dict(V=v.tolist(), chi2=c, p=p)
        RES["Malin1_thickness"][str(h)] = row
        P(f"Malin 1 thickness h = {h} kpc (reported): " + "; ".join(f"{f} V {np.round(row[f]['V'],1).tolist()} chi2 {row[f]['chi2']:.1f}" for f in FOOT))

# =================================================================== SPARC/RAR recheck: exponential discs
if not MU_ONE:
    P("\n=== SPARC/RAR recheck: |log10(g_exact/g_alg)| on exponential discs, R = 1-8 R_d (line 0.057 dex)")
    worst = 0.0; rows = []
    for S0 in (10.0, 100.0, 1000.0):
        for Rd in (1.0, 3.0, 5.0):
            hs = 0.1 * Rd; Rg = 2.0 * Rd; Sg = 10.0
            rho_e = lambda R, z, S0=S0, Rd=Rd, hs=hs, Rg=Rg: (S0 * 1e6 * np.exp(-R / Rd) * np.exp(-0.5 * (z / hs) ** 2) / (np.sqrt(2 * np.pi) * hs)
                                                             + Sg * 1e6 * np.exp(-R / Rg) * np.exp(-0.5 * (z / (0.2 * Rg)) ** 2) / (np.sqrt(2 * np.pi) * 0.2 * Rg))
            gg = A.Grid(0.01 * Rd, 3000.0 * Rd, *RUNGS[0], p=3); Mc = gg.deposit(rho_e)
            PhiN, _, _ = A.solve(gg, Mc, a0c, mu_one=True); Rq = Rd * np.array([1, 2, 3, 4, 6, 8.0])
            gNq = A.midplane_vc(gg, PhiN, Rq) ** 2 / Rq
            for f, a0s in FOOT.items():
                a0 = A.a0_kpc(a0s); Phi, _, _ = A.solve(gg, Mc, a0)
                ge = A.midplane_vc(gg, Phi, Rq) ** 2 / Rq; dl = np.log10(ge / (nu(gNq / a0) * gNq))
                worst = max(worst, float(np.max(np.abs(dl)))); rows.append(dict(S0=S0, Rd=Rd, foot=f, dlog=dl.tolist()))
                P(f"  Sigma0 {S0:6.0f} R_d {Rd:.0f} [{f}] dlog g at 1,2,3,4,6,8 R_d: {np.round(dl,4).tolist()}")
    RES["sparc_recheck"] = dict(rows=rows, worst=worst, line=0.057, ok=worst <= 0.057)
    P(f"SPARC recheck worst |dlog g| = {worst:.4f} dex (line 0.057) -> {'HOLDS' if worst <= 0.057 else 'EXCEEDED: SPARC pass needs an exact-field regrade'}")

P(f"\nwall {time.time()-t0:.0f} s")
name = ("iter1_MUTATE" if MU_ONE else "iter1") + ("_quick" if QUICK else "")
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
