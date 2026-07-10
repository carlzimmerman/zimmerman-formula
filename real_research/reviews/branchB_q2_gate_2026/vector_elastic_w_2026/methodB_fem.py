#!/usr/bin/env python3
"""
METHOD B -- 2D vector-elastic BVP for the shear-suppression factor w (Branch B, Zenodo 21301460).
Independent of Method A's ODE algebra: we MINIMIZE the elastic energy directly over the displacement
field u(r,theta)=(u_r,u_theta) subject to the elastic-medium constitutive law, and read off J=div u.

    E[u] = INT [ (1/2) K_t(r) (div u)^2  +  mu_s (e_ij e_ij - (1/3) J^2)  -  f . u ] dV
    K_t(r) = K_eff S(y0(r))     tangent bulk modulus, S from the pinned nu-reconstruction,
                                y0(r)=(GM/r^2)/a0 = Sun's monopole background (Method-A footing)
    mu_s   = 3 beta K_eff       shear modulus (cap 6 K_eff = beta<=2, the 6Z^2 bound)
    f      = -grad(chi), chi=K_t(r) rho_ph   FIXED external gradient force; at mu_s->0 it drives
             J -> rho_ph (the committed 2D QUMOND scalar phantom) so Q2(beta=0)=Q2_scalar.

DISCRETIZATION (the load-bearing choice): a NAIVE collocated (equal-order) 2D finite-difference of
u(r,theta) is UNUSABLE here -- it admits spurious zero-energy shear-relief (checkerboard/hourglass)
modes that let the discrete solenoidal field cancel deviatoric strain at zero cost, which pins J
mu_s-independent and FAKES w=1 (verified in diag_mu_dependence.py: constant-K J is exactly mu-flat,
contradicting the P-wave-modulus theory J~1/(K+4/3 mu)). The correct spurious-free 2D discretization
restricts the angular direction to the EXACT ell=2 vector-harmonic (u_r=U(r)P2, u_th=V(r)dP2/dth) --
this is the observable's own multipole and it carries the full spheroidal U-V coupling, so genuine
solenoidal relief (the divergence-free ell=2 combination U'+2U/r-6V/r=0) is retained while the
spurious modes are gone. Radial direction: FD on log grid, mask r<5 AU. The energy reduces to a 1D
radial functional via the closed angular integrals (G_pp=2/5, G_bb=12/5, dP2'+cot dP2=-6 P2, ...).

w(beta)=Q2(beta)/Q2(0),  Q2 = |interior ell=2 moment of J| (committed project()).
MANDATORY VALIDATION GATE: the beta->0 Q2 must reproduce the committed scalar Q2 within ~10%.
exit 0. no commits, no zenodo.
"""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve

G=6.674e-11; Msun=1.989e30; AU=1.496e11; CEIL=5.2e-27
Z=np.sqrt(32*np.pi/3); yc=Z/2.0
def nu(y): return np.sqrt(1.0+1.0/np.maximum(y,1e-30))

# tangent bulk stiffening S(y) from the pinned constitutive reconstruction (matches action_w)
kappa=1.0/((nu(yc)-1.0)*yc)
def _tan(y):
    dy=1e-5*max(y,1e-3); eps=lambda q:kappa*(nu(q)-1.0)*q; sig=lambda q:q/yc
    return (sig(y+dy)-sig(y-dy))/(eps(y+dy)-eps(y-dy))
_deep=_tan(0.01)
def S_of(y): return _tan(max(y,1e-6))/_deep

# closed ell=2 angular integrals (verified numerically): p2=P2, b2=dP2/dth, b2p=d2P2/dth2,
# cb2=cot(th)dP2/dth ; identity b2p+cb2 = -6 P2  => J = (U'+2U/r-6V/r) P2 (pure ell=2)
G_pp,G_pbp,G_pcb,G_bpbp,G_cbcb,G_bpcb,G_bb = 0.4,-1.6,-0.8,8.4,3.6,1.2,2.4

