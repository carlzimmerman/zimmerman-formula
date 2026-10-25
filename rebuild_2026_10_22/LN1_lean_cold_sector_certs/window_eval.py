"""Evaluate T8 (sidm_window) at stated premise values. The premises are SCENARIOS, not measurements, except Q (cluster
core requirement), which comes from X39 (~2x) and X40b's (C) (3-5x). Output: window_eval.out."""
import math
rows = []
for F, Rg, lab_g in ((2.0, 8.0, 'galaxies flat within x2 over sigma x8'), (1.5, 8.0, 'within x1.5 over x8'), (2.0, 5.0, 'within x2 over x5')):
    for Rc, tau, lab_c in ((10.0, 0.4, 'sigma_cl/sigma_gal <= 10, clusters >= 0.4 of galaxy age'), (7.0, 0.5, '<= 7, >= 0.5 age')):
        for Q in (2.0, 3.0, 4.0, 5.0):
            lo = (math.log(Q) + 0.5 * math.log(tau)) / math.log(Rc); hi = math.log(F) / math.log(Rg)
            rows.append(f"F {F:3.1f} Rg {Rg:3.0f} | Rc {Rc:4.0f} tau {tau:3.1f} | Q {Q:3.1f} : q in [{lo:+.3f}, {hi:+.3f}] "
                        + (f"OPEN  (n = 2q-1 in [{2*lo-1:+.2f}, {2*hi-1:+.2f}])" if lo <= hi else "EMPTY"))
open('window_eval.out', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
