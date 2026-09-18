#!/usr/bin/env python3
"""L276 -- REAL DATA versus every law: the acceleration scale (panel A) and the Tully-Fisher zero point (panel B), z = 0-5.

Panel A, Delta log10 a0(z)/a0(0): the model curves of L274 (framework own law; framework with DESI's w(z) at face value through the pressure law,
bands from the DESI chains via L275; the rejected density mapping; the H(z) law = the alt footing; the LambdaCDM-native emergent scale with the
DM14 range) against the only DIRECT multi-point measurement on the record, MUSE-DARK III (Ciocan, Bouche et al. 2026, A&A 709 L16,
arXiv:2604.22613): a0(z) = a0(0) + a1 z with a0(0) = 1.0 +/- 0.04, a1 = +1.59 +/- 0.105 (x1e-10 m/s^2) over z = 0.33-1.44, a0|z~1 = 2.38 +/- 0.11
(the numbers the repository fetched and banked in real_research/reviews/project_a0z_MUSE_DARK_III_confrontation.py); and the LambdaCDM
APPARENT a0 of Mayer et al. 2023 (Magneticum hydro, no fundamental a0; MNRAS 518, 257): RAR-fitted a0 rises ~x3 by z = 2 (one number on the record).
Panel B, the BTFR zero point Delta_b (mass axis at fixed velocity, dex, relative to local): the repository's 17-row ledger of published high-z
Tully-Fisher zero points (prep_2026/highz_tfr_fork/data_ledger.csv: Ubler+17, Tiley+16/19, Jeanneau+26, Mancera Pina+26, Straatman+17,
Amvrosiadis+25, Turner+17, Danhaive+26, ...), statistical and full systematic bars, against each law's per-sample prediction Delta_b = -dil x
Delta log a0(z) with the ledger's own linearised dilution dil = x/(2+x), x = a0/g_bar (only 7-55% of the a0 lever survives at g_bar = 0.5-6 a0), and
the ledger's LambdaCDM halo term.  Verdicts inherited from the record (FORK_RESULTS.md; A0Z_MUSE_DARK_III_CONFRONTATION.md), not re-litigated.
A FAIL is a finding."""
import os, csv, json, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L276 -- real data versus every law\n")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
# ------------------------------------------------------------------ the model curves (same code as L274; DESI bands from L275)
OM = 0.3027; OL = 1 - OM
f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
w_z = lambda z, w0, wa: w0 + wa * z / (1 + z)
E = lambda z, w0=-1.0, wa=0.0, om=OM: np.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w0, wa))
dex = lambda r: np.log10(r)
def dm14_c(z, M=1e12):
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z; return 10 ** (a + b * np.log10(M / 1e12))
fc = lambda c: np.log(1 + c) - c / (1 + c)
def lcdm_emergent(z, M=1e12, dlogc=0.0):
    c0 = dm14_c(0.0, M) * 10 ** dlogc; cz = dm14_c(z, M) * 10 ** dlogc
    return E(z) ** (4.0 / 3.0) * (cz ** 2 / fc(cz)) / (c0 ** 2 / fc(c0))
zg = np.linspace(0.0, 5.0, 101)
Bc = json.load(open(os.path.join(HERE, "L275_results.json")))["bands"]
def unionband(key):
    return (np.min([Bc[key][sn]["grid"]["lo"] for sn in Bc[key]], axis=0), np.max([Bc[key][sn]["grid"]["hi"] for sn in Bc[key]], axis=0), np.array(Bc[key]["desy5sn"]["grid"]["med"]))
laws = {}
laws["framework, own law (flat)"] = dict(c=np.zeros_like(zg), lo=-0.004 * np.ones_like(zg), hi=0.004 * np.ones_like(zg))
lo, hi, med = unionband("pressure"); laws["framework, DESI w(z) at face value (pressure law)"] = dict(c=med, lo=lo, hi=hi)
lo, hi, med = unionband("density"); laws["density mapping (rejected)"] = dict(c=med, lo=lo, hi=hi)
lo, hi, med = unionband("hz"); laws["H(z) law (alt footing)"] = dict(c=med, lo=lo, hi=hi)
lc = [dex(lcdm_emergent(zg, M, dl)) for M in (1e11, 1e12, 1e13) for dl in (-0.11, 0.0, 0.11)]
laws["ΛCDM emergent scale (DM14)"] = dict(c=dex(lcdm_emergent(zg)), lo=np.min(lc, axis=0), hi=np.max(lc, axis=0))
names = list(laws); cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
# ------------------------------------------------------------------ the data
MU_a00, MU_a00e, MU_a1, MU_a1e = 1.0, 0.04, 1.59, 0.105          # MUSE-DARK III fit, x1e-10, banked
zm = np.linspace(0.33, 1.44, 50); mu_c = dex((MU_a00 + MU_a1 * zm) / MU_a00)
mu_lo = dex((MU_a00 - MU_a00e + (MU_a1 - MU_a1e) * zm) / (MU_a00 + MU_a00e)); mu_hi = dex((MU_a00 + MU_a00e + (MU_a1 + MU_a1e) * zm) / (MU_a00 - MU_a00e))
mu_pt = (1.0, dex(2.38), dex(2.38 + 0.11) - dex(2.38))             # a0|z~1 = 2.38 +/- 0.11 vs a0(0) = 1.0
mayer = (2.0, dex(3.0))                                             # Mayer+2023 LCDM apparent a0: x3 by z = 2
rows = list(csv.DictReader(open(os.path.join(ROOT, "prep_2026", "highz_tfr_fork", "data_ledger.csv"))))
def fl(x):
    try: return float(x)
    except Exception: return np.nan
