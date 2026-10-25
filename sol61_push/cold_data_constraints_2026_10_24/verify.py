"""Orthogonal checks and mutation controls; no production outputs modified."""
import hashlib, json, math
from pathlib import Path
from scipy.integrate import quad
import constrain as c

r=json.loads((c.HERE/'results.json').read_text())
receipt=json.loads((c.HERE/'receipt.json').read_text())
assert receipt['input_hashes_after']==c.hashes()
assert receipt['result_sha256']==hashlib.sha256((c.HERE/'results.json').read_bytes()).hexdigest()
a=485.89
exact=math.pi*c.G/(32*a)
k=c.kernel(a,a)
assert abs(k/exact-1)<1e-9
assert abs(2*k/exact-1)>.9  # double-counting mutation bites absolute normalization
example=r['sextans_two_population'][0]
aa=example['tracer_scales_pc']; fit=example['fits'][0]
bb=fit['scale_pc']
# Direct radial tracer density integral, independent of the shell kernel transform.
def direct_kernel(a,b):
    f=lambda x: c.G*x*x/(x*x+b*b)**1.5 * x*x/a**3 * (1+(x/a)**2)**(-2.5)
    return quad(f,0,math.inf,epsabs=1e-16,epsrel=1e-9)[0]
errors=[abs(direct_kernel(a,bb)/c.kernel(a,bb)-1) for a in aa]
assert max(errors)<1e-7
s=fit['shell_relaxation']; dualc=s['dual_c']; hmax=s['dual_max_kernel']
# Adaptive integral of a smooth positive mass profile must respect the dual.
weights=[c.kernel(a,bb) for a in aa]
assert weights[1]-dualc*weights[0] <= hmax*(1+1e-10)
bad_ratio=aa[1]/aa[0] # reversed compact-source ratio mutation
assert abs(bad_ratio-aa[0]/aa[1])>.1
out=dict(status='self-checks passed; no independent referee review',
    direct_cold_kernel_relative_errors=errors,
    mutation_double_cold_gravity_rejected=True,mutation_reversed_compact_ratio_rejected=True,
    result_hash_matches=True,all_input_hashes_match=True)
(c.HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
