#!/usr/bin/env python3
"""Extract table and column names from the Gaia DR4 DRAFT data model (ESA, PDF dated 2026-05-20 inside a zip dated 2026-06-26).

Source (downloaded 2026-09-29 with the owner's go): https://anonftp.cosmos.esa.int/pub/GAIA_PUBLIC_DATA/Gaia_DR4/dr4-prerelease/gaia-dr4-prerelease-draft-data-model_2026-06-26.zip
2,840,832 bytes; the zip and the PDF stay OUTSIDE the repo in ~/new_physics/_external_data/gaia_dr4_draft_datamodel/.  The PDF itself says the final model "is subject to change ... without any public notification".
EVERY name here is "draft 2026-06-26, confirm on release day" (Amendment 15(d): names are read on release day).  Names and types only; no data.
Parsing: table sections from the PDF's contents list (printed page = PDF page index + 1); a column entry is a line "name : description (type)".
Outputs: dr4_draft_tables.csv (every table with page range and column count), dr4_draft_columns_selected.csv (columns of the tables the DR4-READY-1 plan needs),
dr4_draft_where_is.csv (where the plan's key column names appear across ALL tables).  No cut value or decision is touched.
"""
import csv, hashlib, os, re, zipfile
import fitz
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.expanduser("~/new_physics/_external_data/gaia_dr4_draft_datamodel/")
ZIP = EXT + "gaia-dr4-prerelease-draft-data-model_2026-06-26.zip"
PDF = EXT + "gaia-dr4-prerelease-draft-data-model.pdf"
sha = hashlib.sha256(open(ZIP, "rb").read()).hexdigest()
d = fitz.open(PDF)
pages = [p.get_text() for p in d]
full = "\n".join(pages)
# ---- table of contents: "N.M name . . . . page" (page on same or next line)
i0 = full.find("Contents"); i1 = full.find("Datamodel description", i0)
toc_lines = [l.strip() for l in full[i0:i1].split("\n") if l.strip() and not l.startswith(("Gaia DPAC", "Draft", "CUx", "N/A"))]
toc = []
k = 0
while k < len(toc_lines):
    m = re.match(r"^(\d+)\.(\d+)\s+([A-Za-z0-9_\-]+)", toc_lines[k])
    if m:
        name = m.group(3); rest = toc_lines[k]
        pg = re.search(r"(\d+)\s*$", rest)
        if pg and int(pg.group(1)) > 5 and "." in rest[len(m.group(0)):]:
            page = int(pg.group(1))
        else:
            nxt = toc_lines[k + 1] if k + 1 < len(toc_lines) else ""
            pn = re.search(r"(\d+)\s*$", nxt)
            page = int(pn.group(1)) if pn and not re.match(r"^\d+\.\d+\s", nxt) else None
            if page is None and nxt.isdigit(): page = int(nxt)
        toc.append((m.group(1) + "." + m.group(2), name, page))
    k += 1
toc = [t for t in toc if t[2]]
toc.sort(key=lambda t: t[2])
assert len(toc) > 100, len(toc)
tables = []
for n, (num, name, page) in enumerate(toc):
    end = toc[n + 1][2] - 1 if n + 1 < len(toc) else len(pages)
    tables.append((num, name, page, end))
entry = re.compile(r"^([a-z][a-z0-9_]*) : (.*)$")
cols = {}
for num, name, a, b in tables:
    rows = []
    for pi in range(a - 1, min(b, len(pages))):
        lines = pages[pi].split("\n"); j = 0
        while j < len(lines):
            m = entry.match(lines[j])
            if m:
                text = m.group(2); jj = j
                while not re.search(r"\((short|int|long|float|double|boolean|string|char|float array|double array|int array|long array|short array|bigint|smallint|real|varchar|byte|array|[A-Za-z0-9_\[\] ,]+)\)\s*$", text) and jj < j + 3 and jj + 1 < len(lines):
                    jj += 1; text += " " + lines[jj].strip()
                t = re.search(r"\(([^()]*)\)\s*$", text)
                rows.append((m.group(1), t.group(1) if t else "", re.sub(r"\s+", " ", re.sub(r"\([^()]*\)\s*$", "", text)).strip(), pi + 1))
            j += 1
    cols[name] = rows
with open(os.path.join(HERE, "dr4_draft_tables.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["section", "table", "printed_page_start", "printed_page_end", "n_columns_parsed"])
    for num, name, a, b in tables: w.writerow([num, name, a, b, len(cols[name])])
WANT = ["gaia_source", "all_source_astrometry", "all_source_flags", "all_source_match", "all_source_photometry", "all_source_rvs", "crowded_field_source", "crowded_field_source_environment_match",
        "gaia_source_environment", "nss_acceleration_astro", "nss_epoch_flags", "nss_masses", "nss_multiple_orbits", "nss_multiplicity", "nss_non_linear_spectro", "nss_resolved_pair",
        "nss_two_body_orbit", "nss_vim_fl", "optical_pair", "ap_class", "ap_xp", "ap_rvs", "ap_chem", "interstellar_medium_params", "total_galactic_extinction_map", "total_galactic_extinction_map_opt", "dr3_neighbourhood"]
with open(os.path.join(HERE, "dr4_draft_columns_selected.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["table", "column", "type", "short_description", "printed_page", "status"])
    for t in WANT:
        for c in cols.get(t, []): w.writerow([t, c[0], c[1], c[2][:200], c[3], "draft 2026-06-26, confirm on release day"])
KEY = ["ruwe", "ipd_frac_multi_peak", "radial_velocity", "radial_velocity_error", "non_single_star", "parallax", "parallax_error", "parallax_over_error", "phot_g_mean_mag", "phot_bp_mean_mag",
       "astrometric_params_solved", "astrometric_gof_al", "astrometry_origin", "ra", "dec", "pmra", "pmdec", "l", "b", "ag_gspphot", "ebpminrp_gspphot", "a_g_val", "source_id", "duplicated_source",
       "visibility_periods_used", "astrometric_excess_noise", "phot_g_n_obs"]
with open(os.path.join(HERE, "dr4_draft_where_is.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["column", "tables_containing_it", "status"])
    for kk in KEY:
        where = [t for t, rows in cols.items() if any(r[0] == kk for r in rows)]
        w.writerow([kk, ";".join(where), "draft 2026-06-26, confirm on release day"])
open(os.path.join(HERE, "manifest.txt"), "w").write(f"zip sha256 {sha}\nurl https://anonftp.cosmos.esa.int/pub/GAIA_PUBLIC_DATA/Gaia_DR4/dr4-prerelease/gaia-dr4-prerelease-draft-data-model_2026-06-26.zip\nbytes {os.path.getsize(ZIP)}\ntables parsed {len(tables)}\n")
print(len(tables), "tables;", sum(len(v) for v in cols.values()), "column entries;", sha)
for t in WANT: print(t, len(cols.get(t, [])))
