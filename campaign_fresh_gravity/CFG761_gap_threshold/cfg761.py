"""CFG761: where exactly does P radiation switch on? Exact Green-function threshold x_e = omega/omega_g (hardening CFG760 G2)

Criteria: FROZEN_CRITERIA.md (committed alone, 364fc9c73). Equations and code copied from CFG760. CFG691/696 units (s = r/l_gamma, t in l_gamma/c_P).
Linear perturbation about the law's static profile v0:  dv_tt = dv'' - 2 dv/s^2 - (2|v0|/s) dv + J.
The mass term 2|v0|/s is the curvature of the cubic W (the deep law itself). MUTATE drops it.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg761.py      (CFG761_MUTATE=1: no vacuum curvature; exit 1 iff both teeth bite)
"""
import os, sys, json, math

import numpy as np
from scipy.integrate import solve_bvp, solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG761_MUTATE", "0") == "1"
CURV = 0.0 if MUT else 1.0                                             # weight of the vacuum-curvature mass term
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg761{TAG}.out"), "w")
RES = {"lane": "CFG761", "criteria": "364fc9c73", "mutate": MUT, "checks": {}, "numbers": {}}
G, MSUN, PC, C = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
GYR = 3.15576e16
LSTAR = 5.754 * PC


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())

# ============================================================================ K1: static profile (CFG691/696 BVP)
def f(t, y):
    s = np.exp(t)
    return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])


tt = np.linspace(math.log(1e-4), math.log(1e4), 4001)
ss = np.exp(tt)
SOL = solve_bvp(f, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt,
                np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)
c691 = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["profile"]["S_table"]
dS = max(abs(float(k) * float(SOL.sol(math.log(float(k)))[0]) - v) for k, v in c691.items())
check("K1 static profile reproduces CFG691's S table to <= 1e-6", SOL.status == 0 and dS <= 1e-6, f"max |dS| = {dS:.1e}")


def v0(s):
    """law's static profile v0 = s q0 (scalar)"""
    if s < 1e-4:
        return 0.5 * s
    if s > 1e4:
        return 1.0 - 1.0 / s
    return s * float(SOL.sol(math.log(s))[0])


def k2_full(s, w):
    return w * w - 2.0 / s ** 2 - CURV * 2.0 * abs(v0(s)) / s


def k2_ref(s, w):
    return w * w - 2.0 / s ** 2


def omega_gap(s0):
    return math.sqrt(2.0 * abs(v0(s0)) / s0 + 2.0 / s0 ** 2)


# ============================================================================ frequency-domain Green's function
def power(s0, w, k2fun):
    """radiated power (common constant dropped) of a unit point source at s0, frequency w; returns (P, flux-invariant spread)."""
    # turning point beyond which k2 > 0 everywhere
    st = s0
    while k2fun(st, w) <= 0 or k2fun(2 * st, w) <= 0:
        st *= 2
    Sout = 50.0 * max(s0, st, 2.0 / w ** 2)
    # u1: regular at 0 (u ~ s^2), real
    def rhs1(s, y):
        return [y[1], -k2fun(s, w) * y[0]]
    s_in = 1e-3
    r1 = solve_ivp(rhs1, (s_in, s0), [s_in ** 2, 2 * s_in], rtol=1e-11, atol=1e-30, method="DOP853")
    u1, du1 = r1.y[0, -1], r1.y[1, -1]
    # u2: outgoing WKB at Sout, integrated inward (complex as two real pairs)
    k = math.sqrt(k2fun(Sout, w))
    h = 1e-3 * Sout
    dk = (math.sqrt(k2fun(Sout + h, w)) - math.sqrt(k2fun(Sout - h, w))) / (2 * h)
    u = 1 / math.sqrt(k) + 0j
    du = (1j * k - dk / (2 * k)) * u

    def rhs2(s, y):
        kk = k2fun(s, w)
        return [y[2], y[3], -kk * y[0], -kk * y[1]]
    s_turn = s0
    if k2fun(s0, w) <= 0:
        hi = s0
        while k2fun(hi, w) <= 0:
            hi *= 1.5
        s_turn = brentq(lambda x: k2fun(x, w), hi / 1.5, hi, xtol=1e-12 * hi)
    pts = np.geomspace(max(s_turn * 1.05, s0), Sout, 60)[::-1]
    r2 = solve_ivp(rhs2, (Sout, s0), [u.real, u.imag, du.real, du.imag], rtol=1e-11, atol=1e-40, method="DOP853",
                   dense_output=True)
    inv = []
    for sp in pts:
        y = r2.sol(sp)
        uu, dd = y[0] + 1j * y[1], y[2] + 1j * y[3]
        inv.append((np.conj(uu) * dd).imag)
    inv = np.array(inv)
    y = r2.y[:, -1]
    u2, du2 = y[0] + 1j * y[1], y[2] + 1j * y[3]
    W = u1 * du2 - du1 * u2
    flux = inv[0]
    Pw = 0.5 * w * abs(u1) ** 2 * flux / abs(W) ** 2
    return Pw, float(np.max(np.abs(inv - inv[0])) / abs(inv[0]))


