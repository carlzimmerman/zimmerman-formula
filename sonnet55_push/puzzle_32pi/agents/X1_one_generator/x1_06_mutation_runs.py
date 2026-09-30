#!/usr/bin/env python3
"""x1_06_mutation_runs.py -- lane X1: does the suite fail when a load-bearing constant is wrong?
Step 1: run x1_01 .. x1_05 clean (each must exit 0; x1_01/x1_02 first because x1_03/x1_04 read their JSON output).
Step 2: for each of 22 mutations (ONE load-bearing constant or expectation changed in a temporary copy of ONE script) the copy must exit NON-zero AND print at least one FAIL line without a Python traceback (a crash does not count as a catch).
Mutated copies live in a temporary directory (deleted at the end); no file of the lane is modified.  Exit 0 iff 5/5 clean runs pass and 22/22 mutants are caught.
"""
import sys, os, shutil, subprocess, tempfile, time
from concurrent.futures import ThreadPoolExecutor

here = os.path.dirname(os.path.abspath(__file__))
scripts = ['x1_01_atoms.py', 'x1_02_dlifts.py', 'x1_03_ledger.py', 'x1_04_candidates_of_4.py', 'x1_05_noether_euler_static_patch.py']
def run(path, cwd):
    p = subprocess.run([sys.executable, path], cwd=cwd, capture_output=True, text=True)
    last = [l for l in p.stdout.strip().splitlines() if 'behave as declared' in l]
    nfail = sum(1 for l in p.stdout.splitlines() if l.startswith('FAIL'))
    crashed = 'Traceback' in p.stderr
    return p.returncode, (last[-1] if last else 'no summary line'), nfail, crashed
T0 = time.time()
results = []
print("CLEAN RUNS")
with ThreadPoolExecutor(2) as ex:
    a = list(ex.map(lambda s: (s, run(os.path.join(here, s), here)), scripts[:2]))
with ThreadPoolExecutor(3) as ex:
    b = list(ex.map(lambda s: (s, run(os.path.join(here, s), here)), scripts[2:]))
clean_ok = 0
for s, (rc, msg, nfail, crashed) in a + b:
    good = rc == 0 and nfail == 0 and not crashed
    clean_ok += good
    print("  %s %-42s exit %d  %s" % ("PASS" if good else "FAIL", s, rc, msg))