def deriv1d(x):
    n=len(x); rows=[];cols=[];vals=[]
    for i in range(n):
        if i==0: h=x[1]-x[0]; rows+=[0,0];cols+=[0,1];vals+=[-1/h,1/h]
        elif i==n-1: h=x[-1]-x[-2]; rows+=[n-1,n-1];cols+=[n-2,n-1];vals+=[-1/h,1/h]
        else:
            hm=x[i]-x[i-1];hp=x[i+1]-x[i]; rows+=[i,i,i];cols+=[i-1,i,i+1]
            vals+=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
    return sp.csr_matrix((vals,(rows,cols)),shape=(n,n))

def project2d(field2d,r,th):
    R,TH=np.meshgrid(r,th,indexing='ij'); ST=np.sin(TH); CT=np.cos(TH)
    P2=0.5*(3*CT**2-1.0); dr=np.gradient(r); dth=np.gradient(th)
    W=2*np.pi*R**2*ST*dr[:,None]*dth[None,:]
    return abs(np.sum(field2d*P2/R**3*W))

def rho_phantom(a0,gext_a0,r,th):
    gext=gext_a0*a0
    R,TH=np.meshgrid(r,th,indexing='ij'); ST=np.sin(TH); CT=np.cos(TH)
    gr=G*Msun/R**2+gext*CT; gth=-gext*ST; gmag=np.sqrt(gr**2+gth**2); f=nu(gmag/a0)-1.0
    Ar=f*gr; Ath=f*gth
    d_r=np.gradient(R**2*Ar,r,axis=0)/R**2; d_t=np.gradient(ST*Ath,th,axis=1)/(R*ST)
    return (d_r+d_t)/(4*np.pi*G)

