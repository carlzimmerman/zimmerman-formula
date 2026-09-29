#!/usr/bin/env python3
"""Parse per-galaxy LaTeX tables from four arXiv sources (public TeX source, raw fragments in raw_small/).

  MSA-3D            arXiv:2606.27853  galaxy_parameters.tbl, fitted_parameters.tbl (JWST/NIRSpec, z 0.5-1.7)
  Mancera Pina 2026 arXiv:2511.08685  'Main parameters of our galaxy sample' (KROSS+KMOS3D discs, z=0.9)
  Amvrosiadis 2025  arXiv:2312.08959  parent-sample table and best-fit table (ALMA CO discs, z 1.2-4.7)
  Sharma 2024       arXiv:2406.08934  extra_material/GS21b_catalog.fits (225 KROSS galaxies), CRC fit FITS (16 bins)

Outputs: msa3d_galaxies.csv, msa3d_kinematics.csv, manceraPina2026_sample.csv, amvrosiadis_parent.csv,
         amvrosiadis_bestfit.csv, sharma2024_gs21b.csv, checks.txt, manifest.json.
Commented-out LaTeX (lines starting with %) is ignored: several of these files keep superseded drafts of the tables.
No fit, no derived physics.  Usage: python3 build.py
"""
import collections, csv, hashlib, json, os, re, sys
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
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def active_lines(fn):
    """Non-comment lines; strip a trailing unescaped % comment."""
    out = []
    for l in open(os.path.join(RAW, fn), encoding="utf-8", errors="replace"):
        s = l.rstrip("\n")
        if s.lstrip().startswith("%"):
            continue
        m = re.search(r"(?<!\\)%", s)
        if m:
            s = s[:m.start()]
        out.append(s)
    return out


NAN = float("nan")


def cell(s):
    """-> (value, err_hi, err_lo, flag). value NaN if not numeric. flag = dagger/ddagger/other marker text."""
    raw = s
    s = re.sub(r"\\iffalse.*?\\fi", "", s)
    flag = ""
    for k, tag in (("dagger", "fixed1"), ("ddagger", "fixed2")):
        if k in s:
            flag = "ddagger" if "ddagger" in s else "dagger"
    t = re.sub(r"\\(dagger|ddagger|,|;|!|:|\s)", " ", s)
    t = t.replace("$", " ").replace("{", " ").replace("}", " ").replace("\\pm", " PM ")
    if re.search(r"---|xmark|cdots\s*$", raw) and not re.search(r"\d", re.sub(r"cdots", "", t)):
        return NAN, NAN, NAN, flag
    m = re.search(r"(-?\d+\.?\d*)", t)
    if not m:
        return NAN, NAN, NAN, flag
    val = float(m.group(1)); rest = t[m.end():]
    hi = lo = NAN
    if "PM" in rest:
        e = re.search(r"PM\s*(\d+\.?\d*)", rest)
        if e:
            hi = lo = float(e.group(1))
    else:
        h = re.search(r"\+\s*(\d+\.?\d*)", rest); l_ = re.search(r"-\s*(\d+\.?\d*)", rest)
        if h: hi = float(h.group(1))
        if l_: lo = float(l_.group(1))
    return val, hi, lo, flag


def row_cells(line):
    line = re.sub(r"\\\\.*$", "", line)          # drop the row terminator and anything after
    return [c.strip() for c in line.split("&")]


