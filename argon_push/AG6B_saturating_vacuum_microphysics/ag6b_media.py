"""AG6B media: which microscopic medium saturates the vacuum polarization at u -> a0/n, and which n does it give?

Criteria: FROZEN_CRITERIA.md (committed alone, dbcaeba9e, before any computation).
Classes A-F; admissibility A1-A4 here (A5 = raw SPARC in ag6b_sparc.py); theorems T-A, T-F1, T-F2; second predictions S-a..S-f.
kappa = 1/2 FITTED; both footings, never pooled; no particle species; not theory closed.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 ag6b_media.py        (AG6B_MUTATE=1: Mu1-Mu4, Mu6, Mu7; exit 1 iff all bite)

Mapping used throughout (PAPER49 rest state, gamma -> 0):  g_N = R(u),  g = g_N + u,  u = U(g) (polarization vs total field),
R(u) = U^{-1}(u) - u.  dR/du = 1/U'(g) - 1.  Capacity family: R_n = u^2/(a0 - n u).
"""
import os, sys, json, math

import numpy as np
import sympy as sp
import mpmath as mp
from scipy import special, integrate, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("AG6B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6b_media{TAG}.out"), "w")
RES = {"lane": "AG6B", "script": "ag6b_media.py", "criteria": "dbcaeba9e", "mutate": MUT,
       "candidates": {}, "theorems": {}, "second_predictions": {}, "checks": {}}

Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)                 # 5.7888 (= CFG4_common.Z_FRAME); a_H = Z a0 on each footing
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}        # asserted equal to CFG4_common.A0 in ag6b_sparc.py
G_SI, MSUN, PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16


def P_(s=""):
    print(s)
    OUT.write(s + "\n")
    OUT.flush()


def check(key, ok, detail=""):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())
g, u, a0, c, s_ = sp.symbols("g u a_0 c s", positive=True)
gr = sp.symbols("g_r", real=True)                         # real (signed) field component for the oddness/analyticity test


def lead(expr, var):
    """leading term coeff * var**p of expr as var -> 0+ (sympy series)."""
    e = sp.simplify(expr)
    lt = sp.series(e, var, 0, 7).removeO()
    if lt == 0:
        return sp.Integer(0), sp.oo
    lt = sp.expand(lt)
    terms = lt.as_ordered_terms()
    best = None
    for t in terms:
        cf, ex = t.as_coeff_exponent(var)
        if best is None or sp.simplify(ex - best[1]) < 0:
            best = (cf, ex)
    return sp.simplify(best[0]), sp.nsimplify(best[1])


def chi_is_analytic(U_of_g):
    """T-A test: write the vector response as U = chi(s) g with s = g^2 and ask whether chi has a Taylor series in integer powers
    of s at s = 0 (analytic in the vector field). Returns (analytic?, exponents seen)."""
    chi = sp.simplify((U_of_g / g).subs(g, sp.sqrt(s_)))
    ser = sp.series(chi, s_, 0, 3).removeO()
    exps = sorted({sp.nsimplify(t.as_coeff_exponent(s_)[1]) for t in sp.expand(ser).as_ordered_terms()})
    return all(e.is_integer for e in exps), [str(e) for e in exps]


def record(key, **kw):
    RES["candidates"][key] = {k: (str(v) if isinstance(v, sp.Basic) else v) for k, v in kw.items()}


def deep_slope(p):
    """for g_N ~ g^p at small g: point mass g ~ r^(-2/p), V ~ r^((p-2)/(2p)); BTFR (V^4 ~ M, r-independent) only at p = 2."""
    p = sp.nsimplify(p)
    return str(sp.simplify((p - 2) / (2 * p)))


def classify_U(key, cls, U, desc, free, natural, scale_note=""):
    """U(g) already has A1 and A2 imposed where possible (scale expressed through a0). Computes A1-A4, n1, n_cap, family test."""
    U = sp.simplify(U)
    U1 = sp.limit(sp.diff(U, g), g, 0, "+")
    a1 = sp.simplify(U1 - 1) == 0
    cf, p = lead(g - U, g)
    a2 = bool(p == 2 and sp.simplify(cf - 1 / a0) == 0)
    umax = sp.limit(U, g, sp.oo)
    a3 = bool(umax.is_finite and umax.is_real and umax.is_positive)
    ncap = sp.simplify(a0 / umax) if a3 else sp.oo
    # n1 = 2 - b3 a0^2, b3 = cubic coefficient of U(g) (valid when A1, A2 hold)
    n1 = None
    if a1 and a2:
        b3 = sp.series(U, g, 0, 4).removeO().coeff(g, 3)
        n1 = sp.nsimplify(sp.simplify(2 - b3 * a0 ** 2))
    one = {sym: 1 for sym in U.free_symbols if sym != g}          # numerics: every scale = 1 (a0 = 1 after A2)
    Un = U.subs(one)
    fam = False
    if a3 and a1 and a2:
        resid = sp.simplify((g - U) * (a0 - ncap * U) - U ** 2)
        fam = resid == 0
        if not fam:  # numeric fallback (frozen: relative residual < 1e-10 on 200 points in (0, 0.999 u_max))
            f = sp.lambdify(g, (((g - U) * (a0 - ncap * U) - U ** 2) / U ** 2).subs(one), modules=["scipy", "numpy"])
            xs = np.logspace(-3, 3, 200)
            with np.errstate(all="ignore"):
                rv = np.abs(np.asarray(f(xs), dtype=float))
            fam = bool(np.all(np.isfinite(rv)) and np.max(rv) < 1e-10)
    # A4 numeric with every scale = 1: 0 < U'(g) < 1 for g in (1e-3, 1e3)  (R' = 1/U' - 1 > 0); 40-digit mpmath so that
    # neither cancellation near g -> 0 nor underflow at large g can fake a failure
    dU = sp.lambdify(g, sp.diff(Un, g), modules="mpmath")
    a4 = True
    with mp.workdps(40):
        for xv in np.logspace(-3, 3, 300):
            try:
                dv = mp.mpmathify(dU(mp.mpf(xv)))
            except (ZeroDivisionError, ValueError):
                a4 = False
                break
            if abs(mp.im(dv)) > mp.mpf(10) ** -30 or not (0 < mp.re(dv) < 1):
                a4 = False
                break
    analytic, exps = chi_is_analytic(U)
    record(key, cls=cls, desc=desc, U=U, A1=bool(a1), A2=a2, A3=a3, A4=a4, deep_power=str(p), deep_coeff=cf,
           V_slope=deep_slope(p) if p != sp.oo else "n/a", u_max=umax, n_cap=str(ncap), n1=str(n1), in_family=bool(fam),
           chi_analytic=analytic, chi_exponents=exps, free_choices=free, natural=natural, scale_note=scale_note,
           pass_A1_A4=bool(a1 and a2 and a3 and a4))
    P_(f"  {key:6s} [{cls}] {desc}")
    P_(f"         U(g) = {U}")
    P_(f"         A1 U'(0)={U1} {'ok' if a1 else 'FAIL'} | deep g_N ~ {cf} g^{p} -> A2 {'ok' if a2 else 'FAIL'}"
       f"{'' if a2 else f' (point-mass V ~ r^{deep_slope(p)})' if p != sp.oo else ''} | u_max={umax} (A3 {'ok' if a3 else 'FAIL'})"
       f" n_cap={ncap} n1={n1} | A4 {'ok' if a4 else 'FAIL'} | in-family={fam} | chi analytic in g^2: {analytic} {exps}")
    P_(f"         free choices: {free}; natural: {natural} {scale_note}")
    return RES["candidates"][key]


