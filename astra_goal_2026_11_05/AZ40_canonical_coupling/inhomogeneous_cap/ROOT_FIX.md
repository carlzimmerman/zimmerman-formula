# Safeguarded auxiliary root, before reruns

The257-node last-state dense interpolation reproduces a pure Newton2-cycle
for c=rA+rB+2Theta_star=1.319752267106786. Starting lambda=-c/3 yields
-.4399174,.1661601,-.4489129,.1684898,...; after80steps lambda=-.5018578,
step=.681832. The residual has derivative>=1.5, so failure does not mean
nonexistence of a cap solution. Root lies in[-c/3-2T/3,-c/3+2T/3].

bracketed.py inherits every equation, discretization and time rule from
planar.py and overrides only this scalar auxiliary solve. Accept Newton steps
inside the maintained bracket; otherwise bisect. Stop on normalized residual
1e-13, not just small step. Check against independent scipy brentq including
the reproduced failing coefficient and signed large coefficients. Rerun check17,
cap65 andcap257 with the original300second bound. Retain all previous outputs.
The postprocessing audit also uses this robust root for off-grid evaluations.
