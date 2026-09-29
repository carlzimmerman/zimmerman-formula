#!/usr/bin/env python3
"""Assemble the KMOS3D + PHIBSS (Tacconi+2013) high-z baryon/kinematics table.

Inputs (all in raw_small/, provenance in manifest.json):
  k3d_fnlsp_table_v3.fits          KMOS3D main catalogue (Wisnioski+2019), 785 rows
  k3d_fnlsp_table_hafits_v3.fits   KMOS3D Halpha aperture fluxes, 739 rows
  tacconi2013_table1.dat           PHIBSS CO observations (positions, z_CO), 58 rows
  tacconi2013_table2.dat           PHIBSS derived properties (Vrot, Mmol, M*), 73 rows

Outputs (this directory):
  phibss13_joined.csv       table 1 + table 2 joined on galaxy name
  kmos3d_phibss_match.csv   the sky+redshift cross-match KMOS3D <-> PHIBSS
  kmos3d_catalog.csv        KMOS3D catalogue with the Halpha fluxes merged on (FIELD, ID)
  checks.txt                every assertion and the chance-match control
  manifest.json             sha256 / size / URL of every raw input

No fits are run here and no number is tuned. Usage:  python3 build.py [--cubes DIR]
--cubes DIR (optional) records sha256/size of the KMOS3D cube tarballs found in DIR.
"""
import csv, hashlib, json, os, sys
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_small")
LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


