"""Checks for the MUSE-DARK I/II/III table extractions in this folder.

Reads only files in this folder: raw_table_cells.txt (the table cells as read from the arXiv HTML DOM)
and the CSVs. It re-parses the raw LaTeX cells and compares every number to the CSVs, then runs
consistency checks against statements in the papers' text. Writes nothing; run
    python3 checks.py > checks.txt
Exit code 0 only if every check passes.
"""
import csv
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def read_csv(fn):
    with open(os.path.join(HERE, fn), newline="") as f:
        return list(csv.DictReader(f))


def raw_section(element_id, paper):
    """table rows (lines holding ' || ') of the raw block headed '## arXiv:<paper>..., element <element_id>'"""
    txt = open(os.path.join(HERE, "raw_table_cells.txt")).read()
    for b in txt.split("\n## "):
        first = b.splitlines()[0]
        if first.startswith(f"arXiv:{paper}") and first.endswith(f"element {element_id}"):
            return [ln for ln in b.splitlines()[1:] if " || " in ln]
    raise KeyError(element_id)


def split_row(line):
    """cells of one raw row; a trailing '||' (empty last cell) is dropped"""
    cells = [x.strip() for x in re.split(r"\s*\|\|\s*", line)]
    return cells[:-1] if line.rstrip().endswith("||") else cells


PM = re.compile(r"\$\(?(-?[\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}\)?(?:\\times 10\^\{(\d+)\})?\$")


def cell_nums(cell):
    """return (value, plus, minus, exp) for a $v^{+p}_{-m}$ cell, or (value, None, None, None) for a plain number"""
    cell = cell.strip()
    m = PM.search(cell)
    if m:
        return m.group(1), m.group(2), m.group(3), m.group(4)
    m = re.search(r"\$?(-?[\d.]+)\$?", cell)
    return (m.group(1), None, None, None) if m else (None, None, None, None)


# ---------------------------------------------------------------- MUSE-DARK-II Table 3
rows = raw_section("S6.T3", "2603.28856v1")[1:]
csv3 = read_csv("musedarkII_table3_tfr_fits.csv")
check("II T3: 6 data rows in raw and CSV", len(rows) == 6 and len(csv3) == 6, f"raw {len(rows)}, csv {len(csv3)}")
mism = []
for r, c in zip(rows, csv3):
    cells = split_row(r)
    a, ap, am, _ = cell_nums(cells[4])
    b, bp, bm, _ = cell_nums(cells[6])
    bref = cell_nums(cells[5])[0]
    sig = cell_nums(cells[7])[0]
    n = cell_nums(cells[8])[0]
    want = dict(a_slope=a, a_err_plus=ap or "", a_err_minus=am or "", b_zero_point=b, b_err_plus=bp or "",
                b_err_minus=bm or "", b_ref=bref or "", sigma_perp_int_dex=sig, N=n)
    for k, v in want.items():
        if (c[k] or "") != (v or ""):
            mism.append((c["local_reference"], k, c[k], v))
check("II T3: every number in the CSV equals the raw DOM cell", not mism, str(mism[:3]))
# offsets b - b_ref against the text (Sect. 7.1: sTFR -0.42, Ristea -0.37, bTFR 0.00)
off = {(c["mass"], c["local_reference"], c["v_over_sigma0_cut"]): float(c["b_zero_point"]) - float(c["b_ref"])
       for c in csv3 if c["b_ref"]}
check("II T3: bTFR offset b - b_ref = 0.00 (text: 0.00 +0.06 -0.06 dex)", abs(off[("Mbar", "Lelli et al. (2019)", ">1")]) < 1e-9)
check("II T3: sTFR offset vs Ristea b - b_ref = -0.37 (text: -0.37)", abs(off[("Mstar", "Ristea et al. (2024)", ">1")] + 0.37) < 1e-9)
d1, d2 = off[("Mstar", "Reyes et al. (2011)", ">1")], off[("Mstar", "Reyes et al. (2011)", ">2")]
print(f"NOTE  II T3: fiducial sTFR offset vs Reyes from the table's rounded b and b_ref = {d1:+.2f} (v/sigma0 > 1; "
      f"{d2:+.2f} for v/sigma0 > 2); the text prints -0.42: a rounding difference, not an extraction error (mine)")
