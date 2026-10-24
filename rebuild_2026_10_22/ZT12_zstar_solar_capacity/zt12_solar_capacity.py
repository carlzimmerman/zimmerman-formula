#!/usr/bin/env python3
"""ZT12_zstar_solar_capacity: does Z-star's R1 cap (0 <= D.P <= rho_d) on the Sun's screened hedgehog break Solar-System
screening?  Mechanism M1-M4 (sympy + full-functional bounded minimisation), then planets and the Cassini quadrupole in
brackets B0 / B1 / B2 / v3s.

Criteria: FROZEN_CRITERIA.md (c4b23a2970, committed with the ledger before any number).  kappa = 1/2 FITTED.  Not "theory closed".
Run:   OMP_NUM_THREADS=1 nice -n 15 python3 zt12_solar_capacity.py [--mutate]
"""
import os, sys, json, math, resource
import numpy as np
import sympy as sp
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUTL = []
RES = dict(lane="ZT12_zstar_solar_capacity", criteria="c4b23a2970", mutate=MUT, checks={})
FOOTS = ("canonical", "alt")


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value):
    RES["checks"][key] = dict(ok=bool(ok), value=value); P(f"{key} {'PASS' if ok else 'FAIL'}  {value}")


# ---------------- M1 / M2 (sympy) ----------------
g, p, K, gam, D, r, Gs, M, mu = sp.symbols("g_N p K gamma D r G M mu", positive=True)
# screened static Lagrangian density with K absorbed so that (L) lap Phi = K rho + div p and (P_L) grad Phi + gamma grad D = p
dphi = g + p                                                  # Phi' from the Phi equation (exact, spherical)
local = -dphi ** 2 / (2 * K) + p * dphi / K - p ** 2 / (2 * K)
m1 = sp.simplify(local - (-g ** 2 / (2 * K)))
P(f"M1: on the Phi shell, -(g+p)^2/2K + p(g+p)/K - p^2/2K = -g^2/2K + ({m1}): every p-term cancels; what remains is "
  "-(gamma/2K) D^2 - rho Phi, and int rho Phi_D = (1/K) int Phi_N D (Green) -> E[D] = (1/K) int [(gamma/2) D^2 + Phi_N D] dV")
PhiN = -Gs * M / r
Dfree = sp.solve(sp.diff(gam * D ** 2 / 2 + PhiN * D - mu * D, D), D)[0]
m2 = sp.simplify(sp.diff(Dfree, r) * gam + Gs * M / r ** 2)
P(f"M2: stationarity gamma D + Phi_N = mu -> D = {Dfree}; gamma D' + g_N = {m2}  (gamma = L*^2/2: D = 2GM/(L*^2 r) + const, C6's hedgehog)")
check("KM1", m1 == 0, f"residual {m1}")
check("KM2", m2 == 0, f"residual {m2}")

# ---------------- M3 / M4 (full functional, discretised; units G = M = L* = 1) ----------------
Gn, Mn, Ls = 1.0, 1.0, 1.0
Kn, gn = 4 * math.pi * Gn, Ls ** 2 / 2
edges = np.concatenate([[0.0], np.logspace(-7, 2, 241)])
rm = 0.5 * (edges[1:] + edges[:-1]); rm[0] = edges[1] / 2
dr = np.diff(edges); vol = (edges[1:] ** 3 - edges[:-1] ** 3) / 3        # per 4 pi
N = len(rm)
# p at midpoints = A @ D  (enclosed held 'charge' / r^2, charge in units of K-weighted volume / 4 pi)
A = np.zeros((N, N))
for k in range(N):
    A[k, :k] = vol[:k] / rm[k] ** 2
    A[k, k] = (rm[k] ** 3 - edges[k] ** 3) / 3 / rm[k] ** 2
gN = Gn * Mn / rm ** 2
w = 4 * math.pi * rm ** 2 * dr


def E_full(Dv):
    """the UNSIMPLIFIED static energy -S on the Phi shell, point mass at the origin (rho Phi -> M Phi(0) = -M int Phi' dr),
    minus its D = 0 value: each term is kept separately ((g+p)^2 - g^2 = p(2g+p)), so the p-cancellation is still tested in
    floating point while the D-independent g^2 energy (1e7 x the stiffness term on this grid) is not subtracted numerically."""
    pv = A @ Dv
    dens = pv * (2 * gN + pv) / (2 * Kn) - pv * (gN + pv) / Kn + pv ** 2 / (2 * Kn) + gn * Dv ** 2 / (2 * Kn)
    return float(np.sum(w * dens) - Mn * np.sum(dr * pv))


# quadratic form of E_full (exact for a quadratic): H, b by finite differences of the full expression
E0 = E_full(np.zeros(N))
I = np.eye(N)
e1 = np.array([E_full(I[i]) for i in range(N)]); e2 = np.array([E_full(2 * I[i]) for i in range(N)])
Hd = e2 - 2 * e1 + E0; bv = e1 - E0 - Hd / 2
rng = np.random.default_rng(20261024)
offd = []
for _ in range(200):
    i, j = rng.integers(0, N, 2)
    if i == j:
        continue
    Hij = E_full(I[i] + I[j]) - e1[i] - e1[j] + E0
    offd.append(abs(Hij) / math.sqrt(abs(Hd[i] * Hd[j])))
