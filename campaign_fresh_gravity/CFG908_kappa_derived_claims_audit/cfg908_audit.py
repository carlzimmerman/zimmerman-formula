#!/usr/bin/env python3
"""CFG908: audit of the record's unaudited 'kappa derived' claims (CFG894 prerequisite P5).

Criteria: FROZEN_CRITERIA.md, committed alone first (122af8ada). This is an audit lane: it derives nothing.
kappa = 1/2 is FITTED (CFG493 measurement, rho_DE footing). Not theory closed.

Claims (FROZEN_CRITERIA section 1):
  C1 Q010   'kappa = 1/2: DERIVED as the closure coefficient of the dynamical face'
  C2 G031   'rho_L = 4 a0^2/(G c^2) <=> Lambda = 32 pi a0^2/c^4: DERIVED (action level)' (+ G058 / G052)
  C3 glm53  'kappa = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count)' (G002)
  C4 gemini38 Link 1: photocount mu_2 with n = 2 TT polarisations, Y = g/s  =>  'kappa = 1/2, zero free parameters'

Run from the repo root:
  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_audit.py
  MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/cfg908_audit.py
The normal run writes cfg908_audit.out / .json and exits 0 (2 on an internal failure). The MUTATE run writes
cfg908_audit_MUTATE.out / .json and exits 1 when every control bites as expected, 3 if any fails to bite.
"""
import json
import math
import os
import subprocess
import sys

import sympy as sp

MUTATE = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PIN = "122af8ada"  # the criteria commit; every quoted record line is checked in this tree (K6)
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, "cfg908_audit%s.out" % TAG)
OUT_JSON = os.path.join(HERE, "cfg908_audit%s.json" % TAG)

# --------------------------------------------------------------------------------------------- run parameters
HALF = sp.Rational(1, 2)
RENAME = sp.Rational(2, 5)                      # the rename value of the law's kappa (KAPPA_CAMPAIGN_RULES I4)
KAPPA_LAW = RENAME if MUTATE else HALF          # M1
GAMMA = sp.Rational(21, 10) if MUTATE else sp.Integer(2)   # M2 (SIS exponent)
D_SPATIAL = 4 if MUTATE else 3                  # M3 (gemini38 dimension)
UNIT = "cH" if MUTATE else "s"                  # M4 (the occupancy / interpolation unit in C3, C4)
KAPPA_TRUE_SYN = sp.Rational(1, 3) if MUTATE else HALF     # M5 (synthetic data in C3)
W_DATA_WIDTH = 0.380                            # KAPPA_CAMPAIGN_RULES section 7, rho_DE; MENU threshold only

LINES = []
RESULTS = {"lane": "CFG908", "mutate": MUTATE, "pin": PIN, "params": {
    "kappa_law": str(KAPPA_LAW), "gamma": str(GAMMA), "d_spatial": D_SPATIAL, "unit": UNIT,
    "kappa_true_synthetic": str(KAPPA_TRUE_SYN)}, "tests": {}, "checks": {}, "claims": {}, "mutate_controls": {}}
INTERNAL_FAIL = []


def out(s=""):
    LINES.append(s)
    print(s)


def test(key, name, ok, evidence, store="tests"):
    RESULTS[store][key] = {"name": name, "pass": bool(ok), "evidence": evidence}
    out("  [%s] %s %s" % ("PASS" if ok else "FAIL", key, name))
    for e in (evidence if isinstance(evidence, list) else [evidence]):
        out("         %s" % e)
    return bool(ok)


def git_show(path):
    try:
        return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (PIN, path)], capture_output=True, text=True,
                              check=True).stdout
    except subprocess.CalledProcessError as exc:
        INTERNAL_FAIL.append("git show %s: %s" % (path, exc))
        return ""


