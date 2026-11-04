"""Operational G1 fit checks. ADDENDUM_G2_2026-11-04 records scope and provenance."""
import math
import statistics


def start_agreement(speeds):
    """All three starts must yield finite positive speeds within the filed 15%."""
    values = [float(v) for v in speeds]
    usable = len(values) == 3 and all(math.isfinite(v) and v > 0 for v in values)
    spread = (max(values) - min(values)) / statistics.median(values) if usable else None
    return {'speeds': values, 'spread': spread, 'pass': bool(usable and spread <= 0.15)}


def velocity_error(speed, quoted_error, mock_fraction):
    """Fixed empirical floor, not an S/N-dependent coverage guarantee."""
    if not all(math.isfinite(x) for x in (speed, quoted_error, mock_fraction)) or speed <= 0 or quoted_error < 0 or mock_fraction < 0:
        raise ValueError('Finite positive speed and nonnegative error/floor required')
    return {'error': max(quoted_error, mock_fraction * speed), 'quoted_error': quoted_error,
            'floor_fraction': mock_fraction, 'floor_error': mock_fraction * speed,
            'method': 'fixed archived mock RMS floor; not S/N-matched'}
