# Exploratory stress run interrupted; excluded from final formation evidence

The agent sent Ctrl-C through its execution session after the optional100x-rate
experiment entered cells with opacity proxy C*rho*width about9.25. At that point
the current large-system trajectory had not reached its requested final time.
Four earlier rows are present in results.json; the running trajectory is only
represented by progress.json. These are partial exploratory data, not a completed
or validated suite.

The bounded runner's finally block stops and waits for its child. The execution
session ended with exit130/KeyboardInterrupt. Interrupting its outer wait bypassed
its final manifest writer, so there is NO completed manifest for this folder.
Do not fabricate missing before/after hashes or count this run as validated.
No source was intentionally changed during execution. Preserve these files as
history, but exclude their numerical formation results from final analysis.

The independent stress_screen experiment records the initial cell-opacity screen
with normal bounded-run provenance. This limitation concerns the high-rate
experiment; all default-coefficient formation suites completed separately.
