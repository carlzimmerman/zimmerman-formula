"""PAPER44 figures + numbers. Parsed from committed outputs (sonnet55_push/cold_mass/cm14b, cm15; sonnet55_push/puzzle_32pi/p57, p58) and recomputed curves
from the same scripts' setup (read-only). Writes fig1_paper44_satellites.pdf, fig2_paper44_widebinaries.pdf, PAPER44_figures_numbers.json."""
import json, math, os, re, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); CM = os.path.join(H, "..", "..", "sonnet55_push", "cold_mass"); PZ = os.path.join(H, "..", "..", "sonnet55_push", "puzzle_32pi")
rd = lambda d, f: open(os.path.join(d, f)).read()
o15, o14b, o58, o57 = rd(CM, "cm15_sw01_rule_vs_satellites.out"), rd(CM, "cm14b_sifon_table.out"), rd(PZ, "p58_cassini_kappa_bound.out"), rd(PZ, "p57_etno_secular_nbody.out")
m = {}
m["chi2_noEFE"], m["chi2_SW01"], m["chi2_linear"] = [float(re.search(rf"{k}\s*:\s*chi2\s+([\d.]+)/5", o15).group(1)) for k in ("A no EFE", "D SW01 quadrature EFE", "B linear EFE")]
m["chi2_ownership"] = float(re.search(r"C ownership: no phantom : pulls .*?chi2 ([\d.]+)/5", o14b).group(1))
m["offset_noEFE"] = float(re.search(r"A full MOND boost .*?mean log offset ([+-][\d.]+) dex", o14b).group(1))
m["offset_EFE"] = float(re.search(r"B boost with host EFE .*?mean log offset ([+-][\d.]+) dex", o14b).group(1))
m["offset_own"] = float(re.search(r"C ownership: no phantom .*?mean log offset ([+-][\d.]+) dex", o14b).group(1))
etas = [float(x) for x in re.findall(r"eta ([\d.]+):", o15)]; xs = [float(x) for x in re.findall(r"x ([\d.]+), eta", o15)]
m["eta_range"] = [min(etas), max(etas)]; m["x_range"] = [min(xs), max(xs)]
m["rbg_range"] = [int(min(map(int, re.findall(r"r_bg\s+(\d+) kpc", o14b)))), int(max(map(int, re.findall(r"r_bg\s+(\d+) kpc", o14b))))]
m["Q2_half"] = float(re.search(r"a0 = 9.360e-11\s+kappa = 0.500\s+Q2 = ([\d.e+-]+)", o58).group(1))
m["Q2_sig_half"] = float(re.search(r"kappa = 0.500\s+Q2 = [\d.e+-]+ s\^-2\s+\(([+-][\d.]+) sigma\)", o58).group(1))
m["kappa_max_2s"] = float(re.search(r"Cassini 2 sigma: a0 < [\d.e+-]+ m/s\^2, kappa < ([\d.]+)", o58).group(1))
m["noEFE_dq"] = float(re.search(r"C2 MOND without the external field leaves q unchanged vs Newton: max \|dq\| = ([\d.]+) AU", o57).group(1))
occ = dict(re.findall(r"(K[0-3]): final .*?detached occupancy ([\d.]+)", o57)); m["occ"] = {k: float(v) for k, v in occ.items()}
# wide-binary prediction (isolated MOND, no EFE) vs the SW01 magnitude rule at the solar eta and Newton; 1.5 Msun total, 3-D r ~ projected s (approximation)
G, Msun, AU, a0 = 6.674e-11, 1.989e30, 1.495978707e11, 9.3603e-11
nu = lambda y: math.sqrt(1 + 1 / y); eta_sun = 2.146e-10 / a0 * 0.0 + 1.85   # the record's solar eta (Newtonian Galactic field / a0, y_e = 1.847 canonical, p57)
s = np.geomspace(1e3, 3e4, 60)
y = G * 1.5 * Msun / (s * AU)**2 / a0
gam_iso = np.sqrt([nu(v) for v in y]); gam_sw01 = np.sqrt([nu(math.sqrt(v * v + eta_sun**2)) / nu(eta_sun) * nu(eta_sun) for v in y])
m["gamma_iso"] = {str(int(k)): round(float(np.sqrt(nu(G * 1.5 * Msun / (k * AU)**2 / a0))), 3) for k in (2000, 5000, 10000, 20000)}
m["gamma_sw01_20k"] = round(float(math.sqrt(nu(math.sqrt((G * 1.5 * Msun / (2e4 * AU)**2 / a0)**2 + eta_sun**2)))), 3)
json.dump(m, open(os.path.join(H, "PAPER44_figures_numbers.json"), "w"), indent=1)
INK, MUTED, C1, C2, C3 = "#1f1f1e", "#6f6e69", "#2a78d6", "#eb6834", "#4a9b5f"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})
# fig 1: satellites
sys.argv = ["x"]; ns = {"__file__": os.path.join(CM, "cm14b_sifon_table.py")}
exec(rd(CM, "cm14b_sifon_table.py").split("rows = {")[0].replace("print(f\"   parsed", "pass  # print(f\"   parsed"), ns)
fig, ax = plt.subplots(figsize=(5.4, 3.4))
lm = np.array(ns["mstar"]); mb = np.array([v[0] for v in ns["mbg"]]); el = np.array([v[1] for v in ns["mbg"]]); eh = np.array([v[2] for v in ns["mbg"]])
ax.errorbar(lm, mb, yerr=[el, eh], fmt="o", color=INK, ms=4, capsize=2, label="lensing $m_{\\rm bg}$ (Sifón+2018)")
grid = np.linspace(9.4, 11.1, 40)
def pred(lms, mode):
    out = []
    for l in lms:
        Mb = 1.2 * 10**l; ret = 0.13 * (0.12 / 0.02237) * Mb; mbv = 10**np.interp(l, lm, mb); R = np.interp(l, lm, ns["rsat"])
        rbg = (mbv / (4 * math.pi * ns["rho_h"](R)))**(1 / 3); x = ns["G"] * Mb * ns["Msun"] / (rbg * ns["Mpc"])**2 / ns["a0"]
        e = ns["G"] * ns["Mh"](R) * ns["Msun"] / (R * ns["Mpc"])**2 / ns["a0"]
        v = {"iso": nu(x), "sw01": nu(math.sqrt(x * x + e * e)), "own": 1.0}[mode]; out.append(math.log10(v * Mb + ret))
    return np.array(out)
