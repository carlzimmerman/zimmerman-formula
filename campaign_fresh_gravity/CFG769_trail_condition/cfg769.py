#!/usr/bin/env python3
"""CFG769: what condition do the NGC 1052 debris lack? C-SIGMA kill test on SPARC + sealed C-A6 predictions.

Criteria: FROZEN_CRITERIA.md (committed alone, c7cf0c857). Seconds, < 200 MB, no downloads (inputs transcribed below from the
PDFs in _external_data/arxiv_cfg769, sha256 in the criteria).
CFG769_MUTATE=1: V_obs := Newtonian curve at Upsilon_d = 0.5; exit 1 iff no tested galaxy then requires the boost.
kappa = 1/2 FITTED; both footings, never pooled; the cold energy's mass is required; no particle species; not "theory closed".
"""
import hashlib, json, math, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG769_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg769{TAG}.out"), "w")
RES = {"lane": "CFG769", "criteria": "c7cf0c857", "mutate": MUT, "part1": {}, "part2": {}}
NU = np.vectorize(lambda y: C4.nu_mono(float(y)))
KPC_M = 3.0856775814913673e19
GK = 4.30091727e-6                       # kpc (km/s)^2 / Msun


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


P_(__doc__.strip())

# ============================================================================ Part 1: C-SIGMA on SPARC
SIG_CRIT = 18.4 * (1 - 0.23)
P_(f"\nPART 1  C-SIGMA: SPARC galaxies with lenient Sigma < {SIG_CRIT:.2f} Msun/pc^2 are predicted Newtonian")
gals = C4.load_sparc()
UPS = np.round(np.arange(0.10, 2.0001, 0.01), 2)
UPS5 = np.round(np.arange(0.10, 5.0001, 0.01), 2)
tested = []
for g in gals:
    m = g["meta"]
    if m is None or m["Q"] not in (1, 2) or m["Inc"] < 30 or len(g["R"]) < 5 or m["Reff"] <= 0:
        continue
    area = math.pi * (m["Reff"] * 1e3) ** 2                                   # pc^2
    s_star = 0.5 * 0.5 * m["L36"] * 1e9 / area
    s_len = (0.5 * 0.7 * m["L36"] + 0.5 * 1.33 * m["MHI"]) * 1e9 / area
    if s_len < SIG_CRIT:
        tested.append(dict(g=g, s_star=s_star, s_len=s_len))
P_(f"  sample Q<=2, Inc>=30, N>=5; tested (Sigma_len < {SIG_CRIT:.2f}): {len(tested)} galaxies")


def vbar2(g, U):
    return np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2


def chi2_min(g, Vobs, a0, law, grid):
    best = (math.inf, None)
    R = g["R"]
    for U in grid:
        vb2 = vbar2(g, U)
        if law:
            gN = np.abs(vb2) / R * 1e6 / KPC_M
            v2 = NU(np.maximum(gN, 1e-30) / a0) * vb2
        else:
            v2 = vb2
        v = np.sign(v2) * np.sqrt(np.abs(v2))
        c = float(np.sum(((Vobs - v) / g["eV"]) ** 2))
        if c < best[0]:
            best = (c, float(U))
    return best


verdict1 = {}
for foot in C4.FOOTS:
    a0 = C4.A0[foot]
    rows, n_req, n_req5 = [], 0, 0
    for t in tested:
        g = t["g"]
        Vobs = np.sqrt(np.maximum(vbar2(g, 0.5), 0.0)) if MUT else g["Vobs"]
        cN, uN = chi2_min(g, Vobs, a0, False, UPS)
        cL, uL = chi2_min(g, Vobs, a0, True, UPS)
        cN5, uN5 = chi2_min(g, Vobs, a0, False, UPS5)
        d, d5 = cN - cL, cN5 - cL
        n_req += d >= 25
        n_req5 += d5 >= 25
        rows.append(dict(name=g["name"], N=len(g["R"]), Sigma_star=t["s_star"], Sigma_len=t["s_len"], chi2_N=cN, U_N=uN,
                         chi2_law=cL, U_law=uL, Delta=d, chi2_N_U5=cN5, U_N5=uN5, Delta_U5=d5, requires=bool(d >= 25)))
    rows.sort(key=lambda r: -r["Delta"])
    v = "EXCLUDED" if n_req >= 10 else ("SURVIVES" if n_req == 0 else "TENSION")
    verdict1[foot] = v
    RES["part1"][foot] = dict(n_tested=len(rows), n_requires=int(n_req), n_requires_U5=int(n_req5), verdict=v, rows=rows)
    P_(f"\n  {foot}: {n_req}/{len(rows)} tested galaxies require the boost (Delta >= 25); Newton allowed Ups_d <= 5: {n_req5}  "
       f"-> {v}")
    for r in rows[:12]:
        P_(f"    {r['name']:12s} N {r['N']:3d}  Sigma* {r['Sigma_star']:6.2f}  Sigma_len {r['Sigma_len']:6.2f}  chi2 N {r['chi2_N']:9.1f} "
           f"(U {r['U_N']:.2f})  law {r['chi2_law']:8.1f} (U {r['U_law']:.2f})  Delta {r['Delta']:+9.1f}  [Ups<=5: {r['Delta_U5']:+8.1f}]")
    med = float(np.median([r["Delta"] for r in rows])) if rows else float("nan")
    P_(f"    ... median Delta {med:+.1f}; fewest: " + ", ".join(f"{r['name']} {r['Delta']:+.1f}" for r in rows[-3:]))

