"""Read-only reconciliation of a newly committed, different real-field model."""
import argparse,csv,hashlib,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OTHER=ROOT/'reviews/cold_collective_phase_2026_10_26'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);start=time.monotonic();declared=json.loads((OTHER/'raw_artifact_hashes.json').read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();checked=[]
 for f,h in declared.items():assert sha(ROOT/f)==h;checked.append(dict(path=f,sha256=h))
 d=json.loads((OTHER/'lattice/result.json').read_text());rows=[]
 for rec in d['rows']:
  f=OTHER/'lattice'/(rec['name']+'.csv');allrows=list(csv.DictReader(f.open()));rr=[{k:float(v) for k,v in row.items()} for row in allrows if float(row['time'])>=30];span=rr[-1]['time']-rr[0]['time'];mean=lambda key:sum((x[key]+y[key])*.5*(y['time']-x['time']) for x,y in zip(rr[:-1],rr[1:]))/span;ratio=mean('pressure')/mean('energy');assert abs(ratio-rec['late_P_over_E'])<1e-12;rows.append(dict(name=rec['name'],late_samples=len(rr),periodic_box_pressure_over_energy=ratio,recorded_max_contrast=rec['max_contrast'],density_pattern_converged=False))
 scales=json.loads((OTHER/'physical_scales.json').read_text());assert len(scales)==5
 for x in checked:assert sha(ROOT/x['path'])==x['sha256']
 result=dict(scope='read-only hash and CSV pressure reconciliation only; no rerun or transfer to CCT gravity or dwarf formation',source_commit='15b4863c1f',source_scope='flat periodic real scalar, supplied energy and fixed uniform baryon background; no cold self-Poisson or dwarf assembly',rows=rows,physical_duration_days=[min(x['time_days'] for x in scales),max(x['time_days'] for x in scales)],physical_box_pc=[min(x['box_pc'] for x in scales),max(x['box_pc'] for x in scales)],raw_artifacts_verified=checked,implication='Spatial self-resonance alone does not establish a cold stable supply. No derived action/kinetic/source bridge to the complex CCT wave proxy; no four-dwarf result follows.',seconds=time.monotonic()-start);(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(verified=len(checked),CSV_cases=len(rows),seconds=result['seconds'])))
if __name__=='__main__':main()
