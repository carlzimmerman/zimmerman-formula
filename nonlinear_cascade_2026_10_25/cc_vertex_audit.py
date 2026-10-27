"""Independent full phase/scalar stationary elimination, then third derivative."""
import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from cc_vertex import cc_vertex
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();torch.set_num_threads(1);rho=.09478717830483639;u=.2659697829626922;kap=.0006995338357181399;N=9;L=2*np.pi;vol=L*L;nodes=N*N;freq=np.fft.fftfreq(N,d=1/N);D1=np.fft.ifft(1j*freq[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real;Ds=[torch.tensor(np.kron(D1,np.eye(N))),torch.tensor(np.kron(np.eye(N),D1))];Z=torch.tensor(null_space(np.ones((1,nodes))));ones=torch.ones(nodes,dtype=torch.float64);A0=sum(D.T@D for D in Ds);xx=np.stack(np.meshgrid(*[np.arange(N)*L/N]*2,indexing='ij'),axis=-1);rows=[]
for eta in [0.,.001,.1,1.]:
 k1=np.array([1.,0.,0.]);k2=np.array([0.,1.,0.]);v=cc_vertex(k1,k2,rho,u,kap,vol,eta);ns=[];nts=[];dns=[];dgs=[]
 for k,w,A in zip([k1,k2,k1+k2],v['omega'],v['A']):
  wave=np.exp(1j*(xx@k[:2])).reshape(-1);ns.append(2*np.real(A*wave)/np.sqrt(vol));nts.append(2*np.real(-1j*w*A*wave)/np.sqrt(vol));dns.append(2*np.real(1j*wave[:,None]*k[:2]*A)/np.sqrt(vol));dgs.append(2*np.real(-1j*wave[:,None]*k[:2]*A/(k@k))/np.sqrt(vol))
 ns=torch.tensor(np.array(ns));nts=torch.tensor(np.array(nts));dns=torch.tensor(np.array(dns));dgs=torch.tensor(np.array(dgs));eps=torch.zeros(3,dtype=torch.float64,requires_grad=True);n=eps@ns;nt=eps@nts;rr=rho+n;gc=np.sqrt(eta/rho**3)
 def weighted(f):return sum(D.T@(f[:,None]*D) for D in Ds)
 Ar=weighted(rr);Ar2=weighted(rr**2);Ar3=weighted(rr**3);K=torch.cat([torch.cat([Ar,-gc*Ar2],dim=1),torch.cat([-gc*Ar2,A0+gc*gc*Ar3],dim=1)],dim=0);ZZ=torch.block_diag(Z,Z);src=torch.cat([nt,-2*gc*rr*nt]);sr=ZZ.T@src;Kr=ZZ.T@K@ZZ;Tkin=.5*vol/nodes*(sr@torch.linalg.solve(Kr,sr));dn=torch.einsum('i,ina->na',eps,dns);dg=torch.einsum('i,ina->na',eps,dgs);uu=torch.sqrt(u*u+torch.sum(dg*dg,dim=1));U=vol/nodes*torch.sum(kap/(8*rr)*torch.sum(dn*dn,dim=1)-torch.log1p(-uu)-uu-.5*torch.sum(dg*dg,dim=1));expression=-Tkin+U;d1=torch.autograd.grad(expression,eps,create_graph=True)[0][0];d2=torch.autograd.grad(d1,eps,create_graph=True)[0][1];third=float(torch.autograd.grad(d2,eps)[0][2]);pred=2*v['V'].real;err=abs(third-pred)/max(abs(pred),1e-12);assert err<2e-9;rows.append({'eta':eta,'stationary_elimination_mixed_third':third,'predicted_cubic_H':float(pred),'relative_error':float(err),'nonlinear_inertia_vertex':float(v['nonlinear_inertia'])})
out={'checks':rows,'scope':'Independent exact nonzero-mode stationary elimination of full original quasi-static phase/current square on9x9 periodic plane at variable density, then third derivative with Legendre sign. Verifies cubic conservative vertex, not full retarded galaxy evolution.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
