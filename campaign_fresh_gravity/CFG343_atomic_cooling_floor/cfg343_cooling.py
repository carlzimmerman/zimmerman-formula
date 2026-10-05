#!/usr/bin/env python3
"""CFG343 -- UFD cold mass from the atomic-cooling collapse threshold, read against CFG317's committed s(log R), z(log R).
Frozen: FROZEN_CRITERIA.md (dc000e9ce).  Run from the repository root; CFG343_MUTATE=1 uses T_vir = 1e3 K (separate outputs)."""
import os, csv, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("CFG343_MUTATE", "0") == "1"; SLUG = "cfg343_cooling" + ("_MUTATE" if MUTATE else "")
TVIR = 1e3 if MUTATE else 1e4
H, OM, FB = 0.674, 0.315, 0.157126
LOG, CH, OUT = [], [], {"lane": "CFG343", "frozen": "dc000e9ce", "mutate": MUTATE, "T_vir": TVIR, "checks": {}}


def P(s=""):
    print(s); LOG.append(s)


def check(n, v, ok):
    CH.append(bool(ok)); OUT["checks"][n] = {"ok": bool(ok), "measured": str(v)}; P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")


def m_cool(z, T=TVIR, mu=1.22, om_ratio=None):
    omr = (OM if om_ratio is None else om_ratio)  # Omega_m / Omega_m^z with Omega_m^z ~ 1 at z >= 6
    return 1.0e8 / H * (mu / 0.6) ** -1.5 * omr ** -0.5 * (T / 1.98e4) ** 1.5 * ((1 + z) / 10.0) ** -1.5


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


c1 = m_cool(9.0, T=1.98e4, mu=0.6, om_ratio=1.0) * H
check("C1 normalisation: 1e8 h^-1 Msun at T 1.98e4 K, mu 0.6, z 9 (Omega ratio 1)", f"{c1:.4e} h^-1 Msun", abs(c1 / 1e8 - 1) < 1e-9)

N317 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json")))["numbers"]
names = N317["NAMES"]["ufd"]; grid = np.array(N317["grid_logR"])
LV = {}
for r in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))):
    MV = fnum(r["M_V"])
    if MV is not None:
        LV[r["name"]] = 10 ** (0.4 * (4.83 - MV))
Mb = np.array([2.0 * LV[n] for n in names if n in LV])
P(f"CFG343: T_vir = {TVIR:.0e} K; {len(Mb)} of {len(names)} CFG317 UFDs matched; median M_b {np.median(Mb):.3e} Msun")
cls_Mb = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))):
    MV = fnum(r["M_V"])
    if MV is not None and MV <= -7.7:
        cls_Mb.append(2.0 * 10 ** (0.4 * (4.83 - MV)))
for zf in (6.0, 8.0, 10.0):
    Mc = m_cool(zf); R = np.maximum(1.0, FB * Mc / Mb); lr = float(np.median(np.log10(R)))
    rc = np.maximum(1.0, FB * Mc / np.array(cls_Mb))
    row = {"M_cool": Mc, "median_logR_cool": lr, "frac_R_gt1": float(np.mean(R > 1)), "classical_median_logR": float(np.median(np.log10(rc)))}
    P(f"\n  z_f {zf:.0f}: M_cool = {Mc:.3e} Msun; median log R_cool = {lr:.3f} (R = {10**lr:.0f}); classicals median log R_cool = {row['classical_median_logR']:.2f}")
    for prof in ("nfw", "sis"):
        for foot in ("canonical", "alt"):
            e = N317["NEED"][f"{prof}|{foot}|P1"]
            s = float(np.interp(lr, grid, e["s"])); z = float(np.interp(lr, grid, e["z"]))
            row[f"{prof}|{foot}"] = {"s": s, "z": z, "logR_need": e["lr0"], "factor_short": 10 ** (e["lr0"] - lr)}
            P(f"    {prof:3s} {foot:9s}: UFD offset at that R = {s:+.3f} dex (z {z:+.2f}); log R_need {e['lr0']:.2f} -> short by x{10 ** (e['lr0'] - lr):.1f}")
    OUT[f"zf{zf:.0f}"] = row

prim = OUT["zf8"]
resolves = all(abs(prim[f"{p}|{f}"]["z"]) < 2 for p in ("nfw", "sis") for f in ("canonical", "alt"))
brack = any(all(abs(OUT[k][f"{p}|{f}"]["z"]) < 2 for f in ("canonical", "alt")) for k in ("zf6", "zf8", "zf10") for p in ("nfw", "sis"))
verdict = "RESOLVES" if resolves else ("PARTIAL" if brack else "NOT")
check("C2 classical dwarfs: R_cool = 1 (no change), median log R_cool <= 0", OUT["zf8"]["classical_median_logR"], OUT["zf8"]["classical_median_logR"] <= 0.0)
P(f"\n{'MUTATE (T_vir 1e3 K) ' if MUTATE else ''}VERDICT: {verdict}"); OUT["verdict"] = verdict
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cfg343_cooling_results.json")))
    check("MUTATE: result changes with T_vir = 1e3 K", f"{real['zf8']['median_logR_cool']:.3f} -> {OUT['zf8']['median_logR_cool']:.3f}",
          abs(real["zf8"]["median_logR_cool"] - OUT["zf8"]["median_logR_cool"]) > 0.1)
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
