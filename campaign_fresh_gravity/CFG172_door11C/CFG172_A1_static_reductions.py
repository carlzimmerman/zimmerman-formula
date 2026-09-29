# -*- coding: utf-8 -*-
"""CFG172 A1 -- static spherical reductions of 11C-a/-b/-c and G1 (law, mechanism).  Frozen: CFG172_FROZEN_CRITERIA.md sec. 1.3, 1.4, 2.
sympy: weak-field Lagrangian -> Euler-Lagrange (Psi = Phi; first integral r^2 mu Phi' = G M(<r)); q(y) for the declared kernels;
numpy/scipy: G1-law over x in [0.1,30], 7 masses, point mass + exponential sphere h = 2 kpc, both footings, kernels P2 (CFG44, primary),
nu_mono, simple (the brief's 1/2+sqrt(1/4+1/y), NOT CFG44's P2).  Pass line 0.10.
MUTATE = M1 (flow scale 3 a0, target unchanged) | M2 (kernel -> GR, q = 0) | M3 (q -> -q); each must make G1-law FAIL (exit 1)."""
import sympy as sp
from cfg172_common import *

R = Run("CFG172_A1_static_reductions")
mut = R.mut

# ---- sympy: reduction ------------------------------------------------------------------------------------------------
r = sp.symbols("r", positive=True)
Gs, rho = sp.symbols("G rho", positive=True)
Phi, Psi = sp.Function("Phi")(r), sp.Function("Psi")(r)
ell = sp.Function("ell")
s = sp.diff(Phi, r) ** 2
# per 1/(8 pi G): L = r^2 [ Psi'^2 - 2 Phi' Psi' + ell(Phi'^2) ] - 8 pi G r^2 rho Phi
L = r ** 2 * (sp.diff(Psi, r) ** 2 - 2 * sp.diff(Phi, r) * sp.diff(Psi, r) + ell(s)) - 8 * sp.pi * Gs * r ** 2 * rho * Phi
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L, [Phi, Psi], r)
eqPsi = sp.simplify(eqs[1].lhs)
# Psi equation: d/dr[ r^2 (2Psi' - 2Phi') ] = 0  -> with regularity r^2 (Psi'-Phi') = 0
chk_psi = sp.simplify(eqPsi - (-sp.diff(r ** 2 * (2 * sp.diff(Psi, r) - 2 * sp.diff(Phi, r)), r)))
R.check("S1 Psi equation is d/dr[r^2 (Psi'-Phi')] = 0 => Psi' = Phi' (gamma = 1, no flow source in the g_ij equation)", str(chk_psi), chk_psi == 0)
# Phi equation with Psi'=Phi'
eqPhi = eqs[0].lhs.subs(Psi, Phi).doit()
qexpr = sp.Function("q")
# ell'(s) = q  =>  Phi eq: 2 d/dr[ r^2 (1 - ell') Phi' ] - 8 pi G r^2 rho = 0 (sign to be checked)
target = 2 * sp.diff(r ** 2 * (1 - sp.Subs(sp.diff(ell(sp.Symbol('S')), sp.Symbol('S')), sp.Symbol('S'), s)) * sp.diff(Phi, r), r) - 8 * sp.pi * Gs * r ** 2 * rho
d = sp.simplify(sp.expand(eqPhi + target))
d2 = sp.simplify(sp.expand(eqPhi - target))
R.check("S2 Phi equation reduces to d/dr[ r^2 (1 - ell') Phi' ] = 4 pi G r^2 rho (Euler-Lagrange, Psi=Phi)", f"|E+T|={d}, |E-T|={d2}", (d == 0) or (d2 == 0))

