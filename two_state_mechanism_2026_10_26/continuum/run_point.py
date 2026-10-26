"""Fixed-nuclei two-electron Coulomb scattering using UKRmol+; no DR rates."""
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent

def replace(text,key,value):
    out,n=re.subn(r'(?mi)^(\s*'+re.escape(key)+r'\s*=)[^!\n]*',lambda m:m[1]+' '+value+', ',text)
    assert n==1,(key,n)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output');p.add_argument('--bin',required=True);p.add_argument('--R',type=float,default=2.);p.add_argument('--nb',type=int,default=15);p.add_argument('--lmax',type=int,default=2);p.add_argument('--radius',type=float,default=20.);p.add_argument('--reference',action='store_true');p.add_argument('--multipole',type=int,default=8);a=p.parse_args()
    w=Path(a.work).resolve();w.mkdir(parents=True,exist_ok=False);(w/'logs').mkdir();template=HERE/'templates';binary=Path(a.bin).resolve();env=dict(os.environ,OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1')
    records=[]
    def run(exe,inp,label):
        if inp is not None:(w/(label+'.inp')).write_text(inp)
        if exe=='scatci_integrals':(w/'inp').write_text(inp)
        t=time.monotonic()
        with (w/'logs'/(label+'.out')).open('w') as out,(w/'logs'/(label+'.err')).open('w') as err:
            proc=subprocess.run([str(binary/exe)],input=inp,text=True,cwd=w,env=env,stdout=out,stderr=err,timeout=900)
        records.append(dict(exe=exe,label=label,returncode=proc.returncode,seconds=time.monotonic()-t))
        (w/'steps.json').write_text(json.dumps(records,indent=2))
        if proc.returncode:raise RuntimeError((label,proc.returncode))
        print(label,round(records[-1]['seconds'],2),flush=True)
    if a.reference:
        assert a.R==1.4
        shutil.copy2(template/'reference.molden',w/'h2+.molden')
    else:
        import numpy as np
        from pyscf import gto,scf,symm,lib
        from pyscf.tools import molden
        lib.num_threads(1)
        mol=gto.M(atom=[('H',(0,0,-a.R/2)),('H',(0,0,a.R/2))],unit='Bohr',basis='aug-cc-pvdz',charge=1,spin=1,symmetry='D2h',verbose=0)
        mf=scf.ROHF(mol).run(conv_tol=1e-12);assert mf.converged
        labels=symm.label_orb_symm(mol,mol.irrep_name,mol.symm_orb,mf.mo_coeff)
        mapping={'Ag':1,'B3u':2,'B2u':3,'B1g':4,'B1u':5,'B2g':6,'B3g':7,'Au':8};counts={k:0 for k in mapping};nums=[]
        for label in labels:counts[label]+=1;nums.append(str(counts[label])+'.'+str(mapping[label]))
        assert [counts[k] for k in mapping]==[5,2,2,0,5,2,2,0],counts
        with (w/'h2+.molden').open('w') as f:
            molden.header(mol,f);molden.orbital_coeff(mol,f,mf.mo_coeff,ene=mf.mo_energy,occ=mf.mo_occ,symm=nums)
        molden_path=w/'h2+.molden'
        molden_path.write_text(molden_path.read_text().replace('[5d]','[5D]').replace('[7f]','[7F]').replace('[9g]','[9G]'))
        (w/'target.json').write_text(json.dumps(dict(R=a.R,ion_energy=mf.e_tot,labels=list(labels)),indent=2))
    inp=(template/'integrals.inp').read_text()
    for key,val in [('a',str(a.radius)),('max_bspline_l',str(a.lmax)),('no_bsplines',str(a.nb))]:
        if key=='max_bspline_l':inp=inp.replace('max_bspline_l = 6','max_bspline_l = '+str(a.lmax))
        else:inp=replace(inp,key,val)
    for l in range(7):inp=replace(inp,'bspline_indices(2,'+str(l)+')',str(a.nb))
    for key in ['max_l_legendre_1el','max_l_legendre_2el']:inp=replace(inp,key,str(a.multipole))
    inp=inp.replace('run_free_scattering = .true.','run_free_scattering = .false.')
    run('scatci_integrals',inp,'integrals')
    log=(w/'log_file.0').read_text();assert 'done:mpi_mod:mpi_mod_finalize' in log
    counts=re.findall(r'3\.1 Orbitals for symmetry\s+(\d+), for target, PCO, continuum\s+(\d+)\s+(\d+)\s+(\d+)',log)
    assert len(counts)==8,counts
    total=[int(t)+int(pc)+int(c) for s,t,pc,c in counts];cont=[int(c) for s,t,pc,c in counts]
    (w/'moints').rename(w/'fort.16')
    for f in sorted(template.glob('target.congen.*.inp')):
        key=f.name[len('target.congen.'):-4]
        run('congen',replace(f.read_text(),'nob',','.join(map(str,total))),'target.congen.'+key)
        run('scatci',(template/('target.scatci.'+key+'.inp')).read_text(),'target.scatci.'+key)
    run('denprop',(template/'target.denprop.inp').read_text(),'target.denprop')
    run('congen',replace((template/'scattering.congen.01.singlet.Ag.inp').read_text(),'nob',','.join(map(str,total))),'scattering.congen')
    inp=replace((template/'scattering.scatci.01.singlet.Ag.inp').read_text(),'notgt',','.join(str(cont[i]) for i in [0,1,2,4,5,6]))
    run('scatci',inp,'scattering.scatci')
    inp=replace((template/'scattering.swinterf.01.singlet.Ag.inp').read_text(),'rmatr',str(a.radius))
    run('swinterf',inp,'scattering.swinterf')
    inp=(template/'scattering.rsolve.01.singlet.Ag.inp').read_text()
    for key,val in [('nescat','5'),('einc','0.002,0.002'),('ieunit','1'),('calcdip','0,0,0'),('raf','80')]:inp=replace(inp,key,val)
    inp=inp.replace('&bprop','&bprop\n nrange = '+str(max(1,int(80-a.radius)))+',')
    run('rsolve',inp,'scattering.rsolve')
    shutil.copy2(w/'fort.19',w/'Kmat.txt')
    run('eigenp',(template/'scattering.eigenp.01.singlet.Ag.inp').read_text(),'scattering.eigenp')
    shutil.copy2(w/'fort.110',w/'eigenphases.txt')
    manifest=dict(settings=vars(a),counts=counts,steps=records,binaries={e:hashlib.sha256((binary/e).read_bytes()).hexdigest() for e in {r['exe'] for r in records}},status='completed_fixed_nuclei_not_DR')
    manifest['inputs_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in w.glob('*.inp')}
    manifest['molden_sha256']=hashlib.sha256((w/'h2+.molden').read_bytes()).hexdigest()
    (w/'result.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if a.output:
        out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(manifest,indent=2)+'\n')
        for name in ['Kmat.txt','eigenphases.txt','h2+.molden','fort.10','fort.21','target.json']:
            if (w/name).exists():shutil.copy2(w/name,out.parent/name)
        shutil.copytree(w/'logs',out.parent/'logs')
        for f in w.glob('*.inp'):shutil.copy2(f,out.parent/f.name)
if __name__=='__main__':main()
