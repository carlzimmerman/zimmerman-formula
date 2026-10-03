#!/usr/bin/env python3
"""Release-day companion to the frozen pipeline's [7(e)] report (NEW file; nothing frozen is edited).

Why: Amendment 14(f) extends the 7(e) reporting rule -- the raw gamma_hat with sigma_fit and its distances to the
chain's ceilings (1.0725 canonical / 1.0900 alt) are ALSO reported -- and says "No pipeline file changes".  The frozen
wide_binary_pipeline.py (sha 7c884e0e...) therefore never prints them; seed_label.py lists the ceiling as NOT_IN_CODE.
Found by the 2026-10-03 dry run.  This script reads a pipeline log and prints those distances.

It also flags any catalogue fit whose gamma_hat sits ON an edge of the frozen estimator grid (GRID, read from the
pipeline): such a fit is boundary-pinned, and its sigma_fit is not a measurement.  The 2026-10-03 DR3 dry run had every
proj-PARALLEL fit pinned at the 0.90 floor, which inflates the anisotropy split.  Flag only: the grid is frozen.

Every registered number is READ from the frozen texts (Amendment 14(d) rows and sigma_tot from PREREGISTRATION_DR4.md,
GRID from wide_binary_pipeline.py), never typed here.  No verdict word is printed (Amendment 7(e)); the interval
gamma_hat falls in is named by its edges only.

Run:  python3 amdt14_distances.py --log <pipeline --catalog output>      (prints the block; exit 0)
      python3 amdt14_distances.py --self-test                              (offline; MUTATE=1 must fail)
"""
import argparse, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
PREREG = PREP / "PREREGISTRATION_DR4.md"
PIPELINE = PREP / "wide_binary_pipeline.py"


def registered():
    t = PREREG.read_text(encoding="utf-8")
    # Amendments 13 and 14 share the '(d) Decision rows' heading; Amendment 14's table header is unique
    assert t.count("| γ̂ lands in | the chain's reading |") == 1, "Amendment 14(d) table header not unique"
    i = t.find("| γ̂ lands in | the chain's reading |")
    blk = t[i - 400:i + 2600]
    s_tot = float(re.search(r"σ_tot = ([0-9.]+), the table's convention", blk).group(1))
    m_ceil = re.search(r"\| ≤ ([0-9.]+) \(≤ ([0-9.]+)\) \|", blk)
    m_kill = re.search(r"\| ≥ ([0-9.]+) \(≥ ([0-9.]+)\) \|", blk)
    m_edge = re.search(r"\| > ([0-9.]+) \| \*\*no verdict\*\*", blk)
    g = re.search(r"^GRID = np\.arange\(([0-9.]+), ([0-9.]+), ([0-9.]+)\)", PIPELINE.read_text(encoding="utf-8"), re.M)
    lo, hi_arg, step = (float(x) for x in g.groups())
    hi = lo + step * int(round((hi_arg - lo) / step - 0.5))
    return {"sigma_tot": s_tot,
            "ceil": {"canonical": float(m_ceil.group(1)), "alt": float(m_ceil.group(2))},
            "kill": {"canonical": float(m_kill.group(1)), "alt": float(m_kill.group(2))},
            "edge": float(m_edge.group(1)), "grid": (lo, hi)}


FIT = re.compile(r"catalog \[a0 (canonical|alt footing)\]\s*(proj-PARALLEL |proj-PERPENDICULAR )?\s*gamma_inf = ([0-9.]+) \+- ([0-9.]+)")


def parse(log_text):
    out = []
    for m in FIT.finditer(log_text):
        out.append({"footing": "canonical" if m.group(1) == "canonical" else "alt",
                    "subset": (m.group(2) or "all").strip(), "g": float(m.group(3)), "s": float(m.group(4))})
    return out


