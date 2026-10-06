#!/usr/bin/env python3
"""CFG367 -- black-hole superradiance vs the CFG288 wave-field mass window. Frozen: FROZEN_CRITERIA.md (822a6f3ff).
Data: bh_spins_reynolds2021.csv (Reynolds 2021 ARAA, arXiv 2011.08948, Tables 1-2, transcribed by position).
Run from the repo root or here; CFG367_MUTATE=1 sets all spins to 0 (separate outputs)."""
import os, csv, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG367_MUTATE", "0") == "1"; SLUG = "cfg367_superradiance" + ("_MUTATE" if MUTATE else "")
H_EV = 4.135667e-15; TSUN = 4.925491e-6; YR = 3.15576e7; ALPHA_K = 7.49e9
WIN = (2e-20, 37.0); FLOOR = 2e-19; NEF = 200.0; TAU = {"smbh": 4.5e7 * YR, "xrb": 1e6 * YR}
LOG, CH, OUT = [], [], {"lane": "CFG367", "frozen": "822a6f3ff", "mutate": MUTATE}


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


def rate(alpha, a, l):
    """Gamma in units c^3/(GM): Detweiler x2 (l=1 small-alpha -> a alpha^9/24). Returns 0 if not superradiant."""
    n = l + 1; rp = 1 + math.sqrt(max(1 - a * a, 0.0)); OH = a / (2 * rp)
    w = alpha * (1 - alpha**2 / (2 * n * n))
    if alpha >= l * OH or w <= 0 or w >= l * OH:   # bound-state approximation valid only for 0 < w, alpha < l Omega_H (fix 1, disclosed)
        return 0.0
    C = 2**(4 * l + 1) * math.factorial(n + l) / (n**(2 * l + 4) * math.factorial(n - l - 1)) * (math.factorial(l) / (math.factorial(2 * l) * math.factorial(2 * l + 1)))**2
    g = 1.0
    for j in range(1, l + 1):
        g *= j * j * (1 - a * a) + (a * l - 2 * rp * w)**2
    return 2 * 2 * rp * C * g * (l * OH - w) * alpha**(4 * l + 5)


def excluded(m, M, a, tau):
    alpha = ALPHA_K * M * m; tunit = TSUN * M
    return any(rate(alpha, a, l) / tunit * tau >= NEF for l in (1, 2, 3))


a_t, al_t = 0.5, 1e-4   # fix 2 (disclosed): alpha = 0.01 is not << Omega_H(0.5) = 0.134
check("C1 l=1 small alpha -> a alpha^9/24 (1%)", abs(rate(al_t, a_t, 1) / (a_t * al_t**9 / 24) - 1) < 0.01, f"ratio {rate(al_t, a_t, 1) / (a_t * al_t**9 / 24):.4f}")
check("C2 a = 0 gives no superradiance", all(rate(x, 0.0, l) == 0.0 for x in (0.01, 0.1, 0.4) for l in (1, 2, 3)))

rows = list(csv.DictReader(open(os.path.join(HERE, "bh_spins_reynolds2021.csv"))))
mg = np.logspace(math.log10(WIN[0]) - 1, math.log10(WIN[1]), 1400)


def mass_range(r):
    if r["set"] == "xrb":
        return 5.0, 20.0
    c = float(r["mass_1e6"]) * 1e6
    if r["approx"] == "1":
        return 0.5 * c, 1.5 * c
    lo, hi = float(r["err_lo"]) * 1e6, float(r["err_hi"]) * 1e6
    return max(c - 2 * lo, 0.3 * c), c + 2 * hi


def intervals(mask):
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]:
                j += 1
            out.append((float(mg[i]), float(mg[j]))); i = j + 1
        else:
            i += 1
    return out


def band(f):
    if f < 1e-7: return "PTA (nHz)"
    if f < 1e-4: return "uHz gap (no running detector)"
    if f < 1e-1: return "LISA"
    if f < 10: return "deci-Hz gap (DECIGO-class)"
    if f < 1e3: return "LIGO/Virgo/KAGRA"
    return "above ground-based band"


union = {"smbh": np.zeros(len(mg), bool), "xrb": np.zeros(len(mg), bool)}
per = {}
for r in rows:
    a = 0.0 if MUTATE else max(float(r["spin_lo"]), 0.0)
    lo, hi = mass_range(r); Ms = np.logspace(math.log10(lo), math.log10(hi), 9)
    mask = np.array([all(excluded(m, M, a, TAU[r["set"]]) for M in Ms) for m in mg])
    union[r["set"]] |= mask; per[r["name"]] = intervals(mask)
for s, lab in (("smbh", "PRIMARY (SMBH, Table 1)"), ("xrb", "SECONDARY (X-ray binaries, PROVISIONAL-MASS 5-20 Msun)")):
    iv = intervals(union[s]); OUT[s] = iv
    P(f"\n{lab}: excluded m intervals (eV): " + ("; ".join(f"[{x:.2e}, {y:.2e}]" for x, y in iv) or "none"))
inwin = (mg >= WIN[0]) & (mg <= WIN[1])
for key, mask in (("primary", union["smbh"]), ("primary+secondary", union["smbh"] | union["xrb"])):
    surv = intervals(inwin & ~mask)
    OUT[key] = {"excluded_in_window": intervals(inwin & mask), "surviving": surv,
                "verdict": "NARROWS" if (inwin & mask).any() else "NO CONSTRAINT"}
    P(f"\n{key}: VERDICT {OUT[key]['verdict']}; surviving window pieces:")
    for x, y in surv:
        P(f"   [{x:.2e}, {y:.2e}] eV: f = {x / H_EV:.2e} .. {y / H_EV:.2e} Hz; f_GW = {2 * x / H_EV:.2e} ({band(2 * x / H_EV)}) .. {2 * y / H_EV:.2e} Hz ({band(2 * y / H_EV)})")
P(f"\n  record floor L383 = {FLOOR:.0e} eV: excluded by primary? {bool(np.interp(math.log10(FLOOR), np.log10(mg), union['smbh'].astype(float)) > 0.5)}")
OUT["per_object"] = per
if MUTATE:
    check("MUTATE: spins 0 -> union empty", not (union["smbh"] | union["xrb"]).any())
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
