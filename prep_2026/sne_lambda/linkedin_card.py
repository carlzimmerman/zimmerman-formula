#!/usr/bin/env python3
"""
Standalone LinkedIn card (4:5 portrait, 1200x1500) of the side-by-side result:
the supernova dark-energy term fit freely (LCDM) vs pinned from galaxy rotation curves.
Headline + two stacked panels + honest caption + DOI baked in. Reuses side_by_side.py's fit.
"""
import numpy as np
from scipy import optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec

c_ms, G, MPC = 2.99792458e8, 6.67430e-11, 3.0856776e22
Z = np.sqrt(32*np.pi/3)
A0_CANON = 9.355e-11
A0_SPARC, A0_LO, A0_HI = 1.181e-10, 0.84e-10, 1.36e-10

d = np.genfromtxt("pantheonplus_full.dat", names=True, dtype=None, encoding=None)
m = (d["IS_CALIBRATOR"] == 0) & (d["zHD"] > 0.023)
z, mb, dmb = d["zHD"][m], d["m_b_corr"][m], d["m_b_corr_err_DIAG"][m]
N = len(z); w = 1/dmb**2; zg = np.linspace(0, z.max()*1.02, 4000)

def Ez(zz, OmL): return np.sqrt((1-OmL)*(1+zz)**3 + OmL)
def shape_at(OmL, zarr):
    inv = 1.0/Ez(zg, OmL)
    integ = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])
    return 5*np.log10((1+zarr)*np.interp(zarr, zg, integ))
def chi2(OmL):
    dd = mb - shape_at(OmL, z); return float(np.sum(dd*dd*w) - np.sum(dd*w)**2/np.sum(w))

r = optimize.minimize_scalar(chi2, bounds=(0.0, 0.99), method="bounded")
OmL_A, chiA = r.x, r.fun
f = lambda x: chi2(x)-(chiA+1); lo = optimize.brentq(f,0.001,OmL_A); hi = optimize.brentq(f,OmL_A,0.999)
def OmL_from_a0(a0,H0): return (Z**2*a0**2)/(c_ms**2*(H0*1e3/MPC)**2)
def a0_from_OmL(OmL,H0): return (c_ms*(H0*1e3/MPC)/Z)*np.sqrt(OmL)
OmL_can = OmL_from_a0(A0_CANON, 67.4)
dchi = chi2(OmL_can) - chiA

# ---------- card ----------
INK, MUTE, RED, BLUE = "#1a1a2e", "#5a5a6e", "#c0392b", "#2471a3"
plt.rcParams.update({"font.family":"DejaVu Sans"})
fig = plt.figure(figsize=(8, 10), dpi=150)
fig.patch.set_facecolor("white")
gs = gridspec.GridSpec(4, 1, height_ratios=[0.155, 0.335, 0.235, 0.275], hspace=0.42,
                       left=0.105, right=0.955, top=0.985, bottom=0.02)

# --- header ---
axh = fig.add_subplot(gs[0]); axh.axis("off")
axh.text(0, 0.66, "Same supernovae. One fewer free parameter.",
         fontsize=20.5, fontweight="bold", color=INK, va="center")
axh.text(0, 0.12, "The dark-energy term: fit freely (ΛCDM)  vs  pinned from galaxy rotation curves",
         fontsize=12.2, color=MUTE, va="center")

# --- panel 1: Hubble residuals to Model A ---
ax1 = fig.add_subplot(gs[1])
shpA = shape_at(OmL_A, z); shpB = shape_at(OmL_can, z)
residA = mb - shpA; residA -= np.sum(residA*w)/np.sum(w)
offB = np.sum((shpB-shpA)*w)/np.sum(w)
zb = np.logspace(np.log10(z.min()), np.log10(z.max()), 15); idx = np.digitize(z, zb)
keep = [i for i in range(1,len(zb)) if (idx==i).sum()>3]
zc = np.array([z[idx==i].mean() for i in keep])
rc = np.array([np.average(residA[idx==i],weights=w[idx==i]) for i in keep])
re = np.array([1/np.sqrt(w[idx==i].sum()) for i in keep])
zz = np.logspace(np.log10(z.min()), np.log10(z.max()), 300)
curveB = (shape_at(OmL_can,zz)-shape_at(OmL_A,zz)) - offB
ax1.errorbar(zc, rc*1e3, yerr=re*1e3, fmt='o', ms=6, color="0.4", capsize=2.5,
             label=f"Pantheon+ supernovae (N={N})", zorder=3)
