# Direct read-only link to Claude p57

The following actual inputs were read on 2026-10-06; neither script was run or edited:

- `sonnet55_push/puzzle_32pi/p57_etno_secular_nbody.py` SHA-256 `3024aaebf83532eadf741b3dbaf2b0c1f810c6559289438ccb2b26ef1dcbb521`.
- `sonnet55_push/puzzle_32pi/qumond_efe_multipole.py` SHA-256 `1559904adb6b63b108a9f9345c07fc0303cf7cd7423a4df9b6a4aa957ed52001`.

The p57 docstring explicitly uses the QUMOND multipole solver, a secular detached-disk proxy, fixed source/orbit initial conditions, and planetary/tidal terms. It withdraws an earlier algebraic shortcut and labels its Neptune-scattering omission. The multipole solver computes the physical gradient by solving a Poisson equation with div[(nu−1)G] source. The symmetric candidate instead solves an eliminated nonlinear star equation and has the distinct linear external-field Green response derived here. Thus neither p57 source fields, Q2, secular occupancy nor likelihood can be carried over. This child is a discriminating local prediction, not a rerun or validation of the old observational computation. These source-link notes are outside the mathematical runner inputs and make no new numerical claim.
