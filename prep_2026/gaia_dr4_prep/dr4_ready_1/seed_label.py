#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 (draft rev 2, NOT FILED) tooling: the EDGE TABLE extracted BY CODE from the frozen pipeline and the SEED-SENSITIVITY LABEL (NEW file; nothing frozen is edited).
Design and controls: SEED_LABEL_DESIGN_FROZEN.md (a9f0290bb), written before this code.  DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.

Edge table: the decision constants of `wide_binary_pipeline.py` (module attributes GAMMA_*, NOVERDICT_EDGE, KAPPA_WINDOW), EVERY one classified (an unclassified attribute makes the extraction fail), each with its value and the pipeline's own
source line; the STALE / SUPERSEDED ones excluded with the code's own reason (asserted to occur in the source text); sigma_sys = 0.02 is read from the frozen pre-registration text (it is not a named constant in the code).
Label: if the primary gamma-hat lies within max(sigma_build, 0.3 sigma_fit) of any edge (the z-rule edges t -+ 2, 3 sigma_tot around each in-force target t, at the PRIMARY's sigma_tot, and the hard edges), the verdict carries the label
'seed-sensitive' with the number of builds below / above that edge; stability conditions (kappa window; each implemented ladder rung's shift below 1 sigma_fit) whose pass/fail status differs across builds are labelled the same way.
At least 10 further G-only builds (K_G >= 10) are required before the label applies.
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seed_label.py --write-edge-table prep_2026/gaia_dr4_prep/dr4_ready_1/edge_table_dr4.json
      python3 .../seed_label.py --evaluate <g-only sweep manifest> [--full <full-rebuild sweep manifest>] [--table edge_table_dr4.json] [--write-report PATH]"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, importlib.util, json, math, re
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
PIPELINE = PREP / "wide_binary_pipeline.py"
PREREG = PREP / "PREREGISTRATION_DR4.md"
FROZEN_PIPELINE_SHA256 = "7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9"      # RELEASE_DAY_CHECKLIST section 3
FAMILY_RE = re.compile(r"^(GAMMA_|NOVERDICT|KAPPA_)")
MIN_FURTHER_BUILDS = 10
WIDTH_FLOOR = 0.3                                                                               # the label width is max(sigma_build, 0.3 sigma_fit)

# in-force gamma-hat targets (the z-rule's centres) and the footings they apply to
IN_FORCE_TARGETS = {
    "GAMMA_TARGET": ("Arm A band floor (Amdt 10), canonical", ("canonical",)),
    "GAMMA_TARGET_TOP": ("Arm A band top (Amdt 10), canonical", ("canonical",)),
    "GAMMA_TARGET_ALT": ("Arm A band floor (Amdt 10), alt footing", ("alt",)),
    "GAMMA_TARGET_ALT_TOP": ("Arm A band top (Amdt 10), alt footing", ("alt",)),
    "GAMMA_B_PRED": ("Arm B corrected prediction = Newton = Arm C (Amdt 12(c), 13), both footings", ("canonical", "alt")),
    "GAMMA_B_PRED_SUNWARD": ("Arm B, sunward gate only (Amdt 12(c)), both footings", ("canonical", "alt")),
    "GAMMA_MOND": ("conventional-MOND benchmark (not framework), both footings", ("canonical", "alt")),
}
IN_FORCE_HARD = {"GAMMA_A_FALSIFIED_BELOW": "Arm A falsified below (Amdt 11(d))", "GAMMA_B_KILL": "Arm B killed at or above (Amdt 12(d))", "NOVERDICT_EDGE": "no-verdict edge (Amdt 10)"}
STABILITY = {"KAPPA_WINDOW": "frozen kappa window (outside: systematic-limited, no verdict)"}
# excluded constants -> a string that must occur in the pipeline source (the code's own reason)
EXCLUDED = {
    "GAMMA_MG": "STALE per Amdt 4(i)",
    "GAMMA_MI": "SUPERSEDED by Amdt 9",
    "GAMMA_MI_RANGE_RAD": "superseded record only: MI",
    "GAMMA_MI_RANGE_MAG": "superseded record only: MI",
    "GAMMA_B_CEIL": "AMENDMENT 12 (2026-09-09) SUPERSEDES THE TWO CEILINGS ABOVE",
    "GAMMA_B_CEIL_ALT": "AMENDMENT 12 (2026-09-09) SUPERSEDES THE TWO CEILINGS ABOVE",
    "GAMMA_B_PRED_SIG": "Amdt 12(c)",
    "GAMMA_B_PRED_SUNWARD_SIG": "Amdt 12(c)",
    "GAMMA_GATED_10KAU": "registered as a WATCH item, not a decisive test",
}
EXCLUDED_WHY = {"GAMMA_B_PRED_SIG": "an uncertainty, not an edge", "GAMMA_B_PRED_SUNWARD_SIG": "an uncertainty, not an edge"}
NOT_IN_CODE = ["Amendment 14's chain ceiling (1.0725 canonical / 1.0900 alt) is not a constant of the frozen pipeline (it appears in the amendment text only)",
               "sigma_sys = 0.02 is not a named constant of the pipeline; it is read from PREREGISTRATION_DR4.md section 1.5"]


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _load_module(path):
    spec = importlib.util.spec_from_file_location("wide_binary_pipeline_readonly", str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("wide_binary_pipeline_readonly", mod)
    spec.loader.exec_module(mod)
    return mod


def extract_edge_table(pipeline_path=PIPELINE, prereg_path=PREREG, expected_sha=FROZEN_PIPELINE_SHA256):
    """the machine-readable edge table, extracted from the pipeline module and its source text."""
    pipeline_path = Path(pipeline_path)
    sha = file_sha256(pipeline_path)
    if expected_sha is not None and sha != expected_sha:
        raise RuntimeError(f"the frozen pipeline's sha256 changed: {sha} != {expected_sha}")
    mod = _load_module(pipeline_path)
    text = pipeline_path.read_text()
    lines = text.splitlines()
    names = sorted(n for n in dir(mod) if FAMILY_RE.match(n))
    classified = set(IN_FORCE_TARGETS) | set(IN_FORCE_HARD) | set(STABILITY) | set(EXCLUDED)
    if sorted(set(names) - classified):
        raise ValueError(f"unclassified decision constant(s) in the pipeline: {sorted(set(names) - classified)}")
    if sorted(classified - set(names)):
        raise ValueError(f"classified constant(s) missing from the pipeline: {sorted(classified - set(names))}")

    def src_line(n):
        for i, l in enumerate(lines, 1):
            if re.match(rf"^{n}\s*=", l):
                return i, l.strip()
        raise ValueError(f"no definition line for {n}")
    for n, reason in EXCLUDED.items():
        if reason not in text:
            raise ValueError(f"the exclusion reason of {n} ({reason!r}) does not occur in the pipeline source")
    pre = Path(prereg_path).read_text()
    if not re.search(r"\*\*sigma_sys = 0\.02\*\*", pre):
        raise ValueError("sigma_sys = 0.02 not found in the pre-registration text")
    val = lambda n: getattr(mod, n)
    targets = {"canonical": [], "alt": []}
    for n, (lab, foots) in IN_FORCE_TARGETS.items():
        ln, sl = src_line(n)
        for f in foots:
            targets[f].append(dict(constant=n, name=lab, gamma=float(val(n)), source_line=ln, source=sl))
    hard = []
    for n, lab in IN_FORCE_HARD.items():
        ln, sl = src_line(n)
        hard.append(dict(constant=n, name=lab, gamma=float(val(n)), source_line=ln, source=sl))
    excluded = {}
    for n, reason in EXCLUDED.items():
        ln, sl = src_line(n)
        excluded[n] = dict(value=getattr(mod, n), reason=EXCLUDED_WHY.get(n, reason), source_line=ln, source=sl)
    kl, ks = src_line("KAPPA_WINDOW")
    return dict(about="Amendment 18 (draft rev 2, NOT FILED) edge table: the in-force decision constants of the frozen pipeline, extracted BY CODE; every constant of the families GAMMA_*, NOVERDICT_EDGE, KAPPA_* is classified; "
                      "the z-rule edges are t -+ 2 sigma_tot and t -+ 3 sigma_tot around each target t at the PRIMARY's sigma_tot",
                pipeline_sha256=sha, preregistration="PREREGISTRATION_DR4.md section 1.5: sigma_sys = 0.02 (frozen allowance); z-rule 'consistent |z| < 2', 'disfavored |z| > 3'",
                sigma_sys=0.02, z_rule=dict(consistent=2, disfavored=3), targets=targets, hard_edges=hard,
                stability=dict(kappa_window=[float(x) for x in val("KAPPA_WINDOW")], kappa_source_line=kl, kappa_source=ks, ladder_shift_below_sigma_fit=1.0,
                               ladder_rungs_implemented=["R_chance<0.001", "sep 3-20 kAU", "RUWE<1.2 both"], ladder_rungs_NOT_IMPLEMENTED=["RV-screened subsample only", "NSS screen OFF"]),
                excluded=excluded, not_in_code=NOT_IN_CODE, classified_constants=sorted(classified))


def edges_for(table, footing, sigma_tot):
    """[(name, value)]: the z-rule edges around every target of the footing and the hard edges."""
    out = []
    for t in table["targets"][footing]:
        for n in (3, 2):
            out.append((f"{t['constant']} - {n} sigma_tot", t["gamma"] - n * sigma_tot))
        for n in (2, 3):
            out.append((f"{t['constant']} + {n} sigma_tot", t["gamma"] + n * sigma_tot))
    for h in table["hard_edges"]:
        out.append((h["constant"], h["gamma"]))
    return out


def sd1(x):
    return float(np.std(np.asarray(x, float), ddof=1))


def label_report(gammas_g, sigma_fit, table, footing, gammas_full=None, min_further=MIN_FURTHER_BUILDS):
    """gammas_g: gamma-hat of the G-only builds, k = 0 (the primary) first; sigma_fit: the primary's."""
    g = np.asarray(gammas_g, float)
    primary = float(g[0])
    if len(g) - 1 < min_further:
        return dict(footing=footing, label="NOT APPLICABLE (K < %d)" % min_further, K=len(g) - 1, primary=primary)
    sb = sd1(g)
    width = max(sb, WIDTH_FLOOR * sigma_fit)
    sigma_tot = math.hypot(sigma_fit, table["sigma_sys"])
    flagged = []
    for name, val in edges_for(table, footing, sigma_tot):
        d = abs(primary - val)
        if d <= width:
            e = dict(edge=name, value=val, distance=d, builds_below=int((g < val).sum()), builds_at_or_above=int((g >= val).sum()))
            if gammas_full is not None:
                gf = np.asarray(gammas_full, float)
                e.update(full_builds_below=int((gf < val).sum()), full_builds_at_or_above=int((gf >= val).sum()))
            flagged.append(e)
    return dict(footing=footing, K=len(g) - 1, primary=primary, sigma_fit=float(sigma_fit), sigma_tot=sigma_tot, sigma_build=sb, sigma_build_full=(sd1(gammas_full) if gammas_full is not None and len(gammas_full) > 1 else None),
                width=width, width_governed_by=("sigma_build" if sb >= WIDTH_FLOOR * sigma_fit else "0.3 sigma_fit"), label=("seed-sensitive" if flagged else "not seed-sensitive at the edges of the table"), flagged=flagged)


def stability_report(kappas, kappa_window, ladder_shifts=None):
    """conditions evaluated for every build; a condition whose pass/fail status differs across builds is labelled 'seed-sensitive'.
    kappas: per-build kappa; ladder_shifts: {rung: per-build shift in units of sigma_fit} (only implemented rungs)."""
    out = {}
    kp = [bool(kappa_window[0] <= k <= kappa_window[1]) for k in kappas]
    out["kappa window"] = dict(passes=int(sum(kp)), fails=int(len(kp) - sum(kp)), label="seed-sensitive" if 0 < sum(kp) < len(kp) else "stable")
    for rung, sh in (ladder_shifts or {}).items():
        lp = [bool(abs(s) < 1.0) for s in sh]
        out[f"ladder {rung}"] = dict(passes=int(sum(lp)), fails=int(len(lp) - sum(lp)), label="seed-sensitive" if 0 < sum(lp) < len(lp) else "stable")
    return out


def evaluate_sweep(manifest_g, manifest_full=None, table=None):
    """the label report of a DR3 or DR4 sweep from the manifests written by seed_sweep.py."""
    table = table or extract_edge_table()
    Mg = json.load(open(manifest_g))
    Mf = json.load(open(manifest_full)) if manifest_full else None
    rep = dict(manifest_g=str(manifest_g), manifest_full=str(manifest_full) if manifest_full else None, footings={})
    for f in ("canonical", "alt"):
        gG = [b["fit"][f]["g"] for b in Mg["builds"]]
        sfit = Mg["builds"][0]["fit"][f]["s"]
        gF = [b["fit"][f]["g"] for b in Mf["builds"]] if Mf else None
        rep["footings"][f] = label_report(gG, sfit, table, f, gF)
        kap = [b["fit"][f]["kappa"] for b in Mg["builds"]]
        shifts = {}
        if all("ladder" in b for b in Mg["builds"]):
            for rung in [r for r in Mg["builds"][0]["ladder"] if r != "NOT_IMPLEMENTED"]:
                shifts[rung] = [(b["ladder"][rung]["fit"][f]["g"] - b["fit"][f]["g"]) / b["fit"][f]["s"] for b in Mg["builds"]]
        rep["footings"][f]["stability"] = stability_report(kap, table["stability"]["kappa_window"], shifts)
    return rep


def format_report(rep):
    out = []
    for f, r in rep["footings"].items():
        out.append(f"  {f:9s}: {r['label']}" + (f"; primary gamma-hat {r['primary']:.4f}, sigma_fit {r['sigma_fit']:.4f}, sigma_tot {r['sigma_tot']:.4f}, sigma_build {r['sigma_build']:.4f}" + (f" (full-rebuild SD {r['sigma_build_full']:.4f})" if r.get("sigma_build_full") is not None else "")
                                                   + f"; width {r['width']:.4f} set by {r['width_governed_by']}; K = {r['K']}" if "sigma_build" in r else ""))
        for e in r.get("flagged", []):
            out.append(f"      edge {e['edge']} = {e['value']:.4f} (distance {e['distance']:.4f}): {e['builds_below']} builds below, {e['builds_at_or_above']} at or above" + (f"; full rebuilds {e['full_builds_below']} / {e['full_builds_at_or_above']}" if "full_builds_below" in e else ""))
        for k, v in r.get("stability", {}).items():
            out.append(f"      stability {k}: {v['passes']} pass, {v['fails']} fail -> {v['label']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-edge-table", default=None)
    ap.add_argument("--evaluate", default=None, help="the G-only sweep manifest (seed_sweep_manifest*.json)")
    ap.add_argument("--full", default=None, help="the full-rebuild sweep manifest (reported beside)")
    ap.add_argument("--table", default=None, help="an edge table JSON (default: extracted now)")
    ap.add_argument("--write-report", default=None)
    a = ap.parse_args()
    if a.write_edge_table:
        t = extract_edge_table()
        Path(a.write_edge_table).write_text(json.dumps(t, indent=1, default=str) + "\n")
        print("wrote", a.write_edge_table, "; targets canonical", [x["constant"] for x in t["targets"]["canonical"]], "; hard", [x["constant"] for x in t["hard_edges"]], "; excluded", sorted(t["excluded"]))
    if a.evaluate:
        table = json.load(open(a.table)) if a.table else None
        rep = evaluate_sweep(a.evaluate, a.full, table)
        print("\n".join(format_report(rep)))
        if a.write_report:
            Path(a.write_report).write_text(json.dumps(rep, indent=1, default=float) + "\n")


if __name__ == "__main__":
    main()
