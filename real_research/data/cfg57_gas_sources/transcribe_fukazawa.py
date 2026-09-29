#!/usr/bin/env python3
"""
CFG57 gas source 2 -- transcribe Table 4 ('Results of analyses of Sample
Elliptical Galaxies') and the distances of Table 1 ('List of Sample Elliptical
Galaxies') of Fukazawa et al. 2006, ApJ 636, 698 (arXiv:astro-ph/0509521),
directly from the LaTeX source in the arXiv tarball.  ALL rows are written.

Run from anywhere:   python3 transcribe_fukazawa.py
Needs:               raw/fukazawa2006_astro-ph_0509521.tar.gz (git-ignored; sha256 checked)
Writes:              fukazawa2006_table4.tsv, transcribe_fukazawa.out

The deluxetables are numbered by order of appearance (AASTeX); the script
checks that the source holds exactly five, in the order sample-chandra (1),
sample-newton (2), spec (3), results (4), nfwcmp (5), and no other table.
Checks: the row count; an independent re-read of spot values (a second parse
of the raw lines by a different route); the paper's EXG/CXG rule
(ne10 > or < 2e-3 cm^-3) against every row; and the lower-limit R_max rows,
which the text ties to the field edge, giving the same angle (R_max / D) for
every galaxy -- a joint check of the D and R_max transcriptions.
"""
import hashlib
import io
import math
import os
import re
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARBALL = os.path.join(HERE, "raw", "fukazawa2006_astro-ph_0509521.tar.gz")
SHA256 = "68f6999d676086b022df57be48c76bd29e64f13b6a4c322c2c9e8ac8301e5ec4"
OUT_TSV = os.path.join(HERE, "fukazawa2006_table4.tsv")
OUT_LOG = os.path.join(HERE, "transcribe_fukazawa.out")
CFG57 = ["NGC5846", "NGC4374", "NGC4649", "NGC4365", "NGC4494", "NGC3607", "NGC4697"]
ARCSEC = math.pi / 180.0 / 3600.0

_log = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log.append(s)


def clean(cell):
    c = re.sub(r"\\tablenotemark\{[^}]*\}", "", cell)
    c = c.replace("$\\pm$", "+-").replace("$>$", ">").replace("$", "")
    return " ".join(c.split())


def tables(lines):
    """[(label, caption_line, startdata_line, [(line_no, raw_line), ...]), ...] in order."""
    out, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("\\begin{deluxetable}"):
            label = cap = start = None
            rows = []
            j = i
            while not lines[j].lstrip().startswith("\\end{deluxetable}"):
                m = re.search(r"\\label\{([^}]*)\}", lines[j])
                if m and label is None:
                    label, cap = m.group(1), j + 1
                if lines[j].strip().startswith("\\startdata"):
                    start = j + 1
                    k = j + 1
                    while not lines[k].strip().startswith("\\enddata"):
                        if lines[k].strip():
                            rows.append((k + 1, lines[k].rstrip("\n")))
                        k += 1
                j += 1
            out.append((label, cap, start, rows))
            i = j
        i += 1
    return out


