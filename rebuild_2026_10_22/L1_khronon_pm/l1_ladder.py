#!/usr/bin/env python3
"""L1_khronon_pm A5/A6 summary (reported only, never pooled; convergence, not a verdict): sigma8 vs S0, rho_NL per footing and rung,
DBI vs its LIN, nonconvergence audit, halo dust/baryon (satellite vs field).  Reads work/prod/*/result.json (no runs).
  python3 l1_ladder.py  -> l1_ladder.out, l1_ladder_results.json.  kappa = 1/2 FITTED; footings never pooled."""
import os, sys, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import khronon_pm as K
W = os.path.join(HERE, "work", "prod"); OUT = []; RES = {"lane": "L1_khronon_pm", "part": "A5_A6_summary"}
def P(s): print(s, flush=True); OUT.append(s)
R = {}
for f in glob.glob(os.path.join(W, "A[56]_*", "result.json")):
    r = json.load(open(f))
    if r.get("status") == "done": R[os.path.basename(os.path.dirname(f))] = r
def s8(t): return R[t]["snap"]["z0"]["sigma8"] if t in R else None
def audit(t):
    d = R[t]["diag"]; return dict(nonconv=sum(1 for q in d if "converged" in q and not q["converged"]), itmax=max([q.get("iters", 0) for q in d] or [0]),
                                  xmax=max([q.get("x_max", 0.0) for q in d] or [0.0]), sha=R[t].get("final_state_sha256"))
cells = {}
for N in (128, 256, 384):
    S0 = f"A5_S0_N{N}_zi199"; groups = [("ode", f"A5_LIN_N{N}_zi199", {"can": f"A5_KX_can_N{N}_zi199", "alt": f"A5_KX_alt_N{N}_zi199"})]
    if N == 384: groups.append(("lob", "A5_LIN_N384_zi199_LOB", {"can": "A5_KX_can_N384_zi199_LOB"}))
    for st in ("cap30", "P1"):
        groups.append((f"dbi_{st}", f"A6_LIN_dbi_{st}_N{N}_zi199", {"can": f"A6_KX_can_dbi_{st}_N{N}_zi199", "alt": f"A6_KX_alt_dbi_{st}_N{N}_zi199"}))
    for ic, lin, kxs in groups:
        if lin not in R or S0 not in R: continue
        row = dict(N=N, ic=ic, sigma8_S0=s8(S0), sigma8_LIN=s8(lin), LIN_over_S0=s8(lin) / s8(S0), kx={})
        for ft, kx in kxs.items():
            if kx not in R: continue
            a = audit(kx); rho = (s8(kx) - s8(lin)) / (s8(S0) - s8(lin))
            kl = R[kx]["snap"]["z0"]["k"]; pk = R[kx]["snap"]["z0"]["P"]; pl = R[lin]["snap"]["z0"]["P"]; ps = R[S0]["snap"]["z0"]["P"]
            rat = {str(kq): (min(range(len(kl)), key=lambda i: abs(kl[i] - kq))) for kq in (0.1, 0.3, 1.0, 3.0)}
            row["kx"][ft] = dict(sigma8=s8(kx), KX_over_LIN=s8(kx) / s8(lin), rho_NL=rho, reading=("restores most" if rho >= 0.5 else "partial" if rho >= 0.1 else
                                 "does not restore" if rho > -0.1 else "deepens the deficit"), sha_differs_from_LIN=a["sha"] != R[lin].get("final_state_sha256"),
                                 P_KX_over_LIN={kq: pk[i] / pl[i] for kq, i in rat.items() if kl[i] <= math.pi * N / 100}, P_KX_over_S0={kq: pk[i] / ps[i] for kq, i in rat.items() if kl[i] <= math.pi * N / 100}, **a)
        cells[f"{ic}_N{N}"] = row
        P(f"  N {N} {ic}: S0 {row['sigma8_S0']:.4f}, LIN {row['sigma8_LIN']:.4f} (LIN/S0 {row['LIN_over_S0']:.3f}); " + "; ".join(
            f"KX-{ft} {v['sigma8']:.4f} (KX/LIN {v['KX_over_LIN']:.3f}, rho_NL {v['rho_NL']:+.4f} -> {v['reading']}; nonconv {v['nonconv']}, it<= {v['itmax']}, x_max {v['xmax']:.3g})"
            for ft, v in row["kx"].items()))
RES["cells"] = cells
# halo report (A3/A6), z = 0
H = {}
for t, r in sorted(R.items()):
    h = r["snap"]["z0"].get("halos")
    if not h: continue
    H[t] = {c: {k: v.get(k) for k in ("n", "M1_Msun_median", "ratio_0p3_1_stacked", "ratio_1_3_stacked", "ratio_0p3_1_median")} for c, v in h["classes"].items()}
    H[t]["cosmic"] = h["cosmic_tau_over_b"]; H[t]["n_halos"] = h["n_halos"]
RES["halos"] = H
for t in sorted(H):
    if "N384" not in t and "N256" not in t: continue
    sel = {c: H[t][c] for c in ("cluster", "top50", "galaxy", "satellite_1_3Mpc", "field_gt3Mpc") if c in H[t]}
    P(f"  halos {t}: n {H[t]['n_halos']}; " + "; ".join(f"{c} n {v['n']}" + (f" tau/b(0.3-1) {v['ratio_0p3_1_stacked']:.2f}, (1-3) {v['ratio_1_3_stacked']:.2f}" if v.get("n") else "")
                                                     for c, v in sel.items()) + f"; cosmic {H[t]['cosmic']:.2f}")
K.atomic_json(os.path.join(HERE, "l1_ladder_results.json"), RES); K.atomic_text(os.path.join(HERE, "l1_ladder.out"), "\n".join(OUT) + "\n")
