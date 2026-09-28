"""Bounded FGF-017 relative-catalogue calculation. Only writes --out."""
import sys
sys.dont_write_bytecode = True
import argparse, csv, json, math
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0,str(ROOT))
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.optimize import brentq
from campaign_fresh_gravity_astra.stage_03.cluster_precision.constraint import force, G, MSUN, KPC, NORMS, LG, HG
BASE=ROOT/'campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002'
DATA=ROOT/'real_research/data'
checks=[]
def check(name, actual, tolerance, passed):
    checks.append(dict(name=name,actual=actual,tolerance=tolerance,passed=bool(passed)))
    assert passed,(name,actual,tolerance)
def save(p,x): p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def csvsave(p,rows):
    with p.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
class Curve:
    def __init__(self,r,m):
        self.r=np.array(r,float);self.x=np.log(self.r); self.m=np.array(m,float);self.y=np.log(self.m)
        assert np.all(np.diff(self.r)>0) and np.all(self.m>0)
        self.s=np.diff(self.y)/np.diff(self.x)
    def val(self,r):
        assert self.r[0]*(1-1e-13)<=r<=self.r[-1]*(1+1e-13)
        return float(np.exp(np.interp(np.log(r),self.x,self.y)))
    def slope_in(self,r):
        i=np.clip(np.searchsorted(self.r,r,side='right')-1,0,len(self.s)-1)
        return float(self.s[i])
class Diff:
    def __init__(self,c,e=None):self.c=c;self.e=e
    def val(self,r):return self.c.val(r)-(self.e.val(r) if self.e else 0)
    def slopes(self,left,right):
        mid=math.sqrt(left*right);s=self.c.slope_in(mid)
        if self.e is None:return s,s
        t=self.e.slope_in(mid)
        v=[(s*self.c.val(r)-t*self.e.val(r))/self.val(r) for r in (left,right)]
        return min(v),max(v)

