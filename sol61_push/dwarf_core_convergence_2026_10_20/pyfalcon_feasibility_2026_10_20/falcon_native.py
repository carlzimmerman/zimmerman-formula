"""Explicitly built binary64 full3D falcON P0 Plummer, with no installation.

FALCON_NATIVE_LIBRARY must name an admitted local library. Upstream defaults
float/P1 are never used. The approximation has a theta opening criterion and
compile-time expansion order, not a rigorous tolerance. Direct mode is a small-N
reference. Native calls are serialized because upstream reentrancy is unaudited.
No NumPy/Python version or input phase-space normalization is changed.
"""
import ctypes
from functools import lru_cache
import hashlib
import os
from pathlib import Path
import threading
import numpy as np

G = .004498638185693768
_lock = threading.RLock()


@lru_cache(maxsize=4)
def _load(path):
    library = ctypes.CDLL(path)
    array = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
    library.falcon_gravity.argtypes = [array, array, ctypes.c_uint, ctypes.c_double,
        ctypes.c_double, ctypes.c_double, ctypes.c_int, array, array, ctypes.c_char_p, ctypes.c_uint]
    library.falcon_gravity.restype = ctypes.c_int
    library.falcon_real_bytes.argtypes = []; library.falcon_real_bytes.restype = ctypes.c_int
    library.falcon_expansion_order.argtypes = []; library.falcon_expansion_order.restype = ctypes.c_int
    if library.falcon_real_bytes() != 8:
        raise RuntimeError('binary64 falcON required; upstream float build forbidden')
    return library


def _path():
    if 'FALCON_NATIVE_LIBRARY' not in os.environ:
        raise RuntimeError('explicit FALCON_NATIVE_LIBRARY required; no hidden default build')
    return str(Path(os.environ['FALCON_NATIVE_LIBRARY']).resolve())


def backend_metadata():
    path = _path(); library = _load(path)
    return dict(real_bytes=library.falcon_real_bytes(), expansion_order=library.falcon_expansion_order(),
        kernel='P0 Plummer, hardcoded', library=path, library_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        upstream='GalacticDynamics-Oxford/pyfalcon', upstream_commit='d2e2e05acb377d21b9a87d94aa8b283f52f39fca',
        license='GPL-2.0-or-later (upstream source headers)',
        method='full3D mutual cell-cell Cartesian Taylor tree/FMM; all active; rebuilt each call',
        approximation='theta mass-dependent opening criterion; empirical accuracy/conservation checks required')


def gravity(x, m, eps, theta=.5, direct=False):
    x, m = np.ascontiguousarray(x, dtype=np.float64), np.ascontiguousarray(m, dtype=np.float64)
    if (m.ndim != 1 or x.shape != (m.size, 3) or len(m) > 1000000
            or not np.all(np.isfinite(x)) or not np.all(np.isfinite(m)) or np.any(m <= 0.)
            or not np.isscalar(eps) or not np.isfinite(eps) or eps < 0.
            or not np.isscalar(theta) or not np.isfinite(theta) or not 0 < theta < 1.):
        raise ValueError('finite x(N,3), positive m(N), eps>=0 and0<theta<1 required')
    a, phi = np.zeros_like(x), np.zeros(len(m))
    if len(m) < 2:
        return a, 0., phi
    error = ctypes.create_string_buffer(4096)
    with _lock:
        status = _load(_path()).falcon_gravity(x, m, len(m), float(eps), float(theta), G,
                                               bool(direct), a, phi, error, len(error))
    if status:
        raise RuntimeError(error.value.decode())
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(phi)):
        raise RuntimeError('nonfinite falcON force or potential')
    return a, .5 * float(m @ phi), phi
