#!/usr/bin/env python3
"""D-YM2 swing: where the rigorous lattice gap ends, where the continuum
limit lives, and what the framework's own scales can reach.

Inputs (all quoted with source; nothing fitted):
  * rigorous windows from this campaign's committed results:
      ../ym1_hamiltonian/results.json  (Kogut-Susskind, explicit X_d)
      ../ym1_euclidean/results.json    (Wilson, Dobrushin; SZZ 2023 column)
  * SU(3) Wilson scale: Necco & Sommer, Nucl. Phys. B622 (2002) 328,
    hep-lat/0108008, eq. (2.6):
      ln(a/r0) = -1.6804 - 1.7331(b-6) + 0.7849(b-6)^2 - 0.4428(b-6)^3,
      valid 5.7 <= beta <= 6.92.
  * lightest glueball: Morningstar & Peardon, PRD 60 (1999) 034509,
    hep-lat/9901004: r0 m(0++) = 4.21(12); r0^-1 = 410 MeV (their scale).
  * framework scales: a0 = 1.2e-10 m/s^2, H0 = 67.4 km/s/Mpc.
Outputs: results.json and a printed table.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
HBAR_EVS = 6.582119569e-16      # eV s
C = 2.99792458e8                # m/s
MPC = 3.0856775814913673e22     # m
M_PL_GEV = 1.220890e19          # GeV
N = 3


def a_over_r0(beta):
    x = beta - 6.0
    return math.exp(-1.6804 - 1.7331 * x + 0.7849 * x ** 2 - 0.4428 * x ** 3)


def two_loop_a_lambda(beta, n=N):
    """a * Lambda_L at two loops (perturbative, illustrative only)."""
    g2 = 2 * n / beta
    b0 = 11 * n / (48 * math.pi ** 2)
    b1 = 34 * n ** 2 / (3 * (16 * math.pi ** 2) ** 2)
    return (b0 * g2) ** (-b1 / (2 * b0 ** 2)) * math.exp(-1 / (2 * b0 * g2))


def run():
    ham = json.loads((HERE.parent / "ym1_hamiltonian" / "results.json").read_text())
    euc = json.loads((HERE.parent / "ym1_euclidean" / "results.json").read_text())
    X3 = ham["headline"]["X_3"]
    e4 = [t for t in euc["thresholds"] if t["D"] == 4][0]

    rigorous = {
        "hamiltonian_X3_uniform_N_(g^2 >=)": X3["uniform_all_N_bN<=2N"],
        "hamiltonian_X3_SU3_bN=N_(g^2 >=)": X3["SU3_bN=N"],
        "euclidean_dobrushin_beta_W_max_D4": e4["beta_W_max_all_N"],
        "euclidean_dobrushin_as_g2_SU3": 2 * N / e4["beta_W_max_all_N"],
        "SZZ2023_beta_W_max_SU3_D4": e4["SZZ_2023_beta_W_max_SU3"],
        "SZZ2023_as_g2_SU3": 2 * N / e4["SZZ_2023_beta_W_max_SU3"],
    }

    scaling = []
    for beta in (5.7, 6.0, 6.2, 6.4, 6.57, 6.69, 6.81, 6.92):
        ar0 = a_over_r0(beta)
        mGa = 4.21 * ar0
        scaling.append({"beta_W": beta, "g2": 2 * N / beta, "a/r0": ar0,
                        "a_fm(r0=0.5fm)": 0.5 * ar0, "m_G*a": mGa,
                        "xi_G/a": 1 / mGa})

    # rigorous lattice-unit gap vs what the continuum needs
    shape = []
    for beta in (0.005, 0.01, 0.02, 0.04, 0.05):
        z = 18 * math.tanh(beta)
        shape.append({"beta_W": beta, "rigorous_m*a_lower_bound": -math.log(z)})
    ref = two_loop_a_lambda(6.92)
    continuum = [{"beta_W": b, "a(beta)/a(6.92)_two_loop": two_loop_a_lambda(b) / ref,
                  "m_G*a_extrapolated": 4.21 * a_over_r0(6.92) * two_loop_a_lambda(b) / ref}
                 for b in (6.92, 8.0, 10.0, 15.0, 30.0, 100.0)]

    # framework scales (own terms)
    a0, H0 = 1.2e-10, 67.4e3 / MPC
    mG_GeV = 4.21 * 0.410
    fw = {
        "hbar*a0/c_eV": HBAR_EVS * a0 / C,
        "hbar*H0_eV": HBAR_EVS * H0,
        "glueball_0++_GeV": mG_GeV,
        "glueball/(hbar a0/c)": mG_GeV * 1e9 / (HBAR_EVS * a0 / C),
        "glueball/(hbar H0)": mG_GeV * 1e9 / (HBAR_EVS * H0),
        "gravitational_coupling_(m_G/M_Pl)^2": (mG_GeV / M_PL_GEV) ** 2,
    }

    checks = []

    def check(name, predicate, **data):
        checks.append({"name": name, "passed": bool(predicate), **data})

    check("necco_sommer_beta6_r0/a_5.37", abs(1 / a_over_r0(6.0) - 5.368) < 0.01,
          r0_over_a=1 / a_over_r0(6.0))
    check("glueball_MP99_1.73GeV", abs(mG_GeV - 1.726) < 0.005, m=mG_GeV)
    check("scaling_window_starts_above_rigorous_windows",
          scaling[0]["beta_W"] / rigorous["SZZ2023_beta_W_max_SU3_D4"] > 30,
          ratio=scaling[0]["beta_W"] / rigorous["SZZ2023_beta_W_max_SU3_D4"])
    check("rigorous_bound_grows_toward_strong_coupling",
          all(shape[i]["rigorous_m*a_lower_bound"] > shape[i + 1]["rigorous_m*a_lower_bound"]
              for i in range(len(shape) - 1)))
    check("continuum_needs_m*a_to_0",
          all(continuum[i]["m_G*a_extrapolated"] > continuum[i + 1]["m_G*a_extrapolated"]
              for i in range(len(continuum) - 1)) and continuum[-1]["m_G*a_extrapolated"] < 1e-10)
    check("framework_scales_42_orders_below", fw["glueball/(hbar H0)"] > 1e41)
    return {"rigorous": rigorous, "scaling_window_SU3": scaling,
            "rigorous_bound_shape_D4": shape, "continuum_two_loop": continuum,
            "framework_scales": fw, "checks": checks,
            "all_passed": all(c["passed"] for c in checks)}


if __name__ == "__main__":
    rep = run()
    (HERE / "results.json").write_text(json.dumps(rep, indent=2) + "\n")
    print("RIGOROUS (fixed spacing):")
    for k, v in rep["rigorous"].items():
        print(f"  {k:42s} {v:.4g}")
    print("SU(3) SCALING WINDOW (Necco-Sommer + MP99):")
    for r in rep["scaling_window_SU3"]:
        print(f"  beta={r['beta_W']:.2f} g2={r['g2']:.3f} a={r['a_fm(r0=0.5fm)']:.4f} fm "
              f"m_G a={r['m_G*a']:.3f} xi/a={r['xi_G/a']:.2f}")
    print("CONTINUUM (two-loop extrapolation, illustrative):")
    for r in rep["continuum_two_loop"]:
        print(f"  beta={r['beta_W']:6.2f} m_G a={r['m_G*a_extrapolated']:.3e}")
    print("FRAMEWORK SCALES:")
    for k, v in rep["framework_scales"].items():
        print(f"  {k:40s} {v:.3e}")
    failed = [c["name"] for c in rep["checks"] if not c["passed"]]
    print("FAILED:", failed if failed else "none")
    print("ALL CHECKS PASSED" if rep["all_passed"] else "CHECKS FAILED")
