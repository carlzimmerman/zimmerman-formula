"""E6_native_fret -- a framework-native rule for a satellite's catchment (turnaround in the framework background, host tides
in the framework law, retention), applied to E3's sub-threshold systems; plus the satellites' own chemical lower bound.
Criteria: FROZEN_CRITERIA.md (committed alone first, c42925d9dc).

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 e6_native_fret.py            -> e6_native_fret.out, e6_native_fret_results.json,
                                                                         e6_per_system.csv
      OMP_NUM_THREADS=1 nice -n 15 python3 e6_native_fret.py --mutate   -> *_MUTATE.* (law acts outside the turnaround ball)
Deterministic (seeded), no network, seconds, one thread.  kappa = 1/2 FITTED; footings never pooled; not theory closed.
Read-only inputs: doors_push_2026_10_22/E3_dwarf_excess/e3_per_system.csv; real_research/data/dsph/lvd_dwarf_*.csv;
campaign_fresh_gravity/CFG654_independent_inputs/{cfg654_delta_ta.json, cfg654_ics_tables.npz};
campaign_fresh_gravity/CFG920_dwarf_baryon_loss_chemistry/cfg920_results.json (K4 only)."""
import csv, json, math, os, sys
import numpy as np
from scipy.special import exp1
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data", "dsph")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
E3 = os.path.join(os.path.dirname(HERE), "E3_dwarf_excess")
MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None


# ------------------------------------------------------------------ constants (sources: README ledger)
G_SI, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # BRIEF footings; kappa = 1/2 FITTED
FOOTS = ("canonical", "alt")
SUP = 5.364                                                 # Omega_c/Omega_b (Planck; CFG886 recovered, not pinned) -- LCDM-PROCESSED
OM_OC = (1.0 + SUP) / SUP                                   # M_ta per unit catchment cold
FRET_CENSUS = 0.10                                          # CFG416 census floor -- LCDM-PROCESSED (E3 reproduction only)
MHOST = {"MW": 6.0e10, "M31": 1.0e11}                       # MW: CFG332; M31: labelled external (as E3/D2)
GAS_FAC = 1.33                                              # HI -> gas (CFG920 / CFG873)
LOGY = (-0.5, -0.2, 0.1); GAMMA = 0.5772156649015329; LN10 = math.log(10.0)
NBOOT, SEED = 4000, 20261022
RNG = np.random.default_rng(SEED)

ICS = np.load(os.path.join(CFG, "CFG654_independent_inputs", "cfg654_ics_tables.npz"))
H_N = float(ICS["h"]); OM_N = (float(ICS["omega_b"]) + float(ICS["omega_c"])) / H_N ** 2     # native 0.67403, 0.31285
H0_SI = H_N * 100e3 / (1e3 * KPC)
RHOM0_SI = OM_N * 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
DTA = json.load(open(os.path.join(CFG, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA_Z, DTA_D = np.array(DTA["z"]), np.array(DTA["D"])


def nu(y):
    y = max(y, 1e-30); return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))


# ============================================================ spherical collapse (dust + Lambda, framework background, law off)
def shell_turnaround(delta_i, Om, a_i=1e-5, extra=None):
    """Dimensionless shell y = r / r_L (r_L = comoving Lagrangian radius), time in 1/H0.  Pure growing mode at a_i (EdS-like).
    extra(t, y) -> additional inward acceleration (units H0^2 r_L).  Returns (a_ta, y_ta, t_ta) or None."""
    OL = 1.0 - Om
    if OL > 0:
        t_of_a = lambda a: 2 / (3 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om * a ** 3))
        a_of_t = lambda t: (Om / OL) ** (1 / 3) * math.sinh(1.5 * math.sqrt(OL) * t) ** (2 / 3)
    else:
        t_of_a = lambda a: 2 / 3 * a ** 1.5
        a_of_t = lambda t: (1.5 * t) ** (2 / 3)
    Hi = math.sqrt(Om / a_i ** 3 + OL)
    y0 = a_i * (1 - delta_i / 3); v0 = Hi * y0 * (1 - delta_i / 3)        # f ~ 1 at a_i
    def rhs(t, s):
        acc = -0.5 * Om / s[0] ** 2 + OL * s[0]
        if extra is not None:
            acc -= extra(t, s[0])
        return [s[1], acc]
    ev = lambda t, s: s[1]; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (t_of_a(a_i), 6.0), [y0, v0], events=ev, rtol=1e-11, atol=1e-14, method="DOP853")
    if not sol.t_events[0].size:
        return None
    tt = sol.t_events[0][0]; yt = sol.y_events[0][0][0]
    return a_of_t(tt), yt, tt


