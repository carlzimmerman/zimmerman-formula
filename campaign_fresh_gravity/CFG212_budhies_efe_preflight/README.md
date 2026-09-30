# CFG212 — BUDHIES external-field pre-flight (A963 / A2192): can HI widths separate an EFE-merge law from B's isolated law?

- **Criteria:** `FROZEN_CRITERIA.md` (6df482512), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Run:** `python3 campaign_fresh_gravity/CFG212_budhies_efe_preflight/cfg212_budhies_preflight.py`, about 17 s. Main: 3/3 checks. MUTATE (A963 mass × 100): 4/4, with S_opt going from 1.04 to 6.55.
- **Inputs:**
  - Positions, HI redshifts and published cluster masses only. **The script never reads W20/W50.**
  - Two W50 values were displayed once while checking the column format; this is disclosed in the criteria.
  - Every cluster number is a summariser read (d5d584788), UNVERIFIED against the PDFs.
  - B's prediction (isolated law, no EFE) is the orchestrator's reading of FG001, not a committed formula.

## Bottom line: power only under optimistic inputs; not run

- **Members.** A963 has 94 members (|Δv| < 3σ), of which **8 lie within 1 Mpc** projected and 30 within 2 Mpc. A2192 has 24 members, **3 within 1 Mpc** and 8 within 2 Mpc. The members' median R is about 2.6 Mpc.
- **PRIMARY cell:**
  - Inputs: M200 X-ray / A2192_1a; r = √1.5 R; y_int = 0.3; σ = 0.20 dex; perpendicular EFE form; P2; canonical.
  - **S_opt = 1.04**, and that is an UPPER bound on any real test's separation.
  - **93% of Σ Δ² comes from the 11 members within 1 Mpc.**
- **OPTIMISTIC cell:** high masses, r = R, y_int = 0.1, σ = 0.15, wider A963 membership. S_opt = 5.70.
- **Full grid:** 768 cells, maximum 12.2 (parallel form, y_int = 0.1); 354 cells are ≥ 3. The power depends mostly on y_int, the internal field at the HI edge, which these tables do not give per galaxy, and on the deprojection.
- **Decision (frozen):** "power only under optimistic inputs: not run unless the inputs are tightened". That means verified masses/M500, a membership catalogue and per-galaxy internal fields.
- **Physics against running it even then.** Nearly all the power sits in the 11 inner members. That is where ram-pressure truncation of the HI also lowers W50, with the same sign as the EFE. The pre-flight cannot separate the EFE from stripping, and B's own exception (tidal stripping, not modelled) acts in the same direction.

## Fixes after the first MUTATE run (kept)

1. The first MUTATE run printed S_opt 6.55 against the main run's 1.04, but did not state the frozen control as a check. The check was added (`*_MUTATE_firstrun*`).
2. The added check's unmutated reference divided both clusters' masses and printed 1.02. It was fixed to rescale only A963 and now prints 1.04; the check passes either way (`*_MUTATE_secondrun*`).
