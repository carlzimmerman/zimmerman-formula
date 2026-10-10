"""Chart of the framework's kernel nu(y) = 1/(1-exp(-sqrt y)) vs Newton and two standard MOND kernels."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

y = np.logspace(-3, 3, 600)
nu_mono = 1.0 / (1.0 - np.exp(-np.sqrt(y)))                 # McGaugh+16 RAR form (framework kernel)
nu_simple = 0.5 + np.sqrt(0.25 + 1.0 / y)                    # MOND 'simple'
nu_standard = np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))      # MOND 'standard'
deep = 1.0 / np.sqrt(y)                                       # deep-MOND limit

fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
for a, f, lab in [(ax[0], lambda v: v, r"$\nu(y)=g/g_N$"), (ax[1], lambda v: v * y, r"$g/a_0 = \nu(y)\,y$")]:
    a.loglog(y, f(np.ones_like(y)), "k--", lw=1.2, label="Newton (ν = 1)")
    a.loglog(y, f(deep), ":", color="grey", lw=1.2, label="deep MOND (ν = 1/√y)")
    a.loglog(y, f(nu_simple), color="tab:orange", lw=1.5, label="MOND simple")
    a.loglog(y, f(nu_standard), color="tab:green", lw=1.5, label="MOND standard")
    a.loglog(y, f(nu_mono), color="tab:blue", lw=2.6, label="framework: 1/(1−exp(−√y))")
    a.axvline(1, color="0.8", lw=0.8)
    a.set_xlabel(r"$y = g_N/a_0$  (baryonic acceleration in units of $a_0$)")
    a.set_ylabel(lab); a.grid(True, which="both", alpha=0.25)
ax[0].set_ylim(0.9, 40); ax[0].set_title("Boost factor: how much stronger gravity is than Newton")
ax[1].set_title("Total acceleration vs baryonic acceleration (the RAR)")
ax[0].legend(fontsize=8, loc="upper right")
for yy in (0.01, 0.1, 1, 10):
    v = 1 / (1 - np.exp(-np.sqrt(yy)))
    ax[0].annotate(f"{v:.2f}", (yy, v), textcoords="offset points", xytext=(4, 6), fontsize=8, color="tab:blue")
fig.suptitle(r"The kernel $\nu(y)=1/(1-e^{-\sqrt{y}})$ (McGaugh, Lelli & Schombert 2016), with $a_0=\frac{1}{2}c\sqrt{G\rho_{DE}}$ (κ fitted)", fontsize=11)
fig.tight_layout()
fig.savefig("explainers/img/kernel_nu_mono.png", dpi=150)
print("wrote explainers/img/kernel_nu_mono.png")
