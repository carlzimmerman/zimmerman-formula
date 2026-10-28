# Execution amendments

A1, before successful audit execution: the first normal and mutation launches
failed in the runner's preexec_fn, before Python executed the scientific script.
An isolated diagnostic identifies macOS RLIMIT_AS as the failing operation;
RLIMIT_CPU succeeds. Preserve both launch-failed manifests. Retry with the same
mathematical contract, CPU/thread/time caps, and no OS address-space cap. The
script reports actual peak RSS; the small standard-library audit remains bounded.
No criterion or source data changed. These are environment failures, not results.
