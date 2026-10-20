#!/usr/bin/env python3
"""W4-10 POST-HOC diagnostic (added after the frozen run; NO verdict weight): refit the early-type subsamples with the
CFG926 R5 IMF correction for early types (ATLAS3D dynamical M/L ~1.5x Chabrier = +0.176 dex, on top of CFG667's +0.123 dex),
i.e. g_bar x 10^0.299 for red and Sersic n>2 lenses only; discs (blue, n<2) unchanged. Same W4-06 estimator and window.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_10_one_kappa_lensing/w4_10_posthoc_imf.py > .../w4_10_posthoc_imf.out"""
import importlib.util, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("w4_06", os.path.join(REPO, "why_4_puzzle", "W4_06_lensing_kappa", "w4_06.py"))
w6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(w6)
SHIFT = math.log10(1.5) + 0.123
print(f"W4-10 POST HOC: early-type IMF correction g_bar x 10^{SHIFT:.3f} (CFG926 R5 + CFG667); no verdict weight")
out = {}
for name, f, c, bm, early in (("blue", "Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0, False),
                              ("red", "Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5, True),
                              ("n<2", "Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0, False),
                              ("n>2", "Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0, True)):
    gb, go, C = w6.load(f, c, bm)
    if early:
        gb = gb * 10 ** SHIFT
    r = w6.fit_kappa(gb, go, C, w6.W, w6.nu_s, w6.S["rho_DE"])
    out[name] = r
    print(f"  {name:5s} {'(IMF-corrected)' if early else '(unchanged)    '} kappa {r['kappa']:.3f} [{r['lo']:.3f}, {r['hi']:.3f}] n {r['n']}")
for a, b in (("blue", "red"), ("n<2", "n>2")):
    sa, sb = 0.5 * (out[a]["hi"] - out[a]["lo"]), 0.5 * (out[b]["hi"] - out[b]["lo"])
    z = (out[b]["kappa"] - out[a]["kappa"]) / math.hypot(sa, sb)
    print(f"  {b} vs {a}: z {z:+.2f}")
