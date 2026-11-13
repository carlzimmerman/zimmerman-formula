"""Pixel lens maps. Coordinates X west, N north, angles from +X toward +N."""
from pathlib import Path
import json
import numpy as np
from scipy.ndimage import map_coordinates

BASE=Path(__file__).resolve().parent

class AqualLens:
    def __init__(self,library=None):
        f=np.load(library or BASE/'library_01/library.npz')
        self.logmass=f['logmass'];self.lr=np.log(f['rad']);self.ang=f['angle'];self.maps=f['alpha']
        c=json.loads((BASE/'inputs/results/coolest_sersic.json').read_text())
        p=c['lensing_entities'][0]['light_model'][0]['parameters'];get=lambda k:p[k]['point_estimate']['value']
        self.cx=get('center_x');self.cn=get('center_y');self.angle=np.pi/2+np.deg2rad(get('phi'))
    def deflection(self,X,N,logmass,g1=0.,g2=0.,a0_ratio=1.,kappa_external=0.):
        # Exact AQUAL joint scaling maps alternative a0 to canonical library.
        m=logmass-np.log10(a0_ratio)
        if not self.logmass[0]<=m<=self.logmass[-1]:raise ValueError('mass outside field library')
        dx=X-self.cx;dn=N-self.cn;co=np.cos(self.angle);si=np.sin(self.angle)
        u=co*dx+si*dn;v=-si*dx+co*dn
        r=np.maximum(np.hypot(u,v),np.exp(self.lr[0]));t=np.arctan2(np.abs(v),np.abs(u))
        coord=np.array([np.full_like(r,(m-self.logmass[0])/(self.logmass[1]-self.logmass[0])),
           (np.log(r)-self.lr[0])/(self.lr[1]-self.lr[0]),t/(self.ang[1]-self.ang[0])])
        au=a0_ratio*map_coordinates(self.maps[:,0],coord,order=1,mode='nearest')*np.sign(u)
        av=a0_ratio*map_coordinates(self.maps[:,1],coord,order=1,mode='nearest')*np.sign(v)
        ax=co*au-si*av+g1*X+g2*N+kappa_external*X
        an=si*au+co*av+g2*X-g1*N+kappa_external*N
        return ax,an

def sie_parameters():
    c=json.loads((BASE/'inputs/results/coolest.json').read_text());v=lambda p,k:p[k]['point_estimate']['value']
    p=c['lensing_entities'][0]['mass_model'][0]['parameters'];g=c['lensing_entities'][2]['mass_model'][0]['parameters']
    gp=np.pi/2+np.deg2rad(v(g,'phi_ext'));gam=v(g,'gamma_ext')
    return dict(theta=v(p,'theta_E'),q=v(p,'q'),angle=np.pi/2+np.deg2rad(v(p,'phi')),cx=v(p,'center_x'),cn=v(p,'center_y'),g1=gam*np.cos(2*gp),g2=gam*np.sin(2*gp))

def sie_deflection(X,N,theta,q,angle,cx,cn,g1,g2):
    co=np.cos(angle);si=np.sin(angle);dx=X-cx;dn=N-cn
    u=co*dx+si*dn;v=-si*dx+co*dn;psi=np.maximum(np.sqrt(q*q*u*u+v*v),1e-10);f=np.sqrt(1-q*q)
    au=theta*np.sqrt(q)/f*np.arctan(f*u/psi);av=theta*np.sqrt(q)/f*np.arctanh(f*v/psi)
    return co*au-si*av+g1*X+g2*N,si*au+co*av+g2*X-g1*N
