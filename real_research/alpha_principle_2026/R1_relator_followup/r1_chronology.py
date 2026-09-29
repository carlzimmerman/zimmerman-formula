#!/usr/bin/env python3
"""r1_chronology.py -- lane R1, part 2: version chronology of the published 1/alpha of the 'Relator / Emergent C-Space' record (Zenodo concept 16944532) against the references
of the day. Reads the Zenodo API (created dates, files, licence) and the version PDFs (CC-BY-4.0; downloaded into $R1_CACHE/pdf, converted with pdftotext), extracts every printed
value of 1/alpha by regex, and computes the offsets in units of each reference's stated uncertainty.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 r1_chronology.py
              -> exit 0 iff the flag vector equals the pre-registered one:
                 {H1_no_version_predates_a_reference: True, movement_not_explained_by_reference_release: True, printed_values_match_transcription: True}
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 r1_chronology.py --mutate
              -> the version history is replaced by a synthetic one in which the value moves with the reference across the CODATA-2018 -> CODATA-2022 change; the 'tracks the reference'
                 detector must fire, which contradicts the recorded vector: exit 1.

Reference values (alpha^-1, stated standard uncertainty in the last digits):
  CODATA 2018  137.035999084(21)   verified in the NIST 2018 constants list (all_2018.pdf) during this lane
  CODATA 2022  137.035999177(21)   verified on the NIST web page (Value?alphinv) during this lane
  g-2 (PRL 130, 071801)  137.035999166(15)   verified in the abstract of arXiv:2209.13084 (v1 27 Sep 2022)
  Rb recoil 2020  137.035999206(11), Cs recoil 2018  137.035999046(27)   RECALLED (cross-checked against the author's Table V entries)
Release dates: g-2 arXiv v1 2022-09-27 (verified); CODATA 2018 2019-05 and CODATA 2022 2024-05 (RECALLED; only the fact that both precede 2025-08 is used); Rb 2020 (Nature 588, 61; Dec 2020, recalled).
"""
import sys, os, re, json, subprocess, urllib.request, math, datetime
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = "--mutate" in sys.argv
CACHE = os.environ.get("R1_CACHE", "./r1_cache")
os.makedirs(os.path.join(CACHE, "pdf"), exist_ok=True)
import mpmath as mp
mp.mp.dps = 30
def P(*a):
    print(" ".join(str(x) for x in a), flush=True)

REFS = [("CODATA 2018", "137.035999084", "0.000000021", "2019-05-20 (recalled)"),
        ("CODATA 2022", "137.035999177", "0.000000021", "2024-05 (recalled)"),
        ("g-2 PRL 2023", "137.035999166", "0.000000015", "2022-09-27 arXiv v1 (verified)"),
        ("Rb recoil 2020", "137.035999206", "0.000000011", "2020-12 (recalled)"),
        ("Cs recoil 2018", "137.035999046", "0.000000027", "2018-06 (recalled)")]
REFD = {n: (mp.mpf(v), mp.mpf(s)) for n, v, s, d in REFS}
T = REFD["CODATA 2022"][0]

def fetch(url, dest):
    if not os.path.exists(dest):
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req, timeout=180) as r:
            open(dest, "wb").write(r.read())
    return dest

VERS = [("16944533", "2025-08-25", None), ("16951008", "2025-08-30", None), ("17021330", "2025-09-01", "sep"), ("17109113", "2025-09-12", "sep"),
        ("17385707", "2025-10-18", "sep"), ("19462288", "2026-04-08", "apr8"), ("19819000", "2026-04-27", "apr27")]
P("== T1: versions of the concept record (Zenodo API) ==")
api = {}
for rid, dt, tag in VERS:
    j = json.load(urllib.request.urlopen(urllib.request.Request("https://zenodo.org/api/records/%s" % rid, headers={"User-Agent": "curl/8"}), timeout=60))
    api[rid] = j
    files = [(f["key"], f["size"]) for f in j.get("files", [])]
    lic = j["metadata"].get("license", {}).get("id") if "metadata" in j else None
    acc = j.get("metadata", {}).get("access_right")
    P("  %s  created %s  publication_date %s  licence %s  access %s  files %s" % (rid, j["created"][:19], j["metadata"].get("publication_date"), lic, acc, files if files else "NONE PUBLIC (restricted)"))
P("  (files of 16944533 and 16951008 are restricted: the first two versions cannot be read; their abstracts claim 'sub-ppt accuracy')")

# printed values from the PDFs
def pdf_text(rid, raw=False):
    pdf = os.path.join(CACHE, "pdf", "v%s.pdf" % rid)
    fetch("https://zenodo.org/api/records/%s/files/Alpha.pdf/content" % rid, pdf)
    txt = pdf + (".raw.txt" if raw else ".txt")
    if not os.path.exists(txt):
        subprocess.run(["pdftotext"] + ([] if raw else ["-layout"]) + [pdf, txt], check=True, capture_output=True)
    return open(txt, encoding="utf-8", errors="ignore").read()
