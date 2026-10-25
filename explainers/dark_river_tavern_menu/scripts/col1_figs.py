"""Column 1, 'Galaxies': one picture per status-board tile, plus captions/col1.json. Plot and read only; no physics is rerun.

Every plotted number is read from a committed lane file (paths in SRC) or from the committed raw-data tables the lanes read
(SPARC rotmod files, Bovy & Rix 2013 Table 3, Ou+24 Table 1, Lelli+15 TDG table). Thresholds are the lanes' own frozen lines.
The only arithmetic done here is the standard conversion of rotation-curve velocities into accelerations
(g_obs = V^2/R, g_bar from the mass-model velocities at the lane's own per-galaxy Upsilon) and drawing the law
g = nu1(g_bar/a0) g_bar, nu1(y) = 1/2 + sqrt(1/4 + 1/y) (P4's v3 kernel, mu = x/(1+x)).
"""
import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import menu_style as ms  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

R = ms.ROOT
SRC = {
    "P4": "rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json",
    "P4R": "rebuild_2026_10_22/P4_v3_galaxy_tiles/README.md",
    "S2": "rebuild_2026_10_22/S2_v3_lowg_lensing/s2_v3_lowg_lensing_results.json",
    "S4": "rebuild_2026_10_22/S4_v3_muK_clusters/s4_v3_muk_clusters_results.json",
    "P2": "rebuild_2026_10_22/P2_spec_isolated_lensing/p2_spec_isolated_lensing_results.json",
    "U1": "rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content_results.json",
    "D10": "doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json",
    "R4S": "rebuild_2026_10_22/S4_v3_muK_clusters/r4_out/cfg528b_measured_tracers/nu1/"
           "campaign_fresh_gravity__CFG528_sluggs_centrals_mechanism__cfg528b_measured_tracers_results.json",
    "R4N": "rebuild_2026_10_22/S4_v3_muK_clusters/r4_out/cfg528b_measured_tracers/nu1_noown/"
           "campaign_fresh_gravity__CFG528_sluggs_centrals_mechanism__cfg528b_measured_tracers_results.json",
    "S3": "rebuild_2026_10_22/S3_v3_mw_seals/s3_partA_mw_results.json",
}
RAW = {
    "sparc": "real_research/data/sparc_data",
    "kz": "real_research/data/mw_kz11_bovyrix2013_table3.tsv",
    "ou": "real_research/data/mw_rc_ou2024_table1.tsv",
    "tdg": "real_research/data/tidal_dwarfs/lelli2015_tdg.csv",
}
J = {k: json.load(open(R / v)) for k, v in SRC.items() if v.endswith(".json")}
FOOT = {"canonical": ms.DATA, "alt": "#7a5195"}
A0 = {"canonical": 9.360325e-11, "alt": 1.131204e-10}       # FP0 footings, as printed in p4_v3_galaxy_tiles.out
CAP = []


def commit(path):
    out = subprocess.run(["git", "-C", str(R), "log", "-1", "--format=%h", "--", path], capture_output=True, text=True)
    return out.stdout.strip() or "uncommitted"


def srcs(*keys):
    paths = [SRC.get(k, RAW.get(k, k)) for k in keys]
    return [{"path": p, "commit": commit(p)} for p in paths]


def caption(slug, name, status, data, picture, why, numbers, sources):
    CAP.append(dict(slug=slug, name=name, status=status, data=data, picture=picture, why=why, numbers=numbers,
                    sources=sources))


def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    return {h: np.array([float(r[i]) for r in rows[1:]]) for i, h in enumerate(rows[0])}


def fmt(x, n=3):
    return f"{x:+.{n}f}"


# ===================================================================================================  c1_01 SPARC RAR
def tile_sparc():
    slug, status = "c1_01_sparc_rar", "COND"
    T1 = J["P4"]["tiles"]["T1"]
    KPC_S = 3.0857e19                                    # P4 / CFG695 conversion constant
    gals = {}
    d_ = R / RAW["sparc"]
    for f in sorted(d_.iterdir()):
        if not f.name.endswith("_rotmod.dat"):
            continue
        a = np.genfromtxt(f, comments="#")
        if a.ndim == 2 and a.shape[1] >= 6:
            gals[f.name.replace("_rotmod.dat", "")] = a
    fig = plt.figure(figsize=(12.0, 5.2))
    axs = [fig.add_axes([0.06, 0.17, 0.27, 0.60]), fig.add_axes([0.385, 0.17, 0.27, 0.60]),
           fig.add_axes([0.72, 0.17, 0.26, 0.60])]
    chk = {}
    for ax, foot in zip(axs[:2], ("canonical", "alt")):
        rows = T1["footings"][foot]["L24"]["per_galaxy"]
        U = {r["name"]: r["U_rms"] for r in rows}
        GB, GO, W = [], [], []
        for name, a in gals.items():
            u = U[name]
            Rm = a[:, 0] * KPC_S
            vb2 = np.sign(a[:, 3]) * a[:, 3] ** 2 + u * a[:, 4] ** 2 + 1.4 * u * a[:, 5] ** 2
            gb = vb2 * 1e6 / Rm
            go = (a[:, 1] * 1e3) ** 2 / Rm
            ok = (gb > 0) & (go > 0) & (a[:, 1] > 0)
            GB.append(gb[ok]); GO.append(go[ok])
            W.append((1.0 / (np.clip(a[ok, 2], 1, None) / np.clip(a[ok, 1], 1, None)) ** 2))
        GB, GO, W = map(np.concatenate, (GB, GO, W))
        res = np.log10(GO) - np.log10(nu1(GB / A0[foot]) * GB)
        chk[foot] = (math.sqrt(np.sum(W * res ** 2) / np.sum(W)), len(GB))
        ax.scatter(np.log10(GB), np.log10(GO), s=2.5, color=FOOT[foot], alpha=0.25, lw=0, rasterized=True)
        # binned medians of the measured points
        be = np.arange(-12.6, -8.4, 0.3)
        idx = np.digitize(np.log10(GB), be)
        bx = [np.median(np.log10(GB)[idx == i]) for i in range(1, len(be)) if np.sum(idx == i) >= 10]
        by = [np.median(np.log10(GO)[idx == i]) for i in range(1, len(be)) if np.sum(idx == i) >= 10]
        ax.plot(bx, by, "o", ms=4.5, mfc="white", mec=FOOT[foot], mew=1.3, label="binned median (data)")
        xx = np.linspace(-12.8, -8.3, 300)
        ax.plot(xx, np.log10(nu1(10 ** xx / A0[foot]) * 10 ** xx), color=ms.MODEL, lw=2.0,
                label=f"law, a0 = {A0[foot]:.4g}")
        ax.plot(xx, xx, ls="--", color=ms.MUTED, lw=1.0, label="Newton (g = g_bar)")
        st = T1["footings"][foot]["L24"]
        ax.set_title(f"{foot} footing: {len(GB)} points, 175 galaxies\nrms {st['rms']:.4f} dex, median Υ {st['U_median']:.2f}",
                     fontsize=9.5)
        ax.set_xlim(-12.8, -8.3); ax.set_ylim(-12.0, -8.3)
        ax.set_xlabel("log g_bar  [m/s²]  (baryons, lane's per-galaxy Υ)")
        ax.set_ylabel("log g_obs = log V²/R  [m/s²]")
        ax.legend(fontsize=7.5, loc="upper left")
    ax = axs[2]
    bins = np.arange(0.275, 1.226, 0.05)
    for foot, off in (("canonical", 0), ("alt", 1)):
        st = T1["footings"][foot]["L24"]
        u = [r["U_rms"] for r in st["per_galaxy"]]
        ax.hist(u, bins=bins, histtype="step", lw=1.8, color=FOOT[foot], label=f"{foot}: median {st['U_median']:.2f}")
        ax.axvline(st["U_median"], color=FOOT[foot], ls=":", lw=1.4)
    ax.axvspan(0.50, 0.80, color=ms.BAND, alpha=0.7, zorder=0, label="frozen window 0.50–0.80")
    ax.set_xlabel("per-galaxy disc Υ (3.6 μm) fitted by the lane")
    ax.set_ylabel("galaxies")
    ax.set_title("Υ line: median must sit in the window\nχ² line: ≥ 90 % of galaxies with p ≥ 0.001", fontsize=9.5)
    fc, fa = (T1["footings"][f]["L24"]["frac_p_ok"] for f in ("canonical", "alt"))
    ax.text(0.98, 0.62, f"χ² line FAILS on both:\n{fc:.1%} / {fa:.1%} acceptable\n(χ²/dof {T1['footings']['canonical']['L24']['chi2nu']:.2f}"
            f" / {T1['footings']['alt']['L24']['chi2nu']:.2f})", transform=ax.transAxes, ha="right", fontsize=8,
            color=ms.STATUS["FAIL"])
    ax.legend(fontsize=7.5, loc="upper right")
    ms.finish(fig, slug, status, "Rotation curves: the SPARC radial-acceleration relation",
              "CONDITIONAL: canonical passes the rms + Υ line, alt's median Υ 0.44 falls below 0.50; the χ² line fails on both",
              SRC["P4"] + " (per-galaxy Υ, L★ 24 pc); " + RAW["sparc"])
    print(f"[c1_01] check: isolated-law rms at the file's per-galaxy Υ: canonical {chk['canonical'][0]:.4f}, alt {chk['alt'][0]:.4f}"
          f" (file, EFE solved: {T1['footings']['canonical']['L24']['rms']:.4f} / {T1['footings']['alt']['L24']['rms']:.4f}); "
          f"points {chk['canonical'][1]}")
    c, a = T1["footings"]["canonical"]["L24"], T1["footings"]["alt"]["L24"]
    caption(slug, "Rotation curves (SPARC RAR)", status,
            "175 SPARC galaxies (Lelli+16 rotmod files): observed acceleration V²/R against the baryonic acceleration from the "
            "gas, disc and bulge velocities. P4 fitted one disc Υ per galaxy (bulge 1.4Υ) and solved v3's AQUAL law with each "
            "galaxy's external field (Chae+21 environments, 109 of 175) and screening at L★ = 24 and 90 pc.",
            "Left and middle: every measured point (small dots) and binned medians (open circles) against v3's law on the canonical "
            "and the alt footing (red line), with Newton as the dashed diagonal. Right: the distribution of the fitted per-galaxy "
            "Υ on both footings, with the frozen 0.50–0.80 window shaded; P4's Υ grid runs 0.30–1.20, so the piles at the two ends "
            "are galaxies sitting on the grid bounds.",
            "The points follow the law closely on both footings: the rms scatter is 0.054 dex, well inside the 0.110 line. On the "
            "alt footing the larger a₀ makes the fits prefer lighter discs, so the median Υ is 0.44, below the frozen 0.50 window; "
            "that splits the tile, so it is conditional. The χ² line fails on both footings (about 63–64 % of galaxies acceptable "
            "against 90 %), and the record's kernel ν_mono does the same with the same freedom, so the miss is the error budget "
            "or non-circular motions, not something specific to v3. Points are drawn with the isolated law at the file's per-galaxy "
            "Υ; the external field changes the rms by under 0.001 dex.",
            [{"what": "rms (dex), canonical / alt, L★ 24 pc", "value": f"{c['rms']:.4f} / {a['rms']:.4f}", "file": SRC["P4"]},
             {"what": "median Υ, canonical / alt", "value": f"{c['U_median']:.2f} / {a['U_median']:.2f}", "file": SRC["P4"]},
             {"what": "fraction of galaxies with p ≥ 0.001", "value": f"{c['frac_p_ok']:.3f} / {a['frac_p_ok']:.3f}", "file": SRC["P4"]},
             {"what": "χ²/dof", "value": f"{c['chi2nu']:.3f} / {a['chi2nu']:.3f}", "file": SRC["P4"]},
             {"what": "ν_mono same freedom, fraction acceptable", "value":
              f"{T1['footings']['canonical']['nu_mono_iso_perUps']['frac_p_ok']:.3f} / {T1['footings']['alt']['nu_mono_iso_perUps']['frac_p_ok']:.3f}",
              "file": SRC["P4"]}],
            srcs("P4", "P4R", "sparc"))


