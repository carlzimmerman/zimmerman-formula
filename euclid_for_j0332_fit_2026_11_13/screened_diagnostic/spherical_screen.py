"""Bounded smooth spherical screened-v3s weak-field diagnostic.

Adapt QX17C's conservative radial P equation to exact Abel-deprojected Sersic
mass and the adopted Pi6/Pi2 C4 blend. This is NOT a covariant/oblate fit.
Only this folder is written. Run with the fit venv, python -B.
"""
import hashlib
import argparse
import json
import sys
import time
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid,quad
from scipy.interpolate import PchipInterpolator
from scipy.linalg import solve_banded
from scipy.special import gammainc,gammaincinv, gammaln

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from aqual_lensing import geometry

G,C,MSUN,PC = 6.67430e-11,299792458.,1.98847e30,3.085677581491367e16
A0 = 9.3603e-11
MASS = 1.1e12*MSUN
RE = 10.366696039493778*1000*PC
N = 5.868719099803722
RHO_DE = 4*A0*A0/(C*C*G)  # the stated kappa=1/2 vacuum postulate
A = 734183424/8922115
B = 3165142806/44610575
KNOTS = [0.,.5,.625,.9,1.]
GX,GW = np.polynomial.legendre.leggauss(8)  # exact through degree15


def smoothstep(t):
    return t**5*(126-420*t+540*t*t-315*t**3+70*t**4)


def fpp(q):
    q = np.asarray(q)
    val = np.zeros_like(q,dtype=float)
    small = (q>0)&(q<=.5)
    val[small] = A*q[small]**4
    middle = (q>.5)&(q<1)
    x = 2*q[middle]-1
    val[middle] = (A*q[middle]**4*(1-smoothstep(np.minimum(x/.25,1)))
        +B*x**5*(1-x)**5+smoothstep(np.maximum((x-.8)/.2,0)))
    val[q>=1] = 1.
    return val


def fp(q):
    q = np.asarray(q,dtype=float)
    val = np.zeros_like(q)
    val[q>=1] = q[q>=1]
    small = (q>0)&(q<=.5)
    val[small] = A/5*q[small]**5
    middle = (q>.5)&(q<1)
    if np.any(middle):
        end = q[middle]
        total = np.zeros_like(end)
        for lo,hi in zip(KNOTS[:-1],KNOTS[1:]):
            right = np.clip(end,lo,hi)
            width = right-lo
            sample = lo+width[:,None]*(GX+1)/2
            total += width/2*np.sum(fpp(sample)*GW,axis=1)
        val[middle] = total
    return val


def mass_table():
    lr = np.linspace(-25,10,24000)
    r = np.exp(lr)
    b = gammaincinv(2*N,.5)
    z,w = np.polynomial.legendre.leggauss(512)
    t = (z+1)*np.pi/4
    w = w*np.pi/4
    sec = 1/np.cos(t)
    pref = 2*N*np.log(b)-np.log(2*np.pi*N)-gammaln(2*N)+np.log(b/(np.pi*N))
    # Batch to bound memory while resolving the central Abel density.
    rho = np.empty_like(r)
    for first in range(0,len(r),1000):
        sl=slice(first,first+1000)
        rho[sl] = np.exp(pref+(1/N-1)*lr[sl])*np.sum(w*sec**(1/N)*
            np.exp(-b*(r[sl,None]*sec)**(1/N)),axis=1)
    mf = cumulative_trapezoid(4*np.pi*rho*r**3,lr,initial=0)
    return lr,mf


LR,MF = mass_table()


def mfrac(r):
    return np.interp(np.log(np.maximum(r/RE,np.exp(LR[0]))),LR,MF,right=1.)


def law_y(gn):
    # Stable positive root for excess acceleration/a0, not total g/a0.
    return 2*gn/(gn+np.sqrt(gn*gn+4*gn))


def exact_abel_mass(x):
    """Orthogonal enclosed-mass angular-kernel quadrature."""
    t0=gammaincinv(2*N,.5)*x**(1/N)
    shape=2*N+1
    def integrand(t):
        u=min(1.,(t0/t)**N)
        bracket=(2*u**3/3+u**5/5+3*u**7/28) if u<.01 else (
            np.arcsin(u)-u*np.sqrt(max(0.,1-u*u)))
        return 2/np.pi*bracket*np.exp((shape-1)*np.log(t)-t-gammaln(shape))
    return gammainc(shape,t0)+quad(integrand,t0,np.inf,epsabs=1e-12,epsrel=1e-10)[0]