ax1.axhline(0, color=RED, lw=3, label=f"ΛCDM: Ω$_\\Lambda$ FREE = {OmL_A:.2f}   (1 free knob)")
ax1.plot(zz, curveB*1e3, '--', lw=3, color=BLUE,
         label=f"Framework: a$_0$-pinned Ω$_\\Lambda$ = {OmL_can:.2f}   (0 free knobs)")
ax1.set_xscale("log"); ax1.set_xlabel("redshift  z", fontsize=12)
ax1.set_ylabel("Δμ vs ΛCDM  [milli-mag]", fontsize=12)
ax1.set_title(f"The two fits are indistinguishable in the data  (Δχ² = +{dchi:.1f} over {N} SNe)",
              fontsize=12.5, fontweight="bold", color=INK, pad=8)
ax1.legend(fontsize=10.3, loc="upper left", framealpha=0.9)
ax1.grid(alpha=0.22, which="both"); ax1.tick_params(labelsize=10.5)

# --- panel 2: a0 agreement number line ---
ax2 = fig.add_subplot(gs[2])
ax2.axvspan(A0_LO*1e11, A0_HI*1e11, color=BLUE, alpha=0.14)
ax2.text((A0_LO*1e11+A0_HI*1e11)/2, 2.72, "galaxies MEASURE a$_0$  (rotation curves, Λ-blind)",
         ha="center", va="center", fontsize=10.6, color=BLUE, fontweight="bold")
a1=a0_from_OmL(OmL_A,67.4)*1e11; a1l=a0_from_OmL(lo,67.4)*1e11; a1h=a0_from_OmL(hi,67.4)*1e11
a2=a0_from_OmL(OmL_A,73.0)*1e11; a2l=a0_from_OmL(lo,73.0)*1e11; a2h=a0_from_OmL(hi,73.0)*1e11
ax2.errorbar([a1],[1.75],xerr=[[a1-a1l],[a1h-a1]],fmt='s',ms=12,color=RED,capsize=5,
             label="SNe DEMAND a$_0$  (H$_0$=67.4)")
ax2.errorbar([a2],[0.95],xerr=[[a2-a2l],[a2h-a2]],fmt='D',ms=12,color="#e67e22",capsize=5,
             label="SNe DEMAND a$_0$  (H$_0$=73)")
ax2.axvline(9.355, color="k", ls=":", lw=2)
ax2.text(9.355, 0.2, "canonical\n9.36", ha="center", va="bottom", fontsize=9, color="k")
ax2.set_yticks([]); ax2.set_ylim(0,3.25); ax2.set_xlim(7.6,14.4)
ax2.set_xlabel(r"a$_0$   [$\times 10^{-11}$ m s$^{-2}$]", fontsize=12)
ax2.set_title("Two datasets that share no inputs agree on a$_0$",
              fontsize=12.5, fontweight="bold", color=INK, pad=8)
ax2.legend(fontsize=10.3, loc="lower right", framealpha=0.9)
ax2.grid(alpha=0.22, axis="x"); ax2.tick_params(labelsize=10.5)

# --- footer caption ---
axf = fig.add_subplot(gs[3]); axf.axis("off")
cap = ("Pin the dark-energy term from galaxy rotation curves — zero free dark-energy "
       "parameters — and the Pantheon+\nsupernovae fit as well as ΛCDM's free fit. The a$_0$ the "
       "supernovae demand (≈ 9.2–9.9) lands inside the box\ngalaxies independently measure. "
       "Identical to ΛCDM at z = 0; the two diverge only if a$_0$ evolves — a test for\ngalaxy "
       "surveys, not supernovae.  Not a correction of ΛCDM; a consistency check with one fewer knob.")
axf.text(0, 0.86, cap, fontsize=10.9, color=INK, va="top", linespacing=1.5)
axf.text(0, 0.02, "H²(z) = (8πG/3)·ρ$_m$(z) + Z²·a$_0$²(z)/c²,   Z = √(32π/3)        "
                  "Zenodo 10.5281/zenodo.21440408 · Carl Zimmerman, Briar Creek Tech",
         fontsize=9.6, color=MUTE, va="bottom", fontweight="bold")

fig.savefig("linkedin_card.png", dpi=150, facecolor="white", bbox_inches="tight")
print(f"OmL_A={OmL_A:.3f}  OmL_can={OmL_can:.3f}  dchi={dchi:+.1f}  SNe-a0 {a1:.2f}(P)/{a2:.2f}(S)")
print("card -> linkedin_card.png"); print("EXIT 0")
