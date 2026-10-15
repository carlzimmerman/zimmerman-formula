The first launcher invocation failed before executing the computation because
the Mathbox runner accepts project-relative output paths and rejected the
absolute output path. No scientific output or manifest was created. The
controls_001_contract.json remains as the attempted contract. The launcher
was corrected to pass its project-relative output path; retry uses a fresh name.