# ===================================================================================================  c1_02 MeerKAT a0
def tile_meerkat():
    slug, status = "c1_02_meerkat_local_a0", "PASS"
    T2 = J["P4"]["tiles"]["T2"]
    rows = T2["rows"]
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    items = [("MIGHTEE-HI (MeerKAT), REST frame, ν₁\n47 deep galaxies", rows["REST|nu1"]["a0"], rows["REST|nu1"]["q_a0"], ms.DATA),
             ("SPARC, same recipe, ν₁\n123 galaxies", rows["REST|nu1"]["a0_sparc"], rows["REST|nu1"]["q_sparc"], "#3a6f8f"),
             ("MIGHTEE-HI, OBS frame (variant)", rows["OBS|nu1"]["a0"], rows["OBS|nu1"]["q_a0"], ms.MUTED)]
    ys = [2, 1, 0]
    S = rows["REST|nu1"]["a0_sparc"]
    ax.axvspan(S * 10 ** -0.15, S * 10 ** 0.15, color=ms.BAND, alpha=0.6, zorder=0, label="pass line: within ±0.15 dex of SPARC")
    for (lab, a, q, col), y in zip(items, ys):
        ax.plot([q[0], q[3]], [y, y], color=col, lw=1.4)
        ax.plot([q[1], q[2]], [y, y], color=col, lw=5, alpha=0.6, solid_capstyle="butt")
        ax.plot(a, y, "o", color=col, ms=8, mec="white")
        ax.text(q[3] * 1.02, y, f"{a:.3e}", va="center", fontsize=8.5, color=col)
    for f, ls in (("canonical", "-"), ("alt", "--")):
        ax.axvline(A0[f], color=ms.MODEL, ls=ls, lw=1.4, label=f"{f} footing {A0[f]:.4g}")
    ax.set_xscale("log")
    ax.set_yticks(ys); ax.set_yticklabels([i[0] for i in items], fontsize=8.5)
    ax.set_ylim(-0.7, 2.7)
    ax.set_xlabel("a₀ [m/s²]  (thick bar 68 %, thin bar 95 %)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.33)
    d = rows["REST|nu1"]["dlog_M_minus_S"]
    ms.finish(fig, slug, status, "Local a₀ from MeerKAT (MIGHTEE-HI)",
              f"PASS: MeerKAT sits {d:+.3f} dex from SPARC's same-recipe value, against a ±0.15 dex line",
              SRC["P4"] + " tiles.T2.rows")
    caption(slug, "Local a0 from MeerKAT", status,
            "47 MIGHTEE-HI (MeerKAT) galaxies, all deep in the low-acceleration regime, with HI line widths in the rest frame "
            "(the frame CFG309 decided); a₀ estimated with the same recipe as 123 SPARC galaxies, using v3's kernel ν₁.",
            "A log a₀ axis. Each row is an estimate with its 68 % (thick) and 95 % (thin) bootstrap interval: MeerKAT rest frame, "
            "SPARC same recipe, and the observed-frame variant in grey. The grey band is the ±0.15 dex pass line around SPARC; red "
            "lines mark the two footings.",
            "The MeerKAT value lands 0.03 dex above SPARC's same-recipe value, far inside the 0.15 dex line, so the tile passes. The "
            "observed-frame variant (−0.066 dex) also passes, so the verdict does not hinge on the frame. Both footings sit outside "
            "MeerKAT's statistical 95 % interval but inside the recipe's width; the flux-scale systematic is not addressed. "
            "No environment estimate exists for these galaxies, so they are treated as isolated.",
            [{"what": "MeerKAT REST ν₁ a₀ (m/s²), 95 %", "value": f"{rows['REST|nu1']['a0']:.4e} ({rows['REST|nu1']['q_a0'][0]:.3e}–{rows['REST|nu1']['q_a0'][3]:.3e})", "file": SRC["P4"]},
             {"what": "SPARC same recipe a₀", "value": f"{S:.4e}", "file": SRC["P4"]},
             {"what": "log MeerKAT − SPARC (dex)", "value": f"{d:+.4f}", "file": SRC["P4"]},
             {"what": "OBS-frame variant offset (dex)", "value": f"{rows['OBS|nu1']['dlog_M_minus_S']:+.4f}", "file": SRC["P4"]},
             {"what": "MeerKAT vs footings (dex), canonical / alt", "value": f"{rows['REST|nu1']['vs_footing']['canonical']:+.3f} / {rows['REST|nu1']['vs_footing']['alt']:+.3f}", "file": SRC["P4"]}],
            srcs("P4", "P4R", "campaign_fresh_gravity/CFG309_mightee_width_frame/README.md"))


# ===================================================================================================  c1_03 lensing inner
def tile_lens_inner():
    slug, status = "c1_03_lensing_inner", "COND"
    s = J["S2"]
    fig, ax = plt.subplots(figsize=(10.0, 5.2))
    steps = list(s["ladder"]["canonical"].keys())
    short = ["L0 record\n(CFG829)", "L1 kernel\nν₁", "L2 native\nh, Ωm", "L3 forward\nAQUAL ΔΣ", "L4 + hot\nCGM 0.5 M★",
             "L5 + EFE\n(primary)", "maxclu\nfield"]
    x = np.arange(len(short))
    for foot, dx in (("canonical", -0.12), ("alt", 0.12)):
        A = [s["ladder"][foot][k]["blue"]["A"] for k in steps] + [s["cells_central"][f"{foot}|R0|maxclu|blue"]["A"]]
        sA = [s["ladder"][foot][k]["blue"]["sA"] for k in steps] + [s["cells_central"][f"{foot}|R0|maxclu|blue"]["sA"]]
        cls = [s["ladder"][foot][k]["blue"]["cls"] for k in steps] + [s["cells_central"][f"{foot}|R0|maxclu|blue"]["cls"]]
        ax.errorbar(x + dx, A, yerr=2 * np.array(sA), fmt="o", color=FOOT[foot], capsize=3, ms=6, label=f"{foot}: A ± 2σ_A")
        for xi, a, c in zip(x + dx, A, cls):
            if c != "consistent":
                ax.annotate(c, (xi, a), xytext=(6, -12), textcoords="offset points", fontsize=7.5, color=ms.STATUS["COND"])
    ax.axhline(1.0, color=ms.MODEL, lw=1.6, label="A = 1: data = v3 prediction")
    ax.axvspan(4.6, 5.4, color=ms.BAND, alpha=0.5, zorder=0)
    ax.text(5.0, 0.6, "v3 cell\n(primary)", ha="center", fontsize=8, color=ms.MUTED)
    ax.set_xticks(x); ax.set_xticklabels(short, fontsize=8)
    ax.set_ylabel("A = data / model  (blue lenses, B21 window)")
    ax.set_ylim(0.5, 1.35)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="x", visible=False)
    cb, ab = s["cells_central"]["canonical|R0|noclu|blue"], s["cells_central"]["alt|R0|noclu|blue"]
    ms.finish(fig, slug, status, "Isolated-galaxy lensing, inner window (blue lenses)",
              f"CONDITIONAL: A {cb['A']:.2f} (canonical, consistent) / {ab['A']:.2f} (alt, between); the hot CGM step is what moves it",
              SRC["S2"] + " ladder, cells_central")
    caption(slug, "Isolated-galaxy lensing, inner", status,
            "KiDS galaxy–galaxy lensing of isolated blue (late-type) lenses in Brouwer+21's low-acceleration window "
            "(g_bar 10^−13.3–10^−11.9 m/s², 6 points), forward-modelled as v3's ΔΣ over the record's 181,477-lens stack.",
            "The amplitude A = data/model (with 2σ_A bars) at each step of the lane's ladder, from the record's algebraic number to "
            "the v3 cell (AQUAL, hot CGM, external field), and at the maximum-cluster field. The red line A = 1 means data equal "
            "the prediction; 'consistent' is |A − 1| ≤ 2σ_A.",
            "Each ingredient of v3 is added one at a time. The kernel, cosmology and forward-modelling barely move A; adding a hot "
            "circumgalactic gas halo of half the stellar mass drops it by about 0.11, and the external field moves it by at most "
            "0.004 in this window. On the canonical footing A stays consistent with 1; on the alt footing it is 'between' "
            "(−2.9σ) and only becomes consistent at the maximum-cluster field, so the tile is conditional. It hinges on the "
            "unmeasured hot gas of blue lenses and on SPS stellar masses, and it holds only for μ_K < 0.1/Mpc (S4); the μ_K²ψ "
            "term was not included in S2.",
            [{"what": "blue A, v3 primary field, canonical", "value": f"{cb['A']:.3f} ± {cb['sA']:.3f} ({cb['cls']})", "file": SRC["S2"]},
             {"what": "blue A, v3 primary field, alt", "value": f"{ab['A']:.3f} ± {ab['sA']:.3f} ({ab['cls']})", "file": SRC["S2"]},
             {"what": "blue A at maxclu, canonical / alt", "value": f"{s['cells_central']['canonical|R0|maxclu|blue']['A']:.3f} / {s['cells_central']['alt|R0|maxclu|blue']['A']:.3f}", "file": SRC["S2"]},
             {"what": "y_e primary (noclu), canonical / alt", "value": f"{s['y_e']['canonical']['noclu']:.2e} / {s['y_e']['alt']['noclu']:.2e}", "file": SRC["S2"]},
             {"what": "galaxy guard μ_K limit (1/Mpc)", "value": f"{J['S4']['mu_K_gal']['canonical']}", "file": SRC["S4"]}],
            srcs("S2", "rebuild_2026_10_22/S2_v3_lowg_lensing/README.md", "S4"))


