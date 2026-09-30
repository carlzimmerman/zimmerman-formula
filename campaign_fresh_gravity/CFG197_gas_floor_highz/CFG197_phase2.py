#!/usr/bin/env python3
"""CFG197 phase 2 -- the gas floor applied: per-galaxy s_req for the flat law, the rival a0 E(z) and Newton, bin verdicts.

Frozen criteria: campaign_fresh_gravity/CFG197_FROZEN_CRITERIA.md (committed in bb91eeb23 before this script existed).
  R_obs = g_obs(r)/g_star(r) with each paper's own estimator as primary (Danhaive: its M_dyn with k_tot = 1.8; CRISTAL, MSA-3D:
  V_rot(R_e)^2 + 3.36 sigma0^2 over R_e; KURVS: the paper's f_DM with its own thin-disc baryon model), plus the frozen sensitivities
  (recomputed / moderate pressure 1.68, KURVS at 3 R_D with alpha 6.0 / 3.0, three geometries, compact stars, V-lim, both footings,
  P2 and nu_mono).  log s_req = log10(Phi^-1(x R_obs)/x); bin median with a 4000-draw bootstrap (seed 197); the frozen
  DISFAVOURED / CONSISTENT / NON-DIAGNOSTIC lines, the robustness rule, ESTIMATOR-LIMITED, the pooling rule; the external field
  that would restore consistency for any DISFAVOURED primary verdict (reported only); the Roman-Oliveira gas-only over-prediction
  check against V_ext.
MUTATE=1 sets R_obs = 1 for every galaxy and variant (the RO check is unchanged): V1-V3 (the real-data identities) must FAIL.
Run: python3 campaign_fresh_gravity/CFG197_gas_floor_highz/CFG197_phase2.py   [MUTATE=1 for the control run]
"""
import os, sys, csv, math, json, builtins, itertools
import numpy as np
from scipy.special import i0, k0, i1, k1

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
SLUG = "CFG197_phase2" + ("_MUTATE" if MUT else "")
LINES, CHECKS, NUM = [], [], {}


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def check(name, detail, ok, load_bearing=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)


P(__doc__.split("Run: python3")[0].strip())
if MUT:
    P("\n*** MUTATE=1: R_obs = 1 for every galaxy and variant.  V1-V3 must FAIL; the run must exit 1. ***")

# ================================================================================================= constants (as the pre-flight)
G, MSUN, KPC = K.G_SI, K.MSUN, K.KPC
A0 = dict(K.A0)
FOOTS = K.FOOTS
OM = C.OM_PL
assert abs(OM - 0.3153) < 1e-12
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
RE_RD = 1.6783469900166625
UV2HA = 1.58
K_TOT = 1.8
F_THICK = 2.0 / K_TOT
LN10 = math.log(10.0)
SEED, NBOOT = 197, 4000
KERN = {"P2": K.nu_p2, "nu_mono": K.nu_mono}
LAWS = ("flat", "rival")
GEOMS = [("sph", "mlf"), ("thick", "mlf"), ("thin", "mlf"), ("sph", "compact"), ("thick", "compact"), ("thin", "compact")]
PRIM_G = ("sph", "mlf")
DISF, CONS, NOND = "DISFAVOURED", "CONSISTENT", "NON-DIAGNOSTIC"


def a0_law(foot, law, z):
    return A0[foot] * (E(z) if law == "rival" else 1.0)


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def e0(s):
    v = fnum(s)
    return v if np.isfinite(v) else 0.0


def g_freeman(M, R, Rd):
    y = R / (2.0 * Rd)
    return 2.0 * G * M * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (Rd * R)


def f_enc(t):
    return 1.0 - (1.0 + t) * math.exp(-t)


def gstar(M_msun, r_kpc, geom, rad, frac_mlf=0.5, rhalf_over_r=1.0):
    M, R = M_msun * MSUN, r_kpc * KPC
    rhalf = rhalf_over_r * R
    if rad == "mlf":
        Rd, fsph = rhalf / RE_RD, frac_mlf
    else:
        Rd = (rhalf / UV2HA) / RE_RD
        fsph = f_enc(R / Rd)
    if geom == "sph":
        return G * fsph * M / R ** 2
    if geom == "thick":
        return F_THICK * G * fsph * M / R ** 2
    return float(g_freeman(M, R, Rd))


def phi_inv(k, t, nit=90):
    t = np.asarray(t, float)
    lo, hi = np.full_like(t, math.log(1e-14)), np.log(np.maximum(t, 1e-14))
    for _ in range(nit):
        mid = 0.5 * (lo + hi)
        ym = np.exp(mid)
        big = ym * KERN[k](ym) > t
        hi = np.where(big, mid, hi)
        lo = np.where(big, lo, mid)
    return np.exp(0.5 * (lo + hi))


def log_sreq(k, x, R):
    x, R = np.asarray(x, float), np.asarray(R, float)
    if k == "Newton":
        return np.log10(R)
    if k == "P2":
        return np.log10(2.0 * x * R ** 2 / (np.sqrt(1.0 + 4.0 * x ** 2 * R ** 2) + 1.0))
    return np.log10(phi_inv(k, x * R) / x)


def verdict(st):
    if st["median"] < -0.30 and st["p95"] < -0.10:
        return DISF
    if st["median"] >= -0.10 and st["p5"] >= -0.30:
        return CONS
    return NOND


# ================================================================================================= data (phase 2: all columns needed)
banner("DATA AND ESTIMATORS (each paper's own estimator is primary)")
LOADED = []


def load(fname, cols):
    rows = []
    with builtins.open(os.path.join(AT, fname)) as fh:
        for r in csv.DictReader(fh):
            rows.append({c: r[c] for c in cols})
    LOADED.append((fname, tuple(cols)))
    return rows


def dlog_vc2(V, dV, S, dS, alpha):
    vc2 = V ** 2 + alpha * S ** 2
    return vc2, math.sqrt((2 * V * dV) ** 2 + (2 * alpha * S * dS) ** 2) / (vc2 * LN10)


