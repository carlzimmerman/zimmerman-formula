# POST-HOC (labelled): the CFG61 script comment says its hot-gas ladder shifts the M_* NODE by whole 0.05-dex steps (so the true baryon mass
# is M*(+shift)(1+f_cold(M*+shift)), not M_gal(1+f)).  Test that reading with my own implementation.
import math, numpy as np, cfg77_lib as L
dat = L.load_data("Color"); K = list(range(8, 15))
len_ = L.load_lenses(); grp = L.make_groups(len_); a0 = L.A0["canonical"]
late = L.stack(grp[0], L.law_profile(grp[0], "canonical"))
lm_all = len_["logM"]; fc_all = len_["Mgal"] / 10 ** lm_all - 1
bins = np.arange(7.0, 11.6, 0.05); ib = np.digitize(lm_all, bins)
xc = np.array([lm_all[ib == i].mean() for i in range(1, len(bins)) if (ib == i).sum() > 5])
yc = np.array([fc_all[ib == i].mean() for i in range(1, len(bins)) if (ib == i).sum() > 5])
fcold = lambda x: np.interp(x, xc, yc)
def prof(gc, sh):
    def fn(i, R):
        Mg, z, lm = gc["Mgal"][i], gc["z"][i], gc["logM"][i]
        lt = lm + 0.05 * sh
        Mt = 10 ** lt * (1 + fcold(lt))
        re = 0.4 * L.r_ta_law(Mt, a0, z); r = np.geomspace(1e-4, re, 1500); y = L.G_MPC * Mt / r ** 2 / a0
        Md = Mt * (L.nu_mono(y) - 1.0)
        return L.dsigma(R, r, Md, m0=Md[0]) + Mt / (math.pi * R ** 2)
    return fn
out = []
for f0 in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
    sh = int(round(math.log10(1 + f0) / 0.05))
    e = L.stack(grp[1], prof(grp[1], sh)); out.append(L.diff_stat(dat, K, late, e)[0])
print(", ".join(f"{v:.2f}" for v in out)); print("CFG61: 28.1, 18.2, 10.0, 4.8, 4.1, 10.4, 26.9, 58.4")
