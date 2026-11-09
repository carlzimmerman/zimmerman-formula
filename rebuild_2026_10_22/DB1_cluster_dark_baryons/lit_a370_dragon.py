"""DB1 literature follow-up (2026-11-09): put a number on DB1's microlensing gate (d).

Source: Palencia et al. 2026, A&A, DOI 10.1051/0004-6361/202660640, arXiv:2604.22702v3.
Read in full (arXiv HTML), not from a summary. Quoted inputs:
  - 104 caustic-crossing events in the Dragon arc (z_s = 0.725) behind Abell 370 (z_l = 0.375).
  - With beta fixed at 2.5: mean microlens surface density Sigma_* = 104 +- 21 Msun/pc^2,
    "twice as large as derived from intracluster light" (Montes & Trujillo 2022); IMF-dependent,
    Salpeter roughly doubles the ICL mass. With beta free they fit beta = 2.18 (+0.20 / -0.30)
    and Sigma_* is not separately constrained.
  - Microlens mass window named in the paper: 1e-1 to 1e2 Msun.
  - Paper cosmology: flat, Om 0.3, h 0.7 (used here only to turn kappa into Sigma).
  - No PBH / compact-DM fraction is quoted. Parity asymmetry "remains present" but the
    authors say it may come from the critical-curve position in the lens model.

Not in the paper, so bracketed here (stated, not fitted):
  - kappa (total convergence) at the arc: 0.4 to 0.9 (near a tangential critical curve).
  - CBDM share of the projected mass at the arc: DB1 says CBDM is ~50 % of the core mass;
    a lenient 25 % is also run.
  - ICL stellar column: half of Sigma_* (Chabrier reading, the paper's "twice") or all of it
    (Salpeter reading).
Everything here is order-of-magnitude. kappa = 1/2 FITTED; not theory closed.
"""
import json
import numpy as np
from scipy.integrate import quad

C_KMS = 299792.458
G_PC = 4.30091e-3  # pc Msun^-1 (km/s)^2
ZL, ZS = 0.375, 0.725
SIG_STAR, SIG_STAR_ERR = 104.0, 21.0


def sigma_crit(h0=70.0, om=0.3):
    e = lambda z: np.sqrt(om * (1 + z) ** 3 + 1 - om)
    dc = lambda z: C_KMS / h0 * quad(lambda x: 1 / e(x), 0, z)[0] * 1e6
    dl, ds = dc(ZL) / (1 + ZL), dc(ZS) / (1 + ZS)
    dls = (dc(ZS) - dc(ZL)) / (1 + ZS)
    return C_KMS ** 2 / (4 * np.pi * G_PC) * ds / (dl * dls)


def main():
    sc = sigma_crit()
    room = {  # non-stellar compact column allowed, 2 sigma upper
        "chabrier_icl": SIG_STAR + 2 * SIG_STAR_ERR - SIG_STAR / 2,
        "salpeter_icl": SIG_STAR + 2 * SIG_STAR_ERR - SIG_STAR,
    }
    rows = []
    for kappa in (0.4, 0.65, 0.9):
        for f_cb in (0.25, 0.5):
            need = f_cb * kappa * sc
            rows.append({
                "kappa": kappa, "f_cb": f_cb, "cbdm_column_needed": round(need, 1),
                "excess_over_room_chabrier": round(need / room["chabrier_icl"], 2),
                "excess_over_room_salpeter": round(need / room["salpeter_icl"], 2),
            })
    least = min(r["excess_over_room_chabrier"] for r in rows)
    db1_case = [r for r in rows if r["kappa"] == 0.65 and r["f_cb"] == 0.5][0]
    out = {
        "sigma_crit_Msun_pc2": round(sc, 1),
        "sigma_star_over_sigma_crit": round(SIG_STAR / sc, 4),
        "room_2sigma_Msun_pc2": {k: round(v, 1) for k, v in room.items()},
        "rows": rows,
        "most_lenient_excess": least,
        "db1_central_excess_chabrier": db1_case["excess_over_room_chabrier"],
        "verdict": ("FAIL" if least > 1 else "OPEN")
        + ": compact CBDM in 0.1-100 Msun at the amount DB1 needs vs the measured microlens column",
    }
    print(json.dumps(out, indent=1))
    with open("lit_a370_dragon.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
