"""Experimental complete-harmonic variational continuum Poisson regularization.

This finite-basis pair kernel differs from finite-epsilon Plummer and is not
admitted to production. Basis parameters stay fixed under all differentiations.
The centre is the physical mass COM; its chain-rule acceleration is included.
"""
import ctypes
from functools import lru_cache
import hashlib,importlib,os,sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
G=.004498638185693768


@lru_cache(maxsize=1)
def load_agama():
    path=Path(os.environ.get('AGAMA_CANDIDATE_DIRECTORY',HERE/'vendor/native_build_002')).resolve()
    sys.path.insert(0,str(path))
    agama=importlib.import_module('agama')
    if Path(agama.__file__).resolve().parent!=path:raise RuntimeError('Agama loaded from unexpected location')
    agama.setNumThreads(2)
    return agama


@lru_cache(maxsize=1)
def _diagonal_lib():
    path=Path(os.environ.get('SCF_DIAGONAL_LIBRARY',HERE/'vendor/diagonal_build_001/scf_diagonal.dylib')).resolve()
    lib=ctypes.CDLL(str(path));arr=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
    lib.scf_diagonal.argtypes=[arr,ctypes.c_size_t,ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,arr,arr]
    lib.scf_diagonal.restype=ctypes.c_int
    return lib


def diagonal(radius,nmax,lmax,eta,r0):
    radius=np.ascontiguousarray(radius,dtype=np.float64)
    k=np.empty_like(radius);dk=np.empty_like(radius)
    if _diagonal_lib().scf_diagonal(radius,len(radius),nmax,lmax,eta,r0,k,dk):
        raise FloatingPointError('SCF diagonal outside declared positive-radius finite domain')
    return k,dk


def gravity(x,m,nmax=32,lmax=8,r0=300.,eta=1.,self_mode='excluded'):
    x=np.ascontiguousarray(x,dtype=np.float64);m=np.ascontiguousarray(m,dtype=np.float64)
    if (m.ndim!=1 or x.shape!=(len(m),3) or len(m)<2 or not np.isfinite(x).all()
        or not np.isfinite(m).all() or np.any(m<=0) or not isinstance(nmax,int) or not 0<=nmax<=256
        or not isinstance(lmax,int) or not 0<=lmax<=64 or not np.isfinite(r0) or r0<=0
        or not np.isfinite(eta) or eta<.5 or self_mode not in ('included','excluded')):
        raise ValueError('finite positive-mass N>=2, fixed finite basis parameters required')
    centre=np.average(x,axis=0,weights=m);y=np.ascontiguousarray(x-centre)
    radius=np.linalg.norm(y,axis=1)
    if np.any(radius==0):raise ValueError('particle exactly at basis centre is outside admitted analytic-gradient domain')
    agama=load_agama()
    # Native N-body units have G=1: source masses G*m put outputs directly in
    # existing pc/Msun/Myr potential and acceleration units without changing ICs.
    pot=agama.Potential(type='BasisSet',particles=(y,G*m),symmetry='None',
        lmax=lmax,mmax=lmax,nmax=nmax,eta=eta,r0=r0)
    phi,afixed=pot.eval(y,pot=True,acc=True)
    phi=np.asarray(phi).copy();afixed=np.asarray(afixed).copy()
    if self_mode=='excluded':
        k,dk=diagonal(radius,nmax,lmax,eta,r0)
        phi-=G*m*k
        afixed+=.5*(G*m*dk/radius)[:,None]*y
    acceleration=afixed-np.average(afixed,axis=0,weights=m)
    if not np.isfinite(phi).all() or not np.isfinite(acceleration).all():
        raise FloatingPointError('nonfinite SCF field')
    return acceleration,.5*float(m@phi),phi
