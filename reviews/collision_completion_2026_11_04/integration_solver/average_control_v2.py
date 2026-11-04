"""Independent metamorphic phase-helper control, before actual angular use."""
from protocol_control import *
from protocol_average import AveragedNumberEvents
class ScaledBackend(ToyNumberBackend):
 def __init__(self,scale):
  super().__init__([2.,3.,.1]);self.scale=scale;self.omitted_by_parent=np.array([.1,.2,.3])*scale;self.included_by_parent=np.ones(3)*scale
 def number_rhs(self,f,availability=None):return self.scale*super().number_rhs(f,availability)
 def number_jacobian(self,f,availability=None):return self.scale*super().number_jacobian(f,availability)
 def number_gross(self,f,availability=None):return self.scale*super().number_gross(f,availability)
def main_average(out):
 start=time.monotonic();a=ScaledBackend(1.);b=ScaledBackend(2.);av= AveragedNumberEvents([a,b],[.25,.75],[1.,2.]);state=QuantumState(a.measure,a.eta,Y=a.measure*np.array([.3,.2,.7]));f,p=state.arrays();factor=1.75;rhs_error=float(max(abs(av.number_rhs(f,p)-factor*a.number_rhs(f,p))));jac_error=float(max(abs((av.number_jacobian(f,p)-factor*a.number_jacobian(f,p)).toarray()).ravel()));gross_error=float(max(abs(av.number_gross(f,p)-factor*a.number_gross(f,p))));m=av.forward_omission(f);new,diag=implicit_step(av,state,.1,tol=2e-10);nf,np_=new.arrays();checks=dict(rhs=rhs_error<1e-14,jacobian=jac_error<1e-14,gross=gross_error<1e-14,local_energy=float(max(abs(av.local_energy_rates(f,p))))<1e-14,phase_weights=abs(sum(av.phase_weights)-1)<1e-15,omission=m['available'] and 0<m['occupied_forward_omitted_fraction']<1,physical_step=min(nf)>=0 and max(nf[[0,2]])<=1);checks={k:bool(v) for k,v in checks.items()};result=dict(claim_id='CC10_AVERAGED_NUMBER_PROTOCOL_CONTROL',checks=checks,rhs_error=rhs_error,jacobian_error=jac_error,gross_error=gross_error,omission=m,newton=diag,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main_average(sys.argv[1])