def strip_ws(t):
    return re.sub(r"\s+", "", t)
def values_in(text):
    """every string of the form 137.0dd... (>= 13 characters) in the whitespace-stripped text, cut where a non-digit follows"""
    out = {}
    for m in re.finditer(r"137\.0\d{10,20}", strip_ws(text)):
        out[m.group(0)] = out.get(m.group(0), 0) + 1
    return out
P("\n== T4: values of alpha^-1 printed in each version's PDF (regex over the whitespace-stripped text; strings 137.0 + 10..20 digits; digit groups printed with spaces in the PDF are joined) ==")
printed = {}
for rid, dt, tag in VERS:
    if tag is None: continue
    printed[rid] = values_in(pdf_text(rid))
    P("  %s (%s): %s" % (rid, dt, ", ".join("%s (x%d)" % (k, v) for k, v in sorted(printed[rid].items()))))
TRANSCRIBED = {"sep": "137.0359991770873", "apr8_headline": "137.03599917315644", "apr8_lock": "137.03599916349474", "apr8_qed": "137.03599917411693925",
               "apr27_headline": "137.035999163494704", "apr27_qed": "137.035999174116901"}
found = lambda rid, key: any(k.startswith(TRANSCRIBED[key][:len(TRANSCRIBED[key]) - 1]) for k in printed[rid]) or TRANSCRIBED[key][:-1] in strip_ws(pdf_text(rid))
match_ok = (found("17021330", "sep") and found("17109113", "sep") and found("17385707", "sep") and found("19462288", "apr8_headline") and found("19462288", "apr8_lock")
            and found("19462288", "apr8_qed") and found("19819000", "apr27_headline") and found("19819000", "apr27_qed"))
P("  every transcribed headline value is found in the PDF of the version where it is attributed: %s" % match_ok)
P("  NOTE: the April-8 PDF prints TWO different values of alpha^-1 (headline 137.03599917315644 and 'current article lock output' 137.03599916349474); the April-27 PDF's headline is the latter.")

# history for the offsets: (label, date, value)
HIST = [("Sep-2025 (17021330/17109113/17385707; printed headline)", "2025-09-01", mp.mpf("137.0359991770873")),
        ("Sep-2025 program default (cfg-1)", "2025-08-30", mp.mpf("137.0359991769773")),
        ("Apr-08-2026 headline (Eq. 5)", "2026-04-08", mp.mpf("137.03599917315644")),
        ("Apr-08-2026 'current article lock' (Table XII)", "2026-04-08", mp.mpf("137.03599916349474")),
        ("Apr-27-2026 headline (Eq. 6)", "2026-04-27", mp.mpf("137.035999163494704")),
        ("Apr-28-2026 separate note 19852220 (Dirac-QED closure; uses A_1^(10) = 5.891 as input)", "2026-04-28", mp.mpf("137.035999174117"))]
if MUTATE:
    HIST = [("synthetic v1 (reference = CODATA 2018)", "2019-06-01", mp.mpf("137.035999084")),
            ("synthetic v2 (reference = CODATA 2022)", "2024-06-01", mp.mpf("137.035999177"))]

P("\n== T2: offsets of each printed value from each reference: (value - ref) in units of the reference's stated uncertainty ==")
hdr = "  %-86s" % "value" + "".join("%16s" % n[:15] for n, _, _, _ in REFS)
P(hdr)
rows = []
for lab, dt, v in HIST:
    zs = [(v - REFD[n][0]) / REFD[n][1] for n, _, _, _ in REFS]
    rows.append((lab, dt, v, zs))
    P("  %-86s" % (lab + " " + mp.nstr(v, 18)) + "".join("%+16.3f" % float(z) for z in zs))
P("  and in units of 1e-10 relative to the CODATA-2022 centre (the bar's tolerance is 5): " + "; ".join("%s %+.2f" % (r[1], float((r[2] - T) / T / mp.mpf("1e-10"))) for r in rows))

P("\n== T3: tests ==")
first_ref_dates = {"CODATA 2018": "2019-05-20", "CODATA 2022": "2024-05-01", "g-2 PRL 2023": "2022-09-27", "Rb recoil 2020": "2020-12-01", "Cs recoil 2018": "2018-06-01"}
earliest = min(dt for _, dt, _ in VERS)
predates = [n for n, d in first_ref_dates.items() if earliest < d]
P("  (a) earliest public version %s ; references released after it: %s" % (earliest, predates if predates else "none"))
H1 = len(predates) == 0 if not MUTATE else all(r[1] > "2024-05-01" for r in rows)
P("      H1: no version of the value pre-dates any reference it agrees with (chronology cannot show a prediction): %s" % H1)
def tracks_reference(hist, refs_over_time):
    """detector: between two consecutive versions v1 -> v2, was there a change of the reference (ref2 - ref1, in units of its uncertainty) and did the value move by the same amount within 0.25 sigma?"""
    fired = []
    for (l1, d1, v1), (l2, d2, v2) in zip(hist[:-1], hist[1:]):
        r1 = refs_over_time(d1); r2 = refs_over_time(d2)
        dref = r2 - r1
        if abs(dref) > mp.mpf("1e-9") and abs((v2 - v1) - dref) <= mp.mpf("0.25") * mp.mpf("0.000000021"):
            fired.append((d1, d2, float(dref), float(v2 - v1)))
    return fired
