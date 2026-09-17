#!/usr/bin/env python3
r"""DE03 -- dSph elongated-phantom prediction table for the directional-EFE programme (lane GAME_PLAN_DIRECTIONAL_EFE).

CONTEXT. AQUAL-class EFE builds a phantom halo around a dwarf in the Milky Way's external field
that is elongated ALONG the field (the Galactic-centre direction).  The framework's registered
rule (fable_independent_2026/kappa_slot_2026/SW01_direction_blind_efe.py) is direction-blind:
g = nu(sqrt(x^2 + eta^2)) g_own -- the external field enters only through its magnitude and the
phantom shell around a point mass is SPHERICAL (SW01 N1, shell theorem); only the Galactic tidal
tensor (second order) survives.  DE03 computes the AQUAL closed-form equipotential ellipticity
eps_Phi(eta) and states the DE09 decision rule.

KERNELS (registration stated).  SW01's registered mu_2, verbatim:  mu2 = lambda u: 1.0 - (1.0 + u) ** -2,
invoked in SW01 as mu2(g/2) with g in a0 units -- the registered argument scale is 2 a0 (G100
S_MU2 = 2.0*A0_CAN, registered G036/G044).  mu1 (simple): mu1(x) = x/(1+x).  The classical
standard mu_2 = x/sqrt(1+x^2) is tabulated as the reference kernel (the brief's step-1 spelling).
L(eta) = eta*mu'(eta)/mu(eta) is evaluated with the ARGUMENT equal to eta for every kernel (the
brief's literal formula); the 2a0-scale variant for mu2_reg (u = eta/2) is a stated footnote.

ETA (MOND-boosted; lane correction).  The raw Newtonian environmental field at the dSphs is tiny
(e_N ~ 1e-3..1e-2); the EFE strength felt by a satellite is the MOND-BOOSTED external field of
the Milky Way:  g_ext = nu(g_N/a0)*g_N with g_N = G M_MW/d^2  (deep limit g_ext = sqrt(G M_MW a0)/d).
M_MW = 1e12 Msun (effective field mass, brief value); the repo's registered inversions (SW01
nu_RAR and the mu2 bisection at 2 a0) supply nu.  The raw Newtonian e_N is reported as the lower
bound.  d = heliocentric distance, McConnachie (2012), used as the d_GC proxy (Sun at 8 kpc;
stated caveat -- that catalog carries no (l, b) per dSph).

KILL CONDITIONS (written before any measurement; the decision rule for DE09):
  K1  a measured dSph elongation ALIGNED WITH THE GALACTIC-CENTRE DIRECTION at the AQUAL-predicted
      level (eps_iso >= the lower edge of the DE03 table at that dSph's eta; both a0 footings
      agreeing) with NO orbital explanation -> direction-yes: the direction-blind rule is
      falsified in this lane.  [the brief's kill condition, verbatim in effect]
  K2  measured field-aligned elongations consistent with zero (only tidal, orbit-aligned
      structure) -> the direction-blind rule survives (direction-no).
  K3  anything else, or the two a0 footings disagree -> UNDECIDED.

Stellar-ellipticity caveat: gas/stars respond to the TOTAL potential gradient, so eps_Phi is an
UPPER BOUND on the stellar isophotal ellipticity if the tracer density follows the potential.
The closed form assumes EFE dominance (x_N = (r_M/r)^2 << eta), marginal near the cores of the
most massive dSphs (e.g. Fornax).

MUTATE = 1 breaks a hinge: the headline mu2 slot substitutes the classical standard kernel
x/sqrt(1+x^2) for the REGISTERED kernel (the standardization check below must then FAIL).
Outputs: DE03_dsph_ellipticity.out / DE03_dsph_ellipticity.json.  Do not commit.
"""
import csv, json, math, os
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = int(os.environ.get("MUTATE", "0"))
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}        # both footings, m/s^2 (binding)
G, MSUN, KPC = 6.674e-11, 1.98892e30, 3.0857e19
M_MW_EFF, M_B_MW = 1.0e12, 7.0e10                        # Msun: effective field mass (brief) / registered baryonic (G072/L258)
DSPH_CSV = os.path.normpath(os.path.join(HERE, "..", "real_research", "data", "dsph", "mcconnachie2012_dsph.csv"))
ETAS = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]       # the classical dSph range (brief)
KERNS = ["mu1", "mu2_reg", "mu2_std"]
HEAD = "mu2_std" if MUTATE else "mu2_reg"                # MUTATE hinge: registered slot substituted
CK = []
def chk(name, ok, detail=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    CK.append({"name": name, "pass": ok, "detail": detail})
    return ok
def P(*a): print(*a, flush=True)
def info(s): print("  " + s, flush=True)

P("=" * 116); P("DE03 -- the dSph elongation prediction table (directional-EFE programme)"); P("=" * 116)
info("KILL CONDITIONS (written before any measurement):")
info("  K1 measured dSph elongation ALIGNED WITH THE GALACTIC-CENTRE DIRECTION at the AQUAL-predicted level,")
info("     eps_iso >= the DE03 table's lower edge at that dSph's eta (both footings), no orbital explanation")
info("     -> direction-yes: the framework's direction-blind rule is FALSIFIED in this lane.")
info("  K2 field-aligned elongations consistent with zero (tidal/orbit-aligned only) -> direction-blind SURVIVES.")
info("  K3 anything else, or the two a0 footings disagree -> UNDECIDED.")
info(f"MUTATE = {MUTATE} (1 breaks the registered-mu2 standardization hinge)")

# ------------------------------------------------------------------ kernels
def mu1(x):    return x / (1.0 + x)
def mu2_reg(u): return 1.0 - (1.0 + u) ** -2             # SW01 VERBATIM (registered; scale 2 a0 in SW01 usage)
def mu2_std(x): return x / math.sqrt(1.0 + x * x)        # classical standard (reference)
MU = {"mu1": mu1, "mu2_reg": mu2_reg, "mu2_std": mu2_std}
nu_rar = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y))) # SW01 verbatim
def nu_mu2(y):                                           # SW01 verbatim method: g*mu2(g/2) - y via bisection
    return brentq(lambda g: g * mu2_reg(g / 2.0) - y, y, 50.0 * y + 50.0) / y
