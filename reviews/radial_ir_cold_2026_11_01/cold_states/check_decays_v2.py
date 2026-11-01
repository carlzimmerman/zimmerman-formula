"""Bounded TP04 decay and source checks. No population or scale is selected."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from model import build_model,SU5_D
from spectrum import T
from gaugino_threshold import threshold,ext_basis,summarize,Z0

def groups_low(v):
    p=v[v>0];a=p.min()
    return np.where(abs(v/a-1)<1e-7)[0]

def one(e):
    X=Z0/math.sqrt(31*e);g=math.sqrt(29/200)*e
    d=build_model(X,e,e,g,vertices=True)
    n=49;nf=73;y=d['yukawa'];U=d['U'];O=d['O']
    fnull=np.where(d['mF']==0)[0]
    G=np.r_[d['F'].conj(),np.zeros(24)]/np.linalg.norm(d['F'])
    cG=U.conj().T@G
    tangent=np.r_[1.,np.zeros(24),SU5_D]/math.sqrt(31)
    radial=np.r_[tangent.real,tangent.imag]
    phase=np.r_[-tangent.imag,tangent.real]
    cR=O.T@radial;cP=O.T@phase
    parents=groups_low(d['mF2']);scalars=groups_low(d['mS2'])
    rates=[]
    for i in parents:
        M=d['mF'][i];tot=gold=0.
        for k in np.where((d['mS2']>0)&(d['mS2']<M*M))[0]:
            yy=y[i,:,k];ampG=np.dot(yy,cG)
            fac=M/(16*math.pi)*(1-d['mS2'][k]/M**2)**2
            tot+=fac*float(np.sum(abs(yy[fnull])**2))
            gold+=fac*abs(ampG)**2
        flat=0.
        for cc in [cR,cP]:
            yy=np.einsum('ak,k->a',y[i],cc)
            flat+=M/(16*math.pi)*float(np.sum(abs(yy[fnull])**2))
        rates.append({'M':float(M),'Gamma_to_light_scalar_and_null':float(tot),
                      'Gamma_Goldstino_component':float(gold),
                      'Gamma_unbroken_gaugino_component':float(tot-gold),
                      'Gamma_physical_flat_scalar_and_null':float(flat)})
    scalar_rates=[]
    for k in scalars:
        m=math.sqrt(d['mS2'][k]);nn=y[:,:,k][np.ix_(fnull,fnull)]
        gg=m/(16*math.pi)*float(np.sum(abs(nn)**2))
        C=d['cubic'][k];flat=np.array([[a@C@b for b in [cR,cP]] for a in [cR,cP]])
        gflat=float(np.sum(flat**2))/(32*math.pi*m)
        scalar_rates.append({'M':m,'Gamma_two_null_fermions':gg,'Gamma_two_flat_scalars':gflat})
    # The transpose involution is diagonal in this real/imaginary generator basis.
    ca=np.einsum('aij,aji->a',T,T.transpose(0,2,1)).real
    # Explicit trace(Ta Tb^T) evaluated below avoids notation ambiguity.
    ca=np.array([np.trace(t@t.T).real for t in T])
    cm=np.r_[1.,ca,ca];cf=np.r_[cm,-ca];cr=np.r_[cm,cm];cv=-ca
    sy={
      'C_squared':float(max(abs(cm*cm-1))),
      'vacuum':float(max(abs((cm-1)*d['z']))),
      'superpotential_tensor':float(np.max(abs(d['Y']*(cm[:,None,None]*cm[None,:,None]*cm[None,None,:]-1))))/e,
      'fermion_mass':float(np.max(abs(d['MF']*(cf[:,None]*cf[None,:]-1))))/max(d['mF']),
      'scalar_Hessian':float(np.max(abs(d['H']*(cr[:,None]*cr[None,:]-1))))/max(d['mS2']),
      'gauge_representation':float(np.max(abs(d['R']*(cv[:,None,None]*cm[None,:,None]*cm[None,None,:]-1))))
    }
    ext,Cas=ext_basis(d);out=threshold(d,ext);masses,_=summarize(out,Cas)
    iY=np.where(abs(Cas)<1e-7)[0][0];vY=ext[49:,iY]
    Q=np.einsum('a,aij->ij',vY,d['R'])
    chargedS=(np.linalg.norm(Q@d['Em'],axis=0)>1e-7)&(d['mS2']>0)
    RF=np.zeros((73,73),complex);RF[:49,:49]=Q
    RF[49:,49:]=np.einsum('a,aij->ij',vY,d['R'][:,1:25,1:25])
    chargedF=(np.linalg.norm(RF@U,axis=0)>1e-7)&(d['mF']>0)
    gap=min(math.sqrt(min(d['mS2'][chargedS])),min(d['mF'][chargedF]))
    return {'e':e,'X':X,'F_total':float(np.linalg.norm(d['F'])),
            'Goldstino_null_residual':float(np.linalg.norm(d['MF']@G)),
            'Goldstino_null_projection':float(np.sum(abs(cG[fnull])**2)),
            'physical_flat_scalar_H_residual':float(max(np.linalg.norm(d['H']@radial),np.linalg.norm(d['H']@phase))),
            'fermion_parent_count':len(parents),'light_scalar_count':len(scalars),
            'fermion_decays':rates,'light_scalar_tree_decays':scalar_rates,
            'C_controls':sy,'gaugino_masses':masses,'charged_heavy_gap':float(gap),
            'light_scalar_tree_width_max':max(z['Gamma_two_null_fermions']+z['Gamma_two_flat_scalars'] for z in scalar_rates)}

def photino(e=.003):
    X=Z0/math.sqrt(31*e);g=math.sqrt(29/200)*e
    def m(s):
        d=build_model(X*math.exp(s),e,e,g,vertices=False)
        ext,C=ext_basis(d);out,_=summarize(threshold(d,ext),C)
        return out['U1']['signed_mass']
    mass=m(0);slopes=[]
    for h in [.001,.0005]:
        der=(m(-2*h)-8*m(-h)+8*m(h)-m(2*h))/(12*h)
        slopes.append(der/mass)
    # Leading weak radial normalization; finite .01/.03 matching is separately recorded.
    A=Z0**2/e;mr=.0001670533939107*e**1.5
    y=slopes[-1]*mass/math.sqrt(2*A)
    hbar=6.582119569e-25;hc=1.973269804e-14
    target_m=1e-3 # GeV: parent-selected conditional 1 MeV benchmark
    mu=target_m/mass;rho=.3*hc**3;vdisp=.001;n=rho/target_m
    yp=y;mrphys=mu*mr
    feedback=n*yp*yp/(mrphys**2*target_m*vdisp**2)
    width=31*mass**5/(16*math.pi)
    C3=4.63255527e-5;CY=1.11641615058e-4
    return {'e':e,'mhat':mass,'kappa_dlnm_ds':slopes,'A_leading':A,'mrad_hat_leading':mr,
            'radial_yukawa':y,'Gammahat_Goldstino_photon_partial':width,
            'benchmark':{'m_GeV':target_m,'mu_GeV':mu,'rho_GeV_cm3':.3,'vdisp':vdisp,
              'mrad_GeV':mrphys,'feedback_over_ideal_compressibility':feedback,
              'radial_shift_sigma_GeV':n*y/mrphys**2,
              'tau_Goldstino_photon_partial_s':hbar/(mu*width)},
            'SU3_to_U1_mass_ratio':C3/CY,'three_SU3_gaugino_threshold_ratio':3*C3/CY,
            'partial_not_total':True}

def main(path):
    rows=[one(e) for e in [.01,.03]];p=photino()
    checks={}
    for r in rows:
        tag=str(r['e']);checks['C_action_'+tag]=max(r['C_controls'].values())<1e-9
        checks['Goldstino_projection_'+tag]=abs(r['Goldstino_null_projection']-1)<1e-9
        checks['actual_adjoint_decay_'+tag]=min(x['Gamma_to_light_scalar_and_null'] for x in r['fermion_decays'])>0
        checks['tree_scalar_null_channels_zero_'+tag]=r['light_scalar_tree_width_max']<1e-25
        checks['positive_charged_physical_gap_'+tag]=r['charged_heavy_gap']>0
        checks['multiplicities_'+tag]=r['fermion_parent_count']==r['light_scalar_count']==8
    a,b=rows
    err=max(abs(b['fermion_decays'][i]['Gamma_to_light_scalar_and_null']/a['fermion_decays'][i]['Gamma_to_light_scalar_and_null']/(.03/.01)**2.5-1) for i in range(8))
    checks['tree_width_e_5over2_scaling']=err<1e-7
    checks['photino_slope_stencil']=abs(p['kappa_dlnm_ds'][0]/p['kappa_dlnm_ds'][1]-1)<1e-5
    checks['photino_source_positive_compressibility']=p['benchmark']['feedback_over_ideal_compressibility']<1e-6
    checks['three_gaugino_channel_closed']=p['three_SU3_gaugino_threshold_ratio']>1
    out={'claim_id':'TP04-COLD-DECAYS','checks':checks,'cases':rows,'photino':p,
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'width_scaling_error':err,'scope':'Tree adjoint widths; Ward partial photino width; symmetry and source response. No total photino lifetime.'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