def classify_R(key, cls, R, desc, free, natural, umax=None, note=""):
    """R(u) given (restoring force). A1 <=> R(0) = 0 and R'(0) = 0 (leading power > 1); A2 <=> R ~ u^2/a0, achievable iff the
    leading power is 2 with a positive coefficient (the medium's one scale is then set to a0)."""
    cf, p = lead(R, u)
    a1 = bool(p > 1)
    a2 = bool(p == 2 and sp.simplify(cf).is_positive)
    a3 = umax is not None
    pos = bool(sp.simplify(cf).is_positive) if cf != 0 else False
    a4 = pos  # leading-order sign (stability of the deep regime); full check done per candidate where a capacity exists
    record(key, cls=cls, desc=desc, R=R, A1=a1, A2=a2, A3=a3, A4=a4, R_power=str(p), R_coeff=cf,
           deep_power=str(p) if a1 else "Newtonian (linear restoring / non-critical)",
           V_slope=deep_slope(p) if a1 else "n/a", u_max=str(umax), free_choices=free, natural=natural, note=note,
           pass_A1_A4=bool(a1 and a2 and a3 and a4), in_family=False)
    P_(f"  {key:6s} [{cls}] {desc}")
    why = "" if (a2 or not a1) else (" (negative coefficient: anti-restoring)" if p == 2 else
                                     f" (deep g_N ~ g^{p}, V ~ r^{deep_slope(p)})")
    P_(f"         R(u) = {R};  leading {cf} u^{p} -> A1 {'ok' if a1 else 'FAIL'}, A2 {'ok' if a2 else 'FAIL'}"
       f"{why}, A3 {'ok' if a3 else 'FAIL (no capacity)'},"
       f" sign {'+' if pos else '-/0'} (A4 {'ok' if a4 else 'FAIL'})  {note}")
    P_(f"         free choices: {free}; natural: {natural}")
    return RES["candidates"][key]


# ======================================================================================================== CLASS A
P_("\n" + "=" * 110 + "\nCLASS A: analytic equilibrium media (criticality A1 imposed by solving for the medium's amplitude)")
us, gT, b, zeta, vc = sp.symbols("u_s g_T b zeta v_c", positive=True)


def crit_amp(Uexpr, amp):
    sol = sp.solve(sp.Eq(sp.limit(sp.diff(Uexpr, g), g, 0, "+"), 1), amp)
    return sp.simplify(Uexpr.subs(amp, sol[0]))


L = lambda y: sp.coth(y) - 1 / y
classify_U("A-1", "A", crit_amp(us * L(g / gT), us), "Langevin classical dipoles u = u_s L(g/g_T)", "g_T (one scale)", True)
for J in (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2)):
    BJ = lambda y: (2 * J + 1) / (2 * J) * sp.coth((2 * J + 1) * y / (2 * J)) - 1 / (2 * J) * sp.coth(y / (2 * J))
    classify_U(f"A-2J{J}", "A", crit_amp(us * BJ(g / gT), us), f"Brillouin spin-J={J} (J=1/2: thermal two-level tanh)",
               "g_T", True)
cc5 = sp.symbols("c_5", positive=True)
classify_R("A-3", "A", b * u ** 3 + cc5 * u ** 5, "Landau para/ferroelectric at criticality (R = b u^3 + c u^5)", "b, c", True,
           umax=None)
classify_U("A-4i", "A", g / sp.sqrt(1 - g ** 2 / b ** 2), "Born-Infeld, D(E) with g<->E, u = D (critical, field-limited)", "b",
           True)
classify_U("A-4ii", "A", g / sp.sqrt(1 + g ** 2 / b ** 2), "Born-Infeld field-limited branch u = E(D), D<->g (saturates at b)",
           "b", True)
c4iii = sp.limit(sp.diff(g / sp.sqrt(1 - g ** 2 / b ** 2) - g, g), g, 0, "+")
record("A-4iii", cls="A", desc="Born-Infeld literal vacuum polarization u = D - E", U=str(g / sp.sqrt(1 - g ** 2 / b ** 2) - g),
       A1=False, A2=False, A3=False, A4=False, pass_A1_A4=False, in_family=False, natural=True, free_choices="b",
       note=f"linear susceptibility U'(0) = {c4iii}: cannot be critical")
P_(f"  A-4iii [A] Born-Infeld literal polarization u = D - E: U'(0) = {c4iii} -> A1 FAIL (zero linear susceptibility)")
classify_R("A-5", "A", 4 * zeta * u ** 3, "Euler-Heisenberg weak field (massive loops) as the remainder energy: R = 4 zeta u^3",
           "zeta", True, note="(literal EH polarization 4 zeta E^3 has U'(0)=0: not critical)")
