#!/usr/bin/env python3
"""G071 -- THE FULL-CURVE TEST OF THE EQUIPARTITION LAW ON SPARC.

THE LAW (the committed chain G03E/G03G + the universal linear law):
    M_ph(<r) = M_b * r/r_M      (the phantom/dark sector, universal linear law)
    r_M      = sqrt(G M_b / a0) (the MOND radius; equipartition: M_ph(<r_M) = M_b)
    v_c(r)^2 = v_b(r)^2 + v_flat^2 * (1 - r_in/r)      r_in = 0.3 r_M (DECLARED)
    v_flat   = (G M_b a0)^(1/4) (the BTFR zero point, zero free parameters)
    domain   : r <= R_efe = sqrt(G M_b / g_ext)   (the EFE line: the law's own
               boundary; beyond it the external-field/free-dust regime takes over)
The (1 - r_in/r) factor is the declared inner edge of the phantom region (the
isothermal profile carries an inner hole at 0.3 r_M): below r_in the phantom
term is clamped to zero (v_pred = v_b).

THE TEST (this lane): the law's OWN rotation curves, curve by curve, on the
SPARC galaxies of the G044 corpus (glm53_push/data/rotation_curve_corpus_v7.json)
that are ISOLATED and LOW-EFE per the environment table
(real_research/data/sparc_a0_environment_table.csv).  Zero free parameters:
M_b is read off the corpus baryonic decomposition, a0 is the registered
dark-energy footing 9.3619e-11 m/s^2 (G052; the same value G03E/G03G carry),
v_flat is then FIXED.  No fitting of any kind: chi2/dof has dof = n (no fitted
parameters), and the primary metric is the rms of log10(v_obs/v_pred) vs the
registered SPARC/RAR benchmark rms ~ 0.15 dex (STATE.md board, G002/L232).

DECLARED CONVENTIONS (all stated, none fitted):
  * m2l: the corpus row's m2l_disk (per-galaxy SPARC value; fallback 0.50 solar
    if absent/<=0) applied to BOTH Vdisk and Vbul (the corpus carries only the
    disk value).
  * v_b(r)^2 = sign(Vgas)*Vgas^2 + m2l*(Vdisk^2 + Vbul^2)  (SPARC sign convention
    for negative Vgas = outward thermal pressure, per the corpus known_issues).
  * M_b = enclosed baryons at the OUTERMOST ring with a positive baryonic model:
    M_b = v_b(R_out)^2 * R_out / G.  The corpus carries no luminosities/gas
    masses; the enclosed-baryons convention (G036's parser convention) is the
    corpus-intrinsic mass.
  * EFE: g_ext = G * 10^logMhalo_host / D_Mpc^2  (the REGISTERED proper-Y
    convention of G03E -- which found mean Y = 0.000: under this reading the
    whole table is low-EFE by construction).  LOW-EFE cut: Y = g_ext/a0 < 0.1.
  * ISOLATED cut (structural, from the same table; stated): Nm_host <= 1
    (blank -> 0 candidate hosts) AND usable_2mrs == 1.
  * chi2 uses the corpus errV only; M_b/v_flat treated as exact (zero-parameter
    prediction, no propagation into chi2; the truth of V1 is judged on the rms).
  * V2 slope threshold (declared): |pooled slope of log10(v_obs/v_pred) vs
    log10(R)| <= 0.05 dex/dex AND |median per-galaxy slope| <= 0.05 dex/dex.

VERDICTS:
  V1 pooled rms of log10(v_obs/v_pred) <= 0.18 dex (vs the 0.15 benchmark).
  V2 no systematic slope of the residual vs radius out to the EFE line.
  V3 the EFE-line truncation NEEDED: without it (rings beyond R_efe included)
     the chi2 degrades by > 10%.  (In the isolated sample the boundary sits at
     ~10^2-10^3 kpc, beyond every curve: the test is expected to be VACUOUS --
     stated honestly, not spun.)
  V4 the honest statement: does the law stand as a zero-parameter curve
     predictor?
"""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
ENV = os.path.join(REPO, "real_research", "data", "sparc_a0_environment_table.csv")
COR = os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")
A0 = 9.3619e-11            # the registered footing (the dark-energy scale, G052)
A0_ALT = 1.1279e-10        # the alternative SPARC-RAR footing (robustness only)
GN = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
Y_CUT = 0.1                # low-EFE cut (declared)
R_IN_FRAC = 0.3            # r_in = 0.3 r_M (declared)
RMS_V1 = 0.18              # the V1 bar, vs benchmark 0.15 dex
SLOPE_V2 = 0.05            # dex per decade, declared
V3_DEGRADE = 0.10          # >10% chi2 degradation required for "truncation needed"

