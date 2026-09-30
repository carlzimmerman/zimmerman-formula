#!/usr/bin/env python3
"""z05: MUTATION HARNESS.  Each mutant is a copy of one Z6 script with ONE load-bearing line broken (a wrong moment, a wrong requirement, a wrong Sciama strength,
a wrong renormalisation, an unnormalised kernel, a loosened bound).  Every mutant must FAIL (non-zero exit); a mutant that passes means the scripts do not
constrain that line.  Mutant runs write to a throw-away directory inside this lane's directory (removed afterwards); no result file is overwritten."""
import subprocess, sys, tempfile, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = [
    ("z02", "wrong moment: sharp kernel replaced by an r^2 dr weight (m1 = 3/4, not 2/3)",
     '"sharp r dr (Sciama weight, [0,1])": (2 * xx, (0, 1)),', '"sharp r dr (Sciama weight, [0,1])": (3 * xx ** 2, (0, 1)),'),
    ("z02", "wrong requirement: (2/3) c/a0 -> c/a0 (the pre-renormalisation record value)",
     "M1_req = Rat(4, 3) * tL", "M1_req = Rat(2, 1) * tL"),
    ("z02", "wrong Sciama strength: 4 pi G rho -> 2 pi G rho",
     "w_S = 4 * pi * Gr * u ", "w_S = 2 * pi * Gr * u "),
    ("z01", "wrong renormalisation: mu_eff = mu + Y mu' (drop the 1/2 of the memory force)",
     "mueff = mu2 + Y * sp.diff(mu2, Y) / 2 ", "mueff = mu2 + Y * sp.diff(mu2, Y) "),
    ("z01", "wrong closed form: (4 + x^2) -> (2 + x^2) in the record's exponential-kernel Theta",
     "return 4 * Nv * vv * xx * mp.coth(mp.pi / xx) / (4 + xx ** 2)", "return 4 * Nv * vv * xx * mp.coth(mp.pi / xx) / (2 + xx ** 2)"),
    ("z03", "wrong weight: r dr -> r^2 dr in Sciama's force expansion",
     "w = Cc * u                                                          # weight ~ r dr on [0, T]", "w = Cc * u ** 2"),
    ("z04", "unnormalised kernel: 2/T^2 -> 3/T^2 in the sharp kernel",
     "return N * (2 / Tm ** 2) * 2 * v * I_abs(Tm, Om / 2)", "return N * (3 / Tm ** 2) * 2 * v * I_abs(Tm, Om / 2)"),
    ("z04", "loosened bound: 3.66e-14 -> 3.66e-2 m/s^2 (the killing factor 1e12 disappears)",
     'BOUND = mp.mpf("3.66e-14")', 'BOUND = mp.mpf("3.66e-2")'),
]
rows = []
tmp = tempfile.mkdtemp(prefix="mut_", dir=HERE)
try:
    for i, (sc, desc, old, new) in enumerate(MUTANTS):
        fn = [f for f in os.listdir(HERE) if f.startswith(sc + "_") and f.endswith(".py")][0]
        src = open(os.path.join(HERE, fn)).read()
        assert old in src, f"mutation anchor not found in {fn}: {old[:50]}"
        out = os.path.join(tmp, f"mut{i}_{fn}")
        open(out, "w").write(src.replace(old, new, 1))
        r = subprocess.run([sys.executable, out], capture_output=True, text=True, timeout=300)
        tot = [l for l in r.stdout.splitlines() if l.startswith("== TOTAL")]
        rows.append((fn, desc, r.returncode != 0, tot[-1] if tot else (r.stderr.strip().splitlines() or ["crashed"])[-1][:100]))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
caught = 0
for fn, desc, failed, tail in rows:
    print(f"  [{'caught' if failed else 'MISSED'}] {fn:36s} {desc}\n           -> {tail}")
    caught += failed
print(f"\n== MUTANTS: {caught}/{len(rows)} caught (each broken script exits non-zero) ==")
sys.exit(0 if caught == len(rows) else 1)
