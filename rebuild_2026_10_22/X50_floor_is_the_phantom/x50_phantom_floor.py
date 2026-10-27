#!/usr/bin/env python3
"""X50_floor_is_the_phantom: is X38's a0/(2 pi G) floor halo the law's own phantom halo (simple nu)?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (4d3134a014, committed alone). EM1's SPARC machinery (up to its
backgrounds block) is executed read-only; X38's Burkert solver and X49's dwarf path are copied; X40b / X43 / X49 / EM1 / F3
committed JSONs are read. One thread, about a minute.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x50_phantom_floor.py                -> .out, _results.json
    X50_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x50_phantom_floor.py   -> nu -> 1 (K0b, K2, K3 must fail)
"""
import os, sys, io, csv, json, math, time, resource, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar, least_squares
from scipy.integrate import quad
warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
MUTATE = os.environ.get("X50_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
FEET = ("canonical", "alt")
C_B = 0.254484                    # X47: Burkert floor peak self-pull / a0 (task2a, zeta_over_a0)
RES = dict(lane="X50_floor_is_the_phantom", frozen="4d3134a014", mutate=MUTATE, checks={}, analytic={}, sparc={}, dwarfs={}, clusters={})
checks = []
def check(k, ok, msg):
    checks.append((k, bool(ok))); RES["checks"][k] = dict(ok=bool(ok), detail=msg); P(f"{k} {'PASS' if ok else 'FAIL'}: {msg}")

def nu(y):
    """The record's simple nu (P4, EM1); MUTATE: nu = 1 (no phantom)."""
    y = np.asarray(y, float)
    return np.ones_like(y) if MUTATE else 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))

P(f"X50_floor_is_the_phantom  {'MUTATE run (nu -> 1, no phantom)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy is a w ~ 0 field component (not matter); law phantom vs X38 floor halo; not theory closed")

# ===================================================================== EM1 machinery (read-only)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
codeE = TE[:TE.index("# ---------------- backgrounds")]
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, line, UPS, A0 = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "A0"))
G, MSUN, MPC = NE["G"], NE["MSUN"], NE["MPC"]
PC = 3.0857e16
SIG = {f: A0[f] / (2 * math.pi * G) for f in FEET}
SIGPC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}
P(f"EM1 machinery read-only: {len(GALS)} galaxies; Sigma_a0 {SIGPC['canonical']:.1f} / {SIGPC['alt']:.1f} Msun/pc^2  [{time.time() - T0:.0f} s]")

# ===================================================================== X38's Burkert solver (copied)
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot):
        SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
def rho_c(h): return 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
def x38_r0(q, f, bg):
    M200 = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)) * MSUN; R200 = (3 * M200 / (4 * math.pi * 200 * rho_c(bg["h"]))) ** (1 / 3)
    return solve_r0(M200, R200, SIG[f])
def g_burk(r, Sig, r0): return G * math.pi * Sig * r0 ** 2 * B(np.asarray(r) / r0) / np.asarray(r) ** 2

# ===================================================================== STEP 0
X38REF = {("canonical", "A_c2b_refit"): (0.0795, 0.77), ("canonical", "B_cfg886_bg"): (0.0792, 0.76),
          ("alt", "A_c2b_refit"): (0.0729, 0.60), ("alt", "B_cfg886_bg"): (0.0729, 0.60)}
X38R0 = {}; X38U = {}; s0 = []
for f in FEET:
    for t, bg in BGS.items():
        rows = []; r0s = []
        for q in GALS:
            r0 = x38_r0(q, f, bg); r0s.append(r0)
            rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + g_burk(q["Rm"], SIG[f], r0)[:, None], 1e-300))))
        st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
        X38R0[(f, t)] = r0s; X38U[(f, t)] = [int(r[2]) for r in rows]
        ref = X38REF[(f, t)]; ok = abs(st["rms"] - ref[0]) < 1e-4 and abs(st["U_median"] - ref[1]) < 1e-9
        s0.append(ok); P(f"  X38 row [{f}, {t}]: rms {st['rms']:.4f} @ U {st['U_median']:.2f} (X38 {ref[0]}@{ref[1]}): {'ok' if ok else 'MISMATCH'}")
