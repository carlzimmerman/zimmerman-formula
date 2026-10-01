"""CFG263 compare step: after the independent re-derivations (scripts 01-08) were run, read the ORIGINAL lanes'
committed outputs (read-only) and compare their load-bearing numbers with this audit's values in results.json.
Also reconciles the one discrepancy found (lane K's 'fraction of c from x < X').
Nothing outside this directory is written.
"""
import json
import os
import re
import mpmath as mp
from cfg263_lib import Checks, run_main, HERE

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = os.path.join(ROOT, "sonnet55_push", "puzzle_32pi")
A = os.path.join(P, "agents")
mp.mp.dps = 30


def read(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return fh.read()


def grab(text, pattern, cast=float):
    m = re.search(pattern, text)
    return cast(m.group(1)) if m else None


def main():
    C = Checks("COMPARE")
    R = json.load(open(os.path.join(HERE, "results.json")))
    v = lambda lane, key: R[lane]["values"][key]

    # G
    g02 = read("sonnet55_push/puzzle_32pi/agents/G_symmetry_conformal/g02_scale_symmetry_and_offset.out")
    # own fix: the first regex for w_g matched an earlier (sharp-transition) line; both numbers now read from the RAR line
    c_g = grab(g02, r"RAR \(exponential nu\): c = ([0-9.]+)")
    w_g = grab(g02, r"RAR \(exponential nu\): c = [0-9.]+ ; G rho/a0\^2 = c/\(8 pi\) = ([0-9.]+)")
    C.check("G_RAR_offset", abs(c_g - v("NG-G", "RAR_offset_c")) < 1e-4 and abs(w_g - v("NG-G", "RAR_Grho_over_a0sq")) < 1e-4,
            f"lane G {c_g}, {w_g} vs audit {v('NG-G','RAR_offset_c'):.6f}, {v('NG-G','RAR_Grho_over_a0sq'):.6f} (= 4pi^4/15, pi^3/30)")
    g04 = read("sonnet55_push/puzzle_32pi/agents/G_symmetry_conformal/g04_conformal_group_desitter.out")
    C.check("G_killing_signature", "(6, 4)" in g04 and R["NG-G"]["checks"][[c["id"] for c in R["NG-G"]["checks"]].index("G8c_killing_form_so41")]["pass"],
            "lane G (neg,pos) = (6,4); audit (+4,-6): same so(4,1)")

    # E
    e01 = read("sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/e01_derivation_algebra.out")
    C.check("E_coefficients", "a0hat = 2H" in e01 and "exactly 1/6" in e01 and "1.376e-10" in e01,
            "lane E: T - T_Lambda a0 = 2H, Verlinde 1/6, van Putten 1.376e-10 at H0 = 70; audit: 2H, 1/6, 0.20231 cH")
    e02 = read("sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/e02_pi_class_and_normalisation.out")
    C.check("E_verlinde_d_min", "5.828" in e02 or "3 + 2 sqrt2" in e02 or "2*sqrt(2) + 3" in e02, "lane E d-continuation minimum 5.828 = 3 + 2 sqrt2 (audit E7 identical)")

    # X1
    x15 = read("sonnet55_push/puzzle_32pi/agents/X1_one_generator/x1_05_noether_euler_static_patch.out")
    need = grab(x15, r"G\|Q\|/L = Z\^3/16 = ([0-9.]+)")
    C.check("X1_noether_need_Lunits", abs(need - float(mp.sqrt(32 * mp.pi / 3)**3 / 16)) < 1e-4,
            f"lane X1 G|Q|/L = {need} (Lambda-units) = audit X1_3; lane X1 never evaluates the charge in u-units (no 'G rho'-normalised unit in x1_05.out)")
    C.check("X1_alpha_and_EOM_premise", "(1 + 4 alpha/L^2) Q_EH(r)" in x15 and "equation-of-motion statement" in x15,
            "lane X1 P5 alpha-rescaling = audit X1_5; the 'a0 = (1/2) sqrt(G rho) is an equation-of-motion statement' premise is asserted at x1_05.out:39, not derived")
    C.check("X1_uunit_absent_in_original", ("u-unit" not in x15) and ("G rho" not in x15.split("P4")[1].split("P5")[0] if "P4" in x15 else True),
            "x1_05 P3/P4 (pi-power, 'units') are evaluated with L held fixed only: the H3-class unit dependence is uncorrected in X1")

    # K
    k01 = read("sonnet55_push/puzzle_32pi/agents/K_density_linear_family/k01_offset_relocation.out")
    m = re.search(r"RAR-nu \(c = 25\.98\):\s+([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+)", k01)
    kfr = [float(m.group(i)) for i in range(1, 5)]
    # reconcile: lane K computes int_0^X x^2 dmu (partial second moment); the audit computed int_0^X (1-mu) d(x^2).
    # They differ by the boundary term X^2 (1 - mu(X)).
    def mu_rar(xv):
        lo = ((mp.sqrt(1 + 4 * xv) - 1) / 2)**2; hi = xv
        fn = lambda t: t / (-mp.expm1(-mp.sqrt(t))) - xv
        for _ in range(110):
            mid = (lo + hi) / 2
            if fn(mid) > 0:
                hi = mid
            else:
                lo = mid
        return ((lo + hi) / 2) / xv
    ctot = 4 * mp.pi**4 / 15
    stj = []
    for Xc in (3, 10, 30, 100):
        aud = mp.mpf(v("NG-K", f"RAR_fraction_below_x{Xc}")) * ctot
        stj.append(float((aud - Xc**2 * (1 - mu_rar(mp.mpf(Xc)))) / ctot))
    C.check("K_accumulation_reconciled", all(abs(a - b) < 2e-3 for a, b in zip(stj, kfr)),
            f"lane K fractions {kfr} = audit's partial second moment {[round(s, 3) for s in stj]} (audit's (1-mu)d(x^2) fractions differ by X^2(1-mu(X))): definitional, NOT an error")
    # own fix: the first regex matched lane K's other N* (2.0797, the c = 32 pi reading); read the F6 line
    nstar = grab(k01, r"N\* = \(3 \+ sqrt\(1 \+ 1/pi\)\)/2 = ([0-9.]+)")
    C.check("K_Nstar", abs(nstar - v("NG-K", "Nstar")) < 1e-3, f"lane K N* = {nstar} vs audit {v('NG-K','Nstar'):.5f}")

    # L
    l01 = read("sonnet55_push/puzzle_32pi/agents/L_sds_two_horizon/l01_sds_facts.out")
    mub = grab(l01, r"mu_b\* = ([0-9.]+)"); muc = grab(l01, r"mu_c\* = ([0-9.]+)")
    C.check("L_a0_points", abs(mub - v("NG-L", "mu_star_b")) < 1e-9 and abs(muc - v("NG-L", "mu_star_c")) < 1e-8,
            f"lane L mu*_b {mub}, mu*_c {muc} vs audit {v('NG-L','mu_star_b'):.10f}, {v('NG-L','mu_star_c'):.8f}")
    l02 = read("sonnet55_push/puzzle_32pi/agents/L_sds_two_horizon/l02_principles_E1_E5.out")
    C.check("L_functionals", "19 of 19 functionals" in l02 and "none" in l02, "lane L: 19/19 functionals monotone; audit L9: no sign change in 19 (16 distinct) functionals")

    # N
    n03 = read("sonnet55_push/puzzle_32pi/agents/N_jacobson_thermo_dS/n03_dS_clausius_no_crossover.out")
    n04 = read("sonnet55_push/puzzle_32pi/agents/N_jacobson_thermo_dS/n04_conversion_and_crossover.out")
    C.check("N_pair_and_a0", "exactly ONE mismatched pair" in n03 and "(kobs, a)" in n03 and "a0 = H" in n04,
            "lane N: one pair (kobs, a), a0 = H; audit N3/N4: identical")

    # p12, B3
    p12 = read("sonnet55_push/puzzle_32pi/p12_horizon_equation_no_local_bridge.out")
    C.check("P12_values", "-12.0664" in p12 and "7/7" in p12, "p12 (B) kappa r_h = -12.0664; audit P3B identical")
    b01 = read("sonnet55_push/puzzle_32pi/agents/B3_modified_horizon_equation/b01.out")
    b03 = read("sonnet55_push/puzzle_32pi/agents/B3_modified_horizon_equation/b03.out")
    C.check("B3_values", "N_h = 1/(1-8 pi) = -0.04144" in b01 and "-8 pi/3" in b03 and "-15.7552" in b03,
            "B3: signed kappa needs N_h = 1/(1-8pi) < 0 (BH-type excluded); GL a = -8pi/3, 1+2a = -15.7552; audit P7b identical. "
            "B3 does not treat the cosmological-type |kappa| reading (N_h = +1/(8pi-1)); audit P5 closes it under NEC")

    # sol61
    sres = json.loads(read("sol61_push/runs/clock_bbn/results.json"))
    sres2 = json.loads(read("sol61_push/runs/clock_coefficient_bound/results.json"))
    C.check("S61_runs", sres.get("passed") is True and sres2.get("passed") is True and abs(v("NG-S61", "R_max") - 0.8238740919142051) < 1e-14,
            f"sol61 runs passed; R_max audit {v('NG-S61','R_max'):.16f} vs 0.8238740919142051")

    return C.write()


if __name__ == "__main__":
    run_main(main)