def main(out):
    out.mkdir(exist_ok=True,parents=True)
    zdata=json.loads((DATA/'xcop/xcop_r500_ettori2019.json').read_text())
    old=list(csv.DictReader((BASE/'closure_requirements.csv').open()))
    nom=list(csv.DictReader((BASE/'gas_comparison.csv').open()))
    matches=list(csv.DictReader((BASE/'catalogue_matches.csv').open()))
    slopeM=np.diff(HG)/np.diff(LG)/np.log(10)
    check('registered_M_positive_slopes',float(np.min(slopeM)),0,np.all(slopeM>0))
    check('registered_M_elasticity_at_most_one',float(np.max(slopeM/HG[:-1])),1,np.all(slopeM<=HG[:-1]))
    metadata={'catalogue_headers':{},'objects':{},'missing_metadata':['Actual eRASS angular aperture paired to R500 and an authenticated DA conversion','Common cosmology and its propagation to rho_Lambda/a','Centre-matched profiles or correction for measured offsets','Independent emissivity bound and pressure-gradient calibration','Uniform-density-shape premise not established by integral gas mass']}
    with fits.open(DATA/'erass1cl_primary_v3.2.fits',memmap=True) as hd:
        cat=hd[1].data.copy()
        metadata['catalogue_headers']={str(i):str(h.header) for i,h in enumerate(hd)}
        metadata['catalogue_columns']=[{'name':c.name,'unit':c.unit} for c in hd[1].columns]
    ec=SkyCoord(np.asarray(cat['RA'],float)*u.deg,np.asarray(cat['DEC'],float)*u.deg)
    allrows=[]; summaries=[]; maxres=0.;maxnom=0.; maxmon=0.; bracket_y=[float('inf'),0.]; allcells=0
    for name in ('A644','ZW1215'):
        profiles={};knots=[];rawmeta={}
        for kind,ext,key,error in [('fgas_profile',1,'MGAS','MGAS_LO'),('hydro_mass',1,'M_FORW','EM_FORW'),('mstar',2,'MSTAR','MSTAR_HI')]:
            path=DATA/'xcop'/name/(name+'_'+kind+'.fits')
            with fits.open(path) as hd:
                h=hd[ext];unit=h.columns['RADIUS'].unit
                conv={'kpc':1.,'Mpc':1000.,'R/R500':h.header.get('R500')}[unit]
                assert conv>0
                r=np.asarray(h.data['RADIUS'],float)*conv
                assert h.columns[key].unit in ('Msun','M_sun') and h.columns[error].unit in ('Msun','M_sun')
                profiles[kind]=(Curve(r,h.data[key]),Curve(r,h.data[error]));knots.extend(r)
                rawmeta[kind]={'header':str(h.header),'radius_unit':unit,'radius_multiplier_to_kpc':conv,'support_kpc':[float(r[0]),float(r[-1])],'mass_units':{key:h.columns[key].unit,error:h.columns[error].unit}}
                if kind=='mstar':ra,dec=float(h.header['RA']),float(h.header['DEC'])
        sep=SkyCoord(ra*u.deg,dec*u.deg).separation(ec).arcmin
        j=int(np.argmin(sep));e=cat[j];z=zdata[name]['z'];Re=float(e['R500']);Me=float(e['MGAS500'])*1e11;Mehi=float(e['MGAS500_H'])*1e11
        accepted=next(x for x in matches if x['name']==name)
        check(name+'_nearest_match',str(e['NAME']).strip(),accepted['erass_nearest_name'],str(e['NAME']).strip()==accepted['erass_nearest_name'] and sep[j]<=5 and abs(float(e['BEST_Z'])-z)<=.01)
        lo=max(v[0].r[0] for v in profiles.values());hi=min(v[0].r[-1] for v in profiles.values())
        radii=sorted(set([float(lo),float(hi),Re]+[float(r) for r in knots if lo<r<hi]))
        check(name+'_nominal_supported',Re,[float(lo),float(hi)],lo<Re<hi)
        metadata['objects'][name]={'profiles':rawmeta,'erass_name':str(e['NAME']).strip(),'erass_R500_kpc':Re,'erass_gas_msun':Me,'erass_gas_high_msun':Mehi,'z_erass':float(e['BEST_Z']),'z_xcop':z,'offset_arcmin':float(sep[j]),'common_support_kpc':[float(lo),float(hi)],'relative_distance_support':[float(lo/Re),float(hi/Re)],'knots':len(radii),'catalogue_row':{k:float(e[k]) for k in ('R500','MGAS500','MGAS500_L','MGAS500_H','BEST_Z','KT','KT_L','KT_H')}}
        gc,ge=profiles['fgas_profile'];hc,he=profiles['hydro_mass'];sc,shi=profiles['mstar']
        for corner in ('central','favorable'):
            X=Diff(gc,ge if corner=='favorable' else None);H=Diff(hc,he if corner=='favorable' else None);S=Diff(shi if corner=='favorable' else sc);me=Mehi if corner=='favorable' else Me
            check(name+'_'+corner+'_positive_masses',min(min(X.val(r),H.val(r),S.val(r)) for r in radii),0,all(min(X.val(r),H.val(r),S.val(r))>0 for r in radii))
            # Positivity over every interval follows because each difference is between two power laws; their ratio is monotone there.
            for footing,a0 in NORMS.items():
                for history in ('vacuum','H'):
                    a=a0*(1 if history=='vacuum' else math.sqrt(.315*(1+z)**3+.685))
                    for kernel in ('Q','R','M'):
                        cache={}
                        def solve(r):
                            nonlocal maxres,maxmon
                            if r in cache:return cache[r]
                            x,h,s=X.val(r),H.val(r),S.val(r);C=G*MSUN/(r*KPC)**2;d=r/Re
                            def p(logeta):
                                eta=math.exp(logeta)
                                return eta*float(force(C*(eta*x+s),a,kernel))/(C*h)
                            ends=[C*(math.exp(t)*x+s)/a for t in (-20.,20.)]
                            bracket_y[0]=min(bracket_y[0],*ends);bracket_y[1]=max(bracket_y[1],*ends)
                            pl,pu=p(-20.),p(20.);assert pl<1<pu
                            root=brentq(lambda t:math.log(p(t)),-20,20,xtol=1e-13,rtol=1e-14)
                            eta=math.exp(root);ell=(me*d**2.5/(eta*x))**2
                            residual=abs(p(root)-1);maxres=max(maxres,residual)
                            assert p(root-1e-5)<1<p(root+1e-5)
                            mono=max(0,p(root-1e-5)-1,1-p(root+1e-5));maxmon=max(maxmon,mono)
                            v={'radius_kpc':r,'d':d,'eta_root':eta,'ell_crit':ell,'p_at_ell_1':p(math.log(me*d**2.5/x)),'forward_residual':residual}
                            cache[r]=v;return v
                        values=[solve(r) for r in radii]
                        ref=next(t for t in old if t['name']==name and t['footing']==footing and t['scaling']==history and t['kernel']==kernel)
                        rr=solve(Re);pk='pressure_gradient_ratio_box_high' if corner=='favorable' else 'pressure_gradient_ratio_required';ek='largest_emissivity_ratio_that_can_close_box' if corner=='favorable' else 'emissivity_ratio_required_fixed_counts_distance'
                        maxnom=max(maxnom,abs(rr['p_at_ell_1']/float(ref[pk])-1),abs(rr['ell_crit']/float(ref[ek])-1))
                        uppers=[];crossings=[];ambiguous=[];monotone=0
                        for l,r in zip(radii[:-1],radii[1:]):
                            sx=X.slopes(l,r);sh=H.slopes(l,r);ss=S.slopes(l,r)
                            dl=4.5-sx[1]-sh[1]+min(0,ss[0]-2);du=4.5-sx[0]-sh[0]+max(.5,ss[1]-2)
                            vl,vr=math.log(solve(l)['ell_crit']),math.log(solve(r)['ell_crit']);width=math.log(r/l)
                            if dl>0 or du<0:
                                upper=max(vl,vr);lower=min(vl,vr);monotone+=1
                            else:
                                L=2*max(abs(dl),abs(du));upper=max(vl,vr)+L*width/2;lower=min(vl,vr)-L*width/2
                            uppers.append(math.exp(upper));allcells+=1
                            if vl*vr<0:
                                cr=math.exp(brentq(lambda lr:math.log(solve(math.exp(lr))['ell_crit']),math.log(l),math.log(r),xtol=1e-13))
                                crossings.append({'d':cr/Re,'r_kpc':cr,'ell_crit':solve(cr)['ell_crit'],'unique_on_cell':bool(dl>0 or du<0),'cell_d':[l/Re,r/Re]})
                            elif lower<=0<=upper:ambiguous.append([l/Re,r/Re])
                        key=dict(name=name,corner=corner,footing=footing,history=history,kernel=kernel,a=a)
                        for row in sorted(cache.values(),key=lambda t:t['d']):allrows.append(dict(**key,**row))
                        summaries.append(dict(**key,nominal=rr,sampled_max_ell=max(v['ell_crit'] for v in cache.values()),support_upper_bound_ell=max(uppers),cells=len(radii)-1,certified_monotone_cells=monotone,distance_only_crossings=crossings,unresolved_distance_only_cells=ambiguous))
    check('nominal_48_curve_recovery_relative',maxnom,1e-9,maxnom<1e-9)
    check('root_forward_recovery',maxres,1e-10,maxres<1e-10)
    check('root_monotonic_perturbations',maxmon,0,maxmon==0)
    check('registered_M_all_brackets_in_domain',bracket_y,[1e-12,1e12],bracket_y[0]>=1e-12 and bracket_y[1]<=1e12)
    check('all_branches_corners_present',len(summaries),48,len(summaries)==48)
    csvsave(out/'curves.csv',allrows);save(out/'summary.json',summaries);save(out/'metadata.json',metadata)
    save(out/'checks.json',{'checks':checks,'curve_rows':len(allrows),'intervals_bounded':allcells,'arithmetic':'binary64; analytic slope enclosure with no directed rounding','seed':None,'extrapolations':0})
    print(json.dumps({'curve_rows':len(allrows),'intervals_bounded':allcells,'max_forward_residual':maxres,'max_nominal_error':maxnom,'checks':len(checks),'objects':{n:{'sampled_favorable_max':max(s['sampled_max_ell'] for s in summaries if s['name']==n and s['corner']=='favorable'),'support_favorable_upper_bound':max(s['support_upper_bound_ell'] for s in summaries if s['name']==n and s['corner']=='favorable'),'distance_only_roots':[s['distance_only_crossings'] for s in summaries if s['name']==n and s['corner']=='favorable' and s['distance_only_crossings']],'ambiguous_cells':sum(len(s['unresolved_distance_only_cells']) for s in summaries if s['name']==n)} for n in ('A644','ZW1215')}},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);main(ap.parse_args().out)
