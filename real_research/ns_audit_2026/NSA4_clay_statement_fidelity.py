#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA4 -- IS THE PRIZE QUESTION ALREADY ANSWERED?  Statement fidelity of the OpenAI Navier-Stokes breakdown theorem
against Fefferman's official Clay text, checked by the Lean kernel on this machine.

WHY THIS DOOR
  The Clay problem asks "for a proof of one of the following four statements" (A)-(D) (Fefferman, official problem
  description, p.2).  N08/N14 record an OpenAI Lean construction of (C)/(D) (forced breakdown), rebuilt here with clean
  axioms, and name ONE open verification item: statement drift.  If the proved theorem says what (C) says, the
  LETTER of the prize problem is met in the breakdown direction; whether that resolves the prize is the Clay
  Institute's decision (amended 2026-09-22: see the verdict's status note).

THE CHAIN, LINK BY LINK
  F0 BUILD INPUTS.  The clone and every lake package (Mathlib included) are clean at the manifest revisions, so the
     definitions the statement uses are the published ones.
  F1 FEFFERMAN -> CHALLENGE TEXT.  The Comparator challenge (ComparatorChallenges/NavierStokes.lean, adapted from
     google-deepmind/formal-conjectures @ 8bf45ed) is mapped clause by clause onto Fefferman's (1)-(7) and (C);
     every clause is checked to be present in the challenge source.  Reading: faithful for (C); (D) follows the Clay
     errata (periodic pressure).
  F2 CHALLENGE TEXT -> SUBMITTED DEFINITIONS.  The submission elaborates against its own copy
     (NavierStokes/ComparatorDefinitions.lean), not the challenge file.  The two are compared after stripping
     comments: the only difference allowed is the two `sorry` challenge theorems.
  F3 KERNEL BRIDGE.  A verbatim copy of the challenge file (namespace renamed, the two `sorry` bodies replaced) is
     generated, imports the submission, and PROVES the challenge statements (C) and (D) from the submitted
     theorems.  Compiled with `lake env lean`; `#print axioms` must show exactly propext, Classical.choice,
     Quot.sound (no sorryAx).  This is the job Comparator does (its landrun sandbox is Linux-only; unavailable here).
  F4 NON-VACUITY.  In the same file: (a) `∞` is C^infinity, not analyticity (`∞ ≠ ω`); (b) the zero field solves
     the R^3 class (f = 0), so the class is not empty by a junk encoding; (c) v = t c, f = c solves the base class,
     so the time-derivative term is live.
  F5 UPSTREAM (documentary).  The DeepMind file at the pinned commit was read through WebFetch and carries the same
     structures and theorem statements; recorded as a transcription, not a byte comparison.
  MUTATE=1 drops `globally_bounded_energy` from the challenge copy (a LARGER solution class, so a STRONGER
  nonexistence claim): the bridge must fail to compile and F3 must FAIL (rc = 1).

WHAT THIS DOES NOT CHECK
  The informal paper, the Lean kernel's own soundness, Mathlib's definitions beyond F4, and the Clay prize rules
  (refereed publication + two years).  The OpenAI clone is untracked; the runner records its commit.

