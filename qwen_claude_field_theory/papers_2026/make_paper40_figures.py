#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PAPER40 figures (the MOND acceleration scale from MeerKAT: 47 deep-regime HI discs in MIGHTEE-HI COSMOS).

Builds, from committed inputs only:
  fig1_paper40_levels.pdf  the implied a0 per redshift window and pooled (CFG301's s* estimator), the direct BTFR rows and the single-dish
                           flux-scale readings of CFG304, against the two footings, SPARC's fitted scale and the MIGHTEE-HI/LADUMA resolved fit;
  fig2_paper40_btfr.pdf    V against M_b for the 47 discs with the deep-MOND line V^4 = G M_b a0 on both footings;
  PAPER40_figures_numbers.json  every number the figures and the paper's own diagnostic rows use.

Inputs (all committed): the MIGHTEE-HI COSMOS catalogue (data_assembly/mightee_hi_catalogue_2026-10-02/, sha256 prefix bcf9e8558bc56448),
CFG301's stage-A survivor IDs and stage-B results (campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/), CFG302's results JSON and
per-galaxy table, CFG304's results JSON, CFG301's estimator and kernel via hzq_core (CFG223's median-residual s*, nu_mono) and its constants
via cfg260_core.

The chain is re-implemented here from cfg301_width_chain.py (lines 105-121) and is GATED: before anything is plotted the script must reproduce
CFG301's committed pooled s*, window s*, the -0.30 dex baryon band, the H0 = 67.4 knob and the BTFR medians to 1e-9 (dex or relative).
If any reproduction fails the script exits 1 and writes nothing.

POST HOC diagnostic rows, labelled as such in the paper (not CFG301 numbers; not frozen): exact chain re-runs of the single-dish flux scale
of CFG304 (all baryons raised at fixed R, as the band rows are defined; the gas alone raised with R following the size relation), the
velocity frame (k = 0), the inclination thickness q0, MIGHTEE's own size relation, and the join of CFG301's 47 discs with CFG302's cube table.
kappa = 1/2 is FITTED.  No verdict words.

Usage:  python3 make_paper40_figures.py           (writes the two PDFs and the JSON next to this file)
        python3 make_paper40_figures.py --check   (reproduction gate only; writes nothing)
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
LANE = os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain")
sys.path.insert(0, os.path.join(CFG, "HZQ_common")); sys.path.insert(0, os.path.join(CFG, "CFG260_budhies_a0_z02"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import hzq_core as H                      # CFG223's estimator (verbatim copy) and nu_mono, exactly as CFG301 uses them
    import cfg260_core as C                   # CFG260's constants (G, MSUN, KPC, FP0's full-precision a0 on both footings)

G, MSUN, KPC = C.G, C.MSUN, C.KPC
A0C, A0A = C.A0["canonical"], C.A0["alt"]
NU = H.NU
CSV = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
JA = json.load(open(os.path.join(LANE, "cfg301_stageA_results.json")))["numbers"]
JB = json.load(open(os.path.join(LANE, "cfg301_stageB_results.json")))["numbers"]
J302 = json.load(open(os.path.join(CFG, "CFG302_mightee_cube_raw_widths", "cfg302_raw_widths_results.json")))["numbers"]
J304 = json.load(open(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_flux_scale_alfalfa_results.json")))["numbers"]
# the published whole-sample RAR level of Varasteanu et al. 2026 (arXiv:2608.03576, abstract: a0 = (1.50 +- 0.05) x 10^-10 m s^-2; CFG279 README);
# the authors' kernel and mass-to-light modelling, not our estimator -- a reference line only
A0_V26 = 1.50e-10
REC0 = dict(delta=0.0, sini=None, tau_ms=0.0, tau_b=0.0, rdex=0.0, h0=70.0, gas_dex=0.0, k=1, size=(0.506, -3.293))
CHECK_ONLY = "--check" in sys.argv


def chain(a, W, rec):
    """cfg301_width_chain.py's chain (primary: k = 1, size relation 0.506 / -3.293), plus three post hoc handles: gas_dex (a shift of M_HI alone:
    the gas and, through the size relation, R), k (the (1+z) frame exponent; k = 0 reads the catalogue W50 as rest-frame) and size (the D_HI relation)."""
    ds = 70.0 / rec["h0"]
    Mhi = a["mhi"] * ds ** 2 * 10 ** rec["gas_dex"]
    Ms = a["ms"] * ds ** 2 * 10 ** rec["tau_ms"]
    Mg = 1.33 * Mhi
    tb = 10 ** rec["tau_b"]
    Mg, Ms = Mg * tb, Ms * tb
    Mb = Mg + Ms
    R = 0.5 * 10 ** (rec["size"][0] * np.log10(Mhi) + rec["size"][1] + rec["rdex"]) * KPC
    sini = a["sini"] if rec["sini"] is None else rec["sini"]
    Wc = (np.asarray(W, float) - rec["delta"]) / (1 + a["z"]) ** rec["k"]
    V = Wc / (2 * sini) * 1e3
    gb = G * Mb * MSUN / R ** 2
    go = V ** 2 / R
    return dict(D=go / gb, gb=gb, V=V, Mb=Mb, Mg=Mg, Ms=Ms, R=R, y=gb / A0C)


def est(dd, a0=A0C):
    l, u = H.AI.implied(dd["D"], dd["gb"], NU, a0)
    return float(l[0]), bool(u[0])


# ------------------------------------------------------------------ the 47 survivors, in CFG301's order (z_HI, ID)
d = pd.read_csv(CSV, dtype={"ID_catalogue": str})
assert H.sha(CSV) == "bcf9e8558bc56448", "catalogue sha256 prefix differs from CFG301's"
S = d[d.ID_catalogue.isin(set(JA["survivor_ids"]))].sort_values(["z_HI", "ID_catalogue"], kind="mergesort").reset_index(drop=True)
assert S.ID_catalogue.tolist() == JA["survivor_ids"], "survivor order differs from CFG301 stage A"
N = len(S)
a = dict(mhi=10 ** S.log_M_HI.values, ms=10 ** S.log_M_stel.values, z=S.z_HI.values.astype(float), sini=np.sin(np.radians(S.incl_deg.values)))
W = S.W_50_km_s.values.astype(float)
WIN = [np.asarray(x) for x in np.array_split(np.arange(N), 3)]

# ------------------------------------------------------------------ reproduction gate against CFG301's committed stage-B JSON
dd0 = chain(a, W, REC0)
gate = []


def g(name, mine, committed, tol=1e-9, rel=False):
    dev = abs(mine / committed - 1) if rel else abs(mine - committed)
    gate.append(dict(name=name, mine=mine, committed=committed, dev=dev, ok=bool(dev <= tol)))


lP, _ = est(dd0)
g("pooled log10 s*", lP, JB["pooled"]["log_s"])
for i, w in enumerate(WIN):
    g(f"W{i + 1} log10 s*", est({k: v[w] for k, v in dd0.items()})[0], JB["results"][f"W{i + 1}"]["log_s"])
lband = est(chain(a, W, dict(REC0, tau_b=-0.30)))[0]
g("pooled band -0.30 dex s*", 10 ** lband, JB["pooled"]["bands"]["-0.30"], rel=True)
lh0 = est(chain(a, W, dict(REC0, h0=67.4)))[0]
g("pooled H0 = 67.4 log10 s*", lh0, JB["recipe"]["pooled"]["rows"]["h0"]["log_s"][0])
a0b = dd0["V"] ** 4 / (G * dd0["Mb"] * MSUN)
gasdom = dd0["Mg"] > dd0["Ms"]
g("BTFR median (i)", float(np.median(a0b)), JB["btfr"]["(i) all survivors"]["median"], rel=True)
g("BTFR median (ii)", float(np.median(a0b[gasdom])), JB["btfr"]["(ii) gas-dominated (M_gas > M*)"]["median"], rel=True)
g("y max (README 0.084)", float(dd0["y"].max()), 0.084, tol=5e-4)
print("REPRODUCTION GATE (this script's chain against CFG301's committed stage-B JSON):")
for r in gate:
    print(f"  [{'PASS' if r['ok'] else 'FAIL'}] {r['name']}: mine {r['mine']:.12g}, committed {r['committed']:.12g}, |dev| {r['dev']:.1e}")
if not all(r["ok"] for r in gate):
    sys.exit("reproduction gate FAILED -- nothing written")
if CHECK_ONLY:
    print(f"{sum(r['ok'] for r in gate)}/{len(gate)} reproduction checks pass (--check: nothing written)")
    sys.exit(0)

# ------------------------------------------------------------------ the single-dish flux scale (CFG304) as exact chain re-runs (POST HOC)
# CFG304's frozen primary: catalogue / ALFALFA median log flux ratio R_cat (code 1, OPT); its CFG301 consequence is a band-row interpolation.
R304 = J304["results"]["cat"]["C1"]["OPT"]["median"]
lA = est(chain(a, W, dict(REC0, tau_b=-R304)))[0]                                   # all baryons raised by -R_cat at fixed R (the band-row definition)
lB = est(chain(a, W, dict(REC0, gas_dex=-R304)))[0]                                 # the gas alone raised, R following the size relation
lBR = est(chain(a, W, dict(REC0, gas_dex=-R304, rdex=R304 * 0.506)))[0]             # the gas alone raised, R held at its catalogue value
flux = dict(
    note="POST HOC exact re-runs of CFG301's chain at CFG304's single-dish flux scale (CFG304 itself interpolates CFG301's band rows)",
    R_cat=R304,
    A_all_baryons_R_fixed=dict(log_s=lA, s=10 ** lA, a0=10 ** lA * A0C, dlog_vs_primary=lA - lP),
    B_gas_only_R_follows=dict(log_s=lB, s=10 ** lB, a0=10 ** lB * A0C, dlog_vs_primary=lB - lP),
    B_gas_only_R_fixed=dict(log_s=lBR, s=10 ** lBR, a0=10 ** lBR * A0C, dlog_vs_primary=lBR - lP),
    cfg304_interpolated=dict(A=J304["cfg301"]["A"]["central"]["a0"], B=J304["cfg301"]["B"]["central"]["a0"]))
print(f"POST HOC single-dish flux scale (R_cat {R304:+.4f}): (A) all baryons, R fixed: a0 {10 ** lA * A0C:.4e} ({lA - lP:+.3f} dex; CFG304 interpolation "
      f"{J304['cfg301']['A']['central']['a0']:.4e}); (B) gas only, R follows: a0 {10 ** lB * A0C:.4e} ({lB - lP:+.3f} dex; CFG304 interpolation "
      f"{J304['cfg301']['B']['central']['a0']:.4e}); gas only, R fixed: a0 {10 ** lBR * A0C:.4e} ({lBR - lP:+.3f} dex)")

# ------------------------------------------------------------------ further POST HOC systematic rows (this paper's script; selection fixed at CFG301's 47)
post = {}
# (a) the velocity frame: k = 0 reads the catalogue W50 as already rest-frame (CFG302 cannot decide the convention: +0.003 vs -0.022 dex)
lk0 = est(chain(a, W, dict(REC0, k=0)))[0]
post["frame_k0"] = dict(log_s=lk0, s=10 ** lk0, a0=10 ** lk0 * A0C, dlog_vs_primary=lk0 - lP, z_median=float(np.median(a["z"])))
# (b) the intrinsic thickness q0 of the inclination formula cos^2 i = (q^2 - q0^2)/(1 - q0^2) (the catalogue uses q0 = 0.2)
qax = S.axis_ratio.values.astype(float)
def incl_of(q0):
    return np.degrees(np.arccos(np.sqrt(np.clip((qax ** 2 - q0 ** 2) / (1 - q0 ** 2), 0.0, 1.0))))
irec = float(np.max(np.abs(incl_of(0.2) - S.incl_deg.values)))
post["q0_check_max_dev_deg"] = irec
for q0 in (0.10, 0.30):
    l_ = est(chain(dict(a, sini=np.sin(np.radians(incl_of(q0)))), W, REC0))[0]
    post[f"q0_{q0:.2f}"] = dict(log_s=l_, s=10 ** l_, a0=10 ** l_ * A0C, dlog_vs_primary=l_ - lP, median_dincl_deg=float(np.median(incl_of(q0) - S.incl_deg.values)))
# (c) MIGHTEE's own HI size-mass relation (Rajohnson et al. 2022: slope 0.501, intercept -3.252) in place of 0.506 / -3.293
lsz = est(chain(a, W, dict(REC0, size=(0.501, -3.252))))[0]
post["size_rajohnson2022"] = dict(log_s=lsz, s=10 ** lsz, dlog_vs_primary=lsz - lP,
                                  dlogD_at_median=float((0.501 - 0.506) * np.median(S.log_M_HI.values) + (-3.252 + 3.293)), median_logMHI=float(np.median(S.log_M_HI.values)))
# (d) the cube flux scale for exactly these 47 discs (join with CFG302's committed per-galaxy table)
c302 = pd.read_csv(os.path.join(CFG, "CFG302_mightee_cube_raw_widths", "cfg302_per_galaxy.csv"))
j = c302[c302.ID.isin(set(S.ID_catalogue))]
jp = j[j.primary == 1]; jd = jp[jp.detected.astype(str) == "True"]
post["cfg302_join"] = dict(n_in_table=int(len(j)), n_primary=int(len(jp)), n_detected=int(len(jd)), median_ratio_primary=float(np.median(jp.ratio_S)),
                           median_logratio_S_detected=float(np.median(jd.logratio_S)), median_logratio_W50_detected=float(np.median(jd.logratio_W50.dropna())))
for k_, v_ in post.items():
    print(f"POST HOC {k_}: {v_}")

# ------------------------------------------------------------------ kappa on both footings (kappa = 1/2 x a0 / a0_footing), statistics and recipe
q = JB["pooled"]["q"]; half = JB["pooled"]["recipe_half"]
kap = {}
for nm, a0f in (("rho_Lambda", A0C), ("rho_crit", A0A)):
    s = JB["pooled"]["a0"] / a0f
    kap[nm] = dict(kappa=0.5 * s, stat68=[0.5 * 10 ** q[1] * A0C / a0f, 0.5 * 10 ** q[2] * A0C / a0f], stat95=[0.5 * 10 ** q[0] * A0C / a0f, 0.5 * 10 ** q[3] * A0C / a0f],
                   recipe=[0.5 * s * 10 ** (-half), 0.5 * s * 10 ** half], h0_674=0.5 * 10 ** lh0 * A0C / a0f)
    print(f"kappa ({nm}): {kap[nm]['kappa']:.4f}; stat 68% {kap[nm]['stat68'][0]:.4f}-{kap[nm]['stat68'][1]:.4f}; 95% {kap[nm]['stat95'][0]:.4f}-{kap[nm]['stat95'][1]:.4f}; "
          f"x10^+-recipe {kap[nm]['recipe'][0]:.4f}-{kap[nm]['recipe'][1]:.4f}; at H0 = 67.4 {kap[nm]['h0_674']:.4f}")

# ------------------------------------------------------------------ figures
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8.5, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42,
                     "axes.edgecolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.labelcolor": "#0b0b0b"})
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"           # validated categorical slots 1-3 (all-pairs, light mode)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
U = 1e-10

# Fig 1: the levels
fig, ax = plt.subplots(figsize=(6.9, 3.3))
items = []
for i in range(3):
    r = JB["results"][f"W{i + 1}"]
    items.append((f"W{i + 1}\nz {r['z_med']:.3f}\nN {r['n']}", r["a0"], [10 ** v * A0C for v in r["q"]], r["recipe_half"], BLUE, "o", True))
r = JB["pooled"]
items.append((f"pooled\nz 0.03-0.09\nN {r['n']}", r["a0"], [10 ** v * A0C for v in r["q"]], r["recipe_half"], BLUE, "D", True))
cA, cB = J304["cfg301"]["A"], J304["cfg301"]["B"]                                   # CFG304's committed single-dish readings (68 % from its R_cat bootstrap)
items.append(("single-dish\nscale (A)\nall baryons", cA["central"]["a0"], [cA["hi"]["a0"], cA["hi"]["a0"], cA["lo"]["a0"], cA["lo"]["a0"]], None, ORANGE, "D", False))
items.append(("single-dish\nscale (B)\ngas only", cB["central"]["a0"], [cB["hi"]["a0"], cB["hi"]["a0"], cB["lo"]["a0"], cB["lo"]["a0"]], None, ORANGE, "^", False))
for key, lab in (("(i) all survivors", "BTFR, all\nN 47\n(+kernel)"), ("(ii) gas-dominated (M_gas > M*)", "BTFR, gas-\ndom., N 37\n(+kernel)")):
    b = JB["btfr"][key]
    items.append((lab, b["median"], b["q"], b["recipe_half"], AQUA, "s", True))
refs = [(A0C, "canonical footing ($\\rho_\\Lambda$) 0.936", (0, (5, 2.5)), INK),
        (A0A, "alt footing ($\\rho_{\\rm crit}$) 1.131", (0, (6, 1.5, 1.5, 1.5)), INK),
        (1.20e-10, "SPARC $g_\\dagger$ (McGaugh+16) 1.20", (0, (1, 1.6)), INK2),
        (A0_V26, "MIGHTEE-HI/LADUMA resolved\nRAR fit (authors' $M/L$) 1.50", (0, (1, 3)), INK2)]
for (yv, lab, ls, col), va in zip(refs, ("top", "top", "bottom", "bottom")):
    ax.axhline(yv / U, color=col, lw=0.8, ls=ls, zorder=1)
    ax.text(len(items) - 0.35, yv / U * (0.992 if va == "top" else 1.008), lab, fontsize=6.4, color=col, ha="left", va=va)
for k, (lab, v, qq, rh, col, mk, filled) in enumerate(items):
    if rh is not None:
        ax.add_patch(plt.Rectangle((k - 0.22, v / U * 10 ** (-rh)), 0.44, v / U * (10 ** rh - 10 ** (-rh)), facecolor=col, alpha=0.13, edgecolor="none", zorder=2))
    if qq is not None:
        ax.plot([k, k], [qq[0] / U, qq[3] / U], color=col, lw=0.9, zorder=3, solid_capstyle="round")
        ax.plot([k, k], [qq[1] / U, qq[2] / U], color=col, lw=2.6, zorder=3, solid_capstyle="round")
    ax.plot(k, v / U, marker=mk, ms=7.5 if mk != "^" else 8.5, mfc=(col if filled else "white"), mec=col, mew=1.4, zorder=4, ls="none")
    ax.text(k + 0.27, v / U, f"{v / U:.2f}", fontsize=6.6, color=INK, va="center", ha="left", zorder=5)
ax.set_yscale("log"); ax.set_ylim(0.42, 2.3)
ax.set_yticks([0.5, 0.7, 1.0, 1.5, 2.0]); ax.set_yticklabels(["0.5", "0.7", "1.0", "1.5", "2.0"]); ax.minorticks_off()
ax.set_xticks(range(len(items))); ax.set_xticklabels([it[0] for it in items], fontsize=6.3)
ax.set_xlim(-0.6, len(items) + 1.75)
ax.set_ylabel("$a_0$  [$10^{-10}$ m s$^{-2}$]")
ax.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
f1 = os.path.join(HERE, "fig1_paper40_levels.pdf"); fig.savefig(f1); plt.close(fig)

# Fig 2: the BTFR
V = dd0["V"] / 1e3; Mb = dd0["Mb"]
sV = S.W_50_km_s_err.values / (1 + a["z"]) / (2 * a["sini"])
sMb = np.sqrt((dd0["Mg"] * math.log(10) * S.log_M_HI_err.values) ** 2 + (dd0["Ms"] * math.log(10) * S.log_M_stel_err.values) ** 2) / Mb / math.log(10)
fig, ax = plt.subplots(figsize=(5.0, 3.6))
xx = np.linspace(9.2, 11.0, 50)
lines = []
for a0v, lab, ls in ((A0C, "$V^4=GM_ba_0$, canonical $a_0$ (0.936)", (0, (5, 2.5))), (A0A, "$V^4=GM_ba_0$, alt $a_0$ (1.131)", (0, (6, 1.5, 1.5, 1.5)))):
    vv = (G * 10 ** xx * MSUN * a0v) ** 0.25 / 1e3
    lines += ax.plot(xx, np.log10(vv), color=INK, lw=0.9, ls=ls, zorder=2, label=lab)
vv = (G * 10 ** xx * MSUN * JB["btfr"]["(i) all survivors"]["median"]) ** 0.25 / 1e3
lines += ax.plot(xx, np.log10(vv), color=AQUA, lw=1.0, zorder=2, label="median $V^4/(GM_b)$ (1.25, incl. kernel)")
leg_lines = ax.legend(handles=lines, loc="lower right", fontsize=6.6, frameon=False, title="[$10^{-10}$ m s$^{-2}$]", title_fontsize=6.6)
ax.add_artist(leg_lines)
pts = []
for sel, col, mk, lab, filled in ((gasdom, BLUE, "o", f"gas-dominated ($M_{{\\rm gas}}>M_\\star$), N {int(gasdom.sum())}", True),
                                  (~gasdom, ORANGE, "s", f"star-dominated, N {int((~gasdom).sum())}", False)):
    ax.errorbar(np.log10(Mb[sel]), np.log10(V[sel]), xerr=sMb[sel], yerr=sV[sel] / V[sel] / math.log(10), fmt="none", ecolor=col, elinewidth=0.6, alpha=0.6, zorder=3)
    pts += ax.plot(np.log10(Mb[sel]), np.log10(V[sel]), marker=mk, ms=5.2, ls="none", mfc=(col if filled else "white"), mec=col, mew=1.1, zorder=4, label=lab)
ax.set_xlabel("$\\log_{10}\\,M_b$  [M$_\\odot$]   ($M_b=1.33\\,M_{\\rm HI}+M_\\star$)")
ax.set_ylabel("$\\log_{10}\\,V$  [km s$^{-1}$]   ($V=W_{50}/[2(1+z)\\sin i]$)")
ax.set_xlim(9.15, 11.05)
ax.legend(handles=pts, loc="upper left", fontsize=6.8, frameon=False)
ax.grid(True, color=GRID, lw=0.5, zorder=0); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
f2 = os.path.join(HERE, "fig2_paper40_btfr.pdf"); fig.savefig(f2); plt.close(fig)

out = dict(paper="PAPER40", inputs=dict(catalogue_sha256_prefix="bcf9e8558bc56448", cfg301_stageA="cfg301_stageA_results.json", cfg301_stageB="cfg301_stageB_results.json"),
           reproduction_gate=gate, reproduction_ok=bool(all(r["ok"] for r in gate)), flux_translation_post_hoc=flux, post_hoc_rows=post, kappa=kap,
           h0_674=dict(log_s=lh0, s=10 ** lh0, a0=10 ** lh0 * A0C, dlog_vs_primary=lh0 - lP),
           per_galaxy=dict(ID=S.ID_catalogue.tolist(), V_kms=V.tolist(), log_Mb=np.log10(Mb).tolist(), gas_dominated=gasdom.tolist(), y=dd0["y"].tolist()),
           figures=[os.path.basename(f1), os.path.basename(f2)])
json.dump(out, open(os.path.join(HERE, "PAPER40_figures_numbers.json"), "w"), indent=1)
print(f"wrote {os.path.basename(f1)}, {os.path.basename(f2)}, PAPER40_figures_numbers.json; {len(gate)}/{len(gate)} reproduction checks pass")
