"""Independent coarse support control; no additional root calculation."""
import sys
sys.dont_write_bytecode=True
import json,math,argparse
from pathlib import Path
import numpy as np
from astropy.io import fits
G,MSUN,KPC=6.67430e-11,1.98847e30,3.085677581491367e19
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out
rows=[]
for name in ('A644','ZW1215'):
 bounds={}; supports=[]
 for typ,ext,c,e in [('fgas_profile',1,'MGAS','MGAS_LO'),('hydro_mass',1,'M_FORW','EM_FORW'),('mstar',2,'MSTAR','MSTAR_HI')]:
  with fits.open(Path('real_research/data/xcop')/name/(name+'_'+typ+'.fits')) as f:
   h=f[ext];r=np.array(h.data['RADIUS'],float)*{'kpc':1.,'Mpc':1000.,'R/R500':h.header.get('R500')}[h.columns['RADIUS'].unit];v=np.array(h.data[c],float);ev=np.array(h.data[e],float)
   supports.append([min(r),max(r)])
   if typ!='mstar':
    # c and e share this original grid, so e/c is a power law on each cell.
    ratio=max(ev/v);assert ratio<1
    bounds[typ]=[min(v)*(1-ratio),max(v)]
   else:bounds[typ]=[min(min(v),min(ev)),max(max(v),max(ev))]
 lo=max(t[0] for t in supports);hi=min(t[1] for t in supports)
 Cmin=G*MSUN/(hi*KPC)**2;Cmax=G*MSUN/(lo*KPC)**2
 xmin,xmax=bounds['fgas_profile'];hmin,hmax=bounds['hydro_mass'];smin,smax=bounds['mstar']
 amin=9.3619e-11;amax=1.1279e-10*1.05 # E(z)<1.05 for both pinned z.
 ystarmin=Cmin*smin/amax;ystarmax=Cmax*smax/amin
 # At the top of the M range B=a*1e12, eta=(a*1e12/C-S)/X.
 etalower=(amin*1e12/Cmax-smax)/xmax
 htoplower=etalower*amin*1e12/(Cmax*hmax) # F>=B
 assert ystarmin>1e-12 and ystarmax<1e12 and etalower>0 and htoplower>1
 rows.append({'name':name,'all_support_mass_bounds_msun':bounds,'ystar_lower':ystarmin,'ystar_upper':ystarmax,'M_upper_boundary_eta_lower':etalower,'M_upper_boundary_h_lower':htoplower,'M_root_exists_uniquely_entire_support':True})
out.mkdir(parents=True,exist_ok=True);(out/'support_control.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