GAL = []
MISSING_ERR = []
# ---- Danhaive+2025 gold
for r in load("danhaive2025_gold.csv", ["jades_id", "z", "logMstar", "logMstar_errhi", "logMstar_errlo", "logMstar_lim", "re_kpc",
                                         "re_kpc_errhi", "re_kpc_errlo", "re_kpc_lim", "v_over_sigma0", "v_over_sigma0_errhi",
                                         "v_over_sigma0_errlo", "v_over_sigma0_lim", "sigma0_kms", "sigma0_kms_errhi",
                                         "sigma0_kms_errlo", "sigma0_kms_lim", "logMdyn", "logMdyn_errhi", "logMdyn_errlo", "logMdyn_lim"]):
    z, lM, re = fnum(r["z"]), fnum(r["logMstar"]), fnum(r["re_kpc"])
    sM = 0.5 * (fnum(r["logMstar_errhi"]) + fnum(r["logMstar_errlo"]))
    lim = r["sigma0_kms_lim"] == "<"
    est = {}
    # primary: the paper's own M_dyn = k_tot r_e v_circ^2/G  ->  g_obs = G M_dyn/(k_tot r_e^2)
    gob = G * 10 ** fnum(r["logMdyn"]) * MSUN / (K_TOT * (re * KPC) ** 2)
    sD = 0.5 * (fnum(r["logMdyn_errhi"]) + fnum(r["logMdyn_errlo"]))
    est["paper"] = (gob, math.sqrt(sD ** 2 + sM ** 2))
    if not lim:
        est["paper_Vlim"] = est["paper"]
        q, dq = fnum(r["v_over_sigma0"]), 0.5 * (fnum(r["v_over_sigma0_errhi"]) + fnum(r["v_over_sigma0_errlo"]))
        s0, ds0 = fnum(r["sigma0_kms"]), 0.5 * (fnum(r["sigma0_kms_errhi"]) + fnum(r["sigma0_kms_errlo"]))
        sr = 0.5 * (fnum(r["re_kpc_errhi"]) + fnum(r["re_kpc_errlo"])) / (re * LN10)
        for al in (3.36, 1.68):
            vc2 = s0 ** 2 * (q ** 2 + al)
            dl = math.sqrt((2 * ds0 / s0) ** 2 + (2 * q * dq / (q ** 2 + al)) ** 2) / LN10
            est[f"recomp{al:.2f}"] = (vc2 * 1e6 / (re * KPC), math.sqrt(dl ** 2 + sr ** 2 + sM ** 2))
    assert r["logMdyn_lim"] == "" and r["logMstar_lim"] == "" and r["re_kpc_lim"] == ""
    GAL.append(dict(sample="danhaive", id=r["jades_id"], z=z, logM=lM, r=re, rhalf=1.0, frac=0.5, flags="sigma0<" if lim else "",
                    est=est, logMdyn=fnum(r["logMdyn"])))
# ---- ALMA-CRISTAL
samp = {r["id"]: r for r in load("cristal2025_sample.csv", ["id", "z_cii", "logMstar"])}
alias = {"09": "09a"}
for r in load("cristal2025_dynamics.csv", ["id", "Re_disk_kpc", "Re_disk_kpc_errhi", "Re_disk_kpc_errlo", "Vrot_Re_kms",
                                           "Vrot_Re_kms_errhi", "Vrot_Re_kms_errlo", "sigma0_kms", "sigma0_kms_errhi", "sigma0_kms_errlo"]):
    s_ = samp[alias.get(r["id"], r["id"])]
    if not np.isfinite(fnum(s_["logMstar"])):
        continue
    re = fnum(r["Re_disk_kpc"])
    fixed = not np.isfinite(fnum(r["Re_disk_kpc_errhi"]))
    sr = 0.0 if fixed else 0.5 * (fnum(r["Re_disk_kpc_errhi"]) + fnum(r["Re_disk_kpc_errlo"])) / (re * LN10)
    V, dV = fnum(r["Vrot_Re_kms"]), 0.5 * (fnum(r["Vrot_Re_kms_errhi"]) + fnum(r["Vrot_Re_kms_errlo"]))
    S, dS = fnum(r["sigma0_kms"]), 0.5 * (fnum(r["sigma0_kms_errhi"]) + fnum(r["sigma0_kms_errlo"]))
    est = {}
    for al in (3.36, 1.68):
        vc2, dl = dlog_vc2(V, dV, S, dS, al)
        est[f"a{al:.2f}"] = (vc2 * 1e6 / (re * KPC), math.sqrt(dl ** 2 + sr ** 2 + 0.2 ** 2))
    GAL.append(dict(sample="cristal", id=r["id"], z=fnum(s_["z_cii"]), logM=fnum(s_["logMstar"]), r=re, rhalf=1.0, frac=0.5,
                    flags="Re_fixed" if fixed else "", est=est, V=V, S=S))
# ---- MSA-3D
mg = {r["id"]: r for r in load("msa3d_galaxies.csv", ["id", "sample", "z", "logMstar", "footnote"])}
for r in load("msa3d_kinematics.csv", ["id", "re_disk_kpc", "re_disk_kpc_errhi", "re_disk_kpc_errlo", "vrot_re_kms",
                                       "vrot_re_kms_errhi", "vrot_re_kms_errlo", "sigma0_kms", "sigma0_kms_errhi", "sigma0_kms_errlo",
                                       "sigma0_kms_flag"]):
    g_ = mg[r["id"]]
    re = fnum(r["re_disk_kpc"])
    for c in ("re_disk_kpc_errhi", "re_disk_kpc_errlo", "vrot_re_kms_errhi", "vrot_re_kms_errlo", "sigma0_kms_errhi", "sigma0_kms_errlo"):
        if not np.isfinite(fnum(r[c])):
            MISSING_ERR.append(("msa3d", r["id"], c))
    sr = 0.5 * (e0(r["re_disk_kpc_errhi"]) + e0(r["re_disk_kpc_errlo"])) / (re * LN10)
    V, dV = fnum(r["vrot_re_kms"]), 0.5 * (e0(r["vrot_re_kms_errhi"]) + e0(r["vrot_re_kms_errlo"]))
    S, dS = fnum(r["sigma0_kms"]), 0.5 * (e0(r["sigma0_kms_errhi"]) + e0(r["sigma0_kms_errlo"]))
    est = {}
    for al in (3.36, 1.68):
        vc2, dl = dlog_vc2(V, dV, S, dS, al)
        est[f"a{al:.2f}"] = (vc2 * 1e6 / (re * KPC), math.sqrt(dl ** 2 + sr ** 2 + 0.2 ** 2))
    fl = ",".join(f for f in (("fn_" + g_["footnote"]) if g_["footnote"] else "", ("sigma0_" + r["sigma0_kms_flag"]) if r["sigma0_kms_flag"] else "") if f)
    GAL.append(dict(sample="msa3d", id=r["id"], z=fnum(g_["z"]), logM=fnum(g_["logMstar"]), r=re, rhalf=1.0, frac=0.5, flags=fl,
                    golden=(g_["sample"] == "golden"), est=est, V=V, S=S))
