"""Column 3 ("Cosmology and a0 over time") of the Dark River Tavern Menu. PLOT ONLY: every number is read from a committed
file of the lane that carries the tile. No physics is re-run.

Owner rule: LCDM is not a yardstick. No LCDM curve, fit or Delta-chi2 is drawn. CMB and growth tiles show v3's own output
against the raw Planck plik-lite chi2 (613 bins) or against the framework's own requirements (BBN; sigma8 within 5% of v3's
own dust limit).

Run from explainers/dark_river_tavern_menu:  python3 -I scripts/col3_figs.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import menu_style as ms  # noqa: E402

R = ms.ROOT
CAN, ALT = "#0072B2", "#D55E00"      # canonical / alt footing (never pooled)
OLD = "#9aa3a9"                       # record kernel nu_mono (shown beside v3's nu_1)


def J(p):
    return json.load(open(R / p))


# ------------------------------------------------------------------------------------------------ c3_00 a0(z) native band
def fig_a0z():
    p = "campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json"
    d = J(p)["BAO+SN"]["P1"]
    zs = sorted(d, key=float)
    z = np.array([float(k) for k in zs])
    q = np.array([d[k]["sqrtX_q"] for k in zs])        # 2.5 16 50 84 97.5
    e = np.array([d[k]["E_q"] for k in zs])
    fig, ax = plt.subplots()
    ax.fill_between(z, q[:, 0], q[:, 4], color=ms.BAND, alpha=0.55, lw=0, label="native band, 95%")
    ax.fill_between(z, q[:, 1], q[:, 3], color="#aab4bb", alpha=0.75, lw=0, label="native band, 68%")
    ax.errorbar(z, q[:, 2], yerr=[q[:, 2] - q[:, 1], q[:, 3] - q[:, 2]], fmt="o", color=ms.DATA, ms=5, capsize=3,
                label="tracking a$_0$(z)/a$_0$(0) from BAO + SN (median, 68%)")
    ax.axhline(1.0, color=ms.MODEL, lw=2.2, label="v3 prediction: constant a$_0$ (flat line)")
    ax.errorbar(z, e[:, 2], yerr=[e[:, 2] - e[:, 1], e[:, 3] - e[:, 2]], fmt="D", color="#5b7db1", ms=5, capsize=3,
                mfc="white", label="rival a$_0$ ∝ H(z): E = H/H$_0$ on the same native fit")
    for zi, k in zip(z, zs):
        ax.text(zi, 0.05, f"3σ split needs\nσ ≤ {d[k]['e_3sigma']:.3f} dex", ha="center", fontsize=7, color=ms.MUTED)
    ax.set_xlim(0.85, 2.5); ax.set_ylim(0, 3.9)
    ax.set_xlabel("redshift z"); ax.set_ylabel("a$_0$(z) / a$_0$(0)")
    ax.legend(loc="upper left", fontsize=8)
    ms.finish(fig, "c3_00_a0z_native_band", "UNDEC", "a0(z): native band vs a0 ~ H(z)",
              "Flat line inside the band at every node; today's galaxy samples cannot decide",
              p + " (primary: curvature free, DESI DR2 BAO + Pantheon+)")
    q = np.array([d[k]["sqrtX_q"] for k in zs])
    return {k: dict(q16=d[k]["sqrtX_q"][1], q50=d[k]["sqrtX_q"][2], q84=d[k]["sqrtX_q"][3], E50=d[k]["E_q"][2],
                    gap_dex=d[k]["gap_dex"], e_3sigma=d[k]["e_3sigma"]) for k in zs}


# ------------------------------------------------------------------------------------------------ c3_01 high-z
R4 = "rebuild_2026_10_22/S4_v3_muK_clusters/r4_out/"
RC = ("cfg303_rc100_cristal_LCDMFREE/{v}/campaign_fresh_gravity__CFG303_lcdm_free_inputs__"
      "cfg303_rc100_cristal_LCDMFREE_results.json")


def fig_highz():
    pts = [("RC100", "B Q1", "RC100 Q1"), ("RC100", "B Q2", "RC100 Q2"), ("RC100", "B Q3", "RC100 Q3"),
           ("RC100", "B Q4", "RC100 Q4"), ("CRISTAL", "R_e native, six", "CRISTAL R$_e$"),
           ("CRISTAL", "R_out native, six, outermost data marker (primary)", "CRISTAL R$_{out}$")]
    D = {v: J(R4 + RC.format(v=v))["points"] for v in ("repro", "nu1")}
    fig, ax = plt.subplots()
    FLOOR = 0.12
    out = {}
    for i, (blk, key, lab) in enumerate(pts):
        for v, dx, col, mk, name in (("repro", -0.22, OLD, "s", "record kernel ν$_{mono}$"),
                                     ("nu1", 0.0, ms.DATA, "o", "v3 kernel ν$_1$")):
            r = D[v][blk][key]
            zz = i + dx
            noroot = r["s"] <= 0.0011
            s = max(r["s"], FLOOR)
            lo, hi = max(r["lo68"], FLOOR), max(r["hi68"], FLOOR)
            if noroot:
                ax.annotate("", xy=(zz, FLOOR * 0.85), xytext=(zz, FLOOR * 1.7),
                            arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6))
            else:
                ax.errorbar(zz, s, yerr=[[s - lo], [hi - s]], fmt=mk, color=col, ms=6, capsize=3,
                            label=name + " (68%)" if i == 0 else None)
            if v == "nu1":
                if noroot:
                    ax.text(i - 0.11, FLOOR * 0.8, "no root (both)", ha="center", fontsize=7, color=ms.DATA, va="top")
                ax.plot(i + 0.22, r["expected"]["H(z)"]["s"], "D", mfc="white", mec="#5b7db1", mew=1.6, ms=7,
                        label="rival a$_0$ ∝ H(z) at that z" if i == 0 else None)
                out[lab.replace("$", "").replace("_", "").replace("{", "").replace("}", "")] = dict(
                    z=r["z_med"], s_v3=r["s"], lo68=r["lo68"], hi68=r["hi68"], s_record=D["repro"][blk][key]["s"],
                    s_Hz=r["expected"]["H(z)"]["s"], a0_over_s=r["a0_implied_1e-10"] / r["s"] if r["s"] > 0.0011 else None)
    ax.axhline(1.0, color=ms.MODEL, lw=2.2, label="v3 prediction: flat a$_0$ (s★ = 1)")
    ax.set_yscale("log"); ax.set_ylim(0.07, 40); ax.set_xlim(-0.6, len(pts) - 0.4)
    ax.set_xticks(range(len(pts)))
    ax.set_xticklabels([f"{lab}\nz {D['nu1'][b][k]['z_med']:.2f}" for b, k, lab in pts], fontsize=8)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("implied s★ = a$_0$(z) / a$_0$(0)  (canonical)")
    ax.legend(loc="upper left", fontsize=7.8, ncol=2)
    ms.finish(fig, "c3_01_highz_halo_free", "UNDEC", "High-z on halo-free inputs",
              "v3's kernel moves s★ by at most 0.1 dex; every class unchanged; flat vs H(z) not separated",
              R4 + "cfg303_rc100_cristal_LCDMFREE/{repro,nu1}/..._results.json (S4 R4 swap of CFG303)")
    return out


# ------------------------------------------------------------------------------------------------ c3_02 CRISTAL / ALESS
def fig_cristal_aless():
    a = {v: J(R4 + f"cfg307_stress/{v}/campaign_fresh_gravity__CFG307_aless122_stress_test__cfg307_stress_results.json")
         ["decision"]["primary"] for v in ("repro", "nu1")}
    c = {v: J(R4 + f"cfg308_cristal_stress/{v}/campaign_fresh_gravity__CFG308_cristal_stress_test__"
              "cfg308_cristal_stress_results.json")["fractions"] for v in ("repro", "nu1")}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.2), gridspec_kw=dict(width_ratios=[4, 2.6]))
    fig.subplots_adjust(left=0.19, right=0.97, wspace=0.62)
    # ALESS 122.1 (540 cells): triggers and robust lines from CFG307's frozen rule
    rows = [("no root in the cell", "f_noroot", 0.25, "NOT ROBUST if > 25%"),
            ("flat a$_0$ inside 95%", "f_FLAT_inside", 0.25, "NOT ROBUST if > 25%"),
            ("flat a$_0$ excluded (above)", "f_FLAT_excl", 0.80, "robust needs ≥ 80%"),
            ("a$_0$ ∝ H(z) excluded", "f_Hz_excl", 0.50, "robust needs ≥ 50%")]
    y = np.arange(len(rows))[::-1]
    for yi, (lab, k, thr, tl) in zip(y, rows):
        ax1.barh(yi + 0.18, a["repro"][k], 0.34, color=OLD)
        ax1.barh(yi - 0.18, a["nu1"][k], 0.34, color=ms.DATA)
        ax1.plot([thr, thr], [yi - 0.42, yi + 0.42], color=ms.MODEL, lw=2.2)
        ax1.text(max(thr, a["repro"][k], a["nu1"][k]) + 0.02, yi + 0.18, tl, fontsize=7.3, color=ms.MODEL, va="center")
        ax1.text(a["nu1"][k] + 0.01, yi - 0.18, f"{100*a['nu1'][k]:.1f}%", fontsize=7.5, va="center")
    ax1.set_yticks(y); ax1.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax1.set_xlim(0, 1.05); ax1.set_xlabel("fraction of the 540 stress cells")
    ax1.set_title("ALESS 122.1 (z 2.02): NOT ROBUST", loc="left", fontsize=10, weight="bold")
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(color=OLD, label="record kernel ν$_{mono}$ (upper bar)"),
                        Patch(color=ms.DATA, label="v3 kernel ν$_1$ (lower bar)")], loc="lower right", fontsize=7.6)
    # CRISTAL (1008 cells): exclusion fractions vs the 80% line
    rows2 = [("a$_0$ ∝ H(z)\nexcluded", "frac_H_excl"), ("flat a$_0$\nexcluded", "frac_F_excl")]
    y2 = np.arange(2)[::-1]
    for yi, (lab, k) in zip(y2, rows2):
        ax2.barh(yi + 0.18, c["repro"][k], 0.34, color=OLD)
        ax2.barh(yi - 0.18, c["nu1"][k], 0.34, color=ms.DATA)
        ax2.text(c["nu1"][k] + 0.01, yi - 0.18, f"{100*c['nu1'][k]:.1f}%", fontsize=7.5, va="center")
    ax2.axvline(0.80, color=ms.MODEL, lw=2.2)
    ax2.text(0.79, 1.35, "decides at 80%", fontsize=7.3, color=ms.MODEL, ha="right")
    ax2.set_yticks(y2); ax2.set_yticklabels([r[0] for r in rows2], fontsize=8.5)
    ax2.set_xlim(0, 1.05); ax2.set_ylim(-0.6, 1.75); ax2.set_xlabel("fraction of the 1,008 cells")
    ax2.set_title("CRISTAL (z ≈ 5)", loc="left", fontsize=10, weight="bold")
    ax2.text(0.02, 0.985, "NOT DISCRIMINATING", transform=ax2.transAxes, fontsize=9, weight="bold", va="top")
    ms.finish(fig, "c3_02_cristal_aless", "UNDEC", "CRISTAL z~5 / ALESS 122.1",
              "ALESS trips both NOT ROBUST triggers; CRISTAL excludes neither law in 80% of cells; v3 kernel changes no class",
              R4 + "cfg307_stress/*, cfg308_cristal_stress/* (repro = record, nu1 = v3); CFG307/CFG308 frozen rules")
    return dict(aless=a, cristal=c)


# ------------------------------------------------------------------------------------------------ c3_03 native CMB
Q6 = "rebuild_2026_10_22/Q6_v3_class/q6_native_results.json"
Q7 = "rebuild_2026_10_22/Q7_bs25_cosmology/q7_native_results.json"


def fig_cmb():
    q6, q7 = J(Q6), J(Q7)
    mu = q6["mu_grid_hMpc"]; hconv = q6["mu_grid_per_Mpc"][0] / mu[0]       # Mpc^-1 per h/Mpc (the lane's h)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.2))
    fig.subplots_adjust(wspace=0.32, left=0.08, right=0.98)
    # (a) BBN: the framework's own requirement dNeff,equiv(1 MeV) <= 0.5
    dn = [q6["stepB"]["rows"][f"{m:g}"]["dNeff_equiv_1MeV"] for m in mu]
    ax1.plot(mu, dn, "o-", color=ms.MODEL, lw=1.8, label="literal v3, quadratic K (Q6)")
    rows7 = q7["stepB"]["rows"]
    lab7 = {"P1": "P1", "P2": "P2", "C1": "cap, λ$_D$=1", "C30": "cap, λ$_D$=30"}
    for k, v in rows7.items():
        if k not in lab7:
            continue
        m = v["mu_per_Mpc"] / hconv
        ax1.plot(m, v["dNeff_equiv_1MeV"], "s", color=ms.DATA, ms=6, label="BS25 DBI K (Q7)" if k == "P1" else None)
        ax1.annotate(lab7[k], (m, v["dNeff_equiv_1MeV"]), textcoords="offset points", xytext=(6, 4 if k != "C1" else -11),
                     fontsize=7.3, color=ms.DATA)
    ax1.axhline(0.5, color=ms.STATUS["PASS"], lw=2, ls="--")
    ax1.text(200, 0.8, "BBN line: ΔN$_{eff}$ ≤ 0.5", color=ms.STATUS["PASS"], fontsize=8)
    ax1.axvline(14.8, color=ms.MUTED, lw=1, ls=":")
    ax1.text(13.5, 1e-3, "BS galaxy cap 14.8 h/Mpc", rotation=90, fontsize=7.3, color=ms.MUTED, ha="right")
    ax1.set_xscale("log"); ax1.set_yscale("log"); ax1.set_xlim(0.03, 5000); ax1.set_ylim(1e-7, 1e16)
    ax1.set_xlabel("μ$_K$ (h/Mpc)"); ax1.set_ylabel("ΔN$_{eff}$ equivalent of the K sector at T = 1 MeV")
    ax1.set_title("(a) radiation era / BBN", loc="left", fontsize=10, weight="bold")
    ax1.legend(loc="center right", fontsize=7.6)
    # (b) raw Planck plik-lite chi2 of v3's own best fit (613 high-l bins), dust background (LOB)
    chi = [q6["fits"][f"LOB_{m:g}"]["chi2"]["plik"] for m in mu]
    ax2.plot(mu, chi, "o-", color=ms.MODEL, lw=1.8, label="v3 best fit on dust background (Q6, LOB)")
    for k in ("P1", "P2", "C30"):
        m = rows7[k]["mu_per_Mpc"] / hconv
        ax2.plot(m, q7["fits"][k]["chi2"]["plik"], "s", color=ms.DATA, ms=6, label="BS25 DBI best fit (Q7)" if k == "P1" else None)
        ax2.annotate(lab7[k], (m, q7["fits"][k]["chi2"]["plik"]), textcoords="offset points", xytext=(6, 3), fontsize=7.3)
    ax2.axhline(613, color=ms.MUTED, lw=1.4, ls="--")
    ax2.text(0.04, 650, "613 = number of plik-lite bins", fontsize=7.5, color=ms.MUTED)
    ax2.axvline(14.8, color=ms.MUTED, lw=1, ls=":")
    ax2.annotate("not converged", (14.8, chi[0]), textcoords="offset points", xytext=(6, 2), fontsize=7.3, color=ms.MODEL)
    ax2.set_xscale("log"); ax2.set_yscale("log"); ax2.set_xlim(0.03, 5000); ax2.set_ylim(300, 3e4)
    ax2.set_xlabel("μ$_K$ (h/Mpc)"); ax2.set_ylabel("χ² against raw Planck plik-lite TTTEEE")
    ax2.set_title("(b) the CMB spectra themselves", loc="left", fontsize=10, weight="bold")
    ax2.legend(loc="upper right", fontsize=7.6)
    ms.finish(fig, "c3_03_native_cmb", "FAIL", "Native CMB (patched CLASS)",
              "Literal v3: no radiation era (ΔN_eff 2.6e9-7.7e13 vs ≤ 0.5); on dust its own spectra miss Planck inside the cap",
              Q6 + ", " + Q7 + " (plik-lite bin count: q6_native.py)")
    return dict(mu=mu, dNeff=dn, chi2_plik=chi, q7={k: dict(dNeff=rows7[k]["dNeff_equiv_1MeV"],
                chi2_plik=q7["fits"][k]["chi2"]["plik"], converged=q7["fits"][k]["converged"]) for k in lab7})


# ------------------------------------------------------------------------------------------------ c3_04 linear growth
def fig_growth():
    q6, q7 = J(Q6), J(Q7)
    mu = q6["mu_grid_hMpc"]; hconv = q6["mu_grid_per_Mpc"][0] / mu[0]
    t = q6["stepC"]["table"]
    RB = [t[f"{m:g}"]["R_B"] for m in mu]
    R3 = [t[f"{m:g}"]["R_F3_bsk2_ai0.001"] for m in mu]
    R4_ = [t[f"{m:g}"]["R_F3_bsk2_ai0.0001"] for m in mu]
    fig, ax = plt.subplots()
    ax.axhspan(0.95, 1.05, color="#d8efe0", lw=0)
    ax.axhline(0.95, color=ms.STATUS["PASS"], lw=2, ls="--")
    ax.text(0.04, 0.965, "requirement: σ$_8$ within 5% of v3's own dust limit (R ≥ 0.95)", fontsize=8,
            color=ms.STATUS["PASS"])
    ax.plot(mu, RB, "o-", color=ms.MODEL, lw=2.2, ms=6, label="v3, full Boltzmann (Q6 CLASS, LOB)")
    ax.plot(mu, R3, "^--", color=ms.MUTED, lw=1.2, ms=5, label="F3 growth ODE, start a = 1e-3")
    ax.plot(mu, R4_, "v--", color="#b0b8bd", lw=1.2, ms=5, label="F3 growth ODE, start a = 1e-4")
    lab7 = {"P1": "P1", "P2": "P2", "C1": "cap λ$_D$=1", "C30": "cap λ$_D$=30"}
    for k in lab7:
        m = q7["stepB"]["rows"][k]["mu_per_Mpc"] / hconv
        rb = q7["stepC"]["per_set"][k]["R_B"]
        ax.plot(m, rb, "s", color=ms.DATA, ms=6, label="BS25 DBI K, Boltzmann (Q7)" if k == "P1" else None)
        ax.annotate(lab7[k], (m, rb), textcoords="offset points", xytext={"P1": (-6, -12), "C30": (6, -12), "C1": (-6, 6), "P2": (-4, 6)}[k],
                    fontsize=7.2, ha="left" if k == "C30" else "right")
    ax.axvspan(0.03, 14.8, color="#f1f2f3", lw=0, zorder=0)
    ax.text(0.04, 0.6, "galaxy-allowed\nμ$_K$ ≤ 14.8 h/Mpc\n(BS cap)", fontsize=7.6, color=ms.MUTED)
    ax.set_xscale("log"); ax.set_xlim(0.03, 5000); ax.set_ylim(0, 1.08)
    ax.set_xlabel("μ$_K$ (h/Mpc)"); ax.set_ylabel("R = σ$_8$(v3) / σ$_8$(v3 dust limit μ$_K$ → ∞)")
    ax.legend(loc="lower right", fontsize=7.6)
    ms.finish(fig, "c3_04_linear_growth_v3", "FAIL", "Linear growth, v3 Khronon",
              "At the cap v3 keeps 7% of its own dust-limit σ8; even μ_K = 2542 h/Mpc misses the 95% line",
              Q6 + " (stepC), " + Q7 + " (stepC)")
    return dict(mu=mu, R_B=RB, R_F3_ai1e3=R3, R_F3_ai1e4=R4_,
                q7={k: q7["stepC"]["per_set"][k]["R_B"] for k in lab7})


# ------------------------------------------------------------------------------------------------ c3_05 ALMA
SEAL = "rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_ALMA_AQUAL.json"


def fig_alma():
    s = J(SEAL)
    br = ["F-flat", "F-DESI", "BH-k3", "E", "E-CCBH", "L-fb(RAR-eq)", "R-H"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.2), gridspec_kw=dict(width_ratios=[1.15, 1]))
    fig.subplots_adjust(wspace=0.38, left=0.12, right=0.98)
    FL = 8.75
    out = {"GS4": {}, "U4": {}}
    for j, ms_ in enumerate(("10.89", "10.76")):
        for i, b in enumerate(br):
            yv = i + (0.17 if j == 0 else -0.17)
            for fp, col, dx in (("canon 9.36e-11", CAN, 0.06), ("alt 1.13e-10", ALT, -0.06)):
                c = s["GS4_24110"][ms_][f"{fp}|{b}"]
                mk = "o" if j == 0 else "s"
                if c["floor"] is True or c["floor"] == "True":
                    ax1.plot(FL, yv + dx, marker="<", color=col, ms=6, mfc="white")
                    val = None
                else:
                    val = c["logMgas_Rg=Rd"]
                    ax1.plot(val, yv + dx, marker=mk, color=col, ms=6.5, mfc=col if j == 0 else "white")
                out["GS4"][f"{ms_}|{fp}|{b}"] = val
    ax1.axvline(FL + 0.1, color=ms.MUTED, lw=0.8, ls=":")
    ax1.text(FL - 0.03, -1.05, "FLOOR: stars\nalone suffice", fontsize=7.3, color=ms.MUTED, va="bottom")
    ax1.set_yticks(range(len(br))); ax1.set_yticklabels(br, fontsize=8.3)
    ax1.set_xlim(8.6, 10.8); ax1.set_ylim(-1.1, len(br) - 0.5)
    ax1.set_xlabel("sealed required log M$_{gas}$ / M$_☉$ (R$_g$ = R$_d$)")
    ax1.set_title("(a) GS4_24110, public 28 Nov", loc="left", fontsize=10, weight="bold")
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=CAN, marker="o", ls="none", label="canonical 9.36e-11"),
         Line2D([], [], color=ALT, marker="o", ls="none", label="alt 1.13e-10"),
         Line2D([], [], color=ms.MUTED, marker="o", ls="none", label="log M★ 10.89 (primary)"),
         Line2D([], [], color=ms.MUTED, marker="s", mfc="white", ls="none", label="log M★ 10.76")]
    ax1.legend(handles=h, loc="upper right", fontsize=7.0, bbox_to_anchor=(1.0, 1.0))
    # (b) U4: required gas vs the (to be measured) V_c, sealed grid
    vg = sorted(s["U4_27928"], key=float)
    for b, ls_ in (("F-flat", "-"), ("F-DESI", "--"), ("E", ":")):
        for fp, col in (("canon 9.36e-11", CAN), ("alt 1.13e-10", ALT)):
            xs, ys = [], []
            for v in vg:
                c = s["U4_27928"][v][f"{fp}|{b}"]
                if c["logMgas_Rg=Rd"] is not None:
                    xs.append(float(v)); ys.append(c["logMgas_Rg=Rd"])
                out["U4"][f"{v}|{fp}|{b}"] = c["logMgas_Rg=Rd"]
            ax2.plot(xs, ys, ls_, color=col, marker="o", ms=3.5, lw=1.6, label=f"{b}, {fp.split()[0]}")
    ax2.set_xlim(145, 305)
    ax2.set_xlabel("V$_c$ at 2R$_e$ = 8.3 kpc, to be measured (km/s)")
    ax2.set_ylabel("sealed required log M$_{gas}$ (R$_g$ = R$_d$)")
    ax2.set_title("(b) U4_27928, public 6 Nov", loc="left", fontsize=10, weight="bold")
    ax2.text(150, ax2.get_ylim()[0] + 0.05, "lines start where FLOOR ends", fontsize=7.3, color=ms.MUTED)
    ax2.legend(fontsize=6.8, loc="upper left")
    ms.finish(fig, "c3_05_alma_u4_gs4", "OPEN", "ALMA U4 (6 Nov), GS4 (28 Nov)",
              "Sealed before the data: the gas each branch needs. One disc excludes no model; S/N expected low",
              SEAL + " (v3 AQUAL-disc reading, addendum F); verdict kernel stays ν_mono (CFG806/CFG809)")
    return out


# ------------------------------------------------------------------------------------------------ c3_06 DR4 wide binaries
C6 = "covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json"
E2 = "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json"


def fig_wb():
    c6, e2 = J(C6)["R3_wide_binary"], J(E2)["R2"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
    fig.subplots_adjust(wspace=0.32, left=0.08, right=0.98)
    # (a) gamma_v on the DR4 scale (frozen plan numbers from CFG943 README: sigma_tot 0.028, kill line 1.084, guard 1.23)
    ax1.axvspan(1 - 2 * 0.028, 1 + 2 * 0.028, color="#d8efe0", lw=0)
    ax1.text(1.0, 2.62, "±2σ$_{tot}$ of DR4\n(σ$_{tot}$ 0.028, N 30,000)", ha="center", fontsize=7.4, color=ms.STATUS["PASS"])
    ax1.axvline(1.084, color=ms.MODEL, lw=1.8, ls="--"); ax1.text(1.087, 0.15, "kill line\n1.084", fontsize=7.4, color=ms.MODEL)
    ax1.axvspan(1.23, 1.30, color="#eeeeee", lw=0); ax1.text(1.235, 0.15, "guard zone\n> 1.23", fontsize=7.4, color=ms.MUTED)
    g24c = np.mean(c6["canonical|24"]["gamma_minus_1"])
    ax1.plot(1 + g24c, 2, "o", color=ms.DATA, ms=9)
    ax1.text(1 + g24c + 0.006, 2.0, "v3 screened (L★ 24 pc): γ$_v$ − 1 ≈ 8e-6", fontsize=8, va="center")
    for yv, key, lab in ((1.0, "PREREG_primary", "PREREG primary field"), (0.55, "PREREG_alt", "PREREG alt field")):
        for fp, col in (("canonical", CAN), ("alt", ALT)):
            g = e2[f"{fp}|{key}"]["gamma_AQUAL_anch"]
            ax1.plot(g, yv, "s", color=col, ms=8, mfc="white", mew=2)
            ax1.text(g, yv + 0.13, f"{g:.3f}", fontsize=7.4, ha="center", color=col)
        ax1.text(0.93, yv, "unscreened AQUAL\n" + lab, fontsize=7.4, va="center")
    ax1.set_xlim(0.92, 1.30); ax1.set_ylim(0, 3.1); ax1.set_yticks([])
    ax1.set_xlabel("γ$_v$  (velocity boost of 1.5 M$_☉$ pairs at 20 kAU)")
    ax1.set_title("(a) where DR4 can see", loc="left", fontsize=10, weight="bold")
    from matplotlib.lines import Line2D
    ax1.legend(handles=[Line2D([], [], color=CAN, marker="s", mfc="white", ls="none", label="canonical"),
                        Line2D([], [], color=ALT, marker="s", mfc="white", ls="none", label="alt")],
               loc="upper right", fontsize=7.5)
    # (b) screened gamma_v - 1 vs L*
    Ls = [24, 50, 90]
    for fp, col in (("canonical", CAN), ("alt", ALT)):
        g = [c6[f"{fp}|{L}"]["gamma_minus_1"] for L in Ls]
        ax2.plot(Ls, [min(x) for x in g], "-", color=col, lw=1)
        ax2.plot(Ls, [max(x) for x in g], "o-", color=col, lw=1.6, label=f"v3 screened, {fp} (E0–E3)")
    ax2.axhline(0.084, color=ms.MODEL, ls="--", lw=1.6); ax2.text(26, 0.1, "DR4 kill line (γ$_v$ − 1 = 0.084)", fontsize=7.5, color=ms.MODEL)
    ax2.axhline(0.028, color=ms.STATUS["PASS"], ls=":", lw=1.4); ax2.text(26, 0.018, "1σ$_{tot}$ of DR4", fontsize=7.5, color=ms.STATUS["PASS"])
    ax2.set_xscale("log"); ax2.set_yscale("log"); ax2.set_ylim(1e-7, 1)
    ax2.set_xticks(Ls); ax2.set_xticklabels([str(x) for x in Ls]); ax2.xaxis.set_minor_formatter(plt.NullFormatter())
    ax2.set_xlabel("stiffness length L★ (pc)"); ax2.set_ylabel("γ$_v$ − 1 (screened v3)")
    ax2.set_title("(b) screened v3, log scale", loc="left", fontsize=10, weight="bold")
    ax2.legend(loc="center right", fontsize=7.4)
    ms.finish(fig, "c3_06_gaia_dr4_wide_binaries", "OPEN", "Gaia DR4 wide binaries (Dec)",
              "Screened v3 predicts no visible boost (~1e-5); the unscreened AQUAL contrast sits far above the kill line",
              C6 + " (R3); " + E2 + " (R2); DR4 plan numbers: campaign_fresh_gravity/CFG943_dr4_readiness/README.md")
    return dict(screened={f"{fp}|{L}": c6[f"{fp}|{L}"]["gamma_minus_1"] for fp in ("canonical", "alt") for L in Ls},
                aqual={k: (e2[k]["gamma_AQUAL"], e2[k]["gamma_AQUAL_anch"]) for k in e2})


# ------------------------------------------------------------------------------------------------ c3_07 DR4 Milky Way
MW = "rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_MW_DR4.json"


def fig_mw():
    d = J(MW)["v3"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.2), gridspec_kw=dict(width_ratios=[1.3, 1]))
    fig.subplots_adjust(wspace=0.30, left=0.08, right=0.98)
    sk = sorted(d["canonical"], key=float)
    out = {}
    for fp, col in (("canonical", CAN), ("alt", ALT)):
        curves = []
        for s in sk:
            v = d[fp][s]
            pts = {**v["P2_Vc_azimuthal_mean"], **v["P5_Vc_azimuthal_mean"]}
            Rr = sorted(pts, key=lambda k: float(k[1:]))
            curves.append(([float(k[1:]) for k in Rr], [pts[k] for k in Rr]))
        x = curves[0][0]
        lo = np.min([c[1] for c in curves], axis=0); hi = np.max([c[1] for c in curves], axis=0)
        mid = curves[sk.index("1.000000")][1]
        ax1.fill_between(x, lo, hi, color=col, alpha=0.18, lw=0)
        ax1.plot(x, mid, "-", color=col, lw=2, marker="o", ms=3, label=f"v3 sealed, {fp} (band: stellar mass ×0.895–1.105)")
        A = d[fp]["1.000000"]["P6_asymmetry_A"]
        Rr = sorted(A, key=lambda k: float(k[1:]))
        ax2.plot([float(k[1:]) for k in Rr], [100 * A[k] for k in Rr], "o-", color=col, lw=2, label=f"v3 with EFE, {fp}")
        out[fp] = dict(V20=mid[x.index(20.0)], V60=mid[x.index(60.0)],
                       A={k: A[k] for k in Rr}, slope_15_27p5=d[fp]["1.000000"]["P2_slope_15_27p5"])
    ax1.set_xlabel("Galactocentric radius R (kpc)"); ax1.set_ylabel("circular speed V$_c$ (km/s), azimuthal mean")
    ax1.set_title("(a) sealed rotation curve", loc="left", fontsize=10, weight="bold")
    ax1.legend(fontsize=7.4, loc="lower left")
    ax2.axhline(0, color=ms.MUTED, lw=1.4, ls="--"); ax2.text(16, 0.35, "isolated v3: A = 0", fontsize=7.5, color=ms.MUTED)
    ax2.set_xlabel("R (kpc)"); ax2.set_ylabel("in-plane V$_c$ asymmetry A (%)")
    ax2.set_title("(b) new observable P6 (V$_{min}$ toward l ≈ 270°)", loc="left", fontsize=10, weight="bold")
    ax2.legend(fontsize=7.6, loc="upper left")
    ms.finish(fig, "c3_07_gaia_dr4_mw", "OPEN", "Gaia DR4 MW predictions",
              "Sealed for v3 (AQUAL disc, ν1, EFE) before DR4; scored when the data arrive",
              MW + " (sha256 15b7e6ff..., S3_v3_mw_seals); round-rule seal CFG553 kept, not drawn")
    return out


# ------------------------------------------------------------------------------------------------ c3_08 owner's wave idea
W = "campaign_fresh_gravity/CFG956_a0z_wave_bound/cfg956.json"


def fig_wave():
    M = J(W)
    fig, ax = plt.subplots()
    sty = {"S": (ms.DATA, "o", "-", "branch S: wave on CFG689's native background"),
           "C": (ms.MODEL, "s", "-", "branch C: wave on constant ρ$_{DE}$ (v3's flat a$_0$)"),
           "N": ("#9aa3a9", "D", ":", "branch N: six free nodes (reported only)")}
    out = {}
    for br, (col, mk, ls_, lab) in sty.items():
        rr = M["rows"][br]
        P = [r["P"] for r in rr]; e = [min(r["eps95"], 1.0) for r in rr]
        ax.plot(P, e, ls_, color=col, marker=mk, ms=4.5, lw=1.8, label=lab, mfc=col if br != "N" else "white")
        out[br] = {f"{r['P']:g}": r["eps95"] for r in rr}
    ax.fill_between([0.04, 3.5], 1.0, 1.6, color="#eeeeee", lw=0)
    ax.axhline(1.0, color=ms.MUTED, lw=1, ls="--")
    ax.text(0.05, 1.08, "ε = 1: a$_0$ touches zero (no bound)", fontsize=7.6, color=ms.MUTED)
    ax.text(0.05, 0.2, "allowed: below each curve (95%, Δχ² = 3.84, phase profiled)", fontsize=7.6, color=ms.MUTED)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.045, 3.3); ax.set_ylim(0.005, 1.5)
    ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1, 2, 3]); ax.set_xticklabels(["0.05", "0.1", "0.25", "0.5", "1", "2", "3"])
    ax.set_xlabel("wave period P in ln(1+z)"); ax.set_ylabel("ε$_{95}$: largest allowed fractional wobble of a$_0$")
    ax.legend(loc="lower right", fontsize=7.6)
    ms.finish(fig, "c3_08_owner_wave_a0z", "OPEN", "The owner's wave a0(z) idea",
              "Expansion data cap the wave at ~3-8% for P ≤ 1.5; a bound is not evidence; z > 2.5 untested",
              W + " (plain wave, β = 0; same on both footings: ratio bound)")
    return out


if __name__ == "__main__":
    res = {}
    for f in (fig_a0z, fig_highz, fig_cristal_aless, fig_cmb, fig_growth, fig_alma, fig_wb, fig_mw, fig_wave):
        res[f.__name__] = f()
        print("done", f.__name__)
    if "--dump" in sys.argv:
        print(json.dumps(res, indent=1, default=str))
