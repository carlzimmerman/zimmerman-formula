#!/usr/bin/env python3
"""c05_mutation_runs.py -- do the census scripts actually FAIL when a load-bearing number is wrong?

Each mutation copies one script into a scratch directory, changes ONE load-bearing constant (the claim's own coefficient), runs it, and requires
a non-zero exit with at least one FAIL line.  The unmutated scripts are run first and must exit 0 with no FAIL.
Exit 0 = every clean run passes and every mutated run is caught.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ['c01_gravity_instances.py', 'c02_dynamics_thermal_instances.py', 'c03_topology_loops_anomalies.py', 'c04_census_and_analysis.py']

MUT = [   # (script, old text, new text, label)
    ('c01_gravity_instances.py', "sp.simplify(t00 - h0**2 * w**2 / (32 * pi)) == 0)", "sp.simplify(t00 - h0**2 * w**2 / (16 * pi)) == 0)", "Isaacson coefficient 32 pi -> 16 pi"),
    ('c01_gravity_instances.py', "sp.Rational(32, 5) * Ga**4 * mu**2 * Mm**3 / a_**5) == 0)", "sp.Rational(64, 5) * Ga**4 * mu**2 * Mm**3 / a_**5) == 0)", "Peters 32/5 -> 64/5"),
    ('c01_gravity_instances.py', "sol == 32 * pi)", "sol == 16 * pi)", "graviton kappa^2 = 32 pi -> 16 pi (tensor convention)"),
    ('c02_dynamics_thermal_instances.py', "sp.simplify(tff**2 - 3 * pi / (32 * G * rho)) == 0)", "sp.simplify(tff**2 - 3 * pi / (16 * G * rho)) == 0)", "free-fall 3 pi/32 -> 3 pi/16"),
    ('c02_dynamics_thermal_instances.py', "sp.simplify(life - 5120 * pi * G**2 * Mh**3) == 0)", "sp.simplify(life - 2560 * pi * G**2 * Mh**3) == 0)", "Hawking lifetime 5120 pi -> 2560 pi"),
    ('c03_topology_loops_anomalies.py', "sp.simplify(FF - 32 * pi**2) == 0)", "sp.simplify(FF - 16 * pi**2) == 0)", "instanton integral 32 pi^2 -> 16 pi^2"),
    ('c03_topology_loops_anomalies.py', "sp.simplify(E4 - 24 / L**4) == 0)", "sp.simplify(E4 - 12 / L**4) == 0)", "S^4 Euler density 24/L^4 -> 12/L^4"),
    ('c03_topology_loops_anomalies.py', "sp.simplify(rho_dS - H**4 / (960 * pi**2)) == 0)", "sp.simplify(rho_dS - H**4 / (480 * pi**2)) == 0)", "de Sitter anomaly rho 960 pi^2 -> 480 pi^2"),
    ('c04_census_and_analysis.py', "[(E8, 1 / (8 * pi)), (ACT, R(1, 2)), (ACT, R(1, 4)), (ACT, 2)], 'scale', 'opened gr-qc/0501041", "[(E8, 1 / (8 * pi)), (ACT, R(1, 2)), (ACT, R(1, 3)), (ACT, 2)], 'scale', 'opened gr-qc/0501041", "census atom: Isaacson 1/4 -> 1/3"),
    ('c04_census_and_analysis.py', "[(E8, 8 * pi), (FIT, 4)], 'scale', 'the record; p01, p04'", "[(E8, 8 * pi), (FIT, 2)], 'scale', 'the record; p01, p04'", "census atom: puzzle 4 -> 2"),
]

def run(path):
    r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=1200, cwd=os.path.dirname(path))
    return r.returncode, r.stdout + r.stderr

results = []
print("clean runs")
for sc in SCRIPTS:
    rc, out = run(os.path.join(HERE, sc))
    nfail = out.count('[FAIL]')
    good = rc == 0 and nfail == 0
    results.append(good); print(f"  [{'OK' if good else 'FAIL'}] {sc}: exit {rc}, FAIL lines {nfail}")

print("mutated runs (each must be CAUGHT: non-zero exit and >= 1 FAIL line)")
tmp = tempfile.mkdtemp(prefix='c05_')
try:
    for f in os.listdir(HERE):
        if f.endswith('.out') or f.endswith('.py'):
            shutil.copy(os.path.join(HERE, f), tmp)
    for sc, old, new, label in MUT:
        src = open(os.path.join(HERE, sc)).read()
        if src.count(old) != 1:
            results.append(False); print(f"  [FAIL] mutation text not found exactly once in {sc}: {label}"); continue
        mp = os.path.join(tmp, sc)
        open(mp, 'w').write(src.replace(old, new))
        rc, out = run(mp)
        nfail = out.count('[FAIL]') + out.count('BAD:')
        caught = rc != 0 and nfail >= 1
        results.append(caught)
        print(f"  [{'OK' if caught else 'FAIL'}] {sc}: '{label}' -> exit {rc}, FAIL/BAD lines {nfail}")
        shutil.copy(os.path.join(HERE, sc), mp)                  # restore
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\n  {sum(results)}/{len(results)} clean runs pass and mutations caught.")
sys.exit(0 if all(results) else 1)
