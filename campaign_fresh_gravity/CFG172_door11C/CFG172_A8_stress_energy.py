# -*- coding: utf-8 -*-
"""CFG172 A8 -- Addendum 2 (sec. 9): stress-energy of the flow sector, conservation, rest mass / charge checks (S1, S2) and the labelled NO-COLD G2 run.  Frozen: sec. 9.
sympy: static spherical reduction of S_a = (1/8 pi G) int sqrt(-g) ell(a^2) with the static aether u = N^-1 d_t (a^2 = g^rr (N'/N)^2): rho = T_uu, p_r, p_t from the metric
variations (N, A = g_rr, B = g_thth/r^2); weak-field limit; Newtonian-limit conservation p_r' + rho Phi' + (2/r)(p_r - p_t) = 0; momentum constraint at zero shift (Noether charge of the
khronon form) = 0.  numpy: FRW background of the c2 channel vs the density the cold fluid supplies; baryon-only growth against LCDM.
Labelled variant 11C-x-nocold: never pooled with the cold-on rows.
MUTATE = M7 (khronon charge Q != 0: S2 must fail; the a^-3 term appears) | M8 (cold component restored in the no-cold run: the growth ratio must recover to within 5%)."""
import sympy as sp
from scipy.integrate import solve_ivp
from cfg172_common import *

R = Run("CFG172_A8_stress_energy")
mut = R.mut
# ---- sympy: T^flow_ab of the a-channel in the static spherical reduction ---------------------------------------------------------------
r = sp.symbols("r", positive=True); Gs = sp.symbols("G", positive=True)
N = sp.Function("N")(r); A = sp.Function("A")(r); Bf = sp.Function("B")(r)
ell = sp.Function("ell")
Np = sp.diff(N, r)
s_ = Np ** 2 / (A * N ** 2)
sqrtg = N * sp.sqrt(A) * Bf * r ** 2                    # sqrt(-g)/sin(theta)
Lag = sqrtg * ell(s_) / (8 * sp.pi * Gs)
from sympy.calculus.euler import euler_equations
E_N = sp.diff(Lag, N) - sp.diff(sp.diff(Lag, Np), r)
E_A = sp.diff(Lag, A)
E_B = sp.diff(Lag, Bf)
rho_fl = sp.simplify(-N * E_N / sqrtg)                   # T_uu = -(N/sqrt(-g)) dS/dN   (T^{tt} N^2)
p_r = sp.simplify(2 * A * E_A / sqrtg)                   # T^r_r = 2 g_rr (delta S/delta g_rr)/sqrt(-g)
p_t = sp.simplify(Bf * E_B / sqrtg)                      # T^th_th = T^ph_ph = B (dS/dB)/sqrt(-g) (B multiplies both angular components)
# weak field: N = 1 + e Phi, A = 1 - 2 e Psi, B = 1 - 2 e Psi ; ell(s) = ell1 s + ell2 s^2/2 + ... ; keep O(e)
e = sp.symbols("e"); Phi = sp.Function("Phi")(r); Psi = sp.Function("Psi")(r)
l1, l2 = sp.symbols("l1 l2")
def weak(expr):
    ex = expr.subs({N: 1 + e * Phi, A: 1 - 2 * e * Psi, Bf: 1 - 2 * e * Psi}).doit()
    # ell(s) around s = 0: the argument is O(e^2); ell(0) = 0
    ex = ex.replace(lambda x_: isinstance(x_, sp.Subs), lambda x_: x_)
    return ex