Run from the repository root:  python3 real_research/ns_audit_2026/NSA4_clay_statement_fidelity.py
"""
import os, re, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLONE = os.path.join(ROOT, "deepseek_push", "navier_stokes_attempt", "openai_NS_lean")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "NSA4_clay_statement_fidelity"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA4", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


def strip_comments(src):
    src = re.sub(r"/-.*?-/", "", src, flags=re.S)
    src = re.sub(r"--[^\n]*", "", src)
    return [ln.rstrip() for ln in src.splitlines() if ln.strip()]


if not os.path.isdir(CLONE):
    P(f"OpenAI clone not found at {CLONE}; clone github.com/openai/NavierStokesAndEuler there and `lake build`.")
    sys.exit(2)
commit = subprocess.run(["git", "-C", CLONE, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "-C", CLONE, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
OUT["numbers"]["clone"] = {"commit": commit, "clean": dirty == ""}
P(f"OpenAI clone commit {commit}  (working tree {'clean' if not dirty else 'MODIFIED'})")

# ============================================================================================ F0
banner("F0  THE BUILD INPUTS: CLONE AND EVERY LAKE PACKAGE (MATHLIB INCLUDED) CLEAN AT THE PINNED REVISION")
manifest = json.load(open(os.path.join(CLONE, "lake-manifest.json")))
pk_rows = {}
for pk in manifest["packages"]:
    d = os.path.join(CLONE, ".lake", "packages", pk["name"])
    head = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    pdirty = subprocess.run(["git", "-C", d, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    pk_rows[pk["name"]] = {"pinned": pk.get("rev"), "head": head, "clean": pdirty == ""}
    P(f"    {pk['name']:18s} pinned {pk.get('rev', '')[:12]}  head {head[:12]}  {'clean' if not pdirty else 'MODIFIED'}")
OUT["numbers"]["F0"] = pk_rows
check("F0 the clone and every package are clean at the manifest revisions: Mathlib's definitions (ContDiffOn, "
      "laplacian, gradient, integral) are the published ones", f"clone {commit[:12]} clean={not dirty}; "
      f"{sum(r['clean'] and r['head'] == r['pinned'] for r in pk_rows.values())}/{len(pk_rows)} packages match",
      not dirty and all(r["clean"] and r["head"] == r["pinned"] for r in pk_rows.values()),
      "a modified Mathlib could change a statement's meaning without touching #print axioms; it is not modified")

CHAL = open(os.path.join(CLONE, "ComparatorChallenges", "NavierStokes.lean")).read()
DEFS = open(os.path.join(CLONE, "NavierStokes", "ComparatorDefinitions.lean")).read()

# ============================================================================================ F1
banner("F1  FEFFERMAN'S OFFICIAL TEXT -> THE CHALLENGE STATEMENT, CLAUSE BY CLAUSE")
CLAUSES = [
    ("(1) d_t u + (u.grad)u = nu Lap u - grad p + f, x in R^n, t >= 0",
     "derivWithin (v x ·) (Set.Ici 0) t + fderiv ℝ (v · t) x (v x t) =\n      nu • Δ (v · t) x - gradient (p · t) x + f x t",
     "faithful: one-sided time derivative at t = 0, (u.grad)u = Du[u]"),
    ("(2) div u = 0 for t >= 0", "div_free : ∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0", "faithful"),
    ("(3) u(x,0) = u0(x)", "initial_condition : ∀ x, v x 0 = u₀ x", "faithful"),
    ("u0 smooth, divergence-free", "smooth : ContDiff ℝ ∞ u₀", "faithful (∞ = C^inf, F4a)"),
    ("(4) |d^a u0| <= C_aK (1+|x|)^-K", "‖iteratedFDeriv ℝ m u₀ x‖ ≤ C / (1 + ‖x‖) ^ K",
     "equivalent: full m-th derivative norm bounds every order-m partial and conversely up to constants"),
    ("f smooth on R^3 x [0,inf)", "smooth : ContDiffOn ℝ ∞ (↿f) (Set.univ ×ˢ Set.Ici 0)", "faithful"),
    ("(5) |d^a_x d^m_t f| <= C (1+|x|+t)^-K", "C / (1 + ‖x‖ + t) ^ K", "equivalent (mixed partials inside the full derivative)"),
    ("(6) p, u in C^inf(R^n x [0,inf))", "velocity_smooth : ContDiffOn ℝ ∞ (↿v) (Set.univ ×ˢ Set.Ici 0)",
     "faithful; pressure_smooth likewise; no extra decay imposed on p (none in Fefferman either)"),
    ("(7) int |u(x,t)|^2 dx < C for all t >= 0", "globally_bounded_energy : ∃ E, ∀ t ≥ 0, (∫ x : ℝ^n, ‖v x t‖ ^ 2) < E",
     "faithful; the added `integrable : MemLp 2` field only blocks Lean's junk value 0 for non-integrable functions "
     "and is implied by (7) for continuous u"),
    ("(C) take nu > 0, n = 3; exist u0 (4), f (5) with NO solution of (1)(2)(3)(6)(7)",
     "theorem navier_stokes_breakdown_R3 (nu : ℝ) (hnu : nu > 0) :",
     "faithful and quantified over every nu > 0"),
    ("(D) periodic u0, f (8),(9); no solution of (1)(2)(3)(10)(11)",
     "isOnePeriodic_pressure : ∀ t ≥ 0, IsOnePeriodic (p · t)",
     "follows the Clay errata (pressure periodic too); the original (10)-(11) text omits it"),
]
missing = [c for c, lean, _ in CLAUSES if lean not in CHAL]
for c, lean, verdict in CLAUSES:
    P(f"    {c:74s} -> {'present' if lean in CHAL else 'MISSING'}; {verdict}")
OUT["numbers"]["F1"] = [{"fefferman": c, "lean": lean, "verdict": v} for c, lean, v in CLAUSES]
check("F1 every clause of Fefferman's (C) (and (D) per the errata) appears in the challenge statement with the "
      "reading given", f"{len(CLAUSES) - len(missing)}/{len(CLAUSES)} clauses present; missing {missing}", not missing,
      "no statement drift found between the official text and the Lean challenge")

# ============================================================================================ F2
banner("F2  CHALLENGE FILE vs THE SUBMISSION'S OWN DEFINITIONS COPY")
a, b = strip_comments(CHAL), strip_comments(DEFS)
import difflib
diff = [d for d in difflib.unified_diff(a, b, lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("+++", "---")]
removed = [d[1:].strip() for d in diff if d.startswith("-")]
added = [d[1:].strip() for d in diff if d.startswith("+")]
only_sorry_theorems = (not added) and all(
    ln.startswith(("theorem navier_stokes_breakdown", "∃ (u₀", "InitialVelocityCondition", "¬ (∃ v p",
                   "sorry", "/")) or ln == "" for ln in removed)
P(f"    comment-stripped diff: {len(removed)} lines only in the challenge, {len(added)} only in the definitions copy")
for ln in removed:
    P(f"      - {ln}")
OUT["numbers"]["F2"] = {"removed": removed, "added": added}
check("F2 the submission's definitions are the challenge definitions verbatim; the only difference is the two "
      "`sorry` challenge theorems", f"{len(removed)} challenge-only lines (the theorems), {len(added)} added",
      only_sorry_theorems and len(removed) > 0, "the proof elaborates against the same text the challenge states")

# ============================================================================================ F3 + F4
banner("F3/F4  THE KERNEL BRIDGE: PROVE THE CHALLENGE STATEMENTS FROM THE SUBMITTED THEOREMS")
src = CHAL
assert src.count("import Mathlib") == 1 and src.count("namespace NavierStokes.Comparator") == 1
src = src.replace("import Mathlib", "import NavierStokes.ComparatorSolution")
src = src.replace("namespace NavierStokes.Comparator", "namespace NSA4Challenge")
src = src.replace("end NavierStokes.Comparator", "")
BR_R3 = """by
  obtain ⟨u₀, f, hu, hf, hno⟩ := NavierStokes.Comparator.navier_stokes_breakdown_R3 nu hnu
  refine ⟨u₀, f, ⟨⟨hu.div_free, hu.smooth⟩, hu.decay⟩, ⟨⟨hf.smooth⟩, hf.decay⟩, ?_⟩
  rintro ⟨v, p, h⟩
  exact hno ⟨v, p, ⟨⟨h.navier_stokes, h.div_free, h.initial_condition, h.velocity_smooth,
    h.pressure_smooth⟩, h.integrable, h.globally_bounded_energy⟩⟩"""
BR_PER = """by
  obtain ⟨u₀, f, hu, hf, hno⟩ := NavierStokes.Comparator.navier_stokes_breakdown_periodic nu hnu
  refine ⟨u₀, f, ⟨⟨hu.div_free, hu.smooth⟩, hu.isOnePeriodic⟩, ⟨⟨hf.smooth⟩, hf.isOnePeriodic, hf.decay⟩, ?_⟩
  rintro ⟨v, p, h⟩
  exact hno ⟨v, p, ⟨⟨h.navier_stokes, h.div_free, h.initial_condition, h.velocity_smooth,
    h.pressure_smooth⟩, h.isOnePeriodic_velocity, h.isOnePeriodic_pressure⟩⟩"""
parts = src.split("by\n  sorry")
assert len(parts) == 3, "expected exactly two sorry bodies"
src = parts[0] + BR_R3 + parts[1] + BR_PER + parts[2]
if MUTATE:
    src, k = re.subn(r"  /-- The kinetic energy.*?-/\n  globally_bounded_energy : [^\n]*\n", "", src, flags=re.S)
    assert k == 1
SANITY = r"""
/-! ## F4 non-vacuity checks (NSA4) -/

