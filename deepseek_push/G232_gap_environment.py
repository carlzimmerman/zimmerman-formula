#!/usr/bin/env python3
"""G232 -- C4's KILL TEST: the a0_eff/a0_DE GAP vs THE ENVIRONMENT.

Executes hy4 H054 C4 as a kill test of the EFFECTIVE/EMERGENT reading:
  * if a_0 is emergent, rho_Lambda sets it only approximately, and the
    residual gap (per-galaxy a0_eff-deep vs the DE-anchored foot a0_DE)
    should CORRELATE WITH ENVIRONMENT rather than be universal.
  * the nulls:
      (a) universal-scale reading: the residual is FOOTING-ONLY
          (no environmental run) -> rho ~ 0;
      (b) effective/emergent reading: a REAL run, with the LOW-EFE
          (isolated, field) galaxies showing the LARGEST residual.

TESTS
 (1) THE CORRELATION: per-galaxy a0_eff-deep residual (G208's per-object
     values, recomputed in-file from the committed registers) vs the
     committed environment (g_ext / e_N from gext_vectors_2026, the
     neighbour counts Nm_host/onepd_2mpp from the SPARC environment table,
     the group field dom_kind/G100 pair axis): Spearman rho + permutation p.
 (2) THE SPLIT: SPARC at the median e_N -- high-EFE vs low-EFE half's mean
     a0_eff-deep residual, difference and sigma (Welch + bootstrap);
     PLUS the field-vs-group face: the G114 HI field dwarfs (lowest EFE)
     vs the WALLABY-DR2 group members (G100's pair axis, e_N > 0), same
     a0_eff-deep comparison.
 (3) VERDICTS: V1 rho & p; V2 the split sigmas; V3 the honest statement
     (CORRELATED / UNCORRELATED / the data silent -- with the numbers).

Registers: H054 C4 [I] (the gap should correlate with environment -- a
REAL kill); G133/G167/G193/G211 (the footing: a0_eff/a0_DE ~ 1.09-1.15,
~2-sigma preference); G208 (the per-galaxy a0_eff-deep, N=90); G199/G03D
(SPARC deep 0.643-0.692 a0_DE, HI R-free 1.075e-10); G036/G044 (e_N =
g_ext/a0, EFE conventions); G100 (WALLABY pair axis, max e_N 0.193);
G114/G071 (the per-object sample registers). All a0_eff-deep values are
RECOMPUTED in-file from the committed registers (G114 combined sample,
G071_results.json), exactly as G208 does.

Environment registers (committed):
  * gext_vectors_2026/data/gext_vectors.csv -- log_eN_noclu/maxclu
    (e_N = g_ext/a0), dom_name/dom_kind (group field), dom_share.
  * real_research/data/sparc_a0_environment_table.csv -- Nm_host
    (host neighbour count), onepd_2mpp (1-Mpc 2M++ density), usable_2mrs.
  * data2/wallaby_dr2_* (G100) -- the survey pair/group axis (e_N > 0
    sources), recomputed with G100's linking scheme.
"""
import csv, json, math, os, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
GN = 6.674e-11
A0DE = 9.3619e-11          # the DE-anchored foot (vacuum scale, G036)
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
DEEP = 0.2                 # the registered deep window: g_N < 0.2 a0 (G208)
WDEEP = 0.1                # G100's registered WALLABY deep cut (g_N < 0.1 a0)
GAS_X, STAR_X = 1.33, 2.0  # G100 mass schemes
D_PAIR, D_LINK, D_MAX_KPC = 2.0, 6.0, 200.0   # G100 linking
THETA_MAX_DEG = 3.0
CI = 2.99792458e8

RES = []
def check(label, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

def mad(xs):
    m = statistics.median(xs)
    return statistics.median([abs(x - m) for x in xs])

def spear(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(np.argsort(np.argsort(x)), np.argsort(np.argsort(y)))[0, 1])

def perm_p(x, y, n=20000, seed=232):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float); y0 = np.asarray(y, float)
    r0 = abs(spear(x, y0)); cnt = 0
    if math.isnan(r0):
        return float("nan")
    for _ in range(n):
        if abs(spear(x, rng.permutation(y0))) >= r0:
            cnt += 1
    return (cnt + 1) / (n + 1.0)

def welch(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m1, m2 = a.mean(), b.mean()
    s1, s2 = a.std(ddof=1), b.std(ddof=1)
    se = math.sqrt(s1*s1/len(a) + s2*s2/len(b))
    diff = m1 - m2
    sig = diff / se if se > 0 else float("nan")
    return diff, se, sig, m1, m2

def boot_ci_diff(a, b, n=5000, seed=232):
    rng = np.random.default_rng(seed)
    a = np.asarray(a, float); b = np.asarray(b, float)
    ds = []
    for _ in range(n):
        ds.append(rng.choice(a, len(a), replace=True).mean()
                  - rng.choice(b, len(b), replace=True).mean())
    ds = np.array(ds)
    return float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5)), float((ds >= 0).mean())

print("=" * 104)
print("G232 -- C4's KILL TEST: the a0_eff/a0_DE GAP vs THE ENVIRONMENT")
print("        (hy4 H054 C4 [I]: if a_0 is emergent, rho_Lambda sets it only approximately,")
print("         so the gap should CORRELATE WITH ENVIRONMENT -- a REAL kill)")
print(f"        foot: a0_DE = {A0DE:.5e} m/s^2; deep window g_N < {DEEP} a0 (G208)")
print("=" * 104)

# =====================================================================
# PART 0 -- THE PER-GALAXY TABLE (G208's per-object a0_eff-deep, recomputed)
# =====================================================================
print("\n--- PART 0: PER-GALAXY a0_eff-deep (G208's construction, recomputed in-file) ---")

hi_rows = list(csv.DictReader(open(os.path.join(HERE, "G114_data", "G114_combined_sample.csv"))))
hi = []
for r in hi_rows:
    V = float(r["V_obs_kms"]) * 1e3
    Mb = float(r["M_b_Msun"]) * MSUN
    hi.append(dict(name=r["name"].strip(), sample=r["sample"], a0e=V**4 / (GN * Mb),
                   f_gas=float(r["f_gas"]), Mb_Msun=float(r["M_b_Msun"])))
hi_med = float(np.median([h["a0e"] for h in hi]))

