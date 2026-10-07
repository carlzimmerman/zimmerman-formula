#!/usr/bin/env python3
"""CFG383 -- the cold fluid as a Bose field: is the unsettled cluster fraction the normal (non-condensed) fraction?
Frozen: FROZEN_CRITERIA.md.  Ideal uniform Bose gas, k T = m sigma^2.  CFG383_MUTATE=1 sets sigma_cluster = sigma_MW (separate outputs)."""
import os, json, math
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG383_MUTATE") == "1"; SLUG = "cfg383_bec_split" + ("_MUTATE" if MUTATE else "")
h, hbar, G, eV, c = 6.62607015e-34, 1.054571817e-34, 6.674e-11, 1.602176634e-19, 2.99792458e8
MSUN, PC, KPC, GYR = 1.989e30, 3.0857e16, 3.0857e19, 3.15576e16
ZETA32 = 2.6123753486854883
H0 = 67.4e3 / 3.0857e22; RHOC = 3 * H0**2 / (8 * math.pi * G)
WIN = (2e-20, 2.78); CFG367_FREE = 8.8e-12
LOG, OUT, CH = [], {"mutate": MUTATE}, []
def P(s=""): print(s); LOG.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
VMW = 200e3
SYS = {"cluster": dict(sigma=1000e3, rho=0.85 * 500 * RHOC / 3, R=1.0e3 * KPC, br=(800e3, 1200e3)),
       "group": dict(sigma=400e3, rho=0.85 * 500 * RHOC / 3, R=0.5e3 * KPC, br=(300e3, 500e3)),
       "MilkyWay": dict(sigma=VMW / math.sqrt(2), rho=VMW**2 / (4 * math.pi * G * (30 * KPC)**2), R=30 * KPC, br=None),
       "UFD": dict(sigma=5e3, rho=1e6 * MSUN / (4 / 3 * math.pi * (100 * PC)**3), R=100 * PC, br=None)}
if MUTATE:
    SYS["cluster"]["sigma"] = SYS["MilkyWay"]["sigma"]
def degeneracy(m_eV, rho, sigma, g=1):
    m = m_eV * eV / c**2; lam = h / (m * sigma * math.sqrt(2 * math.pi)); return g * (rho / m) * lam**3
def unsettled(m_eV, rho, sigma, g=1):
    D = degeneracy(m_eV, rho, sigma, g); return 1.0 if D <= ZETA32 else ZETA32 / D
def m_for(u_target, rho, sigma, g=1):
    f = lambda lm: math.log(unsettled(10**lm, rho, sigma, g)) - math.log(u_target)
    return 10**brentq(f, -30, 3, xtol=1e-12)
def tau_gr(m_eV, rho, sigma, R):       # Levkov et al. 2018 gravitational condensation time
    m = m_eV * eV / c**2; n = rho / m; v = sigma; lnL = max(math.log(m * v * R / hbar), 1.0)
    return 0.7 * math.sqrt(2) / (12 * math.pi**3) * m * v**6 / (G**2 * n**2 * hbar**3 * lnL) / GYR
# identity checks
D0 = degeneracy(1.0, SYS["cluster"]["rho"], 1e6)
check("C1 u = zeta(3/2)/D above threshold and u(m_half) = 0.5 round trip", abs(unsettled(m_for(0.5, SYS["cluster"]["rho"], 1e6), SYS["cluster"]["rho"], 1e6) - 0.5) < 1e-9)
check("C2 degeneracy scales as m^-4 at fixed rho, sigma (n ~ 1/m, lambda^3 ~ m^-3)", abs(degeneracy(2.0, SYS["cluster"]["rho"], 1e6) / D0 - 2.0**-4) < 1e-12)
for g in (1, 2):
    tag = f"g{g}"; cl = SYS["cluster"]
    mh = m_for(0.5, cl["rho"], cl["sigma"], g)
    lo = m_for(0.7, cl["rho"], cl["br"][0], g) if not MUTATE else float("nan")     # more unsettled + colder -> lower m bound
    hi = m_for(0.3, cl["rho"], cl["br"][1], g) if not MUTATE else float("nan")
    res = {"m_half_eV": mh, "m_range_eV": [lo, hi], "in_window": WIN[0] <= mh <= WIN[1], "above_CFG367_free_edge": mh >= CFG367_FREE, "u": {}, "tau_gr_Gyr": {}}
    P(f"\n  {tag} ({'one species' if g == 1 else 'particle + antiparticle'}): m_half (clusters u = 0.5) = {mh:.3g} eV; bracket [{lo:.3g}, {hi:.3g}] eV; "
      f"in fluid window {WIN}: {res['in_window']}; above CFG367 free edge: {res['above_CFG367_free_edge']}")
    for name, s in SYS.items():
        u = unsettled(mh, s["rho"], s["sigma"], g); t = tau_gr(mh, s["rho"], s["sigma"], s["R"])
        res["u"][name] = u; res["tau_gr_Gyr"][name] = t
        P(f"     {name:9s}: sigma {s['sigma']/1e3:6.1f} km/s, rho_c {s['rho']:.2e} kg/m^3, degeneracy {degeneracy(mh, s['rho'], s['sigma'], g):.3g}, "
          f"unsettled u = {u:.3g}; gravitational condensation time {t:.2e} Gyr ({'< age' if t < 13.8 else '> AGE'})")
    ok = [res["in_window"], res["u"]["MilkyWay"] < 0.05, res["u"]["UFD"] < 0.05, res["u"]["group"] < res["u"]["cluster"]]
    res["verdict"] = "VIABLE" if all(ok) else ("PARTIAL" if any(ok) else "FAILS")
    if not res["in_window"] or res["u"]["MilkyWay"] >= 0.05 or res["u"]["UFD"] >= 0.05:
        res["verdict"] = "FAILS" if not res["in_window"] else res["verdict"]
    OUT[tag] = res
    P(f"     -> {tag} verdict: {res['verdict']}  (checks window/MW/UFD/order = {ok})")
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cfg383_bec_split_results.json")))
    mh_real = real["g1"]["m_half_eV"]; uc = unsettled(mh_real, SYS["cluster"]["rho"], SYS["cluster"]["sigma"])
    check(f"MUTATE: with sigma_cluster = sigma_MW, clusters are condensed (u < 0.05) at the real run's m_half {mh_real:.3g} eV", uc < 0.05, f"u = {uc:.3g}")
OUT["verdict"] = OUT["g1"]["verdict"]
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT (one species, primary): {OUT['verdict']}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=str)
raise SystemExit(0 if all(CH) else 1)