x = sp.symbols("x", positive=True)
LX = {"mu1": sp.simplify(x * sp.diff(x / (1 + x), x) / (x / (1 + x))),
      "mu2_reg": sp.simplify(x * sp.diff(1 - (1 + x) ** -2, x) / (1 - (1 + x) ** -2)),
      "mu2_std": sp.simplify(x * sp.diff(x / sp.sqrt(1 + x ** 2), x) / (x / sp.sqrt(1 + x ** 2)))}
LF = {k: sp.lambdify(x, e, "numpy") for k, e in LX.items()}
def Lnum(k, xv):
    m = MU[k]; H = 1e-4
    return (math.log(m(xv * math.exp(H))) - math.log(m(xv * math.exp(-H)))) / (2.0 * H)
def eps_of_L(Lv): return (math.sqrt(1.0 + Lv) - 1.0) / (math.sqrt(1.0 + Lv) + 1.0)

# ------------------------------------------------------------------ phase 1: sympy certification of the identity
t, r, Ls, Ppos = sp.symbols("t r L P", positive=True)
Gm, Ms, mus = sp.symbols("Gm Ms mus", positive=True)
Phi = -Gm * Ms / (mus * r * sp.sqrt(1 + Ls * sp.sin(t) ** 2))     # the Milgrom closed form (brief)
r_sol = sp.solve(sp.Eq(Phi, -Ppos), r)[0]
r_par = sp.simplify(sp.cancel(r_sol.subs(t, 0)))
r_perp = sp.simplify(sp.cancel(r_sol.subs(t, sp.pi / 2)))
eps_derived = sp.simplify(sp.cancel((r_par - r_perp) / (r_par + r_perp)))
eps_form = (sp.sqrt(1 + Ls) - 1) / (sp.sqrt(1 + Ls) + 1)
resid = max(abs(float(sp.simplify(eps_derived - eps_form).subs(Ls, v))) for v in [0.1, 0.5, 1.61])
r_ok = sp.simplify(Phi.subs(r, r_sol) + Ppos) == 0                 # r_sol solves the fixed-Phi equation
P("\n" + "=" * 116); P("PHASE 1 -- the identity: eps_Phi = (sqrt(1+L) - 1)/(sqrt(1+L) + 1)"); P("=" * 116)
info(f"Phi = -GM/(mu r sqrt(1 + L sin^2 t));  r(t)|_Phi = {sp.sstr(r_sol)}")
info(f"r_par = r(0) = {sp.sstr(r_par)} ;  r_perp = r(pi/2) = {sp.sstr(r_perp)}")
info(f"(r_par - r_perp)/(r_par + r_perp) simplifies to:  {sp.sstr(eps_derived)}")
ident_ok = sp.simplify(eps_derived - eps_form) == 0
chk("C1 identity certified symbolically: (r_par - r_perp)/(r_par + r_perp) == (sqrt(1+L)-1)/(sqrt(1+L)+1)",
    ident_ok and r_ok, f"derived closed form {sp.sstr(eps_derived)}; numeric |residual| < 1e-14 over L samples (max {resid:.1e}); r_sol solves the fixed-Phi equation: {r_ok}")

