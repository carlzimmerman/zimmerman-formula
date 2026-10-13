#!/usr/bin/env python3
"""CFG712 SCORE (criteria d73d64603): reads Etherington+2022's gamma column for the first time and scores the sealed predictions.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, re, json, math, hashlib
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
for line in open(os.path.join(HERE, "cfg712_PREDICTIONS_HASH.txt")):
    h, f = line.split(); assert hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() == h, f"sealed file changed: {f}"
pred = json.load(open(os.path.join(HERE, "cfg712_predictions.json")))["lenses"]
stars = json.load(open(os.path.join(HERE, "cfg712_predictions_MUTATE.json")))["lenses"]
s = open(os.path.join(os.path.dirname(REPO), "_external_data", "etherington2022", "src", "6_Results.tex")).read()
i = s.find("label{table: SLACS mass"); blk = s[s.rfind("begin{table", 0, i):i]
obs = {}
for line in blk.splitlines():
    m = re.search(r"(J\d{4}[+-]\d{4})", line)
    if not m or "&" not in line: continue
    cells = line.split("&"); k = [j for j, c in enumerate(cells) if m.group(1) in c][0]
    g = re.findall(r"(\d+\.?\d*)\^\{(?:\\textrm\{)?\+?(\d+\.?\d*)\}?\}?_\{(?:\\textrm\{)?-?(\d+\.?\d*)", cells[k + 2]) or \
        re.findall(r"(\d+\.?\d*)\^\\textrm\{\+?(\d+\.?\d*)\}_\\textrm\{-?(\d+\.?\d*)\}", cells[k + 2])
    if g: obs[m.group(1)] = (float(g[0][0]), 0.5 * (float(g[0][1]) + float(g[0][2])))
names = sorted(set(obs) & set(pred))
OUT, RES = [], {"n": len(names)}
P = lambda x: (print(x), OUT.append(x))
go = np.array([obs[n][0] for n in names]); eo = np.array([obs[n][1] for n in names])
st = np.array([stars[n]["canonical"]["gamma_pred"] for n in names])
P(f"n = {len(names)}; observed median gamma {np.median(go):.3f} (16-84 {np.percentile(go,16):.2f}-{np.percentile(go,84):.2f}); stars-only median {np.median(st):.3f}")
m1 = np.median(st) - np.median([pred[n]["canonical"]["gamma_pred"] for n in names])
P(f"M1 tooth: stars-only minus law median = {m1:.3f} -> {'BITES (sensitive)' if m1 >= 0.15 else 'FAILS'}")
for foot in ("canonical", "alt"):
    gp = np.array([pred[n][foot]["gamma_pred"] for n in names]); d = gp - go
    rng = np.random.default_rng(712); bs = [np.median(rng.choice(d, d.size)) for _ in range(4000)]
    med, sm = float(np.median(d)), float(np.std(bs))
    rho, p = spearmanr(gp, go)
    T1 = "CONSISTENT" if abs(med) <= 0.10 else ("INCONSISTENT" if (abs(med) > 0.20 and abs(med) > 3 * sm) else "TENSION")
    T2 = "PREDICTIVE" if (rho > 0 and p < 0.01) else ("NOT PREDICTIVE" if (p >= 0.05 or rho <= 0) else "WEAK")
    chi = float(np.sqrt(np.mean((d / eo) ** 2)))
    RES[foot] = dict(median_delta=med, boot_sigma=sm, T1=T1, spearman_rho=float(rho), spearman_p=float(p), T2=T2,
                     rms_delta=float(np.sqrt(np.mean(d ** 2))), rms_obs_about_mean=float(np.std(go)), rms_norm=chi,
                     median_pred=float(np.median(gp)))
    P(f"{foot}: median gamma_pred - gamma_obs = {med:+.3f} +- {sm:.3f} -> {T1}; Spearman rho {rho:+.3f} p {p:.2e} -> {T2}; "
      f"rms(delta) {np.sqrt(np.mean(d**2)):.3f} vs obs scatter {np.std(go):.3f}; rms(delta/err) {chi:.2f}")
RES["M1_stars_minus_law"] = float(m1); RES["M1_bites"] = bool(m1 >= 0.15)
json.dump(RES, open(os.path.join(HERE, "cfg712_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg712.out"), "w").write("\n".join(OUT) + "\n")