for mode, c, lab in (("iso", C1, "no external-field effect"), ("sw01", C2, "magnitude EFE (SW01 rule)"), ("own", C3, "no phantom (ownership)")):
    ax.plot(grid, pred(grid, mode), color=c, lw=1.6, label=lab)
ax.set_xlabel("$\\log_{10} M_*/M_\\odot$"); ax.set_ylabel("$\\log_{10}$ mass inside $r_{\\rm bg}$ / $M_\\odot$"); ax.legend(frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(H, "fig1_paper44_satellites.pdf")); plt.close(fig)
fig, ax = plt.subplots(figsize=(5.4, 3.0))
ax.plot(s / 1e3, gam_iso, color=C1, lw=1.6, label="no EFE (isolated MOND)"); ax.plot(s / 1e3, [math.sqrt(nu(math.sqrt(v * v + eta_sun**2))) for v in y], color=C2, lw=1.6, label="SW01 magnitude rule, $\\eta_\\odot=1.85$")
ax.axhline(1.0, color=MUTED, lw=1, ls="--", label="Newton"); ax.set_xscale("log"); ax.set_xlabel("separation (kAU), $M_{\\rm tot}=1.5\\,M_\\odot$"); ax.set_ylabel("$\\gamma_v=\\sqrt{\\nu}$")
ax.legend(frameon=False, fontsize=7.5); fig.tight_layout(); fig.savefig(os.path.join(H, "fig2_paper44_widebinaries.pdf")); plt.close(fig)
print(json.dumps(m, indent=1))
