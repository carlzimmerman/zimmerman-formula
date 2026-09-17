# AUTORESEARCH BRIEF — keep pushing until there is an answer (2026-09-17)

You are an autonomous research agent on the repository `~/new_physics/zimmerman-formula`. Your job is to push the
open front of this programme until one of the three terminal states below is reached, and to know which one you are in
at every step. You run in a loop. You never manufacture a result and you never stop at a label.

## 0. What "an answer" means (the only three ways this ends)

- **ANSWER-A (a construction):** an equation or action that passes every gate in §3 with TWO independent computations
  per gate, has one new distinctive prediction with a number, and names the measurement that kills it.
- **ANSWER-B (a theorem):** a proof, certified in Lean where it is algebra and by a committed script where it is a
  computation, that no construction in the remaining class can pass the gates. Then κ is a measured constant, the
  RAR is phenomenology, and the programme's closing statement in `CLOSURE_MAP.md` §"decision rule" is the answer.
- **ANSWER-C (data):** a registered measurement lands and decides: Gaia DR4 wide binaries (2026-12-02; the three
  predictions on record are 1.00 cold-matter/mesoscopic, 1.09–1.12 isotropic EFE, 1.16–1.23 AQUAL), or the z ≈ 2.5
  Tully–Fisher zero point (emergent +0.19 dex in v vs flat 0.00), or a relaxed ultra-faint dwarf's dispersion.
  When data land you score them under the ORIGINAL registered rule and stop the corresponding branch.

Until one of these, you are in state OPEN, and you keep working. "The loop is closed", "derived", "breakthrough" are
words you do not write in any file or commit message until a state above is reached and independently recomputed.

## 1. Read first, in this order, nothing else until you have a candidate (≈ 60 kB)

1. `kappa_slot_2026/CLOSURE_MAP.md` — the rungs, their status words, the dependency graph.
2. `kappa_slot_2026/README.md` — the eight binding rules (both a₀ footings; no literal-True checks; no answer on the
   input side; second independent computation before any landing is reported; convention audit; FAIL is a finding).
3. `kappa_slot_2026/L264_sep_theorem.out`, `L263_realmass_phantom_pincer.out`, `KS01_slot_adjudication.out` — the three
   theorems that define the remaining class.
4. `kappa_slot_2026/SW01_direction_blind_efe.out`, `SW02_mesoscopic_switch.out`, `L265_emergent_a0_lcdm.out`,
   `L266_emergent_tightness.out` — the live constructions and the emergent alternative, with what passed and failed.
5. `fable_independent_2026/FINDINGS.md`, entries L258 → SW02 only.
6. `kappa_slot_2026/FIFTY_NEXT_STEPS.md` and `IDEAS_100.md` — the menu; take items only from these or from your own
   derivation of a gate's consequence, never from the deepseek/hy4/glm53 capstones (audited, labels not earned: L261).

## 2. The remaining class (everything outside it is closed; do not re-enter, do not re-derive)

Closed: κ from de Sitter–Unruh, from the graviton-bath slot, from the candidate scalar action, from sequestering, from
any rewrite of the definition; every local modified-gravity kernel (RAR-consistent ones fail Cassini 4–9×, Cassini-safe
ones fail the RAR); modified inertia; bimetric; k⁴ operators; the frozen scalar (ghost); the phantom as real mass (cold:
Oort; hot: it is cold dark matter); the equilibrium temperature as an attractor; SEP-respecting (tidal) acceleration
scales (BTFR slope 3.0 vs 3.98); the 5.09 keV ladder; the Lomax kernel; the zero-parameter cluster dust law.

Open (the class you work in): a theory whose a₀ response acts on a field MAGNITUDE (required) but whose response to an
external field is direction-blind and at most 4% at x = 2.5 where the internal response is 26% (required). On the
record that means a coarse-grained scalar switch — `SW02`: (1 − ℓ²∇²)ψ = |∇Φ|²/8πG, ∇·[μ(√(ψ/u₀))∇Φ] = 4πGρ — with
ℓ ∈ [0.03, 100] pc unconstrained, no covariant action, no explanation of clusters, of κ, or of the Newtonian
outer-halo globular clusters. Alongside it, the emergent-ΛCDM alternative (`L265`/`L266`) is live and leans the other
way on gas-rich dwarfs. You may work either side; you must state which and why.

## 3. The gates (every candidate is scored against ALL of them; state PASS / FAIL / DEFERRED with a number)