classify_U("A-6", "A", g * (1 - g ** 2 / vc ** 2), "Ginzburg-Landau depairing j = rho_s v(1 - v^2/v_c^2), critical rho_s",
           "v_c", True, scale_note="(turns over at v_c/sqrt3: A4 fails there)")
classify_U("A-7", "A", crit_amp(us * L(g / gT), us), "freely-jointed polymer chain: extension = L(f b/kT) (same as A-1)",
           "kT/b", True)

P_("\nT-A theorem (sympy): U = chi(g^2) g with chi analytic, A1 imposed (chi(0) = 1)  =>  g - U has odd powers only, >= 3")
x1, x2, x3 = sp.symbols("chi_1 chi_2 chi_3")
chi_gen = 1 + x1 * s_ + x2 * s_ ** 2 + x3 * s_ ** 3
Ugen = gr * chi_gen.subs(s_, gr ** 2)
diff_gen = sp.expand(gr - Ugen)
odd = sp.simplify(diff_gen.subs(gr, -gr) + diff_gen) == 0
pows = sorted({t.as_coeff_exponent(gr)[1] for t in diff_gen.as_ordered_terms()})
no_quadratic = sp.expand(diff_gen).coeff(gr, 2) == 0
TA = dict(odd=bool(odd), powers=[str(p) for p in pows], no_g2_term=bool(no_quadratic),
          statement="analytic isotropic media give g_N = -chi_1 g^3 - chi_2 g^5 ...: never the deep law g_N = g^2/a0; "
                    "with criticality the deep law is g_N ~ g^3 (point mass V ~ r^(1/6), no BTFR)")
class_A_keys = [k for k in RES["candidates"] if k.startswith("A-")]
TA["all_class_A_fail_A2"] = all(not RES["candidates"][k]["A2"] for k in class_A_keys)
TA["class_A_chi_analytic"] = {k: RES["candidates"][k].get("chi_analytic") for k in class_A_keys if "chi_analytic" in RES["candidates"][k]}
RES["theorems"]["T-A"] = TA
check("T-A analytic media never give the deep law (odd powers only, no g^2 term); all class-A candidates fail A2",
      odd and no_quadratic and TA["all_class_A_fail_A2"], f"powers {TA['powers']}")

# ======================================================================================================== CLASS B
P_("\n" + "=" * 110 + "\nCLASS B: scale-free non-analytic power media W ~ |u|^q  (R ~ u^(q-1)); CFG690: deep law <=> q = 3")
kq = sp.symbols("k", positive=True)
for d in (1, 2, 3):
    q = 1 + sp.Rational(2, d)
    classify_R(f"B-1d{d}", "B", kq * u ** (q - 1), f"degenerate Fermi carriers in d={d}: E ~ n^(1+2/d), q = {q}", "k", True,
               note="(continuum: no capacity)")
RES["candidates"]["B-1d1"]["continuum_law"] = "R = u^2/a0 for all u  =>  g = g_N + sqrt(a0 g_N) = CFG690's nu_SI = 1 + y^-1/2 " \
                                              "(scored FAIL on the Upsilon band by CFG690: 0.1012@0.46 / 0.1007@0.42)"
P_("         B-1d1 continuum law: R = u^2/a0 everywhere => nu = 1 + y^-1/2 = CFG690's SI law (CFG690: FAIL, Upsilon band); "
   "the cubic arises from 1D Pauli exclusion")
classify_R("B-2D4", "B", kq * u * sp.log(u), "massless Euler-Heisenberg, D=4: L ~ E^2 ln E", "k", True,
           note="(dimensional analysis; log)")
for D in (5, 6):
    classify_R(f"B-2D{D}", "B", kq * u ** (sp.Rational(D, 2) - 1), f"massless Euler-Heisenberg, D={D}: L ~ |eE|^(D/2)", "k", True,
               note="(no capacity; D=6 is not our spacetime)")
Tl = sp.symbols("T_lam", positive=True)
WT = -(Tl / (12 * sp.pi)) * (u / (4 * sp.pi * sp.Symbol("G", positive=True))) ** 3       # -(T lambda^3/2 /12pi)|P|^3, P = u/K
RT = sp.simplify(4 * sp.pi * sp.Symbol("G", positive=True) * sp.diff(WT, u))
classify_R("B-3", "B", RT, "thermal bosonic zero-mode cubic -(T/12pi)(lambda P^2)^(3/2) (textbook high-T expansion)", "T lambda^3/2",
           True, note="(sign is the point)")

# ======================================================================================================== CLASS C
P_("\n" + "=" * 110 + "\nCLASS C: kinetic driven single-occupancy cells  theta' = alpha g^p (1-theta) - beta theta, u = u_m theta_ss")
al, be, um = sp.symbols("alpha beta u_m", positive=True)


def langmuir(p):
    th = al * g ** p / (al * g ** p + be)
    return um * th


pump_p = 2 if MUT else 1                                  # Mu1: coherent pump p = 2
Ul = langmuir(pump_p)
dU0 = sp.limit(sp.diff(Ul, g), g, 0, "+")
P_(f"  C-1 pump exponent p = {pump_p}: U'(0) = {dU0}")
for ptest in (sp.Rational(1, 2), 2):
    P_(f"      (report) p = {ptest}: U'(0) = {sp.limit(sp.diff(langmuir(ptest), g), g, 0, '+')}  -> A1 needs p = 1")
if dU0.is_finite and dU0 != 0:
    Ul = Ul.subs(be, sp.solve(sp.Eq(dU0, 1), be)[0])      # criticality: beta = alpha u_m (capacity = saturation field)
    cf, pw = lead(g - Ul, g)
    Ul = sp.simplify(Ul.subs(um, sp.solve(sp.Eq(cf, 1 / a0), um)[0])) if pw == 2 else Ul
else:
    Ul = sp.simplify(Ul.subs({be: al * a0, um: a0}))      # mutated pump: keep scales at a0 to show the failure
rC1 = classify_U("C-1", "C", Ul, f"Langmuir / Michaelis-Menten / incoherently pumped two-level saturation, pump ~ |g|^{pump_p}",
                 "pump exponent (A1 forces 1), single occupancy", True,
                 scale_note="(one scale u_m = beta/alpha, fixed = a0 by A2)")
