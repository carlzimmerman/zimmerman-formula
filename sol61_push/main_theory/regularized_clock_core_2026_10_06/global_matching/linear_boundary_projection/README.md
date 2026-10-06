# Exact linear source-boundary projection

`REPORT.md` gives the real complex-order modified-Bessel basis and shows C0 does not remove the formal growing-I clock mode in the interpolated source endpoint. `checks.py` reads the frozen finer nonlinear outputs and performs only an independent finite linear ODE check. No nonlinear source shoot is executed.

`runs/main_a` must pass. Controls wronskian/drop_r2/C0_is_growing0 must fail. Standard runner contract/provenance pin actual inputs and tested ranges. Reproduce with run_experiment.py, this contract and every execution_artifact as --input, fresh output, /usr/bin/python3 checks.py --output <run>/results.json; caps wall60s CPU45s threads1. Validate all manifests.

Primary DLMF URLs/version/hypotheses/cachehash are in sources.json. The ignored cached web snapshot is a readable webtool return, notoriginalHTML; restore by opening thelisted primarypages for source re-audit and record any newhash. Computation reruns do not require that cache. Formal asymptotics classify only the linear equation; full cosmic boundary matching, health and A/Hselection remainunproved.
