"""CFG956 figure (PLOT ONLY): every plotted number is read from cfg956.json, cfg956_DAMPED.json, CFG689's cfg689.json and the
galaxy points stored in cfg956.json (themselves read from the committed chart / CFG303 / CFG309 / CFG301 files).

The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21).
kappa = 1/2 FITTED; the two footings are drawn separately and never pooled; ratio bounds are identical on both by construction.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg956_figure.py
"""
import os, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.interpolate import PchipInterpolator

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE)
M = json.load(open(os.path.join(HERE, "cfg956.json"))); D = json.load(open(os.path.join(HERE, "cfg956_DAMPED.json")))
PH = json.load(open(os.path.join(HERE, "cfg956_POSTHOC_G1.json")))      # post hoc inner window (boundary waves), reported only
J689 = json.load(open(os.path.join(CFG, "CFG689_native_ruler_bao", "cfg689.json")))
NODES = np.array(J689["cfg"]["nodes"]); WB = np.array(J689["BAO+SN"]["P2"]["pbest"][:6])
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
COL = {"canonical": "#0072B2", "alt": "#D55E00"}; MFC = {"canonical": COL["canonical"], "alt": "white"}
BCOL = {"S": "#009E73", "C": "#1a1a1a", "N": "#999999"}
BETACOL = {0.0: "#1a1a1a", 0.5: "#0072B2", 1.0: "#009E73", 2.0: "#CC79A7"}
INK, GREY = "#1a1a1a", "#6b6b6b"
ATTR = "The oscillating-a$_0$(z) hypothesis, including its damped form, is the owner's idea (2026-10-21)."
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.linewidth": 0.8, "legend.frameon": False, "legend.fontsize": 8.4, "savefig.facecolor": "white"})
fig, axs = plt.subplots(2, 2, figsize=(13.0, 10.6))
fig.subplots_adjust(left=0.07, right=0.985, top=0.885, bottom=0.115, wspace=0.26, hspace=0.34)

# ---------------- (a) plain wave: eps_95 vs P
ax = axs[0, 0]
for br, lab in (("S", "branch S: CFG689 best-fit background"), ("C", "branch C: constant ρ$_{\\rm DE}$"), ("N", "branch N: six free nodes (reported only)")):
    rr = M["rows"][br]; Pv = np.array([r["P"] for r in rr]); ev = np.array([min(r["eps95"], 1.0) for r in rr])
    nb = np.array([r["bound_class"].startswith("NO BOUND") for r in rr])
    ax.plot(Pv, ev, color=BCOL[br], lw=2.0 if br != "N" else 0, marker="o" if br != "N" else "D", ms=4.5 if br != "N" else 6.5,
            mfc=BCOL[br] if br != "N" else "white", mec=BCOL[br], label=lab, zorder=3)
    if nb.any(): ax.plot(Pv[nb], ev[nb], ls="none", marker="^", ms=9, color=BCOL[br], zorder=4)
ax.axhline(1.0, color=GREY, lw=0.9, ls=(0, (2, 2)))
ax.text(0.052, 1.03, "ε = 1: a$_0$ touches zero at the troughs (no bound if reached, ▲)", fontsize=7.8, color=GREY, va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(0.004, 1.6); ax.set_xlim(0.045, 3.3)
ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1, 2, 3]); ax.set_xticklabels(["0.05", "0.1", "0.25", "0.5", "1", "2", "3"])
ax.set_xlabel("period P in ln(1+z)"); ax.set_ylabel("ε$_{95}$  (95% upper bound, Δχ² = 3.84, φ profiled)")
ax.set_title("(a)  Plain wave: largest allowed ε vs period", loc="left", fontweight="bold")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.93), fontsize=8.0)
ax.text(0.02, 0.03, "a$_0$(z)/a$_0$(0) = A(z)[1 + ε sin(2π ln(1+z)/P + φ)]/(1 + ε sin φ)\nratio bound: identical on the canonical and alt footings (κ fitted per footing)",
        transform=ax.transAxes, fontsize=7.8, color=INK, va="bottom")

# ---------------- (b) damped wave: eps0_95 vs P per beta
ax = axs[0, 1]
for beta in D["betas"]:
    for br, ls in (("C", "-"), ("S", (0, (4, 2)))):
        rr = D["rows"][f"beta{beta}_{br}"]; Pv = np.array([r["P"] for r in rr]); ev = np.array([r["eps95"] for r in rr])
        ax.plot(Pv, ev, color=BETACOL[beta], lw=1.8, ls=ls, marker="o" if br == "C" else "s", ms=3.4, mfc=BETACOL[beta] if br == "C" else "white", mec=BETACOL[beta])
    ax.axhline(3.5**-beta, color=BETACOL[beta], lw=0.7, ls=(0, (1, 2)))
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.045, 3.3); ax.set_ylim(0.0015, 1.6)
ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1, 2, 3]); ax.set_xticklabels(["0.05", "0.1", "0.25", "0.5", "1", "2", "3"])
ax.set_xlabel("period P in ln(1+z)"); ax.set_ylabel("ε$_{0,95}$  (amplitude today, 95% upper bound)")
ax.set_title("(b)  Damped wave, on the way down today: ε$_0$ bound", loc="left", fontweight="bold")
h = [Line2D([], [], color=BETACOL[b], lw=1.8, label=f"β = {b:g}") for b in D["betas"]]
h += [Line2D([], [], color=GREY, lw=1.6, ls="-", marker="o", ms=3.4, label="branch C"), Line2D([], [], color=GREY, lw=1.6, ls=(0, (4, 2)), marker="s", ms=3.4, mfc="white", label="branch S"),
      Line2D([], [], color=GREY, lw=0.7, ls=(0, (1, 2)), label="a$_0$ ≥ 0 cap 3.5$^{-β}$")]
