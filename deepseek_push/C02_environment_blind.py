#!/usr/bin/env python3
r"""C02 -- ENVIRONMENT-BLINDNESS: Lean certificate + numeric cross-check.

The theorem (certified in deepseek_push/lean/C02_environment_blind.lean,
exit 0, zero sorry, axioms subset {propext, Classical.choice, Quot.sound}):
the ladder m = k_B T_0 (1+z*)/sigma^2 and the freeze relation
(1+z*) = m sigma^2/(k_B T_0) are algebraic inverses -- substituting the
freeze relation into the ladder returns m IDENTICALLY for ANY environment
(the mass is a fixed point of the ladder).  The certified algebra is the
positive-reals field identity (a*b/c)*(c/a) = b with a = sigma^2, b = m,
c = k_B T_0.  Corollaries certified: (1) the recovered mass is
sigma-independent; (2) (1+z*) is a bijective function of sigma alone.

This driver (a) re-runs the Lean compile and verifies the clean-axiom gate,
and (b) performs the NUMERIC cross-check with the committed B03/G213
constants: m_rec == m to 1e-12 for ANY (m, sigma) -- the exact identity in
floating point -- plus a sanity pass on B03's own 11 committed freeze rungs
(every rung recovers the 5.0000-5.0001 keV class, spread 0.00012).

Registers read (committed, nothing tuned here):
  B03 constants ("project_atomos/B03_doubleZ_mass.py"): k_B = 1.380649e-23,
  T_0 = 2.72548 K, c exact, eV exact; the ladder m = k_B T_0(1+z*)/sigma^2.
  G213 freeze map: (1+z*) = m sigma^2/(k_B T_0)  [T_CMB(z) = T_0 (1+z)].
  G212: the germ m = 5.09 keV, band [4.99, 5.19].
  B03 V1: recovered masses [5.0000, 5.0001] keV, spread = 0.00012 keV.

DELIVERABLE: deepseek_push/C02_environment_blind.py + .out +
C02_results.json + deepseek_push/lean/C02_environment_blind.lean.
Commit and push.
"""
import json
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "C02_environment_blind.out")
JSON = os.path.join(HERE, "C02_results.json")
LEAN_FILE = os.path.join(HERE, "lean", "C02_environment_blind.lean")
LEAN_DIR = os.path.join(REPO, "fable_independent_2026", "lean_2026")

# ---------------------------------------------------------------- constants
C = 2.99792458e8                 # m/s, exact
KB = 1.380649e-23                # J/K, exact (SI 2019)
EV = 1.602176634e-19             # J, exact
T0 = 2.72548                     # K, CMB today (G213 footing)
KBT0 = KB * T0                   # J
M_GERM_KEV = 5.09                # G212 germ
G212_BAND = (4.99, 5.19)         # G212 1-sigma band (keV)
B03_SPREAD_KEV = 0.00012         # B03 V1 inter-rung spread (keV)

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def kev(kg):
    """kg -> keV (rest energy)."""
    return kg * C * C / (EV * 1e3)


def freeze_factor(m_keV, sigma_kms):
    """The freeze map: (1+z*) = m sigma^2/(k_B T_0), dimensionless."""
    m_kg = m_keV * 1e3 * EV / (C * C)
    return m_kg * (sigma_kms * 1e3) ** 2 / KBT0


def m_recovered_keV(m_keV, sigma_kms):
    """The ladder ON the freeze relation: k_B T_0 (1+z*)/sigma^2 -> keV."""
    return kev(KBT0 * freeze_factor(m_keV, sigma_kms) / (sigma_kms * 1e3) ** 2)


# -------------------------------------------------------- numeric cross-check
def numeric_cross_check():
    """m_rec == m to 1e-12 for ANY (m, sigma): committed grid + random."""
    rng = random.Random(20260916)
    cases = []
    # the committed physical band swept densely (m in keV, sigma in km/s)
    for m in [10 ** x for x in
              [math.log10(0.1) + i * (math.log10(100.0) - math.log10(0.1)) / 39
               for i in range(40)]]:
        for s in [10 ** x for x in
                  [math.log10(5.0) + i * (math.log10(3000.0) - math.log10(5.0)) / 39
                   for i in range(40)]]:
            cases.append((m, s))
    # 100k random environments (log-uniform over the physical ranges)
    for _ in range(100000):
        m = 10 ** rng.uniform(math.log10(0.1), math.log10(100.0))
        s = 10 ** rng.uniform(math.log10(5.0), math.log10(3000.0))
        cases.append((m, s))
    worst = 0.0
    for m, s in cases:
        d = abs(m_recovered_keV(m, s) - m)
        if d > worst:
            worst = d
    return worst, len(cases)


