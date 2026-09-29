# covariance / data-side attacks on the zero-model difference chi2 (law's D_L = 0 to 0.3% of sigma, so chi2_L = zero-model chi2)
import numpy as np, cfg77_lib as L
from scipy.stats import chi2 as c2, norm
dat = L.load_data("Color"); K = np.arange(8, 15); l, e = K, K + 15
C = dat["C"]; d = dat["d"]; D = d[e] - d[l]
def chi(CD): return float(D @ np.linalg.solve(CD, D))
full = C[np.ix_(e, e)] + C[np.ix_(l, l)] - C[np.ix_(e, l)] - C[np.ix_(l, e)]
nocross = C[np.ix_(e, e)] + C[np.ix_(l, l)]
diag = np.diag(np.diag(full))
print(f"full C_D: {chi(full):.2f}; drop cross-class blocks: {chi(nocross):.2f}; diagonal only: {chi(diag):.2f}")
cross = C[np.ix_(e, l)]; sd = np.sqrt(np.diag(C))
print("cross-class correlation, same g_bar bins (diag of C_el/(s_e s_l)):", np.round(np.diag(cross) / (sd[e] * sd[l]), 3))
print("adjacent-bin correlation within class (early):", np.round([C[e[i], e[i+1]] / (sd[e[i]] * sd[e[i+1]]) for i in range(6)], 2))
# inflate errors x1.2 / x1.5
for s in (1.2, 1.5, 2.0): print(f"errors x{s}: chi2 {chi(full*s**2):.2f}/7 p {c2.sf(chi(full*s**2), 7):.1e}")
# significance in sigma
p = c2.sf(chi(full), 7); print(f"p {p:.2e} -> two-sided-equivalent {norm.isf(p/2):.2f} sigma")
# leave-one-out over K1
for j in range(7):
    m = [i for i in range(7) if i != j]; Cs = full[np.ix_(m, m)]; Ds = D[m]
    print(f" drop bin {K[j]}: chi2 {float(Ds @ np.linalg.solve(Cs, Ds)):.2f}/6")
# fractional difference (early/late) per bin in K1
print("early/late ratio in K1:", np.round(d[e] / d[l], 2))
# Sersic
ds = L.load_data("Sersic"); Cs = ds["C"]; Ds = ds["d"][e] - ds["d"][l]
Fs = Cs[np.ix_(e, e)] + Cs[np.ix_(l, l)] - Cs[np.ix_(e, l)] - Cs[np.ix_(l, e)]
print(f"Sersic zero-model chi2 K1: {float(Ds @ np.linalg.solve(Fs, Ds)):.2f}/7")
