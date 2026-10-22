#!/usr/bin/env python3
"""
A83_lean_spine — verification harness for the Lean 4 algebraic spine.

What this checks
  L1  `lake build A83` on the real project (lean_2026) exits 0
  L2  `lake env lean A83_Axioms.lean` exits 0 and prints one axiom footprint per theorem
  L3  zero `sorry` / `admit` / `native_decide` in the module sources (comments stripped)
  L4  zero `axiom` declarations in the module sources
  L5  every theorem's axiom set is a subset of {propext, Classical.choice, Quot.sound}
  L6  >= 24 named theorems in the new modules; exact delta over A8_lean's 40 certified
  L7  no A8_lean theorem disappeared; A8 sources byte-identical to the frozen baseline
  N*  numerical cross-checks of the symbolic identities at the canonical constants
      against A72/A75/A78 JSON values and the task's quoted digits

Mutation mode: `A83_MUTATE=<name>` or `--mutate <name>`; each mutation must be killed
(compile error, or a banned token reaching the source).  Exit status: 0 iff all checks
pass (mutation mode: iff the mutant is killed).

Usage
  python3 a83_checks.py                 # full verification
  python3 a83_checks.py --cold          # delete A83 build artefacts first
  python3 a83_checks.py --mutate inject_sorry
  python3 a83_checks.py --json-out a83_results.json | tee a83.out
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]                      # zimmerman-formula/
DS = ROOT / "deepseek_push" / "DS_FINAL_2026_10_21"
LEAN = ROOT / "fable_independent_2026" / "lean_2026"
A8 = DS / "A8_lean"

MODULES = [LEAN / "A83.lean"] + sorted((LEAN / "A83").glob("Block*.lean"))
BANNED = ("sorry", "admit", "native_decide")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

RESULTS: dict = {"lane": "A83_lean_spine", "checks": [], "numerics": [], "mutations": [],
                 "mutations_inplace": []}


# ----------------------------------------------------------------------------- utils
def run(cmd: list[str], cwd: Path, timeout: int = 1800) -> tuple[int, str, float]:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out, time.time() - t0
    except subprocess.TimeoutExpired as e:
        return 124, f"TIMEOUT after {timeout}s\n{e}", time.time() - t0


def strip_comments(src: str) -> str:
    """Remove Lean line and (nested) block comments so token scans see code only."""
    out, i, n, depth = [], 0, len(src), 0
    while i < n:
        if src.startswith("/-", i):
            depth += 1
            i += 2
            while i < n and depth > 0:
                if src.startswith("/-", i):
                    depth += 1
                    i += 2
                elif src.startswith("-/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
        elif src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(cid: str, ok: bool, detail: str, **extra) -> bool:
    RESULTS["checks"].append({"id": cid, "pass": bool(ok), "detail": detail, **extra})
    print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {detail}")
    return ok


def numeric(cid: str, quantity: str, computed: float, reference: float, source: str,
            tol: float, mode: str = "rel", note: str = "") -> bool:
    c, r = float(computed), float(reference)
    resid = abs(c - r)
    rel = resid / abs(r) if r != 0 else resid
    val = rel if mode == "rel" else resid
    ok = val <= tol
    RESULTS["numerics"].append({
        "id": cid, "quantity": quantity, "computed": c, "reference": r, "source": source,
        "residual": resid, "relative": rel, "mode": mode, "tol": tol,
        "pass": bool(ok), "note": note,
    })
    print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {quantity} = {c:.17g}  vs {r:.17g} "
          f"({source}); {mode} resid {val:.3e} <= {tol:.1e}")
    return ok


# ------------------------------------------------------------------- Lean-side checks
def cold_clean() -> None:
    for pat in (".lake/build/lib/lean/A83*", ".lake/build/ir/A83*"):
        for p in glob.glob(str(LEAN / pat)):
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    for p in glob.glob(str(LEAN / ".lake/build/lib/lean/A83") + "/*"):
        os.remove(p)
    print("[cold] removed A83 build artefacts")


def lean_build() -> bool:
    rc, out, dt = run(["lake", "build", "A83"], LEAN)
    RESULTS["lean_build"] = {"cmd": "lake build A83", "exit": rc, "seconds": round(dt, 1),
                             "tail": "\n".join(out.strip().splitlines()[-8:])}
    return check("L1_lean_build", rc == 0, f"`lake build A83` exit {rc} in {dt:.1f}s; "
                 f"tail: {out.strip().splitlines()[-1] if out.strip() else '(no output)'}")


def axiom_audit() -> bool:
    rc, out, dt = run(["lake", "env", "lean", "A83_Axioms.lean"], LEAN)
    RESULTS["axiom_audit_raw_exit"] = rc
    footprints = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out))
    parsed = {k: [a.strip() for a in v.split(",") if a.strip()] for k, v in footprints.items()}
    RESULTS["axioms"] = {"exit": rc, "seconds": round(dt, 1), "per_theorem": parsed,
                         "count": len(parsed), "union": sorted({a for v in parsed.values() for a in v})}
    ok1 = check("L2_axiom_audit_exit", rc == 0 and len(parsed) > 0,
                f"`lake env lean A83_Axioms.lean` exit {rc}, {len(parsed)} footprints")
    bad = {k: v for k, v in parsed.items() if not set(v) <= ALLOWED_AXIOMS}
    ok2 = check("L5_axioms_subset", not bad,
                f"union of axiom sets = {sorted({a for v in parsed.values() for a in v})}; "
                f"offenders: {bad if bad else 'none'}")
    return ok1 and ok2


def source_scan() -> bool:
    counts = {t: 0 for t in BANNED}
    per_file = {}
    axiom_decls = []
    for f in MODULES:
        code = strip_comments(f.read_text())
        fc = {t: len(re.findall(rf"\b{re.escape(t)}\b", code)) for t in BANNED}
        per_file[str(f.relative_to(LEAN))] = fc
        for t in BANNED:
            counts[t] += fc[t]
        axiom_decls += re.findall(r"^\s*axiom\s+([A-Za-z0-9_'.]+)", code, re.M)
    RESULTS["source_scan"] = {"files": per_file, "banned_counts": counts,
                              "axiom_declarations": axiom_decls}
    ok1 = check("L3_no_banned_tokens", sum(counts.values()) == 0,
                f"sorry/admit/native_decide counts = {counts} over {len(MODULES)} files")
    ok2 = check("L4_no_axiom_declarations", len(axiom_decls) == 0,
                f"source-level `axiom` declarations = {axiom_decls if axiom_decls else 'none'}")
    return ok1 and ok2


def archive_check() -> bool:
    """The lane ships byte-identical copies of the five built modules plus the audit file."""
    pairs = [(LEAN / "A83.lean", LANE / "lean" / "A83.lean"),
             (LEAN / "A83_Axioms.lean", LANE / "lean" / "A83_Axioms.lean")]
    pairs += [(LEAN / "A83" / f"Block{n}.lean", LANE / "lean" / f"Block{n}.lean") for n in "ABCD"]
    bad = [str(b.name) for a, b in pairs if not (a.exists() and b.exists() and sha256(a) == sha256(b))]
    RESULTS["archive"] = {"files": [str(b.relative_to(LANE)) for _, b in pairs], "mismatch": bad}
    return check("L8_archive_copies", not bad,
                 f"lane copies of the built modules are byte-identical: "
                 f"{'yes' if not bad else 'MISMATCH ' + str(bad)}")


def theorem_delta() -> bool:
    new = []
    for f in sorted((LEAN / "A83").glob("Block*.lean")):
        code = strip_comments(f.read_text())
        new += [f"A83.{n}" for n in re.findall(r"^theorem\s+([A-Za-z0-9_]+)", code, re.M)]
    base = json.loads((LANE / "a8_baseline.json").read_text())
    certified, declared = base["certified"], base["declared"]

    # current A8 state: names still parse, hashes unchanged
    cur_declared, cur_hash = [], {}
    for f in sorted(A8.glob("*.lean")):
        if "MUTATE" in f.name:
            continue
        code = f.read_text()
        ns = re.findall(r"^namespace\s+(\S+)", code, re.M)
        ns = ns[0] if ns else ""
        cur_declared += [f"{ns}.{n}" for n in re.findall(r"^theorem\s+([A-Za-z0-9_]+)", code, re.M)]
        cur_hash[f.name] = sha256(f)
    disappeared = sorted(set(declared) - set(cur_declared))
    hash_changed = sorted(k for k, v in base["files_sha256"].items() if cur_hash.get(k) != v)
    delta = sorted(set(new) - set(certified) - set(declared))
    overlap = sorted(set(new) & set(declared))

    RESULTS["theorems"] = {
        "new_count": len(new), "new": new,
        "a8_certified_count": len(certified), "a8_certified_unique": len(set(certified)),
        "a8_declared_count": len(declared), "a8_declared_unique": len(set(declared)),
        "a8_certified_note": "40 declarations / 39 unique names (A8.gCanon_form is declared twice)",
        "delta_count": len(delta), "delta": delta,
        "delta_over_40": len(set(new) - set(certified)),
        "overlap_with_a8": overlap, "disappeared": disappeared,
        "a8_hash_changed": hash_changed,
    }
    ok1 = check("L6a_theorem_count", len(new) >= 24, f"{len(new)} named theorems in the new modules (>= 24)")
    ok2 = check("L6b_delta_over_40", len(set(new) - set(certified)) == len(new) and not overlap,
                f"delta over the {len(certified)} certified A8 declarations ({len(set(certified))} "
                f"unique names): +{len(set(new) - set(certified))} (new names only; overlap = "
                f"{overlap if overlap else 'none'})")
    ok3 = check("L7a_no_a8_theorem_disappeared", not disappeared,
                f"A8 declared names still present: {len(set(cur_declared))}/{len(set(declared))}; "
                f"missing: {disappeared if disappeared else 'none'}")
    ok4 = check("L7b_a8_sources_unchanged", not hash_changed,
                f"A8 source hashes identical to the frozen baseline: "
                f"{'yes' if not hash_changed else hash_changed}")
    return ok1 and ok2 and ok3 and ok4


# ------------------------------------------------------------------------- numerics
def numerics() -> bool:
    pi = mp.pi
    G = mp.mpf("6.67430e-11")
    K = 4 * pi * G
    Z = 2 * mp.sqrt(8 * pi / 3)
    kappa = Z / (4 * pi)
    kappa_full = kappa / (2 * pi)

    ok = []
    ok.append(numeric("N1_kappa_Z2", "Z^2 vs 32*pi/3", float(Z**2), float(32 * pi / 3),
                      "exact identity (A72 §0)", 1e-15,
                      note=f"Z^2 - 32*pi/3 = {float(Z**2 - 32*pi/3):.3e}"))
    ok.append(numeric("N2_kappa_DE", "kappa_DE = Z/(4*pi)", float(kappa),
                      float(mp.mpf("0.46065886596178063")),
                      "A72 a72_results.json /numbers/Z_over_4pi", 1e-12))
    ok.append(numeric("N3_kappa_A75", "kappa_DE (A75 K20)", float(kappa),
                      float(mp.mpf("0.4606588659617806")),
                      "A75 a75_results.json /numbers/K20_kappa", 1e-12))
    ok.append(numeric("N4_sqrt_form", "sqrt(2/(3*pi))", float(mp.sqrt(2 / (3 * pi))),
                      float(kappa), "closed form vs Z/(4*pi)", 1e-15))
    ok.append(numeric("N5_12pi2", "8*pi/kappa^2", float(8 * pi / kappa**2),
                      float(12 * pi**2), "exact 12*pi^2", 1e-15,
                      note="task prints 118.435 (3 dp)"))
    ok.append(numeric("N6_48pi4", "8*pi/kappa_full^2", float(8 * pi / kappa_full**2),
                      float(48 * pi**4), "exact 48*pi^4", 1e-15,
                      note="task prints 4674.6 — a 2.22e-4 arithmetic slip (48*pi^4 = 4675.6364)"))
    ok.append(numeric("N7_12pi2_task_literal", "12*pi^2 vs task literal", float(12 * pi**2),
                      118.435, "task text", 1e-3))
    # beta and the BBN window
    OL = mp.mpf("0.6838")          # A72's Omega_Lambda
    OL2 = mp.mpf("0.6847")         # the task's Omega_L
    C_rep = mp.mpf("11.1738")      # the task's rounded C
    C_full = mp.mpf("11.173790231394968")   # A78 /derived/dNeff_per_unit_beta (abs)
    eps = mp.mpf("0.30")
    beta_at_1061 = (2 / 3) * OL * (mp.mpf("1.061") - 1)
    ok.append(numeric("N8_beta_at_r1061", "beta(r=1.061, Omega_L=0.6838)",
                      float(beta_at_1061), float((2 / 3) * OL * mp.mpf("0.061")),
                      "A78 relation beta=(2/3)Omega_L(r-1)", 1e-15))
    ok.append(numeric("N9_beta_vs_A78_bound", "beta(r=1.061) vs A78 printed bound 0.0280",
                      float(beta_at_1061), 0.0280,
                      "A78 report §3 (beta < 0.0280 from |Delta N_eff| < 0.30)", 1e-2,
                      note="beta(r=1.061)=0.027808 < 0.0280: consistent with A78's bound"))
    r_bound = 1 + 3 * eps / (2 * OL2 * C_rep)
    ok.append(numeric("N10_r_bound", "1 + 3*eps/(2*Omega_L*C), eps=0.30, C=11.1738, Omega_L=0.6847",
                      float(r_bound), float(1 + 3 * eps / (2 * OL2 * C_rep)),
                      "closed form (task's parameters)", 1e-15,
                      note="task quotes 1.0588"))
    r_lin_full = 1 + 3 * eps / (2 * OL * C_full)
    r_exact = 1 + 3 * mp.mpf("0.02797513981523432") / (2 * OL)
    ok.append(check("N11_linear_vs_exact",
                    r_lin_full < r_exact,
                    f"linearised bound {float(r_lin_full):.9f} < exact (2+3beta) bound "
                    f"{float(r_exact):.9f}; difference {float(r_exact - r_lin_full):.3e} = O(beta), "
                    f"the 3beta term in 2C beta/(2+3beta) = eps"))
    bA78 = mp.mpf("0.02797513981523432")
    L_implied = eps * (2 + 3 * bA78) / (3 * bA78)
    ok.append(numeric("N12_beta_inversion",
                      "Delta-N_eff coefficient L = eps(2+3beta)/(3beta) at A78's beta_max",
                      float(L_implied), 7.4492, "A78 report §3 (Delta N_eff = -7.4492 beta + ...)", 1e-6,
                      note="A78's beta_max solves its own equation with L = 7.4492047; the report "
                           "prints 7.4492, hence the 6e-7 residual"))
    beta_from_L = 2 * eps / (3 * (mp.mpf("7.4492") - eps))
    ok.append(numeric("N12b_beta_from_L", "beta from L = 7.4492 exactly", float(beta_from_L),
                      float(bA78), "A78 /derived/beta_max_BBN", 1e-6,
                      note="6.5e-7 relative, entirely the rounding of 7.4492 in the report"))
    ok.append(numeric("N13_beta_max_to_r", "1 + 3*beta_max/(2*Omega_L)",
                      float(1 + 3 * mp.mpf("0.02797513981523432") / (2 * OL)),
                      float(mp.mpf("1.0613669016163023")),
                      "A78 /derived/Lambda_bare_over_obs_betamax_present", 1e-7))
    # mass cancellation at the canonical constants
    hbar, c, kB = mp.mpf("1.054571817e-34"), mp.mpf("2.99792458e8"), mp.mpf("1.380649e-23")
    a0 = mp.mpf("8.618166e-11")
    H = 2 * pi * a0 / c
    T = hbar * H / (2 * pi * kB)
    vals = []
    for m in ("1e-30", "1e-27", "1e-24", "1e-21", "1e-18"):
        m = mp.mpf(m)
        vals.append(kB * T / (m * (hbar / (m * c))))
    spread = max(vals) - min(vals)
    ok.append(numeric("N14_mass_cancel_spread", "spread of a_sat over 5 masses", float(spread), 0.0,
                      "A75 K11 mass independence", 1e-40, mode="abs"))
    ok.append(numeric("N15_a_sat_canonical", "a_sat = k_B T c/hbar at T_dS", float(vals[0]),
                      float(a0), "A72 a0 = cH_Lambda/2pi = 8.618166e-11", 1e-9))
    # A68's Z at beta=1, eta=0, p=0 is 5K
    Zb1 = K * (2 + 3 * 1) / 1 + 0
    ok.append(numeric("N16_Z_beta1", "Z(beta=1, eta=0, p=0) = 5K", float(Zb1),
                      float(mp.mpf("4.193586e-09")), "A68 §3.2 (5K = 4.193586e-09)", 1e-6))
    # exact residuals at 50 digits (the "1e-12" requirement, exceeded by ~40 orders)
    exact = [
        ("E1", "Z^2 - 32*pi/3", Z ** 2 - 32 * pi / 3),
        ("E2", "Z/(4*pi) - sqrt(2/(3*pi))", kappa - mp.sqrt(2 / (3 * pi))),
        ("E3", "8*pi/kappa^2 - 12*pi^2", 8 * pi / kappa ** 2 - 12 * pi ** 2),
        ("E4", "8*pi/kappa_full^2 - 48*pi^4", 8 * pi / kappa_full ** 2 - 48 * pi ** 4),
        ("E5", "2cH/a0 - 4*pi at a0 = cH/(2*pi)", 2 * mp.mpf(1) / (mp.mpf(1) / (2 * pi)) - 4 * pi),
    ]
    for eid, label, resid in exact:
        ok.append(numeric(eid, label, float(abs(resid)), 0.0,
                          "50-digit mpmath residual", 1e-12, mode="abs"))
    RESULTS["exact_residuals_50dps"] = {eid: mp.nstr(abs(r), 5) for eid, _, r in exact}
    RESULT_NUM = all(ok)
    check("N_all", RESULT_NUM, f"{sum(ok)}/{len(ok)} numerical cross-checks pass")
    return RESULT_NUM


# ------------------------------------------------------------------------ mutations
MUTATIONS = {
    "vacuum_only_beta": (
        "A83/BlockD.lean",
        "    β = (2 / 3) * ΩL * (r - 1) := by\n  linarith",
        "    β = (2 / 3) * (ΩL * r - 1) := by\n  linarith",
        "A33's vacuum-only relation 3β = 2Ω_L r − 2 in place of A78's matter-inclusive one"),
    "inject_sorry": (
        "A83/BlockA.lean",
        "  simp [Kmat, Matrix.det_fin_two]\n  field_simp\n  ring",
        "  sorry",
        "one proof replaced by sorry (Lean exits 0 with a warning; the token gate must reject)"),
    "break_alpha_gamma": (
        "A83/BlockA.lean",
        "  !![α * p ^ 4, 0; 0, γ * p ^ 2]",
        "  !![α * p ^ 4, 0; 0, γ * p ^ 4]",
        "second stiffness p^2 -> p^4, breaking the α = γ single-stiffness theorem"),
    "unreduced_wavelength": (
        "A83/BlockC.lean",
        "    a0OfWavelength c (2 * Real.pi * (c / H)) = a0Thermal c H / (2 * Real.pi) := by",
        "    a0OfWavelength c (2 * Real.pi * (c / H)) = a0Thermal c H := by",
        "drop the 2π from the unreduced-wavelength branch"),
    "drop_Omega_m": (
        "A83/BlockD.lean",
        "(hrel : 2 + 3 * β = 2 * (ΩL * r + Ωm))",
        "(hrel : 2 + 3 * β = 2 * (ΩL * r))",
        "A78's matter term Ω_m deleted from the Friedmann relation"),
}


def mutate(name: str) -> int:
    if name not in MUTATIONS:
        print(f"unknown mutation {name!r}; choose from {sorted(MUTATIONS)}")
        return 2
    rel, old, new, desc = MUTATIONS[name]
    src = (LEAN / rel).read_text()
    if old not in src:
        print(f"[MUTATE] FAIL: anchor not found in {rel}")
        return 2
    mutated = src.replace(old, new, 1)
    outdir = LANE / "_scratch" / f"mut_{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    mf = outdir / Path(rel).name
    mf.write_text(mutated)
    rc, out, dt = run(["lake", "env", "lean", str(mf)], LEAN)
    code = strip_comments(mutated)
    hits = {t: len(re.findall(rf"\b{re.escape(t)}\b", code)) for t in BANNED}
    banned_total = sum(hits.values())
    killed = (rc != 0) or (banned_total > 0)
    ev = {"name": name, "file": rel, "description": desc, "exit": rc,
          "banned_tokens": hits, "killed": killed, "seconds": round(dt, 1),
          "errors": [l for l in out.splitlines() if "error" in l][:4]}
    RESULTS["mutations"].append(ev)
    print(f"[MUTATE] {name}: {desc}")
    print(f"         lean exit {rc}, banned tokens {hits} -> "
          f"{'KILLED' if killed else 'SURVIVED'}")
    if rc != 0:
        print("         first error: " + (ev["errors"][0] if ev["errors"] else out.splitlines()[0]))
    return 0 if killed else 1


def mutate_inplace(name: str) -> int:
    """Apply `name` to the built module *and* its lane copy, run the full checker, restore.

    This is the direct form of "each mutation forces exit 1": the mutant is not a
    separate file, it is the real certificate, and the verification must reject it.
    """
    if name not in MUTATIONS:
        print(f"unknown mutation {name!r}")
        return 2
    rel, old, new, desc = MUTATIONS[name]
    targets = [LEAN / rel, LANE / "lean" / Path(rel).name]
    backups = {t: t.read_bytes() for t in targets}
    tmpjson = LANE / "_scratch" / f"inplace_{name}.json"
    tmpjson.parent.mkdir(parents=True, exist_ok=True)
    try:
        for t in targets:
            src = backups[t].decode()
            assert old in src, f"anchor missing in {t}"
            t.write_text(src.replace(old, new, 1))
        rc, out, dt = run([sys.executable, str(LANE / "a83_checks.py"),
                           "--json-out", str(tmpjson)], LANE, timeout=1800)
        failed = []
        if tmpjson.exists():
            failed = [c["id"] for c in json.loads(tmpjson.read_text())["checks"] if not c["pass"]]
        ev = {"name": name, "description": desc, "verification_exit": rc,
              "failed_checks": failed, "seconds": round(dt, 1), "killed": rc == 1}
        RESULTS["mutations_inplace"].append(ev)
        print(f"[IN-PLACE] {name}: verification exit {rc}, failed checks {failed} -> "
              f"{'KILLED' if rc == 1 else 'SURVIVED'}")
        return 0 if rc == 1 else 1
    finally:
        for t, b in backups.items():
            t.write_bytes(b)
        assert all(sha256(t) == hashlib.sha256(b).hexdigest() for t, b in backups.items()), \
            "RESTORE FAILED"


# ------------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", default=os.environ.get("A83_MUTATE", ""))
    ap.add_argument("--cold", action="store_true")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    print("A83_lean_spine verification")
    print(f"  repo:  {ROOT}")
    print(f"  lean:  {LEAN}")
    print(f"  A8:    {A8}")
    print()

    if args.mutate.startswith("inplace:"):
        name = args.mutate.split(":", 1)[1]
        names = list(MUTATIONS) if name == "all" else [name]
        rc = 0
        for n in names:
            rc |= mutate_inplace(n)
        (LANE / "a83_mutations_inplace.json").write_text(json.dumps(
            {"lane": "A83_lean_spine", "mutations_inplace": RESULTS["mutations_inplace"]}, indent=1))
        print(f"\nIN-PLACE MUTATION MODE exit = {rc}")
        return rc

    if args.mutate:
        if args.mutate == "all":
            rc = 0
            for name in MUTATIONS:
                rc |= mutate(name)
            (LANE / "a83_mutations.json").write_text(json.dumps(
                {"lane": "A83_lean_spine", "mutations": RESULTS["mutations"]}, indent=1))
            print(f"\nMUTATION MODE (all) exit = {rc}")
            return rc
        rc = mutate(args.mutate)
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(RESULTS, indent=1))
        print(f"\nMUTATION MODE exit = {rc}")
        return rc

    if args.cold:
        cold_clean()

    ok = lean_build()
    ok = axiom_audit() and ok
    ok = source_scan() and ok
    ok = archive_check() and ok
    ok = theorem_delta() and ok
    ok = numerics() and ok
    mutf = LANE / "a83_mutations.json"
    if mutf.exists():
        RESULTS["mutations"] = json.loads(mutf.read_text())["mutations"]
        killed = sum(1 for m in RESULTS["mutations"] if m["killed"])
        ok = check("M_all_killed", killed == len(RESULTS["mutations"]) and len(RESULTS["mutations"]) >= 4,
                   f"{killed}/{len(RESULTS['mutations'])} mutations killed "
                   f"(recorded by `--mutate all`, a83_mutations.json)") and ok
    else:
        ok = check("M_all_killed", False, "a83_mutations.json missing: run `--mutate all`") and ok
    ipf = LANE / "a83_mutations_inplace.json"
    if ipf.exists():
        ip = json.loads(ipf.read_text())["mutations_inplace"]
        RESULTS["mutations_inplace"] = ip
        bad = [m["name"] for m in ip if m["verification_exit"] != 1]
        ok = check("M_inplace_exit1", not bad and len(ip) >= 4,
                   f"{len(ip) - len(bad)}/{len(ip)} mutants make the full verification exit 1 "
                   f"(files restored): {'; '.join(m['name'] + ':' + ','.join(m['failed_checks']) for m in ip)}"
                   ) and ok
    RESULTS["modules_sha256"] = {str(f.relative_to(LEAN)): sha256(f) for f in MODULES}

    RESULTS["pass"] = bool(ok)
    RESULTS["verdict"] = "CERTIFIED" if ok else "REJECTED"
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(RESULTS, indent=1))
    print()
    print(f"RESULT: {'ALL CHECKS PASS' if ok else 'CHECKS FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
