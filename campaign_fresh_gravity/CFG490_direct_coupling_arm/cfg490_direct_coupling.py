#!/usr/bin/env python3
"""CFG490: the G9-violating arm of the fork (LABELLED EXPERIMENT). Does ONE direct baryon-cold coupling deliver the
supply (S x M_b), the 5.8498 r_M edge and the temperature sigma^4 = G M_b a0/4, with <= 1 new constant, and survive the
bounds a direct coupling must face?
Criteria: FROZEN_CRITERIA.md (committed alone first, b385f4306).

EVERY coupling here violates G9 (CFG329) by construction. kappa = 1/2 is FITTED. Both footings scored separately, never
pooled. The cold fluid's MASS is still required and its amount (Omega_c/Omega_b = 5.364) is an input. Where a coupling
needs a field quantum, that is said plainly (a dark-matter particle). Offline theory + numerics; committed record files are
read read-only; no downloads. Not "theory closed".

Run:  python3 cfg490_direct_coupling.py                    (cfg490.out, cfg490_results.json; exit 0 iff K1-K5 pass)
      CFG490_MUTATE=1 python3 cfg490_direct_coupling.py    (cfg490_MUTATE.out, cfg490_results_MUTATE.json; exit 1 iff the
                                                            frozen teeth are detected)
Units inside the equilibria: G = M_b = a0(true) = 1, lengths in r_M = sqrt(G M_b/a0) per footing.
Inputs marked (U) are recalled from the literature and UNVERIFIED; the record's own values are used where it has them.
"""
import os
import sys
import math
import json
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C  # noqa: E402  (record constants; nu_mono = FP1's committed kernel, exec'd read-only)

MUT = os.environ.get("CFG490_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg490{TAG}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


def banner(t):
    P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)


def dex(x):
    return float(math.log10(x)) if x > 0 else float("-inf")


# ============================================================================================================ constants
G, CL, MSUN, KPC = C.G_SI, C.C_SI, C.MSUN, C.KPC
A0 = C.A0
FOOTS = C.FOOTS
S = 5.364                                         # Omega_c/Omega_b (input)
FB = 1.0 / (1.0 + S)
X_EDGE = 1.0 / math.log(1.0 + 1.0 / S)            # 5.8498 r_M
LOGMB = [9.0, 10.5, 11.5]
CELLS = [(f, m) for f in FOOTS for m in LOGMB]
S_CAT, S_CAT_REP = 23.63, 22.6                    # CFG488 K4 (scored) / CFG462 (reported)
RTA_1E9_KPC = 236.0                               # CFG462's CFG118 constant, r_ta ~ M^(1/3)
HOSTS = {"point": 0.0, "H0.3": 0.3}               # scored
HOST_REP = {"H1.0": 1.0}                          # reported
TOL_E, TOL_T, TOL_LAW = 0.05, 0.1, 0.05
EPS_CAP = 10 ** 0.05 - 1.0                        # 0.122: the cold excess a 0.05-dex edge allows (deep regime M ~ r)
GYR = 3.15576e16
EV = 1.602176634e-19
HBAR = 1.054571817e-34
M_U = 1.66053906660e-27
MPL_EV = 2.435e27                                 # reduced Planck mass (record CFG122)
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
GM_EARTH, R_EARTH = 3.986004418e14, 6.371e6       # (U) as CFG122 (g at 710 km = 7.9497)
CM2G = 0.1                                        # 1 cm^2/g = 0.1 m^2/kg

R = {"lane": "CFG490", "mutate": MUT, "kappa": "1/2 FITTED", "g9": "VIOLATED BY CONSTRUCTION (labelled experiment)",
     "constants": {"S": S, "f_b": FB, "x_edge": X_EDGE, "S_cat": S_CAT, "eps_cap": EPS_CAP}, "controls": {},
     "couplings": {}, "bounds_inputs": {}, "reported": {}}

P("=" * 116)
P(f"CFG490 the direct-coupling arm (G9 violated by construction; labelled experiment)   MUTATE={MUT}")
P(f"S = {S}; f_b = {FB:.6f}; x_edge = {X_EDGE:.6f} r_M; catchment supply {S_CAT} M_b (CFG488 K4; {S_CAT_REP} reported)")
P("kappa = 1/2 FITTED; both footings, never pooled; the cold fluid's mass is still required (its amount is an input).")
P("=" * 116)

# ============================================================================================================ kernel
nu = C.nu_mono
_LY = np.linspace(-12.0, 12.0, 240001)
_LX = np.log10(10 ** _LY * nu(10 ** _LY))
assert np.all(np.diff(_LX) > 0), "y nu_mono(y) must be strictly increasing"


def inv(x):
    """mass-shell inverse g_N(g) in a0 units: y with y nu(y) = x (monotone table, log-linear interpolation)."""
    return 10 ** np.interp(np.log10(np.maximum(np.asarray(x, float), 1e-300)), _LX, _LY)


def Mb_enc(r, a):
    r = np.asarray(r, float)
    return np.ones_like(r) if a == 0 else r ** 2 / (r + a) ** 2


def M_ph(r, a):
    m = Mb_enc(r, a)
    return (nu(m / np.asarray(r, float) ** 2) - 1.0) * m


def rho_ph(x, a, h=1e-4):
    """phantom density at x (units M_b / r_M^3), centred log derivative."""
    lo, hi = x * (1 - h), x * (1 + h)
    dM = (float(M_ph(np.array([hi]), a)[0]) - float(M_ph(np.array([lo]), a)[0])) / (hi - lo)
    return dM / (4 * math.pi * x ** 2)


def rM_m(logM, foot):
    return math.sqrt(G * 10 ** logM * MSUN / A0[foot])


def x_ta(logM, foot):
    return RTA_1E9_KPC * KPC * (10 ** (logM - 9.0)) ** (1.0 / 3.0) / rM_m(logM, foot)


def sig_t_kms(logM, foot):
    return (G * 10 ** logM * MSUN * A0[foot] / 4.0) ** 0.25 / 1e3


def first_root(fun, lo, hi, n=4000):
    xs = np.logspace(math.log10(lo), math.log10(hi), n)
    v = np.array([fun(x) for x in xs])
    k = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]
    if len(k) == 0:
        return None
    return brentq(fun, xs[k[0]], xs[k[0] + 1], xtol=1e-14)


# ============================================================================================================ K1 (sympy)
banner("K1  structural identities (sympy)")
K1 = {}
# (a) seesaw: for same-spin exchange fields alpha_bb alpha_cc - alpha_bc^2 = sum_{i<j} (gb_i gc_j - gb_j gc_i)^2 >= 0
gb = sp.symbols("gb1:4", real=True)
gc = sp.symbols("gc1:4", real=True)
abb, acc, abc = sum(x ** 2 for x in gb), sum(x ** 2 for x in gc), sum(x * y for x, y in zip(gb, gc))
lagr = sum((gb[i] * gc[j] - gb[j] * gc[i]) ** 2 for i in range(3) for j in range(i + 1, 3))
K1["a_seesaw"] = sp.expand(abb * acc - abc ** 2 - lagr) == 0
# the mixed-spin loophole: scalar (attractive) + vector (opposite b/c charges, repulsive for like): equal magnitudes
gs_b, gs_c = sp.symbols("g_b g_c", positive=True)
a_bb_mix = gs_b ** 2 - gs_b ** 2
a_cc_mix = gs_c ** 2 - gs_c ** 2
a_bc_mix = gs_b * gs_c + gs_b * gs_c
K1["a_mixed_loophole"] = (a_bb_mix == 0 and a_cc_mix == 0 and sp.simplify(a_bc_mix - 2 * gs_b * gs_c) == 0)
P(f"  (a) same-spin exchange: alpha_bb alpha_cc - alpha_bc^2 = Lagrange sum of squares (N = 3, symbolic): {K1['a_seesaw']}")
P(f"      so |alpha_bc| <= sqrt(alpha_bb alpha_cc) for any number of scalars (or of vectors).  Mixed loophole (scalar + vector,")
P(f"      equal magnitudes, opposite vector charges): alpha_bb = {a_bb_mix}, alpha_cc = {a_cc_mix}, alpha_bc = {a_bc_mix} "
  f"-> cancellation exists: {K1['a_mixed_loophole']} (reported; see B2 note)")