def lin_D(a, Om):
    """growing mode D(a) for flat dust + Lambda, normalised D -> a at early times."""
    OL = 1 - Om; E = lambda x: math.sqrt(Om / x ** 3 + OL)
    I = quad(lambda x: 1.0 / (x * E(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12)[0]
    return 2.5 * Om * E(a) * I


def _ata(di, Om, a_i=1e-5, extra=None):
    r = shell_turnaround(di, Om, a_i, extra)
    return 10.0 if r is None else r[0]


def collapse_at(z_ta, Om, a_i=1e-5):
    """delta_i s.t. the shell turns around at z_ta.  Returns (Delta_ta = rho_shell/rho_mean, delta_lin at turnaround)."""
    a_t = 1.0 / (1 + z_ta)
    f = lambda ld: _ata(10 ** ld, Om, a_i) - a_t
    ld = brentq(f, math.log10(0.5 * a_i), math.log10(300 * a_i), xtol=1e-13)
    di = 10 ** ld
    at, yt, _ = shell_turnaround(di, Om, a_i)
    return (at / yt) ** 3, di * lin_D(at, Om) / lin_D(a_i, Om)


# ============================================================ CFG920 leaky box (copied verbatim from cfg920.py, K4-checked)
def elnx(X):
    if not np.isfinite(X):
        return -GAMMA
    if X < 1.0:
        lX, s, term = math.log(X), 0.0, X
        for n in range(40):
            s += term * (lX / (n + 1) - 1.0 / (n + 1) ** 2)
            term *= -X / (n + 1)
        return s / (-math.expm1(-X))
    return (-GAMMA - exp1(X) - math.exp(-X) * math.log(X)) / (1.0 - math.exp(-X))


def w1(feh, Ms, Mg, logy):
    if Mg <= 0:
        le = logy - GAMMA / LN10 - feh
        if le <= 0:
            return 0.0, 1.0, True
        eta = 10 ** le - 1.0
        return eta, 1.0 + eta, False

    def g(le):
        X = math.log((Mg + 10 ** le * Ms) / Mg)
        return logy - le + elnx(X) / LN10 - feh
    if g(0.0) <= 0:
        return 0.0, 1.0, True
    grid = np.linspace(0, 12.0, 241); vals = [g(x) for x in grid]
    k = next(i for i in range(1, len(grid)) if vals[i] <= 0)
    le = brentq(g, grid[k - 1], grid[k], xtol=1e-14, rtol=1e-14)
    eta = 10 ** le - 1.0
    return eta, ((1 + eta) * Ms + Mg) / (Ms + Mg), False


def u0_of(feh, logy):
    tgt = (feh - logy) * LN10
    if -GAMMA <= tgt:
        return None
    lo, hi = -40.0, 0.0
    while elnx(math.exp(hi)) < tgt and hi < 6.0:
        hi += 1.0
    if elnx(math.exp(hi)) < tgt:
        return float("inf")
    return math.exp(brentq(lambda s: elnx(math.exp(s)) - tgt, lo, hi, xtol=1e-15, rtol=1e-15))


def onepluseta_w2(u, feh, logy):
    return math.exp(logy * LN10 + elnx(u) - feh * LN10)


def L_w2(u, feh, logy):
    ope = onepluseta_w2(u, feh, logy)
    return ope if not np.isfinite(u) else ope / (-math.expm1(-u))


def family_min(fun, u0, ngrid=200, umax=60.0):
    if u0 is None:
        return None
    if not np.isfinite(u0) or u0 >= umax:
        return fun(float("inf")), float("inf")
    s_lo = math.log(u0)
    S = np.linspace(s_lo, math.log(umax), ngrid)
    vals = [fun(math.exp(s)) for s in S]; vinf = fun(float("inf"))
    i = int(np.argmin(vals))
    if vinf <= vals[i]:
        return vinf, float("inf")
    a, b = S[max(i - 1, 0)], S[min(i + 1, ngrid - 1)]
    if b > a:
        r = minimize_scalar(lambda s: fun(math.exp(s)), bounds=(a, b), method="bounded", options=dict(xatol=1e-12))
        if r.fun < vals[i]:
            return float(r.fun), math.exp(r.x)
    return float(vals[i]), math.exp(S[i])


def w2(feh, logy):
    u0 = u0_of(feh, logy)
    if u0 is None:
        return 1.0, float("inf"), 0.0, True
    Lm, um = family_min(lambda u: L_w2(u, feh, logy), u0)
    return Lm, um, onepluseta_w2(um, feh, logy) - 1.0, False


def chem_corners(feh, Ms, Mg):
    out = {}
    for ly in LOGY:
        e1, L1, f1 = w1(feh, Ms, Mg, ly)
        out[(ly, "W1")] = dict(L=L1, eta=e1, under=f1)
        if Mg <= 0:
            L2, u2, e2, f2 = w2(feh, ly)
            out[(ly, "W2")] = dict(L=L2, eta=e2, u=u2, under=f2)
        else:
            out[(ly, "W2")] = dict(L=L1, eta=e1, under=f1, same_as_W1=True)
    return out


NGL = 96
XL, WL = np.polynomial.legendre.leggauss(NGL)
XG, WG = np.polynomial.laguerre.laggauss(NGL)


def lnphi(x):
    x = np.asarray(x, dtype=float)
    small = x < 1e-7
    xs = np.where(small, 1.0, x)
    return np.where(small, -0.5 * x, np.log(-np.expm1(-xs) / xs))


def Phi(k, uq):
    if k <= 0:
        return 0.0
    if not np.isfinite(uq) or uq > 50.0:
        return float(np.sum(WG * lnphi(k * XG)))
    u = 0.5 * uq * (XL + 1.0); w = 0.5 * uq * WL
    return float(np.sum(w * np.exp(-u) * lnphi(k * u)) / (-math.expm1(-uq)))


def mean_lnZ(eta, zeta, uq, logy):
    k = (zeta - 1.0) * eta / (1.0 + eta)
    return logy * LN10 - math.log1p(eta) + elnx(uq) + Phi(k, uq)


def eta_zeta(uq, zeta, feh, logy):
    g = lambda le: mean_lnZ(math.expm1(le), zeta, uq, logy) - feh * LN10
    g0 = g(0.0)
    if g0 < 0:
        return None
    if g0 == 0:
        return 0.0
    hi = 1.0
    while g(hi) > 0 and hi < 40:
        hi *= 2.0
    if g(hi) > 0:
        return None
    return math.expm1(brentq(g, 0.0, hi, xtol=1e-12, rtol=1e-12))


def Lmin_zeta(zeta, feh, Ms, Mg, logy):
    if Mg <= 0:
        u0 = u0_of(feh, logy)
        if u0 is None:
            return 1.0

        def fun(u):
            e = eta_zeta(u, zeta, feh, logy)
            if e is None:
                return float("inf")
            return (1 + e) if not np.isfinite(u) else (1 + e) / (-math.expm1(-u))
        return family_min(fun, u0, ngrid=40)[0]
    g = lambda le: mean_lnZ(math.expm1(le), zeta, math.log((Mg + math.exp(le) * Ms) / Mg), logy) - feh * LN10
    if g(0.0) <= 0:
        return 1.0
    hi = 1.0
    while g(hi) > 0 and hi < 40:
        hi *= 2.0
    e = math.expm1(brentq(g, 0.0, hi, xtol=1e-12, rtol=1e-12))
    return ((1 + e) * Ms + Mg) / (Ms + Mg)


def zeta_need(Lreq, feh, Ms, Mg, logy=-0.5):
    if Lreq <= 1.0:
        return "none (L_req <= 1)"
    if Lmin_zeta(1.0, feh, Ms, Mg, logy) <= Lreq:
        return 1.0
    if Lmin_zeta(1000.0, feh, Ms, Mg, logy) > Lreq:
        return "> 1000"
    lz = brentq(lambda z: Lmin_zeta(10 ** z, feh, Ms, Mg, logy) - Lreq, 0.0, 3.0, xtol=1e-4)
    return float(10 ** lz)


# ============================================================ IC column: sigma(M) from the CFG654 native z = 0 linear P(k)
KH, PK = np.asarray(ICS["kh"], float), np.asarray(ICS["Plin0"], float)
_m = KH > KH[-1] / 10 ** 0.5
SLOPE_TAB = float(np.polyfit(np.log(KH[_m]), np.log(PK[_m]), 1)[0])
SLOPE_NS = float(ICS["ns"]) - 4.0
RHOM0_H = 2.77536627e11 * OM_N                               # (Msun/h) / (Mpc/h)^3


def Pk(k, slope):
    k = np.asarray(k, float)
    inside = np.interp(np.log(np.clip(k, KH[0], KH[-1])), np.log(KH), np.log(PK))
    out = np.where(k > KH[-1], math.log(PK[-1]) + slope * (np.log(k) - math.log(KH[-1])), inside)
    return np.exp(out)


def sigma_M(Mh, slope=None):
    slope = SLOPE_TAB if slope is None else slope
    R = (3 * Mh / (4 * math.pi * RHOM0_H)) ** (1 / 3)
    lk = np.linspace(math.log(KH[0]), math.log(300.0 / R), 6000)
    k = np.exp(lk); x = k * R
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapz(k ** 3 * Pk(k, slope) * W ** 2, lk) / (2 * math.pi ** 2))


LNA, LND = np.asarray(ICS["lna"], float), np.asarray(ICS["lnD"], float)
def D_native(z):
    return math.exp(float(np.interp(-math.log1p(z), LNA, LND)))      # D(z=0) = 1


# ============================================================ data
PER = list(csv.DictReader(open(os.path.join(E3, "e3_per_system.csv"))))
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DATA, fn))):
        LVD.setdefault(r["name"], r)