# ---- q(y) for the declared kernels, symbolic for true P2 ---------------------------------------------------------------
y = sp.symbols("y", positive=True)
mu_P2 = (sp.sqrt(1 + 4 * y ** 2) - 1) / (2 * y)          # g_N = a0 (sqrt(1+4y^2)-1)/2 from g^2 = g_N^2 + a0 g_N
q_P2 = sp.simplify(1 - mu_P2)
# check: mu(y_g) y_g = y_N and y_g = nu(y_N) y_N
yN = sp.symbols("yN", positive=True)
res = sp.simplify(sp.simplify((mu_P2 * y).subs(y, sp.sqrt(yN ** 2 + yN)) - yN).subs(sp.sqrt(4 * yN ** 2 + 4 * yN + 1), 2 * yN + 1))
R.check("S3 true P2: mu(y_g) = (sqrt(1+4y^2)-1)/(2y) satisfies mu*y_g = y_N at y_g = sqrt(y_N^2+y_N)", str(res), res == 0)
Q_P2 = sp.integrate(sp.simplify(2 * y * q_P2), y)         # d Q/d(y^2) = q  <=> dQ/dy = 2 y q
dQ = sp.simplify(sp.diff(Q_P2, y) - 2 * y * q_P2)
R.check("S4 flow term Q(y) for true P2 has dQ/dy = 2 y q(y)  (so dQ/d(y^2) = q)", f"Q(y)={Q_P2}", dQ == 0)
mu_S = y / (1 + y); q_S = 1 - mu_S
R.check("S5 simple-nu: q = 1/(1+y), Q = 2[y - ln(1+y)]", str(sp.simplify(sp.diff(2 * (y - sp.log(1 + y)), y) - 2 * y * q_S)), sp.simplify(sp.diff(2 * (y - sp.log(1 + y)), y) - 2 * y * q_S) == 0)
qP2f = sp.lambdify(y, q_P2, "numpy")
qSf = sp.lambdify(y, q_S, "numpy")
# (yq)' for true P2 and simple: positivity
yqp = sp.simplify(sp.diff(y * q_P2, y))
R.check("S6 (y q)' for true P2 = 1 - 2y/sqrt(1+4y^2) > 0 for all y (radially stable kinetic sign, decoupling limit; A2 derives it)", str(yqp), sp.simplify(yqp - (1 - 2 * y / sp.sqrt(1 + 4 * y ** 2))) == 0)

# ---- controls C1 (CFG44 identities at the P2 point mass, extended profile) -------------------------------------------------
worst = 0.0
for M in MASSES:
    for f in FOOT:
        a0 = A0[f]
        r_, gN = profile_gN(M, "point", a0)
        x = r_ / rM_kpc(M, a0)
        g = nu_p2(gN / a0) * gN
        worst = max(worst, float(np.max(np.abs(g / np.sqrt(gN ** 2 + a0 * gN) - 1))))
        Mc = M * (np.sqrt(1 + x ** 2) - 1)                       # dynamical mass minus baryons
        Mdyn = g * r_ ** 2 / G
        worst = max(worst, float(np.max(np.abs((Mdyn - M) / Mc - 1))))
R.check("C1a CFG44 P2 point-mass identities g = sqrt(gN^2+a0 gN), M_c = M(sqrt(1+x^2)-1) (all masses, footings)", f"max rel dev {worst:.2e}", worst < 1e-9)
prof = BC.exp_sphere(1e11, H_EXP)
rr = np.linspace(0.5, 30, 40)
d1 = float(np.max(np.abs(prof.u(rr) / G / M_enc_exp(1e11, rr) - 1)))
R.check("C1b exponential sphere enclosed mass equals Bcommon.exp_sphere (read-only import)", f"max rel dev {d1:.2e}", d1 < 1e-6)

# ---- G1-law numerics ------------------------------------------------------------------------------------------------------
def qfun_for(kernel):
    if kernel == "P2":
        f = lambda yg: qP2f(np.asarray(yg, float))
    elif kernel == "simple":
        f = lambda yg: qSf(np.asarray(yg, float))
    else:
        cache = {}
        # numeric inversion for nu_mono, tabulated
        ygs = np.logspace(-8, 8, 4001)
        qs = q_of_yg(nu_mono, ygs)
        f = lambda yg: np.interp(np.log10(np.asarray(yg, float)), np.log10(ygs), qs)
    return f