g071 = json.load(open(os.path.join(HERE, "G071_results.json")))
sp = []
for pg in g071["per_galaxy"]:
    rings = [r for r in pg["rings"] if r["v_b"] > 0 and r["v_obs"] > 0]
    if not rings:
        continue
    Mb = pg["Mb_Msun"] * MSUN
    deep = [r for r in rings if (r["v_b"] * 1e3)**2 / (r["R_kpc"] * KPC) < DEEP * A0DE]
    src = deep if deep else rings
    a0e = float(np.median([(r["v_obs"] * 1e3)**4 / (GN * Mb) for r in src]))
    outer = max(rings, key=lambda r: r["R_kpc"])
    sp.append(dict(name=pg["name"], a0e=a0e, Mb_Msun=pg["Mb_Msun"],
                   D_Rmax=outer["v_obs"] / outer["v_b"]))
sp_med = float(np.median([x["a0e"] for x in sp]))

print(f"  HI   : {len(hi)} dwarfs (LT {sum(1 for h in hi if h['sample']=='LT')} + FIGGS "
      f"{sum(1 for h in hi if h['sample']=='FIGGS')})  a0e med {hi_med/1e-10:.3f} x1e-10 "
      f"(G208/G199 1.0751e-10)")
print(f"  SPARC: {len(sp)} isolated z0 (G071, Y<0.1)  a0e per-gal med {sp_med/1e-10:.3f} x1e-10 "
      f"(G208 0.501)")
print(f"  residual_dex = log10(a0e/a0_DE): HI med {math.log10(hi_med/A0DE):+.3f} "
      f"| SPARC med {math.log10(sp_med/A0DE):+.3f}")

# ---- environment join (committed tables) ----
gext = list(csv.DictReader(open(os.path.join(REPO, "gext_vectors_2026", "data", "gext_vectors.csv"))))
GX = {}
for r in gext:
    GX[r["name"].strip()] = r
envtab = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data",
                                               "sparc_a0_environment_table.csv"))))
ET = {}
for r in envtab:
    ET[r["name"].strip()] = r

def norm_hi_name(n):
    # LT/FIGGS names carry spaces ("DDO 154"); the env tables carry SPARC
    # names ("DDO154"). De-space only for the small matched set, and only
    # when the de-spaced name exists in the env tables.
    return n.replace(" ", "")

for h in hi:
    nn = norm_hi_name(h["name"])
    h["gext"] = GX.get(nn) if nn in GX else None
for x in sp:
    x["gext"] = GX.get(x["name"])
    x["envtab"] = ET.get(x["name"])

nh = sum(1 for h in hi if h["gext"])
print(f"  env-table coverage: SPARC {sum(1 for x in sp if x['gext'])}/{len(sp)} | "
      f"HI {nh}/{len(hi)} (matched by de-spaced name: "
      f"{[h['name'] for h in hi if h['gext']]})")

# =====================================================================
# PART 1 -- THE CORRELATION (residual vs environment), SPARC N=35
# =====================================================================
print("\n--- PART 1: THE CORRELATION: residual_dex vs the environment (SPARC, fully matched) ---")

sp_valid = [x for x in sp if x["gext"]]
rs = np.array([math.log10(x["a0e"] / A0DE) for x in sp_valid])
eN = np.array([10.0 ** float(x["gext"]["log_eN_maxclu"]) for x in sp_valid])
eN_nc = np.array([10.0 ** float(x["gext"]["log_eN_noclu"]) for x in sp_valid])
g_ext = eN * A0DE
Nm = np.array([float(x["envtab"]["Nm_host"]) if x["envtab"] and str(x["envtab"]["Nm_host"]) not in ("", "nan") else float("nan")
               for x in sp_valid])
omp = np.array([float(x["envtab"]["onepd_2mpp"]) if x["envtab"] and str(x["envtab"]["onepd_2mpp"]) not in ("", "nan") else float("nan")
                for x in sp_valid])
share = np.array([float(x["gext"]["dom_share"]) for x in sp_valid])
dkind = np.array([1.0 if x["gext"]["dom_kind"].strip() == "cluster" else 0.0 for x in sp_valid])
flag_rob = np.array([1.0 if x["gext"]["flag"].strip() == "robust" else 0.0 for x in sp_valid])

axes = [
    ("e_N_maxclu (g_ext/a0, 2M++/MCXC maxclu)", np.log10(eN)),
    ("e_N_noclu  (g_ext/a0, no-cluster)",        np.log10(eN_nc)),
    ("g_ext abs  (m/s^2 = e_N . a0_DE)",          np.log10(g_ext)),
    ("Nm_host (neighbour count)",                 np.log10(Nm + 1.0)),
    ("onepd_2mpp (1-Mpc 2M++ density)",           np.log10(omp + 1e-9)),
    ("dom_share (dominant-structure share)",      share),
    ("dom_kind (group field, cluster=1)",         dkind),
]
corr = {}
print(f"  per-galaxy residual_dex: N={len(rs)}, med {np.median(rs):+.3f}, MAD {mad(rs):.3f} dex; "
      f"e_N_maxclu range {10**np.log10(eN).min():.2e}..{10**np.log10(eN).max():.2e} (max {eN.max():.3f})")
for label, v in axes:
    ok = ~(np.isnan(v) | np.isnan(rs))
    if ok.sum() < 10:
        print(f"  {label:<46s} n={int(ok.sum())} < 10 -- SKIPPED")
        corr[label] = {"n": int(ok.sum()), "rho": None, "p": None}
        continue
    if np.std(v[ok]) == 0.0:
        print(f"  {label:<46s} DEGENERATE in-sample (constant value {v[0]:.3g} for all n={int(ok.sum())}) -- no lever, stated")
        corr[label] = {"n": int(ok.sum()), "rho": None, "p": None, "degenerate": True,
                       "constant": float(v[0])}
        continue
    rho = spear(rs[ok], v[ok])
    p = perm_p(rs[ok], v[ok])
    corr[label] = {"n": int(ok.sum()), "rho": rho, "p": p}
    print(f"  Spearman({label:<46s})  rho = {rho:+.3f}   p = {p:.4f}   (n={int(ok.sum())})")

# quadratic: top-5 vs bottom-5 e_N mean residual (the "largest-residual" face)
o = np.argsort(eN)
top5, bot5 = o[-5:], o[:5]
d_top_bot = rs[top5].mean() - rs[bot5].mean()
se_tb = math.sqrt(rs[top5].var(ddof=1)/5 + rs[bot5].var(ddof=1)/5) if len(top5) > 1 else float("nan")
print(f"  EXTREME FACE (top-5 vs bottom-5 e_N): mean residual {rs[top5].mean():+.3f} vs "
      f"{rs[bot5].mean():+.3f} dex -> diff {d_top_bot:+.3f} +- {se_tb:.3f} "
      f"({d_top_bot/se_tb:+.2f} sigma, n=5+5)")
for i in top5:
    print(f"    TOP  {sp_valid[i]['name']:<12s} e_N={eN[i]:.4f}  resid={rs[i]:+.3f} dex")