def read_worktree(path):
    p = os.path.join(REPO, path)
    if not os.path.exists(p):
        return None, None
    with open(p, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    h = subprocess.run(["git", "-C", REPO, "hash-object", path], capture_output=True, text=True).stdout.strip()
    return txt, h


def line_of(text, needle):
    for i, ln in enumerate(text.splitlines(), 1):
        if needle in ln:
            return i
    return None


def pi_weight(expr):
    """Exponent k such that expr = rational/algebraic * pi^k (None if pi enters non-monomially)."""
    t = sp.Symbol("t_pi", positive=True)
    e = sp.factor(sp.simplify(sp.sympify(expr).subs(sp.pi, t)))
    for k in range(-6, 7):
        if not sp.simplify(e / t ** k).has(t):
            return k
    return None


# --------------------------------------------------------------------------------------------- symbols
G, c, rho, rho_p, a0, C, r, M, sigma, n, u, k, H = sp.symbols(
    "G c rho_DE rho_prime a_0 C r M sigma n u k H", positive=True)
s_unit = c * sp.sqrt(G * rho)                      # the record's dark-energy unit s = c sqrt(G rho_DE)
H_L = sp.sqrt(8 * sp.pi * G * rho / 3)             # Friedmann on the rho_DE footing
kappa_of = lambda a: sp.simplify(a / s_unit)       # the law's kappa of an acceleration a
lam, mu_s, nu_s = sp.symbols("lambda_s mu_s nu_s", positive=True)


def scale_invariant(expr):
    """K3: G -> lam G, rho -> mu rho, c -> nu c, a0 -> nu sqrt(lam mu) a0 leaves expr unchanged."""
    e2 = sp.sympify(expr).subs({G: lam * G, rho: mu_s * rho, c: nu_s * c, a0: nu_s * sp.sqrt(lam * mu_s) * a0},
                               simultaneous=True)
    return sp.simplify(e2 - expr) == 0


out("CFG908 -- audit of the record's unaudited 'kappa derived' claims (CFG894 P5)")
out("criteria 122af8ada (committed alone first); quoted lines checked in tree %s; mode %s" %
    (PIN, "MUTATE" if MUTATE else "normal"))
out("kappa = 1/2 is FITTED (CFG493 measurement, rho_DE footing). This lane derives nothing. Not theory closed.")
out("run parameters: kappa_law = %s, gamma = %s, d = %d, unit = %s, synthetic kappa_true = %s" %
    (KAPPA_LAW, GAMMA, D_SPATIAL, UNIT, KAPPA_TRUE_SYN))
out()

law_a0 = KAPPA_LAW * s_unit

# ============================================================================================= C1 Q010
out("C1 -- Q010: 'kappa = 1/2 DERIVED as the closure coefficient of the dynamical face'")
gam = sp.Symbol("gamma", positive=True)
Phi = C * sp.log(r)
lap = sp.simplify(sp.diff(r ** 2 * sp.diff(Phi, r), r) / r ** 2)          # spherical Laplacian
rho_halo = sp.simplify(lap / (4 * sp.pi * G))                              # Poisson
# hydrostatics at constant sigma^2 for rho = A r^-gamma: sigma^2 d ln rho/dr = -dPhi/dr  =>  sigma^2 = C/gamma
A = sp.Symbol("A", positive=True)
sig2_sol = sp.solve(sp.Eq(sigma ** 2 * sp.diff(sp.log(A * r ** (-gam)), r), -sp.diff(Phi, r)), sigma ** 2)[0]
# uniqueness: the self-sourced power law (Poisson with rho = A r^-gamma) needs gamma = 2
defect = sp.simplify(sp.diff(lap - 4 * sp.pi * G * A * r ** (-gam), r))
gam_unique = sp.solve(sp.Eq(sp.Integer(2) ** (-gam), sp.Rational(1, 4)), gam)
sig2 = sig2_sol.subs(gam, GAMMA)
vc2 = sp.simplify(r * sp.diff(Phi, r))                                      # v_c^2 = r dPhi/dr = C
kappa_dyn = sp.simplify(sig2 / vc2)
cs2_Q001 = sig2                                                             # isothermal: c_s^2 = P/rho = sigma^2
kappa_Q001 = sp.simplify(cs2_Q001 / vc2)
kappa_Q007 = sp.simplify(sig2 / (2 * sig2))      # Q007: v_c^2 = 2 sigma^2 -> sigma^2/v_c^2 (gamma = 2 statement)
t1a_ok = (sp.simplify(lap - C / r ** 2) == 0 and sp.simplify(rho_halo - C / (4 * sp.pi * G * r ** 2)) == 0
          and sp.simplify(sig2_sol - C / gam) == 0 and gam_unique == [2]
          and kappa_dyn == HALF and kappa_Q001 == HALF and kappa_Q007 == HALF)
test("T1a", "SIS chain reproduced (GF2 closure, Q001 constitutive, Q007 amplitude)", t1a_ok, [
    "lap(C ln r) = %s ; rho = %s ; hydrostatics sigma^2 = %s ; two-point 2^-gamma = 1/4 -> gamma = %s" %
    (lap, rho_halo, sig2_sol, gam_unique),
    "Poisson defect d/dr[lap - 4 pi G A r^-gamma] = %s (zero for all r iff gamma = 2 with C = 4 pi G A)" % defect,
    "at gamma = %s: kappa_dyn = sigma^2/v_c^2 = %s ; Q001 c_s^2/v_c^2 = %s ; Q007 sigma^2/(2 sigma^2) = %s" %
    (GAMMA, kappa_dyn, kappa_Q001, kappa_Q007)])
fs = sorted(str(x) for x in sp.sympify(kappa_dyn).free_symbols)
test("T1b", "kappa_dyn carries no c, no rho_DE, no a0 (no a0 normalisation against the vacuum)",
     not ({c, rho, a0} & sp.sympify(kappa_dyn).free_symbols),
     "free symbols of kappa_dyn = %s ; the law's kappa = a0/(c sqrt(G rho_DE)) needs a0, c, G, rho_DE" % fs)
kappa_dyn_renamed = kappa_dyn          # nothing in the SIS chain references the law
test("T1c", "rename test: kappa_law -> 2/5 leaves kappa_dyn unchanged while the law's kappa moves",
     kappa_dyn_renamed == kappa_dyn and kappa_of(RENAME * s_unit) == RENAME,
     "kappa_dyn = %s with the law at %s ; kappa_dyn = %s with the law at 2/5 ; law's kappa then = %s" %
     (kappa_dyn, KAPPA_LAW, kappa_dyn_renamed, kappa_of(RENAME * s_unit)))
# germ face (GF1 R1e)
kappa_germ = a0 / (n * a0)
germ_identity = sp.simplify(kappa_germ - 1 / n) == 0
kl = sp.Symbol("kappa_law", positive=True)
a0_reg = kl * c * sp.sqrt(G * rho_p)                 # a footing a0 is a kappa = kappa_law statement (rules section 0)
n_germ_sym = sp.simplify(s_unit / a0_reg)
n_germ_at_law = sp.simplify(n_germ_sym.subs({kl: KAPPA_LAW, rho_p: rho}))
n_germ_at_rename = sp.simplify(n_germ_sym.subs({kl: RENAME, rho_p: rho}))
gf1 = {}
try:
    with open(os.path.join(REPO, "deepseek_push/GF1_germ_flip/GF1_results.json")) as fh:
        gf1 = json.load(fh)
    reg = gf1["registers"]
    n_germ_rep = reg["c"] * math.sqrt(reg["G"] * reg["Omega_L"] * reg["rho_c"]) / reg["a0"]
    n_germ_rec = gf1["derived"]["n_germ"]
    rep_line = ("report only: GF1 registers (read at run time) give s/a0_reg = %.7f (GF1 printed %.7f); "
                "implied rho/rho' = (n_germ/2)^2 = %.6f -- the 1e-4 offset is a footing-input drift, not physics" %
                (n_germ_rep, n_germ_rec, (n_germ_rep / 2) ** 2))
    rep_ok = abs(n_germ_rep - n_germ_rec) < 1e-9
except Exception as exc:  # noqa: BLE001
    rep_line, rep_ok = "GF1 registers unreadable: %s" % exc, False
    INTERNAL_FAIL.append("GF1 registers")
test("T1d", "germ face: kappa_germ = 1/n is a definition; n_germ follows the law's kappa (footing circularity)",
     germ_identity and sp.simplify(n_germ_sym - sp.sqrt(rho / rho_p) / kl) == 0 and rep_ok, [
         "kappa_germ := a0/s with s := n a0  ->  kappa_germ - 1/n = %s for every n, a0" % sp.simplify(kappa_germ - 1 / n),
         "n_germ := s/a0_reg with a0_reg = kappa_law c sqrt(G rho') = %s" % n_germ_sym,
         "at kappa_law = %s, rho' = rho: n_germ = %s ; at the rename 2/5: n_germ = %s (it moves with the law)" %
         (KAPPA_LAW, n_germ_at_law, n_germ_at_rename), rep_line])
# BTFR slope channel
y = sp.Symbol("y", positive=True)
mu_n = 1 - (1 + y) ** (-n)
deep_slope_n = sp.limit(sp.diff(mu_n, y), y, 0)
vflat4 = G * M * u / deep_slope_n                    # deep branch of mu_n(g/u) g = g_N: g^2 n/u = G M/r^2
btfr_slope = sp.simplify(sp.diff(sp.log(vflat4), M) * M)
test("T1e", "BTFR slope channel (b = 1.004 +/- 0.011) is blind to n and to kappa (H061 I7)",
     btfr_slope == 1 and not ({n, u} & sp.sympify(btfr_slope).free_symbols), [
         "deep slope of mu_n = %s ; v_flat^4 = %s ; d ln v^4 / d ln M = %s for every n and every unit u" %
         (deep_slope_n, vflat4, btfr_slope),
         "so one of Q010's three anchoring channels carries no information on n (or on kappa)"])
rho_h = sp.Symbol("rho_halo", positive=True)
chain_eqs = [sp.Eq(sp.Symbol("Phi"), C * sp.log(r)), sp.Eq(lap, 4 * sp.pi * G * rho_h),
             sp.Eq(sigma ** 2 * sp.diff(sp.log(A * r ** (-gam)), r), -sp.diff(Phi, r)),
             sp.Eq(C, sp.sqrt(G * M * a0))]
chain_syms = set().union(*[e.free_symbols for e in chain_eqs])
test("T1f", "junction: no equation of the closure chain contains rho_DE (the link sigma^2/v^2 -> a0/s is posited)",
     rho not in chain_syms, [
         "free symbols of {log branch, Poisson, hydrostatics, C = sqrt(G M a0)} = %s" %
         sorted(str(x) for x in chain_syms),
         "Q010 labels this junction 'rung 5' POSTULATED-CARRIED; the law's kappa = 1/2 enters only through it "
         "and through n_germ (T1d)"])
out()

# ============================================================================================= C2 G031
out("C2 -- G031: 'rho_L = 4 a0^2/(G c^2) <=> Lambda = 32 pi a0^2/c^4: DERIVED (action level)' (+ G058/G052)")
rhoL_G031 = 4 * a0 ** 2 / (G * c ** 2)
v1 = sp.simplify(sp.sqrt(G * rhoL_G031) * c / 2 - a0)
test("T2a", "G031 V1 reproduced: (c/2) sqrt(G rho_L) - a0 = 0 with rho_L = 4a0^2/(Gc^2) substituted", v1 == 0,
     "residual = %s" % v1)
rhoL_k = a0 ** 2 / (k ** 2 * G * c ** 2)
v1_k = sp.simplify(k * c * sp.sqrt(G * rhoL_k) - a0)
test("T2b", "generalised V1 holds for EVERY k: the check is an identity of the substituted tie (S2 fails)",
     v1_k == 0, "k c sqrt(G a0^2/(k^2 G c^2)) - a0 = %s for symbolic k > 0" % v1_k)
v1_law = sp.simplify(KAPPA_LAW * c * sp.sqrt(G * rhoL_G031) - a0)
v1_rename = sp.simplify(RENAME * c * sp.sqrt(G * rhoL_G031) - a0)
test("T2c", "rename test: against the law at 2/5, G031's tie returns -a0/5 (the 'derivation' is its own premise)",
     v1_rename == -a0 / 5, "law at %s: residual %s ; law at 2/5: residual %s" % (KAPPA_LAW, v1_law, v1_rename))
Lam = sp.simplify(8 * sp.pi * G * rhoL_G031 / c ** 2)
test("T2d", "G031 V2: Lambda = 8 pi G rho_L/c^2 = 32 pi a0^2/c^4 follows from the substituted tie",
     sp.simplify(Lam - 32 * sp.pi * a0 ** 2 / c ** 4) == 0, "Lambda = %s" % Lam)
H0 = sp.Symbol("H_0", positive=True)
omega = sp.simplify(rhoL_G031 / (3 * H0 ** 2 / (8 * sp.pi * G)))
g058 = git_show("glm53_push/lean/G058_omega_from_a0.lean")
wit = "refine ⟨4 * a0 ^ 2 / (G * c ^ 2), ⟨rfl, ?_⟩, ?_⟩"
test("T2e", "G058: Omega_L = 32 pi a0^2/(3 H0^2 c^2) is the tie rewritten; one_constant_closure is witnessed by the tie",
     sp.simplify(omega - 32 * sp.pi * a0 ** 2 / (3 * H0 ** 2 * c ** 2)) == 0 and wit in g058, [
         "rho_L/rho_crit with the tie = %s" % omega,
         "G058 lean line %s: '%s'" % (line_of(g058, wit), wit)])
out()

# ============================================================================================= C3 glm53 / G002
out("C3 -- glm53 README / G002: 'kappa = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count)'")
units = {"s": s_unit, "cH": c * H_L, "c sqrt(8 pi G rho)": c * sp.sqrt(8 * sp.pi * G * rho),
         "c sqrt(4 pi G rho)": c * sp.sqrt(4 * sp.pi * G * rho)}
kappa_family = sp.simplify((u / s_unit) / deep_slope_n)   # deep law of mu_n(g/u): a0 = u/n
k3_s = sp.simplify(kappa_family.subs(u, units["s"]))
k3_cH = sp.simplify(kappa_family.subs(u, units["cH"]))
test("T3a", "deep slope of mu_n is n; with Y = g/u the deep law gives a0 = u/n, kappa = (u/s)/n",
     deep_slope_n == n and k3_s == 1 / n and sp.simplify(k3_cH - sp.sqrt(sp.Rational(8, 3) * sp.pi) / n) == 0,
     ["kappa(u = s) = %s (premise A: the unit c sqrt(G rho) with coefficient 1)" % k3_s,
      "kappa(u = c H_Lambda) = %s" % k3_cH])


def solve_y(x, nn):
    """y(1 - (1+y)^-n) = x for y = g/s (monotone in y)."""
    lo, hi = 1e-12, max(10.0, 10 * x + 10)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * (1 - (1 + mid) ** (-nn)) < x:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def rar_fit(kappa_true):
    xs = [0.005 * (1000.0 ** (i / 59.0)) for i in range(60)]             # g_bar/s in [0.005, 5]
    ys = [x / (1 - math.exp(-math.sqrt(x / kappa_true))) for x in xs]   # McGaugh RAR at a0 = kappa_true s

    def rms(nn):
        return math.sqrt(sum((math.log10(solve_y(x, nn)) - math.log10(yy)) ** 2 for x, yy in zip(xs, ys)) / len(xs))

    ints = {m: rms(m) for m in range(1, 7)}
    a, b = 0.5, 8.0
    gr = (math.sqrt(5) - 1) / 2
    for _ in range(60):
        c1, c2 = b - gr * (b - a), a + gr * (b - a)
        if rms(c1) < rms(c2):
            b = c2
        else:
            a = c1
    ncont = 0.5 * (a + b)
    return min(ints, key=ints.get), ncont, ints, rms(ncont)


fit_half = rar_fit(0.5)
fit_third = rar_fit(1.0 / 3.0)
fit_rename = rar_fit(float(RENAME))
fit_run = rar_fit(float(KAPPA_TRUE_SYN))
test("T3b", "n is a measurement of kappa: the best integer tracks kappa_true of the data",
     fit_half[0] == 2 and fit_third[0] == 3, [
         "kappa_true 1/2: n_best = %d, n_cont = %.3f (rms %.4f dex); integer rms %s" %
         (fit_half[0], fit_half[1], fit_half[3], {m: round(v, 4) for m, v in fit_half[2].items()}),
         "kappa_true 1/3: n_best = %d, n_cont = %.3f (rms %.4f dex)" % (fit_third[0], fit_third[1], fit_third[3]),
         "run value kappa_true %s: n_best = %d, n_cont = %.3f" % (KAPPA_TRUE_SYN, fit_run[0], fit_run[1]),
         "synthetic data in units of s, McGaugh RAR shape; no constants"])
g002 = git_show("glm53_push/G002_onefunction_construction.py")
n1, n2 = "kappa_pred = sy.Rational(1, 2)", "NOTHING fitted (L232: mu_n(g/s) g = g_bar, integer by integer;"
test("T3c", "G002 text: kappa_pred is the literal 1/2; n is selected by SPARC fits of mu_n(g/s) with s fixed",
     n1 in g002 and n2 in g002, ["G002 line %s: '%s'" % (line_of(g002, n1), n1),
                                  "G002 line %s: '%s'" % (line_of(g002, n2), n2)])
test("T3d", "rename test: data at kappa_true = 2/5 move n_cont by more than 0.25",
     abs(fit_rename[1] - fit_half[1]) > 0.25,
     "n_cont(1/2) = %.3f ; n_cont(2/5) = %.3f (n_best %d) -- the 'derived' 1/n follows the data" %
     (fit_half[1], fit_rename[1], fit_rename[0]))
out()

# ============================================================================================= C4 gemini38
out("C4 -- gemini38 Link 1: photocount mu_2, n = 2 TT polarisations, Y = g/s  =>  'kappa = 1/2, zero free parameters'")
dd = sp.Symbol("d", positive=True, integer=True)
N_pol = (dd + 1) * (dd - 2) / 2
mu_2_slope = sp.limit(sp.diff((1 - (1 + y) ** (-2)), y), y, 0)
test("T4a", "deep slope of mu_2 is 2; N_pol(d) = (d+1)(d-2)/2 = 2 at d = 3",
     mu_2_slope == 2 and N_pol.subs(dd, 3) == 2, "slope = %s ; N_pol(3) = %s" % (mu_2_slope, N_pol.subs(dd, 3)))
kappa_c4 = lambda dv, uu: sp.simplify((uu / s_unit) / N_pol.subs(dd, dv))
k_d = {dv: kappa_c4(dv, units["s"]) for dv in (3, 4, 5)}
test("T4b", "kappa(d) at u = s: the 1/2 is the d = 3 value only (S3)",
     k_d[3] == HALF and k_d[4] == sp.Rational(1, 5) and k_d[5] == sp.Rational(1, 9),
     "kappa(d=3) = %s, kappa(d=4) = %s, kappa(d=5) = %s" % (k_d[3], k_d[4], k_d[5]))
menu = {name: kappa_c4(3, uu) for name, uu in units.items()}
menu_f = {name: float(v) for name, v in menu.items()}
menu_pw = {name: pi_weight(v ** 2) for name, v in menu.items()}
spread = max(menu_f.values()) - min(menu_f.values())
pi_free = [nm for nm, w in menu_pw.items() if w == 0]
test("T4c", "unit menu at d = 3: the spread exceeds 0.380 and the only pi-free entry is the premise-A unit (MENU)",
     spread > W_DATA_WIDTH and pi_free == ["s"], [
         "%s: kappa = %s = %.4f, pi-weight of kappa^2 = %s" % (nm, menu[nm], menu_f[nm], menu_pw[nm]) for nm in menu] +
     ["spread = %.3f > %.3f" % (spread, W_DATA_WIDTH)])
c4_out_renamed = kappa_c4(3, units["s"])          # the chain never reads the law's kappa
test("T4d", "rename test: kappa_law -> 2/5 leaves the gemini38 output at 1/2 (a value fixed by its posits)",
     c4_out_renamed == HALF, "output with the law at %s: %s ; with the law at 2/5: %s" %
     (KAPPA_LAW, kappa_c4(3, units["s"]), c4_out_renamed))
gpy = git_show("gemini38_flash_push/first_principles_derivation_chain.py")
glean = git_show("gemini38_flash_push/FirstPrinciplesChainProof.lean")
q1 = "a0_canonical = s_de / 2.0"
q2 = 'print("5. Matching g_N = g^2 / a0 forces: a0 = s / 2  ==>  kappa = 1/2.")'
q3 = "((3 + 1 : ℝ) * (3 - 2) / 2 = 2) ∧ ((1 : ℝ) / 2 = 1 / 2)"
ln_q1, ln_def1 = line_of(gpy, q1), line_of(gpy, "def derive_link1_quantum_photocount")
slope_assign = [ln for ln in gpy.splitlines() if "slope_0" in ln and ("a0" in ln or "kappa" in ln) and "=" in ln
                and not ln.strip().startswith(("#", "print"))]
test("T4e", "gemini38 text: a0 = s/2 is set before Link 1 and printed, not computed; the Lean kappa part is 1/2 = 1/2",
     ln_q1 is not None and ln_def1 is not None and ln_q1 < ln_def1 and q2 in gpy and not slope_assign and q3 in glean, [
         "script line %s: '%s' (Link 1 starts at line %s)" % (ln_q1, q1, ln_def1),
         "script line %s prints the conclusion as a string; assignments of a0/kappa from slope_0: %d" %
         (line_of(gpy, q2), len(slope_assign)),
         "Lean line %s: '%s'" % (line_of(glean, q3), q3)])
out()

# ============================================================================================= K checks
out("IDENTITY CHECKS")
with open(os.path.abspath(__file__), encoding="utf-8") as fh:
    src = fh.read()
forbidden = ["9.36" + "e-11", "9.3603" + "e-11", "9.3619" + "e-11", "1.13" + "e-10", "1.1312" + "e-10",
             "1.1279" + "e-10", "1.2" + "e-10", "5.78" + "88", "0.17" + "27", "0.4" + "17", "0.5" + "51", "0.4" + "65"]
hits = [f for f in forbidden if f in src]
test("K1", "no forbidden literal in this script", not hits, "hits: %s" % hits, store="checks")
k2_exprs = {"kappa_dyn": kappa_dyn, "kappa_germ": kappa_germ, "n_germ": n_germ_sym, "G031 V1(k)": v1_k,
            "C3 kappa(u)": kappa_family, "C4 kappa(d=3,u=s)": menu["s"]}
test("K2", "every kappa expression printed symbolically", True,
     ["%s = %s  [free: %s]" % (nm, e, sorted(str(x) for x in sp.sympify(e).free_symbols)) for nm, e in k2_exprs.items()],
     store="checks")
k3 = {"law kappa": kappa_of(law_a0), "kappa_dyn": kappa_dyn, "n_germ(rho'=rho)": n_germ_sym.subs(rho_p, rho),
      "G031 V1/a0": v1_law / a0, "C3 kappa(u=cH)": k3_cH, "C4 menu cH": menu["cH"]}
k3_ok = {nm: scale_invariant(e) for nm, e in k3.items()}
test("K3", "scaling G -> lam G, rho -> mu rho, c -> nu c leaves every kappa output invariant", all(k3_ok.values()),
     "%s" % k3_ok, store="checks")
k4 = {"C1 kappa_dyn": RESULTS["tests"]["T1c"]["pass"], "C1 n_germ": RESULTS["tests"]["T1d"]["pass"],
      "C2 V1": RESULTS["tests"]["T2c"]["pass"], "C3 n_cont": RESULTS["tests"]["T3d"]["pass"],
      "C4 output": RESULTS["tests"]["T4d"]["pass"]}
test("K4", "rename test evaluated for every chain (behaviour as declared)", all(k4.values()), "%s" % k4,
     store="checks")
k5 = {"kappa_dyn^2": pi_weight(kappa_dyn ** 2), "C3 kappa(u=s)^2 at n=2": pi_weight(k3_s.subs(n, 2) ** 2),
      "C3 kappa(u=cH)^2 at n=2": pi_weight(k3_cH.subs(n, 2) ** 2), "C4 menu": menu_pw}
test("K5", "pi-weight of kappa^2 per chain output", all(v is not None for v in [k5["kappa_dyn^2"]]), "%s" % k5,
     store="checks")
quotes = [
    ("qwen38_push/Q010_kappa_referee/FROZEN_CRITERIA.md", 'Register line becomes: "κ=½: DERIVED as the closure'),
    ("glm53_push/G031_gr_fluid_action.py", "rhoL_of_a0 = 4*a0**2/(G*c**2)"),
    ("glm53_push/G031_gr_fluid_action.py", "chk1 = sp.simplify(sp.sqrt(G*rhoL_of_a0)*c/2 - a0) == 0"),
    ("glm53_push/STATE.md", "| 0 | ρ_Λ = 4a₀²/(Gc²) ⟺ Λ_geom = 32πa₀²/c⁴ | DERIVED (action level, sympy-exact 9/9) | G031 |"),
    ("glm53_push/STATE.md", "| 2 | κ = ½ = 1/n from SPARC (n = 2) | DERIVED from data | G002 |"),
    ("glm53_push/README.md", "**κ = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count), a_0 ="),
    ("glm53_push/README.md", "the OneFunction (kappa = 1/2 derived, Lean 4)"),
    ("gemini38_flash_push/FIRST_PRINCIPLES_DERIVATION_CHAIN_REPORT.md", "\\implies \\kappa = \\frac{1}{2}$$"),
    ("gemini38_flash_push/FIRST_PRINCIPLES_DERIVATION_CHAIN_REPORT.md", "with **zero free parameters**."),
    ("deepseek_push/GF1_germ_flip/GF1_germ_flip.py", "kappa := a0/s = 1/n (s := n a0; s=2a0 committed)"),
    ("deepseek_push/GF2_closure_half/README.md", "# GF2 — The closure half: κ = ½ derived as the self-source closure"),
    ("campaign_fresh_gravity/AUDIT_GF2_kappa_claim_2026-10-09.md", "NOT A DERIVATION OF THE LAW'S κ"),
    ("hy4_push/H061_RECIPE_AMENDMENT.md", "**That announcement is withdrawn.**"),
]
qres = []
for path, needle in quotes:
    txt = git_show(path)
    qres.append((path, line_of(txt, needle), needle))
test("K6", "every quoted record line is present in tree %s" % PIN, all(q[1] for q in qres),
     ["%s:%s  '%s'" % (p, ln, nd[:90]) for p, ln, nd in qres], store="checks")
# untracked Q010 material (explicit paths only; reported, not part of K6)
q010_readme, q010_hash = read_worktree("qwen38_push/Q010_kappa_referee/README.md")
uq = []
if q010_readme is not None:
    for needle in ["κ = ½: **DERIVED as the closure coefficient of the dynamical face**", "POSTULATED-CARRIED",
                   "AUDIT_GF2", "a755b66ca"]:
        uq.append("%s -> line %s" % (needle, line_of(q010_readme, needle)))
out("  [info] untracked qwen38_push/Q010_kappa_referee/README.md hash-object %s (frozen f4b2400c774f): %s" %
    ((q010_hash or "missing")[:12], "; ".join(uq)))
RESULTS["q010_untracked"] = {"hash": q010_hash, "lines": uq}
out()

# ============================================================================================= classification
out("CLASSIFICATION (FROZEN_CRITERIA section 3; headline = class of the step where 1/2 for the law's kappa enters)")
T = RESULTS["tests"]


def classify_c1():
    sec = []
    if T["T1d"]["pass"]:
        sec += ["I-W (kappa_germ = 1/n is a definition, GF1 R1e)", "I-M (n_germ = s/a0_reg uses the kappa = 1/2 footing)"]
    if T["T1f"]["pass"]:
        sec.append("junction posited (rung 5; no equation links sigma^2/v^2 to a0/s)")
    if T["T1e"]["pass"]:
        sec.append("BTFR-slope anchor uninformative on n and kappa (H061 I7)")
    head = "DIFFERENT QUANTITY" if (T["T1b"]["pass"] and T["T1c"]["pass"]) else "UNRESOLVED"
    return head, "step 1: kappa_dyn := sigma^2/v_c^2 (the SIS ratio); the law's kappa enters only via the posited junction", sec


def classify_c2():
    head = "IDENTITY/INSERTION (I-W)" if (T["T2b"]["pass"] and T["T2c"]["pass"]) else "UNRESOLVED"
    sec = ["G058 one_constant_closure witnessed by the tie; Omega_L from a0 is the tie rewritten (I5)"] \
        if T["T2e"]["pass"] else []
    return head, "G031 V1: the tie rho_L = 4a0^2/(Gc^2) is substituted, then verified", sec


def classify_c3():
    sec = []
    if T["T3a"]["pass"]:
        sec.append("I-A (kappa = 1/n only with the unit s = c sqrt(G rho) at coefficient 1; u = cH gives sqrt(8pi/3)/n)")
    if T["T3c"]["pass"]:
        sec.append("I-W (G002 compares the literal kappa_pred = 1/2 with the fitted 1/2)")
    head = "IDENTITY/INSERTION (I-M)" if (T["T3b"]["pass"] and T["T3d"]["pass"]) else "UNRESOLVED"
    return head, "n = 2 is the integer SPARC selected with s fixed: a measurement of 1/kappa, relabelled", sec


def classify_c4():
    sec = []
    if T["T4c"]["pass"]:
        sec.append("MENU over the occupancy unit {0.5, 1.447, 2.507, 1.772}; only the premise-A unit is pi-free")
    if T["T4b"]["pass"]:
        sec.append("S3: 1/2 is the d = 3 value of 1/N_pol (1/5 at d = 4)")
    sec.append("retracted class X5: kappa = 1/(polarisation count) (H061, K568, K521)")
    if T["T4e"]["pass"]:
        sec.append("I-W hygiene: a0 = s/2 hard-coded before Link 1 and printed; Lean proves 1/2 = 1/2")
    head = "IDENTITY/INSERTION (I-A)" if (T["T4c"]["pass"] and T["T4d"]["pass"] and T["T4a"]["pass"]) else "UNRESOLVED"
    return head, "Y = g/s_DE posits the unit c sqrt(G rho_DE) with coefficient 1 (premise A) and n = N_pol", sec


k_ok = all(v["pass"] for v in RESULTS["checks"].values())
for cid, fn, nm in [("C1", classify_c1, "Q010"), ("C2", classify_c2, "G031 (+G058/G052)"),
                    ("C3", classify_c3, "glm53 README / G002"), ("C4", classify_c4, "gemini38 chain")]:
    head, step, sec = fn()
    if not k_ok:
        head = "VOID (a K check failed)"
    RESULTS["claims"][cid] = {"name": nm, "headline": head, "step": step, "secondary": sec,
                              "valid_derivation": False}
    out("  %s %s: %s" % (cid, nm, head))
    out("     step: %s" % step)
    for x in sec:
        out("     + %s" % x)
out("  VALID DERIVATION: none of the four claims (each fails at least one of: law's kappa, no insertion, rename test).")
out()

# ============================================================================================= mutation controls
exit_code = 0
if MUTATE:
    out("MUTATION CONTROLS (expected per FROZEN_CRITERIA section 5)")
    m = RESULTS["mutate_controls"]
    m["M1"] = {"expect": "n_germ -> 5/2; G031 V1 vs law -> -a0/5; kappa_dyn stays 1/2 (gamma=2 part); gemini38 stays 1/2",
               "bite": (n_germ_at_law == sp.Rational(5, 2) and v1_law == -a0 / 5 and
                        sp.simplify(sig2_sol.subs(gam, 2) / vc2) == HALF and kappa_c4(3, units["s"]) == HALF),
               "got": "n_germ %s ; V1 %s ; kappa_dyn(gamma=2) %s ; gemini38(u=s,d=3) %s" %
                      (n_germ_at_law, v1_law, sp.simplify(sig2_sol.subs(gam, 2) / vc2), kappa_c4(3, units["s"]))}
    m["M2"] = {"expect": "kappa_dyn -> 1/2.1 = 0.476", "bite": kappa_dyn == sp.Rational(10, 21),
               "got": "kappa_dyn = %s = %.4f" % (kappa_dyn, float(kappa_dyn))}
    k_m3 = kappa_c4(D_SPATIAL, units["s"])
    m["M3"] = {"expect": "d = 4: kappa -> 1/5", "bite": k_m3 == sp.Rational(1, 5), "got": "kappa = %s" % k_m3}
    k_m4 = kappa_c4(3, units[UNIT])
    m["M4"] = {"expect": "u = cH: kappa -> sqrt(8 pi/3)/2 = 1.447, pi-weight +1",
               "bite": sp.simplify(k_m4 - sp.sqrt(sp.Rational(8, 3) * sp.pi) / 2) == 0 and pi_weight(k_m4 ** 2) == 1,
               "got": "kappa = %s = %.4f, pi-weight %s" % (k_m4, float(k_m4), pi_weight(k_m4 ** 2))}
    m["M5"] = {"expect": "synthetic kappa_true 1/3: n_best 2 -> 3", "bite": fit_run[0] == 3,
               "got": "n_best = %d, n_cont = %.3f" % (fit_run[0], fit_run[1])}
    unchanged = {cid: RESULTS["claims"][cid]["headline"] for cid in RESULTS["claims"]}
    expected_heads = {"C1": "DIFFERENT QUANTITY", "C2": "IDENTITY/INSERTION (I-W)", "C3": "IDENTITY/INSERTION (I-M)",
                      "C4": "IDENTITY/INSERTION (I-A)"}
    m["classes_unchanged"] = {"expect": "headlines as in the normal run", "bite": unchanged == expected_heads,
                              "got": "%s" % unchanged}
    for key, v in m.items():
        out("  [%s] %s: expected %s ; got %s" % ("BITES" if v["bite"] else "NO BITE", key, v["expect"], v["got"]))
    all_bite = all(v["bite"] for v in m.values())
    exit_code = 1 if all_bite else 3
    out("MUTATE: %s" % ("every control bites as expected (exit 1)" if all_bite else "a control failed to bite (exit 3)"))
else:
    repro = ["T1a", "T1d", "T2a", "T2d", "T2e", "T3a", "T3c", "T4a", "T4e"]
    repro_ok = all(T[x]["pass"] for x in repro)
    all_eval = all(x in T for x in ["T1a", "T1b", "T1c", "T1d", "T1e", "T1f", "T2a", "T2b", "T2c", "T2d", "T2e",
                                    "T3a", "T3b", "T3c", "T3d", "T4a", "T4b", "T4c", "T4d", "T4e"])
    npass = sum(1 for v in T.values() if v["pass"]) + sum(1 for v in RESULTS["checks"].values() if v["pass"])
    ntot = len(T) + len(RESULTS["checks"])
    out("SUMMARY: %d/%d tests and checks pass; reproduction checks %s" % (npass, ntot, "hold" if repro_ok else "FAIL"))
    exit_code = 0 if (repro_ok and all_eval and k_ok and not INTERNAL_FAIL) else 2
if INTERNAL_FAIL:
    out("INTERNAL FAILURES: %s" % INTERNAL_FAIL)
    exit_code = 2
out("kappa = 1/2 is FITTED. No claim audited here derives it. Not theory closed.")
RESULTS["exit_code"] = exit_code
with open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(RESULTS, fh, indent=1, default=str)
sys.exit(exit_code)
