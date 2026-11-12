# FINAL-20 (KAPPA_AUDIT) -- audit of the kappa-derivation lanes FINAL-16 .. FINAL-19

Date: 2026-11-11. Auditing lane. **Nothing committed by this lane** (the parent commits).
Nothing pre-existing was deleted or modified; this folder is the only thing created.
Footings are never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.
**kappa = 1/2 stays FITTED unless a lane outputs it.**

---

## 0. Method (what was actually done, in order)

1. Located each lane at its committed path under
   `/Users/carlzimmerman/new_physics/zimmerman-formula/closure_2026_11_11/`.
2. Recompiled each lane's Lean file **at its exact committed path** with the verified recipe
   (`cd fable_independent_2026/lean_2026 && env LEAN_PATH="$(...)" lean /abs/path/File.lean`).
   **No compile output was piped through `head`, `tail`, `grep` or any exclusion filter** —
   stdout+stderr was redirected whole to a file and the whole file was read (`run_compiles.sh`).
3. Read **every `#print axioms` line verbatim** and compared against
   `{propext, Classical.choice, Quot.sound}`.
4. Grepped the proof **terms** for `sorry` with the required pattern
   `(^|[^`])sorry([^`]|$)` (grep -E). Also grepped emitted terms for `sorryAx`.
5. Judged each lane on the three failure modes this repo keeps hitting:
   **(C) circularity** -- does the lane assume `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2`,
   in order to derive it? **(F) footing dependence** -- does the derived kappa depend on which
   footing was used, and is that disclosed rather than hidden? **(P) post hoc** -- was any gate
   retrofitted after the outcome was seen?

Evidence files in this folder: `run_compiles.sh`, `compiles_console.log`,
`compile_FINAL16.out`, `compile_ax_FINAL16_wc.out`, `compile_ax_FINAL16_head.out`,
`probe_ax_FINAL16_wc.lean`, `probe_ax_FINAL16_head.lean`, `HEAD_FINAL16.lean`.

### `md5` provenance of the FINAL-16 source

| object | md5 |
|--------|-----|
| `closure_2026_11_11/FINAL16_kappa_real/FINAL16.lean` (compiled, 23:45) | `db7a54eb96c684cef667c83f87a89a4b` |
| `git show HEAD:...FINAL16.lean` (HEAD = `e29d1c1d83`, re-fetched 23:58) | `db7a54eb96c684cef667c83f87a89a4b` |
| `probe_ax_FINAL16_wc.lean` minus its 4 `#print axioms` lines | identical to the HEAD blob |

So the source compiled in step (a) is **byte-identical to the currently committed blob**; the
probe differs from it only by the four added `#print axioms` directives used to expose the axiom set.

---

## 1. The audit table (one row per lane)

| lane | derived kappa | circular? | footing dependence | post hoc? | verdict |
|------|---------------|-----------|--------------------|-----------|---------|
| **FINAL-16** (KAPPA_REAL) | **none derived** (Q2 = NO). The *form* `a0 = kappa c sqrt(G rho_Lambda)` is an output (universality + conservation ⇒ epoch-independent a0; rho_Lambda is the unique epoch-independent cosmic density). kappa is a **flat direction**: the G_lam symmetry (a0,g) → (lam·a0, lam·g) is exact and kappa is its only charged quantity. Best "route" (C1, freeze-out at equality) returns 1/2 only because it *is* the footing definition. | **No.** The lane refuses the circular step: F2 is recognised as a *definition* of kappa, not a constraint; C1 is flagged verbatim as "the SAME statement" as kappa = 1/2. The decisive numbers (0.319 dex menu freedom) are computed *against* the route that would have assumed the result. | **Disclosed, not hidden.** kappa is footing-invariant **by construction**: 0.500296 (can, vs rho_Lambda) and 0.500295 (alt, vs rho_crit,0). RESULT.md says plainly that 1/2 "is the definition of a footing convention, not a datum", and prints the external value kappa_ext = 0.6414 ± 0.0107 (rand) ± 0.1283 (sys) that breaks it. Footings are reported separately everywhere; never pooled. | **No retrofit of a deciding gate.** PREREGISTER committed alone before any script existed; AMENDMENT A1 (item J7) was added *before the reported run*, and the amendment itself discloses that a first run (without J7) had already completed with J0–J5 identical. J7 touches only the conservation clause, not the decisive J2 spread test. The two reported FAILs (J2, J3) are pre-registered honest negatives, and MUTATE's MU3 is explicitly designed to punish the lazy version of that negative. | **CLEAN / HOLDS.** Lean builds at the committed path (exit 0, empty output). All 4 theorems' axiom sets = `[propext, Classical.choice, Quot.sound]`. No `sorry` in any proof term. Caveats below (§2). |
| **FINAL-17** | — | — | — | — | **NOT PRESENT.** No `FINAL17*`/`FINAL-17*` directory exists anywhere in the repo (find, maxdepth 4), no commit subject names it (`git log --grep`), and no file in the campaign folders references the id. Nothing to compile, nothing to judge. |
| **FINAL-18** (KAPPA_B / "kappa from the FOLD matching condition") | **Not computed yet -- pre-registration only.** The lane fixes the closed form `kappa_M = G M_b q(1+q) / (c sqrt(G rho_Lambda) R_fold^2)` and pre-registers the expectation `kappa_M ~ 2.4e-3`, i.e. ~2.3 dex *below* the frozen band, with `kappa_M ∝ M_b^{1/3}` (G4 miss) and epoch drift in `D(z) = log10(X_fold/q_fold)` (G5 miss). | **Guarded, and the guard is pre-registered.** The circular trap here is specific: (M) pins kappa only if its RHS is built from *different* physics than its LHS. Item **G2** exists precisely to test that, and it explicitly forbids using the wall radius `r_w = sqrt(G m/a_0)·FW` as a hidden a_0 lever (must pass with the wall scaling switched **off** *and* on). MU3 pre-registers the failure mode in the other direction (calling a falsified route "vacuous"). Sound design. | **Explicitly non-pooled:** G2/G3/G4 are all specified on both footings, and the PREREGISTER repeats the never-pool convention in its header. | **No.** PREREGISTER.md was committed alone (`4144abfc80`) before `final18_shells.py` / `final18_run.py` existed. Criteria and predicted label are both frozen pre-number. | **INCOMPLETE / UNGRADED.** No `.lean` file exists in the lane (0 found), so no compile and no `#print axioms` could be run. No RESULT.md. The production run printed 8 of 39 rows and then **crashed** (`BrokenPipeError` in `multiprocessing/queues.py`, see `FINAL18_kappa_fold/run.log`); `runs/` was still being rewritten when this audit closed. **Cannot be judged on circularity of a number that does not exist yet.** |
| **FINAL-19** | — | — | — | — | **NOT PRESENT.** Same evidence as FINAL-17: no directory, no commit, no reference anywhere. |

---

## 2. FINAL-16 -- full evidence

### 2.1 Compile at the exact committed path

```
$ cd fable_independent_2026/lean_2026
$ env LEAN_PATH="$(...)" lean /Users/carlzimmerman/new_physics/zimmerman-formula/closure_2026_11_11/FINAL16_kappa_real/FINAL16.lean
LEAN_EXIT_a=0
--- full contents of compile_FINAL16.out ---
--- end (a) ---
```

**Exit 0, zero lines of output.** `FINAL16.lean` (4 theorems: `XL_quadratic`, `XL_covariant`,
`XL_quadratic_weight`, `ratio_invariant`) compiles clean at its committed path.

### 2.2 `#print axioms` lines, verbatim

The committed file contains **no `#print axioms` directives at all** (`grep -c 'print axioms'` = 0),
and the lane's own `compile.txt` (50 bytes) records only a wall-clock timing and `exit=0`:

```

real	0m50.573s
user	0m2.295s
sys	0m5.466s
exit=0
```

So the axiom set is **not evidenced anywhere inside the lane**. I recovered it by compiling a
byte-identical copy with the four print directives inserted (source = HEAD blob, verified by md5;
the copy lives in this audit folder, the committed file was not touched). Verbatim output:

```
'XL_quadratic' depends on axioms: [propext, Classical.choice, Quot.sound]
'XL_covariant' depends on axioms: [propext, Classical.choice, Quot.sound]
'XL_quadratic_weight' depends on axioms: [propext, Classical.choice, Quot.sound]
'ratio_invariant' depends on axioms: [propext, Classical.choice, Quot.sound]
```

All four are **within `{propext, Classical.choice, Quot.sound}`** — nothing extra, and in
particular no `sorryAx`.

### 2.3 `sorry` in the proof terms

```
$ grep -nE '(^|[^`])sorry([^`]|$)' closure_2026_11_11/FINAL16_kappa_real/FINAL16.lean
exit=1                       # zero matches
```

Same for the HEAD blob. **No `sorry`, no `sorryAx`.**

### 2.4 One real defect found (and it is already fixed)

The version of `FINAL16.lean` committed in `f639380e36` **did not build**. Compiled verbatim:

```
probe_ax_FINAL16_head.lean:52:4: error: No goals to be solved
probe_ax_FINAL16_head.lean:69:2: error: No goals to be solved
'XL_quadratic' depends on axioms: [propext, Classical.choice, Quot.sound]
'XL_covariant' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'XL_quadratic_weight' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'ratio_invariant' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Two redundant `ring` calls after `field_simp` (which already closed the goals) produced two hard
errors; Lean's error recovery then axiomatised `XL_covariant` and `XL_quadratic_weight` with
`sorryAx`. **At that revision the lane had no valid Lean certificate while RESULT.md cited it.**
A sibling removed the two redundant `ring` lines and the repaired file was committed as
`e29d1c1d83`; that is the revision I compiled in §2.1, and it is clean. Recording the defect
because "the compile that was committed" and "the compile that passes" are two different events.

### 2.5 Scope limit of the certificate

`FINAL16.lean` proves the **kinematics of X**: the quadratic `g·X·(1+X) = a0` (KA-3) and the
G_lam covariance of `XL` (J1 i–iii). It does **not** encode:

- the classification "F2 is the *only* non-invariant relation of F",
- the exhaustion "rho_Lambda is the *unique* epoch-independent cosmic density",
- the epoch menu C1–C6 or the 0.3189 dex spread,
- the n = 2 / `kappa = 1/n` channel (J3).

Those are sympy + prose. Only J1 (the symmetry, in the sense of `XL`'s invariance) and KA-3 are
Lean-certified. The lane's own Lean header is honest about the narrower scope ("the two EXACT
statements the lane's no-go rests on"), so this is a scope note, not a misrepresentation.

### 2.6 Independent re-derivation (sympy, this lane)

Not taken on trust; re-ran the two exact steps:

```
quadratic g*X*(1+X) -> a0                      (exact)
covariance XL(lam*a0, lam*g) - XL(a0,g) -> 0   (exact)
rho_crit0 = 8.522730e-27, rho_L = 5.835513e-27, c*sqrt(G rho_L) = 1.870954e-10 m/s^2
  kappa[can] = 0.500296 (vs rho_L)        matches final16.out 0.500296
  kappa[alt] = 0.500295 (vs rho_crit,0)   matches final16.out 0.500295
  kappa[ext] = 0.641384 (a0 = 1.20e-10)  matches final16.out 0.641384
z(rho_m = rho_L)  = 0.294967   matches FINAL16's z_L
z(rho_m = 2rho_L) = 0.631556   matches FINAL16's C3 epoch
```

Arithmetic reproduces the committed outputs exactly.

### 2.7 The three failure modes, explicitly

**(C) Circular?** No. This is the lane's central result and it is a *negative*: it does not claim
`kappa = 1/2`. The step that would be circular -- pinning formation to a named cosmic epoch whose
density was itself chosen to reproduce a0 -- is named (C1) and convicted in the printed output
("C1 is a restatement of rho_* = rho_L, not a derivation of kappa"). The one thing the lane does
claim, the *form*, is obtained from universality (no M in a0) plus conservation (no z in a0),
neither of which mentions kappa.

**(F) Footing dependence?** Derived kappa = none, so there is no footing-dependent kappa to hide.
What the lane *does* show is stronger and it is disclosed: kappa = 1/2 comes out on **both**
footings (0.500296 / 0.500295), and the lane states why -- each footing's rho_ref is *defined*
by `rho_ref := 4 a0^2/(c^2 G)`, so the footings cannot disagree about kappa by construction.
It then breaks the tie with an external measurement (0.6414), which is the right move. Printed
per-footing everywhere; never pooled.

**(P) Post hoc?** No deciding gate was added after the fact. PREREGISTER was committed alone
pre-script; AMENDMENT A1 added J7 before the reported run **and** discloses the earlier run whose
J0–J5 were identical. J7 concerns a different clause (conservation) from the decisive item (J2's
0.3189 dex spread test). All four known answers pass. MUTATE rejects all three twins, including
MU3, which is specifically designed to catch a too-easy "it's just another flat direction"
verdict. Honest negative, not a rescued one.

---

## 3. Cross-lane read on the failure mode

- **FINAL-16** is the model of how to do this: it asks whether the coincidence is an output,
  finds that the *form* is and the *coefficient* is not, identifies the circular route as circular,
  discloses the footing construction that makes 1/2 unfalsifiable internally, and brings an
  external number to break it. This is exactly the anti-pattern the parent is worried about,
  caught rather than committed.
- **FINAL-18** pre-registers the same self-defence structure (MU3 guards against the lazy
  negative; G2 forbids smuggling a_0 in through the wall radius). Promising design, but it has
  produced **no result and no Lean**, and its production run crashed. It cannot be scored yet.
- **FINAL-17** and **FINAL-19** do not exist. Two of the four lanes in the brief have no
  artifact on disk or in history; the brief's assumption that they are running is not supported
  by anything I can see. Either they were never spawned, or they were spawned into a
  different repo/campaign folder than `closure_2026_11_11`.

**Bottom line on the kappa question itself:** nothing in FINAL-16 or FINAL-18 converts
`kappa = 1/2` from a fitted normalisation into a derived number. The register's
`kappa = 1/2 FITTED; not theory closed` stands.

---

## 4. Files written by this lane

All under `hy4_preview_push/FINAL-20_kappa_audit/`:

- `AUDIT.md` -- this document.
- `run_compiles.sh` -- the compile driver (each compile separately captured, no filtering).
- `compiles_console.log` -- full console transcript of the three compiles.
- `compile_FINAL16.out` -- full output of `lean` on the committed path (empty; exit 0).
- `probe_ax_FINAL16_wc.lean` -- committed source + `#print axioms` (source verified identical to HEAD).
- `compile_ax_FINAL16_wc.out` -- the four axiom lines.
- `HEAD_FINAL16.lean` -- the HEAD blob, for provenance.
- `probe_ax_FINAL16_head.lean` -- earlier revision + `#print axioms`.
- `compile_ax_FINAL16_head.out` -- the two build errors and the two `sorryAx` theorems of that revision.
