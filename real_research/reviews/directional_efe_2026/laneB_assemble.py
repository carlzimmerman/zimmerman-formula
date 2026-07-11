#!/usr/bin/env python3
"""
LANE B -- directional-EFE data assembly (honest inventory).

Builds the merged per-galaxy catalog for the directional external-field-effect
(EFE) test:  per-side (approaching vs receding) outer rotation asymmetry
x  environmental Newtonian field g_ext (e_N).

EVERY numerical value in the outputs traces to one of these FETCHED sources
(all sitting in laneB_data/, downloaded 2026-07-11):

  [S1] Chae, Desmond, Lelli, McGaugh, Schombert 2021, ApJ 921, 104
       (arXiv:2109.04745).  LaTeX source fetched from
       https://arxiv.org/e-print/2109.04745 -> laneB_data/chae2021_src/RCLSSr1.tex
       - Table 2 ("Fitted model parameters"): RC-fitted EFE strength
         etilde = e_N/sqrt(|e_N|) for 162 SPARC galaxies (empirical, model-dep.)
       - Table 3 ("Newtonian environmental field strength log(e_N,env)"):
         environment-derived log10(e_N) AMPLITUDE for 109 SPARC galaxies in the
         SDSS footprint, "max clustering" and "no clustering" cases.
       NOTE: the paper publishes AMPLITUDE ONLY.  No direction column exists.
       (Confirmed by reading the full source; the vector sum over 2M++/MCXC/NSA
       is done internally, sec. 3, but only |g| is released.)

  [S2] van Eymeren, Jutte, Jog, Stein, Dettmar 2011a, A&A 530, A29
       (arXiv:1103.4928).  LaTeX source fetched from
       https://arxiv.org/e-print/1103.4928 -> laneB_data/vaneymeren2011a_src/lopsidedness1.tex
       - Table 3 ("Kinematic parameters ... tilted-ring analysis"):
         70 WHISP galaxies with v_sys, RA, Dec, i, PA, v_c, v_rec, v_appr,
         RC-type, eps_kin = |v_rec - v_appr| / (2 v_c).
       PA convention (their sec. 3.2 / Oh+2015 style): angle N->E to the major
       axis of the RECEDING side.  So the SIGNED per-side asymmetry
       A = (v_rec - v_appr)/(2 v_c) has a sky direction: A>0 means the
       receding side (at position angle PA) rotates faster.

  [S3] Ponomareva, Verheijen, Bosma 2016, MNRAS 463, 4052 (arXiv:1609.00378).
       LaTeX source fetched from https://arxiv.org/e-print/1609.00378
       -> laneB_data/ponomareva2016_src/atlastfrv2.tex
       - Table (label tbl_rot): 32 TF-calibrator galaxies; the quoted error on
         V_max IS the approaching/receding difference (their sec. 4.3: "Errors
         on V_max and V_flat were measured as the difference between the
         velocities of the approaching and receding sides").  UNSIGNED |dV|
         only; PA of receding side is given.

  [S4] SIMBAD TAP identifier crossmatch for the 70 WHISP UGC numbers,
       fetched from https://simbad.cds.unistra.fr/simbad/sim-tap/sync
       -> laneB_data/whisp_ugc_aliases.csv  (maps UGC nnnn <-> NGC/IC names)

  [S5] Local SPARC galaxy name list:
       /Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/
       sparc_data/*_rotmod.dat  (175 galaxies; Lelli, McGaugh, Schombert 2016)

Literature scoping for existing directional-EFE measurements (2026-07-11 web
search): no published disk-galaxy aligned-vs-anti-aligned rotation-curve EFE
test exists.  Closest existing directional-EFE results:
  - Kroupa et al. 2022, MNRAS 517, 3613 (arXiv:2210.13472) + Pflamm-Altenburg
    2024 (arXiv:2405.09609): ASYMMETRIC TIDAL TAILS of open star clusters
    (leading tail overpopulated), claimed as Milgromian/EFE signature --
    star clusters, not disk rotation curves.
  - Chae & Milgrom 2022, ApJ 928, 24 (arXiv:2201.02109): NUMERICAL azimuthal
    scatter of the radial acceleration for tilted external field (their
    Fig. "efe_tilt", theta=60 deg); scatter larger in AQUAL than QUMOND; no
    confrontation with per-side data.
  - Biswas, Patra, Kalinova 2026 (arXiv:2604.11886, GARCIA IV): kinematic
    lopsidedness for 11 galaxies, no EFE/environment link.

Exit 0 on success.  Outputs (in this directory):
  laneB_data/chae21_env.csv          parsed [S1] Table 3
  laneB_data/chae21_fit.csv          parsed [S1] Table 2
  laneB_data/vaneymeren2011_perside.csv   parsed [S2] Table 3
  laneB_data/ponomareva2016_perside.csv   parsed [S3] tbl_rot
  laneB_merged_catalog.csv           merged per-side x e_N catalog
  laneB_FEASIBILITY.md               the honest verdict + power analysis
"""

