#!/usr/bin/env python3
"""FN2 Part C (FROZEN_CRITERIA.md, 755f05c3cf): Gaia DR4. C1 the release date from ESA's page (provisional); C2 is there a frozen
decision rule for the bare law; C3 that rule's band edges, mechanically, and where CW1's plain-QUMOND values fall; C4 the amendment
drafts marked NOT FILED. Everything in prep_2026/gaia_dr4_prep/ and cw_lanes_2026_11_04/ is read as text or JSON, never imported,
never written. No DR4 byte exists.
    python3 -B fn2_dr4.py [--fetch] [--mutate]     --fetch re-reads ESA's page; MUTATE flips one prereg byte in memory and reads
                                                   CW1's LOC3 row as PQ: K-C3 and K-C1 must fail (exit 1)
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import datetime, hashlib, html, json, math, os, re, subprocess, sys, urllib.request
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PREP = os.path.join(ROOT, "prep_2026", "gaia_dr4_prep"); CW1 = os.path.join(ROOT, "cw_lanes_2026_11_04", "CW1_wide_binary_seal_dr4")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []; K = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def chk(n, ok, x=""): K.append((n, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {n}: {x}")
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()

# ---------------- C1: release date (web page text is data) ----------------
URL = "https://www.cosmos.esa.int/web/gaia/release"; C1F = os.path.join(HERE, "c1_esa_gaia_release_extract.json")
if "--fetch" in sys.argv or not os.path.exists(C1F):
    raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "research-metadata/1.0"}), timeout=60).read()
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw.decode("utf8", "replace")); t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    m = re.search(r"Gaia DR4 \(based on \d+ months of data\)\s*(\d{1,2} \w+ 20\d\d)", t)
    json.dump(dict(url=URL, utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), page_sha256=sha(raw), page_bytes=len(raw),
                   extract=(m.group(0) if m else None), date=(m.group(1) if m else None)), open(C1F, "w"), indent=1)
C1 = json.load(open(C1F))
lab1 = "NOT STATED" if not C1["date"] else ("DATE CONFIRMED" if C1["date"] == "2 December 2026" else f"DATE DIFFERS ({C1['date']})")
P(f"C1 ESA page {C1['url']} read {C1['utc']} (page sha256 {C1['page_sha256'][:16]}): '{C1['extract']}' -> {lab1}; PROVISIONAL (a web page; ESA can move it)")

# ---------------- known answers on the frozen inputs ----------------
pre = bytearray(rd(os.path.join(PREP, "PREREGISTRATION_DR4.md")))
if MUT: pre[1000] ^= 0x01
h22 = re.search(r"after Amendment 22: ([0-9a-f]{64})", open(os.path.join(PREP, "AMENDMENT22_HASH.txt")).read()).group(1)
chk("K-C3 prereg SHA-256 equals Amendment 22's after-hash", sha(bytes(pre)) == h22, f"{sha(bytes(pre))[:16]} vs {h22[:16]}")
PIPE = os.path.join(PREP, "wide_binary_pipeline.py"); ps = sha(rd(PIPE)); cw1_pipe = re.search(r"`wide_binary_pipeline\.py`, SHA-256 `([0-9a-f]{64})`", open(os.path.join(CW1, "SEALED_PREDICTION.md")).read()).group(1)
chk("K-C4 wide_binary_pipeline.py SHA-256 equals the hash CW1 recorded", ps == cw1_pipe, f"{ps[:16]} vs {cw1_pipe[:16]}")
seal = rd(os.path.join(CW1, "SEALED_PREDICTION.md")); sline = open(os.path.join(CW1, "SEALED_PREDICTION.sha256")).read().split()[0]
chk("K-C2 CW1 seal SHA-256 equals its .sha256 file", sha(seal) == sline, f"{sha(seal)[:16]} vs {sline[:16]}")
cw = json.load(open(os.path.join(CW1, "cw1.json"))); form = "LOC3" if MUT else "PQ"
PQ = {f: (cw["pipeline"]["out"][f][form]["gamma_inf"], cw["pipeline"]["out"][f][form]["spread"]) for f in ("canonical", "alt")}
chk("K-C1 CW1 PQ gamma_inf (cw1.json) = 1.149 +- 0.027 canonical, 1.208 +- 0.007 alt (printed 3 decimals)",
    f"{PQ['canonical'][0]:.3f}" == "1.149" and f"{PQ['canonical'][1]:.3f}" == "0.027" and f"{PQ['alt'][0]:.3f}" == "1.208" and f"{PQ['alt'][1]:.3f}" == "0.007",
    f"canonical {PQ['canonical'][0]:.4f} +- {PQ['canonical'][1]:.4f}, alt {PQ['alt'][0]:.4f} +- {PQ['alt'][1]:.4f}" + (" (MUTATE: LOC3 row read)" if MUT else ""))
NOTE = os.path.join(PREP, "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md")
blob = subprocess.run(["git", "show", "3d82af0a7e:prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md"], cwd=ROOT, capture_output=True).stdout
chk("K-C5 D2 note unchanged since 3d82af0a7e", blob == rd(NOTE) and len(blob) > 0, f"sha256 {sha(rd(NOTE))[:16]}")
ptxt = bytes(pre).decode("utf8", "replace"); src = open(PIPE).read()
fl_text = re.search(r"\| canonical \| \*\*([\d.]+) ± [\d.]+\*\*.*?\n> \| alt \| \*\*([\d.]+) ±", ptxt, re.S)
pc = {k: float(re.search(rf"^{k}\s*=\s*([\d.]+)", src, re.M).group(1)) for k in ("GAMMA_TARGET", "GAMMA_TARGET_ALT", "GAMMA_TARGET_TOP", "GAMMA_TARGET_ALT_TOP", "NOVERDICT_EDGE")}
FLOOR = {"canonical": pc["GAMMA_TARGET"], "alt": pc["GAMMA_TARGET_ALT"]}
chk("K-C6 Arm A floors in the prereg text (Amendment 10 table) equal the pipeline's GAMMA_TARGET / GAMMA_TARGET_ALT",
    bool(fl_text) and float(fl_text.group(1)) == FLOOR["canonical"] and float(fl_text.group(2)) == FLOOR["alt"], f"text {fl_text.groups() if fl_text else None}; code {FLOOR}")
note = open(NOTE).read(); m7 = re.search(r"\*\*([\d.]+) \(canonical\)\*\* or \*\*< ([\d.]+) \(alt\)\*\*", note)
chk("K-C7 D2 §3 ceilings (floor - 1)/3 = 0.054 / 0.064", bool(m7) and f"{(FLOOR['canonical'] - 1) / 3:.3f}" == m7.group(1) and f"{(FLOOR['alt'] - 1) / 3:.3f}" == m7.group(2),
    f"{(FLOOR['canonical'] - 1) / 3:.4f} / {(FLOOR['alt'] - 1) / 3:.4f} against the note's {m7.groups() if m7 else None}")

# ---------------- C2: which frozen line names the bare law, and with which kernel ----------------
solver = open(os.path.join(PREP, "aqual_efe_full_solve_2026.py")).read(); body = re.search(r"def nu\(y\):\n((?:    .*\n)+)", solver).group(0)
ns = {}; exec("import numpy as np\n" + body, ns); nuA = lambda y: float(ns["nu"](y))
nu1 = lambda y: 0.5 + math.sqrt(0.25 + 1 / y); nu2 = lambda y: math.sqrt(1 + 1 / y)
ys = (0.1, 1.0, 1.4647, 10.0)
P("\nC2 kernels behind the numbers (nu at y = " + ", ".join(map(str, ys)) + "):")
P("   bare law, n = 1 (PAPER67, CW1 PQ, D2 A1):  " + ", ".join(f"{nu1(y):.4f}" for y in ys))
P("   Arm A, Route A (aqual_efe_full_solve_2026.py nu):  " + ", ".join(f"{nuA(y):.4f}" for y in ys))
P("   prereg 2026-07-16 statement, n = 2 (sqrt(1+1/y)):  " + ", ".join(f"{nu2(y):.4f}" for y in ys))
same = all(abs(nuA(y) - nu1(y)) < 1e-6 for y in ys)
hyp = re.search(r"each\s+hypothesis H in \{([^}]*)\}", ptxt); law_first = re.search(r"\*\*Law-first\*\*: (.*?)\n", note)
rowsD2 = re.findall(r"  - (γ̂ − 1\.000 ≥ 3σ.*?|Arm A floor − γ̂ ≥ 3σ.*?|Otherwise: UNDECIDED\.)\n", note)
LINES = [
 dict(source="PREREGISTRATION_DR4.md §1.5 (2026-07-16)", hypothesis=f"H in {{{hyp.group(1) if hyp else '?'}}}", kernel="n = 2 framework MI/MG of 2026-07 (sqrt(1+1/y)); amended to alpha = 2, then Route A",
      names_bare_law=False, rule="z_H = (gamma_hat - gamma_H)/sigma_tot; consistent |z|<2, disfavored |z|>3", against_outcome=True),
 dict(source="PREREGISTRATION_DR4.md Amendments 10-11 (Arm A)", hypothesis="Arm A: the frozen kernel as modified gravity, no coherence length; band 1.1614-1.1814 / 1.1917-1.2267",
      kernel="Route A, nu = 1/(1 - exp(-sqrt(y)))", names_bare_law=False, rule="table: gamma_hat <= 1.007 Arm A falsified; ... ; > 1.23 no verdict", against_outcome=True),
 dict(source="NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md (D2, owner-approved) + A1-A3", hypothesis="law-first: " + (law_first.group(1) if law_first else "?"),
      kernel="names g_N = g^2/(g + a0) (n = 1); its decision rows use Arm A's registered floor (Route A kernel); A1/A3 quote the n = 1 AQUAL values 1.167/1.199 (primary g_ext), 1.145/1.173 (alternative)",
      names_bare_law=True, rule=" | ".join(rowsD2) + " ; sigma = sqrt(sigma_fit^2 + sigma_sys^2), sigma_sys definition (b) primary; (a), (e), (g2) must agree at >= 3 sigma, else UNDECIDED (A3)", against_outcome=True),
 dict(source="CW1 SEALED_PREDICTION.md (df7801238b)", hypothesis="PQ plain QUMOND (n = 1 nu, Newtonian host field) and filter forms", kernel="n = 1", names_bare_law=True,
      rule="none: separation labels between forms (dQ/0.020, dgamma/0.028) and a qualitative 'What DR4 would decide'; no gamma_hat band or z rule", against_outcome=False),
 dict(source="CFG800 / Amendment 22 R rule", hypothesis="'FRAMEWORK KILLED' = the CFG740 stiffness construction (Amendment 22 c4)", kernel="CFG740", names_bare_law=False,
      rule="KILLED iff R - 1 >= 0.01 and >= 3 sigma_R", against_outcome=True)]
for L in LINES: P(f"   {L['source']}: names the bare law {L['names_bare_law']}; rule against it {L['against_outcome'] and L['names_bare_law']}; kernel: {L['kernel']}")
exists = any(L["names_bare_law"] and L["against_outcome"] for L in LINES)
off = {f: abs(FLOOR[f] - PQ[f][0]) / 0.028 for f in FLOOR}
lab2 = ("NO RULE" if not exists else "RULE EXISTS" if same else "RULE EXISTS, ANCHOR NOT THE BARE LAW'S OWN NUMBER")
P(f"C2 label: {lab2}. Arm A's kernel equals the bare law's nu: {same}. Anchor offset |Arm A floor - CW1 PQ gamma_inf| / 0.028: canonical {off['canonical']:.2f}, alt {off['alt']:.2f} sigma_tot")

# ---------------- C3: the D2 rule's band edges, both footings ----------------
P("\nC3 the D2 law-first rows, mechanically. law-first EXCLUDED iff gamma_hat <= floor - 3 sigma; medium-first EXCLUDED iff gamma_hat >= 1 + 3 sigma and not law-first excluded; else UNDECIDED.")
CASES = {"(a) sigma_fit 0.019, sigma_sys 0.020 (registered, N = 30,000)": {"canonical": (0.019, 0.020), "alt": (0.019, 0.020)},
         "(b) sigma_fit 0.019, sigma_sys DR3 def. (b) 0.0375 / 0.041 (NON-SCORING illustration)": {"canonical": (0.019, 0.0375), "alt": (0.019, 0.041)}}
AQ = {"canonical": 1.167, "alt": 1.199}
def call(g, fl, s): return "law-first EXCLUDED" if fl - g >= 3 * s else ("medium-first EXCLUDED" if g - 1 >= 3 * s else "UNDECIDED")
C3 = {}
for cn, cd in CASES.items():
    for f, (sf, ss) in cd.items():
        s = math.hypot(sf, ss); lo, mf = FLOOR[f] - 3 * s, 1 + 3 * s
        r = dict(sigma=s, law_first_excluded_at_or_below=lo, medium_first_excluded_at_or_above=max(mf, lo), CW1_PQ=PQ[f][0], CW1_PQ_call=call(PQ[f][0], FLOOR[f], s),
                 newton_1p000_call=call(1.0, FLOOR[f], s), info_anchor_A1_AQUAL=AQ[f], info_law_first_excluded_if_anchor_were_A1=AQ[f] - 3 * s)
        C3[f"{cn}|{f}"] = r
        P(f"   {cn} | {f}: sigma {s:.4f}; law-first excluded at gamma_hat <= {lo:.4f}; medium-first excluded at gamma_hat >= {max(mf, lo):.4f}; "
          f"CW1 PQ {PQ[f][0]:.4f} reads '{r['CW1_PQ_call']}'; a Newtonian 1.000 reads '{r['newton_1p000_call']}'; information: with A1's AQUAL anchor {AQ[f]} the law-first edge would be {AQ[f] - 3 * s:.4f}")
P("   (D2 A3: both frozen g_ext values are scored separately; the floor above is Arm A's at the primary g_ext. sigma_fit scales as sqrt(30000/N) per PREREG §1.5.)")

# ---------------- C4: drafts marked NOT FILED ----------------
P("\nC4 drafts marked NOT FILED in prep_2026/gaia_dr4_prep/:")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"^[>\s]*", "", s)).strip()
heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^> ### .*?AMENDMENT (\d+) —", ptxt, re.M)]
spans = {}
for i, (n, st) in enumerate(sorted(heads, key=lambda x: x[1])):
    nxt = [s for _, s in heads if s > st]; h2 = [m.start() for m in re.finditer(r"^## ", ptxt[st:], re.M)]
    spans[n] = ptxt[st:min(nxt + [st + h2[0]] if h2 else nxt + [len(ptxt)])]
MANUAL = {9: "CHANGES ROWS: MG target 1.2139/1.2592 replaces MI 1.1582; no-verdict edge 1.20 -> 1.26; rows 1.145-1.26 relabelled (all later superseded by Amendment 10)",
          12: "CHANGES ROWS: Arm B's coherence length, prediction and kill threshold corrected; declares Arm B not a testable arm; Arm A untouched"}
C4 = []
for fn in sorted(os.listdir(PREP)):
    p = os.path.join(PREP, fn)
    if not (fn.startswith("AMENDMENT") and fn.endswith(".md")): continue
    txt = open(p).read(); first = txt.strip().splitlines()[0] if txt.strip() else ""
    if "NOT_FILED" not in fn and "NOT FILED" not in first.upper(): continue
    n = int(re.match(r"AMENDMENT(\d+)", fn).group(1)); hf = os.path.join(PREP, f"AMENDMENT{n}_HASH.txt")
    filed = n in spans and os.path.exists(hf); fb = spans.get(n, "")
    dl = {norm(l) for l in txt.splitlines() if norm(l)}; fl_ = {norm(l) for l in fb.splitlines() if norm(l)}
    only_draft, only_filed = len(dl - fl_), len(fl_ - dl)
    stmt = re.search(r"CHANGES NO[^.]*DECISION ROW", fb)
    rowc = MANUAL.get(n) or ("NO ROW CHANGE (its own text: '" + stmt.group(0)[:90] + "...')" if stmt else "UNSTATED")
    label = ("FILED, " if filed else "NOT FILED, ") + ("CHANGES ROWS" if rowc.startswith("CHANGES") else "NO ROW CHANGE" if rowc.startswith("NO ROW") else "ROW CHANGE UNSTATED")
    C4.append(dict(file=fn, amendment=n, filed_in_prereg=n in spans, hash_file=os.path.exists(hf), draft_lines_not_in_filed=only_draft, filed_lines_not_in_draft=only_filed, rows=rowc, label=label))
    P(f"   {fn}: Amendment {n} filed in the prereg {n in spans}, hash file {os.path.exists(hf)}; draft lines not in the filed block {only_draft}, filed lines not in the draft {only_filed}; {rowc} -> {label}")
pending = [c for c in C4 if not c["filed_in_prereg"]]
P(f"C4: {len(C4)} drafts; {len(pending)} not filed in the prereg" + (f": {[c['file'] for c in pending]}" if pending else " (every draft file name is stale; the filed block governs)"))

ok = all(o for _, o in K)
P(f"\nknown answers {sum(o for _, o in K)} of {len(K)} PASS" + ("; MUTATE: K-C3 and K-C1 must fail" if MUT else ""))
if MUT:
    bit = not dict(K)["K-C3 prereg SHA-256 equals Amendment 22's after-hash"] and not [o for n, o in K if n.startswith("K-C1")][0]; P(f"MUTATE {'bites' if bit else 'DOES NOT BITE'}")
json.dump(dict(criteria="755f05c3cf", mutate=MUT, C1=dict(C1, label=lab1, status="PROVISIONAL"), known=K, C2=dict(lines=LINES, label=lab2, arm_a_kernel_equals_bare_law=same,
               anchor_offset_sigma_tot=off, floors=FLOOR, pipeline_constants=pc, CW1_PQ=PQ), C3=C3, C4=C4),
          open(os.path.join(HERE, f"fn2_dr4{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"fn2_dr4{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else (0 if ok else 1))
