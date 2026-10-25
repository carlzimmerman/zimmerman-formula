"""Reject source/model/geometry changes across a numerical continuation."""
import hashlib,numpy as np

def validate(previous,saved,current_pins,model_paths,physical,s,initial,root):
 assert previous['status'] in ['stopped soft wall budget','stopped memory headroom','finished requested finite interval']
 assert previous['inputs_before']==previous['inputs_after']
 for path,digest in previous['inputs_after'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest, 'changed predecessor input '+path
 for path in model_paths:assert path in previous['inputs_after'] and previous['inputs_after'][path]==current_pins[path], 'changed model '+path
 assert previous['physical']==physical,'changed units'
 for key,value in dict(r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase).items():assert np.array_equal(saved[key],value),'changed grid/carrier '+key
 for key in ['M','K','W','E','Jz']:assert abs(previous['initial_moments'][key]-initial[key])<1e-12*max(1,abs(initial[key])),'changed initial reference '+key
 assert saved['u'].shape==(len(s.r),s.nt,s.nf)
 assert abs(np.sum(abs(saved['u'])**2)-previous['history'][-1]['M'])<1e-11
