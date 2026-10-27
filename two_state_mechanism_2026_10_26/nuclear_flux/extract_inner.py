"""Read UKRmol int64/real64 sequential files; preserve Q/P block evidence."""
from scipy.io import FortranFile
import numpy as np

def read_ci(path):
    f=FortranFile(path,'r');header=f.read_record('u1').tobytes();assert b'CIDATA' in header
    meta=f.read_record('u1').tobytes();nnuc,ncsf,nstat,irrep=np.frombuffer(meta[136:168],dtype='<i8');e0=np.frombuffer(meta[192:200],dtype='<f8')[0]
    assert ncsf==nstat
    for _ in range(nnuc):f.read_record('u1')
    rec=f.read_record('u1').tobytes();phase=np.frombuffer(rec[:8*ncsf],dtype='<i8');E=np.frombuffer(rec[8*ncsf:8*(ncsf+nstat)],dtype='<f8')+e0
    vectors=[]
    for i in range(nstat):
        rec=f.read_record('u1').tobytes();idx=np.frombuffer(rec[:8],dtype='<i8')[0];assert idx==i+1
        vectors.append(np.frombuffer(rec[8:],dtype='<f8').copy())
    U=np.array(vectors).T;assert np.max(abs(U.T@U-np.eye(nstat)))<1e-10
    return E,U,phase

def read_boundary(path):
    f=FortranFile(path,'r');f.read_record('u1');f.read_record('u1');nt,nv,nd,nch=f.read_ints('<i8');f.read_record('u1')
    meta=f.read_record('u1').tobytes();ism,nstat,npole,ibut=np.frombuffer(meta[:32],dtype='<i8');radius=np.frombuffer(meta[32:],dtype='<f8')[0];assert ibut==0 and npole==0
    if ism:cf=f.read_reals('<f8')
    E=f.read_reals('<f8');W=f.read_reals('<f8').reshape((nstat,nch)).T
    return E,W,radius
