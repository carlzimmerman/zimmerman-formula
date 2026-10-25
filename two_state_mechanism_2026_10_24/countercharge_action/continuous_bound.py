import argparse,json,math
from pathlib import Path
from experiment import G,HBAR,C,A0,GEV_KG,MSUN,KPC,ETA,PROFILES

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
eps=1e-4;rows=[]
for margin in (1.,10.):
    m=(HBAR**2*math.sqrt(A0)*(1+eps)/(margin*G**1.5*eps))**(2/7)
    mu=eps*m/(1+eps);alpha=G*m*m/(HBAR*C)
    bohr=HBAR/(mu*C*alpha);core=math.sqrt(G*m/A0)
    ratios=[]
    for M,b in PROFILES:
        v2=G*(1+ETA)*M*MSUN/(b*KPC)
        ratios.append(3*eps/(1+eps)**2*alpha**2*C*C/v2)
    assert abs(bohr/core/margin-1)<1e-12
    assert alpha<.1
    rows.append(dict(core_margin=margin,epsilon=eps,m_max_GeV=m/GEV_KG,alpha_G=alpha,
                     bohr_m=bohr,core_m=core,upper_binding_over_T=ratios))
Path(a.output).write_text(json.dumps(dict(bound='continuous m>0, epsilon in[1e-4,1], specified Coulomb/virial assumptions',rows=rows),indent=2)+'\n')
print(json.dumps(rows,indent=2))