def ref_of_the_day(d):      # the CODATA central value current on date d (2022 set from 2024-05-01, 2018 set from 2019-05-20)
    if d >= "2024-05-01": return mp.mpf("137.035999177")
    if d >= "2019-05-20": return mp.mpf("137.035999084")
    return mp.mpf("137.035999139")
main_hist = [(l, d, v) for l, d, v in HIST]
main_hist.sort(key=lambda t: t[1])
fired = tracks_reference(main_hist, ref_of_the_day)
P("  (b) reference releases between consecutive versions: CODATA changed between 2019-05-20 and 2024-05-01 only; every dated version is after 2024-05-01 (reference constant over the whole record)")
mv = [(main_hist[i][1], main_hist[i + 1][1], float((main_hist[i + 1][2] - main_hist[i][2]) / mp.mpf("0.000000021"))) for i in range(len(main_hist) - 1) if main_hist[i][1] != main_hist[i + 1][1]]
for a, b, z in mv:
    P("      movement %s -> %s : %+.3f sigma_CODATA (%s)" % (a, b, z, "reference unchanged" if a >= "2024-05-01" else "reference changed"))
P("      'tracks the reference' detector fired on: %s" % (fired if fired else "no consecutive pair"))
moved_unexplained = (len(fired) == 0)
P("      movement_not_explained_by_reference_release: %s" % moved_unexplained)
sep = rows[0] if not MUTATE else rows[0]
P("  (c) closeness to the CODATA-2022 centre (if the printed value were a correct theory's value, |z| would be a draw from N(0,1) in units of the CODATA uncertainty):")
for lab, dt, v, zs in rows:
    z = abs(zs[1])
    Pz = math.erf(float(z) / math.sqrt(2))
    P("      %-86s |z| = %.4f sigma  ->  P(|draw| <= |z|) = %.3e  (likelihood ratio 'centred by construction' : 'correct theory' = %.3g)" % (lab[:86], float(z), Pz, 1 / Pz if Pz > 0 else float('inf')))
P("      (the printed headline of Sep-2025 sits 0.004 sigma from the centre, the April headlines 0.18 and 0.64 sigma; relative to the g-2 value 137.035999166(15) the Sep value is %+.2f sigma and the Apr-27 value %+.2f sigma)" %
  (float((mp.mpf("137.0359991770873") - mp.mpf("137.035999166")) / mp.mpf("0.000000015")), float((mp.mpf("137.035999163494704") - mp.mpf("137.035999166")) / mp.mpf("0.000000015"))))

P("\n== T5: statements of the Sep-2025 paper that can be checked against r3's numbers (short quotes) ==")
txt = re.sub(r"[\x00-\x08\x0b-\x1f]", "", re.sub(r"\s+", " ", pdf_text("17109113", raw=True)))   # \x15 stands for a lost hyphen in the PDF text
for key in ("reported value equals the closedform evaluation", "crosschecked against the analytic closed form", "curvature ladder on/o", "surgical edits"):
    i = txt.find(key)
    P("  [%s] %s" % (key, txt[max(0, i - 100):i + 150] if i >= 0 else "not found"))
r3 = os.path.join(HERE, "r3_results.json")
if os.path.exists(r3) and not MUTATE:
    d = json.load(open(r3))
    P("  r3 (independent re-implementation): Delta Lambda_out literal = %.13f (the value the paper prints) ; printed closed form (44) = %.13f ; they differ by %.1f%% ; physical exterior energy = %.13f" %
      (d["out_literal"], d["out_closed"], 100 * abs(d["out_literal"] - d["out_closed"]) / abs(d["out_closed"]), d["out_true"]))
    P("  r3: dropping the chi ladder moves alpha^-1 by 2.03e-8 relative and the self ladder by 6.8e-10 relative (author-lineage set), against the paper's 'negligible drift'")

flags = dict(H1_no_version_predates_a_reference=bool(H1), movement_not_explained_by_reference_release=bool(moved_unexplained), printed_values_match_transcription=bool(match_ok))
expected = dict(H1_no_version_predates_a_reference=True, movement_not_explained_by_reference_release=True, printed_values_match_transcription=True)
P("\nflags   :", flags)
P("expected:", expected)
ok = flags == expected
P("VERDICT of script: %s" % ("recorded flag vector reproduced (exit 0)" if ok else "flag vector differs from the recorded one (exit 1)"))
json.dump(dict(rows=[(r[0], r[1], str(r[2]), [float(z) for z in r[3]]) for r in rows], printed={k: v for k, v in printed.items()}), open(os.path.join(HERE, "r1_results%s.json" % ("_MUTATE" if MUTATE else "")), "w"), indent=1)
sys.exit(0 if ok else 1)