diag_ok = np.allclose(Hd, gn * w / Kn, rtol=1e-8)
P(f"M1 numeric: Hessian of the UNSIMPLIFIED functional is diagonal = gamma w/K (rel max |off-diag| {max(offd):.1e} over 200 pairs; "
  f"diag matches {diag_ok}): held-dust self-gravity cancels against W, so the cap problem is pointwise")
Dfree_n = -bv / Hd
Dfree_a = 2 * Gn * Mn / Ls ** 2 * (1 / rm - 1 / edges[-1])
inner = rm < 1.0
free_err = float(np.max(np.abs(Dfree_n[inner] / Dfree_a[inner] - 1)))
r_nl = 1e-4                                                        # test cap radius in units of L*
cap = 2 * Gn * Mn / (Ls ** 2 * r_nl)                               # K rho_cap with rho_cap = M/(2 pi L*^2 r_nl)


def grad_full(Dv):
    """gradient of the UNSIMPLIFIED E_full, term by term."""
    pv = A @ Dv
    dp = (2 * gN + 2 * pv) / (2 * Kn) - (gN + 2 * pv) / Kn + pv / Kn
    return A.T @ (w * dp) + w * gn * Dv / Kn - Mn * (A.T @ dr)


SC = np.sqrt(gn * w / Kn)                                          # preconditioner: z = SC * D


def solve_box(hi):
    f = lambda z: E_full(z / SC)
    jac = lambda z: grad_full(z / SC) / SC
    z0 = np.clip(Dfree_n, 0, hi) * SC * 0.5
    bnds = [(0, h * s) for h, s in zip(np.broadcast_to(hi, (N,)), SC)]
    return minimize(f, z0, jac=jac, method="L-BFGS-B", bounds=bnds, options=dict(ftol=1e-20, gtol=1e-16, maxiter=20000)).x / SC


Dmin = solve_box(cap)
pred = np.clip(Dfree_n, 0, cap)
if MUT:                                                            # cap applied to p (non-local) instead of D
    pv_free = A @ np.clip(Dfree_n, 0, None); pcap = (Kn / 3) * (cap / Kn) * r_nl
    pred = np.linalg.solve(A, np.minimum(pv_free, pcap))
scale = np.maximum(np.abs(pred), 1e-300)
dev = float(np.max(np.abs(Dmin - pred) / scale))
ext = rm > 1.5 * r_nl
class _R:
    pass


res_free = _R(); res_free.x = solve_box(np.inf)
ext_dev = float(np.max(np.abs(Dmin[ext] - res_free.x[ext]) / np.abs(res_free.x[ext])))
check("KM3", dev <= 1e-6 and ext_dev <= 1e-6 and free_err <= 1e-2,
      f"bounded minimiser of the full functional vs pointwise clamp: max rel {dev:.1e}; exterior (r > 1.5 r_nl) vs uncapped {ext_dev:.1e}; "
      f"free D vs 2GM/(L*^2)(1/r - 1/r_out) {free_err:.1e} (discretisation)")
# M4 closed forms
pZ = A @ Dmin; pV = A @ res_free.x
from scipy.integrate import quad
Dcl = lambda x: min(2 * Gn * Mn / (Ls ** 2 * x), cap)               # analytic clamped D (exterior constant 0)
m4 = 0.0
for x in np.logspace(-6, -2, 41):
    num = (quad(lambda y: Dcl(y) * y * y, 0, min(x, r_nl), epsabs=0, epsrel=1e-13)[0] +
           (quad(lambda y: Dcl(y) * y * y, r_nl, x, epsabs=0, epsrel=1e-13)[0] if x > r_nl else 0.0)) / x ** 2
    cf = (cap / 3) * x if x <= r_nl else (Gn * Mn / Ls ** 2) * (1 - r_nl ** 2 / (3 * x ** 2))
    m4 = max(m4, abs(num / cf - 1))
mono = bool(np.all(pZ <= pV * (1 + 1e-9)))
check("KM4", m4 <= 1e-6 and mono, f"closed forms vs quadrature of the clamped D (1e-6 <= r/L* <= 0.01): max rel {m4:.1e}; p_Z* <= p_v3s everywhere: {mono}")
RES["mechanism"] = dict(offdiag_max=max(offd), free_err=free_err, clamp_dev=dev, exterior_dev=ext_dev, closed_form_dev=m4, monotone=mono)

# ---------------- physical rows ----------------
GM = 1.32712440018e20; PC = 3.0856775814913673e16; AU = 1.495978707e11; G_SI = 6.67430e-11
MSPC = 1.98847e30 / PC ** 3
C6 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json")))
Z11 = json.load(open(os.path.join(os.path.dirname(HERE), "ZT11_zstar_cherenkov", "zt11_cherenkov_results.json")))
RHO = {f: Z11["MW"][f]["8.122"]["rho_ph_Msun_pc3"] for f in FOOTS}
PLAN = {"Earth": (1.000, 8.7e-15), "Mars": (1.524, 1.4e-15), "Saturn": (9.537, 7.0e-15)}
HEES, PARK = 9.0e-27, 5.2e-27
LST = (24.0, 50.0, 90.0)


