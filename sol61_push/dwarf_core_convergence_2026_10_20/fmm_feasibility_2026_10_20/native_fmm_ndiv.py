"""Research-only leaf occupancy tuning of unchanged upstream raw Laplace FMM."""
import ctypes as ct
import numpy as np
from native_fmm import _library,G


def gravity(x,m,tolerance=1e-12,ndiv=4000):
    x=np.ascontiguousarray(x,dtype=np.float64);m=np.ascontiguousarray(m,dtype=np.float64)
    if (m.ndim!=1 or x.shape!=(len(m),3) or not len(m) or not np.isfinite(x).all()
        or not np.isfinite(m).all() or np.any(m<=0) or not 0<tolerance<1
        or not isinstance(ndiv,int) or ndiv<1):raise ValueError('invalid finite raw FMM domain')
    lib,_=_library();lib.omp_set_num_threads(4)
    i8=ct.POINTER(ct.c_int64);d=ct.POINTER(ct.c_double)
    arr=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
    fn=lib.lfmm3d_ndiv_
    fn.argtypes=[i8,d,i8,arr,i8,arr,i8,arr,i8,i8,arr,arr,arr,i8,arr,i8,arr,arr,arr,i8,i8,i8,arr,i8]
    fn.restype=None
    def integer(n):return ct.c_int64(n)
    nd,n,chargeflag,dipflag,iper,pg,nt,pgt,leaf,divflag,near,ier=map(integer,[1,len(m),1,0,0,2,0,0,ndiv,0,1,-1])
    tol=ct.c_double(tolerance);charge=np.ascontiguousarray(4*np.pi*G*m)
    pot=np.zeros(len(m));a=np.zeros_like(x);hess=np.zeros(6);dummy=np.zeros(6);dip=np.zeros(3);timing=np.zeros(6)
    ref=ct.byref
    fn(ref(nd),ref(tol),ref(n),x,ref(chargeflag),charge,ref(dipflag),dip,ref(iper),ref(pg),pot,a,hess,
        ref(nt),dummy,ref(pgt),dummy,dummy,dummy,ref(leaf),ref(divflag),ref(near),timing,ref(ier))
    if ier.value:raise RuntimeError('FMM error%d'%ier.value)
    phi=-pot
    if not np.isfinite(a).all() or not np.isfinite(phi).all():raise FloatingPointError('nonfinite FMM output')
    return a,.5*float(m@phi),phi
