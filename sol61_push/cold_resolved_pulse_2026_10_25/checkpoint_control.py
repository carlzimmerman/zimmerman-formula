import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import copy,json,pathlib,types,numpy as np
from checkpoint import validate
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];old=json.loads((P/'runs/protocol_seed.json').read_text());raw=np.load(P/'runs/protocol_seed.npz');saved={k:raw[k] for k in raw.files};s=types.SimpleNamespace(r=saved['r'],w=saved['w'],mu=saved['mu'],aw=saved['aw'],phase=saved['S'],nt=8,nf=8);pins=old['inputs_after'];required=[str((P/'lean.py').relative_to(ROOT))];initial=old['initial_moments'];validate(old,saved,pins,required,old['physical'],s,initial,ROOT);checks=['unchanged accepted']
def reject(name,d=old,sv=saved,units=None,im=None):
 try:validate(d,sv,pins,required,old['physical'] if units is None else units,s,initial if im is None else im,ROOT)
 except AssertionError:checks.append(name+' rejected');return
 raise AssertionError(name+' mutation accepted')
d=copy.deepcopy(old);d['status']='stopped Jz drift >5%';reject('failed accuracy checkpoint',d)
d=copy.deepcopy(old);q=required[0];d['inputs_before'][q]=d['inputs_after'][q]='0'*64;reject('changed predecessor source hash',d)
u=copy.deepcopy(old['physical']);u['eta_code']*=1.1;reject('changed units',units=u)
sv=saved.copy();sv['r']=sv['r'].copy();sv['r'][0]*=1.01;reject('changed radial grid',sv=sv)
im=initial.copy();im['E']+=1e-5;reject('changed energy reference',im=im)
print(json.dumps(dict(checks=checks),indent=2))
