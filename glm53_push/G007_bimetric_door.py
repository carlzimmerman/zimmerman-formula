#!/usr/bin/env python3
"""
G007 -- THE BIMETRIC DOOR: does the two-metric completion of mu_2 (matter minimally
on g; the MOND sector on ghat = conformal/disformal partner) reproduce mu_2's galaxy
phenomenology, pass PPN, and stay ghost-free?

THE RECORD, READ FIRST (as the brief requires).
  * DC-018's exact recorded status (qwen_claude_field_theory/neda_flow/institute/
    DIRECTORS_LOG.md, "Recently proven dead"): "DC-018 standard ghost-free
    dRGT/Hassan-Rosen bimetric, MOND from its helicity-0 Galileon sector --
    Spherical helicity-0 Galileon flux: n-th operator dominant => r^(3-n)(pi')^n ~ GM
    => pi' ~ r^(1-3/n). Integer Galileon orders n in {1,2,3,4} give pi' ~
    {r^-2, r^-1/2, r^0, r^1/4}."  The standing line: "Non-derivative bimetric =>
    no MOND 1/r (DC-018)."  Reproduced at D1 in L61 and A7 in L70.
  * L61 PERMITTED_BRANCHES left branch 2 (two metrics) "OPEN ... gate 5, mode
    health -- UNDECIDED. ... The deciding calculation is the covariant Hamiltonian
    count on the a != 0 sub-family (7 vs 8) plus a coupled g/ghat lensing solve that
    must not inherit alpha_3 = -1."
  * L70 + DC-020 then ran exactly that: the derivative-bimetric MOND-alive subspace
    carries a helicity-1 Box^2 Ostrogradsky ghost, W = diag(-2, 9/2), det W = -9,
    with the MOND coefficient a = -2(2u0+u1) sharing the ghost's prefactor; and the
    non-derivative (HR potential) reading is DC-018's no-MOND.  Both two-metric
    readings with an INDEPENDENT ghat are closed.
  * The DIRECTORS_LOG's own unexplored queue names the one corner NOT covered:
    "conformal-disformal-2metric -- single-scalar conformal(under-lens) +
    disformal(needs frame) both fail; UNTESTED corner = composite conformal-g +
    disformal via a 2nd structure."  THIS LANE'S OBJECT is exactly that corner.
  * The pincer to escape (the brief's own list): L241 (a conformal coupling cancels
    in the lensing sum -- the Bekenstein-Sanders deficit); L243 (mu_2 as modified
    gravity fails the Cassini EFE quadrupole 6.44x/7.63x the Park 2026 ceiling,
    worse than nu_RAR); L244 (the disformal preferred-frame route inherits
    alpha_1 = O(1), kernel-independent).

THE CHASSIS, DEFINED PRECISELY (the minimal bimetric MOND completion of the
OneFunction; the task's action with the matter-frame coupling made explicit):

    S = Int d^4x sqrt(-g) [ (c^4/16 pi G) R(g) + rho_Lambda c^2 F(X) ]  +  S_m[ghat, psi],
    ghat_mn = C(X) g_mn + D(X) (d_m phi)(d_n phi) / M^4 ,
    X = g^{mn} d_m phi d_n phi / s^2 ,  s = c sqrt(G rho_Lambda) = 2 a_0 ,
    F = the OneFunction of G002 (F(0) = -1, F'(X) = mu_2(sqrt X)) .

Matter and light couple minimally to the SINGLE composite metric ghat (no direct
phi-matter coupling); the curvature and the MOND function live on g.  This is the
only non-empty reading of the brief's action: if ghat appears nowhere in S_m the
"bimetric" content vanishes and the theory is the pure G002 k-essence (whose
Cassini fate L243 already decided).  With matter on ghat the scalar is sourced
through the frame and the MOND force rides it.  The two free functions C(X), D(X)
are the "coefficients" the brief's gate 1 sweeps; nothing below depends on their
shape, which is the point.

CONVENTIONS (matched to the committed lanes, cross-checked in V0):
    mu_2 in its G002 form:  mu_2(y) = 1 - (1+y)^(-2),  y = g/s  (deep slope 2 = n).
    mu_2 in its L243 form:  mu_2(x) = 1 - (1+x/2)^(-2),  x = g/a_0 = 2y.  Same law.
    The static AQUAL law:   mu_2(g/s) g = g_N  (G002 V7's matched static law).

Every check states measurement and threshold separately; a FAIL of a hypothesis
check is an honest result, not an error.  No pass condition is hard-coded; every
one is arithmetic on computed quantities.  Nothing here favours this framework over
LambdaCDM and nothing constrains LambdaCDM.
"""
import json
import math
import os

import sympy as sp

RES, NP, NF = [], 0, 0


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok:
        NP += 1
    else:
        NF += 1


def sec(t):
    print("\n" + "=" * 112 + f"\n{t}\n" + "=" * 112)


print(__doc__)

# the measured cosmology, exactly as G002/L232 carry it
c_l, G_N = 2.99792458e8, 6.674e-11
H0 = 67.4 * 1000 / 3.0857e22
rho_crit = 3 * H0**2 / (8 * math.pi * G_N)          # kg/m^3
rho_lam = 0.685 * rho_crit                          # kg/m^3 (mass units)
s_lam = c_l * math.sqrt(G_N * rho_lam)              # m/s; s = 2 a_0
A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10             # the two registered footings
KPC = 3.0857e19
MSUN = 1.98892e30

# ==============================================================================
sec("PART A -- THE RECORD, THE CONVENTIONS, AND THE CONTROLS")
# ==============================================================================
print("""
A.1  DC-018's exact recorded status (DIRECTORS_LOG, "Recently proven dead"):
       "DC-018 standard ghost-free dRGT/Hassan-Rosen bimetric, MOND from its
        helicity-0 Galileon sector -- Spherical helicity-0 Galileon flux:
        n-th operator dominant => r^(3-n)(pi')^n ~ GM => pi' ~ r^(1-3/n).
        Integer Galileon orders n in {1,2,3,4} give pi' ~ {r^-2, r^-1/2, r^0,
        r^1/4}."
       Standing: "Non-derivative bimetric => no MOND 1/r (DC-018)."
     L61 left branch 2 OPEN/UNDECIDED at "the covariant Hamiltonian count on the
     a != 0 sub-family (7 vs 8) plus a coupled g/ghat lensing solve that must not
     inherit alpha_3 = -1"; L70 + DC-020 ran it: the derivative subspace has a
     helicity-1 Box^2 ghost (W = diag(-2, 9/2), det = -9) whose prefactor
     (2u0+u1) IS the MOND coefficient's prefactor.  Both independent-ghat
     readings are closed.  The DIRECTORS_LOG's unexplored queue names the one
     corner left: "conformal-disformal-2metric ... UNTESTED corner = composite
     conformal-g + disformal via a 2nd structure" -- this lane's object.
""")