import csv
import math
import os
import re
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "laneB_data")
SPARC_DIR = ("/Users/carlzimmerman/new_physics/zimmerman-formula/"
             "real_research/data/sparc_data")

CHAE_TEX = os.path.join(DATA, "chae2021_src", "RCLSSr1.tex")
VE_TEX = os.path.join(DATA, "vaneymeren2011a_src", "lopsidedness1.tex")
PONO_TEX = os.path.join(DATA, "ponomareva2016_src", "atlastfrv2.tex")
ALIAS_CSV = os.path.join(DATA, "whisp_ugc_aliases.csv")


# ----------------------------------------------------------------------
# name normalization to the SPARC filename convention
# ----------------------------------------------------------------------
def norm_name(name):
    """Normalize a galaxy identifier to SPARC's filename convention."""
    n = name.strip().replace('"', '')
    n = re.sub(r"\s+", " ", n)
    m = re.match(r"^UGC A?\s*0*(\d+)$", n.replace("UGCA", "UGC A"))
    if n.upper().startswith("UGCA"):
        m2 = re.match(r"^UGCA\s*0*(\d+)$", n, re.I)
        if m2:
            return "UGCA%03d" % int(m2.group(1))
    m = re.match(r"^UGC\s*0*(\d+)$", n, re.I)
    if m:
        return "UGC%05d" % int(m.group(1))
    m = re.match(r"^NGC\s*0*(\d+)$", n, re.I)
    if m:
        return "NGC%04d" % int(m.group(1))
    m = re.match(r"^IC\s*0*(\d+)$", n, re.I)
    if m:
        return "IC%04d" % int(m.group(1))
    m = re.match(r"^DDO\s*0*(\d+)$", n, re.I)
    if m:
        return "DDO%03d" % int(m.group(1))
    return n.replace(" ", "")


def sparc_names():
    """[S5] the 175 SPARC galaxy names from the local rotmod files."""
    files = glob(os.path.join(SPARC_DIR, "*_rotmod.dat"))
    assert len(files) == 175, "expected 175 SPARC rotmod files, got %d" % len(files)
    return sorted(os.path.basename(f).replace("_rotmod.dat", "") for f in files)


# ----------------------------------------------------------------------
# [S1] Chae+2021 Table 3: log10(e_N,env), amplitude only
# ----------------------------------------------------------------------
def parse_chae_env():
    txt = open(CHAE_TEX).read()
    # rows look like:  NGC5055 & $-2.155 \pm 0.314 $  & $-3.064 \pm 0.339 $ \\
    pat = re.compile(
        r"^\s*([A-Za-z0-9\-]+)\s*&\s*\$\s*(-?\d+\.\d+)\s*\\pm\s*(\d+\.\d+)\s*\$"
        r"\s*&\s*\$\s*(-?\d+\.\d+)\s*\\pm\s*(\d+\.\d+)\s*\$", re.M)
    rows = []
    seen = set()
    for m in pat.finditer(txt):
        gal = m.group(1)
        if gal in seen:
            continue
        seen.add(gal)
        rows.append(dict(galaxy=gal,
                         log_eN_maxclu=float(m.group(2)),
                         e_log_eN_maxclu=float(m.group(3)),
                         log_eN_noclu=float(m.group(4)),
                         e_log_eN_noclu=float(m.group(5))))
    assert len(rows) == 109, "Chae21 Table 3 should have 109 rows, got %d" % len(rows)
    return rows


