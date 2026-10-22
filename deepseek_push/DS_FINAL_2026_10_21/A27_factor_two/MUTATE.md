# A27 — mutations

Three mutations, each corrupting a different load-bearing input of the argument, each run as
`python3 a27_checks.py --mutate=<id>`. Mutated stdout: `a27_MUTATE_<id>.out`; mutated results:
`a27_results_<id>.json`. All three exit 1 with **15/16**, so each breaks exactly one check.

| id | corrupts | must fire | observed |
|---|---|---|---|
| M1 | the target factor: `β = 2 → 1` (diameter → radius) | K1 | the three statements stop agreeing: a₀* moves by 0.5 relative → 15/16 |
| M2 | the boundary condition: Dirichlet → Neumann | K5 | `λ_max/ℓ = inf` instead of 2 → 15/16 |
| M3 | the cell topology: `χ = 1 → 4` | K2 | `κ(β=2, χ=4) = 0.25` instead of 0.5 → 15/16 |

## M1 — replace the diameter by the radius

    $ python3 a27_checks.py --mutate=M1
    K1  FAIL measured=0.5 threshold=1e-14  R-beta^2=0, kappa-1/beta=0, three a0* agree to 5.0e-01;
        a0*= sqrt(2)*sqrt(Lambda)*c**2/(4*sqrt(pi))
    A27 COMPLETE: 15/16 checks PASS.

This is the mutation that matters: with β = 1 the identities R ≡ β² and κ ≡ 1/β still hold, but the
three *statements* no longer describe the same theory. The a₀* printed is c²√(Λ/8π) — exactly twice
the correct c²√(Λ/32π) — so the check measures that the equivalence of "L = 2ℓ₁", "κ = ½" and
"R = 4" is what pins the integer 2, and that replacing 2 by 1 destroys the equivalence rather than
merely shifting a number. That is the quantitative form of the report's §1.

## M2 — swap the wall for no wall

    $ python3 a27_checks.py --mutate=M2
    K5  FAIL measured=inf threshold=0  BC=neumann lambda_max/ell=inf (Dirichlet gives exactly 2),
        overtone lambda/ell=1
    A27 COMPLETE: 15/16 checks PASS.

The standing-wave candidate's 2 exists only because a Dirichlet wall is imposed at r = ℓ₁. With
Neumann conditions the constant mode has k = 0 and there is no longest wavelength at all. The check
compares λ_max/ℓ against 2 exactly, so `inf` cannot slip through. This is the report's point that
the factor 2 in candidate (ii) is a property of the wall, not of the cell.

## M3 — change the cell's topology

    $ python3 a27_checks.py --mutate=M3
    K2  FAIL measured=0.25 threshold=1e-14  kappa(beta=2,chi=4)=0.25 (must be .5);
        kappa(2,1)=1/2 kappa(1,4)=1/2 R(2,1)=4 R(1,4)=4
    A27 COMPLETE: 15/16 checks PASS.

With χ = 4 (S²×S²) the diameter of the cell is *not* the length that gives κ = ½: β = 1 is. The
mutation therefore tests the report's §2 claim that the factor 2 is the χ = 1 coordinate of the curve
β√χ = 2, not an invariant of the theory. Note that the two explicitly evaluated pairs (2,1) and
(1,4) still print 1/2 and 4 — they are computed at fixed χ — which is exactly why the check has to
test the *mutated* pair (β = 2, χ = CHI) and not the two reference pairs.

## What is *not* mutated, and why

The no-go claims (K13, K15, K16) are not tied to a constant: they are statements about the *form* of
the argument (the cap family is the natural-length family; every link premise fixes a₀; no candidate's
image is {2}). A mutation that broke them would have to alter the algebra of the definitions, which
K1 already pins symbolically. The three mutations above cover the three places where a number enters
by hand: the target integer, the boundary condition, and the topology. K15's own teeth are shown
inside the check (defining L := 2ℓ₁ makes the conclusion identically zero, which is the signature of
a redefinition) rather than by a fourth mutation.