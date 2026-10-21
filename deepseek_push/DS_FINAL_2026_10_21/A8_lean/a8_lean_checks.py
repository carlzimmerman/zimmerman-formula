#!/usr/bin/env python3
"""A8 lane checks: the Lean certificates, their axiom footprints, and the
numeric consistency of the algebra with the constants of the BRIEF.

Run:  python3 a8_lean_checks.py            (all checks must pass, exit 0)
      python3 a8_lean_checks.py --mutate   (K5 is replaced by the FALSE
                                            "1/12 identity" claim, so it FAILs)

Every declared check prints one line:  K<n> PASS <measured> <threshold>
and the run ends with "<LANE> COMPLETE: N/M checks PASS."
Deterministic, no network, stdlib only.
"""
import math
import os
import re
import sys

LANE = "A8"
HERE = os.path.dirname(os.path.abspath(__file__))

ALLOWED = ["propext", "Classical.choice", "Quot.sound"]

# theorem -> expected file (sources of truth: the #print axioms lines)
MANIFEST = {
    "A8_C1_C2_kappa_Z": [
        "A8.a0_sq", "A8.kappa_Z_identity", "A8.kappa_half_sq",
        "A8.inv_two_sqrt_sq", "A8.a0_over_cH_eq_inv_two_sqrt",
        "A8.two_sqrt_32pi_3", "A8.inv_two_sqrt_eq_sqrt_ratio",
        "A8.inv_twoZ_bracket", "A8.inv_twoZ_ne_twelfth",
    ],
    "A8_C3_law_ordering": [
        "A8.gCanon_form", "A8.gCanon_gt_gN", "A8.gQuad_gt_gN",
        "A8.gCanon_root", "A8.gQuad_root", "A8.gCanon_root_unique",
        "A8.gCanon_sq_sub_gQuad_sq", "A8.gQuad_lt_gCanon",
        "A8.gCanon_sub_gQuad_eq", "A8.gCanon_sub_gQuad_le_gN",
        "A8.gCanon_sub_gQuad_le_a0", "A8.gQuad_normalised_tendsto",
        "A8.gCanon_normalised_tendsto", "A8.gap_tendsto_a0_zero",
    ],
    "A8_C4_monotonicity": [
        "A8.gCanon_form", "A8.deriv_gQuad", "A8.deriv_gCanon",
        "A8.deriv_gQuad_pos", "A8.deriv_gCanon_pos", "A8.gQuad_strictMonoOn",
        "A8.gCanon_strictMonoOn", "A8.gQuad_slope_pos", "A8.gCanon_slope_pos",
        "A8.gQuad_strictMonoOn_a0", "A8.gCanon_strictMonoOn_a0",
    ],
    "A8_C5_capacity": [
        "A8.mu_eq_of_canonical", "A8.boost_eq_one_add", "A8.mu_pos",
        "A8.mu_lt_one", "A8.mu_tendsto_zero", "A8.mu_tendsto_one",
    ],
}

CERT_FILES = list(MANIFEST)

# BRIEF constants (external inputs, SI)
C_LIGHT = 2.99792458e8
G_NEWTON = 6.67430e-11
LAMBDA = 1.0890e-52
A0_CAN_QUOTED = 9.36e-11
KAPPA_CAN = 0.5

RESULTS = []


def record(cid, ok, value, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok), "value": value,
                    "threshold": threshold, "note": note})
    print(f"{cid} {'PASS' if ok else 'FAIL'} {value} {threshold}"
          + (f"  # {note}" if note else ""))


def strip_comments(src):
    """Crude but sufficient: drop /- ... -/ (non-nested handled) and -- lines."""
    src = re.sub(r"/-.*?-/", "", src, flags=re.S)
    src = re.sub(r"--[^\n]*", "", src)
    return src


def parse_axioms(text):
    """'A8.foo' depends on axioms: [a, b]  ->  {foo: ['a','b']}"""
    out = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
        name, ax = m.group(1), m.group(2).strip()
        out[name] = [a.strip() for a in ax.split(",")] if ax else []
    return out


def k1_build_logs():
    clean, total = 0, len(CERT_FILES)
    detail = []
    for f in CERT_FILES:
        p = os.path.join(HERE, f + ".out")
        if not os.path.exists(p):
            detail.append(f"{f}: MISSING .out")
            continue
        txt = open(p).read()
        bad = ("error" in txt.lower()) or ("sorryAx" in txt)
        if not bad and "depends on axioms" in txt:
            clean += 1
        else:
            detail.append(f"{f}: error/sorryAx/missing axioms")
    record("K1", clean == total, f"{clean}/{total} clean build logs", f"{total}/{total}",
           "; ".join(detail))


def k2_axioms():
    ok, total = 0, sum(len(v) for v in MANIFEST.values())
    missing, wrong = [], []
    for f, thms in MANIFEST.items():
        p = os.path.join(HERE, f + ".out")
        have = parse_axioms(open(p).read()) if os.path.exists(p) else {}
        for t in thms:
            if t not in have:
                missing.append(t)
            elif sorted(have[t]) == sorted(ALLOWED):
                ok += 1
            else:
                wrong.append(f"{t}:{have[t]}")
    record("K2", ok == total, f"{ok}/{total} theorems with exactly the allowed axioms",
           f"{total}/{total}",
           ("missing=" + ",".join(missing) if missing else "")
           + (" wrong=" + ",".join(wrong) if wrong else ""))


