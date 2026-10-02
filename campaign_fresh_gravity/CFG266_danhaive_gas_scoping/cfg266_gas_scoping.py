#!/usr/bin/env python3
"""CFG266 scoping helper: field per row and gas-tracer REQUIREMENT fluxes for the 41 Danhaive+25 gold discs.

SCOPING ONLY. No a0 analysis, no s* is computed. kappa = 1/2 is FITTED.
Inputs (read-only, on disk):
  data_assembly/arxiv_tables/danhaive2025_gold.csv              (arXiv:2503.21863 v1, the 41-row gold table)
  campaign_fresh_gravity/CFG273_danhaive_gold41/cfg273_points_stageB_relabelled.csv
      (CFG273's own columns: gas_to_star_req = extra baryons in units of M* that FLAT needs at the canonical
       scale, no_root, D, y, lever; this script only READS them)
Outputs: cfg266_rows.csv and stdout (tee to cfg266_gas_scoping.out); MUTATE=1 writes *_MUTATE1.* instead.

Field rule (page reads, SCOPING.md section 1):
  * a 7-digit JADES ID starting 10xxxxx is a GOODS-N ID (arXiv:2505.02895 writes "GN-1034620" and
    "JADES ID: 1080661; RA = 189.27616 deg, Dec = 62.21416 deg", IDs "from JADES DR2"); 6-digit IDs are GOODS-S;
  * independent check from the paper's own text (main.tex line 178): FRESCO F444W (3.9-5.0 um) in both fields,
    CONGRESS F356W (3-4 um) in GOODS-N only; Halpha (6564.61 A vacuum) is in F444W only for z >= 4.941, so every
    row with z < 4.941 must be CONGRESS, i.e. GOODS-N. Control C2 checks the two rules agree.
Requirement flux = the flux a tracer would show if the disc held exactly the gas FLAT needs (M_req =
gas_to_star_req x M*), computed at the FAVOURABLE end of the metallicity-sensitive conversions (solar gas-to-dust,
Galactic alpha_CO, thermalised CO: the end that gives the MOST flux for a sub-solar z ~ 4-6 disc), so "powered" is
optimistic on those factors. NOT favourable on dust temperature: T_d is fixed at 25 K as in CFG142; a warmer
mass-weighted T_d would raise the dust flux per unit gas mass.
  dust  : Scoville+2016 RJ recipe exactly as CFG142 (T_d = 25 K, alpha_850 = 6.7e19, solar gas-to-dust);
          CFG142's generous end (gas-to-dust x 2) and a CMB-contrast variant (1 - B(T_CMB(z))/B(T_d) at the rest
          frequency, still 25 K) are also scored;
  CO    : alpha_CO = 4.36 (Galactic incl. He; sub-solar discs have higher alpha_CO, i.e. less flux), r_J1 = 1;
  [CII] : Zanella+2018 as quoted by Dessauges-Zavadsky+2020 (arXiv:2004.10771, eq. zanella):
          log L = -1.28 + 0.98 log M_mol (0.3 dex dispersion); reference only (no public [CII] in GOODS-N);
  line width: FWHM = max(200, 2.355 sigma0) km/s (sigma0-limit rows use the limit: favourable).
"Powered" = requirement flux >= 3 sigma of the survey at its quoted (best) depth: only then can a non-detection at
a known position exclude FLAT's gas requirement for that row. Positions are NOT known (SCOPING.md section 1).
"""
import csv
import math
import os
import sys

MUT = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE1" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", ".."))

h, k, c = 6.62607015e-34, 1.380649e-23, 2.99792458e8
TD = 25.0
NU850 = c / 850e-6
H0, OM = 67.66, 0.30966              # Planck18, as CFG142
T_CMB0 = 2.7255
HALPHA_A = 6564.61                   # vacuum
ALPHA_CO = 4.36