if not MUT:
    Gam = sp.simplify((al * g + al * a0) / (al * a0))
    RES["candidates"]["C-1"]["kinetic_rate_ratio"] = str(Gam)
    P_(f"         kinetic relaxation Gamma(g)/Gamma(0) = {Gam}")
for p_h in (sp.Rational(1, 2), 2):
    th = (g / a0) ** p_h / (1 + (g / a0) ** p_h)
    d0 = sp.limit(sp.diff(a0 * th, g), g, 0, "+")
    record(f"C-2h{p_h}", cls="C", desc=f"Hill-cooperative theta = y^h/(1+y^h), h = {p_h}", U=str(a0 * th), A1=False, A2=False,
           A3=True, A4=False, pass_A1_A4=False, in_family=False, natural=True, free_choices="h",
           note=f"U'(0) = {d0}: no finite critical susceptibility for any amplitude")
    P_(f"  C-2h{p_h} Hill h = {p_h}: U'(0) = {d0} -> A1 FAIL for any amplitude")
for bt in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)):
    Uct = g / (1 + (g / um) ** bt) ** (1 / bt)
    cf, pw = lead(g - Uct, g)
    if pw == 2:
        Uct = sp.simplify(Uct.subs(um, sp.solve(sp.Eq(cf, 1 / a0), um)[0]))
    else:
        Uct = Uct.subs(um, a0)
    classify_U(f"C-3b{bt}", "C", Uct, f"Caughey-Thomas velocity saturation, beta = {bt}", "beta (A2 forces 1)", True)
betaS = sp.symbols("beta_s", positive=True)
P_(f"      (general beta) (g - U)/g^(1+beta) -> {sp.limit((g - g / (1 + (g / um) ** 3) ** sp.Rational(1, 3)) / g ** 4, g, 0, '+')} "
   f"at beta=3, i.e. 1/(beta u_m^beta): deep power 1 + beta; A2 <=> beta = 1")
gs = sp.symbols("g_s", positive=True)
sR = (g / gs) ** 2
classify_U("C-4", "C", um * sR / (1 + sR), "coherent (Rabi) pump s ~ g^2: u = u_m s/(1+s)", "g_s", True)
record_C5 = dict(cls="C", desc="Unruh-Langmuir: C-1 with saturation field tied to the horizon, a0_eff = a_H = Z a0_footing",
                 U="a_H g/(a_H + g)", A1=True, A2=True, A3=True, A4=True, n_cap="1", in_family=True, natural=True,
                 free_choices="pump ~ T_U ~ |g|, emptying ~ horizon rate", pass_A1_A4=True, scale_ratio=Z,
                 a0_eff={f: Z * A0[f] for f in A0})
RES["candidates"]["C-5"] = record_C5
P_(f"  C-5    [C] Unruh-Langmuir scale tie: a0_eff = a_H = Z a0 = {Z:.4f} a0 (canonical {Z * A0['canonical']:.4e}, alt "
   f"{Z * A0['alt']:.4e}); A5 scored at that a0 in ag6b_sparc.py")
# C-6 thermal Fermi single cell responding to |g| (one quantum of displacement per cell, displaced along the local field)
dT = sp.symbols("d_T", positive=True)
th0 = sp.symbols("theta_0", positive=True)
# theta(g) = 1/(1 + exp(eps0 - d g/T)) rewritten with theta(0) = theta_0 (eps0/T = ln(1/theta_0 - 1)); energies in units of T
thF = th0 * sp.exp(dT * g) / (th0 * sp.exp(dT * g) + 1 - th0)
UF = um * (thF - th0)
U1F = sp.simplify(sp.diff(UF, g).subs(g, 0))
U2F = sp.simplify(sp.diff(UF, g, 2).subs(g, 0))
um_sol = sp.solve(sp.Eq(U1F, 1), um)[0]
a0_F = sp.simplify(-2 / U2F.subs(um, um_sol))
umax_F = sp.simplify((um * (1 - th0)).subs(um, um_sol))
ncap_F = sp.simplify(a0_F / umax_F)
P_(f"  C-6    [C] thermal Fermi cell theta = 1/(1+exp(eps0 - d g/T)), U = u_m[theta(g) - theta(0)]:")
P_(f"         A1 => u_m = {um_sol};  A2 => a0 = {a0_F};  u_max = {umax_F};  n_cap = {ncap_F}  (needs theta_0 > 1/2)")
# family test at theta_0 = 3/4 (numeric), and A4 (U' < 1) check
thv = 0.75
dTv = 1.0
umv = float(um_sol.subs({th0: thv, dT: dTv}))
e0v = math.log(1 / thv - 1)
a0v = float(a0_F.subs({th0: thv, dT: dTv}))
UFn = lambda gg: umv * (1 / (1 + np.exp(e0v - dTv * gg)) - thv)
xs = np.logspace(-3, 2.5, 400) * a0v
Uv = UFn(xs)
ncv = float(ncap_F.subs(th0, thv))
famres = np.max(np.abs(((xs - Uv) * (a0v - ncv * Uv) - Uv ** 2) / Uv ** 2))
dUv = np.gradient(Uv, xs)
RES["candidates"]["C-6"] = dict(cls="C", desc="thermal Fermi single cell (displaced along the local field)", A1=True, A2=True,
                                A3=True, A4=bool(np.all(dUv < 1.0001) and np.all(dUv > 0)), n_cap=str(ncap_F),
                                n_cap_at_theta0_0p75=ncv, family_residual_at_0p75=float(famres), in_family=bool(famres < 1e-10),
                                natural=False, free_choices="two scales (d/T, eps0/T): theta_0 free",
                                pass_A1_A4=True, note="n_cap = 2 theta0/(2 theta0 - 1) in (2, inf): free, not picked")
P_(f"         theta_0 = 0.75: n_cap = {ncv:.3f}; family residual max {famres:.2e} -> in-family False; two scales -> NOT natural")