check("II T3: bTFR scatter is 0.16 dex (the timeline note's 0.10-0.12 is the sTFR's)",
      all(c["sigma_perp_int_dex"] == "0.16" for c in csv3 if c["mass"] == "Mbar"))

# ---------------------------------------------------------------- MUSE-DARK-I Tables 2 and 3
t23 = read_csv("musedarkI_table2_3_halo_model_comparison.csv")
for tab, elem, ntot in (("Table 2", "S5.T2", 127), ("Table 3", "S5.T3", 44)):
    raw = raw_section(elem, "2506.19721v3")[1:]
    got = [(c["model_vs_DC14"], c["more_likely_than_DC14"], c["inconclusive"], c["less_likely_than_DC14"])
           for c in t23 if c["table"] == tab]
    exp = [tuple(split_row(r)) for r in raw]
    check(f"I {tab}: CSV equals raw DOM cells", got == exp)
    sums = {g[0]: int(g[1]) + int(g[2]) + int(g[3]) for g in got}
    check(f"I {tab}: each row sums to {ntot}", all(s == ntot for s in sums.values()), str(sums))
t2 = {c["model_vs_DC14"]: c for c in t23 if c["table"] == "Table 2"}
pct = {m: 100 * (int(t2[m]["inconclusive"]) + int(t2[m]["less_likely_than_DC14"])) / 127 for m in t2}
stated = {"Burkert": 81, "Dekel-Zhao": 84, "Einasto": 82, "coreNFW": 88, "baryons-only": 96}
check("I Table 2 vs text (Sect. 5.1): DC14 as good or better in 81/84/82/88/96 % (paper truncates, does not round)",
      all(math.floor(pct[m]) == v for m, v in stated.items()), ", ".join(f"{m} {pct[m]:.1f}" for m in stated))
check("I Table 2 vs text: NFW ~90 % and baryons-only disfavoured 107/127 = 84 %",
      round(pct["NFW"]) in (90, 91) and math.floor(100 * 107 / 127) == 84, f"NFW {pct['NFW']:.1f}")

# ---------------------------------------------------------------- MUSE-DARK-I Table 5
t5 = read_csv("musedarkI_table5_bestfit_halo_params_3galaxies.csv")
raw = raw_section("A8.T5", "2506.19721v3")[1:]
check("I Table 5: 18 rows (3 galaxies x 6 models) in raw and CSV", len(raw) == 18 and len(t5) == 18)
cols = [("V_vir_kms", "V_vir_err_plus", "V_vir_err_minus"), ("log_M_vir_Msun", "log_M_vir_err_plus", "log_M_vir_err_minus"),
        ("c_vir", "c_vir_err_plus", "c_vir_err_minus"), ("r_s_kpc", "r_s_err_plus", "r_s_err_minus"),
        ("rho_s_mantissa", "rho_s_mantissa_err_plus", "rho_s_mantissa_err_minus"),
        ("log_X", "log_X_err_plus", "log_X_err_minus"), ("alpha_einasto", "alpha_einasto_err_plus", "alpha_einasto_err_minus")]
mism = []
for r, c in zip(raw, t5):
    cells = split_row(r)
    if cells[0] != c["muse_id"] or cells[1] != c["model"]:
        mism.append(("id/model", cells[:2], c["muse_id"], c["model"]))
    for i, (kv, kp, km) in enumerate(cols):
        cell = cells[2 + i] if 2 + i < len(cells) else ""
        v, p, m, e = cell_nums(cell) if cell else ("", "", "", None)
        if (c[kv], c[kp], c[km]) != (v or "", p or "", m or ""):
            mism.append((c["muse_id"], c["model"], kv, (c[kv], c[kp], c[km]), (v, p, m)))
        if kv == "rho_s_mantissa":
            if (c["rho_s_exp10"] != (e or "")):
                mism.append((c["muse_id"], c["model"], "exp", c["rho_s_exp10"], e))
            if (c["rho_s_is_density_at_150pc"] == "yes") != ("*" in cell):
                mism.append((c["muse_id"], c["model"], "star flag"))