# ---- KURVS-CDFS: primary = the paper's f_DM with its thin-disc baryon model (M_bar = M*/0.6); sensitivity at 3 R_D
ki = {r["kurvs_id"]: r for r in load("kurvs2023_integrated.csv", ["kurvs_id", "z_halpha", "logMstar", "reff_kpc", "e_reff"])}
kk = {r["kurvs_id"]: r for r in load("kurvs2023_kinematics.csv", ["kurvs_id", "sigma0_kms", "e_sigma0"])}
kv = {r["kurvs_id"]: r for r in load("kurvs2023_velocities_at_radii.csv", ["kurvs_id", "v_at_R3D_kms", "e_v_R3D"])}
for r in load("kurvs2023_fdm.csv", ["kurvs_id", "flag_star", "fDM_within_reff", "e_fDM"]):
    g_ = ki[r["kurvs_id"]]
    z, lM, re = fnum(g_["z_halpha"]), fnum(g_["logMstar"]), fnum(g_["reff_kpc"])
    fdm = fnum(r["fDM_within_reff"])
    if not np.isfinite(fnum(r["e_fDM"])):
        MISSING_ERR.append(("kurvs", r["kurvs_id"], "e_fDM"))
    gthin = gstar(10 ** lM, re, "thin", "mlf")
    est = {"fdm": (gthin / 0.6 / (1.0 - fdm), math.sqrt((e0(r["e_fDM"]) / ((1.0 - fdm) * LN10)) ** 2 + 0.2 ** 2))}
    GAL.append(dict(sample="kurvs", id=r["kurvs_id"], z=z, logM=lM, r=re, rhalf=1.0, frac=0.5,
                    flags="flag_star" if r["flag_star"] else "", est=est, fdm=fdm))
    r3 = 3.0 * re / RE_RD
    V, dV = fnum(kv[r["kurvs_id"]]["v_at_R3D_kms"]), fnum(kv[r["kurvs_id"]]["e_v_R3D"])
    S, dS = fnum(kk[r["kurvs_id"]]["sigma0_kms"]), fnum(kk[r["kurvs_id"]]["e_sigma0"])
    sr = fnum(g_["e_reff"]) / (re * LN10)
    est3 = {}
    for al in (6.0, 3.0):
        vc2, dl = dlog_vc2(V, dV, S, dS, al)
        est3[f"3RD_a{al:.1f}"] = (vc2 * 1e6 / (r3 * KPC), math.sqrt(dl ** 2 + sr ** 2 + 0.2 ** 2))
    GAL.append(dict(sample="kurvs3RD", id=r["kurvs_id"], z=z, logM=lM, r=r3, rhalf=RE_RD / 3.0, frac=f_enc(3.0), flags="", est=est3))

for g_ in GAL:
    g_["gs"] = {v: gstar(10 ** g_["logM"], g_["r"], *v, frac_mlf=g_["frac"], rhalf_over_r=g_["rhalf"]) for v in GEOMS}


def S_(sample, estk, filt=None):
    return [(g, estk) for g in GAL if g["sample"] == sample and estk in g["est"] and (filt is None or filt(g))]


# bins: {bin: {estimator-variant: [(galaxy, estimator key), ...]}}; the first estimator-variant is the primary
BINS = {
    "z>3.5 pooled (Danhaive + CRISTAL)": {
        "primary (paper M_dyn + CRISTAL 3.36)": S_("danhaive", "paper") + S_("cristal", "a3.36"),
        "V-lim (sigma0 detected)": S_("danhaive", "paper_Vlim") + S_("cristal", "a3.36"),
        "recomputed, paper pressure 3.36": S_("danhaive", "recomp3.36") + S_("cristal", "a3.36"),
        "moderate pressure 1.68": S_("danhaive", "recomp1.68") + S_("cristal", "a1.68")},
    "Halpha sub-bin: Danhaive gold": {
        "primary (paper M_dyn)": S_("danhaive", "paper"),
        "V-lim (sigma0 detected)": S_("danhaive", "paper_Vlim"),
        "recomputed, paper pressure 3.36": S_("danhaive", "recomp3.36"),
        "moderate pressure 1.68": S_("danhaive", "recomp1.68")},
    "[CII] sub-bin: CRISTAL": {
        "primary (3.36)": S_("cristal", "a3.36"),
        "moderate pressure 1.68": S_("cristal", "a1.68")},
    "comparison: MSA-3D (all 30)": {
        "primary (3.36)": S_("msa3d", "a3.36"),
        "moderate pressure 1.68": S_("msa3d", "a1.68")},
    "comparison: KURVS (10)": {
        "primary (paper f_DM)": S_("kurvs", "fdm"),
        "3 R_D, pressure 6.0": S_("kurvs3RD", "3RD_a6.0"),
        "3 R_D, moderate 3.0": S_("kurvs3RD", "3RD_a3.0")},
    "reported: MSA-3D golden": {
        "primary (3.36)": S_("msa3d", "a3.36", lambda g: g.get("golden")),
        "moderate pressure 1.68": S_("msa3d", "a1.68", lambda g: g.get("golden"))},
}
PF_NAME = {"z>3.5 pooled (Danhaive + CRISTAL)": "z>3.5 pooled (Danhaive + CRISTAL)", "Halpha sub-bin: Danhaive gold": "Halpha sub-bin: Danhaive gold",
           "[CII] sub-bin: CRISTAL": "[CII] sub-bin: CRISTAL", "comparison: MSA-3D (all 30)": "comparison: MSA-3D (all 30)",
           "comparison: KURVS (10)": "comparison: KURVS (10, r = R_eff)", "reported: MSA-3D golden": "MSA-3D golden"}
