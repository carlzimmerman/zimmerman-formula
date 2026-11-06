# Independent audit: combined constitutive concentration

**Verdict: proved as written.** The construction refutes an algebra-only
universal exclusion of finite timelike surface stress. It does not give a
solution of the native differential equations or a same-data nonuniqueness
example.

The quantified algebraic target is that every finite concentration of
native constitutive stresses obeying normal no-dipole must vanish. The
displayed positive-weight mixture has nonzero stress and zero normal row,
so it is a counterexample to precisely that assertion.

## Independent calculation

At P=0, use W(0)=W_P(0)=0 and fixed finite V. Differentiating H at fixed A,

    H=gamma r^4/2-A r^3+O(r^2),
    r H_r=2 gamma r^4-3 A r^3+O(r^2).

For an unboosted high-r state, T=diag(r H_r-H,H,H,H). Multiplication by
2c/(gamma r^4) gives diag(3c,c,c,c). These states are on branch despite
their negative large D: D+r^2=(Ar-1)/gamma>0 once r>1/A. Thus the switch
condition is not being silently violated.

At r_L=1/A, Q=1 and direct differentiation gives r_L H_r=2 gamma r_L^4.
Choosing mu=2 gamma r_L^4+d>0 makes the enthalpy coefficient -d.
For each sign, n_a=(-sqrt(1+lambda^2),+/-lambda,0,0). Multiplication of
H_L eta_ab-d n_a n_b by c/(2d lambda^2) gives a negative null tensor.
The two signs cancel the mixed component and add to diag(-c,-c,0,0).
The bounded H_L term vanishes. Total unweighted multiplier mass is
c mu/(d lambda^2), which tends to zero. Each constituent uses a positive
volume weight and lies in the native algebraic admissible domain.

Their sum is diag(2c,0,c,c). It has zero normal row and column and base
trace -2c. That trace comes from high-r concentration, so it is not
covered by the bounded-invariant boost-only trace lemma. Its transverse
pressure c also does not contradict the large-r lemma, which requires
bounded boosts for the whole sequence. These are exact limiting identities,
not a finite-parameter numerical fit.

The mixture can be placed in disjoint vanishing-volume sublayers as an
algebraic stress sequence. A single finite common A and P=0 are enough;
no cap excursion is required. This observation makes no claim that those
sublayers can be integrated into the other native fields.

## Scope checks

The differential constraints are genuinely additional: setting P=0
identically in a regular field would give eP=0, whereas the displayed
algebraic D is nonzero. Thus the chosen values cannot simply be declared
a native field solution. Smooth interpolations must solve polarization,
clock integrability, scalar evolution and Einstein equations, along with
the limiting conservation law and prescribed incoming data. Normal
no-dipole is only one necessary part of that law.

All constitutive and normal-flux obligations pass. Field realizability,
formation, post-breakdown existence and uniqueness are not addressed.
The strongest safe conclusion is that these differential obligations
cannot be replaced by the proposed universal constitutive/no-dipole
argument. No additional loophole or selection rule is inferred.

## Reproduction and provenance

Independent delegated algebra review, 2026-11-06. Reran:

    python3 ac2q_postfold_2026_11_06/pf09/check_combined_defect.py --output ac2q_postfold_2026_11_06/pf09/review/combined_defect_result.json

All six assertions passed. The raw output is retained beside this note.
Input SHA256 values:

- `COMBINED_DEFECT_TEST.md`: `0b2f1f106ba8e14a1ec98a18b1c50f545d79d7008ce60004ed649da6b2e9aaf8`
- `check_combined_defect.py`: `1cdcdb58293b957f3d68d1a2105930cddb837b36bbdff0f6f455848cebbd1445`
