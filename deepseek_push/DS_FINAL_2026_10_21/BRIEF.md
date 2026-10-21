# DS_FINAL_2026_10_21 — shared brief for all lanes

Repo: `/Users/carlzimmerman/new_physics/zimmerman-formula`. New work goes ONLY in
`deepseek_push/DS_FINAL_2026_10_21/<your lane>/`. Do not edit files outside your lane.
Do not commit. Do not delete anything.

## 0. What this push is

Two prior four-lane rounds (`core_open_problems_2026_10_20/`,
`core_open_problems_round2_2026_10_20/`) attacked the four physical-origin
questions and returned **incomplete**, each with scoped conditional results.
This push does not repeat their model-building. It either (a) closes a question
with a derivation that survives an adversarial check, or (b) returns a sharp
no-go with the exact missing premise named, or (c) converts the question into a
pre-registered numerical discriminator that decides it. **A negative result with
the obstruction proven is a full-credit deliverable. Restating a known result is
not.**

## 1. The theory as it stands (canonical, do not re-derive)

Units: c = 1 unless stated; signature (-+++); K = 8πG.

- Vacuum-tied scale: `a0 = κ c √(G ρ_Λ)`, κ = 1/2 canonical.
  Equivalent: `a0 = c²√(Λ/32π) = c H_Λ / Z`, `Z = 2√(8π/3) = 5.78881`.
  So `a0/(cH_Λ) = 1/Z = 0.172746`, and `2Z = 11.5776` — *this* is the
  "1/12 of the horizon" number. It is not an independent coincidence: it is
  `2Z`, i.e. κ = 1/2 restated with the Einstein 8π/3 bookkeeping. Any claim to
  "derive the twelfth" must therefore derive the integer `n = 1/κ = 2`, and
  must not smuggle 8π/3 in as if it were derived.
- Footings (never pool): canonical `a0 = 9.36e-11 m/s²`; alt `1.13e-10 m/s²`.
- Galactic law, frozen S2 rest state (PAPER57, AG4 branch a):
  `g_N = g²/(g + a0)`  ⇔  `g = (g_N/2)(1 + √(1 + 4a0/g_N))`, deep limit
  `g → √(a0 g_N)`. Here `g` is the observed (total) acceleration and `g_N` the
  baryonic one. **This is the canonical law.**
- The n = 2 "a₀-line" half-capacity variant: `g² − g_N² = a0 g_N`, i.e.
  `g = √(g_N² + a0 g_N)`. Same deep limit, different interpolation, capacity
  `a0/2` vs `a0`. n = 1 and n = 2 are **different effective theories**.
- Ontology: there is no dark-matter particle. The extra gravitating mass is the
  stress-energy `T^φ_μν` of the scalar/cold-energy sector ("cold energy"),
  collisionless, with `div P = ρ − ρ̄` in the covariant parent.
- The one strong-field problem on the record: the quadrature kernel has a slow
  tail `ν − 1 ~ 1/(2y)` giving a constant `a0/2` anomaly in the Solar System,
  1279× the Earth–Mars ephemeris bound. The accepted cure is a turn-off
  `ν_fix = 1 + (√(1+1/y) − 1)/(1 + (y/y_t)²)`, `y_t ≈ 94–129`, i.e. a turn-off
  near `1e-8 m/s²`; the vacuum term then closes as `Λ/a0² ≈ (π/4) y_t`.
  (Zenodo 23171085, 23251231.) Whether the *canonical* law needs the same cure
  is an open question for lane C2.

## 2. Closed doors — do NOT re-run

κ: sonnet55 puzzle_32pi (~50 lanes), opus_48 kappa_audit, KS01 channel-count,
Oppenheim–Russo, nodal-fermion medium (CFG900), gauged-carrier Festina Lente
(CFG905), unimodular AS (CFG906), NCG spectral action (CFG907), the four
"κ derived" claims (CFG908: Q010 = different quantity, G031 = identity,
glm53/G002 = relabelled measurement, gemini38 = premise insertion).
Medium: diffusive Markov chain (rounds 1–2), dielectric/Born–Infeld/two-level
and simple lattice models (round 1), the band-integral quartic (round 2).
Relativity: the round-2 ADM scalar/tensor reduction and oblique principal
symbol are already verified — reuse them, do not redo them.
Stiffness: finite-range exchange, contact-fluid pressure, quantum-pressure
mechanisms (round 1); affine isotropic solid (round 2: λ = −μ forced, negative
bulk modulus).

## 3. Output contract (every lane, without exception)

In your lane directory:

1. `report.md` — ≤ 250 lines. Sections: **Claim** (one paragraph, exact),
   **Derivation** (numbered equations, every symbol defined), **Status**
   (`DERIVED` / `CONDITIONAL(premise)` / `NO-GO(obstruction)` / `NUMERICAL`),
   **Checks** (what the script proves), **What this does not do**, **Next**.
2. `<lane>_checks.py` — prints one line per check:
   `K1 PASS <measured> <threshold>` or `K1 FAIL ...`, and ends with
   `"<LANE> COMPLETE: N/M checks PASS."`, exit code 0 iff all declared checks
   pass. Deterministic, no network, ≤ 120 s runtime, stdlib + numpy/scipy/sympy.
3. `<lane>.out` — the captured stdout of the script exactly as run.
4. `<lane>_results.json` — `{"lane":..., "status":..., "checks":[{"id","pass","value","threshold"}], "numbers":{...}, "constants_used":[...]}`.
5. `MUTATE.md` + a `--mutate` flag in the script: at least one mutation that
   **must** break a check (proves the check has teeth). Record the mutated
   output in `MUTATE.md`.

Rules: every number in `report.md` must appear in `results.json` or be a
labelled external input with its source. No fitted constant may be introduced
silently; list every constant you used and where it came from. If you used an
assumption, it goes in `CONDITIONAL(...)`. Keep derivations exact (sympy) where
possible; numerical only where exactness is impossible, and then state the
convergence.

## 4. Constants (SI, exact values to use)

c = 2.99792458e8 m/s; G = 6.67430e-11; H0 = 67.4 km/s/Mpc = 2.1843e-18 s^-1;
Λ = 1.0890e-52 m^-2; ρ_Λ = Λc²/(8πG) = 5.831e-27 kg/m³;
a0_can = 9.36e-11 m/s²; a0_alt = 1.13e-10 m/s²; Mpc = 3.0856775814913673e22 m;
1 pc = 3.0856775814913673e16 m; κ_can = 0.5.

## 5. What "completion" means for this push

The four questions must each end in one of exactly three states, and the state
must be earned by the script:

- **CLOSED-DERIVED** — a derivation from premises already in the theory, with
  the premise list explicit and no new fitted number.
- **CLOSED-NO-GO** — a proof that no construction of the stated class can do
  it, with the obstruction identified (so the question becomes "is premise X
  true?", not "can we find a model?").
- **DECIDABLE** — a pre-registered numerical test on data already on disk that
  separates the surviving alternatives at a stated significance, with the
  computed Δχ² or forecast N.

Anything else is `OPEN` and must say exactly which single premise is missing.
