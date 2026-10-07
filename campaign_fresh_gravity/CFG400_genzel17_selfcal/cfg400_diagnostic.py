"""CFG400 POST-RUN diagnostic (labelled): per-galaxy best a0 scale (f and a0 both free per galaxy), chi2/N, and the outer slope of g_obs.
If galaxies disagree wildly or chi2/N >> 1 for every law, the single-law model is inadequate (falling curves / pressure / beam), not an a0(z) signal."""
import os, sys, math, numpy as np
sys.argv = [sys.argv[0]]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg400_test.py")).read().split("LF = np.linspace")[0]
exec(src)
LF = np.linspace(-3, 3, 601); SC = np.logspace(-2, 2, 161)
print("\nper galaxy (canonical, nu_mono): best a0 scale (vs local a0), its law equivalents, chi2/N at the best, and dlog g_obs/dlog R outer")
for g, d in data.items():
    gb = gbar_shape(d["R"], d["Rh"], d["bt"]); best = (1e99, None, None)
    for s in SC:
        a0 = A0["canonical"] * s
        for lf in LF:
            gn = gb * 10**lf * 1e11
            c = np.sum(((np.log10(d["gobs"]) - np.log10(C4.nu_mono(gn / a0) * gn)) / d["elog"]) ** 2)
            if c < best[0]: best = (c, s, lf)
    o = d["R"] > d["Rh"]
    slope = np.polyfit(np.log10(d["R"][o]), np.log10(d["gobs"][o]), 1)[0] if o.sum() >= 2 else float("nan")
    print(f"  {g:11s} z {d['z']:.2f}: best a0 x{best[1]:.2f} (DE law x{de(d['z']):.2f}, RIVAL x{E(d['z']):.2f}); chi2/N {best[0]/len(d['R']):.2f}; outer dlog g/dlog R {slope:+.2f} (deep MOND -1, Kepler -2)")
