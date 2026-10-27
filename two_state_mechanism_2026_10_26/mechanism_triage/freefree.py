"""Conditional ionized, optically thin free-free emission times; not net halo cooling."""
import argparse,json,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent
profiles=json.loads((b/'run/results.json').read_text())['rows'];hb=1.054571817e-34;c=299792458.;kg=1.7826619216279e-36;Gyr=365.25*86400*1e9;kpc=3.085677581491367e19;Cff=16/3*math.sqrt(2*math.pi/3);rows=[]
for mass in [1e6,3.162277660168379e6,1e7,3.162277660168379e7,1e8]:
 alpha=.01;aD=hb/(mass*kg*c*alpha);td=hb/(alpha**2*mass*kg*c*c)
 for r in profiles:
  nreal=r['rho']/(101*mass*kg);n=nreal*aD**3;T=101*(1000*r['sigma_km_s'])**2/(2*c*c*alpha**2)
  time=3*math.sqrt(T)/(Cff*alpha**3*n)*td/Gyr
  # Analytic fixed-density fully ionized solution, only until the excitation scale.
  toline=2*time*(1-math.sqrt(.375/T)) if T>.375 else None
  elapsed=min(10,toline) if toline is not None else 0
  final=(math.sqrt(T)-elapsed*Gyr/td*Cff*alpha**3*n/6)**2
  emitted=3*(T-final);ledger=abs(3*final+emitted-3*T);assert ledger<1e-12
  thomson=8*math.pi/3*(alpha*hb/(mass*kg*c))**2
  photo_threshold=512*math.pi**2/(3*math.e**4)*alpha*aD**2
  rows.append(dict(mass_eV=mass,alpha=alpha,Mb=r['Mb'],r_kpc=r['r_kpc'],T_Hartree=T,excitation_gap_over_T=.375/T,ionized_thin_emission_time_Gyr=time,time_to_line_scale_Gyr=toline,ledger_error=ledger,Thomson_tau=nreal*thomson*r['r_kpc']*kpc,neutral_fraction_for_unit_threshold_opacity=1/(nreal*photo_threshold*r['r_kpc']*kpc),initially_above_line=T>.375))
# Check the universal mass-cubed scaling at fixed alpha, rho and velocity.
for i in range(4):assert abs(rows[8+i]['ionized_thin_emission_time_Gyr']/rows[i]['ionized_thin_emission_time_Gyr']-1000)<1e-9
Path(a.output).write_text(json.dumps(dict(rows=rows,Gaunt_factor=1,approximation='Nonrelativistic Maxwellian fully ionized common-temperature fixed-density emissivity; mX >> mC; photons assumed to escape. No ionization or opacity evolution. Not a physical cooling trajectory or galaxy separation.',source='https://arxiv.org/pdf/1705.10341 equation 8'),indent=2)+'\n')
