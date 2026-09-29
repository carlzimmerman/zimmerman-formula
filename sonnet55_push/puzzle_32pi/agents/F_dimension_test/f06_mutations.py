#!/usr/bin/env python3
"""f06_mutations.py -- mutation runner for f01-f05.  Each mutant changes ONE load-bearing claim to a wrong one in a temporary copy and must make that script exit non-zero.
Also re-runs the five real scripts and requires exit 0.  Exit 0 = all five real scripts pass and all mutants are caught."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = ["f01_ddim_ingredients.py", "f02_deep_mond_ddim.py", "f03_volume_law_ddim.py", "f04_topological_units_ddim.py", "f05_reading_matrix.py"]
MUTANTS = [
    ("f01_ddim_ingredients.py", "sp.simplify(H2v - 16 * sp.pi * G * rho / (d * (d - 1))) == 0", "sp.simplify(H2v - 8 * sp.pi * G * rho / 3) == 0", "Friedmann coefficient taken d-independent (8 pi/3)"),
    ("f01_ddim_ingredients.py", "8 * sp.pi * G * ((d - 2) * rho + d * p) / (d * (d - 1))) == 0", "8 * sp.pi * G * (rho + d * p) / (d * (d - 1))) == 0", "naive rho + d p acceleration law (the PD11 form)"),
    ("f01_ddim_ingredients.py", "sp.simplify(kap_bh - (n - 1) / (2 * rs)) == 0", "sp.simplify(kap_bh - n / (2 * rs)) == 0", "Tangherlini surface gravity d/(2 r_s) instead of (d-2)/(2 r_s)"),
    ("f02_deep_mond_ddim.py", "sp.simplify(e - sp.Rational(3 - dd, 2)) == 0)", "sp.simplify(e - sp.Rational(3 - dd, 3)) == 0)", "wrong deep-MOND exponent"),
    ("f02_deep_mond_ddim.py", "sol_conf == [dd_ - 2])", "sol_conf == [dd_ - 1])", "conformal invariance at p = d+1"),
    ("f03_volume_law_ddim.py", "(Dd - 3) / ((Dd - 2) * (Dd - 1))) == 0 and aM_over_a0", "(Dd - 3) / ((Dd - 2) * (Dd - 2))) == 0 and aM_over_a0", "wrong Verlinde D-dependence"),
    ("f04_topological_units_ddim.py", "U[4] == 32 * sp.pi**2 and sp.simplify((2 * sp.pi)**2 * 2)", "U[4] == 30 * sp.pi**2 and sp.simplify((2 * sp.pi)**2 * 2)", "wrong Gauss-Bonnet unit 30 pi^2"),
    ("f04_topological_units_ddim.py", "c5 == sp.Rational(9, 4)", "c5 == sp.Rational(9, 5)", "wrong d = 5 coefficient of AL/U"),
    ("f05_reading_matrix.py", "sp.solve(sp.Eq((d - 2) / 2, sp.Rational(1, 2)), d) == [3])", "sp.solve(sp.Eq((d - 2) / 2, sp.Rational(1, 2)), d) == [4])", "wrong crossing dimension"),
    ("f05_reading_matrix.py", "sp.simplify(Zd2 * dimSO * kap**2 - 8 * sp.pi) == 0", "sp.simplify(Zd2 * dimSO * kap**2 - 4 * sp.pi) == 0", "wrong dim SO(d) identity constant"),
]

def run(path):
    return subprocess.run([sys.executable, path], capture_output=True, text=True)

ok = []
print("REAL scripts")
for fn in REAL:
    r = run(os.path.join(HERE, fn))
    last = [ln for ln in r.stdout.splitlines() if 'checks held' in ln][-1].strip()
    print(f"  {fn:<34} exit={r.returncode}   {last}")
    ok.append(r.returncode == 0)
print("\nMUTANTS (each must exit non-zero)")
with tempfile.TemporaryDirectory() as td:
    for fn, old, new, why in MUTANTS:
        src = open(os.path.join(HERE, fn)).read()
        if old not in src:
            print(f"  [SETUP ERROR] pattern not found in {fn}: {old[:60]}")
            ok.append(False)
            continue
        path = os.path.join(td, "mut_" + fn)
        open(path, "w").write(src.replace(old, new, 1))
        r = run(path)
        fails = [ln.strip() for ln in r.stdout.splitlines() if '[FAIL]' in ln]
        caught = r.returncode != 0 and len(fails) >= 1
        ok.append(caught)
        print(f"  [{'CAUGHT' if caught else 'MISSED'}] {why}  ({fn}: exit={r.returncode}, {len(fails)} failed checks)")
print(f"\n  {sum(ok)}/{len(ok)}")
sys.exit(0 if all(ok) else 1)
