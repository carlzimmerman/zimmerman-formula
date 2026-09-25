#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L345 -- THE TWO LIVE FRONTS, TESTED TOGETHER: the gravity candidate C-H/K (L340) and the Lambda-triggered dark carrier
(L319-L322).  C-H/K is UNIVERSAL by construction -- its MOND sector reads the total lapse, so any metric-coupled dark
component is boosted exactly like baryons -- and L321 found that a carrier that sources the MOND field overshoots the
X-COP clusters.  Does ANY carrier parameter survive the clusters under C-H/K's coupling?

WHY THIS IS THE QUESTION
  L321/L322 kept the carrier alive only under ADDITIVE coupling: a metric-coupled carrier whose gravity is added to the
  MOND field of the baryons without being boosted.  In a single-metric action whose MOND sector reads the lapse (C-H, and
  C-H/K on top of it: ACTION.md -- "The metric g is the sole physical metric for ordinary matter ... minimally coupled
  standard matter may replace this example without introducing U or tau couplings"), the lapse is sourced by ALL matter,
  the kernel reads its filtered gradient, and there is no channel that can tell baryons from a minimally coupled carrier.
  L321's "additive" therefore has no realisation in C-H/K; its "universal" is what C-H/K does.

WHAT THIS LANE DOES
  U0 FROM THE ACTION (L340's own unitary scalar block, symbolic): with the matter source split R = R_b + R_c, the static
     AND the moving response of every field to R_c is identical to its response to R_b: the carrier is boosted by
     (1 + C)/(1 - alpha_c (1 + C)/2), exactly like baryons.  Control: a carrier given a direct U-coupling (a non-minimal
     coupling C-H/K does not contain) is NOT boosted -- the check can fail, and that coupling is the only internal escape.
  U1 THE CLUSTER GATE UNDER C-H/K's COUPLING, on the real X-COP sample (L321's validated phase-mixing retention machinery,
     unchanged), with L340's kernel nu_mono and BOTH footings, over the carrier's whole plausible range: decayed fraction
     today f_d(0) in {0.8, 0.9, 0.95, 0.99} and kick v_k in {1000 .. 3000} km/s.  Pre-declared thresholds = L322's:
     strict |median M_dyn/M_HSE - 1| <= 0.2; alternative: the same after X-COP's measured 6% non-thermal support.
  U2 S_8 for every cell (L319's exact linear-response solver, unchanged; S_8 depends on (f_d, v_k) only, not on the
     coupling), against L322's floors: strict 0.767 (KiDS-Legacy 3 sigma), alternative 0.748 (DES-Y3 x KiDS-1000 3 sigma).
  U3 the galaxy gate (L321's hosts, shift <= 0.06 dex) at every cell that passes U1 and U2.
  VERDICT a universal window = a cell passing U1, U2 and U3 under the same threshold set.

  NOT in scope: C-H/K's cosmological growth -- computed by the parallel lane L341 (g03_audit_2026/L341_chk_frw_gate):
  with the cold fluid the CMB requires, C-H/K's unfloored kernel gives sigma_8 = 18-27, and its natural K-floor erases
  MOND in galaxies.  L319's S_8 here is computed with GR growth, so it is a NECESSARY condition only: a window found here
  could still close on growth; none found here cannot reopen there.  This lane is the complementary CLUSTER gate: can
  the carrier (whose decay would reduce the retained cold fluid) survive C-H/K's coupling at z = 0?

MUTATE=1 evaluates U1-U3 with L321's ADDITIVE coupling (the unrealisable one): L322's alternative window must reappear, and
the load-bearing "no universal window" finding must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L345_chk_universal_carrier_pincer.py
"""
import os, sys, json, math, time, warnings, io, contextlib
import numpy as np
import sympy as sp
from scipy.optimize import brentq
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L345_chk_universal_carrier_pincer"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L345", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
COUP = "additive" if MUTATE else "universal"
if MUTATE:
    P("  MUTATE: U1-U3 use L321's ADDITIVE coupling (the one C-H/K cannot realise)")

# ============================================================================================ U0 from the action
banner("U0  FROM THE ACTION: L340's unitary scalar block with the matter source split into baryons + carrier")
k, C, c2, ac, w, gU = sp.symbols('k C c_2 alpha_c omega g_U', real=True)
psi, phi, beta, U = sp.symbols('psi phi beta U')
Rb, Rc = sp.symbols('R_b R_c')
Dt = -sp.I * w; eps_ = -c2


def block(gUx, static=False):
    """L340's block (its E rows, a2 = a3 = g = 0), total source R_b + R_c in the Hamiltonian and momentum rows; gUx couples
    the carrier directly to U (NOT in C-H/K; the control).  static=True solves at omega = 0 (non-singular for c_2 != 0)."""
    R = Rb + Rc
    E = [4 * k**2 * psi - 4 * k**2 * phi - Dt * (-12 * Dt * psi + 4 * k**2 * beta + 6 * eps_ * (3 * Dt * psi - k**2 * beta)),
         -4 * k**2 * psi - 4 * k**2 * (U - phi) + 2 * ac * k**2 * phi - R,
         4 * k**2 * Dt * psi - 2 * eps_ * k**2 * (3 * Dt * psi - k**2 * beta) + Dt * R,
         4 * k**2 * (U - phi) + 4 * k**2 * C * U + gUx * Rc]
    X = [psi, phi, beta, U]
    if static:
        E = [e.subs(w, 0) for e in E]
    M = sp.Matrix([[sp.diff(e, x) for x in X] for e in E]); S = sp.Matrix([-e.subs({x: 0 for x in X}) for e in E])
    return M.LUsolve(S)


sol = block(0)
d_mov = sp.simplify(sp.diff(sol[0], Rb) - sp.diff(sol[0], Rc))
sol_st = block(0, static=True)
st = [sp.simplify(sp.diff(sol_st[0], R_) / (-1 / (4 * k**2))) for R_ in (Rb, Rc)]
solU = block(gU, static=True)
st_ctrl = sp.simplify(sp.diff(solU[0], Rc) / (-1 / (4 * k**2)))
P(f"    static boost on baryons: {sp.factor(st[0])};  on the carrier: {sp.factor(st[1])}")
P(f"    moving (omega != 0): d psi/dR_b - d psi/dR_c = {d_mov}")
P(f"    control, carrier with a direct U-coupling g_U: static boost on the carrier = {sp.factor(st_ctrl)}")
OUT["numbers"]["U0"] = dict(boost_b=str(st[0]), boost_c=str(st[1]), ctrl=str(st_ctrl))
check("U0 C-H/K IS UNIVERSAL: in L340's own block the carrier's static and moving response equals the baryons' exactly "
      "(boost (1+C)/(1 - alpha_c(1+C)/2)); only a direct U-coupling -- absent from C-H/K -- changes it",
      f"static difference {sp.simplify(st[0] - st[1])}; moving difference {d_mov}; with g_U: {sp.factor(st_ctrl)}",
      sp.simplify(st[0] - st[1]) == 0 and d_mov == 0 and sp.simplify(st_ctrl - st[1]) != 0,
      "L321's additive coupling needs the carrier to be invisible to the kernel; a minimally coupled carrier is not")

# ============================================================================================ machinery
_src = open(os.path.join(HERE, "L321_carrier_z0_retention_gate.py")).read()
_top = _src.split("# ============================================================================================ controls")[0]
_top = _top.split("P(__doc__)", 1)[1]
Lm = {"__name__": "l321", "__file__": os.path.join(HERE, "L321_carrier_z0_retention_gate.py"), "HERE": HERE,
      "MUTATE": False, "P": (lambda *a: None), "banner": (lambda t: None), "json": json, "os": os, "math": math, "np": np,
      "time": time, "T0": T0, "CH": [], "OUT": {"numbers": {}}, "check": (lambda *a, **k: True), "SLUG": "l321"}
exec("import os, sys, json, math, time\nimport numpy as np\n" + _top, Lm)
KPC_M = Lm["KPC_M"]


# L340's monotone kernel nu_mono (nu_RAR below its phantom peak, then h' = 0.05 h_p/(y + y_p)), rebuilt as in L340 A1
def h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


Lm["nu"] = nu_mono
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
retained, gal_shift, cl_ratio, CL, GAL = Lm["retained"], Lm["gal_shift"], Lm["cl_ratio"], Lm["CL"], Lm["GAL"]
hernquist, c200_dm14, GE_GAL, GE_CL = Lm["hernquist"], Lm["c200_dm14"], Lm["GE_GAL"], Lm["GE_CL"]
cl_ref = CL[int(np.argmin([abs(math.log10(cl["M200"] / 1e15)) for cl in CL]))]
cl_mass_fn = (lambda x, cl=cl_ref: cl["Mb"] * np.clip(np.asarray(x, dtype=float) / cl["R500"], 0, 1))
P(f"\n  L321 machinery loaded ({len(CL)} X-COP clusters); kernel nu_mono (y_p = {Y_P:.3f}); coupling '{COUP}'")

FDS = [0.8, 0.9, 0.95, 0.99]
VKS = [1000.0, 1500.0, 2000.0, 2500.0, 3000.0]
NT = 0.06
S8_STRICT, S8_ALT = 0.767, 0.748

# ============================================================================================ U1 clusters
banner("U1  THE X-COP GATE UNDER C-H/K's COUPLING (nu_mono, both footings), median M_dyn/M_HSE over 12 clusters")
U1 = {}
for foot, a0 in FOOT.items():
    Lm["A0"] = a0 * KPC_M / 1e6
    need = float(np.median([Lm["eps_needed"](cl, COUP) for cl in CL]))
    for fd in FDS:
        cells = []
        for vk in VKS:
            ecl, _ = retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, COUP, vk, fd, rhoc=cl_ref["rhoc"])
            med = float(np.median([cl_ratio(cl, ecl, COUP) for cl in CL]))
            cells.append(dict(vk=vk, eps=float(ecl), ratio=med, ratio_nt=med * (1 - NT)))
        U1[(foot, fd)] = cells
        P(f"    {foot:9s} f_d {fd:4.2f}: " + "  ".join(f"{c['vk']:.0f}: {c['ratio']:.2f} (eps {c['eps']:.2f})" for c in cells)
          + f"   [retention needed for M_dyn = M_HSE: {need:.2f}; {time.time() - T0:.0f}s]")
OUT["numbers"]["U1"] = {f"{f}_{fd}": v for (f, fd), v in U1.items()}

# ============================================================================================ U2 S_8
banner("U2  S_8 PER (f_d, v_k): L319's exact linear-response solver (GR growth -- a necessary condition only)")
_s19 = open(os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")).read().split(
    "# ============================================================================================ controls")[0]
G19 = {"__name__": "l319", "__file__": os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s19, G19)
    LC19 = G19["run"](np.ones(G19["N_A"]), 0.0)
S8 = {}
for fd in FDS:
    with contextlib.redirect_stdout(io.StringIO()):
        sv, _ = G19["surv_triggered"](fd, 2)
    for vk in VKS:
        with contextlib.redirect_stdout(io.StringIO()):
            S8[(fd, vk)] = float(G19["S8_of"](G19["T2"](G19["run"](sv, vk), LC19, 0.0)))
    P(f"    f_d {fd:4.2f}: " + "  ".join(f"{vk:.0f}: {S8[(fd, vk)]:.3f}" for vk in VKS) + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["U2"] = {f"{fd}_{vk:.0f}": v for (fd, vk), v in S8.items()}

# ============================================================================================ U3 galaxies + the window
banner("U3  GALAXIES at the cells passing U1 and U2, and THE WINDOW")
window = {"strict": [], "alt": []}
best = []
for (foot, fd), cells in U1.items():
    Lm["A0"] = FOOT[foot] * KPC_M / 1e6
    for c in cells:
        s8 = S8[(fd, c["vk"])]
        pass_cl = {"strict": abs(c["ratio"] - 1) <= 0.2, "alt": abs(c["ratio_nt"] - 1) <= 0.2}
        pass_s8 = {"strict": s8 >= S8_STRICT, "alt": s8 >= S8_ALT}
        best.append((abs(c["ratio_nt"] - 1), foot, fd, c["vk"], c["ratio_nt"], s8))
        for th in ("strict", "alt"):
            if pass_cl[th] and pass_s8[th]:
                gal = {}
                for kh, hst in GAL.items():
                    e, _ = retained(hernquist(hst["Mb"], hst["a"]), hst["M200"], c200_dm14(hst["M200"]), hst["rg"], GE_GAL,
                                    COUP, c["vk"], fd)
                    gal[kh] = gal_shift(hst, e, COUP)
                ok_g = all(v <= 0.06 for v in gal.values())
                P(f"    {th:6s} candidate {foot} f_d {fd} v_k {c['vk']:.0f}: X-COP {c['ratio']:.2f} (NT {c['ratio_nt']:.2f}), "
                  f"S_8 {s8:.3f}, galaxies max +{max(gal.values()):.3f} dex -> {'WINDOW' if ok_g else 'galaxies fail'}")
                if ok_g:
                    window[th].append((foot, fd, c["vk"]))
best.sort()
P("    closest cells to the X-COP gate (NT-corrected): " + "; ".join(
    f"{b[1]} f_d {b[2]} v_k {b[3]:.0f}: {b[4]:.2f} at S_8 {b[5]:.3f}" for b in best[:4]))
# the pincer in numbers: for each footing and f_d, the smallest kick that brings X-COP within 20% (alt), and S_8 there
pinch = []
for (foot, fd), cells in U1.items():
    okk = [c for c in cells if abs(c["ratio_nt"] - 1) <= 0.2]
    vmin = min((c["vk"] for c in okk), default=None)
    pinch.append(dict(foot=foot, fd=fd, vk_min=vmin, S8_at=(S8[(fd, vmin)] if vmin else None),
                      ratio_at_3000=cells[-1]["ratio_nt"]))
    P(f"    {foot:9s} f_d {fd:4.2f}: X-COP within 20% (NT) first at v_k = {vmin if vmin else '> 3000'}"
      + (f", where S_8 = {S8[(fd, vmin)]:.3f}" if vmin else f" (at 3000: {cells[-1]['ratio_nt']:.2f})"))
OUT["numbers"]["window"] = window; OUT["numbers"]["pinch"] = pinch
no_window = not window["strict"] and not window["alt"]
check("V1 NO UNIVERSAL WINDOW: under C-H/K's coupling no (footing, f_d, v_k) cell passes X-COP, S_8 and galaxies together, "
      "under either pre-declared threshold set",
      f"strict window {window['strict'] or 'none'}; alternative window {window['alt'] or 'none'}", no_window,
      "the live gravity candidate and the live dark carrier cannot both stand as written")

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  C-H/K's MOND sector reads the total lapse, so a minimally coupled carrier is boosted exactly like baryons (U0, from
  L340's own block).  Under that coupling the Lambda-triggered carrier, over f_d(0) = 0.8-0.99 and v_k = 1000-3000 km/s,
  with L340's kernel and both footings: window {'NONE' if no_window else window}.  The clusters need so little retained
  carrier once it is MOND-boosted that the kicks required to shed it take S_8 below its floors.
  WHAT WOULD SAVE THE PAIR (each a new ingredient, none on the record): a carrier coupled directly to U (so its phantom
  cancels -- a non-minimal coupling the U0 control shows is the only internal route); a kernel that does not read the
  carrier's field (a second metric or a baryon-only MOND source, i.e. not C-H/K); or a carrier that is absent from
  clusters at z = 0 while present at z = 2-3 (a faster late decay than Omega_Lambda^2).  NOT computed: C-H/K's own
  cosmological growth (unfloored kernel), which can only tighten the S_8 side.""")

n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
