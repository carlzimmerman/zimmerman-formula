# -*- coding: utf-8 -*-
"""CFG172 A2 -- G5: stability (kinetic-sign, decoupling limit), Q2 tail and Cassini, and the G1 x G5 pincer.  Frozen: sec. 2 (G5), 4 (C2, C5).
(i) sympy: khronon perturbation pi on a static background, phi = t + eps*pi, u_mu = -d_mu phi/sqrt(-X), a_mu = h_mu^nu d_nu ln N_phi,
    S = int sqrt(-g) ell(a^2) with the metric held fixed (DECOUPLING LIMIT: no metric mixing, no theta-channel; declared).  Second variation ->
    kinetic coefficients K_x = N (l1 + 2 a^2 l2), K_perp = N l1 (l1 = ell', l2 = ell'') and gradient coefficients.
(ii) Q2 as CFG7 H1: tide = max(|dg_ph/dR|, g_ph/R); Sun's own flow field at Saturn (isolated) and the MW's at the Sun; bound 5.2e-27 s^-2.
(iii) the pincer: the minimum tail any kernel can have if it stays within 10% of the target over y_N = 1/x^2, x in [0.1,30] AND has (y q)' >= 0.
MUTATE = M2 (kernel -> GR, q = 0: G5 Q2 cell must flip to PASS) | M3 (q -> -q: the kinetic-sign cell must flip to FAIL)."""
import sympy as sp
from cfg172_common import *

R = Run("CFG172_A2_stability_pincer")
mut = R.mut
Q2_BOUND = 5.2e-27
GSI = 6.67430e-11
MSUN = 1.98847e30
GMSUN = 1.32712440018e20
AU = 1.495978707e11
KPC = KPC_M

# ---- (i) sympy second variation ------------------------------------------------------------------------------------------
t, x, y_, z, eps = sp.symbols("t x y z epsilon")
Nf = sp.Function("N")(x); pi = sp.Function("pi")(t, x, y_, z)
co = [t, x, y_, z]
g = sp.diag(-Nf ** 2, 1, 1, 1); gi = g.inv()
phi = t + eps * pi
dphi = [sp.diff(phi, c) for c in co]
X = sum(gi[i, i] * dphi[i] ** 2 for i in range(4))
n = -sp.log(-X) / 2
dn = [sp.diff(n, c) for c in co]
ucov = [-d / sp.sqrt(-X) for d in dphi]
uup = [gi[i, i] * ucov[i] for i in range(4)]
a2 = sum(gi[i, i] * dn[i] ** 2 for i in range(4)) + sum(uup[i] * dn[i] for i in range(4)) ** 2
l0, l1, l2 = sp.symbols("l0 l1 l2")
a20 = (sp.diff(Nf, x) / Nf) ** 2
Lg = Nf * (l0 + l1 * (a2 - a20) + l2 * (a2 - a20) ** 2 / 2)
L2 = sp.expand(sp.simplify(sp.diff(Lg, eps, 2).subs(eps, 0) / 2))
names = ["pt", "px", "py", "pz", "ptx", "pty", "ptz", "pxx", "pxy", "pxz", "ptt"]
S = {k: sp.Symbol(k) for k in names}
rep = {sp.Derivative(pi, (t, 2)): S["ptt"], sp.Derivative(pi, t, x): S["ptx"], sp.Derivative(pi, t, y_): S["pty"], sp.Derivative(pi, t, z): S["ptz"],
       sp.Derivative(pi, (x, 2)): S["pxx"], sp.Derivative(pi, x, y_): S["pxy"], sp.Derivative(pi, x, z): S["pxz"],
       sp.Derivative(pi, t): S["pt"], sp.Derivative(pi, x): S["px"], sp.Derivative(pi, y_): S["py"], sp.Derivative(pi, z): S["pz"]}