# (b) FRW neutrality and the C2 force law from the perfect-square charge energy
eb, ec, nB, nc, mu_, mc_, k_, Gs, Mc_, Mb_, r_ = sp.symbols("e_b e_c n_B n_c m_u m_c k G M_c M_b r", positive=True)
Ssym = sp.Symbol("S", positive=True)
ec_neutral = sp.solve(sp.Eq(ec * nc, eb * nB), ec)[0]
eps_b, eps_c = eb / mu_, ec_neutral / mc_
ratio = sp.simplify((eps_c / eps_b).subs({nc: Ssym * nB * mu_ / mc_}))       # rho_c = S rho_b
Qenc = eps_b * Mb_ - eps_c.subs({nc: Ssym * nB * mu_ / mc_}) * Mc_
F_cold_out = sp.simplify(k_ * (-eps_c.subs({nc: Ssym * nB * mu_ / mc_})) * Qenc / r_ ** 2)  # k q Q/r^2 outward (like repel)
alpha_cc_sym = k_ * (eps_c.subs({nc: Ssym * nB * mu_ / mc_})) ** 2 / Gs
F_expected = alpha_cc_sym * Gs * (Mc_ - Ssym * Mb_) / r_ ** 2
K1["b_neutrality"] = (sp.simplify(ratio - 1 / Ssym) == 0) and (sp.simplify(F_cold_out - F_expected) == 0)
P(f"  (b) FRW neutrality e_c n_c = e_b n_B -> eps_c/eps_b per unit mass = {ratio}; outward force on cold = "
  f"alpha_cc G (M_c - S M_b)/r^2: {K1['b_neutrality']}")
# (d) BK supply exponent
m_, Lam, al, Mpl, a0s, xs_ = sp.symbols("m Lambda alpha M_Pl a_0 x", positive=True)
kap = al * Mb_ / (8 * sp.pi * Mpl * r_ ** 2)
rho_dm = 2 * m_ ** 2 * Lam * sp.sqrt(kap)
t_ = sp.Symbol('t', positive=True)
Mdm = sp.integrate(4 * sp.pi * t_ ** 2 * rho_dm.subs(r_, t_), (t_, 0, r_))
rM2 = Mb_ / (8 * sp.pi * Mpl ** 2 * a0s)
sup = sp.simplify((Mdm / Mb_).subs(r_, xs_ * sp.sqrt(rM2)).subs(Lam, sp.sqrt(a0s * Mpl / al ** 3)))
expo = sp.simplify(sp.diff(sp.log(sup), Mb_) * Mb_)
sup_expected = m_ ** 2 * xs_ ** 2 / (2 * al * Mpl ** 2) * sp.sqrt(Mb_ / (8 * sp.pi * a0s))
K1["d_BK_exponent"] = (expo == sp.Rational(1, 2)) and (sp.simplify(sup - sup_expected) == 0)
P(f"  (d) BK (CFG122/154 EFT, a0 tie): M_DM(<x r_M)/M_b = {sup}; d ln/d ln M_b = {expo}: {K1['d_BK_exponent']}")
# (e) R0
r0 = float((1 + S) ** 2 * math.log(1 + 1 / S) ** 2)
K1["e_R0"] = abs(r0 - 1.1835) < 5e-4
P(f"  (e) R0 at the exact edge: (1+S)^2 ln^2(1+1/S) = {r0:.5f} ({dex(r0):+.4f} dex): {K1['e_R0']}")
# (f) vector dipole / GR quadrupole
mu_r, D_, a_, w_, c_, aN = sp.symbols("mu Delta a omega c alpha_N", positive=True)
Pdip = sp.Rational(2, 3) * (aN * Gs * D_ ** 2) * mu_r ** 2 * a_ ** 2 * w_ ** 4 / c_ ** 3   # k (Delta q/m)^2 = alpha_N G Delta_B^2
Pgr = sp.Rational(32, 5) * Gs * mu_r ** 2 * a_ ** 4 * w_ ** 6 / c_ ** 5
v_ = sp.Symbol("v", positive=True)
rat = sp.simplify((Pdip / Pgr).subs(w_, v_ / a_))
K1["f_dipole"] = sp.simplify(rat - sp.Rational(5, 48) * aN * D_ ** 2 * c_ ** 2 / v_ ** 2) == 0
P(f"  (f) massless-vector dipole / GR quadrupole = {rat}: {K1['f_dipole']}")


# ============================================================================================================ C2 machinery
def mstar(r, a, alpha_N, S_ratio=S, n_it=90):
    """C2 equilibrium (F-H + neutralising U(1), w = 1): r^2 g_N((M_b + m)/r^2) - M_b + alpha_cc (m - S M_b) = 0."""
    acc = alpha_N / S_ratio ** 2
    mb = Mb_enc(r, a)
    lo, hi = np.zeros_like(r), np.full_like(r, 1e5)
    for _ in range(n_it):
        mid = 0.5 * (lo + hi)
        f = r ** 2 * inv((mb + mid) / r ** 2) - mb + acc * (mid - S_ratio * mb)
        hi = np.where(f > 0, mid, hi)
        lo = np.where(f > 0, lo, mid)
    m = 0.5 * (lo + hi)
    res = r ** 2 * inv((mb + m) / r ** 2) - mb + acc * (m - S_ratio * mb)
    return m, res


def settled_stats(r, ms_full, a, xta, Scat):
    """CAT supply on [r_min, x_ta]: settled = min(m*, S_cat); E = 99.9% radius; returns gate numbers."""
    k = r <= xta
    rr, ms = r[k], np.minimum(ms_full[k], Scat)
    ms = np.maximum.accumulate(ms)                                   # nondecreasing (K4 checks it was already)
    tot = ms[-1]
    tgt = 0.999 * tot
    j = int(np.searchsorted(ms, tgt))
    if j == 0:
        E = float(rr[0])
    else:
        f = (tgt - ms[j - 1]) / max(ms[j] - ms[j - 1], 1e-300)
        E = float(10 ** (math.log10(rr[j - 1]) + f * (math.log10(rr[j]) - math.log10(rr[j - 1]))))
    MsE = float(np.interp(math.log10(E), np.log10(rr), ms))
    MbE = float(Mb_enc(np.array([E]), a)[0])
    w = (rr >= 0.1 * X_EDGE) & (rr <= 0.8 * X_EDGE)
    law = float(np.max(np.abs(ms[w] / M_ph(rr[w], a) - 1)))
    return dict(E=E, E_dex=dex(E / X_EDGE), sup_dex=dex(MsE / S), T_dex=dex((MbE + MsE) ** 2 / E ** 2),
                Tc_dex=dex(MsE ** 2 / E ** 2), law=law, settled_total=float(tot), unsettled_at_xta=float(Scat - tot))