data = []
for r in rows:
    z, db, st, sy, dil = fl(r["z_eff"]), fl(r["delta_b_dex_mass_axis"]), fl(r["stat_err_dex"]), fl(r["sys_est_dex"]), fl(r["dilution_typ"])
    if np.isnan(db) or np.isnan(st): continue
    data.append(dict(study=r["study"], z=z, rel=r["relation"], db=db, st=st, sy=(0.0 if np.isnan(sy) else sy), dil=dil, gb=fl(r["gbar_over_a0_typ"]), use=r["usable_for_fork"], lcdm=fl(r["lcdm_halo_term"])))
# per-sample model predictions on the BTFR axis: Delta_b = -dil * Delta log a0(z)   (mass at fixed velocity falls when a0 rises)
def at(z, arr): return float(np.interp(z, zg, arr))
for d in data:
    d["pred"] = {nm: -d["dil"] * at(d["z"], laws[nm]["c"]) for nm in names}
    d["pred"]["H(z) law, undiluted"] = -at(d["z"], laws[names[3]]["c"])
# ------------------------------------------------------------------ table
print("=" * 118); print("PANEL B TABLE -- published BTFR/TFR zero points (mass axis, dex vs local) and each law's per-sample prediction (diluted)"); print("=" * 118)
print(f"    {'study':16s} {'z':>4s} {'rel':5s} {'g_bar/a0':>8s} {'dil':>5s} {'measured':>18s} | {'flat':>6s} {'DESI/press':>10s} {'density':>8s} {'H(z) dil':>9s} {'H(z) undil':>10s} {'LCDM emg':>9s} {'LCDM halo(ledger)':>17s}")
for d in sorted(data, key=lambda x: (x["z"], x["study"])):
    p = d["pred"]
    print(f"    {d['study'][:16]:16s} {d['z']:4.1f} {d['rel'][:5]:5s} {d['gb']:8.1f} {d['dil']:5.2f} {d['db']:+6.2f} ±{d['st']:.2f} ±{d['sy']:.2f}sys | {p[names[0]]:+6.3f} {p[names[1]]:+10.3f} {p[names[2]]:+8.3f} {p[names[3]]:+9.3f} {p['H(z) law, undiluted']:+10.3f} {p[names[4]]:+9.3f} {d['lcdm']:+17.3f}")
OUT["panelB"] = [dict(study=d["study"], z=d["z"], rel=d["rel"], db=d["db"], stat=d["st"], sys=d["sy"], dil=d["dil"], pred=d["pred"], lcdm_ledger=d["lcdm"]) for d in data]
# ------------------------------------------------------------------ checks (computed statements about the comparison)
btfr = [d for d in data if d["rel"].startswith("bTFR")]
def pull(d, nm):
    e = math.sqrt(d["st"] ** 2 + d["sy"] ** 2); return (d["db"] - d["pred"][nm]) / e
pulls = {nm: [pull(d, nm) for d in btfr] for nm in names}
check("B1 with the full systematic budget every bTFR row is within 2 sigma of EVERY law's diluted prediction (the fork separations of 0.02-0.15 dex per sample sit inside +/-0.27-0.35 dex bands): the archival BTFR arm is UNDECIDED, as FORK_RESULTS records",
      all(abs(p) < 2.0 for v in pulls.values() for p in v), "max |pull| per law: " + ", ".join(f"{nm.split(' (')[0]} {max(abs(p) for p in v):.1f}" for nm, v in pulls.items()))
