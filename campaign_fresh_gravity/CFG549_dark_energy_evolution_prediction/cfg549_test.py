#!/usr/bin/env python3
"""CFG549 stage 2: the frozen DESI DR2 test of the stage-1 predictions, R2 (galaxy measurement channel), R4 (consistency), figure.

Reads cfg549_predictions.json ONLY after checking its SHA-256 against PREDICTIONS_HASH.txt (K7), then opens the DESI DR2 w0wa chains.
Run: nice -n 10 python3 cfg549_test.py   (CFG549_MUTATE=1 reads the MUTATE predictions and writes *_MUTATE outputs; MU1)
"""
import hashlib
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np                       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
MUT = os.environ.get("CFG549_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg549_test{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


R = {"lane": "CFG549", "stage": "test (DESI DR2 enters here only)", "mutate": MUT, "checks": {}}

# ---------------------------------------------------------------- K7 hash firewall
pf = os.path.join(HERE, f"cfg549_predictions{SUF}.json")
hsh = hashlib.sha256(open(pf, "rb").read()).hexdigest()
ref = open(os.path.join(HERE, f"PREDICTIONS_HASH{SUF}.txt")).read().split()[0]
R["checks"]["K7_hash"] = dict(sha256=hsh, ok=bool(hsh == ref))
P(f"K7 predictions hash {hsh[:16]}... {'MATCH' if hsh == ref else 'MISMATCH'}")
if hsh != ref:
    sys.exit(2)
PR = json.load(open(pf))

# ---------------------------------------------------------------- chains (read as CFG511 does)
CHAINS = os.path.abspath(os.path.join(REPO, "..", "_external_data", "desi_dr2_chains"))
NAMES = ("cmb", "pantheonplus", "union3", "desy5"); SN = ("pantheonplus", "union3", "desy5")


def load_chain(nm):
    hdr = open(os.path.join(CHAINS, nm, "chain.1.txt")).readline().lstrip("#").split()
    names = ("weight", "w", "wa", "omegam")
    cols = [hdr.index(x) for x in names]
    xs = []
    for kk in range(1, 5):
        d = np.loadtxt(os.path.join(CHAINS, nm, f"chain.{kk}.txt"), usecols=cols)
        xs.append(d[int(0.3 * len(d)):])
    x = np.vstack(xs)
    return {n: x[:, i] for i, n in enumerate(names)}


def wpct(x, wt, q):
    o = np.argsort(x); cw = np.cumsum(wt[o]); cw /= cw[-1]
    return float(np.interp(q, cw, x[o]))


def f_cpl(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))


CH = {nm: load_chain(nm) for nm in NAMES}
ST = {}
for nm, cdat in CH.items():
    wt = cdat["weight"]
    mu = np.array([np.average(cdat["w"], weights=wt), np.average(cdat["wa"], weights=wt)])
    C = np.cov(np.vstack([cdat["w"], cdat["wa"]]), aweights=wt)
    ST[nm] = dict(mu=mu, C=C, Ci=np.linalg.inv(C))
a25 = {nm: wpct(np.sqrt(f_cpl(2.5, CH[nm]["w"], CH[nm]["wa"])), CH[nm]["weight"], 0.5) for nm in NAMES}
ref511 = dict(pantheonplus=0.827, union3=0.782, desy5=0.798)
R["checks"]["K4_cfg511_a0_2p5"] = dict(values=a25, ok=bool(all(abs(a25[n] - ref511[n]) <= 0.01 for n in SN)))
P("K4 a0(2.5)/a0(0) medians " + ", ".join(f"{n} {a25[n]:.3f}" for n in NAMES) + f" -> {'PASS' if R['checks']['K4_cfg511_a0_2p5']['ok'] else 'FAIL'}")
R["chains"] = {nm: dict(w0wa_mean=ST[nm]["mu"].tolist(), w0wa_cov=ST[nm]["C"].tolist()) for nm in NAMES}


def d2(p, nm):
    v = np.array(p) - ST[nm]["mu"]
    return float(v @ ST[nm]["Ci"] @ v)