/-- `∞` in these statements is C^∞ smoothness (`(⊤ : ℕ∞)`), not analyticity `ω`. -/
theorem nsa4_infty_is_smooth : (∞ : WithTop ℕ∞) = ((⊤ : ℕ∞) : WithTop ℕ∞) ∧ (∞ : WithTop ℕ∞) ≠ ω :=
  ⟨rfl, WithTop.coe_ne_top⟩

/-- The zero field solves the ℝ³ class with zero force: the class is not empty by a junk encoding. -/
theorem nsa4_zero_solution_R3 (nu : ℝ) :
    NavierStokesExistenceAndSmoothnessRn (n := 3) nu 0 0 (fun _ _ => 0) (fun _ _ => 0) := by
  refine ⟨⟨?_, ?_, ?_, ?_, ?_⟩, ?_, ?_⟩
  · intro x t _
    simp [gradient_fun_const]
  · intro x t _
    simp [divergence]
  · intro x
    rfl
  · exact contDiffOn_const
  · exact contDiffOn_const
  · intro t _
    simp
  · exact ⟨1, fun t _ => by simp⟩

/-- v = t • c with f = c solves the base class: the time-derivative term is live. -/
theorem nsa4_linear_in_time (nu : ℝ) (c : EuclideanSpace ℝ (Fin 3)) :
    NavierStokesExistenceAndSmoothness nu (fun _ => 0) (fun _ _ => c) (fun _ t => t • c) (fun _ _ => 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro x t ht
    have hd : derivWithin (fun s : ℝ => s • c) (Set.Ici 0) t = c := by
      have h := ((hasDerivAt_id t).smul_const c).hasDerivWithinAt (s := Set.Ici 0)
      simpa using h.derivWithin ((uniqueDiffOn_Ici 0) t ht)
    simp [hd, gradient_fun_const]
  · intro x t _
    simp [divergence]
  · intro x
    simp
  · exact (contDiff_snd.smul contDiff_const).contDiffOn
  · exact contDiffOn_const

end NSA4Challenge

#print axioms NSA4Challenge.navier_stokes_breakdown_R3
#print axioms NSA4Challenge.navier_stokes_breakdown_periodic
#print axioms NSA4Challenge.nsa4_zero_solution_R3
#print axioms NSA4Challenge.nsa4_linear_in_time
#print axioms NSA4Challenge.nsa4_infty_is_smooth
"""
src = src.rstrip() + "\n" + SANITY
lean_name = f"{SLUG}{'_MUTATE' if MUTATE else ''}.lean"
lean_path = os.path.join(HERE, lean_name)
open(lean_path, "w").write(src)
res = subprocess.run(["lake", "env", "lean", lean_path], cwd=CLONE, capture_output=True, text=True, timeout=1800)
out = (res.stdout + res.stderr).strip().replace(ROOT + os.sep, "")        # no machine paths in the record
P(f"    lake env lean {lean_name}: exit {res.returncode}")
for ln in out.splitlines()[:40]:
    P(f"      {ln}")
ax = dict(re.findall(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]", out))
std = {"propext", "Classical.choice", "Quot.sound"}
axsets = {k: set(x.strip() for x in v.split(",")) for k, v in ax.items()}
for k in re.findall(r"'([\w.]+)' does not depend on any axioms", out):
    axsets[k] = set()
OUT["numbers"]["F3"] = {"lean_file": lean_name, "exit": res.returncode, "axioms": {k: sorted(v) for k, v in axsets.items()},
                        "output_head": out.splitlines()[:40]}
br = ["NSA4Challenge.navier_stokes_breakdown_R3", "NSA4Challenge.navier_stokes_breakdown_periodic"]
check("F3 the Lean kernel derives the challenge statements (C) and (D), verbatim, from the submitted theorems; axioms "
      "exactly {propext, Classical.choice, Quot.sound}",
      f"exit {res.returncode}; " + "; ".join(f"{k.split('.')[-1]}: {sorted(axsets.get(k, []))}" for k in br),
      res.returncode == 0 and all(axsets.get(k) == std for k in br),
      "the theorem proved IS the challenge statement: no drift between what was proved and what was asked")
san = ["NSA4Challenge.nsa4_zero_solution_R3", "NSA4Challenge.nsa4_linear_in_time", "NSA4Challenge.nsa4_infty_is_smooth"]
check("F4 non-vacuity: ∞ is C^inf (≠ ω); the zero field solves the R^3 class; v = t c, f = c solves the base class",
      "; ".join(f"{k.split('.')[-1]}: {'ok' if k in axsets and 'sorryAx' not in axsets[k] else 'missing'}" for k in san),
      res.returncode == 0 and all(k in axsets and "sorryAx" not in axsets[k] for k in san),
      "the solution class is inhabited and its time derivative is live: nonexistence is not a vacuous encoding")

# ============================================================================================ F5
banner("F5  UPSTREAM DEEPMIND STATEMENT (documentary)")
P("    google-deepmind/formal-conjectures @ 8bf45ed FormalConjectures/Millenium/NavierStokes.lean, read via WebFetch on\n"
  "    2026-09-22: same eight structures, same fields, same (C)/(D) statements (namespace NavierStokes, tagged\n"
  "    `@[category research open, AMS 35]`); the challenge's edits are imports, namespace and inlined notation.")
check("F5 the challenge matches the upstream Formal Conjectures statement (transcribed, not byte-compared)",
      "WebFetch transcription 2026-09-22", True, "recorded as documentary", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
if MUTATE:
    P("  MUTATE: energy clause removed from the challenge copy (a stronger statement than was proved): the bridge "
      + ("FAILED to compile, as required -- the check detects drift." if n_fail else "COMPILED -- the check is blind (bad)."))
elif n_fail:
    P("  At least one load-bearing link failed; no conclusion about the prize question is drawn from this run.")
else:
    P("""  On this machine the Lean kernel proves Fefferman's (C) and (D), as encoded by DeepMind's Formal Conjectures and
  checked here clause by clause against the official text, from the OpenAI construction -- no statement drift at
  any link, by a construction that uses no framework input.  What remains outside this check: the kernel's and
  Mathlib's soundness.
  STATUS (amended 2026-09-22 from public reporting): the Clay Institute has NOT ruled -- it still lists the problem
  as unsolved and calls its evaluation 'deliberately unhurried'; OpenAI says it will not claim the prize;
  mathematicians quoted publicly do not dispute correctness but regard the forced alternative as not the main
  question.  So: the letter of (C) is proved; whether that resolves the prize is pending with the Clay Institute;
  the unforced problem (A)/(B) is open either way.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