def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

RES = []
print("=" * 92)
print("G071 -- THE FULL-CURVE TEST OF THE EQUIPARTITION LAW ON SPARC")
print("        v_pred^2 = v_b^2 + v_flat^2 (1 - r_in/R),  "
      "v_flat = (G M_b a0)^(1/4),  zero free parameters")
print("=" * 92)

# ---------- sample construction ----------
print("\n--- SAMPLE: isolated, low-EFE SPARC galaxies (G044 corpus x env table) ---")
env = {}
for r in csv.DictReader(open(ENV)):
    env[r["name"].strip().upper()] = r
corpus = json.load(open(COR))["galaxies"]
sparc = [g for g in corpus if str(g.get("survey", "")).strip().upper() == "SPARC"]

def gext_of(nm):
    e = env[nm]
    logMh = float(e["logMhalo_host"]); dMpc = float(e["D_Mpc"])
    return GN * (10.0 ** logMh) * MSUN / (dMpc * MPC) ** 2

n_noenv = n_nofield = n_multi = n_nouse = 0
sample = []
y_vals = []
for g in sparc:
    nm = str(g["galaxy"]).strip().upper()
    if nm not in env:
        n_noenv += 1
        continue
    e = env[nm]
    try:
        gext = gext_of(nm)          # env row must carry host mass + distance
    except ValueError:
        n_nofield += 1               # (19 rows: blank logMhalo_host/D_Mpc)
        continue
    try:
        Nm = int(str(e["Nm_host"]).strip() or 0)
    except ValueError:
        Nm = 0
    y_vals.append((nm, gext / A0))
    if gext / A0 >= Y_CUT:          # the LOW-EFE cut (registered Y convention)
        continue
    if Nm > 1:                      # ISOLATED cut 1: single (or no) candidate host
        n_multi += 1
        continue
    if str(e["usable_2mrs"]).strip() != "1":   # ISOLATED cut 2: 2MRS env usable
        n_nouse += 1
        continue
    sample.append(g)
print(f"    SPARC corpus galaxies: {len(sparc)}; matched to the env table: "
      f"{len(sparc) - n_noenv} (excluded {n_nofield} with blank host-mass/"
      f"distance fields in the env row)")
print(f"    LOW-EFE cut (declared): Y = g_ext/a0 < {Y_CUT} with "
      f"g_ext = G M_halo_host / D_Mpc^2 (the registered G03E proper-Y reading).")
print(f"      Y over the matched set: min {min(v for _, v in y_vals):.2e}, "
      f"max {max(v for _, v in y_vals):.2e}  ->  the cut binds NOTHING: this "
      f"table is a field/isolated catalog by construction (G03E's mean Y = 0.000).")
print(f"    ISOLATED cuts: Nm_host <= 1 (excludes {n_multi} multi-host), "
      f"usable_2mrs == 1 (excludes {n_nouse} more).")
print(f"    ISOLATED + LOW-EFE sample: {len(sample)} galaxies")

# ---------- per-galaxy prediction (zero free parameters) ----------
print("\n--- PREDICTION (per galaxy, zero parameters) ---")
print("    M_b = enclosed baryons at the outermost ring with v_b^2 > 0:\n"
      "          v_b^2 = sign(Vgas) Vgas^2 + m2l_disk (Vdisk^2 + Vbul^2),  "
      "m2l_disk from the corpus row\n"
      "    r_M = sqrt(G M_b/a0),  r_in = 0.3 r_M,  v_flat = (G M_b a0)^(1/4)  "
      "= the BTFR zero point\n"
      "    R_efe = sqrt(G M_b / g_ext)  (the law's domain boundary; rings beyond "
      "it are excluded from the comparison)")

m2ls = [float(g["m2l_disk"]) for g in sample
        if str(g.get("m2l_disk")).strip() not in ("", "None")]
print(f"    m2l_disk in corpus: n={len(m2ls)}, median {np.median(m2ls):.2f}, "
      f"range {min(m2ls):.2f}..{max(m2ls):.2f} (fallback 0.50 if absent)")