# survey depths (verified page reads; SCOPING.md section 2 gives the sources)
S2_RMS_850 = 0.28                    # SCUBA-2 SUPER GOODS I, central rms, mJy (arXiv:1702.03002 abstract)
N2_RMS_12, N2_RMS_20 = 0.17, 0.047   # N2CLS GOODS-N 1 sigma, mJy/beam (arXiv:2506.22046 sec. 2.1)
GA_RMS_265 = 0.0684                  # GOODS-ALMA 2.0 mean combined rms, mJy/beam (arXiv:2106.13246, Table 1, on disk)
AS_RMS_12 = 0.0093                   # ASPECS 1.2 mm rms, mJy/beam (arXiv:2002.07199 abstract)
COLDZ_6SIG_GN = 0.55                 # COLDz GOODS-N median 6 sigma, mJy/beam, 200 km/s line (arXiv:1808.04372 App. D.2)
COLDZ_Z = (4.91, 6.70)               # CO(2-1) window (arXiv:1808.04372 abstract)
HDFN_RMS_9MHZ = 0.42                 # NOEMA HDF-N best cube rms per 9 MHz channel, mJy/beam (arXiv:2301.05705 Table 2)
HDFN_NU = (82.394, 113.322)          # GHz (arXiv:2301.05705 Table 1 note)
NU_CO = {"CO(4-3)": 461.041, "CO(5-4)": 576.268, "[CI](1-0)": 492.161}
NU_CII = 1900.537


def d_l_gpc(z, n=20000):
    s = sum(1.0 / math.sqrt(OM * (1 + z * (i + 0.5) / n) ** 3 + 1 - OM) for i in range(n)) * z / n
    return (1 + z) * c / 1e3 / H0 * s / 1e3


def gam(nu, z, td=TD):
    x = h * nu * (1 + z) / (k * td)
    return x / math.expm1(x)


def s_dust_mjy(m_ism, z, nu_obs):
    per_mjy = 1.78 * (1 + z) ** -4.8 * (NU850 / nu_obs) ** 3.8 * (gam(NU850, 0) / gam(nu_obs, z)) * d_l_gpc(z) ** 2 * 1e10
    return m_ism / per_mjy


def cmb_contrast(z, nu_obs, td=TD):
    nur = nu_obs * (1 + z)
    tc = T_CMB0 * (1 + z)
    return 1.0 - math.expm1(h * nur / (k * td)) / math.expm1(h * nur / (k * tc))


def sdv_from_lprime(lp, z, nu_rest_ghz):
    """S dv [Jy km/s] from L' [K km/s pc^2] (Solomon+1997): L' = 3.25e7 S dv nu_obs^-2 D_L^2 (1+z)^-3."""
    nu_obs = nu_rest_ghz / (1 + z)
    dl = d_l_gpc(z) * 1e3
    return lp * nu_obs ** 2 * (1 + z) ** 3 / (3.25e7 * dl ** 2)


def lprime_from_sdv(sdv, z, nu_rest_ghz):
    nu_obs = nu_rest_ghz / (1 + z)
    dl = d_l_gpc(z) * 1e3
    return 3.25e7 * sdv * dl ** 2 / (nu_obs ** 2 * (1 + z) ** 3)


def cii_sdv(m_mol, z):
    lcii = 10 ** (-1.28 + 0.98 * math.log10(m_mol))
    nu_obs = NU_CII / (1 + z)
    dl = d_l_gpc(z) * 1e3
    return lcii / (1.04e-3 * nu_obs * dl ** 2)


def fnum(x, f="{:.3g}"):
    return "" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f.format(x)


checks = []


def check(name, ok, detail):
    checks.append((name, bool(ok)))
    print(f"  {name}: {'PASS' if ok else 'FAIL'}  ({detail})")


print("CFG266 scoping helper" + ("   [MUTATE=1: field rule inverted; C2 must FAIL]" if MUT else ""))
gold = list(csv.DictReader(open(os.path.join(root, "data_assembly", "arxiv_tables", "danhaive2025_gold.csv"))))
pts = list(csv.DictReader(open(os.path.join(here, "..", "CFG273_danhaive_gold41", "cfg273_points_stageB_relabelled.csv"))))
pts = pts[:41]

z_f444_min = 3.9e4 / HALPHA_A - 1
z_f356_max = 4.0e4 / HALPHA_A - 1
print("\nCONTROLS")
check("C1 41 rows; gold CSV IDs equal CFG273 row order", len(gold) == 41 and all(gold[i]["jades_id"] in pts[i]["object"] for i in range(41)), f"{len(gold)} rows")