check("I Table 5: every number (value, +err, -err, 10^k, * flag) equals the raw DOM cell", not mism, str(mism[:3]))
odd = [(c["muse_id"], c["model"]) for c in t5 if c["rho_s_mantissa_err_minus"] and float(c["rho_s_mantissa_err_minus"]) > float(c["rho_s_mantissa"])]
print(f"NOTE  I Table 5: rows whose printed rho_s lower error exceeds the value (as printed, not corrected): {odd}")

# ---------------------------------------------------------------- MUSE-DARK-I Tables 1 and 4
t1 = read_csv("musedarkI_table1_mock_initial_conditions.csv")
raw = raw_section("S3.T1", "2506.19721v3")[2:]
exp = [split_row(r) for r in raw]
got = [list(c.values()) for c in t1]
check("I Table 1 (mock galaxies): CSV equals raw DOM cells", got == exp)
t4 = read_csv("musedarkI_table4_free_parameters_by_model.csv")
raw = raw_section("A1.T4", "2506.19721v3")[1:]
sym = {"✓": "yes", "✗": "no", "✓/✗": "yes/no", "": ""}
ok = len(raw) == len(t4)
for r, c in zip(raw, t4):
    cells = split_row(r)
    vals = [sym.get(x, "?") for x in cells[1:]] + [""] * (9 - len(cells[1:]))
    ok &= vals[:9] == [c[k] for k in ["URC", "DC14", "NFW", "Dekel-Zhao", "Burkert", "coreNFW", "Einasto", "baryons-only", "Bulge"]]
check("I Table 4: every tick/cross equals the raw DOM cell", ok)
dc = {c["parameter"]: c for c in t4}
check("I Table 4: DC14 and Dekel-Zhao fit X, not M*; NFW/Burkert/coreNFW/Einasto/baryons-only fit M*",
      dc["X"]["DC14"] == "yes" and dc["Stellar Mass (M_star)"]["DC14"] == "no" and dc["X"]["Dekel-Zhao"] == "yes"
      and all(dc["Stellar Mass (M_star)"][m] == "yes" for m in ["NFW", "Burkert", "coreNFW", "Einasto", "baryons-only"]))

# ---------------------------------------------------------------- MUSE-DARK-II Tables 1, 2, 4 (row counts)
for fn, elem, n in (("musedarkII_table1_kinematic_priors.csv", "S4.T1", 8), ("musedarkII_table2_sed_priors.csv", "S5.T2", 8),
                    ("musedarkII_table4_observations.csv", "A1.T4", 4)):
    check(f"II {elem}: {n} rows in the CSV", len(read_csv(fn)) == n)

# ---------------------------------------------------------------- MUSE-DARK-III stated results
s3 = read_csv("musedarkIII_stated_results_NOT_A_TABLE.csv")
get = lambda q, fw: next(float(c["value"]) for c in s3 if c["quantity"].startswith(q) and c["framework"].startswith(fw))
a00, a1 = get("a0(0) in", "DC14"), get("a1 in", "DC14")
check("III: a0(0) + a1 z reaches the abstract's 2.38 at z = 0.87 (the timeline note's reading)", abs(a00 + a1 * 0.87 - 2.383) < 1e-3)
check("III: Eq. 2 and Eq. 4 errors are recorded as 95% CI (stated in Sect. 3.1 and 3.2)",
      all("95% CI" in c["error_convention_as_stated"] for c in s3 if "Eq. 2" in c["source_in_paper"] or "Eq. 4" in c["source_in_paper"]))

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks pass")
sys.exit(0 if all(RESULTS) else 1)