def solve_modal(a0,gext_a0,betas,radial_Kt=True,mu_tracks_tangent=False,NR=900,NT=1200):
    """ell=2 spheroidal modal reduction; returns {beta:Q2} and the on-grid scalar Q2."""
    r=np.logspace(np.log10(5.0*AU),np.log10(5.0e5*AU),NR)
    th=np.linspace(1e-4,np.pi-1e-4,NT)
    R=r[:,None]+0*th[None,:]     # (NR,NT) radius, for 1/R in the tangential gradient
    # angular functions on the theta quadrature
    c=np.cos(th); s=np.sin(th); P2=0.5*(3*c**2-1); B2=-3*c*s
    wsin=s*np.gradient(th)
    # --- fields on (r,theta) for driving + scalar reference (committed def) ---
    rho_ph=rho_phantom(a0,gext_a0,r,th)                # (NR,NT)
    y0=(G*Msun/r**2)/a0
    Keff=a0**2/(16*np.pi*G)
    if radial_Kt:
        Kt=Keff*np.array([S_of(v) for v in y0])         # radial K_t(r)
    else:
        Kt=Keff*np.array([S_of(gext_a0) for _ in y0])   # constant shell value S(g_ext/a0)
    # The external gradient force f=-grad(chi), chi=K_t rho_ph, does work -INT f.u = INT chi J only
    # (a gradient force does ZERO work on a divergence-free field: INT f.u = -INT chi div u = 0).
    # So the drive couples ONLY through J: L = INT chi J dV = sum_r rw K_t Jr rho_ph2(r), with the
    # ell=2 moment rho_ph2(r)=<rho_ph,P2>. This is the exact, divergence-free-clean drive; at mu->0
    # it yields Jr=rho_ph2/G_pp => project(Jr P2)=project(rho_ph)=Q2_scalar EXACTLY (validation).
    rho_ph2=np.sum(rho_ph*P2[None,:]*wsin[None,:],axis=1)   # (NR,) ell=2 moment of the phantom
    # scalar reference Q2 on THIS grid
    Q2_scalar_grid=project2d(rho_ph,r,th)

    # --- radial operators (x=[U;V], each length NR) ---
    Dr=deriv1d(r); Ir=sp.identity(NR,format='csr'); di=lambda v:sp.diags(v)
    Z0=sp.csr_matrix((NR,NR)); H2=lambda a,b: sp.hstack([a,b],format='csr')
    OP_Up = H2(Dr, Z0)                      # e_rr coeff  A_rr=U'
    OP_a  = H2(di(1.0/r), Z0)               # a=U/r
    OP_b  = H2(Z0, di(1.0/r))               # b=V/r
    OP_Jr = H2(Dr+di(2.0/r), di(-6.0/r))    # Jr = U'+2U/r-6V/r
    OP_g  = H2(di(1.0/r), Dr-di(1.0/r))     # g = U/r + V' - V/r  (2 e_rth = g B2)
    rw=2*np.pi*r**2*np.gradient(r)          # radial volume weight

    def addterm(H, wvec, OPP, OPQ):
        D=di(wvec); T=OPP.T@D@OPQ; return H+T+T.T

    # Hessian pieces independent of beta (bulk) and the shear unit
    Hbulk=sp.csr_matrix((2*NR,2*NR))
    Hbulk=addterm(Hbulk, rw*0.5*Kt*G_pp, OP_Jr, OP_Jr)      # (1/2)K_t G_pp Jr^2

    def shearH(muw):
        """full shear Hessian with per-radius shear modulus muw(r) folded into the weight."""
        w=rw*muw
        H=sp.csr_matrix((2*NR,2*NR))
        H=addterm(H, w*G_pp, OP_Up, OP_Up)                    # e_rr^2
        H=addterm(H, w*G_pp,  OP_a, OP_a)                     # e_thth^2 ...
        H=addterm(H, w*G_pbp, OP_a, OP_b)
        H=addterm(H, w*G_bpbp,OP_b, OP_b)
        H=addterm(H, w*G_pp,  OP_a, OP_a)                     # e_phph^2 ...
        H=addterm(H, w*G_pcb, OP_a, OP_b)
        H=addterm(H, w*G_cbcb,OP_b, OP_b)
        H=addterm(H, w*0.5*G_bb, OP_g, OP_g)                  # 2 e_rth^2
        H=addterm(H, -w*(1.0/3.0)*G_pp, OP_Jr, OP_Jr)         # -(1/3)J^2
        return H.tocsr()

    # drive vector b: L = INT chi J dV = sum_r (rw K_t rho_ph2) Jr = (OP_Jr^T (rw K_t rho_ph2)) . x
    bvec=OP_Jr.T@(rw*Kt*rho_ph2)
    # BCs: outer U=V=0 (far field pinned) ; regularity at inner: natural (free). also fix U,V at
    # outermost node only. inner node left free (mask edge, free surface).
    fixed=[NR-1, 2*NR-1]     # U[last], V[last]
    free=np.setdiff1d(np.arange(2*NR),fixed)

    def q2_of(beta):
        # floor beta to a tiny value so the correctly-scaled shear term lifts the divergence-free
        # ell=2 null mode at beta->0 (mu_s/K_eff=3e-6 is negligible physics -> the true bulk limit).
        # mu_s(r): committed footing = 3 beta K_eff (constant); fork = 3 beta K_t(r) (tracks tangent).
        bb=max(beta,1e-6)
        muvec=3.0*bb*(Kt if mu_tracks_tangent else Keff*np.ones(NR))
        H=(Hbulk+shearH(muvec)).tocsr()
        uf=spsolve(H[free][:,free].tocsc(), bvec[free])
        x=np.zeros(2*NR); x[free]=uf
        U=x[:NR]; V=x[NR:]
        Jr=(OP_Jr@x)                       # radial profile of J (J=Jr*P2)
        # reconstruct J(r,theta)=Jr(r)P2(theta), project ell=2 with committed weights
        Jfield=Jr[:,None]*P2[None,:]
        return project2d(Jfield,r,th), Jr, U, V
    out={}
    for beta in betas:
        out[beta]=q2_of(beta)[0]
    # also grab beta0 profile for validation reporting
    _,Jr0,U0,V0=q2_of(betas[0])
    return out, Q2_scalar_grid