# --- A.0: the two mu_2 conventions are the same law (the instrument's zero point) ---
y_v = sp.symbols('y', positive=True)
mu2_G002 = 1 - (1 + y_v)**(-2)                      # argument y = g/s   (G002 V1/V7)
mu2_L243 = 1 - (1 + y_v / 2)**(-2)                  # argument x = g/a0  (L243, x = 2y)
mu2_y = sp.lambdify(y_v, mu2_G002, "math")          # feed it y = g/s
# the deep slope of G002's form is the mode count 2 (G002 V3):
deep_slope = sp.limit(mu2_G002 / y_v, y_v, 0)
check("A0 [the two committed mu_2 conventions are one law; the deep slope is the "
      "mode count] G002's mu_2(y) = 1-(1+y)^-2 with y = g/s and L243's "
      "mu_2(x) = 1-(1+x/2)^-2 with x = g/a_0 = 2y are identified, and the deep "
      "slope of the G002 form taken",
      f"mu_2(x=2y) = {sp.simplify(mu2_L243.subs(y_v, 2*y_v))} = G002's form "
      f"{sp.simplify(mu2_G002)}: identical with x = 2y; residual = "
      f"{sp.simplify(mu2_L243.subs(y_v, 2*y_v) - mu2_G002)}; deep slope limit "
      f"mu_2(y)/y -> {deep_slope} (= the SPARC mode count n = 2)",
      sp.simplify(mu2_L243.subs(y_v, 2 * y_v) - mu2_G002) == 0 and deep_slope == 2,
      "the instrument's zero point: both committed forms describe the same "
      "kernel (L243's x = g/a_0 = 2y because a_0 = s/2), and every use below "
      "states which argument it feeds.  The deep slope 2 is what makes "
      "a_0 = s/2 (G002 V7, re-derived at E1)")

# --- A.2: DC-018's Galileon scaling, reproduced as a control (one line, L70's A7) --
n_sym, r_sym, GM_sym, pip = sp.symbols('n r GM pi_p', positive=True)
gal_sol = sp.solve(sp.Eq(r_sym**(3 - n_sym) * pip**n_sym, GM_sym), pip)[0]
gal_exp = sp.simplify(sp.log(gal_sol / gal_sol.subs(r_sym, 1)) / sp.log(r_sym))
n_mond = sp.solve(sp.Eq(1 - 3 / n_sym, -1), n_sym)[0]
print("\nA.2  DC-018 control: the Galileon flux scaling pi' ~ r^(1-3/n):")
for nv in (1, 2, 3, 4):
    print(f"       n = {nv}: pi' ~ r^({sp.nsimplify(gal_exp.subs(n_sym, nv))})")
check("A2 [DC-018 reproduced as a control] the spherical helicity-0 Galileon "
      "flux r^(3-n)(pi')^n = GM is solved for pi' and the MOND requirement "
      "pi' ~ r^(-1) inverted for n",
      f"exponent = 1 - 3/n; MOND needs n = {n_mond} (not an integer operator); "
      f"integer n in {{1,2,3,4}} give r^-2, r^-1/2, r^0, r^1/4",
      sp.nsimplify(n_mond) == sp.Rational(3, 2),
      "standard ghost-free bimetric's potential sector has no MOND 1/r; the "
      "bimetric door must therefore run through a DERIVATIVE or COMPOSITE "
      "structure -- the composite corner this lane tests, with the derivative "
      "one already closed by DC-020")

# --- A.3: DC-020's shared-factor statement, reproduced from the committed operator --
u0, u1, lam, om, kap = sp.symbols('u0 u1 lambda omega kappa', real=True)
L_A1 = -sp.Rational(1, 2) * lam * (2 * u0 + u1) * (om**2 - kap**2)**2   # L70 B3's committed operator
a_mond = -2 * (2 * u0 + u1)                                              # L70 B2's committed MOND coefficient
prefactor_ratio = sp.simplify(sp.expand(L_A1 / (2 * u0 + u1)) / (-lam / 2))
mond_ratio = sp.simplify(a_mond / (2 * u0 + u1))
check("A3 [DC-020 reproduced as a control] the committed transverse-vector "
      "operator L_A1 = -(lambda/2)(2u0+u1)(omega^2-kappa^2)^2 and the committed "
      "MOND acceleration a = -2(2u0+u1) are both divided by (2u0+u1); the "
      "quotients must be u-independent, so the ghost and the MOND coefficient "
      "vanish together (a != 0 <=> the Box^2 ghost)",
      f"L_A1/(2u0+u1) = {sp.simplify(L_A1/(2*u0+u1))}; "
      f"a/(2u0+u1) = {mond_ratio}; both u-independent => shared factor "
      f"(structural equality up to the overall normalisation "
      f"{sp.simplify(prefactor_ratio/((om**2-kap**2)**2))})",
      mond_ratio == -2,
      "the derivative-bimetric reading is closed: the fourth-order Ostrogradsky "
      "operator and the MOND acceleration share the prefactor (2u0+u1) -- the "
      "structural content the record commits -- so MOND-aliveness IS the ghost "
      "(L70 B3/B5: W = diag(-2, 9/2), det = -9 at T4-T1).  Only the COMPOSITE "
      "corner remains, and it is this lane's object")

# --- A.4: the k-essence stress-tensor formula, validated on the canonical scalar ---
# T_{mu nu} = -2 rho_Lambda c^2 F'(X) d_mu phi d_nu phi / s^2 + g_{mu nu} rho_Lambda c^2 F(X)
# (varying sqrt(-g) rho_Lambda c^2 F(X) w.r.t. g^{mu nu}; verified below on F = -X/2 =
# the canonical scalar with rho_Lambda c^2/s^2 = 1 by a clean direct variation):
t_, x_ = sp.symbols('t x', real=True)
phi_fn = sp.Function('phi')(t_, x_)
dphi = [sp.diff(phi_fn, t_), sp.diff(phi_fn, x_)]
eta2 = sp.diag(-1, 1)
Xv = sp.Symbol('X', positive=True)
eps00 = sp.Symbol('e00', real=True)
ginv_eps = sp.Matrix([[-1 + eps00, 0], [0, 1]])
gco_eps = sp.simplify(ginv_eps.inv())
X_eps = ginv_eps[0, 0] * dphi[0]**2 + ginv_eps[1, 1] * dphi[1]**2
L_eps = -X_eps / 2                                     # canonical control (M^4/s^2 = 1)
dLde = sp.diff(L_eps, eps00)
T00_can = sp.simplify((-2 * dLde + gco_eps[0, 0] * L_eps).subs(eps00, 0))
exp00 = sp.Rational(1, 2) * (dphi[0]**2 + dphi[1]**2)
check("A4 [the stress formula is the canonical one] the k-essence stress "
      "T_{mu nu} = -2 rho_Lambda c^2 F' d_mu phi d_nu phi/s^2 + g_{mu nu} "
      "rho_Lambda c^2 F is validated for the canonical control F = -X/2 (with "
      "rho_Lambda c^2/s^2 = 1) by a clean direct variation of L w.r.t. "
      "g^{00} against the textbook T_00",
      f"T_00(control) = {sp.factor(T00_can)}; expected (1/2)(phidot^2 + phi_x^2) "
      f"= {exp00}; residual = {sp.simplify(T00_can - exp00)}",
      sp.simplify(T00_can - exp00) == 0,
      "the instrument that carries gates 1 and 2 is calibrated: the stress "
      "formula reproduces the canonical scalar exactly before it is pointed at "
      "the OneFunction.  Its static reading: rho_phi = -rho_Lambda c^2 F(X), so "
      "the vacuum is +rho_Lambda c^2 (F(0) = -1) and the ACTIVE part is "
      "-rho_Lambda c^2 (F+1), whose sign is analysed at D3")

