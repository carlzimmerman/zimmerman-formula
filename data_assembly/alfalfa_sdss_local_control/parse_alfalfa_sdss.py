#!/usr/bin/env python3
"""Parse the ALFALFA-SDSS Galaxy Catalog (Durbala+ 2020) joined to the ALFALFA alpha.100 HI catalogue (Haynes+ 2018).

DATA GATHERING ONLY.  This script parses and merges published tables; it computes no accelerations, no a0, no rotation
velocities, no baryonic masses and runs no gravity test.  (The `--checks` mode recomputes two catalogue-internal identities,
log M_HI = log10(2.356e5 D^2 S21) and the iMAG definition, purely to verify what the catalogue's columns mean.)

Inputs (all fetched with data_assembly/fetch_logged.py into DATA_DIR; sha256 verified before parsing):
  durbala2020_table1.dat.gz        VizieR J/AJ/160/271/table1.dat   (31,501 rows, fixed width, 103 bytes/line)
  durbala2020_table2.dat.gz        VizieR J/AJ/160/271/table2.dat   (31,501 rows, fixed width, 122 bytes/line)
  haynes2018_a100_table2.dat.gz    VizieR J/ApJ/861/49/table2.dat   (31,502 rows, fixed width, 113 bytes/line, Aug-2019 corrected)
Optional inputs used only by `--checks` (cross-version verification; the CSV does not depend on them):
  durbala2020-table1.21-Sep-2020.fits.gz, durbala2020-table2.21-Sep-2020.fits.gz   (Cornell archive, float64 originals)
  a100.code12.table2.190808.csv                                                    (Cornell archive, decimal-degree twin)

Output: alfalfa_sdss.csv, one row per AGC number (outer join of the three tables, ascending AGC).  Every value is the
catalogue's own decimal text (stripped of padding), so no rounding is introduced; missing = empty field.  The only derived
values are the four sky-position pairs for the alpha.100 sexagesimal coordinates (converted to decimal degrees, 6 decimals).

Usage:
  python3 parse_alfalfa_sdss.py                 # (re)build alfalfa_sdss.csv next to this script
  python3 parse_alfalfa_sdss.py --checks        # build, then print the sanity checks quoted in README.md
  python3 parse_alfalfa_sdss.py --verify        # rebuild in memory and confirm byte-for-byte identity with the file on disk
  options: --data-dir DIR   (default <repo-parent>/_external_data/alfalfa_sdss, located relative to this script)   --out FILE
Only the Python standard library is used; re-running reproduces the CSV byte-for-byte (UTF-8, LF line ends).
"""
import argparse
import collections
import csv
import gzip
import hashlib
import io
import math
import os
import re
import statistics
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data", "alfalfa_sdss"))   # <repo-parent>/_external_data/alfalfa_sdss
DEFAULT_OUT = os.path.join(HERE, "alfalfa_sdss.csv")

# --- fetched files and their sha256 (from data_assembly/FETCH_MANIFEST_2026-10-01.jsonl) -------------------------------
REQUIRED = {
    "durbala2020_table1.dat.gz": "21e7e51ea9f75ceab6c039fe56e86ee6669f0323b173453b0b5da73173cfbcee",
    "durbala2020_table2.dat.gz": "216e96b97fb12eda3dff7c937775be9d384697dd5eaab4b5fd839f71c926031e",
    "haynes2018_a100_table2.dat.gz": "85d4c299ea6cceea61f9b016a1b6c93cbbd9603a2f72aa1a11f12789f3abd31a",
}
OPTIONAL = {
    "durbala2020-table1.21-Sep-2020.fits.gz": "73cf97effac6fbf1676c330d7648ccb45cf1e2b11414a12b72036c758d7cf917",
    "durbala2020-table2.21-Sep-2020.fits.gz": "1423c29717aff27e58dad2b7f4fb6055878866f06188cb08a35055ee9438d32e",
    "a100.code12.table2.190808.csv": "a029d2786d0c41098777f1c2a17d2a4c993d1654a5144618b7998a537d6bdcd6",
}

# --- byte-by-byte layouts, copied from the two VizieR ReadMe files (1-based inclusive byte ranges) ----------------------
T1_SPEC = [("agc", 1, 6), ("flag", 8, 8), ("objid", 10, 29), ("ra", 31, 40), ("dec", 42, 49), ("rvel", 51, 55),
           ("dist", 57, 61), ("e_dist", 63, 66), ("gext", 68, 71), ("iext", 73, 76), ("ba", 78, 81), ("e_ba", 83, 88),
           ("imag", 90, 94), ("e_imag", 96, 103)]
T2_SPEC = [("agc", 1, 6), ("gam_g", 8, 11), ("gam_i", 13, 16), ("imag_abs", 18, 23), ("e_imag_abs", 25, 29),
           ("gi", 31, 35), ("e_gi", 37, 42), ("ms_t", 44, 48), ("e_ms_t", 50, 55), ("ms_m", 57, 61), ("e_ms_m", 63, 66),
           ("ms_g", 68, 72), ("e_ms_g", 74, 77), ("sfr22", 79, 83), ("e_sfr22", 85, 88), ("sfrn", 90, 94),
           ("e_sfrn", 96, 100), ("sfrg", 102, 106), ("e_sfrg", 108, 111), ("mhi", 113, 117), ("e_mhi", 119, 122)]
