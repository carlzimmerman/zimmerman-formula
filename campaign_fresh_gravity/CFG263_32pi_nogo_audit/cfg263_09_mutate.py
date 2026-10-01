"""CFG263 MUTATE controls (declared in CFG263_FROZEN_CRITERIA.md section 6).

M-ERR-1  plant 8 pi -> 4 pi in a COPY of the p12 horizon identity: the audit's independent Ricci-tensor check must FAIL
M-ERR-2  plant c(N) = 2N^2/((N-1)(N+2)) in a COPY of the K offset derivation: the quadrature check must FAIL
M-ERR-3  plant Q = r^2 f'/(2G) (Komar instead of Iyer-Wald) in a COPY of the X1 charge derivation: the vacuum-mass check must FAIL
M-PREM-1a change the held-fixed variable (Lambda -> G rho_Lambda) for X1's pi-power claim: the frozen classifier must change class
M-PREM-1b drop the null energy condition between the normalising observer and the horizon in p12's strengthened (D): the class must change

Mutant copies are written to mutants/ and their results to mutants/results_MUTATE_*.json (never the main results.json).
"""
import os
import re
import subprocess
import sys
import numpy as np
import mpmath as mp
from cfg263_lib import Checks, run_main, classify, HERE

MUT = os.path.join(HERE, "mutants")
os.makedirs(MUT, exist_ok=True)


def make_mutant(src, tag, old, new):
    with open(os.path.join(HERE, src)) as fh:
        s = fh.read()
    assert s.count(old) == 1, f"mutation anchor not unique in {src}: {old!r}"
    s = s.replace(old, new)
    dst = os.path.join(MUT, src.replace(".py", f"_MUTATE_{tag}.py"))
    with open(dst, "w") as fh:
        fh.write(s)
    env = dict(os.environ, CFG263_RESULTS=os.path.join(MUT, f"results_MUTATE_{tag}.json"), PYTHONPATH=HERE)
    p = subprocess.run([sys.executable, dst], capture_output=True, text=True, env=env, cwd=HERE, timeout=900)
    with open(dst.replace(".py", ".out"), "w") as fh:
        fh.write(p.stdout + p.stderr)
    fails = re.findall(r"\[FAIL\] ([^\s]+)", p.stdout)
    return p.returncode, fails, p.stdout + p.stderr