def gates(st, count_ok=True):
    g = dict(sup=abs(st["sup_dex"]) <= TOL_E, edge=abs(st["E_dex"]) <= TOL_E, T=abs(st["T_dex"]) <= TOL_T,
             law=st["law"] <= TOL_LAW, count=count_ok)
    g["all"] = all(g.values())
    return g


RGRID = np.logspace(-3.0, math.log10(1.02 * max(x_ta(m, f) for f, m in CELLS)), 4001)

# ============================================================================================================ K2-K4
banner("K2-K4  controls on the equilibria")
yy = np.logspace(-5, 5, 4001)
rt_err = float(np.max(np.abs(inv(yy * nu(yy)) / yy - 1)))
j462 = json.load(open(os.path.join(CFG, "CFG462_lapse_settling_edge", "cfg462_results.json")))
xe462 = float(j462["flows"]["CAT|F-H"]["canonical|9.0"]["xe"])
m0, res0 = mstar(RGRID, 0.3, 0.0)
k = int(np.searchsorted(m0, S_CAT_REP))
xe_k2 = float(10 ** np.interp(S_CAT_REP, m0[k - 1:k + 1], np.log10(RGRID[k - 1:k + 1])))
K2 = abs(xe_k2 / xe462 - 1) <= 1e-4
P(f"  K2: C2 at alpha_N = 0 (= F-H), Hernquist 0.3, S_cat = 22.6: exhaustion radius {xe_k2:.5f} r_M vs CFG462's committed "
  f"{xe462:.5f} (rel {xe_k2 / xe462 - 1:+.1e}) -> {'PASS' if K2 else 'FAIL'}")
x3 = first_root(lambda x: float(M_ph(np.array([x]), 0.0)[0]) - S, 0.5, 50)
K3 = abs(x3 / X_EDGE - 1) <= 1e-6 and rt_err <= 1e-9
P(f"  K3: C3 point-mass gate edge {x3:.7f} r_M vs x_edge {X_EDGE:.7f} (rel {x3 / X_EDGE - 1:+.1e}); nu_mono inverse round "
  f"trip {rt_err:.1e} -> {'PASS' if K3 else 'FAIL'}")
# (c) the neutral point: m* = S at x_edge for every alpha_N (point mass)
neut = []
for aN in (1e-6, 1e-2, 1.0, 1e2, 1e4, 1e6):
    mm, _ = mstar(np.array([X_EDGE]), 0.0, aN)
    neut.append(abs(float(mm[0]) - S))
K1["c_neutral_point"] = max(neut) <= 1e-6
P(f"  K1(c): C2's neutral point: |m*(x_edge) - S| over alpha_N = 1e-6..1e6 (point mass): max {max(neut):.1e} -> "
  f"{'PASS' if K1['c_neutral_point'] else 'FAIL'}  (both terms vanish there for every alpha_N)")

# ============================================================================================================ C2 scan
banner("C2  neutralising U(1): the declared alpha_N window scan (F-H + Coulomb force on the cold fluid, w = 1)")
ALPHAS = np.logspace(-8, 8, 161)
mono_ok, res_max = True, 0.0
C2scan = {h: {} for h in list(HOSTS) + list(HOST_REP)}
for h, a in list(HOSTS.items()) + list(HOST_REP.items()):
    for aN in ALPHAS:
        ms, res = mstar(RGRID, a, aN)
        scale = np.maximum(1.0, np.abs(ms))
        res_max = max(res_max, float(np.max(np.abs(res) / scale)))
        if not np.all(np.diff(ms) >= -1e-9 * np.max(ms)):
            mono_ok = False
        cells = {}
        for f, lm in CELLS:
            st = settled_stats(RGRID, ms, a, x_ta(lm, f), S_CAT)
            st["gates"] = gates(st)
            cells[f"{f}|{lm}"] = st
        C2scan[h][f"{aN:.3e}"] = cells
K4 = mono_ok and res_max <= 1e-8
P(f"  K4: roots nondecreasing in r for all {len(ALPHAS)} alpha_N x 3 hosts: {mono_ok}; max relative root residual "
  f"{res_max:.1e} -> {'PASS' if K4 else 'FAIL'}")


def scan_summary(h):
    rows = []
    for aN in ALPHAS:
        cs = C2scan[h][f"{aN:.3e}"]
        rows.append((aN, all(c["gates"]["law"] for c in cs.values()), all(c["gates"]["edge"] for c in cs.values()),
                     all(c["gates"]["sup"] for c in cs.values()), all(c["gates"]["T"] for c in cs.values()),
                     all(c["gates"]["all"] for c in cs.values()),
                     max(c["law"] for c in cs.values()), min(abs(c["E_dex"]) for c in cs.values()),
                     max(abs(c["E_dex"]) for c in cs.values()), max(abs(c["sup_dex"]) for c in cs.values())))
    return rows


C2win = {}
for h in list(HOSTS) + list(HOST_REP):
    rows = scan_summary(h)
    law_ok = [r_[0] for r_ in rows if r_[1]]
    edge_ok = [r_[0] for r_ in rows if r_[2]]
    sup_ok = [r_[0] for r_ in rows if r_[3]]
    all_ok = [r_[0] for r_ in rows if r_[5]]
    C2win[h] = dict(law_max=max(law_ok) if law_ok else None, edge_any=edge_ok, sup_min=min(sup_ok) if sup_ok else None,
                    all_pass=all_ok)
    P(f"  [{h:5s}] law within 5% for alpha_N <= {C2win[h]['law_max']:.2e}; edge within 0.05 dex at "
      f"{len(edge_ok)} of {len(ALPHAS)} alpha_N; supply within 0.05 dex for alpha_N >= "
      f"{(C2win[h]['sup_min'] if C2win[h]['sup_min'] else float('nan')):.2e}; ALL gates: {len(all_ok)} alpha_N")
    for aN in (0.0, 1e-12, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e3, 1e4, 1e6):
        if aN == 0.0:
            continue
        key = f"{ALPHAS[np.argmin(np.abs(np.log10(ALPHAS) - math.log10(aN)))]:.3e}"
        c = C2scan[h][key]["canonical|10.5"]
        P(f"      alpha_N = {float(key):8.1e}: E {c['E']:9.3f} r_M ({c['E_dex']:+.3f} dex), supply {c['sup_dex']:+.3f}, "
          f"T {c['T_dex']:+.3f}, law {c['law']:.3g}, settled {c['settled_total']:.3f} M_b, unsettled at r_ta "
          f"{c['unsettled_at_xta']:.3f}  (canonical 10^10.5)")
mcol, _ = mstar(RGRID, 0.0, 100.0)
P(f"  point host, alpha_N = 100: cold inside r = {RGRID[0]:.0e} r_M is {mcol[0]:.3f} M_b (collapse onto the baryons)")
P(f"  POST-RUN LINE (labelled; noticed in the first output): point-host alpha_N with the edge inside 0.05 dex in all cells: "
  f"{[f'{x:.2e}' for x in C2win['point']['edge_any']]} -- a sweep crossing (E goes +0.39 -> -0.17 dex between 1e3 and 1e4) "
  f"with law deviation {max(C2scan['point'][f'{x:.3e}']['canonical|10.5']['law'] for x in C2win['point']['edge_any']):.1f}")
