"""Long-wavelength phase mode derived from the full two-complex-field action."""
import json,math
from pathlib import Path
import numpy as np
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())['softened']
m=params['m_eV'];g=params['cubic_g_eV'];Delta=4*m*m*params['u']**2;lam=params['lambda_']
Astar=portal['Astar_eV2'];S0=portal['S0_eV2'];c=299792458.
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def branch(n):
 beta=2*lam*n/Delta;gamma=2*g*g*n/(Delta*Delta)
 root=math.sqrt((1-4*beta)**2+16*gamma)
 d=Delta*2*(beta-gamma)/(1+4*beta+root)
 den=Delta-4*d;s=-g*n/den;S=n+4*s*s
 dp=(2*lam-2*g*g/den)/(1+8*g*g*n/(den*den))
 sp=-g/den-4*g*n*dp/(den*den);Sp=1+8*s*sp
 x=S/S0;r=math.hypot(1,x);Up=Astar*x/r;Upp=Astar/S0/r**3
 X=m*m+Up+d;dXdS=Upp+dp/Sp
 sound=S*dXdS/(2*X+S*dXdS)
 rr=math.sqrt(n);Hrr=8*lam*n+4*n*Upp;Hss=2*den+64*s*s*Upp;Hrs=4*g*rr+16*rr*s*Upp
 hessian=np.array([[Hrr,Hrs],[Hrs,Hss]])/Delta
 return dict(n=n,s=s,S=S,d=d,den=den,X=X,shift=Up+d,Sp=Sp,dXdS=dXdS,
             sound=sound,NR_sound=S*Upp/(2*m*m),hessian=hessian,
             source_charge_fraction=4*s*s/S)
rows=[]
for x in [.01,.1,1.,10.,100.]:
 a=branch(x*S0);n=a['n'];s=a['s'];d=a['d'];h=1e-4
 check('daughter stationary equation',abs((2*g*s+2*lam*n)/d-1)<1e-12)
 check('source stationary equation',abs(a['den']*s/(g*n)+1)<1e-12)
 check('positive amplitude grand-potential Hessian',np.min(np.linalg.eigvalsh(a['hessian']))>0)
 check('positive relative-phase curvature',-2*g*s*n>0)
 plus=branch(n*(1+h));minus=branch(n*(1-h))
 fd=(plus['shift']-minus['shift'])/(plus['S']-minus['S'])
 check('implicit chemical-potential derivative',abs(fd/a['dXdS']-1)<3e-7)
 check('subluminal positive phase sound speed',0<a['sound']<1)
 rows.append(dict(S_over_S0=a['S']/S0,source_charge_fraction=a['source_charge_fraction'],
                 sound_speed_kms=c*math.sqrt(a['sound'])/1000,
                 NR_pressure_speed_kms=c*math.sqrt(a['NR_sound'])/1000,
                 sound_squared_relative_NR_difference=a['sound']/a['NR_sound']-1,
                 amplitude_hessian_eigenvalues_over_Delta=np.linalg.eigvalsh(a['hessian']).tolist()))
out=dict(all_pass=all(t['passed'] for t in checks),checks=checks,rows=rows,
 non_claims=['Coherent phase-locked stationary branch only, not produced mixed distribution',
 'Low-frequency adiabatic amplitude elimination; no complete finite-k mode spectrum',
 'No cosmological transfer function, nonlinear stability or halo-law derivation'])
(p/'portal_coherent_modes_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