MUT = [
 ('x1_01_atoms.py', "sp.simplify(S2 - 4 * sp.pi) == 0 and sp.simplify(Omega[2] - 4 * sp.pi) == 0", "sp.simplify(S2 - 2 * sp.pi) == 0 and sp.simplify(Omega[2] - 2 * sp.pi) == 0", 'S2 area 4 pi -> 2 pi'),
 ('x1_01_atoms.py', "ratio == sp.Rational(D - 2, D - 3)", "ratio == sp.Rational(D - 1, D - 3)", 'trace-reversal factor (D-2)/(D-3) -> (D-1)/(D-3)'),
 ('x1_01_atoms.py', "Ltarget = sp.Rational(1, 2) *", "Ltarget = sp.Rational(1, 3) *", 'TT quadratic coefficient 1/2 -> 1/3'),
 ('x1_01_atoms.py', "192 * rho ** 4 / (x2 + rho ** 2) ** 4) == 0", "96 * rho ** 4 / (x2 + rho ** 2) ** 4) == 0", 'BPST F^2 192 -> 96'),
 ('x1_01_atoms.py', "sp.simplify(24 * S4 - 64 * sp.pi ** 2)", "sp.simplify(12 * S4 - 64 * sp.pi ** 2)", 'E4 on S^4: 24 -> 12'),
 ('x1_01_atoms.py', "Qgen - Rsym ** 2 * sp.diff(fgen, Rsym) / (4 * Gs)", "Qgen - Rsym ** 2 * sp.diff(fgen, Rsym) / (8 * Gs)", 'Iyer-Wald Q = r^2 f\'/(4G) -> /(8G)'),
 ('x1_02_dlifts.py', "pred = e - 2 * (D - 2) * (D - 3) * kk * R", "pred = e - (D - 2) * (D - 3) * kk * R", 'GB shift 2(D-2)(D-3) -> (D-2)(D-3)'),
 ('x1_02_dlifts.py', "val = -2 * np.pi * (1 / (32 * np.pi))", "val = -2 * np.pi * (1 / (16 * np.pi))", 'Wald entropy coefficient 1/(32 pi) -> 1/(16 pi)'),
 ('x1_02_dlifts.py', "sp.simplify(kap * rhs - sp.Rational(D - 3, 2)) == 0", "sp.simplify(kap * rhs - sp.Rational(D - 2, 2)) == 0", 'Tangherlini kappa r_h (D-3)/2 -> (D-2)/2'),
 ('x1_02_dlifts.py', "all(tt_coef[D] == sp.Rational(1, 2) for D in Ds)", "all(tt_coef[D] == sp.Rational(1, 3) for D in Ds)", 'TT coefficient 1/2 -> 1/3 in D = 4..8'),
 ('x1_03_ledger.py', "MMQ_val = sp.Rational(1, 4)", "MMQ_val = sp.Rational(1, 2)", 'MM algebra 1/4 -> 1/2'),
 ('x1_03_ledger.py', "sp.simplify(isaacson_val - 1 / (32 * pi)) == 0", "sp.simplify(isaacson_val - 1 / (16 * pi)) == 0", 'Isaacson 1/(32 pi) -> 1/(16 pi)'),
 ('x1_03_ledger.py', "{'CAN': 1, 'VAR': 1, 'BIA': 1, 'S2': 1, 'QEH': -1}", "{'CAN': 1, 'VAR': 1, 'BIA': 1, 'S2': 1, 'QEH': -2}", 'kappa_g^2 decomposition exponent QEH -1 -> -2'),
 ('x1_03_ledger.py', "npair == 5", "npair == 6", 'number of D-lift-distinct slot pairs 5 -> 6'),
 ('x1_04_candidates_of_4.py', "slot_G = {D: sp.Integer(4) for D in Ds}", "slot_G = {D: sp.Integer(5) for D in Ds}", 'graviton slot 4 -> 5'),
 ('x1_04_candidates_of_4.py', "'c7 HORIZON':      lambda D: sp.Rational(4, (D - 3) ** 2)", "'c7 HORIZON':      lambda D: sp.Rational(4, (D - 3) ** 3)", 'c7 D-lift 4/(D-3)^2 -> 4/(D-3)^3'),
 ('x1_04_candidates_of_4.py', "hits[4][1] >= 10", "hits[4][1] >= 1000", 'decoy claim: >= 10 D-dependent hits -> >= 1000'),
 ('x1_04_candidates_of_4.py', "expected = D in (4, 5)", "expected = D in (4, 5, 6)", 'Myers-Perry expectation extended to D = 6'),
 ('x1_05_noether_euler_static_patch.py', "sp.simplify(Qr + r ** 3 / (2 * G * L ** 2)) == 0", "sp.simplify(Qr + r ** 3 / (G * L ** 2)) == 0", 'dS Noether charge -r^3/(2GL^2) -> -r^3/(GL^2)'),
 ('x1_05_noether_euler_static_patch.py', "sp.simplify(fac - (1 + 4 * alpha_s / L ** 2)) == 0", "sp.simplify(fac - (1 + 2 * alpha_s / L ** 2)) == 0", 'Euler-term factor 1 + 4 alpha/L^2 -> 1 + 2 alpha/L^2'),
 ('x1_05_noether_euler_static_patch.py', "MMalpha = -L ** 2 / 4", "MMalpha = -L ** 2 / 2", 'MM alpha -L^2/4 -> -L^2/2'),
 ('x1_05_noether_euler_static_patch.py', "all(b == sp.Rational(n, 2) for n, v, b in rows)", "all(b == sp.Rational(n, 3) for n, v, b in rows)", 'pi-power n/2 -> n/3'),
]
tmp = tempfile.mkdtemp(prefix='x1mut_')
for j in ('x1_atoms.json', 'x1_dlifts.json'):
    shutil.copy(os.path.join(here, j), tmp)
for s in scripts:
    pass
def do(mut):
    idx, (script, old, new, desc) = mut
    src = open(os.path.join(here, script)).read()
    n_occ = src.count(old)
    d = os.path.join(tmp, 'm%02d' % idx); os.makedirs(d)
    for j in ('x1_atoms.json', 'x1_dlifts.json'):
        shutil.copy(os.path.join(here, j), d)
    if n_occ < 1:
        return idx, script, desc, None, 'PATTERN NOT FOUND', 0, False
    open(os.path.join(d, script), 'w').write(src.replace(old, new, 1))
    rc, msg, nfail, crashed = run(os.path.join(d, script), d)
    return idx, script, desc, rc, msg, nfail, crashed
print("\nMUTATIONS (each must exit non-zero)")
with ThreadPoolExecutor(4) as ex:
    out = list(ex.map(do, list(enumerate(MUT, 1))))
caught = 0
for idx, script, desc, rc, msg, nfail, crashed in out:
    good = rc is not None and rc != 0 and nfail >= 1 and not crashed          # caught by a FAILING CHECK, not by a crash
    caught += good
    print("  %s m%02d %-42s %-52s exit %s, %d failing checks%s" % ("PASS" if good else "FAIL", idx, script, desc, rc, nfail, ', CRASHED' if crashed else ''))
shutil.rmtree(tmp, ignore_errors=True)
print("\nclean runs %d/%d, mutants caught %d/%d  (%.0f s)" % (clean_ok, len(scripts), caught, len(MUT), time.time() - T0))
sys.exit(0 if clean_ok == len(scripts) and caught == len(MUT) else 1)