# ---- REPORTED (criteria: no verdict weight): the stars-only Sigma set (Sigma_* < SIG_CRIT, gas not counted)
stars_set = []
for g in gals:
    m = g["meta"]
    if m is None or m["Q"] not in (1, 2) or m["Inc"] < 30 or len(g["R"]) < 5 or m["Reff"] <= 0:
        continue
    s_star = 0.5 * 0.5 * m["L36"] * 1e9 / (math.pi * (m["Reff"] * 1e3) ** 2)
    if s_star < SIG_CRIT:
        stars_set.append((g, s_star))
for foot in C4.FOOTS:
    a0 = C4.A0[foot]
    ds = []
    for g, s_star in stars_set:
        Vobs = np.sqrt(np.maximum(vbar2(g, 0.5), 0.0)) if MUT else g["Vobs"]
        cN, _ = chi2_min(g, Vobs, a0, False, UPS)
        cL, _ = chi2_min(g, Vobs, a0, True, UPS)
        cN5, _ = chi2_min(g, Vobs, a0, False, UPS5)
        ds.append(dict(name=g["name"], Sigma_star=s_star, Delta=cN - cL, Delta_U5=cN5 - cL))
    nr = sum(d["Delta"] >= 25 for d in ds); nr5 = sum(d["Delta_U5"] >= 25 for d in ds)
    RES["part1"][foot]["REPORTED_stars_only"] = dict(n_tested=len(ds), n_requires=int(nr), n_requires_U5=int(nr5), rows=ds)
    P_(f"\n  REPORTED (no verdict weight) {foot}, stars-only Sigma_* < {SIG_CRIT:.2f}: {nr}/{len(ds)} require the boost "
       f"(Delta >= 25); Newton Ups_d <= 5: {nr5}/{len(ds)}; median Delta {float(np.median([d['Delta'] for d in ds])):+.1f}")

if MUT:
    bites = all(RES["part1"][f]["n_requires"] == 0 for f in C4.FOOTS)
    P_(f"\nMUTATE: V_obs := Newton(Ups 0.5) -> no tested galaxy requires the boost: {bites}")
    json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg769_results{TAG}.json"), "w"), indent=1)
    sys.exit(1 if bites else 0)

# ============================================================================ Part 2: sealed predictions (C-A6)
P_("\nPART 2a  SEALED: trail galaxies with no measured dispersion (Tang+25b Tables 1-2; CFG655 estimator, no EFE)")
TRAIL = {  # name: (log M*, R_e major arcsec, b/a, t_M Gyr, vD+22 label)
    "DF5 (RCP 11)": (7.15, 11.85, 0.782, 7.49, "E"),
    "DF7 (RCP 9)": (7.02, 14.66, 0.431, 6.73, "T"),
    "RCP 16": (6.97, 5.25, 0.543, 8.16, "E"),
    "RCP 21": (6.78, 8.91, 0.775, 6.48, "E"),
    "RCP 26": (7.40, 8.46, 0.632, 9.43, "E"),
    "RCP 28": (6.49, 6.15, 0.834, 6.61, "E"),
}
seal = {}
for name, (lm, re_as, ba, age, lab) in TRAIL.items():
    seal[name] = dict(logM=lm, Re_arcsec=re_as, b_a=ba, t_M=age, label=lab, pred={})
    for D in (17.7, 20.0, 21.7):
        rc = re_as * math.sqrt(ba) * D * 1e3 * math.pi / 648000.0      # kpc
        r = 4.0 / 3.0 * rc
        M = 10 ** lm
        gN = GK * 0.5 * M / r ** 2                                       # (km/s)^2/kpc
        sN = math.sqrt(gN * r / 3.0)
        for foot in C4.FOOTS:
            nu = C4.nu_mono(gN * 1e6 / KPC_M / C4.A0[foot])
            sL = math.sqrt(nu * gN * r / 3.0)
            seal[name]["pred"][f"{foot}@{D}"] = dict(r_half_kpc=r, sigma_N=sN, sigma_law=sL, nu=nu)
    p = seal[name]["pred"]
    P_(f"  {name:13s} [{lab}] logM {lm:.2f}  t_M {age:5.2f}  sigma_N {p['canonical@20.0']['sigma_N']:.2f} km/s (17.7-21.7 Mpc: "
       f"{p['canonical@17.7']['sigma_N']:.2f}-{p['canonical@21.7']['sigma_N']:.2f})   sigma_law can {p['canonical@20.0']['sigma_law']:.2f} "
       f"/ alt {p['alt@20.0']['sigma_law']:.2f}   C-A6 predicts {'sigma_N' if lab == 'E' else 'sigma_law'}")
seal_doc = dict(lane="CFG769", criteria="c7cf0c857", rule="C-A6 own supply: E (debris) -> sigma_N forever; T -> sigma_law",
                trail=seal,
                ngc5557_E1=dict(prediction="Newtonian circular speed band 16-24 km/s, NOT the law band 28-41 km/s (CFG441/763)",
                                age_Gyr=4))
blob = json.dumps(C4.jclean(seal_doc), indent=1, sort_keys=True)
open(os.path.join(HERE, "cfg769_SEALED_predictions.json"), "w").write(blob + "\n")
sha = hashlib.sha256((blob + "\n").encode()).hexdigest()
RES["part2"] = dict(sealed_file="cfg769_SEALED_predictions.json", sha256=sha)
P_("\nPART 2b  SEALED: NGC 5557-E1 (~4 Gyr old TDG) Newtonian band 16-24 km/s, not the law band 28-41 km/s")
P_(f"\nSEAL sha256(cfg769_SEALED_predictions.json) = {sha}")
for foot in C4.FOOTS:
    P_(f"VERDICT {foot}: Part 1 C-SIGMA {verdict1[foot]}; Part 2 C-A6 SEALED (not scoreable yet)")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg769_results{TAG}.json"), "w"), indent=1)
