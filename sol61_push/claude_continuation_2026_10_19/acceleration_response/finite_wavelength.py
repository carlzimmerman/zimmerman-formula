#!/usr/bin/env python3
"""CL-AR-2026-10-19-01 -- finite-wavelength static response and limit order.

A. Free composite (cloud m_c bound to host m_h, total COM removed exactly).
   Odd probe U=-E sin(kz)/k about the COM:
     D_k(z) = [m_c sin(k mu_h z) - m_h sin(k mu_c z)]/k,  mu_a = m_a/M,
   dipole term vanishes identically; leading term -(k^2/6) q3 z^3 with
   q3 = mu_red (m_h - m_c)/M; equal masses give D_k == 0 at every k.
   Harmonic ground state: chi_D = (11/18) k^4 q3^2 s^6/(hbar w) + O(k^6),
   checked against the exact all-k matrix-element sum (numerically, small).
   Medium of free composites (random COMs, COM response removed): the O(k)
   term of rho_k is exactly zero (EP); the first internal term is the
   quadrupole, so alpha_int(k) = -chi_int/k^2 = O(k^2) -> 0.
B. Supported compressible scalar medium of the original action (matched
   contact + quantum pressure): proper static chi_p = -1/h(k),
   h = 2K + tau k^2/(2 rho).  eps(k) = 1 - 4 pi G/(k^2 h) has exactly one
   positive root (Jeans), TF value k*^2 = 2 pi G/K = 8 pi G m^4/lambda_rep.
   Dressed static response chi_p/eps -> +k^2/(4 pi G) below k_J (perfect
   screening on the unstable branch).  Dynamic chi_p(k,w)=rho k^2/(w^2-w_B^2):
   lim_{k->0} chi/k^2 = rho/w^2 (free fall) but lim_{w->0} chi/k^2 -> -oo.
   Benchmark length 1/k* compared with the record's L0 = 3.68347e7 m.
C. Mode-family order of limits: chi = -2 W k^(2a)/Omega.  Internal modes have
   a >= 2 (EP).  Constant alpha needs Omega ~ k^(2a-2).
D. Supported insulating dielectric (cloud in a uniform-density host core held
   static): 4 pi G alpha = 3 rho_c/rho_h; hard-wall saturation at the core
   radius gives g* = G M_core/R_c^2; finite support compressibility C_site>0
   makes 4 pi G(-chi)/k^2 diverge as k->0 (fails the target).
E. The target's linear term in k-space: K|P_L|^2/2 = K|drho_k|^2/(2k^2)
   cancels the Newtonian self-energy for EVERY k (exact marginality,
   h_target(k) = 4 pi G/k^2).

Usage: python3 finite_wavelength.py OUTDIR  (writes OUTDIR/finite_wavelength.json)
"""
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

results = {"checkpoint": "CL-AR-2026-10-19-01", "script": "finite_wavelength.py",
           "checks": {}, "numbers": {}}