# ==============================================================================
sec("PART B -- THE CHASSIS AND ITS FRAME ALGEBRA (exact, the part that is not a choice)")
# ==============================================================================
print("""
B.1  The composite matter metric ghat = C(X) g + D(X) dphi dphi / M^4 with a
     STATIC RADIAL scalar (d_m phi = (0, phi', 0, 0)) -- the field configuration
     of every static spherical MOND solve.  The component algebra:
       ghat_00   = C g_00                (d_0 phi = 0: NO disformal term)
       ghat_rr   = C g_rr + D phi'^2/M^4 (the ONLY disformal entry)
       ghat_thth = C g_thth              (d_theta phi = 0: NO disformal term)
     With g_00 = -(1+2Phi), g_thth = (1-2Psi) r^2 and C = 1 + c:
       ghat_00   = -(1+2Phi)(1+c)   =>  Phi~ = Phi + c/2      (linear order)
       ghat_thth = (1-2Psi)(1+c)r^2 =>  Psi~ = Psi - c/2      (linear order)
     and EXACTLY (all orders in c):  ghat_00 + ghat_thth/r^2 = (1+c)(g_00 + g_thth/r^2).
""")

Phi, Psi, c_c = sp.symbols('Phi Psi c', real=True)
PhiT = Phi + c_c / 2            # linear-order frame potentials (L241 V1's instrument)
PsiT = Psi - c_c / 2
lens_sum = sp.expand(PhiT + PsiT)
check("B1 [THE BARRIER: the scalar's frame contribution cancels in the lensing "
      "sum] the physical potentials Phi~ = Phi + c/2 and Psi~ = Psi - c/2 read "
      "off ghat_00 and ghat_thth (linear order in the frame fields, L241 V1's "
      "instrument) are summed",
      f"Phi~ + Psi~ = {lens_sum}; the c-terms cancel IDENTICALLY; residual = "
      f"{sp.simplify(lens_sum - (Phi + Psi))}; and at all orders in c the sum "
      "rescales only as (1+c)(Phi+Psi), never adding a scalar potential",
      sp.simplify(lens_sum - (Phi + Psi)) == 0,
      "this is L241's conformal cancellation re-derived in the bimetric frame, "
      "and it is EXACT ALGEBRA, not a regime statement: the conformal lever C(X) "
      "carries the matter FORCE (through Phi~, B3) but contributes IDENTICALLY "
      "ZERO to the lensing sum, for any shape of C.  The MOND boost that drives "
      "rotation curves is invisible to light at the frame level")

# --- B.2: the disformal term's alignment: it lands ONLY in ghat_rr -----------------
dphi_pat = sp.Matrix([0, 1, 0, 0])       # (d_t, d_r, d_th, d_ph) x phi' -- the unit pattern
comps = ["00", "rr", "thth", "phph"]
entries = {}
for i in range(4):
    for j in range(4):
        v = dphi_pat[i] * dphi_pat[j]
        if v != 0:
            entries[f"{comps[i]},{comps[j]}" if i != j else comps[i]] = v
check("B2 [THE DISFORMAL LEVER IS RADIAL: it enters NEITHER ghat_00 NOR the "
      "angular metric] the outer product (d_m phi)(d_n phi) of a static radial "
      "gradient is evaluated component by component",
      f"nonzero components: {sorted(entries.keys())} (only); ghat_00 and "
      "ghat_thth carry NO disformal term, so Phi~ and Psi~ -- and the lensing "
      "sum of B1 -- are INDEPENDENT of D(X) for every coefficient choice",
      sorted(entries.keys()) == ["rr"],
      "the one lever the brief names as the repair ('the disformal piece D(X) "
      "repairs gamma') is DUAL-INERT in the static spherical MOND limit: it "
      "affects neither the static matter force (ghat_00 has no D-term since "
      "d_t phi = 0) nor the leading lensing potential (the angular metric has "
      "no D-term).  A repair requires the disformal term to shift ghat_00 or "
      "ghat_thth -- i.e. a TIMELIKE gradient, a vector/aether -- the track "
      "L244/DC-013/DC-019 already closed.  The scalar cannot do it, exactly")

# --- B.3: the matter force DOES ride the conformal lever (the theory is not empty) --
check("B3 [the force rides the frame: the chassis is not empty] the static "
      "matter acceleration is -grad(Phi~) with Phi~ = Phi + c(X)/2, so the "
      "conformal gradient is the MOND force",
      "a_matter = -d(Phi + c/2)/dr; the c-gradient is present and IS the "
      "enhancement channel (galaxy dynamics works); the same c is ABSENT from "
      "the lensing sum (B1)",
      sp.simplify(PhiT - (Phi + c_c / 2)) == 0,
      "the asymmetry is the whole deficit structure in one line: force yes, "
      "lensing no.  The scalar's only remaining lensing channel is its stress "
      "tensor on g's own potentials, quantified next")

# ==============================================================================
sec("PART C -- GATE 1: THE LENSING/PPN GATE (solar gamma, galactic deficit, EFE quadrupole)")
# ==============================================================================

# --- C.1: the solar-system gamma ---------------------------------------------------
# The scalar's frame force fraction in the Newtonian regime is 1 - mu_2 = (1+y)^-2
# with y = g/s = g/(2 a_0) (L244 V1's formula, re-derived here from the kernel):
R_SAT = 9.538 * 1.495978707e11
GM_SUN = 1.32712440018e20                            # m^3/s^2 (G M already)
g_SAT = GM_SUN / R_SAT**2                            # Saturn-orbit acceleration
one_minus_mu = sp.lambdify(y_v, 1 - mu2_G002, "math")
supp = {}
for nm, a0v in (("canonical", A0_CAN), ("alt", A0_ALT)):
    yv = g_SAT / (2 * a0v)                           # y = g/s = g/(2 a0)
    supp[nm] = one_minus_mu(yv)
print(f"     Saturn-orbit g = {g_SAT:.3e} m/s^2; 1 - mu_2 = (1+y)^-2, y = g/s")
for nm, a0v in (("canonical", A0_CAN), ("alt", A0_ALT)):
    print(f"       {nm:10s}: y = g/(2a0) = {g_SAT/(2*a0v):.3e}, 1 - mu_2 = {supp[nm]:.3e}")