def verdict(dd):
    if all(dd[n] >= 11.83 for n in SN):
        return "EXCLUDED"
    if all(dd[n] >= 6.18 for n in SN):
        return "TENSION"
    return "CONSISTENT"


# ---------------------------------------------------------------- frozen test of the DERIVED models
P("\n[TEST] frozen DESI DR2 test: d^2 = (p - mu)^T C^-1 (p - mu), 2 dof; EXCLUDED >= 11.83 / TENSION >= 6.18 in all SN chains")
models = {"M-Lambda": (-1.0, 0.0)}
for key in ("can|A|Mmin1e+08", "can|B|Mmin1e+08", "alt|A|Mmin1e+08", "alt|B|Mmin1e+08"):
    r = PR["R1"][key]
    models[f"M-R1 {key} (frozen rho_eff projection)"] = (r["w0_eff"], r["wa_eff"])
    models[f"M-R1 {key} (H-fit projection)"] = (r["w0_eff_H"], r["wa_eff_H"])
for foot in ("can", "alt"):
    models[f"M-C4 {foot} (H-fit projection; frozen one undefined)"] = (PR["M_C4"][foot]["w0_eff"], PR["M_C4"][foot]["wa_eff"])
T = {}
dL = {n: d2((-1.0, 0.0), n) for n in NAMES}
for name, p in models.items():
    dd = {n: d2(p, n) for n in NAMES}
    dist = any(abs(dd[n] - dL[n]) >= 1 for n in SN)
    T[name] = dict(p=list(p), d2=dd, d2_minus_d2Lambda={n: dd[n] - dL[n] for n in NAMES}, verdict=verdict(dd),
                   distinguishable_from_Lambda=bool(dist))
    P(f"  {name:58s} (w0, wa) = ({p[0]:+.7f}, {p[1]:+.7f})  d2 " + "/".join(f"{dd[n]:.2f}" for n in NAMES)
      + f"  -> {T[name]['verdict']}; distinguishable from Lambda: {dist}")
R["test"] = T
for key in ("can|A|Mmin1e+08",):
    r = PR["R1"][key]
    R["R1_observable_ever"] = dict(max_abs_onepw=r["max_abs_onepw_z_le_2p5"], floor=1e-3,
                                   observable=bool(r["max_abs_onepw_z_le_2p5"] >= 1e-3))
sig_w0 = {n: math.sqrt(ST[n]["C"][0][0]) for n in NAMES}; sig_wa = {n: math.sqrt(ST[n]["C"][1][1]) for n in NAMES}
R["desi_sigmas"] = dict(w0=sig_w0, wa=sig_wa)
P("  DESI 1-sigma (w0, wa): " + ", ".join(f"{n} ({sig_w0[n]:.3f}, {sig_wa[n]:.3f})" for n in NAMES))
if MUT:
    m = T["M-R1 can|A|Mmin1e+08 (frozen rho_eff projection)"]
    det = (m["verdict"] == "EXCLUDED") or all(abs(m["d2_minus_d2Lambda"][n]) >= 9 for n in SN)
    R["checks"]["MU1_Qx1e6_detected"] = dict(verdict=m["verdict"], dd=m["d2_minus_d2Lambda"], ok=bool(det))
    mh = T["M-R1 can|A|Mmin1e+08 (H-fit projection)"]
    R["MU1_Hfit_report"] = dict(verdict=mh["verdict"], dd=mh["d2_minus_d2Lambda"])
    P(f"  MU1 (Q x 1e6): frozen projection verdict {m['verdict']}, d2 - d2_Lambda " + "/".join(f"{m['d2_minus_d2Lambda'][n]:+.1f}" for n in NAMES)
      + f" -> {'DETECTED' if det else 'NOT DETECTED'}; H-fit verdict {mh['verdict']}")

