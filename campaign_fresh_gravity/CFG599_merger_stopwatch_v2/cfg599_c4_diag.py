#!/usr/bin/env python3
"""CFG599 C4(b) diagnosis (post-run, 2026-10-10; README D-2).  The isolated main failed C4(b): lensing-galaxy 18.17 kpc > 15.
No verdict is changed by this script and NO merger run is made (section 5: none before C4 passes).  Isolated halos only:
(a) the committed isolated-main run (alpha 1): offsets per epoch for the primary lensing peak and for each of the four frozen
    convergence-check variants, the galaxy and cold-energy peaks, M(<300 kpc);
(b) an isolated main at alpha = 0 (no drift, no OU; same seed) over 0.6 Gyr: does the outlier need the settling machinery?
(c) the alpha = 1 isolated main re-run to the failing epoch: the cold-energy map near the centre at 12.5-kpc pixels.
Run: nice -n 10 python3 cfg599_c4_diag.py  -> cfg599_c4_diag.out, cfg599_c4_diag_results.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg599_lib as L
import cfg599_sim as S

OUT = []; RES = {}
def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def offsets(diag, w="main"):
    rows = []
    for d in diag:
        m = d[w]; g = np.array(m["gal"])
        rows.append(dict(t=d["t"], lens=float(np.hypot(*(np.array(m["lens"]) - g))),
                         alts=[float(np.hypot(*(np.array(a) - g))) for a in m["lens_alts"]],
                         gas=float(np.hypot(*(np.array(m["gas"]) - g))), gal_r=float(np.hypot(*g)),
                         lens_r=float(np.hypot(*np.array(m["lens"]))), cold_r=float(np.hypot(*np.array(m["cold"]))), M300=m["M300"]))
    return rows


def summary(rows, label):
    s = dict(max_lens_gal=max(r["lens"] for r in rows), n_lens_over_15=sum(r["lens"] > 15 for r in rows),
             median_lens_gal=float(np.median([r["lens"] for r in rows])),
             max_alt_lens_gal=[max(r["alts"][k] for r in rows) for k in range(4)],
             max_gas_gal=max(r["gas"] for r in rows), max_gal_from_true=max(r["gal_r"] for r in rows),
             max_lens_from_true=max(r["lens_r"] for r in rows), max_cold_from_true=max(r["cold_r"] for r in rows),
             M300_drift=rows[-1]["M300"] / rows[0]["M300"] - 1, n=len(rows))
    P(f"{label}: " + json.dumps({k: (np.round(v, 2).tolist() if isinstance(v, (list, float)) else v) for k, v in s.items()}))
    return s


r1 = json.load(open(os.path.join(HERE, "runs", "iso_main_a1_can.json")))
rows1 = offsets(r1["diag"])
RES["a_alpha1"] = summary(rows1, "(a) committed isolated main, alpha 1 [alts = (R0,Rmin) (300,35) (300,75) (200,50) (400,50)]")
worst = max(rows1, key=lambda r: r["lens"])
RES["a_worst_epoch"] = worst
P(f"    worst epoch t = {worst['t']:.2f} Gyr: primary {worst['lens']:.1f} kpc; variants {np.round(worst['alts'], 1).tolist()} kpc; "
  f"galaxy {worst['gal_r']:.1f} kpc and lensing {worst['lens_r']:.1f} kpc from the true centre")

cfg0 = dict(foot="can", alpha=0.0, mode="isolated", iso_which="main", t_iso=0.6)
r0 = S.run(cfg0)
RES["b_alpha0"] = summary(offsets(r0["diag"]), "(b) isolated main, alpha 0 (no drift, no OU), same seed")

sim = S.Sim(dict(foot="can", alpha=1.0, mode="isolated", iso_which="main"))
next_d = S.DIAG_EVERY
while sim.t < worst["t"] - 1e-9:
    dt = min(L.hydro_dt(sim.U, sim.g.dx), 0.3 * sim.g.dx / np.abs(sim.v).max(), 0.005, next_d - sim.t + 1e-9)
    dt = max(dt, 1e-5)
    sim.step(dt)
    if sim.t >= next_d - 1e-9:
        next_d += S.DIAG_EVERY
d = sim.diagnose()["main"]
gas_k, st_k, tot, cold = sim.maps()
XX, YY = sim.XX, sim.YY
c = (np.abs(XX) <= 50) & (np.abs(YY) <= 50)
idx = np.argwhere(c)
i0, j0 = idx.min(0); i1, j1 = idx.max(0)
sub = cold[i0:i1 + 1, j0:j1 + 1]; subt = tot[i0:i1 + 1, j0:j1 + 1]
RES["c_rerun_epoch"] = dict(t=sim.t, primary_lens=d["lens"], galaxy=d["gal"], cold_peak=d["cold"],
                            reproduces_committed=bool(abs(np.hypot(*(np.array(d["lens"]) - np.array(d["gal"]))) - worst["lens"]) < 0.5),
                            cold_map_central_8x8_rel=(sub / sub.mean()).round(3).tolist(), tot_map_central_8x8_rel=(subt / subt.mean()).round(3).tolist(),
                            pixel_centres_x=XX[i0:i1 + 1, 0].tolist())
P(f"(c) alpha 1 re-run to t = {sim.t:.3f}: primary lens {np.round(d['lens'], 1).tolist()}, galaxy {np.round(d['gal'], 1).tolist()}, "
  f"cold peak {np.round(d['cold'], 1).tolist()} (reproduces the committed epoch: {RES['c_rerun_epoch']['reproduces_committed']})")
P("    central +-50 kpc cold-energy map / its mean (12.5-kpc pixels, rows = x):")
for row in (sub / sub.mean()):
    P("      " + " ".join(f"{v:5.2f}" for v in row))
P("READING: see README D-2.")
open(os.path.join(HERE, "cfg599_c4_diag.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg599_c4_diag_results.json"), "w"), indent=1, default=float)
