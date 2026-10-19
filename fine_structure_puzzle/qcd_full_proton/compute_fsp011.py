#!/usr/bin/env python3
"""FSP-011 author calculation: what of the proton first-order electromagnetic
mass derivative M_u = dM_p/d(e^2) can be assembled from published numbers.

Small, single-core script (a few seconds).  No numerical alpha is fitted.
alpha_ref is used only to (i) undo the alpha a cited source multiplied onto its
own alpha-free integral and (ii) print comparison numbers in that source's MeV.

Sections
  A. Born (elastic) Cottingham kernel, FSP-008 eq. (3), and the point-Dirac
     sharp-cutoff constant 3/2 (kernel normalisation check).
  B. Full-Q^2 Born integrals for proton and neutron from two published
     form-factor parametrisations; isoscalar and isovector projections.
  C. Published isovector (p-n) totals converted to coefficients of e^2, with
     the share that rests on alpha-normalised experimental inputs.
  D. Author closed-form charge weights of every two-current contraction class
     (proton, neutron, p-n, isoscalar) at physical charges, flavours u,d,s,c.
  E. Assembly ledger: known pieces of M_u^p and the single missing piece.
"""
import argparse
import hashlib
import json
import math
import platform
import sys
from fractions import Fraction as Fr

from scipy import __version__ as scipy_version
from scipy.integrate import quad

PI = math.pi


# ---------------------------------------------------------------- form factors
def ratfun(a, b, tau):
    num = sum(ak * tau ** k for k, ak in enumerate(a))
    den = 1.0 + sum(bk * tau ** (k + 1) for k, bk in enumerate(b))
    return num / den


def sachs(param, nucleon, Q2, M, inp):
    """Return (G_E, G_M) at Q2 (GeV^2) for nucleon 'p' or 'n'."""
    kin = inp["nucleon_kinematics"]
    tau = Q2 / (4.0 * M * M)
    if param == "BBBA05":
        c = inp["form_factor_parametrisations"]["BBBA05"]
        if nucleon == "p":
            return (ratfun(c["GEp"]["a"], c["GEp"]["b"], tau),
                    kin["mu_p"] * ratfun(c["GMp_over_mu_p"]["a"], c["GMp_over_mu_p"]["b"], tau))
        return (ratfun(c["GEn"]["a"], c["GEn"]["b"], tau),
                kin["mu_n"] * ratfun(c["GMn_over_mu_n"]["a"], c["GMn_over_mu_n"]["b"], tau))
    if param == "dipole_Galster":
        c = inp["form_factor_parametrisations"]["dipole_Galster"]
        GD = (1.0 + Q2 / c["Lambda2_GeV2"]) ** -2
        if nucleon == "p":
            return GD, kin["mu_p"] * GD
        return -kin["mu_n"] * tau * GD / (1.0 + c["Galster_B"] * tau), kin["mu_n"] * GD
    raise ValueError(param)


def dirac_pauli(GE, GM, tau):
    F1 = (GE + tau * GM) / (1.0 + tau)
    F2 = (GM - GE) / (1.0 + tau)
    A = (GE * GE + tau * GM * GM) / (1.0 + tau)
    return F1, F2, A


# ---------------------------------------------------------------- Born kernel
def born_B(z, F1, A, GM):
    """FSP-008 proton_kernel DERIVATION eq. (3); sqrt(1+z^2)-z written stably."""
    s = 1.0 / (math.sqrt(1.0 + z * z) + z)
    return z * (3.0 * F1 * F1 - A) / 2.0 + ((1.0 + z * z) * A - 3.0 * z * z * GM * GM) * s


def B_of_z(param, nucleon, M, inp, z):
    Q2 = 4.0 * M * M * z * z
    GE, GM = sachs(param, nucleon, Q2, M, inp)
    F1, F2, A = dirac_pauli(GE, GM, z * z)
    return born_B(z, F1, A, GM)