check("K0a", all(s0), "X38's four SPARC rows reproduced")
P4R = {"canonical": (0.054087447879939264, 0.52), "alt": (0.05371798965550355, 0.44)}
LAWU = {}; lawok = []; LAWROW = {}
for f in FEET:
    rows = [fit_one(q, np.log10(np.maximum(nu(q["GB"] / A0[f]) * q["GB"], 1e-300))) for q in GALS]
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]); LAWROW[f] = st
    LAWU[f] = [int(r[2]) for r in rows]
    lawok.append(abs(st["rms"] - P4R[f][0]) < 1e-4 and abs(st["U_median"] - P4R[f][1]) < 1e-9)
    P(f"  law row [{f}]: rms {st['rms']:.6f} @ U {st['U_median']:.2f} (P4 {P4R[f][0]:.6f}@{P4R[f][1]:.2f})")
check("K0b", all(lawok), "P4's law row reproduced with this lane's nu")
STEP0 = all(s0) and all(lawok)
RES["step0"] = dict(x38=all(s0), law=all(lawok), law_rows=LAWROW)
P(f"  [{time.time() - T0:.0f} s]")

# ===================================================================== ANALYTIC (sympy)
P("\n=== ANALYTIC (sympy)")
y, t, x, u = sp.symbols("y t x u", positive=True)
nu_s = sp.Integer(1) if MUTATE else sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)
Q_s = sp.simplify(y * (nu_s - 1))
Qlim = sp.limit(Q_s, y, sp.oo)
Q_id = sp.simplify(Q_s - 1 / nu_s) == 0                                       # A1: Q = y(nu - 1) = 1/nu (cancellation-free)
Qf = lambda yy: (0.0 * np.asarray(yy, float)) if MUTATE else 1.0 / nu(yy)
ygrid = np.logspace(-6, 8, 400); Qv = np.broadcast_to(np.asarray(Qf(ygrid), float), ygrid.shape)
mono = bool(np.all(np.diff(Qv) > 0)) and bool(np.all(Qv < 1))
# S(y) = int_0^y (nu - 1) dt; closed form of the record's nu (always the record's nu, as frozen for K2)
S_closed = lambda yy: 0.5 * np.sqrt(yy * (yy + 4)) + 2 * np.log((np.sqrt(yy) + np.sqrt(yy + 4)) / 2) - yy / 2
S_sym = sp.Rational(1, 2) * sp.sqrt(y * (y + 4)) + 2 * sp.log((sp.sqrt(y) + sp.sqrt(y + 4)) / 2) - y / 2
nu_rec = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)
dS_ok = sp.simplify(sp.diff(S_sym, y) - (nu_rec - 1)) == 0 and sp.simplify(S_sym.subs(y, 0)) == 0
nu_lane = (lambda tt: float(nu(tt)) - 1.0)
qS = [abs(quad(nu_lane, 0, yy, limit=400, epsabs=0, epsrel=1e-12)[0] - float(S_closed(yy))) / float(S_closed(yy)) for yy in (0.01, 0.3, 1.0, 10.0, 1000.0)]
check("K1", Qlim == 1 and Q_id and mono and dS_ok and max(qS) < 1e-8,
      f"lim Q = {Qlim}; Q = 1/nu (sympy): {Q_id}; Q monotone and < 1 on 1e-6..1e8: {mono}; dS/dy = nu - 1 (sympy): {dS_ok}; S closed vs quad max rel {max(qS):.1e}")
S_small = sp.series(S_sym, y, 0, 1).removeO(); S_large = sp.limit(S_sym - sp.log(y), y, sp.oo)
y_S1 = brentq(lambda yy: S_closed(yy) - 1.0, 1e-6, 1e6); y_Spi2 = brentq(lambda yy: S_closed(yy) - math.pi / 2, 1e-6, 1e6)
P(f"A1 Q(y) = y(nu-1) = {sp.simplify(Q_s)}; lim_(y->oo) Q = {Qlim}; so |g_ph| < a0, i.e. pull-equivalent Sigma < 1/c_B = {1 / C_B:.3f} Sigma_a0; "
  f"mean enclosed M_ph/(pi r^2) < 2 Sigma_a0")
