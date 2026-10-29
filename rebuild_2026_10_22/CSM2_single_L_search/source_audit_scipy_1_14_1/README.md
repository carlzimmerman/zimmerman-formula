# Solver source provenance

installed_bounded.py.txt and installed_brentq_wrapper.py.txt are inspect.getsource
captures from installed SciPy1.14.1. brentq.c is the official version-matched
source from https://raw.githubusercontent.com/scipy/scipy/v1.14.1/scipy/optimize/Zeros/brentq.c.
SOURCE.json records installed versions/platform and observed binary hashes;
the completed solver_scope_001 manifest pins every cached input's SHA256.
scipy_LICENSE.txt is the installed distribution's redistribution license.
These records do not independently establish build equivalence or libm ULP bounds.

The installed license is preserved verbatim, including four whitespace-only lines.
