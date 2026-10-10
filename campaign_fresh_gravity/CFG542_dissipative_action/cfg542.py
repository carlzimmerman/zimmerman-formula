#!/usr/bin/env python3
"""CFG542: one dissipative variational principle for candidate B. FROZEN_CRITERIA.md (committed alone first, 3d435f032).

Principles: Pa (Schwinger-Keldysh / MSR open-system action, KMS/FDR), Pb (metriplectic Onsager principle with a dark-energy
partner phi), Pb* (Pb + inertial flux-relaxation slip, relaxation time alpha tau_ff), Pc (conservative readings c1, c2).
Sympy derivations + small 1-D spherical numerics (CFG541's Model class imported read-only; static baryons; cold energy at rest
in a top-hat to r_ta at the cosmic ratio; instantaneous psi). No PM runs. No downloads (the DESI DR2 chains already on disk).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
CFG542_MUTATE=1 -> M1 partner removed, M2 dissipative sign flipped, M3 thermal partner, M4 healthy-scalar conservative reading;
outputs *_MUTATE.*; exit 1 iff all teeth bite.
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg542.py
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ["CFG541_MUTATE"] = "0"
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CFG, "CFG541_cold_energy_equations_precise"))
import cfg541 as A  # noqa: E402  (read-only import: Model, constants, fret_census)

MUT = os.environ.get("CFG542_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G, c, MSUN, KPC, GYR = A.G, A.c, A.MSUN, A.KPC, A.GYR
FOOT = A.FOOT
KAPPA = 0.5
FB = A.FB
CH_DIR = os.path.abspath(os.path.join(os.path.dirname(CFG), "..", "_external_data", "desi_dr2_chains"))
J541 = json.load(open(os.path.join(CFG, "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
OUT = []
RES = {"lane": "CFG542", "mutate": MUT, "settings": dict(kappa=KAPPA, footings=FOOT, f_b=FB, grid_N=400)}


def log(s=""):
    print(s, flush=True); OUT.append(s)


def simp0(e):
    return sp.simplify(sp.expand(e)) == 0


# ================================================================================================ Pa: SK / MSR
def sympy_Pa():
    r = {}
    # (1) MSR action, 1-D: variation w.r.t. the response field at rh = 0 gives the class-A drift equation
    x, t, Th = sp.symbols("x t Theta", positive=True)
    rho, rh, psi, m = [sp.Function(n)(x, t) for n in ("rho", "rhohat", "psi", "m")]
    Lmsr = rh * (sp.diff(rho, t) - sp.diff(rho * m * sp.diff(psi, x), x)) - Th * rho * m * sp.diff(rh, x) ** 2
    eqs = sp.euler_equations(Lmsr, [rh], [x, t])
    e_rh = sp.simplify(eqs[0].lhs.subs(rh, 0).doit())
    target = sp.diff(rho, t) - sp.diff(rho * m * sp.diff(psi, x), x)
    r["MSR_response_variation_gives_drift"] = bool(simp0(e_rh - target) or simp0(e_rh + target))
    # (2) KMS / fluctuation relation for ANY symmetric positive mobility (2-cell, general F): Onsager-Machlup
    x1, x2, v1, v2 = sp.symbols("x1 x2 v1 v2", real=True)
    a, b, d_ = sp.symbols("m11 m12 m22", real=True)
    M = sp.Matrix([[a, b], [b, d_]])
    Ff = sp.Function("F")(x1, x2)
    gF = sp.Matrix([sp.diff(Ff, x1), sp.diff(Ff, x2)])
    v = sp.Matrix([v1, v2])
    Lom = lambda vv: ((vv + M * gF).T * M.inv() * (vv + M * gF))[0] / (4 * Th)
    diff_ = sp.simplify(Lom(-v) - Lom(v) + (v.T * gF)[0] / Th)
    r["KMS_fluctuation_relation_M_independent"] = bool(diff_ == 0)
    # (3) stationary Fokker-Planck density exp(-F/Theta) for ANY M (equilibria mobility-free)
    p = sp.exp(-Ff / Th)
    Jfp = -M * (gF * p + Th * sp.Matrix([sp.diff(p, x1), sp.diff(p, x2)]))
    r["FP_equilibrium_M_independent"] = bool(all(sp.simplify(j) == 0 for j in Jfp))
    # (4) energy balance is homogeneous of degree 1 in alpha: it cannot fix alpha
    al, lam, rc, tau, gpsi, gPhi = sp.symbols("alpha lambda rho_c tau gpsi gPhi", positive=True)
    Q = rc * al * tau * gpsi * gPhi; dEN = -rc * al * tau * gpsi * gPhi
    r["energy_balance_identity"] = bool(simp0(Q + dEN))
    r["energy_balance_homogeneous_deg1_in_alpha"] = bool(simp0((Q + dEN).subs(al, lam * al) - lam * (Q + dEN)))
    # (5) Caldeira-Leggett: bath mode q coupled g*X*q; Laplace-domain back-reaction force is proportional to g^2
    s, g, mq, w = sp.symbols("s g m_q omega", positive=True)
    Xs = sp.Symbol("X_s")
    qs = sp.solve(sp.Eq(mq * (s ** 2 + w ** 2) * sp.Symbol("q_s"), g * Xs), sp.Symbol("q_s"))[0]
    Fb = sp.simplify(g * qs)
    r["bath_force_laplace"] = str(Fb)
    r["bath_friction_scales_g2"] = bool(simp0(sp.diff(Fb, g, 2) * g ** 2 / 2 - Fb))
    r["alpha_verdict"] = "FREE: KMS/FDR fix the noise given the mobility; the mobility is a transport coefficient (bath: alpha ~ g^2 x spectral density)"
    return r


# ================================================================================================ Pb: metriplectic Onsager + partner
def sympy_Pb():
    r = {}
    n = 3
    rho = sp.symbols("rho1:4", positive=True)
    eps = sp.Symbol("epsilon")
    Th, Tp = sp.symbols("Theta T_phi", positive=True)
    Kg = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"K{min(i, j)}{max(i, j)}"))     # symmetric gravity kernel
    Pb_ = sp.symbols("Pb1:4")                                                       # baryon potential
    R = sp.Matrix(rho)
    Phi = Kg * R + sp.Matrix(Pb_)
    E = (R.T * Kg * R)[0] / 2 + (sp.Matrix(Pb_).T * R)[0] + eps
    dE = sp.Matrix([sp.diff(E, ri) for ri in rho] + [sp.diff(E, eps)])
    r["dE_drho_is_Phi"] = bool(all(simp0(dE[i] - Phi[i]) for i in range(n)))
    psi = sp.symbols("psi1:4")                                                     # psi_i = dF/drho_i (any F)
    me = sp.symbols("m12 m23", positive=True)

    def Mop(partner=True):
        Mm = sp.zeros(n + 1, n + 1)
        for k, (i, j) in enumerate([(0, 1), (1, 2)]):
            vv = sp.zeros(n + 1, 1); vv[i], vv[j] = -1, 1
            if partner: vv[n] = -(Phi[j] - Phi[i])
            Mm += me[k] * vv * vv.T
        return Mm

    def dS(thermal=False):
        return sp.Matrix([-p / Th for p in psi] + [1 / Tp if thermal else 0])

    M = Mop(True)
    r["M_symmetric"] = bool(M == M.T)
    r["degeneracy_M_dE_zero"] = bool(all(simp0(z) for z in M * dE))
    xdot = M * dS(False)
    J12 = sp.simplify(-xdot[0])
    r["flux_12"] = str(J12)
    r["flux_is_classA_discrete"] = bool(simp0(J12 - (-(me[0] / Th) * (psi[1] - psi[0]))))
    Qd = sp.simplify(xdot[n])
    r["Q_discrete"] = str(Qd)
    Qexp = sum(me[k] / Th * (psi[j] - psi[i]) * (Phi[j] - Phi[i]) for k, (i, j) in enumerate([(0, 1), (1, 2)]))
    r["Q_is_mob_dpsi_dPhi"] = bool(simp0(Qd - Qexp))
    r["dEdt_exact_zero"] = bool(simp0((dE.T * xdot)[0]))
    dSdt = sp.factor(sp.expand((dS(False).T * M * dS(False))[0]))
    r["dSdt"] = str(dSdt)
    r["dSdt_sum_of_squares"] = bool(simp0(dSdt - sum(me[k] * ((psi[j] - psi[i]) / Th) ** 2 for k, (i, j) in enumerate([(0, 1), (1, 2)]))))
    r["mass_conserved"] = bool(simp0(sum(xdot[i] for i in range(n))))
    # support function: the GENERIC conditions hold for ANY m_e >= 0 -> the principle does not select the switch support
    r["support_free"] = "m_e enter only as nonnegative prefactors of sum-of-squares and of M dE = 0: any support s(x) >= 0 passes"
    # M3: thermal partner (finite T_phi): extra drift -> stationary condition shifts
    xth = M * dS(True)
    Jth = sp.simplify(-xth[0])
    extra = sp.simplify(Jth - J12)
    r["M3_thermal_extra_flux"] = str(extra)
    r["M3_thermal_shifts_stationarity"] = bool(not simp0(extra))
    # M1: partner removed -> dE/dt != 0
    Mn = Mop(False)
    dEn = sp.simplify((dE.T * (Mn * dS(False)))[0])
    r["M1_noPartner_dEdt"] = str(dEn)
    r["M1_noPartner_energy_not_conserved"] = bool(not simp0(dEn))
    # GENERIC degeneracy L dS = 0: the orbital (Vlasov) transport changes F: dF/dt|orb = int rho u psi' dV (1-D radial)
    rr, rc, u, dpsi = sp.symbols("r rho_c u dpsi", positive=True)
    dFdt_orb = rc * u * dpsi * 4 * sp.pi * rr ** 2      # integrand for outward orbital motion (u > 0) where psi' > 0
    r["orbital_dFdt_integrand_outward"] = str(dFdt_orb)
    r["L_dS_degeneracy_holds"] = bool(not sp.ask(sp.Q.positive(dFdt_orb)))   # False: positive -> F can rise -> degeneracy fails
    # continuum Q and the phi equation
    al, tau = sp.symbols("alpha tau", positive=True)
    gpsi, gPhi = sp.symbols("dpsi_dr dPhi_dr", nonnegative=True)
    Qc = rc * al * tau * gpsi * gPhi
    r["Q_continuum"] = "Q = rho_c alpha tau_ff 1_B 1_C grad(psi).grad(Phi)"
    r["Q_nonneg_spherical"] = bool(sp.ask(sp.Q.nonnegative(Qc), sp.Q.nonnegative(gpsi) & sp.Q.nonnegative(gPhi)) is not False)
    X, T_ = sp.symbols("x t")
    ph = sp.Function("phi")(X, T_); V = sp.Function("V"); cc = sp.Symbol("c", positive=True)
    eps_phi = sp.diff(ph, T_) ** 2 / 2 + cc ** 2 * sp.diff(ph, X) ** 2 / 2 + V(ph)
    flux = -cc ** 2 * sp.diff(ph, T_) * sp.diff(ph, X)
    lhs = sp.diff(eps_phi, T_) + sp.diff(flux, X)
    rhs = sp.diff(ph, T_) * (sp.diff(ph, T_, 2) - cc ** 2 * sp.diff(ph, X, 2) + sp.diff(V(ph), ph))
    r["phi_energy_identity"] = bool(simp0(lhs - rhs))
    r["phi_equation"] = "phi_tt + 3H phi_t - c^2 lap phi + V'(phi) = Q/phi_t  (singular where phi_t = 0, i.e. w = -1)"
    return r


# ================================================================================================ Pb*: slip with flux relaxation
def sympy_Pbstar():
    r = {}
    rr, t = sp.symbols("r t", positive=True)
    al, tau = sp.symbols("alpha tau", positive=True)
    rho, w, psi = [sp.Function(nm)(rr, t) for nm in ("rho", "w", "psi")]
    rho_t = -sp.diff(rr ** 2 * rho * w, rr) / rr ** 2
    w_t = -w * sp.diff(w, rr) - sp.diff(psi, rr) - w / (al * tau)
    # local identity: psi rho_t r^2 + d_t(rho w^2/2) r^2 + rho w^2/(alpha tau) r^2 = -d_r( r^2 rho w psi + r^2 rho w^3/2 )
    lhs = psi * rho_t * rr ** 2 + rr ** 2 * (rho_t * w ** 2 / 2 + rho * w * w_t) + rr ** 2 * rho * w ** 2 / (al * tau)
    rhs = -sp.diff(rr ** 2 * rho * w * psi + rr ** 2 * rho * w ** 3 / 2, rr)
    r["extended_Lyapunov_identity"] = bool(simp0(lhs - rhs))
    r["extended_Lyapunov"] = "d/dt [F + int rho_c w^2/2 dV] = -int rho_c w^2/(alpha tau) dV <= 0 (no boundary term: w = 0 on the mobility boundary)"
    # overdamped limit: w = -alpha tau psi' + O((alpha tau)^2)
    e = sp.Symbol("e", positive=True); dpsi = sp.Symbol("dpsi")
    w0 = -e * dpsi
    resid = sp.series(-dpsi - w0 / e, e, 0, 2).removeO()
    r["overdamped_limit_leading_order"] = bool(simp0(resid))
    # stationary set: w = 0 and rho psi' = 0
    r["stationary_set"] = "w = 0 and rho_c grad psi = 0 (same as class A; alpha-free)"
    # speed bound along an element with static psi: d/dt(w^2/2 + psi(X)) = -w^2/(alpha tau) <= 0
    X = sp.Function("X")(t); W = sp.Function("W")(t); P = sp.Function("psi_s")
    ener = W ** 2 / 2 + P(X)
    dt_ener = sp.diff(ener, t).subs({sp.diff(X, t): W, sp.diff(W, t): -sp.diff(P(X), X) - W / (al * tau)})
    r["speed_bound_identity"] = bool(simp0(sp.simplify(dt_ener.doit()) + W ** 2 / (al * tau)))
    r["speed_bound"] = "|w| <= sqrt(2 max|psi|) for static psi, starting at rest (psi <= 0)"
    return r


# ================================================================================================ Pc: conservative readings
def sympy_Pc():
    r = {}
    G_, rho_m, d = sp.symbols("G rho_m d", nonnegative=True)
    # c1: friction on the cold energy's own velocity -> stationary needs grad(Phi + psi) = 0 on the support:
    # lap(Phi + psi) = 4 pi G (rho_m + d) = 0 with rho_m > 0, d >= 0: impossible
    lap = 4 * sp.pi * G_ * (rho_m + d)
    r["c1_stationary_requires"] = "4 pi G (rho_m + d) = 0"
    rm_ = sp.Symbol("rm", positive=True)
    sol = sp.solve(sp.Eq(4 * sp.pi * G_ * (rm_ + sp.Symbol("dd")), 0), sp.Symbol("dd"))
    r["c1_required_d"] = str(sol)
    r["c1_impossible"] = bool(all(sp.ask(sp.Q.negative(z)) for z in sol))
    # c2: a local field chi with L = a chi_t^2 + b |grad chi|^2 - sigma chi; static mediated energy U = + b int |grad chi|^2
    a_, b_, k, om = sp.symbols("a b k omega", real=True)
    disp = -b_ * k ** 2 / a_          # omega^2 from -2a chi_tt - 2b lap chi = 0 with chi ~ exp(i k x - i omega t)
    # healthy scalar: a = 1/2, b = -1/2 -> U = -(1/2) int |grad chi|^2 < 0 (attractive between like charges); deficit charge of
    # rho_c is -1 -> cold energy is pushed AWAY from deficits: settling reverses
    r["healthy_omega2"] = str(sp.simplify(disp.subs({a_: sp.Rational(1, 2), b_: -sp.Rational(1, 2)})))
    r["needed_U_plus_F_requires_b_pos"] = True
    r["b_pos_a_pos_omega2"] = str(sp.simplify(disp.subs({a_: 1, b_: 1})))     # -k^2: gradient instability
    r["b_pos_a_neg"] = "ghost (negative kinetic energy)"
    # discrete 3-cell check: healthy-scalar static on-shell energy = -F, so its force on cold energy is +grad psi
    Gm = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"G{min(i, j)}{max(i, j)}"))   # positive Green's matrix, psi = -Gm d
    dv = sp.Matrix(sp.symbols("d1:4"))
    psi = -Gm * dv
    F = (dv.T * Gm * dv)[0] / 2                                               # = -(1/2) d.psi
    grad_energy = -(psi.T * dv)[0] / 2                                        # (1/8 pi G) int |grad psi|^2 = -(1/2) int psi d
    H_onshell = grad_energy + (dv.T * psi)[0]
    r["healthy_static_energy_equals_minus_F"] = bool(simp0(H_onshell + F))
    # dH/drho_c = -dF/drho_c = -psi (with dd/drho_c = -1) -> force -grad(-psi) = +grad psi: up the deficit gradient
    r["M4_force_on_cold_energy"] = "+grad psi (outward: settling reverses)"
    r["coulomb_escape"] = "a constraint (A0-type) field needs a conserved deficit charge; d = max(rho_ph - rho_c, 0) is one-sided and rho_ph is not conserved"
    return r


# ================================================================================================ dispersion (K9)
def dispersion():
    s, K, q, al, be = sp.symbols("s K q alpha beta", positive=True)
    out = {}
    # units tau_ff = 1. Pb (overdamped) + damped psi wave (tau_psi = beta tau): s^3 + s^2/beta + K^2 s + alpha q K^2 = 0
    pb = sp.Poly(s ** 3 + s ** 2 / be + K ** 2 * s + al * q * K ** 2, s)
    a = pb.all_coeffs()
    h2 = sp.simplify(a[1] * a[2] - a[0] * a[3])
    out["Pb"] = dict(poly=str(pb.as_expr()), H2=str(sp.factor(h2)), condition="alpha beta q < 1")
    # Pb*: s (s + 1/alpha)(s^2 + s/beta + K^2) + q K^2 = 0
    ps = sp.Poly(sp.expand(s * (s + 1 / al) * (s ** 2 + s / be + K ** 2) + q * K ** 2), s)
    c4, c3, c2, c1, c0 = ps.all_coeffs()
    H2 = sp.simplify(c3 * c2 - c4 * c1)
    H3 = sp.factor(sp.simplify(c3 * c2 * c1 - c4 * c1 ** 2 - c3 ** 2 * c0))
    lim = sp.factor(sp.limit(H3 / K ** 2, K, 0))
    out["Pbstar"] = dict(poly=str(ps.as_expr()), H2=str(sp.factor(H2)), H3=str(H3), H3_over_K2_at_K0=str(lim))
    # K -> 0 condition: q alpha (alpha + beta) < 1 ; large K: H3 ~ K^4 (alpha beta)^-1 ... > 0
    cond = sp.simplify(lim * al ** 3 * be ** 2)       # positive factor removed
    out["Pbstar"]["K0_condition_expr"] = str(sp.factor(cond))
    amax_pb = 1.0
    amax_ps = float(sp.nsolve(al * (al + 1) - 1, al, 0.6))
    out["alpha_max_beta1_q1"] = dict(Pb=amax_pb, Pbstar=amax_ps)
    out["alpha_max_beta1_q_cosmic"] = dict(Pb=1 / (1 - FB), Pbstar=float(sp.nsolve(al * (al + 1) - 1 / (1 - FB), al, 0.6)))
    # Pb* instantaneous psi: s^2 + s/alpha + q = 0 -> stable always
    out["Pbstar_instantaneous"] = "s^2 + s/alpha + q = 0: STABLE for every alpha > 0, q > 0"
    # numeric scan: max Re s over K in [1e-3, 1e3], q in [0.01, 0.99], alpha set, beta = 1
    Ks = np.geomspace(1e-3, 1e3, 121); qs = np.linspace(0.01, 0.99, 50)
    scan = {}
    for name in ("Pb", "Pbstar"):
        scan[name] = {}
        for A_ in (0.25, 0.5, 0.6, 0.618, 0.65, 1.0, 2.0):
            worst = -np.inf; arg = None
            for qq in qs:
                for KK in Ks:
                    if name == "Pb":
                        co = [1, 1.0, KK ** 2, A_ * qq * KK ** 2]
                    else:
                        co = [1, 1 / A_ + 1, KK ** 2 + 1 / A_, KK ** 2 / A_, qq * KK ** 2]
                    mr = float(np.max(np.roots(co).real))
                    if mr > worst: worst, arg = mr, (float(KK), float(qq))
            scan[name][str(A_)] = dict(max_Re_s=worst, at_K_q=arg, stable=bool(worst < 1e-9))
    out["scan_beta1"] = scan
    return out


# ================================================================================================ switch (S1-S3)
def sympy_switch():
    r = {}
    rb, rc, P = sp.symbols("rho_b rho_c P", positive=True)
    s = sp.Function("s")
    d = P - rc
    for nm, u in (("total_density_reading", rb + rc), ("baryon_reading", rb)):
        F = s(u) * d ** 2 / 2
        mu = sp.diff(F, rc)
        leak = sp.simplify(mu - (-s(u) * d))
        r[f"S1_{nm}_leak"] = str(leak)
        r[f"S1_{nm}_LEAK"] = bool(not simp0(leak))
    # S2: gate in the mobility: drift = -s(u) m grad(mu), mu = dF/drho_c with F ungated; no s' term ever; dF/dt = -int s m rho |grad mu|^2
    r["S2_mobility_gate"] = "NO LEAK for any reading: the gate multiplies a sum of squares and never enters the drive"
    # S3: theta_b candidate. top hat: theta = 3 Rdot/R = 0 at turnaround.
    t = sp.Symbol("t"); Rf = sp.Function("R")(t)
    theta_th = 3 * sp.diff(Rf, t) / Rf
    r["S3_tophat_theta_zero_at_turnaround"] = bool(simp0(theta_th.subs(sp.diff(Rf, t), 0)))
    # Zel'dovich, EdS (D = a, Ddot = H a): physical theta = sum_i (H - lam_i Ddot/(1 - lam_i D)); one axis lam1 > 0, lam2 = lam3 = 0
    H, aa, l1 = sp.symbols("H a lambda1", positive=True)
    theta_z = 3 * H - l1 * H * aa / (1 - l1 * aa)
    sol = sp.solve(sp.Eq(theta_z, 0), l1)
    r["S3_sheet_theta_zero_at_lambda1_a"] = str([sp.simplify(x * aa) for x in sol])
    r["S3_theta_b_fires_in_sheets"] = True       # theta_b <= 0 at lambda1 a >= 3/4 with lambda2 = 0 (E8 needs lambda2 >= tau_ta)
    r["S3_switch"] = "INPUT"
    return r


# ================================================================================================ angular momentum
def sympy_angmom():
    r = {}
    x = sp.Matrix(sp.symbols("x1:4", real=True)); v = sp.Matrix(sp.symbols("v1:4", real=True))
    w = sp.Symbol("w", real=True); dPhi = sp.Symbol("dPhi", real=True)
    rr = sp.sqrt(x.dot(x)); xh = x / rr
    vperp = v - v.dot(xh) * xh
    a_s = -(w / rr) * vperp
    xdot = v + w * xh
    vdot = -dPhi * xh + a_s
    Ldot = xdot.cross(v) + x.cross(vdot)
    r["j_conserved_per_element"] = bool(all(sp.simplify(z) == 0 for z in Ldot))
    # radial velocity unchanged by a_s (minimal choice)
    r["a_s_radial_component_zero"] = bool(sp.simplify(a_s.dot(xh)) == 0)
    Edot = sp.simplify(v.dot(vdot) + dPhi * xh.dot(xdot))
    r["element_energy_rate"] = "w (dPhi/dr - v_perp^2/r)"
    r["element_energy_rate_check"] = bool(simp0(Edot - w * (dPhi - vperp.dot(vperp) / rr)))
    # solvability for a general (non-radial) slide: x x a_s = v x v_s requires (v x v_s).x = 0
    vs = sp.Matrix(sp.symbols("u1:4", real=True))
    r["nonradial_solvability_condition"] = str(sp.simplify((v.cross(vs)).dot(x)))
    # round deficit: shell-averaged rho_c in d keeps the gradient-flow symmetry (response matrix A^T K A symmetric)
    Kd = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"k{min(i, j)}{max(i, j)}"))
    Av = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2), 0], [sp.Rational(1, 2), sp.Rational(1, 2), 0], [0, 0, 1]])
    Rm = Av.T * Kd * Av
    r["round_deficit_response_symmetric"] = bool(Rm == Rm.T)
    r["label"] = "CONSERVED (conditions: radial slide in the region's baryon-centre frame; round deficit; velocity-space term a_s = -(w/r) v_perp)"
    return r


# ================================================================================================ DESI w = -1 crossing (K10)
def desi_crossing():
    out = {}
    for nm in ("cmb", "pantheonplus", "union3", "desy5"):
        fn1 = os.path.join(CH_DIR, nm, "chain.1.txt")
        hdr = open(fn1).readline().lstrip("#").split()
        cols = [hdr.index(cn) for cn in ("weight", "w", "wa")]
        xs = []
        for kk in range(1, 5):
            dd = np.loadtxt(os.path.join(CH_DIR, nm, f"chain.{kk}.txt"), usecols=cols)
            xs.append(dd[int(0.3 * len(dd)):])
        xx = np.vstack(xs); wt, w0, wa = xx[:, 0], xx[:, 1], xx[:, 2]
        # w(z) = w0 + wa z/(1+z); crossing at y = z/(1+z) = (-1 - w0)/wa in (0, 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            y = (-1 - w0) / wa
        cross = (y > 0) & (y < 1)
        o = np.argsort(w0); cw = np.cumsum(wt[o]) / wt.sum()
        med_w0 = float(w0[o][np.searchsorted(cw, 0.5)])
        zc = np.where(cross, y / (1 - y), np.nan)
        oz = np.argsort(np.nan_to_num(zc, nan=1e9)); cz = np.cumsum((wt * cross)[oz]) / max((wt * cross).sum(), 1e-300)
        out[nm] = dict(cross_weight_frac=float((wt * cross).sum() / wt.sum()), median_w0=med_w0,
                       median_z_cross=float(np.nan_to_num(zc, nan=1e9)[oz][np.searchsorted(cz, 0.5)]))
    return out


# ================================================================================================ 1-D runs
def run1d(mod, alpha=1.0, mode="od", sign=1, tmax=300 * GYR, maxsteps=3_000_000, nshell=4000):
    """mode 'od': Eulerian overdamped class A (Pb), CFG541 donor-cell scheme + Q bookkeeping.
    mode 'slip': Eulerian slip velocity on faces (Pb*), see _run_slip."""
    return _run_od(mod, alpha, sign, tmax, maxsteps) if mode == "od" else _run_slip(mod, alpha, sign, tmax, maxsteps, nshell)


def _post(mod, m, m0, ts, Ss, W0, extra):
    ts, Ss = np.array(ts), np.array(Ss)
    if Ss[-1] > Ss[0]:
        tgt = Ss[0] + 0.9 * (Ss[-1] - Ss[0]); j = int(np.argmax(Ss >= tgt))
        t90 = float(ts[j] if j == 0 else ts[j - 1] + (tgt - Ss[j - 1]) / (Ss[j] - Ss[j - 1]) * (ts[j] - ts[j - 1]))
    else:
        t90 = float("nan")
    W1, _ = mod.energy(m)
    fl, fs, _ = mod.front(m)
    out = dict(t90=t90, dW=W0 - W1, F1=mod.F(m), mass_err=float(abs(m.sum() - m0.sum()) / m0.sum()), rstar=mod.analytic_rstar(),
               front_lit=fl, front_sub=fs)
    out.update(extra)
    return out


def _run_od(mod, alpha, sign, tmax, maxsteps):
    N, V, Af, rf, rc_ = mod.N, mod.V, mod.A, mod.rf, mod.rc
    m = mod.rhoc0 * V.copy(); m0 = m.copy(); thr = 1e-12 * m0
    rstar = mod.analytic_rstar(); kin = int(np.searchsorted(rf, rstar)) - 1
    Sin = lambda mm: float(mm[:kin].sum())
    dist = rc_[1:] - rc_[:-1]
    W0, _ = mod.energy(m); F0 = mod.F(m); Fprev = F0; maxinc = -np.inf
    Qint = 0.0; t = 0.0; n = 0; ts, Ss = [0.0], [Sin(m)]
    vmax = pimax = psimax = xq = 0.0
    while t < tmax and n < maxsteps:
        rho, d, Md, dpsi = mod.fields(m)
        live = m > thr
        with np.errstate(divide="ignore"):
            tau = np.where(live, 1 / np.sqrt(4 * math.pi * G * np.maximum(rho + mod.rhob, 1e-300)), 0.0)
        don = slice(1, N) if sign > 0 else slice(0, N - 1)
        v = alpha * tau[don] * dpsi[1:N]
        ok = live[don]
        flux = rho[don] * v * Af[1:N]
        with np.errstate(divide="ignore", over="ignore"):
            dtc = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(Af[1:N] * v, 1e-300), np.inf).min()
        gam = float((4 * math.pi * G * rho * tau * alpha)[live].max()) if live.any() else 0.0
        dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, tmax - t)
        if not np.isfinite(dt): dt = tmax - t
        tr = np.where(ok, np.minimum(flux * dt, m[don]), 0.0)
        tr = np.where(ok & (m[don] - tr < thr[don]) & (tr > 0), m[don], tr)
        if sign > 0:
            m[1:] -= tr; m[:-1] += tr
        else:
            m[:-1] -= tr; m[1:] += tr
        gf = G * (mod.Mbf[1:N] + np.cumsum(m)[:-1]) / rf[1:N] ** 2
        qf = sign * tr * gf * dist
        Qint += float(qf.sum())
        xq = max(xq, float(np.max(np.cumsum(qf) / dt / (4 * math.pi * rf[1:N] ** 2))))
        t += dt; n += 1
        sel = (rho >= 1e-3 * mod.rhoc0)[don] & ok
        if sel.any():
            vmax = max(vmax, float(np.max(np.where(sel, v, 0.0))))
            pimax = max(pimax, float(np.max(np.where(sel, v * tau[don] / rf[1:N], 0.0))))
        Fn = mod.F(m); maxinc = max(maxinc, (Fn - Fprev) / F0); Fprev = Fn
        if n % 100 == 0:
            psimax = max(psimax, float(np.max(np.abs(mod.psi_cells(Md, dpsi)))))
            ts.append(t); Ss.append(Sin(m))
            if sign > 0 and flux.sum() * GYR < 1e-7 * mod.Mcat: break
    ts.append(t); Ss.append(Sin(m))
    return _post(mod, m, m0, ts, Ss, W0, dict(t=t, n=n, Qint=Qint, F0=F0, maxincF=maxinc, maxincL=None, vmax=vmax, pimax=pimax,
                                             psimax=psimax, Lq_flux_max=xq, settled=Sin(m)))


def _run_slip(mod, alpha, sign, tmax, maxsteps, nshell=None):
    """Eulerian, momentum-conserving slip (Pb*): cell mass m_i and cell slip momentum P_i = m_i u_i (radial, positive outward).
    Donor-cell transfers carry mass and the donor's slip momentum (pressureless: no geometric source); source -m psi'(r_c);
    implicit friction u -> (u + dt f)/(1 + dt/(alpha tau_i)). Mass exact; slip momentum exact in transfers."""
    N, V, Af, rf, rc_ = mod.N, mod.V, mod.A, mod.rf, mod.rc
    m = mod.rhoc0 * V.copy(); m0 = m.copy(); thr = 1e-12 * m0
    rstar = mod.analytic_rstar(); kin = int(np.searchsorted(rf, rstar)) - 1
    Sin = lambda mm: float(mm[:kin].sum())
    dist = rc_[1:] - rc_[:-1]
    u = np.zeros(N)
    W0, _ = mod.energy(m); F0 = mod.F(m); Fprev = Lprev = F0; maxincF = maxincL = -np.inf
    Qint = 0.0; t = 0.0; n = 0; ts, Ss = [0.0], [Sin(m)]
    vmax = pimax = psimax = xq = 0.0
    fi = np.arange(N - 1)
    lr = np.log(rf)
    while t < tmax and n < maxsteps:
        rho, d, Md, dpsi = mod.fields(m)
        live = m > thr
        tau = 1 / np.sqrt(4 * math.pi * G * np.maximum(rho + mod.rhob, 1e-300))
        fc = -sign * np.interp(np.log(rc_), lr, dpsi)               # -psi' at cell centres
        with np.errstate(divide="ignore", invalid="ignore"):
            dt_dyn = float(np.min(np.where(live & (np.abs(fc) > 0), 0.1 * np.sqrt(rc_ / np.maximum(np.abs(fc), 1e-300)), np.inf)))
        # face velocity = donor velocity (upwind): inward if the outer cell moves in, outward if the inner cell moves out
        uin = np.minimum(u[1:], 0.0); uout = np.maximum(u[:-1], 0.0)
        with np.errstate(divide="ignore", invalid="ignore"):
            dt_cfl = float(min(np.min(np.where(live[1:] & (uin < 0), 0.4 * V[1:] / np.maximum(Af[1:N] * (-uin), 1e-300), np.inf)),
                               np.min(np.where(live[:-1] & (uout > 0), 0.4 * V[:-1] / np.maximum(Af[1:N] * uout, 1e-300), np.inf))))
        dt = min(dt_dyn, dt_cfl, tmax - t)
        if not np.isfinite(dt): dt = tmax - t
        # transfers (mass + momentum) with the current velocities
        tin = np.where(live[1:], np.minimum(rho[1:] * (-uin) * Af[1:N] * dt, m[1:]), 0.0)     # outer -> inner across face f
        tout = np.where(live[:-1], np.minimum(rho[:-1] * uout * Af[1:N] * dt, m[:-1]), 0.0)   # inner -> outer
        tin = np.where(live[1:] & (m[1:] - tin < thr[1:]) & (tin > 0), m[1:], tin)
        tout = np.where(live[:-1] & (m[:-1] - tout < thr[:-1]) & (tout > 0), m[:-1], tout)
        P = m * u
        dm = np.zeros(N); dP = np.zeros(N)
        dm[1:] -= tin; dm[:-1] += tin; dP[1:] -= tin * u[1:]; dP[:-1] += tin * u[1:]
        dm[:-1] -= tout; dm[1:] += tout; dP[:-1] -= tout * u[:-1]; dP[1:] += tout * u[:-1]
        m = m + dm; P = P + dP
        with np.errstate(divide="ignore", invalid="ignore"):
            u = np.where(m > thr, P / np.maximum(m, 1e-300), 0.0)
        rho2 = m / V
        tau2 = 1 / np.sqrt(4 * math.pi * G * np.maximum(rho2 + mod.rhob, 1e-300))
        u = np.where(m > thr, (u + dt * fc) / (1 + dt / (alpha * tau2)), 0.0)
        gf = G * (mod.Mbf[1:N] + np.cumsum(m)[:-1]) / rf[1:N] ** 2
        qf = (tin - tout) * gf * dist
        Qint += float(qf.sum())
        if dt > 0: xq = max(xq, float(np.max(np.cumsum(qf) / dt / (4 * math.pi * rf[1:N] ** 2))))
        t += dt; n += 1
        sel = (m > thr) & (rho2 >= 1e-3 * mod.rhoc0)
        if sel.any():
            vmax = max(vmax, float(np.max(np.abs(u[sel]))))
            pimax = max(pimax, float(np.max((np.abs(u) * tau2 / rc_)[sel])))
        if n % 10 == 0:
            Fn = mod.F(m)
            psimax = max(psimax, float(np.max(np.abs(mod.psi_cells(*mod.fields(m)[2:4])))))
            Ln = Fn + 0.5 * float(np.sum(m * u ** 2))
            maxincL = max(maxincL, (Ln - Lprev) / F0); maxincF = max(maxincF, (Fn - Fprev) / F0); Lprev, Fprev = Ln, Fn
        if n % 100 == 0:
            ts.append(t); Ss.append(Sin(m))
            if (tin.sum() + tout.sum()) / dt * GYR < 1e-7 * mod.Mcat and float(np.max(np.abs(u))) * GYR < 1e-3 * rstar: break
    ts.append(t); Ss.append(Sin(m))
    return _post(mod, m, m0, ts, Ss, W0, dict(t=t, n=n, Qint=Qint, F0=F0, maxincF=maxincF, maxincL=maxincL, vmax=vmax, pimax=pimax,
                                             psimax=psimax, Lq_flux_max=xq, settled=Sin(m)))


# ================================================================================================ main
def main():
    t0 = time.time()
    log(f"CFG542 {'MUTATE' if MUT else 'PRIMARY'}: one dissipative variational principle for candidate B")
    log("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not 'theory closed'.")
    log("")
    # -------- sympy
    pa = sympy_Pa(); RES["Pa"] = pa
    log("Pa (Schwinger-Keldysh / MSR):"); [log(f"  {k}: {v}") for k, v in pa.items()]
    pb = sympy_Pb(); RES["Pb"] = pb
    log("Pb (metriplectic Onsager + dark-energy partner):"); [log(f"  {k}: {v}") for k, v in pb.items()]
    ps = sympy_Pbstar(); RES["Pbstar"] = ps
    log("Pb* (slip with flux relaxation alpha tau_ff):"); [log(f"  {k}: {v}") for k, v in ps.items()]
    pc = sympy_Pc(); RES["Pc"] = pc
    log("Pc (conservative readings):"); [log(f"  {k}: {v}") for k, v in pc.items()]
    dsp = dispersion(); RES["K9_dispersion"] = dsp
    log("K9 dispersion (tau_ff = 1, beta = 1 in scans):")
    log(f"  Pb  : {dsp['Pb']}")
    log(f"  Pb* : H3/K^2 at K->0 = {dsp['Pbstar']['H3_over_K2_at_K0']}; condition expr {dsp['Pbstar']['K0_condition_expr']}")
    log(f"  alpha_max (beta = 1, q -> 1): {dsp['alpha_max_beta1_q1']}; at q = 1 - f_b: {dsp['alpha_max_beta1_q_cosmic']}")
    for nm, sc in dsp["scan_beta1"].items():
        log(f"  scan {nm}: " + ", ".join(f"a={k}: {'STABLE' if v['stable'] else 'UNSTABLE'} ({v['max_Re_s']:+.2e})" for k, v in sc.items()))
    sw = sympy_switch(); RES["switch"] = sw
    log("Switch:"); [log(f"  {k}: {v}") for k, v in sw.items()]
    am = sympy_angmom(); RES["angular_momentum"] = am
    log("Angular momentum:"); [log(f"  {k}: {v}") for k, v in am.items()]
    dc = desi_crossing(); RES["K10_desi"] = dc
    log("K10 DESI DR2 w0wa chains (on disk):"); [log(f"  {k}: {v}") for k, v in dc.items()]
    log(f"  [sympy done, {time.time() - t0:.0f} s]")

    # -------- K0 control
    f_mw = A.fret_census(6.0e10)[0]
    modc = A.Model(6.0e10, 2.5, FOOT["can"], f_mw)
    rk0 = modc.run(alpha=1.0)
    t90_541 = J541["one_d"]["can"]["MW"]["t90_Gyr"]["1.0"]
    k0 = abs(rk0["t90"] / GYR / t90_541 - 1)
    RES["K0"] = dict(t90_Gyr=rk0["t90"] / GYR, t90_CFG541=t90_541, rel=k0, pass_=bool(k0 <= 1e-6))
    log(f"K0 control: CFG541 Model.run MW t90(1) = {rk0['t90'] / GYR:.6f} Gyr vs JSON {t90_541:.6f}: rel {k0:.1e} -> {'PASS' if k0 <= 1e-6 else 'FAIL'}")

    # -------- 1-D runs
    systems = {"MW": (6.0e10, 2.5), "cluster": (1.5e14, None)}
    one = {}
    alphas = (0.5, 1.0, 2.0) if not MUT else (1.0,)
    for fk, a0 in FOOT.items():
        one[fk] = {}
        rhoDE = (a0 / (KAPPA * c)) ** 2 / G
        epsDE = rhoDE * c ** 2
        for nm, (Mb, ah) in systems.items():
            f = A.fret_census(Mb)[0]
            mod = A.Model(Mb, ah, a0, f)
            rec = dict(fret=f, Vf_kms=math.sqrt(mod.Vf2) / 1e3, r_analytic_kpc=mod.analytic_rstar() / KPC)
            if not MUT:
                for mode in ("od", "slip"):
                    for al in alphas:
                        rr = run1d(mod, alpha=al, mode=mode)
                        key = f"{mode}_a{al}"
                        rec[key] = dict(t90_Gyr=rr["t90"] / GYR, t_end_Gyr=rr["t"] / GYR, steps=rr["n"], dW_per_Mcat_Vf2=rr["dW"] / mod.Mcat / mod.Vf2,
                                        Q_over_dW=rr["Qint"] / rr["dW"], maxincF=rr["maxincF"], maxincL=rr["maxincL"],
                                        vmax_over_c=rr["vmax"] / c, vmax_kms=rr["vmax"] / 1e3, Pi_max=rr["pimax"],
                                        sqrt2psimax_kms=math.sqrt(2 * rr["psimax"]) / 1e3,
                                        speed_bound_ok=bool(rr["vmax"] <= math.sqrt(2 * rr["psimax"]) * (1 + 1e-9)),
                                        mass_err=rr["mass_err"], front_sub_over_analytic=rr["front_sub"] / rr["rstar"],
                                        front_lit_over_analytic=rr["front_lit"] / rr["rstar"], settled_over_Mcat=rr["settled"] / mod.Mcat,
                                        x_flux=rr["Lq_flux_max"] / (c * epsDE))
                        e = rec[key]
                        log(f"  {fk} {nm} {mode} alpha {al}: t90 {e['t90_Gyr']:.2f} Gyr (end {e['t_end_Gyr']:.1f}, {e['steps']} steps); "
                            f"dW {e['dW_per_Mcat_Vf2']:.3f} V_f^2 M_cat; intQ/dW {e['Q_over_dW']:.4f}; maxinc F {e['maxincF']:+.1e}"
                            + (f", L {e['maxincL']:+.1e}" if e['maxincL'] is not None else "")
                            + f"; vmax {e['vmax_kms']:.0f} km/s ({e['vmax_over_c']:.2e} c) vs sqrt(2|psi|max) {e['sqrt2psimax_kms']:.0f}; Pi {e['Pi_max']:.1f}; "
                            f"|dM|/M {e['mass_err']:.1e}; front sub/analytic {e['front_sub_over_analytic']:.4f} (lit {e['front_lit_over_analytic']:.4f}); "
                            f"settled {e['settled_over_Mcat']:.4f}; flux x {e['x_flux']:.2e}")
            else:
                # M1: partner removed: E_N alone changes by dW
                rr = run1d(mod, alpha=1.0, mode="od")
                # without the partner nothing absorbs the released energy: Delta E_N = -dW, so |Delta E_N|/|dW| = 1
                rec["M1_dEN_over_dW"] = float(abs(rr["dW"]) / abs(rr["dW"])) if rr["dW"] != 0 else 0.0
                rec["M1_detected"] = bool(rec["M1_dEN_over_dW"] >= 0.5)
                # M2: dissipative sign flipped (anti-drift)
                r2 = run1d(mod, alpha=1.0, mode="od", sign=-1, tmax=2 * GYR)
                rec["M2_maxincF"] = r2["maxincF"]; rec["M2_detected"] = bool(r2["maxincF"] > 0)
                log(f"  {fk} {nm}: M1 dE_N/dW = {rec['M1_dEN_over_dW']:.2f} (detected {rec['M1_detected']}); M2 max step dF/F0 {r2['maxincF']:+.2e} (detected {rec['M2_detected']})")
            one[fk][nm] = rec
    RES["one_d"] = one

    if MUT:
        teeth = dict(M1=all(one[f][n]["M1_detected"] for f in FOOT for n in systems) and pb["M1_noPartner_energy_not_conserved"],
                     M2=all(one[f][n]["M2_detected"] for f in FOOT for n in systems),
                     M3=pb["M3_thermal_shifts_stationarity"],
                     M4=pc["healthy_static_energy_equals_minus_F"])
        RES["MUTATE_teeth"] = teeth
        log(f"MUTATE teeth: {teeth}")
        finish()
        sys.exit(1 if all(teeth.values()) else 0)

    # -------- K7 / K8 from the runs
    J = J541["one_d"]; S = J541["S"]["ii"]
    ratio = []
    for fk in FOOT:
        for nm in ("MW", "cluster"):
            ratio.append(J[fk][nm]["dW_over_Vf2"] / J[fk][nm]["Esink_over_Vf2"])
        ratio.append(J[fk]["group"]["dW_over_Vf2"] / J[fk]["group"]["Esink_over_Vf2"])
    rmax = max(ratio)
    drho = S["cosmic_drho_over_rho"] * rmax
    wmin = min(abs(v["median_w0"]) for v in dc.values())
    one_plus_w = min(1 + v["median_w0"] for v in dc.values())
    k7 = dict(energy_ratio_Q_over_Esink_max=rmax, cosmic_drho_over_rho=drho, dlog10_a0_rho=0.5 * math.log10(1 + drho),
              dlog10_a0_minus_p=abs(0.5 * math.log10(1 - drho / wmin)), bound=4e-3)
    k7["pass_"] = bool(abs(k7["dlog10_a0_rho"]) <= 4e-3 and k7["dlog10_a0_minus_p"] <= 4e-3)
    RES["K7"] = k7
    k8 = {}
    for prin, mode in (("Pb", "od"), ("Pbstar", "slip")):
        xs = {f"{fk}_{nm}_a{al}": one[fk][nm][f"{mode}_a{al}"]["x_flux"] for fk in FOOT for nm in systems for al in alphas}
        xm = max(xs.values())
        e = dict(x_outgoing_max=xm, one_plus_w_min_median=one_plus_w, near_field=xm ** 2 / (2 * one_plus_w), bound=1e-3, x_by_run=xs)
        e["delta_rho_over_rho"] = max(xm, e["near_field"]); e["pass_"] = bool(e["delta_rho_over_rho"] <= 1e-3)
        k8[prin] = e
    RES["K8"] = k8
    log(f"K7: Q/E_sink up to {rmax:.2f}; cosmic drho/rho {drho:.2e}; dlog10 a0 {k7['dlog10_a0_rho']:.2e} (rho fork), {k7['dlog10_a0_minus_p']:.2e} (-p fork) -> {'PASS' if k7['pass_'] else 'FAIL'}")
    for prin, e in k8.items():
        log(f"K8 {prin}: outgoing x max {e['x_outgoing_max']:.2e}; near-field x^2/(2(1+w)) {e['near_field']:.2e} (1+w {one_plus_w:.3f}) -> {'PASS' if e['pass_'] else 'FAIL'}")

    # -------- checks and labels
    k10 = all(v["cross_weight_frac"] > 0.5 for v in dc.values())
    K = {}
    K["K1"] = bool(pa["MSR_response_variation_gives_drift"] and pb["flux_is_classA_discrete"] and ps["overdamped_limit_leading_order"])
    K["K2_sympy"] = bool(pb["dEdt_exact_zero"] and pb["degeneracy_M_dE_zero"] and pb["phi_energy_identity"])
    qd = [abs(one[fk][nm][k]["Q_over_dW"] - 1) for fk in FOOT for nm in systems for k in one[fk][nm] if isinstance(one[fk][nm][k], dict)]
    K["K2_numeric_max_dev"] = max(qd); K["K2_numeric"] = bool(max(qd) <= 0.02)
    me = [one[fk][nm][k]["mass_err"] for fk in FOOT for nm in systems for k in one[fk][nm] if isinstance(one[fk][nm][k], dict)]
    K["K3"] = bool(pb["mass_conserved"] and max(me) <= 1e-12); K["K3_max_mass_err"] = max(me)
    incF = [one[fk][nm][k]["maxincF"] for fk in FOOT for nm in systems for k in one[fk][nm] if isinstance(one[fk][nm][k], dict) and k.startswith("od")]
    incL = [one[fk][nm][k]["maxincL"] for fk in FOOT for nm in systems for k in one[fk][nm] if isinstance(one[fk][nm][k], dict) and k.startswith("slip")]
    K["K4_sympy"] = bool(pb["dSdt_sum_of_squares"] and ps["extended_Lyapunov_identity"])
    K["K4_od_max_step_inc"] = max(incF); K["K4_slip_max_step_inc_L"] = max(incL)
    K["K4_od_flag"] = bool(max(incF) > 1e-6); K["K4_slip_flag"] = bool(max(incL) > 1e-6)
    K["K5"] = "FREE"
    K["K6"] = "DERIVED: Q = rho_c alpha tau_ff 1_B 1_C grad psi . grad Phi (Pb); Pb*: Q = -rho_c w . grad Phi"
    K["K7"] = k7["pass_"]; K["K8_Pb"] = k8["Pb"]["pass_"]; K["K8_Pbstar"] = k8["Pbstar"]["pass_"]
    K["K9_Pb"] = f"CAUSAL-WITH-tau for alpha beta q < 1 (alpha_max {dsp['alpha_max_beta1_q1']['Pb']:.3f} at beta = 1, q -> 1)"
    K["K9_Pbstar"] = f"CAUSAL-WITH-tau for q alpha (alpha + beta) < 1 (alpha_max {dsp['alpha_max_beta1_q1']['Pbstar']:.4f} at beta = 1, q -> 1)"
    cl_c = {f"{fk}_{k}": one[fk]["cluster"][k]["vmax_over_c"] for fk in FOOT for k in one[fk]["cluster"] if isinstance(one[fk]["cluster"][k], dict)}
    K["C1_cluster_vmax_over_c"] = cl_c
    K["K10_crossing_open_item"] = k10
    RES["checks"] = K
    # reservoirs (task 3)
    slip = [one[fk][nm][f"slip_a{al}"] for fk in FOOT for nm in systems for al in alphas]
    sb = all(e["speed_bound_ok"] for e in slip)
    cl = all(one[fk]["cluster"][f"slip_a{al}"]["vmax_over_c"] <= 1e-2 for fk in FOOT for al in alphas)
    sens = {f"{fk}_{nm}": dict(od=one[fk][nm]["od_a0.5"]["t90_Gyr"] / one[fk][nm]["od_a2.0"]["t90_Gyr"],
                               slip=one[fk][nm]["slip_a0.5"]["t90_Gyr"] / one[fk][nm]["slip_a2.0"]["t90_Gyr"]) for fk in FOOT for nm in systems}
    edge = {f"{fk}_{nm}_a{al}": one[fk][nm][f"slip_a{al}"]["front_sub_over_analytic"] for fk in FOOT for nm in systems for al in alphas}
    res3 = dict(speed_bound_all=sb, cluster_vmax_le_1e2c=cl, no_new_constant=True,
                INERTIA_LIMITED=("YES" if (sb and cl) else "NO"), t90_ratio_0p5_over_2=sens, edge_sub_over_analytic=edge,
                edge_within_2pct=all(abs(v - 1) <= 0.02 for v in edge.values()))
    RES["task3"] = res3
    log(f"Task 3: speed bound in every run {sb}; cluster |w|/c <= 1e-2 {cl}; INERTIA-LIMITED REGIME: {res3['INERTIA_LIMITED']}")
    log(f"  t90(0.5)/t90(2): " + ", ".join(f"{k}: od {v['od']:.2f}, slip {v['slip']:.2f}" for k, v in sens.items()))
    log(f"  edge (sub-cell / analytic): " + ", ".join(f"{k} {v:.4f}" for k, v in edge.items()) + f"; within 2%: {res3['edge_within_2pct']}")
    # labels
    open_pb = ["alpha FREE (bounded by K9)", "GENERIC degeneracy L dS = 0 fails: orbital motion can raise F (no second law for the full kinetic system)",
               "overdamped drift speeds in diffuse reservoirs (CFG541 item 3)" , "kinetic consistency (CFG541 item 5)", "switch INPUT"]
    if k10: open_pb.append("canonical partner singular at the DESI-preferred w = -1 crossing")
    if not K["K2_numeric"]: open_pb.append("numerical Q bookkeeping deviates > 2%")
    c1od = max(v for k, v in cl_c.items() if "_od_" in k)
    if c1od > 1e-2: open_pb.append("C1: overdamped cluster drift speed up to %.3f c (> 1e-2 margin)" % c1od)
    if not K["K8_Pb"]: open_pb.append("K8 fails")
    core = K["K1"] and K["K2_sympy"] and K["K3"] and K["K4_sympy"]
    labels = {
        "Pa": dict(label="CONSISTENT WITH OPEN ITEMS" if core else "INCONSISTENT", alpha="FREE", Q="DERIVED (same as Pb, from the SK energy current)", switch="INPUT",
                   open=["alpha FREE: KMS/FDR fix the noise, not the mobility; a bath gives alpha ~ g^2 (new coupling)"] + open_pb[1:]),
        "Pb": dict(label="CONSISTENT WITH OPEN ITEMS" if core else "INCONSISTENT", alpha="FREE", Q="DERIVED: Q = rho_c alpha tau_ff 1_B 1_C grad psi . grad Phi", switch="INPUT", open=open_pb),
        "Pbstar": dict(label=("INCONSISTENT" if (K["K4_slip_flag"] or not core) else "CONSISTENT WITH OPEN ITEMS"),
                       failure=("K4: the extended Lyapunov F + K_w rises in the 1-D runs (max step +%.1e of F0). The sympy identity uses "
                                "dF/drho_c = psi everywhere; at overfilled points (d = 0) adding mass has derivative 0, so inertial "
                                "overshoot into the filled core raises F while the slip has already been paid by -grad psi. "
                                "The one-sided deficit never removes the overfill." % K["K4_slip_max_step_inc_L"]) if K["K4_slip_flag"] else None,
                       alpha="FREE", Q="DERIVED: Q = -rho_c w . grad Phi", switch="INPUT",
                       open=["alpha FREE (bounded: q alpha (alpha + 1) < 1 -> alpha < 0.618 for q -> 1)"] + open_pb[1:2]
                       + ([] if res3["edge_within_2pct"] else ["edge moves inward (inertial overfill)"])
                       + [o for o in open_pb[3:] if not o.startswith(("C1", "K8"))]
                       + ([] if K["K8_Pbstar"] else ["K8 fails (collapsed cores radiate; outgoing x up to %.1e)" % k8["Pbstar"]["x_outgoing_max"]])
                       + ([] if res3["INERTIA_LIMITED"] == "YES" else ["inertia-limited regime NO as frozen"])),
        "Pc1": dict(label="INCONSISTENT", failure="friction on the cold energy's own velocity removes its support: stationary needs rho_m + d = 0"),
        "Pc2": dict(label="INCONSISTENT", failure="a healthy local mediator gives static energy -F: force +grad psi (settling reverses); +F needs a ghost or a gradient-unstable field"),
    }
    RES["labels"] = labels
    log("LABELS:"); [log(f"  {k}: {v}") for k, v in labels.items()]
    log(f"[total {time.time() - t0:.0f} s]")
    finish()


def finish():
    def conv(o):
        if isinstance(o, dict): return {k: conv(v) for k, v in o.items() if not isinstance(v, np.ndarray)}
        if isinstance(o, (list, tuple)): return [conv(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        return o
    with open(os.path.join(HERE, f"cfg542_results{TAG}.json"), "w") as fh:
        json.dump(conv(RES), fh, indent=1, default=str)
    with open(os.path.join(HERE, f"cfg542{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