P(f"   Q at y = 0.0869 equals c_B (phantom pull = floor peak pull): Q(0.0869) = {float(Qf(0.0869)):.4f}; y where Q = c_B: "
  f"{brentq(lambda yy: float(Qf(yy)) - C_B, 1e-6, 1e6) if not MUTATE else float('nan'):.4f}")
P(f"A2 thin-disc axis column Sigma_ph(0) = Sigma_M S(y_s), S(y) = {S_sym}; S ~ {S_small} (y->0); S - ln y -> {S_large} (y->oo): "
  f"UNBOUNDED (logarithmic) for the simple nu")
P(f"   S = 1 (column = Sigma_a0) at y_s = {y_S1:.4f}; S = pi/2 (the floor Burkert's own central column) at y_s = {y_Spi2:.4f}")
# A3 shapes
xs = sp.symbols("x", positive=True)
f_pm = sp.sqrt(sp.Rational(1, 4) + xs ** 2) - sp.Rational(1, 2)     # M_ph/M for a point mass, x = r/r_M (record's nu)
rho_pm = sp.simplify(sp.diff(f_pm, xs) / (4 * sp.pi * xs ** 2))
pm_small = sp.limit(rho_pm * xs, xs, 0); pm_large = sp.limit(rho_pm * xs ** 2, xs, sp.oo)
P(f"A3 point mass: M_ph(<r)/M = {f_pm} (x = r/r_M, r_M = sqrt(GM/a0)); rho_ph = M/(r_M^3) * {rho_pm}; "
  f"x->0: rho ~ {pm_small}/x (1/r cusp); x->oo: rho ~ {pm_large}/x^2 = sqrt(G M a0)/(4 pi G r^2)")
# cored sphere and spherical-equivalent exponential disc: central log-slope of rho_ph (record's nu)
r_, k_, yc = sp.symbols("r k y_c", positive=True)
def rho_ph_expr(gN):
    yy = gN; gph = yy * (sp.sqrt(sp.Rational(1, 4) + 1 / yy) - sp.Rational(1, 2)); return sp.diff(r_ ** 2 * gph, r_) / r_ ** 2
slope_core = sp.limit(r_ * sp.diff(sp.log(rho_ph_expr(k_ * r_)), r_), r_, 0)
gN_disc = 2 * yc * (1 - (1 + r_) * sp.exp(-r_)) / r_ ** 2                   # y(r) for an exponential disc, y_c = pi G Sigma0/a0 at r->0
slope_disc_e = r_ * sp.diff(sp.log(rho_ph_expr(gN_disc)), r_)
slope_disc = {str(v): float(sp.limit(slope_disc_e.subs(yc, v), r_, 0)) for v in (sp.Rational(1, 10), sp.Integer(1), sp.Integer(10))}   # A1: evaluated
P(f"   cored baryon sphere (g_N = k r): central d ln rho_ph/d ln r = {slope_core}; spherical-equivalent exponential disc: {slope_disc}; "
  "Burkert: 0 (core) and -3 (tail); phantom tail -2 (deep MOND)")
P("A4 Sigma_ph,max: the strict bound is on the phantom's own pull, |g_ph| < a0 = 2 pi G Sigma_a0 (mean enclosed phantom surface density "
  "< 2 Sigma_a0; pull-equivalent Burkert rho0 r0 < 3.93 Sigma_a0). The central column of a thin disc is Sigma_a0 S(y_s), which equals "
  f"Sigma_a0 at y_s = {y_S1:.3f} and grows as ln y_s beyond; a0/(2 pi G) is the column scale, not a cap, for the simple nu.")
RES["analytic"] = dict(Q=str(Q_s), Q_limit=str(Qlim), S=str(S_sym), S_small=str(S_small), S_minus_lny_large=str(S_large),
                       y_S_eq_1=y_S1, y_S_eq_pi2=y_Spi2, pull_equiv_bound_Sigma_a0=1 / C_B, point_mass_MphM=str(f_pm), point_mass_rho=str(rho_pm),
                       rho_small=str(pm_small), rho_large=str(pm_large), slope_core_sphere=str(slope_core), slope_disc_spherical=str(slope_disc))

