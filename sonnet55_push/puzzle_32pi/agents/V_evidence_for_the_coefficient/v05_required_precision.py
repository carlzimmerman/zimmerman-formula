#!/usr/bin/env python3
"""v05_required_precision.py -- what precision on a0 (and on H) would discriminate the declared candidates, what the present budget is, and what the
listed future measurements can and cannot do.  Requirement calculations only: I do not have, and do not invent, forecasts for Gaia DR4 or JWST.

 A  pairwise separations of the declared Z values and the total fractional error needed for an n-sigma separation and for an expected Bayes factor
 B  subtract the H0 / Omega_Lambda floor: the required precision on a0 ALONE (and when it is impossible)
 C  present a0 error budget (v01/v02) against the requirement
 D  wide binaries: how accurately the boost must be measured (and the EFE modelled) to fix a0 to the required fraction
 E  a0(z): what a z ~ 0.9 - 2.5 measurement can and cannot say about Z
 F  the figure: posterior of Z under both footings
Exit 0 = every check held.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_common import *
import importlib.util
spec = importlib.util.spec_from_file_location("v00", os.path.join(os.path.dirname(os.path.abspath(__file__)), "v00_declared_hypotheses.py"))
v00 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v00)
ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
r1, r2, r3 = json.load(open("v01_results.json")), json.load(open("v02_results.json")), json.load(open("v03_results.json"))
res = {}
Zd = {h[0].split()[0]: h[1] for h in v00.HYPOTHESES if h[3] == "candidate"}

# ---------------------------------------------------------------- A
print("A  separations of the declared candidates and the total fractional error s_tot needed")
pairs = [("F", "V"), ("F", "M"), ("F", "N"), ("F", "P"), ("V", "M"), ("F", "K1")]
print(f"   {'pair':<8}{'Z_i':>8}{'Z_j':>8}{'|dZ|/Z (%)':>12}{'s for 2 sigma':>15}{'s for 3 sigma':>15}{'s for E[BF]=3':>15}{'s for E[BF]=10':>16}")
A = {}
for i, j in pairs:
    d = abs(math.log(Zd[j] / Zd[i])); pct = 100 * (max(Zd[i], Zd[j]) / min(Zd[i], Zd[j]) - 1)
    s2, s3 = d / 2, d / 3
    sb3, sb10 = d / math.sqrt(2 * math.log(3)), d / math.sqrt(2 * math.log(10))       # expected ln BF = d^2/(2 s^2) = ln BF
    A[f"{i}-{j}"] = dict(d=d, pct=pct, s2=s2, s3=s3, sb3=sb3, sb10=sb10)
    print(f"   {i+'-'+j:<8}{Zd[i]:>8.4f}{Zd[j]:>8.4f}{pct:>12.2f}{100*s2:>14.2f}%{100*s3:>14.2f}%{100*sb3:>14.2f}%{100*sb10:>15.2f}%")
check(abs(A["F-V"]["pct"] - 3.64) < 0.02 and abs(A["F-M"]["pct"] - 8.54) < 0.02, "A1 the brief's numbers reproduce: 6 vs 5.789 is 3.6%, 2 pi vs 5.789 is 8.5%")
check(abs(A["F-V"]["s2"] - 0.0179) < 2e-4, "A2 a 2-sigma F-V separation needs s_tot = 1.8% (a0 and H combined)")
res["A"] = A

# ---------------------------------------------------------------- B
print("\nB  subtract the H floor: required precision on a0 ALONE, s_a = sqrt(s^2 - s_H^2)")
floors = {"H0 Planck 67.4+-0.5 (rho_tot footing)": 0.5 / 67.4,
          "H0 SH0ES 73.0+-1.0 (rho_tot)": 1.0 / 73.0,
          "H0 Planck + Omega_L 0.685+-0.007 (rho_Lambda footing)": math.hypot(0.5 / 67.4, 0.5 * 0.007 / 0.685),
          "H0 tension unresolved: half-difference 2.8/70.2": 2.8 / 70.2}
print(f"   {'H floor':<58}{'s_H':>7}   " + "   ".join(f"{p+' 2s':>10}" for p in ("F-V", "F-M", "V-M")) + "   (required s_a for a 2-sigma separation; 'none' = the floor already exceeds it)")
B = {}
for fk, sH in floors.items():
    row = []
    for p in ("F-V", "F-M", "V-M"):
        s2 = A[p]["s2"]; sa = math.sqrt(s2 ** 2 - sH ** 2) if s2 > sH else None
        row.append(sa); B[f"{fk}|{p}"] = sa
    print(f"   {fk:<58}{100*sH:>6.2f}%   " + "   ".join(f"{('%.2f%%' % (100*x)) if x else 'none':>10}" for x in row))
check(B["H0 tension unresolved: half-difference 2.8/70.2|F-V"] is None and B["H0 tension unresolved: half-difference 2.8/70.2|F-M"] is not None,
      "B1 with the H0 tension unresolved, NO a0 precision can separate 5.79 from 6 (the floor 4.0% exceeds the 1.8% needed); 5.79 from 2 pi would need 3.5%")
check(B["H0 Planck 67.4+-0.5 (rho_tot footing)|F-V"] is not None and abs(B["H0 Planck 67.4+-0.5 (rho_tot footing)|F-V"] - 0.0163) < 1e-3, "B2 with Planck H0 the F-V separation needs s_a = 1.6% on a0")
res["B"] = {k: v for k, v in B.items()}

# ---------------------------------------------------------------- C
print("\nC  present a0 error components (fractions of a0) against the requirement")
bud = r2["budget"]
comp = [("statistical, points-independent (fine grid)", r2["record_pl"]["sig_ln_ind"]), ("statistical, galaxy bootstrap", r2["record_pl"]["sig_ln_bootstrap"]),
        ("Desmond 2023 published total (stat + sys)", math.hypot(0.04, 0.09) / 1.19), ("MLS16 published total", math.hypot(0.02, 0.24) / 1.2),
        ("ensemble E analysis-choice scatter", r1["E"]["sd_ln"])] + [(k, v) for k, v in bud.items()]
for k, v in comp:
    print(f"   {k:<80}{100*v:6.1f}%   = {v/A['F-V']['s2']:5.1f} x the 1.8% needed for F-V at 2 sigma;  {v/A['F-M']['s2']:5.1f} x the 4.1% for F-M")
best_now = math.hypot(0.04, 0.09) / 1.19
print(f"   best published total ({100*best_now:.1f}%) must improve by x{best_now/(A['F-V']['s2']*0.9):.1f} to separate F from V at 2 sigma (Planck H0), by x{best_now/math.sqrt(A['F-M']['s2']**2-floors['H0 Planck 67.4+-0.5 (rho_tot footing)']**2):.1f} for F from 2 pi")
res["C"] = dict(comp)

# ---------------------------------------------------------------- D wide binaries
print("\nD  wide binaries: sensitivity of the boost nu = g_obs/g_N to a0, for the IFs of v_common (y = g_N/a0)")
print("   (wide binaries are NOT an a0 measurement by themselves: they probe nu(y) at y ~ 0.1-3 inside the MW's external field; this is only the sensitivity)")
ys = [0.03, 0.1, 0.3, 1.0, 3.0]
print(f"   {'IF':<26}" + "".join(f"   y={y:<5}" for y in ys) + "     [d ln nu / d ln a0 at fixed g_N]")
sens = {}
for nm, F in IFS.items():
    row = []
    for y in ys:
        gN = 1.0; a0 = gN / y; h = 1e-4
        sl = (math.log(F(np.array([gN]), a0 * (1 + h))[0]) - math.log(F(np.array([gN]), a0 * (1 - h))[0])) / (math.log(1 + h) - math.log(1 - h))
        row.append(sl)
    sens[nm] = row
    print(f"   {nm:<26}" + "".join(f"{v:>+9.3f} " for v in row))
alpha1_analytic = [0.5 / (1 + y) for y in ys]        # nu = sqrt(1+1/y): d ln nu/d ln a0 = 1/(2(1+y))
check(np.allclose(sens["alpha1 (record kernel)"], alpha1_analytic, atol=1e-6), "D1 numerical sensitivity of the alpha1 kernel equals the analytic 1/(2(1+y))")
sl_mid = np.mean([abs(sens[nm][2]) for nm in IFS])        # y = 0.3
sl_hi = np.mean([abs(sens[nm][4]) for nm in IFS])          # y = 3
need = A["F-V"]["s2"]
print(f"   to fix a0 to {100*need:.1f}% (2-sigma F-V) from the boost at y ~ 0.3 the boost must be known to {100*need*sl_mid:.1f}% (sensitivity {sl_mid:.2f}), at y ~ 3 to {100*need*sl_hi:.1f}% (sensitivity {sl_hi:.2f});")
print(f"   for F-M (4.1%): {100*A['F-M']['s2']*sl_mid:.1f}% at y ~ 0.3.  The boost must also be independent of the external-field model, the interpolating function and the triple/contamination fraction at that level.")
print("   I make no claim about what DR4 will achieve; the requirement is what any wide-binary analysis would have to beat.")
check(sl_mid < 0.5 and sl_hi < sl_mid, "D2 the boost is LESS sensitive to a0 than a0 itself is to the data (slope < 0.5 and falling with y): a percent-level a0 needs a sub-percent boost")
res["D"] = dict(sens={k: v for k, v in sens.items()}, boost_precision_FV=need * sl_mid, boost_precision_FM=A["F-M"]["s2"] * sl_mid)

# ---------------------------------------------------------------- E a0(z)
print("\nE  a0(z): what evolution measurements bear on Z")
def Ez(z, Om=0.315): return math.sqrt(Om * (1 + z) ** 3 + (1 - Om))
for z in (0.9, 2.5):
    print(f"   z = {z}: E(z) = {Ez(z):.3f}  -> a0(z)/a0(0) = 1 (flat, rho_Lambda footing) or {Ez(z):.3f} (tracks cH(z), rho_total footing), a {math.log10(Ez(z)):.3f} dex difference")
print("   (the record's a0_of_z.csv also carries a z = 0.05 point, 1.69 +- 0.13, attributed to a 2025 paper that I have NOT opened; it is not used here)")
nm, z, a, s = "MUSE-DARK-III 2026, arXiv:2604.22613 (abstract / HTML summary; local intercept a0(0) = 1.0 +-0.04 in their linear fit, 1.2 +-0.26 adopted as z = 0 reference)", 0.9, 2.38, 0.11
for lab, pred in (("flat, a0(0) = ensemble E 1.097", 1.0974), ("cH(z): 1.097 x E(z)", 1.0974 * Ez(z)), ("their own intercept 1.0 x E(z)", 1.0 * Ez(z))):
    print(f"   MUSE-DARK-III z={z}: measured {a:.2f}+-{s:.2f} vs {lab} = {pred:.2f}: {(a-pred)/s:+.1f} sigma (measurement error only; their systematics: gas mass ~0.2 dex, disc-halo decomposition)")
print("   -> if a z ~ 1 value near 2.4 stands, BOTH z-laws are strained (flat by a factor ~2; cH(z) by ~1.3); that is a question about the footing / evolution law, not about Z = 5.79 vs 6.")
print("      I do not evaluate that claim here (the record's own standing on MUSE is 'non-diagnostic'); it is listed because it bears on which H the coefficient multiplies.")
print("      A z = 2.5 point at single-object precision (0.13 dex = 35%, record eq03) cannot separate Z values 4% apart; it separates the two footings (0.576 dex).")
check(abs(Ez(2.5, 0.3138) - 3.7604) < 1e-3 and abs(Ez(2.5) - 3.767) < 1e-3, "E1 E(2.5) = 3.760 (Om_m = 0.3138) / 3.767 (Om_m = 0.315) reproduce the record's eq03 / ChainCert values")
res["E"] = dict(E09=Ez(0.9), E25=Ez(2.5))

# ---------------------------------------------------------------- F figure
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    a_sc = r3["scenarios"]
    zz = np.linspace(3, 9, 600)
    for ax, foot, HH in ((axs[0], "tot", H_si(67.4)), (axs[1], "Lam", H_si(67.4) * math.sqrt(OM_L))):
        for sk, col in (("REC-quoted   (record PL, its own 5.44%)", "C3"), ("ENSEMBLE E   (9 analysis choices)", "C0"), ("MLS16        (1.20 +-0.02 +-0.24)", "C2")):
            a, s = a_sc[sk]["a0"], a_sc[sk]["s_a"]
            mu = math.log(c_si * HH / a); pdf = np.exp(-0.5 * ((np.log(zz) - mu) / s) ** 2) / (s * zz * math.sqrt(2 * math.pi))
            ax.plot(zz, pdf, color=col, label=f"{sk.split('(')[0].strip()} ({100*s:.0f}%)")
        for nm, zv, ls in (("F 5.789", Zd["F"], "-"), ("V 6", 6.0, "--"), ("M 2$\\pi$", Z_M, ":"), ("N 3$\\sqrt{3}$", Zd["N"], "-.")):
            ax.axvline(zv, color="k", ls=ls, lw=0.8); ax.text(zv, 0.0, " " + nm, rotation=90, va="bottom", fontsize=7)
        ax.set_title(("rho_total footing: Z = c H0 / a0" if foot == "tot" else "rho_Lambda footing: Z = c H0 sqrt(Omega_L) / a0") + " (H0 = 67.4)", fontsize=9)
        ax.set_xlabel("Z")
    axs[0].set_ylabel("posterior density (flat in ln Z)"); axs[0].legend(fontsize=7)
    plt.tight_layout(); plt.savefig("v_Z_posteriors.png", dpi=130); print("\nF  figure written: v_Z_posteriors.png")
except Exception as e:
    print("F  figure skipped:", e)

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
json.dump(res, open("v05_results.json", "w"), indent=1, default=float)
sys.exit(0 if all(ok) else 1)