for b, ev in BINS.items():
    P(f"  {b:36s} " + ";  ".join(f"{k_}: N = {len(v_)}" for k_, v_ in ev.items()))
P(f"  missing tabulated errors set to 0 (reported): {len(MISSING_ERR)} -> {MISSING_ERR}")
P("  no ratio is tabulated as a limit (Danhaive logMdyn_lim, logMstar_lim, re_kpc_lim all empty; asserted) -> no median bracketing is needed")

# ================================================================================================= R_obs, and the real-data identities
def R_obs(g, estk, geom):
    if MUT:
        return 1.0
    return g["est"][estk][0] / g["gs"][geom]


banner("REAL-DATA IDENTITIES (V1-V3: must FAIL under MUTATE) and ties to phase 1")
dan = [g for g in GAL if g["sample"] == "danhaive"]
v1 = max(abs(R_obs(g, "paper", PRIM_G) / ((2.0 / K_TOT) * 10 ** (g["logMdyn"] - g["logM"])) - 1.0) for g in dan)
check("V1 Danhaive primary R_obs (sphere, mass follows light) = (2/1.8) x 10^(logMdyn - logM*) for all 41 (the paper's own ratio)",
      f"max relative deviation {v1:.1e}", v1 < 1e-12)
kur = [g for g in GAL if g["sample"] == "kurvs"]
v2 = max(abs(R_obs(g, "fdm", ("thin", "mlf")) / ((1.0 / 0.6) / (1.0 - g["fdm"])) - 1.0) for g in kur)
check("V2 KURVS primary R_obs in the paper's thin-disc geometry = (1/0.6)/(1 - f_DM) for all 10", f"max relative deviation {v2:.1e}", v2 < 1e-12)
cm = [g for g in GAL if g["sample"] in ("cristal", "msa3d")]
v3 = max(abs(R_obs(g, "a3.36", PRIM_G) / (2.0 * (g["V"] ** 2 + 3.36 * g["S"] ** 2) * 1e6 * g["r"] * KPC / (G * 10 ** g["logM"] * MSUN)) - 1.0)
         for g in cm)
check("V3 CRISTAL and MSA-3D primary R_obs = 2 (V_rot^2 + 3.36 sigma0^2) R_e/(G M*) (an independent formula) for all 42",
      f"max relative deviation {v3:.1e}", v3 < 1e-12)
PF = json.load(builtins.open(os.path.join(LANE, "CFG197_preflight_results.json")))["numbers"]
tie = []
for b, pb in PF_NAME.items():
    gs = [g for g, _ in list(BINS[b].values())[0]]
    xf = np.median([g["gs"][PRIM_G] / a0_law("canonical", "flat", g["z"]) for g in gs])
    tie.append(abs(xf / PF[f"{pb}|P2|canonical"]["median_x_flat"] - 1.0))
check("C0 phase 2's g_star reproduces the committed pre-flight's bin-median x_flat (P2, canonical) in every bin", f"max rel. dev. {max(tie):.1e}",
      max(tie) < 1e-12)
nD = len(BINS["Halpha sub-bin: Danhaive gold"]["primary (paper M_dyn)"])
check("C0b counts as frozen: Danhaive 41 (24 with sigma0 detected), CRISTAL 12, MSA-3D 30 (23 golden), KURVS 10",
      f"{nD}, {len(BINS['Halpha sub-bin: Danhaive gold']['V-lim (sigma0 detected)'])}, {len(BINS['[CII] sub-bin: CRISTAL']['primary (3.36)'])}, "
      f"{len(BINS['comparison: MSA-3D (all 30)']['primary (3.36)'])} ({len(BINS['reported: MSA-3D golden']['primary (3.36)'])}), "
      f"{len(BINS['comparison: KURVS (10)']['primary (paper f_DM)'])}",
      nD == 41 and len(BINS["Halpha sub-bin: Danhaive gold"]["V-lim (sigma0 detected)"]) == 24 and len(BINS["[CII] sub-bin: CRISTAL"]["primary (3.36)"]) == 12
      and len(BINS["comparison: MSA-3D (all 30)"]["primary (3.36)"]) == 30 and len(BINS["reported: MSA-3D golden"]["primary (3.36)"]) == 23
      and len(BINS["comparison: KURVS (10)"]["primary (paper f_DM)"]) == 10)
# reported: the recomputed Danhaive ratio at the paper's pressure term against the paper's own M_dyn
d_rc = [math.log10(g["est"]["recomp3.36"][0] / g["est"]["paper"][0]) for g in dan if "recomp3.36" in g["est"]]
P(f"  (reported) Danhaive recomputed (v/sigma0 x sigma0, alpha 3.36) vs the paper's M_dyn, log g_obs ratio over the 24: median "
  f"{np.median(d_rc):+.3f} dex, range {min(d_rc):+.3f} to {max(d_rc):+.3f} (k_tot = 1.8 cancels; posterior medians vs products of medians)")
NUM["danhaive_recomp_vs_paper_dex"] = dict(median=float(np.median(d_rc)), min=float(min(d_rc)), max=float(max(d_rc)))


# ================================================================================================= the statistic over all variants
def stats(vals, idx):
    m = np.median(vals[idx], axis=1)
    return dict(median=float(np.median(vals)), p5=float(np.percentile(m, 5)), p16=float(np.percentile(m, 16)),
                p84=float(np.percentile(m, 84)), p95=float(np.percentile(m, 95)))


