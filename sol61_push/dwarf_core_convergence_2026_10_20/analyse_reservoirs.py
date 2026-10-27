"""Read completed saved states; separate subgroup spin from bulk orbital J."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from reservoir_decomposition import decompose
HERE=Path(__file__).resolve().parent

def analyse(case):
    folder=HERE/('run_'+case)
    manifest=json.loads((folder/'manifest.json').read_text())
    if manifest['run']['status']!='completed':raise ValueError('completed record required: '+case)
    data=json.loads((folder/'results.json').read_text());a=np.load(folder/'initial.npz');b=np.load(folder/'final.npz')
    m,cold=b['m'],b['cold'];r=np.linalg.norm(b['x']-data['snapshots'][-1]['centre'],axis=1)
    groups=dict(final_core=cold&(r<=300),other_cold=cold&(r>300),stars=~cold)
    initial=decompose(a['x'],a['v'],m,a['phi'],groups);final=decompose(b['x'],b['v'],m,b['phi'],groups)
    differences={}
    for name in groups:
        before,after=initial['groups'][name],final['groups'][name]
        delta={key:(np.asarray(after[key])-before[key]).tolist() for key in ('Jspin','Jcentre','Jallocated','Kwithin','Kcentre','Uallocated','Eallocated')}
        receipt=data['fixed_membership_groups'][name]
        delta.update(host_work_allocated=receipt['host_work'],host_torque_allocated=receipt['host_torque'],
                     original_energy_allocation_residual=float(delta['Eallocated']-receipt['delta_E']),
                     original_J_allocation_residual=float(np.linalg.norm(np.asarray(delta['Jallocated'])-receipt['delta_J'])))
        differences[name]=delta
    return dict(case=case,initial=initial,final=final,fixed_membership_changes=differences,
                global_maxima=data['maxima'],elastic_energy_defect=data['collision_energy_defect'],elastic_J_defect=data['collision_J_defect'],
                input_sha256={name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ('initial.npz','final.npz','results.json','manifest.json')},
                conventions=['Same final300pc-selected cold particle identities at both endpoints; complementary cold and all stars',
                             'Different runs generally select different final particle memberships',
                             'Group spin uses own COM/bulk; group-centre J uses all-original-particle COM',
                             'Potential allocation includes half cross-group interaction energy and is not isolated binding',
                             'Stored host receipts use the all-original COM frame, not subgroup-local spin/work',
                             'Convergence is assessed separately; failed-energy/unresolved records retain their labels'])

def main():
    p=argparse.ArgumentParser();p.add_argument('--case',action='append',required=True);p.add_argument('--output',required=True);args=p.parse_args()
    output=Path(args.output)
    if output.exists():raise FileExistsError('fresh reservoir analysis directory required')
    rows=[analyse(case) for case in args.case];output.mkdir(parents=True)
    (output/'reservoirs.json').write_text(json.dumps(dict(cases=rows),indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(cases=args.case,output=str(output/'reservoirs.json'))))

if __name__=='__main__':main()
