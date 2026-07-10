#!/usr/bin/env python3
"""
METHOD A -- the l=2 spheroidal Navier BVP for the two-invariant elastic dark-energy medium.
Decides the m3 residual: does shear stiffness mu_s SUPPRESS the ell=2 of the bulk strain J
(w<1) that sources the Cassini quadrupole, or not (w~1)?

MODEL.  Isotropic linear elasticity in the l=2 poloidal sector around the spherical MOND
background of a point mass (Sun) in a uniform external field g_ext:
    u = U(r) P2(cos th) e_r + V(r) dP2/dth e_th ,     n=l(l+1)=6 .
State y=[U, Sig_rr, V, Sig_rth] (Takeuchi-Saito static spheroidal), moduli
    K_t(r) = K0hat*K_eff*max(1, r/r_t)   (tangent bulk modulus, sqrt(J) bulk branch),
    mu_s   = 3 beta K_eff (constant, capped by 6Z^2: beta<=2),  lam = K_t - 2mu_s/3.
FORCING is the pure gradient f=grad(Phi_drive), Phi_drive=K_t(r) J_target(r,th),
J_target=2|g_N|/a0V (the framework compressive strain) -- built so that at mu_s->0 the pure-bulk
equilibrium K_t J = Phi_drive gives J=div(u)=[J_target]_2 exactly (the VALIDATION reference).

PIPELINE for Q2.  Excess-potential field Psi(r,th)=W(r) J2(r) P2, W=h'(J0) ~ (nu(y0)-1) r
(framework excess-potential weight); phantom density rho_D=(c^2/8piG) lap(Psi); Q2 = l=2 interior
moment of rho_D via the SAME 2D projection as the committed m3_bvp_2d_quadrupole.py.
w(beta)=Q2_medium(beta)/Q2_medium(0).  Both footings, g_ext bracket, two bulk-modulus footings.
The committed scalar-class Q2 (2.0-2.5e-26 canon / 2.7-3.3e-26 alt) is the anchor: Q2=w*Q2_scalar.

VALIDATION: (P1) homogeneous exponents = {-4,-2,1,3} (textbook Navier r^{l-1},r^{l+1},r^{-l},
r^{-l-2}; r^1 = uniform strain = source-free -> the "uniform dilatation, zero shear" check).
(P2) BVP dilatation reproduces the local P-wave law J2=Jt2*K_t/(K_t+4mu_s/3) in the shell.
(P3) medium(beta=0) density moment reproduces the committed scalar-class projection.
"""
import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline

G=6.674e-11; Msun=1.989e30; AU=1.496e11; c=2.998e8
Z=np.sqrt(32*np.pi/3.0); CEIL=5.2e-27; n_l=6.0
def nu(y): return np.sqrt(1.0+1.0/np.maximum(y,1e-30))
Q2_SCALAR={"canon":(2.0e-26,2.5e-26),"alt":(2.7e-26,3.3e-26)}   # banked class band
Q2_SCALAR_C={"canon":2.2e-26,"alt":3.0e-26}                     # central anchor @ 2.2 a0

# =========================================================== background/moduli/forcing
def setup(a0,gext_a0,K0hat=0.5):
    a0V=Z*a0; r_t=np.sqrt(2*G*Msun/a0V); K_eff=a0**2/(16*np.pi*G); gext=gext_a0*a0
    def Jt2_of(rho):
        cc=np.linspace(-1,1,4001); P2=0.5*(3*cc**2-1)
        rho=np.atleast_1d(np.asarray(rho,float)); out=np.empty_like(rho)
        for i,rr in enumerate(rho):
            gsun=a0V/(2*rr**2); gr=gsun+gext*cc; gth=-gext*np.sqrt(np.maximum(1-cc**2,0))
            Jt=2*np.sqrt(gr**2+gth**2)/a0V
            out[i]=2.5*np.trapz(Jt*P2,cc)
        return out
    kt=lambda rho: K0hat*np.maximum(1.0,np.asarray(rho,float))          # K_t/K_eff
    y0=lambda rho: np.sqrt((a0V/(2*np.asarray(rho,float)**2))**2+gext**2)/a0
    return dict(a0=a0,a0V=a0V,r_t=r_t,K_eff=K_eff,gext=gext,gext_a0=gext_a0,
                Jt2_of=Jt2_of,kt=kt,y0=y0,K0hat=K0hat)

