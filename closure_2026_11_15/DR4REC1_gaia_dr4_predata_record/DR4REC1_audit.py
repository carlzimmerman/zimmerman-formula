#!/usr/bin/env python3
"""DR4REC1 audit: every quoted number and word of the cover note is checked against the committed file it comes from.

Each entry is (what the note says, the file, what must be found in that file). The first string must be in the TeX
source; the last must be in the file. Files are compared after removing markdown asterisks and collapsing whitespace,
so a quotation may cross a line break in its source. Further checks: every digest in the note's table is the start of
the sha256 of its file; the PDF is newer than the TeX and holds single-word markers of the note; no pending marker
is left (reported, and a failure only with --final); no home-directory path in the note.

  python3 DR4REC1_audit.py           audit; a remaining pending marker is reported and does not fail
  python3 DR4REC1_audit.py --final   the same, and a remaining pending marker fails (the publish gate uses this)
  python3 DR4REC1_audit.py --mutate  mutation twin: every file literal altered by one character; every entry must fail

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEX = HERE / "DR4REC1_gaia_dr4_predata_record_2026.tex"
PDF = HERE / "DR4REC1_gaia_dr4_predata_record_2026.pdf"

PREP = "prep_2026/gaia_dr4_prep/"
DP = "dr4_push_2026_11_05/"
MAP = "closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md"
SEAL = "cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md"
D05 = PREP + "OWNER_DECISION_2026-11-05_DR4_FORKS.md"
D05C = PREP + "OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md"
D15 = PREP + "OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md"
D15B = PREP + "OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md"
CQB1 = "closure_2026_11_15/CQB1_cq2_under_blend/RESULT.md"
DP8 = DP + "DP8_release_path_wiring/RESULT.md"

ENTRIES = [
    # abstract
    ("no registered prediction has come true", "predictions_2026/PREDICTIONS_SCORECARD_2026-11-12.md",
     "No registered prediction has come true."),
    # Section 1
    ("made on 2026-11-04", SEAL, "Sealed 2026-11-04"),
    ("screened and Newtonian", SEAL, "v3s wide binaries are screened and Newtonian"),
    ("$4.45\\times10^{-5}$", SEAL, "[canonical] NEWTONIAN: max γ_r − 1 4.45e-05"),
    ("$4.01\\times10^{-5}$", SEAL, "[alt] NEWTONIAN: max γ_r − 1 4.01e-05"),
    ("identical to Newton's in every realisation", SEAL, "γ_inf identical to Newton's in every realisation"),
    ("NOT SEPARABLE on both footings", SEAL, "[canonical] V3S vs plain QUMOND: 2.62, 5.27 → SEPARABLE; V3S vs Newton: 0.0000, 0.0000 → NOT SEPARABLE"),
    ("NOT SEPARABLE on both footings", SEAL, "[alt] V3S vs plain QUMOND: 2.86, 7.08 → SEPARABLE; V3S vs Newton: 0.0000, 0.0000 → NOT SEPARABLE"),
    ("$1.149\\pm0.027$ canonical and $1.208\\pm0.007$ alternative", D05, "1.149 ± 0.027 / 1.208 ± 0.007"),
    ("it adds no rule", SEAL, "this seal adds no rule"),
    ("On 2026-11-07 the record replaced v3s's stiffness", "closure_2026_11_07/OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md",
     "v3s's stiffness is the blend."),
    # Section 2
    ("$\\hat\\gamma-1\\ge3\\sigma$", D05, "γ̂ − 1.000 ≥ 3σ, and γ̂ not below the law-first anchor by ≥ 3σ"),
    ("anchor $-\\,\\hat\\gamma\\ge3\\sigma$", D05, "anchor − γ̂ ≥ 3σ"),
    ("1.1614 canonical and 1.1917 alternative", D05, "Arm A floor (A10) | 1.1614 / 1.1917"),
    ("0.048 or more (canonical), or 0.058 or more (alternative)", D05, "σ_sys(b) < 0.048 canonical / 0.058 alt (D2 A1)"),
    ("$\\hat\\gamma>1.23$ (the guard zone)", D05, "γ̂ > 1.23 is no verdict for every arm"),
    ("$\\hat\\gamma\\le1-3\\sigma$ (sub-Newtonian)", D05, "γ̂ ≤ 1 − 3σ is NO VERDICT for every reading"),
    ("the reading is BOTH EXCLUDED", D05, "the reading is BOTH EXCLUDED"),
    ("$R-1\\ge\\max(0.01,\\,3\\sigma_R)$", D05, "KILL iff R − 1 ≥ max(0.01, 3σ_R)"),
    ("one stiffness construction only", MAP, "means CFG740's stiffness construction only"),
    ("$N=30{,}000$ pairs, $\\sigma_{\\rm sys}=0.020$, canonical footing", D05, "canonical footing, registered error (N = 30,000, σ_sys 0.020, σ = 0.0276)"),
    ("0.917 to 1.079 & survives, not confirmed & excluded", D05, "| 0.917 – 1.079 | survives (not confirmed) | EXCLUDED |"),
    ("1.079 to 1.083 & survives & survives & UNDECIDED", D05, "| 1.079 – 1.083 | survives | survives | UNDECIDED"),
    ("1.083 to 1.23 & excluded & survives", D05, "| 1.083 – 1.23 | EXCLUDED | survives |"),
    ("at or below 0.917", D05, "| ≤ 0.917 |"),
    ("about 8,000 pairs (7,025 to 8,618), not 30,000", D05C, "DR4 N under the frozen cuts is about 8,000 (7,025–8,618), not 30,000"),
    ("about 0.80 if $\\sigma_{\\rm sys}$ is 0.020, and at 0.12 to 0.40 if it is the 0.0375 measured on DR3", MAP,
     "a Newtonian sky reads decisive against the bare law with probability about 0.80 at sigma_sys 0.020 and 0.12-0.40 at DR3's 0.0375"),
    ("a Newtonian sky reads UNDECIDED", D05, "a Newtonian sky (~1.00) reads UNDECIDED"),
    # Section 3
    ("worded ``v3s survives'', never ``confirmed''", D05, "worded \"v3s survives\", never \"confirmed\""),
    ("form B) takes the same reading as its headline score", D15, "Form B's headline score on Gaia DR4 wide binaries is the 11-05 reading."),
    ("an excluded reading counts against form B in the same words", D15, "An excluded reading counts against form B on this row in the same words as for v3s."),
    ("Each footing has its own verdict line", D15B, "Each footing has its own verdict line."),
    ("The $R$ label quoted is the one the $R$ lane's own frozen criteria give", D15B, "The R label quoted is CFG816's own"),
    ("with no verdict weight, by the ruling of 2026-10-22", D15, "computed and reported beside the verdict, with no verdict weight"),
    ("On DR3 they failed on both footings", MAP, "On DR3 the stability gate FAILED on both footings (largest ladder shift 0.075 > sigma_fit 0.055)"),
    # Section 4 (the digests are checked separately)
    ("with 22 amendments", PREP + "AMENDMENT22_HASH.txt", "AMENDMENT 22"),
    ("last changed on 2026-09-22", PREP + "NOTE_2026-11-15_PIPELINE_HASH.md", "It last changed in commit 2a18b570e8 on 2026-09-22."),
    # Section 5
    ("REPRODUCED ON DR3, rung IMPLEMENTED", DP + "DP1_nss_off_rung/README.md", "REPRODUCED ON DR3, rung IMPLEMENTED"),
    ("information only, no verdict weight", DP + "DP2_n_forecast_triples/README.md", "information only, no verdict weight"),
    ("EQUIVALENT ON DR3, BYTE FOR BYTE", DP + "DP4_parallel_q1/README.md", "EQUIVALENT ON DR3, BYTE FOR BYTE"),
    ("BUILT, 6/6 OFFLINE CHECKS PASS", DP + "DP5_dr4_fetchers/README.md", "BUILT, 6/6 OFFLINE CHECKS PASS"),
    ("BUILT, 8/8 CHECKS PASS, BOTH MUTATES BITE", DP + "DP6_cut12_wiring/README.md", "BUILT, 8/8 CHECKS PASS, BOTH MUTATES BITE"),
    ("the seed-mean entry of the systematic error: CHECK PASSED", DP + "DP7_seed_mean_check/RESULT.md", "CHECK PASSED"),
    ("the seed-mean entry, the cone fallback, the three rungs", DP8, "| Q1 seed-mean entry wired | WIRED |"),
    ("the seed-mean entry, the cone fallback, the three rungs", DP8, "| Q2 cone fallback, with counts | WIRED |"),
    ("the seed-mean entry, the cone fallback, the three rungs", DP8, "| Q5 the (b) rungs | WIRED |"),
    ("the separation-resolved statistic are each WIRED", DP8, "| Q8 Amendment 14(c) statistic | WIRED |"),
    ("the wrapper pins both decisions of that day", DP8, "| Pins | WIRED | 11-15 (3641f7de...) and 11-15b (dad0d100...) in HASHES (28 -> 30)"),
    ("it never computes the error with the single-seed entry", DP8,
     "at G11S or O12 and never computes (b) with the single-seed entry; a dated owner decision is needed before the data"),
    ("cannot be tested before the release", DP8, "cannot be tested before release"),
    ("reproduces the earlier lane bit for bit", DP8, "42 of 42 values bit-identical to DP7's committed"),
    ("a dated note corrects it", DP + "DP7_seed_mean_check/RESULT.md", "take the mean over k = 1..50 and SE = SD / sqrt(50)"),
    ("MARGIN HOLDS, UNCHANGED on both footings", CQB1, "LABEL [canonical]: MARGIN HOLDS, UNCHANGED"),
    ("MARGIN HOLDS, UNCHANGED on both footings", CQB1, "LABEL [alt]: MARGIN HOLDS, UNCHANGED"),
    ("$4.90\\times10^4$", CQB1, "min Sigma/b 4.90e4; 2.34e4 after the factor"),
    ("$2.34\\times10^4$", CQB1, "min Sigma/b 4.90e4; 2.34e4 after the factor"),
    # Section 6
    ("32 registered or sealed DR4 entries", MAP, "Items found: 32 registered or sealed DR4 entries"),
    ("its floor is the law-first anchor", MAP, "Its floor is the law-first anchor of the D2 rows"),
    ("their own scorer is not run", D15B, "`dr4_scorer.py` is not run"),
    ("No Milky Way row", D15B, "No Milky Way row is scored for form B or v3s."),
    # Section 7
    ("survival for the adopted theory, never confirmation", MAP, "A Newtonian sky is survival for the adopted theory, never confirmation."),
    ("states no fallback", D15B, "For Q1 and Q2 none was put to the owner"),
    ("the reading under which a kill is harder", D15B, "this is the reading under which a kill is harder"),
    ("one absolute path of the author's machine", "closure_2026_11_15/DR4REC1_gaia_dr4_predata_record/DR4REC1_build_supplement.py",
     "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py"),
]

DIGESTS = [
    ("20677265fdace8e1", PREP + "PREREGISTRATION_DR4.md"),
    ("d09a920f8e03fb12", "campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md"),
    ("e25be2cf54bdd933", PREP + "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md"),
    ("1d65509dbf277fe5", SEAL),
    ("5768a66c1a0a2c2c", D05),
    ("448bf4ef63e253f8", PREP + "OWNER_DECISION_2026-11-05b_DR4_D7_D8.md"),
    ("8dfcc1d89bcfc38a", D05C),
    ("3641f7de41510512", D15),
    ("dad0d10040c5424b", D15B),
    ("7c884e0e0a4cb9cb", PREP + "wide_binary_pipeline.py"),
]

# Lean certificates named in the note: (what the note says, folder, lane, theorem count).
LEAN = [
    ("(DP3, 18 theorems)", DP + "DP3_release_day", "DP3", 18),
    ("(DP7, 10 theorems)", DP + "DP7_seed_mean_check", "DP7", 10),
    ("(CQB1, 19 theorems)", "closure_2026_11_15/CQB1_cq2_under_blend", "CQB1", 19),
]

PDF_MARKERS = ["DR4REC1", "Newtonian", "UNDECIDED", "20677265fdace8e1", "dad0d10040c5424b", "MARGIN", "Lean", "WIRED"]


def norm(text):
    return re.sub(r"\s+", " ", text.replace("*", "")).strip()


def mutated(s):
    i = len(s) // 2
    return s[:i] + ("#" if s[i] != "#" else "%") + s[i + 1:]


def main():
    final = "--final" in sys.argv
    mutate = "--mutate" in sys.argv
    tex_raw = TEX.read_text(encoding="utf-8")
    tex = norm(tex_raw)
    cache = {}
    res = []

    for said, rel, lit in ENTRIES:
        if rel not in cache:
            cache[rel] = norm((ROOT / rel).read_text(encoding="utf-8"))
        want = norm(mutated(lit) if mutate else lit)
        ok = (norm(said) in tex) and (want in cache[rel])
        res.append((ok, f"{rel}: {lit[:70]}"))

    for dig, rel in DIGESTS:
        real = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        d = mutated(dig) if mutate else dig
        res.append(((dig in tex_raw) and real.startswith(d), f"digest {dig} is the sha256 of {rel}"))

    for said, folder, lane, n in LEAN:
        d = ROOT / folder
        cert = (d / f"{lane}.lean").read_text(encoding="utf-8")
        twin = (d / f"{lane}_MUTATE.lean").read_text(encoding="utf-8")
        count = len(re.findall(r"^\s*(?:theorem|lemma)\s", cert, flags=re.M))
        count_twin = len(re.findall(r"^\s*(?:theorem|lemma)\s", twin, flags=re.M))
        comp = (d / "compile.txt").read_text(encoding="utf-8")
        comp_m = (d / "compile_MUTATE.txt").read_text(encoding="utf-8")
        want = n + 1 if mutate else n
        clean = comp.strip().endswith("exit 0") and "error" not in comp.lower() and "sorry" not in comp.lower()
        ok = (said in tex_raw) and count == want and count_twin == want and clean and comp_m.strip().endswith("exit 1")
        res.append((ok, f"{lane}: {n} theorems in the certificate and in its twin; certificate compiles clean (exit 0); twin fails (exit 1)"))

    if mutate:
        failed = sum(1 for ok, _ in res if not ok)
        for ok, label in res:
            print(("bites " if not ok else "MISSED") + "  " + label)
        print(f"mutation twin: {failed} of {len(res)} checks fail under the mutation")
        return 0 if failed == len(res) else 1

    pend = re.findall(r"\\pend\{([^}]*)\}", tex_raw.split("\\begin{document}", 1)[-1])
    res.append((not pend or not final, f"pending markers left: {pend if pend else 'none'}" + ("" if final else " (reported only)")))

    home = str(Path.home())
    res.append((home not in tex_raw and "/Users/" not in tex_raw, "no home-directory path in the note"))

    if PDF.exists():
        fresh = PDF.stat().st_mtime >= TEX.stat().st_mtime
        res.append((fresh, "the PDF is not older than the TeX"))
        txt = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True).stdout
        for m in PDF_MARKERS:
            res.append((m in txt, f"the PDF holds the marker {m}"))
    else:
        res.append((not final, "the PDF exists" + ("" if final else " (not built yet; reported only)")))

    passed = sum(1 for ok, _ in res if ok)
    for ok, label in res:
        print(("ok    " if ok else "FAIL  ") + label)
    print(f"audit: {passed} of {len(res)}")
    return 0 if passed == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