# ===================================================================================================  c1_04 lensing all radii
def tile_lens_all():
    slug, status = "c1_04_lensing_all_radii", "UNDEC"
    p = J["P2"]["verdict"]
    fig = plt.figure(figsize=(11.5, 5.2))
    ax = fig.add_axes([0.07, 0.17, 0.42, 0.60]); bx = fig.add_axes([0.58, 0.17, 0.39, 0.60])
    pc, pa = p["canonical"]["profile"], p["alt"]["profile"]
    Rr = np.array(pc["R"])
    ax.errorbar(Rr, Rr * np.array(pc["d"]), yerr=Rr * np.array(pc["sig"]), fmt="o", color=ms.DATA, capsize=2.5, ms=4.5,
                label="GAMA isolated lenses, data (N = 2,251)")
    ax.plot(Rr, Rr * np.array(pc["m_a"]), color=ms.MODEL, lw=1.8, label="v3, no external field (a), canonical")
    ax.plot(Rr, Rr * np.array(pc["m_b"]), color=ms.MODEL, lw=1.4, ls="--", label="v3, catalogue field (b), canonical")
    ax.plot(Rr, Rr * np.array(pa["m_a"]), color=FOOT["alt"], lw=1.2, ls="-.", label="v3 (a), alt")
    ax.axhline(0, color=ms.MUTED, lw=0.8)
    ax.axvspan(1.1, 2.6, color=ms.BAND, alpha=0.6, zorder=0)
    ax.text(1.7, -2.6, "O2: 1.1–2.6 Mpc", ha="center", fontsize=8, color=ms.MUTED)
    ax.set_xscale("log"); ax.set_ylim(-3.2, 9.5)
    ax.set_xlabel("projected radius R [Mpc]"); ax.set_ylabel("R × ΔΣ  [Mpc · M☉/pc²]")
    ax.set_title("P2: spectroscopic isolation — (a) and (b) differ by 0.87σ / 0.96σ;\nthe frozen line needs 3σ (N ≈ 22–26k)",
                 fontsize=9)
    ax.legend(fontsize=7.3, loc="upper right")
    g = J["S4"]["galaxy"]
    mus = sorted({float(k.split("|")[0]) for k in g})
    mus = [m for m in mus if m <= 10.0]
    for foot, mk in (("canonical", "o"), ("alt", "s")):
        dev = [g[f"{k}|{foot}|0.0"]["maxdev_guard"] for k in [next(kk.split('|')[0] for kk in g if float(kk.split('|')[0]) == m) for m in mus]]
        bx.plot(mus, dev, mk + "-", color=FOOT[foot], label=f"{foot}", ms=5)
    bx.axhline(0.14, color=ms.STATUS["FAIL"], lw=1.4, ls="--", label="guard: |v3/law − 1| ≤ 0.14 (R ≤ 1.1 Mpc)")
    bx.set_xscale("log"); bx.set_yscale("log")
    bx.set_xlabel("μ_K [1/Mpc]  (v3's μ_K²ψ term)"); bx.set_ylabel("max |v3 / law − 1| at R ≤ 1.1 Mpc")
    k01 = next(kk.split('|')[0] for kk in g if float(kk.split('|')[0]) == 0.1)
    dc, da = g[f"{k01}|canonical|0.0"]["dchi2_zero_vs_law"], g[f"{k01}|alt|0.0"]["dchi2_zero_vs_law"]
    bx.annotate(f"μ_K = 0.1: Δχ² +{dc:.0f} / +{da:.0f}", (0.1, g[f"{k01}|canonical|0.0"]["maxdev_guard"]), xytext=(0.13, 0.03),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=ms.MUTED))
    bx.set_title("S4: every μ_K ≥ 0.1/Mpc breaks isolated-galaxy lensing", fontsize=9)
    bx.legend(fontsize=7.5, loc="lower right")
    ms.finish(fig, slug, status, "Isolated-galaxy lensing at all radii",
              "UNDECIDED: the clean sample is too small to tell v3's external-field readings apart; the μ_K² term must stay below 0.1/Mpc",
              SRC["P2"] + " verdict.profile; " + SRC["S4"] + " galaxy")
    a3 = J["P2"]["amplitudes_S3"]
    caption(slug, "Isolated-galaxy lensing, all radii", status,
            "Weak lensing out to 3 Mpc around 2,251 spectroscopically isolated GAMA galaxies (P2), plus S4's test of v3's μ_K²ψ "
            "term against Brouwer+21's isolated-lens profile with its released covariance.",
            "Left: the measured excess surface density ΔΣ (multiplied by R so the outer points show) with errors against v3's prediction with no external field (solid red) and "
            "with the field the catalogue's own baryons imply (dashed), canonical footing; the alt no-field curve is dash-dot. "
            "Right: the largest departure of v3 from the plain law inside 1.1 Mpc as μ_K grows, against the 0.14 guard line.",
            "Beyond 1.1 Mpc the stack sits below the zero-field prediction and is consistent with the catalogue-field one, but the two "
            "predictions differ by under 1σ with this sample; the frozen line needs 3σ, which needs roughly ten times more lenses, so "
            "the tile is undecided. Separately, S4 finds that any μ_K of 0.1/Mpc or more makes v3 depart from the law by more than "
            "the guard inside 1.1 Mpc (Δχ² +110 / +190 at 0.1), so the tile can only stay open if μ_K is below that.",
            [{"what": "decisiveness S (σ), canonical / alt", "value": "0.87 / 0.96 (frozen line 3σ)", "file": "rebuild_2026_10_22/P2_spec_isolated_lensing/README.md"},
             {"what": "lenses needed for 3σ, canonical / alt", "value": "≈ 26,500 / 22,000", "file": "rebuild_2026_10_22/P2_spec_isolated_lensing/README.md"},
             {"what": "Δχ² vs law at μ_K = 0.1/Mpc, canonical / alt", "value": f"+{dc:.1f} / +{da:.1f}", "file": SRC["S4"]},
             {"what": "guard max dev at μ_K = 0.1, canonical", "value": f"{g[f'{k01}|canonical|0.0']['maxdev_guard']:.3f} (line 0.14)", "file": SRC["S4"]}],
            srcs("P2", "rebuild_2026_10_22/P2_spec_isolated_lensing/README.md", "S4"))
    return a3