# ---------------------------------------------------------------- R2 measurement channel
P("\n[R2] galaxies as the dark-energy probe: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)), kappa cancels")
ZQ = (0.5, 1.0, 2.0, 2.5)
R2 = {"desi_halfwidth_log10_rho": {}, "required_sigma_log10_a0": {}, "N_needed": {}}
for nm in NAMES:
    wt = CH[nm]["weight"]
    hw = {}
    for z in ZQ:
        lr = np.log10(f_cpl(z, CH[nm]["w"], CH[nm]["wa"]))
        hw[str(z)] = 0.5 * (wpct(lr, wt, 0.84) - wpct(lr, wt, 0.16))
    R2["desi_halfwidth_log10_rho"][nm] = hw
    R2["required_sigma_log10_a0"][nm] = {z: v / 2 for z, v in hw.items()}
    R2["N_needed"][nm] = {z: {str(so): (3 * so / (v / 2)) ** 2 for so in (0.1, 0.2)} for z, v in hw.items()}
    P(f"  {nm:12s} DESI 68% half-width of log10 rho ratio: " + ", ".join(f"z{z} {v:.3f}" for z, v in hw.items())
      + " | a0 precision to match: " + ", ".join(f"{v / 2:.3f}" for v in hw.values())
      + " dex | N per z-bin (sigma_obj 0.1/0.2, CFG256 wall): " + ", ".join(f"{R2['N_needed'][nm][z]['0.1']:.0f}/{R2['N_needed'][nm][z]['0.2']:.0f}" for z in hw))
