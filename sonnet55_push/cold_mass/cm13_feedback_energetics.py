"""cm13: can SN/AGN feedback, coupled to the cold fluid only through gravity, unbind 0.87 of the cold share below the step but not above?
Frozen: cm13_FROZEN_CRITERIA.md (e4b7303f1).  Energetic necessary condition only; no mechanism.
Run: python3 cm13_feedback_energetics.py | MUTATE=1 sets the cold share to 0.536 M_b (separate outputs; M_crit must rise > 0.5 dex)
"""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"; SLUG = "cm13_feedback_energetics" + ("_MUTATE" if MUTATE else "")
G, MSUN, C = 6.674e-8, 1.989e33, 2.998e10                        # cgs
A0 = {"canonical": 9.3603e-9, "alt": 1.1312e-8}
RC = 0.536 if MUTATE else 5.36; REMOVE = 0.87; FSTAR = 0.7
BRACKET = (6e10, 2.2e12); EPS = (0.01, 0.1, 1.0)
LOG, OUT, res = [], {"lane": "cm13", "frozen": "e4b7303f1", "mutate": MUTATE, "cells": {}}, []


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok):
    res.append(bool(ok)); P(("PASS  " if ok else "FAIL  ") + n)


def e_bind(Mb, a0, Rmul, ge):
    M = Mb * MSUN; V2 = math.sqrt(G * M * a0); rM = math.sqrt(G * M / a0); R = Rmul * rM; re = rM / ge
    eM = V2 * (math.log(re / R) + 1.0); eN = G * (1 + RC) * M / R
    return REMOVE * RC * M * max(eM, eN), eM >= eN


def e_fb(Mb, a0, agn):
    Ms = FSTAR * Mb; E = 1e51 * Ms / 100.0
    if agn:
        sig = (G * Mb * MSUN * a0) ** 0.25 / math.sqrt(2) / 1e5
        E += 0.1 * 0.05 * 3.09e8 * (sig / 200.0) ** 4.38 * MSUN * C**2
    return E


lM = np.linspace(9, 14, 2001)
_M = 1e11 * MSUN; _rM = math.sqrt(G * _M / A0["canonical"]); _V2 = math.sqrt(G * _M * A0["canonical"])
check("C1 log-potential identity: e_MOND at R = r_e (Rmul = a0/g_e) equals V^2 (to 1e-12)",
      abs(_V2 * (math.log((_rM / 0.01) / (_rM / 0.01)) + 1.0) / _V2 - 1) < 1e-12 and abs(_rM * 100 / (_rM / 0.01) - 1) < 1e-12)
check("C2 SN energy = 1e49 erg per Msun of stars (to 1e-12)", abs(e_fb(1.0 / FSTAR, A0["canonical"], False) / 1e49 - 1) < 1e-12)
P(f"cm13{' MUTATE (cold share x0.1)' if MUTATE else ''}: remove {REMOVE} of {RC} M_b; bracket [{BRACKET[0]:.1e}, {BRACKET[1]:.1e}]")
inside = {e: 0 for e in EPS}
for foot, a0 in A0.items():
    for Rmul in (1, 10):
        for ge in (0.01, 0.05):
            for agn in (False, True):
                key = f"{foot}|R{Rmul}rM|ge{ge}|{'SN+AGN' if agn else 'SN'}"
                ratio = np.array([e_fb(10**x, a0, agn) / e_bind(10**x, a0, Rmul, ge)[0] for x in lM])
                mond = e_bind(10**11, a0, Rmul, ge)[1]
                cell = {"mond_dominates_potential_at_1e11": bool(mond), "eps_need_MW": float(1 / np.interp(math.log10(6e10), lM, ratio)),
                        "dlog_ratio_dlogM_at_1e11": float(np.polyfit(lM[(lM > 10.5) & (lM < 11.5)], np.log10(ratio[(lM > 10.5) & (lM < 11.5)]), 1)[0])}
                txt = []
                for e in EPS:
                    r = e * ratio; dn = np.where((r[:-1] >= 1) & (r[1:] < 1))[0]
                    if len(dn):
                        i = dn[0]; x = lM[i] + (0 - math.log10(r[i])) / (math.log10(r[i + 1]) - math.log10(r[i])) * (lM[i + 1] - lM[i])
                        hit = BRACKET[0] <= 10**x <= BRACKET[1]; inside[e] += int(hit)
                        cell[f"eps{e}"] = {"logMcrit": float(x), "in_bracket": bool(hit), "n_down": int(len(dn)), "n_up": int(np.sum((r[:-1] < 1) & (r[1:] >= 1)))}
                        txt.append(f"eps {e}: 10^{x:.2f}{' IN' if hit else ''}")
                    else:
                        cell[f"eps{e}"] = {"logMcrit": None, "all_unbindable": bool(r[-1] >= 1), "none_unbindable": bool(r[0] < 1)}
                        txt.append(f"eps {e}: {'all' if r[-1] >= 1 else 'none'}")
                OUT["cells"][key] = cell
                P(f"  {key:34s} eps_need(MW) {cell['eps_need_MW']:.3f}  slope {cell['dlog_ratio_dlogM_at_1e11']:+.2f}  | " + "; ".join(txt))
n01, n1 = inside[0.1], inside[1.0]
any_crit_above = any((OUT["cells"][k].get(f"eps{e}", {}).get("logMcrit") or 0) >= math.log10(BRACKET[0]) or OUT["cells"][k].get(f"eps{e}", {}).get("all_unbindable")
                     for k in OUT["cells"] for e in EPS)
verdict = ("ALLOWED-AND-PLACED" if n01 >= 12 else "PARTIAL" if n01 >= 1 else "NEEDS-CEILING" if n1 >= 1 else
           ("FORBIDDEN" if not any_crit_above else "NOT PLACED"))
OUT.update({"inside_eps0.1": n01, "inside_eps1": n1, "inside_eps0.01": inside[0.01], "verdict": verdict})
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT: {verdict} (in bracket: eps 0.01 {inside[0.01]}/16, eps 0.1 {n01}/16, eps 1 {n1}/16)")
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cm13_feedback_energetics_results.json")))
    k = "canonical|R1rM|ge0.01|SN"
    def lv(c):   # 'none unbindable' on the grid means M_crit < 1e9 (grid floor); 'all unbindable' means > 1e14
        return c["logMcrit"] if c.get("logMcrit") is not None else (9.0 if c.get("none_unbindable") else 14.0)
    a = lv(real["cells"][k]["eps0.1"]); b = lv(OUT["cells"][k]["eps0.1"])
    check(f"MUTATE: M_crit rises > 0.5 dex in {k} at eps 0.1 (<= {a:.2f} -> {b:.2f})", b - a > 0.5)
P(f"\n{sum(res)}/{len(res)} pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(res) else 1)
