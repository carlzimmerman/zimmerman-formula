"""Finite-F radial couplings on conditional saved TP05 stationary rows."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize,Z0
MULT={'SU3':8,'SU2':3,'U1':1}
def profile(t,e):
    d=build_model(t*Z0/math.sqrt(31*e),e,e,math.sqrt(29/200)*e,vertices=False)
    ext,C=ext_basis(d);r,deg=summarize(threshold(d,ext),C)
    gap=math.sqrt(min(d['mS2'][d['mS2']>0].min(),d['mF2'][d['mF2']>0].min(),d['mV2'][d['mV2']>0].min()))
    return {k:r[k]['signed_mass'] for k in MULT},float(gap),deg
def widths(row,slopes):
    R=row['R_GeV'];m=row['m_sigma_GeV'];a=row['m_phase_GeV'];F=row['mu_GeV']**2/math.sqrt(31)
    mi=row['gauginos_GeV'];sig={};phase={}
    for k,di in MULT.items():
        sig[k]=di*(slopes[k]*mi[k]/(math.sqrt(2)*R))**2*m/(16*math.pi)*max(0,1-4*(mi[k]/m)**2)**1.5
        phase[k]=di*(mi[k]/(math.sqrt(2)*R))**2*a/(16*math.pi)*math.sqrt(max(0,1-4*(mi[k]/a)**2))
    r=(a/m)**2
    sig['aa']=m**3/(64*math.pi*R*R)*(1-r)**2*math.sqrt(max(0,1-4*r))
    sig['GG']=m**5/(32*math.pi*F*F)
    phase['GG']=a**5/(32*math.pi*F*F)
    # Deliberately loose unmatched heavy-anomaly envelope C<=10 per factor,
    # |light triangle|<=10 per factor. Total envelope includes all 12 bosons.
    # L=(c/4)a F Ftilde with c<=20*g^2/(8pi^2 sqrt(2)R).
    g=math.sqrt(29/200)*row['e'];c=20*g*g/(8*math.pi**2*math.sqrt(2)*R)
    anomaly=12*c*c*a**3/(64*math.pi)
    return dict(sigma=sig,phase=phase,sigma_total=sum(sig.values()),phase_total=sum(phase.values()),phase_gauge_unmatched_upper_envelope=anomaly,phase_gauge_envelope_over_total=anomaly/sum(phase.values()),m32_over_sigma=row['m32_GeV']/m,m32_over_phase=row['m32_GeV']/a)
def main(out):
    start=time.monotonic();src=json.loads((ROOT/'reviews/gravity_vacuum_production_2026_11_01/canonical_gravity/run_shape/result.json').read_text());rows=[]
    for r in src['points']:
        if abs(r['e']-.003)>1e-12:continue
        m0,gap,deg=profile(r['t'],r['e']);ss=[]
        for h in (.001,.0005):
            vals=[profile(r['t']*math.exp(j*h),r['e'])[0] for j in (-2,-1,1,2)]
            ss.append({k:(vals[0][k]-8*vals[1][k]+8*vals[2][k]-vals[3][k])/(12*h*m0[k]) for k in MULT})
        masserr=max(abs(m0[k]*r['mu_GeV']/r['gauginos_GeV'][k]-1) for k in MULT)
        slerr=max(abs(ss[0][k]-ss[1][k])/max(abs(ss[1][k]),1e-20) for k in MULT)
        q=dict(r);q.update(logmass_slopes=ss[-1],slope_stencil_relative_error=slerr,mass_reconstruction_relative_error=masserr,min_heavy_gap_GeV=gap*r['mu_GeV'],subgroup_degeneracy_error=deg,widths=widths(r,ss[-1]));rows.append(q)
    checks=dict(seven_rows=len(rows)==7,mass_reconstruction=max(r['mass_reconstruction_relative_error'] for r in rows)<1e-7,slope_convergence=max(r['slope_stencil_relative_error'] for r in rows)<1e-4,has_open_closed=any(r['phase_open'] for r in rows) and any(not r['phase_open'] for r in rows),goldstino_equivalence_hierarchy=max(r['widths']['m32_over_phase'] for r in rows)<1e-3,anomaly_envelope_subpercent=max(r['widths']['phase_gauge_envelope_over_total'] for r in rows)<.01)
    result=dict(claim_id='GC03_PRODUCTION_KERNELS_CONDITIONAL',checks=checks,rows=rows,scope='Conditional rigid finite-F slopes on saved leading-tilt stationary branch, not reconciled finite SUGRA pole vertices',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,rows=[dict(t=r['t'],mchi=r['photino_GeV'],ms=r['m_sigma_GeV'],ma=r['m_phase_GeV'],slopes=r['logmass_slopes'],widths=r['widths']) for r in rows]),indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