c2_common = set.intersection(*[set(C2win[h]["all_pass"]) for h in HOSTS])
c2_delivers = len(c2_common) > 0
# alpha = 0 (= MUTATE M-a for C2; the uncoupled F-H CAT fill)
m00, _ = mstar(RGRID, 0.0, 0.0)
c2_zero = {f"{h}|{f}|{lm}": settled_stats(RGRID, mstar(RGRID, a, 0.0)[0], a, x_ta(lm, f), S_CAT)
           for h, a in HOSTS.items() for f, lm in CELLS}
P(f"  alpha_N = 0 (uncoupled F-H, CAT): E = {c2_zero['point|canonical|10.5']['E']:.2f} r_M "
  f"({c2_zero['point|canonical|10.5']['E_dex']:+.3f} dex), supply {c2_zero['point|canonical|10.5']['sup_dex']:+.3f} dex, "
  f"T {c2_zero['point|canonical|10.5']['T_dex']:+.3f} dex (the law-target carries the temperature for any far edge)")

# gravity-normalised thresholds
grav = {}
for h, a in list(HOSTS.items()) + list(HOST_REP.items()):
    rr = np.linspace(0.1 * X_EDGE, 0.8 * X_EDGE, 2001)
    mb, mp = Mb_enc(rr, a), M_ph(rr, a)
    acc_law = float(np.min(0.05 * (mb + mp) / np.abs(S * mb - mp)))
    acc_cap = (1 + S) / (EPS_CAP * S)
    grav[h] = dict(alpha_law=S ** 2 * acc_law, alpha_cap=S ** 2 * acc_cap,
                   window_dex=dex(S ** 2 * acc_cap / (S ** 2 * acc_law)))
    P(f"  gravity-normalised [{h}]: law needs alpha_N <= {grav[h]['alpha_law']:.3g}; the cap needs alpha_N >= "
      f"{grav[h]['alpha_cap']:.4g}; window closed by {grav[h]['window_dex']:.2f} dex")
scan_window = {h: (dex(C2win[h]["sup_min"] / C2win[h]["law_max"]) if (C2win[h]["sup_min"] and C2win[h]["law_max"]) else None)
               for h in HOSTS}
P(f"  scan (w = 1): supply-cap threshold / law threshold = "
  + ", ".join(f"{h} {v:.2f} dex" for h, v in scan_window.items() if v is not None) + " (invariant under the F-H weight w)")
ALPHA_REQ_C2 = min(grav[h]["alpha_cap"] for h in HOSTS)
R["couplings"]["C2"] = {"scan_window": C2win, "scan_window_dex": scan_window, "grav": grav, "alpha_N_req": ALPHA_REQ_C2,
                        "zero_coupling": c2_zero,
                        "samples": {h: {k_: C2scan[h][k_]["canonical|10.5"] for k_ in list(C2scan[h])[::10]} for h in C2scan}}

# ============================================================================================================ C3 gate
banner("C3  supply-transfer gate: J = Gamma rho_u Theta(-E.g), composition field div E = 4 pi G (s rho_b - rho_c)")
C3 = {}
for h, a in list(HOSTS.items()) + list(HOST_REP.items()):
    re = first_root(lambda x: float(M_ph(np.array([x]), a)[0]) - S * float(Mb_enc(np.array([x]), a)[0]), 0.3, 100)
    Me = float(M_ph(np.array([re]), a)[0])
    E = brentq(lambda x: float(M_ph(np.array([x]), a)[0]) - 0.999 * Me, 0.3 * re, re, xtol=1e-14)
    MsE, MbE = 0.999 * Me, float(Mb_enc(np.array([E]), a)[0])
    st = dict(r_gate=re, E=E, E_dex=dex(E / X_EDGE), sup_dex=dex(MsE / S), sup_enclosed_dex=dex(MsE / (S * MbE)),
              T_dex=dex((MbE + MsE) ** 2 / E ** 2), Tc_dex=dex(MsE ** 2 / E ** 2), law=0.0,
              Mb_inside=MbE)
    rr = np.linspace(0.1 * X_EDGE, 0.8 * X_EDGE, 2001)
    st["law"] = float(np.max(np.abs(np.where(rr <= re, M_ph(rr, a), Me) / M_ph(rr, a) - 1)))
    st["gates"] = gates(st)
    C3[h] = st
    P(f"  [{h:5s}] gate edge {re:.4f} r_M; E(99.9%) {E:.4f} ({st['E_dex']:+.4f} dex); supply vs S M_b,total "
      f"{st['sup_dex']:+.4f} dex (vs S M_b(<E) {st['sup_enclosed_dex']:+.4f}); T {st['T_dex']:+.4f} dex (cold-only "
      f"{st['Tc_dex']:+.4f}); law {st['law']:.1e}; baryons inside E {MbE:.3f}; gates {'ALL PASS' if st['gates']['all'] else st['gates']}")
c3_geom = all(C3[h]["gates"]["all"] for h in HOSTS)


# ============================================================================================================ bounds inputs
banner("BOUNDS  inputs ((U) = recalled, unverified; record values marked)")
ISO = {"9Be": (9, 9.0121831), "48Ti": (48, 47.94794), "195Pt": (195, 194.96479)}   # 48Ti/195Pt = record (CFG122)
Bmu = {k_: v[0] / v[1] for k_, v in ISO.items()}
d_TiPt = Bmu["48Ti"] - Bmu["195Pt"]
d_BeTi = abs(Bmu["9Be"] - Bmu["48Ti"])
B_H, B_He = 1 / 1.00782503207, 4 / 4.00260325413
Bmu_sun = 0.74 * B_H + 0.25 * B_He + 0.01 * 1.0005                                  # (U) X, Y, Z
Bmu_sat = 0.75 * B_H + 0.25 * B_He                                                 # (U)
Bmu_rock = 0.32 * 55.93494 ** -1 * 56 + 0.30 * 16 / 15.99491 + 0.15 * 28 / 27.97693 + 0.14 * 24 / 23.98504 + 0.09 * 1.0007
EW_ETA, MIC_ETA, MIC_ETA_REP = 3.9e-13, 1e-15, 7e-15
CASSINI, S_EPH = 2.3e-5, 1.27e-5
g_micro = GM_EARTH / (R_EARTH + 710e3) ** 2
g_lab = GM_EARTH / R_EARTH ** 2
P(f"  Delta(B/mu): Ti-Pt {d_TiPt:.4e} (record 9.052e-4), Be-Ti {d_BeTi:.4e}; B/mu Sun {Bmu_sun:.5f}, Saturn {Bmu_sat:.5f}, "
  f"rocky {Bmu_rock:.5f} (U)")
P(f"  Eot-Wash |eta| <= {EW_ETA:g} (U); MICROSCOPE |eta| <= {MIC_ETA:g} (record CFG122; recalled final 2-sigma {MIC_ETA_REP:g}, U); "
  f"Cassini {CASSINI:g} (record); ephemeris ceiling {S_EPH:g} a0 (record)")