# ======================================================================================================== CLASS D
P_("\n" + "=" * 110 + "\nCLASS D: 1D lattice Pauli capacity (spinless fermions in tight-binding channels along the field)")
tt, nn, aa = sp.symbols("t n a", positive=True)
k_F = sp.pi * nn                                           # spinless, lattice constant a = 1: k_F = pi n
E_band = sp.integrate(-2 * tt * sp.cos(sp.Symbol("k")), (sp.Symbol("k"), -k_F, k_F)) / (2 * sp.pi)
mu = sp.simplify(sp.diff(E_band, nn))
RD = sp.simplify(mu - mu.subs(nn, 0))                    # chemical-potential rise = restoring force (units of R), u = u_m n
RDu = sp.simplify(RD.subs(nn, u / um))
cfD, pD = lead(RDu, u)
a0D = sp.simplify(1 / cfD)
ncapD = sp.simplify(a0D / um)
RmaxD = sp.simplify(RDu.subs(u, um))
dRD = sp.simplify(sp.diff(RDu, u))
P_(f"  D-1    E(n) = {sp.simplify(E_band)};  R(u) = {RDu};  leading {cfD} u^{pD} -> A1 ok (no linear term), A2 fixes a0 = {a0D}")
P_(f"         capacity u_m reached at FINITE g_N = R(u_m) = {RmaxD} (band full, R'(u_m) = {sp.simplify(dRD.subs(u, um))});"
   f" n_cap = a0/u_m = {ncapD}: two scales (t, u_m) -> n free")
RES["candidates"]["D-1"] = dict(cls="D", desc="1D tight-binding Pauli channels along the field", R=str(RDu), A1=True,
                                A2=True, A3=True, A4=True, n_cap=str(ncapD), in_family=False, natural=False,
                                free_choices="two scales (hopping t, capacity u_m)", pass_A1_A4=True,
                                wall="finite-field hard saturation at g_N = 4t (Pauli-blocked band), R bounded",
                                continuum="t fixed, u_m -> inf at fixed a0: R -> u^2/a0 (CFG690 SI law, FAIL)")

# ======================================================================================================== CLASS E
P_("\n" + "=" * 110 + "\nCLASS E: relativistic / Deser-Levin quadrature  g_N = sqrt(g^2 + m^2) - m (Milgrom 1999 Delta-T ansatz)")
m = sp.symbols("m", positive=True)
UE = g + m - sp.sqrt(g ** 2 + m ** 2)
cfE, pE = lead(g - UE, g)
msol = sp.solve(sp.Eq(cfE, 1 / a0), m)[0]
if MUT:
    msol = a0                                               # Mu2: m = a0 instead of a0/2
UE_fixed = sp.simplify(UE.subs(m, msol))
rE1 = classify_U("E-1", "E", UE_fixed, f"Deser-Levin/relativistic dispersion (g_N = kinetic energy of mass m = {msol} at momentum g)",
                 "Milgrom's inertia ~ Delta T ansatz (choice); one scale m", True)
wE = sp.sqrt(g ** 2 + m ** 2) - g
mass_action = sp.simplify(wE * (wE + 2 * g) - m ** 2) == 0
GamE = sp.simplify((2 * (wE + g) / (2 * m)).subs(m, a0 / 2))
RES["candidates"]["E-1"]["mass_action_identity"] = bool(mass_action)
RES["candidates"]["E-1"]["kinetic_rate_ratio"] = str(GamE)
P_(f"         mass-action identity w(w + 2g) = m^2 with w = m - u: {mass_action}; recombination relaxation Gamma/Gamma0 = {GamE}")
RES["candidates"]["E-2"] = dict(cls="E", desc="E-1 with Milgrom's literal dS scale m = a_H: a0_eff = 2 a_H = 2Z a0", A1=True,
                                A2=True, A3=True, A4=True, n_cap="2", in_family=True, natural=True, pass_A1_A4=True,
                                scale_ratio=2 * Z, a0_eff={f: 2 * Z * A0[f] for f in A0},
                                note="equation book (07-16) already records 2cH_Lambda as excluded; re-scored as a control")
P_(f"  E-2    [E] dS scale tie m = a_H: a0_eff = 2Z a0 = {2 * Z:.3f} a0 (equation book: known exclusion; A5 control)")

# ======================================================================================================== CLASS F
P_("\n" + "=" * 110 + "\nCLASS F: reversible critical clipping cells u_c(g) = min(g, c) with capacity spectrum p(c)")
U1law = a0 * g / (a0 + g)
U2law = g + a0 / 2 - sp.sqrt(g ** 2 + a0 ** 2 / 4)


def from_spectrum(pc):
    """U(g) = int_0^g c p dc + g int_g^inf p dc."""
    return sp.simplify(sp.integrate(c * pc, (c, 0, g)) + g * sp.integrate(pc, (c, g, sp.oo)))


TF1 = {}
for name, Ul_, ncap_true in (("n=1", U1law, 1), ("n=2", U2law, 2)):
    pc = sp.simplify(-sp.diff(Ul_, g, 2).subs(g, c))
    norm = sp.simplify(sp.integrate(pc, (c, 0, sp.oo)))
    p0 = sp.simplify(pc.subs(c, 0))
    mean = sp.simplify(sp.integrate(c * pc, (c, 0, sp.oo)))
    ncap = sp.simplify(2 / (p0 * mean))
    Urec = from_spectrum(pc)
    ok = sp.simplify(Urec - Ul_) == 0 and norm == 1 and sp.simplify(p0 - 2 / a0) == 0 and sp.simplify(ncap - ncap_true) == 0
    TF1[name] = dict(p=str(pc), norm=str(norm), p0=str(p0), mean=str(mean), n_cap=str(ncap), reconstructs=bool(ok))
    P_(f"  T-F1 {name}: p(c) = {pc}; int p = {norm}; p(0) = {p0}; <c> = {mean}; n_cap = 2/(p(0)<c>) = {ncap}; U rebuilt: {ok}")
pc1 = sp.simplify(-sp.diff(U1law, g, 2).subs(g, c))
mism_n = sp.simplify(from_spectrum(pc1) - U2law) if MUT else None   # Mu6: spectrum p1 checked against the n=2 law
RES["theorems"]["T-F1"] = TF1
check("T-F1 representation: p = -U'' rebuilds U; A1 <=> int p = 1; A2 <=> p(0) = 2/a0; n_cap = 2/(p(0)<c>)",
      all(v["reconstructs"] for v in TF1.values()))