def main():
    C = Checks("MUTATE")

    # M-ERR-1
    rc, fails, _ = make_mutant("cfg263_07_P12_B3_horizon.py", "ERR1_8pi_to_4pi",
                               "ident = sp.simplify(1 - 2 * (fp_h / 2) * rh - 8 * sp.pi * rho_h * rh**2)",
                               "ident = sp.simplify(1 - 2 * (fp_h / 2) * rh - 4 * sp.pi * rho_h * rh**2)")
    C.check("M_ERR1_caught", rc != 0 and any("P2_horizon_identity" in f for f in fails), f"exit {rc}, failed checks {fails}")

    # M-ERR-2
    rc, fails, _ = make_mutant("cfg263_04_K_density_linear.py", "ERR2_cN",
                               "target = 2 * N**2 / ((N - 1) * (N - 2))",
                               "target = 2 * N**2 / ((N - 1) * (N + 2))")
    C.check("M_ERR2_caught", rc != 0 and any("K2c_OR_family" in f for f in fails), f"exit {rc}, failed checks {fails}")

    # M-ERR-3
    rc, fails, _ = make_mutant("cfg263_03_X1_generator_noether.py", "ERR3_komar_for_IW",
                               "Q_IW = MK / 2                         # Iyer-Wald Noether charge of EH = half Komar",
                               "Q_IW = MK                             # MUTANT: Komar used as the Iyer-Wald charge")
    C.check("M_ERR3_caught", rc != 0 and any("X1_2b_charge_is_minus_vacuum_mass" in f for f in fails) and any("X1_1b_schwarzschild_norm" in f for f in fails),
            f"exit {rc}, failed checks {fails}")

    # M-PREM-1a: X1 pi-power claim, 'no rational multiple of pi^k at the a0 radius', tested in the admitted unit systems
    mp.mp.dps = 50
    def rational_times_pi_power(val):
        for k in range(0, 4):
            try:
                if mp.findpoly(val / mp.pi**k, 1, maxcoeff=10**4) is not None:
                    return True
            except Exception:
                pass
        return False
    Z = mp.sqrt(32 * mp.pi / 3)
    q_L = Z**3 / 16                    # G|Q|/L at r = Z L/2
    q_u = mp.mpf(4) / 3 * mp.pi        # G|Q| u at r = 1/u
    def x1_class(units):
        holds = all(not rational_times_pi_power(q) for q in units)
        # the claim is worded unit-free; if it fails in an admissible unit system it is a unit-dependent pi-count
        return classify({"step_false": False, "premise_unverified": not holds, "headline_scope_ok": holds})
    cls_L = x1_class([q_L])
    cls_Lu = x1_class([q_L, q_u])
    C.check("M_PREM1a_class_shifts", cls_L == "CORRECT-GENERAL" and cls_Lu == "PREMISE-UNVERIFIED",
            f"Lambda held fixed only: {cls_L}; G rho_Lambda admitted: {cls_Lu}")

    # M-PREM-1b: p12 strengthened (D) with and without NEC. Units r_h = 1, G rho_L = 1 (Lambda r_h^2 = 8 pi).
    rv, ra, rb, rhod = 0.97, 0.5, 0.7, 0.05
    shell = 4 * np.pi / 3 * (1 - rv**3); layer = 4 * np.pi / 3 * rhod * (rb**3 - ra**3)
    m0 = 0.5 - shell - layer
    rs = np.linspace(2 * m0 + 0.01, 0.999, 40001)
    def m_of(r):
        out = m0 + 4 * np.pi / 3 * rhod * (np.clip(r, ra, rb)**3 - ra**3)
        return out + 4 * np.pi / 3 * (np.clip(r, rv, 1)**3 - rv**3)
    fv = 1 - 2 * m_of(rs) / rs
    fp_h = (1 - 8 * np.pi)     # f'(r_h) r_h with rho(r_h) = rho_L, r_h = 1
    def kappa_rh(pr_layer):
        # rho + p_r: layer contributes rho_d + p_r(layer); vacuum shell 0; vacuole 0
        dens = np.where((rs > ra) & (rs < rb), rhod + pr_layer, 0.0)
        integrand = 4 * np.pi * rs * dens / fv
        dlnN = np.trapezoid(integrand, rs) if hasattr(np, "trapezoid") else np.trapz(integrand, rs)
        return np.exp(dlnN) * abs(fp_h) / 2, dlnN
    k_nec, d_nec = kappa_rh(0.0)                          # dust: rho + p_r = rho_d > 0
    from scipy.optimize import brentq
    pr_star = brentq(lambda p: kappa_rh(p)[0] - 0.5, -10, 0.0)
    k_ex, d_ex = kappa_rh(pr_star)
    nec_holds_everywhere = (rhod + 0.0) >= 0
    nec_violated = (rhod + pr_star) < 0
    def p12_class(k_value, nec):
        # strengthened (D): '|kappa| r_h = 1/2 is impossible for every static-patch normalisation'
        holds = abs(k_value - 0.5) > 1e-6 and k_value > 0.5
        return classify({"step_false": False, "premise_unverified": False, "headline_scope_ok": holds})
    c_nec = p12_class(k_nec, True)
    c_ex = p12_class(k_ex, False)
    C.check("M_PREM1b_class_shifts", nec_holds_everywhere and nec_violated and abs(k_ex - 0.5) < 1e-6 and c_nec == "CORRECT-GENERAL" and c_ex == "CORRECT-NARROWER-THAN-WORDED",
            f"NEC layer: |kappa| r_h = {k_nec:.2f} -> {c_nec}; exotic radial tension p_r = {pr_star:.3f} (rho + p_r = {rhod + pr_star:.3f} < 0) gives "
            f"ln(N_h/N_ref) = {d_ex:.3f} = -ln(8pi - 1) = {-np.log(8*np.pi-1):.3f} and |kappa| r_h = {k_ex:.6f} -> {c_ex}: the strengthened (D) needs NEC")
    C.value("M_PREM1b_pr_star", pr_star)
    return C.write()


if __name__ == "__main__":
    run_main(main)