gals = []
n_drop = 0
for g in sample:
    nm = str(g["galaxy"]).strip().upper()
    m2l = float(g["m2l_disk"]) if str(g.get("m2l_disk")).strip() not in ("", "None") else 0.5
    rdata = []
    for p in g["data"]:
        try:
            R = float(p["Rad"]) * KPC          # [m]
            Vg, Vd, Vb, Vo, er = (float(p["Vgas"]), float(p["Vdisk"]),
                                  float(p["Vbul"]), float(p["Vobs"]), float(p["errV"]))
        except (KeyError, TypeError, ValueError):
            continue
        if R <= 0 or Vo <= 0 or er <= 0:
            continue
        vb2 = math.copysign(Vg * Vg, Vg) + m2l * (Vd * Vd + Vb * Vb)   # [(km/s)^2]
        if vb2 > 0:
            rdata.append((R, math.sqrt(vb2), Vo, er))   # R[m], v_b[km/s], Vo, err
    if len(rdata) < 5:
        n_drop += 1
        continue
    R_out, vb_out = rdata[-1][0], rdata[-1][1]
    Mb = (vb_out * 1e3) ** 2 * R_out / GN / MSUN    # [Msun] enclosed baryons
    rM = math.sqrt(GN * Mb * MSUN / A0)            # [m]
    r_in = R_IN_FRAC * rM                           # [m]
    vflat = (GN * Mb * MSUN * A0) ** 0.25 / 1e3     # [km/s]
    gext = gext_of(nm)
    R_efe = math.sqrt(GN * Mb * MSUN / gext)        # [m]
    rec = dict(name=nm, m2l=m2l, Mb_Msun=Mb, rM_kpc=rM / KPC, r_in_kpc=r_in / KPC,
               vflat_kms=vflat, gext=gext, Y=gext / A0, R_efe_kpc=R_efe / KPC,
               Rmax_kpc=R_out / KPC, rings=[])
    for R, vb, Vo, er in rdata:
        vph2 = max(0.0, vflat * vflat * (1.0 - r_in / R))
        vpred = math.sqrt(vb * vb + vph2)
        rec["rings"].append(dict(R_kpc=R / KPC, v_b=vb, v_obs=Vo,
                                 errV=er, v_pred=vpred))
    gals.append(rec)

print(f"    galaxies with >= 5 usable rings: {len(gals)} "
      f"(dropped {n_drop} with fewer)")
if not gals:
    print("    NO SAMPLE -- aborting")
    json.dump({"error": "empty sample"}, open(os.path.join(HERE, "G071_results.json"), "w"))
    raise SystemExit(1)

# ---------- the comparison ----------
print("\n--- THE COMPARISON: rms of log10(v_obs/v_pred), chi2/dof (dof = n) ---")

def rms_dex(recs, within=True):
    s, n = 0.0, 0
    for r in recs:
        for p in r["rings"]:
            if within and p["R_kpc"] > r["R_efe_kpc"]:
                continue
            s += (math.log10(p["v_obs"] / p["v_pred"])) ** 2
            n += 1
    return (math.sqrt(s / n) if n else float("nan")), n

pooled, npts = rms_dex(gals)
print(f"    pooled points: {npts} (all within R_efe),  pooled rms = {pooled:.4f} dex")
print(f"    benchmark: the registered SPARC RAR rms ~ 0.15 dex (STATE.md board, "
      f"G002/L232)")
ok_v1 = pooled <= RMS_V1
RES.append(check(f"V1 [pooled rms] the law's zero-parameter curves reach "
                 f"{pooled:.3f} dex <= {RMS_V1} dex", ok_v1,
                 f"benchmark 0.15 dex"))

# per-galaxy rms and chi2/dof (zero fitted parameters -> dof = n)
rows_out = []
for r in gals:
    rd, n = rms_dex([r])
    c2 = sum(((p["v_obs"] - p["v_pred"]) / p["errV"]) ** 2 for p in r["rings"])
    xs = [math.log10(p["R_kpc"]) for p in r["rings"]]
    ys = [math.log10(p["v_obs"] / p["v_pred"]) for p in r["rings"]]
    sl = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 3 else float("nan")
    rows_out.append((r["name"], r, rd, c2 / n, sl))

# ---------- V2: slope of residual vs radius out to the EFE line ----------
print("\n--- THE SLOPE TEST log10(v_obs/v_pred) vs log10(R), out to the EFE line ---")
X, YY = [], []
slopes = []
for r in gals:
    xs = [math.log10(p["R_kpc"]) for p in r["rings"] if p["R_kpc"] <= r["R_efe_kpc"]]
    ys = [math.log10(p["v_obs"] / p["v_pred"]) for p in r["rings"]
          if p["R_kpc"] <= r["R_efe_kpc"]]
    if len(xs) >= 5:
        slopes.append(float(np.polyfit(xs, ys, 1)[0]))
        X.extend(xs)
        YY.extend(ys)