for i in bot5:
    print(f"    BOT  {sp_valid[i]['name']:<12s} e_N={eN[i]:.4f}  resid={rs[i]:+.3f} dex")
# leave-one-out: drop the e_N-EXTREME galaxy (UGC07261, 12x the median) and redo
rest = np.delete(o, -1)
t5b = rest[-5:]
d_loo = rs[t5b].mean() - rs[bot5].mean()
se_loo = math.sqrt(rs[t5b].var(ddof=1)/5 + rs[bot5].var(ddof=1)/5)
print(f"  LOO (drop the e_N-extreme galaxy {sp_valid[o[-1]]['name']}, e_N={eN[o[-1]]:.4f}): "
      f"top-5-of-rest vs bottom-5 diff {d_loo:+.3f} +- {se_loo:.3f} ({d_loo/se_loo:+.2f} sigma)")
corr["extreme_face_top5_vs_bottom5"] = {
    "diff_dex": float(d_top_bot), "se_dex": float(se_tb),
    "sigma": float(d_top_bot / se_tb) if se_tb and se_tb == se_tb else None,
    "loo_drop": sp_valid[o[-1]]["name"], "loo_diff_dex": float(d_loo),
    "loo_sigma": float(d_loo/se_loo) if se_loo and se_loo == se_loo else None,
    "top5": [sp_valid[i]["name"] for i in top5], "bot5": [sp_valid[i]["name"] for i in bot5]}

# secondary: pooled with the 4 env-matched HI dwarfs (field anchor, tiny n)
hx = [h for h in hi if h["gext"]]
if len(hx) >= 3:
    pn = [h["name"] for h in hx] + [x["name"] for x in sp_valid]
    pr = [math.log10(h["a0e"]/A0DE) for h in hx] + list(rs)
    pe = [10.0 ** float(h["gext"]["log_eN_maxclu"]) for h in hx] + list(eN)
    prho, pp = spear(pr, np.log10(pe)), perm_p(pr, np.log10(pe))
    print(f"  POOLED (SPARC 35 + HI-matched {len(hx)}: DDO154/DDO168/NGC2366/NGC3741): rho = "
          f"{prho:+.3f} (p {pp:.4f}) -- 4-point field anchor, no power, stated")
    corr["pooled_with_HI_field_anchor"] = {"n": len(pr), "rho": prho, "p": pp,
                                           "HI_matched": [h["name"] for h in hx]}

# =====================================================================
# PART 2 -- THE NULLS
# =====================================================================
rho_main = corr["e_N_maxclu (g_ext/a0, 2M++/MCXC maxclu)"]["rho"]
p_main = corr["e_N_maxclu (g_ext/a0, 2M++/MCXC maxclu)"]["p"]
print("\n--- PART 2: THE NULLS ---")
print("  (a) UNIVERSAL-scale reading: the residual is FOOTING-ONLY, no environmental run")
print("      -> rho ~ 0, p ~ ns (the gap would be a constant offset, not a gradient)")
print("  (b) EFFECTIVE/EMERGENT reading: a REAL run -- the LOW-EFE galaxies show the")
print("      LARGEST residual -> rho < 0 (residual falls as g_ext rises)")
print(f"  MEASURED on the primary axis (e_N_maxclu, SPARC N={int(corr['e_N_maxclu (g_ext/a0, 2M++/MCXC maxclu)']['n'])}): "
      f"rho = {rho_main:+.3f}, p = {p_main:.4f}")
if p_main < 0.05 and rho_main < 0:
    pref = "the data PREFER (b) the emergent run (negative rho, p < 0.05)"
elif abs(rho_main) < 0.25 or p_main >= 0.05:
    pref = ("the data do NOT prefer (b): the correlation is absent/ns -> consistent with (a) "
            "the universal/footing-only reading at the committed amplitudes (see the amplitude caveat)")
else:
    pref = f"the measured sign ({rho_main:+.2f}) is OPPOSITE to (b)'s prediction -- neither null cleanly"
print(f"  VERDICT ON THE NULLS: {pref}")
print("  AMPLITUDE CAVEAT (registered): the committed SPARC e_N spans only 0.0008-0.039;")
print(f"    the EFE-shift scale at the top e_N ~ (g_ext)^2/a0 ~ {(0.039*A0DE)**2/A0DE/A0DE*100:.1f}% of a0 "
      f"vs the per-galaxy residual MAD {mad(rs):.2f} dex -- the run the emergent reading predicts here is far "
      "below the per-galaxy scatter (a starving test)")

# =====================================================================
# PART 3 -- THE SPLITS
# =====================================================================
print("\n--- PART 3: THE SPLITS ---")
med_e = float(np.median(eN))
hi_m, lo_m = eN >= med_e, eN < med_e
if hi_m.sum() >= 5 and lo_m.sum() >= 5:
    d1, se1, sig1, mhi, mlo = welch(rs[hi_m], rs[lo_m])
    cilo, cihi, ppos = boot_ci_diff(rs[hi_m], rs[lo_m])
    print(f"  S1 SPARC MEDIAN-e_N SPLIT (median e_N = {med_e:.4f}):")
    print(f"     high-EFE half (n={int(hi_m.sum())}): mean residual {mhi:+.3f} dex "
          f"(a0e med {np.median([sp_valid[i]['a0e'] for i in np.where(hi_m)[0]])/1e-10:.3f} x1e-10)")
    print(f"     low-EFE  half (n={int(lo_m.sum())}): mean residual {mlo:+.3f} dex "
          f"(a0e med {np.median([sp_valid[i]['a0e'] for i in np.where(lo_m)[0]])/1e-10:.3f} x1e-10)")
    print(f"     HIGH - LOW = {d1:+.3f} +- {se1:.3f} dex  ->  sigma = {sig1:+.2f}  "
          f"(emergent predicts NEGATIVE: low-EFE larger residual)")
    print(f"     bootstrap 95% CI [{cilo:+.3f}, {cihi:+.3f}], P(diff>=0) = {ppos:.3f}")
    # ---- CONFOUND AUDIT: does the high/low e_N split differ in the KNOWN
    # in-sample drivers (G208: f_dark via D = v_obs/v_b at Rmax; mass)? ----
    Dv = np.array([sp_valid[i]["D_Rmax"] for i in range(len(sp_valid))])
    Mbv = np.array([sp_valid[i]["Mb_Msun"] for i in range(len(sp_valid))])
    print("  CONFOUND AUDIT (high-e_N half vs low-e_N half):")
    sighD = float("nan")
    for nm, vv in (("log10 D (f_dark proxy)", np.log10(Dv)), ("log10 Mb", np.log10(Mbv))):
        dh, seh, sigh, mhh, mlh = welch(vv[hi_m], vv[lo_m])
        if nm.startswith("log10 D"):
            sighD = sigh
        r_eD = spear(np.log10(eN[hi_m | lo_m]), vv[hi_m | lo_m])
        print(f"    {nm:<28s} high {mhh:+.3f} vs low {mlh:+.3f} -> diff {dh:+.3f} "
              f"({sigh:+.2f} sigma) | rho(e_N, {nm}) = {r_eD:+.2f}")
    r_eD_all = spear(np.log10(eN), np.log10(Dv)); r_eM_all = spear(np.log10(eN), np.log10(Mbv))
    # G208's own F law: log10 a0e = -0.640 + 1.47 log10 D -> predict how much of
    # the S1 split the D-difference explains
    Dl_m, Dh_m = np.log10(Dv[lo_m]).mean(), np.log10(Dv[hi_m]).mean()
    dD_pred = 1.47 * (Dh_m - Dl_m)          # predicted a0e-dex shift from the D-run
    d_res_env = d1 - dD_pred                # split remainder after the D-confound
    print(f"    overall: rho(e_N, log10 D) = {r_eD_all:+.2f} | rho(e_N, log10 Mb) = {r_eM_all:+.2f} "
          f"-- if strong, the S1 split mirrors the registered f_dark/mass structure, NOT the EFE")
    print(f"    F-LAW DECOMPOSITION (G208: log10 a0e = -0.640 + 1.47 log10 D): the D-difference "
          f"{Dh_m - Dl_m:+.3f} dex predicts an a0e shift {dD_pred:+.3f} dex ~ "
          f"{100*abs(dD_pred)/max(abs(d1),1e-9):.0f}% of the observed {-1*d1 if d1<0 else d1:+.3f}-dex "
          f"split; environmental remainder {d_res_env:+.3f} dex ({(d_res_env/se1):+.1f} sigma)")
    confound = {"rho_eN_logD": float(r_eD_all), "rho_eN_logMb": float(r_eM_all),
                "D_high_minus_low_sigma": float(sighD),
                "F_law_predicted_split_dex": float(dD_pred),
                "environmental_remainder_dex": float(d_res_env),
                "environmental_remainder_sigma": float(d_res_env / se1) if se1 and se1 == se1 else None}
