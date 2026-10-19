import json,sys,itertools
from fractions import Fraction as F
from pathlib import Path
import sympy as s
base=Path(__file__).parent
inp=json.loads((base/'INPUTS.json').read_text())
rows=[]; assertions=0; configs=0
for pp in inp['probability_zero']:
    p=F(pp); prob={-1:(1-p)/2,0:p,1:(1-p)/2}
    for n in range(inp['N_min'],inp['N_max']+1):
        norm=es=eq=ess=eqq=F(0)
        for qs in itertools.product(inp['states'],repeat=n):
            w=F(1)
            for q in qs:w*=prob[q]
            ss=sum(q*q for q in qs);qq=sum(qs)
            assert ss>=abs(qq);assertions+=1;configs+=1
            norm+=w;es+=w*ss;eq+=w*qq;ess+=w*ss*ss;eqq+=w*qq*qq
        vs=ess-es*es;vq=eqq-eq*eq
        assert norm==1 and eq==0;assertions+=2
        assert es==n*(1-p);assertions+=1
        assert vs==n*p*(1-p) and vq==n*(1-p);assertions+=2
        assert ess>=eqq and vs>=vq-es*es;assertions+=2
        assert vs<vq and vs-vq==-n*(1-p)**2;assertions+=2
        rows.append({'p_zero':str(p),'N':n,'states_summed':3**n,'mean_S':str(es),'variance_S':str(vs),'variance_Q':str(vq),'connected_gap':str(vs-vq),'raw_gap':str(ess-eqq)})
z,theta,j,N=s.symbols('z theta j N',positive=True,real=True)
L=N*s.log(1+2*z*s.exp(-j)*s.cos(theta))
ps=1/(1+2*z)
exact=[s.diff(L,j,2).subs({j:0,theta:0})-N*ps*(1-ps),-s.diff(L,theta,2).subs({j:0,theta:0})-N*(1-ps)]
H,Om,E,t=s.symbols('H Om E t',positive=True,real=True)
V=Om/H**4;W=E*V
rho=-H*s.diff(W,H)/(4*V)
exact += [rho-E,s.diff(E*Om*s.exp(4*t),t,2)-4*s.diff(E*Om*s.exp(4*t),t)]
for e in exact:assert s.simplify(e)==0;assertions+=1
result={'assertion_tested':'Finite positive unconditioned ensemble refutes raw-to-connected variance ordering inferred solely from S>=|Q|; corrected inequality and normalized log derivatives checked. Flat density has zero curvature-difference coefficient.','exact_symbolic_identities':len(exact),'finite_cases':len(rows),'configurations_summed':configs,'assertions':assertions,'rows':rows,'outcome':'Abstract inference refuted; not a microscopic QCD counterexample or rejection of its low-energy theorem. Source application requires independent connected/contact prescription.','physical_A_computed':False,'physical_R_computed':False,'alpha_input':False}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['exact_symbolic_identities','finite_cases','configurations_summed','assertions','outcome']}))
