# QX4 amendments (each committed before the numbers it governs)

## A1 (iteration 1, before any graded galaxy number): Malin 1 Sigma by non-negative annulus decomposition

The quick run's direct Toomre inversion failed K4 (gas 11.7 %, LSB 6.4 % against the 3 % line). It crashed
before any graded galaxy number. Causes: the plotted curves start at 3.1 kpc, and clipping negative Sigma breaks
the inversion. Replacement: write Sigma as non-negative uniform annuli, about 60 log-spaced edges from 0.3 to
200 kpc. Each annulus's thin-disc midplane V^2 is computed by ring sums. Non-negative least squares
(scipy.optimize.nnls) then matches the plotted V^2 on the plotted range, weighted by 1/V^2_plot. This
reconstructs an input; it fits nothing in the grade.
- No regularisation.
- K4's line is unchanged (3 % at the Table radii, thin ring-sum). If K4 still fails, Malin 1 gets no
  iteration-1 label.
- AGC 114905 is unaffected (its Sigma forms are published).

## A2 (POST-RESULT, after the iteration-1 quick run): no annulus beyond the plotted range, reported alongside A1

The quick run shows that A1's NNLS places most of the gas mass (total 3.4e11 Msun) in annuli between the last plotted
radius (98.4 kpc) and 200 kpc, where the plotted curve does not constrain it. That mass changes the nonlinear field
inside 98 kpc. A2 restricts the annuli to [0.3, 98.4] kpc, which means no mass beyond the plot (the same as a
Keplerian extension). It was written after seeing A1's quick chi2 (54.1 / 42.2, NOT RESCUED). It is therefore
labelled post-result. Both are reported, and Malin 1's iteration-1 label is given only if A1 and A2 agree.