def p_cap(rr, Lp, rho):
    """Sun's held-dust anomaly at radius rr (m) with cap rho (kg/m^3); rho = inf -> v3s."""
    h = GM / (Lp * PC) ** 2
    if rho == 0:
        return 0.0, 0.0
    if not math.isfinite(rho):
        return h, 0.0
    rnl = (GM / G_SI) / (2 * math.pi * (Lp * PC) ** 2 * rho)
    return ((4 * math.pi / 3) * G_SI * rho * rr if rr <= rnl else h * (1 - rnl ** 2 / (3 * rr ** 2))), rnl


kc6 = []
for f in FOOTS:
    for Lp in LST:
        for pl, (aau, bd) in PLAN.items():
            key = f"{f}|{int(Lp)}|{pl}"
            if key in C6["R2_planets"]:
                kc6.append(abs(p_cap(aau * AU, Lp, math.inf)[0] / bd - C6["R2_planets"][key]["ratio"]) / C6["R2_planets"][key]["ratio"])
check("KC6", len(kc6) >= 9 and max(kc6) <= 1e-3, f"v3s planetary ratios vs C6 R2 ({len(kc6)} rows): max rel {max(kc6):.1e}")
rnl11 = p_cap(1 * AU, 24.0, RHO["canonical"] * MSPC)[1] / AU
check("KZ11", abs(rnl11 / 970 - 1) <= 0.02, f"r_nl(B1, 24 pc, canonical) = {rnl11:.0f} AU vs ZT11 970 AU")

BR = {"B0": 0.0, "B1": 1.0, "B2": 10.0, "v3s": math.inf}
TAB = {}; worst = {b: 0.0 for b in BR}
P("")
P("bracket | footing | L* | r_nl (AU) | Earth / Mars / Saturn  ratio to bound | Q2 bound / Hees, / Park")
for b, fac in BR.items():
    for f in FOOTS:
        rho = fac * RHO[f] * MSPC if math.isfinite(fac) else math.inf
        for Lp in LST:
            rat = {}
            for pl, (aau, bd) in PLAN.items():
                pa, rnl = p_cap(aau * AU, Lp, rho); rat[pl] = pa / bd
            q6 = max(C6["R1_physical"][f"{f}|{int(Lp)}|E{e}"]["over_Hees_upper"] for e in range(4)) * HEES
            q2 = q6 + (4 * math.pi * G_SI * rho if math.isfinite(rho) else 0.0)
            qr = (q2 / HEES, q2 / PARK)
            rnl_au = p_cap(AU, Lp, rho)[1] / AU if (math.isfinite(rho) and rho > 0) else (0.0 if rho == 0 else float("inf"))
            TAB[f"{b}|{f}|{int(Lp)}"] = dict(r_nl_AU=rnl_au, ratios=rat, Q2=q2, Q2_over_Hees=qr[0], Q2_over_Park=qr[1])
            worst[b] = max(worst[b], max(rat.values()), *qr)
            P(f"{b:4s} | {f:9s} | {int(Lp):2d} | {rnl_au:9.1f} | {rat['Earth']:.2e} / {rat['Mars']:.2e} / {rat['Saturn']:.2e} | {qr[0]:.2e}, {qr[1]:.2e}")
RES["table"] = TAB; RES["worst"] = worst
# reported rows: ambient MW held density and the wake
amb = {}
for f in FOOTS:
    rho = RHO[f] * MSPC
    amb[f] = {pl: dict(x1=(4 * math.pi / 3) * G_SI * rho * aau * AU / bd, x10=10 * (4 * math.pi / 3) * G_SI * rho * aau * AU / bd,
                       wake=(4 * math.pi / 3) * G_SI * rho * (2 * GM / (aau * AU * 230e3 ** 2)) * aau * AU / bd) for pl, (aau, bd) in PLAN.items()}
    P(f"reported [{f}] ambient MW held density {RHO[f]:.4f} Msun/pc^3 as a uniform ball: " +
      ", ".join(f"{pl} {v['x1']:.1e} (x10 {v['x10']:.1e}; wake {v['wake']:.1e})" for pl, v in amb[f].items()) + "  (ratios to bounds)")
RES["ambient"] = amb
fail = worst["B0"] > 1 or worst["B1"] > 1
V = "FAIL" if fail else ("PASS" if worst["B2"] <= 1 else "CONDITIONAL")
RES["verdict"] = V
P(f"worst ratio: B0 {worst['B0']:.2e}, B1 {worst['B1']:.2e}, B2 {worst['B2']:.2e}, v3s {worst['v3s']:.2e}")
P(f"VERDICT Z-T12: {V}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("KR", rss < 1.0, f"{rss:.2f} GB")
allok = all(v["ok"] for v in RES["checks"].values())
P(f"checks: {'ALL PASS' if allok else 'SOME FAIL'}")
open(os.path.join(HERE, f"zt12_solar_capacity{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt12_solar_capacity_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if allok else 1)