ax.legend(handles=h, loc="lower right", ncol=2, fontsize=7.8)
ax.text(0.02, 0.97, "ε(z) = ε$_0$ (1+z)$^β$;  φ restricted to d a$_0$/dt < 0 today", transform=ax.transAxes, fontsize=7.8, va="top")

# ---------------- (c) largest allowed amplitude by redshift (max over P)
ax = axs[1, 0]
zz = np.linspace(0, 5.5, 300)
ax.axvspan(2.5, 5.5, color="#efefef", lw=0, zorder=0)
ax.text(4.0, 0.012, "no expansion datum above z ≈ 2.5:\nthe amplitude here is the family's\nextrapolation, not a bound", ha="center", fontsize=8.0, color=GREY)
for beta in D["betas"]:
    for br, ls in (("C", "-"), ("S", (0, (4, 2)))):
        e0 = max(r["eps95"] for r in D["rows"][f"beta{beta}_{br}"])
        ax.plot(zz, e0*(1 + zz)**beta, color=BETACOL[beta], lw=1.8, ls=ls)
for br, ls in (("C", "-"), ("S", (0, (4, 2)))):
    e = max(min(r["eps95"], 1.0) for r in M["rows"][br])
    ax.plot(zz, np.full_like(zz, e), color="#E69F00", lw=1.4, ls=ls)
ax.axhline(1.0, color=GREY, lw=0.9, ls=(0, (2, 2))); ax.text(0.05, 1.06, "amplitude 1: a$_0$ reaches zero at a trough", fontsize=7.8, color=GREY)
ax.set_yscale("log"); ax.set_xlim(0, 5.5); ax.set_ylim(0.01, 40)
ax.set_xlabel("redshift z"); ax.set_ylabel("largest allowed wave amplitude ε(z)  (max over P)")
ax.set_title("(c)  Largest allowed amplitude by redshift", loc="left", fontweight="bold")
h = [Line2D([], [], color=BETACOL[b], lw=1.8, label=f"damped β = {b:g}") for b in D["betas"]] + [Line2D([], [], color="#E69F00", lw=1.4, label="plain wave (a), any phase")]
h += [Line2D([], [], color=GREY, lw=1.6, ls="-", label="branch C"), Line2D([], [], color=GREY, lw=1.6, ls=(0, (4, 2)), label="branch S")]
ax.legend(handles=h, loc="upper left", fontsize=7.8, ncol=2)

