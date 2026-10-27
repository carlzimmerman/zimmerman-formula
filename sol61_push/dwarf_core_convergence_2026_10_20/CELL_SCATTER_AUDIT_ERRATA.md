The preserved `cell_scatter_audit_run_001` contract mistakenly declared SciPy
1.13.1. The actual `/usr/bin/python3` worker environment is SciPy1.11.4,
NumPy1.26.2, Python3.9.6. The source, numerical output, manifest and mistaken
contract remain unchanged. The corrected version must be used for any replay;
no numerical result or scope is changed by this explicit metadata correction.
