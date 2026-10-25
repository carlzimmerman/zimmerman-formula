"""Bounded analytic controls; NOT a nonlinear cluster-formation simulation."""
import argparse, csv, json, math
from pathlib import Path
import numpy as np

ROOT = Path('reviews/cold_rapid_assembly_2026_10_25')
N = 200000

def capture(q, mutate=False):
    r2 = ((1 if mutate else 2) / q**2)**2 - 1
    return min(1., max(0., r2)**1.5 / 4**3)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    ap.add_argument('--mutate', action='store_true')
    args = ap.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    # Independently classify final energies on equal-volume initial cells.
    r = 4 * ((np.arange(N)+.5)/N)**(1/3)
    captures=[]
    for q in [.25,.5,.75,1.,1.25,1.5,2.]:
        numerical = float(np.mean(.5*q*q - 1/np.sqrt(1+r*r) < 0))
        exact = capture(q,args.mutate)
        assert abs(exact-numerical) <= 1/N, 'capture energy threshold mismatch'
        captures.append(dict(q=q,bound_fraction=exact,quadrature=numerical))
    # Phase-mixed orbits: dt/dE_anomaly = (1-e cos E)/n.
    E = (np.arange(N)+.5)*2*np.pi/N
    orbits=[]
    for e in [.2,.6,.9]:
        if e <= .5:
            exact=0.
        else:
            E0=math.acos(.5/e)
            exact=(E0-e*math.sin(E0))/math.pi
        radial=1-e*np.cos(E)
        weight=1-e*np.cos(E)
        numerical=float(np.mean(weight*(radial < .5)))
        assert abs(exact-numerical) <= 2/N, 'orbit residence-time mismatch'
        assert abs(float(np.mean(weight))-1) < 1e-12
        # Vis-viva energy = -1/2 at every phase, GM=a=1.
        v2=2/radial-1
        assert np.max(np.abs(.5*v2-1/radial+.5)) < 1e-12
        orbits.append(dict(e=e,energy_per_mass=-.5,net_vector_spin=0,
                           pericentre=1-e,apocentre=1+e,
                           enclosed_fraction_at_half_a=exact,quadrature=numerical))
    # rg=-GM²/W; 2T+W=0 implies E=-GM²/(2rg).
    mergers=[]
    for orbital in [-1.,0.,1.]:
        Etotal=-2+orbital
        rg=4/(2-orbital)
        assert abs(-4/rg-Etotal)<1e-12
        mergers.append(dict(orbital_energy_units=orbital,final_rg_over_initial_rg=rg,
                            assumption='virial endpoints; no ejecta or work; necessary only'))
    rows=list(csv.DictReader(open('reviews/cold_wave_relaxation_2026_10_25/run/timescales.csv')))
    # Select sigma=vc, one of three rows per source shell, not independent data.
    crossing=[]
    conversion=3.085677581491367e16/1000/(1e9*365.25*86400)
    for row in rows:
        if float(row['sigma_factor']) != 1.: continue
        t=float(row['r_pc'])/float(row['sigma_kms'])*conversion
        crossing.append(dict(footing=row['footing'],name=row['name'],model=row['model'],
                             shell=int(row['shell']),t_R_over_vc_Gyr=t))
    assert len(crossing)==303
    source=json.load(open('reviews/cold_shell_covariance_2026_10_24/run_selective/result.json'))
    requirements=[]
    for footing,systems in source['footings'].items():
        for name,system in systems.items():
            for model in system['models']:
                requirements.append(dict(footing=footing,name=name,model=model['model'],
                    Mc_R500_Msun=model['Mc'][-1],negative_shells=model['negative_shells']))
    assert len(requirements)==70
    result=dict(scope='analytic and tracer-limit controls; not full assembly simulation',
        captures=captures,orbits=orbits,merger_energy_constraints=mergers,
        crossing_summary=dict(count=len(crossing),min_Gyr=min(x['t_R_over_vc_Gyr'] for x in crossing),
                              max_Gyr=max(x['t_R_over_vc_Gyr'] for x in crossing)),
        crossing_rows=crossing,cluster_mass_requirements=requirements,
        checks=['capture vs equal-volume energy classification','orbit time weighting',
                'orbit vis-viva energy','merger virial energy identity','source case counts'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['scope','captures','orbits','merger_energy_constraints','crossing_summary']},indent=2))
if __name__=='__main__': main()
