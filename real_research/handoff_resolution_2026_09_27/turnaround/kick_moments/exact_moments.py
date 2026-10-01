"""Exact conditional isotropic kick moments, same one-daughter closure as CFG5."""
import numpy as np

def kick_moments(vr, vt, phi, vk, mutate=False):
    vr,vt,phi=np.broadcast_arrays(np.asarray(vr,float),np.asarray(vt,float),np.asarray(phi,float))
    if vk<0: raise ValueError('kick speed must be nonnegative')
    speed=np.hypot(vr,vt);den=2*vk*speed
    c=np.zeros_like(speed)
    np.divide(-2*phi-speed**2-vk**2,den,out=c,where=den>0)
    c=np.clip(c,-1,1)
    fb=(c+1)/2
    # Zero speed or zero kick: every direction has identical total energy.
    fb=np.where(den==0,(.5*(speed**2+vk**2)+phi<=0).astype(float),fb)
    m1=(c-1)/2;m2=(c*c-c+1)/3
    if mutate:m1=np.zeros_like(m1)
    er=np.divide(vr,speed,out=np.zeros_like(vr),where=speed>0)
    et=np.divide(vt,speed,out=np.zeros_like(vt),where=speed>0)
    aa=(1-m2)/2;dd=(3*m2-1)/2
    nr2=aa+dd*er**2;nt2=2*aa+dd*et**2
    nr2=np.where(speed==0,1/3,nr2);nt2=np.where(speed==0,2/3,nt2)
    radial=vr**2+2*vk*vr*m1*er+vk**2*nr2
    tangential=vt**2+2*vk*vt*m1*et+vk**2*nt2
    # Empty conditional population has no moments: engine ignores these zero placeholders.
    return 1-fb,np.where(fb>0,np.maximum(radial,0),0),np.where(fb>0,np.maximum(tangential,0),0)
