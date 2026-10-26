"""IB1 POST-RESULT diagnostic (labelled, NOT graded): HG's OUTER misses by MGAS500 tercile, split into the 106 KT clusters and
the 220 sigma-filled ones (canonical, h 0.672). kappa = 1/2 FITTED; not theory closed."""
import os, sys; HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
import numpy as np
exec(open(os.path.join(HERE, "ib1_hse_halo.py")).read().split("P(\"IB1 HG")[0])
foot, hk = "canonical", "h0672"; d = L.DAT[hk]; WB = d["W"] * d["B"][None, :]
n = WB * (d["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0]); VC = L.DC[(foot, hk)]; V, _ = vectors(foot, hk)
ob = NX["BANDS"]["OUTER"]; out = []
for t in range(3):
    for lab, m in (("KT", L.OKK), ("fill", ~L.OKK), ("all", np.ones(L.N, bool))):
        s = (L.T3M == t) & m; s[[i for i in range(L.N) if i not in set(int(x) for x in L.ALLI)]] = False
        A = n[s][:, ob].sum() / VC[s][:, ob].sum(); Ap = V[s][:, ob].sum() / VC[s][:, ob].sum()
        sk = np.sqrt(np.median([sig2(int(i)) for i in np.where(s)[0]])) / 1e3
        out.append(f"M{t+1} {lab:4s} n {s.sum():3d}  OUTER meas A {A:.3f}  HG pred {Ap:.3f}  pred/meas {Ap / A:.2f}  median sigma {sk:.0f} km/s")
for i in np.where(L.OKK)[0][:0]: pass
kt = np.where(L.OKK)[0]; fill_at_kt = None
out.append("sigma used: KT clusters kT-based; fill = OS1/X30 tercile fill (SIG_C)")
print("\n".join(out)); open(os.path.join(HERE, "ib1_post_outer.out"), "w").write("\n".join(out) + "\n")