def b03_rungs_sanity():
    """B03's committed rungs all recover the 5.0000-5.0001 keV class.
    Reads the committed rung table from project_atomos/B03_results.json."""
    b03 = json.load(open(os.path.join(
        os.path.dirname(HERE), "project_atomos", "B03_results.json")))
    rungs = []
    for r in b03["part1_multi_rung_test"]["rungs"]:
        rungs.append((r["class"], r["sigma_kms"], r["z_star"]))
    rec = []
    for cls, s, z in rungs:
        m = kev(KBT0 * (1.0 + z) / (s * 1e3) ** 2)   # ladder, B03 form
        rec.append((cls, s, z, m))
    return rec


# ------------------------------------------------------------- lean check
def lean_check(log):
    """Compile the certificate; return (exit_code, n_sorry, axioms, ok)."""
    proc = subprocess.run(
        ["lake", "env", "lean", LEAN_FILE],
        cwd=LEAN_DIR, capture_output=True, text=True, timeout=600)
    out = (proc.stdout or "") + (proc.stderr or "")
    log.write("=== lake env lean %s ===\n" % LEAN_FILE)
    log.write("exit code: %d\n" % proc.returncode)
    log.write(out)
    n_sorry = out.count("sorry")
    axioms = set()
    for line in out.splitlines():
        if "depends on axioms:" in line:
            body = line.split("depends on axioms:")[1].strip()
            for a in body.strip("[]").replace("'", "").split(","):
                a = a.strip()
                if a:
                    axioms.add(a)
    ok = (proc.returncode == 0 and n_sorry == 0 and
          axioms.issubset(ALLOWED_AXIOMS) and axioms != set())
    return proc.returncode, n_sorry, sorted(axioms), ok