def field_by_id(jid):
    gn = int(jid) >= 1_000_000
    if MUT:
        gn = not gn
    return "GOODS-N" if gn else "GOODS-S"


bad = [g["jades_id"] for g in gold if float(g["z"]) < z_f444_min and field_by_id(g["jades_id"]) != "GOODS-N"]
check("C2 ID rule agrees with the filter rule (every z < %.3f row is GOODS-N)" % z_f444_min, not bad, f"disagreeing rows: {bad if bad else 'none'}")
k11 = s_dust_mjy(2 * 10 ** 10.68, 1.384, c / 1.1e-3)
check("C3 dust conversion reproduces CFG142's committed KURVS-11 S(mu_dust=2) = 0.912 mJy at 272.5 GHz (0.5%)", abs(k11 / 0.912 - 1) < 0.005, f"{k11:.4f} mJy")
coef = 1.19e27 * 1e-3 * 1e6 / 6.7e19
check("C4 Scoville coefficient 1.78e10 (1%) and Gamma_0 = 0.71 (2%) as CFG142 C-a / C-b", abs(coef / 1.78e10 - 1) < 0.01 and abs(gam(NU850, 0) / 0.71 - 1) < 0.02, f"{coef:.4e}, {gam(NU850, 0):.4f}")
a10 = 1e10 / 10 ** (-1.28 + 0.98 * 10)
check("C5 Zanella relation gives alpha_[CII] = M/L in 25-35 at M = 1e10 (the paper's ~31)", 25 < a10 < 35, f"{a10:.1f} Msun/Lsun")
rt = lprime_from_sdv(sdv_from_lprime(3.3e9, 5.19, 230.538), 5.19, 230.538) / 3.3e9 - 1
check("C6 L' <-> S dv round trip", abs(rt) < 1e-12, f"{rt:.1e}")
print(f"  C7 (info): Halpha in F444W (3.9-5.0 um) for z {z_f444_min:.3f}-{5.0e4 / HALPHA_A - 1:.3f}; in F356W (3-4 um) for z {3.0e4 / HALPHA_A - 1:.3f}-{z_f356_max:.3f}")

