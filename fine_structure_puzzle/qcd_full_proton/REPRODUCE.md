# FSP-011 reproduction

From the repository root, write into a fresh directory so that the archived run_001 is not overwritten:

    mkdir -p /tmp/fsp011_replay
    python3 -I fine_structure_puzzle/qcd_full_proton/compute_fsp011.py \
        --inputs fine_structure_puzzle/qcd_full_proton/INPUTS.json --output /tmp/fsp011_replay/result.json
    python3 -I fine_structure_puzzle/qcd_full_proton/rederive_fsp011.py \
        --inputs fine_structure_puzzle/qcd_full_proton/INPUTS.json --output /tmp/fsp011_replay/rederive_blind.json
    python3 -I fine_structure_puzzle/qcd_full_proton/rederive_fsp011.py \
        --inputs fine_structure_puzzle/qcd_full_proton/INPUTS.json --output /tmp/fsp011_replay/rederive_compare.json \
        --author-result /tmp/fsp011_replay/result.json

All three runs must exit with code 0 and report "all_checks_pass": true. Each takes about one second on one core. The run used Python 3.13.9, numpy 1.26.4, scipy 1.14.1, sympy 1.13.1 and mpmath 1.3.0. Numerical values should agree with run_001 to quadrature tolerance, about 1e-12 relative.

Input and output hashes are in [run_001/manifest.json](run_001/manifest.json). This is a plain manifest: the programme's local mathbox-v2 runner was not available, so it is not a v2 manifest. The FSP-010 file imported for the sigma calibration is pinned there by SHA-256.

The source PDFs used for PDF-text authentication (2609.15154v1 and hep-ex/0602017v3) are not committed. Their SHA-256 values are in [SOURCES.json](SOURCES.json). Obtain the exact arXiv versions to re-check them.
