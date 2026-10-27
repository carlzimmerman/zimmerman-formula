"""OPTIONAL precision-emulated GPU direct gravity; must pass local accuracy gates.

Build metal_gravity.mm explicitly. No CPU or FP32 fallback is hidden here.
Raw positions use hi/lo plus a third residual FP32 component, preserving the
stored binary64 input bits even for close pairs far from the coordinate origin.
Masses, coefficients, displacement arithmetic, forces and phi use high/low FP32
pairs; shader math is safe and error-free-transformation based. The default uses two DS
rsqrt Newton steps. Build with -DMETAL_GRAVITY_FAST_NEWTON for the separately
gated one-correction FMA residual expansion. Neither variant is raw FP32.
Output hi+lo reconstruction and U=.5*m@phi use CPU binary64. This is not native
FP64, bitwise CPU identity, or an a priori uniform error certificate.
"""
import ctypes
from functools import lru_cache
import hashlib
import os
from pathlib import Path

import numpy as np

G = .004498638185693768


def _split(values):
    values = np.asarray(values, dtype=np.float64)
    high = values.astype(np.float32)
    low = (values - high.astype(np.float64)).astype(np.float32)
    return np.ascontiguousarray(np.stack((high, low), axis=-1))


@lru_cache(maxsize=2)
def _load(path):
    if not Path(path).is_file(): raise RuntimeError('Explicitly build metal_gravity.mm or set METAL_GRAVITY_LIBRARY')
    library = ctypes.CDLL(path)
    array = np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS')
    library.metal_gravity_kernel.argtypes = [array, ctypes.c_uint32, array, array, array,
                                             ctypes.c_char_p, ctypes.c_size_t]
    library.metal_gravity_kernel.restype = ctypes.c_int
    library.metal_gravity_device_name.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    library.metal_gravity_device_name.restype = ctypes.c_char_p
    library.metal_gravity_newton_variant.argtypes = []
    library.metal_gravity_newton_variant.restype = ctypes.c_int
    library.metal_gravity_abi_version.argtypes = []
    library.metal_gravity_abi_version.restype = ctypes.c_int
    if library.metal_gravity_abi_version() != 2:
        raise RuntimeError('Metal library ABI does not match3-component coordinate layout')
    return library


def _library():
    return _load(str(Path(os.environ.get('METAL_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve()))


def backend_metadata():
    error = ctypes.create_string_buffer(4096)
    name = _library().metal_gravity_device_name(error, len(error))
    if name is None: raise RuntimeError(error.value.decode())
    variant = _library().metal_gravity_newton_variant()
    path = Path(os.environ.get('METAL_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve()
    return dict(device=name.decode(), precision='explicit double-single FP32 pairs; safe math',
                abi_version=_library().metal_gravity_abi_version(),
                algorithm_version='raw3f-coordinates/full-TwoSum-subtraction/ds-force-v2',
                newton_corrections=variant, tile_threads=128,
                library=str(path), library_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                coordinate_encoding='raw binary64 positions split into3 FP32 residual components; third added after pair subtraction',
                rsqrt_variant=('two general DS Newton corrections' if variant == 2 else 'one FMA-expanded Newton correction'),
                gravity='all ordered off-diagonal pairs in full3D, no tree',
                guarantee='empirical accuracy gate required; no native FP64 or bitwise CPU identity')


def _pack_particles(x, m):
    """Encode raw positions exactly in the admitted range, plus DS masses."""
    # Subtracting a distant reference origin in CPU binary64 can itself lose
    # close-pair bits. Preserve the raw coordinate representation instead.
    pairs = _split(np.column_stack((x, m)))
    packed = np.zeros((len(m), 12), dtype=np.float32)
    packed[:, :8] = pairs.reshape(len(m), 8)
    packed[:, 8:11] = ((x - pairs[:, :3, 0].astype(np.float64))
                       - pairs[:, :3, 1].astype(np.float64)).astype(np.float32)
    if not np.all(np.isfinite(packed)):
        raise ValueError('input range exceeds emulated arithmetic domain')
    reconstructed = (pairs[:, :3, 0].astype(np.float64) + pairs[:, :3, 1].astype(np.float64)
                     + packed[:, 8:11].astype(np.float64))
    if not np.array_equal(reconstructed, x):
        raise ValueError('coordinate range cannot be preserved by the explicit3-component encoding')
    return packed


def gravity(x, m, eps):
    x, m = np.asarray(x, dtype=np.float64), np.asarray(m, dtype=np.float64)
    if (m.ndim != 1 or x.shape != (len(m), 3) or not np.all(np.isfinite(x))
            or not np.all(np.isfinite(m)) or np.any(m <= 0.)
            or not np.isscalar(eps) or not np.isfinite(eps) or eps < 0. or len(m) > 1000000):
        raise ValueError('finite x(N,3), positive m(N), finite eps>=0 and bounded N required')
    if len(m) < 2: return np.zeros_like(x), 0., np.zeros(len(m))
    packed = _pack_particles(x, m)
    output = np.empty((len(m), 4, 2), dtype=np.float32)
    error = ctypes.create_string_buffer(4096)
    status = _library().metal_gravity_kernel(packed, len(m), _split(eps * eps), _split(G),
                                              output, error, len(error))
    if status: raise RuntimeError(error.value.decode())
    answer = output[..., 0].astype(np.float64) + output[..., 1].astype(np.float64)
    if not np.all(np.isfinite(answer)): raise ValueError('singular or overflowing emulated gravity result')
    acceleration, phi = answer[:, :3].copy(), answer[:, 3].copy()
    return acceleration, .5 * float(m @ phi), phi
