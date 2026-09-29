# POST-HOC (labelled): alternative readings of the f_hot ladder, after the pre-declared reading gave 4.08/5.09 rather than 4.8/4.1.
import math, numpy as np, cfg77_lib as L
dat = L.load_data("Color"); K = list(range(8, 15))
len_ = L.load_lenses(); grp = L.make_groups(len_)
a0 = L.A0["canonical"]
def law_pt(groups_c, f, mode):
    """mode A (pre-declared): law of M_true, R from M_gal.  B: law of M_gal + hot gas as extra point mass f*M_gal (R from M_gal).
       C: law of M_true, R from M_true (pair positions from M_true)."""
    def fn(i, R):
        Mg = groups_c["Mgal"][i]; z = groups_c["z"][i]
        Ml = Mg * (1 + f) if mode in ("A", "C") else Mg
        re = 0.4 * L.r_ta_law(Ml, a0, z)
        r = np.geomspace(1e-4, re, 1500); y = L.G_MPC * Ml / r ** 2 / a0
        Md = Ml * (L.nu_mono(y) - 1.0)
        ds = L.dsigma(R, r, Md, m0=Md[0]) + Ml / (math.pi * R ** 2)
        if mode == "B": ds = ds + f * Mg / (math.pi * R ** 2)
        return ds
    return fn
def stack_mode(groups_c, f, mode):
    g, w = L._quad_nodes(); num = np.zeros(15); den = np.zeros(15); fn = law_pt(groups_c, f, mode)
    for i in range(len(groups_c["n"])):
        M = groups_c["Mgal"][i]; n = groups_c["n"][i]
        Rm = M * (1 + f) if mode == "C" else M
        R = np.sqrt(L.G_MPC * Rm / g).ravel()
        ds = fn(i, R).reshape(g.shape) * 1e-12; ww = n * M * w / g
        num += (ww * ds).sum(1); den += ww.sum(1)
    return num / den
late = L.stack(grp[0], L.law_profile(grp[0], "canonical"))
for mode in ("A", "B", "C"):
    out = []
    for f in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0):
        e = stack_mode(grp[1], f, mode)
        out.append(L.diff_stat(dat, K, late, e)[0])
    print(mode, ", ".join(f"{v:.2f}" for v in out), flush=True)
print("CFG61 README: 28.1, 18.2, 10.0, 4.8, 4.1 at 0, .25, .5, 1, 1.5")