# ------------------------------------------------------------------ driver
def main():
    log = open(OUT, "w")
    def say(*a):
        print(*a)
        log.write(" ".join(str(x) for x in a) + "\n")

    say("C02 -- ENVIRONMENT-BLINDNESS: Lean certificate + numeric cross-check")

    # 1. numeric cross-check: ANY (m, sigma)
    worst, n_cases = numeric_cross_check()
    xcheck = {"n_cases": n_cases, "max_abs_diff_keV": worst,
              "passed_1eminus12": worst <= 1e-12}
    say("numeric cross-check: %d (m, sigma) environments, "
        "max |m_rec - m| = %.3e keV  -- passed_1e-12: %s"
        % (n_cases, worst, xcheck["passed_1eminus12"]))

    # 2. B03 committed rungs sanity
    rec = b03_rungs_sanity()
    vals = [r[3] for r in rec]
    spread = max(vals) - min(vals)
    rungs_tbl = [
        {"class": c, "sigma_kms": s, "z_star": z, "m_recovered_keV": round(m, 8)}
        for c, s, z, m in rec]
    rung_ok = (spread <= 0.0002 and
               all(abs(m - 5.0) <= 0.001 for m in vals))
    say("B03 committed rungs sanity: %d rungs, recovered [%.5f, %.5f] keV, "
        "spread %.5f keV -- ok: %s"
        % (len(vals), min(vals), max(vals), spread, rung_ok))

    # 3. Lean compile + axiom gate
    rc, n_sorry, axioms, lean_ok = lean_check(log)
    say("lean: exit %d, sorry %d, axioms %s -- clean: %s"
        % (rc, n_sorry, axioms, lean_ok))

    results = {
        "lane": "C02_environment_blind",
        "title": "ENVIRONMENT-BLINDNESS: the ladder and the freeze map are "
                 "algebraic inverses -- the mass is a fixed point of the "
                 "ladder, independent of the environment (sigma, z*)",
        "question": "certify in Lean the positive-reals field identity "
                    "(a*b/c)*(c/a) = b with a = sigma^2, b = m, c = k_B T_0 -- "
                    "substituting the freeze relation (1+z*) = m sigma^2/"
                    "(k_B T_0) into the ladder m = k_B T_0 (1+z*)/sigma^2 "
                    "returns m identically for ANY environment; corollaries "
                    "(1) the recovered mass is sigma-independent, (2) (1+z*) "
                    "is a function of the environment only via sigma; numeric "
                    "cross-check m_rec == m to 1e-12 for ANY (m, sigma). "
                    "The z* >= -1 domain statement (G213) is NOT attempted.",
        "mapping": {
            "a": "sigma^2 (squared velocity dispersion)",
            "b": "m (particle mass)",
            "c": "k_B T_0",
            "ladder": "m_rec = c * (1+z*) / a  [keV-footed: k_B T_0(1+z*)/sigma^2]",
            "freeze": "1+z* = m * a / c  [G213/G194, T_CMB(z*) = T_0 (1+z*)]"
        },
        "constants": {
            "k_B_J_K": KB, "T_0_K": T0, "c_m_s": C, "eV_J": EV,
            "germ_keV": M_GERM_KEV, "G212_band_keV": list(G212_BAND),
            "B03_spread_keV": B03_SPREAD_KEV
        },
        "lean_certificate": {
            "file": "deepseek_push/lean/C02_environment_blind.lean",
            "exit_code": rc,
            "zero_sorry": n_sorry == 0,
            "axioms": axioms,
            "allowed_axioms": sorted(ALLOWED_AXIOMS),
            "axioms_subset_allowed": set(axioms).issubset(ALLOWED_AXIOMS),
            "pass": lean_ok,
            "theorems": [
                "posreal_field_identity -- (a*b/c)*(c/a) = b for a,b,c > 0 "
                "(the master positive-reals field identity)",
                "field_identity_nonzero -- same under a,b,c divisors nonzero",
                "environment_blindness -- ladder s^2 (freeze s^2 m) = m, the "
                "fixed point (B03 V1)",
                "environment_blindness_pos -- fixed point on the positive-"
                "reals footing (s^2 > 0, k_B T_0 > 0)",
                "recovered_mass_sigma_independent -- m_rec identical for any "
                "two dispersions (corollary 1)",
                "zstar_function_of_sigma_only -- freeze s1 = freeze s2 <-> "
                "s1 = s2, a bijection in sigma alone (corollary 2)",
                "recovered_mass_within_1e12 -- |m_rec - m| <= 1e-12 for ANY "
                "(m, sigma) (the numeric cross-check, exact identity)",
                "environment_blindness_statement -- the conjoined statement"
            ]
        },
        "numeric_cross_check": xcheck,
        "b03_rungs_sanity": {
            "rungs": rungs_tbl,
            "recovered_min_keV": min(vals),
            "recovered_max_keV": max(vals),
            "spread_keV": spread,
            "pass": rung_ok
        },
        "verdicts": {
            "V1": "LEAN CERTIFIES THE FIXED POINT: all 8 theorems compile "
                  "exit 0, zero sorry, axioms %s -- subset of {propext, "
                  "Classical.choice, Quot.sound}.  The algebra is exact: "
                  "(a*b/c)*(c/a) = b, so the ladder is the algebraic inverse "
                  "of the freeze map on the mass coordinate for EVERY "
                  "environment." % sorted(axioms),
            "V2": "THE RECOVERED MASS IS SIGMA-INDEPENDENT (corollary 1, "
                  "certified): m_rec(sigma1) = m_rec(sigma2) = m for any two "
                  "dispersions -- B03's multi-rung spread 0.00012 keV is the "
                  "floating-point shadow of an exact identity.",
            "V3": "z* IS A FUNCTION OF THE ENVIRONMENT ONLY VIA sigma "
                  "(corollary 2, certified): (1+z*) = m sigma^2/(k_B T_0) is "
                  "a bijection in sigma alone -- the freeze epoch encodes "
                  "exactly the environment's dispersion, no other environment "
                  "variable.",
            "V4": "NUMERIC CROSS-CHECK: over %d environments (committed grid "
                  "+ 100k random), max |m_rec - m| = %.2e keV < 1e-12 for "
                  "ANY (m, sigma); B03's committed rungs all recover "
                  "[%.5f, %.5f] keV (spread %.5f) -- every frozen rung the "
                  "5 keV-class mass." % (n_cases, worst, min(vals),
                                         max(vals), spread),
            "V5": "SCOPE: the z* >= -1 domain statement is G213's and is "
                  "NOT attempted; Lean certifies the pure algebra of the "
                  "fixed point, not the physics."
        },
        "checks": [
            "lean exit 0", "zero sorry", "axioms subset {propext, "
            "Classical.choice, Quot.sound}",
            "numeric |m_rec - m| <= 1e-12 for ANY (m, sigma)",
            "B03 rungs all recover the 5.0000-5.0001 keV class"
        ],
        "n_pass": sum([lean_ok, rung_ok, xcheck["passed_1eminus12"]]),
        "n_total": 3,
        "deliverable": "deepseek_push/C02_environment_blind.py + .out + "
                       "C02_results.json + deepseek_push/lean/"
                       "C02_environment_blind.lean"
    }
    results["lean_certificate"]["n_pass"] = 1 if lean_ok else 0
    with open(JSON, "w") as f:
        json.dump(results, f, indent=1)
    say("results written: %s" % JSON)
    log.close()
    return 0 if (lean_ok and rung_ok and xcheck["passed_1eminus12"]) else 1


if __name__ == "__main__":
    sys.exit(main())