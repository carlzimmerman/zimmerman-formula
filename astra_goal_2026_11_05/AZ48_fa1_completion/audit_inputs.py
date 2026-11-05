#!/usr/bin/env python3
"""Read-only FA1 input inventory; no old driver execution or physical grading."""
import ast,hashlib,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(path):
    import os
    return os.path.relpath(path,ROOT)
def lens_id(value):
    match=re.search(r'J?(\d{4})\d*\.?\d*([+-]\d{4})',value.replace(' ',''))
    return 'J'+match.group(1)+match.group(2) if match else None

def rotation_columns(header):
    # Explicit names only: dispersion, morphological type and a generic V
    # photometric band are not evidence for a resolved rotation measurement.
    allowed={'v/sigma','vsigma','vsig','lambda_r','lambdar','rotation_class','rotclass','fast_slow','vrot','vmax'}
    return [name for name in header if name.strip().lower().replace(' ','') in allowed]

def table_header(text):
    lines=text.splitlines()
    for index,line in enumerate(lines):
        if line.startswith('#') or '\t' not in line:continue
        header=line.split('\t')
        if header[0] in ('recno','name') or 'SDSS' in header:return index,header
    return None,[]

def atomic(path,value):
    import os
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as handle:json.dump(value,handle,indent=2,allow_nan=False);handle.write('\n');handle.flush();os.fsync(handle.fileno())
    os.replace(tmp,path)

def main():
    sources={};checks=[]
    def remember(path):sources[relative(path)]=sha(path)
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    remember(Path(__file__));remember(HERE/'PREPARATION_PLAN.md')
    catalogue=ROOT/'real_research/data/slacs_auger2009_lenses.tsv';atlas=ROOT/'real_research/data/atlas3d_fj_table.tsv'
    tables=[];lens_rows={}
    for path in (catalogue,atlas):
        text=path.read_text(encoding='latin-1');index,header=table_header(text);remember(path)
        tables.append(dict(path=relative(path),header_line=None if index is None else index+1,header=header,rotation_columns=rotation_columns(header)))
        check(path.stem+'_header_parsed',index is not None)
        if path==catalogue:
            for line in text.splitlines()[index+1:]:
                fields=line.split('\t')
                if len(fields)!=len(header):continue
                row=dict(zip(header,fields));name=lens_id(row['SDSS'])
                if name:lens_rows.setdefault(name,[]).append({key:row[key].strip() for key in ('SDSS','sigma','e_sigma','MType')})
    path=ROOT/'campaign_fresh_gravity/CFG713_slacs_required_extra/cfg713_results.json';prior=json.loads(path.read_text());remember(path)
    rosters={foot:sorted(row['name'] for row in prior[foot]['rows']) for foot in ('canonical','alt')}
    check('footing_rosters_identical',rosters['canonical']==rosters['alt'])
    check('rosters_unique',all(len(names)==len(set(names)) for names in rosters.values()))
    rows=[dict(name=name,catalogue_rows=lens_rows.get(name,[]),rotation_measurement=None,rotation_class=None,
          availability='UNKNOWN: inspected catalogue has no resolved rotation field; candidate text search requires manual review',
          footing_availability={foot:'NOT EVALUABLE from inspected rotation inputs' for foot in rosters}) for name in sorted(set(sum(rosters.values(),[])))]
    # Exact bounded search: text formats only, explicit roots, no network/archive extraction.
    command=['rg','-l','-i','--glob','*.tex','--glob','*.tsv','--glob','*.csv','--glob','*.txt',r'\bSLACS\b','real_research/data','../_external_data']
    found=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    if found.returncode not in (0,1):raise RuntimeError('Local SLACS search failed: '+found.stderr)
    paths=sorted(set(found.stdout.splitlines()));candidates=[]
    rotation=re.compile(r'rotat|v\s*/\s*(?:\\?sigma|σ)|lambda[_\\{ ]*R',re.I)
    for name in paths:
        path=ROOT/name;size=path.stat().st_size
        if size>4_000_000:
            candidates.append(dict(path=name,bytes=size,status='NOT READ: exceeds declared4MB text bound'));continue
        remember(path);text=path.read_text(errors='replace');hits=[]
        for number,line in enumerate(text.splitlines(),1):
            if rotation.search(line):hits.append(dict(line=number,excerpt=line.strip()[:240]))
        candidates.append(dict(path=name,bytes=size,status='Text inspected for rotation terms; no automatic class assignment',rotation_term_hits=hits[:80],total_rotation_term_hits=len(hits)))
    marker_specs={
      'campaign_fresh_gravity/CFG713_slacs_required_extra/cfg713.py':['Planck18','cosmo.angular_diameter_distance','sps['],
      'rebuild_2026_10_22/X30_sheet_cluster_profile/x30_sheet_cluster_profile.py':['DA_lcdm','5.364','OB946 = 0.0493','Mgas500','gas(Mg500, R500'],
      'rebuild_2026_10_22/X2_cluster_outskirts/x2_cluster_outskirts.py':['def gas(','0.15*R500','2.2*R500','DA_lcdm'],
      'rebuild_2026_10_22/FA1_fresh_action/I6_galileon/galsolve.py':['Axisymmetric','eps lap(phi)','def derivs(','def solve(']}
    dependencies=[]
    for name,markers in marker_specs.items():
        path=ROOT/name;remember(path);lines=path.read_text().splitlines();evidence=[]
        for marker in markers:
            hit=[dict(line=i+1,text=line.strip()[:300]) for i,line in enumerate(lines) if marker in line]
            check('source_marker_'+name+'_'+marker,bool(hit));evidence.append(dict(marker=marker,occurrences=hit))
        dependencies.append(dict(path=name,evidence=evidence))
    path=ROOT/'rebuild_2026_10_22/FA1_fresh_action/fa1_zeta.py';remember(path);tree=ast.parse(path.read_text());bullet={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('GAS','GAL','PTS'):
            if node.targets[0].id=='PTS':continue # dict call; source coordinates are recorded separately, not executed.
            bullet[node.targets[0].id]=ast.literal_eval(node.value)
    check('Bullet_source_components_parsed',set(bullet)=={'GAS','GAL'})
    bullet=dict(components=bullet,units='mass Msun; Plummer radius and projected centre coordinates kpc; centres z=0',
        signed_component_present=any(row[0]<0 for group in bullet.values() for row in group),
        scope='Inherited phenomenological source prescription; total density positivity, native calibration and full3D solver not yet verified')
    output=dict(status='INPUT AUDIT IN PROGRESS; no physical verdict',checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),
        tables=tables,rosters=rosters,per_lens=rows,search=dict(command=command,matched_files=len(paths),candidates=candidates,
        scope='Only uncompressed tex/tsv/csv/txt in the two named roots; excludes PDFs, archives, other extensions and other roots; term matches are leads, not measurements'),
        dependencies=dependencies,bullet=bullet,source_hashes=sources,
        limitations=['No lens rotation class assigned','No fifteen shear keys calculated','No three-dimensional nonlinear Bullet solve','No old cosmological driver executed','retired sector, adopts nothing; kappa=1/2 FITTED; not theory closed'])
    atomic(HERE/'input_audit.json',output)
    print(json.dumps(dict(checks=output['passed'],total=output['total'],lens_roster=len(rows),matched_text_files=len(paths),rotation_candidates=[x['path'] for x in candidates if x.get('total_rotation_term_hits',0)>0]),indent=2))
    return int(output['passed']!=output['total'])
if __name__=='__main__':raise SystemExit(main())
