"""CFG760: can P-wave radiation export the infall energy of cold energy? (the vacuum gap test)

Criteria: FROZEN_CRITERIA.md (committed alone, 6f2ee620b). CFG691/696 units (s = r/l_gamma, t in l_gamma/c_P).
Linear perturbation about the law's static profile v0:  dv_tt = dv'' - 2 dv/s^2 - (2|v0|/s) dv + J.
The mass term 2|v0|/s is the curvature of the cubic W (the deep law itself). MUTATE drops it.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg760.py      (CFG760_MUTATE=1: no vacuum curvature; exit 1 iff both teeth bite)
"""
import os, sys, json, math

import numpy as np
from scipy.integrate import solve_bvp, solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG760_MUTATE", "0") == "1"
CURV = 0.0 if MUT else 1.0                                             # weight of the vacuum-curvature mass term
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg760{TAG}.out"), "w")
RES = {"lane": "CFG760", "criteria": "6f2ee620b", "mutate": MUT, "checks": {}, "numbers": {}}
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
    pts = np.unique(np.concatenate([np.geomspace(s0, Sout, 60)]))[::-1]
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


# ============================================================================ G1 + K2 + K3
P_("\nG1  suppression S = P_full / P_ref of a point source below the vacuum gap, vs the WKB exponent")
G1, k2_ok, k3_ok = {}, True, True
g1_ok = True
for s0 in (20.0, 50.0, 200.0):
    wg = omega_gap(s0)
    for r in (0.5, 0.7, 2.0):
        w = r * wg
        Pf, sf = power(s0, w, k2_full)
        Pr, sr = power(s0, w, k2_ref)
        Sn = Pf / Pr
        dE = kappa_int(s0, w, k2_full) - kappa_int(s0, w, k2_ref)
        k2_ok &= (sf <= 1e-6 and sr <= 1e-6)
        row = dict(s0=s0, w_over_wg=r, w=w, S=Sn, lnS=math.log(Sn), dE_WKB=dE, ratio=(math.log(Sn) / -dE if dE > 0 else None),
                   inv_spread_full=sf, inv_spread_ref=sr)
        if r == 2.0:
            k3_ok &= 0.3 <= Sn <= 3
        elif dE >= 5:
            ok = 0.8 <= math.log(Sn) / -dE <= 1.25 and Sn <= 1e-2
            row["ok"] = ok
            g1_ok &= ok
        G1[f"{s0:g}_{r:g}"] = row
        P_(f"    s0 = {s0:5g}, w/w_g = {r:3g} (w = {w:.4f}): S = {Sn:.3e}  ln S = {math.log(Sn):+8.3f};  WKB dE = {dE:7.3f}"
           + (f";  lnS/(-dE) = {math.log(Sn) / -dE:.3f}" if dE > 0 else "") + f";  invariant spread {sf:.1e}/{sr:.1e}")
if MUT:
    g1_ok = g1_ok and any(v.get("ok") is not None for v in G1.values())     # with no barrier there are no dE >= 5 cases
RES["numbers"]["G1"] = G1
check("K2 flux invariant Im(u2* u2') constant to <= 1e-6 (full and reference)", k2_ok, "")
check("K3 above the gap (w = 2 w_g) S in [0.3, 3]", k3_ok, "; ".join(f"s0 {v['s0']:g}: {v['S']:.3f}" for v in G1.values() if v["w_over_wg"] == 2.0))
g1 = check("G1 below the gap: ln S/(-dE_WKB) in [0.8, 1.25] and S <= 1e-2 for every case with dE >= 5", g1_ok,
           "; ".join(f"{k}: {v['ratio']:.3f}" for k, v in G1.items() if v.get("ok") is not None) or "no case with dE >= 5")

# ============================================================================ K4: time domain, nonlinear CFG696 equation
P_("\nK4  time domain: CFG696's nonlinear equation + small oscillating source at s0 = 20 (difference of runs with and without the source)")
DS, DT, SB = 0.02, 0.01, 400.0
sg = np.arange(0, SB + DS / 2, DS)
si = sg.copy(); si[0] = 1.0
v_st = np.array([v0(x) for x in sg])
S0K, WID, EPS = 20.0, 0.5, 1e-4
prof = np.exp(-0.5 * ((sg - S0K) / WID) ** 2)
iobs = int(round(0.9 * SB / DS))