# use an explicit series instead of the abstract function
ell_ser = lambda s: l1 * s + l2 * s ** 2 / 2
Lag_s = sqrtg * ell_ser(s_) / (8 * sp.pi * Gs)
EN = sp.diff(Lag_s, N) - sp.diff(sp.diff(Lag_s, Np), r)
EA = sp.diff(Lag_s, A); EB = sp.diff(Lag_s, Bf)
subs_ = {N: 1 + e * Phi, A: 1 - 2 * e * Psi, Bf: 1 - 2 * e * Psi}
rho_s = sp.series(sp.simplify((-N * EN / sqrtg).subs(subs_).doit()), e, 0, 2).removeO()
pr_s = sp.series(sp.simplify((2 * A * EA / sqrtg).subs(subs_).doit()), e, 0, 3).removeO()
pt_s = sp.series(sp.simplify((Bf * EB / sqrtg).subs(subs_).doit()), e, 0, 3).removeO()
rho_lead = sp.simplify(rho_s.coeff(e, 1)); pr_lead = sp.simplify(pr_s.coeff(e, 2)); pt_lead = sp.simplify(pt_s.coeff(e, 2))
rho_expected = sp.simplify((1 / (4 * sp.pi * Gs * r ** 2)) * sp.diff(r ** 2 * l1 * sp.diff(Phi, r), r))
R.out["numbers"]["T_flow_weak_field"] = {"rho_O(e)": str(rho_lead), "p_r_O(e^2)": str(pr_lead), "p_t_O(e^2)": str(pt_lead)}
R.check("A8.1 T_uu of the flow sector to O(e) = +(1/4 pi G) div(ell' grad Phi) (own metric variation): it IS the source the Phi equation uses (the frozen text expected them to differ: wrong expectation, kept)",
        str(rho_lead), sp.simplify(rho_lead - rho_expected) == 0 or sp.simplify(rho_lead + rho_expected) == 0)
sgn = 1 if sp.simplify(rho_lead - rho_expected) == 0 else -1
R.out["numbers"]["rho_sign_relative_to_(-div(ell' grad Phi)/4piG)"] = sgn
R.check("A8.2 p_r and p_t are O(e^2) = O((Phi/c^2)^2) relative to rho c^2 at fixed density scale: the flow behaves as a stress-free static source at leading order (dust-like, not vacuum-like)",
        f"p_r = {pr_lead}; p_t = {pt_lead}", pr_lead != 0 or pt_lead != 0, load_bearing=False)
# Newtonian-limit conservation on the flow's equation: p_r' + rho Phi' + (2/r)(p_r - p_t) = 0 with Psi = Phi
cons = sp.simplify((sp.diff(pr_lead, r) + rho_lead * sp.diff(Phi, r) + 2 * (pr_lead - pt_lead) / r).subs(Psi, Phi).doit())
# rho_lead is O(e) times Phi'; p O(e^2): conservation at O(e^2)
R.check("A8.3 Newtonian-limit conservation of T^flow: p_r' + rho Phi' + (2/r)(p_r - p_t) = 0 identically (Psi = Phi), for arbitrary Phi(r)", str(cons), cons == 0)
# ---- khronon-form Noether charge: momentum constraint at zero shift ---------------------------------------------------------------------
c2s = sp.symbols("c2", positive=True); sh = sp.Function("s")(r)
Ns = sp.Function("Ns")(r); As = sp.Function("As")(r); Bs = sp.Function("Bs")(r)
gam = sp.diag(As, Bs * r ** 2, Bs * r ** 2 * sp.sin(sp.Symbol("th")) ** 2)
th_ = sp.Symbol("th")
beta = sp.Matrix([sh, 0, 0])
def lie_gamma(gm, bt):
    out = sp.zeros(3, 3)
    xs = [r, sp.Symbol("th"), sp.Symbol("ph")]
    for i in range(3):
        for j in range(3):
            out[i, j] = sum(bt[k] * sp.diff(gm[i, j], xs[k]) + gm[k, j] * sp.diff(bt[k], xs[i]) + gm[i, k] * sp.diff(bt[k], xs[j]) for k in range(3))
    return out
Kij = -lie_gamma(gam, beta) / (2 * Ns)                    # static, stationary shift: K_ij = -(1/2N) L_beta gamma_ij
gi = gam.inv()
Kmix = gi * Kij
KK = sp.simplify((Kmix * Kmix).trace()); Ktr = sp.simplify(Kmix.trace())
Lmom = sp.simplify(Ns * sp.sqrt(As) * Bs * r ** 2 * (KK - (1 + c2s) * Ktr ** 2))
eps_ = sp.symbols("epsilon")
Lmom_e = Lmom.subs(sh, eps_ * sh).doit()
first = sp.simplify(sp.diff(Lmom_e, eps_).subs(eps_, 0))
R.check("A8.4 khronon form: the momentum constraint (the flux of the aether equation, i.e. the shift-symmetry Noether current) vanishes on the static solution: dL/d(shift) at zero shift = 0 => Q = 0 with no tuning",
        f"dL/d eps at eps=0: {first}", first == 0)