# ===================================================================================================  c1_05 tidal dwarfs
def tile_tdg():
    slug, status = "c1_05_tidal_dwarfs_df2_df4", "PASS"
    import csv
    rows = list(csv.DictReader(open(R / RAW["tdg"])))
    td = J["U1"]["numbers"]["N5"]["tdg"]
    T5 = J["P4"]["tiles"]["T5"]["footings"]
    fig = plt.figure(figsize=(12.0, 5.2))
    a1 = fig.add_axes([0.105, 0.17, 0.215, 0.60]); a2 = fig.add_axes([0.475, 0.17, 0.25, 0.60]); a3 = fig.add_axes([0.80, 0.17, 0.18, 0.60])
    names = [r["object"] for r in rows]
    lr = np.array([math.log10(float(r["Mdyn_over_Mbar"])) for r in rows])
    el = np.array([float(r["e_Mdyn_over_Mbar"]) / (float(r["Mdyn_over_Mbar"]) * math.log(10)) for r in rows])
    y = np.arange(len(rows))
    a1.errorbar(lr, y, xerr=el, fmt="o", color=ms.DATA, capsize=3)
    a1.axvline(0, color=ms.MODEL, lw=1.8, label="dust-free v3 = Newton")
    a1.set_yticks(y); a1.set_yticklabels(names, fontsize=8)
    a1.set_xlabel("log M_dyn / M_bar  (Lelli+15 table)"); a1.set_ylim(-0.6, len(rows) + 0.2)
    a1.text(0.0, len(rows) - 0.35, "dust-free v3 = Newton", ha="center", fontsize=7.5, color=ms.MODEL)
    a1.set_title("six tidal dwarf galaxies", fontsize=9.5); a1.grid(axis="y", visible=False)
    c = T5["canonical"]; al = T5["alt"]
    lab = ["v3 own dynamics:\ndust-free (B0)", "posited multi-stream\ndust held (B1-MS)", "static AQUAL + host\nfield, canonical",
           "static AQUAL + host\nfield, alt", "isolated law,\ncanonical"]
    vals = [(td["canonical"]["TDG_B0"]["rbar"], td["canonical"]["TDG_B0"]["se"]),
            (td["canonical"]["TDG_B1_MS"]["rbar"], td["canonical"]["TDG_B1_MS"]["se"]),
            (c["L24"]["T"]["rbar"], c["L24"]["T"]["se"]), (al["L24"]["T"]["rbar"], al["L24"]["T"]["se"]),
            (c["T_law_isolated"]["rbar"], c["T_law_isolated"]["se"])]
    cols = [ms.STATUS["PASS"], ms.MUTED, ms.STATUS["FAIL"], ms.STATUS["FAIL"], ms.MUTED]
    yy = np.arange(len(lab))[::-1]
    for (v, e), yi, col in zip(vals, yy, cols):
        a2.errorbar(v, yi, xerr=2 * e, fmt="o", color=col, capsize=3, ms=7)
        a2.text(v, yi + 0.22, f"{v:+.3f} ± {e:.3f}", ha="center", fontsize=7.5, color=col)
    a2.axvline(0, color=ms.MODEL, lw=1.4); a2.set_ylim(-0.5, len(lab) - 0.3)
    a2.set_yticks(yy); a2.set_yticklabels(lab, fontsize=8); a2.grid(axis="y", visible=False)
    a2.set_xlabel("mean residual r̄ = data − model [dex], ±2 se")
    a2.set_title("which reading of v3 the TDGs allow", fontsize=9.5)
    df = td["canonical"]["DF_B0"]
    obs = [8.5, 6.3]
    xs = np.arange(2)
    a3.bar(xs - 0.27, obs, 0.25, color=ms.DATA, label="observed σ")
    a3.bar(xs, df["sigma_pred"], 0.25, color=ms.STATUS["PASS"], label="dust-free v3")
    a3.bar(xs + 0.27, [p_["sigma_pred"] for p_ in c["L24"]["U_points"]], 0.25, color=ms.STATUS["FAIL"], alpha=0.8, label="static AQUAL + field")
    a3.set_xticks(xs); a3.set_xticklabels(["DF2", "DF4"]); a3.set_ylabel("σ [km/s], canonical")
    a3.legend(fontsize=7, loc="upper right"); a3.set_ylim(0, 24); a3.grid(axis="x", visible=False)
    a3.set_title(f"r = {df['r'][0]:+.2f} / {df['r'][1]:+.2f} ln", fontsize=9)
    ms.finish(fig, slug, status, "Tidal dwarfs and NGC 1052-DF2 / DF4",
              "PASS (native, no knob): hosted systems that fall with their host carry no held dust, so v3 predicts Newton, and the data sit there",
              SRC["U1"] + " numbers.N5.tdg; " + SRC["P4"] + " T5; " + RAW["tdg"])
    caption(slug, "Tidal dwarfs, NGC 1052-DF2/DF4", status,
            "Six tidal dwarf galaxies (Lelli+15: rotation, baryonic and dynamical masses) and the two ultra-diffuse galaxies "
            "NGC 1052-DF2 and DF4 (velocity dispersions), all sitting in their hosts' fields (g_e 0.15–0.28 a₀).",
            "Left: each TDG's measured dynamical-to-baryonic mass ratio (log) with its error; the red line at zero is what dust-free "
            "v3 (Newton) predicts. Middle: the mean residual with ±2 se for each reading of v3 — dust-free (U1's own dynamics), "
            "posited multi-stream dust, the static AQUAL solution with the host field (P4), and the isolated law. Right: DF2 / DF4 "
            "observed σ against dust-free v3 and static AQUAL.",
            "Solved as a static AQUAL problem in the host's field, v3 over-predicts these systems: the TDGs sit −0.59 dex below it and "
            "DF2/DF4 −1.66 ln below (P4, a fail). U1 then showed from v3's own equations that a system falling freely with its host "
            "cannot hold dust (the host's pull on the dust is exactly the external-field term), so v3's own prediction is Newtonian. "
            "The data sit on that: TDGs +0.055 ± 0.114 dex, DF2/DF4 +0.30 / −0.24 ln, with no knob. TDG discs have turned less than "
            "one orbit, and every estimator assumes equilibrium.",
            [{"what": "TDG r̄, dust-free (B0)", "value": f"{td['canonical']['TDG_B0']['rbar']:+.3f} ± {td['canonical']['TDG_B0']['se']:.3f} dex", "file": SRC["U1"]},
             {"what": "DF2 / DF4 r, dust-free", "value": f"{df['r'][0]:+.3f} / {df['r'][1]:+.3f} ln", "file": SRC["U1"]},
             {"what": "DF2 / DF4 σ_pred dust-free (km/s)", "value": f"{df['sigma_pred'][0]:.2f} / {df['sigma_pred'][1]:.2f}", "file": SRC["U1"]},
             {"what": "TDG r̄, static AQUAL + field (L★ 24), canonical / alt", "value": f"{c['L24']['T']['rbar']:+.3f} ± {c['L24']['T']['se']:.3f} / {al['L24']['T']['rbar']:+.3f} ± {al['L24']['T']['se']:.3f} dex", "file": SRC["P4"]},
             {"what": "DF2/DF4 static AQUAL σ_pred, canonical (km/s)", "value": " / ".join(f"{p_['sigma_pred']:.1f}" for p_ in c["L24"]["U_points"]), "file": SRC["P4"]},
             {"what": "DF2/DF4 observed σ (km/s)", "value": "8.5 / 6.3", "file": SRC["P4R"]},
             {"what": "TDG r̄, posited multi-stream dust (B1-MS), canonical", "value": f"{td['canonical']['TDG_B1_MS']['rbar']:+.3f} ± {td['canonical']['TDG_B1_MS']['se']:.3f}", "file": SRC["U1"]}],
            srcs("U1", "rebuild_2026_10_22/U1_v3_dust_content/README.md", "P4", "rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.out", "P4R", "tdg"))
    return lr


