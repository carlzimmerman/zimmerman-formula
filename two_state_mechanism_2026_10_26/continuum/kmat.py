"""UKRmol formatted K data: upper triangle by columns, energy in Rydbergs."""
from pathlib import Path
import numpy as np

def read_k(path):
    lines=Path(path).read_text().splitlines();i=5;rows=[]
    while i<len(lines):
        line=lines[i];n=int(line[:10]);nd=int(line[10:20]);count=int(line[20:30]);energy=float(line[30:].replace('D','E'))/2
        assert nd==0 and count==n*(n+1)//2
        i+=1;values=[]
        while len(values)<count:
            line=lines[i];i+=1
            values.extend(float(line[j:j+20].replace('D','E')) for j in range(0,len(line),20) if line[j:j+20].strip())
        assert len(values)==count
        K=np.zeros((n,n));q=0
        for col in range(n):
            for row in range(col+1):K[row,col]=K[col,row]=values[q];q+=1
        ident=np.eye(n);S=np.linalg.solve(ident-1j*K,ident+1j*K)
        rows.append(dict(energy_au=energy,K=K.tolist(),S_real=S.real.tolist(),S_imag=S.imag.tolist(),eigenphase_sum=float(np.arctan(np.linalg.eigvalsh(K)).sum()),unitarity_error=float(np.linalg.norm(S.conj().T@S-ident))))
    return rows