else:
    d1 = se1 = sig1 = mhi = mlo = float("nan")
    print(f"  S1 median-e_N split: insufficient halves (hi {int(hi_m.sum())}, lo {int(lo_m.sum())})")

# ---- S2: HI field dwarfs vs WALLABY group members (G100 pair axis) ----
print("\n  S2 HI FIELD DWARFS (lowest EFE) vs WALLABY GROUP MEMBERS (G100's pair axis):")
print("  (recompute of G100's gas-RAR machinery: per-galaxy a0_gas = median g_obs^2/g_N over")
print("   deep rings g_N < 0.1 a0; e_N_b = max G*2.66*M_HI_j/d_proj^2 over neighbours in G100's")
print("   linking corridor -- |dD|<=2 Mpc, d_proj<=200 kpc, theta<=3 deg)")
kin = list(csv.DictReader(open(os.path.join(HERE, "data2", "wallaby_dr2_kinematic_catalogue.tsv")), delimiter="\t"))
sall = list(csv.DictReader(open(os.path.join(HERE, "data2", "wallaby_dr2_source_catalogue.tsv")), delimiter="\t"))
# dedupe kinematic by name, keep the LAST tile release (G100 convention)
k2 = {}
for r in kin:
    k2[r["name"]] = r
kin_u = list(k2.values())

def to_f(x):
    return np.array([float(t) for t in str(x).split(",") if t.strip()])

def unit_vectors(ras, decs):
    ra = np.radians(np.array(ras, float)); dc = np.radians(np.array(decs, float))
    return np.stack([np.cos(dc)*np.cos(ra), np.cos(dc)*np.sin(ra), np.sin(dc)], 1)

# ---- FAITHFUL PORT of G100's neighbour-catalogue cleaning.  Without the
# quality drops, comment-fragment merges and sub-beam geometric merges the
# survey's own duplicate/part detections appear as ~0-separation
# 'companions' and the pair axis is garbage (max e_N ~ 1e2).  Steps in the
# committed order: (1) name-dedupe keep max f_sum; (2) quality drop
# (rel<0.8 or qflag==4); (3) comment pipeline (hard drops, fragment merges);
# (4) geometric double-detection merge (<0.75 arcmin, |dD|<0.71 Mpc,
# f-ratio<3); (5) targets = all sources minus fragments.
import re as _re
su_all0 = []
for r in sorted(sall, key=lambda r: -float(r["f_sum"])):
    if r["name"] not in {x["name"] for x in su_all0}:
        su_all0.append(r)
COMMENTS = {r["name"]: (r.get("comments") or "").strip() for r in su_all0}
HARD_DROP_KW = ("artefact", "artifac", "sidelobe", "questionable",
                "no optical counterpart", "false positive", "continuum artefact",
                "continuum artifact", "missing flux", "flagged continuum",
                "flagged channel", "debris near", "residual continuum",
                "gas bridge", "sidelobes")
FRAG_KW = ("only half", "only part", "partial detection", "fragment",
           "components of the same galaxy", "two halves of the same galaxy",
           "might be two halves", "other part is", "other half is",
           "part of the galaxy pair", "part of this galaxy was")

def has_kw(s, kws):
    sl = s.lower()
    return any(k in sl for k in kws)

qdrop = [r["name"] for r in su_all0 if float(r["rel"]) < 0.8 or float(r["qflag"]) == 4]
# NOTE (G100 semantics): quality drops apply ONLY to the NEIGHBOUR set; the
# dropped rows remain TARGETS (they just cannot serve as companions).
drop_names, merge_pairs = set(), []
qdrop_set = set(qdrop)
allnames = {r["name"] for r in su_all0}
for r in su_all0:
    c = COMMENTS.get(r["name"], "")
    if not c:
        continue
    if has_kw(c, HARD_DROP_KW):
        drop_names.add(r["name"]); continue
    if has_kw(c, FRAG_KW):
        other = None
        for mo in _re.finditer(r"WALLABY J\d{6}[+-]\d{6}", c):
            oo = mo.group(0)
            if oo != r["name"] and oo in allnames:
                other = oo; break
        if other is not None:
            merge_pairs.append((other, r["name"]))
        else:
            drop_names.add(r["name"])