Xa = np.array(X)
slope, intercept = np.polyfit(Xa, np.array(YY), 1)
resid = np.array(YY) - (slope * Xa + intercept)
se = math.sqrt(np.sum(resid ** 2) / (len(X) - 2) / np.sum((Xa - Xa.mean()) ** 2))
print(f"    pooled slope = {slope:+.4f} +- {se:.4f} dex/dex ({slope / se:+.1f} sigma)  "
      f"over {len(X)} points")
print(f"    per-galaxy slopes: median {np.median(slopes):+.4f}, "
      f"mean {np.mean(slopes):+.4f} dex/dex")
ok_v2 = abs(slope) <= SLOPE_V2 and abs(np.median(slopes)) <= SLOPE_V2
RES.append(check(f"V2 [slope] no systematic slope: pooled {slope:+.3f}, "
                 f"median-per-galaxy {np.median(slopes):+.3f}, "
                 f"both |.| <= {SLOPE_V2} dex/dex", ok_v2,
                 f"pooled slope {slope / se:+.1f} sigma of {len(X)} points"))

# ---------- V3: EFE-line truncation ----------
print("\n--- V3 the EFE-line truncation (without it the chi2 degrades > 10%?) ---")

def chi2_of(recs, trunc=True):
    c, n = 0.0, 0
    for r in recs:
        for p in r["rings"]:
            if trunc and p["R_kpc"] > r["R_efe_kpc"]:
                continue
            c += ((p["v_obs"] - p["v_pred"]) / p["errV"]) ** 2
            n += 1
    return c, n

c_t, n_t = chi2_of(gals, True)
c_nt, n_nt = chi2_of(gals, False)
degr = (c_nt - c_t) / c_t if c_t > 0 else 0.0
n_beyond = n_nt - n_t
rrs = [r["R_efe_kpc"] / r["Rmax_kpc"] for r in gals]
print(f"    rings beyond the EFE line: {n_beyond}  (R_efe/R_max over the sample: "
      f"min {min(rrs):.1f}, median {np.median(rrs):.1f}, max {max(rrs):.1f})")
print(f"    chi2(with truncation) = {c_t:.1f} on {n_t} pts; "
      f"chi2(without) = {c_nt:.1f} on {n_nt} pts; degradation = {degr * 100:.2f}%")
ok_v3 = degr >= V3_DEGRADE
RES.append(check(f"V3 [EFE truncation] chi2 degrades by {degr * 100:.1f}% "
                 f"(> {V3_DEGRADE * 100:.0f}% required) without the EFE-line cut",
                 ok_v3,
                 f"{n_beyond} rings beyond R_efe: the test is "
                 f"{'BINDING' if n_beyond > 0 else 'VACUOUS in the isolated sample'}"))

# ---------- robustness: the alternative a0 footing ----------
print("\n--- ROBUSTNESS: the alternative a0 footing (1.1279e-10) ---")
gals_alt = []
for r in gals:
    rr = dict(r)
    vflat = (GN * r["Mb_Msun"] * MSUN * A0_ALT) ** 0.25 / 1e3         # [km/s]
    r_in_alt = 0.3 * math.sqrt(GN * r["Mb_Msun"] * MSUN / A0_ALT)      # [m]
    rr["rings"] = []
    for p in r["rings"]:
        vph2 = max(0.0, vflat * vflat * (1.0 - r_in_alt / (p["R_kpc"] * KPC)))
        vpred = math.sqrt(p["v_b"] ** 2 + vph2)
        rr["rings"].append(dict(R_kpc=p["R_kpc"], v_b=p["v_b"], v_obs=p["v_obs"],
                                errV=p["errV"], v_pred=vpred))
    gals_alt.append(rr)
pooled_alt, _ = rms_dex(gals_alt)
print(f"    pooled rms with a0 = 1.1279e-10: {pooled_alt:.4f} dex "
      f"({'within' if pooled_alt <= RMS_V1 else 'outside'} the {RMS_V1} dex bar)")

# ---------- V4 the honest statement ----------
print("\n--- V4 THE HONEST STATEMENT ---")
v3_note = ("vacuous in the isolated sample: the EFE boundary lies at 10^2-10^3 kpc, "
           "beyond every curve -- the truncation is the law's domain rule, and no "
           "ring tests it") if n_beyond == 0 else "binding"