Nsym, Nx = sp.symbols("Nsym Nx")
L2s = sp.expand(L2.subs(rep).subs(sp.Derivative(Nf, x), Nx).subs(Nf, Nsym))
Pl = sp.Poly(L2s, *S.values())
co_ = {tuple(k for k, e in zip(S.keys(), m) if e for _ in range(e)): c for m, c in Pl.terms()}
a = Nx / Nsym
Kx = sp.simplify(co_[("ptx", "ptx")]); Kp = sp.simplify(co_[("pty", "pty")])
R.check("A2.1 radial kinetic coefficient K_x = N (l1 + 2 a^2 l2), i.e. N (y q)' with q = ell'", str(Kx), sp.simplify(Kx - Nsym * (l1 + 2 * a ** 2 * l2)) == 0)
R.check("A2.2 tangential kinetic coefficient K_perp = N l1 = N q", str(Kp), sp.simplify(Kp - Nsym * l1) == 0)
R.check("A2.3 no pi_tt^2 term survives (no extra time derivatives from the projection)", "absent", ("ptt", "ptt") not in co_)
# gradient coefficients after by-parts (px pxx -> -1/2 c' px^2 etc.), with a' = da/dx = symbol ap
ap = sp.Symbol("ap")
Gx = 3 * Nsym * Nx ** 2 * l1 - sp.simplify(sp.Rational(1, 2) * 2) * (2 * Nsym ** 2 * Nx * l1 / 2 * 2) * 0
# do it explicitly: c(x) = N^2 N' l1 ; (N^2 N' l1)' = 2 N N'^2 l1 + N^2 N'' l1 + N^2 N' l1'
Npp = Nsym * (ap + a ** 2)                      # N'' = N (a' + a^2)
l1p = l2 * 2 * a * ap                            # l1' = l2 (a^2)'
dc = 2 * Nsym * Nx ** 2 * l1 + Nsym ** 2 * Npp * l1 + Nsym ** 2 * Nx * l1p
Gx = sp.simplify(co_[("px", "px")] - dc)          # px^2: 3 N N'^2 l1 minus (c)'
Gp = sp.simplify(co_[("py", "py")] - dc)
R.out["numbers"]["gradient_coeffs_decoupling_limit"] = {"G_x": str(sp.factor(Gx)), "G_perp": str(sp.factor(Gp))}
R.check("A2.4 G_x = -N^3 a' (l1 + 2 a^2 l2)  => omega_x^2 = -G_x/K_x = N^2 a' (kernel-independent; decoupling limit only)",
        str(sp.factor(Gx)), sp.simplify(Gx + Nsym ** 3 * ap * (l1 + 2 * a ** 2 * l2)) == 0)
P("  NOTE (declared): the gradient / characteristic sector in the decoupling limit gives omega_x^2 = N^2 da/dx, a kernel-independent local dynamical rate;"
  " without metric mixing and the theta-channel it is NOT a reliable stability verdict.  Only the kinetic signs are used (they agree with the record's (yq)' >= 0).")

# ---- q(y) functions (numeric) -------------------------------------------------------------------------------------------
def q_true_P2(y):
    y = np.asarray(y, float)
    return 1.0 - (np.sqrt(1.0 + 4 * y * y) - 1.0) / (2 * y)


def q_simple(y):
    return 1.0 / (1.0 + np.asarray(y, float))


def q_exp(y):
    return np.exp(-np.asarray(y, float))


def yqp(qf, y, h=1e-6):
    y = np.asarray(y, float)
    if qf is q_true_P2:                       # analytic, numerically stable: 1 - 2y/sqrt(1+4y^2)
        s_ = np.sqrt(1.0 + 4 * y * y)
        return 1.0 / (s_ * (s_ + 2 * y))
    if qf is q_simple:
        return 1.0 / (1.0 + y) ** 2
    if qf is q_exp:
        return (1.0 - y) * np.exp(-y)
    return (((y * (1 + h)) * qf(y * (1 + h))) - ((y * (1 - h)) * qf(y * (1 - h)))) / (2 * y * h)


yy = np.logspace(-4, 6, 4001)
sgn = -1.0 if mut == "M3" else 1.0
gr = mut == "M2"
qsel = (lambda v: 0.0 * np.asarray(v, float)) if gr else (lambda v: sgn * q_true_P2(v))
qsel_p = (lambda v: 0.0 * np.asarray(v, float)) if gr else (lambda v: sgn * yqp(q_true_P2, v))
# control C2: FC-KH exponential kernel
ys_ = np.logspace(-3, 1.5, 500)
def fd(qf, y, h=1e-6):
    return (((y * (1 + h)) * qf(y * (1 + h))) - ((y * (1 - h)) * qf(y * (1 - h)))) / (2 * y * h)