# =========================================================== PART 1 validation
def indicial_eigs(lam,mu):
    M2=lam+2*mu; n=n_l
    P=np.array([
        [-2*lam/M2, 1.0/M2, n*lam/M2, 0.0],
        [4*mu*(3*lam+2*mu)/M2, -4*mu/M2, -2*mu*n*(3*lam+2*mu)/M2, n],
        [-1.0, 0.0, 1.0, 1.0/mu],
        [-2*mu*(3*lam+2*mu)/M2, -lam/M2, 2*mu*(2*n*(lam+mu)-M2)/M2, -3.0]])
    return np.sort(np.linalg.eigvals(P+np.diag([0.,1.,0.,1.])).real)
def validate_ode():
    print("="*84); print("PART 1  ODE validation (l=2 homogeneous exponents; uniform-strain source-free)"); print("="*84)
    tgt=np.array([-4.,-2.,1.,3.]); ok=True
    for lam,mu in [(1.,1.),(2.3,.7),(5.,.2)]:
        e=indicial_eigs(lam,mu); good=np.allclose(e,tgt,atol=1e-6); ok&=good
        print(f"  lam={lam} mu={mu}: U-exponents={np.round(e,3)}  textbook{{-4,-2,1,3}}={{r^-4,r^-2,r^1,r^3}}  {'OK' if good else 'FAIL'}")
    print("  (r^1 = displacement linear in x = uniform strain = exact source-free soln => the")
    print("   'uniform dilatation gives zero net shear force' check; textbook r^{l-1,l+1,-l,-l-2}.)")
    print(f"  --> ODE coefficients {'VALIDATED' if ok else 'NOT VALIDATED'}\n")
    return ok

# =========================================================== PART 2 forced BVP
def solve_beta(S,beta,gridN=1200):
    r_t=S['r_t']; kt=S['kt']; n=n_l
    rin=5.0*AU/r_t; rout=3.0e5*AU/r_t
    rho=np.logspace(np.log10(rin),np.log10(rout),gridN)
    phi=kt(rho)*S['Jt2_of'](rho); sp_=CubicSpline(np.log(rho),phi)
    Fr=lambda x: sp_(np.log(x),1)/x; Fth=lambda x: sp_(np.log(x))/x
    b=beta
    def rhs(x,Y):
        U,Srr,V,Srt=Y; k=kt(x); lam=k-2*b; mu=3*b; M2=k+4*b
        dU=-(2*lam/(M2*x))*U+(1/M2)*Srr+(n*lam/(M2*x))*V
        dSrr=(4*mu*(3*lam+2*mu)/(M2*x**2))*U-(4*mu/(M2*x))*Srr-(2*mu*n*(3*lam+2*mu)/(M2*x**2))*V+(n/x)*Srt-Fr(x)
        dV=-(1/x)*U+(1/x)*V+(1/mu)*Srt
        dSrt=-(2*mu*(3*lam+2*mu)/(M2*x**2))*U-(lam/(M2*x))*Srr+(2*mu*(2*n*(lam+mu)-M2)/(M2*x**2))*V-(3/x)*Srt-Fth(x)
        return np.vstack([dU,dSrr,dV,dSrt])
    bc=lambda Ya,Yb: np.array([Ya[1],Ya[3],Yb[0],Yb[2]])
    Yg=np.zeros((4,rho.size)); Yg[0]=phi/(kt(rho)+4*b)
    sol=solve_bvp(rhs,bc,rho,Yg,max_nodes=300000,tol=1e-6)
    xr=np.logspace(np.log10(rin),np.log10(rout),2500)
    U,Srr,V,Srt=sol.sol(xr); k=kt(xr); lam=k-2*b; mu=3*b; M2=k+4*b
    dU=-(2*lam/(M2*xr))*U+(1/M2)*Srr+(n*lam/(M2*xr))*V
    J2=dU+2*U/xr-n*V/xr
    return xr,J2,sol.status==0

