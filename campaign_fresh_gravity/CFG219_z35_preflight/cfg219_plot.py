#!/usr/bin/env python3
"""CFG219 figure: what six to twenty z ~ 5 independent-baryon discs could separate (a pre-flight forecast, not a measurement).
Drawn from cfg219_preflight_results.json (the lane's own mocks; nu_mono, canonical footing, S6 = the six CRISTAL dust detections, resampled for N > 6).
Panels 1-2: the systematic-inclusive significance n_tot (POST HOC, see the README: the frozen n_sigma is blind to a shared calibration systematic) against N for each shared
gas-calibration systematic tau (dex on the gas mass), at R_e (solid) and at the radius reached R_out (dashed); the 3-sigma line.  Panel 3: the largest tau at which each pair
still reaches 3 sigma at N = 20 and at N = 100 (a bar of 0 = never), R_e beside R_out.
Run: python3 campaign_fresh_gravity/CFG219_z35_preflight/cfg219_plot.py -> cfg219_power_forecast.png
"""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(LANE, "cfg219_preflight_results.json")))["results"]
NS = (6, 13, 16, 20, 30, 50, 100)
TAUS = (0.0, 0.1, 0.25, 0.4)
PAIRS = [("FLAT", "H(z)"), ("FLAT", "HORIZON"), ("FLAT", "LCDM-NATIVE"), ("H(z)", "HORIZON"), ("H(z)", "LCDM-NATIVE"), ("HORIZON", "LCDM-NATIVE")]


def rec(key, T, L, N, tau):
    return R[key][f"{T}|{L}|{N}|{tau}"]


def ntot(key, a, b, N, tau):
    x, y = rec(key, a, b, N, tau), rec(key, b, a, N, tau)
    return min(abs(x["mu"]) / x["sd_mock"], abs(y["mu"]) / y["sd_mock"])


def taumax(key, a, b, N):
    vs = [ntot(key, a, b, N, t) for t in TAUS]
    if vs[0] < 3.0:
        return 0.0
    for k in range(1, len(TAUS)):
        if vs[k] < 3.0:
            return TAUS[k - 1] + (vs[k - 1] - 3.0) * (TAUS[k] - TAUS[k - 1]) / (vs[k - 1] - vs[k])
    return TAUS[-1]


KE, KO = "S6|nu_mono|canonical|Re", "S6|nu_mono|canonical|Rout"
COL = {0.0: "#2a9d8f", 0.1: "#5b8def", 0.25: "#e9a23b", 0.4: "#d1541f"}
fig, ax = plt.subplots(1, 3, figsize=(17.5, 6.0), gridspec_kw={"width_ratios": [1, 1, 1.15]})
for a_, (A, B) in zip(ax[:2], PAIRS[:2]):
    for tau in TAUS:
        a_.plot(NS, [ntot(KE, A, B, N, tau) for N in NS], color=COL[tau], lw=2.2, marker="o", ms=4, label=f"τ = {tau:.2f} dex" + (" (statistical only)" if tau == 0 else ""))
        a_.plot(NS, [ntot(KO, A, B, N, tau) for N in NS], color=COL[tau], lw=1.6, ls="--", marker="s", ms=3.5)
    a_.axhline(3, color="0.25", lw=1.2)
    a_.text(100, 3.15, "3σ", ha="right", fontsize=9)
    a_.set_xscale("log"); a_.set_yscale("log")
    a_.set_xticks(NS); a_.set_xticklabels([str(n) for n in NS]); a_.set_ylim(0.6, 25)
    a_.set_xlabel("number of discs N (S6 inputs resampled for N > 6)")
    a_.set_ylabel("n_tot = |expected shift| / total scatter of the pooled median δ")
    a_.set_title(f"{A} vs {B}", fontsize=12)
    a_.grid(alpha=0.25, which="both")
ax[0].legend(fontsize=8.5, loc="upper left", title="shared gas calibration\n(solid: R_e, dashed: R_out)", title_fontsize=8)
w = 0.2
x = np.arange(len(PAIRS))
for j, (N, key, lab, hat) in enumerate(((20, KE, "N = 20, R_e", ""), (20, KO, "N = 20, R_out", "//"), (100, KE, "N = 100, R_e", ""), (100, KO, "N = 100, R_out", "//"))):
    vals = [taumax(key, a, b, N) for a, b in PAIRS]
    ax[2].bar(x + (j - 1.5) * w, vals, w, color=["#7aa6d8", "#7aa6d8", "#2f5d99", "#2f5d99"][j], hatch=hat, edgecolor="white", label=lab)
SHORT = {"LCDM-NATIVE": "ΛCDM-nat."}
ax[2].set_xticks(x); ax[2].set_xticklabels([f"{a}–{SHORT.get(b, b)}" for a, b in PAIRS], fontsize=8.5, rotation=18, ha="right")
ax[2].set_ylabel("largest τ that still gives 3σ (dex, on the gas mass)")
ax[2].set_title("how well the gas calibration must be known", fontsize=12)
ax[2].legend(fontsize=8.5); ax[2].grid(alpha=0.25, axis="y"); ax[2].set_ylim(0, 0.45)
ax[2].text(0.02, 0.42, "0 = never reaches 3σ\n0.40 = the grid's edge", fontsize=8, color="0.35", va="top")
fig.suptitle("CFG219: what 6–20 discs at z ≈ 4–6 with independent baryons could separate (pre-flight forecast, not a measurement; κ = ½ fitted)", fontsize=12.5)
fig.text(0.01, 0.005, "Six CRISTAL dust-detected discs' z, radius and baryon errors only (no velocities, no f_DM; velocity errors omitted, so optimistic). Laws from Z1: flat, H(z), particle horizon, ΛCDM-native; every pair is its own test.\n"
         "n_tot is a post hoc, systematic-inclusive statistic (the frozen n_σ ignores a shared offset by construction). τ is on the GAS mass; at gas fractions of 0.5-0.7 it is about 0.6 τ on the baryon mass.", fontsize=8.3, color="0.3")
plt.tight_layout(rect=(0, 0.06, 1, 0.95))
out = os.path.join(LANE, "cfg219_power_forecast.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