# ===================================================================================================  c1_06 globulars
def tile_globulars():
    slug, status = "c1_06_outer_globulars_lstar", "COND"
    d = J["D10"]
    fig = plt.figure(figsize=(11.5, 5.2))
    ax = fig.add_axes([0.07, 0.17, 0.43, 0.60]); bx = fig.add_axes([0.58, 0.17, 0.39, 0.60])
    x_aq, x_nw = 1.0, 800.0
    for foot in ("canonical", "alt"):
        c = d[f"chi2_curve|{foot}|central"]
        ch = np.array(c["chi2"]); dch = ch - ch.min()
        L = np.array([float(v) for v in c["L"][1:-1]])
        ax.plot(L, dch[1:-1], "-", color=FOOT[foot], lw=1.8, label=f"{foot}: L★₉₅ = {d['verdict'][foot]['central']:.2f} pc")
        ax.plot([x_aq], [dch[0]], "o", color=FOOT[foot]); ax.plot([x_nw], [dch[-1]], "s", color=FOOT[foot])
        ax.axvline(d["verdict"][foot]["central"], color=FOOT[foot], ls=":", lw=1.3)
    ax.axhline(3.84, color=ms.STATUS["FAIL"], ls="--", lw=1.3, label="Δχ² = 3.84 (95 %)")
    ax.axvspan(20, 90, color=ms.BAND, alpha=0.5, zorder=0, label="[20, 90] pc window")
    ax.set_xscale("log"); ax.set_xlim(0.7, 1200)
    ax.set_xticks([1, 10, 100, 800]); ax.set_xticklabels(["AQUAL\n(L★ = 0)", "10", "100", "Newton\n(L★ → ∞)"])
    ax.set_xlabel("screening length L★ [pc]"); ax.set_ylabel("Δχ² (three outer globulars, central case)")
    ax.legend(fontsize=7.8, loc="upper right")
    c = d["chi2_curve|canonical|central"]
    L = np.array([float(v) for v in c["L"][1:-1]])
    for n, col in (("Pal 4", "#c0392b"), ("Pal 14", "#d4a017"), ("NGC 2419", "#3a6f8f"), ("Pal 3", ms.MUTED)):
        v = np.array(c["per_cluster"][n]); v = v - v.min()
        ls = ":" if n == "Pal 3" else "-"
        bx.plot(L, v[1:-1], ls, color=col, lw=1.6, label=n + (" (not in primary)" if n == "Pal 3" else ""))
        bx.plot([x_aq], [v[0]], "o", color=col); bx.plot([x_nw], [v[-1]], "s", color=col)
    bx.set_xscale("log"); bx.set_xlim(0.7, 1200)
    bx.set_xticks([1, 10, 100, 800]); bx.set_xticklabels(["AQUAL", "10", "100", "Newton"])
    bx.set_xlabel("L★ [pc]"); bx.set_ylabel("per-cluster Δχ² (canonical)")
    bx.set_title("Pal 4 and Pal 14 carry the bound", fontsize=9.5)
    bx.legend(fontsize=7.8, loc="upper right")
    v = d["verdict"]
    ms.finish(fig, slug, status, "Outer globular clusters: the L★ screening floor",
              f"CONDITIONAL: unscreened AQUAL excluded; floor L★ ≥ {v['canonical']['central']:.2f} / {v['alt']['central']:.2f} pc with SPS M/L, "
              f"but the M/L band reaches {v['canonical']['band'][0]:.2f} pc",
              SRC["D10"] + " chi2_curve, verdict")
    caption(slug, "Outer globulars: L* floor", status,
            "Line-of-sight velocity dispersions of the distant Milky Way globulars NGC 2419, Pal 4 and Pal 14 (Pal 3 reported), "
            "each solved as a Plummer sphere in the Galaxy's field with v3's stiffened field equation; SPS stellar M/L (Υ_V "
            "logN(1.6, 0.15 dex)), binary fraction 0.3.",
            "Left: Δχ² against the screening length L★ on both footings, from unscreened AQUAL (left end) to Newton (right end); "
            "the red dashed line is the 95 % cut and the dotted verticals the resulting floors. Right: each cluster's own Δχ² "
            "(canonical), showing which clusters set the bound.",
            "Unscreened AQUAL predicts dispersions well above the measured ones for Pal 4 and Pal 14, so it is excluded in every "
            "cell; screening with L★ of about 22 pc or more brings v3 back to the data, and no finite L★ beats Newton, so this is "
            "a lower bound only. The floor is set by the M/L prior: with the mass-function-slope M/L (CFG332) the band drops to "
            "3–10 pc and straddles the 20 pc window edge, which is why the tile is conditional.",
            [{"what": "L★₉₅ central, canonical / alt (pc)", "value": f"{v['canonical']['central']:.2f} / {v['alt']['central']:.2f}", "file": SRC["D10"]},
             {"what": "band over Υ prior and MW field, canonical", "value": f"{v['canonical']['band'][0]:.2f}–{v['canonical']['band'][1]:.2f} pc", "file": SRC["D10"]},
             {"what": "band, alt", "value": f"{v['alt']['band'][0]:.2f}–{v['alt']['band'][1]:.2f} pc", "file": SRC["D10"]},
             {"what": "Δχ² at AQUAL (central, canonical)", "value": f"{np.array(d['chi2_curve|canonical|central']['chi2'])[0] - min(d['chi2_curve|canonical|central']['chi2']):.2f}", "file": SRC["D10"]},
             {"what": "AQUAL excluded in all cells", "value": str(v["canonical"]["AQUAL_excluded_all_cells"]), "file": SRC["D10"]}],
            srcs("D10", "doors_push_2026_10_22/D10_native_Lstar/README.md"))