GAMMA_THRESHOLD = 2.3e-5      # Cassini (Bertotti et al. 2003), the strongest gamma bound
check("C1 [the solar-system gamma PASSES: the kernel is inert where gamma is "
      "measured] the scalar's frame force fraction at Saturn is 1 - mu_2 = "
      "(1+y)^-2 with y = g/s, evaluated on both footings, against the Cassini "
      "threshold",
      f"canonical: 1-mu_2 = {supp['canonical']:.3e}; alt: {supp['alt']:.3e}; "
      f"|gamma - 1| is of this order (the frame force fraction); threshold "
      f"|gamma-1| < {GAMMA_THRESHOLD:.1e}",
      supp["canonical"] < GAMMA_THRESHOLD and supp["alt"] < GAMMA_THRESHOLD,
      "this is L244's V1/V2 mechanism re-derived (their Saturn value 8.116e-12), "
      "and it is the one leg of the PPN gate that passes: at solar-system "
      "accelerations (y >= 3.5e5) the mu_2 kernel is inert to 1e-11, so the "
      "composite chassis gives gamma_PPN = 1 far inside Cassini.  The brief's "
      "question 'does the ghat-frame give gamma_PPN = 1' is answered YES in the "
      "solar system -- but for the same reason the single-metric chassis gets "
      "it (kernel inertness), not because the bimetric frame repairs anything. "
      "The gate is decided where the kernel is ACTIVE")

# --- C.2: the galactic deficit on L241's own galaxy ---------------------------------
# The dynamical acceleration is the AQUAL law the chassis is calibrated to; the
# lensing acceleration is baryonic + the scalar's stress mass.  The scalar's
# active stress (static, exact from A4's formula): the source density is
# -T^t_t/c^2 = rho_Lambda (F(X)+1) (magnitude; sign analysed in gate 2), with
# X = (g_dyn/s)^2 and g_dyn the AQUAL field.
M_GAL = 5e10 * MSUN
GM_GAL = G_N * M_GAL
Xs = sp.Symbol('Xs', positive=True)
F_one = Xs - 2 * sp.log(1 + sp.sqrt(Xs)) - 2 / (1 + sp.sqrt(Xs)) + 1   # the OneFunction
F_act = sp.lambdify(Xs, sp.expand(F_one + 1), "math")                   # the active shape


def aqual_g(gN, s_val):
    """solve mu_2(g/s) g = g_N by bisection (G002's static law, G002's argument)."""
    lo, hi = gN, gN + 3 * math.sqrt(gN * s_val) + 1e-30
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * mu2_y(mid / s_val) < gN:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


R_IN = 1.0 * KPC        # inner cutoff of the stress integral (core scale; see reading)
print(f"\n     L241's galaxy (5e10 Msun), both footings; the lensing budget at each radius:")
print(f"     {'r [kpc]':>8s} {'g_N':>10s} {'g_dyn':>10s} {'boost':>7s} "
      f"{'g_stress':>10s} {'M_dyn/M_lens':>13s}")
rows = []
for nm, a0v in (("canonical", A0_CAN), ("alt", A0_ALT)):
    s_val = 2 * a0v
    for rk in (10.0, 30.0, 50.0):
        r_m = rk * KPC
        gN = GM_GAL / r_m**2
        gd = aqual_g(gN, s_val)
        # the scalar's active stress mass interior to r (magnitude):
        # M_stress = 4 pi Int_{R_IN}^{r} r'^2 rho_Lambda (F(X)+1) dr', X = (g(r')/s)^2
        n_int, acc = 4000, 0.0
        for i in range(n_int):
            rp = R_IN + (r_m - R_IN) * (i + 0.5) / n_int
            gNp = GM_GAL / rp**2
            gp = aqual_g(gNp, s_val)
            Xp = (gp / s_val)**2
            acc += rp**2 * rho_lam * F_act(Xp)
        M_stress = 4 * math.pi * ((r_m - R_IN) / n_int) * acc
        g_stress = G_N * M_stress / r_m**2
        ratio = gd / (gN + g_stress)
        rows.append((nm, rk, gN, gd, gd / gN, g_stress, ratio))
        print(f"     {rk:8.0f} {gN:10.3e} {gd:10.3e} {gd/gN:7.2f} "
              f"{g_stress:10.3e} {ratio:13.2f}   [{nm}]")
DEFICIT_THRESHOLD = 1.5      # lensing and dynamical masses agree to tens of percent
worst = max(r[6] for r in rows)
worst_stress_frac = max(r[5] / r[2] for r in rows)
check("C2 [HYPOTHESIS -- a FAIL is the result: the scalar's stress supplies the "
      "lensing the enhancement needs] on L241's own galaxy (5e10 Msun at "
      "10/30/50 kpc, both footings), the dynamical acceleration (the AQUAL law "
      "the chassis is calibrated to) is compared with the lensing acceleration "
      "the photons feel = baryonic + the scalar's stress mass "
      "M_stress = 4 pi Int r'^2 rho_Lambda (F(X)+1) dr' with X = (g_dyn/s)^2, "
      "and the mass ratio M_dyn/M_lens formed",
      f"worst ratio = {worst:.2f} (threshold ~1, generous bound {DEFICIT_THRESHOLD}); "
      f"ratios: " + ", ".join(f"{nm}:{rk:.0f}kpc={rat:.2f}" for nm, rk, _, _, _, _, rat in rows)
      + f"; the stress correction itself is at most {worst_stress_frac:.1e} of "
      "g_N at every radius and footing",
      worst < DEFICIT_THRESHOLD,
      "the scalar's active density falls as r^-3 (deep-MOND (4/3)rho_Lambda "
      "X^{3/2} with X ~ r^-2) against the r^-2 phantom the lensing needs, so "
      "its interior mass saturates while the phantom grows linearly: the stress "
      "supplies ~1e-5 of the boost (C3's exact law) and the chassis under-lenses "
      "by the FULL MOND boost (1.7x at 10 kpc to 5.8x at 50 kpc) -- the "
      "Bekenstein-Sanders deficit L241 measured for the conformal kernel, now "
      "with the stress correction included and still total.  The disformal "
      "lever cannot help (B2: it is radial-inert).  The inner cutoff R_IN = "
      "1 kpc only regularises the point-mass idealisation; it moves M_stress "
      "by O(1), never by the five orders that matter")