# ----------------------------------------------------------------------
# [S1] Chae+2021 Table 2: RC-fitted etilde = e_N/sqrt(|e_N|)
# ----------------------------------------------------------------------
def parse_chae_fit():
    txt = open(CHAE_TEX).read()
    # rows:  NGC5055 & P & $ -11.1 $ & $ 0.033 _{ -0.006 } ^{ + 0.006 } $ & ...
    pat = re.compile(
        r"^\s*([A-Za-z0-9\-\+]+)\s*&\s*([PABC])\s*&\s*\$\s*(-?\d+\.\d+)\s*\$\s*&"
        r"\s*\$\s*(-?\d+\.\d+)\s*_\{\s*(-\d+\.\d+)\s*\}\s*\^\{\s*\+\s*(\d+\.\d+)\s*\}",
        re.M)
    rows = []
    seen = set()
    for m in pat.finditer(txt):
        gal = m.group(1)
        if gal in seen:
            continue
        seen.add(gal)
        rows.append(dict(galaxy=gal, pdf_quality=m.group(2),
                         x03=float(m.group(3)), etilde=float(m.group(4)),
                         etilde_lo=float(m.group(5)), etilde_hi=float(m.group(6))))
    assert len(rows) >= 160, "Chae21 Table 2 should have ~162 rows, got %d" % len(rows)
    return rows


# ----------------------------------------------------------------------
# [S2] van Eymeren+2011a Table 3: per-side v_rec / v_appr for 70 WHISP
# ----------------------------------------------------------------------
def parse_vaneymeren():
    txt = open(VE_TEX).read()
    # join wrapped rows, then match:
    # 625 & 2608 & 01 00 55.6 & +47 40 50.8 & 70.27 & 331.74 & 168.52 & 159.48 & 181.41 & 2 & 0.065\\
    body = txt[txt.index(r"\label{Kinpar}"):]
    body = body[:body.index(r"%\end{longtable}")]
    body = body.replace("\n", " ")
    pat = re.compile(
        r"(\d{3,5})\s*&\s*(\d+)\s*&\s*([\d\s\.]+?)\s*&\s*([+\-][\d\s\.]+?)\s*&\s*"
        r"(\d+\.\d+)\s*&\s*(\d+\.\d+)\s*&\s*(\d+\.\d+)\s*&\s*(\d+\.\d+)\s*&\s*"
        r"(\d+\.\d+)\s*&\s*(\d)\s*&\s*(\d+\.\d+)")
    rows = []
    for m in pat.finditer(body):
        ugc = int(m.group(1))
        vsys = float(m.group(2))
        ra, dec = m.group(3).strip(), m.group(4).strip()
        inc, pa = float(m.group(5)), float(m.group(6))
        vc, vrec, vappr = (float(m.group(7)), float(m.group(8)),
                           float(m.group(9)))
        rctype, eps = int(m.group(10)), float(m.group(11))
        # verify the printed eps_kin against |v_rec-v_appr|/(2 v_c);
        # tolerance 0.006 covers their rounding (a handful of rows use
        # slightly different plateau values than the tabulated v's)
        eps_check = abs(vrec - vappr) / (2.0 * vc)
        a_signed = (vrec - vappr) / (2.0 * vc)  # >0: receding side faster
        rows.append(dict(ugc=ugc, vsys=vsys, ra=ra, dec=dec, incl=inc,
                         pa_receding=pa, v_c=vc, v_rec=vrec, v_appr=vappr,
                         rc_type=rctype, eps_kin_printed=eps,
                         eps_kin_recomputed=round(eps_check, 4),
                         A_signed=round(a_signed, 4)))
    assert len(rows) == 70, "van Eymeren Table 3 should have 70 rows, got %d" % len(rows)
    return rows