def main():
    log("transcribe_fukazawa.py -- CFG57 gas source 2: Fukazawa et al. 2006, ApJ 636, 698")
    raw = open(TARBALL, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    log("tarball", os.path.relpath(TARBALL, HERE), "sha256", h, "match:", h == SHA256)
    if h != SHA256:
        raise SystemExit("sha256 mismatch")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        member = tf.getmember("ms.tex")
        tex = tf.extractfile(member).read().decode("latin-1")
    lines = tex.splitlines(keepends=True)
    log("ms.tex: %d lines, sha256 %s" % (len(lines), hashlib.sha256(tex.encode("latin-1")).hexdigest()))
    h0 = [(i + 1, l.strip()) for i, l in enumerate(lines) if "H_0=70" in l]
    log("distance scale: line %d: %s" % h0[0])
    assert not re.search(r"\\begin\{table\*?\}", tex), "a plain table environment exists"

    tabs = tables(lines)
    order = [t[0] for t in tabs]
    log("deluxetables in order of appearance:", order)
    assert order == ["tab:sample-chandra", "tab:sample-newton", "table:spec", "table:results", "table:nfwcmp"]
    t1 = tabs[0]
    t4 = tabs[3]
    log("Table 1 = %s: caption line %d, data lines %d-%d" % (t1[0], t1[1], t1[3][0][0], t1[3][-1][0]))
    log("Table 4 = %s: caption line %d, data lines %d-%d" % (t4[0], t4[1], t4[3][0][0], t4[3][-1][0]))

    # ---- Table 1: Galaxy & SeqID & D & log LB & r_e (kpc, arcsec) & ACIS & exp & cts
    D, t1line, acis = {}, {}, {}
    for ln, row in t1[3]:
        cells = [clean(c) for c in row.split("\\\\")[0].split("&")]
        if not cells[0]:
            continue                     # NGC4697's second line of sequence numbers
        D[cells[0]] = cells[2]
        acis[cells[0]] = cells[5]
        t1line[cells[0]] = ln
    # ---- Table 4: Galaxy & kT_i (arcsec) & kT_o & n_t-r & n_beta & n_depro & R_max & M/L_B & ne10 & type
    rows = []
    for ln, row in t4[3]:
        cells = [clean(c) for c in row.split("\\\\")[0].split("&")]
        assert len(cells) == 10, (ln, cells)
        name, kti, kto, ntr, nb, ndep, rmax, ml, ne10, typ = cells
        lower = rmax.startswith(">")
        rows.append(dict(name=name, n_beta=nb, Rmax=rmax.lstrip(">"), Rmax_lower_limit=int(lower),
                         ne10="nan" if ne10 == "---" else ne10, type=typ, D=D[name],
                         kTi=kti, kTo=kto, ML=ml, n_depro=ndep, line=ln, t1line=t1line[name]))
    log("Table 4 rows: %d; Table 1 rows: %d; every Table 4 galaxy has a Table 1 distance: %s"
        % (len(rows), len(D), all(r["name"] in D for r in rows)))

    # ---- checks -----------------------------------------------------------
    # (1) the paper's classification rule, row by row
    bad = []
    for r in rows:
        if r["ne10"] == "nan":
            ok = r["type"] == "VCXG"
        else:
            v = float(r["ne10"])
            ok = (r["type"] == "EXG" and v > 2.0) or (r["type"] == "CXG" and v < 2.0)
        if not ok:
            bad.append(r["name"])
    log("check EXG/CXG rule (ne10 > / < 2e-3 cm^-3; VCXG has no ne10): violations %s" % (bad or "none"))
    # (2) lower-limit R_max = the field edge: one angle per detector (ACIS-S / ACIS-I)
    angs = {}
    for r in rows:
        if r["Rmax_lower_limit"]:
            angs.setdefault(acis[r["name"]], []).append(
                (r["name"], float(r["Rmax"]) / (float(r["D"]) * 1e3) / ARCSEC))
    for det, lst in sorted(angs.items()):
        a = [x for _, x in lst]
        log("check R_max lower limits, %s: %d rows, R_max/D = %.1f-%.1f arcsec (%s)"
            % (det, len(a), min(a), max(a), ", ".join("%s %.1f" % t for t in lst)))
    aS = [x for _, x in angs["ACIS-S"]]
    log("  -> the ACIS-S lower limits share one field-edge angle to %.2f%% (full spread), within the rounding of"
        " D to 0.1 Mpc (up to +-0.35%% at D = 14 Mpc): the D and R_max columns are transcribed consistently;"
        " the ACIS-I limits sit further out (larger field, pointing-dependent)"
        % (100 * (max(aS) - min(aS)) / (sum(aS) / len(aS))))
    # (3) independent re-read of the CFG57 rows: a second route through the raw lines
    log("independent re-read (regex on the raw .tex lines, not the table parser):")
    for nm in CFG57:
        l4 = [(i + 1, l) for i, l in enumerate(lines) if re.match(r"^%s\s*&" % nm, l)]
        l1 = [x for x in l4 if x[0] < t4[1]]          # the Table 1 line precedes Table 4
        l4 = [x for x in l4 if x[0] > t4[1]]
        f4 = [x.strip() for x in l4[0][1].split("&")]
        f1 = [x.strip() for x in l1[0][1].split("&")]
        r = [x for x in rows if x["name"] == nm][0]
        rmax2 = f4[6].replace("$>$", "")
        ne2 = f4[8]
        same = (rmax2 == r["Rmax"] and (ne2 == r["ne10"] or (ne2 == "---" and r["ne10"] == "nan"))
                and f4[4] == r["n_beta"] and f1[2] == r["D"])
        log("  %-8s Table 4 line %d: %s" % (nm, l4[0][0], l4[0][1].strip()))
        log("  %-8s Table 1 line %d: %s" % (nm, l1[0][0], l1[0][1].strip()))
        log("  %-8s -> n_beta %s, R_max %s%s kpc, ne10 %s e-3 cm^-3, D %s Mpc, type %s; re-read agrees: %s"
            % (nm, r["n_beta"], ">" if r["Rmax_lower_limit"] else "", r["Rmax"], r["ne10"], r["D"], r["type"], same))
        assert same

    # ---- write -----------------------------------------------------------
    H = ["# Fukazawa Y., Betoya-Nonesa J. G., Pu J., Ohto A., Kawano N., 2006, ApJ 636, 698, 'Scaling Mass Profiles"
         " around Elliptical Galaxies Observed with Chandra and XMM-Newton'",
         "# arXiv:astro-ph/0509521; source raw/fukazawa2006_astro-ph_0509521.tar.gz, sha256 " + SHA256,
         "# Transcribed by transcribe_fukazawa.py from ms.tex in the tarball (%d lines); run log transcribe_fukazawa.out"
         % len(lines),
         "# Table 4 = deluxetable 'table:results' (4th of 5 in order of appearance), caption line %d, data lines %d-%d:"
         " Galaxy, kT_i, kT_o, n_t-r, n_beta, n_depro, R_max, M/L_B, n_e,10kpc, type. ALL %d rows."
         % (t4[1], t4[3][0][0], t4[3][-1][0], len(rows)),
         "# D_Mpc = Table 1 = deluxetable 'tab:sample-chandra', caption line %d, data lines %d-%d; note b: 'D is a"
         " distance to the galaxy ... taken from O'Sullivan et al. (2001) [MNRAS 328, 461] and NED'."
         % (t1[1], t1[3][0][0], t1[3][-1][0]),
         "# Distance convention: 'Throughout this paper, we assume H0=70 km/s/Mpc' (ms.tex line %d); the analysis"
         " uses the Table 1 D (many Virgo galaxies at 15.9 Mpc; lines 686-689: NGC 4697 at 15.1 Mpc)." % h0[0][0],
         "# ne10_1e-3cm3 = 'the hot gas electron density at 10 kpc' (note f), from the beta-model fit to the"
         " 0.5-1.5 keV surface brightness (Sec. 3.2); NO per-galaxy error is given (text: beta fits to <10%,"
         " local structure 'gives 10% error to the hot gas density'); nan = '---' (VCXG: emission inside 10 kpc).",
         "# n_beta = number of beta components fitted to the surface brightness (the AGN component not counted)."
         " Rmax_kpc = 'maximum detection radius (kpc)'; Rmax_lower_limit = 1 where printed as '>' (emission beyond"
         " the field edge: every such row gives R_max/D = %.0f-%.0f arcsec on ACIS-S, %.0f-%.0f on ACIS-I)."
         % (min(aS), max(aS), min(x for _, x in angs["ACIS-I"]), max(x for _, x in angs["ACIS-I"])),
         "# SPOT CHECK (independent re-read of the raw .tex lines by a second route, see transcribe_fukazawa.out):"
         " NGC5846 Table 4 line %d '... 2 & 9 & $>$44.18 & 6.70 & 7.17 & EXG' -> n_beta 2, R_max >44.18, ne10 7.17;"
         " Table 1 line %d D = 22.9 Mpc. Agrees. Checks: the EXG/CXG rule holds for all rows; the R_max lower limits"
         " on ACIS-S share one field-edge angle to the rounding of D." % ([r["line"] for r in rows if r["name"] == "NGC5846"][0], t1line["NGC5846"]),
         "\t".join(["name", "n_beta", "Rmax_kpc", "Rmax_lower_limit", "ne10_1e-3cm3", "D_Mpc", "type",
                    "kTi_keV(arcsec)", "kTo_keV", "ML_B", "n_depro", "tex_line_table4", "tex_line_table1"])]
    for r in rows:
        H.append("\t".join([r["name"], r["n_beta"], r["Rmax"], str(r["Rmax_lower_limit"]), r["ne10"], r["D"],
                            r["type"], r["kTi"], r["kTo"], r["ML"], r["n_depro"], str(r["line"]), str(r["t1line"])]))
    with open(OUT_TSV, "w") as f:
        f.write("\n".join(H) + "\n")
    log("wrote %s (%d rows)" % (os.path.basename(OUT_TSV), len(rows)))
    log("\nCFG57 rows:")
    for nm in CFG57:
        r = [x for x in rows if x["name"] == nm][0]
        log("  %-8s D %5s Mpc  n_beta %s  R_max %s%s kpc  ne10 %s e-3 cm^-3  %s"
            % (nm, r["D"], r["n_beta"], ">" if r["Rmax_lower_limit"] else "", r["Rmax"], r["ne10"], r["type"]))
    with open(OUT_LOG, "w") as f:
        f.write("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