RES = {}          # (bin, estvar, geom, law, kernel, foot) -> stats + verdict + n_below
PERGAL = {}       # (bin, estvar, geom) -> dict of arrays for printing
for b, ev in BINS.items():
    for evn, members in ev.items():
        n = len(members)
        idx = np.random.default_rng(SEED).integers(0, n, size=(NBOOT, n))
        for geom in GEOMS:
            R = np.array([R_obs(g, k_, geom) for g, k_ in members])
            sR = np.array([g["est"][k_][1] for g, k_ in members])
            gsv = np.array([g["gs"][geom] for g, _ in members])
            z = np.array([g["z"] for g, _ in members])
            lsN = log_sreq("Newton", 1.0, R)
            st = stats(lsN, idx)
            st["verdict"] = verdict(st)
            st["n_below"] = int(np.sum(log_sreq("Newton", 1.0, R * 10 ** sR) < 0))
            for k in KERN:
                for f in FOOTS:
                    RES[(b, evn, geom, "Newton", k, f)] = st
            pg = dict(R=R, sR=sR, N=lsN)
            for k in KERN:
                for f in FOOTS:
                    for law in LAWS:
                        x = gsv / np.array([a0_law(f, law, zi) for zi in z])
                        ls = log_sreq(k, x, R)
                        st = stats(ls, idx)
                        st["verdict"] = verdict(st)
                        st["n_below"] = int(np.sum(log_sreq(k, x, R * 10 ** sR) < 0))
                        RES[(b, evn, geom, law, k, f)] = st
                        pg[(law, k, f)] = ls
                        pg[("x", law, f)] = x
            PERGAL[(b, evn, geom)] = pg

# ================================================================================================= per-galaxy tables (primary)
banner("PER-GALAXY, primary estimator and variant (sphere, mass follows light), P2.  log s_req: Newton | flat c/a | rival c/a.  "
       "'*' = BELOW FLOOR even with R_obs raised by 1 sigma")
for b in ("z>3.5 pooled (Danhaive + CRISTAL)", "comparison: MSA-3D (all 30)", "comparison: KURVS (10)"):
    evn = list(BINS[b].keys())[0]
    members = BINS[b][evn]
    pg = PERGAL[(b, evn, PRIM_G)]
    P(f"\n  {b} [{evn}]")
    P(f"  {'sample':9s} {'id':>9s} {'z':>5s} {'logM*':>6s} {'r':>5s} {'R_obs':>6s} {'sig':>5s} {'x_f(c)':>7s} {'Newton':>7s} "
      f"{'flat c':>7s} {'flat a':>7s} {'rival c':>7s} {'rival a':>7s}  flags")
    for i, (g, k_) in enumerate(members):
        def mk(v, sR=pg["sR"][i], R=pg["R"][i], law=None, f=None):
            if law is None:
                below = math.log10(R * 10 ** sR) < 0
            else:
                below = float(log_sreq("P2", pg[("x", law, f)][i], R * 10 ** sR)) < 0
            return f"{v:+7.3f}" + ("*" if below else " ")
        P(f"  {g['sample']:9s} {g['id']:>9s} {g['z']:5.2f} {g['logM']:6.2f} {g['r']:5.2f} {pg['R'][i]:6.2f} {pg['sR'][i]:5.2f} "
          f"{pg[('x', 'flat', 'canonical')][i]:7.3f} {mk(pg['N'][i])}{mk(pg[('flat', 'P2', 'canonical')][i], law='flat', f='canonical')}"
          f"{mk(pg[('flat', 'P2', 'alt')][i], law='flat', f='alt')}{mk(pg[('rival', 'P2', 'canonical')][i], law='rival', f='canonical')}"
          f"{mk(pg[('rival', 'P2', 'alt')][i], law='rival', f='alt')} {g['flags']}")

# ================================================================================================= bin results, primary
banner("BIN RESULTS, primary estimator and variant: median log s_req [bootstrap p5, p16, p84, p95] -> frozen label; n BELOW FLOOR (1 sigma)")
for b, ev in BINS.items():
    evn = list(ev.keys())[0]
    P(f"\n  {b} [{evn}], N = {len(ev[evn])}")
    st = RES[(b, evn, PRIM_G, "Newton", "P2", "canonical")]
    P(f"    Newton                    {st['median']:+.3f} [{st['p5']:+.3f}, {st['p16']:+.3f}, {st['p84']:+.3f}, {st['p95']:+.3f}] -> "
      f"{st['verdict']:14s} below floor {st['n_below']}/{len(ev[evn])}   (median R_obs = {10 ** st['median']:.2f})")
    for k in KERN:
        for law in LAWS:
            for f in FOOTS:
                st = RES[(b, evn, PRIM_G, law, k, f)]
                P(f"    {law:5s} {k:7s} {f:9s}   {st['median']:+.3f} [{st['p5']:+.3f}, {st['p16']:+.3f}, {st['p84']:+.3f}, {st['p95']:+.3f}] -> "
                  f"{st['verdict']:14s} below floor {st['n_below']}/{len(ev[evn])}")

# ================================================================================================= variant grid
banner("VARIANT GRID (P2): median log s_req and label (D = DISFAVOURED, C = CONSISTENT, N = NON-DIAGNOSTIC) in every declared variant")
LET = {DISF: "D", CONS: "C", NOND: "N"}
for b, ev in BINS.items():
    P(f"\n  {b}")
    P(f"    {'estimator variant':38s} {'geometry':15s} {'Newton':>9s} {'flat c':>9s} {'flat a':>9s} {'rival c':>9s} {'rival a':>9s}")
    for evn in ev:
        for geom in GEOMS:
            cells = [RES[(b, evn, geom, "Newton", "P2", "canonical")]]
            cells += [RES[(b, evn, geom, law, "P2", f)] for law in LAWS for f in FOOTS]
            P(f"    {evn:38s} {geom[0] + '/' + geom[1]:15s} " + " ".join(f"{c['median']:+7.3f} {LET[c['verdict']]}" for c in cells))