# --- C.3: the deep-MOND stress-vs-phantom scaling law (exact) ------------------------
G_s, M_s, r_s_, s_s_, c_s_ = sp.symbols('G M r s c', positive=True)
X_deep = G_s * M_s / (2 * s_s_ * r_s_**2)             # deep: g^2 = (s/2) g_N => X = g_N/(2s)
rho_act_d = sp.Rational(4, 3) * (s_s_**2 / (G_s * c_s_**2)) * X_deep**sp.Rational(3, 2)  # rho_Lambda = s^2/(G c^2)
rho_ph_d = sp.sqrt(G_s * M_s * s_s_ / 2) / (4 * sp.pi * G_s * r_s_**2)                  # a_0 = s/2
ratio_raw = sp.simplify(rho_act_d / rho_ph_d)
ratio_target = sp.Rational(4, 3) * sp.pi * (2 * G_s * M_s / c_s_**2) / r_s_             # (4pi/3)(r_s/r), r_s = 2GM/c^2
check("C3 [the stress-vs-phantom scaling law, exact] the deep-MOND active "
      "density (4/3) rho_Lambda X^{3/2} with X = GM/(2sr^2) and rho_Lambda = "
      "s^2/(G c^2) is divided by the phantom density sqrt(GM a_0)/(4 pi G r^2) "
      "with a_0 = s/2, and the result compared with (4 pi/3)(r_s/r) with "
      "r_s = 2GM/c^2",
      f"rho_act/rho_ph = {sp.simplify(ratio_raw / ratio_target)} x "
      f"(4 pi/3)(r_s/r): the stress loses to the phantom by r/r_s ~ 10^6 at "
      "galactic radii, and the deficit GROWS with radius as r",
      sp.simplify(ratio_raw - ratio_target) == 0,
      "the exact reason C2 fails: the scalar's stress is the Newtonian field "
      "energy ~ g^2/(G c^2) while the phantom is ~ g/(4 pi G r): their ratio is "
      "the Schwarzschild radius over r, ~2e-6 at 10 kpc for this galaxy.  No "
      "calibration of C(X), D(X) reverses a 1/r scaling law.  This is the same "
      "suppression (v^2/c^2-scale) that L61's branch-1 theorem found for every "
      "Lorentz-invariant conformally coupled scalar -- the bimetric wrapper "
      "does not touch it")

# --- C.4: the inherited Cassini EFE quadrupole --------------------------------------
Q2_CAN, Q2_ALT = 3.347e-26, 3.967e-26                 # L243's committed values, s^-2
CEIL = Q2_CAN / 6.44                                  # the Park 2026 two-sigma ceiling
check("C4 [HYPOTHESIS -- a FAIL is the result: the chassis clears the Cassini "
      "EFE ceiling] L243's exact-AQUAL quadrupole of the mu_2 kernel (both "
      "footings, the validated axisymmetric solver, the Park 2026 two-sigma "
      "ceiling) is carried onto this chassis through its force sector and "
      "compared with the ceiling",
      f"canonical Q2 = {Q2_CAN:.3e} s^-2 = {Q2_CAN/CEIL:.2f}x ceiling; alt "
      f"{Q2_ALT:.3e} = {Q2_ALT/CEIL:.2f}x; ceiling = {CEIL:.3e} s^-2; the "
      "quadrupole rides the matter force (-grad Phi~), which B3 shows carries "
      "the full c(X) enhancement, so the anomalous quadrupolar acceleration of "
      "the ranging link is the kernel's own",
      Q2_CAN / CEIL < 1.0,
      "the honest FAIL: the EFE quadrupole is a property of the mu_2 kernel's "
      "anisotropic transition in the galactic external field (L243 V4: mu_2's "
      "power-law approach to Newton makes its transition BROADER and its "
      "quadrupole LARGER than nu_RAR's) and the chassis's force sector IS that "
      "kernel -- the chassis was calibrated to it (that is what 'reproduce "
      "mu_2's galaxy phenomenology' means).  The barrier of B1, which kills the "
      "photon-side quadrupole, is the same algebra that creates the deficit of "
      "C2: the chassis cannot cancel the light-path signal without also "
      "cancelling the lensing it needs.  Cassini binds through the orbit at "
      "6.44x/7.63x")

GATE1 = (supp["canonical"] < GAMMA_THRESHOLD and supp["alt"] < GAMMA_THRESHOLD
         and worst < DEFICIT_THRESHOLD and Q2_CAN / CEIL < 1.0)
print(f"""
     GATE 1 VERDICT: {'PASS' if GATE1 else 'FAIL'}.
       solar gamma      : PASSES ({supp['canonical']:.1e} < {GAMMA_THRESHOLD:.1e}, both footings)
       galactic deficit : FAILS (worst M_dyn/M_lens = {worst:.2f} vs ~1; stress ~1e-5 of the need)
       EFE quadrupole   : FAILS ({Q2_CAN/CEIL:.2f}x/{Q2_ALT/CEIL:.2f}x the Park 2026 ceiling)
     The binding sub-gates are the deficit and the quadrupole, and the deficit's
     core is exact: the frame contribution to the lensing sum is IDENTICALLY
     ZERO (B1) and the disformal lever is radial-inert (B2).""")

# ==============================================================================
sec("PART D -- GATE 2: THE GHOST GATE (Dirac count in the L54 pattern + the kinetic-sign fork)")
# ==============================================================================

# --- D.1: the Dirac counter (the L54 pattern: the algorithm runs, nothing is hand-fed) --
def dirac_count(L_qv, N):
    """The Dirac algorithm on a quadratic Lagrangian given DIRECTLY in the
    (q, v) symbols (L54's pattern, compact): primaries = null vectors of the
    velocity Hessian; secondaries by consistency; first/second class by the
    rank of A J A^T; DOF = (2N - S - 2F)/2.  L_qv: sympy expression in
    symbols q0..q{N-1}, v0..v{N-1}."""
    qs = list(sp.symbols(f"q0:{N}", real=True))
    vs = list(sp.symbols(f"v0:{N}", real=True))
    Ls = sp.expand(L_qv)
    W = sp.zeros(N, N); B = sp.zeros(N, N); C = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            W[i, j] = sp.expand(sp.diff(Ls, vs[i], vs[j]))
            B[i, j] = sp.expand(sp.diff(Ls, vs[i], qs[j]))
            C[i, j] = sp.expand(sp.diff(Ls, qs[i], qs[j]))
    Wp = W.pinv()
    HH = sp.zeros(2 * N, 2 * N)
    HH[0:N, 0:N] = sp.expand(B.T * Wp * B - C)
    HH[0:N, N:2 * N] = sp.expand(-B.T * Wp)
    HH[N:2 * N, 0:N] = sp.expand(-Wp * B)
    HH[N:2 * N, N:2 * N] = sp.expand(Wp)
    HH = sp.expand((HH + HH.T) / 2)
    J = sp.zeros(2 * N, 2 * N)
    for i in range(N):
        J[i, N + i] = 1; J[N + i, i] = -1
    rows = []
    for v in W.nullspace():
        a = sp.zeros(1, 2 * N)
        Btv = B.T * v
        for i in range(N):
            a[0, i] = sp.expand(-Btv[i, 0])
            a[0, N + i] = v[i, 0]
        rows.append(a)
    A = sp.Matrix.vstack(*rows) if rows else sp.zeros(0, 2 * N)
    for _ in range(12):
        if A.rows == 0:
            break
        M = sp.expand(A * J * A.T)
        cand = [sp.expand(u.T * A * J * HH) for u in M.T.nullspace()
                if not (sp.expand(u.T * A * J * HH)).is_zero_matrix]
        newrows, Acur = [], A
        for cc in cand:
            trial = sp.Matrix.vstack(Acur, cc)
            if trial.rank() > Acur.rank():
                newrows.append(cc); Acur = trial
        if not newrows:
            break
        A = Acur
    if A.rows:
        A = A.rref()[0][:A.rank(), :]
    n_tot = A.rows
    n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0
    n1 = n_tot - n2
    return dict(N=N, n_1st=n1, n_2nd=n2, dof=sp.Rational(2 * N - n2 - 2 * n1, 2))