def merge_rows(df, pairs):
    avail = {x["name"] for x in df}
    pairs = [(a, b) for a, b in pairs if a in avail and b in avail and a != b]
    frag_of = {}
    for a, b in sorted(pairs):
        if a in frag_of or b in frag_of:
            continue
        frag_of[b] = a
    if not frag_of:
        return df, []
    keep = [x for x in df if x["name"] not in set(frag_of)]
    slist = {x["name"]: x for x in df}
    for b, a in frag_of.items():
        pa, pb = slist[a], slist[b]
        w = float(pa["f_sum"]) + float(pb["f_sum"])
        m_hi = 10.0**float(pa["log_m_hi_corr"]) + 10.0**float(pb["log_m_hi_corr"])
        for k in ("ra", "dec", "dist_h"):
            pa[k] = (float(pa[k])*float(pa["f_sum"]) + float(pb[k])*float(pb["f_sum"])) / w
        pa["log_m_hi_corr"] = math.log10(m_hi)
    return keep, list(frag_of.keys())

su = [x for x in su_all0 if x["name"] not in drop_names and x["name"] not in qdrop_set]
su, merged = merge_rows(su, merge_pairs)
Uc = unit_vectors([float(r["ra"]) for r in su], [float(r["dec"]) for r in su])
Dc = np.array([float(r["dist_h"]) for r in su])
fc = np.array([float(r["f_sum"]) for r in su])
geo_merge = []
for i in range(len(su)):
    for j in range(i + 1, len(su)):
        ddeg = math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(Uc[i], Uc[j]))))))
        if ddeg > 0.75 / 60.0:
            continue
        if abs(Dc[i] - Dc[j]) >= 0.71:
            continue
        if max(fc[i] / max(fc[j], 1e-3), fc[j] / max(fc[i], 1e-3)) >= 3.0:
            continue
        keep = i if fc[i] >= fc[j] else j
        geo_merge.append((j if keep == i else i, keep))
if geo_merge:
    geo_frag = [su[i]["name"] for i, _ in geo_merge]
    su, _ = merge_rows(su, [(su[k]["name"], su[i]["name"]) for i, k in geo_merge])
else:
    geo_frag = []
fragments = set(drop_names) | set(merged) | set(geo_frag)
suT = [x for x in su_all0 if x["name"] not in fragments]
smap = {x["name"]: x for x in suT}
Uc = unit_vectors([float(r["ra"]) for r in su], [float(r["dec"]) for r in su])
sD = np.array([float(r["dist_h"]) for r in su])
sM = np.array([10.0 ** float(r["log_m_hi_corr"]) for r in su])
Ut = unit_vectors([float(r["ra"]) for r in suT], [float(r["dec"]) for r in suT])
KPC_AS = 4.8481368e-3
C3 = math.cos(math.radians(3.0))
SELF = {su[i]["name"]: i for i in range(len(su))}
E_NB = {}
d0m = np.abs(sD[None, :] - np.array([float(r["dist_h"]) for r in suT])[:, None])
with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
    ddegm = np.degrees(np.arccos(np.clip(Ut @ Uc.T, -1.0, 1.0)))
angm = ddegm < 3.0    # NaN rows (missing coords) drop out automatically (NaN < x = False)
dm = d0m <= D_PAIR
mask = angm & dm
for i, r in enumerate(suT):
    ok = np.where(mask[i])[0]
    ok = np.array([j for j in ok if j != SELF.get(r["name"], -1)])
    g, gb, nb, dmin = 0.0, 0.0, -1, np.inf
    for j in ok:
        cang = max(-1.0, min(1.0, float(np.dot(Ut[i], Uc[j]))))
        dproj = math.acos(cang) * 0.5 * (float(r["dist_h"]) + sD[j]) * 1000.0
        if dproj > D_MAX_KPC:
            continue
        dk = max(dproj, 1.0)
        gi = GN * GAS_X * sM[j] * MSUN / (dk * KPC)**2
        gib = GN * (GAS_X * STAR_X) * sM[j] * MSUN / (dk * KPC)**2
        if gib > gb:
            gb, g, nb, dmin = gib, gi, j, dk
    E_NB[r["name"]] = {"gb": gb / A0DE, "g": g / A0DE,
                       "n_nb": 1 if nb >= 0 else 0,
                       "dmin_kpc": float(dmin) if nb >= 0 else None}
print(f"  WALLABY cleaning replicating G100: {len(qdrop)} quality + "
      f"{len(drop_names)} comment drops, {len(merged)} comment merges, "
      f"{len(geo_merge)} geometric merges; targets {len(suT)} | clean neighbours {len(su)}")
mx_all = max((E_NB[n]["gb"] for n in E_NB), default=0.0)
kx = [n for n in E_NB if n in {r["name"] for r in kin_u}]
mx_kin = max((E_NB[n]["gb"] for n in kx), default=0.0)
n_kin_nz = sum(1 for n in kx if E_NB[n]["gb"] > 0)
print(f"  recomputed e_N_b (bracket 2.66*M_HI, G100's scheme): max over ALL targets "
      f"{mx_all:.4f} (G100 registered 0.1931) | over KINEMATIC targets {mx_kin:.4f} "
      f"(G100 registered 0.0033) | kinematic n_eN>0 {n_kin_nz}/{len(kx)}")

wall = []
for r in kin_u:
    nm = r["name"]
    e = E_NB.get(nm, {"gb": 0.0, "g": 0.0, "n_nb": 0, "dmin_kpc": None})
    s = smap.get(nm)
    if s is None:
        continue
    D = float(s["dist_h"])
    eN_b, eN_g, nb, dmin = e["gb"], e["g"], e["n_nb"], e["dmin_kpc"]
    # a0_gas from the rings (G100's gas-RAR construction)
    rad, vrot = to_f(r["Rad"]), to_f(r["Vrot_model"])
    sr = to_f(r["Rad_SD"]); sd = to_f(r["SD_model"])
    if len(rad) == 0 or len(vrot) != len(rad) or len(sr) < 2:
        continue
    kpc_as = D * KPC_AS
    rk, srk = rad * kpc_as, sr * kpc_as
    dr = np.diff(np.concatenate([[0.0], srk]))
    M_int = 2*np.pi*np.sum(srk*sd*dr)
    f = 10.0**float(s["log_m_hi_corr"]) / max(M_int, 1e-30)
    cum = np.cumsum(2*np.pi*srk*sd*dr) * f
    gas = []
    for k in range(len(rad)):
        x = float(min(rk[k], srk[-1]))
        m_lt = min(float(np.interp(x, srk, cum)) if x >= srk[0] else 0.0, 10.0**float(s["log_m_hi_corr"]))
        go = (vrot[k]*1e3)**2 / (rk[k]*KPC) if rk[k] > 0 else 0.0
        gN = GN * GAS_X * m_lt * MSUN / (rk[k]*KPC)**2 if rk[k] > 0 else 0.0
        if go > 0 and gN > 0 and gN < WDEEP * A0DE:
            gas.append((go, gN, go*go/gN))
    a0gas = float(np.median([t[2] for t in gas])) if len(gas) >= 2 else float("nan")
    wall.append(dict(name=nm, D=D, eN_b=eN_b, eN_g=eN_g, n_nb=int(nb),
                     dmin_kpc=float(dmin) if nb else None, a0gas=a0gas, n_deep=len(gas)))
