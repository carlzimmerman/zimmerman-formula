"""Reproduce conditional abundance and nonlinear-source diagnostic scalings."""
import json,sys,math
from pathlib import Path
p=Path(__file__).parent
rows=json.loads((p/'physical_spectrum_wkb2_v2_run/results.json').read_text())['rows']
m=.001;M=2*m*math.sqrt(1+.02**2);g=2.168e-6;Mpl=2.435e18;gstar=106.75;Ne=60
target=4.37e-10/m
Tcom=(90/(math.pi**2*gstar))**.25*math.sqrt(Mpl*m)
scom=2*math.pi**2/45*gstar*Tcom**3
yields=[m**3*(r['species'][0]['n_comoving']+2*r['species'][1]['n_comoving'])/scom for r in rows]
Tosc=(90/(math.pi**2*gstar))**.25*math.sqrt(Mpl*M)
sosc=2*math.pi**2/45*gstar*Tosc**3
Xneeded=math.sqrt(target*sosc/(2*M));Xcrit=m*m/(2*g)
out=dict(asymptotic_yields=yields,abundance_fraction=yields[-1]/target,
    mass_if_other_dimensionless_ratios_fixed_GeV=m*(yields[-1]/target)**(-.4),
    free_source_estimate=dict(N_e=Ne,H_osc_GeV=M,T_osc_GeV=Tosc,
        X_required_GeV=Xneeded,H_inf_required_GeV=2*math.pi*Xneeded/math.sqrt(Ne),
        X_tachyon_threshold_GeV=Xcrit,threshold_ratio=Xneeded/Xcrit,
        maximum_subthreshold_abundance_fraction=(Xcrit/Xneeded)**2),
    checks=dict(spectrum_yield_agreement=abs(yields[0]/yields[1]-1)<1e-5,
                required_source_exceeds_tachyon_threshold=Xneeded>Xcrit),
    scope='Algebraic diagnostics of declared free-spectator and free-condensate assumptions; threshold failure invalidates the latter abundance estimate as a prediction.')
out['all_pass']=all(out['checks'].values())
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