# K2: numerical exponential thin disc on the axis (units G = a0 = Rd = 1)
def disc_column(ys):
    S0 = ys / (2 * math.pi)                                         # 2 pi G Sigma0 / a0 = ys
    def gz(z): return -2 * math.pi * S0 * quad(lambda k: k * math.exp(-k * z) * (1 + k * k) ** -1.5, 0, np.inf, limit=500)[0]
    def dRgR(z): return -math.pi * S0 * quad(lambda k: k * k * math.exp(-k * z) * (1 + k * k) ** -1.5, 0, np.inf, limit=500)[0]
    zz = np.logspace(-9, 3, 2400)
    GZ = np.array([gz(z) for z in zz]); DR = np.array([dRgR(z) for z in zz])
    nm1 = nu(np.abs(GZ)) - 1.0
    Fz = nm1 * GZ
    divF = 2 * nm1 * DR + np.gradient(Fz, zz)
    rho = -divF / (4 * math.pi)
    lz = np.log(zz); half = float(np.sum(0.5 * (rho[1:] * zz[1:] + rho[:-1] * zz[:-1]) * np.diff(lz)))
    M = 2 * math.pi * S0; rM = math.sqrt(M); Xz = zz[-1] / rM                 # tail beyond z_max: point-mass phantom (record's nu)
    tail = M / (4 * math.pi * rM ** 3) * quad(lambda xx: 1 / (xx * math.sqrt(xx * xx + 0.25)), Xz, np.inf)[0] * rM if not MUTATE else 0.0
    sheet = (float(nu(np.array(ys))) - 1.0) * S0
    return sheet + 2 * (half + tail)
k2 = []
for ys in (0.1, 1.0, 10.0):
    num = disc_column(ys); ana = float(S_closed(ys)) / (2 * math.pi)        # Sigma_M = a0/(2 pi G) = 1/(2 pi)
    k2.append(abs(num / ana - 1)); P(f"   K2 exponential disc y_s {ys}: numerical column {num:.6f}, Sigma_M S(y_s) {ana:.6f}, rel {num / ana - 1:+.2e}")
check("K2", max(k2) < 1e-3, f"thin-disc axis column vs Sigma_M S(y_s), max rel {max(k2):.1e}")
# K3: point mass
fnum = lambda xx: float(nu(np.array(1 / xx ** 2))) - 1.0
tail100 = fnum(100.0) / 100.0
dfx = lambda xx: (fnum(xx * (1 + 1e-6)) - fnum(xx * (1 - 1e-6))) / (2e-6 * xx)
qm = quad(lambda xx: dfx(xx), 1e-8, 3.0, limit=400, epsrel=1e-10)[0]
k3 = abs(tail100 - 1) < 1e-2 and abs(qm - fnum(3.0)) < 1e-6
check("K3", k3, f"point mass M_ph(<100 r_M)/(100 sqrt(M a0/G)) = {tail100:.4f} (-> 1); int 4 pi r^2 rho_ph to 3 r_M = {qm:.7f} vs (nu-1)M = {fnum(3.0):.7f}")
P(f"  [{time.time() - T0:.0f} s]")

# ===================================================================== SPARC per galaxy
P("\n=== SPARC per galaxy: law phantom (P4 Upsilon) vs X38 floor halo (bg A)")
SBD = np.array([q["meta"]["SBdisk"] for q in GALS])
def spearman(a, b):
    a = np.asarray(a); b = np.asarray(b); m = np.isfinite(a) & np.isfinite(b); a, b = a[m], b[m]
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float); ra -= ra.mean(); rb -= rb.mean()
    return float((ra * rb).sum() / math.sqrt((ra ** 2).sum() * (rb ** 2).sum()))