# ===================================================================================================  c1_07 SLUGGS
def tile_sluggs():
    slug, status = "c1_07_sluggs_central_ellipticals", "UNDEC"
    d, dn = J["R4S"], J["R4N"]
    gals = ["NGC4486", "NGC4365", "NGC4374", "NGC5846"]
    lab = ["M87\n(NGC 4486)", "NGC 4365", "NGC 4374", "NGC 5846"]
    fig, ax = plt.subplots(figsize=(10.0, 5.2))
    x = np.arange(4)
    sets = [("M own", "measured tracers (row M own)", "s", 0.6), ("J joint best case", "joint best case J", "o", 1.0)]
    k = 0
    for rkey, rlab, mk, alpha in sets:
        for foot in ("canonical", "alt"):
            row = d["rows"][rkey][foot]
            off = np.array([row["per"][g] for g in gals]); Z = np.array([row["Z"][g] for g in gals])
            sig = off / Z
            dx = -0.27 + 0.18 * k
            ax.errorbar(x + dx, off, yerr=2 * sig, fmt=mk, color=FOOT[foot], alpha=alpha, capsize=3, ms=6,
                        label=f"{rlab}, {foot}: mean {row['mean']:+.3f} ± {row['err']:.3f}")
            k += 1
    ax.axhline(0, color=ms.MODEL, lw=1.6, label="v3 law (ν₁, all baryons)")
    ax.set_xticks(x); ax.set_xticklabels(lab)
    ax.set_ylabel("offset log σ_obs − log σ_v3 [dex], ±2σ (statistical)")
    ax.legend(fontsize=7.3, loc="lower left", ncol=1)
    ax.set_ylim(-0.42, 0.32); ax.grid(axis="x", visible=False)
    ja, jn = d["rows"]["J joint best case"]["alt"]["Z_class"], dn["rows"]["J joint best case"]["alt"]["Z_class"]
    ms.finish(fig, slug, status, "Central ellipticals (SLUGGS globular-cluster kinematics)",
              f"UNDECIDED: genuine tension {ja:.1f}σ in the joint best case ({jn:.1f}σ without ownership); 1 of 4 cleared",
              SRC["R4S"].split("/r4_out")[0] + "/r4_out/cfg528b_measured_tracers/{nu1,nu1_noown}")
    caption(slug, "Central ellipticals (SLUGGS)", status,
            "Globular-cluster velocity dispersions at large radius around four central ellipticals (M87, NGC 4365, NGC 4374, "
            "NGC 5846) from SLUGGS, with measured GC density profiles and anisotropy where available (CFG528b), rerun by S4 with "
            "v3's kernel ν₁.",
            "Each galaxy's offset between the measured and the v3-predicted dispersion (dex) with ±2σ statistical bars, for the "
            "measured-tracer row and for the joint best case (every admissible lever pushed in the law's favour), on both footings. "
            "The red line at zero is the law.",
            "Three of the four centrals sit well above the law, by 0.09–0.15 dex even in the joint best case; only NGC 4374 "
            "is cleared. The class tension is 3.1σ on the less favourable footing (3.3σ if host ownership is dropped, as v3 has no "
            "ownership rule). Mass-side levers (IMF, distance, hot gas, external field) cannot remove it; only the unmeasured "
            "tracer slope and anisotropy for three of the four could, so the tile stays undecided. The errors are statistical only.",
            [{"what": "joint best case class Z, canonical / alt", "value": f"{d['rows']['J joint best case']['canonical']['Z_class']:.2f} / {ja:.2f}", "file": SRC["R4S"]},
             {"what": "joint best case class Z without ownership, alt", "value": f"{jn:.2f}", "file": SRC["R4N"]},
             {"what": "joint best case mean offset, canonical / alt (dex)", "value": f"{d['rows']['J joint best case']['canonical']['mean']:+.3f} / {d['rows']['J joint best case']['alt']['mean']:+.3f}", "file": SRC["R4S"]},
             {"what": "cleared (of 4)", "value": f"{d['rows']['J joint best case']['alt']['n_cleared']}", "file": SRC["R4S"]},
             {"what": "record (ν_mono) joint best case Z, alt", "value": "2.76 (2.8σ)", "file": "campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.out"}],
            srcs("R4S", "R4N", "campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.out",
                 "rebuild_2026_10_22/S4_v3_muK_clusters/README.md"))