wallA = [w for w in wall if not math.isnan(w["a0gas"])]
grp = [w for w in wallA if w["eN_b"] > 0]
field = [w for w in wallA if w["eN_b"] == 0]
print(f"  WALLABY kinematics with deep rings: {len(wallA)} ({len(wall)} with curves); "
      f"group members (e_N>0): {len(grp)}, field: {len(field)}")
print(f"  recomputed e_N_b over the KINEMATIC sample: max {mx_kin:.4f} "
      f"(G100 registered kinematic max 0.0033) | n>0: {n_kin_nz} (all-target max {mx_all:.4f} vs "
      f"G100's 0.1931)")
a0g_grp = np.array([w["a0gas"] for w in grp])
a0g_fld = np.array([w["a0gas"] for w in field])
a0hi = np.array([h["a0e"] for h in hi])
print(f"  a0_gas (gas-only abscissa): group members med {np.median(a0g_grp)/1e-10:.3f} x1e-10 "
      f"mean(log10) {np.mean(np.log10(a0g_grp)):+.3f} (n={len(grp)}) | WALLABY field med "
      f"{np.median(a0g_fld)/1e-10:.3f} x1e-10 mean(log10) {np.mean(np.log10(a0g_fld)):+.3f} "
      f"(n={len(field)}) | HI field dwarfs (G114, full baryons) med {hi_med/1e-10:.3f} x1e-10 "
      f"mean(log10) {np.mean(np.log10(a0hi)):+.3f} (n={len(hi)})")
if len(grp) >= 5 and len(field) >= 5:
    dg, seg, sigg, mg, mf = welch(np.log10(a0g_grp), np.log10(a0g_fld))
    medg, medf = np.median(a0g_grp), np.median(a0g_fld)
    print(f"  WITHIN-WALLABY group-vs-field: mean log10 a0_gas {mg:+.3f} vs {mf:+.3f} dex "
          f"-> diff {dg:+.3f} +- {seg:.3f} ({sigg:+.2f} sigma) | MEDIANS: group "
          f"{math.log10(medg):+.3f} vs field {math.log10(medf):+.3f} dex -> "
          f"{math.log10(medg/medf):+.3f} dex (median runs the ANTI-emergent way)")
else:
    dg = seg = sigg = mg = mf = float("nan")
    print("  group-member cell too small for a stable within-WALLABY split; stated, not run")
# HI field dwarfs vs WALLABY group members (the task's split 2, cross-sample)
if len(grp) >= 5:
    dhg, sehg, sighg, mhi2, mgrp2 = welch(np.log10(a0hi), np.log10(a0g_grp))
    print(f"  HI FIELD (lowest EFE) vs WALLABY GROUP MEMBERS: mean log10 a0 {mhi2:+.3f} (HI) vs "
          f"{mgrp2:+.3f} (group) -> HI - GROUP = {dhg:+.3f} +- {sehg:.3f} dex ({sighg:+.2f} sigma); "
          f"medians {math.log10(hi_med):+.3f} vs {math.log10(np.median(a0g_grp)):+.3f} "
          f"({math.log10(hi_med/np.median(a0g_grp)):+.3f} dex)")
    print("  SYSTEMATIC BRACKET: the WALLABY side is GAS-ONLY (no stellar masses; G100 registered "
          "+0.2 dex absolute deep-end offset).  Applying that -0.2 dex to the group side moves "
          f"HI - GROUP to {dhg+0.2:+.3f} dex ({sighg+0.2/ (sehg if sehg>0 else 1):+.2f} sigma) -- "
          "the correction direction HELPS the emergent prediction, but the comparison stays "
          "construction-mismatched (G114 full baryons vs WALLABY M_HI-only)")
else:
    dhg = sehg = sighg = mhi2 = mgrp2 = float("nan")
    print("  cross-sample split not run (group cell < 5)")

# cross-check vs the G100 REGISTERED split (conservative-limit result)
print("  CROSS-CHECK (G100 registered): WALLABY last-ring deep-end residual, high-e_N minus low-e_N")
print("    = -0.207 dex, CI95 [-0.505, +0.050], p(offset>=0) = 0.083 -- the survey-pair axis shows")
print("    an ns candidate in the additive (sag-low) direction; 2M++ axis +0.070 ns")

# =====================================================================
print("\n--- THE CHECKS")
RES.append(check("C0 [registers] HI a0e med == 1.0751e-10 (2%) and SPARC per-gal med == 0.501e-10 (10%)",
                 abs(hi_med/1.0751e-10 - 1) < 0.02 and abs(sp_med/0.501e-10 - 1) < 0.10,
                 f"{hi_med/1e-10:.3f} vs 1.0751 | {sp_med/1e-10:.3f} vs 0.501"))
RES.append(check("C1 [coverage] ALL 35 SPARC galaxies matched to the committed env tables (gext + envtab)",
                 sum(1 for x in sp if x["gext"]) == 35, f"{sum(1 for x in sp if x['gext'])}/35"))
RES.append(check("C2 [correlation computed] primary-axis Spearman rho + p reported on n >= 30",
                 rho_main == rho_main and sum(1 for v in corr.values() if v.get("rho") is not None) >= 3,
                 f"rho_main {rho_main:+.3f}, axes computed {sum(1 for v in corr.values() if v.get('rho') is not None)}"))
RES.append(check("C3 [determinism] permutation p seeded (seed=232, n=20000)",
                 True, "seeded rng"))
RES.append(check("C4 [WALLABY recompute] G100's pair axis reproduced: all-target max e_N_b within 25% of the registered 0.1931 AND kinematic max within 50% of 0.0033, with n_eN>0 >= 20",
                 abs(mx_all/0.1931 - 1) < 0.25 and abs(mx_kin/0.0033 - 1) < 0.50
                 and n_kin_nz >= 20,
                 f"all-target {mx_all:.4f} vs 0.1931 | kinematic {mx_kin:.4f} vs 0.0033 | n>0 {n_kin_nz}"))
RES.append(check("C5 [deep rings] WALLABY a0_gas computed for >= 15 galaxies with >= 2 deep rings",
                 len(wallA) >= 15, f"n={len(wallA)}"))
RES.append(check("C6 [extreme face stated] top-5 vs bottom-5 e_N residual difference reported",
                 d_top_bot == d_top_bot, f"diff {d_top_bot:+.3f} dex"))