A100_SPEC = [("agc", 1, 6), ("name", 8, 15), ("rah", 17, 18), ("ram", 19, 20), ("ras", 21, 24), ("des", 25, 25),
             ("ded", 26, 27), ("dem", 28, 29), ("dess", 30, 31), ("orah", 33, 34), ("oram", 35, 36), ("oras", 37, 40),
             ("odes", 41, 41), ("oded", 42, 43), ("odem", 44, 45), ("odess", 46, 47), ("vhel", 49, 53), ("w50", 55, 57),
             ("e_w50", 59, 61), ("w20", 63, 65), ("s21", 67, 72), ("e_s21", 74, 77), ("snr", 79, 83), ("rms", 85, 89),
             ("dist", 91, 95), ("e_dist", 97, 100), ("mhi", 102, 106), ("e_mhi", 108, 111), ("code", 113, 113)]
OBJID_SENTINEL = "-9223372036854775808"   # int64 minimum written by the catalogue where there is no SDSS counterpart

# --- output columns (name, unit, one-line meaning); the full dictionary is columns.md ---------------------------------
COLUMNS = [
    ("agc", "-", "AGC catalogue number (<100000 = UGC number)"),
    ("in_durbala2020", "0/1", "row present in Durbala+2020 tables 1-2"),
    ("in_a100_table2", "0/1", "row present in Haynes+2018 table 2 (Aug-2019 corrected version)"),
    ("name_oc", "-", "common name of the optical counterpart (alpha.100)"),
    ("sdss_objid", "-", "SDSS DR15 objID of the optical counterpart (empty if none)"),
    ("sdss_phot_flag", "0-3", "photometry flag: 0 outside footprint, 1 good, 2 g/i error >0.05, 3 no counterpart"),
    ("ra_dur_deg", "deg", "RA J2000, optical counterpart (or HI centroid if none), Durbala table 1"),
    ("dec_dur_deg", "deg", "Dec J2000, same"),
    ("ra_hi_deg", "deg", "RA J2000 of the HI centroid (alpha.100, converted from h m s)"),
    ("dec_hi_deg", "deg", "Dec J2000 of the HI centroid (alpha.100, converted from d m s)"),
    ("ra_oc_deg", "deg", "RA J2000 of the alpha.100 optical counterpart (converted)"),
    ("dec_oc_deg", "deg", "Dec J2000 of the alpha.100 optical counterpart (converted)"),
    ("vhel_kms", "km/s", "heliocentric velocity of the HI profile midpoint (optical convention)"),
    ("dist_mpc", "Mpc", "adopted (Hubble/flow-model/primary/group) distance"),
    ("e_dist_mpc", "Mpc", "uncertainty in dist_mpc"),
    ("s21_jykms", "Jy km/s", "integrated HI line flux density S21"),
    ("e_s21_jykms", "Jy km/s", "uncertainty in S21"),
    ("w50_kms", "km/s", "HI velocity width at 50% of the peak (instrumental-broadening corrected only)"),
    ("e_w50_kms", "km/s", "uncertainty in W50"),
    ("w20_kms", "km/s", "HI velocity width at 20% of the peak (0 appears to mean missing)"),
    ("snr", "-", "signal-to-noise ratio of the detection"),
    ("rms_mjy", "mJy", "rms noise of the extracted spectrum at 10 km/s resolution"),
    ("hi_code", "1/2", "HI source code: 1 = high quality, 2 = 'prior' (lower S/N, coincident optical redshift)"),
    ("logmhi", "log Msun", "log10 HI mass = log10(2.356e5 D^2 S21)"),
    ("e_logmhi", "dex", "uncertainty in logmhi"),
    ("gext_mag", "mag", "foreground Galactic extinction in SDSS g"),
    ("iext_mag", "mag", "foreground Galactic extinction in SDSS i"),
    ("ba_r", "-", "axis ratio b/a, SDSS r band (expAB_r)"),
    ("e_ba_r", "-", "uncertainty in b/a (SDSS pipeline value; a few absurdly large)"),
    ("imag_cmodel", "mag", "SDSS i-band cmodel magnitude (apparent; NOT extinction corrected)"),
    ("e_imag_cmodel", "mag", "uncertainty in imag_cmodel (SDSS pipeline value)"),
    ("gamma_g", "mag", "internal-extinction coefficient gamma_g (A_int = gamma * log10(a/b)); VizieR label Ag"),
    ("gamma_i", "mag", "internal-extinction coefficient gamma_i; VizieR label Ai"),
    ("imag_abs_corr", "mag", "absolute i magnitude, cmodel, Galactic+internal extinction corrected (iMAG)"),
    ("e_imag_abs_corr", "mag", "uncertainty in iMAG"),
    ("gi_corr", "mag", "(g-i) colour, Galactic+internal extinction corrected"),
    ("e_gi_corr", "mag", "uncertainty in (g-i)"),
    ("logms_taylor", "log Msun", "stellar mass, Taylor+2011 colour method (uncorrected for the GSWLC offset)"),
    ("e_logms_taylor", "dex", "uncertainty in logms_taylor"),
    ("logms_mcgaugh", "log Msun", "stellar mass, McGaugh & Schombert 2015 unWISE W1 method"),
    ("e_logms_mcgaugh", "dex", "uncertainty in logms_mcgaugh"),
    ("logms_gswlc", "log Msun", "stellar mass from GSWLC-2 (SED fit), where available"),
    ("e_logms_gswlc", "dex", "uncertainty in logms_gswlc"),
    ("logsfr22", "log Msun/yr", "SFR from unWISE 22 micron"),
    ("e_logsfr22", "dex", "uncertainty in logsfr22"),
    ("logsfr_nuvir", "log Msun/yr", "SFR from GALEX NUV corrected with 22 micron (VizieR label logSFRN)"),
    ("e_logsfr_nuvir", "dex", "uncertainty in logsfr_nuvir"),
    ("logsfr_gswlc", "log Msun/yr", "SFR from GSWLC-2, where available"),
    ("e_logsfr_gswlc", "dex", "uncertainty in logsfr_gswlc"),
]
COLNAMES = [c[0] for c in COLUMNS]