J571 = json.load(open(os.path.join(CFG, "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))
rat = J571["ratios"]
dlog_flat = math.log10(rat["F-flat"]["1.6"] / rat["F-DESI"]["1.6"])
dlog_RH = math.log10(rat["R-H"]["1.6"] / rat["F-DESI"]["1.6"])
tr571 = {}
for k_, v in J571["forecast"].items():
    r_flat = abs(v["sep_flat"]) / dlog_flat; r_RH = abs(v["sep_RH"]) / dlog_RH
    tr571[k_] = dict(response_from_flat=r_flat, response_from_RH=r_RH,
                     sigma_log10_a0_flat=0.15 / r_flat, sigma_log10_a0_RH=0.15 / r_RH,
                     sigma_log10_rho_flat=0.30 / r_flat, sigma_log10_rho_RH=0.30 / r_RH)
    P(f"  CFG571 {k_:20s} gas-mass response d(log M_gas)/d(log a0) {r_flat:.2f} (flat) / {r_RH:.2f} (R-H) -> with the 0.15 dex floor "
      f"sigma(log a0 ratio) >= {0.15 / r_RH:.2f}-{0.15 / r_flat:.2f} dex, sigma(log rho_DE ratio) >= {0.30 / r_RH:.2f}-{0.30 / r_flat:.2f} dex at z ~ 1.6")
R2["CFG571_translation"] = tr571
R2["CFG571_dlog_a0_flat_vs_FDESI_z1p6"] = dlog_flat
# CFG511 fork: sqrt(rho) vs sqrt(-p)
_ow = PR["R1"]["can|A|Mmin1e+08"]["onepw"]
fork = {"framework_prediction": {z: abs(math.sqrt((-1 + _ow[z]) / (-1 + _ow["0"])) - 1) for z in ("1", "2.5")}}
fork["framework_prediction_note"] = "w = -1 + O(1e-7): sqrt(w(z)/w0) - 1 = O(1e-7); the fork is unobservable under the framework's own prediction"
fd = {}
for nm in NAMES:
    wt = CH[nm]["weight"]; w0 = CH[nm]["w"]; wa = CH[nm]["wa"]
    fd[nm] = {}
    for z in (1.0, 2.5):
        wz = w0 + wa * z / (1 + z)
        sep = 0.5 * np.log10(np.clip(wz / w0, 1e-12, None))
        fd[nm][str(z)] = [wpct(sep, wt, q) for q in (0.16, 0.5, 0.84)]
fork["under_DESI_dex"] = fd
R2["fork"] = fork
P("  CFG511 fork log10[a0_tension/a0_density] under DESI (16/50/84): " + "; ".join(
    f"{nm} z1 {fd[nm]['1.0'][1]:+.3f}, z2.5 {fd[nm]['2.5'][1]:+.3f} [{fd[nm]['2.5'][0]:+.3f},{fd[nm]['2.5'][2]:+.3f}]" for nm in NAMES))
R["R2"] = R2

# ---------------------------------------------------------------- R3d ratchet under DESI
rat_d = {}
zz = np.linspace(0, 2.5, 126)
for nm in NAMES:
    wt = CH[nm]["weight"]; w0 = CH[nm]["w"]; wa = CH[nm]["wa"]
    rat_d[nm] = {}
    for zs in (1.0, 2.0):
        mx = np.max(np.vstack([f_cpl(z, w0, wa) for z in zz[zz <= zs]]), axis=0)
        dl = 0.5 * np.log10(mx)
        rat_d[nm][str(zs)] = [wpct(dl, wt, q) for q in (0.16, 0.5, 0.84)]
R["R3d_ratchet_under_DESI_dex"] = rat_d
P("\n[R3d] ratchet under DESI: local galaxies read a0 of the max rho_DE since settling, excess log10 a0 (16/50/84): " + "; ".join(
    f"{nm} z_s1 {rat_d[nm]['1.0'][1]:+.3f}, z_s2 {rat_d[nm]['2.0'][1]:+.3f} [{rat_d[nm]['2.0'][0]:+.3f},{rat_d[nm]['2.0'][2]:+.3f}]" for nm in NAMES))

# ---------------------------------------------------------------- R3f CFG542 partner field (read-only, post-freeze report)
J541 = json.load(open(os.path.join(CFG, "CFG541_cold_energy_equations_precise", "cfg541_results.json")))["one_d"]
d542 = os.path.join(CFG, "CFG542_dissipative_action")
files542 = sorted(os.listdir(d542))
ratio = {f"{f}_{n}": J541[f][n]["dW_per_mass"] / J541[f][n]["Esink_per_mass"] for f in ("can", "alt") for n in ("MW", "group", "cluster")}
rmax = max(ratio.values())
r1 = PR["R1"]["can|A|Mmin1e+08"]
R["R3f_CFG542"] = dict(files_seen=files542, results_landed=any(x.endswith("results.json") for x in files542),
                      Q_form="Q = rho_c alpha tau_ff 1_B 1_C grad psi . grad Phi (ACTION.md, uncommitted draft): the whole binding energy dW, "
                             "with w(z) of the partner an INPUT and alpha O(1) FREE",
                      dW_over_Esink=ratio, scaled_drho_over_rho_z0=r1["drho_over_rho_z0"] * rmax,
                      scaled_max_abs_onepw=r1["max_abs_onepw_z_le_2p5"] * rmax)
P(f"\n[R3f] CFG542 folder: {files542}; results landed: {R['R3f_CFG542']['results_landed']}. If Q takes the whole dW (ACTION.md draft), "
  f"R1 scales by <= {rmax:.2f}: drho/rho(0) {r1['drho_over_rho_z0'] * rmax:.2e}, max|1+w| {r1['max_abs_onepw_z_le_2p5'] * rmax:.2e}; "
  "w(z) of the partner stays an input, so no ODE closes for rho_DE beyond the trickle")

# ---------------------------------------------------------------- R4 consistency
P("\n[R4] DESI-tracking a0(z) vs the record's a0(z) constraints")
J255 = json.load(open(os.path.join(CFG, "CFG255_lensing_rar_zsplit", "cfg255_stageB_results.json")))["numbers"]
zlo, zhi = 0.2045, 0.3996
A_obs, sA = J255["A_data"], J255["sigma_A"]          # CFG255 stage B JSON (A = +0.060 +- 0.038)
OM = PR["inputs"]["Omega_m"]
dR = 0.5 * math.log10((OM * (1 + zhi) ** 3 + 1 - OM) / (OM * (1 + zlo) ** 3 + 1 - OM)) * 2   # log10 H(zhi)/H(zlo)
R4 = {"KiDS": {}}
for foot in ("canonical", "alt"):
    AF = J255["amp_models"][f"FLAT_{foot}"]; AR = J255["amp_models"][f"RIVAL_{foot}"]
    for nm in NAMES:
        wt = CH[nm]["weight"]
        dD = 0.5 * np.log10(f_cpl(zhi, CH[nm]["w"], CH[nm]["wa"]) / f_cpl(zlo, CH[nm]["w"], CH[nm]["wa"]))
        AD = AF + (AR - AF) * wpct(dD, wt, 0.5) / dR
        Z = (A_obs - AD) / sA
        diag = abs(AD - AF) >= 2 * sA
        R4["KiDS"][f"{foot}|{nm}"] = dict(dlog_a0_DESI=wpct(dD, wt, 0.5), A_DESI=AD, A_FLAT=AF, Z=Z,
                                          tension=bool(abs(Z) >= 2), diagnostic=bool(diag))
        if nm != "cmb" or foot == "canonical":
            P(f"  KiDS {foot:9s} {nm:12s} dlog a0 (z 0.20->0.40) {wpct(dD, wt, 0.5):+.4f}; A_DESI {AD:+.4f} vs obs {A_obs:+.3f} +- {sA:.3f} "
              f"(Z {Z:+.2f}); |A_DESI - A_FLAT| = {abs(AD - AF):.4f} vs 2 sigma {2 * sA:.3f} -> {'DIAGNOSTIC' if diag else 'not diagnostic'}")
J547 = json.load(open(os.path.join(CFG, "CFG547_cosmic_time_triangulation", "cfg547_results.json")))["test_a"]["table"]
R4["CFG547_test_a_DESI"] = {k_: dict(verdict=v["verdict"], maxZ=v["maxZ"]) for k_, v in J547.items() if k_.endswith("|DESI")}
P("  CFG547 test (a) DESI-tracking: " + ", ".join(f"{k_} {v['verdict']} (max|Z| {v['maxZ']:.2f})" for k_, v in R4["CFG547_test_a_DESI"].items()))
band = {}
for nm in NAMES:
    wt = CH[nm]["weight"]
    mx = np.max(np.abs(np.vstack([0.5 * np.log10(f_cpl(z, CH[nm]["w"], CH[nm]["wa"])) for z in zz])), axis=0)
    band[nm] = dict(median=wpct(mx, wt, 0.5), p95=wpct(mx, wt, 0.95))
R4["max_abs_dlog_a0_z_le_2p5"] = band
R4["calibration_band_dex"] = 0.15
P("  max over z<=2.5 of |log10 a0(z)/a0(0)| under DESI (median / 95%): " + ", ".join(f"{nm} {v['median']:.3f}/{v['p95']:.3f}" for nm, v in band.items())
  + " vs the 0.15 dex inner calibration band (2 sigma = 0.30)")
anyT = any(v["tension"] for v in R4["KiDS"].values()) or any(v["maxZ"] >= 2 for v in R4["CFG547_test_a_DESI"].values()) \
    or any(v["median"] >= 0.30 for v in band.values())
anyD = any(v["diagnostic"] for v in R4["KiDS"].values()) or any(v["p95"] >= 0.30 for v in band.values())
R4["verdict"] = ("TENSION" if anyT else "NO TENSION") + "; " + ("DIAGNOSTIC" if anyD else "NOT DIAGNOSTIC")
P(f"  R4 verdict: {R4['verdict']}")
R["R4"] = R4

# ---------------------------------------------------------------- figure (main run only)
if not MUT:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    zf = np.linspace(0, 2.6, 131)
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))
    cols = dict(pantheonplus="#1f77b4", union3="#2ca02c", desy5="#9467bd")
    for nm in SN:
        wt = CH[nm]["weight"]
        lo = [wpct(f_cpl(z, CH[nm]["w"], CH[nm]["wa"]), wt, 0.16) for z in zf]
        hi = [wpct(f_cpl(z, CH[nm]["w"], CH[nm]["wa"]), wt, 0.84) for z in zf]
        ax[0].fill_between(zf, lo, hi, color=cols[nm], alpha=0.18, label=f"DESI DR2+{nm} 68% (CPL)")
    ax[0].axhline(1, color="k", lw=1.5, label="Lambda (w = -1): framework with constant a0 / PAPER42")
    r1 = PR["R1"]["can|A|Mmin1e+08"]
    zr = np.array([0, 0.5, 1, 2, 2.5]); rr = np.array([1] + [r1["rho_ratio"][str(z)] for z in (0.5, 1, 2, 2.5)])
    ax[0].plot(zr, 1 + (rr - 1) * 1e5, "r-o", ms=3, label="settling trickle (R1, can, A): deviation x 1e5")
    c4 = PR["M_C4"]["can"]
    ax[0].plot(zr, [1] + [c4["rho_vac_ratio"][str(z)] for z in (0.5, 1, 2, 2.5)], "m--s", ms=3,
               label="M-C4 vacuum -> cold at a0/c (record model, re-run)")
    ax[0].set_xlabel("z"); ax[0].set_ylabel("rho_DE(z) / rho_DE(0)"); ax[0].set_ylim(0.3, 1.6)
    ax[0].legend(fontsize=7, loc="lower left"); ax[0].set_title("Dark-energy density: framework-only predictions vs DESI")
    for nm in SN:
        wt = CH[nm]["weight"]
        lo = [wpct(np.sqrt(f_cpl(z, CH[nm]["w"], CH[nm]["wa"])), wt, 0.16) for z in zf]
        hi = [wpct(np.sqrt(f_cpl(z, CH[nm]["w"], CH[nm]["wa"])), wt, 0.84) for z in zf]
        ax[1].fill_between(zf, lo, hi, color=cols[nm], alpha=0.18)
    ax[1].axhline(1, color="k", lw=1.5)
    s571 = tr571["P-B|canon 9.36e-11"]["sigma_log10_a0_RH"]
    ax[1].errorbar([1.6], [1], yerr=[[1 - 10 ** -s571], [10 ** s571 - 1]], fmt="o", color="orange", capsize=4,
                   label=f"CFG571 KURVS sealed test: sigma(log a0) >= {s571:.2f} dex")
    req = R2["required_sigma_log10_a0"]["desy5"]
    zz4 = [0.5, 1.0, 2.0, 2.5]
    ax[1].errorbar(np.array(zz4) + 0.03, [1] * 4, yerr=[[1 - 10 ** -req[str(z)] for z in zz4], [10 ** req[str(z)] - 1 for z in zz4]],
                   fmt="s", color="teal", capsize=3, label="a0 precision needed to match DESI+DESY5 on rho_DE")
    sw = 3 * 0.1 / math.sqrt(20)
    ax[1].errorbar([2.3], [1], yerr=[[1 - 10 ** -sw], [10 ** sw - 1]], fmt="^", color="grey", capsize=3,
                   label=f"CFG256 wall, N = 20, 0.1 dex/obj: >= {sw:.3f} dex")
    ax[1].set_xlabel("z"); ax[1].set_ylabel("a0(z) / a0(0)   (kappa cancels)")
    sec = ax[1].secondary_yaxis("right", functions=(lambda x: np.clip(x, 1e-6, None) ** 2, lambda y: np.sqrt(np.clip(y, 1e-6, None))))
    sec.set_ylabel("rho_DE(z) / rho_DE(0) = (a0 ratio)^2")
    ax[1].set_ylim(0.45, 1.75); ax[1].legend(fontsize=7, loc="upper left")
    ax[1].set_title("Galaxies as the dark-energy thermometer (bands: DESI mapped)")
    fig.text(0.5, 0.005, "kappa = 1/2 fitted (cancels in ratios); cold energy mass required. DESI shown for comparison only; no DE data in the predictions.",
             ha="center", fontsize=7)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(os.path.join(HERE, "cfg549_prediction.png"), dpi=130)
    P("\nwrote cfg549_prediction.png")

ok = all(v["ok"] for v in R["checks"].values())
P("checks: " + ", ".join(f"{k_} {'PASS' if v['ok'] else 'FAIL'}" for k_, v in R["checks"].items()))
json.dump(R, open(os.path.join(HERE, f"cfg549_results{SUF}.json"), "w"), indent=1)
OUT.close()
sys.exit(0 if ok else 1)
