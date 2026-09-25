import itertools, torch, numpy as np
from toy import *
torch.manual_seed(0)
# qubits, n=6, one plaquette + 2 off sites
for (n,q) in [(6,2),(5,3)]:
    toy = Toy(n, q, [(0,1,2,3)] + ([(2,3,4,5)] if n==6 else []))
    sets = [M for r in range(1,n+1) for M in itertools.combinations(range(n), r) if set(M)&{0,1,2,3}]
    S = toy.family_struct(sets)
    for k in (1,3,8,9):
        Ss=[S]*k; pars=[torch.randn(S['npar'],dtype=CD) for _ in range(k)]
        Vl=[torch.randn(q**4,q**4,dtype=CD) for _ in toy.plaqs]
        v1=toy.nested(Ss,pars,Vl)
        v2=dense_check(toy,Ss,pars,Vl) if toy.dim<=729 else None
        print(n,q,k, float(v1.abs().max()), None if v2 is None else float((v1-v2).abs().max()))
