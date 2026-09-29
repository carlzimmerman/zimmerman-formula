"""Selection-bias mock: truth = flat-a0 law on each galaxy's tabulated (Mbar,R); observed Mbar scattered by 0.2 dex and V by sV;
select on OBSERVED g_bar/a0 < cut (as the counting does); report mean Delta_flat in the selected set. Expect >0 (selection on noisy mass)."""
import runpy, numpy as np, math, io, contextlib, sys
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ns = runpy.run_path("feas.py")
res = ns["res"]; g_disc = ns["g_disc"]; gpred = ns["gpred"]; A0 = ns["A0"]["can"]; KPC = ns["KPC"]; LN10 = math.log(10)
rng = np.random.default_rng(7)
for ds in ["RC100", "KMOS3D", "MSA-3D stars+gas", "MSA-3D stars", "KROSS stars+gas", "MUSE-DARK II"]:
    S = [o for o in res if o["ds"] == ds]
    M = np.array([o["Mbar"] for o in S]); R = np.array([o["r"] for o in S]); Re = np.array([o["Re"] for o in S]); sV = np.array([o["sV"] for o in S])
    gt = g_disc(M, R, Re); gtrue = gpred(gt, A0)
    out = {1.0: [], 0.3: []}; nsel = {1.0: [], 0.3: []}
    for k in range(300):
        Mo = M * 10 ** rng.normal(0, 0.2, len(M))
        go = gtrue * 10 ** (2 * rng.normal(0, sV / LN10))   # V scatter
        gbo = g_disc(Mo, R, Re); Df = np.log10(go / gpred(gbo, A0))
        for c in out:
            m = gbo / A0 < c
            if m.sum(): out[c].append(Df[m].mean()); nsel[c].append(m.sum())
    print(f"{ds:20} selected y_obs<1: n~{np.mean(nsel[1.0]):5.1f} mean Df bias {np.mean(out[1.0]):+.3f} | y_obs<0.3: n~{np.mean(nsel[0.3]):5.1f} mean Df bias {np.mean(out[0.3]):+.3f}")