P_("\n  T-F2 (proof): hazard h = p/S non-decreasing (IFR; every log-concave p) => h(c) >= h(0) = p(0) => S(c) <= exp(-p(0) c)"
   "\n        => <c> = int S <= 1/p(0) => p(0)<c> <= 1 => n_cap = 2/(p(0)<c>) >= 2, equality iff h constant (exponential).")
lam = sp.symbols("lambda", positive=True)
pexp = lam * sp.exp(-lam * c)
eq_case = sp.simplify(pexp.subs(c, 0) * sp.integrate(c * pexp, (c, 0, sp.oo)))
P_(f"        equality case exponential: p(0)<c> = {eq_case}")


def spec_stats(pdf, cmax=np.inf):
    """numeric p(0)<c>, hazard monotonicity (non-decreasing?) on a grid."""
    norm = integrate.quad(pdf, 0, cmax, limit=200)[0]
    mean = integrate.quad(lambda cc: cc * pdf(cc), 0, cmax, limit=200)[0] / norm
    p0 = pdf(0.0) / norm
    hi = (cmax if np.isfinite(cmax) else 30.0) * (0.999 if np.isfinite(cmax) else 1.0)
    cs = np.linspace(0, hi, 400)
    S = np.array([integrate.quad(pdf, cc, cmax, limit=200)[0] / norm for cc in cs])
    h = np.array([pdf(cc) / norm for cc in cs]) / np.maximum(S, 1e-300)
    m_ = S > 1e-8
    ifr = bool(np.all(np.diff(h[m_]) >= -1e-9 * np.max(h[m_])))
    return p0 * mean, ifr


SPECS = {
    "exponential": (lambda cc: math.exp(-cc), np.inf),
    "half-normal": (lambda cc: math.exp(-cc * cc / 2), np.inf),
    "uniform[0,1]": (lambda cc: 1.0, 1.0),
    "half-logistic": (lambda cc: 2 * math.exp(-cc) / (1 + math.exp(-cc)) ** 2, np.inf),
    "Beta(1,3)": (lambda cc: 3 * (1 - cc) ** 2, 1.0),
    "half-exp-power(4)": (lambda cc: math.exp(-cc ** 4), np.inf),
}
TF2 = {}
for k_, (pdf, cm) in SPECS.items():
    pm, ifr = spec_stats(pdf, cm)
    TF2[k_] = dict(p0_mean=pm, IFR=ifr, n_cap=2 / pm, bound_ok=bool((not ifr) or pm <= 1 + 1e-9))
    P_(f"        {k_:18s}: IFR {ifr}, p(0)<c> = {pm:.5f}, n_cap = {2 / pm:.4f}")
pmL, ifrL = spec_stats(lambda cc: 2 / (1 + cc) ** 3)
pmT, ifrT = spec_stats(lambda cc: 0.25 / (cc * cc + 0.25) ** 1.5)
P_(f"        Lomax(2) [n=1 spectrum] : IFR {ifrL}, p(0)<c> = {pmL:.5f}, n_cap = {2 / pmL:.4f}  (decreasing hazard)")
P_(f"        half-t2  [n=2 spectrum] : IFR {ifrT}, p(0)<c> = {pmT:.5f}, n_cap = {2 / pmT:.4f}")
RES["theorems"]["T-F2"] = dict(spectra=TF2, lomax=dict(p0_mean=pmL, IFR=ifrL), half_t2=dict(p0_mean=pmT, IFR=ifrT),
                               statement="IFR (incl. log-concave) capacity spectra give n_cap >= 2 (= 2 only for the exponential);"
                                         " the action's n = 1 needs a decreasing-hazard spectrum with a c^-3 tail")
check("T-F2 bound holds on all 6 IFR spectra (and all 6 are IFR)", all(v["bound_ok"] and v["IFR"] for v in TF2.values()))

P_("\n  Natural spectra (scale fixed by A2: p(0) = 2/a0):")
sig = a0 / sp.sqrt(2 * sp.pi)
UF1 = sp.simplify(from_spectrum((2 / a0) * sp.exp(-2 * c / a0)))
classify_U("F-1", "F", UF1, "exponential spectrum (MaxEnt at fixed <c>)", "MaxEnt constraint <c>", True)
UF2 = g * sp.erfc(g / (sig * sp.sqrt(2))) + sig * sp.sqrt(2 / sp.pi) * (1 - sp.exp(-g ** 2 / (2 * sig ** 2)))
pF2 = sp.sqrt(2 / sp.pi) / sig * sp.exp(-c ** 2 / (2 * sig ** 2))
chkF2 = sp.simplify(sp.diff(UF2, g, 2) + pF2.subs(c, g)) == 0 and sp.simplify(pF2.subs(c, 0) - 2 / a0) == 0
classify_U("F-2", "F", UF2, "half-normal spectrum (MaxEnt at fixed <c^2>)", "MaxEnt constraint <c^2>", True)
RES["candidates"]["F-2"]["U_matches_spectrum"] = bool(chkF2)
P_(f"         F-2 closed form matches -U'' = p and p(0) = 2/a0: {chkF2}")
# F-3 uniform on [0, a0/2] (piecewise): U = g - g^2/a0 for g <= a0/2, a0/4 beyond
RES["candidates"]["F-3"] = dict(cls="F", desc="uniform spectrum on [0, c_max], c_max = a0/2", U="g - g^2/a0 (g<=a0/2); a0/4 beyond",
                                A1=True, A2=True, A3=True, A4=True, u_max="a0/4", n_cap="4", n1="2", in_family=False,
                                natural=True, free_choices="flat bounded spectrum", pass_A1_A4=True,
                                wall="finite-field hard saturation at g = a0/2 (g_N = a0/4); beyond: g_N = g - a0/4 exactly")