class Problem:
    def __init__(self,L_pc,npd=350,rout_mpc=30.,blend=True):
        self.L=L_pc*PC
        self.blend=blend
        self.zb=4*np.pi*G*self.L*RHO_DE/A0
        rmin=RE*1e-8
        outer=rout_mpc*1e6*PC
        r=np.r_[0.,np.geomspace(rmin,outer,int(npd*np.log10(outer/rmin))+1)]
        self.s=r/self.L
        s=self.s
        self.h=np.diff(s)
        self.sm2=(s[:-1]**2+s[:-1]*s[1:]+s[1:]**2)/3
        self.H=(s[2:]-s[:-2])/2
        self.gn=np.r_[0.,G*MASS*mfrac(r[1:])/r[1:]**2/A0]
        self.ys=np.r_[0.,law_y(self.gn[1:])]
        self.r=r

    def quantities(self,y):
        z=np.diff(self.s**2*y)/(self.h*self.sm2)
        if not self.blend:
            return z,np.maximum(z,0.),np.where(z>0,1.,0.)
        return z,self.zb*fp(z/self.zb),fpp(z/self.zb)

    def residual(self,y):
        z,t,f2=self.quantities(y)
        delta=y[1:-1]-self.ys[1:-1]
        restoring=2*delta*(1/((1-y[1:-1])*(1-self.ys[1:-1]))-1)
        r=(t[1:]-t[:-1])/self.H-restoring
        scale=(np.abs(t[1:])+np.abs(t[:-1]))/self.H+2*self.gn[1:-1]+2*np.abs(y[1:-1])+1e-30
        return np.r_[r,y[-1]-self.ys[-1]],np.r_[scale,1.],f2

    def jacobian(self,y,f2):
        s,h,sm2,H=self.s,self.h,self.sm2,self.H
        count=len(s)-1
        diag=np.ones(count)
        upper=np.zeros(count-1)
        lower=np.zeros(count-1)
        i=np.arange(1,len(s)-1)
        cp=f2[1:]/(h[1:]*sm2[1:]*H)
        cm=f2[:-1]/(h[:-1]*sm2[:-1]*H)
        diag[:-1]=-s[i]**2*(cp+cm)-2*(1/(1-y[i])**2-1)
        upper[:]=cp*s[i+1]**2
        lower[:-1]=cm[1:]*s[i[1:]-1]**2
        ab=np.zeros((3,count))
        ab[0,1:]=upper
        ab[1]=diag
        ab[2,:-1]=lower
        return ab

    def solve(self):
        y=self.ys.copy()
        for it in range(120):
            residual,scale,f2=self.residual(y)
            error=np.max(np.abs(residual)/scale)
            if error<1e-12:
                break
            step=solve_banded((1,1),self.jacobian(y,f2),-residual)
            damping=1.
            accepted=False
            for _ in range(50):
                trial=y.copy()
                trial[1:]+=damping*step
                if np.all((trial[1:]>0)&(trial[1:]<1)):
                    rr,ss,_=self.residual(trial)
                    ee=np.max(np.abs(rr)/ss)
                    if np.isfinite(ee) and ee<error:
                        y=trial
                        accepted=True
                        break
                damping/=2
            if not accepted:
                raise RuntimeError(f'Newton stagnation L={self.L/PC},it={it},error={error}')
        self.y=y
        self.error=float(np.max(np.abs(self.residual(y)[0])/self.residual(y)[1]))
        self.iterations=it
        if self.error>=1e-12:
            raise RuntimeError(f'Newton failed {self.error}')
        self.ratio=PchipInterpolator(np.log(self.r[1:]),y[1:]/self.ys[1:],extrapolate=False)
        return self

    def acceleration(self,r):
        r=np.asarray(r)
        gn=G*MASS*mfrac(r)/r**2/A0
        ratio=np.where(r<=self.r[-1],self.ratio(np.log(np.clip(r,self.r[1],self.r[-1]))),1.)
        return A0*(gn+law_y(gn)*ratio)

    def deflection(self,R,nlos=512):
        z,w=np.polynomial.legendre.leggauss(nlos)
        t=(z+1)*np.pi/4
        w=w*np.pi/4
        rr=R[:,None]/np.cos(t)
        gn=G*MASS*mfrac(rr)/rr**2
        reference=.5*(gn+np.sqrt(gn**2+4*A0*gn))
        actual=self.acceleration(rr)
        integral=lambda g:4*R/C**2*np.sum(g/np.cos(t)*w,axis=1)
        return integral(actual),integral(reference)