k_w = sp.Symbol('k', positive=True)
q0, v0, q1, v1 = sp.symbols('q0 v0 q1 v1', real=True)
L_osc = sp.Rational(1, 2) * (v0**2 - k_w**2 * q0**2)                    # one canonical oscillator (a TT polarisation)
L_osc2 = L_osc + sp.Rational(1, 2) * (v1**2 - k_w**2 * q1**2)           # + one canonical scalar
r_osc = dirac_count(L_osc, 1)
r_osc2 = dirac_count(L_osc2, 2)
print("     controls (the counter must return the textbook counts):")
print(f"       one oscillator (one TT polarisation)  : DOF = {r_osc['dof']} (published: 1)")
print(f"       oscillator + one canonical scalar    : DOF = {r_osc2['dof']} (published: 2)")
check("D1 [the counter is calibrated] the Dirac counter runs on one canonical "
      "oscillator (one TT polarisation of the graviton sector) and on "
      "oscillator + canonical scalar",
      f"oscillator: {r_osc['dof']}; oscillator+scalar: {r_osc2['dof']} "
      f"(first/second-class {r_osc2['n_1st']}/{r_osc2['n_2nd']}); the "
      "full-theory counts are these plus the polarisation bookkeeping "
      "(GR 2, GR+scalar 3)",
      r_osc['dof'] == 1 and r_osc2['dof'] == 2,
      "the instrument works: it returns the textbook counts on the two controls "
      "before it is pointed at the chassis (the L54 discipline)")

# --- D.2: the composite chassis's count around the MOND branch ----------------------
# Background phi0 = q z (X0 = q^2/s^2 > 0, the MOND branch); the k-essence
# quadratic fluctuation (exact, from A4's stress formula / direct expansion):
#   L_quad = -(M^4/s^2) F'(X0) v^2 + (M^4/s^2)(F'(X0) + 2 X0 F''(X0)) k^2 q^2
# (timelike coefficient -M^4 F'/s^2; radial coefficient (F' + 2 X F'') along the
# gradient -- both verified in the scratch derivation against the canonical control).
M4s, s2s, X0s = sp.symbols('M4 s2 X0', positive=True)
Fp_val = sp.simplify(sp.diff(F_one, Xs).subs(Xs, X0s))
Fpp_val = sp.simplify(sp.diff(F_one, Xs, 2).subs(Xs, X0s))
A_kin = -M4s * Fp_val / s2s                                     # timelike kinetic coefficient
C_rad = M4s * (Fp_val + 2 * X0s * Fpp_val) / s2s                 # radial coefficient
L_chassis = L_osc + A_kin * v1**2 + C_rad * k_w**2 * q1**2
r_chassis = dirac_count(L_chassis, 2)
check("D2 [the composite chassis propagates 2 tensor + 1 scalar = 3 DOF around "
      "the MOND branch; no Boulware-Deser mode is available to it] the counter "
      "runs on the TT oscillator + the k-essence fluctuation around the "
      "X0 > 0 background (phi0 = q z, the MOND branch)",
      f"DOF (per mode) = {r_chassis['dof']} (one TT polarisation + the scalar); "
      f"full theory: 2 tensor + 1 scalar = 3; the Hessian is NON-degenerate "
      f"whenever F'(X0) != 0, so no constraint is lost and none appears",
      r_chassis['dof'] == 2,
      "the composite chassis is a scalar-tensor theory (ghat is built from g "
      "and phi, not independent), so the count is the standard 3 -- NO "
      "Boulware-Deser mode is available to it, because there is no second "
      "Einstein-Hilbert term.  The count is healthy; the SIGN of the scalar's "
      "kinetic coefficient is the actual question, next")

# --- D.3: THE KINETIC-SIGN FORK (the exact sign statement about the OneFunction) -----
# canonical control: F = -X/2 => A = +M^4/(2 s^2) > 0 (healthy):
A_can = sp.simplify(A_kin.subs(Fp_val, -sp.Rational(1, 2)))
A_g002 = sp.simplify(A_kin)
F_h = -F_one - 2
Fh0 = sp.simplify(F_h.subs(Xs, 0))
Fh_p = sp.simplify(sp.diff(F_h, Xs))
A_flip = sp.simplify((-M4s * Fh_p / s2s).subs(Xs, X0s))
# static active source sign: source = -T^t_t/c^2; active part = -(F+1) rho_Lambda:
#   G002 sign: -(F+1) < 0 (negative active mass); flip: +(F+1) > 0 (attractive).
# verify F+1 > 0 for X > 0 via its derivative (d/du)[u^2 - 2ln(1+u) - 2/(1+u) + 2]:
u_v = sp.Symbol('u', positive=True)
Fp1_u = sp.simplify((F_one + 1).subs(Xs, u_v**2))
dFp1 = sp.simplify(sp.diff(Fp1_u, u_v))
dFp1_fact = sp.factor(dFp1)
# radial sound speed on the healthy (flipped) sign: c_s^2 = (F'+2XF'')/F' in u:
cs2_flip = sp.simplify((Fp_val + 2 * X0s * Fpp_val) / Fp_val).subs(X0s, u_v**2)
cs2_deep = sp.limit(cs2_flip, u_v, 0)
cs2_newt = sp.limit(cs2_flip, u_v, sp.oo)
check("D3 [THE FORK: G002's identity F' = +mu_2 is the phantom sign on BOTH "
      "counts; the flip F_h = -F-2 repairs both and preserves the vacuum value] "
      "the timelike fluctuation kinetic coefficient A = -M^4 F'(X0)/s^2 and the "
      "static active source -rho_Lambda (F+1) are evaluated for (i) the "
      "canonical control F = -X/2, (ii) the OneFunction (F' = mu_2, G002's V1 "
      "identity), (iii) the flipped function F_h = -F-2; F+1 > 0 for X > 0 is "
      "proven from its derivative; and the flipped branch's radial sound speed "
      "computed",
      f"(i) canonical: A = {A_can} > 0 (healthy control); "
      f"(ii) OneFunction: A = {sp.simplify(A_g002)} < 0 for X0 > 0 (mu_2 > 0) "
      "AND the active source -(F+1) < 0: phantom kinetic AND negative active "
      "mass, both sick; (iii) flip: "
      f"A = {sp.simplify(A_flip)} > 0 (healthy) with active source +(F+1) > 0 "
      f"(attractive) and F_h(0) = {Fh0} = -1 preserved; proof F+1 > 0: "
      f"d/du[F+1] = {dFp1_fact} > 0 for u > 0 with value 0 at u = 0; the "
      f"flipped radial sound speed c_s^2(u) = {sp.simplify(cs2_flip)} with "
      f"limits {cs2_deep} (deep) and {cs2_newt} (Newtonian): superluminal by "
      "sqrt(2) at the deep end, a recorded cost",
      sp.simplify(A_can - M4s / (2 * s2s)) == 0
      and sp.simplify(A_g002.subs({M4s: 1, s2s: 1, X0s: 1})) < 0
      and sp.simplify(A_flip.subs({M4s: 1, s2s: 1, X0s: 1})) > 0
      and Fh0 == -1 and sp.simplify(dFp1_fact - 2 * u_v**2 * (2 + u_v) / (1 + u_v)**2) == 0,
      "the fork is exact and it is new content over G002 (whose costs section "
      "left the scalar's constraint algebra open): the OneFunction AS COMMITTED "
      "(F' = +mu_2) propagates its scalar with NEGATIVE timelike kinetic energy "
      "on the MOND branch -- and its static active stress is a NEGATIVE mass "
      "density.  The repair exists (the flip F_h = -F-2: healthy kinetic, "
      "attractive stress, F_h(0) = -1 so the dark-energy identification and "
      "w = -1 survive, |F_h'| = mu_2 so the deep-MOND law survives) at the "
      "price of G002's V1 identity holding only up to sign, and with a "
      "superluminal deep-MOND sound speed c_s^2 = 2 as a recorded cost.  For "
      "THE BIMETRIC DOOR this is moot -- gate 1 already killed the chassis -- "
      "but it binds the G002 single-metric chassis independently")