gq = sp.symbols("gq", positive=True)
Uq = gq - gq ** 2 / a0
b3q = sp.series(Uq, gq, 0, 4).removeO().coeff(gq, 3)
P_(f"  F-3    [F] uniform spectrum: U = g - g^2/a0 up to g = a0/2, then a0/4: A1 ok, A2 ok, u_max = a0/4 (n_cap = 4), "
   f"n1 = {2 - b3q * a0 ** 2}; finite-field saturation; not in family")
RES["candidates"]["F-4"] = dict(cls="F", desc="identical cells (delta spectrum at c0)", U="min(g, c0)", A1=True, A2=False, A3=True,
                                A4=False, pass_A1_A4=False, in_family=False, natural=True, free_choices="c0",
                                note="p(0) = 0: g_N = 0 below c0 (no restoring force, no deep law)")
P_("  F-4    [F] identical cells U = min(g, c0): g_N = 0 for g < c0 -> A2 FAIL (p(0) = 0; no deep law at all)")
# F-5 superstatistics (by construction)
r_, tau = sp.symbols("r tau", positive=True)
lomax = sp.simplify(sp.integrate(r_ * sp.exp(-r_ * c) * a0 ** 2 * r_ * sp.exp(-r_ * a0), (r_, 0, sp.oo)))
ss1 = sp.simplify(lomax - pc1) == 0
lam2 = a0 ** 2 / 8
halft = sp.simplify(sp.integrate(sp.sqrt(2 * tau / sp.pi) * sp.exp(-tau * c ** 2 / 2) * lam2 * sp.exp(-lam2 * tau), (tau, 0, sp.oo)))
pc2 = sp.simplify(-sp.diff(U2law, g, 2).subs(g, c))
ss2 = sp.simplify(halft - pc2) == 0
RES["candidates"]["F-5"] = dict(cls="F", desc="in-family spectra as superstatistics", natural=False, by_construction=True,
                                n1_exponential_with_Gamma2_rate=bool(ss1), n2_halfnormal_with_exponential_precision=bool(ss2),
                                pass_A1_A4=True, in_family=True,
                                note="mixing shape (Gamma shape 2 / precision Gamma shape 1) chosen to hit the family")
P_(f"  F-5    [F] superstatistics (by construction): Lomax(2) = Exp(c; r) with r ~ Gamma(2, rate a0): {ss1};  "
   f"half-t2 = half-normal with precision ~ Exp(rate a0^2/8): {ss2}")

# ======================================================================================================== second predictions
P_("\n" + "=" * 110 + "\nSECOND PREDICTIONS (a0 = 1 units; S-a also in Msun/pc^2) for the fixed-number A1-A4 passers")
sg = 1 / math.sqrt(2 * math.pi)
mE = 1.0 if MUT else 0.5                                   # Mu2 propagated: n=2 law built with m = a0
LAWS = {   # name: (U, U' in a numerically stable form, u_max, wall)
    "C-1 (n=1)": (lambda x: x / (1 + x), lambda x: 1 / (1 + x) ** 2, 1.0, "simple pole"),
    "E-1 (n=2)": (lambda x: x + mE - np.sqrt(x * x + mE * mE),
                  lambda x: mE * mE / (np.sqrt(x * x + mE * mE) * (np.sqrt(x * x + mE * mE) + x)), mE, "simple pole"),
    "F-1 exp": (lambda x: -0.5 * np.expm1(-2 * x), lambda x: np.exp(-2 * x), 0.5, "log"),
    "F-2 half-normal": (lambda x: x * special.erfc(x / (sg * math.sqrt(2))) + sg * math.sqrt(2 / math.pi) * (-np.expm1(-x * x / (2 * sg * sg))),
                        lambda x: special.erfc(x / (sg * math.sqrt(2))), 1 / math.pi, "sub-log (Gaussian tail)"),
    "F-3 uniform": (lambda x: np.where(x <= 0.5, x - x * x, 0.25), lambda x: np.where(x <= 0.5, 1 - 2 * x, 0.0), 0.25,
                    "finite-field saturation"),
}
SP = {}
for nm, (Uf, dUf, umx, wall) in LAWS.items():
    rec = {"u_max_over_a0": umx, "n_cap": 1 / umx, "wall": wall,
           "Sigma_max_Msun_pc2": {f: umx * A0[f] / (math.pi * G_SI) / (MSUN / PC ** 2) for f in A0}}
    tailf = lambda xx: integrate.quad(lambda cc: float(dUf(np.array(cc))), xx, np.inf, limit=400, epsabs=0, epsrel=1e-10)[0]
    rec["tail"] = {str(xx): float(tailf(xx)) for xx in (3.0, 10.0)}
    rec["gap_Rprime"] = {str(xx): (float(1 / dUf(np.array(xx)) - 1) if float(dUf(np.array(xx))) > 0 else float("inf"))
                         for xx in (0.1, 1.0, 10.0)}
    # S-e: g_N where u = 0.99 u_max
    gg = optimize.brentq(lambda x: float(Uf(np.array(x))) - 0.99 * umx, 1e-9, 1e4)
    rec["gN_at_99pct"] = float(gg - Uf(np.array(gg)))
    # tail form: local log-slope of (u_max - U) between x = 10 and 20
    t10, t20 = rec["tail"]["10.0"], float(tailf(20.0))
    rec["tail_logslope_10_20"] = float(math.log(t20 / t10) / math.log(2)) if t10 > 0 and t20 > 0 else "zero (saturated)"
    SP[nm] = rec
    P_(f"  {nm:16s} u_max {umx:.4f} a0 (Sigma_max {rec['Sigma_max_Msun_pc2']['canonical']:.0f}/{rec['Sigma_max_Msun_pc2']['alt']:.0f}"
       f" Msun/pc^2) | tail x=3 {rec['tail']['3.0']:.3e} x=10 {rec['tail']['10.0']:.3e} slope {rec['tail_logslope_10_20']}"
       f" | gap R' x=0.1/1/10 = {rec['gap_Rprime']['0.1']:.4g}/{rec['gap_Rprime']['1.0']:.4g}/{rec['gap_Rprime']['10.0']:.4g}"
       f" | g_N(99%) {rec['gN_at_99pct']:.3g} | wall {wall}")
