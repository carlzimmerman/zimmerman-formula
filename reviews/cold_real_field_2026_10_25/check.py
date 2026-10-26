import argparse,json,subprocess,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
source=Path(__file__).with_name('evolve.cpp');binary=out/'evolve';subprocess.run(['clang++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True)
cases=[(0,.5,3),(0,1.2,3),(0,1.6,3),(0,1.6,6),(60,.8,3)];rows=[]
C=299792458.;G=6.67430e-11;PC=3.085677581491367e16;MS=1.98847e30;Dmass=.75*3*(1.8e-18)**2/(8*math.pi*G);omega=C*C/(1500*PC*1000)/(2.4*math.sqrt(5/6));L=C/omega;kappa=8*math.pi*G*Dmass*L*L/(C*C);massunit=Dmass*L**3/MS
for i,(d,amp,width) in enumerate(cases):
 stem=out/f'case_{i}';subprocess.run([str(binary),str(stem),str(d),str(amp),str(width),'60','.05','.005','200',str(int(a.mutate))],check=True)
 row=json.load(open(str(stem)+'.json'));row.update(d=d,amplitude=amp,width=width,metric_excitation_bound=kappa*row['max_integrated_energy_over_radius'],late_core_Msun=massunit*row['late_core_mean']);rows.append(row)
result=dict(scope='Direct spherical real-field PDE in controlled weak-metric regime; not full Einstein evolution',kappa=kappa,length_unit_pc=L/PC,time_unit_years=1/omega/(365.25*86400),mass_unit_Msun=massunit,rows=rows)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
