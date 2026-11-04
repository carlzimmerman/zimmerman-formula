# Environment-record correction

All vectors experiments launched by `launch.py` used its `sys.executable` for
both the audit runner and numerical child. Here the shell command `python`
resolved to Miniconda Python3.13.9, NumPy1.26.4, SciPy1.14.1. The original
launcher incorrectly copied historical software strings Python3.9.6,
NumPy1.26.2, SciPy1.11.4 into those contracts. Frozen contracts, manifests and
sources are preserved; this explicit correction applies only to vectors jobs
launched by that launcher. It does not apply to coordinator jobs, which use
an explicitly different Python3.9.6 interpreter.

Starting with `run_coulomb002`, `launch_v2.py` detects and records the actual
versions. Runner manifest interpreter metadata independently identifies the
runner version. No package was installed or changed. Source hashes and
numerical results from earlier vectors jobs are unchanged. Their declared
software strings should be read with this erratum.
