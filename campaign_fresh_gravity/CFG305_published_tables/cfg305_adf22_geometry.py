#!/usr/bin/env python3
"""CFG305 step 4: the ADF22.5 geometry with the journal's 870 um masked-fit values (FROZEN_CRITERIA.md, 82dfcc1b3).

Two scratch mirrors (git archive of HEAD + read-through links, built with cfg305_rerun.build_mirror):
  CTRL       no substitution: CFG285's post-hoc must reproduce its committed .out and _results.json exactly.
  PUBLISHED  the CONFIRMED Umehata+25 (ApJ 997:79) Table 3 masked A7 values (n, R_e, b/a, PA and their errors, as printed) replace
             umehata25_870um_masked_* in the mirror copy of adf22_pdf_direct_reads_A7.csv and alma870_* in the mirror copy of
             adf22_5_literature_values.csv; the other confirmed Umehata cell (the unmasked n error bar) is substituted the same way.
             CFG285's post-hoc script runs with one disclosed label patch (the two printed labels that quote arXiv numbers).
Order in each mirror: the post-hoc first (it reads CFG285's committed stage-B results for its control), then the labelled extra:
STAGE=B cfg284_adf22_5_stars.py, then STAGE=B cfg285_adf22_5_gas.py (it reads CFG284's stage-B results).
Usage:  python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_adf22_geometry.py <scratch_dir>
Writes here: cfg285_posthoc_expfit_geometry_PUBLISHED.out / _PUBLISHED_results.json, cfg305_adf22_geometry.out / _results.json,
cfg284_stageB_PUBLISHED.diff, cfg285_stageB_PUBLISHED.diff.  Exit 1 if a CTRL reproduction fails.
"""
import csv, difflib, io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import cfg305_rerun as RR

scratch = os.path.abspath(sys.argv[1])
LD = "data_assembly/adf22_5_literature_2026-10-02"
D285 = "campaign_fresh_gravity/CFG285_adf22_5_measured_gas"
D284 = "campaign_fresh_gravity/CFG284_adf22_5_with_stars"
PH = "cfg285_posthoc_expfit_geometry"
CF = json.load(open(os.path.join(HERE, "cfg305_confirm_results.json")))
lines, checks = [], []
P = lambda s="": (print(s, flush=True), lines.append(s))


def check(name, ok, detail=""):
    checks.append(dict(check=name, ok=bool(ok), detail=detail))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def fmt(x):
    return f"{x:g}"


