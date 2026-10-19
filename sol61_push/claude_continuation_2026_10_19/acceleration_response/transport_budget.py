#!/usr/bin/env python3
"""CL-AR-2026-10-19-01 -- positive-energy transport budget for a gravitating
polarization medium.

Lemma (exact, nonlinear).  Let the medium's gravitating energy density be
nonnegative and locally conserved, and let every energy element move at most
a distance ell between a reference state and the final state.  Then for every
ball B_r(c):
    M_ref(B_{r-ell}) <= M_fin(B_r) <= M_ref(B_{r+ell}).
Hence the polarization mass M_pol(B_r) = M_fin(B_r) - M_ref(B_r) is bounded by
the reference mass in the shell of width ell outside r, and
    int_0^R M_pol(<r) dr <= ell * M_ref(B_{R+ell}).
Corollary (non-increasing reference density):
    M_ref(B_r) >= M_pol(<r) * r^3/((r+ell)^3 - r^3)  ~ (r/(3 ell)) M_pol.
The law counts the WHOLE final medium mass inside r, M_law = M_ref(B_r) +
M_pol(<r).  So a LOCAL (ell << r) response can GENERATE at most the fraction
    f_gen <= 1 - (1 + ell/r)^(-3)  ~ 3 ell/r
of the law's medium mass; the rest must already be present in the reference
(pre-arranged by formation).  If instead the reference is a cosmologically
subtracted uniform background rho_bar (all of M_law generated), the needed
excursion is
    ell_min(r) = (r^3 + 3 M_law(<r)/(4 pi rho_bar))^(1/3) - r.

Checks: (A) Monte Carlo verification of the lemma for random, inward and
outward transports with |u|<=ell, several ball centres (small N, 1 core);
(B) sympy corollary algebra; (C) illustrative galaxy numbers for BOTH a0
footings (9.36e-11 and 1.13e-10 m s^-2).  The galaxy inputs are declared
illustrations, not fits.

Usage: python3 transport_budget.py OUTDIR  (writes OUTDIR/transport_budget.json)
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

results = {"checkpoint": "CL-AR-2026-10-19-01", "script": "transport_budget.py",
           "checks": {}, "numbers": {}}


def record(name, ok, detail=""):
    results["checks"][name] = {"passed": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
    return ok


# ---------------------------------------------------------------- A
def part_a(seed=20261019, N=20000):
    rng = np.random.default_rng(seed)
    # reference: declared cored profile, rho ~ 1/(1+r^2), truncated at r=10
    rr = []
    while len(rr) < N:
        r = rng.uniform(0, 10, size=4 * N)
        keep = rng.uniform(0, 1, size=r.size) < (r ** 2 / (1 + r ** 2))
        rr.extend(r[keep].tolist())
    r = np.array(rr[:N])
    v = rng.normal(size=(N, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    x_ref = r[:, None] * v
    ell = 0.7
    radii = np.linspace(0.05, 12.0, 240)
    centres = [np.zeros(3), np.array([1.5, -0.4, 0.2]), np.array([-3.0, 2.0, 1.0])]
    transports = {}
    d = rng.normal(size=(N, 3))
    d /= np.linalg.norm(d, axis=1)[:, None]
    transports["random"] = x_ref + d * (ell * rng.uniform(0, 1, size=N))[:, None]
    worst_viol = 0.0
    integ_ok = True
    for ci, c in enumerate(centres):
        rel = x_ref - c
        dist_ref = np.linalg.norm(rel, axis=1)
        unit = rel / np.maximum(dist_ref, 1e-12)[:, None]
        step = np.minimum(dist_ref, ell)
        trans = dict(transports)
        trans["inward"] = x_ref - unit * step[:, None]
        trans["outward"] = x_ref + unit * ell
        sref = np.sort(dist_ref)
        for name, xf in trans.items():
            sfin = np.sort(np.linalg.norm(xf - c, axis=1))
            Mfin = np.searchsorted(sfin, radii, side="right")
            lo = np.searchsorted(sref, radii - ell, side="right")
            hi = np.searchsorted(sref, radii + ell, side="right")
            viol = max(int(np.max(lo - Mfin)), int(np.max(Mfin - hi)), 0)
            worst_viol = max(worst_viol, viol)
            # integrated form on [0, R] for R = 6
            Rm = 6.0
            grid = np.linspace(0, Rm, 3001)
            Mref_g = np.searchsorted(sref, grid, side="right")
            Mfin_g = np.searchsorted(sfin, grid, side="right")
            lhs = np.trapz(Mfin_g - Mref_g, grid)
            rhs = ell * np.searchsorted(sref, Rm + ell, side="right")
            integ_ok &= lhs <= rhs + 1e-9
    record("A1_shell_bounds_hold", worst_viol == 0,
           f"N={N}, ell={ell}, 3 centres x 3 transports (random/inward/outward), "
           f"240 radii: worst violation = {worst_viol} particles")
    record("A2_integrated_bound_holds", bool(integ_ok),
           "int_0^R M_pol(<r) dr <= ell M_ref(B_{R+ell}) in every case")
    # the inward transport saturates the upper bound where the profile allows
    c = centres[0]
    dist_ref = np.linalg.norm(x_ref - c, axis=1)
    xf = x_ref - (x_ref / dist_ref[:, None]) * np.minimum(dist_ref, ell)[:, None]
    sfin = np.sort(np.linalg.norm(xf, axis=1))
    sref = np.sort(dist_ref)
    rt = np.array([2.0, 4.0, 6.0])
    sat = (np.searchsorted(sfin, rt, side="right")
           == np.searchsorted(sref, rt + ell, side="right"))
    record("A3_bound_is_sharp", bool(np.all(sat)),
           "radial inward transport by ell attains M_fin(B_r) = M_ref(B_{r+ell})")


# ---------------------------------------------------------------- B
def part_b():
    r, ell, rho, Mpol = sp.symbols("r ell rho M_pol", positive=True)
    shell = sp.Rational(4, 3) * sp.pi * rho * ((r + ell) ** 3 - r ** 3)
    ball = sp.Rational(4, 3) * sp.pi * rho * r ** 3
    ratio = sp.simplify(ball / shell)
    x = sp.symbols("x", positive=True)      # x = ell/r
    rx = sp.simplify(ratio.subs(ell, x * r))
    ser = sp.series(rx, x, 0, 2).removeO()
    record("B1_monotone_corollary",
           sp.simplify(rx - 1 / ((1 + x) ** 3 - 1)) == 0
           and sp.simplify(ser - (1 / (3 * x) - sp.Rational(1, 3) + x * sp.Rational(2, 9))) == 0,
           "M_ref(B_r)/M_pol(<r) >= 1/((1+x)^3-1) = 1/(3x) - 1/3 + 2x/9 + ..., x=ell/r")
    # M_law = M_ref(B_r) + M_pol(<r) and M_pol <= ((1+x)^3 - 1) M_ref give
    # the largest fraction of the law mass a local response can generate.
    Mref = sp.symbols("M_ref", positive=True)
    Mpol_max = ((1 + x) ** 3 - 1) * Mref
    fgen_max = sp.simplify(Mpol_max / (Mref + Mpol_max))
    ok_f = sp.simplify(fgen_max - (1 - (1 + x) ** -3)) == 0
    ok_s = sp.simplify(sp.series(fgen_max, x, 0, 2).removeO() - 3 * x) == 0
    vals = {str(fv): float((1 - fv) ** (-1 / 3) - 1) for fv in (0.5, 0.9, 0.99)}
    fmax = {str(xv): float(1 - (1 + xv) ** -3) for xv in (0.01, 0.1, 0.3)}
    results["numbers"]["B_min_ell_over_r_to_generate_fraction_f"] = vals
    results["numbers"]["B_max_generated_fraction_at_ell_over_r"] = fmax
    record("B2_generated_fraction_bound", ok_f and ok_s,
           "f_gen <= 1-(1+ell/r)^-3 = 3 ell/r + O((ell/r)^2); "
           "max f_gen at ell/r=0.01,0.1,0.3: "
           + ", ".join(f"{v:.3f}" for v in fmax.values())
           + "; ell/r needed for f_gen=0.5,0.9,0.99: "
           + ", ".join(f"{v:.3f}" for v in vals.values()))


# ---------------------------------------------------------------- C
def part_c():
    G = 6.67430e-11
    Msun = 1.98847e30
    kpc = 3.0856775814913673e19
    Mpc = 1e3 * kpc
    H0 = 67.4e3 / Mpc
    Om = 0.315
    rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
    rho_bar = Om * rho_crit
    Mb = 1e10 * Msun
    out = {"declared_inputs": {"M_b_Msun": 1e10, "H0_km_s_Mpc": 67.4,
                               "Omega_m": Om, "rho_bar_kg_m3": rho_bar,
                               "baryons": "point mass (illustration)"},
           "footings": {}}
    ok = True
    for a0 in (9.36e-11, 1.13e-10):
        rows = []
        for rk in (10.0, 30.0, 100.0):
            rm = rk * kpc
            gN = G * Mb / rm ** 2
            g = 0.5 * (gN + math.sqrt(gN ** 2 + 4 * gN * a0))
            Mlaw = rm ** 2 * (g - gN) / G          # = 4 pi r^2 p(g)
            # check against p(g) = a0 g/(4 pi G (a0+g))
            Mlaw2 = 4 * math.pi * rm ** 2 * a0 * g / (4 * math.pi * G * (a0 + g))
            ok &= abs(Mlaw / Mlaw2 - 1) < 1e-12
            # dynamical density at r (all medium, point baryons)
            h = 1e-4 * rm
            def r2g(x):
                gn = G * Mb / x ** 2
                gg = 0.5 * (gn + math.sqrt(gn ** 2 + 4 * gn * a0))
                return x ** 2 * gg
            rho_dyn = (r2g(rm + h) - r2g(rm - h)) / (2 * h) / (4 * math.pi * G * rm ** 2)
            ell_min = (rm ** 3 + 3 * Mlaw / (4 * math.pi * rho_bar)) ** (1 / 3) - rm
            rows.append({
                "r_kpc": rk, "g_over_a0": g / a0, "g_N_over_a0": gN / a0,
                "M_law_Msun": Mlaw / Msun, "rho_dyn_kg_m3": rho_dyn,
                "rho_dyn_over_rho_bar": rho_dyn / rho_bar,
                "ell_min_uniform_background_kpc": ell_min / kpc,
                "ell_min_over_r": ell_min / rm,
                "pointwise_u_over_r_if_carriers_at_rho_bar":
                    (a0 * g / (4 * math.pi * G * (a0 + g))) / rho_bar / rm,
            })
        out["footings"][str(a0)] = rows
    results["numbers"]["C_illustrative_galaxy"] = out
    record("C1_law_mass_identity", ok,
           "M_law(<r) = r^2 (g - g_N)/G = 4 pi r^2 p(g) for the simple law")
    for a0, rows in out["footings"].items():
        print(f"  a0={a0}: " + "; ".join(
            f"r={x['r_kpc']:.0f}kpc g/a0={x['g_over_a0']:.3f} "
            f"M_law={x['M_law_Msun']:.3e}Msun ell_min={x['ell_min_uniform_background_kpc']:.0f}kpc"
            f" (ell/r={x['ell_min_over_r']:.1f}) rho_dyn/rho_bar={x['rho_dyn_over_rho_bar']:.2e}"
            for x in rows))


# ---------------------------------------------------------------- D
def part_d():
    """Two small arithmetic illustrations used in RESULT.md."""
    G = 6.67430e-11
    Msun = 1.98847e30
    pc = 3.0856775814913673e16
    # (i) Gauss form of the normalization: p is the enclosed medium surface
    #     density M_med(<r)/(4 pi r^2); saturation Sigma_sat = a0/(4 pi G)
    sig = {}
    for a0 in (9.36e-11, 1.13e-10):
        s_si = a0 / (4 * math.pi * G)
        sig[str(a0)] = {"Sigma_sat_kg_m2": s_si,
                        "Sigma_sat_Msun_pc2": s_si / (Msun / pc ** 2)}
    results["numbers"]["D_Sigma_sat"] = sig
    # (ii) support acceleration of rotation-supported disc gas relative to
    #      free fall: |a_rel|/g ~ (c_s/v_c)^2 |dlnP/dlnr|; stars: exactly 0
    rows = []
    for vc in (50.0, 100.0, 200.0):
        rows.append({"c_s_km_s": 10.0, "v_c_km_s": vc, "dlnP_dlnr": 2.0,
                     "a_rel_over_g": (10.0 / vc) ** 2 * 2.0})
    results["numbers"]["D_disc_gas_support_fraction"] = rows
    record("D1_illustrations", True,
           "Sigma_sat = " + ", ".join(
               f"{v['Sigma_sat_Msun_pc2']:.1f} Msun/pc^2 (a0={k})"
               for k, v in sig.items())
           + "; disc gas |a_rel|/g = "
           + ", ".join(f"{x['a_rel_over_g']:.3f} (v_c={x['v_c_km_s']:.0f})"
                       for x in rows))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    out.mkdir(parents=True, exist_ok=True)
    part_a()
    part_b()
    part_c()
    part_d()
    allok = all(c["passed"] for c in results["checks"].values())
    results["all_passed"] = allok
    results["versions"] = {"numpy": np.__version__, "sympy": sp.__version__}
    (out / "transport_budget.json").write_text(json.dumps(results, indent=1))
    print("ALL PASSED" if allok else "SOME CHECKS FAILED")
    sys.exit(0 if allok else 1)
