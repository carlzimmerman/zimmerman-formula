import numpy as np, math, time, scipy.sparse as sps, scipy.sparse.linalg as spla
exec(open("proto.py").read().split("# control: one mass")[0])
exec(open("proto2.py").read().split('if __name__')[0].split('exec(open("proto.py")')[0].replace("import numpy as np, math, time, scipy.sparse as sps, scipy.sparse.linalg as spla",""))

def make_faces_sym(xmax, refs):
    xp = make_faces(xmax, refs)
    return np.concatenate([-xp[::-1][:-1], xp])

def divflux(g,fR,fz):
    out=np.zeros((g.NR,g.NZ))
    AR=2*math.pi*g.Rf[1:-1,None]*np.diff(g.zf)[None,:]
    out[:-1,:]+=fR*AR; out[1:,:]-=fR*AR
    Az=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)[:,None]*np.ones((1,g.NZ-1))
    out[:,:-1]+=fz*Az; out[:,1:]-=fz*Az
    return out

def face_grads(g,Phi,pbR,pbZ,e=0.0):
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
    return 0.5+np.sqrt(0.25+1.0/np.maximum(y,1e-30))

def qumond(g,m,e=0.0,phif=None):
    phif = phif or (lambda r: math.sqrt(2.0)*math.log(r))
    one=lambda x: np.ones_like(x); zero=np.zeros((g.NR,g.NZ))
    Rb=np.hypot(g.Rf[-1],g.zc); Zb=np.hypot(g.Rc,g.zf[-1])
    pNbR,pNbZ=-2.0/Rb,-2.0/Zb
    A,b=assemble(g,*coeffs(g,zero,pNbR,pNbZ,one,0.),pNbR,pNbZ)
    PhiN=spla.spsolve(A.tocsc(),4*math.pi*m.ravel()+b).reshape(g.NR,g.NZ)
    (nR,tR,nRo,tRo),(nz,tz,nzo,tzo)=face_grads(g,PhiN,pNbR,pNbZ,e)
    vR=nu_simple(np.hypot(nR,tR)); vz=nu_simple(np.hypot(nz,tz))
    Sflux=divflux(g,(vR-1.)*nR,(vz-1.)*nz)
    ph=lambda r: phif(r)+2.0/r
    ppbR,ppbZ=ph(Rb),ph(Zb)
    A2,b2=assemble(g,*coeffs(g,zero,ppbR,ppbZ,one,0.),ppbR,ppbZ)
    rhs=4*math.pi*m.ravel()+Sflux.ravel()
    Phiph=spla.spsolve(A2.tocsc(),rhs+b2).reshape(g.NR,g.NZ)
    C=laplacian(g,Phiph,ppbR,ppbZ)/(4*math.pi)
    return C

def colS(g,C):
    row=C[:,0]
    return float(2*np.sum(np.minimum(row,0)*np.diff(g.Rf))),row

h=0.005
Rf=make_faces(XMAX,[(0.0,h),(0.5,h)])
zf_h=make_faces(XMAX,[(0.0,h),(0.5,h)])
zf_f=make_faces_sym(XMAX,[(0.0,h),(0.5,h)])

# AQUAL half, e sweep (A13 style)
gh=Grid(Rf,zf_h); mh=plummer(gh,BFAC,1.0,(0.5,))
# AQUAL full
gf=Grid(Rf,zf_f); mf=plummer(gf,BFAC,2.0,(0.5,-0.5))

t0=time.time()
print("=== AQUAL e-sweep ===")
prev=None
for e in (0.0,0.3,1.0,3.0):
    Ph,pR,pZ,res,it,d=solve(gh,mh,DEEP,lambda r: math.sqrt(2.)*math.log(r) if e==0 else (lambda rr: math.sqrt(2.)*math.log(rr)),e=e,alpha=0.3,itmax=600,tol=1e-7,Phi0=prev)
    prev=Ph
    C=laplacian(gh,Ph,pR,pZ)/(4*math.pi)-mh/gh.V
    S,row=colS(gh,C)
    print(f" half e={e}: S={S:+.5f} C02={np.interp(0.2,gh.Rc,row):+.4f} it={it} res={res:.1e} t={time.time()-t0:.1f}")
    if e==0: S0h=S
print(" ratios:",)
prevf=None
for e in (0.0,0.3,1.0,3.0):
    Ph,pR,pZ,res,it,d=solve(gf,mf,DEEP,lambda r: math.sqrt(2.)*math.log(r),e=e,alpha=0.3,itmax=600,tol=1e-7,Phi0=prevf)
    prevf=Ph
    C=laplacian(gf,Ph,pR,pZ)/(4*math.pi)-mf/gf.V
    j=np.argmin(abs(gf.zc-0.0)); row=0.5*(C[:,j]+C[:,j-1]) if j>0 else C[:,0]
    S=float(2*np.sum(np.minimum(row,0)*np.diff(gf.Rf)))
    print(f" full e={e}: S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f} it={it} res={res:.1e} t={time.time()-t0:.1f}")
    if e==0: S0f=S

print("=== QUMOND e-sweep ===")
for e in (0.0,0.3,1.0,3.0):
    C=qumond(gh,mh,e)
    S,row=colS(gh,C); print(f" half e={e}: S={S:+.5f} C02={np.interp(0.2,gh.Rc,row):+.4f}")
for e in (0.0,0.3,1.0,3.0):
    C=qumond(gf,mf,e)
    j=np.argmin(abs(gf.zc-0.0)); row=0.5*(C[:,j]+C[:,j-1]) if j>0 else C[:,0]
    S=float(2*np.sum(np.minimum(row,0)*np.diff(gf.Rf)))
    print(f" full e={e}: S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f}")
print("time",time.time()-t0)
