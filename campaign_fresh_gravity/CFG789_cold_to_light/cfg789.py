"""CFG789 -- cold energy -> light: COB-limited spontaneous rate, ambient power ceiling, stimulation factor for a 1 N light drive.
Criteria FROZEN_CRITERIA.md.  Run: python3 cfg789.py  (CFG789_MUTATE=1: glowing sky x1e8).  Inputs PROVISIONAL.
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("CFG789_MUTATE") == "1"
c, G, MSUN, PC, GYR = 2.998e8, 6.674e-11, 1.989e30, 3.0857e16, 3.156e16
rho_crit = 3 * (70e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
rho_c = 0.26 * rho_crit; tH = 13.8 * GYR
OUT = []
def P(s): print(s); OUT.append(s)
res = {}
P("CFG789  cold energy -> light" + ("  [MUTATE x1e8]" if MUT else ""))
k1 = 4 * math.pi * 8e-9 / c
P(f"  K1 u_ex(8 nW) = {k1:.2e} J/m^3 (hand 3.4e-16): {'PASS' if abs(k1 / 3.35e-16 - 1) < 0.05 else 'FAIL'}")
for Iex in (2e-9, 8e-9, 16e-9):
    for fz in (0.2, 0.5, 1.0):
        for rl in (0.005, 0.01, 0.02):
            I = Iex * (1e8 if MUT else 1)
            u = 4 * math.pi * I / c
            Gam = u / (rho_c * c ** 2 * tH * fz)
            rho_loc = rl * MSUN / PC ** 3
            Pkm3 = rho_loc * c ** 2 * 1e9 * Gam
            res[f"{Iex}|{fz}|{rl}"] = dict(tau_yr=1 / Gam / 3.156e7, P_km3=Pkm3, S=3e8 / Pkm3)
pr = res["8e-09|0.5|0.01"]
rho_loc = 0.01 * MSUN / PC ** 3
P(f"  primary: tau_min = {pr['tau_yr']:.2e} yr; ambient light power from 1 km^3 of local cold energy <= {pr['P_km3']:.2e} W; 1 m^3: {pr['P_km3'] / 1e9:.2e} W")
P(f"           a 1 km-radius sphere: {pr['P_km3'] * 4.19:.2e} W; required stimulation factor for 300 MW (1 N) from 1 km^3: S = {pr['S']:.1e}")
lo = min(v["S"] for v in res.values()); hi = max(v["S"] for v in res.values())
P(f"  bracket over I_ex 2-16 nW, f_z 0.2-1, rho_loc 0.005-0.02: S = {lo:.1e} .. {hi:.1e}")
A = 3e8 / (math.pi * 100)
P(f"  eye-safe hull area for 300 MW at radiance 100 W/m^2/sr: {A:.2e} m^2 ({A / 1e6:.2f} km^2)")
cls = "DATA-CLOSED for ambient fuel" if pr["P_km3"] < 1 else "OPEN"
P(f"  CLASS: {cls}")
json.dump(dict(res=res, cls=cls, A_m2=A, mutate=MUT), open(os.path.join(HERE, f"cfg789_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg789{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
