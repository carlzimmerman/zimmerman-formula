# POST-HOC (labelled): quantised f_hot (CFG61's README/script comment says the shift is a whole number of 0.05-dex nodes) -- I read only the
# comment line of the CFG61 code to diagnose the disagreement; no analysis code executed.
import math, numpy as np, cfg77_lib as L
dat = L.load_data("Color"); K = list(range(8, 15))
len_ = L.load_lenses(); grp = L.make_groups(len_)
late = L.stack(grp[0], L.law_profile(grp[0], "canonical"))
for f0 in (0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
    sh = int(round(math.log10(1 + f0) / 0.05)); fe = 10 ** (0.05 * sh) - 1
    e = L.stack(grp[1], L.law_profile(grp[1], "canonical", f_hot=fe))
    e2 = L.stack(grp[1], L.law_profile(grp[1], "canonical", f_hot=f0))
    print(f"f={f0}: quantised f_eff={fe:.3f} chi2={L.diff_stat(dat, K, late, e)[0]:.2f}   unquantised {L.diff_stat(dat, K, late, e2)[0]:.2f}", flush=True)
print("CFG61: 18.2, 10.0, 4.8, 4.1, 10.4, 26.9, 58.4")