# ================================================================================================= headlines under the frozen rules
def headline(b, law, k):
    ev = BINS[b]
    evp = list(ev.keys())[0]
    prim = {f: RES[(b, evp, PRIM_G, law, k, f)]["verdict"] for f in FOOTS}
    allv = {RES[(b, evn, geom, law, k, f)]["verdict"] for evn in ev for geom in GEOMS for f in FOOTS}
    if prim["canonical"] != prim["alt"]:
        return NOND, f"footings disagree ({prim['canonical']} / {prim['alt']})", prim, allv
    p = prim["canonical"]
    if p == NOND:
        return NOND, "primary NON-DIAGNOSTIC", prim, allv
    if allv == {p}:
        return p, "robust (every variant, both footings)", prim, allv
    return NOND, f"primary only ({p}); variants give {sorted(allv)}", prim, allv


banner("HEADLINES under the frozen rules (robustness, ESTIMATOR-LIMITED, pooling).  Kernel P2 is the headline; nu_mono is reported")
HEAD = {}
for b, ev in BINS.items():
    evp = list(ev.keys())[0]
    nmed = RES[(b, evp, PRIM_G, "Newton", "P2", "canonical")]["median"]
    limited = nmed < -0.10
    nN = {RES[(b, evn, geom, "Newton", "P2", "canonical")]["verdict"] for evn in ev for geom in GEOMS}
    newton_head = (RES[(b, evp, PRIM_G, "Newton", "P2", "canonical")]["verdict"] if len(nN) == 1 else NOND)
    P(f"\n  {b}:  Newton median log R_obs {nmed:+.3f} -> {'ESTIMATOR-LIMITED' if limited else 'not estimator-limited'}; "
      f"Newton's own label {RES[(b, evp, PRIM_G, 'Newton', 'P2', 'canonical')]['verdict']} (robust over variants: {newton_head}; "
      f"variant labels {sorted(nN)})")
    for k in KERN:
        for law in LAWS:
            h, why, prim, allv = headline(b, law, k)
            final = NOND if (limited and h != NOND) else h
            why2 = why + ("; ESTIMATOR-LIMITED -> NON-DIAGNOSTIC" if (limited and h != NOND) else "")
            HEAD[(b, law, k)] = dict(headline=final, reason=why2, primary=prim, variant_labels=sorted(allv), limited=limited)
            P(f"    {law:5s} {k:7s}: {final:14s}  ({why2})")
    HEAD[(b, "Newton")] = dict(median=nmed, limited=limited, label=RES[(b, evp, PRIM_G, "Newton", "P2", "canonical")]["verdict"],
                               robust=newton_head)
# pooling rule on the primary verdicts of the two sub-bins
pool = "z>3.5 pooled (Danhaive + CRISTAL)"
for law in LAWS:
    opp = []
    for f in FOOTS:
        a_ = RES[("Halpha sub-bin: Danhaive gold", "primary (paper M_dyn)", PRIM_G, law, "P2", f)]["verdict"]
        c_ = RES[("[CII] sub-bin: CRISTAL", "primary (3.36)", PRIM_G, law, "P2", f)]["verdict"]
        if {a_, c_} == {DISF, CONS}:
            opp.append(f)
    if opp:
        HEAD[(pool, law, "P2")]["headline"] = NOND
        HEAD[(pool, law, "P2")]["reason"] += f"; POOLING RULE: sub-bins opposite in {opp} -> NON-DIAGNOSTIC"
    P(f"  pooling rule ({law}): sub-bins opposite (one DISFAVOURED, the other CONSISTENT) in footings {opp or 'none'}")
# nu_mono vs P2
for b in BINS:
    for law in LAWS:
        if HEAD[(b, law, "P2")]["headline"] != HEAD[(b, law, "nu_mono")]["headline"]:
            P(f"  nu_mono differs from P2: {b} / {law}: P2 {HEAD[(b, law, 'P2')]['headline']}, nu_mono {HEAD[(b, law, 'nu_mono')]['headline']}")
# separation / flat-law failure statements
PFV = {k_.strip(): v_ for k_, v_ in PF["verdicts"].items()}
P("")
for b in BINS:
    hf, hr = HEAD[(b, "flat", "P2")]["headline"], HEAD[(b, "rival", "P2")]["headline"]
    pfv = PFV.get(PF_NAME[b], "?")
    sep = hr == DISF and hf == CONS and not HEAD[(b, "Newton")]["limited"] and pfv == "CAN"
    both = hr == DISF and hf == DISF and not HEAD[(b, "Newton")]["limited"]
    P(f"  {b:36s} pre-flight {pfv:8s} headline flat {hf:14s} rival {hr:14s} -> "
      + ("the gas floor SEPARATES the laws (rival DISFAVOURED, flat CONSISTENT)" if sep else
         ("BOTH DISFAVOURED: a failure of the flat law against Newton/LCDM" if both else "no separation")))
    HEAD[(b, "outcome")] = "separates" if sep else ("both disfavoured" if both else "no separation")


# ================================================================================================= external field for DISFAVOURED primary verdicts
def s_req_efe(k, x, R, e):
    """s with s nu(s x + e) = R (monotone in s for e >= 0): the 1-D external-field approximation of the floor."""
    lo, hi = np.full_like(x, math.log(1e-8)), np.log(np.maximum(R, 1e-8))
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        s = np.exp(mid)
        big = s * KERN[k](s * x + e) > R
        hi = np.where(big, mid, hi)
        lo = np.where(big, lo, mid)
    return np.exp(0.5 * (lo + hi))


