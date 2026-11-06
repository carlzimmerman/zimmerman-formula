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
