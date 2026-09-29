# POST-HOC (labelled) further readings of the f_hot ladder
import math, numpy as np, cfg77_lib as L
dat = L.load_data("Color"); K = list(range(8, 15))
len_ = L.load_lenses(); grp = L.make_groups(len_); a0 = L.A0["canonical"]
late = L.stack(grp[0], L.law_profile(grp[0], "canonical"))
def run(groups_c, f, mode):
    g, w = L._quad_nodes(); num = np.zeros(15); den = np.zeros(15)
    for i in range(len(groups_c["n"])):
        M = groups_c["Mgal"][i]; n = groups_c["n"][i]; z = groups_c["z"][i]; Mt = M * (1 + f)
        R = np.sqrt(L.G_MPC * M / g).ravel()
        if mode == "E":     # dark from the law of M_true; point baryon mass only M_gal
            Ml, pt = Mt, M
        elif mode == "F":   # law of M_true with edge from M_gal's r_ta
            Ml, pt = Mt, Mt
        elif mode == "G":   # hot gas = extra mass; law of M_gal edge but nu argument M_true
            Ml, pt = Mt, Mt
        re = 0.4 * L.r_ta_law(M if mode == "F" else Mt, a0, z)
        r = np.geomspace(1e-4, re, 1500); y = L.G_MPC * Ml / r ** 2 / a0
        Md = Ml * (L.nu_mono(y) - 1.0)
        ds = (L.dsigma(R, r, Md, m0=Md[0]) + pt / (math.pi * R ** 2)).reshape(g.shape) * 1e-12
        ww = n * (Mt if mode == "G" else M) * w / g
        num += (ww * ds).sum(1); den += ww.sum(1)
    return num / den
for mode in ("E", "F", "G"):
    print(mode, ", ".join(f"{L.diff_stat(dat, K, late, run(grp[1], f, mode))[0]:.2f}" for f in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0)), flush=True)
print("CFG61: 28.1, 18.2, 10.0, 4.8, 4.1, 10.4, 26.9, 58.4")