dev_e = float(np.max(np.abs(fd(q_exp, ys_) - (1 - ys_) * np.exp(-ys_))))
R.check("C2 FC-KH exponential kernel: (y q)' = (1-y) e^{-y} (finite difference vs analytic), negative for 1 < y <= 30 (record: c^2_par < 0 on 1 < y < ~38)",
        f"max dev {dev_e:.1e}; negative on (1,30]: {bool(np.all(yqp(q_exp, ys_[(ys_>1.001)&(ys_<=30)])<0))}",
        dev_e < 1e-6 and bool(np.all(yqp(q_exp, ys_[(ys_ > 1.001) & (ys_ <= 30)]) < 0)))
dev_p = float(np.max(np.abs(fd(q_true_P2, ys_) - yqp(q_true_P2, ys_)) )); dev_s = float(np.max(np.abs(fd(q_simple, ys_) - 1 / (1 + ys_) ** 2)))
R.check("C2b true P2: q > 0 and (y q)' = 1 - 2y/sqrt(1+4y^2) > 0 (finite difference agrees); simple kernel (sensitivity) (y q)' = 1/(1+y)^2 > 0",
        f"dev P2 {dev_p:.1e}, dev simple {dev_s:.1e}; min (yq)'(P2, y<=1e6) {np.min(yqp(q_true_P2, yy)):.2e}; min q {np.min(q_true_P2(yy)):.2e}",
        dev_p < 1e-6 and dev_s < 1e-6 and np.min(yqp(q_true_P2, yy)) > 0 and np.min(q_true_P2(yy)) > 0)
kin_x = qsel_p(yy); kin_p = qsel(yy)
kin_ok = bool(np.all(kin_x >= 0) and np.all(kin_p >= 0))
R.verdict("G5-kinetic-sign (11C-a decoupling limit)", "PASS" if kin_ok else "FAIL", f"K_x=(yq)'>=0 everywhere: {bool(np.all(kin_x>=0))}; K_perp=q>=0: {bool(np.all(kin_p>=0))}")

# ---- 11C-b: q_eff with the theta offset t: (y q_eff)' sign --------------------------------------------------------------------
def yq_eff_prime_negative_fraction(t_off, qf=q_true_P2):
    """q_eff(y) = q(sqrt(y^2 - t)) for y^2 > t, else 0 (Newtonian continuation, declared); returns (fraction of log-y where (y q_eff)'<0, min value)."""
    ys = np.logspace(math.log10(math.sqrt(t_off)) + 1e-9, math.log10(math.sqrt(t_off)) + 4, 6000) if t_off > 0 else np.logspace(-4, 4, 6000)
    w = np.sqrt(np.maximum(ys ** 2 - t_off, 1e-300))
    f = lambda yv: yv * qf(np.sqrt(np.maximum(yv ** 2 - t_off, 1e-300)))
    h = 1e-6
    d = (f(ys * (1 + h)) - f(ys * (1 - h))) / (2 * ys * h)
    return float(np.mean(d < 0)), float(np.min(d))
bneg = {}
for tt in (0.0, 1e-4, 1.0, 3.7e6):
    fr, mn = yq_eff_prime_negative_fraction(tt)
    bneg[str(tt)] = {"neg_fraction_of_4_decades_above_threshold": fr, "min_(y q_eff)'": mn}
    P(f"  11C-b operating offset t={tt:g}: fraction of the 4 decades above threshold with (y q_eff)' < 0 = {fr:.3f}; min = {mn:.3e}")
R.out["numbers"]["b_kinetic_sign_scan"] = bneg
R.verdict("G5-kinetic-sign (11C-b, declared Newtonian continuation of F below the branch point)", "FAIL" if bneg["1.0"]["neg_fraction_of_4_decades_above_threshold"] > 0 else "PASS",
          "radial kinetic coefficient (y q_eff)' turns negative just above the branch point whenever t>0 (analytic: numerator 1 - t/w < 0 for w = sqrt(y^2-t) < t)")

# ---- (ii) Q2 -----------------------------------------------------------------------------------------------------------------
def tide(gph, Rm, gph_fun=None):
    if gph_fun is None:
        return gph / Rm
    d = (gph_fun(Rm * 1.01) - gph_fun(Rm * 0.99)) / (0.02 * Rm)
    return max(abs(d), gph_fun(Rm) / Rm)


RS = 9.537 * AU
Q2 = {}
for f in FOOT:
    a0 = A0_SI[f]
    for kern in ("P2", "nu_mono", "simple"):
        nu = KERNELS[kern]
        if gr:
            gph_fun = lambda Rm: 0.0 * Rm
        else:
            gph_fun = lambda Rm, nu=nu, a0=a0: (float(nu(GMSUN / Rm ** 2 / a0)) - 1.0) * GMSUN / Rm ** 2
        Q2[f"Sun@Saturn/{kern}/{f}"] = tide(0, RS, gph_fun) / Q2_BOUND