def accel(v, lin_ref=False):
    a = np.zeros_like(v)
    if lin_ref:
        a[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / DS ** 2 - 2 * v[1:-1] / si[1:-1] ** 2
    else:
        a[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / DS ** 2 - 2 * v[1:-1] / si[1:-1] ** 2 \
                  - (CURV * v[1:-1] * np.abs(v[1:-1]) + (1 - CURV) * 0.0) / si[1:-1] + 1 / si[1:-1]
    return a


def td_flux(w, mode):
    """mode 'full': nonlinear eq about v_st, difference of driven - undriven; 'ref': linear eq without curvature."""
    T_END = SB + 12 * 2 * math.pi / w
    n = int(round(T_END / DT))
    t_avg0 = T_END - 6 * 2 * math.pi / w
    if mode == "full":
        A = v_st.copy(); Ao = v_st.copy(); B = v_st.copy(); Bo = v_st.copy()
    else:
        A = np.zeros_like(sg); Ao = A.copy(); B = None
    acc, cnt = 0.0, 0
    for i in range(n):
        t = i * DT
        drive = EPS * math.cos(w * t) * prof
        if mode == "full":
            An = 2 * A - Ao + DT ** 2 * (accel(A) + drive)
            Bn = 2 * B - Bo + DT ** 2 * accel(B)
            for X, Xo, Xn in ((A, Ao, An), (B, Bo, Bn)):
                Xn[0] = 0.0
                Xn[-1] = X[-1] + DT * (-(X[-1] - X[-2]) / DS + 1 / SB ** 2)
            Ao, A, Bo, B = A, An, B, Bn
            d, do = A - B, Ao - Bo
        else:
            An = 2 * A - Ao + DT ** 2 * (accel(A, lin_ref=True) + drive)
            An[0] = 0.0
            An[-1] = A[-1] - DT * (A[-1] - A[-2]) / DS
            Ao, A = A, An
            d, do = A, Ao
        if t >= t_avg0:
            dvt = (d[iobs] - do[iobs]) / DT
            dvs = (d[iobs + 1] - d[iobs - 1]) / (2 * DS)
            acc += -dvs * dvt; cnt += 1
    return acc / max(cnt, 1)


wg20 = omega_gap(S0K)
F_hi = td_flux(2 * wg20, "full")
F_lo = td_flux(0.5 * wg20, "full")
F_ref = td_flux(2 * wg20, "ref")
S_td = F_hi / F_ref
S_fd = G1["20_2"]["S"]
ratio_lohi = abs(F_lo) / abs(F_hi)
RES["numbers"]["K4"] = dict(F_above=F_hi, F_below=F_lo, F_ref_above=F_ref, S_td=S_td, S_fd=S_fd, below_over_above=ratio_lohi)
P_(f"    flux above gap (w = 2 w_g) {F_hi:.3e}; below (0.5 w_g) {F_lo:.3e}; reference above {F_ref:.3e}")
P_(f"    below/above = {ratio_lohi:.2e};  S time-domain {S_td:.3f} vs frequency-domain {S_fd:.3f}")
k4 = check("K4 nonlinear time domain: below/above-gap flux <= 1e-3 and above-gap S within 30% of the frequency domain",
           ratio_lohi <= 1e-3 and abs(S_td / S_fd - 1) <= 0.30, f"{ratio_lohi:.2e}; S_td/S_fd = {S_td / S_fd:.3f}")

# ============================================================================ G2: the physical pincer
P_("\nG2  physical pincer at L* = 5.754 pc: export needs dE(w) <= 1 (w = (V/c_P)/s0, V = 2 V_f); P relaxation needs r/c_P <= 13.8 Gyr")


def dE_at(s0, w):
    return kappa_int(s0, w, k2_full) - kappa_int(s0, w, k2_ref)


def cp_max(s0, V):
    """largest c_P with dE <= 1 (export allowed)"""
    wg = omega_gap(s0)
    if dE_at(s0, 1e-6 * wg) <= 1:
        return math.inf
    lo, hi = math.log(1e-6 * wg), math.log(20 * wg)
    while dE_at(s0, math.exp(hi)) > 1:
        hi += 1
    lw = brentq(lambda x: dE_at(s0, math.exp(x)) - 1, lo, hi, xtol=1e-10)
    return V / (math.exp(lw) * s0)


def case(Mb_sun, y, a0, Lst):
    M = Mb_sun * MSUN
    rM = math.sqrt(G * M / a0)
    r = rM / math.sqrt(y)
    ell = Lst ** 2 / (2 * rM)
    s0 = r / ell
    Vf = (G * M * a0) ** 0.25
    V = 2 * Vf
    cmax = cp_max(s0, V)
    cmin = r / (13.8 * GYR)
    cmin744 = 2.56 * s0 ** 1.5 * ell / (4.6 * GYR)
    return dict(Mb=Mb_sun, y=y, r_kpc=r / PC / 1e3, ell_pc=ell / PC, s0=s0, Vf_kms=Vf / 1e3, cP_max_ms=cmax, cP_min_ms=cmin,
                cP_min_CFG744_ms=cmin744, open=bool(cmax >= cmin))


CASES = [(m, y) for m in (1e9, 1e10, 1e11, 1e12) for y in (0.1, 0.01)]
G2 = {}
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    rows = [case(m, y, a0, LSTAR) for m, y in CASES]
    G2[fo] = rows
    for x in rows:
        P_(f"    {fo:9s} M_b {x['Mb']:.0e} y {x['y']:<5g} r {x['r_kpc']:7.2f} kpc  l_gamma {x['ell_pc']:.3e} pc  s0 {x['s0']:.3e}  "
           f"c_P,max {x['cP_max_ms']:.3e} m/s  c_P,min {x['cP_min_ms']:.3e} m/s (CFG744 law {x['cP_min_CFG744_ms']:.3e})  "
           f"{'OPEN' if x['open'] else 'closed'}  margin c_min/c_max = {x['cP_min_ms'] / x['cP_max_ms']:.2e}")
RES["numbers"]["G2"] = G2
g2_closed = all(not x["open"] for fo in C4.FOOTS for x in G2[fo])
P_(f"  G2 verdict: {'CLOSED' if g2_closed else 'OPEN'}")
RES["numbers"]["G2_verdict"] = "CLOSED" if g2_closed else "OPEN"

# ============================================================================ G3: the larger-L* hatch vs SPARC (CFG691 statistic, copied)
P_("\nG3  smallest L* opening each case; SPARC rms at L*_all (CFG691 statistic, copied)")
from CFG691_copy import sparc_fit  # noqa: E402  (local copy of CFG691's fit; see CFG691_copy.py)
k5 = True
c691g = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["G_GAL"]
for fo in C4.FOOTS:
    for Lpc, key in ((5.754, None), (1000.0, "1e+03")):
        rr, uu = sparc_fit(C4.A0[fo], Lpc * PC, SOL)
        ref = c691g[fo]["rms_at_Lmin"] if key is None else c691g[fo]["ladder"][key]["rms"]
        k5 &= abs(rr - ref) <= 1e-4
        P_(f"    K5 {fo:9s} L* {Lpc:g} pc: rms {rr:.5f} (CFG691 {ref:.5f})")
check("K5 copied SPARC statistic reproduces CFG691 at L* = 5.754 and 1000 pc to <= 1e-4", k5, "")
LGRID = 10 ** np.arange(math.log10(5.754), 5.0001, 0.02) * PC
G3 = {}
hatch = True
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    Lopen = {}
    for m, y in CASES:
        # bisection on the grid index (openness checked monotone: the found point opens and its predecessor does not)
        if not case(m, y, a0, LGRID[-1])["open"]:
            Lopen[f"{m:.0e}_{y:g}"] = None
            continue
        lo, hi = 0, len(LGRID) - 1
        if case(m, y, a0, LGRID[0])["open"]:
            hi = 0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if case(m, y, a0, LGRID[mid])["open"]:
                hi = mid
            else:
                lo = mid
        Lopen[f"{m:.0e}_{y:g}"] = LGRID[hi] / PC
    if any(v is None for v in Lopen.values()):
        G3[fo] = dict(L_open=Lopen, L_all=None, rms=None, open=False)
        hatch = False
        P_(f"    {fo:9s}: some case never opens on the grid (to 1e5 pc): {Lopen}")
        continue
    Lall = max(Lopen.values())
    rr, uu = sparc_fit(a0, Lall * PC, SOL)
    ok = rr <= 0.110
    hatch &= ok
    G3[fo] = dict(L_open=Lopen, L_all_pc=Lall, rms=rr, U=uu, open=ok)
    P_(f"    {fo:9s}: L*_open per case {', '.join(f'{k} {v:.3g}' for k, v in Lopen.items())} pc;  L*_all {Lall:.4g} pc: "
       f"SPARC rms {rr:.4f} @ U {uu:.2f} -> {'OPEN' if ok else 'closed'}")
RES["numbers"]["G3"] = G3
P_(f"  G3 hatch: {'OPEN' if hatch else 'CLOSED'}")

# ============================================================================ verdict
if MUT:
    bites = dict(G1=not g1, G2=not g2_closed)
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    RES["verdict"] = dict(G1="PASS" if g1 else "FAIL", G2="CLOSED" if g2_closed else "OPEN", G3="OPEN" if hatch else "CLOSED")
    P_(f"\nVERDICT: G1 {RES['verdict']['G1']}; G2 {RES['verdict']['G2']}; G3 hatch {RES['verdict']['G3']}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg760_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
