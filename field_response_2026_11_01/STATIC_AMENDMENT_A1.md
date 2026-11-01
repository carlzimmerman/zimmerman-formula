# A1: retain nonfinite diagnostics from failed continuation

Run `static_run_001` reached all scheduled baseline/family loops but failed
strict JSON output because a nonconverged BVP diagnostic was NaN. Its logs,
manifest, original script and contract remain unchanged. The incomplete
result JSON is not scientific evidence.

The new entry point `static_response_v2.py` wraps only JSON serialization.
It retains every existing calculation and failure gate in the unchanged
`static_response.py`, converts nonfinite numeric diagnostics to JSON null,
and records their exact paths and original representations in the output.
It also records observed macOS peak RSS. No forcing, tolerance, equation,
continuation step, branch choice or success criterion changes.

The executable command for the fresh run is

    python3 field_response_2026_11_01/static_response_v2.py NEW_RUN/result.json

An unsuccessful mathematical/solver case will still cause exit status one,
even when the run successfully preserves all its evidence. A runner status
`failed` must therefore be interpreted using individual case records; it is
not automatically a serialization failure or a physical nonexistence result.