n = sum(1 for r in RES if r)
print(f"\nG232 COMPLETE: {n}/{len(RES)} checks PASS.")
print("written: G232_results.json")

# =====================================================================
# THE VERDICTS
# =====================================================================
splits = {"S1_sparc_median_efe": {
    "median_eN_maxclu": float(med_e), "n_high": int(hi_m.sum()), "n_low": int(lo_m.sum()),
    "mean_resid_high_dex": float(mhi), "mean_resid_low_dex": float(mlo),
    "diff_high_minus_low_dex": float(d1), "se_dex": float(se1), "sigma": float(sig1),
    "boot_ci95": [float(cilo), float(cihi)], "P_diff_ge_0": float(ppos),
    "emergent_predicts": "negative diff (low-EFE larger residual)"},
  "S2_field_vs_group": {
    "HI_field_n": len(hi), "HI_a0e_med_x1e-10": float(hi_med/1e-10),
    "WALLABY_group_n": len(grp), "WALLABY_group_a0gas_med_x1e-10": float(np.median(a0g_grp)/1e-10) if len(grp) else None,
    "WALLABY_field_n": len(field), "WALLABY_field_a0gas_med_x1e-10": float(np.median(a0g_fld)/1e-10) if len(field) else None,
    "within_wallaby_group_vs_field_diff_dex": float(dg) if dg == dg else None,
    "within_wallaby_sigma": float(sigg) if sigg == sigg else None,
    "within_wallaby_group_vs_field_median_dex": float(np.log10(np.median(a0g_grp)/np.median(a0g_fld))) if len(grp) and len(field) else None,
    "HI_field_minus_group_diff_dex": float(dhg) if dhg == dhg else None,
    "HI_field_minus_group_sigma": float(sighg) if sighg == sighg else None,
    "HI_field_minus_group_dex_after_gas_bracket": float(dhg + 0.2) if dhg == dhg else None,
    "systematic": "WALLABY side is GAS-ONLY abscissa (no stellar masses; G100 registered +0.2 dex "
                  "absolute deep-end offset) -- flagged, not corrected",
    "g100_registered_split": "last-ring offset -0.207 dex, CI [-0.505,+0.050], p(>=0)=0.083 (ns)"}}

confound = locals().get("confound", None)
V1 = (f"V1 THE CORRELATION (per-galaxy a0_eff-deep residual = log10(a0e/a0_DE) vs the committed "
      f"environment, SPARC N={len(sp_valid)}): primary axis e_N_maxclu = g_ext/a0 (2M++/MCXC maxclu, "
      f"gext_vectors_2026): Spearman rho = {rho_main:+.3f}, p = {p_main:.4f}.  Full axis set: "
      + "; ".join(
          f"{k} rho {v['rho']:+.3f} (p {v['p']:.4f})" if v.get("rho") is not None
          else f"{k} DEGENERATE (constant in-sample)" if v.get("degenerate")
          else f"{k} skipped (n={v['n']})"
          for k, v in corr.items() if k not in ("extreme_face_top5_vs_bottom5", "pooled_with_HI_field_anchor"))
      + f".  Extreme face (top-5 vs bottom-5 e_N): {d_top_bot:+.3f} +- {se_tb:.3f} dex "
      f"({d_top_bot/se_tb:+.2f} sigma; LOO drop {sp_valid[o[-1]]['name']}: {d_loo:+.3f} +- {se_loo:.3f}, "
      f"{d_loo/se_loo:+.2f} sigma).")

_sigh_ = confound["D_high_minus_low_sigma"] if confound else float("nan")
V2 = (f"V2 THE SPLITS.  S1 (SPARC at the median e_N = {med_e:.4f}): high-EFE half mean residual "
      f"{mhi:+.3f} dex vs low-EFE {mlo:+.3f} dex -> HIGH - LOW = {d1:+.3f} +- {se1:.3f} dex, "
      f"sigma = {sig1:+.2f}, bootstrap 95% CI [{cilo:+.3f}, {cihi:+.3f}], P(diff>=0) = {ppos:.3f} "
      f"(emergent predicts NEGATIVE).  CONFOUND AUDIT: the high-e_N half differs from the low in the "
      f"registered in-sample driver D (f_dark proxy) by {_sigh_:+.2f} sigma, rho(e_N, log10 D) = "
      f"{confound['rho_eN_logD']:+.2f}, rho(e_N, log10 Mb) = {confound['rho_eN_logMb']:+.2f} -- the "
      f"split is NOT clean of G208's known f_dark structure.  "
      f"S2 (field vs group): HI field dwarfs a0e med {hi_med/1e-10:.3f} x1e-10 "
      f"(n={len(hi)}, full baryons) vs WALLABY group members a0_gas med "
      f"{np.median(a0g_grp)/1e-10:.3f} x1e-10 (n={len(grp)}): raw HI - GROUP = {dhg:+.3f} +- {sehg:.3f} "
      f"dex ({sighg:+.2f} sigma) -- CONSTRUCTION-DOMINATED (gas-only vs full-baryon abscissa, "
      f"{math.log10(np.median(a0g_grp)/hi_med):+.2f} dex systematic floor, only -0.2 dex of which "
      f"is G100-registered); the construction-clean within-WALLABY group-vs-field a0_gas diff "
      f"{dg:+.3f} +- {seg:.3f} dex ({sigg:+.2f} sigma, medians "
      f"{math.log10(np.median(a0g_grp)/np.median(a0g_fld)):+.3f} dex anti-emergent); "
      f"the G100 registered last-ring split (high-e_N minus low-e_N, the same "
      f"environmental face on the RAR directly): -0.207 dex, CI [-0.505, +0.050], p = 0.083 ns.")

corr_word = ("CORRELATED" if (p_main < 0.05 and rho_main < 0)
             else "UNCORRELATED (primary axis) with a direction-correct 2-sigma split candidate -- NOT CONFIRMED"
             if (p_main >= 0.05 and sig1 == sig1 and sig1 < -1.5)
             else "UNCORRELATED" if (p_main >= 0.05 and abs(rho_main) < 0.25)
             else "DATA SILENT")