banner("EXTERNAL FIELD (reported only; no verdict changes): the e (in units of that law's a0) that lifts the primary median log s_req to -0.10")
EFE = {}
any_d = False
for b, ev in BINS.items():
    evp = list(ev.keys())[0]
    members = ev[evp]
    R = np.array([R_obs(g, k_, PRIM_G) for g, k_ in members])
    gsv = np.array([g["gs"][PRIM_G] for g, _ in members])
    z = np.array([g["z"] for g, _ in members])
    for law in LAWS:
        for f in FOOTS:
            if RES[(b, evp, PRIM_G, law, "P2", f)]["verdict"] != DISF:
                continue
            any_d = True
            x = gsv / np.array([a0_law(f, law, zi) for zi in z])
            med = lambda e: float(np.median(np.log10(s_req_efe("P2", x, R, e))))
            if med(1e3) < -0.10:
                EFE[(b, law, f)] = None
                P(f"  {b:36s} {law:5s} {f:9s}: not restored even at e = 1000")
                continue
            lo, hi = 0.0, 1e3
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if med(mid) < -0.10 else (lo, mid)
            EFE[(b, law, f)] = hi
            P(f"  {b:36s} {law:5s} {f:9s}: e = {hi:.3f} a0_law  (median x of the bin {np.median(x):.3f})")
if not any_d:
    P("  no primary P2 verdict is DISFAVOURED: nothing to report")

# ================================================================================================= Roman-Oliveira over-prediction check
banner("ROMAN-OLIVEIRA: gas-only over-prediction check against V_ext (lower side only; no M* on disk).  Unchanged under MUTATE")
ro_s = {r["id"]: r for r in load("romanoliveira2023_sample.csv", ["id", "z", "kpc_per_arcsec"])}
ro_g = {r["id"]: r for r in load("romanoliveira2023_gasmasses.csv", ["id", "mh2_msun", "e_mh2", "mh2_flag"])}
ro_k = load("romanoliveira2023_kinematics.csv", ["id", "vrot_ext_kms", "vrot_ext_kms_errhi", "vrot_ext_kms_errlo", "sigma_ext_kms",
                                                 "sigma_ext_kms_errhi", "sigma_ext_kms_errlo"])
RINGS = {"BRI1335-0417": (5, 0.15), "J081740": (4, 0.13), "SGP38326-1": (5, 0.13), "SGP38326-2": (3, 0.12)}
RO = {}
P("  margin = (log g_obs - log g_floor)/sigma; OVER-PREDICTS needs margin < -2 in the primary AND every variant "
  "(ring radius x f_g x alpha x footing)")
P(f"  {'id':13s} {'V_ext':>6s} {'s_ext':>6s} {'law':6s} {'kernel':7s}  primary: {'r_ext':>5s} {'log g_obs':>9s} {'log g_fl':>8s} {'sigma':>6s} "
  f"{'margin':>7s}   margin range over variants   label")
for r in ro_k:
    sid = r["id"]
    z = fnum(ro_s[sid]["z"])
    V, dV = fnum(r["vrot_ext_kms"]), 0.5 * (fnum(r["vrot_ext_kms_errhi"]) + fnum(r["vrot_ext_kms_errlo"]))
    S, dS = fnum(r["sigma_ext_kms"]), 0.5 * (fnum(r["sigma_ext_kms_errhi"]) + fnum(r["sigma_ext_kms_errlo"]))
    mh2 = fnum(ro_g[sid]["mh2_msun"])
    em = fnum(ro_g[sid]["e_mh2"])
    s_q = (em / mh2 / LN10) if np.isfinite(em) else 0.3                  # SGP38326-1/2: no quoted error -> 0.3 dex (frozen)
    s_gas = math.sqrt(s_q ** 2 + 0.3 ** 2)                               # plus 0.3 dex for alpha_CO (frozen)
    nr, rs = RINGS[sid]
    kpa = fnum(ro_s[sid]["kpc_per_arcsec"])
    for law in ("Newton",) + LAWS:
        for k in (("P2", "nu_mono") if law != "Newton" else ("-",)):
            margins = {}
            for ring, off in (("primary", 1.0), ("variant", 1.5)):
                rext = (nr - off) * rs * kpa
                for fg in (0.5, 0.25):
                    for al in (0.0, 2.0):
                        for f in FOOTS:
                            vc2, dl_obs = dlog_vc2(V, dV, S, dS, al)
                            gobs = vc2 * 1e6 / (rext * KPC)
                            gg = G * fg * mh2 * MSUN / (rext * KPC) ** 2
                            if law == "Newton":
                                gfl, slope = gg, 1.0
                            else:
                                a = a0_law(f, law, z)
                                y = gg / a
                                gfl = a * y * float(KERN[k](y))
                                eps = 1e-6
                                slope = (math.log(y * (1 + eps) * float(KERN[k](y * (1 + eps)))) - math.log(y * (1 - eps) * float(KERN[k](y * (1 - eps))))) / (2 * eps)
                            sig = math.sqrt(dl_obs ** 2 + (slope * s_gas) ** 2)
                            margins[(ring, fg, al, f)] = dict(r_ext=rext, log_gobs=math.log10(gobs), log_gfloor=math.log10(gfl), sigma=sig,
                                                             margin=(math.log10(gobs) - math.log10(gfl)) / sig)
            pm = margins[("primary", 0.5, 0.0, "canonical")]
            allm = [m["margin"] for m in margins.values()]
            over = all(m < -2.0 for m in allm)
            lab = "OVER-PREDICTS" if over else ("no over-prediction" if all(m >= -2.0 for m in allm) else "over-predicts in some variants only")
            RO[(sid, law, k)] = dict(primary=pm, margin_min=min(allm), margin_max=max(allm), label=lab,
                                     V_ext=V, sigma_ext=S, mh2=mh2, s_gas_dex=s_gas)
            P(f"  {sid:13s} {V:6.1f} {S:6.1f} {law:6s} {k:7s}           {pm['r_ext']:5.2f} {pm['log_gobs']:9.3f} {pm['log_gfloor']:8.3f} "
              f"{pm['sigma']:6.3f} {pm['margin']:+7.2f}   {min(allm):+6.2f} to {max(allm):+6.2f}              {lab}")
P("  (the primary column is: last-two-ring radius (N - 1) RADSEP, f_g = 0.5, alpha = 0, canonical footing)")