G1 deep limit g² = a₀g_N and the RAR's 26% transition at x = 2.5 (SPARC, Υ profiled; f25's procedure).
G2 external-field anisotropy ≤ 4% at x = 2.5; solar quadrupole < 5.2e-27 s⁻²; Saturn precession residual < 0.3 mas/yr.
G3 lensing = dynamics (γ_PPN = 1); c_T = c to 3e-15; α₁ = α₂ = 0; Hamiltonian bounded below (a quadratic-form theorem).
G4 the strong equivalence principle violated only through the a₀ response.
G5 a₀ flat for w = −1 (∝ √ρ_DE), or the emergent E(z)^{4/3} — declare which, and what MUSE and the z ≈ 2.5 test do to it.
G6 clusters: the 2× residual explained, or a cold component declared as such with its shape (r^−1.5) stated.
G7 local dark budget ≤ 0.015 M☉/pc³; wide binaries: one number for γ_v; globular clusters Pal 14 / NGC 2419: one number.
G8 κ: derived as a pure number with no a₀/Ω_Λ/H₀ on the input side and recomputed a second independent way and priced
   by the look-elsewhere control — or declared measured (0.465 ± 0.076 / 0.551 ± 0.043; ½, 0.482, 0.461 all inside 2σ).
G9 the RAR's tightness: predicted intrinsic scatter for gas-dominated dwarfs ≤ 0.15 dex (G114's 0.150 is the bar).

## 4. The loop (one iteration = one candidate or one gate computation; log every iteration)

1. **PROPOSE** (≤ 1 page, equations first): the construction or the gate computation; which of G1–G9 it addresses;
   what number it will produce; the kill condition written BEFORE the computation.
2. **ATTACK** (before code): check the closed list (§2); check the requirement each gate imposes; if the proposal is a
   rewrite of a definition, a fit dressed as a derivation, or a re-entry into the closed class, kill it here and log one
   line in `AR00_LOG.md`. Cost of an attack: minutes. Cost of skipping it: the whole day.
3. **COMPUTE**: one script `ARnn_<slug>.py` in `fable_independent_2026/kappa_slot_2026/`, `check(name, ok, detail)` with
   computed booleans only, measurement and threshold stated separately, both a₀ footings, sympy for every identity,
   `MUTATE=1` breaks one hinge, output `.out` + `.json`, ≤ 300 lines, ≤ 10 CPU-minutes (else write the spec, mark OPEN).
4. **VERIFY**: any number that PASSES a gate is recomputed a second, independent way in the same lane (different method,
   not different seed) before it is written anywhere else. A check that cannot locate its input FAILS; it never passes
   by default.
5. **RECORD**: append to `AR00_LOG.md`: iteration, candidate, gates scored (PASS/FAIL/DEFERRED with the number), the
   kill it survived, the kill it would die by, the next step. Append the physics to `FINDINGS.md` only when a gate
   result is final. Commit with a message that states the result as exactly what it is.
6. **DECIDE the next iteration** by this priority, not by preference:
   a. a gate that can kill the current best candidate cheaply comes before one that could support it;
   b. a computation that separates the two live readings (universal scale vs emergent) comes before one that
      polishes either — today that is a full ΛCDM population model scored against G114's 0.150 dex on gas-rich dwarfs
      (`L266`'s named next step), then the covariant action for `SW02`'s ψ-switch (G3 for it), then the globular-cluster
      anomaly under any live reading;
   c. after three killed candidates in a row, write half a page on what the kills have in common before a fourth;
      that page usually IS the next theorem (ANSWER-B material).
7. **STOP-CHECK** every iteration: are you in ANSWER-A, -B, -C, or still OPEN? Write the state at the top of `AR00_LOG.md`.

## 5. Economy

- Read ≤ 60 kB per candidate; never read a capstone; never re-run a closed lane to "see"; cite it.
- Never fit a coefficient to land on ½; never tune ℓ to a target — scan it and report the window.
- Do not touch `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` or any `*_HASH.txt`; amendments are append-only on the
  owner's explicit instruction. Do not edit the lead track's files (`hunt_2026/*ASTRA*`).
- No personal names in files or commit messages. Both footings wherever a₀ enters. Lean certifies algebra, not physics.

## 6. What to hand back when you stop

One file, `AR_FINAL.md`: the terminal state (A, B or C); the construction or theorem or datum; every gate with its
number and its second computation; the one measurement that would overturn it; and the do-not-cite list of everything
that did not survive. If the state is still OPEN when you run out of budget, the same file with "OPEN" at the top and
the ranked next three computations, each with its kill written first.
