import numpy as np, math, scipy.sparse as sps, scipy.sparse.linalg as spla
exec(open("proto.py").read().split("# control: one mass")[0])

def make_faces_sym(xmax, refs):
    xp = make_faces(xmax, refs)
    return np.concatenate([-xp[::-1][:-1], xp])

h=0.004
Rf=make_faces(XMAX,[(0.0,h),(0.5,h)]); zf=make_faces(XMAX,[(0.0,h),(0.5,h)])
g=Grid(Rf,zf); m=plummer(g,BFAC,1.0,(0.5,))
one=lambda x: np.ones_like(x)
zero=np.zeros((g.NR,g.NZ))
Rb=np.hypot(g.Rf[-1],g.zc); Zb=np.hypot(g.Rc,g.zf[-1])
phiN=lambda r: -2.0/r
pNbR,pNbZ=phiN(Rb),phiN(Zb)
mu=coeffs(g,zero,pNbR,pNbZ,one,0.0)
A,b=assemble(g,*mu,pNbR,pNbZ)
PhiN=spla.spsolve(A.tocsc(),4*math.pi*m.ravel()+b).reshape(g.NR,g.NZ)
# check discrete Poisson
L=laplacian(g,PhiN,pNbR,pNbZ)
print("Poisson check: max|lap/(4pi) - rho|/max rho =", np.max(np.abs(L/(4*math.pi)-m/g.V))/np.max(m/g.V))
# gradients at R=0.2,z=0
dR=np.zeros_like(PhiN); dZ=np.zeros_like(PhiN)
dR[1:-1,:]=(PhiN[2:,:]-PhiN[:-2,:])/(g.Rc[2:,None]-g.Rc[:-2,None])
dR[0,:]=(PhiN[1,:]-PhiN[0,:])/(g.Rc[1]+g.Rc[0])
dZ[:,1:-1]=(PhiN[:,2:]-PhiN[:,:-2])/(g.zc[None,2:]-g.zc[None,:-2])
dZ[:,0]=(PhiN[:,1]-PhiN[:,0])/(g.zc[1]+g.zc[0])
print("gN(0.2) =",-dR[np.argmin(abs(g.Rc-0.2)),0], " analytic", 2*0.2/(0.29**1.5))
print("PhiN(0.2,0)=",PhiN[np.argmin(abs(g.Rc-0.2)),0], " analytic", -2/math.sqrt(0.29))
# face nu and flux
nR=(PhiN[1:,:]-PhiN[:-1,:])/(g.Rc[1:,None]-g.Rc[:-1,None])
tR=0.5*(dZ[1:,:]+dZ[:-1,:])
nz=(PhiN[:,1:]-PhiN[:,:-1])/(g.zc[None,1:]-g.zc[None,:-1])
tz=0.5*(dR[:,1:]+dR[:,:-1])
gR=np.hypot(nR,tR); gz=np.hypot(nz,tz)
print("gN face: min",gR.min()," at R=",g.Rf[1:-1][np.unravel_index(gR.argmin(),gR.shape)[0]])
nu=lambda y: 0.5+np.sqrt(0.25+1.0/np.maximum(y,1e-30))
vR=nu(gR); vz=nu(gz)
print("nu max",vR.max(),"nu at R=0.2", nu(np.array([2.56]))[0])
AR=2*math.pi*g.Rf[1:-1,None]*np.diff(g.zf)[None,:]
Az=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)[:,None]*np.ones((1,g.NZ-1))
fR=(vR-1.0)*nR; fz=(vz-1.0)*nz
out=np.zeros((g.NR,g.NZ))
out[:-1,:]+=fR*AR; out[1:,:]-=fR*AR
out[:,:-1]+=fz*Az; out[:,1:]-=fz*Az
S=out/g.V
print("S at R=0.2,z=0:", S[np.argmin(abs(g.Rc-0.2)),0], " max|S|",np.max(np.abs(S)))
print("V at R=0.2:",g.V[np.argmin(abs(g.Rc-0.2)),0], " AR",AR[np.argmin(abs(g.Rc-0.2))-1,0])
# analytic phantom in midplane from point masses
for R in (0.05,0.2,0.5):
    gn=2*R/(R*R+0.25)**1.5
    print("R",R,"gN",gn,"nu",nu(np.array([gn]))[0])
