"""Column 0, 'Relativistic theory (the chassis)': one picture per tile. Plot and read only; no physics is rerun.

Every plotted number is read from a committed lane file (paths in SRC). Thresholds are the lanes' own frozen lines.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import menu_style as ms  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

R = ms.ROOT
SRC = {
    "C5": "covariant_push_2026_10_22/C5_health/c5_health_results.json",
    "C8": "covariant_push_2026_10_22/C8_instantaneous/c8_instantaneous_results.json",
    "P3": "rebuild_2026_10_22/P3_v3_strong_field/p3_v3_strong_field_results.json",
    "X3": "rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness_results.json",
    "SS": "reviews/v3s_soft_side_strong_coupling_2026_10_23/soft_side_sc_results.json",
    "C6": "covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json",
    "E2": "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json",
    "G9": "campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0_results.json",
}
J = {k: json.load(open(R / v)) for k, v in SRC.items()}
FOOT = {"canonical": ms.DATA, "alt": "#7a5195"}


def logbar(ax, labels, vals, colors, xlabel, fmt="{:.2e}"):
    y = np.arange(len(vals))[::-1]
    ax.barh(y, vals, color=colors, height=0.6, left=0)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlabel(xlabel)
    for yi, v in zip(y, vals):
        ax.text(v * 1.6, yi, fmt.format(v), va="center", fontsize=7.5, color=ms.INK)
    ax.grid(axis="y", visible=False)
    return y


# ---------------------------------------------------------------- 01 gravity waves at light speed
def fig01():
    p3, c5 = J["P3"], J["C5"]["H4"]
    tensor = [float(w) for w in c5["C4-literal + BS dust (mu^-1=100 kpc) | y=1"]["w2_over_k2"]]
    rows = [("lab (Eot-Wash 38.6 um)", "Eot-Wash (38.6 um)|canonical|24pc"), ("planets, 1 AU", "planets (1 AU)|canonical|24pc"),
            ("double pulsar", "double pulsar|canonical|24pc"),
            ("galaxy, 1 kpc", "galaxy (1 kpc; phantom 0.01 Msun/pc^3, ILLUSTRATIVE)|canonical|24pc"),
            ("stellar BH at 3M", "BH10 (r = 3M)|canonical|24pc"), ("NS surface", "NS surface|canonical|24pc"),
            ("M87* at 3M (capped)", "M87* (r = 3M)|canonical|24pc"), ("Sgr A* at 3M (capped)", "SgrA* (r = 3M)|canonical|24pc")]
    labels = ["tensor modes (both)"] + ["pair: " + a for a, _ in rows]
    vals = [math.sqrt(tensor[0])] + [p3["E4"][k]["c_pi"] for _, k in rows]
    cols = [ms.STATUS["PASS"]] + [ms.MUTED if v <= 1 else ms.STATUS["FAIL"] for v in vals[1:]]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.2), gridspec_kw={"width_ratios": [1.7, 1]})
    logbar(a, labels, vals, cols, "propagation speed / c", fmt="{:.3g}")
    a.axvline(1.0, color=ms.MODEL, lw=1.3, ls="--")
    a.text(1.3, -0.45, "c", color=ms.MODEL, fontsize=9)
    a.set_xlim(3e-5, 3e4)
    a.set_title("speeds (canonical footing, L* = 24 pc)", fontsize=9.5, color=ms.MUTED)
    eps_bh = p3["verdicts"]["numbers"]["mixing_eps_max"]
    eps_dp = p3["double_pulsar_mixing_eps_max"]
    gw = J["C8"]["K9"]["alt_Earth_surface_g"]["dv_over_c"]
    logbar(b, ["tensor |dv/c| (GW170817)", "pair-metric mixing,\ndouble pulsar", "pair-metric mixing,\nmax (BH)"],
           [gw, eps_dp, eps_bh], [ms.STATUS["PASS"], ms.MUTED, ms.MUTED], "size (dimensionless)", fmt="{:.2e}")
    b.axvline(1e-15, color=ms.MODEL, lw=1.3, ls="--")
    b.text(1.4e-15, 2.35, "GW170817\nbound 1e-15", color=ms.MODEL, fontsize=7.5, va="top")
    b.set_xlim(1e-34, 1e-2)
    b.set_title("coupling to the metric", fontsize=9.5, color=ms.MUTED)
    fig.subplots_adjust(left=0.22, wspace=0.85, right=0.97)
    ms.finish(fig, "c0_01_gw_light_speed", "PASS", "Gravity waves at light speed",
              "PASS: the 2 tensor modes travel at exactly c; the khronon pair is slow where it matters and barely couples",
              f"{SRC['C5']} (H4 rows); {SRC['P3']} (E4, mixing); {SRC['C8']} (K9)")


# ---------------------------------------------------------------- 02 health
def fig02():
    c = J["X3"]["C"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    for key, lab, col, mk in [("C0_unswitched_1e-3", "v3 as written (stiffness everywhere)", ms.STATUS["FAIL"], "s"),
                              ("C1_0.001", "v3s switched, zero dust", ms.STATUS["PASS"], "o"),
                              ("C2_0.001", "v3s switched, dust buffer", ms.STATUS["COND"], "^")]:
        N = [r["N"] for r in c[key]]
        G = [r["Gamma"] for r in c[key]]
        a.plot(N, G, marker=mk, color=col, label=lab, lw=1.6)
    bound = c["C1_0.001"][-1]["bound"]
    a.axhline(bound, color=ms.MUTED, ls=":", lw=1)
    a.text(70, bound * 1.07, f"rate bound, zero-dust slab {bound:.4f}", fontsize=7.5, color=ms.MUTED)
    a.set_xscale("log", base=2)
    a.set_yscale("log")
    a.set_xlabel("slab grid points N (gamma_L = 1e-3)")
    a.set_ylabel("growth rate Gamma where rho_tau < 0")
    a.legend(fontsize=7.8, loc="center right")
    a.set_title("1D slab, no WKB: does refining the grid blow up?", fontsize=9, color=ms.MUTED)
    rows = J["SS"]["N3"]["rows"]
    l = np.array([r["l_full_m"] for r in rows])
    lmin, lmax = J["SS"]["N3"]["l_min_m"], J["SS"]["N3"]["l_max_m"]
    b.hist(np.log10(l), bins=np.arange(1, 17.01, 0.25), color=ms.DATA, alpha=0.85)
    pc = 3.0857e16
    b.axvline(math.log10(pc), color=ms.MODEL, ls="--", lw=1.3)
    b.text(math.log10(pc) - 0.2, b.get_ylim()[1] * 0.9, "1 pc", color=ms.MODEL, ha="right", fontsize=8.5)
    b.set_xlim(1, 17.5)
    b.set_xlabel("log10 strong-coupling length on the soft side (m)")
    b.set_ylabel(f"region values (of {len(l)})")
    b.set_title(f"soft side weakly coupled: {lmin:.1f} m to {lmax:.3g} m", fontsize=9, color=ms.MUTED)
    fig.subplots_adjust(wspace=0.3, left=0.08, right=0.97)
    ms.finish(fig, "c0_02_health", "COND", "Health: ghosts, gradients",
              "CONDITIONAL: the switch stops the blow-up in 1D; needs dust >= -D.P, has a zero-dust knife edge; 2D/3D open",
              f"{SRC['X3']} (C); {SRC['SS']} (N3)")


# ---------------------------------------------------------------- 03 leaf problem
def fig03():
    k4, k5 = J["C8"]["K4"], J["C8"]["K5"]
    items = [("sphere r_M/L*=0.3: two guesses", k4["rM_0.3"]["max_rel_diff_guesses"], 1e-6),
             ("sphere r_M/L*=3: two guesses", k4["rM_3.0"]["max_rel_diff_guesses"], 1e-6),
             ("sphere r_M/L*=0.3: domain doubled", k4["rM_0.3"]["max_rel_diff_domain_doubling_r<=L"], 1e-3),
             ("sphere r_M/L*=3: domain doubled", k4["rM_3.0"]["max_rel_diff_domain_doubling_r<=L"], 1e-3),
             ("3D two masses: grad Phi, two guesses", k5["max_rel_diff_gradPhi"], 1e-4),
             ("3D two masses: P, two guesses", k5["max_rel_diff_P"], 1e-4)]
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    y = logbar(ax, [i[0] for i in items], [i[1] for i in items], [ms.STATUS["PASS"]] * len(items),
               "relative difference between solutions (lower = unique)")
    for yi, it in zip(y, items):
        ax.plot([it[2]], [yi], marker="|", ms=18, mew=2.2, color=ms.MODEL)
    ax.plot([], [], marker="|", ls="", ms=12, mew=2, color=ms.MODEL, label="frozen pass line (C8 K4/K5)")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(1e-16, 1e1)
    ax.set_title("convex leaf functional (K2); symbol >= min(K, gamma_L xi^2) (K1: min ratio "
                 f"{J['C8']['K1']['min_schur_over_bound']:.0f})\nOPEN: infinite volume; coupled GR + dust",
                 fontsize=8.5, color=ms.MUTED)
    fig.subplots_adjust(left=0.33, right=0.97)
    ms.finish(fig, "c0_03_leaf_problem", "COND", "Leaf problem well-posed",
              "CONDITIONAL: one solution per leaf on bounded domains; infinite volume and coupled GR + dust open",
              f"{SRC['C8']} (K1, K4, K5); v3s switch: {SRC['X3']} (B3S)")


# ---------------------------------------------------------------- 04 causality
def fig04():
    s = J["C8"]["signal_illustration"]
    a0 = J["C6"]["inputs"]["a0"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.0), gridspec_kw={"width_ratios": [1, 1.25]})
    for t in np.linspace(0, 1, 6):
        a.plot([-1, 1], [t, t], color=ms.GRID, lw=1.2)
    a.text(1.0, 1.02, "leaves tau = const", fontsize=7.5, color=ms.MUTED, ha="right")
    a.fill_between([-0.5, 0, 0.5], [1, 0.4, 1], [1, 1, 1], color=ms.BAND, alpha=0.7)
    a.plot([-0.5, 0, 0.5], [1, 0.4, 1], color=ms.DATA, lw=1.2)
    a.text(0, 0.83, "light cone", ha="center", fontsize=8, color=ms.DATA)
    a.annotate("", xy=(0.95, 0.4), xytext=(0.02, 0.4), arrowprops=dict(arrowstyle="->", color=ms.MODEL, lw=2))
    a.text(0.5, 0.33, "P / lapse response:\nsame instant of tau", ha="center", va="top", fontsize=8, color=ms.MODEL)
    a.plot([0], [0.4], "o", color=ms.INK)
    a.text(-0.95, 0.12, "B: nothing goes back in tau -> holds\nA: no influence outside the cone -> fails",
           fontsize=8, color=ms.INK)
    a.set_xlim(-1, 1)
    a.set_ylim(0, 1.08)
    a.set_xticks([])
    a.set_yticks([])
    a.set_xlabel("space")
    a.set_ylabel("khronon time tau")
    a.grid(False)
    labels = ["signal, L* = 20 pc", "signal, L* = 24 pc", "signal, L* = 90 pc", "a0 canonical (scale)", "a0 alt (scale)"]
    vals = [s["L20"], s["L24"], s["L90"], a0["canonical"], a0["alt"]]
    logbar(b, labels, vals, [ms.MODEL] * 3 + [ms.MUTED] * 2, "acceleration (m/s^2)")
    b.set_xlim(1e-49, 1e-6)
    b.set_title("1000 kg moved 1 m, felt 1 km away", fontsize=9, color=ms.MUTED)
    fig.subplots_adjust(wspace=0.55, left=0.05, right=0.96)
    ms.finish(fig, "c0_04_causality", "COND", "Causality: criterion A / B",
              "CONDITIONAL: ordered in khronon time (B holds); faster than light in principle (A fails), at ~1e-46 m/s^2",
              f"{SRC['C8']} (signal_illustration); a0 from {SRC['C6']} (inputs)")


# ---------------------------------------------------------------- 05 binary pulsars + GW170817
def fig05():
    k7 = J["C8"]["K7"]["systems"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.0), gridspec_kw={"width_ratios": [1.6, 1]})
    names = list(k7)
    w = 0.25
    for j, (L, col) in enumerate([("L20", ms.DATA), ("L24", ms.MUTED), ("L90", "#a9b4bb")]):
        v = [k7[n][L]["eps_over_precision"] for n in names]
        a.bar(np.arange(3) + (j - 1) * w, v, w, color=col, label=f"L* = {L[1:]} pc")
    a.set_yscale("log")
    a.axhline(1, color=ms.MODEL, ls="--", lw=1.3)
    a.text(2.45, 2.2, "measurement error", color=ms.MODEL, fontsize=8, ha="right")
    a.set_xticks(range(3))
    a.set_xticklabels(names, fontsize=8.5)
    a.set_ylabel("orbit change / Pdot_b precision")
    a.set_ylim(1e-19, 1e3)
    a.legend(fontsize=8, loc="center right")
    a.text(0.02, 0.80, f"worst {J['C8']['K7']['worst_ratio']:.2e}; no radiative channel", transform=a.transAxes,
           fontsize=8, va="top")
    k9 = J["C8"]["K9"]
    labs = ["canonical, g = a0", "canonical, g = Earth", "alt, g = a0", "alt, g = Earth"]
    keys = ["canonical_galactic_g=a0", "canonical_Earth_surface_g", "alt_galactic_g=a0", "alt_Earth_surface_g"]
    logbar(b, labs, [k9[k]["dv_over_c"] for k in keys], [ms.STATUS["PASS"]] * 4, "tensor |dv/c| at 100 Hz")
    b.axvline(1e-15, color=ms.MODEL, ls="--", lw=1.3)
    b.text(2e-16, 3.4, "GW170817\n1e-15", color=ms.MODEL, fontsize=7.5, ha="right", va="top")
    b.set_xlim(1e-41, 1e-13)
    fig.subplots_adjust(wspace=0.55, left=0.08, right=0.97)
    ms.finish(fig, "c0_05_binary_pulsars", "PASS", "Binary pulsars + GW170817",
              "PASS: every effect sits 13+ orders below the timing error; GW speed shift 6e-32 vs 1e-15",
              f"{SRC['C8']} (K7, K9); Pdot_b precisions are record transcriptions")


# ---------------------------------------------------------------- 06 Cassini screened
def fig06():
    c6 = J["C6"]
    r1, hees, park = c6["R1_physical"], c6["inputs"]["band_Hees_2sigma"][1], c6["inputs"]["band_Park_2sigma"][1]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.0), gridspec_kw={"width_ratios": [1.5, 1]})
    Ls = [24, 50, 90]
    for f, dx in [("canonical", -0.12), ("alt", 0.12)]:
        for i, L in enumerate(Ls):
            q = [r1[f"{f}|{L}|E{e}"]["Q2"] for e in range(4)]
            a.plot([i + dx] * 4, q, "o", color=FOOT[f], ms=5, label=f if i == 0 else None)
    a.axhline(hees, color=ms.MODEL, ls="--", lw=1.3)
    a.axhline(park, color=ms.MODEL, ls=":", lw=1.3)
    a.text(2.4, hees * 1.6, "Hees 2014, 2 sigma", color=ms.MODEL, fontsize=7.5, ha="right")
    a.text(2.4, park / 3.5, "Park 2026, 2 sigma", color=ms.MODEL, fontsize=7.5, ha="right")
    a.set_yscale("log")
    a.set_ylim(1e-37, 1e-25)
    a.set_xticks(range(3))
    a.set_xticklabels([f"L* = {L} pc" for L in Ls])
    a.set_ylabel("Cassini quadrupole Q2 (s^-2), fields E0-E3")
    a.legend(fontsize=8, loc="center right")
    m = c6["R1_margin"]
    a.set_title(f"margin {m['Park_min']:.2e} (Park) to {m['Hees_max']:.2e} (Hees)", fontsize=9, color=ms.MUTED)
    pl = c6["R2_planets"]
    planets = ["Earth", "Mars", "Saturn"]
    for j, (L, col) in enumerate([(24, ms.DATA), (50, ms.MUTED), (90, "#a9b4bb")]):
        b.bar(np.arange(3) + (j - 1) * 0.25, [pl[f"canonical|{L}|{p}"]["ratio"] for p in planets], 0.25, color=col,
              label=f"L* = {L} pc")
    b.axhline(1, color=ms.MODEL, ls="--", lw=1.3)
    b.set_xticks(range(3))
    b.set_xticklabels(planets)
    b.set_ylabel("anomalous acceleration / bound")
    b.set_ylim(0, 1.1)
    b.legend(fontsize=8)
    b.text(1, pl["canonical|24|Mars"]["ratio"] + 0.03, f"{pl['canonical|24|Mars']['ratio']:.3f}", ha="center",
           fontsize=8)
    b.set_title("inner planets (same on both footings)", fontsize=9, color=ms.MUTED)
    fig.subplots_adjust(wspace=0.35, left=0.09, right=0.97)
    ms.finish(fig, "c0_06_cassini_screened", "PASS", "Solar system + Cassini (screened)",
              "PASS (reading): 24 of 24 Cassini cells 2.8e7+ below the bound; frozen rule UNDECIDED on one rounding check",
              f"{SRC['C6']} (R1, R2, checks C2)")


# ---------------------------------------------------------------- 07 unscreened law vs Cassini
def fig07():
    r1 = J["E2"]["R1"]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    for f, dx in [("canonical", -0.13), ("alt", 0.13)]:
        rows = [k for k in r1 if k.startswith(f + "|")]
        for e in range(4):
            v = [r1[k]["over_Hees"][e] for k in rows]
            base = r1[f + "|none"]["over_Hees"][e]
            ax.plot([e + dx, e + dx], [min(v), max(v)], color=FOOT[f], lw=6, alpha=0.35, solid_capstyle="butt")
            ax.plot([e + dx], [base], "o", color=FOOT[f], ms=6, label=f if e == 0 else None)
            ax.text(e + dx, max(v) + 0.12, f"{min(v):.2f}-{max(v):.2f}", ha="center", fontsize=7, color=FOOT[f])
    ax.axhline(1, color=ms.MODEL, ls="--", lw=1.4)
    ax.text(3.45, 1.08, "Hees 2014 2 sigma upper", color=ms.MODEL, fontsize=8, ha="right")
    ax.fill_between([-0.5, 3.5], 0, 1, color=ms.BAND, alpha=0.5)
    ax.text(-0.4, 0.5, "allowed", fontsize=8, color=ms.MUTED)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(0, 6)
    ax.set_xticks(range(4))
    ax.set_xticklabels([f"E{e}" for e in range(4)])
    ax.set_xlabel("Galactic field at the Sun (E0 weakest ... E3 strongest)")
    ax.set_ylabel("AQUAL Q2 / Hees bound (L* = 0)")
    ax.legend(fontsize=8.5, loc="upper left", title="dot: no transition; bar: y_t rows", title_fontsize=7.5)
    o = J["E2"]["R1_outcome"]
    ms.finish(fig, "c0_07_unscreened_cassini", "FAIL", "Unscreened law vs Cassini",
              f"FAIL (control): screening off, Q2 = {o['canonical_range'][0]:.2f}-{o['canonical_range'][1]:.2f}x (canonical), "
              f"{o['alt_range'][0]:.2f}-{o['alt_range'][1]:.2f}x (alt) the bound",
              f"{SRC['E2']} (R1, R1_outcome)")


# ---------------------------------------------------------------- 08 strong coupling
def fig08():
    e4 = J["P3"]["E4"]
    sysl = [("Eot-Wash 38.6 um", "Eot-Wash (38.6 um)"), ("planets 1 AU", "planets (1 AU)"), ("double pulsar", "double pulsar"),
            ("NS surface", "NS surface"), ("BH 10 Msun, 3M", "BH10 (r = 3M)"), ("M87*, 3M", "M87* (r = 3M)"),
            ("galaxy 1 kpc", "galaxy (1 kpc; phantom 0.01 Msun/pc^3, ILLUSTRATIVE)"),
            ("cosmology 10 h/Mpc", "cosmology (10 h/Mpc; FRW, P0 = 0)")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 5.0), gridspec_kw={"width_ratios": [1.5, 1]})
    vals = [e4[f"{k}|canonical|24pc"]["eps_max"] for _, k in sysl]
    logbar(a, [s for s, _ in sysl], vals, [ms.STATUS["COND"]] + [ms.MUTED] * (len(vals) - 1), "loop factor eps (worst vertex)")
    a.axvline(1e-2, color=ms.MODEL, ls="--", lw=1.3)
    a.text(1e-1, 4.5, "pass line\n1e-2", color=ms.MODEL, fontsize=7.5, va="center")
    a.set_xlim(1e-100, 1e14)
    a.set_title("all declared systems (canonical, L* = 24 pc)", fontsize=9, color=ms.MUTED)
    Ls = [20, 24, 90]
    ew = [e4[f"Eot-Wash (38.6 um)|canonical|{L}pc"]["eps_max"] for L in Ls]
    b.bar(range(3), ew, color=ms.STATUS["COND"], width=0.55)
    b.axhline(1e-2, color=ms.MODEL, ls="--", lw=1.3)
    b.set_yscale("log")
    b.set_ylim(1e-5, 5e-2)
    b.set_xticks(range(3))
    b.set_xticklabels([f"L* = {L} pc" for L in Ls])
    b.set_ylabel("eps at Eot-Wash 38.6 um")
    for i, v in enumerate(ew):
        b.text(i, v * 1.3, f"{v:.2e}\nk margin\n{(1e-2 / v) ** 0.25:.2f}x", ha="center", fontsize=7.5)
    b.set_title("the tight spot (same on both footings)", fontsize=9, color=ms.MUTED)
    fig.subplots_adjust(wspace=0.45, left=0.17, right=0.97)
    ms.finish(fig, "c0_08_strong_coupling", "COND", "Strong coupling",
              "CONDITIONAL (estimate): weakly coupled at every declared system; only a 1.7x margin in k at Eot-Wash",
              f"{SRC['P3']} (E4); pass line eps <= 1e-2 from rebuild_2026_10_22/P3_v3_strong_field/FROZEN_CRITERIA.md V4")


# ---------------------------------------------------------------- 09 matter conservation
def fig09():
    n = J["G9"]["numbers"]
    items = [("GR control: div G (C1)", max(n["C1"]["bianchi_rel"]), ms.STATUS["PASS"]),
             ("matter identity, any coupling (S1)", n["S1"]["identity_rel"], ms.STATUS["PASS"]),
             ("GR Bianchi (S2)", n["S2"]["GR"], ms.STATUS["PASS"]),
             ("plain khronometric (S2)", n["S2"]["KH"], ms.STATUS["PASS"]),
             ("full chassis, diffeo-invariant (S2)", n["S2"]["CHK"], ms.STATUS["PASS"]),
             ("power check: non-covariant term (C3)", n["S2"]["CHK_NONCOV"], ms.STATUS["FAIL"])]
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    logbar(ax, [i[0] for i in items], [i[1] for i in items], [i[2] for i in items], "relative residual of the identity")
    ax.set_xlim(1e-50, 1e2)
    ax.text(0.98, 0.96, "identity ~ 1e-47 (floating zero) for every covariant action;\n"
            "the power check shows the test catches a real violation",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, bbox=dict(fc="white", ec=ms.GRID))
    fig.subplots_adjust(left=0.33, right=0.96)
    ms.finish(fig, "c0_09_matter_conservation", "PASS", "Matter conservation (G9)",
              "PASS: grad T = 0 is a theorem for any diffeomorphism-invariant action with matter on g, v3 included",
              f"{SRC['G9']} (numbers C1, S1, S2); v3 is diffeo-invariant per covariant_push_2026_10_22/C4_khronon_parent")


# ---------------------------------------------------------------- 10 black holes
def fig10():
    w = J["P3"]["worst_shifts"]
    order = [("photon sphere r_ph", "r_ph"), ("local shadow", "shadow_local"), ("ISCO radius", "r_isco"),
             ("ISCO frequency", "Omega_isco"), ("QNM frequency", "f_qnm"), ("QNM damping time", "tau_qnm"),
             ("shadow via M87*'s 100 pc\ndynamical mass (law, not strong field)", "shadow_dyn")]
    vals = [w[k][0] for _, k in order]
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    logbar(ax, [s for s, _ in order], vals, [ms.STATUS["PASS"]] * 6 + [ms.MUTED], "largest fractional shift (all benchmarks)")
    ax.axvline(1e-2, color=ms.MODEL, ls="--", lw=1.3)
    ax.text(1.2e-2, 6.3, "pass line 1e-2\n(EHT / ringdown)", color=ms.MODEL, fontsize=7.5, va="top")
    ax.set_xlim(1e-12, 1e1)
    ax.text(0.29, 0.5, "static, non-rotating only: regular horizons need an infalling (tilted) khronon;\n"
            "rotating and moving holes not computed (OPEN)", transform=ax.transAxes, fontsize=8, va="center",
            bbox=dict(fc="white", ec=ms.GRID))
    fig.subplots_adjust(left=0.34, right=0.96)
    ms.finish(fig, "c0_10_black_holes", "COND", "Black holes (EHT, LIGO ringdown)",
              "CONDITIONAL: static holes pass (shape shifts <= 3e-11); rotating and moving holes open",
              f"{SRC['P3']} (worst_shifts)")


if __name__ == "__main__":
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10):
        f()
    print("col0: 10 figures written to", ms.IMG)