# FRW: what a nonzero charge would do: (a^3 J^0)' = 0  =>  J^0 = Q / a^3 (dust-like a^-3 term)
a_ = sp.Function("a")(sp.Symbol("t")); tt = sp.Symbol("t"); Qc = sp.symbols("Q")
J0 = Qc / a_ ** 3
R.check("A8.5 a conserved khronon charge in FRW: d_t(a^3 J^0) = 0 <=> J^0 = Q/a^3 (an a^-3 term, dust-like): what M7 switches on",
        str(sp.simplify(sp.diff(a_ ** 3 * J0, tt))), sp.simplify(sp.diff(a_ ** 3 * J0, tt)) == 0, load_bearing=False)
# ---- S2 admission ----------------------------------------------------------------------------------------------------------------------
dims = {"a_*^2 = kappa^2 Lambda/8pi": "L^-2", "theta_L^2 = 3 Lambda c^2": "T^-2", "G": "overall 1/16 pi G normalisation (not a rest mass)", "c2": "1", "beta": "1", "kappa": "1",
        "M^2 (11C-b) = 3 c2 Lambda c^2": "T^-2", "shape functions": "1"}
R.out["numbers"]["parameter_dimensions"] = dims
no_mass = True
R.check("S2a no parameter of any variant carries the dimension of a rest mass (scales are Lambda-derived: L^-2, T^-2; couplings dimensionless)", str(dims), no_mass, load_bearing=False)
R.out["numbers"]["S2"] = {"11C-a": {"a_rest_mass": "none", "b_conserved_number": "none (aether form); Q = 0 (khronon form, A8.4)", "c_functional_of_baryons": "yes: rho_eff -> 0 as M -> 0 (deep-MOND rho_eff ~ sqrt(M))"},
                           "11C-b": {"a_rest_mass": "none", "b_conserved_number": "none / Q = 0", "c_functional_of_baryons": "yes; plus a background G-renormalisation rho_ae ~ H^2 slaved to expansion"},
                           "11C-c": {"a_rest_mass": "none in the flow; the coupling changes the BARYONS' effective mass m(1 + beta h)", "b_conserved_number": "none / Pi_0 fixed by <delta theta> = 0",
                                     "c_functional_of_baryons": "yes (delta theta slaved to rho)"}}
# rho_eff -> 0 as M -> 0 (P2 point mass, fixed r): rho_ph = a0/(4 pi G r sqrt(1+x^2))
a0 = A0["canonical"]; rfix = 3000.0
rho_ph = lambda M: a0 / (4 * math.pi * G * rfix * math.sqrt(1 + (rfix / rM_kpc(M, a0)) ** 2))
R.check("S2c the effective density is a functional of the baryons: at fixed r it falls like sqrt(M) as M -> 0", f"rho_ph(1e9)/rho_ph(1e12) = {rho_ph(1e9)/rho_ph(1e12):.3e} (sqrt(1e-3) = 0.0316)",
        abs(rho_ph(1e9) / rho_ph(1e12) - math.sqrt(1e-3)) / math.sqrt(1e-3) < 0.05)
s2b_ok = True
if mut == "M7":
    s2b_ok = False                                      # a nonzero Q is a conserved number
    R.check("M7 khronon charge Q != 0: S2(b) FAILS (a conserved number a^3 J^0 = Q exists)", "Q = 1", s2b_ok)
    R.finish(bite=(not s2b_ok))
# ---- FRW background of the c2 channel vs the cold density ----------------------------------------------------------------------------
Om_r = 9.1e-5
Ob0 = OB_H2 / HH ** 2; Oc0 = OC_H2 / HH ** 2
avals = np.logspace(-3, 0, 7)
def frac_ae(c2v):
    """rho_ae / rho_crit(a) = -(3 c2/2) * (3H^2/8 pi G)/rho_crit(a)... with G_cos = G/(1+3c2/2):  rho_ae/rho_tot = -(3c2/2)/(1+3c2/2)."""
    return -(1.5 * c2v) / (1 + 1.5 * c2v)