# Published numbers the row counts are compared with (see README.md for the sources).
PUBLISHED = {
    "durbala_rows": 31501,
    "a100_rows": 31502,
    "durbala_flag_readme": {"0": 1296, "1": 28267, "2": 1371, "3": 567},      # VizieR ReadMe, Note (1) of table1
    "durbala_flag_arxiv_v1": {"0": 1296, "1": 28057, "2": 1361, "3": 787},    # arXiv:2011.02588v1 text, Section 2.1
    "a100_code": {"1": 25434, "2": 6068},                                       # Haynes+2018 Section 3.1, column 13
}


# --- small helpers -----------------------------------------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_inputs(data_dir, names, strict):
    for name, want in names.items():
        path = os.path.join(data_dir, name)
        if not os.path.exists(path):
            if strict:
                sys.exit(f"missing input file: {path}")
            continue
        got = sha256_file(path)
        if got != want:
            sys.exit(f"sha256 mismatch for {name}: got {got}, expected {want}")


def read_fixed(path, spec):
    """Return {agc: {label: stripped text}} for a gzip'd CDS fixed-width table (1-based inclusive byte ranges)."""
    out = {}
    with gzip.open(path, "rt", encoding="ascii", newline="") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            rec = {lab: line[a - 1:b].strip() for lab, a, b in spec}
            agc = int(rec["agc"])
            if agc in out:
                sys.exit(f"duplicate AGC {agc} in {path}")
            out[agc] = rec
    return out


def sexagesimal_to_deg_text(h, m, s, sign=None, ra=True):
    """h/m/s (RA) or sign,d,m,s (Dec) text -> decimal degrees text with 6 decimals; '' if the fields are empty."""
    if h == "" or m == "" or s == "":
        return ""
    if ra:
        v = 15.0 * (int(h) + int(m) / 60.0 + float(s) / 3600.0)
    else:
        v = int(h) + int(m) / 60.0 + int(s) / 3600.0
        if sign == "-":
            v = -v
    if abs(v) < 5e-7:
        v = 0.0                                           # avoid '-0.000000'
    return "%.6f" % v


def build_rows(data_dir):
    verify_inputs(data_dir, REQUIRED, strict=True)
    t1 = read_fixed(os.path.join(data_dir, "durbala2020_table1.dat.gz"), T1_SPEC)
    t2 = read_fixed(os.path.join(data_dir, "durbala2020_table2.dat.gz"), T2_SPEC)
    a1 = read_fixed(os.path.join(data_dir, "haynes2018_a100_table2.dat.gz"), A100_SPEC)
    if set(t1) != set(t2):
        sys.exit("Durbala table1 and table2 do not list the same AGC numbers")
    rows = []
    for agc in sorted(set(t1) | set(a1)):
        d1, d2, h = t1.get(agc), t2.get(agc), a1.get(agc)
        r = dict.fromkeys(COLNAMES, "")
        r["agc"] = str(agc)
        r["in_durbala2020"] = "1" if d1 else "0"
        r["in_a100_table2"] = "1" if h else "0"
        if d1:
            r["sdss_objid"] = "" if d1["objid"] == OBJID_SENTINEL else d1["objid"]
            r["sdss_phot_flag"] = d1["flag"]
            r["ra_dur_deg"], r["dec_dur_deg"] = d1["ra"], d1["dec"]
            r["gext_mag"], r["iext_mag"] = d1["gext"], d1["iext"]
            r["ba_r"], r["e_ba_r"] = d1["ba"], d1["e_ba"]
            r["imag_cmodel"], r["e_imag_cmodel"] = d1["imag"], d1["e_imag"]
            # overlapping columns: identical in Durbala and alpha.100 wherever both exist (checked in --checks);
            # alpha.100 is the primary source, Durbala fills only the row that alpha.100 lacks (AGC 2023).
            r["vhel_kms"], r["dist_mpc"], r["e_dist_mpc"] = d1["rvel"], d1["dist"], d1["e_dist"]
        if d2:
            r["gamma_g"], r["gamma_i"] = d2["gam_g"], d2["gam_i"]
            r["imag_abs_corr"], r["e_imag_abs_corr"] = d2["imag_abs"], d2["e_imag_abs"]
            r["gi_corr"], r["e_gi_corr"] = d2["gi"], d2["e_gi"]
            r["logms_taylor"], r["e_logms_taylor"] = d2["ms_t"], d2["e_ms_t"]
            r["logms_mcgaugh"], r["e_logms_mcgaugh"] = d2["ms_m"], d2["e_ms_m"]
            r["logms_gswlc"], r["e_logms_gswlc"] = d2["ms_g"], d2["e_ms_g"]
            r["logsfr22"], r["e_logsfr22"] = d2["sfr22"], d2["e_sfr22"]
            r["logsfr_nuvir"], r["e_logsfr_nuvir"] = d2["sfrn"], d2["e_sfrn"]
            r["logsfr_gswlc"], r["e_logsfr_gswlc"] = d2["sfrg"], d2["e_sfrg"]
            r["logmhi"], r["e_logmhi"] = d2["mhi"], d2["e_mhi"]
        if h:
            r["name_oc"] = h["name"]
            r["ra_hi_deg"] = sexagesimal_to_deg_text(h["rah"], h["ram"], h["ras"], ra=True)
            r["dec_hi_deg"] = sexagesimal_to_deg_text(h["ded"], h["dem"], h["dess"], sign=h["des"], ra=False)
            r["ra_oc_deg"] = sexagesimal_to_deg_text(h["orah"], h["oram"], h["oras"], ra=True)
            r["dec_oc_deg"] = sexagesimal_to_deg_text(h["oded"], h["odem"], h["odess"], sign=h["odes"], ra=False)
            r["vhel_kms"], r["dist_mpc"], r["e_dist_mpc"] = h["vhel"], h["dist"], h["e_dist"]
            r["s21_jykms"], r["e_s21_jykms"] = h["s21"], h["e_s21"]
            r["w50_kms"], r["e_w50_kms"], r["w20_kms"] = h["w50"], h["e_w50"], h["w20"]
            r["snr"], r["rms_mjy"], r["hi_code"] = h["snr"], h["rms"], h["code"]
            r["logmhi"], r["e_logmhi"] = h["mhi"], h["e_mhi"]
        rows.append([r[c] for c in COLNAMES])
    return rows


