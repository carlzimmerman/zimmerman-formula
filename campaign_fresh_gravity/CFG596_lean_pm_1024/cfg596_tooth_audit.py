#!/usr/bin/env python3
"""CFG596 TOOTH AUDIT (follows cfg596_preflight.py; no verdict role of its own): why CFG592's frozen native tooth NZ2
(20% excess ramped over k 0.5 -> 1 h/Mpc, injected into the S0 best-fit mock; S0 refit must reach chi2_min >= 9)
fails even when every published point is resolved, and how large an excess the measured data CAN detect.

Same spliced S0 spectrum and CFG592 machinery as the pre-flight (exec'd unchanged). Boxes: the idealised
'everything resolved' reference (k 0.005-49), L400 N1024 (the planned production), L150 N1024 and L100 N1024.
  (a) frozen NZ2 (IA marginalised), (b) the same with IA fixed to 0 in both mock and fit,
  (c) excess amplitude needed for chi2_min = 9 (same ramp shape; bisection on the amplitude),
  (d) the framework's OWN measured boost B = P_grav / P_part (CFG530 L100 N512, canonical and alt, z = 0, held) injected instead.
  nice -n 10 python3 cfg596_tooth_audit.py -> cfg596_tooth_audit.out / .json
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

rA = G["load_run"]("518_DCcan_512"); rB = G["load_run"]("530_LRcan_L100_N512"); rBa = G["load_run"]("530_LRalt_L100_N512")
kA, kB = rA["k"], rB["k"]; ks = np.r_[kA[kA < 0.5], kB[kB >= 0.5]]
nodes = {}
for z in (0.0, 0.5, 1.0):
    pA = rA["nodes"][z][1]; pB = rB["nodes"][z][1]
    sc = np.exp(np.interp(math.log(0.5), np.log(kA), np.log(pA)) - np.interp(math.log(0.5), np.log(kB), np.log(pB)))
    ps = np.r_[pA[kA < 0.5], pB[kB >= 0.5] * sc]; nodes[z] = (ps, ps)
ratio_lo = float(rA["k_lo"] / (2 * math.pi / rA["L"]))
def Binj(run_src):
    lk = np.log(run_src["k"]); lb = np.log(run_src["B"]); klo, khi = run_src["k"][0], run_src["k"][-1]
    return lambda KK: np.exp(np.interp(np.log(np.clip(KK, klo, khi)), lk, lb))   # boost held flat outside its own k range
def ramp(amp): return lambda KK: 1 + amp * np.clip(np.log(np.clip(KK, 1e-9, None) / 0.5) / math.log(2.0), 0, 1)

BOXES = [(1600, 100000), (400, 1024), (150, 1024), (100, 1024)]
RES = {}
for L, N in BOXES:
    k_lo = ratio_lo * 2 * math.pi / L; k_hi = math.pi * N / (4 * L)
    run = dict(k=ks, nodes=nodes, k_lo=max(k_lo, ks[0]), k_hi=min(k_hi, ks[-1]), B=np.ones_like(ks))
    PS0 = G["Pmat"](run, "S0"); row = dict(L=L, N=N, k_lo=k_lo, k_hi=k_hi)
    for sn, S in G["SURV"].items():
        f = G["support_mask"](S, dict(run, k_lo=k_lo, k_hi=k_hi), PS0); D = G["subset"](S, S["pubkeep"] & (f >= 0.9))
        r = dict(N_kept=D["N"])
        if D["N"] < 10:
            row[sn] = r; P(f"  L {L} N {N} {sn}: N_kept {D['N']} -> no tooth possible"); continue
        def tooth(inj, ia=True):
            s0 = G["fit"](S, D, PS0, ia=ia); par = G["nuis_spec"](S, 1.0, ia)[3](np.array(s0["x"]))
            mock = G["theory"](S, D, par, G["Pmat"](run, "S0", inject=inj), "PM")
            return G["fit"](S, D, PS0, ia=ia, data=mock)["chi2"]
        r["a_frozen_NZ2"] = tooth(G["G_INJ"]); r["b_noIA"] = tooth(G["G_INJ"], ia=False)
        lo, hi = 0.2, 3.0
        if tooth(ramp(hi)) < 9: r["c_amp_for_chi2_9"] = f"> {hi}"
        else:
            for _ in range(14):
                mid = 0.5 * (lo + hi)
                if tooth(ramp(mid)) >= 9: hi = mid
                else: lo = mid
            r["c_amp_for_chi2_9"] = hi
        r["d_own_boost_can"] = tooth(Binj(rB)); r["d_own_boost_alt"] = tooth(Binj(rBa))
        r["d_own_boost_can_noIA"] = tooth(Binj(rB), ia=False)
        row[sn] = r; amp_s = r['c_amp_for_chi2_9'] if isinstance(r['c_amp_for_chi2_9'], str) else f"{r['c_amp_for_chi2_9']:.3f}"
        P(f"  L {L} N {N} (k {k_lo:.3f}-{k_hi:.3f}) {sn}: N_kept {D['N']}; (a) frozen NZ2 chi2 {r['a_frozen_NZ2']:.2f}; (b) no IA {r['b_noIA']:.2f}; "
          f"(c) ramp amplitude for chi2 = 9: {amp_s}; "
          f"(d) own boost injected: can {r['d_own_boost_can']:.2f}, alt {r['d_own_boost_alt']:.2f} (can, no IA {r['d_own_boost_can_noIA']:.2f})")
    RES[f"L{L}_N{N}"] = row
json.dump(dict(lane="CFG596 tooth audit", date="2026-10-10", boxes=RES), open(os.path.join(HERE, "cfg596_tooth_audit.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg596_tooth_audit.out"), "w").write("\n".join(OUT) + "\n")
