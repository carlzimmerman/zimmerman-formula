# Fixture-count correction

The frozen grids contain 3 epsilon values, 3 stiffness values and 4 wavenumbers:
3*3*4=36 combinations, not the stated 48. The initial script checked 48 and
failed only that count check. Its output and code remain preserved. No fixture,
threshold, equation, parameter range or result has changed. run_v2.py checks
the correct Cartesian-product cardinality. This is a counting correction,
not a change to the physics test or its pass tolerances.