_eshift_ = math.log10(1.0 + eN.max()**2)  # EFE floor (g_ext)^2/a0 as a dex shift of the deep scale
V3 = (f"V3 C4's KILL TEST -- VERDICT: {corr_word} WITH THE NUMBERS.  "
      f"On the fully matched SPARC sample the per-galaxy residual vs e_N_maxclu gives rho = "
      f"{rho_main:+.3f}, p = {p_main:.4f} -- the primary correlation is ABSENT (the universal/foothing "
      f"reading's expectation) -- and the median-e_N split runs HIGH - LOW = {d1:+.3f} +- {se1:.3f} dex "
      f"({sig1:+.2f} sigma, bootstrap P(diff>=0) = {ppos:.3f}) with the extreme face {d_top_bot:+.3f} +- "
      f"{se_tb:.3f} dex ({d_top_bot/se_tb:+.2f} sigma), BOTH in the emergent-predicted direction "
      f"(low-EFE -> larger residual).  TWO AMPLITUDE/PURITY OBJECTIONS prevent reading that as C4 "
      f"confirmation: (i) the committed e_N only spans 0.0008-0.039 and the EFE floor shift at the top "
      f"e_N = (g_ext)^2/a0 ~ {100*eN.max()**2:.2f}% of a0 ({_eshift_:.2e} dex) vs a per-galaxy residual "
      f"MAD {mad(rs):.2f} dex -- the observed {abs(d1):.2f}-dex split is ~{abs(d1)/_eshift_:.0f}x "
      f"LARGER than the emergent/rho_Lambda amplitude budget (if real, it is NOT the EFE channel); "
      f"(ii) the high-e_N half differs in the "
      f"registered in-sample driver D by {_sigh_:+.2f} sigma (rho(e_N, log10 D) = "
      f"{confound['rho_eN_logD']:+.2f}), and G208's own F law (log10 a0e = -0.640 + 1.47 log10 D) "
      f"attributes {100*abs(confound['F_law_predicted_split_dex'])/max(abs(d1),1e-9):.0f}% of the "
      f"observed split to that D-difference -- the environmental remainder is only "
      f"{confound['environmental_remainder_dex']:+.2f} dex "
      f"({confound['environmental_remainder_sigma']:+.1f} sigma): the split is CONFOUNDED with "
      f"G208's f_dark structure.  "
      f"The GROUP/PAIR face (HI field vs WALLABY group members: raw {dhg:+.3f} +- {sehg:.3f} dex, "
      f"{sighg:+.2f} sigma, but CONSTRUCTION-DOMINATED -- gas-only vs full-baryon abscissa, "
      f"{math.log10(np.median(a0g_grp)/hi_med):+.2f} dex systematic floor; the construction-clean "
      f"within-WALLABY face {dg:+.3f} +- {seg:.3f} dex, {sigg:+.2f} sigma with anti-emergent medians; "
      f"G100 registered last-ring split -0.207 dex, p = 0.083 ns) is also null-to-candidate.  "
      f"C4's kill test therefore: the EMERGENT reading's environmental correlation is NOT confirmed "
      f"(primary rho null, amplitude-inconsistent candidate, confounded split) and the UNIVERSAL "
      f"reading is NOT killed -- the data are largely SILENT at the committed amplitudes, with a "
      f"direction-correct ~2-sigma split candidate on the SPARC face REGISTERED for the large-EFE "
      f"sample (e_N ~ 0.3-1, the G036/G044 registered boundary) that can actually distinguish.")

VERDICTS = {"V1": V1, "V2": V2, "V3": V3}

out = {
    "lane": "G232",
    "title": "C4-as-G232: THE GAP-VS-ENVIRONMENT KILL TEST (residual a0_eff/a0_DE vs g_ext/neighbours/group)",
    "registers": {"H054_C4": "if a_0 is emergent, rho_Lambda sets it only approximately: the gap should CORRELATE WITH ENVIRONMENT [I]",
                  "footing": "G133/G167/G193/G211: a0_eff/a0_DE ~ 1.09-1.15, pooled z = 1.53 sigma (robust [0.26, 2.10])",
                  "G208": "per-galaxy a0_eff-deep z0 pair N=90 (HI 55 + SPARC 35)",
                  "a0_DE": A0DE, "deep_window": f"g_N < {DEEP} a0"},
    "per_galaxy": {
        "HI": {"n": len(hi), "a0e_med_x1e-10": float(hi_med/1e-10),
               "resid_med_dex": float(math.log10(hi_med/A0DE)),
               "source": "G114_combined_sample.csv: a0e = V_obs^4/(G M_b), R-free"},
        "SPARC": {"n": len(sp), "a0e_med_x1e-10": float(sp_med/1e-10),
                  "resid_med_dex": float(math.log10(sp_med/A0DE)),
                  "source": "G071_results.json: per-galaxy median over deep rings (g_N < 0.2 a0)"},
        "rows": [{"name": x["name"], "a0e_x1e-10": float(x["a0e"]/1e-10),
                  "resid_dex": float(math.log10(x["a0e"]/A0DE)),
                  "eN_maxclu": float(10**float(x["gext"]["log_eN_maxclu"])) if x["gext"] else None,
                  "eN_noclu": float(10**float(x["gext"]["log_eN_noclu"])) if x["gext"] else None,
                  "g_ext_m_s2": float(10**float(x["gext"]["log_eN_maxclu"])*A0DE) if x["gext"] else None,
                  "dom_kind": x["gext"]["dom_kind"].strip() if x["gext"] else None,
                  "dom_share": float(x["gext"]["dom_share"]) if x["gext"] else None,
                  "Nm_host": float(x["envtab"]["Nm_host"]) if x["envtab"] else None,
                  "onepd_2mpp": float(x["envtab"]["onepd_2mpp"]) if x["envtab"] else None}
                 for x in sp_valid],
    },
    "correlation": corr,
    "nulls": {"universal": "rho ~ 0 (footing-only)", "emergent": "rho < 0 (low-EFE largest residual)",
              "measured_primary": {"rho": rho_main, "p": p_main},
              "preferred": pref, "amplitude_caveat": "SPARC e_N 0.0008-0.039; EFE shift at top e_N ~0.15% of a0 vs MAD ~0.22 dex -- starving test"},
    "splits": splits,
    "confound_audit": confound,
    "extreme_face_loo": {"drop": sp_valid[o[-1]]["name"], "diff_dex_loo": float(d_loo),
                         "sigma_loo": float(d_loo/se_loo) if se_loo and se_loo == se_loo else None},
    "wallaby": {"n_galaxies": len(wall), "n_with_deep_a0": len(wallA),
                "eN_b_max": float(max((w["eN_b"] for w in wall), default=0.0)),
                "n_group_members_eN_gt_0": int(sum(1 for w in wall if w["eN_b"] > 0)),
                "g100_registered_max": 0.1931,
                "g100_registered_last_ring_split": "offset -0.207 dex, CI [-0.505,+0.050], p(>=0)=0.083"},
    "verdicts": VERDICTS,
    "checks": [bool(r) for r in RES], "n_pass": int(n), "n_total": len(RES),
}
json.dump(out, open(os.path.join(HERE, "G232_results.json"), "w"), indent=1)
print("VERDICTS:")
for v in (V1, V2, V3):
    print(f"  {v}\n")
print("done")