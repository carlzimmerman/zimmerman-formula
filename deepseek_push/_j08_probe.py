import numpy as np, sys
from scipy.stats import chi2
sys.path.insert(0, "deepseek_push")
from J02_moment_hierarchy import simulate

n = 600000
for (tau0,q,src) in ((1.0,0.0,'central'),(1.0,10.0,'central'),(2.0,3.0,'central'),(1.0,0.0,'volume')):
    r = simulate(n, tau0, q, src, seed=71)
    D, v2, ang, N = r["D"], r["v2"], r["ang"], r["N"]
    atom = N == 0
    frac = np.mean(atom)
    pred = np.exp(-tau0*(1+q/3.0))
    W = v2/(2*np.clip(ang,1e-12,None))
    m = ang > 0
    ww = W[m]
    pts = np.linspace(0.05, 8, 40)
    ecdf = np.array([np.mean(ww<=p) for p in pts])
    ks = np.max(np.abs(ecdf - chi2.cdf(pts,1)))
    edges = np.percentile(D[m], [0,33,67,100])
    bins_ok = True
    for k in range(3):
        mm = m & (D>=edges[k]) & (D<edges[k+1])
        e2 = np.array([np.mean(W[mm]<=p) for p in pts])
        ks2 = np.max(np.abs(e2 - chi2.cdf(pts,1)))
        bins_ok = bins_ok and ks2 < 0.03
    print(f"{src} tau0={tau0} q={q}: atom frac={frac:.4f} (pred {pred:.4f})  "
          f"chi2_1 KS(ang>0)={ks:.4f}  all-Dbins={bins_ok}")