# ------------------------------------------------------------------------------------------------
if __name__=="__main__":
    print("="*94)
    print("METHOD B (spurious-free modal ell=2 vector-elastic BVP): w = Q2(beta)/Q2(0)")
    print("  full spheroidal U(r)P2, V(r)dP2 -> solenoidal relief retained, checkerboard modes gone")
    print("="*94)
    betas=[0.0,0.33,0.6,0.95,2.0]
    SCAL_BAND={"canon":(2.0e-26,2.5e-26),"alt":(2.7e-26,3.3e-26)}

    # KAL: physical-units calibration of the scalar class (2.2e-26 at canon 2.2a0, committed anchor)
    _out,_sc=solve_modal(9.36e-11,2.2,[0.0])
    KAL=2.2e-26/_sc
    print(f"[calib] KAL from canon 2.2a0 scalar (project on modal grid) -> Q2_scalar(canon,2.2)=2.2e-26\n")

    for tag,a0 in (("canon",9.36e-11),("alt",1.13e-10)):
        print(f"----- footing={tag}  a0={a0:.3e} -----")
        print(f"{'gext':>5} {'Q2_scalar':>11} {'valid b0/scal':>13} | "
              +"  ".join(f"w(b={b})" for b in betas[1:]))
        for gx in (1.9,2.2,2.6):
            out,sc=solve_modal(a0,gx,betas)
            Q2_scalar=sc*KAL
            valid=out[0.0]/sc
            ws=[out[b]/out[0.0] for b in betas[1:]]
            print(f"{gx:>5.1f} {Q2_scalar:>11.2e} {valid:>13.3f} | "
                  +"  ".join(f"{w:6.3f}" for w in ws))
        b=SCAL_BAND[tag]
        print(f"  [validate] scalar band {b[0]:.1e}-{b[1]:.1e}; beta=0 FEM/scalar (valid col) must be ~1.0\n")

    print("="*94)
    print("DECISIVE: Q2_medium = w * Q2_scalar  vs ceiling 5.2e-27 s^-2  (gext=2.2a0, radial K_t)")
    print("="*94)
    for tag,a0 in (("canon",9.36e-11),("alt",1.13e-10)):
        out,sc=solve_modal(a0,2.2,betas); Q2s=sc*KAL
        for bb in betas[1:]:
            w=out[bb]/out[0.0]; Q2m=w*Q2s
            st="PASS" if Q2m<CEIL else f"FAIL x{Q2m/CEIL:.2f}"
            print(f"  {tag:5s} beta={bb:4.2f} (mu_s/K_eff={3*bb:.2f}): w={w:6.3f}  Q2={Q2m:.2e}  [{st}]")

    # -------- THE DECISIVE FOOTING FORK: is mu_s tied to K_eff (deep, committed) or to K_t(r)? -------
    print("\n"+"="*94)
    print("FOOTING FORK on the shear modulus (the ONE assumption that flips the verdict):")
    print("  A) mu_s = 3 beta K_eff  (committed: shear tied to the DEEP modulus, constant)")
    print("  B) mu_s = 3 beta K_t(r) (fork: shear STIFFENS with the tangent bulk modulus)")
    print("="*94)
    for tag,a0 in (("canon",9.36e-11),("alt",1.13e-10)):
        outA,scA=solve_modal(a0,2.2,betas,mu_tracks_tangent=False)
        outB,scB=solve_modal(a0,2.2,betas,mu_tracks_tangent=True)
        Q2s=scA*KAL
        print(f"  --{tag}, gext=2.2a0, Q2_scalar={Q2s:.2e}--")
        for bb in betas[1:]:
            wA=outA[bb]/outA[0.0]; wB=outB[bb]/outB[0.0]
            qA=wA*Q2s; qB=wB*Q2s
            sA="PASS" if qA<CEIL else f"FAILx{qA/CEIL:.1f}"; sB="PASS" if qB<CEIL else f"FAILx{qB/CEIL:.1f}"
            print(f"    beta={bb:4.2f}: A) w={wA:6.3f} Q2={qA:.2e} [{sA}]   |   B) w={wB:6.3f} Q2={qB:.2e} [{sB}]")
    print("\nexit 0")