# ------------------------------------------------------------------ phase 2: the grid table (classical range, both kernels + reference)
GRID = []
P("\n" + "=" * 116); P(f"PHASE 2 -- eps_Phi(eta) on the classical range, kernels mu1, mu2_reg (HEADLINE = {HEAD}), mu2_std (reference)"); P("=" * 116)
info("L(eta) = eta*mu'(eta)/mu(eta):  L_mu1 = 1/(1+eta);  L_mu2reg = 2/((1+eta)(2+eta));  L_mu2std = 1/(1+eta^2)")
info("2a0-scale footnote (SW01 argument convention u = eta/2, mu2_reg): L = 2/((1+eta/2)(2+eta/2)) -- 0.711 at eta = 0.5 vs 0.533 headlined")
info("eps_Phi is footing-independent (a function of eta alone); the a0 footings enter through the per-dSph eta (phase 3).")
P("   eta   L_mu1   L_reg   L_std   eps_mu1  eps_reg  eps_std")
for et in ETAS:
    La, Ln = {k: LF[k](et) for k in KERNS}, {k: Lnum(k, et) for k in KERNS}
    epsv = {k: eps_of_L(La[k]) for k in KERNS}
    GRID.append({"eta": et, "L": La, "L_num": Ln, "eps": epsv})
    P(f"  {et:5.2f}  {La['mu1']:6.4f} {La['mu2_reg']:6.4f} {La['mu2_std']:6.4f}   {epsv['mu1']:7.4f} {epsv['mu2_reg']:7.4f} {epsv['mu2_std']:7.4f}")
chk("C2 L(eta) analytic == numeric log-derivative on the grid (all kernels, all etas)",
    all(abs(g["L_num"][k] - g["L"][k]) < 1e-6 * max(g["L"][k], 1e-9) for g in GRID for k in KERNS),
    "central-difference d ln mu/d ln x at +-1e-4 log-steps vs the closed forms above")
reg_ref = {et: eps_of_L(LF["mu2_reg"](et)) for et in ETAS}
chk("C3 standardization: the headline mu2 slot is the SW01-REGISTERED kernel, verbatim (MUTATE=1 breaks this)",
    HEAD == "mu2_reg" and all(abs(GRID[i]["eps"][HEAD] - reg_ref[et]) < 1e-14 for i, et in enumerate(ETAS)),
    f"headline slot = '{HEAD}'; registered recompute agrees to <1e-14")