j291 = json.load(open(os.path.join(CFG, "CFG291_khronon_binary_pulsar", "cfg291_khronon_binary_pulsar_results.json")))
SYS = j291["numbers"]["systems"]
T_SUN = GM_SUN / CL ** 3


def pm_pbdot(s):
    Pb = s["Pb_d"] * 86400.0
    m = s["m1"] + s["m2"]
    e = s["e"]
    fe = (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / (1 - e ** 2) ** 3.5
    return -(192 * math.pi / 5) * (2 * math.pi / Pb) ** (5 / 3) * T_SUN ** (5 / 3) * s["m1"] * s["m2"] / m ** (1 / 3) * fe


def charge_per_mass(M, kind, Rkm=12.0):
    if kind == "NS":
        beta = GM_SUN * M / (Rkm * 1e3 * CL ** 2)
        return (1 + 0.6 * beta / (1 - beta / 2)) / 1.00866491595
    return B_He                                                                    # He white dwarf


def pulsar_alpha_limit(Rkm=12.0):
    lim = {}
    for nm, s in SYS.items():
        k1, k2 = ("NS", "NS") if s["kind"] == "NS-NS" else ("NS", "WD")
        dB = abs(charge_per_mass(s["m1"], k1, Rkm) - charge_per_mass(s["m2"], k2, Rkm))
        v = (2 * math.pi * GM_SUN * (s["m1"] + s["m2"]) / (s["Pb_d"] * 86400.0)) ** (1 / 3)
        coef = 5 / 48 * dB ** 2 * (CL / v) ** 2
        lim[nm] = dict(Delta_B=dB, v_over_c=v / CL, ratio_per_alpha=coef, hi=s["hi"], alpha_max=s["hi"] / coef)
    return lim


PUL = {Rk: pulsar_alpha_limit(Rk) for Rk in (11.0, 12.0, 13.0)}
pb1738 = pm_pbdot(SYS["J1738+0333"])
K5_items = dict(dTiPt=abs(d_TiPt - 9.052e-4) <= 2e-7,
                etaB=abs(math.sqrt(A0["canonical"] / g_micro) * d_TiPt / 3.106e-9 - 1) <= 2e-3,
                pb1738=abs(pb1738 / -2.746e-14 - 1) <= 1e-3)
K5 = all(K5_items.values())
P(f"  K5: Delta(B/mu)_Ti,Pt {d_TiPt:.4e} vs 9.052e-4; CFG122 Reading-B eta_MIC {math.sqrt(A0['canonical'] / g_micro) * d_TiPt:.4e} "
  f"vs 3.106e-9; J1738 GR Pb-dot {pb1738:.4e} vs -2.746e-14 -> {'PASS' if K5 else 'FAIL'}")
for nm, v in PUL[12.0].items():
    P(f"  pulsar {nm:14s}: Delta_B {v['Delta_B']:.4f}, v/c {v['v_over_c']:.2e}, dipole/GR = {v['ratio_per_alpha']:.3g} alpha_N; "
      f"window +{v['hi']:.3g} -> alpha_N <= {v['alpha_max']:.3g}  (R = 11 / 13 km: {PUL[11.0][nm]['alpha_max']:.3g} / "
      f"{PUL[13.0][nm]['alpha_max']:.3g})")
# Bullet (record table via the CFG4_clusters source: Clowe 2006 Table 2)
BUL = {"main": dict(d_kpc=209.4, Mpl=6.6e12), "sub": dict(d_kpc=194.1, Mpl=5.8e12)}
T_BUL, T_BUL_REP = 0.2 * GYR, 0.1 * GYR


def bullet_alpha_bc_max(t):
    return min(0.5 * (v["d_kpc"] * KPC) ** 3 / (G * v["Mpl"] * MSUN * t ** 2) for v in BUL.values())


SIG_PL_main = BUL["main"]["Mpl"] * MSUN / (math.pi * (100 * KPC) ** 2)            # kg/m^2
P(f"  Bullet (record Table 2): alpha_bc <= {bullet_alpha_bc_max(T_BUL):.3g} at t = 0.2 Gyr ({bullet_alpha_bc_max(T_BUL_REP):.3g} "
  f"at 0.1 Gyr, U); main plasma column {SIG_PL_main / 10:.4f} g/cm^2 -> drag kappa_d <= {0.3 / SIG_PL_main / CM2G:.3g} cm^2/g")
KD_CMB, KD_CMB_REP = 5e-3, 5e-2
CMB_REL = 0.01
R["bounds_inputs"] = dict(dTiPt=d_TiPt, dBeTi=d_BeTi, Bmu_sun=Bmu_sun, Bmu_sat=Bmu_sat, Bmu_rock=Bmu_rock, EW=EW_ETA,
                          MIC=MIC_ETA, MIC_rep=MIC_ETA_REP, cassini=CASSINI, eph=S_EPH, pulsars=PUL,
                          bullet_alpha_bc_max=bullet_alpha_bc_max(T_BUL), bullet_alpha_bc_max_0p1=bullet_alpha_bc_max(T_BUL_REP),
                          drag_bullet_max_cm2g=0.3 / SIG_PL_main / CM2G, kd_cmb=KD_CMB, cmb_rel=CMB_REL)


# ---------------------------------------------------------------------------------------------- U(1) bound evaluator
def u1_limits():
    g_sat = GM_SUN / (9.5826 * AU) ** 2
    lim = dict(B1=EW_ETA / d_BeTi, B2=MIC_ETA / d_TiPt,
               B3_eph=S_EPH * A0["canonical"] / (Bmu_sun * abs(Bmu_rock - Bmu_sat) * g_sat), B3_orbits=1.0,
               B4=min(v["alpha_max"] for v in PUL[12.0].values()),
               B5=S * bullet_alpha_bc_max(T_BUL), B6=CMB_REL * S ** 2, B7=1.0)
    return lim


U1LIM = u1_limits()
P("  U(1) (alpha_N) limits: " + ", ".join(f"{k_} {v:.3g}" for k_, v in U1LIM.items()))


def score_u1(aN, keep_material_phantom=True, inherited=False):
    v = {}
    for k_ in ("B1", "B2", "B4", "B6"):
        v[k_] = "PASS" if aN <= U1LIM[k_] else "FAIL"
    v["B3"] = "PASS" if (aN <= U1LIM["B3_eph"] and aN < 1.0) else "FAIL"          # Cassini: a vector does not couple to light
    v["B5"] = "PASS" if aN <= U1LIM["B5"] else "FAIL"
    v["B7"] = "PASS" if (keep_material_phantom and aN < 1.0) else "FAIL"
    if inherited:
        for k_ in ("B5", "B6"):
            if v[k_] == "PASS":
                v[k_] = "PASS (CONDITIONAL: inherited settling rate / linear-order settling)"
    return v


def label_survives(v):
    if any(str(x).startswith("FAIL") for x in v.values()):
        return "FAIL"
    if any("CONDITIONAL" in str(x) for x in v.values()):
        return "PASS (CONDITIONAL)"
    return "PASS"


# ============================================================================================================ C1 BK
banner("C1  Berezhiani-Khoury phonon coupling -(alpha Lambda/M_Pl) theta rho_b (best case: one constant m^2/alpha centred)")


def natural_L(logM, foot):
    Mb_eV = 10 ** logM * MSUN * CL ** 2 / EV
    a0_eV = A0[foot] * HBAR / CL / EV
    return 0.5 * math.log10(Mb_eV / (8 * math.pi * a0_eV))


def bk_F(x, a):
    if a == 0:
        return x ** 2
    return 2 * quad(lambda t: t * math.sqrt(float(Mb_enc(np.array([t]), a)[0])), 0, x, limit=200)[0]


combos = [(h, a, f, lm) for h, a in HOSTS.items() for f, lm in CELLS]
logsup_unit = {(h, f, lm): math.log10(bk_F(X_EDGE, a) / S) + natural_L(lm, f) for h, a, f, lm in combos}  # + log C
logC = -0.5 * (max(logsup_unit.values()) + min(logsup_unit.values()))
C1 = {}
for h, a, f, lm in combos:
    Lc = natural_L(lm, f) + logC
    sup = logsup_unit[(h, f, lm)] + logC
    xbk = brentq(lambda x: math.log10(bk_F(x, a)) + Lc - math.log10(S), 1e-3, 1e4, xtol=1e-12)
    MbE = float(Mb_enc(np.array([xbk]), a)[0])
    rr = np.linspace(0.1 * X_EDGE, 0.8 * X_EDGE, 41)
    law = max(abs(bk_F(x, a) * 10 ** Lc / float(M_ph(np.array([x]), a)[0]) - 1) for x in rr)
    st = dict(E=xbk, E_dex=dex(xbk / X_EDGE), sup_dex=sup, T_dex=dex((MbE + S) ** 2 / xbk ** 2), law=law)
    st["gates"] = gates(st, count_ok=False)
    C1[f"{h}|{f}|{lm}"] = st
m_alpha1 = MPL_EV * math.sqrt(2 * 10 ** logC)                                        # m at alpha = 1
P(f"  best-case constant m^2/(2 alpha M_Pl^2) = 10^{logC:.3f}  (m = {m_alpha1:.3g} eV at alpha = 1)")
for kk, st in C1.items():
    P(f"    {kk:22s}: supply {st['sup_dex']:+.3f} dex, BK edge {st['E']:.3f} r_M ({st['E_dex']:+.3f}), T(R0 formal) "
      f"{st['T_dex']:+.3f}, cold-mass law dev {st['law']:.3g}")
c1_sup_spread = max(s_["sup_dex"] for s_ in C1.values()) - min(s_["sup_dex"] for s_ in C1.values())
P(f"  supply spread over the 12 combinations {c1_sup_spread:.3f} dex (exponent 1/2 in M_b/a0); constants m, alpha (+ rate) = 3")
eps_B_lab = math.sqrt(A0["canonical"] / g_lab)
eps_B_mic = math.sqrt(A0["canonical"] / g_micro)
eps_B_au = math.sqrt(A0["canonical"] / (GM_SUN / AU ** 2))
eps_A_mic = 0.5 * A0["canonical"] / g_micro
bk_b = {"B1": "FAIL" if eps_B_lab * d_BeTi > EW_ETA else "PASS",
        "B2": "FAIL" if eps_B_mic * d_TiPt > MIC_ETA else "PASS",
        "B3": "FAIL" if (2 * eps_B_au / (1 + eps_B_au) > CASSINI or math.sqrt(A0["canonical"] * GM_SUN / AU ** 2) / A0["canonical"] > S_EPH) else "PASS",
        "B4": "N-C (no committed BK strong-field calculation; not needed for the verdict)",
        "B5": "N-C (BK literature claims consistency; unverified here)",
        "B6": "CONDITIONAL (CFG122 G2 UNDECIDED; its option (a) excluded)",
        "B7": "FAIL (the MOND force is the phonon force on baryons: the EFE triangle, CFG447/PAPER44)"}
P(f"  bounds (Reading B = BK as written; CFG122 showed screening impossible): Eot-Wash eta {eps_B_lab * d_BeTi:.2e} "
  f"({eps_B_lab * d_BeTi / EW_ETA:.3g} x); MICROSCOPE {eps_B_mic * d_TiPt:.2e} ({eps_B_mic * d_TiPt / MIC_ETA:.3g} x); Cassini "
  f"|gamma-1| {2 * eps_B_au / (1 + eps_B_au):.2e} ({2 * eps_B_au / (1 + eps_B_au) / CASSINI:.3g} x); reading A MICROSCOPE "
  f"{eps_A_mic * d_TiPt / MIC_ETA:.3g} x")
R["couplings"]["C1"] = dict(best_case_logC=logC, m_at_alpha1_eV=m_alpha1, cells=C1, supply_spread_dex=c1_sup_spread,
                            count=3, delivers="FAIL", bounds=bk_b, survives=label_survives(bk_b),
                            particle="YES: a superfluid of quanta of mass m (~eV at alpha ~ 1): a dark-matter particle")

# ============================================================================================================ C2 bounds + G-REAL (C3b)
banner("C2 / C3b  the U(1) at its scored strengths; G-REAL for the sign gate")
c2_b = score_u1(ALPHA_REQ_C2)
P(f"  C2 at alpha_N,req = {ALPHA_REQ_C2:.4g} (gravity-normalised cap): " + "; ".join(f"{k_} {v}" for k_, v in c2_b.items()))
P("     limit / required: " + ", ".join(f"{k_} {dex(U1LIM[k_] / ALPHA_REQ_C2):+.1f} dex" for k_ in ("B1", "B2", "B3_eph", "B4", "B5", "B6", "B7")))
c2_law_b = score_u1(min(grav[h]["alpha_law"] for h in HOSTS))
P(f"  C2 at the law's own maximum alpha_N = {min(grav[h]['alpha_law'] for h in HOSTS):.3g}: "
  + "; ".join(f"{k_} {v}" for k_, v in c2_law_b.items()))
R["couplings"]["C2"].update(bounds=c2_b, bounds_at_law_max=c2_law_b, survives=label_survives(c2_b), count=1,
                            delivers="PASS" if c2_delivers else "FAIL",
                            particle="YES: the cold fluid must carry a gauge charge (a complex field with quanta), plus a "
                                     "massless baryon-number gauge boson")
ALPHA_C3B = 0.5 * min(U1LIM[k_] for k_ in ("B1", "B2", "B3_eph", "B4", "B5", "B6"))


def greal_W1(a):
    re = C3[[h for h, aa in list(HOSTS.items()) + list(HOST_REP.items()) if aa == a][0]]["r_gate"]
    W1 = quad(lambda r: (S * float(Mb_enc(np.array([r]), a)[0]) - float(M_ph(np.array([r]), a)[0])) / r ** 2,
              re * 10 ** -0.05, re, limit=200)[0] / S ** 2                      # per unit alpha_N (alpha_cc = alpha_N/S^2)
    sig2 = (float(Mb_enc(np.array([re]), a)[0]) + float(M_ph(np.array([re]), a)[0])) / (2 * re)
    return W1, sig2


GREAL = {}
for h, a in HOSTS.items():
    W1, sig2 = greal_W1(a)
    GREAL[h] = dict(W_per_alpha=W1, sigma2=sig2, contrast_at_scored=ALPHA_C3B * W1 / sig2, alpha_real=sig2 / W1)
    P(f"  G-REAL [{h}]: contrast = {W1 / sig2:.3e} alpha_N; at the scored alpha_N = {ALPHA_C3B:.3g}: "
      f"{ALPHA_C3B * W1 / sig2:.2e}; a readable gate (contrast 1) needs alpha_N >= {sig2 / W1:.4g}")
c3b_b = score_u1(ALPHA_C3B, inherited=True)
P(f"  C3b at alpha_N = {ALPHA_C3B:.3g}: " + "; ".join(f"{k_} {v}" for k_, v in c3b_b.items()))
c3b_real_b = score_u1(min(GREAL[h]["alpha_real"] for h in HOSTS))
P(f"  C3b at the readable-gate strength alpha_N = {min(GREAL[h]['alpha_real'] for h in HOSTS):.4g}: "
  + "; ".join(f"{k_} {v}" for k_, v in c3b_real_b.items()))
c3a_b = {k_: "PASS (no force on baryons)" for k_ in ("B1", "B2", "B3", "B4")}
c3a_b.update(B5="CONDITIONAL (no force; the offset constrains only the inherited settling rate)",
             B6="CONDITIONAL (no force; requires the inherited settling drive to be off at linear order)",
             B7="PASS (material phantom kept)")
greal_ok = all(GREAL[h]["contrast_at_scored"] >= 1 for h in HOSTS)
c3_label_a = ("PASS-R" if c3_geom else "FAIL")
c3_label_b = ("PASS" if (c3_geom and greal_ok) else ("PASS-NA" if c3_geom else "FAIL"))
R["couplings"]["C3a"] = dict(cells=C3, count=1, flag="R", delivers=c3_label_a, bounds=c3a_b, survives="VACUOUS",
                             particle="NO field quantum required (auxiliary non-dynamical field; no Lagrangian)")
R["couplings"]["C3b"] = dict(cells=C3, count=1, alpha_N_scored=ALPHA_C3B, greal=GREAL, delivers=c3_label_b, bounds=c3b_b,
                             bounds_at_readable=c3b_real_b, survives=label_survives(c3b_b),
                             particle="YES (as C2): a charged cold field with quanta + a massless baryon-number gauge boson")

# ============================================================================================================ C4 drag
banner("C4  drag: d_t v_c = ... - rho_b kappa_d |v_rel| (v_c - v_b)")
rho_p = rho_ph(X_EDGE, 0.0) / S                                         # partner baryons at the edge, M_b/r_M^3
C4 = {}
for f in FOOTS:
    Sig_unit = A0[f] / G                                                # M_b/r_M^2 in kg/m^2
    Sig = rho_p * X_EDGE * Sig_unit
    C4[f] = dict(Sigma_kgm2=Sig, kappa_req_cm2g=1.0 / Sig / CM2G)
    P(f"  [{f}] partner-baryon column at the edge {Sig / 10:.3e} g/cm^2 -> locking needs kappa_d >= {1 / Sig / CM2G:.3g} cm^2/g "
      f"(mass-independent); CMB allows <= {KD_CMB:g} ({dex(1 / Sig / CM2G / KD_CMB):+.1f} dex); Bullet allows <= "
      f"{0.3 / SIG_PL_main / CM2G:.3g} ({dex(1 / Sig / CM2G / (0.3 / SIG_PL_main / CM2G)):+.1f} dex)")
KAPPA_REQ = max(v["kappa_req_cm2g"] for v in C4.values())
c4_static = {k_: v for k_, v in c2_zero.items()}
locked = {}
for h, a in HOSTS.items():
    rr = np.linspace(0.1 * X_EDGE, 0.8 * X_EDGE, 2001)
    lawL = float(np.max(np.abs(S * Mb_enc(rr, a) / M_ph(rr, a) - 1)))
    if a == 0:
        EL = 0.0
    else:
        EL = brentq(lambda x: float(Mb_enc(np.array([x]), a)[0]) - 0.999, 1, 1e6)
    locked[h] = dict(law=lawL, E=EL, E_dex=dex(EL / X_EDGE) if EL > 0 else float("-inf"))
    P(f"  locked transient [{h}]: M_c = S M_b(<r): law dev {lawL:.3g}; E(99.9%) {EL:.3g} r_M")
P(f"  static equilibrium (drag vanishes when nothing moves) = the uncoupled F-H CAT fill: E {c4_static['point|canonical|10.5']['E_dex']:+.3f} dex, "
  f"supply {c4_static['point|canonical|10.5']['sup_dex']:+.3f} dex")
c4_b = {k_: "N-C (contact drag: static fifth-force tests do not apply; DM-wind / direct-detection bounds are not on the list)"
        for k_ in ("B1", "B2", "B3", "B4")}
c4_b["B5"] = "FAIL" if KAPPA_REQ > 0.3 / SIG_PL_main / CM2G else "PASS"
c4_b["B6"] = "FAIL" if KAPPA_REQ > KD_CMB else "PASS"
c4_b["B7"] = "PASS (no long-range force; material phantom kept)"
R["couplings"]["C4"] = dict(kappa_req_cm2g=KAPPA_REQ, per_footing=C4, static=c4_static, locked=locked, count=1,
                            delivers="FAIL", bounds=c4_b, survives=label_survives(c4_b),
                            particle="YES: a scattering cross section needs quanta (a dark-matter particle)")

# ============================================================================================================ reported rows
banner("REPORTED (not verdict inputs)")
j488 = json.load(open(os.path.join(CFG, "CFG488_cosettling_supply", "cfg488_results.json")))
cl = j488["clusters"]["per_footing"]
P("  clusters (CFG488, closed box): free placement u = " + ", ".join(f"{f} {cl[f]['u_free']:.3f}" for f in FOOTS)
  + "; in-place u = " + ", ".join(f"{f} {cl[f]['u_inplace']:.3f}" for f in FOOTS) + "; record range "
  + ", ".join(f"{f} [{cl[f]['u_rec_range'][0]:.3f}, {cl[f]['u_rec_range'][1]:.3f}]" for f in FOOTS)
  + ". C3's gate decides neither (it depends on the sign of the cluster outskirts' composition): UNDECIDED.")
P(f"  energy sink (CFG462): {j462['verdict'][:60]}... the sink stays NOT SUPPLIED in every coupling here (inherited).")
# composition-field external-field effect on satellites (C3b), host 6e10 point, canonical
host_M, host_rM = 6e10, rM_m(math.log10(6e10), "canonical") / KPC
efe = {}
for Msat in (1e7, 1e9):
    rMs = rM_m(math.log10(Msat), "canonical") / KPC
    xin = 0.5 * X_EDGE
    Fsat = (S - float(M_ph(np.array([xin]), 0.0)[0])) * Msat / (xin * rMs) ** 2
    for D in (20.0, 50.0):
        xD = D / host_rM
        Fhost = (S - float(M_ph(np.array([xD]), 0.0)[0])) * host_M / D ** 2 if xD < X_EDGE else 0.0
        efe[f"{Msat:.0e}@{D:.0f}kpc"] = Fhost / Fsat
P("  C3b composition-field EFE (host 6e10 Msun, edge " + f"{X_EDGE * host_rM:.1f} kpc): host field / satellite's own at "
  "0.5 r_e,sat = " + ", ".join(f"{k_} {v:.3g}" for k_, v in efe.items()) + "  (>~1: the satellite's gate is set by its host)")
cgm = {}
for fc in (0.05, 0.2, 0.5):
    xc = first_root(lambda x: float(M_ph(np.array([x]), 0.0)[0]) - S * (1 + fc), 0.5, 100)
    cgm[fc] = dex(xc / X_EDGE)
P("  C3b counts ALL baryons (hot CGM too): edge shift for extra counted baryons f_CGM M_b inside the edge: "
  + ", ".join(f"f = {k_}: {v:+.3f} dex" for k_, v in cgm.items()))
P("  B-L instead of B (anomaly-free gauging): hydrogen is neutral, the charge counts neutrons only, so the gate's supply would\n"
  "  track the neutron fraction (Y_p, metals), not M_b. Gauging B alone needs anomaly-cancelling fermions. (stated, not computed)")
P(f"  scalar + vector cancellation (K1a loophole): baryon-baryon force cancelled exactly only if both couple to the same charge;\n"
  f"  a scalar couples to mass, a vector to B, so the residual is alpha x Delta(B m_u/M) = the B2 composition signal again.")
R["reported"] = dict(clusters=cl, efe_composition=efe, cgm_edge_shift_dex=cgm, sink=j462["verdict"])

# ============================================================================================================ physical table
banner("PER-CELL TABLE (point host; physical units)")
for f, lm in CELLS:
    rm = rM_m(lm, f) / KPC
    c2 = C2scan["point"][f"{ALPHAS[np.argmin(np.abs(np.log10(ALPHAS) - math.log10(ALPHA_REQ_C2)))]:.3e}"][f"{f}|{lm}"]
    c1 = C1[f"point|{f}|{lm}"]
    P(f"  {f:9s} 10^{lm:<4}: r_M {rm:6.2f} kpc, r_edge {X_EDGE * rm:7.2f} kpc, sigma_t {sig_t_kms(lm, f):6.1f} km/s, x_ta {x_ta(lm, f):6.1f} | "
      f"C1 E {c1['E_dex']:+.3f} sup {c1['sup_dex']:+.3f} T {c1['T_dex']:+.3f} | C2(alpha_req) E {c2['E_dex']:+.3f} sup "
      f"{c2['sup_dex']:+.3f} T {c2['T_dex']:+.3f} law {c2['law']:.2g} | C3 E {C3['point']['E_dex']:+.4f} sup "
      f"{C3['point']['sup_dex']:+.4f} T {C3['point']['T_dex']:+.4f} | C4(static) E {c2_zero[f'point|{f}|{lm}']['E_dex']:+.3f}")

# ============================================================================================================ MUTATE
banner("MUTATE  (M-a) coupling -> 0 must lose the edge; (M-b) coupling x 100 must violate >= 1 bound")
Ma = {"C1": "edge lost (alpha -> 0 at fixed m, Lambda removes the baryon source of the condensate: rho_DM ~ sqrt(alpha) -> 0, " \
            "no BK edge; the a0 tie then gives a0 -> 0, no MOND force)",
      "C2": all(abs(v["E_dex"]) > TOL_E for v in c2_zero.values()),
      "C3a": all(abs(v["E_dex"]) > TOL_E for v in c2_zero.values()),          # gate off -> the uncoupled CAT fill
      "C3b": all(abs(v["E_dex"]) > TOL_E for v in c2_zero.values()),          # E == 0 -> sign undefined -> no gate
      "C4": all(abs(v["E_dex"]) > TOL_E for v in c2_zero.values())}
MbChk = {"C1": label_survives(bk_b) == "FAIL",                                      # under the a0 tie the force is alpha-free
       "C2": label_survives(score_u1(100 * ALPHA_REQ_C2)) == "FAIL",
       "C3a": "VACUOUS (no force strength to scale; s_gate x 100 moves the edge to the CAT fill but violates no bound)",
       "C3b": label_survives(score_u1(100 * ALPHA_C3B)) == "FAIL",
       "C4": (100 * KAPPA_REQ > KD_CMB)}
if MUT:
    P("  (M-a) " + "; ".join(f"{k_}: {v}" for k_, v in Ma.items()))
    P("  (M-b) " + "; ".join(f"{k_}: {v}" for k_, v in MbChk.items()))
    P(f"        C3b x 100 = {100 * ALPHA_C3B:.3g}: " + "; ".join(f"{k_} {v}" for k_, v in score_u1(100 * ALPHA_C3B).items()
                                                            if v.startswith("FAIL")))
    P(f"        C2 x 100 = {100 * ALPHA_REQ_C2:.4g}: " + "; ".join(f"{k_} {v}" for k_, v in score_u1(100 * ALPHA_REQ_C2).items()))
    P(f"        C4 x 100 = {100 * KAPPA_REQ:.4g} cm^2/g vs CMB {KD_CMB:g}, Bullet {0.3 / SIG_PL_main / CM2G:.3g}")
else:
    P("  (the mutated checks print only with CFG490_MUTATE=1)")
teeth = all(v is True or isinstance(v, str) for v in Ma.values()) and all(MbChk[k_] is True for k_ in ("C1", "C2", "C3b", "C4"))
R["mutate_checks"] = dict(Ma=Ma, Mb=MbChk, teeth=teeth)

# ============================================================================================================ verdict
banner("VERDICT")
counts = {"C1": 3, "C2": 1, "C3a": 1, "C3b": 1, "C4": 1}
dl = {"C1": "FAIL", "C2": "PASS" if c2_delivers else "FAIL", "C3a": c3_label_a, "C3b": c3_label_b, "C4": "FAIL"}
sv = {"C1": label_survives(bk_b), "C2": label_survives(c2_b), "C3a": "VACUOUS", "C3b": label_survives(c3b_b),
      "C4": label_survives(c4_b)}
for k_ in dl:
    P(f"  {k_:4s} DELIVERS {dl[k_]:8s} SURVIVES {sv[k_]:20s} constants {counts[k_]}")
clean = [k_ for k_, v in dl.items() if v == "PASS"]
lane = ("arm (a) DELIVERS: " + ", ".join(clean)) if clean else \
    "arm (a) does NOT deliver cleanly: no Lagrangian coupling delivers; only the rule-level gate does, as the edge definition " \
    "(C3a, PASS-R) or as a sign gate on a gauged charge too weak to be read (C3b, PASS-NA)" if c3_geom else \
    "arm (a) does NOT deliver: no coupling passes the frozen gates on the scored hosts"
P("  LANE: " + lane)
R["verdict"] = dict(delivers=dl, survives=sv, counts=counts, lane=lane, c3_geometry_pass=c3_geom)

ctrl = dict(K1=all(K1.values()), K2=K2, K3=K3, K4=K4, K5=K5)
R["controls"] = dict(K1=K1, K2=dict(pass_=K2, xe=xe_k2, xe462=xe462), K3=dict(pass_=K3, x3=x3, inv=rt_err),
                     K4=dict(pass_=K4, monotone=mono_ok, residual=res_max), K5=dict(pass_=K5, **K5_items), all=ctrl)
P("  controls: " + ", ".join(f"{k_} {'PASS' if v else 'FAIL'}" for k_, v in ctrl.items()))
if MUT:
    rc = 1 if teeth else 0
    P(f"  MUTATE: teeth {'DETECTED' if teeth else 'NOT detected'} -> exit {rc}")
else:
    rc = 0 if all(ctrl.values()) else 1
    P(f"  exit {rc}")
R["exit_code"] = rc
json.dump(C.jclean(R), open(os.path.join(HERE, f"cfg490_results{TAG}.json"), "w"), indent=1)
OUT.close()
sys.exit(rc)
