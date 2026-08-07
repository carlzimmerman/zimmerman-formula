# W02 — Can you hear the shape of a drum?
COST: M | script: `wacky_isospectral_drums.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Kac asked in 1966 whether the spectrum of the Laplacian determines a planar domain. Gordon, Webb and
Wolpert answered **no** in 1992 with an explicit pair of 7-sided polygons that are *not* congruent but have
*identical* Dirichlet eigenvalue spectra. Build them and verify it numerically.

## Do
1. Construct both GWW domains (they are unions of 7 congruent triangles glued differently — look up the
   standard coordinates).
2. Solve the Dirichlet eigenvalue problem on each (finite elements, or a boundary/mode-matching method).
   Get the first ~12 eigenvalues on both.
3. Compare eigenvalue by eigenvalue. They should agree to your solver's accuracy. **Refine the mesh 4× and
   show the agreement improves** — that is the check that distinguishes a real result from mesh error.
4. Control: perturb one domain slightly and confirm the spectra now visibly split.

## Why it is thematically apt
It is the cleanest existence proof that *a complete set of measurements can fail to determine a structure.*
Which is exactly the shape of this project's coefficient problem — the RAR shape is provably blind to a₀.