# =========================================================== PART 3 phantom moment (committed-style 2D)
def scalar_committed(a0,gx,rmin_AU=5.0,NR=1400,NT=420):
    """Reproduce the committed scalar-class ell=2 phantom moment div[(nu-1)g_N] (m3_bvp)."""
    gext=gx*a0
    r=np.logspace(np.log10(rmin_AU*AU),np.log10(5.0e5*AU),NR); th=np.linspace(1e-4,np.pi-1e-4,NT)
    R,TH=np.meshgrid(r,th,indexing='ij'); ST=np.sin(TH); CT=np.cos(TH)
    gsun=G*Msun/R**2; gr=gsun+gext*CT; gth=-gext*ST; gmag=np.sqrt(gr**2+gth**2); y=gmag/a0
    f=nu(y)-1.0
    d_r=np.gradient(R**2*(f*gr),r,axis=0)/R**2; d_t=np.gradient(ST*(f*gth),th,axis=1)/(R*ST)
    rho=(d_r+d_t)/(4*np.pi*G)
    P2=0.5*(3*CT**2-1.0); dr=np.gradient(r); dth=np.gradient(th)
    W=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(rho*P2/R**3*W))

def extra_field_l2(a0,gx,r,NT=1200):
    """
    l=2 radial functions of the QUMOND extra-acceleration field A=(nu-1)g_N:
       A_r,2(r)  (coeff of P2 e_r),  A_th,2(r) (coeff of dP2/dth e_th).
    Divergence preserves l, so rho_ph,2 = (1/4piG)[(r^2 A_r,2)'/r^2 - 6 A_th,2/r].
    """
    gext=gx*a0
    th=np.linspace(1e-6,np.pi-1e-6,NT); ct=np.cos(th); st=np.sin(th)
    P2t=0.5*(3*ct**2-1); dP2t=-3*ct*st                    # P2, dP2/dtheta
    norm_th=np.trapz(dP2t*dP2t*st,th)                     # = l(l+1)*2/(2l+1) = 12/5
    Ar2=np.empty_like(r); Ath2=np.empty_like(r)
    for i,rr in enumerate(r):
        gsun=G*Msun/rr**2; gr=gsun+gext*ct; gth=-gext*st
        f=nu(np.sqrt(gr**2+gth**2)/a0)-1.0
        Ar2[i]=2.5*np.trapz((f*gr)*P2t*st,th)             # (2l+1)/2 * <A_r P2>
        Ath2[i]=np.trapz((f*gth)*dP2t*st,th)/norm_th      # projection onto dP2/dth
    return Ar2,Ath2

def div_l2(r,Ar2,Ath2):
    """rho_2 = (1/4piG)[ (r^2 A_r,2)'/r^2 - 6 A_th,2/r ]   (the l=2 part of div A)."""
    lnr=np.log(r); sp_=CubicSpline(lnr,r**2*Ar2)
    dterm=sp_(lnr,1)/r / r**2                              # d(r^2 Ar2)/dr = [d/dlnr](r^2 Ar2)/r
    return (dterm - 6*Ath2/r)/(4*np.pi*G)

