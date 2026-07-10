import numpy as np, importlib.util
from scipy.interpolate import CubicSpline
spec=importlib.util.spec_from_file_location('m','methodA_ode.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
G=6.674e-11; Msun=1.989e30; AU=1.496e11
a0c=9.36e-11; Z=np.sqrt(32*np.pi/3)

def lap_l2(r,psi2):
    # l=2 Laplacian of psi2(r)*P2 :  (1/r^2)(r^2 psi2')' - 6 psi2/r^2
    lnr=np.log(r); sp=CubicSpline(lnr,psi2)
    d1=sp(lnr,1)/r                      # psi2'
    sp2=CubicSpline(lnr, r**2*d1)
    term=sp2(lnr,1)/r/r**2              # (r^2 psi2')'/r^2
    return term-6*psi2/r**2

def project_dens(r,rho2,NT=600):
    th=np.linspace(1e-4,np.pi-1e-4,NT); ST=np.sin(th); CT=np.cos(th); P2=0.5*(3*CT**2-1)
    R,TH=np.meshgrid(r,th,indexing='ij'); RHO=rho2[:,None]*P2[None,:]
    dr=np.gradient(r); dth=np.gradient(th); Wv=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(RHO*P2[None,:]/R**3*Wv))

for tag,a0 in [("canon",9.36e-11),("alt",1.13e-10)]:
    a0V=Z*a0; r_t=np.sqrt(2*G*Msun/a0V)
    gx=2.2
    r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),4000)
    S=m.setup(a0,gx,0.5)
    J2=S['Jt2_of'](r)                      # l=2 of bulk strain J = 2|g_N|/a0V
    # excess-potential weight W = h'(J0) ~ (nu(y0)-1)*r   (docstring)
    y0=S['y0'](r); W=(m.nu(y0)-1.0)*r
    psi2_scal=W*J2
    rhoD_scal=lap_l2(r,psi2_scal)
    Iscal_h=project_dens(r,rhoD_scal)
    # committed scalar anchor (div of (nu-1)g_N) for calibration
    Iscal_committed=m.scalar_committed(a0,gx)
    print(f"\n[{tag}] gx={gx}: r_t={r_t/AU:.0f}AU  Iscal(grad2[W J2])={Iscal_h:.3e}  Iscal(committed div A)={Iscal_committed:.3e}  ratio={Iscal_h/Iscal_committed:.3f}")
    for K0hat in [0.5,1.0]:
        rho_=r/r_t; kt=K0hat*np.maximum(1.0,rho_)
        for beta in [0.6,0.95]:
            Ssup=kt/(kt+4*beta)
            # w_h: suppress J2 inside the h construction
            rhoD_med=lap_l2(r,W*Ssup*J2)
            wh=project_dens(r,rhoD_med)/Iscal_h
            # wJ direct
            wJ=project_dens(r,Ssup*J2)/project_dens(r,J2)
            q2c={"canon":2.2e-26,"alt":3.0e-26}[tag]
            print(f"   K0hat={K0hat} beta={beta}: w_h(grad2[W S J2])={wh:.3f} -> Q2={wh*q2c:.2e}  ({'PASS' if wh*q2c<5.2e-27 else 'FAIL x%.2f'%(wh*q2c/5.2e-27)})   [wJ_direct={wJ:.3f}]")
