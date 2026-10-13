"""CFG687 POST-HOC (not frozen): why does the outer shear scale like M^0.9 instead of the law's M^0.47?
Per Mgas500 tercile: A_OUTER (law), median z, eRASS1 neighbours (|dz| < 0.02, projected 0.5-3 Mpc, any Mgas), and the slope s on
ISOLATED clusters only (no such neighbour). Environment (neighbour mass) adds outer shear in any theory and grows with mass."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = np.load(os.path.join(HERE, "cfg687_percluster.npz"))
D, E, PL, PN, mg, z, ra, dec = (P[k] for k in ("D", "E", "PL", "PN", "mg", "z", "ra", "dec")); W = np.where(E > 0, 1/E**2, 0)
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg687_inputs", "erass1_main.tsv"))]
cat = []
for r in rows:
    try: cat.append((float(r[1]), float(r[2]), float(r[3])))
    except Exception: pass
cat = np.array(cat)
# projected separation with a small-angle approx at the cluster's distance (BAO-raw D_A as CFG686; reuse a simple local scale)
from scipy.interpolate import PchipInterpolator
zb = [0, 0.295, 0.510, 0.706]; dm = [0, 8.325, 13.588, 17.351]; pch = PchipInterpolator(zb, dm); RD = 101.54/0.70
nb = np.zeros(len(z), int)
for i in range(len(z)):
    sel = np.abs(cat[:, 2] - z[i]) < 0.02
    c_ = cat[sel]; dra = (c_[:, 0] - ra[i])*np.cos(np.radians(dec[i])); dde = c_[:, 1] - dec[i]
    sep = np.radians(np.hypot(dra, dde))*pch(z[i])*RD/(1 + z[i])
    nb[i] = ((sep > 0.5) & (sep < 3.0)).sum()
q = np.quantile(mg, [0, 1/3, 2/3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2); j = [6, 7]
def A(sel, Pr): return (W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*Pr[sel][:, j]).sum()
def outer(sel, arr): return (W[sel][:, j]*arr[sel][:, j]).sum()/W[sel][:, j].sum()
out = {}
for t in range(3):
    s = tid == t
    out[t] = dict(n=int(s.sum()), Mgas_med=float(np.median(mg[s])), z_med=float(np.median(z[s])), nb_mean=float(nb[s].mean()), frac_with_nb=float((nb[s] > 0).mean()),
                  A_outer_law=float(A(s, PL)), A_outer_iso=float(A(s & (nb == 0), PL)) if (s & (nb == 0)).sum() > 5 else None, n_iso=int((s & (nb == 0)).sum()))
    print(f"tercile {t}: N={out[t]['n']} Mgas~{out[t]['Mgas_med']:.2e} z~{out[t]['z_med']:.3f} neighbours/cl {out[t]['nb_mean']:.2f} (with≥1: {out[t]['frac_with_nb']:.2f})  "
          f"A_OUTER(law) {out[t]['A_outer_law']:.2f}   isolated: n={out[t]['n_iso']} A={out[t]['A_outer_iso']}")
def slope(sel, arr):
    xs, ys = [], []
    for t in range(3):
        s = sel & (tid == t); v = outer(s, arr)
        if v <= 0 or s.sum() < 5: return np.nan
        xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]
iso = nb == 0; rng = np.random.default_rng(3)
s_iso = slope(iso, D); boots = [slope(np.isin(np.arange(len(z)), rng.choice(np.where(iso)[0], iso.sum())) & iso, D) for _ in range(500)]
print(f"\nisolated clusters ({iso.sum()}): s_obs = {s_iso:.2f} ± {np.nanstd(boots):.2f} (bootstrap)   s_law(iso) = {slope(iso, PL):.2f}   s_Newton(iso) = {slope(iso, PN):.2f}")
print(f"all: corr(Mgas500, neighbours) Spearman ≈ {np.corrcoef(np.argsort(np.argsort(mg)), np.argsort(np.argsort(nb)))[0,1]:.2f}")
out["isolated"] = dict(n=int(iso.sum()), s_obs=float(s_iso), s_err=float(np.nanstd(boots)), s_law=float(slope(iso, PL)), s_newton=float(slope(iso, PN)))
json.dump(out, open(os.path.join(HERE, "cfg687_posthoc_t2.json"), "w"), indent=1)
