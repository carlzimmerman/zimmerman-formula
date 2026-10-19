import json
import pathlib
import sys
import mpmath as mp


def value(x,dps):
    with mp.workdps(dps):
        a=mp.sqrt(mp.mpf(x)**2-1);N=256;K=40
        finite=mp.fsum(1/(n*n+a*a) for n in range(1,N+1))
        terms=[(-a*a)**k*mp.zeta(2*k+2,N+1) for k in range(K+1)]
        tail=mp.fsum(terms)
        spec=(-mp.mpf('0.5')-a*a*(finite+tail))/(2*mp.pi**2*mp.mpf(x))
        exact=-a*mp.coth(mp.pi*a)/(4*mp.pi*mp.mpf(x))
        return {'finite':finite,'tail':tail,'spec':spec,'exact':exact,'terms':terms}


rows=[]
for x in [5,30]:
    reference=value(x,160)
    for dps in [70,90,95]:
        v=value(x,dps)
        with mp.workdps(170):
            errors={k:str(abs(v[k]-reference[k])) for k in ['finite','tail','spec','exact']}
            term_errors=[(i,abs(t-reference['terms'][i])) for i,t in enumerate(v['terms'])]
            worst=max(term_errors,key=lambda it:it[1])
            rows.append({'mR':x,'dps':dps,'component_errors_vs_160dps':errors,'within_precision_identity_error':str(abs(v['spec']-v['exact'])),'worst_tail_term_index':worst[0],'worst_tail_term_absolute_error':str(worst[1])})
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
(out/'diagnostic.json').write_text(json.dumps({'status':'diagnostic-completed','rows':rows},indent=2)+'\n')
print(json.dumps(rows))