def k3_no_sorry():
    clean = 0
    bad = []
    for f in CERT_FILES:
        src = open(os.path.join(HERE, f + ".lean")).read()
        if re.search(r"\bsorry\b", strip_comments(src)):
            bad.append(f)
        else:
            clean += 1
    record("K3", clean == len(CERT_FILES), f"{clean}/{len(CERT_FILES)} sources free of 'sorry'",
           f"{len(CERT_FILES)}/{len(CERT_FILES)}", ",".join(bad))


def k4_mutant_fails():
    p = os.path.join(HERE, "A8_C3_MUTATE.out")
    txt = open(p).read() if os.path.exists(p) else ""
    failed = ("error" in txt) and ("EXIT=1" in txt) and ("linarith failed" in txt)
    record("K4", failed, "mutant rejected" if failed else "mutant compiled (BAD)",
           "error + EXIT=1", "A8_C3_MUTATE.lean")


def geometry():
    """The exact closed forms, evaluated in double precision."""
    pi = math.pi
    Z = 2 * math.sqrt(8 * pi / 3)
    return Z


def g_canon(gN, a0):
    return gN / 2 * (1 + math.sqrt(1 + 4 * a0 / gN))


def g_quad(gN, a0):
    return math.sqrt(gN ** 2 + a0 * gN)


def k5_bracket(mutate):
    Z = geometry()
    if mutate:
        # MUTATION: assert the FALSE "one twelfth of the horizon" identity.
        val = abs(1 / (2 * Z) - 1 / 12)
        record("K5", val < 1e-3, f"|1/(2Z)-1/12|={val:.6e}", "1e-3 (MUTATED CLAIM)")
        return
    inside = (11 < 2 * Z < 12) and (1 / 12 < 1 / (2 * Z) < 1 / 11)
    gap = (1 / (2 * Z)) / (1 / 12) - 1
    ok = inside and gap > 0.01
    record("K5", ok, f"2Z={2*Z:.6f} 1/(2Z)={1/(2*Z):.9f} gap_vs_1/12={gap*100:.3f}%",
           "11<2Z<12 and gap>1%", "1/12 is NOT an identity")


def k6_constants():
    Z = geometry()
    rho = LAMBDA * C_LIGHT ** 2 / (8 * math.pi * G_NEWTON)
    a0 = KAPPA_CAN * C_LIGHT * math.sqrt(G_NEWTON * rho)
    h_lambda = C_LIGHT * math.sqrt(LAMBDA / 3)
    ratio = a0 / (C_LIGHT * h_lambda)
    rel = abs(ratio - 1 / Z) / (1 / Z)
    rel_quoted = abs(A0_CAN_QUOTED - a0) / a0
    ok = rel < 1e-9 and rel_quoted < 2e-3
    record("K6", ok, f"a0/(cH_Lam)={ratio:.12f} vs 1/Z={1/Z:.12f} rel={rel:.2e}; "
                     f"a0 formula={a0:.4e} vs quoted rel={rel_quoted:.2e}",
           "rel<1e-9 and a0 rel<2e-3",
           "H_Lam=c*sqrt(Lam/3)=%.6e" % h_lambda)


def k7_ordering():
    gN, a0 = 1.0, 1.0
    gc, gq = g_canon(gN, a0), g_quad(gN, a0)
    gap = gc - gq
    ok = (gq < gc) and (gap > 0) and (gap <= min(gN, a0))
    record("K7", ok, f"gq={gq:.9f} < gc={gc:.9f}, gap={gap:.9f}", "0<gap<=min(gN,a0)=1",
           "witness gN=a0=1")


def k8_deep_limit():
    a0 = 1.0
    worst_c = worst_q = 0.0
    for d in (1e-8, 1e-10):
        gN = d
        s = math.sqrt(a0 * gN)
        worst_c = max(worst_c, abs(g_canon(gN, a0) / s - 1))
        worst_q = max(worst_q, abs(g_quad(gN, a0) / s - 1))
    ok = worst_c < 1e-4 and worst_q < 1e-4
    record("K8", ok, f"max|gc/sqrt(a0gN)-1|={worst_c:.2e} max|gq/sqrt(a0gN)-1|={worst_q:.2e}",
           "1e-4", "delta=gN/a0 in {1e-8,1e-10}")


def main():
    mutate = "--mutate" in sys.argv
    if mutate:
        print("# MUTATED RUN: K5 asserts the false 1/12 identity")
    k1_build_logs()
    k2_axioms()
    k3_no_sorry()
    k4_mutant_fails()
    k5_bracket(mutate)
    k6_constants()
    k7_ordering()
    k8_deep_limit()
    passed = sum(1 for r in RESULTS if r["pass"])
    total = len(RESULTS)
    print(f"{LANE} COMPLETE: {passed}/{total} checks PASS.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
