"""GD1b (AMENDMENT A1, reported): can the core law's own self-coupling (LN1 T7) lift the Milky Way's halo pull at R0?

The native lift is the thermalised (Gamma t >= 1) region relaxing to isothermal equilibrium in the TOTAL potential
(baryons included). Inside the thermal radius r1 the halo is redistributed with M(<r1) conserved; outside r1 the OS1
Burkert halo is untouched. So the halo pull at R0 can change only if r1 > R0.
r1 from T7 with no new number: Gamma t = rho K sigma^(1-n) t, K t = 9 sigma_ref^(1+n) / (4 pi G Sigma_a0^2) (LN2 / BU1),
so Gamma(r1) t = 1 at rho(r1) = 4 pi G Sigma_a0^2 / (9 sigma_ref^(1+n) sigma^(1-n)). t cancels.
sigma = V_last/sqrt2 (OS1/SC1), n = 2 q_f - 1. Reads GD1's OS1 results (gd1_route_e_mw_results_OS1_V*.json).
kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Run: python3 gd1b_thermal_radius.py [--mutate]
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import brentq

MUTATE = "--mutate" in sys.argv                       # mutate: drop the (1-n) exponent's sigma factor -> K5 fails
HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091e-6; SREF = 70.50; QF = {"canonical": 0.892, "alt": 0.748}; SIG_A0 = {"canonical": 106.879e6, "alt": 129.165e6}
R0 = 8.122; VC_E, VC_E_ERR = 229.053, 4.645
OUT = []; RES = {"rows": {}, "checks": {}}
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)
def B(x): return math.log1p(x * x) + 2 * math.log1p(x) - 2 * math.atan(x)
P("GD1b thermal radius of the OS1 Milky Way halo (T7, no new number)", "MUTATE" if MUTATE else "")
checks = []
for V in (172.98, 229.05):
    J = json.load(open(os.path.join(HERE, f"gd1_route_e_mw_results_OS1_V{V:.0f}.json")))
    for f in ("canonical", "alt"):
        n = 2 * QF[f] - 1; sig = V / math.sqrt(2)
        Sig = SIG_A0[f] * (sig / SREF) ** QF[f]
        rho1 = 4 * math.pi * G * SIG_A0[f] ** 2 / (9 * SREF ** (1 + n) * (1.0 if MUTATE else sig ** (1 - n)))   # Msun/kpc^3
        row = J["rows"]["1.000000"][f"{f}|A_c2b_refit"]; r0 = row["r0_kpc"]; rho0 = Sig / r0
        rho = lambda r: rho0 / ((1 + r / r0) * (1 + (r / r0) ** 2))
        GtR0 = rho(R0) / rho1                                           # Gamma t at R0
        r1 = brentq(lambda r: rho(r) - rho1, 1e-6, 1e4) if rho0 > rho1 else 0.0
        vbar = J["today"][f]["Vbar_R0"]
        Mr1 = math.pi * Sig * r0 ** 2 * B(r1 / r0)
        v_bound = math.sqrt(vbar ** 2 + G * Mr1 / R0) if r1 > R0 else row["V8"]   # all of M(<r1) inside R0: upper bound
        # Gamma t multiplier m needed for the upper bound to reach Eilers: r1(m) with rho(r1) = rho1/m
        def vb_of(m):
            if rho0 <= rho1 / m: return row["V8"]                       # Gamma t < 1 everywhere: nothing thermalised
            rr = brentq(lambda r: rho(r) - rho1 / m, 1e-6, 1e5)
            return math.sqrt(vbar ** 2 + G * math.pi * Sig * r0 ** 2 * B(rr / r0) / R0) if rr > R0 else row["V8"]
        m_need = brentq(lambda m: vb_of(m) - VC_E, 1.0001, 1e6) if vb_of(1e6) > VC_E else float("inf")
        RES["rows"][f"V{V:.0f}|{f}"] = dict(n=n, sigma=sig, rho1_Msun_pc3=rho1 / 1e9, rho0_Msun_pc3=rho0 / 1e9, r0_kpc=r0, r1_kpc=r1,
                                           Gamma_t_at_R0=GtR0, Vc_R0_OS1=row["V8"], Vc_R0_upper_bound=v_bound, z_bound=(v_bound - VC_E) / VC_E_ERR,
                                           Gamma_t_multiplier_needed=m_need)
        P(f"V_last {V:6.2f} [{f:<9}] n {n:.3f}: rho0 {rho0/1e9:.4f}, rho(Gt=1) {rho1/1e9:.4f} Msun/pc^3 -> r1 {r1:5.2f} kpc "
          f"(r0 {r0:.1f}, R0 {R0}); Gamma t at R0 {GtR0:.2f}; V_c(R0) OS1 {row['V8']:.1f} -> upper bound {v_bound:.1f} "
          f"(z {(v_bound - VC_E) / VC_E_ERR:+.1f}); Gamma t x{m_need:.1f} needed for the bound to reach {VC_E}")
        checks.append((f"K5_T7_rho1_V{V:.0f}_{f}", abs(rho1 * 9 * SREF ** (1 + n) * sig ** (1 - n) / (4 * math.pi * G * SIG_A0[f] ** 2) - 1) < 1e-12))
for k, v in checks:
    P(f"{k}: {'PASS' if v else 'FAIL'}"); RES["checks"][k] = bool(v)
tag = "_MUTATE" if MUTATE else ""
json.dump(RES, open(os.path.join(HERE, f"gd1b_thermal_radius_results{tag}.json"), "w"), indent=1)
open(os.path.join(HERE, f"gd1b_thermal_radius{tag}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v for _, v in checks) else 1)