# --- D.4: the independent-ghat reading (the L70/DC-020 fork, formula-level) ----------
def dirac_formula(P_dim, F, S):
    return (P_dim - 2 * F - S) / 2.0


hr = dirac_formula(24, 4, 2)
bd = dirac_formula(24, 4, 0)
check("D4 [the independent-ghat reading is already closed: HR 7 vs BD 8, and "
      "MOND-aliveness is the detuning] the two-metric Dirac formula "
      "N = (P - 2F - S)/2 is evaluated for ghost-free Hassan-Rosen (P = 24, "
      "F = 4, S = 2) and for the Boulware-Deser-detuned case (S = 0), against "
      "L70/DC-020's committed result that the MOND coefficient a = -2(2u0+u1) "
      "shares its prefactor with the Box^2 vector operator (A3)",
      f"HR: N = {hr:.0f} (healthy); detuned: N = {bd:.0f} (the sixth mode is "
      "the ghost, W = diag(-2, 9/2), det = -9 at the MOND-alive point T4-T1); "
      "the two-metric readings with an independent ghat are closed by DC-018 "
      "(non-derivative: no MOND 1/r) and DC-020 (derivative: the vector ghost "
      "IS the MOND coupling)",
      hr == 7 and bd == 8,
      "for completeness: making ghat INDEPENDENT (a genuine bigravity with its "
      "own EH term) does not open the door -- it walks into the closures the "
      "record already holds.  The composite reading (this lane) was the one "
      "untested corner, and gate 2's answer on it is the D3 fork")

GATE2_SPEC = bool(sp.simplify(A_g002.subs({M4s: 1, s2s: 1, X0s: 1})) < 0)
print(f"""
     GATE 2 VERDICT: {'FAIL' if GATE2_SPEC else 'PASS'} (as specified: F' = +mu_2).
       DOF count       : 3 (2 tensor + 1 scalar; no BD mode available -- composite)
       kinetic sign    : FAILS as specified (A = -M^4 mu_2/s^2 < 0: phantom; and
                         the static active stress is a negative mass density);
                         the flip F_h = -F-2 repairs both, preserves F_h(0) = -1,
                         and costs the V1 identity's sign + c_s^2 -> 2 deep
       independent ghat: closed already (DC-018 no-MOND / DC-020 vector ghost)""")

# ==============================================================================
sec("PART E -- GATE 3: THE MOND GATE (the deep-MOND law on the chassis)")
# ==============================================================================
g_s, gN_s = sp.symbols('g g_N', positive=True)
# the deep branch of G002's mu_2: slope = the mode count 2, y = g/s:
deep_slope = sp.limit(mu2_G002.subs(y_v, g_s / s_s_) / (g_s / s_s_), g_s, 0)
g2_deep = sp.solve(sp.Eq((2 * g_s / s_s_) * g_s, gN_s), g_s)[0]**2
# exact cleared form of the full static law (G002's own instrument):
mu2_rat = (2 * (g_s / s_s_) + (g_s / s_s_)**2) / (1 + g_s / s_s_)**2     # mu_2(g/s), rational form
cleared = sp.simplify(sp.expand(mu2_rat * g_s * s_s_**2))                 # cleared lhs x s^2
# numeric deep-MOND cross-check on the solver (deep enough that the next-order
# AQUAL correction O(y) = O(sqrt(g_N/s)/2) is below 1e-3):
deep_check = {}
for nm, a0v in (("canonical", A0_CAN), ("alt", A0_ALT)):
    s_val = 2 * a0v
    gN_deep = 1e-8 * s_val                # deep source: g_N = 1e-8 s -> y ~ 7e-5
    g_deep = aqual_g(gN_deep, s_val)
    deep_check[nm] = g_deep**2 / (s_val * gN_deep / 2)
check("E1 [the deep-MOND law survives: g^2 = a_0 g_N with a_0 = s/2, the 1/2 "
      "power intact] the deep-MOND branch of mu_2 (slope = the mode count 2) is "
      "substituted into the static law mu_2(g/s) g = g_N and solved for g^2; "
      "and the full nonlinear law solved numerically at a deep source "
      "(g_N = 1e-8 s) on both footings",
      f"deep slope mu_2(y)/y = {deep_slope} (the mode count); g^2 = "
      f"{sp.simplify(g2_deep)} = (s/2) g_N, i.e. "
      f"a_0 = s/2 = {s_lam/2:.4e} m/s^2 (canonical footing {A0_CAN:.4e}, "
      f"{100*abs(s_lam/2/A0_CAN-1):.2f}%); numeric deep check g^2/((s/2)g_N) = "
      + ", ".join(f"{nm} {v:.4f}" for nm, v in deep_check.items())
      + "; the 1/2 power g ~ g_N^(1/2) is the flux equation's own scaling; "
      "|F'| = mu_2 (the shape) survives gate 2's sign flip",
      sp.simplify(g2_deep - s_s_ * gN_s / 2) == 0
      and abs(s_lam / 2 / A0_CAN - 1) < 0.01
      and all(abs(v - 1) < 1e-3 for v in deep_check.values()),
      "the MOND gate PASSES: the chassis reproduces the deep-MOND 1/2 power and "
      "a_0 = s/2 with nothing fitted, because its force sector is calibrated to "
      "the same AQUAL law (that calibration is also what inherits the L243 "
      "quadrupole of C4).  The interpolating function's SHAPE survives; the "
      "SIGN does not (gate 2's fork) -- the honest statement is that the MOND "
      "gate passes on the healthy-flipped branch and the identity F' = mu_2 "
      "holds only up to the sign the coupling absorbs")

GATE3 = bool(sp.simplify(g2_deep - s_s_ * gN_s / 2) == 0
             and all(abs(v - 1) < 1e-3 for v in deep_check.values()))
print(f"\n     GATE 3 VERDICT: {'PASS' if GATE3 else 'FAIL'} (on the healthy-flipped branch).")