def write(fn, cols, rows):
    with open(os.path.join(HERE, fn), "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)


def tt(s):
    return re.sub(r"\\texttt\{|\$\^\{\([a-z]\)\}\$|\}|\$", "", s).strip()


# ------------------------------------------------------------------ MSA-3D
sec = None; G = []
for l in active_lines("msa3d_2606.27853_galaxy_parameters.tbl"):
    if "Golden sample" in l: sec = "golden"; continue
    if "Good sample" in l: sec = "good"; continue
    if l.lstrip().startswith("\\texttt"):
        c = row_cells(l)
        foot = re.findall(r"\^\{\(([a-z])\)\}", l)
        z = cell(c[1])[0]; ra = float(c[2]); dec = float(c[3]); lm = cell(c[4])[0]; sfr = cell(c[5])[0]; re_ = cell(c[6])[0]
        G.append([tt(c[0]), sec, z, ra, dec, lm, sfr, re_, ";".join(foot)])
ids_g = [r[0] for r in G]
cnt = collections.Counter(r[1] for r in G)
check(len(G) == 30 and cnt == {"golden": 23, "good": 7} or len(G) == 30,
      f"MSA-3D galaxy table: {len(G)} active rows, sections {dict(cnt)} (paper: 30 = 23 golden + 7 good)")
check(cnt.get("golden") == 23 and cnt.get("good") == 7, "MSA-3D sections are 23 golden and 7 good")
check(len(set(ids_g)) == len(ids_g), "MSA-3D galaxy IDs unique")
zs = np.array([r[2] for r in G]); lm = np.array([r[5] for r in G])
check(bool(np.all((zs > 0.5) & (zs < 1.75)) and np.all((lm > 8.5) & (lm < 11.5))),
      f"MSA-3D z in (0.5, 1.75) and log M* in (8.5, 11.5): z {zs.min()}-{zs.max()}, logM {lm.min()}-{lm.max()}")
write("msa3d_galaxies.csv", ["id", "sample", "z", "ra_deg", "dec_deg", "logMstar", "sfr_msun_yr", "re_arcsec", "footnote"], G)

sec = None; Kn = []
for l in active_lines("msa3d_2606.27853_fitted_parameters.tbl"):
    if "Golden sample" in l: sec = "golden"; continue
    if "Good sample" in l: sec = "good"; continue
    if l.lstrip().startswith("\\texttt"):
        c = row_cells(l)
        row = [tt(c[0]), sec, cell(c[1])[0]]
        for i in range(2, 10):
            v, hi, lo, fl = cell(c[i])
            row += [v, hi, lo, fl]
        row.append(re.sub(r"[\$\s]", "", c[10]) if len(c) > 10 else "")
        Kn.append(row)
names_k = ["inc_F444W_deg", "pa_deg", "re_disk_kpc", "sigma0_kms", "vrot_re_kms", "v_over_sigma", "fdm_re", "bt_kin"]
kcols = ["id", "sample", "z"] + [f"{n}{s}" for n in names_k for s in ("", "_errhi", "_errlo", "_flag")] + ["rc_shape"]
check(len(Kn) == 30 and [r[0] for r in Kn] == ids_g, "MSA-3D kinematics table lists the same 30 IDs in the same order as the galaxy table")
check(all(a[2] == b[2] for a, b in zip(G, Kn)), "MSA-3D redshifts agree between the two tables for every galaxy")
vr = np.array([r[3 + 4 * names_k.index("vrot_re_kms")] for r in Kn], float)
fd = np.array([r[3 + 4 * names_k.index("fdm_re")] for r in Kn], float)
check(bool(np.all(np.isfinite(vr)) and vr.min() > 20 and vr.max() < 400), f"MSA-3D Vrot(Re) finite for all 30, {vr.min():.1f}-{vr.max():.1f} km/s")
check(bool(np.all(np.isfinite(fd)) and fd.min() >= 0 and fd.max() <= 1), f"MSA-3D fDM(Re) in [0,1]: {fd.min():.2f}-{fd.max():.2f}; median of golden {np.median([f for f,r in zip(fd,Kn) if r[1]=='golden']):.2f}")
shapes = collections.Counter(r[-1] for r in Kn)
log(f"MSA-3D rotation-curve shapes: {dict(shapes)}; velocity is Vrot at ONE radius, R_e of the disk; no gas mass in either table")
write("msa3d_kinematics.csv", kcols, Kn)

# ------------------------------------------------------------------ Mancera Pina 2026
M = []
for l in active_lines("manceraPina2026_2511.08685_table_sample.tex"):
    c = row_cells(re.sub(r"\\noalign\{[^}]*\}", "", l))
    if len(c) >= 11 and re.fullmatch(r"\d\.\d+", c[1].strip() or "x"):
        M.append([c[0].strip()] + [float(x) for x in c[1:11]])
mc = ["name", "z", "logMstar", "e_logMstar", "jstar_p16", "jstar_p50", "jstar_p84", "vcirc_flat_p16", "vcirc_flat_p50", "vcirc_flat_p84", "v_over_sigma_halpha"]
check(len(M) == 43, f"Mancera Pina 2026 table has 43 galaxies (paper: 43 discs at z=0.9) (got {len(M)})")
mz = np.array([r[1] for r in M]); check(bool(mz.min() > 0.5 and mz.max() < 1.1), f"Mancera Pina z in (0.5,1.1): {mz.min()}-{mz.max()}")
check(all(r[7] <= r[8] <= r[9] for r in M), "Mancera Pina Vcirc,f percentiles are ordered p16 <= p50 <= p84 for every row")
write("manceraPina2026_sample.csv", mc, M)

# ------------------------------------------------------------------ Amvrosiadis 2025
P = []
for l in active_lines("amvrosiadis2025_2312.08959_table_parent.tex"):
    if l.lstrip().startswith("\\textbf{"):
        c = row_cells(l)
        idn_raw = re.sub(r"\\textbf\{|\}", "", c[0]).strip()
        idn = idn_raw.split("$")[0].strip()          # drop footnote markers such as $^{\alpha,\beta$
        beam = re.sub(r"[\$\\ ]|times", lambda m: "x" if m.group(0) == "times" else "", c[3])
        lm = cell(c[4]); lg = cell(c[5]); ls = cell(c[6]); ll = cell(c[7]); dv = cell(c[8])[0]
        snr = cell(c[9])[0]
        cls = re.sub(r"\\Romannum\{(\d)\}", lambda m: {"1": "I", "2": "II", "3": "III"}.get(m.group(1), m.group(1)), c[10]).strip()
        co = re.sub(r"[\$\\ ]", "", c[2]).replace("-", "-")
        P.append([idn, cell(c[1])[0], co, beam, lm[0], lm[1], lm[2], lg[0], lg[1], ls[0], ll[0], dv, snr, cls])
pc_ = ["alessid", "z", "co_transition", "beam_arcsec", "logMstar", "logMstar_errhi", "logMstar_errlo", "logMgas_msun", "logMgas_err",
       "logSFR", "logLIR", "delta_v_kms", "snr", "class"]
check(len(P) >= 15, f"Amvrosiadis parent table parsed {len(P)} sources")
pz = np.array([r[1] for r in P]); check(bool(pz.min() > 1.0 and pz.max() < 5.0), f"Amvrosiadis z in (1,5): {pz.min()}-{pz.max()}")
write("amvrosiadis_parent.csv", pc_, P)
B = []
for l in active_lines("amvrosiadis2025_2312.08959_table_bestfit.tex"):
    if l.lstrip().startswith("\\textbf{"):
        c = row_cells(l)
        idn = re.sub(r"\\textbf\{|\}", "", c[0]).strip()
        row = [idn]
        for i in range(1, 8):
            v, hi, lo, fl = cell(c[i]) if i < len(c) else (NAN, NAN, NAN, "")
            row += [v, hi, lo]
        B.append(row)
bc = ["alessid"] + [f"{n}{s}" for n in ("re_arcsec", "theta_deg", "inc_deg", "vmax_kms", "sigma_kms", "vcirc_2re_kms", "mdyn_10kpc_1e11msun") for s in ("", "_errhi", "_errlo")]
check(len(B) >= 8, f"Amvrosiadis best-fit table parsed {len(B)} sources with a fit")
pids = {r[0] for r in P}
check(all(r[0] in pids for r in B), "every Amvrosiadis best-fit source is in the parent table")
have_v = [r for r in B if np.isfinite(r[bc.index('vcirc_2re_kms')])]
log(f"Amvrosiadis: {len(B)} fitted sources; {len(have_v)} have a finite V_circ(2 r_e); velocity is at a STATED radius, 2 r_e; "
    f"gas mass is measured CO gas with a conversion factor (parent-table logMgas), not a scaling")
write("amvrosiadis_bestfit.csv", bc, B)

# ------------------------------------------------------------------ Sharma 2024
from astropy.io import fits
d = fits.open(os.path.join(RAW, "sharma2024_2406.08934_GS21b_catalog.fits"))[1].data
check(len(d) == 225, f"Sharma GS21b catalogue has 225 rows (got {len(d)})")
cols = list(d.columns.names)
with open(os.path.join(HERE, "sharma2024_gs21b.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for r in d:
        w.writerow([str(x) if isinstance(x, (str, np.str_)) else float(x) for x in r])
zz = np.asarray(d["Redshift"], float); check(bool(zz.min() > 0.7 and zz.max() < 1.05), f"Sharma z in (0.7, 1.05): {zz.min():.3f}-{zz.max():.3f}")
for c in ("Ve", "Vopt", "Vout", "Mstar", "MH2", "MHI"):
    check(bool(np.all(np.isfinite(np.asarray(d[c], float))) and np.all(np.asarray(d[c], float) > 0)), f"Sharma {c} finite and positive for every row")
hi_over_star = np.asarray(d["MHI"], float) / np.asarray(d["Mstar"], float)
log(f"Sharma: median M_HI / M_star = {np.median(hi_over_star):.2f} (HI from a stacked M*-M_HI relation, NOT measured per galaxy); "
    f"median M_H2 / M_star = {np.median(np.asarray(d['MH2'], float) / np.asarray(d['Mstar'], float)):.2f} (Tacconi+2018 scaling)")
log("Sharma: Ve, Vopt, Vout are velocities at R_e, R_opt and R_out (about 5 R_D) per the paper text; the FITS carries no radius column and "
    "Rout_Flag marks 19 galaxies as F")

# ------------------------------------------------------------------ ALPAKA I (Rizzo+ / Roman-Oliveira+, arXiv:2303.16227)
def cell_lim(s):
    v, hi, lo, fl = cell(s)
    lim = "<" if "lesssim" in s else (">" if "gtrsim" in s else "")
    return v, hi, lo, lim


def alp_rows(fn):
    """Rows of an ALPAKA table: lines whose first cell starts with an integer ID. A terminal \\ only is removed
    (\\substack cells contain \\\\ inside the row)."""
    out = []
    for l in active_lines(fn):
        s = re.sub(r"\s*\\\\\s*$", "", l.strip())
        c = [x.strip() for x in s.split("&")]
        if len(c) >= 3 and re.match(r"^\d+(\$\^\{\*\}\$)?$", c[0]):
            out.append(c)
    return out


def alp_id(x):
    return int(re.match(r"\d+", x).group(0)), ("*" if "*" in x else "")


A1 = []
for c in alp_rows("alpaka1_2303.16227_table1_sample.tex"):
    i, m = alp_id(c[0])
    A1.append([i, c[1].strip(), float(c[2]), float(c[3]), float(c[4]), c[5].strip(), c[6].strip()])
check(len(A1) == 28, f"ALPAKA I sample table has 28 galaxies (got {len(A1)})")
check([r[0] for r in A1] == list(range(1, 29)), "ALPAKA IDs run 1..28")
az = np.array([r[4] for r in A1]); check(bool(az.min() > 0.5 and az.max() < 3.7), f"ALPAKA z in (0.5, 3.7): {az.min()}-{az.max()} (the paper's title and abstract say z = 0.5-3.5; the table's maximum is {az.max()}, a small wording mismatch in the source)")
write("alpaka1_sample.csv", ["id", "name", "ra_deg", "dec_deg", "z", "field_survey", "notes"], A1)

A2 = []
for c in alp_rows("alpaka1_2303.16227_table2_alma_obs.tex"):
    i, _ = alp_id(c[0])
    bm = re.findall(r"\d+\.?\d*", c[4])
    A2.append([i, c[1], c[2], c[3], float(bm[0]), float(bm[1]), cell(c[5])[0], cell(c[6])[0], cell(c[7])[0]])
check(len(A2) == 28, f"ALPAKA I ALMA-observation table has 28 rows (got {len(A2)})")
write("alpaka1_alma_obs.csv", ["id", "project", "line", "freq_range_ghz", "beam_major_arcsec", "beam_minor_arcsec",
                             "channel_kms", "rms_mjy_beam", "int_time_hr"], A2)

A3 = []
for c in alp_rows("alpaka1_2303.16227_table3_properties.tex"):
    i, _ = alp_id(c[0])
    ms = cell(c[1]); sf = cell(c[2]); dm = cell(c[3]); li = cell(c[5]); il = cell(c[6]); lp = cell(c[7])
    A3.append([i, ms[0], ms[1], sf[0], sf[1], dm[0], dm[1], dm[2], c[4].strip(), li[0], il[0], il[1], lp[0], lp[1],
               re.sub(r"[\$\\ ]", "", c[8]), cell(c[9])[0]])
check(len(A3) == 28, f"ALPAKA I properties table has 28 rows (got {len(A3)})")
ms_ = np.array([r[1] for r in A3], float)
no_ms = [r[0] for r in A3 if not np.isfinite(r[1])]
check(no_ms == [16, 17, 24], f"ALPAKA M* is finite for 25 of 28 galaxies; the source table prints '-' for IDs {no_ms} (expected [16, 17, 24])")
check(bool(np.all(ms_[np.isfinite(ms_)] > 0)), f"ALPAKA M* positive where given (1e10 Msun): {np.nanmin(ms_)}-{np.nanmax(ms_)}")
write("alpaka1_properties.csv", ["id", "mstar_1e10msun", "e_mstar", "sfr_msun_yr", "e_sfr", "delta_ms", "delta_ms_errhi",
      "delta_ms_errlo", "type_ms_or_other", "lir_1e12lsun", "iline_jykms", "e_iline", "lprime_1e10_kkmspc2", "e_lprime",
      "hst_filter", "lambda_rest_eff_A"], A3)

A4 = []
for c in alp_rows("alpaka1_2303.16227_table4_geometry.tex"):
    i, m = alp_id(c[0])
    v = [cell(c[k]) for k in range(1, 6)]
    A4.append([i, m] + [x for t_ in v for x in t_[:3]] + [c[6].strip()])
check(len(A4) == 28, f"ALPAKA I geometry table has 28 rows (got {len(A4)})")
kc4 = collections.Counter(r[-1] for r in A4)
log(f"ALPAKA kinematic classes (KC column): {dict(kc4)}")
write("alpaka1_geometry.csv", ["id", "footnote_star", "pa_hst", "e1", "e2", "i_hst", "e1", "e2", "pa_alma", "e1", "e2",
      "i_alma", "e1", "e2", "pa_kin", "e1", "e2", "kc"], A4)

A5 = []
for c in alp_rows("alpaka1_2303.16227_table5_kinematics.tex"):
    i, _ = alp_id(c[0])
    v = [cell_lim(c[k]) for k in range(1, 7)]
    A5.append([i] + [x for t_ in v for x in t_])
check(len(A5) == 19, f"ALPAKA I kinematics table has 19 disks (paper: 19 secure disks) (got {len(A5)})")
check(all(r[0] in {a[0] for a in A1} for r in A5), "every kinematics ID is in the sample table")
vm = np.array([r[1] for r in A5], float); ve = np.array([r[9] for r in A5], float)
check(bool(np.all(vm > 0) and np.all(ve > 0)), f"ALPAKA Vmax and Vext positive: Vmax {vm.min():.0f}-{vm.max():.0f}, Vext {ve.min():.0f}-{ve.max():.0f} km/s")
check(bool(np.all(ve <= 1.5 * vm) and np.all(ve >= 0.3 * vm)), "ALPAKA Vext within a factor 0.3-1.5 of Vmax for every disk (both are outer-radius velocities of the same curve)")
log(f"ALPAKA: disks with kinematic class D in table 4: {sum(1 for r in A4 if r[-1] == 'D')}; Vext is the average of the last TWO radial points; "
    f"the outermost radius R_ext is NOT tabulated (only plotted); gas is given as line luminosity L' (CO or [CI]), not a gas mass")
write("alpaka1_kinematics.csv", ["id", "vmax_kms", "vmax_errhi", "vmax_errlo", "vmax_lim", "sigma_m_kms", "sigma_m_errhi",
      "sigma_m_errlo", "sigma_m_lim", "vext_kms", "vext_errhi", "vext_errlo", "vext_lim", "sigma_ext_kms", "sigma_ext_errhi",
      "sigma_ext_errlo", "sigma_ext_lim", "vmax_over_sigma_m", "e1", "e2", "lim", "vext_over_sigma_ext", "e1", "e2", "lim2"], A5)

# ------------------------------------------------------------------ helpers for the 2023-2026 papers below
def generic_rows(fn, first_regex, ncell_min=3):
    out = []
    for l in active_lines(fn):
        s = re.sub(r"\\noalign\{[^}]*\}", "", l)
        s = re.sub(r"\\vspace\{[^}]*\}", "", s)
        s = re.sub(r"\s*\\\\.*$", "", s.strip()) if not re.search(r"\\substack", s) else re.sub(r"\s*\\\\\s*$", "", s.strip())
        c = [x.strip() for x in s.split("&")]
        if len(c) >= ncell_min and re.match(first_regex, c[0]):
            out.append(c)
    return out


def cellf(s):
    v, hi, lo, fl = cell(s)
    fixed = "fixed" if re.search(r"^\s*\[.*\]\s*$", s.strip()) else ""
    lim = "<" if "lesssim" in s else (">" if "gtrsim" in s else "")
    return v, hi, lo, fixed or lim


# ------------------------------------------------------------------ Lelli+2023, arXiv:2302.00030 (two cosmic-noon discs with ALMA CO)
# 3DBarolo geometry table (two columns)
L3 = {}
for l in active_lines("lelli2023_2302.00030_table_3dfits.tex"):
    s = re.sub(r"\s*\\\\.*$", "", l.strip())
    c = [x.strip() for x in s.split("&")]
    if len(c) == 3 and c[0].startswith("$") or (len(c) == 3 and "sigma" in c[0]):
        L3[c[0]] = (c[1], c[2])
write("lelli2023_3dbarolo.csv", ["parameter", "zC-400569", "zC-488879"], [[k, v[0].replace("$", ""), v[1].replace("$", "")] for k, v in L3.items()])
# mass-model table: a row can wrap across two source lines (a line ending in '&')
txt = "\n".join(active_lines("lelli2023_2302.00030_table_massmodels.tex"))
txt = re.sub(r"&\s*\n\s*", "& ", txt)
LM = []; gal = None
for s in txt.split("\n"):
    s = re.sub(r"\s*\\\\.*$", "", s.strip())
    if "&" in s and "Galaxy" not in s and "multicolumn" not in s and "Model" not in s:
        c = [x.strip() for x in s.split("&")]
        if re.match(r"^zC-\d+", c[0]):
            gal = c[0]; c = c[1:]
        else:
            c = c[1:]
        LM.append([gal] + c)
check(len(LM) == 6, f"Lelli 2023 mass-model table has 6 rows (2 galaxies x 3 models) (got {len(LM)})")
lm_cols = ["galaxy", "model"] + [f"{n}{s}" for n in ("inc_deg", "Mgas_1e10", "Mdisk_1e10", "Mbul_1e10", "M200_1e12", "C200", "Mbar_1e10", "Mbul_over_Mbar") for s in ("", "_errhi", "_errlo")]
rows_lm = []
for r in LM:
    vals = [cell(x) for x in r[2:10]]
    rows_lm.append([r[0], re.sub(r"[\$]", "", r[1])] + [y for v in vals for y in v[:3]])
check({r[0] for r in rows_lm} == {"zC-400569", "zC-488879"}, "Lelli 2023: the two galaxies are zC-400569 (z 2.24) and zC-488879 (z 1.47)")
write("lelli2023_massmodels.csv", lm_cols, rows_lm)
mb = {(r[0], r[1]): r for r in rows_lm}
mbar_i = lm_cols.index("Mbar_1e10")
log("Lelli 2023: baryonic mass (1e10 Msun) in the baryons-only fits: zC-400569 %.1f, zC-488879 %.1f; MOND fits use a0 = 1.2e-10 (the z = 0 value); "
    "the paper states the rotation curves are limited to high-acceleration regions with V_obs^2/R > 3-4 a0" % (
    mb[("zC-400569", "Baryons only")][mbar_i], mb[("zC-488879", "Baryons only")][mbar_i]))

# ------------------------------------------------------------------ ALPAKA discs with JWST + CO/[CI] decomposition, arXiv:2601.03338
J1 = generic_rows("alpaka_jwst2026_2601.03338_table_data.tex", r"^\d+$", 8)
check(len(J1) == 3, f"arXiv:2601.03338 data table has 3 discs (got {len(J1)})")
jrows = []
for c in J1:
    ms = cell(c[7]); sf = cell(c[8]); lp = cell(c[3])
    jrows.append([int(c[0]), float(c[1]), re.sub(r"[\$\\ ]", "", c[2]), lp[0], lp[1], float(c[4]), c[5].strip(), float(c[6]), ms[0], ms[1], ms[2], sf[0], sf[1]])
check([r[0] for r in jrows] == [1, 3, 13], "arXiv:2601.03338 discs are ALPAKA IDs 1, 3 and 13")
write("alpaka_jwst2026_data.csv", ["alpaka_id", "z", "line", "Lprime_1e10", "e_Lprime", "n_resolution_elements", "jwst_filter", "rest_wavelength_um",
      "logMstar_sed", "errhi", "errlo", "sfr_msun_yr", "e_sfr"], jrows)
J2 = generic_rows("alpaka_jwst2026_2601.03338_table_fiducial.tex", r"^ID\d+$", 8)
check(len(J2) == 3, f"arXiv:2601.03338 fiducial-fit table has 3 rows (got {len(J2)})")
frows = []
for c in J2:
    vals = [cell(x) for x in c[1:9]]
    frows.append([int(c[0][2:])] + [y for v in vals for y in v[:3]])
write("alpaka_jwst2026_fiducial_fit.csv", ["alpaka_id"] + [f"{n}{s}" for n in ("logMstar_dyn", "logMbulge", "logMdisk", "logMgas", "alphaCO_times_rl", "logM200", "log_fbar", "c200") for s in ("", "_errhi", "_errlo")], frows)
mgas = {r[0]: r[1 + 3 * 3] for r in frows}; mst = {r[0]: r[1] for r in frows}
log(f"arXiv:2601.03338 fiducial decompositions (JWST NIRCam stars + CO/[CI] gas, free gas normalisation): "
    f"ID1 log M* {mst[1]}, log M_gas {mgas[1]}; ID3 log M* {mst[3]}, log M_gas {mgas[3]}; ID13 log M* {mst[13]}, log M_gas {mgas[13]}. "
    f"ID1's dynamical stellar mass exceeds its SED value (the paper says the pre-JWST SED mass is 2-3 times too low)")

# ------------------------------------------------------------------ ALMA-CRISTAL kinematics, arXiv:2507.11600 (z 4-6, [CII])
def cristal_id(x):
    return re.sub(r"\\tablefootmark\{\w\}", "", re.sub(r"^CRISTAL-", "", x)).strip()

C1 = generic_rows("cristal2025_2507.11600_table_main.tex", r"^CRISTAL-\d+[a-z]?(-E)?(\\tablefootmark\{\w\})?$", 8)
C1r = []
for c in C1:
    beam = re.sub(r"\\farcs", '"', c[7]).replace("$\\times$", "x").replace("$", "").strip()
    C1r.append([cristal_id(c[0]), c[1].replace("\\_", "_"), float(c[2]), float(c[3]), float(c[4]), cell(c[5])[0], cell(c[6])[0], beam, cell(c[8])[0]])
check(len(C1r) == 32, f"CRISTAL main table has 32 rows (the paper's 32 galaxies of the kinematics sample) (got {len(C1r)})")
cz = np.array([r[2] for r in C1r]); check(bool(cz.min() > 4.0 and cz.max() < 6.0), f"CRISTAL z in (4, 6): {cz.min()}-{cz.max()}")
nan_ms = [r[0] for r in C1r if not np.isfinite(r[5])]
log(f"CRISTAL sample rows with no stellar mass printed ('...'): {nan_ms}; with no SFR: {[r[0] for r in C1r if not np.isfinite(r[6])]}")
write("cristal2025_sample.csv", ["id", "name", "z_cii", "ra_deg", "dec_deg", "logMstar", "logSFR", "beam_arcsec", "cube_noise_mjy_beam"], C1r)
C2 = generic_rows("cristal2025_2507.11600_table_kinematics.tex", r"^\d+[a-z]?(-E)?(\\tablefootmark\{\w\})?$", 8)
C2r = []
for c in C2:
    fm = cell(c[5])
    C2r.append([cristal_id(c[0]), c[1].strip(), cell(c[2])[0], cell(c[3])[0], cell(c[3])[1], cell(c[4])[0], cell(c[4])[1], fm[0], fm[1], fm[2], cell(c[6])[0], cell(c[7])[0]])
check(len(C2r) >= 30, f"CRISTAL kinematics table has {len(C2r)} rows")
cls = collections.Counter(r[1] for r in C2r)
log(f"CRISTAL kinematic classes: {dict(cls)}")
write("cristal2025_kinematics.csv", ["id", "classification", "pa_kin_deg", "vobs_over_2_kms", "e", "vobs_over_2sigma", "e", "f_molgas", "errhi", "errlo", "k_asym", "disk_score"], C2r)
C3 = generic_rows("cristal2025_2507.11600_table_dynamics.tex", r"^\d+[a-z]?(-E)?(\\tablefootmark\{\w\})?$", 8)
C3r = []
for c in C3:
    vals = [cellf(x) for x in c[1:10]]
    C3r.append([cristal_id(c[0])] + [y for v in vals for y in v[:4]])
cols3 = ["id"] + [f"{n}{s}" for n in ("logMtot", "Re_disk_kpc", "BT", "Vrot_Re_kms", "sigma0_kms", "fDM_Re", "inc_deg", "Rout_over_Re", "Rout_over_beam") for s in ("", "_errhi", "_errlo", "_flag")]
check(len(C3r) == 14, f"CRISTAL dynamical-model table has 14 rows as printed (got {len(C3r)}); the kinematics table classifies 16 galaxies as Disk or Best Disk")
ro = np.array([r[cols3.index("Rout_over_Re")] for r in C3r], float)
check(bool(np.all(np.isfinite(ro))), f"CRISTAL R_out/R_e,disk finite for all {len(C3r)} disks: {np.nanmin(ro):.1f}-{np.nanmax(ro):.1f}")
write("cristal2025_dynamics.csv", cols3, C3r)
ids3 = {r[0] for r in C3r}; ids1 = {r[0] for r in C1r}
alias = {i: (i + "a") for i in ids3 if i not in ids1 and (i + "a") in ids1}
check(all(i in ids1 or i in alias for i in ids3), f"every CRISTAL dynamical-model ID appears in the sample table (aliases used: {alias})")
disk_ids = {r[0] for r in C2r if r[1] in ("Disk", "Best Disk")}
no_dyn = sorted(d for d in disk_ids if d not in ids3 and d not in {v for v in alias.values()} | {k + "a" for k in ids3})
log(f"CRISTAL: 16 galaxies are classified Disk or Best Disk; {sorted(disk_ids - ids3 - set(alias.values()))} have no row in the dynamical-model table (the table lists 14; ID '09' there is '09a' elsewhere)")
log(f"CRISTAL: {len(C3r)} disks with a dynamical model; median R_out/R_e = {np.median(ro):.1f}; velocities are Vrot at R_e; gas is [CII]-based (f_molgas), not CO")

# ------------------------------------------------------------------ Roman-Oliveira+2023, arXiv:2302.03049 ([CII] discs at z ~ 4.3, five sources, four discs)
def ro_rows(fn, first_regex):
    out = []
    for l in active_lines(fn):
        s = re.sub(r"\\vspace\{[^}]*\}", "", l)
        s = re.sub(r"\s*\\\\.*$", "", s.strip())
        c = [x.strip() for x in s.split("&")]
        if len(c) >= 3 and re.match(first_regex, c[0]):
            out.append(c)
    return out


RO_ID = r"^(AzTEC 1|BRI1335-0417|J081740|SGP38326-[12])"
R1 = ro_rows("romanoliveira2023_2302.03049_table_sample.tex", RO_ID)
check(len(R1) == 5, f"Roman-Oliveira sample table has 5 sources (got {len(R1)})")
rr = []
for c in R1:
    idn = re.sub(r"\s*\$.*$", "", c[0]).strip()
    beam = re.findall(r"\d+\.\d+", c[6])
    rr.append([idn, c[1], c[2], float(c[3]), float(c[4]), float(c[5]), float(beam[0]), float(beam[1]), cell(c[7])[0], cell(c[8])[0], cell(c[8])[1], cell(c[8])[2], cell(c[9])[0]])
write("romanoliveira2023_sample.csv", ["id", "ra", "dec", "z", "kpc_per_arcsec", "channel_kms", "beam_major_arcsec", "beam_minor_arcsec", "rms_mjy_beam",
      "I_cii_jykms", "errhi", "errlo", "int_time_s"], rr)
check(all(4.2 < r[3] < 4.5 for r in rr), "Roman-Oliveira z in (4.2, 4.5)")
R2 = ro_rows("romanoliveira2023_2302.03049_table_gasmasses.tex", RO_ID)
check(len(R2) == 5, f"Roman-Oliveira gas-mass table has 5 sources (got {len(R2)})")
def sci(s):
    m = re.search(r"(\d+\.?\d*)\s*\\pm\s*(\d+\.?\d*)\s*\\times\s*10\^\{(\d+)\}", s)
    if m: return float(m.group(1)) * 10 ** int(m.group(3)), float(m.group(2)) * 10 ** int(m.group(3))
    m = re.search(r"(\d+\.?\d*)\s*\\times\s*10\^\{(\d+)\}", s)
    return (float(m.group(1)) * 10 ** int(m.group(2)), np.nan) if m else (np.nan, np.nan)
gas = []
for c in R2:
    idn = re.sub(r"\s*\$.*$", "", c[0]).strip()
    s_sfr = cell(c[1].replace("\\sim", "")); g, ge = sci(c[2])
    gas.append([idn, s_sfr[0], s_sfr[1], s_sfr[2], "approx" if "sim" in c[1] else "", g, ge, "approx" if "sim" in c[2] else "", c[3]])
write("romanoliveira2023_gasmasses.csv", ["id", "sfr_msun_yr", "errhi", "errlo", "sfr_flag", "mh2_msun", "e_mh2", "mh2_flag", "refs"], gas)
log("Roman-Oliveira: H2 masses (from literature CO luminosities, the paper's own conversion) between %.1e and %.1e Msun" % (min(g[5] for g in gas), max(g[5] for g in gas)))
R3 = ro_rows("romanoliveira2023_2302.03049_table_kinematics.tex", RO_ID)
check(len(R3) == 4, f"Roman-Oliveira kinematics table has 4 discs (got {len(R3)})")
kk = []
for c in R3:
    idn = re.sub(r"\s*\$.*$", "", c[0]).strip()
    v = [cell(x) for x in c[1:7]]
    kk.append([idn] + [y for t_ in v for y in t_[:3]])
write("romanoliveira2023_kinematics.csv", ["id"] + [f"{n}{s}" for n in ("vrot_max_kms", "vrot_ext_kms", "sigma_mean_kms", "sigma_ext_kms", "vmax_over_sigma", "vext_over_sigma_ext") for s in ("", "_errhi", "_errlo")], kk)
vmx = [k[1] for k in kk]; check(all(150 < v < 700 for v in vmx), f"Roman-Oliveira Vrot,max in 150-700 km/s: {vmx}")
log("Roman-Oliveira: V_ext is the mean of the last two radial points; the outermost radius is not tabulated (plotted only); H2 masses are literature CO-based; external velocities 125-548 km/s (massive submillimetre galaxies); the acceleration at the outer radius is not assessed here")

# ------------------------------------------------------------------ Danhaive+2025 (geko, JWST NIRCam grism), arXiv:2503.21863: the gold sample at z ~ 3.8-4.9
def err2(s):
    """value, upper, lower from '$a^{+u}_{-l}$' with optional missing signs; upper-limit flag from '<'"""
    lim = "<" if "<" in s else ""
    m = re.search(r"(-?\d+\.?\d*)\s*\^\{\+?(\d+\.?\d*)\}\s*_\{-?(\d+\.?\d*)\}", s)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3)), lim
    m = re.search(r"(-?\d+\.?\d*)\s*_\{-?(\d+\.?\d*)\}\s*\^\{\+?(\d+\.?\d*)\}", s)
    if m:
        return float(m.group(1)), float(m.group(3)), float(m.group(2)), lim
    m = re.search(r"(-?\d+\.?\d*)", s)
    return (float(m.group(1)) if m else NAN, NAN, NAN, lim)


G = []
for l in active_lines("danhaive2025_2503.21863_table_gold.tex"):
    s = re.sub(r"\s*\\\\.*$", "", l.strip())
    c = [x.strip() for x in s.split("&")]
    if len(c) == 8 and re.match(r"^\d{6,7}$", c[0]):
        row = [int(c[0]), float(c[1])]
        for x in c[2:]:
            row += list(err2(x))
        G.append(row)
check(len(G) == 41, f"Danhaive 2025 gold-sample table has 41 galaxies as the paper's sample table states (got {len(G)})")
gz = np.array([r[1] for r in G]); check(bool(gz.min() > 3.7 and gz.max() < 6.0), f"gold-sample z in (3.7, 6.0): {gz.min()}-{gz.max()}")
gc = ["jades_id", "z"] + [f"{n}{s}" for n in ("logMstar", "logSFR", "re_kpc", "v_over_sigma0", "sigma0_kms", "logMdyn") for s in ("", "_errhi", "_errlo", "_lim")]
write("danhaive2025_gold.csv", gc, G)
lim_sig = sum(1 for r in G if r[gc.index("sigma0_kms_lim")] == "<")
log(f"Danhaive 2025 gold sample: 41 galaxies, sigma0 is only an upper limit for {lim_sig} of them; Halpha (ionised gas) kinematics with a dynamical mass, no gas mass")

# ------------------------------------------------------------------ manifest
src = {"msa3d_2606.27853_galaxy_parameters.tbl": "arXiv:2606.27853 source, tables/galaxy_parameters.tbl",
       "msa3d_2606.27853_fitted_parameters.tbl": "arXiv:2606.27853 source, tables/fitted_parameters.tbl",
       "manceraPina2026_2511.08685_table_sample.tex": "arXiv:2511.08685 source, aa57349-25.tex lines 509-566",
       "amvrosiadis2025_2312.08959_table_parent.tex": "arXiv:2312.08959 source, main.tex lines 148-264",
       "amvrosiadis2025_2312.08959_table_bestfit.tex": "arXiv:2312.08959 source, main.tex lines 440-538",
       "alpaka1_2303.16227_table1_sample.tex": "arXiv:2303.16227 source, alpaka_v2.tex lines 185-231",
       "alpaka1_2303.16227_table2_alma_obs.tex": "arXiv:2303.16227 source, alpaka_v2.tex lines 246-297",
       "alpaka1_2303.16227_table3_properties.tex": "arXiv:2303.16227 source, alpaka_v2.tex lines 332-381",
       "alpaka1_2303.16227_table4_geometry.tex": "arXiv:2303.16227 source, alpaka_v2.tex lines 415-461",
       "alpaka1_2303.16227_table5_kinematics.tex": "arXiv:2303.16227 source, alpaka_v2.tex lines 684-723",
       "lelli2023_2302.00030_table_3dfits.tex": "arXiv:2302.00030 source, ColdGasDiskCosmicNoon.tex lines 274-294",
       "lelli2023_2302.00030_table_massmodels.tex": "arXiv:2302.00030 source, ColdGasDiskCosmicNoon.tex lines 338-359",
       "alpaka_jwst2026_2601.03338_table_data.tex": "arXiv:2601.03338 source, main.tex lines 198-212",
       "alpaka_jwst2026_2601.03338_table_fiducial.tex": "arXiv:2601.03338 source, main.tex lines 588-611",
       "cristal2025_2507.11600_table_main.tex": "arXiv:2507.11600 source, main_arxiv.tex lines 241-297",
       "cristal2025_2507.11600_table_kinematics.tex": "arXiv:2507.11600 source, main_arxiv.tex lines 317-393",
       "cristal2025_2507.11600_table_dynamics.tex": "arXiv:2507.11600 source, main_arxiv.tex lines 761-815",
       "romanoliveira2023_2302.03049_table_sample.tex": "arXiv:2302.03049 source, main.tex (sample table)",
       "romanoliveira2023_2302.03049_table_gasmasses.tex": "arXiv:2302.03049 source, main.tex (SFR and gas-mass table)",
       "romanoliveira2023_2302.03049_table_kinematics.tex": "arXiv:2302.03049 source, main.tex (kinematic parameters)",
       "danhaive2025_2503.21863_table_gold.tex": "arXiv:2503.21863 source, main.tex lines 817-877",
       "sharma2024_2406.08934_GS21b_catalog.fits": "arXiv:2406.08934 source, extra_material/GS21b_catalog.fits",
       "sharma2024_2406.08934_CRCs_FitsParam_Burkert.fits": "arXiv:2406.08934 source, extra_material/CRCs_FitsParam_Burkert.fits"}
man = {"built_by": "data_assembly/arxiv_tables/build.py", "source_tarballs": "https://arxiv.org/e-print/<id>", "raw_small": {}}
for fn, s in src.items():
    p = os.path.join(RAW, fn); man["raw_small"][fn] = {"source": s, "bytes": os.path.getsize(p), "sha256": sha(p)}
json.dump(man, open(os.path.join(HERE, "manifest.json"), "w"), indent=2)
log("wrote manifest.json")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