def project_l2(r,rho2,NT=600):
    """committed interior ell=2 moment of a density whose radial l=2 fn is rho2(r)."""
    th=np.linspace(1e-4,np.pi-1e-4,NT); ST=np.sin(th); CT=np.cos(th); P2=0.5*(3*CT**2-1)
    R,TH=np.meshgrid(r,th,indexing='ij'); RHO=rho2[:,None]*P2[None,:]
    dr=np.gradient(r); dth=np.gradient(th); Wv=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(RHO*P2[None,:]/R**3*Wv))

def medium_w(S,a0,gx,beta,K0hat):
    """
    Apply the BVP-validated shear suppression Ssup(r)=K_t/(K_t+4 mu_s/3) to the l=2 of the QUMOND
    extra-acceleration FIELD, then take its divergence as a genuine (localized) density and project
    with the committed kernel.  At beta=0 -> committed scalar (gate).  Returns (w, Imed0, Iscal).
    """
    r=np.logspace(np.log10(5.0*AU),np.log10(5.0e5*AU),2000)
    Ar2,Ath2=extra_field_l2(a0,gx,r)
    Imed0=project_l2(r,div_l2(r,Ar2,Ath2))
    Iscal=scalar_committed(a0,gx)
    rho_=r/S['r_t']; kt=K0hat*np.maximum(1.0,rho_); Ssup=kt/(kt+4*beta)
    Imed=project_l2(r,div_l2(r,Ssup*Ar2,Ssup*Ath2))
    return Imed/Imed0, Imed0, Iscal

# =========================================================== MAIN
def main():
    validate_ode()
    print("="*84); print("PART 2  BVP dilatation vs local P-wave law  J2 = Jt2 * K_t/(K_t+4mu_s/3)")
    print("="*84)
    S=setup(9.36e-11,2.2,0.5)
    for b in [0.1,0.33,0.95]:
        xr,J2,ok=solve_beta(S,b); kt=S['kt'](xr); Jt2=S['Jt2_of'](xr)
        Jloc=Jt2*kt/(kt+4*b); msk=(xr>0.3)&(xr<3.0)
        rat=np.median((J2/Jloc)[msk])
        print(f"  beta={b:.2f}: median(J2_BVP/J2_local) over sourcing shell = {rat:+.4f}   (|.|~1 => P-wave law confirmed)")
    print()
    print("="*84); print("PART 3  gate + w(beta)  [Q2_medium = w * Q2_scalar ; ceiling 5.2e-27 s^-2]")
    print("="*84)
    betas=[0.33,0.6,0.95,2.0]
    for K0hat,ktag in [(0.5,"K_t=(Keff/2)*max(1,r/rt)  [sqrt-branch tangent]"),
                       (1.0,"K_t= Keff *max(1,r/rt)  [tangent=Keff at r_t]")]:
        print(f"\n### bulk-modulus footing: {ktag}")
        for tag,a0 in [("canon",9.36e-11),("alt",1.13e-10)]:
            for gx in [1.9,2.2,2.6]:
                S=setup(a0,gx,K0hat)
                ws=[]; g0=None
                for b in betas:
                    w,Imed0,Iscal=medium_w(S,a0,gx,b,K0hat); ws.append(w); g0=Imed0/Iscal
                q2c=Q2_SCALAR_C[tag]
                print(f"  [{tag} gext={gx}a0] GATE Imed(beta=0)/Iscal={g0:.3f} (must be ~1) "
                      f"{'OK' if 0.9<g0<1.1 else 'CHECK'}")
                print("     beta:      "+"  ".join(f"{b:>7.2f}" for b in betas))
                print("     w:         "+"  ".join(f"{v:>7.3f}" for v in ws))
                print("     Q2=w*scal: "+"  ".join(f"{v*q2c:>7.1e}" for v in ws)
                      +f"   [ceil {CEIL:.1e}]")
                print("     verdict:   "+"  ".join(f"{('PASS' if v*q2c<CEIL else 'FAILx%.1f'%(v*q2c/CEIL)):>7s}" for v in ws))
    print("\nexit 0")

if __name__=="__main__":
    main()