def main(output):
    output.mkdir(parents=True,exist_ok=True)
    paths=[Path(__file__).resolve(),BASE/"aqual_lensing.py",
        BASE.parent/"closure_2026_11_06/QX17C_fd_spherical_solver/qx17c.py",
        BASE.parent/"action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/form.json"]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p):sha(p) for p in paths}
    # Moment checks: f'(1)=1, f(1)=1/2, exact quadratic continuation.
    f1=0.;f0=0.
    for lo,hi in zip(KNOTS[:-1],KNOTS[1:]):
        xx=lo+(hi-lo)*(GX+1)/2
        f1+=(hi-lo)/2*np.sum(GW*fpp(xx))
        f0+=(hi-lo)/2*np.sum(GW*(1-xx)*fpp(xx))
    assert abs(f1-1)<1e-12 and abs(f0-.5)<1e-12
    assert abs(MF[-1]-1)<2e-5
    theta=np.array([.5,1.,1.5,2.,3.])
    R=theta*geometry()[0]*1000*PC
    rows=[]
    for L,npd,outer in [(21.7,350,30),(21.7,700,30),(21.7,350,100),
                        (100.,350,30),(100.,700,30),(1000.,350,30),(1000.,700,30),
                        (1000.,350,100),(.1,350,30)]:
        start=time.monotonic()
        problem=Problem(L,npd,outer).solve()
        alpha,ref=problem.deflection(R)
        gn=G*MASS*mfrac(R)/R**2
        gref=.5*(gn+np.sqrt(gn**2+4*A0*gn))
        z,t,f2=problem.quantities(problem.y)
        at=problem.acceleration(R)
        alpha_fine,ref_fine=problem.deflection(R,nlos=1024)
        # Local small-L asymptotic check, independently using log-r derivatives.
        hh=.01
        def ys_at(r):
            return law_y(G*MASS*mfrac(r)/r**2/A0)
        ym,yc,yp=ys_at(R*np.exp(-hh)),ys_at(R),ys_at(R*np.exp(hh))
        vector_laplacian=((yp-2*yc+ym)/hh**2+(yp-ym)/(2*hh)-2*yc)/R**2
        delta_y=.5*problem.L**2*vector_laplacian/(1/(1-yc)**2-1)
        perturbative_force_fraction=A0*delta_y/gref
        # Integral Pi mass telescopes to r²P, independently checking feedback.
        integral=np.cumsum(problem.sm2*problem.h*z)
        mass_flux=problem.s[1:]**2*problem.y[1:]
        flux_error=np.max(np.abs(integral-mass_flux)/np.maximum(np.abs(mass_flux),1e-30))
        # Constitutive-force imbalance directly from the solved face fluxes.
        derivative=np.diff(t)/problem.H
        target=2*(problem.y[1:-1]/(1-problem.y[1:-1])-problem.gn[1:-1]-problem.y[1:-1])
        row={"Lstar_pc":L,"nodes_per_decade":npd,"outer_Mpc":outer,
            "nodes":len(problem.s),"iterations":problem.iterations,"scaled_residual":problem.error,
            "theta_arcsec":theta.tolist(),"impact_kpc":(R/(1000*PC)).tolist(),
            "force_fraction_change":(at/gref-1).tolist(),
            "deflection_fraction_change":(alpha/ref-1).tolist(),
            "LOS512_vs1024_fraction_change_difference":float(np.max(np.abs(alpha/ref-alpha_fine/ref_fine))),
            "local_small_L_force_fraction_prediction":perturbative_force_fraction.tolist(),
            "phantom_mass_telescoping_max_relative_error":float(flux_error),
            "min_charge_ratio_Pi_over_b":float((z/problem.zb).min()),
            "max_charge_ratio_Pi_over_b":float((z/problem.zb).max()),
            "charge_ratio_at_impacts":np.interp(R,(problem.r[1:]+problem.r[:-1])/2,z/problem.zb).tolist(),
            "max_covar_constitutive_prefactor_gammaFprime_over_c2":float(np.max(A0*problem.L/(2*C*C)*t)),
            "weak_constitutive_raw_difference_max":float(np.max(np.abs(derivative-target))),
            "seconds":time.monotonic()-start}
        rows.append(row)
        print(json.dumps(row),flush=True)
    raw=Problem(21.7,350,30,blend=False).solve()
    raw_alpha,raw_ref=raw.deflection(R)
    blend_raw_difference=(raw_alpha/raw_ref-1)-np.asarray(rows[0]["deflection_fraction_change"])
    # Independent exact-Abel enclosed-mass crosscheck at the five impact radii.
    mass_exact=np.array([exact_abel_mass(float(x/RE)) for x in R])
    mass_comparison=mfrac(R)/mass_exact-1
    assert np.max(np.abs(mass_comparison))<2e-6
    assert max(x['phantom_mass_telescoping_max_relative_error'] for x in rows)<1e-10
    after={str(p):sha(p) for p in paths}
    assert before==after
    result={"assertion_tested":"Conservative spherical weak-field screened P-sector solution for one smooth Sersic baryonic profile, adopted Pi6/Pi2 blend, named Lstar/grid/domain fixtures",
        "non_claims":["Not full covariant/PN v3s","Not oblate/image fit","No granularity or external field","No uniform error bound for all allowed Lstar","Not empirical theory pass/fail"],
        "mass_Msun":MASS/MSUN,"Re_kpc":RE/(1000*PC),"sersic_n":N,"a0":A0,
        "rho_DE_kg_m3":RHO_DE,"mass_table_total_fraction":float(MF[-1]),
        "blend_checks":{"integral_fpp":f1,"integral_1_minus_q_fpp":f0},
        "mass_table_vs_direct_exact_Abel_relative_error_at_impacts":mass_comparison.tolist(),
        "raw_quadratic_minus_adopted_blend_deflection_fraction_at_floorL":blend_raw_difference.tolist(),
        "inputs_sha256_before":before,"inputs_sha256_after":after,"runs":rows,
        "tail_prescription":"For r beyond numerical outer radius use unscreened isolated spherical force; vary outer radius to diagnose this boundary approximation",
        "status":"completed"}
    (output/"result.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE)
    main(parser.parse_args().output)
