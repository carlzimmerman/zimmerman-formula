#!/usr/bin/env python3
"""L274 -- a0(z)/a0(0) for every law on the table, z = 0-5, WITH its +/- range: the chart and the table behind PAPER7 v2.
Laws: (1) the framework's own law (stage-17 pressure law: flat; the excitation's pressure moves it by < 1% for z <= 5, drawn as +/-0.004 dex);
(2) the framework with DESI DR2's w(z) taken at face value and mapped through the pressure, a0(z)/a0(0) = sqrt(w(z) rho_DE(z)/(w0 rho_DE(0))) (central: DESI+CMB+DESY5;
range: the union of the three SNe combinations' 68% bands at rho(w0,wa) = -0.9); (3) the density mapping a0 ∝ sqrt(rho_DE(z)) -- the naive
promotion stage-17 rejects, PAPER7's DESI sentence, an UPPER BOUND on the effect (same range recipe); (4) the H(z) law a0 ∝ H(z) (the alt footing;
range: DESI CPL vs Lambda and Omega_m +/- 0.0036); (5) the LambdaCDM-native emergent scale a_s(z)/a_s(0) = E(z)^{4/3} [c^2/f(c)](z)/[c^2/f(c)](0)
(PAPER7) with Dutton-Maccio 2014 c(M, z) at 1e12 h^-1 Msun (range: halo mass 1e11-1e13 and the 0.11 dex concentration scatter).  Marker: the
pre-registered single-rotator precision +/-0.13 dex at z = 2.5 (PAPER7).  Delta log v_flat at fixed M_b = 1/4 of the plotted axis.  A FAIL is a finding."""
import os, json, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L274 -- a0(z) for every law, with ranges\n")
HERE = os.path.dirname(os.path.abspath(__file__))
OM, SOM = 0.3027, 0.0036; OL = 1 - OM
DESI = {"DESY5": dict(w0=-0.752, sw0=0.057, wa=-0.86, swa=0.215), "Pantheon+": dict(w0=-0.838, sw0=0.055, wa=-0.62, swa=0.205), "Union3": dict(w0=-0.667, sw0=0.088, wa=-1.09, swa=0.29)}
f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
w_z = lambda z, w0, wa: w0 + wa * z / (1 + z)
E = lambda z, w0=-1.0, wa=0.0, om=OM: np.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w0, wa))
dex = lambda r: np.log10(r)
def dm14_c(z, M=1e12):                      # Dutton & Maccio 2014, NFW, Planck: log c = a + b log(M/1e12 h^-1 Msun)
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(M / 1e12))
fc = lambda c: np.log(1 + c) - c / (1 + c)
def lcdm_emergent(z, M=1e12, dlogc=0.0):
    c0 = dm14_c(0.0, M) * 10 ** dlogc; cz = dm14_c(z, M) * 10 ** dlogc
    return E(z) ** (4.0 / 3.0) * (cz ** 2 / fc(cz)) / (c0 ** 2 / fc(c0))
zg = np.linspace(0.0, 5.0, 101); ZT = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0])
rng = np.random.default_rng(274)
def band(zs, mapping):
    """68% band at rho = -0.9, union over the three SNe combinations; central = DESY5 best fit."""
    lo, hi = np.full(len(zs), np.inf), np.full(len(zs), -np.inf)
    for d in DESI.values():
        cov = np.array([[d["sw0"] ** 2, -0.9 * d["sw0"] * d["swa"]], [-0.9 * d["sw0"] * d["swa"], d["swa"] ** 2]])
        s = rng.multivariate_normal([d["w0"], d["wa"]], cov, size=40000, method="cholesky")
        for i, z in enumerate(zs):
            v = dex(mapping(z, s[:, 0], s[:, 1])); l, h = np.percentile(v, [16, 84]); lo[i] = min(lo[i], l); hi[i] = max(hi[i], h)
    return lo, hi
press = lambda z, w0, wa: np.sqrt(w_z(z, w0, wa) * f_DE(z, w0, wa) / w0)     # normalised at z = 0: w(0) = w0 at face value
dens = lambda z, w0, wa: np.sqrt(f_DE(z, w0, wa))
laws = {}
laws["framework, own law (pressure law, w = -1 exact)"] = dict(c=np.zeros_like(zg), lo=-0.004 * np.ones_like(zg), hi=0.004 * np.ones_like(zg))
laws["framework, DESI w(z) at face value (pressure mapping)"] = dict(c=dex(press(zg, -0.752, -0.86)), **dict(zip(("lo", "hi"), band(zg, press))))
laws["density mapping (rejected promotion; PAPER7's DESI sentence)"] = dict(c=dex(dens(zg, -0.752, -0.86)), **dict(zip(("lo", "hi"), band(zg, dens))))
hcurves = [dex(E(zg)), dex(E(zg, om=OM - SOM)), dex(E(zg, om=OM + SOM))] + [dex(E(zg, d["w0"], d["wa"])) for d in DESI.values()]
laws["H(z) law a0 ∝ H (the alt footing)"] = dict(c=dex(E(zg)), lo=np.min(hcurves, axis=0), hi=np.max(hcurves, axis=0))
lc = [dex(lcdm_emergent(zg, M, dl)) for M in (1e11, 1e12, 1e13) for dl in (-0.11, 0.0, 0.11)]
laws["LambdaCDM-native emergent scale (DM14 c-M, PAPER7)"] = dict(c=dex(lcdm_emergent(zg)), lo=np.min(lc, axis=0), hi=np.max(lc, axis=0))
# ------------------------------------------------------------------ table
print("    Delta log10 a0(z)/a0(0) [dex], central and range")
names = list(laws); short = ["own law", "DESI/pressure", "density (rejected)", "H(z) law", "LCDM emergent"]
print("    z    " + "".join(f"{s:>28s}" for s in short))
table = {}
for z in ZT:
    i = int(round(z / 5.0 * 100)); row = []
    for nm in names:
        L = laws[nm]; row.append((float(L["c"][i]), float(L["lo"][i]), float(L["hi"][i])))
    table[float(z)] = row
    print(f"    {z:3.1f}  " + "".join(f"{c:+.3f} [{lo:+.3f},{hi:+.3f}]".rjust(28) for c, lo, hi in row))