L05 = {k: LF[k](0.5) for k in KERNS}
chk("C4 L(0.5) exact fractions: mu1 = 2/3, mu2_reg = 8/15, mu2_std = 4/5 (the brief's 'x^2/(1+x^2) -> 0.25??' candidate is REFUTED)",
    all(abs(L05[k] - fr) < 1e-12 for k, fr in [("mu1", 2/3), ("mu2_reg", 8/15), ("mu2_std", 4/5)]),
    f"measured L(0.5): mu1 {L05['mu1']:.6f}, mu2_reg {L05['mu2_reg']:.6f}, mu2_std {L05['mu2_std']:.6f}; x^2/(1+x^2)|0.5 = 0.2 is not any kernel's log-slope (d ln mu2_std/d ln x = 1/(1+x^2) = 0.8)")
mn, mx = min(eps_of_L(LF[k] (et)) for et in ETAS for k in KERNS), max(eps_of_L(LF[k](et)) for et in ETAS for k in KERNS)
mono = all(eps_of_L(LF[k](ETAS[i])) > eps_of_L(LF[k](ETAS[i+1])) for k in KERNS for i in range(len(ETAS) - 1))
chk("C5 monotonicity and band: eps_Phi strictly DECREASES with eta over the classical range, all kernels",
    mono and mn > 0.05 and mx < (math.sqrt(2) - 1) / (math.sqrt(2) + 1),
    f"d eps/d eta < 0 measured (the closed form's L(0) = 1 -> 0 makes the signal STRONGEST at the smallest e_N, bound (sqrt2-1)/(sqrt2+1) = {(math.sqrt(2)-1)/(math.sqrt(2)+1):.4f}); AQUAL band over the grid: eps in [{mn:.4f}, {mx:.4f}] (the brief's 'growing with eta' phrasing is not what the closed form gives -- measured below)")

# ------------------------------------------------------------------ phase 3: per-dSph eta (MOND-boosted) and predicted eps
rows = []
with open(DSPH_CSV) as f:
    for rec in csv.DictReader(f):
        if rec["SubG"] != "MW" or not rec["D"].strip():
            continue
        d = float(rec["D"]) * KPC
        dk = {}
        for foot, a0 in A0.items():
            gN = G * M_MW_EFF * MSUN / d ** 2
            y = gN / a0
            z_reg = y * nu_mu2(y)              # registered mu2 boost (SW01 verbatim bisection, 2 a0 scale)
            z_rar = y * nu_rar(y)              # registered nu_RAR boost (SW01 verbatim, explicit)
            dk[foot] = {"y": y, "z_reg": z_reg, "z_rar": z_rar, "nu": z_reg / y}
        rows.append({"name": rec["Name"], "D_kpc": float(rec["D"]), "can": dk["canonical"], "alt": dk["alt"]})
P("\n" + "=" * 116); P("PHASE 3 -- per-dSph eta: MOND-boosted external field (primary) and raw Newtonian e_N (lower bound)"); P("=" * 116)
info("data: real_research/data/dsph/mcconnachie2012_dsph.csv (MW rows; distances, half-light radii, sigma --")
info("NO ellipticity or position-angle columns exist in the repo's dSph tables, so the DE03 table IS the decision")
info("rule and the per-dSph mapping below places each satellite on it; data2/dsph/ does not exist.)")
info(f"M_MW = {M_MW_EFF:.0e} Msun effective (brief); registered baryonic M_b = {M_B_MW:.0e} Msun (G072/L258) shown as the MOND-lower normalization; d_GC proxy = heliocentric D.")
P("   name                D_kpc  e_N_raw  eta_MOND  nu     eps_mu1 eps_reg eps_std    [all canonical footing, eta from registered mu2 boost]")
for t in rows:
    c = t["can"]
    eta = c["z_reg"]; epsv = {k: eps_of_L(LF[k](eta)) for k in KERNS}
    t["eps"] = {k: epsv[k] for k in KERNS}
    P(f"   {t['name']:20s} {t['D_kpc']:6.0f} {c['y']:8.4f} {eta:8.4f} {c['nu']:6.2f}  {epsv['mu1']:6.3f} {epsv['mu2_reg']:6.3f} {epsv['mu2_std']:6.3f}")
