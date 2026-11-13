"""Axisymmetric, isolated, UNSCREENED AQUAL lensing, not the complete v3s action.

rho follows an oblate Abel-deprojected Sersic profile with constant M/L.
Coordinates of projected maps: u major axis, v minor axis, units arcsec.
The adopted metric has equal weak-field potentials. alpha=2/c^2 int grad_perp Phi dz.
No algebraic non-spherical MOND approximation is used.
"""
import importlib.util
from pathlib import Path
import numpy as np
from scipy.special import gammaincinv, gammaln
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import quad

BASE = Path(__file__).resolve().parent
SOLVER = BASE.parent / 'closure_2026_11_06/QX4_udg/aqual.py'
spec = importlib.util.spec_from_file_location('fv_aqual', SOLVER)
fv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fv)
C = 299792.458
ARCSEC = 206264.80624709636
G = fv.G

def geometry(zl=.986, zs=3.773, h0=67.74, om=.3089):
    def dc(z):
        return C/h0*quad(lambda zz: 1/np.sqrt(om*(1+zz)**3+1-om),0,z,
                         epsabs=1e-10,epsrel=1e-11)[0]
    dl, ds = dc(zl), dc(zs)
    return dl/(1+zl)*1000/ARCSEC, (ds-dl)/ds

def spherical_density_table(n, nodes=256):
    """rho(r) for M=Re=1 via direct Abel integral, then log interpolation."""
    logr = np.linspace(-10, 7, 5000)
    r = np.exp(logr)
    b = gammaincinv(2*n,.5)
    z,w = np.polynomial.legendre.leggauss(nodes)
    t=(z+1)*np.pi/4; w=w*np.pi/4
    # Sigma0=b^(2n)/(2pi n Gamma(2n)); Abel rho=-int Sigma'/sqrt/pi.
    logpref=2*n*np.log(b)-np.log(2*np.pi*n)-gammaln(2*n)+np.log(b/(np.pi*n))
    sec=1/np.cos(t)
    val=np.exp(logpref+(1/n-1)*logr)*np.sum(w[None,:]*sec[None,:]**(1/n)*
        np.exp(-b*(r[:,None]*sec[None,:])**(1/n)),axis=1)
    return logr,np.log(np.maximum(val,1e-300))

def make_field(mass, re_major, n, qi, a0=9.3603e-11, nr=192, nt=48,
               rmax_re=500., rmin_re=1e-5, tol=2e-8, mu_one=False):
    """Return potential and gradients. M cell convention is hemisphere mass."""
    grid=fv.Grid(re_major*rmin_re,re_major*rmax_re,nr,nt,p=1)
    lr,ld=spherical_density_table(n)
    def rho(R,z):
        m=np.sqrt(R*R+(z/qi)**2)/re_major
        return mass/(qi*re_major**3)*np.exp(np.interp(np.log(m),lr,ld))
    cells=grid.deposit(rho,nsub=5)
    enclosed=2*cells.sum()
    # Quadrature deposition error is reported, never normalized away silently.
    phi,res,it=fv.solve(grid,cells,fv.a0_kpc(a0),mu_one=mu_one,tol=tol,maxit=240)
    if not np.isfinite(phi).all() or res>tol:
        raise RuntimeError(f'AQUAL solve did not converge: residual={res}, iterations={it}')
    gr,gt=fv._gradients(grid,phi)
    return dict(grid=grid,phi=phi,gr=gr,gt=gt,mass=mass,re=re_major,n=n,qi=qi,
                a0=a0,residual=res,iterations=it,deposited_mass=enclosed,mu_one=mu_one)

