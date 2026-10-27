"""Symmetric FP32 pairforce/pairpotential with four chains and DS tile merge.

Both accumulated force and pairpotential are divided by true mi in CPU.
This restores pair antisymmetry before summation for unequal carrier species;
rounded symmetric mass couplings retain a separately measured FP32 budget.

Separate empirical error budget; not the existing DS1e-11 reference. Rawbinary64
positions retain3f encoding but pair subtraction is FP32 highdiff+lowdiff+taildiff.
No tree, physical pair kernel, domain truncation, or particle deletion change.
Requires measured force/invariant gates and later trajectory controls.
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
    if not Path(path).is_file(): raise RuntimeError('Explicitly build tile4_gravity.mm or set TILE4_GRAVITY_LIBRARY')
    library = ctypes.CDLL(path)
    array = np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS')
    library.tile4_gravity_kernel.argtypes = [array, ctypes.c_uint32, array, array, array,
                                             ctypes.c_char_p, ctypes.c_size_t]
    library.tile4_gravity_kernel.restype = ctypes.c_int
    library.tile4_gravity_device_name.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    library.tile4_gravity_device_name.restype = ctypes.c_char_p
    library.tile4_gravity_newton_variant.argtypes = []
    library.tile4_gravity_newton_variant.restype = ctypes.c_int
    library.tile4_gravity_abi_version.argtypes = []
    library.tile4_gravity_abi_version.restype = ctypes.c_int
    if library.tile4_gravity_abi_version() != 7:
        raise RuntimeError('Metal library ABI does not match3-component coordinate layout')
    return library


def _library():
    return _load(str(Path(os.environ.get('TILE4_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve()))


def backend_metadata():
    error = ctypes.create_string_buffer(4096)
    name = _library().tile4_gravity_device_name(error, len(error))
    if name is None: raise RuntimeError(error.value.decode())
    variant = _library().tile4_gravity_newton_variant()
    path = Path(os.environ.get('TILE4_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve()
    return dict(device=name.decode(), precision='raw3f; symmetric FP32 pairforce/pairpotential; fourDSforce chains, FP32phi chains, DSmerges; true-mass division in CPU',
                abi_version=_library().tile4_gravity_abi_version(),
                algorithm_version='raw3f/fp32-displacement/fp32-pair-tile128/four-chain-balanced/symmetric-pairforce-pairpotential/DS-force-chains/DS-merge-v4',
                pair_coupling='symmetric FP32 product of rounded particle masses',
                output_convention='DS-summed pairforce and pairpotential divided by true mass in CPU',
                newton_corrections=variant, tile_threads=128, independent_DS_force_chains=4, independent_FP32_phi_chains=4, DS_merge_frequency='once per source tile',
                library=str(path), library_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                coordinate_encoding='raw binary64 positions split into3 FP32 residual components; FP32 highdiff+lowdiff+taildiff',
                rsqrt_variant='precise FP32 inverse square root; no DS Newton correction',
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
    status = _library().tile4_gravity_kernel(packed, len(m), _split(eps * eps), _split(G),
                                              output, error, len(error))
    if status: raise RuntimeError(error.value.decode())
    receipts = output[..., 0].astype(np.float64) + output[..., 1].astype(np.float64)
    answer = receipts / m[:, None]
    if not np.all(np.isfinite(answer)): raise ValueError('singular or overflowing emulated gravity result')
    acceleration, phi = answer[:, :3].copy(), answer[:, 3].copy()
    return acceleration, .5 * float(m @ phi), phi
