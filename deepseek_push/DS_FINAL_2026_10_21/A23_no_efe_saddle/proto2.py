import numpy as np, math, time, scipy.sparse as sps, scipy.sparse.linalg as spla
exec(open("proto.py").read().split("# control: one mass")[0])

def make_faces_sym(xmax, refs):
    """faces on [-xmax, xmax] including 0, graded about the refs."""
    xp = make_faces(xmax, refs)
    return np.concatenate([-xp[::-1][:-1], xp])

def plummer_full(g,b,mtot=2.0,centres=(0.5,-0.5)):
    return plummer(g,b,mtot,centres)

def face_grads(g,Phi,pbR,pbZ,e=0.0):
    """normal/tangential components of grad(Phi_tot) on faces, with grad(Phi)=grad(Psi)-e zhat."""
    dR=np.zeros_like(Phi); dZ=np.zeros_like(Phi)
    dR[1:-1,:]=(Phi[2:,:]-Phi[:-2,:])/(g.Rc[2:,None]-g.Rc[:-2,None])
    dR[0,:]=(Phi[1,:]-Phi[0,:])/(g.Rc[1]+g.Rc[0])
    dR[-1,:]=(pbR-Phi[-2,:])/(g.Rf[-1]-g.Rc[-2])
    dZ[:,1:-1]=(Phi[:,2:]-Phi[:,:-2])/(g.zc[None,2:]-g.zc[None,:-2])
    dZ[:,0]=(Phi[:,1]-Phi[:,0])/(g.zc[1]+g.zc[0])
    dZ[:,-1]=(pbZ-Phi[:,-2])/(g.zf[-1]-g.zc[-2])
    nR=(Phi[1:,:]-Phi[:-1,:])/(g.Rc[1:,None]-g.Rc[:-1,None])
    tR=0.5*(dZ[1:,:]+dZ[:-1,:])-e
    nz=(Phi[:,1:]-Phi[:,:-1])/(g.zc[None,1:]-g.zc[None,:-1])-e
    tz=0.5*(dR[:,1:]+dR[:,:-1])
    nRo=(pbR-Phi[-1,:])/(g.Rf[-1]-g.Rc[-1]); tRo=dZ[-1,:]-e
    nzo=(pbZ-Phi[:,-1])/(g.zf[-1]-g.zc[-1])-e; tzo=dR[:,-1]
    return (nR,tR,nRo,tRo),(nz,tz,nzo,tzo)

def nu_simple(y):
    y=np.maximum(y,1e-30)
    return 0.5+np.sqrt(0.25+1.0/y)

def divflux(g,fR,fz,pbR=None,pbZ=None,open_z0=False):
    """discrete divergence of a face flux (fR on R-faces, fz on z-faces); returns per-cell value (not /V)."""
    out=np.zeros((g.NR,g.NZ)); I=g.idx
    AR=2*math.pi*g.Rf[1:-1,None]*np.diff(g.zf)[None,:]
    out[:-1,:]+= (fR*AR)
    out[1:,:] -= (fR*AR)
    Az=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)[:,None]*np.ones((1,g.NZ-1))
    out[:,:-1]+= (fz*Az)
    out[:,1:] -= (fz*Az)
    return out