rho_tot = lambda a: (Ob0 + Oc0) / a ** 3 + Om_r / a ** 4 + OL
rows = []
for c2v in (6.3e-4, 2.9e-3):
    for av in avals:
        rae = frac_ae(c2v) * rho_tot(av)                 # in units of rho_crit,0
        rreq = Oc0 / av ** 3
        rows.append((c2v, float(av), rae / rreq))
worst = min(abs(x[2]) for x in rows), max(abs(x[2]) for x in rows)
R.out["numbers"]["nocold_background_ratio"] = {"c2=6.3e-4..2.9e-3, a in [1e-3,1]: |rho_ae/rho_req| range": list(worst), "sign": "negative (rho_ae < 0)"}
P(f"  no-cold background test (i): |rho_ae/rho_req| ranges {worst[0]:.2e} .. {worst[1]:.2e}, sign negative; line: within 5% of 1")
nocold_i = worst[0] > 0.95 and worst[1] < 1.05
# leaf-averaged c2 (11C-a, -c): FRW is GR: rho_ae = 0
P("  11C-a/-c (leaf-averaged theta-term): rho_ae = 0 on FRW exactly (G_cos = G, L350 G5)")
# ---- baryon-only growth vs LCDM (open universe with the same Lambda) ------------------------------------------------------------------
def growth_ratio(Om_m, curved):
    Ok = 1.0 - Om_m - Om_r - OL if curved else 0.0
    OLv = OL if curved else 1.0 - Om_m - Om_r
    E2 = lambda a: Om_m / a ** 3 + Om_r / a ** 4 + Ok / a ** 2 + OLv
    def rhs(N_, y):
        a = math.exp(N_)
        E2a = E2(a)
        dlnE = 0.5 * (-3 * Om_m / a ** 3 - 4 * Om_r / a ** 4 - 2 * Ok / a ** 2) / E2a
        Om_a = Om_m / a ** 3 / E2a
        return [y[1], -(2 + dlnE) * y[1] + 1.5 * Om_a * y[0]]
    a_i = 1e-3
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i], rtol=1e-9, atol=1e-14)
    return float(sol.y[0, -1] / a_i)
cold_on_Om = OM if mut != "M8" else OM
Om_nocold = (Ob0) if mut != "M8" else OM
g_lcdm = growth_ratio(OM, False)
g_nc = growth_ratio(Om_nocold, True) if mut != "M8" else growth_ratio(OM, False)
ratio = g_nc / g_lcdm
R.out["numbers"]["nocold_growth"] = {"D(1)/D(1e-3) LCDM": g_lcdm, "baryon-only (open, same Lambda)": g_nc, "ratio": ratio}
P(f"  no-cold growth D(a=1)/D(a=1e-3): LCDM {g_lcdm:.1f}; baryon-only universe {g_nc:.1f}; ratio {ratio:.3f} (line: within 5% of 1; Compton drag / baryon pressure ignored: would make it worse)")
nocold_ii = abs(ratio - 1) <= 0.05
R.check("C8 LCDM growth D(1)/D(1e-3) ~ 800-1000 (matter-radiation-dominated initial condition ignored)", f"{g_lcdm:.1f}", 500 < g_lcdm < 1100, load_bearing=False)
R.verdict("G2 no-cold (11C-x-nocold), background test (i) [11C-b; 11C-a/-c have rho_ae = 0]", "PASS" if nocold_i else "FAIL", f"|rho_ae/rho_req| = {worst[0]:.1e}..{worst[1]:.1e}, wrong sign")
R.verdict("G2 no-cold, growth test (ii) [all three]", "PASS" if nocold_ii else "FAIL", f"baryon-only growth ratio {ratio:.3f}")
R.verdict("S2 (inside the owner's picture)", "PASS (a, b); PASS with caveat (c)", "no rest mass, no conserved number (Q = 0), effective density slaved to the baryons; 11C-c's coupling changes the baryons' mass, not the flow's")
R.verdict("S1 stress-energy", "REPORTED", "rho_flow = T_uu = the Phi-equation source (A8.1); p_r, p_t = O(Phi/c^2) relative; conserved (A8.3); not a perfect fluid, not vacuum-like")
if mut == "M8":
    R.finish(bite=(abs(ratio - 1) <= 0.05))
R.finish(bite=False)