def check(cond, msg):
    log(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        write_checks()
        sys.exit("check failed: " + msg)


def write_checks():
    with open(os.path.join(HERE, "checks.txt"), "w") as f:
        f.write("\n".join(LOG) + "\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- KMOS3D
main = fits.open(os.path.join(RAW, "k3d_fnlsp_table_v3.fits"))[1].data
haf = fits.open(os.path.join(RAW, "k3d_fnlsp_table_hafits_v3.fits"))[1].data
check(len(main) == 785, f"KMOS3D main catalogue has 785 rows (got {len(main)})")
check(len(haf) == 739, f"KMOS3D Halpha-flux catalogue has 739 rows (got {len(haf)})")


def s(x):
    return x.decode().strip() if isinstance(x, bytes) else str(x).strip()


keys_main = [(s(a), s(b)) for a, b in zip(main["FIELD"], main["ID"])]
check(len(set(keys_main)) == len(keys_main), "KMOS3D (FIELD, ID) is unique in the main catalogue")
keys_haf = {(s(a), s(b)): i for i, (a, b) in enumerate(zip(haf["FIELD"], haf["ID"]))}
check(len(keys_haf) == len(haf), "KMOS3D (FIELD, ID) is unique in the Halpha catalogue")
check(set(keys_haf) <= set(keys_main), "every Halpha-catalogue galaxy is in the main catalogue")

mcols = list(main.columns.names)
hcols = ["AP_RADIUS", "Z_ERR", "SIG", "SIG_ERR", "FLUX_HA", "FLUX_HA_ERR", "FLUX_AP_CORR", "FLAG"]
# Z appears in both: keep the main catalogue Z; the Halpha-fit redshift is kept as Z_HAFIT.
with open(os.path.join(HERE, "kmos3d_catalog.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(mcols + ["HAFIT_" + c for c in hcols] + ["HAFIT_Z", "HAFIT_PRESENT"])
    for i, k in enumerate(keys_main):
        row = [s(main[c][i]) if main[c].dtype.kind in "SU" else main[c][i] for c in mcols]
        j = keys_haf.get(k)
        if j is None:
            row += [""] * (len(hcols) + 1) + [0]
        else:
            row += [haf[c][j] for c in hcols] + [haf["Z"][j], 1]
        w.writerow(row)
log(f"wrote kmos3d_catalog.csv ({len(main)} rows, {len(mcols)} main + {len(hcols)+2} Halpha columns)")

# ---------------------------------------------------------------- PHIBSS (Tacconi+2013)
def sexa(sign, d, m, sec):
    v = abs(float(d)) + float(m) / 60 + float(sec) / 3600
    return -v if sign == "-" else v


t1 = {}
for ln in open(os.path.join(RAW, "tacconi2013_table1.dat")):
    ln = ln.rstrip("\n")
    if not ln.strip():
        continue
    name = ln[0:11].strip()
    try:
        ra = 15 * (float(ln[24:26]) + float(ln[27:29]) / 60 + float(ln[30:34]) / 3600)
        dec = sexa(ln[35:36], ln[36:38], ln[39:41], ln[42:46])
    except ValueError:
        ra = dec = np.nan
    zco = ln[70:75].strip()
    t1[name] = dict(ra=ra, dec=dec, zco=float(zco) if zco else np.nan, conf=ln[12:16].strip())
check(len(t1) == 58, f"PHIBSS table 1 has 58 rows (got {len(t1)})")


def num(x):
    x = x.strip()
    return float(x) if x else np.nan


t2 = []
for ln in open(os.path.join(RAW, "tacconi2013_table2.dat")):
    if not ln.strip():
        continue
    p = ln.rstrip("\n").split("|")
    check(len(p) == 14, f"table 2 line has 14 pipe-separated fields ({p[0].strip()})")
    t2.append(dict(
        name=p[0][:11].strip(), comp=p[0][11:].strip(), type=p[1].strip(),
        vrot_kms=num(p[2]), rh_opt_kpc=num(p[3]), rh_co_kpc=num(p[4]), sfr_msun_yr=num(p[5]),
        fco_jykms=num(p[6]), fco_err=num(p[7]), lco=num(p[8]), mmol_msun=num(p[9]),
        mstar_msun=num(p[10]), fgas=num(p[11]), logsmol=num(p[12]), logssfr=num(p[13])))
check(len(t2) == 73, f"PHIBSS table 2 has 73 rows (got {len(t2)})")
# ReadMe note 4: a minus sign marks a 3-sigma UPPER LIMIT.  Mmol carries the sign too.  Keep the
# magnitude and an explicit flag so nobody treats an upper limit as a measurement.
for r in t2:
    r["co_ul"] = int(r["fco_jykms"] < 0)
    r["mmol_signed"] = r["mmol_msun"]
    r["mmol_msun"] = abs(r["mmol_msun"])
check(all((r["mmol_signed"] < 0) == bool(r["co_ul"]) for r in t2 if np.isfinite(r["mmol_signed"])),
      "the sign of Mmol and the sign of F(CO) agree on which rows are upper limits")
# Internal consistency of the source table: fgas = Mmol/(Mmol+M*).  Masses are quoted to 2 significant
# figures, so 0.02 is the rounding floor.  Three PEP-sample rows exceed it; that is a property of the
# source table (recorded, not corrected): the quoted fgas is not reproducible from the quoted masses.
for r in t2:
    r["fgas_recomputed"] = r["mmol_msun"] / (r["mmol_msun"] + r["mstar_msun"]) \
        if np.isfinite(r["mmol_msun"]) and np.isfinite(r["mstar_msun"]) else np.nan
bad = sorted(r["name"] for r in t2 if np.isfinite(r["fgas"]) and np.isfinite(r["fgas_recomputed"])
             and abs(r["fgas_recomputed"] - r["fgas"]) > 0.02)
KNOWN_INCONSISTENT = ["PEPJ123709", "PEPJ123712", "PEPJ123759"]
check(bad == KNOWN_INCONSISTENT,
      f"fgas reproduced to 0.02 from the quoted masses for every row except the documented {KNOWN_INCONSISTENT} (found {bad})")
log("n_upper_limits = %d; %d rows have Mmol; the upper-limit rows are flagged co_upper_limit=1 in the output"
    % (sum(r["co_ul"] for r in t2), sum(np.isfinite(r["mmol_msun"]) for r in t2)))

cols = ["name", "comp", "type", "vrot_kms", "rh_opt_kpc", "rh_co_kpc", "sfr_msun_yr", "fco_jykms", "fco_err",
        "lco_K_kms_pc2", "mmol_msun", "mstar_msun", "mbar_msun", "mbar_is_upper_limit", "fgas_quoted", "fgas_recomputed", "logSigma_mol", "logSigma_sfr",
        "ra_deg", "dec_deg", "z_co", "has_position", "co_upper_limit", "fgas_inconsistent_in_source"]
n_pos = 0
rows_join = []
for r in t2:
    g = t1.get(r["name"])
    if g is not None and np.isfinite(g["ra"]):
        n_pos += 1
    rows_join.append([r["name"], r["comp"], r["type"], r["vrot_kms"], r["rh_opt_kpc"], r["rh_co_kpc"],
                      r["sfr_msun_yr"], r["fco_jykms"], r["fco_err"], r["lco"], r["mmol_msun"], r["mstar_msun"],
                      (r["mstar_msun"] + r["mmol_msun"]) if np.isfinite(r["mmol_msun"]) and np.isfinite(r["mstar_msun"]) else np.nan,
                      r["co_ul"], r["fgas"], r["fgas_recomputed"], r["logsmol"], r["logssfr"],
                      g["ra"] if g else np.nan, g["dec"] if g else np.nan, g["zco"] if g else np.nan,
                      int(bool(g) and np.isfinite(g["ra"])), r["co_ul"], int(r["name"] in KNOWN_INCONSISTENT)])
with open(os.path.join(HERE, "phibss13_joined.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    w.writerows(rows_join)
log(f"wrote phibss13_joined.csv: {len(t2)} galaxies; {n_pos} have an optical position from table 1; "
    f"{sum(1 for r in t2 if np.isfinite(r['vrot_kms']))} have Vrot; "
    f"{sum(r['co_ul'] for r in t2)} are CO upper limits")

# ---------------------------------------------------------------- cross-match
mask = np.array([bool(r[21]) for r in rows_join])
pc = SkyCoord([r[18] for r, m in zip(rows_join, mask) if m] * u.deg, [r[19] for r, m in zip(rows_join, mask) if m] * u.deg)
kc = SkyCoord(np.asarray(main["RA"], float) * u.deg, np.asarray(main["DEC"], float) * u.deg)
RADIUS, DZ = 1.5, 0.01


def do_match(pcoords, zco):
    idx, sep, _ = pcoords.match_to_catalog_sky(kc)
    hit = []
    for i, (k, sp) in enumerate(zip(idx, sep.arcsec)):
        if sp < RADIUS and abs(float(main["Z"][k]) - zco[i]) < DZ:
            hit.append((i, int(k), sp))
    return hit


zco_sel = np.array([r[20] for r, m in zip(rows_join, mask) if m])
names_sel = [r[0] for r, m in zip(rows_join, mask) if m]
hit = do_match(pc, zco_sel)
log(f"cross-match (<{RADIUS} arcsec and |dz|<{DZ}): {len(hit)} of {len(pc)} PHIBSS galaxies with positions match a KMOS3D galaxy")

# positive control: the matcher must recover KMOS3D's own positions after 0.3 arcsec of jitter
rng = np.random.default_rng(1)
jit = SkyCoord(kc.ra + rng.normal(0, 0.3, len(kc)) * u.arcsec / np.cos(kc.dec.rad), kc.dec + rng.normal(0, 0.3, len(kc)) * u.arcsec)
i2, s2, _ = jit.match_to_catalog_sky(kc)
n_rec = int(((s2.arcsec < RADIUS) & (i2 == np.arange(len(kc)))).sum())
check(n_rec >= 0.98 * len(kc), f"positive control: {n_rec}/{len(kc)} jittered KMOS3D positions recovered to their own row within {RADIUS} arcsec")
# negative control: shift the PHIBSS positions by 1-2 arcmin in six directions
ctrl = []
for dra, ddec in [(60, 0), (-60, 0), (0, 60), (0, -60), (120, 0), (0, 120)]:
    shifted = SkyCoord(pc.ra + dra * u.arcsec / np.cos(pc.dec.rad), pc.dec + ddec * u.arcsec)
    ctrl.append(len(do_match(shifted, zco_sel)))
log(f"negative control (PHIBSS positions shifted by 1-2 arcmin, six shifts): {ctrl} chance matches")
check(max(ctrl) == 0 or len(hit) > 3 * max(ctrl), "the real match count beats every shifted-position control")
_, nsep, _ = pc.match_to_catalog_sky(kc)
log(f"nearest PHIBSS->KMOS3D separation over all 56 positioned galaxies: {nsep.arcsec.min():.0f} arcsec "
    f"({names_sel[int(np.argmin(nsep.arcsec))]}), i.e. the two surveys do not overlap in the 2013 PHIBSS sample "
    f"(KMOS3D: COSMOS, GOODS-S, UDS only)" if len(hit) == 0 else f"{len(hit)} overlap galaxies")

with open(os.path.join(HERE, "kmos3d_phibss_match.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["phibss_name", "kmos3d_field", "kmos3d_id", "kmos3d_file", "sep_arcsec", "z_kmos3d", "z_co",
                "lmstar_kmos3d", "log10_mstar_phibss", "vrot_kms", "mmol_msun", "mstar_phibss_msun", "phibss_type", "co_upper_limit"])
    lookup = {r[0]: r for r in rows_join}
    for i, k, sp in hit:
        r = lookup[names_sel[i]]
        w.writerow([names_sel[i], s(main["FIELD"][k]), s(main["ID"][k]), s(main["FILE"][k]), round(sp, 3),
                    float(main["Z"][k]), zco_sel[i], float(main["LMSTAR"][k]),
                    round(float(np.log10(r[11])), 3) if np.isfinite(r[11]) else "", r[3], r[10], r[11], r[2], r[22]])
log("wrote kmos3d_phibss_match.csv")

# ---------------------------------------------------------------- manifest
man = {"built_by": "data_assembly/kmos3d_phibss/build.py", "raw_small": {}, "cubes": {}}
src = {
    "k3d_fnlsp_table_v3.fits": "https://www.mpe.mpg.de/resources/KMOS3D/catalogs/k3d_fnlsp_table_v3.fits.tgz (unpacked)",
    "k3d_fnlsp_table_hafits_v3.fits": "https://www.mpe.mpg.de/resources/KMOS3D/catalogs/k3d_fnlsp_table_hafits_v3.fits.tgz (unpacked)",
    "tacconi2013_ReadMe.txt": "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/768/74/ReadMe",
    "tacconi2013_table1.dat": "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/768/74/table1.dat",
    "tacconi2013_table2.dat": "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/768/74/table2.dat",
}
for fn, url in src.items():
    p = os.path.join(RAW, fn)
    man["raw_small"][fn] = dict(url=url, bytes=os.path.getsize(p), sha256=sha256(p))
if "--cubes" in sys.argv:
    cd = sys.argv[sys.argv.index("--cubes") + 1]
    for fn in ["KMOS3D_cubes_COSMOS.tar.gz", "KMOS3D_cubes_GOODSS.tar.gz", "KMOS3D_cubes_UDS.tar.gz"]:
        p = os.path.join(cd, fn)
        if os.path.exists(p):
            man["cubes"][fn] = dict(url="https://www.mpe.mpg.de/resources/KMOS3D/" + fn,
                                    bytes=os.path.getsize(p), sha256=sha256(p))
json.dump(man, open(os.path.join(HERE, "manifest.json"), "w"), indent=2)
log("wrote manifest.json")
write_checks()
