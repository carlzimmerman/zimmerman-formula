# Preserved first-run failure

The first run solved all24 backgrounds and printed their envelopes, then failed
at JSON serialization because the sum of NumPy booleans produced numpy.int64.
No mathematics, solver, threshold or fixture changed. The retained original
script is gradient_serialization_failure.py.txt. The subsequent version casts
the count to a Python int. The original raw execution remains local under
evidence/gradient; its traceback contains a local absolute path, so that raw
traceback and its manifest are not included in the portable committed evidence.
The new run is evidence/gradient_verified. This is an implementation failure,
not a failed gradient bound.

Original script SHA256: 944580be33131cf9a9d84a6a41ea62846ca77883668d4ed23a2ae1d98222b331