def csv_bytes(rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLNAMES)
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


# --- sanity checks -----------------------------------------------------------------------------------------------
def num(x):
    return None if x == "" else float(x)


def pctl(xs, q):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    k = (len(xs) - 1) * q / 100.0
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def summ(xs):
    return (f"n={len(xs)} median={statistics.median(xs):.4g} p16={pctl(xs, 16):.4g} p84={pctl(xs, 84):.4g} "
            f"min={min(xs):.4g} max={max(xs):.4g}")


def read_fits_bintable(path):
    """Minimal pure-Python reader for a gzip'd FITS file with one BINTABLE extension (types K,J,D,E,I,B)."""
    with gzip.open(path, "rb") as f:
        raw = f.read()

    def header(pos):
        cards = []
        while True:
            blk = raw[pos:pos + 2880]
            pos += 2880
            if len(blk) < 2880:
                sys.exit(f"truncated FITS header in {path}")
            for i in range(0, 2880, 80):
                card = blk[i:i + 80].decode("ascii")
                if card[:8].strip() == "END":
                    return cards, pos
                cards.append(card)

    _, pos = header(0)                                   # primary HDU (no data; NAXIS = 0)
    cards, pos = header(pos)
    kv = {}
    for c in cards:
        if c[8:10] != "= ":
            continue
        m = re.match(r"\s*'([^']*)'", c[10:])
        kv[c[:8].strip()] = m.group(1).strip() if m else c[10:].split("/")[0].strip()
    nrow, rowlen, nf = int(kv["NAXIS2"]), int(kv["NAXIS1"]), int(kv["TFIELDS"])
    codes = {"K": "q", "J": "i", "D": "d", "E": "f", "I": "h", "B": "B"}
    names, fmt = [], ">"
    for i in range(1, nf + 1):
        tf = re.match(r"(\d*)([A-Z])", kv[f"TFORM{i}"])
        if tf.group(1) not in ("", "1") or tf.group(2) not in codes:
            sys.exit(f"unsupported TFORM{i}={kv[f'TFORM{i}']} in {path}")
        names.append(kv[f"TTYPE{i}"])
        fmt += codes[tf.group(2)]
    if struct.calcsize(fmt) != rowlen:
        sys.exit(f"row length mismatch in {path}")
    cols = {n: [] for n in names}
    for i in range(nrow):
        vals = struct.unpack_from(fmt, raw, pos + i * rowlen)
        for n, v in zip(names, vals):
            cols[n].append(v)
    return cols