def nonpole_integrand(param, nucleon, M, inp, z):
    """Contribution of the polynomial -2F1^2 in T_1^B to M_u/M:
    (1/(4 pi^3)) z * 6 F1^2 * int dx sqrt(1-x^2) = (3/(4 pi^2)) z F1^2."""
    Q2 = 4.0 * M * M * z * z
    GE, GM = sachs(param, nucleon, Q2, M, inp)
    F1, _, _ = dirac_pauli(GE, GM, z * z)
    return 3.0 / (4.0 * PI * PI) * z * F1 * F1


BREAKS = [0.0, 0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 20.0]


def integrate_z(f):
    total, err = 0.0, 0.0
    for lo, hi in zip(BREAKS[:-1], BREAKS[1:]):
        v, e = quad(f, lo, hi, limit=400, epsabs=1e-14, epsrel=1e-12)
        total += v
        err += e
    v, e = quad(f, BREAKS[-1], math.inf, limit=400, epsabs=1e-14, epsrel=1e-12)
    return total + v, err + e


# ---------------------------------------------------------------- Dirac check
def dirac_constant(Lambda_over_m):
    """16 pi^2 M_u/m - 3 log(Lambda^2/m^2) for a unit point Dirac particle with
    a sharp O(4) photon cutoff, via the exact primitive of B_D (closed form)
    and via quadrature of the stable form of B_D."""
    import mpmath as mp
    mp.mp.dps = 50
    Z = mp.mpf(Lambda_over_m) / 2
    prim = (mp.mpf(3) / 4 * mp.asinh(Z) + mp.mpf(3) / 4 * Z * mp.sqrt(1 + Z * Z)
            - Z * (1 + Z * Z) ** mp.mpf(1.5) / 2 + Z ** 4 / 2)
    c_closed = 8 * prim - 3 * mp.log(mp.mpf(Lambda_over_m) ** 2)
    BD = lambda z: (math.sqrt(1 + z * z) + 2 * z) / (math.sqrt(1 + z * z) + z) ** 2
    pts = [0.0, 0.5, 2.0, 10.0, 100.0, 1000.0, 1e4, 1e5]
    zmax = float(Z)
    num = 0.0
    for lo, hi in zip(pts[:-1], pts[1:]):
        if lo >= zmax:
            break
        v, _ = quad(BD, lo, min(hi, zmax), limit=400, epsabs=1e-13, epsrel=1e-13)
        num += v
    c_quad = 8 * num - 3 * math.log(Lambda_over_m ** 2)
    return float(c_closed), c_quad


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    raw = open(args.inputs, "rb").read()
    inp = json.loads(raw)
    kin = inp["nucleon_kinematics"]
    Mp, Mn = kin["M_p_MeV"] / 1000.0, kin["M_n_MeV"] / 1000.0
    a_ref = 1.0 / inp["alpha_ref"]["value_inverse"]
    four_pi_aref = 4.0 * PI * a_ref
    checks = []

    # A. Dirac normalisation check
    dirac = {}
    for L in (1e2, 1e3, 1e4):
        cc, cq = dirac_constant(L)
        dirac[f"Lambda_over_m={L:g}"] = {"closed_form": cc, "quadrature": cq}
    dirac["asymptotic_expected"] = 1.5
    ok = abs(dirac["Lambda_over_m=10000"]["closed_form"] - 1.5) < 1e-6 and \
        abs(dirac["Lambda_over_m=10000"]["quadrature"] - 1.5) < 1e-6
    checks.append({"name": "point-Dirac sharp-cutoff constant -> 3/2 (closed form and quadrature)", "pass": ok})

    # B. Born integrals
    born = {}
    for param in ("BBBA05", "dipole_Galster"):
        res = {}
        for nuc, M in (("p", Mp), ("n", Mn)):
            val, err = integrate_z(lambda z: B_of_z(param, nuc, M, inp, z))
            MuB_over_M = val / (2.0 * PI * PI)
            npv, _ = integrate_z(lambda z: nonpole_integrand(param, nuc, M, inp, z))
            res[nuc] = {
                "MuB_over_M_per_e2": MuB_over_M,
                "quad_abs_error_estimate": err / (2.0 * PI * PI),
                "MuB_MeV_per_e2": MuB_over_M * M * 1000.0,
                "nonpole_minus2F1sq_share_MeV_per_e2": npv * M * 1000.0,
                "MuB_MeV_at_alpha_ref_comparison_only": four_pi_aref * MuB_over_M * M * 1000.0,
            }
        p, n = res["p"]["MuB_MeV_per_e2"], res["n"]["MuB_MeV_per_e2"]
        res["isoscalar_(p+n)/2_MeV_per_e2"] = 0.5 * (p + n)
        res["isovector_p-n_MeV_per_e2"] = p - n
        res["isovector_p-n_MeV_at_alpha_ref_comparison_only"] = four_pi_aref * (p - n)
        res["isovector_p-n_poleonly_MeV_at_alpha_ref_comparison_only"] = four_pi_aref * (
            (p - res["p"]["nonpole_minus2F1sq_share_MeV_per_e2"])
            - (n - res["n"]["nonpole_minus2F1sq_share_MeV_per_e2"]))
        res["proton_poleonly_MeV_per_e2"] = p - res["p"]["nonpole_minus2F1sq_share_MeV_per_e2"]
        born[param] = res
    # independent 2D angular route for a few z (pointwise check of B)
    def two_d_B(param, nuc, M, z):
        Q2 = 4.0 * M * M * z * z
        GE, GM = sachs(param, nuc, Q2, M, inp)
        F1, F2, A = dirac_pauli(GE, GM, z * z)
        def integrand(th):
            x = math.sin(th)
            T1 = 2.0 * (z * z * GM * GM / (z * z + x * x) - F1 * F1)
            T2 = 2.0 * A / (z * z + x * x)
            return math.cos(th) ** 2 * (-3.0 * T1 + (1.0 - x * x) * T2)
        v, _ = quad(integrand, 0.0, PI / 2, points=[min(z, 0.5)], limit=400, epsabs=1e-13, epsrel=1e-12)
        return z / (2.0 * PI) * 2.0 * v
    pointwise = []
    for z in (0.03, 0.2, 0.7, 1.5, 4.0):
        for nuc, M in (("p", Mp), ("n", Mn)):
            b1 = B_of_z("BBBA05", nuc, M, inp, z)
            b2 = two_d_B("BBBA05", nuc, M, z)
            pointwise.append({"z": z, "nucleon": nuc, "B_kernel_eq3": b1, "B_from_T1_T2_angular": b2,
                              "abs_diff": abs(b1 - b2)})
    ok = all(r["abs_diff"] < 1e-9 * max(1.0, abs(r["B_kernel_eq3"])) for r in pointwise)
    checks.append({"name": "FSP-008 Born kernel eq.(3) equals direct angular integral of T1^B,T2^B (10 points)", "pass": ok})
    # neutron soft limit and proton soft limit
    checks.append({"name": "proton B(z->0)=1, neutron B(z->0)=0",
                   "pass": abs(B_of_z("BBBA05", "p", Mp, inp, 1e-7) - 1.0) < 1e-5
                   and abs(B_of_z("BBBA05", "n", Mn, inp, 1e-7)) < 1e-5})

    # C. Published isovector totals
    cdg = inp["published_isovector"]["CaoDaiGuo_2609.15154v1"]
    glr = inp["published_isovector"]["GasserLeutwylerRusetsky_2003.13612v3"]
    def per_e2(x):
        return x / four_pi_aref
    nb_cdg = cdg["m_F12_MeV"] + cdg["m_Sbar_MeV"]
    isovector = {
        "CDG_delta_m_QED_per_e2_MeV": per_e2(cdg["delta_m_QED_MeV"]),
        "CDG_elastic_per_e2_MeV": per_e2(cdg["m_el_MeV"]),
        "CDG_nonelastic_(F12+Sbar)_MeV": nb_cdg,
        "CDG_nonelastic_per_e2_MeV": per_e2(nb_cdg),
        "CDG_nonelastic_alt_M0_per_e2_MeV": per_e2(cdg["m_F12_MeV"] + cdg["m_Sbar_alternative_M0_0p7GeV_MeV"]),
        "CDG_share_resting_on_alpha_normalised_inputs": abs(nb_cdg) / cdg["delta_m_QED_MeV"],
        "GLR_delta_m_QED_per_e2_MeV": per_e2(glr["delta_m_QED_MeV"]),
        "GLR_err_per_e2_MeV": per_e2(glr["err_MeV"]),
        "note": "per_e2 = source MeV / (4 pi alpha_ref): exact inverse of the source's alpha prefactor. The elastic part rests on charge-normalised form factors (alpha-free at leading order); F12 and Sbar rest on cross sections normalised by alpha^2, so their per-e2 values inherit 1/alpha_meas^2 scaling through the data."
    }
    # compare our full-Born p-n with CDG elastic
    for param in ("BBBA05", "dipole_Galster"):
        isovector[f"ours_fullBorn_p-n_{param}_MeV_at_alpha_ref"] = born[param]["isovector_p-n_MeV_at_alpha_ref_comparison_only"]
        isovector[f"ours_poleonly_p-n_{param}_MeV_at_alpha_ref"] = born[param]["isovector_p-n_poleonly_MeV_at_alpha_ref_comparison_only"]
    full_b = born["BBBA05"]["isovector_p-n_MeV_at_alpha_ref_comparison_only"]
    checks.append({"name": "our BBBA05 full-Born p-n agrees with CDG m_el=0.75(2) MeV within 3x its quoted error",
                   "pass": abs(full_b - cdg["m_el_MeV"]) < 3 * cdg["m_el_err_MeV"],
                   "value": full_b})

    # D. Author closed-form charge weights (exact fractions)
    Q = {"u": Fr(2, 3), "d": Fr(-1, 3), "s": Fr(-1, 3), "c": Fr(2, 3)}
    sea = ["l", "s", "c"]          # isospin-symmetric light loop l = u or d
    Qsum = {"l": Q["u"] + Q["d"], "s": Q["s"], "c": Q["c"]}
    Q2sum = {"l": Q["u"] ** 2 + Q["d"] ** 2, "s": Q["s"] ** 2, "c": Q["c"] ** 2}
    def weights(maj, mino):
        w = {"X_maj": Q[maj] ** 2, "X_min": Q[mino] ** 2,
             "Y_majmaj": Q[maj] ** 2, "Y_majmin": Q[maj] * Q[mino]}
        for g in sea:
            w[f"Z_maj_{g}"] = Q[maj] * Qsum[g]
            w[f"Z_min_{g}"] = Q[mino] * Qsum[g]
            w[f"W_{g}"] = Q2sum[g]
        for i, g in enumerate(sea):
            for h in sea[i:]:
                w[f"V_{g}{h}"] = Qsum[g] * Qsum[h] * (1 if g == h else 2)
        return w
    wp, wn = weights("u", "d"), weights("d", "u")
    table = {}
    for k in wp:
        table[k] = {"p": str(wp[k]), "n": str(wn[k]), "p-n": str(wp[k] - wn[k]),
                    "(p+n)/2": str((wp[k] + wn[k]) / 2)}
    zero_in_pn = [k for k in wp if wp[k] - wn[k] == 0]
    checks.append({"name": "all same-loop (W) and two-loop (V) sea classes cancel in p-n",
                   "pass": all(k in zero_in_pn for k in wp if k.startswith(("W_", "V_")))})
    checks.append({"name": "the connected majority-minority exchange Y_majmin cancels in p-n but not in (p+n)/2",
                   "pass": wp["Y_majmin"] == wn["Y_majmin"] and wp["Y_majmin"] != 0})

    # E. Assembly ledger for the proton.
    # Exact isospin split: M_u^p = M_u^(0) + (1/2) M_u^(p-n),
    # M_u^(0) = Born^(0) + NB^(0)(mu).  The published p-n TOTAL is convention
    # free, so no Born/non-Born convention needs to be matched to the source.
    pim = inp["programme_imports"]
    sp_, ss_, sc_ = Fr(pim["sigma_piN_MeV"]), Fr(pim["sigma_s_MeV"]), Fr(pim["sigma_c_MeV"])
    gS_, ml_ = Fr(pim["gS_u_minus_d"]), Fr(pim["ml_MSbar2GeV_MeV"])
    su_, sd_ = (sp_ + ml_ * gS_) / 2, (sp_ - ml_ * gS_) / 2
    qq = [Fr(2, 3) ** 2, Fr(1, 3) ** 2, Fr(1, 3) ** 2, Fr(2, 3) ** 2]
    sig_p = qq[0] * su_ + qq[1] * sd_ + qq[2] * ss_ + qq[3] * sc_
    sig_n = qq[0] * sd_ + qq[1] * su_ + qq[2] * ss_ + qq[3] * sc_
    sig_iso = (sig_p + sig_n) / 2
    pref = 2.5 / (16 * PI * PI)
    checks.append({"name": "imported proton sigma-weighted sum reproduces FSP-010 488167/9375 MeV exactly",
                   "pass": sig_p == Fr(pim["sigma_weighted_exact"])})
    ledger = {"identity": "M_u^p = Born^(0) + (1/2) M_u^(p-n) + NB^(0)(mu)"}
    for param in ("BBBA05", "dipole_Galster"):
        b0 = born[param]["isoscalar_(p+n)/2_MeV_per_e2"]
        ledger[f"Born^(0)_{param}_MeV_per_e2"] = b0
        ledger[f"known_partial_CDG_{param}_MeV_per_e2"] = b0 + 0.5 * isovector["CDG_delta_m_QED_per_e2_MeV"]
        ledger[f"known_partial_GLR_{param}_MeV_per_e2"] = b0 + 0.5 * isovector["GLR_delta_m_QED_per_e2_MeV"]
    ledger["half_isovector_total_CDG_MeV_per_e2"] = 0.5 * isovector["CDG_delta_m_QED_per_e2_MeV"]
    ledger["half_isovector_total_CDG_err_plus_minus_MeV_per_e2"] = [0.5 * cdg["err_plus_MeV"] / four_pi_aref,
                                                                   0.5 * cdg["err_minus_MeV"] / four_pi_aref]
    ledger["half_isovector_total_GLR_MeV_per_e2"] = 0.5 * isovector["GLR_delta_m_QED_per_e2_MeV"]
    ledger["half_isovector_total_GLR_err_MeV_per_e2"] = 0.5 * isovector["GLR_err_per_e2_MeV"]
    ledger["convention_crosscheck_Bornp_plus_half_CDG_own_nonelastic_MeV_per_e2"] = (
        born["BBBA05"]["p"]["MuB_MeV_per_e2"] + 0.5 * isovector["CDG_nonelastic_per_e2_MeV"])
    ledger["missing"] = ("NB^(0)(mu): isoscalar non-Born first-order response on the fixed renormalised path, "
                         "including the isoscalar UV matching (quark sigma-term and gluon thresholds) and every "
                         "contraction class of the u,d,s current; NOT estimated here")
    ledger["UV_anchor"] = {
        "sigma_weighted_proton_MeV": float(sig_p), "sigma_weighted_isoscalar_MeV": float(sig_iso),
        "isovector_part_(p-n)/2_MeV": float((sig_p - sig_n) / 2),
        "charm_share_of_isoscalar_sum": float(qq[3] * sc_ / sig_iso),
        "finite_quark_ct_mu_eq_Lambda_proton_MeV_per_e2": float(sig_p) * pref,
        "finite_quark_ct_mu_eq_Lambda_isoscalar_MeV_per_e2": float(sig_iso) * pref,
        "status": "FSP-010 leading strong-order local quark conversion; the isoscalar value belongs INSIDE NB^(0) and must not be added to the known partial sum as if NB^(0) were known; its isovector part is already inside the published p-n total"}
    ledger["warning"] = "the known partial sums are NOT M_u^p and must not be used as such"

    out = {
        "script": "compute_fsp011.py",
        "inputs_sha256": hashlib.sha256(raw).hexdigest(),
        "python": platform.python_version(), "scipy": scipy_version,
        "A_dirac_normalisation": dirac,
        "B_born": born,
        "B_born_pointwise_angular_check": pointwise,
        "C_isovector_published": isovector,
        "D_charge_weights_author": table,
        "E_assembly_ledger": ledger,
        "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks),
    }
    with open(args.output, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"all_checks_pass": out["all_checks_pass"],
                      "checks": [(c["name"], c["pass"]) for c in checks]}, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
