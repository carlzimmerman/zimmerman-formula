# 02 — HOUSE RULES (re-read every cycle; all non-negotiable)

## R1. κ = ½ is FITTED, NOT DERIVED

`a₀ = ½·c·√(G·ρ_Λ)`. The **½ is fitted to rotation curves.** No script, paper, or comment may say or imply
otherwise. Banned phrasings: "derived from first principles", "emerges from the dark energy density",
"zero free parameters", "parameter-free", "predicted rather than fitted", "no fit".

If a calculation appears to derive it, that is the most important result in the programme — so it must clear
`06_VERIFY_PROTOCOL.md` completely before it is written down as anything stronger than "candidate".

**Count your free parameters explicitly, in the script, and print the count.** A construction that replaces
κ with a different free number has *relocated* the fit, not removed it. Say "reparametrisation, not derivation".

## R2. Credit is mandatory, in every script docstring that uses these

- `ν(y) = √(1+1/y)` and the temperature balance `I = √(a²+H²) − H` → **Milgrom 1999, Phys. Lett. A 253, 273,
  eqs. 6–9**, who fixes the coefficient at `â₀ = 2cH_Λ`.
- `a_λ = c²√(Λ/3)` → **Milgrom 1994, Ann. Phys. 229, 384, §II eq. 3**.
- the five-acceleration construction → **Deser & Levin 1997, CQG 14, L163**.
- `ν = 1/(1−e^{−√y})` → **McGaugh 2008, ApJ 683, 137, eq. 11a**.
- `κ = 1/2π` → **Milgrom 2020**.

The framework's own distinctive content is **the coefficient plus the modified-inertia completion** — nothing
more. Never present the kernel as this project's invention.

## R3. Every check must be able to fail

Banned: `check(True, ...)`, `assert 1 == 1`, any condition that is an algebraic identity of how you just
defined the terms, any condition with no numerical content. Nine such checks have been removed from this
corpus and four shipped inside "verified" scripts.

Test: **can you name an input that would make this check print FAIL?** If not, delete it and write a real one.

## R4. Verify a failure exactly as hard as a success

A "fails / too low / in tension / ruled out" claim needs the same rigour as a "works" claim. Manufacture
neither. Two specific ways this project manufactured deficits before:
- treating **scatter** as if it were measurement error (a model with no measurement in it has no σ),
- truncating a **systematic range** at its tight end.

## R5. Both a₀ footings, on every dimensional number

Report canonical **and** ALT (see `04_FRAMEWORK_FACTS.md`). If a verdict flips between them, that is the
headline, not a footnote.

## R6. Watch for the a₀-versus-floor factor of 2

Milgrom's balance contains the **floor** `k = a₀/2`, not a₀, and `a₀ = 2k` always. This factor has been got
wrong **four times independently** in this project. Before reporting any coefficient, print which object you
computed — a₀ or the floor — and the other one next to it.

## R7. Never claim closure

Banned: "the theory is closed", "no open doors", "this settles it", "definitively ruled out". A no-go is
always **relative to a named class**. State the class. Then state one thing outside it.

## R8. Five examples is not a theorem

If you test N candidates and they all agree, you have N data points. Write "of the N tested". To claim a
theorem you need the general argument, and you must check the step where the general argument could fail.

## R9. FROZEN — never modify

- `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`
- any `*_HASH.txt`
- any file under `ai_slop/`
- any already-published paper in `opus_48_extended_research/papers/` (write a new file instead)

## R10. Never put private material in the repo

No email addresses, no phone numbers, no correspondence, no third-party names, no API keys or tokens.
The Zenodo token lives in `/Users/carlzimmerman/new_physics/.env` and must **never** be printed or committed.

## R11. Sibling repos are LOCAL-ONLY — never push

`project_atomos`, `sonolysis_lab`, `weather-lab`. They have no remote by design.

## R12. Do not publish to Zenodo

That is Carl's action. You may prepare a paper file and a publisher script with a `--dry-run` flag; you may
run the dry run. You may not publish.

## R13. Reason from the framework's own premises first

This is **modified inertia** with a horizon-derived a₀ and its own interpolation. Do not judge it as "just
Milgrom's", do not import McGaugh's ν, and do not treat agreement with ΛCDM as the standard of correctness.
Equally, do not treat disagreement with ΛCDM as evidence for the framework.