thr = dict(scuba2_850=3 * S2_RMS_850, n2cls_12=3 * N2_RMS_12, n2cls_20=3 * N2_RMS_20, goodsalma_265=3 * GA_RMS_265, aspecs_12=3 * AS_RMS_12)
nu = dict(scuba2_850=NU850, n2cls_12=c / 1.2e-3, n2cls_20=c / 2.0e-3, goodsalma_265=265.0e9, aspecs_12=c / 1.2e-3)
rows = []
for g, p in zip(gold, pts):
    jid, z, lms = g["jades_id"], float(g["z"]), float(g["logMstar"])
    s0 = float(g["sigma0_kms"])
    fld = field_by_id(jid)
    survey = "FRESCO (F444W)" if z >= z_f444_min else "CONGRESS (F356W)"
    req = float(p["gas_to_star_req"]) if p["gas_to_star_req"] not in ("", "nan") else float("nan")
    no_root, dd = int(p["no_root"]), float(p["D"])
    if no_root and dd <= 1:
        cat = "floor (D<=1): FLAT below the stars alone; gas cannot change the FLAT reading"
    elif not math.isfinite(req):
        cat = "ceiling: requirement above CFG273's bracket; not computed"
    elif req <= 0:
        cat = "stars-only bound already below s=1: gas cannot change the FLAT reading"
    else:
        cat = "needs gas for FLAT"
    mreq = req * 10 ** lms if (math.isfinite(req) and req > 0) else float("nan")
    r = dict(jades_id=jid, z=z, logMstar=lms, sigma0_kms=s0, sigma0_limit=g["sigma0_kms_lim"].strip(), field=fld, grism_survey=survey,
             protocluster_z_tag=("z~4.41 (Lin+25)" if abs(z - 4.41) <= 0.03 + 1e-9 else "z~5.19 (Lin+25)" if abs(z - 5.19) <= 0.03 + 1e-9 else "") if fld == "GOODS-N" else "",
             cfg273_y=float(p["y"]), cfg273_lever=float(p["lever"]), cfg273_D=dd, cfg273_gas_to_star_req=req, category=cat, M_gas_req=mreq)
    fwhm = max(200.0, 2.355 * s0)
    r["fwhm_kms_assumed"] = fwhm
    # dust (favourable end) per survey that can reach the field
    for key in thr:
        ok_field = (fld == "GOODS-N") == key.startswith(("scuba2", "n2cls"))
        if math.isfinite(mreq) and ok_field:
            sreq = s_dust_mjy(mreq, z, nu[key])
            cc = cmb_contrast(z, nu[key])
            r[f"S_req_{key}_mJy"] = sreq
            r[f"cmb_contrast_{key}"] = cc
            r[f"powered_{key}"] = int(sreq >= thr[key])
            # CFG142's generous end: gas-to-dust x 2 (sub-solar metallicity) halves the dust flux; then the CMB contrast at 25 K
            r[f"powered_gdr2_{key}"] = int(sreq / 2 >= thr[key])
            r[f"powered_gdr2_cmb_{key}"] = int(sreq / 2 * cc >= thr[key])
        else:
            r[f"S_req_{key}_mJy"] = float("nan")
            r[f"cmb_contrast_{key}"] = float("nan")
            r[f"powered_{key}"] = ""
            r[f"powered_gdr2_{key}"] = ""
            r[f"powered_gdr2_cmb_{key}"] = ""
    # COLDz CO(2-1), GOODS-N only, inside its z window
    if fld == "GOODS-N" and COLDZ_Z[0] <= z <= COLDZ_Z[1] and math.isfinite(mreq):
        sdv = sdv_from_lprime(mreq / ALPHA_CO, z, 230.538)
        peak = sdv / (1.0645 * fwhm) * 1e3
        sig = COLDZ_6SIG_GN / 6 * math.sqrt(200.0 / fwhm)
        r.update(coldz_Sdv_req=sdv, coldz_peak_req_mJy=peak, coldz_3sig_mJy=3 * sig, powered_coldz=int(peak >= 3 * sig))
    else:
        r.update(coldz_Sdv_req=float("nan"), coldz_peak_req_mJy=float("nan"), coldz_3sig_mJy=float("nan"), powered_coldz="")
    # NOEMA HDF-N 3 mm scan, GOODS-N only, brightest line in the window (thermalised: S dv ~ nu^2)
    best = None
    if fld == "GOODS-N" and math.isfinite(mreq):
        for ln, nr in NU_CO.items():
            nobs = nr / (1 + z)
            if HDFN_NU[0] <= nobs <= HDFN_NU[1] and ln.startswith("CO"):
                sdv = sdv_from_lprime(mreq / ALPHA_CO, z, nr)
                dnu_mhz = fwhm / 2.99792458e5 * nobs * 1e3
                sig = HDFN_RMS_9MHZ * math.sqrt(9.0 / dnu_mhz)
                peak = sdv / (1.0645 * fwhm) * 1e3
                if best is None or peak / sig > best[2] / best[3]:
                    best = (ln, sdv, peak, sig)
    if best:
        # ratio = peak / 3 sigma at r_J1 = 1; the row stays powered for any excitation r_J1 >= 1 / ratio
        r.update(hdfn_line=best[0], hdfn_Sdv_req=best[1], hdfn_peak_req_mJy=best[2], hdfn_3sig_mJy=3 * best[3], powered_hdfn=int(best[2] >= 3 * best[3]),
                 hdfn_rJ1_needed=3 * best[3] / best[2])
    else:
        r.update(hdfn_line="", hdfn_Sdv_req=float("nan"), hdfn_peak_req_mJy=float("nan"), hdfn_3sig_mJy=float("nan"), powered_hdfn="", hdfn_rJ1_needed=float("nan"))
    r["cii_Sdv_req_Jykms"] = cii_sdv(mreq, z) if math.isfinite(mreq) else float("nan")
    r["cii_nu_obs_GHz"] = NU_CII / (1 + z)
    rows.append(r)