def solve_flow(qf, yN, scale=1.0, sign=1.0, gr=False):
    """solve mu(y_g) y_g = y_N with mu = 1 - sign*q(y_g/scale...) ; the flow's own scale is scale*a0 (mutations)."""
    out = np.empty_like(yN)
    for i, yn in enumerate(yN):
        if gr:
            out[i] = yn
            continue
        fn = lambda ly: (1.0 - sign * float(qf(math.exp(ly) / scale))) * math.exp(ly) - yn
        try:
            out[i] = math.exp(brentq(fn, math.log(yn) - 30, math.log(yn) + 30, xtol=1e-13))
        except ValueError:
            out[i] = np.nan
    return out


sc = 3.0 if mut == "M1" else 1.0
sg = -1.0 if mut == "M3" else 1.0
gr = mut == "M2"
table = {}
for kern in ("P2", "nu_mono", "simple"):
    qf = qfun_for(kern)
    nu_t = KERNELS[kern]
    mx = 0.0
    for f in FOOT:
        a0 = A0[f]
        for prof_name in ("point", "exp"):
            for M in MASSES:
                r_, gN = profile_gN(M, prof_name, a0)
                yN = gN / a0
                yg = solve_flow(qf, yN, sc, sg, gr)
                g_flow = yg * a0
                g_tar = nu_t(yN) * gN
                dev = np.nanmax(np.abs(g_flow / g_tar - 1)) if not np.all(np.isnan(g_flow)) else np.inf
                mx = max(mx, dev)
                table[f"{kern}/{f}/{prof_name}/{M:.0e}"] = float(dev)
    table[f"MAX/{kern}"] = float(mx)
    P(f"  kernel {kern:8s}: max |g_flow/g_target - 1| over grid, masses, profiles, footings = {mx:.3e}")
worstP2 = table["MAX/P2"]
R.out["numbers"]["G1_max_dev"] = {k: v for k, v in table.items() if k.startswith("MAX")}
g1 = worstP2 <= 0.10
if not mut:
    R.check("G1a algebraic law reproduces the P2 target within 1e-6 (own solve from the symbolic q, not the kernel itself)", f"{worstP2:.2e}", worstP2 < 1e-6)
    # flux (first integral) residual for the extended sphere: (1/r^2) d(r^2 mu g)/dr = 4 pi G rho
    a0 = A0["canonical"]; M = 1e11
    r_, gN = profile_gN(M, "exp", a0)
    yg = solve_flow(qfun_for("P2"), gN / a0)
    g = yg * a0
    mu = gN / g
    flux = r_ ** 2 * mu * g
    lhs = np.gradient(flux, r_) / r_ ** 2
    rhs = 4 * math.pi * G * rho_exp(M, r_)
    sel = (r_ < 20.0)
    resid = float(np.max(np.abs(lhs[sel][3:-3] - rhs[sel][3:-3])) / np.max(rhs[sel]))
    R.check("G1b field equation d(r^2 mu g)/dr = 4 pi G r^2 rho holds for the exponential sphere (finite difference, 1e11)", f"max |resid|/max(rhs) over r<20 kpc {resid:.2e}", resid < 5e-3)
R.verdict("G1-law", "PASS" if g1 else "FAIL", f"max dev (P2 target) = {worstP2:.3e} (pass line 0.10)")
R.verdict("G1-mechanism", "P-declared" if g1 else "FAIL",
          "the flow function (q, Q) is set to the target's kernel by declaration (menu written knowing the target); nothing in rule T fixes q(y); M2 (derived kernel) NOT achieved")
R.out["numbers"]["dev_between_kernels"] = None
# how far apart are the declared kernels themselves (sensitivity: the P2/simple/nu_mono target functions)
yy = np.logspace(-3, 2, 400)
R.out["numbers"]["nu_ratio_simple_over_P2_range"] = [float(np.min(nu_simple(yy) / nu_p2(yy))), float(np.max(nu_simple(yy) / nu_p2(yy)))]
R.out["numbers"]["nu_ratio_mono_over_P2_range"] = [float(np.min(nu_mono(yy) / nu_p2(yy))), float(np.max(nu_mono(yy) / nu_p2(yy)))]
P("  nu_simple/nu_P2 range:", R.out["numbers"]["nu_ratio_simple_over_P2_range"], " nu_mono/nu_P2:", R.out["numbers"]["nu_ratio_mono_over_P2_range"])
R.finish(bite=(mut != "" and not g1))
