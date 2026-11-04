"""Canonical scalar gauge-annihilation discriminator on actual oldcold packets."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parent));import numpy as np
from gauge_basis_v1 import build
from probe_v3 import relative_density

def main(out):
 start=time.monotonic();stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];probe=json.loads((HERE.parent/'run_coulomb003/result.json').read_text());x=old['history'][-1]['x_minimum'];b=build(x);Sc=next(g for g in b['s']['groups'] if g['id']=='Sc_0');ids=np.array(Sc['indices']);vid=np.r_[b['vgroups']['V8'],b['vgroups']['V3'],b['vgroups']['V1']];Q=b['qs'][np.ix_(vid,ids,ids)];vals,U=np.linalg.eigh(Q[-1]);V=U[:,vals>0];t=np.einsum('ia,kij,jb->kab',V.conj(),Q,V,optimize=True);d=6;Gamma=np.zeros((d*d,d*d),complex);pot=np.zeros_like(Gamma)
 for a in t:
  pot-=np.kron(a,a.conj())
  for c in t:
   v=(a@c+c@a).ravel();Gamma+=np.outer(v,v.conj())
 lam,R=np.linalg.eigh(pot);decomp=[]
 for value in (-2.5,-1.5,-1.,0.):
  v=R[:,abs(lam-value)<1e-8];trace=float(np.trace(v.conj().T@Gamma@v).real);decomp.append(dict(potential_coefficient=value,multiplicity=v.shape[1],annihilation_trace=trace,annihilation_weight=trace/float(np.trace(Gamma).real)))
 Cann=float(np.trace(Gamma).real/(d*d));g=math.sqrt(29/200)*.003;alpha=g*g/(4*math.pi);m=.003/2*math.sqrt(x*x+2/(31*.003));born=g**4*Cann/(32*math.pi*m*m);edges=np.array(stage['q_edges']);rows=[];logedges=np.linspace(-12,math.log10(2*edges[-1]),601);z,w=np.polynomial.legendre.leggauss(6);lq=(logedges[:-1,None]+logedges[1:,None])/2+(logedges[1:,None]-logedges[:-1,None])*z/2;r=10**lq.ravel();rw=(w[None,:]*(logedges[1:,None]-logedges[:-1,None])/2*math.log(10)*10**lq).ravel()
 for name,ff,pr in [('stage_initial',stage['initial_fS'],probe['cases'][0]),('stage_final',stage['final_fS'],probe['cases'][1]),('hybrid_final',old['final_f_S_number_normalization'],probe['cases'][2])]:
  f=2*np.array(ff);T=pr['Tc'];H=pr['H_mu'];n=pr['n_mu3'];density=relative_density(r,edges,f);u=T/m*r;S=np.zeros_like(u);lowprob=0.;channel=[]
  for c in decomp:
   ae=-c['potential_coefficient']*alpha;xx=2*math.pi*ae/np.maximum(u,1e-300);ss=np.ones_like(u) if ae<1e-30 else xx/(-np.expm1(-xx));mean=float(np.sum(rw*density*ss));bad=u<ae;frac=float(np.sum((rw*density*ss)[bad])/max(mean,1e-300));prob=float(np.sum((rw*density)[bad]));channel.append(dict(potential=c['potential_coefficient'],mean_Coulomb_Sommerfeld=mean,alphaeff_over_v_gt1_probability=prob,alphaeff_over_v_gt1_annihilation_fraction=frac));S+=c['annihilation_weight']*ss;lowprob=max(lowprob,prob)
  savg=float(np.sum(rw*density*S));rows.append(dict(name=name,Tc=T,H_mu=H,scalar_mass_mu=m,born_sigma_v_mu_minus2=born,born_chemical_fractional_loss_over_H=n/2*born/H,Coulomb_reference_Sommerfeld_average=savg,Coulomb_reference_chemical_loss_over_H=n/2*born/H*savg,channel_weights=channel,max_low_velocity_probability=lowprob,screening_masses_mu=pr['Debye_masses_mu'],most_attractive_alpha_mu_over_screen=float(2.5*alpha*m/2/min(pr['Debye_masses_mu'])),mean_relative_kinetic_to_max_binding=float((T*T/m*np.sum(f*(edges[1:]**5-edges[:-1]**5)/5)/np.sum(f*(edges[1:]**3-edges[:-1]**3)/3))/(m*(2.5*alpha)**2/4))))
 checks=dict(colour=bool(abs(Cann-13/4)<1e-10),potential_multiplicities=bool([c['multiplicity'] for c in decomp]==[1,3,8,24]),positive=bool(min(c['annihilation_trace'] for c in decomp)>0),commuting_channels=bool(np.linalg.norm(pot@Gamma-Gamma@pot)<1e-10),cold_Born_small=bool(max(r['born_chemical_fractional_loss_over_H'] for r in rows)<1e-10))
 Path(out).write_text(json.dumps(dict(colour_annihilation_factor=Cann,colour_channels=decomp,cases=rows,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualcoldSc0C-Cstar→all12unbrokengaugepairs canonicalthresholds-wave; transverse scalar-exchange/s-channel vanishatrest, leavingseagull. Exactcanonicalcolourtrace+actualrelative-distributionCoulombSommerfeldreference. Screenedcolourpotentialcanhaveboundstates/shallowresonances; currentbulkkineticenergyandlowvweightreported. ThisdoesnotboundarbitrarilylateSommerfeld/boundformationorreplacefullSommerfeldcoupled-channelcalculation. WarmrelativisticF/vectorannihilationnotcoveredbythresholdscalarformula.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