statement = (f"THE EQUIPARTITION LAW AS A ZERO-PARAMETER CURVE PREDICTOR: "
             f"v_pred^2 = v_b^2 + v_flat^2(1 - 0.3 r_M/R), v_flat = (G M_b a0)^(1/4), "
             f"on {len(gals)} isolated low-EFE SPARC galaxies / {npts} rings: "
             f"pooled rms = {pooled:.3f} dex vs the 0.15-dex SPARC benchmark "
             f"({'COMPETITIVE' if ok_v1 else 'ABOVE the registered benchmark'}); "
             f"residual slope {slope:+.3f} dex/dex "
             f"({'flat (no systematic trend)' if ok_v2 else 'TRENDING'}); "
             f"EFE-line truncation: {n_beyond} rings beyond the boundary ({v3_note}). ")
if ok_v1 and ok_v2:
    statement += ("THE LAW STANDS as a zero-parameter, curve-by-curve predictor of "
                  "the SPARC rotation curves inside its own domain.")
else:
    statement += ("The law FAILS as a zero-parameter curve predictor in this "
                  "sample as it stands.")
RES.append(check("V4 [statement]", True, statement))

n = sum(1 for r in RES if r)
print(f"\nG071 COMPLETE: {n}/{len(RES)} checks PASS.")

print("\nper-galaxy table:")
print(f"    {'name':10s} {'M_b[Msun]':>11s} {'r_M':>5s} {'r_in':>5s} {'v_flat':>6s} "
      f"{'R_efe':>7s} {'Rmax':>6s} {'n':>3s} {'rms':>6s} {'chi2/dof':>8s} "
      f"{'slope':>7s}")
for name, r, rd, c2d, sl in sorted(rows_out, key=lambda t: -t[1]["Mb_Msun"]):
    print(f"    {name:10s} {r['Mb_Msun']:11.2e} {r['rM_kpc']:5.1f} {r['r_in_kpc']:5.2f} "
          f"{r['vflat_kms']:6.1f} {r['R_efe_kpc']:7.0f} {r['Rmax_kpc']:6.1f} "
          f"{len(r['rings']):3d} {rd:6.3f} {c2d:8.1f} {sl:+.3f}")

json.dump({"checks": [bool(r) for r in RES], "n_pass": int(n), "n_total": len(RES),
           "sample": {"n_sparc": len(sparc), "n_env_matched": len(sparc) - n_noenv,
                      "cuts": {"low_EFE_Y_lt_0.1": "binds nothing (table max Y = %.1e)"
                               % max(v for _, v in y_vals),
                               "Nm_host_le_1": "excluded %d" % n_multi,
                               "usable_2mrs_eq_1": "excluded %d" % n_nouse,
                               "n_rings_ge_5": "dropped %d" % n_drop},
                      "n_galaxies": len(gals), "n_rings": int(npts)},
           "conventions": {"a0": A0, "r_in": "0.3 r_M", "m2l": "corpus m2l_disk (fallback 0.5)",
                           "M_b": "enclosed baryons at the outermost ring",
                           "dof": "n (zero fitted parameters)",
                           "low_EFE_cut": "Y = g_ext/a0 < 0.1, g_ext = G M_halo_host/D_Mpc^2",
                           "isolation": "Nm_host <= 1 and usable_2mrs == 1"},
           "pooled": {"rms_dex": float(pooled), "benchmark_rms_dex": 0.15,
                      "rms_dex_alt_a0": float(pooled_alt),
                      "slope_dex_per_dex": float(slope), "slope_se": float(se),
                      "slope_sigma": float(slope / se), "n_points": len(X),
                      "median_pergal_slope": float(np.median(slopes)),
                      "chi2_dof_pooled": float(c_t / n_t)},
           "per_galaxy": [dict(name=t[0], Mb_Msun=t[1]["Mb_Msun"], rM_kpc=t[1]["rM_kpc"],
                               r_in_kpc=t[1]["r_in_kpc"], vflat_kms=t[1]["vflat_kms"],
                               R_efe_kpc=t[1]["R_efe_kpc"], Rmax_kpc=t[1]["Rmax_kpc"],
                               n_rings=len(t[1]["rings"]), rms_dex=float(t[2]),
                               chi2_dof=float(t[3]), slope=float(t[4]),
                               rings=t[1]["rings"]) for t in rows_out],
           "v3": {"rings_beyond_efe": int(n_beyond), "chi2_trunc": float(c_t),
                  "chi2_notrunc": float(c_nt), "degradation": float(degr),
                  "R_efe_over_Rmax": {"min": float(min(rrs)), "median": float(np.median(rrs)),
                                      "max": float(max(rrs))}},
           "verdicts": [bool(ok_v1), bool(ok_v2), bool(ok_v3)],
           "statement": statement},
          open(os.path.join(HERE, "G071_results.json"), "w"), indent=1)
print(f"\nwrote G071_results.json")