def pct(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if v.size == 0: return dict(median=float("nan"), p16=float("nan"), p84=float("nan"), N=0)
    return dict(median=float(np.median(v)), p16=float(np.percentile(v, 16)), p84=float(np.percentile(v, 84)), N=int(v.size))
def outer_slope(r, M):
    n = len(r);
    if n < 4: return np.nan
    o = slice(n // 2, n); return float(np.polyfit(np.log(r[o]), np.log(M[o]), 1)[0]) - 3.0
def burk_fit(r, M, Sig_ref):
    def res(p): return np.log(math.pi * 10 ** p[0] * Sig_ref * (10 ** p[1] * r[-1]) ** 2 * B(r / (10 ** p[1] * r[-1]))) - np.log(M)
    best = None
    for lr in (-1.0, 0.0, 1.0):
        s = least_squares(res, [0.0, lr], bounds=([-4, -3], [4, 3]))
        if best is None or s.cost < best.cost: best = s
    hit = bool(np.any(np.abs(best.x - np.array([0, 0])) > np.array([3.99, 2.99])))
    return float(best.x[0]), hit
def per_galaxy(f, tbg="A_c2b_refit", ups_from="law"):
    a0 = A0[f]; rows = []
    U_idx = LAWU[f] if ups_from == "law" else X38U[(f, tbg)]
    for gi, q in enumerate(GALS):
        i = U_idx[gi]; ok = q["OK"][:, i]
        if ok.sum() < 2: continue
        r = q["Rm"][ok]; gN = q["GB"][ok, i]; o = np.argsort(r); r, gN = r[o], gN[o]
        gph = (nu(gN / a0) - 1.0) * gN
        r0 = X38R0[(f, tbg)][gi]; gh = g_burk(r, SIG[f], r0)
        if not np.all(gph > 0):
            rows.append(dict(name=q["name"], zero=True)); continue
        d = np.log10(gph / gh)
        Ups = UPS[i]; Sb0 = Ups * SBD[gi] * MSUN / PC ** 2; ys = 2 * math.pi * G * Sb0 / a0
        rows.append(dict(name=q["name"], zero=False, logq=float(d[-1]), logs=float(np.log10(gph.max() / gh.max())),
                         shape=float(np.sqrt(np.mean((d - d.mean()) ** 2))), pull_equiv=float(np.log10(gph.max() / (C_B * a0))),
                         x38_pull_equiv=float(np.log10(gh.max() / (C_B * a0))),
                         slope_ph=outer_slope(r, gph * r * r / G), slope_x38=outer_slope(r, gh * r * r / G),
                         col_ratio=float(S_closed(ys) / (math.pi / 2)) if ys > 0 else np.nan, logSb0=math.log10(max(Sb0 * PC ** 2 / MSUN, 1e-9)),
                         Rlast_over_r0=float(r[-1] / r0), U=float(Ups), r=r, Mph=gph * r * r / G))
    return rows
def summarise(rows, f, fit=False):
    R = [x for x in rows if not x["zero"]]; nz = len(rows) - len(R)
    m1 = pct([x["logq"] for x in R]); m2 = pct([x["logs"] for x in R]); m3 = pct([x["shape"] for x in R])
    hw = (m1["p84"] - m1["p16"]) / 2
    g1 = abs(m1["median"]) <= 0.10 and hw <= 0.20; g2 = abs(m2["median"]) <= 0.10; g3 = m3["median"] <= 0.10
    out = dict(N=len(R), N_zero_phantom=nz, M1_logq=m1, M1_halfwidth=hw, M2_logs=m2, M3_shape=m3, gate_M1=g1, gate_M2=g2, gate_M3=g3,
               pull_equiv_phantom=pct([x["pull_equiv"] for x in R]), pull_equiv_x38=pct([x["x38_pull_equiv"] for x in R]),
               slope_phantom=pct([x["slope_ph"] for x in R]), slope_x38=pct([x["slope_x38"] for x in R]),
               disc_col_over_floor_col=pct([x["col_ratio"] for x in R]), frac_col_gt_floor=float(np.mean([x["col_ratio"] > 1 for x in R if np.isfinite(x["col_ratio"])])) if R else float("nan"),
               spearman_logs_logSb0=float("nan") if len(R) < 3 else spearman([x["logs"] for x in R], [x["logSb0"] for x in R]),
               frac_phantom_heavier_Rlast=float(np.mean([x["logq"] > 0 for x in R])) if R else float("nan"), frac_pull_higher=float(np.mean([x["logs"] > 0 for x in R])) if R else float("nan"),
               Rlast_over_r0=pct([x["Rlast_over_r0"] for x in R]))
    if fit:
        bf = [burk_fit(x["r"], x["Mph"], SIG[f]) for x in R]
        out["burkert_fit_rho0r0_dex"] = pct([b[0] for b in bf]); out["burkert_fit_at_bound"] = int(sum(b[1] for b in bf))
    return out
SP = {}
for f in FEET:
    rows = per_galaxy(f); s = summarise(rows, f, fit=True)
    sB = summarise(per_galaxy(f, "B_cfg886_bg"), f); sU = summarise(per_galaxy(f, ups_from="x38"), f)
    if not s["gate_M2"]:
        v = "PF FAILS"
    elif s["gate_M1"] and s["gate_M3"]:
        v = "PF HOLDS"
    else:
        v = "PF HOLDS IN SURFACE DENSITY ONLY"
    s.update(verdict=v, variant_bgB=sB, variant_x38_Upsilon=sU); SP[f] = s
    P(f"\n[{f}] N {s['N']} (phantom zero at some point: {s['N_zero_phantom']})")
    P(f"  M1 log M_ph/M_X38 at R_last: median {s['M1_logq']['median']:+.3f} (16-84 {s['M1_logq']['p16']:+.3f}, {s['M1_logq']['p84']:+.3f}; half-width {s['M1_halfwidth']:.3f}) "
      f"-> {'pass' if s['gate_M1'] else 'FAIL'}; phantom heavier in {s['frac_phantom_heavier_Rlast']:.2f}")
    P(f"  M2 log peak-pull ratio: median {s['M2_logs']['median']:+.3f} (16-84 {s['M2_logs']['p16']:+.3f}, {s['M2_logs']['p84']:+.3f}) -> {'pass' if s['gate_M2'] else 'FAIL'}; "
      f"phantom pulls harder in {s['frac_pull_higher']:.2f}")
    P(f"     pull-equivalent rho0 r0 (dex of Sigma_a0): phantom {s['pull_equiv_phantom']['median']:+.3f} ({s['pull_equiv_phantom']['p16']:+.3f}, {s['pull_equiv_phantom']['p84']:+.3f}); "
      f"X38 within data {s['pull_equiv_x38']['median']:+.3f} (floor = 0 when its peak is inside the data)")
    P(f"  M3 shape rms: median {s['M3_shape']['median']:.3f} (16-84 {s['M3_shape']['p16']:.3f}, {s['M3_shape']['p84']:.3f}) -> {'pass' if s['gate_M3'] else 'FAIL'}")
    P(f"  reported: outer density slope phantom {s['slope_phantom']['median']:+.2f} vs X38 {s['slope_x38']['median']:+.2f}; R_last/r0 median {s['Rlast_over_r0']['median']:.2f}; "
      f"free Burkert fit to the phantom rho0 r0 {s['burkert_fit_rho0r0_dex']['median']:+.3f} dex of Sigma_a0 ({s['burkert_fit_rho0r0_dex']['p16']:+.3f}, {s['burkert_fit_rho0r0_dex']['p84']:+.3f}; {s['burkert_fit_at_bound']} at bounds)")
    P(f"  reported: disc-centre column Sigma_M S(y_s)/((pi/2) Sigma_a0) median {s['disc_col_over_floor_col']['median']:.3f} ({s['disc_col_over_floor_col']['p16']:.3f}, {s['disc_col_over_floor_col']['p84']:.3f}); "
      f"above the floor column in {s['frac_col_gt_floor']:.2f}; Spearman(log s, log Sigma_b0) {s['spearman_logs_logSb0']:+.2f}")
    P(f"  variants: bg B M1/M2/M3 {sB['M1_logq']['median']:+.3f} / {sB['M2_logs']['median']:+.3f} / {sB['M3_shape']['median']:.3f}; "
      f"X38's own Upsilon {sU['M1_logq']['median']:+.3f} / {sU['M2_logs']['median']:+.3f} / {sU['M3_shape']['median']:.3f}")
    P(f"  VERDICT [{f}]: {v}")
P(f"  [{time.time() - T0:.0f} s]")

# reported: X47's free per-galaxy Sigma fit, recomputed, against the phantom's pull-equivalent Sigma
P("\n=== reported: X47 free-Sigma fit (Upsilon free, bg A) vs phantom pull-equivalent Sigma")
LG = np.round(np.arange(-1.5, 1.5001, 0.02), 2)
for f in (() if MUTATE else FEET):
    bg = BGS["A_c2b_refit"]; free = []
    for gi, q in enumerate(GALS):
        M200 = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)) * MSUN; R200 = (3 * M200 / (4 * math.pi * 200 * rho_c(bg["h"]))) ** (1 / 3)
        best = None
        for lg in LG:
            Sg = SIG[f] * 10 ** lg; r0 = solve_r0(M200, R200, Sg)
            w, ws, _ = fit_one(q, np.log10(np.maximum(q["GB"] + g_burk(q["Rm"], Sg, r0)[:, None], 1e-300)))
            v_ = w / max(ws, 1e-300)
            if best is None or v_ < best[1]: best = (lg, v_)
        free.append(best[0])
    free = np.array(free); con = (free > LG[0]) & (free < LG[-1])
    rows = per_galaxy(f); pe = {x["name"]: x["pull_equiv"] for x in rows if not x["zero"]}
    nm = [q["name"] for q in GALS]; a = np.array([free[i] for i in range(len(GALS)) if con[i] and nm[i] in pe]); b = np.array([pe[nm[i]] for i in range(len(GALS)) if con[i] and nm[i] in pe])
    rho = spearman(a, b)
    SP[f]["x47_free_fit"] = dict(N_constrained=int(con.sum()), median=float(np.median(free[con])), spearman_vs_phantom_pull_equiv=rho,
                                 median_phantom_minus_free=float(np.median(b - a)))
    P(f"  [{f}] free fit: constrained {int(con.sum())}/{len(GALS)}, median {np.median(free[con]):+.3f} dex (X47: canonical +0.070, alt -0.020); "
      f"Spearman(free, phantom pull-equiv) {rho:+.2f}; median phantom - free {np.median(b - a):+.3f} dex")
