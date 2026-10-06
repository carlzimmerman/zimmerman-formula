"""cm12: predict the retention-step mass from t_cool = t_dyn with the framework's virial relation V^4 = G M_b a0.
Frozen: cm12_FROZEN_CRITERIA.md (d39a20280). No LCDM halo mass is used.
Run: python3 cm12_cooling_step.py | MUTATE=1 multiplies Lambda by 100 (separate outputs; the step must move > 0.3 dex)
"""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"; SLUG = "cm12_cooling_step" + ("_MUTATE" if MUTATE else "")
G, MSUN, MP, KB, KPC, KEV = 6.674e-8, 1.989e33, 1.6726e-24, 1.380649e-16, 3.0857e21, 1.602177e-9   # cgs
A0 = {"canonical": 9.3603e-9, "alt": 1.1312e-8}       # cm s^-2
MU = 0.6; NE_NH, N_NH = 1.17, 2.3
H0 = 67.4e5 / 3.0857e24; RHO_B = 0.0493 * 3 * H0**2 / (8 * math.pi * G)
BRACKET = (6e10, 2.2e12)
LOG, OUT, res = [], {"lane": "cm12", "frozen": "d39a20280", "mutate": MUTATE, "cells": {}}, []


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok):
    res.append(bool(ok)); P(("PASS  " if ok else "FAIL  ") + n)


def lam(T):                    # Tozzi & Norman 2001, Z = 0.3 Zsun; erg cm^3 s^-1
    kT = KB * T / KEV
    return (8.6e-3 * kT**-1.7 + 5.8e-2 * kT**0.5 + 6.3e-2) * 1e-23 * (100.0 if MUTATE else 1.0), (0.01 <= kT <= 20)


def ratio(Mb, a0, rad, fhot):
    M = Mb * MSUN; V = (G * M * a0) ** 0.25; T = MU * MP * V**2 / (2 * KB)
    R = math.sqrt(G * M / a0) if rad == "R1" else (3 * M / (4 * math.pi * 200 * RHO_B)) ** (1 / 3)
    rho = fhot * M / (4 / 3 * math.pi * R**3); nH = rho / (MU * MP * N_NH)    # n = rho/(mu m_p) = 2.3 n_H
    L, inrange = lam(T)
    tcool = 3 * N_NH * nH * KB * T / (2 * NE_NH * nH * nH * L); tdyn = R / V
    return tcool / tdyn, V / 1e5, T, R / KPC, inrange


P(f"cm12{' MUTATE (Lambda x100)' if MUTATE else ''}: bracket M_b in [{BRACKET[0]:.1e}, {BRACKET[1]:.1e}] Msun")
lM = np.linspace(9, 14, 2001)
# identity check: V^4 = G M_b a0 round trip
v = (G * 1e11 * MSUN * A0["canonical"]) ** 0.25
check("C1 V^4 = G M_b a0 round trip to 1e-12", abs(v**4 / (G * 1e11 * MSUN * A0["canonical"]) - 1) < 1e-12)
inside = 0
for foot, a0 in A0.items():
    for rad in ("R1", "R2"):
        for fhot in (1.0, 0.5):
            r = np.array([ratio(10**x, a0, rad, fhot)[0] for x in lM])
            up = np.where((r[:-1] < 1) & (r[1:] >= 1))[0]
            key = f"{foot}|{rad}|fhot{fhot}"
            if len(up) == 0:
                OUT["cells"][key] = {"crossing": None, "ratio_lo": float(r[0]), "ratio_hi": float(r[-1])}
                P(f"  {key:24s}: no upward crossing (t_cool/t_dyn {r[0]:.2e} at 1e9 -> {r[-1]:.2e} at 1e14)")
                continue
            i = up[0]; x = lM[i] + (0 - math.log10(r[i])) / (math.log10(r[i + 1]) - math.log10(r[i])) * (lM[i + 1] - lM[i])
            _, V, T, R, ok = ratio(10**x, a0, rad, fhot)
            hit = BRACKET[0] <= 10**x <= BRACKET[1]; inside += hit
            slope = float(np.polyfit(lM[(lM > x - 0.5) & (lM < x + 0.5)], np.log10(r[(lM > x - 0.5) & (lM < x + 0.5)]), 1)[0])
            OUT["cells"][key] = {"logMb_star": float(x), "V": V, "T": T, "R_kpc": R, "fit_in_range": bool(ok), "in_bracket": bool(hit),
                                 "dlog_ratio_dlogM": slope, "n_upward_crossings": int(len(up))}
            P(f"  {key:24s}: M_b* = 10^{x:.2f} Msun  V {V:.0f} km/s  T {T:.2e} K  R {R:.0f} kpc  slope {slope:+.2f}  "
              f"{'IN' if hit else 'OUT'}{'' if ok else '  (Lambda fit out of range)'}")
verdict = "PREDICTS" if inside == 8 else ("PARTIAL" if inside > 0 else "FAILS")
OUT["n_inside"] = int(inside); OUT["verdict"] = verdict
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT: {verdict} ({inside} of 8 cells inside the bracket)")
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cm12_cooling_step_results.json")))
    a = real["cells"]["canonical|R1|fhot1.0"].get("logMb_star"); b = OUT["cells"]["canonical|R1|fhot1.0"].get("logMb_star")
    check(f"MUTATE: canonical R1 f_hot 1 step moves > 0.3 dex ({a} -> {b})", a is None or b is None or abs(a - b) > 0.3)
P(f"\n{sum(res)}/{len(res)} pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(res) else 1)