def report(fits, R):
    L = []
    for f in fits:
        on_edge = abs(f["g"] - R["grid"][0]) < 1e-9 or abs(f["g"] - R["grid"][1]) < 1e-9
        if f["subset"] != "all":
            if on_edge:
                L.append(f"[A14] GRID-EDGE: {f['footing']} {f['subset']} gamma_hat = {f['g']:.4f} sits on the frozen grid edge "
                         f"{R['grid']}; boundary-pinned, its sigma_fit {f['s']:.4f} is not a measurement")
            continue
        c, k = R["ceil"][f["footing"]], R["kill"][f["footing"]]
        if f["g"] > R["edge"]:
            iv = f"> {R['edge']}"
        elif f["g"] >= k:
            iv = f">= {k}"
        elif f["g"] > c:
            iv = f"{c} - {k}"
        else:
            iv = f"<= {c}"
        L.append(f"[A14] {f['footing']}: raw gamma_hat = {f['g']:.4f}, sigma_fit = {f['s']:.4f}; distance to the chain ceiling "
                 f"{c} = {(f['g'] - c) / f['s']:+.2f} sigma_fit = {(f['g'] - c) / R['sigma_tot']:+.2f} sigma_tot ({R['sigma_tot']}); "
                 f"to the row edge {k} = {(f['g'] - k) / R['sigma_tot']:+.2f} sigma_tot; Amendment 14(d) interval: {iv}"
                 + ("  [GRID-EDGE: boundary-pinned]" if on_edge else ""))
    L.append("[A14] distances only; no verdict word (Amendment 7(e)); the stability requirements of the >= row are not evaluated here")
    # Amendment 20: per footing, the anisotropy split is measurable only if neither orientation fit sits on a grid edge
    for fo in ("canonical", "alt"):
        sub = {f["subset"]: f for f in fits if f["footing"] == fo and f["subset"] != "all"}
        if not sub:
            continue
        pinned = [f"{k} {v['g']:.4f}" for k, v in sorted(sub.items())
                  if abs(v["g"] - R["grid"][0]) < 1e-9 or abs(v["g"] - R["grid"][1]) < 1e-9]
        if pinned or len(sub) < 2:
            L.append(f"[A20] {fo}: anisotropy split NOT MEASURABLE -- NOT QUOTED; cannot falsify, support or be read "
                     f"({'; '.join(pinned) if pinned else 'an orientation fit is missing'} on the frozen grid edge)")
        else:
            L.append(f"[A20] {fo}: anisotropy split MEASURABLE (neither orientation fit on a grid edge) -- report the "
                     f"pipeline's [aniso] line as registered (Amendments 2(f), 3(c), 8(f), 11(d2))")
    return L


def self_test():
    R = registered()
    mut = os.environ.get("MUTATE") == "1"
    ok = []
    ok.append(R["ceil"] == {"canonical": 1.0725, "alt": 1.0900} and R["kill"] == {"canonical": 1.157, "alt": 1.174}
              and R["sigma_tot"] == 0.028 and R["edge"] == 1.23)
    ok.append(R["grid"] == (0.90, 1.50))
    log = ("  catalog [a0 canonical]             gamma_inf = 1.0750 +- 0.0550  (chi2)\n"
           "  catalog [a0 canonical] proj-PARALLEL gamma_inf = 0.9000 +- 0.0250  (chi2)\n"
           "  catalog [a0 alt footing]           gamma_inf = 1.1800 +- 0.0500  (chi2)\n")
    if mut:
        log = log.replace("1.0750", "1.0700")
    rep = report(parse(log), R)
    ok.append(any("canonical: raw gamma_hat = 1.0750" in l and "+0.05 sigma_fit" in l and "interval: 1.0725 - 1.157" in l for l in rep))
    ok.append(any("alt: raw gamma_hat = 1.1800" in l and "interval: >= 1.174" in l for l in rep))
    ok.append(any("GRID-EDGE" in l and "proj-PARALLEL" in l for l in rep))
    ok.append(not any(re.search(r"\b(confirm|falsif|consistent|kill)", l, re.I) for l in rep if l.startswith("[A14]")))
    # Amendment 20: canonical has a pinned PARALLEL fit -> not measurable; a clean pair -> measurable
    ok.append(any(l.startswith("[A20] canonical: anisotropy split NOT MEASURABLE") and "proj-PARALLEL 0.9000" in l for l in rep))
    clean = ("  catalog [a0 alt footing]           gamma_inf = 1.1800 +- 0.0500  (chi2)\n"
             "  catalog [a0 alt footing] proj-PARALLEL gamma_inf = 1.1200 +- 0.0400  (chi2)\n"
             "  catalog [a0 alt footing] proj-PERPENDICULAR gamma_inf = 1.2400 +- 0.0600  (chi2)\n")
    if mut:
        clean = clean.replace("1.2400", "1.5000")
    ok.append(any(l.startswith("[A20] alt: anisotropy split MEASURABLE") for l in report(parse(clean), R)))
    for i, o in enumerate(ok, 1):
        print(f"  [{'PASS' if o else 'FAIL'}] S{i}")
    print(f"{sum(ok)}/{len(ok)} checks pass" + ("  [MUTATE=1: a failure is REQUIRED]" if mut else ""))
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    fits = parse(Path(a.log).read_text(encoding="utf-8"))
    if not fits:
        sys.exit("no catalogue fit lines found in the log")
    print("\n".join(report(fits, registered())))


if __name__ == "__main__":
    main()