def run_checks(csv_path, data_dir):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    P = print
    P(f"# sanity checks on {os.path.basename(csv_path)}  (sha256 {sha256_file(csv_path)})")

    P("\n## 1. row counts")
    both = sum(1 for r in rows if r["in_durbala2020"] == "1" and r["in_a100_table2"] == "1")
    donly = [r["agc"] for r in rows if r["in_durbala2020"] == "1" and r["in_a100_table2"] == "0"]
    honly = [r["agc"] for r in rows if r["in_durbala2020"] == "0" and r["in_a100_table2"] == "1"]
    P(f"rows (union of AGC numbers) = {n}; in both = {both}; Durbala only = {len(donly)} (AGC {', '.join(donly)}); "
      f"alpha.100 only = {len(honly)} (AGC {', '.join(honly)})")
    P(f"Durbala rows = {sum(1 for r in rows if r['in_durbala2020'] == '1')} (published {PUBLISHED['durbala_rows']}); "
      f"alpha.100 rows = {sum(1 for r in rows if r['in_a100_table2'] == '1')} (published {PUBLISHED['a100_rows']})")
    fl = collections.Counter(r["sdss_phot_flag"] for r in rows if r["sdss_phot_flag"] != "")
    P(f"sdss_phot_flag counts {dict(sorted(fl.items()))}; VizieR ReadMe {PUBLISHED['durbala_flag_readme']}; "
      f"arXiv v1 text {PUBLISHED['durbala_flag_arxiv_v1']}")
    nobj = sum(1 for r in rows if r["sdss_objid"] != "")
    P(f"rows with an SDSS objID = {nobj} (flags 1+2 = {fl['1'] + fl['2']}); arXiv v1 text quoted 29,418")
    code = collections.Counter(r["hi_code"] for r in rows if r["hi_code"] != "")
    ncode = sum(code.values())
    P(f"hi_code counts {dict(sorted(code.items()))} (published {PUBLISHED['a100_code']}); fraction code 1 = "
      f"{code['1'] / ncode:.4f} of {ncode}")

    P("\n## 2. HI widths and fluxes (alpha.100 rows)")
    h = [r for r in rows if r["in_a100_table2"] == "1"]
    w50 = [num(r["w50_kms"]) for r in h]
    P(f"W50 [km/s]: {summ(w50)}")
    for c in ("1", "2"):
        P(f"  code {c}: W50 {summ([num(r['w50_kms']) for r in h if r['hi_code'] == c])}")
    P(f"S21 [Jy km/s]: {summ([num(r['s21_jykms']) for r in h if num(r['s21_jykms']) > 0 and num(r['s21_jykms']) < 900])} "
      f"(excluding S21 <= 0 and the 999.9 placeholder)")
    P(f"SNR: {summ([num(r['snr']) for r in h])}")
    P(f"logMHI: {summ([num(r['logmhi']) for r in h])}")
    P(f"Vhel [km/s]: {summ([num(r['vhel_kms']) for r in h])}; dist [Mpc]: {summ([num(r['dist_mpc']) for r in h])}")

    P("\n## 3. log M_HI = log10(2.356e5 D^2 S21) against the catalogue logMHI")
    dev, bad_env = [], []
    for r in h:
        s, d, m = num(r["s21_jykms"]), num(r["dist_mpc"]), num(r["logmhi"])
        if s == 0:
            continue
        s = abs(s)                                  # AGC 715637 has S21 = -7.61 with logMHI of +7.61 (sign glitch)
        pred = math.log10(2.356e5 * d * d * s)
        env = 0.005 + 2 * abs(math.log10(max(1 - 0.05 / d, 1e-9))) + abs(math.log10(max(1 - 0.005 / s, 1e-9)))
        dev.append((abs(pred - m), r["agc"], pred - m, env, d, s))
        if abs(pred - m) > env:
            bad_env.append((r["agc"], pred - m, env))
    dev.sort(reverse=True)
    P(f"rows checked = {len(dev)}; max |deviation| = {dev[0][0]:.4f} dex at AGC {dev[0][1]} "
      f"(its distance rounding envelope is {dev[0][3]:.3f} dex); median = {statistics.median(x[0] for x in dev):.4f}; "
      f"p99 = {pctl([x[0] for x in dev], 99):.4f}; rows outside the rounding envelope "
      f"(0.005 + 2|log10(1-0.05/D)| + |log10(1-0.005/S21)|) = {len(bad_env)}")
    P("top 5 deviations: " + "; ".join(f"AGC {a} {d:+.4f} (envelope {e:.3f})" for _, a, d, e, _, _ in dev[:5]))
    far = [x for x in dev if x[4] >= 10 and x[5] >= 0.5]
    P(f"rows with D >= 10 Mpc and S21 >= 0.5 Jy km/s: n = {len(far)}, max |deviation| = {max(x[0] for x in far):.4f} dex, "
      f"median = {statistics.median(x[0] for x in far):.4f} dex")
    P("  (the catalogue publishes D to 0.1 Mpc, S21 to 0.01 Jy km/s and logMHI to 0.01 dex, so the identity can only be "
      "verified to that rounding)")
    neg = [(r["agc"], r["s21_jykms"], r["logmhi"], r["w20_kms"]) for r in h if num(r["s21_jykms"]) <= 0]
    big = [(r["agc"], r["s21_jykms"], r["logmhi"], r["dist_mpc"], r["vhel_kms"]) for r in h if num(r["s21_jykms"]) >= 900]
    P(f"S21 <= 0 rows (agc, S21, logMHI, W20): {neg}")
    P(f"S21 >= 900 rows (agc, S21, logMHI, D, Vhel): {big}")
    ee = []
    for r in h:
        s, es, d, ed, e = (num(r[k]) for k in ("s21_jykms", "e_s21_jykms", "dist_mpc", "e_dist_mpc", "e_logmhi"))
        if 0 < s < 900:
            ee.append(abs(math.sqrt((es / s) ** 2 + (2 * ed / d) ** 2 + 0.01) / math.log(10) - e))
    P(f"Haynes+2018 Eq. 5 for e_logMHI: median |deviation| = {statistics.median(ee):.4f}, max = {max(ee):.4f} dex")

    P("\n## 4. optical columns")
    f1 = [r for r in rows if r["sdss_phot_flag"] == "1"]
    P(f"(g-i)_corr [mag], flag 1 rows: {summ([num(r['gi_corr']) for r in f1])}")
    for c in ("1", "2"):
        P(f"  flag 1 & HI code {c}: {summ([num(r['gi_corr']) for r in f1 if r['hi_code'] == c])}")
    P(f"iMAG [mag], flag 1: {summ([num(r['imag_abs_corr']) for r in f1])}")
    P(f"i_cmodel [mag], flag 1: {summ([num(r['imag_cmodel']) for r in f1])}")
    P(f"b/a (SDSS expAB_r), flag 1: {summ([num(r['ba_r']) for r in f1])}")
    P(f"logM*_Taylor, flag 1: {summ([num(r['logms_taylor']) for r in f1])}; logM*_McGaugh: "
      f"{summ([num(r['logms_mcgaugh']) for r in rows if r['logms_mcgaugh'] != ''])}; logM*_GSWLC: "
      f"{summ([num(r['logms_gswlc']) for r in rows if r['logms_gswlc'] != ''])}")
    for a_name, a_col in (("Taylor", "logms_taylor"), ("McGaugh", "logms_mcgaugh")):
        dd = [num(r["logms_gswlc"]) - num(r[a_col]) for r in rows if r[a_col] != "" and r["logms_gswlc"] != ""]
        P(f"stellar-mass offset, median(logM_GSWLC - logM_{a_name}) = {statistics.median(dd):+.3f} dex over {len(dd)} rows "
          f"(p16 {pctl(dd, 16):+.3f}, p84 {pctl(dd, 84):+.3f}); the table holds the raw method values")
    chk = []
    for r in f1:
        if r["imag_abs_corr"] == "":
            continue
        pred = (num(r["imag_cmodel"]) - num(r["iext_mag"]) - num(r["gamma_i"]) * math.log10(1.0 / num(r["ba_r"]))
                - 5 * math.log10(num(r["dist_mpc"])) - 25)
        chk.append(abs(pred - num(r["imag_abs_corr"])))
    P(f"iMAG definition check, iMAG = i_cmodel - iext - gamma_i*log10(a/b) - 5log10(D/Mpc) - 25: n = {len(chk)}, "
      f"median |dev| = {statistics.median(chk):.4f}, max = {max(chk):.4f} mag (rounding-limited)")
    gm = [r for r in rows if r["gamma_i"] != ""]
    faint = [r for r in gm if num(r["imag_abs_corr"]) > -17.0]
    bright = [r for r in gm if num(r["imag_abs_corr"]) < -18.0]
    P(f"gamma_i behaviour: rows with iMAG > -17: {len(faint)}, of which gamma_i = 0: "
      f"{sum(1 for r in faint if num(r['gamma_i']) == 0)}; rows with iMAG < -18: {len(bright)}, of which gamma_i > 0: "
      f"{sum(1 for r in bright if num(r['gamma_i']) > 0)} (D20 eq. 1: gamma = 0 fainter than -17, rising linearly above)")
    pres = collections.Counter()
    for r in rows:
        pres[(r["sdss_phot_flag"], r["imag_abs_corr"] != "", r["logms_taylor"] != "")] += 1
    P("derived optical columns present by flag (flag, iMAG present, Taylor mass present): "
      + "; ".join(f"{k}: {v}" for k, v in sorted(pres.items())))

    P("\n## 5. missing values per column (empty fields), of %d rows" % n)
    for c in COLNAMES:
        P(f"  {c:18s} {sum(1 for r in rows if r[c] == ''):6d}")

    key = ("w50_kms", "s21_jykms", "hi_code", "dist_mpc", "logmhi", "ba_r", "gi_corr", "imag_abs_corr", "logms_taylor")
    full = [r for r in rows if all(r[k] != "" for k in key)]
    P(f"rows with ALL of {', '.join(key)} present: {len(full)} (HI code 1: {sum(1 for r in full if r['hi_code'] == '1')}, "
      f"code 2: {sum(1 for r in full if r['hi_code'] == '2')}); these are exactly the sdss_phot_flag = 1 rows: "
      f"{len(full) == fl['1'] and all(r['sdss_phot_flag'] == '1' for r in full)}")

    P("\n## 6. oddities kept as published")
    P(f"W20 = 0: {sum(1 for r in h if r['w20_kms'] == '0')} rows; W20 < W50: "
      f"{sum(1 for r in h if num(r['w20_kms']) < num(r['w50_kms']))} rows (of which W20 = 0: "
      f"{sum(1 for r in h if r['w20_kms'] == '0')}); e_dist = 0.0: "
      f"{[r['agc'] for r in rows if r['e_dist_mpc'] == '0.0']}")
    P(f"hi_code 2 with SNR < 3: {sum(1 for r in h if r['hi_code'] == '2' and num(r['snr']) < 3)}; "
      f"e_ba_r > 1: {sum(1 for r in rows if r['e_ba_r'] != '' and num(r['e_ba_r']) > 1)}; "
      f"e_imag_cmodel > 1: {sum(1 for r in rows if r['e_imag_cmodel'] != '' and num(r['e_imag_cmodel']) > 1)}")
    P(f"Vhel < 2000 km/s: {sum(1 for r in h if num(r['vhel_kms']) < 2000)}; Vhel > 6000: "
      f"{sum(1 for r in h if num(r['vhel_kms']) > 6000)}; Vhel > 15000: {sum(1 for r in h if num(r['vhel_kms']) > 15000)}")
    oc = collections.Counter(r["sdss_objid"] for r in rows if r["sdss_objid"] != "")
    dup = sorted(k for k, v in oc.items() if v > 1)
    P(f"SDSS objIDs shared by two AGC rows: {len(dup)} objIDs ({sum(oc[k] for k in dup)} rows); AGC pairs: "
      + "; ".join("/".join(r["agc"] for r in rows if r["sdss_objid"] == k) for k in dup))
    P(f"alpha.100 rows without an optical counterpart position (ra_oc_deg empty): "
      f"{sum(1 for r in h if r['ra_oc_deg'] == '')}, all with sdss_phot_flag "
      f"{sorted(set(r['sdss_phot_flag'] for r in h if r['ra_oc_deg'] == ''))}; flag-3 rows overall: {fl['3']}")
    P(f"name_oc beginning 'VCC' (Virgo Cluster Catalogue designation, a partial Virgo indicator only): "
      f"{sum(1 for r in rows if r['name_oc'].startswith('VCC'))}")
    dc = collections.Counter((r["dist_mpc"], r["e_dist_mpc"]) for r in h)
    P("most common (dist, e_dist) pairs, i.e. group / Virgo-substructure assignments (no flag column exists): "
      + "; ".join(f"{k[0]}+-{k[1]} x{v}" for k, v in dc.most_common(10)))
    for tag, sel in (("Vhel > 6000", [r for r in h if num(r["vhel_kms"]) > 6000]),
                     ("Vhel <= 6000", [r for r in h if num(r["vhel_kms"]) <= 6000])):
        k = sum(1 for r in sel if abs(num(r["dist_mpc"]) - num(r["vhel_kms"]) / 70.0) <= 5.5)
        P(f"distance recipe visibility, {tag}: {k} of {len(sel)} rows ({k / len(sel):.3f}) have D within 5.5 Mpc of "
          f"Vhel/70 (Hubble-flow rows D = cz_cmb/70 differ from Vhel/70 by the CMB-frame term, at most ~5.3 Mpc)")
    dd = collections.Counter(r["dist_mpc"] for r in h)
    P("most common dist values: " + "; ".join(f"{k} x{v}" for k, v in dd.most_common(10)))
    P(f"rows with 15 <= D <= 18 Mpc: {sum(1 for r in h if 15 <= num(r['dist_mpc']) <= 18)}; "
      f"rows with D == 16.7 exactly: {dd['16.7']}")

    P("\n## 7. cross-version checks")
    both_rows = [r for r in rows if r["in_durbala2020"] == "1" and r["in_a100_table2"] == "1"]
    verify_inputs(data_dir, REQUIRED, strict=True)
    t1 = read_fixed(os.path.join(data_dir, "durbala2020_table1.dat.gz"), T1_SPEC)
    t2 = read_fixed(os.path.join(data_dir, "durbala2020_table2.dat.gz"), T2_SPEC)
    a1 = read_fixed(os.path.join(data_dir, "haynes2018_a100_table2.dat.gz"), A100_SPEC)
    nd = collections.Counter()
    for r in both_rows:
        a = int(r["agc"])
        for k_d, k_h, tag in (("rvel", "vhel", "vhel"), ("dist", "dist", "dist"), ("e_dist", "e_dist", "e_dist")):
            if num(t1[a][k_d]) != num(a1[a][k_h]):
                nd[tag] += 1
        if num(t2[a]["mhi"]) != num(a1[a]["mhi"]):
            nd["logmhi"] += 1
        if num(t2[a]["e_mhi"]) != num(a1[a]["e_mhi"]):
            nd["e_logmhi"] += 1
    P(f"Durbala vs alpha.100 overlapping columns over {len(both_rows)} shared AGC: differing rows per column = "
      f"{dict(nd) if nd else 'none (Vhel, Dist, e_Dist, logMHI, e_logMHI identical)'}")

    fits_files = ("durbala2020-table1.21-Sep-2020.fits.gz", "durbala2020-table2.21-Sep-2020.fits.gz")
    if all(os.path.exists(os.path.join(data_dir, x)) for x in fits_files):
        verify_inputs(data_dir, OPTIONAL, strict=False)
        byagc = {int(r["agc"]): r for r in rows}
        spec1 = [("sdss_phot_flag", "sdssPhotFlag", None), ("sdss_objid", "sdss_objid", None), ("ra_dur_deg", "RA", 6),
                 ("dec_dur_deg", "DEC", 5), ("vhel_kms", "Vhelio", 0), ("dist_mpc", "Dist", 1), ("e_dist_mpc", "sigDist", 1),
                 ("gext_mag", "extinction_g", 2), ("iext_mag", "extinction_i", 2), ("ba_r", "expAB_r", 2),
                 ("e_ba_r", "expAB_r_err", 2), ("imag_cmodel", "cModelMag_i", 2), ("e_imag_cmodel", "cModelMagErr_i", 2)]
        spec2 = [("gamma_g", "gamma_g", 2), ("gamma_i", "gamma_i", 2), ("imag_abs_corr", "absMag_i_corr", 2),
                 ("e_imag_abs_corr", "absMag_i_corr_err", 2), ("gi_corr", "gmi_corr", 2), ("e_gi_corr", "gmi_corr_err", 2),
                 ("logms_taylor", "logMstarTaylor", 2), ("e_logms_taylor", "logMstarTaylor_err", 2),
                 ("logms_mcgaugh", "logMstarMcGaugh", 2), ("e_logms_mcgaugh", "logMstarMcGaugh_err", 2),
                 ("logms_gswlc", "logMstarGSWLC", 2), ("e_logms_gswlc", "logMstarGSWLC_err", 2),
                 ("logsfr22", "logSFR22", 2), ("e_logsfr22", "logSFR22_err", 2), ("logsfr_nuvir", "logSFRNUVIR", 2),
                 ("e_logsfr_nuvir", "logSFRNUVIR_err", 2), ("logsfr_gswlc", "logSFRGSWLC", 2),
                 ("e_logsfr_gswlc", "logSFRGSWLC_err", 2), ("logmhi", "logMH", 2), ("e_logmhi", "logMH_err", 2)]
        P("VizieR (rounded text) vs Cornell FITS (float64): max |FITS - CSV| per column, in units of the rounding "
          "half-step, and missing-pattern mismatches")
        worst_all = 0.0
        for fn, spec in ((fits_files[0], spec1), (fits_files[1], spec2)):
            cols = read_fits_bintable(os.path.join(data_dir, fn))
            fa = cols["AGC"]
            if len(fa) != 31501:
                P(f"  {fn}: {len(fa)} rows (expected 31501)")
            line = []
            for cname, fname, dec in spec:
                mx, miss = 0.0, 0
                for i, a in enumerate(fa):
                    r = byagc.get(a)
                    if r is None:
                        miss += 1
                        continue
                    v = cols[fname][i]
                    if fname == "sdss_objid":
                        fits_missing, vv = v == -9223372036854775808, v
                    elif isinstance(v, float):
                        fits_missing, vv = math.isnan(v), v
                    else:
                        fits_missing, vv = False, v
                    csv_missing = r[cname] == ""
                    if fits_missing != csv_missing:
                        miss += 1
                        continue
                    if fits_missing:
                        continue
                    if dec is None:
                        miss += int(int(r[cname]) != vv)
                    else:
                        mx = max(mx, abs(float(r[cname]) - vv) / (0.5 * 10 ** (-dec)))
                worst_all = max(worst_all, mx)
                line.append(f"{cname}: {mx:.3f}/{miss}")
            P(f"  {fn}: " + "; ".join(line))
        P(f"  largest ratio over all columns = {worst_all:.4f} (1.0 = exactly at the rounding boundary; the CSV text is "
          f"the 2-decimal rounding of the FITS values everywhere)")
    else:
        P("Cornell FITS files not present: FITS cross-check skipped")

    cc = os.path.join(data_dir, "a100.code12.table2.190808.csv")
    if os.path.exists(cc):
        verify_inputs(data_dir, OPTIONAL, strict=False)
        with open(cc, newline="", encoding="ascii") as f:
            crow = list(csv.DictReader(f))
        byagc = {int(r["agc"]): r for r in rows}
        mm = collections.Counter()
        dra = dde = dora = dode = 0.0
        for c in crow:
            r = byagc[int(c["AGCNr"])]
            for ck, rk in (("Vhelio", "vhel_kms"), ("W50", "w50_kms"), ("sigW", "e_w50_kms"), ("W20", "w20_kms"),
                           ("HIflux", "s21_jykms"), ("sigflux", "e_s21_jykms"), ("SNR", "snr"), ("RMS", "rms_mjy"),
                           ("Dist", "dist_mpc"), ("sigDist", "e_dist_mpc"), ("logMH", "logmhi"),
                           ("siglogMH", "e_logmhi"), ("HIcode", "hi_code")):
                if float(c[ck]) != float(r[rk]):
                    mm[rk] += 1
            dra = max(dra, abs(float(c["RAdeg_HI"]) - float(r["ra_hi_deg"])))
            dde = max(dde, abs(float(c["DECdeg_HI"]) - float(r["dec_hi_deg"])))
            if r["ra_oc_deg"] != "":
                dora = max(dora, abs(float(c["RAdeg_OC"]) - float(r["ra_oc_deg"])))
                dode = max(dode, abs(float(c["DECdeg_OC"]) - float(r["dec_oc_deg"])))
        P(f"VizieR alpha.100 vs Cornell a100.code12.table2.190808.csv: {len(crow)} rows; numeric columns differing = "
          f"{dict(mm) if mm else 'none'}; max position differences (deg) HI RA {dra:.2e} Dec {dde:.2e}, OC RA {dora:.2e} "
          f"Dec {dode:.2e} (the Cornell decimal degrees are rounded; the VizieR sexagesimal is the original)")
    else:
        P("Cornell alpha.100 CSV not present: CSV cross-check skipped")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", default=DEFAULT_DATA)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--checks", action="store_true", help="after building, print the sanity checks")
    ap.add_argument("--verify", action="store_true", help="rebuild in memory and compare with the CSV on disk")
    a = ap.parse_args()
    data = csv_bytes(build_rows(a.data_dir))
    if a.verify:
        disk = open(a.out, "rb").read()
        same = disk == data
        print(f"rebuilt {len(data)} bytes sha256 {hashlib.sha256(data).hexdigest()}; on disk {len(disk)} bytes "
              f"sha256 {hashlib.sha256(disk).hexdigest()}; byte-identical = {same}")
        sys.exit(0 if same else 1)
    with open(a.out, "wb") as f:
        f.write(data)
    print(f"wrote {os.path.basename(a.out)}: {data.count(10) - 1} data rows, {len(COLNAMES)} columns, {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    if a.checks:
        run_checks(a.out, a.data_dir)


if __name__ == "__main__":
    main()
