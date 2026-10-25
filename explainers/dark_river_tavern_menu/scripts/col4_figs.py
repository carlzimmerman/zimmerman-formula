"""Column 4 of the status board, "The deep 'why' and the parent": one picture per tile, plus captions/col4.json.

Plot and read only. Every number comes from a committed lane file (paths below). Run from the menu folder:
    python3 -I scripts/col4_figs.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import menu_style as ms  # noqa: E402
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

R = ms.ROOT
FOOT = {"canonical": "#26323a", "alt": "#8c6d46"}


def J(p):
    return json.load(open(R / p))


def commit(p):
    try:
        return subprocess.run(["git", "-C", str(R), "log", "-1", "--format=%h", "--", p],
                              capture_output=True, text=True).stdout.strip() or "uncommitted"
    except Exception:
        return "unknown"


def src(paths):
    return [{"path": p, "commit": commit(p)} for p in paths]


CAPS = []

# ----------------------------------------------------------------------------------------------------------------
# c4_01 why kappa = 1/2
# ----------------------------------------------------------------------------------------------------------------
P_S3 = "rebuild_2026_10_22/S3_v3_mw_seals/s3_partB_kappa_results.json"
P_D5 = "doors_push_2026_10_22/D5_kappa_four/d5_kappa_four_results.json"
s3 = J(P_S3)["steps"]
d5 = J(P_D5)
Z = d5["inputs"]["Z"]
z4pi = Z / (4 * np.pi)
steps = [("record_numono", "record CFG493\n(ν_mono, algebraic)"), ("K_kernel_nu1", "v3 kernel ν₁\n(P3 rebuilt)"),
         ("A_aqual_disc", "v3: AQUAL\ndiscs"), ("E_efe_noclu", "v3 + EFE\n(primary field)"),
         ("E_efe_maxclu", "v3 + EFE\n(max field)")]
fig, ax = plt.subplots(figsize=(10, 5.4))
for j, (key, lab, col) in enumerate([("canonical", "κ_Λ (a₀ vs ρ_Λ)", "#26323a"), ("alt", "κ_crit (a₀ vs ρ_crit)", "#5b7db1")]):
    k = [s3[s][key]["kappa"] for s, _ in steps]
    e = [s3[s][key]["kappa_err"] for s, _ in steps]
    ax.errorbar(np.arange(len(steps)) + (j - 0.5) * 0.18, k, yerr=e, fmt="o", color=col, capsize=3, ms=6, label=lab)
ax.axhline(0.5, color=ms.MODEL, lw=1.6)
ax.text(0.62, 0.505, "κ = ½ (FITTED)", color=ms.MODEL, fontsize=8.5, ha="left", va="bottom")
ax.axhline(z4pi, color=ms.MUTED, lw=1.1, ls="--")
ax.text(-0.45, 0.17, f"dashed: Z/4π = {z4pi:.4f}, Milgrom's cH_Λ/2π (D5: the horizon class's simplest output; a postulate)",
        color=ms.MUTED, fontsize=7.8, va="bottom")
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[1] for s in steps], fontsize=8.5)
ax.set_ylabel("κ measured from local a₀  (a₀ = κ c √(Gρ))")
ax.set_ylim(0.15, 0.75)
ax.legend(fontsize=8.5, loc="upper left")
A = s3["A_aqual_disc"]
ms.finish(fig, "c4_01_why_kappa_half", "OPEN", "Why kappa = 1/2",
          f"OPEN: κ_Λ {A['canonical']['kappa']:.3f} ± {A['canonical']['kappa_err']:.3f}, κ_crit "
          f"{A['alt']['kappa']:.3f} ± {A['alt']['kappa_err']:.3f}: consistent with ½, not discriminating; no derivation",
          "S3_v3_mw_seals/s3_partB_kappa_results.json; D5_kappa_four (Z, theorem T1–T3)")
CAPS.append({
    "slug": "c4_01_why_kappa_half", "name": "Why kappa = 1/2", "status": "OPEN",
    "data": "κ in a₀ = κc√(Gρ), measured from the combined local a₀ of CFG493's three routes (P1 SPARC gas points, P2 "
            "MeerKAT MIGHTEE-HI widths, P3 WALLABY DR2), re-fitted by S3 step by step for v3 (kernel ν₁, AQUAL disc "
            "geometry, host field). κ_Λ uses ρ_Λ, κ_crit uses ρ_crit. D5 enumerates de Sitter horizon constructions.",
    "picture": "κ_Λ (dark) and κ_crit (blue) with 1σ errors after each re-fit step. Red line: κ = ½, the fitted value the "
               "framework uses. Grey dashed line: Z/4π, which is Milgrom's cH_Λ/2π, the simplest value horizon "
               "thermodynamics gives (a postulate, not ½).",
    "why": "With v3's AQUAL disc geometry, κ_Λ = 0.499 ± 0.116 and κ_crit = 0.413 ± 0.096: both are consistent with ½ "
           "but the error (about 0.1) cannot tell ½ from Z/4π or neighbouring values, so the data do not discriminate. "
           "On the theory side, D5 proves that products of horizon quantities give κ² = rational × odd power of π, so "
           "½ is never reached; with square roots ½ appears only as 'κ = 1 times a half picked from a menu'. κ = ½ is "
           "therefore FITTED, and why it is ½ stays open.",
    "numbers": [
        {"what": "κ_Λ, κ_crit at AQUAL discs (S3 step A)", "value": f"{A['canonical']['kappa']:.4f} +- {A['canonical']['kappa_err']:.4f}, "
         f"{A['alt']['kappa']:.4f} +- {A['alt']['kappa_err']:.4f}", "file": P_S3},
        {"what": "pull of ½, κ_Λ / κ_crit (sigma)", "value": f"{A['canonical']['pulls']['1/2']:.3f} / {A['alt']['pulls']['1/2']:.3f}",
         "file": P_S3},
        {"what": "record CFG493 κ_Λ, κ_crit", "value": f"{s3['record_numono']['canonical']['kappa']:.4f} +- "
         f"{s3['record_numono']['canonical']['kappa_err']:.4f}, {s3['record_numono']['alt']['kappa']:.4f} +- "
         f"{s3['record_numono']['alt']['kappa_err']:.4f}", "file": P_S3},
        {"what": "Z (Z/4π computed in-script)", "value": f"{Z} ({z4pi:.6f})", "file": P_D5},
        {"what": "½ in product class S1 / square-root class S2", "value": f"{d5['angle_T']['half_in_S1']} / {d5['angle_T']['half_in_S2']}",
         "file": P_D5},
    ],
    "sources": src([P_S3, P_D5, "rebuild_2026_10_22/S3_v3_mw_seals/README.md", "doors_push_2026_10_22/D5_kappa_four/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c4_02 stiffness length L*
# ----------------------------------------------------------------------------------------------------------------
P_D10 = "doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json"
P_C3 = "covariant_push_2026_10_22/C3_scale_map/c3_scale_map_results.json"
d10 = J(P_D10)
c3 = J(P_C3)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 5.4), gridspec_kw={"width_ratios": [1.35, 1]})
fig.subplots_adjust(wspace=0.55, left=0.08, right=0.97)
for ft in ["canonical", "alt"]:
    c = d10[f"chi2_curve|{ft}|central"]
    L = [x for x in c["L"] if x != "inf"]
    chi = np.array(c["chi2"][:len(L)], float)
    Lp = np.array(L, float); Lp[0] = 1.0      # plot L* = 0 (AQUAL) at the left edge
    a1.plot(Lp, chi - chi.min(), "o-", color=FOOT[ft], ms=3.5, label=f"{ft}")
    a1.axvline(d10["verdict"][ft]["central"], color=FOOT[ft], ls="--", lw=1.1)
a1.axvspan(20, 90, color=ms.STATUS["COND"], alpha=0.12)
a1.text(42, a1.get_ylim()[1] * 0.92 if a1.get_ylim()[1] > 0 else 15, "window\n20–90 pc", ha="center", fontsize=8.5,
        color="#8a6a0c")
a1.set_xscale("log")
a1.set_xlabel("L*  (pc; leftmost point = L* 0, plain AQUAL)")
a1.set_ylabel("Δχ² of 4 outer globulars (vs best)")
v = d10["verdict"]
a1.text(1.1, 1.2, f"95 % floors (dashed):\n{v['canonical']['central']:.2f} / {v['alt']['central']:.2f} pc", fontsize=8.5)
a1.legend(fontsize=8, loc="center right")
a1.set_title("globular-cluster floor (D10, native field equation)", fontsize=10, color=ms.INK)

sc = c3["K10_scales"]["lengths_pc"]
items = [("L* floor (D10, canonical)", v["canonical"]["central"], ms.STATUS["COND"]),
         ("L* window top", 90.0, ms.STATUS["COND"]),
         ("AeST r_C, Sun", sc["r_C Sun (canonical)"], ms.MUTED),
         ("AeST r_C, 1e11 M☉ galaxy", sc["r_C 1e11 Msun galaxy (canonical)"], ms.MUTED),
         ("AeST μ⁻¹", sc["mu^-1"], ms.MUTED),
         ("AeST L_eq = √2/μ", sc["L_eq = sqrt2/mu"], ms.MUTED)]
for i, (lab, val, col) in enumerate(items):
    a2.barh(i, val, color=col, height=0.55)
    a2.text(val * 1.3, i, f"{val:.3g} pc", va="center", fontsize=8)
a2.set_xscale("log"); a2.set_xlim(1, 1e9)
a2.set_yticks(range(len(items))); a2.set_yticklabels([i[0] for i in items], fontsize=8); a2.invert_yaxis()
a2.set_xlabel("length (pc)")
a2.set_title("AeST's own scales are all far too large", fontsize=10, color=ms.INK)
ms.finish(fig, "c4_02_stiffness_length", "OPEN", "Stiffness length L*",
          f"OPEN: a new FITTED constant; floor {v['canonical']['central']:.1f} / {v['alt']['central']:.1f} pc, edge "
          "~90 pc; no scale of AeST's class produces it (C3)",
          "D10_native_Lstar/d10_native_lstar_results.json; C3_scale_map/c3_scale_map_results.json")
CAPS.append({
    "slug": "c4_02_stiffness_length", "name": "Stiffness length L*", "status": "OPEN",
    "data": "D10: velocity dispersions of four outer Milky Way globulars (NGC 2419, Pal 3, Pal 4, Pal 14), each solved "
            "as a Plummer sphere in the Galaxy's field with v3's stiffened field equation, scanned in L*. C3: the length "
            "scales of AeST's own action (mass term μ, r_C, curl length).",
    "picture": "Left: Δχ² of the globulars against L* for both footings; the leftmost point is L* = 0 (plain AQUAL); "
               "dashed lines mark the 95 % floor; the yellow band is the 20–90 pc window. Right: log bar chart of "
               "the floor and window top against AeST's own length scales (canonical).",
    "why": "Plain AQUAL (L* = 0) is excluded by the globulars and no finite L* beats Newton, so the data give only a "
           "lower bound: L* ≥ 21.68 / 22.85 pc with SPS mass-to-light ratios (2.9–23.8 pc across the M/L and MW-field "
           "brackets). The upper edge near 90 pc comes from the window used in the lanes, not from a fit here. C3 shows "
           "no term in AeST's class makes such a short length: its scales start at kiloparsecs and its equivalent "
           "length √2/μ is ≥ 1.41 Mpc. So L* is a new constant, FITTED, and its origin is open.",
    "numbers": [
        {"what": "L*_95 floor canonical / alt (pc)", "value": f"{v['canonical']['central']:.2f} / {v['alt']['central']:.2f}", "file": P_D10},
        {"what": "band over priors canonical / alt (pc)", "value": f"{v['canonical']['band']} / {v['alt']['band']}", "file": P_D10},
        {"what": "AeST L_eq = √2/μ (pc)", "value": f"{sc['L_eq = sqrt2/mu']:.4g}", "file": P_C3},
        {"what": "AeST r_C Sun / 1e11 M☉ galaxy (pc, canonical)", "value": f"{sc['r_C Sun (canonical)']:.4g} / "
         f"{sc['r_C 1e11 Msun galaxy (canonical)']:.4g}", "file": P_C3},
    ],
    "sources": src([P_D10, P_C3, "doors_push_2026_10_22/D10_native_Lstar/README.md",
                    "covariant_push_2026_10_22/C3_scale_map/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c4_03 cold-mass amount
# ----------------------------------------------------------------------------------------------------------------
P_886 = "campaign_fresh_gravity/CFG886_ratio_fret_without_planck/cfg886_results.json"
P_U1 = "rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content_results.json"
c886 = J(P_886)
u1 = J(P_U1)["numbers"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.1, 1]})
Ra = c886["T3"]["R_a"]; Rb = c886["T3"]["R_b"]
v5 = [r["R"] for r in c886["V5_freeX"]["BAO"]["rows"]]
a1.errorbar([Ra["mean"]], [1], xerr=[Ra["sd"]], fmt="o", color=ms.DATA, capsize=4, ms=7)
a1.errorbar([Rb["mean"]], [2], xerr=[Rb["sd"]], fmt="o", color=ms.DATA, capsize=4, ms=7)
a1.plot([min(v5), max(v5)], [3, 3], color=ms.DATA, lw=5, solid_capstyle="butt")
a1.axvline(c886["K1"]["R_planck"], color=ms.MUTED, ls="--", lw=1.2)
a1.text(c886["K1"]["R_planck"] + 0.08, 0.35, f"input used: {c886['K1']['R_planck']:.3f}\n(Planck-derived)", fontsize=8,
        color=ms.MUTED)
a1.set_yticks([1, 2, 3])
a1.set_yticklabels(["DESI BAO + BBN,\nflat a₀", "SH0ES H₀ + BAO\n+ BBN", "BAO, no flat-a₀\n(free DE)"], fontsize=8.5)
a1.set_ylim(3.6, 0.1)
a1.set_xlabel("R = ω_c / ω_b (cold dark energy to baryons)")
a1.set_title("the abundance is an input, not derived", fontsize=10, color=ms.INK)

N1 = u1["N1"]; N2 = u1["N2"]; N5 = u1["N5"]["satellites"]
bars = [("isotropic hot dust\n(T1, 14,373 equilibria)", N1["max_ratio"]["frozen"]),
        ("tangential anisotropy\nβ = −1", N2["-1.0"]["max_ratio"]),
        ("β = −0.5", N2["-0.5"]["max_ratio"]),
        ("β = 0.1", N2["0.1"]["max_ratio"]),
        ("hosted satellites:\nheld fraction (T3, median)", N5["canonical"]["median_held_frac_MS"])]
y = np.arange(len(bars))
a2.barh(y, [b[1] for b in bars], color=[ms.DATA] * 4 + [ms.STATUS["FAIL"]], height=0.55)
for i, b in enumerate(bars):
    a2.text(b[1] + 0.02, i, f"{b[1]:.3g}", va="center", fontsize=8.5)
a2.axvline(1, color=ms.MODEL, lw=1.6)
a2.text(1.02, -0.6, "= the law's phantom", color=ms.MODEL, fontsize=8.5)
a2.set_xlim(0, 1.45); a2.set_ylim(len(bars) - 0.4, -0.9)
a2.set_yticks(y); a2.set_yticklabels([b[0] for b in bars], fontsize=8)
a2.set_xlabel("largest held dust mass / phantom mass (U1)")
a2.set_title("v3's dust can hold at most the phantom", fontsize=10, color=ms.INK)
ms.finish(fig, "c4_03_cold_mass_amount", "OPEN", "What sets the cold-mass amount",
          f"OPEN: abundance is an initial condition; {c886['K1']['R_planck']:.3f} is an input; held dust ≤ phantom "
          f"(max {N1['max_ratio']['frozen']:.3f}); hosted systems carry none",
          "CFG886 (cfg886_results.json); U1_v3_dust_content N1, N2, N5; C2, C4 READMEs")
CAPS.append({
    "slug": "c4_03_cold_mass_amount", "name": "What sets the cold-mass amount", "status": "OPEN",
    "data": "CFG886 rebuilds the cold-to-baryon ratio R = ω_c/ω_b from DESI DR2 BAO + BBN deuterium (and a SH0ES H₀ "
            "variant, and a free-dark-energy scan) without the Planck fit. U1 solves v3's dust equilibria for 137 "
            "system-footing cases (satellites, Coma UDGs, TDGs, DF2/DF4) and asks how much dust v3 can hold.",
    "picture": "Left: R from the three CFG886 routes (points with 1σ, the free-DE range as a bar) against the 5.364 "
               "input the lanes use (dashed). Right: U1's largest held-dust-to-phantom mass ratio for isotropic and "
               "anisotropic dust, and the median held fraction for hosted satellites; the red line at 1 is the law's "
               "phantom.",
    "why": "In v3 (C2, C4) the dust abundance is a free initial condition, so nothing in the theory sets it; the value "
           "5.364 is an input taken from Planck's ΛCDM fit (inherited input). CFG886 recovers 5.27 ± 0.22 only by "
           "assuming constant dark energy, gets 6.12 ± 0.32 with the local H₀, and with free dark energy BAO + BBN "
           "allow 2.95–8.06: not pinned. Locally, U1's theorem T1 says held dust never exceeds the phantom (largest "
           "ratio 0.666 over 14,373 equilibria; radial anisotropy β > ¼ can exceed it only near the centre, not shown), "
           "and T3 says hosted systems hold none. The amount is not derived anywhere.",
    "numbers": [
        {"what": "R (a) BAO+BBN flat a₀", "value": f"{Ra['mean']:.3f} +- {Ra['sd']:.3f}", "file": P_886},
        {"what": "R (b) SH0ES", "value": f"{Rb['mean']:.3f} +- {Rb['sd']:.3f}", "file": P_886},
        {"what": "R free-DE BAO range", "value": f"{min(v5):.3f} – {max(v5):.3f}", "file": P_886},
        {"what": "Planck-derived input R", "value": f"{c886['K1']['R_planck']:.4f}", "file": P_886},
        {"what": "U1 T1 largest M_τ/M_ph, equilibria count", "value": f"{N1['max_ratio']['frozen']:.4f}, {N1['counts'][0]}", "file": P_U1},
        {"what": "hosted satellites median held fraction (MS)", "value": f"{N5['canonical']['median_held_frac_MS']}", "file": P_U1},
    ],
    "sources": src([P_886, P_U1, "campaign_fresh_gravity/CFG886_ratio_fret_without_planck/README.md",
                    "rebuild_2026_10_22/U1_v3_dust_content/README.md", "covariant_push_2026_10_22/C2_aest_cosmology/README.md",
                    "covariant_push_2026_10_22/C4_khronon_parent/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c4_04 law + a^1 growth + no EFE
# ----------------------------------------------------------------------------------------------------------------
P_F3 = "rebuild_2026_10_22/F3_growth_audit/f3_growth_audit_results.json"
P_S1 = "rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small_results.json"
f3 = J(P_F3)
s1 = J(P_S1)["satellites"]
K4 = f3["K4"]; K5 = f3["K5"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 5.4), gridspec_kw={"width_ratios": [1.45, 1]})
fig.subplots_adjust(wspace=0.45, left=0.07, right=0.97)
kern = [("bsk2_ai0.001", "BSK2 kernel, a_i 1e-3"), ("bsk2_ai0.0001", "BSK2 kernel, a_i 1e-4"),
        ("jeans_ai0.001", "Jeans kernel, a_i 1e-3"), ("jeans_ai0.0001", "Jeans kernel, a_i 1e-4")]
cols = ["#26323a", "#5b7db1", "#8c6d46", "#9b59b6"]
pts = [K4["BS24_scale"], K4["BS24_Eq39_edge_100kpc"], K4["BSK2_floor_1100"]]
for (k, lab), c in zip(kern, cols):
    xs = [p["mu_hMpc"] for p in pts if p.get(k) is not None]
    ys = [p[k]["sigma8_ratio"] for p in pts if p.get(k) is not None]
    a1.plot(xs, ys, "o:", color=c, ms=6, lw=1, label=lab)
mumax = K5["mu_max_hMpc_BS24_Eq39"]
a1.axvspan(1e-3, mumax, color=ms.STATUS["PASS"], alpha=0.08)
a1.axvline(mumax, color=ms.STATUS["PASS"], lw=1.4)
a1.text(mumax * 0.8, 1.04, f"BS24 cap\nμ_K ≤ {mumax:.1f}", ha="right", fontsize=8, color=ms.STATUS["PASS"])
mins = [K5["windows"][w]["mu_min_hMpc"] for w in ["bsk2_ai0.001", "jeans_ai0.001", "bsk2_ai0.0001"]]
a1.axvspan(min(mins), 1e4, color=ms.STATUS["FAIL"], alpha=0.08)
for m in mins:
    a1.axvline(m, color=ms.STATUS["FAIL"], lw=0.9, ls=":")
a1.text(min(mins) * 1.15, 0.2, f"growth needs\nμ_K ≥ {min(mins):.0f}–{max(mins):.0f}", fontsize=8, color=ms.STATUS["FAIL"])
a1.axhline(0.95, color=ms.MODEL, lw=1.3, ls="--")
a1.text(0.03, 0.965, "σ8 within 5 % of the dust limit", color=ms.MODEL, fontsize=8)
a1.set_xscale("log"); a1.set_xlim(1e-2, 1e4); a1.set_ylim(0, 1.15)
a1.set_xlabel("dust mass μ_K  (h/Mpc)")
a1.set_ylabel("linear σ8 / σ8(dust limit)")
a1.legend(fontsize=7.5, loc="center left")
a1.set_title(f"growth leg: empty window, gap {K5['windows']['bsk2_ai0.001']['gap_factor']:.0f}–"
             f"{K5['windows']['bsk2_ai0.0001']['gap_factor']:.0f}×", fontsize=10, color=ms.INK)

iso_c = s1["canonical|primary|S2 AQUAL isolated L*0 E-W"]["Delta"]; efe_c = s1["canonical|primary|S3 AQUAL + EFE (E_mid) L*0 E-W"]["Delta"]
iso_a = s1["alt|primary|S2 AQUAL isolated L*0 E-W"]["Delta"]; efe_a = s1["alt|primary|S3 AQUAL + EFE (E_mid) L*0 E-W"]["Delta"]
vals = [("F3 1-D estimate", -f3["K6"]["dex"]), ("S1 solved, canonical", efe_c - iso_c), ("S1 solved, alt", efe_a - iso_a)]
a2.barh(range(3), [v[1] for v in vals], color=[ms.MUTED, FOOT["canonical"], FOOT["alt"]], height=0.5)
for i, (lab, val) in enumerate(vals):
    a2.text(val + 0.01, i, f"{val:.2f} dex", va="center", fontsize=8.5)
a2.set_yticks(range(3)); a2.set_yticklabels([v[0] for v in vals], fontsize=8.5); a2.invert_yaxis()
a2.set_xlim(0, 0.8)
a2.set_xlabel("boost lost to the external field (dwarf satellites)")
a2.set_title("no-EFE leg: v3 pays with an EFE", fontsize=10, color=ms.INK)
ms.finish(fig, "c4_04_law_growth_no_efe", "FAIL", "Law + a¹ growth + no EFE, local",
          "FAIL: the no-go stands; v3 evades 'no EFE' by having one, and its growth leg has no allowed μ_K",
          "F3_growth_audit/f3_growth_audit_results.json (K4, K5, K6); S1_v3_hosted_small; CFG946 README")
CAPS.append({
    "slug": "c4_04_law_growth_no_efe", "name": "Law + a^1 growth + no EFE, local", "status": "FAIL",
    "data": "A theory statement (CFG946 theorem: a local second-order field that gives the profile-independent deep law "
            "must carry an external-field effect), checked for v3 by F3: linear σ8 of v3's Khronon dust as a function of "
            "its mass μ_K, for two kernels and two start times, and the EFE cost on dwarf satellites (F3's 1-D estimate, "
            "S1's solved value).",
    "picture": "Left: linear σ8 relative to the dust limit at three μ_K values per kernel (log axis). Green: μ_K allowed "
               "by BS24's Eq. 39 cap; red: μ_K needed for σ8 within 5 % (dashed line). The two never meet. Right: the "
               "boost the satellites lose to the external field (F3 estimate vs S1's solve).",
    "why": "The no-go says no local theory can have the law, standard a¹ growth and no EFE at once. v3 does not dodge it: "
           "it pays the no-EFE leg by having an EFE (which costs the satellites 0.58 / 0.57 dex, about twice F3's 1-D "
           "estimate), and the growth leg comes back as an empty μ_K window: growth needs μ_K ≥ 361–2542 h/Mpc, the cap "
           "is 14.8, a gap of 24–172×. Inherited inputs: F3's linear runs use Planck-2018 initial conditions and a "
           "flat w = −1 background (ΛCDM-processed).",
    "numbers": [
        {"what": "BS24 cap on μ_K (h/Mpc)", "value": f"{mumax:.3f}", "file": P_F3},
        {"what": "μ_K needed (h/Mpc): bsk2 a_i 1e-3, jeans 1e-3, bsk2 1e-4", "value": ", ".join(f"{m:.1f}" for m in mins), "file": P_F3},
        {"what": "gap factors", "value": ", ".join(f"{w} {K5['windows'][w]['gap_factor']:.1f}" for w in K5["windows"]), "file": P_F3},
        {"what": "σ8 ratio at the cap (bsk2 1e-3 / jeans 1e-3)", "value":
         f"{K4['BS24_Eq39_edge_100kpc']['bsk2_ai0.001']['sigma8_ratio']:.3f} / {K4['BS24_Eq39_edge_100kpc']['jeans_ai0.001']['sigma8_ratio']:.3f}", "file": P_F3},
        {"what": "EFE cost: F3 1-D / S1 solved canonical / alt (dex)", "value": f"{-f3['K6']['dex']:.3f} / {efe_c - iso_c:.3f} / {efe_a - iso_a:.3f}",
         "file": P_F3 + " ; " + P_S1},
    ],
    "sources": src([P_F3, P_S1, "rebuild_2026_10_22/F3_growth_audit/README.md",
                    "campaign_fresh_gravity/CFG946_option2_phantom_not_cold/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c4_05 radiative stability (STALE -> OPEN grey)
# ----------------------------------------------------------------------------------------------------------------
P_320 = "campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability_results.json"
c320 = J(P_320)["numbers"]
grid = c320["grid"]; summ = c320["summary"]; bound = c320["inputs"]["bound"]
fig, ax = plt.subplots(figsize=(10, 5.4))
Ls = np.array([g["Lambda_sc_GeV"] for g in grid])
ax.scatter(Ls, [g["delta_EFT"] for g in grid], s=20, color=ms.DATA, label="EFT leakage δ_EFT (passes everywhere)")
ax.scatter(Ls, [g["delta_UV"] for g in grid], s=20, facecolors="none", edgecolors=ms.MODEL,
           label="worst-case UV leakage δ_UV (O(1) LV at Λ_sc)")
ax.axhline(bound, color=ms.MODEL, lw=1.4, ls="--")
ax.text(Ls.max(), bound * 1.8, f"bound {bound:g} (KS08, provisional)", ha="right", fontsize=8.5, color=ms.MODEL)
ax.axvline(summ["Lambda_HL_max_GeV"], color=ms.STATUS["COND"], lw=1.4)
ax.text(summ["Lambda_HL_max_GeV"] * 1.1, 1e-15, f"condition: M_* ≤ {summ['Lambda_HL_max_GeV']:.2g} GeV".replace("e+0", "e"), fontsize=8.5,
        color="#8a6a0c")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("strong-coupling cutoff Λ_sc of each chassis grid point (GeV)")
ax.set_ylabel("Lorentz-violation leakage into matter")
ax.legend(fontsize=8.5, loc="lower right")
ax.text(0.01, 0.97, "computed on the retired filtered C-H/K chassis, not v3", transform=ax.transAxes, fontsize=9,
        color=ms.MUTED, va="top", weight="bold")
ms.finish(fig, "c4_05_radiative_stability", "OPEN", "Radiative stability (G12)",
          f"NOT YET RECOMPUTED FOR v3 (was conditional: UV new physics needed at ≤ {summ['Lambda_HL_max_GeV']:.1e} GeV)".replace("e+0", "e"),
          "CFG320_radiative_stability_g12/cfg320_radiative_stability_results.json (old chassis); N0_board_audit")
CAPS.append({
    "slug": "c4_05_radiative_stability", "name": "Radiative stability (G12)", "status": "OPEN",
    "data": "CFG320's gate G12 on the old filtered C-H/K chassis: an 81-point grid of the couplings α_c and c₂, each with "
            "its own strong-coupling cutoff Λ_sc, and the Lorentz-violation leakage into matter from loops (EFT piece) "
            "and from a worst-case UV completion, against a 2σ bound from Klinkhamer & Schreck 2008 (marked provisional "
            "in the lane). The board tile is grey: not yet recomputed for v3 (N0 audit row 54).",
    "picture": "Log-log scatter over the 81 grid points: EFT leakage (dark dots) and worst-case UV leakage (open red) "
               "against each point's cutoff, the bound as a dashed line, and the condition M_* ≤ 9.9e8 GeV as a "
               "vertical line.",
    "why": "On the old chassis the theory is natural (loop corrections to the couplings stay tiny) and the EFT leakage "
           "is at least 40 times under the bound at every point, but a worst-case UV completion passes at only 3 of 81 "
           "points. So the old verdict was conditional: new UV physics must enter below about 1e9 GeV. v3 also has a "
           "preferred foliation, so this bound must be redone with v3's own couplings (batch R5); until then the tile "
           "is grey and the old numbers are shown only as the record.",
    "numbers": [
        {"what": "Λ_sc range (GeV)", "value": f"{summ['Lambda_sc_min']:.3g} – {summ['Lambda_sc_max']:.3g}", "file": P_320},
        {"what": "max δ_EFT vs bound", "value": f"{summ['delta_EFT_max']:.3g} vs {bound:g}", "file": P_320},
        {"what": "δ_UV range; UV-ok points", "value": f"{summ['delta_UV_min']:.3g} – {summ['delta_UV_max']:.3g}; "
         f"{summ['UV_ok_points']}/{summ['n_points']}", "file": P_320},
        {"what": "condition M_* ≤ (GeV)", "value": f"{summ['Lambda_HL_max_GeV']:.4g}", "file": P_320},
    ],
    "sources": src([P_320, "campaign_fresh_gravity/CFG320_radiative_stability_g12/README.md",
                    "rebuild_2026_10_22/N0_board_audit/AUDIT.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c4_06 covariant completion (trilemma schematic)
# ----------------------------------------------------------------------------------------------------------------
P_I1 = "rebuild_2026_10_22/I1_gammaL_causality/i1_gammal_causality_results.json"
i1 = J(P_I1)
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 6.2)
boxes = [
    (0.1, 3.7, "1  Screening needs γ_L", f"C3: AeST's own scales are ≥ kpc;\nL_eq = √2/μ = {c3['Q1']['L_eq_pc'] / 1e6:.2f} Mpc "
     f"vs L* ≈ {v['canonical']['central']:.0f} pc.\nThe stiffness term γ_L must be added.", ms.INK),
    (5.75, 3.7, "2  γ_L is well-posed only untwisted", f"I1: {i1['verdict']}.\nOn a twisting aether (any disc galaxy,\n"
     "the Sun in the Galaxy) Im ω grows without\nbound: Hadamard ill-posed.", ms.STATUS["FAIL"]),
    (2.95, 0.35, "3  Untwisted (v3 Khronon) fails growth", f"F3: linear growth needs μ_K ≥ {min(mins):.0f} h/Mpc,\n"
     f"BS24 cap {mumax:.1f}: gap {K5['windows']['bsk2_ai0.001']['gap_factor']:.0f}–{K5['windows']['bsk2_ai0.0001']['gap_factor']:.0f}×.\n"
     "C7: the twisted v4 (AeST + γ_L) runs away\nat linear order on FRW.", ms.STATUS["FAIL"]),
]
for x0, y0, head, body, col in boxes:
    ax.add_patch(FancyBboxPatch((x0, y0), 4.15, 2.1, boxstyle="round,pad=0.08", fc="white", ec=col, lw=2))
    ax.text(x0 + 0.15, y0 + 1.85, head, fontsize=10, weight="bold", color=col, va="top")
    ax.text(x0 + 0.15, y0 + 1.35, body, fontsize=8.6, color=ms.INK, va="top", linespacing=1.4)
ax.annotate("", xy=(5.7, 4.75), xytext=(4.3, 4.75), arrowprops=dict(arrowstyle="->", color=ms.MUTED, lw=1.5))
ax.annotate("", xy=(6.2, 2.5), xytext=(7.6, 3.6), arrowprops=dict(arrowstyle="->", color=ms.MUTED, lw=1.5))
ax.annotate("", xy=(2.2, 3.6), xytext=(3.1, 2.5), arrowprops=dict(arrowstyle="->", color=ms.MUTED, lw=1.5))
ax.text(5.0, 3.1, "one open escape: native nonlinear v3 run (L1's frozen 512³ plan)", ha="center", va="center", fontsize=9,
        color=ms.STATUS["UNDEC"], weight="bold", bbox=dict(fc="white", ec="none", pad=2), zorder=5)
ms.finish(fig, "c4_06_covariant_completion", "FAIL", "Covariant completion",
          "FAIL: trilemma; screening needs γ_L, γ_L works only untwisted, untwisted (v3) fails growth",
          "C3_scale_map, I1_gammaL_causality, F3_growth_audit (results json); C7_aest_class README")
CAPS.append({
    "slug": "c4_06_covariant_completion", "name": "Covariant completion", "status": "FAIL",
    "data": "No data arrays: a theory tile. Three lanes form the trilemma: C3 (AeST's own length scales), I1 (principal "
            "symbol and Cauchy problem of the γ_L stiffness term on twisting and untwisted aethers), F3 (linear growth of "
            "the untwisted v3 Khronon), with C7 (v4 = AeST + γ_L in a patched CLASS) for the twisted option on FRW.",
    "picture": "Three boxes, one per horn, each with its deciding number, and arrows showing how fixing one horn forces "
               "the next; the centre names the one escape still open.",
    "why": "A covariant parent must (1) screen the law on small scales, which needs the added stiffness term γ_L because "
           "AeST's own scales are all far too large; (2) keep the field equations well-posed, but I1 shows γ_L is "
           "well-posed only where the aether is twist-free, and a disc galaxy or the Sun in the Galaxy forces twist; "
           "(3) the twist-free choice is v3's Khronon, whose linear growth fails (no allowed μ_K window), while the "
           "twisted v4 runs away on FRW (C7). Only a native nonlinear v3 simulation could still rescue growth; until it "
           "runs, the completion fails.",
    "numbers": [
        {"what": "AeST L_eq (pc)", "value": f"{c3['Q1']['L_eq_pc']:.4g}", "file": P_C3},
        {"what": "L* floor canonical (pc)", "value": f"{v['canonical']['central']:.2f}", "file": P_D10},
        {"what": "I1 verdict", "value": i1["verdict"], "file": P_I1},
        {"what": "μ_K needed / cap (h/Mpc)", "value": f"{min(mins):.1f}–{max(mins):.1f} / {mumax:.2f}", "file": P_F3},
    ],
    "sources": src([P_C3, P_I1, P_F3, P_D10, "rebuild_2026_10_22/I1_gammaL_causality/README.md",
                    "covariant_push_2026_10_22/C7_aest_class/README.md", "rebuild_2026_10_22/F3_growth_audit/README.md"]),
})

out = HERE.parent / "captions"
out.mkdir(exist_ok=True)
json.dump(CAPS, open(out / "col4.json", "w"), indent=1, ensure_ascii=False)
print("wrote", len(CAPS), "figures and captions/col4.json")