P("  Q2 / bound, the Sun's own flow field at Saturn (isolated, no EFE):", {k: f"{v:.2e}" for k, v in Q2.items()})
R.out["numbers"]["Q2_over_bound_sun_saturn"] = Q2
# MW tide at the Sun (CFG7 H1 recipe, reproduced)
MD, RD, MBUL, ABUL, MGAS, RGAS = 4.5e10, 2.6, 0.9e10, 0.5, 1.2e10, 5.0
def M_exp(Md, Rd, Rk):
    s = Rk / Rd
    return Md * (1 - (1 + s) * math.exp(-s))
def gN_MW(Rm):
    Rk = Rm / KPC
    M = M_exp(MD, RD, Rk) + M_exp(MGAS, RGAS, Rk) + MBUL * Rk ** 2 / (Rk + ABUL) ** 2
    return GSI * M * MSUN / Rm ** 2
R0 = 8.2 * KPC
MW = {}
for f in FOOT:
    a0 = A0_SI[f]
    for kern in ("P2", "nu_mono"):
        nu = KERNELS[kern]
        gph = (lambda Rm, nu=nu, a0=a0: (float(nu(gN_MW(Rm) / a0)) - 1.0) * gN_MW(Rm)) if not gr else (lambda Rm: 0.0 * Rm)
        MW[f"{f}/{kern}"] = {"tide": tide(0, R0, gph), "gN": gN_MW(R0), "gph": gph(R0)}
P("  MW phantom tide at the Sun:", {k: f"{v['tide']:.3e}" for k, v in MW.items()})
if not mut:
    R.check("C5b reproduces CFG7 H1's numbers (canonical P2: g_N(R0) = 1.055e-10, tide 1.56e-31; nu_mono 2.20e-31; alt P2 1.83e-31; alt nu_mono 2.56e-31)",
            {k: f"{v['tide']:.3e}" for k, v in MW.items()},
            abs(MW["canonical/P2"]["gN"] / 1.055e-10 - 1) < 5e-3 and abs(MW["canonical/P2"]["tide"] / 1.56e-31 - 1) < 0.03 and abs(MW["canonical/nu_mono"]["tide"] / 2.20e-31 - 1) < 0.03
            and abs(MW["alt/P2"]["tide"] / 1.83e-31 - 1) < 0.03 and abs(MW["alt/nu_mono"]["tide"] / 2.56e-31 - 1) < 0.03)
    R.check("C5 (AS FROZEN) 'the strict-law MW ratio is 4.0-5.7x the ceiling' -- NOT what the H1 recipe gives: the H1 tide is 1.6-2.6e-31 s^-2, i.e. 6e-5 x the bound; the 4.0-5.7 in GATES.md 4.01 has another origin (kept as a failed control)",
            f"H1 tide/bound = {MW['canonical/P2']['tide']/Q2_BOUND:.1e}", 4.0 <= MW["canonical/P2"]["tide"] / Q2_BOUND <= 5.7, load_bearing=False)


# ---- 11C-b Q2 (operating offset t, declared Newtonian continuation) -------------------------------------------------------------------
def gph_b(gN_si, a0, t_off):
    yN_ = gN_si / a0
    def mu(yg):
        u = yg ** 2 - t_off
        return 1.0 - q_true_P2(math.sqrt(u)) if u > 0 else 1.0
    fz = lambda ly: mu(math.exp(ly)) * math.exp(ly) - yN_
    lo, hi = math.log(yN_) - 1e-12, math.log(yN_) + 40
    if fz(lo) >= 0:
        return 0.0
    return (math.exp(brentq(fz, lo, hi, xtol=1e-13)) - yN_) * a0
Q2b = {}
for tt_ in (1.2e-6, 1.0, 4.04e6):
    for f in FOOT:
        a0 = A0_SI[f]
        Q2b[f"Sun@Saturn/t={tt_:g}/{f}"] = tide(0, RS, lambda Rm, a0=a0, tt_=tt_: gph_b(GMSUN / Rm ** 2, a0, tt_)) / Q2_BOUND
        Q2b[f"MW@Sun/t={tt_:g}/{f}"] = tide(0, R0, lambda Rm, a0=a0, tt_=tt_: gph_b(gN_MW(Rm), a0, tt_)) / Q2_BOUND
