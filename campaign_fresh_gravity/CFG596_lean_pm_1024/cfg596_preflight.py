#!/usr/bin/env python3
"""CFG596 PRE-FLIGHT (before any engine work or production): with CFG592's native machinery UNCHANGED (its support
cut f >= 0.9 inside [k_lo, k_hi = pi N / (4 L)], N_kept >= 10, and its MUTATE tooth NZ2: a 20% excess ramped
0.5 -> 1 h/Mpc injected into the S0 best-fit mock must give chi2_min >= 9), which (L, N) boxes could make the
framework-native shear test DIAGNOSTIC at all?

The S0 spectrum used for the support integrand and the tooth is a splice of existing S0 PM spectra
(CFG518 S0 L200 N512 for k < 0.5, CFG530 S0 L100 N512 above; z nodes from their JSONs), extended below the
first bin with the engines' own IC shape and above with the run's own slope, exactly as cfg592_native.node_P does.
A hypothetical box only changes [k_lo, k_hi]. k_lo = 1.27 x 2 pi / L (the first-bin-centre ratio of the L200 / L100 runs).

  nice -n 10 python3 cfg596_preflight.py -> cfg596_preflight.out, cfg596_preflight.json
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---- spliced S0 spectrum (both pieces are S0, same ICs family / engine constants)
rA = G["load_run"]("518_DCcan_512"); rB = G["load_run"]("530_LRcan_L100_N512")
kA, kB = rA["k"], rB["k"]
ks = np.r_[kA[kA < 0.5], kB[kB >= 0.5]]
nodes = {}
for z in (0.0, 0.5, 1.0):
    pA = rA["nodes"][z][1]; pB = rB["nodes"][z][1]
    # match B to A at k = 0.5 (removes any sample-variance offset between the two boxes)
    sc = np.exp(np.interp(math.log(0.5), np.log(kA), np.log(pA)) - np.interp(math.log(0.5), np.log(kB), np.log(pB)))
    ps = np.r_[pA[kA < 0.5], pB[kB >= 0.5] * sc]
    nodes[z] = (ps, ps)
ratio_lo = float(rA["k_lo"] / (2 * math.pi / rA["L"]))
P(f"CFG596 pre-flight: CFG592 native machinery unchanged; first-bin ratio k_lo/(2pi/L) = {ratio_lo:.3f} (from the L200 run)")

BOXES = [(200, 512), (100, 512), (400, 768), (400, 1024), (300, 1024), (250, 1024), (200, 1024), (400, 1536), (400, 2048), (150, 1024),
         (100, 1024), (100, 2048), (1600, 100000)]   # last = idealised 'everything resolved' reference (k 0.005-49), not a buildable box
RES = {}
for L, N in BOXES:
    k_lo = ratio_lo * 2 * math.pi / L; k_hi = math.pi * N / (4 * L)
    # spectrum on the spliced grid; out-of-grid parts follow node_P's own extension rule
    run = dict(k=ks, nodes=nodes, k_lo=max(k_lo, ks[0]), k_hi=min(k_hi, ks[-1]), B=np.ones_like(ks), name=f"L{L}_N{N}")
    run_true = dict(run, k_lo=k_lo, k_hi=k_hi)
    PS0 = G["Pmat"](run, "S0")
    row = {"L": L, "N": N, "k_lo": k_lo, "k_hi": k_hi}
    for sn, S in G["SURV"].items():
        f = G["support_mask"](S, run_true, PS0); keep = S["pubkeep"] & (f >= 0.9); D = G["subset"](S, keep)
        r = dict(N_kept=int(D["N"]), N_kept_f08=int((S["pubkeep"] & (f >= 0.8)).sum()))
        if D["N"] >= 10:
            s0 = G["fit"](S, D, PS0)
            mock = G["theory"](S, D, G["nuis_spec"](S, 1.0, True)[3](np.array(s0["x"])), G["Pmat"](run, "S0", inject=G["G_INJ"]), "PM")
            fm = G["fit"](S, D, PS0, data=mock); r["NZ2_chi2"] = fm["chi2"]; r["NZ2_bites"] = bool(fm["chi2"] >= 9)
        row[sn] = r
        P(f"  L {L:4d} N {N:5d}: k {k_lo:.3f}-{k_hi:.3f}  {sn}: N_kept {r['N_kept']:3d} (f>=0.8: {r['N_kept_f08']:3d})"
          + (f"; NZ2 tooth chi2 {r['NZ2_chi2']:.2f} -> {'bites' if r['NZ2_bites'] else 'FAILS'}" if "NZ2_chi2" in r else ""))
    RES[f"L{L}_N{N}"] = row
json.dump(dict(lane="CFG596 pre-flight", date="2026-10-10", boxes=RES), open(os.path.join(HERE, "cfg596_preflight.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg596_preflight.out"), "w").write("\n".join(OUT) + "\n")
