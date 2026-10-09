#!/usr/bin/env python3
"""Release-day companion for Arm C and Amendment 21 (NEW file; nothing frozen is edited).

Why: Arm C's decision rows (the ownership rule, gamma_C = 1.000) are decided by z_C = (gamma_hat - 1.000) / sigma_tot with
sigma_tot = sqrt(sigma_fit^2 + sigma_sys^2), sigma_sys = 0.02 (PREREGISTRATION_DR4.md section 1).  Amendment 21 (2026-10-06)
registers the settling working model's gamma = 1.000 against those SAME rows.  The frozen pipeline's [7(e)] block prints the
distance to Newton 1.000 in sigma_fit only, and no tool prints z_C or names the Arm C row.  Found by the 2026-10-09 dry run.

Every registered number is READ from the frozen text (gamma_C, sigma_sys, the Arm C table edges, the 1.23 no-verdict edge);
none is typed here.  The row is chosen by the operative z-rule on the DATA's sigma_tot, not by the illustrative edges, which
are also printed.  No verdict word is printed (Amendment 7(e)); stability requirements of the falsification row are NOT
evaluated here (ladder within 1 sigma_fit, kappa in [0.95, 1.05], NSS-off probe) -- the operator checks them from the log.

Run:  python3 arm_c_rows.py --log <pipeline --catalog output>      (exit 0)
      python3 arm_c_rows.py --self-test                              (offline; MUTATE=1 must fail)
"""
import argparse, math, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREREG = HERE.parent / "PREREGISTRATION_DR4.md"
FIT = re.compile(r"catalog \[a0 (canonical|alt footing)\]\s*(proj-PARALLEL |proj-PERPENDICULAR )?\s*gamma_inf = ([0-9.]+) \+- ([0-9.]+)")


def registered():
    t = PREREG.read_text(encoding="utf-8")
    hdr = "| γ̂ lands in | Arm C | added reading |"
    assert t.count(hdr) == 1, "Arm C table header not unique"
    i = t.find(hdr); blk = t[i - 1200:i + 1600]
    gC = float(re.search(r"γ_C = ([0-9.]+) and z_C = \(γ̂ − ([0-9.]+)\)/σ_tot", blk).group(1))
    s_sys = float(re.search(r"\*\*sigma_sys = ([0-9.]+)\*\* \(frozen allowance\)", t).group(1))
    assert "**sigma_tot = sqrt(sigma_fit^2 + 0.02^2)**" in t, "frozen sigma_tot definition not found"
    first_cells = []
    for line in t[i:i + 1600].splitlines()[1:]:          # lines after the header
        if not line.startswith("> |"):
            break
        cell = line[3:].split("|")[0].strip()
        if set(cell) <= set("-"):                         # the |---| rule line
            continue
        first_cells.append(cell)
    edges = sorted({float(x) for c in first_cells for x in re.findall(r"[0-9]\.[0-9]+", c)})
    nv = float(re.search(r"\| > ([0-9.]+) \| \*\*no verdict\*\*", t[i:i + 1600]).group(1))
    a21 = "AMENDMENT 21" in t or "Amendment 21" in t
    return dict(gC=gC, s_sys=s_sys, edges=edges, no_verdict=nv, a21=a21)


def report(log_text, R):
    L = []
    for m in FIT.finditer(log_text):
        if m.group(2):                                    # orientation subsets are not Arm C's statistic
            continue
        fo = "canonical" if m.group(1) == "canonical" else "alt"
        g, sf = float(m.group(3)), float(m.group(4))
        st = math.hypot(sf, R["s_sys"]); z = (g - R["gC"]) / st
        if g > R["no_verdict"]:
            row = f"> {R['no_verdict']} (frozen guard zone)"
        elif z >= 3:
            row = "z_C >= 3 (the falsification row, only if the frozen stability requirements pass)"
        elif z >= 2:
            row = "2 <= z_C < 3 (disfavoured, not a kill)"
        elif z > -2:
            row = "|z_C| < 2 (the consistent row)"
        elif z > -3:
            row = "-3 < z_C <= -2"
        else:
            row = "z_C <= -3 (sub-Newtonian row)"
        ill = next((f"{a}-{b}" for a, b in zip([-1] + R["edges"], R["edges"] + [9]) if a < g <= b), "?")
        L.append(f"[ArmC] {fo}: raw gamma_hat = {g:.4f}, sigma_fit = {sf:.4f}, sigma_tot = sqrt(sigma_fit^2 + {R['s_sys']}^2) = {st:.4f}; "
                 f"z_C = (gamma_hat - {R['gC']:.3f})/sigma_tot = {z:+.2f}; Arm C row by the operative z-rule: {row}; "
                 f"illustrative-edge interval (sigma_tot 0.028): {ill}")
    if R["a21"]:
        L.append("[ArmC] Amendment 21: the settling working model's gamma = 1.000 is scored on these same Arm C rows; "
                 "a Newtonian result is survival only, never confirmation (read the amendment text for its full rule)")
    L.append("[ArmC] distances and rows only; no verdict word (Amendment 7(e)); stability requirements not evaluated here")
    return L


def self_test():
    R = registered(); mut = os.environ.get("MUTATE") == "1"; ok = []
    ok.append(R["gC"] == 1.0 and R["s_sys"] == 0.02 and R["no_verdict"] == 1.23 and R["edges"][:4] == [0.916, 0.944, 1.056, 1.084])
    log = ("  catalog [a0 canonical]             gamma_inf = 1.0750 +- 0.0550  (chi2)\n"
           "  catalog [a0 canonical] proj-PARALLEL gamma_inf = 0.9000 +- 0.0250  (chi2)\n"
           "  catalog [a0 alt footing]           gamma_inf = 1.1000 +- 0.0190  (chi2)\n")
    if mut:
        log = log.replace("1.1000 +- 0.0190", "1.0400 +- 0.0190")
    rep = report(log, R)
    zc = 0.075 / math.hypot(0.055, 0.02); za = 0.100 / math.hypot(0.019, 0.02)
    ok.append(any(f"z_C = (gamma_hat - 1.000)/sigma_tot = {zc:+.2f}" in r and "|z_C| < 2" in r for r in rep))
    ok.append(any(f"= {za:+.2f}" in r and "z_C >= 3" in r for r in rep))
    ok.append(sum(r.startswith("[ArmC] canonical") or r.startswith("[ArmC] alt") for r in rep) == 2)   # subset skipped
    ok.append(not any("CONSISTENT" in r or "FALSIFIED" in r for r in rep))                             # no verdict words
    for r in rep:
        print(r)
    print(f"\nself-test {sum(ok)}/{len(ok)} -> {'PASS' if all(ok) else 'FAIL'}{' (MUTATE)' if mut else ''}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--log"); ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    for r in report(Path(a.log).read_text(encoding="utf-8"), registered()):
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
