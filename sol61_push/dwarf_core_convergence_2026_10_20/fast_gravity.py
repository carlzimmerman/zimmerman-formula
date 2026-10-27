"""Double-precision direct gravity; no compilation or installation on import.

Build explicitly with no fast-math and disabled FMA contraction:
  clang -O3 -ffp-contract=off -dynamiclib -pthread fast_gravity.c -o fast_gravity.dylib
Set FAST_GRAVITY_LIBRARY to use an explicitly built alternative path. The
FAST_GRAVITY_SCALAR C preprocessor flag selects the portable scalar pair loop.
Both versions use the same full 3D Plummer Hamiltonian and exact pair coverage.
Four pthreads are requested by default; set threads=1 for a serial comparison.
No bitwise trajectory identity with the historical summation order is claimed.
"""
import ctypes
from functools import lru_cache
import os
from pathlib import Path

import numpy as np


G = .004498638185693768


@lru_cache(maxsize=4)
def _load(path):
    if not Path(path).is_file():
        raise RuntimeError('Build fast_gravity.c explicitly, or set FAST_GRAVITY_LIBRARY to the built library')
    library = ctypes.CDLL(path)
    array = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
    library.fast_gravity_kernel.argtypes = [array, array, ctypes.c_size_t,
        ctypes.c_double, ctypes.c_double, ctypes.c_size_t, array, array]
    library.fast_gravity_kernel.restype = ctypes.c_int
    library.fast_gravity_simd_enabled.argtypes = []
    library.fast_gravity_simd_enabled.restype = ctypes.c_int
    return library


def backend_metadata():
    path = str(Path(os.environ.get('FAST_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve())
    library = _load(path)
    return dict(library=path, neon_double2=bool(library.fast_gravity_simd_enabled()),
                pair_law='symmetric full-3D Plummer; exact unordered pair coverage',
                summation='per-call thread-local double buffers, fixed thread-order merge')


def gravity(x, m, eps, threads=4):
    """Return acceleration, U and self-excluded per-particle potential phi.

    Units pc, Msun, Myr. U=.5*m@phi. Input positions may be noncontiguous;
    inputs are never mutated. Each invocation owns all C scratch/thread state.
    """
    x, m = np.ascontiguousarray(x, dtype=np.float64), np.ascontiguousarray(m, dtype=np.float64)
    if (x.ndim != 2 or x.shape != (len(m), 3) or m.ndim != 1
            or not np.all(np.isfinite(x)) or not np.all(np.isfinite(m)) or np.any(m <= 0.)
            or not np.isscalar(eps) or not np.isfinite(eps) or eps < 0.
            or isinstance(threads, (bool, np.bool_)) or not isinstance(threads, (int, np.integer))
            or threads < 1 or threads > 64):
        raise ValueError('finite positions(N,3), positive masses(N), eps>=0 and integer1<=threads<=64 required')
    path = str(Path(os.environ.get('FAST_GRAVITY_LIBRARY', Path(__file__).with_suffix('.dylib'))).resolve())
    library = _load(path)
    acceleration, phi = np.zeros_like(x), np.zeros(len(m), dtype=np.float64)
    status = library.fast_gravity_kernel(x, m, len(m), float(eps), G, int(threads), acceleration, phi)
    if status == 1:
        raise ValueError('singular unsoftened coincident particles')
    if status == 2:
        raise MemoryError('gravity scratch allocation or input size overflow')
    if status == 3:
        raise RuntimeError('gravity pthread creation failed')
    if status:
        raise ValueError('invalid gravity scalar parameters')
    return acceleration, .5 * float(m @ phi), phi