def projected_deflection(field,u,v,inclination=90.,zl=.986,zs=3.773,nlos=192):
    """Reduced deflection in arcsec. LOS spherical tail extends to infinity.

    Spherical-gradient continuation beyond grid suppresses unknown angular
    multipoles there; grid-radius convergence must bound that truncation.
    """
    g=field['grid']; scale,ratio=geometry(zl,zs)
    u,v=np.broadcast_arrays(u,v); shape=u.shape
    U=u.ravel()*scale; V=v.ravel()*scale
    impact=np.maximum(np.hypot(U,V),g.rc[0]*2)
    z,w=np.polynomial.legendre.leggauss(nlos)
    t=z*np.pi/2; weight=w*np.pi/2
    los=impact[:,None]*np.tan(t)[None,:]
    jac=impact[:,None]/np.cos(t)[None,:]**2
    si=np.sin(np.deg2rad(inclination)); co=np.cos(np.deg2rad(inclination))
    zy=V[:,None]*si+los*co
    cyl_y=los*si-V[:,None]*co
    cyl_r=np.sqrt(U[:,None]**2+cyl_y**2)
    radius=np.sqrt(cyl_r**2+zy**2)
    th=np.arctan2(cyl_r,np.abs(zy))
    # Include symmetry faces; gradient theta vanishes there.
    tc=np.r_[0,g.tc,np.pi/2]
    grpad=np.column_stack((field['gr'][:,0],field['gr'],field['gr'][:,-1]))
    gtpad=np.column_stack((np.zeros(g.nr),field['gt'],np.zeros(g.nr)))
    coords=np.column_stack((np.clip(np.log(radius.ravel()),g.xc[0],g.xc[-1]),th.ravel()))
    gr=RegularGridInterpolator((g.xc,tc),grpad)(coords).reshape(radius.shape)
    gt=RegularGridInterpolator((g.xc,tc),gtpad)(coords).reshape(radius.shape)
    outside=radius>g.rc[-2]
    gn=G*field['mass']/radius[outside]**2
    gr[outside]=gn if field['mu_one'] else .5*(gn+np.sqrt(gn**2+4*fv.a0_kpc(field['a0'])*gn))
    gt[outside]=0
    # g_theta basis (cos theta, -sin theta), then reflect z hemisphere.
    grc=gr*np.sin(th)+gt*np.cos(th)
    gz=(gr*np.cos(th)-gt*np.sin(th))*np.sign(zy)
    gu=grc*U[:,None]/np.maximum(cyl_r,1e-100)
    gv=-co*grc*cyl_y/np.maximum(cyl_r,1e-100)+si*gz
    factor=2/C**2*ratio*ARCSEC
    au=factor*np.sum(gu*jac*weight,axis=1)
    av=factor*np.sum(gv*jac*weight,axis=1)
    return au.reshape(shape),av.reshape(shape)

def polar_map(field, inclination=90., nr=110, na=49,nlos=192):
    rad=np.geomspace(.006,12.,nr); angle=np.linspace(0,np.pi/2,na)
    u=rad[:,None]*np.cos(angle); v=rad[:,None]*np.sin(angle)
    au,av=projected_deflection(field,u,v,inclination,nlos=nlos)
    return rad,angle,au,av

def spherical_abel_alpha(mass,re,n,theta,a0=9.3603e-11):
    """Independent radial reference from derivative of exact Abel mass table."""
    from scipy.integrate import cumulative_trapezoid
    lr,ld=spherical_density_table(n,nodes=512)
    r=np.exp(lr)
    mf=cumulative_trapezoid(4*np.pi*np.exp(ld)*r**3,lr,initial=0)
    scale,ratio=geometry()
    z,w=np.polynomial.legendre.leggauss(512); t=(z+1)*np.pi/4; w*=np.pi/4
    radius=np.asarray(theta)[...,None]*scale/np.cos(t)
    mfrac=np.interp(np.log(radius/re),lr,mf,right=1)
    gn=G*mass*mfrac/radius**2
    acceleration=.5*(gn+np.sqrt(gn**2+4*fv.a0_kpc(a0)*gn))
    return 4*np.asarray(theta)*scale/C**2*ratio*ARCSEC*np.sum(acceleration/np.cos(t)*w,axis=-1)
