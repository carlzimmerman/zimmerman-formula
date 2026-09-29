#!/usr/bin/env python3
"""Parse three public per-galaxy Tully-Fisher tables (CDS copies) into CSV, with checks.

Inputs (raw_small/, fixed-width, byte ranges from each table's ReadMe):
  ubler2017_table3.dat     Ubler+2017, ApJ 842, 121 (KMOS3D)      CDS J/ApJ/842/121   135 rows
  gogate2020_tablea1/a2    Gogate+2020, MNRAS 496, 3531 (BUDHIES)  CDS J/MNRAS/496/3531  127 + 39 HI rows
  gogate2020_tablea3/a4    same, optical properties                                     127 + 39 rows
  tiley2019_tablea1.dat    Tiley+2019, MNRAS 482, 2166 (KROSS/SAMI) CDS J/MNRAS/482/2166 754 rows

Outputs: ubler2017.csv, budhies_hi.csv, budhies_optical.csv, budhies_joined.csv, tiley2019.csv,
         checks.txt, manifest.json.   No fit, no derived physics beyond unit-free joins.
Usage: python3 build.py
"""
import csv, hashlib, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_small")
LOG = []


def log(m):
    print(m); LOG.append(m)


def check(c, m):
    log(("PASS  " if c else "FAIL  ") + m)
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
        sys.exit("check failed: " + m)


def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()


def fnum(s):
    s = s.strip()
    return float(s) if s else np.nan


def slc(line, a, b):           # ReadMe bytes a-b (1-based inclusive)
    return line[a - 1:b]


def read(fn):
    return [l.rstrip("\n") for l in open(os.path.join(RAW, fn)) if l.strip()]