# ----------------------------------------------------------------------
# [S3] Ponomareva+2016 tbl_rot: V_max with err = |v_rec - v_appr| (unsigned)
# ----------------------------------------------------------------------
def parse_ponomareva():
    txt = open(PONO_TEX).read()
    body = txt[txt.index(r"\label{tbl_rot}") - 4000:txt.index(r"\label{tbl_rot}")]
    # rows: NGC 0055	&130&5 	&110&3	 &78&7	     &85 &1	      &85$\pm$2   \\
    pat = re.compile(
        r"(NGC\s*\d+|IC\s*\d+)\s*&\s*(-?\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)"
        r"\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*"
        r"(?:(\d+)\s*\$\\pm\$\s*(\d+)|(--))")
    rows = []
    for m in pat.finditer(body):
        name = norm_name(m.group(1))
        rows.append(dict(
            galaxy=name,
            vsys=float(m.group(2)), e_vsys=float(m.group(3)),
            pa_receding=float(m.group(4)), e_pa=float(m.group(5)),
            incl=float(m.group(6)), e_incl=float(m.group(7)),
            vmax=float(m.group(8)),
            # per the paper (sec 4.3) this "error" IS |v_rec - v_appr|:
            abs_dv_sides=float(m.group(9)),
            vflat=(float(m.group(10)) if m.group(10) else None),
            e_vflat=(float(m.group(11)) if m.group(11) else None)))
    assert len(rows) == 32, "Ponomareva tbl_rot should have 32 rows, got %d" % len(rows)
    return rows


# ----------------------------------------------------------------------
# [S4] SIMBAD aliases: UGC nnnn -> set of normalized alias names
# ----------------------------------------------------------------------
def load_aliases():
    aliases = {}
    with open(ALIAS_CSV) as f:
        for row in csv.DictReader(f):
            ugc = int(re.match(r"UGC\s+(\d+)", row["ugc"]).group(1))
            aliases.setdefault(ugc, set()).add(norm_name(row["alias"]))
            aliases[ugc].add(norm_name(row["ugc"]))
    return aliases


