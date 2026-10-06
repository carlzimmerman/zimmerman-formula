"""cm14: the cooling-window pattern -- does the cold fluid sit only where a host's gas cannot cool?
Frozen: cm14_FROZEN_CRITERIA.md (8c5d1ada2).  Scored: SPARC within-disc outer-residual jump above the cm12 step.
Run: python3 cm14_cooling_window.py | MUTATE=1 injects +0.10 dex into HOT galaxies (separate outputs; must give SUPPORTED)
"""
import os, sys, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "puzzle_32pi", "agents", "V_evidence_for_the_coefficient"))
from v_common import load_sparc
MUTATE = os.environ.get("MUTATE") == "1"; SLUG = "cm14_cooling_window" + ("_MUTATE" if MUTATE else "")
G, MSUN, KPC, MP, KB = 6.674e-11, 1.989e30, 3.0857e19, 1.6726e-27, 1.380649e-23
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
STEP = {"lower": 10**11.36, "upper": 10**11.62}
LOG, OUT, res = [], {"lane": "cm14", "frozen": "8c5d1ada2", "mutate": MUTATE}, []
rng = np.random.default_rng(14)


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok):
    res.append(bool(ok)); P(("PASS  " if ok else "FAIL  ") + n)


def nu(y):
    y = np.maximum(y, 1e-14); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def Tvir(Mb, a0):
    V = (G * Mb * MSUN * a0) ** 0.25; return MP * 0.6 * V**2 / (2 * KB), V / 1e3


gals = [g for g in load_sparc() if g.get("Q") is not None and g["Q"] <= 2]
check("C1 nu_mono -> 1 at y = 1e4 (to 1e-12) and nu ~ 1/sqrt(y) at y = 1e-6 (to 1e-3)",
      abs(nu(1e4) - 1) < 1e-12 and abs(nu(1e-6) * 1e-3 - 1) < 1e-3)
for foot, a0 in A0.items():
    rows = []
    for g in gals:
        R = g["Rm"]                      # load_sparc returns metres
        vb2 = (g["Vgas"] * np.abs(g["Vgas"]) + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2) * 1e6
        ok = vb2 > 0
        if ok.sum() < 3:
            continue
        gb = vb2[ok] / R[ok]; go = (g["Vobs"][ok] * 1e3)**2 / R[ok]
        d = float(np.median(np.log10(go[-3:] / (gb[-3:] * nu(gb[-3:] / a0)))))
        Mb = vb2[ok][-1] * R[ok][-1] / G / MSUN
        rows.append((g["name"], Mb, d))
    Mb = np.array([r[1] for r in rows]); D0 = np.array([r[2] for r in rows])
    OUT[foot] = {"N": len(rows)}
    for lab, cut in STEP.items():
        hot = Mb > cut; D = D0 + (0.10 * hot if MUTATE else 0.0)
        diff = float(np.median(D[hot]) - np.median(D[~hot])) if hot.sum() else float("nan")
        bs = []
        for _ in range(4000):
            i = rng.integers(0, len(D), len(D)); h = hot[i]
            if h.sum() and (~h).sum():
                bs.append(np.median(D[i][h]) - np.median(D[i][~h]))
        err = float(np.std(bs))
        T, V = Tvir(cut, a0)
        OUT[foot][lab] = {"N_hot": int(hot.sum()), "D": diff, "err": err, "z": diff / err if err else None,
                          "hot_names": [r[0] for r, h in zip(rows, hot) if h], "step_T": T, "step_V": V,
                          "median_mid": float(np.median(D[~hot])), "median_hot": float(np.median(D[hot])) if hot.sum() else None}
        P(f"  {foot:9s} step {lab} (M_b > {cut:.2e}, V {V:.0f} km/s, T {T:.2e} K): N_hot {hot.sum()} / {len(D)}; "
          f"median Delta MID {np.median(D[~hot]):+.3f}, HOT {np.median(D[hot]) if hot.sum() else float('nan'):+.3f}; D = {diff:+.3f} +- {err:.3f} ({diff/err:+.2f} sigma)")
    P(f"    HOT galaxies (lower step): {', '.join(OUT[foot]['lower']['hot_names'])}")
prim = [OUT[f]["lower"] for f in A0]
if any(p["N_hot"] < 5 for p in prim):
    verdict = "INCONCLUSIVE (N_hot < 5)"
elif all(p["D"] > 2 * p["err"] for p in prim):
    verdict = "SUPPORTED"
elif all(p["D"] + 2 * p["err"] < 0.05 for p in prim):
    verdict = "CONTRADICTED"
else:
    verdict = "INCONCLUSIVE"
OUT["verdict"] = verdict
P("\n  Population table (record, reported only; native T_vir from typical M_b, canonical):")
for name, mb, outcome in (("ultra-faints", 1e4, "need extra (+0.325 dex, 3.8 sigma)"), ("classical dSphs", 1e7, "pass B (no extra)"),
                          ("SPARC spirals", 1e10, "f <= 0.105"), ("Milky Way", 6e10, "0.14"), ("non-central ETGs", 1e11, "0.13 (fail bare law +0.098 dex)"),
                          ("massive HI discs", 2e11, "pass (-0.028 +- 0.066)"), ("super spirals", 5e11, "+0.164 dex (2.34 sigma)"),
                          ("groups", 3e12, "0.60 (centrals 0.64)"), ("X-COP clusters", 1e14, "0.576")):
    T, V = Tvir(mb, A0["canonical"])
    zone = "COLD (cannot cool)" if T < 1e4 else ("HOT (cannot cool)" if mb > STEP["lower"] else "MID (cools)")
    P(f"    {name:18s} M_b ~{mb:.0e}: V {V:4.0f} km/s, T {T:.1e} K -> {zone:20s} record: {outcome}")
P(f"\n{'MUTATE (+0.10 dex injected into HOT) ' if MUTATE else ''}VERDICT: {verdict}")
if MUTATE:
    check("MUTATE: the injection is recovered as SUPPORTED", verdict == "SUPPORTED")
P(f"\n{sum(res)}/{len(res)} pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(res) else 1)
