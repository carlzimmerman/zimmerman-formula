# Numerical transition

run_001 is a preserved failed record: the order-8 early-time heat series
on (0,.025) left 1.1515273e-20 error against a 1e-20 criterion. Direct
split/order checks gave 6.6646192e-25 at split .02/order10 and
1.6052003e-28 at split .01/order10. This is truncation of a numerical
cross-check, not a changed spectral/physical result. The current code
uses order10 at the original .025 split and retains the unchanged
criterion plus the .02/order10 stability comparison. Original code
bytes are saved in historical_inputs/compute_photon_run001.py.snapshot.txt.
No DERIVATION, REPORT, source, old science or old manifest was edited.
The current authoritative evidence is run_002/manifest.json if completed.