def qumond(g,m,phif,e=0.0,full_mu=False,nu=nu_simple,tag=""):
    """QUMOND-type: lap(phi)=div(nu(|grad phi_N,tot|) grad phi_N,tot).
    phi_N solved discretely with the same mass array; phi_ph solved linearly."""
    Rb=np.hypot(g.Rf[-1],g.zc); Zb=np.hypot(g.Rc,g.zf[-1])
    pbR,pbZ=phif(Rb),phif(Zb)
    # discrete Newtonian potential with BC -2/r (total mass 2)
    phiN=lambda r: -2.0/r
    A,b=assemble(g,*[np.ones_like(x) for x in coeffs(g, np.zeros((g.NR,g.NZ)), pbR,pbZ, lambda x: np.ones_like(x), 0.0)], pbR,pbZ)
    # rebuild cleanly
    zero=np.zeros((g.NR,g.NZ))
    one=lambda x: np.ones_like(x)
    mu=coeffs(g,zero,pbR,pbZ,one,0.0)
    A,b=assemble(g,*mu,pbR,pbZ)
    rhsN=4*math.pi*m.ravel()
    pNbR,pNbZ=phiN(Rb),phiN(Zb)
    AN,bN=assemble(g,*coeffs(g,zero,pNbR,pNbZ,one,0.0),pNbR,pNbZ)
    PhiN=spla.spsolve(AN.tocsc(),rhsN+bN).reshape(g.NR,g.NZ)
    # nu on faces from phiN + e z
    (nR,tR,nRo,tRo),(nz,tz,nzo,tzo)=face_grads(g,PhiN,pNbR,pNbZ,e)
    vR=nu(np.hypot(nR,tR)); vRo=nu(np.hypot(nRo,tRo))
    vz=nu(np.hypot(nz,tz)); vzo=nu(np.hypot(nzo,tzo))
    # flux (nu-1)*grad phi_N,tot on interior faces
    AR=2*math.pi*g.Rf[1:-1,None]*np.diff(g.zf)[None,:]
    Az=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)[:,None]*np.ones((1,g.NZ-1))
    fR=(vR-1.0)*nR; fz=(vz-1.0)*nz
    Sflux=divflux(g,fR,fz)
    S=Sflux/g.V
    # boundary flux of (nu-1)grad phi_N,tot -> Dirichlet correction for phi_ph
    # phi_ph BC = phif - phiN (= sqrt2 log r + 2/r), independent of e
    ph=lambda r: phif(r)+2.0/r
    ppbR,ppbZ=ph(Rb),ph(Zb)
    mu2=coeffs(g,zero,ppbR,ppbZ,one,0.0)
    A2,b2=assemble(g,*mu2,ppbR,ppbZ)
    rhs=4*math.pi*m.ravel()+Sflux.ravel()
    Phiph=spla.spsolve(A2.tocsc(),rhs+b2).reshape(g.NR,g.NZ)
    res=np.max(np.abs(A2@Phiph.ravel()-b2-rhs))/np.max(np.abs(rhs))
    C=laplacian(g,Phiph,ppbR,ppbZ)/(4*math.pi)
    return C,PhiN,Phiph,res

def colS(g,C,z=0.0):
    # interpolate C onto z (linear between two nearest z cells)
    j=np.searchsorted(g.zc,z)
    if j<=0: row=C[:,0]
    elif j>=g.NZ: row=C[:,-1]
    else:
        t=(z-g.zc[j-1])/(g.zc[j]-g.zc[j-1]); row=(1-t)*C[:,j-1]+t*C[:,j]
    return float(2*np.sum(np.minimum(row,0)*np.diff(g.Rf))), row

if __name__=="__main__":
    t0=time.time()
    h=0.004
    # full domain, e=0
    Rf=make_faces(XMAX,[(0.0,h),(0.5,h)])
    zf=make_faces_sym(XMAX,[(0.0,h),(0.5,h)])
    g=Grid(Rf,zf); m=plummer_full(g,BFAC,2.0,(0.5,-0.5))
    print("full grid N=",g.N, "mass",m.sum())
    C0,PN,PP,res=qumond(g,m,PHI2,0.0)
    S0,row0=colS(g,C0,0.0)
    print("QUMOND full e=0: S=",S0,"C(0.2)=",np.interp(0.2,g.Rc,row0),"res",res)
    print("  C profile",[(round(x,3),round(float(np.interp(x,g.Rc,row0)),4)) for x in (0.02,0.05,0.1,0.2,0.3,0.5,1.0)])
    # half domain, e=0
    zf2=make_faces(XMAX,[(0.0,h),(0.5,h)])
    g2=Grid(Rf,zf2); m2=plummer(g2,BFAC,1.0,(0.5,))
    C2,PN2,PP2,res2=qumond(g2,m2,PHI2,0.0)
    S2,row2=colS(g2,C2,0.0)
    print("QUMOND half e=0: S=",S2,"C(0.2)=",np.interp(0.2,g2.Rc,row2),"res",res2)
    print("time",time.time()-t0)
    # AQUAL half at e=0 for reference
    Ph,pR,pZ,res3,it3,d3=solve(g2,m2,DEEP,PHI2)
    C3=laplacian(g2,Ph,pR,pZ)/(4*math.pi)-m2/g2.V
    S3,row3=colS(g2,C3,0.0)
    print("AQUAL half e=0: S=",S3,"C(0.2)=",np.interp(0.2,g2.Rc,row3))
    print("time",time.time()-t0)
