#!/usr/bin/env python3
"""CFG384 -- can a lambda|Phi|^4 self-interaction relax the ~eV cold-fluid field to CFG383's condensate split within the limits?
Frozen: FROZEN_CRITERIA.md.  Natural-unit cross-section sigma = lambda^2/(128 pi m^2); Bose-enhanced rate Gamma = D sigma v n.
CFG384_MUTATE=1 removes the Bose enhancement (D := 1; separate outputs)."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG384_MUTATE") == "1"; SLUG = "cfg384_si_bose" + ("_MUTATE" if MUTATE else "")
h, hbar, G, eV, c = 6.62607015e-34, 1.054571817e-34, 6.674e-11, 1.602176634e-19, 2.99792458e8
MSUN, PC, KPC, GYR, AGE = 1.989e30, 3.0857e16, 3.0857e19, 3.15576e16, 13.8
HBARC_CM = 1.97327e-5                      # eV cm
H0 = 67.4e3 / 3.0857e22; RHOC = 3 * H0**2 / (8 * math.pi * G)
LOG, OUT, CH = [], {"mutate": MUTATE}, []
def P(s=""): print(s); LOG.append(s)
def check(n, ok, v=""): CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")
VMW = 200e3
SYS = {"cluster": dict(sigma=1000e3, rho=0.85 * 500 * RHOC / 3),
       "MilkyWay": dict(sigma=VMW / math.sqrt(2), rho=VMW**2 / (4 * math.pi * G * (30 * KPC)**2))}
def sigma_cm2(lam, m_eV): return lam**2 / (128 * math.pi) * (HBARC_CM / m_eV)**2
def sigma_over_m(lam, m_eV): return sigma_cm2(lam, m_eV) / (m_eV * eV / c**2 * 1e3)           # cm^2 / g
def degeneracy(m_eV, rho, sv, g):
    m = m_eV * eV / c**2; return g * (rho / m) * (h / (m * sv * math.sqrt(2 * math.pi)))**3
def rate(lam, m_eV, s, g):                 # s^-1
    m = m_eV * eV / c**2; n = s["rho"] / m * 1e-6                                  # cm^-3
    D = 1.0 if MUTATE else max(degeneracy(m_eV, s["rho"], s["sigma"], g), 1.0)
    return D * sigma_cm2(lam, m_eV) * (s["sigma"] * 100) * n
def lam_min(m_eV, g):                      # G1: Gamma * age >= 1 in clusters AND MW
    return max(math.sqrt(1.0 / (rate(1.0, m_eV, s, g) * AGE * GYR)) for s in SYS.values())
def lam_max_bullet(m_eV):                  # G2: sigma/m < 1 cm^2/g
    return math.sqrt(1.0 / sigma_over_m(1.0, m_eV))
def lam_max_G3(m_eV):                      # c_s^2 = lam rho/(4 m^4) [natural units] -> SI: c_s^2/c^2 = lam rho_E (hbar c)^3/(4 (m c^2)^4)
    mE = m_eV * eV; hc3 = (hbar * c)**3
    rho_rec = 0.12 / 0.674**2 * RHOC * 1101**3 * c**2                          # J/m^3, cosmic cold at z = 1100
    lamA = 1e-6 * 4 * mE**4 / (rho_rec * hc3)                                    # c_s < 1e-3 c
    rhoMW = SYS["MilkyWay"]["rho"] * c**2
    cs_max = 1 * KPC * math.sqrt(G * SYS["MilkyWay"]["rho"])                    # Jeans length < 1 kpc
    lamB = (cs_max / c)**2 * 4 * mE**4 / (rhoMW * hc3)
    return min(lamA, lamB), lamA, lamB
check("C1 sigma(lambda) quadratic: sigma(2)/sigma(1) = 4", abs(sigma_cm2(2, 0.8) / sigma_cm2(1, 0.8) - 4) < 1e-12)
check("C2 Bullet bound inverse: sigma/m at lam_max = 1 cm^2/g", abs(sigma_over_m(lam_max_bullet(0.8), 0.8) - 1) < 1e-9)
ms = np.geomspace(0.62, 1.04, 9)
for g in (1, 2):
    rows = []
    for m in ms:
        lmin = lam_min(m, g); lb = lam_max_bullet(m); l3, l3a, l3b = lam_max_G3(m); lmax = min(lb, l3)
        rows.append(dict(m_eV=float(m), lam_min=lmin, lam_max_bullet=lb, lam_max_G3=l3, lam_G3_rec=l3a, lam_G3_jeans=l3b,
                         window_dex=math.log10(lmax / lmin), bullet_relax_factor=(lmin / lb)**2 if lmin > lb else 1.0))
    OUT[f"g{g}"] = rows
    P(f"\n  g = {g}:")
    for r in rows:
        P(f"    m {r['m_eV']:.3f} eV: lambda_min (relax) {r['lam_min']:.2e}; lambda_max Bullet {r['lam_max_bullet']:.2e}, G3 {r['lam_max_G3']:.2e} "
          f"(rec {r['lam_G3_rec']:.1e}, Jeans {r['lam_G3_jeans']:.1e}); window {r['window_dex']:+.2f} dex; Bullet would need x{r['bullet_relax_factor']:.2g}")
best = max(OUT["g1"], key=lambda r: r["window_dex"])
wd = best["window_dex"]
verdict = "OPEN WINDOW" if wd >= 0 else ("MARGINAL" if wd > -math.log10(3) else "CLOSED")
OUT["verdict"] = verdict; OUT["best"] = best
lb_m = lam_max_bullet(best["m_eV"])
P(f"\n  implied MW relaxation rate at lambda = lambda_max(Bullet), m {best['m_eV']:.2f}: Gamma = {rate(lb_m, best['m_eV'], SYS['MilkyWay'], 1) * 13.8 * GYR:.2e} per age "
  f"(record's settling window: ~3 H_L in the MW; 1 per age ~ 1 H_L)")
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT (g = 1, best m {best['m_eV']:.3f} eV): {verdict} (window {wd:+.2f} dex)")
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cfg384_si_bose_results.json")))
    check("MUTATE: window shrinks by > 1 dex without Bose enhancement", real["best"]["window_dex"] - wd > 1.0, f"{real['best']['window_dex']:+.2f} -> {wd:+.2f}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
