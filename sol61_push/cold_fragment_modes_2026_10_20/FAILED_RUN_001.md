# Failed direct tight profile launch

run_001 has status failed. The copied original function exhausted its
8000-node mesh cap on a direct L60/tol1e-8 cold start. It returned status1
while charge and virial checks passed, so no Hessian result was accepted.
The saved maximum collocation residual4.57e-6 exceeds the requested tolerance.

V2 retains tolerance1e-8 and all spectrum controls. It warm-starts from the
documented L40 branch and changes only the locally loaded function's
max_nodes keyword to24000. The original source, old helper/script/contract
and failed logs are preserved. No physical coefficient or pass threshold changes.