# ===================================================================================================  c1_08 groups
def tile_groups():
    slug, status = "c1_08_galaxy_groups_bfjr", "PASS"
    F = J["P4"]["tiles"]["T3"]["footings"]
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    xs = np.array([0.0, 1.0, 2.0])
    tot0 = F["canonical"]["v3_isolated"]["tot"]
    ax.axhspan(-2 * tot0, 2 * tot0, color=ms.BAND, alpha=0.6, zorder=0, label=f"CONSISTENT: |Z| < 2 (±{2 * tot0:.3f} dex)")
    ax.axhline(0, color=ms.MODEL, lw=1.6, label="v3 law on the catalogue baryons")
    for foot, dx in (("canonical", -0.08), ("alt", 0.08)):
        cells = [F[foot]["v3_isolated"], F[foot]["EFE_sensitivity"]["ge=0.01"], F[foot]["EFE_sensitivity"]["ge=0.03"]]
        m = [c["mean"] for c in cells]; t = [c["tot"] for c in cells]
        ax.errorbar(xs + dx, m, yerr=t, fmt="o", color=FOOT[foot], capsize=3, ms=7, label=f"{foot}")
        for xi, c in zip(xs, cells):
            ax.annotate(f"Z {c['Z']:+.2f}  {c['verdict']}", (xi + dx, c["mean"]), xytext=(10 if foot == "alt" else -10, -3),
                        ha="left" if foot == "alt" else "right", textcoords="offset points", fontsize=7.5,
                        color=ms.STATUS["FAIL"] if c["verdict"] != "CONSISTENT" else FOOT[foot])
    ax.text(2.0, -0.085, "0.03 a₀ is the low end of\nSPARC galaxies' environments (0.03–0.06 a₀)", ha="center", fontsize=7.5,
            color=ms.MUTED)
    ax.set_xticks(xs); ax.set_xticklabels(["isolated\n(g_e = 0, the frozen primary)", "g_e = 0.01 a₀", "g_e = 0.03 a₀"])
    ax.set_xlabel("external field solved for every group (no group field is on disk)")
    ax.set_ylabel("mean offset, data − v3 [dex] (63 groups), ±1σ_tot")
    ax.set_xlim(-0.8, 2.6); ax.set_ylim(-0.1, 0.22); ax.grid(axis="x", visible=False)
    ax.legend(fontsize=8, loc="upper left")
    ms.finish(fig, slug, status, "Galaxy groups: the baryonic Faber–Jackson relation",
              f"PASS (isolated): {F['canonical']['v3_isolated']['mean']:+.3f} / {F['alt']['v3_isolated']['mean']:+.3f} dex; "
              "ABOVE LAW if the groups sit in a field ≥ 0.03 a₀",
              SRC["P4"] + " tiles.T3.footings")
    c, a = F["canonical"], F["alt"]
    caption(slug, "Galaxy groups (BFJR)", status,
            "63 galaxy groups from Tian+2026 (member velocity dispersion, mean projected radius, K-band + X-ray-gas baryonic mass), "
            "scored with v3's law on the catalogue baryons with a whole-system aperture.",
            "The mean offset of the groups from v3 (with total error) when the groups are taken as isolated, and when an external "
            "field of 0.01 and 0.03 a₀ is solved, on both footings. The grey band is the CONSISTENT zone |Z| < 2.",
            "Taken as isolated, the groups sit on the law: +0.010 / −0.010 dex, Z ±0.31, with no supply or edge rule (v3 has none). "
            "Every aperture variant stays consistent. The pass depends on the groups' external field, which is not on disk: at "
            "0.01 a₀ they stay consistent (Z 1.94 / 1.46), but at 0.03 a₀, the low end of SPARC environments, they sit above the law "
            "(Z 4.7 / 4.5). The baryon masses inherit a Kroupa K-band M/L. The μ_K² term was not included.",
            [{"what": "isolated mean offset, canonical / alt (dex)", "value": f"{c['v3_isolated']['mean']:+.4f} / {a['v3_isolated']['mean']:+.4f}", "file": SRC["P4"]},
             {"what": "isolated Z", "value": f"{c['v3_isolated']['Z']:+.2f} / {a['v3_isolated']['Z']:+.2f}", "file": SRC["P4"]},
             {"what": "g_e 0.01 a₀: Z", "value": f"{c['EFE_sensitivity']['ge=0.01']['Z']:+.2f} / {a['EFE_sensitivity']['ge=0.01']['Z']:+.2f}", "file": SRC["P4"]},
             {"what": "g_e 0.03 a₀: offset, Z", "value": f"{c['EFE_sensitivity']['ge=0.03']['mean']:+.3f} (Z {c['EFE_sensitivity']['ge=0.03']['Z']:+.2f}) / {a['EFE_sensitivity']['ge=0.03']['mean']:+.3f} (Z {a['EFE_sensitivity']['ge=0.03']['Z']:+.2f})", "file": SRC["P4"]}],
            srcs("P4", "P4R"))


# ===================================================================================================  c1_09 MW vertical force
def tile_mw_kz():
    slug, status = "c1_09_mw_vertical_force", "FAIL"
    T4 = J["P4"]["tiles"]["T4"]
    BR = load_tsv(R / RAW["kz"])
    R0 = 8.122                                                   # P4's R0_MW
    Rr = BR["R_kpc"] + (R0 - 8.0); K = BR["Kz11_o2piG"]; E = np.hypot(BR["dKz11_o2piG"], 0.05 * K)
    o = np.argsort(Rr)
    fig, ax = plt.subplots(figsize=(10.0, 5.2))
    ax.errorbar(Rr, K, yerr=E, fmt="o", color=ms.DATA, ms=4, capsize=2, label="Bovy & Rix 2013, 43 MAPs (K_z at 1.1 kpc)")
    for bname, m in T4["models"].items():
        if bname == "B1_McMillan17":
            continue
        ax.plot(Rr[o], np.array(m["canonical"]["F0|L24"]["K"])[o], color=ms.MODEL, lw=0.8, alpha=0.35)
    ax.plot([], [], color=ms.MODEL, lw=0.8, alpha=0.35, label="v3, other baryon models (B2, B2b, B3), canonical")
    for foot, ls in (("canonical", "-"), ("alt", "--")):
        m = T4["models"]["B1_McMillan17"][foot]["F0|L24"]
        ax.plot(Rr[o], np.array(m["K"])[o], color=ms.MODEL, lw=2.0, ls=ls,
                label=f"v3 AQUAL disc, McMillan17, {foot}: χ² {m['chi2_kz']:.1f}")
    ax.set_yscale("log")
    ax.set_xlabel("Galactocentric radius R [kpc]"); ax.set_ylabel("K_z(1.1 kpc) / 2πG  [M☉/pc²]")
    ax.legend(fontsize=7.8, loc="upper right")
    ax.text(0.02, 0.05, f"pass line: χ² ≤ {T4['LINE_chi2_0p99']:.1f} (99 %, 43 points)\nat R₀: data 66.4 ± 2.2, v3 "
            f"{T4['models']['B1_McMillan17']['canonical']['F0|L24']['K_R0']:.1f} / {T4['models']['B1_McMillan17']['alt']['F0|L24']['K_R0']:.1f}",
            transform=ax.transAxes, fontsize=8.5, color=ms.STATUS["FAIL"])
    ms.finish(fig, slug, status, "Milky Way vertical force",
              "FAIL: v3's disc-like AQUAL phantom over-predicts K_z for every baryon model on both footings",
              SRC["P4"] + " tiles.T4.models; " + RAW["kz"])
    b = T4["models"]
    caption(slug, "MW vertical force (round rule)", status,
            "The vertical force K_z at 1.1 kpc above the Galactic plane for 43 mono-abundance populations (Bovy & Rix 2013, "
            "with a 5 % error floor), against v3's AQUAL solution for the Milky Way's baryons (McMillan17 and three bracketing "
            "baryon models).",
            "Measured K_z against radius (log scale) with errors; the thick red lines are v3 on the canonical (solid) and alt "
            "(dashed) footings for McMillan17's baryons, the faint lines are v3 for the other baryon models.",
            "The record's pass used a round enclosed-mass rule that v3 does not have. v3's own AQUAL phantom is disc-like, so it "
            "adds vertical force where the disc is: K_z at the Sun comes out 92.3 / 96.9 against 66.4 ± 2.2, with a longer scale "
            "length than the data. χ² is 178 / 251 against the 67.5 line, and every baryon model fails, as do screening and a "
            "0.03 a₀ field. McMillan17 is partly halo-fitted; the other models bracket that.",
            [{"what": "χ²_Kz McMillan17, canonical / alt", "value": f"{b['B1_McMillan17']['canonical']['F0|L24']['chi2_kz']:.1f} / {b['B1_McMillan17']['alt']['F0|L24']['chi2_kz']:.1f}", "file": SRC["P4"]},
             {"what": "pass line χ²₀.₉₉(43)", "value": f"{T4['LINE_chi2_0p99']:.2f}", "file": SRC["P4"]},
             {"what": "K_z(R₀) v3 canonical / alt vs data", "value": f"{b['B1_McMillan17']['canonical']['F0|L24']['K_R0']:.1f} / {b['B1_McMillan17']['alt']['F0|L24']['K_R0']:.1f} vs {T4['data']['K_R0_data']}", "file": SRC["P4"]},
             {"what": "χ²_Kz other baryon models, canonical", "value": ", ".join(f"{k.split('_')[0]} {v['canonical']['F0|L24']['chi2_kz']:.0f}" for k, v in b.items() if k != 'B1_McMillan17'), "file": SRC["P4"]}],
            srcs("P4", "P4R", "kz"))