RES = dict(lane="E6_native_fret", criteria="c42925d9dc", mutate=MUT,
           settings=dict(A0=A0, SUP=SUP, OM_OC=OM_OC, MHOST=MHOST, h_native=H_N, Om_native=OM_N, LOGY=LOGY,
                         slope_tab=SLOPE_TAB, slope_ns=SLOPE_NS, nboot=NBOOT, seed=SEED), K={})
KOK = []


def ck(k, ok, val, thr, what):
    KOK.append(bool(ok)); RES["K"][k] = dict(pass_=bool(ok), value=val, threshold=thr, what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")


P("E6_native_fret  native satellite catchment rule + chemical lower bound, applied to E3's sub-threshold systems")
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled" + ("   [MUTATE: law acts outside the ball]" if MUT else ""))
P()

# ---------------- K1 spherical collapse
D_eds, dl_eds = collapse_at(5.0, 1.0)
zk = (0.0, 0.5, 1.0, 2.0, 4.0, 9.0)
mine = {z: collapse_at(z, OM_N) for z in zk}
rel = {z: mine[z][0] / float(np.interp(z, DTA_Z, DTA_D)) - 1 for z in zk}
ok1 = abs(D_eds / (9 * math.pi ** 2 / 16) - 1) <= 1e-4 and abs(dl_eds - 1.0624) <= 1e-3 and max(abs(v) for v in rel.values()) <= 0.01
ck("K1", ok1, f"EdS Delta {D_eds:.5f} dlin {dl_eds:.5f}; native vs CFG654 max|rel| {max(abs(v) for v in rel.values()):.4f}",
   "5.5517/1.0624 & <=1%", "spherical collapse in the framework background")
RES["K1_detail"] = {str(z): dict(Delta_mine=mine[z][0], dlin=mine[z][1], Delta_cfg654=float(np.interp(z, DTA_Z, DTA_D)), rel=rel[z]) for z in zk}

# ---------------- K2 catchment identity (code check; true by construction under Gauss)
# toy: inner ball (baryons Mb + cold Mc) turns around at z_b = 6; outer shell of 30x its mass turns around near z = 0 (law off).
Mb_t = 1.0e4; Mc_t = SUP * 10 * Mb_t; Min_t = (Mb_t + Mc_t)
Mout_t = 30 * Min_t
rL_out = (3 * Mout_t * MSUN / (4 * math.pi * RHOM0_SI)) ** (1 / 3)
a0t = A0["canonical"]
di0 = brentq(lambda ld: _ata(10 ** ld, OM_N) - 1.0, math.log10(5e-6), math.log10(3e-3), xtol=1e-13)
OLn = 1 - OM_N
t_b = 2 / (3 * math.sqrt(OLn)) * math.asinh(math.sqrt(OLn / OM_N * (1 / 7.0) ** 3))     # inner ball's turnaround (z = 6), 1/H0
Vf2 = math.sqrt(G_SI * Mb_t * MSUN * a0t)                                              # deep-law V^2 of the toy baryons
r_e = Mc_t * MSUN * G_SI / Vf2                                                         # edge: phantom mass = Mc (deep)
min_ratio = [float("inf")]


def law_inside(t, y):
    """law on inside the ball, phantom drawn from the catchment: at the shell (outside the edge) the enclosed gravitating
    mass is unchanged -> zero extra.  Track r / r_e to verify the shell stays outside."""
    if t >= t_b:
        min_ratio[0] = min(min_ratio[0], y * rL_out / r_e)
    return 0.0


def law_outside(t, y):
    """MUTATE reading (CFG654 bracket B / CFG548 reference): the toy baryons' phantom acts on the shell as an extra source."""
    if t < t_b:
        return 0.0
    r = y * rL_out; gN = G_SI * Mb_t * MSUN / r ** 2
    return gN * (nu(gN / a0t) - 1.0) / (H0_SI ** 2 * rL_out)


base = shell_turnaround(10 ** di0, OM_N)
on = shell_turnaround(10 ** di0, OM_N, extra=law_outside if MUT else law_inside)
dt_rel = abs(on[2] / base[2] - 1)
ok2 = dt_rel <= 1e-6 and (MUT or min_ratio[0] > 1.0)
ck("K2", ok2, f"|dt_ta/t_ta| {dt_rel:.2e}" + ("" if MUT else f"; min r/r_e after ball turnaround {min_ratio[0]:.1f}"), "<=1e-6",
   "catchment identity: shell outside the ball (code check, by construction)")
lag_ratio = None
if MUT:
    # how much larger would a law-driven catchment be: mass turning around at z = 0 with the extra source, same delta_i field?
    RES["K2_mutate_shift"] = dict(t_ta_off=base[2], t_ta_on=on[2], a_ta_off=base[0], a_ta_on=on[0])
RES["K2_detail"] = dict(t_ta_off=base[2], t_ta_test=on[2], rel=dt_rel, min_r_over_re=min_ratio[0], r_e_kpc=r_e / KPC,
                        rL_out_kpc=rL_out / KPC)

# ---------------- K3 E3 reproduction
def col(foot, key):
    return [fl(r[key]) for r in PER if r["footing"] == foot]

k3 = {}
for f in FOOTS:
    k3[f] = (float(np.median(col(f, "q_fret010"))), float(np.median(col(f, "L_req"))))
ok3_frozen = abs(k3["canonical"][0] - 0.811) <= 0.005 and abs(k3["alt"][0] - 0.768) <= 0.005 and \
    abs(k3["canonical"][1] - 8.3) <= 0.1 and abs(k3["alt"][1] - 8.0) <= 0.1
P(f"K3-as-frozen {'PASS' if ok3_frozen else 'FAIL'} q {k3['canonical'][0]:.3f}/{k3['alt'][0]:.3f} L_req {k3['canonical'][1]:.2f}/"
  f"{k3['alt'][1]:.2f} 0.811/0.768 +-0.005; 8.3/8.0 +-0.1  (mis-specified statistic, A1; not in the exit code)")
RES["K3_as_frozen"] = dict(pass_=ok3_frozen, q=[k3["canonical"][0], k3["alt"][0]], L=[k3["canonical"][1], k3["alt"][1]])
dq = max(abs(fl(r["q_fret010"]) - fl(r["L_req"]) / 10) / max(fl(r["L_req"]) / 10, 1e-300) for r in PER)
ok3 = abs(k3["canonical"][1] - 8.3) <= 0.1 and abs(k3["alt"][1] - 8.0) <= 0.1 and dq <= 1e-9
ck("K3'", ok3, f"L_req {k3['canonical'][1]:.2f}/{k3['alt'][1]:.2f}; max rel |q - L_req/10| {dq:.1e}", "8.3/8.0 +-0.1; <=1e-9",
   "E3 per-system CSV reproduced (A1)")

# ---------------- K4 CFG920 reproduction (Hercules)
c920 = json.load(open(os.path.join(CFG, "CFG920_dwarf_baryon_loss_chemistry", "cfg920_results.json")))["rows"]["Hercules"]
hc = chem_corners(c920["feh"], c920["Ms"], c920["Mg"])
dmax = max(abs(hc[(ly, w)]["L"] / c920["L_min"]["0"][f"{ly:+.1f}|{w}"] - 1) for ly in LOGY for w in ("W1", "W2"))
ck("K4", dmax <= 1e-6, f"max rel {dmax:.1e}", "<=1e-6", "CFG920 leaky box reproduced (Hercules, 6 corners)")

# ---------------- K5 sigma8
s8 = sigma_M(4 * math.pi / 3 * 8.0 ** 3 * RHOM0_H)
ck("K5", abs(s8 / 0.8271 - 1) <= 0.005, f"sigma8 {s8:.4f}", "0.8271 +-0.5%", "CFG654 native IC column")
P()

# ============================================================ D2/D3 per system
DLT = {}                                                       # delta_lin at turnaround vs z (own integrator)
for z in (0.0, 1, 2, 3, 4, 6, 9, 14, 20, 30, 49):
    DLT[z] = collapse_at(z, OM_N)[1]
_dz = np.array(sorted(DLT)); _dl = np.array([DLT[z] for z in _dz])
dlin_ta = lambda z: float(np.interp(math.log1p(z), np.log1p(_dz), _dl))
Dta_n = lambda z: float(np.interp(math.log1p(z), np.log1p(DTA_Z), DTA_D))


def host_T(Mh, d, a0):
    def g(x):
        gN = G_SI * Mh * MSUN / x ** 2; return gN * nu(gN / a0)
    h = 1e-4 * d
    return g(d) / d - (g(d + h) - g(d - h)) / (2 * h)


def z_req_of(T):
    tgt = 3 * T / (4 * math.pi * G_SI * RHOM0_SI)
    f = lambda lz: Dta_n(math.expm1(lz)) * math.exp(3 * lz) - tgt
    if f(0.0) >= 0:
        return 0.0
    if f(math.log(50.0)) < 0:
        return float("inf")
    return math.expm1(brentq(f, 0.0, math.log(50.0), xtol=1e-12))


ROWS = []
for r in PER:
    f = r["footing"]; nm = r["name"]; a0 = A0[f]; lv = LVD.get(nm, {})
    Ms = 10 ** fl(r["logMstar"]); Mdyn = fl(r["M_dyn"]); Mreq1 = fl(r["M_c_req"]); Lreq1 = fl(r["L_req"])
    Mb = Mreq1 / (SUP * Lreq1) if Lreq1 and Lreq1 > 0 else Ms
    Mreq2 = Mdyn - Ms / 2; Lreq2 = Mreq2 / (SUP * Mb)
    q_lo10 = fl(r["q_fret010_p2p5"])
    d = fl(lv.get("distance_host")); host = r["host"]
    row = dict(footing=f, name=nm, host=host, logMstar=math.log10(Ms), Mb=Mb, M_req_F1=Mreq1, M_req_F2=Mreq2, L_req_F1=Lreq1,
               L_req_F2=Lreq2, q_census_F1=fl(r["q_fret010"]), q_floor_F1=Lreq1, q_floor_F2=Lreq2, dhost_kpc=d)
    # D2
    if host in MHOST and d:
        T = host_T(MHOST[host], d * KPC, a0)
        zr = z_req_of(T); row.update(T=T, z_req=zr)
    else:
        row.update(T=None, z_req=None)
    # D3
    for tag, Mreq in (("F1", Mreq1), ("F2", Mreq2)):
        row[f"Mta_req_{tag}"] = Mreq * OM_OC
        if row["z_req"] is not None and np.isfinite(row["z_req"]) and Mreq > 1e-6 * Ms:   # A2: E3 floors M_req <= 0 at 1e-30
            Mh = Mreq * OM_OC * H_N
            dreq = dlin_ta(row["z_req"]) / D_native(row["z_req"])
            row[f"delta_req_{tag}"] = dreq
            row[f"nu_req_{tag}"] = dreq / sigma_M(Mh)
            row[f"nu_req_{tag}_ns"] = dreq / sigma_M(Mh, SLOPE_NS)
            row[f"rta_req_kpc_{tag}"] = (3 * Mreq * OM_OC * MSUN / (4 * math.pi * Dta_n(row["z_req"]) * RHOM0_SI)) ** (1 / 3) / (1 + row["z_req"]) / KPC
        else:
            row[f"nu_req_{tag}"] = None
    # Part C
    feh = fl(lv.get("metallicity")); mhi = fl(lv.get("mass_HI"))
    Mg = GAS_FAC * 10 ** mhi if mhi is not None else 0.0
    row["feh"] = feh; row["Mg"] = Mg
    if feh is not None:
        cc = chem_corners(feh, Ms, Mg)
        for ly in LOGY:
            for w in ("W1", "W2"):
                key = f"{ly:+.1f}|{w}"; L = cc[(ly, w)]["L"]
                row[f"Lmin_{key}"] = L; row[f"under_{key}"] = cc[(ly, w)]["under"]
                row[f"qchem_F1_{key}"] = Lreq1 / L; row[f"qchem_F2_{key}"] = Lreq2 / L
        Lc = row["Lmin_-0.5|W2"]
        row["qchem_F1_lo2s"] = (q_lo10 * 10.0 / Lc) if q_lo10 is not None else None
        row["zeta_need_F1"] = zeta_need(Lreq1, feh, Ms, Mg) if Lreq1 / Lc > 1 else None
        # A2 (post-result): for systems the chemistry floor supplies, the metal-enhanced wind zeta at which it stops supplying
        row["zeta_break_F1"] = zeta_need(Lreq1, feh, Ms, Mg) if (Lreq1 / Lc <= 1 and Lreq1 > 1) else None
    ROWS.append(row)


def boot(x):
    x = np.asarray(x, float); n = len(x)
    m = np.median(x[RNG.integers(0, n, size=(NBOOT, n))], axis=1)
    return float(np.median(x)), float(np.percentile(m, 16)), float(np.percentile(m, 84))


SUM = {}
P("[D1] the law acts only inside the turnaround ball and its phantom is drawn from the same catchment (sum zero), so every")
P("     shell outside the ball turns around under GR dust + Lambda with its true enclosed mass: M_ta is set by the patch's")
P("     initial overdensity and by when accretion stops. M_b, a0, kappa, L* do not enter. (K2 is the code check.)")
P(f"     toy: edge r_e {r_e / KPC:.2f} kpc, outer shell Lagrangian radius {rL_out / KPC:.1f} kpc; {'MUTATE (law outside)' if MUT else 'law inside'} t_ta shift {dt_rel:.3e}")
P()
for f in FOOTS:
    R = [x for x in ROWS if x["footing"] == f]; S = {}
    P(f"[{f}] N = {len(R)}")
    for tag in ("F1", "F2"):
        S[f"q_census_{tag}"] = boot([x["q_census_F1"] if tag == "F1" else x["L_req_F2"] / 10 for x in R])
        S[f"q_floor_{tag}"] = boot([x[f"L_req_{tag}"] for x in R])
        P(f"  {tag} q census f_ret 0.10: {S[f'q_census_{tag}'][0]:.3f} [{S[f'q_census_{tag}'][1]:.3f}-{S[f'q_census_{tag}'][2]:.3f}]   "
          f"f_ret 1 (floor): {S[f'q_floor_{tag}'][0]:.2f} [{S[f'q_floor_{tag}'][1]:.2f}-{S[f'q_floor_{tag}'][2]:.2f}]   "
          f"median M_ta,req {np.median([x[f'Mta_req_{tag}'] for x in R]):.3e} Msun")
    zr = [x["z_req"] for x in R if x["z_req"] is not None]
    S["z_req_median"] = float(np.median(zr)); S["z_req_range"] = [float(min(zr)), float(max(zr))]; S["n_zreq"] = len(zr)
    P(f"  D2 tidal epoch z_req (turnaround sphere denser than 3T/4piG at d_now): median {S['z_req_median']:.2f}, range "
      f"{S['z_req_range'][0]:.2f}-{S['z_req_range'][1]:.2f} (N {len(zr)}; field systems undefined)")
    for tag in ("F1", "F2"):
        nv = [x[f"nu_req_{tag}"] for x in R if x.get(f"nu_req_{tag}") is not None]
        nvs = [x[f"nu_req_{tag}_ns"] for x in R if x.get(f"nu_req_{tag}") is not None]
        rt = [x[f"rta_req_kpc_{tag}"] for x in R if x.get(f"nu_req_{tag}") is not None]
        S[f"nu_req_{tag}"] = boot(nv); S[f"nu_req_{tag}_ns_median"] = float(np.median(nvs)); S[f"nu_req_{tag}_max"] = float(max(nv))
        S[f"n_nu_{tag}"] = len(nv); S[f"n_nu_gt3_{tag}"] = int(sum(v > 3 for v in nv))
        P(f"  D3 {tag} nu_req (IC column, EXTERNALLY CALIBRATED): median {S[f'nu_req_{tag}'][0]:.2f} [{S[f'nu_req_{tag}'][1]:.2f}-"
          f"{S[f'nu_req_{tag}'][2]:.2f}], max {S[f'nu_req_{tag}_max']:.2f}, >3: {S[f'n_nu_gt3_{tag}']}/{len(nv)}; slope n_s-4 median "
          f"{S[f'nu_req_{tag}_ns_median']:.2f}; physical r_ta,req median {np.median(rt):.2f} kpc")
    T = [x for x in R if x["feh"] is not None]; S["n_chem"] = len(T); S["n_chem_untested"] = len(R) - len(T)
    P(f"  Part C chemistry: tested {len(T)} / {len(R)} (no LVD [Fe/H]: {', '.join(x['name'] for x in R if x['feh'] is None) or 'none'})")
    for tag in ("F1", "F2"):
        for ly in LOGY:
            for w in ("W2", "W1"):
                key = f"{ly:+.1f}|{w}"
                S[f"qchem_{tag}_{key}"] = boot([x[f"qchem_{tag}_{key}"] for x in T])
        lm = boot([x["Lmin_-0.5|W2"] for x in T])
        S["Lmin_cons_median"] = lm
        P(f"   {tag} median q_chem  " + "  ".join(f"{ly:+.1f}{w}:{S[f'qchem_{tag}_{ly:+.1f}|{w}'][0]:.3f}" for ly in LOGY for w in ("W2", "W1"))
          + f"   (conservative corner 84%: {S[f'qchem_{tag}_-0.5|W2'][2]:.3f})")
    P(f"   median L_min (-0.5, W2) {S['Lmin_cons_median'][0]:.1f}  vs median L_req F1 {np.median([x['L_req_F1'] for x in R]):.2f}  "
      f"(census 10)")
    over = [x for x in T if x["qchem_F1_-0.5|W2"] > 1]
    over2 = [x for x in T if x["qchem_F1_lo2s"] is not None and x["qchem_F1_lo2s"] > 1]
    S["chem_over_central"] = [x["name"] for x in over]; S["chem_over_2s"] = [x["name"] for x in over2]
    S["zeta_need"] = {x["name"]: x["zeta_need_F1"] for x in over}
    P(f"   F1 q_chem > 1 at the conservative corner: central {len(over)} ({', '.join(x['name'] for x in over) or 'none'}); "
      f"at 2 sigma {len(over2)} ({', '.join(x['name'] for x in over2) or 'none'})")
    if over:
        P("   zeta_need (metal-enhanced wind that would remove the bound, log y -0.5): " +
          ", ".join(f"{x['name']} {x['zeta_need_F1'] if isinstance(x['zeta_need_F1'], str) else round(x['zeta_need_F1'], 2)}" for x in over))
    zb = [x["zeta_break_F1"] for x in T if x.get("zeta_break_F1") is not None]
    zbn = [1001.0 if isinstance(v, str) else v for v in zb]
    S["zeta_break_median"] = float(np.median(zbn)) if zbn else None; S["zeta_break_min"] = float(min(zbn)) if zbn else None
    S["n_zeta_break"] = len(zbn); S["n_zeta_break_le3"] = int(sum(v <= 3 for v in zbn))
    if zbn:
        P(f"   A2 (post-result) zeta_break, F1 (-0.5): metal-enhanced wind at which the floor stops supplying, over {len(zbn)} supplied "
          f"systems: median {S['zeta_break_median']:.2f}, min {S['zeta_break_min']:.2f}, <= 3 for {S['n_zeta_break_le3']} (>1000 counted 1001)")
    zinf = [x["name"] for x in R if x["z_req"] is not None and not np.isfinite(x["z_req"])]
    S["z_req_beyond_49"] = zinf
    P(f"   D2 systems whose required turnaround density exceeds the z = 49 value: {', '.join(zinf) or 'none'}")
    und = [x["name"] for x in T if x["under_-0.5|W2"]]
    S["chem_underproduced_cons"] = und
    if und:
        P(f"   chemistry under-produces [Fe/H] at (-0.5, W2) (L_min := 1, favours shortfall): {', '.join(und)}")
    SUM[f] = S
    P()
RES["summary"] = SUM

# ============================================================ classes
cls_chem = {}
for f in FOOTS:
    S = SUM[f]
    if S["qchem_F1_-0.5|W2"][0] <= 1 and S["qchem_F1_-0.5|W2"][2] <= 1:
        cls_chem[f] = "CHEM-SUPPLIES"
    elif S["qchem_F1_+0.1|W1"][0] > 1 and S["qchem_F1_+0.1|W1"][1] > 1:
        cls_chem[f] = "CHEM-SHORTFALL"
    else:
        cls_chem[f] = "CHEM-UNDERDETERMINED"
nu_med = {f: max(SUM[f]["nu_req_F1"][0], SUM[f]["nu_req_F2"][0]) for f in FOOTS}
cls_ic = {f: ("IC-ORDINARY" if nu_med[f] <= 3 else ("IC-FORBIDS" if nu_med[f] >= 5 else "IC-STRAINED")) for f in FOOTS}
if all(SUM[f]["nu_req_F1"][0] >= 5 for f in FOOTS):
    main = "SHORTFALL under the IC column (externally calibrated)"
else:
    main = ("STILL UNDECIDABLE -- ingredient: the satellite's Lagrangian catchment mass, i.e. the initial overdensity of its patch "
            "and the epoch its accretion stopped (infall); the law, the host's tides and M_b do not fix it (D1)")
RES["classes"] = dict(main=main, ic=cls_ic, chem=cls_chem)
P(f"-> MAIN (dynamics): {main}")
for f in FOOTS:
    P(f"-> {f}: D3 {cls_ic[f]} (median nu_req F1 {SUM[f]['nu_req_F1'][0]:.2f} / F2 {SUM[f]['nu_req_F2'][0]:.2f});  Part C {cls_chem[f]} "
      f"(q_chem F1 at -0.5 W2 {SUM[f]['qchem_F1_-0.5|W2'][0]:.3f}, at +0.1 W1 {SUM[f]['qchem_F1_+0.1|W1'][0]:.3f})")
P()
npass = sum(KOK)
P(f"E6_NATIVE_FRET COMPLETE: {npass}/{len(KOK)} checks PASS.")

with open(os.path.join(HERE, f"e6_native_fret{SFX}.out"), "w") as fo:
    fo.write("\n".join(OUT) + "\n")
RES["rows"] = ROWS
with open(os.path.join(HERE, f"e6_native_fret_results{SFX}.json"), "w") as fo:
    json.dump(RES, fo, indent=1, default=lambda o: None if (isinstance(o, float) and not math.isfinite(o)) else str(o))
keys = ["footing", "name", "host", "logMstar", "feh", "dhost_kpc", "L_req_F1", "L_req_F2", "q_census_F1", "z_req",
        "Mta_req_F1", "nu_req_F1", "nu_req_F2", "Lmin_-0.5|W2", "Lmin_+0.1|W1", "qchem_F1_-0.5|W2", "qchem_F1_+0.1|W1",
        "qchem_F2_-0.5|W2", "qchem_F1_lo2s", "zeta_need_F1", "zeta_break_F1"]
with open(os.path.join(HERE, f"e6_per_system{SFX}.csv"), "w", newline="") as fo:
    w = csv.writer(fo); w.writerow(keys)
    for x in ROWS:
        w.writerow([x.get(k) for k in keys])
sys.exit(0 if npass == len(KOK) else 1)
