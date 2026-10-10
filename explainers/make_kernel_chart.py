"""Chart of the framework's kernel nu(y) = 1/(1-exp(-sqrt y)) vs Newton and two standard MOND kernels."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
# nu_mono exactly as in the framework engine (campaign_fresh_gravity/CFG424_turnaround_catchment/cfg424_pm.py)
def h_rar(y):
    y=np.asarray(y,float)
    with np.errstate(over="ignore"):
        return np.where(y<1e4, y/np.expm1(np.sqrt(np.minimum(y,1e4))), 0.0)
def dh_rar(y,e=1e-6): return (h_rar(y*(1+e))-h_rar(y*(1-e)))/(2*y*e)
Y_P=brentq(lambda t: float(dh_rar(t)),1.0,5.0); H_P=float(h_rar(Y_P)); DELTA=0.05
LYG=np.linspace(-12,12,240001); YG=10**LYG
DH=np.maximum(dh_rar(YG),DELTA*H_P/(YG+Y_P))
HM=float(h_rar(YG[0]))+np.concatenate([[0.0],np.cumsum(0.5*(DH[1:]+DH[:-1])*np.diff(YG))])
def nu_mono(y): y=np.maximum(np.asarray(y,float),1e-12); return 1.0+np.interp(np.log10(y),LYG,HM)/y

y = np.logspace(-3, 3, 600)
nu_rar = 1.0 / (1.0 - np.exp(-np.sqrt(y)))                  # McGaugh+16 RAR form
nu_fw = nu_mono(y)                                            # framework kernel nu_mono
nu_simple = 0.5 + np.sqrt(0.25 + 1.0 / y)                    # MOND 'simple'
nu_standard = np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))      # MOND 'standard'
deep = 1.0 / np.sqrt(y)                                       # deep-MOND limit

fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
for a, f, lab in [(ax[0], lambda v: v, r"$\nu(y)=g/g_N$"), (ax[1], lambda v: v * y, r"$g/a_0 = \nu(y)\,y$")]:
    a.loglog(y, f(np.ones_like(y)), "k--", lw=1.2, label="Newton (ν = 1)")
    a.loglog(y, f(deep), ":", color="grey", lw=1.2, label="deep MOND (ν = 1/√y)")
    a.loglog(y, f(nu_simple), color="tab:orange", lw=1.5, label="MOND simple")
    a.loglog(y, f(nu_standard), color="tab:green", lw=1.5, label="MOND standard")
    a.loglog(y, f(nu_rar), color="tab:purple", lw=1.4, ls="--", label="RAR form 1/(1−exp(−√y)) (McGaugh+16)")
    a.loglog(y, f(nu_fw), color="tab:blue", lw=2.6, label="framework ν_mono (= RAR form for y ≲ 2.5, monotonic tail above)")
    a.axvline(1, color="0.8", lw=0.8)
    a.set_xlabel(r"$y = g_N/a_0$  (baryonic acceleration in units of $a_0$)")
    a.set_ylabel(lab); a.grid(True, which="both", alpha=0.25)
ax[0].set_ylim(0.9, 40); ax[0].set_title("Boost factor: how much stronger gravity is than Newton")
ax[1].set_title("Total acceleration vs baryonic acceleration (the RAR)")
ax[0].legend(fontsize=8, loc="upper right")
for yy in (0.01, 0.1, 1, 10):
    v = float(nu_mono(yy))
    ax[0].annotate(f"{v:.2f}", (yy, v), textcoords="offset points", xytext=(4, 6), fontsize=8, color="tab:blue")
fig.suptitle(r"Framework kernel $\nu_{\rm mono}$: the RAR form $1/(1-e^{-\sqrt{y}})$ (McGaugh+16) below $y\approx2.5$, with a monotonic tail above; $a_0=\frac{1}{2}c\sqrt{G\rho_{DE}}$ (κ fitted)", fontsize=10)
fig.tight_layout()
fig.savefig("explainers/img/kernel_nu_mono.png", dpi=150)
print("wrote explainers/img/kernel_nu_mono.png")