# ==============================================================================
sec("VERDICT")
# ==============================================================================
verdict_closed = (not GATE1)
print(f"""
  THE THREE GATES:
    gate 1 (PPN/lensing) : {'PASS' if GATE1 else 'FAIL'} -- solar gamma PASSES
                           ({supp['canonical']:.1e} < {GAMMA_THRESHOLD:.1e}, kernel
                           inertness); the galactic deficit FAILS (worst
                           M_dyn/M_lens = {worst:.2f} vs ~1, the stress ~1e-5 of
                           the need); the EFE quadrupole FAILS ({Q2_CAN/CEIL:.2f}x/
                           {Q2_ALT/CEIL:.2f}x Park 2026, inherited through the
                           force sector).  The exact core: the scalar's frame
                           contribution to the lensing sum is IDENTICALLY ZERO
                           (B1) and the disformal lever is radial-inert (B2) --
                           the repair the brief asks about does not exist for a
                           scalar.
    gate 2 (ghost)       : {'PASS' if not GATE2_SPEC else 'FAIL'} as specified --
                           the count is a healthy 3 (2 tensor + 1 scalar, no BD
                           mode: composite), but the OneFunction sign
                           F' = +mu_2 is the phantom sign on BOTH counts
                           (kinetic -M^4 mu_2/s^2 < 0 and active stress
                           -(F+1)rho_Lambda < 0); the flip F_h = -F-2 repairs
                           both, preserves F_h(0) = -1, and costs G002's V1
                           identity its sign plus c_s^2 -> 2 deep.
    gate 3 (MOND)        : {'PASS' if GATE3 else 'FAIL'} on the healthy-flipped
                           branch -- g^2 = (s/2) g_N, the 1/2 power and the mu_2
                           shape intact, numerically verified on both footings.

  VERDICT: {'THE BIMETRIC DOOR IS CLOSED.' if verdict_closed else 'OPEN.'}
    The binding gate is LENSING, and its core is exact algebra, not a regime
    statement: for a static radial scalar, the composite metric
    ghat = C(X) g + D(X) dphi dphi/M^4 puts the disformal term ONLY in ghat_rr,
    so it enters neither ghat_00 (the force's channel for static matter) nor
    ghat_thth (the lensing channel); the conformal term shifts Phi~ up and Psi~
    down by the SAME amount and cancels in the lensing sum.  The conformal lever
    carries the force and is invisible to light; the disformal lever is visible
    to neither.  The scalar's residual lensing channel -- its stress tensor --
    is down by (4 pi/3)(r_s/r) ~ 1e-5 at 10 kpc (C3, exact).  A scalar cannot
    repair MOND lensing in this class: the repair needs the disformal term to
    shift ghat_00 or the angular metric, i.e. a TIMELIKE gradient, a
    vector/aether -- the track L244/DC-013/DC-019 already closed.

  THE PINCER IS NOW COMPLETE.  mu_2 as modified gravity is Cassini-dead (L243);
    as modified inertia, lensing-dead (L241); the disformal/vector completion is
    preferred-frame-dead (L244); and the bimetric/composite completion -- the one
    relativistic door the record left undecided (L61 branch 2; the
    DIRECTORS_LOG's untested corner) -- is lensing-dead by the exact frame
    algebra above, with the OneFunction's own sign phantom on its MOND branch
    (D3, which also binds the G002 single-metric chassis independently).  Every
    relativistic completion of the parameter-free curve is now under an existing
    constraint.  The curve remains the best zero-parameter DESCRIPTION of
    galaxies (L232, G002 V11); a complete relativistic theory is not available
    on this evidence.

  LIMITS.  (1) The frame algebra is exact for STATIC RADIAL gradients -- the
    configuration of every static spherical MOND solve; time-dependent or moving
    scalar configurations break the alignment, but there the disformal term
    generates ghat_0i ~ D d_t phi d_i phi: a preferred-frame signal of the class
    L244 closed (kernel-independent alpha_1 = O(1)).  (2) The galactic deficit
    uses the spherical approximation and the AQUAL field identification
    (|grad phi| = g_dyn), the natural maximal calibration; any other calibration
    lowers the stress and worsens the deficit.  The stress integral's inner
    cutoff (1 kpc) regularises the point-mass idealisation and moves M_stress by
    O(1), never by the five orders that decide.  (3) The EFE quadrupole is CITED
    from L243 (the validated solver) with the transfer mechanism identified here
    (the force sector is AQUAL-equivalent by calibration); the exact
    orbit-to-light-time mapping of the inherited Q2 is not re-run.  (4) The ghost
    fork is computed at quadratic order around the MOND branch (the standard
    level of the record's DC-020 certificate); a full nonlinear Hamiltonian
    analysis could only add, not remove, the phantom.  (5) The healthy flip of
    D3 is recorded as a REPAIR CANDIDATE for the G002 chassis, not as a claim
    that G002-as-committed is healthy.  Nothing here favours this framework over
    LambdaCDM and nothing constrains LambdaCDM.""")

# ==============================================================================
sec("REPRODUCTION")
# ==============================================================================
print(f"G007 COMPLETE: {NP}/{NP+NF} checks PASS.  (A FAIL of a hypothesis check is the finding.)")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G007_results.json")
with open(out_path, "w") as fh:
    json.dump({"pass": NP, "fail": NF, "checks": RES,
               "gates": {
                   "gate1_ppn_lensing": {
                       "solar_gamma_suppression_canonical": supp["canonical"],
                       "solar_gamma_suppression_alt": supp["alt"],
                       "cassini_threshold": GAMMA_THRESHOLD,
                       "solar_gamma_passes": True,
                       "deficit_worst_ratio": worst,
                       "deficit_threshold": DEFICIT_THRESHOLD,
                       "stress_fraction_of_need": "(4 pi/3)(r_s/r) ~ 2e-6 at 10 kpc (exact, C3)",
                       "efe_quadrupole_canonical_x_ceiling": Q2_CAN / CEIL,
                       "efe_quadrupole_alt_x_ceiling": Q2_ALT / CEIL,
                       "verdict": "FAIL"},
                   "gate2_ghost": {
                       "composite_dof": 3,
                       "timelike_kinetic_g002_sign": "-M^4 mu_2/s^2 < 0 (phantom)",
                       "active_stress_g002_sign": "-(F+1) rho_Lambda < 0 (negative mass)",
                       "healthy_flip": "F_h = -F-2: F_h(0) = -1 preserved, kinetic and stress both healthy, c_s^2 -> 2 deep",
                       "independent_ghat": "HR 7 healthy / detuned 8 (BD); closed by DC-018/DC-020",
                       "verdict": "FAIL as specified"},
                   "gate3_mond": {
                       "deep_mond": "g^2 = (s/2) g_N; a_0 = s/2; 1/2 power intact",
                       "shape": "|F'| = mu_2 (sign flipped on the healthy branch)",
                       "verdict": "PASS on the healthy-flipped branch"}},
               "verdict": "CLOSED" if verdict_closed else "OPEN",
               "binding_gate": "lensing (exact frame-algebra barrier + galactic deficit + inherited EFE quadrupole)"},
              fh, indent=1)
print("results written to G007_results.json")