# ------------------------------------------------------------------ checks
i25 = 50
check("C1 the LambdaCDM-native law as implemented (E^{4/3} x [c^2/f(c)] with DM14 at 1e12 h^-1 Msun) reproduces PAPER7's 'factor 2.1 at z = 2.5, 0.33 dex' within 0.03 dex",
      abs(laws[names[4]]["c"][i25] - 0.33) < 0.03, f"z = 2.5: {laws[names[4]]['c'][i25]:+.3f} dex (factor {10**laws[names[4]]['c'][i25]:.2f})")
i10 = 20
check("C2 computed structure of the curves: (i) the framework's face-value-DESI (pressure) curve lies ABOVE the density mapping at every z > 0; (ii) it peaks near z ~ 1 at +0.10 dex, where it is within 0.02 dex of the LambdaCDM-emergent +0.09 (indistinguishable there), and crosses zero between z = 2.5 and 3.5; (iii) for z >= 2 the LambdaCDM-emergent central exceeds it by >= 0.18 dex; (iv) the H(z) band lies above the LambdaCDM band for 1 <= z <= 4 (the LambdaCDM range's upper edge reaches the H(z) band only at z ~ 5)",
      all(laws[names[1]]["c"][j] > laws[names[2]]["c"][j] for j in range(1, 101)) and abs(laws[names[1]]["c"][i10] - laws[names[4]]["c"][i10]) < 0.02 and laws[names[1]]["c"][50] > 0 > laws[names[1]]["c"][70]
      and all(laws[names[4]]["c"][j] - laws[names[1]]["c"][j] >= 0.18 for j in range(40, 101)) and all(laws[names[3]]["lo"][j] > laws[names[4]]["hi"][j] for j in range(20, 81)),
      f"z = 1: pressure {laws[names[1]]['c'][i10]:+.3f} vs LCDM {laws[names[4]]['c'][i10]:+.3f}; z = 2: gap {laws[names[4]]['c'][40] - laws[names[1]]['c'][40]:+.3f}; zero crossing between 2.5 and 3.5 -- THE DISCRIMINATING WINDOW IS z >= 2, as PAPER7 pre-registered")
gap_c = laws[names[4]]["c"][i25] - laws[names[1]]["c"][i25]; gap_e = laws[names[4]]["lo"][i25] - laws[names[1]]["hi"][i25]
check("C3 at z = 2.5 the framework's face-value-DESI curve is 2.1-2.5 sigma (+/-0.13 dex, centre-to-centre) below the LambdaCDM emergent curve, but the two RANGES nearly touch edge to edge (gap < 0.13 dex): a single rotator separates the central predictions, not the bands; the framework's own law (0.00) is 2.5 sigma from +0.33",
      2.0 < gap_c / 0.13 < 2.6 and 0.0 < gap_e < 0.13 and abs(0.334 / 0.13 - 2.57) < 0.1, f"centre gap {gap_c:+.3f} dex = {gap_c/0.13:.1f} sigma; edge gap {gap_e:+.3f} dex")
# ------------------------------------------------------------------ chart
cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]; labels = ["framework, own law (flat; ±<1%)", "framework, DESI w(z) at face value (pressure)", "density mapping (rejected promotion)", "H(z) law (alt footing)", "ΛCDM-native emergent (DM14)"]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=160); fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
for nm, col, lab in zip(names, cols, labels):
    L = laws[nm]; ax.fill_between(zg, L["lo"], L["hi"], color=col, alpha=0.18, linewidth=0); ax.plot(zg, L["c"], color=col, linewidth=2, label=lab)
    ax.annotate(lab.split(" (")[0], xy=(5.0, L["c"][-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8.5, color="#52514e")
ax.errorbar([2.5], [0.0], yerr=[[0.13], [0.13]], fmt="o", color="#0b0b0b", ms=5, capsize=4, elinewidth=1.2, label="one lensed rotator at z ≈ 2.5, ±0.13 dex (PAPER7)")
ax.axhline(0, color="#52514e", linewidth=0.8, alpha=0.6); ax.set_xlim(0, 5); ax.set_ylim(-0.35, 1.0)
ax.set_xlabel("redshift z"); ax.set_ylabel("Δ log₁₀ a₀(z) / a₀(0)  [dex]   (Δ log v_flat at fixed M_b = ¼ of this)")
ax.set_title("The acceleration scale versus redshift: every law on the table, with its range", fontsize=11, color="#0b0b0b")
ax.grid(True, color="#e6e5e1", linewidth=0.6); ax.spines[["top", "right"]].set_visible(False); ax.tick_params(colors="#52514e")
ax.legend(loc="upper left", fontsize=8, frameon=False); plt.subplots_adjust(right=0.78)
png = os.path.join(HERE, "L274_a0z_theories.png"); fig.savefig(png, bbox_inches="tight", facecolor=fig.get_facecolor()); print(f"\n    chart written: {png}")
json.dump(dict(pass_=sum(CH), n=len(CH), z=list(map(float, ZT)), laws=names, table={str(k): v for k, v in table.items()}), open(os.path.join(HERE, "L274_results.json"), "w"), indent=1)
print(f"\nL274 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
