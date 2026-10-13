"""Tree-level elastic kinematics for one outgoing daughter at rest."""
import json,math
from pathlib import Path
import numpy as np
p=Path(__file__).parent
pars=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
prod=json.loads((p/'detuned_bogoliubov_run/results.json').read_text())
m=pars['m_eV'];M=pars['M_eV'];D=M*M-4*m*m;gap=M-2*m
checks=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
E=M/2;p0=math.sqrt(D)/2
cosine=gap/(M+2*m);s=2*m*M;x=(s-4*m*m)/D
eta=1-2*m/M
ck('shell energy momentum conservation',abs(2*p0*p0*(1+cosine)-((M-m)**2-m*m))<1e-10)
ck('shell amplitude identity',abs((1-x/(1-x))-eta)<1e-10)
rows=[]
for alpha in [1.,1.5,2.]:
    amp=alpha-x/(1-x)
    k=(1+alpha)*pars['lambda_min']/(4*m*m)
    c=pars['cubic_g_eV']/(2*m*math.sqrt(2*M))
    residual=k-c*c/gap
    r2=c*c/(gap*k);beta=(1+1/math.sqrt(1-r2))/2
    ck('positive NR square residual '+str(alpha),residual>0)
    rows.append(dict(alpha=alpha,amplitude_over_lambda_min=amp,amplitude_over_threshold=amp/alpha,cross_section_over_own_threshold=(amp/alpha)**2*(4*m*m/s),threshold_cross_section_cm2_g=alpha**2,positive_NR_residual=residual,pressure_upper_multiplier=beta))
radial=[]
for row in prod['rows'][:3]:
    q=np.asarray(row['initial_mode_p_over_m']); w=np.asarray(row['final_pair_fractions']);w=w/w.sum()
    p1=m*q[:,None];p2=m*q[None,:]
    e1=m*np.sqrt(1+q[:,None]**2);e2=m*np.sqrt(1+q[None,:]**2)
    et=e1+e2;sij=2*m*et
    # Required angle from |p1+p2|²=(Etotal-m)²-m².
    co=((et-m)**2-m*m-p1*p1-p2*p2)/(2*p1*p2)
    xx=(sij-4*m*m)/D;weight=w[:,None]*w[None,:]
    out=dict(K=row['K'],vmax=row['vmax'],all_pairs_kinematically_allowed=bool(np.all(abs(co)<=1)),x_min=float(xx.min()),x_max=float(xx.max()))
    for alpha in [1.,2.]:
        a=(alpha-xx/(1-xx))/alpha
        out['alpha'+str(alpha)+'_weighted_amplitude_squared']=float(np.sum(weight*a*a))
    ck('radial channel accessible '+str(row['K']),out['all_pairs_kinematically_allowed'])
    radial.append(out)
out=dict(shell=dict(p_over_m=p0/m,required_incoming_cosine=cosine,invariant_s_eV2=s,x=x,alpha1_amplitude_suppression=eta),variants=rows,radial_band_proxies=radial,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Tree amplitude is not a medium rate or condensate growth prediction','Radial weights form an amplitude proxy, not a collision integral','Alternative alpha variants require their own production and transport tests'])
(p/'condensate_channel_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