# ---------------- (d) a0(z)/a0(footing, today)
ax = axs[1, 1]; ax.set_yscale("log")
ax.axvspan(2.5, 5.75, color="#f4f4f4", lw=0, zorder=0)
b689 = J689["BAO+SN"]
zb = [1.0, 1.2, 1.5, 2.0, 2.33]; qq = [b689["P6"]["2.0"]["sqrtX_q"] if z == 2.0 else b689["P1"][str(z)]["sqrtX_q"] for z in zb]
ax.fill_between(zb, [q[1] for q in qq], [q[3] for q in qq], color="#009E73", alpha=0.22, lw=0, zorder=1)
zs = np.linspace(0, 2.5, 300); AS = np.sqrt(np.interp(zs, NODES, WB)/WB[0])
ax.plot(zs, AS, color="#009E73", lw=1.6, zorder=2); ax.axhline(1.0, color=INK, lw=1.2, zorder=2)
# largest allowed plain wave (branch S) envelope and its realisation at the bound
rS = max(M["rows"]["S"], key=lambda r: min(r["eps95"], 1.0)); e = min(rS["eps95"], 1.0)
ax.fill_between(zs, AS*(1 - e), AS*(1 + e), color="#E69F00", alpha=0.25, lw=0, zorder=1.5)
wv = AS*(1 + e*np.sin(2*np.pi*np.log1p(zs)/rS["P"] + rS["phi95"]))/(1 + e*np.sin(rS["phi95"]))
ax.plot(zs, wv, color="#E69F00", lw=1.3, zorder=2.5)
# high-z prediction window (z 3-5): union over beta, P and both branches. Outer (frozen): eps0 <= eps0_95 at every allowed phi.
# Inner (post hoc): the boundary waves themselves. The true allowed window lies between them.
zw = [float(z) for z in D["window_z"]]; keys = [f"beta{b}_{br}" for b in D["betas"] for br in ("S", "C")]
lo = [min(D["summary"][k]["window_all_P"]["lo"][str(z)] for k in keys) for z in D["window_z"]]
hi = [max(D["summary"][k]["window_all_P"]["hi"][str(z)] for k in keys) for z in D["window_z"]]
ax.fill_between(zw, np.maximum(lo, 0.045), hi, facecolor="none", edgecolor=GREY, hatch="////", lw=0.8, alpha=0.7, zorder=1.6)
ilo = [min(PH["inner_window"][k]["lo"][str(z)] for k in keys) for z in D["window_z"]]
ihi = [max(PH["inner_window"][k]["hi"][str(z)] for k in keys) for z in D["window_z"]]
ax.fill_between(zw, np.maximum(ilo, 0.045), ihi, color="#CC79A7", alpha=0.22, lw=0, zorder=1.7)
ax.text(4.0, 0.052, "a$_0$ can reach 0 (β ≥ 1, family extrapolation)", fontsize=7.0, color=GREY, ha="center", va="bottom")
# galaxy points (s* relative to canonical; converted per footing)
for g in M["galaxy"]:
    if g["s"] is None or g["sigma_dex"] is None or not g["label"].startswith(("CFG303", "CFG309")) and "ALESS" not in g["label"] and "ALPINE6" not in g["label"]: continue
    for f, dx in (("canonical", -0.04), ("alt", 0.04)):
        k = 9.3603e-11/A0[f]; x = g["z"] + dx
        ax.plot([x, x], [max(g["lo68"]*k, 0.05), min(g["hi68"]*k, 60)], color=COL[f], lw=2.6, solid_capstyle="butt", zorder=4, alpha=0.9)
        ax.plot([x], [g["s"]*k], marker="o", ms=5.2, color=COL[f], mfc=MFC[f], mec=COL[f], mew=1.2, zorder=5)
# illustrative sketch (faint)
sk = M["illustrative_sketch"]["points"]; PCH = PchipInterpolator(np.log1p(sk["z"]), np.log(sk["s"]))
zk = np.linspace(0, 4.5, 300); ax.plot(zk, np.exp(PCH(np.log1p(zk))), color="#7f7fbf", lw=1.1, ls=(0, (3, 2)), alpha=0.7, zorder=2)
ax.text(0.62, 2.25, "illustrative sketch (not the hypothesis)", fontsize=7.6, color="#7f7fbf")
ax.set_xlim(-0.1, 5.75); ax.set_ylim(0.045, 60)
ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]); ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("redshift z"); ax.set_ylabel("a$_0$(z) / a$_0$(footing, today)")
ax.set_title("(d)  Allowed waves in a$_0$(z), and the z 3–5 window", loc="left", fontweight="bold")
h = [Patch(color="#009E73", alpha=0.3, label="CFG689 native band, 68%; green line = branch-S background"),
     Patch(color="#E69F00", alpha=0.35, label=f"largest allowed plain wave, ±ε$_{{95}}$ = ±{e:.3f} (P = {rS['P']:g}; line at the bound)"),
     Patch(facecolor="none", edgecolor=GREY, hatch="////", label="z 3–5 window, all damped β and P: outer (any allowed phase)"),
     Patch(color="#CC79A7", alpha=0.3, label="z 3–5 window: inner (the boundary waves; post hoc)"),
     Line2D([], [], color=COL["canonical"], marker="o", lw=2.4, label="implied a$_0$, canonical footing (68%)"),
     Line2D([], [], color=COL["alt"], marker="o", mfc="white", lw=2.4, label="implied a$_0$, alt footing (68%)")]
ax.legend(handles=h, loc="upper left", fontsize=7.4)
ax.text(5.7, 42, "no expansion bound\nabove z ≈ 2.5", ha="right", va="top", fontsize=8.0, color=GREY)

fig.suptitle("CFG956 — the largest wave in a$_0$(z) that the framework's own expansion constraint allows (CFG689 native-ruler BAO + Pantheon+, primary)",
             x=0.07, y=0.975, ha="left", fontsize=12.5, fontweight="bold")
fig.text(0.07, 0.935, "a$_0$(z) = κ c √(G ρ$_{\\rm DE}$(z)), κ = ½ fitted; a wave in a$_0$ is a wave in ρ$_{\\rm DE}$, squared.  Bounds use z ≤ 2.33 data only; above z ≈ 2.5 the expansion data place no bound.",
         fontsize=9.2, color=INK)
fig.text(0.07, 0.035, ATTR + "  Footings never pooled; a bound on a wave is not evidence for a wave; nothing here favours the framework over ΛCDM; not a closed theory.",
         fontsize=8.2, color=GREY)
fig.savefig(os.path.join(HERE, "cfg956_wave_bound.png"), dpi=200)
print("wrote cfg956_wave_bound.png")
