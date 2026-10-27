"""Opt-in common Gaussian Fourier coefficients for future X48 IC studies.

No import of, or change to, x48_zoom.py. For the same physical box, seed and
P(k), dk/ng**3 agrees at shared interior integer modes across resolutions.
P has volume units, k has inverse-length units, and E|dk/ng**3|**2=P(k)/L**3.

All even-grid Nyquist planes are zero: they cannot be treated as the same
independent +/- physical modes after refinement. The DC coefficient is zero.
The k_z=0 plane is explicitly Hermitian. Odd grids have no Nyquist plane.
This does not make separately constrained Hoffman-Ribak fields identical.
"""
import hashlib
import math
import struct

import numpy as np


def _normal_mode(seed, mode):
    """CN(0,1), with conjugation determined by the first nonzero mode index."""
    direction = next(value for value in mode if value != 0)
    sign = 1 if direction > 0 else -1
    canonical = tuple(sign * value for value in mode)
    digest = hashlib.blake2b(struct.pack("<4q", seed, *canonical), digest_size=16,
                             person=b"X48common-v1").digest()
    a, b = struct.unpack("<2Q", digest)
    # Exactly representable 52-bit fractions strictly inside (0,1).
    u = ((a >> 12) + 0.5) / 2 ** 52
    v = ((b >> 12) + 0.5) / 2 ** 52
    radius = math.sqrt(-math.log(u))
    phase = 2 * math.pi * v
    return radius * complex(math.cos(phase), sign * math.sin(phase))


def support_mask(ng, box_size, kmax=None):
    """Shared draw/conditioning support in NumPy rFFT order.

    Zero DC and every even-grid Nyquist plane, optionally restrict physical |k|.
    Apply this same mask to P(k) before building constraint covariances.
    """
    if (not isinstance(ng, (int, np.integer)) or ng < 3 or
            not np.isfinite(box_size) or box_size <= 0):
        raise ValueError("Require integer ng>=3 and positive finite box_size")
    if kmax is not None and (not np.isfinite(kmax) or kmax <= 0):
        raise ValueError("kmax must be finite and positive")
    ng = int(ng)
    m = np.rint(np.fft.fftfreq(ng) * ng).astype(int)
    mz = np.arange(ng // 2 + 1)
    mx, my, zz = np.meshgrid(m, m, mz, indexing="ij")
    k = (2 * math.pi / box_size) * np.sqrt(mx * mx + my * my + zz * zz)
    allowed = k > 0
    if ng % 2 == 0:
        allowed &= (abs(mx) != ng // 2) & (abs(my) != ng // 2) & (zz != ng // 2)
    if kmax is not None:
        allowed &= k <= kmax
    return allowed


def gaussian_rfft(ng, box_size, seed, power_spectrum, kmax=None):
    """Return NumPy-rFFT-normalized coefficients, shaped (ng, ng, ng//2+1).

    power_spectrum returns finite nonnegative P(k), broadcasting to the k grid.
    The same physical kmax gives a common band-limited field across resolutions.
    No resolution, array size, draw order or FFT index appears in a mode's RNG key.
    """
    allowed = support_mask(ng, box_size, kmax)
    if not isinstance(seed, (int, np.integer)) or not 0 <= seed < 2 ** 63:
        raise ValueError("Require integer 0<=seed<2**63")
    ng, seed = int(ng), int(seed)
    m = np.rint(np.fft.fftfreq(ng) * ng).astype(int)
    mx, my, zz = np.meshgrid(m, m, np.arange(ng // 2 + 1), indexing="ij")
    k = (2 * math.pi / box_size) * np.sqrt(mx * mx + my * my + zz * zz)
    power = np.broadcast_to(np.asarray(power_spectrum(k), float), k.shape)
    if not np.all(np.isfinite(power)) or np.any(power < 0):
        raise ValueError("P(k) must be finite and nonnegative")
    dk = np.zeros(k.shape, dtype=complex)
    scale = ng ** 3 * np.sqrt(power / box_size ** 3)
    for i, j, l in zip(*np.nonzero(allowed)):
        dk[i, j, l] = scale[i, j, l] * _normal_mode(seed, (int(mx[i, j, l]), int(my[i, j, l]), int(zz[i, j, l])))
    return dk