RES["sparc"] = SP
P(f"  [{time.time() - T0:.0f} s]")

# ===================================================================== DWARFS (X49's data path, phantom isolated)
P("\n=== Dwarfs: phantom (isolated, upper bound) vs X49 floor halos")
MSUN49, PC49 = 1.98847e30, 3.0856775814913673e16
a_, b_ = BGS["A_c2b_refit"]["a"], BGS["A_c2b_refit"]["b"]
RHOC = 3 * (100 * BGS["A_c2b_refit"]["h"] * 1e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * G)   # A1: X49's own Mpc constant
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
X49J = json.load(open(os.path.join(REB, "X49_dwarfs_route_e_floor", "x49_dwarfs_results.json")))
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
k49 = []
for f in FEET:
    Sg = A0[f] / (2 * math.pi * G); R = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        bb = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * bb; r12 = 4 / 3 * float(r["rh_pc"]) * PC49; Mb = 10 ** float(r["logMstar"])
        gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G * (Mb / 2) * MSUN49 / r12 ** 2
        M200 = 10 ** (a_ + b_ * (math.log10(Mb) - 10)) * MSUN49; R200 = (3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
        r0 = solve_r0(M200, R200, Sg); Mh = math.pi * Sg * r0 ** 2 * float(B(min(r12, R200) / r0))
        nm1 = float(nu(np.array(gN / A0[f]))) - 1.0
        R.append(dict(cls=r["cls"], E_floor=math.log10(gobs / (gN + G * Mh / r12 ** 2)), E_ph=math.log10(gobs / ((1 + nm1) * gN)),
                      ratio=(nm1 * Mb / 2 * MSUN49) / Mh if Mh > 0 else np.inf, s=float(r["sdMC[Newton]"]), y=gN / A0[f]))
    rng = np.random.default_rng(20261026); FL = {}
    for c in CLS:
        q = [x for x in R if x["cls"] == c]; m, sd = boot(np.array([x["E_floor"] for x in q]), np.array([x["s"] for x in q]), rng); FL[c] = (m, m / sd)
    rep = all(abs(FL[c][0] - X49J["footings"][f]["classes"][c]["median"]) < 1e-9 and abs(FL[c][1] - X49J["footings"][f]["classes"][c]["Z"]) < 1e-9 for c in CLS)
    k49.append(rep)
    rng = np.random.default_rng(20261026); D = {}
    for c in CLS:
        q = [x for x in R if x["cls"] == c]; E = np.array([x["E_ph"] for x in q]); s = np.array([x["s"] for x in q]); m, sd = boot(E, s, rng)
        D[c] = dict(N=len(q), E_ph=m, sd=sd, Z_ph=m / sd, E_floor=FL[c][0], Z_floor=FL[c][1], mass_ratio_ph_over_floor=float(np.median([x["ratio"] for x in q])),
                    median_y=float(np.median([x["y"] for x in q])))
        P(f"  [{f}] {c:15s} N {len(q):2d}: phantom E {m:+.3f} (Z {m / sd:+.2f}) | floor E {FL[c][0]:+.3f} (Z {FL[c][1]:+.2f}) | M_ph/M_floor(<r12) {D[c]['mass_ratio_ph_over_floor']:.2f}; median g_N/a0 {D[c]['median_y']:.3f}")
    u = D["MW ultra-faint"]
    ans = ("PHANTOM NOT HEAVIER" if u["mass_ratio_ph_over_floor"] <= 1 else "PHANTOM HEAVIER AND FITS" if abs(u["Z_ph"]) < 2 else "PHANTOM HEAVIER, STILL SHORT")
    RES["dwarfs"][f] = dict(classes=D, UFD_answer=ans, x49_reproduced=rep); P(f"  [{f}] UFD answer: {ans}; X49 medians and Z reproduced: {rep}")
RES["dwarfs"]["x49_reproduced_both"] = all(k49)

# ===================================================================== CLUSTERS (reported)
P("\n=== Clusters (reported only)")
X40 = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))
X43 = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
B1 = float(B(1.0)); ETA = 4.0 / (3.0 * B1) * 4.0 ** 1.25
for f in FEET:
    d = X40["footings"][f]["A"]["reported"]["gb_r0_diag"]; cl = {}
    for tt in ("T1", "T2", "T3"):
        yb = d[tt]["gb_over_a0"]; cl[tt] = dict(gb_over_a0=yb, phantom_pull_equiv_Sigma_a0=float(Qf(yb)) / C_B)
    need = {m: ETA * X43["sigma_coll_table"][m][0] / X43["Sigma_Msun_pc2"][f] for m in ("1e14", "1e15")}
    RES["clusters"][f] = dict(terciles=cl, eta=ETA, required_core_Sigma_a0=need)
    P(f"  [{f}] phantom pull-equiv at X40b cluster-core g_b: " + ", ".join(f"{k} (g_b/a0 {v['gb_over_a0']:.3f}) {v['phantom_pull_equiv_Sigma_a0']:.2f}" for k, v in cl.items())
      + f" Sigma_a0; X43 required core eta Sigma_coll (eta {ETA:.2f}): 1e14 {need['1e14']:.2f}, 1e15 {need['1e15']:.2f} Sigma_a0")

# ===================================================================== VERDICT + CHECKS
check("K4", rss() < 1.0, f"peak RSS {rss():.2f} GB")
allok = all(ok for _, ok in checks)
if not STEP0:
    V = "UNDECIDED (step 0)"
elif not allok:
    V = "UNDECIDED (checks)"
elif SP["canonical"]["verdict"] != SP["alt"]["verdict"]:
    V = f"UNDECIDED (footings disagree: {SP['canonical']['verdict']} / {SP['alt']['verdict']})"
else:
    V = SP["canonical"]["verdict"]
RES["verdict"] = V; RES["verdict_per_footing"] = {f: SP[f]["verdict"] for f in FEET}
P(f"\n=== VERDICT (both footings): {V}")
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
open(os.path.join(HERE, f"x50_phantom_floor{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(RES), open(os.path.join(HERE, f"x50_phantom_floor_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if (n == len(checks) and STEP0) else 1)
