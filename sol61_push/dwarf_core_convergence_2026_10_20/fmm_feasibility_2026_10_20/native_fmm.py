"""Experimental raw-Laplace native ctypes bridge, not production softening.

Original production Python and IC generation can use this native ABI unchanged.
Four OpenMP threads are set explicitly for each call; this module is scoped to
serial invocation from this feasibility process, not concurrent Python clients.
Coincident distinct sources are outside this raw singular-kernel probe's domain;
upstream also omits separations below 2**-51 times the global bounding-box edge.
"""
import ctypes
from functools import lru_cache
import hashlib
import os
from pathlib import Path
import numpy as np

G=.004498638185693768
HERE=Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def _library():
    path=Path(os.environ.get('NATIVE_FMM_LIBRARY',HERE/'native_build_003/libfmm3d.dylib')).resolve()
    lib=ctypes.CDLL(str(path))
    arr=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
    i8=ctypes.POINTER(ctypes.c_int64); dbl=ctypes.POINTER(ctypes.c_double)
    lib.lfmm3d_s_c_g_.argtypes=[dbl,i8,arr,arr,arr,arr,i8]
    lib.lfmm3d_s_c_g_.restype=None
    lib.omp_set_dynamic.argtypes=[ctypes.c_int];lib.omp_set_dynamic.restype=None
    lib.omp_set_num_threads.argtypes=[ctypes.c_int];lib.omp_set_num_threads.restype=None
    lib.omp_get_max_threads.argtypes=[];lib.omp_get_max_threads.restype=ctypes.c_int
    lib.omp_set_dynamic(0); lib.omp_set_num_threads(4)
    return lib,path


def metadata():
    lib,path=_library()
    return dict(library=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                openmp_max_threads=lib.omp_get_max_threads(),source_tag='v2.1.0',
                regularization='none: unsoftened Laplace; not admitted to production')


def gravity(x,m,tolerance=1e-12):
    x=np.ascontiguousarray(x,dtype=np.float64);m=np.ascontiguousarray(m,dtype=np.float64)
    if (m.ndim!=1 or x.shape!=(len(m),3) or not np.isfinite(x).all() or not np.isfinite(m).all()
            or np.any(m<=0) or not np.isfinite(tolerance) or not 0<tolerance<1):
        raise ValueError('finite x(N,3), positive finite m(N), tolerance in(0,1) required')
    if not len(m):return x.copy(),0.,m.copy()
    lib,_=_library();lib.omp_set_num_threads(4)
    n=ctypes.c_int64(len(m));tol=ctypes.c_double(tolerance);ier=ctypes.c_int64(-1)
    charge=np.ascontiguousarray(4*np.pi*G*m)
    potential=np.zeros(len(m));acceleration=np.zeros_like(x)
    # C x(N,3) is the exact contiguous storage of Fortran source(3,N).
    lib.lfmm3d_s_c_g_(ctypes.byref(tol),ctypes.byref(n),x,charge,potential,acceleration,ctypes.byref(ier))
    if ier.value:raise RuntimeError('FMM error %d'%ier.value)
    phi=-potential
    if not np.isfinite(acceleration).all() or not np.isfinite(phi).all():raise FloatingPointError('nonfinite FMM output')
    return acceleration,.5*float(m@phi),phi