def edit_csv(path, edits):
    """replace (value, err_hi, err_lo) in the rows named by edits {quantity: (value, err)}; other lines byte-identical"""
    if os.path.islink(path):
        tgt = os.path.realpath(path); os.unlink(path); open(path, "wb").write(open(tgt, "rb").read())
    raw = open(path, newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    L = raw.split(nl)
    hdr = next(csv.reader(io.StringIO(L[0])))
    iv, ih, il = hdr.index("value"), hdr.index("err_hi"), hdr.index("err_lo")
    done = []
    for k in range(1, len(L)):
        if not L[k]:
            continue
        cells = next(csv.reader(io.StringIO(L[k])))
        if cells[0] in edits:
            v, e = edits[cells[0]]
            old = (cells[iv], cells[ih], cells[il])
            cells[iv], cells[ih], cells[il] = v, e, e
            b = io.StringIO(); csv.writer(b, lineterminator="").writerow(cells); L[k] = b.getvalue()
            done.append((cells[0], old, (v, e, e)))
    open(path, "w", newline="").write(nl.join(L))
    return done


def materialise(zf, rel_dir):
    d = os.path.join(zf, rel_dir)
    for f in os.listdir(d):
        p = os.path.join(d, f)
        if os.path.islink(p):
            t = os.path.realpath(p); os.unlink(p); open(p, "wb").write(open(t, "rb").read())


def run(zf, rel, env_extra=None):
    env = dict(os.environ, MPLBACKEND="Agg")
    for k in ("MUTATE", "SELFTEST", "STAGE"):
        env.pop(k, None)
    env.update(env_extra or {})
    p = subprocess.run([sys.executable, os.path.join(zf, rel)], cwd=zf, env=env, capture_output=True, text=True, timeout=3000)
    return p.returncode, p.stdout, p.stderr


def head(rel):
    p = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{rel}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


masked = {c["field"]: c for c in CF["umehata"]["masked"]}
extra = {c["direct_quantity"]: c for c in CF["umehata"]["other_differences"]}
conf = {d["field"] for d in CF["decisions"] if d["table"].startswith("Umehata") and d["decision"] == "CONFIRMED"}
E_DIR, E_LIT = {}, {}
for f, ql in (("n", "alma870_sersic_n"), ("Re", "alma870_Re"), ("ba", "alma870_axis_ratio"), ("PA", "alma870_PA")):
    if f in conf:
        c = masked[f]
        E_DIR[c["direct_quantity"]] = (fmt(c["value"]), fmt(c["err"]))
        E_LIT[ql] = (fmt(c["value"]), fmt(c["err"]))
for q, c in extra.items():
    E_DIR[q] = (fmt(c["value"]), fmt(c["err"]))
P(f"CFG305 ADF22.5 geometry: substitutions (PUBLISHED mirror only) adf22_pdf_direct_reads_A7.csv {E_DIR}; adf22_5_literature_values.csv {E_LIT}")
LABELS = [('("870 um masked, b/a 0.58", ', f'("870 um masked, b/a {E_DIR["umehata25_870um_masked_ba"][0]}", '),
          ("gas proxy {RE_G_EXP} kpc (870 um masked, n = 1.01)", f"gas proxy {{RE_G_EXP}} kpc (870 um masked, n = {E_DIR['umehata25_870um_masked_n'][0]})")]
RES = {}
for mode in ("CTRL", "PUBLISHED"):
    base = os.path.join(scratch, f"ADF_{mode}")
    os.makedirs(base, exist_ok=True)
    zf, links = RR.build_mirror(base)
    for d in (D285, D284, LD):
        materialise(zf, d)
    if mode == "PUBLISHED":
        dd = edit_csv(os.path.join(zf, LD, "adf22_pdf_direct_reads_A7.csv"), E_DIR)
        dl = edit_csv(os.path.join(zf, LD, "adf22_5_literature_values.csv"), E_LIT)
        P(f"  PUBLISHED mirror: edited rows {[(q, o, n) for q, o, n in dd + dl]}")
        sp = os.path.join(zf, D285, PH + ".py")
        s = open(sp).read()
        for old, new in LABELS:
            assert s.count(old) == 1, f"label patch: {old!r} found {s.count(old)} times"
            s = s.replace(old, new)
        open(sp, "w").write(s)
        P(f"  label patch in the mirror copy of {PH}.py: {[n for _, n in LABELS]}")
    before = RR.stat_targets(links)
    rc, so, se = run(zf, os.path.join(D285, PH + ".py"))
    P(f"\n[{mode}] {PH}.py rc {rc}" + (f"; stderr tail: {se.strip().splitlines()[-1]}" if rc and se.strip() else ""))
    out = open(os.path.join(zf, D285, PH + ".out")).read()
    js = json.load(open(os.path.join(zf, D285, PH + "_results.json")))
    RES[mode] = dict(rc=rc, out=out, json=js)
    stage = {}
    for d, scr, tag in ((D284, "cfg284_adf22_5_stars.py", "cfg284"), (D285, "cfg285_adf22_5_gas.py", "cfg285")):
        rc2, so2, se2 = run(zf, os.path.join(d, scr), {"STAGE": "B"})
        stage[tag] = dict(rc=rc2, out=open(os.path.join(zf, d, f"{tag}_stageB.out")).read(),
                          json=open(os.path.join(zf, d, f"{tag}_stageB_results.json"), "rb").read(),
                          csv=open(os.path.join(zf, d, f"{tag}_points_stageB.csv"), "rb").read())
        P(f"[{mode}] STAGE=B {scr} rc {rc2}")
    RES[mode]["stage"] = stage
    after = RR.stat_targets(links)
    wrote = [p for p in links if before.get(p) != after.get(p)]
    other = [p for p in wrote if "/CFG294_" in p]          # a parallel session edits CFG294's lane during these runs (disclosed)
    check(f"{mode}: no run wrote through a read-through link into the repo (targets changed by the parallel CFG294 session listed, not counted)",
          not [p for p in wrote if p not in other], f"{len(links)} links checked; changed: {[os.path.relpath(p, REPO) for p in wrote]}")

# ---- CTRL reproduction
c_out_ok = RES["CTRL"]["out"].encode() == head(f"{D285}/{PH}.out")
c_js_ok = json.loads(head(f"{D285}/{PH}_results.json")) == RES["CTRL"]["json"]
check("CTRL: the post-hoc reproduces its committed .out and _results.json exactly", c_out_ok and c_js_ok, f".out identical {c_out_ok}; JSON equal {c_js_ok}")
for tag, d in (("cfg284", D284), ("cfg285", D285)):
    st = RES["CTRL"]["stage"][tag]
    # run-time fields such as "(4 s)" are dropped before comparing (CFG289's rule); everything else must be identical
    rt = lambda t: [re.sub(r"\(\d+(\.\d+)? ?s\)\s*$", "(<t> s)", l) for l in t.splitlines()]
    ok_o = rt(st["out"]) == rt(head(f"{d}/{tag}_stageB.out").decode())
    ok_j = st["json"] == head(f"{d}/{tag}_stageB_results.json")
    ok_c = st["csv"] == head(f"{d}/{tag}_points_stageB.csv")
    check(f"CTRL: STAGE=B {tag} reproduces its committed stage-B .out / _results.json / points CSV", ok_o and ok_j and ok_c,
          f".out {ok_o}; JSON {ok_j}; CSV {ok_c}")

# ---- the PUBLISHED variant outputs
banner = ("VARIANT _PUBLISHED (CFG305, FROZEN_CRITERIA.md 82dfcc1b3): the 870 um masked-fit values are the journal's (Umehata+25, ApJ 997:79, "
          f"Table 3, row ADF22.A7: n {E_DIR['umehata25_870um_masked_n'][0]} +- {E_DIR['umehata25_870um_masked_n'][1]}, R_e {E_DIR['umehata25_870um_masked_Re'][0]} +- "
          f"{E_DIR['umehata25_870um_masked_Re'][1]} kpc, b/a {E_DIR['umehata25_870um_masked_ba'][0]} +- {E_DIR['umehata25_870um_masked_ba'][1]}, PA "
          f"{E_DIR['umehata25_870um_masked_PA'][0]}), substituted in a scratch mirror; arXiv v1 had n 1.01, R_e 1.53, b/a 0.58, PA 17.4.\n"
          "The docstring text printed below (its 'Why' paragraph and hand estimates) is CFG285's and still quotes the arXiv values; the numbers in the tables use the journal's.\n\n")
open(os.path.join(HERE, PH + "_PUBLISHED.out"), "w").write(banner + RES["PUBLISHED"]["out"])
json.dump(RES["PUBLISHED"]["json"], open(os.path.join(HERE, PH + "_PUBLISHED_results.json"), "w"), indent=1)
for tag in ("cfg284", "cfg285"):
    a = RES["CTRL"]["stage"][tag]["out"].splitlines()
    b = RES["PUBLISHED"]["stage"][tag]["out"].splitlines()
    d = list(difflib.unified_diff(a, b, fromfile=f"CTRL/{tag}_stageB.out", tofile=f"PUBLISHED/{tag}_stageB.out", lineterm="", n=0))
    open(os.path.join(HERE, f"{tag}_stageB_PUBLISHED.diff"), "w").write("\n".join(d) + "\n")
    P(f"\n{tag} STAGE=B, PUBLISHED vs CTRL: {sum(1 for l in d if l[:1] in '+-' and not l.startswith(('+++', '---')))} differing .out lines")
    for l in d:
        if l[:1] in "+-" and not l.startswith(("+++", "---")):
            P("   " + l[:260])

# ---- the row-by-row report
rc_, rp_ = RES["CTRL"]["json"]["rows"], RES["PUBLISHED"]["json"]["rows"]
P("\nCFG285 POST-HOC (exponential-matched geometry), CTRL -> PUBLISHED")
rows = {}
for k in ("S0", "S1", "S2", "G1", "G2", "G3"):
    a, b = rc_[k], rp_[k]
    sa = f"{a['nominal']['s']:.3g}" if a["nominal"]["status"] == "root" else "-"
    sb = f"{b['nominal']['s']:.3g}" if b["nominal"]["status"] == "root" else "-"
    qa = [10 ** x if x is not None else None for x in a["q"]] if a.get("q") else None
    qb = [10 ** x if x is not None else None for x in b["q"]] if b.get("q") else None
    rows[k] = dict(D=(a["nominal"]["D"], b["nominal"]["D"]), status=(a["nominal"]["status"], b["nominal"]["status"]), s=(sa, sb),
                   frac_noroot=(a["frac_noroot"], b["frac_noroot"]), resolution=(a["resolution"], b["resolution"]))
    def iv(q):
        try:
            return f"68% [{q[1]:.3g}, {q[3]:.3g}]"
        except Exception:
            return "-"
    P(f"  {k}: D {a['nominal']['D']:.3f} -> {b['nominal']['D']:.3f}; {a['nominal']['status']} -> {b['nominal']['status']}; s* {sa} -> {sb}; "
      f"no-root {a['frac_noroot']:.3f} -> {b['frac_noroot']:.3f}; {a['resolution']} -> {b['resolution']}; rooted {iv(qa)} -> {iv(qb)}")
P("  conversion equivalents (floor boundary / FLAT / PROXY / H(z)):")
for fam in ("eq_stars + gas", "eq_gas only"):
    a, b = rc_[fam], rp_[fam]
    f3 = lambda v: "nan" if v is None else f"{v:.3f}"
    P(f"    {fam[3:]:12s}: " + " / ".join(f"{f3(a[x])} -> {f3(b[x])}" for x in ("D1", "FLAT", "PROXY", "H(z)")))
P("  inclination rows (S0 stars only / G1 gas only at 0.8):")
ia, ib = rc_["inclination"], rp_["inclination"]
inc = {}
for (ka, va), (kb, vb) in zip(ia.items(), ib.items()):
    s0a = f"s* <= {va['S0']['s']:.3g}" if va["S0"]["status"] == "root" else va["S0"]["status"]
    s0b = f"s* <= {vb['S0']['s']:.3g}" if vb["S0"]["status"] == "root" else vb["S0"]["status"]
    g1a = f"s* <= {va['G1']['s']:.3g}" if va["G1"]["status"] == "root" else va["G1"]["status"]
    g1b = f"s* <= {vb['G1']['s']:.3g}" if vb["G1"]["status"] == "root" else vb["G1"]["status"]
    inc[ka] = dict(label_published=kb, i=(va["i_deg"], vb["i_deg"]), S0=(s0a, s0b), G1=(g1a, g1b))
    P(f"    {ka:28s} -> {kb:28s} i {va['i_deg']:.1f} -> {vb['i_deg']:.1f} deg: S0 {s0a} -> {s0b} | G1 {g1a} -> {g1b}")
n_ok = sum(c["ok"] for c in checks)
P(f"\n{n_ok}/{len(checks)} checks pass")
json.dump(dict(substitutions=dict(direct_reads=E_DIR, literature=E_LIT), label_patch=[n for _, n in LABELS], posthoc_rows=rows, inclination=inc,
               checks=checks), open(os.path.join(HERE, "cfg305_adf22_geometry_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "cfg305_adf22_geometry.out"), "w").write("\n".join(lines).replace(scratch, "<scratch>") + "\n")
sys.exit(0 if n_ok == len(checks) else 1)
