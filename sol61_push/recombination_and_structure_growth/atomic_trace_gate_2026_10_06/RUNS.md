# Frozen atomic trace and frame checks

- `main`: 14/14; failures: none.
- `density`: 13/14; failures: saha_frame_cancellation.
- `trace`: 11/14; failures: trace_expression, ionization_trace_derivative, ionized_nonzero_rest_trace.

All three version-2 manifests validated against current inputs. Controls change the density conformal weight or incorrectly use energy density as stress trace; their intended checks fail. Runner completion is distinct from mathematical acceptance. Exact symbolic identities support the declared ideal-gas reduction; finite temperatures corroborate the analytic bound. No atomic transport or expansion history was simulated.
