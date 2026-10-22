# A50 mutation control

Purpose: prove the checks have teeth. Each mutation changes one physical claim that the
lane's verdict depends on, and each must break at least one check and exit non-zero.

Run from this directory:

    python3 a50_checks.py                 # baseline: 17/17 PASS, exit 0
    python3 a50_checks.py --mutate=m1     # 14/17 PASS, exit 1
    python3 a50_checks.py --mutate=m2     # 16/17 PASS, exit 1
    python3 a50_checks.py --mutate=m3     # 16/17 PASS, exit 1

Each mutation is a single branch in the script (search for `MUT ==`), so the baseline
binary is untouched and the diff is auditable.

---

## m1 — "the first-law coefficient is the constant 1/2"

What it changes: `lam` is replaced by `sp.Rational(1, 2)` after K2 has verified the true
formula, i.e. the claim "λ = 1/2 for every equation of state" is injected.

Why it matters: this is precisely the claim that would make κ = 1/2 "thermodynamically
forced". If the checks did not notice, the lane's whole no-go would be empty.

Observed:

    [m1] lambda forced to the constant 1/2 (K2 still verifies the true formula)
    K3   FAIL measured=w_sol=[] dust_factor=2.000000000000000 lam(vac)=0 threshold=w=1/3, 2, -1
    K4   FAIL measured=spread=0.000000000000000 over w in [-1,1/2] threshold=2.25 (>2)
    K5   FAIL measured=resid=1.5e+00 d(resid)/dHdot=1.5e+00 G_eff/G(w=0)=2.000000 threshold=0, 0, 2
    A50 COMPLETE: 14/17 checks PASS.
    exit=1

Teeth: K3 loses its unique solution w = 1/3 (a constant can never equal 1), K4's spread
collapses from 2.25 to 0, and K5's residual becomes non-zero — the law stops being an
identity. Three independent checks catch the same false premise.

---

## m2 — naive energy in the Komar slot

What it changes: in K8 the Komar energy `|ρ+3P|V = 2ρV` is replaced by the naive `ρV`.

Why it matters: this is the exact confusion that produces the "1/2" in the equipartition
count. If K8 could not distinguish the two energies, the lane could not claim that the 1/2
is bookkeeping rather than physics.

Observed:

    K8   FAIL measured=ratio=0.500000000000000 sym=1 threshold=1
    A50 COMPLETE: 16/17 checks PASS.
    exit=1

Teeth: the ratio moves from exactly 1 to exactly 1/2, i.e. the check separates the two
energy definitions by the factor that is the whole subject of §5.

---

## m3 — wrong geometric factor in the κ map

What it changes: in K12 the required coefficient is computed as `a0/(cH) = κ·Z` instead of
`κ·√(3/8π) = κ·2/Z`.

Why it matters: `Z` is the reciprocal-flavoured number (`2Z = 11.5776`, the brief's "2/0.1727").
Using it in place of `2/Z` is the most natural wrong turn in this lane, and it is the
difference between "the factor is √(3/8π)" and "the factor is 2√(32π/3)".

Observed:

    K12  FAIL measured=a0/(cH)=1.000000000000000 threshold==1/Z=0.1727471
    A50 COMPLETE: 16/17 checks PASS.
    exit=1

Teeth: at κ = 1/2 the mutant returns a0/(cH) = 1.0 instead of 0.172747, a factor 5.79 wrong,
and K12's identity residual is non-zero.

---

## What the mutations do *not* break

m2 and m3 each break exactly one check; m1 breaks three. No mutation touches K1, K6, K7,
K9, K10, K11, K13–K17. That is intended: those checks encode the exact identities and the
κ-absence argument, which no local mutation of a coefficient can change. A mutation that
broke everything would prove nothing about which check is load-bearing.

## Cold start

Verified with a stripped environment:

    env -i PATH=/opt/homebrew/Caskroom/miniconda/base/bin:/usr/bin:/bin HOME=$HOME \
        python3 a50_checks.py
    A50 COMPLETE: 17/17 checks PASS.        (exit 0, 1.0 s)

No network, no state carried between runs, no files read except the interpreter's own
libraries. `a50.out` is the captured stdout of exactly that run; `a50_results.json` is
rewritten by each run and is the 17/17 baseline as delivered.