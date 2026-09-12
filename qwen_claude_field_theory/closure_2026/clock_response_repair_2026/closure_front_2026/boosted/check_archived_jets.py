#!/usr/bin/env python3
"""Evaluate derived coefficients on every archived aligned exterior jet."""
import argparse
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[2]
SOURCE=BASE/'inhomogeneous_charge_2026/exterior/run_001/result.json'


def main():
    raw=json.loads(SOURCE.read_text());rows=[]
    for row in raw['rows']:
        j=row['jets'];q=row['physical_Q'];s=row['clock_rate'];g=row['gamma'];M=row['M2']
        H=row['hessian_cov'];p=j['PX'];r=j['PXX'];W=j['W'];d=j['WY']
        K=2*p+4*q*q*r+12*g*H[1][1]+6*g*g*q**4/M
        G=2*p-2*s*d*W/(W-2*q*q*d)+4*g*(-H[0][0]+2*H[1][1])-2*g*g*q**4/M
        old=row['principal'];errors=[abs(K-old['K']),abs(G-old['G'])]
        assert max(errors)<1e-12
        assert row['Y']==0
        rows.append(dict(index=row['index'],K=K,G=G,speed_squared=G/K,archive_errors=errors,static_dust_coupling=g*q*q/M))
    return dict(scope='Re-evaluation of rounded archived physical jets, not a new ODE solve or interval certificate.',input_path=str(SOURCE),input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),rows=rows,all_K_positive=all(r['K']>0 for r in rows),negative_G_count=sum(r['G']<0 for r in rows),positive_G_count=sum(r['G']>0 for r in rows),interpretation='Negative G rows have a principal hyperbolicity obstruction. Positive G rows satisfy the conditional moving cone only for source speeds exceeding sqrt(G/K); neither their full health nor a localized moving source has been solved.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    text=json.dumps(main(),indent=2)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text,end='')