P("  11C-b Q2 / bound:", {k_: f"{v_:.2e}" for k_, v_ in Q2b.items() if "canonical" in k_})
R.out["numbers"]["Q2_over_bound_11Cb"] = Q2b
R.verdict("G5-Q2 (11C-b, canonical)", "FAIL" if all(v_ > 1 for k_, v_ in Q2b.items() if "Sun@Saturn" in k_ and "canonical" in k_) else "PASS",
          "the Sun's own tail at Saturn is unchanged by the operating offset (y = 7e5 >> sqrt(t)); the MW tide at the Sun is switched off for large t (y_gal << sqrt(t)) at the price of G1")

# ---- (iii) the pincer: minimum tail for any kernel inside the G1 band with (y q)' >= 0 ------------------------------------------------
yN = 1.0 / XGRID ** 2
tails = {}
for kern in ("P2", "nu_mono", "simple"):
    nu = KERNELS[kern]
    ygt = nu(yN) * yN
    lo = 0.9 * ygt - yN
    tail = float(np.max(lo))
    argmax = float(yN[np.argmax(lo)])
    tails[kern] = {"tail_over_a0": tail, "at_yN": argmax}
    for f in FOOT:
        a0 = A0_SI[f]
        tails[kern][f"Q2_over_bound_{f}"] = tail * a0 / RS / Q2_BOUND
P("  minimum tail (units of a0) a kernel must keep if it is within 10% of the target on y_N in [1.1e-3, 100] AND (y q)' >= 0:", {k: round(v['tail_over_a0'], 4) for k, v in tails.items()})
P("  ... Q2/bound at Saturn for that minimal tail:", {k: f"{v['Q2_over_bound_canonical']:.2e}" for k, v in tails.items()})
R.out["numbers"]["pincer_min_tail"] = tails
# explicit construction: A(y_g) = running max of the lower envelope; verify it is inside the band and monotone
ok_c = True
for kern in ("P2",):
    nu = KERNELS[kern]
    ygt = nu(yN) * yN
    lo_y = 0.9 * ygt
    lo_A = lo_y - yN
    order = np.argsort(lo_y)
    A = np.maximum.accumulate(lo_A[order])
    ok_c = bool(np.all(np.diff(A) >= -1e-15))
    # check that y_N + A stays within [0.9, 1.1] y_g,target when applied at y_g = y_N + A (fixed point)
    yg_new = yN[order] + A
    ratio = yg_new / ygt[order]
    ok_c = ok_c and bool(np.all(ratio <= 1.1 + 1e-9) and np.all(ratio >= 0.9 - 1e-9))
R.check("C7 the minimal-tail kernel exists inside the band and is monotone (yq nondecreasing): pincer numerically constructive for P2", f"ok={ok_c}", ok_c)
# verdicts
tail_P2 = tails["P2"]["tail_over_a0"]
q2_actual = min(v for k, v in Q2.items() if k.startswith("Sun@Saturn/P2"))
q2_ok = q2_actual <= 1.0
R.verdict("G5-Q2-Sun-own-field (11C-a, -c; P2)", "PASS" if q2_ok else "FAIL",
          f"Q2/bound = {Q2['Sun@Saturn/P2/canonical']:.2e} (canonical), {Q2['Sun@Saturn/P2/alt']:.2e} (alt)")
R.verdict("G5-pincer (11C-a)", "FAIL" if (tail_P2 * Q2["Sun@Saturn/P2/canonical"] / (0.5) >= 1 and not gr) else "n/a",
          f"any kernel inside the G1 band with (yq)'>=0 keeps a tail >= {tail_P2:.3f} a0 => Q2 >= {tails['P2']['Q2_over_bound_canonical']:.1e} x bound (canonical)")
R.verdict("G5-gamma", "PASS", "Psi = Phi exactly in the static reduction (A1 S1): gamma - 1 = 0 (11C-a, -c; -b same a-channel)")
R.verdict("G5-hyperbolicity / criterion B / gradient sector", "UNDEFINED", "decoupling limit only; metric mixing and the theta-channel not treated")
R.out["numbers"]["Q2_MW"] = MW
if mut == "M2":
    bite = q2_ok
elif mut == "M3":
    bite = not kin_ok
else:
    bite = False
R.finish(bite=(mut != "" and bite))