def record(name, ok, detail=""):
    results["checks"][name] = {"passed": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
    return ok


# ---------------------------------------------------------------- A
def part_a():
    mc, mh, k, z = sp.symbols("m_c m_h k z", positive=True)
    M = mc + mh
    muc, muh = mc / M, mh / M
    mured = mc * mh / M
    D = (mc * sp.sin(k * muh * z) - mh * sp.sin(k * muc * z)) / k
    ser = sp.series(D, k, 0, 5).removeO()
    c0 = sp.simplify(ser.coeff(k, 0))
    c2 = sp.simplify(ser.coeff(k, 2))
    q3 = mured * (mh - mc) / M
    record("A1_odd_probe_dipole_vanishes", c0 == 0,
           "k^0 (uniform) coefficient of D_k is identically zero about the COM")
    record("A2_odd_probe_octupole", sp.simplify(c2 + q3 * z ** 3 / 6) == 0,
           "D_k = -(k^2/6) q3 z^3 + O(k^4), q3 = mu_red (m_h - m_c)/M")
    record("A3_equal_masses_zero_all_k",
           sp.simplify(D.subs(mh, mc)) == 0,
           "m_c = m_h: D_k == 0 identically (all k)")
    # harmonic ground state, leading order via ladder operators
    s, hw = sp.symbols("s hbar_omega", positive=True)
    # <1|z^3|0> = 3 s^3, <3|z^3|0> = sqrt(6) s^3
    chi_lead = 2 * (k ** 2 * q3 / 6) ** 2 * ((3 * s ** 3) ** 2 / hw
                                           + (sp.sqrt(6) * s ** 3) ** 2 / (3 * hw))
    target = sp.Rational(11, 18) * k ** 4 * q3 ** 2 * s ** 6 / hw
    record("A4_ground_state_chi_D_leading", sp.simplify(chi_lead - target) == 0,
           "chi_D = (11/18) k^4 q3^2 s^6/(hbar w) + O(k^6)")

    # exact all-k sum: <n|e^{i kap z}|0> = e^{-kap^2 s^2/2} (i kap s)^n/sqrt(n!)
    def chi_exact(kv, mcv=1.0, mhv=3.0, sv=1.0, hwv=1.0, nmax=80):
        Mv = mcv + mhv
        kh, kc = kv * mhv / Mv, kv * mcv / Mv
        tot = mp.mpf(0)
        for n in range(1, nmax, 2):
            # Im part of (i kap s)^n for odd n: sign (-1)^((n-1)/2) (kap s)^n
            sg = (-1) ** ((n - 1) // 2)
            amp = (mcv * mp.e ** (-(kh * sv) ** 2 / 2) * (kh * sv) ** n
                   - mhv * mp.e ** (-(kc * sv) ** 2 / 2) * (kc * sv) ** n) * sg
            amp = amp / (kv * mp.sqrt(mp.factorial(n)))
            tot += 2 * amp ** 2 / (n * hwv)
        return tot

    mcv, mhv = 1.0, 3.0
    Mv = mcv + mhv
    q3v = (mcv * mhv / Mv) * (mhv - mcv) / Mv
    rows = []
    for kv in (0.01, 0.1, 0.3, 1.0):
        ex = chi_exact(kv)
        lead = 11.0 / 18.0 * kv ** 4 * q3v ** 2
        rows.append({"k_s": kv, "chi_exact": float(ex),
                     "chi_leading": lead, "ratio": float(ex / lead)})
    results["numbers"]["A_two_body_chi_D"] = rows
    record("A5_exact_sum_matches_k4_law",
           abs(rows[0]["ratio"] - 1) < 1e-3 and abs(rows[1]["ratio"] - 1) < 2e-2,
           "ratios exact/leading at k s=0.01,0.1,0.3,1: "
           + ", ".join(f"{r['ratio']:.6f}" for r in rows))
    # equal masses: exact sum is zero
    record("A6_equal_mass_exact_sum_zero",
           chi_exact(0.7, 2.0, 2.0) < mp.mpf("1e-40"),
           "m_c=m_h: every odd matrix element cancels")

    # medium of free composites at generic COM position R (1D):
    R = sp.symbols("R", real=True)
    rho_k = mc * sp.exp(sp.I * k * (R + muh * z)) + mh * sp.exp(sp.I * k * (R - muc * z))
    serk = sp.series(sp.exp(-sp.I * k * R) * rho_k, k, 0, 3).removeO()
    record("A7_medium_rho_k_no_internal_dipole",
           sp.simplify(serk.coeff(k, 1)) == 0
           and sp.simplify(serk.coeff(k, 2) + mured * z ** 2 / 2) == 0,
           "rho_k = e^{ikR}[M + 0*k - (k^2/2) mu_red z^2 + ...]: "
           "first internal coupling is the quadrupole")
    # classical thermal harmonic composite medium: chi_int = -n k^4 T/(2 w^4)
    n, T, w = sp.symbols("n T omega", positive=True)
    sig2 = T / (mured * w ** 2)
    var_z2 = 2 * sig2 ** 2                      # Gaussian Var(z^2)
    chi_int = -n * (k ** 4 / 4) * (mured ** 2 * var_z2) / T
    record("A8_medium_alpha_int_order_k2",
           sp.simplify(chi_int + n * k ** 4 * T / (2 * w ** 4)) == 0,
           "chi_int = -n k^4 T/(2 w^4) -> alpha_int = n k^2 T/(2 w^4) -> 0")


# ---------------------------------------------------------------- B
def part_b():
    k, K, tau, rho, G, w = sp.symbols("k K tau rho G omega", positive=True)
    h = 2 * K + tau * k ** 2 / (2 * rho)
    chi_p = -1 / h
    eps = 1 - 4 * sp.pi * G / (k ** 2 * h)
    z = sp.symbols("z", positive=True)
    roots = sp.solve(sp.Eq((z * h.subs(k, sp.sqrt(z))) - 4 * sp.pi * G, 0), z)
    pos = [r for r in roots if sp.simplify(r).is_positive is not False]
    tf = sp.limit(pos[0], tau, 0) if pos else None
    record("B1_single_Jeans_root",
           len(pos) == 1 and sp.simplify(tf - 2 * sp.pi * G / K) == 0,
           f"one positive root k_J^2; TF limit k*^2 = 2 pi G/K; root = {pos[0] if pos else None}")
    mono = sp.simplify(sp.diff(h.subs(k, sp.sqrt(z)) - 4 * sp.pi * G / z, z))
    record("B2_kernel_minus_gravity_increasing",
           sp.simplify(mono - (tau / (2 * rho) + 4 * sp.pi * G / z ** 2)) == 0,
           "d/dk^2 [h - 4piG/k^2] = tau/(2 rho) + 4 pi G/k^4 > 0")
    dressed = sp.simplify(chi_p / eps)
    lead = sp.series(dressed, k, 0, 4).removeO()
    record("B3_dressed_perfect_screening_below_kJ",
           sp.simplify(lead - k ** 2 / (4 * sp.pi * G)) == 0,
           "chi_p/eps = +k^2/(4 pi G) + O(k^4) (unstable branch): "
           "drho = -rho_ext, total density perturbation -> 0")
    wB2 = k ** 2 * (2 * K * rho + tau * k ** 2 / 2)
    chi_dyn = rho * k ** 2 / (w ** 2 - wB2)
    l1 = sp.limit(chi_dyn / k ** 2, k, 0)
    st = sp.simplify(chi_dyn.subs(w, 0) - chi_p)
    l2 = sp.limit(chi_dyn.subs(w, 0) / k ** 2, k, 0)
    record("B4_limit_order_proper",
           sp.simplify(l1 - rho / w ** 2) == 0 and st == 0 and l2 == -sp.oo,
           f"lim_k->0 chi/k^2 = {l1} (free fall); static chi(k,0)=chi_p; "
           f"lim_k->0 chi(k,0)/k^2 = {l2}")
    chi_full_dyn = sp.simplify(chi_dyn / (1 + 4 * sp.pi * G * chi_dyn / k ** 2))
    l3 = sp.limit(chi_full_dyn / k ** 2, k, 0)
    l4 = sp.limit(l3, w, 0)
    record("B5_limit_order_dressed",
           sp.simplify(l3 - rho / (w ** 2 + 4 * sp.pi * G * rho)) == 0
           and sp.simplify(l4 - 1 / (4 * sp.pi * G)) == 0,
           f"dressed: lim_k->0 chi/k^2 = {l3}; then w->0: {l4} "
           "(homogeneous background collapse/swindle branch, not a static "
           "stable state)")
    # benchmark numbers (SI), K = lambda_rep hbar^3/(4 m^4 c)
    hbar = 1.054571817e-34
    c = 299792458.0
    Gs = 6.67430e-11
    MeV = 1.602176634e-13
    mkg = MeV / c ** 2
    lam = 0.00587528017
    Ksi = lam * hbar ** 3 / (4 * mkg ** 4 * c)
    kstar = math.sqrt(2 * math.pi * Gs / Ksi)
    L = 1 / kstar
    results["numbers"]["B_benchmark"] = {
        "m_kg": mkg, "lambda_rep": lam, "K_SI_m5_per_kg_s2": Ksi,
        "kstar_per_m": kstar, "one_over_kstar_m": L,
        "polytrope_radius_pi_over_kstar_m": math.pi * L,
        "record_L0_m": 3.68347e7,
        "kpc_over_one_over_kstar": 3.0856775814913673e19 / L,
        "eps_at_k_equal_1_over_kpc": 1 - (kstar * 3.0856775814913673e19) ** 2,
    }
    record("B6_benchmark_matches_record_L0",
           abs(L / 3.68347e7 - 1) < 1e-5,
           f"1/k* = {L:.6e} m (record L0 3.68347e7 m); "
           f"pi/k* = {math.pi*L:.4e} m; at k=1/kpc eps = "
           f"{results['numbers']['B_benchmark']['eps_at_k_equal_1_over_kpc']:.3e}")


# ---------------------------------------------------------------- C
def part_c():
    k, W, Om, a, b = sp.symbols("k W Omega a b", positive=True)
    chi = -2 * W * k ** (2 * a) / Om
    alpha = sp.simplify(-chi / k ** 2)
    # along a family Omega = Om0 k^b, alpha ~ k^(2a-2-b)
    Om0 = sp.symbols("Omega_0", positive=True)
    alpha_fam = sp.simplify(alpha.subs(Om, Om0 * k ** b))
    expo = sp.simplify(sp.log(alpha_fam / (2 * W / Om0)) / sp.log(k))
    record("C1_mode_family_exponent",
           sp.simplify(sp.expand_log(expo, force=True) - (2 * a - 2 - b)) == 0,
           "alpha ~ k^(2a-2-b); internal modes a>=2 (EP) need b=2a-2>=2: "
           "a gap closing like k^2 at the probe scale; a=1 at finite gap "
           "is the pinned COM (external anchor)")
    lim1 = sp.limit(sp.limit(alpha.subs(a, 2), Om, 0), k, 0)
    lim2 = sp.limit(sp.limit(alpha.subs(a, 2), k, 0), Om, 0)
    record("C2_critical_limits_noncommuting", lim1 == sp.oo and lim2 == 0,
           f"internal quadrupole family: lim_k lim_Omega = {lim1}, "
           f"lim_Omega lim_k = {lim2}")


# ---------------------------------------------------------------- D
def part_d():
    G, rho_h, mc, n, Rc, g, Csite, k = sp.symbols(
        "G rho_h m_c n R_c g C_site k", positive=True)
    w2 = sp.Rational(4, 3) * sp.pi * G * rho_h       # uniform-core restoring
    d = g / w2                                      # static sag, a_rel = -g
    alpha = sp.simplify(n * mc * d / g)
    record("D1_supported_dielectric_normalization",
           sp.simplify(4 * sp.pi * G * alpha - 3 * n * mc / rho_h) == 0,
           "4 pi G alpha = 3 rho_c/rho_h  (rho_c = n m_c, rho_h host core)")
    gstar = sp.simplify(w2 * Rc)
    Mcore = sp.Rational(4, 3) * sp.pi * rho_h * Rc ** 3
    psat = n * mc * Rc
    record("D2_hard_wall_saturation_scale",
           sp.simplify(gstar - G * Mcore / Rc ** 2) == 0
           and sp.simplify(psat / gstar - alpha) == 0,
           "g* = w^2 R_c = G M_core/R_c^2 (core surface gravity); "
           "p_sat/g* = alpha, so the target needs rho_c = rho_h/3 AND "
           "a0 = G M_core/R_c^2 -- state selections")
    chi = -(Csite + alpha * k ** 2)
    ratio = sp.simplify(4 * sp.pi * G * (-chi) / k ** 2)
    record("D3_compressible_support_fails",
           sp.limit(ratio, k, 0) == sp.oo,
           "with site compressibility C_site>0: 4 pi G(-chi)/k^2 -> oo "
           "(k->0); only C_site=0 (incompressible static support) passes")
    # pointwise positive-mass budget for a flat rotation curve
    r = sp.symbols("r", positive=True)
    rho_dyn = g / (4 * sp.pi * G * r)
    rho_c = sp.symbols("rho_c", positive=True)
    u = (g / (4 * sp.pi * G)) / rho_c               # deep regime |P|=g/(4piG)
    record("D4_displacement_over_radius",
           sp.simplify(u / r - rho_dyn / rho_c) == 0,
           "deep regime, flat curve: |u|/r = rho_dyn/rho_carrier; locality "
           "(|u|<<r) requires carrier density >> total dynamical density")


# ---------------------------------------------------------------- E
def part_e():
    k, G, drho = sp.symbols("k G delta_rho", positive=True)
    K = 4 * sp.pi * G
    PL = drho / k                     # |P_L| from drho_k = -i k P_L
    e_med = K * PL ** 2 / 2
    e_grav = -sp.Rational(1, 2) * 4 * sp.pi * G * drho ** 2 / k ** 2
    record("E1_target_is_exact_marginality",
           sp.simplify(e_med + e_grav) == 0,
           "target quadratic medium energy K|P|^2/2 cancels the Newtonian "
           "self-energy at every k: h_target(k) = 4 pi G/k^2")


# ---------------------------------------------------------------- F
def part_f():
    """Independent audit of the record's n=1 closed-object cubic response
    (shared_state finite_wavelength eq. 2-3), units G=R=1, K=2/pi."""
    r, E = sp.symbols("r E", positive=True)
    A, lam = sp.symbols("A lambda")
    K = 2 / sp.pi
    j1 = sp.sin(sp.pi * r) / (sp.pi * r) ** 2 - sp.cos(sp.pi * r) / (sp.pi * r)
    H = A * j1 - 10 * E * r / sp.pi ** 2
    # (lap_1 + pi^2) H = -10 E r  (l=1 radial Laplacian)
    lap1 = sp.diff(H, r, 2) + 2 * sp.diff(H, r) / r - 2 * H / r ** 2
    ode_ok = sp.simplify(lap1 + sp.pi ** 2 * H + 10 * E * r) == 0
    dUself = H + E * r ** 3 + lam * r          # interior self-potential
    sol = sp.solve([dUself.subs(r, 1), sp.diff(dUself, r).subs(r, 1)],
                   [A, lam], dict=True)[0]
    ok_A = sp.simplify(sol[A] - 2 * sp.pi * E / 3) == 0
    ok_l = sp.simplify(sol[lam] - (10 / sp.pi ** 2 - sp.Rational(5, 3)) * E) == 0
    Hs = H.subs(sol)
    drho = -Hs / (2 * K)
    com = sp.simplify(sp.integrate(drho * r ** 3, (r, 0, 1)))
    chi1 = sp.simplify(sp.Rational(4, 3) * sp.pi
                       * sp.integrate(drho * r ** 5, (r, 0, 1)) / E)
    target = 20 / (3 * sp.pi ** 2) - sp.Rational(40, 63)
    record("F1_record_n1_cubic_response_reproduced",
           ode_ok and ok_A and ok_l and com == 0
           and sp.simplify(chi1 - target) == 0,
           f"A=2piE/3, lambda/E=10/pi^2-5/3, COM integral {com}, "
           f"chi_1 = {sp.nsimplify(chi1)} = {float(chi1):.6f} R^7/G "
           "(record: 20/(3pi^2)-40/63); plane-probe l=1 part gives "
           "chi_k = (k^4/100) chi_1 + O(k^6) per centred object")
    results["numbers"]["F_chi1_R7_over_G"] = float(chi1)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    out.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = 50
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    part_f()
    allok = all(c["passed"] for c in results["checks"].values())
    results["all_passed"] = allok
    results["sympy_version"] = sp.__version__
    (out / "finite_wavelength.json").write_text(json.dumps(results, indent=1))
    print("ALL PASSED" if allok else "SOME CHECKS FAILED")
    sys.exit(0 if allok else 1)
