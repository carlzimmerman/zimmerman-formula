"""Independent Q quartic and R bisection spot checks against original FITS."""
import json,sys,math
from pathlib import Path
import numpy as np
from astropy.io import fits

P=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-017/fgf017_run_001')
summary=json.loads((P/'run_001/summary.json').read_text())
meta=json.loads((P/'run_001/metadata.json').read_text())
G=6.67430e-11;MSUN=1.98847e30;KPC=3.085677581491367e19
def interp(name,kind,ext,col,r):
    path=Path('real_research/data/xcop')/name/(name+'_'+kind+'.fits')
    with fits.open(path) as f:
        h=f[ext]; unit=h.columns['RADIUS'].unit
        fac={'kpc':1,'Mpc':1000,'R/R500':h.header.get('R500')}[unit]
        rr=np.array(h.data['RADIUS'],float)*fac; yy=np.array(h.data[col],float)
        assert rr[0]<=r<=rr[-1]
        return float(np.exp(np.interp(np.log(r),np.log(rr),np.log(yy))))
rows=[]
for s in summary:
    if s['kernel'] not in ['Q','R']:continue
    name=s['name']; obj=meta['objects'][name]; favorable=s['corner']=='favorable'
    tests=[(1.,s['nominal']['ell_crit'])]+[(v['d'],1.) for v in s['distance_only_crossings']]
    for d,reference in tests:
        r=d*obj['erass_R500_kpc']
        X=interp(name,'fgas_profile',1,'MGAS',r)
        H=interp(name,'hydro_mass',1,'M_FORW',r)
        if favorable:
            X-=interp(name,'fgas_profile',1,'MGAS_LO',r)
            H-=interp(name,'hydro_mass',1,'EM_FORW',r)
        S=interp(name,'mstar',2,'MSTAR_HI' if favorable else 'MSTAR',r)
        C=G*MSUN/(r*KPC)**2; bg=C*X; bs=C*S; gh=C*H; a=s['a']
        if s['kernel']=='Q':
            beta=bg/gh;sigma=bs/gh;alpha=a/gh
            roots=np.roots([beta*beta,beta*(2*sigma+alpha),sigma*(sigma+alpha),0,-1])
            positive=[z.real for z in roots if abs(z.imag)<1e-10 and z.real>0]
            assert len(positive)==1; eta=positive[0]
        else:
            def h(eta):
                B=eta*bg+bs
                return eta*B/(-math.expm1(-math.sqrt(B/a)))/gh
            lo=0.;hi=1.
            while h(hi)<1:hi*=2
            for _ in range(90):
                mid=(hi+lo)/2
                if h(mid)<1:lo=mid
                else:hi=mid
            eta=(lo+hi)/2
        me=obj['erass_gas_high_msun' if favorable else 'erass_gas_msun']
        ell=(me*d**2.5/(eta*X))**2
        residual=abs(ell/reference-1)
        assert residual<1e-9
        rows.append({'name':name,'kernel':s['kernel'],'corner':s['corner'],'footing':s['footing'],
                     'history':s['history'],'d':d,'ell':ell,'reference':reference,'relative_error':residual})
out={'scope':'Q quartic and R linear-eta bisection at nominal and reported crossing points; original FITS independently parsed. No M or full-support envelope audit.',
     'cases':rows,'max_relative_error':max(x['relative_error'] for x in rows),'all_checks_pass':True}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(len(rows),out['max_relative_error'])
