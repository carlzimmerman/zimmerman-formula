#!/usr/bin/env python3
"""Post-result A2: compare like inputs and avoid cancellation in 1-N."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent
all_ok=True
for mode,sign in (('main',1),('mutate',-1)):
    source=HERE/mode/'results.json';raw=json.loads(source.read_text());rows={}
    for foot,record in raw['footings'].items():
        rows[foot]=[]
        for row in record['cases']:
            L,y,n=row['Lstar_pc'],row['y'],row['N']
            m=(L/100000)**2/2
            original=sign*(y*(1+sign*y)+m*(1-n)/n**2)/((1+sign*y)**2+sign*m/n**2)
            delta=float(Decimal(1)-Decimal(str(n)))
            stable=sign*(y*(1+sign*y)+m*delta/n**2)/((1+sign*y)**2+sign*m/n**2)
            with mp.workdps(80):
                l,Y,N=map(mp.mpf,(L,y,n))
                M=(l/100000)**2/2
                binary_reference=sign*(Y*(1+sign*Y)+M*(1-N)/N**2)/((1+sign*Y)**2+sign*M/N**2)
                l,Y,N=(mp.mpf(str(v)) for v in (L,y,n));M=(l/100000)**2/2
                decimal_reference=sign*(Y*(1+sign*Y)+M*(1-N)/N**2)/((1+sign*Y)**2+sign*M/N**2)
                binary_error=float(abs(mp.mpf(original)/binary_reference-1))
                stable_error=float(abs(mp.mpf(stable)/decimal_reference-1))
            rows[foot].append(dict(Lstar_pc=L,y=y,N=n,A=row['A'],matter_z=row['matter_z'],
                original_same_binary_input_relative=binary_error,stable_decimal_input_relative=stable_error))
    checks={f:all(max(r['original_same_binary_input_relative'],r['stable_decimal_input_relative'])<=1e-12 for r in rs) for f,rs in rows.items()}
    result=dict(mode=mode,checks=checks,footings=rows,
        inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),source,HERE/'AMENDMENTS.md')},
        scope='Post-result numerical diagnosis only; original main/mutant precision failures remain.',
        statement='kappa = 1/2 FITTED; not theory closed')
    (HERE/mode/'precision_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
    print(mode,checks,{f:dict(binary=max(r['original_same_binary_input_relative'] for r in rs),stable=max(r['stable_decimal_input_relative'] for r in rs)) for f,rs in rows.items()})
    all_ok=all_ok and all(checks.values())
raise SystemExit(0 if all_ok else 1)