# ================================================================================================= controls
banner("CONTROLS")
_E = E
E = lambda z: 1.0
c1 = 0.0
for b, ev in BINS.items():
    for evn, members in ev.items():
        for geom in (PRIM_G, ("thin", "compact")):
            R = np.array([R_obs(g, k_, geom) for g, k_ in members])
            gsv = np.array([g["gs"][geom] for g, _ in members])
            z = np.array([g["z"] for g, _ in members])
            for k in KERN:
                for f in FOOTS:
                    xf = gsv / np.array([a0_law(f, "flat", zi) for zi in z])
                    xr = gsv / np.array([a0_law(f, "rival", zi) for zi in z])
                    c1 = max(c1, float(np.max(np.abs(log_sreq(k, xr, R) - log_sreq(k, xf, R)))))
E = _E
check("C1 E(z) = 1 makes the rival identical to the flat law on the real R_obs (all bins and estimator variants, two geometries, both "
      "kernels and footings)", f"max |dlog s_req| = {c1:.1e}", c1 < 1e-12)
c2 = []
for b, ev in BINS.items():
    evp = list(ev.keys())[0]
    for k in KERN:
        for f in FOOTS:
            for law in LAWS:
                c2.append(float(log_sreq(k, np.median(PERGAL[(b, evp, PRIM_G)][("x", law, f)]), 1.0)))
check("C2 a planted galaxy with R_obs = 1 at each bin's median x is below both laws' floors (log s_req < 0), Newton exactly 0",
      f"max law log s_req {max(c2):+.4f}; Newton {float(log_sreq('Newton', 1.0, 1.0)):+.1e}", max(c2) < 0 and float(log_sreq("Newton", 1.0, 1.0)) == 0)
c3 = 0.0
for g in GAL:
    for f in FOOTS:
        for k in KERN:
            for law in LAWS:
                xx = g["gs"][PRIM_G] / a0_law(f, law, g["z"])
                c3 = max(c3, abs(float(log_sreq(k, xx, KERN[k](xx)))))
check("C3 a planted galaxy exactly on a law's floor has log s_req = 0 (to 1e-9)", f"max |log s_req| = {c3:.1e}", c3 < 1e-9)
c4 = min(float(log_sreq(k, g["gs"][PRIM_G] / a0_law(f, "flat", g["z"]), 2.0 * KERN[k](2.0 * g["gs"][PRIM_G] / a0_law(f, "flat", g["z"]))))
         for g in GAL for f in FOOTS for k in KERN)
check("C4 a planted flat-law galaxy with gas mu = 1 has flat log s_req > 0", f"min = {c4:+.4f}", c4 > 0)
c5 = max(float(np.max(PERGAL[key][("rival", k, f)] - PERGAL[key][("flat", k, f)])) for key in PERGAL for k in KERN for f in FOOTS)
check("C5 the rival's log s_req never exceeds the flat law's for any real galaxy in any variant (L4)", f"max (rival - flat) = {c5:+.2e}", c5 <= 1e-12)
if MUT:
    allneg = all(float(np.max(PERGAL[key][(law, k, f)])) < 0 for key in PERGAL for law in LAWS for k in KERN for f in FOOTS)
    nzero = max(abs(float(np.max(PERGAL[key]["N"]))) for key in PERGAL)
    check("M-C2 (C2 at scale) with R_obs = 1 every galaxy lies below both laws' floors in every variant (log s_req < 0), Newton exactly 0",
          f"all law values < 0: {allneg}; max |Newton| = {nzero:.1e}", allneg and nzero == 0.0)
    exp_all = [(b, law, RES[(b, list(ev.keys())[0], PRIM_G, law, 'P2', f)]['verdict'], f) for b, ev in BINS.items() for law in LAWS for f in FOOTS]
    bad = [t for t in exp_all if t[2] != DISF]
    check("M-EXP (the frozen expectation, kept as written) under R_obs = 1 every bin comes out DISFAVOURED for both laws (primary, P2)",
          f"{len(exp_all) - len(bad)}/{len(exp_all)} are DISFAVOURED; not: {bad}", not bad, load_bearing=False)

# ================================================================================================= bottom line
banner("BOTTOM LINE (frozen labels; P2 headline, nu_mono reported)")
P(f"  {'bin':36s} {'Newton median':>13s}  {'flat (P2)':14s} {'rival (P2)':14s} {'flat (nu_mono)':14s} {'rival (nu_mono)':15s} outcome")
for b in BINS:
    P(f"  {b:36s} {HEAD[(b, 'Newton')]['median']:+13.3f}  {HEAD[(b, 'flat', 'P2')]['headline']:14s} {HEAD[(b, 'rival', 'P2')]['headline']:14s} "
      f"{HEAD[(b, 'flat', 'nu_mono')]['headline']:14s} {HEAD[(b, 'rival', 'nu_mono')]['headline']:15s} {HEAD[(b, 'outcome')]}")
P("  L4: the floor can single out the rival, never the flat law; a CONSISTENT flat law is the survival of a one-sided bound, not evidence.")

NUM["results"] = {"|".join([k_[0], k_[1], k_[2][0] + "/" + k_[2][1], k_[3], k_[4], k_[5]]): v_ for k_, v_ in RES.items()}
NUM["headlines"] = {"|".join(str(p_) for p_ in k_): v_ for k_, v_ in HEAD.items()}
NUM["external_field"] = {"|".join(k_): v_ for k_, v_ in EFE.items()}
NUM["roman_oliveira"] = {"|".join(k_): v_ for k_, v_ in RO.items()}
NUM["missing_errors_set_to_zero"] = MISSING_ERR
NUM["loaded_columns"] = [dict(file=f, cols=list(c)) for f, c in LOADED]
lb = [c for c in CHECKS if c["load_bearing"]]
nf = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")


def jclean(o):
    if isinstance(o, dict):
        return {str(k_): jclean(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [jclean(v_) for v_ in o]
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(jclean(dict(slug=SLUG, mutate=MUT, summary=dict(n_checks=len(CHECKS), load_bearing_failures=nf,
                                                           failed=[c["name"][:90] for c in CHECKS if not c["ok"]]),
                      checks=CHECKS, numbers=NUM)), builtins.open(os.path.join(LANE, SLUG + "_results.json"), "w"), indent=1)
builtins.open(os.path.join(LANE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
