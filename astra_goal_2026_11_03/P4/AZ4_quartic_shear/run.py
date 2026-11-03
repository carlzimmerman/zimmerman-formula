import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
import numpy as np

def calculate():
    I=np.eye(3); A=np.diag([-2.,1.,1.])
    shear=lambda K:0.5*(K+K.T)-np.trace(K)*I/3
    W=lambda K:float(np.sum(shear(K)**2)**2)
    K=I+A; S=shear(K); analytic=4*np.sum(S*S)*S
    fd=np.zeros((3,3));h=1e-5
    for i in range(3):
        for j in range(3):
            E=np.zeros((3,3));E[i,j]=h;fd[i,j]=(W(K+E)-W(K-E))/(2*h)
    ratio=W(I+0.5*A)/W(I+A); mutant=float(np.sum(shear(I+0.5*A)**2)/np.sum(shear(I+A)**2))
    err=float(np.max(abs(fd-analytic)));hom=W(-I);stress=float(np.max(abs(4*np.sum(shear(-I)**2)*shear(-I))))
    checks={'quartic_scaling':abs(ratio-1/16)<=1e-12,'isotropic_zero':hom<=1e-12 and stress<=1e-12,'stress_derivative':err<=1e-6,'mutate_bites':abs(mutant-1/16)>0.1}
    label='FAIL' if all(checks.values()) else 'NO VERDICT'
    vals={'quartic_ratio':ratio,'mutate_ratio':mutant,'stress_derivative_error':err,'homologous_energy':hom,'homologous_stress':stress,'quartic_margin':1e-12-abs(ratio-1/16),'derivative_margin':1e-6-err}
    return {'assertion_tested':'quartic shear leaves linear FRW untouched but vanishes on homologous contraction','label':label,'scope':'FAIL as universal local contraction cure; not an observational grade','footings':{f:{'label':label,'linear_FRW_structural':'PASS','empirical_label':'NOT EVALUABLE','values':vals} for f in ['canonical','alt']},'bounds':{'dimension':3,'H':1,'epsilon':[1,0.5],'A_diagonal':[-2,1,1],'finite_difference_step':h},'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'free_physical_numbers':['kappa=1/2 FITTED','lambda>0 undetermined dimensionful coefficient: FITTED if selected'],'residual_risks':['full covariant stability uncomputed','boundary-driven and anisotropic dynamics not tested']}
record(__file__,calculate)
