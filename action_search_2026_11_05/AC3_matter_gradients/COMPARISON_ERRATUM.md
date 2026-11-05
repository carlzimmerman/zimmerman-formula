# Symbolic comparison repair

The original UV run failed only a structural SymPy equality test: a factored
and an expanded diagonal entry compare unequal with ==. The simplified
matrix difference is exactly zero. derive_v2.py tests zero residuals entrywise,
matching the other exact checks. No equation, fixture or tolerance changed.
The original failed evidence/uv record is retained.