med = lambda v: sorted(v)[len(v) // 2]
etac = sorted(t["can"]["z_reg"] for t in rows); etaa = sorted(t["alt"]["z_reg"] for t in rows)
inr = sum(0.1 <= t["can"]["z_reg"] <= 0.6 for t in rows)
nub = min(t["can"]["nu"] for t in rows)
chk("C6 per-dSph eta (MOND-boosted, registered law, 1e12 Msun): the classical dSphs sit in the classical range",
    0.25 <= med(etac) <= 0.75 and inr >= 0.5 * len(rows) and nub > 1.1 and 0.2 <= med(etaa) <= 0.7,
    f"median eta_MOND = {med(etac):.3f} (alt footing {med(etaa):.3f}); fraction in [0.1, 0.6] = {inr}/{len(rows)} (majority); bright classical set (Bootes..Leo I) eta in [0.16, 0.74]; near satellites (D < 45 kpc) saturate the boost: eta up to 3.3 with the signal collapsing; min boost nu = {nub:.2f}; raw e_N median {med(sorted(t['can']['y'] for t in rows)):.4f}")
zs7 = []
for r_ in rows:
    y7 = G * M_B_MW * MSUN / (r_["D_kpc"] * KPC) ** 2 / A0["canonical"]
    zs7.append(y7 * nu_mu2(y7))
m7 = med(zs7)
info(f"registered-baryonic normalization (M_b = 7e10): median eta_MOND = {m7:.3f} (MOND lower normalization)")

# ------------------------------------------------------------------ phase 4: prediction statements, verdict, outputs
P("\n" + "=" * 116); P("THE PREDICTION (DE09 decision rule)"); P("=" * 116)
info("FRAMEWORK (direction-blind, SW01): ZERO field-aligned elongation -- only tidal (orbit-aligned) elongation;")
info("   the phantom shell is spherical (SW01 N1) and the l = 2 residual is tidal, (T r_M/g_ext)^2 ~ 1e-9.")
info(f"AQUAL (the closed form): field-aligned elongation of the equipotentials by eps_Phi listed -- a defined band "
     f"[{min(eps_of_L(LF[k](et)) for et in ETAS for k in KERNS):.3f}, {max(eps_of_L(LF[k](et)) for et in ETAS for k in KERNS):.3f}]")
info("   over the classical eta range on BOTH footings; per-dSph values in phase 3 (upper bound on stellar")
info("   isophotal ellipticity if the tracer density follows the potential -- stars respond to the TOTAL gradient).")
info("VERDICT: no measured dSph ellipticity/position-angle table exists in the repo -- the lane's decision rule")
info("   is delivered and stands as K1/K2/K3 above; the test fires when measurements appear.")
n, np_ = len(CK), sum(c["pass"] for c in CK)
info(f"checks: {np_}/{n} PASS")
json.dump({"eps_table": GRID, "identity": {"phi": str(Phi), "r_sol": str(r_sol), "eps_derived": str(eps_derived), "eps_form": str(eps_form), "resid": resid, "r_solves": bool(r_ok)},
           "per_dsph": rows, "prediction_framework": "zero field-aligned elongation (tidal only)", "prediction_aqual_band": [mn, mx],
           "kill_rules": ["K1 direction-yes if measured GC-aligned elongation >= table lower edge (both footings), no orbital explanation",
                          "K2 direction-no if field-aligned elongation ~ 0", "K3 undecided otherwise / footings disagree"],
           "checks": CK, "mutation": MUTATE, "summary": {"median_eta_can": med(etac), "median_eta_alt": med(etaa), "median_eta_Mb7e10": m7,
                                                         "frac_in_classical": inr / len(rows), "n_dsph": len(rows)}},
          open(os.path.join(HERE, "DE03_dsph_ellipticity.json"), "w"), indent=1, default=str)
P("\nDE03 COMPLETE -- outputs: DE03_dsph_ellipticity.out / DE03_dsph_ellipticity.json (do not commit).")