SP["C-1 (n=1)"]["kinetic_Gamma_ratio"] = {str(xx): 1 + xx for xx in (0.1, 1.0, 10.0)}
SP["E-1 (n=2)"]["kinetic_Gamma_ratio"] = {str(xx): math.sqrt(1 + 4 * xx * xx) for xx in (0.1, 1.0, 10.0)}
P_(f"  S-d kinetic Gamma(x)/Gamma(0) x=0.1/1/10: Langmuir (n=1) {[round(1 + xx, 4) for xx in (0.1, 1, 10)]}; "
   f"mass action (n=2) {[round(math.sqrt(1 + 4 * xx * xx), 4) for xx in (0.1, 1, 10)]}")
SP["scale"] = {"C-5 a0_eff/a0": Z, "E-2 a0_eff/a0": 2 * Z}
P_(f"  S-f scale: Unruh-Langmuir a0_eff/a0 = Z = {Z:.4f}; Deser-Levin literal a0_eff/a0 = 2Z = {2 * Z:.4f} (both footings)")


# static-law minimax |Delta log10 g| at fixed g_N over y = g_N/a0 in [0.01, 100], free a0 rescale of the second law
def g_of_gN(Uf, umx, y):
    lo, hi = y.copy(), y + umx + 1e-12
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f = mid - Uf(mid) - y
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    return 0.5 * (lo + hi)


yy = np.logspace(-2, 2, 400)
GL = {nm: g_of_gN(v[0], v[2], yy) for nm, v in LAWS.items()}
MM = {}
names = list(LAWS)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        A_, B_ = names[i], names[j]
        UfB, umB = LAWS[B_][0], LAWS[B_][2]

        def mx(ls):
            sc = 10 ** ls
            gB = sc * g_of_gN(UfB, umB, yy / sc)
            return float(np.max(np.abs(np.log10(GL[A_]) - np.log10(gB))))
        r0 = mx(0.0)
        opt = optimize.minimize_scalar(mx, bounds=(-0.5, 0.5), method="bounded", options=dict(xatol=1e-6))
        MM[f"{A_} | {B_}"] = dict(no_rescale=r0, minimax=float(opt.fun), log10_rescale=float(opt.x))
        P_(f"  static |dlog g| {A_:16s} vs {B_:16s}: raw {r0:.4f} dex; after a0 rescale x10^{opt.x:+.4f}: {opt.fun:.4f} dex")
SP["static_minimax"] = MM
RES["second_predictions"] = SP

# ======================================================================================================== reported extras
P_("\nREPORTED (no verdict weight)")
# (i) is criticality automatic in the medium's own structure, or a tuned linear susceptibility?
AUTO = {"A-*": "tuned (amplitude solved for U'(0) = 1)", "C-1": "tuned (u_m = beta/alpha)",
        "C-3b1": "tuned (mobility normalised to 1)", "C-6": "tuned (u_m solved)",
        "D-1": f"automatic (band bottom: R'(0) = {sp.limit(sp.diff(RDu, u), u, 0, '+')})",
        "E-1": f"automatic (kinetic energy has no linear term: d/dg[sqrt(g^2+m^2) - m] at 0 = "
               f"{sp.limit(sp.diff(sp.sqrt(g ** 2 + m ** 2) - m, g), g, 0, '+')})",
        "F-*": "normalisation (every cell critical: int p = 1)"}
RES["criticality_origin"] = AUTO
for k_, v_ in AUTO.items():
    P_(f"  criticality {k_:6s}: {v_}")
# (ii) the whole capacity family as an M/M/1 mean queue length: R_n = (u_m^2/a0) rho^2/(1 - rho), rho = u/u_m, u_m = a0/n
nq = sp.symbols("n", positive=True)
rho = u / (a0 / nq)
TQ = sp.simplify(((a0 / nq) ** 2 / a0) * rho ** 2 / (1 - rho) - u ** 2 / (a0 - nq * u)) == 0
RES["theorems"]["T-Q"] = dict(identity=bool(TQ), statement="R_n(u) = (u_max^2/a0) L_q(rho), L_q = rho^2/(1-rho) (M/M/1), "
                                                           "rho = u/u_max: n = a0/u_max is the ratio of force scale to capacity, "
                                                           "not fixed by the queue")
P_(f"  T-Q  R_n(u) == (u_max^2/a0) rho^2/(1-rho), rho = u/u_max (M/M/1 mean queue length), for every n: {TQ}")

# ======================================================================================================== MUTATE / verdict hand-off
if MUT:
    c1 = RES["candidates"]["C-1"]
    e1 = RES["candidates"]["E-1"]
    # Mu3: family test on C-1 at n_cap + 1 (built from the unmutated Langmuir law)
    resid_mu3 = sp.simplify((g - U1law) * (a0 - 2 * U1law) - U1law ** 2)
    # Mu4: the T-A analyticity test applied to C-1's law must report NON-analytic (theorem does not fire)
    an_c1, ex_c1 = chi_is_analytic(U1law)
    # Mu7: Lomax(2) is not IFR and gives n_cap < 2
    bites = dict(Mu1=not (c1["A1"] and c1["A2"]), Mu2=not e1["A2"], Mu3=resid_mu3 != 0, Mu4=not an_c1,
                 Mu6=mism_n != 0, Mu7=(not ifrL) and (2 / pmL < 2))
    RES["mutate_bites"] = {k: bool(v) for k, v in bites.items()}
    P_(f"\nMUTATE: {RES['mutate_bites']}  (Mu3 residual {resid_mu3}; Mu4 chi exponents {ex_c1}; Mu6 U(p1) - U2 = {mism_n})")
    rc = 1 if all(bites.values()) else 0
else:
    ok_all = all(v["ok"] for v in RES["checks"].values())
    passers = [k for k, v in RES["candidates"].items() if v.get("pass_A1_A4")]
    RES["A1_A4_passers"] = passers
    P_(f"\nA1-A4 passers: {passers}")
    P_("A5 (raw SPARC) and the verdict: ag6b_sparc.py")
    rc = 0 if ok_all else 1
json.dump(RES, open(os.path.join(HERE, f"ag6b_media_results{TAG}.json"), "w"), indent=1, default=str)
OUT.close()
sys.exit(rc)
