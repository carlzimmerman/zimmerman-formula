"""1D periodic self-gravity toy: exact constant phase factoring, not a galaxy model."""
import pathlib,json,hashlib,datetime,platform,resource,time,numpy as np
P=pathlib.Path(__file__).resolve().parent;files=[pathlib.Path(__file__),P/'MECHANISM_AUDIT.md'];before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};start=datetime.datetime.now(datetime.timezone.utc).isoformat();eta=.004639099785300577;carrier=128;boost=eta*carrier;G=.002;T=.3;dt=.001

def run(N,factored):
 x=np.arange(N)*2*np.pi/N;h=2*np.pi/N;p=np.fft.fftfreq(N,d=1/N);dist=np.angle(np.exp(1j*(x-np.pi)));a=np.exp(-dist**2/(2*.5**2)).astype(complex);a/=np.sqrt(np.sum(abs(a)**2)*h)
 if not factored:a*=np.exp(1j*carrier*x)
 disp=.5*eta*p*p+(boost*p if factored else 0);prop=np.exp(-1j*dt*disp/2)
 def gravity(a):
  rho=abs(a)**2;rh=np.fft.fft(rho);ph=np.zeros_like(rh);ii=p!=0;ph[ii]=-4*np.pi*G*rh[ii]/p[ii]**2;return np.fft.ifft(ph).real
 def stats(a):
  da=np.fft.ifft(1j*p*np.fft.fft(a));mass=float(np.sum(abs(a)**2)*h);pa=float(eta*np.sum(np.imag(a.conj()*da))*h);kin=float(.5*eta*eta*np.sum(abs(da)**2)*h);pot=gravity(a);W=float(.5*np.sum(abs(a)**2*pot)*h)
  return dict(M=mass,P=pa+(boost*mass if factored else 0),E=kin+W+(boost*pa+.5*boost*boost*mass if factored else 0))
 initial=stats(a)
 for it in range(round(T/dt)):
  a=np.fft.ifft(np.fft.fft(a)*prop);a*=np.exp(-1j*dt*gravity(a)/eta);a=np.fft.ifft(np.fft.fft(a)*prop)
 final=stats(a)
 # Compare the physical amplitude after removing the known carrier and time phase.
 if not factored:a*=np.exp(-1j*carrier*x+.5j*boost*boost*T/eta)
 return x,a,initial,final
rows=[];reference=run(1024,False)
for N,fact in [(512,False),(64,True),(128,True)]:
 x,a,ini,fin=run(N,fact);rr=reference[1][::1024//N];phase=np.angle(np.vdot(rr,a));err=float(np.linalg.norm(a*np.exp(-1j*phase)-rr)/np.linalg.norm(rr));rhoerr=float(np.max(abs(abs(a)**2-abs(rr)**2)));row=dict(N=N,factored=fact,relative_amplitude_error=err,max_density_error=rhoerr,initial=ini,final=fin,M_residual=fin['M']-ini['M'],P_residual=fin['P']-ini['P'],E_residual=fin['E']-ini['E']);rows.append(row);assert err<1e-7 and rhoerr<1e-7 and abs(row['M_residual'])<1e-10 and abs(row['P_residual'])<1e-9
# Deliberate unresolved direct carrier: N64 aliases k128 to zero. It must fail the physical momentum check.
_,_,bad0,bad=run(64,False);badP=abs(bad0['P']-boost);assert badP>.5*boost
after={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};assert before==after;(P/'phase_factored_benchmark.json').write_text(json.dumps(dict(started_utc=start,software=dict(Python=platform.python_version(),numpy=np.__version__),scope='one-dimensional periodic mean-subtracted Poisson toy; exact constant-gradient carrier; no 3D radial/amplitude or variable-phase galaxy solver',eta=eta,carrier=carrier,boost=boost,G_toy=G,T=T,dt=dt,reference_N=1024,results=rows,direct_N64_alias_momentum_error=badP,unresolved_direct_control_rejected=True,source_hashes_before=before,source_hashes_after=after,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n');print(rows);print('unresolved direct N64 momentum error',badP)
