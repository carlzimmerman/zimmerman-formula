import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
from scipy.integrate import quad

def gauss(x,s=1,mu=0):return math.exp(-0.5*((x-mu)/s)**2)/(math.sqrt(2*math.pi)*s)
def calculate():
    err=max(abs(quad(lambda y:gauss(y)*gauss(x-y),-math.inf,math.inf,epsabs=1e-12)[0]-gauss(x,math.sqrt(2))) for x in [0,1,3])
    mass=quad(lambda x:gauss(x,math.sqrt(2)),-math.inf,math.inf,epsabs=1e-12)[0]
    mean=quad(lambda x:x*gauss(x,math.sqrt(2)),-math.inf,math.inf,epsabs=1e-12)[0]
    mut=quad(lambda x:x*gauss(x,math.sqrt(2),3),-math.inf,math.inf,epsabs=1e-12)[0]
    checks={'known_answer':err<=1e-10,'mass':abs(mass-1)<=1e-10,'centroid':abs(mean)<=1e-10,'mutate_bites':abs(mut)>1 and abs(mut-3)<=1e-10}
    label='FAIL' if all(checks.values()) else 'NO VERDICT'
    return {'assertion_tested':'positive centred Gaussian transport cannot shift one gas clump peak','label':label,'bounds':{'convolution_x':[0,1,3],'widths':[1,1],'integration_domain':'real line','mutate_offset':3},'scope':'synthetic mechanism counterexample only','footings':{f:{'label':label,'peak':0,'required_synthetic_peak':3,'peak_margin':-3,'centroid':mean,'mutate_centroid':mut,'known_answer_error':err,'normalization_error':abs(mass-1),'empirical_label':'NOT EVALUABLE'} for f in ['canonical','alt']},'free_physical_numbers':['kappa=1/2 FITTED','physical transport width and amplitude not supplied; would be FITTED'], 'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'residual_risks':['not a two-clump Bullet calculation','signed or anisotropic kernels not excluded']}
record(__file__,calculate)