def write(fn, cols, rows):
    with open(os.path.join(HERE, fn), "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)


def inrange(vals, lo, hi):
    v = np.asarray(vals, float)
    return bool(np.all(np.isfinite(v)) and v.min() >= lo - 1e-9 and v.max() <= hi + 1e-9)


# ------------------------------------------------------------------ Ubler+2017 table 3
rows = []
for l in read("ubler2017_table3.dat"):
    rows.append([int(slc(l, 1, 3)), fnum(slc(l, 5, 9)), fnum(slc(l, 11, 15)), fnum(slc(l, 17, 21)),
                 fnum(slc(l, 23, 27)), fnum(slc(l, 29, 33))])
check(len(rows) == 135, f"Ubler table 3 has 135 rows (got {len(rows)})")
a = np.array(rows, float)
check(list(a[:, 0].astype(int)) == list(range(1, 136)), "Ubler Seq runs 1..135")
# ranges quoted in the ReadMe
check(inrange(a[:, 1], 0.6, 2.6), "Ubler z in the ReadMe range [0.6, 2.6]")
check(inrange(a[:, 2], 9.5, 11.5), "Ubler logM* in [9.5, 11.5]")
check(inrange(a[:, 3], 9.8, 11.7), "Ubler logMb in [9.8, 11.7]")
check(inrange(a[:, 4], 111.6, 476.1), "Ubler Vcirc in [111.6, 476.1] km/s")
check(inrange(a[:, 5], 1.0, 159.0), "Ubler sigma0 in [1, 159] km/s")
check(bool(np.all(a[:, 3] >= a[:, 2] - 1e-9)), "Ubler baryonic mass >= stellar mass for every row")
bins = {"z<1.3": int((a[:, 1] < 1.3).sum()), "1.3<=z<1.8": int(((a[:, 1] >= 1.3) & (a[:, 1] < 1.8)).sum()),
        "z>=1.8": int((a[:, 1] >= 1.8).sum())}
log(f"Ubler rows by redshift: {bins} (the ledger's 65 at z~0.9 and 46 at z~2.3 are the two outer bins; the {bins['1.3<=z<1.8']} intermediate rows are not in the ledger's two bins)")
check(bins["z<1.3"] == 65 and bins["z>=1.8"] == 46, "Ubler bin counts equal the ledger's 65 (z<1.3) and 46 (z>=1.8)")
write("ubler2017.csv", ["seq", "z", "logMstar", "logMbar", "vcirc_max_kms", "sigma0_kms"], rows)

# ------------------------------------------------------------------ Gogate+2020 (BUDHIES)
def coords(l, dsec_end):
    return (int(slc(l, 27, 28)), int(slc(l, 30, 31)), float(slc(l, 33, 37)),
            slc(l, 38, 38), int(slc(l, 39, 40)), int(slc(l, 42, 43)), float(slc(l, 45, dsec_end)))


hi = {}
for cl, fn, n_exp in (("A963", "gogate2020_tablea1.dat", 127), ("A2192", "gogate2020_tablea2.dat", 39)):
    L = read(fn)
    check(len(L) == n_exp, f"BUDHIES {cl} HI table has {n_exp} rows (got {len(L)})")
    for l in L:
        hi[(cl, int(slc(l, 1, 3)))] = [cl, int(slc(l, 1, 3)), slc(l, 5, 25).strip(), *coords(l, 48),
                                        fnum(slc(l, 50, 56)), fnum(slc(l, 58, 63)), fnum(slc(l, 65, 69)),
                                        fnum(slc(l, 71, 74)), fnum(slc(l, 76, 80)), fnum(slc(l, 82, 86)),
                                        fnum(slc(l, 88, 92)), fnum(slc(l, 94, 97)), fnum(slc(l, 99, 103)),
                                        fnum(slc(l, 105, 108)), int(slc(l, 110, 110))]
hicols = ["cluster", "index", "hi_name", "rah", "ram", "ras", "de_sign", "ded", "dem", "des", "z_hi", "dlum_mpc",
          "w20_kms", "e_w20", "w50_kms", "e_w50", "sint_mjykms", "e_sint", "mhi_1e9msun", "e_mhi", "profile_type"]
write("budhies_hi.csv", hicols, list(hi.values()))
H = np.array([[r[10], r[11], r[14], r[18]] for r in hi.values()], float)
check(bool(np.all(H[:, 0] > 0.15) and np.all(H[:, 0] < 0.25)), f"BUDHIES z_hi all within 0.15-0.25 (min {H[:,0].min():.4f}, max {H[:,0].max():.4f})")
check(bool(np.all(np.isfinite(H[:, 2])) and np.all(H[:, 2] > 0)) , "BUDHIES W50 finite and positive for every galaxy")
check(bool(np.all(H[:, 3] > 0)), "BUDHIES HI mass positive for every galaxy")

opt = {}
for cl, fn, n_exp in (("A963", "gogate2020_tablea3.dat", 127), ("A2192", "gogate2020_tablea4.dat", 39)):
    L = read(fn)
    check(len(L) == n_exp, f"BUDHIES {cl} optical table has {n_exp} rows (got {len(L)})")
    for l in L:
        opt[(cl, int(slc(l, 1, 3)))] = [cl, int(slc(l, 1, 3)), slc(l, 5, 25).strip(),
                                         int(slc(l, 51, 53)), fnum(slc(l, 55, 62)), fnum(slc(l, 64, 67)),
                                         slc(l, 68, 68).strip(), fnum(slc(l, 70, 73)), slc(l, 74, 74).strip(),
                                         fnum(slc(l, 76, 79)), fnum(slc(l, 81, 84))]
write("budhies_optical.csv", ["cluster", "index", "hi_name", "pa_deg", "z_opt", "bmag", "bmag_flag", "rmag",
                              "rmag_flag", "fuv_mag", "nuv_mag"], list(opt.values()))
check(set(hi) == set(opt), "BUDHIES HI and optical tables list the same (cluster, index) keys")
# The two tables use different names for the same detection (HI position vs optical counterpart), so the join is
# by the serial number the ReadMe defines. Verify it is a real counterpart match: HI and optical positions agree.
def deg(h, m, s, sg, d, dm, ds):
    return 15 * (h + m / 60 + s / 3600), (-1 if sg == "-" else 1) * (d + dm / 60 + ds / 3600)


sep, dz = [], []
for cl, fn in (("A963", "gogate2020_tablea3.dat"), ("A2192", "gogate2020_tablea4.dat")):
    for l in read(fn):
        k = (cl, int(slc(l, 1, 3)))
        ro, do = deg(*coords(l, 49))
        rh, dh = deg(*hi[k][3:10])
        sep.append(3600 * np.hypot((ro - rh) * np.cos(np.radians(dh)), do - dh))
        zo = fnum(slc(l, 55, 62))
        if zo and zo > 0:
            dz.append(abs(zo - hi[k][10]))
sep = np.array(sep); dz = np.array(dz)
log(f"BUDHIES HI-vs-optical position separation: median {np.median(sep):.1f} arcsec, max {sep.max():.1f} arcsec over {len(sep)} galaxies")
check(bool(sep.max() < 30), "BUDHIES HI and optical positions agree to < 30 arcsec for every galaxy (the join by serial number is a real match)")
log(f"BUDHIES |z_opt - z_hi| over {len(dz)} galaxies with an optical redshift: median {np.median(dz):.5f}, max {dz.max():.5f}")
# One documented mismatch: A963 #68 has z_hi = 0.19947 but a literature optical z of 0.12 (a different object, or a poor
# optical redshift). It is KEPT and FLAGGED, never dropped or corrected.
zopt_by_key = {}
for cl, fn in (("A963", "gogate2020_tablea3.dat"), ("A2192", "gogate2020_tablea4.dat")):
    for l in read(fn):
        zopt_by_key[(cl, int(slc(l, 1, 3)))] = fnum(slc(l, 55, 62))
ZMIS = sorted(k for k, zo in zopt_by_key.items() if zo > 0 and abs(zo - hi[k][10]) > 0.005)
check(ZMIS == [("A963", 68)], f"exactly one BUDHIES galaxy has |z_opt - z_hi| > 0.005: A963 #68 (found {ZMIS})")
J = []
for k in hi:
    o = opt[k]
    J.append(hi[k] + [o[3], o[4], o[5], o[6], o[7], o[8], int(k in ZMIS)])
write("budhies_joined.csv", hicols + ["pa_deg", "z_opt", "bmag", "bmag_flag", "rmag", "rmag_flag", "z_opt_hi_mismatch_flag"], J)
log(f"BUDHIES joined: {len(J)} galaxies; with an optical redshift: {sum(1 for r in J if r[-6] and r[-6] > 0)}; "
    f"B or R magnitude flagged as converted from SDSS: {sum(1 for r in J if r[-4] == '*' or r[-2] == '*')}")

# ------------------------------------------------------------------ Tiley+2019
T = []
for l in read("tiley2019_tablea1.dat"):
    p = l.split()
    check(len(p) == 9, f"Tiley row has 9 whitespace fields (ID {p[1] if len(p) > 1 else '?'})") if len(p) != 9 else None
    T.append([p[0], int(p[1]), int(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[6]), float(p[7]), float(p[8])])
check(len(T) == 754, f"Tiley table A1 has 754 rows (got {len(T)})")
import collections
cnt = collections.Counter(r[0] for r in T)
log(f"Tiley rows by survey: {dict(cnt)}")
check(set(cnt) == {"KROSS", "SAMI_matched", "SAMI_original"}, "Tiley surveys are exactly KROSS, SAMI_matched, SAMI_original")
check(all(r[2] in (0, 1) for r in T), "Tiley sub-sample flag is 0 or 1 for every row")
write("tiley2019.csv", ["survey", "id", "flag_disky", "logv22_kms", "e_logv22", "logMstar", "e_logMstar", "kmag_vega",
                        "e_kmag"], T)

# ------------------------------------------------------------------ manifest
man = {"built_by": "data_assembly/high_z_tf_tables/build.py", "raw_small": {}}
url = {"ubler2017_table3.dat": "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/842/121/table3.dat",
       "ubler2017_ReadMe.txt": "https://cdsarc.cds.unistra.fr/ftp/J/ApJ/842/121/ReadMe",
       "tiley2019_tablea1.dat": "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/482/2166/tablea1.dat",
       "tiley2019_ReadMe.txt": "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/482/2166/ReadMe",
       "gogate2020_ReadMe.txt": "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/496/3531/ReadMe"}
for t in ("tablea1", "tablea2", "tablea3", "tablea4"):
    url[f"gogate2020_{t}.dat"] = f"https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/496/3531/{t}.dat"
for fn in sorted(os.listdir(RAW)):
    p = os.path.join(RAW, fn)
    man["raw_small"][fn] = {"url": url[fn], "bytes": os.path.getsize(p), "sha256": sha(p)}
json.dump(man, open(os.path.join(HERE, "manifest.json"), "w"), indent=2)
log("wrote manifest.json")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
