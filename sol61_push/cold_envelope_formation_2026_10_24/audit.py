"""Bounded READ-ONLY provenance/serialization audit of saved CCT-009 evidence."""
import argparse,ast,array,hashlib,json,math,pathlib,struct,sys,zipfile
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
# Present archived producer bytes can resolve a historical original filename.
pool={}
for f in P.rglob('*'):
 if f.is_file() and not any(x.startswith('audit_') for x in f.relative_to(P).parts) and '__pycache__' not in f.parts:pool.setdefault(sha(f),str(f.relative_to(ROOT)))
records=[];unresolved=[]
for f in sorted(list(P.glob('*.json'))+list((P/'runs').glob('*.json'))):
 if f.name in ['CLOSEOUT_RECEIPT.json','audit_contract.json']:continue
 q=json.loads(f.read_text());before=q.get('source_hashes_before',q.get('inputs_before'));after=q.get('source_hashes_after',q.get('inputs_after'))
 if before is None:continue
 assert before==after,('runtime inputs changed',str(f))
 matches=[]
 for name,h in before.items():
  options=[ROOT/name,P/name,P/'runs'/name];found=next((str(v.relative_to(ROOT)) for v in options if v.is_file() and sha(v)==h),None) or pool.get(h)
  if found is None:unresolved.append((f.name,name,h))
  matches.append({'recorded_name':name,'sha256':h,'resolved_to':found})
 records.append({'record':str(f.relative_to(P)),'runtime_inputs_unchanged':True,'resolved_inputs':matches})
claude=json.loads((P/'CLAUDE_READ_ONLY_CHECK.json').read_text())
assert all(sha(ROOT/name)==dig for name,dig in claude['files_sha256'].items())
raw={f.stem:json.loads(f.read_text()) for f in sorted((P/'runs').glob('*.json'))};statuses=[];parents=[]
def norm_npy(blob):
 assert blob[:6]==b'\x93NUMPY';major=blob[6];nbytes=2 if major==1 else 4;hlen=int.from_bytes(blob[8:8+nbytes],'little');start=8+nbytes;header=ast.literal_eval(blob[start:start+hlen].decode('latin1'));assert header['descr'] in ['<c16','=c16','|c16'];values=array.array('d');values.frombytes(blob[start+hlen:]);
 if sys.byteorder!='little':values.byteswap()
 return math.fsum(x*x for x in values)
for tag,q in raw.items():
 hs=q['history'];ini=q['initial'];last=hs[-1];fields=P/'runs'/f'{tag}_fields.npz';assert fields.is_file()
 with zipfile.ZipFile(fields) as z:
  ni=norm_npy(z.read('initial.npy'));nf=norm_npy(z.read('final.npy'));initialbytes=z.read('initial.npy')
 assert abs(ni-ini['M'])<1e-10 and abs(nf-last['M'])<1e-10,(tag,ni,nf)
 scale=q.get('energy_ledger_scale_code',max(abs(ini['E']),1e-12));computed=(last['E']+last['removed']['E']-last['source_work']-ini['E'])/scale
 if 'E_residual' in last:assert abs(computed-last['E_residual'])<1e-10,(tag,computed,last['E_residual'])
 maxE=max(abs(h.get('E_residual',0)) for h in hs);maxJ=max(abs(h.get('J_residual',0)) for h in hs);maxM=max(abs(h.get('M_residual',0)) for h in hs)
 statuses.append({'tag':tag,'kind':'preflight' if q['parameters']['T']==0 else 'dynamics','producer_status':q['status'],'strict_ledger_pass':maxE<.01 and maxJ<.01 and maxM<1e-8,'max_E_residual':maxE,'max_J_residual':maxJ,'max_M_residual':maxM,'field_initial_norm_error':ni-ini['M'],'field_final_norm_error':nf-last['M'],'peak_RSS_bytes':q['peak_RSS_bytes'],'source_revision':q['revision']})
 parent=q['parameters'].get('resume')
 if parent:
  pq=raw[parent];assert hs[:len(pq['history'])]==pq['history'],tag
  with zipfile.ZipFile(P/'runs'/f'{parent}_fields.npz') as z:assert initialbytes==z.read('initial.npy'),tag
  parents.append({'child':tag,'parent':parent,'history_prefix_unchanged':True,'original_initial_field_unchanged':True,'parent_dt':pq['parameters']['dt'],'child_dt':q['parameters']['dt']})
assert not unresolved,unresolved
assert all(v['peak_RSS_bytes']<10**9 for v in statuses)
strictfails=[v['tag'] for v in statuses if not v['strict_ledger_pass']];assert set(strictfails)=={'sextans_monopole','sextans_monopole_dt005'},strictfails
out={'status':'saved evidence audit completed; physical theory/formation goal not complete','structured_input_records_checked':records,'raw_record_count':len(raw),'raw_records':statuses,'resume_checks':parents,'strict_numerical_failures_retained':strictfails,'maximum_observed_dynamics_RSS_bytes':max(v['peak_RSS_bytes'] for v in statuses),'interpretation':'Positive finite mode transfer/transport; no stable four-dwarf or real-star safety pass. Frame audit and unresolved fragment intrinsic spin must accompany original-origin diagnostics.','residual_provenance_limits':['Underlying raw dynamics used custom before/after SHA records rather than this standardized runner; this v2 run audits stored evidence, not reexecutes dynamics.','Individual original dynamics start timestamps/per-run software fingerprints were not recorded; none invented.','Supplementary inline notes are not promoted to independently executed physical proofs.'],'input_resolution_failures':unresolved}
path=pathlib.Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n');print('Audited',len(raw),'raw records and',len(records),'derived records;',len(parents),'resume chains; all stored input pins resolved.');print('Strict numerical failures retained:',strictfails);print('Max recorded dynamics RSS:',out['maximum_observed_dynamics_RSS_bytes']);print('No physical four-dwarf completion claimed.')