# ===================================================================================================  c1_10 MW outer slope
def tile_mw_slope():
    slug, status = "c1_10_mw_outer_slope", "FAIL"
    s = J["S3"]
    ou = load_tsv(R / RAW["ou"])
    r, v = ou["R_kpc"], ou["vc_kms"]; sg = 0.5 * (ou["sig_plus"] + ou["sig_minus"])
    E = np.hypot(sg, np.where(r <= 22.0, 0.03, 0.15) * v)            # S3's error model for Ou24
    fig = plt.figure(figsize=(11.5, 5.2))
    ax = fig.add_axes([0.07, 0.17, 0.42, 0.60]); bx = fig.add_axes([0.62, 0.17, 0.35, 0.60])
    w = (r >= 15) & (r <= 27.5)
    ax.errorbar(r[~w], v[~w], yerr=E[~w], fmt="o", color=ms.MUTED, ms=3.5, capsize=2, alpha=0.6)
    ax.errorbar(r[w], v[w], yerr=E[w], fmt="o", color=ms.DATA, ms=4.5, capsize=2, label="Ou+24 (Gaia DR3), 15–27.5 kpc")
    cell = s["steps"]["AQ_gamma0"]
    rr = np.linspace(15, 27.5, 50)
    # data slope line: weighted LSQ of ln V on ln R in the window (the lane's slope estimator form), drawn for the eye
    A = np.vstack([np.ones(w.sum()), np.log(r[w] / 20.0)]).T
    Wt = (v[w] / E[w]) ** 2
    coef = np.linalg.solve(A.T @ (A * Wt[:, None]), A.T @ (Wt * np.log(v[w])))
    ax.plot(rr, np.exp(coef[0]) * (rr / 20.0) ** cell["canonical"]["cells"]["Ou24"]["slope_data"], color=ms.DATA, lw=1.2, ls=":",
            label=f"data slope {cell['canonical']['cells']['Ou24']['slope_data']:+.3f} ± {cell['canonical']['cells']['Ou24']['slope_err']:.3f}")
    for foot, ls in (("canonical", "-"), ("alt", "--")):
        c = cell[foot]["cells"]["Ou24"]
        ax.plot(rr, c["V20_census"] * (rr / 20.0) ** c["slope_census"], color=ms.MODEL, lw=2, ls=ls,
                label=f"v3 {foot}: slope {c['slope_census']:+.3f}, V(20) {c['V20_census']:.0f}")
    ax.set_xlabel("R [kpc]"); ax.set_ylabel("circular velocity [km/s]")
    ax.set_xlim(5, 30); ax.set_ylim(150, 250)
    ax.legend(fontsize=7.5, loc="lower left")
    ax.set_title("v3 drawn as a power law with its own 15–27.5 kpc slope and V(20 kpc)", fontsize=8.5)
    steps = [("ALG_numono", "algebraic, ν_mono"), ("ALG_nu1", "algebraic, ν₁"), ("AQ_iso", "AQUAL disc, isolated"),
             ("AQ_gamma0", "AQUAL + h81 field\n(the v3 cell)"), ("AQ_gamma0_2x", "AQUAL + 2 × h81")]
    y = np.arange(len(steps))[::-1]
    sd, se = cell["canonical"]["cells"]["Ou24"]["slope_data"], cell["canonical"]["cells"]["Ou24"]["slope_err"]
    bx.axvspan(sd - se, sd + se, color=ms.BAND, alpha=0.8, zorder=0, label="Ou+24 data slope ±1σ")
    bx.axvline(sd, color=ms.DATA, lw=1.2)
    for foot, dy in (("canonical", 0.12), ("alt", -0.12)):
        xs = [s["steps"][k][foot]["cells"]["Ou24"]["slope_census"] for k, _ in steps]
        bx.plot(xs, y + dy, "o", color=FOOT[foot], ms=6, label=f"law slope, {foot}")
    for (k, _), yi in zip(steps, y):
        Zc = s["steps"][k]["canonical"]["combined"]["primary"]["Z"]; Za = s["steps"][k]["alt"]["combined"]["primary"]["Z"]
        bx.text(0.02, yi, f"Z {Zc:+.2f} / {Za:+.2f}", va="center", fontsize=7.5, color=ms.STATUS["FAIL"])
    bx.set_yticks(y); bx.set_yticklabels([l for _, l in steps], fontsize=8)
    bx.set_xlim(-0.45, 0.16); bx.grid(axis="y", visible=False)
    bx.set_xlabel("dlnV/dlnR over 15–27.5 kpc (Ou+24)")
    bx.set_title("each ingredient added; primary Ou+Jiao Z (can / alt)", fontsize=8.5)
    bx.legend(fontsize=7, loc="lower left")
    ms.finish(fig, slug, status, "Milky Way outer rotation-curve slope (Gaia)",
              f"FAIL (shape excluded): v3's slope {cell['canonical']['cells']['Ou24']['slope_census']:+.3f} / {cell['alt']['cells']['Ou24']['slope_census']:+.3f} "
              f"vs data {sd:+.3f}; Z {s['reading']['canonical']['Z']:+.2f} / {s['reading']['alt']['Z']:+.2f}",
              SRC["S3"] + " steps; " + RAW["ou"])
    print(f"[c1_10] check: my weighted LSQ slope {coef[1]:+.4f} vs file slope_data {sd:+.4f}")
    caption(slug, "MW outer slope (Gaia)", status,
            "The Milky Way's circular velocity from Gaia DR3 red giants (Ou+24, 37 points; Jiao+23 in the primary test) over "
            "15–27.5 kpc, against v3's AQUAL disc solution for McMillan17's baryons in the Galaxy's external field.",
            "Left: the measured rotation curve (window points dark, others grey) with the data's slope (dotted) and v3 drawn as a "
            "power law with its own fitted slope and V(20 kpc), on both footings. Right: v3's slope as each ingredient is added "
            "(kernel, disc geometry, external field), against the data slope band, with the primary Z.",
            "The Gaia curve falls steeply beyond 15 kpc (slope −0.325); v3 falls only gently (−0.126 / −0.114), so the shape is "
            "excluded at Z −4.37 / −4.62. No ingredient cures it: the kernel, the AQUAL disc solve and the external field each move "
            "the slope by about 0.01, and the μ_K² term (first-order bound) makes it shallower still. The cause is the steep DR3 "
            "decline itself, not the law's amplitude: at the census baryons v3 also runs low (V(20 kpc) "
            f"{cell['canonical']['cells']['Ou24']['V20_census']:.1f} / {cell['alt']['cells']['Ou24']['V20_census']:.1f} km/s), but rescaling the "
            f"stellar mass to fix the amplitude leaves the slope at {cell['canonical']['cells']['Ou24']['slope_s']:+.3f} / "
            f"{cell['alt']['cells']['Ou24']['slope_s']:+.3f}. Cepheids (Feng+26) are shape-consistent. The power-law lines on the "
            "left are a drawing aid; the verdict uses the lane's solved curves.",
            [{"what": "v3 law slope on Ou24, canonical / alt", "value": f"{cell['canonical']['cells']['Ou24']['slope_census']:+.4f} / {cell['alt']['cells']['Ou24']['slope_census']:+.4f}", "file": SRC["S3"]},
             {"what": "data slope Ou24", "value": f"{sd:+.4f} ± {se:.4f}", "file": SRC["S3"]},
             {"what": "primary Ou+Jiao Z, canonical / alt", "value": f"{s['reading']['canonical']['Z']:+.3f} / {s['reading']['alt']['Z']:+.3f}", "file": SRC["S3"]},
             {"what": "μ_K² first-order slope shift, canonical / alt", "value": f"{s['muK_bound']['canonical']['dslope']:+.3f} / {s['muK_bound']['alt']['dslope']:+.3f}", "file": SRC["S3"]},
             {"what": "Keplerian-tail injection Z, canonical", "value": f"{s['M3_injection']['canonical']['Z']:+.2f}", "file": SRC["S3"]}],
            srcs("S3", "rebuild_2026_10_22/S3_v3_mw_seals/README.md", "ou"))


if __name__ == "__main__":
    tile_sparc(); tile_meerkat(); tile_lens_inner(); tile_lens_all(); lr = tile_tdg(); tile_globulars(); tile_sluggs()
    tile_groups(); tile_mw_kz(); tile_mw_slope()
    print(f"[c1_05] check: unweighted mean log Mdyn/Mbar of the 6 TDGs {np.mean(lr):+.3f} (U1 B0 r̄ "
          f"{J['U1']['numbers']['N5']['tdg']['canonical']['TDG_B0']['rbar']:+.3f})")
    out = Path(__file__).resolve().parents[1] / "captions" / "col1.json"
    out.parent.mkdir(exist_ok=True)
    json.dump(CAP, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {len(CAP)} captions -> {out}")
