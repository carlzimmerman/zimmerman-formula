#!/usr/bin/env python3
"""HY1 grader (FROZEN_CRITERIA.md 2fbb41123a, section 5): assembles parts/*.json into hy1.json / hy1.out (labels) and
hy1_MUTATE.json / hy1_MUTATE.out (M1 kappa -> 0, M3 f -> 2R). No new physics here; reads only the parts and pgrep.
kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing."""
import os, json, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.join(HERE, "parts")
FOOTS = ("canonical", "alt")
J = {k: json.load(open(os.path.join(PARTS, f"{k}.json"))) for k in ("sparc", "sparc_M3", "battery", "battery_M3", "kids")}
OUT, MOUT = [], []
def P(s="", m=False): print(s, flush=True); (MOUT if m else OUT).append(str(s))
MU_STAR = {"canonical": 8.890e6, "alt": 8.889e6}                     # KD1 mu* (Mpc^-1)
CHI2_LINE, GFO_LINE = 18.48, 0.162
cmb3 = subprocess.run(["pgrep", "-f", "cmb3.py"], capture_output=True, text=True).stdout.split()

RES = dict(lane="HY1", criteria="2fbb41123a", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
MUT = dict(lane="HY1 MUTATE (M1 kappa -> 0, M3 f -> 2R)", criteria="2fbb41123a", footings={})
P("HY1: the a0 law with kappa free plus the universal cold component at F1A's f (KD1 model P, mu*: central point mass).")
P("Criteria 2fbb41123a. Footings never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P("HY1 MUTATE: M1 (kappa -> 0, pure component) and M3 (f -> 2R at fixed kappa).", True)

for f in FOOTS:
    S, B, K = J["sparc"][f], J["battery"][f], J["kids"][f]
    ka = dict(KA1=B["KA"]["KA1"]["pass_"], KA2=S["KA2"]["pass_"], KA3=B["KA"]["KA3"]["pass_"], KA4=K["KA4"]["pass_"],
              KA5=B["KA"]["KA5"]["pass_"], KA6=B["KA"]["KA6"]["pass_"], KA7=B["KA"]["KA7"]["pass_"])
    F = dict(KA=ka); RES["footings"][f] = F
    P(f"\n================ [{f}]")
    P(f"[{f}] KA (M2 f -> 0 included): " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in ka.items()))
    if not all(ka.values()):
        F["label"] = "NO VERDICT (KA FAIL)"; P(f"[{f}] LABEL: {F['label']}"); continue
    kg = [r["kappa"] for r in S["grid"]]
    st = {"C1": [r["status"] for r in S["grid"]], "C2": [r["status"] for r in B["C2"]], "C3a": [r["status"] for r in B["C3a"]],
          "C4": [r["status"] for r in K["grid"]], "C5": [r["status"] for r in B["C5"]]}
    W = {c: [k for k, s in zip(kg, v) if s == "PASS"] for c, v in st.items()}
    # M1: C1 at kappa 0 must FAIL
    m1 = st["C1"][kg.index(0.0)] == "FAIL"
    # M3: opposite-direction rms moves beyond resolution at one or more grid kappas
    rows3 = []
    for a, b in zip(J["sparc_M3"][f], J["battery_M3"][f]):
        assert a["kappa"] == b["kappa"]
        opp = (a["dS"] > 0) != (b["dX"] > 0); res = abs(a["dS"]) > 0.010 and abs(b["dX"]) > 0.020
        rows3.append(dict(kappa=a["kappa"], dS=a["dS"], dX=b["dX"], opposite=opp, beyond_resolution=res, bites=bool(opp and res)))
    m3 = any(r["bites"] for r in rows3)
    c3a_power = not (B["C3a"][kg.index(0.5)]["law_only_step"][0] >= B["UA1_ci95"][0] and B["C3a"][kg.index(0.5)]["law_only_step"][0] <= B["UA1_ci95"][1]) and B["UA1_ci95"][0] < B["UA1_ci95"][1]
    power = {"C1": bool(m1 and m3), "C2": bool(m3), "C3a": bool(c3a_power), "C4": bool(K["power"]), "C5": True}
    MUT["footings"][f] = dict(M1=dict(C1_at_kappa0=st["C1"][kg.index(0.0)], C1_rms=S["grid"][0]["rms"], C1_U=S["grid"][0]["U_median"],
                                      C2_at_kappa0=st["C2"][0], C4_at_kappa0=st["C4"][0], bites=bool(m1),
                                      fried_chicken="not a known answer for this profile (NFW/coreNFW + feedback, simulation-shaped; not importable); stated"),
                              M3=dict(rows=rows3, bites=bool(m3)))
    P(f"[{f}] M1 kappa 0 (pure component): C1 {st['C1'][0]} (rms {S['grid'][0]['rms']:.4f}, U {S['grid'][0]['U_median']:.2f}), C2 {st['C2'][0]}, C4 {st['C4'][0]} -> {'BITES' if m1 else 'DOES NOT BITE'}", True)
    P(f"[{f}] M3 f -> 2R: dS (C1 rms) / dX (C2 rms) per kappa: " + "; ".join(f"{r['kappa']:g}: {r['dS']:+.3f}/{r['dX']:+.3f}{' *' if r['bites'] else ''}" for r in rows3), True)
    P(f"[{f}] M3: {'BITES' if m3 else 'DOES NOT BITE (same direction at every kappa: more dust worsens both columns)'}", True)
    common = sorted(set(kg).intersection(*[set(W[c]) for c in W if power[c]]))
    kill_reading = sorted(set(W["C1"]) & set(W["C2"]))
    # C6: kappa 0 replays (graded), kappa > 0 conditional
    c6a = dict(cmb_lensing_chi2=B["KA"]["KA7"]["G9a_chi2"], cmb_pass=B["KA"]["KA7"]["G9a_chi2"] <= CHI2_LINE, fsigma8_Rf=1.0,
               forest_lambda_J_Mpc=math.pi / MU_STAR[f], forest_pass=math.pi / MU_STAR[f] <= GFO_LINE)
    c6a["status"] = "PASS" if (c6a["cmb_pass"] and c6a["forest_pass"]) else "FAIL"
    cond = bool(common)
    c3b = ("NOT EVALUABLE (the only on-disk Bullet machinery, DB1/UX6 via NA2's child, peaks at 1.19 GB (NA2) / 1.48 GB (CE2), above the 1 GB line; not run)"
           if cond else "NOT RUN (common window empty)")
    c6b = (("NOT EVALUABLE (python3 cmb3.py running: pids " + ",".join(cmb3) + ")") if cmb3 else "NOT EVALUABLE (WG2 engine not adapted in this lane)") if cond else "NOT RUN (common window empty)"
    # PASS needs every column, C3b and C6 included, to PASS with power at one kappa; C3b/C6b are never PASS in this lane
    label = "FAIL" if not common else "NO VERDICT"
    F.update(kappa_grid=kg, status=st, windows=W, power=power, common_window=common, kill_reading_C1_and_C2=kill_reading,
             C6a=c6a, C3b=c3b, C6b=c6b, M1_bites=bool(m1), M3_bites=bool(m3), label=label,
             edges=dict(C1=S["edges"], C2=B["C2_edges"], C3a=B["C3a_edges"], C4=K["edges"], C5=B["C5_edges"]),
             eps_max={r["kappa"]: r["eps_max"] for r in S["grid"]}, F_X={r["kappa"]: r["F_X"] for r in B["C2"]})
    def wtxt(w): return "empty" if not w else f"{{{', '.join(f'{k:g}' for k in w)}}} = [{min(w):g}, {max(w):g}]"
    for c in st:
        P(f"[{f}] {c:4s} power {'YES' if power[c] else 'NO POWER'}; window {wtxt(W[c])}")
    P(f"[{f}] C3b {c3b}")
    P(f"[{f}] C6a kappa 0: CMB lensing chi2 {c6a['cmb_lensing_chi2']:.3f} (<= {CHI2_LINE}), fsigma8 Rf 1 (CE2 convention, no independent power), forest lambda_J {c6a['forest_lambda_J_Mpc']:.2e} Mpc (<= {GFO_LINE}) -> {c6a['status']}")
    P(f"[{f}] C6b kappa > 0: {c6b}")
    P(f"[{f}] common window (columns with power): {wtxt(common)}")
    P(f"[{f}] brief's kill reading W_SPARC ∩ W_X-COP: {wtxt(kill_reading)}")
    P(f"[{f}] LABEL: {label}")
RES["peak_rss_GB"] = {k: J[k].get("peak_rss_GB") for k in ("sparc", "battery", "kids")}
RES["cmb3_running_at_grade"] = bool(cmb3)
P("\nAdopts nothing. kappa = 1/2 FITTED; not theory closed."); P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.", True)
json.dump(RES, open(os.path.join(HERE, "hy1.json"), "w"), indent=1)
json.dump(MUT, open(os.path.join(HERE, "hy1_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "hy1.out"), "w").write("\n".join(OUT) + "\n")
open(os.path.join(HERE, "hy1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