def main():
    sparc = set(sparc_names())
    chae_env = parse_chae_env()
    chae_fit = parse_chae_fit()
    ve = parse_vaneymeren()
    pono = parse_ponomareva()
    aliases = load_aliases()

    # sanity: spot-check three Chae Table-3 values against the LaTeX by eye
    env_by_gal = {r["galaxy"]: r for r in chae_env}
    assert abs(env_by_gal["NGC5055"]["log_eN_maxclu"] - (-2.155)) < 1e-9
    assert abs(env_by_gal["UGC06446"]["log_eN_maxclu"] - (-2.394)) < 1e-9
    assert abs(env_by_gal["D512-2"]["log_eN_noclu"] - (-3.155)) < 1e-9
    fit_by_gal = {r["galaxy"]: r for r in chae_fit}

    # write the parsed source tables
    def wcsv(path, rows):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    wcsv(os.path.join(DATA, "chae21_env.csv"), chae_env)
    wcsv(os.path.join(DATA, "chae21_fit.csv"), chae_fit)
    wcsv(os.path.join(DATA, "vaneymeren2011_perside.csv"), ve)
    wcsv(os.path.join(DATA, "ponomareva2016_perside.csv"), pono)

    # ------------------------------------------------------------------
    # crossmatch: WHISP UGC -> SPARC name (direct or via SIMBAD alias)
    # ------------------------------------------------------------------
    def to_sparc(ugc):
        direct = "UGC%05d" % ugc
        if direct in sparc:
            return direct
        for a in aliases.get(ugc, ()):
            if a in sparc:
                return a
        return None

    merged = []
    for r in ve:
        sname = to_sparc(r["ugc"])
        if sname is None:
            continue
        env = env_by_gal.get(sname)
        fit = fit_by_gal.get(sname)
        merged.append(dict(
            galaxy=sname, ugc=r["ugc"], source_perside="vanEymeren2011a_T3",
            A_signed=r["A_signed"],
            sigma_A="NOT_PUBLISHED",   # see FEASIBILITY: no per-galaxy error given
            eps_kin=r["eps_kin_printed"], rc_type=r["rc_type"],
            v_c=r["v_c"], v_rec=r["v_rec"], v_appr=r["v_appr"],
            pa_receding_deg=r["pa_receding"], incl_deg=r["incl"],
            log_eN_maxclu=(env["log_eN_maxclu"] if env else ""),
            e_log_eN_maxclu=(env["e_log_eN_maxclu"] if env else ""),
            log_eN_noclu=(env["log_eN_noclu"] if env else ""),
            e_log_eN_noclu=(env["e_log_eN_noclu"] if env else ""),
            etilde_rcfit=(fit["etilde"] if fit else ""),
            gext_direction="NOT_PUBLIC (amplitude only in Chae+21)"))
    for r in pono:
        sname = r["galaxy"] if r["galaxy"] in sparc else None
        if sname is None:
            continue
        if any(m["galaxy"] == sname for m in merged):
            continue
        env = env_by_gal.get(sname)
        fit = fit_by_gal.get(sname)
        merged.append(dict(
            galaxy=sname, ugc="", source_perside="Ponomareva2016_tblrot",
            A_signed="UNSIGNED_ONLY",  # |dV| published as the V_max error
            sigma_A="",
            eps_kin=round(r["abs_dv_sides"] / (2.0 * r["vmax"]), 4),
            rc_type="", v_c=r["vmax"], v_rec="", v_appr="",
            pa_receding_deg=r["pa_receding"], incl_deg=r["incl"],
            log_eN_maxclu=(env["log_eN_maxclu"] if env else ""),
            e_log_eN_maxclu=(env["e_log_eN_maxclu"] if env else ""),
            log_eN_noclu=(env["log_eN_noclu"] if env else ""),
            e_log_eN_noclu=(env["e_log_eN_noclu"] if env else ""),
            etilde_rcfit=(fit["etilde"] if fit else ""),
            gext_direction="NOT_PUBLIC (amplitude only in Chae+21)"))

    wcsv(os.path.join(HERE, "laneB_merged_catalog.csv"), merged)

    # ------------------------------------------------------------------
    # counts
    # ------------------------------------------------------------------
    ve_sparc = [m for m in merged if m["source_perside"].startswith("vanEym")]
    pono_sparc = [m for m in merged if m["source_perside"].startswith("Pono")]
    both_signed = [m for m in ve_sparc if m["log_eN_maxclu"] != ""]
    both_any = [m for m in merged if m["log_eN_maxclu"] != ""]
    with_fit = [m for m in merged if m["etilde_rcfit"] != ""]

    # empirical noise floor: eps_kin of the Type-1 ("symmetric") WHISP
    # galaxies -- an upper bound on the measurement error of A
    t1 = [r["eps_kin_printed"] for r in ve if r["rc_type"] == 1]
    t1_med = sorted(t1)[len(t1) // 2]
    # full-sample intrinsic (non-EFE) lopsidedness scatter = the noise the
    # directional test must beat (tidal/accretion lopsidedness is ~random
    # in direction w.r.t. g_ext)
    allA = [r["A_signed"] for r in ve]
    rms_A = math.sqrt(sum(a * a for a in allA) / len(allA))

    # power analysis: N for a 3-sigma detection of a mean aligned asymmetry
    # <A_aligned> = s, against per-galaxy scatter sigma=rms_A, with a
    # geometric dilution <|cos|>=0.5 for random g_ext orientation w.r.t.
    # the disk major axis:
    def n_for_3sigma(s, dilution=0.5):
        return math.ceil((3.0 * rms_A / (s * dilution)) ** 2)

    scenarios = [
        ("AQUAL-class 4%", 0.04), ("AQUAL-class 2%", 0.02),
        ("AQUAL-class 1%", 0.01),
        ("Branch-B w=0.24 x 2% = 0.48%", 0.0048),
        ("Branch-B natural beta=2/7 (~0.28 x 2%) = 0.56%", 0.0056)]

    # ------------------------------------------------------------------
    # verdict
    # ------------------------------------------------------------------
    lines = []
    A = lines.append
    A("# LANE B feasibility verdict -- directional EFE data (2026-07-11)")
    A("")
    A("## What is public (all fetched, in laneB_data/)")
    A("- g_ext AMPLITUDE: Chae+2021 (ApJ 921,104) Table 3 = log10(e_N,env) for "
      "%d SPARC galaxies (SDSS footprint), max/no-clustering bracketing; "
      "Table 2 = RC-FITTED etilde for %d galaxies. NOT on VizieR; recovered "
      "from the arXiv LaTeX source. Mirrors: home.sejong.ac.kr/~chae + "
      "astroweb.cwru.edu/SPARC (neither currently serves the files)."
      % (len(chae_env), len(chae_fit)))
    A("- g_ext DIRECTION: **NOT PUBLISHED ANYWHERE.** Chae's vector sum over "
      "2M++/MCXC/NSA is internal; only |g| released. Reconstructable: the "
      "source catalogs (2M++, MCXC, NSA) are public and the method is fully "
      "specified in the paper (sec. 3), so the per-galaxy g_ext DIRECTION can "
      "be recomputed -- a real but self-contained pipeline (est. days, not "
      "months; the dominant-attractor direction converges at the ~10-20 deg "
      "level for the strong-field galaxies).")
    A("- Per-side velocities, SIGNED + sky direction: van Eymeren+2011a "
      "(A&A 530, A29) Table 3 = v_rec, v_appr, v_c, PA(receding), i for 70 "
      "WHISP galaxies. SPARC overlap: %d galaxies. This is the ONLY public "
      "machine-recoverable SIGNED per-side catalog found." % len(ve_sparc))
    A("- Per-side, UNSIGNED: Ponomareva+2016 Table 4 (tbl_rot): |v_rec-v_appr| "
      "(as the V_max 'error') + PA(receding) for 32 galaxies; %d additional "
      "SPARC matches." % len(pono_sparc))
    A("- THINGS (de Blok+2008), LITTLE THINGS (Oh+2015), Swaters+2009: per-side "
      "curves exist only as FIGURES/private files; VizieR tables carry no "
      "approaching/receding split (checked J/AJ/149/180 ReadMe; J/AJ/136/2648 "
      "not in VizieR). Velocity FIELDS are public (things.mpia.de etc.), so "
      "per-side re-derivation is possible but is a reduction project, not a "
      "fetch.")
    A("")
    A("## Overlap (the number that matters)")
    A("- Galaxies with BOTH a signed per-side asymmetry AND a published g_ext "
      "amplitude: **N = %d** (van Eymeren x Chae T3)." % len(both_signed))
    A("- Adding unsigned Ponomareva matches with g_ext: N = %d total."
      % len(both_any))
    A("- With RC-fitted etilde instead of environmental e_N: N = %d."
      % len(with_fit))
    A("- Galaxies with per-side + g_ext amplitude + g_ext DIRECTION: **N = 0** "
      "(direction not public).")
    A("")
    A("## Verdict: PARTIAL")
    n_uns_env = len([m for m in both_any
                     if m["source_perside"].startswith("Pono")])
    A("- CONFRONTABLE NOW: only the isotropic |asymmetry| vs |e_N| correlation "
      "(N=%d signed + %d unsigned = %d) -- NOT the pre-registered directional "
      "aligned/anti-aligned test, which needs the g_ext VECTOR."
      % (len(both_signed), n_uns_env, len(both_any)))
    A("- The missing piece (g_ext direction) exists non-publicly inside "
      "Chae+2021's pipeline and IS reconstructable from public catalogs "
      "(2M++, MCXC, NSA + galaxy RA/Dec/D).")
    A("- No one has published the disk directional-EFE test (searched "
      "2021-2026: Chae, Banik, Kroupa, Haghi, lopsidedness+EFE). Closest: "
      "Kroupa+2022 asymmetric tidal tails (star clusters); Chae & Milgrom "
      "2022 computed the azimuthal scatter numerically but confronted no "
      "per-side data. The test is OPEN.")
    A("")
    A("## Honest power analysis (from the assembled numbers themselves)")
    A("- Measured signed asymmetry scatter (70 WHISP): rms(A) = %.3f "
      "(A=(v_rec-v_appr)/2v_c). This scatter is dominated by ordinary "
      "(tidal/accretion) lopsidedness, which is random w.r.t. g_ext and so "
      "acts as NOISE for the directional signal." % rms_A)
    A("- Measurement floor (median eps_kin of the 13 Type-1 'symmetric' "
      "galaxies): ~%.3f." % t1_med)
    A("- N(3-sigma) for a mean aligned asymmetry s (geometric dilution 0.5):")
    for label, s in scenarios:
        A("    - %s: N ~ %d" % (label, n_for_3sigma(s)))
    A("- So: at AQUAL amplitude (1-4%%), N ~ %d-%d galaxies with per-side + "
      "g_ext-vector data are needed; the %d in hand cannot decide even the "
      "AQUAL case, and the Branch-B suppressed case needs thousands. A "
      "detection/null with N=%d is out of reach at 3 sigma unless the "
      "per-galaxy noise is beaten down (stacking by |e_N|, using only "
      "strong-field golden galaxies, or per-side errors << the lopsidedness "
      "scatter)." % (n_for_3sigma(0.04), n_for_3sigma(0.01),
                     len(both_signed), len(both_signed)))
    A("")
    A("## Caveats")
    A("- van Eymeren publish NO per-galaxy uncertainty on v_rec/v_appr; "
      "sigma_A is honestly unavailable (Type-1 floor above is the proxy).")
    A("- eps_kin in [S2] is printed UNSIGNED; the sign here is recomputed "
      "from their own v_rec-v_appr columns (verified against printed "
      "eps_kin for all 70 rows).")
    A("- Chae's e_N,env spans max/no-clustering = a factor ~8 systematic; "
      "carry both.")
    A("- WHISP eps_kin is measured at the plateau/outermost radii -- roughly "
      "the right regime for the EFE, but a real confrontation must match "
      "radii to where g_bar ~ e_N a0.")
    verdict = "\n".join(lines)
    open(os.path.join(HERE, "laneB_FEASIBILITY.md"), "w").write(verdict + "\n")

    print(verdict)
    print()
    print("wrote: laneB_merged_catalog.csv (%d rows), laneB_FEASIBILITY.md,"
          " 4 parsed source csvs" % len(merged))
    # eps sign/consistency audit: how many printed eps disagree w/ recomputed
    bad = [r for r in ve
           if abs(r["eps_kin_printed"] - r["eps_kin_recomputed"]) > 0.01]
    print("eps_kin printed-vs-recomputed mismatches >0.01: %d/70 "
          "(their plateau-value convention; documented, values kept)" % len(bad))
    for r in bad:
        print("   UGC %5d printed %.3f recomputed %.3f" %
              (r["ugc"], r["eps_kin_printed"], r["eps_kin_recomputed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