def kappa_int(s0, w, k2fun):
    """2 * integral_{s0}^{inf} sqrt(max(0, -k2)) ds over the barrier"""
    if k2fun(s0, w) >= 0 and k2fun(2 * s0, w) >= 0:
        return 0.0
    st = s0
    while k2fun(st, w) < 0:
        st *= 1.5
    lo = st / 1.5
    try:
        st = brentq(lambda x: k2fun(x, w), lo, st, xtol=1e-12 * st)
    except ValueError:
        pass
    g = lambda lx: math.sqrt(max(0.0, -k2fun(math.exp(lx), w))) * math.exp(lx)
    val, _ = quad(g, math.log(s0), math.log(st), limit=400, epsabs=0, epsrel=1e-9)
    return 2 * val


# ============================================================================ K1: reproduce CFG760 G1
c760 = json.load(open(os.path.join(LANES, "CFG760_p_wave_gap", "cfg760_results.json")))["numbers"]["G1"]
k1 = True
for key in ("20_0.5", "50_0.5", "50_0.7", "200_0.7"):
    s0, r = float(key.split("_")[0]), float(key.split("_")[1])
    w = r * omega_gap(s0)
    Sn = power(s0, w, k2_full)[0] / power(s0, w, k2_ref)[0]
    ref = c760[key]["S"]
    k1 &= abs(Sn / ref - 1) <= 1e-6 if not MUT else True
    P_(f"    K1 ({s0:g}, {r:g}): S = {Sn:.6e} (CFG760 {ref:.6e})")
check("K1 reproduces CFG760 G1 S values to <= 1e-6 relative", k1, "")

# ============================================================================ threshold scan
P_("\nSCAN  S(x, s0), x = w/w_g on 0.30..1.50; x_e = smallest x with S >= 1/e")
XS = np.round(np.arange(0.30, 1.5001, 0.01), 2)
SCAN, XE, inv_worst = {}, {}, 0.0
for s0 in (20.0, 50.0, 200.0, 1000.0, 5000.0):
    wg = omega_gap(s0)
    row = []
    for x in XS:
        Pf, sf = power(s0, x * wg, k2_full)
        Pr, sr = power(s0, x * wg, k2_ref)
        inv_worst = max(inv_worst, sf, sr)
        row.append(Pf / Pr)
    row = np.array(row)
    hit = np.where(row >= math.exp(-1))[0]
    XE[s0] = float(XS[hit[0]]) if hit.size else None
    SCAN[f"{s0:g}"] = dict(x=XS.tolist(), S=row.tolist(), x_e=XE[s0])
    P_(f"    s0 = {s0:6g}: x_e = {XE[s0]};  S at x = 0.5/0.7/0.9/1.0/1.2: "
       + " / ".join(f"{row[np.argmin(abs(XS - v))]:.2e}" for v in (0.5, 0.7, 0.9, 1.0, 1.2)))
RES["numbers"]["SCAN"] = SCAN
check("K2 flux invariant beyond the outer turning point constant to <= 1e-6 (all scan solves)", inv_worst <= 1e-6, f"worst {inv_worst:.1e}")
xe = [XE[s] for s in sorted(XE)]
t1 = all(v is not None for v in xe) and all(b >= a for a, b in zip(xe, xe[1:])) and xe[-1] > xe[0]
check("T1 x_e non-decreasing in s0 and x_e(5000) > x_e(20)", t1, f"x_e = {xe}")

# ============================================================================ T2: re-scored pincer
xmin = min(v for v in xe if v is not None)
P_(f"\nT2  c_P,max = V/(x_e,min w_g s0 ), x_e,min = {xmin}; V = 2 V_f; L* = 5.754 pc; c_P,min = r/13.8 Gyr")
T2 = {}
closed = True
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    rows = []
    for m, y in [(m, y) for m in (1e9, 1e10, 1e11, 1e12) for y in (0.1, 0.01)]:
        M = m * MSUN
        rM = math.sqrt(G * M / a0); r = rM / math.sqrt(y); ell = LSTAR ** 2 / (2 * rM); s0 = r / ell
        V = 2 * (G * M * a0) ** 0.25
        cmax = V / (xmin * omega_gap(s0) * s0)
        cmin = r / (13.8 * GYR)
        op = cmax >= cmin
        closed &= not op
        rows.append(dict(Mb=m, y=y, s0=s0, cP_max_ms=cmax, cP_min_ms=cmin, margin=cmin / cmax, open=bool(op)))
        P_(f"    {fo:9s} M_b {m:.0e} y {y:<5g} s0 {s0:.3e}: c_P,max {cmax:.3e} m/s  c_P,min {cmin:.3e} m/s  margin {cmin / cmax:.2f}  "
           f"{'OPEN' if op else 'closed'}")
    T2[fo] = rows
RES["numbers"]["T2"] = T2
if MUT:
    bites = dict(T1=not t1, T2=not closed)
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    verdict = ("CLOSED" if closed else "OPEN") if t1 else "NOT ESTABLISHED"
    RES["verdict"] = dict(T1="PASS" if t1 else "FAIL", T2="CLOSED" if closed else "OPEN", overall=verdict)
    P_(f"\nVERDICT: T1 {RES['verdict']['T1']}; T2 {RES['verdict']['T2']}; overall {verdict}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg761_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