print("\nPER ROW (requirement fluxes at the favourable end; 'P' = powered = requirement >= 3 sigma at the survey's quoted depth)")
print(f"  {'id':>8s} {'z':>5s} {'field':7s} {'lgM*':>5s} {'req':>6s} {'M_req':>8s}  {'S850':>6s} {'S1.2':>6s} {'S2.0':>6s} {'SGA':>6s} {'SAS':>6s}  {'CO21pk':>6s}/{'3sig':>5s}  {'HDFN pk':>7s}/{'3sig':>5s}  {'[CII]':>6s}  powered")
for r in rows:
    pw = [nm for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12") if r[f"powered_{nm}"] == 1]
    pw += ["coldz"] if r["powered_coldz"] == 1 else []
    pw += ["hdfn"] if r["powered_hdfn"] == 1 else []
    print(f"  {r['jades_id']:>8s} {r['z']:5.2f} {r['field']:7s} {r['logMstar']:5.2f} {fnum(r['cfg273_gas_to_star_req'], '{:+6.2f}'):>6s} {fnum(r['M_gas_req'], '{:8.2e}'):>8s}  "
          + " ".join(f"{fnum(r[f'S_req_{nm}_mJy'], '{:6.3f}'):>6s}" for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12"))
          + f"  {fnum(r['coldz_peak_req_mJy'], '{:6.3f}'):>6s}/{fnum(r['coldz_3sig_mJy'], '{:5.3f}'):>5s}  {fnum(r['hdfn_peak_req_mJy'], '{:7.3f}'):>7s}/{fnum(r['hdfn_3sig_mJy'], '{:5.3f}'):>5s}  {fnum(r['cii_Sdv_req_Jykms'], '{:6.3f}'):>6s}  "
          + (",".join(pw) if pw else ("-" if r["category"] == "needs gas for FLAT" else "[" + r["category"].split(":")[0] + "]")))

print("\n3-sigma thresholds (mJy): " + ", ".join(f"{kk} {vv:.3f}" for kk, vv in thr.items()) + f"; COLDz 3 sigma at 200 km/s {COLDZ_6SIG_GN / 2:.3f} (scaled by sqrt(200/FWHM)); HDF-N per-row (best cube rms {HDFN_RMS_9MHZ} mJy / 9 MHz)")
ngn = sum(r["field"] == "GOODS-N" for r in rows)
print("\nCOUNTS")
print(f"  fields: GOODS-N {ngn}, GOODS-S {41 - ngn}; grism: CONGRESS {sum(r['grism_survey'].startswith('CONGRESS') for r in rows)}, FRESCO {sum(r['grism_survey'].startswith('FRESCO') for r in rows)} "
      f"(FRESCO GOODS-N {sum(r['grism_survey'].startswith('FRESCO') and r['field'] == 'GOODS-N' for r in rows)}, FRESCO GOODS-S {sum(r['grism_survey'].startswith('FRESCO') and r['field'] == 'GOODS-S' for r in rows)})")
cats = {}
for r in rows:
    cats[r["category"]] = cats.get(r["category"], 0) + 1
for kk, vv in cats.items():
    print(f"  category: {vv:2d}  {kk}")
for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12", "coldz", "hdfn"):
    elig = [r for r in rows if r[f"powered_{nm}"] != ""]
    pw = [r["jades_id"] for r in elig if r[f"powered_{nm}"] == 1]
    print(f"  {nm:14s}: rows with a requirement in reach of the survey's field/z window {len(elig):2d}; powered {len(pw):2d} {pw}")
for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12"):
    g2 = [r["jades_id"] for r in rows if r[f"powered_gdr2_{nm}"] == 1]
    g2c = [r["jades_id"] for r in rows if r[f"powered_gdr2_cmb_{nm}"] == 1]
    print(f"  {nm:14s}: powered at gas-to-dust x2: {len(g2):2d} {g2}; and with the CMB contrast: {len(g2c):2d} {g2c}")
hd = sorted(((r["hdfn_rJ1_needed"], r["jades_id"], r["hdfn_line"]) for r in rows if r["powered_hdfn"] == 1))
print("  hdfn powered rows and the excitation r_J1 each needs to stay powered: " + ", ".join(f"{i} {ln} r>={v:.2f}" for v, i, ln in hd))
anyp = [r["jades_id"] for r in rows if any(r[f"powered_{nm}"] == 1 for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12", "coldz", "hdfn"))]
print(f"  any route powered at the favourable end (IF the row lies inside that survey's footprint; positions unknown): {len(anyp)} {anyp}")
anyg = [r["jades_id"] for r in rows if any(r[f"powered_gdr2_cmb_{nm}"] == 1 for nm in ("scuba2_850", "n2cls_12", "n2cls_20", "goodsalma_265", "aspecs_12"))]
print(f"  dust routes still powered at gas-to-dust x2 with the CMB contrast: {len(anyg)} {anyg}")
alma_ok = [r["jades_id"] for r in rows if r["field"] == "GOODS-S"]
print(f"  rows ALMA can observe at all (GOODS-S; ALMA upper declination limit +47 deg): {len(alma_ok)} {alma_ok}")
tags = {}
for r in rows:
    if r["protocluster_z_tag"]:
        tags.setdefault(r["protocluster_z_tag"], []).append(r["jades_id"])
for kk, vv in tags.items():
    print(f"  z-only tag {kk} (|dz| <= 0.03, GOODS-N): {len(vv)} {vv}")

print("\nPRECISION A GAS MASS WOULD NEED (arithmetic on CFG273's own columns; no s* computed)")
print("  separation of the rival from FLAT in log a0 = log10 E(z), E = sqrt(Om (1+z)^3 + 1 - Om), Om 0.30 / 0.315 (PAPER38's range);")
print("  a COMMON-MODE baryon-calibration error sigma_cal moves log s* by |lever| sigma_cal and does not average down, so a k-sigma")
print("  separation needs sigma_cal <= log10 E / (k |lever|). lever = CFG273's d log10 s*/d(baryon dex) at STARS-ONLY baryons;")
print("  adding the gas FLAT needs raises y and |lever| (toward the Newtonian side), so these are upper bounds on sigma_cal.")
allp = list(csv.DictReader(open(os.path.join(here, "..", "CFG273_danhaive_gold41", "cfg273_points_stageB_relabelled.csv"))))
cond = sorted(abs(r["cfg273_lever"]) for r in rows if math.isfinite(r["cfg273_lever"]) and abs(r["cfg273_lever"]) < 10)
med_lev = cond[len(cond) // 2] if len(cond) % 2 else 0.5 * (cond[len(cond) // 2 - 1] + cond[len(cond) // 2])
print(f"  per-galaxy |lever| (conditioned rows, |lever| < 10, N = {len(cond)}): median {med_lev:.2f}, range {cond[0]:.2f}-{cond[-1]:.2f}")
print(f"  {'row':>6s} {'z':>6s} {'E(0.30)':>7s} {'E(0.315)':>8s} {'dlog a0':>8s} {'|lever|':>7s}  sigma_cal(3sig) pooled-lever / median-row-lever / PAPER38 4.8   T4 floor 3*0.2/sqrt(N)")
for p in allp[41:]:
    pn = p["object"].split()[-1]
    zz, lv = float(p["z"]), abs(float(p["lever"]))
    e30 = math.sqrt(0.30 * (1 + zz) ** 3 + 0.70)
    e315 = math.sqrt(0.315 * (1 + zz) ** 3 + 0.685)
    dl = math.log10(e30)
    nn = {"PALL": 41, "PDET": 24, "Pz1": 21, "Pz2": 12, "Pz3": 8, "P38": 38}.get(pn, 0)
    print(f"  {pn:>6s} {zz:6.3f} {e30:7.2f} {e315:8.2f} {dl:8.3f} {lv:7.2f}  {dl / (3 * lv):.3f} / {dl / (3 * med_lev):.3f} / {dl / (3 * 4.8):.3f} dex"
          + (f"   {3 * 0.2 / math.sqrt(nn):.3f}" if nn else ""))

out = os.path.join(here, f"cfg266_rows{SUF}.csv")
cols = list(rows[0].keys())
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({kk: (fnum(v, "{:.6g}") if isinstance(v, float) else v) for kk, v in r.items()})
print(f"\nwrote {os.path.relpath(out, root)}")
fails = [n for n, ok in checks if not ok]
print("ALL CONTROLS PASS" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