j = [d for d in btfr if d["study"].startswith("Jeanneau")][0]; u = [d for d in btfr if d["study"].startswith("Ubler") and d["z"] < 1.5][0]
check("B2 the two bTFR points at the SAME redshift z = 0.9 disagree with each other by more than their combined statistical errors (Jeanneau+26 0.00 +/- 0.06 vs Ubler+17 -0.44 +/- 0.04): the data are internally inconsistent at the level of the effect, which is the record's reason the arm is a wash",
      abs(j["db"] - u["db"]) / math.sqrt(j["st"] ** 2 + u["st"] ** 2) > 3.0, f"{abs(j['db']-u['db']):.2f} dex apart = {abs(j['db']-u['db'])/math.sqrt(j['st']**2+u['st']**2):.1f} sigma (stat)")
mu_dex_z1 = mu_pt[1]; sep = {nm: (mu_dex_z1 - at(1.0, laws[nm]["c"])) for nm in names}
check("A1 MUSE-DARK III's fitted a0 at z ~ 1 (+0.38 dex) lies ABOVE every law on the chart, including the H(z) law (+0.25) and the LambdaCDM emergent scale (+0.09): taken as a fundamental a0 it would exclude the flat law by ~19 sigma of its quoted error -- and it exceeds the rivals too, which is why the record reads it as an APPARENT a0 (Mayer+2023: LambdaCDM hydro with no fundamental a0 gives a RAR-fitted a0 rising x3 by z = 2), method-localised, non-diagnostic",
      all(v > 0.1 for v in sep.values()) and (mu_dex_z1 - 0.0) / mu_pt[2] > 15, "MUSE z~1 minus each law: " + ", ".join(f"{nm.split(' (')[0]} {v:+.2f}" for nm, v in sep.items()) + f"; flat excluded at {mu_dex_z1/mu_pt[2]:.0f} sigma at face value")
check("A2 the ONE direct measurement therefore separates none of the laws from each other on the chart: the gap between it and the nearest law (0.13 dex) is comparable to the spread among the laws at z = 1 (0.25 dex), and the record's ledger of BTFR zero points cannot resolve 0.1 dex -- the decisive observation remains the pre-registered deep-MOND rotator at z ~ 2.5 (PAPER7)",
      min(sep.values()) > 0.1 and (max(at(1.0, laws[nm]["c"]) for nm in names) - min(at(1.0, laws[nm]["c"]) for nm in names)) > 0.2)
# ------------------------------------------------------------------ chart
fig, (ax, bx) = plt.subplots(2, 1, figsize=(11.5, 11), dpi=160, gridspec_kw=dict(height_ratios=[1.15, 1.0], hspace=0.28)); fig.patch.set_facecolor("#fcfcfb")
for a in (ax, bx): a.set_facecolor("#fcfcfb"); a.grid(True, color="#e6e5e1", linewidth=0.6); a.spines[["top", "right"]].set_visible(False); a.tick_params(colors="#52514e")
for nm, col in zip(names, cols):
    L = laws[nm]; ax.fill_between(zg, L["lo"], L["hi"], color=col, alpha=0.16, linewidth=0); ax.plot(zg, L["c"], color=col, linewidth=2, label=nm)
    ax.annotate(nm.split(" (")[0], xy=(5.0, L["c"][-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8, color="#52514e")
ax.fill_between(zm, mu_lo, mu_hi, color="#0b0b0b", alpha=0.10, linewidth=0); ax.plot(zm, mu_c, color="#0b0b0b", linewidth=2.2, linestyle="--", label=r"DATA: MUSE-DARK III 2026 RAR-fitted $a_0(z)=1.0+1.59z$ (z = 0.33-1.44)")
ax.errorbar([mu_pt[0]], [mu_pt[1]], yerr=[[mu_pt[2]], [mu_pt[2]]], fmt="s", color="#0b0b0b", ms=6, capsize=4, label=r"DATA: MUSE-DARK III $a_0|_{z\simeq1}=2.38\pm0.11$ ($\times10^{-10}$)")
ax.plot([mayer[0]], [mayer[1]], marker="D", color="#e87ba4", ms=8, markeredgecolor="#0b0b0b", linestyle="none", label=r"$\Lambda$CDM hydro, APPARENT $a_0$ (Mayer+2023): $\times3$ by z = 2, no fundamental $a_0$")
ax.errorbar([2.5], [0.0], yerr=[[0.13], [0.13]], fmt="o", color="#52514e", ms=5, capsize=4, elinewidth=1.2, label=r"pre-registered target: one deep-MOND rotator at $z\simeq2.5$, $\pm0.13$ dex (no data yet)")
ax.axhline(0, color="#52514e", linewidth=0.8, alpha=0.6); ax.set_xlim(0, 5); ax.set_ylim(-0.42, 1.36)
ax.set_ylabel(r"$\Delta\log_{10}\,a_0(z)/a_0(0)$  [dex]"); ax.set_title("A.  The acceleration scale: every law, and the one direct measurement", fontsize=11, loc="left")
ax.legend(loc="upper left", fontsize=7.6, frameon=False)
# panel B: data points + per-sample predictions
for d in data:
    x = d["z"] + (0.04 if d["rel"].startswith("bTFR") else -0.04); mk = "o" if d["rel"].startswith("bTFR") else "^"; fc_ = "#0b0b0b" if d["rel"].startswith("bTFR") else "white"
    bx.errorbar([x], [d["db"]], yerr=[[math.sqrt(d["st"] ** 2 + d["sy"] ** 2)], [math.sqrt(d["st"] ** 2 + d["sy"] ** 2)]], fmt="none", ecolor="#52514e", elinewidth=0.8, alpha=0.45, capsize=0)
    bx.errorbar([x], [d["db"]], yerr=[[d["st"]], [d["st"]]], fmt=mk, color="#0b0b0b", markerfacecolor=fc_, ms=6, capsize=3, elinewidth=1.2)
    for nm, col in zip(names, cols):
        if nm.startswith("density"): continue
        bx.plot([x], [d["pred"][nm]], marker="_", color=col, ms=11, markeredgewidth=2.2, linestyle="none", alpha=0.95)
    bx.plot([x], [d["lcdm"]], marker="_", color="#7a2c4e", ms=11, markeredgewidth=2.2, linestyle="none", alpha=0.95)
bx.errorbar([], [], fmt="o", color="#0b0b0b", label="published bTFR zero point (stat; faint bar = stat ⊕ full systematic)"); bx.errorbar([], [], fmt="^", color="#0b0b0b", markerfacecolor="white", label="published stellar-TFR zero point")
for nm, col in zip(names, cols):
    if not nm.startswith("density"): bx.plot([], [], marker="_", color=col, ms=11, markeredgewidth=2.2, linestyle="none", label=f"prediction: {nm.split(' (')[0]} (diluted by the sample's lever)")
bx.plot([], [], marker="_", color="#7a2c4e", ms=11, markeredgewidth=2.2, linestyle="none", label="prediction: ΛCDM halo scaling (ledger term)")
bx.axhline(0, color="#52514e", linewidth=0.8, alpha=0.6); bx.set_xlim(0, 5.3); bx.set_ylim(-1.55, 0.45)
bx.set_xlabel("redshift  z"); bx.set_ylabel(r"$\Delta_b$ = BTFR zero point, mass axis at fixed velocity  [dex vs local]")
bx.set_title("B.  The observable: 17 published high-z Tully–Fisher zero points against each law's per-sample prediction", fontsize=11, loc="left")
bx.legend(loc="lower left", fontsize=7.4, frameon=False, ncol=2)
bx.text(5.25, 0.38, "at g_bar = 0.5–6 a₀ only 7–55% of an a₀ shift reaches the zero point\n(dilution x/(2+x)); systematics ±0.2–0.5 dex; z = 0.9 points disagree with each other", fontsize=7.4, color="#52514e", ha="right", va="top")
png = os.path.join(HERE, "L276_data_vs_models_a0z.png"); fig.savefig(png, bbox_inches="tight", facecolor=fig.get_facecolor()); print(f"\n    chart written: {png}")
json.dump(dict(pass_=sum(CH), n=len(CH), **OUT), open(os.path.join(HERE, "L276_results.json"), "w"), indent=1, default=str)
print(f"\nL276 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
print("""VERDICT (inherited from the record, restated on one chart).  (A) The one direct multi-point measurement of a0(z), MUSE-DARK III, rises
far above EVERY law -- taken as a fundamental a0 it excludes the flat law, the H(z) law and the LambdaCDM emergent scale alike -- which is
why the record reads it as an APPARENT a0 (LambdaCDM hydro without any a0 produces the same rise, Mayer+2023), method-localised to
RAR fits on intermediate-z star-forming disks, and non-diagnostic.  (B) The 17 published Tully-Fisher zero points are diluted by 45-93%
at the accelerations they probe, carry +/-0.2-0.5 dex systematics, and disagree among themselves at fixed z: every law fits them.
Nothing in hand confirms or refutes the framework's novel prediction (flat, or +0.01..+0.06 dex with DESI at face value); nothing in hand
favours it over LambdaCDM either.  The decisive datum is still the pre-registered deep-MOND rotator at z ~ 2.5.  Nothing here derives kappa.""")
